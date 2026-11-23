"""Build task27/target/: materialize all 17 pack files from core.py, export Charter RC-2027 PDF via
LibreOffice Writer (officepdf.py), normalize all XLSX containers via postprocess.normalize_ooxml,
and stamp every file with a distinct issuer mtime <= as_of (2027-01-19).

    python3 task27/generator/build.py                 -> writes task27/target/
    python3 task27/generator/build.py --out <folder>  -> writes into <folder> (for gates.py rebuild check)
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "reduce-house-fixes", "scripts", "writers"))

import postprocess  # noqa: E402
import docs  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc
F = PK.FILES

# Distinct realistic system export timestamps strictly <= as_of (2027-01-19)
EXPORTED = {
    F["milestones"]:   dt.datetime(2027, 1, 14,  5, 18, 22, tzinfo=UTC),
    F["pallets"]:      dt.datetime(2027, 1, 13,  4, 42, 11, tzinfo=UTC),
    F["turnin"]:       dt.datetime(2027, 1, 14,  6,  9, 47, tzinfo=UTC),
    F["port_yard"]:    dt.datetime(2027, 1, 11,  8, 15, 34, tzinfo=UTC),
    F["dc_inv"]:       dt.datetime(2027, 1, 13,  7, 31, 56, tzinfo=UTC),
    F["chambers"]:     dt.datetime(2026, 12, 19, 10, 12, 40, tzinfo=UTC),
    F["skus"]:         dt.datetime(2026, 12, 22, 14, 27, 19, tzinfo=UTC),
    F["consignments"]: dt.datetime(2027, 1, 12,  9, 44,  5, tzinfo=UTC),
    F["bip_notices"]:  dt.datetime(2027, 1, 12, 11, 23, 51, tzinfo=UTC),
    F["shuttles"]:     dt.datetime(2027, 1, 12, 16,  8, 13, tzinfo=UTC),
    F["portal"]:       dt.datetime(2027, 1, 19,  6, 42, 18, tzinfo=UTC),
    F["budgets_2027"]: dt.datetime(2026, 11, 25, 13, 36, 44, tzinfo=UTC),
    F["crosswalk"]:    dt.datetime(2026,  9, 18, 11,  5, 17, tzinfo=UTC),
    F["dist_bunker"]:  dt.datetime(2027, 1,  8, 15, 19,  3, tzinfo=UTC),
}

OFFICE = [
    (
        F["disputes"],
        PK.PEOPLE["controlling"],
        PK.PEOPLE["procurement"],
        "2027-01-09T09:14:00Z",
        "2027-01-12T14:51:26Z",
        PK.ORG,
    ),
    (
        F["dist_maut"],
        PK.PEOPLE["drayage"],
        PK.PEOPLE["drayage"],
        "2026-10-14T10:08:00Z",
        "2026-12-04T16:22:19Z",
        PK.ORG,
    ),
]


def build(target, world=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    counts = PK.build(target, world=world)
    docs.write_all(target)
    for name, creator, last_by, created, modified, company in OFFICE:
        postprocess.normalize_ooxml(
            os.path.join(target, name),
            creator,
            last_by,
            created,
            modified,
            excel=True,
            company=company,
        )
    postprocess.own_mtimes(target, EXPORTED)
    return counts


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    counts = build(out)
    print(counts)
    for name in sorted(os.listdir(out)):
        print("%10d  %s" % (os.path.getsize(os.path.join(out, name)), name))
