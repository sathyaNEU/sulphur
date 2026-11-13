"""Build the pack under target/: the history (sim.py), the data files (pack.py), the documents (docs.py), every office
container laid out as Office saves it (the house writers), each file's own save time. Then the 2027 truth run, which
the pack never sees."""
import datetime as dt
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
GMT = dt.timezone.utc
OFFICE = {"register": ("2026-11-30T16:40:00Z", "2026-12-01T17:05:00Z", P.PEOPLE["fleet"]),
          "stocktake": ("2024-12-02T09:10:00Z", "2026-12-01T15:31:00Z", P.PEOPLE["fleet"]),
          "recovery": ("2026-12-01T10:02:00Z", "2026-12-01T10:02:00Z", "KegTrace accounts"),
          "plan": ("2026-10-20T13:15:00Z", "2026-11-26T17:48:00Z", P.PEOPLE["sales"]),
          "cask": ("2026-11-30T15:58:00Z", "2026-11-30T16:20:00Z", P.PEOPLE["fleet"])}
EXPORTED = {"rfid": dt.datetime(2026, 12, 1, 14, 14, 51, tzinfo=GMT),
            "visits": dt.datetime(2026, 12, 1, 14, 31, 7, tzinfo=GMT),
            "gate": dt.datetime(2026, 12, 1, 14, 38, 40, tzinfo=GMT),
            "washer": dt.datetime(2026, 12, 1, 15, 2, 13, tzinfo=GMT),
            "fills": dt.datetime(2026, 12, 1, 15, 4, 55, tzinfo=GMT),
            "repairs": dt.datetime(2026, 12, 1, 15, 9, 26, tzinfo=GMT),
            "audits": dt.datetime(2026, 11, 27, 16, 44, 2, tzinfo=GMT),
            "weather": dt.datetime(2026, 12, 1, 11, 26, 30, tzinfo=GMT),
            "erp": dt.datetime(2026, 12, 1, 15, 40, 18, tzinfo=GMT),
            "packline": dt.datetime(2026, 12, 1, 18, 2, 44, tzinfo=GMT)}


def volume_plan(w, plans):
    agg = defaultdict(float)
    for d, kid, s, sku in w.ev["fill"]:
        if d.year == 2026:
            agg[sku if not sku.startswith("F") else "FOUNDRY"] += s / 100.0
    est = defaultdict(float)
    for e in plans["estate"]:
        for code, r in e["lines"].items():
            wk = (dt.date(2027, 12, 31) - e["start"]).days / 7.0
            est[code] += r * wk * w.sku_info[code][2] / 100.0
    taps = sum(t["rate"] * (dt.date(2027, 12, 31) - t["start"]).days / 7.0 * 0.2 for t in plans["foundry_taps"])
    rows = []
    for code, name, size, style, tk, xm in P.SKUS:
        a = agg[code]
        full = a * 12.4 / 11.0
        p = full * 1.01 + est.get(code, 0.0)
        note = "includes Maplestead from April" if code in est else ""
        rows.append((code, name, round(a), round(p / 10) * 10, note))
    a = agg["FOUNDRY"]
    rows.append(("FOUNDRY", "Foundry range", round(a), round((a * 12.4 / 11.0 * 1.12 + taps) / 10) * 10,
                 "18 beers in 2027 (8 in 2026); new taps from April"))
    return rows


def run(target):
    os.makedirs(target, exist_ok=True)
    Fp = {k: os.path.join(target, v) for k, v in FILES.items()}
    rng = np.random.default_rng(P.SEED)
    w = sim.build_world(rng)
    w = sim.run_history(w)
    plans = sim.make_plans(w)
    # the brew plan is the head brewer's, made from the stock at the end of November
    brew = sim.foundry_brew_plan(w, plans, w.engine)
    plans["foundry_brews"] = {s: v[2] for s, v in brew.items()}
    plans["volume"] = volume_plan(w, plans)
    n = {}
    n["rfid"] = pack.rfid(w, Fp["rfid"])
    n["visits"] = pack.visits(w, Fp["visits"])
    n["gate"] = pack.gate(w, Fp["gate"])
    n["washer"] = pack.washer(w, Fp["washer"])
    n["fills"] = pack.fills(w, Fp["fills"])
    n["repairs"] = pack.repairs(w, Fp["repairs"])
    n["audits"] = pack.audits(w, Fp["audits"])
    n["weather"] = pack.weather(w, Fp["weather"])
    n["packline"] = pack.packline(w, Fp["packline"])
    pack.register(w, Fp["register"])
    pack.stocktake(w, Fp["stocktake"])
    pack.recovery(w, Fp["recovery"])
    pack.plan(w, plans, Fp["plan"])
    pack.cask(w, Fp["cask"])
    pack.erp(w, plans, Fp["erp"])
    docs.standard(Fp["standard"])
    docs.exchange(Fp["exchange"], w)
    docs.quote(Fp["quote"])
    docs.agreement(Fp["agreement"], plans)
    for k, (c, m, who) in OFFICE.items():
        company = "KegTrace Recovery Services Ltd" if k == "recovery" else P.ORG
        postprocess.normalize_ooxml(Fp[k], who, who, c, m, excel=True, company=company)
    postprocess.normalize_docx(Fp["agreement"], P.PEOPLE["sales"], P.PEOPLE["sales"], "2026-10-14T15:20:00Z",
                               "2026-10-16T09:02:00Z", revision=6, total_time=74, seed=4417, company=P.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, plans, n


def truth(w, plans):
    """the 2027 summer at normal weather with the plans, unconstrained (never shipped)"""
    tr = sim.run_2027(w, plans)
    return tr
