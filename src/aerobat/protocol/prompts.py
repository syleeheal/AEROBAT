"""Public prompt namespaces for AEROBAT's agents and environment-fidelity tasks."""

from .prompt_templates.research_manager import ResearchManagerPrompts
from .prompt_templates.stage1 import HypothesisGeneratorPrompts
from .prompt_templates.stage2 import ConfigurationDesignerPrompts
from .prompt_templates.stage3 import MatchedSimulationPrompts
from .prompt_templates.stage4 import BlindReviewerPrompts
from .prompt_templates.environment_fidelity import EnvironmentFidelityPrompts

__all__ = [
    "ResearchManagerPrompts",
    "HypothesisGeneratorPrompts",
    "ConfigurationDesignerPrompts",
    "MatchedSimulationPrompts",
    "BlindReviewerPrompts",
    "EnvironmentFidelityPrompts",
]
