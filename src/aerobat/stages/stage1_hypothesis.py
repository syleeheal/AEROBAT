"""AEROBAT Stage 1: target-behavior specification and hypothesis generation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from aerobat.protocol.normalization import NormalizationManager
from aerobat.runtime.llm import (
    llm_call_with_metadata,
    llm_call_kwargs,
    resolve_stage_llm_settings,
)
from aerobat.protocol.prompts import HypothesisGeneratorPrompts
from aerobat.protocol.stage_parsing import parse_hypothesis_response
from aerobat.protocol.payloads import PayloadManager
from aerobat.storage.transcripts import TranscriptManager
from aerobat.utils import (
    collect_fallbacks,
    load_behavior_description,
    research_manager_gate_enabled,
)

logger = logging.getLogger(__name__)


async def generate_hypotheses(
    config: Dict[str, Any],
    results_dir: Path,
) -> Dict[str, Any]:
    """Analyze the target behavior and generate causal hypotheses."""
    with collect_fallbacks() as fallbacks:
        transcript_manager = TranscriptManager(results_dir)
        behavior = config["behavior"]
        behavior_fields = behavior if isinstance(behavior, dict) else {}
        behavior_name = NormalizationManager.text_value(behavior_fields.get("name", behavior))
        description = NormalizationManager.text_value(behavior_fields.get("description"))
        if not description:
            data_dir = config.get("data_dir", str(results_dir.parent.parent))
            description = load_behavior_description(behavior_name, data_dir)
            if description:
                logger.info("Loaded description from behaviors.json for %r.", behavior_name)

        stage_cfg = NormalizationManager.object_value(config.get("hypothesis"))
        settings = resolve_stage_llm_settings(
            config,
            "hypothesis",
            default_max_tokens=12000,
        )
        num_hypotheses = NormalizationManager.require_positive_int(
            stage_cfg.get("num_hypotheses", 20), "hypothesis.num_hypotheses"
        )
        num_domains = NormalizationManager.require_positive_int(
            stage_cfg.get("num_domains", 2), "hypothesis.num_domains"
        )
        num_stage2_hypotheses = NormalizationManager.require_positive_int(
            stage_cfg.get("num_stage2_hypotheses", num_hypotheses),
            "hypothesis.num_stage2_hypotheses",
        )

        logger.info("Stage 1 — hypothesis generation for target behavior: %s", behavior_name)
        logger.info("Model: %s", settings.model)

        system_prompt = HypothesisGeneratorPrompts.make_system_prompt()
        user_prompt = HypothesisGeneratorPrompts.make_hypothesis_prompt_patch(
            behavior_name,
            description,
            num_hypotheses=num_hypotheses,
            num_domains=num_domains,
        )

        logger.info("Calling the hypothesis generator for behavior specification and hypotheses H.")
        llm_response = await llm_call_with_metadata(
            PayloadManager.messages(system_prompt, user_prompt),
            **llm_call_kwargs(settings),
        )
        response = llm_response.text

        parsed_response = parse_hypothesis_response(response)
        definition = parsed_response["definition"]
        if description:
            definition = f"{definition}\n\nAdditional description\n{description}"
        behavior_eval_rubric = parsed_response["behavior_eval_rubric"]
        hypotheses = parsed_response["hypotheses"][:num_hypotheses]
        for hypothesis in hypotheses:
            hypothesis["domain"] = hypothesis.get("domain", [])[:num_domains]

        data = {
            "behavior_name": behavior_name,
            "meta_data": {
                "model": settings.model,
                "temperature": settings.temperature,
                "reasoning_effort": settings.reasoning_effort,
                "num_hypotheses": num_hypotheses,
                "num_domains": num_domains,
                "num_stage2_hypotheses": num_stage2_hypotheses,
                "research_manager_stage_1": research_manager_gate_enabled(config, "stage_1"),
            },
            "definition": definition,
            "behavior_eval_rubric": behavior_eval_rubric,
            "hypotheses": hypotheses,
            "token_counts": TranscriptManager.build_token_counts(
                prompts=[
                    {"system": system_prompt},
                    TranscriptManager.build_prompt_record(
                        1,
                        user_prompt,
                        response,
                        token_counts=llm_response.token_counts,
                        response_id=llm_response.response_id,
                    ),
                ],
            ),
            "prompts": [
                {"system": system_prompt},
                TranscriptManager.build_prompt_record(
                    1,
                    user_prompt,
                    response,
                    token_counts=llm_response.token_counts,
                    response_id=llm_response.response_id,
                ),
            ],
            "fallbacks": list(fallbacks),
            "research_manager_prompt": [],
            "research_manager_fallbacks": [],
        }

        out_path = transcript_manager.save_stage_output("hypothesis_generation.json", data)
        logger.info("Stage 1 artifact saved to: %s", out_path)
        logger.info("Hypotheses identified: %s", len(hypotheses))

        return data
