"""task2 architecture 4: the data files of the pack, written the way the site's database and its contractors
write them: collars, 1 m assays from two laboratories, the QAQC results, bulk densities, weathering logs, the Stage 5
design, and two files that look relevant and are not (the metallurgical testwork and the Stage 4 survey pickup)."""
import csv
import datetime as dt
import io
import math

import numpy as np
import openpyxl
from openpyxl.styles import Font

import ooxml
import params as P

LABS = {"old": ("Goldfields Assay Laboratories", "FA50", "ppm"), "new": ("Boulder Analytical", "FA30", "g/t")}
CRMS = [("GCRM-05", 0.512), ("GCRM-21", 1.985), ("GCRM-44", 4.672)]


def _csv(rows, header):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


def _fmt(v, dl=0.01):
    if v < dl:
        return "<%.2f" % dl
    return "%.2f" % v if v < 10 else "%.1f" % v


def hole_ids(holes):
    """Hole numbers as the database issues them: consecutive within each programme, with the numbers of holes
    abandoned or never drilled skipped."""
    skip = np.random.default_rng(P.SEED + 41)
    n_rc, n_dd, n_gc = 16, 4, 0
    order = sorted(range(len(holes)), key=lambda i: (holes[i]["campaign"], holes[i]["y"], holes[i]["x"]))
    ids = [None] * len(holes)
    for i in order:
        h = holes[i]
        if h["type"] == "GC":
            n_gc += 1
            ids[i] = "MCGC%04d" % (2400 + n_gc)
        elif h["type"] == "RC":
            n_rc += 1 + (1 if skip.random() < 0.06 else 0)
            ids[i] = "MCRC%04d" % n_rc
        else:
            n_dd += 1 + (1 if skip.random() < 0.08 else 0)
            ids[i] = "MCDD%03d" % n_dd
    return ids


def write_all(paths, truth):
    rng = np.random.default_rng(P.SEED + 3)
    holes = truth["holes"]
    ids = hole_ids(holes)
    cell = truth["cell"]
    ox, tr = truth["ox"], truth["tr"]
    collars, assays, qaqc, dens, weath = [], [], [], [], []
    sid = {"old": 104300, "new": 22800}
    for h, hid in sorted(zip(holes, ids), key=lambda t: t[1]):
        new = h["campaign"] >= 2022
        lab = "new" if h["campaign"] >= 2023 else "old"
        e, n = P.GRID_E0 + h["x"], P.GRID_N0 + h["y"]
        grid = "MGA94_51" if new else "MINE"
        ce, cn = (e + P.MGA_SHIFT[0], n + P.MGA_SHIFT[1]) if new else (e, n)
        depth = (20.0 if h["type"] == "GC" else
                 round(100.0 + rng.uniform(0, 6) if h["type"] == "RC" else 100.0 + rng.uniform(2, 14), 1))
        collars.append((hid, "RC" if h["type"] == "GC" else h["type"], "%.2f" % ce, "%.2f" % cn, "%.2f" % (P.TOP_RL + rng.normal(0.4, 0.15)), grid,
                        "%.1f" % depth, -90, 0, "%d-%02d-%02d" % (h["campaign"], int(rng.integers(2, 12)),
                                                                 int(rng.integers(1, 28)))))
        ix, iy = min(int(h["x"] / P.D), P.NX - 1), min(int(h["y"] / P.D), P.NY - 1)
        # weathering log from the surfaces at the collar
        oxd, trd = P.TOP_RL - ox[ix, iy], P.TOP_RL - tr[ix, iy]
        weath.append((hid, "0.0", "%.1f" % oxd, "OX"))
        weath.append((hid, "%.1f" % oxd, "%.1f" % trd, "TR"))
        weath.append((hid, "%.1f" % trd, "%.1f" % depth, "FR"))
        # sample intervals
        a = 0.0
        while a < depth - 0.05:
            if h["type"] == "DD":
                ln = float(np.clip(round(rng.choice([0.7, 0.8, 1.0, 1.0, 1.0, 1.2, 1.3]), 1), 0.5, 1.5))
            else:
                ln = 1.0
            b = min(round(a + ln, 1), depth)
            mid = (a + b) / 2
            k = min(int(mid / P.D), P.NZ - 1)
            if rng.random() < 0.012:          # no recovery, not sampled
                a = b
                continue
            geo = math.exp(rng.normal(0, 0.70) - 0.245)
            split = math.exp(rng.normal(0, 0.35) - 0.06125)
            labe = math.exp(rng.normal(0, P.S_ASSAY) - P.S_ASSAY ** 2 / 2)
            v = cell[ix, iy, k] * geo * split * labe if mid < 100 else cell[ix, iy, P.NZ - 1] * geo * split
            s = sid[lab]
            sid[lab] += 1
            labname, meth, unit = LABS[lab]
            assays.append((hid, "%.1f" % a, "%.1f" % b, "MC%06d" % s, _fmt(v, 0.02 if lab == "new" else 0.01), unit,
                           meth, labname, ""))
            if v >= 5.0 and rng.random() < 0.7:
                rv = cell[ix, iy, k] * geo * split * math.exp(rng.normal(0, 0.12))
                assays.append((hid, "%.1f" % a, "%.1f" % b, "MC%06dR" % s, _fmt(rv), unit, "SFA", labname,
                               "screen fire re-assay"))
            if sid[lab] % 20 == 0:             # the QAQC slot after every 19 samples
                sid[lab] += 1
                kind = int(sid[lab] // 20) % 3
                qid = "MC%06d" % sid[lab]
                if kind == 0:
                    name, cert = CRMS[int(rng.integers(0, 3))]
                    res = cert * math.exp(rng.normal(0.0, 0.03))
                    if lab == "old" and 105900 <= sid[lab] <= 106400 and name == "GCRM-21":
                        res = cert * 1.11 * math.exp(rng.normal(0, 0.02))   # one batch out of tolerance
                    qaqc.append((qid, "CRM", name, "%.3f" % cert, "%.3f" % res, "", hid, labname))
                elif kind == 1:
                    qaqc.append((qid, "BLANK", "BL-quartz", "<0.01", _fmt(abs(rng.normal(0.003, 0.004))), "", hid,
                                 labname))
                else:
                    dv = cell[ix, iy, k] * geo * math.exp(rng.normal(0, 0.35) - 0.06125) * math.exp(
                        rng.normal(0, P.S_ASSAY) - P.S_ASSAY ** 2 / 2)
                    qaqc.append((qid, "FIELD_DUP", "", "", _fmt(dv), "MC%06d" % s, hid, labname))
            a = b
        if h["type"] == "DD":
            for z in np.arange(3.0, depth, 9.0) + rng.uniform(0, 3):
                rl = P.TOP_RL - z
                zn = "OX" if rl > ox[ix, iy] else ("TR" if rl > tr[ix, iy] else "FR")
                dens.append((hid, "%.2f" % z, zn, "%.2f" % (P.DENSITY[zn] * math.exp(rng.normal(0, 0.035))),
                             "Archimedes, wax-coated" if zn != "FR" else "Archimedes"))
    open(paths["collars"], "wb").write(_csv(collars, ["hole_id", "hole_type", "east", "north", "rl", "grid",
                                                      "total_depth", "dip", "azimuth", "date_completed"]))
    open(paths["assays"], "wb").write(_csv(assays, ["hole_id", "depth_from", "depth_to", "sample_id", "au",
                                                    "unit", "method", "laboratory", "comment"]))
    open(paths["qaqc"], "wb").write(_csv(qaqc, ["sample_id", "qc_type", "standard", "certified_au", "result_au",
                                                "parent_sample_id", "hole_id", "laboratory"]))
    open(paths["density"], "wb").write(_csv(dens, ["hole_id", "depth", "weathering", "density_t_m3", "method"]))
    open(paths["weathering"], "wb").write(_csv(weath, ["hole_id", "depth_from", "depth_to", "weathering"]))
    rows = []
    for k in range(P.S5_FLITCHES):
        e0, e1, n0, n1 = P.S5_TOP
        s = P.S5_STEP * k
        rows.append((k + 1, "%.1f" % (P.TOP_RL - k * P.D), "%.1f" % (P.TOP_RL - (k + 1) * P.D), "%.2f" % (e0 + s),
                     "%.2f" % (e1 - s), "%.2f" % (n0 + s), "%.2f" % (n1 - s)))
    open(paths["design"], "wb").write(_csv(rows, ["flitch", "rl_top", "rl_bottom", "east_min", "east_max",
                                                  "north_min", "north_max"]))
    return {"assays": len(assays), "qaqc": len(qaqc), "collars": len(collars)}


def write_metallurgy(path, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bottle rolls"
    ws.append(["Test", "Hole", "From (m)", "To (m)", "Weathering", "Head grade (g/t)", "Grind P80 (um)",
               "24 h recovery (%)", "48 h recovery (%)", "NaCN (kg/t)", "Lime (kg/t)"])
    for k in range(18):
        zn = ["OX", "TR", "FR"][k % 3]
        head = round(float(np.exp(rng.normal(0.95, 0.45))), 2)
        rec = {"OX": 94.5, "TR": 91.2, "FR": 88.6}[zn] + rng.normal(0, 1.2)
        top = int(rng.integers(6, 95))
        ws.append(["BR-%02d" % (k + 1), "MCDD%03d" % int(rng.integers(5, 60)), top, top + int(rng.integers(3, 7)), zn,
                   head, 75,
                   round(rec - 3.1, 1), round(rec, 1), round(0.42 + 0.1 * rng.random(), 2), round(1.1 + 0.6 * rng.random(), 2)])
    for c in ws[1]:
        c.font = Font(bold=True)
    wb.properties.creator = "Tallowood Processing"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2025, 8, 12, 9, 5), dt.datetime(2025, 9, 1, 11, 40), "Tallowood Processing")


def write_survey(path, rng):
    rows = []
    for k in range(2400):
        e = 920 + rng.uniform(0, 70)
        n = 2050 + rng.uniform(0, 300)
        rl = 330 + (e - 920) * 0.9 + rng.normal(0, 0.3)
        rows.append(("P%05d" % (k + 1), "%.3f" % (e + P.MGA_SHIFT[0]), "%.3f" % (n + P.MGA_SHIFT[1]), "%.3f" % rl,
                     "TOE" if k % 7 == 0 else ("CREST" if k % 7 == 1 else "FLOOR")))
    open(path, "wb").write(_csv(rows, ["point", "east_mga", "north_mga", "rl", "code"]))
