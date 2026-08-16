"""LLM API calls, provider options, and shared runtime helpers."""

from __future__ import annotations

import asyncio
import logging
import warnings
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import litellm

from ..protocol.constants import (
    ANTHROPIC_MODEL_PREFIX,
    EMPTY_OUTPUT_RETRY_COUNT,
    GEMINI_MODEL_PREFIX,
    MOONSHOT_MODEL_PREFIX,
    NA_VALUE,
    OPENAI_MODEL_PREFIXES,
    PYDANTIC_WARNING_RE,
    ZAI_MODEL_PREFIX,
)

logger = logging.getLogger(__name__)

__all__ = [
    "LLMResponse",
    "StructuredLLMResponse",
    "llm_call",
    "llm_call_kwargs",
    "llm_call_with_metadata",
    "llm_structured_call",
    "limited_llm_call",
    "limited_llm_call_with_metadata",
    "limited_structured_llm_call",
    "make_llm_call_kwargs",
    "resolve_research_manager_settings",
    "resolve_stage_llm_settings",
    "StageLLMSettings",
]


@dataclass(frozen=True)
class LLMResponse:
    """Visible response text plus optional provider-returned reasoning summary."""

    text: str
    reasoning_summary: str = ""
    token_counts: Dict[str, Any] | None = None
    response_id: str = ""


@dataclass(frozen=True)
class StructuredLLMResponse:
    """Raw structured-response text plus the caller-parsed payload."""

    text: str
    parsed: Any
    token_counts: Dict[str, Any] | None = None
    response_id: str = ""


@dataclass(frozen=True)
class StageLLMSettings:
    """Resolved model-call settings for one pipeline stage or reviewer."""

    model: str
    temperature: float
    max_tokens: int
    reasoning_effort: str = NA_VALUE
    reasoning_summary: str = NA_VALUE
    service_tier: str = NA_VALUE
    prompt_cache_key: str = NA_VALUE
    prompt_cache_retention: str = NA_VALUE


def _section(config: Dict[str, Any], name: str) -> Dict[str, Any]:
    value = config.get(name, {}) if isinstance(config, dict) else {}
    return value if isinstance(value, dict) else {}


def _required_temperature(section_cfg: Dict[str, Any], section: str) -> float:
    if "temperature" not in section_cfg:
        raise ValueError(f"{section}.temperature must be configured.")
    return float(section_cfg["temperature"])


def resolve_stage_llm_settings(
    config: Dict[str, Any],
    section: str,
    *,
    default_model: str = "openai/gpt-5.1",
    default_max_tokens: int = 10000,
) -> StageLLMSettings:
    """Resolve common model-call settings from a named config section."""

    stage_cfg = _section(config, section)
    return StageLLMSettings(
        model=stage_cfg.get("model", default_model),
        temperature=_required_temperature(stage_cfg, section),
        max_tokens=int(stage_cfg.get("max_tokens", default_max_tokens)),
        reasoning_effort=stage_cfg.get("reasoning_effort", NA_VALUE),
        reasoning_summary=stage_cfg.get("reasoning_summary", NA_VALUE),
        service_tier=stage_cfg.get("service_tier", config.get("service_tier", NA_VALUE)),
        prompt_cache_key=stage_cfg.get("prompt_cache_key", NA_VALUE),
        prompt_cache_retention=stage_cfg.get("prompt_cache_retention", NA_VALUE),
    )


def resolve_research_manager_settings(
    config: Dict[str, Any],
    stage: str | int,
    *,
    default_max_tokens: int = 10000,
) -> StageLLMSettings:
    """Resolve research-manager model-call settings."""

    manager_cfg = _section(config, "research_manager")
    stages_cfg = manager_cfg.get("stages", {})
    stages_cfg = stages_cfg if isinstance(stages_cfg, dict) else {}
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
    stage_cfg = stages_cfg.get(stage_key, {})
    stage_cfg = stage_cfg if isinstance(stage_cfg, dict) else {}
    return StageLLMSettings(
        model=manager_cfg.get("model", "openai/gpt-5.1"),
        temperature=_required_temperature(manager_cfg, "research_manager"),
        max_tokens=int(manager_cfg.get("max_tokens", default_max_tokens)),
        reasoning_effort=stage_cfg.get("reasoning_effort", manager_cfg.get("reasoning_effort", NA_VALUE)),
        service_tier=manager_cfg.get("service_tier", config.get("service_tier", NA_VALUE)),
        prompt_cache_key=manager_cfg.get("prompt_cache_key", NA_VALUE),
        prompt_cache_retention=manager_cfg.get("prompt_cache_retention", NA_VALUE),
    )


def llm_call_kwargs(settings: StageLLMSettings) -> Dict[str, Any]:
    """Convert settings to kwargs, omitting unset optional provider controls."""

    kwargs: Dict[str, Any] = {
        "model": settings.model,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }
    if settings.reasoning_effort != NA_VALUE:
        kwargs["reasoning_effort"] = settings.reasoning_effort
    if settings.reasoning_summary != NA_VALUE:
        kwargs["reasoning_summary"] = settings.reasoning_summary
    if settings.service_tier != NA_VALUE:
        kwargs["service_tier"] = settings.service_tier

    cache_key = str(settings.prompt_cache_key or "").strip()
    if cache_key and cache_key.upper() != NA_VALUE:
        kwargs["prompt_cache_key"] = cache_key

    cache_retention = str(settings.prompt_cache_retention or "").strip()
    if cache_retention and cache_retention.upper() != NA_VALUE:
        kwargs["prompt_cache_retention"] = cache_retention

    return kwargs


def make_llm_call_kwargs(
    model: str,
    temperature: float,
    max_tokens: int,
    reasoning_effort: str = NA_VALUE,
    reasoning_summary: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> Dict[str, Any]:
    """Build LLM call kwargs from scalar stage/runtime values."""

    return llm_call_kwargs(
        StageLLMSettings(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
            reasoning_summary=reasoning_summary,
            service_tier=service_tier,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
        )
    )


async def llm_call(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4000,
    reasoning_effort: str = NA_VALUE,
    reasoning_summary: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> str:
    """Call an LLM through LiteLLM and retry once if the output is empty."""
    response = await llm_call_with_metadata(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
        reasoning_summary=reasoning_summary,
        service_tier=service_tier,
        prompt_cache_key=prompt_cache_key,
        prompt_cache_retention=prompt_cache_retention,
    )
    return response.text


async def llm_call_with_metadata(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4000,
    reasoning_effort: str = NA_VALUE,
    reasoning_summary: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> LLMResponse:
    """Call an LLM and retain optional response metadata such as reasoning summary."""
    if _configured_option(reasoning_summary) and _uses_responses_api(model):
        return await _responses_text_with_empty_retry(
            _responses_kwargs(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                reasoning_effort=reasoning_effort,
                reasoning_summary=reasoning_summary,
                service_tier=service_tier,
                prompt_cache_key=prompt_cache_key,
                prompt_cache_retention=prompt_cache_retention,
            )
        )

    return await _completion_response_with_empty_retry(
        _completion_kwargs(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
            service_tier=service_tier,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
        )
    )


async def llm_structured_call(
    messages: List[Dict[str, str]],
    model: str,
    response_format: Dict[str, Any],
    parser: Callable[[str], Any],
    temperature: float = 0.7,
    max_tokens: int = 4000,
    reasoning_effort: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> StructuredLLMResponse:
    """Call an LLM with a response schema and retry once on empty payloads."""
    litellm_model = _normalize_litellm_model(model)
    if not litellm.supports_response_schema(litellm_model):
        raise ValueError(f"Model {model!r} does not support structured response schemas.")

    return await _structured_completion_with_empty_retry(
        _completion_kwargs(
            messages=messages,
            model=litellm_model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
            reasoning_effort=reasoning_effort,
            service_tier=service_tier,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
        ),
        parser,
    )


async def limited_llm_call(
    messages: List[Dict[str, str]],
    *,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    **kwargs: Any,
) -> str:
    """Run an LLM call behind an optional semaphore."""

    if llm_semaphore is None:
        return await llm_call(messages, **kwargs)
    async with llm_semaphore:
        return await llm_call(messages, **kwargs)


async def limited_llm_call_with_metadata(
    messages: List[Dict[str, str]],
    *,
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    **kwargs: Any,
) -> LLMResponse:
    """Run a metadata-preserving LLM call behind an optional semaphore."""

    if llm_semaphore is None:
        return await llm_call_with_metadata(messages, **kwargs)
    async with llm_semaphore:
        return await llm_call_with_metadata(messages, **kwargs)


async def limited_structured_llm_call(
    messages: List[Dict[str, str]],
    *,
    response_format: Dict[str, Any],
    parser: Callable[[str], Any],
    llm_semaphore: Optional[asyncio.Semaphore] = None,
    **kwargs: Any,
) -> StructuredLLMResponse:
    """Run a structured LLM call behind an optional semaphore."""

    if llm_semaphore is None:
        return await llm_structured_call(
            messages,
            response_format=response_format,
            parser=parser,
            **kwargs,
        )
    async with llm_semaphore:
        return await llm_structured_call(
            messages,
            response_format=response_format,
            parser=parser,
            **kwargs,
        )


def _completion_kwargs(
    *,
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_tokens: int,
    response_format: Dict[str, Any] | None = None,
    reasoning_effort: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> Dict[str, Any]:
    litellm_model = _normalize_litellm_model(model)
    kwargs: Dict[str, Any] = {
        "model": litellm_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format

    _apply_reasoning_effort(kwargs, model=litellm_model, reasoning_effort=reasoning_effort)
    _apply_openai_options(
        kwargs,
        model=litellm_model,
        service_tier=service_tier,
        prompt_cache_key=prompt_cache_key,
        prompt_cache_retention=prompt_cache_retention,
    )
    return kwargs


def _responses_kwargs(
    *,
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_tokens: int,
    reasoning_effort: str = NA_VALUE,
    reasoning_summary: str = NA_VALUE,
    service_tier: str = NA_VALUE,
    prompt_cache_key: str = NA_VALUE,
    prompt_cache_retention: str = NA_VALUE,
) -> Dict[str, Any]:
    instructions, input_messages = _split_responses_messages(messages)
    kwargs: Dict[str, Any] = {
        "model": _normalize_litellm_model(model),
        "input": input_messages,
        "temperature": temperature,
        "max_output_tokens": max_tokens,
        "reasoning": {"summary": _configured_option(reasoning_summary)},
    }
    if instructions:
        kwargs["instructions"] = instructions

    effort = _configured_option(reasoning_effort)
    if effort:
        kwargs["reasoning"]["effort"] = effort

    _apply_openai_options(
        kwargs,
        model=str(kwargs["model"]),
        service_tier=service_tier,
        prompt_cache_key=prompt_cache_key,
        prompt_cache_retention=prompt_cache_retention,
    )
    return kwargs


async def _run_acompletion(kwargs: Dict[str, Any]) -> Any:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=PYDANTIC_WARNING_RE,
            category=UserWarning,
            module=r"pydantic\.main",
        )
        return await litellm.acompletion(**kwargs)


async def _run_aresponses(kwargs: Dict[str, Any]) -> Any:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=PYDANTIC_WARNING_RE,
            category=UserWarning,
            module=r"pydantic\.main",
        )
        return await litellm.aresponses(**kwargs)


def _completion_response(response: Any) -> LLMResponse:
    message = response.choices[0].message
    return LLMResponse(
        text=_coerce_message_content(_field(message, "content")),
        reasoning_summary=str(_field(message, "reasoning_content", "") or "").strip(),
        token_counts=_extract_token_counts(response),
        response_id=str(_field(response, "id", "") or ""),
    )


async def _completion_response_with_empty_retry(kwargs: Dict[str, Any]) -> LLMResponse:
    result = LLMResponse(text="")
    for _ in range(EMPTY_OUTPUT_RETRY_COUNT + 1):
        result = _completion_response(await _run_acompletion(kwargs))
        if not _is_empty_text(result.text):
            break
    return result


# async def _responses_text_with_empty_retry(kwargs: Dict[str, Any]) -> LLMResponse:
#     result = LLMResponse(text="")
#     for _ in range(EMPTY_OUTPUT_RETRY_COUNT + 1):
#         result = _responses_response(await _run_aresponses(kwargs))
#         if not _is_empty_text(result.text):
#             break
#     return result

async def _responses_text_with_empty_retry(kwargs: Dict[str, Any]) -> LLMResponse:
    result = LLMResponse(text="")
    for _ in range(EMPTY_OUTPUT_RETRY_COUNT + 1):
        try:
            result = _responses_response(await _run_aresponses(kwargs))
        except litellm.BadRequestError as e:
            # Flex tier intermittently rejects requests with this error; fall back to default tier.
            if "Invalid service_tier" in str(e) and kwargs.get("service_tier") == "flex":
                fallback_kwargs = {**kwargs, "service_tier": "default"}
                logger.info("Retrying Responses API call with service_tier='default'.")
                result = _responses_response(await _run_aresponses(fallback_kwargs))
            else:
                raise
        if not _is_empty_text(result.text):
            break
    return result


async def _structured_completion_with_empty_retry(
    kwargs: Dict[str, Any],
    parser: Callable[[str], Any],
) -> StructuredLLMResponse:
    result = StructuredLLMResponse(text="", parsed=None)
    for _ in range(EMPTY_OUTPUT_RETRY_COUNT + 1):
        response = _completion_response(await _run_acompletion(kwargs))
        text = response.text
        result = StructuredLLMResponse(
            text=text,
            parsed=parser(text),
            token_counts=response.token_counts,
            response_id=response.response_id,
        )
        if not _is_empty_structured_response(result):
            break
    return result


def _is_empty_text(text: Any) -> bool:
    return not str(text or "").strip()


def _is_empty_structured_response(response: StructuredLLMResponse) -> bool:
    if _is_empty_text(response.text):
        return True
    return isinstance(response.parsed, (dict, list, tuple, set)) and not response.parsed


def _responses_response(response: Any) -> LLMResponse:
    return LLMResponse(
        text=_coerce_message_content(_field(response, "output_text")),
        reasoning_summary=_extract_responses_reasoning_summary(response),
        token_counts=_extract_token_counts(response),
        response_id=str(_field(response, "id", "") or ""),
    )


def _split_responses_messages(messages: List[Dict[str, str]]) -> tuple[str, List[Dict[str, str]]]:
    instructions: List[str] = []
    input_messages: List[Dict[str, str]] = []
    for message in messages:
        role = str(message.get("role", "user"))
        content = _coerce_message_content(message.get("content"))
        if role == "system":
            instructions.append(content)
        else:
            input_messages.append({"role": role, "content": content})
    return "\n\n".join(part for part in instructions if part), input_messages


def _normalize_litellm_model(model: str) -> str:
    model_name = str(model or "").strip()
    if not model_name:
        return model_name

    # Gemini (Google)
    if model_name.startswith(GEMINI_MODEL_PREFIX):
        return model_name
    if model_name.startswith("models/gemini-"):
        return f"{GEMINI_MODEL_PREFIX}{model_name.removeprefix('models/')}"
    if model_name.startswith("google/gemini-"):
        return f"{GEMINI_MODEL_PREFIX}{model_name.removeprefix('google/')}"
    if model_name.startswith("gemini-"):
        return f"{GEMINI_MODEL_PREFIX}{model_name}"

    # Claude (Anthropic): claude-... -> anthropic/claude-...
    if model_name.startswith("claude-"):
        return f"{ANTHROPIC_MODEL_PREFIX}{model_name}"

    # GLM (z.ai): glm-... -> zai/glm-...
    if model_name.startswith("glm-"):
        return f"{ZAI_MODEL_PREFIX}{model_name}"

    # KIMI (Moonshot): kimi-... / moonshot-... -> moonshot/...
    if model_name.startswith("kimi-") or model_name.startswith("moonshot-"):
        return f"{MOONSHOT_MODEL_PREFIX}{model_name}"

    return model_name


def _uses_responses_api(model: str) -> bool:
    """The OpenAI Responses API is provider-specific; every other provider
    (Anthropic, z.ai/GLM, Moonshot/KIMI, Gemini, ...) uses chat completions,
    so reasoning summaries for those models come back via ``reasoning_content``.
    """
    return _normalize_litellm_model(model).startswith(OPENAI_MODEL_PREFIXES)


def _apply_reasoning_effort(
    kwargs: Dict[str, Any],
    *,
    model: str,
    reasoning_effort: str,
) -> None:
    effort = _configured_option(reasoning_effort)
    if not effort:
        return
    # Moonshot/KIMI models report supports_reasoning()=True (they think natively and
    # return reasoning_content by default), but the moonshot provider rejects the
    # reasoning_effort request parameter itself, raising UnsupportedParamsError. Skip
    # forwarding it; the reasoning content still comes back via reasoning_content.
    if _normalize_litellm_model(model).startswith(MOONSHOT_MODEL_PREFIX):
        return
    if litellm.supports_reasoning(model):
        kwargs["reasoning_effort"] = effort


def _apply_openai_options(
    kwargs: Dict[str, Any],
    *,
    model: str,
    service_tier: str,
    prompt_cache_key: str,
    prompt_cache_retention: str,
) -> None:
    if not str(model or "").startswith(OPENAI_MODEL_PREFIXES):
        return

    option_map = {
        "service_tier": service_tier,
        "prompt_cache_key": prompt_cache_key,
        "prompt_cache_retention": prompt_cache_retention,
    }
    for key, raw_value in option_map.items():
        value = _configured_option(raw_value)
        if value:
            kwargs[key] = value


def _configured_option(value: Any) -> str:
    text = str(value or "").strip()
    return "" if not text or text.upper() == NA_VALUE else text


def _field(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _plain_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump()
        return dumped if isinstance(dumped, dict) else {}
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        dumped = to_dict()
        return dumped if isinstance(dumped, dict) else {}
    return {
        key: getattr(value, key)
        for key in dir(value)
        if not key.startswith("_") and not callable(getattr(value, key, None))
    }


def _int_field(mapping: Dict[str, Any], *keys: str) -> int:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def _extract_token_counts(response: Any) -> Dict[str, Any] | None:
    usage = _plain_mapping(_field(response, "usage"))
    if not usage:
        return None

    input_details = _plain_mapping(
        usage.get("input_tokens_details") or usage.get("prompt_tokens_details")
    )
    output_details = _plain_mapping(
        usage.get("output_tokens_details") or usage.get("completion_tokens_details")
    )
    input_tokens = _int_field(usage, "input_tokens", "prompt_tokens")
    output_tokens = _int_field(usage, "output_tokens", "completion_tokens")
    reasoning_tokens = _int_field(output_details, "reasoning_tokens")
    cached_input_tokens = _int_field(input_details, "cached_tokens")
    total_tokens = _int_field(usage, "total_tokens")
    if not total_tokens:
        total_tokens = input_tokens + output_tokens

    return {
        "total_input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "total_output_tokens": output_tokens,
        "reasoning_output_tokens": reasoning_tokens,
        "visible_output_tokens": max(output_tokens - reasoning_tokens, 0),
        "total_tokens": total_tokens,
    }


def _extract_responses_reasoning_summary(response: Any) -> str:
    summaries: List[str] = []
    for item in _field(response, "output", []) or []:
        if _field(item, "type") != "reasoning":
            continue
        for summary in _field(item, "summary", []) or []:
            text = str(_field(summary, "text", "") or "").strip()
            if text:
                summaries.append(text)
    return "\n".join(summaries)


def _coerce_message_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            if isinstance(item, dict):
                text_value = item.get("text")
                if isinstance(text_value, str):
                    parts.append(text_value)
                    continue
            parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)
