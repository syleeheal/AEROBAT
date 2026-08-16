"""Run identity.

A simulation run is identified by exactly four coordinates, named as in the manuscript:

    domain d, group i, value j, repetition r

``group i`` indexes the matched configuration group -- one value combination `z_i` of the
non-hypothesized variables, held fixed while the hypothesized cause varies. ``value j`` indexes
the candidate value `x_j` of the hypothesized cause, ordered by the variable's own range, so
``j - 1`` is the level's ordinal rank. Everything else that used to travel with a run --
``simulation_index``, ``causal_rank``, ``causal_score``, ``value_set_tag``, ``variation_number``,
``batch_id`` -- was derivable from these four and is gone.

Note that ``i`` restarts at 1 in every domain, so neither ``i`` nor ``j`` identifies a run on its
own: the domain is always part of the key. ``group_id`` and ``simulation_id`` below build that in.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from ..protocol.normalization import NormalizationManager

__all__ = [
    "RunId",
    "SIMULATION_FILE_RE",
    "REVIEW_FILE_RE",
    "domain_slug",
    "group_id",
    "simulation_id",
]

SIMULATION_FILE_RE = re.compile(
    r"^simulation_i(?P<group_index>\d+)_j(?P<value_index>\d+)_rep(?P<repetition>\d+)\.json$"
)
REVIEW_FILE_RE = re.compile(
    r"^review_i(?P<group_index>\d+)_j(?P<value_index>\d+)_rep(?P<repetition>\d+)\.json$"
)


def domain_slug(value: Any) -> str:
    """Filesystem- and id-safe form of a domain name."""
    if isinstance(value, (list, tuple)):
        value = value[0] if value else ""
    return NormalizationManager.slugify(value) or "domain"


def group_id(domain: Any, group_index: Any) -> str:
    """Identifier of matched group i within a domain -- the block b of the statistical model."""
    return f"group_{domain_slug(domain)}_{_index(group_index, 'group_index')}"


def simulation_id(domain: Any, group_index: Any, value_index: Any) -> str:
    """Identifier of the run at value j of group i within a domain."""
    return (f"simulation_{domain_slug(domain)}"
            f"_{_index(group_index, 'group_index')}_{_index(value_index, 'value_index')}")


def _index(value: Any, name: str) -> int:
    return NormalizationManager.require_positive_int(value, name)


@dataclass(frozen=True, order=True)
class RunId:
    """The identity of one simulation run."""

    domain_slug: str
    group_index: int          # i
    value_index: int          # j
    repetition: int = 1       # r

    def __post_init__(self) -> None:
        object.__setattr__(self, "domain_slug", domain_slug(self.domain_slug))
        for name in ("group_index", "value_index", "repetition"):
            object.__setattr__(self, name, _index(getattr(self, name), name))

    @classmethod
    def from_mapping(cls, source: Mapping[str, Any]) -> "RunId":
        """Read a flat runtime row or a canonical artifact's ``run`` block."""
        metadata = source.get("run", source.get("metadata", source))
        if not isinstance(metadata, Mapping):
            raise ValueError("run metadata must be a mapping")
        return cls(
            domain_slug=metadata.get("domain_slug") or metadata.get("domain") or "domain",
            group_index=metadata.get("group_index", metadata.get("matched_group_index")),
            value_index=metadata.get("value_index", metadata.get("causal_value_index")),
            repetition=metadata.get("repetition", metadata.get("repetition_number", 1)),
        )

    @classmethod
    def from_filename(cls, name: str, domain: Any) -> "RunId":
        match = SIMULATION_FILE_RE.match(name) or REVIEW_FILE_RE.match(name)
        if not match:
            raise ValueError(f"Unrecognized artifact filename: {name}")
        return cls(domain, *(int(match.group(key))
                             for key in ("group_index", "value_index", "repetition")))

    @property
    def key(self) -> tuple[str, int, int]:
        """Identity without the repetition: which configured cell this run instantiates."""
        return (self.domain_slug, self.group_index, self.value_index)

    @property
    def group_id(self) -> str:
        return group_id(self.domain_slug, self.group_index)

    @property
    def simulation_id(self) -> str:
        return simulation_id(self.domain_slug, self.group_index, self.value_index)

    @property
    def level_position(self) -> int:
        """Zero-based ordinal position of candidate value :math:`x_j`."""
        return self.value_index - 1

    @property
    def simulation_filename(self) -> str:
        return f"simulation_i{self.group_index}_j{self.value_index}_rep{self.repetition}.json"

    @property
    def review_filename(self) -> str:
        return f"review_i{self.group_index}_j{self.value_index}_rep{self.repetition}.json"

    def as_dict(self) -> dict[str, Any]:
        """The four coordinates, as they are written into every artifact."""
        return {
            "domain_slug": self.domain_slug,
            "group_index": self.group_index,
            "value_index": self.value_index,
            "repetition": self.repetition,
        }

    def label(self) -> str:
        return (f"{self.domain_slug} group {self.group_index} value {self.value_index}"
                f" rep {self.repetition}")
