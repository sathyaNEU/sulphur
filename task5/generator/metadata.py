"""task5 architecture 4: metadata.json beside the pack (never inside it): what the task decides, the deliverables, the
files the solution does not read, and where every file comes from. It names no method and no figure."""
import json
import os

import world as W


def write(task, n):
    target = os.path.join(task, "target")
    files = sorted(os.listdir(target))
    rows = {W.FILES[k]: int(v) for k, v in n.items()}
    meta = {
        "task": "task5",
        "architecture": 4,
        "title": "Each Franklin county's December 2026 covered jobs for the Commissioner's certification to the 2027 Community Transition Fund, from the Unemployment Insurance Tax Division's records as they stood on 15 February 2027",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality",
        "analysis_type": "Data Extraction & Conformation (ETL / Pipeline Build)",
        "answer_shape": "a reconciled table plus findings",
        "as_of": "2027-02-15",
        "deliverables": [W.DELIVERABLES[k] for k in ("cert", "employers", "memo")],
        "distractor_files": [W.FILES[k] for k in W.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
                        "largest_file": W.FILES["reports"], "rows": rows},
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task5/generator/build.py (seeded, deterministic): a simulation of a US state "
                      "unemployment insurance tax division's filing and account processes, cut in the layouts of its statistical "
                      "extract (quarterly contribution reports, the employer account register and its status history, multiple "
                      "worksite reports), a county code list, the NAICS 2017 and 2022 supersector concordance, an enrolled state "
                      "act, a data sharing agreement, an email, a published county table, a contribution rate notice and county "
                      "population estimates; the State of Franklin, its counties, agencies, employers and people are fictional "
                      "and account numbers are not real",
            "date": "2027-02-16",
            "license": "original work for this task; no third-party data",
            "naics_titles": "NAICS 2017 and 2022 code titles from the U.S. Census Bureau's public classification (public domain)",
        }],
    }
    json.dump(meta, open(os.path.join(task, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(task, "metadata.json"), "a").write("\n")
