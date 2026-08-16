"""Shared utilities for config files, JSON I/O, and IDs."""

from __future__ import annotations

import json
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Sequence

from aerobat.protocol.normalization import NormalizationManager

__all__ = [
    "collect_fallbacks",
    "config_section",
    "load_behavior_description",
    "load_json",
    "mapping_records",
    "mapping_value",
    "mean_or_none",
    "now",
    "positive_int_setting",
    "record_fallback",
    "research_manager_gate_enabled",
    "save_json",
]


# ---------------------------------------------------------------------------
# Fallback tracking
# ---------------------------------------------------------------------------


_fallbacks_var: ContextVar[List[Dict[str, Any]] | None] = ContextVar(
    "aerobat_fallbacks",
    default=None,
)


def _normalize_fallback_details(details: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in details.items():
        if value is not None:
            normalized[key] = value
    return normalized


def record_fallback(
    code: str,
    function: str,
    message: str,
    **details: Any,
) -> None:
    """
    Purpose: Record a problematic fallback event in the active collection scope.
    Logic: Deduplicates identical entries within the current scope and increments a count.
    """
    active = _fallbacks_var.get()
    if active is None:
        return

    entry = {
        "code": code,
        "function": function,
        "message": message,
        **_normalize_fallback_details(details),
    }
    key = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    for existing in active:
        existing_key = json.dumps(
            {k: v for k, v in existing.items() if k != "count"},
            sort_keys=True,
            ensure_ascii=False,
        )
        if existing_key == key:
            existing["count"] = int(existing.get("count", 1)) + 1
            return

    active.append({**entry, "count": 1})


@contextmanager
def collect_fallbacks() -> Iterator[List[Dict[str, Any]]]:
    """
    Purpose: Collect fallback events within a bounded execution scope.
    Logic: Installs an isolated list in a context variable and restores the previous scope afterward.
    """
    token = _fallbacks_var.set([])
    try:
        active = _fallbacks_var.get()
        assert active is not None
        yield active
    finally:
        _fallbacks_var.reset(token)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def mapping_value(value: Any) -> Mapping[str, Any]:
    """Return mapping values as-is and coerce everything else to an empty mapping."""
    return value if isinstance(value, Mapping) else {}


def mapping_records(value: Any) -> List[Dict[str, Any]]:
    """Return only dict records from a list-like payload."""
    if not isinstance(value, list):
        return []
    return [row for row in value if isinstance(row, dict)]


def mean_or_none(
    values: Sequence[int | float],
    *,
    digits: int | None = None,
) -> float | None:
    """Return a numeric mean, optionally rounded, or ``None`` for no observations."""
    if not values:
        return None
    mean = sum(values) / len(values)
    return round(mean, digits) if digits is not None else mean


def config_section(config: Mapping[str, Any], name: str) -> Dict[str, Any]:
    """Return a config section as a mutable dict, or an empty dict when absent."""
    value = config.get(name, {})
    return dict(value) if isinstance(value, Mapping) else {}


def positive_int_setting(
    config: Mapping[str, Any],
    section: str,
    key: str,
    default: int,
) -> int:
    """Read a positive integer setting from a config section."""
    value = config_section(config, section).get(key, default)
    parsed = NormalizationManager.positive_int(value)
    if parsed is None:
        raise ValueError(f"{section}.{key} must be a positive integer, got {value!r}")
    return parsed


def research_manager_gate_enabled(config: Mapping[str, Any], stage: str | int) -> bool:
    """Resolve the per-stage research-manager switch."""
    manager_cfg = config.get("research_manager", {}) if isinstance(config, Mapping) else {}
    if not isinstance(manager_cfg, Mapping):
        return True

    if isinstance(stage, int):
        stage_key = f"stage_{stage}"
    else:
        stage_key = str(stage).strip().lower().replace("-", "_")
        if stage_key.isdigit():
            stage_key = f"stage_{stage_key}"
        elif stage_key.startswith("stage") and not stage_key.startswith("stage_"):
            suffix = stage_key[5:]
            if suffix.isdigit():
                stage_key = f"stage_{suffix}"

    stages_cfg = manager_cfg.get("stages", {})
    stages_cfg = stages_cfg if isinstance(stages_cfg, Mapping) else {}
    stage_cfg = stages_cfg.get(stage_key, manager_cfg.get(stage_key, True))
    if isinstance(stage_cfg, Mapping):
        return bool(stage_cfg.get("enabled", True))
    return bool(stage_cfg)


def load_behavior_description(name: str, data_dir: str | Path) -> str:
    """Return a behavior description from ``data_dir/behaviors.json`` if present."""
    behaviors_path = Path(data_dir) / "behaviors.json"
    if not behaviors_path.exists():
        return ""
    try:
        with open(behaviors_path, "r", encoding="utf-8") as f:
            behaviors = json.load(f)
        return behaviors.get(name, "")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------


def save_json(data: Any, path: str | Path, indent: int = 2) -> Path:
    """Write JSON to disk, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    return path


def load_json(path: str | Path) -> Any:
    """Read a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# IDs / timestamps
# ---------------------------------------------------------------------------


def now() -> str:
    """Return the current local timestamp as ISO-8601 text."""
    return datetime.now().isoformat()
