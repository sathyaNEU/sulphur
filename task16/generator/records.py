"""task16 records: the clean truth written out the way each system exports it. Calder Bay's patient index and merge
history, Rosario's patient index, the two groups' blood bank results, delivery logs and matched death notices, the
matching engine's 2026 pilot with the pairs HIM reviewed, and the engine's name equivalence table."""
import datetime as dt
import itertools
import zlib
from collections import defaultdict

import numpy as np
import pandas as pd

import params as P
import world as WD
from nicknames import PAIRS

ZIP = {"north": ["77971", "77972", "77973", "77975"], "south": ["77981", "77982", "77984", "77986"]}
FAC_A = ["CB Main", "CB North", "CB Bayside"]
FAC_B = ["RMG Rosario", "RMG Children's"]


def zip_of(w, pid, addr):
    side = w.persons[pid]["side"]
    z = ZIP[side]
    return z[zlib.crc32(("%s|%s" % (addr[0], addr[1])).encode()) % len(z)]


def a_phone(ph):
    return "" if not ph else "%s-%s-%s" % (ph[:3], ph[3:6], ph[6:])


def b_phone(ph):
    return "" if not ph else "(%s) %s-%s" % (ph[:3], ph[3:6], ph[6:])


def index_a(w):
    rng = np.random.default_rng(P.SEED + 101)
    rows = []
    for r in w.recs:
        if r["sys"] != "A" or r["retired"]:
            continue
        num, st, suf, unit = r["addr_now"]
        ssn = r["ssn"]
        rows.append(dict(MRN=r["mrn"], LAST_NAME=r["last"], FIRST_NAME=r["first_now"], MIDDLE_INIT=r["middle"],
                         DOB=r["dob"].strftime("%m/%d/%Y"), SEX=r["sex"],
                         ADDRESS="%d %s %s" % (num, st.upper(), suf.upper()), APT=unit.upper(),
                         CITY="PORT CALDER", STATE="TX", ZIP=zip_of(w, r["pid"], r["addr_now"]),
                         HOME_PHONE=a_phone(r["phone_now"]),
                         SSN="" if not ssn else "%s-%s-%s" % (ssn[:3], ssn[3:5], ssn[5:]),
                         REG_DATE=r["created"].strftime("%m/%d/%Y %H:%M"),
                         LAST_ACTIVITY=w.last_activity[r["mrn"]].strftime("%m/%d/%Y")))
    return pd.DataFrame(rows)


def index_b(w):
    rows = []
    for r in w.recs:
        if r["sys"] != "B" or r["retired"]:
            continue
        num, st, suf, unit = r["addr_now"]
        street = "%d %s %s" % (num, st, suf) + ((" " + unit) if unit else "")
        rows.append(dict(PATIENT_ID=r["mrn"], PAT_LNAME=r["last"].title() if r["created"].year >= 2016 else r["last"],
                         PAT_FNAME=r["first_now"].title() if r["created"].year >= 2016 else r["first_now"],
                         PAT_MNAME=r["middle"], BIRTH_DT=r["dob"].isoformat(), GENDER_CD=r["sex"],
                         STREET_ADDR=street, CITY="Port Calder", ST="TX", ZIP_CD=zip_of(w, r["pid"], r["addr_now"]),
                         PHONE_NUM=b_phone(r["phone_now"]), SSN_NUM=r["ssn"] or "",
                         CREATED_TS=r["created"].strftime("%Y-%m-%dT%H:%M:%S"),
                         LAST_ENC_DT=w.last_activity[r["mrn"]].isoformat()))
    return pd.DataFrame(rows)


def merge_history(w):
    rng = np.random.default_rng(P.SEED + 103)
    users = ["him.bhartman", "him.lgarza", "him.dvela", "him.rtorres", "him.kpham", "him.mcantu"]
    rows = []
    for i, m in enumerate(sorted(w.merges, key=lambda m: m["when"])):
        r = m["rec"]
        num, st, suf, unit = r["addr"]
        utc = m["when"] + dt.timedelta(hours=5 if _cdt(m["when"]) else 6)
        rows.append(dict(MERGE_ID="M%06d" % (100000 + i * 3 + int(rng.integers(0, 3))), SURVIVOR_MRN=m["survivor"],
                         RETIRED_MRN=m["retired"], MERGED_UTC=utc.strftime("%Y-%m-%d %H:%M:%S"),
                         METHOD="AUTO" if m["method"] == "AUTO-LDS" else "MANUAL",
                         MERGED_BY="REGSVC" if m["method"] == "AUTO-LDS" else users[int(rng.integers(0, len(users)))],
                         RET_LAST=r["last"], RET_FIRST=r["first"], RET_MIDDLE=r["middle"],
                         RET_DOB=r["dob"].strftime("%m/%d/%Y"), RET_SEX=r["sex"],
                         RET_ADDRESS=("%d %s %s" % (num, st.upper(), suf.upper())) + ((" " + unit.upper()) if unit else ""),
                         RET_PHONE=a_phone(r["phone"])))
    return pd.DataFrame(rows)


def _cdt(t):
    """US Central daylight time in force (second Sunday of March to first Sunday of November)."""
    y = t.year
    mar = dt.datetime(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.datetime(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return mar.replace(hour=2) <= t < nov.replace(hour=2)


def blood_bank(w):
    rng = np.random.default_rng(P.SEED + 105)
    rows = []
    for i, t in enumerate(sorted(w.tests, key=lambda t: (t["when"], t["mrn"]))):
        fac = (FAC_A if t["sys"] == "A" else FAC_B)[int(rng.integers(0, 3 if t["sys"] == "A" else 2))]
        abo, rh = t["abo"][:-1], "POS" if t["abo"].endswith("+") else "NEG"
        rows.append(dict(FACILITY=fac, MRN=t["mrn"], SPECIMEN_ID="%s%07d" % ("B" if t["sys"] == "A" else "R", 2000000 + i * 2),
                         COLLECTED=t["when"].strftime("%Y-%m-%d %H:%M"), TEST="TYPE AND SCREEN", ABO=abo, RH=rh))
    return pd.DataFrame(rows)


def deliveries(w):
    rows = []
    for d in sorted(w.deliveries, key=lambda d: d["when"]):
        fac = "CB Main" if d["sys"] == "A" else "RMG Rosario"
        rows.append(dict(FACILITY=fac, DELIVERY_DTTM=d["when"].strftime("%Y-%m-%d %H:%M"), MOTHER_MRN=d["mother_mrn"] or "",
                         NEWBORN_MRN=d["born_mrn"], NEWBORN_SEX=d["sex"], BIRTH_WT_G=d["grams"]))
    return pd.DataFrame(rows)


def death_notices(w):
    rows = []
    rng = np.random.default_rng(P.SEED + 107)
    for d in sorted(w.deaths, key=lambda d: (d["died"], d["mrn"])):
        src = "VSU match" if rng.random() < 0.8 else "Inpatient death"
        rows.append(dict(SYSTEM="Calder Bay" if d["sys"] == "A" else "Rosario", MRN=d["mrn"],
                         DATE_OF_DEATH=d["died"].isoformat(), SOURCE=src))
    return pd.DataFrame(rows)


def name_equivalents():
    rows = []
    for formal, nicks in PAIRS.items():
        for n in nicks:
            rows.append(dict(NAME=formal.upper(), EQUIVALENT=n.upper()))
    return pd.DataFrame(rows).sort_values(["NAME", "EQUIVALENT"]).reset_index(drop=True)


# ---------------------------------------------------------------------------------------------------------------
# the matching engine's 2026 pilot
# ---------------------------------------------------------------------------------------------------------------

VENDOR = dict(
    first=dict(exact=(0.92, 0.0050), equiv=(0.05, 0.0012), similar=(0.015, 0.0040), diff=(0.015, 0.9898)),
    last=dict(exact=(0.86, 0.0011), partial=(0.08, 0.0006), similar=(0.02, 0.0030), diff=(0.04, 0.9953)),
    dob=dict(exact=(0.965, 0.000037), partial=(0.025, 0.00045), diff=(0.010, 0.99951)),
    sex=dict(same=(0.995, 0.5), diff=(0.005, 0.5)),
    addr=dict(same=(0.62, 0.00012), diff=(0.38, 0.99988)),
    phone=dict(same=(0.55, 0.00010), diff=(0.45, 0.99990)),
    ssn=dict(same=(0.985, 0.0000012), diff=(0.015, 0.9999988)),
)
AUTO_LINK, REVIEW_FROM = 31.0, 19.0


def weight(field, level):
    m, u = VENDOR[field][level]
    return float(np.log2(m / u))


def jw(a, b):
    if a == b:
        return 1.0
    la, lb = len(a), len(b)
    if not la or not lb:
        return 0.0
    md = max(max(la, lb) // 2 - 1, 0)
    ma, mb = [False] * la, [False] * lb
    m = 0
    for i, c in enumerate(a):
        for j in range(max(0, i - md), min(lb, i + md + 1)):
            if not mb[j] and b[j] == c:
                ma[i] = mb[j] = True
                m += 1
                break
    if m == 0:
        return 0.0
    k = tr = 0
    for i in range(la):
        if ma[i]:
            while not mb[k]:
                k += 1
            if a[i] != b[k]:
                tr += 1
            k += 1
    jaro = (m / la + m / lb + (m - tr / 2) / m) / 3
    pre = 0
    for x, y in zip(a, b):
        if x == y and pre < 4:
            pre += 1
        else:
            break
    return jaro + pre * 0.1 * (1 - jaro)


EQ = defaultdict(set)
for _f, _ns in PAIRS.items():
    for _n in _ns + [_f]:
        EQ[_n.upper()].add(_f.upper())


def name_level(a, b):
    if a == b:
        return "exact"
    if EQ.get(a, set()) & EQ.get(b, set()):
        return "equiv"
    if jw(a, b) >= 0.88:
        return "similar"
    return "diff"


def last_level(a, b):
    if a == b:
        return "exact"
    ta, tb = set(a.split()), set(b.split())
    if ta & tb:
        return "partial"
    if jw(a, b) >= 0.9:
        return "similar"
    return "diff"


def dob_level(a, b):
    if a == b:
        return "exact"
    if (a.year == b.year and a.month == b.day and a.day == b.month) or (a.month == b.month and a.day == b.day) or \
            (a.year == b.year and a.month == b.month):
        return "partial"
    return "diff"


def pilot(w):
    """The engine scored cross-system candidate pairs for patients whose last names begin with B, G, L, P or T:
    exact first, last, birth date and sex were linked deterministically first; the rest were scored, pairs at or above
    the auto-link score linked, and pairs in the review band went to HIM."""
    rng = np.random.default_rng(P.SEED + 109)
    act = [r for r in w.recs if not r["retired"]]
    for r in act:
        r["_f"], r["_l"] = WD.std(r["first_now"]), WD.std(r["last"])
        num, st, suf, unit = r["addr_now"]
        r["_a"] = "%d %s %s" % (num, st.upper(), suf.upper())
    A = [r for r in act if r["sys"] == "A" and r["_l"][:1] in "BGLPT"]
    B = [r for r in act if r["sys"] == "B" and r["_l"][:1] in "BGLPT"]
    blocks = defaultdict(lambda: ([], []))
    for r in A:
        blocks[("d", r["dob"])][0].append(r)
        blocks[("y", r["_l"][:4], r["dob"].year)][0].append(r)
    for r in B:
        blocks[("d", r["dob"])][1].append(r)
        blocks[("y", r["_l"][:4], r["dob"].year)][1].append(r)
    seen = set()
    rows = []
    for k, (ra, rb) in blocks.items():
        for x, y in itertools.product(ra, rb):
            key = (x["mrn"], y["mrn"])
            if key in seen:
                continue
            seen.add(key)
            if x["_f"] == y["_f"] and x["_l"] == y["_l"] and x["dob"] == y["dob"] and x["sex"] == y["sex"]:
                continue
            lf, ll, ld = name_level(x["_f"], y["_f"]), last_level(x["_l"], y["_l"]), dob_level(x["dob"], y["dob"])
            ls = "same" if x["sex"] == y["sex"] else "diff"
            la = "same" if x["_a"] == y["_a"] else "diff"
            lp = "same" if x["phone_now"] and x["phone_now"] == y["phone_now"] else "diff"
            xs = x["ssn"] if x["ssn"] not in (None, "000000000", "999999999") else None
            ys = y["ssn"] if y["ssn"] not in (None, "000000000", "999999999") else None
            lss = None if not (xs and ys) else ("same" if xs == ys else "diff")
            score = (weight("first", lf) + weight("last", ll) + weight("dob", ld) + weight("sex", ls)
                     + weight("addr", la) + weight("phone", lp) + (weight("ssn", lss) if lss else 0.0))
            if REVIEW_FROM <= score < AUTO_LINK:
                same = x["pid"] == y["pid"]
                r = rng.random()
                dec = ("Same patient" if same else "Different patients") if r > 0.035 else "Cannot determine"
                if r < 0.012:
                    dec = "Different patients" if same else "Same patient"
                lab = {"exact": "Exact", "equiv": "Nickname", "similar": "Similar", "diff": "Different",
                       "partial": "Partial", "same": "Same"}
                rows.append(dict(CB_MRN=x["mrn"], RMG_PATIENT_ID=y["mrn"], SCORE=round(score, 1),
                                 FIRST=lab[lf], LAST=lab[ll], DOB=lab[ld], SEX=lab[ls], ADDRESS=lab[la],
                                 PHONE=lab[lp], SSN=lab[lss] if lss else "Missing", HIM_DECISION=dec))
    df = pd.DataFrame(rows)
    df = df.sample(frac=1.0, random_state=int(P.SEED % 1000)).reset_index(drop=True)
    df.insert(0, "PAIR_ID", ["PP%05d" % (10000 + 7 * i + int(rng.integers(0, 7))) for i in range(len(df))])
    reviewers = ["L. Garza", "D. Vela", "R. Torres", "K. Pham", "M. Cantu"]
    day0 = P.PILOT[0]
    df["REVIEWED_BY"] = [reviewers[int(rng.integers(0, len(reviewers)))] for _ in range(len(df))]
    df["REVIEWED_ON"] = [(day0 + dt.timedelta(days=int(rng.integers(0, 50)))).isoformat() for _ in range(len(df))]
    return df


def registration_volumes(w):
    rows = defaultdict(int)
    for r in w.recs:
        if r["created"].year >= 2024:
            rows[(r["created"].strftime("%Y-%m"), "Calder Bay" if r["sys"] == "A" else "Rosario")] += 1
    return pd.DataFrame([dict(MONTH=k[0], GROUP=k[1], NEW_REGISTRATIONS=v) for k, v in sorted(rows.items())])


def rosario_duplicate_report(w):
    rng = np.random.default_rng(P.SEED + 111)
    rows = []
    d = dt.date(2025, 1, 1)
    while d < dt.date(2026, 11, 1):
        flagged = int(rng.normal(410, 45))
        merged = int(flagged * rng.uniform(0.48, 0.62))
        dismissed = int(flagged * rng.uniform(0.18, 0.27))
        rows.append(dict(REPORT_MONTH=d.strftime("%Y-%m"), PAIRS_FLAGGED=flagged, MERGED=merged, NOT_DUPLICATES=dismissed,
                         CARRIED_FORWARD=flagged - merged - dismissed))
        d = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    return pd.DataFrame(rows)


def frames(w):
    return dict(index_a=index_a(w), index_b=index_b(w), merges=merge_history(w), blood=blood_bank(w),
                deliveries=deliveries(w), deaths=death_notices(w), names=name_equivalents(), pilot=pilot(w),
                volumes=registration_volumes(w), dupreport=rosario_duplicate_report(w))
