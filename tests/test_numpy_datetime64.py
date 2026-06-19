import datetime
import os
import time
from collections.abc import Iterator

import numpy as np
import pytest

import timevec.numpy as tv
import timevec.numpy_datetime64 as tv64
from timevec.numpy_datetime64 import datetime64_to_datetime

FIXED_DATETIME = datetime.datetime(2024, 1, 2, 3, 4, 5, 123456)


@pytest.fixture
def timezone() -> Iterator[None]:
    old_tz = os.environ.get("TZ")
    try:
        yield
    finally:
        if old_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old_tz
        time.tzset()


def test_datetime_to_datetime64_preserves_microseconds() -> None:
    dt = datetime.datetime(
        2024,
        1,
        1,
        12,
        0,
        0,
        500000,
        tzinfo=datetime.timezone.utc,
    )
    dt64 = tv64.datetime_to_datetime64(dt)
    dt_back = tv64.datetime64_to_datetime(dt64)
    assert dt_back.microsecond == dt.microsecond


def test_long_time_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.long_time_vec(dt64), tv.long_time_vec(dt))


def test_millennium_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.millennium_vec(dt64), tv.millennium_vec(dt))


def test_century_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.century_vec(dt64), tv.century_vec(dt))


def test_year_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.year_vec(dt64), tv.year_vec(dt))


def test_month_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.month_vec(dt64), tv.month_vec(dt))


def test_week_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.week_vec(dt64), tv.week_vec(dt))


def test_day_vec() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.day_vec(dt64), tv.day_vec(dt))


def test_datetime64_to_datetime_in_range() -> None:
    # values within Python datetime range should succeed
    assert datetime64_to_datetime(np.datetime64("2000-01-01T00:00:00")) == datetime.datetime(
        2000, 1, 1, 0, 0, 0,
    )
    assert datetime64_to_datetime(np.datetime64("0001-01-01T00:00:00")) == datetime.datetime(
        1, 1, 1, 0, 0, 0,
    )


def test_datetime64_to_datetime_out_of_range() -> None:
    # values outside Python datetime range raise ValueError with a clear message
    with pytest.raises(ValueError, match="outside the Python datetime range"):
        datetime64_to_datetime(np.datetime64("10000-01-01"))
    with pytest.raises(ValueError, match="outside the Python datetime range"):
        datetime64_to_datetime(np.datetime64("0000-12-31"))


def test_multiple_datetime64() -> None:
    dt = FIXED_DATETIME
    dt64 = np.datetime64(dt)
    vec = np.array([dt64, dt64, dt64], dtype=np.datetime64)
    assert vec.shape == (3,)
    vec2 = np.frompyfunc(tv64.day_vec, 1, 1)(vec)
    assert np.stack(vec2, axis=0).shape == (3, 2)
    vec3 = np.array(
        [[dt64, dt64, dt64], [dt64, dt64, dt64]],
        dtype=np.datetime64,
    )
    assert vec3.shape == (2, 3)


@pytest.mark.skipif(
    not hasattr(time, "tzset"),
    reason="timezone switching requires time.tzset()",
)
@pytest.mark.usefixtures("timezone")
def test_datetime_to_datetime64_is_timezone_independent() -> None:
    dt = datetime.datetime(2024, 1, 1, 12, 0, 0)

    os.environ["TZ"] = "UTC"
    time.tzset()
    utc_result = tv64.datetime_to_datetime64(dt)

    os.environ["TZ"] = "Asia/Tokyo"
    time.tzset()
    tokyo_result = tv64.datetime_to_datetime64(dt)

    assert utc_result == tokyo_result == np.datetime64("2024-01-01T12:00:00")
