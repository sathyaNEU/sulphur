"""Every owed figure, computed from the cut pack by analysis.py: the golden chain, the rival methods that set each
result's band (the golden family), and the hurried routes the effort test prices. One option set runs the whole
chain, so a rival or a shortcut is the golden with one step done another way."""
import numpy as np
import pandas as pd

import analysis as A

SIZES = A.SIZES
GOLDEN = {"loss": "stock", "fleet": "stock", "hold": "linear", "width": 0.2, "store": "walk", "elastic": None,
          "share_days": 120, "holding_months": (5, 6, 7, 8, 9), "loss_scale": 1.0, "hold_scale": 1.0,
          "pipe_scale": 1.0, "elastic_scale": 1.0, "depot_rule": "beers", "share_basis": "fills"}
_CACHE = {}


def chain(F, tp, lw, opt):
    o = dict(GOLDEN)
    o.update(opt)
    A.PIPE_DAYS.clear()
    A.pipe_days(F, tp)
    for k in A.PIPE_DAYS:
        A.PIPE_DAYS[k] *= o["pipe_scale"]
    A.SHARE_DAYS[0] = o["share_days"]
    A.DEPOT_RULE[0] = o["depot_rule"]
    A.SHARE_BASIS[0] = o["share_basis"]
    key = ("yl", o["share_days"], o["share_basis"])
    if key not in _CACHE:
        _CACHE[key] = A.year_loss(F, tp)
    yl = dict(_CACHE[key])
    yl["loss"] = {s: v * o["loss_scale"] for s, v in yl["loss"].items()}
    if o["loss"] == "gate":
        yl = dict(yl)
        yl["loss"] = A.gate_loss(F)
    elif o["loss"] == "no_stock_change":
        yl = dict(yl)
        yl["loss"] = {s: yl["sent"][s] - yl["back"][s] for s in SIZES}
    if o["fleet"] == "register":
        u2 = A.register_active(F)
    elif o["fleet"] == "register_less_losses":
        reg = A.register_active(F)
        y1 = {s: A.fills_between(F, A.T1 - pd.Timedelta(days=730), A.T1 - pd.Timedelta(days=365))[s] -
              A.own_back(F, A.T1 - pd.Timedelta(days=730), A.T1 - pd.Timedelta(days=365))[s] for s in SIZES}
        y2 = {s: A.fills_between(F, A.T1 - pd.Timedelta(days=365), A.T1)[s] -
              A.own_back(F, A.T1 - pd.Timedelta(days=365), A.T1)[s] for s in SIZES}
        u2 = {s: reg[s] - y1[s] - y2[s] - yl["loss"][s] for s in SIZES}
    else:
        u2, _ = A.usable(F, tp, yl["out2"])
    if "R3" not in _CACHE:
        _CACHE["R3"] = A.busiest_deliveries(F, lw)
    R3 = _CACHE["R3"]
    key = ("hd", o["holding_months"])
    if key not in _CACHE:
        _CACHE[key] = A.holding_data(F, o["holding_months"])
    hd = _CACHE[key]
    hs = o["hold_scale"]
    if o["hold"] == "binned":
        hold = lambda s, r: hs * A.holding_binned(hd, s, r, width=o["width"])
    elif o["hold"] == "linear":
        bb = {z: A.fit_holding(hd[(hd.interval == 7.0) & (hd["size"] == z)]) for z in SIZES}
        hold = lambda s, r: hs * float(A.predict_holding(bb[s], 1, r, 7.0, 1))
    else:
        hold = None
    fg27 = None
    el = o["elastic"]
    if o["elastic_scale"] != 1.0:
        base = A.need_2027(F, tp, yl, R3, lw, hd, hold_fn=hold, fg27=fg27)
        el = {s: base[s]["elasticity"] * o["elastic_scale"] for s in SIZES}
    R6 = A.need_2027(F, tp, yl, R3, lw, hd, hold_fn=hold, fg27=fg27, elastic=el)
    if o["hold"] == "turns":
        for s in (50, 30):
            df = R6[s]["weekly"].copy()
            wk = R6[s]["week"]
            adj = A.turns_holding(F, tp, R3, s) - (df.loc[wk, "new_lines"] + df.loc[wk, "new_pipe"])
            df["total"] = df["total"] + adj
            R6[s] = dict(R6[s], weekly=df, peak=float(df.total.max()), week=df.total.idxmax())
    if o["store"] == "days_cover":
        s = 20
        df = R6[s]["weekly"].copy()
        for wk in df.index:
            df.loc[wk, "foundry_store"] = A.foundry_days_of_cover(F, R3, wk)
        df["total"] = df[["existing", "new_lines", "new_pipe", "foundry_store"]].sum(axis=1)
        R6[s] = dict(R6[s], weekly=df, peak=float(df.total.max()), week=df.total.idxmax())
    if o.get("need") == "turns":
        for s in SIZES:
            days = A.dwell_at_customers(tp, s)
            df = R6[s]["weekly"].copy()
            df["total"] = R3[s]["weekly"].values / 7.0 * days
            R6[s] = dict(R6[s], weekly=df, peak=float(df.total.max()), week=df.total.idxmax())
    order = A.order(F, tp, yl, u2, R3, R6)
    out = {"loss": yl["loss"], "fleet": u2, "deliv": {s: R3[s]["point"] for s in SIZES},
           "deliv_lo": {s: R3[s]["lo"] for s in SIZES}, "deliv_hi": {s: R3[s]["hi"] for s in SIZES},
           "deliv_week": {s: R3[s]["week"] for s in SIZES}}
    out["estate"] = {s: float(R6[s]["weekly"].loc[R6[s]["week"], "new_lines"]) for s in (50, 30)}
    out["store"] = float(R6[20]["weekly"].loc[R6[20]["week"], "foundry_store"])
    out["week"] = {s: R6[s]["week"] for s in SIZES}
    out["need_parts"] = {s: R6[s]["weekly"].loc[R6[s]["week"]].to_dict() for s in SIZES}
    out["need"] = {s: order[s]["need"] for s in SIZES}
    out["float"] = {s: order[s]["float"] for s in SIZES}
    out["have"] = {s: order[s]["have"] for s in SIZES}
    out["lost_to_week"] = {s: order[s]["lost_to_week"] for s in SIZES}
    out["buy"] = {s: order[s]["buy"] for s in SIZES}
    out["elasticity"] = {s: R6[s]["elasticity"] for s in SIZES}
    out["_R3"] = R3
    out["_R6"] = R6
    out["_yl"] = yl
    return out


FAMILY = {
    "the fleet's kegs out at the two stocktakes held equal (no change in the trade)": {"loss": "no_stock_change"},
    "the holding read off counted lines within 0.2 kegs a week of the plan's rate": {"hold": "binned", "width": 0.2},
    "the holding read off counted lines within 0.35 kegs a week of the plan's rate": {"hold": "binned", "width": 0.35},
    "the straight-line holding fit on every quarter's counts": {"holding_months": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)},
    "the tagged share of fills taken over the last 60 days": {"share_days": 60},
    "the depots' Foundry stock following the beers on sale and their sales": {"depot_rule": "beers_and_rate"},
    "the tagged kegs scaled by their share of the register's active kegs": {"share_basis": "register"},
}

HURRIED = {
    "gate": {"loss": "gate"},
    "register": {"fleet": "register"},
    "estate_turns": {"hold": "turns"},
    "store_cover": {"store": "days_cover"},
    "fleet_turns": {"need": "turns"},
}


def careful_route():
    """the careful but hurried pass: every file cleaned, the gate counters' loss, the register as the fleet, the
    estate and the Foundry range carried at the fleet's own turns and days of cover"""
    return {"loss": "gate", "fleet": "register", "hold": "turns", "store": "days_cover"}


PERTURB = {"the year's loss 10 per cent lower (its rivals' spread)": {"loss_scale": 0.9},
           "the year's loss 10 per cent higher": {"loss_scale": 1.1},
           "the holding per line 8 per cent lower (its rivals' spread)": {"hold_scale": 0.92},
           "the holding per line 8 per cent higher": {"hold_scale": 1.08},
           "the days on the way 20 per cent shorter": {"pipe_scale": 0.8},
           "the days on the way 20 per cent longer": {"pipe_scale": 1.2},
           "circulation's response to deliveries 20 per cent weaker": {"elastic_scale": 0.8},
           "circulation's response to deliveries 20 per cent stronger": {"elastic_scale": 1.2}}


def compute(target):
    _CACHE.clear()
    F = A.load(target)
    tp = A.trips(F)
    lw = A.weekly_weather(F)
    G = {"golden": chain(F, tp, lw, {})}
    G["perturbed"] = {k: chain(F, tp, lw, v) for k, v in PERTURB.items()}
    G["family"] = {k: chain(F, tp, lw, v) for k, v in FAMILY.items()}
    G["hurried"] = {k: chain(F, tp, lw, v) for k, v in HURRIED.items()}
    G["careful"] = chain(F, tp, lw, careful_route())
    G["turns_estate"] = {s: A.turns_holding(F, tp, G["golden"]["_R3"], s) for s in (50, 30)}
    G["quick"], G["quick_deliv"], G["quick_need"] = quick(F, tp, lw)
    G["register"] = A.register_active(F)
    G["gate_loss"] = A.gate_loss(F)
    G["F"] = F
    G["tp"] = tp
    return G


def quick(F, tp, lw):
    """ten minutes: the register as the fleet, last summer's busiest week's deliveries at the fleet's turns"""
    reg = A.register_active(F)
    out, deliv, need = {}, {}, {}
    for s in SIZES:
        g = A.gate_daily(F, s).resample("W-SUN").sum()
        peak = float(g["2026-05-01":"2026-09-30"].max())
        fills = A.fills_between(F, A.T1, A.T2)[s]
        turns_days = reg[s] / fills * 365.0
        deliv[s] = peak
        need[s] = peak / 7.0 * turns_days
        out[s] = max(0.0, need[s] - reg[s])
    return out, deliv, need
