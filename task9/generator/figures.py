"""task9 (architecture 10): every graded figure on the cut pack, its band from the defensible rivals, and the figures
each hurried route files.

The golden is one route of analysis.py (the exact replay from the covers and the winners' prints, each trade's cost read
30 trading days on, the year drawn in 21-day blocks). A band is the span the rivals land in (other cost horizons on
either side of complete, other tape-matching windows, unmatched losses taken at the matched rate, other block lengths)
widened by a stated margin; every hurried route is asserted outside it in checks.py.
"""
import json

import numpy as np

import params as P
from analysis import Analysis
from record import Record

SIMS = P.SIMS
GOLD = dict(win="exact", H=30, added="own", unmatched="lost")
RIVALS = {
    "the cost read 25 trading days on": dict(GOLD, H=25),
    "the cost read 45 trading days on": dict(GOLD, H=45),
    "unmatched losses won at the matched losses' rate": dict(GOLD, unmatched="share"),
}
MATCH_RIVALS = {"prints matched within 2 minutes": 120, "prints matched within 5 minutes": 300}
BLOCK_RIVALS = (10, 42, 63)
ROUTES = {
    "careful but hurried": dict(win="logit", H=5, added="avg", iid=True),
    "the tape's levels, a week's marks": dict(win="exact", H=5, added="own", iid=True),
    "complete moves, a fit on the desk's quotes": dict(win="logit", H=30, added="avg", iid=True),
    "a fit on the desk's quotes, each request's own cost": dict(win="logit", H=5, added="own", iid=True),
    "the desk's next-day view": dict(win="exact", H=1, added="own", iid=True),
    "the tape's levels, today's wins' cost for the added trades": dict(win="exact", H=30, added="avg", iid=False),
    "the golden's figures, days drawn one at a time": dict(win="exact", H=30, added="own", iid=True),
    "careful, the year in blocks": dict(win="logit", H=5, added="avg", iid=False),
    "the tape's levels, a week's marks, the year in blocks": dict(win="exact", H=5, added="own", iid=False),
    # the careful pass re-priced on the judge's first pass (rivals' levels from the tape earned), and its one-move neighbours
    "the tape's levels, a week's marks, today's wins' cost for the added trades": dict(win="exact", H=5, added="avg", iid=True),
    "the tape's levels, complete moves, today's wins' cost for the added trades, days one at a time":
        dict(win="exact", H=30, added="avg", iid=True),
    "the tape's levels, a week's marks, today's wins' cost for the added trades, the year in blocks":
        dict(win="exact", H=5, added="avg", iid=False),
}
CAREFUL = "the tape's levels, a week's marks, today's wins' cost for the added trades"
MARGIN = {"usd": 0.04, "share": 0.02, "cost": 25.0, "cost_rel": 0.08}   # band margins: 4 per cent of a P&L figure, 2 points of a
# share, and for a cost a million the larger of USD 25 and 8 per cent of the figure


def _figures(A, kw, block=P.BLOCK, iid=False, sims=SIMS):
    out, dc, dp = A.plan(**{k: v for k, v in kw.items() if k != "iid"})
    segs = A.rec.changed
    cur = sum(v["cur"] for v in out.values())
    prop = sum(v["prop"] for v in out.values())
    lo, hi, mu = Analysis.year_range(dp, block=block, sims=sims, iid=iid or kw.get("iid", False))
    bridge = {"|".join(s): out[s]["prop"] - out[s]["cur"] for s in segs}
    return dict(current=cur, proposed=prop, p10=lo, p90=hi, bridge=bridge,
                lose=sorted(k for k, v in bridge.items() if v < 0),
                share={"|".join(s): out[s]["share"] for s in segs},
                won_cost={"|".join(s): out[s]["won_cost"] for s in segs},
                add_cost={"|".join(s): out[s]["add_cost"] for s in segs},
                adopt=cur + sum(v for v in bridge.values() if v > 0))


def _band(values, margin, rel=False):
    lo, hi = min(values), max(values)
    m = margin * max(abs(lo), abs(hi)) if rel else margin
    return [lo - m, hi + m]


def compute(tgt, sims=SIMS):
    A = Analysis(Record(tgt))
    F = {"segments": ["|".join(s) for s in A.rec.changed], "match_rate": A.match_rate}
    # the replay at the current schedule, where it equals the schedule each request was quoted at, keeps its outcome
    R = A.R
    same = np.isclose(R.h_cur.values, R.h_actual.values)
    r, won = R.r.values, R.won.values
    d0 = np.nan_to_num(R.d_old.values)
    wc = np.isfinite(r) & R.traded.values & ((d0 < r) | (won & (d0 <= r + 1e-9)))
    F["replay_check"] = {"rows": int(same.sum()), "differ": int((same & (wc != won)).sum())}
    # the daily P&L's serial dependence, the named data that rules out drawing the year's days one at a time (6c)
    _, _, dprop = A.plan(**GOLD)
    x = np.asarray(dprop, float)
    xm = x - x.mean()
    s21 = np.convolve(x, np.ones(21), "valid")
    F["dependence"] = {"acf1": float(np.dot(xm[:-1], xm[1:]) / np.dot(xm, xm)), "noise_bound": float(2 / np.sqrt(len(x))),
                       "vr21": float(s21.var() / (21 * x.var())), "days": int(len(x))}
    g = _figures(A, GOLD, sims=sims)
    F["gold"] = g
    riv = {k: _figures(A, kw, sims=sims) for k, kw in RIVALS.items()}
    # tape-matching windows
    import analysis as AN
    keep = AN.MATCH_SECONDS
    for name, sec in MATCH_RIVALS.items():
        AN.MATCH_SECONDS = sec
        A2 = Analysis(A.rec)
        riv[name] = _figures(A2, GOLD, sims=sims)
    AN.MATCH_SECONDS = keep
    blocks = {b: _figures(A, GOLD, block=b, sims=sims) for b in BLOCK_RIVALS}
    F["rivals"] = riv
    allv = [g] + list(riv.values())
    F["bands"] = {
        "current": _band([v["current"] for v in allv], MARGIN["usd"], rel=True),
        "proposed": _band([v["proposed"] for v in allv], MARGIN["usd"], rel=True),
        "adopt": _band([v["adopt"] for v in allv], MARGIN["usd"], rel=True),
        "p10": _band([v["p10"] for v in allv + list(blocks.values())], MARGIN["usd"], rel=True),
        "p90": _band([v["p90"] for v in allv + list(blocks.values())], MARGIN["usd"], rel=True),
        "bridge": {s: _band([v["bridge"][s] for v in allv], max(25e3, 0.10 * abs(g["bridge"][s]))) for s in F["segments"]},
        "share": {s: _band([v["share"][s] for v in allv], MARGIN["share"]) for s in F["segments"]},
        "won_cost": {s: _band([v["won_cost"][s] for v in allv], max(MARGIN["cost"], MARGIN["cost_rel"] * abs(g["won_cost"][s])))
                     for s in F["segments"]},
        "add_cost": {s: _band([v["add_cost"][s] for v in allv if v["add_cost"][s] is not None],
                              max(MARGIN["cost"], MARGIN["cost_rel"] * abs(g["add_cost"][s] or 0)))
                     for s in F["segments"]},
    }
    # a changed segment whose sign moves under any defensible rival may be named either way
    F["lose_either"] = sorted(s for s in F["segments"] if len({v["bridge"][s] < 0 for v in allv}) > 1)
    F["routes"] = {k: _figures(A, kw, sims=sims) for k, kw in ROUTES.items()}
    F["blocks"] = {str(b): [v["p10"], v["p90"]] for b, v in blocks.items()}
    F["scale"] = {"|".join(k): float(v) for k, v in A.scale.items()}
    R = A.R
    # the markout curve of today's wins in every segment, and where the evaluations' lag shows outside the draft
    curve = {}
    for H in (1, 5, 10, 20, 30, 45):
        c = A.cost(H)
        for sk in sorted(R.seg.unique()):
            m = ((R.seg == sk) & R.won).values
            if m.sum() >= 150:
                curve.setdefault(sk, {})[str(H)] = float(np.average(c[m], weights=R.q.values[m]) * 100)
    F["markout_curve"] = curve
    unchanged = [sk for sk, c in curve.items() if sk not in F["segments"] and sk.split("|")[1] in ("medium", "thin") and
                 (c["30"] - c["5"]) / max(abs(c["30"]), 1.0) > 0.1]
    F["footprint"] = {"unchanged_with_lag": len(unchanged), "segments": unchanged}
    F["h"] = {"|".join(s): [A.rec.current[s], A.rec.proposed[s]] for s in A.rec.changed}
    gold_out, _, _ = A.plan(**{k: v for k, v in GOLD.items()})
    F["today_share"] = {"|".join(s): float(gold_out[s]["cur_share"]) for s in A.rec.changed}
    F["quick"] = quick(A, tgt)
    F["routes_shown"] = {
        "The desk's next-day view (the month-end summaries' markout)": F["routes"]["the desk's next-day view"],
        "A week's marks, rivals' levels from the tape": F["routes"]["the tape's levels, a week's marks"],
        "A win model fitted on the desk's own quotes, added trades costed like today's wins":
            F["routes"]["careful but hurried"],
        "Rivals' levels from the tape, added trades costed like today's wins":
            F["routes"]["the tape's levels, today's wins' cost for the added trades"],
        "Rivals' levels from the tape, a week's marks, added trades costed like today's wins": F["routes"][CAREFUL],
    }
    gb = F["gold"]
    sel = sorted(F["segments"], key=lambda x: (gb["add_cost"][x] or 0) - (gb["won_cost"][x] or 0))
    F["note_examples"] = [sel[0], sel[-1]]
    # the golden's figures under the keys effort.json names (the answer blocks state them from here)
    F.update(won_cost=gb["won_cost"], share=gb["share"], add_cost=gb["add_cost"], current=gb["current"], proposed=gb["proposed"],
             range={"P10": gb["p10"], "P90": gb["p90"]}, bridge=gb["bridge"], rec={"plan": gb["adopt"], "drop": gb["lose"]})
    return F


def quick(A, tgt):
    """The ten-minute pass: the desk's month-end summaries for the base year, the draft read as spread given up."""
    import os
    from openpyxl import load_workbook
    import pack as PK
    wb = load_workbook(os.path.join(tgt, PK.F["summaries"]), read_only=True)
    code = {v: k for k, v in PK.TYPE_NAME.items()}
    tot, face, mk, edge, done, req = 0.0, {}, {}, {}, {}, {}
    for name in wb.sheetnames:
        if not (P.BASE_FROM[:7] <= name <= P.BASE_TO[:7]):
            continue
        for row in wb[name].iter_rows(min_row=5, values_only=True):
            if not row or row[0] not in ("IG", "HY"):
                continue
            k = "%s|%s|%s" % (row[0], row[1], code[row[2]])
            req[k] = req.get(k, 0) + row[3]
            done[k] = done.get(k, 0) + row[4]
            face[k] = face.get(k, 0) + row[5] * 1e6
            edge[k] = edge.get(k, 0) + row[6]
            mk[k] = mk.get(k, 0) + row[7]
            tot += row[8]
    segs = ["|".join(s) for s in A.rec.changed]
    cost = {s: (-mk[s] / face[s] * 1e6 if face.get(s) else None) for s in segs}
    give = {s: -(A.rec.current[tuple(s.split("|"))] - A.rec.proposed[tuple(s.split("|"))]) * face.get(s, 0) / 1e4 for s in segs}
    return dict(current=tot, proposed=tot + sum(give.values()), p10=None, p90=None, bridge=give,
                lose=sorted(s for s in segs if give[s] < 0), share={s: done[s] / req[s] for s in segs},
                won_cost=cost, add_cost=cost, adopt=tot)


def write(F, path):
    json.dump(F, open(path, "w"), indent=1, sort_keys=True, default=float)
