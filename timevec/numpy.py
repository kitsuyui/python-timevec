import datetime
from collections.abc import Callable, Iterable

import numpy as np
import numpy.typing as npt

import timevec.util as util

NumpyVecFactory = Callable[[datetime.datetime], npt.NDArray]
NumpyRangeFactory = Callable[[datetime.datetime], util.DateTimeRange]


def long_time_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the long time as a vector"""
    range = util.long_time_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def millennium_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the millennium as a vector"""
    range = util.millennium_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def century_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the century as a vector"""
    range = util.century_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def decade_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the decade as a vector"""
    range = util.decade_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def year_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    range = util.year_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    range = util.month_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    range = util.week_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: datetime.datetime,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    range = util.day_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def ratio_to_vec(
    ratio: float,
    *,
    dtype: npt.DTypeLike = np.float64,
) -> npt.NDArray:
    """Represent the ratio as a vector"""
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2.0 * np.pi * ratio)
    vec[1] = np.sin(2.0 * np.pi * ratio)
    return vec


def vec_to_ratio(arr: npt.NDArray) -> float:
    """Convert a vector to a ratio"""
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    base = np.arctan2(arr[1], arr[0]) / (2.0 * np.pi)
    return float(base if base >= 0.0 else base + 1.0)


NUMPY_RANGE_FACTORIES: tuple[tuple[util.TARGET, NumpyRangeFactory], ...] = (
    ("long_time", util.long_time_range),
    ("millennium", util.millennium_range),
    ("century", util.century_range),
    ("decade", util.decade_range),
    ("year", util.year_range),
    ("month", util.month_range),
    ("week", util.week_range),
    ("day", util.day_range),
)


def numpy_vec_factories(
    *,
    dtype: npt.DTypeLike,
) -> tuple[
    tuple[util.TARGET, Callable[[datetime.datetime], npt.NDArray]],
    ...,
]:
    return (
        ("long_time", lambda dt: long_time_vec(dt, dtype=dtype)),
        ("millennium", lambda dt: millennium_vec(dt, dtype=dtype)),
        ("century", lambda dt: century_vec(dt, dtype=dtype)),
        ("decade", lambda dt: decade_vec(dt, dtype=dtype)),
        ("year", lambda dt: year_vec(dt, dtype=dtype)),
        ("month", lambda dt: month_vec(dt, dtype=dtype)),
        ("week", lambda dt: week_vec(dt, dtype=dtype)),
        ("day", lambda dt: day_vec(dt, dtype=dtype)),
    )


def present_numpy_ranges(
    items: dict[util.TARGET, npt.NDArray],
) -> Iterable[tuple[NumpyRangeFactory, npt.NDArray]]:
    for target, range_factory in NUMPY_RANGE_FACTORIES:
        value = items.get(target)
        if value is not None:
            yield range_factory, value


def datetime_to_vecs(
    dt: datetime.datetime,
    targets: Iterable[util.TARGET],
    *,
    dtype: npt.DTypeLike = np.float64,
) -> dict[util.TARGET, npt.NDArray]:
    """Convert a datetime to a vector"""
    target_set = set(targets)
    return {
        target: factory(dt)
        for target, factory in numpy_vec_factories(dtype=dtype)
        if target in target_set
    }


def datetime_from_vecs(
    items: dict[util.TARGET, npt.NDArray],
) -> datetime.datetime:
    """Convert a vector to a datetime"""
    t = util.BEGIN_OF_DATETIME
    for range_factory, value in present_numpy_ranges(items):
        range = range_factory(t)
        t = range.current_time_by_ratio(vec_to_ratio(value))
    return t


__all__ = [
    "century_vec",
    "datetime_from_vecs",
    "datetime_to_vecs",
    "day_vec",
    "long_time_vec",
    "millennium_vec",
    "month_vec",
    "week_vec",
    "year_vec",
]
