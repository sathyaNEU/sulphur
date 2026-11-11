"""task9 (architecture 10): the build. The pack under target/ (the FRED and Cboe series as published, cut at the record's
last day; the desk's, the platform's and the pricing service's records written by pack.py and docs.py from the simulated
market), the golden deliverables, both zips, figures.json, effort.json, submission.md and metadata.json.

    python3 build.py                 # builds into a scratch folder, then installs into the task folder
    python3 build.py --out <folder>  # builds into <folder> only (two such builds are byte-identical)
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import effort_passes as EP  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import market as MK  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402

AS_OF = "2026-11-11"
SERIES = {
    "DGS1": "1-year Treasury constant-maturity yield, daily", "DGS2": "2-year Treasury constant-maturity yield, daily",
    "DGS3": "3-year Treasury constant-maturity yield, daily", "DGS5": "5-year Treasury constant-maturity yield, daily",
    "DGS7": "7-year Treasury constant-maturity yield, daily", "DGS10": "10-year Treasury constant-maturity yield, daily",
    "DGS20": "20-year Treasury constant-maturity yield, daily", "DGS30": "30-year Treasury constant-maturity yield, daily",
    "DBAA": "Moody's seasoned Baa corporate bond yield, daily", "DAAA": "Moody's seasoned Aaa corporate bond yield, daily",
    "SOFR": "Secured Overnight Financing Rate, daily",
}
COVERS = {k + ".csv": v + ", as FRED publishes it" for k, v in SERIES.items()}
COVERS.update({"SPX_History.csv": "S&P 500 index daily closing levels, as Cboe publishes them",
               "VIX_History.csv": "Cboe Volatility Index daily open, high, low and close"})
COVERS.update({
    PK.F["rfq1"]: "Tidewell's audit of the requests for quote the desk received, 3 January 2023 to 4 April 2025 (first export generation)",
    PK.F["rfq2"]: "the same audit from 7 April 2025 to 6 November 2026 (second export generation)",
    PK.F["blotter"]: "the desk's trades: client trades on Tidewell and trades with other dealers",
    PK.F["tape"]: "the public trade tape for the bonds the desk quotes, with dissemination times, capped sizes, cancels and corrections",
    PK.F["eval"]: "Ashcote's daily evaluated bid, mid and ask for each bond",
    PK.F["master"]: "the security master: issuer, sector, coupon, maturity, size, 144A status and registered successor",
    PK.F["buckets"]: "the security master's liquidity bucket for each bond and quarter",
    PK.F["ratings"]: "issuer ratings and the dates they changed",
    PK.F["clients"]: "the Tidewell client list: each client code's type and onboarding date",
    PK.F["schedule"]: "the auto-quoter's schedule, versions 1 to 3, with its multiples and formula",
    PK.F["draft"]: "the draft 2027 schedule",
    PK.F["summaries"]: "the desk's month-end summaries by segment, January 2023 to October 2026",
    PK.F["league"]: "Tidewell's monthly dealer league tables for 2026",
    PK.F["policy"]: "the desk's electronic quoting policy (2026 edition)",
})
CATEGORY = {"csv": "spreadsheet", "xlsx": "spreadsheet", "pdf": "text"}


def metadata(tgt, info):
    man = MK.manifest()
    raw = {f["file"]: f for f in man["files"]}
    files = []
    for name in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, name)
        e = {"path": name, "format": name.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "covers": COVERS[name]}
        if name in raw:
            e.update(made="downloaded and shipped as published, cut at 6 November 2026 (the record's last day)", url=raw[name]["url"],
                     pulled=raw[name]["pulled"], rows=info["market_rows"][name])
        else:
            e.update(made="written by task9/generator (pack.py, docs.py) from the simulated market on the published series (deterministic)")
        files.append(e)
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Brindlemoor Securities' credit desk: the 2027 P&L to plan on the draft quoting schedule, with its range, and the "
                 "changes that lose money",
        "domain": "Quantitative Finance and Trading, Quantitative Finance",
        "task_type": "strategy backtesting and evaluation (a dealer's auto-quoting schedule backtested on its request-for-quote history)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": AS_OF,
        "deliverables": [GD.BOOK, GD.NOTE],
        "distractor_files": PK.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_file": PK.F["tape"], "largest_file_rows": info["tape_rows"],
                        "long_file": PK.F["rfq2"], "long_file_rows": info["rfq_rows"][1]},
        "sources": [
            {"files": "the 11 FRED series (DGS1 to DGS30, DBAA, DAAA, SOFR)", "origin": "Federal Reserve Bank of St. Louis, FRED; each "
             "series as its graph download serves it.", "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series>",
             "date": man["pulled"], "license": "Public domain or reproducible with attribution as FRED's terms state for each source "
             "series (Board of Governors, Moody's via FRED, Federal Reserve Bank of New York); values reproduced unaltered with the "
             "source and pull date recorded."},
            {"files": "SPX_History.csv, VIX_History.csv", "origin": "Cboe Global Markets daily price history downloads.",
             "url": "https://cdn.cboe.com/api/global/us_indices/daily_prices/", "date": man["pulled"],
             "license": "Published by Cboe for public download; values reproduced unaltered with the source and pull date recorded."},
            {"files": "every other file", "origin": "written for this task. Brindlemoor Securities, Tidewell Credit Network, Ashcote "
             "Evaluations, the issuers, bonds, clients, dealers and paperwork are invented; every bond's value is the published "
             "Treasury curve and Moody's spreads plus its issuer's own simulated information, and every request, quote and trade is "
             "simulated from the request-for-quote process on them.", "date": AS_OF, "license": "CC BY 4.0 (original work)"},
        ],
        "files": files,
    }


def run(out, sims=FG.SIMS):
    tgt, gold = os.path.join(out, "target"), os.path.join(out, "golden")
    for d in (tgt, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    MK.check_raw()
    W = WD.World(MK.Market(), seed=P.SEED)
    info, _ = PK.write(W, tgt)
    F = FG.compute(tgt, sims=sims)
    E = EP.build(F)
    GD.write_all(F, gold)
    PP.own_mtimes(gold, {})
    PP.zip_folder(tgt, os.path.join(out, "target.zip"), zone=P.ZONE)
    PP.zip_folder(gold, os.path.join(out, "golden.zip"), zone=P.ZONE)
    sub = WU.build(F)
    F["stated"] = sorted(set(WU.STATED))          # every figure the answer blocks state, as they state it
    FG.write(F, os.path.join(out, "figures.json"))
    json.dump(E, open(os.path.join(out, "effort.json"), "w"), indent=1, sort_keys=True, default=float)
    open(os.path.join(out, "submission.md"), "w").write(sub)
    json.dump(metadata(tgt, info), open(os.path.join(out, "metadata.json"), "w"), indent=1)
    return F, E, info


def install(out):
    """Copies a finished build into the task folder, each file keeping its own save time."""
    for d in ("target", "golden"):
        dst = os.path.join(TASK, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(out, d), dst, copy_function=shutil.copy2)
    for name, dst in (("target.zip", TASK), ("golden.zip", TASK), ("submission.md", TASK), ("metadata.json", TASK),
                      ("figures.json", HERE), ("effort.json", HERE)):
        shutil.copyfile(os.path.join(out, name), os.path.join(dst, name))


if __name__ == "__main__":
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        os.makedirs(out, exist_ok=True)
        run(out)
    else:
        out = tempfile.mkdtemp(prefix="task9-out-")
        F, E, info = run(out)
        install(out)
        shutil.rmtree(out, ignore_errors=True)
        for z in ("target.zip", "golden.zip"):
            print("%s  %s" % (hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16], z))
        print({k: v for k, v in info.items() if k != "market_rows"})
