"""rate_limiter — sample-проект vertical slice WARRANT (ADR-0039).

Ограничитель частоты запросов по схеме token bucket (spec `rate-limiter`, REQ-RL-001, REQ-RL-002): по каждому ключу
запас до N, пополнение со скоростью N/W в секунду по внедряемому источнику времени.

Ограничения: только для вызова из одного потока; состояние ключей хранится в памяти и не вытесняется.
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable, Hashable

__all__ = ["RateLimiter"]

_MAX_LIMIT = 2**53


def _finite_seconds(value: object, what: str) -> float:
    """Значение секунд (REQ-RL-001, UNK-RL-002): `int`/`float` (не `bool`), которое конечный double представляет точно;
    иначе `ValueError`."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{what} must be an int or float, got {value!r}")
    try:
        seconds = float(value)
    except OverflowError:
        raise ValueError(f"{what} is out of the float range: {value!r}") from None
    if not math.isfinite(seconds):
        raise ValueError(f"{what} must be finite, got {value!r}")
    # Сравнение int с float в Python точное: ложно ровно для int, которое double не представляет (2**53 + 1).
    if seconds != value:
        raise ValueError(f"{what} is not exactly representable as a float: {value!r}")
    return seconds


class RateLimiter:
    """Token bucket: не больше N запросов подряд по ключу, пополнение N запросов за окно W секунд."""

    def __init__(self, limit: int, window: float, clock: Callable[[], float] | None = None) -> None:
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= _MAX_LIMIT:
            raise ValueError(f"limit must be an int from 1 to 2**53, got {limit!r}")
        seconds = _finite_seconds(window, "window")
        if seconds <= 0:
            raise ValueError(f"window must be greater than zero, got {window!r}")
        if clock is None:
            clock = time.monotonic
        elif not callable(clock):
            raise TypeError(f"clock must be callable or None, got {clock!r}")
        self._limit = float(limit)
        self._window = seconds
        self._clock = clock
        # key -> (запас, отметка времени последнего обработанного запроса)
        self._buckets: dict[Hashable, tuple[float, float]] = {}

    def allow(self, key: Hashable) -> bool:
        """Пропустить (`True`) или отклонить (`False`) запрос по ключу; при исключении состояние не меняется."""
        hash(key)  # нехешируемый ключ — TypeError до вызова источника времени
        now = _finite_seconds(self._clock(), "clock value")
        state = self._buckets.get(key)
        if state is None:
            tokens = self._limit
        else:
            tokens, last = state
            # Часы пошли назад (UNK-RL-001): прошедшее время — ноль, отметка сдвигается на now.
            elapsed = max(0.0, now - last)
            tokens = min(self._limit, tokens + elapsed * self._limit / self._window)
        allowed = tokens >= 1
        if allowed:
            tokens -= 1
        self._buckets[key] = (tokens, now)
        return allowed
