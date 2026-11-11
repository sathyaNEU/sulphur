"""Calendar facts the site runs on: Finnish public holidays (the site is closed), Black Friday, ISO weeks, the
working days (Monday to Friday, and Saturday in the peak weeks)."""
import datetime as dt
from functools import lru_cache

import params as P


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


@lru_cache(maxsize=None)
def holidays(y):
    e = easter(y)
    mid_eve = next(dt.date(y, 6, d) for d in range(19, 26) if dt.date(y, 6, d).weekday() == 4)
    saints = next(dt.date(y, 10, 31) + dt.timedelta(days=k) for k in range(7)
                  if (dt.date(y, 10, 31) + dt.timedelta(days=k)).weekday() == 5)
    return {dt.date(y, 1, 1), dt.date(y, 1, 6), e - dt.timedelta(days=2), e + dt.timedelta(days=1),
            dt.date(y, 5, 1), e + dt.timedelta(days=39), mid_eve, mid_eve + dt.timedelta(days=1), saints,
            dt.date(y, 12, 6), dt.date(y, 12, 24), dt.date(y, 12, 25), dt.date(y, 12, 26)}


def black_friday(y):
    d = dt.date(y, 11, 1)
    thu = d + dt.timedelta(days=(3 - d.weekday()) % 7)
    return thu + dt.timedelta(days=22)


def isoweek(d):
    return d.isocalendar()[1]


def isoyear(d):
    return d.isocalendar()[0]


def peak(d):
    return isoweek(d) in P.PEAK_WEEKS


def working(d):
    if d in holidays(d.year):
        return False
    wd = d.weekday()
    if wd < 5:
        return True
    return wd == 5 and peak(d)


def days(a, b):
    n = (b - a).days
    return [a + dt.timedelta(days=i) for i in range(n + 1)]


def next_working(d):
    x = d
    while not working(x):
        x += dt.timedelta(days=1)
    return x
