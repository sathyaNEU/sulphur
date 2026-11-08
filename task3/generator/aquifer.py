"""Well hydraulics on numpy alone: the Hantush leaky well function (Theis when the leakage factor is infinite),
image wells for two parallel no-flow walls, the unit step response at an observation point, and superposition of a
monthly or minute pumping record. Shared by the world (truth), the golden solution and the rivals."""
import math
from functools import lru_cache

import numpy as np

_G = np.linspace(0.0, 1.0, 260)


def well_function(u, rho=0.0):
    """W(u, rho) = integral from u to infinity of exp(-y - rho^2/(4y))/y dy, on a log grid; rho = r/B."""
    u = np.asarray(u, dtype=float)
    rho = np.broadcast_to(np.asarray(rho, dtype=float), u.shape)
    lu = np.log(np.maximum(u, 1e-300))[..., None]
    span = np.maximum(np.log(80.0) - lu, 2.0)
    ly = lu + span * _G
    y = np.exp(ly)
    f = np.exp(-y - (rho[..., None] ** 2) / (4.0 * y))
    return np.trapezoid(f, ly, axis=-1)


def images(c0, width, k=4):
    """Cross-valley positions of a well at c0 and its images in no-flow walls at -width/2 and +width/2."""
    if width is None:
        return [c0]
    s = c0 + width / 2.0
    out = []
    for n in range(-k, k + 1):
        for p in (2 * n * width + s, 2 * n * width - s):
            out.append(p - width / 2.0)
    return out


def step_response(T, S, B, well_ac, obs_ac, times, width=None):
    """Drawdown (ft) per unit rate (ft3/day) at obs for pumping that starts at time 0; times in days."""
    times = np.asarray(times, dtype=float)
    a0, c0 = well_ac
    tot = np.zeros_like(times)
    for ci in images(c0, width):
        r = max(math.hypot(obs_ac[0] - a0, obs_ac[1] - ci), 0.5)
        if B is not None and r / B > 14.0:
            continue
        u = r * r * S / (4.0 * T * np.maximum(times, 1e-9))
        tot += well_function(u, 0.0 if B is None else r / B) / (4.0 * math.pi * T)
    return np.where(times > 0, tot, 0.0)


@lru_cache(maxsize=None)
def monthly_kernel(T, S, B, well_ac, obs_ac, width, n):
    """Mean drawdown over month k (k = 0 is the month the step starts) per unit rate, from mid-month samples."""
    t = (np.arange(n) + 0.5) * 30.4375
    return step_response(T, S, B, well_ac, obs_ac, t, width)


def superpose_monthly(q_gpm, kernel, gpm_ft3=192.5):
    """Monthly mean drawdown for a monthly mean rate series (gpm) through a monthly step kernel."""
    q = np.asarray(q_gpm, dtype=float) * gpm_ft3
    dq = np.diff(np.concatenate([[0.0], q]))
    return np.convolve(dq, kernel[:len(q)])[:len(q)]


def superpose_steps(t_days, steps, T, S, B, well_ac, obs_ac, width=None, gpm_ft3=192.5):
    """Drawdown at times t (days) for rate changes [(t_change, new_rate_gpm), ...] starting from zero."""
    t_days = np.asarray(t_days, dtype=float)
    out = np.zeros_like(t_days)
    prev = 0.0
    for tc, rate in steps:
        dq = (rate - prev) * gpm_ft3
        prev = rate
        if dq == 0:
            continue
        out += dq * step_response(T, S, B, well_ac, obs_ac, t_days - tc, width)
    return out
