"""task9: the independent verifier. Reads target/ with its own code (it imports nothing from the generator) and
recomputes what the answer blocks state that a reader can recompute without the posterior simulation: the replacements
the record holds per quarter, DC-3's migration-day install dates and the sources its ages are rebuilt from, the bad-build
window and its drives and July to September 2026 rate, the back-test's actual cells, the spare orders and the break-even
and flip arithmetic, and that the path sums to its total.

    python3 generator/verify.py        # exit 1 on any mismatch
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
FAILS = []
FAMILY = {"MD8000NM": "OM-6", "MD14TNM": "M-14", "MD16TNM": "M-16", "TS20000E": "T-20", "TS22000E": "W-22",
          "HX18T8A": "HX-8", "KS10T0A": "KS-10", "VB12000": "VB-12", "TS24000E": "X-24"}


def ok(name, cond, detail=""):
    print("%s  %-60s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def day(s):
    s = (s or "").strip()
    if not s:
        return None
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def fam(model):
    k = re.sub(r"[^A-Z0-9]", "", model.upper())
    for m, f in FAMILY.items():
        if k.endswith(m):
            return f
    return None


def qof(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def build_week(serial):
    s = serial.replace("-", "")
    if not s.startswith("KS") or len(s) < 13:
        return None
    try:
        return dt.date.fromisocalendar(2000 + int(s[4:6]), int(s[6:8]), 1)
    except ValueError:
        return None


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    inv = list(csv.DictReader(open(os.path.join(TGT, "drive_inventory.csv"))))
    tickets = list(csv.DictReader(open(os.path.join(TGT, "removal_tickets.csv"))))
    events = list(csv.DictReader(open(os.path.join(TGT, "vault_events.csv"))))
    # ---- the drives: data drives in fleet vaults, reseats merged
    drives = {}
    back = {}
    for r in inv:
        f = fam(r["model_string"])
        if f is None or not r["vault_id"] or r["vault_id"] == "QA-01":
            continue
        r = dict(r, family=f, removal=day(r["removal_date"]), install=day(r["install_date"]), first=day(r["first_seen"]))
        if r["serial"].endswith("-R"):
            back[r["serial"][:-2]] = r
        else:
            drives[r["serial"]] = r
    merged = 0
    for s, b in back.items():
        r = drives.get(s)
        if r and r["removal"] and b["install"] and (b["install"] - r["removal"]).days <= 30:
            r["removal"], r["removal_reason"] = b["removal"], b["removal_reason"]
            merged += 1
    # blank reasons from the tickets within three days, by serial, else by slot
    by_serial, by_slot = {}, {}
    for t in tickets:
        o = day(t["opened_ts"])
        if t["serial"]:
            by_serial.setdefault(t["serial"], []).append((o, t))
        by_slot.setdefault((t["vault_id"], t["chassis_id"], t["slot"]), []).append((o, t))
    cat = {"DRIVE_FAILURE": "FAIL", "HEALTH_PULL": "PULL"}
    for r in drives.values():
        if r["removal"] and r["removal_reason"] == "":
            c = [t for o, t in by_serial.get(r["serial"], []) if abs((o - r["removal"]).days) <= 3]
            if not c:
                c = [t for o, t in by_slot.get((r["vault_id"], r["chassis_id"], r["slot"]), [])
                     if abs((o - r["removal"]).days) <= 3 and t["category"] in cat]
            r["removal_reason"] = cat.get(c[0]["category"], "FAIL") if c else "FAIL"
    ok("reseats merged", merged > 0, "%d" % merged)
    rep = [r for r in drives.values() if r["removal"] and r["removal_reason"] in ("FAIL", "PULL")]
    hist = {}
    for r in rep:
        hist[qof(r["removal"])] = hist.get(qof(r["removal"]), 0) + 1
    for q, v in F["history"].items():
        ok("replacements in %s" % q, hist.get(q, 0) == v, "%d against %d" % (hist.get(q, 0), v))
    # ---- DC-3
    mig = [r for r in drives.values() if r["dc"] == "DC-3" and r["install"] == dt.date(2024, 3, 1)]
    ok("DC-3 drives with the migration day as install", len(mig) == F["record"]["migrated"], "%d" % len(mig))
    # ---- the bad builds: HX-8 drives by build week over the year to 30 September 2026, against each vault's level
    cut = dt.date(2026, 9, 30)
    a = cut - dt.timedelta(days=365)
    hx = [r for r in drives.values() if r["family"] == "HX-8" and r["first"] and r["first"] <= cut]
    for r in hx:
        end = r["removal"] if r["removal"] and r["removal"] <= cut else cut
        r["x"] = max((min(end, cut) - max(r["first"], a)).days, 0) / 365.25
        r["o"] = 1 if (r["removal"] and r["removal_reason"] in ("FAIL", "PULL") and a < r["removal"] <= cut) else 0
        r["x0"] = max((min(end, a) - r["first"]).days, 0) / 365.25
        r["o0"] = 1 if (r["removal"] and r["removal_reason"] in ("FAIL", "PULL") and r["removal"] <= a) else 0
        r["wk"] = build_week(r["serial"])
    r0 = sum(r["o0"] for r in hx) / max(sum(r["x0"] for r in hx), 1e-9)
    lvl = {}
    for v in {r["vault_id"] for r in hx}:
        o0 = sum(r["o0"] for r in hx if r["vault_id"] == v)
        x0 = sum(r["x0"] for r in hx if r["vault_id"] == v)
        lvl[v] = (o0 + 10.0) / (x0 * r0 + 10.0)
    for r in hx:
        r["xe"] = r["x"] * lvl[r["vault_id"]]
    weeks = sorted({r["wk"] for r in hx if r["wk"]})
    O = {w: sum(r["o"] for r in hx if r["wk"] == w) for w in weeks}
    X = {w: sum(r["xe"] for r in hx if r["wk"] == w) for w in weeks}
    to, tx = sum(r["o"] for r in hx), sum(r["xe"] for r in hx)
    best = (0.0, None)
    for i in range(len(weeks)):
        o = x = 0.0
        for j in range(i, len(weeks)):
            o += O[weeks[j]]
            x += X[weeks[j]]
            oo, xx = to - o, tx - x
            if o <= 0 or x <= 0 or xx <= 0 or o / x <= oo / xx:
                continue
            rr = to / tx
            v = o * math.log(o / x / rr) + (oo * math.log(oo / xx / rr) if oo > 0 else 0.0)
            if v > best[0]:
                best = (v, (weeks[i], weeks[j]))
    w0, w1 = best[1]
    got = ["%d-W%02d" % w0.isocalendar()[:2], "%d-W%02d" % w1.isocalendar()[:2]]
    ok("the bad-build window", got == F["hot_window"], "%s to %s (likelihood ratio %.1f)" % (got[0], got[1], best[0]))
    inw = [r for r in drives.values() if r["family"] == "HX-8" and r["wk"] and w0 <= r["wk"] <= w1 + dt.timedelta(days=6)]
    alive = [r for r in inw if r["first"] <= cut and not (r["removal"] and r["removal"] <= cut)]
    qa, qb = dt.date(2026, 7, 1), dt.date(2026, 10, 1)
    xs = sum(max((min(r["removal"] if r["removal"] and r["removal"] <= cut else dt.date(2026, 9, 30), dt.date(2026, 9, 30)) -
                  max(r["first"], qa)).days, 0) for r in inw if r["first"] <= cut) / 365.25
    os_ = sum(1 for r in inw if r["removal"] and r["removal_reason"] in ("FAIL", "PULL") and qa <= r["removal"] < qb)
    ok("the batch's drives in service", len(alive) == F["hot_batch"]["drives"], "%d against %d" % (len(alive), F["hot_batch"]["drives"]))
    ok("the batch's July to September rate", abs(os_ / xs - F["hot_batch"]["rate"]) < 5e-4,
       "%.4f against %.4f" % (os_ / xs, F["hot_batch"]["rate"]))
    # ---- the back-test's actual cells (stayed vaults, family by quarter)
    bc = dt.date(2025, 9, 30)
    gone = {e["vault_id"] for e in events if e["event_type"] == "DECOM_START"}
    present = {r["vault_id"] for r in drives.values() if r["first"] and r["first"] <= bc and not (r["removal"] and r["removal"] < bc)}
    stayed = present - gone
    act = {}
    for r in rep:
        if r["vault_id"] in stayed and dt.date(2025, 10, 1) <= r["removal"] < dt.date(2026, 10, 1):
            k = (qof(r["removal"]), r["family"])
            act[k] = act.get(k, 0) + 1
    bad = [c for c in F["gold"]["backtest_detail"] if act.get((c["q"], c["family"]), 0) != c["actual"]]
    ok("back-test actuals", not bad, "%d cells" % len(F["gold"]["backtest_detail"]) if not bad else str(bad[:2]))
    inside = sum(1 for c in F["gold"]["backtest_detail"] if c["lo"] <= c["actual"] <= c["hi"])
    ok("back-test coverage", abs(inside / len(F["gold"]["backtest_detail"]) - F["coverage"]) < 1e-3,
       "%d of %d" % (inside, len(F["gold"]["backtest_detail"])))
    # ---- the decision arithmetic from the procurement file
    y = open(os.path.join(TGT, "procurement_and_costs.yaml")).read()
    mig_cost = int(re.search(r"vault_migration_cost_usd:\s*(\d+)", y).group(1))
    handle = int(re.search(r"failure_handling_cost_usd:\s*(\d+)", y).group(1))
    be = mig_cost / (1200.0 * handle)
    ok("break-even share", abs(be - 0.2) < 1e-9, "%.3f" % be)
    stock = {m: int(n) for m, n in re.findall(r"^\s+(\w+):\s*(\d+)\s*$", y.split("unit_cost_usd:")[0], re.M)}
    model = {"OM-6": "MD8000NM", "M-14": "MD14TNM", "M-16": "MD16TNM", "T-20": "TS20000E", "W-22": "TS22000E",
             "HX-8": "HX18T8A", "KS-10": "KS10T0A", "VB-12": "VB12000", "X-24": "TS24000E"}
    bad = [f for f, n in F["spares"].items() if n != max(int(math.ceil(F["gold"]["spares_p90"][f])) - stock.get(model[f], 0), 0)]
    ok("spare orders from the 90th percentiles and the stock", not bad, ", ".join(bad) or "every family")
    line = mig_cost / handle
    pick = sorted(x for x, s in F["vaults"].items() if s["mean"] > line)
    ok("vaults to migrate are those over the break-even", pick == sorted(F["rec"]["migrate"]), "%s over %d" % (pick, line))
    h0 = F["hot_batch"]["rate"] / 12.0
    D = F["rec"]["flip"]
    H = h0 * D / math.log(2) * (2 ** (24.0 / D) - 1)
    ok("flip point", abs(1 - math.exp(-H) - be) < 0.005, "%.4f at %.1f months" % (1 - math.exp(-H), D))
    ok("path sums to its total", abs(sum(F["path"].values()) - F["total"]) <= 2, "%d against %d" % (sum(F["path"].values()), F["total"]))
    print("%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
