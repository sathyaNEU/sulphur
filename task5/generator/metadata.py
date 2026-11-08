"""task5 architecture 3: metadata.json beside the pack (outside target/): the decision, the deliverables, the
distractors and each file's provenance. It names no method and no figure from the graded blocks."""
import json
import os

import world as W


def write(task, n):
    target = os.path.join(task, "target")
    files = sorted(os.listdir(target))
    exts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(files, key=lambda f: os.path.getsize(os.path.join(target, f)))
    meta = {
        "task": "task5",
        "architecture": 3,
        "title": "Each Franklin county's December 2026 covered jobs, certified from the unemployment insurance reports received "
                 "by 15 February 2027, and the counties that qualify for the 2027 Community Transition Fund",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "03: each county's December covered jobs, from the reports received to the certified figure, against December 2025",
        "as_of": "2027-02-15",
        "deliverables": [W.DELIVERABLES["cert"], W.DELIVERABLES["employers"]],
        "distractor_files": [W.FILES[k] for k in W.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": exts, "largest_file": big,
                        "rows": {W.FILES[k]: v for k, v in n.items()}},
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task5/generator/build.py (seeded, deterministic) in the layouts of a US "
                      "state unemployment insurance tax division's statistical extract (quarterly contribution reports, the "
                      "employer account register and its status history, multiple worksite reports), a county code list, the "
                      "NAICS 2017 and 2022 supersector concordance, an enrolled state act, a data sharing agreement, an email, "
                      "a published county table, a contribution rate notice and county population estimates; the State of "
                      "Franklin, its counties, agencies, employers and people are fictional and account numbers are not real",
            "date": "2027-02-16",
            "license": "original work for this task; no third-party data",
            "naics_titles": "NAICS 2017 and 2022 code titles from the U.S. Census Bureau's public classification (public domain)",
        }],
    }
    json.dump(meta, open(os.path.join(task, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    return meta
