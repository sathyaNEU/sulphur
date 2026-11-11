"""Build task20's pack, goldens, figures.json, effort.json, submission.md and metadata.json twice, require byte-identical
output, install them and cut target.zip and golden.zip.

    python3 task20/generator/build.py            # full build (two passes)
    python3 task20/generator/build.py --once     # one pass into the task folder, no comparison
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

ZONE = "America/New_York"
NY = ZoneInfo(ZONE)
AS_OF = "2025-07-14"
# exports with no stamp of their own: the time each was pulled or written (New York)
SAVED = {
    PK.F_VENDOR: (2025, 7, 1, 6, 12, 40),
    PK.F_SPX: (2025, 7, 7, 10, 21, 5),
    PK.F_NDX: (2025, 7, 7, 10, 23, 48),
    PK.F_SETTLE: (2025, 7, 1, 7, 2, 11),
    PK.F_MASTER: (2025, 7, 1, 8, 15, 30),
    PK.F_MAP: (2025, 7, 1, 8, 40, 2),
    PK.F_XWALK: (2025, 1, 21, 7, 30, 19),
    PK.F_EQX1: (2025, 1, 21, 6, 5, 12),
    PK.F_EQX2: (2025, 7, 1, 6, 30, 44),
    PK.F_FUTS: (2025, 7, 1, 6, 31, 20),
    PK.F_BLOTTER: (2025, 7, 8, 7, 12, 40),
    PK.F_PC: (2025, 7, 2, 9, 14, 55),
    PK.F_GL: (2025, 7, 3, 8, 47, 31),
    PK.F_RUNLOG: (2025, 7, 1, 6, 45, 9),
    PK.F_LIMITS: (2025, 7, 1, 7, 20, 37),
}
DISTRACTORS = {
    PK.F_LIMITS: "the desk's daily VaR limit utilisation: it looks like a record of the VaR's adequacy but only restates "
                 "the reported VaR against a limit",
    DC.F_STRESS: "the desk's weekly stress results under standing scenarios: they look like a measure of the risks not in "
                 "VaR but price fixed shocks on the engine's book and bear on no heading or add-on",
    PK.F_GL: "the general ledger journal: it looks like the booked P&L's source of record and agrees with product control "
             "to the dollar, but no result needs it beyond the booked figure product control already carries",
}
SOURCES = {
    PK.F_VENDOR: ("Simulated market data vendor end-of-day closes for the desk's universe of 190 invented Nasdaq small "
                  "and mid caps, driven by the published index tape", "evidence"),
    PK.F_SPX: ("S&P 500 Index daily closes, Cboe index history download (SPX_History.csv), values as published, cut at "
               "30 June 2025", "evidence"),
    PK.F_NDX: ("NASDAQ-100 Index daily closes, FRED series NASDAQ100 (Nasdaq), values as published, cut at 30 June 2025",
               "evidence"),
    PK.F_SETTLE: ("Simulated CME E-mini S&P 500 and E-mini Nasdaq-100 daily settlements, index levels with carry",
                  "evidence"),
    PK.F_MASTER: ("Simulated instrument master of the desk's universe", "evidence"),
    PK.F_MAP: ("Simulated risk engine proxy mapping vintages (quarterly betas, store start dates)", "evidence"),
    PK.F_XWALK: ("Simulated EQX v1 to v2 instrument crosswalk from the January 2025 migration", "evidence"),
    PK.F_EQX1: ("Simulated EQX cash position extracts, v1 schema", "evidence"),
    PK.F_EQX2: ("Simulated EQX cash position extracts, v2 schema", "evidence"),
    PK.F_FUTS: ("Simulated FUTS futures position snapshots", "evidence"),
    PK.F_BLOTTER: ("Simulated order management system blotter export", "evidence"),
    PK.F_PC: ("Simulated product control daily P&L", "evidence"),
    PK.F_GL: ("Simulated general ledger journal for the desk's cost centre", "distractor"),
    PK.F_RUNLOG: ("Simulated risk engine run log", "evidence"),
    PK.F_LIMITS: ("Simulated VaR limit utilisation report", "distractor"),
    DC.F_STANDARD: ("Market Risk Standard MRS-4 (written for this task)", "governing"),
    DC.F_METHOD: ("ERE methodology note (written for this task)", "governing"),
    DC.F_PLAN: ("The desk's second-half 2025 plan (written for this task)", "evidence"),
    DC.F_BACKTEST: ("The quarter's official backtest (simulated)", "incumbent"),
    DC.F_STRESS: ("The desk's weekly stress results (simulated)", "distractor"),
}
LICENSE = {
    PK.F_SPX: "Cboe index history, published by Cboe for public download; values reproduced unaltered with source and "
              "pull date",
    PK.F_NDX: "FRED series NASDAQ100, reproducible with attribution under FRED's terms of use (source: Nasdaq); values "
              "reproduced unaltered with source and pull date",
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def write_pack(tgt):
    w = W.simulate(PK.SEED)
    o = PK.write_all(tgt, w)
    DC.standard(os.path.join(tgt, DC.F_STANDARD))
    DC.method_note(os.path.join(tgt, DC.F_METHOD))
    DC.plan(os.path.join(tgt, DC.F_PLAN))
    PP.normalize_ooxml(os.path.join(tgt, DC.F_PLAN), "Christopher Reilly", "Christopher Reilly", "2025-06-20T19:41:00Z",
                       "2025-06-27T20:10:14Z", excel=True, company="Tarrant Hale Securities LLC")
    n = DC.backtest(os.path.join(tgt, DC.F_BACKTEST), w, o["P"])
    PP.normalize_ooxml(os.path.join(tgt, DC.F_BACKTEST), "Nancy Ayala", "Nancy Ayala", "2025-07-02T21:04:00Z",
                       "2025-07-03T19:22:10Z", excel=True, company="Tarrant Hale Securities LLC")
    DC.stress(os.path.join(tgt, DC.F_STRESS), w, o["names"], o["tm"])
    PP.normalize_ooxml(os.path.join(tgt, DC.F_STRESS), "SMCF Risk Desk", "SMCF Risk Desk", "2024-07-08T12:15:00Z",
                       "2025-06-30T21:40:52Z", excel=True, company="Tarrant Hale Securities LLC")
    rows = dict(o["rows"])
    rows[DC.F_BACKTEST] = 250
    return w, o, rows


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    for d in (tgt, gld):
        os.makedirs(d, exist_ok=True)
    w, o, rows = write_pack(tgt)
    R = A.run(tgt)
    F, E = FG.write(R, root)
    GD.workbook(F, R, os.path.join(gld, GD.XLSX))
    PP.normalize_ooxml(os.path.join(gld, GD.XLSX), "Nancy Ayala", "Nancy Ayala", "2025-07-15T13:12:00Z",
                       "2025-07-18T14:58:02Z", excel=True, company="Tarrant Hale Securities LLC")
    GD.note(F, os.path.join(gld, GD.NOTE))
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    pulled = {n: dt.date(*SAVED[n][:3]).isoformat() for n in SAVED}
    meta = {"task": "task20", "architecture": 1, "as_of": AS_OF,
            "decision": "which of the SMCF desk's VaR exceptions in the 250 days to 30 June 2025 the model answers for, "
                        "each dated under one MRS-4 heading, the corrected count and zone, and the add-on for July to "
                        "December 2025",
            "deliverables": [GD.XLSX, GD.NOTE],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["99", "250", "500", "86", "0.94", "0.97", "2024", "2025", "30", "18:30", "18:45"],
            "field_terms": ["the model", "risks not in the model", "count against the model"],
            "rows": rows,
            "market_tape": {"source": "Cboe index history (S&P 500) and FRED NASDAQ100, pulled 2026-11-11; the raw "
                                      "downloads and their sha256 sit in generator/raw/manifest.json",
                            "truncated_at": "2025-06-30"},
            "files": {n: {"source": s, "role": r,
                          "pull_date": pulled.get(n, AS_OF),
                          "license": LICENSE.get(n, "generated for this task by task20/generator (a seeded simulation of "
                                                     "the desk, its systems and its documents on the published index "
                                                     "tape), CC BY 4.0")}
                      for n, (s, r) in sorted(SOURCES.items())}}
    json.dump(meta, open(os.path.join(root, "metadata.json"), "w"), indent=1)
    return F


def hashes(root):
    out = {}
    for sub in ("target", "golden"):
        for f in sorted(os.listdir(os.path.join(root, sub))):
            out["%s/%s" % (sub, f)] = sha(os.path.join(root, sub, f))
    for f in ("figures.json", "effort.json", "submission.md", "metadata.json"):
        out[f] = sha(os.path.join(root, f))
    return out


def install(root):
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(root, sub), dst)
    for f in ("figures.json", "effort.json"):
        shutil.copy(os.path.join(root, f), os.path.join(HERE, f))
    for f in ("submission.md", "metadata.json"):
        shutil.copy(os.path.join(root, f), os.path.join(TASK, f))
    fallback = {n: dt.datetime(*v, tzinfo=NY) for n, v in SAVED.items()}
    PP.own_mtimes(os.path.join(TASK, "target"), fallback)
    PP.own_mtimes(os.path.join(TASK, "golden"), {})
    PP.zip_folder(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"), zone=ZONE)
    PP.zip_folder(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"), zone=ZONE)


def main():
    once = "--once" in sys.argv
    a = tempfile.mkdtemp(prefix="task20a-")
    build_into(a)
    if not once:
        b = tempfile.mkdtemp(prefix="task20b-")
        build_into(b)
        ha, hb = hashes(a), hashes(b)
        diff = [k for k in ha if ha[k] != hb.get(k)]
        if diff:
            print("NOT byte-identical:", diff)
            sys.exit(1)
        print("two builds byte-identical over %d files" % len(ha))
        shutil.rmtree(b)
    install(a)
    shutil.rmtree(a)
    print("installed")


if __name__ == "__main__":
    main()
