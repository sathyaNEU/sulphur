"""task2 architecture 5: the world behind the pack (Larkmoor Speech and Shannonside Hospital Group).

Eight hospitals offer Larkmoor's medical dictation; before a hospital's compulsory date its clinicians choose whether
to dictate (the voluntary uptake), from that date every clinician in post dictates and every later starter does too.
A clinician's own error level is drawn once: clinicians who began dictating before their hospital's compulsory date
(chose it) sit lower than those who began on or after it. Each model release multiplies every clinician's level by
its own factor. A dictation's word error rate scatters about the clinician's level at the release in force. The
audit takes a random sample of each hospital's dictations each month. Recognition is frozen at the last 2026 release
through 2027 (the platform migration), and the two teaching hospitals go compulsory in March and September 2027."""
import math
import os as _os
import numpy as np

SEED = int(__import__("os").environ.get("T2_SEED", "52515"))
START, END = (2022, 1), (2027, 12)          # months simulated; the pack records to December 2026
REC_FROM, REC_TO = (2023, 1), (2026, 12)    # the audit record


def mi(y, m):
    return (y - START[0]) * 12 + (m - 1)


NM = mi(*END) + 1
ASOF = mi(2027, 1)                          # first month not on record

# code, name, size (clinicians in post), voluntary uptake, compulsory month
HOSPITALS = [
    ("CLM", "Clonmore General Hospital", 160, float(_os.environ.get("T2_UPS", "0.70")), mi(2022, 5)),
    ("RTH", "Rathcullen Hospital", 140, float(_os.environ.get("T2_UPS", "0.70")), mi(2022, 11)),
    ("KBR", "Kilbrannagh Regional Hospital", 200, float(_os.environ.get("T2_UPS", "0.70")), mi(2023, 6)),
    ("CSL", "Castlelough Hospital", 150, float(_os.environ.get("T2_UPS", "0.70")), mi(2024, 6)),
    ("KNA", "Knockarra Community Hospital", 190, float(_os.environ.get("T2_UPS", "0.70")), mi(2025, 1)),
    ("DRL", "Drumleigh Hospital", 170, float(_os.environ.get("T2_UPS", "0.70")), mi(2025, 9)),
    ("SSU", "Shannonside University Hospital", int(_os.environ.get("T2_SSU", "820")), float(_os.environ.get("T2_UPT", "0.13")), mi(2027, 2)),
    ("BKU", "Ballykeel University Hospital", int(_os.environ.get("T2_BKU", "1250")), float(_os.environ.get("T2_UPT", "0.13")) + 0.02, mi(2027, 10)),
]
TEACHING = ("SSU", "BKU")

# release, first month in force, factor on every clinician's level
RELEASES = [
    ("4.0", mi(2023, 2), float(_os.environ.get("T2_R1", "0.975"))),
    ("5.0", mi(2024, 6), float(_os.environ.get("T2_R2", "0.94"))),
    ("5.2", mi(2025, 3), float(_os.environ.get("T2_R3", "0.975"))),
    ("6.0", mi(2025, 11), float(_os.environ.get("T2_R4", "0.975"))),
]
BASE_RELEASE = "3.4"                        # in force from before 2022
FROZEN = "6.0"

MED = {"V": 0.075, "M": float(_os.environ.get("T2_MEDM", "0.114"))}              # clinician level at release 3.4, median by type
SIG = {"V": 0.30, "M": 0.34}                # between clinicians, log scale
SD_DICT = 0.30                              # between a clinician's dictations, log scale
UPTAKE_NEW = {"SSU": 0.40, "BKU": 0.40}      # new hires at the teaching hospitals take the service up more readily
TURNOVER = 0.10                             # leavers a year
VOL_MED = 40.0                              # dictations a month, median clinician
VOL_SIG = 0.45
AUDIT_RATE = 0.025
LINE = 0.15                                 # heavy correction: word error rate above 15 per cent
CEILINGS = (10, 12, 14, 16)


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


class World:
    pass


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    w = World()
    w.hospitals = HOSPITALS
    rows = []          # one per clinician spell of dictating
    sid = 100000
    for hi, (code, name, n, up, comp) in enumerate(HOSPITALS):
        rng = np.random.default_rng([seed, hi])
        sid = 100000 + 9000 * hi
        for slot in range(n):
            t = float(rng.uniform(-60, 0))            # the occupant took up post before 2022
            while t < NM:
                end = t + rng.exponential(12.0 / TURNOVER)
                s0 = max(0.0, t)
                typ = None
                if s0 < comp:
                    u = UPTAKE_NEW.get(code, up) if t > 0 else up
                    if rng.random() < u:
                        typ, first = "V", int(s0) if t >= 0 else int(rng.integers(0, 1))
                    elif end > comp:
                        typ, first = "M", comp + int(rng.choice([0, 0, 1, 1, 2]))
                else:
                    typ, first = "M", int(s0) + int(rng.choice([0, 0, 1]))
                if typ is not None and first < min(NM, int(end)):
                    sid += int(rng.integers(1, 40))
                    rows.append(dict(staff=sid, h=code, typ=typ, first=first, last=min(NM, int(end)),
                                     level=MED[typ] * math.exp(rng.normal(0, SIG[typ])),
                                     vol=VOL_MED * math.exp(rng.normal(0, VOL_SIG))))
                t = end
    w.clin = rows
    return w


def ramp(t, first):
    a = t - first
    return 0.5 if a == 0 else (0.8 if a == 1 else 1.0)


def p_heavy(level, sd=SD_DICT):
    """share of a clinician's dictations above the line at a given level"""
    z = (math.log(LINE) - math.log(level)) / sd
    return 0.5 * math.erfc(z / math.sqrt(2))


def truth_quarter(w, y, q, factor=None, sel=None):
    """the expected heavy-correction share of a quarter's dictations, and its expected dictations"""
    num = den = 0.0
    for k in range(3):
        t = mi(y, 3 * (q - 1) + k + 1)
        f = release_factor(t) if factor is None else factor
        for c in w.clin:
            if c["first"] <= t < c["last"] and (sel is None or sel(c)):
                v = c["vol"] * ramp(t, c["first"])
                num += v * p_heavy(c["level"] * f)
                den += v
    return num / den, den


# ---------------------------------------------------------------- the records the pack is cut from
GRADES = [("Consultant", 0.34), ("Specialist registrar", 0.22), ("Registrar", 0.16), ("Senior house officer", 0.14),
          ("Advanced nurse practitioner", 0.08), ("Clinical nurse specialist", 0.06)]
SPECIALTIES = [("General medicine", 0.17), ("General surgery", 0.11), ("Emergency medicine", 0.10), ("Radiology", 0.09),
               ("Orthopaedics", 0.07), ("Cardiology", 0.06), ("Respiratory medicine", 0.05), ("Paediatrics", 0.06),
               ("Obstetrics and gynaecology", 0.06), ("Psychiatry", 0.05), ("Anaesthetics", 0.05),
               ("Gastroenterology", 0.04), ("Oncology", 0.04), ("Geriatric medicine", 0.05)]
REF_MED, REF_SIG = 230.0, 0.50          # reference words in an audited dictation
SPLIT = (0.62, 0.24, 0.14)              # substitutions, deletions, insertions
READJ = 0.05                            # share of audits adjudicated
UNSCORABLE = 0.006


def pick(rng, table):
    names = [a for a, _ in table]
    p = np.array([b for _, b in table], dtype=float)
    return names[int(rng.choice(len(names), p=p / p.sum()))]


def records(w, seed=SEED + 1):
    """monthly dictations per clinician (2022 to 2026), the audit sample (2023 to 2026), register details and movers"""
    rng = np.random.default_rng(seed)
    last_rec = mi(*REC_TO)
    for c in w.clin:
        c["grade"] = pick(rng, GRADES)
        c["specialty"] = pick(rng, SPECIALTIES)
        c["post_start"] = c["first"] - (int(rng.integers(6, 120)) if c["typ"] == "V" or c["first"] == dict(
            (h[0], h[4]) for h in HOSPITALS)[c["h"]] or c["first"] == dict((h[0], h[4]) for h in HOSPITALS)[c["h"]] + 1
            else int(rng.integers(0, 2)))
        c["prev"] = None
    # movers: a few clinicians who left one hospital and took up post at another keep dictating under a new number
    comp = {h[0]: h[4] for h in HOSPITALS}
    left = [c for c in w.clin if 12 <= c["last"] <= last_rec - 6]
    movers = rng.choice(len(left), size=36, replace=False)
    nxt = max(c["staff"] for c in w.clin) + 50
    extra = []
    for k in sorted(movers):
        c = left[k]
        dest = [h[0] for h in HOSPITALS if h[0] != c["h"] and comp[h[0]] <= c["last"]]
        if not dest:
            continue
        nxt += int(rng.integers(1, 30))
        d = dict(c)
        d.update(staff=nxt, h=str(rng.choice(dest)), first=c["last"] + int(rng.integers(1, 3)),
                 last=min(NM, c["last"] + int(rng.exponential(12.0 / TURNOVER)) + 3), prev=c["staff"],
                 post_start=c["last"] + 1)
        if d["first"] < d["last"]:
            extra.append(d)
    w.clin.extend(extra)
    # monthly dictations
    vol = {}
    for c in w.clin:
        for t in range(max(0, c["first"]), min(c["last"], last_rec + 1)):
            n = int(rng.poisson(c["vol"] * ramp(t, c["first"])))
            if n > 0:
                vol[(c["staff"], t)] = n
    w.vol = vol
    # the audit sample: 1.2 per cent of each hospital's dictations each month, drawn at random
    byh = {}
    for c in w.clin:
        byh.setdefault(c["h"], []).append(c)
    audits = []
    aid = 4100000
    did_base = 70000000
    for t in range(mi(*REC_FROM), last_rec + 1):
        f = release_factor(t)
        rel = release_at(t)
        for code, _, _, _, _ in HOSPITALS:
            pool = [(c, vol.get((c["staff"], t), 0)) for c in byh.get(code, [])]
            pool = [(c, n) for c, n in pool if n > 0]
            tot = sum(n for _, n in pool)
            k = int(round(AUDIT_RATE * tot))
            if k == 0:
                continue
            wts = np.array([n for _, n in pool], dtype=float)
            idx = rng.choice(len(pool), size=k, replace=True, p=wts / wts.sum())
            for j in sorted(idx):
                c = pool[j][0]
                aid += int(rng.integers(1, 4))
                refw = int(min(1500, max(40, round(REF_MED * math.exp(rng.normal(0, REF_SIG))))))
                wer = c["level"] * f * math.exp(rng.normal(0, SD_DICT))
                errs = int(min(refw, round(wer * refw)))
                s = int(round(errs * SPLIT[0]))
                d = int(round(errs * SPLIT[1]))
                i = max(0, errs - s - d)
                day = int(rng.integers(1, 29))
                audits.append(dict(audit=aid, dictation=did_base + int(rng.integers(0, 10 ** 7)), t=t, day=day,
                                   h=code, staff=c["staff"], release=rel, ref=refw, sub=s, dele=d, ins=i,
                                   unscorable=bool(rng.random() < UNSCORABLE), adjudicated=None))
                if rng.random() < READJ:
                    # adjudicated: the panel's corrected count replaces the first pass
                    e2 = max(0, errs + int(rng.choice([-3, -2, -1, 1, 2, 3])))
                    audits[-1]["adjudicated"] = (int(round(e2 * SPLIT[0])), int(round(e2 * SPLIT[1])),
                                                 max(0, e2 - int(round(e2 * SPLIT[0])) - int(round(e2 * SPLIT[1]))))
    # audit times, from their own stream: the first pass 3 to 20 days after the dictation, an adjudication 5 to 24 days
    # after that; the export run on 8 January 2027 holds only what had been scored by then
    import datetime as _dt
    trng = np.random.default_rng(seed + 11)
    cutoff = _dt.datetime(2027, 1, 8, 6, 0)
    kept = []
    for a in audits:
        y, m = divmod(a["t"], 12)
        first = _dt.datetime(START[0] + y, m + 1, a["day"], 9, 0) + _dt.timedelta(days=int(trng.integers(3, 21)),
                                                                                 minutes=int(trng.integers(0, 600)))
        adj = first + _dt.timedelta(days=int(trng.integers(5, 25)))
        a["audited_at"], a["adjudicated_at"] = first, adj
        if first > cutoff:
            continue
        if a["adjudicated"] is not None and adj > cutoff:
            a["adjudicated"] = None
        kept.append(a)
    w.audits = kept
    return w
