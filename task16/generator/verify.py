"""task16 verify: an independent recompute from the bundle alone (target/, golden/ and generator/figures.json), on its
own code path: its own standardization, its own Jaro-Winkler, each rule's links counted by key, rule A's chance
agreement from the indexes' joint cells, the blood groups' cross-check, rule D's names and the overlays from the merge
history. It imports nothing from the generator.

    python3 task16/generator/verify.py
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from itertools import combinations

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAILS = []


def say(label, ok, detail=""):
    print("%s  %-82s %s" % ("PASS" if ok else "FAIL", label[:82], str(detail)[:140]))
    if not ok:
        FAILS.append(label)


def f_(stem):
    for n in sorted(os.listdir(T)):
        if n.startswith(stem):
            return os.path.join(T, n)
    raise FileNotFoundError(stem)


def name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper().replace("-", " ")
    return " ".join(re.sub(r"[^A-Z ]", "", s).split())


def street(s):
    s = (s or "").upper().strip()
    s = re.sub(r"\s+(APT|UNIT|STE|SUITE|#|LOT|TRLR|BLDG)\b.*$", "", s)
    return " ".join(s.split())


def digits(s, n):
    d = re.sub(r"\D", "", s or "")
    return d if len(d) == n else ""


def jw(a, b):
    if a == b:
        return 1.0
    la, lb = len(a), len(b)
    if not la or not lb:
        return 0.0
    r = max(max(la, lb) // 2 - 1, 0)
    ma, mb = [False] * la, [False] * lb
    m = 0
    for i, c in enumerate(a):
        for j in range(max(0, i - r), min(lb, i + r + 1)):
            if not mb[j] and b[j] == c:
                ma[i] = mb[j] = True
                m += 1
                break
    if not m:
        return 0.0
    sa = [c for c, f in zip(a, ma) if f]
    sb = [c for c, f in zip(b, mb) if f]
    t = sum(x != y for x, y in zip(sa, sb)) / 2.0
    j = (m / la + m / lb + (m - t) / m) / 3.0
    p = 0
    for x, y in zip(a[:4], b[:4]):
        if x != y:
            break
        p += 1
    return j + p * 0.1 * (1 - j)


def records():
    rd = lambda p: pd.read_csv(p, dtype=str, keep_default_na=False)
    a, b = rd(f_("calder_bay_patient_index")), rd(f_("rosario_patient_index"))
    ra = pd.DataFrame(dict(sys="A", mrn=a["MRN"], first=a["FIRST_NAME"].map(name), last=a["LAST_NAME"].map(name),
                           dob=pd.to_datetime(a["DOB"], format="%m/%d/%Y").dt.strftime("%Y%m%d"), sex=a["SEX"],
                           addr=a["ADDRESS"].map(street), phone=a["HOME_PHONE"].map(lambda s: digits(s, 10)),
                           ssn=a["SSN"].map(lambda s: digits(s, 9)),
                           created=pd.to_datetime(a["REG_DATE"], format="%m/%d/%Y %H:%M")))
    rb = pd.DataFrame(dict(sys="B", mrn=b["PATIENT_ID"], first=b["PAT_FNAME"].map(name), last=b["PAT_LNAME"].map(name),
                           dob=pd.to_datetime(b["BIRTH_DT"]).dt.strftime("%Y%m%d"), sex=b["GENDER_CD"],
                           addr=b["STREET_ADDR"].map(street), phone=b["PHONE_NUM"].map(lambda s: digits(s, 10)),
                           ssn=b["SSN_NUM"].map(lambda s: digits(s, 9)), created=pd.to_datetime(b["CREATED_TS"])))
    R = pd.concat([ra, rb], ignore_index=True)
    R.loc[R["ssn"].isin(["000000000", "999999999"]), "ssn"] = ""
    return R


def pairs_by(R, cols, mask=None):
    df = R if mask is None else R[mask]
    out = []
    for _, idx in df.groupby(cols).indices.items():
        if len(idx) > 1:
            ix = df.index[idx]
            out += list(combinations(ix, 2))
    return out


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    B = figs["bands"]
    R = records()
    say("active records", len(R) == figs["active_records"], (len(R), figs["active_records"]))
    eqdf = pd.read_csv(f_("halvard_name_equivalence"), dtype=str, keep_default_na=False)
    grp = defaultdict(set)
    for n_, e_ in zip(eqdf["NAME"], eqdf["EQUIVALENT"]):
        grp[n_].add(n_)
        grp[e_].add(n_)
    equiv = lambda x, y: x == y or bool(grp.get(x, set()) & grp.get(y, set())) or jw(x, y) >= 0.92

    # ---------------------------------------------------------------- each rule's links
    A_ = pairs_by(R, ["first", "last", "dob", "sex"])
    addr, phone, first = R["addr"].to_numpy(), R["phone"].to_numpy(), R["first"].to_numpy()
    B_ = [(x, y) for x, y in A_ if addr[x] and addr[x] == addr[y]]
    C0 = pairs_by(R, ["last", "dob", "sex"])
    C_ = [(x, y) for x, y in C0 if equiv(first[x], first[y]) and
          ((addr[x] and addr[x] == addr[y]) or (phone[x] and phone[x] == phone[y]))]
    D_ = pairs_by(R, ["ssn", "dob"], mask=R["ssn"] != "")
    links = {"A": A_, "B": B_, "C": C_, "D": D_}
    for k, v in links.items():
        say("rule %s's automatic links" % k, len(v) == figs["rule_links"][k], (len(v), figs["rule_links"][k]))

    # ---------------------------------------------------------------- rule A: chance agreement from the joint cells
    e = R.groupby(["first", "last", "sex", "dob"]).size().rename("n").reset_index()
    e["y"] = e["dob"].str[:4].astype(int)
    e["dec"] = (e["y"] // 10) * 10
    e["j1"] = (e["dob"].str[4:] == "0101").astype(float)
    e["j7"] = (e["dob"].str[4:] == "0701").astype(float)
    base = e.groupby("dec")[["j1", "j7"]].mean()
    g = e.groupby(["last", "dec"]).agg(m=("j1", "size"), s1=("j1", "sum"), s7=("j7", "sum")).reset_index()
    g = g.join(base, on="dec")
    g["h1"] = (g["s1"] + 20 * g["j1"]) / (g["m"] + 20)
    g["h7"] = (g["s7"] + 20 * g["j7"]) / (g["m"] + 20)
    e = e.merge(g[["last", "dec", "h1", "h7"]], on=["last", "dec"])
    c = e.groupby(["first", "last", "sex", "y"]).agg(k=("n", "size"), r=("n", "mean"), h1=("h1", "mean"),
                                                     h7=("h7", "mean"))
    c = c[c["k"] >= 2]
    rest = (1 - c["h1"] - c["h7"]).clip(0, 1)
    ps = (c["h1"] + rest / 365) ** 2 + (c["h7"] + rest / 365) ** 2 + 363 * (rest / 365) ** 2
    chance = float((c["k"] * (c["k"] - 1) / 2 * ps * c["r"] ** 2).sum())
    say("R2 rule A's false merges from the joint cells, inside the band", B["R2_rule_a_false"][0] <= chance <=
        B["R2_rule_a_false"][1], round(chance, 1))
    say("R2 the same estimate as the answer blocks (within 1 per cent)", abs(chance - figs["R2_rule_a_false"]) <=
        0.01 * figs["R2_rule_a_false"], (round(chance, 1), figs["R2_rule_a_false"]))
    n = len(R)
    u = {col: float((R[col].value_counts().to_numpy(float) ** 2).sum() - n) / (n * (n - 1)) for col in
         ("first", "last", "dob", "sex")}
    local = n * (n - 1) / 2 * u["first"] * u["last"] * u["dob"] * u["sex"]
    say("R2 the records' own per-field rates (the shortcut) as the figures state", abs(local - figs["indep_local"]) < 0.2,
        (round(local, 1), figs["indep_local"]))

    # ---------------------------------------------------------------- the blood groups' cross-check on rule A
    mg = pd.read_csv(f_("calder_bay_merge_history"), dtype=str, keep_default_na=False)
    nxt = dict(zip(mg["RETIRED_MRN"], mg["SURVIVOR_MRN"]))

    def fin(x):
        for _ in range(20):
            if x not in nxt:
                break
            x = nxt[x]
        return x
    bb = pd.read_csv(f_("blood_bank"), dtype=str, keep_default_na=False)
    typ = defaultdict(list)
    for m_, a_, r_ in zip(bb["MRN"], bb["ABO"], bb["RH"]):
        typ[fin(m_) if m_.startswith("CB") else m_].append(a_ + r_)
    p = (bb["ABO"] + bb["RH"]).value_counts(normalize=True).to_numpy()
    p_diff = 1 - float((p ** 2).sum())
    mrn = R["mrn"].to_numpy()
    disc = typed = 0
    for x, y in A_:
        sx, sy = set(typ.get(mrn[x], [])), set(typ.get(mrn[y], []))
        if sx and sy:
            typed += 1
            disc += not (sx & sy)
    as_read = disc / p_diff * len(A_) / max(typed, 1)
    mk = figs["marker"]["A"]
    say("R2 the blood groups as they read on rule A (the shortcut) as the figures state",
        abs(as_read - mk["as_read"]) <= 0.5 and typed == mk["typed_links"] and disc == mk["discordant"],
        (round(as_read, 1), typed, disc))

    # ---------------------------------------------------------------- rule D: two first names under one SSN
    last = R["last"].to_numpy()

    def one(x, y):
        if x == y or jw(x, y) >= 0.85:
            return True
        if grp.get(x, set()) & grp.get(y, set()):
            return True
        tx, ty = x.split(" ")[0], y.split(" ")[0]
        return tx == ty or jw(tx, ty) >= 0.85 or bool(grp.get(tx, set()) & grp.get(ty, set()))
    inc = [(x, y) for x, y in D_ if not (one(first[x], first[y]) or (one(first[x], last[y]) and one(last[x], first[y])))]
    lo, hi = B["R4_rule_d_false"]
    say("R4 rule D's links whose first names are not one person's (a lower bound on its count), inside the band",
        lo <= len(inc) <= hi, len(inc))

    # ---------------------------------------------------------------- the overlays from the merge history
    a_idx = pd.read_csv(f_("calder_bay_patient_index"), dtype=str, keep_default_na=False).set_index("MRN")
    hit = set()
    for s_, rf, meth in zip(mg["SURVIVOR_MRN"], mg["RET_FIRST"], mg["METHOD"]):
        if meth != "AUTO":
            continue
        s_now = fin(s_)
        if s_now not in a_idx.index:
            continue
        sf, r_f = name(a_idx.at[s_now, "FIRST_NAME"]), name(rf)
        if not (equiv(sf, r_f) or sf.split(" ")[0] == r_f.split(" ")[0]):
            hit.add(s_now)
    say("R5 Calder Bay records holding two or more patients, inside the band", B["R5_overlays"][0] <= len(hit) <=
        B["R5_overlays"][1], len(hit))
    say("R5 the same count as the answer blocks", len(hit) == figs["R5_overlays"], (len(hit), figs["R5_overlays"]))

    # ---------------------------------------------------------------- the call from the figures
    rate = {k: 2000.0 * figs["rule_false"][k] / figs["rule_links"][k] for k in "ABCD"}
    ok_rules = [k for k in "ABCD" if rate[k] <= 1.0]
    call = max(ok_rules, key=lambda k: figs["rule_links"][k]) if ok_rules else "none"
    say("R6 the compliant rule that joins the most pairs", call == figs["R6_rule"], (call, {k: round(v, 2) for k, v in
                                                                                        rate.items()}))

    # ---------------------------------------------------------------- the golden files agree with the figures
    from openpyxl import load_workbook
    gold = os.path.join(TASK, "golden")
    wb = load_workbook(os.path.join(gold, [x for x in os.listdir(gold) if x.endswith(".xlsx")][0]), data_only=True)
    ws = wb["Rules"]
    rows = {ws.cell(row=r, column=1).value: [ws.cell(row=r, column=c).value for c in range(3, 6)]
            for r in range(4, 8)}
    for k in "ABCD":
        v = rows.get("Rule " + k)
        say("workbook: rule %s's links, false merges and rate" % k, v is not None and v[0] == figs["rule_links"][k] and
            abs(v[1] - figs["rule_false"][k]) < 0.06 and abs(v[2] - figs["rule_rate_per_2000"][k]) < 0.006, v)
    ix = wb["Index"]
    vals = [ix.cell(row=r, column=2).value for r in range(4, 9)]
    say("workbook: the index figures", vals[:4] == [figs["R1_index"]["distinct patients"],
                                                    figs["R1_index"]["patients in both indexes"],
                                                    figs["R5_overlays"], figs["R7_left_after_rule"]], vals)
    ov = wb["Overlays to split"]
    listed = {ov.cell(row=r, column=1).value for r in range(4, ov.max_row + 1)} - {None}
    say("workbook: the overlays listed are the records counted", listed == hit, (len(listed), len(hit)))
    import zipfile
    memo = [x for x in os.listdir(gold) if x.endswith(".docx")][0]
    xml = zipfile.ZipFile(os.path.join(gold, memo)).read("word/document.xml").decode("utf8")
    text = re.sub(r"<[^>]+>", "", xml)
    for v in ("{:,}".format(figs["rule_links"]["B"]), "%d Calder Bay records" % figs["R5_overlays"],
              "{:,}".format(figs["R1_index"]["distinct patients"]), "{:,}".format(figs["R7_left_after_rule"])):
        say("memo states %s" % v, v in text)
    print("\n%d FAIL" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
