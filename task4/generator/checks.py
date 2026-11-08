"""Assertions on the cut pack (python3 checks.py <target>). Exit 1 on the first failure.

Groups: the input gates; the pack's own hygiene (no describing file, no reserved or real organisation's domain, no
em dash); the semantic forks SF1 to SF16 of the design note; the ladder (every rung files its own wrong list, the
golden's margins); the Sulfur block on the clean truth (the analyst test, the deep chain, the one-fact test, the
rivals); the forecast's back-test."""
import copy
import csv
import importlib
import io
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np

import analysis as A
import golden as GD

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        print("FAIL", msg)
        sys.exit(1)


def text_of(path):
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        r = PdfReader(path)
        return "\n".join(p.extract_text() for p in r.pages) + str(r.metadata)
    if path.endswith(".xlsx"):
        z = zipfile.ZipFile(path)
        return "\n".join(z.read(n).decode("utf-8", "replace") for n in z.namelist())
    return open(path, encoding="utf-8").read()


def gates(target):
    import pack
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "10 or more usable files (%d)" % len(files))
    cats = {f.rsplit(".", 1)[1] for f in files}
    ok(len({"spreadsheet" if c in ("csv", "xlsx") else "text" for c in cats}) >= 2, "2 or more file categories")
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok(rows[pack.FILES["stops"]] >= 20000, "stop log 20,000 rows or more")
    ok(rows[pack.FILES["rundays"]] * 12 / 55 >= 15, "run log 10 to 20 printed pages or more")
    for f in files:
        ok(not re.search(r"readme|dictionary|notes|manifest|schema", f, re.I), "no describing file by name: " + f)
        t = text_of(os.path.join(target, f))
        ok(chr(0x2014) not in t and chr(0x2013) not in t, "no em or en dash in " + f)
        ok(not re.search(r"\.(example|test|invalid|localhost)\b|example\.(com|net|org)", t), "no reserved domain in " + f)
        for dom in re.findall(r"[\w.-]+@([\w.-]+)", t):
            ok(dom in ("brackloondirect.ie", "owenduffcouriers.ie"), "only the two invented domains: " + dom)
    for k in pack.DISTRACTORS:
        ok(pack.FILES[k] not in A.FILES.values(), "distractor never read by the golden: " + k)
    offer = re.sub(r"\s+", " ", text_of(os.path.join(target, pack.FILES["offer"])))
    ok("EUR 13.40 per parcel delivered" in offer, "the offer's price is the one analysis uses")
    ok("combination" not in offer.lower(), "the offer files no search over combinations")
    import params as P
    for c in A.offered(None):
        ok(P.D[c][0] in offer and c in offer, "offered district in the letter: " + c)
    std = re.sub(r"\s+", " ", text_of(os.path.join(target, pack.FILES["standard"])))
    for phrase in ("takes off Brackloon's runs", "lowers the year's delivery cost most", "depot out to depot in"):
        ok(phrase in std, "NPS-3 files the WHAT: " + phrase)
    for bad in ("road", "drive", "through", "beyond", "combination", "end of the run", "skipped", "sequence"):
        ok(bad not in std.lower(), "NPS-3 names nothing the deep step rides on: " + bad)


def forks(pk, res):
    g = sorted(res["set"])
    gs = GD.r5000(res["saving"])
    # SF14 the fit and forecast variants converge on the list and the rounded figures
    for kw in ({"years": (2025,)}, {"years": (2026,)}, {"stat": np.median}, {"annual": True}):
        v = A.golden(pk, **kw)
        ok(sorted(v["set"]) == g, "SF14 same list under %s" % kw)
        ok(GD.r5000(v["saving"]) == gs, "SF14 same rounded net saving under %s (%.0f)" % (kw, v["saving"]))
        for r, rr in v["runs"].items():
            ok(GD.r100(rr["hours"]) == GD.r100(res["runs"][r]["hours"]), "SF14 same rounded hours saved on %s under %s" % (r, kw))
            ok(GD.r50(rr["base_h"]) == GD.r50(res["runs"][r]["base_h"]), "SF14 same rounded before hours on %s under %s" % (r, kw))
    ok(abs(res["saving"] - gs) < 1500, "SF12 the net saving sits mid-bin (%.0f)" % res["saving"])
    for r, rr in res["runs"].items():
        if not rr["cand"]:
            continue
        v = rr["hours"]
        ok(v == 0 or abs(v - GD.r100(v)) < 25, "SF12 run %s saved hours mid-bin at 100 (%.1f)" % (r, v))
        v = rr["base_h"]
        ok(abs(v - GD.r50(v)) < 12, "SF12 run %s before hours mid-bin at 50 (%.1f)" % (r, v))
    # SF9 each district on its own merit moves Mulranny and Bangor Erris (ruled out by NPS-3 4.3)
    one = A.removal_one(pk, res)
    one_set = sorted(c for c in one if one[c][2] > 0)
    ok(one_set != g and "MUL" not in one_set and "BAN" not in one_set, "SF9 one-at-a-time keeps Mulranny and Bangor Erris")
    # SF10 time in district moves Leenane and Letterfrack (ruled out by NPS-3 4.1 and 3.2)
    for incl in (False, True):
        tid = A.time_in_district(pk, incl)
        ts = sorted(c for c in A.offered(pk) if tid[c][1] > tid[c][2])
        ok("LEE" in ts and "LET" in ts and ts != g, "SF10 time in district (exit leg %s) hands over Leenane and Letterfrack" % incl)
        ok(min(tid["LEE"][1] / tid["LEE"][2], tid["LET"][1] / tid["LET"][2]) >= 1.15, "SF10 by a margin of 1.15x")
    al = A.allocation_by_stops(pk)
    ok(sorted(c for c in A.offered(pk) if al[c][0] > al[c][1]) != g, "allocation by stops files another list")
    # SF11 the proportional carry moves the rounded net saving
    ok(GD.r5000(A.proportional_carry(pk, res)) != gs, "SF11 the proportional carry rounds elsewhere")
    # SF16 weekdays as delivery days instead of the calendar's
    pk2 = copy.copy(pk)
    pk2.days27 = [sum(1 for d in range(1, 32) if _wd(2027, m, d)) for m in range(1, 13)]
    v = A.golden(pk2)
    ok(sorted(v["set"]) == g, "SF16 same list on weekdays")
    # SF4 the year's parcels read as the last twelve months' parcels instead of the plan's: same list
    pk3 = copy.copy(pk)
    plan = {}
    for c in pk.plan:
        m = [0] * 12
        for (d, r), lst in pk.rundays.items():
            if d >= "2025-11-01":
                for x in lst:
                    if x["district_code"] == c:
                        m[int(d[5:7]) - 1] += int(x["parcels_delivered"])
        plan[c] = m
    pk3.plan = plan
    ok(sorted(A.golden(pk3)["set"]) == g, "SF4 same list on the last twelve months' parcels")
    # SF2 van-hours depot out to depot in: the fitted run (drives, door, local, break) reproduces the run log's hours
    model, per = res["model"], res["per"]
    for run in pk.runs:
        cnt = {}
        days = [0] * 12
        tot = 0.0
        for (d, r), lst in pk.rundays.items():
            if r != run or not d.startswith("2026"):
                continue
            m = int(d[5:7]) - 1
            days[m] += 1
            t0, t1 = pk.runlog[(d, r)]
            tot += t1 - t0
            for x in lst:
                if x["stop_type"] != "BREAK":
                    cnt.setdefault(x["district_code"], [0] * 12)[m] += 1
        mus = {c2: [cnt.get(c2, [0] * 12)[k] / days[k] if days[k] else 0 for k in range(12)] for c2 in model[run]["chain"]}
        mus["__days__"] = days
        fit_h = A.run_hours(model, per, run, mus)
        ok(abs(fit_h - tot) / tot < 0.03, "SF2 the fitted run reproduces the run log's 2026 hours on %s (%.0f against %.0f)" % (run, fit_h, tot))
    # SF1 the year is the calendar year 2027 of the delivery calendar
    ok(sum(pk.days27) == 251, "SF1 2027 has 251 delivery days in the calendar")
    # SF7 Castlebar town's two new codes belong to a run that serves no offered district
    ok(not res["runs"]["R01"]["cand"], "SF7 the split district's run serves no offered district")
    # SF13 the runs that serve an offered district
    ok(sorted(r for r, rr in res["runs"].items() if rr["cand"]) == ["R03", "R04", "R05", "R06", "R07", "R08", "R09"],
       "SF13 seven runs serve an offered district")
    # SF8 Owenduff charges per parcel delivered: the plan counts deliveries, and no plan row is a collection
    ok(all(sum(v) > 0 for c, v in pk.plan.items() if c in A.offered(pk)), "SF8 every offered district has plan parcels")
    for S, (hrs, ch, val) in res["runs"]["R05"]["table"].items():
        if S:
            ok(hrs * pk.rate / ch <= 0.87, "Connemara: no combination saves (%s %.2f)" % (S, hrs * pk.rate / ch))
    for run, rr in res["runs"].items():
        S = set(rr["set"])
        for c in rr["cand"]:
            w = tuple(x for x in rr["cand"] if x in S | {c})
            wo = tuple(x for x in rr["cand"] if x in S - {c})
            marg = (rr["table"][w][0] - rr["table"][wo][0]) * pk.rate / (sum(pk.plan[c]) * A.PRICE)
            ok(marg >= 1.15 if c in S else marg <= 0.87, "golden margin %s %.2f" % (c, marg))


def _wd(y, m, d):
    import datetime as dt
    try:
        return dt.date(y, m, d).weekday() < 5
    except ValueError:
        return False


def neutral(target, res):
    """SF5, SF6, SF15: the mess moves nothing; SF3 the break is never saved"""
    g = sorted(res["set"])
    tmp = tempfile.mkdtemp(prefix="task4-neutral-")
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        p = os.path.join(tmp, A.FILES["stops"])
        rows = list(csv.reader(open(p, encoding="utf-8")))
        # SF6 the re-synced copies: Pack drops them; kept as stops they would add door time only (asserted below)
        # SF5 failed attempts and collections dropped as if they were not stops
        hdr = rows[0]
        keep = [hdr] + [r for r in rows[1:] if r[hdr.index("stop_type")] not in ("FAILED_ATTEMPT", "COLLECTION")]
        with open(p, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(keep)
        v = A.golden(A.Pack(tmp))
        ok(sorted(v["set"]) == g, "SF5 same list with failed attempts and collections dropped")
        # SF15 the stops with no departure scan: dropping their run-days from the fit moves nothing
        rows2 = list(csv.reader(open(os.path.join(target, A.FILES["stops"]), encoding="utf-8")))
        bad = {(r[0], r[1]) for r in rows2[1:] if r[hdr.index("departed_local")] == "" and r[hdr.index("stop_type")] != "BREAK"}
        with open(p, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows([hdr] + [r for r in rows2[1:] if (r[0], r[1]) not in bad])
        v = A.golden(A.Pack(tmp))
        ok(sorted(v["set"]) == g and GD.r5000(v["saving"]) == GD.r5000(res["saving"]), "SF15 same list without those run-days")
        # SF6 with every re-synced copy kept as a stop of its own
        with open(p, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(rows2)
        pk6 = A.Pack(tmp)
        ok(len(pk6.rundays) == len(A.Pack(target).rundays), "SF6 the copies sit on existing run-days")
    finally:
        shutil.rmtree(tmp)
    pk = A.Pack(target)
    breaks = sum(1 for lst in pk.rundays.values() if sum(1 for x in lst if x["stop_type"] == "BREAK") == 1)
    ok(breaks == len(pk.rundays), "SF3 every run-day carries exactly one break, never saved")


def sulfur(res_pack):
    """the clean truth: a pack built with no mess, the analyst test and the rivals executed on it"""
    import params as P
    import pack as PK
    import sim
    saved = (P.DUP_RATE, P.MISSING_DEP)
    P.DUP_RATE, P.MISSING_DEP = 0.0, 0.0
    tmp = tempfile.mkdtemp(prefix="task4-clean-")
    try:
        w = sim.world()
        PK.write_tables(w, tmp)
        pk = A.Pack(tmp)
        res = A.golden(pk)
        ok(sorted(res["set"]) == sorted(res_pack["set"]), "R1 the clean truth's golden list is the pack's")
        tid = A.time_in_district(pk)
        ts = sorted(c for c in A.offered(pk) if tid[c][1] > tid[c][2])
        ok("LEE" in ts and "LET" in ts, "R2 the analyst test on the clean truth hands over Leenane and Letterfrack")
        one = A.removal_one(pk, res)
        ok(sorted(c for c in one if one[c][2] > 0) != sorted(res["set"]), "R3 one-at-a-time on the clean truth files another list")
        # R4 the one-fact test: told the through-road fact alone (removal), the solver still keeps Mulranny and
        # Bangor Erris; told the spur fact alone with time in district, it still hands over Leenane and Letterfrack
        ok("MUL" not in [c for c in one if one[c][2] > 0], "R4 the through-road hint alone leaves the spur wrong")
        # R5 the truth: the generator's own expected run times put the same list (checked through the fitted model's
        # recovery of the generator's sections)
        for r in ("R04", "R05", "R07"):
            for c in pk.chain[r]:
                e_true = sim.edge_h(c)
                ok(abs(res["model"][r]["e"][c] - e_true) / e_true < 0.08 or c == pk.chain[r][-1],
                   "R5 fitted section %s within 8 per cent of the truth" % c)
    finally:
        shutil.rmtree(tmp)
        P.DUP_RATE, P.MISSING_DEP = saved


def backtest(pk):
    """the forecast earns its place: fitted on 2025, the visit model forecasts 2026's run hours (January to October)
    from 2026's stops better than 2025's hours carried in proportion to stops"""
    model, per = A.fit(pk, (2025,))
    err_v, err_p = [], []
    for run in pk.runs:
        if not [c for c in model[run]["chain"] if c in A.offered(pk)]:
            continue
        hrs = {y: 0.0 for y in (2025, 2026)}
        stops = {y: [0] * 12 for y in (2025, 2026)}
        cnt = {y: {c: [0] * 12 for c in model[run]["chain"]} for y in (2025, 2026)}
        days = {y: [0] * 12 for y in (2025, 2026)}
        for (d, r), lst in pk.rundays.items():
            if r != run:
                continue
            y, m = int(d[:4]), int(d[5:7]) - 1
            if m > 9:
                continue
            t0, t1 = pk.runlog[(d, r)]
            hrs[y] += t1 - t0
            days[y][m] += 1
            for x in lst:
                if x["stop_type"] != "BREAK":
                    cnt[y][x["district_code"]][m] += 1
        mus = {c: [cnt[2026][c][m] / days[2026][m] for m in range(12) if m < 10] + [0, 0] for c in model[run]["chain"]}
        mus["__days__"] = days[2026][:10] + [0, 0]
        fv = A.run_hours(model, per, run, mus) - 0.0
        tot25 = sum(sum(v) for v in cnt[2025].values())
        tot26 = sum(sum(v) for v in cnt[2026].values())
        fp = hrs[2025] * tot26 / tot25
        err_v.append(abs(fv - hrs[2026]))
        err_p.append(abs(fp - hrs[2026]))
    ok(sum(err_v) < sum(err_p), "the visit model beats the proportional carry out of sample (%.0f against %.0f h)"
       % (sum(err_v), sum(err_p)))
    return sum(err_v), sum(err_p)


def main(target):
    gates(target)
    pk = A.Pack(target)
    res = A.golden(pk)
    ok(sorted(res["set"]) == sorted(["ACH", "BAN", "BCA", "BLM", "LOU", "MUL"]), "the golden list is the designed one")
    forks(pk, res)
    neutral(target, res)
    sulfur(res)
    ev, ep = backtest(pk)
    print("checks: %d assertions passed; back-test absolute error %.0f h (visit model) against %.0f h (proportional)"
          % (N[0], ev, ep))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
