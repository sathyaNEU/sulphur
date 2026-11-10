"""task15: the conformed record built straight from the clean world (checks.py compares it with the one verify.py
builds from the shipped pack)."""
import numpy as np
import pandas as pd

import golden as G
import world as W

COLS = ["trial", "plot", "rep", "blk", "range", "col", "entry", "line", "y", "L", "ab"]


def season_water(e):
    """A programme trial's season water: April to October rain plus irrigation, millimetres."""
    return float(np.round(float(np.sum(e["months"])) + sum(mm for _, mm in e["irrigation"]), 1))


def from_world(w):
    tr = w["trials"]
    pl = pd.DataFrame(w["plots"], columns=COLS)
    pl["site"] = pl["trial"].map(lambda t: tr[t]["site"])
    pl["season"] = pl["trial"].map(lambda t: tr[t]["season"])
    pl["stage"] = pl["trial"].map(lambda t: tr[t]["stage"])
    pl["ab"] = pl["ab"].astype(int)
    pl.loc[pl["ab"] == 1, "y"] = np.nan
    pl = pl[["trial", "site", "season", "stage", "line", "rep", "blk", "col", "y", "L", "ab"]]
    water = {t: season_water(w["env"][(d["site"], d["season"])]) for t, d in tr.items() if not d["series"]}
    ser = pd.DataFrame(w["series_cells"])[["trial", "site", "season", "line", "y", "L"]]
    swater = {t: float(d["rain"]) for t, d in w["series_trials"].items()}
    cv = {t: float(d["cv"]) for t, d in w["series_trials"].items()}
    cohort = {l: v["cohort"] for l, v in w["lines"].items()}
    noms = [dict(sow=y, line=d["line"], index=round(d["index"], 1), s3=list(d["s3"]))
            for y, ds in sorted(w["nominations"].items()) for d in ds]
    nominated = {d["line"] for d in noms}
    cands = [l for l in w["stage_sets"][("S3", W.LAST)] if l not in nominated]
    P = G.Panel(pl, water, ser, swater, cv, cohort, W.CHECKS, noms, cands, w["s3_seasons"], W.LAST)
    P.irrigation = {t: float(sum(mm for _, mm in w["env"][(d["site"], d["season"])]["irrigation"]))
                    for t, d in tr.items() if not d["series"]}
    P.standard = float(W.STANDARD)
    P.wi = {l: v["wi"] for l, v in w["lines"].items() if v.get("wi")}
    return P
