"""Build task9's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip and golden.zip, then run the checks and the verifier.

    python3 task9/generator/build.py            # full build (two passes, then checks)
    python3 task9/generator/build.py --once     # one pass into the task folder, no comparison
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
import effort_passes as EP  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import postprocess as PP  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

ISO = "%Y-%m-%dT%H:%M:%SZ"
UTC = dt.timezone.utc
# the exports have no save stamp of their own: each file's time is the pull that wrote it (metadata.json's dates)
EXPORTS = {
    "dealtrail_buyout_transactions_1997-2026.csv": dt.datetime(2027, 2, 15, 16, 22, 41, tzinfo=UTC),
    "ecb_euro_reference_rates_2026-12.csv": dt.datetime(2027, 1, 4, 15, 5, 12, tzinfo=UTC),
    "euribor_forward_curve_2026-12-31.csv": dt.datetime(2026, 12, 31, 17, 10, 3, tzinfo=UTC),
    "lei_reference_extract_2026-12-31.csv": dt.datetime(2026, 12, 31, 14, 26, 55, tzinfo=UTC),
    "lenderbase_loan_performance_2008-2026.csv": dt.datetime(2027, 2, 16, 7, 58, 19, tzinfo=UTC),
    "lenderbase_workout_recoveries_2008-2026.csv": dt.datetime(2027, 2, 16, 8, 3, 7, tzinfo=UTC),
    "lenderbase_sector_codes.json": dt.datetime(2024, 1, 1, 10, 15, 30, tzinfo=UTC),
}
DISTRACTORS = {
    "euribor_forward_curve_2026-12-31.csv": "the euro money market curve at the cut-off; looks relevant to the notes' "
                                            "floating coupons but the test is on principal loss alone",
    "phl_matching_portfolio_cashflows_2027-2076.xlsx": "the fund's projected benefit payments; looks relevant to what the "
                                                       "notes are bought for but no figure is read from it",
}
SOURCES = {
    "lenderbase_loan_performance_2008-2026.csv": ("Lenderbase quarterly loan performance extract, European sponsor-backed first-lien loans", "2027-02-16", "evidence"),
    "lenderbase_workout_recoveries_2008-2026.csv": ("Lenderbase workout and recovery file", "2027-02-16", "evidence"),
    "lenderbase_sector_codes.json": ("Lenderbase sector classification and crosswalk, version 2024.1", "2024-01-01", "evidence"),
    "dealtrail_buyout_transactions_1997-2026.csv": ("Dealtrail European buyout transactions extract", "2027-02-15", "evidence"),
    "lei_reference_extract_2026-12-31.csv": ("Legal entity identifier reference extract (GLEIF format) for the borrowers and fund vehicles", "2026-12-31", "evidence"),
    "klcp_static_portfolio_2026-12-31.xlsx": ("Kestrel Lane Credit Partners collateral tape", "2027-01-05", "evidence"),
    "ostvale_collateral_tape_20261231.xlsx": ("Ostvale Capital collateral tape", "2027-01-05", "evidence"),
    "kestrel_lane_senior_note_term_sheet.pdf": ("Kestrel Lane indicative terms, KLCP Senior Loan Note 2027", "2026-12-08", "evidence"),
    "ostvale_senior_note_term_sheet.pdf": ("Ostvale indicative terms, Senior Secured Note 2027-1", "2026-12-11", "evidence"),
    "phl_rated_note_standard_2026.pdf": ("PHL investment committee standard MP-RN-2 for senior rated notes", "2026-11-18", "governing"),
    "ecb_euro_reference_rates_2026-12.csv": ("European Central Bank euro reference rates, December 2026", "2027-01-04", "evidence"),
    "euribor_forward_curve_2026-12-31.csv": ("EURIBOR fixings and three-month forwards at the cut-off", "2026-12-31", "distractor"),
    "phl_matching_portfolio_cashflows_2027-2076.xlsx": ("PHL matching portfolio projected benefit cash flows", "2026-11-20", "distractor"),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_into(root, nsim=A.NSIM):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    scratch = os.path.join(root, "scratch")
    for d in (tgt, gld, scratch):
        os.makedirs(d, exist_ok=True)
    world = W.simulate()
    info = PK.write(world, tgt)
    for name, when, who, org in (
            ("klcp_static_portfolio_2026-12-31.xlsx", dt.datetime(2027, 1, 5, 9, 12), "Portfolio Operations",
             "Kestrel Lane Credit Partners LLP"),
            ("ostvale_collateral_tape_20261231.xlsx", dt.datetime(2027, 1, 5, 10, 41), "Ostvale Reporting", "Ostvale Capital AB"),
            ("phl_matching_portfolio_cashflows_2027-2076.xlsx", dt.datetime(2026, 11, 20, 14, 3), "Liza Dekker",
             "Kadeweg Fiduciair Beheer")):
        PP.normalize_ooxml(os.path.join(tgt, name), who, who, (when - dt.timedelta(days=3)).strftime(ISO),
                           when.strftime(ISO), excel=True, company=org)
    DC.standard(os.path.join(tgt, "phl_rated_note_standard_2026.pdf"))
    kl = [world.loans[world.comps[c]["loan"]] for c in world.X]
    os_ = [world.loans[world.comps[c]["loan"]] for c in world.Y]
    DC.term_sheet(os.path.join(tgt, "kestrel_lane_senior_note_term_sheet.pdf"), "KL", sum(L["size"] for L in kl), len(kl))
    DC.term_sheet(os.path.join(tgt, "ostvale_senior_note_term_sheet.pdf"), "OS", sum(L["size"] for L in os_), len(os_))
    R = A.run(tgt, nsim=nsim)
    F = FG.make(R)
    EF = EP.attach(F)
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1)
    json.dump(EF, open(os.path.join(root, "effort.json"), "w"), indent=1)
    GD.write(F, gld, scratch)
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    meta = {"architecture": 7, "as_of": "2027-02-17", "call": F["call"],
            "deliverables": ["ic_note_senior_notes_2027.docx"],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "rows": {k: v for k, v in info.items() if k != "lb_id"},
            "files": {n: {"source": s, "date": d, "role": r,
                          "license": "synthetic, CC0, generated for this task by task9/generator"}
                      for n, (s, d, r) in sorted(SOURCES.items())}}
    json.dump(meta, open(os.path.join(root, "metadata.json"), "w"), indent=1)
    shutil.rmtree(scratch)
    return F


def zipdir(folder, out):
    """Each file's own save time, as a desktop zip tool at Kadeweg's office writes it (postprocess.zip_folder)."""
    PP.own_mtimes(folder, EXPORTS)
    PP.zip_folder(folder, out, zone="Europe/Amsterdam")


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
    shutil.copy(os.path.join(root, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(root, "effort.json"), os.path.join(HERE, "effort.json"))
    shutil.copy(os.path.join(root, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.copy(os.path.join(root, "metadata.json"), os.path.join(TASK, "metadata.json"))
    zipdir(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    zipdir(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"))


def main():
    once = "--once" in sys.argv
    a = tempfile.mkdtemp(prefix="task9a-")
    if once:
        build_into(a)
    else:
        # the two builds run side by side; each is a separate process with its own state
        import concurrent.futures as cf
        b = tempfile.mkdtemp(prefix="task9b-")
        with cf.ProcessPoolExecutor(max_workers=2) as ex:
            list(ex.map(build_into, [a, b]))
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
            print(r.stdout)
            if r.returncode != 0:
                print(r.stderr[-3000:])
                sys.exit(r.returncode)


if __name__ == "__main__":
    main()
