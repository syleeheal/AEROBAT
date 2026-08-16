"""Shared formatting, numeric, and filtering helpers for analysis modules."""

from __future__ import annotations

import math
from collections import defaultdict
from statistics import mean
from typing import Any, Dict, List, Mapping, Sequence

from aerobat.protocol.constants import (
    ANALYSIS_INCLUDED_VALIDITY_RATINGS,
    OVERALL_VALIDITY_SCALE,
)
from aerobat.protocol.payloads import PayloadManager


def _fmt_idx(value: Any) -> str:
    return f"{value:.2f}" if isinstance(value, (int, float)) else "NA"


def _fmt_bf(value: Any) -> str:
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return "NA"
    if value != 0 and (abs(value) > 1000 or abs(value) < 0.01):
        return f"{value:.2e}"
    return f"{value:.2f}"


def _coerce_float(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        text = str(value).strip()
        if not text:
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def _round_3(value: Any) -> float | None:
    parsed = _coerce_float(value)
    return round(parsed, 3) if parsed is not None and math.isfinite(parsed) else None


def _one_hot(
    values: Sequence[Any],
    *,
    drop_first: bool = True,
) -> tuple[List[Any], List[List[float]]]:
    levels = sorted(
        set(values),
        key=lambda value: (value if isinstance(value, (int, float)) else str(value)),
    )
    encoded_levels = levels[1:] if drop_first else levels
    rows = [[1.0 if value == level else 0.0 for level in encoded_levels] for value in values]
    return encoded_levels, rows


def _fidelity_gate_ratings_by_run(
    review: Mapping[str, Any],
) -> Dict[tuple[Any, str], str]:
    if review.get("research_manager_enabled") is False:
        return {}
    fidelity_rating_by_run: Dict[tuple[Any, str], str] = {}
    for entry in review.get("simulations", []):
        if not isinstance(entry, Mapping):
            continue
        rm_review = entry.get("research_manager_review") or {}
        if not isinstance(rm_review, Mapping):
            continue
        rating = (rm_review.get("overall_validity") or {}).get("rating")
        if not isinstance(rating, str) or rating not in OVERALL_VALIDITY_SCALE:
            continue
        fidelity_rating_by_run[(entry.get("repetition"), str(entry.get("simulation_id")))] = rating
    return fidelity_rating_by_run


def _fidelity_gate_rating(
    entry: Mapping[str, Any],
    fidelity_rating_by_run: Mapping[tuple[Any, str], str],
) -> str | None:
    return fidelity_rating_by_run.get(
        (entry.get("repetition"), str(entry.get("simulation_id")))
    )


def _include_in_analysis(
    entry: Mapping[str, Any],
    fidelity_rating_by_run: Mapping[tuple[Any, str], str],
) -> bool:
    rating = _fidelity_gate_rating(entry, fidelity_rating_by_run)
    return rating is None or rating in ANALYSIS_INCLUDED_VALIDITY_RATINGS


def _behavior_eval_stats(entry: Mapping[str, Any]) -> Dict[str, Any]:
    behavior_eval = entry.get("behavior_eval")
    if not isinstance(behavior_eval, Mapping):
        return PayloadManager.empty_behavior_stats(total_rounds=0)
    return PayloadManager.behavior_stats(behavior_eval, total_rounds=0)


def _rows_by_hypothesis(rows: Sequence[Mapping[str, Any]]) -> Dict[str, List[Mapping[str, Any]]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["axis_slug"])].append(row)
    return grouped


def _rows_by_block(rows: Sequence[Mapping[str, Any]]) -> Dict[str, List[Mapping[str, Any]]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["group_id"])].append(row)
    return grouped


def _mean_score_per_condition(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    scores_by_condition: Dict[tuple[Any, Any], List[float]] = defaultdict(list)
    for row in rows:
        score = _coerce_float(row.get("behavior_eval_mean_score"))
        if score is None:
            continue
        scores_by_condition[(row.get("causal_rank"), row.get("causal_value"))].append(score)

    return [
        {
            "condition": condition,
            "raw_scores": scores,
            "avg_score": _round_3(mean(scores)),
            "var_score": _round_3(
                sum((score - mean(scores)) ** 2 for score in scores) / len(scores)
            ),
        }
        for (_, condition), scores in sorted(
            scores_by_condition.items(),
            key=lambda item: (
                item[0][0] if isinstance(item[0][0], (int, float)) else 10**9,
                str(item[0][1]),
            ),
        )
    ]
