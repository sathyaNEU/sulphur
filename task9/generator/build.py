"""task9: the build. The pack under target/ (written by pack.py and docs.py from the simulated fab), the golden deck,
both zips, figures.json, effort.json, submission.md and metadata.json.

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
import zipfile
from zoneinfo import ZoneInfo

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
AZ = dt.timezone(dt.timedelta(hours=-7))
ZONE = "America/Phoenix"
# each export's own save time on the system that wrote it (the files carry no stamp of their own)
EXPORT_TIMES = {
    PK.F["sort"]: dt.datetime(2026, 8, 31, 22, 14, 37, tzinfo=AZ),
    PK.F["mes"]: dt.datetime(2026, 8, 31, 23, 2, 11, tzinfo=AZ),
    PK.F["fdc"]: dt.datetime(2026, 8, 31, 22, 41, 50, tzinfo=AZ),
    PK.F["diemaps"]: dt.datetime(2026, 8, 31, 21, 37, 4, tzinfo=AZ),
    PK.F["geometry"]: dt.datetime(2025, 11, 18, 10, 6, 29, tzinfo=AZ),
    PK.F["examples"]: dt.datetime(2026, 6, 24, 9, 31, 0, tzinfo=AZ),
    PK.F["spec"]: dt.datetime(2026, 8, 27, 16, 48, 22, tzinfo=AZ),
    PK.F["ticket"]: dt.datetime(2026, 7, 30, 15, 2, 46, tzinfo=AZ),
    PK.F["costs"]: dt.datetime(2026, 8, 28, 11, 26, 9, tzinfo=AZ),
    PK.F["rf"]: dt.datetime(2026, 8, 31, 6, 0, 3, tzinfo=AZ),
    PK.F["particles"]: dt.datetime(2026, 8, 31, 6, 30, 41, tzinfo=AZ),
    PK.F["sc4"]: dt.datetime(2026, 8, 30, 13, 17, 55, tzinfo=AZ),
    PK.F["slurry"]: dt.datetime(2026, 8, 24, 8, 44, 12, tzinfo=AZ),
    PK.F["stores"]: dt.datetime(2026, 8, 31, 17, 5, 48, tzinfo=AZ),
    PK.F["ft"]: dt.datetime(2026, 8, 31, 19, 52, 26, tzinfo=AZ),
}
COVERS = {
    PK.F["sort"]: "the sort database's wafer records: zone fail and tested counts, bins, the classifier's label, retests",
    PK.F["mes"]: "the MES: lot-level steps and the six chamber-per-wafer steps with their tools and times",
    PK.F["pm"]: "the ILD-CMP units' PM log, one row per entry as the technicians made it",
    PK.F["fdc"]: "the polish record per wafer from the units' fault-detection system",
    PK.F["diemaps"]: "the yield database's die maps for the wafers pulled into the review set, with the die geometry",
    PK.F["geometry"]: "the yield database's die position helpers (zones by radius)",
    PK.F["examples"]: "twelve wafer maps from the yield review deck",
    PK.F["spec"]: "the ILD-CMP PM specification's revision history, waiver EW-118 and the Rev G draft",
    PK.F["ticket"]: "the yield excursion ticket YE-2026-031",
    PK.F["costs"]: "finance's cost inputs: parts, labour, downtime, single changes and the full PM all in, volume, die values",
    PK.F["rf"]: "the deposition chambers' RF hours since their last clean, by day",
    PK.F["particles"]: "hourly particle counts by bay",
    PK.F["sc4"]: "scanner SC-4's edge-field focus and levelling data for its lots",
    PK.F["slurry"]: "slurry lot certificates of analysis",
    PK.F["stores"]: "the CMP consumables' receiving log by part and lot",
    PK.F["ft"]: "the back-end site's per-lot summary of units in and out at each step",
}
CATEGORY = {"csv": "spreadsheet", "xlsx": "spreadsheet", "sqlite": "database", "py": "code", "md": "text", "txt": "text",
            "yaml": "code", "png": "image"}


def png_times(folder):
    """The review deck's maps, exported one by one on 24 June."""
    out = {}
    for k, name in enumerate(sorted(os.listdir(folder))):
        out[name] = dt.datetime(2026, 6, 24, 9, 12, 0, tzinfo=AZ) + dt.timedelta(seconds=37 * k + 5)
    return out


def zip_tree(folder, out, zone=ZONE):
    """An archive of a folder as a desktop zip tool writes it: entries in name order, a folder's entry before its
    files, each entry's time the file's own modification time in the sender's local clock."""
    tz = ZoneInfo(zone)

    def info(name, p):
        t = dt.datetime.fromtimestamp(os.path.getmtime(p), dt.timezone.utc).astimezone(tz)
        zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
        zi.create_system = 3
        return zi
    with zipfile.ZipFile(out, "w") as z:
        for name in sorted(os.listdir(folder)):
            p = os.path.join(folder, name)
            if os.path.isdir(p):
                zi = info(name + "/", p)
                zi.external_attr = (0o40755 << 16) | 0x10
                z.writestr(zi, b"")
                for sub in sorted(os.listdir(p)):
                    zs = info(name + "/" + sub, os.path.join(p, sub))
                    zs.compress_type = zipfile.ZIP_DEFLATED
                    zs.external_attr = 0o644 << 16
                    z.writestr(zs, open(os.path.join(p, sub), "rb").read())
            else:
                zi = info(name, p)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, open(p, "rb").read())


def metadata(tgt, info):
    files = []
    for name in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, name)
        if os.path.isdir(p):
            for sub in sorted(os.listdir(p)):
                files.append({"path": name + "/" + sub, "format": "png", "bytes": os.path.getsize(os.path.join(p, sub)),
                              "covers": COVERS[name], "made": "written by task9/generator (pack.py) from the simulated fab"})
            continue
        files.append({"path": name, "format": name.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "covers": COVERS[name],
                      "made": "written by task9/generator (world.py, pack.py, docs.py) from the simulated fab (deterministic)"})
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Tessaline Fab 2's edge ring: what causes it, what it cost from April to August 2026, and after how many "
                 "wafers each polish unit should change the part responsible once Rev G takes it out of the full PM",
        "domain": "Machine Learning Research, General Statistics & Data Science (Interpretability: feature attribution, probing, "
                  "mechanistic analysis)",
        "task_type": "Interpretability: a sort-yield loss attributed across dependent process features to the part whose "
                     "wear carries it, its dose-response, and its split across the maintenance rules",
        "objective": "Root-Cause Analysis",
        "as_of": str(P.PULL),
        "built": AS_OF,
        "setting_date": str(P.PULL),
        "deliverables": list(GD.FILES),
        "distractor_files": PK.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_file": PK.F["mes"], "largest_file_rows": info["mes_rows"],
                        "long_file": PK.F["sort"], "long_file_rows": info["sort_rows"],
                        "pm_rows": info["pm_rows"], "fdc_rows": info["fdc_rows"], "diemap_wafers": info["diemap_wafers"]},
        "sources": [
            {"files": "every file", "origin": "written for this task. Tessaline Semiconductor, Fab 2, its products, tools, "
             "people and paperwork are invented; the fab is simulated wafer by wafer (weekly lot starts at a shifting product "
             "mix, a forty-step flow with six chamber steps and one deposition chamber's affinity for two polish units, "
             "dispatch around each unit's downtime, clustered random defects with a weekly drift and a particle week, the "
             "outermost zone's fallout, conditioner-disk wear at each unit's, each supplier lot's and each disk's own rate "
             "with a pad term, thinned edge dielectric that passes sort and fails burn-in, the maintenance the spec, waiver "
             "EW-118 and the floor's unscheduled swaps produced, stores issuing the oldest disk lot first, removal-rate "
             "metrology, the ring classifier, the yield team's review pulls, assembly loss and final test at the assembly "
             "house), and every record is written from that process.",
             "date": AS_OF, "license": "CC BY 4.0 (original work)"},
        ],
        "files": files,
    }


def run(out):
    tgt, gold = os.path.join(out, "target"), os.path.join(out, "golden")
    for d in (tgt, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    fab = WD.Fab(seed=P.SEED)
    info, _ = PK.write(fab, tgt)
    ex = os.path.join(tgt, PK.F["examples"])
    PP.own_mtimes(ex, png_times(ex))
    PP.own_mtimes(tgt, EXPORT_TIMES)
    F = FG.compute(tgt)
    E = EP.build(F)
    GD.write_all(F, gold)
    PP.own_mtimes(gold, {})
    zip_tree(tgt, os.path.join(out, "target.zip"))
    zip_tree(gold, os.path.join(out, GOLD_ZIP))
    sub = WU.build(F)
    F["stated_text"] = sorted(set(WU.STATED))
    FG.write(F, os.path.join(out, "figures.json"))
    json.dump(FG.jsonable(E), open(os.path.join(out, "effort.json"), "w"), indent=1, sort_keys=True)
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
