"""The generator's assertions on the built pack: the input gates, the realism sweep, the bar block (R1 to R7), the clean
truth against the golden, the bands and the forcing, and the golden files. Exit 1 on any failure."""
import collections
import datetime as dt
import json
import os
import re
import sys
import warnings
import zipfile

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import golden as GD  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def pdf_text(path):
    import fitz
    return "\n".join(p.get_text() for p in fitz.open(path))


def main():
    E = json.load(open(os.path.join(HERE, "effort.json")))
    Fg = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(T))
    # ---------------------------------------------------------------- input gates
    ok("G1 ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {("spreadsheet" if f.endswith((".csv", ".xlsx")) else "text") for f in files}
    ok("G2 two or more file categories", len(cats) >= 2, ", ".join(sorted(cats)))
    rows = {f: sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("G3 a CSV of 20,000 rows or more", max(rows.values()) >= 20000, "%s rows" % max(rows.values()))
    ok("G4 a second large CSV of 10 to 20 printed pages or more", sorted(rows.values())[-2] >= 900, str(sorted(rows.values())[-2]))
    ok("G5 two or more distractors named only in metadata", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    ok("G6 no file names the trap or describes the data",
       not any(re.search(r"readme|dictionary|notes|manifest|distractor|rogue|trap|answer", f, re.I) for f in files))
    # ---------------------------------------------------------------- realism sweep
    C = pd.read_csv(os.path.join(T, pack.FILES["changes"]), dtype=str, keep_default_na=False)
    nums = C["change_no"].str.extract(r"CC-(\d\d)-(\d{5})").dropna().astype(int)
    steps = set()
    for y, g in nums.groupby(0):
        steps |= set(np.diff(np.sort(g[1].values)))
    ok("S1 change numbers run with gaps, no constant step", len(steps) > 2, "steps %s" % sorted(steps)[:6])
    V = pd.read_excel(os.path.join(T, pack.FILES["vendor"]))
    rn = np.sort(V["Order"].str[3:].astype(int).values)
    ok("S2 repair order numbers no constant step", len(set(np.diff(rn))) > 2)
    sns = C["serial_off"][C["serial_off"] != ""]
    ok("S3 serials typed several ways (the 2024 scanner prefix, lower case)", sns.str.startswith("S/N").sum() > 5
       and sns.str.contains(r"[a-z]").sum() >= 1)
    ok("S4 both reason vocabularies in the export", {"U", "UNSCH"} <= set(C["reason"]))
    ok("S5 corrected changes carry -R1 and the originals are kept", C["change_no"].str.endswith("-R1").sum() > 5)
    L = pd.read_csv(os.path.join(T, pack.FILES["legs"]), dtype=str)
    ok("S6 the feed's re-sent days are exact duplicates", L.duplicated().sum() > 100, "%d duplicate rows" % L.duplicated().sum())
    ok("S7 some legs lost their air times", (L["off_utc"].isna() | (L["off_utc"] == "")).sum() > 200)
    em = [f for f in files if f.endswith(".csv") and "\u2014" in open(os.path.join(T, f), encoding="utf-8").read()]
    ok("S8 no em dash in any text file", not em, ", ".join(em))
    rep = pdf_text(os.path.join(T, pack.FILES["report"]))
    std = pdf_text(os.path.join(T, pack.FILES["standard"]))
    ok("S9 the report and the standard extract (positive control)", "Reliability report, October 2026" in rep and
       "mean time between unscheduled removals" in std)
    ok("S10 no document names the decisive relations",
       not re.search(r"landing.{0,20}(drive|cause)|rogue|aircraft.{0,15}fault|turnaround.{0,30}load|queue", rep + std, re.I))
    # ---------------------------------------------------------------- the analysis on the pack
    F = A.load(T)
    D = A.drivers_cache(F)
    fc = A.forecast(F, D)
    H = A.hurried(F)
    # R1: the raw material ships at the field's grain
    ok("R1a legs at the leg grain (block and air times)", {"out_utc", "off_utc", "on_utc", "in_utc"} <= set(L.columns))
    U0 = C[C["reason"].isin(["U", "UNSCH"])]
    ok("R1b every unscheduled row carries its aircraft, and a row without a serial off is a fit with its serial on",
       (U0["aircraft"] != "").all() and (U0[U0["serial_off"] == ""]["serial_on"] != "").all())
    ok("R1c no shipped column holds a forecast, a need or a verdict",
       not any(re.search(r"forecast|need|rogue|verdict|expected", c, re.I) for f in files if f.endswith(".csv")
               for c in pd.read_csv(os.path.join(T, f), nrows=1).columns))
    # R2: mess neutral: the golden with each item mishandled keeps every call
    base_set = Fg["call"]
    F_dup = A.load(T)
    ok("R2a the re-sent legs, kept, move the 2027 landing-driven forecasts under 2 per cent",
       all(abs(_rem_with_dups(F_dup, D, k) / fc[k]["total"] - 1) < 0.02 for k in ("SG", "BRK", "BAV")))
    ok("R2b the superseded originals, kept, change the twelve months' counts by under 3 per cent",
       abs(_n12_with_originals(T) / _n12(F) - 1) < 0.03)
    # R3: each priced result's hurried figure outside its band, by a margin
    for r in E["results"]:
        g, b, c = r["golden"], r.get("bands") or r.get("band"), r["passes"]["careful"]
        if isinstance(c, dict) and "value" in c and "grade" in c:
            c = c["value"]
        if r["id"] in ("R2",):
            out = [k for k in g if not (b[k][0] <= c[k] <= b[k][1])]
            ok("R3 %s careful figure outside the band on every landing-driven part" % r["id"], len(out) == len(g),
               "outside on %s" % out)
        if r["id"] == "R3b":
            ok("R3 R3b careful saving outside the band", not (b[0] <= c <= b[1]), "%s against %s" % (c, b))
        if r["id"] == "R3":
            ok("R3 R3 careful set differs from the golden", sorted(c) != sorted(g))
    # R4: no plant
    ok("R4 no repeated block of removal rows", not C.drop(columns=["change_no"]).duplicated().any() or
       C.drop(columns=["change_no"]).duplicated().sum() < 5)
    # R5: every factor across the data
    w = sim.history()
    w.movers = sim.movers_of(w.hist)
    faults = [f for f in w.E.faults if f["onset"] <= P.ASOF]
    ok("R5a aircraft faults on many aircraft and several parts", len({f["tail"] for f in faults}) >= 10 and
       len({f["k"] for f in faults}) >= 5, "%d aircraft, %d parts" % (len({f["tail"] for f in faults}), len({f["k"] for f in faults})))
    rog = [u for u in w.E.units.values() if u["rogue"]]
    ok("R5b rogue serials in several part numbers", len({u["k"] for u in rog}) >= 5)
    ok("R5c the landing-driven wear across several parts (not only the priced)", sum(1 for p in P.PARTS if p["drv"] == "cyc") >= 5)
    ok("R5d the shop's load from every in-house part", len(P.IN_HOUSE) >= 5)
    W = pd.DataFrame()
    Wg, sav = A.watch_golden(F, fc)
    nonrog_victims = [s for s in Wg.index if not w.E.units[s]["rogue"]]
    ok("R5e the watch list holds serials that are not rogue (victims and chance)", len(nonrog_victims) >= 8, str(len(nonrog_victims)))
    # R6: the one-fact test, executed: the exposure hint on the careful pass moves at most R2, never the spares
    Hd = A.hurried(F, exposure="drv", D=D)
    rb = {r["id"]: r for r in E["results"]}
    r2 = rb["R2"]
    near = [k for k in ("SG", "BRK", "BAV") if abs(round(Hd[k]["proj"]) / r2["golden"][k] - 1) <= 0.20]
    ok("R6a the exposure hint takes the landing-driven removals most of the way (within 20 per cent of the golden)",
       len(near) >= 2, "%s" % {k: (round(Hd[k]["proj"]), r2["golden"][k]) for k in ("SG", "BRK", "BAV")})
    r6 = rb["R6"]
    inb6 = sum(1 for k in r6["golden"] if r6["bands"][k][0] <= Hd[k]["spares"] <= r6["bands"][k][1])
    r9 = rb["R9"]
    inb9 = sum(1 for k in r9["golden"] if r9["bands"][k][0] <= Hd[k]["spares"] - P.POOL[k] <= r9["bands"][k][1])
    ok("R6b the exposure hint rescues neither the in-house spares nor the plan's lines", inb6 <= 2 and inb9 < len(r9["golden"]),
       "in-house %d of 5, plan lines %d of %d" % (inb6, inb9, len(r9["golden"])))
    # R7: the rivals inside the bands
    import results as RS
    riv = {"both exposures": RS._forecast_with(F, D, both=RS.both_fit(F)),
           "no-fault-found pooled": RS._forecast_with(F, D, nff_pooled=True)}
    r5 = rb["R5"]
    for n, v in riv.items():
        off = [k for k in A.PARTS if not (r5["bands"][k][0] - 0.5 <= v[k] <= r5["bands"][k][1] + 0.5)]
        ok("R7 rival '%s' inside every removals band" % n, not off, ", ".join(off))
    ok("R7 forcing: every golden-family variant files the call",
       all(sorted(x["answer"]) == sorted(E["forcing"]["golden_answer"]) for x in E["forcing"]["golden_family"]))
    ok("R7 forcing: every perturbation holds the call",
       all(sorted(x["answer"]) == sorted(E["forcing"]["golden_answer"]) for x in E["forcing"]["perturbations"]))
    ok("R7 forcing: every shortcut files another call",
       all(sorted(x["answer"]) != sorted(E["forcing"]["golden_answer"]) for x in E["forcing"]["shortcuts"]))
    # ---------------------------------------------------------------- the clean truth
    ok("T1 the drivers found are the true ones for the priced parts",
       all(D[k]["driver"] == {"cyc": "cyc", "sta": "cyc", "fh": "fh", "cal": "days"}[P.PART[k]["drv"]] for k in ("SG", "BRK", "BAV")))
    ok("T2 the record separates landings from hours for the priced parts (2 dlogL over 6)",
       all(2 * D[k]["ll_gap"] > 6 for k in ("SG", "BRK", "BAV")), str({k: round(2 * D[k]["ll_gap"], 1) for k in ("SG", "BRK", "BAV")}))
    sc = set(Fg["scrap_set"])
    ok("T3 every serial the golden withdraws is a true rogue", all(w.E.units[s]["rogue"] for s in sc))
    ok("T4 every true rogue on the list is withdrawn", all((s in sc) for s in Wg.index if w.E.units[s]["rogue"]))
    R = sim.replay_2027(w, 16)
    tru = {k: np.mean([sum(1 for d, c, f in r["demand"][k] if d.year == 2027) for r in R]) for k in A.PARTS}
    off = [k for k in ("SG", "BRK", "BAV", "PEC") if abs(Fg["rem_%s" % k] / tru[k] - 1) > 0.15]
    ok("T5 the golden's removals within 15 per cent of the truth on the priced parts", not off,
       str({k: (Fg["rem_%s" % k], round(tru[k], 1)) for k in ("SG", "BRK", "BAV", "PEC")}))
    off = [k for k in ("SG", "BRK", "BAV") if abs(round(H[k]["proj"]) / tru[k] - 1) < 0.10]
    ok("T6 the per-flight-hour outlook misses the truth by 10 per cent or more on the landing-driven parts", not off, str(off))
    sp = fc["PEC"]["split"]
    ok("T7 the propeller control's bulletin effect near the truth", abs(sp["rate_mod"] / sp["rate_un"] - P.PART["PEC"]["sb"]) < 0.15,
       "%.2f against %.2f" % (sp["rate_mod"] / sp["rate_un"], P.PART["PEC"]["sb"]))
    # ---------------------------------------------------------------- the semantic fork table, asserted
    import results as RS2
    ok("SF1 unscheduled removals are every UNSCH removal whatever the finding: each part's forecast carries its no-fault-found",
       all(fc[k]["nff"] > 0 for k in A.PARTS))
    ok("SF2 the year is calendar 2027: the forecast's months are January to December and sum to its total",
       all(sorted(fc[k]["by_month"]) == list(range(1, 13)) and abs(sum(fc[k]["by_month"].values()) - fc[k]["total"]) < 1e-6
           for k in A.PARTS))
    fb = pd.read_excel(os.path.join(GOLD, GD.XLSX), sheet_name="Fill by spares")
    fb = fb.set_index("Part number")
    first95 = {k: int(np.argmax(fb.loc[P.PART[k]["pn"]].values.astype(float) >= 95.0)) for k in A.PARTS}
    ok("SF3 the fill rate is over the year's removals: each need is the fewest spares whose replayed fill reaches 95 per cent",
       all(first95[k] == Fg["need_%s" % k] for k in A.PARTS), str({k: (first95[k], Fg["need_%s" % k]) for k in A.PARTS
                                                                   if first95[k] != Fg["need_%s" % k]}))
    snap = pd.read_excel(os.path.join(T, pack.FILES["pool"]), dtype=str)
    pool_snap = {k: int(((snap["Part number"] == P.PART[k]["pn"]) & (snap["Condition"] != "Installed")).sum()) for k in A.PARTS}
    ok("SF4 a pool's spares are every unit beyond the installed ones (serviceable, unserviceable, on order)",
       all(pool_snap[k] == P.POOL[k] == Fg["pool_%s" % k] for k in A.PARTS), str({k: pool_snap[k] for k in A.PARTS if pool_snap[k] != P.POOL[k]}))
    ok("SF5 the 80 per cent range carries the rate's own uncertainty: wider than a Poisson count's at the same mean",
       all(Fg["p90_%s" % k] - Fg["p10_%s" % k] >= A._pois_q(Fg["rem_%s" % k], 0.9) - A._pois_q(Fg["rem_%s" % k], 0.1)
           for k in ("SG", "BRK", "BAV")))
    nfit = sum(int(A.panel(F, k, "CF")["n"].sum()) for k in ("SG", "BAV"))
    ncf = int(((F["removals"]["k"].isin(["SG", "BAV"])) & (F["removals"]["reason"] == "UNSCH") &
               F["removals"]["finding"].isin(["CF", "BER"]) & (F["removals"]["date"] <= A.Y26[1])).sum())
    ok("SF6 the plan is for the units in service: the rates are fitted on every serial, the listed ones too", nfit == ncf,
       "%d of %d" % (nfit, ncf))
    X27 = A.expo_2027(F)
    ok("SF7 the 2027 exposure is the issued programme's: its landings against the twelve months' give the change the plan states",
       abs(X27["cyc"].sum() / F["day"][(F["day"]["date"] >= A.Y26[0]) & (F["day"]["date"] <= A.Y26[1])]["cyc"].sum() - 1
           - Fg["cyc_ch_pct"] / 100) < 0.006)
    lows = []
    for k in sorted(set(Wg["k"])):
        U_ = A.aircraft_driven(F, k)
        win = A.fault_windows(U_)
        ex = A.serial_exposure(F, k, win)
        inw = U_.apply(lambda r: any(a <= r["date"] <= b for a, b in win.get((r["aircraft"], r["position"]), [])), axis=1)
        own = U_[~U_["by_aircraft"] & ~inw].groupby("serial_off").size()
        sns = [x for x in ex if ex[x] > 0]
        n_ = np.array([float(own.get(x, 0)) for x in sns])
        e_ = np.array([ex[x] for x in sns])
        lo, hi, pi, w2 = A.mixture_rates(n_, e_)
        lows.append(lo < n_.sum() / e_.sum())
    ok("SF8 a new unit is compared at the healthy serials' rate, below every listed part's pooled rate", all(lows))
    from scipy import optimize as OPT, special as SPC
    gaps18 = {}
    for k in sorted(set(Wg["k"])):
        U_ = A.aircraft_driven(F, k)
        win = A.fault_windows(U_)
        ex = A.serial_exposure(F, k, win)
        inw = U_.apply(lambda r: any(a <= r["date"] <= b for a, b in win.get((r["aircraft"], r["position"]), [])), axis=1)
        own = U_[~U_["by_aircraft"] & ~inw].groupby("serial_off").size()
        sns = [x for x in ex if ex[x] > 0]
        n_ = np.array([float(own.get(x, 0)) for x in sns])
        e_ = np.array([ex[x] for x in sns])
        lo, hi, pi, w2 = A.mixture_rates(n_, e_)
        if hi / lo < 2:
            continue
        mu = n_.sum() / e_.sum()

        def nll(th):
            m, a_ = np.exp(th[0]), np.exp(th[1])
            p = a_ / (a_ + m * e_)
            return -float(np.sum(SPC.gammaln(n_ + a_) - SPC.gammaln(a_) - SPC.gammaln(n_ + 1) + a_ * np.log(p) +
                                 n_ * np.log(1 - p + 1e-300)))
        llnb = -min((OPT.minimize(nll, [np.log(mu), s0], method="Nelder-Mead",
                                  options={"maxiter": 4000, "xatol": 1e-9, "fatol": 1e-11}) for s0 in (-1, 0, 1, 2, 4)),
                    key=lambda r: r.fun).fun
        l1 = np.log(1 - pi) + n_ * np.log(lo * e_) - lo * e_ - SPC.gammaln(n_ + 1)
        l2 = np.log(pi) + n_ * np.log(hi * e_) - hi * e_ - SPC.gammaln(n_ + 1)
        mx = np.maximum(l1, l2)
        gaps18[k] = 2 * (float(np.sum(mx + np.log(np.exp(l1 - mx) + np.exp(l2 - mx)))) - llnb)
    ok("SF18 a serial's expected rate: two groups, not one gamma; the serials' own counts reject the gamma (2 dlogL over 6)",
       len(gaps18) >= 5 and all(v > 6 for v in gaps18.values()), str({k: round(v, 1) for k, v in gaps18.items()}))
    ok("SF9 the saving is counted for the position over the year: every listed serial's on-wing share under one",
       bool((Wg["on_wing"] < 1).all()))
    rows_pdf = re.findall(r"\n([A-Z]{1,3}\d{3,6})\n", rep.split("Watch list")[-1])
    ok("SF10 the October watch list is the report's own", sorted(set(rows_pdf)) == sorted(Wg.index), "%d in the report" % len(set(rows_pdf)))
    ok("SF11 the change is the spares needed less the pool, on every line the plan names",
       all(Fg["change_%s" % k] == Fg["need_%s" % k] - Fg["pool_%s" % k] for k in Fg["call_units"]))
    ok("SF12 a line is short or over-stocked only where every golden-family method moves it the same way",
       all(all((v[k] > 0) == (Fg["call_units"][k] > 0) and v[k] != 0 for v in RS2.calls_family(E)) for k in Fg["call_units"]))
    ok("SF13 the exposure is forced by the record (landings over hours and days, 2 dlogL over 6)",
       all(2 * D[k]["ll_gap"] > 6 and D[k]["driver"] == "cyc" for k in ("SG", "BRK", "BAV")))
    r5 = {r["id"]: r for r in E["results"]}["R5"]
    ok("SF14 the window the rates are fitted on (the whole record, 2024 to 2026, the last twelve months) inside every band",
       all(r5["bands"][k][0] <= Fg["rem_%s" % k] <= r5["bands"][k][1] for k in A.PARTS))
    taxi = []
    for so in (3.0, 8.0):
        F2 = dict(F)
        F2["taxi"] = {"out": dict(F["taxi"]["out"]), "in": dict(F["taxi"]["in"])}
        for fld in ("SSJ", "BNN", "MJF", "MQN", "RVK"):
            if fld not in F["taxi"]["out"]:
                F2["taxi"]["out"][fld], F2["taxi"]["in"][fld] = so, so
        taxi.append(A.expo_2027(F2)["fh"].sum() / X27["fh"].sum() - 1)
    ok("SF15 the unseen Helgeland fields' taxi time moves 2027's flight hours by under 1.5 per cent from 3 to 8 minutes",
       all(abs(x) < 0.015 for x in taxi), str([round(x, 4) for x in taxi]))
    ok("SF16 the shop's staffing and capacity: the call holds with the calibrated capacity 5 per cent either side",
       all(sorted(x["answer"]) == sorted(E["forcing"]["golden_answer"]) for x in E["forcing"]["perturbations"]
           if "capacity" in x["input"]))
    Lr = F["legs"]
    m12 = (Lr["date"] >= A.Y26[0]) & (Lr["date"] <= A.Y26[1])
    air12 = float(Lr[m12]["fh"].sum())
    blk12 = float((Lr[m12]["block"] / 60.0).sum())
    rep_fh = float(re.search(r"flew ([\d,]+) flight hours", rep).group(1).replace(",", ""))
    ok("SF17 flight hours are air time: the report's twelve-month total reproduces on off to on and not on out to in",
       abs(air12 / rep_fh - 1) < 0.005 and blk12 / rep_fh > 1.3, "air %.0f, block %.0f, report %.0f" % (air12, blk12, rep_fh))
    # ---------------------------------------------------------------- figures and files
    ok("F1 the golden ZIP's files are exactly the requested two", sorted(os.listdir(GOLD)) == sorted([GD.XLSX, GD.PPTX]))
    wb = pd.read_excel(os.path.join(GOLD, GD.XLSX), sheet_name="Spares plan 2027", header=3)
    wb = wb[wb["Part number"].isin([p["pn"] for p in P.PARTS])]
    ok("F2 the workbook's sixteen lines agree with figures.json",
       len(wb) == 16 and all(int(r["Spares needed"]) == Fg["need_%s" % A.PARTS[[p["pn"] for p in P.PARTS].index(r["Part number"])]]
                             for _, r in wb.iterrows()))
    ok("F3 the workbook's removals agree with figures.json",
       all(int(r["Expected 2027 unscheduled removals"]) == Fg["rem_%s" % A.PARTS[[p["pn"] for p in P.PARTS].index(r["Part number"])]]
           for _, r in wb.iterrows()))
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("F4 no em dash in the submission or the prompt", "\u2014" not in sub and "\u2014" not in open(os.path.join(TASK, "prompt.txt")).read())
    ok("F5 the recommendation states the buy and cut totals", ("Buy %d" % Fg["buy_units"]) in sub and ("cut %d" % Fg["cut_units"]) in sub)
    from pptx import Presentation
    prs = Presentation(os.path.join(GOLD, GD.PPTX))
    txt = " ".join(s.text for sl in prs.slides for s in sl.shapes if s.has_text_frame)
    ok("F6 the slides carry the watch-list saving and every withdrawn serial",
       ("about %d removals" % Fg["saving"]) in txt and all(s in txt for s in Fg["scrap_set"]))
    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print("%s  %-90s %s" % ("PASS" if good else "FAIL", label, detail))
    print("checks: %d of %d pass" % (len(RES) - len(fails), len(RES)))
    sys.exit(1 if fails else 0)


def _rem_with_dups(F, D, k):
    L = pd.read_csv(os.path.join(T, pack.FILES["legs"]), dtype=str)
    F2 = dict(F)
    for c in ("out_utc", "off_utc", "on_utc", "in_utc"):
        L[c] = pd.to_datetime(L[c], format="%Y-%m-%dT%H:%MZ", errors="coerce")
    L["date"] = pd.to_datetime(L["flight_date"])
    L["fh"] = ((L["on_utc"] - L["off_utc"]).dt.total_seconds() / 3600).fillna(((L["in_utc"] - L["out_utc"]).dt.total_seconds() / 3600) - 0.15)
    day = L.groupby(["aircraft", "date"]).agg(cyc=("fh", "size"), fh=("fh", "sum")).reset_index()
    day = day.merge(F["day"][["aircraft", "date", "base", "tmin", "frost"]], on=["aircraft", "date"], how="left")
    F2["day"] = day
    A._DCACHE.pop(id(F2), None)
    return A.forecast(F2, A.drivers(F2))[k]["total"]


def _n12(F):
    R = F["removals"]
    return int(((R["reason"] == "UNSCH") & (R["date"] >= A.Y26[0]) & (R["date"] <= A.Y26[1])).sum())


def _n12_with_originals(target):
    C = pd.read_csv(os.path.join(target, pack.FILES["changes"]), dtype=str, keep_default_na=False)
    C["date"] = pd.to_datetime(C["change_date"])
    C = C[C["reason"].isin(["U", "UNSCH"]) & (C["serial_off"] != "")]
    return int(((C["date"] >= A.Y26[0]) & (C["date"] <= A.Y26[1])).sum())


if __name__ == "__main__":
    main()
