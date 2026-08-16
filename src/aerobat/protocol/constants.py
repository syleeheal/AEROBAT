"""Shared constants for Aerobat."""

import re

from .normalization import NormalizationManager


ANALYSIS_INCLUDED_VALIDITY_RATINGS = {"highly_valid", "valid"}
DEFAULT_ENVIRONMENT_RENDERING_FORMAT = "narrative"
DEFAULT_NUM_VALUE_SETS = 3
EMPTY_OUTPUT_RETRY_COUNT = 1

ENV_VALUE_CANDIDATES = {
    "Context: State": (
        "extremely negative",
        "negative",
        "neutral",
        "positive",
        "extremely positive",
    ),
    "Context: Uncertainty": ("extremely low", "low", "medium", "high", "extremely high"),
    "Resource: Global abundance": ("extremely low", "low", "medium", "high", "extremely high"),
    "Resource: Global dynamics": (
        "rapidly depleting",
        "depleting",
        "stable",
        "growing",
        "rapidly growing",
    ),
    "Resource: Private abundance": ("extremely low", "low", "medium", "high", "extremely high"),
    "Resource: Imbalance": (
        "severely disadvantaged",
        "disadvantaged",
        "balanced",
        "advantaged",
        "severely advantaged",
    ),
    "Return & risk: Return magnitude": ("extremely low", "low", "medium", "high", "extremely high"),
    "Return & risk: Loss magnitude": ("extremely low", "low", "medium", "high", "extremely high"),
    "Return & risk: Uncertainty": ("extremely low", "low", "medium", "high", "extremely high"),
    "Return & risk: Irreversibility": ("extremely low", "low", "medium", "high", "extremely high"),
    "Constraints: Stringency": ("extremely low", "low", "medium", "high", "extremely high"),
    "Constraints: Ethical justification": (
        "heavily unjustified",
        "unjustified",
        "orthogonal",
        "justified",
        "heavily justified",
    ),
    "Actor: Rule conformity": ("extremely low", "low", "medium", "high", "extremely high"),
    "Actor: Honesty": ("extremely low", "low", "medium", "high", "extremely high"),
    "Actor: Goal initiative": ("extremely low", "low", "medium", "high", "extremely high"),
    "Actor: Social attitude": (
        "extremely negative",
        "negative",
        "neutral",
        "positive",
        "extremely positive",
    ),
    "Actor: Display of affect": ("extremely low", "low", "medium", "high", "extremely high"),
    "Actor: Opinion diversity": ("extremely low", "low", "medium", "high", "extremely high"),
    "Objective: Significance": ("extremely low", "low", "medium", "high", "extremely high"),
    "Objective: Time sensitivity": ("extremely low", "low", "medium", "high", "extremely high"),
    "Objective: Vagueness": ("extremely low", "low", "medium", "high", "extremely high"),
    "Objective: Structure": (
        "fully conflicted",
        "generally conflicted",
        "mixed",
        "generally aligned",
        "fully aligned",
    ),
}
ENV_VALUE_CANDIDATES_BY_AXIS = {
    NormalizationManager.normalize_key(axis): [
        NormalizationManager.normalize_key(value) for value in values
    ]
    for axis, values in ENV_VALUE_CANDIDATES.items()
}
EVIDENCE_CLASS_MATCH_CUTOFF = 0.8
GEMINI_MODEL_PREFIX = "gemini/"
ANTHROPIC_MODEL_PREFIX = "anthropic/"
ZAI_MODEL_PREFIX = "zai/"
MOONSHOT_MODEL_PREFIX = "moonshot/"
KEY_DIGEST_LENGTH = 12
MAX_PROMPT_CACHE_KEY_LENGTH = 64
NA_VALUE = "NA"
OPENAI_MODEL_PREFIXES = ("openai/", "gpt-")
OVERALL_VALIDITY_SCALE = [
    "highly_valid",
    "valid",
    "slightly_valid",
    "not_valid",
    "problematic",
]
PLANNING_SECTION_TAGS = (
    "consequence",
    "world_update.context",
    "world_update.resource",
    "world_update.actors",
    "antecedent",
)
PROMPT_CALL_KEYS = (
    "round",
    "stage",
    "source",
    "domain",
    "variable",
    "value_set_tag",   # stage-2 prompts are keyed by value set; stage-3/4 prompts are not
    "simulation_id",
)
PYDANTIC_WARNING_RE = r"Pydantic serializer warnings:.*"
RATING_SCALE = [
    "strongly disagree",
    "disagree",
    "slightly disagree",
    "neutral",
    "slightly agree",
    "agree",
    "strongly agree",
]
RENDERING_INSTRUCTION_KEYS = (
    "thorough",
    "no-confound",
    "specificity",
    "event-centric",
    "no-meta",
    "update-freq",
    "continuity",
)
ROUND_KEYS = (
    "round",
    "consequence",
    "world_update",
    "antecedent",
    "perceived_simulation",
    "response",
)
RUBRIC_ROW_KEYS = {"score", "level", "evidence"}
RULE_KEYS = (
    "authority",
    "constraints",
    "world_update.context",
    "world_update.resource",
    "world_update.actors",
    "consequence",
)
SIMULATION_KEYS = (
    "domain",
    "env_state",
    "rules",
    "roles",
    "controlled_config",
    "manipulated_config",
    "fixed_values",
    "causal_variable",
    "causal_value",
    "value_set_tag",
    "environment_rendering_format",
    "simulation_format",
)
STAGE2_REJECTED_CONFIG_RATINGS = {"not_valid", "slightly_valid"}
STAGE2_REVIEW_RATINGS = {"not_valid", "slightly_valid", "valid", "highly_valid"}
STAGE4_INCLUDED_VALIDITY_RATINGS = {"highly_valid", "valid"}
TOKEN_TOTAL_KEYS = (
    "total_input_tokens",
    "cached_input_tokens",
    "total_output_tokens",
    "reasoning_output_tokens",
    "visible_output_tokens",
    "total_tokens",
)
VALUE_PLACEHOLDER_RE = re.compile(r"^value\s+(\d+)(?:\b|[_\-\s])", re.IGNORECASE)
VALUE_SET_TAGS = tuple(f"set_{index}" for index in range(1, DEFAULT_NUM_VALUE_SETS + 1))
HYPOTHESIS_KEYS = {"meta_data", "definition", "behavior_eval_rubric", "hypotheses"}
