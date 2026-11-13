"""Build task20's pack, goldens, figures.json, effort.json, submission.md and metadata.json twice, require byte-identical
output, install them and cut target.zip and golden.zip.

    python3 task20/generator/build.py            # full build (two passes)
    python3 task20/generator/build.py --once     # one pass into the task folder, no comparison
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import writeup as WU  # noqa: E402

ZONE = "America/New_York"
NY = ZoneInfo(ZONE)
AS_OF = "2027-03-12"          # the March pull; the position is at 31 December 2026
# exports with no stamp of their own: the time each was pulled (New York)
SAVED = {
    PK.F_STMT: (2027, 3, 12, 8, 14, 5), PK.F_CASH: (2027, 3, 12, 8, 20, 41), PK.F_ACT: (2027, 3, 11, 16, 2, 33),
    PK.F_BENCH: (2026, 12, 4, 10, 31, 0), PK.F_MKT: (2027, 1, 4, 9, 12, 18), DC.F_SPEND: (2026, 7, 2, 14, 5, 50),
}
WORKBOOKS = {  # creator, last saved by, created, modified (UTC), company
    PK.F_REG: ("Donna Turner", "Donna Turner", "2016-03-02T14:20:00Z", "2027-03-10T19:44:12Z", "Wexmoor University"),
    PK.F_AUD: ("Donna Turner", "Donna Turner", "2017-05-11T13:05:00Z", "2026-11-20T21:12:40Z", "Wexmoor University"),
    DC.F_LIQ: ("Donna Turner", "Donna Turner", "2027-01-12T15:30:00Z", "2027-01-14T18:02:27Z", "Wexmoor University"),
    DC.F_PLAN: ("Corrigan Hart", "Corrigan Hart", "2026-11-30T16:10:00Z", "2026-12-07T22:48:05Z", "Corrigan Hart LLC"),
    DC.F_PEER: ("Corrigan Hart", "Corrigan Hart", "2025-10-02T13:41:00Z", "2025-10-06T20:15:33Z", "Corrigan Hart LLC"),
}
DISTRACTORS = {
    DC.F_PEER: "a peer survey of endowments' allocations, unfunded ratios and liquidity: it looks like a yardstick for the "
               "budget, but the policy tests Wexmoor's own reserve and cash flows, so no figure in it enters a result",
    DC.F_CAPPLAN: "the university's capital plan and borrowing: it looks like a claim on liquidity, but it draws nothing from "
                  "the endowment beyond the approved distribution, which the spending file already carries",
    DC.F_IPS: "the investment policy statement's allocation targets and spending rule: the liquidity policy fixes the "
              "spending as FY2027's approved distribution, so neither enters a result",
}
SOURCES = {
    PK.F_STMT: ("Simulated quarterly capital account statements of the endowment's private-fund interests", "evidence"),
    PK.F_CASH: ("Simulated custodian cash activity for the fourth quarter of 2026", "evidence"),
    PK.F_ACT: ("Simulated managers' portfolio activity reports (fund level)", "evidence"),
    PK.F_AUD: ("Simulated funds' audited financial statements, compiled by the Office of Investments", "evidence"),
    PK.F_REG: ("Simulated private commitment register of the Office of Investments", "evidence"),
    PK.F_BENCH: ("Simulated industry private-fund cash-flow benchmark (anonymised funds)", "evidence"),
    PK.F_MKT: ("Simulated quarterly market series (exit activity index, public equity index, short rate)", "evidence"),
    DC.F_LIQ: ("Simulated year-end liquid holdings report", "evidence"),
    DC.F_SPEND: ("Simulated spending distributions by fiscal year", "evidence"),
    DC.F_PLAN: ("Simulated consultant's draft pacing plan for 2027, with its alternative programs", "evidence"),
    DC.F_PEER: ("Simulated consultant's peer endowment survey", "distractor"),
    DC.F_POLICY: ("The endowment's liquidity policy (written for this task)", "standard"),
    DC.F_IPS: ("The endowment's investment policy statement (written for this task)", "distractor"),
    DC.F_CAPPLAN: ("The university's capital plan (written for this task)", "distractor"),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    for d in (tgt, gld):
        os.makedirs(d, exist_ok=True)
    Wo = PK.build_world()
    H = PK.history(Wo)
    rows = PK.write_all(Wo, H, tgt)
    DC.policy(os.path.join(tgt, DC.F_POLICY)); DC.ips(os.path.join(tgt, DC.F_IPS)); DC.capplan(os.path.join(tgt, DC.F_CAPPLAN))
    for name, (cr, lb, c0, c1, co) in WORKBOOKS.items():
        PP.normalize_ooxml(os.path.join(tgt, name), cr, lb, c0, c1, excel=True, company=co)
    R = A.full5(tgt)
    F, E = FG.write(R, root)
    GD.workbook(F, R, os.path.join(gld, GD.XLSX))
    PP.normalize_ooxml(os.path.join(gld, GD.XLSX), "Caitlin Hill", "Caitlin Hill", "2027-03-13T15:02:00Z", "2027-03-16T19:41:26Z",
                       excel=True, company="Wexmoor University")
    GD.memo(F, R, os.path.join(gld, GD.MEMO))
    PP.normalize_docx(os.path.join(gld, GD.MEMO), "Caitlin Hill", "Caitlin Hill", "2027-03-16T13:21:00Z", "2027-03-16T20:07:00Z",
                      revision=7, total_time=86, seed="task20-memo-2027", company="Wexmoor University")
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F, R))
    pulled = {n: dt.date(*SAVED[n][:3]).isoformat() for n in SAVED}
    meta = {"task": "task20", "architecture": 5, "as_of": AS_OF, "position_date": "2026-12-31",
            "decision": "which of Corrigan Hart's 2027 commitment programs Wexmoor University's endowment can adopt under its liquidity policy",
            "deliverables": [GD.XLSX, GD.MEMO],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["2027", "2028", "2026", format(int(DC.CUSHION), ","), str(int(DC.CUSHION))],
            "field_terms": ["capital call", "distribution", "unfunded commitment", "first close", "subscription line", "recycling",
                            "pacing", "liquidity", "stress", "follow-on", "rescue financing", "investment period"],
            "rows": rows,
            "files": {n: {"source": s, "role": r, "pull_date": pulled.get(n, AS_OF),
                          "license": "generated for this task by task20/generator (a seeded simulation of an endowment's private-fund "
                                     "program, its managers, their portfolio companies, an industry benchmark and the market), CC BY 4.0"}
                      for n, (s, r) in sorted(SOURCES.items())}}
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
    fallback = {n: dt.datetime(*v, tzinfo=NY) for n, v in SAVED.items()}
    PP.own_mtimes(os.path.join(TASK, "target"), fallback)
    PP.own_mtimes(os.path.join(TASK, "golden"), {})
    PP.zip_folder(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"), zone=ZONE)
    PP.zip_folder(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"), zone=ZONE)


def main():
    if "--into" in sys.argv:                     # the second build, in a process of its own
        build_into(sys.argv[sys.argv.index("--into") + 1])
        return
    once = "--once" in sys.argv
    a = tempfile.mkdtemp(prefix="task20a-")
    build_into(a)
    if not once:
        b = tempfile.mkdtemp(prefix="task20b-")
        import subprocess
        subprocess.run([sys.executable, os.path.abspath(__file__), "--into", b], check=True,
                       env=dict(os.environ, PYTHONHASHSEED="20271"))
        ha, hb = hashes(a), hashes(b)
        diff = [k for k in ha if ha[k] != hb.get(k)]
        if diff:
            print("NOT byte-identical:", diff)
            sys.exit(1)
        print("two builds byte-identical (%d files)" % len(ha))
    install(a)
    print("installed into", TASK)


if __name__ == "__main__":
    main()
