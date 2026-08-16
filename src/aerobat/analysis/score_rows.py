"""Build the paper's observation rows from Stage 4 behavior scores."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

from aerobat.storage.ids import RunId
from aerobat.protocol.normalization import NormalizationManager
from aerobat.protocol.payloads import PayloadManager

from .helpers import (
    _fidelity_gate_rating,
    _behavior_eval_stats,
    _coerce_float,
    _include_in_analysis,
    _fidelity_gate_ratings_by_run,
)


def _analysis_row_context(
    config_design: Mapping[str, Any],
) -> tuple[Dict[tuple, Mapping[str, Any]], Dict[tuple, Mapping[str, Any]]]:
    """Stage-2 simulation specs and their matched groups, both keyed by (domain, i, j)."""
    simulation_by_run = {
        RunId.from_mapping(simulation).key: simulation
        for simulation in PayloadManager.simulation_entries_from_config_design(config_design)
    }
    group_by_run = {
        RunId.from_mapping(simulation).key: group
        for group in PayloadManager.simulation_groups_from_config_design(config_design)
        for simulation in group.get("simulations", [])
    }
    return simulation_by_run, group_by_run


def _analysis_base_row(
    *,
    hypothesis_id: str,
    config_design: Mapping[str, Any],
    entry: Mapping[str, Any],
    simulation: Mapping[str, Any],
    group: Mapping[str, Any],
) -> Dict[str, Any]:
    """Identity and design columns shared by every analysis row.

    `group_id` is the block b of the statistical model. It is domain-qualified, because group i
    restarts at 1 in every domain -- keying a block on i alone silently merges groups that were
    never matched to each other.
    """
    run = RunId.from_mapping(entry)
    return {
        "axis_slug": hypothesis_id,
        "variable": config_design.get("variable"),
        **run.as_dict(),
        "simulation_id": run.simulation_id,
        "group_id": run.group_id,
        "domain": group.get("domain") or simulation.get("domain"),
        "causal_variable": simulation.get("causal_variable"),
        "causal_value": simulation.get("causal_value"),
        "causal_rank": run.level_position,
    }


def behavior_score_rows(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
) -> List[Dict[str, Any]]:
    """Return one observation per reviewed run ``S_ij`` with score ``y_hat_ij``.

    ``axis_slug``, ``causal_rank``, and ``behavior_eval_mean_score`` are retained as
    legacy artifact keys; in the paper they denote hypothesis id, ``j - 1``, and
    ``y_hat_ij``, respectively.
    """

    rows = []
    for hypothesis_id in selected_hypothesis_ids:
        config_design = matched_configurations_by_id.get(hypothesis_id, {})
        review = blind_reviews_by_id.get(hypothesis_id) or {}
        simulation_by_run, group_by_run = _analysis_row_context(config_design)
        fidelity_rating_by_run = _fidelity_gate_ratings_by_run(review)
        for entry in review.get("simulations", []):
            if not _include_in_analysis(entry, fidelity_rating_by_run):
                continue
            behavior_eval = entry.get("behavior_eval")
            if not isinstance(behavior_eval, Mapping):
                continue
            fidelity_gate_rating = _fidelity_gate_rating(entry, fidelity_rating_by_run)
            run_key = RunId.from_mapping(entry).key
            stats = _behavior_eval_stats(entry)
            score = _coerce_float(stats.get("behavior_eval_mean_score"))
            if score is None:
                continue
            rows.append(
                {
                    **_analysis_base_row(
                        hypothesis_id=hypothesis_id,
                        config_design=config_design,
                        entry=entry,
                        simulation=simulation_by_run.get(run_key, {}),
                        group=group_by_run.get(run_key, {}),
                    ),
                    "behavior_eval_mean_score": score,
                    "analysis_validity_rating": fidelity_gate_rating,
                }
            )
    return rows


def behavior_evidence_class_score_rows(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
) -> List[Dict[str, Any]]:
    """Return one analysis row per reviewed simulation cell and evidence class."""

    rows = []
    for hypothesis_id in selected_hypothesis_ids:
        config_design = matched_configurations_by_id.get(hypothesis_id, {})
        review = blind_reviews_by_id.get(hypothesis_id) or {}
        simulation_by_run, group_by_run = _analysis_row_context(config_design)

        fidelity_rating_by_run = _fidelity_gate_ratings_by_run(review)
        for entry in review.get("simulations", []):
            if not _include_in_analysis(entry, fidelity_rating_by_run):
                continue
            behavior_eval = entry.get("behavior_eval")
            if not isinstance(behavior_eval, Mapping):
                continue
            assessment = behavior_eval.get("behavior_assessment")
            if not isinstance(assessment, Mapping):
                continue

            fidelity_gate_rating = _fidelity_gate_rating(entry, fidelity_rating_by_run)
            run_key = RunId.from_mapping(entry).key
            simulation = simulation_by_run.get(run_key, {})
            simulation_group = group_by_run.get(run_key, {})
            stats = _behavior_eval_stats(entry)
            class_scores = stats.get("behavior_evidence_class_scores") or {}

            for evidence_class, class_eval in assessment.items():
                if not isinstance(class_eval, Mapping):
                    continue
                score = NormalizationManager.level_score(class_eval.get("level_score"))
                if score is None:
                    score = _coerce_float(class_scores.get(evidence_class))
                if score is None:
                    continue
                rows.append(
                    {
                        **_analysis_base_row(
                            hypothesis_id=hypothesis_id,
                            config_design=config_design,
                            entry=entry,
                            simulation=simulation,
                            group=simulation_group,
                        ),
                        "evidence_class": str(evidence_class),
                        "behavior_eval_mean_score": score,
                        "analysis_validity_rating": fidelity_gate_rating,
                    }
                )
    return rows
