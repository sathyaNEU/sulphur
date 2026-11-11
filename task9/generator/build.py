"""task9: the build. The pack under target/ (written by pack.py and docs.py from the simulated fleet), the golden
deliverables, both zips, figures.json, effort.json, submission.md and metadata.json.

    python3 build.py                 # builds into a scratch folder, then installs into the task folder
    python3 build.py --out <folder>  # builds into <folder> only (two such builds are byte-identical)
"""
import datetime as dt
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
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402

AS_OF = "2026-11-11"
GOLD_ZIP = "task9_golden.zip"
CT = dt.timezone(dt.timedelta(hours=-5))
# each export's own save time on the systems that wrote it (the files carry no stamp of their own)
EXPORT_TIMES = {
    PK.F["inventory"]: dt.datetime(2026, 10, 1, 6, 12, 40, tzinfo=CT),
    PK.F["quarters"]: dt.datetime(2026, 10, 1, 7, 48, 3, tzinfo=CT),
    PK.F["tickets"]: dt.datetime(2026, 10, 1, 6, 31, 17, tzinfo=CT),
    PK.F["events"]: dt.datetime(2026, 10, 1, 9, 4, 52, tzinfo=CT),
    PK.F["wiki"]: dt.datetime(2026, 9, 2, 15, 22, 9, tzinfo=CT),
    PK.F["costs"]: dt.datetime(2026, 9, 30, 17, 41, 26, tzinfo=CT),
    PK.F["closeout"]: dt.datetime(2026, 10, 2, 10, 15, 33, tzinfo=CT),
    PK.F["env"]: dt.datetime(2026, 10, 1, 5, 2, 11, tzinfo=CT),
    PK.F["ssd"]: dt.datetime(2026, 10, 1, 6, 58, 47, tzinfo=CT),
    GD.CHART: dt.datetime(2026, 10, 15, 16, 21, 5, tzinfo=CT),
}
COVERS = {
    PK.F["inventory"]: "every serial seen in a vault slot since 2022: model, vault, chassis, slot, install, first and last "
                       "seen, removal date and reason, firmware, purchase order",
    PK.F["quarters"]: "each drive's telemetry rolled up by quarter: days observed, replacement flag, SMART maxima, power-on "
                      "hours, temperature, firmware",
    PK.F["tickets"]: "the data-centre technicians' removal tickets with their free-text notes",
    PK.F["events"]: "vault life events: commissioning, the Brightstore migration, decommissioning reviews and work, logged "
                    "chassis power events and cooling excursions",
    PK.F["handover"]: "Brightstore's handover workbook: the rack manifest, purchase batches and its own failure summary",
    PK.F["kestrel"]: "the drive vendor's field guide to its serial numbers and factory firmware",
    PK.F["wiki"]: "the operations wiki page defining replacements, the health-pull policies, spares and decommissioning",
    PK.F["capacity"]: "the vault installs scheduled for 2026-Q4 to 2027-Q3",
    PK.F["costs"]: "spares on hand, lead time, unit costs, the vault-migration and failure-handling costs, the stock-out "
                   "tolerance",
    PK.F["closeout"]: "the Q3 2026 fleet reliability close-out page: quarterly replacement rates by data centre",
    PK.F["env"]: "daily temperature and humidity by data centre",
    PK.F["datasheets"]: "the drive vendors' published reliability specifications",
    PK.F["ssd"]: "boot SSD telemetry",
}
CATEGORY = {"csv": "spreadsheet", "xlsx": "spreadsheet", "pdf": "text", "md": "text", "yaml": "code", "png": "image"}


def metadata(tgt, info):
    files = []
    for name in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, name)
        e = {"path": name, "format": name.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "covers": COVERS[name],
             "made": "written by task9/generator (world.py, pack.py, docs.py) from the simulated fleet (deterministic)"}
        files.append(e)
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Halden Vault's drive replacements for 2026-Q4 to 2027-Q3: the quarterly path with its range, the fourth "
                 "quarter's spare order and the HX-8 bad builds' migration",
        "domain": "General Statistics & Data Science, Bayesian modeling & posterior inference",
        "task_type": "Bayesian modeling and posterior inference (a posterior predictive forecast of replacement counts "
                     "from a hierarchical hazard model)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": AS_OF,
        "setting_date": str(P.END),
        "deliverables": list(GD.FILES),
        "distractor_files": PK.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_file": PK.F["quarters"], "largest_file_rows": info["quarter_rows"],
                        "long_file": PK.F["inventory"], "long_file_rows": info["inventory_rows"],
                        "tickets_rows": info["ticket_rows"], "events_rows": info["event_rows"]},
        "sources": [
            {"files": "every file", "origin": "written for this task. Halden Vault, Brightstore, Kestrel Data Products, "
             "Meridian, Tamsin, Borealis, the drives, vaults, tickets and paperwork are invented; the fleet is simulated day by "
             "day per vault (manufacture batches and deploy lags, family wear-out hazards with an infant term, vault and batch "
             "frailty, one manufacturing window whose hazard ramps with age, chassis power and cooling incidents, SMART "
             "precursors and two health-pull policies, replacements into the same slot, selective decommissioning, and an "
             "acquired data centre whose records start at its migration), and every record is written from that process.",
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
    W = WD.World(seed=P.SEED)
    info, _ = PK.write(W, tgt)
    PP.own_mtimes(tgt, EXPORT_TIMES)
    F = FG.compute(tgt, sims=sims)
    E = EP.build(F)
    GD.write_all(F, gold)
    PP.own_mtimes(gold, EXPORT_TIMES)
    PP.zip_folder(tgt, os.path.join(out, "target.zip"), zone="America/Chicago")
    PP.zip_folder(gold, os.path.join(out, GOLD_ZIP), zone="America/Chicago")
    sub = WU.build(F)
    F["stated_text"] = sorted(set(WU.STATED))      # every figure the answer blocks state, as they state it
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
    for name, dst in (("target.zip", TASK), (GOLD_ZIP, TASK), ("submission.md", TASK), ("metadata.json", TASK),
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
        for z in ("target.zip", GOLD_ZIP):
            print("%s  %s" % (hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16], z))
        print(info)
