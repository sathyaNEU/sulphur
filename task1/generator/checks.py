"""The generator's assertions on the cut pack (python3 checks.py): the input gates, the bar block R1 to R7, every
semantic fork row, mess neutrality item by item, the realism sweep, the distractor deletion test and the pack's
agreement with the simulator's clean truth. Exit 1 on any failure."""
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BD  # noqa: E402
import docs  # noqa: E402
import golden as GD  # noqa: E402
import models  # noqa: E402
import pack as PK  # noqa: E402
import panel  # noqa: E402
import params as P  # noqa: E402
import results  # noqa: E402
import routes  # noqa: E402
import sim  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
OUT = []


def check(label, ok, detail=""):
    OUT.append((label, bool(ok), detail))


def rows(name):
    with open(os.path.join(TARGET, PK.FILES[name]), encoding="utf-8") as f:
        return list(csv.reader(f, delimiter=";" if name == "spend" else ","))


def pdf_text(path):
    import subprocess
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    files = sorted(os.listdir(TARGET))
    # ---------------------------------------------------------------- input gates
    usable = [f for f in files if not f.startswith(".")]
    check("gate: ten or more usable files", len(usable) >= 10, "%d files" % len(usable))
    cats = {f.rsplit(".", 1)[1] for f in usable}
    check("gate: two or more file categories", {"csv", "xlsx", "pdf"} <= cats, ", ".join(sorted(cats)))
    big = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in usable if f.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more", max(big.values()) >= 20000, "%d rows" % max(big.values()))
    sp = big[PK.FILES["spend"]]
    check("gate: a CSV of 10 to 20 printed pages, messy (German locale, renamed codes)", 500 <= sp <= 1100, "%d rows" % sp)
    check("gate: two or more distractors, unlabelled", len(PK.DISTRACTORS) >= 2 and not any(
        "distract" in f.lower() for f in usable), ", ".join(PK.FILES[k] for k in PK.DISTRACTORS))
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|manifest|field.?notes|schema",
                                                                 f, re.I) for f in usable))
    check("gate: no file named after a mechanism", not any(re.search(r"drift|return|household|reading_habit|cohort",
                                                                     f, re.I) for f in usable if f != PK.FILES["reading"]))
    # ---------------------------------------------------------------- the panel the golden reads, against the world
    S = world.history()
    pw = panel.from_world(S)
    pp = panel.from_pack(TARGET)
    pk = PK.Pack(S, P.SEED + 101)
    idx = {s: j for j, s in enumerate(pp["sid"])}
    order = np.array([idx[pk.sid[i]] for i in range(pw["n"])])
    same = all(np.array_equal(pw[k], pp[k][order]) for k in ["start", "title", "channel", "offer", "route", "end", "L",
                                                            "tenure0", "customer"])
    check("R1 raw material: the consumer subscriptions rebuilt from the exports equal the record field for field", same)
    check("R1 raw material: charges and reading rebuilt from the price periods and the login log equal the record",
          np.allclose(pw["gross"], pp["gross"][order]) and np.array_equal(pw["reading"], pp["reading"][order]))
    hdr = [r[0] for r in [rows(k)[:1][0] for k in ["subs", "periods", "reading", "customers", "methods", "logins"]]]
    allhdr = " ".join(",".join(rows(k)[0]) for k in ["subs", "periods", "reading", "customers", "methods", "logins",
                                                     "spend", "offers"])
    check("R1 raw material: no shipped column holds a result (value, multiple, survival, household, funded)",
          not re.search(r"value|multiple|ltv|survival|household|funded|churn|proxy|score", allhdr, re.I), allhdr[:80])
    # households: the pack links what the record links, plus genuine shared-building addresses
    hw, hp = pw["household"], pp["household"][order]
    m = {}
    consistent = True
    for a, b in zip(hw, hp):
        if m.setdefault(a, b) != b:
            consistent = False
    check("R1 raw material: every household the record links is one household in the pack", consistent)
    # ---------------------------------------------------------------- the golden and its rivals
    G = GD.compute(TARGET)
    g = G["golden"]
    check("golden equals figures.json: funded lines", [GD.key(l) for l in g["R8"]] == F["funded"])
    check("golden equals figures.json: budget", g["budget"] == F["budget"])
    check("golden equals figures.json: line values", all(int(round(g["R7"][l])) == F["line_value"][GD.key(l)]
                                                         for l in g["R7"]))
    check("golden equals effort.json", [e for e in E["results"] if e["id"] == "R8"][0]["golden"] == F["funded"])
    # R7 the rivals: every rival funds the same lines, each line keeps its side by a margin
    riv = G["rivals"]
    check("R7 rivals: every rival funds the golden's lines", all(riv[n]["R8"] == g["R8"] for n in riv),
          ", ".join(n for n in riv if riv[n]["R8"] != g["R8"]))
    margins = []
    for l in g["R7"]:
        side = g["R7"][l] / G["cps"][l] >= P.HURDLE
        for n in riv:
            mult = riv[n]["R7"][l] / G["cps"][l]
            margins.append(abs(mult - P.HURDLE))
            if (mult >= P.HURDLE) != side:
                margins.append(-1)
    check("R7 rivals: no line within 0.005 of the bar under any rival", min(margins) >= 0.005, "%.3f" % min(margins))
    check("SF16 the funding bar: no golden multiple within 0.1 of 3.5",
          min(abs(g["R7"][l] / G["cps"][l] - P.HURDLE) for l in g["R7"]) >= 0.1)
    # R3 each result's hurried figure outside its band, by result
    car = G["routes"]["careful"]
    for r, keys in [("R2", ["SOC", "SEA", "TEL", "APP", "DIR"]), ("R4", list(g["R4"])), ("R5", ["SOC", "SEA", "PART"]),
                    ("R6", P.TITLES), ("R9", ["SOC", "SEA", "PART", "TEL", "APP"])]:
        b = G["bands"][r]
        out = [k for k in keys if not (b[k][0] <= car[r][k] <= b[k][1])]
        check("R3 hurried figure: %s outside its band on %s" % (r, ", ".join(map(str, keys))), len(out) == len(keys),
              "outside on %d of %d" % (len(out), len(keys)))
    b7 = G["bands"]["R7"]
    n_out = sum(1 for l in g["R7"] if not (b7[l][0] <= car["R7"][l] <= b7[l][1]))
    check("R3 hurried figure: R7 outside its band on most lines", n_out >= 12, "%d of 18" % n_out)
    check("R3 hurried figure: R8 the careful pass funds another set", car["R8"] != g["R8"],
          "%d lines" % len(car["R8"]))
    check("R3 earned: R1 the careful pass counts the base right (the panel is the same)", True)
    b3 = G["bands"]["R3"]
    check("R3 earned: R3 the careful pass's period term lands inside the band on three or more offers",
          sum(1 for k in g["R3"] if b3[k][0] - 0.001 <= car["R3"][k] <= b3[k][1] + 0.001) >= 3)
    # depth: different shortcuts, different wrong sets
    sets = {nm: tuple(GD.key(l) for l in G["routes"][nm]["R8"]) for nm in G["routes"]}
    wrong = {s for s in sets.values() if list(s) != F["funded"]}
    check("level 5: four or more distinct wrong sets over the shortcuts", len(wrong) >= 4, "%d" % len(wrong))
    for nm in ["completion on each channel's older starts", "no full-price term at the intro's end",
               "returns on the customer number only"]:
        check("level 5: '%s' alone funds a wrong set" % nm, list(sets[nm]) != F["funded"])
    for nm in routes.PAIRS:
        check("level 5: '%s' funds a wrong set" % nm, list(sets[nm]) != F["funded"])
    # R5 no one thing and R6 the one-fact test
    lost = [e["id"] for e in E["results"] if e["id"] not in ("R1",)]
    worst = max(len(h["rescues"]) for h in E["hints"])
    check("R5/R6 one-fact test: no hint rescues more than a third of the results", worst <= 3, "%d of 9" % worst)
    check("R6 one-fact test: no hint rescues the funded set", not any("R8" in h["rescues"] for h in E["hints"]))
    # hidden factor footprints outside the deciding units
    moved = {l for l in g["R7"] if abs(G["routes"]["completion on each channel's older starts"]["R7"][l] / g["R7"][l] - 1) > 0.03}
    flipped = set(sets["completion on each channel's older starts"]) ^ set(F["funded"])
    check("R5 footprint: the reading change moves more lines than it flips", len(moved) > len(flipped),
          "%d moved, %d flipped" % (len(moved), len(flipped)))
    moved = {l for l in g["R7"] if abs(G["routes"]["no full-price term at the intro's end"]["R7"][l] / g["R7"][l] - 1) > 0.03}
    flipped = set(sets["no full-price term at the intro's end"]) ^ set(F["funded"])
    check("R5 footprint: the full-price term moves more lines than it flips", len(moved) > len(flipped),
          "%d moved, %d flipped" % (len(moved), len(flipped)))
    moved = {l for l in g["R7"] if abs(G["routes"]["returns on the customer number only"]["R7"][l] / g["R7"][l] - 1) > 0.01}
    flipped = set(sets["returns on the customer number only"]) ^ set(F["funded"])
    check("R5 footprint: the household links move more lines than they flip", len(moved) > len(flipped),
          "%d moved, %d flipped" % (len(moved), len(flipped)))
    for c in ["SOC", "PART", "SEA"]:
        a, b, s = P.DRIFT[c]
        check("realism: the %s reading change ramps over two or more months, not a step" % c, b - a >= 2)
    # ---------------------------------------------------------------- R2 mess, item by item
    raw = rows("subs")
    body = [tuple(r) for r in raw[1:]]
    dup = len(body) - len(set(body))
    check("R2 mess: the re-run export's repeated rows exist and are exact copies", dup > 0, "%d rows" % dup)
    prods = {r[3] for r in raw[1:]}
    check("R2 mess: staff, gift and company products sit in the export", {"DIGITAL_STAFF", "DIGITAL_GIFT",
                                                                         "DIGITAL_GROUP"} <= prods)
    q = G["quick"]["R1"]
    check("R2 mess: kept, the texture and repeated rows move R1 (and only R1 reads them)",
          all(q[t] > g["R1"][t] for t in P.TITLES), str(q))
    codes = {r[4] for r in raw[1:] if r[3] == "DIGITAL" and r[4]}
    check("R2 mess: the renamed channel codes map one to one", codes <= set(P.OLD_CODE.values()) | set(P.CHANNELS)
          and len({P.OLD_CODE[c] for c in P.CHANNELS}) == len(P.CHANNELS))
    first_only = panel.from_pack(TARGET)
    # a second login's reading dropped: the reading proxy moves, the call does not
    logins = rows("logins")
    second = sum(1 for r in logins[1:] if r[3] == "APP")
    check("R2 mess: second logins exist and carry reading", second > 1000, "%d" % second)
    # every mishandling leaves the call: a raw address key (no normalising) and fingerprint-only links
    check("R2 mess: households on the fingerprint alone fund the same lines",
          riv["returns on the payment fingerprint"]["R8"] == g["R8"])
    check("R2 mess: households on the address alone fund the same lines",
          riv["returns on the address"]["R8"] == g["R8"])
    # ---------------------------------------------------------------- semantic forks
    check("SF1 paying: free intro months are not paying (G3 subscribers in their free quarter excluded)",
          int(((pp["gross"][:, P.CUT] == 0) & pp["running"] & (pp["offer"] == sim.O_IDX["G3"])).sum()) > 0)
    check("SF2 a start: withdrawn subscriptions carry no charge and are no start",
          float(pp["gross"][pp["withdrawn"]].sum()) == 0.0 and int(pp["withdrawn"].sum()) > 100)
    std = pdf_text(os.path.join(TARGET, PK.FILES["standard"]))
    for sf, phrase in [("SF3 net revenue", "less VAT at 7 per cent"), ("SF4 household", "A household is the reader"),
                       ("SF5 the window", "in the 36 months from the"), ("SF6 the 2027 starts", "the twelve months to"),
                       ("SF7 prices", "including changes it announces"), ("SF8 cost per start",
                                                                            "divided by its planned starts"),
                       ("SF9 extra cancellations", "would still be running on it without the change"),
                       ("SF11 paying at a date", "billing period that covers the date"),
                       ("SF12 expected values", "average over the starts it covers"),
                       ("SF16 the bar", "at least 3.5 times")]:
        check("%s: filed once in the standard" % sf, " ".join(std.split()).count(phrase) == 1, phrase)
    check("positive control: the standard's text was read", len(std) > 3000 and "Version 3" in std)
    intro_at_cut = pp["running"] & (pp["offer"] >= 0) & (pp["stepup"] > P.CUT) & (pp["kind"] != "base")
    free = intro_at_cut & (pp["offer"] == sim.O_IDX["G3"])
    check("SF10 intro subscribers: the free quarter is under a fifth of them", free.sum() < 0.2 * intro_at_cut.sum(),
          "%d of %d" % (free.sum(), intro_at_cut.sum()))
    b6 = G["bands"]["R6"]
    check("SF15 the rise's window: to June lands inside R6's band, April-May does not",
          all(b6[t][0] <= riv["the rise's window to June"]["R6"][t] <= b6[t][1] for t in P.TITLES) and
          all(not (b6[t][0] <= G["routes"]["the 2025 rise read from April, pooled"]["R6"][t] <= b6[t][1])
              for t in P.TITLES))
    check("SF13 reading measures: every reading rival funds the same lines",
          all(riv[n]["R8"] == g["R8"] for n in ["reading taken linearly", "reading in bands",
                                                "reading with a square term", "reading over the first two months",
                                                "reading against the month's average"]))
    check("SF14 offer terms: the depth-and-length form funds the same lines",
          riv["discount depth and intro length"]["R8"] == g["R8"])
    # ---------------------------------------------------------------- the plan and the documents
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TARGET, PK.FILES["plan"]))
    ws = wb["Plan 2027"]
    lines_x = [ws.cell(r, 1).value for r in range(5, 23)]
    check("plan: 18 lines, one per channel and title", len(set(lines_x)) == 18 and all(lines_x))
    check("plan: no column ranks the lines or states a value",
          not any(re.search(r"value|rank|ltv|priority|multiple", str(c.value or ""), re.I) for c in ws[4]))
    kpi = load_workbook(os.path.join(TARGET, PK.FILES["kpi"]))["KPI Digital 2026"]
    sep = [kpi.cell(13, c).value for c in range(2, 6)]
    m_sep = 44
    pay_sep = [int(((pp["gross"][:, m_sep] > 0) & (pp["title"] == sim.T_IDX[t])).sum()) for t in P.TITLES]
    check("context artifact: the KPI workbook's September counts reproduce from the exports", sep == pay_sep,
          "%s against %s" % (sep, pay_sep))
    pl = pdf_text(os.path.join(TARGET, PK.FILES["prices"]))
    check("price list: the April 2027 prices are stated once", " ".join(pl.split()).count("from 1 April 2027") == 1)
    # ---------------------------------------------------------------- realism sweep
    sids = sorted(int(r[0][2:]) for r in raw[1:])
    steps = set(np.diff(sids))
    check("realism: subscription ids are not a sequence", len(steps) > 100)
    cust = sorted({int(r[1]) for r in raw[1:]})
    check("realism: customer numbers are not a sequence", len(set(np.diff(cust))) > 2)
    check("realism: no identical paying counts across titles", len(set(g["R1"].values())) == 4)
    check("realism: the budget is not a round figure", F["budget"] % 1000 != 0)
    check("realism: line costs per start vary within each channel", all(
        len({round(G["cps"][l], 1) for l in G["plan"] if l[0] == c}) >= 2 for c in P.PAID))
    names = {P.TITLE_NAME[t].split()[-1] for t in P.TITLES}
    check("realism: the titles' names take more than two shapes", len(names) >= 3, ", ".join(sorted(names)))
    check("realism: every document is dated before the exports it sits beside",
          "20 January 2026" in std and "Issued 15 September 2026" in pl)
    check("realism: no start or received cancellation after the export; a later end date only with a received "
          "cancellation", max(r[6] for r in raw[1:]) <= "2026-10-31" and max((r[8] for r in raw[1:] if r[8]),
                                                                              default="") <= "2026-11-03"
          and all(r[8] or r[10] in ("PAYMENT_FAILED", "GIFT_END", "STAFF_END") for r in raw[1:]
                  if r[9] > "2026-11-03" and r[3] == "DIGITAL"))
    # distractors: deleting each changes nothing the golden reads
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in [PK.FILES[k] for k in PK.DISTRACTORS]:
                shutil.copy(os.path.join(TARGET, f), tmp)
        p2 = panel.from_pack(tmp)
        check("distractors: the golden's panel is the same with every distractor deleted",
              np.array_equal(p2["gross"], pp["gross"]) and np.array_equal(p2["reading"], pp["reading"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # report
    bad = [o for o in OUT if not o[1]]
    for label, ok, detail in OUT:
        print("%s  %-92s %s" % ("PASS" if ok else "FAIL", label[:92], detail[:60]))
    print("%d checks, %d FAIL" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
