"""Central payload construction for Aerobat stages."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from .constants import (
    DEFAULT_ENVIRONMENT_RENDERING_FORMAT,
    PLANNING_SECTION_TAGS,
    ROUND_KEYS,
    RULE_KEYS,
    SIMULATION_KEYS,
    STAGE2_REJECTED_CONFIG_RATINGS,
    VALUE_PLACEHOLDER_RE,
    VALUE_SET_TAGS,
)
from ..storage.ids import RunId
from .normalization import NormalizationManager
from .parsing import StringParser
from .formats import SIMULATION_FORMATS, get_format_spec
from aerobat.utils import record_fallback


class PayloadManager:
    """Build the payload views passed between stages and LLM calls."""

    @staticmethod
    def messages(system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    @staticmethod
    def chat_message(role: str, content: str) -> Dict[str, str]:
        return {"role": role, "content": content}

    @classmethod
    def subject_agent_state(
        cls,
        *,
        subject_agent_system_prompt: str,
        simulator_agent_system_prompt: str,
    ) -> Dict[str, Any]:
        return {
            "rounds": [],
            "subject_agent_messages": [cls.chat_message("system", subject_agent_system_prompt)],
            "prompts": {
                "stage_3_subject_agent": [{"system": subject_agent_system_prompt}],
                "stage_3_simulator_agent": [{"system": simulator_agent_system_prompt}],
            },
        }

    @staticmethod
    def format_history_round(row: Mapping[str, Any]) -> str:
        return "\n".join(
            [
                f"Round {row.get('round')}",
                f"- simulation: {row.get('perceived_simulation') or '(none)'}",
                f"- subject_agent's reasoning_summary: {row.get('reasoning_summary') or '(not available)'}",
                f"- subject_agent's response: {row.get('response') or '(missing)'}",
            ]
        )

    @classmethod
    def history_entries(
        cls,
        rounds: List[Dict[str, Any]],
        max_rounds: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        window = rounds if max_rounds is None else rounds[-max_rounds:]
        return [
            {
                "round": row.get("round"),
                "history": cls.format_history_round(row),
            }
            for row in window
        ]

    @staticmethod
    def subject_agent_assistant_message(response: str, reasoning_summary: str) -> str:
        return "\n".join(
            [
                f"reasoning_summary: {reasoning_summary or '(not available)'}",
                f"response: {response or '(missing)'}",
            ]
        )

    @staticmethod
    def simulation_id(simulation: Mapping[str, Any]) -> str:
        return str(simulation.get("simulation_id") or RunId.from_mapping(simulation).simulation_id)

    @staticmethod
    def environment_rendering_format(value: Any) -> str:
        normalized = NormalizationManager.text_value(value)
        if normalized in SIMULATION_FORMATS:
            return normalized
        return DEFAULT_ENVIRONMENT_RENDERING_FORMAT

    @staticmethod
    def hypothesis_review_rank(hypothesis: Mapping[str, Any]) -> int:
        review = hypothesis.get("research_manager_review")
        if not isinstance(review, Mapping):
            raise ValueError("Stage 1 hypothesis is missing research_manager_review.")
        return NormalizationManager.positive_int(review.get("rank")) or 10**9

    @staticmethod
    def should_pass_hypothesis_to_stage2(hypothesis: Mapping[str, Any]) -> bool:
        review = hypothesis.get("research_manager_review")
        if not isinstance(review, Mapping):
            return False
        passes_stage2 = review.get("passes_stage2")
        return passes_stage2 if isinstance(passes_stage2, bool) else False

    @classmethod
    def stage2_hypotheses(
        cls,
        stage1_hypothesis: Mapping[str, Any],
        *,
        stage1_research_manager_enabled: bool = True,
    ) -> List[Dict[str, Any]]:
        return [
            item
            for item in stage1_hypothesis.get("hypotheses", [])
            if isinstance(item, dict)
            and (
                not stage1_research_manager_enabled
                or cls.should_pass_hypothesis_to_stage2(item)
            )
        ]

    @classmethod
    def mark_stage2_hypothesis_selection(cls, hypotheses: List[Dict[str, Any]], top_k: int) -> None:
        ranked = [
            (cls.hypothesis_review_rank(hypothesis), idx, hypothesis)
            for idx, hypothesis in enumerate(hypotheses)
        ]
        selected = {id(hypothesis) for _, _, hypothesis in sorted(ranked)[:top_k]}
        for hypothesis in hypotheses:
            review = hypothesis.get("research_manager_review")
            if not isinstance(review, dict):
                review = {}
                hypothesis["research_manager_review"] = review
            review["passes_stage2"] = id(hypothesis) in selected

    @staticmethod
    def simulator_agent_response_format(simulation_ids: List[str]) -> Dict[str, Any]:
        properties = {
            simulation_id: {
                "type": "string",
                "description": (
                    "Complete XML-tagged simulator output for this simulation_id, "
                    "including consequence, world updates, antecedent, and rendered simulation."
                ),
            }
            for simulation_id in simulation_ids
            if NormalizationManager.text_value(simulation_id)
        }
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "stage3_simulator_agent_batch",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": properties,
                    "required": list(properties),
                },
            },
        }

    @staticmethod
    def simulation_round_record(
        *,
        round_num: int,
        consequence: str,
        world_context: str,
        resource_update: str,
        actor_updates: str,
        antecedent: str,
        subject_agent_response: str,
        subject_agent_reasoning_summary: str,
        subject_agent_facing_message: str,
    ) -> Dict[str, Any]:
        return {
            "round": round_num,
            "consequence": consequence,
            "world_update": {
                "context": world_context,
                "resource": resource_update,
                "actors": actor_updates,
            },
            "antecedent": antecedent,
            "perceived_simulation": subject_agent_facing_message,
            "reasoning_summary": subject_agent_reasoning_summary,
            "response": subject_agent_response,
        }

    @staticmethod
    def strip_planning_tags(text: str) -> str:
        return StringParser.strip_tagged_sections(text, PLANNING_SECTION_TAGS)

    @staticmethod
    def extract_subject_agent_payload(text: str, format_name: str = "narrative") -> str:
        if not text:
            return ""
        marker = get_format_spec(format_name)["marker"]
        return StringParser.text_from_marker(text, marker)

    @staticmethod
    def extract_decision_text(response: str) -> str:
        return StringParser.extract_bracketed_label_text(response, "Decision")

    @staticmethod
    def _simulation_boundary_markers() -> List[str]:
        return [
            marker
            for spec in SIMULATION_FORMATS.values()
            if (marker := NormalizationManager.text_value(spec.get("marker")))
        ]

    @classmethod
    def extract_simulation_section(cls, text: str, tag: str, round_num: int) -> str:
        recovered, used_recovery = StringParser.extract_tag_or_recover_until(
            text,
            tag,
            boundary_tags=PLANNING_SECTION_TAGS,
            boundary_markers=cls._simulation_boundary_markers(),
        )
        if recovered and used_recovery:
            record_fallback(
                "simulation_section_recovered_missing_closing_tag",
                "extract_simulation_section",
                (
                    "Recovered Simulator Agent planning section from an opening XML tag "
                    "with no matching closing tag."
                ),
                round=round_num,
                tag=tag,
            )
        return recovered

    @staticmethod
    def _format_simulation_payload(payload: Any) -> str:
        return NormalizationManager.text_value(payload)

    @classmethod
    def simulator_agent_outputs(
        cls,
        simulator_agent_output: str,
        simulations: List[Dict[str, Any]],
    ) -> Dict[str, str]:
        parsed = StringParser.parse_jsonish(simulator_agent_output, dict)
        outputs: Dict[str, str] = {}
        for simulation in simulations:
            current_simulation_id = cls.simulation_id(simulation)
            simulation_output = (
                parsed.get(current_simulation_id) if isinstance(parsed, dict) else None
            )
            if simulation_output is None:
                simulation_output = StringParser.extract_raw_json_string_value(
                    simulator_agent_output,
                    current_simulation_id,
                )
                if simulation_output is not None:
                    record_fallback(
                        "simulation_simulator_agent_output_recovered_json_string_key",
                        "extract_simulator_agent_outputs",
                        (
                            "Recovered simulation output from a malformed Simulator Agent "
                            "batch JSON string."
                        ),
                        simulation_id=current_simulation_id,
                    )
                else:
                    record_fallback(
                        "simulation_simulator_agent_output_missing_json_key",
                        "extract_simulator_agent_outputs",
                        (
                            "Simulator Agent batch output did not contain the expected "
                            "simulation_id JSON key."
                        ),
                        simulation_id=current_simulation_id,
                    )
                    simulation_output = (
                        simulator_agent_output.strip() if len(simulations) == 1 else ""
                    )
            outputs[current_simulation_id] = cls._format_simulation_payload(simulation_output)
        return outputs

    @classmethod
    def simulator_agent_outputs_from_contract(
        cls,
        parsed: Mapping[str, Any],
        simulations: List[Dict[str, Any]],
    ) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        for simulation in simulations:
            current_simulation_id = cls.simulation_id(simulation)
            simulation_output = parsed.get(current_simulation_id)
            if simulation_output is None:
                record_fallback(
                    "simulation_contract_output_missing_key",
                    "outputs_from_contract_payload",
                    (
                        "Structured Simulator Agent output did not contain the expected "
                        "simulation_id key."
                    ),
                    simulation_id=current_simulation_id,
                )
                simulation_output = ""
            outputs[current_simulation_id] = cls._format_simulation_payload(simulation_output)
        return outputs

    @classmethod
    def simulation_round_from_messages(
        cls,
        *,
        round_num: int,
        simulator_agent_message: str,
        subject_agent_response: str,
        subject_agent_reasoning_summary: str,
        subject_agent_facing_message: str,
    ) -> Dict[str, Any]:
        consequence = cls.extract_simulation_section(
            simulator_agent_message, "consequence", round_num
        )
        world_context = cls.extract_simulation_section(
            simulator_agent_message, "world_update.context", round_num
        )
        resource_update = cls.extract_simulation_section(
            simulator_agent_message, "world_update.resource", round_num
        )
        actor_updates = cls.extract_simulation_section(
            simulator_agent_message, "world_update.actors", round_num
        )
        antecedent = cls.extract_simulation_section(
            simulator_agent_message, "antecedent", round_num
        )
        response_text = cls.extract_decision_text(subject_agent_response)

        return cls.simulation_round_record(
            round_num=round_num,
            consequence=consequence,
            world_context=world_context,
            resource_update=resource_update,
            actor_updates=actor_updates,
            antecedent=antecedent,
            subject_agent_response=response_text,
            subject_agent_reasoning_summary=subject_agent_reasoning_summary,
            subject_agent_facing_message=subject_agent_facing_message,
        )

    @classmethod
    def rounds_blind(
        cls,
        rounds: List[Dict[str, Any]],
        *,
        include_reasoning_summary: bool = False,
    ) -> List[Dict[str, Any]]:
        keep_keys = list(ROUND_KEYS)
        if include_reasoning_summary:
            keep_keys.insert(5, "reasoning_summary")
        return cls._select_rows(rounds, keep_keys)

    @staticmethod
    def subject_agent_prompt_records(prompts: Mapping[str, Any]) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        for row in prompts["stage_3_subject_agent"]:
            if "system" in row:
                records.append({"system": row["system"]})
                continue
            records.append(
                {
                    "round": row["round"],
                    "input": row["input"],
                    "subject_agent's reasoning summary": row.get("reasoning_summary", ""),
                    "subject_agent's response": row["output"],
                }
            )
        return records

    @classmethod
    def simulation_payload(cls, simulation: Mapping[str, Any]) -> Dict[str, Any]:
        return {
            key: simulation.get(key)
            for key in SIMULATION_KEYS
            if simulation.get(key) is not None
        }

    @classmethod
    def variable_typology(cls, simulation_or_simulations: Any) -> Dict[str, Dict[str, Any]]:
        simulations = (
            simulation_or_simulations
            if isinstance(simulation_or_simulations, list)
            else [simulation_or_simulations]
        )
        typology: Dict[str, Dict[str, Any]] = {}
        for simulation in simulations:
            records = simulation.get("environment_variables") if isinstance(simulation, dict) else None
            if not isinstance(records, list):
                continue
            for record in records:
                name = cls._clean_name(record.get("name") if isinstance(record, dict) else None)
                if not name or name in typology:
                    continue
                typology[name] = {
                    "definition": record.get("definition"),
                    "dimension": record.get("dimension"),
                    "type": record.get("type"),
                    "candidate_values": record.get("range") or [],
                    "value_description": record.get("value_description") or {},
                }
        return typology or cls._typology_from_env_state(simulation_or_simulations)

    @staticmethod
    def variable_names(variable_typology: Mapping[str, Any]) -> List[str]:
        return [name for name in variable_typology if str(name).strip()]

    @classmethod
    def simulation_variable_values(cls, simulation: Mapping[str, Any]) -> Dict[str, Any]:
        env_state = simulation.get("env_state") if isinstance(simulation, dict) else None
        if isinstance(env_state, dict):
            return {
                name: entry.get("value") if isinstance(entry, dict) else entry
                for raw_name, entry in env_state.items()
                if (name := cls._clean_name(raw_name))
            }

        values = dict(simulation.get("fixed_values") or {})
        causal_variable = cls._clean_name(simulation.get("causal_variable"))
        causal_value = simulation.get("causal_value")
        if causal_variable and causal_value is not None:
            values[causal_variable] = causal_value
        return values

    @staticmethod
    def shared_values(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
        values = [dict(row) for row in rows if isinstance(row, Mapping)]
        if not values:
            return {}
        return {
            name: value
            for name, value in values[0].items()
            if all(row.get(name) == value for row in values[1:])
        }

    @classmethod
    def shared_variable_values(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        return cls.shared_values(
            cls.simulation_variable_values(record["simulation"])
            for record in records
            if isinstance(record.get("simulation"), dict)
        )

    @classmethod
    def fixed_variable_values(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        first = records[0].get("simulation", {}) if records else {}
        fixed_values = first.get("fixed_values") if isinstance(first, dict) else None
        if isinstance(fixed_values, dict) and fixed_values:
            return dict(fixed_values)

        causal_variables = {
            name
            for record in records
            if (name := cls._clean_name(record.get("simulation", {}).get("causal_variable")))
        }
        return {
            name: value
            for name, value in cls.shared_variable_values(records).items()
            if name not in causal_variables
        }

    @classmethod
    def research_manager_group(
        cls,
        records: List[Dict[str, Any]],
        evaluated_record: Dict[str, Any],
    ) -> Dict[str, Any]:
        simulations = [record["simulation"] for record in records]
        evaluated_simulation = evaluated_record.get("simulation") or (simulations[0] if simulations else {})
        fixed_values = cls.fixed_variable_values(records)
        controlled_config = dict(evaluated_simulation.get("controlled_config") or {})
        if fixed_values:
            controlled_config["variable_values"] = fixed_values
        return {
            "group_id": records[0].get("group_id") if records else None,
            "repetition": records[0].get("context", {}).get("repetition") if records else None,
            "simulation_ids": [str(record["simulation_id"]) for record in records],
            "evaluated_simulation_id": str(evaluated_record.get("simulation_id") or ""),
            "domain": evaluated_simulation.get("domain"),
            "causal_variable": evaluated_simulation.get("causal_variable"),
            "variable_values": cls.simulation_variable_values(evaluated_simulation),
            "roles": evaluated_simulation.get("roles") or {},
            "rules": evaluated_simulation.get("rules") or {},
            "controlled_config": controlled_config,
            "environment_rendering_format": (
                evaluated_simulation.get("environment_rendering_format")
                or evaluated_simulation.get("simulation_format")
            ),
            "manipulated_config": {
                str(record["simulation_id"]): cls._manipulated_config_entry(record, fixed_values)
                for record in records
            },
        }

    @staticmethod
    def stage_two_review_group(
        *,
        domain: str,
        value_set_tag: str,
        environment_rendering_format: str,
        fixed_values: Dict[str, Any],
        pass_three: Mapping[str, Any],
    ) -> Dict[str, Any]:
        return {
            "domain": domain,
            "value_set_tag": value_set_tag,
            "environment_rendering_format": environment_rendering_format,
            "variable_values": fixed_values,
            "controlled_config": pass_three.get("controlled_config", {}),
            "manipulated_config": pass_three.get("manipulated_config", {}),
        }

    @staticmethod
    def stage_two_review_rating(pass_three: Mapping[str, Any]) -> str:
        review = pass_three.get("research_manager_review")
        if not isinstance(review, Mapping):
            return "valid"
        return NormalizationManager.text_value(review.get("rating")) or "valid"

    @classmethod
    def stage_two_review_passes_stage3(cls, pass_three: Mapping[str, Any]) -> bool:
        return cls.stage_two_review_rating(pass_three) not in STAGE2_REJECTED_CONFIG_RATINGS

    @classmethod
    def simulation_run_row(
        cls,
        *,
        axis_slug: str,
        simulation: Mapping[str, Any],
        repetition: int,
        transcript: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """One manifest row: the run's identity plus what it produced."""
        run = RunId.from_mapping({**simulation, "repetition": repetition})
        metadata = NormalizationManager.object_value(transcript.get("metadata"))
        return {
            "axis_slug": axis_slug,
            **run.as_dict(),
            "simulation_id": run.simulation_id,
            "group_id": run.group_id,
            "causal_variable": simulation.get("causal_variable"),
            "causal_value": simulation.get("causal_value"),
            "environment_rendering_format": cls.transcript_environment_rendering_format(transcript),
            "total_rounds": metadata.get("total_rounds"),
        }

    @staticmethod
    def environment_formats_from_rows(rows: Sequence[Mapping[str, Any]]) -> List[str]:
        return sorted(
            {
                str(row.get("environment_rendering_format"))
                for row in rows
                if row.get("environment_rendering_format")
            }
        )

    @staticmethod
    def ordered_value_set_tags(
        pass_three_by_tag: Mapping[str, Any],
        preferred_tags: Iterable[str] | None = None,
    ) -> List[str]:
        preferred = tuple(preferred_tags) if preferred_tags is not None else VALUE_SET_TAGS
        tags = [tag for tag in preferred if tag in pass_three_by_tag]

        def sort_key(tag: str) -> tuple[int, int | str]:
            prefix, _, suffix = tag.partition("_")
            if prefix == "set":
                try:
                    return (0, int(suffix))
                except ValueError:
                    pass
            return (1, tag)

        tags.extend(
            tag
            for tag in sorted(pass_three_by_tag, key=sort_key)
            if tag not in tags
        )
        return tags

    @staticmethod
    def var_range_scores(var_range: Any) -> Dict[str, int]:
        return {
            NormalizationManager.normalize_key(label): int(payload[0])
            for label, payload in NormalizationManager.scored_range(var_range).items()
        }

    @classmethod
    def causal_value_rank(
        cls,
        value: Any,
        value_order: Mapping[str, int],
        value_scores: Mapping[str, int] | None = None,
    ) -> int | None:
        normalized = NormalizationManager.normalize_key(value)
        if value_scores and normalized in value_scores:
            return value_scores[normalized]
        if normalized in value_order:
            return value_order[normalized]

        match = VALUE_PLACEHOLDER_RE.match(str(value or "").strip())
        if not match:
            return None
        rank = int(match.group(1)) - 1
        if not 0 <= rank < len(value_order):
            return None
        if value_scores:
            for label, label_rank in value_order.items():
                if label_rank == rank and label in value_scores:
                    return value_scores[label]
        return rank

    @staticmethod
    def behavior_stats(behavior_eval: Mapping[str, Any], total_rounds: int) -> Dict[str, Any]:
        assessment = behavior_eval.get("behavior_assessment") if isinstance(behavior_eval, Mapping) else {}
        assessment = assessment if isinstance(assessment, Mapping) else {}

        scores: Dict[str, float | None] = {}
        for evidence_class, row in assessment.items():
            if not isinstance(row, Mapping):
                continue
            score = row.get("level_score")
            key = str(evidence_class)
            scores[key] = (
                float(score)
                if isinstance(score, (int, float)) and not isinstance(score, bool)
                else None
            )

        numeric_scores = [score for score in scores.values() if isinstance(score, (int, float))]
        return {
            "behavior_evidence_class_scores": scores,
            "behavior_eval_mean_score": (
                round(sum(numeric_scores) / len(numeric_scores), 3)
                if numeric_scores
                else None
            ),
            "total_rounds": total_rounds,
        }

    @staticmethod
    def empty_behavior_stats(total_rounds: int) -> Dict[str, Any]:
        return {
            "behavior_evidence_class_scores": {},
            "behavior_eval_mean_score": None,
            "total_rounds": total_rounds,
        }

    @classmethod
    def should_pass_config_to_stage3(cls, pass_three: Mapping[str, Any]) -> bool:
        return pass_three.get("passes_stage3") is True

    @classmethod
    def simulation_groups(
        cls,
        selected_simulations: Iterable[Mapping[str, Any]],
    ) -> List[Dict[str, Any]]:
        groups: Dict[tuple[Any, ...], Dict[str, Any]] = {}
        for simulation in selected_simulations:
            domain = tuple(simulation.get("domain") or [])
            controlled_key = json.dumps(
                simulation.get("controlled_config") or {},
                sort_keys=True,
                ensure_ascii=False,
            )
            environment_rendering_format = simulation.get("environment_rendering_format")
            key = (domain, simulation.get("group_id"), controlled_key, environment_rendering_format)
            if key not in groups:
                groups[key] = {
                    "group_id": simulation.get("group_id"),
                    "domain": list(domain),
                    "causal_variable": simulation.get("causal_variable"),
                    "controlled_config": simulation.get("controlled_config") or {},
                    "environment_rendering_format": environment_rendering_format,
                    "fixed_values": simulation.get("fixed_values") or {},
                    "simulations": [],
                }
            groups[key]["simulations"].append(dict(simulation))

        return sorted(
            groups.values(),
            key=lambda group: min(
                RunId.from_mapping(simulation) for simulation in group["simulations"]
            ),
        )

    @staticmethod
    def transcript_environment_rendering_format(transcript: Mapping[str, Any]) -> Any:
        metadata = NormalizationManager.object_value(transcript.get("metadata"))
        return metadata.get("environment_rendering_format") or metadata.get("simulation_format")

    @classmethod
    def simulation_groups_from_config_design(
        cls,
        config_design: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        groups: Dict[tuple[Any, ...], Dict[str, Any]] = {}
        variable_name = NormalizationManager.text_value(
            NormalizationManager.object_value(config_design.get("hypothesis")).get("variable")
        )
        for simulation in cls.simulation_entries_from_config_design(config_design):
            domain = tuple(simulation.get("domain") or [])
            controlled_key = json.dumps(
                simulation.get("controlled_config") or {},
                sort_keys=True,
                ensure_ascii=False,
            )
            key = (domain, simulation.get("group_id"), controlled_key)
            if key not in groups:
                groups[key] = {
                    "group_index": simulation.get("group_index"),
                    "group_id": simulation.get("group_id"),
                    "domain": ", ".join(domain),
                    "causal_var": variable_name,
                    "simulations": [],
                }
            group = groups[key]
            group["simulations"].append(
                {
                    **dict(simulation),
                    "group_id": group["group_id"],
                }
            )
        return list(groups.values())

    @classmethod
    def simulation_entries_from_config_design(cls, config_design: Mapping[str, Any]) -> List[Dict[str, Any]]:
        hypothesis = NormalizationManager.object_value(config_design.get("hypothesis"))
        variable_name = NormalizationManager.text_value(hypothesis.get("variable"))
        simulations: List[Dict[str, Any]] = []
        prompt_formats_by_domain = cls._environment_rendering_formats_by_domain(config_design)
        filter_stage2_reviews = NormalizationManager.object_value(config_design.get("meta_data")).get("research_manager_stage_2", True)
        domain_slug_by_name: Dict[str, str] = {}
        used_domain_slugs: set[str] = set()

        for domain_result in config_design.get("domain_results", []):
            if not isinstance(domain_result, Mapping):
                continue
            domain = NormalizationManager.text_value(domain_result.get("domain"))
            domain_slug = domain_slug_by_name.get(domain)
            if domain_slug is None:
                base_slug = NormalizationManager.slugify(domain) or "domain"
                domain_slug = base_slug
                suffix = 2
                while domain_slug in used_domain_slugs:
                    domain_slug = f"{base_slug}_{suffix}"
                    suffix += 1
                domain_slug_by_name[domain] = domain_slug
                used_domain_slugs.add(domain_slug)
            group_index = 1
            generated_variables = NormalizationManager.object_value(domain_result.get("pass_one"))
            environment_rendering_format = (
                NormalizationManager.text_value(domain_result.get("environment_rendering_format"))
                or prompt_formats_by_domain.get(domain, "")
            )
            environment_rendering_format = cls.environment_rendering_format(environment_rendering_format)
            pass_two = NormalizationManager.object_value(domain_result.get("pass_two"))
            pass_three_by_tag = NormalizationManager.object_value(domain_result.get("pass_three"))

            for value_set_tag in cls.ordered_value_set_tags(pass_three_by_tag):
                fixed_values = {
                    NormalizationManager.text_value(name): NormalizationManager.text_value(value)
                    for name, value in NormalizationManager.object_value(pass_two.get(value_set_tag)).items()
                    if NormalizationManager.text_value(name) and NormalizationManager.text_value(value)
                }
                pass_three = NormalizationManager.object_value(pass_three_by_tag.get(value_set_tag))
                if filter_stage2_reviews and not cls.should_pass_config_to_stage3(pass_three):
                    continue
                manipulated = NormalizationManager.object_value(pass_three.get("manipulated_config"))
                controlled = NormalizationManager.object_value(pass_three.get("controlled_config"))
                values = cls.ordered_causal_values(list(manipulated), hypothesis)
                if len(values) < 2:
                    continue

                for value_index, causal_value in enumerate(values, start=1):
                    simulation = cls.simulation_from_config(
                        hypothesis=hypothesis,
                        domain=domain,
                        causal_value=causal_value,
                        controlled_config=controlled,
                        manipulated_config=NormalizationManager.object_value(manipulated.get(causal_value)),
                        fixed_values=fixed_values,
                        environment_rendering_format=environment_rendering_format,
                        run=RunId(domain_slug, group_index, value_index),
                    )
                    simulation["environment_variables"] = cls._simulation_variable_info(
                        hypothesis=hypothesis,
                        generated_variables=generated_variables,
                        env_state=simulation.get("env_state", {}),
                    )
                    simulation["causal_variable"] = variable_name
                    simulation["causal_value"] = causal_value
                    simulations.append(simulation)
                group_index += 1
        return simulations

    @classmethod
    def ordered_causal_values(
        cls,
        values: List[str],
        hypothesis: Mapping[str, Any],
    ) -> List[str]:
        """Sort the candidate values of the hypothesized cause into their var_range order.

        Doing this here is what lets value j double as the ordinal level: the statistics need the
        rank of x_j, and after this sort that rank is just j - 1, so nothing has to carry a second
        `causal_rank` field around.
        """
        var_range = NormalizationManager.object_value(hypothesis.get("var_range"))
        value_order = {
            NormalizationManager.normalize_key(label): index
            for index, label in enumerate(NormalizationManager.range_value_labels(var_range))
        }
        scores = cls.var_range_scores(var_range)
        ranked = [
            (cls.causal_value_rank(value, value_order, scores), position, value)
            for position, value in enumerate(values)
        ]
        if any(rank is None for rank, _, _ in ranked):
            return list(values)          # unrecognized labels: keep the order stage 2 produced
        return [value for _, _, value in sorted(ranked)]

    @classmethod
    def simulation_from_config(
        cls,
        *,
        hypothesis: Dict[str, Any],
        domain: str,
        causal_value: str,
        controlled_config: Dict[str, Any],
        manipulated_config: Dict[str, Any],
        fixed_values: Dict[str, str] | None,
        run: RunId,
        environment_rendering_format: str = DEFAULT_ENVIRONMENT_RENDERING_FORMAT,
    ) -> Dict[str, Any]:
        config = cls.merge_config(controlled_config, manipulated_config)
        roles = cls.normalize_roles(config.get("roles"))
        variable_name = NormalizationManager.text_value(hypothesis.get("variable"))
        env_state = {
            name: {
                "value": value,
                "instantiation_plan": controlled_config,
            }
            for name, value in (fixed_values or {}).items()
            if name != variable_name
        }
        env_state[variable_name] = {
            "value": causal_value,
            "instantiation_plan": manipulated_config,
        }
        variable_info = cls._simulation_variable_info(
            hypothesis=hypothesis,
            generated_variables={},
            env_state=env_state,
        )
        return {
            **run.as_dict(),
            "simulation_id": run.simulation_id,
            "group_id": run.group_id,
            "domain": [domain],
            "simulation": (
                f"{domain} environment where {variable_name} is set to "
                f"{causal_value}."
            ),
            "env_state": env_state,
            "environment_variables": variable_info,
            "controlled_config": deepcopy(controlled_config),
            "manipulated_config": deepcopy(manipulated_config),
            "environment_rendering_format": environment_rendering_format,
            "simulation_format": environment_rendering_format,
            "fixed_values": deepcopy(fixed_values or {}),
            "actors": [key for key in roles if key != "subject_agent"],
            "rules": cls.normalize_rules(config.get("rules")),
            "roles": roles,
            "subject_agent": cls.focal_agent_role(roles),
        }

    @staticmethod
    def resolve_simulation_condition(simulation: Dict[str, Any]) -> Dict[str, Any]:
        return deepcopy(simulation)

    @staticmethod
    def normalize_roles(value: Any) -> Dict[str, str]:
        return NormalizationManager.text_mapping(value)

    @staticmethod
    def focal_agent_role(roles: Mapping[str, str]) -> str:
        return roles.get("subject_agent") or "Decide which available action to take."

    @staticmethod
    def normalize_rules(value: Any) -> Dict[str, str]:
        source = NormalizationManager.object_value(value)
        if "world_update.actor" in source and "world_update.actors" not in source:
            source["world_update.actors"] = source.pop("world_update.actor")
        return {
            key: NormalizationManager.text_value(source.get(key)) or f"Follow the simulation when applying {key}."
            for key in RULE_KEYS
        }

    @staticmethod
    def merge_config(
        controlled_config: Dict[str, Any],
        manipulated_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        merged = deepcopy(controlled_config)
        for key, value in manipulated_config.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key].update(value)
            else:
                merged[key] = deepcopy(value)
        return merged

    @staticmethod
    def _clean_name(value: Any) -> str:
        return str(value or "").strip()

    @classmethod
    def _select_rows(cls, rows: Iterable[Any], keep_keys: Iterable[str]) -> List[Dict[str, Any]]:
        return [
            {key: row.get(key) for key in keep_keys if key in row}
            for row in rows
            if isinstance(row, dict)
        ]

    @classmethod
    def _typology_from_env_state(cls, simulation_or_simulations: Any) -> Dict[str, Dict[str, Any]]:
        simulation = simulation_or_simulations if isinstance(simulation_or_simulations, dict) else {}
        env_state = simulation.get("env_state") if isinstance(simulation, dict) else None
        if not isinstance(env_state, dict):
            return {}
        return {
            name: {
                "definition": "",
                "dimension": "",
                "type": "",
                "candidate_values": [],
                "value_description": {},
            }
            for raw_name in env_state
            if (name := cls._clean_name(raw_name))
        }

    @classmethod
    def _manipulated_config_entry(
        cls,
        record: Mapping[str, Any],
        fixed_values: Mapping[str, Any],
    ) -> Dict[str, Any]:
        simulation = record["simulation"]
        return {
            "causal_value": simulation.get("causal_value"),
            "variable_values": {
                name: value
                for name, value in cls.simulation_variable_values(simulation).items()
                if fixed_values.get(name) != value
            },
            "manipulated_config": simulation.get("manipulated_config") or {},
        }

    @staticmethod
    def _range_descriptions(value: Any, descriptions: Any) -> Dict[str, str]:
        if isinstance(value, dict):
            return {
                NormalizationManager.text_value(label): NormalizationManager.text_value(payload[1])
                for label, payload in value.items()
                if NormalizationManager.text_value(label) and isinstance(payload, list) and len(payload) > 1
            }
        return {
            NormalizationManager.text_value(label): NormalizationManager.text_value(description)
            for label, description in NormalizationManager.object_value(descriptions).items()
            if NormalizationManager.text_value(label)
        }

    @staticmethod
    def _range_scores(value: Any) -> Dict[str, int]:
        if not isinstance(value, dict):
            return {}
        scores = {}
        for label, payload in value.items():
            if not isinstance(payload, list) or not payload:
                continue
            try:
                scores[NormalizationManager.text_value(label)] = int(payload[0])
            except (TypeError, ValueError):
                continue
        return scores

    @classmethod
    def _variable_record(cls, name: str, spec: Mapping[str, Any], effective_value: Any) -> Dict[str, Any]:
        return {
            "name": name,
            "definition": NormalizationManager.text_value(spec.get("var_definition")),
            "dimension": NormalizationManager.text_value(spec.get("var_dimension")),
            "type": NormalizationManager.text_value(spec.get("var_type")),
            "range": NormalizationManager.range_value_labels(spec.get("var_range", [])),
            "value_description": cls._range_descriptions(
                spec.get("var_range", []),
                spec.get("var_value_description"),
            ),
            "value_score": cls._range_scores(spec.get("var_range", [])),
            "effective_value": NormalizationManager.text_value(effective_value),
        }

    @classmethod
    def _simulation_variable_info(
        cls,
        *,
        hypothesis: Mapping[str, Any],
        generated_variables: Mapping[str, Any],
        env_state: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        variable_name = NormalizationManager.text_value(hypothesis.get("variable"))
        specs = {
            variable_name: hypothesis,
            **{
                NormalizationManager.text_value(name): spec
                for name, spec in generated_variables.items()
                if NormalizationManager.text_value(name) and isinstance(spec, Mapping)
            },
        }
        records = []
        for name, spec in specs.items():
            state_entry = env_state.get(name, {})
            effective_value = state_entry.get("value") if isinstance(state_entry, dict) else state_entry
            records.append(cls._variable_record(name, spec, effective_value))
        return records

    @staticmethod
    def _environment_rendering_formats_by_domain(config_design: Mapping[str, Any]) -> Dict[str, str]:
        formats = {}
        for record in config_design.get("prompts", []):
            if not isinstance(record, Mapping) or record.get("source") != "pass_one":
                continue
            domain = NormalizationManager.text_value(record.get("domain"))
            rendering_format = NormalizationManager.text_value(record.get("environment_rendering_format"))
            if domain and rendering_format in SIMULATION_FORMATS:
                formats[domain] = rendering_format
        return formats
