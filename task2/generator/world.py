"""task2 architecture 6: the world behind the pack (Larkmoor Speech and Shannonside Hospital Group).

Eight hospitals offer Larkmoor's medical dictation. Every clinician has their own recognisability (their grade and
specialty, their voice and habits); every hospital has its own acoustic conditions (wards, rooms, network), which
raise or lower the error of whoever dictates there. Before a hospital's compulsory date its clinicians choose whether
to dictate, and they choose by how well it works for them, so uptake is selective, and how many choose differs from
hospital to hospital. From the compulsory date every clinician in post dictates, and so does every later starter;
departments switch over in waves and a new user's first months are short ones. Clinicians move between the group's
hospitals under a new staff number and keep dictating if they already did. Each recognition release multiplies every
clinician's error by its own factor; recognition is frozen at release 6.0 through 2027 for the platform migration, and
the two university hospitals go compulsory on 1 February and 1 October 2027."""
import datetime as dt
import math
import os as _os
from statistics import NormalDist

import numpy as np

E = _os.environ.get
SEED = int(E("T2_SEED", "60607"))
START, END = (2022, 1), (2027, 12)          # months simulated; the pack records to December 2026
REC_FROM, REC_TO = (2023, 1), (2026, 12)    # the audit record


def mi(y, m):
    return (y - START[0]) * 12 + (m - 1)


NM = mi(*END) + 1
ASOF = mi(2027, 1)                          # first month not on record
DEC = mi(2026, 12)

# code, name, posts (clinicians in post), voluntary uptake, compulsory month, acoustic effect (log), university hospital
HOSPITALS = [
    ("CLM", "Clonmore General Hospital", 160, float(E("U_CLM", "0.62")), mi(2022, 5), float(E("G_CLM", "-0.05")), False),
    ("RTH", "Rathcullen Hospital", 140, float(E("U_RTH", "0.74")), mi(2022, 11), float(E("G_RTH", "0.03")), False),
    ("KBR", "Kilbrannagh Regional Hospital", 200, float(E("U_KBR", "0.55")), mi(2023, 6), float(E("G_KBR", "0.00")), False),
    ("CSL", "Castlelough Hospital", 150, float(E("U_CSL", "0.81")), mi(2024, 6), float(E("G_CSL", "0.05")), False),
    ("KNA", "Knockarra Community Hospital", 190, float(E("U_KNA", "0.68")), mi(2025, 1), float(E("G_KNA", "-0.03")), False),
    ("DRL", "Drumleigh Hospital", 170, float(E("U_DRL", "0.86")), mi(2025, 9), float(E("G_DRL", "0.02")), False),
    ("SSU", "Shannonside University Hospital", 820, float(E("U_SSU", "0.13")), mi(2027, 2), float(E("G_SSU", "0.06")), True),
    ("BKU", "Ballykeel University Hospital", 1250, float(E("U_BKU", "0.15")), mi(2027, 10), float(E("G_BKU", "0.08")), True),
]
CODES = [h[0] for h in HOSPITALS]
H = {h[0]: dict(name=h[1], posts=h[2], up=h[3], comp=h[4], g=h[5], teach=h[6]) for h in HOSPITALS}
TEACHING = ("SSU", "BKU")
UPTAKE_NEW = float(E("U_NEW", "0.40"))      # later hires at the university hospitals, offered it at induction

# release, first month in force, factor on every clinician's error
RELEASES = [("4.0", mi(2023, 2), 0.975), ("5.0", mi(2024, 6), 0.94), ("5.2", mi(2025, 3), 0.975),
            ("6.0", mi(2025, 11), 0.975)]
BASE_RELEASE = "3.4"
FROZEN = "6.0"

MU = math.log(float(E("T2_MU", "0.1048")))   # median clinician error at release 3.4, before grade and specialty
SIG_U = 0.32                                # between clinicians, log scale
SIG_SEL = 0.20                              # how far a clinician's trial differs from their long-run error, log scale
SD_DICT = 0.30                              # between a clinician's dictations, log scale
TURNOVER = 0.09                             # leavers a year
PTR = {False: 0.05, True: 0.25}             # share of posts filled from another group hospital (small, university)
AUDIT_RATE = 0.025
LINE = 0.15
CEILINGS = (10, 12, 14, 16)

GRADES = ["Consultant", "Specialist registrar", "Registrar", "Senior house officer", "Advanced nurse practitioner",
          "Clinical nurse specialist"]
G_EFF = dict(zip(GRADES, [-0.08, 0.0, 0.06, 0.13, 0.03, 0.0]))
G_VOL = dict(zip(GRADES, [55.0, 42.0, 36.0, 30.0, 24.0, 20.0]))   # dictations a month, median by grade
MIX_SMALL = [0.36, 0.18, 0.16, 0.16, 0.08, 0.06]
MIX_UNIV = [0.27, 0.25, 0.19, 0.19, 0.05, 0.05]
SPECS = [("General medicine", 0.17, 0.03), ("General surgery", 0.11, 0.0), ("Emergency medicine", 0.10, 0.08),
         ("Radiology", 0.09, -0.16), ("Orthopaedics", 0.07, -0.03), ("Cardiology", 0.06, 0.0),
         ("Respiratory medicine", 0.05, 0.02), ("Paediatrics", 0.06, 0.02), ("Obstetrics and gynaecology", 0.06, 0.01),
         ("Psychiatry", 0.05, 0.05), ("Anaesthetics", 0.05, -0.02), ("Gastroenterology", 0.04, 0.0),
         ("Oncology", 0.04, -0.01), ("Geriatric medicine", 0.05, 0.03)]
S_EFF = {s[0]: s[2] for s in SPECS}
UNIV_TILT = {}
SWITCH = [0, 0, 1, 1, 2, 2, 3, 4]           # months after the compulsory date a department switches over
SEASON = [1.02, 1.03, 1.04, 0.97, 1.02, 1.0, 0.95, 0.86, 1.0, 1.04, 1.05, 0.88]   # dictation volume by calendar month


def release_factor(t):
    f = 1.0
    for _, s, x in RELEASES:
        if t >= s:
            f *= x
    return f


def release_at(t):
    r = BASE_RELEASE
    for name, s, _ in RELEASES:
        if t >= s:
            r = name
    return r


def ramp(t, first):
    a = t - first
    return 0.5 if a == 0 else (0.8 if a == 1 else 1.0)


def p_heavy(loglevel, sd=SD_DICT):
    """share of a clinician's dictations above the line, their log error level (site and release included) given"""
    z = (math.log(LINE) - loglevel) / sd
    return 0.5 * math.erfc(z / math.sqrt(2))


class World:
    pass


def build(seed=SEED):
    w = World()
    rng = np.random.default_rng(seed)
    people = []
    pid = 0
    sd_s = math.sqrt(SIG_U ** 2 + SIG_SEL ** 2 + 0.012)
    cut = {c: NormalDist(0, sd_s).inv_cdf(v["up"]) for c, v in H.items()}
    cut_new = NormalDist(0, sd_s).inv_cdf(UPTAKE_NEW)

    def new_person(code):
        nonlocal pid
        pid += 1
        univ = H[code]["teach"]
        grade = GRADES[int(rng.choice(6, p=np.array(MIX_UNIV if univ else MIX_SMALL)))]
        sp = np.array([s[1] * (UNIV_TILT.get(s[0], 1.0) if univ else 1.0) for s in SPECS])
        si = int(rng.choice(len(SPECS), p=sp / sp.sum()))
        a = MU + G_EFF[grade] + SPECS[si][2] + rng.normal(0, SIG_U)
        return dict(pid=pid, grade=grade, spec=SPECS[si][0], alpha=a, eta=rng.normal(0, SIG_SEL),
                    vol=G_VOL[grade] * math.exp(rng.normal(0, 0.40)), spells=[])

    # each post's occupant serves an exponential stay, then the post is refilled
    for code in CODES:
        for slot in range(H[code]["posts"]):
            t = -float(rng.exponential(12.0 / TURNOVER))
            while t < NM:
                p = new_person(code)
                end = t + rng.exponential(12.0 / TURNOVER)
                p["after_launch"] = t > -4          # the service was offered at every hospital from autumn 2021
                p["spells"].append(dict(h=code, start=t, end=end))
                people.append(p)
                t = end
    # moves within the group: some posts filled after 2022 go to a clinician leaving another group hospital, who keeps
    # their own voice and habits (and their dictation, if they dictated) under a new staff number; most moves go towards
    # the university hospitals
    leavers = sorted([p for p in people if 0 <= p["spells"][-1]["end"] < NM - 2], key=lambda p: p["spells"][-1]["end"])
    joiners = [p for p in people if p["spells"][0]["start"] > 0]
    rng.shuffle(joiners)
    used, merged = set(), set()
    for j in joiners:
        d = j["spells"][0]["h"]
        if rng.random() >= PTR[H[d]["teach"]]:
            continue
        t0 = j["spells"][0]["start"]
        cands = [p for p in leavers if p["pid"] not in used and p["pid"] not in merged and p["spells"][-1]["h"] != d
                 and 0 <= t0 - p["spells"][-1]["end"] <= 2.5]
        if not cands:
            continue
        # careers run from the smaller hospitals towards the university hospitals, seldom back
        wt = np.array([(4.0 if (H[d]["teach"] and not H[p["spells"][-1]["h"]]["teach"]) else
                        0.15 if (H[p["spells"][-1]["h"]]["teach"] and not H[d]["teach"]) else 1.0) for p in cands])
        src = cands[int(rng.choice(len(cands), p=wt / wt.sum()))]
        used.add(src["pid"])
        src["spells"].append(dict(j["spells"][0]))
        merged.add(j["pid"])
    people = [p for p in people if p["pid"] not in merged]

    def score(p):
        return (p["alpha"] - MU) + p["eta"]

    # dictation at each posting
    for p in people:
        dictating = False
        for sp in p["spells"]:
            hh = H[sp["h"]]
            s0, e0 = max(0.0, sp["start"]), min(float(NM), sp["end"])
            sp["first"], sp["kind"] = None, None
            if e0 <= s0:
                continue
            if dictating:
                first, kind = int(s0) + int(rng.choice([0, 1])), "carried"
            elif s0 < hh["comp"]:
                cv = cut_new if (hh["teach"] and p["after_launch"]) else cut[sp["h"]]
                if score(p) < cv:
                    first, kind = (int(s0) if sp["start"] >= 0 else 0), "chose"
                elif e0 > hh["comp"]:
                    first, kind = hh["comp"] + int(rng.choice(SWITCH)), "compelled"
                else:
                    continue
            else:
                first, kind = int(s0) + int(rng.choice([0, 0, 1])), "hired"
            if first < int(e0):
                sp["first"], sp["kind"] = first, kind
                dictating = True
    w.people = people
    return w


def truth_quarter(w, y, q, sel=None):
    """the expected heavy-correction share of a quarter's dictations under the service, and its expected dictations"""
    num = den = 0.0
    for k in range(3):
        t = mi(y, 3 * (q - 1) + k + 1)
        f = math.log(release_factor(min(t, DEC)))
        s = SEASON[t % 12]
        for p in w.people:
            for sp in p["spells"]:
                if sp["first"] is not None and sp["first"] <= t < min(sp["end"], NM) and (sel is None or sel(p, sp)):
                    v = p["vol"] * ramp(t, sp["first"]) * s
                    num += v * p_heavy(p["alpha"] + H[sp["h"]]["g"] + f)
                    den += v
    return num / den, den


# ---------------------------------------------------------------- the records the pack is cut from
REF_MED, REF_SIG = 230.0, 0.50          # reference words in an audited dictation
SPLIT = (0.62, 0.24, 0.14)              # substitutions, deletions, insertions
READJ = 0.05                            # share of audits adjudicated
UNSCORABLE = 0.006


def records(w, seed=SEED + 1):
    """staff numbers, monthly dictations (2022 to 2026), the audit sample (2023 to 2026) and the HR register"""
    rng = np.random.default_rng(seed)
    last_rec = DEC
    # the group's HR system issues a staff number at each appointment, in appointment order
    posts = [(sp["start"], p["pid"], k) for p in w.people for k, sp in enumerate(p["spells"])]
    posts.sort()
    byid = {p["pid"]: p for p in w.people}
    sid = 200400
    for start, pid_, k in posts:
        sid += int(rng.integers(1, 6))
        sp = byid[pid_]["spells"][k]
        sp["staff"] = sid
        sp["prev"] = byid[pid_]["spells"][k - 1]["staff"] if k > 0 else None
    # monthly dictations, staff number by staff number
    vol = {}
    for p in w.people:
        for sp in p["spells"]:
            if sp["first"] is None:
                continue
            for t in range(max(0, sp["first"]), min(int(sp["end"]), last_rec + 1)):
                n = int(rng.poisson(p["vol"] * ramp(t, sp["first"]) * SEASON[t % 12]))
                if n > 0:
                    vol[(sp["staff"], t)] = n
    w.vol = vol
    w.spell_of = {sp["staff"]: (p, sp) for p in w.people for sp in p["spells"]}
    # the audit sample: 2.5 per cent of each hospital's dictations each month, drawn at random
    byh = {c: [] for c in CODES}
    for p in w.people:
        for sp in p["spells"]:
            if sp["first"] is not None:
                byh[sp["h"]].append((p, sp))
    audits = []
    aid = 4100000
    did_base = 70000000
    for t in range(mi(*REC_FROM), last_rec + 1):
        f = release_factor(t)
        rel = release_at(t)
        for code in CODES:
            pool = [(p, sp, vol.get((sp["staff"], t), 0)) for p, sp in byh[code]]
            pool = [x for x in pool if x[2] > 0]
            tot = sum(x[2] for x in pool)
            k = int(round(AUDIT_RATE * tot))
            if k == 0:
                continue
            wts = np.array([x[2] for x in pool], dtype=float)
            idx = rng.choice(len(pool), size=k, replace=True, p=wts / wts.sum())
            for j in sorted(idx):
                p, sp, _ = pool[j]
                aid += int(rng.integers(1, 4))
                refw = int(min(1500, max(40, round(REF_MED * math.exp(rng.normal(0, REF_SIG))))))
                wer = math.exp(p["alpha"] + H[code]["g"]) * f * math.exp(rng.normal(0, SD_DICT))
                errs = int(min(refw, round(wer * refw)))
                s = int(round(errs * SPLIT[0]))
                d = int(round(errs * SPLIT[1]))
                i = max(0, errs - s - d)
                day = int(rng.integers(1, 29))
                audits.append(dict(audit=aid, dictation=did_base + int(rng.integers(0, 10 ** 7)), t=t, day=day,
                                   h=code, staff=sp["staff"], release=rel, ref=refw, sub=s, dele=d, ins=i,
                                   unscorable=bool(rng.random() < UNSCORABLE), adjudicated=None))
                if rng.random() < READJ:
                    e2 = max(0, errs + int(rng.choice([-3, -2, -1, 1, 2, 3])))
                    audits[-1]["adjudicated"] = (int(round(e2 * SPLIT[0])), int(round(e2 * SPLIT[1])),
                                                 max(0, e2 - int(round(e2 * SPLIT[0])) - int(round(e2 * SPLIT[1]))))
    # audit times, from their own stream: the first pass 3 to 20 days after the dictation, an adjudication 5 to 24 days
    # after that; the export run on 8 January 2027 holds only what had been scored by then
    trng = np.random.default_rng(seed + 11)
    cutoff = dt.datetime(2027, 1, 8, 6, 0)
    kept = []
    for a in audits:
        y, m = divmod(a["t"], 12)
        first = dt.datetime(START[0] + y, m + 1, a["day"], 9, 0) + dt.timedelta(days=int(trng.integers(3, 21)),
                                                                                minutes=int(trng.integers(0, 600)))
        adj = first + dt.timedelta(days=int(trng.integers(5, 25)))
        a["audited_at"], a["adjudicated_at"] = first, adj
        if first > cutoff:
            continue
        if a["adjudicated"] is not None and adj > cutoff:
            a["adjudicated"] = None
        kept.append(a)
    w.audits = kept
    return w
