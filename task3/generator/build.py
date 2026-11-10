"""Build task3's pack, goldens, figures.json, effort.json, submission.md and metadata.json twice, require byte-identical
output, install them and cut target.zip and golden.zip.

    python3 task3/generator/build.py            # full build (two passes)
    python3 task3/generator/build.py --once     # one pass into the task folder, no comparison
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile

import numpy as np

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
SAVED = {
    A.F_HOURLY: (2026, 11, 2, 9, 12, 41),
    A.F_HL: (2026, 11, 2, 9, 15, 8),
    A.F_HLP: (2026, 11, 2, 9, 17, 33),
    A.F_MONTHLY: (2026, 11, 2, 9, 18, 52),
    A.F_DATUMS: (2026, 11, 2, 9, 20, 15),
    A.F_RIVER: (2026, 11, 2, 9, 31, 47),
    A.F_LOG["marsh"]: (2024, 11, 22, 14, 6, 19),
    A.F_LOG["oyster"]: (2025, 10, 31, 10, 44, 2),
    A.F_LOG["river"]: (2025, 4, 21, 15, 27, 36),
    A.F_SENSOR: (2026, 11, 3, 11, 2, 58),
    A.F_RAIN: (2026, 11, 3, 11, 40, 12),
    A.F_311: (2026, 11, 4, 16, 21, 5),
    A.F_SLR: (2026, 8, 19, 13, 55, 40),
    A.F_INV: (2026, 10, 2, 10, 37, 27),
    A.F_GUIDE: (2026, 10, 16, 9, 14, 37),
    GD.XLSX: (2026, 11, 10, 8, 47, 51),
    GD.MEMO: (2026, 11, 10, 8, 52, 14),
}
DISTRACTORS = {
    A.F_311: "the city's 311 service requests 2023-2026: street flooding reports beside potholes and clogged inlets; they look "
             "like an observed flood count but residents report a fraction of daytime floods and almost none at night",
    A.F_SLR: "long-range relative sea level scenarios to 2100 for the gauge; they look like the sea level for the tide year but "
             "the program fixes the planning value",
    A.F_RAIN: "the airport's daily rainfall and temperature; it looks needed to separate rain ponding from tidal water on "
              "Front Street, which the harbor's high waters already separate",
}
SOURCES = {
    A.F_HOURLY: ("NOAA CO-OPS water levels page export, verified and preliminary hourly heights with predictions, station 8673718", "evidence"),
    A.F_HL: ("NOAA CO-OPS verified high and low waters, station 8673718", "evidence"),
    A.F_HLP: ("NOAA CO-OPS high and low tide predictions, station 8673718", "evidence"),
    A.F_MONTHLY: ("NOAA CO-OPS monthly means, station 8673718", "evidence"),
    A.F_DATUMS: ("NOAA CO-OPS datums page, station 8673718 (1983-2001 epoch)", "evidence"),
    A.F_RIVER: ("USGS NWIS daily mean discharge, Brayle River near Hensley, GA (02203560)", "evidence"),
    A.F_LOG["marsh"]: ("City logger campaign export (vented pressure logger), Marsh Road at Pellam Creek, Sep-Nov 2024", "evidence"),
    A.F_LOG["oyster"]: ("City logger campaign export, Oyster Creek Road, Aug-Oct 2025", "evidence"),
    A.F_LOG["river"]: ("City logger campaign export, River Road at Hensley Landing, Jan-Apr 2025", "evidence"),
    A.F_SENSOR: ("City ultrasonic street sensor PT-FRONT-01 export, Front Street at Ferry Lane", "evidence"),
    A.F_RAIN: ("NOAA NCEI GHCN-Daily, Port Tolliver Municipal Airport", "distractor"),
    A.F_311: ("City 311 service requests export", "distractor"),
    A.F_SLR: ("Relative sea level scenarios for the gauge (interagency 2022 framework)", "distractor"),
    A.F_INV: ("Port Tolliver Stormwater Utility tidal low point inventory export", "evidence"),
    A.F_GUIDE: ("Port Tolliver Stormwater Utility, FY2028 tide valve round guidelines", "governing"),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def stamp_saves(folder):
    from zoneinfo import ZoneInfo
    for f in os.listdir(folder):
        t = dt.datetime(*SAVED[f], tzinfo=ZoneInfo(ZONE)).timestamp()
        os.utime(os.path.join(folder, f), (t, t))


def write_pack(S, tgt):
    rows = {}
    rows[A.F_HL] = PK.write_hilo(os.path.join(tgt, A.F_HL), S, "obs")
    rows[A.F_HLP] = PK.write_hilo(os.path.join(tgt, A.F_HLP), S, "pred")
    rows[A.F_HOURLY] = PK.write_hourly(os.path.join(tgt, A.F_HOURLY), S)
    rows[A.F_MONTHLY] = PK.write_monthly(os.path.join(tgt, A.F_MONTHLY), S)
    PK.write_datums(os.path.join(tgt, A.F_DATUMS), S)
    rows[A.F_RIVER] = PK.write_river(os.path.join(tgt, A.F_RIVER), S)
    for site, sn, title in (("marsh", "21187431", "PEL-MR-24"), ("oyster", "21187433", "OYS-CR-25"), ("river", "21187432", "HEN-RR-25")):
        rows[A.F_LOG[site]] = PK.write_logger(os.path.join(tgt, A.F_LOG[site]), S, site, sn, title)
    days = np.arange(np.datetime64("2023-01-01"), np.datetime64("2026-11-01"))
    pr = PK.rainfall(days)
    rows[A.F_RAIN] = PK.write_rain(os.path.join(tgt, A.F_RAIN), days, pr)
    rows[A.F_SENSOR] = PK.write_sensor(os.path.join(tgt, A.F_SENSOR), S, days, pr)
    rows[A.F_311] = PK.write_311(os.path.join(tgt, A.F_311), S, days, pr)
    rows[A.F_SLR] = PK.write_slr(os.path.join(tgt, A.F_SLR))
    DC.inventory(os.path.join(tgt, A.F_INV))
    PP.normalize_ooxml(os.path.join(tgt, A.F_INV), "Port Tolliver Stormwater Utility", "Port Tolliver Stormwater Utility",
                       "2026-09-29T13:12:00Z", "2026-10-02T14:37:27Z", excel=True, company="City of Port Tolliver")
    DC.guidelines(os.path.join(tgt, A.F_GUIDE))
    return rows


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    for d in (tgt, gld):
        os.makedirs(d, exist_ok=True)
    S = W.simulate()
    rows = write_pack(S, tgt)
    R = A.run(tgt)
    F, E = FG.write(R, root)
    inv = A.read_inventory(tgt)
    lane = {k: v["lane"] for k, v in inv.items()}
    GD.workbook(F, lane, os.path.join(gld, GD.XLSX))
    PP.normalize_ooxml(os.path.join(gld, GD.XLSX), "Cheryl Olsen", "Cheryl Olsen", "2026-11-09T19:02:00Z",
                       "2026-11-10T13:47:51Z", excel=True, company="City of Port Tolliver")
    GD.memo(F, lane, os.path.join(gld, GD.MEMO))
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    meta = {"task": "task3", "architecture": 7, "as_of": "2026-11-10",
            "decision": "which two of Port Tolliver's five tidal low points get the FY2028 tide valves",
            "deliverables": [GD.XLSX, GD.MEMO],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["0.70", "8.6", "8673718", "02203560", "2027", "2028", "2025", "2026", "1990", "2001", "1983"],
            "field_terms": [],
            "rows": rows,
            "files": {n: {"source": s, "role": r, "pull_date": dt.date(*SAVED[n][:3]).isoformat(),
                          "license": "synthetic, CC0, generated for this task by task3/generator (a seeded tide, sea level, "
                                     "surge, river and low point simulation)"} for n, (s, r) in sorted(SOURCES.items())}}
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
    for sub, z in (("target", "target.zip"), ("golden", "golden.zip")):
        stamp_saves(os.path.join(TASK, sub))
        PP.zip_folder(os.path.join(TASK, sub), os.path.join(TASK, z), zone=ZONE)


def main():
    once = "--once" in sys.argv
    a = tempfile.mkdtemp(prefix="task3a-")
    build_into(a)
    if not once:
        b = tempfile.mkdtemp(prefix="task3b-")
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
