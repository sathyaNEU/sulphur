"""task2: read the cut pack back as an analyst would, with every Layer 1 item handled: the adjudicated score replaces
the first pass, unscorable audio is out, the error rate is recomputed from its counts, the release strings are read as
one release, staff numbers reissued on a move are linked through the register, the volume export's repeated rows are
counted once. Nothing here estimates anything."""
import csv
import datetime as dt
import os
import re
import subprocess
from collections import defaultdict

from openpyxl import load_workbook

import world as W


def month_index(s):
    y, m = int(s[:4]), int(s[5:7])
    return W.mi(y, m)


def release_of(s):
    s = s.strip()
    m = re.match(r"^(?:LS-Med |r)?(\d+\.\d+)(?:\.\d+)?$", s)
    return m.group(1)


class Pack:
    pass


def load(target, comp=None, first_pass=False, link_movers=True, by_audit_date=False):
    P = Pack()
    # register and the person behind each staff number (a move gives a new number; previous_staff_no links them)
    wb = load_workbook(os.path.join(target, "clinician_register_2026.xlsx"), read_only=True)
    ws = wb["clinicians"]
    reg = {}
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        reg[int(r[0])] = dict(site=r[1], grade=r[2], specialty=r[3], prev=int(r[5]) if r[5] else None, status=r[6])
    person = {}
    for s in reg:
        p = s
        while link_movers and reg.get(p, {}).get("prev"):
            p = reg[p]["prev"]
        person[s] = p
    P.reg, P.person = reg, person
    # deployment dates from Schedule 2
    txt = "" if comp is not None else subprocess.run(
        ["pdftotext", "-layout", os.path.join(target, "services_agreement_schedule2_deployment.pdf"), "-"],
        capture_output=True, text=True, check=True).stdout
    comp = dict(comp) if comp is not None else {}
    for line in txt.splitlines():
        m = re.search(r"\s([A-Z]{3})\s+\d{1,2} \w+ \d{4}\s+(\d{1,2} \w+ \d{4})\s*$", line)
        if m:
            d = dt.datetime.strptime(m.group(2), "%d %B %Y").date()
            comp[m.group(1)] = W.mi(d.year, d.month)
    P.comp = comp
    # the 2027 go-lives: clinicians in post at the hospitals going compulsory
    wb = load_workbook(os.path.join(target, "shannonside_dictation_rollout_2027.xlsx"), read_only=True)
    staff = {}
    for i, r in enumerate(wb["2027 go-lives"].iter_rows(values_only=True)):
        if i and r[1]:
            staff[r[1]] = int(r[2])
    P.staff_in_post = staff
    # monthly volumes, the export's repeated rows counted once
    seen = set()
    vol = defaultdict(dict)
    site_of = {}
    with open(os.path.join(target, "dictation_volumes_2022_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["month"], r["staff_no"], r["dictations"], r["audio_minutes"], r["site"])
            if key in seen:
                continue
            seen.add(key)
            s = int(r["staff_no"])
            t = month_index(r["month"])
            vol[s][t] = vol[s].get(t, 0) + int(r["dictations"])
            site_of[(s, t)] = r["site"]
    P.vol, P.site_of = dict(vol), site_of
    # audits: one row per audited dictation, the adjudicated score where there is one
    rows = {}
    with open(os.path.join(target, "dictation_audits_2023_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["outcome"] != "scored":
                continue
            k = int(r["audit_id"])
            if first_pass:
                if r["audit_stage"] == "first pass":
                    rows[k] = r
                continue
            if k in rows and rows[k]["audit_stage"] == "adjudicated":
                continue
            rows[k] = r
    aud = []
    for k, r in rows.items():
        n = int(r["ref_words"])
        e = int(r["substitutions"]) + int(r["deletions"]) + int(r["insertions"])
        s = int(r["staff_no"])
        when = r["audited_at"] if by_audit_date else r["dictated_on"]
        aud.append(dict(audit=k, t=month_index(when), site=r["site"], staff=s, person=person.get(s, s),
                        release=release_of(r["release"]), n=n, e=e, wer=e / n))
    P.audits = aud
    return P
