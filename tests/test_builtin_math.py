import datetime

import pytest
from typing import Tuple, Callable

import timevec.builtin_math as tv


def assert_vector_in_circle(x: float, y: float, *, abs: float = 1e-6) -> None:
    assert pytest.approx(x**2 + y**2, abs=abs) == 1.0


def assert_vector_continuity(
    dt: datetime.datetime,
    fn: Callable[[datetime.datetime], Tuple[float, float]],
    eps_timedelta: datetime.timedelta = datetime.timedelta(seconds=0.01),
) -> None:
    """Test that the vector is continuous and in the same basis"""
    # all vectors must be same length in polar coordinates
    x1, y1 = fn(dt)
    assert_vector_in_circle(x1, y1)

    # Add small tim delta means that very small rotation
    x2, y2 = fn(dt + eps_timedelta)
    assert_vector_in_circle(x2, y2)
    # The angle between vectors must be very small
    cos_similarity1 = abs(x1 * x2 + y1 * y2)  # cos(angle)
    assert cos_similarity1 > 0.9999

    # rotate to reverse direction
    x3, y3 = fn(dt + 2 * eps_timedelta)
    assert_vector_in_circle(x3, y3)
    cos_similarity2 = abs(x2 * x3 + y2 * y3)  # cos(angle)
    assert cos_similarity2 > 0.9999

    assert cos_similarity1 == pytest.approx(cos_similarity2)
    # The vectors must be in the same basis
    assert (x1 + x2 + x3) / 3 == pytest.approx(x2, abs=1e-6)
    assert (y1 + y2 + y3) / 3 == pytest.approx(y2, abs=1e-6)


def test_basis() -> None:
    # Test that all the functions are consistent with each other
    # and that they are all in the same basis
    many_dates = [
        datetime.datetime(100, 1, 1, 0, 0, 0),
        datetime.datetime(2001, 1, 1, 0, 0, 0),
        datetime.datetime(2023, 1, 1, 0, 0, 0),
        datetime.datetime(2023, 2, 1, 0, 0, 0),
        datetime.datetime(5001, 1, 1, 0, 0, 0),
    ]
    for dt in many_dates:
        assert_vector_continuity(dt, tv.long_time_vec)
        assert_vector_continuity(dt, tv.millenium_vec)
        assert_vector_continuity(dt, tv.century_vec)
        assert_vector_continuity(dt, tv.year_vec)
        assert_vector_continuity(dt, tv.month_vec)
        assert_vector_continuity(dt, tv.week_vec)
        assert_vector_continuity(dt, tv.day_vec)


def test_long_time_vec() -> None:
    # 0 degrees at the beginning of the long time
    dt = datetime.datetime(1, 1, 1, 0, 0, 0)
    x, y = tv.long_time_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_millenium_vec() -> None:
    # 0 degrees at the beginning of the millenium
    dt = datetime.datetime(2001, 1, 1, 0, 0, 0)
    x, y = tv.millenium_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_century_vec() -> None:
    # 0 degrees at the beginning of the century
    dt = datetime.datetime(2001, 1, 1, 0, 0, 0)
    x, y = tv.century_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_year_vec() -> None:
    # 0 degrees at the beginning of the year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = tv.year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the year
    dt = datetime.datetime(2023, 7, 2, 12, 0, 0)
    x, y = tv.year_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the end of the year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59)
    x, y = tv.year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_month_vec() -> None:
    # 0 degrees at the beginning of the month
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = tv.month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the month
    dt = datetime.datetime(2023, 1, 16, 12, 0, 0)
    x, y = tv.month_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the end of the month
    dt = datetime.datetime(2023, 1, 31, 23, 59, 59)
    x, y = tv.month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-5)


def test_week_vec() -> None:
    # 0 degrees at the beginning of the week
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 3, 0, 0, 0)  # Tuesday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((0.623489, 0.781831), abs=1e-6)

    dt = datetime.datetime(2023, 1, 4, 0, 0, 0)  # Wednesday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((-0.222521, 0.974928), abs=1e-6)

    dt = datetime.datetime(2023, 1, 5, 0, 0, 0)  # Thursday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((-0.900969, 0.433884), abs=1e-6)

    dt = datetime.datetime(2023, 1, 6, 0, 0, 0)  # Friday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((-0.900969, -0.433884), abs=1e-6)

    dt = datetime.datetime(2023, 1, 7, 0, 0, 0)  # Saturday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((-0.222521, -0.974928), abs=1e-6)

    dt = datetime.datetime(2023, 1, 8, 0, 0, 0)  # Sunday
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((0.623489, -0.781831), abs=1e-6)

    # next monday
    dt = datetime.datetime(2023, 1, 9, 0, 0, 0)
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_day_vec() -> None:
    # 0 degrees at the beginning of the day
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = tv.day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the day
    dt = datetime.datetime(2023, 1, 2, 12, 0, 0)
    x, y = tv.day_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the almost end of the day
    dt = datetime.datetime(2023, 1, 2, 23, 59, 59, 999999)
    x, y = tv.day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_edge_cases() -> None:
    # beginning of year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = tv.year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = tv.month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = tv.week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = tv.day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # end of year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    x, y = tv.year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_datetime_from_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    yv = tv.year_vec(dt)
    dv = tv.day_vec(dt)
    dt2 = tv.datetime_from_vec(2023, yv, dv)
    assert pytest.approx(dt, abs=1e-6) == dt2
