"""Conservative parsing of LLM responses at every AEROBAT stage.

These parsers retain permissive recovery behavior learned from irregular provider
outputs. Change their normalization or fallback semantics only with protocol-level
equivalence evidence.
"""

from __future__ import annotations

import difflib
from typing import Any, Dict, List, Mapping, Optional, Sequence

from aerobat.utils import record_fallback

from .constants import (
    EVIDENCE_CLASS_MATCH_CUTOFF,
    OVERALL_VALIDITY_SCALE,
    RATING_SCALE,
    RENDERING_INSTRUCTION_KEYS,
    STAGE2_REVIEW_RATINGS,
    VALUE_SET_TAGS,
)
from .normalization import NormalizationManager
from .parsing import StringParser, TaggedResponse
from .payloads import PayloadManager


# Stage 1: behavior specification and causal hypotheses.


def _parse_behavior_eval_rubric(response: str) -> List[Dict[str, Any]] | None:
    raw = StringParser.tag(response, "behavior_eval_rubric")
    if not raw:
        record_fallback(
            "behavior_eval_rubric_missing_tag",
            "parse_hypothesis_response",
            "Stage 1 behavior evaluation rubric omitted the behavior_eval_rubric XML tag; empty rubric propagated.",
        )
        return []
    if NormalizationManager.is_none_marker(raw):
        return None
    return _behavior_eval_rubric_rows(StringParser.parse_jsonish_array(raw))


def _behavior_eval_rubric_rows(items: Any) -> List[Dict[str, Any]] | None:
    if NormalizationManager.is_none_marker(items):
        return None
    if not isinstance(items, list):
        return []

    rubric: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        score_value = item.get("score")
        score = _behavior_eval_rubric_score(score_value)
        level = NormalizationManager.text_value(
            item.get("level")
            or item.get("intensity")
            or item.get("label")
            or item.get("intensity_label")
        )
        if score is None and (score_value is not None or level.lower() != "no evidence"):
            continue
        rubric.append(
            {
                "score": score,
                "level": level,
                "evidence": NormalizationManager.object_value(item.get("evidence")),
            }
        )
    return sorted(rubric, key=lambda row: (row["score"] is None, row["score"] or 0))


def _behavior_eval_rubric_score(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_hypothesis_response(response: str) -> Dict[str, Any]:
    tagged = TaggedResponse(response)
    return {
        "definition": tagged.tag("behavior_hypothesis"),
        "behavior_eval_rubric": _parse_behavior_eval_rubric(response),
        "hypotheses": NormalizationManager.hypothesis_records(tagged.array("hypothesis")),
    }


# Stage 2: environment variables, value sets, and matched configurations.


def parse_environment_rendering_format(response: str) -> str:
    return PayloadManager.environment_rendering_format(
        TaggedResponse(response).tag("environment_rendering_format")
    )


def parse_pass_one(response: str) -> Dict[str, Dict[str, Any]]:
    variables = TaggedResponse(response).object("variables")
    return {
        NormalizationManager.text_value(name): {
            "var_definition": NormalizationManager.text_value(spec.get("var_definition")),
            "var_dimension": NormalizationManager.text_value(spec.get("var_dimension")),
            "var_type": NormalizationManager.text_value(spec.get("var_type")),
            "var_range": NormalizationManager.split_listish(spec.get("var_range", [])),
            "var_value_description": NormalizationManager.object_value(
                spec.get("var_value_description")
            ),
        }
        for name, spec in variables.items()
        if NormalizationManager.text_value(name) and isinstance(spec, dict)
    }


def parse_pass_two(
    response: str,
    value_set_tags: Sequence[str] | None = None,
) -> Dict[str, Dict[str, str]]:
    parsed = TaggedResponse(response)
    tags = tuple(value_set_tags) if value_set_tags is not None else VALUE_SET_TAGS
    result = {
        tag: NormalizationManager.text_mapping(parsed.object(f"var_value_{tag}"))
        for tag in tags
    }
    for tag in (
        "covariance_structure",
        "potential_interactions",
        "problematic_combinations",
    ):
        result[tag] = NormalizationManager.text_mapping(parsed.object(tag))
    return result


def parse_pass_three(response: str) -> Dict[str, Any]:
    parsed = TaggedResponse(response)
    return {
        "manipulated_config": parsed.object("manipulated_config"),
        "controlled_config": parsed.object("controlled_config"),
    }


# Stage 3: simulator-agent batched rendering.


def parse_simulator_agent_batch(response: str) -> Dict[str, str]:
    return NormalizationManager.text_mapping(StringParser.parse_jsonish_object(response))


# Stage 4: blind behavioral review.


def _rubric_rows(
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None,
) -> List[Mapping[str, Any]]:
    if isinstance(behavior_eval_rubric, dict):
        return [
            row
            for sublist in behavior_eval_rubric.values()
            if isinstance(sublist, list)
            for row in sublist
            if isinstance(row, Mapping)
        ]
    if isinstance(behavior_eval_rubric, list):
        return [row for row in behavior_eval_rubric if isinstance(row, Mapping)]
    return []


def _rubric_numeric_score_range(
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None,
) -> tuple[float, float] | None:
    rows = _rubric_rows(behavior_eval_rubric)
    scores = [
        score
        for row in rows
        if (score := NormalizationManager.level_score(row.get("score"))) is not None
    ]
    return (min(scores), max(scores)) if scores else None


def _behavior_assessment_score_value(entry: Any) -> tuple[bool, Any]:
    if not isinstance(entry, Mapping):
        return False, None
    for key in ("level_score", "intensity_score", "score"):
        if key in entry:
            return True, entry.get(key)
    return False, None


def _rubric_evidence_class_names(
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None,
) -> List[str]:
    names: List[str] = []
    seen: set[str] = set()
    for row in _rubric_rows(behavior_eval_rubric):
        evidence = row.get("evidence")
        if not isinstance(evidence, Mapping):
            continue
        for evidence_class in evidence:
            name = NormalizationManager.text_value(evidence_class)
            key = NormalizationManager.normalize_key(name)
            if key and key not in seen:
                seen.add(key)
                names.append(name)
    return names


def _match_rubric_evidence_class(name: str, rubric_names: Sequence[str]) -> str | None:
    by_key = {NormalizationManager.normalize_key(item): item for item in rubric_names}
    key = NormalizationManager.normalize_key(name)
    if key in by_key:
        return by_key[key]
    close = difflib.get_close_matches(key, list(by_key), n=1, cutoff=EVIDENCE_CLASS_MATCH_CUTOFF)
    return by_key[close[0]] if close else None


def _has_numeric_level_score(entry: Any) -> bool:
    _, raw_score = _behavior_assessment_score_value(entry)
    return NormalizationManager.level_score(raw_score) is not None


def align_behavior_assessment_keys(
    assessment: Any,
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None,
) -> Dict[str, Any]:
    """Re-key a behavior assessment onto the rubric's evidence class spellings.

    Reviewers occasionally misspell an evidence class (``Engagement_bread_duration``
    for ``Engagement_breadth_duration``), which downstream stages then treat as a
    separate class. Near-misses are mapped back onto the rubric name; anything with
    no close rubric match is kept as-is and reported as a fallback.
    """

    if not isinstance(assessment, Mapping):
        return {}
    rubric_names = _rubric_evidence_class_names(behavior_eval_rubric)
    if not rubric_names:
        return dict(assessment)

    aligned: Dict[str, Any] = {}
    for evidence_class, entry in assessment.items():
        name = NormalizationManager.text_value(evidence_class)
        if not name:
            continue
        rubric_name = _match_rubric_evidence_class(name, rubric_names)
        if rubric_name is None:
            record_fallback(
                "behavior_eval_unknown_evidence_class",
                "align_behavior_assessment_keys",
                "Behavior evaluator returned an evidence class absent from the rubric; name kept as-is.",
                evidence_class=name,
            )
            aligned.setdefault(name, entry)
            continue
        if rubric_name != name:
            record_fallback(
                "behavior_eval_evidence_class_renamed",
                "align_behavior_assessment_keys",
                "Behavior evaluator used a non-rubric spelling for an evidence class; remapped to the rubric name.",
                evidence_class=name,
                rubric_evidence_class=rubric_name,
            )
        if rubric_name in aligned:
            record_fallback(
                "behavior_eval_duplicate_evidence_class",
                "align_behavior_assessment_keys",
                "Behavior evaluator returned the same rubric evidence class twice; kept the scored entry.",
                evidence_class=name,
                rubric_evidence_class=rubric_name,
            )
            if _has_numeric_level_score(aligned[rubric_name]) or not _has_numeric_level_score(entry):
                continue
        aligned[rubric_name] = entry
    return aligned


def _parse_behavior_assessment(
    raw_assessment: Any,
    *,
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None = None,
) -> Dict[str, Dict[str, Any]]:
    if not isinstance(raw_assessment, Mapping):
        record_fallback(
            "behavior_eval_missing_assessment",
            "parse_behavior_eval",
            "Behavior evaluator omitted a valid behavior_assessment object; empty assessment propagated.",
        )
        return {}

    score_range = _rubric_numeric_score_range(behavior_eval_rubric)
    assessment: Dict[str, Dict[str, Any]] = {}
    for evidence_class, entry in align_behavior_assessment_keys(
        raw_assessment,
        behavior_eval_rubric,
    ).items():
        name = NormalizationManager.text_value(evidence_class)
        if not name:
            continue
        normalized = NormalizationManager.behavior_eval_evidence_class(entry)
        has_score, raw_score = _behavior_assessment_score_value(entry)
        if normalized["level_score"] is None and (not has_score or raw_score is not None):
            record_fallback(
                "behavior_eval_missing_level_score",
                "_parse_behavior_assessment",
                "Behavior evaluator omitted a valid numeric or null level_score; null propagated.",
                evidence_class=name,
            )
        if (
            normalized["level_score"] is not None
            and score_range is not None
            and not (score_range[0] <= normalized["level_score"] <= score_range[1])
        ):
            record_fallback(
                "behavior_eval_level_score_out_of_rubric_range",
                "_parse_behavior_assessment",
                "Behavior evaluator returned a level_score outside the numeric rubric range; null propagated.",
                evidence_class=name,
                level_score=normalized["level_score"],
                min_score=score_range[0],
                max_score=score_range[1],
            )
            normalized["level_score"] = None
        assessment[name] = normalized
    return assessment


def parse_behavior_eval(
    response: str,
    *,
    behavior_eval_rubric: Dict[str, List[Dict[str, Any]]] | List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    parsed = TaggedResponse(response)
    assessment_block = parsed.tag("behavior_assessment")
    raw_assessment = {}
    if not assessment_block:
        record_fallback(
            "behavior_eval_missing_assessment_tag",
            "parse_behavior_eval",
            "Behavior evaluator omitted the behavior_assessment XML tag; empty assessment propagated.",
        )
    elif not NormalizationManager.is_none_marker(assessment_block):
        raw_assessment = StringParser.parse_jsonish_object(assessment_block)

    return {
        "simulation_summary": parsed.tag("simulation_summary"),
        "behavior_patterns": parsed.tag("behavior_patterns"),
        "behavior_assessment": _parse_behavior_assessment(
            raw_assessment,
            behavior_eval_rubric=behavior_eval_rubric,
        ),
        "inferred_mechanisms": parsed.tag("inferred_mechanisms"),
    }


# Research-manager gates and final report.


def parse_stage_one_review(
    response: str,
    hypotheses: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_key = NormalizationManager.by_normalized_key(StringParser.parse_jsonish_object(response))
    reviews: Dict[str, Dict[str, Any]] = {}

    for hypothesis in hypotheses:
        variable = NormalizationManager.text_value(hypothesis.get("variable"))
        payload = _stage_one_review_payload(by_key, variable)
        if payload is None:
            record_fallback(
                "stage_one_review_missing_hypothesis_key",
                "parse_stage_one_review",
                "Research-manager review omitted a hypothesis; null rank propagated.",
                expected_key=NormalizationManager.normalize_key(variable),
            )
            reviews[variable] = {"rank": None, "rationale": ""}
            continue
        rank = NormalizationManager.positive_int(payload.get("rank"))
        if rank is None:
            raise ValueError(
                (
                    f"Stage 1 research-manager review for hypothesis {variable!r} "
                    "must include a positive integer rank."
                )
            )
        reviews[variable] = {
            "rank": rank,
            "rationale": NormalizationManager.text_value(payload.get("rationale")),
        }
    return reviews


def _stage_one_review_payload(
    reviews_by_key: Dict[str, Any],
    variable: str,
) -> Dict[str, Any] | None:
    target = NormalizationManager.normalize_key(variable)
    payload = reviews_by_key.get(target)
    if isinstance(payload, dict):
        return payload

    matches = [
        (key, item)
        for key, item in reviews_by_key.items()
        if isinstance(item, dict) and _relaxed_stage_one_review_key_match(key, target)
    ]
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(f"Stage 1 research-manager review has ambiguous key for hypothesis {variable!r}.")

    matched_key, matched_payload = matches[0]
    record_fallback(
        "stage_one_review_relaxed_hypothesis_key_match",
        "parse_stage_one_review",
        "Matched research-manager review key after normalized containment check.",
        expected_key=target,
        matched_key=matched_key,
    )
    return matched_payload


def _relaxed_stage_one_review_key_match(candidate: str, target: str) -> bool:
    if not candidate or not target:
        return False
    return f" {target} " in f" {candidate} "


def parse_stage_two_review(response: str) -> Dict[str, str]:
    parsed = StringParser.parse_jsonish_object(response)
    return {
        "rating": NormalizationManager.normalize_choice(
            parsed.get("rating"),
            STAGE2_REVIEW_RATINGS,
            "valid",
        )
        or "valid",
        "rationale": NormalizationManager.text_value(parsed.get("rationale")),
    }


def _normalize_overall_validity(value: Any) -> Optional[str]:
    rating = NormalizationManager.rating_text(value)
    if not rating:
        return None
    return NormalizationManager.normalize_choice(rating, OVERALL_VALIDITY_SCALE)


def _parse_research_rating_object(
    response: str,
    tag: str,
    rating_scale: List[str],
    expected_keys: Optional[List[str]],
) -> Dict[str, Optional[str]]:
    parsed = StringParser.parse_tagged(response, tag, dict)
    out: Dict[str, Optional[str]] = {}
    missing: List[str] = []

    for key in expected_keys or []:
        value = NormalizationManager.find_normalized_key_value(parsed, key)
        rating = NormalizationManager.rating_text(value)
        if not rating:
            missing.append(key)
            out[key] = None
            continue
        out[key] = NormalizationManager.normalize_rating(rating, rating_scale)

    if missing:
        record_fallback(
            "research_manager_missing_rating_entries",
            "_parse_research_rating_object",
            "Research manager omitted expected rating entries; null propagated.",
            tag=tag,
            missing_keys=missing,
        )
    return out


def _find_variable_fidelity_value(parsed: Any, variable_name: str) -> Any:
    return NormalizationManager.find_normalized_key_prefix_value(parsed, variable_name)


def _parse_research_variable_fidelity(
    response: str,
    variable_names: List[str],
) -> Dict[str, Optional[str]]:
    parsed = StringParser.parse_tagged(response, "task_1.variable_fidelity", dict)
    out: Dict[str, Optional[str]] = {}
    missing: List[str] = []
    for variable_name in variable_names:
        value = _find_variable_fidelity_value(parsed, variable_name)
        rating = NormalizationManager.rating_text(value)
        if not rating:
            missing.append(variable_name)
            out[variable_name] = None
            continue
        out[variable_name] = NormalizationManager.normalize_rating(rating, RATING_SCALE)

    if missing:
        record_fallback(
            "research_manager_missing_rating_entries",
            "_parse_research_variable_fidelity",
            "Research manager omitted expected variable fidelity entries; null propagated.",
            tag="task_1.variable_fidelity",
            missing_keys=missing,
        )
    return out


def _parse_research_rationale(response: str, tag: str) -> List[str]:
    return StringParser.parse_tagged_text_list(response, tag)


def _parse_research_overall_validity(response: str) -> Dict[str, Optional[str]]:
    parsed = StringParser.parse_tagged(response, "task_2.overall_validity", dict)
    rating = _normalize_overall_validity(
        parsed.get("rating")
        or parsed.get("overall validity rating")
        or parsed.get("overall_validity")
    )
    rationale = NormalizationManager.text_value(parsed.get("rationale")) or None
    if rating is None:
        record_fallback(
            "research_manager_missing_overall_validity",
            "_parse_research_overall_validity",
            "Research manager omitted a valid overall validity rating; null propagated.",
        )
    return {"rating": rating, "rationale": rationale}


def parse_research_manager_review(
    response: str,
    variable_names: List[str],
) -> Dict[str, Any]:
    return {
        "variable_fidelity": _parse_research_variable_fidelity(response, variable_names),
        "variable_fidelity_rationale": _parse_research_rationale(
            response, "task_1.variable_fidelity_rationale",
        ),
        "rule_fidelity": _parse_research_rating_object(
            response,
            "task_1.rule_fidelity",
            RATING_SCALE,
            [
                "rules[world_update.context]",
                "rules[world_update.resource]",
                "rules[world_update.actors]",
                "rules[consequence]",
            ],
        ),
        "rule_fidelity_rationale": _parse_research_rationale(
            response, "task_1.rule_fidelity_rationale",
        ),
        "rendering_fidelity": _parse_research_rating_object(
            response,
            "task_1.rendering_fidelity",
            RATING_SCALE,
            list(RENDERING_INSTRUCTION_KEYS),
        ),
        "rendering_fidelity_rationale": _parse_research_rationale(
            response, "task_1.rendering_fidelity_rationale",
        ),
        "overall_validity": _parse_research_overall_validity(response),
    }


def parse_final_report_response(response: str) -> str:
    report = StringParser.tag(response, "final_report")
    if not report:
        record_fallback(
            "final_report_missing_tag",
            "parse_final_report_response",
            "Research manager omitted the final_report XML tag; using full response text.",
        )
        return str(response or "").strip()
    return report
