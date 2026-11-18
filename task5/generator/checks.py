"""Every assertion of the build on the cut pack: the input gates, the never-filed list, the bar block (R1 to R7), every
row of the fork table (SF1 to SF25), the pinning list, the pack against the core's arrays, the second implementation,
the goldens against figures.json and the realism sweep.

    python3 task5/generator/checks.py [target]
"""
import csv
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import analysis as A  # noqa: E402
import deliver  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import results as RS  # noqa: E402
import verify as V  # noqa: E402

ROWS = []
HOSTS, HOME = C.HOSTS, C.HOME
NEVER = (r"under-?regist|over-?regist|under-?count|over-?count|under-?report|coverage|completeness|incomplete|mirror|"
         r"double[- ]entry|reference (country|state)|correction factor|adjustment factor|adjusted for|error of closure|"
         r"intercensal|residual|fail(s|ed)? to deregister|do not deregister|not deregister|survey|consular regist|"
         r"voters abroad|passports? issued|diaspora|quality report|misses|missed|does not record|not recorded")


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), str(detail)))
    return bool(cond)


def texts(target):
    """every word a reader can find in the pack: file names, headers, workbook cells, the PDFs' text"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                out[name] = " ".join(next(csv.reader(fh)))
            if os.path.getsize(path) < 400000:
                out[name] += " " + open(path).read()
        elif name.endswith(".xlsx"):
            wb = load_workbook(path, read_only=True, data_only=True)
            out[name] = " ".join(wb.sheetnames) + " " + " ".join(
                str(c) for ws in wb for r in ws.iter_rows(values_only=True) for c in r if c is not None)
        elif name.endswith(".pdf"):
            out[name] = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)
    return out


def inside(v, band):
    return band[0] - 1e-9 <= v <= band[1] + 1e-9


def graded(R, o, fig, year_of=None):
    """the fourteen ask figures and the three components under one reading; the list of those outside their bands"""
    out = []
    for h in HOSTS:
        g = C.chain(R, h, o)
        if not inside(round(g["n"]), fig["citizens_band"][h]):
            out.append("N %s %.0f" % (h, g["n"]))
        if not inside(round(g["left"]), fig["left_band"][h]):
            out.append("L %s %.0f" % (h, g["left"]))
    c1 = 100.0 * C.b_home(R, o)
    c2 = 100.0 * R["host"]["Skarholm"]["dep"][:10].sum() / C.chain(R, "Skarholm", o)["ex_p"]
    c3 = C.chain(R, "Tesmar", o)["late"]
    for k, v, nd in (("c1", c1, 1), ("c2", c2, 1), ("c3", c3, 2)):
        if not inside(round(v, nd), fig[k + "_band"]):
            out.append("%s %.3f" % (k, v))
    return out, RS.call_of({h: C.chain(R, h, o)["n"] for h in HOSTS})


def main(target):
    files = sorted(os.listdir(target))
    T = texts(target)
    world = C.simulate()
    RW = C.records(world)
    R, fig, E, spec = RS.run(target)
    F = dict(pack.FILES)
    F.update(docs.FILES)
    # ------------------------------------------------------------------------------------------- the input gates
    kinds = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))], "text": [f for f in files if f.endswith(".pdf")]}
    ok("gate: ten or more usable files", len(files) >= 10 and all(os.path.getsize(os.path.join(target, f)) > 200 for f in files), "%d files" % len(files))
    ok("gate: two or more file categories", all(kinds.values()), {k: len(v) for k, v in kinds.items()})
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", rows[F["register"]] >= 20000, "%d rows" % rows[F["register"]])
    ok("gate: a second large CSV of ten printed pages or more", rows[F["tables"]] >= 600, "%d rows" % rows[F["tables"]])
    ok("gate: both large files carry mess to clean", fig["counts"]["register_repeats"] > 500 and fig["counts"]["blank_codes"] > 5000
       and fig["counts"]["table_rows_superseded"] > 500)
    size = sum(os.path.getsize(os.path.join(target, f)) for f in files)
    ok("gate: the pack is 30 MB or more", size >= 30e6, "%.1f MB" % (size / 1e6))
    unused = [F["pop"], F["traffic"]]
    src = open(os.path.join(HERE, "analysis.py")).read() + open(os.path.join(HERE, "verify.py")).read()
    ok("gate: two distractors ship, unused and unlabelled", all(f in files for f in unused) and
       not any(re.search(r"distract|unused|decoy|extra|misc", f, re.I) for f in files) and '"pop"' not in src and '"traffic"' not in src
       and "passenger" not in src)
    ok("gate: no file or sheet describes the data",
       not any(re.search(r"readme|dictionary|notes|manifest|codebook|schema|field|about", f, re.I) for f in files) and
       not any(re.search(r"\b(readme|notes|dictionary|about|definitions)\b", " ".join(load_workbook(os.path.join(target, f), read_only=True).sheetnames), re.I)
               for f in files if f.endswith(".xlsx")))
    ok("gate: no file name names a judgment", not any(re.search(r"share|correct|adjust|coverage|mirror|estimate|undercount|residual", f, re.I) for f in files))
    # --------------------------------------------------------------------------------------------- never filed
    hits = [(f, m.group(0)) for f, t in T.items() for m in re.finditer(NEVER, t, re.I)]
    ok("never filed: no shipped word names a judgment's step", not hits, hits[:5])
    heads = " ".join(T[f].split(" ")[0] if False else T[f][:400] for f in files if f.endswith(".csv"))
    ok("R1 no shipped column holds a result", not re.search(r"officers?_needed|estimate|corrected|true_|share_of", heads, re.I))
    stocks = [f for f, t in T.items() if re.search(r"Orlavan citizens", t) and f not in (F["estab"], F["order"], F["letter"])]
    ok("never filed: no count of Orlavan citizens in a host after the censuses but Fenmark's of 2016",
       not stocks and "2016" in T[F["count16"]] and not re.search(r"202[2-7]", " ".join(load_workbook(os.path.join(target, F["census"]), read_only=True).sheetnames)), stocks)
    ok("never filed: Orlava's census table holds no row for Orlavan citizens", "Orlava" not in T[F["c14"]].replace("Elsewhere in Orlava", ""))
    ok("R1 the field's raw material ships", all(F[k] in files for k in ("register", "tables", "vital", "census", "c14", "count16")))
    # ----------------------------------------------------------------------------- the pinning list, in the files
    order, reg, letter = T[F["order"]], T[F["regulation"]], T[F["letter"]]
    for label, pat, doc in (
            ("the rate (2.1)", r"one consular officer for every 5,000 Orlavan citizens, or part of 5,000", order),
            ("the date (2.1, 3.1)", r"1 January of the first year of the cycle.*first cycle under this Order is 2027 to 2029", order),
            ("a district is one partner state (1.1)", r"A consular district is the territory of one partner state", order),
            ("each district on its own, no smallest or largest (2.4)", r"fixed for each district on its own.*no smallest or largest", order),
            ("usual residence, twelve months (order 2.2)", r"for a period of twelve months or more", order),
            ("the leavers' window and what a leaver is (4.1)", r"emigrations of citizens from the district \(Regulation 7/2009, article 2\(c\)\) from the date of the last census", order),
            ("emigration whatever the destination (2(c))", r"ceases to be usually resident there, whatever the state they move to", reg),
            ("citizenship as registered and kept (2(d))", r"citizenship registered when they established usual residence.*keeps that classification", reg),
            ("the year of the move (2(e))", r"calendar year in which the change of usual residence took place", reg),
            ("Table A by citizenship, Table B by next residence (3)", r"Table A\. Immigration, by citizenship.*Table B\. Emigration of the reporting state's own citizens, by state of next", reg),
            ("counts at 00:00 on 1 January (4.1)", r"refers to 00:00 on 1 January", reg),
            ("a later release replaces an earlier one (6(3))", r"a later release replaces an earlier one", reg),
            ("24 months (6(1))", r"within 24 months of the end of that year", reg),
            ("the request's window", r"between the census of 1 January 2021 and 31 December 2026", letter)):
        ok("pinned: " + label, re.search(pat, doc), pat)
    ok("the golden uses no constant of the core beyond the years and the rate",
       not re.search(r"C\.(W|A_HOME|B_HOME|B_HOST|RET|AO|WIG|BIRTH|DEATH)\b", open(os.path.join(HERE, "analysis.py")).read() +
                     open(os.path.join(HERE, "results.py")).read()) and "import core" not in open(os.path.join(HERE, "verify.py")).read())
    # -------------------------------------------------------------------------------- the pack against the core
    diff = A.same_as_world(R, RW)
    ok("pack against core: every array the estimate reads is the core's, to the unit", not diff, diff[:4])
    ok("pack against core: the register's counts equal Orlava's released cells, 2011 to 2023",
       all(np.array_equal(R["reg"][t][h][:C.LAST], R["tab"][t, HOME, h][:C.LAST]) for t in "ABCD" for h in HOSTS))
    ok("golden files the truth's officers", fig["officers"] == fig["truth_officers"], fig["truth"])
    ok("the truth sits inside every citizens band and every leavers band",
       all(inside(fig["truth"][h], fig["citizens_band"][h]) for h in HOSTS) and all(inside(fig["truth_left"][h], fig["left_band"][h]) for h in HOSTS),
       [(h, fig["truth"][h], fig["citizens_band"][h], fig["truth_left"][h], fig["left_band"][h]) for h in HOSTS
        if not (inside(fig["truth"][h], fig["citizens_band"][h]) and inside(fig["truth_left"][h], fig["left_band"][h]))])
    ok("the cut pack re-proves the core at level 5", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], fig["rubric"])
    ok("rubric: a run that loses one stump earns 50 or under", max(fig["rubric"]["one_lost"].values()) <= 50, fig["rubric"]["one_lost"])
    ok("rubric: the reflex route earns 30 or under, the rigorous route 50 or under", fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50)
    # ------------------------------------------------------------------------------- the second implementation
    bad = V.compare(V.run(target), json.loads(json.dumps(fig, default=float)))
    ok("verify: the second implementation lands every stated figure", not bad, bad)
    # ---------------------------------------------------------------------------------------- R2 the mess, neutral
    by = A.codes(target)
    import pandas as pd
    raw = pd.read_csv(os.path.join(target, F["register"]), dtype=str, keep_default_na=False)
    own = raw["citizenship"].str.lower().map(by) == HOME
    st = pd.Series(np.where(raw["state_code"].str.strip() != "", raw["state_code"], raw["state_text"]), index=raw.index).str.strip().str.lower().map(by)
    yr = raw["move_date"].str[:4].astype(int) - C.Y0
    dup = raw.duplicated("event_no")
    R2 = dict(R, recD=dict(R["recD"]), host={h: dict(R["host"][h]) for h in HOSTS})
    for h in HOSTS:
        R2["recD"][HOME, h] = np.bincount(yr[own & (st == h) & (raw["event_type"] == "deregistration_abroad")], minlength=C.NY).astype(float)
        R2["host"][h]["ret"] = np.bincount(yr[own & (st == h) & (raw["event_type"] == "registration_from_abroad")], minlength=C.NY).astype(float)
    C._FC.clear(), C._PC.clear()
    off, call = graded(R2, {}, fig)
    ok("SF22 a register event sent twice: with the repeats left in every graded figure stays in its band and the officers stay", not off and call == fig["call"], off)
    C._FC.clear(), C._PC.clear()
    Re = A.load(target, year_of="entered_on")
    off, call = graded(Re, {}, fig)
    ok("R2 events dated by entry in place of the move: every graded figure stays in its band and the officers stay", not off and call == fig["call"], off)
    C._FC.clear(), C._PC.clear()
    ok("R2 a blank state code is resolved by the clerk's text on every row", fig["counts"]["blank_codes"] > 0 and
       bool(st.notna().all()))
    ok("R2 the repeats are whole re-sent runs, identical to their first copy", int(dup.sum()) == fig["counts"]["register_repeats"] and
       len(raw[dup].merge(raw[~dup], how="inner")) == int(dup.sum()))
    # --------------------------------------------------------------------------------- R3 each result's hurried figure
    hc = fig["hurried"]
    ok("R3 component 1's hurried figure is outside its band", not inside(hc["c1"], fig["c1_band"]), hc["c1"])
    ok("R3 component 2's hurried figure is outside its band", not inside(hc["c2"], fig["c2_band"]), hc["c2"])
    ok("R3 component 3's hurried figure is outside its band", not inside(hc["c3"], fig["c3_band"]), hc["c3"])
    refl = fig["routes"]["S1+S2+S3"]
    ok("R3 the hurried citizens are outside the band at every district", all(not inside(refl["citizens"][h], fig["citizens_band"][h]) for h in HOSTS))
    ok("R3 the hurried officers differ at five districts or more", sum(refl["officers"][h] != fig["officers"][h] for h in HOSTS) >= 5)
    for s, own_h in (("S1", "Brennia"), ("S2", "Marovia"), ("S3", "Tesmar")):
        r = fig["routes"][s]
        ok("R3 %s dropped alone moves %s's officers" % (s, own_h), r["officers"][own_h] != fig["officers"][own_h], r["officers"])
        alone = fig["routes"][RS.ALONE[s]]
        ok("R3 %s fixed alone on the reflex route still misses the establishment" % s, alone["officers"] != fig["officers"])
    wrong = {json.dumps(r["answer"]) for r in E["routes"] if not r.get("golden")}
    ok("R3 the shortcuts land on different wrong establishments", len(wrong) >= 6, "%d distinct" % len(wrong))
    # ---------------------------------------------------------------------------------------------- R4 no plant
    ok("R4 no shipped file ranks the districts on the estimate (Gate G)", not any(
        re.search(r"2027", t) and re.search(r"officers", t, re.I) and f not in (F["order"], F["letter"], F["estab"]) for f, t in T.items()))
    ok("R4 the establishment in force answers its own question, on the 2021 census counts",
       "census counts of 1 January 2021" in T[F["estab"]] and all(str(fig["census_2021"][h]) in T[F["estab"]] for h in HOSTS))
    ok("R4 no memo, draft or stakeholder figure ships", not any(re.search(r"memo|draft|review|proposal|briefing", f, re.I) for f in files))
    # ------------------------------------------------------------------------------------------- R5 no one thing
    a, d = fig["share_host_arrivals_pct"], fig["share_host_departures_pct"]
    ok("R5 arrival shares part from the whole across the hosts, and where they decide nothing",
       sum(abs(a[h] - 100.0) > 10 for h in HOSTS) >= 5 and abs(a["Kestria"] - 100.0) > 10 and fig["routes"]["S1"]["officers"]["Kestria"] == fig["officers"]["Kestria"])
    ok("R5 every state's own emigrants are part recorded", all(v < 90 for v in fig["share_partner_emigrants_pct"].values()))
    ok("R5 departure shares are below the whole at every host", all(v < 99 for v in d.values()) and sum(v < 60 for v in d.values()) >= 5)
    late = fig["late_ratio"]
    ok("R5 the years after the tables differ from 2021 to 2023 at most hosts, and where they decide nothing",
       sum(abs(late[h] - 1.0) > 0.1 for h in HOSTS) >= 5 and fig["routes"]["S3"]["officers"]["Almera"] == fig["officers"]["Almera"]
       and not inside(fig["routes"]["S3"]["citizens"]["Almera"], fig["citizens_band"]["Almera"]))
    by_id = {r["id"]: r for r in E["results"]}
    for j in E["factorial"]["judgments"]:
        if j["kind"] == "stump":
            ok("R5 %s fixed alone rescues a third of the results or fewer" % j["id"], len(j["alone"]["results_rescued"]) <= len(by_id) / 3.0,
               j["alone"]["results_rescued"])
            ok("R5 %s dropped alone moves the call" % j["id"], j["dropped"]["answer"] != fig["call"])
    # ----------------------------------------------------------------------------------------- R6 the one-fact test
    for h in E["hints"]:
        ok("R6 the hint rescues a third or fewer: " + h["sentence"][:48], len(h["rescues"]) <= len(by_id) / 3.0, h["rescues"])
    # ------------------------------------------------------------------------------------------------ R7 the rivals
    ok("R7 the battery: every variant files the golden's officers", fig["family_calls_all_golden"] and fig["variants"] >= 12, "%d variants" % fig["variants"])
    C._FC.clear(), C._PC.clear()
    worst = []
    for name, o in C.FAMILY:
        off, call = graded(R, o, fig)
        if off or call != fig["call"]:
            worst.append((name, off[:2]))
    ok("R7 the battery: every variant's every figure sits inside the stated band", not worst, worst[:3])
    ok("R7 forcing: each fitted share moved by its spread leaves the officers", all(p["call_holds"] for p in fig["perturbations"]))
    # -------------------------------------------------------------------------------------------- the fork table
    ok("SF1 a citizen is a person registered as one: the order 2.2 files it and the country-of-birth sheets are another population",
       re.search(r"An Orlavan citizen is a person registered as a citizen of Orlava", order) and "T2 country of birth 2021" in T[F["census"]])
    ok("SF2 a change of citizenship: the regulation 2(d) keeps the classification while resident", re.search(r"keeps that classification", reg))
    ok("SF3 usual residence is twelve months in the order and the regulation", re.search(r"twelve months or more", order) and re.search(r"twelve months or more", reg))
    ok("SF4 1 January 2027 is the start of the day (4.1): the events to 31 December 2026 and none after",
       re.search(r"00:00 on 1 January", reg) and raw["move_date"].max() <= "2026-12-31")
    near = fig["nearest_variant"]["distance"]
    ok("SF5 or part of 5,000 is filed and no variant comes within 900 of a multiple of 5,000", near >= 900, near)
    ok("SF6 a district is one partner state: 1.1 and the schedule name seven", all(h in order for h in HOSTS))
    ok("SF7 moved away is an emigration whatever the destination (4.1, 2(c)); deaths are tabled apart (Table E)",
       re.search(r"whatever the state they move to", reg) and "deaths" in T[F["vital"]])
    ok("SF8 the leavers' window ends 31 December 2026 (the order 4.1, the request)", re.search(r"to the day before the date in 2\.1", order))
    ok("SF9 the year of a move is filed (2(e)) and the register carries both dates", {"move_date", "entered_on"} <= set(raw.columns))
    first = pd.read_csv(os.path.join(target, F["tables"]), dtype=str)
    k = ["table", "reporting_state", "partner", "reference_year", "sex", "age_group"]
    f1 = first.sort_values("release", kind="mergesort").drop_duplicates(k, keep="first")
    f1["persons"] = f1["persons"].astype(int)
    g1 = f1.groupby(["table", "reporting_state", "partner", "reference_year"])["persons"].sum()
    code3 = {v: kk.upper() for kk, v in by.items() if len(kk) == 3 and kk.isalpha() and kk != "zzz"}
    R1 = dict(R, recA=dict(R["recA"]), recD=dict(R["recD"]), host={h: dict(R["host"][h]) for h in HOSTS})

    def cell(t, rep, par):
        out = np.full(C.NY, np.nan)
        for y in range(C.LAST):
            out[y] = g1[t, code3[rep], code3[par], str(C.Y0 + y)]
        return out
    for i in C.STATES:
        for j in C.STATES:
            if i != j and j != HOME:
                R1["recA"][i, j] = cell("A", j, i)
            if i != j and i != HOME:
                R1["recD"][i, j] = cell("B", i, j)
    for h in HOSTS:
        R1["host"][h]["dep"] = cell("C", h, HOME)
    C._FC.clear(), C._PC.clear()
    off, call = graded(R1, {}, fig)
    ok("SF10 the latest release is filed (6(3)); on the first release of every cell the officers stay and every figure keeps its band",
       not off and call == fig["call"], off)
    C._FC.clear(), C._PC.clear()
    arr = raw[(raw["event_type"] == "registration_from_abroad") & ~own & (raw["citizenship"].str.lower().map(by) != "Other")]
    ok("SF11 Table A is by citizenship (article 3) and in the register a foreign citizen's arrival is from the state of citizenship, "
       "so the two readings of an arrival are one count", bool((arr["citizenship"].str.lower().map(by) == st[arr.index]).all()))
    names = fig["variant_names"]
    ok("SF12 births less deaths after 2023 as a count is in the battery; left out is refused by Table E (births exceed deaths in every host and year)",
       "births less deaths carried as a count" in names and fig["births_exceed_deaths_everywhere"])
    ok("SF13 the three other fitting windows are in the battery", all(("shares fitted on " + w) in names for w in ("2014 to 2023", "2011 to 2020", "2016 to 2023")))
    ok("SF14 the mean, the median and the smallest sender dropped are in the battery",
       all(n in names for n in ("host share as the mean of the senders' ratios", "host share as their median", "the smallest sender to each host dropped")))
    rv = fig["referee"]["rivals"]
    ok("SF15 the level: the census table pooled, by mean, by median and Fenmark's accounts are in the battery; the fullest recorder and the "
       "shares' own average are refused by the census table and by the 2016 count",
       all(n in names for n in ("home share as the mean of the seven partners' ratios", "home share as their median",
                                "the level taken from Fenmark's two half-decade accounts")) and
       abs(fig["rigorous_home_share_pct"] - fig["share_home_arrivals_pct"]) > 10 and abs(fig["mean_route_home_share_pct"] - fig["share_home_arrivals_pct"]) > 10
       and rv["shares scaled to the fullest recorder"]["off"] > 5 * fig["referee"]["off"] and rv["shares scaled about their own average"]["off"] > 5 * fig["referee"]["off"],
       (fig["rigorous_home_share_pct"], fig["mean_route_home_share_pct"]))
    ok("SF15 the fullest recorder and the shares' own average file other officers", fig["routes"]["rigorous"]["officers"] != fig["officers"] and
       fig["routes"]["mean"]["officers"] != fig["officers"])
    ok("SF21 the census table's other citizenships counted in: the officers stay and every citizens figure keeps its band",
       fig["other_row"]["call_holds"] and fig["other_row"]["inside_bands"], fig["other_row"]["share_pct"])
    ok("SF16 the register's shares on three later windows, on 2011 to 2020 and pooled over the hosts are in the battery",
       all(("home register's shares on " + w) in names for w in ("2016 to 2023", "2019 to 2023", "2021 to 2023", "2011 to 2020")) and
       "one home register share for all seven hosts" in names)
    ok("SF17 exits timed by Orlava's registrations are in the battery", "exits timed by the home's re-registrations throughout" in names)
    ok("SF18 the 2016 count as a third census is the battery's Fenmark variant, and as a check the estimate is within 150 of it",
       fig["referee"]["off"] <= 150, fig["referee"]["off"])
    blocks = open(os.path.join(os.path.dirname(HERE), "submission.md")).read()
    ok("SF19 every graded figure is stated with its band", blocks.count(" to ") >= 17 and all(
        ("%s citizens usually resident on 1 January 2027 (%s to %s)" % (format(fig["citizens"][h], ","), format(fig["citizens_band"][h][0], ","),
                                                                        format(fig["citizens_band"][h][1], ","))) in blocks for h in HOSTS))
    ok("SF20 the register's entries follow moves by 42 days at most and run to February 2027",
       fig["counts"]["entry_lag_max_days"] <= 42 and fig["counts"]["entered_last"] >= "2027-02-01")
    ok("control: the hosts' tables at face value do not close on their own censuses (the gap is thousands at five hosts or more)",
       sum(abs(v) > 1000 for v in fig["face_value_census_gap_by_host"].values()) >= 5, fig["face_value_census_gap_by_host"])
    # ------------------------------------------------------------------------------------- the referee and controls
    ok("referee: every shortcut misses Fenmark's 2016 count by five times the estimate's error or more",
       all(v["off"] >= 5 * fig["referee"]["off"] for v in rv.values()), {k: v["off"] for k, v in rv.items()})
    ho = fig["held_out"]
    ok("control: held out, the register at its 2011 to 2020 share tracks the arrivals of 2021 to 2023 within a tenth at every host; "
       "the carry of 2018 to 2020 misses by more at six hosts or more and by a quarter or more at two",
       all(abs(ho[h]["register_scaled"] / ho[h]["arrivals"] - 1) < 0.10 for h in HOSTS) and
       sum(abs(ho[h]["carried"] / ho[h]["arrivals"] - 1) > abs(ho[h]["register_scaled"] / ho[h]["arrivals"] - 1) for h in HOSTS) >= 6 and
       sum(abs(ho[h]["carried"] / ho[h]["arrivals"] - 1) > 0.25 for h in HOSTS) >= 2)
    # ----------------------------------------------------------------------------------- the goldens, one set of numbers
    gold = os.path.join(os.path.dirname(HERE), "golden")
    if os.path.isdir(gold):
        with open(os.path.join(gold, deliver.FILES["csv"]), newline="") as fh:
            rows_ = list(csv.DictReader(fh))
        ok("golden CSV: one row per district and year 2011 to 2027 and the 2027 rows are the stated citizens", len(rows_) == 17 * len(HOSTS) and all(
            int(r["citizens_1_january"]) == fig["citizens"][r["district"]] for r in rows_ if r["year"] == "2027"))
        ok("golden CSV: the exits of 2021 to 2026 sum to the stated leavers within the rounding of six rows", all(
            abs(sum(int(r["exits"]) for r in rows_ if r["district"] == h and 2021 <= int(r["year"]) <= 2026) - fig["left"][h]) <= 3 for h in HOSTS))
        ok("golden CSV: the census years carry the census counts", all(
            int(r["citizens_1_january"]) == fig["census_%s" % r["year"]][r["district"]] for r in rows_ if r["year"] in ("2011", "2021")))
        ws = load_workbook(os.path.join(gold, deliver.FILES["wb"]), data_only=True).worksheets[0]
        got = {r[0]: r for r in ws.iter_rows(min_row=6, max_row=12, values_only=True)}
        ok("golden workbook: the first sheet holds the stated citizens, officers and leavers", all(
            got[h][3] == fig["citizens"][h] and got[h][5] == fig["officers"][h] and got[h][7] == fig["left"][h] for h in HOSTS))
        ok("golden workbook: the first sheet names what it rejects", "This is not the establishment" in str(ws["A3"].value))
    # ------------------------------------------------------------------------------------------------ realism sweep
    lag = (pd.to_datetime(raw["entered_on"]) - pd.to_datetime(raw["move_date"])).dt.days
    ok("realism: register entries trail the move unevenly (same day to six weeks)", lag.min() == 0 and 2 < lag.mean() < 12 and lag.max() == 42)
    ok("realism: moves cluster by season and avoid weekends", pd.to_datetime(raw["move_date"]).dt.dayofweek.ge(5).mean() < 0.2)
    ok("truth anchor: the fitted arrival shares recover the world's own within five per cent and the departure shares within eight",
       all(abs(a[h] / (100.0 * C.W[h]["a"]) - 1) < 0.05 and abs(d[h] / (100.0 * C.W[h]["d"]) - 1) < 0.08 for h in HOSTS) and
       sum(a[h] != 100.0 * C.W[h]["a"] for h in HOSTS) >= 6,
       [(h, a[h], C.W[h]["a"], d[h], C.W[h]["d"]) for h in HOSTS])
    # no generator setting in sight: nothing changes level from one year to the next, least of all at a census
    arr = {h: R["recA"][HOME, h][:C.LAST] for h in HOSTS}
    dep = {h: R["host"][h]["dep"][:C.LAST] for h in HOSTS}
    step = {h: float(np.max(np.abs(np.log(arr[h][1:] / arr[h][:-1])))) for h in HOSTS}
    when = {h: int(np.argmax(np.abs(np.log(arr[h][1:] / arr[h][:-1])))) for h in HOSTS}
    ok("realism: no host's tabled arrivals of Orlavan citizens move by more than 60 per cent from one year to the next",
       max(step.values()) < np.log(1.6), step)
    ok("realism: the hosts' largest year-on-year moves in arrivals fall in four different years or more", len(set(when.values())) >= 4, when)
    ok("realism: no host's tabled departures of Orlavan citizens move by more than 60 per cent from one year to the next",
       all(float(np.max(np.abs(np.log(dep[h][1:] / dep[h][:-1])))) < np.log(1.6) for h in HOSTS))
    ok("realism: the hosts' exit rates in the world do not jump at the 2021 census (2020 to 2021 within 30 per cent)",
       all(abs(np.log((world["host"][h]["ex"][10] / world["host"][h]["n"][10]) / (world["host"][h]["ex"][9] / world["host"][h]["n"][9]))) < np.log(1.3)
           for h in HOSTS))
    ok("realism: the 2011 census counts of Orlavan citizens are not round numbers",
       sum(int(fig["census_2011"][h]) % 50 == 0 for h in HOSTS) <= 1, fig["census_2011"])
    whole = pd.read_csv(os.path.join(target, F["pop"]))["usual_residents"].astype(int)
    ok("realism: the states' whole populations are not round numbers (no more than a fiftieth are multiples of 100)",
       int((whole % 100 == 0).sum()) <= max(2, len(whole) // 50), int((whole % 100 == 0).sum()))
    ok("realism: corrected cells are a minority and move a cell by a few persons",
       0 < fig["counts"]["table_rows_superseded"] < 0.08 * fig["counts"]["table_rows"])
    # --- the judge's pass, stage 4: the census-closure route, the pooled departure share, the cap, the late entries
    cl = fig["closure"]
    ok("closure route: each host's two shares fitted on its own census accounts files the golden's officers under every weighting, "
       "with the departure share fitted or closed", cl["officers_same"] and len(cl["fits"]) == 8, cl["nearest_line"])
    ok("closure route refused by the two reports: its arrival share lies outside every sender's reading in four hosts or more",
       len(cl["outside_senders"]) >= 4, cl["outside_senders"])
    ok("closure route refused by the 2021 census: both shares fitted, it misses the count of Orlavan citizens by 250 or more in two hosts",
       sum(abs(v) >= 250 for v in cl["fits"]["unweighted, both"]["census_2021_miss"].values()) >= 2, cl["fits"]["unweighted, both"]["census_2021_miss"])
    ok("closure route refused by Fenmark's 2016 count: every fit misses it by twice the golden's miss or more",
       cl["referee_off"][0] >= 2 * fig["referee"]["off"], cl["referee_off"])
    ok("closure route leaves a stated band in every fit (it is a refused route, not a member of the family)",
       all(any(not inside(v["citizens"][h], fig["citizens_band"][h]) or not inside(v["left"][h], fig["left_band"][h]) for h in HOSTS)
           or not inside(v["c2"], fig["c2_band"]) for v in cl["fits"].values()))
    lv = cl["level"]
    ok("SF23 the level from the hosts' 49 census accounts: inside every stated band and on the golden's officers, alone and with "
       "each other single choice, under four weightings", lv["inside_every_band"] and lv["officers_same"] and lv["rebuilds"] >= 100
       and lv["accounts"] == 49 and abs(lv["home_share_pct"][0] - fig["share_home_arrivals_pct"]) < 1.5
       and abs(lv["home_share_pct"][1] - fig["share_home_arrivals_pct"]) < 1.5, lv["home_share_pct"])
    pd_ = cl["pooled_departures"]
    ok("SF24 the departure share is the host's own on the Orlavan account: pooled over its citizenships it misses the 2021 census "
       "count of Orlavan citizens by 250 or more in two hosts or more",
       sum(abs(pd_[h]["census_2021"] - fig["census_2021"][h]) >= 250 for h in HOSTS) >= 2,
       {h: pd_[h]["census_2021"] - fig["census_2021"][h] for h in HOSTS})
    cp = cl["cap"]
    top = cp["hosts"][cp["top"]]
    ok("SF25 a share above 100 per cent is kept: capped, the home register's share of moves to that host falls below every other host's, "
       "and every sender puts the table above 100", top["home_moves_pct"] < cp["others_home_moves_pct"][0] - 2.0
       and cl["hosts"][cp["top"]]["senders_pct"][0] > 110.0 and top["officers"] == fig["officers"][cp["top"]], top)
    le = fig["late_entries"]
    ok("SF20 the entries still outstanding for the last days of 2026 are two events at most", le["outstanding"] <= 2 and le["tail_days"] <= 3
       and le["over_reach_pct"] < 2.0, le)
    ok("the blocks name each refused level's rule: the geometric mean, the repeated years, face value at 2024",
       "geometric mean of one" in blocks and "repeated through 2024 to 2026" in blocks and "at face value reach 1 January 2024" in blocks
       and "moves that host's own" in blocks)
    ok("the answer blocks carry no em dash and no design word", "\u2014" not in blocks and not re.search(r"\bstump|\breflex\b|\bcore\b|golden", blocks))
    bad = [r for r in ROWS if not r[1]]
    for label, good, detail in ROWS:
        if not good:
            print("FAIL  %s  %s" % (label, detail[:300]))
    print("checks: %d assertions, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
