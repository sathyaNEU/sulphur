"""task16 clean truth: the people of Port Calder who registered with Calder Bay Health or Rosario Medical Group from 2006
to the November 2026 extract, their families, homes, phones and identifiers; every registration as a registrar typed
it; Calder Bay's registration rule that from 4 March 2019 merged a new registration into an existing record with the
same last name, birth date and sex; Rosario's HIM merges; and the clinical events (blood bank results, deliveries,
death notices) each record carries. Each component draws from its own random stream."""
import datetime as dt
import math
import os
import zlib
from collections import defaultdict

import numpy as np
import pandas as pd

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
Y0, Y1 = 1918, 2026


class W:
    pass


def stream(tag):
    return np.random.default_rng(P.SEED + zlib.crc32(tag.encode()) % 100000)


# ---------------------------------------------------------------------------------------------------------------
# names
# ---------------------------------------------------------------------------------------------------------------

def first_name_tables():
    out = {}
    years = np.arange(Y0, Y1 + 1)
    for key, txt in P.FIRST_NAMES.items():
        rows = [r.split() for r in txt.replace("\n", "").split(";") if r.strip()]
        names = [r[0] for r in rows]
        peak = np.array([float(r[1]) for r in rows])
        width = np.array([float(r[2]) for r in rows])
        wt = np.array([float(r[3]) for r in rows])
        m = wt[None, :] * np.exp(-0.5 * ((years[:, None] - peak[None, :]) / width[None, :]) ** 2)
        m = m / m.sum(axis=1, keepdims=True)
        out[key] = (np.array(names), np.cumsum(m, axis=1))
    return out


def first_name_tail():
    """The uncommon first names a share of each community gives its children: the Census Bureau's 1990 first-name
    frequencies by sex, the names the cohort curves already carry left out."""
    core = {sex: set() for sex in "FM"}
    for (g, sex), txt in P.FIRST_NAMES.items():
        core[sex] |= {r.split()[0] for r in txt.replace("\n", "").split(";") if r.strip()}
    out = {}
    for sex, fname in (("F", "census1990_first_female.txt"), ("M", "census1990_first_male.txt")):
        rows = [ln.split() for ln in open(os.path.join(HERE, fname)) if ln.strip()]
        names = np.array([r[0] for r in rows if r[0] not in core[sex]])
        w = np.array([float(r[1]) for r in rows if r[0] not in core[sex]])
        out[sex] = (names, np.cumsum(w / w.sum()))
    return out


def surname_tables():
    c = pd.read_csv(os.path.join(HERE, "census2010_surnames.csv"), keep_default_na=False, dtype={"name": str})
    out = {}
    for g, col in (("H", "pcthispanic"), ("W", "pctwhite"), ("B", "pctblack"), ("O", None)):
        w = c["count"].to_numpy(float) * (c[col].to_numpy(float) / 100.0 if col else 1.0)
        if g == "H":
            boost = c["name"].map(P.SOUTH_TEXAS_BOOST).fillna(1.0).to_numpy(float)
            w = w * boost
        keep = w > 0
        out[g] = (c["name"].to_numpy()[keep], np.cumsum(w[keep] / w[keep].sum()))
    v = c[c["name"].isin(P.VIET_SURNAMES)]
    w = v["count"].to_numpy(float) * v["pctapi"].to_numpy(float) / 100.0
    out["V"] = (v["name"].to_numpy(), np.cumsum(w / w.sum()))
    return out


def draw(cum, u):
    return np.minimum(np.searchsorted(cum, u), len(cum) - 1)


# ---------------------------------------------------------------------------------------------------------------
# the people: families, twins, homes and identifiers
# ---------------------------------------------------------------------------------------------------------------

def birth_day(rng, year, n=None):
    """A birth date in a year, births a little more common in late summer."""
    doy = rng.integers(0, 365, size=n)
    lift = rng.random(size=n) < 0.06
    doy = np.where(lift, rng.integers(200, 275, size=n), doy)
    if n is None:
        return dt.date(int(year), 1, 1) + dt.timedelta(days=int(doy))
    return [dt.date(int(y), 1, 1) + dt.timedelta(days=int(d)) for y, d in zip(np.broadcast_to(year, n), doy)]


def foreign_share(g, year):
    for a, b, p in P.FOREIGN[g]:
        if a <= year <= b:
            return p
    return 0.0


def people(w):
    rng = stream("people")
    fn = first_name_tables()
    tail = first_name_tail()
    rt = stream("first_tail")
    sn = surname_tables()
    persons = []

    def new_person(fam, role, g, sex, bdate, surname_p, surname_m, foreign, side):
        pid = len(persons)
        yi = min(max(bdate.year, Y0), Y1) - Y0
        names, cum = fn[(g, sex)]
        first = names[draw(cum[yi], rng.random())]
        if rt.random() < P.FIRST_TAIL[g]:
            tn, tc = tail[sex]
            first = tn[draw(tc, rt.random())]
        p = dict(pid=pid, fam=fam, role=role, g=g, sex=sex, dob=bdate, first=first, sur_p=surname_p, sur_m=surname_m,
                 foreign=foreign, side=side, twin=-1, mz=False, married_name=None, married_on=None, compound=False,
                 death=None, ssn=None, abo=None, home=[], phone=[], subscriber=None, middle="")
        persons.append(p)
        return p

    def surname(g):
        names, cum = sn[g]
        return names[draw(cum, rng.random())]

    def legal_dob(g, year, foreign):
        if foreign:
            r = rng.random()
            if r < P.JAN1_FOREIGN[g]:
                return dt.date(int(year), 1, 1)
            if r < P.JAN1_FOREIGN[g] + P.JUL1_FOREIGN[g]:
                return dt.date(int(year), 7, 1)
        return birth_day(rng, year)

    gs = rng.choice(len(P.GROUPS), size=P.N_FAMILIES, p=P.GROUP_P)
    for fam in range(P.N_FAMILIES):
        g = P.GROUPS[gs[fam]]
        side = "north" if rng.random() < P.NORTH_P[g] else "south"
        # the family head's birth year: the patients born 1925 to 2004
        hy = int(np.clip(rng.normal(1968, 17), 1925, 2004))
        kind = rng.choice(["couple_kids", "couple", "single_parent", "single"], p=[0.50, 0.17, 0.13, 0.20])
        mfor = rng.random() < foreign_share(g, hy)
        if kind == "single":
            sex = "F" if rng.random() < 0.52 else "M"
            sp = surname(g)
            p = new_person(fam, "adult", g, sex, legal_dob(g, hy, mfor), sp, surname(g) if g == "H" else None, mfor, side)
            p["compound"] = g == "H" and mfor and rng.random() < P.COMPOUND_SURNAME["H"] * 1.4
            continue
        mother_p = surname(g)
        mother = new_person(fam, "mother", g, "F", legal_dob(g, hy, mfor), mother_p,
                            surname(g) if g == "H" else None, mfor, side)
        father = None
        if kind in ("couple_kids", "couple"):
            fy = int(np.clip(hy + rng.normal(2.5, 3.5), 1922, 2004))
            ffor = mfor if rng.random() < 0.85 else (rng.random() < foreign_share(g, fy))
            father = new_person(fam, "father", g, "M", legal_dob(g, fy, ffor), surname(g),
                                surname(g) if g == "H" else None, ffor, side)
            wed = dt.date(int(min(hy + rng.integers(19, 31), 2025)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            if rng.random() < P.TAKES_SPOUSE_NAME[g]:
                mother["married_name"] = father["sur_p"]
                mother["married_on"] = wed
        for q in (mother, father):
            if q is not None and g == "H":
                q["compound"] = rng.random() < (P.COMPOUND_SURNAME["H"] * (1.5 if q["foreign"] else 0.7))
        if kind in ("couple_kids", "single_parent"):
            mean_k = {"H": 2.6, "W": 2.0, "B": 2.3, "V": 2.4, "O": 2.1}[g] * (1.15 if hy < 1960 else 1.0)
            nk = max(1, min(7, int(rng.poisson(mean_k))))
            ages = np.sort(rng.integers(18, 41, size=nk))
            dad_sur = father["sur_p"] if father is not None else mother_p
            for a in ages:
                by = hy + int(a)
                if by > 2026:
                    continue
                bd = birth_day(rng, by)
                if bd >= P.EXTRACT:
                    continue
                kfor = mfor and by < hy + 26 and rng.random() < 0.55
                if kfor:
                    bd = legal_dob(g, by, True)
                twins = rng.random() < P.TWIN_RATE
                n = 2 if twins else 1
                sex1 = "F" if rng.random() < 0.49 else "M"
                kids = []
                for j in range(n):
                    sx = sex1
                    if j == 1 and rng.random() > P.TWIN_SAME_SEX:
                        sx = "M" if sex1 == "F" else "F"
                    k = new_person(fam, "child", g, sx, bd, dad_sur, mother_p if g == "H" else None, kfor, side)
                    k["compound"] = g == "H" and rng.random() < P.COMPOUND_SURNAME["H"] * (1.3 if kfor else 0.75)
                    kids.append(k)
                if twins:
                    a1, a2 = kids
                    a1["twin"], a2["twin"] = a2["pid"], a1["pid"]
                    if a1["sex"] == a2["sex"] and rng.random() < P.TWIN_MZ_GIVEN_SAME_SEX:
                        a1["mz"] = a2["mz"] = True
                    r = rng.random()
                    if r < P.TWIN_SAME_NAME:
                        a2["first"] = a1["first"]
                    elif r < P.TWIN_SAME_NAME + P.TWIN_SIMILAR_NAMES and a1["sex"] == a2["sex"]:
                        a2["first"] = similar_name(rng, a1["first"], fn[(g, a1["sex"])][0])
                    elif a2["first"] == a1["first"]:
                        names, cum = fn[(g, a2["sex"])]
                        a2["first"] = names[draw(cum[min(max(bd.year, Y0), Y1) - Y0], rng.random())]
    w.persons = persons
    w.n = len(persons)


TWIN_PAIRS = {
    # boys
    "Jayden": ["Jaden", "Jaiden"], "Jaden": ["Jayden", "Jaiden"], "Aiden": ["Aidan", "Ayden"], "Mateo": ["Matteo"],
    "Adrian": ["Adrien"], "Angel": ["Angelo"], "Julian": ["Julien"], "Isaac": ["Isac"], "Josiah": ["Josias"],
    "Lucas": ["Luca", "Lukas"], "Nathan": ["Nathaniel"], "Ethan": ["Ethen"], "Elijah": ["Elias"], "Gabriel": ["Gabriele"],
    "Daniel": ["Danial"], "Christopher": ["Cristopher"], "Jonathan": ["Johnathan"], "Brandon": ["Brendan"],
    "Jackson": ["Jaxson"], "Mason": ["Maison"], "Carter": ["Karter"], "Caleb": ["Kaleb"], "Eric": ["Erik"],
    "Brian": ["Bryan"], "Steven": ["Stephen"], "Kevin": ["Kelvin"], "Ivan": ["Ivano"], "Diego": ["Dieguito"],
    "Santiago": ["Santino"], "Sebastian": ["Sebastien"], "Emiliano": ["Emilio"], "Leonardo": ["Leonard"],
    # girls
    "Isabella": ["Isabel", "Isabelle"], "Isabel": ["Isabella", "Isabelle"], "Ava": ["Avah"], "Emma": ["Ema"],
    "Valeria": ["Valerie"], "Jasmine": ["Jasmin"], "Kaylee": ["Kaylie"], "Natalie": ["Natalia", "Nathalie"],
    "Sofia": ["Sofie"], "Camila": ["Camilla"], "Hannah": ["Hanna"], "Destiny": ["Destinee"], "Aaliyah": ["Aliyah"],
    "Emily": ["Emely"], "Abigail": ["Abigale"], "Gabriela": ["Gabriella"], "Juliana": ["Julianna"],
    "Adriana": ["Adrianna"], "Alyssa": ["Alissa"], "Ashley": ["Ashlee"], "Kaitlyn": ["Katelyn"], "Madison": ["Madisyn"],
    "Allison": ["Alison"], "Mia": ["Miah"], "Ximena": ["Jimena"], "Daniela": ["Daniella"], "Mariana": ["Marianna"],
    "Andrea": ["Andria"], "Alejandra": ["Alexandra"], "Victoria": ["Viktoria"], "Samantha": ["Samanta"],
}


def similar_name(rng, name, pool):
    opts = TWIN_PAIRS.get(name)
    if opts:
        return opts[int(rng.integers(0, len(opts)))]
    # a rhyme or alliteration from the same pool: share the first two letters
    cands = [x for x in pool if x != name and x[:2] == name[:2]]
    if cands:
        return cands[int(rng.integers(0, len(cands)))]
    return name + "e" if not name.endswith("e") else name[:-1] + "a"


def homes_and_ids(w):
    """Addresses and phones over time (a family moves together; children leave around 21), SSNs, blood groups,
    middle names and deaths."""
    rng = stream("homes")
    fams = defaultdict(list)
    for p in w.persons:
        fams[p["fam"]].append(p)

    def address():
        num = int(rng.integers(100, 9999))
        st = P.STREETS[int(rng.integers(0, len(P.STREETS)))]
        suf = P.SUFFIX[int(rng.integers(0, len(P.SUFFIX)))]
        unit = ("Apt %d%s" % (int(rng.integers(1, 30)), "ABCD"[int(rng.integers(0, 4))])) if rng.random() < 0.38 else ""
        return (num, st, suf, unit)

    def phone():
        n = int(rng.integers(2000000, 9999999))
        if n // 10000 == 555:                # the 555 exchange is not assigned to subscribers
            n += 10000
        return "361%07d" % n

    def history(start, end, rate):
        out = []
        t = start
        while t < end:
            out.append(t)
            t = t + dt.timedelta(days=int(rng.exponential(365.0 / rate)) + 30)
        return out

    T0, T1 = dt.date(2004, 1, 1), P.EXTRACT
    for fam, mem in fams.items():
        renter = rng.random() < 0.45
        rate = 0.15 if renter else 0.07
        moves = history(T0, T1, rate)
        fam_addr = [(t, address()) for t in moves]
        land = phone() if rng.random() < 0.55 else None
        land_hist = [(T0, land)] if land else []
        for p in mem:
            leave = None
            if p["role"] == "child":
                leave = p["dob"] + dt.timedelta(days=int(365.25 * (20 + rng.normal(1.5, 2.0))))
            hist = [(t, a) for (t, a) in fam_addr if leave is None or t < leave]
            if leave is not None and leave < T1:
                own = history(max(leave, T0), T1, 0.18)
                hist += [(t, address()) for t in own]
            if not hist:
                hist = [(T0, address())]
            p["home"] = hist
            mob = []
            if p["role"] != "child" or (p["dob"] < T1 - dt.timedelta(days=365 * 14)):
                t = T0
                while t < T1:
                    mob.append((t, phone()))
                    t = t + dt.timedelta(days=int(rng.exponential(365 * 6)) + 200)
            p["phone"] = land_hist + mob if land_hist and rng.random() < 0.5 else (mob or land_hist)
            if not p["phone"]:
                mom = next((q for q in mem if q["role"] == "mother"), None)
                p["phone"] = mom["phone"] if mom and mom["phone"] else [(T0, phone())]
            # identifiers
            us_born = not p["foreign"]
            has_ssn = (rng.random() < 0.96) if us_born else (rng.random() < (0.72 if p["g"] == "H" else 0.9))
            p["ssn"] = "%03d%02d%04d" % (int(rng.integers(1, 899)), int(rng.integers(1, 99)),
                                          int(rng.integers(1, 9999))) if has_ssn else None
            dist = P.ABO_RH[p["g"]]
            p["abo"] = rng.choice(list(dist.keys()), p=np.array(list(dist.values())) / sum(dist.values()))
            mid_pool = ["A", "B", "C", "D", "E", "F", "G", "J", "L", "M", "N", "R", "S", "T", "V"]
            p["middle"] = mid_pool[int(rng.integers(0, len(mid_pool)))] if rng.random() < 0.7 else ""
            age_2016 = (dt.date(2016, 1, 1) - p["dob"]).days / 365.25
            hz = 0.000022 * math.exp(0.096 * max(age_2016, 0))
            if rng.random() < 1 - math.exp(-hz * 10.8):
                p["death"] = dt.date(2016, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3950)))
                if p["death"] >= P.EXTRACT:
                    p["death"] = None
        # twins share blood groups when identical; a dependent's subscriber is a parent
        for p in mem:
            if p["twin"] >= 0 and p["mz"]:
                tw = w.persons[p["twin"]]
                if p["pid"] < tw["pid"]:
                    tw["abo"] = p["abo"]
            if p["role"] == "child":
                par = [q for q in mem if q["role"] in ("mother", "father") and q["ssn"]]
                p["subscriber"] = par[int(rng.integers(0, len(par)))]["ssn"] if par else None


def at(hist, d):
    v = hist[0][1]
    for t, x in hist:
        if t <= d:
            v = x
        else:
            break
    return v


# ---------------------------------------------------------------------------------------------------------------
# registrations: what each registrar typed
# ---------------------------------------------------------------------------------------------------------------

NICK = {}


def load_nicknames():
    from nicknames import PAIRS
    for formal, nicks in PAIRS.items():
        NICK[formal.upper()] = [n.upper() for n in nicks]


def typo(rng, s):
    if len(s) < 3:
        return s
    i = int(rng.integers(1, len(s)))
    r = rng.random()
    if r < 0.4:
        return s[:i] + s[i + 1:]
    if r < 0.7 and i < len(s) - 1:
        return s[:i] + s[i + 1] + s[i] + s[i + 2:]
    letters = "AEIOURSTLNMHCDY"
    return s[:i] + letters[int(rng.integers(0, len(letters)))] + s[i + 1:]


def entered_last(rng, p, d):
    """The last name a registrar typed on day d."""
    if p["married_name"] and p["married_on"] and d >= p["married_on"] and rng.random() > 0.08:
        base = p["married_name"]
        if p["g"] == "H" and rng.random() < 0.18:
            base = p["sur_p"] + " " + p["married_name"]     # de casada, both
        return base
    if p["compound"] and p["sur_m"]:
        r = rng.random()
        acc = 0.0
        for form, q in P.COMPOUND_FORMS:
            acc += q
            if r < acc:
                break
        if form == "both":
            return p["sur_p"] + " " + p["sur_m"]
        if form == "hyphen":
            return p["sur_p"] + "-" + p["sur_m"]
        if form == "maternal":
            return p["sur_m"]
        return p["sur_p"]
    return p["sur_p"]


def entered(rng, p, d, system, newborn=False):
    first = p["first"].upper()
    last = entered_last(rng, p, d).upper()
    adult = (d - p["dob"]).days > 365 * 16
    if newborn:
        first = ("BABY%s" % ("GIRL" if p["sex"] == "F" else "BOY"))
    else:
        if adult and first in NICK and rng.random() < P.P_NICKNAME:
            opts = NICK[first]
            first = opts[int(rng.integers(0, len(opts)))]
        if p["g"] == "H" and p["sex"] == "F" and p["first"] == "Maria" and p["middle"] and rng.random() < 0.25:
            first = "MARIA " + {"E": "ELENA", "G": "GUADALUPE", "D": "DE LOS ANGELES", "L": "LUISA", "T": "TERESA",
                                "C": "CRISTINA", "J": "JOSEFINA"}.get(p["middle"], "ELENA")
        if rng.random() < P.P_TYPO_FIRST:
            first = typo(rng, first)
    if rng.random() < P.P_TYPO_LAST:
        last = typo(rng, last)
    if p["g"] == "V" and p["foreign"] and adult and rng.random() < P.P_VIET_ORDER_SWAP:
        first, last = last, first
    dob = p["dob"]
    r = rng.random()
    if r < P.P_DOB_SWAP and dob.day <= 12 and dob.day != dob.month:
        dob = dt.date(dob.year, dob.day, dob.month)
    elif r < P.P_DOB_SWAP + P.P_DOB_YEAR:
        dob = dt.date(dob.year + (1 if rng.random() < 0.5 else -1), dob.month, min(dob.day, 28))
    elif r < P.P_DOB_SWAP + P.P_DOB_YEAR + P.P_DOB_DAY:
        dob = dt.date(dob.year, dob.month, max(1, min(28, dob.day + int(rng.choice([-1, 1, 10, -10])))))
    if dob > (d.date() if hasattr(d, "date") else d):
        dob = p["dob"]                       # the registration screen refuses a birth date after the visit
    sex = p["sex"] if rng.random() > P.P_SEX_ERR else ("M" if p["sex"] == "F" else "F")
    num, st, suf, unit = at(p["home"], d)
    if unit and rng.random() < P.P_UNIT_DROPPED:
        unit = ""
    addr = (num, st, suf, unit)
    ph = at(p["phone"], d)
    ssn = None
    age = (d - p["dob"]).days / 365.25
    if age >= 18:
        if p["ssn"] and rng.random() < P.P_SSN_ADULT[system]:
            ssn = p["ssn"]
    elif system == "B" and d < P.B_SUBSCRIBER_SSN_UNTIL and p["subscriber"] and rng.random() < P.P_SUBSCRIBER_SSN_CHILD:
        ssn = p["subscriber"]
    if ssn and rng.random() < P.P_SSN_TYPO:
        k = int(rng.integers(0, 9))
        ssn = ssn[:k] + str(int(rng.integers(0, 10))) + ssn[k + 1:]
    if ssn is None and rng.random() < P.P_SSN_PLACEHOLDER[system]:
        ssn = "999999999" if system == "B" else "000000000"
    return dict(first=first, middle=p["middle"], last=last, dob=dob, sex=sex, addr=addr, phone=ph, ssn=ssn)


def registrations(w):
    """Every registration that created a record in either index, in time order per system."""
    load_nicknames()
    rng = stream("registrations")
    recs = []
    births = []
    first_visit = {}
    first_ts = {}
    # which group each person uses, and where each child born since 2006 was delivered
    for p in w.persons:
        north = p["side"] == "north"
        ua = rng.random() < P.USE_A[p["side"]]
        ub = rng.random() < P.USE_B[p["side"]]
        if not ua and not ub:
            if north:
                ua = True
            else:
                ub = True
        p["birth_sys"] = None
        if p["dob"] >= P.FIRST_REG:
            tw = p["twin"]
            if 0 <= tw < p["pid"]:
                p["birth_sys"] = w.persons[tw]["birth_sys"]
            else:
                p["birth_sys"] = "A" if (rng.random() < (0.78 if north else 0.24)) else "B"
            if p["birth_sys"] == "A":
                ua = True
            else:
                ub = True
        p["uses"] = [s for s, u in (("A", ua), ("B", ub)) if u]
    # a mother who delivered at a hospital is registered there before her first delivery there
    must_by = {}
    for p in w.persons:
        if p["birth_sys"] and p["role"] == "child":
            mom = next((q for q in w.persons_by_fam[p["fam"]] if q["role"] == "mother"), None)
            if mom is not None:
                key = (mom["pid"], p["birth_sys"])
                must_by[key] = min(must_by.get(key, p["dob"]), p["dob"])
                if p["birth_sys"] not in mom["uses"]:
                    mom["uses"].append(p["birth_sys"])
    for p in w.persons:
        north = p["side"] == "north"
        end = min(p["death"] or P.EXTRACT, P.EXTRACT)
        start = max(P.FIRST_REG, p["dob"])
        birth_sys = p["birth_sys"]
        for s in p["uses"]:
            if (end - start).days < 2:
                continue
            if birth_sys == s:
                d0 = p["dob"]
                newborn = True
            else:
                d0 = start + dt.timedelta(days=int(rng.integers(0, max(1, (end - start).days))))
                newborn = False
                cap = must_by.get((p["pid"], s))
                if cap is not None and d0 >= cap:
                    lo = max(start, cap - dt.timedelta(days=400))
                    d0 = lo + dt.timedelta(days=int(rng.integers(0, max(1, (cap - lo).days))))
                # twins are usually brought in together: the second twin's first registration on the same visit
                tw = p["twin"]
                if 0 <= tw < p["pid"] and (tw, s) in first_visit and start <= first_visit[(tw, s)] < end and rng.random() < 0.72:
                    d0 = first_visit[(tw, s)]
            first_visit[(p["pid"], s)] = d0
            regs = [(d0, newborn)]
            lam = P.DUP_BASE[s] + (P.DUP_COMPOUND if p["compound"] else 0) + (P.DUP_VIET if p["g"] == "V" else 0)
            if p["first"].upper() in NICK:
                lam += P.DUP_NICK
            ndup = int(rng.poisson(lam * min(1.0, (end - d0).days / 3650.0) * 1.6))
            for _ in range(ndup):
                if (end - d0).days > 3:
                    regs.append((d0 + dt.timedelta(days=int(rng.integers(1, (end - d0).days))), False))
            if p["married_on"] and d0 < p["married_on"] < end and rng.random() < P.P_MARRIED_NEW_RECORD:
                regs.append((p["married_on"] + dt.timedelta(days=int(rng.integers(30, 900))), False))
            for d, nb in regs:
                if d >= end:
                    continue
                e = entered(rng, p, d, s, newborn=nb)
                hh = int(rng.integers(6, 22)) if not nb else int(rng.integers(0, 24))
                ts = dt.datetime(d.year, d.month, d.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
                tw = p["twin"]
                if 0 <= tw < p["pid"] and (tw, s, d) in first_ts:
                    ts = first_ts[(tw, s, d)] + dt.timedelta(minutes=int(rng.integers(2, 25)))
                first_ts[(p["pid"], s, d)] = ts
                recs.append(dict(sys=s, pid=p["pid"], created=ts, newborn=nb, **e))
                if nb:
                    births.append((s, p["pid"], ts))
    recs.sort(key=lambda r: (r["sys"], r["created"], r["pid"]))
    w.recs = recs
    w.births = births


# ---------------------------------------------------------------------------------------------------------------
# the indexes: MRNs, Calder Bay's 2019 merge rule, Rosario's HIM merges
# ---------------------------------------------------------------------------------------------------------------

def std(s):
    return "".join(ch for ch in s.upper().replace("-", " ") if ch.isalpha() or ch == " ").strip()


def indexes(w):
    rng = stream("indexes")
    mrn_a = 1000000 + int(rng.integers(0, 50000))
    mrn_b = 20000000 + int(rng.integers(0, 50000))
    by_key = {}
    merges = []
    for r in w.recs:
        if r["sys"] == "A":
            mrn_a += int(rng.integers(1, 4))
            r["mrn"] = "CB%07d" % mrn_a
        else:
            mrn_b += int(rng.integers(1, 3))
            r["mrn"] = "%08d" % mrn_b
        r["survivor"] = r["mrn"]
        r["retired"] = False
    # Calder Bay: from 4 March 2019 a new registration with the same last name, birth date and sex as an existing
    # record is merged into the earliest such record (newborn registrations bypass the rule)
    for r in w.recs:
        if r["sys"] != "A":
            continue
        key = (std(r["last"]), r["dob"], r["sex"])
        if r["created"] >= P.A_AUTOMERGE_FROM and not r["newborn"] and key in by_key:
            surv = by_key[key]
            r["retired"] = True
            r["survivor"] = surv["mrn"]
            merges.append(dict(survivor=surv["mrn"], retired=r["mrn"], when=r["created"], method="AUTO-LDS", rec=r))
        else:
            by_key.setdefault(key, r)
    # HIM manual merges in Calder Bay: duplicates of one patient found later (always the same patient)
    act = defaultdict(list)
    for r in w.recs:
        if r["sys"] == "A" and not r["retired"]:
            act[r["pid"]].append(r)
    for pid, rs in act.items():
        if len(rs) < 2:
            continue
        for r in rs[1:]:
            if rng.random() < 0.38:
                when = r["created"] + dt.timedelta(days=int(rng.integers(20, 900)))
                if when.date() >= P.EXTRACT:
                    continue
                r["retired"] = True
                r["survivor"] = rs[0]["mrn"]
                merges.append(dict(survivor=rs[0]["mrn"], retired=r["mrn"], when=when, method="HIM", rec=r))
    # Rosario: HIM merges duplicates its monthly report shows (no log in the extract)
    act = defaultdict(list)
    for r in w.recs:
        if r["sys"] == "B":
            act[r["pid"]].append(r)
    for pid, rs in act.items():
        for r in rs[1:]:
            exactish = (std(r["first"]) == std(rs[0]["first"]) and std(r["last"]) == std(rs[0]["last"])
                        and r["dob"] == rs[0]["dob"])
            if (exactish and rng.random() < P.B_HIM_MERGE + 0.25) or (not exactish and rng.random() < P.B_HIM_MERGE * 0.5):
                r["retired"] = True
                r["survivor"] = rs[0]["mrn"]
    # a retired record's survivor may itself be retired later (Calder Bay): follow the chain
    by_mrn = {r["mrn"]: r for r in w.recs}
    for r in w.recs:
        s = r["survivor"]
        seen = 0
        while by_mrn[s]["retired"] and by_mrn[s]["survivor"] != s and seen < 10:
            s = by_mrn[s]["survivor"]
            seen += 1
        r["final"] = s
    w.merges = merges
    w.by_mrn = by_mrn
    # who each active record holds
    holds = defaultdict(set)
    for r in w.recs:
        holds[r["final"]].add(r["pid"])
    w.holds = holds


# ---------------------------------------------------------------------------------------------------------------
# what each active record carries now: current demographics, last activity, clinical events
# ---------------------------------------------------------------------------------------------------------------

def activity(w):
    rng = stream("activity")
    # each person's active records per system (what a registrar finds at a visit)
    mine = defaultdict(list)
    for r in w.recs:
        mine[(r["pid"], r["sys"])].append(r["final"])
    w.mine = {k: sorted(set(v)) for k, v in mine.items()}
    last = {}
    for r in w.recs:
        p = w.persons[r["pid"]]
        end = min(p["death"] or P.EXTRACT, P.EXTRACT)
        la = r["created"].date() + dt.timedelta(days=int(rng.integers(0, max(1, (end - r["created"].date()).days))))
        f = r["final"]
        last[f] = max(last.get(f, la), la)
    w.last_activity = last
    # current address and phone on each active record: updated at a later visit after a move
    for r in w.recs:
        if r["retired"]:
            continue
        p = w.persons[r["pid"]]
        la = last[r["mrn"]]
        if rng.random() < P.P_ADDR_UPDATE:
            num, st, suf, unit = at(p["home"], la)
            if unit and rng.random() < P.P_UNIT_DROPPED:
                unit = ""
            r["addr_now"] = (num, st, suf, unit)
        else:
            r["addr_now"] = r["addr"]
        r["phone_now"] = at(p["phone"], la) if rng.random() < P.P_PHONE_UPDATE else r["phone"]
        if r["newborn"]:
            r["first_now"] = p["first"].upper()        # the newborn's name entered once known
        else:
            r["first_now"] = r["first"]


def clinical(w):
    rng = stream("clinical")
    tests = []
    deliveries = []
    deaths = []

    def record_at(pid, s):
        ms = w.mine.get((pid, s))
        if not ms:
            return None
        return ms[int(rng.integers(0, len(ms)))]

    for p in w.persons:
        end = min(p["death"] or P.EXTRACT, P.EXTRACT)
        for s in p.get("uses", []):
            age = (dt.date(2021, 1, 1) - p["dob"]).days / 365.25
            rate = 0.035 + (0.04 if age > 55 else 0.0) + (0.03 if p["sex"] == "F" and 18 < age < 42 else 0.0)
            n = int(rng.poisson(rate * 9))
            for _ in range(n):
                d0 = max(P.FIRST_REG, p["dob"], dt.date(2016, 1, 1))
                if (end - d0).days < 2:
                    continue
                d = d0 + dt.timedelta(days=int(rng.integers(0, (end - d0).days)))
                m = record_at(p["pid"], s)
                if m is None:
                    continue
                abo = p["abo"]
                if rng.random() < P.WBIT:
                    abo = rng.choice(["O+", "A+", "B+", "AB+", "O-", "A-"])
                tests.append(dict(sys=s, mrn=m, when=dt.datetime(d.year, d.month, d.day, int(rng.integers(0, 24)),
                                                                   int(rng.integers(0, 60))), abo=abo))
        if p["death"] and p["death"] >= dt.date(2016, 1, 1):
            for s in p.get("uses", []):
                for m in w.mine.get((p["pid"], s), []):
                    deaths.append(dict(sys=s, mrn=m, died=p["death"]))
    # deliveries: each newborn record with its mother's record in the same index
    for s, pid, ts in w.births:
        p = w.persons[pid]
        fam_mother = next((q for q in w.persons_by_fam[p["fam"]] if q["role"] == "mother"), None)
        mm = None
        if fam_mother is not None:
            mm = record_at(fam_mother["pid"], s)
        rec = next(r for r in w.recs_by_pid[pid] if r["sys"] == s and r["newborn"])
        wt = int(np.clip(rng.normal(3350 if p["twin"] < 0 else 2450, 480), 700, 5200))
        deliveries.append(dict(sys=s, newborn_mrn=rec["final"], born_mrn=rec["mrn"], mother_mrn=mm,
                               when=ts, sex=p["sex"], grams=wt, pid=pid))
    w.tests, w.deliveries, w.deaths = tests, deliveries, deaths


RENAME_FIRST = {"CLAUDE": "CLYDE", "WHITNEY": "BRITTANY"}
RENAME_LAST = {"WHITNEY": "WHITLEY"}


def build():
    w = W()
    people(w)
    for p in w.persons:                      # names the client's file checks read as tool or project names
        p["first"] = RENAME_FIRST.get(p["first"], p["first"])
        for k in ("sur_p", "sur_m", "married_name"):
            if p.get(k):
                p[k] = RENAME_LAST.get(p[k], p[k])
    homes_and_ids(w)
    w.persons_by_fam = defaultdict(list)
    for p in w.persons:
        w.persons_by_fam[p["fam"]].append(p)
    registrations(w)
    w.recs_by_pid = defaultdict(list)
    for r in w.recs:
        w.recs_by_pid[r["pid"]].append(r)
    indexes(w)
    activity(w)
    clinical(w)
    return w
