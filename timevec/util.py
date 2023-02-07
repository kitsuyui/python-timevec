import calendar
import datetime
from dataclasses import dataclass


@dataclass
class DateTimeRange:
    begin: datetime.datetime
    end: datetime.datetime

    @property
    def total_time(self) -> datetime.timedelta:
        return self.end - self.begin

    @property
    def half_time(self) -> datetime.timedelta:
        return self.total_time / 2

    @property
    def quarter_time(self) -> datetime.timedelta:
        return self.total_time / 4

    def elapsed_time(self, current: datetime.datetime) -> datetime.timedelta:
        return current - self.begin

    def time_elapsed_ratio(self, current: datetime.datetime) -> float:
        return (
            self.elapsed_time(current).total_seconds()
            / self.total_time.total_seconds()
        )

    @property
    def end_of_1st_quarter(self) -> datetime.datetime:
        return self.begin + 1 * self.quarter_time

    @property
    def end_of_2nd_quarter(self) -> datetime.datetime:
        return self.begin + 2 * self.quarter_time

    @property
    def end_of_3rd_quarter(self) -> datetime.datetime:
        return self.begin + 3 * self.quarter_time


def long_time_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin = datetime.datetime.min.replace(
        year=1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end = datetime.datetime.min.replace(
        year=5001,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin, end)


def millenium_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_millenium = datetime.datetime.min.replace(
        year=(dt.year - 1) // 1000 * 1000 + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_millenium = datetime.datetime.min.replace(
        year=(dt.year - 1) // 1000 * 1000 + 1001,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_millenium, end_of_millenium)


def century_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_century = datetime.datetime.min.replace(
        year=(dt.year - 1) // 100 * 100 + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_century = datetime.datetime.min.replace(
        year=(dt.year - 1) // 100 * 100 + 101,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_century, end_of_century)


def year_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_year = datetime.datetime.min.replace(
        year=dt.year,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_year = datetime.datetime.min.replace(
        year=dt.year + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_year, end_of_year)


def month_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    _, last_day = calendar.monthrange(dt.year, dt.month)
    end_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=last_day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    return DateTimeRange(begin_of_month, end_of_month)


def week_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) - datetime.timedelta(days=dt.weekday())
    end_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=7 - dt.weekday())
    return DateTimeRange(begin_of_week, end_of_week)


def day_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    begin_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    return DateTimeRange(begin_of_day, end_of_day)
