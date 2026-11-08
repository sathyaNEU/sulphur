"""task5 architecture 3: the independent verifier. It reads only the shipped bundle (target/, golden/, submission.md,
generator/figures.json), shares no code with the generator's methods, recomputes each county's December 2026 covered
jobs on the golden route, and checks every graded figure, the deliverables and every shipped format."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CUTOFF = {}          # quarter index -> cutoff timestamp
for qi in range(16):
    y, k = 2023 + qi // 4, qi % 4 + 1
    m = 3 * k + 2
    yy = y + (m > 12)
    CUTOFF[qi] = pd.Timestamp(yy, (m - 1) % 12 + 1, 15, 23, 59, 59)
FLASH, BASE = 15, 11
EXTRACT = CUTOFF[FLASH]
CLOSED = list(range(4, 11))
OK = []


def ok(name, cond, detail=""):
    OK.append((name, bool(cond), detail))


def qstart(q):
    return pd.Timestamp(2023 + q // 4, 3 * (q % 4) + 1, 1)


def qend(q):
    return qstart(q) + pd.offsets.QuarterEnd(0)


def load(target):
    rd = lambda f: pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False)
    names = sorted(os.listdir(target))
    pick = lambda pat: [f for f in names if re.search(pat, f)][0]
    rep = rd(pick(r"quarterly_reports"))
    rep["a"] = rep["account_no"].str.replace("-", "", regex=False)
    rep["q"] = (rep["year"].astype(int) - 2023) * 4 + rep["quarter"].astype(int) - 1
    rep["t"] = pd.to_datetime(rep["received_at"])
    for c in ("month1_employment", "month2_employment", "month3_employment"):
        rep[c] = rep[c].astype(int)
    rep = rep.sort_values(["a", "q", "t"], kind="stable")
    k = ["a", "q", "report_type", "month1_employment", "month2_employment", "month3_employment", "total_wages"]
    pt = rep.groupby(k, sort=False)["t"].shift(1)
    rep = rep[~(pt.notna() & ((rep["t"] - pt).dt.total_seconds() <= 120))]
    acc = rd(pick(r"employer_accounts")).copy()
    acc["a"] = acc["account_no"].str.replace("-", "", regex=False)
    acc["liab"] = pd.to_datetime(acc["liability_date"], format="%m/%d/%Y")
    nx = rd(pick(r"naics.*concordance"))
    acc["ss"] = acc["naics_code"].map(dict(zip(nx["naics_code"], nx["supersector_code"])))
    acc = acc.set_index("a")
    st = rd(pick(r"status_history"))
    st["a"] = st["account_no"].str.replace("-", "", regex=False)
    st["eff"] = pd.to_datetime(st["effective_date"])
    st["proc"] = pd.to_datetime(st["processed_date"])
    ws = rd(pick(r"multiple_worksite"))
    ws["q"] = (ws["year"].astype(int) - 2023) * 4 + ws["quarter"].astype(int) - 1
    for c in ("m1_emp", "m3_emp"):
        ws[c] = ws[c].astype(int)
    cc = rd(pick(r"county_codes"))
    ws["c"] = ws["worksite_county"].map({nm.upper(): c for c, nm in zip(cc["county_code"], cc["county_name"])})
    return rep, acc, st, ws, list(cc["county_code"]), dict(zip(cc["county_code"], cc["county_name"].str.replace(" County", "")))


class Flash:
    def __init__(self, rep, acc, st, ws):
        self.rep, self.acc, self.st, self.ws = rep, acc, st, ws
        self.memo = {}

    def last(self, q, asof):
        key = (q, asof)
        if key not in self.memo:
            x = self.rep[(self.rep["q"] == q) & (self.rep["t"] <= asof)]
            l = x.groupby("a").tail(1).set_index("a")
            o = x[x["report_type"] == "ORIGINAL"].groupby("a").head(1).set_index("a")
            self.memo[key] = (l["month3_employment"], o["t"])
        return self.memo[key]

    def liable(self, q, asof):
        e = self.st[self.st["change_type"].isin(["INACTIVATED", "CLOSED", "TRANSFERRED"]) & (self.st["proc"] <= asof)]
        gone = set(e.loc[e["eff"] <= qstart(q), "a"])
        return set(self.acc.index[self.acc["liab"] <= qend(q)]) - gone

    def trans(self, q, asof):
        x = self.rep[(self.rep["q"] == q) & (self.rep["t"] <= asof) & (self.rep["report_type"] == "ORIGINAL")]
        x = x.groupby("a").head(1)
        x = x[x["t"].dt.strftime("%H:%M:%S") != "00:00:00"]
        n = x.groupby("t")["a"].transform("size")
        x = x[n >= 3]
        return x.set_index("a")["t"]

    def classify(self, q):
        asof = CUTOFF[q]
        m3, _ = self.last(q, asof)
        li = self.liable(q, asof)
        m3 = m3[m3.index.isin(li)]
        miss = sorted(li - set(m3.index))
        prev, _ = self.last(q - 1, asof)
        tr = self.trans(q - 1, asof)
        groups = tr.groupby(tr).groups
        late, onf = {}, {}
        for h in range(max(0, q - 4), q):
            _, ot = self.last(h, asof)
            for a, t in ot.items():
                onf[a] = onf.get(a, 0) + 1
                late[a] = late.get(a, 0) + int(t > CUTOFF[h])
        out = {}
        for a in miss:
            if a in prev.index:
                p = float(prev[a])
                if a in tr.index:
                    mates = [m for m in groups[tr[a]] if m != a and m in li]
                    share = np.mean([m in m3.index for m in mates]) if mates else 0.0
                    out[a] = ("alone" if share >= 0.5 else "batch", p)
                else:
                    habit = onf.get(a, 0) >= 2 and late.get(a, 0) == onf.get(a, 0)
                    out[a] = ("habitual" if habit else "alone", p)
            else:
                pq = None
                for h in range(q - 2, -1, -1):
                    lh, _ = self.last(h, asof)
                    if a in lh.index:
                        pq = float(lh[a])
                        break
                out[a] = ("two_q", pq) if pq is not None else ("new", np.nan)
        return out, m3, prev

    def kept(self, kind):
        num = den = 0.0
        fin_all = {}
        ended = self.st[self.st["change_type"].isin(["INACTIVATED", "CLOSED"]) & (self.st["proc"] <= EXTRACT)].groupby("a")["eff"].min()
        for h in CLOSED:
            cl, _, _ = self.classify(h)
            fin, _ = self.last(h, EXTRACT)
            m3d = qstart(h) + pd.DateOffset(months=2)
            for a, (k, p) in cl.items():
                if k != kind or not p or not np.isfinite(p) or p <= 0:
                    continue
                if a in fin.index:
                    num += float(fin[a]); den += p
                elif a in ended.index and ended[a] <= m3d:
                    den += p
        return num / den

    def estimate(self):
        cl, m3, prev = self.classify(FLASH)
        k_alone, k_two = self.kept("alone"), self.kept("two_q")
        both = m3.index.intersection(prev.index)
        df = pd.DataFrame({"n": m3[both].values, "b": prev[both].values}, index=both)
        df["c"] = self.acc.loc[both, "county_code"].values
        df["s"] = self.acc.loc[both, "ss"].values
        cell = df.groupby(["c", "s"]).agg(n=("n", "sum"), b=("b", "sum"), k=("n", "size"))
        cty = df.groupby("c").agg(n=("n", "sum"), b=("b", "sum"))
        def ratio(c, s):
            if (c, s) in cell.index and cell.loc[(c, s), "k"] >= 10 and cell.loc[(c, s), "b"] > 0:
                return cell.loc[(c, s), "n"] / cell.loc[(c, s), "b"]
            return cty.loc[c, "n"] / cty.loc[c, "b"]
        own = {}
        for a in cl:
            rs = []
            for d_, s_ in ((FLASH - 4, FLASH - 5), (FLASH - 8, FLASH - 9)):
                ld, _ = self.last(d_, CUTOFF[FLASH])
                ls, _ = self.last(s_, CUTOFF[FLASH])
                if a in ld.index and a in ls.index and ls[a] > 0:
                    rs.append(ld[a] / ls[a])
            if len(rs) == 2 and max(rs) < 0.6:
                own[a] = float(np.mean(rs))
        newacc = self.acc.index[(self.acc["liab"] >= qstart(FLASH)) & (self.acc["liab"] <= qend(FLASH))]
        got = m3.index.intersection(newacc)
        newmean = float(m3[got].mean()) if len(got) else 0.0
        est, kind = {a: float(v) for a, v in m3.items()}, {a: "reported" for a in m3.index}
        for a, (k, p) in cl.items():
            c, s = self.acc.loc[a, "county_code"], self.acc.loc[a, "ss"]
            if k in ("batch", "habitual"):
                est[a] = p * own[a] if a in own else p * ratio(c, s)
            elif k == "alone":
                est[a] = p * k_alone
            elif k == "two_q":
                est[a] = p * k_two
            else:
                est[a] = newmean
            kind[a] = k
        return est, kind, k_alone

    def split(self, q, est):
        tot = {}
        mw = set(self.acc.index[self.acc["multi_worksite"] == "Y"])
        wsq = self.ws[self.ws["q"] <= q]
        lastq = wsq.groupby("uiacct")["q"].max()
        for a, e in est.items():
            if a in mw and a in lastq.index:
                x = wsq[(wsq["uiacct"] == a) & (wsq["q"] == lastq[a])]
                s = x.groupby("c")["m3_emp"].sum()
                if s.sum() <= 0:
                    s = x.groupby("c")["m1_emp"].sum()
                if s.sum() > 0:
                    for c, v in (s / s.sum()).items():
                        tot[c] = tot.get(c, 0.0) + e * v
                    continue
            c = self.acc.loc[a, "county_code"]
            tot[c] = tot.get(c, 0.0) + e
        return tot


def main(task=TASK):
    OK.clear()
    target = os.path.join(task, "target")
    figs = json.load(open(os.path.join(task, "generator", "figures.json")))
    rep, acc, st, ws, codes, names = load(target)
    F = Flash(rep, acc, st, ws)
    est, kind, ka = F.estimate()
    tot = F.split(FLASH, est)
    b3, _ = F.last(BASE, EXTRACT)
    base = F.split(BASE, {a: float(v) for a, v in b3.items()})
    ch = {c: 100 * (tot[c] / base[c] - 1) for c in codes}
    des = sorted(names[c] for c in codes if round(ch[c] + 1e-9, 1) <= -2.0)
    ok("verify: the designated counties", des == sorted(figs["designated"]), des)
    for c in codes:
        f = figs["county." + names[c]]
        ok("verify: %s change at one decimal" % names[c], round(ch[c] + 1e-9, 1) == f["change"], (round(ch[c], 3), f["change"]))
        ok("verify: %s December 2026 jobs to the hundred" % names[c], int(round(tot[c] / 100.0)) * 100 == f["total"], (tot[c], f["total"]))
        ok("verify: %s December 2025 base to the hundred" % names[c], int(round(base[c] / 100.0)) * 100 == f["base"], (base[c], f["base"]))
    ok("verify: the missing-alone kept share", round(ka, 2) == figs["kept"]["alone"], (round(ka, 4), figs["kept"]["alone"]))
    # the deliverables
    gold = os.path.join(task, "golden")
    emp = pd.read_csv(os.path.join(gold, [f for f in os.listdir(gold) if f.endswith(".csv")][0]), dtype={"county_code": str})
    sums = emp.groupby("county_code")["december_2026_jobs"].sum()
    ok("verify: the employer list sums to each county's December 2026 jobs, within ten and to the same hundred",
       all(abs(sums[c] - tot[c]) < 10 and round(sums[c] / 100.0) == round(tot[c] / 100.0) for c in codes),
       {names[c]: round(sums[c] - tot[c], 2) for c in codes})
    rec_accts = {a for a in est if kind[a] == "reported"}
    marked = set(emp.loc[emp["report_received"] == "Y", "account_no"].str.replace("-", "", regex=False))
    ok("verify: the employer list marks a report received exactly where one arrived", marked == rec_accts,
       (len(marked), len(rec_accts)))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(gold, [f for f in os.listdir(gold) if f.endswith(".xlsx")][0]), data_only=False)
    sh = wb["Certification"]
    rows = {r[0]: r for r in sh.iter_rows(min_row=8, max_row=21, max_col=8, values_only=True) if r[0] in codes}
    ok("verify: the certification table carries every county", len(rows) == len(codes))
    for c in codes:
        r = rows[c]
        f = figs["county." + names[c]]
        ok("verify: certification row %s agrees with figures.json" % names[c], (r[5], r[6], r[4]) == (f["total"], f["change"], f["estimated"]), (r, f))
    ok("verify: the certification names the designated counties", all(nm in str(sh["A5"].value) for nm in figs["designated"]), sh["A5"].value)
    ok("verify: the workbook carries its chart", len(sh._charts) == 1)
    # every shipped format reads back, each with a positive control
    from docx import Document
    def txt(f):
        d = Document(os.path.join(target, f))
        parts = [p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells]
        return re.sub(r"\s+", " ", "\n".join(parts).replace("’", "'"))
    pdfs = sorted(f for f in os.listdir(target) if f.endswith(".docx"))
    act = txt([f for f in pdfs if "act" in f][0])
    ok("verify: the Act reads back (positive control) and files the population and the cutoff",
       "whether or not the employer's report for that quarter has been received" in act and "February 15" in act)
    agr = txt([f for f in pdfs if "agreement" in f][0])
    ok("verify: the agreement reads back (positive control)", "00:00:00" in agr)
    ok("verify: neither governing document names an agent or a transmission",
       not re.search(r"\bagents?\b|transmission|bureau(?! of Labor Statistics)|imput", act + agr, re.I))
    eml = open(os.path.join(target, [f for f in os.listdir(target) if f.endswith(".eml")][0]), encoding="utf-8").read()
    ok("verify: the request reads back", "March 1" in eml and "section 5" in eml)
    pubf = [f for f in os.listdir(target) if f.endswith(".xlsx")][0]
    pub = openpyxl.load_workbook(os.path.join(target, pubf)).active
    pubd = {r[0]: r[5] for r in pub.iter_rows(min_row=6, max_row=19, values_only=True) if r[0] in codes}
    ok("verify: the published Q4 2025 table equals the reports' December 2025 base", all(abs(pubd[c] - base[c]) < 0.5 for c in codes))
    sub = open(os.path.join(task, "submission.md")).read()
    ok("verify: the Final Recommendation names the designated counties", all(nm in sub.split("## Supplementary")[0] for nm in figs["designated"]))
    good = all(x[1] for x in OK)
    for name, g, d in OK:
        if not g:
            print("VERIFY FAIL", name, d)
    print("verify: %d of %d pass" % (sum(x[1] for x in OK), len(OK)))
    return good


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
