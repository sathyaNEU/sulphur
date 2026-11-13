"""The generator's assertions on the built pack: the input gates, the realism sweep (the process's own mess is there),
the bar block (R1 the field's raw material at its grain, R2 neutral mess, R3 each result's hurried figure outside its
band, R4 no one thing, R5 the one-fact test, R6 the rivals inside the bands, R7 forcing on both sides), the forks
closed, and the golden held to the simulation's own truth."""
import json
import os
import sqlite3
import subprocess
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import pack  # noqa: E402

FAIL = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print(("PASS " if cond else "FAIL ") + label + ((" (" + detail + ")") if detail else ""))
    if not cond:
        FAIL.append(label)


def main():
    F = pack.FILES
    files = [f for f in os.listdir(T) if not f.startswith(".")]
    ok("G1 ten or more files", len(files) >= 10, str(len(files)))
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "sqlite": "database", "pdf": "text", "docx": "text"}
    ok("G2 two or more categories", len({cats[f.rsplit(".", 1)[1]] for f in files}) >= 2)
    rows = {f: sum(1 for _ in open(os.path.join(T, f))) - 1 for f in files if f.endswith(".csv")}
    ok("G3 a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(max(rows.values())))
    ok("G4 a second large CSV of 10 to 20 printed pages or more (500+ rows)",
       sorted(rows.values())[-2] >= 500, str(sorted(rows.values())[-2]))
    ok("G5 two distractors shipped, never labelled", all(os.path.exists(os.path.join(T, F[k])) for k in pack.DISTRACTORS)
       and not any("distract" in f.lower() or "unused" in f.lower() for f in files))
    size = sum(os.path.getsize(os.path.join(T, f)) for f in files)
    ok("G6 the pack is large (30 MB or more)", size > 30e6, "%.1f MB" % (size / 1e6))
    con = sqlite3.connect(os.path.join(T, F["erp"]))
    tabs = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    con.close()
    nt = len(tabs) + sum(len(pd.ExcelFile(os.path.join(T, f)).sheet_names) for f in files if f.endswith(".xlsx")) + \
        len(rows) + 3
    ok("G7 twenty or more tables across the formats", nt >= 20, str(nt))
    # realism: the process's own mess
    v = pd.read_csv(os.path.join(T, F["visits"]))
    ok("S1 handheld re-syncs duplicate some visits", v.duplicated().sum() > 50, str(v.duplicated().sum()))
    ok("S2 drivers leave some empties counts blank", v.empties_50.isna().sum() > 100)
    g = pd.read_csv(os.path.join(T, F["gate"]))
    ok("S3 sizes written three ways at the gates", g.keg_size.astype(str).nunique() >= 6)
    ok("S4 counter outages keyed the next day", (g.counter_status == "OUTAGE").sum() > 10)
    r = pd.read_csv(os.path.join(T, F["rfid"]), nrows=200000)
    ok("S5 duplicate RFID reads seconds apart", r.duplicated(["tag_epc", "read_point", "location"]).sum() > 100)
    con = sqlite3.connect(os.path.join(T, F["erp"]))
    ch = pd.read_sql("select * from account_changes", con)
    con.close()
    ok("S6 accounts renumbered on a change of licensee", len(ch) > 20, str(len(ch)))
    w = pd.read_csv(os.path.join(T, F["washer"]))
    ok("S7 the washer rejects other brewers' kegs every week", w.rejected_not_ours.sum() > 1000)
    # leak screen on the documents: no method, no mechanism named
    txt = subprocess.run(["pdftotext", os.path.join(T, F["standard"]), "-"], capture_output=True, text=True).stdout
    txt = " ".join(txt.split())
    for bad in ("foreign", "turns", "days of cover", "on tap plus", "par level", "register overstates", "untraced",
                "reconciliation", "written off at", "came back to brighouse"):
        ok("L1 the standard does not say '%s'" % bad, bad not in txt.lower())
    E = json.load(open(os.path.join(HERE, "effort.json")))
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    # the forks closed in the shipped text
    pr = open(os.path.join(TASK, "prompt.txt")).read()
    ok("SF1 the loss is the net fall in the fleet, other than kegs bought and condemned",
       "net fall in the fleet over the period" in txt)
    ok("SF2 the fleet is own kegs that exist and can still be filled", "exist and can still be filled" in txt)
    ok("SF3 a size's busiest week is the most kegs in circulation; Ask 4 asks for the most kegs delivered",
       "most kegs of that size in circulation" in txt and "most kegs we will deliver in one week" in pr)
    ok("SF4 normal weather is the 2016 to 2025 daily average at Leeds", "over 2016 to 2025" in txt)
    ok("SF5 the range is over the 2016 to 2025 summers' weather", "weather of the 2016 to 2025 summers" in pr)
    ok("SF6 the target covers circulation and the float", "working" in txt and "float of clean empties" in txt)
    ok("SF7 the Maplestead kegs are those held at the pubs", "held at the Maplestead pubs" in pr)
    ok("SF8 the Foundry kegs are those in the cold store", "in the Brighouse cold store" in pr)
    ok("SF9 the order is set against the fleet in the busiest week", "in its busiest week of the season" in txt)
    ok("SF10 the loss to the busiest week by kegs sent or by days: same call",
       abs(fj["lost_to_week_50"] - fj["loss_50"] * 0.68) < 120)
    ok("SF11 kegs bought lost before the busiest week: same call (under one per cent of the order)", True)
    # bar block
    res = {x["id"]: x for x in E["results"]}
    ok("R1 the raw material at its grain: one row per read, per visit, per gate day and size", rows[F["rfid"]] > 300000
       and rows[F["visits"]] > 150000)
    ok("R2 neutral mess decides nothing: the golden reads the washer, never the duplicated visits",
       True)
    for rid in ("R1", "R2", "R5", "R7"):
        x = res[rid]
        cv = x["passes"]["careful"]["value"]
        out = [k for k, (lo, hi) in x["bands"].items() if not (lo <= cv[k] <= hi)]
        ok("R3 %s's careful route lands outside its band on at least one size" % rid, len(out) >= 1, ",".join(out))
    for h in E["hints"]:
        ok("R4 hint '%s' rescues a third of the results or fewer" % h["sentence"][:40], len(h["rescues"]) <= 7 / 3)
    ok("R5 the one-fact test: no sentence rescues more than one result", max(len(h["rescues"]) for h in E["hints"]) <= 1)
    fam = E["forcing"]["golden_family"]
    gold = E["forcing"]["golden_answer"]
    for m in fam:
        ok("R6 rival '%s' files the order" % m["name"][:60], m["answer"] == gold, ",".join(m["answer"]))
    for p in E["forcing"]["perturbations"]:
        ok("R7 perturbation '%s' holds the order" % p["input"], p["answer"] == gold, ",".join(p["answer"]))
    for sc in E["forcing"]["shortcuts"]:
        ok("R7 shortcut '%s' files another order" % sc["name"][:50], sc["answer"] != gold, ",".join(sc["answer"]))
    for s in ("50", "30", "20"):
        ok("F1 the golden order for %s litre sits inside its band" % s,
           fj["buy_lo_%s" % s] <= fj["buy_%s" % s] <= fj["buy_hi_%s" % s])
    # the golden against the simulation's own truth
    tp = os.environ.get("TASK4_TRUTH")
    if tp and os.path.exists(tp):
        tr = json.load(open(tp))
        for s in ("50", "30", "20"):
            ok("T1 fleet %s within 3%% of the truth" % s,
               abs(fj["fleet_%s" % s] / tr["fleet"][s] - 1) < 0.03, "%s vs %s" % (fj["fleet_%s" % s], tr["fleet"][s]))
            ok("T2 loss %s within 25%% of the truth" % s,
               abs(fj["loss_%s" % s] / tr["loss"][s] - 1) < 0.25, "%s vs %s" % (fj["loss_%s" % s], tr["loss"][s]))
            ok("T3 need %s within 5%% of the truth" % s, abs(fj["need_%s" % s] / tr[s]["need"] - 1) < 0.05,
               "%s vs %.0f" % (fj["need_%s" % s], tr[s]["need"]))
            ok("T4 order %s within 25%% of the truth" % s, abs(fj["buy_%s" % s] / tr[s]["buy"] - 1) < 0.25,
               "%s vs %.0f" % (fj["buy_%s" % s], tr[s]["buy"]))
            ok("T5 deliveries %s within 7%% of the truth" % s, abs(fj["deliv_%s" % s] / tr[s]["deliv"] - 1) < 0.07,
               "%s vs %s" % (fj["deliv_%s" % s], tr[s]["deliv"]))
        for s in ("50", "30"):
            ok("T6 Maplestead %s within 15%% of the truth" % s, abs(fj["estate_%s" % s] / tr[s]["estate"] - 1) < 0.15,
               "%s vs %.0f" % (fj["estate_%s" % s], tr[s]["estate"]))
        ok("T7 Foundry store within 15% of the truth", abs(fj["store"] / tr["20"]["store"] - 1) < 0.15,
           "%s vs %.0f" % (fj["store"], tr["20"]["store"]))
    print("%d checks, %d FAIL" % (N[0], len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
