"""Small public surface for the camera-ready analysis package."""

from .results import analyze_hypothesis, build_observation_rows, load_behavioral_findings
from .effects import MonotoneAnalysisOptions, analyze_hypothesis_effect

__all__ = [
    "MonotoneAnalysisOptions",
    "analyze_hypothesis",
    "build_observation_rows",
    "analyze_hypothesis_effect",
    "load_behavioral_findings",
]
