"""task9: the build. The pack under target/ (the Cboe histories byte for byte from raw/, the sleeve's paperwork written
by pack.py and docs.py), the golden deliverables, both zips, figures.json, effort.json, submission.md and metadata.json.

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
import analysis as AN  # noqa: E402
import effort_passes as EP  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import market as MK  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402
import writeup as WU  # noqa: E402

AS_OF = "2026-11-10"          # the day the pack was put together: closes through the review date, pulled the next morning
COVERS = {
    "SPX_History.csv": "S&P 500 Index daily closing levels as Cboe publishes them",
    "VIX_History.csv": "Cboe Volatility Index (30-day) daily open, high, low and close",
    "VIX9D_History.csv": "Cboe S&P 500 9-Day Volatility Index daily open, high, low and close",
    "VIX3M_History.csv": "Cboe S&P 500 3-Month Volatility Index daily open, high, low and close",
    "VIX6M_History.csv": "Cboe S&P 500 6-Month Volatility Index daily open, high, low and close",
    "VIX1Y_History.csv": "Cboe S&P 500 1-Year Volatility Index daily open, high, low and close",
    "VVIX_History.csv": "Cboe VIX of VIX Index daily closing levels",
    "SKEW_History.csv": "Cboe SKEW Index daily closing levels",
    PK.F["holidays"]: "New York Stock Exchange holidays and early closes, 2026 to 2028",
    PK.F["blotter"]: "the investment office's order blotter for the sleeve: every ticket since July 2021, and the dealer panel",
    PK.F["settlements"]: "settlement advices for the sleeve's expired swaps",
    PK.F["valuations"]: "the custodian's file of the three dealers' daily valuations of each open swap, July 2021 to October 30, 2026",
    PK.F["ledger"]: "the custodian's collateral ledger for the sleeve, by dealer and day",
    PK.F["policy"]: "Investment Policy Statement, Schedule D (the sleeve's program, limits, measurement and cash plan)",
    PK.F["confirmation"]: "the master confirmation for the variance swap transactions",
    PK.F["csa"]: "treasury's summary of the three credit support annexes",
    PK.F["terms"]: "the dealer panel's indicative terms for 3-month and 6-month ladders",
    PK.F["assets"]: "extract of the audited statement of net assets at June 30, 2026",
    PK.F["st_BSS"]: "Brecon Sound's statement of open transactions at October 30, 2026",
    PK.F["st_ACM"]: "Altamere's statement of open transactions at October 30, 2026",
    PK.F["st_WXB"]: "Wexcombe's statement of open transactions at October 30, 2026",
}
CATEGORY = {"csv": "spreadsheet", "xlsx": "spreadsheet", "pdf": "text"}


def metadata(tgt, info):
    man = json.load(open(os.path.join(MK.RAW, "manifest.json")))
    chk = json.load(open(os.path.join(HERE, "raw_check", "manifest.json")))
    raw = {f["file"]: f for f in man["files"]}
    files = []
    for name in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, name)
        e = {"path": name, "format": name.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "covers": COVERS[name]}
        if name in raw:
            e.update(made="downloaded from Cboe Global Markets and shipped unaltered", url=raw[name]["url"], pulled=raw[name]["pulled"],
                     sha256=raw[name]["sha256"], rows=raw[name]["rows"])
            assert hashlib.sha256(open(p, "rb").read()).hexdigest() == raw[name]["sha256"], "%s differs from the pull" % name
        elif name == PK.F["holidays"]:
            e.update(made="transcribed from the exchange's published holiday schedule", rows=info[name])
        else:
            e.update(made="written by task9/generator (pack.py, docs.py) from the authored positions and the published closes (deterministic)")
            if name in info:
                e["rows"] = info[name]
        files.append(e)
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Carrow Fields Foundation: how large a 3-month variance swap program the volatility sleeve can add from January 2027, and the "
                 "sleeve's 2027 cash plan",
        "domain": "Quantitative Finance and Trading, Quantitative Finance",
        "task_type": "derivative pricing and collateral exposure",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": AS_OF,
        "deliverables": [GD.MEMO, GD.BOOK, GD.DAILY],
        "distractor_files": PK.DISTRACTORS,
        "field_terms": ["ladder"],
        "stated_inputs": ["200,000", "50,000", "25,000", "100,000", "250,000", "1,487.6"],
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_file": PK.F["valuations"], "largest_file_rows": info[PK.F["valuations"]],
                        "long_file": PK.F["ledger"], "long_file_rows": info[PK.F["ledger"]]},
        "sources": [
            {"files": "the eight *_History.csv files", "origin": man["source"] + ". Used as is: each file ships byte for byte as downloaded.",
             "url": "https://cdn.cboe.com/api/global/us_indices/daily_prices/", "date": man["pulled"],
             "license": "Published by Cboe Global Markets for public download. The values are facts, reproduced unaltered with the source and the "
                        "pull date recorded. The S&P 500 is a product of S&P Dow Jones Indices, whose closing levels Cboe republishes in the "
                        "same download."},
            {"files": PK.F["holidays"], "origin": "the New York Stock Exchange's published holiday and early-close schedule for 2026 to 2028, "
                                                   "transcribed", "url": "https://www.nyse.com/markets/hours-calendars", "date": man["pulled"],
             "license": "public schedule, facts only"},
            {"files": "every other file", "origin": "written for this task. The foundation, its dealers, custodian, people, positions and paperwork "
                                                    "are invented; every market value in them is computed from the published closes above.",
             "date": AS_OF, "license": "CC BY 4.0 (original work)"},
        ],
        "cross_check_source": {
            "series": chk["source"], "url": chk["url"], "date": chk["pulled"], "sha256": chk["sha256"], "first": chk["first"],
            "shipped": False,
            "what": "The same index as VIX3M_History.csv, published back to 2007-12-04 (the Cboe download begins 2009-09-18) and equal to it on "
                    "every day both carry. Held in the generator beside the pulls, outside the pack, and read by no golden figure; every graded "
                    "band is checked to contain the answer obtained with it."},
        "files": files,
    }


def run(out):
    tgt, gold = os.path.join(out, "target"), os.path.join(out, "golden")
    for d in (tgt, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    scratch = tempfile.mkdtemp(prefix="task9-build-")
    A = AN.Analysis()
    R = A.run()
    F = FG.make(A, R)
    info = PK.write(A, tgt)
    PP.own_mtimes(tgt, PK.EXPORT_TIMES)
    GD.write_all(A, R, F, gold, scratch)
    shutil.rmtree(scratch, ignore_errors=True)
    PP.zip_folder(tgt, os.path.join(out, "target.zip"), zone=P.ZONE)
    PP.zip_folder(gold, os.path.join(out, "golden.zip"), zone=P.ZONE)
    E = EP.build(A, R, F)
    json.dump(F, open(os.path.join(out, "figures.json"), "w"), indent=1)
    json.dump(E, open(os.path.join(out, "effort.json"), "w"), indent=1)
    WU.write(os.path.join(out, "submission.md"), F)
    json.dump(metadata(tgt, info), open(os.path.join(out, "metadata.json"), "w"), indent=1)
    return A, R, F, E, info


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
        A, R, F, E, info = run(out)
        install(out)
        shutil.rmtree(out, ignore_errors=True)
        for z in ("target.zip", "golden.zip"):
            print("%s  %s" % (hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16], z))
        print({k: v for k, v in info.items()})
