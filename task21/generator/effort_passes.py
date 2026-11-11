"""The three passes, each run end to end on the cut pack, and the files the gates read: generator/figures.json (every
figure the answer blocks state) and generator/effort.json (each result's golden, band, and the value each pass
files, with the hints, the routes and the forcing block).

    python3 effort_passes.py [target]
"""
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import methods as M  # noqa: E402

SITES = ("Kitecompare", "Covertide", "Brightquote", "Pricelark")


def r1_cells(D, weighted=True, drop_tests=True):
    f = D["feeds"]
    f = f[f.date >= dt.date(2026, 1, 1)]
    out = {}
    for seg in M.SEGS:
        g = f[f.seg == seg]
        q = g.w.sum() if weighted else len(g)
        s = int((g.w == 1).sum())
        out["%s quotes" % seg] = int(q)
        out["%s sales" % seg] = s
        out["%s conversion" % seg] = round(s / q, 4)
    return out


def textbook(base):
    return lambda L: base * (1 + M.INFL) / (1 + L)


def run(target):
    GD = G.compute(target)
    D, S = GD["D"], GD["S"]
    # ---- golden figures
    fig = {}
    fig["u25_lr_at_proposal"] = round(GD["u25_lr_at_proposal"] * 100, 1)
    fig["u25_rise"] = GD["u25_rise"]
    fig["mid_rise"] = GD["mid_rise"]
    fig["u25_lr_at_rise"] = round(GD["u25_lr_at_rise"] * 100, 1)
    fig["mid_lr_at_rise"] = round(GD["mid_lr_at_rise"] * 100, 1)
    fig["lr_at_rise_band"] = [74.0, 75.0]
    fig["u25_policies_at_rise"] = int(round(GD["u25_vol_at_rise"][0], -1))
    fig["mid_policies_at_rise"] = int(round(GD["mid_vol_at_rise"][0], -1))
    fig["u25_premium_at_rise_m"] = round(GD["u25_vol_at_rise"][1] / 1e6, 1)
    fig["mid_premium_at_rise_m"] = round(GD["mid_vol_at_rise"][1] / 1e6, 1)
    fig["u25_policies_at_proposal"] = int(round(GD["vol_u25_proposal"][0], -1))
    fig["o65_policies_at_cut"] = int(round(GD["vol_o65_proposal"][0], -1))
    fig["o65_policies_at_hold"] = int(round(GD["vol_o65_hold"][0], -1))
    fig["cut_nb_m"] = round(GD["cut"]["nb"] / 1e6, 2)
    fig["cut_ren_m"] = round(GD["cut"]["ren"] / 1e6, 2)
    fig["cut_net_m"] = round(GD["cut"]["net"] / 1e6, 2)
    fig["cut_ren_loss_m"] = -fig["cut_ren_m"]
    for k in ("nb0", "nb1", "rp0", "rp1"):
        fig["cut_%s_m" % k] = round(GD["cut"][k] / 1e6, 2)
    fig["cut_net_loss_m"] = -fig["cut_net_m"]
    for g in ("u25", "mid"):
        fig[g + "_profit_hold_m"] = round(GD[g + "_profit"][0] / 1e6, 2)
        fig[g + "_profit_rise_m"] = round(GD[g + "_profit"][1] / 1e6, 2)
    fig["mid_range_lo"] = round(GD["mid_range"][0] * 100, 1)
    fig["mid_range_hi"] = round(GD["mid_range"][1] * 100, 1)
    for g in M.SEGS:
        fig[g + "_base_lr"] = round(S[g]["base"] * 100, 1)
    fig["u25_slope"] = round(S["u25"]["info"]["slope"], 2)
    fig["u25_ae_deepest"] = round(float(S["u25"]["info"]["y"][0]), 2)
    fig["u25_ae_shallowest"] = round(float(S["u25"]["info"]["y"][-1]), 2)
    cells = r1_cells(D)
    fig["r1"] = cells
    fig["r1_rows"] = {g: [int(GD["r1"][g][0]), int(GD["r1"][g][1]), round(GD["r1"][g][2] * 100, 2)] for g in M.SEGS}
    fig["s_jan"] = round(float(D["s_cost"][0]), 2)
    fig["s_jun"] = round(float(D["s_cost"][5]), 2)
    for k in (1, 2, 3, 4):
        fig["u25_conv_%d" % k] = round(S["u25"]["conv"][k] * 100, 2)
    fig["mid_slope"] = round(S["mid"]["info"]["slope"], 2)
    fig["constants"] = {"proposal_u25": int(round(G.PROPOSAL_U25 * 100)), "cut": int(round(G.PROPOSAL_O65 * 100)),
                        "target": int(round(M.TARGET * 100)), "market": int(round(M.MARKET * 100)),
                        "extract_weight": 50, "cap": int(M.CAP), "servicing": int(M.SERVICING), "draws": 1500,
                        "inflation": M.INFL * 100, "cut_size": -int(round(G.PROPOSAL_O65 * 100)),
                        "band_range_pts": 1.5, "band_policies_pct": 8, "band_profit_m": 0.4,
                        "sections": {"PLN-2027-03 claims cap": 2.1, "CMP-RP-04 renewal cap": 3.1,
                                     "PLN-2027-03 ranges": 5.2}}
    tot = D["feeds"][D["feeds"].date >= dt.date(2026, 1, 1)]
    for g in M.SEGS:
        t = tot[tot.seg == g]
        fig[g + "_2026_quotes"] = int(t.w.sum())
        fig[g + "_2026_sales"] = int((t.w == 1).sum())
        fig[g + "_2026_conversion"] = round((t.w == 1).sum() / t.w.sum() * 100, 2)
    # ---- the hurried constructions
    sc = {g: G.shortcuts(D, S, g) for g in ("u25", "mid")}
    fam = {g: G.family(D, S, g) for g in ("u25", "mid")}
    fam_rise = {g: {k: M.smallest_change(f) for k, f in fam[g].items()} for g in fam}
    sr_all = {g: {k: M.smallest_change(f) for k, f in sc[g].items()} for g in sc}
    fam_lr15 = [f(G.PROPOSAL_U25) for f in fam["u25"].values()]
    lat12 = {g: sc[g]["loss-ratio method, latest twelve months"] for g in sc}
    todate = {g: sc[g]["loss-ratio method, 2026 to date"] for g in sc}
    careful_u25_rise = M.smallest_change(lat12["u25"])
    careful_mid_rise = M.smallest_change(lat12["mid"])
    quick_u25_rise = M.smallest_change(todate["u25"])
    quick_mid_rise = M.smallest_change(todate["mid"])

    def vol(g, L):
        return M.volumes(D["feeds"], g, S[g]["conv"], L)

    def seg_table(g, rise):
        s, p = vol(g, rise / 100.0)
        return {"rise": rise, "policies": int(round(s, -1)), "premium_m": round(p / 1e6, 1)}

    # careful's range: the same draws around its own base and rise
    S_care = dict(S["mid"])
    S_care["lr"] = lat12["mid"]
    care_range = G.lr_range(D, S_care, careful_mid_rise / 100.0)
    # the over-65 cut, priced on new business alone
    nb_only = GD["cut"]["nb"]
    fig["cut_nb_only_m"] = round(nb_only / 1e6, 2)
    fig["careful_u25_rise"] = careful_u25_rise
    fig["careful_mid_rise"] = careful_mid_rise
    fig["careful_u25_lr_at_proposal"] = round(lat12["u25"](G.PROPOSAL_U25) * 100, 1)
    fig["todate_u25_rise"] = quick_u25_rise
    fig["todate_mid_rise"] = quick_mid_rise
    fig["pooled_mid_rise"] = M.smallest_change(sc["mid"]["loss-ratio method, 2025 and 2026 pooled"])
    fig["pooled_u25_rise"] = M.smallest_change(sc["u25"]["loss-ratio method, 2025 and 2026 pooled"])
    fig["completed_mid_rise"] = M.smallest_change(sc["mid"]["loss-ratio method, current book completed"])
    fig["careful_cl_u25_rise"] = M.smallest_change(sc["u25"]["loss-ratio method, latest twelve months, triangles' development"])
    fig["careful_cl_mid_rise"] = M.smallest_change(sc["mid"]["loss-ratio method, latest twelve months, triangles' development"])
    fig["completed_u25_rise"] = M.smallest_change(sc["u25"]["loss-ratio method, current book completed"])
    fig["u25_family_lo"], fig["u25_family_hi"] = min(fam_rise["u25"].values()), max(fam_rise["u25"].values())
    fig["mid_family_lo"], fig["mid_family_hi"] = min(fam_rise["mid"].values()), max(fam_rise["mid"].values())
    # a band's ends are bounds: the floor rounds down and the ceiling up, so no member sits outside its print
    fig["u25_lr15_lo"] = float(np.floor(min(fam_lr15) * 1000) / 10)
    fig["u25_lr15_hi"] = float(np.ceil(max(fam_lr15) * 1000) / 10)
    replay = lambda b: M.smallest_change(lambda L: M.lr_2027(b, S["mid"]["cur"], S["mid"]["curve"], S["mid"]["conv"], L))
    wins = []
    for name, b in (("Priced by HPM v7 (since 1 February 2026), a full year of seasons", S["mid"]["base"]),
                    ("Priced by HPM v7, to 31 October as it stands",
                     G.base_variant(D, "mid", "current", "extract", False)),
                    ("Latest twelve months earned, every policy", G.latest12(D, "mid")),
                    ("2025 and 2026 written, pooled, a full year of seasons", G.base_variant(D, "mid", "pooled"))):
        wins.append([name, round(float(b), 4), replay(b)])
    fig["mid_windows"] = wins
    fig["mid_replay_latest12_rise"] = wins[2][2]
    fig["mid_replay_pooled_rise"] = wins[3][2]

    # ---- effort.json
    golden_calls = ["under 25: rise of %d per cent" % GD["u25_rise"], "25 to 64: rise of %d per cent" % GD["mid_rise"],
                    "65 and over: hold, no cut"]
    u25_band = [fig["u25_family_lo"], fig["u25_family_hi"]]
    mid_band = [fig["mid_family_lo"], fig["mid_family_hi"]]
    res = []
    q_cells = r1_cells(D, weighted=False)
    res.append({"id": "R1", "name": "2026 quotes, sales and conversion by segment", "graded_as": "Ask 6",
                "figure": "r1", "depends": [], "independent": "the four feeds",
                "golden": cells, "bands": {k: ([v - 2, v + 2] if k.endswith("sales") else
                                               [v * 0.995, v * 1.005] if k.endswith("quotes") else [v - 0.001, v + 0.001])
                                           for k, v in cells.items()}, "partly_share": 0.5,
                "passes": {"quick": q_cells, "careful": cells, "thorough": cells}})
    pu = int(round(G.PROPOSAL_U25 * 100))
    pr = {"u25 at +%d" % pu: fig["u25_policies_at_proposal"], "o65 at -3": fig["o65_policies_at_cut"]}
    held = {"u25 at +%d" % pu: int(round(fig["u25_2026_sales"] * 12 / 10.0, -1)),
            "o65 at -3": int(round(fig["o65_2026_sales"] * 12 / 10.0, -1))}
    fig["r2_table"] = pr
    res.append({"id": "R2", "name": "2027 policies the team's two proposals would write", "graded_as": "Ask 4",
                "figure": "r2_table", "depends": [], "independent": "the feeds and the planning paper",
                "golden": pr, "bands": {k: [v * 0.92, v * 1.08] for k, v in pr.items()},
                "passes": {"quick": held, "careful": pr, "thorough": pr}})
    res.append({"id": "R3", "name": "the under-25 2027 loss ratio at the team's rise", "graded_as": "Component 1",
                "figure": "u25_lr_at_proposal", "depends": ["R1"], "independent": "",
                "golden": fig["u25_lr_at_proposal"], "band": [fig["u25_lr15_lo"], fig["u25_lr15_hi"]],
                "partly": [fig["u25_lr15_lo"] - 1.5, fig["u25_lr15_hi"] + 1.5],
                "precedent": ["L29", "L22", "L23"],
                "passes": {"quick": round(todate["u25"](G.PROPOSAL_U25) * 100, 1),
                           "careful": fig["careful_u25_lr_at_proposal"], "thorough": fig["u25_lr_at_proposal"]}})
    gold4 = seg_table("u25", GD["u25_rise"])
    fig["r4_table"] = gold4
    for g, band in (("u25", u25_band), ("mid", mid_band)):
        (n_hi, p_hi), (n_lo, p_lo) = vol(g, band[1] / 100.0), vol(g, band[0] / 100.0)
        fig[g + "_policies_band"] = [int(np.floor(n_hi / 10) * 10), int(np.ceil(n_lo / 10) * 10)]
        fig[g + "_premium_band_m"] = [float(np.floor(p_hi / 1e5) / 10), float(np.ceil(p_lo / 1e5) / 10)]
    res.append({"id": "R4", "name": "the smallest under-25 rise and the policies and premium at it", "graded_as": "Ask 1",
                "figure": "r4_table", "depends": ["R3"], "independent": "",
                "golden": gold4, "bands": {"rise": u25_band, "policies": fig["u25_policies_band"],
                                           "premium_m": fig["u25_premium_band_m"]},
                "partly_share": 0.67, "precedent": ["L22", "L23"],
                "passes": {"quick": seg_table("u25", quick_u25_rise), "careful": seg_table("u25", careful_u25_rise),
                           "thorough": gold4}})
    gold5 = seg_table("mid", GD["mid_rise"])
    fig["r5_table"] = gold5
    res.append({"id": "R5", "name": "the smallest 25-to-64 rise and the policies and premium at it",
                "graded_as": "Component 2", "figure": "r5_table", "depends": [], "independent": "the claims and the model log",
                "golden": gold5, "bands": {"rise": mid_band, "policies": fig["mid_policies_band"],
                                           "premium_m": fig["mid_premium_band_m"]},
                "partly_share": 0.67, "precedent": ["L12", "L34"],
                "passes": {"quick": seg_table("mid", quick_mid_rise), "careful": seg_table("mid", careful_mid_rise),
                           "thorough": gold5}})
    res.append({"id": "R6", "name": "what the over-65 cut does to 2027 underwriting profit, £ million",
                "graded_as": "Component 3", "figure": "cut_net_m", "depends": [], "independent": "the renewal schedule",
                "golden": fig["cut_net_m"], "band": [fig["cut_net_m"] - 0.4, fig["cut_net_m"] + 0.4],
                "partly": [fig["cut_net_m"] - 1.2, fig["cut_net_m"] + 1.2], "precedent": ["L16"],
                "passes": {"quick": fig["cut_nb_only_m"],
                           "careful": {"value": fig["cut_nb_only_m"], "grade": "partly",
                                       "why": "a careful run reads the renewal pricing policy and the renewal schedule, "
                                              "so about half net the renewal book the lower cap reaches and half price "
                                              "the cut on new business alone (L16); priced as the half"},
                           "thorough": fig["cut_net_m"]}})
    fig["r7_range"] = {"lo": fig["mid_range_lo"], "hi": fig["mid_range_hi"]}
    res.append({"id": "R7", "name": "the 80 per cent range of the 25-to-64 2027 loss ratio at the recommended rise",
                "graded_as": "Ask 2", "figure": "r7_range", "depends": ["R5"], "independent": "",
                "golden": {"lo": fig["mid_range_lo"], "hi": fig["mid_range_hi"]},
                "bands": {"lo": [fig["mid_range_lo"] - 1.5, fig["mid_range_lo"] + 1.5],
                          "hi": [fig["mid_range_hi"] - 1.5, fig["mid_range_hi"] + 1.5]},
                "precedent": ["L34", "L12"],
                "passes": {"quick": {"lo": 0.0, "hi": 0.0},
                           "careful": {"lo": round(care_range[0] * 100, 1), "hi": round(care_range[1] * 100, 1)},
                           "thorough": {"lo": fig["mid_range_lo"], "hi": fig["mid_range_hi"]}}})
    careful_calls = ["under 25: rise of %d per cent" % careful_u25_rise, "25 to 64: rise of %d per cent" % careful_mid_rise,
                     "65 and over: the 3 per cent cut"]
    fig["calls"] = golden_calls
    res.append({"id": "R8", "name": "the three calls", "graded_as": "Recommendation", "figure": "calls",
                "depends": ["R4", "R5", "R6"], "independent": "", "golden": golden_calls, "ordered": True,
                "precedent": ["L11"],
                "passes": {"quick": ["under 25: rise of %d per cent" % quick_u25_rise,
                                     "25 to 64: rise of %d per cent" % quick_mid_rise, "65 and over: the 3 per cent cut"],
                           "careful": careful_calls, "thorough": golden_calls}})
    # hints: each sentence applied to the careful pass's own construction
    lat_curse = M.lr_2027(lat12["u25"](0.0) / (1 + M.INFL), S["u25"]["cur"], S["u25"]["curve"], S["u25"]["conv"], 0.0)
    hint_u25 = M.smallest_change(lambda L: M.lr_2027(lat12["u25"](0.0) / (1 + M.INFL), S["u25"]["cur"],
                                                     S["u25"]["curve"], S["u25"]["conv"], L))
    hint_lr15 = M.lr_2027(lat12["u25"](0.0) / (1 + M.INFL), S["u25"]["cur"], S["u25"]["curve"], S["u25"]["conv"],
                          G.PROPOSAL_U25) * 100
    fig["hint_u25_rise"] = hint_u25
    fig["hint_u25_lr15"] = round(hint_lr15, 1)
    hints = [{"sentence": "the business a higher comparison-site price wins is the business the rating model "
                          "under-priced most", "rescues": ["R3", "R4"]},
             {"sentence": "only the business HPM v7 has priced since 1 February 2026 represents the 25-to-64s, over a full year of "
                          "its seasons", "rescues": ["R5", "R7"]},
             {"sentence": "a new-business cut lowers the cap on every renewal of a customer first sold through the "
                          "sites", "rescues": ["R6"]}]
    routes = [{"name": "the golden", "answer": golden_calls, "golden": True},
              {"name": "the loss-ratio method on the latest twelve months", "answer": careful_calls},
              {"name": "the 2026 policy year to date", "answer": res[-1]["passes"]["quick"]},
              {"name": "the loss-ratio method on the latest twelve months, the triangles' chain ladder",
               "answer": ["under 25: rise of %d per cent" % fig["careful_cl_u25_rise"],
                          "25 to 64: rise of %d per cent" % fig["careful_cl_mid_rise"], "65 and over: the 3 per cent cut"]},
              {"name": "the current book completed, no selection",
               "answer": ["under 25: rise of %d per cent" % fig["completed_u25_rise"],
                          "25 to 64: rise of %d per cent" % fig["completed_mid_rise"], "65 and over: hold, no cut"]},
              {"name": "experience pooled across the refit",
               "answer": ["under 25: rise of %d per cent" % fig["pooled_u25_rise"],
                          "25 to 64: rise of %d per cent" % fig["pooled_mid_rise"], "65 and over: the 3 per cent cut"]}]
    # the lines sit halfway between the golden family and the nearest shortcut on each side
    su = [v for v in sr_all["u25"].values()]
    u_line = int(np.ceil((max(su) + fig["u25_family_lo"]) / 2.0))
    sm_lo = [v for v in sr_all["mid"].values() if v < fig["mid_family_lo"]]
    sm_hi = [v for v in sr_all["mid"].values() if v > fig["mid_family_hi"]]
    m_lo = int(np.ceil((max(sm_lo) + fig["mid_family_lo"]) / 2.0)) if sm_lo else fig["mid_family_lo"]
    m_hi = int(np.floor((min(sm_hi) + fig["mid_family_hi"]) / 2.0)) if sm_hi else fig["mid_family_hi"]
    fig["forcing_lines"] = {"u25": u_line, "mid": [m_lo, m_hi]}
    cls = lambda u, m, o: ["under 25: %d or more" % u_line if u is not None and u >= u_line else
                           "under 25: under %d" % u_line,
                           "25 to 64: %d to %d" % (m_lo, m_hi) if m is not None and m_lo <= m <= m_hi
                           else "25 to 64: outside %d to %d" % (m_lo, m_hi),
                           "65 and over: hold" if o < 0 else "65 and over: cut"]
    gold_cls = cls(GD["u25_rise"], GD["mid_rise"], GD["cut"]["net"])
    fam_entries = []
    for k in fam["u25"]:
        fam_entries.append({"name": "under 25 " + k, "answer": cls(fam_rise["u25"][k], GD["mid_rise"], GD["cut"]["net"])})
    for k in fam["mid"]:
        fam_entries.append({"name": "25 to 64 " + k, "answer": cls(GD["u25_rise"], fam_rise["mid"][k], GD["cut"]["net"])})
    pert = perturbations(D, S, GD, cls)
    nb_alone, net = GD["cut"]["nb"], GD["cut"]["net"]
    short_vals = [("the loss-ratio method on the latest twelve months", careful_u25_rise, careful_mid_rise, nb_alone),
                  ("the 2026 policy year to date", quick_u25_rise, quick_mid_rise, nb_alone),
                  ("the loss-ratio method on the latest twelve months, the triangles' chain ladder",
                   fig["careful_cl_u25_rise"], fig["careful_cl_mid_rise"], nb_alone),
                  ("the current book completed, no selection", fig["completed_u25_rise"], fig["completed_mid_rise"], net),
                  ("experience pooled across the refit", fig["pooled_u25_rise"], fig["pooled_mid_rise"], nb_alone)]
    forcing = {"kind": "set", "golden_answer": gold_cls, "golden_family": fam_entries, "perturbations": pert,
               "shortcuts": [{"name": nm, "answer": cls(u, m, o)} for nm, u, m, o in short_vals]}
    E = {"results": res, "hints": hints, "routes": routes, "forcing": forcing,
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    return fig, E, GD


def perturbations(D, S, GD, cls):
    """Each fitted input moved by its defensible spread (20 per cent where none is known), the call re-read."""
    out = []
    for g_mult, name in ((0.8, "gap-curve slope -20%"), (1.2, "gap-curve slope +20%")):
        def scaled(seg):
            c = S[seg]["curve"]
            return lambda x: c(x) ** g_mult
        u = M.smallest_change(lambda L: M.lr_2027(S["u25"]["base"], S["u25"]["cur"], scaled("u25"), S["u25"]["conv"], L))
        m = M.smallest_change(lambda L: M.lr_2027(S["mid"]["base"], S["mid"]["cur"], scaled("mid"), S["mid"]["conv"], L))
        out.append({"input": name, "answer": cls(u, m, GD["cut"]["net"])})
    for mult, name in ((0.8, "conversion at rank 2 and below -20%"), (1.2, "conversion at rank 2 and below +20%")):
        conv = {g: {k: (v if k == 1 else v * mult) for k, v in S[g]["conv"].items()} for g in ("u25", "mid")}
        u = M.smallest_change(lambda L: M.lr_2027(S["u25"]["base"], S["u25"]["cur"], S["u25"]["curve"], conv["u25"], L))
        m = M.smallest_change(lambda L: M.lr_2027(S["mid"]["base"], S["mid"]["cur"], S["mid"]["curve"], conv["mid"], L))
        out.append({"input": name, "answer": cls(u, m, GD["cut"]["net"])})
    for amp, name in ((0.8, "seasonal amplitude -20%"), (1.2, "seasonal amplitude +20%")):
        s = 1 + (D["s_cost"] - 1) * amp
        D2 = dict(D)
        D2["s_cost"] = s
        bu = M.base_lr(D["pol"], D["clm_dev"], D["expo"], s, G.current_mask(D, "u25"))
        bm = M.base_lr(D["pol"], D["clm_dev"], D["expo"], s, G.current_mask(D, "mid"))
        u = M.smallest_change(lambda L: M.lr_2027(bu, S["u25"]["cur"], S["u25"]["curve"], S["u25"]["conv"], L))
        m = M.smallest_change(lambda L: M.lr_2027(bm, S["mid"]["cur"], S["mid"]["curve"], S["mid"]["conv"], L))
        out.append({"input": name, "answer": cls(u, m, GD["cut"]["net"])})
    for mult, name in ((0.8, "renewal retention slope -20%"), (1.2, "renewal retention slope +20%"),
                       (0.8, "over-65 new-business conversion -20%"), (1.2, "over-65 new-business conversion +20%")):
        c = cut_variant(D, S, name, mult)
        out.append({"input": name, "answer": cls(GD["u25_rise"], GD["mid_rise"], c)})
    return out


def cut_variant(D, S, name, mult):
    if "retention" in name:
        return G.o65_cut(D, S["o65"], slope_mult=mult)["net"]
    S2 = dict(S["o65"])
    S2["conv"] = {k: v * mult for k, v in S["o65"]["conv"].items()}
    return G.o65_cut(D, S2)["net"]


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    fig, E, GD = run(t)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, default=float)
    print(json.dumps({k: v for k, v in fig.items() if k != "r1"}, indent=0, default=float)[:2500])
