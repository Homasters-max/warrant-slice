"""Тесты spec `rate-limiter`: каждый тест несёт токен своего сценария SCN-RL-…"""

import math

import pytest

from rate_limiter import RateLimiter


class FakeClock:
    """Источник времени, управляемый тестом: возвращает `value` (или бросает `error`) и считает вызовы."""

    def __init__(self, value=0):
        self.value = value
        self.error = None
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.value


def test_scn_rl_001_limit_exhausted():
    """SCN-RL-001: без хода времени пропускаются первые N запросов, (N+1)-й отклонён."""
    limiter = RateLimiter(3, 10, clock=FakeClock(0))

    assert [limiter.allow("a") for _ in range(4)] == [True, True, True, False]


def test_scn_rl_002_refill():
    """SCN-RL-002: запас пополняется со скоростью N/W и не превышает N."""
    clock = FakeClock(0)
    limiter = RateLimiter(2, 8, clock=clock)

    assert [limiter.allow("a") for _ in range(3)] == [True, True, False]
    clock.value = 3
    assert limiter.allow("a") is False  # запас 0.75
    clock.value = 4
    assert [limiter.allow("a") for _ in range(2)] == [True, False]  # запас ровно 1
    clock.value = 64
    assert [limiter.allow("a") for _ in range(3)] == [True, True, False]  # запас не выше N


def test_scn_rl_003_independent_keys():
    """SCN-RL-003: исчерпание квоты ключа `a` не влияет на ключ `b`."""
    limiter = RateLimiter(2, 10, clock=FakeClock(0))

    assert [limiter.allow("a") for _ in range(3)] == [True, True, False]
    assert [limiter.allow("b") for _ in range(3)] == [True, True, False]
    assert limiter.allow("a") is False


@pytest.mark.parametrize("limit", [0, -1, 2**53 + 1, 3.0, True])
def test_scn_rl_004_invalid_limit(limit):
    """SCN-RL-004: недопустимая квота N — ValueError при создании."""
    with pytest.raises(ValueError):
        RateLimiter(limit, 10, clock=FakeClock(0))


@pytest.mark.parametrize("window", [0, -1, math.nan, math.inf, 10**400, True, "10"])
def test_scn_rl_004_invalid_window(window):
    """SCN-RL-004: недопустимое окно W — ValueError при создании."""
    with pytest.raises(ValueError):
        RateLimiter(2, window, clock=FakeClock(0))


def test_scn_rl_004_non_callable_clock():
    """SCN-RL-004: невызываемый источник времени — TypeError при создании."""
    with pytest.raises(TypeError):
        RateLimiter(2, 10, clock=5)


def test_scn_rl_004_boundary_values_accepted():
    """SCN-RL-004: граничные допустимые значения N = 1, N = 2^53, дробное W и clock=None принимаются."""
    RateLimiter(1, 0.5, clock=FakeClock(0))
    RateLimiter(2**53, 10, clock=FakeClock(0))
    assert RateLimiter(2, 10, clock=None).allow("a") is True  # монотонные часы процесса


def test_scn_rl_005_clock_goes_back():
    """SCN-RL-005: часы назад — прошедшее время ноль, отметка сдвигается на новое значение (UNK-RL-001)."""
    clock = FakeClock(10)
    limiter = RateLimiter(2, 10, clock=clock)

    assert [limiter.allow("a") for _ in range(3)] == [True, True, False]
    clock.value = 5
    assert limiter.allow("a") is False
    clock.value = 10
    assert [limiter.allow("a") for _ in range(2)] == [True, False]  # запас 1 от отметки 5 с


def test_scn_rl_006_request_failures():
    """SCN-RL-006: отказы при запросе не меняют состояние; источник вызывается ровно раз на запрос."""
    clock = FakeClock(0)
    limiter = RateLimiter(2, 10, clock=clock)
    assert clock.calls == 0  # при создании источник не вызывается

    with pytest.raises(TypeError):
        limiter.allow([1])
    assert clock.calls == 0  # ключ проверяется до вызова источника

    assert limiter.allow("a") is True

    clock.value = math.nan
    with pytest.raises(ValueError):
        limiter.allow("a")
    clock.value = 0
    clock.error = RuntimeError("clock failed")
    with pytest.raises(RuntimeError, match="clock failed"):
        limiter.allow("a")
    clock.error = None
    clock.value = 10**400
    with pytest.raises(ValueError):
        limiter.allow("a")

    clock.value = 5
    assert [limiter.allow("a") for _ in range(3)] == [True, True, False]  # запас 1 + 1, отметка 0 не сдвинута
    assert [limiter.allow(k) for k in (1, 1.0, True)] == [True, True, False]  # один ключ
    assert clock.calls == 10  # все запросы, кроме запроса с ключом [1]
