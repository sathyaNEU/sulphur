"""Build task3's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip and golden.zip, then run the checks and the verifier.

    python3 task3/generator/build.py            # full build (two passes, then checks and verify)
    python3 task3/generator/build.py --once     # one pass into the task folder, no comparison
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import ooxml  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

ZSTAMP = (2026, 10, 14, 9, 41, 0)
DISTRACTORS = {
    "usgs_12183450_coyner_r_daily_discharge.csv": "the donor gauge's daily mean flows; looks relevant to the river's floods "
                                                   "but the frequency analysis reads the instantaneous peaks",
    "usgs_12187200_annual_peaks.txt": "a regional gauge's annual peaks (Tarrow River near Brandt, 27 miles away); looks "
                                      "relevant as a donor but the standard takes the nearest gauged basin",
    "usgs_12181650_annual_peaks.txt": "a regional gauge's annual peaks (Gorham Creek near Vesper, 19 miles away)",
    "usgs_12189500_annual_peaks.txt": "a regional gauge's annual peaks (Quillen River at Ashby Falls, 41 miles away)",
    "usgs_12184900_annual_peaks.txt": "a regional gauge's annual peaks (Pinnell Creek near Coe, 34 miles away)",
}
SOURCES = {
    "usgs_12183450_coyner_r_daily_discharge.csv": ("USGS NWIS daily mean discharge, Coyner River near Tessel, WA", "2026-10-14", "distractor"),
    "usgs_12183450_coyner_r_annual_peaks.txt": ("USGS NWIS annual peak streamflow, Coyner River near Tessel, WA", "2026-10-14", "evidence"),
    "usgs_12183450_coyner_r_peaks_above_base.txt": ("USGS Washington Water Science Center partial-duration series, Coyner River near Tessel", "2026-10-14", "evidence"),
    "usgs_12187200_annual_peaks.txt": ("USGS NWIS annual peak streamflow, Tarrow River near Brandt, WA", "2026-10-14", "distractor"),
    "usgs_12181650_annual_peaks.txt": ("USGS NWIS annual peak streamflow, Gorham Creek near Vesper, WA", "2026-10-14", "distractor"),
    "usgs_12189500_annual_peaks.txt": ("USGS NWIS annual peak streamflow, Quillen River at Ashby Falls, WA", "2026-10-14", "distractor"),
    "usgs_12184900_annual_peaks.txt": ("USGS NWIS annual peak streamflow, Pinnell Creek near Coe, WA", "2026-10-14", "distractor"),
    "ghcnd_tessel_daily_1950-2025.csv": ("NOAA NCEI GHCN-Daily daily summaries, Tessel 2 NE and Tessel 3 E cooperative stations", "2026-10-13", "evidence"),
    "ghcnd_durrow_ridge_daily_1950-2025.csv": ("NOAA NCEI GHCN-Daily daily summaries, Durrow Ridge cooperative station", "2026-10-13", "evidence"),
    "lcd_tessel_field_hourly_1950-2025.csv": ("NOAA NCEI Local Climatological Data, hourly observations, Tessel Field Airport (WBAN 24151)", "2026-10-13", "evidence"),
    "snotel_1187_hatchet_meadow_daily.csv": ("USDA NRCS SNOTEL daily report, Hatchet Meadow (1187)", "2026-10-13", "evidence"),
    "snotel_1203_corbel_ridge_daily.csv": ("USDA NRCS SNOTEL daily report, Corbel Ridge (1203)", "2026-10-13", "evidence"),
    "region3_basin_characteristics.xlsx": ("State flood study basin characteristics (Region 3) and the county's delineation of the crossing", "2026-03-19", "evidence"),
    "pelton_county_road_standards_ch7_excerpt.pdf": ("Pelton County Road Design Standards, chapter 7 (excerpt), revision 6", "2026-04-07", "governing"),
    "wsdot_region3_flood_frequency_excerpt.pdf": ("WSDOT WA-RD 891.2, Magnitude and frequency of floods in western Washington, Region 3 excerpt", "2024-05-14", "evidence"),
    "hess_tm_durrow_creek_bridge_span_ratings.pdf": ("Hess Hydraulic Engineering TM 26-118, hydraulic rating of the span alternatives", "2026-09-21", "evidence"),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    scratch = os.path.join(root, "scratch")
    for d in (tgt, gld, scratch):
        os.makedirs(d, exist_ok=True)
    world = W.simulate()
    info = PK.write(world, tgt)
    ooxml.normalize(os.path.join(tgt, "region3_basin_characteristics.xlsx"), dt.datetime(2026, 3, 17, 10, 22),
                    dt.datetime(2026, 3, 19, 16, 4), creator="Pelton County GIS", company="Pelton County")
    maps = {k: PK.basin_map(world, world.basins[k]) for k in range(len(world.basins))}
    eq, rinfo = DC.regional_equations(world, maps)
    DC.county_standard(os.path.join(tgt, "pelton_county_road_standards_ch7_excerpt.pdf"))
    DC.state_report(os.path.join(tgt, "wsdot_region3_flood_frequency_excerpt.pdf"), eq, rinfo)
    DC.consultant_tm(os.path.join(tgt, "hess_tm_durrow_creek_bridge_span_ratings.pdf"))
    A.STATE_B = round(eq[100]["b"], 3)
    R = A.run(tgt, rated=dict(DC.SPANS), equations=eq)
    F = FG.make(R, tgt)
    F["equations"] = {str(T): {k: round(v, 4) for k, v in e.items()} for T, e in eq.items()}
    F["equation_ranges"] = {"area": [round(x, 1) for x in rinfo["area"]], "map": [round(x, 0) for x in rinfo["map"]],
                            "n": rinfo["n"]}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1)
    GD.write(F, gld, scratch)
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    meta = {"task": "task3", "architecture": 6, "as_of": "2026-11-06",
            "decision": "which span (140, 185 or 240 ft) Pelton County builds for the Durrow Creek bridge on Ransom Bar Road",
            "deliverables": ["durrow_creek_bridge_hydrology_report.pdf", "durrow_creek_estimated_annual_peaks.csv"],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["%d" % q for _, q in DC.SPANS] + ["{:,}".format(q) for _, q in DC.SPANS]
                             + [str(sp) for sp, _ in DC.SPANS] + ["12183450"],
            "rows": {k: v for k, v in info.items() if k != "maps"},
            "files": {n: {"source": s, "date": d, "role": r,
                          "license": "synthetic, CC0, generated for this task by task3/generator (a seeded hydrometeorological simulation)"}
                      for n, (s, d, r) in sorted(SOURCES.items())}}
    json.dump(meta, open(os.path.join(root, "metadata.json"), "w"), indent=1)
    shutil.rmtree(scratch)
    return F


def zipdir(folder, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=ZSTAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())


def hashes(root):
    out = {}
    for sub in ("target", "golden"):
        for f in sorted(os.listdir(os.path.join(root, sub))):
            out["%s/%s" % (sub, f)] = sha(os.path.join(root, sub, f))
    for f in ("figures.json", "submission.md", "metadata.json"):
        out[f] = sha(os.path.join(root, f))
    return out


def install(root):
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(root, sub), dst)
    shutil.copy(os.path.join(root, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(root, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.copy(os.path.join(root, "metadata.json"), os.path.join(TASK, "metadata.json"))
    zipdir(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    zipdir(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"))


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
    print("target.zip", sha(os.path.join(TASK, "target.zip"))[:16], "golden.zip", sha(os.path.join(TASK, "golden.zip"))[:16])
    if not once:
        for script in ("checks.py", "verify.py"):
            r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True)
            print(r.stdout[-5000:])
            if r.returncode != 0:
                print(r.stderr[-3000:])
                sys.exit(r.returncode)


if __name__ == "__main__":
    main()
