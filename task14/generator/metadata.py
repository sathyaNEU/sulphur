"""task14: metadata.json (outside target/): the decision, the deliverables, the distractors and each file's provenance.
It names no method, link or mechanism."""
import os

import golden as GD
import pack as PK

TITLE = "Penmarra Statistics Office: what the bond-based private rents measure will show for the December 2026 quarter"
COVERS = {
    "legacy": "the Tenancy Bond Board's legacy register: every bond held on or after 1 January 2019 with its records, to "
              "5 March 2023",
    "online": "the Tenancy Bond Board's online system: events from 6 March 2023 to the close of 27 November 2026",
    "xwalk": "landlord identifiers in the two systems, for landlords holding a bond on 5 March 2023",
    "codes": "the Board's code lists: record and event types, rent frequencies, dwelling types, rental areas, regions",
    "conc": "the Statistics Office's suburb concordance: rental areas and the regions in use from 1 July 2024",
    "panel": "the Statistics Office's Rent Survey: quarterly reports from its panel of rental dwellings, 2018 to the "
             "September 2026 quarter",
    "pcodes": "the Rent Survey's code list",
    "series": "the private rents index the Statistics Office published from the Rent Survey, to the September 2026 quarter",
    "cpi": "the consumers price index release for the September 2026 quarter",
    "method": "Methods paper PS-2026-07: the private rents measure's definition and scope",
    "hpi": "the house price index from settled sales, to the September 2026 quarter",
    "consents": "dwellings consented by month, region and type, January 2019 to September 2026",
}


def metadata(target, counts):
    files = sorted(os.listdir(target))
    key_of = {v: k for k, v in PK.FILES.items()}
    return {
        "task": "task14", "title": TITLE,
        "domain": "Other, Survey Research & Official Statistics",
        "task_type": "seasonal adjustment and official time-series production",
        "objective": "Data Extraction & Conformation (ETL / Pipeline Build)", "as_of": "2026-12-03",
        "deliverables": [GD.WORKBOOK, GD.SLIDES],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS] + [PK.FILES["series"]],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "categories": ["spreadsheet", "text"],
                        "largest_file": PK.FILES["online"], "largest_file_rows": counts["online"],
                        "long_file": PK.FILES["legacy"], "long_file_rows": counts["legacy"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task by simulating the process that makes the files: dwellings "
                               "entering and leaving Penmarra's rental market, landlords letting them, tenancies starting "
                               "at the going rent, running and ending, rents reviewed by landlords and operators, bonds "
                               "lodged, topped up, transferred and refunded at the Tenancy Bond Board, the Board's move to "
                               "a new system, and the Statistics Office's quarterly Rent Survey. Penmarra, its agencies, "
                               "its places and its people are invented.",
                     "date": "2026-11-11", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS[key_of[f]], "made": "written by task14/generator/make.py from the simulated process "
                                                        "(deterministic)"} for f in files],
    }
