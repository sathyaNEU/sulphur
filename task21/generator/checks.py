"""The generator's assertions on the cut pack: the input gates, the results' bands against the hurried routes, every
fork the design note closes, the mess handled the careless way, each factor's footprint outside the units it decides,
the distractors' deletion, and that no shipped file describes the data. Exit 1 on any failure.

    python3 checks.py
"""
import datetime as dt
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from contextlib import redirect_stdout

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import methods as M  # noqa: E402

F = json.load(open(os.path.join(HERE, "figures.json")))
E = json.load(open(os.path.join(HERE, "effort.json")))
META = json.load(open(os.path.join(TASK, "metadata.json")))
OUT = []


def check(tag, ok, detail):
    OUT.append((tag, bool(ok), detail))
    print("%-4s %-8s %s" % ("PASS" if ok else "FAIL", tag, detail))


def quiet(fn, *a, **k):
    with redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def pdf_text(prefix):
    path = M._find(TARGET, prefix)
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                              text=True).stdout)


def rises(D):
    S = {g: G.segment(D, g) for g in M.SEGS}
    return S, M.smallest_change(S["u25"]["lr"]), M.smallest_change(S["mid"]["lr"])


def main():
    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    U25, MID = (F["u25_family_lo"], F["u25_family_hi"]), (F["mid_family_lo"], F["mid_family_hi"])
    LR15 = (F["u25_lr15_lo"], F["u25_lr15_hi"])
    PROP = F["constants"]["proposal_u25"]

    # ---- input gates ------------------------------------------------------------------------------------------
    check("I1", len(files) >= 10, "%d usable files" % len(files))
    cats = {{"csv": "spreadsheet", "xlsx": "spreadsheet", "jsonl": "database", "pdf": "text", "txt": "text"}
            [f.rsplit(".", 1)[1]] for f in files}
    check("I2", len(cats) >= 2, "file categories %s" % sorted(cats))
    rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("I3", max(rows.values()) >= 20000, "largest CSV %d rows" % max(rows.values()))
    check("I4", sorted(rows.values())[-2] >= 600, "a second CSV of %d rows, past 10 printed pages at 60 lines a page"
          % sorted(rows.values())[-2])
    dis = META["distractor_files"]
    check("I5", len(dis) >= 2 and all(d in files for d in dis), "%d distractors shipped, named only in metadata.json"
          % len(dis))
    bad_names = [f for f in files if re.search(r"distract|decoy|unused|readme|dictionar|manifest|schema|field.?notes|"
                                               r"how.?to", f, re.I)]
    check("I6", not bad_names, "no file named for its role or as a description of the data %s" % bad_names)
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += [(f, s) for s in load_workbook(os.path.join(TARGET, f), read_only=True).sheetnames]
    bad_sheets = [x for x in sheets if re.search(r"note|readme|about|scope|dictionar|guide|how to|definition", x[1], re.I)]
    check("I7", not bad_sheets, "no sheet that describes the data %s" % bad_sheets)
    check("I8", all(f in META["files"] and {"source", "date"} <= set(META["files"][f]) for f in files)
          and "license" in META, "metadata.json records every file's source and date and the licence")
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        zn = sorted(os.path.basename(n) for n in z.namelist() if not n.endswith("/"))
    check("I9", zn == files, "target.zip holds exactly the %d target files" % len(files))
    with zipfile.ZipFile(os.path.join(TASK, "golden.zip")) as z:
        gn = sorted(os.path.basename(n) for n in z.namelist() if not n.endswith("/"))
    check("I10", gn == ["pcw_rate_review_2027.xlsx", "pricing_committee_2027_rates.pptx"],
          "golden.zip holds exactly the workbook and the deck")

    # ---- the pack, the golden and its rivals --------------------------------------------------------------------
    GD = quiet(G.compute, TARGET)
    D, S = GD["D"], GD["S"]
    fam = {g: quiet(G.family, D, S, g) for g in ("u25", "mid")}
    sc = {g: quiet(G.shortcuts, D, S, g) for g in ("u25", "mid")}
    fr = {g: [M.smallest_change(f) for f in fam[g].values()] for g in fam}
    sr = {g: {k: M.smallest_change(f) for k, f in sc[g].items()} for g in sc}
    L = PROP / 100.0

    # ---- the bar: each result in its band, each hurried route outside ------------------------------------------
    r1_ok = all([int(GD["r1"][g][0]), int(GD["r1"][g][1]), round(GD["r1"][g][2] * 100, 2)] == F["r1_rows"][g]
                for g in M.SEGS)
    check("R1", r1_ok, "the 2026 table recomputes: %s" % {g: F["r1_rows"][g] for g in M.SEGS})
    held = {"u25": F["u25_2026_sales"] * 12 / 10.0, "o65": F["o65_2026_sales"] * 12 / 10.0}
    check("R2", abs(held["u25"] / F["u25_policies_at_proposal"] - 1) > 0.08
          and abs(held["o65"] / F["o65_policies_at_cut"] - 1) > 0.08,
          "2026 volumes held (%.0f, %.0f) miss the proposals' %d and %d by more than 8 per cent"
          % (held["u25"], held["o65"], F["u25_policies_at_proposal"], F["o65_policies_at_cut"]))
    lr15 = S["u25"]["lr"](L) * 100
    sc15 = {k: f(L) * 100 for k, f in sc["u25"].items()}
    check("R3", LR15[0] <= round(lr15, 1) <= LR15[1] and max(sc15.values()) <= LR15[0] - 1.0,
          "under-25 loss ratio at +%d: golden %.1f in %.1f to %.1f; every hurried route at or under %.1f (margin %.1f)"
          % (PROP, lr15, LR15[0], LR15[1], max(sc15.values()), LR15[0] - max(sc15.values())))
    check("R4", U25[0] <= GD["u25_rise"] <= U25[1] and max(sr["u25"].values()) <= U25[0] - 2,
          "under-25 rise %+d in %+d to %+d; the shortcuts %s, all at least 2 under"
          % (GD["u25_rise"], U25[0], U25[1], sorted(set(sr["u25"].values()))))
    lat, pool, tod = (sr["mid"]["loss-ratio method, latest twelve months"],
                      sr["mid"]["loss-ratio method, 2025 and 2026 pooled"], sr["mid"]["loss-ratio method, 2026 to date"])
    check("R5", MID[0] <= GD["mid_rise"] <= MID[1] and min(lat, pool) >= MID[1] + 3 and tod <= MID[0] - 3,
          "25-to-64 rise %+d in %+d to %+d; latest twelve months %+d and pooled %+d over it, to date %+d under it"
          % (GD["mid_rise"], MID[0], MID[1], lat, pool, tod))
    cut = GD["cut"]
    check("R6", cut["net"] < 0 < cut["nb"] and abs(cut["net"] / 1e6 - F["cut_net_m"]) < 0.005,
          "the over-65 cut: new business %+.2fm, renewals %+.2fm, in all %+.2fm (new business alone on the other side)"
          % (cut["nb"] / 1e6, cut["ren"] / 1e6, cut["net"] / 1e6))
    r7 = next(r for r in E["results"] if r["id"] == "R7")
    care = r7["passes"]["careful"]
    check("R7", abs(care["lo"] - F["mid_range_lo"]) > 1.5 or abs(care["hi"] - F["mid_range_hi"]) > 1.5,
          "the careful pass's range %.1f to %.1f misses %.1f to %.1f by more than 1.5 at an end"
          % (care["lo"], care["hi"], F["mid_range_lo"], F["mid_range_hi"]))
    routes = [r for r in E["routes"] if not r.get("golden")]
    answers = {tuple(r["answer"]) for r in routes}
    check("R8", len(answers) >= 4 and tuple(F["calls"]) not in answers,
          "%d distinct wrong call sets over %d shortcuts" % (len(answers), len(routes)))
    check("R9", sr["u25"]["loss-ratio method, latest twelve months"] == PROP,
          "the pricing team's +%d is the loss-ratio method's own figure on the latest twelve months" % PROP)
    hint = max(len(h["rescues"]) for h in E["hints"])
    check("R10", hint * 3 <= len(E["results"]), "the largest single hint rescues %d of %d" % (hint, len(E["results"])))

    ptxt = open(os.path.join(TASK, "prompt.txt")).read()
    pcts = sorted({int(x) for x in re.findall(r"(\d+) per cent", ptxt)})
    team = [int(x) for x in re.findall(r"team(?:'s)?(?: wants)? (\d+) per cent", ptxt)]
    check("P0", set(pcts) <= {PROP, 3, 75, 80} and team and all(t == PROP for t in team),
          "the prompt's per-cent figures %s are the world's; the team's rise is named %d time(s), each +%d" %
          (pcts, len(team), PROP))

    # ---- the forks the note closes --------------------------------------------------------------------------------
    pln, cmp_ = pdf_text("PLN-2027-03"), pdf_text("CMP-RP-04")
    filed = [("SF1", pln, "each claim capped at £%s" % format(int(M.CAP), ",")),
             ("SF1", pln, "premium net of insurance premium tax"),
             ("SF2", pln, "raising them %s per cent" % F["constants"]["inflation"]),
             ("SF3", pln, "the rates in force on 31 October 2026"),
             ("SF4", pln, "rise %d per cent on 1 January 2027" % F["constants"]["market"]),
             ("SF5", pln, "from 1 February 2026 to 31 October 2026, scaled to twelve months"),
             ("SF6", pln, "the smallest change, in whole per cent"),
             ("SF7", pln, "the age of the main driver"),
             ("SF9", pln, "servicing of £%d a policy" % F["constants"]["servicing"]),
             ("SF10", pln, "first sold through a comparison site who renew in 2027"),
             ("SF11", cmp_, "equivalent new-business price"),
             ("SF12", pln, "drawn policy by policy")]
    for tag, text, phrase in filed:
        check(tag, phrase in text, "filed: \"%s\"" % phrase)
    w = D["feeds"].w
    check("SF8", set(np.unique(w)) <= {1, 50} and (w == 50).sum() > 0,
          "each feed weights its unsold sample (weights %s)" % sorted(set(np.unique(w))))
    cl = [M.smallest_change(f) for k, f in fam["u25"].items() if "/chainladder/" in k]
    check("SF13", min(cl) >= U25[0] and max(cl) <= U25[1], "the triangles' development files under-25 rises %d to %d, "
          "inside the band" % (min(cl), max(cl)))
    l12 = [M.smallest_change(f) for k, f in fam["u25"].items() if k.startswith("latest12")]
    check("SF14", min(l12) >= U25[0] and sr["u25"]["loss-ratio method, 2025 and 2026 pooled"] < U25[0]
          and lat > MID[1], "the base: under-25 latest twelve months with the selection %d to %d inside; all of 2025 "
          "and 2026 on level outside; 25-to-64 latest twelve months outside" % (min(l12), max(l12)))

    # ---- closures ---------------------------------------------------------------------------------------------
    for g, rise in (("u25", GD["u25_rise"]), ("mid", GD["mid_rise"])):
        at, below = S[g]["lr"](rise / 100.0), S[g]["lr"]((rise - 1) / 100.0)
        check("C9", at <= M.TARGET - 0.0003 and below > M.TARGET + 0.0003,
              "%s: %.2f at %+d and %.2f at %+d, both clear of 75" % (g, at * 100, rise, below * 100, rise - 1))
    D2 = dict(D)
    f2 = D["feeds"].sample(frac=1.0, random_state=3).reset_index(drop=True)
    D2["feeds"] = f2
    D2["sales"] = M.sales_frame(f2, D["pol"])
    D2["af"] = M.ae_frame(D["pol"], D["clm_dev"], D["expo"], D["s_cnt"], D2["sales"])
    _, u2, m2 = rises(D2)
    check("C14", (u2, m2) == (GD["u25_rise"], GD["mid_rise"]), "rows shuffled: rises %+d and %+d" % (u2, m2))
    raw = [json.loads(x) for x in open(M._find(TARGET, "covertide"))]
    refs = pd.Series([r["ref"] for r in raw])
    dup = refs[refs.duplicated(keep=False)]
    days = {dt.datetime.fromtimestamp(r["ts"] / 1000, dt.timezone.utc).date() for r in raw if r["ref"] in set(dup)}
    same = len({json.dumps(r, sort_keys=True) for r in raw if r["ref"] in set(dup)}) * 2 == len(dup)
    check("C15", len(dup) > 0 and days <= {dt.date(2026, 5, 14), dt.date(2026, 5, 13)} and same,
          "Covertide: %d rows sent twice, all of 14 May 2026, each pair identical" % (len(dup) // 2))
    med = D["feeds"].groupby("site").gross.median()
    check("C18", 0.7 < med["Brightquote"] / med["Kitecompare"] < 1.4,
          "Brightquote's pence read as pounds: median £%.0f against Kitecompare's £%.0f"
          % (med["Brightquote"], med["Kitecompare"]))
    dvc = D["clm"].copy()
    dvc["capped"] = dvc.incurred_gbp
    alt = M.developed(dvc, D["pattern"])
    alt["dev_cost"] = np.minimum(alt.dev_cost, M.CAP)
    D3 = dict(D)
    D3["clm_dev"] = alt
    S3, u3, m3 = rises(D3)
    check("C13", U25[0] <= u3 <= U25[1] and MID[0] <= m3 <= MID[1],
          "developed before capping: rises %+d and %+d, inside the bands" % (u3, m3))

    # ---- the mess read the careless way, one at a time ----------------------------------------------------------
    full = M.load_feeds(TARGET)

    def with_feeds(f):
        D4 = dict(D)
        D4["feeds"] = f
        D4["sales"] = M.sales_frame(f, D["pol"])
        D4["af"] = M.ae_frame(D["pol"], D["clm_dev"], D["expo"], D["s_cnt"], D4["sales"])
        S4, u4, m4 = rises(D4)
        return S4, u4, m4, f[f.date >= dt.date(2026, 1, 1)].w.sum()

    dups = full[(full.site == "Covertide") & full.ref.isin(set(dup))]
    keep_dups = pd.concat([full, dups], ignore_index=True)
    S4, u4, m4, q4 = with_feeds(keep_dups)
    check("MN1", U25[0] <= u4 <= U25[1] and MID[0] <= m4 <= MID[1] and abs(S4["u25"]["lr"](L) * 100 - lr15) < 1.0,
          "the re-sent day kept: rises %+d and %+d, under-25 at +%d %.1f" % (u4, m4, PROP, S4["u25"]["lr"](L) * 100))
    tests = M.load_feeds(TARGET, drop_tests=False)
    n_zz = int((tests.district == "ZZ99").sum())
    S6, u6, m6, q6 = with_feeds(tests)
    check("MN2", n_zz > 0 and U25[0] <= u6 <= U25[1] and MID[0] <= m6 <= MID[1],
          "the sites' %d monitoring quotes kept: rises %+d and %+d" % (n_zz, u6, m6))
    utc = full.copy()
    pl = pd.read_csv(M._find(TARGET, "pricelark"))
    utc_dates = dict(zip(pl.reference, pd.to_datetime(pl.created_utc, utc=True).dt.date))
    utc.loc[utc.site == "Pricelark", "date"] = utc.loc[utc.site == "Pricelark", "ref"].map(utc_dates).values
    S5, u5, m5, q5 = with_feeds(utc)
    check("MN3", U25[0] <= u5 <= U25[1] and MID[0] <= m5 <= MID[1],
          "Pricelark's UTC times read as local: rises %+d and %+d" % (u5, m5))
    cur_q = full[(full.seg == "u25") & (full.date >= M.CURRENT_FROM)]
    r1q = cur_q[cur_q.pos == 1]
    rows_conv = (r1q.w == 1).sum() / len(r1q)
    check("MN4", rows_conv > 2 * S["u25"]["conv"][1], "the unsold sample read unweighted: under-25 rank-one conversion "
          "%.1f per cent of rows against %.1f of quotes, so R1 and the volumes move (pinned by each feed's weight "
          "column)" % (rows_conv * 100, S["u25"]["conv"][1] * 100))

    # ---- each factor across the data, not only where it decides --------------------------------------------------
    for g in M.SEGS:
        y = S[g]["info"]["y"]
        check("F1", y[0] > y[-1] and S[g]["info"]["slope"] < 0,
              "%s sales: claims per predicted claim %.2f at the deepest decile, %.2f at the shallowest" % (g, y[0], y[-1]))
    for g in M.SEGS:
        m = (D["pol"].seg == g).values
        pol_g = D["pol"][m].reset_index(drop=True)
        cd_g = D["clm_dev"][D["clm_dev"].policy_number.isin(set(pol_g.policy_number))]
        s = M.seasonal_factors(pol_g, cd_g, D["expo"][m], "count")
        check("F2", s[0] > s[5] * 1.15, "%s claims per vehicle-year: January %.2f, June %.2f" % (g, s[0], s[5]))
    af = D["af"]
    for g, want in (("mid", True), ("u25", False)):
        a = af[af.seg == g]
        v6, v7 = a[a.date < G.V7_FROM], a[a.date >= G.V7_FROM]
        ae6, ae7 = v6.cnt.sum() / v6.exp_cnt.sum(), v7.cnt.sum() / v7.exp_cnt.sum()
        check("F3", (ae6 > ae7 * 1.08) if want else (abs(ae6 / ae7 - 1) < 0.08),
              "%s claims per predicted claim, HPM v6 %.3f against v7 %.3f" % (g, ae6, ae7))
    ren = D["ren"]
    capped = ren.renewal_premium_offered_ex_ipt_gbp < ren.intended_renewal_premium_ex_ipt_gbp - 0.005
    by_site = capped.groupby(ren.first_sold_through).mean()
    check("F4", (by_site > 0.05).all(), "renewals capped at the equivalent new-business price on every site: %s"
          % {k: round(v, 2) for k, v in by_site.items()})
    over = (ren.renewal_premium_offered_ex_ipt_gbp > np.minimum(ren.intended_renewal_premium_ex_ipt_gbp,
                                                           ren.enbp_ex_ipt_at_current_nb_rates_gbp) + 0.005).sum()
    check("H6", over == 0, "every renewal offered at the lower of its intended premium and its equivalent "
          "new-business price (%d over)" % over)

    clm_raw = pd.read_csv(M._find(TARGET, "motor_claims_extract"), keep_default_na=False, na_values=[""])
    late = sum(int((pd.to_datetime(clm_raw[c]) > pd.Timestamp(M.AS_AT)).sum())
               for c in ("accident_date", "notified_date", "settled_date"))
    canc_late = int((pd.to_datetime(D["pol"].cancelled_on.astype(str).replace("None", None)) > pd.Timestamp(M.AS_AT)).sum())
    check("H16", late == 0 and canc_late == 0, "no claim or cancellation dated after the extracts' 31 October 2026 "
          "(%d claim dates, %d cancellations)" % (late, canc_late))

    # ---- the distractors decide nothing --------------------------------------------------------------------------
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in dis:
                os.symlink(os.path.join(TARGET, f), os.path.join(tmp, f))
        GD2 = quiet(G.compute, tmp)
        same = (GD2["u25_rise"], GD2["mid_rise"], round(GD2["cut"]["net"]), round(GD2["u25_lr_at_proposal"], 6)) == \
            (GD["u25_rise"], GD["mid_rise"], round(GD["cut"]["net"]), round(GD["u25_lr_at_proposal"], 6))
        check("D1", same, "the %d distractors deleted: every graded figure unchanged" % len(dis))
    finally:
        shutil.rmtree(tmp)

    # ---- positive controls on the documents ------------------------------------------------------------------------
    comm = D["comm"]
    check("P1", len(comm) == 4 and all(30 < v < 80 for v in comm.values()), "commissions read off PCW-COM-2026: %s"
          % comm)
    from pypdf import PdfReader
    pln2 = re.sub(r"\s+", " ", "".join(p.extract_text() or "" for p in PdfReader(M._find(TARGET, "PLN-2027-03")).pages))
    check("H25", all(ph in pln2 for _, t, ph in filed if t is pln), "a second reader (pypdf) finds every filed "
          "sentence of the planning paper that pdftotext finds")
    notes = open(M._find(TARGET, "hpm_model_deployments")).read()
    check("P2", "deployed 2026-02-01" in notes and "aged 25 to 64" in notes,
          "the deployment log dates HPM v7 to the last rate change and names the segment it rebuilt")

    fails = [t for t, ok, _ in OUT if not ok]
    print("checks: %d assertions, %d failures %s" % (len(OUT), len(fails), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
