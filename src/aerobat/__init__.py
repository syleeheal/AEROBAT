"""AEROBAT: automated behavioral research for language-model agents."""

from .config import AgentCallConfig, ExperimentConfig, load_config
from .pipeline import AerobatPipeline

__all__ = ["AerobatPipeline", "AgentCallConfig", "ExperimentConfig", "load_config"]
__version__ = "1.0.0"
