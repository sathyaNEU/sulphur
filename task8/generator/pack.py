"""task8 architecture 18: writes target/ the way the Board's systems export it. The response platform's export
(item references by paper position before the 2024 platform change, by bank code after; times in UTC; an item
answered again after a reconnect keeps both rows), the candidate register (centre uploads and regional office
entries, some people registered twice), the bank file (the preliminary and final 2026 runs), the paper layouts,
the learning centres list, the specification, the 2022 standard-setting record, the September minute, the chair's
email, and two files the analysis never needs (the learner confidence survey and the computer suite audit)."""
import csv
import datetime as dt
import io
import os

import numpy as np
import openpyxl
from faker import Faker

import docs as D
import params as P
import postprocess as PP
import world as W

FILES = {
    "responses": "pacb_numeracy_responses_2022_2026.csv",
    "register": "pacb_candidate_register_2022_2026.csv",
    "bank": "pacb_item_bank_2026.csv",
    "layouts": "pacb_paper_layouts_2022_2027.xlsx",
    "centres": "pacb_learning_centres.csv",
    "spec": "level1_numeracy_specification_2026.pdf",
    "standard": "ln1_standard_setting_record_2022.pdf",
    "minute": "awards_committee_minute_2026-09-17.pdf",
    "email": "2027_level1_pass_mark_request.eml",
    "survey": "learner_confidence_survey_2026.csv",
    "audit": "centre_computer_suite_audit_2026.xlsx",
}
DISTRACTORS = ("survey", "audit")


def paper_name(level, year):
    return "%s-%d" % (level, year)


def export_paper_code(level, year):
    return "LN%s-%d" % (level[1], year)


def _dst(d):
    """Manitoba keeps Central daylight time from the second Sunday in March to the first Sunday in November."""
    m = dt.date(d.year, 3, 8)
    start = m + dt.timedelta(days=(6 - m.weekday()) % 7)
    n = dt.date(d.year, 11, 1)
    end = n + dt.timedelta(days=(6 - n.weekday()) % 7)
    return start <= d < end


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(header)
        wr.writerows(rows)


def sitting_ids(w):
    rng = np.random.default_rng(P.SEED + 11)
    n = len(w["sittings"])
    order = sorted(range(n), key=lambda j: (w["sittings"][j]["date"], j))
    ids = [None] * n
    k = 4100000 + int(rng.integers(0, 900))
    for j in order:
        k += int(rng.integers(1, 4))
        ids[j] = "S%07d" % k
    return ids


def responses(path, w, sids):
    """One row per answered item; a reconnect re-answers some items and both rows stay."""
    rng = np.random.default_rng(P.SEED + 12)
    X, papers, it = w["X"], w["papers"], w["it"]
    cen = {c["code"]: c for c in w["centres"]}
    rows = []
    for j, s in enumerate(w["sittings"]):
        idx = papers[paper_name(s["level"], s["year"])]
        prov = cen[s["centre"]]["prov"]
        local_off = 5 if (prov == "MB" and _dst(s["date"])) else 6
        start = dt.datetime(s["date"].year, s["date"].month, s["date"].day, int(rng.integers(9, 15)),
                            int(rng.integers(0, 60))) + dt.timedelta(hours=local_off)
        t = start
        order = list(range(40))
        recon = rng.random() < P.RECONNECT_RATE
        cut = int(rng.integers(8, 33)) if recon else None
        redo = set(rng.choice(range(max(0, (cut or 1) - 4), cut or 1), size=min(3, cut or 1), replace=False).tolist()) \
            if recon else set()
        for pos in order:
            i = int(idx[pos])
            t = t + dt.timedelta(seconds=int(rng.integers(35, 190)))
            ref = ("Q%02d" % (pos + 1)) if s["year"] <= 2023 else it["code"][i]
            final = int(X[j, i])
            if pos in redo:
                first = final if rng.random() < 0.7 else 1 - final
                rows.append([sids[j], s["cand"], export_paper_code(s["level"], s["year"]), ref, first,
                             (t - dt.timedelta(seconds=int(rng.integers(400, 900)))).strftime("%Y-%m-%dT%H:%M:%SZ")])
            if recon and pos == cut:
                t = t + dt.timedelta(seconds=int(rng.integers(240, 700)))
            rows.append([sids[j], s["cand"], export_paper_code(s["level"], s["year"]), ref, final,
                         t.strftime("%Y-%m-%dT%H:%M:%SZ")])
    _w(path, ["sitting_id", "candidate_id", "paper", "item", "score", "answered_utc"], rows)
    return len(rows)


def assign_people(w):
    """Candidate ids, names, dates of birth, home centres (where registered) and host centres (where sat)."""
    rng = np.random.default_rng(P.SEED + 13)
    fk = Faker("en_CA")
    fk.seed_instance(P.SEED)
    people = {}
    by_region = {}
    for c in w["centres"]:
        by_region.setdefault(c["region"], []).append(c["code"])
    for s in w["sittings"]:
        p = s["person"]
        if p not in people:
            yob = int(rng.integers(1958, 2007)) if s["level"] == "L1" else int(rng.integers(1972, 2008))
            people[p] = dict(cand="PA%06d" % (p % 1000000), family=fk.last_name(), given=fk.first_name(),
                             dob=dt.date(yob, int(rng.integers(1, 13)), int(rng.integers(1, 29))))
        s["cand"] = people[p]["cand"]
        # most sit where they registered; some sit at another centre in the same region
        s["home_centre"] = s["centre"]
        if rng.random() < 0.045:
            others = [c for c in by_region[s["region"]] if c != s["centre"]]
            s["home_centre"] = str(rng.choice(others))
    return people


def register(path, w, people):
    rng = np.random.default_rng(P.SEED + 14)
    rows = []
    k = 610000 + int(rng.integers(0, 500))
    regoff = {r[0]: "RO-" + r[0] for r in P.REGIONS}
    cen = {c["code"]: c for c in w["centres"]}

    def dob_fmt(d, by_office):
        return d.isoformat() if by_office else d.strftime("%d/%m/%Y")
    entries = []
    for s in w["sittings"]:
        pp = people[s["person"]]
        entries.append((s["date"] - dt.timedelta(days=int(rng.integers(12, 70))), s, pp, "Sat"))
    # withdrawn and absent registrations: people who registered and never sat
    n_extra = int(len(entries) * P.WITHDRAWN)
    fk = Faker("en_CA")
    fk.seed_instance(P.SEED + 1)
    for _ in range(n_extra):
        s0 = w["sittings"][int(rng.integers(0, len(w["sittings"])))]
        ghost = dict(cand="PA%06d" % int(rng.integers(400000, 999999)), family=fk.last_name(), given=fk.first_name(),
                     dob=dt.date(int(rng.integers(1960, 2007)), int(rng.integers(1, 13)), int(rng.integers(1, 29))))
        st = "Withdrawn" if rng.random() < 0.6 else "Absent"
        entries.append((s0["date"] - dt.timedelta(days=int(rng.integers(12, 70))),
                        dict(level=s0["level"], year=s0["year"], centre=s0["centre"], home_centre=s0["home_centre"],
                             region=s0["region"], date=s0["date"]), ghost, st))
    entries.sort(key=lambda e: (e[0], e[2]["cand"]))
    for when, s, pp, st in entries:
        k += int(rng.integers(1, 5))
        by_office = rng.random() < 0.22
        lvl = ("Level %s" % s["level"][1]) if rng.random() < 0.8 else s["level"]
        acc = "" if rng.random() > 0.06 else str(rng.choice(["extra time", "separate room", "reader (instructions)"]))
        sat_at = s["centre"] if st == "Sat" else ""
        sdate = s["date"].isoformat() if st == "Sat" else ""
        reg_by = regoff[s["region"]] if by_office else s["home_centre"]
        rows.append(["R%06d" % k, pp["cand"], pp["family"], pp["given"], dob_fmt(pp["dob"], by_office), lvl, s["year"],
                     s["home_centre"], reg_by, sat_at, sdate, st, acc])
        # some people were also entered by their regional office; the platform matched the second entry to the same
        # candidate and both rows record the sitting
        if st == "Sat" and rng.random() < P.DUP_REGISTRATION:
            k += int(rng.integers(1, 5))
            fam = pp["family"].upper() if rng.random() < 0.5 else pp["family"].replace("Mc", "Mc ")
            rows.append(["R%06d" % k, pp["cand"], fam, pp["given"], pp["dob"].isoformat(), lvl, s["year"],
                         s["home_centre"], regoff[s["region"]], sat_at, sdate, "Sat", ""])
    _w(path, ["registration_no", "candidate_id", "family_name", "given_name", "date_of_birth", "level", "paper_year",
              "home_centre", "entered_by", "sat_at", "sitting_date", "status", "access_arrangement"], rows)
    return len(rows)


def bank_file(path, w, r):
    it = w["it"]
    bank = r["bank"]
    first = {}
    for name in sorted(w["papers"]):
        y = int(name.split("-")[1])
        for i in w["papers"][name]:
            first.setdefault(int(i), y)
            first[int(i)] = min(first[int(i)], y)
    n_resp = (~np.isnan(w["X"])).sum(0)
    keep_pre = r["bank"]["prelim_rows"]
    n_pre = (~np.isnan(w["X"][keep_pre])).sum(0)
    rows = []
    infit, outfit = bank["infit"], bank["outfit"]
    for i in np.argsort(it["code"]):
        if np.isnan(bank["final"]["b"][i]):
            continue
        base = [it["code"][i], "Level %s" % it["pool"][i][1], W.STRAND_NAME[it["strand"][i]],
                "everyday" if it["everyday"][i] else "mathematical", int(it["words"][i]), first.get(int(i), "")]
        if not np.isnan(bank["prelim"]["b"][i]):
            rows.append(base + ["2026-06 preliminary", "%.3f" % bank["prelim"]["b"][i], "%.3f" % bank["prelim"]["se"][i],
                                "", "", int(n_pre[i])])
        rows.append(base + ["2026-10 final", "%.3f" % bank["final"]["b"][i], "%.3f" % bank["final"]["se"][i],
                            "%.2f" % infit[i], "%.2f" % outfit[i], int(n_resp[i])])
    _w(path, ["item", "pool", "strand", "context", "stem_words", "first_paper", "run", "difficulty_logits", "se",
              "infit_ms", "outfit_ms", "responses"], rows)
    return len(rows)


def layouts(path, w):
    it = w["it"]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name in sorted(w["papers"], key=lambda n: (n.split("-")[1], n)):
        lvl, y = name.split("-")
        ws = wb.create_sheet("LN%s %s" % (lvl[1], y))
        ws.append(["Position", "Item", "Strand", "Marks"])
        for pos, i in enumerate(w["papers"][name]):
            ws.append(["Q%02d" % (pos + 1), it["code"][i], W.STRAND_NAME[it["strand"][i]], 1])
        ws.column_dimensions["A"].width = 10
        ws.column_dimensions["B"].width = 12
        ws.column_dimensions["C"].width = 28
    wb.save(path)
    PP.normalize_ooxml(path, D.PEOPLE["psychometrician"], D.PEOPLE["psychometrician"], "2026-09-08T15:20:00Z",
                       "2026-11-04T17:42:00Z", excel=True)


def centres_file(path, w):
    rng = np.random.default_rng(P.SEED + 15)
    regname = {r[0]: r[1] for r in P.REGIONS}
    rows = []
    for c in sorted(w["centres"], key=lambda c: c["code"]):
        town = c["name"].split(" ")[0]
        opened = 1998 + int(rng.integers(0, 22))
        rows.append([c["code"], c["name"], c["region"], regname[c["region"]], c["prov"], town, opened, "open", ""])
    _w(path, ["centre", "centre_name", "region", "region_name", "province", "town", "registered_since", "status",
              "merged_into"], rows)
    return len(rows)


def survey(path, w):
    rng = np.random.default_rng(P.SEED + 16)
    rows = []
    codes = [c["code"] for c in w["centres"]]
    for k in range(1873):
        c = str(rng.choice(codes))
        lvl = "Level 1" if rng.random() < 0.44 else "Level 2"
        age = str(rng.choice(["18-24", "25-34", "35-44", "45-54", "55-64", "65+"], p=[0.24, 0.24, 0.19, 0.16, 0.12, 0.05]))
        qs = [int(np.clip(round(rng.normal(3.3 if lvl == "Level 2" else 2.9, 1.0)), 1, 5)) for _ in range(10)]
        rows.append(["LS26-%05d" % (k * 3 + int(rng.integers(0, 3))), c, lvl, age] + qs +
                    [str(rng.choice(["online", "paper"], p=[0.83, 0.17]))])
    _w(path, ["response_id", "centre", "level", "age_band"] + ["q%02d" % q for q in range(1, 11)] + ["mode"], rows)


def audit(path, w):
    rng = np.random.default_rng(P.SEED + 17)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Suites"
    ws.append(["Centre", "Centre name", "Workstations", "Laptops on loan", "Screen size (in)", "Operating system",
               "Broadband (Mbps)", "Headsets", "Audited", "Auditor's note"])
    notes = [None, None, None, "two machines awaiting repair", "suite shared with the library", None,
             "new router fitted", None, "power bars replaced", None]
    for c in sorted(w["centres"], key=lambda c: c["name"]):
        ws.append([c["code"], c["name"], int(rng.integers(6, 25)), int(rng.integers(0, 9)),
                   str(rng.choice(["19", "21.5", "23.8", "15.6 (laptops)"])), str(rng.choice(["Windows 11", "Windows 10",
                                                                                         "ChromeOS"])),
                   int(rng.integers(25, 500)), int(rng.integers(0, 20)),
                   (dt.date(2026, 5, 4) + dt.timedelta(days=int(rng.integers(0, 70)))).isoformat(),
                   notes[int(rng.integers(0, len(notes)))]])
    wb.save(path)
    PP.normalize_ooxml(path, "Operations group", "Operations group", "2026-07-20T14:00:00Z", "2026-08-28T16:31:00Z",
                       excel=True, company=P.ORG)


def write(target, w, r):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    people = assign_people(w)
    sids = sitting_ids(w)
    w["sids"] = sids
    n = {}
    n["responses"] = responses(os.path.join(target, FILES["responses"]), w, sids)
    n["register"] = register(os.path.join(target, FILES["register"]), w, people)
    n["bank"] = bank_file(os.path.join(target, FILES["bank"]), w, r)
    layouts(os.path.join(target, FILES["layouts"]), w)
    n["centres"] = centres_file(os.path.join(target, FILES["centres"]), w)
    D.specification(os.path.join(target, FILES["spec"]))
    D.standard_record(os.path.join(target, FILES["standard"]))
    l1 = sum(1 for s in w["sittings"] if s["level"] == "L1" and s["year"] == 2026 and s["date"] <= dt.date(2026, 8, 31))
    l2 = sum(1 for s in w["sittings"] if s["level"] == "L2" and s["year"] == 2026 and s["date"] <= dt.date(2026, 8, 31))
    D.minute(os.path.join(target, FILES["minute"]), l1, l2)
    D.email(os.path.join(target, FILES["email"]))
    survey(os.path.join(target, FILES["survey"]), w)
    audit(os.path.join(target, FILES["audit"]), w)
    return n
