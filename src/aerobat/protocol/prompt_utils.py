"""Small prompt-formatting helpers shared across stages."""

from __future__ import annotations

import json
import re
from typing import Any


def _align(text: str) -> str:
    """
    Strip code indentation and collapse repeated horizontal whitespace in prompts.
    """
    lines = text.splitlines()
    margin = ""
    for line in lines:
        if line.strip():
            margin = line[: len(line) - len(line.lstrip())]
            break
    if margin:
        aligned = [line[len(margin):] if line.startswith(margin) else line for line in lines]
    else:
        aligned = lines
    aligned_text = "\n".join(aligned)
    normalized_text = re.sub(r"[^\S\r\n]{2,}", " ", aligned_text)
    return normalized_text + ("\n" if text.endswith("\n") else "")


def stringify_value(value: Any) -> str:
    """Render prompt payloads consistently."""
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return prompt_json(value)
    return str(value)


def prompt_json(value: Any, *, indent: int = 2, sort_keys=False) -> str:
    """Render JSON payloads with stable key ordering for prompt-cache prefixes."""
    return json.dumps(value, ensure_ascii=False, indent=indent, sort_keys=sort_keys)


def build_agent_init_block(
    rules: Any = None,
    subject_agent_role: Any = None,
) -> str:
    """Render role, authority, and constraints for Subject Agent."""
    role_text = stringify_value(subject_agent_role).strip()
    if isinstance(rules, dict):
        authority_text = stringify_value(rules.get("authority")).strip()
        constraints_text = stringify_value(rules.get("constraints")).strip()
    else:
        authority_text = ""
        constraints_text = stringify_value(rules).strip()
    if not role_text and not authority_text and not constraints_text:
        return ""

    return _align(f"""\
        - Your role: {role_text or "Not provided."}
        - Your authority: {authority_text or "Not provided."}
        - Your constraints: {constraints_text or "Not provided."}
    """)
