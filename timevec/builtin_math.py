import calendar
import datetime
import math
from typing import Tuple

from timevec.util import (
    century_range,
    day_range,
    long_time_range,
    millenium_range,
    month_range,
    week_range,
    year_range,
)


def long_time_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the long time as a vector"""
    range = long_time_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def millenium_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the millenium as a vector"""
    range = millenium_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def century_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the century as a vector"""
    range = century_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def year_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    range = year_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def month_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    range = month_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def week_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    range = week_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def day_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    range = day_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def ratio_to_vec(rate: float) -> Tuple[float, float]:
    s = 2 * math.pi * rate
    x = math.cos(s)
    y = math.sin(s)
    return x, y


def vec_to_ratio(x: float, y: float) -> float:
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    angle = math.atan2(y, x) / (2.0 * math.pi)
    return angle if angle >= 0 else angle + 1.0


def datetime_from_vec(
    year: int,
    yv: Tuple[float, float],
    dv: Tuple[float, float],
) -> datetime.datetime:
    position_in_year = vec_to_ratio(*yv)
    position_in_day = vec_to_ratio(*dv)
    d = int(position_in_year * (366.0 if calendar.isleap(year) else 365.0))
    s = position_in_day * 86400.0
    return datetime.datetime(year, 1, 1, 0, 0, 0, 0) + datetime.timedelta(
        days=int(d), seconds=s
    )
