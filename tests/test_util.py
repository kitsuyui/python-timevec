import datetime

import pytest

from timevec.util import (
    DateTimeRange,
    century_range,
    day_range,
    decade_range,
    long_time_range,
    millennium_range,
    month_range,
    week_range,
    year_range,
)


def assert_date_time_range(
    range: DateTimeRange,
    *,
    rounding_tolerance: datetime.timedelta = datetime.timedelta(),
) -> None:
    """Assert that a DateTimeRange is valid"""
    assert range.begin <= range.end
    half_delta = abs(range.total_time - 2 * range.half_time)
    quarter_delta = abs(range.total_time - 4 * range.quarter_time)
    assert half_delta <= rounding_tolerance
    assert quarter_delta <= rounding_tolerance
    assert (
        range.begin
        < range.end_of_first_quarter
        < range.end_of_second_quarter
        < range.end_of_third_quarter
        < range.end
    )


def test_date_time_range() -> None:
    """Test DateTimeRange"""
    range = DateTimeRange(
        datetime.datetime(2000, 1, 1),
        datetime.datetime(2000, 1, 2),
    )
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 1, 2)
    assert range.total_time == datetime.timedelta(days=1)


def test_date_time_range_inverted_raises() -> None:
    """DateTimeRange with begin > end must raise ValueError."""
    with pytest.raises(ValueError):
        DateTimeRange(
            datetime.datetime(2000, 1, 2), datetime.datetime(2000, 1, 1),
        )


def test_time_elapsed_ratio_rejects_zero_duration_range() -> None:
    """Test zero-duration DateTimeRange elapsed ratio contract."""
    instant = datetime.datetime(2000, 1, 1)
    range = DateTimeRange(instant, instant)

    with pytest.raises(ValueError, match="non-zero duration"):
        range.time_elapsed_ratio(instant)


def test_long_time_range() -> None:
    """Test long_time_range()"""
    range = long_time_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(
        range,
        rounding_tolerance=datetime.timedelta(microseconds=1),
    )
    assert range.begin == datetime.datetime.min
    assert range.end == datetime.datetime.max
    assert range.total_time == datetime.datetime.max - datetime.datetime.min


def test_long_time_range_keeps_supported_datetimes_in_range() -> None:
    """Test long_time_range() covers latest representable datetimes."""
    range = long_time_range(datetime.datetime.max)

    assert range.time_elapsed_ratio(datetime.datetime(5001, 1, 1)) < 1.0
    assert range.time_elapsed_ratio(datetime.datetime(9999, 1, 1)) < 1.0
    assert range.time_elapsed_ratio(datetime.datetime.max) == 1.0


def test_millennium_range() -> None:
    """Test millennium_range()"""
    range = millennium_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1001, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=365243)


def test_century_range() -> None:
    """Test century_range()"""
    range = century_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1901, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=36525)


def test_decade_range_near_datetime_min() -> None:
    """Test decade_range() for years where 0-based decade math underflows."""
    range = decade_range(datetime.datetime(1, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1, 1, 1)
    assert range.end == datetime.datetime(11, 1, 1)


def test_year_range() -> None:
    """Test year_range()"""
    range = year_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=366)


def test_month_range() -> None:
    """Test month_range()"""
    range = month_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 2, 1)
    assert range.total_time == datetime.timedelta(days=31)


def test_week_range() -> None:
    """Test week_range()"""
    range = week_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1999, 12, 27)
    assert range.end == datetime.datetime(2000, 1, 3)
    assert range.total_time == datetime.timedelta(days=7)


def test_day_range() -> None:
    """Test day_range()"""
    range = day_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 1, 2)
    assert range.total_time == datetime.timedelta(days=1)


def test_year_range_near_datetime_max() -> None:
    """year_range must not raise ValueError for datetime.max year."""
    range = year_range(datetime.datetime(9999, 1, 1))
    assert range.begin == datetime.datetime(9999, 1, 1)
    assert range.end == datetime.datetime.max
    assert range.begin < range.end


def test_decade_range_near_datetime_max() -> None:
    """decade_range must not raise ValueError near datetime.max."""
    range = decade_range(datetime.datetime(9999, 1, 1))
    assert range.begin.year == 9991
    assert range.end == datetime.datetime.max
    assert range.begin < range.end


def test_century_range_near_datetime_max() -> None:
    """century_range must not raise ValueError near datetime.max."""
    range = century_range(datetime.datetime(9999, 1, 1))
    assert range.begin.year == 9901
    assert range.end == datetime.datetime.max
    assert range.begin < range.end


def test_millennium_range_near_datetime_max() -> None:
    """millennium_range must not raise ValueError near datetime.max."""
    range = millennium_range(datetime.datetime(9999, 1, 1))
    assert range.begin.year == 9001
    assert range.end == datetime.datetime.max
    assert range.begin < range.end
