"""Tables and figures for the Appendix E rubric audit."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ...utils import save_json
from ..paper import AXIS, DIVERGING, GRID, INK, INK2, MUTED, NEG, POS, SURFACE, save_figure
from .measurement import InternalConsistency, NullScores, SemanticSpecificity
from .robustness import sensitivity_summary


def _label(value: str, width: int = 22) -> str:
    text = str(value).replace("_", " ")
    return text if len(text) <= width else text[: width - 1] + "…"


def _cell_number(value: float) -> str:
    return f"{value:.2f}".replace("0.", ".").replace("-0.", "-.")


def plot_internal_consistency(
    diagnostics: InternalConsistency,
    output_stem: str | Path | None = None,
) -> plt.Figure:
    """Plot raw correlations above and residualized correlations below the diagonal."""
    behaviors = sorted(diagnostics.summary.target_behavior)
    figure, axes = plt.subplots(3, 4, figsize=(13.0, 8.4))
    summary = diagnostics.summary.set_index("target_behavior")
    for axis, behavior in zip(axes.ravel(), behaviors):
        block = diagnostics.correlations[
            diagnostics.correlations.target_behavior == behavior
        ]
        raw = block.pivot(
            index="evidence_class_left", columns="evidence_class_right", values="raw_spearman"
        )
        residual = block.pivot(
            index="evidence_class_left",
            columns="evidence_class_right",
            values="residualized_spearman",
        ).reindex(index=raw.index, columns=raw.columns)
        matrix = raw.to_numpy(copy=True)
        matrix[np.tril_indices(len(matrix), -1)] = residual.to_numpy()[
            np.tril_indices(len(matrix), -1)
        ]
        k = len(raw)
        display_matrix = matrix.copy()
        np.fill_diagonal(display_matrix, np.nan)
        cmap = DIVERGING.copy()
        cmap.set_bad(SURFACE)
        axis.imshow(display_matrix, cmap=cmap, vmin=-1, vmax=1, aspect="equal")
        for row in range(k):
            for column in range(k):
                if row == column:
                    axis.text(
                        column, row, f"{row + 1}",
                        ha="center", va="center", fontsize=7.5, color=INK2,
                    )
                    continue
                value = matrix[row, column]
                if not np.isfinite(value):
                    axis.text(
                        column, row, "--",
                        ha="center", va="center", fontsize=6.6, color=INK2,
                    )
                    continue
                axis.text(
                    column, row, _cell_number(value),
                    ha="center", va="center", fontsize=6.6,
                    color=INK if abs(value) < 0.62 else SURFACE,
                )

        labels = [f"{index + 1}. {_label(item, 18)}" for index, item in enumerate(raw.columns)]
        axis.set_xticks(range(k))
        axis.set_xticklabels(range(1, k + 1), fontsize=7)
        axis.set_yticks(range(k))
        axis.set_yticklabels(labels, fontsize=6.4)
        row = summary.loc[behavior]
        axis.set_title(
            f"{behavior}\n"
            + r"$\bar r$ = "
            + f"{row.mean_interclass_spearman:.2f} / {row.residualized_mean_interclass_spearman:.2f}"
            + r"   $\alpha$ = "
            + f"{row.cronbach_alpha:.2f}",
            fontsize=8.6, color=INK, fontweight="bold", pad=5,
        )
        axis.tick_params(length=0)
        for spine in axis.spines.values():
            spine.set_visible(False)
        axis.set_xticks(np.arange(-0.5, k, 1), minor=True)
        axis.set_yticks(np.arange(-0.5, k, 1), minor=True)
        axis.grid(which="minor", color=SURFACE, linewidth=2)
        axis.tick_params(which="minor", length=0)
    for axis in axes.ravel()[len(behaviors) :]:
        axis.set_visible(False)
    figure.tight_layout(h_pad=1.2, w_pad=3.2, rect=(0, 0.05, 1, 1))
    scale = figure.add_axes([0.33, 0.014, 0.34, 0.011])
    figure.colorbar(
        plt.cm.ScalarMappable(cmap=DIVERGING, norm=plt.Normalize(-1, 1)),
        cax=scale,
        orientation="horizontal",
    )
    scale.set_xlabel(
        "Spearman correlation between evidence classes\n"
        "upper triangle: raw    lower triangle: block- and level-residualized",
        fontsize=8,
        color=INK,
        labelpad=3,
    )
    scale.tick_params(labelsize=7, color=AXIS, labelcolor=INK2, length=2)
    if output_stem is not None:
        save_figure(figure, output_stem)
    return figure


def plot_semantic_specificity(
    diagnostics: SemanticSpecificity,
    output_stem: str | Path | None = None,
) -> plt.Figure:
    """Plot criterion distinctiveness and level separation."""
    figure, axes = plt.subplots(1, 2, figsize=(9.0, 3.9), constrained_layout=True)
    pairs = diagnostics.pairs.copy()
    same_behavior = pairs.target_behavior_left == pairs.target_behavior_right
    same_class = same_behavior & (pairs.evidence_class_left == pairs.evidence_class_right)
    same_level = same_behavior & (pairs.level_score_left == pairs.level_score_right)
    pairs["original_relation"] = np.select(
        [
            same_class,
            same_level,
            same_behavior,
        ],
        [
            "same class, different level",
            "different class, same level",
            "different class, different level",
        ],
        default="cross-behavior",
    )

    axis = axes[0]
    relations = [
        "same class,\ndifferent level",
        "different class,\nsame level",
        "different class,\ndifferent level",
        "cross-behavior",
    ]
    keys = [
        "same class, different level",
        "different class, same level",
        "different class, different level",
        "cross-behavior",
    ]
    positions = np.arange(len(keys))
    means = [
        pairs.loc[pairs.original_relation == key, "cosine_similarity"].mean()
        for key in keys
    ]
    axis.barh(
        positions, means, height=0.56, color=NEG,
        edgecolor=SURFACE, linewidth=2, zorder=3,
    )
    for y, value in zip(positions, means):
        axis.text(value + 0.006, y, f"{value:.2f}", va="center", fontsize=7.2, color=INK2)
    axis.set_yticks(positions)
    axis.set_yticklabels(relations, fontsize=7.6)
    axis.invert_yaxis()
    axis.set_xlabel("mean embedding cosine between anchor cells")
    axis.set_title("Distinctiveness", fontsize=9.5, color=INK, fontweight="bold")
    axis.grid(axis="x", zorder=0)
    axis.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        axis.spines[spine].set_visible(False)

    axis = axes[1]
    distance = diagnostics.by_level_distance
    axis.plot(
        distance.level_distance,
        distance.mean_cosine_similarity,
        marker="o",
        markersize=6,
        linewidth=2,
        color=NEG,
        markeredgecolor=SURFACE,
        markeredgewidth=1.2,
        zorder=3,
    )
    floor = pairs.loc[pairs.original_relation == "cross-behavior", "cosine_similarity"].mean()
    axis.axhline(floor, color=MUTED, linewidth=1, linestyle=(0, (4, 3)), zorder=2)
    axis.text(
        float(distance.level_distance.max()) - 0.1,
        floor + 0.006,
        "unrelated-behavior floor",
        ha="right",
        fontsize=7,
        color=MUTED,
    )
    rho = float(diagnostics.statistics.level_distance_spearman.iloc[0])
    p_value = float(diagnostics.statistics.level_distance_p_value.iloc[0])
    axis.set_xlabel(r"level distance  |$j$ $-$ $j'$|")
    axis.set_ylabel("cosine similarity")
    axis.set_xticks(distance.level_distance)
    axis.set_title(
        "Level separation within a class\n"
        + r"$\rho$ = "
        + f"{rho:+.2f}, p = {p_value:.2f}",
        fontsize=9.5,
        color=INK,
        fontweight="bold",
    )
    axis.grid(axis="y", zorder=0)
    axis.set_axisbelow(True)
    for spine in ("top", "right"):
        axis.spines[spine].set_visible(False)
    if output_stem is not None:
        save_figure(figure, output_stem)
    return figure


def plot_null_scores(
    diagnostics: NullScores,
    output_stem: str | Path | None = None,
) -> plt.Figure:
    """Plot concentration of null scores by evidence class."""
    by_class = diagnostics.by_evidence_class
    behaviors = sorted(by_class.target_behavior.unique())
    width = int(by_class.groupby("target_behavior").size().max())
    grid = np.full((len(behaviors), width), np.nan)
    for row, behavior in enumerate(behaviors):
        rates = by_class.loc[by_class.target_behavior == behavior, "null_rate"].sort_values(ascending=False)
        grid[row, : len(rates)] = rates

    figure, axis = plt.subplots(1, 1, figsize=(6.2, 4.2), constrained_layout=True)
    image = axis.imshow(grid, cmap="Blues", vmin=0, vmax=float(np.nanmax(grid)), aspect="auto")
    for row, column in zip(*np.where(np.isfinite(grid))):
        axis.text(
            column, row, _cell_number(grid[row, column]),
            ha="center", va="center", fontsize=6.8,
            color=INK if grid[row, column] < 0.55 * np.nanmax(grid) else SURFACE,
        )
    axis.set_yticks(range(len(behaviors)))
    axis.set_yticklabels([_label(value, 24) for value in behaviors], fontsize=7.4)
    axis.set_xticks(range(width))
    axis.set_xticklabels([f"{index + 1}" for index in range(width)], fontsize=7.4)
    axis.set_xlabel("evidence classes, ordered by null rate within the behavior")
    axis.set_title("Null rate per evidence class", fontsize=9.5, color=INK, fontweight="bold")
    axis.tick_params(length=0)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.set_xticks(np.arange(-0.5, width, 1), minor=True)
    axis.set_yticks(np.arange(-0.5, len(behaviors), 1), minor=True)
    axis.grid(which="minor", color=SURFACE, linewidth=2)
    axis.tick_params(which="minor", length=0)
    colorbar = figure.colorbar(image, ax=axis, fraction=0.035, pad=0.02)
    colorbar.set_label("Null rate", fontsize=8, color=INK)
    colorbar.ax.tick_params(labelsize=7, color=AXIS, labelcolor=INK2, length=2)
    if output_stem is not None:
        save_figure(figure, output_stem)
    return figure


def plot_rubric_sensitivity(
    frame: pd.DataFrame,
    output_stem: str | Path | None = None,
) -> plt.Figure:
    """Compare alternative composites with the available-case effect estimate."""
    panels = [
        ("null_as_zero", "nulls read as level 0"),
        ("complete_case", "runs with any null dropped"),
        ("drop_most_null_class", "most-null class removed"),
        ("leave_one_out", "any one class removed"),
    ]
    figure, axes = plt.subplots(1, 4, figsize=(13.4, 3.6), sharex=True, sharey=True, constrained_layout=True)
    limit = 1.06 * float(
        np.nanmax(np.abs(pd.concat([frame.Delta, frame.baseline_Delta]).to_numpy()))
    )
    for axis, (family, title) in zip(axes, panels):
        block = frame[frame.variant_family == family].dropna(
            subset=["Delta", "baseline_Delta"]
        )
        changed = block.bf10_evidence != block.baseline_bf10_evidence
        axis.plot(
            [-limit, limit], [-limit, limit],
            color=AXIS, linewidth=0.9, linestyle=(0, (4, 3)), zorder=1,
        )
        axis.axhline(0, color=GRID, linewidth=0.7, zorder=0)
        axis.axvline(0, color=GRID, linewidth=0.7, zorder=0)
        axis.scatter(
            block.loc[~changed, "baseline_Delta"],
            block.loc[~changed, "Delta"],
            facecolor=NEG,
            edgecolor=SURFACE,
            linewidth=0.7,
            s=20,
            zorder=3,
        )
        axis.scatter(
            block.loc[changed, "baseline_Delta"],
            block.loc[changed, "Delta"],
            marker="D",
            facecolor=SURFACE,
            edgecolor=POS,
            linewidth=1.4,
            s=42,
            zorder=4,
        )
        correlation = block.Delta.corr(block.baseline_Delta)
        changes = int(changed.sum())
        axis.set_title(
            f"{title}\n"
            + f"r = {correlation:.3f},  {changes} decision change"
            + ("s" if changes != 1 else ""),
            fontsize=9,
            color=INK,
            fontweight="bold",
        )
        axis.set(xlim=(-limit, limit), ylim=(-limit, limit), xlabel=r"effect size $\Delta$ (original)")
        axis.grid(zorder=0)
        axis.set_axisbelow(True)
        axis.set_aspect("equal")
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel(r"effect size $\Delta$ (variant)")
    if output_stem is not None:
        save_figure(figure, output_stem)
    return figure


def write_appendix_e_outputs(
    output_dir: str | Path,
    *,
    score_cells: pd.DataFrame,
    criteria: pd.DataFrame,
    consistency: InternalConsistency,
    nulls: NullScores,
    semantics: SemanticSpecificity,
    sensitivity: pd.DataFrame,
) -> None:
    """Write every machine-readable intermediate and Appendix E figure."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    score_cells.drop(columns="rationale").to_csv(output / "rubric_score_cells.csv", index=False)
    criteria.to_csv(output / "rubric_criteria.csv", index=False)
    consistency.summary.to_csv(output / "rubric_consistency.csv", index=False)
    consistency.correlations.to_csv(output / "rubric_correlations.csv", index=False)
    consistency.items.to_csv(output / "rubric_item_diagnostics.csv", index=False)
    nulls.summary.to_csv(output / "rubric_null_summary.csv", index=False)
    nulls.by_evidence_class.to_csv(output / "rubric_null_by_evidence_class.csv", index=False)
    nulls.by_run.to_csv(output / "rubric_null_by_run.csv", index=False)
    nulls.by_level.to_csv(output / "rubric_null_by_level.csv", index=False)
    semantics.summary.to_csv(output / "rubric_semantic_summary.csv", index=False)
    semantics.pairs.to_csv(output / "rubric_semantic_pairs.csv", index=False)
    semantics.by_level_distance.to_csv(output / "rubric_semantic_by_level_distance.csv", index=False)
    semantics.statistics.to_csv(output / "rubric_semantic_statistics.csv", index=False)
    sensitivity.to_csv(output / "rubric_sensitivity.csv", index=False)
    sensitivity_table = sensitivity_summary(sensitivity)
    sensitivity_table.to_csv(output / "rubric_sensitivity_summary.csv", index=False)

    measurement = consistency.summary
    numbers = {
        "schema_version": 1,
        "internal_consistency": {
            "mean_interclass_spearman": float(measurement.mean_interclass_spearman.mean()),
            "residualized_mean_interclass_spearman": float(
                measurement.residualized_mean_interclass_spearman.mean()
            ),
            "mean_cronbach_alpha": float(measurement.cronbach_alpha.mean()),
            "minimum_cronbach_alpha": float(measurement.cronbach_alpha.min()),
            "mean_first_eigenvalue_share": float(measurement.first_eigenvalue_share.mean()),
            "minimum_corrected_item_total_spearman": float(
                measurement.minimum_corrected_item_total_spearman.min()
            ),
            "maximum_alpha_gain_if_item_deleted": float(
                measurement.maximum_alpha_gain_if_item_deleted.max()
            ),
        },
        "semantic_specificity": {
            "model": semantics.statistics.model.iloc[0],
            "criteria_checksum": semantics.statistics.criteria_checksum.iloc[0],
            "relationship_means": dict(
                zip(semantics.summary.relation, semantics.summary.mean_cosine_similarity)
            ),
            "level_distance_means": dict(
                zip(
                    semantics.by_level_distance.level_distance.astype(str),
                    semantics.by_level_distance.mean_cosine_similarity,
                )
            ),
            "level_distance_spearman": float(
                semantics.statistics.level_distance_spearman.iloc[0]
            ),
            "level_distance_p_value": float(
                semantics.statistics.level_distance_p_value.iloc[0]
            ),
        },
        "null_scores": nulls.summary.iloc[0].to_dict(),
        "sensitivity": sensitivity_table.to_dict("records"),
    }
    save_json(numbers, output / "appendix_e_numbers.json")

    figures = [
        plot_internal_consistency(consistency, output / "figE1_rubric_consistency"),
        plot_semantic_specificity(semantics, output / "figE2_rubric_semantics"),
        plot_null_scores(nulls, output / "figE3_rubric_null"),
        plot_rubric_sensitivity(sensitivity, output / "figE4_rubric_sensitivity"),
    ]
    for figure in figures:
        plt.close(figure)
