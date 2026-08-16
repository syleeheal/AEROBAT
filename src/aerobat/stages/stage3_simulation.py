"""AEROBAT Stage 3: matched simulation runs with simulator and subject agents."""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from aerobat.storage.artifacts import MATCHED_SIMULATION_RUNS
from aerobat.storage.schema import runtime_artifact
from aerobat.runtime.cache import compact_sequence_id, prompt_cache_key
from aerobat.utils import collect_fallbacks, mapping_value, record_fallback
from aerobat.runtime.llm import (
    limited_llm_call_with_metadata,
    limited_structured_llm_call,
    make_llm_call_kwargs,
)
from aerobat.protocol.prompts import MatchedSimulationPrompts
from aerobat.protocol.formats import resolve_format
from aerobat.storage.ids import RunId
from aerobat.protocol.payloads import PayloadManager
from aerobat.protocol.stage_parsing import parse_simulator_agent_batch
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import now

logger = logging.getLogger(__name__)


# Some providers (e.g. Moonshot/KIMI) reject empty user messages, whereas OpenAI
# tolerates them. When the Simulator Agent produced no subject-facing content for a
# round, this placeholder keeps the conversation valid across every provider.
EMPTY_ROUND_PLACEHOLDER = "(No new information was provided this round. Please continue.)"


@dataclass(frozen=True)
class TranscriptContext:
    repetition: int
    group_id: Any
    resolved_format: str
    subject_agent_model: str
    simulator_agent_model: str
    simulator_agent_options: Dict[str, Any]
    created_at: str


@dataclass
class SimulationRunState:
    """Mutable conversation and transcript state for one configured run $S_{ij}$."""

    simulation: Dict[str, Any]
    subject_agent_options: Dict[str, Any]
    rounds: List[Dict[str, Any]]
    subject_agent_messages: List[Dict[str, Any]]
    prompts: Dict[str, List[Dict[str, Any]]]

    @classmethod
    def initialize(
        cls,
        *,
        simulation: Dict[str, Any],
        subject_agent_options: Dict[str, Any],
        subject_agent_system_prompt: str,
        simulator_agent_system_prompt: str,
    ) -> "SimulationRunState":
        conversation = PayloadManager.subject_agent_state(
            subject_agent_system_prompt=subject_agent_system_prompt,
            simulator_agent_system_prompt=simulator_agent_system_prompt,
        )
        return cls(
            simulation=simulation,
            subject_agent_options=subject_agent_options,
            rounds=conversation["rounds"],
            subject_agent_messages=conversation["subject_agent_messages"],
            prompts=conversation["prompts"],
        )

    def run_id(self, repetition: int) -> RunId:
        return RunId.from_mapping({**self.simulation, "repetition": repetition})

    def restore(self, saved: Dict[str, Any], simulator_agent_system_prompt: str) -> None:
        """Restore the conversation fields from a partial transcript artifact."""
        saved_prompts = saved.get("prompts", {})
        subject_prompts = saved_prompts.get("stage_3_subject_agent", [])
        messages: List[Dict[str, Any]] = []
        if subject_prompts:
            messages.append(
                PayloadManager.chat_message(
                    "system",
                    subject_prompts[0].get("system", ""),
                )
            )
            for entry in subject_prompts[1:]:
                restored_input = (
                    str(entry.get("input", "") or "").strip()
                    or EMPTY_ROUND_PLACEHOLDER
                )
                messages.append(PayloadManager.chat_message("user", restored_input))
                messages.append(
                    {
                        "role": "assistant",
                        "content": PayloadManager.subject_agent_assistant_message(
                            entry.get("output", ""),
                            entry.get("reasoning_summary", ""),
                        ),
                    }
                )

        self.rounds = list(saved.get("rounds", []))
        self.subject_agent_messages = messages
        self.prompts = {
            "stage_3_subject_agent": list(subject_prompts),
            "stage_3_simulator_agent": list(
                saved_prompts.get(
                    "stage_3_simulator_agent",
                    [{"system": simulator_agent_system_prompt}],
                )
            ),
        }

    def transcript(
        self,
        *,
        simulation_id: str,
        context: TranscriptContext,
        fallbacks: List[Dict[str, Any]],
        updated_at: str,
        partial: bool,
        target_rounds: int | None = None,
    ) -> Dict[str, Any]:
        metadata = {
            "subject_agent_model": context.subject_agent_model,
            "simulator_agent_model": context.simulator_agent_model,
            "subject_agent_reasoning_effort": self.subject_agent_options["reasoning_effort"],
            "subject_agent_reasoning_summary": self.subject_agent_options["reasoning_summary"],
            "simulator_agent_reasoning_effort": context.simulator_agent_options["reasoning_effort"],
            "subject_agent_service_tier": self.subject_agent_options["service_tier"],
            "simulator_agent_service_tier": context.simulator_agent_options["service_tier"],
            "subject_agent_prompt_cache_key": self.subject_agent_options["prompt_cache_key"],
            "simulator_agent_prompt_cache_key": context.simulator_agent_options["prompt_cache_key"],
            "subject_agent_prompt_cache_retention": self.subject_agent_options[
                "prompt_cache_retention"
            ],
            "simulator_agent_prompt_cache_retention": context.simulator_agent_options[
                "prompt_cache_retention"
            ],
            "subject_agent_temperature": self.subject_agent_options["temperature"],
            "simulator_agent_temperature": context.simulator_agent_options["temperature"],
            "subject_agent_max_tokens": self.subject_agent_options["max_tokens"],
            "simulator_agent_max_tokens": context.simulator_agent_options["max_tokens"],
            "created_at": context.created_at,
            "updated_at": updated_at,
            "partial": partial,
            **self.run_id(context.repetition).as_dict(),
            "simulation_id": simulation_id,
            "group_id": context.group_id,
            "causal_variable": self.simulation.get("causal_variable"),
            "causal_value": self.simulation.get("causal_value"),
            "environment_rendering_format": context.resolved_format,
            "simulation_format": context.resolved_format,
            "total_rounds": len(self.rounds),
        }
        if target_rounds is not None:
            metadata["target_rounds"] = target_rounds

        payload: Dict[str, Any] = {"metadata": metadata}
        if partial:
            payload["passes_stage4"] = False
        payload.update(
            {
                "rounds": self.rounds,
                "token_counts": TranscriptManager.build_token_counts(
                    prompts=self.prompts
                ),
                "prompts": self.prompts,
                "fallbacks": [
                    fallback
                    for fallback in fallbacks
                    if fallback.get("simulation_id") in (None, simulation_id)
                ],
            }
        )
        return payload


def _agent_options(
    simulation_cfg: Dict[str, Any],
    agent_key: str,
    model: str,
    *,
    default_max_tokens: int,
) -> Dict[str, Any]:
    temperature_key = f"{agent_key}_temperature"
    if temperature_key not in simulation_cfg:
        raise ValueError(f"simulation.{temperature_key} must be configured.")
    service_tier = simulation_cfg.get("service_tier", "NA")
    prompt_cache_key = simulation_cfg.get("prompt_cache_key", "NA")
    prompt_cache_retention = simulation_cfg.get("prompt_cache_retention", "NA")
    return {
        "model": model,
        "temperature": float(simulation_cfg[temperature_key]),
        "max_tokens": int(simulation_cfg.get(f"{agent_key}_max_tokens", default_max_tokens)),
        "reasoning_effort": simulation_cfg.get(f"{agent_key}_reasoning_effort", "NA"),
        "service_tier": simulation_cfg.get(f"{agent_key}_service_tier", service_tier),
        "prompt_cache_key": simulation_cfg.get(f"{agent_key}_prompt_cache_key", prompt_cache_key),
        "prompt_cache_retention": simulation_cfg.get(
            f"{agent_key}_prompt_cache_retention",
            prompt_cache_retention,
        ),
        "reasoning_summary": simulation_cfg.get(f"{agent_key}_reasoning_summary", "NA"),
    }


INTERACTION_LENGTH_ROUNDS = (2, 4, 8)


def rounds_from_interaction_length(value: Any) -> int:
    if isinstance(value, int) and value in INTERACTION_LENGTH_ROUNDS:
        return value

    text = str(value or "").strip().lower()
    for num_rounds in INTERACTION_LENGTH_ROUNDS:
        if text == f"{num_rounds} rounds":
            return num_rounds

    choices = ", ".join(f"{num_rounds} rounds" for num_rounds in INTERACTION_LENGTH_ROUNDS)
    raise ValueError(f"interaction_length must be one of [{choices}], got {value!r}")


def load_saved_matched_simulation_runs(
    *,
    results_dir: str | Path,
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    simulation_config: Any,
) -> Dict[str, Dict[str, Any]]:
    """Load Stage 3 artifacts for every selected hypothesized causal variable."""
    per_hypothesis_results: Dict[str, Dict[str, Any]] = {}
    missing_payloads = []
    for hypothesis_id in simulation_config.selected_hypothesis_ids:
        config_design = matched_configurations_by_id[hypothesis_id]
        result = TranscriptManager.load_matched_simulation_runs(
            results_dir=results_dir,
            hypothesis_id=hypothesis_id,
            config_design=dict(config_design),
            num_rounds_fallback=rounds_from_interaction_length(
                mapping_value(config_design.get("hypothesis")).get("interaction_length")
            ),
        )
        if result is None:
            missing_payloads.append(
                str(Path(results_dir) / hypothesis_id / MATCHED_SIMULATION_RUNS)
            )
        else:
            per_hypothesis_results[hypothesis_id] = result

    if missing_payloads:
        raise FileNotFoundError(
            "Missing saved matched_simulation_runs.json for:\n" + "\n".join(missing_payloads)
        )
    return per_hypothesis_results


async def _run_simulator_agent_batch_turn(
    *,
    round_num: int,
    num_rounds: int,
    simulation_group: Dict[str, Any],
    histories_by_simulation: Dict[str, List[Dict[str, Any]]],
    resolved_format: str,
    simulator_agent_sys: str,
    simulator_agent_options: Dict[str, Any],
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> tuple[Dict[str, str], str, str, Dict[str, Any] | None, str]:
    simulator_agent_prompt = MatchedSimulationPrompts.make_simulator_agent_simulation_prompt(
        round_number=round_num,
        num_rounds=num_rounds,
        histories_by_simulation=histories_by_simulation,
        simulation_group=simulation_group,
        format_name=resolved_format,
    )

    messages = PayloadManager.messages(simulator_agent_sys, simulator_agent_prompt)
    simulations = simulation_group["simulations"]
    call_kwargs = make_llm_call_kwargs(**simulator_agent_options)
    simulation_ids = [PayloadManager.simulation_id(simulation) for simulation in simulations]
    try:
        # Prefer structured batch output so the Simulator Agent returns one message
        # for every simulation id.
        structured = await limited_structured_llm_call(
            messages,
            response_format=PayloadManager.simulator_agent_response_format(simulation_ids),
            parser=parse_simulator_agent_batch,
            llm_semaphore=llm_semaphore,
            **call_kwargs,
        )
        simulator_agent_output = structured.text or json.dumps(
            structured.parsed,
            ensure_ascii=False,
        )
        outputs_by_simulation = PayloadManager.simulator_agent_outputs_from_contract(
            structured.parsed,
            simulations,
        )
        token_counts = structured.token_counts
        response_id = structured.response_id
    except ValueError as exc:
        record_fallback(
            "simulation_contract_unsupported_model",
            "_run_simulator_agent_batch_turn",
            "Simulator Agent model does not support structured response schemas; "
            "used plain text batch parsing.",
            model=simulator_agent_options["model"],
            error=str(exc),
        )
        llm_response = await limited_llm_call_with_metadata(
            messages,
            llm_semaphore=llm_semaphore,
            **call_kwargs,
        )
        simulator_agent_output = llm_response.text
        token_counts = llm_response.token_counts
        response_id = llm_response.response_id
        outputs_by_simulation = PayloadManager.simulator_agent_outputs(
            simulator_agent_output,
            simulations,
        )
    return (
        outputs_by_simulation,
        simulator_agent_prompt,
        simulator_agent_output,
        token_counts,
        response_id,
    )


async def _run_subject_agent_turn(
    *,
    simulator_agent_message: str,
    resolved_format: str,
    subject_agent_options: Dict[str, Any],
    subject_agent_messages: List[Dict[str, Any]],
    round_num: int,
    prompts: Dict[str, List[Dict[str, Any]]],
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> tuple[str, str, str]:
    subject_agent_facing_message = PayloadManager.extract_subject_agent_payload(
        simulator_agent_message,
        format_name=resolved_format,
    )
    if not subject_agent_facing_message:
        subject_agent_facing_message = PayloadManager.strip_planning_tags(simulator_agent_message)

    subject_agent_input_message = MatchedSimulationPrompts.make_subject_agent_round_prompt(
        current_simulation=subject_agent_facing_message,
    )

    # If the Simulator Agent produced no subject-facing content this round, substitute a
    # minimal non-empty placeholder so providers that reject empty user turns still work.
    if not subject_agent_input_message.strip():
        record_fallback(
            "subject_agent_empty_round_message",
            "_run_subject_agent_turn",
            "Simulator Agent produced no subject-facing message this round; "
            "substituted a placeholder to satisfy providers that reject empty user turns.",
            round=round_num,
        )
        subject_agent_input_message = EMPTY_ROUND_PLACEHOLDER

    prompts["stage_3_subject_agent"].append(
        TranscriptManager.build_prompt_record(round_num, subject_agent_input_message, "")
    )

    subject_agent_messages.append(PayloadManager.chat_message("user", subject_agent_input_message))
    subject_agent_result = await limited_llm_call_with_metadata(
        subject_agent_messages,
        llm_semaphore=llm_semaphore,
        **make_llm_call_kwargs(**subject_agent_options),
    )

    subject_agent_response = subject_agent_result.text
    subject_agent_reasoning_summary = subject_agent_result.reasoning_summary
    subject_agent_messages.append(
        {
            "role": "assistant",
            "content": PayloadManager.subject_agent_assistant_message(
                subject_agent_response,
                subject_agent_reasoning_summary,
            ),
        }
    )
    prompt_record = prompts["stage_3_subject_agent"][-1]
    prompt_record.pop("output", None)
    if subject_agent_reasoning_summary:
        prompt_record["reasoning_summary"] = subject_agent_reasoning_summary
    prompt_record["token_counts"] = subject_agent_result.token_counts
    prompt_record["response_id"] = subject_agent_result.response_id
    prompt_record["output"] = subject_agent_response
    return subject_agent_response, subject_agent_facing_message, subject_agent_reasoning_summary


def _restore_partial_transcripts(
    *,
    states: Dict[str, SimulationRunState],
    simulation_dir: Path | None,
    repetition: int,
    num_rounds: int,
    simulator_agent_sys: str,
    label: str,
    verbose: bool,
) -> str:
    created_at = now()
    if simulation_dir is None:
        return created_at

    manager = TranscriptManager(simulation_dir)
    restored_created_at = False
    for simulation_id, state in states.items():
        path = manager.simulation_path(state.run_id(repetition))
        if not path.exists():
            continue
        try:
            saved = runtime_artifact(path.name, json.loads(path.read_text()))
            metadata = saved.get("metadata", {})
            rounds = saved.get("rounds")
            is_partial = metadata.get("partial") or (
                isinstance(rounds, list) and len(rounds) < num_rounds
            )
            if isinstance(rounds, list) and rounds and is_partial:
                state.restore(saved, simulator_agent_sys)
                if not restored_created_at and metadata.get("created_at"):
                    created_at = metadata["created_at"]
                    restored_created_at = True
        except Exception as exc:
            if verbose:
                logger.warning(
                    "[%s] Could not load partial for %s: %s",
                    label,
                    simulation_id,
                    exc,
                )
    return created_at


def _build_transcripts(
    *,
    states: Dict[str, SimulationRunState],
    context: TranscriptContext,
    fallbacks: List[Dict[str, Any]],
    partial: bool,
    target_rounds: int | None = None,
) -> Dict[int, Dict[str, Any]]:
    updated_at = now()
    transcripts: Dict[int, Dict[str, Any]] = {}
    for simulation_id, state in states.items():
        if partial and not state.rounds:
            continue
        transcripts[int(state.simulation["value_index"])] = state.transcript(
            simulation_id=simulation_id,
            context=context,
            fallbacks=fallbacks,
            updated_at=updated_at,
            partial=partial,
            target_rounds=target_rounds,
        )
    return transcripts


def _save_partial_transcripts(
    *,
    states: Dict[str, SimulationRunState],
    simulation_dir: Path | None,
    num_rounds: int,
    context: TranscriptContext,
    fallbacks: List[Dict[str, Any]],
    label: str,
    verbose: bool,
) -> None:
    if simulation_dir is None:
        return

    manager = TranscriptManager(simulation_dir)
    partials = _build_transcripts(
        states=states,
        context=context,
        fallbacks=fallbacks,
        partial=True,
        target_rounds=num_rounds,
    )
    for transcript in partials.values():
        metadata = transcript["metadata"]
        manager.save_simulation_transcript(
            transcript=transcript,
            run=RunId.from_mapping(metadata),
        )
        if verbose:
            logger.info(
                "[%s] Saved partial: %s (%s/%s rounds)",
                label,
                metadata["simulation_id"],
                metadata["total_rounds"],
                num_rounds,
            )


async def _append_simulation_round(
    *,
    simulation_id: str,
    state: SimulationRunState,
    simulator_agent_message: str,
    simulator_agent_prompt: str,
    simulator_agent_output: str,
    simulator_agent_token_counts: Dict[str, Any] | None,
    simulator_agent_response_id: str,
    resolved_format: str,
    round_num: int,
    llm_semaphore: Optional[asyncio.Semaphore],
) -> None:
    prompts = state.prompts
    prompts["stage_3_simulator_agent"].append(
        TranscriptManager.build_prompt_record(
            round_num,
            simulator_agent_prompt,
            simulator_agent_output,
            source="simulation_group",
            simulation_id=simulation_id,
            simulation_output=simulator_agent_message,
            token_counts=simulator_agent_token_counts,
            response_id=simulator_agent_response_id,
        )
    )
    response, perceived_simulation, reasoning_summary = await _run_subject_agent_turn(
        simulator_agent_message=simulator_agent_message,
        resolved_format=resolved_format,
        subject_agent_options=state.subject_agent_options,
        subject_agent_messages=state.subject_agent_messages,
        round_num=round_num,
        prompts=prompts,
        llm_semaphore=llm_semaphore,
    )
    state.rounds.append(
        PayloadManager.simulation_round_from_messages(
            round_num=round_num,
            simulator_agent_message=simulator_agent_message,
            subject_agent_response=response,
            subject_agent_reasoning_summary=reasoning_summary,
            subject_agent_facing_message=perceived_simulation,
        )
    )


async def run_matched_simulation_group(
    behavior_name: str,
    simulation_group: Dict[str, Any],
    num_rounds: int,
    subject_agent_model: str,
    simulator_agent_model: str,
    repetition: int,
    simulation_format: Optional[str] = None,
    simulation_cfg: Optional[Dict[str, Any]] = None,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    verbose: bool = True,
    simulation_dir: Optional[Path] = None,
) -> Dict[int, Dict[str, Any]]:
    """Run one repetition of a matched simulation group for the requested rounds."""
    with collect_fallbacks() as fallbacks:
        simulations = [dict(simulation) for simulation in simulation_group.get("simulations", [])]
        if not simulations:
            raise ValueError("simulation group is empty.")
        simulation_group = {**simulation_group, "simulations": simulations}
        first_simulation = simulations[0]
        label = f"{simulation_group.get('group_id', 'simulation_group')}:r{repetition}"
        if verbose:
            logger.info(
                "[%s] Starting matched simulation group (%s runs, %s rounds).",
                label,
                len(simulations),
                num_rounds,
            )

        # Resolve simulation format and model options once for the whole batch.
        simulation_cfg = simulation_cfg or {}
        resolved_format = (
            simulation_format
            or simulation_group.get("environment_rendering_format")
            or resolve_format(first_simulation)
        )
        default_max_tokens = int(simulation_cfg.get("max_tokens", 5000))
        subject_agent_options = _agent_options(
            simulation_cfg,
            "subject_agent",
            subject_agent_model,
            default_max_tokens=default_max_tokens,
        )
        simulator_agent_options = _agent_options(
            simulation_cfg,
            "simulator_agent",
            simulator_agent_model,
            default_max_tokens=default_max_tokens,
        )
        causal_variable = (
            simulation_group.get("causal_var")
            or first_simulation.get("causal_variable")
            or first_simulation.get("causal_var")
        )
        simulator_agent_options = {
            **simulator_agent_options,
            "prompt_cache_key": prompt_cache_key(
                simulator_agent_options["prompt_cache_key"],
                "s3",
                "sim",
                behavior_name,
                causal_variable,
                compact_sequence_id(simulation_group.get("group_id") or label),
                f"r{repetition}",
            ),
        }

        simulator_agent_sys = MatchedSimulationPrompts.make_simulator_agent_system_prompt(
            simulation_group=simulation_group,
        )
        states: Dict[str, SimulationRunState] = {}
        # Each simulation keeps independent rounds, Subject Agent chat history,
        # and prompt transcripts.
        for simulation in simulations:
            simulation_id = PayloadManager.simulation_id(simulation)
            simulation_subject_agent_options = {
                **subject_agent_options,
                "prompt_cache_key": prompt_cache_key(
                    subject_agent_options["prompt_cache_key"],
                    "s3",
                    "sub",
                    behavior_name,
                    simulation.get("causal_variable") or causal_variable,
                    compact_sequence_id(simulation_id),
                    f"r{repetition}",
                ),
            }
            subject_agent_sys = MatchedSimulationPrompts.make_subject_agent_system_prompt(
                rules=simulation.get("rules"),
                subject_agent_role=simulation.get("subject_agent"),
            )
            states[simulation_id] = SimulationRunState.initialize(
                simulation=simulation,
                subject_agent_options=simulation_subject_agent_options,
                subject_agent_system_prompt=subject_agent_sys,
                simulator_agent_system_prompt=simulator_agent_sys,
            )

        created_at = _restore_partial_transcripts(
            states=states,
            simulation_dir=simulation_dir,
            repetition=repetition,
            num_rounds=num_rounds,
            simulator_agent_sys=simulator_agent_sys,
            label=label,
            verbose=verbose,
        )
        transcript_context = TranscriptContext(
            repetition=repetition,
            group_id=simulation_group.get("group_id"),
            resolved_format=resolved_format,
            subject_agent_model=subject_agent_model,
            simulator_agent_model=simulator_agent_model,
            simulator_agent_options=simulator_agent_options,
            created_at=created_at,
        )

        min_completed = min(len(state.rounds) for state in states.values())
        start_round = min_completed + 1
        if min_completed > 0 and verbose:
            logger.info(
                "[%s] Resuming from round %s (%s rounds already done).",
                label,
                start_round,
                min_completed,
            )

        try:
            for round_num in range(start_round, num_rounds + 1):
                if verbose:
                    logger.info("[%s] Round %s/%s", label, round_num, num_rounds)

                # Prepare every history the Simulator Agent sees before generating
                # the next batch turn.
                histories_by_simulation = {
                    simulation_id: PayloadManager.history_entries(state.rounds)
                    for simulation_id, state in states.items()
                }

                (
                    outputs_by_simulation,
                    simulator_agent_prompt,
                    simulator_agent_output,
                    simulator_agent_token_counts,
                    simulator_agent_response_id,
                ) = await _run_simulator_agent_batch_turn(
                    round_num=round_num,
                    num_rounds=num_rounds,
                    simulation_group=simulation_group,
                    histories_by_simulation=histories_by_simulation,
                    resolved_format=resolved_format,
                    simulator_agent_sys=simulator_agent_sys,
                    simulator_agent_options=simulator_agent_options,
                    llm_semaphore=llm_semaphore,
                )

                await asyncio.gather(
                    *(
                        _append_simulation_round(
                            simulation_id=simulation_id,
                            state=state,
                            simulator_agent_message=outputs_by_simulation.get(simulation_id, ""),
                            simulator_agent_prompt=simulator_agent_prompt,
                            simulator_agent_output=simulator_agent_output,
                            simulator_agent_token_counts=simulator_agent_token_counts,
                            simulator_agent_response_id=simulator_agent_response_id,
                            resolved_format=resolved_format,
                            round_num=round_num,
                            llm_semaphore=llm_semaphore,
                        )
                        for simulation_id, state in states.items()
                    )
                )

        except Exception:
            _save_partial_transcripts(
                states=states,
                simulation_dir=simulation_dir,
                num_rounds=num_rounds,
                context=transcript_context,
                fallbacks=fallbacks,
                label=label,
                verbose=verbose,
            )
            raise
        return _build_transcripts(
            states=states,
            context=transcript_context,
            fallbacks=fallbacks,
            partial=False,
        )
