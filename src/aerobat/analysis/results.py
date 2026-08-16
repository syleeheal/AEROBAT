"""Load review artifacts, build analysis rows, and write hypothesis results."""

from __future__ import annotations

import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ..storage.artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    STATISTICAL_ANALYSIS,
    iter_hypothesis_dirs,
)
from ..storage.schema import canonical_artifact, runtime_artifact
from ..utils import load_json, save_json
from ..storage.ids import RunId
from ..utils import mean_or_none
from .score_rows import behavior_evidence_class_score_rows, behavior_score_rows
from .effects import MonotoneAnalysisOptions, analyze_hypothesis_effect


def _review_paths(hypothesis_dir: Path) -> list[Path]:
    return sorted(hypothesis_dir.glob("*/reviews/review_i*_j*_rep*.json"))


def _transcript_path(hypothesis_dir: Path, run_id: RunId) -> Path:
    return hypothesis_dir / run_id.domain_slug / "simulations" / f"simulation_i{run_id.group_index}_j{run_id.value_index}_rep{run_id.repetition}.json"


def _config_with_hypothesis(root: Path) -> dict[str, Any]:
    config_path = root / MATCHED_CONFIGURATIONS
    config = runtime_artifact(config_path.name, load_json(config_path))
    if isinstance(config.get("hypothesis"), Mapping):
        return config
    hypothesis_path = root.parent / HYPOTHESIS_GENERATION
    if not hypothesis_path.exists():
        return config
    hypotheses = runtime_artifact(
        hypothesis_path.name, load_json(hypothesis_path)
    ).get("hypotheses", [])
    hypothesis = next(
        (
            item
            for item in hypotheses
            if isinstance(item, Mapping)
            and str(item.get("variable")) == str(config.get("variable"))
        ),
        None,
    )
    return {**config, "hypothesis": dict(hypothesis)} if hypothesis else config


def _review_entries(root: Path) -> list[dict[str, Any]]:
    entries = []
    for review_path in _review_paths(root):
        review = runtime_artifact(review_path.name, load_json(review_path))
        transcript_path = _transcript_path(root, RunId.from_mapping(review))
        if transcript_path.exists() and not runtime_artifact(
            transcript_path.name, load_json(transcript_path)
        ).get("passes_stage4", True):
            continue
        entries.append(review)
    return entries


def build_observation_rows(hypothesis_dir: str | Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build observations ``(x_j, y_hat_ij)`` from stored blind reviews."""
    root = Path(hypothesis_dir)
    config = _config_with_hypothesis(root)
    hypothesis_id = str(config.get("axis_slug", root.name))
    blind_reviews_by_id = {hypothesis_id: {"simulations": _review_entries(root)}}
    config_by_slug = {hypothesis_id: config}
    return (
        behavior_score_rows(blind_reviews_by_id, config_by_slug, [hypothesis_id]),
        behavior_evidence_class_score_rows(blind_reviews_by_id, config_by_slug, [hypothesis_id]),
    )


def analyze_hypothesis(hypothesis_dir: str | Path, options: MonotoneAnalysisOptions = MonotoneAnalysisOptions(), *, save: bool = True) -> dict[str, Any]:
    """Recompute the paper's full analysis artifact for one hypothesis."""
    root = Path(hypothesis_dir)
    config_path = root / MATCHED_CONFIGURATIONS
    config = runtime_artifact(config_path.name, load_json(config_path))
    aggregate_rows, evidence_rows = build_observation_rows(root)
    aggregate = analyze_hypothesis_effect(aggregate_rows, options)
    quantitative: dict[str, Any] = {
        "analysis_design": (
            "randomized complete block design; block-stratified Kendall tau-b and "
            "Bayesian monotone-increment analysis"
        ),
        "aggregate_mean": aggregate,
    }
    diagnostics = [{"axis_slug": root.name, "variable": config.get("variable"), "outcome": "aggregate_mean", **aggregate}]
    for evidence_class in sorted({row["evidence_class"] for row in evidence_rows}):
        rows = [row for row in evidence_rows if row["evidence_class"] == evidence_class]
        result = analyze_hypothesis_effect(rows, options)
        quantitative[evidence_class] = result
        diagnostics.append({"axis_slug": root.name, "variable": config.get("variable"), "outcome": evidence_class, **result})
    class_means = {
        name: mean_or_none(
            [
                row["behavior_eval_mean_score"]
                for row in evidence_rows
                if row["evidence_class"] == name
            ]
        )
        for name in sorted({row["evidence_class"] for row in evidence_rows})
    }
    payload = {
        "axis_slug": root.name,
        "variable": config.get("variable"),
        "behavior_name": config.get("behavior_name", root.parent.name),
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "review": {
            "summary_statistics": {
                "mean_behavior_eval_score": mean_or_none(
                    [row["behavior_eval_mean_score"] for row in aggregate_rows]
                ),
                "mean_behavior_eval_score_by_evidence_class": class_means,
                "reviewer_counts": {"behavior_eval": len(aggregate_rows)},
            },
        },
        "behavior_eval_rows": aggregate_rows,
        "diagnostic_rows": diagnostics,
        "quantitative_analysis": quantitative,
    }
    if save:
        path = root / STATISTICAL_ANALYSIS
        save_json(canonical_artifact(path.name, payload), path)
    return payload


def load_behavioral_findings(results_dir: str | Path) -> pd.DataFrame:
    """One tidy row per reported hypothesis, from stored analysis artifacts."""
    rows = []
    for hypothesis_dir in iter_hypothesis_dirs(results_dir):
        analysis_path = hypothesis_dir / STATISTICAL_ANALYSIS
        payload = runtime_artifact(analysis_path.name, load_json(analysis_path))
        aggregate = (payload.get("quantitative_analysis") or {}).get("aggregate_mean") or {}
        monotone = aggregate.get("monotone_analysis") or {}
        effect = aggregate.get("effect_size") or {}
        rank_association = aggregate.get("rank_correlation") or {}
        config_path = hypothesis_dir / MATCHED_CONFIGURATIONS
        config = runtime_artifact(config_path.name, load_json(config_path)) if config_path.exists() else {}
        hypothesis = config.get("hypothesis") or {}
        if not hypothesis:
            hypothesis_path = hypothesis_dir.parent / HYPOTHESIS_GENERATION
            if hypothesis_path.exists():
                candidates = runtime_artifact(
                    hypothesis_path.name, load_json(hypothesis_path)
                ).get("hypotheses", [])
                hypothesis = next((item for item in candidates if str(item.get("variable")) == str(payload.get("variable"))), {})
        rows.append({
            "behavior_name": payload.get("behavior_name", hypothesis_dir.parent.name),
            "axis_slug": payload.get("axis_slug", hypothesis_dir.name),
            "variable": payload.get("variable", config.get("variable")),
            "var_dimension": hypothesis.get("var_dimension"),
            "causal_effect": hypothesis.get("causal_effect"),
            "n": aggregate.get("n"),
            "effect_class": aggregate.get("effect_class"),
            "bf10": monotone.get("bf10"),
            "log10_bf10": math.log10(monotone["bf10"]) if isinstance(monotone.get("bf10"), (int, float)) and monotone["bf10"] > 0 else None,
            "Delta": effect.get("Delta"),
            "Delta_low": (effect.get("Delta_ci_95") or [None, None])[0],
            "Delta_high": (effect.get("Delta_ci_95") or [None, None])[1],
            "tau": rank_association.get("tau"),
            "p_tau": rank_association.get("p_tau"),
            "hypothesis_dir": hypothesis_dir,
        })
    return pd.DataFrame(rows).sort_values(["behavior_name", "axis_slug"]).reset_index(drop=True)
