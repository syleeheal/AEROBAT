"""Orchestration of AEROBAT's four-stage behavioral-research pipeline."""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from aerobat.protocol.normalization import NormalizationManager
from aerobat.storage.ids import RunId
from aerobat.storage.artifacts import HYPOTHESIS_GENERATION, MATCHED_CONFIGURATIONS
from aerobat.storage.schema import runtime_artifact
from aerobat.protocol.payloads import PayloadManager
from aerobat.stages.stage1_hypothesis import generate_hypotheses
from aerobat.stages.stage2_config_design import (
    hypothesis_slug,
    resolve_max_concurrent,
    resolve_num_matched_groups,
    design_matched_configurations,
    design_matched_configurations_for_hypothesis,
)
from aerobat.stages.stage3_simulation import (
    load_saved_matched_simulation_runs,
    rounds_from_interaction_length,
    run_matched_simulation_group,
)
from aerobat.stages.stage4_review import run_blind_reviews
from aerobat.stages.research_manager import (
    write_research_reports,
    run_ranking_gate,
    run_fidelity_gate,
    run_coherence_gate,
)
from aerobat.storage.transcripts import TranscriptManager
from aerobat.config import ExperimentConfig
from aerobat.analysis.reports import (
    load_statistical_analyses,
    save_statistical_analyses,
)
from aerobat.utils import (
    config_section,
    load_json,
    mapping_records,
    mapping_value,
    positive_int_setting,
    research_manager_gate_enabled,
)

logger = logging.getLogger(__name__)

PIPELINE_STAGES = frozenset({1, 2, 3, 4})


def _normalize_stages(stages: Sequence[int] | None) -> tuple[int, ...] | None:
    if stages is None:
        return None
    requested = tuple(stages)
    if not requested:
        raise ValueError("stages must contain at least one stage number.")
    invalid = [
        stage
        for stage in requested
        if isinstance(stage, bool) or not isinstance(stage, int) or stage not in PIPELINE_STAGES
    ]
    if invalid:
        raise ValueError(f"stages must contain only 1, 2, 3, or 4; got {invalid}.")
    selected = tuple(sorted(set(requested)))
    expected = tuple(range(selected[0], selected[-1] + 1))
    if selected != expected:
        raise ValueError(f"stages must be consecutive; got {list(selected)}.")
    return selected


@dataclass(frozen=True)
class MatchedSimulationConfig:
    selected_hypothesis_ids: list[str]
    num_reps: int
    num_rounds: int
    max_concurrent: int
    subject_agent_model: str
    simulator_agent_model: str
    subject_agent_temperature: float
    simulator_agent_temperature: float
    simulation_cfg: dict[str, Any]
    pipeline_cfg: dict[str, Any]


def _hypothesis_generation_counts(config: Mapping[str, Any]) -> dict[str, Any]:
    num_hypotheses = positive_int_setting(config, "hypothesis", "num_hypotheses", 20)
    return {
        "num_hypotheses": num_hypotheses,
        "num_domains": positive_int_setting(config, "hypothesis", "num_domains", 2),
        "num_stage2_hypotheses": positive_int_setting(
            config,
            "hypothesis",
            "num_stage2_hypotheses",
            num_hypotheses,
        ),
        "research_manager_stage_1": research_manager_gate_enabled(config, "stage_1"),
    }


def _matched_configuration_metadata(config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        # ``num_value_sets`` is the immutable legacy artifact key for I.
        "num_value_sets": resolve_num_matched_groups(dict(config)),
        "research_manager_stage_2": research_manager_gate_enabled(config, "stage_2"),
    }


def _required_section_float(section: Mapping[str, Any], key: str, section_name: str) -> float:
    if key not in section:
        raise ValueError(f"{section_name}.{key} must be configured.")
    return float(section[key])


async def load_or_generate_hypotheses(
    config: dict[str, Any],
    results_dir: str | Path,
    *,
    force: bool = False,
) -> dict[str, Any]:
    results_path = Path(results_dir)
    hypothesis_path = results_path / HYPOTHESIS_GENERATION

    if not force and hypothesis_path.exists():
        cached = runtime_artifact(hypothesis_path.name, load_json(hypothesis_path))
        if TranscriptManager.hypothesis_artifact_current(
            cached,
            _hypothesis_generation_counts(config),
        ):
            if TranscriptManager.stage_one_reviews_current(cached.get("hypotheses")):
                logger.info("Loaded hypothesis from %s", hypothesis_path)
                return cached
            logger.info("Loaded Stage 1 output from %s; running research manager.", hypothesis_path)
            return await run_ranking_gate(config, results_path, cached)
        logger.info("Existing hypothesis at %s is stale or incomplete; re-running Stage 1.", hypothesis_path)

    hypothesis = await generate_hypotheses(config, results_path)
    return await run_ranking_gate(config, results_path, hypothesis)


def expected_hypothesis_designs(
    hypothesis: Mapping[str, Any],
    results_dir: str | Path,
    config: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    stage1_enabled = (
        research_manager_gate_enabled(config, "stage_1")
        if config is not None
        else True
    )
    entries = PayloadManager.stage2_hypotheses(
        hypothesis,
        stage1_research_manager_enabled=stage1_enabled,
    )
    if not entries:
        raise ValueError("No hypotheses selected for Stage 2 from Stage 1 research-manager review.")

    base = Path(results_dir)
    return [
        {
            "variable": entry["variable"],
            "axis_slug": slug,
            "path": base / slug / MATCHED_CONFIGURATIONS,
        }
        for entry in entries
        for slug in [hypothesis_slug(entry["variable"])]
    ]


def _hypotheses_by_variable(hypothesis: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        NormalizationManager.text_value(item.get("variable")): item
        for item in mapping_records(hypothesis.get("hypotheses"))
        if NormalizationManager.text_value(item.get("variable"))
    }


def _attach_hypothesis(
    config_design: Mapping[str, Any],
    hypotheses_by_variable: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    enriched = dict(config_design)
    match = hypotheses_by_variable.get(
        NormalizationManager.text_value(enriched.get("variable"))
    )
    return {**enriched, "hypothesis": dict(match)} if match is not None else enriched


def _load_cached_matched_configurations(
    hypotheses: Sequence[Mapping[str, Any]],
    hypothesis: Mapping[str, Any],
    expected_metadata: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[Mapping[str, Any]]]:
    matched_configurations: dict[str, dict[str, Any]] = {}
    missing: list[Mapping[str, Any]] = []
    hypotheses_by_variable = _hypotheses_by_variable(hypothesis)

    for item in hypotheses:
        path = Path(item["path"])
        cached = runtime_artifact(path.name, load_json(path)) if path.exists() else None
        if cached is not None and TranscriptManager.config_design_artifact_current(cached, dict(expected_metadata)):
            matched_configurations[str(item["axis_slug"])] = _attach_hypothesis(
                cached,
                hypotheses_by_variable,
            )
        else:
            missing.append(item)
    return matched_configurations, missing


async def _generate_missing_matched_configurations(
    *,
    config: dict[str, Any],
    results_dir: str | Path,
    hypothesis: dict[str, Any],
    missing_hypotheses: Sequence[Mapping[str, Any]],
    semaphore: asyncio.Semaphore,
) -> dict[str, dict[str, Any]]:
    results_path = Path(results_dir)
    variable_by_slug = {
        hypothesis_slug(entry["variable"]): entry
        for entry in PayloadManager.stage2_hypotheses(
            hypothesis,
            stage1_research_manager_enabled=research_manager_gate_enabled(config, "stage_1"),
        )
    }
    tasks = []
    for item in missing_hypotheses:
        slug = str(item["axis_slug"])
        variable_dir = results_path / slug
        variable_dir.mkdir(parents=True, exist_ok=True)
        tasks.append(
            design_matched_configurations_for_hypothesis(
                config=config,
                variable_dir=variable_dir,
                stage1_hypothesis=hypothesis,
                variable_entry=variable_by_slug[slug],
                semaphore=semaphore,
            )
        )

    generated = await asyncio.gather(*tasks)
    return {item["axis_slug"]: item for item in generated}


async def _run_coherence_gate_for_designs(
    config: dict[str, Any],
    matched_configurations_by_id: dict[str, dict[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]],
    semaphore: asyncio.Semaphore,
) -> dict[str, dict[str, Any]]:
    if not research_manager_gate_enabled(config, "stage_2"):
        return matched_configurations_by_id

    hypothesis_by_id = {str(item["axis_slug"]): item for item in hypotheses}
    stale = [
        (slug, design)
        for slug, design in matched_configurations_by_id.items()
        if not TranscriptManager.config_design_reviews_current(design.get("domain_results"))
    ]
    if not stale:
        return matched_configurations_by_id

    reviewed = await asyncio.gather(
        *[
            run_coherence_gate(
                config,
                design,
                hypothesis_by_id[slug]["path"],
                llm_semaphore=semaphore,
            )
            for slug, design in stale
        ]
    )
    for (slug, _), design in zip(stale, reviewed):
        matched_configurations_by_id[slug] = design
    return matched_configurations_by_id


async def load_or_design_matched_configurations(
    config: dict[str, Any],
    results_dir: str | Path,
    hypothesis: dict[str, Any],
    *,
    force: bool = False,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    selected_hypotheses = expected_hypothesis_designs(hypothesis, results_dir, config=config)
    semaphore = asyncio.Semaphore(resolve_max_concurrent(config))

    if force:
        bundle = await design_matched_configurations(config, Path(results_dir), hypothesis)
        matched_configurations = bundle["by_axis_slug"]  # legacy artifact key
    else:
        matched_configurations, missing_hypotheses = _load_cached_matched_configurations(
            selected_hypotheses,
            hypothesis,
            _matched_configuration_metadata(config),
        )
        if missing_hypotheses:
            logger.info(
                "Loaded %s cached matched-configuration artifact(s); generating %s missing hypothesis artifact(s): %s",
                len(matched_configurations),
                len(missing_hypotheses),
                [item["axis_slug"] for item in missing_hypotheses],
            )
            matched_configurations.update(
                await _generate_missing_matched_configurations(
                    config=config,
                    results_dir=results_dir,
                    hypothesis=hypothesis,
                    missing_hypotheses=missing_hypotheses,
                    semaphore=semaphore,
                )
            )
        else:
            logger.info("Loaded %s cached matched-configuration artifact(s).", len(matched_configurations))

    matched_configurations = await _run_coherence_gate_for_designs(
        config,
        matched_configurations,
        selected_hypotheses,
        semaphore,
    )
    return matched_configurations, selected_hypotheses


def build_matched_simulation_config(
    config: Mapping[str, Any],
    all_hypothesis_ids: Sequence[str],
    *,
    selected_hypothesis_ids: Sequence[str] | None = None,
) -> MatchedSimulationConfig:
    selected = list(selected_hypothesis_ids or all_hypothesis_ids)
    unknown = [slug for slug in selected if slug not in all_hypothesis_ids]
    if unknown:
        raise ValueError(f"Unknown hypothesis id(s): {unknown}. Available: {list(all_hypothesis_ids)}")

    simulation_cfg = config_section(config, "simulation")
    simulation_cfg["service_tier"] = simulation_cfg.get("service_tier", config.get("service_tier", "NA"))
    subject_agent_temperature = _required_section_float(
        simulation_cfg,
        "subject_agent_temperature",
        "simulation",
    )
    simulator_agent_temperature = _required_section_float(
        simulation_cfg,
        "simulator_agent_temperature",
        "simulation",
    )
    return MatchedSimulationConfig(
        selected_hypothesis_ids=selected,
        num_reps=int(simulation_cfg.get("num_reps", 1)),
        num_rounds=int(simulation_cfg.get("num_rounds", 4)),
        max_concurrent=int(config.get("max_concurrent", 5)),
        subject_agent_model=simulation_cfg.get("subject_agent_model", "openai/gpt-5-mini"),
        simulator_agent_model=simulation_cfg.get("simulator_agent_model", "openai/gpt-5-mini"),
        subject_agent_temperature=subject_agent_temperature,
        simulator_agent_temperature=simulator_agent_temperature,
        simulation_cfg=simulation_cfg,
        pipeline_cfg={
            "research_manager": config_section(config, "research_manager"),
            "service_tier": config.get("service_tier", "NA"),
        },
    )


def hypothesis_result_dirs(results_dir: str | Path, hypothesis_id: str) -> tuple[Path, Path]:
    experiment_dir = Path(results_dir) / hypothesis_id
    experiment_dir.mkdir(parents=True, exist_ok=True)
    return experiment_dir, experiment_dir


def _ensure_domain_artifact_dirs(experiment_dir: Path, simulations: Sequence[Mapping[str, Any]]) -> None:
    for simulation in simulations:
        domain_slug = TranscriptManager.domain_slug_from_simulation(dict(simulation))
        (experiment_dir / domain_slug / "simulations").mkdir(parents=True, exist_ok=True)
        (experiment_dir / domain_slug / "reviews").mkdir(parents=True, exist_ok=True)


def _hypothesis_run_state(
    results_dir: str | Path,
    hypothesis_id: str,
    config_design: Mapping[str, Any],
) -> dict[str, Any]:
    selected_simulations = PayloadManager.simulation_entries_from_config_design(config_design)
    selected_groups = PayloadManager.simulation_groups(selected_simulations)
    num_rounds = rounds_from_interaction_length(
        mapping_value(config_design.get("hypothesis")).get("interaction_length")
    )
    experiment_dir, simulation_dir = hypothesis_result_dirs(results_dir, hypothesis_id)
    _ensure_domain_artifact_dirs(experiment_dir, selected_simulations)
    return {
        "experiment_dir": experiment_dir,
        "simulation_dir": simulation_dir,
        "review_dir": experiment_dir,
        "selected_simulations": selected_simulations,
        "selected_groups": selected_groups,
        "num_rounds": num_rounds,
    }


def _matched_simulation_jobs(
    hypothesis_runs: Mapping[str, Mapping[str, Any]],
    simulation_config: MatchedSimulationConfig,
) -> list[tuple[str, Path, Mapping[str, Any], int, int]]:
    return [
        (
            hypothesis_id,
            hypothesis_runs[hypothesis_id]["simulation_dir"],
            simulation_group,
            repetition,
            hypothesis_runs[hypothesis_id]["num_rounds"],
        )
        for hypothesis_id in simulation_config.selected_hypothesis_ids
        for simulation_group in hypothesis_runs[hypothesis_id]["selected_groups"]
        for repetition in range(1, simulation_config.num_reps + 1)
    ]


async def _run_matched_simulation_job(
    *,
    job: tuple[str, Path, Mapping[str, Any], int, int],
    behavior_name: str,
    simulation_config: MatchedSimulationConfig,
    llm_semaphore: asyncio.Semaphore,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    hypothesis_id, simulation_dir, simulation_group, repetition, num_rounds = job
    resolved_batch = {
        **dict(simulation_group),
        "simulations": [
            PayloadManager.resolve_simulation_condition(dict(simulation))
            for simulation in simulation_group.get("simulations", [])
        ],
    }
    simulation_call = {
        "behavior_name": behavior_name,
        "simulation_group": resolved_batch,
        "repetition": repetition,
        "llm_semaphore": llm_semaphore,
        "verbose": False,
    }
    transcripts_by_index = await run_matched_simulation_group(
        **simulation_call,
        num_rounds=num_rounds,
        subject_agent_model=simulation_config.subject_agent_model,
        simulator_agent_model=simulation_config.simulator_agent_model,
        simulation_cfg=simulation_config.simulation_cfg,
        simulation_dir=simulation_dir,
    )
    any_partial = any(
        t.get("metadata", {}).get("partial") for t in transcripts_by_index.values()
    )
    if not any_partial:
        transcripts_by_index = await run_fidelity_gate(
            simulation_config.pipeline_cfg,
            behavior_name=behavior_name,
            simulation_group=resolved_batch,
            repetition=repetition,
            llm_semaphore=llm_semaphore,
            verbose=False,
            transcripts_by_index=transcripts_by_index,
        )
    return _save_group_transcripts(
        hypothesis_id,
        simulation_dir,
        simulation_group,
        repetition,
        transcripts_by_index,
    )


def _save_group_transcripts(
    hypothesis_id: str,
    simulation_dir: Path,
    simulation_group: Mapping[str, Any],
    repetition: int,
    transcripts_by_index: Mapping[int, Mapping[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = []
    transcript_manager = TranscriptManager(simulation_dir)
    for simulation in mapping_records(simulation_group.get("simulations")):
        run = RunId.from_mapping({**simulation, "repetition": repetition})
        transcript = transcripts_by_index[run.value_index]
        rows.append(
            PayloadManager.simulation_run_row(
                axis_slug=hypothesis_id,
                simulation=simulation,
                repetition=repetition,
                transcript=transcript,
            )
        )
        transcript_manager.save_simulation_transcript(transcript=dict(transcript), run=run)
    return rows


def _flatten_group_rows(
    grouped_rows: Sequence[Sequence[dict[str, Any]]],
) -> list[dict[str, Any]]:
    return [row for group_rows in grouped_rows for row in group_rows]


def _save_hypothesis_runs(
    *,
    hypothesis_run: dict[str, Any],
    group_rows: Sequence[Sequence[dict[str, Any]]],
    simulation_config: MatchedSimulationConfig,
) -> None:
    experiment_dir = hypothesis_run["experiment_dir"]
    num_rounds = hypothesis_run["num_rounds"]
    runs = _flatten_group_rows(group_rows)

    saved = TranscriptManager(experiment_dir).save_matched_simulation_runs(
        transcript_entries=runs,
        num_reps=simulation_config.num_reps,
        num_rounds=num_rounds,
        environment_rendering_formats=PayloadManager.environment_formats_from_rows(runs),
    )
    hypothesis_run.update({"runs": runs, **saved})


async def run_matched_simulations(
    *,
    results_dir: str | Path,
    hypothesis: Mapping[str, Any],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    simulation_config: MatchedSimulationConfig,
) -> dict[str, dict[str, Any]]:
    behavior_name = hypothesis["behavior_name"]
    llm_semaphore = asyncio.Semaphore(simulation_config.max_concurrent)
    hypothesis_runs = {
        slug: _hypothesis_run_state(results_dir, slug, matched_configurations_by_id[slug])
        for slug in simulation_config.selected_hypothesis_ids
    }
    jobs = _matched_simulation_jobs(hypothesis_runs, simulation_config)

    logger.info(
        "Running %s simulator group simulation(s) (%s transcripts, max %s concurrent LLM call(s)) across %s variable(s).",
        len(jobs),
        sum(len(job[2]["simulations"]) for job in jobs),
        simulation_config.max_concurrent,
        len(simulation_config.selected_hypothesis_ids),
    )
    results = await asyncio.gather(
        *[
            _run_matched_simulation_job(
                job=job,
                behavior_name=behavior_name,
                simulation_config=simulation_config,
                llm_semaphore=llm_semaphore,
            )
            for job in jobs
        ]
    )

    grouped_results = defaultdict(list)
    for job, result in zip(jobs, results):
        grouped_results[job[0]].append(result)

    for hypothesis_id in simulation_config.selected_hypothesis_ids:
        _save_hypothesis_runs(
            hypothesis_run=hypothesis_runs[hypothesis_id],
            group_rows=grouped_results[hypothesis_id],
            simulation_config=simulation_config,
        )
    return hypothesis_runs


@dataclass(frozen=True)
class ResearchPipelineResult:
    hypothesis_generation: dict[str, Any]
    matched_configurations: dict[str, dict[str, Any]]
    matched_simulation_runs: dict[str, dict[str, Any]]
    blind_reviews: dict[str, dict[str, Any]]
    statistical_analyses: dict[str, dict[str, Any]]
    research_reports: dict[str, dict[str, Any]]


class AerobatPipeline:
    """Cache-aware public interface for the method-faithful four-stage pipeline."""

    def __init__(self, config: ExperimentConfig | Mapping[str, Any]):
        if isinstance(config, ExperimentConfig):
            self.public_config = config
            self.config = dict(config.raw)
            self.results_dir = config.target_behavior_dir
        else:
            self.public_config = None
            self.config = dict(config)
            behavior = self.config.get("behavior", {})
            behavior_name = (
                str(behavior.get("name", ""))
                if isinstance(behavior, Mapping)
                else str(behavior)
            )
            self.results_dir = (
                Path(self.config.get("results_dir", "results/GPT-5-mini")) / behavior_name
            )
        self.results_dir.mkdir(parents=True, exist_ok=True)

    async def _simulations(
        self,
        hypothesis: dict[str, Any],
        matched_configurations: dict[str, dict[str, Any]],
        simulation_config: MatchedSimulationConfig,
        *,
        force: bool,
    ) -> dict[str, dict[str, Any]]:
        if not force:
            try:
                return load_saved_matched_simulation_runs(
                    results_dir=self.results_dir,
                    matched_configurations_by_id=matched_configurations,
                    simulation_config=simulation_config,
                )
            except FileNotFoundError:
                pass
        return await run_matched_simulations(
            results_dir=self.results_dir,
            hypothesis=hypothesis,
            matched_configurations_by_id=matched_configurations,
            simulation_config=simulation_config,
        )

    def _analyses(
        self,
        hypothesis: Mapping[str, Any],
        matched_configurations: Mapping[str, Mapping[str, Any]],
        blind_reviews: Mapping[str, Mapping[str, Any]],
        hypothesis_ids: Sequence[str],
        *,
        force: bool,
    ) -> dict[str, dict[str, Any]]:
        if not force:
            try:
                return load_statistical_analyses(
                    results_dir=self.results_dir,
                    selected_hypothesis_ids=hypothesis_ids,
                    require_all=True,
                )
            except FileNotFoundError:
                pass

        save_statistical_analyses(
            results_dir=self.results_dir,
            behavior_name=str(hypothesis.get("behavior_name", "")),
            blind_reviews_by_id=blind_reviews,
            matched_configurations_by_id=matched_configurations,
            selected_hypothesis_ids=hypothesis_ids,
        )
        return load_statistical_analyses(
            results_dir=self.results_dir,
            selected_hypothesis_ids=hypothesis_ids,
            require_all=True,
        )

    async def run(
        self,
        *,
        stages: Sequence[int] | None = None,
        generate_reports: bool = False,
    ) -> ResearchPipelineResult:
        """Run selected stages, loading earlier prerequisites from cache.

        With ``stages=None``, the complete pipeline is cache-aware and only runs
        work whose valid artifact is missing. When stages are provided, each
        listed stage is rerun and stages after the highest selection are skipped.
        """

        selected_stages = _normalize_stages(stages)
        last_stage = max(selected_stages) if selected_stages is not None else 4

        def refresh(stage: int) -> bool:
            return selected_stages is not None and stage in selected_stages

        if generate_reports and last_stage < 4:
            raise ValueError("generate_reports requires Stage 4 to be included.")

        behavior = self.config.get("behavior")
        target_behavior = (
            behavior.get("name") if isinstance(behavior, Mapping) else behavior
        )
        logger.info(
            "Pipeline started for target behavior %r (stages=%s).",
            target_behavior,
            selected_stages,
        )
        logger.info("Stage 1/4 — generating or loading hypotheses.")
        hypothesis = await load_or_generate_hypotheses(
            self.config,
            self.results_dir,
            force=refresh(1),
        )
        logger.info(
            "Stage 1/4 complete — %s hypothesis candidate(s) available.",
            len(hypothesis.get("hypotheses") or []),
        )
        if last_stage == 1:
            return ResearchPipelineResult(hypothesis, {}, {}, {}, {}, {})

        logger.info("Stage 2/4 — designing or loading matched configurations.")
        matched_configurations, selected_hypotheses = await load_or_design_matched_configurations(
            self.config,
            self.results_dir,
            hypothesis,
            force=refresh(2),
        )
        hypothesis_ids = [str(item["axis_slug"]) for item in selected_hypotheses]
        logger.info(
            "Stage 2/4 complete — %s hypothesized causal variable(s) selected.",
            len(hypothesis_ids),
        )
        if last_stage == 2:
            return ResearchPipelineResult(hypothesis, matched_configurations, {}, {}, {}, {})

        simulation_config = build_matched_simulation_config(self.config, hypothesis_ids)
        logger.info("Stage 3/4 — generating or loading matched simulation runs.")
        matched_simulation_runs = await self._simulations(
            hypothesis,
            matched_configurations,
            simulation_config,
            force=refresh(3),
        )
        logger.info(
            "Stage 3/4 complete — %s matched simulation run(s) available.",
            sum(len(item.get("runs") or []) for item in matched_simulation_runs.values()),
        )
        if last_stage == 3:
            return ResearchPipelineResult(
                hypothesis,
                matched_configurations,
                matched_simulation_runs,
                {},
                {},
                {},
            )

        logger.info("Stage 4/4 — running or loading blind reviews and behavior scores.")
        blind_reviews = await run_blind_reviews(
            config=self.config,
            hypothesis=hypothesis,
            matched_configurations_by_id=matched_configurations,
            matched_simulation_runs_by_id=matched_simulation_runs,
            selected_hypothesis_ids=hypothesis_ids,
            load_existing=not refresh(4),
        )
        logger.info(
            "Stage 4/4 complete — review outputs available for %s hypothesized causal variable(s).",
            len(blind_reviews),
        )
        logger.info("Statistical analysis — estimating hypothesized behavioral effects.")
        statistical_analyses = self._analyses(
            hypothesis,
            matched_configurations,
            blind_reviews,
            hypothesis_ids,
            force=refresh(4),
        )
        logger.info(
            "Statistical analysis complete — %s hypothesis-level result(s) available.",
            len(statistical_analyses),
        )
        research_reports = (
            await write_research_reports(
                config=self.config,
                hypothesis=hypothesis,
                matched_configurations_by_id=matched_configurations,
                matched_simulation_runs_by_id=matched_simulation_runs,
                blind_reviews_by_id=blind_reviews,
                selected_hypothesis_ids=hypothesis_ids,
                statistical_analyses_by_id=statistical_analyses,
                quantitative_analyses_by_id={
                    slug: payload.get("quantitative_analysis", {})
                    for slug, payload in statistical_analyses.items()
                },
                load_existing=not refresh(4),
            )
            if generate_reports
            else {}
        )
        logger.info(
            "Pipeline complete — %s research report(s) available.",
            len(research_reports),
        )
        return ResearchPipelineResult(
            hypothesis,
            matched_configurations,
            matched_simulation_runs,
            blind_reviews,
            statistical_analyses,
            research_reports,
        )
