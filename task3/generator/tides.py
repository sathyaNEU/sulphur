"""task3: the astronomical tide. Doodson arguments from the mean lunar and solar longitudes, nodal factors after\nSchureman as tabulated by Pugh; heights at any UT instant from a station's harmonic constants."""
import numpy as np

D2R = np.pi / 180.0
J2000 = np.datetime64("2000-01-01T12:00")

# name: (speed deg/h, doodson (tau, s, h, p, N', p1), extra phase deg, nodal key)
CONST = {
    "M2": (28.9841042, (2, 0, 0, 0, 0, 0), 0.0, "M2"),
    "S2": (30.0000000, (2, 2, -2, 0, 0, 0), 0.0, "1"),
    "N2": (28.4397295, (2, -1, 0, 1, 0, 0), 0.0, "M2"),
    "K2": (30.0821373, (2, 2, 0, 0, 0, 0), 0.0, "K2"),
    "2N2": (27.8953548, (2, -2, 0, 2, 0, 0), 0.0, "M2"),
    "NU2": (28.5125831, (2, -1, 2, -1, 0, 0), 0.0, "M2"),
    "MU2": (27.9682084, (2, -2, 2, 0, 0, 0), 0.0, "M2"),
    "L2": (29.5284789, (2, 1, 0, -1, 0, 0), 180.0, "M2"),
    "T2": (29.9589333, (2, 2, -3, 0, 0, 1), 0.0, "1"),
    "K1": (15.0410686, (1, 1, 0, 0, 0, 0), 90.0, "K1"),
    "O1": (13.9430356, (1, -1, 0, 0, 0, 0), -90.0, "O1"),
    "P1": (14.9589314, (1, 1, -2, 0, 0, 0), -90.0, "1"),
    "Q1": (13.3986609, (1, -2, 0, 1, 0, 0), -90.0, "O1"),
    "M4": (57.9682084, (4, 0, 0, 0, 0, 0), 0.0, "M4"),
    "MS4": (58.9841042, (4, 2, -2, 0, 0, 0), 0.0, "M2"),
    "MN4": (57.4238337, (4, -1, 0, 1, 0, 0), 0.0, "M4"),
    "M6": (86.9523127, (6, 0, 0, 0, 0, 0), 0.0, "M6"),
    "SA": (0.0410686, (0, 0, 1, 0, 0, 0), 0.0, "1"),
    "SSA": (0.0821373, (0, 0, 2, 0, 0, 0), 0.0, "1"),
}


def hours_since_j2000(t):
    return (t - J2000) / np.timedelta64(1, "h")


def astro(t):
    """Mean longitudes (deg) and lunar time for datetime64 UT array t."""
    hrs = hours_since_j2000(t)
    T = hrs / (24.0 * 36525.0)
    s = 218.3164477 + 481267.88123421 * T
    h = 280.46646 + 36000.76983 * T
    p = 83.3532465 + 4069.0137287 * T
    N = 125.04452 - 1934.136261 * T
    p1 = 282.93735 + 1.71946 * T
    # solar hour angle: 180 deg at 00 UT
    ut_hours = ((t - t.astype("datetime64[D]")) / np.timedelta64(1, "h"))
    Tsol = 180.0 + 15.0 * ut_hours
    tau = Tsol + h - s
    return tau, s, h, p, -N, p1, N


def nodal(N):
    """f and u (deg) by nodal key, N in degrees."""
    n = N * D2R
    c1, c2, c3 = np.cos(n), np.cos(2 * n), np.cos(3 * n)
    s1, s2, s3 = np.sin(n), np.sin(2 * n), np.sin(3 * n)
    fM2 = 1.0004 - 0.0373 * c1 + 0.0002 * c2
    uM2 = -2.14 * s1
    fK1 = 1.0060 + 0.1150 * c1 - 0.0088 * c2 + 0.0006 * c3
    uK1 = -8.86 * s1 + 0.68 * s2 - 0.07 * s3
    fO1 = 1.0089 + 0.1871 * c1 - 0.0147 * c2 + 0.0014 * c3
    uO1 = 10.80 * s1 - 1.34 * s2 + 0.19 * s3
    fK2 = 1.0241 + 0.2863 * c1 + 0.0083 * c2 - 0.0015 * c3
    uK2 = -17.74 * s1 + 0.68 * s2 - 0.04 * s3
    one = np.ones_like(n)
    return {"1": (one, 0 * n), "M2": (fM2, uM2), "K1": (fK1, uK1), "O1": (fO1, uO1), "K2": (fK2, uK2),
            "M4": (fM2 ** 2, 2 * uM2), "M6": (fM2 ** 3, 3 * uM2)}


def tide(t, amp, pha, chunk=1000000):
    """Tide height (same units as amp) at datetime64 UT times t, Greenwich phase lags pha (deg)."""
    out = np.zeros(t.shape, dtype=float)
    for a in range(0, len(t), chunk):
        tt = t[a:a + chunk]
        tau, s, h, p, Np, p1, N = astro(tt)
        nf = nodal(N)
        acc = np.zeros(tt.shape, dtype=float)
        for name, A in amp.items():
            sp, d, extra, key = CONST[name]
            V = d[0] * tau + d[1] * s + d[2] * h + d[3] * p + d[4] * Np + d[5] * p1 + extra
            f, u = nf[key]
            acc += f * A * np.cos((V + u - pha[name]) * D2R)
        out[a:a + chunk] = acc
    return out
