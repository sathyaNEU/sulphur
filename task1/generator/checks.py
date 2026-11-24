"""task1 architecture 8: the build's assertions, run on the cut pack (target/), the goldens and the two json files.

    python3 task1/generator/checks.py

The bar block (labels R1 to R7), every row of the design note's fork table (SF1 to SF41), the pinning list, the pack
against the simulation it was written from, mess neutrality, the forcing on both sides, the realism sweep, the input
gates, the goldens, the answer blocks and the prompt. It rebuilds the pack once into a scratch folder (the
byte-identical check, and the account order the array comparison needs)."""
import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
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
OPEN = C.OWN
KEYS7 = ("roas", "installs_week", "vpi", "v12", "pay100")
# the groupings of sources the battery carries, as sets of sources
# the groupings the design note's SF23 says the fit's own test cannot refuse (core.GROUPS: TikTok iOS with Snapchat iOS)
GROUPED = {frozenset(g) for k in ("pair2", "ps", "pt", "pst") for g in C.GROUPS[k]}


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
    vc = C.values(Oc)                                              # the core's own values on the simulation
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
    worst = max(abs(g[c][k] / core_gold[c][k] - 1) for c in C.ORDER for k in KEYS7)
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
    # the core's lattice on the simulation: the bands each stump lost alone moves, the reflex route's bands, and how
    # many different wrong calls the seven routes file
    lat_c = {k: C.route(Oc, **{kk: vv for s_ in k.split("+") for kk, vv in C.HURRIED[s_].items()}) for k in RS.KEYS}
    gb_c = [C.band(core_gold[m]["roas"]) for m in MEM]
    WRONG_ALONE = {s: [m for m, b_ in zip(MEM, gb_c) if C.band(lat_c[s][m]["roas"]) != b_] for s in ("S1", "S2", "S3")}
    for s, fid in C.COMPONENTS.items():
        fv = C.figure_values(lat[s])
        ok("R3 %s lost alone files %s at %s, outside %s by %.0f per cent of the figure" % (
            s, fid, RS.stated(fid, fv[fid]), fig["figure_band"][fid], 100 * gap(fid, fv[fid], fig)), gap(fid, fv[fid], fig) > 0.05)
        others = [x for t, x in C.COMPONENTS.items() if t != s]
        ok("R3 %s lost alone leaves the other two steps' own figures inside their ranges (%s)" % (
            s, ", ".join("%s %s" % (x, RS.stated(x, fv[x])) for x in others)),
           all(in_band(x, fv[x], fig) for x in others), [(x, fv[x]) for x in others])
        wrong = [m for m in MEM if C.band(lat[s][m]["roas"]) != fig["bands"][m]]
        ok("R3 %s lost alone moves its own channel %s to another band (%s)" % (s, OPEN[s], ", ".join(wrong)),
           OPEN[s] in wrong and wrong == WRONG_ALONE[s], wrong)
        moved = [m for m in MEM if not in_band("return " + m, lat[s][m]["roas"], fig)]
        moved_c = [m for m in MEM if not in_band("return " + m, lat_c[s][m]["roas"], fig)]
        ok("R3 %s lost alone misstates %d channels' returns, as the core's lattice does on the simulation (four or more%s)" % (
           s, len(moved), "; the four iOS networks it moves out of range, the core's own, disclosed" if s == "S2" else ""),
           moved == moved_c and len(moved) >= 4 and OPEN[s] in moved, (moved, moved_c))
    reflex_c = C.figure_values(lat_c["S1+S2+S3"])
    # payments: the core's reflex route lands Google iOS's by offsetting errors (the author's ruling of 2026-11-24, disclosed)
    for nm, lim in (("return ", 2), ("payments per 100 ", 1)):
        inside = [c for c in MEM if in_band(nm + c, reflex[nm + c], fig)]
        inside_c = [c for c in MEM if in_band(nm + c, reflex_c[nm + c], fig)]
        ok("R3 the reflex route lands %d of 7 of '%s' inside the ranges (%s), as the core's reflex route on the simulation "
           "does, by offsetting errors" % (len(inside), nm.strip(), ", ".join(inside) or "none"),
           inside == inside_c and len(inside) <= lim, (inside, inside_c))
    for nm in ("installs the plan buys", "revenue the plan's installs bring"):
        ok("R3 the reflex route files %s at %s, outside %s" % (nm, RS.stated(nm, reflex[nm]), fig["figure_band"][nm]),
           not in_band(nm, reflex[nm], fig))
    rb = {c: C.band(lat["S1+S2+S3"][c]["roas"]) for c in MEM}
    rb_c = {c: C.band(lat_c["S1+S2+S3"][c]["roas"]) for c in MEM}
    ok("R3 the reflex route files the core's bands on the simulation (%s), a wrong call" % rb,
       rb == rb_c and RS.call_of(lat["S1+S2+S3"]) != fig["call"], rb_c)
    nd_c = len({tuple(RS.call_of(r)) for r in lat_c.values()})
    ok("R3 the seven shortcut routes file %d different wrong calls, as on the simulation" % fig["distinct_wrong_calls"],
       fig["distinct_wrong_calls"] == nd_c >= 5 and all(RS.call_of(lat[k]) != fig["call"] for k in RS.KEYS))
    ok("R3 the records as they stand file a wrong band on five channels or more",
       sum(C.band(direct[c]["roas"]) != fig["bands"][c] for c in MEM) >= 5, [C.band(direct[c]["roas"]) for c in MEM])
    rv_c = RS.result_values(C.figure_values(lat_c["S1+S2+S3"]), RS.call_of(lat_c["S1+S2+S3"]))
    for rid in ("R1", "R2", "R3", "R4", "R5", "R6"):
        gr = EF.grade(by[rid]["passes"]["careful"], by[rid])[0]
        gr_c = EF.grade(rv_c[rid], by[rid])[0]
        ok("R3 effort.json grades the careful pass %s on %s, as the core's reflex route on the simulation grades" % (gr, rid),
           gr == gr_c and gr != "right", gr_c)
    sc = fig["shortcuts"]
    # the frozen core's secondary rungs, each with the first step made, disclosed in the note (the author's ruling of 2026-11-24: ship as
    # designed): three keep their own step's figure or file no band wrong, six earn over 50
    DISCLOSED_RUNGS = {"markets_pooled", "full_delivery_rescaled", "on_spend"}
    OVER_50 = {"android", "one_ratio", "markets_pooled", "full_delivery_rescaled", "on_spend", "last_year"}
    ok("R3 the simpler ways that earn over 50 are the six the note discloses, each with the first step made (%s)" % (
        ", ".join("%s %.1f" % (k, sc[k]["earns"]) for k in sorted(sc) if sc[k]["earns"] > 50)),
       {k for k in sc if sc[k]["earns"] > 50} == OVER_50 and all("S1" in sc[k]["components_kept"] for k in OVER_50))
    for key in sc:
        x = sc[key]
        kw_ = next(k_ for st_, ky_, _r, k_ in RS.SHORTCUTS if ky_ == key)
        rc_ = C.route(Oc, **kw_)
        wrong_c = [c for c, b_ in zip(MEM, gb_c) if C.band(rc_[c]["roas"]) != b_]
        ok("R3 the simpler way '%s' (%s) files %s wrong, as on the simulation, %s "
           "(earns %.1f%s)" % (x["rule"][:70], x["step"], ", ".join(x["wrong"]) or "no band",
                              "a disclosed rung that keeps a band or its own step's figure" if key in DISCLOSED_RUNGS
                              else "and loses a band and its own step's figure", x["earns"],
                              "; disclosed in the note" if x["earns"] > 50 else ""),
           x["wrong"] == wrong_c and (bool(x["wrong"]) and x["step"] not in x["components_kept"] or key in DISCLOSED_RUNGS),
           (x["wrong"], wrong_c, x["components_kept"]))
    for step, key in (("S1", "as_recorded"), ("S2", "borrowed_shift"), ("S3", "full_delivery")):
        ok("R3 '%s' priced as a simpler way is the lattice's %s lost alone (%.1f)" % (key, step, sc[key]["earns"]),
           sc[key]["earns"] == fig["rubric"]["one_lost"][step])
    ok("R3 the fit on billed spend, the other two steps as estimated, keeps the plan's installs inside their range "
       "(%s) and files %s wrong" % (sc["on_spend"]["plan"]["installs"], ", ".join(sc["on_spend"]["wrong"])),
       "S3" in sc["on_spend"]["components_kept"] and len(sc["on_spend"]["wrong"]) >= 1)    # the core's one band, disclosed
    ru = fig["rubric"]["runs"]
    ok("R3 every run route and setting earns 50 or under on the rubric (highest %.1f)" % fig["rubric"]["runs_max"],
       len(ru) == len(C.RUNS) and all(x is not None and x <= 50 for x in ru.values()), ru)

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
    raw_c = C.route(Oc, s1="raw")
    un_c = {c: 100 * (1 - float(raw_c[c]["v12"]) / float(core_gold[c]["v12"])) for c in ch}
    # Meta iOS's subscribers rarely go silent: its records stand at the core's own -0.4 (the author's ruling of 2026-11-24, disclosed)
    lack = sorted(c for c in ch if ch[c]["unrecorded_pct"] >= 2)
    ok("R5 the records lack 2 per cent or more of every channel's twelve-month revenue (%.1f to %.1f per cent, the core's on "
       "the simulation; 2 per cent or more on %d of 8, short on %s), the most on AppLovin Android" % (
           min(x["unrecorded_pct"] for x in ch.values()), max(x["unrecorded_pct"] for x in ch.values()), len(lack),
           ", ".join(sorted(set(ch) - set(lack)))),
       len(ch) == 8 and set(ch) - set(lack) <= {"Meta iOS"} and max(ch, key=lambda c: ch[c]["unrecorded_pct"]) == C.OWN["S1"]
       and all(abs(ch[c]["unrecorded_pct"] - un_c[c]) <= 0.3 for c in ch), {c: (ch[c]["unrecorded_pct"], round(un_c[c], 1)) for c in ch})
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
    nets = {c: rs[c] for c in C.GATED}
    ok("R5 on every iOS network an unnamed install is worth less than a named one of the same first-48-hour value, by "
       "more than two of the fit's standard errors (%.3f to %.3f); the organic installs' ratio, which no network buys or "
       "steers, is reported, not graded (%.3f, standard error %.3f)" % (
           min(x["ratio"] for x in nets.values()), max(x["ratio"] for x in nets.values()), rs["organic iOS"]["ratio"],
           rs["organic iOS"]["se"]),
       len(rs) == 6 and len(nets) == 5 and all(x["ratio"] + 2 * x["se"] < 1 for x in nets.values()))
    ok("R5 the same holds where the declined installs are named: Apple Search Ads %.2f, Android %s" % (
        fig["ratios"]["search_ads_ratio"], fig["android_ratios"]),
       fig["ratios"]["search_ads_ratio"] < 0.95 and all(x < 0.9 for x in fig["android_ratios"].values()))
    ok("R5 every iOS network's named installs are worth more than its installs as a whole",
       all(ch[c]["named_value"] > 1.1 * ch[c]["paid_per_install"] for c in C.GATED))
    sd = {c: float(np.std(np.log(O.B[c]["spend"] / O.B[c]["budget"]))) for c in C.ORDER}
    ok("R5 the share of the budget spent moves week to week on all eight channels (sd of the log %.2f to %.2f)" % (
        min(sd.values()), max(sd.values())), min(sd.values()) > 0.05)
    ok("R5 fitted on spend, installs respond more steeply than on the budget on all eight channels",
       all(ch[c]["spend_fit_elasticity"] > ch[c]["budget_elasticity"] + 0.1 for c in C.ORDER))
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
    row_ = [r for r in fig["rubric"]["rows"] if r[0] == "one stump fixed alone earns more, a third at most"]
    ok("R6 corelib on the cut pack: no sentence adds more than a third of the rubric to the reflex route (%s over the "
       "reflex route's %.1f; corelib's own row %s)" % (fig["rubric"]["fixed_alone"], fig["rubric"]["reflex"], row_[0][1] if row_ else "missing"),
       max(fig["rubric"]["fixed_alone"].values()) - fig["rubric"]["reflex"] <= 100 / 3.0 and bool(row_) and row_[0][1] == "PASS")

    # ------------------------------------------------------------------------------------------------------------
    # R7: the rivals, and the forcing on both sides
    # ------------------------------------------------------------------------------------------------------------
    n = fig["variant_counts"]
    sg, bes, xr = X["singles"], X["beside"], X["crossed"]
    nb = n["beside"]
    ways = C.crossed_ways(A.SINGLES)
    ok("R7 the battery holds %d single ways (core's %d and the files' %d) and %d crossings from core.crossed_ways on them "
       "(core's own %d among them, the files' conventions crossed by the same rule)" % (
           n["singles"], len(C.VARIANTS), len(A.PACK_VARIANTS), n["crossings"], n["core_crossings"]),
       n["singles"] == len(sg) == len(C.VARIANTS) + len(A.PACK_VARIANTS) == fig["variants"]
       and n["crossings"] == len(xr) == len(ways) and [x[0] for x in xr] == [w[0] for w in ways]
       and n["core_crossings"] == len(C.crossed_ways()) and n["pack_crossings"] == len(xr) - n["core_crossings"]
       and len({x[0] for x in xr} | set(names)) == len(xr) + len(names)
       and not any(nm.split("; ")[0] in dict(C.BESIDE) and not b for nm, _f, b, _c in xr))
    BS = fig["beside"]
    ok("R7 %d more ways stand beside the battery: the second step's fit on finer rows (%d), the installs equation's "
       "unrescaled prediction (%d), the first-48-hour values grouped on one part of them (%d) and the value equation on "
       "the complete weeks (%d)" % (nb, BS["finer_rows"]["ways"], BS["unrescaled"]["ways"],
                                    BS["grouped"]["ways"], BS["value_weeks"]["ways"]),
       nb == len(C.BESIDE) == 17 and [x for x, _r in bes] == [x for x, _k in C.BESIDE] == BS["names"]
       and (BS["finer_rows"]["ways"], BS["unrescaled"]["ways"], BS["grouped"]["ways"], BS["value_weeks"]["ways"]) == (6, 6, 4, 1))
    XR = fig["crossed"]
    bad = [nm for nm, r in sg + bes if RS.call_of(r) != fig["call"]]
    ok("R7 every way files the golden's call: the %d singles, the %d beside the battery and all %d crossings (%d ways; "
       "the nearest crossing to a line %s at %.3f, %s)" % (len(sg), len(bes), len(xr), XR["ways"], XR["nearest"]["channel"],
                                                         XR["nearest"]["return_plan"], XR["nearest"]["variant"]),
       not bad and not XR["moved"] and XR["ways"] == len(sg) + len(bes) + len(xr), (bad[:3], XR["moved"][:3]))
    gfv = C.figure_values(g)
    sf, bf = [C.figure_values(r) for _n, r in sg], [C.figure_values(r) for _n, r in bes]
    ly = X["layered"]
    off = [fid for fid in fids if fig["figure_band"][fid] != list(RS.band_of(
        fid, gfv[fid], [x[fid] for x in sf] + [fv[fid] for _n, fv, b, _c in xr + ly if not b],
        [x[fid] for x in bf] + [fv[fid] for _n, fv, b, _c in xr + ly if b]))]
    outside = [(nm, fid) for nm, fv in [(nm, x) for (nm, _r), x in zip(sg + bes, sf + bf)] + [(x[0], x[1]) for x in xr + ly]
               for fid in fids if not fig["figure_band"][fid][0] <= fv[fid] <= fig["figure_band"][fid][1]]
    ok("R7 every range is core.band_of over the singles, every crossing and every layered way, reaching %.0f per cent of "
       "the figure past the ways beside the battery and every crossing or layered way that holds one, and every way's "
       "every figure sits inside it (%d layered ways, %d ranges they widen)"
       % (100 * RS.BESIDE_PAD, len(ly), len(fig["layered"]["widened"])), not off and not outside, (off[:4], outside[:4]))
    pw = fig["pack_widened"]
    ok("R7 the files' conventions and their crossings widen %d of core's ranges (reported, figure by figure, with the "
       "way: %s)" % (len(pw), "; ".join("%s %s to %s against %s to %s" % (k, x["pack"][0], x["pack"][1], x["core"][0],
                                                                          x["core"][1]) for k, x in sorted(pw.items())[:6])),
       all(x["pack"][0] <= x["core"][0] and x["core"][1] <= x["pack"][1] for x in pw.values())
       and all(pw[k]["pack"] == fig["layered"]["widened"][k]["crossed"] for k in pw if k in fig["layered"]["widened"]))
    ok("R7 Meta iOS's return range stays under the scale line (%s to %s, against 1.20)" % tuple(fig["figure_band"]["return Meta iOS"]),
       fig["figure_band"]["return Meta iOS"][1] < C.LINES[1])
    near = min(abs(r[c]["roas"] - l) for _n, r in sg + [("golden", g)] for c in MEM for l in C.LINES)
    ok("R7 no single way brings a channel within 0.04 of a line (nearest %.3f, %s)" % (near, fig["nearest_variant"]["variant"]),
       near >= 0.04 and abs(near - fig["nearest_variant"]["distance"]) < 0.001)
    near_b = min(abs(r[c]["roas"] - l) for _n, r in bes for c in MEM for l in C.LINES)
    ok("R7 no way beside the battery brings a channel within 0.01 of a line (nearest %.3f, %s, %s)" % (
        near_b, fig["nearest_beside"]["channel"], fig["nearest_beside"]["variant"]),
       near_b >= 0.01 and abs(near_b - fig["nearest_beside"]["distance"]) < 0.001)
    # the readings the blocks refuse by a figure from the files
    PM = fig["pooled"]
    pp = C.pooled_pins(O, v)
    ppc = C.pooled_pins(Oc, vc)                                    # the core's pins on the simulation
    tk, gk = pp["ratio"]["TikTok iOS"], pp["ratio"]["Google iOS"]
    st_ = pp["split"]
    ok("SF32 the rows the ratios are fitted on: the six finer-row fits stand beside the battery and file the golden's "
       "call (above, R7); the ratios fitted on the %d weeks with the three markets summed file TikTok iOS %.3f (scale, "
       "its ratio %.3f against %.3f) and Google iOS %.3f (its ratio %.3f against %.3f), outside its range" % (
           C.MATURE, PM["return_plan"]["TikTok iOS"], tk["pooled"], tk["golden"], PM["return_plan"]["Google iOS"],
           gk["pooled"], gk["golden"]),
       PM["wrong"] == ["TikTok iOS"] and C.band(PM["return_plan"]["TikTok iOS"]) == "scale"
       and not in_band("return Google iOS", PM["return_plan"]["Google iOS"], fig)
       and same(*[n for n, k in C.BESIDE if "rows" in k]) and len([n for n, k in C.BESIDE if "rows" in k]) == 6)
    ok("SF32 pooled_pins on the files: each market's own weeks put TikTok iOS's ratio under the pooled %.3f (%s) and "
       "Google iOS's over the pooled %.3f (%s), and each market alone files the golden's call" % (
           tk["pooled"], ", ".join("%.3f" % x for x in tk["markets"]), gk["pooled"], ", ".join("%.3f" % x for x in gk["markets"])),
       all(x < tk["pooled"] for x in tk["markets"]) and all(x > gk["pooled"] for x in gk["markets"])
       and all(RS.call_of(A.route(O, markets=(m,))) == fig["call"] for m in range(3)))
    ok("SF32 pooled_pins on the files: TikTok iOS's %d live and %d dark market-weeks priced at the pooled ratios at %.3f and "
       "%.3f against the golden's %.3f and %.3f (pooled_pins on the simulation within 0.003), every network's live "
       "and dark weeks at the golden's within %s; the Wald distance %.1f on %d degrees of freedom against %.2f" % (
           st_["TikTok iOS"]["live"], st_["TikTok iOS"]["dark"], st_["TikTok iOS"]["pooled"][0], st_["TikTok iOS"]["pooled"][1],
           st_["TikTok iOS"]["golden"][0], st_["TikTok iOS"]["golden"][1], PM["golden_split_range"], pp["wald"][0],
           pp["wald"][1], PM["wald_point"]),
       all((st_[c]["live"], st_[c]["dark"]) == (ppc["split"][c]["live"], ppc["split"][c]["dark"])
           and all(abs(st_[c][k][j] - ppc["split"][c][k][j]) <= 0.003 for k in ("pooled", "golden") for j in (0, 1))
           for c in st_)
       and abs(st_["TikTok iOS"]["pooled"][0] - st_["TikTok iOS"]["pooled"][1]) > 0.03
       and max(abs(x - 1) for x in PM["golden_split_range"]) < 0.03 and pp["wald"][0] > 5 * PM["wald_point"],
       {c: (st_[c], ppc["split"][c]) for c in st_})
    sp_ = PM["split_pack"]
    ok("SF32 the same split read off the spend export (a market-week a campaign spent in is live): TikTok iOS %d and %d "
       "market-weeks at %.3f and %.3f at the pooled ratios against %.3f and %.3f, the golden's within %s; the blocks "
       "state these" % (sp_["TikTok iOS"]["live"], sp_["TikTok iOS"]["dark"], sp_["TikTok iOS"]["pooled"][0],
                        sp_["TikTok iOS"]["pooled"][1], sp_["TikTok iOS"]["golden"][0], sp_["TikTok iOS"]["golden"][1],
                        PM["golden_split_pack_range"]),
       all(abs(x["pooled"][0] - x["pooled"][1]) > abs(x["golden"][0] - x["golden"][1]) for c, x in sp_.items()
           if c in ("TikTok iOS", "Google iOS"))
       and max(abs(x - 1) for x in PM["golden_split_pack_range"]) < 0.03     # the simulation split's own bound above
       and all(sp_[c]["live"] >= st_[c]["live"] for c in sp_))
    Fm = fig["forms"]
    GIm, MM = fig["check_moves"]["channels"]["Google iOS"], Fm["moved_missed_pct"]
    ok("SF34 the response's form: a straight line in the budget is refused in both of its forms (on the installs themselves "
       "it misses the moved weeks by %.1f per cent against the power form's %.1f and puts Google iOS's raised weeks over "
       "its lowered ones at %.3f against %.3f counted; on the log of installs the log of the budget added to it gives F %.1f) "
       "and an exponential likewise (F %.1f, the moved weeks missed by %.1f), the power form is not by the budget added to it "
       "(%.1f), against %.2f; either line would file the seven bands" % (
           MM["line"], MM["power"], Fm["line_raised_over_lowered"], GIm["actual"], Fm["line"], Fm["exponential"],
           MM["exponential"], Fm["power"], Fm["point"]),
       Fm["line"] >= Fm["point"] + 0.5 and Fm["exponential"] > 10 * Fm["point"] and Fm["power"] < Fm["point"]
       and MM["line"] > MM["power"] and MM["exponential"] > MM["power"]
       and MM["power"] == fig["check_moves"]["missed_pct"]["golden"]
       and not Fm["line_wrong"]["levels"] and not Fm["line_wrong"]["log"])
    ok("SF35 value per install held flat: every plan channel's value slope is below nought by %.1f or more of its "
       "spreads (%.2f to %.2f, the core's on the simulation)" % (
        Fm["value_slope_spreads"], Fm["value_slope_range"][0], Fm["value_slope_range"][1]),
       Fm["value_slope_spreads"] >= 4
       and [round(x, 2) for x in Fm["value_slope_range"]] == [round(f_(float(core_gold[c]["qs"]) for c in MEM), 2) for f_ in (min, max)])
    K_ = fig["carry"]
    UN = BS["unrescaled"]["return_span"]
    DL = fig["delivery"]
    DLc = RS.delivery_block(Oc)                                    # delivery_pins on the simulation
    ok("SF33 the installs equation's unrescaled prediction: put at the share of the budgets billed or week by week through "
       "the delivery term, over both years, the first or the second, it adds up to %.1f to %.1f per cent of every channel's "
       "installs of its own weeks and files the seven bands (AppLovin Android %.3f at the thinnest); put at the geometric "
       "mean of the weekly shares or at the median week's it falls %.1f to %.1f per cent short of some channel's (the forms "
       "kept %.1f at most)" % (K_["held_pct"][0], K_["held_pct"][1], UN["AppLovin Android"][0], K_["refused_short_pct"][0],
                                K_["refused_short_pct"][1], K_["held_short_pct"]),
       K_["held"] == [k + "_" + w for k in RS.CARRY_HELD for w in ("both_years", "first_year", "second_year")]
       and all(not K_["wrong"][k] for k in K_["held"])
       and K_["held_pct"][0] >= 96.0 and K_["held_pct"][1] <= 104.0
       and all(100 - min(K_["adds_up_pct"][k].values()) >= 4.0 for k in K_["refused"])
       and same(*[n for n, k in C.BESIDE if "carry" in k]))
    ok("SF33 full delivery refused by the plan's header and the record: billed %.1f to %.1f per cent of the budgets over the "
       "104 weeks, a whole budget in %d to %d weeks, the best quarter %.1f to %.1f per cent, and the fit at a share of one "
       "adds up to %.1f to %.1f per cent of the installs counted (delivery_pins on the simulation: %s)" % (
           100 * DL["share"][0], 100 * DL["share"][1], DL["whole"][0], DL["whole"][1], 100 * DL["best_quarter"][0],
           100 * DL["best_quarter"][1], DL["adds_up_pct"][0], DL["adds_up_pct"][1],
           {k: DLc[k] for k in ("share", "whole", "best_quarter", "adds_up_pct")}),
       all(abs(a_ - b_) <= 0.0015 for k in ("share", "best_quarter") for a_, b_ in zip(DL[k], DLc[k]))
       and DL["whole"] == DLc["whole"] and all(abs(a_ - b_) <= 0.2 for a_, b_ in zip(DL["adds_up_pct"], DLc["adds_up_pct"]))
       and DL["share"][1] < 0.90 and DL["best_quarter"][1] < 0.95 and DL["adds_up_pct"][0] > 120
       and "as the platforms bill it" in texts["plan"]
       and [C.band(lat["S3"][c]["roas"]) for c in ("Google iOS",)] == ["scale"])
    # a span is stated to the thousandth, so it may sit half a thousandth past the unrounded figure the range was set on
    room = lambda key, c, x: (fig[key + "_band"][c][0] + RS.BESIDE_PAD * abs(fig[key][c]) - 0.0005 <= x[0]
                              and x[1] <= fig[key + "_band"][c][1] - RS.BESIDE_PAD * abs(fig[key][c]) + 0.0005)
    GD, VW = BS["grouped"], BS["value_weeks"]
    ok("SF40 the groups the first-48-hour values are priced in: the eight and the four of the battery, and beside it the "
       "sessions bucket alone (eight values or four pairs) and the flags alone (four groups, or eight with the sessions "
       "split in two); each of the four files the seven bands, Meta iOS's return at %.3f to %.3f, inside its range" % (
           GD["return_plan"]["Meta iOS"][0], GD["return_plan"]["Meta iOS"][1]),
       GD["ways"] == 4 and all(fig["return_plan_band"][c][0] <= GD["return_plan"][c][0]
                               and GD["return_plan"][c][1] <= fig["return_plan_band"][c][1] for c in MEM)
       and same(*[n for n, k in C.BESIDE if "cells" in k]))
    # SF40's crossed family and the layered family on the cut, and the two-grains rule with its pin
    xw = C.crossed_ways(A.SINGLES)
    lay = fig["layered"]
    ok("SF40 the crossed family on the cut: %d crossings from core.crossed_ways on the %d singles and the %d ways beside "
       "them, and the layered family: %d ways (%s layered on every way that does not set them, alone and all together); "
       "the call holds on every one" % (len(X["crossed"]), len(A.SINGLES), len(C.BESIDE), lay["ways"], "; ".join(lay["conventions"])),
       len(X["crossed"]) == len(xw) and not fig["crossed"]["moved"] and not lay["moved"]
       and lay["ways"] == len(X["layered"]) > len(xw)
       and set(lay["conventions"]) == {nm for nm, _k in A.PACK_VARIANTS if lay["convention_moves"][nm] > 0}
       and all(lay["convention_moves"][nm] == 0 for nm, _k in A.PACK_VARIANTS if nm not in lay["conventions"]))
    lw_ = lay["widened"]
    ok("SF42 the conventions only the files carry enter the ranges as measured, not as core's bound: refunds netted on the "
       "refund's day move nothing on this cut and are not layered, every other one is (%s); %d ranges widened by the "
       "layered family, each with the way that sets its edge, and every stated range is the layered one" % (
           ", ".join("%s %.6f" % (nm, x) for nm, x in lay["convention_moves"].items()), len(lw_)),
       lay["convention_moves"]["the stores' refunds netted on the day of the refund"] == 0
       and "the stores' refunds netted on the day of the refund" not in lay["conventions"]
       and len(lay["conventions"]) == len(A.PACK_VARIANTS) - 1
       and all(list(fig["figure_band"][fid]) == x["layered"] and any(k in x for k in ("low", "high"))
               and x["layered"][0] <= x["crossed"][0] and x["crossed"][1] <= x["layered"][1] for fid, x in lw_.items()))
    ok("SF40 the two-grains rule: no crossing and no layered way prices rows finer than its first-48-hour cells (a "
       "finer-row fit priced on cells that pool the sessions values its rows split, core.resolves), and every layered way is a way of "
       "the family with the files' conventions put on it",
       not [nm for nm, kw in xw if kw.get("rows") in C.CELL_ROWS
            and not C.resolves(kw.get("cells", "fine"), C.CELL_ROWS[kw["rows"]])]
       and {nm.split("; layered with ")[0] for nm, _f, _b, _l in X["layered"]}
       <= {nm for nm, _k in A.SINGLES} | {nm for nm, _k in C.BESIDE} | {nm for nm, _k in xw})
    sp_f, sp_c = C.pooled_sessions_pin(O, v), C.pooled_sessions_pin(Oc, vc)
    worst = {g_: max(r[4] / max(r[2], 1e-9) for r in rows) for g_, rows in sp_f.items() if rows}
    ok("SF40 pooled_sessions_pin on the files: inside one pooled cell a named install's worth differs by sessions value up "
       "to %s times, and each cell's least and most worth sessions values are the core's on the simulation" % (
           ", ".join("%.2f (%s)" % (x, g_) for g_, x in worst.items())),
       min(worst.values()) > 1.4 and set(sp_f) == set(sp_c)
       and all([r[:2] + r[3:4] for r in sp_f[g_]] == [r[:2] + r[3:4] for r in sp_c[g_]] for g_ in sp_f),
       {g_: (sp_f[g_][:3], sp_c[g_][:3]) for g_ in sp_f})
    ok("SF41 the weeks the value equation is fitted on: all 104, or the %d complete weeks alone, which stands beside the "
       "battery and files the seven bands, every return inside its range" % C.MATURE,
       VW["ways"] == 1 and all(fig["return_plan_band"][c][0] <= VW["return_plan"][c][0]
                               and VW["return_plan"][c][1] <= fig["return_plan_band"][c][1] for c in MEM)
       and same(*[n for n, k in C.BESIDE if "weeks_v" in k]))
    ok("R7 the halves of postbacks dated before the first install week come to %s installs" % fig["steps"]["early_postback_installs"],
       fig["steps"]["early_postback_installs"] == 83.0)
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
           for k in ("Meta and TikTok", "Meta, TikTok and Snapchat", "the four social networks", "the five networks")))
    L_ = fig["ratios"]["lent"]
    ok("R7 the ratios lent by Apple Search Ads and by the Android look-alikes are refused under both readings (%s, %s)" % (
        L_["search_ads"]["stat"], L_["android"]["stat"]),
       all(min(x["stat"], x["stat_one_variance"]) > 5 * x["point"] for x in L_.values()))
    for p in fig["perturbations"]:
        ok("R7 %s times %.3f: the call holds (nearest line %.3f away)" % (p["input"], p["factor"], p["nearest"]), p["call_holds"])
    ok("R7 the perturbations move every fitted input a fifth either way and the delivery share by its widest quarter",
       len(fig["perturbations"]) >= 20 and fig["delivery_share_spread_pct"] > 5)
    # each cap is the measured family's width on this cut (the layered family of SF42 sets R2's, R5's and R4's; the author's ruling of 2026-11-24):
    # a rebuild that widens a range past it fails here
    WCAP = {"R1": 0.17, "R2": 0.32, "R5": 0.25, "R3": 0.08, "R4": 0.11}
    for rid in ("R1", "R2", "R5"):
        w = max((hi - lo) / abs(by[rid]["golden"][k]) for k, (lo, hi) in by[rid]["bands"].items())
        ok("R7 %s: no range wider than %.1f per cent of its figure (cap %.0f)" % (rid, 100 * w, 100 * WCAP[rid]), w < WCAP[rid])
    for rid in ("R3", "R4"):
        lo, hi = by[rid]["band"]
        ok("R7 %s: its range is %.1f per cent of its figure (cap %.0f)" % (rid, 100 * (hi - lo) / by[rid]["golden"], 100 * WCAP[rid]),
           (hi - lo) / by[rid]["golden"] < WCAP[rid])
    ok("R7 R5: the reflex route lands two returns at most inside their ranges",
       sum(in_band("return " + c, reflex["return " + c], fig) for c in MEM) <= 2)
    ok("R7 corelib on the cut pack: level 5, no failure", fig["rubric"]["level"] == 5 and not fig["rubric"]["fails"], fig["rubric"]["fails"])
    ok("R7 the rubric on the cut pack: one step lost %s, fixed alone %s, the reflex route %.1f, the rigorous route %.1f" % (
        fig["rubric"]["one_lost"], fig["rubric"]["fixed_alone"], fig["rubric"]["reflex"], fig["rubric"]["rigorous"]),
       max(fig["rubric"]["one_lost"].values()) <= 50 and fig["rubric"]["reflex"] <= 30 and fig["rubric"]["rigorous"] <= 50)
    # corelib files S1's referee at its 3.0; S2's stands at the core's 2.8 on the simulation (the author's ruling of 2026-11-24, disclosed)
    for s, r in X["refs"].items():
        ge = abs(r["golden"] - r["truth"])
        worst_rival = min(abs(x - r["truth"]) for x in r["rivals"].values())
        rc_ = {"S1": lambda: C.referee_s1(Oc), "S2": lambda: C.referee_s2(Oc, vc),
               "S3": lambda: C.referee_s3(Oc, vc)}[s]()
        sep_c = min(abs(x - rc_["truth"]) for x in rc_["rivals"].values()) / max(abs(rc_["golden"] - rc_["truth"]), 1e-9)
        ok("R7 the %s referee: the estimate %.2f against the record's %.2f, the nearest simpler way %.1f times further "
           "(%.1f on the simulation)" % (s, r["golden"], r["truth"], worst_rival / max(ge, 1e-9), sep_c),
           worst_rival > {"S1": 3.0, "S2": 2.5, "S3": 3.0}[s] * ge and abs(worst_rival / max(ge, 1e-9) - sep_c) <= 0.1 * sep_c, sep_c)
    T0 = C.truth_at_plan()
    ok("R7 the golden call is the world's own on all seven channels", all(C.band(T0[c]["roas"]) == fig["bands"][c] for c in MEM))
    anc = C.anchor(W, Oc, core_gold, T0)                           # the world's own figures need every account's source
    for fid in fids:
        a_ = anc[fid]
        gap_ = gfv[fid] / a_["world"] - 1.0
        ok("R7 the truth anchor: %s %s against the world's own %s, %+.3f inside its tolerance %.3f" % (
            fid, RS.stated(fid, gfv[fid]), RS.stated(fid, a_["world"]), gap_, a_["tolerance"]),
           abs(gap_) <= a_["tolerance"] and abs(a_["gap"] - gap_) < 1e-3)

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
    CV = fig["conventions"]
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    gold_pay = {c: CV["golden"]["pay100"][c] for c in MEM}
    ok("SF6 the payments counted are the monthly plan's: the prompt's words and policy 2.5's two plans; the counting the "
       "golden does is the figure the CSV states on every channel",
       "how many payments on the monthly plan" in prompt
       and both("EUR 9.99 a month and EUR 59.99 a year, each with a seven-day free trial")
       and gold_pay == fig["pay100"] and [fig["policy"]["monthly"], fig["policy"]["annual"]] == [9.99, 59.99])
    one_, twelve_ = ({c: CV[k]["pay100"][c] - gold_pay[c] for c in MEM} for k in ("annual_as_one", "annual_as_twelve"))
    ok("SF6 an annual-plan charge counted as one payment adds %.1f (%s) to %.1f (%s) per 100 installs, as twelve %.0f to %.0f; "
       "neither is a payment on the monthly plan" % (
           min(one_.values()), min(one_, key=one_.get), max(one_.values()), max(one_, key=one_.get), min(twelve_.values()),
           max(twelve_.values())),
       all(x > 0 for x in one_.values()) and all(twelve_[c] > one_[c] for c in MEM))
    # pinned out by the prompt's monthly plan (the check above); annual-as-one lands Pinterest iOS's payments inside its
    # range (60.0), the core's own (the author's ruling of 2026-11-24, disclosed)
    pin_in, pin_out = ("months_365_25", "days_366", "refunds_counted"), ("first_left_out", "web_left_out", "annual_as_one",
                                                                         "annual_as_twelve")
    ok("SF6 AppLovin Android's payments per 100 installs under each convention: %s; inside its range %s on 365.25 and 366 "
       "days and refunds counted (Google Android too), outside it with the first charge or the web checkout left out and "
       "an annual charge as one or twelve" % (
           ", ".join("%s %.1f" % (k, CV[k]["pay100"]["AppLovin Android"]) for k in ("golden",) + pin_in + pin_out),
           fig["pay100_band"]["AppLovin Android"]),
       all(in_band("payments per 100 " + c, CV[k]["exact"][c], fig) for k in pin_in for c in ("AppLovin Android", "Google Android"))
       and all(not in_band("payments per 100 " + c, CV[k]["exact"][c], fig) for k in pin_out
               for c in ("AppLovin Android", "Google Android"))
       and CV["golden"]["pay100"] == gold_pay, {k: CV[k]["pay100"]["AppLovin Android"] for k in CV})
    Q_ = fig["ratios"]
    pa = Q_["payments_adding_up"]
    ok("SF7 the iOS networks' payments come from the second step fitted on the payments: the fitted ratios add the accounts "
       "with no channel up to %.3f of the monthly payments they made, the revenue ratios carried onto them to %.3f, and put "
       "Meta iOS at %.1f against %.1f (its range %s)" % (
           pa["payment_ratios"], pa["revenue_ratios"], Q_["payments_at_revenue_ratios"]["Meta iOS"], fig["pay100"]["Meta iOS"],
           fig["pay100_band"]["Meta iOS"]),
       abs(pa["payment_ratios"] - 1) < 0.01 and pa["revenue_ratios"] > 1.05
       and not in_band("payments per 100 Meta iOS", Q_["payments_at_revenue_ratios"]["Meta iOS"], fig)
       and all(abs(Q_["payments_at_payment_ratios"][c] - fig["pay100"][c]) <= 0.15 for c in RS.IOS))
    rev2 = sum(float(C.plan_spend(c).sum()) * g[c]["roas"] for c in MEM)
    ok("SF8 the plan's revenue is one figure written two ways: each channel's plan spend times its return, summed, is "
       "%.0f against %.0f summed week by week" % (rev2, g["plan"][1]),
       abs(rev2 / g["plan"][1] - 1) < 1e-6
       and both("the 12-month net revenue of the installs the period's spend on the channel buys"))
    gsheet0 = list(wp["Growth channels"].iter_rows(values_only=True))
    ok("SF13 the installs the plan buys: the prompt asks how many installs its 2027 spend will buy, the growth sheet holds "
       "the seven channels' 52 weeks, and the plan's installs are the seven channels' sum (Apple Search Ads apart)",
       "how many installs its 2027 spend will buy" in prompt and [x for x in gsheet0[3] if x in C.ORDER] == MEM
       and all(len(O.plan[c]) == 52 for c in MEM) and "Apple Search Ads" not in MEM
       and abs(g["plan"][0] - sum(float(g[c]["installs_week"]) * 52 for c in MEM)) / g["plan"][0] < 0.02)
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
    cf1 = C.s1_fit(Oc)                                             # the core's fit on the simulation
    cp, cpc = C.continuation_pin(O), C.continuation_pin(Oc)        # on the files, and on the simulation
    ok("SF21 same call for the four fitted ways; the fitted continuation is the core's (%.3f and %.3f); the web checkout's "
       "(%.3f) and the one the app saw (%.3f and %.3f) take in under 70 per cent of each store's renewals beyond the "
       "records, the fitted one within 1 per cent; continuation_pin on the files (the app's rate %s of the excess, the web "
       "checkout's %s, the fit %s; within 0.02 of the core's) and they file AppLovin Android %.3f and TikTok iOS %.3f in cut" % (
           gr["continuation"], ar["continuation"],
           gr["rivals"]["web"]["rate"], gr["rivals"]["seen"]["rate"], ar["rivals"]["seen"]["rate"],
           " and ".join("%.0f" % (100 * cp[nm]["the rate the app saw"][1]) for nm in cp),
           " and ".join("%.0f" % (100 * cp[nm]["the web checkout's"][1]) for nm in cp),
           " and ".join("%.1f" % (100 * cp[nm]["fitted"][1]) for nm in cp),
           fig["shortcuts"]["web_rate"]["return_plan"]["AppLovin Android"], fig["shortcuts"]["seen_rate"]["return_plan"]["TikTok iOS"]),
       same("two-rate continuation", "fit without the last two months", "thirty-day cadence", "one fit across both stores")
       and [gr["continuation"], ar["continuation"]] == [round(float(cf1[pl]["q"]), 3) for pl in (0, 1)]
       and all(abs(cp[nm]["fitted"][1] - 1) < 0.01 and cp[nm][k][1] < 0.70
               for nm in cp for k in ("the rate the app saw", "the web checkout's"))
       and all(abs(cpc[nm][k][j] - cp[nm][k][j]) <= 0.02 for nm in cp for k in cp[nm] for j in (1, 2))
       and all(x["rivals"][k]["takes_in"] < 0.70 * x["renewal_excess_fitted_periods"] for x in (gr, ar) for k in ("web", "seen"))
       and all(abs(x["rivals"]["fitted"]["takes_in"] / x["renewal_excess_fitted_periods"] - 1) < 0.01 for x in (gr, ar))
       and C.band(fig["shortcuts"]["web_rate"]["return_plan"]["AppLovin Android"]) == "cut"
       and C.band(fig["shortcuts"]["seen_rate"]["return_plan"]["TikTok iOS"]) == "cut")
    ok("SF22 same call: the nine other ways of fitting each source's ratio",
       same("the ratios fitted separately for lighter and heavier first-48-hour use", "the ratios fitted unweighted",
            "the ratios fitted by fortnight", "the ratios fitted by four-week period",
            "the ratios fitted with weights from the fitted revenue", "organic installs' ratio taken from Apple Search Ads",
            "market-weeks of fewer than a hundred unattributed accounts left out",
            "the networks' ratios drawn toward their pooled ratio by the fit's own spread"))
    ST = fig["ratios"]["share_tests"]
    kept = sorted(k for k, x in ST.items() if not x["refused"])
    KEPT = sorted(k for k, nms in RS.SHARE_TESTS if frozenset(nms) in GROUPED)
    # the core's own test on the simulation, each grouping the blocks name: both statistics within 2 per cent of the
    # cut's, and the same verdict
    core_st = {k: (C.s2_equal_test(Oc, vc, nms)[0], C.s2_equal_test(Oc, vc, nms, cov="classical")[0])
               for k, nms in RS.SHARE_TESTS}
    close = lambda a_, b_: abs(a_ - b_) <= 0.02 * max(1.0, abs(b_))
    ok("SF23 sources sharing one ratio: the fit's own test under one of its statistics or the other lets through only %s "
       "(%s), which the battery carries, and refuses the rest under both (the nearest %s %s; the five networks %.2f and "
       "%.2f against %.2f); each statistic within 2 per cent of the core's on the simulation" % (
           ", ".join(kept), "; ".join("%.2f and %.2f against %.2f" % (ST[k]["stat"], ST[k]["stat_one_variance"],
                                                                       ST[k]["point"]) for k in kept),
           min((k for k in ST if ST[k]["refused"]), key=lambda k: min(ST[k]["stat"], ST[k]["stat_one_variance"]) / ST[k]["point"]),
           "%.2f and %.2f" % tuple(min(((ST[k]["stat"], ST[k]["stat_one_variance"]) for k in ST if ST[k]["refused"]),
                                       key=lambda t: min(t))),
           ST["the five networks"]["stat"], ST["the five networks"]["stat_one_variance"], ST["the five networks"]["point"]),
       kept == KEPT and len(KEPT) == 4
       and same(*[nm for nm, kw in C.VARIANTS if kw.get("group") in ("pair2", "ps", "pt", "pst")])
       and all(x["refused"] and x["stat"] > x["point"] and x["stat_one_variance"] > x["point"]
               for k, x in ST.items() if k not in KEPT)
       and all(close(ST[k]["stat"], core_st[k][0]) and close(ST[k]["stat_one_variance"], core_st[k][1])
               and ST[k]["refused"] == (min(core_st[k]) > ST[k]["point"]) for k in ST),
       {k: (ST[k]["stat"], ST[k]["stat_one_variance"], [round(x, 2) for x in core_st[k]]) for k in ST})
    au, ca = fig["ratios"]["adding_up"], fig["check_android"]["AppLovin Android"]
    ok("SF24 a worth lent by another source: the accounts with no channel add up to %.2f and %.2f times what they paid against "
       "%.2f fitted; on Android AppLovin's declined installs paid %.2f against %.2f fitted, %.2f and %.2f lent" % (
           au["named"], au["search_ads"], au["fitted"], ca["paid"], ca["fitted"], ca["search_ads"], ca["named"]),
       all(close(au[k], x) for k, x in (("named", C.adding_up(Oc, vc, "bridge")), ("search_ads", C.adding_up(Oc, vc, "ratio")),
                                         ("fitted", C.adding_up(Oc, vc)),
                                         ("borrowed_shift", C.falsification_s2(Oc, vc, C.values(Oc, which="payers"), "r1mix"))))
       and abs(au["fitted"] - 1) < 0.01 and min(au["named"], au["search_ads"], au["borrowed_shift"]) > 1.15
       and all(close(ca[k], x) for k, x in zip(("paid", "fitted", "search_ads", "named"), (
           lambda r: (r["truth"], r["golden"], r["rivals"]["at Apple Search Ads' ratio"],
                      r["rivals"]["priced at its installs that allowed tracking, by first-48-hour value"]))(
               C.referee_s2(Oc, vc, "AppLovin Android"))))
       and all(abs(x["fitted"] - x["paid"]) < 0.5 * min(abs(x["search_ads"] - x["paid"]), abs(x["named"] - x["paid"]))
               for x in fig["check_android"].values()))
    # the proportional split the determinism judge ran on 2026-11-24: it adds up by construction, so the sources'
    # not being alike at the same first-48-hour value is what refuses it
    SPL = fig["ratios"]["split"]
    sub_ = open(os.path.join(TASK, "submission.md")).read()
    ok("SF24 the accounts with no channel shared across the sources in proportion to their unnamed installs (every "
       "source's alike) put Meta iOS at %.1f per 100 and %.3f by market-week, %.1f and %.3f over the 52 weeks at once, a "
       "wrong band; refused by the sources' not being alike, F %.2f and %.2f on %d and %d against %.2f; the blocks state "
       "these" % (SPL["split"]["pay100_meta"], SPL["split"]["return_plan"]["Meta iOS"], SPL["flat"]["pay100_meta"],
                  SPL["flat"]["return_plan"]["Meta iOS"], SPL["test"]["weighted"], SPL["test"]["unweighted"],
                  SPL["test"]["df"][0], SPL["test"]["df"][1], SPL["test"]["point"]),
       all(SPL[k]["bands"]["Meta iOS"] != fig["bands"]["Meta iOS"] for k in ("split", "flat"))
       and min(SPL["test"]["weighted"], SPL["test"]["unweighted"]) > 5 * SPL["test"]["point"]
       and SPL["test"]["df"] == [5, 127] and SPL["test"]["terms"] == 5 and SPL["test"]["rows"] == 156
       and all("%.2f" % SPL["test"][k] in sub_ for k in ("weighted", "unweighted"))
       and "%.1f payments per 100 installs and a return of %.3f" % (
           SPL["split"]["pay100_meta"], SPL["split"]["return_plan"]["Meta iOS"]) in sub_)
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
    days_ = pd.DataFrame({"a": mon.account_id.to_numpy(), "d": A.secs(mon.transaction_at) // 86400}).sort_values(["a", "d"])
    k_ = days_.groupby("a").cumcount().to_numpy()
    off_ = (days_.d - days_.groupby("a").d.transform("min")).to_numpy()
    gaps = days_.groupby("a").d.diff().dropna()
    ok("pin: the billing cadence measured on the events is a twelfth of a year: every monthly charge falls on its first "
       "charge's day plus k twelfths of 365.25 days, rounded (%d charges; mean gap %.4f days on this record's mix of "
       "lengths)" % (len(days_), gaps.mean()),
       bool((off_ == np.round(C.MONTH_DAYS * k_)).all())      # the exact rule; the mean gap is reported, not tested
       and set(gaps.unique()) <= {30, 31}
       and fig["policy"]["cadence_days"] == C.MONTH_DAYS == 30.4375)
    for pl, name in ((0, "Google Play"), (1, "App Store")):
        s_ = fig["stores"][name]
        want = tuple(round(float(cf1[pl][k]), 3) for k in ("c_m", "c_a", "q"))
        ok("pin: %s's fitted shares and continuation are the core's on the simulation (%.3f, %.3f, %.3f against %s)" % (
            name, s_["trial_end_share_monthly"], s_["trial_end_share_annual"], s_["continuation"], want),
           all(abs(a_ - b_) <= 0.0015 for a_, b_ in zip((s_["trial_end_share_monthly"], s_["trial_end_share_annual"],
                                                         s_["continuation"]), want)))
    srcs_c, b_c = C.s2_fit(Oc, vc, cov=True)[:2]
    core_r = {C.SOURCES[i]: round(float(x), 3) for i, x in zip(srcs_c, b_c)}
    ok("pin: each source's fitted ratio on the files is the core's on the simulation within 0.005 (%s)" % (
        ", ".join("%s %.3f" % (c, x["ratio"]) for c, x in rs.items())),
       set(rs) == set(core_r) and all(abs(rs[c]["ratio"] - core_r[c]) <= 0.005 for c in rs),
       {c: (x["ratio"], core_r.get(c)) for c, x in rs.items()})
    dpc = C.delivery_pins(Oc)
    ds = [ch[c]["delivery_share"] for c in C.MEMBERS]
    ok("pin: each channel's spend over its budget across the 104 weeks is the core's (%.3f to %.3f)" % (min(ds), max(ds)),
       all(abs(ch[c]["delivery_share"] - dpc[c]["share"]) <= 0.0015 for c in C.MEMBERS),
       {c: (ch[c]["delivery_share"], round(dpc[c]["share"], 3)) for c in C.MEMBERS})
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
    body = rows_[1:]
    ok("golden CSV: one row per channel with its band, return and payments per 100 installs, and one row for the plan with "
       "its installs and revenue, as figures.json states them",
       rows_[0] == deliver.CSV_COLS and [r_[1] for r_ in body[:7]] == order_ and len(body) == 8
       and all(r_[0] == "channel" and r_[2] == fig["bands"][r_[1]] and float(r_[3]) == fig["return_plan"][r_[1]]
               and float(r_[4]) == fig["pay100"][r_[1]] and r_[5] == r_[6] == "" for r_ in body[:7])
       and body[7][0] == "plan" and int(body[7][5]) == fig["plan_installs"] and int(body[7][6]) == fig["plan_revenue"]
       and body[7][2:5] == ["", "", ""])
    gw = load_workbook(os.path.join(G, deliver.FILES["wb"]))
    ws = gw.worksheets[0]
    pr = 6 + len(order_) + 1
    ok("golden workbook: the first sheet states the bands, each channel's row and the whole plan's installs and revenue",
       str(ws["A1"].value).startswith("2027 media plan: scale %s, hold %s" % tuple(
           deliver._list(fig["by_band"][b]) for b in ("scale", "hold")))
       and [ws.cell(row=6 + i, column=1).value for i in range(7)] == order_
       and all(ws.cell(row=6 + i, column=2).value.lower() == fig["bands"][c]
               and ws.cell(row=6 + i, column=3).value == fig["return_plan"][c]
               and ws.cell(row=6 + i, column=4).value == fig["pay100"][c] for i, c in enumerate(order_))
       and ws.cell(row=pr + 1, column=2).value == fig["plan_installs"] and ws.cell(row=pr + 2, column=2).value == fig["plan_revenue"])
    ok("golden workbook: named sheets, a chart on the first, frozen headers",
       [w_.title for w_ in gw] == ["Bands 2027", "Unrecorded charges", "Unnamed installs", "Budget response", "Ranges", "Routes"]
       and len(ws._charts) >= 1 and all(w_.freeze_panes for w_ in gw))
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
       all(rg.cell(row=5 + i, column=1).value == c
           and [rg.cell(row=5 + i, column=3 + d).value for d in range(3)] == [fig["return_plan"][c]] + list(fig["return_plan_band"][c])
           and [rg.cell(row=5 + i, column=6 + d).value for d in range(3)] == [fig["pay100"][c]] + list(fig["pay100_band"][c])
           for i, c in enumerate(order_))
       and [rg.cell(row=6 + len(order_), column=3 + d).value for d in range(3)] == [fig["plan_installs"]] + list(fig["plan_installs_band"])
       and [rg.cell(row=7 + len(order_), column=3 + d).value for d in range(3)] == [fig["plan_revenue"]] + list(fig["plan_revenue_band"]))
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("blocks: the tags and the four blocks, no stump question before the runs, no em dash, no table",
       [h for h in re.findall(r"^## (.+)$", sub, re.M)] == ["Tags", "Final Recommendation", "Supplementary Questions",
                                                            "Critical Components", "Step-by-Step"]
       and "\u2014" not in sub and "|" not in sub and "How is each model stumped" not in sub)
    rec = sub.split("## Final Recommendation")[1].split("## Supplementary Questions")[0]
    ok("blocks: every return in the recommendation is the CSV's, and it names what it rejects",
       all(("%s %.3f" % (c, fig["return_plan"][c])) in rec for c in MEM) and "This rejects" in rec)
    supp = sub.split("## Supplementary Questions")[1].split("## Critical Components")[0]
    ok("blocks: two numbered entries, one per ask, the first with seven lettered lines",
       re.findall(r"^(\d)\. ", supp, re.M) == ["1", "2"] and len(re.findall(r"^   [a-g]\. ", supp, re.M)) == 7
       and all(("a return of %.3f (range %.3f to %.3f), and %.1f (range %.1f to %.1f)" % (
           fig["return_plan"][c], fig["return_plan_band"][c][0], fig["return_plan_band"][c][1], fig["pay100"][c],
           fig["pay100_band"][c][0], fig["pay100_band"][c][1])) in supp for c in MEM)
       and ("%s installs (range %s to %s)" % tuple("{:,}".format(x) for x in [fig["plan_installs"]] + list(fig["plan_installs_band"]))) in supp
       and ("EUR %s of 12-month net revenue (range %s to %s)" % tuple(
           "{:,}".format(x) for x in [fig["plan_revenue"]] + list(fig["plan_revenue_band"]))) in supp
       and all(n_ in supp for n_ in deliver.FILES.values()))
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
       and CW["true_up"] < 0.75 * CW["charged"] and CW["true_up_one_factor"] < CW["charged"]
       and abs(CW["estimate"] - CW["charged"]) < 0.05 * CW["charged"])
    ok("SF6 and SF7 in the blocks: step 2 pins the monthly plan's payments, step 5 refuses the revenue ratios carried over",
       "A payment on the monthly plan is any charge of the EUR 9.99 plan" in walk
       and ("put Meta iOS at %.1f" % Q_["payments_at_revenue_ratios"]["Meta iOS"]) in walk)
    comp = sub.split("## Critical Components")[1].split("## Step-by-Step")[0]
    lines = [x for x in comp.strip().split("\n") if x.strip()]
    cs = fig["components"]
    ok("blocks: three components, each the answer with its unit and range and no method word",
       len(lines) == 3 and not re.search(r"fitted|regress|ratio|scaled|trued|adjust|correct|once|after|budget|store|postback|"
                                         r"unnamed|record|estimat|model", comp, re.I)
       and all(("**%.1f payments on the monthly plan per 100 installs**" % cs[s]["value"]) in lines[i]
               and ("(range **%.1f to %.1f**)" % tuple(cs[s]["band"])) in lines[i] for i, s in enumerate(("S1", "S2")))
       and ("**{:,} installs**".format(cs["S3"]["value"])) in lines[2]
       and ("(range **{:,} to {:,}**)".format(*cs["S3"]["band"])) in lines[2])
    for s, fid in C.COMPONENTS.items():
        k = RS.FAM_KEY.get(fid[:-len(OPEN[s])]) if fid.endswith(OPEN[s]) else None
        val = fig[k][OPEN[s]] if k else fig[RS.PLAN_KEY[fid]]
        ok("blocks: component %s (%s) is the figure the CSV and the workbook's first sheet state" % (s, fid),
           val == cs[s]["value"] == RS.stated(fid, fig["figure"][fid]))
    ok("prompt: under 1,000 characters, names no file, no method and no role",
       not any(os.path.splitext(n_)[0] in prompt or n_ in prompt for n_ in files) and len(prompt.strip()) < 1000
       and not re.search(r"postback|consent|tracking|budget|auction|store report|round|regress|model|attribut|organic|billing|"
                         r"renew|trial|deliver", prompt, re.I))
    nums = set(re.findall(r"\d+(?:\.\d+)?", prompt))
    ok("prompt: the only figures in it are dates and the twelve months (%s)" % ", ".join(sorted(nums)),
       nums <= {"2027", "2028", "2026", "2025", "8", "2", "12", "100"})
    ok("prompt: it asks for each step's own quantity in the decision's words",
       "how many installs its 2027 spend will buy" in prompt
       and "how many payments on the monthly plan the installs it bought in the year to 2 November 2025 made in their first "
           "12 months, per 100 installs" in prompt
       and "in euros of 12-month net revenue per euro of spend at the plan's weekly spend" in prompt
       and "the 12-month net revenue in euros those installs will bring" in prompt)
    shutil.rmtree(tmp)
    print("\n%d passed, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
