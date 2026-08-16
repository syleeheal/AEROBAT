"""AEROBAT Stage 4: blind review and target-behavior scoring."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from aerobat.protocol.normalization import NormalizationManager
from aerobat.runtime.llm import (
    limited_llm_call_with_metadata,
    llm_call_kwargs,
    resolve_stage_llm_settings,
)
from aerobat.protocol.prompts import BlindReviewerPrompts
from aerobat.protocol.stage_parsing import (
    align_behavior_assessment_keys,
    parse_behavior_eval,
)
from aerobat.storage.ids import RunId
from aerobat.protocol.payloads import PayloadManager
from aerobat.stages.stage2_config_design import simulations_by_run
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import (
    collect_fallbacks,
    mean_or_none,
    research_manager_gate_enabled,
)

logger = logging.getLogger(__name__)


async def _run_behavior_eval(
    behavior_name: str,
    behavior_hypothesis: str,
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]],
    simulation_history: List[Dict[str, Any]],
    settings: Any,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    user_prompt = BlindReviewerPrompts.make_behavior_eval_prompt_patch(
        behavior_name=behavior_name,
        behavior_hypothesis=behavior_hypothesis,
        behavior_eval_rubric=behavior_eval_rubric,
        simulation_history=simulation_history,
    )
    llm_response = await limited_llm_call_with_metadata(
        [PayloadManager.chat_message("user", user_prompt)],
        llm_semaphore=llm_semaphore,
        **llm_call_kwargs(settings),
    )
    response = llm_response.text
    return parse_behavior_eval(
        response,
        behavior_eval_rubric=behavior_eval_rubric,
    ), [
        TranscriptManager.build_prompt_record(
            1,
            user_prompt,
            response,
            stage="behavior_eval",
            token_counts=llm_response.token_counts,
            response_id=llm_response.response_id,
        ),
    ]


async def _judge_simulation(
    transcript: Dict[str, Any],
    hypothesis: Dict[str, Any],
    run: RunId,
    settings: Any,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
) -> Dict[str, Any]:
    with collect_fallbacks() as fallbacks:
        behavior_name = hypothesis["behavior_name"]
        behavior_hypothesis = hypothesis.get("definition", "")
        behavior_eval_rubric = hypothesis.get("behavior_eval_rubric", [])
        behavior_eval_history = PayloadManager.subject_agent_prompt_records(transcript["prompts"])

        behavior_eval, behavior_prompt = await _run_behavior_eval(
            behavior_name=behavior_name,
            behavior_hypothesis=behavior_hypothesis,
            behavior_eval_rubric=behavior_eval_rubric,
            simulation_history=behavior_eval_history,
            settings=settings,
            llm_semaphore=llm_semaphore,
        )

        return TranscriptManager.stage4_review_entry(
            run=run,
            behavior_eval=behavior_eval,
            prompts=behavior_prompt,
            fallbacks=list(fallbacks),
        )


def _behavior_stats(entry: Mapping[str, Any]) -> Dict[str, Any]:
    behavior_eval = entry.get("behavior_eval")
    if not isinstance(behavior_eval, dict):
        return PayloadManager.empty_behavior_stats(total_rounds=0)
    return PayloadManager.behavior_stats(behavior_eval, total_rounds=0)


def _build_summary_statistics(
    simulations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    evidence_class_scores: Dict[str, List[int | float]] = {}
    mean_scores: List[int | float] = []
    reviewer_counts = {
        "behavior_eval": 0,
    }

    for entry in simulations:
        if isinstance(entry.get("behavior_eval"), dict):
            reviewer_counts["behavior_eval"] += 1
        stats = _behavior_stats(entry)
        scores = stats.get("behavior_evidence_class_scores") or {}
        for evidence_class, score in scores.items():
            evidence_class_scores.setdefault(str(evidence_class), [])
            if isinstance(score, (int, float)) and not isinstance(score, bool):
                evidence_class_scores[str(evidence_class)].append(score)
        mean_score = stats.get("behavior_eval_mean_score")
        if isinstance(mean_score, (int, float)) and not isinstance(mean_score, bool):
            mean_scores.append(mean_score)

    return {
        "mean_behavior_eval_score": mean_or_none(mean_scores, digits=3),
        "mean_behavior_eval_score_by_evidence_class": {
            evidence_class: mean_or_none(scores, digits=3)
            for evidence_class, scores in evidence_class_scores.items()
        },
        "reviewer_counts": reviewer_counts,
    }


def _filter_stage3_valid_transcripts(
    transcript_inputs: List[Tuple[Dict[str, Any], Dict[str, Any]]],
) -> Tuple[List[Tuple[Dict[str, Any], Dict[str, Any]]], int]:
    eligible = []
    for context, transcript in transcript_inputs:
        if isinstance(transcript, dict) and transcript.get("passes_stage4") is True:
            eligible.append((context, transcript))
    return eligible, len(transcript_inputs) - len(eligible)


def _align_cached_behavior_assessment(
    review_entry: Any,
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None,
) -> bool:
    """Re-key a cached review's assessment in place; returns True when names changed."""

    behavior_eval = review_entry.get("behavior_eval") if isinstance(review_entry, Mapping) else None
    if not isinstance(behavior_eval, dict):
        return False
    assessment = behavior_eval.get("behavior_assessment")
    if not isinstance(assessment, Mapping):
        return False
    aligned = align_behavior_assessment_keys(assessment, behavior_eval_rubric)
    behavior_eval["behavior_assessment"] = aligned
    return list(aligned) != list(assessment)


def _review_task_records(
    transcript_inputs: Sequence[tuple[Dict[str, Any], Dict[str, Any]]],
    config_design: Dict[str, Any],
) -> List[Dict[str, Any]]:
    simulation_specs = simulations_by_run(config_design)
    records: List[Dict[str, Any]] = []
    for context, transcript in transcript_inputs:
        run = RunId.from_mapping(context)
        simulation = simulation_specs.get(run.key)
        if not simulation:
            logger.info("Skipping %s: no matched-configuration specification found.", run.label())
            continue
        records.append(
            {
                "context": dict(context),
                "transcript": transcript,
                "simulation_id": run.simulation_id,
                "group_id": run.group_id,
            }
        )
    return records


async def _judge_review_records(
    *,
    records: List[Dict[str, Any]],
    transcript_manager: TranscriptManager,
    behavior_eval_rubric: Any,
    hypothesis: Dict[str, Any],
    settings: Any,
    llm_semaphore: asyncio.Semaphore,
    load_existing: bool,
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    async def judge_one(record: Dict[str, Any]) -> Dict[str, Any]:
        context = record["context"]
        cached = (
            transcript_manager.load_stage4_outputs(context)
            if load_existing
            else None
        )
        if cached is not None:
            record["loaded_existing_review"] = True
            record["realigned_evidence_classes"] = _align_cached_behavior_assessment(
                cached,
                behavior_eval_rubric,
            )
            return cached
        return await _judge_simulation(
            transcript=record["transcript"],
            hypothesis=hypothesis,
            run=RunId.from_mapping(context),
            settings=settings,
            llm_semaphore=llm_semaphore,
        )

    results = await asyncio.gather(
        *(judge_one(record) for record in records),
        return_exceptions=True,
    )
    simulations: List[Dict[str, Any]] = []
    successful_records: List[Dict[str, Any]] = []
    for record, result in zip(records, results):
        if isinstance(result, Exception):
            logger.warning("Review failed: %s", result)
            continue
        simulations.append(result)
        record["review_entry"] = result
        successful_records.append(record)
        logger.info(
            "%s behavior_mean=%s",
            RunId.from_mapping(result).label(),
            _behavior_stats(result).get("behavior_eval_mean_score", "off"),
        )

    realigned_count = sum(
        bool(record.get("realigned_evidence_classes")) for record in successful_records
    )
    if realigned_count:
        logger.info(
            "Aligned evidence class names to the rubric in %s cached review(s).",
            realigned_count,
        )
    return simulations, successful_records


async def run_blind_review(
    config: Dict[str, Any],
    results_dir: Path,
    hypothesis: Dict[str, Any],
    config_design: Dict[str, Any],
    simulation: Optional[Dict[str, Any]] = None,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    load_existing: bool = True,
) -> Dict[str, Any]:
    behavior_name = hypothesis["behavior_name"]
    behavior_eval_rubric = hypothesis.get("behavior_eval_rubric", [])
    transcript_manager = TranscriptManager(results_dir)
    settings = resolve_stage_llm_settings(
        config,
        "review",
        default_max_tokens=8000,
    )
    include_research_manager = research_manager_gate_enabled(config, "stage_3")
    if llm_semaphore is None:
        llm_semaphore = asyncio.Semaphore(max(1, int(config.get("max_concurrent", 5))))

    logger.info("Stage 4 — blind review and behavior scoring: %s", behavior_name)
    logger.info("Model: %s", settings.model)
    logger.info("Fidelity gate: %s", "on" if include_research_manager else "off")

    transcript_inputs = transcript_manager.load_simulation_inputs(simulation=simulation)
    logger.info("Found %s simulation transcript(s).", len(transcript_inputs))
    if include_research_manager:
        transcript_inputs, skipped_count = _filter_stage3_valid_transcripts(transcript_inputs)
        logger.info("Stage 3 research-manager gate skipped %s transcript(s).", skipped_count)

    if not transcript_inputs:
        logger.info("No matched simulation runs found; skipping blind review.")
        return {}

    task_records = _review_task_records(
        transcript_inputs,
        config_design,
    )
    simulations, successful_records = await _judge_review_records(
        records=task_records,
        transcript_manager=transcript_manager,
        behavior_eval_rubric=behavior_eval_rubric,
        hypothesis=hypothesis,
        settings=settings,
        llm_semaphore=llm_semaphore,
        load_existing=load_existing,
    )

    records_to_save = [
        record for record in successful_records if not record.get("loaded_existing_review")
    ]
    for record in records_to_save:
        transcript_manager.save_stage4_outputs(record, record["review_entry"])

    summary_statistics = _build_summary_statistics(simulations)

    data = {
        "behavior_name": behavior_name,
        "model": settings.model,
        "research_manager_model": (
            NormalizationManager.object_value(config.get("research_manager")).get(
                "model",
                "openai/gpt-5.1",
            )
            if include_research_manager
            else None
        ),
        "research_manager_enabled": include_research_manager,
        "behavior_eval_rubric": behavior_eval_rubric,
        "total_simulations": len(task_records),
        "successful_count": len(simulations),
        "failed_count": len(task_records) - len(simulations),
        "simulations": simulations,
        "summary_statistics": summary_statistics,
        "fallbacks": [
            {
                "simulation_id": item.get("simulation_id"),
                "repetition": item.get("repetition"),
                **fallback,
            }
            for item in simulations
            for fallback in item.get("fallbacks", [])
        ],
    }

    logger.info("Blind-review outputs saved into %s review file(s).", len(records_to_save))
    return data


async def run_blind_reviews(
    *,
    config: Dict[str, Any],
    hypothesis: Dict[str, Any],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    matched_simulation_runs_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    load_existing: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """Run Stage 4 independently for each selected hypothesized causal variable."""
    llm_semaphore = asyncio.Semaphore(max(1, int(config.get("max_concurrent", 5))))

    async def run_one(
        hypothesis_id: str,
    ) -> tuple[str, Dict[str, Any] | None, Path, Exception | None]:
        hypothesis_run = matched_simulation_runs_by_id[hypothesis_id]
        experiment_dir = Path(hypothesis_run["experiment_dir"])
        review_dir = Path(hypothesis_run["review_dir"])
        logger.info(
            "Reviewing %s (%s).",
            hypothesis_id,
            matched_configurations_by_id[hypothesis_id].get("variable"),
        )
        try:
            review = await run_blind_review(
                config=config,
                results_dir=experiment_dir,
                hypothesis=hypothesis,
                config_design=dict(matched_configurations_by_id[hypothesis_id]),
                simulation=hypothesis_run["simulation_stub"],
                llm_semaphore=llm_semaphore,
                load_existing=load_existing,
            )
            return hypothesis_id, review, review_dir, None
        except Exception as exc:
            return hypothesis_id, None, review_dir, exc

    blind_reviews_by_id: Dict[str, Dict[str, Any]] = {}
    for hypothesis_id, review, review_dir, error in await asyncio.gather(
        *(run_one(slug) for slug in selected_hypothesis_ids)
    ):
        if error is not None:
            logger.warning("[%s] review failed: %s", hypothesis_id, error)
            continue
        if review is not None:
            blind_reviews_by_id[hypothesis_id] = review
            source = "loaded/updated in" if load_existing else "saved into"
            logger.info("[%s] review %s %s", hypothesis_id, source, review_dir)
    return blind_reviews_by_id
