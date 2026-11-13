"""Every owed figure computed from the cut pack (methods.py on target/), the rivals that set each band, the named
shortcuts and the three passes, written as figures.json and effort.json."""
import collections
import os

import pandas as pd

import methods as M
import params as P
import pack as PK

ROUTES = {
    "the golden": M.GOLD,
    "the careful route: the live roll-up's positions, today's profile export": M.opts(channels=("live",),
                                                                                     member="today"),
    "the licence renewals merged, today's profile export": M.opts(member="today"),
    "the live roll-up's positions, the profiles each charge lists": M.opts(channels=("live",)),
    "the 2026 remuneration basis carried (52 per cent of net revenue)": M.opts(cost="share26"),
    "streamed seconds read as hours, today's profile export": M.opts(channels=("live",), basis="seconds",
                                                                     member="today"),
}
CAREFUL = ROUTES["the careful route: the live roll-up's positions, today's profile export"]
RIVALS = {
    "re-sent warehouse rows summed": M.opts(dedup=False),
    "a trial month's profiles from the profile export": M.opts(trial_fallback="today"),
    "survival by plan alone": M.opts(r6_surv="plan"),
    "the twelve months' mean hours, no season": M.opts(r6_hours="flat"),
    "each account's own twelve months, seasoned": M.opts(r6_hours="own"),
}
NAMES = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}


def quick(pk, target):
    """Ten minutes: the obvious files, the first account that fits."""
    q = {}
    plan = pk["plan"]
    open_ = plan[(plan["period_start"] <= "2026-10-31") & (plan["period_end"].isna() | (plan["period_end"] >= "2026-10-31"))]
    q["R1"] = {pl: int((open_["plan_code"] == pl).sum()) for pl in P.PLANS}
    so = M.opts(channels=("live",), basis="seconds", member="today", dedup=False)
    q["R2"] = M.r2(pk, so)
    r4, _, _ = M.r4_r5(pk, so)
    # revenue at the prices paid, VAT included, no store fee
    c = M.cohort(pk)
    pm = M.paying_months(pk)
    pm = pm.merge(c[["account_id", "m0", "plan"]], on="account_id")
    pm = pm[(pm["m"] >= pm["m0"]) & (pm["m"] < pm["m0"] + P.HORIZON)]
    for pl in P.PLANS:
        n = int((c["plan"] == pl).sum())
        r4[pl] = dict(r4[pl])
        r4[pl]["net revenue"] = float(pm.loc[pm["plan"] == pl, "amount_eur"].sum() / n)
    q["R4"] = r4
    _, r5, _ = M.r4_r5(pk, M.opts(cost="share26", channels=("live",), member="today"))
    q["R5"] = r5
    stm = pd.read_csv(os.path.join(target, PK.FILES["stm"]))
    q["R6"] = float(stm[stm["statement_month"] >= "2025-11"]["amount_eur"].sum())
    q["R7"] = max(r5, key=r5.get)
    return q


def table(d, keys=None):
    return {NAMES[k]: d[k] for k in (keys or P.PLANS)}


def run(target):
    pk = M.load(target)
    out = {nm: M.all_results(pk, o) for nm, o in ROUTES.items()}
    riv = {nm: M.all_results(pk, o) for nm, o in RIVALS.items()}
    G = out["the golden"]
    C = out["the careful route: the live roll-up's positions, today's profile export"]
    Q = quick(pk, target)
    # bands: the golden and every rival, widened by half the printed unit
    def band(key, u, sub=None):
        res = {}
        for pl in P.PLANS:
            vals = [G[key][pl] if sub is None else G[key][pl][sub]]
            vals += [r[key][pl] if sub is None else r[key][pl][sub] for r in riv.values()]
            w = max(u / 2, 0.01 * abs(vals[0]))
            res[NAMES[pl]] = [round(min(vals) - w, 2), round(max(vals) + w, 2)]
        return res
    r6_vals = [G["R6"]] + [r["R6"] for r in riv.values()]
    fig = {
        "lead_plan": NAMES[G["R7"]], "lead_plan_code": G["R7"],
        "careful_lead": NAMES[C["R7"]],
        "paying_oct": table(G["R1"]), "paying_oct_total": sum(G["R1"].values()),
        "counted_per_month": {NAMES[k]: round(v, 2) for k, v in G["R2"].items()},
        "spring24": {"%s %s" % (NAMES[k], a): round(v[a] * (100 if a == "share paying" else 1),
                                                     1 if a == "share paying" else 2)
                     for k, v in G["R4"].items() for a in ("share paying", "paying months", "net revenue")},
        "spring24_trial_starts": {NAMES[k]: v["trial starts"] for k, v in G["R4"].items()},
        "contribution": {NAMES[k]: round(v, 1) for k, v in G["R5"].items()},
        "contribution_detail": {NAMES[k]: {"counted hours": round(v["counted hours"], 1),
                                           "remuneration (EUR)": round(v["remuneration"], 2), "fee (EUR)": v["fee"]}
                                for k, v in G["detail"].items()},
        "fee": table(P.FEE27), "rate": P.RATE27,
        "remuneration_2027_base": int(round(G["R6"], -2)),
        "remuneration_2027_band": [int(round(min(r6_vals) * 0.99, -2)), int(round(max(r6_vals) * 1.01, -2))],
        "routes": {nm: {"lead": NAMES[r["R7"]], "contribution": {NAMES[k]: round(v, 1) for k, v in r["R5"].items()},
                        "counted_per_month": {NAMES[k]: round(v, 2) for k, v in r["R2"].items()},
                        "remuneration_2027": int(round(r["R6"], -2))} for nm, r in out.items()},
        "bands": {"counted_per_month": band("R2", 0.01), "contribution": band("R5", 0.1)},
        "horizon_months": P.HORIZON,
        "clauses": [2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8],
    }
    srt = sorted(G["R5"].values(), reverse=True)
    fig["lead_margin_eur"] = round(srt[0] - srt[1], 1)
    fig["runner_up"] = NAMES[sorted(G["R5"], key=G["R5"].get)[-2]]
    E = effort(G, C, Q, riv, out, fig)
    return fig, E, {"pk": pk, "out": out, "riv": riv}


def _cells(d, u):
    return {NAMES[k]: v for k, v in d.items()}


def effort(G, C, Q, riv, out, fig):
    b2, b5 = fig["bands"]["counted_per_month"], fig["bands"]["contribution"]
    def t(d, nd=2):
        return {NAMES[k]: round(v, nd) for k, v in d.items()}
    def r4t(d):
        return {"%s %s" % (NAMES[k], a): round(v[a] * (100 if a == "share paying" else 1),
                                               1 if a == "share paying" else 2)
                for k, v in d.items() for a in ("share paying", "paying months", "net revenue")}
    r4b = {}
    for k in P.PLANS:
        g = G["R4"][k]
        r4b["%s share paying" % NAMES[k]] = [100 * g["share paying"] - 0.05, 100 * g["share paying"] + 0.05]
        r4b["%s paying months" % NAMES[k]] = [g["paying months"] - 0.005, g["paying months"] + 0.005]
        r4b["%s net revenue" % NAMES[k]] = [g["net revenue"] - 0.5, g["net revenue"] + 0.5]
    results = [
        {"id": "R1", "name": "paying subscriptions by plan at 31 October 2026", "graded_as": "Ask 2",
         "figure": "paying_oct", "depends": [], "independent": "the October base",
         "golden": table(G["R1"]), "bands": {NAMES[k]: [v - 0.5, v + 0.5] for k, v in G["R1"].items()},
         "passes": {"quick": table(Q["R1"]), "careful": table(C["R1"]), "thorough": table(G["R1"])}},
        {"id": "R2", "name": "counted hours per paying subscription-month by plan, Nov 2025 to Oct 2026",
         "graded_as": "Component 2", "figure": "counted_per_month", "depends": [], "independent": "the twelve months' listening",
         "golden": t(G["R2"]), "bands": b2, "precedent": ["L03", "L28", "N09"],
         "passes": {"quick": t(Q["R2"]), "careful": t(C["R2"]), "thorough": t(G["R2"])}},
        {"id": "R4", "name": "spring 2024 trial starts over 24 months by plan", "graded_as": "Ask 3", "figure": "spring24",
         "depends": [], "independent": "the spring 2024 trial starts' billing", "golden": r4t(G["R4"]), "bands": r4b,
         "partly_share": 0.6,
         "passes": {"quick": r4t(Q["R4"]), "careful": r4t(C["R4"]), "thorough": r4t(G["R4"])}},
        {"id": "R5", "name": "24-month contribution per spring 2027 trial start by plan", "graded_as": "Component 1",
         "figure": "contribution", "depends": ["R4"], "independent": "", "golden": t(G["R5"], 1), "bands": b5,
         "precedent": ["L03", "N09", "L28"],
         "passes": {"quick": t(Q["R5"], 1), "careful": t(C["R5"], 1), "thorough": t(G["R5"], 1)}},
        {"id": "R6", "name": "the 2027 remuneration on the October 2026 base", "graded_as": "Ask 4",
         "figure": "remuneration_2027_base", "depends": [], "independent": "the base's own records",
         "golden": fig["remuneration_2027_base"], "band": fig["remuneration_2027_band"],
         "partly": [fig["remuneration_2027_band"][0] * 0.95, fig["remuneration_2027_band"][1] * 1.05],
         "precedent": ["L03", "N13"],
         "passes": {"quick": round(Q["R6"], -2), "careful": round(C["R6"], -2), "thorough": fig["remuneration_2027_base"]}},
        {"id": "R7", "name": "the plan the spring 2027 campaign leads with", "graded_as": "Recommendation",
         "figure": "lead_plan", "depends": ["R5"], "independent": "", "golden": NAMES[G["R7"]],
         "precedent": ["L28", "L29"],
         "passes": {"quick": NAMES[Q["R7"]], "careful": NAMES[C["R7"]], "thorough": NAMES[G["R7"]]}},
    ]
    A = out["the licence renewals merged, today's profile export"]
    B = out["the live roll-up's positions, the profiles each charge lists"]
    hints = [{"sentence": "the licence server's renewals carry the positions of titles played from downloads",
              "rescues": [r for r, ok in (("R2", _inband(A["R2"], b2)), ("R5", _inband(A["R5"], b5)),
                                          ("R6", fig["remuneration_2027_band"][0] <= A["R6"] <= fig["remuneration_2027_band"][1]),
                                          ("R7", A["R7"] == G["R7"])) if ok]},
             {"sentence": "profiles move between accounts, so attribute each one to the account whose charge lists it",
              "rescues": [r for r, ok in (("R2", _inband(B["R2"], b2)), ("R5", _inband(B["R5"], b5)),
                                          ("R6", fig["remuneration_2027_band"][0] <= B["R6"] <= fig["remuneration_2027_band"][1]),
                                          ("R7", B["R7"] == G["R7"])) if ok]}]
    routes = [{"name": nm, "answer": [NAMES[r["R7"]]], "golden": nm == "the golden"} for nm, r in out.items()]
    fam = [{"name": "the golden", "answer": [NAMES[G["R7"]]]}] + \
          [{"name": nm, "answer": [NAMES[r["R7"]]]} for nm, r in riv.items()]
    pert = []
    for pl in P.PLANS:
        for s in (-0.10, 0.10):
            v = {k: G["R5"][k] - (s * P.FEE27[k] if k == pl else 0.0) for k in P.PLANS}
            pert.append({"input": "%s's fee %+d%%" % (NAMES[pl], round(100 * s)), "answer": [NAMES[max(v, key=v.get)]]})
    for pl in P.PLANS:
        for s in (-0.05, 0.05):
            v = {k: G["R5"][k] - (s * G["detail"][k]["remuneration"] if k == pl else 0.0) for k in P.PLANS}
            pert.append({"input": "%s's counted hours %+d%%" % (NAMES[pl], round(100 * s)),
                         "answer": [NAMES[max(v, key=v.get)]]})
    shortcuts = [{"name": nm, "answer": [NAMES[r["R7"]]]} for nm, r in out.items() if nm != "the golden"]
    forcing = {"kind": "set", "golden_answer": [NAMES[G["R7"]]], "golden_family": fam, "perturbations": pert,
               "shortcuts": shortcuts}
    return {"results": results, "hints": hints, "routes": routes, "forcing": forcing,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}


def _inband(d, b):
    return all(b[NAMES[k]][0] <= v <= b[NAMES[k]][1] for k, v in d.items())
