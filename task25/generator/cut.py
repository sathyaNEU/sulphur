"""Cut target.zip and golden.zip from the final build: every file at its own save time (a container's own stamp, an
export's pull time), entries in path order in Helsinki clock, so two cuts of the same build are byte-identical."""
import datetime as dt
import hashlib
import os
import sys
import zipfile
from zoneinfo import ZoneInfo

import postprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
UTC = dt.timezone.utc
EXPORT = {   # the pull of 6 November 2026 (UTC), one export at a time; the plan inputs at their own saves
    "run_registry_2026.csv": dt.datetime(2026, 11, 6, 7, 41, 12, tzinfo=UTC),
    "step_log_2026.csv": dt.datetime(2026, 11, 6, 7, 52, 48, tzinfo=UTC),
    "interruptions_2026.csv": dt.datetime(2026, 11, 6, 7, 44, 5, tzinfo=UTC),
    "node_allocations_2026.csv": dt.datetime(2026, 11, 6, 7, 46, 33, tzinfo=UTC),
    "rank_step_samples_2026.csv": dt.datetime(2026, 11, 6, 8, 3, 17, tzinfo=UTC),
    "packing_manifests_2026.jsonl": dt.datetime(2026, 11, 6, 8, 9, 54, tzinfo=UTC),
    "node_states_2026.csv": dt.datetime(2026, 11, 6, 8, 17, 26, tzinfo=UTC),
    "hall_it_load_2026.csv": dt.datetime(2026, 11, 5, 14, 2, 41, tzinfo=UTC),
    "work_orders_2025_2026.csv": dt.datetime(2026, 11, 5, 14, 5, 9, tzinfo=UTC),
    "incident_log_2026.csv": dt.datetime(2026, 11, 5, 14, 6, 52, tzinfo=UTC),
    "tpbench_results.csv": dt.datetime(2026, 10, 30, 16, 22, 3, tzinfo=UTC),
    "tpbench_harness.yaml": dt.datetime(2026, 9, 18, 11, 7, 45, tzinfo=UTC),
    "doc_length_sample.csv": dt.datetime(2026, 10, 21, 13, 48, 30, tzinfo=UTC),
    "data_mixes.csv": dt.datetime(2026, 10, 23, 9, 15, 2, tzinfo=UTC),
    "checkpoint_evals_2026.csv": dt.datetime(2026, 11, 2, 10, 30, 19, tzinfo=UTC),
}


def config_times(folder):
    out = {}
    for i, name in enumerate(sorted(os.listdir(folder))):
        out[name] = dt.datetime(2026, 10, 27, 9, 0, tzinfo=UTC) + dt.timedelta(hours=7 * i + 3, minutes=13 * i, seconds=17 * i + 5)
    return out


def own_stamp(p):
    """A container's own last-save stamp (a workbook's modified time, a PDF's modification date)."""
    import re
    if p.endswith(".xlsx"):
        with zipfile.ZipFile(p) as z:
            core = z.read("docProps/core.xml").decode()
        m = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core)
        return dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    if p.endswith(".pdf"):
        b = open(p, "rb").read()
        m = re.search(rb"/ModDate\s*\(D:(\d{14})", b) or re.search(rb"/CreationDate\s*\(D:(\d{14})", b)
        return dt.datetime.strptime(m.group(1).decode(), "%Y%m%d%H%M%S").replace(tzinfo=UTC)
    return None


def stamp_tree(root):
    seen = set()
    for dp, dirs, files in os.walk(root):
        fb = config_times(dp) if os.path.basename(dp) == "configs" else EXPORT
        for f in files:
            p = os.path.join(dp, f)
            st = own_stamp(p) or fb.get(f)
            assert st is not None, "no stamp for %s" % p
            assert st not in seen, "two files share a save time: %s" % p
            seen.add(st)
            os.utime(p, (st.timestamp(), st.timestamp()))


def zip_tree(root, out, zone="Europe/Helsinki"):
    tz = ZoneInfo(zone)
    paths = []
    for dp, _, files in os.walk(root):
        for f in files:
            paths.append(os.path.relpath(os.path.join(dp, f), root))
    with zipfile.ZipFile(out, "w") as z:
        for rel in sorted(paths):
            p = os.path.join(root, rel)
            t = dt.datetime.fromtimestamp(os.path.getmtime(p), UTC).astimezone(tz)
            zi = zipfile.ZipInfo(rel, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zi.create_system = 3
            z.writestr(zi, open(p, "rb").read())


def digest(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def main():
    target = os.path.join(TASK, "target")
    golden = os.path.join(TASK, "golden")
    stamp_tree(target)
    postprocess.own_mtimes(golden, {"h1_2027_run_windows_note.md": dt.datetime(2026, 11, 6, 15, 31, 4, tzinfo=UTC)})
    zip_tree(target, os.path.join(TASK, "target.zip"))
    postprocess.zip_folder(golden, os.path.join(TASK, "golden.zip"), zone="Europe/Helsinki")
    print("target.zip", digest(os.path.join(TASK, "target.zip")), "golden.zip", digest(os.path.join(TASK, "golden.zip")))


if __name__ == "__main__":
    main()
