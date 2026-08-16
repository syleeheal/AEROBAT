"""Small concurrency primitives shared by pipeline stages."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


async def gather_after_first(
    items: Sequence[Input],
    operation: Callable[[Input], Awaitable[Output]],
    *,
    return_exceptions: bool = False,
) -> list[Output | Exception]:
    """Warm a shared prompt prefix with the first call, then run the rest together."""
    if not items:
        return []

    try:
        first: Output | Exception = await operation(items[0])
    except Exception as exc:
        if not return_exceptions:
            raise
        first = exc
    remaining = await asyncio.gather(
        *(operation(item) for item in items[1:]),
        return_exceptions=return_exceptions,
    )
    return [first, *remaining]
