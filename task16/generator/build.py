"""Build the pack under target/: the pilot's jobs (sweep.py, trained for real by runner.py), each system's export of
them (pack.py), the group's own documents (docs.py), the workbook laid out as Excel saves it, each file's time its
own last save.

    python3 build.py [--out <folder>]
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs
import pack
import postprocess
import runner as R
import sweep as S

FILES = pack.FILES
DISTRACTORS = pack.DISTRACTORS
ORG = "MML group"
CET = dt.timezone(dt.timedelta(hours=1))
# when each system wrote its export (local time), or when the file was last saved
WRITTEN = {
    "metrics": dt.datetime(2026, 11, 4, 9, 12, 41, tzinfo=CET),
    "runs": dt.datetime(2026, 11, 4, 9, 11, 58, tzinfo=CET),
    "items": dt.datetime(2026, 11, 4, 10, 3, 27, tzinfo=CET),
    "devsplit": dt.datetime(2026, 9, 18, 16, 44, 9, tzinfo=CET),
    "shards": dt.datetime(2026, 10, 22, 14, 20, 33, tzinfo=CET),
    "routes": dt.datetime(2026, 10, 16, 11, 5, 50, tzinfo=CET),
    "classes": dt.datetime(2026, 6, 12, 13, 31, 16, tzinfo=CET),
    "jobs": dt.datetime(2026, 11, 2, 8, 47, 2, tzinfo=CET),
    "ckpt": dt.datetime(2026, 11, 4, 9, 30, 15, tzinfo=CET),
    "bench": dt.datetime(2026, 11, 3, 15, 22, 39, tzinfo=CET),
    "notes": dt.datetime(2026, 11, 5, 16, 58, 4, tzinfo=CET),
    "defaults": dt.datetime(2026, 10, 23, 17, 9, 21, tzinfo=CET),
    "launch": dt.datetime(2026, 10, 26, 8, 46, 52, tzinfo=CET),
    "probe": dt.datetime(2026, 9, 24, 12, 15, 7, tzinfo=CET),
    "counts": dt.datetime(2026, 10, 22, 14, 26, 48, tzinfo=CET),
}
OFFICE = {"shortlist": ("2026-11-03T13:41:00Z", "2026-11-05T15:36:00Z", "Tor Fredriksen")}


def run(target, jobs=None):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    if jobs is None:
        R.run_all([j["train"] for j in S.pilot_specs()], verbose=False)
        jobs = pack.load_jobs()
    n = {}
    n["metrics"] = pack.write_metrics(jobs, F["metrics"])
    n["runs"] = pack.write_runs(jobs, F["runs"])
    n["items"] = pack.write_items(jobs, F["items"])
    n["devsplit"] = pack.write_devsplit(F["devsplit"])
    n["shards"] = pack.write_shards(F["shards"])
    pack.write_routes(F["routes"])
    pack.write_classes(F["classes"])
    n["jobs"] = pack.write_jobs(jobs, F["jobs"])
    n["ckpt"] = pack.write_ckpt(jobs, F["ckpt"])
    n["bench"] = pack.write_bench(jobs, F["bench"])
    pack.write_probe(F["probe"])
    pack.write_class_counts(F["counts"])
    docs.notes(F["notes"])
    docs.shortlist(F["shortlist"])
    docs.defaults(F["defaults"])
    docs.launch(jobs, F["launch"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in WRITTEN.items()})
    return jobs, n


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    jobs, n = run(out)
    print(n)
    for f in sorted(os.listdir(out)):
        print("%10d  %s" % (os.path.getsize(os.path.join(out, f)), f))
