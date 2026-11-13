"""task23 architecture 1 build: the simulated landfill, the pack under target/ (the systems' exports, the workbooks
the people keep, the four documents), the analysis read back from the pack alone, figures.json and effort.json, the
golden workbook and deck, submission.md and metadata.json.

    python3 make.py            builds in place
"""
import datetime as dt
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402

import analysis as A  # noqa: E402
import deliver as DL  # noqa: E402
import docs as DC  # noqa: E402
import metadata as MD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import postprocess  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402

TONS = 1.0 / 0.90718474


def report_history(W, F):
    """The division's reported figures, 2021 to 2025: the collected methane as its plant historian summed it (the
    pack's hourly plant export from 2023, the historian's yearly totals before it) and the rule's equation on each
    year's areas."""
    sm = A.scada_monthly(F)
    rows = []
    for y in range(2021, 2026):
        if y >= 2023:
            col = float(sm[[m for m in range(A.mi(y, 1), A.mi(y + 1, 1)) if m in sm.index]].sum())
        else:
            i0 = WD.month_index(y, 1)
            col = float(sum(W.coll[c][i0:i0 + 12].sum() for c in P.CELLS)) * (1 + 0.006 * (y - 2020))
        areas = P.RULE_AREAS_2025 if y == 2025 else P.RULE_AREAS_HIST
        ce = sum(a * P.RULE["ce"][k] for k, a in areas.items()) / sum(areas.values())
        em = (col / ce - col) * (1 - P.RULE["ox"]) + col * (1 - P.RULE["de"])
        rows.append((y, round(col), round(em)))
    return rows


def waste_in_place(F, end=dt.date(2025, 12, 31)):
    H = F["history"]
    tons = float(H[["msw_tons", "cd_tons", "biosolids_tons", "special_tons"]].sum().sum())
    t = A.tickets_monthly(F, "clean")
    t = t[(t["ticket_date"] <= end) & (t["mat"] != "SOIL")]
    return tons + float(t["net_tons"].sum())


def build(task_dir, gen_out):
    target = os.path.join(task_dir, "target")
    gold = os.path.join(task_dir, "golden")
    for d in (target, gold):
        if os.path.isdir(d):
            shutil.rmtree(d)
    W = WD.World()
    F0 = PK.frames(W)
    counts, stamps = PK.write(W, F0, target)
    F = A.load(target)
    sm = A.scada_monthly(F)
    r_col = float(sm[[m for m in range(A.mi(2025, 1), A.mi(2026, 1))]].sum())
    hist = report_history(W, F)
    wip = round(waste_in_place(F), -3)
    monthly = [(dt.date(2025, k, 1).strftime("%B"), float(sm[A.mi(2025, k)])) for k in range(1, 13)]
    filed = DC.write_all(target, F, r_col, hist, wip, monthly)
    postprocess.own_mtimes(target, stamps)
    figs, E, out, cache = RS.write(F, gen_out)
    figs["_filed"] = dict(filed, history=hist, wip_tons=wip)
    figs["_truth"] = {"actual_2025_t": round(W.truth_year(2025)),
                      "emissions_2027_t": {"package %s" % p: round(W.truth_2027(p)) for p in P.PACKAGES},
                      "cell5_generation_2027_t": round(float(W.gen[5][WD.month_index(2027, 1):WD.month_index(2028, 1)].sum())),
                      "cell4_generation_change_pct": round(100.0 * (float(W.gen[4][A.mi(2025, 11):A.mi(2026, 11)].sum())
                                                                    / float(W.gen[4][A.mi(2022, 1):A.mi(2023, 1)].sum()) - 1), 1)}
    json.dump(figs, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, default=str)
    DL.write(F, out["golden"], out, figs, gold)
    WU.write(figs, E, os.path.join(task_dir, "submission.md"))
    # the figures the pack itself files and the answer blocks restate: the limit, the packages' costs, the report's
    # collected methane, efficiency and figure, and the survey's figure
    stated = ["{:,.0f}".format(P.LIMIT_T)] + ["%.2f" % P.PACKAGES[p]["cost"] for p in P.PACKAGES] + [
        "{:,.0f}".format(figs["collected_2025_t"]), "%.4f" % figs["_extra"]["rule"]["ce_2025"],
        "{:,.0f}".format(figs["report_2025_t"]), "{:,.0f}".format(figs["survey_2025_t"])]
    json.dump(MD.metadata(target, counts, stated), open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
    return W, F, figs, E, out


if __name__ == "__main__":
    build(TASK, HERE)
    print("built", TASK)
