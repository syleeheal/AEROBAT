"""Centralized normalization helpers for Aerobat."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List


class NormalizationManager:
    """Stateless normalization and loose value-coercion helpers."""

    @staticmethod
    def normalize_key(text: Any) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(text or "").lower()).strip()

    @staticmethod
    def slugify(value: Any, separator: str = "_") -> str:
        separator = separator or "_"
        slug = re.sub(r"[^a-z0-9]+", separator, str(value or "").lower())
        return slug.strip(separator)

    @staticmethod
    def normalize_rating(
        value: Any,
        valid_ratings: Iterable[str],
        default: str = "neutral",
    ) -> str:
        allowed = {
            re.sub(r"[^a-z ]+", "", re.sub(r"\s+", " ", str(item).strip().lower())).strip()
            for item in valid_ratings
        }
        normalized = re.sub(r"\s+", " ", str(value or "").strip().lower())
        normalized = re.sub(r"[^a-z ]+", "", normalized).strip()
        if normalized in allowed:
            return normalized
        normalized_default = re.sub(r"\s+", " ", str(default or "").strip().lower())
        normalized_default = re.sub(r"[^a-z ]+", "", normalized_default).strip()
        return normalized_default if normalized_default in allowed else default

    @staticmethod
    def find_normalized_key_value(mapping: Any, target_key: str) -> Any:
        if not isinstance(mapping, dict):
            return None
        target = NormalizationManager.normalize_key(target_key)
        if not target:
            return None
        for key, value in mapping.items():
            if NormalizationManager.normalize_key(key) == target:
                return value
        return None

    @staticmethod
    def find_normalized_key_prefix_value(mapping: Any, target_key: str) -> Any:
        value = NormalizationManager.find_normalized_key_value(mapping, target_key)
        if value is not None or not isinstance(mapping, dict):
            return value
        target = NormalizationManager.normalize_key(target_key)
        if not target:
            return None
        for key, candidate in mapping.items():
            normalized = NormalizationManager.normalize_key(key)
            if normalized.startswith(f"{target} "):
                return candidate
        return None

    @staticmethod
    def by_normalized_key(mapping: Any) -> Dict[str, Any]:
        if not isinstance(mapping, dict):
            return {}
        result: Dict[str, Any] = {}
        for key, value in mapping.items():
            normalized = NormalizationManager.normalize_key(key)
            if normalized:
                result[normalized] = value
        return result

    @staticmethod
    def split_listish(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if not value:
            return []
        text = str(value)
        for separator in ("|", ";"):
            text = text.replace(separator, ",")
        return [part.strip() for part in text.split(",") if part.strip()]

    @staticmethod
    def object_value(value: Any) -> Dict[str, Any]:
        return value if isinstance(value, dict) else {}

    @staticmethod
    def text_mapping(value: Any) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for key, item in NormalizationManager.object_value(value).items():
            normalized_key = NormalizationManager.text_value(key)
            normalized_item = NormalizationManager.text_value(item)
            if normalized_key and normalized_item:
                result[normalized_key] = normalized_item
        return result

    @staticmethod
    def range_value_labels(value: Any) -> List[str]:
        if isinstance(value, dict):
            return [str(item).strip() for item in value if str(item).strip()]
        return NormalizationManager.split_listish(value)

    @staticmethod
    def to_int(value: Any, default: int | None = None) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def extract_int(value: Any, default: int | None = None) -> int | None:
        parsed = NormalizationManager.to_int(value)
        if parsed is not None:
            return parsed
        match = re.search(r"\d+", str(value or ""))
        return int(match.group(0)) if match else default

    @staticmethod
    def positive_int(value: Any, default: int | None = None) -> int | None:
        parsed = NormalizationManager.extract_int(value)
        return parsed if parsed is not None and parsed >= 1 else default

    @staticmethod
    def require_positive_int(value: Any, name: str) -> int:
        parsed = NormalizationManager.positive_int(value)
        if parsed is None:
            raise ValueError(f"{name} must be a positive integer, got {value!r}")
        return parsed

    @staticmethod
    def numeric_score(value: Any) -> int | None:
        return NormalizationManager.to_int(value)

    @staticmethod
    def scored_range(value: Any) -> Dict[str, List[Any]]:
        if not isinstance(value, dict):
            return {}

        normalized = {}
        for label, payload in value.items():
            name = NormalizationManager.text_value(label)
            if not name:
                continue
            score = None
            description = ""
            if isinstance(payload, (list, tuple)):
                score = NormalizationManager.numeric_score(payload[0] if payload else None)
                description = NormalizationManager.text_value(payload[1] if len(payload) > 1 else "")
            elif isinstance(payload, dict):
                score = NormalizationManager.numeric_score(NormalizationManager.get_alias(payload, "score"))
                description = NormalizationManager.text_value(
                    NormalizationManager.get_alias(payload, "description", "value_description")
                )
            if score is not None:
                normalized[name] = [score, description]
        return normalized

    @staticmethod
    def hypothesis_records(items: List[Any]) -> List[Dict[str, Any]]:
        hypotheses: List[Dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue

            variable = NormalizationManager.text_value(
                NormalizationManager.get_alias(item, "variable")
            )
            if not variable:
                continue

            hypotheses.append(
                {
                    "variable": variable,
                    "var_definition": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "var_definition", "definition")
                    ),
                    "var_dimension": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "var_dimension", "dimension")
                    ),
                    "var_type": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "var_type", "type")
                    ),
                    "var_range": NormalizationManager.scored_range(
                        NormalizationManager.get_alias(item, "var_range", "range", default={})
                    ),
                    "mechanism": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "mechanism")
                    ),
                    "domain": NormalizationManager.split_listish(
                        NormalizationManager.get_alias(item, "domain", default=[])
                    ),
                    "causal_effect": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "causal_effect")
                    ),
                    "interaction_length": NormalizationManager.text_value(
                        NormalizationManager.get_alias(item, "interaction_length")
                    ),
                }
            )
        return hypotheses

    @staticmethod
    def behavior_eval_evidence_class(entry: Any) -> Dict[str, Any]:
        if not isinstance(entry, dict):
            entry = {}
        score = NormalizationManager.level_score(
            entry.get("level_score", entry.get("intensity_score", entry.get("score")))
        )
        return {
            "level_score": score,
            "rationale": NormalizationManager.text_value(entry.get("rationale")) or None,
        }

    @staticmethod
    def level_score(value: Any) -> float | None:
        try:
            score = float(str(value).strip())
        except (TypeError, ValueError):
            return None
        if score != score:
            return None
        return score

    @staticmethod
    def rating_text(value: Any) -> str:
        if isinstance(value, dict):
            value = value.get("rating")
        return NormalizationManager.text_value(value)

    @staticmethod
    def is_none_marker(value: Any) -> bool:
        return isinstance(value, str) and value.strip().lower() in {"none", "n/a", "na", "not applicable"}

    @staticmethod
    def text_value(value: Any) -> str:
        return "" if value is None else str(value).strip()

    @staticmethod
    def get_alias(mapping: Any, *names: str, default: Any = "") -> Any:
        if not isinstance(mapping, dict):
            return default
        by_key = NormalizationManager.by_normalized_key(mapping)
        for name in names:
            value = by_key.get(NormalizationManager.normalize_key(name))
            if value is not None:
                return value
        return default

    @staticmethod
    def normalize_choice(
        value: Any,
        choices: Iterable[str],
        default: str | None = None,
    ) -> str | None:
        by_key = {
            NormalizationManager.normalize_key(choice).replace(" ", ""): choice
            for choice in choices
        }
        return by_key.get(NormalizationManager.normalize_key(value).replace(" ", ""), default)
