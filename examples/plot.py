# ja: 実際に year_vec がどのような値を返すかのグラフを描き、わかりやすくします。

import datetime
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np

import timevec.numpy as tv


def plot_func_vec(func: Callable[[datetime.datetime], np.ndarray], dates: list[datetime.datetime]) -> None:
    vecs = np.array([func(dt) for dt in dates])
    _fig, _ax = plt.subplots()
    plt.plot(vecs)
    plt.savefig(f"examples/{func.__name__}.svg")


def main() -> None:
    plot_func_vec(tv.year_vec, dates=[
        datetime.datetime(2023, 1, 1, 0, 0, 0) + datetime.timedelta(days=day)
        for day in range(365 * 2)
    ])
    plot_func_vec(tv.month_vec, dates=[
        datetime.datetime(2023, 1, 1, 0, 0, 0) + datetime.timedelta(days=day)
        for day in range(31 * 2)
    ])
    plot_func_vec(tv.week_vec, dates=[
        datetime.datetime(2023, 1, 1, 0, 0, 0) + datetime.timedelta(hours=h)
        for h in range(24 * 7 * 2)
    ])
    plot_func_vec(tv.day_vec, dates=[
        datetime.datetime(2023, 1, 1, 0, 0, 0) + datetime.timedelta(hours=h)
        for h in range(24 * 2)
    ])


if __name__ == "__main__":
    main()
