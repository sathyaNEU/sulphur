"""Natural gas compressibility for task22: the published correlations a gas measurement engineer reaches for, used by
the simulated correctors and by the analysis alike.

    z_dak(p_psia, t_f, sg)       Dranchuk and Abou-Kassem (1975) on Sutton's (1985) pseudo-critical properties
    z_hy(p_psia, t_f, sg)        Hall and Yarborough (1973) on the same pseudo-criticals
    z_papay(p_psia, t_f, sg)     Papay (1968), the explicit short form
    fpv2(p_psia, t_f, sg, z)     the supercompressibility factor squared, Z at base conditions over Z flowing

Base conditions are 14.73 psia and 60 F; every function takes arrays.
"""
import numpy as np

P_BASE = 14.73
T_BASE_F = 60.0


def pseudo_critical(sg):
    sg = np.asarray(sg, dtype=float)
    tpc = 169.2 + 349.5 * sg - 74.0 * sg ** 2
    ppc = 756.8 - 131.07 * sg - 3.6 * sg ** 2
    return tpc, ppc


def z_dak(p_psia, t_f, sg):
    p, t, sg = np.broadcast_arrays(np.asarray(p_psia, float), np.asarray(t_f, float), np.asarray(sg, float))
    tpc, ppc = pseudo_critical(sg)
    tpr = (t + 459.67) / tpc
    ppr = p / ppc
    a = [0.3265, -1.0700, -0.5339, 0.01569, -0.05165, 0.5475, -0.7361, 0.1844, 0.1056, 0.6134, 0.7210]
    c1 = a[0] + a[1] / tpr + a[2] / tpr ** 3 + a[3] / tpr ** 4 + a[4] / tpr ** 5
    c2 = a[5] + a[6] / tpr + a[7] / tpr ** 2
    c3 = a[8] * (a[6] / tpr + a[7] / tpr ** 2)
    z = np.ones_like(tpr)
    for _ in range(40):
        rr = 0.27 * ppr / (z * tpr)
        f = (1 + c1 * rr + c2 * rr ** 2 - c3 * rr ** 5 + a[9] * (1 + a[10] * rr ** 2) * (rr ** 2 / tpr ** 3)
             * np.exp(-a[10] * rr ** 2))
        z_new = f
        if np.max(np.abs(z_new - z)) < 1e-12:
            z = z_new
            break
        z = z_new
    return z


def z_hy(p_psia, t_f, sg):
    p, t, sg = np.broadcast_arrays(np.asarray(p_psia, float), np.asarray(t_f, float), np.asarray(sg, float))
    tpc, ppc = pseudo_critical(sg)
    tr = tpc / (t + 459.67)
    ppr = p / ppc
    a = 0.06125 * tr * np.exp(-1.2 * (1 - tr) ** 2)
    y = np.full_like(tr, 0.001)
    for _ in range(60):
        f = (-a * ppr + (y + y ** 2 + y ** 3 - y ** 4) / (1 - y) ** 3
             - (14.76 * tr - 9.76 * tr ** 2 + 4.58 * tr ** 3) * y ** 2
             + (90.7 * tr - 242.2 * tr ** 2 + 42.4 * tr ** 3) * y ** (2.18 + 2.82 * tr))
        df = ((1 + 4 * y + 4 * y ** 2 - 4 * y ** 3 + y ** 4) / (1 - y) ** 4
              - (29.52 * tr - 19.52 * tr ** 2 + 9.16 * tr ** 3) * y
              + (2.18 + 2.82 * tr) * (90.7 * tr - 242.2 * tr ** 2 + 42.4 * tr ** 3) * y ** (1.18 + 2.82 * tr))
        step = f / df
        y = y - step
        if np.max(np.abs(step)) < 1e-14:
            break
    return a * ppr / y


def z_papay(p_psia, t_f, sg):
    p, t, sg = np.broadcast_arrays(np.asarray(p_psia, float), np.asarray(t_f, float), np.asarray(sg, float))
    tpc, ppc = pseudo_critical(sg)
    tpr = (t + 459.67) / tpc
    ppr = p / ppc
    return 1 - 3.52 * ppr / 10 ** (0.9813 * tpr) + 0.274 * ppr ** 2 / 10 ** (0.8157 * tpr)


ZF = {"dak": z_dak, "hy": z_hy, "papay": z_papay}


def fpv2(p_psia, t_f, sg, method="dak"):
    z = ZF[method]
    return z(P_BASE, T_BASE_F, sg) / z(p_psia, t_f, sg)
