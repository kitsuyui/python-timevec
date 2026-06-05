import datetime
import math
from collections.abc import Callable, Iterable

import timevec.util as util

BuiltinVecFactory = Callable[[datetime.datetime], tuple[float, float]]
RangeFactory = Callable[[datetime.datetime], util.DateTimeRange]


def long_time_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the long time as a vector"""
    range = util.long_time_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def millennium_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the millennium as a vector"""
    range = util.millennium_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def century_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the century as a vector"""
    range = util.century_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def decade_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the decade as a vector"""
    range = util.decade_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def year_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    range = util.year_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def month_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    range = util.month_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def week_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    range = util.week_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def day_vec(dt: datetime.datetime) -> tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    range = util.day_range(dt)
    ratio = range.time_elapsed_ratio(dt)
    return ratio_to_vec(ratio)


def ratio_to_vec(ratio: float) -> tuple[float, float]:
    """Convert a ratio to a vector.

    Raises ``ValueError`` for NaN or infinite inputs.
    """
    if not math.isfinite(ratio):
        raise ValueError(f"ratio must be a finite float, got {ratio!r}")
    s = 2 * math.pi * ratio
    x = math.cos(s)
    y = math.sin(s)
    return x, y


def vec_to_ratio(x: float, y: float) -> float:
    """Convert a vector to a ratio"""
    if x == 0.0 and y == 0.0:
        raise ValueError(
            "vec_to_ratio received a zero vector (0, 0);"
            " input must be a unit vector",
        )
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    angle = math.atan2(y, x) / (2.0 * math.pi)
    return angle if angle >= 0 else angle + 1.0


BUILTIN_VEC_FACTORIES: tuple[tuple[util.TARGET, BuiltinVecFactory], ...] = (
    ("long_time", long_time_vec),
    ("millennium", millennium_vec),
    ("century", century_vec),
    ("decade", decade_vec),
    ("year", year_vec),
    ("month", month_vec),
    ("week", week_vec),
    ("day", day_vec),
)

RANGE_FACTORIES: tuple[tuple[util.TARGET, RangeFactory], ...] = (
    ("long_time", util.long_time_range),
    ("millennium", util.millennium_range),
    ("century", util.century_range),
    ("decade", util.decade_range),
    ("year", util.year_range),
    ("month", util.month_range),
    ("week", util.week_range),
    ("day", util.day_range),
)


def present_ranges(
    items: dict[util.TARGET, tuple[float, float]],
) -> Iterable[tuple[RangeFactory, tuple[float, float]]]:
    for target, range_factory in RANGE_FACTORIES:
        value = items.get(target)
        if value is not None:
            yield range_factory, value


def datetime_to_vecs(
    dt: datetime.datetime,
    targets: Iterable[util.TARGET],
) -> dict[util.TARGET, tuple[float, float]]:
    """Convert a datetime to a vector"""
    target_set = set(targets)
    return {
        target: factory(dt)
        for target, factory in BUILTIN_VEC_FACTORIES
        if target in target_set
    }


def datetime_from_vecs(
    items: dict[util.TARGET, tuple[float, float]],
) -> datetime.datetime:
    """Convert a vector to a datetime.

    Raises:
        ValueError: If no recognized time targets are present in *items*.
    """
    ranges = list(present_ranges(items))
    if not ranges:
        valid = [target for target, _ in RANGE_FACTORIES]
        raise ValueError(
            f"No recognized time targets in items. "
            f"Expected one or more of {valid}; got {list(items.keys())}.",
        )
    t = util.BEGIN_OF_DATETIME
    for range_factory, value in ranges:
        range = range_factory(t)
        t = range.current_time_by_ratio(vec_to_ratio(*value))
    return t


__all__ = [
    "century_vec",
    "datetime_from_vecs",
    "datetime_to_vecs",
    "day_vec",
    "decade_vec",
    "long_time_vec",
    "millennium_vec",
    "month_vec",
    "week_vec",
    "year_vec",
]
