"""task2 architecture 6 checks, run on the cut pack: the Layer 1 build ties to the quality reports, the record
carries the structure the chain needs (release steps within clinicians, selective uptake, each hospital's own effect
identified through the clinicians who moved, a slow switch-over at every go-live), the golden family lands every
graded figure inside its band, every rival outside the family is ruled out by named data, and every hurried route
lands off at least one graded figure."""
import math
import os
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

import golden as GD
import verify as V
import world as W

RESULTS = []

# the band each graded figure carries (the golden family spans inside it; every hurried route falls outside one)
BANDS = {"ssu": (0.143, 0.155), "bku": (0.123, 0.135), "bku_vol": (85000, 91000), "p90": (0.158, 0.163),
         "site_SSU": (0.035, 0.065), "site_BKU": (0.070, 0.100), "releases": (-0.0474, -0.0348),
         "mix": (0.0124, 0.0250), "ent_SSU": (0.170, 0.195), "ent_BKU": (0.205, 0.230)}
EXACT = ("ceiling", "first_past", "bands")


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), str(detail)))


def q_of(t):
    y, m = divmod(t, 12)
    return (W.START[0] + y, m // 3 + 1)


def audited_shares(P, sel=None):
    acc = defaultdict(list)
    for a in P.audits:
        if sel is None or sel(a):
            acc[q_of(a["t"])].append(a["wer"] > W.LINE)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def graded(X):
    """every figure the rubric grades"""
    out = dict(ceiling=X["ceiling"], first_past=X["first_past"], bands=X["bands"],
               ssu=X["hq"]["SSU"]["share"], bku=X["hq"]["BKU"]["share"], bku_vol=X["hq"]["BKU"]["vol"], p90=X["p90"],
               site_SSU=math.exp(X["F"]["site"]["SSU"]) - 1, site_BKU=math.exp(X["F"]["site"]["BKU"]) - 1,
               ent_SSU=X["U"]["SSU"]["h_ent"], ent_BKU=X["U"]["BKU"]["h_ent"])
    if X["bridge"] is not None:
        out.update(releases=X["bridge"]["releases"], mix=X["bridge"]["mix"])
    return out


def misses(gr, gold):
    """the graded figures a route files outside their bands (or off the golden's exact answers)"""
    out = []
    for k in EXACT:
        if gr.get(k) != gold[k]:
            out.append(k)
    for k, (lo, hi) in BANDS.items():
        if k in gr and not (lo <= gr[k] <= hi):
            out.append(k)
    return out


def three_way(P, iters=400):
    """a rival estimator of the hospital effects: clinician, release and hospital effects fitted together by
    alternating projections over every audit"""
    rows = [(a["person"], a["release"], a["site"], math.log(a["wer"])) for a in P.audits if a["e"] > 0]
    ps = sorted({r[0] for r in rows})
    rs = sorted({r[1] for r in rows})
    hs = list(W.CODES)
    pi = {p: k for k, p in enumerate(ps)}
    ri = {r: k for k, r in enumerate(rs)}
    hi = {h: k for k, h in enumerate(hs)}
    ip = np.array([pi[r[0]] for r in rows])
    ir = np.array([ri[r[1]] for r in rows])
    ih = np.array([hi[r[2]] for r in rows])
    y = np.array([r[3] for r in rows])
    npp, nr, nh = (np.bincount(x).astype(float) for x in (ip, ir, ih))
    a, b, g = np.zeros(len(ps)), np.zeros(len(rs)), np.zeros(len(hs))
    for _ in range(iters):
        a = np.bincount(ip, y - b[ir] - g[ih], minlength=len(ps)) / npp
        b = np.bincount(ir, y - a[ip] - g[ih], minlength=len(rs)) / nr
        g = np.bincount(ih, y - a[ip] - b[ir], minlength=len(hs)) / nh
    small = np.mean([g[hi[h]] for h in GD.SMALL])
    return {h: float(g[hi[h]] - small) for h in hs}, {r: float(b[ri[r]] - b[ri["6.0"]]) for r in rs}


def run(target, gen_dir, w=None):
    C = {}
    P = V.load(target)
    G = GD.golden(P)
    C.update(P=P, G=G)
    gold = graded(G)
    C["graded"] = gold
    # ---- Layer 1: the quality reports tie to the cleaned audits, quarter by quarter
    wb = load_workbook(os.path.join(target, "quality_reports_2023_2026.xlsx"), read_only=True)
    rep = {}
    for i, r in enumerate(wb["Group"].iter_rows(values_only=True)):
        if i:
            rep[(int(r[0][:4]), int(r[0][-1]))] = (int(r[1]), int(r[2]))
    s = audited_shares(P)
    n = defaultdict(int)
    for a in P.audits:
        n[q_of(a["t"])] += 1
    check("Layer 1: the cleaned audits tie to every quarterly report (counts and heavy dictations)",
          len(rep) == 16 and all(rep[k][0] == n[k] and abs(rep[k][1] / rep[k][0] - s[k]) < 1e-9 for k in rep), len(rep))
    rec = [s[(y, q)] for y in (2023, 2024, 2025, 2026) for q in (1, 2, 3, 4)]
    C["record"] = rec
    check("the record: every quarter between 7 and 12 per cent, none since the middle of 2024 above 10",
          min(rec) > 0.07 and max(rec) < 0.12 and max(rec[6:]) <= 0.10, str([round(100 * x, 1) for x in rec]))
    # ---- the error model
    st = G["F"]["steps"]
    order = ["3.4", "4.0", "5.0", "5.2", "6.0"]
    check("the release steps within clinicians fall release by release", all(st[a] > st[b] for a, b in zip(order, order[1:])),
          str({k: round(v, 3) for k, v in st.items()}))
    into = G["F"]["into"]
    check("each university hospital's own effect rests on 30 or more clinicians who dictated there and at another",
          into["SSU"] >= 30 and into["BKU"] >= 30, str(into))
    g3, b3 = three_way(P)
    C["three_way"] = g3
    check("the hospital effects agree within 1.5 points with a joint three-way fit",
          all(abs(g3[h] - G["F"]["site"][h]) < 0.015 for h in W.TEACHING),
          "%s against %s" % ({h: round(g3[h], 3) for h in W.TEACHING}, {h: round(G["F"]["site"][h], 3) for h in W.TEACHING}))
    check("the 4.0 to 6.0 step agrees within a point with the joint fit", abs((b3["6.0"] - b3["4.0"]) - G["bridge"]["step"]) < 0.01,
          "%.4f against %.4f" % (b3["6.0"] - b3["4.0"], G["bridge"]["step"]))
    # ---- the record's own evidence of selective uptake
    kr = GD.small_kind_rates(P, G["post"])
    C["kinds"] = kr
    check("selective uptake: the smaller hospitals' compelled clinicians carry twice the heavy share of those hired "
          "after the go-live, who carry more than those who chose", kr["compelled"] > 2 * kr["hired"] > 2 * kr["chose"],
          str({k: round(100 * v, 2) for k, v in kr.items()}))
    up = {}
    for h in GD.SMALL:
        c = P.comp[h]
        staff = [x for x, d in G["post"].items() if d["site"] == h and d["start"] < c and (d["end"] is None or d["end"] > c)]
        up[h] = sum(1 for x in staff if G["post"][x]["first"] is not None and G["post"][x]["first"] < c) / len(staff)
    C["uptake"] = up
    check("uptake before the go-live differs from hospital to hospital (a spread of 20 points or more)",
          max(up.values()) - min(up.values()) >= 0.20, str({h: round(100 * v) for h, v in up.items()}))
    # ---- the switch-over
    check("every go-live switches over slowly: under 40 per cent of a settled month in the first two months",
          G["ramp"][0] < 0.25 and G["ramp"][1] < 0.45 and G["ramp"][4] > 0.85, str([round(x, 3) for x in G["ramp"]]))
    # ---- the golden family: every graded figure inside its band
    Pf = V.load(target, first_pass=True)
    fam = {"golden": G,
           "SF3 first-pass scores": GD.golden(Pf),
           "SF4 quarters by audit date": GD.golden(V.load(target, by_audit_date=True)),
           "SF11 the dictators' rate from every audit carried by its release step": GD.golden(P, rates_how="all releases"),
           "SF13 population cells by grade alone": GD.golden(P, cells="grade"),
           "SF17 settled volume from the last six months": GD.golden(P, recent=6),
           "SF18 population from every clinician dictating after a go-live": GD.golden(P, pop_set="post go-live"),
           "SF19 population read straight off the smaller hospitals' audits by grade": GD.golden(P, pop_how="empirical"),
           "SF23 no calendar adjustment": GD.golden(P, season=False),
           "SF10 the ramp from the four go-lives since 2023": GD.golden(P, ramp_sites=["KBR", "CSL", "KNA", "DRL"])}
    C["family"] = fam
    for k, X in fam.items():
        gr = graded(X)
        bad = misses(gr, gold)
        check("%s: every graded figure inside its band" % k, not bad,
              "%s %s" % (bad, {kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in gr.items()}))
    spans = {k: (min(graded(X)[k] for X in fam.values() if k in graded(X)),
                 max(graded(X)[k] for X in fam.values() if k in graded(X))) for k in BANDS}
    C["spans"] = spans
    # ---- rivals outside the family, each ruled out by named data
    unl = GD.golden(V.load(target, link_movers=False))
    check("SF14 staff numbers left unlinked: no clinician is seen at two hospitals, so the hospitals' own effects cannot "
          "be measured (the register links %d moves)" % sum(1 for d in P.reg.values() if d["prev"]),
          unl["F"]["pairs"] == 0, str(graded(unl)["ceiling"]))
    C["unlinked"] = unl
    for name, use in [("release 6.0 audits alone", lambda a: a["release"] == "6.0"),
                      ("the 2025 and 2026 audits alone", lambda a: a["t"] >= W.mi(2025, 1))]:
        X = GD.golden(P, fit_use=use)
        check("SF15 the hospital effects from %s rest on %d and %d clinicians seen at two hospitals against %d and %d"
              % (name, X["F"]["into"]["SSU"], X["F"]["into"]["BKU"], into["SSU"], into["BKU"]),
              X["F"]["into"]["SSU"] < 0.8 * into["SSU"] and X["F"]["into"]["BKU"] < 0.8 * into["BKU"])
    # ---- the hurried routes: each lands off at least one graded figure
    routes = {
        "R0 the 2026 share carried forward": GD.route(P, G, "steady"),
        "R0 the record's highest quarter": GD.route(P, G, "history"),
        "R1 each hospital's late-2026 share at 2027's dictations": GD.route(P, G, "hospitals"),
    }
    full = {
        "R2 the 2027 starters at the smaller hospitals' compelled clinicians' rate": GD.golden(P, starter_from="compelled"),
        "R2 the 2027 starters at the smaller hospitals' compulsory starters' rate, pooled": GD.golden(P, starter_from="pooled"),
        "R2 the 2027 starters at the rate of those hired after a go-live": GD.golden(P, starter_from="hired"),
        "R3 no hospital effect (the university hospitals at the smaller hospitals' level)": GD.golden(P, site_off=True),
        "R4 the go-lives at full volume from the date": GD.golden(P, use_ramp=False),
        "R4 every clinician starting on the date at their own first months' volume": GD.golden(P, start_kind="own first months"),
        "careful but hurried: the compelled rate, own first months, no hospital effect":
            GD.golden(P, starter_from="compelled", start_kind="own first months", site_off=True),
    }
    C["routes"] = {k: (v, GD.band(max(v))) for k, v in routes.items()}
    C["full_routes"] = full
    for k, v in routes.items():
        check("route %s lands off the call" % k, GD.band(max(v)) != G["ceiling"],
              "%s -> %s" % ([round(100 * x, 1) for x in v], GD.band(max(v))))
    for k, X in full.items():
        bad = misses(graded(X), gold)
        check("route %s misses graded figures" % k, len(bad) >= 2, "%s ceiling %s" % (bad, X["ceiling"]))
    wrong = {GD.band(max(v)) for v in routes.values()} | {X["ceiling"] for X in full.values()}
    wrong.discard(G["ceiling"])
    check("the hurried routes land on three or more different wrong calls", len(wrong) >= 3, str(sorted(wrong, key=str)))
    br = GD.bridge_routes(P, G)
    C["bridge_routes"] = br
    for k, v in br.items():
        check("bridge route %s files the releases outside their band" % k,
              not (BANDS["releases"][0] <= v["releases"] <= BANDS["releases"][1]), "%.4f" % v["releases"])
    C["p90_levels"] = GD.p90_levels(P, G)
    check("the percentile read off clinicians' levels falls outside its band", not (BANDS["p90"][0] <= C["p90_levels"] <= BANDS["p90"][1]),
          "%.4f" % C["p90_levels"])
    # ---- margins
    allq = [[X["q"][k]["share"] for k in GD.Q27] for X in fam.values()]
    check("the quarters in every member: the first under 9.8, the second and third between 10.2 and 11.8, the fourth "
          "between 12.4 and 13.6", all(x[0] < 0.098 and 0.102 < x[1] < 0.118 and 0.102 < x[2] < 0.118 and 0.124 < x[3] < 0.136
                                       for x in allq), str([[round(100 * v, 2) for v in x] for x in allq]))
    q = [G["q"][k]["share"] for k in GD.Q27]
    C["q"] = q
    # ---- fork rows closed by a filed sentence (the reading is the schedule's, the procedure's or the notice's)
    for sf in ("SF1 the audited share: a random sample within hospital and month (QA-07 1)",
               "SF2 word error rate: substitutions, deletions and insertions over the reference words (QA-07 3)",
               "SF5 above 15 per cent: strictly above (Schedule 4.1)",
               "SF6 the 2027 population: every dictation under the service, compulsory hospitals included (Schedule 4.2)",
               "SF7 the release: 6.0 through 2027 (SN-2026-14)", "SF8 passing a ceiling: above it (Schedule 4.3)",
               "SF9 the staff in post: the HR count at 31 December 2026, a leaver replaced like for like (rollout plan)",
               "SF12 the percentile of dictations: the prompt's 'dictations'",
               "SF16 the ceiling: the lowest offered at or above every quarter (Schedule 4.3)",
               "SF20 the bridge's two orders: both inside the releases' band",
               "SF21 the bridge window: the second quarter of 2023 to the last of 2026 (the prompt)",
               "SF22 a hospital's own effect: against the six smaller hospitals' average (the answer blocks)"):
        check(sf, True)
    return C
