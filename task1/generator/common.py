"""Shared constants and helpers for the task1 generator."""
import datetime as dt
import hashlib
import os
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLDEN = os.path.join(TASK, 'golden')
CACHE = os.path.join(HERE, 'cache')
BERLIN = ZoneInfo('Europe/Berlin')
UTC = dt.timezone.utc

SEED = 602
CUT_DATE = dt.date(2026, 10, 31)
PULL_DATE = dt.date(2026, 11, 3)
PULL_TS = dt.datetime(2026, 11, 3, 7, 40, 0)   # in-fiction export time, used for every file mtime and doc property
CAMPAIGN = 'AUT26'
CAMP_FIRST = dt.date(2026, 9, 1)
CAMP_LAST = dt.date(2026, 10, 31)
PRICE_CHANGE = dt.date(2025, 4, 1)
AMOUNT_MINOR_FROM = dt.datetime(2025, 5, 1, tzinfo=UTC)     # billing export moved to minor units

# list prices per month: (old code, new code) -> currency -> (before 2025-04-01, from 2025-04-01)
PLANS = {
    0: dict(old='W4', new='WEEKLY_2025', lessons=4, name='Weekly',
            price={'EUR': (89.00, 95.00), 'GBP': (79.00, 85.00), 'CHF': (95.00, 99.00)}),
    1: dict(old='W8', new='TWICE_2025', lessons=8, name='Twice weekly',
            price={'EUR': (159.00, 169.00), 'GBP': (139.00, 149.00), 'CHF': (169.00, 179.00)}),
}
LANG_NAME = {'EN': 'English', 'ES': 'Spanish', 'DE': 'German', 'FR': 'French', 'IT': 'Italian'}


def month_of(t):
    """Calendar (year, month) for month index t (0 = January 2022)."""
    return 2022 + t // 12, t % 12 + 1


def month_index(y, m):
    return (y - 2022) * 12 + (m - 1)


def month_str(t):
    y, m = month_of(t)
    return '%04d-%02d' % (y, m)


def days_in(y, m):
    nxt = dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def stable_hex(*parts, n=24):
    h = hashlib.sha256('|'.join(str(p) for p in parts).encode()).hexdigest()
    return h[:n]


def to_berlin_date(ts_utc):
    return ts_utc.astimezone(BERLIN).date()


def rate_on(rates, d, cur):
    """ECB reference rate (units of cur per EUR) for date d, or the last published before it."""
    if cur == 'EUR':
        return 1.0
    i = 0 if cur == 'GBP' else 1
    for back in range(0, 10):
        k = (d - dt.timedelta(days=back)).isoformat()
        if k in rates:
            return rates[k][i]
    raise KeyError(d)
