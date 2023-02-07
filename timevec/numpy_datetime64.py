import datetime

import numpy as np
import numpy.typing as npt

from timevec.numpy import datetime_from_vec, ratio_to_vec
from timevec.util import (
    century_range,
    day_range,
    long_time_range,
    millenium_range,
    month_range,
    week_range,
    year_range,
)


def long_time_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the long time as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = long_time_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def millenium_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the millenium as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = millenium_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def century_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the century as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = century_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def year_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = year_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = month_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = week_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = day_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return ratio_to_vec(rate, dtype=dtype)


def datetime64_to_datetime(dt: np.datetime64) -> datetime.datetime:
    """Convert a numpy.datetime64 to a datetime.datetime"""
    dt64 = np.datetime64(dt)
    ts = float(
        (dt64 - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    )
    return datetime.datetime.utcfromtimestamp(ts)


def datetime64_from_vec(
    year: int,
    yv: npt.NDArray,
    dv: npt.NDArray,
) -> np.datetime64:
    """Convert a vector representation of a datetime to a numpy.datetime64"""
    dt = datetime_from_vec(year, yv, dv)
    return np.datetime64(dt)
