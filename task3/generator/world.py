"""task3 architecture 3: the clean truth of the Corrin Valley world, before any file is written.

Every series the pack will carry is built here from the aquifer, the pumping records and the region's natural
level: the Mill Street wells' monthly pumping 2009 to 2026, the natural level each well would have shown without
any pumping, the drawdown the Mill Street wells caused at every well, the monitoring readings, and the minute record
of the September 2026 Reidel Road test. Nothing here knows how a file will be laid out."""
import datetime as dt
import math

import numpy as np

import aquifer as A
import params as P

UTC = dt.timezone.utc
EDT = dt.timezone(dt.timedelta(hours=-4))


def months(y0=2005, m0=1, y1=2046, m1=12):
    out = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


MONTHS = months()
MI = {ym: i for i, ym in enumerate(MONTHS)}
N = len(MONTHS)
DATA_END = (2026, 9)          # the last month every long-term file carries


def xy(ac):
    a, c = ac
    x0, y0 = P.ORIGIN
    # along-axis unit vector points N 18 E; across-axis points E 18 S
    ua = (math.sin(P.AZ), math.cos(P.AZ))
    uc = (math.cos(P.AZ), -math.sin(P.AZ))
    return (x0 + a * ua[0] + c * uc[0], y0 + a * ua[1] + c * uc[1])


def town_pumping(rng):
    """Monthly mean gpm for TW-1 and TW-2, March 2009 to September 2026."""
    q1 = np.zeros(N)
    q2 = np.zeros(N)
    for i, (y, m) in enumerate(MONTHS):
        if (y, m) < P.TOWN_START or (y, m) > DATA_END:
            continue
        yrs = (y - 2009) + (m - 1) / 12.0
        tot = P.TOWN_BASE_GPM * (1 + P.TOWN_GROWTH) ** yrs
        tot *= 1 + P.TOWN_SEASON * math.cos(2 * math.pi * (m - 7) / 12.0)
        tot *= math.exp(rng.normal(0, 0.035))
        if (y, m) < P.TW2_START:
            q1[i] = tot
        else:
            share = P.TW1_SHARE_AFTER + rng.normal(0, 0.03)
            if (y, m) == (2018, 3):          # TW-1 pulled for a pump and motor replacement
                share = 0.0
            if (y, m) in ((2021, 10), (2021, 11)):   # TW-2 screen redevelopment
                share = 1.0
            q1[i] = tot * share
            q2[i] = tot * (1 - share)
    return q1, q2


def town_projection():
    """The application's projection for the Mill Street wells, October 2026 to December 2046, monthly gpm."""
    base = P.TOWN_PROJ_BASE
    out = np.zeros(N)
    for i, (y, m) in enumerate(MONTHS):
        if (y, m) <= DATA_END:
            continue
        ann = base * (1 + P.TOWN_PROJ_GROWTH) ** (y - 2026)
        out[i] = ann * P.TOWN_MONTH_FACTORS[m - 1]
    return out


def new_field(rate):
    out = np.zeros(N)
    for i, (y, m) in enumerate(MONTHS):
        if (y, m) >= P.NEW_START:
            out[i] = rate * P.NEW_SEASON[m - 1]
    return out


def natural_levels(rng):
    """Natural level anomaly (ft, + higher) for each well, monthly 2005 to 2026: the confined aquifer's regional
    response to wet and dry years, the shallow outwash's quicker and larger one, the bedrock's muted one."""
    yr = np.array([y for y, _ in MONTHS])
    mo = np.array([m for _, m in MONTHS])
    ar = np.zeros(N)
    for i in range(1, N):
        ar[i] = 0.92 * ar[i - 1] + rng.normal(0, 0.24)
    yan = np.array([P.WET_DRY.get(int(y), 0.0) for y in yr])
    # the annual anomalies ease in and out over the months rather than stepping at each new year
    k = np.array([0.08, 0.16, 0.24, 0.24, 0.16, 0.08])
    yan_s = np.convolve(np.pad(yan, (3, 2), mode="edge"), k, mode="valid")[:N]
    regional = 1.05 * np.sin(2 * math.pi * (mo - 2.2) / 12.0) + yan_s + ar
    shallow_ar = np.zeros(N)
    for i in range(1, N):
        shallow_ar[i] = 0.75 * shallow_ar[i - 1] + rng.normal(0, 0.45)
    shallow = 2.6 * np.sin(2 * math.pi * (mo - 2.8) / 12.0) + 1.5 * yan_s + shallow_ar
    out = {}
    for w in P.WELLS:
        gain = P.NAT_GAIN.get(w, 1.0)
        local = np.zeros(N)
        for i in range(1, N):
            local[i] = 0.85 * local[i - 1] + rng.normal(0, 0.05)
        if w in P.CONFINED:
            out[w] = gain * regional + local
        elif w == "CV-13":
            out[w] = 0.35 * regional + 0.6 * local
        else:
            out[w] = gain * shallow + 2 * local
    return out, regional


def town_drawdown(q1, q2, obs, T=P.T, S=P.S, B=P.B, width=P.WIDTH):
    """Monthly mean drawdown the Mill Street wells cause at obs (truth unless parameters are passed)."""
    o = P.WELLS[obs] if isinstance(obs, str) else obs
    s = A.superpose_monthly(q1, A.monthly_kernel(T, S, B, P.WELLS["TW-1"], o, width, N))
    s += A.superpose_monthly(q2, A.monthly_kernel(T, S, B, P.WELLS["TW-2"], o, width, N))
    return s


def field_drawdown(qn, obs, T=P.T, S=P.S, B=P.B, width=P.WIDTH):
    o = P.WELLS[obs] if isinstance(obs, str) else obs
    s = A.superpose_monthly(qn / 2.0, A.monthly_kernel(T, S, B, P.WELLS["PW-1"], o, width, N))
    s += A.superpose_monthly(qn / 2.0, A.monthly_kernel(T, S, B, P.WELLS["PW-2"], o, width, N))
    return s


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    q1, q2 = town_pumping(rng)
    nat, regional = natural_levels(rng)
    draw = {w: town_drawdown(q1, q2, w) for w in P.WELLS if w in P.CONFINED or w in ("CV-04", "CV-09", "CV-13")}
    # the shallow outwash and the bedrock barely feel the confined aquifer's pumping
    for w in ("CV-04", "CV-09"):
        draw[w] = 0.06 * draw[w]
    draw["CV-13"] = 0.10 * draw["CV-13"]
    return {"q1": q1, "q2": q2, "nat": nat, "regional": regional, "draw": draw, "rng": rng}


# ---------------------------------------------------------------- the September 2026 test, minute by minute

def test_clock():
    t0 = dt.datetime.fromisoformat(P.LOG_FROM).replace(tzinfo=EDT)
    t1 = dt.datetime.fromisoformat(P.LOG_TO).replace(tzinfo=EDT)
    on = dt.datetime.fromisoformat(P.TEST_START).replace(tzinfo=EDT)
    n = int((t1 - t0).total_seconds() // 60) + 1
    stamps = [t0 + dt.timedelta(minutes=k) for k in range(n)]
    tdays = np.array([(s - on).total_seconds() / 86400.0 for s in stamps])
    return stamps, tdays, on


def barometer(tdays, rng):
    """Atmospheric pressure (psi) at the site: a slow wave, the daily tide and a front on 16 to 17 September."""
    p = 14.38 + 0.035 * np.sin(2 * math.pi * tdays / 4.3 + 0.7)
    p += 0.012 * np.sin(2 * math.pi * tdays * 2 + 1.1)                 # semidiurnal atmospheric tide
    front = 2.35
    p -= 0.165 * (1 / (1 + np.exp(-(tdays - front) / 0.18)))
    p += 0.120 * (1 / (1 + np.exp(-(tdays - (front + 1.35)) / 0.30)))
    walk = np.cumsum(rng.normal(0, 0.0009, len(tdays)))
    walk -= np.linspace(walk[0], walk[-1], len(tdays))
    return p + walk


def test_rate_steps():
    """PW-1's rate as hourly steps (gpm): it starts at the high end and eases down as the column warms."""
    hi, lo = P.TEST_RATE_GPM
    steps = []
    for h in range(P.TEST_HOURS):
        frac = (1 - math.exp(-h / 9.0)) / (1 - math.exp(-P.TEST_HOURS / 9.0))
        steps.append((h / 24.0, round(hi - (hi - lo) * frac, 1)))
    steps.append((P.TEST_HOURS / 24.0, 0.0))
    return steps


def test_drawdown(tdays, obs, steps, T=P.T, S=P.S, B=P.B, width=P.WIDTH):
    """Drawdown at obs over the test record by interpolating the unit step response on a log time grid."""
    o = P.WELLS[obs]
    rw = P.WELLS["PW-1"]
    grid = np.logspace(-6, 1.6, 900)
    if obs == "PW-1":
        o = (rw[0], rw[1] + 0.5)
    ur = A.step_response(T, S, B, rw, o, grid, width)
    lg = np.log(grid)
    out = np.zeros_like(tdays)
    prev = 0.0
    for tc, rate in steps:
        dq = (rate - prev) * P.GPM
        prev = rate
        dtv = tdays - tc
        m = dtv > 0
        out[m] += dq * np.interp(np.log(dtv[m]), lg, ur)
    return out


def earth_tide(tdays, amp):
    return amp * (np.sin(2 * math.pi * tdays * 1.9323 + 0.4) + 0.46 * np.sin(2 * math.pi * tdays * 2.0 + 1.9) +
                  0.38 * np.sin(2 * math.pi * tdays * 0.9973 + 2.6))
