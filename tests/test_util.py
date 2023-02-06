import datetime

from timevec.util import (
    day_range,
    month_range,
    week_range,
    century_range,
    millenium_range,
    year_range,
)


def test_millenium_range() -> None:
    """Test millenium_range()"""
    begin, end = millenium_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(1001, 1, 1)
    assert end == datetime.datetime(2001, 1, 1)
    assert end - begin == datetime.timedelta(days=365243)  # 1000 years contains 243 leap years


def test_century_range() -> None:
    """Test century_range()"""
    begin, end = century_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(1901, 1, 1)
    assert end == datetime.datetime(2001, 1, 1)
    assert end - begin == datetime.timedelta(days=36525)


def test_year_range() -> None:
    """Test year_range()"""
    begin, end = year_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(2000, 1, 1)
    assert end == datetime.datetime(2001, 1, 1)
    assert end - begin == datetime.timedelta(days=366)  # leap year


def test_month_range() -> None:
    """Test month_range()"""
    begin, end = month_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(2000, 1, 1)
    assert end == datetime.datetime(2000, 2, 1)
    assert end - begin == datetime.timedelta(days=31)


def test_week_range() -> None:
    """Test week_range()"""
    begin, end = week_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(1999, 12, 27)
    assert end == datetime.datetime(2000, 1, 3)
    assert end - begin == datetime.timedelta(days=7)


def test_day_range() -> None:
    """Test day_range()"""
    begin, end = day_range(datetime.datetime(2000, 1, 1))
    assert begin == datetime.datetime(2000, 1, 1, 0, 0, 0)
    assert end == datetime.datetime(2000, 1, 2, 0, 0, 0)
    assert end - begin == datetime.timedelta(days=1)
