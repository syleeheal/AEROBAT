"""Centralized transcript and stage-artifact handling for Aerobat."""

from __future__ import annotations

from copy import deepcopy
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping

from aerobat.protocol.constants import (
    HYPOTHESIS_KEYS,
    PROMPT_CALL_KEYS,
    RUBRIC_ROW_KEYS,
    TOKEN_TOTAL_KEYS,
)
from aerobat.storage.ids import RunId
from aerobat.storage.artifacts import (
    HYPOTHESIS_GENERATION,
    MATCHED_CONFIGURATIONS,
    MATCHED_SIMULATION_RUNS,
    RESEARCH_REPORT_JSON,
    RESEARCH_REPORT_MARKDOWN,
    STATISTICAL_ANALYSIS,
    canonical_filename,
)
from aerobat.storage.schema import canonical_artifact, runtime_artifact
from aerobat.protocol.normalization import NormalizationManager
from aerobat.protocol.payloads import PayloadManager
from aerobat.utils import load_json, save_json


class TranscriptManager:
    def __init__(self, results_dir: str | Path):
        self.results_dir = Path(results_dir)

    @staticmethod
    def build_prompt_record(
        round_number: int,
        input_text: str,
        output_text: str,
        **extra: Any,
    ) -> Dict[str, Any]:
        extra.pop("response_id", None)
        record = {
            "round": round_number,
            "input": input_text,
            "output": output_text,
            **extra,
        }
        return record

    @classmethod
    def build_token_counts(
        cls,
        *,
        prompts: Any = None,
        research_manager_prompt: Any = None,
    ) -> Dict[str, Any]:
        calls: List[Dict[str, Any]] = []
        totals = cls._empty_token_totals()
        by_agent: Dict[str, Dict[str, int]] = {}

        for source, default_agent, fixed_agent in (
            (prompts, "stage_agent", None),
            (research_manager_prompt, "research_manager", "research_manager"),
        ):
            for agent, record in cls._prompt_call_records(source, default_agent=default_agent):
                cls._append_token_call(calls, totals, by_agent, fixed_agent or agent, record)

        return {
            "total": totals,
            "by_agent": by_agent,
            "calls": calls,
        }

    @staticmethod
    def _empty_token_totals() -> Dict[str, int]:
        return {key: 0 for key in TOKEN_TOTAL_KEYS}

    @staticmethod
    def _prompt_call_records(prompts: Any, *, default_agent: str) -> List[tuple[str, Dict[str, Any]]]:
        if isinstance(prompts, dict):
            return [
                (str(agent), row)
                for agent, records in prompts.items()
                if isinstance(records, list)
                for row in records
                if isinstance(row, dict) and isinstance(row.get("token_counts"), dict)
            ]
        if isinstance(prompts, list):
            return [
                (default_agent, row)
                for row in prompts
                if isinstance(row, dict) and isinstance(row.get("token_counts"), dict)
            ]
        return []

    @staticmethod
    def _append_token_call(
        calls: List[Dict[str, Any]],
        totals: Dict[str, int],
        by_agent: Dict[str, Dict[str, int]],
        agent: str,
        record: Dict[str, Any],
    ) -> None:
        counts = {
            key: int(value)
            for key, value in record.get("token_counts", {}).items()
            if key in TOKEN_TOTAL_KEYS and isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        if not counts:
            return

        agent_totals = by_agent.setdefault(agent, TranscriptManager._empty_token_totals())
        for key, value in counts.items():
            totals[key] += value
            agent_totals[key] += value

        call = {"agent": agent, **counts}
        call.update(
            {key: record[key] for key in PROMPT_CALL_KEYS if key in record and key != "response_id"}
        )
        calls.append(call)

    @classmethod
    def storage_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = deepcopy(payload)
        for key in ("prompts", "research_manager_prompt"):
            if key in payload:
                payload[key] = cls._strip_prompt_token_counts(payload[key])
        return cls._place_token_counts_before_prompts(payload)

    @staticmethod
    def _place_token_counts_before_prompts(payload: Dict[str, Any]) -> Dict[str, Any]:
        if "token_counts" not in payload or "prompts" not in payload:
            return payload
        ordered: Dict[str, Any] = {}
        for key, value in payload.items():
            if key == "token_counts":
                continue
            if key == "prompts":
                ordered["token_counts"] = payload["token_counts"]
            ordered[key] = value
        return ordered

    @classmethod
    def _strip_prompt_token_counts(cls, prompts: Any) -> Any:
        if isinstance(prompts, list):
            return [
                cls._stored_prompt_record(record)
                if isinstance(record, dict)
                else record
                for record in prompts
            ]
        if isinstance(prompts, dict):
            return {
                agent: cls._strip_prompt_token_counts(records)
                for agent, records in prompts.items()
            }
        return prompts

    @staticmethod
    def _stored_prompt_record(record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: value
            for key, value in record.items()
            if key not in {"token_counts", "response_id"}
        }

    def save_stage_output(self, filename: str, payload: Dict[str, Any]) -> Path:
        path = self.results_dir / canonical_filename(filename)
        stored = self.storage_payload(payload)
        save_json(canonical_artifact(filename, stored), path)
        return path

    @staticmethod
    def domain_slug(value: Any) -> str:
        if isinstance(value, (list, tuple)):
            value = value[0] if value else ""
        return NormalizationManager.slugify(value) or "domain"

    @classmethod
    def domain_slug_from_simulation(cls, simulation: Dict[str, Any]) -> str:
        return str(simulation.get("domain_slug") or cls.domain_slug(simulation.get("domain")))

    def simulation_path(self, run: RunId) -> Path:
        return self.results_dir / run.domain_slug / "simulations" / run.simulation_filename

    def review_path(self, run: RunId) -> Path:
        return self.results_dir / run.domain_slug / "reviews" / run.review_filename

    def save_simulation_transcript(
        self,
        *,
        transcript: Dict[str, Any],
        run: RunId,
    ) -> Dict[str, Any]:
        """Write one transcript and return its manifest row."""
        path = self.simulation_path(run)
        stored = self.storage_payload(transcript)
        save_json(canonical_artifact(path.name, stored), path)
        metadata = transcript.get("metadata", {}) if isinstance(transcript, dict) else {}
        return {
            **run.as_dict(),
            "causal_value": metadata.get("causal_value"),
            "environment_rendering_format": (
                metadata.get("environment_rendering_format")
                or metadata.get("simulation_format")
            ),
        }

    @staticmethod
    def build_simulation_manifest(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "runs": sorted(
                entries,
                key=lambda row: (
                    row["domain_slug"],
                    row["group_index"],
                    row["value_index"],
                    row["repetition"],
                ),
            )
        }

    @staticmethod
    def metadata_matches(meta_data: Any, expected: Dict[str, Any]) -> bool:
        return isinstance(meta_data, dict) and all(
            meta_data.get(key) == value for key, value in expected.items()
        )

    @staticmethod
    def _mapping_records(value: Any) -> List[Dict[str, Any]]:
        return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []

    @classmethod
    def hypothesis_artifact_current(
        cls,
        payload: Any,
        expected_metadata: Dict[str, Any],
    ) -> bool:
        return (
            isinstance(payload, dict)
            and HYPOTHESIS_KEYS.issubset(payload)
            and cls.metadata_matches(payload.get("meta_data"), expected_metadata)
            and cls.has_system_prompt_record(payload.get("prompts"))
            and cls.behavior_eval_rubric_current(payload.get("behavior_eval_rubric"))
            and cls.hypotheses_have_scored_ranges(payload.get("hypotheses"))
        )

    @staticmethod
    def has_system_prompt_record(prompts: Any) -> bool:
        return isinstance(prompts, list) and any(
            isinstance(row, dict) and bool(row.get("system")) for row in prompts
        )

    @classmethod
    def behavior_eval_rubric_current(cls, rubric: Any) -> bool:
        if not isinstance(rubric, list) or not rubric:
            return False
        if not all(isinstance(row, dict) and set(row) == RUBRIC_ROW_KEYS for row in rubric):
            return False

        numeric_rows = [
            row
            for row in rubric
            if isinstance(row.get("score"), int) and not isinstance(row.get("score"), bool)
        ]
        no_evidence_rows = [
            row
            for row in rubric
            if row.get("score") is None
            and NormalizationManager.text_value(row.get("level")).lower() == "no evidence"
        ]
        return bool(numeric_rows) and len(no_evidence_rows) == 1

    @classmethod
    def hypotheses_have_scored_ranges(cls, hypotheses: Any) -> bool:
        records = cls._mapping_records(hypotheses)
        return bool(records) and all(
            NormalizationManager.scored_range(row.get("var_range")) for row in records
        )

    @classmethod
    def stage_one_reviews_current(cls, hypotheses: Any) -> bool:
        records = cls._mapping_records(hypotheses)
        return bool(records) and all(
            isinstance((review := row.get("research_manager_review")), dict)
            and (review.get("rank") is None or isinstance(review.get("rank"), int))
            and isinstance(review.get("passes_stage2"), bool)
            for row in records
        )

    @classmethod
    def config_design_artifact_current(
        cls,
        payload: Any,
        expected_metadata: Dict[str, Any],
    ) -> bool:
        return (
            isinstance(payload, dict)
            and "domain_results" in payload
            and "behavior_eval_rubric" not in payload
            and "hypothesis" not in payload
            and cls.metadata_matches(payload.get("meta_data"), expected_metadata)
        )

    @classmethod
    def config_design_reviews_current(cls, domain_results: Any) -> bool:
        records = cls._mapping_records(domain_results)
        return bool(records) and all(cls._domain_reviews_current(row) for row in records)

    @staticmethod
    def _domain_reviews_current(domain_result: Dict[str, Any]) -> bool:
        pass_three_by_tag = domain_result.get("pass_three")
        return isinstance(pass_three_by_tag, dict) and bool(pass_three_by_tag) and all(
            isinstance(pass_three, dict)
            and isinstance(pass_three.get("research_manager_review"), dict)
            and isinstance(pass_three["research_manager_review"].get("rating"), str)
            and isinstance(pass_three.get("passes_stage3"), bool)
            for pass_three in pass_three_by_tag.values()
        )

    def save_matched_simulation_runs(
        self,
        *,
        transcript_entries: List[Dict[str, Any]],
        num_reps: int,
        num_rounds: int,
        environment_rendering_formats: List[str],
    ) -> Dict[str, Any]:
        meta_path = self.results_dir / MATCHED_SIMULATION_RUNS
        payload = self.build_simulation_manifest(transcript_entries)
        payload.update(
            {
                "num_reps": num_reps,
                "num_rounds": num_rounds,
                "environment_rendering_formats": environment_rendering_formats,
            }
        )
        self.save_stage_output(MATCHED_SIMULATION_RUNS, payload)
        return {
            "meta_path": meta_path,
            "simulation_stub": {"manifest_path": str(meta_path)},
        }

    @classmethod
    def load_matched_simulation_runs(
        cls,
        *,
        results_dir: str | Path,
        hypothesis_id: str,
        config_design: Dict[str, Any],
        num_rounds_fallback: Any = None,
    ) -> Dict[str, Any] | None:
        experiment_dir = Path(results_dir) / hypothesis_id

        meta_path = experiment_dir / MATCHED_SIMULATION_RUNS
        if not meta_path.exists():
            return None

        payload = runtime_artifact(meta_path.name, load_json(meta_path))
        selected_simulations = PayloadManager.simulation_entries_from_config_design(config_design)
        executed = {
            (run["domain_slug"], run["group_index"], run["value_index"])
            for run in payload.get("runs", [])
            if isinstance(run, dict)
        }
        if executed:
            selected_simulations = [
                simulation
                for simulation in selected_simulations
                if (simulation.get("domain_slug"), simulation.get("group_index"),
                    simulation.get("value_index")) in executed
            ]

        return {
            "experiment_dir": experiment_dir,
            "simulation_dir": experiment_dir,
            "review_dir": experiment_dir,
            "selected_simulations": selected_simulations,
            "selected_groups": PayloadManager.simulation_groups(selected_simulations),
            "num_rounds": payload.get("num_rounds") or num_rounds_fallback,
            "runs": payload.get("runs", []),
            "simulation_stub": {"manifest_path": str(meta_path)},
            "meta_path": meta_path,
        }

    def load_simulation_inputs(
        self,
        simulation: Dict[str, Any] | None = None,
    ) -> List[tuple[Dict[str, Any], Dict[str, Any]]]:
        meta_path = self._resolve_meta_path(simulation)
        if meta_path is not None:
            transcripts = self._load_simulation_inputs_from_meta(meta_path)
            if transcripts:
                return transcripts

        transcript_files = sorted(self.results_dir.glob("*/simulations/simulation_i*_j*_rep*.json"))
        transcripts = []
        for path in transcript_files:
            payload = runtime_artifact(path.name, load_json(path))
            transcripts.append(
                (
                    {**self._parse_transcript_path(path), "transcript_path": str(path)},
                    payload,
                )
            )
        return transcripts

    def _resolve_meta_path(self, simulation: Dict[str, Any] | None) -> Path | None:
        meta_raw = simulation.get("manifest_path") if isinstance(simulation, dict) else None
        return Path(str(meta_raw)) if meta_raw else None

    def _load_simulation_inputs_from_meta(
        self,
        meta_path: Path,
    ) -> List[tuple[Dict[str, Any], Dict[str, Any]]]:
        entries = self._load_meta_entries(meta_path)
        transcripts: List[tuple[Dict[str, Any], Dict[str, Any]]] = []
        for entry in entries:
            try:
                run = RunId.from_mapping(entry)
            except Exception:
                continue
            path = self.simulation_path(run)
            if not path.exists():
                continue
            transcripts.append((self.run_context(run), runtime_artifact(path.name, load_json(path))))
        return transcripts

    @staticmethod
    def run_context(run: RunId) -> Dict[str, Any]:
        """The four manuscript coordinates carried between Stages 3 and 4."""
        return run.as_dict()

    def _load_meta_entries(self, path: Path) -> List[Dict[str, Any]]:
        payload = runtime_artifact(path.name, load_json(path))
        runs = payload.get("runs", []) if isinstance(payload, dict) else []
        if not isinstance(runs, list):
            raise ValueError(f"Invalid simulation meta format: {path}")
        return [run for run in runs if isinstance(run, dict)]

    def _parse_transcript_path(self, path: Path) -> Dict[str, Any]:
        """The filename carries i, j and r; the parent-of-parent directory carries the domain."""
        return self.run_context(RunId.from_filename(path.name, path.parent.parent.name))

    def final_report_path(self) -> Path:
        return self.results_dir / RESEARCH_REPORT_MARKDOWN

    def final_report_metadata_path(self) -> Path:
        return self.results_dir / RESEARCH_REPORT_JSON

    def statistical_analysis_path(self, hypothesis_key: str) -> Path:
        return self.results_dir / hypothesis_key / STATISTICAL_ANALYSIS

    def load_statistical_analysis(self, hypothesis_key: str) -> Dict[str, Any] | None:
        path = self.statistical_analysis_path(hypothesis_key)
        if not path.exists():
            return None
        payload = runtime_artifact(path.name, load_json(path))
        return payload if isinstance(payload, dict) else None

    @classmethod
    def json_ready(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(key): cls.json_ready(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls.json_ready(item) for item in value]
        if isinstance(value, Path):
            return str(value)
        if hasattr(value, "item") and callable(value.item):
            try:
                return cls.json_ready(value.item())
            except Exception:
                pass
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return value

    def save_statistical_analyses(
        self,
        *,
        results_by_hypothesis: Mapping[str, Mapping[str, Any]],
    ) -> List[Path]:
        paths = []
        for hypothesis_key, result in results_by_hypothesis.items():
            path = self.statistical_analysis_path(str(hypothesis_key))
            payload = dict(result)
            payload.pop("hypothesis", None)
            stored = self.storage_payload(self.json_ready(payload))
            save_json(canonical_artifact(path.name, stored), path)
            paths.append(path)
        return paths

    def load_final_report_output(self) -> Dict[str, Any] | None:
        metadata_path = self.final_report_metadata_path()
        report_path = self.final_report_path()
        if metadata_path.exists():
            payload = runtime_artifact(metadata_path.name, load_json(metadata_path))
            if isinstance(payload, dict):
                payload["report"] = self.final_report_payload(payload.get("report"))
                return payload
        if report_path.exists():
            return {
                "report": self.final_report_payload(report_path.read_text(encoding="utf-8")),
            }
        return None

    def load_stage4_outputs(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        try:
            path = self.review_path(RunId.from_mapping(context))
        except (KeyError, ValueError):
            return None
        if not path.exists():
            return None
        payload = runtime_artifact(path.name, load_json(path))
        if not isinstance(payload.get("behavior_eval"), dict):
            return None
        return payload

    @staticmethod
    def stage4_review_entry(
        *,
        run: RunId,
        behavior_eval: Dict[str, Any] | None = None,
        prompts: List[Dict[str, Any]] | None = None,
        fallbacks: List[Dict[str, Any]] | None = None,
    ) -> Dict[str, Any]:
        entry = TranscriptManager.run_context(run)
        if isinstance(behavior_eval, dict):
            entry["behavior_eval"] = behavior_eval
        entry.update(
            {
                "token_counts": TranscriptManager.build_token_counts(prompts=prompts),
                "prompts": list(prompts or []),
                "fallbacks": list(fallbacks or []),
            }
        )
        return entry

    def save_stage4_outputs(self, record: Dict[str, Any], entry: Dict[str, Any]) -> None:
        try:
            run = RunId.from_mapping(record.get("context", {}))
        except (KeyError, ValueError):
            return
        path = self.review_path(run)
        stored = self.storage_payload(entry)
        save_json(canonical_artifact(path.name, stored), path)

    def save_final_report_output(self, entry: Dict[str, Any]) -> Path:
        report_path = self.final_report_path()
        metadata_path = self.final_report_metadata_path()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(self.final_report_markdown(entry), encoding="utf-8")
        metadata = dict(entry)
        metadata["report"] = self.final_report_payload(metadata.get("report"))
        for key in ("quantitative_analysis", "analytic_results", "path", "metadata_path"):
            metadata.pop(key, None)
        stored = self.storage_payload(metadata)
        save_json(canonical_artifact(metadata_path.name, stored), metadata_path)
        return report_path

    @staticmethod
    def final_report_payload(report: Any) -> List[str]:
        if isinstance(report, list):
            return [str(item) for item in report if item is not None]
        if report is None:
            return []
        return [str(report)]

    @staticmethod
    def final_report_text(report: Any) -> str:
        if isinstance(report, list):
            return "\n\n".join(str(item).strip() for item in report if item is not None).strip()
        return str(report or "").strip()

    @staticmethod
    def final_report_markdown(entry: Dict[str, Any]) -> str:
        title = str(entry.get("variable") or entry.get("axis_slug") or "Research Report").strip()
        behavior_name = str(entry.get("behavior_name") or "").strip()
        report = TranscriptManager.final_report_text(entry.get("report"))
        lines = [f"# Research Report: {title}", ""]
        if behavior_name:
            lines.extend([f"**Behavior:** {behavior_name}", ""])
        lines.append(report)
        return "\n".join(lines).rstrip() + "\n"
