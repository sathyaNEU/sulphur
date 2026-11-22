"""Build target/: materialize pack files from core.py, export PDFs via LibreOffice Writer, normalize all XLSX
containers via postprocess.normalize_ooxml, and stamp each file with a distinct issuer mtime <= as_of (2027-01-20).

    python3 task26/generator/build.py                 -> writes task26/target/
    python3 task26/generator/build.py --out <folder>  -> writes into <folder> (used by gates.py rebuild check)
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import docs  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc
F = PK.FILES

EXPORTED = {
    F["scada_sub"]:  dt.datetime(2027, 1, 12,  4, 38, 14, tzinfo=UTC),
    F["gsp_v"]:      dt.datetime(2027, 1, 12,  4, 52, 29, tzinfo=UTC),
    F["cor_lines"]:  dt.datetime(2026, 11, 12, 10, 41, 15, tzinfo=UTC),
    F["scada_fdr"]:  dt.datetime(2027, 1, 12,  5, 19, 42, tzinfo=UTC),
    F["fdr_m15"]:    dt.datetime(2027, 1,  8, 10, 14, 27, tzinfo=UTC),
    F["bus_vph"]:    dt.datetime(2027, 1, 12,  6,  4, 51, tzinfo=UTC),
    F["ami_db"]:     dt.datetime(2027, 1, 14,  9, 47, 19, tzinfo=UTC),
    F["ref_pq"]:     dt.datetime(2027, 1, 13, 14, 23,  8, tzinfo=UTC),
    F["ref_tracer"]: dt.datetime(2025, 12,  5, 15, 11, 33, tzinfo=UTC),
    F["gis_lat"]:    dt.datetime(2026, 12, 18, 11, 42,  6, tzinfo=UTC),
    F["xwalk"]:      dt.datetime(2024,  9, 16,  8, 27, 55, tzinfo=UTC),
    F["class_pf"]:   dt.datetime(2024,  4, 11, 13,  9, 17, tzinfo=UTC),
    F["dist_light"]: dt.datetime(2027, 1,  7, 12, 31, 49, tzinfo=UTC),
    F["dist_dga"]:   dt.datetime(2026, 11, 27, 16,  5, 22, tzinfo=UTC),
}

OFFICE = [
    (F["rev_xlsx"], PK.PEOPLE["metering"], PK.PEOPLE["metering"],
     "2027-01-06T08:12:00Z", "2027-01-11T13:44:18Z", PK.ORG),
    (F["tx_xlsx"], PK.PEOPLE["asset"], PK.PEOPLE["asset"],
     "2025-02-19T09:30:00Z", "2026-11-12T10:26:41Z", PK.ORG),
    (F["ctx_2025"], PK.PEOPLE["analyst"], PK.PEOPLE["head"],
     "2026-02-09T10:05:00Z", "2026-02-14T15:18:32Z", PK.ORG),
]


def build(target, world=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    counts = PK.build(target, world=world)
    docs.write_all(target)
    for name, creator, last, created, modified, company in OFFICE:
        postprocess.normalize_ooxml(os.path.join(target, name), creator, last, created, modified,
                                    excel=True, company=company)
    postprocess.own_mtimes(target, EXPORTED)
    return counts


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    counts = build(out)
    print(counts)
    for name in sorted(os.listdir(out)):
        print("%10d  %s" % (os.path.getsize(os.path.join(out, name)), name))
