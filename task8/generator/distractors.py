"""task8: the trust's other Year 7 files that sit beside the entry reading data and decide nothing here: the
cognitive profile tests some academies run, autumn attendance, the settling-in survey and last year's Reading
Forward session log."""
import datetime as dt

import numpy as np

import params as P


def cognitive(W, rng):
    rows = []
    run = {a["name"] for a in W["academies"][::2]}
    for s in W["students"]:
        if s["left"] or s["academy"] not in run or rng.random() < 0.06:
            continue
        base = 100 + 15 * (0.55 * s["theta"] + rng.normal(0, 0.8))
        v = int(np.clip(round(base + rng.normal(0, 5)), 69, 141))
        q = int(np.clip(round(100 + 15 * (0.35 * s["theta"] + rng.normal(0, 0.9))), 69, 141))
        nv = int(np.clip(round(100 + 15 * (0.25 * s["theta"] + rng.normal(0, 0.95))), 69, 141))
        sp = int(np.clip(round(100 + 15 * (0.2 * s["theta"] + rng.normal(0, 0.97))), 69, 141))
        rows.append([s["upn"], s["academy"], "2026-%02d-%02d" % (9, int(rng.integers(15, 30))), v, q, nv, sp,
                     round((v + q + nv + sp) / 4, 1)])
    return ["upn", "academy", "test_date", "verbal_sas", "quantitative_sas", "non_verbal_sas", "spatial_sas",
            "mean_sas"], rows


def attendance(W, rng):
    rows = []
    weeks = [dt.date(2026, 9, 7) + dt.timedelta(days=7 * k) for k in range(5)]
    for s in W["students"]:
        if s["left"]:
            continue
        base = np.clip(0.955 + 0.02 * s["theta"] - 0.03 * s["fsm"] + rng.normal(0, 0.03), 0.6, 1.0)
        for w in weeks:
            poss = 10
            att = int(np.clip(round(poss * (base + rng.normal(0, 0.05))), 0, poss))
            rows.append([s["upn"], s["academy"], w.isoformat(), poss, att])
    return ["upn", "academy", "week_beginning", "possible_sessions", "attended_sessions"], rows


def survey(W, rng):
    rows = []
    q = ["I have made friends in my form", "I know who to ask for help", "I enjoy reading for pleasure",
         "I find my lessons too hard", "I feel safe at school"]
    k = 0
    for s in W["students"]:
        if s["left"] or rng.random() < 0.38:
            continue
        k += 1
        ans = [int(np.clip(round(3.6 + rng.normal(0, 0.9)), 1, 5)),
               int(np.clip(round(3.9 + rng.normal(0, 0.8)), 1, 5)),
               int(np.clip(round(3.0 + 0.35 * s["theta"] + rng.normal(0, 1.0)), 1, 5)),
               int(np.clip(round(2.4 - 0.3 * s["theta"] + rng.normal(0, 1.0)), 1, 5)),
               int(np.clip(round(4.1 + rng.normal(0, 0.8)), 1, 5))]
        rows.append(["R%05d" % (10000 + k), s["academy"], "2026-09-%02d" % int(rng.integers(21, 30))] + ans)
    return ["response_id", "academy", "submitted"] + q, rows


def sessions(W, rng):
    rows = []
    for a in W["academies"]:
        groups = max(1, int(a["n"] * 0.16 / 6))
        d = dt.date(2025, 9, 22)
        while d < dt.date(2026, 7, 17):
            if d.weekday() < 5 and not (dt.date(2025, 12, 20) <= d <= dt.date(2026, 1, 5)) and \
                    not (dt.date(2026, 3, 28) <= d <= dt.date(2026, 4, 12)):
                for g in range(groups):
                    if rng.random() < 0.58:
                        size = int(np.clip(rng.normal(5.2, 0.9), 2, 6))
                        rows.append([a["name"], d.isoformat(), "G%02d" % (g + 1), size, 40,
                                     round(40 / 60 + rng.normal(0, 0.05), 2)])
            d += dt.timedelta(days=1)
    return ["academy", "session_date", "group", "students_present", "minutes", "tutor_hours"], rows
