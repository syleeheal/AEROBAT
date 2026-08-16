"""Reproducible tables, figures, and manuscript-number registry.

Notebook cells call these functions; all data transformations live here so the
camera-ready notebooks remain short and auditable.
"""

from __future__ import annotations

import math
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from ..storage.artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    MATCHED_SIMULATION_RUNS,
    STATISTICAL_ANALYSIS,
    iter_hypothesis_dirs,
)
from ..storage.schema import runtime_artifact
from ..utils import load_json, save_json
from .accounting import (
    experiment_stage_accounting,
    stage_accounting,
    stage_accounting_numbers,
)
from .costs import appendix_cost_analysis, manuscript_cost_value
from .results import load_behavioral_findings

BF_EFFECT_THRESHOLD = 3.0
P_TAU_THRESHOLD = 0.05
CONFIGURATION_COMPONENT_ORDER = ["objective", "authority", "constraints", "situational context", "resource", "actor", "risk & return"]
POS, NEG, MID = "#E34948", "#2A78D6", "#F0EFEC"
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0B0B0B", "#52514E", "#898781", "#E1E0D9", "#C3C2B7", "#FFFFFF"
EFFECT_COLORS = {"positive": POS, "negative": NEG, "no_effect": MUTED, "inconclusive": MUTED, "direction_unresolved": MUTED}
EFFECT_CLASS_LABELS = {
    "positive": "Positive",
    "negative": "Negative",
    "no_effect": "No effect",
    "inconclusive": "Inconclusive",
    "direction_unresolved": "Inconclusive",
}
DIVERGING = LinearSegmentedColormap.from_list("aerobat_div", [NEG, MID, POS])


def _marker(effect_class: str, size: float = 26) -> dict[str, Any]:
    marker = "^" if effect_class == "positive" else "v" if effect_class == "negative" else "o"
    filled = effect_class in {"positive", "negative", "no_effect"}
    color = EFFECT_COLORS.get(effect_class, MUTED)
    return {"marker": marker, "s": size, "facecolor": color if filled else SURFACE, "edgecolor": color, "linewidth": 0.9}


def hypothesis_metrics(results_dir: str | Path) -> pd.DataFrame:
    """Extend the tidy results frame with the design counts used in the paper."""
    frame = load_behavioral_findings(results_dir)
    extras = []
    for row in frame.itertuples():
        hypothesis_dir = Path(row.hypothesis_dir)
        meta_path = hypothesis_dir / MATCHED_SIMULATION_RUNS
        config_path = hypothesis_dir / MATCHED_CONFIGURATIONS
        analysis_path = hypothesis_dir / STATISTICAL_ANALYSIS
        meta = runtime_artifact(meta_path.name, load_json(meta_path))
        config = runtime_artifact(config_path.name, load_json(config_path))
        runs = [item for item in meta.get("runs", []) if isinstance(item, Mapping)]
        n_designed = sum(
            len(group.get("manipulated_config", {}))
            for domain in config.get("domain_results", [])
            for group in (domain.get("pass_three") or {}).values()
            if isinstance(group, Mapping)
        )
        groups = {(item.get("domain_slug"), item.get("group_index")) for item in runs}
        extras.append({
            "hypothesis_dir": hypothesis_dir,
            "D_h": len({item.get("domain_slug") for item in runs}),
            "I_per_domain": (config.get("meta_data") or {}).get("num_value_sets"),
            "B": len(groups),
            "J": len({item.get("value_index") for item in runs}),
            "T": meta.get("num_rounds"),
            "n_designed": n_designed,
            "n_run": len(runs),
            "Z_per_domain": np.mean([len(domain.get("pass_one", {})) for domain in config.get("domain_results", [])]),
            "n_outcomes": len((runtime_artifact(analysis_path.name, load_json(analysis_path)).get("quantitative_analysis") or {})) - 2,
        })
    extra = pd.DataFrame(extras)
    merged = pd.concat([frame.reset_index(drop=True), extra.drop(columns=["hypothesis_dir"])], axis=1)
    accounting = stage_accounting(results_dir).rename(
        columns={"target_behavior": "behavior_name", "hypothesis_id": "axis_slug"}
    )
    return merged.merge(accounting, on=["behavior_name", "axis_slug"], validate="one_to_one")


def stage1_metrics(results_dir: str | Path) -> pd.DataFrame:
    rows = []
    for path in sorted(Path(results_dir).glob(f"*/{HYPOTHESIS_GENERATION}")):
        payload = runtime_artifact(path.name, load_json(path))
        meta = payload.get("meta_data") or {}
        hypotheses = payload.get("hypotheses") or []
        rows.append({
            "behavior_name": payload.get("behavior_name", path.parent.name),
            "H_configured": meta.get("num_hypotheses"),
            "H_generated": len(hypotheses),
            "num_selected_hypotheses": meta.get("num_stage2_hypotheses"),
            "passes_stage2": sum(bool((item.get("research_manager_review") or {}).get("passes_stage2")) for item in hypotheses),
        })
    return pd.DataFrame(rows)


def behavioral_finding_numbers(results_dir: str | Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Recompute the principal Sec. 4.1 quantities."""
    frame = hypothesis_metrics(results_dir)
    stage1 = stage1_metrics(results_dir)
    evidence = frame.dropna(subset=["bf10", "p_tau"])
    significant = evidence[evidence.bf10 >= BF_EFFECT_THRESHOLD]
    spearman = stats.spearmanr(evidence.bf10, evidence.p_tau)
    tested_per_behavior = frame.groupby("behavior_name").size()
    accounting = stage_accounting_numbers(frame)
    numbers = {
        "n_behaviors": int(frame.behavior_name.nunique()),
        "H_configured": sorted(stage1.H_configured.dropna().unique().tolist()),
        "H_generated_range": [int(stage1.H_generated.min()), int(stage1.H_generated.max())],
        "selected_hypotheses_tested_range": [
            int(tested_per_behavior.min()),
            int(tested_per_behavior.max()),
        ],
        "D_h_values": sorted(frame.D_h.dropna().unique().tolist()),
        "I_per_domain": sorted(frame.I_per_domain.dropna().unique().tolist()),
        "blocks_total_tested": int(frame.B.sum()),
        "J_bar": round(float(frame.J.mean()), 2),
        "stage4_eligible_rounds_per_simulation_mean": round(
            accounting["stage4_eligible_rounds_per_simulation_mean"], 2
        ),
        "stage4_eligible_rounds_per_hypothesis_mean": round(
            accounting["stage4_eligible_rounds_per_hypothesis_mean"], 1
        ),
        "blocks_per_hypothesis_mean": round(float(frame.B.mean()), 2),
        "n_hypotheses_tested": len(frame),
        "n_analysis_observations": accounting["n_analysis_observations"],
        "stage4_eligible_nominal_rounds": accounting["stage4_eligible_nominal_rounds"],
        "stage4_eligible_round_records": accounting["stage4_eligible_round_records"],
        "stage4_eligible_unique_rounds": accounting["stage4_eligible_unique_rounds"],
        "stage4_eligible_duplicate_round_records": accounting[
            "stage4_eligible_duplicate_round_records"
        ],
        "n_mean_per_hypothesis": round(float(frame.n.mean()), 2),
        "n_bf10_ge_3": len(significant),
        "pct_bf10_ge_3_and_p_le_05": round(100 * float((significant.p_tau <= P_TAU_THRESHOLD).mean()), 1),
        "spearman_bf10_vs_p_tau": round(float(spearman.statistic), 3),
        "spearman_bf10_vs_p_tau_pvalue": float(spearman.pvalue),
        "n_class_positive": int((frame.effect_class == "positive").sum()),
        "n_class_negative": int((frame.effect_class == "negative").sum()),
        "n_class_no_effect": int((frame.effect_class == "no_effect").sum()),
        "n_class_inconclusive": int((frame.effect_class == "inconclusive").sum()),
        "n_rows_per_outcome_table": int(frame.n_outcomes.sum()),
        "n_configurations_designed": int(frame.n_designed.sum()),
        "n_simulations_run": int(frame.n_run.sum()),
        "Z_per_domain_mean": round(float(frame.Z_per_domain.mean()), 2),
    }
    return frame, numbers


def environment_fidelity_numbers(environment_fidelity_dir: str | Path) -> dict[str, Any]:
    root = Path(environment_fidelity_dir)
    manifest = pd.DataFrame(load_json(root / "sample_manifest.json"))
    config_rows = pd.read_csv(root / "config_recovery_rows.csv")
    fidelity = pd.read_csv(root / "simulation_fidelity_rows.csv")
    candidate_sizes: dict[tuple[Any, ...], int] = {}
    causal_by_hypothesis: dict[tuple[str, str], str] = {}
    for path in (root / "config_recovery").rglob("*.json"):
        payload = load_json(path)
        sample = payload.get("sample") or {}
        causal_by_hypothesis[(sample.get("behavior_name"), sample.get("axis_slug"))] = sample.get("causal_variable")
        for variable, spec in ((payload.get("target") or {}).get("variable_specs") or {}).items():
            candidate_sizes[(sample.get("behavior_name"), sample.get("axis_slug"), sample.get("simulation_id"), variable)] = len(spec.get("candidate_values") or [])
    config_rows["n_candidates"] = [candidate_sizes.get((b, a, s, v)) for b, a, s, v in zip(config_rows.behavior, config_rows.axis_slug, config_rows.simulation_id, config_rows.variable)]
    config_rows["random_match"] = 1 / config_rows.n_candidates
    config_rows["causal"] = [str(v).casefold() == str(causal_by_hypothesis.get((b, a))).casefold() for b, a, v in zip(config_rows.behavior, config_rows.axis_slug, config_rows.variable)]
    causal = config_rows[config_rows.causal]
    group_cols = ["behavior", "axis_slug", "domain_slug", "group_index"]
    groups = fidelity.groupby(group_cols).agg(J=("correct", "size"), recovered=("correct", "all")).reset_index()
    random_item = float((groups.J * (1 / groups.J)).sum() / groups.J.sum())
    random_group = float(np.mean([1 / math.factorial(int(value)) for value in groups.J]))
    human_eval_result = root / "variable_inference" / "human_eval_result.json"
    human_eval_scores = []
    if human_eval_result.exists():
        rating_values = {"high": 1.0, "medium": 0.5, "low": 0.0}
        for row in load_json(human_eval_result):
            if not isinstance(row, dict):
                continue
            rating = str(row.get("human_evaluated_match", "")).strip().casefold()
            if rating in rating_values:
                human_eval_scores.append(rating_values[rating])
    return {
        "environment_fidelity_n_samples": len(manifest),
        "environment_fidelity_groups_per_behavior": int(manifest.groupby("behavior").size().mode().iloc[0]),
        "task1_n_variables": len(config_rows),
        "task1_exact_match_all": round(float(config_rows.exact_match.mean()), 3),
        "task1_exact_match_causal": round(float(causal.exact_match.mean()), 3),
        "task1_n_causal_variables": len(causal),
        "task1_random_match_all": round(float(config_rows.random_match.mean()), 3),
        "task1_random_match_causal": round(float(causal.random_match.mean()), 3),
        "task2_n_pairs": len(fidelity),
        "task2_item_accuracy_pct": round(100 * float(fidelity.correct.mean()), 1),
        "task2_random_baseline_pct": round(100 * random_item, 1),
        "task2_n_groups": len(groups),
        "task2_group_accuracy_pct": round(100 * float(groups.recovered.mean()), 1),
        "task2_group_random_baseline_pct": round(100 * random_group, 1),
        "task3_n_groups": len(groups),
        "task3_human_eval_n_rated": len(human_eval_scores),
        "task3_human_eval_score": (
            round(float(np.mean(human_eval_scores)), 3)
            if human_eval_scores
            else None
        ),
    }


def inter_subject_generalization_table(reported_results_dir: str | Path, subject_agent_result_dirs: Mapping[str, str | Path]) -> pd.DataFrame:
    reported = load_behavioral_findings(reported_results_dir)[["behavior_name", "axis_slug", "variable", "Delta", "bf10"]].rename(columns={"Delta": "Reported GPT-5-mini", "bf10": "reported_bf10"})
    selected_keys = None
    frames = []
    for name, directory in subject_agent_result_dirs.items():
        current = load_behavioral_findings(directory)[["behavior_name", "axis_slug", "Delta"]].rename(columns={"Delta": name})
        frames.append(current)
        keys = set(zip(current.behavior_name, current.axis_slug))
        selected_keys = keys if selected_keys is None else selected_keys & keys
    selected_keys = selected_keys or set()
    table = reported[[key in selected_keys for key in zip(reported.behavior_name, reported.axis_slug)]].copy()
    for current in frames:
        table = table.merge(current, on=["behavior_name", "axis_slug"], how="inner")
    return table.sort_values(["behavior_name", "axis_slug"]).reset_index(drop=True)


def inter_subject_generalization_detail_table(
    reported_results_dir: str | Path,
    subject_agent_result_dirs: Mapping[str, str | Path],
    *,
    reported_label: str = "GPT (trial 1)",
    subject_agent_labels: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """Return long-form statistics for the Appendix D generalization table."""
    labels = {
        "GPT-5-mini (regenerated)": "GPT (trial 2)",
        "Gemini-3.1-Pro": "Gemini",
        "Kimi K2.6": "Kimi",
        "Kimi-K2.6": "Kimi",
        **(subject_agent_labels or {}),
    }
    reported = load_behavioral_findings(reported_results_dir)
    subject_frames = {
        name: load_behavioral_findings(directory)
        for name, directory in subject_agent_result_dirs.items()
    }
    selected_keys = None
    for current in subject_frames.values():
        keys = set(zip(current.behavior_name, current.axis_slug))
        selected_keys = keys if selected_keys is None else selected_keys & keys
    selected_keys = selected_keys or set()
    base = reported[[key in selected_keys for key in zip(reported.behavior_name, reported.axis_slug)]].copy()
    base = base[["behavior_name", "axis_slug", "variable", "var_dimension"]].sort_values(
        ["behavior_name", "variable"]
    )
    base["_group_order"] = range(len(base))
    stat_columns = ["behavior_name", "axis_slug", "n", "bf10", "Delta", "tau", "p_tau", "effect_class"]
    rows = []
    for alpha_order, (name, frame) in enumerate(
        [(reported_label, reported), *subject_frames.items()]
    ):
        alpha = reported_label if alpha_order == 0 else labels.get(name, name)
        current = base.merge(frame[stat_columns], on=["behavior_name", "axis_slug"], how="inner")
        current["alpha"] = alpha
        current["_alpha_order"] = alpha_order
        rows.append(current)
    table = pd.concat(rows, ignore_index=True)
    table = table.rename(columns={"var_dimension": "manipulated_component"})
    table = table.sort_values(["_group_order", "_alpha_order"]).reset_index(drop=True)
    return table.drop(columns=["_group_order", "_alpha_order"])


def inter_subject_generalization_numbers(table: pd.DataFrame, subject_agent_names: list[str]) -> dict[str, Any]:
    numbers: dict[str, Any] = {"inter_subject_generalization_n_hypotheses": len(table)}
    for left, right in combinations(subject_agent_names, 2):
        pair = table[[left, right]].dropna()
        short = {"GPT-5-mini (regenerated)": "GPT", "Gemini-3.1-Pro": "Gemini", "Kimi-K2.6": "Kimi"}
        label = f"{short.get(left, left)}--{short.get(right, right)}"
        numbers[f"inter_subject_generalization_rank_corr_{label}"] = round(float(stats.spearmanr(pair[left], pair[right]).statistic), 3)
        numbers[f"inter_subject_generalization_l1_{label}"] = round(float((pair[left] - pair[right]).abs().mean()), 3)
    for name in subject_agent_names:
        pair = table[["Reported GPT-5-mini", name]].dropna()
        reported_effect = pair["Reported GPT-5-mini"]
        numbers[f"inter_subject_generalization_vs_reported_rho_{name}"] = round(float(stats.spearmanr(reported_effect, pair[name]).statistic), 3)
        numbers[f"inter_subject_generalization_vs_reported_l1_{name}"] = round(float((reported_effect - pair[name]).abs().mean()), 3)
    return numbers


def research_manager_gate_numbers(results_dir: str | Path) -> dict[str, Any]:
    """Count each research-manager gate from the artifact that owns its decision."""
    _, numbers = experiment_stage_accounting(results_dir)
    return numbers


def evidence_class_effects(results_dir: str | Path) -> pd.DataFrame:
    rows = []
    for hypothesis_dir in iter_hypothesis_dirs(results_dir):
        path = hypothesis_dir / STATISTICAL_ANALYSIS
        payload = runtime_artifact(path.name, load_json(path))
        for name, result in (payload.get("quantitative_analysis") or {}).items():
            if name in {"analysis_design", "aggregate_mean"}:
                continue
            rows.append({
                "behavior_name": payload.get("behavior_name", hypothesis_dir.parent.name),
                "axis_slug": payload.get("axis_slug", hypothesis_dir.name),
                "variable": payload.get("variable"),
                "evidence_class": name,
                "n": result.get("n"),
                "effect_class": result.get("effect_class"),
                "bf10": (result.get("monotone_analysis") or {}).get("bf10"),
                "Delta": (result.get("effect_size") or {}).get("Delta"),
            })
    return pd.DataFrame(rows)


def manuscript_registry(
    project_root: str | Path,
    *,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    _, behavioral_findings = behavioral_finding_numbers(root / "results" / "GPT-5-mini")
    environment_fidelity = environment_fidelity_numbers(root / "results" / "fidelity-results")
    research_manager_gates = research_manager_gate_numbers(root / "results" / "GPT-5-mini")
    subject_agent_result_dirs = {
        "GPT-5-mini (regenerated)": root / "results" / "GPT-5-mini (regenerated)",
        "Gemini-3.1-Pro": root / "results" / "Gemini-3.1-Pro",
        "Kimi-K2.6": root / "results" / "Kimi-K2.6",
    }
    inter_subject_generalization = inter_subject_generalization_numbers(
        inter_subject_generalization_table(root / "results" / "GPT-5-mini", subject_agent_result_dirs), list(subject_agent_result_dirs)
    )
    *_, cost_numbers = appendix_cost_analysis(root)
    values = {
        **environment_fidelity,
        **research_manager_gates,
        **inter_subject_generalization,
        # The stage ledger and the Sec. 4.1 numbers share the round-count keys. The
        # ledger keeps them unrounded; the manuscript reports them rounded, so the
        # Sec. 4.1 dict is merged last and owns the rounded display value.
        **behavioral_findings,
        "appendix_e_cost_analysis": manuscript_cost_value(cost_numbers),
    }
    registry = {key: {"value": value} for key, value in values.items()}
    if output_path is not None:
        save_json(registry, output_path)
    return registry


def behavioral_findings_table(frame: pd.DataFrame, *, significant_only: bool = True) -> pd.DataFrame:
    selected = frame[frame.bf10 >= BF_EFFECT_THRESHOLD] if significant_only else frame
    columns = ["behavior_name", "variable", "D_h", "B", "J", "T", "n", "bf10", "Delta", "tau", "p_tau", "effect_class"]
    table = selected[columns].sort_values(["behavior_name", "variable"]).reset_index(drop=True)
    table["effect_class"] = table.effect_class.map(EFFECT_CLASS_LABELS).fillna(table.effect_class)
    return table


def behavioral_evidence_class_findings_table(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for hypothesis in frame.itertuples(index=False):
        analysis_path = Path(hypothesis.hypothesis_dir) / STATISTICAL_ANALYSIS
        payload = runtime_artifact(analysis_path.name, load_json(analysis_path))
        for evidence_class, result in (payload.get("quantitative_analysis") or {}).items():
            if evidence_class in {"analysis_design", "aggregate_mean"}:
                continue
            monotone = result.get("monotone_analysis") or {}
            effect = result.get("effect_size") or {}
            rank = result.get("rank_correlation") or {}
            rows.append(
                {
                    "behavior_name": hypothesis.behavior_name,
                    "variable": hypothesis.variable,
                    "manipulated_component": hypothesis.var_dimension,
                    "num_domains": hypothesis.D_h,
                    "num_groups": hypothesis.B,
                    "num_causal_values": hypothesis.J,
                    "num_rounds": hypothesis.T,
                    "outcome": evidence_class,
                    "n": result.get("n"),
                    "bf10": monotone.get("bf10"),
                    "Delta": effect.get("Delta"),
                    "tau": rank.get("tau"),
                    "p_tau": rank.get("p_tau"),
                    "effect_class": result.get("effect_class"),
                }
            )
    return pd.DataFrame(rows).sort_values(["behavior_name", "variable", "outcome"]).reset_index(drop=True)


def save_figure(fig: plt.Figure, output_stem: str | Path) -> None:
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".png"):
        fig.savefig(stem.with_suffix(suffix), dpi=300, bbox_inches="tight", facecolor="white")




def plot_effect_landscape(frame: pd.DataFrame, output_stem: str | Path | None = None) -> plt.Figure:
    data = frame.copy()
    preferred_columns = [
        ["compete", "distrust", "plan", "strategic aggression", "non-compliance", "extroversion"],
        ["purchase", "deceive", "friendliness", "empathy", "literalism", "sycophancy"],
    ]
    present = set(data.behavior_name)
    columns = [[behavior for behavior in column if behavior in present] for column in preferred_columns]

    behavior_labels = {
        "strategic aggression": "strategic\naggression",
    }

    variable_labels = {
        "Relative performance emphasis": "Relative perf. emphasis",
        "Role interdependence structure": "Role interdependence",
        "Communication overconfidence": "Actor overconfidence",
        "Opponent aggressiveness level": "Opponent aggression level",
        "Access to counter-attitudinal data": "Access to attitudinal data",
        "Constraint-instruction conflict": "Instruction conflict",
        "Constraint_complexity_and_conflict": "Constraint complexity & conflict",
        "Cost-minimization goal strength": "Cost-minimization goal",
        "Counterparty_interaction_style": "Actor friendliness",
        "Counterparty_vulnerability_cues": "Vulnerability cues",
        "Emotional expression constraints": "Emotional constraints",
        "Intervention authority over others": "Intervention authority",
        "Normative_deception_modeling_by_actors": "Deception norms",
        "Peer purchasing descriptive norms": "Peer purchase norms",
        "Relationship continuity expectation": "Relationship continuity",
        "Reward for throughput efficiency": "Reward for efficiency",
        "Short_term_payoff_weighting": "Short-term payoff",
        "Uncertainty of sanctions for aggression": "Sanction uncertainty",
        "Unfriendliness_penalty_severity": "Unfriendly penalty",
        "Vendor persuasiveness intensity": "Vendor persuasion",
    }

    def format_variable(value: Any) -> str:
        label = variable_labels.get(str(value), str(value).replace("_", " "))
        return " ".join(label.split())

    def layout(behaviors: list[str]) -> tuple[list[tuple[Any, float]], list[tuple[str, float, float]], float]:
        rows, spans, cursor = [], [], 0.0
        for behavior in behaviors:
            block = data[data.behavior_name == behavior].sort_values("Delta", ascending=False)
            if block.empty:
                continue
            start = cursor
            for row in block.itertuples(index=False):
                rows.append((row, cursor))
                cursor += 1.0
            spans.append((behavior, start - 0.45, cursor - 0.55))
            cursor += 1.05
        return rows, spans, max(cursor - 1.05, 0.0)

    layouts = [layout(column) for column in columns]
    max_y = max(item[2] for item in layouts)
    fig = plt.figure(figsize=(9.18, 8.13), facecolor=SURFACE)
    outer = fig.add_gridspec(1, 2, wspace=0.10, left=0.018, right=0.992, top=0.905, bottom=0.065)

    for column_index, (rows, spans, _) in enumerate(layouts):
        inner = outer[0, column_index].subgridspec(
            1, 4, width_ratios=[0.12, 0.43, 0.225, 0.225], wspace=0.055
        )
        ax_behavior = fig.add_subplot(inner[0, 0])
        ax_label = fig.add_subplot(inner[0, 1], sharey=ax_behavior)
        ax_delta = fig.add_subplot(inner[0, 2], sharey=ax_behavior)
        ax_bf = fig.add_subplot(inner[0, 3], sharey=ax_behavior)

        for ax in (ax_behavior, ax_label, ax_delta, ax_bf):
            ax.set_ylim(max_y - 0.35, -0.85)
            ax.set_yticks([])

        ax_behavior.set_xlim(0, 1)
        ax_label.set_xlim(0, 1)
        ax_behavior.axis("off")
        ax_label.axis("off")

        for row, y in rows:
            effect = row.effect_class
            color = EFFECT_COLORS.get(effect, MUTED)
            weight = "bold" if effect in {"positive", "negative"} else "normal"
            label_color = INK if effect in {"positive", "negative"} else INK2
            ax_label.text(0.85, y, format_variable(row.variable), va="center", ha="right", fontsize=7.4, color=label_color, fontweight=weight)
            ax_delta.plot([row.Delta_low, row.Delta_high], [y, y], color=color, alpha=0.55, lw=1.55, solid_capstyle="round")
            ax_delta.scatter([row.Delta], [y], zorder=3, **_marker(effect, 24))
            ax_bf.scatter([row.log10_bf10], [y], zorder=3, **_marker(effect, 19))

        for behavior, start, end in spans:
            ax_behavior.plot([0.46, 0.46], [start, end], color=AXIS, lw=1.35, clip_on=False)
            ax_behavior.text(
                0.16,
                (start + end) / 2,
                behavior_labels.get(behavior, behavior),
                rotation=90,
                va="center",
                ha="center",
                fontsize=8.4,
                color=INK,
                fontweight="bold",
                linespacing=0.9,
                clip_on=False,
            )

        ax_delta.set_xlim(-3.45, 6.05)
        ax_delta.set_xticks([0, 5])
        ax_bf.set_xlim(-1.45, 15.95)
        ax_bf.set_xticks([0, 5, 10, 15])
        for ax, label in ((ax_delta, r"$\Delta$ (95% CrI)"), (ax_bf, r"$\log_{10}\mathrm{BF}_{10}$")):
            ax.axvline(0, color=AXIS, lw=1.05, zorder=0)
            ax.grid(axis="x", color=GRID, lw=0.65, zorder=0)
            ax.tick_params(axis="x", which="both", top=True, labeltop=True, bottom=True, labelbottom=True, length=0, pad=2.5, colors=INK2, labelsize=8.8)
            ax.tick_params(axis="y", length=0)
            ax.text(0.5, 1.025, label, transform=ax.transAxes, ha="center", va="bottom", fontsize=9.4, color=INK)
            ax.set_xlabel(label, fontsize=9.4, color=INK, labelpad=4)
            for side in ("left", "right", "top"):
                ax.spines[side].set_visible(False)
            ax.spines["bottom"].set_color(AXIS)
            ax.spines["bottom"].set_linewidth(0.75)

        ax_behavior.text(0.16, 1.025, r"$Y$", transform=ax_behavior.transAxes, ha="center", va="bottom", fontsize=9.4, color=INK)
        ax_behavior.text(0.16, -0.035, r"$Y$", transform=ax_behavior.transAxes, ha="center", va="top", fontsize=9.4, color=INK)
        ax_label.text(0.5, 1.025, r"$X$", transform=ax_label.transAxes, ha="center", va="bottom", fontsize=9.4, color=INK)
        ax_label.text(0.5, -0.035, r"$X$", transform=ax_label.transAxes, ha="center", va="top", fontsize=9.4, color=INK)

    handles = [
        Line2D([], [], linestyle="none", marker="^", markersize=5.4, markerfacecolor=POS, markeredgecolor=POS, label="positive"),
        Line2D([], [], linestyle="none", marker="v", markersize=5.4, markerfacecolor=NEG, markeredgecolor=NEG, label="negative"),
        Line2D([], [], linestyle="none", marker="o", markersize=5.0, markerfacecolor=MUTED, markeredgecolor=MUTED, label="no effect"),
        Line2D([], [], linestyle="none", marker="o", markersize=5.0, markerfacecolor=SURFACE, markeredgecolor=MUTED, label="inconclusive"),
    ]
    legend = fig.legend(
        handles=handles,
        loc="upper center",
        ncol=4,
        frameon=True,
        bbox_to_anchor=(0.5, 0.995),
        fontsize=8.8,
        handletextpad=0.45,
        columnspacing=1.25,
        borderpad=0.35,
    )
    legend.get_frame().set_edgecolor(AXIS)
    legend.get_frame().set_linewidth(0.9)
    legend.get_frame().set_facecolor(SURFACE)
    if output_stem:
        save_figure(fig, output_stem)
    return fig



def plot_effect_by_configuration_component(frame: pd.DataFrame, output_stem: str | Path | None = None) -> plt.Figure:
    data = frame.dropna(subset=["var_dimension"]).copy()
    rng = np.random.default_rng(20260731)
    y_of = {dimension: position for position, dimension in enumerate(CONFIGURATION_COMPONENT_ORDER)}
    data["y"] = data.var_dimension.map(y_of)
    data["y_jitter"] = data.y + rng.uniform(-.20, .20, len(data))
    data["significant"] = data.bf10 >= BF_EFFECT_THRESHOLD
    fig, ax = plt.subplots(figsize=(9.24, 4.90), facecolor=SURFACE)
    ax.axvline(0, color=AXIS, lw=.8, zorder=0)
    for dimension in CONFIGURATION_COMPONENT_ORDER:
        block = data[data.var_dimension == dimension]
        y = y_of[dimension]
        q25, q50, q75 = block.Delta.quantile([.25, .5, .75])
        ax.plot([q25, q75], [y + .34, y + .34], lw=2.0, color=MUTED, solid_capstyle="round", zorder=1)
        ax.plot([q50, q50], [y + .24, y + .44], lw=2.0, color=MUTED, zorder=1)
        for row in block.itertuples(index=False):
            ax.scatter(row.Delta, row.y_jitter, s=26, marker="s", facecolor=MUTED if row.significant else SURFACE, edgecolor=MUTED, lw=1.05, zorder=2)
        total = len(block)
        ax.text(1.045, y, f"{int(block.significant.sum())}/{total}", transform=ax.get_yaxis_transform(), va="center", fontsize=13, color=INK)
    component = {"objective": r"$f$.roles", "authority": r"$f$.authority", "constraints": r"$f$.constraints", "situational context": r"$f$.world.context", "resource": r"$f$.world.resource", "actor": r"$f$.world.actors", "risk & return": r"$f$.consequence"}
    ax.set_yticks(list(y_of.values()), [component[name] for name in CONFIGURATION_COMPONENT_ORDER], fontsize=13, color=INK)
    ax.set(xlim=(-3, 5.4), ylim=(len(CONFIGURATION_COMPONENT_ORDER) - .42, -.52), xlabel=r"effect size $\Delta$")
    ax.set_xticks(np.arange(-3, 6, 1))
    ax.set_xlabel(r"effect size $\Delta$", fontsize=14)
    ax.grid(axis="x", color=GRID, lw=.6, zorder=0)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=0, labelsize=12, colors=INK)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.spines["bottom"].set_linewidth(.75)
    ax.text(1.045, 1.1, "ratio of", transform=ax.transAxes, va="top", fontsize=13.5, color=INK)
    ax.text(1.045, 1.05, r"$\mathrm{BF}_{10}\geq3$", transform=ax.transAxes, va="top", fontsize=13.5, color=INK)
    ax.text(1.04, 1.01, "-------------", transform=ax.transAxes, va="top", fontsize=13.5, color=INK)
    ax.legend(handles=[Line2D([], [], marker="s", markersize=5.8, linestyle="none", markerfacecolor=MUTED, markeredgecolor=MUTED, label=r"$\mathrm{BF}_{10}\geq3$"), Line2D([], [], marker="s", markersize=5.8, linestyle="none", markerfacecolor=SURFACE, markeredgecolor=MUTED, label="otherwise")], loc="lower center", bbox_to_anchor=(.47, 1.0), ncol=2, frameon=False, fontsize=14, handletextpad=.35, columnspacing=1.2)
    fig.subplots_adjust(left=.20, right=.86, top=.90, bottom=.12)
    if output_stem:
        save_figure(fig, output_stem)
    return fig


def plot_inter_subject_generalization(table: pd.DataFrame, subject_agent_names: list[str], output_stem: str | Path | None = None) -> plt.Figure:
    styles = [('#2A78D6', 'o'), ('#EB6834', 's'), ('#1BAF7A', '^')]
    values = table[["Reported GPT-5-mini", *subject_agent_names]].to_numpy(float)
    low, high = np.nanmin(values) - 0.45, np.nanmax(values) + 0.45
    fig, ax = plt.subplots(figsize=(5.77, 5.685), facecolor=SURFACE)
    ax.plot([low, high], [low, high], color=AXIS, lw=0.9, zorder=1)
    for name, (color, marker) in zip(subject_agent_names, styles):
        pair = table[["Reported GPT-5-mini", name]].dropna()
        reported_effect = pair["Reported GPT-5-mini"]
        rho = stats.spearmanr(reported_effect, pair[name]).statistic
        ax.scatter(reported_effect, pair[name], s=76, marker=marker, color=color, edgecolor="white", lw=1.0, zorder=2, label=rf"{name}   $\rho$ = {rho:.2f}")
    ax.set(
        xlim=(low, high),
        ylim=(low, high),
        xlabel="Effect size $\Delta$   (GPT-5-mini)",
        ylabel="Effect size $\Delta$   (subject agent)",
    )
    ax.grid(color=GRID, lw=.65)
    ax.tick_params(length=0, labelsize=12, colors=INK)
    ax.set_xlabel("Effect size $\Delta$   (GPT-5-mini)", fontsize=14)
    ax.set_ylabel("Effect size $\Delta$   (subject agent)", fontsize=14)
    ax.set_aspect("equal")
    ax.legend(frameon=False, loc="upper left", fontsize=14, handletextpad=.35, borderpad=.2, labelspacing=.45)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(.75)
    fig.subplots_adjust(left=.14, right=.98, top=.985, bottom=.12)
    if output_stem:
        save_figure(fig, output_stem)
    return fig


def plot_evidence_heatmaps(
    frame: pd.DataFrame,
    behaviors: list[str],
    output_stem: str | Path | None = None,
    *,
    columns: int = 2,
) -> plt.Figure:
    """Draw the article's shared-scale evidence-class heatmap grid."""
    limit = max(1.0, float(np.round(frame.Delta.abs().quantile(.95) * 2) / 2))
    rows = math.ceil(len(behaviors) / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(7.4, 3.3 * rows + .4), facecolor=SURFACE)
    axes = np.atleast_1d(axes).ravel()
    for ax, behavior in zip(axes, behaviors):
        block = frame[frame.behavior_name == behavior]
        delta = block.pivot(index="variable", columns="evidence_class", values="Delta")
        bayes = block.pivot(index="variable", columns="evidence_class", values="bf10")
        order = delta.abs().mean(axis=1).sort_values(ascending=False).index
        delta, bayes = delta.loc[order], bayes.loc[order]
        ax.imshow(delta, cmap=DIVERGING, vmin=-limit, vmax=limit, aspect="auto")
        for i in range(delta.shape[0]):
            for j in range(delta.shape[1]):
                value = delta.iloc[i, j]
                ax.text(j, i, "--" if not np.isfinite(value) else f"{value:+.2f}", ha="center", va="center", fontsize=6.6, color=INK if not np.isfinite(value) or abs(value) < .62 * limit else SURFACE)
                if np.isfinite(bayes.iloc[i, j]) and bayes.iloc[i, j] >= BF_EFFECT_THRESHOLD:
                    ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fill=False, edgecolor=INK, lw=1.5))
        ax.set_xticks(range(delta.shape[1]), [str(value)[:24] for value in delta.columns], rotation=30, ha="right", fontsize=6.4)
        ax.set_yticks(range(delta.shape[0]), [str(value)[:26] for value in delta.index], fontsize=6.8)
        ax.set_title(behavior, color=INK, fontweight="bold")
        ax.tick_params(length=0)
        for spine in ax.spines.values(): spine.set_visible(False)
    for ax in axes[len(behaviors):]: ax.set_visible(False)
    fig.tight_layout(h_pad=2.4, w_pad=2.0, rect=(0, .05, 1, 1))
    scale = fig.add_axes([.30, .012, .40, .012])
    fig.colorbar(plt.cm.ScalarMappable(cmap=DIVERGING, norm=plt.Normalize(-limit, limit)), cax=scale, orientation="horizontal")
    scale.set_xlabel(r"$\Delta$ (bold outline: $\mathrm{BF}_{10}\geq3$)", fontsize=8)
    if output_stem: save_figure(fig, output_stem)
    return fig
