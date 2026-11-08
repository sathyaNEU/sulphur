"""task2 checks, run on the cut pack: the Layer 1 build ties to the quality reports, the record carries the
structure the design needs (a steady share, the release gap's climb, the release steps within clinicians, the
compulsory starters' level alike at every go-live), the golden family agrees on every graded figure, the ladder's
routes land off the call, and every fork row is asserted."""
import math
import os
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

import golden as GD
import verify as V
import world as W

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), str(detail)))


def pc(x):
    return int(math.floor(100 * x + 0.5))


def q_of(t):
    y, m = divmod(t, 12)
    return (W.START[0] + y, m // 3 + 1)


def audited_shares(P, sel=None):
    acc = defaultdict(list)
    for a in P.audits:
        if sel is None or sel(a):
            acc[q_of(a["t"])].append(a["wer"] > W.LINE)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def graded(G):
    """every figure the rubric grades, at its asked rounding"""
    return dict(ceiling=G["ceiling"], first_past=G["first_past"], bands=G["bands"],
                p90_q4=pc(G["q"][(2027, 4)]["p90"]))


def starters_pooled(P, per, typ, rates, steps):
    return np.concatenate([rates["V"], rates["M"]])


def starters_recent(P, per, typ, rates, steps):
    rec = {p for p, d in per.items() if W.mi(2025, 1) <= d["first"] <= GD.DEC}
    return np.array([a["wer"] * math.exp(-steps[a["release"]]) for a in P.audits if a["person"] in rec])


def route_flat(P, G):
    s = audited_shares(P)
    v = float(np.mean([s[(2026, q)] for q in (1, 2, 3, 4)]))
    return [v] * 4


def route_drift(P, G):
    s = audited_shares(P)
    drift = (s[(2024, 2)] - s[(2023, 1)]) / 5.0
    base = (s[(2026, 3)] + s[(2026, 4)]) / 2
    return [base + drift * (k + 1.5) for k in range(4)]


def route_hospitals(P, G, step=0.0):
    hs = {h: audited_shares(P, sel=lambda a, h=h: a["site"] == h).get((2026, 4), 0.0) for h in P.comp}
    out = []
    for (y, q) in GD.Q27:
        num = den = 0.0
        for t in GD.months(y, q):
            for h in P.comp:
                v = sum(G["out"][(t, h)].values())
                c = P.comp[h]
                add = step if (c > GD.DEC and t >= c + 1) else 0.0
                num += v * (hs[h] + add)
                den += v
        out.append(num / den)
    return out


def golive_step(P):
    steps = []
    for h, c in P.comp.items():
        if not (W.mi(2023, 4) <= c <= W.mi(2026, 3)):
            continue
        sh = audited_shares(P, sel=lambda a, h=h: a["site"] == h)
        before = q_of(c - 3)
        after = [q_of(c + 3), q_of(c + 6)]
        steps.append(np.mean([sh[k] for k in after]) - sh[before])
    return float(np.mean(steps))


def ceiling_of(shares):
    m = 100 * max(shares)
    return next((c for c in GD.CEILINGS if m <= c), None)


def run(target, gen_dir, w=None):
    C = {}
    P = V.load(target)
    G = GD.golden(P)
    C.update(P=P, G=G)
    dec = [(G["typ"][p], d["vol"].get(GD.DEC, 0)) for p, d in G["per"].items() if d["last"] == GD.DEC]
    C["record_wV_2026"] = sum(v for k, v in dec if k == "V") / sum(v for _, v in dec)
    C["record_vol_q4_2026"] = sum(d["vol"].get(t, 0) for d in G["per"].values() for t in range(GD.DEC - 2, GD.DEC + 1))
    # ---- Layer 1: the quality reports tie to the cleaned audits, quarter by quarter
    wb = load_workbook(os.path.join(target, "quality_reports_2023_2026.xlsx"), read_only=True)
    rep = {}
    for i, r in enumerate(wb["Group"].iter_rows(values_only=True)):
        if i:
            y, q = int(r[0][:4]), int(r[0][-1])
            rep[(y, q)] = (int(r[1]), int(r[2]))
    s = audited_shares(P)
    n = defaultdict(int)
    for a in P.audits:
        n[q_of(a["t"])] += 1
    check("Layer 1: the cleaned audits tie to every quarterly report (counts and heavy dictations)",
          all(rep[k][0] == n[k] and abs(rep[k][1] / rep[k][0] - s[k]) < 1e-9 for k in rep), str(len(rep)))
    Pf = V.load(target, first_pass=True)
    check("Layer 1: first-pass scores move no quarterly share by more than half a point",
          max(abs(audited_shares(Pf)[k] - s[k]) for k in s) < 0.005)
    # ---- the record
    rec = [s[(y, q)] for y in (2023, 2024, 2025, 2026) for q in (1, 2, 3, 4)]
    C["record"] = rec
    late = [s[(y, q)] for (y, q) in sorted(s) if (y, q) >= (2024, 3)]
    check("the record: no quarter since the middle of 2024 passes 10 per cent, and they span under 2.5 points",
          max(late) <= 0.10 and max(late) - min(late) < 0.025, str([round(100 * x, 1) for x in late]))
    g0 = (s[(2023, 1)] + s[(2023, 2)]) / 2
    g1 = (s[(2023, 4)] + s[(2024, 1)]) / 2
    C["gap"] = (g0, g1)
    check("the record: the 2023 to 2024 release gap climbs half a point or more and stays under 10 per cent",
          g1 - g0 >= 0.005 and max(s[(2023, 3)], s[(2023, 4)], s[(2024, 1)]) < 0.10, "%.2f to %.2f" % (100 * g0, 100 * g1))
    st = G["steps"]
    order = ["3.4", "4.0", "5.0", "5.2", "6.0"]
    check("the release steps within clinicians fall release by release", all(st[a] > st[b] for a, b in zip(order, order[1:])),
          str({k: round(v, 3) for k, v in st.items()}))
    check("compulsory starters carry at least six times the voluntary clinicians' heavy share under 6.0",
          G["share"]["M"] >= 6 * G["share"]["V"], "%.2f %.2f" % (100 * G["share"]["M"], 100 * G["share"]["V"]))
    # the compulsory starters sit at one level whatever the go-live
    lv = []
    for h, c in P.comp.items():
        if c > GD.DEC:
            continue
        x = [math.log(a["wer"]) - st[a["release"]] for a in P.audits
             if a["e"] > 0 and G["typ"].get(a["person"]) == "M" and G["per"][a["person"]]["site0"] == h]
        if len(x) > 300:
            lv.append(float(np.mean(x)))
    check("every go-live's compulsory starters at one level (mean log error under 6.0 within 0.15)",
          max(lv) - min(lv) < 0.15, str([round(x, 3) for x in lv]))
    lv = [math.exp(x) for x in lv]
    C["golive_levels"] = lv           # each go-live's compulsory starters' typical error rate under 6.0
    # no learning curve: a compulsory starter's release-adjusted error in the first three months matches later months
    early, later = [], []
    for a in P.audits:
        if a["e"] > 0 and G["typ"].get(a["person"]) == "M":
            k = a["t"] - G["per"][a["person"]]["first"]
            (early if k < 3 else later).append(math.log(a["wer"]) - st[a["release"]])
    C["learning"] = (float(np.mean(early)), float(np.mean(later)), len(early))
    check("SF19 no learning curve: compulsory starters' first three months within 0.05 (log) of their later months",
          abs(np.mean(early) - np.mean(later)) < 0.05, "%.3f against %.3f (%d early audits)" % C["learning"])
    # ---- the golden family: every graded figure the same
    fam = {"golden": G,
           "SF11 the 6.0 audits alone (no release steps)": GD.golden(P, rates_how="frozen only"),
           "SF9 incumbents held (no turnover)": GD.golden(P, incumbents_flat=True),
           "SF13 the compulsory boundary a month earlier": GD.golden(P, boundary=-1),
           "SF3 first-pass scores": GD.golden(Pf),
           "SF14 movers unlinked": GD.golden(V.load(target, link_movers=False)),
           "SF4 quarters by audit date": GD.golden(V.load(target, by_audit_date=True)),
           "SF17 incumbents' volume from their last six months": GD.golden(P, inc_months=6),
           "SF17 a starter's volume from 2025 and 2026": GD.golden(P, vm_from=W.mi(2025, 1))}
    gg = graded(G)
    for k, F in fam.items():
        if k == "golden":
            continue
        check("%s: every graded figure as the golden's" % k, graded(F) == gg,
              "%s %s" % ([round(100 * f["share"], 2) for f in F["q"].values()], graded(F)))
    C["family"] = fam
    # ruled out by a filed date or the record
    nr = GD.golden(P, use_ramp=False)
    check("SF10 starters at full volume from the go-live: the same ceiling (the first quarter past 10 and its band move)",
          nr["ceiling"] == G["ceiling"],
          str(graded(nr)))
    C["no_ramp"] = nr
    # ---- the ladder: every route that skips the step lands off the call
    flat = route_flat(P, G)
    drift = route_drift(P, G)
    hosp = route_hospitals(P, G)
    step = golive_step(P)
    hstep = route_hospitals(P, G, step=step)
    avg = GD.golden(P, starter_rates=starters_pooled)
    recent = GD.golden(P, starter_rates=starters_recent)
    lad = {"R0 the 2026 share carried forward": flat,
           "R1 each hospital's 2026 share at 2027's hospital mix": hosp,
           "R1 starters at the average clinician's level": [f["share"] for f in avg["q"].values()],
           "R2 the release gap's drift added": drift,
           "R2 the go-live step at the small hospitals, in points": hstep,
           "R2 starters at the 2025 and 2026 starters' level": [f["share"] for f in recent["q"].values()]}
    C["ladder"] = {k: (v, ceiling_of(v)) for k, v in lad.items()}
    C["golive_step"] = step
    for k, v in lad.items():
        check("ladder: %s lands off the 14 per cent ceiling" % k, ceiling_of(v) != G["ceiling"],
              "%s -> %s" % ([round(100 * x, 1) for x in v], ceiling_of(v)))
    check("Gate F: no cheap route lands the call", sum(ceiling_of(v) == G["ceiling"] for v in lad.values()) == 0)
    # ---- margins
    qs = [f["share"] for f in G["q"].values()]
    allq = [[f["share"] for f in F["q"].values()] for F in fam.values()]
    check("the voluntary clinicians' share of fourth-quarter dictation under two fifths in every member",
          all(F["q"][(2027, 4)]["wV"] < 0.40 for F in fam.values()),
          str([round(F["q"][(2027, 4)]["wV"], 3) for F in fam.values()]))
    check("the call: every family member's highest quarter between 12.25 and 13.75", all(0.1225 <= max(x) <= 0.1375 for x in allq),
          str([round(100 * max(x), 2) for x in allq]))
    check("the first quarters past 10 and 12: the second and the fourth, in every member, with 0.2 points to spare",
          all(x[0] <= 0.098 and x[1] >= 0.102 and x[2] <= 0.118 and x[3] >= 0.122 for x in allq),
          str([[round(100 * v, 2) for v in x] for x in allq]))
    check("the fourth quarter's 90th percentile at least 0.15 from its rounding line in every member",
          all(abs(100 * F["q"][(2027, 4)]["p90"] - math.floor(100 * F["q"][(2027, 4)]["p90"]) - 0.5) >= 0.15
              for F in fam.values()), str([round(100 * F["q"][(2027, 4)]["p90"], 2) for F in fam.values()]))

    # ---- fork rows closed by a filed sentence (the reading is the schedule's, the procedure's or the notice's)
    for sf in ("SF1 the audited share: the audit is a random sample within hospital and month (QA-07 1)",
               "SF2 word error rate: QA-07 3", "SF5 above 15 per cent: strictly above (Schedule 4.1)",
               "SF6 the 2027 population: every dictation under the service (Schedule 4.2)",
               "SF7 the release: 6.0 through 2027 (SN-2026-14)", "SF8 passing a ceiling: above it (Schedule 4.3)",
               "SF12 the percentile of dictations: the prompt's 'dictations'",
               "SF16 the ceiling: the lowest offered at or above every quarter",
               "SF18 the nine-in-ten rate: the 90th percentile rounded to the nearest whole per cent (the prompt's words)"):
        check(sf, True)
    return C
