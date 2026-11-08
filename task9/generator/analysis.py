"""task9: the golden analysis, run on the shipped files only.

1. Lenderbase: the latest submission of each loan-quarter; statuses, ratings and purposes on one vocabulary.
2. Each loan's company (its LEI, or its name through the LEI extract), and the buyout that began the ownership the
   loan sits in (the latest completed primary or secondary buyout of that company on or before the loan began), with
   the buyer's fund and sponsor house read off the buyer names.
3. Company-years at risk from 2008 (a loan outstanding at the previous year end), default in the year.
4. Default chance by rating and full years since the buyout; dependence by random-effect probits: the economy's year,
   the industry's year given the year, the sponsor house's year given the industry-year.
5. Loss given default from the default years whose workouts have all closed.
6. Both tapes in euros with each borrower's house and years since buyout; five years simulated.
"""
import csv
import collections
import datetime as dt
import json
import os
import re

import numpy as np
import openpyxl

import model as MD

SUBORD = {"KL": 0.150, "OS": 0.150}
BAR = 0.01
TARGETS = (0.01, 0.005, 0.0025)
NSIM = 1_000_000
SEED = 27
_RATING = {"B1": 0, "B2": 1, "B3": 2, "Caa1": 3, "B+": 0, "B": 1, "B-": 2, "CCC+": 3}
_PURPOSE = {"Buyout": "LBO", "Secondary buyout": "SBO", "Refi": "Refinancing", "LBO": "LBO", "SBO": "SBO",
            "Refinancing": "Refinancing"}
_STATUS = {"P": "P", "W": "W", "D": "D", "R": "R", "Performing": "P", "Watchlist": "W", "Defaulted": "D", "Repaid": "R"}
_FORMS = r"\b(gmbh|ag|sas|sa|bv|b v|nv|n v|ltd|limited|plc|ab|a s|aps|as|oy|s l|s l u|slu|sl|s p a|spa|s r l|srl|dac)\b"
_ROMAN = r"\b(i{1,3}|iv|v|vi{0,3}|ix|x|xi{0,2})\b"


def norm_name(s):
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[.,/()'-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(_FORMS, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _date(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(s)


def _period_end(p):
    m = re.fullmatch(r"(\d{4})Q([1-4])", p)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        nxt = dt.date(y + (q == 4), (3 * q) % 12 + 1, 1)
        return nxt - dt.timedelta(days=1)
    return _date(p)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, root):
        self.root = root

    def path(self, name):
        return os.path.join(self.root, name)


# ---------------------------------------------------------------- 1-2. loans, companies, buyouts
def lei_index(pack):
    rows = read_csv(pack.path("lei_reference_extract_2026-12-31.csv"))
    by_name = {}
    for r in rows:
        if r["entity_category"] != "GENERAL":
            continue
        for nm in [r["legal_name"]] + [x for x in r["other_names"].split("|") if x]:
            by_name[norm_name(nm)] = r["lei"]
    return by_name


def loans(pack, by_name):
    rows = read_csv(pack.path("lenderbase_loan_performance_2008-2026.csv"))
    latest = {}
    for r in rows:
        k = (r["lb_loan_id"], _period_end(r["report_period"]))
        if k not in latest or r["submission_ts"] > latest[k]["submission_ts"]:
            latest[k] = r
    by_loan = collections.defaultdict(list)
    for (lid, q), r in latest.items():
        by_loan[lid].append((q, r))
    out = {}
    for lid, recs in by_loan.items():
        recs.sort(key=lambda x: x[0])
        leis = [r["obligor_lei"] for _, r in recs if r["obligor_lei"]]
        names = collections.Counter(norm_name(r["obligor_name"]) for _, r in recs)
        name = names.most_common(1)[0][0]
        key = leis[0] if leis else by_name.get(name, "NAME:" + name)
        last = recs[-1][1]
        st = _STATUS[last["status"]]
        dd = _date(last["default_date"]) if st == "D" else None
        out[lid] = dict(id=lid, company=key, name=name, sector=int(last["sector_code"][2:]) - 1,
                        rating=_RATING[last["rating_at_origination"]], purpose=_PURPOSE[last["purpose"]],
                        orig=_date(last["origination_date"]), ccy=last["currency"],
                        quarters={q: _STATUS[r["status"]] for q, r in recs}, first=recs[0][0], last=recs[-1][0],
                        status=st, default=dd)
    return out


def house_of(buyer, stems):
    s = buyer.split(";")[0]
    s = re.sub(r"\b(Fund|LP|SCSp|SCA|SICAV-RAIF|Co-Invest)\b", " ", s)
    s = re.sub(_ROMAN.upper().replace("I{1,3}", "I{1,3}"), " ", s)
    toks = s.split()
    stem = toks[0] if toks else ""
    return stems.get(stem)


def deals(pack, by_name):
    rows = read_csv(pack.path("dealtrail_buyout_transactions_1997-2026.csv"))
    buys = collections.defaultdict(list)
    house_names = collections.Counter()
    for r in rows:
        if r["deal_status"] != "Completed" or r["deal_type"] not in ("Primary buyout", "Secondary buyout"):
            continue
        house_names[r["buyers"].split(";")[0].split()[0]] += 1
    stems = {s: s for s in house_names}
    for r in rows:
        if r["deal_status"] != "Completed" or r["deal_type"] not in ("Primary buyout", "Secondary buyout"):
            continue
        key = r["target_lei"] or by_name.get(norm_name(r["target"]), "NAME:" + norm_name(r["target"]))
        buyer = r["buyers"].split(";")[0].strip()
        house = buyer.split()[0]
        m = re.search(r"\b(I{1,3}|IV|V|VI{0,3}|IX|X|XI{0,2})\b", buyer)
        fund = "%s %s" % (house, m.group(1)) if m else None
        buys[key].append(dict(date=_date(r["completed"]), house=house, fund=fund, buyer=buyer, type=r["deal_type"]))
    for k in buys:
        buys[k].sort(key=lambda d: d["date"])
    # a buyer named by its house alone: the fund that house was investing from at the time
    spans = collections.defaultdict(list)
    for k, ds in buys.items():
        for d in ds:
            if d["fund"]:
                spans[d["house"]].append((d["date"], d["fund"]))
    for k, ds in buys.items():
        for d in ds:
            if d["fund"] is None and spans[d["house"]]:
                d["fund"] = min(spans[d["house"]], key=lambda x: abs((x[0] - d["date"]).days))[1]
    return buys


def spell(loan, buys):
    ds = [d for d in buys.get(loan["company"], []) if d["date"] <= loan["orig"] + dt.timedelta(days=31)]
    return ds[-1] if ds else None


# ---------------------------------------------------------------- 3. the panel
def panel(L, buys, clock="buy"):
    rows, fund_id, house_id, comp_id = [], {}, {}, {}
    unlinked = 0
    for lid in sorted(L):
        ln = L[lid]
        sp = spell(ln, buys)
        if sp is None:
            unlinked += 1
            continue
        for y in range(2008, 2027):
            ye = dt.date(y - 1, 12, 31)
            if y == 2008:
                at_risk = ln["first"] <= dt.date(2008, 3, 31) and ln["orig"] < dt.date(2008, 1, 1)
            else:
                at_risk = ln["quarters"].get(ye) in ("P", "W")
            if not at_risk:
                continue
            d = int(ln["default"] is not None and ln["default"].year == y)
            age = (y - sp["date"].year) if clock == "buy" else (y - ln["orig"].year)
            c = comp_id.setdefault(ln["company"], len(comp_id))
            f = fund_id.setdefault(sp["fund"] or sp["house"] + " ?", len(fund_id))
            h = house_id.setdefault(sp["house"], len(house_id))
            rows.append((c, y, f, ln["sector"], ln["rating"], max(age, 1), d, h))
    return np.array(rows, dtype=np.int64), dict(funds=fund_id, houses=house_id, companies=comp_id, unlinked=unlinked)


# ---------------------------------------------------------------- 5. loss given default
def lgd(pack, last_closed_year=2019):
    rows = read_csv(pack.path("lenderbase_workout_recoveries_2008-2026.csv"))
    rec = []
    for r in rows:
        v = r["recovery"].strip()
        if not v:
            continue
        x = float(v)
        rec.append((_date(r["default_date"]).year, x / 100.0 if x > 1.0 else x, _date(r["resolution_date"])))
    by_year = collections.defaultdict(list)
    for y, x, _ in rec:
        by_year[y].append(x)
    open_by_year = collections.Counter(_date(r["default_date"]).year for r in rows if r["workout_status"] == "Open")
    mature = [x for y, x, _ in rec if y <= last_closed_year]
    closed = [x for _, x, _ in rec]
    return dict(lgd=1 - float(np.mean(mature)), lgd_closed=1 - float(np.mean(closed)), n_mature=len(mature),
                n_closed=len(closed), open_by_year=dict(open_by_year),
                open_before=sum(v for y, v in open_by_year.items() if y <= last_closed_year))


# ---------------------------------------------------------------- 6. the tapes
def fx_rates(pack):
    rows = read_csv(pack.path("ecb_euro_reference_rates_2026-12.csv"))
    r = [x for x in rows if x["Date"] == "2026-12-31"][0]
    out = {k: float(v) for k, v in r.items() if k != "Date"}
    out["EUR"] = 1.0
    return out


def sector_map(pack):
    doc = json.load(open(pack.path("lenderbase_sector_codes.json"), encoding="utf-8"))
    m = {}
    for s in doc["sectors"]:
        i = int(s["code"][2:]) - 1
        m[s["agency_industry"].lower()] = i
        m[s["gics_industry_group"].lower()] = i
    return m


def tape(pack, which, by_name, fx, smap):
    if which == "KL":
        ws = openpyxl.load_workbook(pack.path("klcp_static_portfolio_2026-12-31.xlsx"), data_only=True)["Portfolio"]
        cols = dict(name=0, lei=1, ind=3, ccy=4, par=5, rating=7, orig=9)
    else:
        ws = openpyxl.load_workbook(pack.path("ostvale_collateral_tape_20261231.xlsx"), data_only=True)["Collateral"]
        cols = dict(name=0, lei=1, ind=3, ccy=4, par=5, rating=7, orig=8)
    rows = []
    hdr_seen = False
    for r in ws.iter_rows(values_only=True):
        if not hdr_seen:
            hdr_seen = r and r[0] in ("Obligor", "Borrower")
            continue
        if not r or r[0] is None:
            continue
        name = str(r[cols["name"]])
        key = (r[cols["lei"]] or "").strip() or by_name.get(norm_name(name), "NAME:" + norm_name(name))
        rows.append(dict(name=name, company=key, sector=smap[str(r[cols["ind"]]).lower()], ccy=r[cols["ccy"]],
                         eur=float(r[cols["par"]]) / fx[r[cols["ccy"]]], rating=_RATING[str(r[cols["rating"]])],
                         orig=r[cols["orig"]].date() if hasattr(r[cols["orig"]], "date") else r[cols["orig"]]))
    return rows


def port_spec(rows, buys, ids, clock="buy", year=2027):
    w, rr, a, k, h, f = [], [], [], [], [], []
    for x in rows:
        ds = [d for d in buys.get(x["company"], []) if d["date"] <= dt.date(2026, 12, 31)]
        sp = ds[-1]
        w.append(x["eur"])
        rr.append(x["rating"])
        a.append(max(1, (year - sp["date"].year) if clock == "buy" else (year - x["orig"].year)))
        k.append(x["sector"])
        h.append(ids["houses"].setdefault(sp["house"], len(ids["houses"])))
        f.append(ids["funds"].setdefault(sp["fund"] or sp["house"] + " ?", len(ids["funds"])))
    w = np.array(w)
    return dict(w=w / w.sum(), r=np.array(rr), a=np.array(a), k=np.array(k), h=np.array(h), f=np.array(f),
                par_eur=float(w.sum()))


# ---------------------------------------------------------------- evidence a reader can check
def pair_evidence(P):
    """Joint defaults among pairs at risk in the same year: same house (any fund) against different houses in the
    same sector-year, like for like; and the same house in different years (a lasting house effect would show)."""
    out = {}
    by_y = collections.defaultdict(list)
    for row in P:
        by_y[int(row[1])].append(row)
    same_h = same_h_d = diff_h = diff_h_d = 0
    for y, rs in by_y.items():
        rs = np.array(rs)
        for k in np.unique(rs[:, 3]):
            s = rs[rs[:, 3] == k]
            n = len(s)
            if n < 2:
                continue
            dsum = s[:, 6].sum()
            all_pairs = n * (n - 1) // 2
            all_dd = dsum * (dsum - 1) // 2
            hh = collections.Counter(s[:, 7].tolist())
            hd = collections.Counter(s[s[:, 6] == 1, 7].tolist())
            sp = sum(v * (v - 1) // 2 for v in hh.values())
            sdd = sum(v * (v - 1) // 2 for v in hd.values())
            same_h += sp
            same_h_d += sdd
            diff_h += all_pairs - sp
            diff_h_d += all_dd - sdd
    out["same_house_same_sector_year"] = (int(same_h_d), int(same_h))
    out["other_house_same_sector_year"] = (int(diff_h_d), int(diff_h))
    # same house, any sector, same year against different years
    hy = collections.Counter()
    hyd = collections.Counter()
    for row in P:
        hy[(int(row[7]), int(row[1]))] += 1
        hyd[(int(row[7]), int(row[1]))] += int(row[6])
    houses = collections.defaultdict(dict)
    for (h, y), n in hy.items():
        houses[h][y] = (n, hyd[(h, y)])
    same_y = same_y_d = cross_y = cross_y_d = 0
    for h, yy in houses.items():
        ys = sorted(yy)
        for i, y in enumerate(ys):
            n, d = yy[y]
            same_y += n * (n - 1) // 2
            same_y_d += d * (d - 1) // 2
            for y2 in ys[i + 1:]:
                n2, d2 = yy[y2]
                cross_y += n * n2
                cross_y_d += d * d2
    out["same_house_same_year"] = (int(same_y_d), int(same_y))
    out["same_house_other_year"] = (int(cross_y_d), int(cross_y))
    pd_all = P[:, 6].mean()
    out["base_rate"] = float(pd_all)
    return out


def run(root, nsim=NSIM, rivals=True):
    pack = Pack(root)
    by_name = lei_index(pack)
    L = loans(pack, by_name)
    buys = deals(pack, by_name)
    P, ids = panel(L, buys)
    E = MD.estimate(P)
    G = lgd(pack)
    fx = fx_rates(pack)
    smap = sector_map(pack)
    tapes = {k: tape(pack, k, by_name, fx, smap) for k in ("KL", "OS")}
    ports = {k: port_spec(v, buys, ids) for k, v in tapes.items()}
    res = dict(est={k: v for k, v in E.items() if k != "pdt"}, pdt=E["pdt"].tolist(), lgd=G, panel_n=int(len(P)),
               panel_defaults=int(P[:, 6].sum()), unlinked=ids["unlinked"], n_houses=len(ids["houses"]),
               n_funds=len(ids["funds"]), ports={})
    res["evidence"] = pair_evidence(P)
    golden = dict(am=E["am"], ak=E["ak"], ah=E["ah"])
    for k, p in ports.items():
        cum = MD.simulate(p, E["pdt"], lgd=G["lgd"], nsim=nsim, seed=SEED, **golden)
        s = MD.summary(cum, SUBORD[k], TARGETS)
        s.update(n=int(len(p["w"])), houses=int(len(set(p["h"]))), funds=int(len(set(p["f"]))),
                 sectors=int(len(set(p["k"]))), par_eur=p["par_eur"], ratings=np.bincount(p["r"], minlength=4).tolist(),
                 age=float(np.mean(p["a"])), pd1=float((p["w"] * E["pdt"][p["r"], p["a"]]).sum()))
        res["ports"][k] = s
    if rivals:
        res["rivals"] = {}
        routes = {"one_factor": dict(am=E["am"]), "industry": dict(am=E["am"], ak=E["ak"]),
                  "fund_year": dict(am=E["am"], ak=E["ak"], af=E["af"]),
                  "fund_persistent": dict(am=E["am"], ak=E["ak"], aq=E["aq"]),
                  "golden_closed_lgd": dict(am=E["am"], ak=E["ak"], ah=E["ah"], lgd=G["lgd_closed"])}
        for name, kw in routes.items():
            kw = dict(kw)
            lg = kw.pop("lgd", G["lgd"])
            res["rivals"][name] = {}
            for k, p in ports.items():
                cum = MD.simulate(p, E["pdt"], lgd=lg, nsim=max(200_000, nsim // 5), seed=SEED + 1, **kw)
                s = MD.summary(cum, SUBORD[k], TARGETS)
                res["rivals"][name][k] = dict(p5=s["p5"], by_year=s["by_year"], need=s["need"])
    if rivals:
        # the band the sound estimators span: two default-rate tables against two dependence estimators
        pdts = {"probit": E["pdt"], "cohort": MD.cohort_pdt(P)}
        deps = {"cluster": golden, "moment": MD.moment_dependence(P)}
        band = {k: [] for k in ports}
        for pn, pt in pdts.items():
            for dn, dep in deps.items():
                for k, p in ports.items():
                    cum = MD.simulate(p, pt, lgd=G["lgd"], nsim=max(200_000, nsim // 5), seed=SEED + 2, **dep)
                    band[k].append(float((cum[-1] > SUBORD[k]).mean()))
        res["band"] = {k: [min(v), max(v)] for k, v in band.items()}
        res["moment_dependence"] = deps["moment"]
    res["_ports"] = ports
    res["_panel"] = P
    return res


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    R = run(sys.argv[1], nsim=int(sys.argv[2]) if len(sys.argv) > 2 else 200_000)
    print("panel", R["panel_n"], "defaults", R["panel_defaults"], "unlinked loans", R["unlinked"], "houses", R["n_houses"],
          "funds", R["n_funds"])
    print({k: round(v, 4) if isinstance(v, float) else v for k, v in R["est"].items()})
    print("lgd", R["lgd"])
    print("evidence", R["evidence"])
    for k, s in R["ports"].items():
        print(k, "n", s["n"], "houses", s["houses"], "p5 %.4f" % s["p5"], "by year", [round(100 * v, 2) for v in s["by_year"]],
              "need", [round(100 * v, 1) for v in s["need"]], "pd1 %.4f" % s["pd1"], "age %.2f" % s["age"])
    for name, d in R.get("rivals", {}).items():
        print("%-18s" % name, {k: round(100 * v["p5"], 2) for k, v in d.items()})
    print("%.0fs" % (time.time() - t0))
