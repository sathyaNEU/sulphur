"""task8: the pack's data files, each as the system that holds it would export it.

  census_year7_2026-10-01.csv        the trust's MIS census extract (one row per Year 7 student on roll)
  ks2_results_2026.csv               KS2 results from the common transfer files (scaled scores and codes)
  lexis_results_autumn2026.csv       the Lexis platform's results export, every sitting (incl. the trial)
  quill_results_2026.csv             Quill's results export (US dates, Quill student numbers)
  quill_roster_map.csv               Quill's rostering sync: Quill student number to admission number
  quill_session_log_2026.csv         Quill's question-level session log (the large file)
  brightway_results_2026.xlsx        the Brightway academies' results, typed by each academy's staff
  academies.csv                      the trust's academy list
  + the distractors (distractors.py)"""
import csv
import math
import datetime as dt
import os

import numpy as np

import params as P

FILES = {
    "census": "census_year7_2026-10-01.csv",
    "ks2": "ks2_results_2026.csv",
    "lexis": "lexis_results_autumn2026.csv",
    "quill": "quill_results_2026.csv",
    "quillmap": "quill_roster_map.csv",
    "quilllog": "quill_session_log_2026.csv",
    "brightway": "brightway_results_2026.xlsx",
    "academies": "academies.csv",
    "policy": "reading_forward_policy_2026.pdf",
    "lexis_tech": "lexis_technical_summary.pdf",
    "quill_tech": "quill_technical_summary.pdf",
    "brightway_tech": "brightway_technical_summary.pdf",
    "cpt": "cognitive_profile_tests_2026.csv",
    "attendance": "attendance_y7_autumn2026.csv",
    "survey": "y7_settling_in_survey_2026.csv",
    "tutorlog": "reading_forward_sessions_2025-26.csv",
}
DISTRACTORS = ["cpt", "attendance", "survey", "tutorlog"]

PREFERRED = {"Thomas": "Tom", "William": "Will", "Alexander": "Alex", "Samuel": "Sam", "Joshua": "Josh",
             "Benjamin": "Ben", "Daniel": "Dan", "Matthew": "Matt", "Rebecca": "Becky", "Elizabeth": "Lizzie",
             "Jessica": "Jess", "Katherine": "Kate", "Charlotte": "Lottie", "Nicholas": "Nick", "Jacob": "Jake",
             "Christopher": "Chris", "Michael": "Mike", "Jonathan": "Jon", "Abigail": "Abi", "Samantha": "Sam"}


def iso(d):
    return d.isoformat() if d else ""


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n" if path.endswith(("census_year7_2026-10-01.csv",
                                                                                       "academies.csv")) else "\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


class Pack:
    def __init__(self, W, seed):
        self.W = W
        self.rng = np.random.default_rng(seed)
        self.acad = {a["name"]: a for a in W["academies"]}
        S = W["students"]
        # admission numbers per academy, and Quill student numbers
        # the trust's MIS numbers admissions trust-wide
        self.adm = {}
        a_no = 260000 + int(self.rng.integers(0, 900))
        for s in sorted(S, key=lambda s: (s["academy"], s["last"], s["first"])):
            a_no += int(self.rng.integers(1, 6))
            self.adm[id(s)] = a_no
        self.quill_no = {}
        q = 400000 + int(self.rng.integers(0, 90000))
        for s in S:
            q += int(self.rng.integers(1, 40))
            self.quill_no[id(s)] = q

    # ------------------------------------------------------------------ the trust's MIS
    def census(self):
        rows = []
        for s in self.W["students"]:
            if s["left"]:
                continue
            a = self.acad[s["academy"]]
            pref = PREFERRED.get(s["first"], "") if self.rng.random() < 0.6 else ""
            rows.append([s["upn"], self.adm[id(s)], a["urn"], a["name"], s["last"], s["first"], pref,
                         iso(s["dob"]), s["gender"], "Y" if s["fsm"] else "N", "Y" if s["eal"] else "N",
                         "K" if s["sen"] else "N", s["tutor_group"]])
        rows.sort(key=lambda r: (r[3], r[4], r[5]))
        return rows

    def ks2(self):
        rows = []
        for s in self.W["students"]:
            if s["ks2_code"] == "NONE":
                continue
            score = "" if s["ks2"] is None else str(s["ks2"])
            maths = "" if s["ks2"] is None else str(int(np.clip(round(s["ks2"] + self.rng.normal(0, 5.5)), 80, 120)))
            gps = "" if s["ks2"] is None else str(int(np.clip(round(s["ks2"] + self.rng.normal(1, 4.8)), 80, 120)))
            rows.append([s["upn"], 2026, score, s["ks2_code"], maths, gps,
                         "%03d%04d" % (int(s["upn"][1:4]), int(s["upn"][4:8]))])
        # a re-sent transfer file appended a few records twice
        dup = [rows[i] for i in self.rng.choice(len(rows), size=int(len(rows) * 0.012), replace=False)]
        rows += dup
        rows.sort(key=lambda r: r[0])
        return rows

    # ------------------------------------------------------------------ the test platforms
    def lexis(self):
        rows = []
        k = 0
        for x in self.W["sittings"]:
            if x["test"] != "LEXIS":
                continue
            s = x["student"]
            a = self.acad[x["academy"]]
            k += 1
            sid = "LX26-%06d" % (318000 + 7 * k + int(self.rng.integers(0, 6)))
            up = s["upn"] if self.rng.random() > 0.025 else ""
            complete = x["status"] == "Complete"
            raw = int(np.clip(round(30 + 9.5 * (x["z"] + 0.15) + self.rng.normal(0, 0.8)), 0, 48)) if complete else \
                int(np.clip(round(12 + 4 * (x["z"] + 0.5)), 0, 20))
            sas = str(x["sas"]) if complete else ""
            stan = "" if not complete else str(int(np.clip(np.digitize(x["sas"], [74, 81, 89, 96, 104, 111, 119, 126]) + 1, 1, 9)))
            rows.append([sid, a["urn"], a["name"], up, s["last"], s["first"], iso(s["dob"]), iso(x["date"]),
                         "Lexis 11-14 Form A", raw, sas, stan, "Complete" if complete else "Incomplete"])
        # the export is run per academy and two academies' runs were appended twice
        twice = [r for r in rows if r[2] in ("Kelham Bridge Academy", "Swinton Moor Academy")][:37]
        rows += twice
        rows.sort(key=lambda r: (r[2], r[7], r[0]))
        return rows

    def quill(self):
        rows = []
        self.sessions = []
        for x in self.W["sittings"]:
            if x["test"] != "QUILL":
                continue
            s = x["student"]
            a = self.acad[x["academy"]]
            sess = "Q-%07d" % (5100000 + len(self.sessions) * 13 + int(self.rng.integers(0, 9)))
            self.sessions.append((sess, x))
            ss = int(round(700 + 92 * (x["z"] + 0.22) / 1.04 + self.rng.normal(0, 6)))
            ds = x["date"].strftime("%m/%d/%Y")
            mins = int(np.clip(round(18 + 0.6 * (x["items"] or 20) + self.rng.normal(0, 4)), 6, 45))
            pr = int(np.clip(round(50 * (1 + math.erf((x["sas"] - 100) / 15 / math.sqrt(2)))), 1, 99))
            rows.append([self.quill_no[id(s)], a["quill_site"], "%s, %s" % (s["last"], s["first"]), "Year 7",
                         ds, sess, x["sas"], pr, mins, "Completed"])
        rows.sort(key=lambda r: (r[1], r[4], r[0]))
        return rows

    def quill_map(self):
        rows = []
        for s in self.W["students"]:
            if s["test"] != "QUILL" and not any(x["test"] == "QUILL" and x["student"] is s for x in self.W["sittings"]):
                continue
            if self.rng.random() < P.QUILL_UNMAPPED:
                continue
            a = self.acad[s.get("moved_from") or s["academy"]] if s.get("moved_from") and \
                self.acad[s["moved_from"]]["test"] == "QUILL" else self.acad[s["academy"]]
            rows.append([self.quill_no[id(s)], a["quill_site"], self.adm[id(s)], s["first"], s["last"],
                         s["dob"].strftime("%m/%d/%Y")])
        rows.sort(key=lambda r: r[0])
        return rows

    def quill_log(self):
        rows = []
        for sess, x in self.sessions:
            n = x["items"]
            th = x["z"]
            t0 = dt.datetime.combine(x["date"], dt.time(9, 5)) + dt.timedelta(minutes=int(self.rng.integers(0, 300)))
            b = 0.0
            for j in range(n):
                p = 1 / (1 + np.exp(-(th - b)))
                c = int(self.rng.random() < p)
                b = b + (0.5 if c else -0.5) * (0.8 ** (j / 4))
                secs = int(np.clip(self.rng.lognormal(3.6, 0.45), 6, 240))
                t0 = t0 + dt.timedelta(seconds=secs)
                rows.append([sess, j + 1, "RQ%05d" % int(self.rng.integers(10000, 99999)), c, secs,
                             t0.strftime("%Y-%m-%dT%H:%M:%S")])
        return rows

    def academies(self):
        rows = []
        for a in self.W["academies"]:
            test = {"LEXIS": "Lexis", "QUILL": "Quill", "BRIGHTWAY": "Brightway"}[a["test"]]
            rows.append([a["urn"], a["name"], a["la"], "%03d/%04d" % (a["la_code"], a["estab"]), test,
                         a["quill_site"]])
        return rows

    # ------------------------------------------------------------------ the Brightway workbook (typed by staff)
    def brightway_sheets(self):
        sheets = {}
        for a in self.W["academies"]:
            if a["test"] != "BRIGHTWAY":
                continue
            out = []
            for x in self.W["sittings"]:
                if x["test"] != "BRIGHTWAY" or x["academy"] != a["name"]:
                    continue
                s = x["student"]
                first = s["first"]
                if self.rng.random() < 0.35 and first in PREFERRED:
                    first = PREFERRED[first]
                style = int(self.rng.integers(0, 3))
                dob = s["dob"].strftime("%d/%m/%Y") if style == 0 else (s["dob"].strftime("%d.%m.%y") if style == 1
                                                                       else s["dob"].strftime("%-d %b %Y"))
                sas = x["sas"]
                shown = "<70" if sas <= 69 else (">130" if sas >= 131 else sas)
                raw = int(np.clip(round(26 + 8.0 * (x["z"] + 0.35)), 0, 50))
                out.append(["%s, %s" % (s["last"], first), s["tutor_group"], dob, raw, shown, x["date"]])
            # absentees appear on the class lists with a blank result
            for s in self.W["students"]:
                if s["academy"] == a["name"] and not s["left"] and not any(
                        x["student"] is s and x["test"] == "BRIGHTWAY" for x in self.W["sittings"]):
                    if self.rng.random() < 0.7:
                        out.append(["%s, %s" % (s["last"], s["first"]), s["tutor_group"], s["dob"].strftime("%d/%m/%Y"),
                                    None, "abs", None])
            out.sort(key=lambda r: (r[1], r[0]))
            sheets[a["name"]] = out
        return sheets


def write_all(W, target):
    pk = Pack(W, P.SEED + 101)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    n["census"] = write_csv(F["census"], ["upn", "admission_no", "urn", "academy", "legal_surname", "legal_forename",
                                          "preferred_forename", "date_of_birth", "gender", "fsm_eligible", "eal",
                                          "sen_status", "tutor_group"], pk.census())
    n["ks2"] = write_csv(F["ks2"], ["upn", "ks2_year", "reading_scaled_score", "reading_code", "maths_scaled_score",
                                    "gps_scaled_score", "primary_laestab"], pk.ks2())
    n["lexis"] = write_csv(F["lexis"], ["session_id", "urn", "school_name", "upn", "surname", "forename", "dob",
                                        "test_date", "test", "raw_score", "standard_age_score", "stanine", "status"],
                           pk.lexis())
    n["quill"] = write_csv(F["quill"], ["Student ID", "Site Code", "Student Name", "Year Group", "Test Date",
                                        "Session ID", "Standardised Score", "National Percentile", "Minutes", "Status"],
                           pk.quill())
    n["quillmap"] = write_csv(F["quillmap"], ["quill_student_id", "site_code", "sis_id", "first_name", "last_name",
                                              "birth_date"], pk.quill_map())
    n["quilllog"] = write_csv(F["quilllog"], ["session_id", "item_seq", "item_id", "correct", "seconds", "answered_at"],
                              pk.quill_log())
    n["academies"] = write_csv(F["academies"], ["urn", "academy", "local_authority", "laestab", "entry_reading_test",
                                                "quill_site_code"], pk.academies())
    n["brightway_sheets"] = pk.brightway_sheets()
    return pk, n
