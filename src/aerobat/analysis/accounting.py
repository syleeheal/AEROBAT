"""Stage-owned gate and simulation-round accounting."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ..storage.artifacts import (
    MATCHED_CONFIGURATIONS,
    MATCHED_SIMULATION_RUNS,
    STATISTICAL_ANALYSIS,
    iter_hypothesis_dirs,
)
from ..storage.ids import RunId
from ..storage.schema import runtime_artifact
from ..storage.transcripts import TranscriptManager
from ..utils import load_json


def _configuration_groups(config: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        group
        for domain in config.get("domain_results", [])
        if isinstance(domain, Mapping)
        for group in (domain.get("pass_three") or {}).values()
        if isinstance(group, Mapping)
    ]


def _review_assessment(path: Path) -> Mapping[str, Any]:
    review = runtime_artifact(path.name, load_json(path))
    evaluation = review.get("behavior_eval") or {}
    assessment = evaluation.get("behavior_assessment") or {}
    return assessment if isinstance(assessment, Mapping) else {}


def _round_counts(transcript: Mapping[str, Any]) -> tuple[int, int, int]:
    rounds = [row for row in transcript.get("rounds", []) if isinstance(row, Mapping)]
    identifiers = [row.get("round") for row in rounds]
    unique_identifiers = set(identifiers)
    return len(rounds), len(unique_identifiers), len(rounds) - len(unique_identifiers)


def _round_totals(
    transcripts: list[tuple[RunId, Mapping[str, Any]]],
) -> tuple[int, int, int]:
    records = unique = duplicates = 0
    for _, transcript in transcripts:
        transcript_records, transcript_unique, transcript_duplicates = _round_counts(
            transcript
        )
        records += transcript_records
        unique += transcript_unique
        duplicates += transcript_duplicates
    return records, unique, duplicates


def stage_accounting(results_dir: str | Path) -> pd.DataFrame:
    """Return one row per hypothesis using records owned by each pipeline stage.

    Stage 2 groups own coherence decisions; Stage 3 transcripts own fidelity decisions
    and round records. Stage 3 round quantities cover every declared simulation, while
    Stage 4-eligible quantities cover only fidelity-passing simulations. Review and
    analysis counts remain separate so later attrition cannot alter an earlier stage.
    """
    rows: list[dict[str, Any]] = []
    for hypothesis_dir in iter_hypothesis_dirs(results_dir):
        config_path = hypothesis_dir / MATCHED_CONFIGURATIONS
        manifest_path = hypothesis_dir / MATCHED_SIMULATION_RUNS
        analysis_path = hypothesis_dir / STATISTICAL_ANALYSIS
        config = runtime_artifact(config_path.name, load_json(config_path))
        manifest = runtime_artifact(manifest_path.name, load_json(manifest_path))
        analysis = runtime_artifact(analysis_path.name, load_json(analysis_path))

        groups = _configuration_groups(config)
        coherence_passed = sum(group.get("passes_stage3") is True for group in groups)

        manager = TranscriptManager(hypothesis_dir)
        transcripts: list[tuple[RunId, Mapping[str, Any]]] = []
        seen_runs: set[RunId] = set()
        for entry in manifest.get("runs", []):
            if not isinstance(entry, Mapping):
                continue
            run = RunId.from_mapping(entry)
            if run in seen_runs:
                raise ValueError(f"Duplicate Stage 3 run in {manifest_path}: {run.label()}")
            seen_runs.add(run)
            path = manager.simulation_path(run)
            if not path.exists():
                raise FileNotFoundError(
                    f"Missing Stage 3 transcript declared by {manifest_path}: {path}"
                )
            transcripts.append((run, runtime_artifact(path.name, load_json(path))))

        passed = [
            (run, transcript)
            for run, transcript in transcripts
            if transcript.get("passes_stage4") is True
        ]
        configured_rounds = int(manifest.get("num_rounds") or 0) * len(transcripts)
        stage3_round_records, stage3_executed_rounds, stage3_duplicate_round_records = (
            _round_totals(transcripts)
        )
        nominal_rounds = int(manifest.get("num_rounds") or 0) * len(passed)
        round_records, unique_rounds, duplicate_round_records = _round_totals(passed)

        passed_ids = {run for run, _ in passed}
        review_paths = sorted(hypothesis_dir.glob("*/reviews/review_i*_j*_rep*.json"))
        eligible_review_paths = [
            path
            for path in review_paths
            if RunId.from_filename(path.name, path.parent.parent.name) in passed_ids
        ]
        parsed_assessments = sum(bool(_review_assessment(path)) for path in eligible_review_paths)

        rows.append(
            {
                "target_behavior": hypothesis_dir.parent.name,
                "hypothesis_id": hypothesis_dir.name,
                "coherence_reviewed_groups": len(groups),
                "coherence_passed_groups": coherence_passed,
                "coherence_excluded_groups": len(groups) - coherence_passed,
                "stage3_transcripts": len(transcripts),
                "stage3_configured_rounds": configured_rounds,
                "stage3_round_records": stage3_round_records,
                "stage3_executed_rounds": stage3_executed_rounds,
                "stage3_duplicate_round_records": stage3_duplicate_round_records,
                "stage3_unexecuted_rounds": configured_rounds - stage3_executed_rounds,
                "fidelity_passed_transcripts": len(passed),
                "fidelity_excluded_transcripts": len(transcripts) - len(passed),
                "stage4_review_outputs": len(eligible_review_paths),
                "stage4_parsed_assessments": parsed_assessments,
                "analysis_observations": len(analysis.get("behavior_eval_rows") or []),
                "stage4_eligible_nominal_rounds": nominal_rounds,
                "stage4_eligible_round_records": round_records,
                "stage4_eligible_unique_rounds": unique_rounds,
                "stage4_eligible_duplicate_round_records": duplicate_round_records,
            }
        )
    return pd.DataFrame(rows)


def stage_accounting_numbers(frame: pd.DataFrame) -> dict[str, Any]:
    """Aggregate a hypothesis-level accounting table without mixing stage boundaries."""
    coherence_reviewed = int(frame.coherence_reviewed_groups.sum())
    coherence_passed = int(frame.coherence_passed_groups.sum())
    fidelity_reviewed = int(frame.stage3_transcripts.sum())
    fidelity_passed = int(frame.fidelity_passed_transcripts.sum())
    hypotheses = len(frame)
    return {
        "coherence_gate_reviewed_groups": coherence_reviewed,
        "coherence_gate_passed_groups": coherence_passed,
        "coherence_gate_excluded_groups": coherence_reviewed - coherence_passed,
        "coherence_gate_pass_rate": coherence_passed / coherence_reviewed,
        "fidelity_gate_reviewed_transcripts": fidelity_reviewed,
        "fidelity_gate_passed_transcripts": fidelity_passed,
        "fidelity_gate_excluded_transcripts": fidelity_reviewed - fidelity_passed,
        "fidelity_gate_pass_rate": fidelity_passed / fidelity_reviewed,
        "stage3_configured_rounds": int(frame.stage3_configured_rounds.sum()),
        "stage3_round_records": int(frame.stage3_round_records.sum()),
        "stage3_executed_rounds": int(frame.stage3_executed_rounds.sum()),
        "stage3_duplicate_round_records": int(frame.stage3_duplicate_round_records.sum()),
        "stage3_unexecuted_rounds": int(frame.stage3_unexecuted_rounds.sum()),
        "stage4_review_outputs": int(frame.stage4_review_outputs.sum()),
        "stage4_parsed_assessments": int(frame.stage4_parsed_assessments.sum()),
        "n_analysis_observations": int(frame.analysis_observations.sum()),
        "stage4_eligible_nominal_rounds": int(frame.stage4_eligible_nominal_rounds.sum()),
        "stage4_eligible_round_records": int(frame.stage4_eligible_round_records.sum()),
        "stage4_eligible_unique_rounds": int(frame.stage4_eligible_unique_rounds.sum()),
        "stage4_eligible_duplicate_round_records": int(
            frame.stage4_eligible_duplicate_round_records.sum()
        ),
        "stage4_eligible_rounds_per_simulation_mean": (
            float(frame.stage4_eligible_nominal_rounds.sum()) / fidelity_passed
        ),
        "stage4_eligible_rounds_per_hypothesis_mean": (
            float(frame.stage4_eligible_nominal_rounds.sum()) / hypotheses
        ),
    }


def experiment_stage_accounting(results_dir: str | Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load and aggregate all stage-owned accounting records."""
    frame = stage_accounting(results_dir)
    return frame, stage_accounting_numbers(frame)
