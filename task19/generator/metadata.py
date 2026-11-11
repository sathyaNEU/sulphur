"""task19: metadata.json (outside target/): the decision, the deliverables, the distractors and each file's provenance.
It names no method, link or mechanism."""
import os

import deliver as DV
import pack as PK

TITLE = "Kilvarra Statistics Office: usual residents of each district on 30 June 2026 for the 2027/28 grant determination"
COVERS = {
    "register": "the Kilvarra Health Service's patient register: every record on a practice's list on 30 June 2026, "
                "extracted on 3 July 2026",
    "practices": "the Health Service's general practices with their postcodes and districts",
    "postcodes": "the Statistics Office's postcode directory, June 2026, with codes retired in the 2024 recoding",
    "blocks": "the 2026 coverage survey's enumeration blocks: dwellings listed, the blocks selected and their selection "
              "probability",
    "persons": "the 2026 coverage survey: every person enumerated at the selected blocks' dwellings",
    "followup": "the 2026 coverage survey's field follow-up of the register records listed at the selected blocks' "
                "addresses",
    "review": "the clerical review of a subsample of the survey's people against the register",
    "vital": "births registered by sex since 1955, deaths registered by sex and age in the years to 30 June 2022 to 2026, "
             "and the national life table 2019-2021",
    "border": "the Border Agency's arrivals and recorded departures of non-national permit holders, July 2021 to June "
              "2026",
    "defence": "serving Defence Forces personnel by location, sex and age band on 30 June 2026",
    "accounts": "the Statistics Office's population accounts: the national population rolled forward from the 2021 "
                "Census with its components, to 30 June 2026",
    "census": "2021 Census usual residents by district, five-year age group and sex",
    "link": "the Health Service's 2023 study linking a sample of its 2021 register records to the 2021 Census",
    "listsize": "patients registered by district, broad age group and sex at each quarter end from September 2021",
    "he": "the Higher Education Authority's enrolment return for 2025/26",
    "circular": "Local Government Grants Commission circular 2026/14: the population basis of the 2027/28 grant "
                "determination",
}


def metadata(target, counts):
    files = sorted(os.listdir(target))
    key_of = {v: k for k, v in PK.FILES.items()}
    return {
        "task": "task19", "title": TITLE,
        "domain": "Other, Survey Research & Official Statistics",
        "task_type": "nonresponse, calibration and measurement-error adjustment",
        "objective": "Descriptive & Distribution Analysis", "as_of": "2026-11-11",
        "deliverables": [DV.WORKBOOK, DV.NOTE],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "categories": ["spreadsheet", "text"],
                        "largest_file": PK.FILES["register"], "largest_file_rows": counts["register"],
                        "long_file": PK.FILES["followup"], "long_file_rows": counts["followup"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task by simulating the processes that make the files: Kilvarra's "
                               "people from mid-2021 to mid-2026 (births, deaths, emigration and immigration, moves "
                               "between districts, students, the Defence Forces), the Health Service's register "
                               "(registration, deregistration, re-registration, list maintenance), the Statistics "
                               "Office's 2026 coverage survey, its follow-up and clerical review, the border, civil "
                               "registration and education returns. Kilvarra, its agencies, places and people are "
                               "invented.",
                     "date": "2026-11-11", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS[key_of[f]], "made": "written by task19/generator/make.py from the simulated "
                                                        "processes (deterministic)"} for f in files],
    }
