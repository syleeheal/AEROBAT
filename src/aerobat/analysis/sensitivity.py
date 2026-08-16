"""Prior-scale and rubric robustness analyses for the appendices."""

from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from ..storage.artifacts import STATISTICAL_ANALYSIS, iter_hypothesis_dirs
from ..storage.schema import runtime_artifact
from ..utils import load_json
from .effects import MonotoneAnalysisOptions, analyze_hypothesis_effect


def _fit(rows: list[dict[str, Any]], prior_scale: float) -> dict[str, Any]:
    # Rank-correlation permutations are invariant to the prior and are not needed by
    # either robustness analysis.
    return analyze_hypothesis_effect(
        rows,
        MonotoneAnalysisOptions(prior_scale=prior_scale, tau_permutations=0),
    )


def prior_sensitivity(
    results_dir: str | Path,
    scales: Iterable[float] = (0.5, math.sqrt(2) / 2, 1.0),
    *,
    workers: int | None = None,
) -> pd.DataFrame:
    """Refit every stored aggregate analysis under each Cauchy prior scale."""
    tasks = []
    for hypothesis_dir in iter_hypothesis_dirs(results_dir):
        path = hypothesis_dir / STATISTICAL_ANALYSIS
        payload = runtime_artifact(path.name, load_json(path))
        score_rows = payload.get("behavior_eval_rows") or []
        baseline = (payload.get("quantitative_analysis") or {}).get("aggregate_mean") or {}
        baseline_bf = (baseline.get("monotone_analysis") or {}).get("bf10")
        for scale in scales:
            tasks.append((payload, hypothesis_dir, score_rows, baseline_bf, float(scale)))

    worker_count = workers or min(8, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=worker_count) as pool:
        fits = list(pool.map(_fit_star, [(item[2], item[4]) for item in tasks]))

    rows = []
    for (payload, hypothesis_dir, _score_rows, baseline_bf, scale), result in zip(tasks, fits):
        bf10 = result["monotone_analysis"]["bf10"]
        rows.append({
            "behavior_name": payload.get("behavior_name", hypothesis_dir.parent.name),
            "axis_slug": payload.get("axis_slug", hypothesis_dir.name),
            "prior_scale": scale,
            "bf10": bf10,
            "log10_bf10": math.log10(bf10) if bf10 and bf10 > 0 else None,
            "baseline_bf10": baseline_bf,
            "baseline_log10_bf10": math.log10(baseline_bf) if baseline_bf and baseline_bf > 0 else None,
            "effect_class": result["effect_class"],
            "Delta": result["effect_size"]["Delta"],
            "log10_bf10_mcse": result["monotone_analysis"]["log10_bf10_mcse"],
        })
    frame = pd.DataFrame(rows)
    frame["absolute_log10_shift"] = (frame.log10_bf10 - frame.baseline_log10_bf10).abs()
    return frame


def _fit_star(arguments: tuple[list[dict[str, Any]], float]) -> dict[str, Any]:
    return _fit(*arguments)


def prior_sensitivity_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby("prior_scale")
        .agg(
            hypotheses=("axis_slug", "size"),
            median_absolute_log10_shift=("absolute_log10_shift", "median"),
            max_absolute_log10_shift=("absolute_log10_shift", "max"),
            median_mcse=("log10_bf10_mcse", "median"),
            max_mcse=("log10_bf10_mcse", "max"),
        )
        .reset_index()
    )
