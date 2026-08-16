"""Reproducible token and cost accounting from the reported result trees."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from ..storage.artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    RESEARCH_REPORT_JSON,
    STATISTICAL_ANALYSIS,
    canonical_filename,
)
from ..storage.ids import RunId
from ..storage.schema import runtime_artifact
from ..utils import load_json

TOKEN_COLUMNS = [
    "total_input_tokens",
    "cached_input_tokens",
    "total_output_tokens",
    "reasoning_output_tokens",
    "visible_output_tokens",
    "total_tokens",
]

# Fixed article price schedule in USD per one million tokens. Flex is 50% of
# these default-tier prices; this is intentionally not a live pricing lookup.
PAPER_PRICES = {
    "gpt-5.1": (1.25, 0.125, 10.00),
    "openai/gpt-5.1": (1.25, 0.125, 10.00),
    "gpt-5-mini": (0.25, 0.025, 2.00),
    "openai/gpt-5-mini": (0.25, 0.025, 2.00),
    "gemini/gemini-3.1-pro-preview": (2.00, 0.20, 12.00),
    "kimi-k2.6": (0.95, 0.16, 4.00),
}

DEFAULT_MODELS = {
    ("stage_1", "hypothesis_generator"): "openai/gpt-5.1",
    ("stage_1", "research_manager"): "openai/gpt-5.1",
    ("stage_2", "configuration_designer"): "openai/gpt-5.1",
    ("stage_2", "research_manager"): "openai/gpt-5.1",
    ("stage_3", "simulator_agent"): "openai/gpt-5.1",
    ("stage_3", "subject_agent"): "openai/gpt-5-mini",
    ("stage_3", "research_manager"): "openai/gpt-5.1",
    ("stage_4", "blind_reviewer"): "openai/gpt-5.1",
    ("final_report", "research_manager"): "openai/gpt-5.1",
}

LEGACY_AGENT_NAMES = {
    ("stage_1", "stage_agent"): "hypothesis_generator",
    ("stage_2", "stage_agent"): "configuration_designer",
    ("stage_3", "stage_3_simulator_agent"): "simulator_agent",
    ("stage_3", "stage_3_subject_agent"): "subject_agent",
    ("stage_4", "stage_agent"): "blind_reviewer",
}

REPORTED_RESULT_DIRECTORIES = ("GPT-5-mini",)


def reported_result_roots(project_root: str | Path) -> list[Path]:
    """Return the result tree included in token and cost accounting."""
    results = Path(project_root) / "results"
    return [results / name for name in REPORTED_RESULT_DIRECTORIES]


def _artifact_kind(path: Path, root: Path) -> str | None:
    name = canonical_filename(path.name)
    parts = path.relative_to(root).parts
    if name == HYPOTHESIS_GENERATION:
        return "hypothesis"
    if name == MATCHED_CONFIGURATIONS:
        return "config_design"
    if name == RESEARCH_REPORT_JSON:
        return "final_report"
    if "simulations" in parts and path.name.startswith("simulation_"):
        return "simulation"
    if "reviews" in parts and path.name.startswith("review_"):
        return "review"
    return None


def _stage(kind: str) -> str:
    return {
        "hypothesis": "stage_1",
        "config_design": "stage_2",
        "simulation": "stage_3",
        "review": "stage_4",
        "final_report": "final_report",
    }[kind]


def _context(path: Path, root: Path, kind: str) -> dict[str, Any]:
    parts = list(path.relative_to(root).parts)
    behavior = hypothesis_id = domain = None
    if kind == "hypothesis":
        behavior = parts[0]
    elif kind in {"config_design", "final_report"}:
        behavior, hypothesis_id = parts[:2]
    else:
        marker = "simulations" if kind == "simulation" else "reviews"
        index = parts.index(marker)
        domain, hypothesis_id, behavior = parts[index - 1], parts[index - 2], parts[index - 3]
    return {
        "root": root.name,
        "source_artifact": str(path.relative_to(root)),
        "behavior": behavior,
        "hypothesis_id": hypothesis_id,
        "domain": domain,
    }


def _reported_hypotheses(root: Path) -> set[tuple[str, str, str]]:
    return {
        (root.name, path.parts[-3], path.parts[-2])
        for path in root.glob("*/*/*.json")
        if canonical_filename(path.name) == STATISTICAL_ANALYSIS
    }


def _agent_name(stage: str, agent: Any) -> str:
    name = str(agent or "unknown")
    return LEGACY_AGENT_NAMES.get((stage, name), name)


def _model(stage: str, agent: str, payload: Mapping[str, Any]) -> str:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), Mapping) else {}
    legacy_metadata = (
        payload.get("meta_data") if isinstance(payload.get("meta_data"), Mapping) else {}
    )
    agents = payload.get("agents") if isinstance(payload.get("agents"), Mapping) else {}
    if agent in {"subject_agent", "simulator_agent"}:
        agent_config = agents.get(agent) if isinstance(agents.get(agent), Mapping) else {}
        legacy_key = f"{agent}_model"
        return str(
            agent_config.get("model")
            or metadata.get(legacy_key)
            or DEFAULT_MODELS[(stage, agent)]
        )
    return str(
        legacy_metadata.get("research_manager_model" if agent == "research_manager" else "model")
        or legacy_metadata.get("model")
        or metadata.get("model")
        or DEFAULT_MODELS[(stage, agent)]
    )


def _call_identity(
    stage: str,
    agent: str,
    call: Mapping[str, Any],
    context: Mapping[str, Any],
    payload: Mapping[str, Any],
    index: int,
) -> str:
    response_id = str(call.get("response_id") or "").strip()
    if stage == "stage_3" and agent == "simulator_agent":
        if response_id:
            return f"stage3-simulator::{context['root']}::{response_id}"
        run = RunId.from_mapping(payload)
        return "::".join(
            map(
                str,
                [
                    context["root"],
                    context["behavior"],
                    context["hypothesis_id"],
                    context["domain"],
                    run.group_id,
                    run.repetition,
                    call.get("round"),
                    agent,
                ],
            )
        )
    if stage == "stage_3" and agent == "subject_agent":
        return "::".join(
            [
                "stage3-subject",
                str(context["root"]),
                str(context["source_artifact"]),
                str(index),
                response_id,
            ]
        )
    suffix = response_id or str(index)
    return f"{context['root']}::{context['source_artifact']}::{suffix}"


def token_calls(result_roots: Sequence[str | Path], *, flex_discount: float = 0.5) -> pd.DataFrame:
    """Build one priced row per billable response.

    Shared Stage 3 simulator calls are stored in every condition transcript and
    are de-duplicated by response id (or by group, repetition, and round when an
    id is absent). Subject-agent calls remain condition-specific.
    """
    roots = [Path(root) for root in result_roots]
    reported = set().union(*(_reported_hypotheses(root) for root in roots))
    reported_behaviors = {(root, behavior) for root, behavior, _ in reported}
    rows: list[dict[str, Any]] = []
    for root in roots:
        for path in root.rglob("*.json"):
            relative = path.relative_to(root)
            if "arxivs" in relative.parts or "backup" in relative.parts:
                continue
            kind = _artifact_kind(path, root)
            if kind is None:
                continue
            context = _context(path, root, kind)
            hypothesis_key = (context["root"], context["behavior"], context["hypothesis_id"])
            if context["hypothesis_id"] is None:
                if (context["root"], context["behavior"]) not in reported_behaviors:
                    continue
            elif hypothesis_key not in reported:
                continue
            payload = load_json(path)
            usage = payload.get("token_usage") or payload.get("token_counts") or {}
            calls = usage.get("calls") if isinstance(usage, Mapping) else None
            if not isinstance(calls, list):
                continue
            stage = _stage(kind)
            for index, call in enumerate(calls):
                if not isinstance(call, Mapping):
                    continue
                agent = _agent_name(stage, call.get("agent"))
                row = {
                    **context,
                    "accounting_stage": stage,
                    "agent": agent,
                    "model": _model(stage, agent, payload),
                    "round": call.get("round"),
                    "response_id": call.get("response_id"),
                }
                row.update(
                    {
                        column: int(call.get(column, 0) or 0)
                        for column in TOKEN_COLUMNS
                    }
                )
                row["uncached_input_tokens"] = max(
                    row["total_input_tokens"] - row["cached_input_tokens"], 0
                )
                row["call_identity"] = _call_identity(
                    stage, agent, call, context, payload, index
                )
                rows.append(row)

    frame = pd.DataFrame(rows).drop_duplicates("call_identity").reset_index(drop=True)
    unknown = sorted(set(frame.model) - set(PAPER_PRICES))
    if unknown:
        raise ValueError(f"Missing article price for models: {unknown}")
    prices = frame.model.map(PAPER_PRICES)
    frame["default_cost_usd"] = [
        (uncached * price[0] + cached * price[1] + output * price[2]) / 1_000_000
        for uncached, cached, output, price in zip(
            frame.uncached_input_tokens,
            frame.cached_input_tokens,
            frame.total_output_tokens,
            prices,
        )
    ]
    frame["flex_cost_usd"] = frame.default_cost_usd * flex_discount
    return frame


def hypothesis_count(calls: pd.DataFrame) -> int:
    return calls[["root", "behavior", "hypothesis_id"]].dropna().drop_duplicates().shape[0]


def cost_summary(calls: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    hypotheses = hypothesis_count(calls)
    stage = (
        calls.groupby("accounting_stage")
        .agg(
            calls=("call_identity", "nunique"),
            total_tokens=("total_tokens", "sum"),
            flex_cost_usd=("flex_cost_usd", "sum"),
        )
        .reset_index()
    )
    means = {
        "hypotheses": hypotheses,
        "billable_calls": len(calls),
        "uncached_input_tokens": float(calls.uncached_input_tokens.sum() / hypotheses),
        "cached_input_tokens": float(calls.cached_input_tokens.sum() / hypotheses),
        "output_tokens": float(calls.total_output_tokens.sum() / hypotheses),
        "total_tokens": float(calls.total_tokens.sum() / hypotheses),
        "flex_cost_usd": float(calls.flex_cost_usd.sum() / hypotheses),
    }
    stage["mean_tokens_per_hypothesis"] = stage.total_tokens / hypotheses
    stage["mean_flex_cost_per_hypothesis"] = stage.flex_cost_usd / hypotheses
    return stage, means


def stage3_agent_summary(calls: pd.DataFrame) -> pd.DataFrame:
    hypotheses = hypothesis_count(calls)
    return (
        calls[calls.accounting_stage.eq("stage_3")]
        .groupby("agent")
        .agg(
            calls=("call_identity", "nunique"),
            total_tokens=("total_tokens", "sum"),
            flex_cost_usd=("flex_cost_usd", "sum"),
        )
        .assign(
            mean_tokens_per_hypothesis=lambda frame: frame.total_tokens / hypotheses,
            mean_flex_cost_per_hypothesis=lambda frame: frame.flex_cost_usd / hypotheses,
        )
        .reset_index()
    )


def _interaction_rounds(result_roots: Sequence[str | Path]) -> dict[tuple[str, str, str], int]:
    rounds: dict[tuple[str, str, str], int] = {}
    for root_value in result_roots:
        root = Path(root_value)
        for analysis_path in root.glob("*/*/*.json"):
            if canonical_filename(analysis_path.name) != STATISTICAL_ANALYSIS:
                continue
            hypothesis_dir = analysis_path.parent
            manifests = [
                path
                for path in hypothesis_dir.glob("*.json")
                if canonical_filename(path.name) == "matched_simulation_runs.json"
            ]
            if len(manifests) != 1:
                raise ValueError(f"Expected one Stage 3 manifest in {hypothesis_dir}")
            payload = runtime_artifact(manifests[0].name, load_json(manifests[0]))
            value = payload.get("num_rounds")
            if not isinstance(value, int):
                raise ValueError(f"Missing configured round count in {manifests[0]}")
            rounds[(root.name, hypothesis_dir.parent.name, hypothesis_dir.name)] = value
    return rounds


def stage3_round_summary(
    calls: pd.DataFrame, result_roots: Sequence[str | Path]
) -> pd.DataFrame:
    configured_rounds = _interaction_rounds(result_roots)
    per_hypothesis = (
        calls[calls.accounting_stage.eq("stage_3")]
        .groupby(["root", "behavior", "hypothesis_id"])
        .agg(
            stage3_calls=("call_identity", "nunique"),
            stage3_tokens=("total_tokens", "sum"),
            stage3_flex_cost_usd=("flex_cost_usd", "sum"),
        )
        .reset_index()
    )
    per_hypothesis["interaction_rounds"] = [
        configured_rounds[(row.root, row.behavior, row.hypothesis_id)]
        for row in per_hypothesis.itertuples()
    ]
    return (
        per_hypothesis.groupby("interaction_rounds")
        .agg(
            hypotheses=("hypothesis_id", "count"),
            mean_stage3_tokens=("stage3_tokens", "mean"),
            mean_stage3_flex_cost_usd=("stage3_flex_cost_usd", "mean"),
        )
        .reset_index()
    )


def validate_reported_coverage(
    calls: pd.DataFrame, result_roots: Sequence[str | Path]
) -> None:
    """Fail if a reported hypothesis is absent from the call ledger."""
    expected = {
        Path(root).name: len(_reported_hypotheses(Path(root)))
        for root in result_roots
    }
    observed = (
        calls[["root", "behavior", "hypothesis_id"]]
        .dropna()
        .drop_duplicates()
        .groupby("root")
        .size()
        .to_dict()
    )
    if observed != expected:
        raise ValueError(
            f"Incomplete Appendix E hypothesis coverage: {observed}; "
            f"expected {expected}"
        )
    if not (
        calls.total_input_tokens
        == calls.uncached_input_tokens + calls.cached_input_tokens
    ).all():
        raise ValueError("Input-token categories do not reconcile")
    if not (calls.total_tokens == calls.total_input_tokens + calls.total_output_tokens).all():
        raise ValueError("Input and output tokens do not reconcile with total tokens")


def appendix_cost_analysis(
    project_root: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, float]]:
    """Rebuild every quantity in the Appendix E cost paragraph."""
    roots = reported_result_roots(project_root)
    calls = token_calls(roots)
    validate_reported_coverage(calls, roots)
    stage, overall = cost_summary(calls)
    agents = stage3_agent_summary(calls)
    rounds = stage3_round_summary(calls, roots)
    stage_values = stage.set_index("accounting_stage")
    agent_values = agents.set_index("agent")
    numbers = {
        **overall,
        "flex_discount": 0.5,
        "stage3_tokens": float(
            stage_values.at["stage_3", "mean_tokens_per_hypothesis"]
        ),
        "stage3_flex_cost_usd": float(
            stage_values.at["stage_3", "mean_flex_cost_per_hypothesis"]
        ),
        **{
            f"{stage_name}_flex_cost_usd": float(
                stage_values.at[stage_name, "mean_flex_cost_per_hypothesis"]
            )
            for stage_name in ("stage_1", "stage_2", "stage_4", "final_report")
        },
        **{
            f"stage3_{agent}_flex_cost_usd": float(
                agent_values.at[agent, "mean_flex_cost_per_hypothesis"]
            )
            for agent in ("simulator_agent", "subject_agent", "research_manager")
        },
    }
    for row in rounds.itertuples():
        prefix = f"stage3_{row.interaction_rounds}_round"
        numbers[f"{prefix}_hypotheses"] = int(row.hypotheses)
        numbers[f"{prefix}_flex_cost_usd"] = float(row.mean_stage3_flex_cost_usd)
    return calls, stage, agents, rounds, numbers


def manuscript_cost_value(numbers: Mapping[str, float]) -> dict[str, float]:
    """Map executable cost outputs to the labels used by the manuscript registry."""
    return {
        "hypothesis-level analyses": numbers["hypotheses"],
        "billable calls": numbers["billable_calls"],
        "mean uncached input tokens": numbers["uncached_input_tokens"],
        "mean cached input tokens": numbers["cached_input_tokens"],
        "mean output tokens": numbers["output_tokens"],
        "mean total tokens": numbers["total_tokens"],
        "mean flex cost (USD)": numbers["flex_cost_usd"],
        "mean stage 3 tokens": numbers["stage3_tokens"],
        "mean stage 3 flex cost (USD)": numbers["stage3_flex_cost_usd"],
    }
