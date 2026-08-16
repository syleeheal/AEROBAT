"""Alternative Stage 4 score constructions used in Appendix E."""

from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ..effects import MonotoneAnalysisOptions, analyze_hypothesis_effect
from .measurement import RUN_COLUMNS, load_rubric_score_cells

DEFAULT_PRIOR_SCALE = math.sqrt(2) / 2
SIMPLE_VARIANTS = (
    "available_case",
    "null_as_zero",
    "complete_case",
)


def reconstruct_behavior_scores(
    cells: pd.DataFrame,
    rule: str,
    *,
    evidence_class: str | None = None,
    most_null_class: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """Rebuild run-level scores while preserving the estimator's row contract."""
    frame = cells.copy()
    if rule == "null_as_zero":
        frame["score"] = frame.score.fillna(0.0)
    elif rule == "complete_case":
        complete = frame.groupby(RUN_COLUMNS).score.transform(lambda values: values.notna().all())
        frame = frame[complete]
    elif rule == "drop_most_null_class":
        if most_null_class is None:
            raise ValueError("drop_most_null_class requires one class per target behavior")
        keep = [
            evidence != most_null_class.get(behavior)
            for behavior, evidence in zip(frame.target_behavior, frame.evidence_class)
        ]
        frame = frame[keep]
    elif rule == "leave_one_out":
        if evidence_class is None:
            raise ValueError("leave_one_out requires evidence_class")
        frame = frame[frame.evidence_class != evidence_class]
    elif rule == "single_class":
        if evidence_class is None:
            raise ValueError("single_class requires evidence_class")
        frame = frame[frame.evidence_class == evidence_class]
    elif rule != "available_case":
        raise ValueError(f"Unknown rubric reconstruction rule: {rule}")

    scores = (
        frame.groupby(RUN_COLUMNS, as_index=False)
        .agg(
            behavior_eval_mean_score=("score", "mean"),
            causal_rank=("level_position", "first"),
            group_id=("block_id", "first"),
        )
        .dropna(subset=["behavior_eval_mean_score"])
    )
    return scores


def _most_null_classes(cells: pd.DataFrame) -> dict[str, str]:
    rates = cells.groupby(["target_behavior", "evidence_class"]).score.apply(
        lambda values: float(values.isna().mean())
    )
    return {
        behavior: block.idxmax()[1]
        for behavior, block in rates.groupby(level="target_behavior")
    }


def _variant_tasks(cells: pd.DataFrame) -> list[tuple[str, str, str, str, list[dict[str, Any]]]]:
    worst = _most_null_classes(cells)
    tasks: list[tuple[str, str, str, str, list[dict[str, Any]]]] = []
    for (behavior, hypothesis), block in cells.groupby(
        ["target_behavior", "hypothesis_id"], sort=True
    ):
        classes = list(block.evidence_class.drop_duplicates())
        variants = [(name, "") for name in SIMPLE_VARIANTS]
        variants.append(("drop_most_null_class", worst[behavior]))
        variants.extend(("leave_one_out", name) for name in classes)
        variants.extend(("single_class", name) for name in classes)
        for family, member in variants:
            rebuilt = reconstruct_behavior_scores(
                block,
                family,
                evidence_class=member or None,
                most_null_class=worst,
            )
            rows = rebuilt[
                ["causal_rank", "behavior_eval_mean_score", "group_id"]
            ].to_dict("records")
            tasks.append((behavior, hypothesis, family, member, rows))
    return tasks


def _fit_task(
    task: tuple[str, str, str, str, list[dict[str, Any]]]
) -> dict[str, Any]:
    behavior, hypothesis, family, member, rows = task
    result = analyze_hypothesis_effect(
        rows,
        MonotoneAnalysisOptions(
            prior_scale=DEFAULT_PRIOR_SCALE,
            tau_permutations=0,
        ),
    )
    return {
        "target_behavior": behavior,
        "hypothesis_id": hypothesis,
        "variant": family if not member else f"{family}::{member}",
        "variant_family": family,
        "evidence_class": member or None,
        "n": len(rows),
        "effect_class": result.get("effect_class"),
        "bf10": (result.get("monotone_analysis") or {}).get("bf10"),
        "Delta": (result.get("effect_size") or {}).get("Delta"),
        "tau": (result.get("rank_correlation") or {}).get("tau"),
    }


def _task_keys(tasks: list[tuple[str, str, str, str, list[dict[str, Any]]]]) -> set[tuple[str, str, str]]:
    return {
        (behavior, hypothesis, family if not member else f"{family}::{member}")
        for behavior, hypothesis, family, member, _ in tasks
    }


def rubric_sensitivity(
    results_dir: str | Path,
    *,
    cells: pd.DataFrame | None = None,
    workers: int | None = None,
    cache_path: str | Path | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Refit all Appendix E null-handling and evidence-class variants."""
    score_cells = load_rubric_score_cells(results_dir) if cells is None else cells
    tasks = _variant_tasks(score_cells)
    path = Path(cache_path) if cache_path is not None else None
    expected_keys = _task_keys(tasks)

    frame: pd.DataFrame | None = None
    if path is not None and path.exists() and not force:
        cached = pd.read_csv(path)
        cached_keys = set(zip(cached.target_behavior, cached.hypothesis_id, cached.variant))
        if cached_keys == expected_keys:
            frame = cached

    if frame is None:
        worker_count = workers or min(8, os.cpu_count() or 1)
        with ProcessPoolExecutor(max_workers=worker_count) as pool:
            frame = pd.DataFrame(pool.map(_fit_task, tasks, chunksize=4))
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            frame.to_csv(path, index=False)

    baseline = (
        frame[frame.variant_family == "available_case"]
        .set_index(["target_behavior", "hypothesis_id"])
        [["n", "effect_class", "bf10", "Delta"]]
        .add_prefix("baseline_")
    )
    frame = frame.drop(
        columns=[column for column in frame if column.startswith("baseline_")],
        errors="ignore",
    ).join(baseline, on=["target_behavior", "hypothesis_id"])
    frame["bf10_evidence"] = frame.bf10 >= 3
    frame["baseline_bf10_evidence"] = frame.baseline_bf10 >= 3
    return frame.sort_values(["target_behavior", "hypothesis_id", "variant"]).reset_index(
        drop=True
    )


def sensitivity_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize each variant family against the available-case composite."""
    rows = []
    for family, block in frame.groupby("variant_family", sort=False):
        valid = block.dropna(subset=["Delta", "baseline_Delta"])
        rows.append(
            {
                "variant_family": family,
                "fits": len(block),
                "hypotheses": block[["target_behavior", "hypothesis_id"]]
                .drop_duplicates()
                .shape[0],
                "minimum_n": int(block.n.min()),
                "median_n": float(block.n.median()),
                "effect_class_agreement": float(
                    (valid.effect_class == valid.baseline_effect_class).mean()
                ),
                "bf10_evidence_agreement": float(
                    (valid.bf10_evidence == valid.baseline_bf10_evidence).mean()
                ),
                "Delta_correlation": float(valid.Delta.corr(valid.baseline_Delta)),
                "sign_flips": int(((valid.Delta * valid.baseline_Delta) < 0).sum()),
            }
        )
    return pd.DataFrame(rows)
