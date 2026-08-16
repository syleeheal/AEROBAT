"""Build, save, and load per-hypothesis analysis artifacts."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import now

from .effects import effect_analysis_rows
from .helpers import _rows_by_hypothesis
from .score_rows import behavior_score_rows


def research_report_analyses_by_hypothesis(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    *,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
    diagnostic_rows: Sequence[Mapping[str, Any]] | None = None,
) -> Dict[str, Dict[str, Any]]:
    rows = (
        [dict(row) for row in diagnostic_rows]
        if diagnostic_rows is not None
        else effect_analysis_rows(
            blind_reviews_by_id,
            matched_configurations_by_id,
            selected_hypothesis_ids,
            effect_bf_threshold=effect_bf_threshold,
            no_effect_bf_threshold=no_effect_bf_threshold,
            tau_near_zero_threshold=tau_near_zero_threshold,
            monotone_prior_scale=monotone_prior_scale,
            monotone_increment_samples=monotone_increment_samples,
            monotone_prior_grid_points=monotone_prior_grid_points,
            monotone_direction_probability_threshold=(
                monotone_direction_probability_threshold
            ),
        )
    )
    rows_by_hypothesis = _rows_by_hypothesis(rows)
    out: Dict[str, Dict[str, Any]] = {}
    for hypothesis_id in selected_hypothesis_ids:
        quantitative_analysis: Dict[str, Any] = {
            "analysis_design": (
                "randomized complete block design; block-stratified Kendall tau-b and "
                "Bayesian monotone-increment analysis"
            ),
        }
        for row in rows_by_hypothesis.get(hypothesis_id, []):
            outcome = row.get("outcome")
            if outcome:
                quantitative_analysis[str(outcome)] = {
                    key: value
                    for key, value in row.items()
                    if key not in {"axis_slug", "variable", "outcome"}
                }
        out[str(hypothesis_id)] = quantitative_analysis
    return out


def statistical_analyses_by_hypothesis(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    *,
    behavior_name: str,
    diagnostic_rows: Sequence[Mapping[str, Any]] | None = None,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
) -> Dict[str, Dict[str, Any]]:
    diagnostic_rows = (
        [dict(row) for row in diagnostic_rows]
        if diagnostic_rows is not None
        else effect_analysis_rows(
            blind_reviews_by_id,
            matched_configurations_by_id,
            selected_hypothesis_ids,
            effect_bf_threshold=effect_bf_threshold,
            no_effect_bf_threshold=no_effect_bf_threshold,
            tau_near_zero_threshold=tau_near_zero_threshold,
            monotone_prior_scale=monotone_prior_scale,
            monotone_increment_samples=monotone_increment_samples,
            monotone_prior_grid_points=monotone_prior_grid_points,
            monotone_direction_probability_threshold=(
                monotone_direction_probability_threshold
            ),
        )
    )
    diagnostic_rows_by_hypothesis = _rows_by_hypothesis(diagnostic_rows)
    research_report_analyses = research_report_analyses_by_hypothesis(
        blind_reviews_by_id,
        matched_configurations_by_id,
        selected_hypothesis_ids,
        effect_bf_threshold=effect_bf_threshold,
        no_effect_bf_threshold=no_effect_bf_threshold,
        tau_near_zero_threshold=tau_near_zero_threshold,
        monotone_prior_scale=monotone_prior_scale,
        monotone_increment_samples=monotone_increment_samples,
        monotone_prior_grid_points=monotone_prior_grid_points,
        monotone_direction_probability_threshold=(
            monotone_direction_probability_threshold
        ),
        diagnostic_rows=diagnostic_rows,
    )
    results: Dict[str, Dict[str, Any]] = {}
    for hypothesis_id in selected_hypothesis_ids:
        config_design = matched_configurations_by_id.get(hypothesis_id, {})
        review = blind_reviews_by_id.get(hypothesis_id) or {}
        results[str(hypothesis_id)] = {
            "axis_slug": hypothesis_id,
            "variable": config_design.get("variable"),
            "behavior_name": behavior_name,
            "saved_at": now(),
            "review": {
                "summary_statistics": review.get("summary_statistics") or {},
            },
            "behavior_eval_rows": behavior_score_rows(
                blind_reviews_by_id,
                matched_configurations_by_id,
                [hypothesis_id],
            ),
            "diagnostic_rows": diagnostic_rows_by_hypothesis.get(hypothesis_id, []),
            "quantitative_analysis": research_report_analyses.get(hypothesis_id, {}),
        }
    return results


def save_statistical_analyses(
    *,
    results_dir: str | Path,
    behavior_name: str,
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    diagnostic_rows: Sequence[Mapping[str, Any]] | None = None,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
) -> List[Path]:
    results_by_hypothesis = statistical_analyses_by_hypothesis(
        blind_reviews_by_id,
        matched_configurations_by_id,
        selected_hypothesis_ids,
        behavior_name=behavior_name,
        diagnostic_rows=diagnostic_rows,
        effect_bf_threshold=effect_bf_threshold,
        no_effect_bf_threshold=no_effect_bf_threshold,
        tau_near_zero_threshold=tau_near_zero_threshold,
        monotone_prior_scale=monotone_prior_scale,
        monotone_increment_samples=monotone_increment_samples,
        monotone_prior_grid_points=monotone_prior_grid_points,
        monotone_direction_probability_threshold=(
            monotone_direction_probability_threshold
        ),
    )
    return TranscriptManager(results_dir).save_statistical_analyses(
        results_by_hypothesis=results_by_hypothesis,
    )


def load_statistical_analyses(
    *,
    results_dir: str | Path,
    selected_hypothesis_ids: Sequence[str],
    require_all: bool = True,
) -> Dict[str, Dict[str, Any]]:
    transcript_manager = TranscriptManager(results_dir)
    results = {}
    missing = []
    for hypothesis_id in selected_hypothesis_ids:
        payload = transcript_manager.load_statistical_analysis(str(hypothesis_id))
        if payload is None:
            missing.append(str(hypothesis_id))
        else:
            results[str(hypothesis_id)] = payload
    if missing and require_all:
        raise FileNotFoundError(
            "Missing statistical_analysis.json for selected hypothesis slug(s): "
            + ", ".join(missing)
        )
    return results
