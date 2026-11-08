"""Build task6: the evidence pack into <task>/target, the goldens into <task>/golden, submission.md, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task6/generator/build.py                everything
    python3 task6/generator/build.py --out DIR      the pack only, into DIR
    python3 task6/generator/build.py --golden-only  the goldens, figures, submission and metadata from the shipped
                                                    pack: target/ is unpacked from target.zip (never rebuilt), checked
                                                    member by member against it, the goldens built twice and compared
                                                    byte for byte, golden.zip cut; target.zip is left as shipped

The --golden-only path exists because a repair of the ask layer must not move the shipped pack: the pack's simulation
reads scipy's root finder and numpy's generators, and a later library build moves a handful of rows in the span export
and the July to December balancer file, so a rebuild in another environment is not the shipped cut."""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402
import zipfile       # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import pack as PK          # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())


def build_pack(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w, n, truths = PK.write_pack(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("slo"), K.PEOPLE["head"], K.PEOPLE["head"], "2025-11-20T10:12:00Z", "2025-12-09T16:41:00Z",
                       title="PR-SLO-3 Service level objectives for internal services")
    PP.normalize_ooxml(p("catalogue"), K.PEOPLE["sre"], K.PEOPLE["sre"], "2025-02-03T09:20:00Z",
                       "2026-12-18T11:05:00Z", excel=True)
    PP.normalize_ooxml(p("feedback"), "Customer Communications", "Customer Communications", "2027-01-05T08:44:00Z",
                       "2027-01-05T08:44:00Z", excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return w, n, truths


def build_golden(target, golden):
    import analysis as A
    import deliver as D
    import writeup as WU
    R = A.Golden(target).run()
    F = D.figures(R)
    text, F = WU.write(R, F)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    D.write_docx(os.path.join(golden, K.DOCX_OUT), R, F)
    D.write_csv(os.path.join(golden, K.CSV_OUT), R, F)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(os.path.join(golden, K.DOCX_OUT), K.PEOPLE["sre"], K.PEOPLE["head"], "2027-01-07T09:12:00Z",
                       "2027-01-08T15:26:00Z", title="Reliability review 2026: latency objectives")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return R, F


def write_metadata(n, R):
    if n is None:                      # the shipped pack: its row counts stand as recorded
        old = json.load(open(os.path.join(TASK, "metadata.json")))
        n = {K.FILES_KEY_OF[f]: c for f, c in old["rows"]}
    synth = ("constructed by the task generator (seeded); Rotalinha, its services, staff, systems and every record are "
             "fictional")
    about = {
        "spans": ("the tracing store's span export for December 2026", "2027-01-01"),
        "lb_h1": ("the load balancer's hourly request counts by target group, January to June 2026", "2026-07-02"),
        "lb_h2": ("the load balancer's hourly request and 5xx counts by target group, July to December 2026",
                  "2027-01-02"),
        "slo": ("PR-SLO-3, the platform's service level objectives standard, version 3.1", "2025-12-09"),
        "catalogue": ("the platform's service catalogue", "2026-12-18"),
        "incidents": ("the incident tool's export of 2026 incidents", "2027-01-04"),
        "timeline": ("the incident tool's timeline events for 2026 incidents", "2027-01-04"),
        "status": ("the public status page's 2026 history as its provider exports it", "2027-01-04"),
        "billing": ("the cloud provider's 2026 billing lines", "2027-01-05"),
        "invoices": ("the cloud provider's 2026 invoices", "2027-01-05"),
        "resources": ("the cloud provider's inventory of resources that ran in 2026", "2027-01-05"),
        "deploys": ("the delivery pipeline's 2026 deployment log", "2027-01-04"),
        "rollouts": ("the production cluster's rollout history", "2027-01-04"),
        "capacity": ("Platform Infrastructure's Q4 2026 capacity review", "2027-01-05"),
        "feedback": ("app store reviews of the Rotalinha app, July to December 2026", "2027-01-05"),
    }
    prov = {}
    for k, fn in K.FILES.items():
        prov[fn] = {"source": synth, "covers": about[k][0], "date": about[k][1],
                    "licence": "CC0 1.0 (constructed for this task)",
                    "made": "generated by task6/generator from its seeded records"}
    m = {"task": "task6",
         "title": "Rotalinha: the internal services that ran over their 2026 latency error budget",
         "domain": "General Statistics & Data Science",
         "objective": "Descriptive & Distribution Analysis",
         "decision": "which internal services ran over their 2026 latency error budget and get a reliability engineer "
                     "for the first half of 2027",
         "answer": ", ".join(R["over"]),
         "deliverables": [K.DOCX_OUT, K.CSV_OUT],
         "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
         "rows": sorted([(K.FILES["spans"], n["spans"]), (K.FILES["lb_h1"], n["lb_h1"]), (K.FILES["lb_h2"], n["lb_h2"])]),
         "provenance": prov}
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(m, f, indent=1)
        f.write("\n")


def cut_golden_zip(golden, path):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(golden)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 1, 8, 15, 26, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(golden, f), "rb").read())


def unpack_shipped(target):
    """target/ from the shipped target.zip, every member compared with the file on disk."""
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp) as z:
        names = [n_ for n_ in z.namelist() if not n_.endswith("/")]
        if not os.path.isdir(target) or sorted(os.listdir(target)) != sorted(n_.split("/", 1)[1] for n_ in names):
            if os.path.exists(target):
                shutil.rmtree(target)
            z.extractall(TASK)
        bad = [n_ for n_ in names if hashlib.md5(z.read(n_)).hexdigest() !=
               hashlib.md5(open(os.path.join(TASK, n_), "rb").read()).hexdigest()]
    return hashlib.md5(open(zp, "rb").read()).hexdigest(), bad


def golden_only():
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    zmd5, bad = unpack_shipped(target)
    print("shipped pack: target.zip md5 %s, %s" % (zmd5, "every member matches target/" if not bad else
                                                   "MEMBERS DIFFER " + ", ".join(bad)))
    R, F = build_golden(target, golden)
    write_metadata(None, R)
    import checks
    rc = checks.main(target)
    import verify
    vbad = verify.run(TASK)
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    first = digest(golden)
    fig1 = open(os.path.join(HERE, "figures.json"), "rb").read()
    sub1 = open(os.path.join(TASK, "submission.md"), "rb").read()
    build_golden(target, golden)
    same = digest(golden) == first and open(os.path.join(HERE, "figures.json"), "rb").read() == fig1 and \
        open(os.path.join(TASK, "submission.md"), "rb").read() == sub1
    print("golden rebuild: %s" % ("byte-identical" if same else "DIFFERS"))
    cut_golden_zip(golden, os.path.join(TASK, "golden.zip"))
    for k, v in sorted(digest(golden).items()):
        print("  %s  golden/%s" % (v, k))
    print("  %s  golden.zip" % hashlib.md5(open(os.path.join(TASK, "golden.zip"), "rb").read()).hexdigest())
    sys.exit(1 if (rc or vbad or bad or not same) else 0)


def digest(d):
    out = {}
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(root, f)
            out[os.path.relpath(p, d)] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return out


def cut_zip(target, path):
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--golden-only", action="store_true")
    a = ap.parse_args()
    if a.golden_only:
        golden_only()
        return
    if a.out:
        build_pack(a.out)
        return
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    w, n, truths = build_pack(target)
    R, F = build_golden(target, golden)
    write_metadata(n, R)
    import checks
    rc = checks.main(target)
    import verify
    vbad = verify.run(TASK)
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    same = True
    if not a.no_rebuild:
        scratch = os.path.join(TASK, ".rebuild")
        build_pack(os.path.join(scratch, "target"))
        a1, a2 = digest(target), digest(os.path.join(scratch, "target"))
        shutil.rmtree(scratch)
        same = a1 == a2
        print("rebuild: %s" % ("byte-identical" if same else "DIFFERS " + ", ".join(k for k in a1 if a1[k] != a2.get(k))))
    cut_zip(target, os.path.join(TASK, "target.zip"))
    cut_golden_zip(golden, os.path.join(TASK, "golden.zip"))
    for k, v in sorted(digest(target).items()):
        print("  %s  %s" % (v, k))
    sys.exit(1 if (rc or vbad or not same) else 0)


if __name__ == "__main__":
    main()
