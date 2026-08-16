"""Research-manager ranking, coherence, and fidelity gates plus reports."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from aerobat.protocol.constants import (
    OVERALL_VALIDITY_SCALE,
    STAGE4_INCLUDED_VALIDITY_RATINGS,
)
from aerobat.protocol.normalization import NormalizationManager
from aerobat.runtime.cache import compact_sequence_id, settings_with_cache_key
from aerobat.runtime.llm import (
    limited_llm_call_with_metadata,
    llm_call_kwargs,
    resolve_research_manager_settings,
)
from aerobat.protocol.prompts import ResearchManagerPrompts
from aerobat.protocol.prompt_utils import prompt_json
from aerobat.protocol.stage_parsing import (
    parse_final_report_response,
    parse_research_manager_review,
    parse_stage_one_review,
    parse_stage_two_review,
)
from aerobat.storage.ids import RunId
from aerobat.protocol.payloads import PayloadManager
from aerobat.runtime.concurrency import gather_after_first
from aerobat.stages.stage2_config_design import simulations_by_run
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import collect_fallbacks, research_manager_gate_enabled

logger = logging.getLogger(__name__)


def _save_stage_one_review(
    hypothesis: Dict[str, Any],
    results_dir: str | Path,
    fallbacks: List[Dict[str, Any]],
) -> None:
    hypothesis["token_counts"] = TranscriptManager.build_token_counts(
        prompts=hypothesis.get("prompts"),
        research_manager_prompt=hypothesis.get("research_manager_prompt"),
    )
    hypothesis["research_manager_fallbacks"] = list(fallbacks)
    TranscriptManager(results_dir).save_stage_output("hypothesis_generation.json", hypothesis)


async def run_ranking_gate(
    config: Dict[str, Any],
    results_dir: str | Path,
    hypothesis: Dict[str, Any],
) -> Dict[str, Any]:
    hypotheses = [
        item
        for item in hypothesis.get("hypotheses", [])
        if isinstance(item, dict)
    ]
    enabled = research_manager_gate_enabled(config, "stage_1")
    hypothesis.setdefault("meta_data", {})["research_manager_stage_1"] = enabled

    if not enabled:
        for rank, item in enumerate(hypotheses, start=1):
            item["research_manager_review"] = {
                "rank": rank,
                "rationale": "",
                "passes_stage2": True,
            }
        hypothesis["research_manager_prompt"] = []
        _save_stage_one_review(hypothesis, results_dir, [])
        return hypothesis

    system_prompt = ResearchManagerPrompts.make_system_prompt()
    user_prompt = ResearchManagerPrompts.stage_one_review_prompt(
        behavior_name=hypothesis["behavior_name"],
        behavior_hypothesis=hypothesis.get("definition", ""),
        hypotheses=hypotheses,
    )

    logger.info("Calling the research-manager ranking gate after Stage 1.")
    with collect_fallbacks() as fallbacks:
        llm_response = await limited_llm_call_with_metadata(
            PayloadManager.messages(system_prompt, user_prompt),
            **llm_call_kwargs(resolve_research_manager_settings(config, "stage_1")),
        )
        response = llm_response.text
        hypothesis["research_manager_prompt"] = [
            {"system": system_prompt},
            TranscriptManager.build_prompt_record(
                1,
                user_prompt,
                response,
                source="stage_one_review",
                token_counts=llm_response.token_counts,
                response_id=llm_response.response_id,
            ),
        ]
        try:
            reviews = parse_stage_one_review(response, hypotheses)
        except Exception:
            _save_stage_one_review(hypothesis, results_dir, fallbacks)
            raise

    for item in hypotheses:
        variable = NormalizationManager.text_value(item.get("variable"))
        item["research_manager_review"] = reviews[variable]
    PayloadManager.mark_stage2_hypothesis_selection(
        hypotheses,
        int(
            NormalizationManager.object_value(hypothesis.get("meta_data")).get(
                "num_stage2_hypotheses"
            )
            or len(hypotheses)
        ),
    )
    _save_stage_one_review(hypothesis, results_dir, fallbacks)
    logger.info(
        "Hypotheses selected for Stage 2: %s",
        sum(PayloadManager.should_pass_hypothesis_to_stage2(item) for item in hypotheses),
    )
    return hypothesis


def _save_stage_two_review(
    config_design: Dict[str, Any],
    save_path: str | Path,
    fallbacks: List[Dict[str, Any]],
) -> None:
    config_design["token_counts"] = TranscriptManager.build_token_counts(
        prompts=config_design.get("prompts"),
        research_manager_prompt=config_design.get("research_manager_prompt"),
    )
    config_design["research_manager_fallbacks"] = list(fallbacks)
    storage_payload = {
        key: value
        for key, value in config_design.items()
        if key not in {"hypothesis", "stage1_hypothesis", "path"}
    }
    path = Path(save_path)
    TranscriptManager(path.parent).save_stage_output(path.name, storage_payload)


def _mark_stage_three_config_selection(config_design: Mapping[str, Any], passes: bool) -> None:
    for domain_result in config_design.get("domain_results", []):
        if not isinstance(domain_result, dict):
            continue
        pass_three_by_tag = NormalizationManager.object_value(
            domain_result.get("pass_three")
        )
        for pass_three in pass_three_by_tag.values():
            if isinstance(pass_three, dict):
                pass_three["passes_stage3"] = passes


async def run_coherence_gate(
    config: Dict[str, Any],
    config_design: Dict[str, Any],
    save_path: str | Path,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> Dict[str, Any]:
    enabled = research_manager_gate_enabled(config, "stage_2")
    config_design.setdefault("meta_data", {})["research_manager_stage_2"] = enabled
    if not enabled:
        _mark_stage_three_config_selection(config_design, True)
        config_design["research_manager_prompt"] = []
        _save_stage_two_review(config_design, save_path, [])
        return config_design

    variable_hypothesis = NormalizationManager.object_value(
        config_design.get("hypothesis")
    )
    if not variable_hypothesis:
        raise ValueError(
            "Stage 2 research manager requires the Stage 1 hypothesis for this "
            "matched-configuration design."
        )

    logger.info(
        "Calling the research-manager coherence gate after Stage 2 for %s.",
        config_design.get("variable") or variable_hypothesis.get("variable"),
    )
    settings = resolve_research_manager_settings(config, "stage_2")
    system_prompt = ResearchManagerPrompts.make_system_prompt()
    prompt_records: List[Dict[str, Any]] = [{"system": system_prompt}]
    calls = []
    prompts = []

    async def call(user_prompt: str) -> Any:
        return await limited_llm_call_with_metadata(
            PayloadManager.messages(system_prompt, user_prompt),
            llm_semaphore=llm_semaphore,
            **llm_call_kwargs(settings),
        )

    for domain_result in config_design.get("domain_results", []):
        if not isinstance(domain_result, dict):
            continue
        pass_two = NormalizationManager.object_value(domain_result.get("pass_two"))
        pass_three_by_tag = NormalizationManager.object_value(domain_result.get("pass_three"))
        for value_set_tag, pass_three in pass_three_by_tag.items():
            if not isinstance(pass_three, dict):
                continue
            review_group = PayloadManager.stage_two_review_group(
                domain=NormalizationManager.text_value(domain_result.get("domain")),
                value_set_tag=value_set_tag,
                environment_rendering_format=NormalizationManager.text_value(
                    domain_result.get("environment_rendering_format")
                ),
                fixed_values=NormalizationManager.object_value(pass_two.get(value_set_tag)),
                pass_three=pass_three,
            )
            user_prompt = ResearchManagerPrompts.stage_two_review_prompt(
                hypothesis=variable_hypothesis,
                simulation_group=review_group,
            )
            calls.append(call(user_prompt))
            prompts.append((domain_result, value_set_tag, user_prompt))

    with collect_fallbacks() as fallbacks:
        responses = await asyncio.gather(*calls)
        for (domain_result, value_set_tag, user_prompt), llm_response in zip(prompts, responses):
            response = llm_response.text
            pass_three = domain_result["pass_three"][value_set_tag]
            pass_three["research_manager_review"] = parse_stage_two_review(response)
            pass_three["passes_stage3"] = PayloadManager.stage_two_review_passes_stage3(pass_three)
            prompt_records.append(
                TranscriptManager.build_prompt_record(
                    1,
                    user_prompt,
                    response,
                    source=f"stage_two_review_{value_set_tag}",
                    value_set_tag=value_set_tag,
                    domain=domain_result.get("domain"),
                    variable=config_design.get("variable"),
                    token_counts=llm_response.token_counts,
                    response_id=llm_response.response_id,
                )
            )

    config_design["research_manager_prompt"] = prompt_records
    _save_stage_two_review(config_design, save_path, fallbacks)
    return config_design


def _passes_fidelity_gate(transcript: Mapping[str, Any]) -> bool:
    review = transcript.get("research_manager_review")
    rating = (
        ((review or {}).get("overall_validity") or {}).get("rating")
        if isinstance(review, Mapping)
        else None
    )
    normalized_rating = NormalizationManager.normalize_choice(rating, OVERALL_VALIDITY_SCALE)
    return normalized_rating in STAGE4_INCLUDED_VALIDITY_RATINGS


async def _run_research_manager(
    variable_typology: Dict[str, Dict[str, Any]],
    simulation_group: Dict[str, Any],
    simulation_history: List[Dict[str, Any]],
    variable_names_: List[str],
    settings: Any,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    system_prompt = ResearchManagerPrompts.make_system_prompt()
    user_prompt = ResearchManagerPrompts.stage_three_review_prompt(
        variable_typology=variable_typology,
        simulation_group=simulation_group,
        simulation_history=simulation_history,
    )
    llm_response = await limited_llm_call_with_metadata(
        PayloadManager.messages(system_prompt, user_prompt),
        llm_semaphore=llm_semaphore,
        **llm_call_kwargs(settings),
    )
    response = llm_response.text
    parsed = parse_research_manager_review(response, variable_names_)
    return parsed, [
        {"stage": "research_manager", "system": system_prompt},
        TranscriptManager.build_prompt_record(
            1,
            user_prompt,
            response,
            stage="research_manager",
            token_counts=llm_response.token_counts,
            response_id=llm_response.response_id,
        ),
    ]


async def judge_stage_three_record(
    record: Dict[str, Any],
    records: List[Dict[str, Any]],
    settings: Any,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> Dict[str, Any]:
    with collect_fallbacks() as fallbacks:
        variable_typology = PayloadManager.variable_typology(record["simulation"])
        variable_names_ = PayloadManager.variable_names(variable_typology)
        simulation_group = PayloadManager.research_manager_group(
            records,
            evaluated_record=record,
        )
        simulation_history = [
            dict(row)
            for row in record.get("transcript", {}).get("rounds", [])
            if isinstance(row, dict)
        ]

        review, prompts = await _run_research_manager(
            variable_typology=variable_typology,
            simulation_group=simulation_group,
            simulation_history=simulation_history,
            variable_names_=variable_names_,
            settings=settings,
            llm_semaphore=llm_semaphore,
        )

        return {
            "research_manager_review": review,
            "research_manager_prompt": prompts,
            "research_manager_fallbacks": list(fallbacks),
        }


async def run_fidelity_gate(
    config: Dict[str, Any],
    *,
    behavior_name: str,
    simulation_group: Mapping[str, Any],
    transcripts_by_index: Dict[int, Dict[str, Any]],
    repetition: int,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    verbose: bool = True,
) -> Dict[int, Dict[str, Any]]:
    if not research_manager_gate_enabled(config, "stage_3"):
        for transcript in transcripts_by_index.values():
            transcript["passes_stage4"] = True
        return transcripts_by_index

    settings = resolve_research_manager_settings(
        config,
        "stage_3",
        default_max_tokens=20000,
    )
    first_simulation = next(
        (
            simulation
            for simulation in simulation_group.get("simulations", [])
            if isinstance(simulation, dict)
        ),
        {},
    )
    causal_variable = (
        simulation_group.get("causal_variable")
        or simulation_group.get("causal_var")
        or first_simulation.get("causal_variable")
        or first_simulation.get("causal_var")
    )
    group_id = simulation_group.get("group_id") or RunId.from_mapping(first_simulation).group_id
    settings = settings_with_cache_key(
        settings,
        "rm",
        "s3",
        behavior_name,
        causal_variable,
        compact_sequence_id(group_id),
        f"r{repetition}",
    )
    records = []
    for simulation in simulation_group.get("simulations", []):
        run = RunId.from_mapping({**simulation, "repetition": repetition})
        simulation_id = PayloadManager.simulation_id(simulation)
        records.append(
            {
                "context": TranscriptManager.run_context(run),
                "transcript": transcripts_by_index[run.value_index],
                "simulation": simulation,
                "simulation_id": simulation_id,
                "group_id": str(simulation_group.get("group_id") or run.group_id),
            }
        )

    label = f"{simulation_group.get('group_id', 'simulation_group')}:r{repetition}"
    review_results = await gather_after_first(
        records,
        lambda record: judge_stage_three_record(
                record=record,
                records=records,
                settings=settings,
                llm_semaphore=llm_semaphore,
        ),
        return_exceptions=True,
    )
    for record, result in zip(records, review_results):
        value_index = int(record["context"]["value_index"])
        if isinstance(result, Exception):
            transcripts_by_index[value_index]["passes_stage4"] = False
            if verbose:
                logger.warning(
                    "[%s] Research-manager review failed for %s: %s",
                    label,
                    record["context"]["simulation_id"],
                    result,
                )
            continue
        transcripts_by_index[value_index].update(result)
        transcripts_by_index[value_index]["passes_stage4"] = _passes_fidelity_gate(
            transcripts_by_index[value_index]
        )
        transcripts_by_index[value_index]["token_counts"] = TranscriptManager.build_token_counts(
            prompts=transcripts_by_index[value_index].get("prompts"),
            research_manager_prompt=transcripts_by_index[value_index].get(
                "research_manager_prompt"
            ),
        )
        if verbose:
            review = result.get("research_manager_review")
            overall_validity = (
                ((review or {}).get("overall_validity") or {}).get("rating")
                if isinstance(review, dict)
                else None
            )
            logger.info(
                "[%s] research manager %s: overall_validity=%s",
                label,
                record["context"]["simulation_id"],
                overall_validity or "missing",
            )

    return transcripts_by_index


def _simulation_summaries_and_evals_by_causal_value(
    config_design: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    causal_variable = (
        NormalizationManager.text_value(config_design.get("variable"))
        or NormalizationManager.text_value(
            NormalizationManager.object_value(config_design.get("hypothesis")).get("variable")
        )
        or "Hypothesized causal variable"
    )
    simulation_by_run = simulations_by_run(config_design)
    grouped: Dict[tuple[Any, Any], Dict[str, Any]] = {}
    for entry in review.get("simulations", []):
        if not isinstance(entry, Mapping):
            continue
        behavior_eval = entry.get("behavior_eval")
        if not isinstance(behavior_eval, Mapping):
            continue
        run = RunId.from_mapping(entry)
        simulation = simulation_by_run.get(run.key, {})
        causal_value = simulation.get("causal_value")
        key = (run.level_position, causal_value)
        group = grouped.setdefault(
            key,
            {
                "causal_value": causal_value,
                "causal_rank": run.level_position,
                "simulations": [],
            },
        )
        behavior_assessment = behavior_eval.get("behavior_assessment")
        assessment = behavior_assessment if isinstance(behavior_assessment, Mapping) else {}
        group["simulations"].append(
            {
                **run.as_dict(),
                "configuration_summary": {
                    "domain": simulation.get("domain"),
                    "variable_values": PayloadManager.simulation_variable_values(simulation),
                },
                "simulation_summary": behavior_eval.get("simulation_summary"),
                "behavior_patterns": behavior_eval.get("behavior_patterns"),
                "inferred_mechanisms": behavior_eval.get("inferred_mechanisms"),
                "behavior_evaluations": assessment,
            }
        )
    blocks = []
    for _, group in sorted(
        grouped.items(),
        key=lambda item: (
            item[0][0] if item[0][0] is not None else 10**9,
            str(item[0][1]),
        ),
    ):
        blocks.append(
            "\n".join(
                [
                    f"## {causal_variable} = {group.get('causal_value')}",
                    prompt_json(group, sort_keys=False),
                ]
            )
        )
    return "\n\n".join(blocks)


async def write_research_report(
    *,
    config: Dict[str, Any],
    results_dir: str | Path,
    hypothesis: Mapping[str, Any],
    config_design: Mapping[str, Any],
    review: Mapping[str, Any],
    quantitative_analysis: Mapping[str, Any] | None = None,
    analytic_results: Mapping[str, Any] | None = None,
    load_existing: bool = True,
) -> Dict[str, Any]:
    transcript_manager = TranscriptManager(results_dir)
    report_path = transcript_manager.final_report_path()
    if load_existing:
        cached = transcript_manager.load_final_report_output()
        if cached is not None:
            return cached

    if not research_manager_gate_enabled(config, "stage_4"):
        logger.info(
            "Final report disabled for %s.",
            config_design.get("axis_slug") or report_path.parent.name,
        )
        return {}

    settings = resolve_research_manager_settings(config, "stage_4", default_max_tokens=12000)
    variable_hypothesis = (
        config_design.get("hypothesis")
        if isinstance(config_design.get("hypothesis"), Mapping)
        else {}
    )
    if not variable_hypothesis:
        variable_name = NormalizationManager.text_value(config_design.get("variable"))
        variable_hypothesis = next(
            (
                item
                for item in hypothesis.get("hypotheses", [])
                if isinstance(item, Mapping)
                and NormalizationManager.text_value(item.get("variable")) == variable_name
            ),
            {},
        )

    analytic_results = (
        dict(analytic_results)
        if isinstance(analytic_results, Mapping)
        else {"quantitative_analysis": dict(quantitative_analysis or {})}
    )
    quantitative_analysis = (
        analytic_results.get("quantitative_analysis")
        if isinstance(analytic_results.get("quantitative_analysis"), Mapping)
        else dict(quantitative_analysis or {})
    )

    system_prompt = ResearchManagerPrompts.make_system_prompt()
    user_prompt = ResearchManagerPrompts.generate_final_report(
        behavior_name=NormalizationManager.text_value(hypothesis.get("behavior_name")),
        definition=NormalizationManager.text_value(hypothesis.get("definition")),
        behavior_eval_rubric=hypothesis.get("behavior_eval_rubric", []),
        hypothesis=dict(variable_hypothesis),
        simulation_summaries_and_evals=_simulation_summaries_and_evals_by_causal_value(
            config_design,
            review,
        ),
        quantitative_analysis=dict(quantitative_analysis or {}),
    )

    logger.info(
        "Calling research manager for final report: %s",
        config_design.get("variable") or config_design.get("axis_slug") or report_path.parent.name,
    )
    with collect_fallbacks() as fallbacks:
        llm_response = await limited_llm_call_with_metadata(
            PayloadManager.messages(system_prompt, user_prompt),
            **llm_call_kwargs(settings),
        )
        response = llm_response.text
        report = parse_final_report_response(response)

    prompts = [
        {"stage": "final_report", "system": system_prompt},
        TranscriptManager.build_prompt_record(
            1,
            user_prompt,
            response,
            stage="final_report",
            source="stage_four_final_report",
            variable=config_design.get("variable"),
            token_counts=llm_response.token_counts,
            response_id=llm_response.response_id,
        ),
    ]
    data = {
        "behavior_name": hypothesis.get("behavior_name"),
        "axis_slug": config_design.get("axis_slug") or report_path.parent.name,
        "variable": config_design.get("variable"),
        "meta_data": {
            "model": settings.model,
            "temperature": settings.temperature,
            "reasoning_effort": settings.reasoning_effort,
            "research_manager_stage_4": True,
        },
        "report": TranscriptManager.final_report_payload(report),
        "token_counts": TranscriptManager.build_token_counts(
            research_manager_prompt=prompts,
        ),
        "research_manager_prompt": prompts,
        "fallbacks": list(fallbacks),
    }
    transcript_manager.save_final_report_output(data)
    return data


async def write_research_reports(
    *,
    config: Dict[str, Any],
    hypothesis: Mapping[str, Any],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    matched_simulation_runs_by_id: Mapping[str, Mapping[str, Any]],
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    quantitative_analyses_by_id: Mapping[str, Mapping[str, Any]] | None = None,
    statistical_analyses_by_id: Mapping[str, Mapping[str, Any]] | None = None,
    load_existing: bool = True,
) -> Dict[str, Dict[str, Any]]:
    if not research_manager_gate_enabled(config, "stage_4"):
        logger.info("Final report research manager disabled.")
        return {}

    quantitative_analyses_by_id = quantitative_analyses_by_id or {}
    statistical_analyses_by_id = statistical_analyses_by_id or {}

    async def run_one(hypothesis_id: str) -> tuple[str, Dict[str, Any]]:
        simulation_result = matched_simulation_runs_by_id[hypothesis_id]
        report = await write_research_report(
            config=config,
            results_dir=simulation_result["experiment_dir"],
            hypothesis=hypothesis,
            config_design=matched_configurations_by_id[hypothesis_id],
            review=blind_reviews_by_id.get(hypothesis_id) or {},
            quantitative_analysis=quantitative_analyses_by_id.get(hypothesis_id) or {},
            analytic_results=statistical_analyses_by_id.get(hypothesis_id),
            load_existing=load_existing,
        )
        return hypothesis_id, report

    pairs = await asyncio.gather(*(run_one(slug) for slug in selected_hypothesis_ids))
    reports = {slug: report for slug, report in pairs if report}
    for slug, report in reports.items():
        report_path = TranscriptManager(
            matched_simulation_runs_by_id[slug]["experiment_dir"]
        ).final_report_path()
        logger.info("[%s] final report: %s", slug, report_path)
    return reports
