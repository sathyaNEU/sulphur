"""figures.json and effort.json from the cut pack: the golden, the routes, the family, the perturbations and the
bands, each figure the answer blocks state."""
import itertools

import numpy as np

import analysis as AN
import params as P

ROUTES = {"golden": ("golden", "golden", "pooled"),
          "careful": ("prop", "consenters", "average"),
          "quick": ("recorded", "consenters", "average")}
NAMES = {("golden", "golden", "pooled"): "the golden",
         ("prop", "consenters", "average"): "the careful route: the stores' excess spread over every account in "
                                             "proportion, the iOS networks read on their consenting users, 2025's "
                                             "return carried to the plan",
         ("recorded", "consenters", "average"): "the direct route: the billing records as they stand, the consenting "
                                                 "users, 2025's return"}


def call_of(r):
    return sorted("%s: %s" % (c, P.band(r[c]["roas"])) for c in P.ORDER)


def r2(x, nd=2):
    return float(round(x, nd))


def run(target):
    pk = AN.Pack(target)
    cache = {}
    R = {}
    for k in itertools.product(("golden", "prop", "recorded"), ("golden", "consenters"), ("pooled", "average")):
        R[k] = AN.route(pk, *k, cache=cache)
    G = R[ROUTES["golden"]]
    fam = AN.family(pk, cache)
    fits = AN.gap_fit(pk)["all"]
    ren, fst = AN.candidates(pk)
    v_rec = AN.a_values(pk, "recorded"); v_gold = cache[("A", "golden")]
    a = pk.acc
    mat = (a.day >= 0) & (a.day < 7 * P.MATURE_WEEKS)
    # perturbations: each fitted input moved by its defensible spread
    pert = []
    for name, ov in (("silent continuation -0.02", {"q_shift": -0.02}), ("silent continuation +0.02", {"q_shift": 0.02}),
                     ("trial-end charge share -20%", {"c_scale": 0.8}), ("trial-end charge share +20%", {"c_scale": 1.2}),
                     ("non-consenting users' value -10%", {"vn_scale": 0.9}), ("non-consenting users' value +10%", {"vn_scale": 1.1}),
                     ("value-per-install slope on spend -20%", {"v_slope": 0.8}), ("value-per-install slope on spend +20%", {"v_slope": 1.2}),
                     ("installs slope on spend -20%", {"i_slope": 0.8}), ("installs slope on spend +20%", {"i_slope": 1.2})):
        AN.OVERRIDE.clear(); AN.OVERRIDE.update(ov)
        r = AN.route(pk, cache={})
        pert.append({"input": name, "answer": call_of(r), "roas": {c: r2(r[c]["roas"], 3) for c in P.ORDER}})
    AN.OVERRIDE.clear()
    fig = {"bands": {c: P.band(G[c]["roas"]) for c in P.ORDER}, "call": call_of(G),
           "roas_2027": {c: r2(G[c]["roas"]) for c in P.ORDER},
           "roas_2027_3dp": {c: r2(G[c]["roas"], 3) for c in P.ORDER},
           "installs_2025": {c: int(G[c]["installs"]) for c in P.ORDER},
           "v12_2025": {c: r2(G[c]["v12"]) for c in P.ORDER},
           "installs_week_2027": {c: int(round(G[c]["installs_week"])) for c in P.ORDER},
           "vpi_2027": {c: r2(G[c]["vpi"]) for c in P.ORDER},
           "plan_weekly_avg": {c: int(round(pk.plan[c].mean())) for c in P.ORDER},
           "plan_total": {c: int(round(pk.plan[c].sum())) for c in P.ORDER},
           "spend_2025": {c: int(round(np.nansum(cache[("W", "golden")][c]["spend"][:P.MATURE_WEEKS]))) for c in P.ORDER},
           "roas_2025": {c: r2(R[("golden", "golden", "average")][c]["roas"]) for c in P.ORDER},
           "silent_q": r2(fits["q"], 3), "trial_end_share": r2(fits["c_m"], 3),
           "candidates_renewal": int(len(ren)), "candidates_trial": int(len(fst)),
           "unrecorded_share_2025": {c: r2(1 - v_rec.reindex(a.index[mat & (a.channel == c)]).sum() /
                                            v_gold.reindex(a.index[mat & (a.channel == c)]).sum(), 3)
                                     for c in P.ORDER if c not in AN.NETS.values()},
           "consent_share_2025": {c: r2(((a.channel == c) & mat).sum() / G[c]["installs"], 3) for c in AN.NETS.values()},
           "v12_consenters_2025": {c: r2(R[("golden", "consenters", "pooled")][c]["v12"]) for c in AN.NETS.values()},
           "store_excess": r2(sum(pk.apple.developer_proceeds_eur.astype(float)) + sum(pk.google.net_eur.astype(float)), 2),
           "app_recorded_net": r2(pk.bill.net.sum(), 2),
           "routes": {"%s|%s|%s" % k: {c: r2(R[k][c]["roas"], 3) for c in P.ORDER} for k in R},
           "family": {c: {n: r2(x["roas"], 3) for n, x in fam[c]} for c in P.ORDER},
           "perturbations": pert}
    fig["store_excess_share"] = r2(fig["store_excess"] / fig["app_recorded_net"] - 1, 3)
    fig["window_months"] = 12
    fig["window_days"] = 365
    fig["plan_weeks"] = 52
    fig["lines"] = list(P.LINES)
    fig["store_excess_pct"] = r2(100 * fig["store_excess_share"], 1)
    gold_bands = {c: P.band(G[c]["roas"]) for c in P.ORDER}
    wrong = set()
    for k in R:
        if k == ROUTES["golden"]:
            continue
        w = tuple(sorted((c, P.band(R[k][c]["roas"])) for c in P.ORDER if P.band(R[k][c]["roas"]) != gold_bands[c]))
        if w:
            wrong.add(w)
    fig["shortcut_routes"] = len(R) - 1
    fig["distinct_wrong_calls"] = len(wrong)
    fig["consenter_overstate"] = {c: r2(fig["v12_consenters_2025"][c] / fig["v12_2025"][c] - 1, 3) for c in AN.NETS.values()}
    fig["google_plan_rise"] = r2(fig["plan_weekly_avg"]["Google Android"] / (fig["spend_2025"]["Google Android"] / 52) - 1, 3)
    fig["pct"] = {"unrecorded": {c: r2(100 * x, 1) for c, x in fig["unrecorded_share_2025"].items()},
                  "consent": {c: r2(100 * x, 1) for c, x in fig["consent_share_2025"].items()},
                  "consenter_overstate": {c: r2(100 * x, 0) for c, x in fig["consenter_overstate"].items()},
                  "google_plan_rise": r2(100 * fig["google_plan_rise"], 0)}
    return fig, R, fam, pk, cache


def bands_for(G, fam, key, rel, floor):
    out = {}
    for c in P.ORDER:
        g = G[c][key]
        vals = [x[key] for _, x in fam[c] if x.get(key) is not None]
        spread = max([abs(v - g) for v in vals] + [0.0])
        w = max(rel * abs(g), floor, 1.5 * spread)
        out[c] = [r2(g - w, 3), r2(g + w, 3)]
    return out


def capped(G, fam, key, base):
    """a band per channel: the base share or one and a half times the family's spread, capped so that R2 and R3 at
    their edges together never carry the channel's return across its nearest line"""
    out, half = {}, {}
    for c in P.ORDER:
        g = G[c][key]
        sp = max([abs(x[key] - g) / g for _, x in fam[c] if x.get(key)] + [0.0])
        cap = min(abs(G[c]["roas"] - l) for l in P.LINES) / G[c]["roas"] / 2.2
        h = min(cap, max(base, 1.5 * sp))
        half[c] = (h, sp, cap)
        out[c] = [g * (1 - h), g * (1 + h)]
    return out, half


def effort(fig, R, fam):
    G = R[ROUTES["golden"]]
    q, ca = R[ROUTES["quick"]], R[ROUTES["careful"]]
    b_inst = {c: [int(G[c]["installs"] * 0.98), int(np.ceil(G[c]["installs"] * 1.02))] for c in P.ORDER}
    b_v12, h2 = capped(G, fam, "v12", 0.03)
    b_v12 = {c: [r2(lo, 3), r2(hi, 3)] for c, (lo, hi) in b_v12.items()}
    b_iw, h3 = capped(G, fam, "installs_week", 0.06)
    b_iw = {c: [int(np.ceil(lo)), int(np.floor(hi))] for c, (lo, hi) in b_iw.items()}
    fig["band_halfwidths"] = {"R2": {c: r2(h2[c][0], 4) for c in P.ORDER}, "R3": {c: r2(h3[c][0], 4) for c in P.ORDER}}
    b_roas = bands_for(G, fam, "roas", 0.03, 0.02)
    quick_inst = {c: int(G[c]["installs"]) if c not in AN.NETS.values() else int(round(G[c]["installs"] * fig["consent_share_2025"][c]))
                  for c in P.ORDER}
    plan_iw_avg = {c: ca[c]["installs"] / fig["spend_2025"][c] * fig["plan_weekly_avg"][c] for c in P.ORDER}
    res = [
        {"id": "R1", "name": "installs each channel bought from 4 November 2024 to 2 November 2025", "graded_as": "Ask 1",
         "figure": "installs_2025", "depends": [], "independent": "the installs themselves",
         "golden": fig["installs_2025"], "bands": b_inst, "partly_share": 0.8,
         "passes": {"quick": quick_inst, "careful": fig["installs_2025"], "thorough": fig["installs_2025"]}},
        {"id": "R2", "name": "12-month net revenue per install of those installs, by channel", "graded_as": "Component 1",
         "figure": "v12_2025", "depends": [], "independent": "the 2025 installs' charges",
         "golden": fig["v12_2025"], "bands": b_v12, "partly_share": 0.7,
         "passes": {"quick": {c: r2(q[c]["v12"]) for c in P.ORDER},
                    "careful": {c: r2(ca[c]["v12"]) for c in P.ORDER}, "thorough": fig["v12_2025"]},
         "precedent": ["N21", "L44", "N27"]},
        {"id": "R3", "name": "installs a week at each channel's 2027 weekly spend", "graded_as": "Ask 2",
         "figure": "installs_week_2027", "depends": [], "independent": "the weekly spend and installs",
         "golden": fig["installs_week_2027"], "bands": b_iw, "partly_share": 0.7,
         "passes": {"quick": {c: r2(plan_iw_avg[c], 1) for c in P.ORDER}, "careful": {c: r2(plan_iw_avg[c], 1) for c in P.ORDER},
                    "thorough": fig["installs_week_2027"]},
         "precedent": ["N01", "L17"]},
        {"id": "R4", "name": "each channel's 2027 return per euro at the plan's weekly spend", "graded_as": "Component 2",
         "figure": "roas_2027", "depends": ["R2", "R3"], "independent": "",
         "golden": fig["roas_2027"], "bands": b_roas, "partly_share": 0.7,
         "passes": {"quick": {c: r2(q[c]["roas"]) for c in P.ORDER}, "careful": {c: r2(ca[c]["roas"]) for c in P.ORDER},
                    "thorough": fig["roas_2027"]},
         "precedent": ["N21", "N27", "N01"]},
        {"id": "R5", "name": "each channel's band", "graded_as": "Recommendation", "figure": "call",
         "depends": ["R4"], "independent": "", "golden": fig["call"],
         "passes": {"quick": call_of(q), "careful": call_of(ca), "thorough": fig["call"]},
         "precedent": ["N21", "N27", "N01"]},
    ]
    gold_call = call_of(G)
    def ans(k):
        return call_of(R[k])
    F = {"golden_answer": gold_call,
         "reflex_route": {"answer": ans(ROUTES["careful"])},
         "judgments": [
             {"id": "J1", "name": "a store charge reaches the billing records only when the subscriber next opens the app, "
                              "so the stores' excess belongs to the subscriptions last seen still set to renew",
              "kind": "stump", "precedent": ["N21", "L44"],
              "dropped": {"answer": ans(("prop", "golden", "pooled")), "results_moved": ["R2", "R4", "R5"]},
              "alone": {"answer": ans(("golden", "consenters", "average")), "results_rescued": []}},
             {"id": "J2", "name": "iOS users who allow tracking are the more engaged, so the iOS networks are read on "
                              "every install's conversion value, not on the users the attribution export holds",
              "kind": "stump", "precedent": ["N27", "L03"],
              "dropped": {"answer": ans(("golden", "consenters", "pooled")), "results_moved": ["R2", "R4", "R5"]},
              "alone": {"answer": ans(("prop", "golden", "average")), "results_rescued": []}},
             {"id": "J3", "name": "a channel's installs come dearer and weaker as its weekly spend rises, so 2025's "
                              "return per euro does not carry to a plan that spends more",
              "kind": "stump", "precedent": ["N01", "L17"],
              "dropped": {"answer": ans(("golden", "golden", "average")), "results_moved": ["R3", "R4", "R5"]},
              "alone": {"answer": ans(("prop", "consenters", "pooled")), "results_rescued": ["R3"]}},
             {"id": "J4", "name": "the iOS networks' installs counted from the install postbacks, not from the "
                              "attribution export", "kind": "reflex", "precedent": ["R81"]},
             {"id": "J5", "name": "re-sent export rows, reinstalls, staff and test accounts and sandbox charges left "
                              "out", "kind": "reflex", "precedent": ["R80"]},
             {"id": "J6", "name": "net revenue at the policy's VAT and 15 per cent commission", "kind": "reflex",
              "precedent": []}]}
    routes = [{"name": NAMES.get(k, "A %s, C %s, B %s" % k), "answer": call_of(R[k]), "golden": k == ROUTES["golden"]}
              for k in R]
    fam_rows = [{"name": "the golden", "answer": gold_call}]
    for n in sorted({n for c in P.ORDER for n, _ in fam[c]} - {"A=golden"}):
        fam_rows.append({"name": n, "answer": sorted("%s: %s" % (c, P.band(dict(fam[c])[n]["roas"])) for c in P.ORDER)})
    forcing = {"kind": "set", "golden_answer": gold_call, "golden_family": fam_rows,
               "shortcuts": [{"name": NAMES.get(k, "A %s, C %s, B %s" % k), "answer": call_of(R[k])}
                             for k in R if k != ROUTES["golden"]],
               "perturbations": [{"input": p["input"], "answer": p["answer"]} for p in fig["perturbations"]]}
    hints = [{"sentence": "a store charge reaches the billing records only when the subscriber next opens the app",
              "rescues": []},
             {"sentence": "iOS users who allow tracking are the more engaged ones", "rescues": []},
             {"sentence": "a channel's installs come dearer and weaker as its weekly spend rises", "rescues": ["R3"]}]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
