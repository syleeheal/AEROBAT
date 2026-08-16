"""Canonical on-disk schemas for pipeline artifacts.

The pipeline's protocol objects deliberately retain the exact field names emitted by
the LLMs.  This module only translates the surrounding storage envelope.  Consequently,
prompt text, raw responses, conservative parsing, and Stage 2 reconstruction are not
coupled to reader-facing artifact terminology.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    MATCHED_SIMULATION_RUNS,
    RESEARCH_REPORT_JSON,
    SENSITIVITY_ANALYSIS,
    STATISTICAL_ANALYSIS,
    canonical_filename,
)
from .ids import RunId


def _renamed(mapping: Mapping[str, Any] | None, names: Mapping[str, str]) -> dict[str, Any]:
    return {
        names.get(key, key): deepcopy(value)
        for key, value in (mapping or {}).items()
    }


_AGENT_NAMES = {
    "hypothesis_generation": {"stage_agent": "hypothesis_generator"},
    "matched_configuration_design": {"stage_agent": "configuration_designer"},
    "matched_simulation_runs": {
        "stage_3_subject_agent": "subject_agent",
        "stage_3_simulator_agent": "simulator_agent",
    },
    "blind_review": {"stage_agent": "blind_reviewer"},
}


def _token_usage(value: Any, stage: str, *, runtime: bool = False) -> dict[str, Any]:
    usage = deepcopy(value) if isinstance(value, Mapping) else {}
    names = _AGENT_NAMES.get(stage, {})
    if runtime:
        names = {canonical: legacy for legacy, canonical in names.items()}
    by_agent = usage.get("by_agent")
    if isinstance(by_agent, Mapping):
        usage["by_agent"] = _renamed(by_agent, names)
    calls = usage.get("calls")
    if isinstance(calls, list):
        for call in calls:
            if isinstance(call, dict) and call.get("agent") in names:
                call["agent"] = names[call["agent"]]
    return usage


def _canonical_gate(value: Any, legacy_pass_key: str, canonical_pass_key: str) -> Any:
    if not isinstance(value, Mapping):
        return deepcopy(value)
    return _renamed(value, {legacy_pass_key: canonical_pass_key})


def hypothesis_generation(payload: Mapping[str, Any]) -> dict[str, Any]:
    hypotheses = []
    for hypothesis in payload.get("hypotheses", []):
        row = deepcopy(hypothesis)
        if isinstance(row, dict) and "research_manager_review" in row:
            row["ranking_gate"] = _canonical_gate(
                row.pop("research_manager_review"), "passes_stage2", "passes_ranking_gate"
            )
        hypotheses.append(row)
    return {
        "target_behavior": payload.get("behavior_name"),
        "behavior_definition": payload.get("definition"),
        "behavior_evaluation_rubric": deepcopy(payload.get("behavior_eval_rubric", [])),
        "hypotheses": hypotheses,
        "metadata": deepcopy(payload.get("meta_data", {})),
        "token_usage": _token_usage(payload.get("token_counts"), "hypothesis_generation"),
        "hypothesis_generator_fallbacks": deepcopy(payload.get("fallbacks", [])),
        "ranking_gate_fallbacks": deepcopy(payload.get("research_manager_fallbacks", [])),
    }


def hypothesis_generation_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    hypotheses = []
    for hypothesis in payload.get("hypotheses", []):
        row = deepcopy(hypothesis)
        if isinstance(row, dict) and "ranking_gate" in row:
            row["research_manager_review"] = _canonical_gate(
                row.pop("ranking_gate"), "passes_ranking_gate", "passes_stage2"
            )
        hypotheses.append(row)
    return {
        "behavior_name": payload.get("target_behavior"),
        "definition": payload.get("behavior_definition"),
        "behavior_eval_rubric": deepcopy(payload.get("behavior_evaluation_rubric", [])),
        "hypotheses": hypotheses,
        "meta_data": deepcopy(payload.get("metadata", {})),
        "token_counts": _token_usage(
            payload.get("token_usage"), "hypothesis_generation", runtime=True
        ),
        "prompts": [],
        "fallbacks": deepcopy(payload.get("hypothesis_generator_fallbacks", [])),
        "research_manager_prompt": [],
        "research_manager_fallbacks": deepcopy(payload.get("ranking_gate_fallbacks", [])),
    }


def _configuration_domains(domains: Any, *, runtime: bool = False) -> list[Any]:
    rows = []
    for domain in domains if isinstance(domains, list) else []:
        row = deepcopy(domain)
        pass_three = row.get("pass_three") if isinstance(row, dict) else None
        if isinstance(pass_three, Mapping):
            for group in pass_three.values():
                if not isinstance(group, dict):
                    continue
                if runtime and "coherence_gate" in group:
                    group["research_manager_review"] = group.pop("coherence_gate")
                elif not runtime and "research_manager_review" in group:
                    group["coherence_gate"] = group.pop("research_manager_review")
                old, new = (
                    ("passes_coherence_gate", "passes_stage3")
                    if runtime
                    else ("passes_stage3", "passes_coherence_gate")
                )
                if old in group:
                    group[new] = group.pop(old)
        rows.append(row)
    return rows


def matched_configurations(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_behavior": payload.get("behavior_name"),
        "hypothesis_id": payload.get("axis_slug"),
        "hypothesized_causal_variable": payload.get("variable"),
        "metadata": deepcopy(payload.get("meta_data", {})),
        "hypothesis_domain_designs": _configuration_domains(payload.get("domain_results")),
        "token_usage": _token_usage(
            payload.get("token_counts"), "matched_configuration_design"
        ),
        "configuration_designer_fallbacks": deepcopy(payload.get("fallbacks", [])),
        "coherence_gate_fallbacks": deepcopy(payload.get("research_manager_fallbacks", [])),
    }


def matched_configurations_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "behavior_name": payload.get("target_behavior"),
        "axis_slug": payload.get("hypothesis_id"),
        "variable": payload.get("hypothesized_causal_variable"),
        "meta_data": deepcopy(payload.get("metadata", {})),
        "domain_results": _configuration_domains(
            payload.get("hypothesis_domain_designs"), runtime=True
        ),
        "token_counts": _token_usage(
            payload.get("token_usage"), "matched_configuration_design", runtime=True
        ),
        "prompts": [],
        "fallbacks": deepcopy(payload.get("configuration_designer_fallbacks", [])),
        "research_manager_prompt": [],
        "research_manager_fallbacks": deepcopy(payload.get("coherence_gate_fallbacks", [])),
    }


_AGENT_CONFIG_KEYS = (
    "model",
    "reasoning_effort",
    "reasoning_summary",
    "service_tier",
    "temperature",
    "max_tokens",
)


def _agent_config(metadata: Mapping[str, Any], agent: str) -> dict[str, Any]:
    return {
        key: deepcopy(metadata[f"{agent}_{key}"])
        for key in _AGENT_CONFIG_KEYS
        if f"{agent}_{key}" in metadata
    }


def simulation_transcript(payload: Mapping[str, Any]) -> dict[str, Any]:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), Mapping) else {}
    run = RunId.from_mapping(metadata)
    result = {
        "run": run.as_dict(),
        "candidate_value": metadata.get("causal_value"),
        "environment_rendering_format": (
            metadata.get("environment_rendering_format") or metadata.get("simulation_format")
        ),
        "agents": {
            "subject_agent": _agent_config(metadata, "subject_agent"),
            "simulator_agent": _agent_config(metadata, "simulator_agent"),
        },
        "rounds": deepcopy(payload.get("rounds", [])),
        "token_usage": _token_usage(payload.get("token_counts"), "matched_simulation_runs"),
        "simulation_fallbacks": deepcopy(payload.get("fallbacks", [])),
        "fidelity_gate": deepcopy(payload.get("research_manager_review")),
        "fidelity_gate_fallbacks": deepcopy(payload.get("research_manager_fallbacks", [])),
    }
    if "passes_stage4" in payload:
        result["passes_fidelity_gate"] = payload["passes_stage4"]
    return result


def simulation_transcript_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    run = RunId.from_mapping(payload)
    agents = payload.get("agents") if isinstance(payload.get("agents"), Mapping) else {}
    execution = payload.get("execution") if isinstance(payload.get("execution"), Mapping) else {}
    metadata = {
        **run.as_dict(),
        **{
            f"{agent}_{key}": value
            for agent in ("subject_agent", "simulator_agent")
            for key, value in (
                agents.get(agent).items() if isinstance(agents.get(agent), Mapping) else []
            )
        },
        **deepcopy(execution),
        "causal_value": payload.get("candidate_value"),
        "environment_rendering_format": payload.get("environment_rendering_format"),
        "total_rounds": len(payload.get("rounds", [])),
    }
    result = {
        "metadata": metadata,
        "rounds": deepcopy(payload.get("rounds", [])),
        "token_counts": _token_usage(
            payload.get("token_usage"), "matched_simulation_runs", runtime=True
        ),
        "prompts": {"stage_3_subject_agent": [], "stage_3_simulator_agent": []},
        "fallbacks": deepcopy(payload.get("simulation_fallbacks", [])),
        "research_manager_review": deepcopy(payload.get("fidelity_gate")),
        "research_manager_prompt": [],
        "research_manager_fallbacks": deepcopy(payload.get("fidelity_gate_fallbacks", [])),
    }
    if "passes_fidelity_gate" in payload:
        result["passes_stage4"] = payload["passes_fidelity_gate"]
    return result


def matched_simulation_runs(payload: Mapping[str, Any]) -> dict[str, Any]:
    runs = []
    for entry in payload.get("runs", []):
        if not isinstance(entry, Mapping):
            continue
        run = RunId.from_mapping(entry)
        runs.append(
            {
                "run": run.as_dict(),
                "candidate_value": entry.get("causal_value"),
                "environment_rendering_format": entry.get("environment_rendering_format"),
            }
        )
    return {
        "design": {
            "repetitions": payload.get("num_reps"),
            "rounds_per_simulation": payload.get("num_rounds"),
            "environment_rendering_formats": deepcopy(
                payload.get("environment_rendering_formats", [])
            ),
        },
        "runs": runs,
    }


def matched_simulation_runs_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    design = payload.get("design") if isinstance(payload.get("design"), Mapping) else {}
    runs = []
    for entry in payload.get("runs", []):
        if not isinstance(entry, Mapping):
            continue
        run = RunId.from_mapping(entry)
        runs.append(
            {
                **run.as_dict(),
                "causal_value": entry.get("candidate_value"),
                "environment_rendering_format": entry.get("environment_rendering_format"),
            }
        )
    return {
        "num_reps": design.get("repetitions"),
        "num_rounds": design.get("rounds_per_simulation"),
        "environment_rendering_formats": deepcopy(
            design.get("environment_rendering_formats", [])
        ),
        "runs": runs,
    }


def blind_review(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run": RunId.from_mapping(payload).as_dict(),
        "behavior_evaluation": deepcopy(payload.get("behavior_eval")),
        "token_usage": _token_usage(payload.get("token_counts"), "blind_review"),
        "blind_reviewer_fallbacks": deepcopy(payload.get("fallbacks", [])),
    }


def blind_review_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        **RunId.from_mapping(payload).as_dict(),
        "behavior_eval": deepcopy(payload.get("behavior_evaluation")),
        "token_counts": _token_usage(payload.get("token_usage"), "blind_review", runtime=True),
        "prompts": [],
        "fallbacks": deepcopy(payload.get("blind_reviewer_fallbacks", [])),
    }


def _observation(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run": RunId.from_mapping(row).as_dict(),
        "domain": row.get("domain"),
        "candidate_value": row.get("causal_value"),
        "level_position": row.get("causal_rank"),
        "behavior_score": row.get("behavior_eval_mean_score"),
        "fidelity_gate_rating": row.get("analysis_validity_rating"),
        **({"evidence_class": row["evidence_class"]} if "evidence_class" in row else {}),
    }


def _observation_runtime(
    row: Mapping[str, Any], hypothesis_id: Any, variable: Any
) -> dict[str, Any]:
    run = RunId.from_mapping(row)
    return {
        "axis_slug": hypothesis_id,
        "variable": variable,
        **run.as_dict(),
        "simulation_id": run.simulation_id,
        "group_id": run.group_id,
        "domain": row.get("domain"),
        "causal_variable": variable,
        "causal_value": row.get("candidate_value"),
        "causal_rank": row.get("level_position"),
        "behavior_eval_mean_score": row.get("behavior_score"),
        "analysis_validity_rating": row.get("fidelity_gate_rating"),
        **({"evidence_class": row["evidence_class"]} if "evidence_class" in row else {}),
    }


def statistical_analysis(payload: Mapping[str, Any]) -> dict[str, Any]:
    summary = (
        payload.get("review", {}).get("summary_statistics", {})
        if isinstance(payload.get("review"), Mapping)
        else {}
    )
    counts = summary.get("reviewer_counts") if isinstance(summary.get("reviewer_counts"), Mapping) else {}
    diagnostics = []
    for row in payload.get("diagnostic_rows", []):
        if isinstance(row, Mapping):
            diagnostics.append(
                {key: deepcopy(value) for key, value in row.items() if key not in {"axis_slug", "variable"}}
            )
    return {
        "target_behavior": payload.get("behavior_name"),
        "hypothesis_id": payload.get("axis_slug"),
        "hypothesized_causal_variable": payload.get("variable"),
        "saved_at": payload.get("saved_at"),
        "behavior_evaluation_summary": {
            "mean_behavior_score": summary.get("mean_behavior_eval_score"),
            "mean_behavior_score_by_evidence_class": deepcopy(
                summary.get("mean_behavior_eval_score_by_evidence_class", {})
            ),
            "evaluated_simulations": counts.get("behavior_eval"),
        },
        "observations": [
            _observation(row)
            for row in payload.get("behavior_eval_rows", [])
            if isinstance(row, Mapping)
        ],
        "effect_analyses": diagnostics,
        "statistical_analysis": deepcopy(payload.get("quantitative_analysis", {})),
    }


def statistical_analysis_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    hypothesis_id = payload.get("hypothesis_id")
    variable = payload.get("hypothesized_causal_variable")
    summary = payload.get("behavior_evaluation_summary") or {}
    diagnostics = [
        {"axis_slug": hypothesis_id, "variable": variable, **deepcopy(row)}
        for row in payload.get("effect_analyses", [])
        if isinstance(row, Mapping)
    ]
    observations = [
        _observation_runtime(row, hypothesis_id, variable)
        for row in payload.get("observations", [])
        if isinstance(row, Mapping)
    ]
    return {
        "axis_slug": hypothesis_id,
        "variable": variable,
        "behavior_name": payload.get("target_behavior"),
        "saved_at": payload.get("saved_at"),
        "review": {
            "reviewers": {"behavior_eval": True},
            "summary_statistics": {
                "mean_behavior_eval_score": summary.get("mean_behavior_score"),
                "mean_behavior_eval_score_by_evidence_class": deepcopy(
                    summary.get("mean_behavior_score_by_evidence_class", {})
                ),
                "reviewer_counts": {
                    "behavior_eval": summary.get("evaluated_simulations")
                },
            },
        },
        "behavior_eval_rows": observations,
        "diagnostic_rows": diagnostics,
        "quantitative_analysis": deepcopy(payload.get("statistical_analysis", {})),
    }


def sensitivity_analysis(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_behavior": payload.get("behavior_name"),
        "hypothesis_id": payload.get("axis_slug"),
        "hypothesized_causal_variable": payload.get("variable"),
        **{
            key: deepcopy(value)
            for key, value in payload.items()
            if key not in {"behavior_name", "axis_slug", "variable", "source_analytic_results"}
        },
        "source_statistical_analysis": "statistical_analysis.json",
    }


def research_report(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_behavior": payload.get("behavior_name"),
        "hypothesis_id": payload.get("axis_slug"),
        "hypothesized_causal_variable": payload.get("variable"),
        "metadata": deepcopy(payload.get("meta_data", {})),
        "report": deepcopy(payload.get("report", [])),
        "token_usage": _token_usage(payload.get("token_counts"), "research_report"),
        "research_manager_fallbacks": deepcopy(payload.get("fallbacks", [])),
    }


def research_report_runtime(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "behavior_name": payload.get("target_behavior"),
        "axis_slug": payload.get("hypothesis_id"),
        "variable": payload.get("hypothesized_causal_variable"),
        "meta_data": deepcopy(payload.get("metadata", {})),
        "report": deepcopy(payload.get("report", [])),
        "token_counts": _token_usage(payload.get("token_usage"), "research_report", runtime=True),
        "research_manager_prompt": [],
        "fallbacks": deepcopy(payload.get("research_manager_fallbacks", [])),
    }


def canonical_artifact(filename: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Translate one pipeline artifact to its canonical on-disk schema."""
    name = canonical_filename(filename)
    if name == HYPOTHESIS_GENERATION:
        return hypothesis_generation(payload)
    if name == MATCHED_CONFIGURATIONS:
        return matched_configurations(payload)
    if name == MATCHED_SIMULATION_RUNS:
        return matched_simulation_runs(payload)
    if name == STATISTICAL_ANALYSIS:
        return statistical_analysis(payload)
    if name == SENSITIVITY_ANALYSIS:
        return sensitivity_analysis(payload)
    if name == RESEARCH_REPORT_JSON:
        return research_report(payload)
    if name.startswith("simulation_i"):
        return simulation_transcript(payload)
    if name.startswith("review_i"):
        return blind_review(payload)
    return deepcopy(dict(payload))


def runtime_artifact(filename: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Translate a canonical artifact into the unchanged protocol/runtime shape."""
    name = canonical_filename(filename)
    if name == HYPOTHESIS_GENERATION:
        return hypothesis_generation_runtime(payload)
    if name == MATCHED_CONFIGURATIONS:
        return matched_configurations_runtime(payload)
    if name == MATCHED_SIMULATION_RUNS:
        return matched_simulation_runs_runtime(payload)
    if name == STATISTICAL_ANALYSIS:
        return statistical_analysis_runtime(payload)
    if name == RESEARCH_REPORT_JSON:
        return research_report_runtime(payload)
    if name.startswith("simulation_i"):
        return simulation_transcript_runtime(payload)
    if name.startswith("review_i"):
        return blind_review_runtime(payload)
    return deepcopy(dict(payload))
