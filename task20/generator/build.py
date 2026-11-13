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
import sim as S  # noqa: E402
import writeup as WU  # noqa: E402

ZONE = "Europe/Oslo"
OSL = ZoneInfo(ZONE)
AS_OF = "2026-12-31"
# exports with no stamp of their own: the time each was pulled (Oslo)
SAVED = {
    PK.F_SETTLE: (2026, 12, 31, 8, 12, 40), PK.F_CURVE: (2026, 12, 31, 7, 55, 3), PK.F_PARAMS: (2026, 12, 31, 8, 14, 22),
    PK.F_STMT: (2026, 12, 31, 8, 16, 9), PK.F_POS: (2026, 12, 31, 8, 17, 51), PK.F_TRADES: (2026, 12, 31, 9, 2, 14),
    PK.F_HYDRO: (2026, 12, 31, 10, 31, 0), PK.F_PLANT: (2026, 12, 31, 10, 44, 37), PK.F_LEDGER: (2026, 12, 31, 13, 5, 12),
    PK.F_DA: (2026, 12, 31, 8, 21, 46), PK.F_FX: (2026, 12, 31, 8, 3, 55), PK.F_HDD: (2026, 12, 30, 15, 40, 18),
}
DISTRACTORS = {
    PK.F_FX: "daily EUR/NOK fixings: every price, margin and invoice in the pack is in euro, so it bears on no result",
    PK.F_HDD: "weekly heating degree days for the company's area: they look like a driver of the retail affiliate's "
              "load, but supply volumes are contracted on fixed profiles and output follows inflow and storage",
}
SOURCES = {
    PK.F_SETTLE: ("Simulated Nordvik Energy Exchange daily settlement prices for base-load futures", "evidence"),
    PK.F_CURVE: ("Simulated risk system daily monthly forward curve", "evidence"),
    PK.F_PARAMS: ("Simulated NEX Clearing margin rate notices", "evidence"),
    PK.F_STMT: ("Simulated NEX Clearing daily clearing statements for the hedge account", "evidence"),
    PK.F_POS: ("Simulated NEX Clearing month-end position statements", "evidence"),
    PK.F_TRADES: ("Simulated trade capture export of the hedge desk", "evidence"),
    PK.F_HYDRO: ("Simulated weekly inflow and storage as reported to the regulator, with weekly normals", "evidence"),
    PK.F_PLANT: ("Simulated monthly output by plant", "evidence"),
    PK.F_LEDGER: ("Simulated billing system extract of supply invoices and payments", "evidence"),
    PK.F_DA: ("Simulated day-ahead market settlements of the company's net position", "evidence"),
    PK.F_FX: ("Simulated EUR/NOK daily fixings", "distractor"),
    PK.F_HDD: ("Simulated weekly heating degree days", "distractor"),
    DC.F_POLICY: ("The company's hedging policy (written for this task)", "standard"),
    DC.F_STANDARD: ("The company's liquidity standard for the margin facility (written for this task)", "standard"),
    DC.F_NEXDOC: ("NEX Clearing's public margining summary (written for this task)", "evidence"),
    DC.F_LICENCE: ("Extract from the reservoirs' regulation licence (written for this task)", "standard"),
    DC.F_BUDGET: ("The company's budget vintages (simulated)", "evidence"),
    DC.F_CONTRACTS: ("The company's supply contract register (written for this task)", "evidence"),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    for d in (tgt, gld):
        os.makedirs(d, exist_ok=True)
    W = S.World()
    rows = PK.write_all(W, tgt)
    DC.write_all(tgt, W)
    PP.normalize_docx(os.path.join(tgt, DC.F_POLICY), "Markus Hanssen", "Helge Saether", "2024-11-27T13:02:00Z",
                      "2024-12-11T15:48:00Z", 9, 214, "task20-policy", title="Hedging policy for power sales",
                      company="Hallingvass Kraft AS")
    PP.normalize_ooxml(os.path.join(tgt, DC.F_BUDGET), "Sindre Sandvik", "Sindre Sandvik", "2017-10-05T09:12:00Z",
                       "2026-10-08T14:20:31Z", excel=True, company="Hallingvass Kraft AS")
    PP.normalize_ooxml(os.path.join(tgt, DC.F_CONTRACTS), "Jorunn Solberg", "Jorunn Solberg", "2019-11-14T10:40:00Z",
                       "2026-06-02T11:05:44Z", excel=True, company="Hallingvass Kraft AS")
    R = A.full(tgt)
    F, E = FG.write(R, root)
    GD.workbook(F, R, os.path.join(gld, GD.XLSX))
    PP.normalize_ooxml(os.path.join(gld, GD.XLSX), "Sindre Sandvik", "Jorunn Solberg", "2027-01-04T08:20:00Z",
                       "2027-01-06T16:42:09Z", excel=True, company="Hallingvass Kraft AS")
    GD.note(F, R, os.path.join(gld, GD.NOTE))
    PP.normalize_docx(os.path.join(gld, GD.NOTE), "Jorunn Solberg", "Jorunn Solberg", "2027-01-06T13:10:00Z",
                      "2027-01-06T17:02:00Z", 4, 63, "task20-note", title="Margin facility for 2027",
                      company="Hallingvass Kraft AS")
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    pulled = {n: dt.date(*SAVED[n][:3]).isoformat() for n in SAVED}
    meta = {"task": "task20", "architecture": 3, "as_of": AS_OF,
            "decision": "the committed margin facility Hallingvass Kraft needs for 2027 under its liquidity standard",
            "deliverables": [GD.XLSX, GD.NOTE],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["2022", "2027", "2026", "2021", "50", "150", "700", "38.00", "100", "70", "1,800", "300"],
            "field_terms": ["margin", "variation margin", "initial margin", "facility", "hedge ratio", "cascade",
                            "day-ahead", "inflow", "storage", "settlement"],
            "rows": rows,
            "files": {n: {"source": s, "role": r, "pull_date": pulled.get(n, AS_OF),
                          "license": "generated for this task by task20/generator (a seeded simulation of a Nordic-style "
                                     "power market, a hydro generator, its hedge desk, clearing house and customers), CC BY 4.0"}
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
    fallback = {n: dt.datetime(*v, tzinfo=OSL) for n, v in SAVED.items()}
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
        print("two builds byte-identical (%d files)" % len(ha))
    install(a)
    print("installed into", TASK)


if __name__ == "__main__":
    main()
