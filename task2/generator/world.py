"""task2 architecture 4: the clean truth of Mount Carrow before any file is written: the grade field, the true
grade of every 5 m by 5 m by 2.5 m block, the weathering surfaces, the drillholes and their 1 m samples."""
import math

import numpy as np

import params as P


def gauss_field(rng, rng_m, anis_z):
    """A standard Gaussian field on the grid with a Gaussian-shaped covariance of practical range rng_m."""
    nx, ny, nz, d = P.NX, P.NY, P.NZ, P.D
    kx = np.fft.fftfreq(nx * 2, d)[:, None, None]
    ky = np.fft.fftfreq(ny * 2, d)[None, :, None]
    kz = np.fft.fftfreq(nz * 2, d)[None, None, :]
    sx = sy = rng_m / math.sqrt(3)
    sz = rng_m * anis_z / math.sqrt(3)
    spec = np.exp(-2 * math.pi ** 2 * ((kx * sx) ** 2 + (ky * sy) ** 2 + (kz * sz) ** 2))
    f = np.real(np.fft.ifftn(np.fft.fftn(rng.normal(size=(nx * 2, ny * 2, nz * 2))) * np.sqrt(spec)))[:nx, :ny, :nz]
    return (f - f.mean()) / f.std()


def cell_centres():
    e = P.GRID_E0 + (np.arange(P.NX) + 0.5) * P.D
    n = P.GRID_N0 + (np.arange(P.NY) + 0.5) * P.D
    rl = P.TOP_RL - (np.arange(P.NZ) + 0.5) * P.D
    return e, n, rl


def weathering_surfaces(rng):
    e, n, _ = cell_centres()
    ee, nn = np.meshgrid(e, n, indexing="ij")
    ox = P.OX_BASE + 2.2 * np.sin((ee - 1000) / 71.0) + 1.6 * np.cos((nn - 2000) / 93.0)
    tr = P.TR_BASE + 1.8 * np.sin((ee - 1000) / 83.0 + 0.7) + 1.4 * np.cos((nn - 2000) / 61.0 + 0.3)
    return ox, tr


def in_stage5(e, n, rl):
    """Whether a point (mine grid) lies inside the Stage 5 design."""
    k = np.floor((P.TOP_RL - np.asarray(rl)) / P.D).astype(int)
    ok = (k >= 0) & (k < P.S5_FLITCHES)
    e0, e1, n0, n1 = P.S5_TOP
    s = P.S5_STEP * np.clip(k, 0, None)
    return ok & (e >= e0 + s) & (e <= e1 - s) & (n >= n0 + s) & (n <= n1 - s)


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    L = gauss_field(np.random.default_rng(seed + 11), P.R_LONG, P.AN_LONG)
    Sh = gauss_field(np.random.default_rng(seed + 12), P.R_SHORT, P.AN_SHORT)
    # the cell grade carries the mean of the sample scatter, so samples and cells share one mean
    cell = np.exp(P.MU + P.S_LONG * L + P.S_SHORT * Sh + P.S_NUG_1M ** 2 / 2)
    blocks = cell.reshape(P.NX // 2, 2, P.NY // 2, 2, P.NZ, 1).mean(axis=(1, 3, 5))
    be = P.GRID_E0 + (np.arange(P.NX // 2) + 0.5) * 5.0
    bn = P.GRID_N0 + (np.arange(P.NY // 2) + 0.5) * 5.0
    brl = P.TOP_RL - (np.arange(P.NZ) + 0.5) * P.D
    BE, BN, BR = np.meshgrid(be, bn, brl, indexing="ij")
    s5 = in_stage5(BE, BN, BR)
    ox, tr = weathering_surfaces(rng)
    oxb = ox.reshape(P.NX // 2, 2, P.NY // 2, 2).mean(axis=(1, 3))[:, :, None]
    trb = tr.reshape(P.NX // 2, 2, P.NY // 2, 2).mean(axis=(1, 3))[:, :, None]
    zone = np.where(BR > oxb, "OX", np.where(BR > trb, "TR", "FR"))
    dens = np.vectorize(P.DENSITY.get)(zone)
    tonnes = 5.0 * 5.0 * 2.5 * dens
    holes = drill(L, cell, rng)
    return {"cell": cell, "blocks": blocks, "s5": s5, "tonnes": tonnes, "zone": zone, "ox": ox, "tr": tr,
            "holes": holes, "L": L, "rng": rng}


def drill(L, cell, rng):
    """Collars: the 2019 to 2021 grid, then the 2022 to 2024 infill where the nearest grid holes ran high."""
    holes = []
    sp = P.GRID_SPACING
    for i, x in enumerate(np.arange(sp / 2, P.NX * P.D, sp)):
        for j, y in enumerate(np.arange(sp / 2, P.NY * P.D, sp)):
            holes.append({"x": x + rng.normal(0, 0.6), "y": y + rng.normal(0, 0.6), "campaign": 2019 + (i + j) % 3,
                          "type": "RC"})
    grid_mean = {}
    for h in holes:
        ix, iy = int(h["x"] / P.D), int(h["y"] / P.D)
        grid_mean[(h["x"], h["y"])] = float(cell[ix, iy, :].mean())
    sp2 = P.INFILL_SPACING
    for x in np.arange(sp2 / 2, P.NX * P.D, sp2):
        for y in np.arange(sp2 / 2, P.NY * P.D, sp2):
            if abs((x - sp / 2) / sp - round((x - sp / 2) / sp)) < 1e-9 and abs((y - sp / 2) / sp - round((y - sp / 2) / sp)) < 1e-9:
                continue
            near = sorted(grid_mean.items(), key=lambda kv: (kv[0][0] - x) ** 2 + (kv[0][1] - y) ** 2)[:4]
            if np.mean([v for _, v in near]) > P.INFILL_TRIGGER:
                holes.append({"x": x + rng.normal(0, 0.6), "y": y + rng.normal(0, 0.6),
                              "campaign": 2022 + int(rng.integers(0, 3)), "type": "DD" if rng.random() < 0.4 else "RC"})
    # the 2024 grade control trial: a 5 m RC pattern over 50 m by 50 m, drilled to 20 m, ahead of the selective fleet
    for x in np.arange(112.5, 162.5, 5.0):
        for y in np.arange(222.5, 272.5, 5.0):
            holes.append({"x": x + rng.normal(0, 0.15), "y": y + rng.normal(0, 0.15), "campaign": 2024, "type": "GC"})
    return holes
