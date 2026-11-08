"""Build task5: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
compared byte for byte, and target.zip and golden.zip cut from the final build.

    python3 task5/generator/build.py              everything
    python3 task5/generator/build.py --fast       one build with the checks, no second build or zips
    python3 task5/generator/build.py --out DIR    the pack and golden only, into DIR/target and DIR/golden
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import docs as D          # noqa: E402
import golden as G        # noqa: E402
import pack as P          # noqa: E402
import postprocess as PP  # noqa: E402
import sim                # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = {   # each file's date as its source wrote it (local time)
    "reports": dt.datetime(2027, 2, 16, 6, 12), "accounts": dt.datetime(2027, 2, 16, 6, 14),
    "status": dt.datetime(2027, 2, 16, 6, 15), "worksites": dt.datetime(2027, 2, 16, 6, 18),
    "counties": dt.datetime(2024, 7, 1, 10, 2), "naics": dt.datetime(2023, 3, 15, 15, 40),
    "act": dt.datetime(2026, 5, 6, 9, 41), "agreement": dt.datetime(2025, 6, 20, 14, 3),
    "request": dt.datetime(2027, 1, 12, 10, 14), "published": dt.datetime(2026, 9, 10, 8, 55),
    "rates": dt.datetime(2026, 11, 30, 8, 30), "population": dt.datetime(2026, 6, 26, 16, 20),
}
GOLDEN_CSV_STAMP = dt.datetime(2027, 2, 26, 16, 8)       # the employer list, written after the workbook's last save
ZONE = "America/New_York"


def _local(when):
    from zoneinfo import ZoneInfo
    return when.replace(tzinfo=ZoneInfo(ZONE))


def build_into(root, quiet=False):
    target, gold = os.path.join(root, "target"), os.path.join(root, "golden")
    for d in (target, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    w = sim.build()
    T = P.tables(w)
    n = P.write_pack(w, T, target)
    f = lambda k: os.path.join(target, W.FILES[k])
    texts = {"act": D.write_act(f("act")), "agreement": D.write_agreement(f("agreement")),
             "request": D.write_request(f("request"))}
    D.write_rates(f("rates"))
    PP.normalize_ooxml(f("published"), "Labor Market Information", "Labor Market Information", "2026-09-08T19:41:00Z",
                       "2026-09-10T13:55:00Z", title="Covered Employment and Wages by County, 2025 Q4", excel=True,
                       company="Franklin Department of Labor")
    # each file's mtime its own last save: an office file's from its container, an export's from the system that wrote it
    PP.own_mtimes(target, {W.FILES[k]: _local(STAMP[k]) for k in W.FILES
                           if not W.FILES[k].endswith((".xlsx", ".docx", ".pptx", ".pdf"))})
    pk, Gd = G.build(target, gold)
    for k in W.DELIVERABLES:
        p = os.path.join(gold, W.DELIVERABLES[k])
        if p.endswith(".xlsx"):
            PP.normalize_ooxml(p, W.PEOPLE["lmi_director"][0], W.PEOPLE["lmi_director"][0], "2027-02-24T15:12:00Z",
                               "2027-02-26T21:05:00Z", title="CTF 2027 certification of December covered employment",
                               excel=True, company="Franklin Department of Labor")
    PP.own_mtimes(gold, {W.DELIVERABLES["employers"]: _local(GOLDEN_CSV_STAMP)})
    if not quiet:
        print("built %s: %s" % (root, ", ".join("%s %d" % kv for kv in n.items())))
    return w, T, pk, Gd, texts, n


def digest(folder):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(folder)):
        h.update(fn.encode())
        h.update(open(os.path.join(folder, fn), "rb").read())
    return h.hexdigest()


def zip_folder(folder, path):
    """the house cut (postprocess.zip_folder): entries in name order, each at its file's own save time on the
    sender's clock"""
    PP.zip_folder(folder, path, zone=ZONE)
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        build_into(a.out)
        return
    w, T, pk, Gd, texts, n = build_into(TASK)
    import writeup as WR
    figs = WR.write(TASK, w, T, pk, Gd, n)
    import metadata as MD
    MD.write(TASK, n)
    import checks as C
    ok = C.run(TASK, w, T, pk, Gd, texts, figs, n)
    import verify as V
    vok = V.main(TASK)
    if a.fast:
        sys.exit(0 if ok and vok else 1)
    scratch = os.path.join(TASK, ".rebuild")
    build_into(scratch, quiet=True)
    same = digest(os.path.join(TASK, "target")) == digest(os.path.join(scratch, "target")) and \
        digest(os.path.join(TASK, "golden")) == digest(os.path.join(scratch, "golden"))
    shutil.rmtree(scratch)
    print("byte-identical rebuild:", "PASS" if same else "FAIL")
    tz = zip_folder(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    gz = zip_folder(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"))
    print("target.zip %s  golden.zip %s" % (tz, gz))
    sys.exit(0 if ok and vok and same else 1)


if __name__ == "__main__":
    main()
