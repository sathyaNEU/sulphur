"""task9: figures.json, every figure the answer blocks state, from the golden analysis run on the cut pack, at the
precision the blocks print it."""
import json

import numpy as np

import effort_passes as EP


def r1(x, k=1):
    return round(float(x), k)


def compute(F, X):
    g = X["vr"]
    fg = {}
    fg["R1_shortfall"] = {"VX40": r1(F["R1"]["VX40"]["shortfall"]), "VP12": r1(F["R1"]["VP12"]["shortfall"])}
    fg["R2_loop"] = {"cause": EP.LABEL["R2"], "VX40": r1(F["R2"]["cost_vx40"]), "VR90": r1(g["cost"]["loop"])}
    fg["R3_bath"] = {"cause": EP.LABEL["R3"], "VX40": r1(F["R3"]["cost_vx40"]), "VR90": r1(g["cost"]["bath"])}
    fg["R4_edge"] = {"cause": EP.LABEL["R4"], "VX40": r1(F["R4"]["cost_vx40"]), "VR90": r1(g["cost"]["edge"], 2)}
    fg["R5_etch"] = {"cause": EP.LABEL["R5"], "VX40": r1(F["R5"]["cost_vx40"]), "VR90": r1(g["cost"]["etch"]),
                     "interval": int(round(F["R5"]["no_flake"] / 10.0) * 10)}
    fg["R6_fixed"] = r1(100 * g["y_fixed"])
    fg["R7_plan"] = {"plan": r1(100 * g["y_plan"]), "starts": int(round(g["starts_fixed"], -1))}
    # supporting figures the write-up states
    fg["vx40_base_good"], fg["vx40_win_good"] = r1(F["R1"]["VX40"]["base"]), r1(F["R1"]["VX40"]["win"])
    fg["vp12_base_good"], fg["vp12_win_good"] = r1(F["R1"]["VP12"]["base"]), r1(F["R1"]["VP12"]["win"])
    fg["residual_vx40"] = r1(F["R1"]["VX40"]["shortfall"] - F["R2"]["cost_vx40"] - F["R3"]["cost_vx40"] - F["R4"]["cost_vx40"]
                             - F["R5"]["cost_vx40"])
    br, raw = F["R2"]["by_regime"], F["R2"]["raw_by_regime"]
    fg["bin5_by_polisher"] = {t: {k: r1(v) for k, v in raw[t].items()} for t in ("CM2", "CM4", "CM1", "CM3")}
    fg["bin5_at_risk"] = {t: {k: r1(v) for k, v in br[t].items()} for t in ("CM2", "CM4", "CM1", "CM3")}
    fg["taps_m"] = {t: int(F["R2"]["tap"][t]) for t in ("CM2", "CM4", "CM1", "CM3")}
    fg["harmonise_alone_vx40"] = r1(F["R4"]["harmonise_alone"])
    fg["harmonise_claimed_vx40"] = r1(F["R4"]["harmonise_claimed"])
    fg["thick_excess_vx40"] = r1(F["R4"]["cls"]["VX40"]["thick"]["b3"])
    fg["thin_excess_vx40"] = r1(F["R4"]["cls"]["VX40"]["thin"]["b4"])
    fg["pair_share_pct"] = r1(100 * F["R4"]["share"]["pair"])
    fg["bath_drag_ppb_per_wafer"] = round(F["R3"]["fit"]["drag"], 4)
    fg["bath_c_fresh_ppb"] = round(F["R3"]["fit"]["c_fresh"], 2)
    fg["goi_threshold_ppb"] = round(F["R3"]["goi"]["c_th"], 2)
    fg["polymer_factor"] = round(F["R5"]["fit"]["kappa"], 2)
    fg["polymer_onset_rf_s"] = int(F["R5"]["fit"]["l_th"])
    fg["nb_alpha"] = round(F["R6"]["nb"]["alpha"], 2)
    fg["nb_D_per_cm2"] = round(F["R6"]["nb"]["D_per_mm2"] * 100, 3)
    fg["vr90_random_yield_pct"] = r1(100 * F["R6"]["parts"]["rand"])
    pt = F["R6"]["parts"]
    fg["vr90_fixed_parts"] = {"scratch": r1(100 * pt["scr"]["fixed"]), "gate_oxide": r1(100 * pt["goi"]["fixed"]),
                              "edge_die": r1(100 * pt["fall"])}
    import analysis as A
    fg["vr90_tile_fixed"] = r1(100 * A.tile_route(X["pk"]))
    fg["vr90_starts_plan"] = int(round(g["starts_plan"], -1))
    fg["vr90_gross"] = int(F["R6"]["grid_n"])
    fg["call_changes"] = EP.change_set(g)
    return fg


def write(fg, path):
    json.dump(fg, open(path, "w"), indent=1, sort_keys=True, ensure_ascii=False)
