"""Canonical result-artifact names and paths."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

HYPOTHESIS_GENERATION = "hypothesis_generation.json"
MATCHED_CONFIGURATIONS = "matched_configurations.json"
MATCHED_SIMULATION_RUNS = "matched_simulation_runs.json"
STATISTICAL_ANALYSIS = "statistical_analysis.json"
SENSITIVITY_ANALYSIS = "sensitivity_analysis.json"
RESEARCH_REPORT_JSON = "research_report.json"
RESEARCH_REPORT_MARKDOWN = "research_report.md"

LEGACY_TO_CANONICAL = {
    "hypothesis.json": HYPOTHESIS_GENERATION,
    "config.json": MATCHED_CONFIGURATIONS,
    "simulation_meta.json": MATCHED_SIMULATION_RUNS,
    "analytic_results.json": STATISTICAL_ANALYSIS,
    "analytic_results_additional.json": SENSITIVITY_ANALYSIS,
    "final_report.json": RESEARCH_REPORT_JSON,
    "final_report.md": RESEARCH_REPORT_MARKDOWN,
}


def canonical_filename(filename: str) -> str:
    return LEGACY_TO_CANONICAL.get(filename, filename)


def iter_hypothesis_dirs(results_dir: str | Path) -> Iterator[Path]:
    """Yield hypothesis directories that contain a completed statistical analysis."""
    root = Path(results_dir)
    for path in sorted(root.glob(f"*/*/{STATISTICAL_ANALYSIS}")):
        yield path.parent
