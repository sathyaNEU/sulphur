"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the documents (docs.py), the site
manager's draft read off the shipped files, every office container laid out as Office saves it (the house writers),
each file's own save time."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import analysis as A  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
FI_W = dt.timezone(dt.timedelta(hours=2))
FI_S = dt.timezone(dt.timedelta(hours=3))
OFFICE = {"budget27": ("2026-10-08T07:12:00Z", "2026-10-15T10:31:00Z", P.PEOPLE["planning"], P.CLIENT),
          "item_master": ("2026-11-02T04:57:00Z", "2026-11-02T04:58:00Z", P.PEOPLE["slotting"], P.ORG),
          "slotting": ("2026-10-27T12:40:00Z", "2026-10-30T13:26:00Z", P.PEOPLE["slotting"], P.ORG),
          "roster": ("2026-10-28T08:05:00Z", "2026-10-28T08:44:00Z", P.PEOPLE["hr"], P.ORG),
          "draft": ("2026-10-29T13:18:00Z", "2026-11-02T14:51:00Z", P.PEOPLE["site"], P.ORG)}
EXPORTED = {"zone_hours": dt.datetime(2026, 11, 2, 7, 14, 26, tzinfo=FI_W),
            "pay_old": dt.datetime(2024, 1, 15, 9, 31, 12, tzinfo=FI_W),
            "pay_new": dt.datetime(2026, 11, 3, 10, 2, 47, tzinfo=FI_W),
            "archive": dt.datetime(2026, 11, 2, 15, 48, 3, tzinfo=FI_W),
            "k_orders": dt.datetime(2026, 11, 2, 7, 21, 55, tzinfo=FI_W),
            "h_daily": dt.datetime(2026, 11, 1, 9, 12, 40, tzinfo=FI_W),
            "h_monthly": dt.datetime(2026, 11, 1, 9, 15, 2, tzinfo=FI_W),
            "pilot": dt.datetime(2026, 11, 2, 8, 3, 19, tzinfo=FI_W),
            "benches": dt.datetime(2026, 11, 2, 11, 20, 45, tzinfo=FI_W),
            "returns": dt.datetime(2026, 11, 3, 13, 5, 30, tzinfo=FI_W)}


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    n = pack.write_tables(w, target)
    docs.standard(F["standard"])
    docs.agreement(F["agreement"])
    f = A.load(target)
    d = pack.draft(w, f, F["draft"])
    tp = A.pilot_times(f)
    z = A.zone_hours(f)
    import pandas as pd
    zp = z[(z["zone"] == "P2") & (z["date"] >= pd.Timestamp(P.PILOT[0])) & (z["date"] <= pd.Timestamp(P.PILOT[1]))]
    p2 = float((zp["task_min"].sum() - tp * zp["lines_hui"].sum()) / zp["kot"].sum())
    days = zp[zp["lines_hui"] > 0]["date"].nunique()
    docs.review(F["review"], {"articles": len(w["pilot"]), "lines": int(zp["lines_hui"].sum()),
                              "per_day": int(round(zp["lines_hui"].sum() / days)), "pilot_t": tp, "p2_t": p2})
    for k, (c, m, who, comp) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, c, m, excel=True, company=comp)
    postprocess.normalize_docx(F["review"], P.PEOPLE["ci"], P.PEOPLE["ci"], "2026-11-02T12:48:00Z", "2026-11-03T08:16:00Z",
                               revision=4, total_time=63, seed="task4-review", company=P.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, n
