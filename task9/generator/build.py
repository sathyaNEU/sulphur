"""task9: the build. The pack under target/ (the FRED and Cboe series as published, cut at the record's last day; the
platform's records written by pack.py and docs.py from the simulated books), the golden deliverables, both zips,
figures.json, effort.json, submission.md and metadata.json.

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

AS_OF = "2026-11-11"          # the day the pack was put together, on the morning's pull of the public series
SERIES = {
    "NASDAQ100": "NASDAQ-100 index, daily close", "DGS2": "2-year Treasury constant-maturity yield, daily",
    "DGS10": "10-year Treasury constant-maturity yield, daily", "DTB3": "3-month Treasury bill secondary-market rate, daily",
    "DBAA": "Moody's seasoned Baa corporate bond yield, daily", "DAAA": "Moody's seasoned Aaa corporate bond yield, daily",
    "DTWEXBGS": "nominal broad US dollar index, daily", "DCOILBRENTEU": "Brent crude oil spot price, daily",
    "DEXUSAL": "US dollars per Australian dollar, noon buying rate", "DEXUSNZ": "US dollars per New Zealand dollar, noon buying rate",
    "DEXUSUK": "US dollars per pound sterling, noon buying rate", "DEXUSEU": "US dollars per euro, noon buying rate",
    "DEXJPUS": "Japanese yen per US dollar, noon buying rate", "DEXSZUS": "Swiss francs per US dollar, noon buying rate",
    "DEXCAUS": "Canadian dollars per US dollar, noon buying rate", "DEXNOUS": "Norwegian kroner per US dollar, noon buying rate",
    "DEXSDUS": "Swedish kronor per US dollar, noon buying rate", "IR3TIB01AUM156N": "Australia 3-month interbank rate, monthly (OECD)",
    "IR3TIB01NZM156N": "New Zealand 3-month interbank rate, monthly (OECD)", "IR3TIB01GBM156N": "United Kingdom 3-month interbank rate, monthly (OECD)",
    "IRSTCI01GBM156N": "United Kingdom call money rate, monthly (OECD)", "IR3TIB01EZM156N": "euro area 3-month interbank rate, monthly (OECD)",
    "IR3TIB01DEM156N": "Germany 3-month interbank rate, monthly (OECD)", "IR3TIB01JPM156N": "Japan 3-month interbank rate, monthly (OECD)",
    "IR3TIB01CHM156N": "Switzerland 3-month interbank rate, monthly (OECD)", "IR3TIB01CAM156N": "Canada 3-month interbank rate, monthly (OECD)",
    "IR3TIB01NOM156N": "Norway 3-month interbank rate, monthly (OECD)", "IR3TIB01SEM156N": "Sweden 3-month interbank rate, monthly (OECD)",
    "IR3TIB01USM156N": "United States 3-month interbank rate, monthly (OECD)",
}
COVERS = {k + ".csv": v + ", as FRED publishes it" for k, v in SERIES.items()}
COVERS.update({"SPX_History.csv": "S&P 500 index daily closing levels, as Cboe publishes them",
               "VIX_History.csv": "Cboe Volatility Index daily open, high, low and close"})
COVERS.update({
    PK.F["legacy"]: "the risk system's daily P&L and capital by pod, January 2017 to the June 2023 migration",
    PK.F["current"]: "the new risk system's daily P&L and allocated capital by book, July 2023 to 6 November 2026",
    PK.F["codes"]: "the map from the old pod codes to the book ids issued on 1 April 2022",
    PK.F["admin"]: "the administrator's month-end statements by sleeve, January 2017 to October 2026",
    PK.F["register"]: "every pod the platform has run, its strategy group, first and last trading day and status",
    PK.F["changes"]: "every change to a pod's capital, with its effective date and reason",
    PK.F["plans"]: "the allocation plans the committee approved for 2018 to 2026",
    PK.F["draft"]: "the draft allocation plan for 2027 and the 2027 platform budget",
    PK.F["policy"]: "the capital review policy (2026 edition)",
    PK.F["riskmodel"]: "the risk model's factor definitions, version 3",
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
                     pulled=raw[name]["pulled"], sha256_as_pulled=raw[name]["sha256"], rows=info["market_rows"][name])
        else:
            e.update(made="written by task9/generator (pack.py, docs.py) from the simulated books and the published series (deterministic)")
        files.append(e)
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Harbourne Capital: the 2027 net P&L to plan at the draft capital plan, with its range, and the increases that do not "
                 "earn the hurdle",
        "domain": "Quantitative Finance and Trading, Quantitative Finance",
        "task_type": "strategy backtesting and evaluation (a multi-manager platform's capital plan across its pods)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": AS_OF,
        "deliverables": [GD.DECK, GD.BOOK],
        "distractor_files": PK.DISTRACTORS,
        "stated_inputs": ["0.35", "1.5", "18", "20", "5", "7.5", "218.4", "126", "252", "40", "1.4"],
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_file": PK.F["legacy"], "largest_file_rows": info["legacy_rows"],
                        "long_file": PK.F["current"], "long_file_rows": info["current_rows"]},
        "sources": [
            {"files": "the 29 FRED series (NASDAQ100.csv to IR3TIB01USM156N.csv)", "origin": "Federal Reserve Bank of St. Louis, FRED; each "
             "series as its graph download serves it (the OECD rates are FRED's copies of the OECD Main Economic Indicators).",
             "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series>", "date": man["pulled"],
             "license": "Public domain or reproducible with attribution as FRED's terms state for each source series (Treasury, Federal "
                        "Reserve, Moody's via FRED, ICE Benchmark Administration and EIA, OECD); values reproduced unaltered with the source and "
                        "pull date recorded."},
            {"files": "SPX_History.csv, VIX_History.csv", "origin": "Cboe Global Markets daily price history downloads.",
             "url": "https://cdn.cboe.com/api/global/us_indices/daily_prices/", "date": man["pulled"],
             "license": "Published by Cboe for public download; values reproduced unaltered with the source and pull date recorded."},
            {"files": "every other file", "origin": "written for this task. Harbourne Capital, its pods, people, systems, administrator and "
                                                    "paperwork are invented; every pod's P&L is its loadings on returns computed from the "
                                                    "published series above plus its own simulated edge and noise.",
             "date": AS_OF, "license": "CC BY 4.0 (original work)"},
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
    W = WD.World(mk=MK.Market(), seed=P.SEED)
    info, B, tables, draft = PK.write(W, tgt)
    F = FG.compute(tgt, sims=sims)
    E = EP.build(F)
    GD.write_all(F, gold)
    PP.own_mtimes(gold, {})
    PP.zip_folder(tgt, os.path.join(out, "target.zip"), zone=P.ZONE)
    PP.zip_folder(gold, os.path.join(out, "golden.zip"), zone=P.ZONE)
    FG.write(F, os.path.join(out, "figures.json"))
    json.dump(E, open(os.path.join(out, "effort.json"), "w"), indent=1, sort_keys=True)
    WU.write(F, os.path.join(out, "submission.md"))
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
