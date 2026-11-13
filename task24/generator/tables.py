"""The clean tables the vendor's systems hold (before any export mess): task passes, QA reviews, worker-weeks with
pay, the video archive's tracks, and the requests' sample labels. world.simulate() makes the events; this module
settles pay exactly as the 2026 pay policy does (piece pay on first submissions, the hourly floor per worker-week)."""
import numpy as np
import pandas as pd

import world as Wd

COUNT_COLS = ["n_S_clr", "n_S_occ", "n_M_clr", "n_M_occ", "n_L_clr", "n_L_occ"]


def build(W=None):
    W = W or Wd.simulate()
    proj = W["proj"].set_index("project")
    rows = []
    for k, d in enumerate(W["passes"]):
        row = dict(pass_key=k, item=d["item"], project=d["project"], kind=d["kind"], pass_no=d["pass_no"],
                   annotator_id=d["annotator_id"], week=d["week"], active_seconds=d["sec"], nobj=d["nobj"])
        c = d.get("counts")
        if c:
            for col in COUNT_COLS + ["n_poly", "n_poly_occ", "vertices"]:
                if col in c:
                    row[col] = c[col]
        if d["kind"] == "video":
            row["chunk_key"] = d["chunk_key"]
        rows.append(row)
    P = pd.DataFrame(rows)
    R = pd.DataFrame(W["reviews"])
    R["pass_key"] = range(len(R))          # reviews were appended in the same order as passes
    WK = pd.DataFrame(W["weeks"])
    ann = W["ann"].set_index("annotator_id")
    # piece pay: first submissions only (corrections are unpaid), credited in the week of submission
    first = P[P.pass_no == 1].copy()
    vch = W["vchunks"]
    first["units_box"] = np.where(first.kind == "box", first.nobj, 0)
    first["units_poly"] = np.where(first.kind == "polygon", first.nobj, 0)
    first["units_track"] = np.where(first.kind == "video", first.nobj, 0)
    first["units_frame"] = np.where(first.kind == "video",
                                    vch.frames.reindex(first.chunk_key.fillna(0).astype(int)).to_numpy(), 0)
    first["piece"] = (first.units_box * Wd.RATES["box"] + first.units_poly * Wd.RATES["polygon"] +
                      first.units_track * Wd.RATES["track"] + first.units_frame * Wd.RATES["frame"])
    pay = first.groupby(["annotator_id", "week"])[["units_box", "units_poly", "units_track", "units_frame", "piece"]].sum()
    WK = WK.merge(pay, left_on=["annotator_id", "week"], right_index=True, how="left").fillna(
        {c: 0 for c in ["units_box", "units_poly", "units_track", "units_frame", "piece"]})
    WK["floor"] = WK.centre.map({c: v["floor"] for c, v in Wd.CENTRES.items()})
    WK["topup"] = np.maximum(0.0, WK.floor * WK.paid_hours - WK.piece)
    return dict(P=P, R=R, WK=WK, ann=W["ann"], rev=W["rev"], proj=W["proj"], vtracks=W["vtracks"], vchunks=vch)
