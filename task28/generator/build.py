#!/usr/bin/env python3
"""Build task28/target/: materialize all 14 files from core.py, export PDFs via LibreOffice Writer,
normalize XLSX containers via postprocess.normalize_ooxml, and stamp each file with a distinct
issuer mtime <= as_of (2027-01-18).

    python3 task28/generator/build.py                 -> writes task28/target/
    python3 task28/generator/build.py --out <folder>  -> writes into <folder> (used by gates.py rebuild check)
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    ".agents",
    "skills",
    "reduce-house-fixes",
    "scripts",
    "writers",
)
sys.path.insert(0, HERE)
sys.path.insert(0, WRITERS)
import docs  # noqa: E402
import pack as PK  # noqa: E402
import postprocess  # noqa: E402

UTC = dt.timezone.utc
F = PK.FILES

EXPORTED = {
    F["asset_reg"]:    dt.datetime(2026, 11, 18,  9, 14, 22, tzinfo=UTC),
    F["op_plan"]:      dt.datetime(2026, 12,  4, 14, 27, 45, tzinfo=UTC),
    F["autosampler"]:  dt.datetime(2027,  1,  5,  8, 36, 19, tzinfo=UTC),
    F["boron_comp"]:   dt.datetime(2027,  1,  9, 11, 22, 41, tzinfo=UTC),
    F["intake_15m"]:   dt.datetime(2027,  1, 11,  6, 15,  8, tzinfo=UTC),
    F["ro_feed_15m"]:  dt.datetime(2027,  1, 11,  6, 48, 33, tzinfo=UTC),
    F["hydraulics_h"]: dt.datetime(2027,  1, 11,  7, 19, 54, tzinfo=UTC),
    F["bay_tds_h"]:    dt.datetime(2027,  1, 11,  7, 52, 16, tzinfo=UTC),
    F["shift_diag"]:   dt.datetime(2027,  1, 12, 10,  4, 17, tzinfo=UTC),
    F["cip_log"]:      dt.datetime(2027,  1, 12, 15, 42,  9, tzinfo=UTC),
    F["scada_cfg"]:    dt.datetime(2026, 10, 21, 13,  8, 51, tzinfo=UTC),
    F["dist_mibel"]:   dt.datetime(2027,  1,  6, 16, 33, 28, tzinfo=UTC),
}

OFFICE = [
    (
        F["dist_reservoir"],
        PK.PEOPLE["analyst"],
        PK.PEOPLE["analyst"],
        "2027-01-04T09:11:00Z",
        "2027-01-07T14:52:16Z",
        PK.ORG,
    ),
]


def build(target, world=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    counts = PK.build(target, world=world)
    docs.write_all(target)
    for name, creator, last, created, modified, company in OFFICE:
        postprocess.normalize_ooxml(
            os.path.join(target, name),
            creator,
            last,
            created,
            modified,
            excel=True,
            company=company,
        )
    postprocess.own_mtimes(target, EXPORTED)
    return counts


if __name__ == "__main__":
    out = (
        sys.argv[sys.argv.index("--out") + 1]
        if "--out" in sys.argv
        else os.path.join(os.path.dirname(HERE), "target")
    )
    counts = build(out)
    print(counts)
    for name in sorted(os.listdir(out)):
        print("%10d  %s" % (os.path.getsize(os.path.join(out, name)), name))
