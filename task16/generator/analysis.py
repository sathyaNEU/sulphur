"""task16 analysis, read from the pack: the candidate rules' links, the evidence that two records belong to two people,
each rule's false merges by the golden method and by the hurried routes, Calder Bay's overlays, and the linked index
(distinct patients, patients in both indexes, patients left under more than one record)."""
import math
from collections import defaultdict

import numba
import numpy as np
import pandas as pd

CAP_PER = 2000.0
RULES = ["A", "B", "C", "D"]


# ---------------------------------------------------------------------------------------------------------------
# string similarity on coded names
# ---------------------------------------------------------------------------------------------------------------

@numba.njit(cache=True)
def _jw(a, la, b, lb):
    if la == lb:
        same = True
        for i in range(la):
            if a[i] != b[i]:
                same = False
                break
        if same:
            return 1.0
    if la == 0 or lb == 0:
        return 0.0
    md = max(max(la, lb) // 2 - 1, 0)
    ma = np.zeros(la, np.bool_)
    mb = np.zeros(lb, np.bool_)
    m = 0
    for i in range(la):
        lo = max(0, i - md)
        hi = min(lb, i + md + 1)
        for j in range(lo, hi):
            if not mb[j] and b[j] == a[i]:
                ma[i] = True
                mb[j] = True
                m += 1
                break
    if m == 0:
        return 0.0
    k = 0
    tr = 0
    for i in range(la):
        if ma[i]:
            while not mb[k]:
                k += 1
            if a[i] != b[k]:
                tr += 1
            k += 1
    jaro = (m / la + m / lb + (m - tr / 2.0) / m) / 3.0
    pre = 0
    for i in range(min(4, min(la, lb))):
        if a[i] == b[i]:
            pre += 1
        else:
            break
    return jaro + pre * 0.1 * (1.0 - jaro)


@numba.njit(cache=True)
def _jw_pairs(codes, lens, ia, ib):
    out = np.empty(len(ia), np.float32)
    for k in range(len(ia)):
        out[k] = _jw(codes[ia[k]], lens[ia[k]], codes[ib[k]], lens[ib[k]])
    return out


class Vocab:
    """Names coded once, so similarity runs over integer codes."""

    def __init__(self, names):
        u = sorted(set(names))
        self.index = {s: i for i, s in enumerate(u)}
        self.names = u
        L = max(1, max((len(s) for s in u), default=1))
        self.codes = np.zeros((len(u), L), np.uint8)
        self.lens = np.zeros(len(u), np.int64)
        for i, s in enumerate(u):
            bs = s.encode("ascii", "ignore")
            self.codes[i, :len(bs)] = np.frombuffer(bs, np.uint8)
            self.lens[i] = len(bs)

    def code(self, series):
        return series.map(self.index).to_numpy(np.int64)

    def jw(self, ca, cb):
        return _jw_pairs(self.codes, self.lens, np.asarray(ca, np.int64), np.asarray(cb, np.int64))


def jw(a, b):
    v = Vocab([a, b])
    return float(v.jw([v.index[a]], [v.index[b]])[0])


# ---------------------------------------------------------------------------------------------------------------
# name equivalence (the engine's table) and the rules
# ---------------------------------------------------------------------------------------------------------------

def equivalents(names_df):
    eq = defaultdict(set)
    for n, e in zip(names_df["NAME"], names_df["EQUIVALENT"]):
        eq[n].add(n)
        eq[e].add(n)
    return eq


def first_equiv(a, b, eq, sim):
    """The rule's first-name test: the same, equivalent in the table, or Jaro-Winkler 0.92 or more."""
    return a == b or bool(eq.get(a, set()) & eq.get(b, set())) or sim >= 0.92


def group_pairs(keys, mask=None):
    """Every pair of rows sharing a key (rows where mask is false are left out)."""
    df = pd.DataFrame({"k": keys})
    if mask is not None:
        df = df[mask]
    df["i"] = df.index.to_numpy()
    g = df.groupby("k")["i"].apply(list)
    ia, ib = [], []
    for rows in g:
        if len(rows) < 2:
            continue
        rows = sorted(rows)
        for x in range(len(rows)):
            for y in range(x + 1, len(rows)):
                ia.append(rows[x])
                ib.append(rows[y])
    return np.array(ia, np.int64), np.array(ib, np.int64)


def rule_links(R, eq, voc):
    """The record pairs each candidate rule joins: rule A on first, last, birth date and sex; B adds the street
    address; C on last, birth date and sex with the first names the same, equivalent or similar at 0.92 and the
    address or phone the same; D on SSN and birth date."""
    out = {}
    dob = R["dob"].dt.strftime("%Y%m%d")
    kA = R["first"] + "|" + R["last"] + "|" + dob + "|" + R["sex"]
    ia, ib = group_pairs(kA.to_numpy())
    out["A"] = (ia, ib)
    addr = R["addr"].to_numpy()
    same_addr = (addr[ia] == addr[ib]) & (addr[ia] != "")
    out["B"] = (ia[same_addr], ib[same_addr])
    kC = R["last"] + "|" + dob + "|" + R["sex"]
    ca, cb = group_pairs(kC.to_numpy())
    fa, fb = R["first"].to_numpy(), R["first"].to_numpy()
    sim = voc.jw(voc.code(R["first"].iloc[ca]), voc.code(R["first"].iloc[cb]))
    ph = R["phone"].to_numpy()
    keep = np.array([first_equiv(fa[x], fb[y], eq, s) for x, y, s in zip(ca, cb, sim)], bool)
    keep &= ((addr[ca] == addr[cb]) & (addr[ca] != "")) | ((ph[ca] == ph[cb]) & (ph[ca] != ""))
    out["C"] = (ca[keep], cb[keep])
    kD = R["ssn"] + "|" + dob
    da, db = group_pairs(kD.to_numpy(), mask=(R["ssn"] != "").to_numpy())
    out["D"] = (da, db)
    return out


# ---------------------------------------------------------------------------------------------------------------
# evidence that two records belong to two different people (fields the rules never compare)
# ---------------------------------------------------------------------------------------------------------------

def survivors(F):
    """Calder Bay MRN -> the active record it was merged into (merges followed to the end of the chain)."""
    m = F["merges"]
    nxt = dict(zip(m["RETIRED_MRN"], m["SURVIVOR_MRN"]))

    def final(x):
        seen = 0
        while x in nxt and seen < 20:
            x = nxt[x]
            seen += 1
        return x
    return final


def blood_types(F):
    """Each active record's ABO and Rh results (a record holding two patients shows two)."""
    b = F["blood"]
    fin = survivors(F)
    out = defaultdict(set)
    for mrn, abo, rh in zip(b["MRN"], b["ABO"], b["RH"]):
        out[fin(mrn) if mrn.startswith("CB") else mrn].add(abo + rh)
    return out


def newborn_mothers(F):
    """Each newborn's record with its mother's record and delivery time (deliveries followed through Calder Bay's
    merges)."""
    d = F["deliveries"]
    fin = survivors(F)
    rows = []
    for fac, t, mm, nm in zip(d["FACILITY"], d["DELIVERY_DTTM"], d["MOTHER_MRN"], d["NEWBORN_MRN"]):
        if not mm:
            continue
        sysA = nm.startswith("CB")
        rows.append((fin(mm) if sysA else mm, fin(nm) if sysA else nm, nm, pd.Timestamp(t)))
    return rows


def two_people(R, F, ia, ib):
    """For record pairs, whether data the rules never use show two people: registered on one visit (the same
    index, the same day, MRNs created minutes apart), two newborns of one mother's delivery, or blood groups that
    differ (ABO or Rh)."""
    created = R["created"].to_numpy()
    sysv = R["sys"].to_numpy()
    mrn = R["mrn"].to_numpy()
    same_visit = (sysv[ia] == sysv[ib]) & (np.abs((created[ia] - created[ib]).astype("timedelta64[m]").astype(np.int64)) <= 90)
    bt = blood_types(F)
    abo = np.array([bool(bt.get(mrn[x]) and bt.get(mrn[y]) and not (bt[mrn[x]] & bt[mrn[y]])) for x, y in zip(ia, ib)], bool)
    sib = set()
    by_mother = defaultdict(list)
    for mm, nm_now, nm0, t in newborn_mothers(F):
        by_mother[mm].append((t, nm_now, nm0))
    for mm, lst in by_mother.items():
        lst.sort()
        for x in range(len(lst)):
            for y in range(x + 1, len(lst)):
                if abs((lst[y][0] - lst[x][0]).total_seconds()) <= 86400 and lst[x][1] != lst[y][1]:
                    sib.add((lst[x][1], lst[y][1]))
                    sib.add((lst[y][1], lst[x][1]))
    deliv = np.array([(mrn[x], mrn[y]) in sib for x, y in zip(ia, ib)], bool)
    return dict(same_visit=same_visit, abo=abo, delivery=deliv, any=same_visit | abo | deliv)


def typings(F):
    """Each active record's blood bank results in collection order, retired Calder Bay records followed to their
    survivor."""
    b = F["blood"]
    fin = survivors(F)
    out = defaultdict(list)
    for mrn, abo, rh, t in zip(b["MRN"], b["ABO"], b["RH"], b["COLLECTED"]):
        out[fin(mrn) if mrn.startswith("CB") else mrn].append((t, abo + rh))
    return out


def marker_noise(F, exclude=()):
    """How often a single specimen shows a blood group its patient does not have (wrong blood in tube), read from the
    records typed twice or more whose typings disagree, records holding two patients left out; and the chance two
    different patients' groups differ, from the type mix."""
    typ = typings(F)
    multi = [k for k, v in typ.items() if len(v) >= 2 and k not in exclude]
    dis = sum(1 for k in multi if len(set(x[1] for x in typ[k])) > 1)
    nspec = sum(len(typ[k]) for k in multi)
    b = F["blood"]
    p = (b["ABO"] + b["RH"]).value_counts(normalize=True).to_numpy()
    return dict(records=len(multi), disagreeing=dis, specimens=nspec, per_specimen=dis / max(nspec, 1),
                p_diff=1.0 - float((p ** 2).sum()))


def marker(R, F, link, exclude=(), noise=None):
    """The blood bank's cross-check on a rule's links: among links whose two records both carry results, those whose
    groups differ, read three ways: as they read; net of the wrong-blood-in-tube rate; and with links that touch a
    record holding two patients left out, net of that rate. Each count of differing pairs is divided by the chance two
    patients' groups differ and scaled from the typed links to all of the rule's links."""
    ia, ib = link
    typ = typings(F)
    bt = {k: set(x[1] for x in v) for k, v in typ.items()}
    m = R["mrn"].to_numpy()
    nz = noise or marker_noise(F, exclude)
    ex = set(exclude)
    typed = disc = typed_x = disc_x = 0
    e_all = e_x = 0.0
    wq = nz["per_specimen"]
    for x, y in zip(ia, ib):
        sx, sy = bt.get(m[x]), bt.get(m[y])
        if not sx or not sy:
            continue
        d = not (sx & sy)
        ew = wq ** len(typ[m[x]]) + wq ** len(typ[m[y]])
        typed += 1
        disc += d
        e_all += ew
        if m[x] in ex or m[y] in ex:
            continue
        typed_x += 1
        disc_x += d
        e_x += ew
    n, pd_ = len(ia), nz["p_diff"]
    return dict(links=n, typed_links=typed, discordant=disc, expected_one_patient=round(e_all, 1),
                typed_links_clear=typed_x, discordant_clear=disc_x, expected_one_patient_clear=round(e_x, 1),
                as_read=disc / pd_ * n / max(typed, 1),
                net_of_wbit=max(disc - e_all, 0.0) / pd_ * n / max(typed, 1),
                net=max(disc_x - e_x, 0.0) / pd_ * n / max(typed_x, 1))


# ---------------------------------------------------------------------------------------------------------------
# rule A: chance agreement
# ---------------------------------------------------------------------------------------------------------------

def person_entries(R):
    """One entry per (first, last, sex, birth date) with its record count: the persons rule A cannot tell apart."""
    k = R.assign(y=R["dob"].dt.year, d=R["dob"].dt.strftime("%m%d"))
    e = k.groupby(["first", "last", "sex", "dob"]).agg(n=("mrn", "size"), y=("y", "first"), d=("d", "first")).reset_index()
    return e


def heap_rates(e, by=("last", "decade"), shrink=20.0):
    """The share of persons born on 1 January and on 1 July, by surname and birth decade, shrunk toward the decade."""
    e = e.assign(decade=(e["y"] // 10) * 10, j1=(e["d"] == "0101").astype(float), j7=(e["d"] == "0701").astype(float))
    base = e.groupby("decade")[["j1", "j7"]].mean()
    g = e.groupby(list(by)).agg(n=("j1", "size"), j1=("j1", "sum"), j7=("j7", "sum")).reset_index()
    g = g.join(base, on="decade", rsuffix="_0")
    g["h1"] = (g["j1"] + shrink * g["j1_0"]) / (g["n"] + shrink)
    g["h7"] = (g["j7"] + shrink * g["j7_0"]) / (g["n"] + shrink)
    return g.set_index(list(by))[["h1", "h7"]]


def p_same_day(h1, h7):
    rest = np.clip(1.0 - h1 - h7, 0.0, 1.0)
    q1 = h1 + rest / 365.0
    q7 = h7 + rest / 365.0
    return q1 ** 2 + q7 ** 2 + 363.0 * (rest / 365.0) ** 2


def chance_rule_a(R, cell=("first", "last", "sex", "y"), heap_by=("last", "decade"), shrink=20.0):
    """The golden reading: rule A's links between different people expected from the joint distribution of first
    name, surname, sex and birth year among the persons in hand, each pair sharing a birth date with the chance its
    surname community's birth dates carry (1 January and 1 July recorded from foreign documents)."""
    e = person_entries(R)
    h = heap_rates(e, by=heap_by, shrink=shrink)
    e = e.assign(decade=(e["y"] // 10) * 10)
    e = e.join(h, on=list(heap_by))
    c = e.groupby(list(cell)).agg(n=("n", "size"), r=("n", "mean"), h1=("h1", "mean"), h7=("h7", "mean")).reset_index()
    c = c[c["n"] >= 2]
    pairs = c["n"] * (c["n"] - 1) / 2.0
    ps = p_same_day(c["h1"].to_numpy(), c["h7"].to_numpy())
    return float((pairs * ps * c["r"] ** 2).sum())


def chance_independent(R, u=None):
    """The hurried reading: chance agreement as the product of each field's own agreement rate over every pair of
    records (u from the records themselves, or the engine's national reference rates)."""
    n = len(R)
    pairs = n * (n - 1) / 2.0
    if u is None:
        def uf(col):
            c = R[col].value_counts().to_numpy(float)
            return float((c * (c - 1)).sum() / (n * (n - 1)))
        u = dict(first=uf("first"), last=uf("last"), dob=uf("dob"), sex=uf("sex"))
    return pairs * u["first"] * u["last"] * u["dob"] * u["sex"]


# ---------------------------------------------------------------------------------------------------------------
# rules C and D: the twins and the subscriber's SSN
# ---------------------------------------------------------------------------------------------------------------

class NameForms:
    """Whether two typed first names can be one person's: the same, close in spelling (Jaro-Winkler 0.85), forms of
    one name in the engine's table (allowing a slip in either), first tokens that match those ways, or the given and
    family names entered the other way round."""

    def __init__(self, eq):
        self.eq = eq
        self.table = sorted(eq)
        self.tv = Vocab(self.table)
        self.cache = {}

    def canon(self, a):
        if a in self.cache:
            return self.cache[a]
        out = set(self.eq.get(a, set()))
        if a and not out:
            for t in self.table:
                if abs(len(t) - len(a)) <= 2 and (jw_py(a, t) >= 0.9 or one_edit(a, t)):
                    out |= self.eq.get(t, set())
        self.cache[a] = out
        return out

    def one(self, a, b):
        if a == b or not a or not b:
            return a == b
        if jw_py(a, b) >= 0.85 or one_edit(a, b):
            return True
        if self.canon(a) & self.canon(b):
            return True
        ta, tb = a.split(" ")[0], b.split(" ")[0]
        if ta == tb or jw_py(ta, tb) >= 0.85 or (self.canon(ta) & self.canon(tb)):
            return True
        return False

    def compatible(self, fa, la, fb, lb):
        return self.one(fa, fb) or (self.one(fa, lb) and self.one(la, fb))


def one_edit(a, b):
    """At most one insertion, deletion, substitution or transposition of neighbours turns a into b."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        d = [i for i in range(la) if a[i] != b[i]]
        if len(d) == 1:
            return True
        return len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]
    if la > lb:
        a, b = b, a
    for i in range(len(b)):
        if a == b[:i] + b[i + 1:]:
            return True
    return False


def jw_py(a, b):
    """Jaro-Winkler for two strings (plain Python, for the occasional pair)."""
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


def false_by_evidence(R, F, eq, voc, ia, ib, names_must_match=False, forms=None):
    """Links the evidence shows join two people; for rule D also links whose first names are not forms of one name."""
    ev = two_people(R, F, ia, ib)
    flag = ev["any"].copy()
    if names_must_match:
        forms = forms or NameForms(eq)
        f = R["first"].to_numpy()
        l = R["last"].to_numpy()
        same_name = np.array([forms.compatible(f[x], l[x], f[y], l[y]) for x, y in zip(ia, ib)], bool)
        flag |= ~same_name
    return flag, ev


# ---------------------------------------------------------------------------------------------------------------
# Calder Bay's overlays: the 2019 automatic merges inverted
# ---------------------------------------------------------------------------------------------------------------

def overlays(F, eq, how="golden", namecheck="equiv", evidence=True):
    """Active Calder Bay records holding two or more patients. golden: an automatic merge whose retired first name is
    not a form of the surviving record's name, or whose names agree but whose two records the evidence shows are two
    people (one visit, one delivery, different blood groups). raw: every automatic merge whose first names differ as
    typed. none: the index as it stands."""
    if how == "none":
        return 0, set(), {}
    m = F["merges"]
    a = F["index_a"].set_index("MRN")
    fin = survivors(F)
    bt_raw = defaultdict(set)
    for mrn, abo, rh in zip(F["blood"]["MRN"], F["blood"]["ABO"], F["blood"]["RH"]):
        bt_raw[mrn].add(abo + rh)
    born = {}
    for mm, nm_now, nm0, t in newborn_mothers(F):
        born[nm0] = (mm, t)
    reg = dict(zip(a.index, a["REG_DATE"]))
    from golden import std_name
    hit = set()
    per = {}
    auto = m[m["METHOD"] == "AUTO"]
    names = sorted(set(auto["RET_FIRST"].map(std_name)) | set(a["FIRST_NAME"].map(std_name)))
    voc = Vocab(names)
    forms = NameForms(eq) if namecheck == "forms" else None
    for surv, ret, rf in zip(auto["SURVIVOR_MRN"], auto["RETIRED_MRN"], auto["RET_FIRST"]):
        s_now = fin(surv)
        if s_now not in a.index:
            continue
        sf = std_name(a.at[s_now, "FIRST_NAME"])
        r_f = std_name(rf)
        if how == "raw":
            if sf != r_f:
                hit.add(s_now)
            per[ret] = (s_now, sf != r_f)
            continue
        if namecheck == "forms":
            same = forms.one(sf, r_f)
        else:
            sim = float(voc.jw([voc.index[sf]], [voc.index[r_f]])[0])
            same = first_equiv(sf, r_f, eq, sim) or sf.split(" ")[0] == r_f.split(" ")[0]
        if not same:
            hit.add(s_now)
            per[ret] = (s_now, True)
            continue
        # names agree: two people only if other evidence says so
        two = False
        if not evidence:
            per[ret] = (s_now, False)
            continue
        if ret in born and surv in born and born[ret][0] == born[surv][0]:
            two = True
        if bt_raw.get(ret) and bt_raw.get(surv) and not (bt_raw[ret] & bt_raw[surv]):
            two = True
        if two:
            hit.add(s_now)
        per[ret] = (s_now, two)
    return len(hit), hit, per


# ---------------------------------------------------------------------------------------------------------------
# the linked index
# ---------------------------------------------------------------------------------------------------------------

def soundex(s):
    if not s:
        return ""
    codes = {**dict.fromkeys("BFPV", "1"), **dict.fromkeys("CGJKQSXZ", "2"), **dict.fromkeys("DT", "3"), "L": "4",
             **dict.fromkeys("MN", "5"), "R": "6"}
    s = s.replace(" ", "")
    out = s[0]
    last = codes.get(s[0], "")
    for ch in s[1:]:
        c = codes.get(ch, "")
        if c and c != last:
            out += c
        if ch not in "HW":
            last = c
    return (out + "000")[:4]


def candidate_pairs(R):
    dob = R["dob"].dt.strftime("%Y%m%d")
    yr = R["dob"].dt.year.astype(str)
    ln = R["last"].str.split(" ")
    keys = [
        (dob + "|" + R["sex"], None),
        (R["ssn"], (R["ssn"] != "").to_numpy()),
        (R["phone"], (R["phone"] != "").to_numpy()),
        (R["last"].map(lambda s: soundex(s.split(" ")[0])) + "|" + yr + "|" + R["sex"], None),
        (ln.map(lambda t: t[-1] if t else "") + "|" + R["first"].str[:3] + "|" + yr, None),
        (R["first"] + "|" + R["last"] + "|" + R["sex"], None),
        (R["addr"] + "|" + yr, (R["addr"] != "").to_numpy()),
    ]
    allp = []
    n = len(R)
    for k, m in keys:
        ia, ib = group_pairs(k.to_numpy(), mask=m)
        allp.append(ia * n + ib)
    u = np.unique(np.concatenate(allp))
    return (u // n).astype(np.int64), (u % n).astype(np.int64)


def comparison_levels(R, eq, voc, ia, ib):
    f = R["first"].to_numpy()
    l = R["last"].to_numpy()
    dob = R["dob"].to_numpy()
    sim_f = voc.jw(voc.code(R["first"].iloc[ia]), voc.code(R["first"].iloc[ib]))
    lv = Vocab(R["last"].tolist())
    sim_l = lv.jw(lv.code(R["last"].iloc[ia]), lv.code(R["last"].iloc[ib]))
    L = {}
    fe = np.array([a == b for a, b in zip(f[ia], f[ib])], bool)
    feq = np.array([bool(eq.get(a, set()) & eq.get(b, set())) or a.split(" ")[0] == b.split(" ")[0]
                    for a, b in zip(f[ia], f[ib])], bool)
    swp = (f[ia] == l[ib]) & (l[ia] == f[ib])
    feq = feq | swp
    L["first"] = np.where(fe, 0, np.where(feq, 1, np.where(sim_f >= 0.88, 2, 3)))
    le = (l[ia] == l[ib]) | swp
    lt = np.array([bool(set(a.split()) & set(b.split())) for a, b in zip(l[ia], l[ib])], bool)
    L["last"] = np.where(le, 0, np.where(lt, 1, np.where(sim_l >= 0.9, 2, 3)))
    da = pd.DatetimeIndex(dob[ia])
    db = pd.DatetimeIndex(dob[ib])
    de = da == db
    swap = (da.year == db.year) & (da.month == db.day) & (da.day == db.month)
    near = ((da.year == db.year) & (da.month == db.month)) | ((da.month == db.month) & (da.day == db.day)) | swap
    L["dob"] = np.where(de, 0, np.where(near, 1, 2))
    sx = R["sex"].to_numpy()
    L["sex"] = np.where(sx[ia] == sx[ib], 0, 1)
    pssn = personal_ssn(R)
    for col in ("addr", "phone", "ssn"):
        v = R[col].to_numpy() if col != "ssn" else pssn
        miss = (v[ia] == "") | (v[ib] == "")
        L[col] = np.where(miss, 2, np.where(v[ia] == v[ib], 0, 1))
    return L


def fs_em(L, n_iter=60, p0=0.1):
    """Fellegi-Sunter weights by EM over the candidate pairs (two latent classes)."""
    fields = list(L)
    K = {k: int(L[k].max()) + 1 for k in fields}
    m = {k: np.full(K[k], 1.0 / K[k]) for k in fields}
    u = {k: np.full(K[k], 1.0 / K[k]) for k in fields}
    for k in fields:
        m[k] = np.linspace(2.0, 0.5, K[k])
        m[k] /= m[k].sum()
        u[k] = np.linspace(0.5, 2.0, K[k])
        u[k] /= u[k].sum()
    p = p0
    for _ in range(n_iter):
        lm = np.full(len(L[fields[0]]), math.log(p))
        lu = np.full(len(L[fields[0]]), math.log(1 - p))
        for k in fields:
            lm += np.log(m[k][L[k]])
            lu += np.log(u[k][L[k]])
        g = 1.0 / (1.0 + np.exp(np.clip(lu - lm, -50, 50)))
        p = float(np.clip(g.mean(), 1e-6, 1 - 1e-6))
        for k in fields:
            m[k] = np.bincount(L[k], weights=g, minlength=K[k]) + 1e-3
            m[k] /= m[k].sum()
            u[k] = np.bincount(L[k], weights=1 - g, minlength=K[k]) + 1e-3
            u[k] /= u[k].sum()
    return g, m, u, p


class UF:
    def __init__(self, n):
        self.p = np.arange(n)

    def find(self, x):
        p = self.p
        r = x
        while p[r] != r:
            r = p[r]
        while p[x] != r:
            p[x], x = r, p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def shared_ssns(R):
    """SSNs carried by records of two or more people (different first names and birth dates): an insurance
    subscriber's number on a family's records, not a personal identifier."""
    d = R[R["ssn"] != ""].assign(fd=lambda x: x["first"].str.split(" ").str[0] + "|" + x["dob"].dt.strftime("%Y%m%d"))
    k = d.groupby("ssn")["fd"].nunique()
    return set(k[k >= 2].index)


def minor_ssn_until(R):
    """The last day a Rosario record registered for a minor carries an SSN: until then the field held the insurance
    subscriber's number for a dependent."""
    b = R[(R["sys"] == "B") & (R["ssn"] != "")]
    age = (b["created"] - b["dob"]).dt.days / 365.25
    m = b[age < 18]
    return m["created"].max() if len(m) else None


def personal_ssn(R):
    """SSNs that identify the patient: a family's shared subscriber number and the numbers on Rosario's minors'
    records before the screen changed are left out."""
    sh = shared_ssns(R)
    v = R["ssn"].to_numpy().copy()
    v[np.isin(v, list(sh))] = ""
    until = minor_ssn_until(R)
    if until is not None:
        age = ((R["created"] - R["dob"]).dt.days / 365.25).to_numpy()
        minor = (R["sys"].to_numpy() == "B") & (age < 18) & (R["created"] <= until).to_numpy()
        v[minor] = ""
    return v


def ssn_conflict(R, ia, ib, v=None):
    """Two valid personal SSNs that differ in more than one digit: two people (a one-digit difference is a slip)."""
    if v is None:
        v = personal_ssn(R)
    both = (v[ia] != "") & (v[ib] != "")
    out = np.zeros(len(ia), bool)
    idx = np.nonzero(both & (v[ia] != v[ib]))[0]
    for k in idx:
        a, b = v[ia[k]], v[ib[k]]
        out[k] = sum(x != y for x, y in zip(a, b)) > 1
    return out


def with_retired(F, R, per):
    """The active records and Calder Bay's retired records (from the merge history), with each merge read as one patient
    (joined) or two (kept apart): the patients an automatic merge hid have no active record of their own."""
    from golden import std_addr, std_name, std_phone
    m = F["merges"]
    fin = survivors(F)
    rows = pd.DataFrame(dict(
        sys="A", mrn=m["RETIRED_MRN"], first=m["RET_FIRST"].map(std_name), last=m["RET_LAST"].map(std_name),
        dob=pd.to_datetime(m["RET_DOB"], format="%m/%d/%Y"), sex=m["RET_SEX"], addr=m["RET_ADDRESS"].map(std_addr),
        phone=m["RET_PHONE"].map(std_phone), ssn="", created=pd.to_datetime(m["MERGED_UTC"]), last_act=pd.NaT))
    Rx = pd.concat([R.assign(active=True), rows.assign(active=False)], ignore_index=True)
    pos = {k: i for i, k in enumerate(Rx["mrn"])}
    must, cannot = [], []
    for ret, surv in zip(m["RETIRED_MRN"], m["SURVIVOR_MRN"]):
        s_now = fin(surv)
        if s_now not in pos:
            continue
        two = per.get(ret, (s_now, False))[1]
        (cannot if two else must).append((pos[ret], pos[s_now]))
    return Rx, must, cannot


VENDOR_LEVELS = {"first": ["exact", "equiv", "similar", "diff"], "last": ["exact", "partial", "similar", "diff"],
                 "dob": ["exact", "partial", "diff"], "sex": ["same", "diff"], "addr": ["same", "diff"],
                 "phone": ["same", "diff"], "ssn": ["same", "diff"]}


def vendor_weight(L):
    """Each pair's total agreement weight at the specification's own m and u (a missing field adds nothing)."""
    import records as RC
    w = np.zeros(len(L["first"]))
    for f, levels in VENDOR_LEVELS.items():
        tab = np.array([np.log2(RC.VENDOR[f][lv][0] / RC.VENDOR[f][lv][1]) for lv in levels] + [0.0])
        w += tab[np.minimum(L[f], len(levels))]
    return w


def link_index(R, F, eq, voc, threshold=0.5, must=(), cannot_extra=(), fixed_weight=None):
    """The linked index: candidate pairs scored by Fellegi-Sunter weights fitted by EM and joined in order of their
    posterior (0.5 or more), refusing any join that would put two records the evidence shows are two people (one
    visit, one delivery, different blood groups, two different SSNs) into one patient. Each patient is a group of
    connected records."""
    ia, ib = candidate_pairs(R)
    L = comparison_levels(R, eq, voc, ia, ib)
    # a pair can only be one patient when the identity fields agree: the birth date at least nearly, and the first
    # name in some form or the SSN; household members share a surname, an address and a phone but not these
    gate = (L["dob"] <= 1) & ((L["first"] <= 2) | (L["ssn"] == 0))
    ia, ib = ia[gate], ib[gate]
    L = {k: v[gate] for k, v in L.items()}
    g, m, u, p = fs_em(L)
    if fixed_weight is not None:            # the specification's weights and a cut-off in place of the fitted posterior
        g = (vendor_weight(L) >= fixed_weight).astype(float)
    ev = two_people(R, F, ia, ib)
    cannot = ev["any"] | ssn_conflict(R, ia, ib)
    n = len(R)
    parent = np.arange(n)
    members = {i: [i] for i in range(n)}
    banned = defaultdict(set)
    for x, y in list(zip(ia[cannot], ib[cannot])) + list(cannot_extra):
        banned[x].add(y)
        banned[y].add(x)

    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r

    for x, y in must:
        a, b = find(x), find(y)
        if a != b:
            if len(members[a]) > len(members[b]):
                a, b = b, a
            parent[a] = b
            members[b].extend(members[a])
            del members[a]
    # strong agreement on the identity fields links whatever the address says (people move between visits)
    strong = ((L["first"] <= 1) & (L["dob"] == 0) & (L["last"] <= 2)) | \
             ((L["first"] <= 2) & (L["last"] == 0) & (L["dob"] <= 1)) | \
             ((L["ssn"] == 0) & (L["dob"] <= 1) & (L["first"] <= 2))
    score = np.where(strong, np.maximum(g, threshold + 1e-6), g)
    order = np.argsort(-score, kind="mergesort")
    joined = 0
    for k in order:
        if score[k] < threshold:
            break
        if cannot[k]:
            continue
        a, b = find(ia[k]), find(ib[k])
        if a == b:
            continue
        ma, mb = members[a], members[b]
        if len(ma) > len(mb):
            a, b, ma, mb = b, a, mb, ma
        bad = False
        for x in ma:
            bx = banned.get(x)
            if bx and any(find(z) == b for z in bx):
                bad = True
                break
        if bad:
            continue
        parent[a] = b
        mb.extend(ma)
        del members[a]
        joined += 1
    root = np.array([find(i) for i in range(n)])
    apart = set()
    for x, by in banned.items():
        for y in by:
            rx, ry = root[x], root[y]
            if rx != ry:
                apart.add((min(rx, ry), max(rx, ry)))
    return root, dict(pairs=len(ia), joined=joined, p=p, m=m, u=u, apart=apart)


def false_links(root, apart, ia, ib):
    """A rule's links that join two patients the evidence keeps apart: the two records sit in different patients and
    some record of one and some record of the other were shown to be two people."""
    rx, ry = root[ia], root[ib]
    lo, hi = np.minimum(rx, ry), np.maximum(rx, ry)
    return np.array([(a != b) and ((a, b) in apart) for a, b in zip(lo, hi)], bool)


def index_figures(Rx, root, rule_b):
    """Distinct patients (every group of records, the patients an overlay hid among them), patients held by both
    indexes, and the patients still under more than one active record once rule B's links are made."""
    persons = int(pd.Series(root).nunique())
    df = pd.DataFrame({"root": root, "sys": Rx["sys"].to_numpy(), "active": Rx["active"].to_numpy()})
    both = int((df.groupby("root")["sys"].nunique() == 2).sum())
    act = df[df["active"]].copy()
    uf = UF(len(Rx))
    for x, y in zip(*rule_b):
        uf.union(x, y)
    act["rb"] = [uf.find(i) for i in act.index]
    left = int((act.groupby("root")["rb"].nunique() >= 2).sum())
    return dict(persons=persons, both=both, left=left)
