"""task8 architecture 19: the simulated trust. Students carry a reading level at the start of Year 7 (z on the Lexis
2019 basis); every record is generated from it by the process that makes that record:

  KS2 (May 2026)       the national reading test, four months before the start of Year 7, from the reading the pupil
                       had in Year 6 (above the start-of-Year-7 level by the summer and the move), with its own error,
                       a not-age-standardised age effect, a compressed top and codes below the test
  Lexis                the trust's test, standardised on a 2019 sample: the Lexis basis itself plus its error
  Quill                an adaptive test standardised on a softer 2024 sample (the same reader scores higher)
  Brightway            a paper test standardised in 2016, harder at the bottom and topping out early
  sittings             a July transition-day sitting reads the pre-transfer level; a second sitting within three
                       weeks carries a gain (familiarity with the test and two weeks of teaching), whichever test is
                       second

Nothing is placed where it decides: the second-sitting gain is on every second sitting (the trial, the switch
academy's Brightway re-sit, re-sits after failed online sessions), the July level on every pupil before the move,
the norm samples on every result of their test."""
import datetime as dt
import math

import numpy as np

import params as P

LETTERS = "ABCDEFGHJKLMNPQRTUVWXYZ"


def upn(la, estab, year, serial):
    digits = "%03d%04d%02d%03d" % (la, estab, year, serial)
    tot = sum(int(d) * w for d, w in zip(digits, range(2, 14)))
    return LETTERS[tot % 23] + digits


def sas_lexis(z):
    return np.clip(np.round(100 + 15 * z), *P.SAS_RANGE["LEXIS"])


def sas_quill(z):
    mu, sd = P.NORM["QUILL"]
    return np.clip(np.round(100 + 15 * (z - mu) / sd), *P.SAS_RANGE["QUILL"])


def sas_brightway_raw(z):
    """Brightway's standardised score before rounding and the reporting range (numpy, unclipped)."""
    mu, sd = P.NORM["BRIGHTWAY"]
    s = 100 + 15 * (z - mu) / sd
    k = P.BRIGHTWAY_KNEE
    return np.where(s > k, k + 14.0 * (1 - np.exp(-(s - k) / 14.0)), s)


def sas_brightway(z):
    s = np.round(sas_brightway_raw(z))
    return np.clip(s, 69, 131)          # 69 is reported "<70", 131 ">130"


def ks2_score(latent, age_c):
    """KS2 reading scaled score from the pupil's Year 6 reading (z), age centred in years (-0.5 youngest .. +0.5)."""
    x = P.KS2_MEAN + P.KS2_SD * (latent - P.JULY_LEVEL) / 1.12 + 2 * P.KS2_AGE * age_c
    top = 113.0
    x = np.where(x > top, top + 7.0 * (1 - np.exp(-(x - top) / 7.0)), x)
    return x


def dates_between(rng, a, b, n):
    span = (b - a).days
    days = rng.integers(0, span + 1, size=n)
    out = []
    for d in days:
        x = a + dt.timedelta(days=int(d))
        while x.weekday() >= 5:
            x = x - dt.timedelta(days=1) if x - dt.timedelta(days=1) >= a else x + dt.timedelta(days=2)
        out.append(x)
    return out


def school_days_after(d, n):
    x = d
    k = 0
    while k < n:
        x = x + dt.timedelta(days=1)
        if x.weekday() < 5:
            k += 1
    return x


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    from faker import Faker
    fk = Faker("en_GB")
    fk.seed_instance(seed)
    acad = []
    for k, (name, la, test, n, mean, timing) in enumerate(P.ACADEMIES):
        la_code = {"Sheffield": 373, "Rotherham": 372, "Barnsley": 370, "Derbyshire": 830, "Nottinghamshire": 891,
                   "Nottingham": 892}[la]
        estab = 4000 + 37 * k + int(rng.integers(0, 30))
        urn = 136000 + 911 * k + int(rng.integers(0, 400))
        acad.append(dict(name=name, la=la, la_code=la_code, estab=estab, urn=urn, test=test, n=n, mean=mean,
                         timing=timing, quill_site="QS%03d" % (101 + 13 * k) if test == "QUILL" else ""))
    S = []
    serial = {}
    for a in acad:
        n = a["n"]
        fsm_p = np.clip(0.22 - 0.35 * a["mean"], 0.08, 0.55)
        for i in range(n):
            g = "F" if rng.random() < 0.49 else "M"
            first = fk.first_name_female() if g == "F" else fk.first_name_male()
            last = fk.last_name()
            if rng.random() < 0.03:
                last = last + "-" + fk.last_name()
            dob = dt.date(2014, 9, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
            age_c = 0.5 - ((dob - dt.date(2014, 9, 1)).days / 364.0)
            fsm = rng.random() < fsm_p
            sen = rng.random() < 0.13
            eal = rng.random() < (0.12 if a["la"] not in ("Nottingham", "Sheffield") else 0.21)
            newcomer = eal and rng.random() < 0.16
            theta = (a["mean"] + rng.normal(0, P.WITHIN_SD) - 0.55 * sen - 0.12 * fsm + 0.0 * eal
                     - 0.45 * newcomer)
            primary_la = a["la_code"] if rng.random() < 0.9 else int(rng.choice([370, 372, 373, 830, 891, 892]))
            pr = 2000 + int(rng.integers(0, 600))
            key = (primary_la, pr)
            serial[key] = serial.get(key, 0) + 1
            S.append(dict(academy=a["name"], test=a["test"], timing=a["timing"], first=first, last=last, gender=g,
                          dob=dob, age_c=age_c, fsm=fsm, sen=sen, eal=eal, newcomer=newcomer, theta=theta,
                          upn=upn(primary_la, pr, 15, serial[key] + int(rng.integers(0, 50)) * 7)))
    n = len(S)
    th = np.array([s["theta"] for s in S])
    # the Year 6 level (KS2 in May, the July transition day) stands above the start of Year 7
    july = P.JULY_LEVEL + rng.normal(0, P.JULY_SD, n)
    gain = P.SECOND_SITTING_GAIN + rng.normal(0, P.GAIN_SD, n)
    change = rng.normal(0, P.KS2_CHANGE_SD, n)
    ks2_lat = th + july + change + rng.normal(0, P.KS2_ERR_SD, n)
    ks2_x = ks2_score(ks2_lat, np.array([s["age_c"] for s in S]))
    for i, s in enumerate(S):
        s["july"] = float(july[i])
        s["gain"] = float(gain[i])
        if s["newcomer"] and rng.random() < 0.75:
            s["ks2"] = None
            s["ks2_code"] = "NONE"
        elif rng.random() < P.KS2_MISSING_ARRIVED * 0.45:
            s["ks2"] = None
            s["ks2_code"] = "NONE"
        elif rng.random() < P.KS2_ABSENT:
            s["ks2"] = None
            s["ks2_code"] = "A"
        elif ks2_x[i] < P.KS2_B_CUT:
            s["ks2"] = None
            s["ks2_code"] = "B"
        else:
            s["ks2"] = int(min(P.KS2_TOP, max(80, round(float(ks2_x[i])))))
            s["ks2_code"] = ""
    # census and the sittings
    for a in acad:
        rows = [s for s in S if s["academy"] == a["name"]]
        tg = rng.integers(0, P.TUTOR_GROUPS, size=len(rows))
        for s, g in zip(rows, tg):
            s["tutor_group"] = "7" + "ABCDEFGH"[int(g)]
    sittings = []

    def sit(s, test, date, z, kind, status="Complete", items=None, academy=None):
        sittings.append(dict(student=s, test=test, date=date, z=float(z), kind=kind, status=status, items=items,
                             academy=academy or s["academy"]))

    for a in acad:
        rows = [s for s in S if s["academy"] == a["name"]]
        group_date = {}
        for g in "ABCDEFGH":
            if a["test"] == "LEXIS" and a["timing"] == "SEPT":
                group_date[g] = dates_between(rng, *P.LEXIS_SEPT, 1)[0]
            elif a["test"] == "LEXIS":
                group_date[g] = dates_between(rng, *P.LEXIS_JULY, 1)[0]
            elif a["test"] == "QUILL":
                group_date[g] = dates_between(rng, *P.QUILL_SEPT, 1)[0]
            else:
                group_date[g] = dates_between(rng, *P.BRIGHTWAY_FIRST, 1)[0]
        trial_gap = {g: int(rng.integers(P.TRIAL_GAP[0], P.TRIAL_GAP[1] + 1)) for g in "ABCDEFGH"}
        for s in rows:
            g = s["tutor_group"][1]
            th_i = s["theta"]
            r = rng.random()
            s["late"] = r < P.ARRIVE_LATE
            s["no_sitting"] = (not s["late"]) and r < P.ARRIVE_LATE + P.MISS_FIRST
            s["left"] = rng.random() < P.LEFT_BEFORE_CENSUS
            if s["late"] or s["no_sitting"]:
                continue
            if a["test"] == "LEXIS":
                if a["timing"] == "JULY" and rng.random() >= P.JULY_ABSENT:
                    d = group_date[g]
                    z = th_i + s["july"] + rng.normal(0, P.TEST_SD["LEXIS"])
                    sit(s, "LEXIS", d, z, "july")
                else:
                    d = dates_between(rng, *P.LEXIS_SEPT, 1)[0] if a["timing"] == "JULY" else group_date[g]
                    if rng.random() < P.FAILED_ONLINE:
                        part = th_i + rng.normal(0, 0.6)
                        sit(s, "LEXIS", d, part, "failed", status="Incomplete")
                        d2 = school_days_after(d, int(rng.integers(2, 7)))
                        z = th_i + 0.3 * s["gain"] + rng.normal(0, P.TEST_SD["LEXIS"])
                        sit(s, "LEXIS", d2, z, "resit")
                    else:
                        z = th_i + rng.normal(0, P.TEST_SD["LEXIS"])
                        sit(s, "LEXIS", d, z, "first")
            elif a["test"] == "QUILL":
                d = group_date[g]
                if rng.random() < P.QUILL_SHORT:
                    items = int(rng.integers(9, P.QUILL_MIN_ITEMS))
                    z = th_i + rng.normal(0, P.TEST_SD["QUILL"] * 1.9)
                    sit(s, "QUILL", d, z, "short", items=items)
                    if rng.random() < 0.72:
                        d2 = school_days_after(d, int(rng.integers(2, 4)))
                        z2 = th_i + 0.3 * s["gain"] + rng.normal(0, P.TEST_SD["QUILL"])
                        sit(s, "QUILL", d2, z2, "resit", items=int(rng.integers(26, 34)))
                else:
                    z = th_i + rng.normal(0, P.TEST_SD["QUILL"])
                    sit(s, "QUILL", d, z, "first", items=int(rng.integers(25, 35)))
            else:
                switch = a["name"] in P.SWITCH_ACADEMIES and g in "ABCD"
                miss_b = rng.random() < P.MISS_BRIGHTWAY
                miss_l = rng.random() < P.MISS_TRIAL
                if switch:
                    d_l = dates_between(rng, dt.date(2026, 9, 7), dt.date(2026, 9, 9), 1)[0]
                    d_b = school_days_after(d_l, int(rng.integers(6, 9)))
                    if not miss_l:
                        sit(s, "LEXIS", d_l, th_i + rng.normal(0, P.TEST_SD["LEXIS"]), "trial_first")
                    if not miss_b:
                        g2 = s["gain"] if not miss_l else 0.0
                        sit(s, "BRIGHTWAY", d_b, th_i + g2 + rng.normal(0, P.TEST_SD["BRIGHTWAY"]),
                            "second" if not miss_l else "first")
                else:
                    d_b = group_date[g]
                    d_l = school_days_after(d_b, int(round(trial_gap[g] * 5 / 7)))
                    if not miss_b:
                        sit(s, "BRIGHTWAY", d_b, th_i + rng.normal(0, P.TEST_SD["BRIGHTWAY"]), "first")
                    if not miss_l:
                        g2 = s["gain"] if not miss_b else 0.0
                        sit(s, "LEXIS", d_l, th_i + g2 + rng.normal(0, P.TEST_SD["LEXIS"]),
                            "trial_second" if not miss_b else "trial_only")
    # a few students moved between trust academies after their first sitting, and sat the new academy's test too
    movers = [s for s in S if not s["late"] and not s["no_sitting"] and not s["left"] and rng.random() < P.MOVED_WITHIN]
    by_test = {}
    for a in acad:
        by_test.setdefault(a["test"], []).append(a)
    for s in movers:
        dest = acad[int(rng.integers(0, len(acad)))]
        if dest["name"] == s["academy"]:
            continue
        s["moved_from"] = s["academy"]
        s["academy"] = dest["name"]
        s["test"] = dest["test"]
        s["timing"] = dest["timing"]
        own = [x for x in sittings if x["student"] is s]
        last = max(x["date"] for x in own) if own else dt.date(2026, 9, 20)
        d = school_days_after(max(last, dt.date(2026, 9, 21)), int(rng.integers(3, 8)))
        z = s["theta"] + s["gain"] + rng.normal(0, P.TEST_SD[dest["test"]])
        sit(s, dest["test"], d, z, "after_move", items=int(rng.integers(25, 33)) if dest["test"] == "QUILL" else None,
            academy=dest["name"])
    for x in sittings:
        if x["test"] == "LEXIS":
            x["sas"] = int(sas_lexis(x["z"]))
        elif x["test"] == "QUILL":
            x["sas"] = int(sas_quill(x["z"]))
        else:
            x["sas"] = int(sas_brightway(x["z"]))
    # the truth: each student's reading as a first September sitting of Lexis would show it
    for s in S:
        p = 0.5 * (1 + math.erf(((84.5 - 100) / 15 - s["theta"]) / (P.TEST_SD["LEXIS"] * math.sqrt(2))))
        s["p_below"] = p
    return {"academies": acad, "students": S, "sittings": sittings, "rng": rng}
