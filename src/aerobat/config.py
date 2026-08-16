"""Typed experiment configuration.

The public YAML stays intentionally small.  Stage-specific model options are kept in
``AgentCallConfig`` so every LLM call follows the same configuration path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

import yaml


@dataclass(frozen=True)
class AgentCallConfig:
    """Model options for one paper-named agent call."""

    model: str
    temperature: float = 1.0
    max_tokens: int = 15_000
    reasoning_effort: str | None = None
    service_tier: str | None = None

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
        *,
        default_model: str,
    ) -> "AgentCallConfig":
        return cls(
            model=str(value.get("model", default_model)),
            temperature=float(value.get("temperature", 1.0)),
            max_tokens=int(value.get("max_tokens", 15_000)),
            reasoning_effort=value.get("reasoning_effort"),
            service_tier=value.get("service_tier"),
        )


@dataclass(frozen=True)
class ExperimentConfig:
    target_behavior: str
    target_behavior_description: str
    results_dir: Path
    data_dir: Path
    hypothesis_generator: AgentCallConfig
    configuration_designer: AgentCallConfig
    simulator_agent: AgentCallConfig
    subject_agent: AgentCallConfig
    blind_reviewer: AgentCallConfig
    research_manager: AgentCallConfig
    num_hypotheses: int = 20
    num_domains: int = 3
    num_selected_hypotheses: int = 5
    num_matched_groups_per_domain: int = 5
    num_repetitions: int = 1
    max_concurrent: int = 10
    research_manager_gates: Mapping[str, bool] = field(default_factory=dict)
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @property
    def target_behavior_dir(self) -> Path:
        return self.results_dir / self.target_behavior


def _section(data: Mapping[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name, {})
    if not isinstance(value, Mapping):
        raise ValueError(f"{name!r} must be a YAML mapping")
    return dict(value)


def load_raw_config(path: str | Path) -> dict[str, Any]:
    """Load the shared YAML representation used by the stage implementations."""
    config_path = Path(path).resolve()
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, Mapping):
        raise ValueError("experiment configuration must be a YAML mapping")
    return dict(data)


def load_config(path: str | Path) -> ExperimentConfig:
    """Load and validate the compact public experiment configuration."""
    config_path = Path(path).resolve()
    data = load_raw_config(config_path)

    root = config_path.parent
    behavior = _section(data, "behavior")
    hypothesis = _section(data, "hypothesis")
    design = _section(data, "config_design")
    simulation = _section(data, "simulation")
    review = _section(data, "review")
    manager = _section(data, "research_manager")
    manager_stage_config = _section(manager, "stages") if manager.get("stages") else {}
    manager_stages = {
        name: bool((settings or {}).get("enabled", False))
        for name, settings in manager_stage_config.items()
        if isinstance(settings, Mapping)
    }

    default_model = "openai/gpt-5.1"
    subject_data = {
        "model": simulation.get("subject_agent_model", "openai/gpt-5-mini"),
        "temperature": simulation.get("subject_agent_temperature", 1.0),
        "max_tokens": simulation.get("subject_agent_max_tokens", 5_000),
        "reasoning_effort": simulation.get("subject_agent_reasoning_effort"),
        "service_tier": simulation.get("subject_agent_service_tier"),
    }
    simulator_data = {
        "model": simulation.get("simulator_agent_model", default_model),
        "temperature": simulation.get("simulator_agent_temperature", 1.0),
        "max_tokens": simulation.get("simulator_agent_max_tokens", 15_000),
        "reasoning_effort": simulation.get("simulator_agent_reasoning_effort"),
        "service_tier": simulation.get("simulator_agent_service_tier"),
    }
    name = str(behavior.get("name", "")).strip()
    if not name:
        raise ValueError("behavior.name must not be empty")

    return ExperimentConfig(
        target_behavior=name,
        target_behavior_description=str(behavior.get("description", "")).strip(),
        results_dir=(root / str(data.get("results_dir", "results/GPT-5-mini"))).resolve(),
        data_dir=(root / str(data.get("data_dir", "."))).resolve(),
        hypothesis_generator=AgentCallConfig.from_mapping(
            hypothesis,
            default_model=default_model,
        ),
        configuration_designer=AgentCallConfig.from_mapping(
            design,
            default_model=default_model,
        ),
        simulator_agent=AgentCallConfig.from_mapping(
            simulator_data,
            default_model=default_model,
        ),
        subject_agent=AgentCallConfig.from_mapping(
            subject_data,
            default_model="openai/gpt-5-mini",
        ),
        blind_reviewer=AgentCallConfig.from_mapping(
            review,
            default_model=default_model,
        ),
        research_manager=AgentCallConfig.from_mapping(
            manager,
            default_model=default_model,
        ),
        num_hypotheses=int(hypothesis.get("num_hypotheses", 20)),
        num_domains=int(hypothesis.get("num_domains", 3)),
        num_selected_hypotheses=int(hypothesis.get("num_stage2_hypotheses", 5)),
        num_matched_groups_per_domain=int(design.get("num_value_sets", 5)),
        num_repetitions=int(simulation.get("num_reps", 1)),
        max_concurrent=int(data.get("max_concurrent", 10)),
        research_manager_gates=manager_stages,
        raw=dict(data),
    )
