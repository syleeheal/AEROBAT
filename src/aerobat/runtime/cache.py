"""Prompt-cache key construction helpers."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from typing import Any

from ..protocol.constants import KEY_DIGEST_LENGTH, MAX_PROMPT_CACHE_KEY_LENGTH
from ..protocol.normalization import NormalizationManager


def configured_cache_key(value: Any) -> str:
    text = str(value or "").strip()
    return "" if not text or text.upper() == "NA" else text


def prompt_cache_key(configured_key: Any, *parts: Any) -> str:
    suffix = ":".join(
        NormalizationManager.slugify(str(part))
        for part in parts
        if str(part or "").strip()
    )
    base = configured_cache_key(configured_key)
    key = f"{base}:{suffix}" if base and suffix else base or suffix
    if len(key) <= MAX_PROMPT_CACHE_KEY_LENGTH:
        return key

    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:KEY_DIGEST_LENGTH]
    prefix_length = MAX_PROMPT_CACHE_KEY_LENGTH - KEY_DIGEST_LENGTH - 1
    return f"{key[:prefix_length]}:{digest}"


def compact_sequence_id(value: Any) -> str:
    """Shorten a group_id / simulation_id for use inside a prompt-cache key."""
    text = str(value or "").strip()
    return text.replace("group_", "g").replace("simulation_", "s")


def settings_with_cache_key(settings: Any, *parts: Any) -> Any:
    return replace(
        settings,
        prompt_cache_key=prompt_cache_key(settings.prompt_cache_key, *parts),
    )
