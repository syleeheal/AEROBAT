"""Environment-fidelity analysis reported in the AEROBAT paper.

The three tasks are:

1. variable value inference: ``(F_ij, V) -> v``
2. configuration-to-simulation mapping: ``({S_iq}_q, {F_ip}_p) -> pi_hat_i``
3. within-group variable inference: ``{F_ij, S_ij}_j -> X_hat``

The short task ids below are retained because they are part of the stored
artifact layout; public functions use the paper terminology.
"""

from __future__ import annotations

import asyncio
import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


from aerobat.runtime.llm import (
    StageLLMSettings,
    limited_llm_call_with_metadata,
    llm_call_kwargs,
)
from aerobat.config import load_raw_config
from aerobat.protocol.normalization import NormalizationManager
from aerobat.protocol.parsing import StringParser, TaggedResponse
from aerobat.storage.ids import RunId
from aerobat.storage.artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    MATCHED_SIMULATION_RUNS,
)
from aerobat.storage.schema import runtime_artifact
from aerobat.protocol.payloads import PayloadManager
from aerobat.protocol.prompts import EnvironmentFidelityPrompts
from aerobat.protocol.prompt_utils import prompt_json
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import load_json, save_json

ROOT = Path(__file__).resolve().parents[3]

ENVIRONMENT_FIDELITY_TASK_IDS = (
    "config_recovery",
    "simulation_fidelity",
    "variable_inference",
)
ENVIRONMENT_FIDELITY_TASK_LABELS = {
    "config_recovery": "variable value inference",
    "simulation_fidelity": "configuration-to-simulation mapping",
    "variable_inference": "within-group variable inference",
}
ENVIRONMENT_FIDELITY_TASK_NAMES = (
    "variable_value_inference",
    "configuration_to_simulation_mapping",
    "within_group_variable_inference",
)
FIDELITY_TASK_ALIASES = {
    "variable_value_inference": "config_recovery",
    "configuration_recovery": "config_recovery",
    "configuration_value_recovery": "config_recovery",
    "config_value_recovery": "config_recovery",
    "configuration_to_simulation_mapping": "simulation_fidelity",
    "configuration_simulation_mapping": "simulation_fidelity",
    "fidelity": "simulation_fidelity",
    "within_group_variable_inference": "variable_inference",
    "group_variable_inference": "variable_inference",
    "variable_match": "variable_inference",
}


@dataclass(frozen=True)
class SampledMatchedGroup:
    behavior_name: str
    behavior_dir: Path
    hypothesis_id: str
    hypothesis_dir: Path
    config_design: Mapping[str, Any]
    domain_slug: str
    group_index: int
    simulations: Sequence[Mapping[str, Any]]
    transcripts_by_simulation_key: Mapping[tuple, Mapping[str, Any]]


def _text(value: Any) -> str:
    return NormalizationManager.text_value(value)


def _norm(value: Any) -> str:
    return NormalizationManager.normalize_key(value)


def normalize_fidelity_tasks(fidelity_tasks: Sequence[str] | None = None) -> tuple[str, ...]:
    if not fidelity_tasks:
        return ENVIRONMENT_FIDELITY_TASK_IDS
    normalized = []
    unknown = []
    for task in fidelity_tasks:
        key = _norm(task).replace(" ", "_").replace("-", "_")
        key = FIDELITY_TASK_ALIASES.get(key, key)
        if key not in ENVIRONMENT_FIDELITY_TASK_IDS:
            unknown.append(str(task))
            continue
        if key not in normalized:
            normalized.append(key)
    if unknown:
        raise ValueError(
            f"Unknown environment-fidelity task id(s): {unknown}. "
            f"Valid names are: {list(ENVIRONMENT_FIDELITY_TASK_NAMES)}"
        )
    return tuple(normalized)


def _settings(section: Mapping[str, Any], fallback: Mapping[str, Any]) -> StageLLMSettings:
    return StageLLMSettings(
        model=str(section.get("model") or fallback.get("model") or "openai/gpt-5.1"),
        temperature=float(section.get("temperature", fallback.get("temperature", 1.0))),
        max_tokens=int(section.get("max_tokens", fallback.get("max_tokens", 8000))),
        reasoning_effort=str(section.get("reasoning_effort", fallback.get("reasoning_effort", "NA"))),
        reasoning_summary=str(section.get("reasoning_summary", fallback.get("reasoning_summary", "NA"))),
        service_tier=str(section.get("service_tier", fallback.get("service_tier", "NA"))),
        prompt_cache_key=str(section.get("prompt_cache_key", fallback.get("prompt_cache_key", "NA"))),
        prompt_cache_retention=str(
            section.get("prompt_cache_retention", fallback.get("prompt_cache_retention", "NA"))
        ),
    )


def environment_fidelity_settings(config: Mapping[str, Any]) -> Dict[str, Any]:
    """Load settings; ``validity_analysis`` remains the legacy YAML section key."""
    cfg = config.get("validity_analysis", {})
    cfg = cfg if isinstance(cfg, Mapping) else {}
    fallback = {
        "model": cfg.get("model", "openai/gpt-5.1"),
        "temperature": cfg.get("temperature", 1.0),
        "max_tokens": cfg.get("max_tokens", 8000),
        "reasoning_effort": cfg.get("reasoning_effort", "NA"),
        "service_tier": cfg.get("service_tier", config.get("service_tier", "NA")),
    }
    return {
        "output_dir": Path(str(cfg.get("output_dir", "results/fidelity-results"))),
        "sample_seed": int(cfg.get("sample_seed", 42)),
        "groups_per_behavior": int(cfg.get("groups_per_behavior", 1)),
        "require_stage3_pass": bool(cfg.get("require_stage3_pass", True)),
        "max_concurrent": int(cfg.get("max_concurrent", config.get("max_concurrent", 5))),
        "config_recovery": _settings(
            cfg.get("config_recovery", {}) if isinstance(cfg.get("config_recovery"), Mapping) else {},
            fallback,
        ),
        "simulation_fidelity": _settings(
            cfg.get("simulation_fidelity", {}) if isinstance(cfg.get("simulation_fidelity"), Mapping) else {},
            fallback,
        ),
        "variable_inference": _settings(
            cfg.get("variable_inference", {}) if isinstance(cfg.get("variable_inference"), Mapping) else {},
            fallback,
        ),
    }


def _simulation_transcript_key(record: Mapping[str, Any]) -> tuple:
    return RunId.from_mapping(record).key


def _load_transcripts(hypothesis_dir: Path) -> Dict[tuple, Mapping[str, Any]]:
    """Matched simulation runs for one hypothesis, keyed by ``(domain, i, j)``."""
    meta_path = hypothesis_dir / MATCHED_SIMULATION_RUNS
    if not meta_path.exists():
        return {}
    meta = runtime_artifact(meta_path.name, load_json(meta_path))
    manager = TranscriptManager(hypothesis_dir)
    transcripts = {}
    for entry in meta.get("runs", []) if isinstance(meta, Mapping) else []:
        if not isinstance(entry, Mapping):
            continue
        try:
            run = RunId.from_mapping(entry)
        except (KeyError, ValueError):
            continue
        path = manager.simulation_path(run)
        if path.exists():
            transcripts[run.key] = runtime_artifact(path.name, load_json(path))
    return transcripts


def _stage3_passed(transcript: Mapping[str, Any]) -> bool:
    return transcript.get("passes_stage4") is True


def _eligible_groups(hypothesis_dir: Path, config_design: Mapping[str, Any], require_stage3_pass: bool) -> List[Dict[str, Any]]:
    transcripts = _load_transcripts(hypothesis_dir)
    grouped: Dict[tuple[str, int, str], List[Mapping[str, Any]]] = {}
    for simulation in PayloadManager.simulation_entries_from_config_design(config_design):
        transcript = transcripts.get(_simulation_transcript_key(simulation))
        if not transcript:
            continue
        if require_stage3_pass and not _stage3_passed(transcript):
            continue
        run = RunId.from_mapping(simulation)
        grouped.setdefault((run.domain_slug, run.group_index), []).append(simulation)

    groups = []
    for (domain_slug, group_index), simulations in grouped.items():
        if len(simulations) < 2:
            continue
        simulations = sorted(simulations, key=lambda row: int(row.get("value_index") or 0))
        groups.append(
            {
                "domain_slug": domain_slug,
                "group_index": group_index,
                "simulations": simulations,
                "transcripts_by_simulation_key": transcripts,
            }
        )
    return groups


def _load_hypotheses_by_variable(behavior_dir: Path) -> Dict[str, Mapping[str, Any]]:
    hypothesis_path = behavior_dir / HYPOTHESIS_GENERATION
    if not hypothesis_path.exists():
        return {}
    hypothesis_payload = runtime_artifact(
        hypothesis_path.name, load_json(hypothesis_path)
    )
    return {
        _norm(row.get("variable")): row
        for row in hypothesis_payload.get("hypotheses", [])
        if isinstance(row, Mapping) and _text(row.get("variable"))
    }


def _load_config_design(hypothesis_dir: Path, hypotheses_by_variable: Mapping[str, Mapping[str, Any]]) -> Dict[str, Any] | None:
    config_path = hypothesis_dir / MATCHED_CONFIGURATIONS
    if not config_path.exists():
        return None
    config_design = runtime_artifact(config_path.name, load_json(config_path))
    if not isinstance(config_design.get("hypothesis"), Mapping):
        variable = _text(config_design.get("variable"))
        config_design["hypothesis"] = hypotheses_by_variable.get(
            _norm(variable),
            hypotheses_by_variable.get(_norm(hypothesis_dir.name), {}),
        )
    if not config_design.get("hypothesis"):
        return None
    return config_design


def _discover_pinned_sampled_groups(
    *,
    results_base: str | Path,
    sample_specs: Sequence[Sequence[Any]],
    require_stage3_pass: bool = True,
    target_behaviors: Sequence[str] | None = None,
) -> List[SampledMatchedGroup]:
    base = Path(results_base)
    target_behavior_keys = {
        _norm(behavior)
        for behavior in (target_behaviors or [])
        if _text(behavior)
    }
    sampled: List[SampledMatchedGroup] = []
    missing = []
    hypotheses_cache: Dict[str, Mapping[str, Mapping[str, Any]]] = {}
    config_cache: Dict[tuple[str, str], Dict[str, Any]] = {}
    eligible_cache: Dict[tuple[str, str], List[Dict[str, Any]]] = {}

    for behavior_name, hypothesis_id, domain_slug, group_index in sample_specs:
        if target_behavior_keys and _norm(behavior_name) not in target_behavior_keys:
            continue
        behavior_dir = base / behavior_name
        hypothesis_dir = behavior_dir / hypothesis_id
        behavior_key = behavior_name
        hypothesis_key = (behavior_name, hypothesis_id)
        if behavior_key not in hypotheses_cache:
            hypotheses_cache[behavior_key] = _load_hypotheses_by_variable(behavior_dir)
        if hypothesis_key not in config_cache:
            config_design = _load_config_design(hypothesis_dir, hypotheses_cache[behavior_key])
            if config_design is not None:
                config_cache[hypothesis_key] = config_design
        config_design = config_cache.get(hypothesis_key)
        if config_design is None:
            missing.append((behavior_name, hypothesis_id, domain_slug, group_index))
            continue
        if hypothesis_key not in eligible_cache:
            eligible_cache[hypothesis_key] = _eligible_groups(hypothesis_dir, config_design, require_stage3_pass)
        group = next(
            (
                row
                for row in eligible_cache[hypothesis_key]
                if _norm(row["domain_slug"]) == _norm(domain_slug)
                and int(row["group_index"]) == int(group_index)
            ),
            None,
        )
        if group is None:
            missing.append((behavior_name, hypothesis_id, domain_slug, group_index))
            continue
        sampled.append(
            SampledMatchedGroup(
                behavior_name=behavior_name,
                behavior_dir=behavior_dir,
                hypothesis_id=hypothesis_id,
                hypothesis_dir=hypothesis_dir,
                config_design=config_design,
                domain_slug=group["domain_slug"],
                group_index=group["group_index"],
                simulations=group["simulations"],
                transcripts_by_simulation_key=group["transcripts_by_simulation_key"],
            )
        )

    if missing:
        formatted = ", ".join(
            f"{behavior}/{axis}/{domain}/i{index}"
            for behavior, axis, domain, index in missing
        )
        raise FileNotFoundError(f"Missing pinned environment-fidelity samples: {formatted}")
    return sampled


def discover_sampled_groups(
    *,
    results_base: str | Path,
    sample_seed: int = 42,
    groups_per_behavior: int = 1,
    require_stage3_pass: bool = True,
    target_behaviors: Sequence[str] | None = None,
    sample_specs: Sequence[Sequence[Any]] | None = None,
) -> List[SampledMatchedGroup]:
    if sample_specs:
        return _discover_pinned_sampled_groups(
            results_base=results_base,
            sample_specs=sample_specs,
            require_stage3_pass=require_stage3_pass,
            target_behaviors=target_behaviors,
        )
    rng = random.Random(sample_seed)
    base = Path(results_base)
    target_behavior_keys = {
        _norm(behavior)
        for behavior in (target_behaviors or [])
        if _text(behavior)
    }
    sampled: List[SampledMatchedGroup] = []
    for behavior_dir in sorted(path for path in base.iterdir() if path.is_dir()):
        if target_behavior_keys and _norm(behavior_dir.name) not in target_behavior_keys:
            continue
        hypothesis_path = behavior_dir / HYPOTHESIS_GENERATION
        if not hypothesis_path.exists():
            continue
        hypothesis_payload = runtime_artifact(
            hypothesis_path.name, load_json(hypothesis_path)
        )
        hypotheses_by_variable = {
            _norm(row.get("variable")): row
            for row in hypothesis_payload.get("hypotheses", [])
            if isinstance(row, Mapping) and _text(row.get("variable"))
        }
        candidates = []
        for config_path in sorted(behavior_dir.glob(f"*/{MATCHED_CONFIGURATIONS}")):
            hypothesis_dir = config_path.parent
            if not (hypothesis_dir / MATCHED_SIMULATION_RUNS).exists():
                continue
            config_design = runtime_artifact(config_path.name, load_json(config_path))
            if not isinstance(config_design.get("hypothesis"), Mapping):
                variable = _text(config_design.get("variable"))
                config_design["hypothesis"] = hypotheses_by_variable.get(
                    _norm(variable),
                    hypotheses_by_variable.get(_norm(hypothesis_dir.name), {}),
                )
            if not config_design.get("hypothesis"):
                continue
            groups = _eligible_groups(hypothesis_dir, config_design, require_stage3_pass)
            for group in groups:
                candidates.append((hypothesis_dir.name, hypothesis_dir, config_design, group))
        if not candidates:
            continue
        rng.shuffle(candidates)
        for hypothesis_id, hypothesis_dir, config_design, group in candidates[:groups_per_behavior]:
            sampled.append(
                SampledMatchedGroup(
                    behavior_name=behavior_dir.name,
                    behavior_dir=behavior_dir,
                    hypothesis_id=hypothesis_id,
                    hypothesis_dir=hypothesis_dir,
                    config_design=config_design,
                    domain_slug=group["domain_slug"],
                    group_index=group["group_index"],
                    simulations=group["simulations"],
                    transcripts_by_simulation_key=group["transcripts_by_simulation_key"],
                )
            )
    return sampled


def _parse_variable_value_inference(response: str, variable_names: Sequence[str]) -> Dict[str, Any]:
    parsed = TaggedResponse(response)
    raw_predictions = parsed.object("value_predictions")
    predictions = {}
    for name in variable_names:
        entry = NormalizationManager.find_normalized_key_value(raw_predictions, name)
        if isinstance(entry, Mapping):
            predicted = entry.get("predicted_value")
            rationale = entry.get("rationale")
        else:
            predicted = entry
            rationale = None
        predictions[name] = {
            "predicted_value": _text(predicted) or None,
            "rationale": _text(rationale) or None,
        }
    return {
        "configuration_summary": parsed.tag("configuration_summary") or parsed.tag("simulation_summary"),
        "value_predictions": predictions,
    }


def _true_values(simulation: Mapping[str, Any]) -> Dict[str, Any]:
    return PayloadManager.simulation_variable_values(simulation)


def _candidate_scores(simulation: Mapping[str, Any]) -> Dict[str, Dict[str, float]]:
    specs = {}
    for row in simulation.get("environment_variables", []):
        if not isinstance(row, Mapping):
            continue
        name = _text(row.get("name"))
        scores = {}
        for value, score in (row.get("value_score") or {}).items():
            if isinstance(score, (int, float)) and not isinstance(score, bool):
                scores[_norm(value)] = float(score)
        if name:
            specs[name] = scores
    return specs


def _record_sample(record: Mapping[str, Any]) -> Mapping[str, Any]:
    sample = record.get("sample")
    sample = dict(sample) if isinstance(sample, Mapping) else dict(record)
    if "group_index" not in sample and "matched_group_index" in sample:
        sample["group_index"] = sample.get("matched_group_index")
    return sample


def _value_recovery_rows(record: Mapping[str, Any]) -> List[Dict[str, Any]]:
    simulation = record.get("simulation") or {}
    sample = _record_sample(record)
    target = record.get("target") if isinstance(record.get("target"), Mapping) else {}
    true_values = (
        dict(target.get("true_values"))
        if isinstance(target.get("true_values"), Mapping)
        else _true_values(simulation)
    )
    predictions = (record.get("result") or {}).get("value_predictions") or {}
    scores_by_var = (
        {
            str(name): {
                _norm(value): float(score)
                for value, score in (spec.get("value_score") or {}).items()
                if isinstance(spec, Mapping)
                and isinstance(score, (int, float))
                and not isinstance(score, bool)
            }
            for name, spec in NormalizationManager.object_value(target.get("variable_specs")).items()
        }
        if isinstance(target.get("variable_specs"), Mapping)
        else _candidate_scores(simulation)
    )
    rows = []
    for variable, true_value in true_values.items():
        predicted = (predictions.get(variable) or {}).get("predicted_value")
        exact = _norm(predicted) == _norm(true_value) if predicted and true_value else None
        true_score = scores_by_var.get(variable, {}).get(_norm(true_value))
        predicted_score = scores_by_var.get(variable, {}).get(_norm(predicted))
        rows.append(
            {
                "behavior": sample.get("behavior_name"),
                "axis_slug": sample.get("axis_slug"),
                "domain_slug": sample.get("domain_slug"),
                "group_index": sample.get("group_index"),
                "simulation_id": sample.get("simulation_id", simulation.get("simulation_id")),
                "variable": variable,
                "true_value": true_value,
                "predicted_value": predicted,
                "exact_match": exact,
                "absolute_score_error": (
                    abs(predicted_score - true_score)
                    if predicted_score is not None and true_score is not None
                    else None
                ),
            }
        )
    return rows


def _parse_configuration_simulation_mapping(response: str) -> Dict[str, Any]:
    parsed = TaggedResponse(response)
    mapping_payload = StringParser.parse_jsonish_object(parsed.tag("configuration_simulation_mapping"))
    raw_matches = mapping_payload.get("matches") if isinstance(mapping_payload, Mapping) else None
    matches = []
    if isinstance(raw_matches, list):
        for entry in raw_matches:
            if not isinstance(entry, Mapping):
                continue
            matches.append(
                {
                    "configuration_id": _text(entry.get("configuration_id")) or None,
                    "simulation_id": _text(entry.get("simulation_id")) or None,
                    "rationale": _text(entry.get("rationale")) or None,
                }
            )
    elif isinstance(mapping_payload, Mapping):
        for configuration_id, simulation_id in mapping_payload.items():
            if _norm(configuration_id) in {"matches", "rationale"}:
                continue
            matches.append(
                {
                    "configuration_id": _text(configuration_id) or None,
                    "simulation_id": _text(simulation_id) or None,
                    "rationale": None,
                }
            )
    return {"matches": matches}


def _label(prefix: str, index: int) -> str:
    return f"{prefix}{index + 1:02d}"


def _permuted_group_payload(group: SampledMatchedGroup, *, sample_seed: int) -> Dict[str, Any]:
    simulations = list(group.simulations)
    simulation_order = list(range(len(simulations)))
    configuration_order = list(range(len(simulations)))
    seed = (
        f"{sample_seed}:{group.behavior_name}:{group.hypothesis_id}:"
        f"{group.domain_slug}:{group.group_index}"
    )
    rng = random.Random(seed)
    rng.shuffle(simulation_order)
    rng.shuffle(configuration_order)

    simulation_records = []
    configuration_records = []
    truth = {}
    simulation_label_by_position = {}
    for label_index, position in enumerate(simulation_order):
        simulation = simulations[position]
        transcript = group.transcripts_by_simulation_key[_simulation_transcript_key(simulation)]
        simulation_label = _label("S", label_index)
        simulation_label_by_position[position] = simulation_label
        simulation_records.append(
            {
                "simulation_id": simulation_label,
                "simulation_history": PayloadManager.rounds_blind(
                    [row for row in transcript.get("rounds", []) if isinstance(row, dict)],
                    include_reasoning_summary=False,
                ),
            }
        )
    for label_index, position in enumerate(configuration_order):
        simulation = simulations[position]
        configuration_label = _label("F", label_index)
        configuration_records.append(
            {
                "configuration_id": configuration_label,
                "configuration": _config_payload(simulation),
            }
        )
        truth[configuration_label] = {
            "simulation_id": simulation_label_by_position[position],
            "real_simulation_id": simulation.get("simulation_id"),
            "value_index": simulation.get("value_index"),
            "causal_value": simulation.get("causal_value"),
        }
    return {
        "simulation_histories": simulation_records,
        "configurations": configuration_records,
        "truth": truth,
        "permutation": {
            "simulation_order": simulation_order,
            "configuration_order": configuration_order,
        },
    }


def _fidelity_rows(record: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    sample = _record_sample(record)
    target = NormalizationManager.object_value(record.get("target"))
    truth = NormalizationManager.object_value(target.get("true_mapping"))
    matches = (record.get("result") or {}).get("matches") or []
    predicted = {
        _text(row.get("configuration_id")): _text(row.get("simulation_id"))
        for row in matches
        if isinstance(row, Mapping)
    }
    for configuration_id, true_entry in truth.items():
        true_entry = NormalizationManager.object_value(true_entry)
        predicted_simulation_id = predicted.get(_text(configuration_id))
        true_simulation_id = _text(true_entry.get("simulation_id"))
        rows.append(
            {
                "behavior": sample.get("behavior_name"),
                "axis_slug": sample.get("axis_slug"),
                "domain_slug": sample.get("domain_slug"),
                "group_index": sample.get("group_index"),
                "configuration_id": configuration_id,
                "true_simulation_id": true_simulation_id,
                "predicted_simulation_id": predicted_simulation_id,
                "correct": predicted_simulation_id == true_simulation_id,
                "real_simulation_id": true_entry.get("real_simulation_id"),
                "value_index": true_entry.get("value_index"),
                "causal_value": true_entry.get("causal_value"),
            }
        )
    return rows


def _group_variable_records(group: SampledMatchedGroup) -> List[Dict[str, Any]]:
    records = []
    for simulation in group.simulations:
        transcript = group.transcripts_by_simulation_key[_simulation_transcript_key(simulation)]
        records.append(
            {
                "simulation_id": simulation.get("simulation_id"),
                "configuration": {
                    "roles": simulation.get("roles") or {},
                    "rules": simulation.get("rules") or {},
                },
                "simulation_result": PayloadManager.rounds_blind(
                    [row for row in transcript.get("rounds", []) if isinstance(row, dict)]
                ),
            }
        )
    return records


def _parse_within_group_variable_inference(response: str) -> Dict[str, Any]:
    parsed = TaggedResponse(response)
    inferred = StringParser.parse_jsonish_object(parsed.tag("inferred_variable"))
    return {
        "inferred_variable": {
            "variable": _text(inferred.get("variable")) or None,
            "definition": _text(inferred.get("definition")) or None,
            "evidence": _text(inferred.get("evidence")) or None,
        }
    }


def _causal_variable_spec(group: SampledMatchedGroup) -> Dict[str, Any]:
    first = group.simulations[0]
    causal = _text(first.get("causal_variable"))
    for row in first.get("environment_variables", []):
        if isinstance(row, Mapping) and _norm(row.get("name")) == _norm(causal):
            return {"variable": causal, "definition": _text(row.get("definition"))}
    hypothesis = group.config_design.get("hypothesis") if isinstance(group.config_design.get("hypothesis"), Mapping) else {}
    return {"variable": causal, "definition": _text(hypothesis.get("var_definition"))}


def _sample_payload(
    group: SampledMatchedGroup,
    *,
    simulation: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    payload = {
        "behavior_name": group.behavior_name,
        "axis_slug": group.hypothesis_id,
        "domain_slug": group.domain_slug,
        "group_index": group.group_index,
    }
    if simulation is not None:
        payload.update(
            {
                "simulation_id": simulation.get("simulation_id"),
                "value_index": simulation.get("value_index"),
                "causal_variable": simulation.get("causal_variable"),
                "causal_value": simulation.get("causal_value"),
            }
        )
    return payload


def _config_payload(simulation: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "roles": simulation.get("roles") or {},
        "rules": simulation.get("rules") or {},
    }


def _variable_specs_payload(simulation: Mapping[str, Any]) -> Dict[str, Any]:
    specs = {}
    for row in simulation.get("environment_variables", []):
        if not isinstance(row, Mapping):
            continue
        name = _text(row.get("name"))
        if not name:
            continue
        specs[name] = {
            "candidate_values": list(row.get("range") or []),
            "value_score": dict(row.get("value_score") or {}),
        }
    return specs


async def _llm_json_task(
    *,
    system_prompt: str,
    user_prompt: str,
    settings: StageLLMSettings,
    parser: Any,
    semaphore: asyncio.Semaphore,
    source: str,
) -> tuple[Dict[str, Any], Dict[str, Any]]:
    response = await limited_llm_call_with_metadata(
        PayloadManager.messages(system_prompt, user_prompt),
        llm_semaphore=semaphore,
        **llm_call_kwargs(settings),
    )
    parsed = parser(response.text)
    prompt_record = {
        "source": source,
        "input": user_prompt,
        "output": response.text,
        "token_counts": response.token_counts or {},
    }
    if system_prompt:
        prompt_record["system"] = system_prompt
    return parsed, prompt_record


def _save_fidelity_payload(payload: Dict[str, Any], path: Path) -> None:
    stored = {
        **payload,
        "token_counts": TranscriptManager.build_token_counts(prompts=payload.get("prompts", [])),
    }
    payload.clear()
    payload.update(stored)
    save_json(TranscriptManager.storage_payload(payload), path)


def _read_cached(path: Path, load_existing: bool) -> Dict[str, Any] | None:
    if load_existing and path.exists():
        payload = load_json(path)
        return payload if isinstance(payload, dict) else None
    return None


def _token_counts_current(payload: Mapping[str, Any]) -> bool:
    token_counts = payload.get("token_counts")
    return (
        isinstance(token_counts, Mapping)
        and isinstance(token_counts.get("total"), Mapping)
        and isinstance(token_counts.get("calls"), list)
    )


def _basic_cache_current(payload: Mapping[str, Any]) -> bool:
    return _token_counts_current(payload)


def _simulation_fidelity_cache_current(payload: Mapping[str, Any]) -> bool:
    return (
        _token_counts_current(payload)
        and isinstance(NormalizationManager.object_value(payload.get("target")).get("true_mapping"), Mapping)
        and isinstance(NormalizationManager.object_value(payload.get("result")).get("matches"), list)
    )


async def run_variable_value_inference(
    groups: Sequence[SampledMatchedGroup],
    *,
    output_dir: Path,
    settings: StageLLMSettings,
    semaphore: asyncio.Semaphore,
    load_existing: bool = True,
) -> List[Dict[str, Any]]:
    """Task 1: infer environmental-variable values from a configuration ``F_ij``."""
    records = []

    async def run_one(group: SampledMatchedGroup, simulation: Mapping[str, Any]) -> Dict[str, Any]:
        out_path = output_dir / "config_recovery" / group.behavior_name / group.hypothesis_id / f"{simulation['simulation_id']}.json"
        cached = _read_cached(out_path, load_existing)
        if cached is not None and _basic_cache_current(cached):
            return cached
        variable_typology = PayloadManager.variable_typology(simulation)
        variable_names = PayloadManager.variable_names(variable_typology)
        system_prompt = EnvironmentFidelityPrompts.make_variable_value_inference_system_prompt()
        user_prompt = EnvironmentFidelityPrompts.make_variable_value_inference_prompt(
            variable_typology=variable_typology,
            simulation=PayloadManager.simulation_payload(simulation),
        )
        result, prompt_record = await _llm_json_task(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            settings=settings,
            parser=lambda response: _parse_variable_value_inference(response, variable_names),
            semaphore=semaphore,
            source="config_recovery",
        )
        payload = {
            "experiment": "config_recovery",
            "sample": _sample_payload(group, simulation=simulation),
            "target": {
                "config": _config_payload(simulation),
                "true_values": _true_values(simulation),
                "variable_specs": _variable_specs_payload(simulation),
            },
            "result": result,
            "prompts": [prompt_record],
        }
        _save_fidelity_payload(payload, out_path)
        return payload

    tasks = [run_one(group, simulation) for group in groups for simulation in group.simulations]
    for result in await asyncio.gather(*tasks):
        records.append(result)
    return records


async def run_configuration_simulation_mapping(
    groups: Sequence[SampledMatchedGroup],
    *,
    output_dir: Path,
    settings: StageLLMSettings,
    semaphore: asyncio.Semaphore,
    sample_seed: int,
    load_existing: bool = True,
) -> List[Dict[str, Any]]:
    """Task 2: recover the bijection between configurations and simulation runs."""
    async def run_one(group: SampledMatchedGroup) -> Dict[str, Any]:
        out_path = (
            output_dir
            / "simulation_fidelity"
            / group.behavior_name
            / group.hypothesis_id
            / f"{group.domain_slug}_i{group.group_index}.json"
        )
        cached = _read_cached(out_path, load_existing)
        if cached is not None and _simulation_fidelity_cache_current(cached):
            return cached
        payload = _permuted_group_payload(group, sample_seed=sample_seed)
        system_prompt = EnvironmentFidelityPrompts.make_configuration_simulation_mapping_system_prompt()
        user_prompt = EnvironmentFidelityPrompts.make_configuration_simulation_mapping_prompt(
            simulation_histories=payload["simulation_histories"],
            configurations=payload["configurations"],
        )
        result, prompt_record = await _llm_json_task(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            settings=settings,
            parser=_parse_configuration_simulation_mapping,
            semaphore=semaphore,
            source="simulation_fidelity",
        )
        record = {
            "experiment": "simulation_fidelity",
            "sample": {
                **_sample_payload(group),
                "simulation_ids": [
                    simulation.get("simulation_id")
                    for simulation in group.simulations
                ],
            },
            "target": {
                "true_mapping": payload["truth"],
                "permutation": payload["permutation"],
            },
            "result": result,
            "prompts": [prompt_record],
        }
        _save_fidelity_payload(record, out_path)
        return record

    return list(await asyncio.gather(*(run_one(group) for group in groups)))


async def run_within_group_variable_inference(
    groups: Sequence[SampledMatchedGroup],
    *,
    output_dir: Path,
    settings: StageLLMSettings,
    semaphore: asyncio.Semaphore,
    load_existing: bool = True,
) -> List[Dict[str, Any]]:
    """Task 3: infer the varying causal variable within one matched group."""
    async def run_one(group: SampledMatchedGroup) -> Dict[str, Any]:
        out_path = (
            output_dir
            / "variable_inference"
            / group.behavior_name
            / group.hypothesis_id
            / f"{group.domain_slug}_i{group.group_index}.json"
        )
        cached = _read_cached(out_path, load_existing)
        if cached is not None and _basic_cache_current(cached):
            return cached
        system_prompt = EnvironmentFidelityPrompts.make_within_group_variable_inference_system_prompt()
        user_prompt = EnvironmentFidelityPrompts.make_within_group_variable_inference_prompt(
            _group_variable_records(group)
        )
        result, prompt_record = await _llm_json_task(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            settings=settings,
            parser=_parse_within_group_variable_inference,
            semaphore=semaphore,
            source="variable_inference",
        )
        payload = {
            "experiment": "variable_inference",
            "sample": {
                **_sample_payload(group),
                "simulation_ids": [
                    simulation.get("simulation_id")
                    for simulation in group.simulations
                ],
            },
            "target": {
                "causal_variable": _causal_variable_spec(group),
            },
            "result": result,
            "prompts": [prompt_record],
        }
        _save_fidelity_payload(payload, out_path)
        return payload

    return list(await asyncio.gather(*(run_one(group) for group in groups)))


def _write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    if not fieldnames:
        fieldnames = sorted({key for row in rows for key in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fieldnames),
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def human_eval_template_items(variable_records: Sequence[Mapping[str, Any]], *, sample_seed: int) -> List[Dict[str, Any]]:
    rng = random.Random(sample_seed)
    items = []
    for record in variable_records:
        target_payload = record.get("target") if isinstance(record.get("target"), Mapping) else {}
        target = target_payload.get("causal_variable") or record.get("causal_variable") or {}
        inferred = ((record.get("result") or {}).get("inferred_variable") or {})
        candidates = [
            {
                "name": target.get("variable"),
                "definition": target.get("definition"),
            },
            {
                "name": inferred.get("variable"),
                "definition": inferred.get("definition"),
            },
        ]
        rng.shuffle(candidates)
        items.append(
            {
                "id": f"sample-{len(items) + 1:03d}",
                "var-A": candidates[0],
                "var-B": candidates[1],
                "human_evaluated_match": "",
            }
        )
    return items


def _human_eval_score(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"n_rated": 0, "score": None}
    rating_values = {"high": 1.0, "medium": 0.5, "low": 0.0}
    rows = load_json(path)
    scores = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, Mapping):
            continue
        rating = _norm(row.get("human_evaluated_match"))
        if rating in rating_values:
            scores.append(rating_values[rating])
    return {
        "n_rated": len(scores),
        "score": round(sum(scores) / len(scores), 3) if scores else None,
    }


def summarize_outputs(
    *,
    output_dir: Path,
    config_records: Sequence[Mapping[str, Any]],
    fidelity_records: Sequence[Mapping[str, Any]],
    variable_records: Sequence[Mapping[str, Any]],
    sample_seed: int,
    fidelity_tasks: Sequence[str] | None = None,
) -> Dict[str, Any]:
    selected = set(normalize_fidelity_tasks(fidelity_tasks))
    config_rows = [row for record in config_records for row in _value_recovery_rows(record)]
    fidelity_rows = [row for record in fidelity_records for row in _fidelity_rows(record)]
    human_eval_template = human_eval_template_items(variable_records, sample_seed=sample_seed)
    human_eval_result = _human_eval_score(output_dir / "variable_inference" / "human_eval_result.json")

    exact_values = [row["exact_match"] for row in config_rows if row["exact_match"] is not None]
    fidelity_correct = [row["correct"] for row in fidelity_rows if row.get("correct") is not None]
    group_correct = []
    for record in fidelity_records:
        rows = _fidelity_rows(record)
        if rows:
            group_correct.append(all(row["correct"] for row in rows))
    summary = {
        "analyses_run": list(normalize_fidelity_tasks(fidelity_tasks)),
        "config_recovery": {
            "skipped": "config_recovery" not in selected,
            "n": len(exact_values),
            "exact_match_rate": round(sum(bool(v) for v in exact_values) / len(exact_values), 3) if exact_values else None,
        },
        "simulation_fidelity": {
            "skipped": "simulation_fidelity" not in selected,
            "n_items": len(fidelity_correct),
            "item_recovery_accuracy": (
                round(sum(bool(value) for value in fidelity_correct) / len(fidelity_correct), 3)
                if fidelity_correct
                else None
            ),
            "n_groups": len(group_correct),
            "group_recovery_accuracy": (
                round(sum(bool(value) for value in group_correct) / len(group_correct), 3)
                if group_correct
                else None
            ),
        },
        "variable_inference": {
            "skipped": "variable_inference" not in selected,
            "groups": len(variable_records),
            "human_eval_items": len(human_eval_template),
            "human_eval_rated": human_eval_result["n_rated"],
            "human_eval_score": human_eval_result["score"],
        },
    }
    if "config_recovery" in selected:
        _write_csv(output_dir / "config_recovery_rows.csv", config_rows)
    if "simulation_fidelity" in selected:
        _write_csv(output_dir / "simulation_fidelity_rows.csv", fidelity_rows)
    if "variable_inference" in selected:
        save_json(human_eval_template, output_dir / "variable_inference" / "human_eval_template.json")
    save_json(summary, output_dir / "summary.json")
    return summary


async def run_environment_fidelity_analysis(
    *,
    config_path: str | Path = ROOT / "seed.yaml",
    results_base: str | Path | None = None,
    output_dir: str | Path | None = None,
    load_existing: bool = True,
    target_behaviors: Sequence[str] | None = None,
    fidelity_tasks: Sequence[str] | None = None,
    groups_per_behavior: int | None = None,
    sample_specs: Sequence[Sequence[Any]] | None = None,
) -> Dict[str, Any]:
    """Run the three environment-fidelity tasks on sampled matched groups."""
    config = load_raw_config(config_path)
    settings = environment_fidelity_settings(config)
    selected_tasks = normalize_fidelity_tasks(fidelity_tasks)
    results_base = Path(results_base or config.get("results_dir", "results/GPT-5-mini"))
    output_dir = Path(output_dir or settings["output_dir"])
    groups = discover_sampled_groups(
        results_base=results_base,
        sample_seed=settings["sample_seed"],
        groups_per_behavior=(
            settings["groups_per_behavior"]
            if groups_per_behavior is None
            else groups_per_behavior
        ),
        require_stage3_pass=settings["require_stage3_pass"],
        target_behaviors=target_behaviors,
        sample_specs=sample_specs,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_manifest = [
        {
            "behavior": group.behavior_name,
            "axis_slug": group.hypothesis_id,
            "domain_slug": group.domain_slug,
            "group_index": group.group_index,
            "simulation_count": len(group.simulations),
        }
        for group in groups
    ]
    save_json(sample_manifest, output_dir / "sample_manifest.json")

    semaphore = asyncio.Semaphore(max(1, int(settings["max_concurrent"])))
    config_records = (
        await run_variable_value_inference(
            groups,
            output_dir=output_dir,
            settings=settings["config_recovery"],
            semaphore=semaphore,
            load_existing=load_existing,
        )
        if "config_recovery" in selected_tasks
        else []
    )
    fidelity_records = (
        await run_configuration_simulation_mapping(
            groups,
            output_dir=output_dir,
            settings=settings["simulation_fidelity"],
            semaphore=semaphore,
            sample_seed=settings["sample_seed"],
            load_existing=load_existing,
        )
        if "simulation_fidelity" in selected_tasks
        else []
    )
    variable_records = (
        await run_within_group_variable_inference(
            groups,
            output_dir=output_dir,
            settings=settings["variable_inference"],
            semaphore=semaphore,
            load_existing=load_existing,
        )
        if "variable_inference" in selected_tasks
        else []
    )
    summary = summarize_outputs(
        output_dir=output_dir,
        config_records=config_records,
        fidelity_records=fidelity_records,
        variable_records=variable_records,
        sample_seed=settings["sample_seed"],
        fidelity_tasks=selected_tasks,
    )
    return {
        "output_dir": str(output_dir),
        "analyses_run": list(selected_tasks),
        "sample_manifest": sample_manifest,
        "summary": summary,
        "config_records": config_records,
        "fidelity_records": fidelity_records,
        "variable_records": variable_records,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run AEROBAT environment-fidelity tasks.")
    parser.add_argument("--config", default=str(ROOT / "seed.yaml"))
    parser.add_argument("--results-base", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument(
        "--target-behavior",
        action="append",
        dest="target_behaviors",
        help="Behavior name to include. Repeat for multiple behaviors.",
    )
    parser.add_argument(
        "--task",
        action="append",
        dest="fidelity_tasks",
        help=(
            "Environment-fidelity task to run. Repeat for multiple tasks. "
            f"Task names: {', '.join(ENVIRONMENT_FIDELITY_TASK_NAMES)}."
        ),
    )
    parser.add_argument("--force", action="store_true", help="Ignore cached environment-fidelity outputs.")
    args = parser.parse_args()
    result = asyncio.run(
        run_environment_fidelity_analysis(
            config_path=args.config,
            results_base=args.results_base,
            output_dir=args.output_dir,
            load_existing=not args.force,
            target_behaviors=args.target_behaviors,
            fidelity_tasks=args.fidelity_tasks,
        )
    )
    print(prompt_json({"output_dir": result["output_dir"], "summary": result["summary"]}))


if __name__ == "__main__":
    main()
