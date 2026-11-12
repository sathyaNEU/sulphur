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
import releases as RL  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

ZONE = "America/New_York"
NY = ZoneInfo(ZONE)
AS_OF = "2026-02-05"
# exports with no stamp of their own: the time each was pulled or written (New York)
SAVED = {
    PK.F_PANEL: (2026, 2, 2, 9, 41, 7),
    PK.F_HIST: (2026, 2, 2, 9, 41, 52),
    PK.F_DESC: (2026, 2, 2, 9, 43, 10),
    PK.F_STREET: (2026, 2, 4, 17, 12, 3),
    PK.F_WEB: (2026, 2, 2, 11, 5, 44),
    PK.F_APP: (2026, 2, 3, 8, 30, 15),
}
DISTRACTORS = {
    PK.F_WEB: "the panel vendor's weekly site visits to brindlemoss.com: it looks like a second read on the quarter's "
              "demand but counts visits, which held up through the holiday quarter while purchases per visit fell",
    PK.F_APP: "a third-party estimate of the Brindle & Moss app's daily category rank and downloads: it looks like a "
              "read on customer engagement and bears on no result",
}
SOURCES = {
    PK.F_PANEL: ("Simulated Kestrel Spend Panel weekly delivery of 2 February 2026 for the Brindle & Moss merchant ids, "
                 "the issuers' feeds as concatenated", "evidence"),
    PK.F_HIST: ("Simulated Kestrel delivery history: the trailing weeks of each weekly delivery as first delivered",
                "evidence"),
    PK.F_DESC: ("Simulated Kestrel monthly spend and transactions by raw merchant descriptor", "evidence"),
    DC.F_FILING: ("Brindle & Moss 10-K excerpts compiled by the desk (written for this task, figures simulated)", "evidence"),
    PK.F_STREET: ("Simulated sell-side estimates of fourth-quarter fiscal 2025 net sales", "evidence"),
    DC.F_MODEL: ("The desk's third-quarter card model (simulated, reproducible from the panel and the releases)",
                 "incumbent"),
    PK.F_WEB: ("Simulated weekly site visit estimates for brindlemoss.com", "distractor"),
    PK.F_APP: ("Simulated daily app category rank and download estimates", "distractor"),
}


def reported_inputs(F):
    """figures the answer blocks quote from the filed records (inputs, not results), as the records print them"""
    out = set()
    for k in ("deposits_q3_m", "deposits_base_m", "deposits_q3fy24_m", "contract_fy2024_m", "contract_9m_fy2024_m",
              "base_net_sales_m", "fern_base_m"):
        out.add("%.1f" % F[k])
        out.add("{:,.1f}".format(F[k]))
    return sorted(out)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def write_pack(tgt):
    w = W.simulate(PK.SEED)
    o = PK.write_all(tgt, w, PK.street_mid(w))
    DC.filing(os.path.join(tgt, DC.F_FILING), PK.regions_by_year(w), PK.by_year(w, w.fern_q), PK.by_year(w, w.contract_q))
    # the desk's third-quarter model, from the shipped files by its own stated method
    R0 = A.run(tgt)
    inc = A.incumbent(R0)
    rows = [(k.replace("FY", "Fiscal ").replace(" Q", " Q"), round(100 * x, 2), round(100 * y, 2)) for k, x, y in inc["rows"]]
    q3 = [("Per-card spend growth, fiscal 2025 Q3 (%)", round(100 * inc["x_q3"], 2)),
          ("Fitted net sales growth, fiscal 2025 Q3 (%)", round(100 * inc["g_q3"], 2)),
          ("Fiscal 2024 Q3 net sales (USD m)", round(inc["q3_base"], 1)),
          ("Model estimate, fiscal 2025 Q3 net sales (USD m)", round(inc["q3_forecast"], 1)),
          ("Reported, 10 December 2025 (USD m)", round(inc["q3_actual"], 1))]
    DC.model(os.path.join(tgt, DC.F_MODEL), rows, inc["fit"], inc["rmse"], q3)
    PP.normalize_ooxml(os.path.join(tgt, DC.F_MODEL), "Audrey Hanson", "Audrey Hanson", "2025-11-03T20:14:00Z",
                       "2025-12-11T22:37:41Z", excel=True, company="Larkhill Partners LP")
    rows_n = dict(o["rows"])
    rows_n[DC.F_MODEL] = len(rows)
    return w, rows_n, o["releases"]


def build_into(root):
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    for d in (tgt, gld):
        os.makedirs(d, exist_ok=True)
    w, rows, rel = write_pack(tgt)
    R = A.full(tgt)
    F, E = FG.write(R, root)
    GD.workbook(F, R, os.path.join(gld, GD.XLSX))
    PP.normalize_ooxml(os.path.join(gld, GD.XLSX), "Audrey Hanson", "Audrey Hanson", "2026-02-04T19:12:00Z",
                       "2026-02-06T15:48:26Z", excel=True, company="Larkhill Partners LP")
    GD.note(F, R, os.path.join(gld, GD.NOTE))
    PP.normalize_docx(os.path.join(gld, GD.NOTE), "Audrey Hanson", "Audrey Hanson", "2026-02-05T22:03:00Z",
                      "2026-02-06T16:21:00Z", 5, 87, "task20-note", title="BMH Q4 FY2025 net sales",
                      company="Larkhill Partners LP")
    open(os.path.join(root, "submission.md"), "w").write(WU.text(F))
    pulled = {n: dt.date(*SAVED[n][:3]).isoformat() for n in SAVED}
    pulled[DC.F_FILING] = "2025-03-27"
    pulled[DC.F_MODEL] = "2025-12-11"
    sources = dict(SOURCES)
    for fn, (k, d) in rel.items():
        pulled[fn] = d.isoformat()
        sources[fn] = ("Simulated Brindle & Moss earnings release for %s (8-K exhibit 99.1 as saved from EDGAR)" % k,
                       "evidence")
    meta = {"task": "task20", "architecture": 2, "as_of": AS_OF,
            "decision": "whether Brindle & Moss's fourth-quarter fiscal 2025 net sales land above or below the "
                        "sell-side consensus, and the position to take into the print",
            "deliverables": [GD.XLSX, GD.NOTE],
            "distractors": sorted(DISTRACTORS), "distractor_notes": DISTRACTORS,
            "stated_inputs": ["80", "13", "14", "53", "52", "31", "27"] + reported_inputs(F),
            "field_terms": ["net sales", "panel", "issuer", "descriptor", "comparable", "consensus", "deposits", "contract"],
            "rows": rows,
            "files": {n: {"source": s, "role": r, "pull_date": pulled.get(n, AS_OF),
                          "license": "generated for this task by task20/generator (a seeded simulation of the retailer, "
                                     "the card panel, its issuers and deliveries, and the desk's documents), CC BY 4.0"}
                      for n, (s, r) in sorted(sources.items())}}
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
    for k_, fn in enumerate(sorted(f for f in os.listdir(os.path.join(TASK, "target")) if f.startswith("bmh_8k_"))):
        d = dt.date.fromisoformat(fn[-14:-4])
        fallback[fn] = dt.datetime(d.year, d.month, d.day, 8, 2 + (7 * k_) % 50, (13 * k_) % 60, tzinfo=NY)
    PP.own_mtimes(os.path.join(TASK, "target"), fallback)
    PP.own_mtimes(os.path.join(TASK, "golden"), {})
    PP.zip_folder(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"), zone=ZONE)
    PP.zip_folder(os.path.join(TASK, "golden"), os.path.join(TASK, "golden.zip"), zone=ZONE)


def main():
    once = "--once" in sys.argv
    a = tempfile.mkdtemp(prefix="task20a-")
    build_into(a)
    if not once:
        b = tempfile.mkdtemp(prefix="task20b-")
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
