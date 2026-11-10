"""task5 architecture 4: the independent verifier. It reads only the shipped bundle (target/, golden/) and
generator/figures.json, on its own code path (plain dictionaries and loops, no generator module), and recomputes the
census, the outstanding reports by kind, what the missing-alone keep, the employers with no account, the worksite split,
every county's December jobs and change, the designated set, the reconciliation to the published table and the replay."""
import csv
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
RES = []
CHAIN = {"236115", "236118", "236220", "237310", "238110", "238160", "238210", "238220", "238310", "238320", "238910",
         "238990", "113310", "115310", "321113", "321918", "337110", "423310", "444180", "444190", "484220", "423810",
         "444110"}


def ok(name, cond, detail=""):
    RES.append((name, bool(cond), str(detail)))


def qstart(q):
    return dt.datetime(2023 + q // 4, 3 * (q % 4) + 1, 1)


def qend(q):
    y, k = 2023 + q // 4, q % 4 + 1
    return dt.datetime(y, 3 * k, [31, 30, 30, 31][k - 1])


def m3start(q):
    return dt.datetime(2023 + q // 4, 3 * (q % 4) + 3, 1)


def cutoff(q):
    e = qend(q)
    m, y = e.month + 2, e.year
    if m > 12:
        m, y = m - 12, y + 1
    return dt.datetime(y, m, 15, 23, 59, 59)


def mdy(s):
    return dt.datetime.strptime(s, "%m/%d/%Y")


class Files:
    def __init__(self, target):
        rd = lambda name: list(csv.DictReader(open(os.path.join(target, name), encoding="utf-8", newline="")))
        names = sorted(os.listdir(target))
        pick = lambda key: [f for f in names if key in f][0]
        self.counties = {r["county_name"].upper(): r["county_code"] for r in rd(pick("county_codes"))}
        self.codes = sorted(self.counties.values())
        self.cname = {v: k.title().replace(" County", "") for k, v in self.counties.items()}
        ss = {r["naics_code"]: r["supersector_code"] for r in rd(pick("naics"))}
        self.acc = {}
        for r in rd(pick("employer_accounts")):
            a = r["account_no"].replace("-", "")
            self.acc[a] = dict(county=r["county_code"], ss=ss[r["naics_code"]], chain=r["naics_code"] in CHAIN and r["ownership"] == "5",
                               liab=mdy(r["liability_date"]), est=mdy(r["account_established"]), multi=r["multi_worksite"] == "Y",
                               no=r["account_no"])
        self.ends = {}
        for r in rd(pick("status_history")):
            if r["change_type"] in ("INACTIVATED", "CLOSED", "TRANSFERRED"):
                a = r["account_no"].replace("-", "")
                self.ends.setdefault(a, []).append((dt.datetime.strptime(r["effective_date"], "%Y-%m-%d"),
                                                    dt.datetime.strptime(r["processed_date"], "%Y-%m-%d")))
        self.rep = {}
        for r in rd(pick("quarterly_reports")):
            a = r["account_no"].replace("-", "")
            q = (int(r["year"]) - 2023) * 4 + int(r["quarter"]) - 1
            self.rep.setdefault(q, []).append((dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M:%S"), a, r["report_type"],
                                               int(r["month3_employment"])))
        for q in self.rep:
            self.rep[q].sort(key=lambda x: x[0])
        self.mwr = {}
        for r in rd(pick("worksite")):
            a = r["uiacct"]
            q = (int(r["year"]) - 2023) * 4 + int(r["quarter"]) - 1
            self.mwr.setdefault(a, {}).setdefault(q, dict(recv=mdy(r["date_received"]), units={}))["units"][r["reporting_unit"]] = \
                (self.counties[r["worksite_county"].upper().strip()], int(r["m3_emp"]))
        self._c = {}

    # ---- as the files stood at a moment
    def latest(self, q, asof):
        key = ("L", q, asof)
        if key not in self._c:
            last, first = {}, {}
            for t, a, kind, m3 in self.rep.get(q, []):
                if t > asof:
                    break
                if self.acc[a]["est"] > asof:
                    continue
                last[a] = m3
                if a not in first:
                    first[a] = t
            self._c[key] = (last, first)
        return self._c[key]

    def liable(self, q, asof):
        key = ("B", q, asof)
        if key not in self._c:
            out = set()
            for a, r in self.acc.items():
                if r["est"] > asof or r["liab"] > qend(q):
                    continue
                if any(eff <= qstart(q) and proc <= asof for eff, proc in self.ends.get(a, [])):
                    continue
                out.add(a)
            self._c[key] = out
        return self._c[key]

    def batches(self, q, asof):
        first = self.latest(q, asof)[1]
        by = {}
        for a, t in first.items():
            if t.hour + t.minute + t.second > 0:
                by.setdefault(t, []).append(a)
        return {a: t for t, ms in by.items() if len(ms) >= 3 for a in ms}

    def census(self, q, asof):
        key = ("V", q, asof)
        if key in self._c:
            return self._c[key]
        L = self.liable(q, asof)
        cur = self.latest(q, asof)[0]
        prev = self.latest(q - 1, asof)[0]
        bk = self.batches(q - 1, asof)
        mem = {}
        for a in L:
            if a in bk:
                mem.setdefault(bk[a], []).append(a)
        out = {}
        for a in L:
            if a in cur:
                out[a] = dict(kind="rep", m3=cur[a], prior=prev.get(a))
                continue
            if a in prev:
                if a in bk:
                    ms = mem[bk[a]]
                    arrived = sum(1 for m in ms if m in cur) / max(1, len(ms) - 1) if len(ms) > 1 else 0.0
                    kind = "alone" if arrived >= 0.5 else "batch"
                else:
                    on = late = 0
                    for h in range(max(0, q - 4), q):
                        f = self.latest(h, asof)[1].get(a)
                        if f is not None:
                            on += 1
                            late += f > cutoff(h)
                    kind = "habit" if (on >= 2 and late == on) else "alone"
                out[a] = dict(kind=kind, prior=prev[a])
            else:
                pa = None
                for h in range(q - 2, -1, -1):
                    x = self.latest(h, asof)[0].get(a)
                    if x is not None:
                        pa = x
                        break
                out[a] = dict(kind="twoq" if pa is not None else "new", prior=pa)
        self._c[key] = out
        return out

    def eventual(self, q, know, a):
        fin = self.latest(q, know)[0]
        if a in fin:
            return float(fin[a])
        if any(eff <= m3start(q) and proc <= know for eff, proc in self.ends.get(a, [])):
            return 0.0
        return None

    def mature(self, know, upto):
        out = []
        for h in range(4, upto):
            if cutoff(h) >= know:
                continue
            V = self.census(h, cutoff(h))
            tot = un = 0.0
            for a, r in V.items():
                if r["kind"] in ("alone", "twoq") and (r["prior"] or 0) > 0:
                    tot += r["prior"]
                    if self.eventual(h, know, a) is None:
                        un += r["prior"]
            if tot and un / tot <= 0.02:
                out.append(h)
        return out

    def outcomes(self, quarters, know):
        s = {}
        new = []
        for h in quarters:
            for a, r in self.census(h, cutoff(h)).items():
                if r["kind"] == "rep":
                    continue
                e = self.eventual(h, know, a)
                if e is None:
                    continue
                if r["kind"] == "new":
                    new.append(e)
                elif (r["prior"] or 0) > 0:
                    x = s.setdefault(r["kind"], [0.0, 0.0])
                    x[0] += e
                    x[1] += r["prior"]
        out = {k: v[0] / v[1] for k, v in s.items()}
        out["new_mean"] = sum(new) / len(new) if new else 0.0
        return out

    def seasonal(self, q, asof, a):
        rs = []
        for d_, s_ in ((q - 4, q - 5), (q - 8, q - 9)):
            if s_ < 0:
                return None
            x, y = self.latest(d_, asof)[0].get(a), self.latest(s_, asof)[0].get(a)
            if x is None or y is None or y <= 0:
                return None
            rs.append(x / y)
        return sum(rs) / 2 if max(rs) < 0.6 else None

    def split(self, q, asof, a):
        """county shares of account a for quarter q from the worksite reports on file at asof"""
        qs = {h: r for h, r in self.mwr.get(a, {}).items() if h <= q and r["recv"] <= asof}
        if not qs:
            return None
        if q in qs:
            w = {}
            for u, (c, m) in qs[q]["units"].items():
                w[c] = w.get(c, 0.0) + m
        else:
            L = max(qs)
            num = qs.get(q - 4, {}).get("units", {})
            den = qs.get(L - 4, {}).get("units", {})
            n_ = d_ = 0.0
            for u in qs[L]["units"]:
                if u in num and u in den and den[u][1] > 0:
                    n_ += num[u][1]
                    d_ += den[u][1]
            er = n_ / d_ if d_ > 0 else 1.0
            w = {}
            for u, (c, m) in qs[L]["units"].items():
                r = num[u][1] / den[u][1] if (u in num and u in den and den[u][1] > 0) else er
                w[c] = w.get(c, 0.0) + m * r
        tot = sum(w.values())
        return {c: x / tot for c, x in w.items()} if tot > 0 else None

    def to_counties(self, est, q, asof):
        tot = {c: 0.0 for c in self.codes}
        for a, e in est.items():
            sh = self.split(q, asof, a) if self.acc[a]["multi"] else None
            if sh:
                for c, s in sh.items():
                    tot[c] += e * s
            else:
                tot[self.acc[a]["county"]] += e
        return tot

    def unregistered(self, q, asof, know):
        n_own = n_old = j_own = j_old = reg_own = reg_prev = 0.0
        for h in range(q - 4, 2, -4):
            if cutoff(h) >= know:
                continue
            for a, r in self.acc.items():
                if r["liab"] <= qend(h) and cutoff(h) < r["est"] <= know:
                    e = self.eventual(h, know, a) or 0.0
                    if r["liab"] >= qstart(h):
                        n_own += 1
                        j_own += e
                    else:
                        n_old += 1
                        j_old += e
                if r["est"] <= cutoff(h):
                    if qstart(h) <= r["liab"] <= qend(h):
                        reg_own += 1
                    elif qstart(max(0, h - 4)) <= r["liab"] < qstart(h):
                        reg_prev += 1
        jobs = {c: 0.0 for c in self.codes}
        n = 0.0
        if not reg_own:
            return jobs, 0.0
        for a, r in self.acc.items():
            if r["est"] <= asof:
                if qstart(q) <= r["liab"] <= qend(q):
                    jobs[r["county"]] += (n_own / reg_own) * (j_own / n_own)
                    n += n_own / reg_own
                elif qstart(max(0, q - 4)) <= r["liab"] < qstart(q):
                    jobs[r["county"]] += (n_old / reg_prev) * (j_old / n_old)
                    n += n_old / reg_prev
        return jobs, n

    def estimate(self, q, asof):
        V = self.census(q, asof)
        oc = self.outcomes(self.mature(asof, q), asof)
        k = oc["alone"]
        # the reporters' change by county and supersector, the seasonal businesses left out
        cell, cty, tr, trs = {}, {}, {}, [0.0, 0.0]
        seas = {a: self.seasonal(q, asof, a) for a in V}
        for a, r in V.items():
            p = r.get("prior")
            if not p or p <= 0:
                continue
            A = self.acc[a]
            if r["kind"] == "rep" and seas[a] is None:
                x = cell.setdefault((A["county"], A["ss"]), [0.0, 0.0, 0])
                x[0] += r["m3"]; x[1] += p; x[2] += 1
                y = cty.setdefault(A["county"], [0.0, 0.0])
                y[0] += r["m3"]; y[1] += p
            if r["kind"] in ("rep", "alone"):
                g = (A["chain"], 0 if p <= 9 else (1 if p <= 49 else 2))
                z = tr.setdefault(g, [0.0, 0.0, 0])
                al = p if r["kind"] == "alone" else 0.0
                z[0] += al; z[1] += p; z[2] += 1
                trs[0] += al; trs[1] += p
        est, kinds = {}, {}
        for a, r in V.items():
            kd = r["kind"]
            kinds[kd] = kinds.get(kd, 0) + 1
            A = self.acc[a]
            p = r.get("prior") or 0.0
            if kd == "rep":
                est[a] = float(r["m3"])
            elif kd in ("batch", "habit"):
                c = cell.get((A["county"], A["ss"]))
                mv = c[0] / c[1] if (c and c[2] >= 10 and c[1] > 0) else cty[A["county"]][0] / cty[A["county"]][1]
                if seas[a] is not None:
                    mv = seas[a]
                g = tr.get((A["chain"], 0 if p <= 9 else (1 if p <= 49 else 2)))
                al = g[0] / g[1] if (g and g[2] >= 30) else trs[0] / trs[1]
                est[a] = p * (mv * (1 - al) + k * al)
            elif kd == "alone":
                est[a] = p * k
            elif kd == "twoq":
                est[a] = p * oc.get("twoq", 0.0)
            else:
                est[a] = oc["new_mean"]
        rep_tot = self.to_counties({a: e for a, e in est.items() if V[a]["kind"] == "rep"}, q, asof)
        out_tot = self.to_counties({a: e for a, e in est.items() if V[a]["kind"] != "rep"}, q, asof)
        un, n_un = self.unregistered(q, asof, asof)
        tot = {c: rep_tot[c] + out_tot[c] + un[c] for c in self.codes}
        return dict(total=tot, kinds=kinds, k=k, unreg=un, n_unreg=n_un, liable=len(V), received=kinds.get("rep", 0), est=est, V=V)

    def base(self, q, asof):
        return self.to_counties({a: float(m) for a, m in self.latest(q, asof)[0].items()}, q, asof)


def r10(x):
    return int(math.floor(x / 10.0 + 0.5)) * 10


def main(task=TASK):
    RES.clear()
    target, gold = os.path.join(task, "target"), os.path.join(task, "golden")
    figs = json.load(open(os.path.join(task, "generator", "figures.json")))
    F = Files(target)
    EXTRACT = dt.datetime(2027, 2, 15, 23, 59, 59)
    X = F.estimate(15, cutoff(15))
    base = F.base(11, EXTRACT)
    r1 = figs["r1_census_and_reconciliation"]
    ok("census: liable, received and outstanding", (X["liable"], X["received"], X["liable"] - X["received"]) == (r1["liable"], r1["received"], r1["outstanding"]),
       (X["liable"], X["received"]))
    r2 = figs["r2_outstanding_by_kind"]
    ok("outstanding by kind", (X["kinds"].get("batch"), X["kinds"].get("alone"), X["kinds"].get("habit"), X["kinds"].get("twoq"), X["kinds"].get("new")) ==
       (r2["late_transmission"], r2["missing_alone"], r2["late_every_quarter"], r2["two_quarters"], r2["new_account"]), X["kinds"])
    ok("what the missing-alone keep", abs(round(X["k"], 2) - r2["missing_alone_keep"]) < 1e-9, round(X["k"], 4))
    r4 = figs["r4_unregistered"]
    ok("employers with no account: count and jobs", int(round(X["n_unreg"], -1)) == r4["employers"] and abs(sum(X["unreg"].values()) - r4["jobs"]) <= 50,
       (round(X["n_unreg"], 1), round(sum(X["unreg"].values()))))
    name = F.cname
    tot_ok = all(r10(X["total"][c]) == figs["r6_county_jobs"][name[c]] for c in F.codes)
    ok("every county's December 2026 jobs", tot_ok, {name[c]: r10(X["total"][c]) for c in F.codes if r10(X["total"][c]) != figs["r6_county_jobs"][name[c]]})
    ch = {c: 100 * (X["total"][c] / base[c] - 1) for c in F.codes}
    ok("every county's change", all(abs(round(ch[c] + 1e-9, 1) - figs["r7_changes"][name[c]]) < 1e-9 for c in F.codes),
       {name[c]: round(ch[c], 3) for c in F.codes})
    ok("the designated counties", [name[c] for c in F.codes if round(ch[c] + 1e-9, 1) <= -2.0] == figs["r8_designated"],
       [name[c] for c in F.codes if round(ch[c] + 1e-9, 1) <= -2.0])
    # the reconciliation
    cutp = dt.datetime(2026, 5, 31, 23, 59, 59)
    pub, now = F.latest(11, cutp)[0], F.latest(11, EXTRACT)[0]
    late = sum(m for a, m in now.items() if a not in pub and F.acc[a]["est"] <= cutp)
    new = sum(m for a, m in now.items() if a not in pub and F.acc[a]["est"] > cutp)
    am = sum(now[a] - pub[a] for a in pub if a in now)
    ok("the reconciliation to the published table", (sum(pub.values()), sum(now.values()), late, new, am) ==
       (r1["published"], r1["now"], r1["late_reports"], r1["accounts_since"], r1["amendments"]), (sum(pub.values()), sum(now.values()), late, new, am))
    import openpyxl
    wsp = openpyxl.load_workbook([os.path.join(target, f) for f in os.listdir(target) if f.endswith(".xlsx")][0])["County"]
    pt = sum(int(r[5]) for r in wsp.iter_rows(min_row=6, values_only=True) if r[0] and str(r[0]).strip().isdigit())
    ok("the published workbook's county rows add to the figure", pt == r1["published"], pt)
    # the replay
    R = F.estimate(11, cutoff(11))
    sd = 100 * (sum(R["total"].values()) / sum(base.values()) - 1)
    ma = sum(abs(100 * (R["total"][c] / base[c] - 1)) for c in F.codes) / len(F.codes)
    r9 = figs["r9_replay"]
    ok("the replay on December 2025", abs(round(sd, 2) - r9["state_difference"]) < 0.011 and abs(round(ma, 2) - r9["mean_county_difference"]) < 0.011, (round(sd, 3), round(ma, 3)))
    # the deliverables read back
    wb = openpyxl.load_workbook(os.path.join(gold, "ctf_certification_december_2026.xlsx"))
    ws = wb["Certification"]
    rows = {str(r[0]): r for r in ws.iter_rows(min_row=8, max_row=21, values_only=True)}
    ok("workbook: county jobs and changes are the recomputed ones", all(rows[c][5] == r10(X["total"][c]) and abs(rows[c][6] - round(ch[c] + 1e-9, 1)) < 1e-9 for c in F.codes))
    byc, nrow = {c: 0.0 for c in F.codes}, 0
    for r in csv.DictReader(open(os.path.join(gold, "ctf_employer_jobs_december_2026.csv"), encoding="utf-8")):
        byc[r["county_code"]] += float(r["december_2026_jobs"])
        nrow += 1
    ok("employer list: adds to the recomputed county totals", max(abs(byc[c] - X["total"][c]) for c in F.codes) < 40, round(max(abs(byc[c] - X["total"][c]) for c in F.codes), 1))
    from docx import Document
    memo = "\n".join(p.text for p in Document(os.path.join(gold, "ctf_certification_memo_2027.docx")).paragraphs)
    ok("memo: reads back and names the designated counties", all(n_ in memo for n_ in figs["r8_designated"]), len(memo))
    act = "\n".join(p.text for p in Document([os.path.join(target, f) for f in os.listdir(target) if "act_2026" in f][0]).paragraphs)
    ok("Act: reads back with the population clause", "whether or not an account has been established" in act, len(act))
    bad = [r for r in RES if not r[1]]
    for nm, good, detail in RES:
        if not good:
            print("VERIFY FAIL  %s  %s" % (nm, detail[:300]))
    print("verify: %d of %d" % (len(RES) - len(bad), len(RES)))
    return not bad


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
