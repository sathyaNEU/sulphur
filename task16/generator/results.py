"""The golden analysis, the hurried routes, the sound rivals behind every band, and the grading of a route.

Nothing here reads the prompt. Each route is the same analysis code (analysis.py) under named method settings.
"""
import numpy as np

import analysis as AN
import load as LD
import params as P

FAM = P.FAM
GOLD = dict(capture_how="state", written="backlog", transport="propensity", alerts="did")
ROUTES = {   # the hurried analyses, each a complete account that reconciles
    "linked": ("the linked record as it stands, carried into the season unchanged",
               dict(capture_how="none", written="none", transport="asis"), "iid"),
    "careful": ("unkeyed calls restored at the week's capture share and open cases added from the backlog count, the "
                "weeks observed carried into the season unchanged", dict(capture_how="week", written="weekly", transport="asis"), "iid"),
    "no_phone": ("open cases added, calls with no tracking number left out, the season's conversations weighted properly",
                 dict(capture_how="none", written="backlog"), "day"),
    "no_written": ("unkeyed calls restored, the resolved-case export taken as the written channel",
                   dict(capture_how="state", written="none"), "day"),
    "stationary": ("open cases completed on the closing times of the summer", dict(capture_how="state", written="stationary"), "day"),
    "parcel_mix": ("each family's rates by delivery outcome weighted by the plan's parcel service levels",
                   dict(transport="parcel"), "iid"),
    "no_alerts": ("the season's conversations weighted by each outcome's contact rate, the delay alerts left out",
                  dict(alerts="none"), "day"),
    "asis": ("every follow-up restored, the weeks observed carried into the season unchanged", dict(transport="asis"), "day"),
}
RIVALS = [   # sound variants of the golden: each must land inside every band
    ("capture by queue and week", dict(capture_how="week")), ("capture by queue and day", dict(capture_how="day")),
    ("capture by queue and hour", dict(capture_how="hour")), ("capture by queue and wait", dict(capture_how="wait")),
    ("one capture share", dict(capture_how="pooled")),
    ("open cases by queue and day raised", dict(written="daily")), ("open cases by queue and week raised", dict(written="weekly")),
    ("alerts read class by class", dict(alerts="byclass")), ("alerts read against version 3 weeks only", dict(pre0=P.V3_DAY)),
]
# bands: what every sound variant shares, checked in checks.py (rivals inside, hurried routes outside where priced)
BAND = {
    "conversations": 0.005,         # relative
    "linked_rate": 0.4, "achieved_all": 0.8, "expected_all": 0.9,
    "phone_unkeyed_share": (36.0, 46.0), "written_open": 0.20, "alert_effect": (35.0, 48.0),
    "late_share": 3.0, "per_week": 0.07,
    "expected": {"TRK": 1.4, "DLV": 1.2, "RDR": 1.6, "RDL": 2.4, "PUP": 1.2, "CUS": 1.4, "DMG": 1.8, "LST": 2.6, "RET": 1.0, "PAY": 1.6},
    "half_ratio": (0.65, 1.6),
}


def analyse(target, B=1000):
    D = LD.load(target)
    S = AN.setup(D)
    out = {"D": D, "S": S}
    G = AN.run(S, D, **GOLD)
    G["boot"] = AN.bootstrap(S, D, G, B=B, unit="day")
    G["tick"] = AN.tag_check(S, D)
    G["diag"] = AN.diagnostics(S, D, AN.weights(S, GOLD["capture_how"], GOLD["written"])[0])
    out["boot_plain"] = AN.bootstrap(S, D, G, B=B, unit="day", seed=23)
    G["recon"] = AN.reconcile(S, D)
    out["golden"] = G
    for name, (_, opts, unit) in ROUTES.items():
        kw = dict(GOLD); kw.update(opts)
        R = AN.run(S, D, **kw)
        R["boot"] = AN.bootstrap(S, D, R, B=B, unit=unit, transport=kw["transport"], alerts=kw["alerts"])
        out[name] = R
    out["rivals"] = []
    for name, opts in RIVALS:
        kw = dict(GOLD); kw.update(opts)
        out["rivals"].append((name, AN.run(S, D, **kw)))
    # the range under other sound resamplings: another seed, and the weights' own error left in
    out["boot_rivals"] = [("another draw", AN.bootstrap(S, D, G, B=B, unit="day", seed=11))]
    return out


def call(R):
    keep = [f for f, x in zip(FAM, R["expected"]) if round(float(x), 1) >= P.LINE]
    return {"keep": keep, "hand_back": [f for f in FAM if f not in keep]}


def figures(R):
    """A route's graded figures, rounded as the answer blocks state them."""
    b = R["boot"]
    f = {
        "conversations": int(R["conversations"]), "linked_rate": round(float(R["linked_rate"]), 1),
        "phone_keyed": int(R["phone_keyed"]), "phone_total": int(round(R["phone_total"])),
        "phone_unkeyed_share": round(float(R["phone_unkeyed_share"]), 1), "written_closed": int(R["written_closed"]),
        "written_open": int(round(R["written_open"])), "achieved_all": round(float(R["achieved_all"]), 1),
        "achieved": {k: round(float(x), 1) for k, x in zip(FAM, R["achieved"])},
        "expected": {k: round(float(x), 1) for k, x in zip(FAM, R["expected"])},
        "expected_all": round(float(R["expected_all"]), 1),
        "low": {k: round(float(x), 1) for k, x in zip(FAM, b["low"])}, "high": {k: round(float(x), 1) for k, x in zip(FAM, b["high"])},
        "half": {k: round(float(x), 2) for k, x in zip(FAM, b["half"])},
        "low_all": round(b["low_all"], 1), "high_all": round(b["high_all"], 1), "half_all": round(b["half_all"], 2),
        "call": call(R),
    }
    if R.get("M") is not None:
        e = R["e"]
        f["alert_effect"] = round(100 * float(e), 0) if not isinstance(e, dict) else round(100 * float(np.mean(list(e.values()))), 0)
        f["late_share"] = round(float(R["late_share"]), 1); f["per_week"] = int(round(R["per_week"], -2))
        f["obs_late_share"] = round(float(R["obs_late_share"]), 1); f["obs_per_week"] = int(round(R["obs_per_week"], -1))
    else:
        f["alert_effect"] = None; f["late_share"] = None; f["per_week"] = None
    return f


KEYS = ["linked", "phone", "written", "achieved", "alerts", "season", "expected", "range", "call"]
NAMES = {"linked": "the linked record", "phone": "telephone follow-ups with no tracking number", "written": "written follow-ups still open",
         "achieved": "the resolution rate achieved under version 3", "alerts": "the delay alerts' effect",
         "season": "the season's conversations", "expected": "each family's expected rate", "range": "the 90 per cent range",
         "call": "the families kept and handed back"}


def grade(f, g, key):
    """right, partly or missed for one result of a route (f) against the golden (g)."""
    def near(a, b, tol):
        return a is not None and abs(a - b) <= tol
    if key == "linked":
        ok = abs(f["conversations"] - g["conversations"]) <= BAND["conversations"] * g["conversations"] and near(f["linked_rate"], g["linked_rate"], BAND["linked_rate"])
        return "right" if ok else "missed"
    if key == "phone":
        lo, hi = BAND["phone_unkeyed_share"]
        return "right" if lo <= f["phone_unkeyed_share"] <= hi else "missed"
    if key == "written":
        return "right" if abs(f["written_open"] - g["written_open"]) <= BAND["written_open"] * g["written_open"] else "missed"
    if key == "achieved":
        return "right" if near(f["achieved_all"], g["achieved_all"], BAND["achieved_all"]) else "missed"
    if key == "alerts":
        lo, hi = BAND["alert_effect"]
        return "right" if f["alert_effect"] is not None and lo <= f["alert_effect"] <= hi else "missed"
    if key == "season":
        ok = near(f["late_share"], g["late_share"], BAND["late_share"]) and f["per_week"] is not None and abs(f["per_week"] - g["per_week"]) <= BAND["per_week"] * g["per_week"]
        return "right" if ok else "missed"
    if key == "expected":
        n = sum(near(f["expected"][k], g["expected"][k], BAND["expected"][k]) for k in FAM) + near(f["expected_all"], g["expected_all"], BAND["expected_all"])
        return "right" if n >= 10 else "partly" if n >= 6 else "missed"
    if key == "range":
        lo, hi = BAND["half_ratio"]
        n = sum(lo <= f["half"][k] / g["half"][k] <= hi for k in FAM) + (lo <= f["half_all"] / g["half_all"] <= hi)
        return "right" if n >= 10 else "partly" if n >= 6 else "missed"
    return "right" if f["call"]["keep"] == g["call"]["keep"] else "missed"
