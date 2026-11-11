"""task8: the golden's reading of the pack (nothing from the simulator). Builds one record per Year 7 student on
the census with every entry-test sitting found for them in the three exports, the KS2 reading result, and the
academy's test.

Matching, as the files allow: Lexis rows by UPN, else by surname, forename (legal or preferred) and date of birth;
Quill rows through the rostering map's admission number, else by name inside the site's academy; Brightway rows by
surname, forename and date of birth inside the sheet's academy. Exact repeated export rows are dropped."""
import csv
import datetime as dt
import os
import re

from openpyxl import load_workbook

import pack as PK
import params as P


def rows(T, key):
    with open(os.path.join(T, PK.FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def norm(x):
    x = (x or "").strip().lower().replace("’", "'")
    return re.sub(r"[^a-z'\- ]", "", x)


def parse_dob(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    v = str(v).strip()
    for fmt in ("%d/%m/%Y", "%d.%m.%y", "%d %b %Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return dt.datetime.strptime(v, fmt).date()
        except ValueError:
            pass
    return None


def load(T):
    acad = {r["academy"]: r for r in rows(T, "academies")}
    site = {r["quill_site_code"]: r["academy"] for r in rows(T, "academies") if r["quill_site_code"]}
    census = rows(T, "census")
    stu = {}
    by_upn, by_adm, by_name, by_sdob = {}, {}, {}, {}
    for r in census:
        s = dict(upn=r["upn"], adm=int(r["admission_no"]), academy=r["academy"], test=acad[r["academy"]]["entry_reading_test"],
                 surname=r["legal_surname"], forename=r["legal_forename"], preferred=r["preferred_forename"],
                 dob=dt.date.fromisoformat(r["date_of_birth"]), tutor_group=r["tutor_group"], sittings=[], ks2=None,
                 ks2_code="NONE", fsm=r["fsm_eligible"] == "Y", eal=r["eal"] == "Y", sen=r["sen_status"] != "N")
        stu[s["upn"]] = s
        by_upn[s["upn"]] = s
        by_adm[s["adm"]] = s
        for fn in {s["forename"], s["preferred"]} - {""}:
            by_name.setdefault((norm(s["surname"]), norm(fn), s["dob"]), []).append(s)
        by_sdob.setdefault((norm(s["surname"]), s["dob"]), []).append(s)
    # KS2
    seen = set()
    for r in rows(T, "ks2"):
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        s = by_upn.get(r["upn"])
        if s is None:
            continue
        s["ks2"] = int(r["reading_scaled_score"]) if r["reading_scaled_score"] else None
        s["ks2_code"] = r["reading_code"] or ""
    # Lexis
    seen = set()
    unmatched = {"lexis": 0, "quill": 0, "brightway": 0}
    for r in rows(T, "lexis"):
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        s = by_upn.get(r["upn"]) if r["upn"] else None
        if s is None:
            d0 = dt.date.fromisoformat(r["dob"])
            c = by_name.get((norm(r["surname"]), norm(r["forename"]), d0), [])
            c = c if c else [x for x in by_sdob.get((norm(r["surname"]), d0), []) if x["academy"] == r["school_name"]]
            s = c[0] if len(c) == 1 else None
        if s is None:
            unmatched["lexis"] += 1
            continue
        s["sittings"].append(dict(test="LEXIS", date=dt.date.fromisoformat(r["test_date"]),
                                  sas=int(r["standard_age_score"]) if r["standard_age_score"] else None,
                                  valid=r["status"] == "Complete", academy=r["school_name"], session=r["session_id"]))
    # Quill: questions answered per session from the session log
    answered = {}
    with open(os.path.join(T, PK.FILES["quilllog"]), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            answered[r["session_id"]] = answered.get(r["session_id"], 0) + 1
    qmap = {}
    for r in rows(T, "quillmap"):
        qmap[r["quill_student_id"]] = int(r["sis_id"])
    for r in rows(T, "quill"):
        s = by_adm.get(qmap.get(r["Student ID"], -1))
        if s is None:
            last, first = [x.strip() for x in r["Student Name"].split(",", 1)]
            ac = site.get(r["Site Code"])
            c = [x for k, v in by_name.items() for x in v if k[0] == norm(last) and k[1] == norm(first)]
            c = list({id(x): x for x in c}.values())
            here = [x for x in c if x["academy"] == ac]
            # a student found elsewhere in the trust only when their own academy does not sit Quill (a move)
            away = [x for x in c if x["test"] != "Quill"]
            s = here[0] if len(here) == 1 else (away[0] if not here and len(away) == 1 else None)
        if s is None:
            unmatched["quill"] += 1
            continue
        s["sittings"].append(dict(test="QUILL", date=dt.datetime.strptime(r["Test Date"], "%m/%d/%Y").date(),
                                  sas=int(r["Standardised Score"]), valid=answered.get(r["Session ID"], 0) >= 24,
                                  academy=site.get(r["Site Code"]), session=r["Session ID"],
                                  answered=answered.get(r["Session ID"], 0)))
    # Brightway: one sheet per academy, typed by its staff
    wb = load_workbook(os.path.join(T, PK.FILES["brightway"]), data_only=True)
    names = {n.replace(" Academy", "")[:30]: n for n in acad}
    for ws in wb.worksheets:
        academy = names.get(ws.title, ws.title)
        head = None
        for r in range(1, 8):
            if ws.cell(r, 1).value == "Name":
                head = r
                break
        for r in range(head + 1, ws.max_row + 1):
            name = ws.cell(r, 1).value
            if not name:
                continue
            score = ws.cell(r, 5).value
            if score in (None, "", "abs"):
                continue
            last, first = [x.strip() for x in str(name).split(",", 1)]
            dob = parse_dob(ws.cell(r, 3).value)
            c = by_name.get((norm(last), norm(first), dob), [])
            if not c:
                c = [x for x in by_sdob.get((norm(last), dob), []) if x["academy"] == academy]
            s = c[0] if len(c) == 1 else None
            if s is None:
                unmatched["brightway"] += 1
                continue
            sas = 69 if str(score).strip() == "<70" else (131 if str(score).strip() == ">130" else int(score))
            d = ws.cell(r, 6).value
            s["sittings"].append(dict(test="BRIGHTWAY", date=d.date() if isinstance(d, dt.datetime) else d, sas=sas,
                                      valid=True, academy=academy, session=None))
    for s in stu.values():
        s["sittings"].sort(key=lambda x: (x["date"], x["test"]))
    return {"students": list(stu.values()), "academies": acad, "unmatched": unmatched}
