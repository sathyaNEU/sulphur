"""Build task3 architecture 5: the pack into <task>/target, the goldens into <task>/golden, submission.md,
metadata.json and generator/figures.json, then the checks and the independent verifier, then a second build into a
scratch folder (removed after) compared byte for byte, then target.zip and golden.zip.

    python3 task3/generator/build.py
"""
import calendar
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K    # noqa: E402
import pack as PK     # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = dt.datetime(2026, 1, 8, 9, 30)
MTIME = calendar.timegm(STAMP.timetuple())


def build_pack(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w, n = PK.write_pack(out)
    _fix_ooxml(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return w, n


def _fix_ooxml(d):
    """Re-pack every docx and xlsx with fixed entry times and order, so a rebuild is byte-identical."""
    for f in sorted(os.listdir(d)):
        if not f.endswith((".docx", ".xlsx")):
            continue
        p = os.path.join(d, f)
        with zipfile.ZipFile(p) as z:
            items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
        os.remove(p)
        with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in items:
                if name == "docProps/core.xml" and f.endswith(".xlsx"):
                    import re
                    txt = data.decode("utf-8")
                    txt = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>2026-01-06T08:12:00Z\2", txt)
                    txt = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>2026-01-06T08:12:00Z\2", txt)
                    data = txt.encode("utf-8")
                if name == "docProps/app.xml":
                    import re
                    txt = data.decode("utf-8")
                    txt = re.sub(r"<Application>[^<]*</Application>", "<Application>Microsoft Excel</Application>"
                                 if f.endswith(".xlsx") else "<Application>Microsoft Office Word</Application>", txt)
                    txt = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0300</AppVersion>", txt)
                    data = txt.encode("utf-8")
                zi = zipfile.ZipInfo(name, date_time=(2026, 1, 8, 9, 30, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, data)


def build_golden(target, golden):
    import analysis as AN
    import deliver as D
    import writeup as WU
    g = AN.Golden(target)
    R = g.run()
    rungs, fam = g.rivals()
    sound = [v[0] for k, v in fam.items()]
    F = D.figures(R, (min(sound), max(sound)), max(list(rungs.values()) + [max(R["ann"])]))
    text, F = WU.write(R, F)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    D.write_docx(os.path.join(golden, K.DOCX_OUT), R, F)
    D.write_csv(os.path.join(golden, K.CSV_OUT), R)
    _fix_ooxml(golden)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return R, F


def write_metadata(n, R):
    about = {
        "flow": ("the creek gauge's daily mean discharge, water years 1956 to 2025 and the provisional months after", "2026-01-05"),
        "peaks": ("the creek gauge's annual peak flows by water year, 1956 to 2025", "2026-01-05"),
        "pot": ("the creek gauge's listing of every independent peak above its 50 cfs base, 1956 to 2025", "2026-01-05"),
        "rain": ("the county rain gauge's daily readings, October 1955 to December 2025", "2026-01-06"),
        "parcels": ("the county stormwater utility's billing parcels with impervious area and the year built", "2026-01-06"),
        "standard": ("the county drainage standard, section 4 (culverts and bridges on county roads), 2017", "2026-01-06"),
        "options": ("the roads division's three culvert alternatives for Kinnard Road, December 2025", "2026-01-06"),
        "inspection": ("the 2024 inspection of the existing Kinnard Road culvert", "2026-01-06"),
        "survey": ("the 2023 cross sections of the Kinnard Road reach", "2026-01-06"),
        "quality": ("the county's grab samples at Kinnard Road, 2019 to 2025", "2026-01-06"),
    }
    synth = ("constructed by the task generator (seeded); Tamsett County, Ollery Creek and every record are fictional")
    prov = {K.FILES[k]: {"source": synth, "covers": about[k][0], "date": about[k][1],
                         "licence": "CC0 1.0 (constructed for this task)", "made": "generated by task3/generator"}
            for k in K.FILES}
    m = {"task": "task3", "architecture": 5,
         "title": "Tamsett County: which culvert carries Kinnard Road over Ollery Creek's design flood",
         "domain": "Physical & Environmental Sciences", "objective": "Forecasting & Predictive Modeling",
         "decision": "which of three costed box culverts passes the 1 per cent flood of its first ten years of service",
         "answer": "Alternative %s" % R["pick"][0],
         "deliverables": [K.DOCX_OUT, K.CSV_OUT],
         "distractor_files": ["target/" + K.FILES[k] for k in ("flow", "inspection", "survey", "quality")],
         "stated_inputs": ["{:,}".format(c[2]) for c in K.CULVERTS],
         "rows": n, "provenance": prov}
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")


def digest(d):
    return {f: hashlib.md5(open(os.path.join(d, f), "rb").read()).hexdigest() for f in sorted(os.listdir(d))}


def cut_zip(src, path, prefix):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(prefix + f, date_time=STAMP.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src, f), "rb").read())


def main():
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    w, n = build_pack(target)
    R, F = build_golden(target, golden)
    write_metadata(n, R)
    import checks
    rc = checks.main(target)
    import verify
    bad = verify.run(TASK)
    print("verify: %s" % ("PASS" if not bad else "FAIL\n  " + "\n  ".join(bad)))
    scratch = os.path.join(TASK, ".rebuild")
    build_pack(os.path.join(scratch, "target"))
    g1 = digest(golden)
    build_golden(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    same = digest(target) == digest(os.path.join(scratch, "target")) and g1 == digest(os.path.join(scratch, "golden"))
    shutil.rmtree(scratch)
    build_golden(target, golden)
    print("rebuild: %s" % ("byte-identical" if same else "DIFFERS"))
    cut_zip(target, os.path.join(TASK, "target.zip"), "target/")
    cut_zip(golden, os.path.join(TASK, "golden.zip"), "")
    for f, v in digest(target).items():
        print("  %s  %s" % (v, f))
    for f in ("target.zip", "golden.zip"):
        print("  %s  %s" % (hashlib.md5(open(os.path.join(TASK, f), "rb").read()).hexdigest(), f))
    sys.exit(1 if (rc or bad or not same) else 0)


if __name__ == "__main__":
    main()
