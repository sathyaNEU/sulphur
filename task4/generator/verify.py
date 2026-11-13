"""The independent verifier: recomputes the figures that rest on counting alone from target/ with its own code (no
analysis.py) and holds figures.json to them: the register's active kegs, the gate counters' in and out, the kegs
filled and the own kegs back at the washer in the year, and the stocktake's clean and repair counts."""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAIL = []


def ok(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((" (" + detail + ")") if detail else ""))
    if not cond:
        FAIL.append(label)


def main():
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    names = {f.split("_")[0] + "_" + f.split("_")[1]: f for f in os.listdir(T)}
    reg = pd.read_excel(os.path.join(T, [f for f in os.listdir(T) if f.startswith("keg_register")][0]), sheet_name="Kegs")
    for s in (50, 30, 20):
        n = int(((reg.size_l == s) & (reg.status == "ACTIVE")).sum())
        ok("V1 register active %d" % s, n == fj["register_%d" % s], "%d vs %d" % (n, fj["register_%d" % s]))
    g = pd.read_csv(os.path.join(T, [f for f in os.listdir(T) if f.startswith("depot_gate")][0]))
    g["size"] = g.keg_size.astype(str).str.extract(r"(\d+)").astype(int)
    g["d"] = pd.to_datetime(g.count_date)
    sel = g[(g.d > "2025-11-30") & (g.d <= "2026-11-30")]
    for s in (50, 30, 20):
        x = sel[sel["size"] == s]
        v = int(x.fulls_out.sum() - x.empties_in.sum())
        ok("V2 gate fulls out less empties in %d" % s, v == fj["gate_%d" % s], "%d vs %d" % (v, fj["gate_%d" % s]))
    fl = pd.read_csv(os.path.join(T, [f for f in os.listdir(T) if f.startswith("filling_log")][0]))
    fl["d"] = pd.to_datetime(fl.fill_date)
    wl = pd.read_csv(os.path.join(T, [f for f in os.listdir(T) if f.startswith("washer_log")][0]))
    wl["d"] = pd.to_datetime(wl.wash_date)
    rp = pd.read_csv(os.path.join(T, [f for f in os.listdir(T) if f.startswith("keg_repair")][0]))
    rp["b"] = pd.to_datetime(rp.back_to_washer)
    for s in (50, 30, 20):
        sent = int(fl[(fl.d > "2025-11-30") & (fl.d <= "2026-11-30") & (fl.keg_l == s)].kegs_filled.sum())
        ok("V3 kegs filled %d" % s, sent == fj["sent_%d" % s], "%d vs %d" % (sent, fj["sent_%d" % s]))
        x = wl[(wl.d > "2025-11-30") & (wl.d <= "2026-11-30") & (wl.keg_size_l == s)]
        rr = rp[(rp.outcome == "REPAIRED") & (rp.b > "2025-11-30") & (rp.b <= "2026-11-30") & (rp.size_l == s)]
        back = int(x.washed_ok.sum() + x.rejected_to_repair.sum() + x.condemned_at_inspection.sum() - len(rr))
        ok("V4 own kegs back %d" % s, back == fj["back_%d" % s], "%d vs %d" % (back, fj["back_%d" % s]))
    for s in (50, 30, 20):
        ok("V5 the order is the need less the fleet in the busiest week %d" % s,
           abs(fj["buy_%d" % s] - max(0, fj["need_%d" % s] - fj["have_%d" % s])) <= 20)
        ok("V6 the busiest week's fleet is the fleet less the loss to it %d" % s,
           abs(fj["have_%d" % s] - (fj["fleet_%d" % s] - fj["lost_to_week_%d" % s])) <= 20)
        ok("V7 the need's parts add up %d" % s,
           abs(fj["need_%d" % s] - (fj["part_existing_%d" % s] + fj["part_new_%d" % s] + fj["part_pipe_%d" % s] +
                                    fj["part_store_%d" % s] + fj["float_%d" % s])) <= 40)
    print("verify: %d FAIL" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
