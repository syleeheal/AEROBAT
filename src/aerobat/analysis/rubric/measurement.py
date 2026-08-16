"""Measurement diagnostics for the Stage 4 behavioral rubrics."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd
from scipy import stats

from ...storage.artifacts import HYPOTHESIS_GENERATION, iter_hypothesis_dirs
from ...storage.ids import RunId
from ...storage.schema import runtime_artifact
from ...utils import load_json, save_json

EMBEDDING_MODEL = "text-embedding-3-large"
RUN_COLUMNS = [
    "target_behavior",
    "hypothesis_id",
    "domain_slug",
    "group_index",
    "value_index",
    "repetition",
]
RELATION_ORDER = [
    "same evidence class",
    "different class, same behavior",
    "unrelated behavior",
]


@dataclass(frozen=True)
class InternalConsistency:
    """Tabular outputs underlying Appendix E's consistency table and figure."""

    summary: pd.DataFrame
    correlations: pd.DataFrame
    items: pd.DataFrame


@dataclass(frozen=True)
class NullScores:
    """Tabular outputs underlying Appendix E's null-score paragraph and figure."""

    summary: pd.DataFrame
    by_evidence_class: pd.DataFrame
    by_run: pd.DataFrame
    by_level: pd.DataFrame


@dataclass(frozen=True)
class SemanticSpecificity:
    """Pair-level and aggregate outputs from the rubric-criterion embeddings."""

    summary: pd.DataFrame
    pairs: pd.DataFrame
    by_level_distance: pd.DataFrame
    statistics: pd.DataFrame


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    parsed = float(value)
    return parsed if math.isfinite(parsed) else None


def rubric_criteria(results_dir: str | Path) -> pd.DataFrame:
    """Return one row for every scored criterion in every behavior rubric."""
    rows: list[dict[str, Any]] = []
    for path in sorted(Path(results_dir).glob(f"*/{HYPOTHESIS_GENERATION}")):
        payload = runtime_artifact(path.name, load_json(path))
        behavior = str(payload.get("behavior_name") or path.parent.name)
        evidence_class_positions: dict[str, int] = {}
        for level in payload.get("behavior_eval_rubric") or []:
            score = _numeric(level.get("score")) if isinstance(level, Mapping) else None
            if score is None:
                continue
            for evidence_class, criterion in (level.get("evidence") or {}).items():
                evidence_class_positions.setdefault(
                    str(evidence_class), len(evidence_class_positions)
                )
                criterion_id = f"{behavior}|{evidence_class}|{score:g}"
                rows.append(
                    {
                        "criterion_id": criterion_id,
                        "target_behavior": behavior,
                        "evidence_class": str(evidence_class),
                        "evidence_class_position": evidence_class_positions[str(evidence_class)],
                        "level_score": score,
                        "level_label": str(level.get("level") or ""),
                        "criterion_text": str(criterion),
                    }
                )
    frame = pd.DataFrame(rows).sort_values(
        ["target_behavior", "evidence_class_position", "level_score"]
    ).reset_index(drop=True)
    if frame.empty or frame.criterion_id.duplicated().any():
        raise ValueError("Behavior rubrics must contain unique scored criteria")
    return frame


def _evidence_classes_by_behavior(results_dir: str | Path) -> dict[str, list[str]]:
    criteria = rubric_criteria(results_dir)
    return {
        behavior: list(block.evidence_class.drop_duplicates())
        for behavior, block in criteria.groupby("target_behavior", sort=False)
    }


def load_rubric_score_cells(results_dir: str | Path) -> pd.DataFrame:
    """Load the run-by-evidence-class cells scored by the Stage 4 reviewer.

    Only emitted assessment keys count as evaluated score cells; explicit null scores are
    preserved. This matches the Stage 4 output contract and the pipeline's available-case rule.
    """
    root = Path(results_dir)
    classes_by_behavior = _evidence_classes_by_behavior(root)
    rows: list[dict[str, Any]] = []

    for hypothesis_dir in iter_hypothesis_dirs(root):
        behavior = hypothesis_dir.parent.name
        classes = classes_by_behavior[behavior]
        for path in sorted(hypothesis_dir.glob("*/reviews/review_i*_j*_rep*.json")):
            review = runtime_artifact(path.name, load_json(path))
            run = RunId.from_mapping(review)
            evaluation = review.get("behavior_eval") or {}
            assessment = evaluation.get("behavior_assessment") or {}
            if not isinstance(assessment, Mapping) or not assessment:
                # A review without an assessment has no evaluated score cells. It is
                # downstream attrition, not a run whose entire rubric was scored null.
                continue
            unexpected = set(assessment) - set(classes)
            if unexpected:
                raise ValueError(
                    f"{path} contains evidence classes absent from the {behavior!r} rubric: "
                    f"{sorted(unexpected)}"
                )
            for evidence_class in classes:
                if evidence_class not in assessment:
                    continue
                cell = assessment[evidence_class] or {}
                score = _numeric(cell.get("level_score")) if isinstance(cell, Mapping) else None
                rows.append(
                    {
                        "target_behavior": behavior,
                        "hypothesis_id": hypothesis_dir.name,
                        **run.as_dict(),
                        "block_id": f"{behavior}|{hypothesis_dir.name}|{run.group_id}",
                        "level_position": run.level_position,
                        "evidence_class": evidence_class,
                        "score": score,
                        "rationale": str(cell.get("rationale") or "")
                        if isinstance(cell, Mapping)
                        else "",
                    }
                )

    frame = pd.DataFrame(rows)
    identity = RUN_COLUMNS + ["evidence_class"]
    if frame.empty or frame.duplicated(identity).any():
        raise ValueError("Stage 4 rubric cells must be non-empty and unique by run and class")
    return frame.sort_values(identity).reset_index(drop=True)


def score_matrix(cells: pd.DataFrame, target_behavior: str) -> pd.DataFrame:
    """Return reviewed runs by evidence classes, preserving null scores."""
    subset = cells[cells.target_behavior == target_behavior]
    return subset.pivot(index=RUN_COLUMNS, columns="evidence_class", values="score")


def _mean_off_diagonal(correlation: pd.DataFrame) -> float:
    if correlation.shape[0] < 2:
        return math.nan
    values = correlation.to_numpy(dtype=float)
    return float(np.nanmean(values[np.triu_indices(len(values), 1)]))


def _standardized_alpha(correlation: pd.DataFrame) -> float:
    item_count = correlation.shape[0]
    mean_correlation = _mean_off_diagonal(correlation)
    denominator = 1 + (item_count - 1) * mean_correlation
    if item_count < 2 or not math.isfinite(mean_correlation) or denominator == 0:
        return math.nan
    return item_count * mean_correlation / denominator


def _first_eigenvalue_share(correlation: pd.DataFrame) -> float:
    fill = _mean_off_diagonal(correlation)
    matrix = correlation.to_numpy(dtype=float, copy=True)
    matrix[~np.isfinite(matrix)] = fill if math.isfinite(fill) else 0.0
    np.fill_diagonal(matrix, 1.0)
    matrix = (matrix + matrix.T) / 2
    return float(np.linalg.eigvalsh(matrix).max() / len(matrix))


def _residualized_scores(
    cells: pd.DataFrame,
    target_behavior: str,
    wide: pd.DataFrame,
    *,
    minimum_pairs: int,
) -> pd.DataFrame:
    subset = cells[cells.target_behavior == target_behavior]
    design = subset.drop_duplicates(RUN_COLUMNS).set_index(RUN_COLUMNS).reindex(wide.index)
    level_id = (
        design.index.get_level_values("hypothesis_id").astype(str)
        + "@"
        + design.index.get_level_values("value_index").astype(str)
    )
    matrix = pd.get_dummies(
        pd.DataFrame({"block": design.block_id.values, "level": level_id.values}),
        dtype=float,
    ).to_numpy()

    residuals = pd.DataFrame(np.nan, index=wide.index, columns=wide.columns)
    for evidence_class in wide:
        values = wide[evidence_class].to_numpy(dtype=float)
        keep = np.isfinite(values)
        if int(keep.sum()) < minimum_pairs:
            continue
        coefficients, *_ = np.linalg.lstsq(matrix[keep], values[keep], rcond=None)
        residuals.loc[keep, evidence_class] = values[keep] - matrix[keep] @ coefficients
    return residuals


def internal_consistency(
    cells: pd.DataFrame,
    *,
    minimum_pairs: int = 20,
) -> InternalConsistency:
    """Compute the raw and design-residualized rubric diagnostics from Appendix E."""
    summaries: list[dict[str, Any]] = []
    correlation_rows: list[dict[str, Any]] = []
    item_rows: list[dict[str, Any]] = []

    for behavior in sorted(cells.target_behavior.unique()):
        wide = score_matrix(cells, behavior)
        residuals = _residualized_scores(
            cells, behavior, wide, minimum_pairs=minimum_pairs
        )
        raw = wide.corr(method="spearman", min_periods=minimum_pairs)
        residual = residuals.corr(method="spearman", min_periods=minimum_pairs)
        alpha = _standardized_alpha(raw)

        for left in wide.columns:
            item_total = wide[left].corr(
                wide.drop(columns=left).mean(axis=1, skipna=True), method="spearman"
            )
            alpha_without = _standardized_alpha(raw.drop(index=left, columns=left))
            item_rows.append(
                {
                    "target_behavior": behavior,
                    "evidence_class": left,
                    "corrected_item_total_spearman": item_total,
                    "alpha_if_item_deleted": alpha_without,
                    "alpha_change_if_item_deleted": alpha_without - alpha,
                    "floor_rate": float((wide[left].dropna() == 0).mean()),
                    "null_rate": float(wide[left].isna().mean()),
                }
            )
            for right in wide.columns:
                correlation_rows.append(
                    {
                        "target_behavior": behavior,
                        "evidence_class_left": left,
                        "evidence_class_right": right,
                        "raw_spearman": raw.loc[left, right],
                        "residualized_spearman": residual.loc[left, right],
                    }
                )

        behavior_items = [row for row in item_rows if row["target_behavior"] == behavior]
        summaries.append(
            {
                "target_behavior": behavior,
                "evidence_classes": wide.shape[1],
                "reviewed_runs": int(wide.notna().any(axis=1).sum()),
                "mean_interclass_spearman": _mean_off_diagonal(raw),
                "residualized_mean_interclass_spearman": _mean_off_diagonal(residual),
                "cronbach_alpha": alpha,
                "first_eigenvalue_share": _first_eigenvalue_share(raw),
                "minimum_corrected_item_total_spearman": float(
                    np.nanmin(
                        [row["corrected_item_total_spearman"] for row in behavior_items]
                    )
                ),
                "maximum_alpha_gain_if_item_deleted": float(
                    np.nanmax([row["alpha_change_if_item_deleted"] for row in behavior_items])
                ),
                "floor_rate": float(
                    np.mean([row["floor_rate"] for row in behavior_items])
                ),
                "null_rate": float(cells.loc[cells.target_behavior == behavior, "score"].isna().mean()),
            }
        )

    return InternalConsistency(
        summary=pd.DataFrame(summaries),
        correlations=pd.DataFrame(correlation_rows),
        items=pd.DataFrame(item_rows),
    )


def null_scores(cells: pd.DataFrame) -> NullScores:
    """Summarize null evidence-class scores without changing their interpretation."""
    by_class = (
        cells.groupby(["target_behavior", "evidence_class"], as_index=False)
        .score.agg(cells="size", null_scores=lambda values: int(values.isna().sum()))
    )
    by_class["null_rate"] = by_class.null_scores / by_class.cells

    by_run = (
        cells.groupby(RUN_COLUMNS, as_index=False)
        .agg(
            evidence_classes=("score", "size"),
            null_scores=("score", lambda values: int(values.isna().sum())),
            level_position=("level_position", "first"),
        )
    )
    by_run["null_rate"] = by_run.null_scores / by_run.evidence_classes
    by_run["all_classes_scored"] = by_run.null_scores == 0
    by_level = (
        by_run.groupby("level_position", as_index=False)
        .agg(reviewed_runs=("null_rate", "size"), mean_null_rate=("null_rate", "mean"))
    )
    worst = by_class.loc[by_class.null_rate.idxmax()]
    summary = pd.DataFrame(
        [
            {
                "evaluated_score_cells": len(cells),
                "null_score_cells": int(cells.score.isna().sum()),
                "null_rate": float(cells.score.isna().mean()),
                "reviewed_runs": len(by_run),
                "complete_run_rate": float(by_run.all_classes_scored.mean()),
                "half_or_more_null_rate": float((by_run.null_rate >= 0.5).mean()),
                "all_null_runs": int((by_run.null_rate == 1).sum()),
                "most_null_target_behavior": worst.target_behavior,
                "most_null_evidence_class": worst.evidence_class,
                "most_null_class_rate": float(worst.null_rate),
            }
        ]
    )
    return NullScores(summary, by_class, by_run, by_level)


def criteria_checksum(criteria: pd.DataFrame) -> str:
    """Stable checksum of the criterion identity and text sent for embedding."""
    records = criteria[
        ["criterion_id", "target_behavior", "evidence_class", "level_score", "criterion_text"]
    ].to_dict("records")
    encoded = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def generate_embedding_cache(
    criteria: pd.DataFrame,
    output_path: str | Path,
    *,
    model: str = EMBEDDING_MODEL,
    batch_size: int = 128,
) -> dict[str, Any]:
    """Embed rubric criteria once and save a versioned, checksummed cache.

    This is the only function in the Appendix E path that makes model calls. Statistical
    summaries and figures consume the saved cache and never issue calls implicitly.
    """
    from litellm import embedding

    records = criteria.to_dict("records")
    response_ids: list[str] = []
    vectors: list[list[float]] = []
    for start in range(0, len(records), batch_size):
        batch = records[start : start + batch_size]
        response = embedding(model=model, input=[row["criterion_text"] for row in batch])
        response_ids.append(str(getattr(response, "id", "") or ""))
        data = sorted(response.data, key=lambda item: item["index"])
        vectors.extend([list(item["embedding"]) for item in data])

    payload = {
        "schema_version": 1,
        "model": model,
        "criteria_checksum": criteria_checksum(criteria),
        "response_ids": response_ids,
        "criteria": [
            {**record, "embedding": vector}
            for record, vector in zip(records, vectors, strict=True)
        ],
    }
    save_json(payload, output_path)
    return payload


def load_embedding_cache(
    path: str | Path,
    criteria: pd.DataFrame,
    *,
    model: str = EMBEDDING_MODEL,
) -> dict[str, Any]:
    """Load an embedding cache and reject stale criteria or the wrong model."""
    payload = load_json(path)
    if payload.get("schema_version") != 1:
        raise ValueError("Unsupported rubric embedding-cache schema")
    if payload.get("model") != model:
        raise ValueError(f"Expected embedding model {model!r}, got {payload.get('model')!r}")
    if payload.get("criteria_checksum") != criteria_checksum(criteria):
        raise ValueError("Rubric embedding cache does not match the current criterion text")
    cached_ids = [row.get("criterion_id") for row in payload.get("criteria") or []]
    if cached_ids != criteria.criterion_id.tolist():
        raise ValueError("Rubric embedding cache has missing or reordered criteria")
    return payload


def semantic_specificity(
    criteria: pd.DataFrame,
    embedding_cache: Mapping[str, Any],
) -> SemanticSpecificity:
    """Compute the semantic-specificity comparisons reported in Appendix E."""
    cached = pd.DataFrame(embedding_cache.get("criteria") or [])
    if cached.criterion_id.tolist() != criteria.criterion_id.tolist():
        raise ValueError("Embedding rows do not align with the supplied rubric criteria")
    vectors = np.asarray(cached.embedding.tolist(), dtype=float)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    if vectors.ndim != 2 or np.any(norms == 0):
        raise ValueError("Rubric embeddings must be a non-zero numeric matrix")
    similarities = (vectors / norms) @ (vectors / norms).T

    rows: list[dict[str, Any]] = []
    for left_index, right_index in combinations(range(len(criteria)), 2):
        left, right = criteria.iloc[left_index], criteria.iloc[right_index]
        same_behavior = left.target_behavior == right.target_behavior
        same_class = same_behavior and left.evidence_class == right.evidence_class
        relation = (
            "same evidence class"
            if same_class
            else "different class, same behavior"
            if same_behavior
            else "unrelated behavior"
        )
        rows.append(
            {
                "criterion_id_left": left.criterion_id,
                "criterion_id_right": right.criterion_id,
                "target_behavior_left": left.target_behavior,
                "target_behavior_right": right.target_behavior,
                "evidence_class_left": left.evidence_class,
                "evidence_class_right": right.evidence_class,
                "level_score_left": left.level_score,
                "level_score_right": right.level_score,
                "relation": relation,
                "level_distance": abs(left.level_score - right.level_score),
                "cosine_similarity": float(similarities[left_index, right_index]),
            }
        )
    pairs = pd.DataFrame(rows)
    summary = (
        pairs.groupby("relation", as_index=False)
        .agg(mean_cosine_similarity=("cosine_similarity", "mean"), pairs=("relation", "size"))
        .set_index("relation")
        .reindex(RELATION_ORDER)
        .reset_index()
    )
    same_class = pairs[pairs.relation == "same evidence class"]
    by_distance = (
        same_class.groupby("level_distance", as_index=False)
        .agg(mean_cosine_similarity=("cosine_similarity", "mean"), pairs=("relation", "size"))
    )
    gradient = (
        stats.spearmanr(same_class.level_distance, same_class.cosine_similarity)
        if same_class.level_distance.nunique() > 1
        else None
    )
    statistics = pd.DataFrame(
        [
            {
                "model": embedding_cache.get("model"),
                "criteria_checksum": embedding_cache.get("criteria_checksum"),
                "level_distance_spearman": (
                    float(gradient.statistic) if gradient is not None else math.nan
                ),
                "level_distance_p_value": (
                    float(gradient.pvalue) if gradient is not None else math.nan
                ),
            }
        ]
    )
    return SemanticSpecificity(summary, pairs, by_distance, statistics)
