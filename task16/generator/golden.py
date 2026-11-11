"""figures.json: every figure the answer blocks and the golden files state, emitted from the analysis."""
import numpy as np

import analysis as AN
import params as P
import results as RS

FAM = P.FAM
NAME = dict(P.FAMILIES)
CLASS_LABEL = {"ON": "on time", "L1": "one day late", "L2": "two or more days late", "EX": "exception"}


def assemble(O):
    G = O["golden"]
    g = RS.figures(G)
    F = dict(g)
    F["line"] = P.LINE
    F["families"] = NAME
    F["by_channel"] = G["by_channel"]
    F["linked_followed"] = int(G["linked_any"])
    F["linked"] = {"conversations": g["conversations"], "linked_rate": g["linked_rate"]}
    F["season"] = {"late_share": g["late_share"], "per_week": g["per_week"]}
    F["expected_table"] = dict(g["expected"], ALL=g["expected_all"])
    F["half_table"] = dict(g["half"], ALL=g["half_all"])
    F["range_table"] = dict({k: [g["low"][k], g["high"][k]] for k in FAM}, ALL=[g["low_all"], g["high_all"]])
    F["keep"] = g["call"]["keep"]; F["hand_back"] = g["call"]["hand_back"]
    F["keep_names"] = [NAME[k] for k in F["keep"]]; F["hand_back_names"] = [NAME[k] for k in F["hand_back"]]
    t = G["tick"]
    F["tick"] = {"hit_rate": round(100 * t["sens"], 1), "false_rate": round(100 * t["false"], 1), "keyed_calls": t["keyed_calls"],
                 "unkeyed_calls": t["unkeyed_calls"], "keyed_follow": t["keyed_follow"],
                 "unkeyed_follow_tick": int(round(t["unkeyed_follow_tick"])), "unkeyed_follow_capture": int(round(t["unkeyed_follow_capture"]))}
    F["recon"] = G["recon"]
    d = G["diag"]
    F["day_dispersion"] = round(d["day_dispersion"], 1)
    F["alerted_rate"] = round(d["alerted_rate"], 1); F["unalerted_like_rate"] = round(d["unalerted_like_rate"], 1); F["alerted_n"] = d["alerted_n"]
    F["cells"] = {f: {c: (round(100 * float(G["cell"][i, j]), 1) if G["n"][i, j] > 0 else None) for j, c in enumerate(P.CLASSES)} for i, f in enumerate(FAM)}
    F["cell_n"] = {f: {c: int(round(G["n"][i, j])) for j, c in enumerate(P.CLASSES)} for i, f in enumerate(FAM)}
    M = G["M"]; S = O["S"]
    rho = G["rho"].sum(axis=0)
    F["mix"] = {c: {"plan_parcels": int(round(S["Wc"][j], -3)), "contact_per_1000": round(1000 * float(rho[j]), 1),
                    "conversations": int(round(M[:, j].sum(), -2)), "share": round(100 * float(M[:, j].sum() / M.sum()), 1),
                    "observed_share": round(100 * float(G["n"][:, j].sum() / G["n"].sum()), 1)} for j, c in enumerate(P.CLASSES)}
    F["season_conversations"] = int(round(M.sum(), -2))
    F["season_weight_late"] = {f: round(100 * float(M[i, 1:].sum() / M[i].sum()), 1) for i, f in enumerate(FAM)}
    F["weeks"] = int(S["weeks"])
    F["alert_by_class"] = {("one day late" if k == 1 else "two or more days late"): round(100 * float(v), 0) for k, v in G["es"].items()}
    F["routes"] = {}
    for name, (label, _, _) in RS.ROUTES.items():
        r = RS.figures(O[name])
        F["routes"][name] = {"label": label, "expected": dict(r["expected"], ALL=r["expected_all"]), "keep": r["call"]["keep"],
                             "achieved_all": r["achieved_all"], "half_all": r["half_all"], "per_week": r["per_week"],
                             "late_share": r["late_share"], "alert_effect": r["alert_effect"],
                             "phone_unkeyed_share": r["phone_unkeyed_share"], "written_open": r["written_open"]}
    c = F["routes"]["asis"]                        # the weeks observed carried forward, on this workbook's own restored rates
    F["hurried"] = {"keep": c["keep"], "extra": [k for k in c["keep"] if k not in F["keep"]], "expected": c["expected"],
                    "half_all": F["routes"]["careful"]["half_all"]}
    F["rivals"] = {name: dict({k: round(float(x), 1) for k, x in zip(FAM, R["expected"])}, ALL=round(float(R["expected_all"]), 1)) for name, R in O["rivals"]}
    F["as_of"] = "2026-11-09"
    F["bands"] = bands(F)
    F["stated"] = {"precision": 0.1, "window_hours": 168, "range_level": 90, "resamples": 1000, "standard": "KS-07",
                   "clauses": [2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.2, 4.3, 5.1, 5.2], "dates": ["28 September", "1 November 2026", "12 October", "16 November", "9 November"],
                   "per_thousand": 1000, "families": 10, "kept": 5, "handed_back": 5, "pilot_depots": 3, "other_depots": 7,
                   "sound_variants": len(O["rivals"]), "version": 3, "steps": list(range(1, 11))}
    return F


def bands(F):
    """Each graded figure's band, as the answer blocks state it."""
    B = RS.BAND
    g = F
    out = {
        "linked": {"conversations": [int(g["conversations"] * (1 - B["conversations"])), int(round(g["conversations"] * (1 + B["conversations"])))],
                   "linked_rate": [round(g["linked_rate"] - B["linked_rate"], 1), round(g["linked_rate"] + B["linked_rate"], 1)]},
        "phone_unkeyed_share": list(B["phone_unkeyed_share"]),
        "written_open": [int(round(g["written_open"] * (1 - B["written_open"]))), int(round(g["written_open"] * (1 + B["written_open"])))],
        "achieved_all": [round(g["achieved_all"] - B["achieved_all"], 1), round(g["achieved_all"] + B["achieved_all"], 1)],
        "alert_effect": list(B["alert_effect"]),
        "season": {"late_share": [round(g["late_share"] - B["late_share"], 1), round(g["late_share"] + B["late_share"], 1)],
                   "per_week": [int(round(g["per_week"] * (1 - B["per_week"]), -2)), int(round(g["per_week"] * (1 + B["per_week"]), -2))]},
        "expected_table": dict({k: [round(g["expected"][k] - B["expected"][k], 1), round(g["expected"][k] + B["expected"][k], 1)] for k in FAM},
                               ALL=[round(g["expected_all"] - B["expected_all"], 1), round(g["expected_all"] + B["expected_all"], 1)]),
        "half_table": {k: [round(v * B["half_ratio"][0], 2), round(v * B["half_ratio"][1], 2)] for k, v in F["half_table"].items()},
    }
    return out
