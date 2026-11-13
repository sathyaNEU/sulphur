"""task9: the independent verifier (python3 verify.py <out>). Reads only the bundle (target/, the answer blocks' figures
and the golden zip), on its own code path, reads back every format the pack ships with a positive control, and
recomputes the figures it can from the rows."""
import csv
import datetime as dt
import json
import math
import os
import sqlite3
import subprocess
import sys
import zipfile

import numpy as np
import openpyxl
import yaml

OUT = []


def check(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def norm(s):
    return s.replace(".", "")


def main(out=None):
    here = os.path.dirname(os.path.abspath(__file__))
    gen = here if out is None else out
    out = os.path.dirname(here) if out is None else out
    tgt = os.path.join(out, "target")
    fg = json.load(open(os.path.join(gen, "figures.json")))
    B = fg["bands"]
    P = lambda n: os.path.join(tgt, n)
    # ---- every format read back, with a positive control on the same path
    plan = subprocess.run(["pdftotext", P("vr90_ramp_plan_q1_2027.pdf"), "-"], capture_output=True, text=True).stdout
    check("read pdf: the ramp plan's commitment", "412,000 good VR90 units" in plan and "2,400 wafers" in plan and len(plan) > 1000)
    check("read pdf: the plan's bench loading and share", "31 lots a day" in plan and "21 per cent" in plan)
    cost = yaml.safe_load(open(P("cost_inputs_2027.yaml")))
    check("read yaml: cost inputs", cost["die_value_per_good_die"]["VR90"] == 41.0 and cost["ct_etch_wet_clean"]["parts_and_labour"] == 2900)
    wb = openpyxl.load_workbook(P("product_data_sheet.xlsx"), read_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    vr = [r for r in rows if r and r[0] == "VR90"][0]
    check("read xlsx: VR90's die and gate area", abs(vr[4] - 320.32) < 0.01 and vr[6] == 53.4 and vr[13] == 0.981, str(vr[:7]))
    lab = list(openpyxl.load_workbook(P("lab_bath_metals_2026.xlsx"), read_only=True).worksheets[0].iter_rows(values_only=True))
    check("read xlsx: the lab's samples", len(lab) > 100 and lab[0][0] == "sample_id")
    nj = 0
    with open(P("pgc_bench_controller.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            json.loads(line)
            nj += 1
    check("read jsonl: the bench log parses line by line", nj > 15000, "%d lines" % nj)
    notes = open(P("shift_handover_ft2_2026.txt"), encoding="utf-8").read()
    check("read txt: the shift book", "SDS-OX1" in notes and len(notes) > 2000)
    con = sqlite3.connect(P("fab2_yield.sqlite"))
    check("read sqlite: products and maps", con.execute("SELECT COUNT(*) FROM product").fetchone()[0] == 2 and
          con.execute("SELECT COUNT(*) FROM sort_map").fetchone()[0] > 10000)
    with zipfile.ZipFile(os.path.join(out, "task9_golden.zip")) as z:
        check("read zip: the golden holds exactly the two requested files", sorted(z.namelist()) ==
              ["vr90_ramp_yield_note.docx", "vr90_ramp_yield_review.xlsx"])
    # ---- R1 from the database, final insertion of every wafer
    last = {}
    for key, ins, prod, end, good in con.execute("SELECT wafer_key, insertion, product, end_time, good FROM sort_wafer"):
        if key not in last or ins > last[key][0]:
            last[key] = (ins, prod, dt.datetime.strptime(end, "%Y-%m-%d %H:%M:%S"), good)
    def mean_good(prod, a, b):
        x = [g for _, p, t, g in last.values() if p == prod and a <= t <= b]
        return sum(x) / len(x)
    for prod in ("VX40", "VP12"):
        s = mean_good(prod, dt.datetime(2026, 1, 1), dt.datetime(2026, 3, 31, 23, 59, 59)) - \
            mean_good(prod, dt.datetime(2026, 6, 1), dt.datetime(2026, 9, 30, 23, 59, 59))
        check("R1 recomputed: %s shortfall matches the blocks" % prod, abs(round(s, 1) - fg["R1_shortfall"][prod]) < 0.05,
              "%.2f against %s" % (s, fg["R1_shortfall"][prod]))
    # ---- R2: bin 5 per VX40 wafer by polisher and the loop's state, from the trend's flow (its own thresholds)
    bins = {}
    for key, ins, b, n in con.execute("SELECT wafer_key, insertion, bin, die FROM sort_bin_count"):
        if last[key][0] == ins:
            bins.setdefault(key, {})[b] = n
    flow_t, flow_v = [], []
    with open(P("sds_ox1_trend_export.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["tag"] == "FT-101":
                flow_t.append(dt.datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S").timestamp())
                flow_v.append(float(r["value"]) * (3.785411784 if r["unit"] == "gpm" else 1.0))
    flow_t, flow_v = np.array(flow_t), np.array(flow_v)
    pol = {}
    for tool in ("CM1", "CM2", "CM4"):
        with open(P("%s_ild0_polish.csv" % tool), newline="") as fh:
            for r in csv.DictReader(fh):
                if tool == "CM1":
                    pol[(norm(r["LotID"]), int(r["Slot"]))] = ("CM1", dt.datetime.strptime(r["StartTime"], "%Y-%m-%d %H:%M:%S") - dt.timedelta(minutes=4))
                else:
                    pol[(norm(r["lot_id"]), int(r["wafer_id"].rsplit("-", 1)[1]))] = (tool, dt.datetime.strptime(r["start_ts"], "%Y-%m-%d %H:%M:%S"))
    with open(P("CM3_ild0_polish.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            pol[(norm(r["Los"]), int(r["Scheibe"]))] = ("CM3", dt.datetime.strptime(r["Startzeit"], "%d.%m.%Y %H:%M:%S"))
    tab = {}
    for key, (ins, prod, t, good) in last.items():
        if prod != "VX40":
            continue
        lot, slot = key.rsplit("-", 1)
        p = pol.get((lot, int(slot)))
        if not p:
            continue
        i = max(0, int(np.searchsorted(flow_t, p[1].timestamp(), side="right")) - 1)
        q = flow_v[i]          # L/min: about 54 in spring, 34 at 38 Hz, 62 on the standby pump
        state = "standby" if q > 58 else ("spring" if q > 44 else "slow")
        bb = bins[key]
        tested = sum(bb.values())
        x = bb.get(5, 0) * tested / max(1, tested - bb.get(3, 0) - bb.get(4, 0))
        tab.setdefault((p[0], state), []).append((bb.get(5, 0), x))
    for tool in ("CM1", "CM2", "CM3", "CM4"):
        for state in ("spring", "slow"):
            v, r = np.mean(np.array(tab[(tool, state)]), axis=0)
            check("R2 recomputed: %s %s bin 5 per wafer" % (tool, state), abs(v - fg["bin5_by_polisher"][tool][state]) < 0.15,
                  "%.2f against %s" % (v, fg["bin5_by_polisher"][tool][state]))
            check("R2 recomputed: %s %s bin 5 per wafer on die at risk" % (tool, state), abs(r - fg["bin5_at_risk"][tool][state]) < 0.15,
                  "%.2f against %s" % (r, fg["bin5_at_risk"][tool][state]))
    # ---- every graded figure inside its band, the ranking forced
    for rid, key in (("R2", "R2_loop"), ("R3", "R3_bath"), ("R4", "R4_edge"), ("R5", "R5_etch")):
        for cell in ("VX40", "VR90"):
            b = B[rid][cell]
            v = fg[key][cell]
            check("band: %s %s mid-band" % (rid, cell), b[0] < v < b[1], "%s in %s" % (v, b))
    order = sorted([fg[k]["VX40"] for k in ("R2_loop", "R3_bath", "R4_edge", "R5_etch")], reverse=True)
    check("ranking: edge, loop, bath, etch", order == [fg["R4_edge"]["VX40"], fg["R2_loop"]["VX40"], fg["R3_bath"]["VX40"], fg["R5_etch"]["VX40"]])
    st = 412000 / (184 * fg["R6_fixed"] / 100 * 0.992 * 0.981)
    check("R7 recomputed: the wafer starts from the fixed yield and the plan's back end", abs(st - fg["R7_plan"]["starts"]) < 15,
          "%.0f against %s" % (st, fg["R7_plan"]["starts"]))
    # ---- the answer blocks state the figures
    sub = open(os.path.join(out, "submission.md")).read()
    for v in (fg["R6_fixed"], fg["R7_plan"]["plan"], fg["R2_loop"]["VR90"], fg["R5_etch"]["VR90"]):
        check("blocks: %s stated" % v, str(v) in sub)
    fails = [r for r in OUT if not r[1]]
    for label, good, detail in OUT:
        print("%s  %s  %s" % ("PASS" if good else "FAIL", label, detail))
    print("%d checks, %d failed" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
