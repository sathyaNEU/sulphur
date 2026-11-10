"""The build's assertions, run on the cut pack (python3 checks.py [target]): the call against the draft and the trailing
extrapolations, the bar block (R1 to R7), every fork in the design note (SF1 to SF24), each graded figure's place in
its bin at its stated rounding, the routes' separation, the commitment rule, the band with and without the
estimation uncertainty, the mess neutrality, the input gates, the realism sweep and the distractors' deletion test.
Exit 1 on any failure."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as An
import build as BD
import effort_passes as EP
import golden as GD
import load as LD
import params as P
import passes as PS
import routes as RT
import writeup as WU

FAIL, N = [], [0]
r10k, r100k, r50k, commit_m, rk, ROUND = GD.r10k, GD.r100k, GD.r50k, GD.commit_m, GD.rk, GD.ROUND
PEOPLE = {"Naomi Weijters", "Jelte Helmerhorst", "Floortje Huisman", "Niels Thout", "Stijn Totwiller", "Isis Kloppert",
          "Cornelis Adriaansen", "Indy Smits", "Lois Jansen", "Noud Geertsen", "Duncan Reed", "Sandra Garner",
          "Reimund Budig", "Erika Buchholz", "Siem Cammel", "Jinthe Kwaadland", "Bente Verbruggen",
          "Senna Lutterveld"}
STEP = 1e5


def ok(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def edge(x, step):
    """Distance from x to the nearest rounding edge under nearest rounding at this step."""
    return step / 2 - abs(x - round(x / step) * step)


def edge_floor(x, step):
    """Distance from x to the nearest step boundary (the commitment's largest-step rule rounds down)."""
    f = (x / step) % 1.0
    return min(f, 1 - f) * step


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def main(target):
    F, B, g, R = GD.compute(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    eff = json.load(open(os.path.join(HERE, "effort.json")))
    res = {r["id"]: r for r in eff["results"]}
    months = figs["path_months"]
    draws = np.array(g["draws"])
    car = R["careful but hurried"]
    naive = {k: v for k, v in R["naive"].items() if k != "kind"}

    # ------------------------------------------------------------------ the call, the draft and the trailing views
    ok("figures.json is the golden recomputed", figs == WU.figures(F, B, g, R))
    ok("call: the commitment is below the draft", figs["commitment"] < figs["draft"],
       "%s against %s" % (figs["commitment"], figs["draft"]))
    ok("draft at least two steps above the commitment", figs["draft"] - figs["commitment"] >= 0.2 - 1e-9)
    ok("draft at least two steps below every trailing extrapolation", all(v >= figs["draft"] * 1e6 + 2 * STEP - 1
                                                                          for v in naive.values()),
       str({k: round(v / 1e3) for k, v in naive.items()}))
    ok("every trailing extrapolation above the expected December figure", all(v > g["dec27"] + 2 * STEP
                                                                               for v in naive.values()))
    ok("careful pass's commitment at or above the draft (it wrongly clears it)", commit_m(car) >= GD.DRAFT,
       str(commit_m(car)))
    ok("quick pass far above the draft", figs["quick_commitment"] >= GD.DRAFT + 0.5, str(figs["quick_commitment"]))
    ok("the draft is met in fewer than 60 of 100 paths", figs["draft_chance_pct"] < 60, str(figs["draft_chance_pct"]))

    # ------------------------------------------------------------------ the commitment rule (policy 5.3)
    com, met, met_next = An.commitment(draws)
    ok("commitment is the largest 0.1 million step met in at least 80 per cent of the paths",
       abs(com / 1e6 - figs["commitment"]) < 1e-9 and met >= 0.8 and met_next < 0.8,
       "%.0f met %.3f next %.3f" % (com, met, met_next))
    ok("commitment is the floor of the 20th percentile at the step", np.floor(g["p20"] / STEP) * STEP == com)
    ok("20th percentile clear of both step boundaries", edge_floor(g["p20"], STEP) >= 20000,
       "%.0f from a boundary" % edge_floor(g["p20"], STEP))
    nop = R["band without the estimation uncertainty"]
    ok("SF20 band with and without the estimation uncertainty lands the commitment in the same step",
       commit_m(nop) == figs["commitment"], "%s against %s" % (commit_m(nop), figs["commitment"]))
    ok("SF20 the 20th percentile without the estimation uncertainty is clear of both step boundaries",
       edge_floor(nop["p20"], STEP) >= 15000, "%.0f" % edge_floor(nop["p20"], STEP))
    ok("SF20 the band with the estimation uncertainty is the wider one", g["p90"] - g["p10"] > nop["p90"] - nop["p10"])
    com_r = R["an assumed common factor of 0.25 added"]
    ok("SF21 an assumed common factor widens the 80 per cent range by a fifth or more and lowers the 20th percentile",
       (com_r["p90"] - com_r["p10"]) >= 1.2 * (g["p90"] - g["p10"]) and com_r["p20"] < g["p20"],
       "%.0f against %.0f" % (com_r["p90"] - com_r["p10"], g["p90"] - g["p10"]))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    ok("R1 raw: contract lines at line grain", len(F["raw_lines"]) > 3000, str(len(F["raw_lines"])))
    ok("R1 raw: Team invoices at invoice grain", len(F["raw_team"]) > 150000)
    ok("R1 raw: workspace activity per workspace-month", len(F["ws"]) > 200000)
    ok("R1 raw: renewal events built from lines and activity", len(B.E) > 2000, str(len(B.E)))
    ok("R1 raw: pipeline snapshots with stage dates", len(F["snap"]) > 9000)
    cols = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols |= set(next(csv.reader(open(os.path.join(target, f)))))
    ok("R1 raw: no shipped column holds a forecast or a result", not any(re.search(r"arr|forecast|churn|retention|"
                                                                                    r"utili|uplift|win_prob|season", c)
                                                                         for c in cols), str(sorted(cols)))

    # ------------------------------------------------------------------ R2: every mess item real and neutral
    base = PS.golden(PS.Book(F), reps=300, seed=RT.SEED)

    def graded(f):
        return {"R2": r10k(f["price"]), "R3": rk("team_left")(f["team_left"]),
                "R4": {"contraction": rk("contraction")(f["contraction"]), "churn": rk("churn")(f["churn"])},
                "R5": {"new_bus": r10k(f["new_bus"]), "new_open": rk("new_open")(f["new_open"])}, "R6": commit_m(f)}
    for item, kw, r1_moves in (("re-exported lines kept", {"dedupe": False}, True),
                               ("credited lines kept beside their re-issues", {"credits": False}, True),
                               ("onboarding fees read as subscriptions", {"fees": False}, True),
                               ("failed Team invoices read in place of the paid ones", {"paid_only": False}, False),
                               ("re-run snapshot rows kept", {"snap_dedupe": False}, False)):
        Fm = LD.load(target, **kw)
        b_m, t_m = An.arr_at(Fm, P.CUT)[:2]
        moved = abs(b_m - g["open_bus"]) + abs(t_m - g["open_team"]) > 5000
        try:
            fm = PS.golden(PS.Book(Fm), reps=300, seed=RT.SEED)
        except Exception as ex:
            # the mishandling leaves two lines on one term and breaks the renewal pairing outright: visible, so it
            # cannot move a forward result quietly
            ok("R2 mess visible: %s stops the renewal pairing" % item, kw in ({"dedupe": False}, {"fees": False}, {"credits": False}),
               repr(ex)[:80])
        else:
            gm = graded(fm)
            inside = all(EP.grade(res[k], gm[k]) == "right" for k in gm)
            ok("R2 mess neutral: %s leaves R2 to R6 in their bands" % item, inside, str(gm))
        if r1_moves:
            ok("R2 mess graded by R1: %s moves the opening book" % item, moved)
    ok("R2 mess: monthly-typed amounts never enter the golden (quoted seats are priced)",
       "amount" not in " ".join(F["snap"].columns))
    ok("R2 mess: CRM name spellings never enter the golden (ids join)", "name" not in " ".join(F["acc"].columns))

    # ------------------------------------------------------------------ R3: each result's hurried figure
    cv = EP.values(car, figs, months)
    for rid, want in (("R1", ("right",)), ("R2", ("missed",)), ("R3", ("missed",)), ("R4", ("partly", "missed")),
                      ("R5", ("missed",)), ("R6", ("missed",)), ("R7", ("missed",))):
        ok("R3 careful pass on %s is %s" % (rid, " or ".join(want)), EP.grade(res[rid], cv[rid]) in want,
           "%s %s" % (cv[rid] if rid != "R7" else "", EP.grade(res[rid], cv[rid])))
    ok("R3 hurried R1: every line summed is outside", figs["r1_all_lines"] != figs["open_bus"])
    for k, key, rid in (("mean uplift applied flat", "price", "R2"), ("list rise applied flat", "price", "R2"),
                        ("Team rates since April", "team_left", "R3"), ("Team rates before April", "team_left", "R3"),
                        ("Team rates of the last three months", "team_left", "R3"),
                        ("Team rates of the trailing twelve months", "team_left", "R3"),
                        ("CRM stage probabilities", "new_open", "R5")):
        step = ROUND.get(key, 1e4)
        v = R[k][key]
        band = res[rid]["band"] if "band" in res[rid] else res[rid]["bands"][key]
        ok("R3 route %s outside %s's bin by 7,000 or more past the edge" % (k, rid),
           v <= band[0] - step / 2 - 7000 or v >= band[1] + step / 2 + 7000, "%d against %s" % (v, band))
    ok("R3 pooled renewal rates outside on accounts lost", rk("churn")(R["pooled renewal rates"]["churn"]) !=
       figs["churn"], str(rk("churn")(R["pooled renewal rates"]["churn"])))
    ok("R3 win odds by stage alone at least 30,000 above the golden's open deals (the CRM's odds carry R5's loss)",
       R["win odds by stage alone"]["new_open"] - g["new_open"] >= 30000)
    ok("R3 independent draws outside on accounts lost", R["accounts drawn independently"]["churn"] <=
       res["R4"]["bands"]["churn"][0] - 100000)
    for k in ("accounts drawn independently", "CRM stage probabilities", "pooled renewal rates", "careful but hurried"):
        ok("R3 route %s files a commitment above the golden's step" % k, commit_m(R[k]) > figs["commitment_hi"],
           str(commit_m(R[k])))
    ok("R3 the trailing run-rate of new ARR misses the open deals' part", rk("new_open")(R["trailing run-rate of new ARR"]["new_open"])
       != figs["new_open"])

    # ------------------------------------------------------------------ R4: no plant
    ok("R4 no plant: the KPI export reproduces from the files", all(
        abs(sum(An.arr_at(F, m)[:2]) - (r[1] + r[2])) < 0.05 for m, r in
        zip(range(P.CUT - 9, P.CUT), _kpi(target))))
    ok("R4 no plant: no file ships a forecast or a draft figure", not any(("%.1f" % GD.DRAFT) in f or "plan" in f.lower()
                                                                          for f in os.listdir(target)))

    # ------------------------------------------------------------------ R5: no one thing (footprints across the data)
    E = B.E
    ok("R5 uplift gradient across every 2026 repricing", An.fit_business(E)["uplift_n"] >= 300 and
       g["uplift_fit"][0] < -0.02, str(g["uplift_fit"]))
    Tp = B.Tp
    pad = Tp[Tp["padded"] & (Tp["k"] >= 0)]
    tfit = An.fit_team(Tp)
    ok("R5 January excess on every padded account, every month since January", pad["acc"].nunique() >= 900 and
       all(v > 0 for v in tfit["excess"].values()), str(pad["acc"].nunique()))
    ok("R5 the January excess has decayed by the cut", np.mean([tfit["excess"][k] for k in sorted(tfit["excess"])[-3:]])
       < 0.4 * tfit["excess"][0])
    # the calendar pattern of Team cancellations runs through every year before the minimum
    pre = Tp[(Tp["m"] < P.TEAM_MIN - 1) & (Tp["m"] >= 0)]
    by_year = pre.assign(y=(pre["m"] + 1) // 12, aut=pre["cal"].isin([8, 9, 10, 11]), win=pre["cal"].isin([2, 3, 4, 5]))
    yr = by_year.groupby("y").apply(lambda d: d[d["aut"]]["cancel"].mean() / d[d["win"]]["cancel"].mean(),
                                    include_groups=False)
    ok("R5 autumn cancellations above late winter's in every year", len(yr) >= 4 and (yr > 1.15).all(),
       str(yr.round(2).to_dict()))
    ok("R5 the calendar index is read from the history, high autumn low winter",
       max(g["team_season"], key=g["team_season"].get) in (8, 9, 10, 11) and
       min(g["team_season"], key=g["team_season"].get) in (2, 3, 4, 5))
    yrs = E.assign(y=E["k"] // 12)
    cut_by_year = yrs[yrs["renewed"] == 1].groupby("y").apply(
        lambda d: np.corrcoef(d["U"], d["new_seats"] / d["seats"])[0, 1], include_groups=False)
    ok("R5 seat cuts follow utilisation in every year", (cut_by_year > 0.2).all(), str(cut_by_year.round(2).to_dict()))
    # utilisation at signing has drifted down through the whole history, so the forward book differs from the pool
    acc = F["acc"].set_index("acc")
    first_u = []
    for i, r in B.st.iterrows():
        st0 = acc.loc[i, "start"] if i in acc.index else None
        if st0 is None or st0 < 0:
            continue
        vals = [B.A.get((i, mm), np.nan) for mm in range(st0 + 4, st0 + 10)]
        vals = [x for x in vals if not (isinstance(x, float) and np.isnan(x))]
        if vals:
            first_u.append((st0 // 12, float(np.mean(vals)) / r["seats0"]))
    fu = pd.DataFrame(first_u, columns=["y", "u"]).groupby("y")["u"].mean()
    ok("R5 utilisation after signing falls cohort by cohort", len(fu) >= 4 and fu.iloc[-1] < fu.iloc[0] - 0.05,
       str(fu.round(3).to_dict()))
    sib_years = yrs[yrs["sib"] == 1].groupby("y").size()
    ok("R5 group exits in every year", len(sib_years) >= 4 and (sib_years >= 5).all(), str(sib_years.to_dict()))
    S = B.S
    stale = S[(S["m"] <= P.CUT - 14)].groupby(S["m"] // 12)["sb"].apply(lambda x: (x == 2).mean())
    ok("R5 stale deals in every year's snapshots", (stale > 0.1).all(), str(stale.round(2).to_dict()))
    lost = [r["id"] for r in eff["results"] if EP.grade(r, r["passes"]["careful"]) != "right"]
    for h in eff["hints"]:
        ok("R5/R6 hint rescues a third or fewer of the lost results: %s" % h["sentence"][:50],
           len(h["rescues"]) <= len(lost) / 3.0 + 1e-9 and len(h["rescues"]) <= 7 / 3.0, str(h["rescues"]))

    # ------------------------------------------------------------------ R6: the one-fact test, computed
    for k, v in R.items():
        if v.get("kind") == "hint":
            now = EP.values(v, figs, months)
            resc = [r["id"] for r in eff["results"] if EP.grade(r, cv[r["id"]]) != "right" and
                    EP.grade(r, now[r["id"]]) == "right"]
            listed = [h["rescues"] for h in eff["hints"] if h["sentence"] == v["sentence"]][0]
            ok("R6 hint executed rescues what it lists: %s" % v["sentence"][:40], resc == listed, str(resc))

    # ------------------------------------------------------------------ R7: the rivals inside every band, one bin
    for k, v in R.items():
        if v.get("kind") != "rival":
            continue
        vv = EP.values(v, figs, months)
        for rid in ("R2", "R3", "R4", "R5", "R6"):
            ok("R7 rival %s inside %s" % (k, rid), EP.grade(res[rid], vv[rid]) == "right", str(vv[rid]))
    for k in ("team_left", "new_open", "contraction", "churn", "price"):
        ok("R7 the defensible family lands in one bin on %s" % k, figs["band_" + k][0] == figs["band_" + k][1],
           str(figs["band_" + k]))
    ok("R7 the defensible family lands in one step on the commitment", figs["commitment_lo"] == figs["commitment_hi"],
       "%s to %s" % (figs["commitment_lo"], figs["commitment_hi"]))
    ok("R7 new Business total within 30,000 across the family (the open deals' family carried into the bridge line)",
       figs["band_new_bus"][1] - figs["band_new_bus"][0] <= 30000, str(figs["band_new_bus"]))

    # ------------------------------------------------------------------ fork table
    pol = " ".join(pdf_text(os.path.join(target, BD.FILES["policy"])).split())
    ok("SF control: the policy reads back", "ARR reporting policy" in pol and len(pol) > 3000, str(len(pol)))
    ok("SF1 ARR as contracted charges in force", "in force on the last day of that month" in pol)
    ok("SF2 GBP at the plan rate", "EUR 1.16 per GBP" in pol and P.PLAN_RATE_GBP == 1.16)
    gb = F["lines"]
    mk = gb.copy()
    mk.loc[mk["cur"] == "GBP", "price"] *= 1.19 / 1.16
    ok("SF2 a market rate would move R1", abs(An.arr_at({"lines": mk, "team": F["team"]}, P.CUT)[0] -
                                              g["open_bus"]) > 10000)
    ok("SF3 onboarding fees and part-term charges excluded", "onboarding fees" in pol and
       "part-term charge" in pol)
    ok("SF4 every credit note references a line that is re-issued", _credits_reissued(F["raw_lines"]))
    ok("SF5 re-exported duplicates are exact copies", F["raw_lines"].duplicated().sum() > 0 and
       F["raw_lines"].drop_duplicates()["line_id"].is_unique)
    ok("SF6 Team ARR from the paid invoice's seats billed", "seats billed on that invoice" in pol)
    ft = F["raw_team"]
    ok("SF7 each failed Team invoice has a paid re-issue for its period", _failed_paid(ft))
    ok("SF8 price movement on seats before renewal", "immediately before the renewal" in pol)
    ok("SF9 seat reductions at the renewed price", "at the renewed price" in pol)
    ok("SF10 lost at its last day in force", "as it stood on its last day in force" in pol)
    ok("SF11 an upgrade is lost from Team and new to Business", "its Business contract is new Business" in pol)
    ok("SF12 the range is the 10th to 90th percentile over the outcomes, filed in policy 5.2",
       "10th to the 90th percentile" in pol and "accounts and deals on the books and of those that join" in pol and
       abs(np.percentile(draws, 10) - g["p10"]) < 1 and abs(np.percentile(draws, 90) - g["p90"]) < 1)
    ok("SF13 the commitment is the largest 0.1 million step met in 80 per cent of outcomes, filed in policy 5.3",
       "largest EUR 0.1 million step that is met or beaten in at least 80 per cent of the outcomes" in pol)
    ok("SF14 the window is November 2026 to December 2027, 14 month ends", len(g["path"]) == 14 and
       months[0] == "Nov 2026" and months[-1] == "Dec 2027")
    sn = pd.read_csv(LD.find(target, "pipeline_snapshots"))
    mon = sn[sn["amount_period"] == "Monthly"]
    ok("SF15 monthly-typed amounts are a twelfth of the annual figure on quoted seats", len(mon) > 300 and
       np.allclose(mon["amount"] * 12, mon["seats_quoted"] * 12 * np.where(
           pd.to_datetime(mon["snapshot_date"]) >= pd.Timestamp(2026, 1, 1),
           np.where(mon["currency"] == "GBP", 16.5, 19.0), np.where(mon["currency"] == "GBP", 13.0, 15.0))))
    ok("SF16 uplift by size band inside R2", EP.grade(res["R2"], r10k(R["uplift by size band"]["price"])) == "right")
    ok("SF17 January excess two months or exponential inside R3", all(
        EP.grade(res["R3"], rk("team_left")(R[k]["team_left"])) == "right" for k in ("April excess from the last two months",
                                                                                   "April excess as an exponential with a floor")))
    ok("SF18 seat additions forms keep the commitment in its step", all(
        EP.grade(res["R6"], commit_m(R[k])) == "right" for k in ("own drift over 12 months", "own drift over 18 months",
                                                                 "each account's trailing true-up rate")))
    ok("SF19 rounding: ARR to EUR 10,000, the two note figures at their stated precision, the commitment a 0.1 million step",
       all(v % 10000 == 0 for v in figs["path"]) and figs["team_left"] % ROUND["team_left"] == 0 and
       figs["new_open"] % ROUND["new_open"] == 0 and round(figs["commitment"], 1) == figs["commitment"])
    ok("SF21 the policy adds nothing beyond the records", "No allowance is added to the range beyond what the records show"
       in pol and "carry their own estimation uncertainty in the range" in pol)
    ok("SF22 deal creation over twelve or eighteen months inside R5",
       EP.grade(res["R5"], EP.values(R["deal creation over the trailing eighteen months"], figs, months)["R5"]) == "right")
    ok("SF23 the calendar index by quarter or smoothed inside R3", all(
        EP.grade(res["R3"], rk("team_left")(R[k]["team_left"])) == "right" for k in ("Team calendar index by quarter",
                                                                                   "Team calendar index smoothed")))
    ok("SF24 utilisation in bins or left out inside R4 and R6", all(
        EP.grade(res["R4"], EP.values(R[k], figs, months)["R4"]) == "right" and commit_m(R[k]) == figs["commitment"]
        for k in ("utilisation in bins", "no utilisation term in the exit model")))
    ok("bridge adds up exactly at the rounding", figs["open_total"] + sum(figs["bridge"].values()) == figs["dec27"])
    ok("bridge identity unrounded", abs(g["open_total"] + g["new_bus"] + g["expansion"] + g["price"] - g["contraction"]
                                        - g["churn"] + g["team_left"] + g["team_new"] - g["open_team"] - g["dec27"]) < 1)

    # ------------------------------------------------------------------ mid-bin
    for k, step, need in (("open_bus", 1e4, 300), ("open_team", 1e4, 300), ("price", 1e4, 1500),
                          ("team_left", ROUND["team_left"], 10000), ("contraction", ROUND["contraction"], 10000),
                          ("churn", ROUND["churn"], 10000), ("new_open", ROUND["new_open"], 10000),
                          ("new_bus", 1e4, 1000), ("dec27", 1e4, 1500), ("p10", 1e4, 1500), ("p90", 1e4, 1500)):
        ok("mid-bin %s" % k, edge(g[k], step) >= need, "%.0f from its edge" % edge(g[k], step))
    # every member of the defensible family clear of the bin's edge at the figure's own precision
    fam = [g] + [v for v in R.values() if v.get("kind") == "rival"]
    for k in ("team_left", "new_open", "contraction", "churn", "price"):
        step = ROUND.get(k, 1e4)
        worst = min(edge(x[k], step) for x in fam)
        ok("family clear of %s's bin edge by 3,000 or more" % k, worst >= 3000, "%.0f" % worst)

    # ------------------------------------------------------------------ input gates
    files = [f for f in os.listdir(target) if not f.startswith(".")]
    ok("gate: 10 or more usable files", len(files) >= 10, str(len(files)))
    ok("gate: 2 or more file categories", len({f.rsplit(".", 1)[1] for f in files} & {"csv", "xlsx"}) >= 1 and
       any(f.endswith(".pdf") for f in files))
    sizes = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", max(sizes.values()) >= 20000)
    ok("gate: a second large messy CSV (10 to 20 printed pages or more)", sorted(sizes.values())[-2] >= 1000 and
       sizes[BD.FILES["lines"]] >= 1000)
    ok("gate: two distractors, named only in metadata", len(BD.DISTRACTORS) == 2 and
       not any("distract" in f for f in files))
    ok("gate: no readme, dictionary, notes or manifest", not any(re.search(r"readme|dictionar|notes|manifest|schema",
                                                                           f, re.I) for f in files))
    # distractor deletion test
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in [BD.FILES[k] for k in BD.DISTRACTORS]:
            shutil.copy(os.path.join(target, f), tmp)
    Fd = LD.load(tmp)
    gd = PS.golden(PS.Book(Fd), reps=300, seed=RT.SEED)
    ok("distractors deleted: every figure unchanged", all(abs(gd[k] - base[k]) < 1e-6 for k in
                                                          ("open_bus", "open_team", "price", "team_left", "new_open",
                                                           "dec27", "p20", "commitment")))
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ realism sweep
    for f, idc in ((BD.FILES["lines"], "line_id"), (BD.FILES["team"], "invoice_no"),
                   (BD.FILES["closed"], "opportunity_id"), (BD.FILES["tickets"], "ticket_id"),
                   (BD.FILES["nps"], "response_id")):
        col = pd.read_csv(os.path.join(target, f), usecols=[idc])[idc].astype(str).str.replace(r"\D", "", regex=True)
        dif = np.diff(col.astype(np.int64).values)
        ok("realism: %s.%s not an arithmetic sequence" % (f[:20], idc), len(set(dif.tolist())) > 2)
    crm = pd.read_excel(LD.find(target, "crm_accounts_export"))
    shapes = crm["Account name"].str.extract(r"(B\.V\.|GmbH|Ltd|plc|KG|N\.V\.|Groep|Gruppe|& |Stichting|en Zonen)")[0]
    ok("realism: company names take more than two shapes", shapes.fillna("none").nunique() >= 4)
    ok("realism: parent names typed several ways", crm.groupby("Parent account ID")["Parent account"].nunique().max() >= 2)
    ok("realism: owners are drawn personas", set(sn["owner"]) <= PEOPLE and set(crm["Account owner"]) <= PEOPLE)
    per_month = F["raw_team"].groupby(F["raw_team"]["period_start"].str[:7]).size()
    ok("realism: no repeated monthly invoice counts", per_month.nunique() >= len(per_month) - 3)
    kp = _kpi(target)
    ok("realism: KPI totals not round", all(abs(r[3] % 1000) > 1e-6 for r in kp))
    lt = pd.read_csv(LD.find(target, "workspace_account_links"))
    ok("realism: links restart at upgrades", (lt["linked_to"].notna()).sum() >= 100)
    ok("realism: no extract date after the pull", all(_max_date(os.path.join(target, f)) <= dt.date(2026, 11, 3)
                                                      for f in (BD.FILES["team"], BD.FILES["snap"],
                                                                BD.FILES["closed"], BD.FILES["nps"])))
    ok("realism: policy v5 dated before the cut and after v4", "21 September 2026" in pol and "Version 5" in pol and
       "February 2026" in pol)
    ok("realism: the KPI export names the policy version in force when it was refreshed",
       "policy v5" in str(pd.read_excel(LD.find(target, "kpi_monthly"), header=None).iloc[0, 0]))
    pb = pd.read_excel(LD.find(target, "price_book"), header=None)
    ok("realism: the price book is approved before its effective dates", "3 December 2025" in str(pb.iloc[-1, 0]) and
       "2026-01-01" in pb.to_string())
    # the calendar index and the excess are not a generator setting in sight: no two years share the autumn ratio
    ok("realism: the calendar pattern differs year by year", yr.round(2).nunique() == len(yr))
    print("checks: %d assertions, %d failed" % (N[0], len(FAIL)))
    for f in FAIL:
        print("FAIL", f)
    sys.exit(1 if FAIL else 0)


def _kpi(target):
    k = pd.read_excel(LD.find(target, "kpi_monthly"), header=2)
    return k.values.tolist()


def _credits_reissued(raw):
    cn = raw[raw["line_type"] == "Credit note"]
    good = 0
    for r in cn.itertuples():
        orig = raw[raw["line_id"] == r.credits_line_id].iloc[0]
        re_ = raw[(raw["billing_account"] == orig["billing_account"]) & (raw["service_start"] == orig["service_start"])
                  & (raw["line_type"] == orig["line_type"]) & (raw["line_id"] > r.line_id)]
        good += len(re_) >= 1
    return len(cn) > 10 and good == len(cn)


def _failed_paid(ft):
    f = ft[ft["status"] != "paid"][["team_account", "period_start"]]
    p = ft[ft["status"] == "paid"][["team_account", "period_start"]]
    m = f.merge(p, how="left", indicator=True)
    return len(f) > 1000 and (m["_merge"] == "both").all()


def _max_date(path):
    df = pd.read_csv(path)
    dcols = [c for c in df.columns if c.endswith("_date") or c in ("submitted", "invoice_date", "snapshot_date")]
    return max(pd.to_datetime(df[c]).max().date() for c in dcols)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
