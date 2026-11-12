"""task22 forcing and the one-fact test: every route run end to end on the same frames. The golden family (the
defensible rivals) must file the golden four; every shortcut a different four; each fitted input moved by its
defensible spread must leave the four standing. Each hint is the careful pass with that one correction made."""
import copy
import json

import numpy as np

import analysis as A
import results as RS


def sweep_of(F, **kw):
    n, _ = A.ntl_route(F, **kw)
    return A.top4(n), n


def perturbed(F, what):
    G = dict(F)
    G["_bid"] = F.get("_bid") or id(F)
    G["_pert"] = what
    if what == "conductor R at 25 C":
        c = F["conductors"].copy()
        c["R50_ohm_per_mile"] = c["R25_ohm_per_mile"]
        G["conductors"] = c
    elif what == "conductor R plus 5 per cent":
        c = F["conductors"].copy()
        c["R50_ohm_per_mile"] = c["R50_ohm_per_mile"] * 1.05
        G["conductors"] = c
    elif what == "transformer losses plus 10 per cent":
        x = F["xfmr_losses"].copy()
        x["NoLoad_W"] = x["NoLoad_W"] * 1.10
        x["LoadLoss_W"] = x["LoadLoss_W"] * 1.10
        G["xfmr_losses"] = x
    elif what == "transformer losses less 10 per cent":
        x = F["xfmr_losses"].copy()
        x["NoLoad_W"] = x["NoLoad_W"] * 0.90
        x["LoadLoss_W"] = x["LoadLoss_W"] * 0.90
        G["xfmr_losses"] = x
    elif what == "burning hours less 5 per cent":
        b = F["burn_hours"].copy()
        b["BurningHours"] = b["BurningHours"] * 0.95
        G["burn_hours"] = b
    elif what == "substation transformer losses plus 20 per cent":
        s = F["subxf"].copy()
        s["NoLoad_kW"] = s["NoLoad_kW"] * 1.2
        s["LoadLoss_kW"] = s["LoadLoss_kW"] * 1.2
        G["subxf"] = s
    else:
        raise ValueError(what)
    return G


def run(F, golden_R=None):
    gold = golden_R or RS.golden(F)
    gset = gold["sweep"]
    out = {"routes": [], "hints": [], "forcing": {}}
    routes = [
        ("the golden: breaker gaps from the delivery point balance, the switching log replayed, technical losses at "
         "each node's monthly metered load", dict(), True),
        ("technical losses at the 2019 study's percentage of each feeder's energy", dict(tech="study_pct"), False),
        ("technical losses on the 2019 study's equivalent resistance with 2026's current", dict(tech="study_req"), False),
        ("technical losses with load placed by transformer rating (the study's load-flow convention)", dict(tech="kva"),
         False),
        ("today's GIS feeder for every month", dict(topology="today"), False),
        ("breaker gaps carried at the feeder's own average for the hour", dict(fill="mean"), False),
        ("breaker gaps interpolated across", dict(fill="interp"), False),
        ("the careful but hurried pass: today's GIS, gaps at the feeder's average, the 2019 percentages",
         dict(topology="today", fill="mean", tech="study_pct"), False),
        ("today's GIS with the study's resistance and interpolated gaps", dict(topology="today", fill="interp",
                                                                               tech="study_req"), False),
    ]
    for name, kw, is_g in routes:
        s, n = sweep_of(F, **kw)
        out["routes"].append(dict(name=name, answer=s, golden=is_g, ntl={f: round(v / 1000.0) for f, v in n.items()}))
    # each correction alone on the careful pass
    alone = [("only the switching log replayed", dict(topology="history", fill="mean", tech="study_pct")),
             ("only the breaker gaps from the balance", dict(topology="today", fill="balance", tech="study_pct")),
             ("only technical losses at the loads' positions", dict(topology="today", fill="mean", tech="golden")),
             ("the log and the gaps, the 2019 percentages kept", dict(topology="history", fill="balance",
                                                                      tech="study_pct")),
             ("the log and the positions, gaps at the average", dict(topology="history", fill="mean", tech="golden")),
             ("the gaps and the positions, today's GIS", dict(topology="today", fill="balance", tech="golden"))]
    for name, kw in alone:
        s, n = sweep_of(F, **kw)
        out["routes"].append(dict(name=name, answer=s, golden=False, ntl={f: round(v / 1000.0) for f, v in n.items()}))
    # the one-fact test: each hint is the careful pass with that one correction
    TG = RS.tables(gold)
    B = RS.bands(TG)
    hints = [
        ("Each substation's delivery point meter covers every hour the feeder breakers' telemetry missed.",
         dict(topology="today", fill="balance", tech="study_pct", r8="nameplate_study"), False),
        ("The GIS shows today's network; the switching log moved customers between feeders.",
         dict(topology="history", fill="mean", tech="study_pct", r8="nameplate_study"), False),
        ("Technical losses follow the square of each segment's current where the loads sit now, not the 2019 "
         "study's percentages.", dict(topology="today", fill="mean", tech="golden", r8="nameplate_study"), False),
        ("New connections draw what comparable connected members draw, not the load they applied for.",
         dict(topology="today", fill="mean", tech="study_pct", r8="nameplate_study"), True),
    ]
    careful = RS.compute(F, **RS.CAREFUL)
    TC = RS.pass_values(careful, careful=True)
    base_right = {rid for rid, _, _, key, *_ in RS.RESULTS if right(TC[key], TG[key], B.get(key))}
    for sent, kw, df_fix in hints:
        R = RS.compute(F, **kw)
        T = RS.pass_values(R, careful=not df_fix)
        if df_fix:
            T["R7_new_peaks"] = TG["R7_new_peaks"]
        now = {rid for rid, _, _, key, *_ in RS.RESULTS if right(T[key], TG[key], B.get(key))}
        out["hints"].append(dict(sentence=sent, rescues=sorted(now - base_right)))
    # forcing: the golden family, the shortcuts and the perturbations, all on the four
    fam = [("the golden", dict()),
           ("load placed by each node's twelve-month metered energy", dict(tech="kwh_year"))]
    gf = []
    for name, kw in fam:
        s, _ = sweep_of(F, **kw)
        gf.append(dict(name=name, answer=s))
    # calendarised evenly over each read period's days rather than by the substation's daily energy
    st_days = A.build_state(F, topology="history", fill="balance", calendar_by="days")
    st_days["_bf"] = A.by_feeder_daily(st_days)
    t_days = A.technical(F, st_days)
    b_days = A.balance(F, st_days, t_days, A.WIN26)
    gf.append(dict(name="each read period spread evenly over its days",
                   answer=A.top4({f: b_days[f]["ntl"] for f in A.FEEDERS})))
    shorts = [dict(name=r["name"], answer=r["answer"]) for r in out["routes"] if not r["golden"]]
    perts = []
    for what in ("conductor R at 25 C", "conductor R plus 5 per cent", "transformer losses plus 10 per cent",
                 "transformer losses less 10 per cent", "burning hours less 5 per cent",
                 "substation transformer losses plus 20 per cent"):
        G2 = perturbed(F, what)
        s, _ = sweep_of(G2)
        perts.append(dict(input=what, answer=s))
    out["forcing"] = dict(kind="set", golden_family=gf, shortcuts=shorts, perturbations=perts)
    return out


def right(v, g, band):
    if isinstance(g, dict):
        for k, gv in g.items():
            b = (band or {}).get(k)
            pv = v.get(k) if isinstance(v, dict) else None
            if pv is None:
                return False
            if b is not None:
                if not (b[0] <= pv <= b[1]):
                    return False
            elif pv != gv:
                return False
        return True
    if isinstance(g, list):
        return set(v) == set(g)
    if isinstance(g, float):
        return abs(v - g) <= 0.03
    return v == g
