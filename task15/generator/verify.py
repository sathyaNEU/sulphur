"""task15: the independent verifier. It reads only the pack under target/, conforms it on its own loaders (the two
harvest layouts, the weighings, the entry lists and the line register, season water from the rain and irrigation
files, the series' published results) and hands the conformed record to golden.py; checks.py asserts that the
figures it yields are the ones the clean world gives."""
import csv
import os
import re
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402

STAGE = {"Stage 1": "S1", "Stage 2": "S2", "Stage 3": "S3"}
CHECKS = ["Byaduk", "Wando", "Carapook", "Nareen"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheet(path, name):
    ws = load_workbook(path, read_only=True, data_only=True)[name]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it if r and r[0] is not None]


def find(target, prefix, ext):
    """The one file in the pack whose name starts with prefix and ends with ext (the names carry their seasons)."""
    hits = sorted(f for f in os.listdir(target) if f.startswith(prefix) and f.endswith(ext))
    if len(hits) != 1:
        raise SystemExit("expected one %s*%s in %s, found %s" % (prefix, ext, target, hits))
    return os.path.join(target, hits[0])


def norm(code):
    """A line as written on an entry list, a register or a results file: no spaces, upper case."""
    return re.sub(r"\s+", "", str(code)).upper()


def documents(target):
    """The text of every document in the pack, read back through its own format."""
    from docx import Document
    from pypdf import PdfReader
    out = {}
    for name in sorted(os.listdir(target)):
        path = os.path.join(target, name)
        if name.endswith(".pdf"):
            out[name] = re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages))
        elif name.endswith(".docx"):
            out[name] = re.sub(r"\s+", " ", " ".join(p.text for p in Document(path).paragraphs))
    return out


def load(target, keep="last", field_weights=False):
    reg = sheet(find(target, "line_register", ".xlsx"), "Lines")
    wi2cross = {norm(r["WI number"]): norm(r["Cross code"]) for r in reg if r["WI number"]}
    cohort = {norm(r["Cross code"]): int(r["First trial season"]) for r in reg}
    check_names = {norm(c): c for c in CHECKS}

    def line_id(label):
        k = norm(label)
        if k in check_names:
            return check_names[k]
        return wi2cross.get(k, k)

    trials = {r["trial_code"]: r for r in rows(find(target, "trials_", ".csv"))}
    entry = {(r["trial_code"], int(r["entry_no"])): line_id(r["line"])
             for r in rows(find(target, "trial_entry_lists_", ".csv"))}

    recs = []
    for r in rows(find(target, "PlotHarvest_", ".csv")):
        if r["Trial"] == "Trial":           # the old logger repeats its header at every trial
            continue
        ab = r["Harvested"].strip().upper() != "Y"
        yv = float("nan") if ab else float(r["Yld_kgha_12.5"]) / 1000.0
        if field_weights and not ab:           # the weight off the plot, moisture ignored (a mishandling, for checks)
            yv = float(r["GrainWt_kg"]) / (float(r["PlotLen_m"]) * float(trials[r["Trial"]]["plot_width_m"])) * 10.0
        recs.append((r["Trial"], int(r["Plot"]), int(r["Rep"]), int(r["Blk"]), int(r["Row"]), int(r["Entry"]),
                     yv, float(r["Lodging_pct"]) / 10.0, int(ab), 1))
    for r in rows(find(target, "plot_harvest_", ".csv")):
        ab = r["plot_status"].strip().lower() != "harvested"
        yv = float("nan") if ab else float(r["yield_t_ha"])
        if field_weights and not ab:
            yv = float(r["grain_kg"]) / float(r["plot_area_m2"]) * 10.0
        recs.append((r["trial_code"], int(r["plot_no"]), int(r["replicate"]), int(r["block"]), int(r["row"]),
                     int(r["entry_no"]), yv, float(r["lodging_pct"]) / 10.0, int(ab), int(r["weigh_seq"])))
    pl = pd.DataFrame(recs, columns=["trial", "plot", "rep", "blk", "col", "entry", "y", "L", "ab", "seq"])
    pl = pl.sort_values(["trial", "plot", "seq"])
    pl = pl.drop_duplicates(["trial", "plot"], keep=keep)      # a plot weighed twice: the later weighing stands
    pl["line"] = [entry[(t, e)] for t, e in zip(pl["trial"], pl["entry"])]
    pl["site"] = pl["trial"].map(lambda t: trials[t]["site"])
    pl["season"] = pl["trial"].map(lambda t: int(trials[t]["season"]))
    pl["stage"] = pl["trial"].map(lambda t: STAGE[trials[t]["stage"]])
    pl = pl[["trial", "site", "season", "stage", "line", "rep", "blk", "col", "y", "L", "ab", "plot"]]

    rain = {}
    for r in rows(find(target, "site_rainfall_monthly_", ".csv")):
        if 4 <= int(r["month"]) <= 10 and r["rain_mm"] != "":
            k = (r["site"], int(r["year"]))
            rain[k] = rain.get(k, 0.0) + float(r["rain_mm"])
    irr = {}
    for r in rows(find(target, "kerang_irrigation_", ".csv")):
        k = ("Kerang", int(r["date"][:4]))
        rain[k] = rain.get(k, 0.0) + float(r["applied_mm"])
        irr[k] = irr.get(k, 0.0) + float(r["applied_mm"])
    water = {t: round(rain[(d["site"], int(d["season"]))], 1) for t, d in trials.items()}

    def tcode(season, site):
        return "HRBS%02d-%s" % (int(season) % 100, site[:3].upper())

    srecs = []
    for r in rows(find(target, "HRBS_site_results_", ".csv")):
        srecs.append((tcode(r["season"], r["site"]), r["site"], int(r["season"]), line_id(r["entry"]),
                      float(r["grain_yield_t_ha"]), float(r["lodging_pct"]) / 10.0))
    ser = pd.DataFrame(srecs, columns=["trial", "site", "season", "line", "y", "L"])
    swater, scv = {}, {}
    for r in rows(find(target, "HRBS_site_seasons_", ".csv")):
        if r["status"] != "harvested":
            continue
        swater[tcode(r["season"], r["site"])] = float(r["apr_oct_rain_mm"])
        scv[tcode(r["season"], r["site"])] = float(r["cv_pct"])

    s3 = {}
    for (t, e), l in entry.items():
        if STAGE[trials[t]["stage"]] == "S3" and l not in CHECKS:
            s3.setdefault(l, set()).add(int(trials[t]["season"]))
    s3 = {l: sorted(v) for l, v in s3.items()}
    noms = []
    for r in sheet(find(target, "hrbs_nominations_", ".xlsx"), "HRBS nominations"):
        l = line_id(r["WI number"])
        noms.append(dict(sow=int(r["Sowing year"]), line=l, index=float(r["High-rainfall index (% of Byaduk)"]),
                         s3=[int(x) for x in str(r["Stage 3 seasons"]).split(",")]))
    last = max(int(d["season"]) for d in trials.values())
    nominated = {n["line"] for n in noms}
    order = sorted((e for (t, e) in entry if trials[t]["season"] == str(last) and STAGE[trials[t]["stage"]] == "S3"
                    and t.endswith("HOR")))
    hor = [t for t in trials if trials[t]["season"] == str(last) and STAGE[trials[t]["stage"]] == "S3"
           and trials[t]["site"] == "Horsham"][0]
    cands = [entry[(hor, e)] for e in order if entry[(hor, e)] not in CHECKS and entry[(hor, e)] not in nominated]
    P = G.Panel(pl, water, ser, swater, scv, cohort, CHECKS, noms, cands, s3, last)
    P.irrigation = {t: irr.get((d["site"], int(d["season"])), 0.0) for t, d in trials.items()}
    P.wi = {v: k for k, v in wi2cross.items()}
    deed = documents(target)[os.path.basename(find(target, "option_deed_schedule_2", ".pdf"))]
    m = re.search(r"first two seasons is (\d+(?:\.\d+)?) or more", deed)
    P.standard = float(m.group(1))             # the uptake standard, read from the deed
    return P


SENTENCES = {
    "HRBS_trial_protocol_": [
        "relative yield over a set of trials is its mean grain yield over those trials as a percentage of Byaduk",
        "Every plot is harvested, lodged plots included",
        "sown in every trial of that season and of the next"],
    "option_deed_schedule_2": [
        "over the Series trials of the line's first two seasons is", "A line is nominated once",
        "the index quoted for a line less the relative yield to be expected of the line at the trials the index was "
        "taken from",
        "less that to be expected of it at the Series trials of its two seasons, apart from head (c)",
        "the relative yield the line lost to lodging beyond what Byaduk lost at those Series trials, less the same at "
        "the trials the index was taken from, on the lodging recorded",
        "the relative yield to be expected of the line at those Series trials less the relative yield it returned"],
    "BGG_trial_handbook_": [
        "of the line's mean yield over its harvested plots in the trial as a percentage of Byaduk's in the same trial",
        "the later weighing stands", "it is recorded as not harvested and has no weight",
        "Every watering is entered in the irrigation log with the depth applied"],
}


def main(argv):
    """Recompute every figure the answer blocks state, from the pack alone, and set it against figures.json."""
    import json
    import figs as FG
    target = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    bad = 0
    docs = documents(target)
    for prefix, sents in SENTENCES.items():
        name = os.path.basename(find(target, prefix, ".pdf"))
        for st in sents:
            ok = st in docs.get(name, "")
            bad += not ok
            print("%s  %s: %s" % ("PASS" if ok else "FAIL", name, st[:70]))
    P = load(target)
    R = G.analyse(P, sims=FG.SIMS)
    sm = FG.summary(R, P)
    print("plots %d, lines %d, completed nominations %d" % (len(P.plots), P.plots["line"].nunique(), R["n_completed"]))
    fj = os.path.join(HERE, "figures.json")
    if not os.path.exists(fj):
        print("no figures.json beside the verifier yet")
        return 1 if bad else 0
    F = json.load(open(fj))
    pairs = [("nominate", sorted(sm["picks"]), sorted(F["nominate"])),
             ("first left out", sm["next"], F["first_left_out"]),
             ("quoted", sm["quoted"], F["quoted_mean"]), ("returned", sm["realised"], F["realised_mean"]),
             ("gap", sm["shortfall"], F["shortfall_points"]),
             ("own trials", sm["own"], F["overstated_at_own_sites_points"]),
             ("benchmark's gain", sm["water"], F["benchmark_water_response_points"]),
             ("lodging", sm["lodging_part"], F["lodging_points"]), ("left", sm["left"], F["left_over_points"]),
             ("past error", sm["rmse"], F["backtest_rmse_points"]),
             ("cut between the last line in and the first out", sm["margin"], F["cut_points"]),
             ("expected relative yields", sm["ry"], {k: v["expected_ry"] for k, v in F["lines"].items()}),
             ("range lows", sm["lo"], {k: v["low"] for k, v in F["lines"].items()}),
             ("range highs", sm["hi"], {k: v["high"] for k, v in F["lines"].items()}),
             ("expected lodging", sm["lodging"], {k: v["lodging_pct"] for k, v in F["lines"].items()})]
    for name, mine, theirs in pairs:
        ok = mine == theirs
        bad += not ok
        print("%s  %s: %s" % ("PASS" if ok else "FAIL", name, mine if not isinstance(mine, dict) else
                              "%d lines" % len(mine)))
    print("%s  verify: %d mismatches" % ("PASS" if not bad else "FAIL", bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
