"""AEROBAT Stage 2: matched-configuration design for each hypothesis."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Sequence

from aerobat.protocol.constants import (
    DEFAULT_NUM_VALUE_SETS,
)
from aerobat.protocol.normalization import NormalizationManager
from aerobat.runtime.cache import settings_with_cache_key
from aerobat.runtime.llm import (
    LLMResponse,
    llm_call_with_metadata,
    llm_call_kwargs,
    resolve_stage_llm_settings,
)
from aerobat.protocol.prompts import ConfigurationDesignerPrompts
from aerobat.protocol.stage_parsing import (
    parse_environment_rendering_format,
    parse_pass_one,
    parse_pass_three,
    parse_pass_two,
)
from aerobat.protocol.payloads import PayloadManager
from aerobat.runtime.concurrency import gather_after_first
from aerobat.storage.ids import RunId
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import collect_fallbacks, research_manager_gate_enabled

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConfigurationPassExchange:
    """One prompt/response pair retained in the Stage 2 artifact."""

    prompt: str
    response: str
    token_counts: Dict[str, Any] | None
    response_id: str

    @classmethod
    def from_response(cls, prompt: str, response: LLMResponse) -> "ConfigurationPassExchange":
        return cls(prompt, response.text, response.token_counts, response.response_id)


@dataclass
class HypothesisDomainDesign:
    """In-memory state carried through the three prescribed Stage 2 passes."""

    domain: str
    stage1_context: Dict[str, Any]
    environment_rendering_format: str = ""
    pass_one: Dict[str, Any] = field(default_factory=dict)
    pass_two: Dict[str, Any] = field(default_factory=dict)
    pass_three: Dict[str, Any] = field(default_factory=dict)
    exchanges: Dict[int, ConfigurationPassExchange] = field(default_factory=dict)
    pass_three_records: List[Dict[str, Any]] = field(default_factory=list)

    def artifact(self) -> Dict[str, Any]:
        pass_one = self.exchanges[1]
        pass_two = self.exchanges[2]
        prompts = [
            TranscriptManager.build_prompt_record(
                1,
                pass_one.prompt,
                pass_one.response,
                source="pass_one",
                environment_rendering_format=self.environment_rendering_format,
                token_counts=pass_one.token_counts,
                response_id=pass_one.response_id,
            ),
            TranscriptManager.build_prompt_record(
                2,
                pass_two.prompt,
                pass_two.response,
                source="pass_two",
                token_counts=pass_two.token_counts,
                response_id=pass_two.response_id,
            ),
            *self.pass_three_records,
        ]
        return {
            "domain": self.domain,
            "environment_rendering_format": self.environment_rendering_format,
            "pass_one": self.pass_one,
            "pass_two": self.pass_two,
            "pass_three": self.pass_three,
            "prompts": prompts,
            "research_manager_prompt": [],
            "research_manager_fallbacks": [],
        }


def hypothesis_slug(variable_name: str) -> str:
    slug = NormalizationManager.slugify(variable_name)
    if not slug:
        raise ValueError(f"variable name yields empty slug: {variable_name!r}")
    return slug


def simulations_by_run(config_design: Dict[str, Any]) -> Dict[tuple, Dict[str, Any]]:
    """Return Stage 2 simulation specifications keyed by domain, group, and value."""
    return {
        RunId.from_mapping(simulation).key: simulation
        for simulation in PayloadManager.simulation_entries_from_config_design(config_design)
        if isinstance(simulation, dict)
    }


def resolve_max_concurrent(config: Dict[str, Any]) -> int:
    return int(config.get("max_concurrent", 5))


def resolve_num_matched_groups(config: Dict[str, Any]) -> int:
    config_design_cfg = config.get("config_design", {})
    if not isinstance(config_design_cfg, dict):
        config_design_cfg = {}
    return int(config_design_cfg.get("num_value_sets", DEFAULT_NUM_VALUE_SETS))


def _hypothesis_domains(hypothesis: Dict[str, Any]) -> List[str]:
    domains = hypothesis.get("domain", [])
    if isinstance(domains, str):
        domains = [domains]
    return [str(domain).strip() for domain in domains if str(domain).strip()]


def _stage1_for_domain(
    stage1_hypothesis: Dict[str, Any],
    variable_hypothesis: Dict[str, Any],
    domain: str,
) -> Dict[str, Any]:
    narrowed_hypothesis = {**variable_hypothesis, "domain": [domain]}
    return {
        "behavior_name": stage1_hypothesis["behavior_name"],
        "definition": stage1_hypothesis.get("definition", ""),
        "behavior_eval_rubric": stage1_hypothesis.get("behavior_eval_rubric", []),
        "hypotheses": [narrowed_hypothesis],
    }


async def _call_prompts_with_cache_warmup(
    *,
    system_prompt: str,
    prompts: Sequence[str],
    settings: Any,
    semaphore: asyncio.Semaphore,
) -> List[LLMResponse]:
    async def call(prompt: str) -> LLMResponse:
        async with semaphore:
            return await llm_call_with_metadata(
                PayloadManager.messages(system_prompt, prompt),
                **llm_call_kwargs(settings),
            )

    responses = await gather_after_first(
        list(prompts),
        call,
    )
    return list(responses)  # return_exceptions=False guarantees LLMResponse values.


async def _run_domains_by_pass(
    *,
    config: Dict[str, Any],
    stage1_hypothesis: Dict[str, Any],
    variable_hypothesis: Dict[str, Any],
    domains: Sequence[str],
    semaphore: asyncio.Semaphore,
) -> List[Dict[str, Any]]:
    behavior_name = stage1_hypothesis["behavior_name"]
    settings = resolve_stage_llm_settings(
        config,
        "config_design",
        default_max_tokens=10000,
    )
    configured_value_set_tags = tuple(
        f"set_{index}" for index in range(1, resolve_num_matched_groups(config) + 1)
    )
    system_prompt = ConfigurationDesignerPrompts.make_system_prompt(behavior_name)
    domain_states = [
        HypothesisDomainDesign(
            domain=domain,
            stage1_context=_stage1_for_domain(
                stage1_hypothesis,
                variable_hypothesis,
                domain,
            ),
        )
        for domain in domains
    ]

    pass_one_prompts = [
        ConfigurationDesignerPrompts.pass_one(
            behavior_name,
            state.stage1_context,
        )
        for state in domain_states
    ]
    pass_one_responses = await _call_prompts_with_cache_warmup(
        system_prompt=system_prompt,
        prompts=pass_one_prompts,
        settings=settings_with_cache_key(
            settings,
            "s2",
            "config",
            behavior_name,
            variable_hypothesis.get("variable"),
            "pass1",
        ),
        semaphore=semaphore,
    )
    for state, prompt, llm_response in zip(domain_states, pass_one_prompts, pass_one_responses):
        exchange = ConfigurationPassExchange.from_response(prompt, llm_response)
        state.exchanges[1] = exchange
        state.pass_one = parse_pass_one(exchange.response)
        state.environment_rendering_format = parse_environment_rendering_format(exchange.response)

    pass_two_prompts = [
        ConfigurationDesignerPrompts.pass_two(
            behavior_name,
            state.stage1_context,
            state.pass_one,
            num_value_sets=len(configured_value_set_tags),
        )
        for state in domain_states
    ]
    pass_two_responses = await _call_prompts_with_cache_warmup(
        system_prompt=system_prompt,
        prompts=pass_two_prompts,
        settings=settings_with_cache_key(
            settings,
            "s2",
            "config",
            behavior_name,
            variable_hypothesis.get("variable"),
            "pass2",
        ),
        semaphore=semaphore,
    )
    for state, prompt, llm_response in zip(domain_states, pass_two_prompts, pass_two_responses):
        exchange = ConfigurationPassExchange.from_response(prompt, llm_response)
        state.exchanges[2] = exchange
        state.pass_two = parse_pass_two(
            exchange.response,
            value_set_tags=configured_value_set_tags,
        )

    pass_three_items = []
    for state in domain_states:
        for value_set_tag in configured_value_set_tags:
            pass_two = state.pass_two
            pass_two_context = {
                "fixed_values": pass_two.get(value_set_tag, {}),
                "covariance_structure": pass_two.get("covariance_structure", {}),
                "potential_interactions": pass_two.get("potential_interactions", {}),
                "problematic_combinations": pass_two.get("problematic_combinations", {}),
            }
            prompt = ConfigurationDesignerPrompts.pass_three(
                behavior_name,
                variable_hypothesis.get("var_dimension", ""),
                state.stage1_context,
                state.pass_one,
                pass_two_context,
            )
            pass_three_items.append((state, value_set_tag, prompt))

    pass_three_responses = await _call_prompts_with_cache_warmup(
        system_prompt=system_prompt,
        prompts=[item[2] for item in pass_three_items],
        settings=settings_with_cache_key(
            settings,
            "s2",
            "config",
            behavior_name,
            variable_hypothesis.get("variable"),
            "pass3",
        ),
        semaphore=semaphore,
    )
    for (state, value_set_tag, prompt), llm_response in zip(pass_three_items, pass_three_responses):
        exchange = ConfigurationPassExchange.from_response(prompt, llm_response)
        state.pass_three[value_set_tag] = parse_pass_three(exchange.response)
        state.pass_three_records.append(
            TranscriptManager.build_prompt_record(
                3,
                exchange.prompt,
                exchange.response,
                source=f"pass_three_{value_set_tag}",
                value_set_tag=value_set_tag,
                token_counts=exchange.token_counts,
                response_id=exchange.response_id,
            )
        )
    return [state.artifact() for state in domain_states]


async def design_matched_configurations_for_hypothesis(
    config: Dict[str, Any],
    variable_dir: Path,
    stage1_hypothesis: Dict[str, Any],
    variable_entry: Dict[str, Any],
    semaphore: asyncio.Semaphore,
) -> Dict[str, Any]:
    variable_name = variable_entry["variable"]
    slug = hypothesis_slug(variable_name)
    domains = _hypothesis_domains(variable_entry)
    if not domains:
        raise ValueError(f"Hypothesis {variable_name!r} has no domains.")

    settings = resolve_stage_llm_settings(
        config,
        "config_design",
        default_max_tokens=10000,
    )
    domain_results: List[Dict[str, Any]] = []
    prompts: List[Dict[str, Any]] = []
    research_manager_prompt: List[Dict[str, Any]] = []
    research_manager_fallbacks: List[Dict[str, Any]] = []

    with collect_fallbacks() as fallbacks:
        results = await _run_domains_by_pass(
            config=config,
            stage1_hypothesis=stage1_hypothesis,
            variable_hypothesis=variable_entry,
            domains=domains,
            semaphore=semaphore,
        )
        for result in results:
            domain_results.append(
                {
                    "domain": result["domain"],
                    "environment_rendering_format": result["environment_rendering_format"],
                    "pass_one": result["pass_one"],
                    "pass_two": result["pass_two"],
                    "pass_three": result["pass_three"],
                }
            )
            for record in result["prompts"]:
                prompts.append({**record, "domain": result["domain"], "variable": variable_name})
            for record in result.get("research_manager_prompt", []):
                research_manager_prompt.append(
                    {
                        **record,
                        "domain": result["domain"],
                        "variable": variable_name,
                    }
                )
            research_manager_fallbacks.extend(result.get("research_manager_fallbacks", []))

        data = {
            "behavior_name": stage1_hypothesis["behavior_name"],
            "variable": variable_name,
            "axis_slug": slug,
            "meta_data": {
                "model": settings.model,
                "temperature": settings.temperature,
                "reasoning_effort": settings.reasoning_effort,
                "num_value_sets": resolve_num_matched_groups(config),
                "research_manager_stage_2": research_manager_gate_enabled(config, "stage_2"),
            },
            "domain_results": domain_results,
            "token_counts": TranscriptManager.build_token_counts(prompts=prompts),
            "prompts": prompts,
            "fallbacks": list(fallbacks),
            "research_manager_prompt": research_manager_prompt,
            "research_manager_fallbacks": research_manager_fallbacks,
        }

    transcript_manager = TranscriptManager(variable_dir)
    out_path = transcript_manager.save_stage_output("matched_configurations.json", data)
    logger.info("Matched configurations for hypothesized causal variable %s saved to %s", variable_name, out_path)
    data["path"] = str(out_path)
    data["hypothesis"] = variable_entry
    return data


async def design_matched_configurations(
    config: Dict[str, Any],
    results_dir: Path,
    stage1_hypothesis: Dict[str, Any],
) -> Dict[str, Any]:
    behavior_name = stage1_hypothesis["behavior_name"]
    stage1_research_manager_enabled = research_manager_gate_enabled(config, "stage_1")
    # Stage 2 only expands hypotheses approved by Stage 1 when that review is enabled.
    hypotheses = [
        variable_hypothesis
        for variable_hypothesis in stage1_hypothesis.get("hypotheses", [])
        if isinstance(variable_hypothesis, dict)
        and (
            not stage1_research_manager_enabled
            or PayloadManager.should_pass_hypothesis_to_stage2(variable_hypothesis)
        )
    ]
    if not hypotheses:
        raise ValueError(
            "No hypotheses selected for Stage 2 from Stage 1 research-manager "
            "review; nothing to design."
        )

    max_concurrent = resolve_max_concurrent(config)
    semaphore = asyncio.Semaphore(max_concurrent)

    logger.info(
        "Stage 2 — matched-configuration design: %s; hypotheses=%s max_concurrent=%s",
        behavior_name,
        len(hypotheses),
        max_concurrent,
    )

    # Create one config_design output per hypothesis variable while sharing the concurrency limit.
    tasks = []
    for variable_hypothesis in hypotheses:
        slug = hypothesis_slug(variable_hypothesis["variable"])
        variable_dir = results_dir / slug
        variable_dir.mkdir(parents=True, exist_ok=True)
        tasks.append(
            design_matched_configurations_for_hypothesis(
                config=config,
                variable_dir=variable_dir,
                stage1_hypothesis=stage1_hypothesis,
                variable_entry=variable_hypothesis,
                semaphore=semaphore,
            )
        )

    variable_results = await asyncio.gather(*tasks)
    return {
        "behavior_name": behavior_name,
        "variables": [
            {
                "variable": item["variable"],
                "axis_slug": item["axis_slug"],
                "path": item["path"],
                "config_design": item,
            }
            for item in variable_results
        ],
        "by_axis_slug": {item["axis_slug"]: item for item in variable_results},
    }
