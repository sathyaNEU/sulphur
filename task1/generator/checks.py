"""task1 architecture 7: the build's assertions, run on the cut pack (target/), the goldens and the two json files.

    python3 task1/generator/checks.py

The bar block (labels R1 to R7), every row of the design note's fork table (SF1 to SF41), the pinning list, the pack
against the simulation it was written from, mess neutrality, the forcing on both sides, the realism sweep, the input
gates, the goldens, the answer blocks and the prompt. It rebuilds the pack once into a scratch folder (the
byte-identical check, and the account order the array comparison needs)."""
import csv
import hashlib
import itertools
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
import writeup as WU  # noqa: E402
import build as BD  # noqa: E402
import deliver  # noqa: E402
import docs as D  # noqa: E402
import make as MK  # noqa: E402
import pack as P  # noqa: E402
import results as RS  # noqa: E402
import effort as EF  # noqa: E402

T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
N = {"pass": 0, "fail": 0}
MEM = C.MEMBERS
OPEN = {"S1": "AppLovin Android", "S2": "Meta iOS", "S3": "Google Android"}
KEYS7 = ("roas", "roas_s", "installs_week", "vpi", "marginal", "marginal_s", "v12")
# the groupings of sources the battery carries, as sets of sources
GROUPED = {frozenset(g) for k in ("gp", "gpo", "po", "go", "pair", "pair2") for g in C.GROUPS[k]}


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
    """the shipped PDF's text through two extractors, white space folded"""
    from pypdf import PdfReader
    a = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    b = "\n".join(p.extract_text() for p in PdfReader(path).pages)
    return [" ".join(x.split()) for x in (a, b)]


def in_band(fid, x, fig):
    lo, hi = fig["figure_band"][fid]
    return lo <= RS.stated(fid, x) <= hi


def gap(fid, x, fig):
    """how far outside its range a figure falls, as a share of the figure"""
    lo, hi = fig["figure_band"][fid]
    return max(lo - x, x - hi) / abs(fig["figure"][fid])


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
    O, g, fam, lat, direct, v = X["O"], X["golden"], X["family"], X["lattice"], X["direct"], X["v"]
    ok("figures.json is what the cut pack computes", json.loads(json.dumps(fig2, sort_keys=True, default=float)) == fig)
    ok("effort.json is what the cut pack computes", json.loads(json.dumps(eff2, default=float)) == eff)
    fids = list(fig["figure"])
    names = [n for n, _r in fam]
    fd = dict(fam)
    same = lambda *ns: all(n in fd and RS.call_of(fd[n]) == fig["call"] for n in ns)

    # ------------------------------------------------------------------------------------------------------------
    # R1: the field's raw material ships, and the golden reads it
    # ------------------------------------------------------------------------------------------------------------
    ids = np.array([int(x[3:], 16) for x in O.account_id])
    order = np.argsort(aid)
    pos = order[np.searchsorted(aid[order], ids)]
    ok("R1 every consumer account of the simulation is an account row", bool((aid[pos] == ids).all()) and O.n == Oc.n)
    for k in ("week", "day", "country", "ios", "cv", "consent", "label", "pool", "last_open", "rec", "rec_a0", "n_rec", "auto_on",
              "plan_seen", "netm", "neta", "mature"):
        ok("R1 the files give back the simulation's %s, account by account" % k,
           bool(np.array_equal(getattr(O, k), getattr(Oc, k)[pos])))
    # the state at the last open: the app shows a checkout trial that was charged after the last open as a trial too
    # (no estimator reads the state of a checkout subscription, whose every charge is on file)
    web_trial = W["web"] & W["conv"] & W["trial"] & (W["last_open"] < W["conv_day"])
    ok("R1 the files give back the simulation's trial_seen, account by account (store subscriptions as the estimators "
       "read them; %d checkout trials charged after the last open show as trials as well)" % int(web_trial.sum()),
       bool(np.array_equal(O.trial_seen, (Oc.trial_seen | web_trial)[pos]))
       and bool(np.array_equal(O.trial_seen[~O.web], Oc.trial_seen[pos][~O.web])))
    sub = (O.plan_seen > 0) | O.trial_seen
    ok("R1 the billing route on file is the simulation's on every account with a subscription or a trial",
       bool(np.array_equal(O.web[sub], Oc.web[pos][sub])))
    for c in C.ORDER:
        ok("R1 %s: weekly installs, budgets and spend read back from the files" % c,
           bool(np.array_equal(O.agg[c], Oc.agg[c]) and np.array_equal(O.B[c]["budget"], Oc.B[c]["budget"])
                and np.allclose(O.B[c]["spend"], Oc.B[c]["spend"], rtol=0, atol=0.006))
           and (c not in C.GATED or bool(np.array_equal(O.agg_cvm[c], Oc.agg_cvm[c]))))
    for pl, name in ((0, "Google Play"), (1, "App Store")):
        tot = all(O.store[pl][k].sum() == Oc.store[pl][k].sum() for k in ("first", "ren", "ann"))
        per = max(float(np.abs(O.store[pl][k] - Oc.store[pl][k]).max()) for k in ("first", "ren", "ann"))
        ok("R1 %s's report holds the simulation's store charges (totals equal; a period at most %d apart%s)" % (
            name, per, ", the App Store's days being Pacific days" if pl else ""),
           tot and (per == 0 if pl == 0 else 0 < per < 100))
    worst = max(abs(g[c][k] / core_gold[c][k] - 1) for c in C.ORDER for k in KEYS7 if c in MEM or k not in ("roas_s", "marginal_s"))
    ok("R1 the golden on the files is the core's golden on the simulation (worst figure %.5f apart)" % worst, worst < 5e-3)
    ok("R1 the call on the files is the core's call", RS.call_of(g) == RS.call_of(core_gold) == fig["call"])
    heads = {}
    for k in P.FILES:
        with open(f(k), newline="") as fh:
            heads[k] = next(csv.reader(fh))
    banned = re.compile(r"return|roas|ltv|value_per|per_install|dormant|silent|lapsed|inventory|auction|deliver|pacing|true_|band|"
                        r"rank|score|unattributed|predicted|expected|quality|wide|churn|continu", re.I)
    hits = [(k, h) for k, hs in heads.items() for h in hs if banned.search(h)]
    ok("R1 no shipped column holds a result or is named for a step", not hits, hits)
    ok("R1 the accounts file has no column for a person's traits, the wide inventory or an unnamed install's source",
       heads["acc"] == ["account_id", "created_at", "platform", "storefront", "account_type", "tracking_status",
                        "conversion_value_48h", "last_open_at", "sub_state_at_last_open", "sub_store_at_last_open",
                        "sub_plan_at_last_open", "auto_renew_at_last_open"])
    ok("R1 the postbacks carry a campaign and no account", "account_id" not in heads["skan"] and "install_id" not in heads["skan"]
       and "campaign_id" in heads["skan"])
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
        r = A.route(A.PackObs(T, slip=slip))
        fv = C.figure_values(r)
        outside = [fid for fid in fids if not in_band(fid, fv[fid], fig)]
        move = max(abs(fv[fid] / gf[fid] - 1) for fid in fids)
        ok("R2 %s: the call stands and every graded figure stays in its range (largest move %.2f per cent)" % (name, 100 * move),
           RS.call_of(r) == fig["call"] and not outside and move > 0, outside)
    for conv, _kw in A.PACK_VARIANTS:
        r = fd[conv]
        ok("R2 %s: same call, largest return move %.2f per cent" % (conv, 100 * max(abs(r[c]["roas"] / g[c]["roas"] - 1) for c in MEM)),
           RS.call_of(r) == fig["call"])

    # ------------------------------------------------------------------------------------------------------------
    # R3: each result's hurried figure, outside its range
    # ------------------------------------------------------------------------------------------------------------
    by = {r["id"]: r for r in eff["results"]}
    reflex = C.figure_values(lat["S1+S2+S3"])
    for s, fid in C.COMPONENTS.items():
        fv = C.figure_values(lat[s])
        ok("R3 %s lost alone files %s at %s, outside %s by %.0f per cent of the figure" % (
            s, fid, RS.stated(fid, fv[fid]), fig["figure_band"][fid], 100 * gap(fid, fv[fid], fig)), gap(fid, fv[fid], fig) > 0.05)
        others = [x for t, x in C.COMPONENTS.items() if t != s]
        ok("R3 %s lost alone leaves the other two steps' own figures inside their ranges (%s)" % (
            s, ", ".join("%s %s" % (x, RS.stated(x, fv[x])) for x in others)),
           all(in_band(x, fv[x], fig) for x in others), [(x, fv[x]) for x in others])
        wrong = [m for m in MEM if C.band(lat[s][m]["roas"]) != fig["bands"][m]]
        ok("R3 %s lost alone moves %s to another band and no other channel" % (s, OPEN[s]), wrong == [OPEN[s]], wrong)
        moved = [m for m in MEM if not in_band("return " + m, lat[s][m]["roas"], fig)]
        ok("R3 %s lost alone misstates %d channels' returns and moves one band (the misreading runs across the data)" % (
            s, len(moved)), len(moved) >= 3 and OPEN[s] in moved, moved)
    for nm, lim in (("return ", 1), ("stretch return ", 1), ("value at plan ", 0), ("next euro ", 1), ("stretch next euro ", 1),
                    ("paid per install ", 0)):
        inside = [c for c in MEM if in_band(nm + c, reflex[nm + c], fig)]
        ok("R3 the reflex route lands %d of 7 of '%s' inside the ranges" % (len(inside), nm.strip()), len(inside) <= lim, inside)
    ok("R3 the reflex route files Meta iOS scale and both Android channels cut",
       [C.band(lat["S1+S2+S3"][c]["roas"]) for c in ("Meta iOS", "Google Android", "AppLovin Android")] == ["scale", "cut", "cut"])
    ok("R3 the seven shortcut routes file seven different wrong calls", fig["distinct_wrong_calls"] == 7)
    ok("R3 the records as they stand cut all seven channels", all(C.band(direct[c]["roas"]) == "cut" for c in MEM),
       [C.band(direct[c]["roas"]) for c in MEM])
    for rid, gr in zip(("R1", "R2", "R3", "R4", "R5", "R6", "R7"), ("missed", "missed", "partly", "missed", "missed", "missed", "missed")):
        ok("R3 effort.json grades the careful pass %s on %s" % (gr, rid), EF.grade(by[rid]["passes"]["careful"], by[rid])[0] == gr)
    sc = fig["shortcuts"]
    for key in ("by_period", "one_factor", "seen_rate", "web_rate", "as_recorded", "named_by_cell", "named_average", "pool_value",
                "search_ads", "android", "one_ratio", "organic_pinned", "four_social", "on_spend", "last_year"):
        ok("R3 the simpler way '%s' files %s at %.3f, %s" % (sc[key]["rule"][:60], sc[key]["channel"], sc[key]["return_plan"],
                                                           sc[key]["band"]),
           sc[key]["channel"] in sc[key]["wrong"] and sc[key]["band"] != fig["bands"][sc[key]["channel"]])
    for step, key in (("S1", "by_period"), ("S2", "named_by_cell"), ("S3", "on_spend")):
        ok("R3 '%s' priced as a simpler way is the lattice's %s lost alone (%.1f)" % (key, step, sc[key]["earns"]),
           sc[key]["earns"] == fig["rubric"]["one_lost"][step])
    off = [k for k in sc if sc[k]["wrong"]]
    ok("R3 every simpler way that files a wrong band loses its own step's figure and keeps the other two steps' "
       "(the records as they stand lose two)",
       all(sc[k]["step"] not in sc[k]["components_kept"] for k in off)
       and all(len(sc[k]["components_kept"]) == 2 for k in off if k != "as_recorded")
       and sc["as_recorded"]["components_kept"] == ["S3"], {k: sc[k]["components_kept"] for k in off})
    top = max(off, key=lambda k: sc[k]["earns"])
    ok("R3 on the rubric the simpler ways that file a wrong band earn %.1f to %.1f (the highest: %s); the ways that never "
       "reach a step's own records (%s) earn %.1f at most, under the bar of 60, and every one of them but the one factor "
       "per store 50 or under" % (
           min(sc[k]["earns"] for k in off), sc[top]["earns"], top, ", ".join(("by_period", "one_factor", "named_by_cell",
                                                                              "named_average", "on_spend", "last_year")),
           max(sc[k]["earns"] for k in ("by_period", "one_factor", "named_by_cell", "named_average", "on_spend", "last_year"))),
       sc[top]["earns"] < 70.0 and max(sc[k]["earns"] for k in ("by_period", "one_factor", "named_by_cell", "named_average",
                                                                "on_spend", "last_year")) < 60.0
       and all(sc[k]["earns"] <= 50.0 for k in ("by_period", "named_by_cell", "named_average", "on_spend", "last_year")))
    ok("R3 the three social networks sharing one ratio, refused by both readings of the fit's spread, files the same seven "
       "bands and keeps all three steps' figures (%.1f)" % sc["three_social"]["earns"],
       not sc["three_social"]["wrong"] and sc["three_social"]["components_kept"] == ["S1", "S2", "S3"])

    # ------------------------------------------------------------------------------------------------------------
    # R4: no plant
    # ------------------------------------------------------------------------------------------------------------
    frames = {}
    for k in ("acc", "bill", "attr", "skan", "spend", "apple", "google", "web", "creat", "rate"):
        frames[k] = d = pd.read_csv(f(k), dtype=str, keep_default_na=False)
        ok("R4 %s: no row is a copy of another" % P.FILES[k], not d.duplicated().any(), int(d.duplicated().sum()))
    sp = frames["spend"]
    blk = sp.drop(columns=["date"]).astype(str).agg("|".join, axis=1)
    day = blk.groupby(sp.date).agg("#".join)
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
    placed = [x for x in cells if any(c in x for c in C.ORDER) and re.search(r"\b(scale|hold|cut)\b", x, re.I)]
    ok("R4 no shipped sentence or cell places a channel in a band", not placed, placed[:3])
    stated = {("%.3f" % fig["return_plan"][c]) for c in MEM} | {("%.2f" % fig["return_plan"][c]) for c in MEM}
    ok("R4 no document states a channel's return", not any(re.search(r"\b%s\b" % re.escape(x), t) for x in stated
                                                         for t in texts.values() if x not in ("0.90", "1.20")))
    ok("R4 the pack holds no memo, draft or prior analysis",
       not any(re.search(r"memo|draft_|analysis|review|ltv|roas|forecast|model", n, re.I) for n in os.listdir(T)))

    # ------------------------------------------------------------------------------------------------------------
    # R5: no one thing: each factor across the data, and none rescuing more than a third alone
    # ------------------------------------------------------------------------------------------------------------
    ch = fig["channels"]
    ok("R5 the records lack 9 per cent or more of every channel's twelve-month revenue (%.1f to %.1f per cent)" % (
        min(x["unrecorded_pct"] for x in ch.values()), max(x["unrecorded_pct"] for x in ch.values())),
       all(x["unrecorded_pct"] >= 9 for x in ch.values()) and len(ch) == 8)
    for oi, nm in ((len(C.ORDER), "iOS"), (len(C.ORDER) + 1, "Android")):
        org = (O.label == oi) & O.mature
        ok("R5 the organic %s installs' records lack their share too" % nm, 1 - C.values(O, "raw")[org].sum() / v[org].sum() > 0.05)
    ren, fst = C.s1_candidates(O)
    for ci, c in enumerate(C.ORDER):
        lab = (O.label == ci) & O.mature
        ok("R5 %s: its installs on file hold subscriptions last seen set to renew and trials last seen unconverted (%d and %d)"
           % (c, (ren & lab).sum(), (fst & lab).sum()), (ren & lab).sum() >= 50 and (fst & lab).sum() >= 200)
    named = [ch[c]["named_pct"] for c in C.GATED]
    ok("R5 every iOS network has 20 to 35 per cent of its installs named by the export (%.1f to %.1f)" % (min(named), max(named)),
       len(named) == 5 and 20 < min(named) and max(named) < 35)
    rs = fig["ratios"]["sources"]
    ok("R5 on every source an unnamed install is worth less than a named one of the same first-48-hour value (%.3f to %.3f)" % (
        min(x["ratio"] for x in rs.values()), max(x["ratio"] for x in rs.values())),
       len(rs) == 6 and all(x["ratio"] + 2 * x["se"] < 1 for x in rs.values()))
    ok("R5 the same holds where the declined installs are named: Apple Search Ads %.2f, Android %s" % (
        fig["ratios"]["search_ads_ratio"], fig["android_ratios"]),
       fig["ratios"]["search_ads_ratio"] < 0.95 and all(x < 0.9 for x in fig["android_ratios"].values()))
    ok("R5 every iOS network's named installs are worth more than its installs as a whole",
       all(ch[c]["named_value"] > 1.1 * ch[c]["paid_per_install"] for c in C.GATED))
    sd = {c: float(np.std(np.log(O.B[c]["spend"] / O.B[c]["budget"]))) for c in C.ORDER}
    ok("R5 the share of the budget spent moves week to week on all eight channels (sd of the log %.2f to %.2f)" % (
        min(sd.values()), max(sd.values())), min(sd.values()) > 0.05)
    ok("R5 fitted on spend, installs respond more steeply than on the budget on all eight channels",
       all(ch[c]["spend_elasticity"] > ch[c]["budget_elasticity"] + 0.1 for c in C.ORDER))
    ok("R5 every channel of the records has budget moves on the log (%d to %d)" % (
        min(ch[c]["moves"] for c in C.ORDER), max(ch[c]["moves"] for c in C.ORDER)), min(ch[c]["moves"] for c in C.ORDER) >= 5)
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
        got = [rid for rid, x in fig["result_grades"][alone[s]].items() if x == "right"]
        ok("R6 the %s sentence, executed on the reflex route, rescues %s" % (s, got or "no whole result"),
           got == h["rescues"] and len(got) <= 2)
    ok("R6 corelib on the cut pack: no sentence rescues more than a third of the rubric (%s)" % fig["rubric"]["fixed_alone"],
       max(fig["rubric"]["fixed_alone"].values()) <= 100 / 3.0)

    # ------------------------------------------------------------------------------------------------------------
    # R7: the rivals, and the forcing on both sides
    # ------------------------------------------------------------------------------------------------------------
    n = fig["variant_counts"]
    nb = n["beside"]
    bat, bes = fam[:len(fam) - nb], fam[len(fam) - nb:]
    ok("R7 the battery holds %d variants beside the golden: %d singly, %d in pairs, %d one for each step" % (
        len(bat), n["singles"], n["pairs"], n["triples"]),
       len(bat) == fig["variants"] == n["singles"] + n["pairs"] + n["triples"] and len(set(names)) == len(fam)
       and n["singles"] == len(C.VARIANTS) + len(A.PACK_VARIANTS) and n["pairs"] + n["apart"] == n["singles"] * (n["singles"] - 1) // 2
       and n["triples"] == n["by_step"]["S1"] * n["by_step"]["S2"] * n["by_step"]["S3"] and min(n["by_step"].values()) >= 10)
    BS = fig["beside"]
    ok("R7 %d more ways stand beside the battery, each run as it stands: the second step's fit on finer rows (%d), the "
       "installs equation's unrescaled prediction (%d), the first-48-hour values grouped on one part of them (%d) and the "
       "value equation on the complete weeks (%d)" % (nb, BS["finer_rows"]["ways"], BS["unrescaled"]["ways"],
                                                      BS["grouped"]["ways"], BS["value_weeks"]["ways"]),
       nb == len(C.BESIDE) == 17 and [x for x, _r in bes] == [x for x, _k in C.BESIDE] == BS["names"]
       and (BS["finer_rows"]["ways"], BS["unrescaled"]["ways"], BS["grouped"]["ways"], BS["value_weeks"]["ways"]) == (6, 6, 4, 1))
    bad = []
    edge = {fid: [fig["figure"][fid], fig["figure"][fid]] for fid in fids}
    for i, (nm, r) in enumerate(fam):
        fv = C.figure_values(r)
        if RS.call_of(r) != fig["call"] or any(not in_band(fid, fv[fid], fig) for fid in fids):
            bad.append(nm)
        if i < len(bat):
            for fid in fids:
                edge[fid] = [min(edge[fid][0], fv[fid]), max(edge[fid][1], fv[fid])]
    ok("R7 every variant, in the battery and beside it, files the golden call with every graded figure in its range", not bad, bad[:5])
    loose, tight = [], []
    for fid in fids:
        if fid in fig["beside"]["edges"]:
            continue
        x, step = abs(fig["figure"][fid]), 10.0 ** -RS.unit(fid)
        for room in (edge[fid][0] - fig["figure_band"][fid][0], fig["figure_band"][fid][1] - edge[fid][1]):
            if room > RS.BAND_PAD * x + step + 1e-9:
                loose.append(fid)
            if room < RS.BAND_PAD * x - 1e-9:
                tight.append(fid)
    ok("R7 every range no way beside the battery leaves is the battery's span with %.1f per cent of the figure either "
       "side, stated outward at the figure's precision: none wider, none narrower" % (100 * RS.BAND_PAD),
       not loose and not tight, (loose[:4], tight[:4]))
    gfv = C.figure_values(g)
    bat_f, bes_f = [C.figure_values(r) for _n, r in bat], [C.figure_values(r) for _n, r in bes]
    off = [fid for fid in fids
           if fig["figure_band"][fid] != RS.band_of(fid, gfv[fid], [x[fid] for x in bat_f], [x[fid] for x in bes_f])]
    # a way beside the battery that moves a figure sits a full per cent of the figure inside its range, both sides
    thin = [fid for fid in fids for x in bes_f
            if abs(x[fid] - gfv[fid]) > 1e-6 * abs(gfv[fid])
            and min(x[fid] - fig["figure_band"][fid][0], fig["figure_band"][fid][1] - x[fid])
            < RS.BESIDE_PAD * abs(gfv[fid]) - 1e-9]
    still = [fid for fid in fids if all(abs(x[fid] - gfv[fid]) <= 1e-6 * abs(gfv[fid]) for x in bes_f)]
    ok("R7 %d ranges are taken out to a way beside the battery, each reaching %.0f per cent of the figure beyond every "
       "such way that moves the figure (%d figures none of them moves)"
       % (len(fig["beside"]["edges"]), 100 * RS.BESIDE_PAD, len(still)),
       not off and not thin and 10 <= len(fig["beside"]["edges"]) <= 45
       and not set(still) & set(fig["beside"]["edges"]), (off[:4], thin[:4]))
    two = [nm for nm in names if nm.count(";") == 1 and all(x.strip().endswith("sharing one ratio") for x in nm.split(";"))]
    ok("R7 two groupings of different sources are taken together in the battery (%d pairs)" % len(two), len(two) == 8, two)
    near = min(abs(r[c]["roas"] - l) for _n, r in bat + [("golden", g)] for c in MEM for l in C.LINES)
    ok("R7 no variant of the battery brings a channel within 0.04 of a line (nearest %.3f, %s)" % (near, fig["nearest_variant"]["variant"]),
       near >= 0.04 and abs(near - fig["nearest_variant"]["distance"]) < 0.001)
    near_b = min(abs(r[c]["roas"] - l) for _n, r in bes for c in MEM for l in C.LINES)
    ok("R7 no way beside the battery brings a channel within 0.01 of a line (nearest %.3f, %s, %s)" % (
        near_b, fig["nearest_beside"]["channel"], fig["nearest_beside"]["variant"]),
       near_b >= 0.01 and abs(near_b - fig["nearest_beside"]["distance"]) < 0.001
       and fig["nearest_beside"]["channel"] == "AppLovin Android")
    XR, crossed = fig["crossed"], X["crossed"]
    near_x = min(abs(r[c]["roas"] - l) for _n, r in crossed for c in MEM for l in C.LINES)
    ok("R7 crossed with the battery (each way beside it with every single way it can be taken with, and with one way of each "
       "of the other two steps at once), no way beside it moves a band: %d crossings, the nearest to a line %.4f (%s, %s)" % (
           len(crossed), near_x, XR["nearest"]["channel"], XR["nearest"]["variant"]),
       XR["crossings"] == len(crossed) >= 3000 and not XR["moved"] and len({n for n, _r in crossed}) == len(crossed)
       and all(RS.call_of(r) == fig["call"] for _n, r in crossed) and near_x >= 0.004
       and abs(near_x - XR["nearest"]["distance"]) < 0.001 and XR["nearest"]["channel"] == "AppLovin Android")
    # the readings the blocks refuse by a figure from the files
    PM = fig["ratios"]["markets_pooled"]
    mwm = fig["ratios"]["market_weeks"]["miss_pct"]
    ok("SF32 the rows the ratios are fitted on: the six fits on finer rows stand beside the battery (above); the ratios "
       "fitted with the markets pooled file Google iOS %.3f, their spreads %.1f to %.1f times the market-weeks', the "
       "market-weeks' revenue missed by %.1f per cent against %.1f" % (
           PM["return_plan"]["Google iOS"], PM["se_times"][0], PM["se_times"][1], mwm["markets_pooled"], mwm["fitted"]),
       not PM["wrong"] and PM["se_times"][0] >= 2.0 and mwm["markets_pooled"] >= mwm["fitted"] + 0.4
       and all(x["se"] > 2 * x["se_market_weeks"] for x in PM["sources"].values())
       and abs(PM["return_plan"]["Google iOS"] - 1.20) < 0.05)
    Fm = fig["forms"]
    GAm, MM = fig["check_moves"]["channels"]["Google Android"], Fm["moved_missed_pct"]
    ok("SF34 the response's form: a straight line in the budget is refused in both of its forms (on the installs themselves "
       "it misses the moved weeks by %.1f per cent against the power form's %.1f and puts Google Android's raised weeks over "
       "its lowered ones at %.3f against %.3f counted; on the log of installs the log of the budget added to it gives F %.1f) "
       "and an exponential likewise (F %.1f, the moved weeks missed by %.1f), the power form is not by the budget added to it "
       "(%.1f), against %.2f; either line would file the seven bands" % (
           MM["line"], MM["power"], Fm["line_raised_over_lowered"], GAm["actual"], Fm["line"], Fm["exponential"],
           MM["exponential"], Fm["power"], Fm["point"]),
       Fm["line"] >= Fm["point"] + 0.5 and Fm["exponential"] > 10 * Fm["point"] and Fm["power"] <= Fm["point"] - 0.5
       and MM["line"] >= 2 * MM["power"] and MM["exponential"] >= 1.5 * MM["power"]
       and MM["power"] == fig["check_moves"]["missed_pct"]["golden"]
       and abs(Fm["line_raised_over_lowered"] - GAm["actual"]) >= 2 * abs(GAm["budget_fit"] - GAm["actual"])
       and not Fm["line_wrong"]["levels"] and not Fm["line_wrong"]["log"])
    ok("SF35 value per install held flat: every plan channel's value slope is below nought by %.1f or more of its "
       "spreads (%.2f to %.2f)" % (
        Fm["value_slope_spreads"], Fm["value_slope_range"][0], Fm["value_slope_range"][1]),
       Fm["value_slope_spreads"] >= 4 and Fm["value_slope_range"][1] < -0.05)
    K_ = fig["carry"]
    y1 = {k: k + "_first_year" for k in ("at_share", "weekly_shares", "geometric_mean", "median_week")}
    al = {k: K_["adds_up_pct"][y1[k]]["AppLovin Android"] for k in y1}
    UN = BS["unrescaled"]["return_plan"]
    ok("SF33 the installs equation's unrescaled prediction: put at the share of the budgets spent or week by week through "
       "the delivery term, over both years, the first or the second, it adds up to %.1f to %.1f per cent of every channel's "
       "installs of its own weeks and files the seven bands (AppLovin Android %.3f at the thinnest); put at the geometric "
       "mean of the weekly shares or at the median week's it falls %.1f to %.1f per cent short of some channel's (the forms "
       "kept %.1f at most) and at the first year's share would cut AppLovin Android (%.3f and %.3f, adding up to %.1f and "
       "%.1f per cent of its installs where the forms kept add up to %.1f and %.1f)" % (
           K_["held_pct"][0], K_["held_pct"][1], min(UN["AppLovin Android"]), K_["refused_short_pct"][0],
           K_["refused_short_pct"][1], K_["held_short_pct"], K_["returns"][y1["geometric_mean"]]["AppLovin Android"],
           K_["returns"][y1["median_week"]]["AppLovin Android"], al["geometric_mean"], al["median_week"], al["at_share"],
           al["weekly_shares"]),
       K_["held"] == [k + "_" + w for k in RS.CARRY_HELD for w in ("both_years", "first_year", "second_year")]
       and all(not K_["wrong"][k] for k in K_["held"])
       and K_["held_pct"][0] >= 97.0 and K_["held_pct"][1] <= 102.0 and K_["held_short_pct"] <= 3.0
       and K_["refused_short_pct"][0] >= K_["held_short_pct"] + 1.5
       and all(100 - min(K_["adds_up_pct"][k].values()) >= 4.0 for k in K_["refused"])
       and all(K_["wrong"][y1[k]] == ["AppLovin Android"] for k in ("geometric_mean", "median_week"))
       and al["geometric_mean"] <= al["at_share"] - 3.0 and al["median_week"] <= al["weekly_shares"] - 3.0
       and all(UN[c] == [K_["returns"][k + "_" + w][c] for w in ("both_years", "first_year", "second_year")
                         for k in RS.CARRY_HELD] for c in MEM)
       and min(UN["AppLovin Android"]) == K_["returns"][y1["at_share"]]["AppLovin Android"]
       and min(K_["rescale"].values()) > 1.01)
    # a span is stated to the thousandth, so it may sit half a thousandth past the unrounded figure the range was set on
    room = lambda fam_, key, c, x: (fig[key + "_band"][c][0] + RS.BESIDE_PAD * abs(fig[key][c]) - 0.0005 <= x[0]
                                    and x[1] <= fig[key + "_band"][c][1] - RS.BESIDE_PAD * abs(fig[key][c]) + 0.0005)
    GD, VW = BS["grouped"], BS["value_weeks"]
    ok("SF40 the groups the first-48-hour values are priced in: the eight and the four of the battery, and beside it the "
       "sessions bucket alone (eight values or four pairs) and the flags alone (four groups, or eight with the sessions "
       "split in two); each of the four files the seven bands, with what one more euro returns at %.3f to %.3f on Meta iOS "
       "and %.3f to %.3f on Google iOS, a full per cent inside their ranges" % (
           GD["next_euro"]["Meta iOS"][0], GD["next_euro"]["Meta iOS"][1], GD["next_euro"]["Google iOS"][0],
           GD["next_euro"]["Google iOS"][1]),
       GD["ways"] == 4 and all(room("grouped", "next_euro", c, GD["next_euro"][c]) for c in MEM)
       and all(room("grouped", "next_euro_stretch", c, GD["next_euro_stretch"][c]) for c in MEM)
       and all(room("grouped", "return_plan", c, GD["return_plan"][c]) for c in MEM)
       and same(*[n for n, k in C.BESIDE if "cells" in k]))
    ok("SF41 the weeks the value equation is fitted on: all 104, or the %d complete weeks alone, which stands beside the "
       "battery and puts what one more euro returns on TikTok iOS at %.3f (%.3f on top of the stretch), a full per cent "
       "inside its range, with the seven bands as they are" % (
           C.MATURE, VW["next_euro"]["TikTok iOS"][0], VW["next_euro_stretch"]["TikTok iOS"][0]),
       VW["ways"] == 1 and all(room("value_weeks", "next_euro", c, VW["next_euro"][c]) for c in MEM)
       and all(room("value_weeks", "next_euro_stretch", c, VW["next_euro_stretch"][c]) for c in MEM)
       and VW["next_euro"]["TikTok iOS"][0] < fig["next_euro"]["TikTok iOS"] - 0.03
       and same(*[n for n, k in C.BESIDE if "weeks_v" in k]))
    ok("R7 the halves of postbacks dated before the first install week come to %s installs" % fig["steps"]["early_postback_installs"],
       fig["steps"]["early_postback_installs"] == 85.0)
    # which sources may share one ratio: every set of two or more of the six, under both readings of the fit's spread
    srcs = C.GATED + ["organic iOS"]
    let, refused = set(), 0
    for k in range(2, len(srcs) + 1):
        for names_ in itertools.combinations(srcs, k):
            a = C.s2_equal_test(O, v, names_)[0]
            b = C.s2_equal_test(O, v, names_, cov="classical")[0]
            pt = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07}[k - 1]
            if a > pt and b > pt:
                refused += 1
            else:
                let.add(frozenset(names_))
    ok("R7 of the %d sets of sources, the test of equal ratios lets through (under one reading of the spread or the other) "
       "exactly the %d groupings the battery carries" % (refused + len(let), len(GROUPED)), let == GROUPED,
       sorted(sorted(x) for x in let ^ GROUPED))
    T_ = fig["ratios"]["share_tests"]
    ok("R7 the groupings refused are refused under both readings of the spread, by a clear margin",
       all(T_[k]["refused"] and min(T_[k]["stat"], T_[k]["stat_one_variance"]) > 2 * T_[k]["point"]
           for k in ("Meta and Snapchat", "Meta, TikTok and Snapchat", "the four social networks", "the five networks")))
    L_ = fig["ratios"]["lent"]
    ok("R7 the ratios lent by Apple Search Ads and by the Android look-alikes are refused under both readings (%s, %s)" % (
        L_["search_ads"]["stat"], L_["android"]["stat"]),
       all(min(x["stat"], x["stat_one_variance"]) > 5 * x["point"] for x in L_.values()))
    for p in fig["perturbations"]:
        ok("R7 %s times %.3f: the call holds (nearest line %.3f away)" % (p["input"], p["factor"], p["nearest"]), p["call_holds"])
    ok("R7 the perturbations move every fitted input a fifth either way and the delivery share by its widest quarter",
       len(fig["perturbations"]) >= 20 and fig["delivery_share_spread_pct"] > 5)
    CO = fig["corners"]
    floor_ = min(fig["variant_range"]["AppLovin Android"][0], XR["return_range"]["AppLovin Android"][0])
    ok("R7 the corners of each channel's installs and value ranges stay in its band on six channels; AppLovin Android's "
       "low corner is %.3f (its installs range reaches one per cent beyond the unscaled prediction at the first year's "
       "share, its value range the battery's low edge) and no way run puts the two together: its lowest return over the "
       "battery, the ways beside it and their crossings is %.3f" % (CO["AppLovin Android"]["low"], floor_),
       sorted(c for c, x in CO.items() if not x["band_holds"]) == ["AppLovin Android"]
       and 0.88 < CO["AppLovin Android"]["low"] < C.LINES[0] < CO["AppLovin Android"]["high"] < C.LINES[1]
       and floor_ >= C.LINES[0] + 0.004, CO)
    for rid in ("R1", "R2", "R3", "R4", "R5"):
        w = max((hi - lo) / abs(by[rid]["golden"][k]) for k, (lo, hi) in by[rid]["bands"].items())
        ok("R7 %s: no range wider than %.1f per cent of its figure (the widest are Meta iOS's, which span the finer-row "
           "fits of its ratio, SF32)" % (rid, 100 * w), w < 0.17)
    w = max((hi - lo) / abs(by["R6"]["golden"][k]) for k, (lo, hi) in by["R6"]["bands"].items())
    ok("R7 R6: no range wider than %.0f per cent of its figure, and the reflex route outside all but two" % (100 * w),
       w < 0.40 and sum(in_band(k, reflex[k], fig) for k in by["R6"]["bands"]) <= 2)
    ok("R7 corelib on the cut pack: level 5, no failure", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], fig["rubric"]["fails"])
    ok("R7 the rubric on the cut pack: one step lost %s, fixed alone %s, the reflex route %.1f, the rigorous route %.1f" % (
        fig["rubric"]["one_lost"], fig["rubric"]["fixed_alone"], fig["rubric"]["reflex"], fig["rubric"]["rigorous"]),
       max(fig["rubric"]["one_lost"].values()) <= 50 and fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50)
    for s, r in X["refs"].items():
        ge = abs(r["golden"] - r["truth"])
        worst_rival = min(abs(x - r["truth"]) for x in r["rivals"].values())
        ok("R7 the %s referee: the estimate %.2f against the record's %.2f, the nearest simpler way %.1f times further" % (
            s, r["golden"], r["truth"], worst_rival / max(ge, 1e-9)), worst_rival > 3 * ge)
    T0 = C.truth_at_plan()
    ok("R7 the golden call is the world's own on all seven channels", all(C.band(T0[c]["roas"]) == fig["bands"][c] for c in MEM))
    ok("R7 every golden return is within 5 per cent of the world's own (worst %.1f)" % (
        100 * max(abs(g[c]["roas"] / T0[c]["roas"] - 1) for c in MEM)), max(abs(g[c]["roas"] / T0[c]["roas"] - 1) for c in MEM) < 0.05)

    # ------------------------------------------------------------------------------------------------------------
    # the fork table, row by row (every filed sentence read from the shipped PDF through two extractors)
    # ------------------------------------------------------------------------------------------------------------
    both = lambda s: s in pol_a and s in pol_b
    acc, att, bil = frames["acc"], frames["attr"], frames["bill"]
    cons = set(acc.account_id[acc.account_type == "consumer"])
    firsts = att[(att.is_reinstall == "false")].drop_duplicates("install_id")
    ok("SF1 policy 2.2 files what an install is, and every consumer account has one first install on file",
       both("An install is the first install of a new consumer account. A second device, a reinstall, a staff account and "
            "a test account are not installs.")
       and firsts.account_id[firsts.account_id.isin(cons)].is_unique and set(firsts.account_id) >= cons)
    rep = sp.assign(n=sp.installs_reported_by_network.astype(int)).groupby(["network", "os"]).n.sum()
    over = {c: rep[P.SOURCE[c]] / O.agg[c].sum() for c in C.ORDER}
    ok("SF2 policy 2.2 gives each install to at most one channel whether or not the partner can name it; the networks' own "
       "counts run above the installs on every growth channel (%.2f to %.2f times)" % (min(over[c] for c in MEM), max(over.values())),
       both("Each install is bought by at most one channel, the one whose ad drove it, whether or not the attribution "
            "partner can name it") and all(over[c] > 1.01 for c in MEM))
    ok("SF3 policy 2.3 files the 365 days and every charge the stores or the checkout made",
       both("every charge the App Store, Google Play or the web checkout made on its account in the 365 days from the install"))
    ap = frames["apple"]
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
    ok("SF7 policy 2.6 files the marginal return at a stated spend, every week raised in the same proportion, and 3.2 asks "
       "for it at the plan's spend and at the stretch spend",
       both("one more euro of spend returns at that spend, every week of the period raised in the same proportion")
       and both("its marginal return at the plan's spend and at the stretch spend"))
    ok("SF8 policy 2.1 and 2.3 make the revenue per install the installs' revenue over the installs a period's spend buys",
       both("the 12-month net revenue of the installs the period's spend on the channel buys"))
    ok("SF9 section 3 files the lines: scale from 1.20, hold from 0.90, cut under it",
       both("scale when the return is 1.20 or more, hold when it is 0.90 or more and under 1.20, and cut when it is under 0.90")
       and tuple(C.LINES) == (0.90, 1.20) and fig["policy"]["lines"] == [0.90, 1.20]
       and C.band(0.90) == "hold" and C.band(1.20) == "scale" and C.band(0.8999) == "cut")
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
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    ok("SF13 the prompt asks for the installs a week the plan's spend will buy, and the plan has 52 weekly spends",
       "how many installs a week the plan's spend will buy" in prompt and all(len(O.plan[c]) == 52 for c in MEM))
    ok("SF14 the 52 install weeks to 2 November 2025 have their 365 days on file by 8 November 2026, and the prompt names them",
       (C.MATURE * 7 - 1) + 365 <= C.END_DAY and int(O.day[O.mature].max()) + 365 <= C.END_DAY
       and A.secs(bil.transaction_at).max() // 86400 == C.END_DAY and "in the year to 2 November 2025" in prompt
       and (P.DAY0 + pd.Timedelta(days=C.MATURE * 7 - 1)).isoformat() == "2025-11-02")
    a2 = acc.set_index("account_id")
    org_rows = firsts[(firsts.media_source == "organic") & (firsts.platform == "ios") & firsts.account_id.isin(cons)]
    ratio = {c: O.agg[c][:C.MATURE].sum() / ((O.label == C.ORDER.index(c)) & O.mature).sum() for c in C.GATED}
    ok("SF15 the export gives the organic label on iOS only to accounts that allowed tracking, and each network's postbacks "
       "outnumber its named installs (%.1f to %.1f times)" % (min(ratio.values()), max(ratio.values())),
       bool((a2.tracking_status.reindex(org_rows.account_id) == "authorized").all()) and min(ratio.values()) > 3)
    sch = json.load(open(f("schema")))
    ok("SF16 the schema files a 48-hour window and a postback 24 to 48 hours after it; three days back and four are the same call",
       sch["postback"]["measurement_window_hours"] == 48 and sch["postback"]["sent_after_window_closes_hours"] == [24, 48]
       and same("every postback dated back three days", "every postback dated back four days") and int(O._pb["day"].min()) >= 3)
    ok("SF17 same call: the first-48-hour values in eight groups, four groups, cells of fifty, one tilt per source",
       same("first-48-hour cells in eight groups", "first-48-hour cells in four groups", "cells of fifty or more",
            "each source's named installs through one tilt") and fig["steps"]["thin_cell"] == 20)
    ok("SF18 same call: the launch quarter left out and the last 78 weeks",
       same("installs response without the launch quarter", "installs response on the last 78 weeks"))
    ok("SF19 same call: the delivery share from the mature weeks and from the last 52",
       same("delivery share from the mature weeks", "delivery share from the last 52 weeks"))
    ok("SF20 same call: one share charged for every trial-end candidate, one fit across both stores",
       same("one share charged for every trial-end candidate", "one fit across both stores"))
    gr, ar = fig["stores"]["Google Play"], fig["stores"]["App Store"]
    ok("SF21 same call for the three fitted ways; the web checkout's continuation and the one the app saw take in under 70 per "
       "cent of each store's renewals beyond the records, the fitted one within 1 per cent",
       same("two-rate continuation", "fit without the last two months", "thirty-day cadence")
       and all(x["rivals"][k]["takes_in"] < 0.70 * x["renewal_excess_fitted_periods"] for x in (gr, ar) for k in ("web", "seen"))
       and all(abs(x["rivals"]["fitted"]["takes_in"] / x["renewal_excess_fitted_periods"] - 1) < 0.01 for x in (gr, ar))
       and all(x["rivals"][k]["period_error"] > 20 * x["rivals"]["fitted"]["period_error"] for x in (gr, ar) for k in ("web", "seen")))
    ok("SF22 same call: the nine other ways of fitting each source's ratio",
       same("the ratios fitted separately for lighter and heavier first-48-hour use", "the ratios fitted unweighted",
            "the ratios fitted by fortnight", "the ratios fitted by four-week period",
            "the ratios fitted with weights from the fitted revenue", "organic installs' ratio taken from Apple Search Ads",
            "market-weeks of fewer than a hundred unattributed accounts left out",
            "the networks' ratios drawn toward their pooled ratio by the fit's own spread"))
    ok("SF23 same call: the six groupings a test of equal ratios lets through, and each pair of them on different sources",
       same("Google iOS and Pinterest iOS sharing one ratio", "Google iOS, Pinterest iOS and the organic installs sharing one ratio",
            "Pinterest iOS and the organic installs sharing one ratio", "Google iOS and the organic installs sharing one ratio",
            "Meta iOS and TikTok iOS sharing one ratio", "TikTok iOS and Snapchat iOS sharing one ratio") and same(*two))
    au, ca = fig["ratios"]["adding_up"], fig["check_android"]["AppLovin Android"]
    ok("SF24 a worth lent by another source: the accounts with no channel add up to %.2f and %.2f times what they paid against "
       "%.2f fitted; on Android AppLovin's declined installs paid %.2f against %.2f fitted, %.2f and %.2f lent" % (
           au["named"], au["search_ads"], au["fitted"], ca["paid"], ca["fitted"], ca["search_ads"], ca["named"]),
       au["named"] > 1.25 and au["search_ads"] > 1.1 and abs(au["fitted"] - 1) < 0.01
       and all(abs(x["fitted"] - x["paid"]) < 0.5 * min(abs(x["search_ads"] - x["paid"]), abs(x["named"] - x["paid"]))
               for x in fig["check_android"].values()))
    cm = fig["check_moves"]
    gm = cm["channels"]["Google Android"]
    ok("SF25 same call for spend instrumented by the budget and the budget alone; the fit on spend misses the moved weeks by "
       "%.1f per cent against %.1f and files %.3f for Google Android's raised over lowered weeks against %.3f" % (
           cm["missed_pct"]["spend"], cm["missed_pct"]["golden"], gm["spend_fit"], gm["actual"]),
       same("spend instrumented by the budget", "the budget alone, the delivery left out")
       and cm["missed_pct"]["spend"] > 3 * cm["missed_pct"]["golden"] and abs(gm["budget_fit"] - gm["actual"]) < 0.05
       and abs(gm["spend_fit"] - gm["actual"]) > 0.3)
    ok("SF26 same call: each channel's own month pattern, one value slope, the value response on the mature weeks' own values",
       same("each channel's own month pattern", "one value slope across channels", "value response on the mature weeks' own values"))
    pb = fig["plan_blocks"]
    ok("SF27 a week's month: the plan's %d changes of weekly spend all fall on a week whose Thursday is in a new month, %d of "
       "them with the Monday still in the old one; the Monday reading files the same call" % (pb["changes"], pb["apart_on_thursday"]),
       pb["changes"] >= 8 and pb["changes"] == pb["on_thursday_months"] and pb["off"] == 0 and pb["apart_on_thursday"] >= 3
       and pb["apart_on_monday"] == 0 and same("a week's month taken from its Monday"))
    ok("SF28 same call: the stores and the records compared by calendar month",
       same("the stores and the records compared by calendar month"))
    ok("SF29 the App Store report's day column is date_pt, and reading its days as UTC is the same call",
       heads["apple"][0] == "date_pt" and heads["google"][0] == "date_utc" and same("the App Store's report days taken as UTC days"))
    ok("SF30 same call: the stores' refunds netted on the day of the refund, or from the renewals",
       same("the stores' refunds netted on the day of the refund", "the stores' refunds netted from their renewals"))
    ok("SF31 same call: the install week and the 365 days counted from the attribution export's install time, which is never "
       "after the account's created_at day",
       same("the install week and the 365 days counted from the attribution export's install time")
       and bool((O.inst_day <= O.created_day).all()))

    # ------------------------------------------------------------------------------------------------------------
    # the pinning list: each constant in its home
    # ------------------------------------------------------------------------------------------------------------
    ok("pin: the policy's text reads the same through two extractors on every filed sentence",
       all(both(s) for s in ("EUR 9.99 a month and EUR 59.99 a year, each with a seven-day free trial",
                             "1.20 or more", "under 0.90", "The policy is reviewed each September")))
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
    ok("pin: the billing cadence measured on the events is a twelfth of a year (mean gap %.4f days)" % gaps.mean(),
       abs(gaps.mean() - C.MONTH_DAYS) < 0.02 and set(gaps.unique()) <= {30, 31} and fig["policy"]["cadence_days"] == 30.4375)
    for name, want in (("Google Play", (0.034, 0.041, 0.971)), ("App Store", (0.030, 0.034, 0.970))):
        s_ = fig["stores"][name]
        ok("pin: %s's fitted shares and continuation are the note's (%.3f, %.3f, %.3f)" % (
            name, s_["trial_end_share_monthly"], s_["trial_end_share_annual"], s_["continuation"]),
           (s_["trial_end_share_monthly"], s_["trial_end_share_annual"], s_["continuation"]) == want)
    ok("pin: each source's fitted ratio is the note's",
       {c: x["ratio"] for c, x in rs.items()} == {"Meta iOS": 0.435, "TikTok iOS": 0.517, "Snapchat iOS": 0.614,
                                                  "Google iOS": 0.898, "Pinterest iOS": 0.808, "organic iOS": 0.888},
       {c: x["ratio"] for c, x in rs.items()})
    ds = [ch[c]["delivery_share"] for c in C.ORDER]
    ok("pin: each channel's spend over its budget across the 104 weeks is 0.83 to 0.87 (%.3f to %.3f)" % (min(ds), max(ds)),
       0.83 <= min(ds) and max(ds) <= 0.875)
    ok("pin: a postback arrives three or four days after its install, never sooner (the schema's timer)",
       sorted(set(W["pb_lag"][np.isin(W["src"], [C.ORDER.index(c) for c in C.GATED])].tolist())) == [3, 4] and C.PB_ALIGN == "split")

    # ------------------------------------------------------------------------------------------------------------
    # what is never filed, and no file that describes the pack
    # ------------------------------------------------------------------------------------------------------------
    alltext = " ".join(texts.values()) + " " + " ".join(h for hs in heads.values() for h in hs)
    for word in ("dormant", "silent", "forgotten", "next open", "next sync", "next opened", "pacing", "underspend", "under-spend",
                 "auction", "delivery", "delivered", "worth less", "worth more", "convert worse", "lower quality", "bought blind",
                 "signal loss", "modelled conversion", "adjustment factor", "unattributed", "what we control", "trust",
                 "churn", "continuation", "lapse"):
        ok("never filed: '%s'" % word, word not in alltext.lower())
    ok("no file or sheet describes the pack",
       not any(re.search(r"readme|dictionary|data_dict|notes|manifest|field_|glossary|about", n_, re.I) for n_ in os.listdir(T))
       and not any(re.search(r"readme|dictionary|notes|about|legend|definitions", ws.title, re.I)
                   for k in ("plan", "budget") for ws in load_workbook(f(k))))
    log = list(load_workbook(f("budget"), read_only=True)["Changes"].iter_rows(values_only=True))[1:]
    reasons = [r[5] for r in log]
    written = [x for x in reasons if x]
    ok("the budget sheet's reasons never name the platform's side (%d notes, %d distinct, %d rows left empty)" % (
        len(written), len(set(written)), len(reasons) - len(written)),
       not any(re.search(r"cpm|cpi|bid|compet|inventory|price|expensive|cheap|auction|deliver|pacing|perform", x, re.I)
               for x in written)
       and len(set(written)) >= 40 and len(reasons) - len(written) >= 20
       and max(written.count(x) for x in set(written)) <= 0.12 * len(reasons))
    opened = [r[5] for r in log if r[3] != "back to base" and r[5]]
    ok("no reason for a budget move is written twice in the same words (%d reasons on %d moves)"
       % (len(opened), sum(1 for r in log if r[3] != "back to base")), len(opened) == len(set(opened)) and len(opened) >= 50)

    # ------------------------------------------------------------------------------------------------------------
    # the realism sweep
    # ------------------------------------------------------------------------------------------------------------
    def steps(vals):
        d = np.diff(np.sort(np.asarray(vals, dtype=np.int64)))
        return len(set(d[d > 0].tolist()))
    ok("realism: account ids are not a sequence", steps([int(x[3:], 16) for x in acc.account_id[:20000]]) > 1000)
    ok("realism: billing event ids are not a constant step", steps([int(x[2:]) for x in bil.event_id[:20000]]) > 5)
    ok("realism: install ids are not a sequence", steps([int(x, 16) for x in att.install_id[:20000]]) > 1000)
    ok("realism: campaign ids are not a constant step", steps(sp.campaign_id.unique().astype(np.int64)) > 20)
    ok("realism: account creation times have no fixed step", steps(A.secs(acc.created_at[:20000])) > 200)
    ok("realism: the channels are not listed in alphabetical order anywhere", list(C.ORDER) != sorted(C.ORDER) and MEM != sorted(MEM))
    shapes = {re.sub(r"[A-Za-z]+", "a", re.sub(r"\d+", "9", x)) for x in sp.campaign_name.unique()}
    ok("realism: campaign names take %d shapes" % len(shapes), len(shapes) > 4)
    by_ = [r[6] for r in log]
    ok("realism: the change log's authors and sizes are uneven", len(set(by_)) == 2 and
       max(by_.count(x) for x in set(by_)) > 2 * min(by_.count(x) for x in set(by_))
       and len({r[3] for r in log if r[3] != "back to base"}) >= 6)
    ok("realism: no channel spends the same amount in two weeks",
       all(len(set(np.round(O.B[c]["spend"], 2).tolist())) == C.WEEKS for c in C.ORDER))
    ok("realism: weekly budgets are rounded as a sheet kept by hand is, spend is to the cent",
       all((O.B[c]["budget"] % 10 == 0).all() for c in C.ORDER) and bool((sp.spend_eur.str.contains(r"\.\d\d$")).all()))
    cnt = acc.account_type.value_counts()
    ok("realism: staff and test accounts are a sliver of the accounts (%d and %d)" % (cnt["staff"], cnt["test"]),
       cnt["staff"] != cnt["test"] and cnt["staff"] + cnt["test"] < 0.001 * len(acc))
    ok("realism: the App Store's report is on Pacific days (its first-charge days differ from the records' UTC days)",
       not np.array_equal(O.view(pt=False).mon, O.mon))
    wk = np.array([O.agg[c] for c in C.ORDER])
    ok("realism: no channel's weekly installs repeat a level four weeks running, and none is a round number throughout",
       all(max(len(list(grp)) for _k, grp in itertools.groupby(np.round(wk[i]).tolist())) < 4 for i in range(len(C.ORDER))))
    live = {c: sum(x for x in ch[c]["live_weeks"].values()) for c in C.ORDER}
    ok("realism: campaigns start and stop market by market at uneven weeks (live market-weeks %d to %d of 312)" % (
        min(live.values()), max(live.values())), len(set(live.values())) >= 6 and min(live.values()) < 300)

    # ------------------------------------------------------------------------------------------------------------
    # the input gates
    # ------------------------------------------------------------------------------------------------------------
    files = sorted(os.listdir(T))
    ok("gate: %d usable files in the pack" % len(files), len(files) >= 10 and not any(n_.startswith((".", "~")) for n_ in files))
    ext = {os.path.splitext(n_)[1] for n_ in files}
    ok("gate: spreadsheet, text and code categories (%s)" % ", ".join(sorted(ext)), {".csv", ".xlsx", ".pdf", ".json"} <= ext)
    rows = {n_: sum(1 for _ in open(os.path.join(T, n_))) - 1 for n_ in files if n_.endswith(".csv")}
    ok("gate: two large CSVs (%s)" % ", ".join("%s %d" % (n_, r) for n_, r in rows.items() if r >= 20000),
       sum(r >= 20000 for r in rows.values()) >= 2 and sum(r >= 600 for r in rows.values()) >= 3)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    ok("gate: every shipped file has its source, date and licence in metadata.json, outside the pack",
       set(meta["files"]) == set(files) and all({"source", "pulled", "license"} <= set(x) for x in meta["files"].values())
       and "metadata.json" not in files)
    ok("gate: %d distractors, named only in metadata.json" % len(dis),
       len(dis) >= 2 and all(n_ in files for n_ in dis) and not any(re.search(r"distract|unused|decoy|extra", n_, re.I) for n_ in files))
    lean = tempfile.mkdtemp(prefix="task1-lean-")
    for n_ in files:
        if n_ not in dis:
            os.symlink(os.path.join(T, n_), os.path.join(lean, n_))
    r = A.route(A.PackObs(lean))
    ok("gate: with the distractors deleted every figure is unchanged", all(r[c][k] == g[c][k] for c in MEM for k in KEYS7))
    shutil.rmtree(lean)
    ok("gate: cross-file work: no single file holds installs, charges and spend together",
       not any({"spend_eur", "amount_eur"} <= set(h) for h in heads.values())
       and not any({"account_id", "spend_eur"} <= set(h) for h in heads.values()))
    size = sum(os.path.getsize(os.path.join(T, n_)) for n_ in files)
    ok("gate: the pack is %.0f MB unzipped" % (size / 1e6), size > 30e6)

    # ------------------------------------------------------------------------------------------------------------
    # the goldens and the blocks
    # ------------------------------------------------------------------------------------------------------------
    ok("golden: exactly the two requested files", sorted(os.listdir(G)) == sorted(deliver.FILES.values()))
    rows_ = list(csv.reader(open(os.path.join(G, deliver.FILES["csv"]))))
    order_ = deliver.order(fig)
    cols = [k for k, _h, _n in deliver.COLS]
    ok("golden CSV: one row per channel with the band and the seven figures, as figures.json states them",
       [r_[0] for r_ in rows_[1:]] == order_ and len(rows_[0]) == 9 and all(
           r_[1] == fig["bands"][r_[0]] and all(float(r_[2 + j]) == fig[k][r_[0]] for j, k in enumerate(cols)) for r_ in rows_[1:]))
    gw = load_workbook(os.path.join(G, deliver.FILES["wb"]))
    ws = gw.worksheets[0]
    ok("golden workbook: the first sheet states the call and each channel's row",
       str(ws["A1"].value) == "2027 media plan: scale %s, hold %s, cut %s" % tuple(
           deliver._list(fig["by_band"][b]) for b in ("scale", "hold", "cut"))
       and [ws.cell(row=6 + i, column=1).value for i in range(7)] == order_
       and all(ws.cell(row=6 + i, column=2).value.lower() == fig["bands"][c]
               and all(ws.cell(row=6 + i, column=3 + j).value == fig[k][c] for j, k in enumerate(cols))
               for i, c in enumerate(order_)))
    ok("golden workbook: named sheets, a chart on the first, frozen headers",
       [w_.title for w_ in gw] == ["Bands 2027", "Unrecorded charges", "Unnamed installs", "Budget response", "Ranges", "Routes"]
       and len(ws._charts) == 1 and all(w_.freeze_panes for w_ in gw))
    bad = []
    for w_ in gw:
        for row_ in w_.iter_rows():
            for c_ in row_:
                try:
                    c_.font, c_.fill, c_.border, c_.alignment, c_.number_format
                except Exception as e:                      # a format pointing outside the style table
                    bad.append((w_.title, c_.coordinate, e.__class__.__name__))
    ok("golden workbook: every cell's font, fill, border and number format resolves in the style table", not bad, bad[:3])
    h_ = ws["A5"]
    ok("golden workbook: the header row reads white on its dark fill with a rule beneath",
       not bad and h_.font.b and h_.font.color is not None and h_.font.color.rgb == "FFFFFFFF"
       and h_.fill.fgColor.rgb == "FF22364F" and h_.border.bottom.style == "thin")
    again = os.path.join(tmp, "golden")
    MK.goldens(fig, again)
    ok("golden: both files rebuilt from figures.json as filed are byte-identical", digest(again) == digest(G))
    rg = gw["Ranges"]
    ok("golden workbook: the ranges sheet carries each figure's range as the blocks state it",
       all(rg.cell(row=5 + i, column=1).value == c and all(
           [rg.cell(row=5 + i, column=3 + 3 * j + d).value for d in range(3)] == [fig[k][c]] + list(fig[k + "_band"][c])
           for j, k in enumerate(cols)) for i, c in enumerate(order_)))
    sub = open(os.path.join(TASK, "submission.md")).read()
    runs_in = os.path.exists(os.path.join(WU.RUNS_DIR, WU.RESPONSES[1]["file"]))
    ok("blocks: the tags and the four blocks, the stump question first after the recommendation once the responses are "
       "on file, no em dash, no table",
       [h for h in re.findall(r"^## (.+)$", sub, re.M)] == ["Tags", "Final Recommendation"] + [WU.STUMP] * runs_in + [
           "Supplementary Questions", "Critical Components", "Step-by-Step"]
       and "\u2014" not in sub and "|" not in sub)
    if runs_in:
        stump = sub.split("## " + WU.STUMP)[1].split("## Supplementary Questions")[0]
        said = {n: open(os.path.join(WU.RUNS_DIR, r["file"])).read() for n, r in WU.RESPONSES.items()}
        r1 = WU.RESPONSES[1]
        ok("stump block: every figure and phrase it takes from a response is in that response's own text (%d and %d), "
           "and the second response never names a store" % (len(WU.quoted(r1)), len(WU.quoted(WU.RESPONSES[2]))),
           all(q in said[n] for n, r in WU.RESPONSES.items() for q in WU.quoted(r)) and "store" not in said[2].lower())
        ok("stump block: the first response's figures at the blocks' precision beside the CSV's, and the question's "
           "three parts in order",
           all(("%.3f where it is a hold at %.3f" % (float(r1["returns"][c]), fig["return_plan"][c])) in stump
               for c in ("Meta iOS", "AppLovin Android"))
           and all(("EUR %.2f each against %.2f" % (float(r1["paid"][c]), fig["paid_per_install"][c])) in stump
                   for c in r1["paid"])
           and ("(%.3f against %.3f)" % (float(r1["returns"]["Google Android"]),
                                         fig["return_plan"]["Google Android"])) in stump
           and ("(%s to %s against %s to %s)" % tuple("0" + x for x in WU.RESPONSES[2]["factors"])) in stump
           and stump.index("**Response 1**") < stump.index("**Response 2**") < stump.index("**Why it is fair.**")
           < stump.index("**Why it takes rigour.**"))
    ok("blocks: every return in the recommendation is the CSV's", all(("%s %.3f" % (c, fig["return_plan"][c])) in sub for c in MEM))
    supp = sub.split("## Supplementary Questions")[1].split("## Critical Components")[0]
    ok("blocks: four numbered entries, one per ask, seven lines each",
       re.findall(r"^(\d)\. ", supp, re.M) == ["1", "2", "3", "4"] and len(re.findall(r"^   [a-g]\. ", supp, re.M)) == 28)
    walk = sub.split("## Step-by-Step")[1]
    CW = fig["check_web"]
    ok("SF36 a postback half dated before the first install week: step 1 counts it in that week (%d installs)" % (
        fig["steps"]["early_postback_installs"]),
       ("a half dated before 4 November 2024 is counted in the week of 4 November 2024 (%d installs in all)" % (
           fig["steps"]["early_postback_installs"])) in walk)
    ok("SF37 a trial starter with no subscription at its last open: step 4 counts it to its platform's store",
       "a trial starter with no subscription at its last open counts to its platform's store" in walk)
    ok("SF38 an iOS network's worth at a first-48-hour value: step 6 takes its named and unnamed installs together",
       "what its named and unnamed installs of that value came to together under step 5" in walk)
    ok("SF39 the scaling on the web check: step 4 states it, and it puts %.2f where EUR %.2f was charged (%.2f with one "
       "factor for the whole record, %.2f by the fit)" % (CW["true_up"], CW["charged"], CW["true_up_one_factor"], CW["estimate"]),
       "each of their charges up to the last open raised by" in walk and "in the charge's period, less one" in walk
       and CW["true_up"] < 0.5 * CW["charged"] and CW["true_up_one_factor"] < 0.6 * CW["charged"]
       and abs(CW["estimate"] - CW["charged"]) < 0.02 * CW["charged"])
    comp = sub.split("## Critical Components")[1].split("## Step-by-Step")[0]
    lines = [x for x in comp.strip().split("\n") if x.strip()]
    ok("blocks: three components, each the answer with its unit and range and no method word",
       len(lines) == 3 and not re.search(r"fitted|regress|ratio|scaled|trued|adjust|correct|once|after|budget|store|postback|"
                                         r"unnamed|record", comp, re.I)
       and all(("%.2f" % fig["components"][s]["value"]) in lines[i] for i, s in enumerate(("S1", "S2"))) and
       ("**%d installs a week**" % fig["components"]["S3"]["value"]) in lines[2])
    for s, fid in C.COMPONENTS.items():
        c = OPEN[s]
        k = RS.FAM_KEY[fid[:-len(c)]]
        ok("blocks: component %s is in the CSV and on the workbook's first sheet under its own column" % s,
           fid.endswith(c) and float(dict((r_[0], r_) for r_ in rows_[1:])[c][2 + cols.index(k)]) == fig["components"][s]["value"])
    ok("prompt: under 1,000 characters, names no file, no method and no role",
       not any(os.path.splitext(n_)[0] in prompt or n_ in prompt for n_ in files) and len(prompt.strip()) < 1000
       and not re.search(r"postback|consent|tracking|budget|auction|store report|round|regress|model|attribut|organic|billing|"
                         r"renew|trial|deliver", prompt, re.I))
    nums = set(re.findall(r"\d+(?:\.\d+)?", prompt))
    ok("prompt: the only figures in it are dates and the twelve months (%s)" % ", ".join(sorted(nums)),
       nums <= {"2027", "2028", "2026", "2025", "8", "2", "12"})
    ok("prompt: it asks for each step's own quantity in the decision's words",
       "how many installs a week the plan's spend will buy" in prompt
       and "the revenue per install of the installs each channel bought in the year to 2 November 2025" in prompt
       and "on top of the plan's weekly spend and on top of its stretch spend" in prompt
       and "with every money figure in euros of 12-month net revenue" in prompt)
    shutil.rmtree(tmp)
    print("\n%d passed, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
