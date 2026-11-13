"""task24: the build. The pack under target/ from the simulated delivery centres, the golden on the cut pack,
figures.json, effort.json, the golden workbook and note, both zips, submission.md and metadata.json.

    python3 build.py                 # builds into a scratch folder, then installs into the task folder
    python3 build.py --out <folder>  # builds into <folder> only (two such builds are byte-identical)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs as D  # noqa: E402
import golden as GD  # noqa: E402
import outputs as OUT  # noqa: E402
import pack as PK  # noqa: E402
import tables  # noqa: E402
import world as Wd  # noqa: E402

EAT = dt.timezone(dt.timedelta(hours=3))
PHT = dt.timezone(dt.timedelta(hours=8))
F, SAMPLES = PK.F, PK.SAMPLES
# each export's own save time (the pull ran on Friday 6 November 2026)
EXPORT = {
    F["passes"]: dt.datetime(2026, 11, 6, 7, 41, 22, tzinfo=EAT), F["reviews"]: dt.datetime(2026, 11, 6, 7, 58, 3, tzinfo=EAT),
    F["punch"]: dt.datetime(2026, 11, 6, 8, 12, 47, tzinfo=EAT), F["pay"]: dt.datetime(2026, 11, 5, 16, 34, 10, tzinfo=EAT),
    F["roster"]: dt.datetime(2026, 11, 6, 9, 3, 55, tzinfo=EAT), F["projects"]: dt.datetime(2026, 11, 4, 14, 20, 31, tzinfo=EAT),
    F["archive"]: dt.datetime(2026, 11, 3, 18, 2, 9, tzinfo=EAT), F["survey"]: dt.datetime(2026, 10, 16, 11, 48, 40, tzinfo=EAT),
    F["gpu"]: dt.datetime(2026, 11, 2, 6, 30, 5, tzinfo=EAT),
    "pricing_policy_FIN-POL-04.pdf": dt.datetime(2026, 9, 14, 16, 41, 0, tzinfo=EAT),
    "annotator_pay_policy_2026.pdf": dt.datetime(2025, 12, 15, 11, 52, 0, tzinfo=EAT),
    "qa_review_standard_QA-STD-03.pdf": dt.datetime(2026, 3, 2, 13, 18, 0, tzinfo=EAT),
}
POLICIES = {"pricing_policy_FIN-POL-04.pdf": D.pricing_policy, "annotator_pay_policy_2026.pdf": D.pay_policy,
            "qa_review_standard_QA-STD-03.pdf": D.qa_standard}
PRICES = Wd.OFFERED


def stamps(t):
    u = t.astimezone(dt.timezone.utc).replace(second=0)
    return (u - dt.timedelta(minutes=37)).strftime("%Y-%m-%dT%H:%M:%SZ"), u.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_pack(target, world_cache=None):
    os.makedirs(target, exist_ok=True)
    W = world_cache or Wd.simulate()
    T = tables.build(W)
    S = PK.shifts(T)
    P, R = PK.stamp_passes(T, S)
    ids = PK.write_passes(T, P, os.path.join(target, F["passes"]))
    PK.write_reviews(T, R, ids, os.path.join(target, F["reviews"]))
    PK.punch_rows(S).to_csv(os.path.join(target, F["punch"]), index=False)
    PK.pay_register(T, S, P, os.path.join(target, F["pay"]), stamps(EXPORT[F["pay"]]))
    PK.roster(T, os.path.join(target, F["roster"]), stamps(EXPORT[F["roster"]]))
    PK.project_register(T, P, R, os.path.join(target, F["projects"]))
    PK.archive(T, P, os.path.join(target, F["archive"]))
    PK.survey(T, os.path.join(target, F["survey"]))
    PK.gpu(T, os.path.join(target, F["gpu"]))
    PK.samples(target, Wd.request_samples())
    for name, fn in POLICIES.items():
        fn(os.path.join(target, name))
    for key, r in D.RFQ.items():
        D.rfq(os.path.join(target, r["file"]), key, PRICES[key], SAMPLES[key])
        EXPORT[r["file"]] = r["sent"]
    for key, fn in SAMPLES.items():
        EXPORT[fn] = D.RFQ[key]["sent"] - dt.timedelta(minutes=19)
    for name in os.listdir(target):
        t = EXPORT[name].timestamp()
        os.utime(os.path.join(target, name), (t, t))
    return T


def zip_tree(folder, out):
    """an archive as a desktop zip tool writes it: entries in name order, each at its file's own save time"""
    with zipfile.ZipFile(out, "w") as z:
        for name in sorted(os.listdir(folder)):
            p = os.path.join(folder, name)
            tt = dt.datetime.fromtimestamp(os.path.getmtime(p), dt.timezone.utc).astimezone(EAT)
            zi = zipfile.ZipInfo(name, date_time=(tt.year, tt.month, tt.day, tt.hour, tt.minute, tt.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(p, "rb") as fh:
                z.writestr(zi, fh.read())


GOLD_ZIP = "task24_golden.zip"
GOLD_FILES = {"batch_cost_forecast.xlsx": dt.datetime(2026, 11, 12, 17, 46, 0, tzinfo=EAT),
              "batch_decision_note.docx": dt.datetime(2026, 11, 12, 18, 3, 0, tzinfo=EAT)}
DISTRACTORS = [F["survey"], F["gpu"]]


def build(out):
    tgt = os.path.join(out, "target")
    gdir = os.path.join(out, "golden")
    gen = os.path.join(out, "generator")
    for d in (tgt, gdir, gen):
        os.makedirs(d, exist_ok=True)
    make_pack(tgt)
    G = GD.compute(tgt)
    FG = OUT.build_figures(G)
    EF = OUT.build_effort(G, FG)
    json.dump(FG, open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(EF, open(os.path.join(gen, "effort.json"), "w"), indent=1)
    wb_t, nt_t = GOLD_FILES["batch_cost_forecast.xlsx"], GOLD_FILES["batch_decision_note.docx"]
    OUT.workbook(G, FG, os.path.join(gdir, "batch_cost_forecast.xlsx"), "Loice Mumo", *stamps(wb_t))
    OUT.note(G, FG, os.path.join(gdir, "batch_decision_note.docx"), "Loice Mumo", *stamps(nt_t))
    for name, t in GOLD_FILES.items():
        os.utime(os.path.join(gdir, name), (t.timestamp(), t.timestamp()))
    zip_tree(tgt, os.path.join(out, "target.zip"))
    zip_tree(gdir, os.path.join(out, GOLD_ZIP))
    meta = metadata(tgt)
    json.dump(meta, open(os.path.join(out, "metadata.json"), "w"), indent=1)
    import writeup as WU
    open(os.path.join(out, "submission.md"), "w").write(WU.submission(G, FG))
    return G, FG, EF


def metadata(tgt):
    files = []
    for name in sorted(os.listdir(tgt)):
        files.append(dict(path="target/" + name, source="generated by task24/generator from a simulation of Pellucid "
                          "Annotation's delivery centres and its clients' requests", pulled="2026-11-06",
                          licence="original synthetic data, no third-party content",
                          covers="see the file's own header or document"))
    return dict(task="task24", decision="which Q1 2027 annotation requests to accept at the clients' offered prices under the "
                "vendor's pricing policy", deliverables=["a spreadsheet", "a short note"], files=files,
                distractor_files=["target/" + d for d in DISTRACTORS], pull_date="2026-11-06")


def install(out):
    for name in ("target", "golden"):
        dst = os.path.join(TASK, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(out, name), dst)
    for name in ("target.zip", GOLD_ZIP, "metadata.json", "submission.md"):
        shutil.copy2(os.path.join(out, name), os.path.join(TASK, name))
    for name in ("figures.json", "effort.json"):
        shutil.copy2(os.path.join(out, "generator", name), os.path.join(HERE, name))


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else tempfile.mkdtemp(prefix="t24_")
    G, FG, EF = build(out)
    if "--out" not in sys.argv:
        install(out)
    print("built in", out, "call", FG["call_accept"], "target.zip", hashlib.sha256(open(os.path.join(out, "target.zip"), "rb").read()).hexdigest()[:16])
