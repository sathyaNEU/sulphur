"""task9 (architecture 3): the build. The pack under target/ from the simulated fab, the golden analysis on the cut pack,
figures.json, effort.json, the golden workbook and note, both zips, submission.md and metadata.json.

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
import analysis as A  # noqa: E402
import effort_passes as EP  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

AS_OF = "2026-11-13"
GOLD_ZIP = "task9_golden.zip"
ZONE = "Europe/Berlin"
BER = ZoneInfo(ZONE)


def t(y, mo, d, h, mi, s):
    return dt.datetime(y, mo, d, h, mi, s, tzinfo=BER)


F = PK.F
EXPORT_TIMES = {
    F["sort"]: t(2026, 11, 6, 7, 52, 18), F["mes"]: t(2026, 11, 6, 7, 44, 3), F["gen"]: t(2026, 11, 6, 7, 45, 40),
    F["cm1"]: t(2026, 11, 6, 8, 5, 11), F["cm2"]: t(2026, 11, 6, 8, 2, 37), F["cm3"]: t(2026, 11, 6, 8, 3, 52),
    F["cm4"]: t(2026, 11, 6, 8, 4, 29), F["dep"]: t(2026, 11, 6, 8, 11, 6), F["etch"]: t(2026, 11, 6, 8, 16, 45),
    F["mon"]: t(2026, 11, 6, 8, 18, 2), F["thk"]: t(2026, 11, 6, 8, 25, 33), F["spc"]: t(2026, 11, 6, 8, 21, 58),
    F["insp"]: t(2026, 11, 6, 8, 30, 14), F["wat"]: t(2026, 11, 6, 8, 34, 49), F["pm"]: t(2026, 11, 5, 16, 12, 44),
    F["rcp"]: t(2026, 11, 3, 10, 7, 21), F["sds"]: t(2026, 11, 4, 14, 41, 9), F["lines"]: t(2026, 2, 11, 14, 40, 21),
    F["fac"]: t(2026, 10, 29, 11, 31, 7), F["bench"]: t(2026, 11, 4, 9, 58, 36), F["lab"]: t(2026, 10, 30, 15, 2, 51),
    F["ecn"]: t(2026, 11, 4, 9, 40, 12), F["prod"]: t(2026, 10, 21, 9, 47, 36), F["plan"]: t(2026, 10, 30, 16, 41, 30),
    F["cost"]: t(2026, 10, 28, 17, 26, 9), F["notes"]: t(2026, 11, 4, 6, 12, 55), F["env"]: t(2026, 11, 2, 23, 0, 41),
    F["probe"]: t(2026, 11, 1, 6, 30, 12), F["ovl"]: t(2026, 11, 6, 8, 40, 26),
}
CATEGORY = {"csv": "spreadsheet", "xlsx": "spreadsheet", "sqlite": "database", "jsonl": "text", "txt": "text",
            "pdf": "text", "yaml": "code"}


def zip_tree(folder, out):
    """an archive as a desktop zip tool writes it: entries in name order, each at its file's own save time"""
    def info(name, p):
        tt = dt.datetime.fromtimestamp(os.path.getmtime(p), dt.timezone.utc).astimezone(BER)
        zi = zipfile.ZipInfo(name, date_time=(tt.year, tt.month, tt.day, tt.hour, tt.minute, tt.second))
        zi.create_system = 3
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        return zi
    with zipfile.ZipFile(out, "w") as z:
        for name in sorted(os.listdir(folder)):
            p = os.path.join(folder, name)
            z.writestr(info(name, p), open(p, "rb").read())


def metadata(tgt, info):
    files = []
    for name in sorted(os.listdir(tgt)):
        ext = name.rsplit(".", 1)[1]
        files.append({"path": name, "format": ext, "bytes": os.path.getsize(os.path.join(tgt, name)),
                      "made": "written by task9/generator from the simulated fab (deterministic)"})
    fmts = sorted({f["format"] for f in files})
    return {
        "task": "task9",
        "title": "Varnholt Halbleiter Fab 2: the June to September 2026 sort-yield shortfall on VX40 and VP12 and VR90's Q1 2027 yield",
        "domain": "General Statistics & Data Science, Interpretability",
        "objective": "Root-Cause Analysis",
        "as_of": "2026-11-06", "built": AS_OF,
        "deliverables": list(GD.FILES),
        "distractor_files": PK.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "categories": sorted({CATEGORY[x] for x in fmts}),
                        "largest_csv": F["mes"], "largest_csv_rows": info["mes_rows"], "long_csv": F["sds"],
                        "long_csv_rows": info["sds_rows"], "sort_wafers": info["sort_wafers"],
                        "sqlite_tables": 6, "pack_bytes": sum(f["bytes"] for f in files)},
        "sources": [{"files": "every file", "origin": "written for this task. Varnholt Halbleiter GmbH, its Fab 2 in Dresden, "
                     "its products, tools, people and paperwork are invented; the fab is simulated lot by lot and wafer by "
                     "wafer (lot starts, dispatch with bay rules and downtime, facilities, chemistry, film profiles, etch, "
                     "clustered defects, sort, metrology and inspection sampling) and every record is written from that "
                     "process.", "date": AS_OF, "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }


def run(out):
    tgt, gold = os.path.join(out, "target"), os.path.join(out, "golden")
    for d in (tgt, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    fab = W.Fab(seed=P.SEED)
    info = PK.write(fab, tgt)
    PP.own_mtimes(tgt, EXPORT_TIMES)
    Fr, X = A.run_all(tgt)
    fg = FG.compute(Fr, X)
    E = EP.build(Fr, X, fg)
    fg["shortcut"] = E.pop("_shortcut")
    fg["routes"] = E["routes"]
    fg["bands"] = {k: ([v[0], v[1]] if isinstance(v, tuple) else {c: [x[0], x[1]] for c, x in v.items()})
                   for k, v in EP.BANDS.items()}
    GD.write_all(fg, gold)
    PP.own_mtimes(gold, {})
    zip_tree(tgt, os.path.join(out, "target.zip"))
    zip_tree(gold, os.path.join(out, GOLD_ZIP))
    sub = WU.build(fg)
    FG.write(fg, os.path.join(out, "figures.json"))
    json.dump(E, open(os.path.join(out, "effort.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(out, "submission.md"), "w").write(sub)
    json.dump(metadata(tgt, info), open(os.path.join(out, "metadata.json"), "w"), indent=1)
    return fg, E, info


def install(out):
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
        fg, E, info = run(out)
        install(out)
        shutil.rmtree(out, ignore_errors=True)
        for z in ("target.zip", GOLD_ZIP):
            print("%s  %s" % (hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16], z))
        print(info)
