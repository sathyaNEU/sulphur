"""task8: the independent verifier (python3 verify.py <target>). It reads only the bundle, on its own parsing path
(pandas), builds its own student table and its own matching, recomputes R1, the second-sitting gain and the order
gaps by its own arithmetic, then runs the golden's conversions on its own table for R3 to R9, and reads every
document a figure leans on back through pdftotext with a positive control. Exit 1 on any mismatch."""
import datetime as dt
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OK = []


def chk(label, ok, detail=""):
    OK.append((label, bool(ok), str(detail)))


def nrm(x):
    x = str(x or "").strip().lower().replace("’", "'")
    return re.sub(r"[^a-z'\- ]", "", x)


def dob_any(v):
    if isinstance(v, (pd.Timestamp, dt.datetime)):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    for f in ("%d/%m/%Y", "%d.%m.%y", "%d %b %Y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            continue
    return None


def table(T):
    import pack as PK
    ac = pd.read_csv(os.path.join(T, PK.FILES["academies"]), dtype=str, keep_default_na=False)
    test_of = dict(zip(ac.academy, ac.entry_reading_test))
    site = {r.quill_site_code: r.academy for r in ac.itertuples() if r.quill_site_code}
    ce = pd.read_csv(os.path.join(T, PK.FILES["census"]), dtype=str, keep_default_na=False)
    S = {}
    key = {}
    sdob = {}
    for r in ce.itertuples():
        s = dict(upn=r.upn, adm=int(r.admission_no), academy=r.academy, test=test_of[r.academy], sittings=[],
                 ks2=None, ks2_code="NONE", surname=r.legal_surname, forename=r.legal_forename,
                 dob=dt.date.fromisoformat(r.date_of_birth))
        S[r.upn] = s
        for fn in {r.legal_forename, r.preferred_forename} - {""}:
            key.setdefault((nrm(r.legal_surname), nrm(fn), s["dob"]), []).append(s)
        sdob.setdefault((nrm(r.legal_surname), s["dob"]), []).append(s)
    by_adm = {s["adm"]: s for s in S.values()}
    k2 = pd.read_csv(os.path.join(T, PK.FILES["ks2"]), dtype=str, keep_default_na=False).drop_duplicates()
    for r in k2.itertuples():
        if r.upn in S:
            S[r.upn]["ks2"] = int(r.reading_scaled_score) if r.reading_scaled_score else None
            S[r.upn]["ks2_code"] = r.reading_code
    lx = pd.read_csv(os.path.join(T, PK.FILES["lexis"]), dtype=str, keep_default_na=False).drop_duplicates()
    for r in lx.itertuples():
        s = S.get(r.upn) if r.upn else None
        if s is None:
            d0 = dt.date.fromisoformat(r.dob)
            c = key.get((nrm(r.surname), nrm(r.forename), d0), []) or [x for x in sdob.get((nrm(r.surname), d0), [])
                                                                        if x["academy"] == r.school_name]
            s = c[0] if len(c) == 1 else None
        if s is None:
            continue
        s["sittings"].append(dict(test="LEXIS", date=dt.date.fromisoformat(r.test_date),
                                  sas=int(r.standard_age_score) if r.standard_age_score else None,
                                  valid=r.status == "Complete", academy=r.school_name))
    log = pd.read_csv(os.path.join(T, PK.FILES["quilllog"]), usecols=["session_id"])
    answered = log.groupby("session_id").size().to_dict()
    qm = pd.read_csv(os.path.join(T, PK.FILES["quillmap"]), dtype=str, keep_default_na=False)
    qmap = dict(zip(qm.quill_student_id, qm.sis_id.astype(int)))
    qr = pd.read_csv(os.path.join(T, PK.FILES["quill"]), dtype=str, keep_default_na=False)
    for r in qr.itertuples():
        sid = getattr(r, "_1")
        s = by_adm.get(qmap.get(sid, -1))
        if s is None:
            last, first = [x.strip() for x in getattr(r, "_3").split(",", 1)]
            acad = site.get(getattr(r, "_2"))
            c = {id(x): x for k, v in key.items() for x in v if k[0] == nrm(last) and k[1] == nrm(first)}
            here = [x for x in c.values() if x["academy"] == acad]
            away = [x for x in c.values() if x["test"] != "Quill"]
            s = here[0] if len(here) == 1 else (away[0] if not here and len(away) == 1 else None)
        if s is None:
            continue
        sess = getattr(r, "_6")
        s["sittings"].append(dict(test="QUILL", date=dt.datetime.strptime(getattr(r, "_5"), "%m/%d/%Y").date(),
                                  sas=int(getattr(r, "_7")), valid=answered.get(sess, 0) >= 24,
                                  academy=site.get(getattr(r, "_2"))))
    xl = pd.read_excel(os.path.join(T, PK.FILES["brightway"]), sheet_name=None, header=None)
    names = {n.replace(" Academy", "")[:30]: n for n in test_of}
    for sheet, df in xl.items():
        acad = names.get(sheet, sheet)
        h = [i for i in range(len(df)) if str(df.iat[i, 0]) == "Name"][0]
        for i in range(h + 1, len(df)):
            name, score = df.iat[i, 0], df.iat[i, 4]
            if pd.isna(name) or pd.isna(score) or str(score) == "abs":
                continue
            last, first = [x.strip() for x in str(name).split(",", 1)]
            d0 = dob_any(df.iat[i, 2])
            c = key.get((nrm(last), nrm(first), d0), []) or [x for x in sdob.get((nrm(last), d0), [])
                                                             if x["academy"] == acad]
            if len(c) != 1:
                continue
            sc = str(score).strip()
            sas = 69 if sc == "<70" else (131 if sc == ">130" else int(float(sc)))
            d = df.iat[i, 5]
            c[0]["sittings"].append(dict(test="BRIGHTWAY", date=pd.Timestamp(d).date(), sas=sas, valid=True,
                                         academy=acad))
    for s in S.values():
        s["sittings"].sort(key=lambda x: (x["date"], x["test"]))
    return {"students": list(S.values()), "academies": {a: {"entry_reading_test": t} for a, t in test_of.items()}}


def main(T):
    import params as P
    import results as R
    import pack as PK
    F = json.load(open(os.path.join(HERE, "figures.json")))
    D = table(T)
    chk("own parse: the census has the golden's students", len(D["students"]) == F["on_roll"], len(D["students"]))
    # R1 by its own count
    cnt = {}
    for s in D["students"]:
        if any(x["valid"] and x["sas"] is not None and x["date"] <= P.CENSUS for x in s["sittings"]):
            cnt[s["academy"]] = cnt.get(s["academy"], 0) + 1
    chk("R1 students with a valid entry sitting by the census, by academy (own count)",
        all(cnt.get(a, 0) == v for a, v in F["valid_by_academy"].items()), str(sum(cnt.values())))
    # R2 by its own arithmetic: the order gaps at the switch academies
    gaps = {"second": [], "first": []}
    per = {}
    for s in D["students"]:
        if s["test"] != "Brightway":
            continue
        b = [x for x in s["sittings"] if x["test"] == "BRIGHTWAY" and x["academy"] == s["academy"]]
        l = [x for x in s["sittings"] if x["test"] == "LEXIS" and x["valid"] and x["academy"] == s["academy"]]
        if b and l:
            k = "second" if l[0]["date"] > b[0]["date"] else "first"
            per.setdefault(s["academy"], {"second": [], "first": []})[k].append(l[0]["sas"] - b[0]["sas"])
    num, den = 0.0, 0
    for a, v in sorted(per.items()):
        if len(v["second"]) >= 20 and len(v["first"]) >= 20:
            w = len(v["second"]) + len(v["first"])
            num += w * (np.mean(v["second"]) - np.mean(v["first"])) / 2
            den += w
            gaps["second"] += v["second"]
            gaps["first"] += v["first"]
    gain = num / den
    chk("R2 the second-sitting gain (own arithmetic)", abs(round(gain, 1) - F["second_sitting_gain"]) < 0.051,
        "%.2f" % gain)
    chk("R2 the order gaps (own arithmetic)", abs(round(np.mean(gaps["second"]), 1) - F["evidence"]["gap_lexis_second"])
        < 0.051 and abs(round(np.mean(gaps["first"]), 1) - F["evidence"]["gap_lexis_first"]) < 0.051)
    # R3 to R9 with the golden's conversions on the verifier's own table
    g = R.all_results(D, R.GOLD)
    chk("R3 Brightway to Lexis on its own table", all(abs(round(g["R3"][x], 1) - F["brightway_lexis"][str(x)]) < 0.051
                                                       for x in R.POINTS))
    chk("R4 Quill to Lexis on its own table", all(abs(round(g["R4"][x], 1) - F["quill_lexis"][str(x)]) < 0.051
                                                  for x in R.POINTS))
    chk("R5 the July level on its own table", abs(round(g["R5"], 1) - F["july_level"]) < 0.051, "%.2f" % g["R5"])
    chk("R6 Reading Forward students by academy on its own table", all(g["R6"][a] == F["programme"][a] for a in g["R6"]),
        g["R6_total"])
    chk("R7 the change from each academy's own test", all(g["R7"][a] == F["change"][a] for a in g["R7"]))
    chk("R8 tutor hours and cost", abs(g["R8_hours"] - F["hours_total"]) < 0.051 and
        abs(round(g["R8_cost"]) - F["cost_total"]) <= 1)
    chk("R9 tutor hours by academy", all(abs(g["R9"][a] - F["hours"][a]) < 0.051 for a in g["R9"]))
    # the documents
    for f, control, needle in [(PK.FILES["policy"], "version 3", "below 85"),
                               (PK.FILES["lexis_tech"], "2019", "first time"),
                               (PK.FILES["quill_tech"], "2024 restandardisation", "24 to 34 questions"),
                               (PK.FILES["brightway_tech"], "2016", "<70")]:
        t = " ".join(subprocess.run(["pdftotext", os.path.join(T, f), "-"], capture_output=True, text=True).stdout.split())
        chk("document read back: %s (control '%s')" % (f, control), control in t and needle in t, "%d chars" % len(t))
    bad = [o for o in OK if not o[1]]
    for label, ok, detail in OK:
        print("%s  %-80s %s" % ("PASS" if ok else "FAIL", label[:80], detail[:60]))
    print("verify: %d checks, %d failed" % (len(OK), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
