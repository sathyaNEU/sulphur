"""task19 golden analysis, read from the shipped files only (target/).

The estimate of each district's usual residents on 30 June 2026:
  1. assemble: every register record placed in a district by its postcode, the survey and follow-up placed by block;
  2. link the survey's people to the register on names, date of birth, sex and postcode, and measure that linkage on
     the clerical review, so each survey person carries the chance they are truly on their own district's list;
  3. measure the register's correct entries from the follow-up of the records listed at the sampled blocks' addresses,
     the records with no contact imputed from a model fitted on the resolved ones;
  4. dual-system estimate in each district by age group and sex: correct entries divided by the share of the survey's
     people on that district's list;
  5. raise men aged 18 to 29 and 30 to 44 so the estimate's sex ratio among Kilvarrans matches the one that births and
     survival give, with serving personnel added on both sides;
  6. serving personnel from the defence return; intervals and each district's chance of reaching 25,000 from a
     bootstrap of the survey blocks that repeats every step; the call under the Commission's rule;
  7. bridge each district's register count to its estimate, and the rolled-forward national figure to the estimate.

`run(target, **opts)` takes switches so the hurried passes and the rival methods run on the same code."""
import datetime as dt
import math
import os
import re
import unicodedata

import numpy as np
import pandas as pd

LINE = 25000
AGEG = [(0, 4), (5, 17), (18, 29), (30, 44), (45, 64), (65, 200)]
AGEG_LABEL = ["0-4", "5-17", "18-29", "30-44", "45-64", "65+"]
REF = dt.date(2026, 6, 30)
NICK = {"kate": "catherine", "cathy": "catherine", "katie": "katherine", "liz": "elizabeth", "beth": "elizabeth",
        "maggie": "margaret", "peggy": "margaret", "pat": "patrick", "paddy": "patrick", "mick": "michael",
        "mike": "michael", "jim": "james", "jimmy": "james", "tom": "thomas", "dan": "daniel", "danny": "daniel",
        "joe": "joseph", "eddie": "edward", "ted": "edward", "rob": "robert", "bob": "robert", "bill": "william",
        "will": "william", "tony": "anthony", "chris": "christopher", "matt": "matthew", "nick": "nicholas",
        "steve": "stephen", "andy": "andrew", "jenny": "jennifer", "becky": "rebecca", "sam": "samantha",
        "ben": "benjamin", "alex": "alexander", "debbie": "deborah", "trish": "patricia", "josie": "josephine",
        "bernie": "bernadette", "ger": "gerard", "kathy": "kathleen", "eily": "eileen", "frank": "francis",
        "fran": "frances", "jon": "jonathan", "tim": "timothy", "phil": "philip", "rich": "richard", "dick": "richard",
        "gabe": "gabriel", "shiv": "siobhan", "derm": "dermot", "con": "cornelius", "jerry": "jeremiah",
        "bridie": "bridget", "brenny": "brendan"}


# ---------------------------------------------------------------------------------------------- helpers
def norm_pc(s):
    s = re.sub(r"[^A-Za-z0-9]", "", str(s)).upper()
    return (s[:-3] + " " + s[-3:]) if len(s) >= 5 else s


def norm_name(s):
    s = str(s).replace("ł", "l").replace("Ł", "L").replace("ß", "ss").replace("ø", "o")
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", "", s.lower().replace("-", " ")).strip()


def soundex(s):
    s = re.sub(r"[^a-z]", "", s)
    if not s:
        return "0000"
    codes = {c: d for d, letters in (("1", "bfpv"), ("2", "cgjkqsxz"), ("3", "dt"), ("4", "l"), ("5", "mn"), ("6", "r"))
             for c in letters}
    out, last = s[0].upper(), codes.get(s[0], "")
    for c in s[1:]:
        d = codes.get(c, "")
        if d and d != last:
            out += d
        if c not in "hw":
            last = d
    return (out + "000")[:4]


def jaro_winkler(a, b):
    if a == b:
        return 1.0
    la, lb = len(a), len(b)
    if not la or not lb:
        return 0.0
    md = max(la, lb) // 2 - 1
    am, bm = [False] * la, [False] * lb
    m = 0
    for i in range(la):
        lo, hi = max(0, i - md), min(lb, i + md + 1)
        for j in range(lo, hi):
            if not bm[j] and a[i] == b[j]:
                am[i] = bm[j] = True
                m += 1
                break
    if not m:
        return 0.0
    t, k = 0, 0
    for i in range(la):
        if am[i]:
            while not bm[k]:
                k += 1
            if a[i] != b[k]:
                t += 1
            k += 1
    j = (m / la + m / lb + (m - t / 2) / m) / 3
    p = 0
    for i in range(min(4, la, lb)):
        if a[i] != b[i]:
            break
        p += 1
    return j + p * 0.1 * (1 - j)


def name_sim(a, b):
    """Best Jaro-Winkler over the whole names and their tokens (compound surnames, second forenames)."""
    if not a or not b:
        return 0.0
    best = jaro_winkler(a.replace(" ", ""), b.replace(" ", ""))
    ta, tb = a.split(), b.split()
    if len(ta) > 1 or len(tb) > 1:
        for x in ta:
            for y in tb:
                if len(x) > 2 and len(y) > 2:
                    best = max(best, jaro_winkler(x, y) - 0.02)
    return best


def parse_dmy(s):
    d, m, y = s.split("/")
    return int(d), int(m), int(y)


def parse_iso(s):
    y, m, d = s.split("-")
    return int(d), int(m), int(y)


def age_at(d, m, y, ref=REF):
    a = ref.year - y - ((ref.month, ref.day) < (m, d))
    return a


def agegroup(a):
    for k, (lo, hi) in enumerate(AGEG):
        if lo <= a <= hi:
            return k
    return 0


# ---------------------------------------------------------------------------------------------- load
FILES = {
    "register": "KHS_register_extract_2026-06-30.csv", "postcodes": "KSO_postcode_directory_2026-06.csv",
    "blocks": "CS26_blocks.csv", "persons": "CS26_persons.csv", "followup": "CS26_register_followup.csv",
    "review": "CS26_clerical_review.csv", "border": "KBA_permit_holder_movements_2021-07_to_2026-06.csv",
    "defence": "DF_personnel_by_location_2026-06-30.csv", "vital": "KSO_vital_statistics_2026.xlsx",
    "accounts": "KSO_population_accounts_2021-2026.xlsx", "census": "KSO_census2021_usual_residents.xlsx",
}


def _xl(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True)]
    # header is the first row whose first cell is text and the next row is data
    for i, r in enumerate(rows):
        if r and r[0] is not None and i + 1 < len(rows) and rows[i + 1] and rows[i + 1][0] is not None and \
                all(c is not None for c in r[:2]) and not str(r[0]).startswith(("Kilvarra", "Live", "Deaths", "National", "2021")):
            hdr = list(r)
            body = [list(x) for x in rows[i + 1:] if x and x[0] is not None and x[1] is not None]
            return pd.DataFrame(body, columns=hdr)
    raise ValueError(path)


def load(target):
    D = {}
    rd = lambda k: pd.read_csv(os.path.join(target, FILES[k]), dtype=str, keep_default_na=False)
    for k in ("register", "postcodes", "blocks", "persons", "followup", "review", "border", "defence"):
        D[k] = rd(k)
    D["births"] = _xl(os.path.join(target, FILES["vital"]), "Births")
    D["lifetable"] = _xl(os.path.join(target, FILES["vital"]), "Life table 2019-21")
    D["accounts"] = _xl(os.path.join(target, FILES["accounts"]), None)
    D["census"] = _xl(os.path.join(target, FILES["census"]), None)
    return D


# ---------------------------------------------------------------------------------------------- assembly
def assemble(D):
    pc = D["postcodes"]
    pc_dist = dict(zip(pc["postcode"].map(norm_pc), pc["district_code"]))
    reg = D["register"].copy()
    reg["pc"] = reg["postcode"].map(norm_pc)
    reg["district"] = reg["pc"].map(pc_dist)
    dob = [parse_dmy(s) for s in reg["date_of_birth"]]
    reg["d"], reg["m"], reg["y"] = [x[0] for x in dob], [x[1] for x in dob], [x[2] for x in dob]
    reg["age"] = [age_at(d, m, y) for d, m, y in dob]
    reg["ag"] = reg["age"].map(agegroup)
    reg["sx"] = np.where(reg["sex"] == "M", 1, 0)
    reg["fn"] = reg["forenames"].map(norm_name)
    reg["sn"] = reg["surname"].map(norm_name)
    bl = D["blocks"].copy()
    bl["p"] = bl["selection_probability"].astype(float)
    bdist = dict(zip(bl["block_id"], bl["district_code"]))
    bprob = dict(zip(bl["block_id"], bl["p"]))
    sv = D["persons"].copy()
    sv["district"] = sv["block_id"].map(bdist)
    dob = [parse_iso(s) for s in sv["date_of_birth"]]
    sv["d"], sv["m"], sv["y"] = [x[0] for x in dob], [x[1] for x in dob], [x[2] for x in dob]
    sv["age"] = [age_at(d, m, y) for d, m, y in dob]
    sv["ag"] = sv["age"].map(agegroup)
    sv["sx"] = np.where(sv["sex"] == "Male", 1, 0)
    sv["nat"] = np.where(sv["citizenship"] == "KV", 0, 1)
    sv["grp"] = sv["nat"] * 2 + np.where(sv["sex"] == "Male", 1, 0)
    sv["forces"] = sv["defence_forces"] == "Y"
    sv["fn"] = sv["forename"].map(norm_name)
    sv["sn"] = sv["surname"].map(norm_name)
    sv["pc"] = sv["postcode"].map(norm_pc)
    sv["w"] = 1.0 / sv["block_id"].map(bprob)
    fu = D["followup"].copy()
    fu["district"] = fu["block_id"].map(bdist)
    fu["w"] = 1.0 / fu["block_id"].map(bprob)
    ri = reg.set_index("khs_number")
    fu = fu.join(ri[["ag", "sx", "age", "registration_date", "last_attended", "district", "fn", "sn", "d", "m", "y"]],
                 on="khs_number", rsuffix="_reg")
    return {"reg": reg, "sv": sv, "fu": fu, "blocks": bl, "bdist": bdist, "pc_dist": pc_dist}


# ---------------------------------------------------------------------------------------------- linkage
def build_index(reg):
    idx = {"dob": {}, "swap": {}, "sdx": {}, "pc": {}}
    for i, (d, m, y, sx, sn, fn, pc) in enumerate(zip(reg["d"], reg["m"], reg["y"], reg["sx"], reg["sn"], reg["fn"], reg["pc"])):
        idx["dob"].setdefault((d, m, y, sx), []).append(i)
        if d <= 12 and d != m:
            idx["swap"].setdefault((m, d, y, sx), []).append(i)
        idx["sdx"].setdefault((y, sx, soundex(sn.split()[0] if sn else "")), []).append(i)
        idx["sdx"].setdefault((y, sx, "F" + soundex(fn.split()[0] if fn else "")), []).append(i)
        idx["pc"].setdefault((pc, sx), []).append(i)
    return idx


def score(sp, rp):
    """A match weight for one survey person against one register record."""
    f1 = sp["fn"].split()[0] if sp["fn"] else ""
    f2 = rp["fn"].split()[0] if rp["fn"] else ""
    f1 = NICK.get(f1, f1)
    f2 = NICK.get(f2, f2)
    fs = max(jaro_winkler(f1, f2), name_sim(sp["fn"], rp["fn"]))
    ls = name_sim(sp["sn"], rp["sn"])
    # given and family names recorded the other way round
    xs = min(name_sim(sp["fn"], rp["sn"]), name_sim(sp["sn"], rp["fn"]))
    if xs > max(fs, ls) and xs >= 0.92:
        fs = ls = xs - 0.03
    s = 0.0
    s += 3.0 if fs >= 0.95 else 2.0 if fs >= 0.88 else 0.6 if fs >= 0.80 else -2.5
    s += 4.0 if ls >= 0.95 else 2.6 if ls >= 0.88 else 0.6 if ls >= 0.80 else -3.0
    a, b = (sp["d"], sp["m"], sp["y"]), (rp["d"], rp["m"], rp["y"])
    if a == b:
        s += 5.0
    elif (a[1], a[0], a[2]) == b:
        s += 3.0
    elif b[0] == 1 and b[1] == 1 and a[2] == b[2]:
        s += 2.2
    elif sum(x == y for x, y in zip(a, b)) == 2:
        s += 2.4
    elif a[2] == b[2]:
        s += 0.4
    else:
        s -= 3.0
    if sp["pc"] == rp["pc"]:
        s += 2.0
    elif sp["pc"][:3] == rp["pc"][:3]:
        s += 0.7
    return s


def link(A, threshold=7.0):
    """Each survey person's best register record above the threshold, one survey person per record."""
    reg, sv = A["reg"], A["sv"]
    idx = build_index(reg)
    R = {c: reg[c].values for c in ("fn", "sn", "d", "m", "y", "pc", "district", "registration_date")}
    best = []
    for k, (d, m, y, sx, sn, fn, pc, dist) in enumerate(zip(sv["d"], sv["m"], sv["y"], sv["sx"], sv["sn"], sv["fn"],
                                                            sv["pc"], sv["district"])):
        cand = set(idx["dob"].get((d, m, y, sx), [])) | set(idx["swap"].get((d, m, y, sx), []))
        cand |= set(idx["sdx"].get((y, sx, soundex(sn.split()[0] if sn else "")), []))
        cand |= set(idx["sdx"].get((y, sx, "F" + soundex(fn.split()[0] if fn else "")), []))
        cand |= set(idx["pc"].get((pc, sx), []))
        cand |= set(idx["dob"].get((1, 1, y, sx), []))
        sp = {"fn": fn, "sn": sn, "d": d, "m": m, "y": y, "pc": pc}
        scored = []
        for i in cand:
            rp = {"fn": R["fn"][i], "sn": R["sn"][i], "d": R["d"][i], "m": R["m"][i], "y": R["y"][i], "pc": R["pc"][i]}
            s = score(sp, rp)
            if s >= threshold:
                # among equal scores prefer a record in the person's own district, then the later registration
                rd = R["registration_date"][i]
                scored.append((s, R["district"][i] == dist, rd[6:] + rd[3:5] + rd[:2], i))
        scored.sort(reverse=True)
        best.append(scored)
    # one survey person per record: the strongest claim keeps it, the others fall to their next candidate
    taken = {}
    choice = [None] * len(best)
    order = sorted(range(len(best)), key=lambda k: -(best[k][0][0] if best[k] else -99))
    for k in order:
        for s, same, rd, i in best[k]:
            if i not in taken:
                taken[i] = k
                choice[k] = i
                break
    A["link"] = choice
    return choice


def link_status(A, choice):
    """0 linked to a record in the person's own district, 1 linked to a record in another district, 2 not linked."""
    sv, reg = A["sv"], A["reg"]
    rdist = reg["district"].values
    st = np.full(len(sv), 2)
    for k, i in enumerate(choice):
        if i is not None:
            st[k] = 0 if rdist[i] == sv["district"].iloc[k] else 1
    return st


def gold_status(A, D):
    """The clerical review's verified status for its subsample: 0 on own district's list, 1 listed elsewhere, 2 none."""
    sv, reg = A["sv"], A["reg"]
    rv = D["review"]
    kd = dict(zip(reg["khs_number"], reg["district"]))
    pos = {p: k for k, p in enumerate(sv["person_id"])}
    g = np.full(len(sv), -1)
    for p, out, khs in zip(rv["person_id"], rv["review_outcome"], rv["khs_number"]):
        k = pos[p]
        if out == "matched":
            g[k] = 0 if kd.get(khs) == sv["district"].iloc[k] else 1
        else:
            g[k] = 2
    return g


def correction_table(L, G, grp, w=None, mode="gold"):
    """P(true status | linked status, group) from the clerical subsample: one 3 x 3 table per group (nationality and
    sex), each row the verified status of the subsample's people linked that way."""
    ng = int(grp.max()) + 1
    w = np.ones(len(L)) if w is None else w
    T = np.zeros((ng, 3, 3))
    for g in range(ng):
        for l in range(3):
            m = (G >= 0) & (grp == g) & (L == l)
            ww = w[m]
            n = ww.sum()
            for t in range(3):
                T[g, l, t] = (ww[G[m] == t].sum() + (0.5 if t == l else 0.0)) / (n + 0.5) if n else float(t == l)
    if mode == "none":
        T = np.zeros((ng, 3, 3))
        for g in range(ng):
            for l in range(3):
                T[g, l, l] = 1.0
    return T


# ---------------------------------------------------------------------------------------------- follow-up
CE_RESIDENT = "resident at address"
MOVED = "moved, now elsewhere in Kilvarra"
NOCONTACT = "no contact"


def fu_features(fu):
    def yrs(s):
        if not s:
            return 99.0
        d, m, y = parse_dmy(s)
        return (REF - dt.date(y, m, d)).days / 365.25
    la = np.array([yrs(s) for s in fu["last_attended"].fillna("")])
    rg = np.array([yrs(s) for s in fu["registration_date"].fillna("")])
    lab = np.digitize(np.where(la > 90, 50, la), [1, 3, 5, 10])
    X = [np.ones(len(fu))]
    for k in range(1, 5):
        X.append((lab == k).astype(float))
    X.append((la > 90).astype(float))
    X.append((rg < 2).astype(float))
    for t in ("flat", "shared", "communal"):
        X.append((fu["dwelling_type"] == t).values.astype(float))
    for g in range(1, 6):
        X.append((fu["ag"].values == g).astype(float))
    X.append(fu["sx"].values.astype(float))
    for dcode in sorted(fu["district"].unique())[1:]:
        X.append((fu["district"].values == dcode).astype(float))
    return np.column_stack(X)


def logistic(X, y, w=None, iters=25, ridge=1e-3):
    w = np.ones(len(y)) if w is None else w
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = X @ b
        p = 1 / (1 + np.exp(-eta))
        W_ = w * p * (1 - p)
        g = X.T @ (w * (y - p)) - ridge * b
        H = (X * W_[:, None]).T @ X + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, g)
        b += step
        if np.abs(step).max() < 1e-8:
            break
    return b


NOT_KNOWN = ("not known at address", "address vacant")


def outcome_shares(fu, rows=None):
    """By district, the shares the follow-up's placed outcomes give for the people no longer at their address: moved
    within the district, moved to another district, left Kilvarra or died. Movers with no district recorded are shared
    as the district's movers with one are."""
    out = fu["outcome"].values
    mv = fu["moved_to_district"].values
    dist = fu["district"].values
    sel = np.ones(len(fu), bool) if rows is None else rows
    S = {}
    for d in np.unique(dist):
        m = (dist == d) & sel
        mk = m & (out == MOVED) & (mv != "")
        same = (mk & (mv == d)).sum()
        known = mk.sum()
        share_same = same / known if known else 0.5
        moved = (m & (out == MOVED)).sum()
        left = (m & (out == "left Kilvarra")).sum()
        died = (m & (out == "died")).sum()
        tot = moved + left + died
        S[d] = {"share_same": share_same,
                "within": moved * share_same / tot if tot else 0.0,
                "elsewhere": moved * (1 - share_same) / tot if tot else 0.0,
                "left_or_died": (left + died) / tot if tot else 0.0,
                "left": left / tot if tot else 0.0}
    return S


def ce_probability(fu, impute="model", mv_unknown="share", rows=None):
    """Each follow-up record's probability of being a correct entry for its district."""
    out = fu["outcome"].values
    mv = fu["moved_to_district"].values
    dist = fu["district"].values
    sel = np.ones(len(fu), bool) if rows is None else rows
    S = outcome_shares(fu, sel)
    ce = np.full(len(fu), np.nan)
    ce[out == CE_RESIDENT] = 1.0
    known = (out == MOVED) & (mv != "")
    ce[known] = (mv[known] == dist[known]).astype(float)
    unk = (out == MOVED) & (mv == "")
    nk = np.isin(out, NOT_KNOWN)
    for d in S:
        m = dist == d
        if mv_unknown == "share":
            ce[unk & m] = S[d]["share_same"]
            ce[nk & m] = S[d]["within"]
        elif mv_unknown == "not_ce":
            ce[unk & m] = 0.0
            ce[nk & m] = 0.0
        else:
            ce[unk & m] = 1.0
            ce[nk & m] = S[d]["within"]
    other = np.isin(out, ["left Kilvarra", "died", "duplicate registration"])
    ce[other] = 0.0
    nc = out == NOCONTACT
    if impute == "drop":
        return ce, nc
    resolved = ~nc & sel & (out != "duplicate registration")
    if impute == "model":
        X = fu_features(fu)
        b = logistic(X[resolved], ce[resolved])
        ce[nc] = 1 / (1 + np.exp(-(X[nc] @ b)))
    elif impute == "cells":
        key = (fu["district"].astype(str) + "|" + fu["dwelling_type"].astype(str)).values
        for k in np.unique(key[nc]):
            m = (key == k) & resolved
            ce[nc & (key == k)] = ce[m].mean() if m.sum() >= 10 else ce[resolved & (dist == k.split("|")[0])].mean()
    elif impute == "district":
        for dcode in np.unique(dist):
            ce[nc & (dist == dcode)] = ce[resolved & (dist == dcode)].mean()
    return ce, nc


# ---------------------------------------------------------------------------------------------- the benchmark
def da_ratio(D, groups=((18, 29), (30, 44))):
    """Men per woman among Kilvarrans aged a at 30 June 2026 from births by sex and the life table's survival."""
    b = D["births"].copy()
    yr = [int(str(x)[:4]) for x in b.iloc[:, 0]]
    bm = dict(zip(yr, b["Males"].astype(float)))
    bf = dict(zip(yr, b["Females"].astype(float)))
    lt = D["lifetable"]
    lm = lt["lx males"].astype(float).values / 100000.0
    lf = lt["lx females"].astype(float).values / 100000.0
    out = []
    for lo, hi in groups:
        M = F = 0.0
        for a in range(lo, hi + 1):
            y1, y2 = 2025 - a, 2026 - a
            M += 0.5 * (bm[y1] + bm[y2]) * lm[a]
            F += 0.5 * (bf[y1] + bf[y2]) * lf[a]
        out.append(M / F)
    return np.array(out)


def census_ratio(D, groups=((18, 29), (30, 44))):
    """A rival benchmark: the 2021 Census's men per woman, carried five years on."""
    c = D["census"]
    out = []
    for lo, hi in groups:
        M = F = 0.0
        for g, row in c.iterrows():
            a0 = int(str(row["Age group"]).split("-")[0].replace("+", ""))
            a = a0 + 5
            if lo <= a + 2 <= hi:
                M += float(row["Males"])
                F += float(row["Females"])
        out.append(M / F)
    return np.array(out)


# ---------------------------------------------------------------------------------------------- estimation
def estimate(A, ce, Lst, T, sv_rows=None, fu_rows=None, dependence="births", da=None, forces=None,
             scope="district", ce_mode="followup", poststrata="age_sex", grp=None, k_override=None, ht=False):
    """District estimates by age group and sex; returns dict with the pieces the bridges need."""
    reg, sv, fu = A["reg"], A["sv"], A["fu"]
    dists = sorted(A["blocks"]["district_code"].unique())
    nD = len(dists)
    di = {d: k for k, d in enumerate(dists)}
    # register counts by district and cell
    rk = reg["district"].map(di).values * 12 + reg["ag"].values * 2 + reg["sx"].values
    L = np.bincount(rk, minlength=nD * 12).reshape(nD, 12).astype(float)
    # correct-entry rate by district and cell from the follow-up
    fsel = np.ones(len(fu), bool) if fu_rows is None else fu_rows
    fk = fu["district"].map(di).values * 12 + fu["ag"].values * 2 + fu["sx"].values
    fw = fu_rows if fu_rows is not None and fu_rows.dtype != bool else np.where(fsel, 1.0, 0.0)
    num = np.bincount(fk, weights=fw * ce, minlength=nD * 12).reshape(nD, 12)
    den = np.bincount(fk, weights=fw, minlength=nD * 12).reshape(nD, 12)
    if ht:
        # the sample blocks' entries expanded by their selection probabilities, in place of the district's own count
        L = np.bincount(fk, weights=fw * fu["w"].values, minlength=nD * 12).reshape(nD, 12).astype(float)
    if ce_mode == "one":
        rate = np.ones((nD, 12))
    else:
        # cells with few records borrow the district's age-group rate across sexes, then the district's
        rate = np.where(den >= 25, num / np.maximum(den, 1e-9), np.nan)
        for d in range(nD):
            for g in range(6):
                pair = [2 * g, 2 * g + 1]
                if np.isnan(rate[d, pair]).any():
                    s_num, s_den = num[d, pair].sum(), den[d, pair].sum()
                    r = s_num / s_den if s_den >= 20 else num[d].sum() / den[d].sum()
                    for c in pair:
                        if np.isnan(rate[d, c]):
                            rate[d, c] = r
    CE = L * rate
    # survey: each person's chance of truly being on their own district's list
    keep = ~sv["forces"].values
    sw = np.where(keep, 1.0, 0.0) if sv_rows is None else sv_rows * keep
    nat = sv["nat"].values
    grp = sv["grp"].values if grp is None else grp
    pin = T[grp, Lst, 0]
    pel = T[grp, Lst, 1]
    if scope == "national":
        pin = pin + pel
        pel = np.zeros_like(pel)
    sk = sv["district"].map(di).values * 12 + sv["ag"].values * 2 + sv["sx"].values
    n = np.bincount(sk, weights=sw, minlength=nD * 12).reshape(nD, 12)
    m_in = np.bincount(sk, weights=sw * pin, minlength=nD * 12).reshape(nD, 12)
    m_el = np.bincount(sk, weights=sw * pel, minlength=nD * 12).reshape(nD, 12)
    n_nat = np.bincount(sk, weights=sw * (nat == 0), minlength=nD * 12).reshape(nD, 12)
    cov = np.where(n >= 25, m_in / np.maximum(n, 1e-9), np.nan)
    for d in range(nD):
        for g in range(6):
            pair = [2 * g, 2 * g + 1]
            if np.isnan(cov[d, pair]).any():
                r = m_in[d, pair].sum() / max(n[d, pair].sum(), 1e-9) if n[d, pair].sum() >= 20 else m_in[d].sum() / n[d].sum()
                for c in pair:
                    if np.isnan(cov[d, c]):
                        cov[d, c] = r
    N = CE / cov
    # the share of each cell's people who are Kilvarrans, from the survey
    share_nat = np.where(n > 0, n_nat / np.maximum(n, 1e-9), 0.0)
    k = np.ones(2)
    dse_ratio = None
    if dependence != "none":
        Nn = N * share_nat
        fm = forces["male"] if forces is not None else np.zeros(2)
        ff = forces["female"] if forces is not None else np.zeros(2)
        dse_ratio = np.array([(Nn[:, 2 * g + 1].sum() + fm[j]) / (Nn[:, 2 * g].sum() + ff[j]) for j, g in enumerate((2, 3))])
        if dependence == "births_no_domain":
            dse_ratio = np.array([(Nn[:, 2 * g + 1].sum()) / (Nn[:, 2 * g].sum()) for j, g in enumerate((2, 3))])
        k = da / dse_ratio
        if k_override is not None:
            k = np.asarray(k_override, float)
        if dependence == "single":
            kk = (da[0] * 0 + 1)
            tot_m = sum(Nn[:, 2 * g + 1].sum() + fm[j] for j, g in enumerate((2, 3)))
            tot_f = sum(Nn[:, 2 * g].sum() + ff[j] for j, g in enumerate((2, 3)))
            k = np.array([1.0, 1.0]) * (da.mean() / (tot_m / tot_f)) * kk
        N_adj = N.copy()
        for j, g in enumerate((2, 3)):
            if dependence == "nationals_only":
                N_adj[:, 2 * g + 1] = N[:, 2 * g + 1] * (share_nat[:, 2 * g + 1] * k[j] + (1 - share_nat[:, 2 * g + 1]))
            else:
                N_adj[:, 2 * g + 1] = N[:, 2 * g + 1] * k[j]
    else:
        N_adj = N
    est = N_adj.sum(1)
    return {"dists": dists, "L": L, "CE": CE, "rate": rate, "cov": cov, "N": N, "N_adj": N_adj, "est": est, "k": k,
            "dse_ratio": dse_ratio, "m_in": m_in, "m_el": m_el, "n": n, "share_nat": share_nat}


def forces_from_return(D):
    f = D["defence"].copy()
    f["personnel"] = f["personnel"].astype(int)
    total = int(f["personnel"].sum())
    young = {"18-24": 0, "25-29": 0, "30-34": 1, "35-39": 1, "40 and over": 1}
    male = np.zeros(2)
    female = np.zeros(2)
    for _, r in f.iterrows():
        j = young[r["age_band"]]
        if r["sex"] == "Male":
            male[j] += r["personnel"]
        else:
            female[j] += r["personnel"]
    return {"total": total, "male": male, "female": female, "district": "D04"}


# ---------------------------------------------------------------------------------------------- bridges
def register_bridge(A, E, ce, fu_rows=None):
    """Each district's register count to its estimate: the parts that add up. The entries not correct for the
    district are shared into people who left Kilvarra or died, duplicate registrations and people living elsewhere in
    Kilvarra; those the household could not place, at vacant addresses or with no contact are shared as the district's
    placed outcomes are."""
    fu = A["fu"]
    dists = E["dists"]
    out = fu["outcome"].values
    mv = fu["moved_to_district"].values
    dist = fu["district"].values
    S = outcome_shares(fu)
    L = E["L"].sum(1)
    est_wo_forces = E["est"]
    rows = {}
    for k, d in enumerate(dists):
        m = dist == d
        n = m.sum()
        nce = 1.0 - ce
        unplaced = m & (np.isin(out, NOT_KNOWN) | (out == NOCONTACT))
        moved_out = m & (out == MOVED)
        # an unplaced record not correct for the district is one who moved away, left or died, in the placed shares
        sh = S[d]
        away = sh["elsewhere"] + sh["left_or_died"]
        f_else = sh["elsewhere"] / away if away else 0.0
        un = nce[unplaced].sum()
        part = {
            "left Kilvarra or died": (((np.isin(out, ["left Kilvarra", "died"])) & m).sum() + un * (1 - f_else)) / n,
            "duplicate registrations": ((out == "duplicate registration") & m).sum() / n,
            "living elsewhere in Kilvarra": ((nce * moved_out).sum() + un * f_else) / n,
        }
        over = {kk: v * L[k] for kk, v in part.items()}
        CEd = E["CE"][k].sum()
        # the parts are shared to the district's correct entries as the cells measured them, so the bridge adds up
        tot = sum(over.values())
        if tot > 0:
            over = {kk: v * (L[k] - CEd) / tot for kk, v in over.items()}
        missing = est_wo_forces[k] - CEd
        mel = E["m_el"][k].sum()
        mnot = (E["n"][k] - E["m_in"][k]).sum()
        q = mel / mnot if mnot > 0 else 0.0
        miss_pre = (E["N"][k] - E["CE"][k]).sum()
        listed_elsewhere = q * miss_pre
        on_no_list = missing - listed_elsewhere
        rows[d] = {"register": L[k], "over": over, "over_total": sum(over.values()), "listed_elsewhere": listed_elsewhere,
                   "on_no_list": on_no_list, "estimate": est_wo_forces[k]}
    return rows


def emigration_still_listed(A, D, ce=None, thr=5.0, undated="district"):
    """Emigrants since 30 June 2021 still on the register and missing from the accounts: the follow-up's people who
    left Kilvarra from July 2021, dated by the month they left, with the undated shared as the dated are and those the
    household could not place, at vacant addresses and the no-contact entries not resident shared in as the district's
    placed outcomes are; less the share of those leavers whose departure the border system recorded."""
    fu = A["fu"]
    out = fu["outcome"].values
    ly = fu["left_kilvarra_month"].values
    dist = fu["district"].values
    L = A["reg"].groupby("district").size()
    S = outcome_shares(fu)
    if ce is None:
        ce, _ = ce_probability(fu)
    nce = 1.0 - ce
    # border departures indexed for the matcher
    dep = D["border"][D["border"]["movement"] == "departure"]
    bidx = {}
    brow = []
    for f, l, dob, sx in zip(dep["forenames"], dep["surname"], dep["date_of_birth"], dep["sex"]):
        d_, m_, y_ = parse_dmy(dob)
        rec = {"fn": norm_name(f), "sn": norm_name(l), "d": d_, "m": m_, "y": y_, "pc": ""}
        brow.append(rec)
        i = len(brow) - 1
        bidx.setdefault(("dob", d_, m_, y_, sx), []).append(i)
        bidx.setdefault(("sdx", y_, sx, soundex(rec["sn"].split()[0] if rec["sn"] else "")), []).append(i)
        bidx.setdefault(("fdx", y_, sx, soundex(rec["fn"].split()[0] if rec["fn"] else "")), []).append(i)
        bidx.setdefault(("jan", y_, sx), []).append(i) if (d_, m_) == (1, 1) else None
    total = 0.0
    matched = recent_left = 0.0
    detail = {}
    sex = np.where(fu["sx"].values == 1, "M", "F")
    for d in sorted(np.unique(dist)):
        m = dist == d
        n = m.sum()
        left = m & (out == "left Kilvarra")
        known = left & (ly != "")
        ky = np.array([int(y[:4]) * 12 + int(y[5:7]) - 1 for y in ly[known]]) if known.any() else np.array([], int)
        w_known = np.where(ky >= 2021 * 12 + 6, 1.0, 0.0)
        recent_share = w_known.mean() if len(ky) else 0.5
        if undated == "national":
            kn_all = (out == "left Kilvarra") & (ly != "")
            ky_all = np.array([int(y[:4]) * 12 + int(y[5:7]) - 1 for y in ly[kn_all]])
            recent_share = float((ky_all >= 2021 * 12 + 6).mean())
        w = np.zeros(len(fu))
        w[known] = w_known
        w[left & (ly == "")] = recent_share
        unplaced = m & (np.isin(out, NOT_KNOWN) | (out == NOCONTACT))
        sh = S[d]
        away = sh["elsewhere"] + sh["left_or_died"]
        f_left = sh["left"] / away if away else 0.0
        r_recent = (w[left].sum() + nce[unplaced].sum() * f_left * recent_share) / n
        total += r_recent * L.get(d, 0)
        detail[d] = r_recent * L.get(d, 0)
        # which of the placed recent leavers the border system saw leave
        for i in np.where(left & (w > 0))[0]:
            sp = {"fn": fu["fn"].values[i] or "", "sn": fu["sn"].values[i] or "", "d": fu["d"].values[i],
                  "m": fu["m"].values[i], "y": fu["y"].values[i], "pc": "-"}
            sx_ = sex[i]
            cand = set(bidx.get(("dob", sp["d"], sp["m"], sp["y"], sx_), []))
            cand |= set(bidx.get(("sdx", sp["y"], sx_, soundex(sp["sn"].split()[0] if sp["sn"] else "")), []))
            cand |= set(bidx.get(("fdx", sp["y"], sx_, soundex(sp["fn"].split()[0] if sp["fn"] else "")), []))
            cand |= set(bidx.get(("jan", sp["y"], sx_), []))
            best = max((score(sp, brow[c]) for c in cand), default=-99)
            recent_left += w[i]
            matched += w[i] * (best >= thr)
    rec_share = matched / recent_left if recent_left else 0.0
    return {"still_listed_recent": total, "border_recorded_share": rec_share,
            "of_which_border_recorded": total * rec_share, "unrecorded": total * (1 - rec_share), "by_district": detail}


def accounts_figures(D, border):
    a = D["accounts"]
    end = float(a["Population at end"].iloc[-1])
    imm_nn = float(a["Immigration: non-nationals"].astype(float).sum())
    arr = (border["movement"] == "arrival").sum()
    return {"official_2026": end, "imm_nn_accounts": imm_nn, "arrivals_border": float(arr),
            "imm_not_in_accounts": float(arr) - imm_nn, "base_2021": float(a["Population at start"].iloc[0])}


# ---------------------------------------------------------------------------------------------- the whole run
def prepare(target, threshold=7.0):
    D = load(target)
    A = assemble(D)
    choice = link(A, threshold)
    Lst = link_status(A, choice)
    G = gold_status(A, D)
    return D, A, Lst, G


def run(target=None, prepared=None, linkage="gold", impute="model", mv_unknown="share", dependence="births",
        forces_mode="defence", scope="district", ce_mode="followup", bootstrap="full", B=300, seed=2026,
        calibrate_official=False, benchmark="births", k_override=None, miss_scale=None, nc_scale=None,
        estimator="ratio"):
    D, A, Lst, G = prepared if prepared is not None else prepare(target)
    sv, fu = A["sv"], A["fu"]
    nat = sv["nat"].values
    grp = sv["grp"].values if linkage != "gold_nat" else sv["nat"].values
    T = correction_table(Lst, G, grp, None, "none" if linkage == "none" else "gold")
    if miss_scale is not None:
        T = T.copy()
        T[:, 2, 0] *= miss_scale
        T[:, 2, 1] *= miss_scale
        T[:, 2, 2] = 1.0 - T[:, 2, 0] - T[:, 2, 1]
    ce, nc = ce_probability(fu, impute, mv_unknown)
    if nc_scale is not None:
        ce = ce.copy()
        ce[nc] = np.clip(ce[nc] * nc_scale, 0, 1)
    if impute == "drop":
        fu_w = (~nc).astype(float)
        ce = np.nan_to_num(ce)
    else:
        fu_w = None
    F = forces_from_return(D)
    da = da_ratio(D) if benchmark == "births" else census_ratio(D)
    dep = dependence
    ht = estimator == "ht"
    E = estimate(A, ce, Lst, T, fu_rows=fu_w, dependence=dep, da=da, forces=F if forces_mode == "defence" else None,
                 scope=scope, ce_mode=ce_mode, grp=grp, k_override=k_override, ht=ht)
    est = E["est"].copy()
    dists = E["dists"]
    gar = dists.index("D04")
    if forces_mode == "defence":
        est[gar] += F["total"]
    acc = accounts_figures(D, D["border"])
    if calibrate_official:
        est = est * acc["official_2026"] / est.sum()
    res = {"dists": dists, "est": est, "national": est.sum(), "k": E["k"], "da": da, "dse_ratio": E["dse_ratio"],
           "E": E, "T": T, "forces": F, "ce": ce, "forces_added": forces_mode == "defence"}
    # coverage of the survey's people by their own district's list, by nationality
    keep = ~sv["forces"].values
    pin = T[grp, Lst, 0]
    for g, lab in ((0, "nationals"), (1, "others")):
        m = keep & (nat == g)
        res["coverage_" + lab] = float((sv["w"].values[m] * pin[m]).sum() / sv["w"].values[m].sum())
    res["linked_" + "nationals"] = float((Lst[keep & (nat == 0)] == 0).mean())
    res["linked_others"] = float((Lst[keep & (nat == 1)] == 0).mean())
    gm = G >= 0
    for g, lab in ((0, "nationals"), (1, "others")):
        m = gm & (nat == g) & (G == 0)
        res["recall_" + lab] = float((Lst[m] == 0).mean())
    res["bridge"] = register_bridge(A, E, ce)
    res["emig"] = emigration_still_listed(A, D, ce)
    res["accounts"] = acc
    # bootstrap of the survey blocks within districts, every step repeated (or the survey alone)
    if bootstrap:
        rng = np.random.default_rng(seed)
        blocks = A["blocks"]
        sel_blocks = blocks[blocks["selected"] == "Y"]
        by_d = {d: sel_blocks["block_id"][sel_blocks["district_code"] == d].values for d in dists}
        sv_b = sv["block_id"].values
        fu_b = fu["block_id"].values
        reps = []
        ks = []
        ncm = []
        for b in range(B):
            mult = {}
            for d in dists:
                bl = by_d[d]
                draw = rng.integers(0, len(bl), len(bl))
                cnt = np.bincount(draw, minlength=len(bl))
                mult.update(dict(zip(bl, cnt)))
            sw = np.array([mult.get(x, 0) for x in sv_b], float)
            fw = np.array([mult.get(x, 0) for x in fu_b], float)
            if bootstrap == "full":
                Tb = correction_table(Lst, G, grp, sw, "none" if linkage == "none" else "gold")
                ceb, ncb = ce_probability(fu, impute, mv_unknown, rows=fw > 0)
                fwb = fw * ((~ncb).astype(float) if impute == "drop" else 1.0)
                if impute == "drop":
                    ceb = np.nan_to_num(ceb)
                Eb = estimate(A, ceb, Lst, Tb, sv_rows=sw, fu_rows=fwb, dependence=dep, da=da,
                              forces=F if forces_mode == "defence" else None, scope=scope, ce_mode=ce_mode, grp=grp, ht=ht)
            else:
                fwb = fw * ((~nc).astype(float) if impute == "drop" else 1.0)
                Eb = _estimate_fixed_k(A, ce, Lst, T, sw, fwb, E["k"], dep, scope, ce_mode, grp, ht)
            eb = Eb["est"].copy()
            if forces_mode == "defence":
                eb[gar] += F["total"]
            if calibrate_official:
                eb = eb * acc["official_2026"] / eb.sum()
            reps.append(eb)
            ks.append(Eb["k"])
            if bootstrap == "full":
                ncm.append(float(np.average(ceb[ncb], weights=fw[ncb])) if (fw[ncb] > 0).any() else np.nan)
        reps = np.array(reps)
        res["reps"] = reps
        res["k_reps"] = np.array(ks)
        res["nc_mean_reps"] = np.array(ncm)
        res["nc_mean"] = float(ce[nc].mean())
        res["sd"] = reps.std(0, ddof=1)
        res["sd_national"] = reps.sum(1).std(ddof=1)
        res["lo"] = est - 1.6449 * res["sd"]
        res["hi"] = est + 1.6449 * res["sd"]
        res["nat_lo"] = est.sum() - 1.6449 * res["sd_national"]
        res["nat_hi"] = est.sum() + 1.6449 * res["sd_national"]
        z = (est - LINE) / res["sd"]
        res["p_line"] = np.array([0.5 * (1 + math.erf(x / math.sqrt(2))) for x in z])
        res["call"] = ["qualifies" if lo >= LINE else ("does not qualify" if hi < LINE else "too close to call")
                       for lo, hi in zip(res["lo"], res["hi"])]
    return res


def _estimate_fixed_k(A, ce, Lst, T, sw, fw, k, dep, scope, ce_mode, grp, ht=False):
    E = estimate(A, ce, Lst, T, sv_rows=sw, fu_rows=fw, dependence="none", scope=scope, ce_mode=ce_mode, grp=grp, ht=ht)
    if dep != "none":
        N = E["N"].copy()
        for j, g in enumerate((2, 3)):
            N[:, 2 * g + 1] *= k[j]
        E["est"] = N.sum(1)
    E["k"] = k
    return E
