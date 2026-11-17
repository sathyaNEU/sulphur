"""task1 architecture 6: the build's assertions, run on the cut pack (target/), the goldens and the two json files.

    python3 task1/generator/checks.py

The bar block (labels R1 to R7), every row of the design note's fork table (SF1 to SF18), the pinning list, the
pack against the simulation it was written from, mess neutrality, the forcing on both sides, the realism sweep,
the input gates and the goldens. It rebuilds the pack once into a scratch folder (the byte-identical check, and
the account order the array comparison needs)."""
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import core as C  # noqa: E402
import analysis as A  # noqa: E402
import build as BD  # noqa: E402
import deliver  # noqa: E402
import docs as D  # noqa: E402
import pack as P  # noqa: E402
import results as RS  # noqa: E402
import effort as EF  # noqa: E402

T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
N = {"pass": 0, "fail": 0}
MEM = C.MEMBERS


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def digest(folder):
    h = hashlib.sha256()
    for name in sorted(os.listdir(folder)):
        h.update(name.encode())
        h.update(open(os.path.join(folder, name), "rb").read())
    return h.hexdigest()[:16]


def pdf_texts(path):
    from pypdf import PdfReader
    a = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    b = "\n".join(p.extract_text() for p in PdfReader(path).pages)
    return [" ".join(x.split()) for x in (a, b)]


def in_band(fid, x, fig):
    lo, hi = fig["figure_band"][fid]
    v = x * RS.unit(fid)[0]
    return lo - 1e-9 <= v <= hi + 1e-9


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    eff = json.load(open(os.path.join(HERE, "effort.json")))
    f = lambda k: os.path.join(T, P.FILES[k] if k in P.FILES else D.FILES[k])

    # ------------------------------------------------------------------------------------------------------------
    # the pack rebuilt once: byte-identical, and the simulation it was written from
    # ------------------------------------------------------------------------------------------------------------
    tmp = tempfile.mkdtemp(prefix="task1-checks-")
    out = BD.build(os.path.join(tmp, "target"))
    ok("rebuild: a second build of the pack is byte-identical", digest(os.path.join(tmp, "target")) == digest(T))
    W, aid = out["W"], out["aid"]
    Oc = C.Obs(W)
    core_gold = C.route(Oc)
    X, fig2, eff2, spec = RS.run(T)
    O, g, fam, lat, direct = X["O"], X["golden"], X["family"], X["lattice"], X["direct"]
    ok("figures.json is what the cut pack computes", json.loads(json.dumps(fig2, sort_keys=True, default=float)) == fig)
    ok("effort.json is what the cut pack computes", json.loads(json.dumps(eff2, default=float)) == eff)

    # ------------------------------------------------------------------------------------------------------------
    # R1: the field's raw material ships, and the golden reads it
    # ------------------------------------------------------------------------------------------------------------
    ids = np.array([int(x[3:], 16) for x in O.account_id])
    order = np.argsort(aid)
    pos = order[np.searchsorted(aid[order], ids)]
    ok("R1 every consumer account of the simulation is an account row", bool((aid[pos] == ids).all()) and O.n == Oc.n)
    for k in ("week", "day", "country", "ios", "cv", "label", "pool", "web", "last_open", "rec", "rec_a0", "n_rec", "auto_on",
              "plan_seen", "trial_seen", "netm", "neta", "mature"):
        ok("R1 the files give back the simulation's %s, account by account" % k,
           bool(np.array_equal(getattr(O, k), getattr(Oc, k)[pos])))
    ok("R1 the tracking answer on file is the simulation's on every iOS account",
       bool(np.array_equal(O.consent[O.ios], Oc.consent[pos][O.ios])) and not O.consent[~O.ios].any())
    for c in C.ORDER:
        ok("R1 %s: weekly installs, budgets and spend read back from the files" % c,
           bool(np.array_equal(O.agg[c], Oc.agg[c]) and np.array_equal(O.B[c]["budget"], Oc.B[c]["budget"])
                and np.array_equal(O.B[c]["spend"], Oc.B[c]["spend"]))
           and (c not in C.GATED or bool(np.array_equal(O.agg_cv[c], Oc.agg_cv[c]))))
    for pl, name in ((0, "Google Play"), (1, "App Store")):
        ok("R1 %s's report holds the simulation's charges (totals equal; the App Store's on Pacific days)" % name,
           all(abs(O.store[pl][k].sum() - Oc.store[pl][k].sum()) < 0.5 for k in ("first", "ren", "ann"))
           and (pl == 1 or all(np.array_equal(O.store[0][k], Oc.store[0][k]) for k in ("first", "ren", "ann"))))
    worst = max(abs(g[c][k] / core_gold[c][k] - 1) for c in C.ORDER for k in ("roas", "roas_s", "vpi", "marginal", "unrec"))
    ok("R1 the golden on the files is the core's golden on the simulation (worst figure %.5f apart)" % worst, worst < 2e-3)
    ok("R1 the call on the files is the core's call", RS.call_of(g) == RS.call_of(core_gold) == fig["call"])
    heads = {}
    for k in P.FILES:
        with open(f(k), newline="") as fh:
            heads[k] = next(csv.reader(fh))
    banned = re.compile(r"return|roas|ltv|value_per|per_install|dormant|silent|lapsed|inventory|auction|deliver|pacing|true_|band|rank|"
                        r"score|unattributed|predicted|expected", re.I)
    hits = [(k, h) for k, hs in heads.items() for h in hs if banned.search(h)]
    ok("R1 no shipped column holds a result or is named for a stump", not hits, hits)
    ok("R1 the accounts file has no column for a person's traits, the wide inventory or an unnamed install's source",
       heads["acc"] == ["account_id", "created_at", "platform", "storefront", "account_type", "tracking_status",
                        "conversion_value_48h", "last_open_at", "sub_state_at_last_open", "sub_store_at_last_open",
                        "sub_plan_at_last_open", "auto_renew_at_last_open"])
    ok("R1 the postbacks carry no account", "account_id" not in heads["skan"] and "install_id" not in heads["skan"])
    ok("R1 the stores' reports carry no account", "account_id" not in heads["apple"] + heads["google"])

    # ------------------------------------------------------------------------------------------------------------
    # R2: every piece of the files' mess is real and neutral (the golden with that item left unhandled)
    # ------------------------------------------------------------------------------------------------------------
    gf = C.figure_values(g)
    SLIPS = [("staff", "staff and test accounts kept as installs (%d accounts)" % (O.rows["accounts"] - O.n)),
             ("web_dup", "a re-sent checkout row summed twice (%d rows)" % O.rows["billing_twice"]),
             ("refund", "refunded purchases kept as revenue (%d purchases)" % O.rows["refunds"]),
             ("resent", "the export's re-sent rows counted as installs"),
             ("reinstall", "reinstalls counted as installs"),
             ("redownload", "redownload postbacks counted as installs"),
             ("dup_postback", "a postback delivered twice counted twice")]
    for slip, name in SLIPS:
        r = C.route(A.PackObs(T, slip=slip))
        fv = C.figure_values(r)
        outside = [fid for fid in fig["figure"] if not in_band(fid, fv[fid], fig)]
        move = max(abs(fv[fid] / gf[fid] - 1) for fid in fig["figure"])
        ok("R2 %s: the call stands and every graded figure stays in its band (largest move %.2f per cent)" % (name, 100 * move),
           RS.call_of(r) == fig["call"] and not outside, outside)
    names = [n for n, _r in fam]
    for conv in ("the App Store's report days taken as UTC days", "a postback's install four days before it arrived",
                 "the stores' refunds netted on the day of the refund", "the stores' refunds netted from their renewals",
                 "stores and records compared by calendar month",
                 "the 365 days and the install week counted from the attribution export's install time"):
        r = dict(fam)[conv]
        fv = C.figure_values(r)
        ok("R2 %s: same call, largest return move %.2f per cent" % (conv, 100 * max(abs(r[c]["roas"] / g[c]["roas"] - 1) for c in MEM)),
           conv in names and RS.call_of(r) == fig["call"] and all(in_band(fid, fv[fid], fig) for fid in fig["figure"]))

    # ------------------------------------------------------------------------------------------------------------
    # R3: each result's hurried figure, outside its band
    # ------------------------------------------------------------------------------------------------------------
    by = {r["id"]: r for r in eff["results"]}
    reflex = C.figure_values(lat["S1+S2+S3"])
    own = {"S1": ["unrecorded share AppLovin Android"], "S2": ["value per install Meta iOS", "plan revenue iOS networks"],
           "S3": ["next euro Meta iOS", "next euro Google Android"]}

    def gap(fid, x):
        lo, hi = fig["figure_band"][fid]
        v = x * RS.unit(fid)[0]
        return max(lo - v, v - hi) / max(abs(fig["figure"][fid]), 1e-9)
    for s, fids in own.items():
        fv = C.figure_values(lat[s])
        for fid in fids:
            ok("R3 %s lost alone files %s at %s, outside %s by %.1f per cent of the figure" % (
                s, fid, RS.stated(fid, fv[fid]), fig["figure_band"][fid], 100 * gap(fid, fv[fid])), gap(fid, fv[fid]) > 0.02)
    ok("R3 the reflex route's AppLovin Android share is %.1f per cent against %.1f" % (
        100 * reflex["unrecorded share AppLovin Android"], fig["unrecorded_share_applovin_android_pct"]),
       gap("unrecorded share AppLovin Android", reflex["unrecorded share AppLovin Android"]) > 0.3)
    ok("R3 the reflex route's Meta iOS value per install is %.2f against %.2f" % (
        reflex["value per install Meta iOS"], fig["value_per_install_meta_ios"]),
       gap("value per install Meta iOS", reflex["value per install Meta iOS"]) > 0.1)
    for nm, lim in (("return ", 0), ("stretch return ", 0), ("value at plan ", 0), ("next euro ", 1)):
        inside = [c for c in MEM if in_band(nm + c, reflex[nm + c], fig)]
        ok("R3 the reflex route lands %d of 7 of '%s' inside the bands" % (len(inside), nm.strip()), len(inside) <= lim, inside)
    ok("R3 the reflex route's two revenue figures are outside their bands",
       not in_band("plan revenue iOS networks", reflex["plan revenue iOS networks"], fig)
       and not in_band("stretch adds", reflex["stretch adds"], fig))
    ok("R3 the reflex route files Meta iOS scale and both Android channels cut",
       [C.band(lat["S1+S2+S3"][c]["roas"]) for c in ("Meta iOS", "Google Android", "AppLovin Android")] == ["scale", "cut", "cut"])
    for s, c, b in (("S1", "AppLovin Android", "cut"), ("S2", "Meta iOS", "scale"), ("S3", "Google Android", "cut")):
        wrong = [m for m in MEM if C.band(lat[s][m]["roas"]) != fig["bands"][m]]
        ok("R3 %s lost alone moves %s to %s and no other channel" % (s, c, b), wrong == [c] and C.band(lat[s][c]["roas"]) == b, wrong)
    ok("R3 the seven shortcut routes file seven different wrong calls", fig["distinct_wrong_calls"] == 7)
    ok("R3 the records as they stand cut all seven channels", all(C.band(direct[c]["roas"]) == "cut" for c in MEM))
    for rid, gr in zip(("R1", "R2", "R3", "R4", "R5", "R6", "R7"), ("missed", "missed", "partly", "missed", "missed", "missed", "missed")):
        ok("R3 effort.json grades the careful pass %s on %s" % (gr, rid), EF.grade(by[rid]["passes"]["careful"], by[rid])[0] == gr)

    # ------------------------------------------------------------------------------------------------------------
    # R4: no plant
    # ------------------------------------------------------------------------------------------------------------
    for k in ("acc", "bill", "attr", "skan", "spend", "apple", "google"):
        d = pd.read_csv(f(k), dtype=str, keep_default_na=False)
        ok("R4 %s: no row is a copy of another" % P.FILES[k], not d.duplicated().any(), int(d.duplicated().sum()))
        if k == "spend":
            blk = d.drop(columns=["date"]).astype(str).agg("|".join, axis=1)
            day = d.groupby("date").apply(lambda x: "#".join(blk[x.index]), include_groups=False)
            ok("R4 no day of ad spend repeats another day's rows", day.is_unique)
    texts = {}
    pol_a, pol_b = pdf_texts(f("policy"))
    texts["policy"] = pol_a
    for k in ("plan", "budget"):
        wb = load_workbook(f(k))
        texts[k] = " | ".join(str(c.value) for ws in wb for row in ws.iter_rows() for c in row if isinstance(c.value, str))
        ok("R4 %s has no hidden sheet and no comment" % D.FILES[k],
           all(ws.sheet_state == "visible" for ws in wb) and not any(c.comment for ws in wb for row in ws.iter_rows() for c in row))
    texts["schema"] = open(f("schema")).read()
    cells = [x for k in ("plan", "budget") for x in texts[k].split(" | ")] + re.split(r"(?<=[.;]) ", texts["policy"])
    placed = [x for x in cells if any(c in x for c in C.ORDER) and re.search(r"\b(scale|hold|cut)\b", x, re.I)
              and not x.startswith("1.2 ")]
    ok("R4 no shipped sentence or cell places a channel in a band", not placed, placed[:3])
    stated = ["%.2f" % fig["return_plan"][c] for c in MEM]
    ok("R4 no document states a channel's return", not any(re.search(r"return[^.|]{0,60}\b%s\b" % re.escape(x), t)
                                                         for x in stated for t in texts.values()))
    ok("R4 the pack holds no memo, draft or prior analysis", not any(re.search(r"memo|draft_|analysis|review|ltv|roas", n, re.I)
                                                                     for n in os.listdir(T)))

    # ------------------------------------------------------------------------------------------------------------
    # R5: no one thing: each factor across the data, and none rescuing more than a third alone
    # ------------------------------------------------------------------------------------------------------------
    ch = fig["channels"]
    ok("R5 the records lack 10 per cent or more of every channel's twelve-month revenue (%.1f to %.1f per cent)" % (
        min(x["unrecorded_pct"] for x in ch.values()), max(x["unrecorded_pct"] for x in ch.values())),
       all(x["unrecorded_pct"] >= 10 for x in ch.values()) and len(ch) == 8)
    org = (O.label == len(C.ORDER) + 1) & O.mature
    ok("R5 organic Android installs lack their share too", 1 - C.values(O, "raw")[org].sum() / X["v"][org].sum() > 0.10)
    shares = []
    for ci, c in enumerate(C.ORDER):
        if C.CH[c]["ios"]:
            lab = (O.label == ci) & O.mature
            shares.append(float(lab.sum() / O.agg[c][:C.MATURE].sum()) if c in C.GATED else float(O.consent[lab].mean()))
    ok("R5 every iOS source has 20 to 35 per cent of its installs allowing tracking (%.3f to %.3f)" % (min(shares), max(shares)),
       len(shares) == 6 and 0.20 < min(shares) and max(shares) < 0.35)
    asa = (O.label == C.ORDER.index("Apple Search Ads")) & O.mature
    ok("R5 on Apple Search Ads the installs that allowed tracking are worth more than the rest (%.2f against %.2f)" % (
        X["v"][asa & O.consent].mean(), X["v"][asa & ~O.consent].mean()),
       X["v"][asa & O.consent].mean() > 1.5 * X["v"][asa & ~O.consent].mean())
    ok("R5 every iOS network's named installs are worth more than its installs as a whole",
       all(ch[c]["named_value"] > 1.3 * ch[c]["value_per_install"] for c in C.GATED))
    sd = {c: float(np.std(np.log(O.B[c]["spend"] / O.B[c]["budget"]))) for c in C.ORDER}
    ok("R5 the share of the budget spent moves week to week on all eight channels (sd of the log %.2f to %.2f)" % (
        min(sd.values()), max(sd.values())), min(sd.values()) > 0.05)
    ok("R5 fitted on spend, installs respond more steeply than on the budget on all eight channels",
       all(ch[c]["spend_elasticity"] > ch[c]["budget_elasticity"] + 0.1 for c in C.ORDER))
    for j in eff["factorial"]["judgments"]:
        if j["kind"] == "stump":
            ok("R5 %s fixed alone on the reflex route rescues %d of 7 results and leaves the call wrong" % (
                j["id"], len(j["alone"]["results_rescued"])),
               len(j["alone"]["results_rescued"]) <= 2 and j["alone"]["answer"] != fig["call"]
               and j["dropped"]["answer"] != fig["call"])

    # ------------------------------------------------------------------------------------------------------------
    # R6: the one-fact test, computed
    # ------------------------------------------------------------------------------------------------------------
    alone = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
    for h, s in zip(eff["hints"], ("S1", "S2", "S3")):
        v = RS.result_values({fid: RS.stated(fid, x) for fid, x in C.figure_values(lat[alone[s]]).items() if fid in fig["figure"]},
                             RS.call_of(lat[alone[s]]))
        got = [rid for rid in by if EF.grade(v[rid], by[rid])[0] == "right"]
        ok("R6 the %s sentence, executed on the reflex route, rescues %s" % (s, got or "no whole result"),
           got == h["rescues"] and len(got) <= 2)
    ok("R6 corelib on the cut pack: no sentence rescues more than a third of the rubric",
       max(fig["rubric"]["fixed_alone"].values()) <= 100 / 3.0)

    # ------------------------------------------------------------------------------------------------------------
    # R7: the rivals, and the forcing on both sides
    # ------------------------------------------------------------------------------------------------------------
    ok("R7 the battery holds %d variants beside the golden" % len(fam), len(fam) >= 180 and len(set(names)) == len(fam))
    ok("R7 the battery carries every way under each of the three as-fitted carries, and the ways the judge's second pass ran",
       all(any(n.startswith(w) for n in names) for w in A.NEW_WAYS)
       and all(sum(1 for n in names if tag in n) >= len(A.WAYS) for tag in ("two-year ratio", "mean log", "averaged over its weeks")))
    e0 = A.route_x(X["O"], **A.EST)
    ok("R7 the battery's own carry of the response reproduces the golden route",
       max(abs(e0[c][k] / g[c][k] - 1) for c in MEM for k in ("roas", "roas_s", "vpi", "marginal", "revenue", "revenue_s")) < 1e-9)
    for n, r in fam:
        fv = C.figure_values(r)
        outside = [fid for fid in fig["figure"] if not in_band(fid, fv[fid], fig)]
        ok("R7 %s: the golden call, every graded figure in its band" % n, RS.call_of(r) == fig["call"] and not outside, outside)
    near = min(abs(r[c]["roas"] - l) for _n, r in fam + [("golden", g)] for c in MEM for l in C.LINES)
    ok("R7 no variant brings a channel within 0.05 of a line (nearest %.3f)" % near, near >= 0.05)
    # the ways a figure from the shipped files refutes: each files the golden call, and its refuting figure stands
    ro = {}
    for r in fig["ruled_out"]:
        ro.setdefault(r["by"], []).append(r)
        ok("R7 refuted, %s: it still files the golden call" % r["name"], r["call_holds"])
    ok("R7 five kinds of refuted rival on file", sorted(ro) == ["Apple Search Ads", "Apple Search Ads by sessions",
                                                                "annual first charges", "media plan", "moved weeks"])
    sg = ro["Apple Search Ads by sessions"][0]["groups"]
    ok("R7 Apple Search Ads' ratio as one number is refuted by its own trial starters: %.2f against %.2f paid in the lower "
       "session buckets, %.2f against %.2f in the upper" % (sg["lower"]["priced"], sg["lower"]["paid"], sg["upper"]["priced"],
                                                           sg["upper"]["paid"]),
       sg["lower"]["priced"] > 1.08 * sg["lower"]["paid"] and sg["upper"]["priced"] < 0.95 * sg["upper"]["paid"]
       and min(sg["lower"]["installs"], sg["upper"]["installs"]) >= 1000)
    bl = ro["media plan"][0]["blocks"]
    ok("R7 a week's month from its Monday is refuted by the plan: %d changes of weekly spend, all on the first week whose "
       "Thursday is in a new month, %d of them with the Monday still in the old month" % (bl["changes"], bl["apart_on_thursday"]),
       bl["changes"] >= 8 and bl["changes"] == bl["on_thursday_months"] and bl["off"] == 0 and bl["apart_on_thursday"] >= 3
       and bl["apart_on_monday"] == 0)
    ho = ro["moved weeks"][0]["holdout"]
    ok("R7 the equations in levels are refuted by the moved weeks: %s per cent off over %d weeks, the logs the lower on %d of "
       "%d channels" % (ho["error_pct"], ho["weeks"], ho["lower_on"], ho["channels"]),
       ho["lower_on"] == ho["channels"] and min(ho["error_pct"]["levels"], ho["error_pct"]["semilog"]) >= 1.5 * ho["error_pct"]["log"])
    sa = ro["Apple Search Ads"][0]["search_ads"]
    est = fig["check_search_ads"]["estimate"]
    ok("R7 one price ratio is refuted on Apple Search Ads' unnamed installs: %.2f against %.2f paid, the ratio by value %.2f"
       % (sa["priced"], sa["paid"], est), abs(sa["priced"] - sa["paid"]) >= 3 * abs(est - sa["paid"]))
    an = ro["annual first charges"][0]
    ok("R7 leaving the annual trials out is refuted by the stores' annual first charges beyond the records %s, and files "
       "the unrecorded share at %.1f, outside its band" % (an["annual"]["excess"], an["unrecorded_share"]),
       min(an["annual"]["excess"].values()) >= 500 and "unrecorded share AppLovin Android" in an["outside"])
    for sid, d in fig["shortcut_conventions"].items():
        ok("R7 the %s shortcut keeps %s in the wrong band under %d ways of carrying the response (%.2f to %.2f)" % (
            sid, d["member"], d["conventions"], d["low"], d["high"]),
           len(d["band"]) == 1 and d["band"][0] != d["golden_band"] and d["conventions"] >= 6)
    ok("realism: every account's first attribution row is at or before its created_at day", bool((X["O"].inst_day <= X["O"].day).all()))
    ck = fig["clock_install_time"]
    ok("R7 the 365 days counted from the attribution export's install time: the call and every return to two decimals",
       ck["call_holds"] and all(round(ck["returns"][c], 2) == fig["return_plan"][c] for c in MEM), ck["returns"])
    for p in fig["perturbations"]:
        ok("R7 %s: the call holds (nearest line %.3f away)" % (p["input"], p["nearest"]), p["call_holds"])
    for rid in ("R3", "R4", "R5", "R6"):
        w = max((hi - lo) / abs(by[rid]["golden"][k]) for k, (lo, hi) in by[rid]["bands"].items())
        ok("R7 %s: no band wider than %.0f per cent of its figure" % (rid, 100 * w), w < 0.35)
    ok("R7 corelib on the cut pack: level 5, no failure", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], fig["rubric"]["fails"])
    ok("R7 the rubric on the cut pack: one stump lost %s, the reflex route %.1f" % (fig["rubric"]["one_lost"], fig["rubric"]["reflex"]),
       max(fig["rubric"]["one_lost"].values()) <= 50 and fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50)
    for s, r in X["refs"].items():
        ge = abs(r["golden"] - r["truth"])
        worst_rival = min(abs(x - r["truth"]) for x in r["rivals"].values())
        ok("R7 the %s referee: the golden %.2f from the record's %.2f, the nearest shortcut %.1f times further" % (
            s, r["golden"], r["truth"], worst_rival / ge), worst_rival > 3 * ge)
    T0 = C.truth_at_plan()
    ok("R7 the golden call is the world's own on all seven channels",
       all(C.band(T0[c]["roas"]) == fig["bands"][c] for c in MEM))
    ok("R7 every golden return is within 5 per cent of the world's own",
       max(abs(g[c]["roas"] / T0[c]["roas"] - 1) for c in MEM) < 0.05)

    # ------------------------------------------------------------------------------------------------------------
    # the fork table, row by row
    # ------------------------------------------------------------------------------------------------------------
    both = lambda s: s in pol_a and s in pol_b
    acc = pd.read_csv(f("acc"), dtype=str, keep_default_na=False)
    att = pd.read_csv(f("attr"), dtype=str, keep_default_na=False)
    bil = pd.read_csv(f("bill"), dtype=str, keep_default_na=False)
    cons = set(acc.account_id[acc.account_type == "consumer"])
    firsts = att[(att.is_reinstall == "false")].drop_duplicates("install_id")
    ok("SF1 policy 2.2 files what an install is, and every consumer account has one first install on file",
       both("An install is the first install of a new consumer account. A second device, a reinstall, a staff account and "
            "a test account are not installs.")
       and firsts.account_id[firsts.account_id.isin(cons)].is_unique and set(firsts.account_id) >= cons)
    spend = pd.read_csv(f("spend"), dtype=str, keep_default_na=False)
    rep = spend.assign(n=spend.installs_reported_by_network.astype(int)).groupby(["network", "os"]).n.sum()
    over = {c: rep[P.SOURCE[c]] / O.agg[c].sum() for c in C.ORDER}
    ok("SF2 policy 2.2 gives each install to at most one channel whether or not the partner can name it; the networks' own "
       "counts run above the installs on every growth channel (%.2f to %.2f times)" % (min(over[c] for c in MEM), max(over.values())),
       both("Each install is bought by at most one channel, the one whose ad drove it, whether or not the attribution "
            "partner can name it") and all(over[c] > 1.01 for c in MEM)
       and sum(rep[P.SOURCE[c]] for c in C.ORDER) > 1.05 * sum(O.agg[c].sum() for c in C.ORDER))
    ok("SF3 policy 2.3 files the 365 days and every charge the stores or the checkout made",
       both("every charge the App Store, Google Play or the web checkout made on its account in the 365 days from the install"))
    ap = pd.read_csv(f("apple"), dtype=str, keep_default_na=False)
    vat = ap.storefront.map(dict(zip(P.COUNTRIES, C.VAT)))
    ok("SF4 policy 2.4 files VAT by storefront, 15 and 3 per cent, and the App Store's proceeds agree with it",
       both("Spain 21 per cent, Italy 22 per cent, Portugal 23 per cent") and both("commission of 15 per cent")
       and both("fee of 3 per cent")
       and bool((abs(ap.developer_proceeds_eur.astype(float) - ap.customer_price_eur.astype(float) / (1 + vat) * 0.85) < 0.006).all()))
    ok("SF5 policy 2.1 files the return as the period's revenue over the period's spend",
       both("per euro of that spend. For a plan year the period is the plan's 52 weeks and the spend is the plan's weekly "
            "spend on the channel"))
    wp = load_workbook(f("plan"), read_only=True, data_only=True)
    st = list(wp["Stretch case"].iter_rows(values_only=True))
    ok("SF6 the plan gives a stretch spend beside each of the 52 weeks for each growth channel",
       [x for x in st[3] if x in MEM] == MEM and len([r for r in st[4:56] if r[0] is not None]) == 52
       and all(len(O.stretch[c]) == 52 and (O.stretch[c] > O.plan[c]).all() for c in MEM))
    ok("SF7 policy 2.6 files the marginal return at a stated spend, every week raised in the same proportion",
       both("one more euro of spend returns at that spend, every week of the period raised in the same proportion"))
    ok("SF8 policy 2.1 and 2.3 make the revenue per install the installs' revenue over the installs a period's spend buys",
       both("the 12-month net revenue of the installs the period's spend on the channel buys"))
    ok("SF9 section 3 files the lines: scale from 1.20, hold from 0.90, cut under it",
       both("scale when the return is 1.20 or more, hold when it is 0.90 or more and under 1.20, and cut when it is under 0.90")
       and tuple(C.LINES) == (0.90, 1.20) and fig["policy"]["lines"] == [0.90, 1.20])
    gsheet = list(wp["Growth channels"].iter_rows(values_only=True))
    ok("SF10 the plan's growth sheet holds the seven channels placed, Apple Search Ads sits on the brand sheet",
       [x for x in gsheet[3] if x in C.ORDER] == MEM and list(O.brand) == ["Apple Search Ads"]
       and both("The channels placed are the channels of the media plan's growth sheet"))
    bt, br = A.secs(bil.transaction_at), A.secs(bil.recorded_at)
    late = (br - bt)[(bil.store != "web").to_numpy()] > 3 * 86400
    ok("SF11 a charge carries its transaction time, recorded no earlier (%.0f per cent of store charges recorded three days "
       "or more later)" % (100 * late.mean()), both("each at the time of the transaction") and bool((br >= bt).all())
       and late.mean() > 0.02)
    refs = bil[bil.event_type == "refund"]
    ok("SF12 policy 2.3 nets refunds, and every refund on file points at a charge on file (%d purchases)" % refs.refund_of_event_id.nunique(),
       both("less the net revenue of any of those charges refunded") and set(refs.refund_of_event_id) <= set(bil.event_id)
       and bool((refs.amount_eur.astype(float) < 0).all()))
    fd = dict(fam)
    ok("SF13 same call: the launch quarter left out and the last 78 weeks",
       all(RS.call_of(fd[n]) == fig["call"] for n in ("installs response without the launch quarter",
                                                     "installs response on the last 78 weeks")))
    ok("SF14 same call: the delivery share from the mature weeks", RS.call_of(fd["delivery share from the mature weeks"]) == fig["call"])
    a2 = acc.set_index("account_id")
    org_rows = firsts[(firsts.media_source == "organic") & (firsts.platform == "ios") & firsts.account_id.isin(cons)]
    ratio = {c: O.agg[c][:C.MATURE].sum() / ((O.label == C.ORDER.index(c)) & O.mature).sum() for c in C.GATED}
    ok("SF15 the export gives the organic label on iOS only to accounts that allowed tracking, and each network's postbacks "
       "outnumber its named installs (%.1f to %.1f times)" % (min(ratio.values()), max(ratio.values())),
       bool((a2.tracking_status.reindex(org_rows.account_id) == "authorized").all()) and min(ratio.values()) > 3)
    sch = json.load(open(f("schema")))
    four = fd["a postback's install four days before it arrived"]
    mv4 = max(abs(four[c]["roas"] / g[c]["roas"] - 1) for c in MEM)
    lag = (O._pb["day"].min(), )
    ok("SF16 the schema files a 48-hour window and a postback 24 to 48 hours after it; four days back is the same call "
       "(largest return move %.1f per cent)" % (100 * mv4),
       sch["postback"]["measurement_window_hours"] == 48 and sch["postback"]["sent_after_window_closes_hours"] == [24, 48]
       and RS.call_of(four) == fig["call"] and mv4 < 0.015 and lag[0] >= 3)
    ok("SF17 same call: the first-48-hour values in eight groups, four groups, cells of fifty, one tilt per source",
       all(RS.call_of(fd[n]) == fig["call"] for n in ("first-48-hour cells in eight groups", "first-48-hour cells in four groups",
                                                     "cells of fifty or more", "each source's consenting installs through one tilt")))
    ok("SF18 the 52 mature weeks have their 365 days on file by 8 November 2026",
       (C.MATURE * 7 - 1) + 365 <= C.END_DAY and int(O.day[O.mature].max()) + 365 <= C.END_DAY
       and A.secs(bil.transaction_at).max() // 86400 == C.END_DAY)

    ok("SF19 same call: stores and records compared by calendar month, alone and with one fit across both stores",
       all(RS.call_of(fd[n]) == fig["call"] for n in ("stores and records compared by calendar month",
                                                     "calendar months, one fit across both stores")))
    ok("SF20 the App Store report's day column is date_pt, and reading its days as UTC is the same call",
       heads["apple"][0] == "date_pt" and heads["google"][0] == "date_utc"
       and RS.call_of(fd["the App Store's report days taken as UTC days"]) == fig["call"])
    ok("SF21 same call: the stores' refunds netted on the day of the refund, or from the renewals",
       all(RS.call_of(fd[n]) == fig["call"] for n in ("the stores' refunds netted on the day of the refund",
                                                     "the stores' refunds netted from their renewals")))
    rod = {r["name"]: r for r in fig["ruled_out"]}
    ok("SF22 a week's month: the plan's blocks follow the Thursday, and the Monday reading files the same call",
       rod[A.MONTH_VARIANT]["call_holds"] and rod[A.MONTH_VARIANT]["blocks"]["off"] == 0)
    lit = lambda nm: A.LIT_NAME + ("; " + nm if nm else "")
    same = lambda *names: all(RS.call_of(fd[n]) == fig["call"] for n in names)
    ok("SF23 same call: the 365 days and the install week counted from the attribution export's install time",
       same("the 365 days and the install week counted from the attribution export's install time"))
    ok("SF24 same call: the annual trials at the monthly trials' share, the two rates fitted together",
       same("the annual trials at the monthly trials' share", "the trial-end share and the continuation fitted together"))
    ok("SF25 same call: the first-48-hour values by the sessions bucket alone, by the trial and purchase bits alone",
       same("first-48-hour values by the sessions bucket alone", "first-48-hour values by the trial and purchase bits alone"))
    ok("SF26 same call: Apple Search Ads in or out of the shared month pattern",
       same("the month pattern of the plan's seven channels, Apple Search Ads left out of the fit", lit("Apple Search Ads in the month pattern")))
    ok("SF27 same call: the equations carried as fitted, with the smearing factor, the share at its mean log or its weekly average",
       same(lit(""), lit("the smearing factor"), lit("the share spent at its mean log"), lit("the share spent averaged over its weeks"),
            lit("the levels set to the history")))
    ok("SF28 same call: a trend, a second-year level, installs fitted on the 52 complete weeks",
       same("a trend in the installs equation, held at its mid-history level", "a second-year level in the installs equation, carried",
            "installs response on the 52 complete weeks"))
    ok("SF29 the equations in levels or in levels on the logs file the same call and are refuted by the moved weeks",
       all(r["call_holds"] for r in fig["ruled_out"] if r["by"] == "moved weeks"))
    ok("SF30 one price ratio, Apple Search Ads' ratio as one number and the annual trials left out file the same call and "
       "are refuted by the files",
       all(r["call_holds"] for r in fig["ruled_out"]
           if r["by"] in ("Apple Search Ads", "Apple Search Ads by sessions", "annual first charges")))
    carried = lambda *names: same(*names) and all(same(cn + "; " + n) for cn, _k in A.AS_FITTED for n in names)
    ok("SF31 same call: a floor of fifty on a first-48-hour value, or every value on its own installs, under every carry",
       carried("cells of fifty or more", "every first-48-hour value on its own installs, however few")
       and fig["steps"]["thin_cell"] == 20)
    ok("SF32 same call: Apple Search Ads' ratio by two groups of the value or value by value, under every carry",
       carried("non-consenting installs at Apple Search Ads' ratio", "non-consenting installs at Apple Search Ads' ratio, value by value",
               "non-consenting installs at Apple Search Ads' ratio, value by value, every value on its own installs"))
    ok("SF33 same call: the delivery share from the complete weeks or from the last 52 weeks, under every carry",
       carried("delivery share from the mature weeks", "the delivery share of the last 52 weeks"))

    # ------------------------------------------------------------------------------------------------------------
    # the pinning list: each constant in its home
    # ------------------------------------------------------------------------------------------------------------
    ok("pin: the policy's text reads the same through two extractors on every filed sentence",
       all(both(s) for s in ("EUR 9.99 a month and EUR 59.99 a year, each with a seven-day free trial",
                             "1.20 or more", "under 0.90", "Version 3 adds the web checkout")))
    prod = bil[bil.environment == "production"]
    ok("pin: the billing events' own prices are 9.99 and 59.99",
       set(prod.amount_eur.astype(float).abs().round(2)) == {9.99, 59.99} == {C.PRICE_M, C.PRICE_A})
    ok("pin: VAT, commission and fee in the policy are the values the golden uses",
       tuple(C.VAT) == (0.21, 0.22, 0.23) and C.COMMISSION == 0.15 and C.WEB_FEE == 0.03)
    for name, good in A.plan_checks(O):
        ok("pin: the workbook's %s is what the analysis reads" % name, good)
    ok("pin: the schema's first-48-hour value has 32 values, on the accounts and on the postbacks",
       set(acc.conversion_value_48h.astype(int)) <= set(range(32)) and int(O._pb["cv"].max()) <= 31 and "5" in sch["fine_value_bits"]
       and sch["value_computed"]["platforms"] == ["ios", "android"] and "conversion_value" in heads["skan"])
    mon = prod[prod.product_id.str.endswith("monthly") & (prod.event_type != "refund")].drop_duplicates(
        ["account_id", "transaction_at"])
    gaps = (A.secs(mon.transaction_at) // 86400)
    gaps = pd.Series(gaps, index=mon.account_id.to_numpy()).sort_values().groupby(level=0).diff().dropna()
    ok("pin: the billing cadence measured on the events is a twelfth of a year (mean gap %.3f days)" % gaps.mean(),
       abs(gaps.mean() - C.MONTH_DAYS) < 0.02 and set(gaps.unique()) <= {30, 31})
    for name, key in (("Google Play", 0), ("App Store", 1)):
        s_ = fig["stores"][name]
        ok("pin: %s's fitted shares and continuation are the note's (%.3f, %.3f, %.3f)" % (
            name, s_["trial_end_share_monthly"], s_["trial_end_share_annual"], s_["continuation"]),
           (s_["trial_end_share_monthly"], s_["trial_end_share_annual"], s_["continuation"]) ==
           ((0.087, 0.105, 0.888) if key == 0 else (0.088, 0.108, 0.888)))
    ok("pin: the web checkout's own continuation is %.3f" % fig["web_continuation"], abs(fig["web_continuation"] - 0.892) < 0.0015)

    # ------------------------------------------------------------------------------------------------------------
    # what is never filed, and no file that describes the pack
    # ------------------------------------------------------------------------------------------------------------
    alltext = " ".join(texts.values()) + " " + " ".join(h for hs in heads.values() for h in hs)
    for word in ("dormant", "silent", "forgotten", "next open", "next sync", "next opened", "pacing", "underspend", "under-spend",
                 "auction", "delivery", "delivered", "worth more", "more engaged", "do not represent", "unattributed",
                 "what we control", "trust"):
        ok("never filed: '%s'" % word, word not in alltext.lower())
    ok("no file or sheet describes the pack",
       not any(re.search(r"readme|dictionary|data_dict|notes|manifest|field_|glossary|about", n, re.I) for n in os.listdir(T))
       and not any(re.search(r"readme|dictionary|notes|about|legend|definitions", ws.title, re.I)
                   for k in ("plan", "budget") for ws in load_workbook(f(k))))
    reasons = [r[5] for r in load_workbook(f("budget"), read_only=True)["Changes"].iter_rows(values_only=True)][1:]
    written = [x for x in reasons if x]
    ok("the budget sheet's reasons never name the platform's side (%d notes, %d distinct, %d rows left empty)" % (
        len(written), len(set(written)), len(reasons) - len(written)),
       not any(re.search(r"cpm|cpi|bid|compet|inventory|price|market|expensive|cheap|auction|deliver|pacing|perform",
                         x, re.I) for x in written)
       and len(set(written)) >= 40 and len(reasons) - len(written) >= 20
       and max(written.count(x) for x in set(written)) <= 0.12 * len(reasons))

    # ------------------------------------------------------------------------------------------------------------
    # the realism sweep
    # ------------------------------------------------------------------------------------------------------------
    def steps(vals):
        d = np.diff(np.sort(np.asarray(vals, dtype=np.int64)))
        return len(set(d[d > 0].tolist()))
    ok("realism: account ids are not a sequence", steps([int(x[3:], 16) for x in acc.account_id[:20000]]) > 1000)
    ok("realism: billing event ids are not a constant step", steps([int(x[2:]) for x in bil.event_id[:20000]]) > 5)
    ok("realism: install ids and postback ids are not sequences",
       steps([int(x, 16) for x in att.install_id[:20000]]) > 1000)
    ok("realism: campaign ids are not a constant step", steps(spend.campaign_id.unique().astype(np.int64)) > 20)
    ok("realism: account creation times have no fixed step", steps(A.secs(acc.created_at[:20000])) > 200)
    ok("realism: the channels are not listed in alphabetical order anywhere", list(C.ORDER) != sorted(C.ORDER) and MEM != sorted(MEM))
    shapes = {re.sub(r"[A-Za-z]+", "a", re.sub(r"\d+", "9", x)) for x in spend.campaign_name.unique()}
    ok("realism: campaign names take %d shapes" % len(shapes), len(shapes) > 4)
    by_ = [r[6] for r in load_workbook(f("budget"), read_only=True)["Changes"].iter_rows(values_only=True)][1:]
    ok("realism: the change log's authors and sizes are uneven", len(set(by_)) == 2 and
       max(by_.count(x) for x in set(by_)) > 3 * min(by_.count(x) for x in set(by_)))
    ok("realism: no channel spends the same amount in two weeks",
       all(len(set(np.round(O.B[c]["spend"], 2).tolist())) == C.WEEKS for c in C.ORDER))
    ok("realism: weekly budgets are rounded as a sheet kept by hand is, spend is to the cent",
       all((O.B[c]["budget"] % 10 == 0).all() for c in C.ORDER) and bool((spend.spend_eur.str.contains(r"\.\d\d$")).all()))
    cnt = acc.account_type.value_counts()
    ok("realism: staff and test accounts are a sliver of the accounts (%d and %d)" % (cnt["staff"], cnt["test"]),
       cnt["staff"] != cnt["test"] and cnt["staff"] + cnt["test"] < 0.001 * len(acc))
    ok("realism: the App Store's report is on Pacific days (its first-charge days differ from the records' UTC days)",
       not np.array_equal(O.store_bins(pt=False)[1]["first"], O.store_bins(pt=True)[1]["first"])
       or not np.array_equal(A.s1_fit(O, pt=False)[1]["F"], X["fits"][1]["F"]))

    # ------------------------------------------------------------------------------------------------------------
    # the input gates
    # ------------------------------------------------------------------------------------------------------------
    files = sorted(os.listdir(T))
    ok("gate: %d usable files in the pack" % len(files), len(files) >= 10 and not any(n.startswith((".", "~")) for n in files))
    ext = {os.path.splitext(n)[1] for n in files}
    ok("gate: spreadsheet, text and code categories (%s)" % ", ".join(sorted(ext)), {".csv", ".xlsx", ".pdf", ".json"} <= ext)
    big = {P.FILES[k]: n for k, n in O.rows.items() if k in P.FILES}
    rows = {n: sum(1 for _ in open(os.path.join(T, n))) - 1 for n in files if n.endswith(".csv")}
    ok("gate: two large CSVs (%s)" % ", ".join("%s %d" % (n, r) for n, r in rows.items() if r >= 20000),
       sum(r >= 20000 for r in rows.values()) >= 2 and sum(r >= 600 for r in rows.values()) >= 3)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    ok("gate: every shipped file has its source, date and licence in metadata.json, outside the pack",
       set(meta["files"]) == set(files) and all({"source", "pulled", "license"} <= set(v) for v in meta["files"].values())
       and "metadata.json" not in files)
    ok("gate: %d distractors, named only in metadata.json" % len(dis),
       len(dis) >= 2 and all(n in files for n in dis) and not any(re.search(r"distract|unused|decoy|extra", n, re.I) for n in files))
    lean = tempfile.mkdtemp(prefix="task1-lean-")
    for n in files:
        if n not in dis:
            os.symlink(os.path.join(T, n), os.path.join(lean, n))
    r = C.route(A.PackObs(lean))
    ok("gate: with the distractors deleted every figure is unchanged",
       all(r[c][k] == g[c][k] for c in C.ORDER for k in ("roas", "roas_s", "vpi", "marginal", "unrec")))
    shutil.rmtree(lean)
    ok("gate: cross-file work: no single file holds installs, charges and spend together",
       not ({"spend_eur", "amount_eur"} <= set(sum(heads.values(), []))) or
       not any({"spend_eur", "amount_eur"} <= set(h) for h in heads.values()))
    size = sum(os.path.getsize(os.path.join(T, n)) for n in files)
    ok("gate: the pack is %.0f MB unzipped" % (size / 1e6), size > 30e6)

    # ------------------------------------------------------------------------------------------------------------
    # the goldens and the blocks
    # ------------------------------------------------------------------------------------------------------------
    ok("golden: exactly the two requested files", sorted(os.listdir(G)) == sorted(deliver.FILES.values()))
    rows_ = list(csv.reader(open(os.path.join(G, deliver.FILES["csv"]))))
    order_ = deliver.order(fig)
    ok("golden CSV: one row per channel with the band and the four figures, as figures.json states them",
       [r_[0] for r_ in rows_[1:]] == order_ and all(
           r_[1] == fig["bands"][r_[0]] and float(r_[2]) == fig["return_plan"][r_[0]] and float(r_[3]) == fig["return_stretch"][r_[0]]
           and float(r_[4]) == fig["value_plan"][r_[0]] and float(r_[5]) == fig["next_euro"][r_[0]] for r_ in rows_[1:]))
    gw = load_workbook(os.path.join(G, deliver.FILES["wb"]))
    ws = gw.worksheets[0]
    ok("golden workbook: the first sheet states the call and each channel's row",
       str(ws["A1"].value).startswith("2027 media plan: scale Google iOS and Pinterest iOS, hold")
       and [ws.cell(row=6 + i, column=1).value for i in range(7)] == order_
       and all(ws.cell(row=6 + i, column=3).value == fig["return_plan"][c] and ws.cell(row=6 + i, column=4).value == fig["return_stretch"][c]
               and ws.cell(row=6 + i, column=5).value == fig["value_plan"][c] and ws.cell(row=6 + i, column=6).value == fig["next_euro"][c]
               and ws.cell(row=6 + i, column=2).value.lower() == fig["bands"][c] for i, c in enumerate(order_)))
    ok("golden workbook: named sheets, a chart on the first, frozen headers",
       [w_.title for w_ in gw] == ["Bands 2027", "Unrecorded charges", "Unnamed installs", "Budget response", "Routes"]
       and len(ws._charts) == 1 and all(w_.freeze_panes for w_ in gw))
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("blocks: the four blocks and the tags, no em dash, no table",
       [h for h in re.findall(r"^## (.+)$", sub, re.M)] == ["Tags", "Final Recommendation", "Supplementary Questions",
                                                           "Critical Components", "Step-by-Step"]
       and "—" not in sub and "|" not in sub)
    ok("blocks: every return in the recommendation is the CSV's", all(("%s %.2f" % (c, fig["return_plan"][c])) in sub for c in MEM))
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    ok("prompt: names no file, no method and no role",
       not any(os.path.splitext(n)[0] in prompt or n in prompt for n in files) and len(prompt) < 1000
       and not re.search(r"postback|consent|tracking|budget|auction|store report|round", prompt, re.I))
    shutil.rmtree(tmp)
    print("\n%d passed, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
