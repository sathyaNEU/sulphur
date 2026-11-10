"""task9: the quick pass, the careful but hurried pass and the careful pass with one sentence of help, each computed
end to end by this generator's own implementations of named methods. None reads the prompt.

A pass files one value per result of the chain, in the shape and rounding the answer blocks state the golden in.
"""
import numpy as np

import analysis as AN
import figures as FG
import params as P

IDS = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11"]
FIGURE = {"R1": "R1_avg_3m_usd", "R2": "R2_worst_year_loss_usd", "R3": "R3_old_peak_usd", "R4": "R4_size_usd", "R5": "R5_alt_size_usd",
          "R6": "R6_avg_range_12m", "R7": "R7_avg_range_3m", "R8": "R8_expected_usd", "R9": "R9_range", "R10": "R10_plan", "R11": "R11_call"}
IID = "single settlements resampled"


def golden(F):
    return {rid: F[key] for rid, key in FIGURE.items()}


def quick(A, R):
    """Ten minutes: the new ladder on the years its index is published, the settlement limit read off its worst year,
    the custodian's ledger for collateral, the statements for the open swaps, a full year of new sales, no ranges."""
    val = A.book.val[A.book.val.date == P.STATEMENT]
    own3 = A.ladder_figs(P.NEW_MAT, "none")
    out = {}
    out["R1"] = FG.r1000(own3["avg_per_sale"] * P.PER)
    out["R2"] = FG.r1000(-own3["worst"] * P.PER)
    out["R3"] = FG.r1000(A.book.ledger.groupby("date").posted.sum().max())
    out["R4"] = A.room(P.NEW_MAT, "none", with_old=False, use_c=False)["size"]
    out["R5"] = A.room(P.ALT_MAT, "none", with_old=False, use_c=False)["size"]
    out["R6"] = out["R7"] = out["R9"] = None
    exp27 = A.book.trades[A.book.trades.expiry.dt.year == P.PLAN_YEAR].ticket
    out["R8"] = FG.r1000(val[val.ticket.isin(exp27)].mtm.sum())
    new = FG.r1000(12 * out["R4"] * own3["avg_per_sale"])
    out["R10"] = dict(twelve_month_usd=out["R8"], three_month_usd=new, total_usd=out["R8"] + new, low_usd=None, high_usd=None)
    out["R11"] = dict(size_usd=out["R4"], plan_usd=out["R8"] + new, low_usd=None, high_usd=None)
    return out


def careful(A, R, rebuild=False, real_world=False, dependence=False, unsold=True):
    """An afternoon, careful but hurried, priced on what strong runs do unprompted: every file cleaned and every filed
    rule applied (the record's sale dates, both limits with the standing ladder beside the new one, the cap, the year
    of expiry, the schedule's basis for swaps not yet sold), swaps valued on their remaining term, a stand-in for the
    missing strikes checked on every day the index is published, and the open swaps replayed together from the
    record's start dates for their range. It stops at three moves: the stand-in is a regression on the 30-day index
    alone, which fits the whole overlap well; the open swaps' expected settlement is read off their marks; and
    anything about a ladder's sales is resampled one settlement at a time.

    rebuild=True is the pass told to rebuild the strikes from both neighbouring maturities; real_world=True told that
    the expectation is what such swaps went on to pay on the record; dependence=True told to keep neighbouring sales
    together and run the swaps not yet sold off the same start dates as the open ones."""
    proxy = AN.CAREFUL_PROXY
    L3 = A.ladder(P.NEW_MAT) if rebuild else A.proxy_ladder(P.NEW_MAT, proxy)
    f3 = A.ladder_figs(P.NEW_MAT, ladder=L3)
    out = {}
    out["R1"] = FG.r1000(f3["avg_per_sale"] * P.PER)
    out["R2"] = FG.r1000(-f3["worst"] * P.PER)
    out["R3"] = FG.r1000(-A.marks(P.OLD_MAT).min() * P.OLD_SIZE)
    size = (A.room(P.NEW_MAT) if rebuild else A.room(P.NEW_MAT, ladder=L3))["size"]
    out["R4"] = size
    out["R5"] = A.room(P.ALT_MAT)["size"]
    # the range of each average
    d12, d3 = A.avg_ranges(P.OLD_MAT), A.avg_ranges(P.NEW_MAT, ladder=L3)
    key12, key3 = R["avg_range"][P.OLD_MAT]["golden"], R["avg_range"][P.NEW_MAT]["golden"]
    out["R6"] = FG.range_cells(d12[0][key12] if dependence else d12[1][IID], P.PER)
    out["R7"] = FG.range_cells(d3[0][key3] if dependence else d3[1][IID], P.PER)
    # the open swaps
    rp = R["replay"]
    ob = rp["ob"]
    iv2 = ob.iv.values ** 2
    tot = A.settle(ob, rp["ratio"] * iv2).sum(axis=1)
    out["R8"] = FG.r1000((tot.mean() if real_world else float(A.settle(ob, iv2).sum())) * P.OLD_SIZE)
    out["R9"] = FG.range_cells((np.percentile(tot, 10), np.percentile(tot, 90)), P.OLD_SIZE)
    # the plan
    legs = R["plan"]["legs"]
    n3 = sum(g["ladder"] == P.NEW_MAT for g in legs)
    n12 = sum(g["ladder"] == P.OLD_MAT for g in legs) if unsold else 0
    old_unsold = FG.r1000(n12 * R["ladder"][P.OLD_MAT]["avg_per_sale"] * P.OLD_SIZE)
    new = FG.r1000(n3 * size * f3["avg_per_sale"])
    if dependence:
        t = A.plan(size, rebuild="calibrated" if rebuild else proxy, with_unsold_old=unsold)["total"]
        rng = (float(np.percentile(t, 10)), float(np.percentile(t, 90)))
    else:
        rng = A.plan_unrelated(size, ladder3=L3)
    out["R10"] = FG.plan_cells(out["R8"], old_unsold, new, rng)
    out["R11"] = dict(size_usd=size, plan_usd=out["R10"]["total_usd"], low_usd=out["R10"]["low_usd"], high_usd=out["R10"]["high_usd"])
    return out


# one sentence of help, and what the careful pass does with it taken literally
HINTS = [
    ("on the days that set the limit the 3-month index sits below the 30-day index, so the missing strikes have to come from the maturities "
     "on both sides of three months", dict(rebuild=True)),
    ("an open swap's value is a price: expect what such swaps went on to pay on the record", dict(real_world=True)),
    ("sales a month apart share most of their days, so keep neighbouring sales together when the record is resampled and run the swaps not "
     "yet sold off the same start dates as the open ones", dict(dependence=True)),
    ("value each open swap at the implied volatility for its remaining term, not at the index it was struck on", dict()),
    ("the cap on realized volatility bounds the valuation as well as the settlement", dict()),
    ("the standing ladder's November and December sales also settle in the plan year", dict()),
    ("only the new ladder's sales to September settle inside the plan year", dict()),
]
# two moves at once, printed as information beside the single sentences
COMPOUNDS = [
    ("the rebuild and the expectation", dict(rebuild=True, real_world=True)),
    ("the rebuild and dependence", dict(rebuild=True, dependence=True)),
    ("the expectation and dependence", dict(real_world=True, dependence=True)),
    ("all three", dict(rebuild=True, real_world=True, dependence=True)),
]


def hint_passes(A, R):
    return [(s, careful(A, R, **kw)) for s, kw in HINTS]


def compound_passes(A, R):
    return [(s, careful(A, R, **kw)) for s, kw in COMPOUNDS]
