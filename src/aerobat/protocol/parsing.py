"""Centralized parsing helpers for Aerobat."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List

from aerobat.utils import record_fallback


class StringParser:
    """Stateless parser for LLM responses and loose text payloads."""

    _DELIMITERS: Dict[type, tuple[str, str]] = {
        dict: ("{", "}"),
        list: ("[", "]"),
    }
    _SMART_QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})

    @classmethod
    def _json_loads(cls, text: str, reject_duplicates: bool = False) -> Any:
        if not reject_duplicates:
            return json.loads(text)

        def _object_pairs_hook(pairs: list[tuple[str, Any]]) -> Dict[str, Any]:
            obj: Dict[str, Any] = {}
            for key, value in pairs:
                if key in obj:
                    raise ValueError(f"Duplicate JSON key: {key}")
                obj[key] = value
            return obj

        return json.loads(text, object_pairs_hook=_object_pairs_hook)

    @staticmethod
    def _text(value: Any) -> str:
        return str(value or "").strip()

    @classmethod
    def _repair_unbalanced_json(cls, text: str) -> str:
        pairs = dict(cls._DELIMITERS.values())
        closers = set(pairs.values())
        stack: List[str] = []
        repaired: List[str] = []
        in_string = False
        escaped = False

        for char in text:
            repaired.append(char)
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char in pairs:
                stack.append(pairs[char])
            elif char in closers:
                if stack and stack[-1] == char:
                    stack.pop()
                    continue
                missing: List[str] = []
                while stack and stack[-1] != char:
                    missing.append(stack.pop())
                if stack and stack[-1] == char:
                    stack.pop()
                    repaired[-1:-1] = missing

        repaired.extend(reversed(stack))
        return "".join(repaired)

    @staticmethod
    def _remove_trailing_json_commas(text: str) -> str:
        chars = list(text)
        in_string = False
        escaped = False

        for idx, char in enumerate(chars):
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char in "}]":
                prev = idx - 1
                while prev >= 0 and chars[prev].isspace():
                    prev -= 1
                if prev >= 0 and chars[prev] == ",":
                    chars[prev] = ""

        return "".join(chars)

    @staticmethod
    def _unescaped_quote_count(text: str) -> int:
        count = 0
        escaped = False
        for char in text:
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
            elif char == '"':
                count += 1
        return count

    @classmethod
    def _repair_missing_line_end_quotes(cls, text: str) -> str:
        lines: List[str] = []
        changed = False

        for line in text.splitlines(keepends=True):
            content = line.rstrip("\r\n")
            newline = line[len(content):]
            insert_at = cls._missing_line_end_quote_index(content)
            if insert_at is not None:
                content = f'{content[:insert_at]}"{content[insert_at:]}'
                changed = True
            lines.append(content + newline)

        return "".join(lines) if changed else text

    @classmethod
    def _missing_line_end_quote_index(cls, line: str) -> int | None:
        stripped = line.rstrip()
        if not stripped or stripped[-1] not in ",]}":
            return None
        if cls._unescaped_quote_count(line) % 2 == 0:
            return None

        idx = len(stripped)
        if stripped[idx - 1] == ",":
            idx -= 1
            while idx > 0 and stripped[idx - 1].isspace():
                idx -= 1
        while idx > 0 and stripped[idx - 1] in "]}":
            idx -= 1
            while idx > 0 and stripped[idx - 1].isspace():
                idx -= 1

        return idx if idx > 0 else None

    @classmethod
    def _json_parse_candidates(cls, text: str) -> list[tuple[str, str]]:
        quoted = cls._repair_missing_line_end_quotes(text)
        repaired = cls._repair_unbalanced_json(text)
        quoted_repaired = cls._repair_missing_line_end_quotes(repaired)
        candidates = [
            ("as_written", text),
            ("removed_trailing_commas", cls._remove_trailing_json_commas(text)),
            ("repaired_missing_line_end_quotes", quoted),
            (
                "repaired_missing_line_end_quotes_and_trailing_commas",
                cls._remove_trailing_json_commas(quoted),
            ),
            ("repaired_unbalanced_delimiters", repaired),
            ("repaired_json", cls._remove_trailing_json_commas(repaired)),
            (
                "repaired_unbalanced_delimiters_and_missing_line_end_quotes",
                quoted_repaired,
            ),
            (
                "repaired_unbalanced_delimiters_missing_line_end_quotes_and_trailing_commas",
                cls._remove_trailing_json_commas(quoted_repaired),
            ),
        ]
        unique: list[tuple[str, str]] = []
        seen = set()
        for name, candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            unique.append((name, candidate))
        return unique

    @classmethod
    def _normalize_jsonish_text(cls, text: str) -> str:
        return text.translate(cls._SMART_QUOTES)

    @staticmethod
    def _tag_pattern(tag: str) -> str:
        escaped = re.escape(str(tag))
        return rf"<{escaped}>(.*?)</{escaped}>"

    @classmethod
    def extract_tag(cls, text: str, tag: str) -> str | None:
        matches = cls.extract_tags(text, tag, limit=1)
        return matches[0] if matches else None

    @classmethod
    def tag(cls, text: str, tag: str, default: str = "") -> str:
        value = cls.extract_tag(text, tag)
        return value if value is not None else default

    @classmethod
    def extract_tags(cls, text: str, tag: str, limit: int | None = None) -> List[str]:
        values: List[str] = []
        for match in re.finditer(cls._tag_pattern(tag), text or "", flags=re.DOTALL):
            values.append(match.group(1).strip())
            if limit is not None and len(values) >= limit:
                break
        return values

    @staticmethod
    def strip_tagged_sections(text: str, tags: Iterable[str]) -> str:
        escaped_tags = "|".join(re.escape(str(tag)) for tag in tags if str(tag))
        if not escaped_tags:
            return str(text or "").strip()
        pattern = rf"<({escaped_tags})>.*?</\1>\s*"
        return re.sub(pattern, "", text or "", flags=re.DOTALL).strip()

    @classmethod
    def extract_bracketed_label_text(cls, text: Any, label: str) -> str:
        normalized = cls._text(text)
        if not normalized:
            return ""
        match = re.search(
            rf"\[{re.escape(label)}\]\s*(.+)",
            normalized,
            flags=re.IGNORECASE | re.DOTALL,
        )
        return match.group(1).strip() if match else normalized

    @classmethod
    def text_from_marker(cls, text: Any, marker: str) -> str:
        normalized = cls._text(text)
        if not normalized:
            return ""
        marker = str(marker or "")
        idx = normalized.find(marker)
        return normalized[idx:].strip() if marker and idx != -1 else normalized

    @classmethod
    def parse_tagged(
        cls,
        text: str,
        tag: str,
        expected: type,
        reject_duplicates: bool = False,
        raise_on_error: bool = False,
    ) -> Any:
        return cls.parse_jsonish(
            cls.tag(text, tag),
            expected=expected,
            reject_duplicates=reject_duplicates,
            raise_on_error=raise_on_error,
        )

    @classmethod
    def parse_tagged_text_list(cls, text: str, tag: str) -> List[str]:
        block = cls.tag(text, tag)
        parsed = cls.parse_tagged(text, tag, list)
        if parsed:
            return [str(item).strip() for item in parsed if str(item).strip()]
        block = str(block or "").strip()
        return [block] if block else []

    @staticmethod
    def _opening_tag_end(text: str, tag: str) -> int | None:
        opening = re.search(rf"<{re.escape(str(tag))}>\s*", text or "", flags=re.IGNORECASE)
        return opening.end() if opening else None

    @staticmethod
    def _first_boundary_index(
        text: str,
        start: int,
        boundary_tags: Iterable[str] = (),
        boundary_markers: Iterable[str] = (),
    ) -> int:
        candidates: List[int] = []
        tail = text[start:]

        for tag in boundary_tags:
            match = re.search(rf"<{re.escape(str(tag))}>\s*", tail, flags=re.IGNORECASE)
            if match:
                candidates.append(start + match.start())

        for marker in boundary_markers:
            marker_text = str(marker or "").strip()
            marker_idx = text.find(marker_text, start) if marker_text else -1
            if marker_idx != -1:
                candidates.append(marker_idx)

        return min(candidates) if candidates else len(text)

    @classmethod
    def extract_tag_or_recover_until(
        cls,
        text: str,
        tag: str,
        boundary_tags: Iterable[str] = (),
        boundary_markers: Iterable[str] = (),
    ) -> tuple[str, bool]:
        parsed = cls.extract_tag(text, tag)
        if parsed is not None:
            return parsed, False

        text = text or ""
        start = cls._opening_tag_end(text, tag)
        if start is None:
            return "", False

        end = cls._first_boundary_index(text, start, boundary_tags, boundary_markers)
        recovered = text[start:end].strip()
        return recovered, bool(recovered)

    @staticmethod
    def _json_string_at(text: str, quote_idx: int) -> str | None:
        if quote_idx < 0 or quote_idx >= len(text) or text[quote_idx] != '"':
            return None
        escaped = False
        for idx in range(quote_idx + 1, len(text)):
            char = text[idx]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                try:
                    value = json.loads(text[quote_idx : idx + 1])
                except json.JSONDecodeError:
                    return text[quote_idx + 1 : idx]
                return str(value)
        return None

    @classmethod
    def extract_raw_json_string_value(cls, text: str, key: str) -> str | None:
        match = re.search(rf'"{re.escape(key)}"\s*:\s*"', text or "")
        return cls._json_string_at(text or "", match.end() - 1) if match else None

    @classmethod
    def strip_code_fences(cls, text: Any) -> str:
        fenced = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            cls._text(text),
            flags=re.DOTALL | re.IGNORECASE,
        )
        if fenced:
            return fenced.group(1).strip()
        return cls._text(text)

    @staticmethod
    def extract_balanced_span(text: str, opening: str, closing: str) -> str:
        start = text.find(opening)
        if start == -1:
            return text

        depth = 0
        in_string = False
        escaped = False
        for idx in range(start, len(text)):
            char = text[idx]

            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return text[start : idx + 1]
        return text[start:]

    @classmethod
    def _delimiters_for(cls, text: str, expected: type | None) -> tuple[str, str]:
        if expected in cls._DELIMITERS:
            return cls._DELIMITERS[expected]
        positions = [
            (text.find(opening), opening, closing)
            for opening, closing in cls._DELIMITERS.values()
            if text.find(opening) != -1
        ]
        if not positions:
            return "{", "}"
        _, opening, closing = min(positions, key=lambda item: item[0])
        return opening, closing

    @staticmethod
    def _empty_for(expected: type | None) -> Any:
        if expected is dict:
            return {}
        if expected is list:
            return []
        return None

    @classmethod
    def parse_jsonish(
        cls,
        raw: Any,
        expected: type | None = None,
        reject_duplicates: bool = False,
        raise_on_error: bool = False,
    ) -> Any:
        raw_text = cls.strip_code_fences(raw)
        if not raw_text:
            return cls._empty_for(expected)

        first_error: Exception | None = None
        seen_texts = set()

        for text in (raw_text, cls._normalize_jsonish_text(raw_text)):
            if text in seen_texts:
                continue
            seen_texts.add(text)

            opening, closing = cls._delimiters_for(text, expected)
            candidate = cls.extract_balanced_span(text, opening, closing)

            for repair, parseable in cls._json_parse_candidates(candidate):
                try:
                    parsed = cls._json_loads(parseable, reject_duplicates=reject_duplicates)
                except Exception as exc:
                    first_error = first_error or exc
                    continue
                if expected is None or isinstance(parsed, expected):
                    if repair != "as_written":
                        record_fallback(
                            f"parse_jsonish_{repair}",
                            "parse_jsonish",
                            f"Parsed JSON-like text after {repair.replace('_', ' ')}.",
                        )
                    return parsed

        if raise_on_error and first_error is not None:
            raise first_error
        return cls._empty_for(expected)

    @classmethod
    def parse_jsonish_array(
        cls,
        raw: Any,
        reject_duplicates: bool = False,
        raise_on_error: bool = False,
    ) -> List[Any]:
        return cls.parse_jsonish(
            raw,
            expected=list,
            reject_duplicates=reject_duplicates,
            raise_on_error=raise_on_error,
        )

    @classmethod
    def parse_jsonish_object(
        cls,
        raw: Any,
        reject_duplicates: bool = False,
        raise_on_error: bool = False,
    ) -> Dict[str, Any]:
        return cls.parse_jsonish(
            raw,
            expected=dict,
            reject_duplicates=reject_duplicates,
            raise_on_error=raise_on_error,
        )

class TaggedResponse:
    """Small convenience wrapper for prompt responses that use XML-like tags."""

    def __init__(self, text: str):
        self.text = text or ""

    def tag(self, tag: str, default: str = "") -> str:
        return StringParser.tag(self.text, tag, default)

    def object(self, tag: str) -> Dict[str, Any]:
        return StringParser.parse_tagged(self.text, tag, dict)

    def array(self, tag: str) -> List[Any]:
        return StringParser.parse_tagged(self.text, tag, list)
