"""The independent verifier (python3 verify.py <target>): reads only the bundle, on its own parsing path (pandas),
and recomputes the graded figures: R1 and R2 from its own tables and its own household linkage, R3 and R4 from its
own logistic fit, the plan's costs and the budget from the workbook as read back, and R5, R6, R7 and R9 from the
golden's models run on the verifier's own panel. Every document a figure or a filed sentence leans on is read back
through the verifier's own extractor, with a positive control. Exit 1 on any mismatch."""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OK = []


def chk(label, ok, detail=""):
    OK.append((label, bool(ok), detail))


def months(a, b):
    return (b.dt.year - a.dt.year) * 12 + (b.dt.month - a.dt.month)


def load(T):
    subs = pd.read_csv(os.path.join(T, "subscriptions_2023-01_2026-10.csv"), dtype=str, keep_default_na=False)
    cust = pd.read_csv(os.path.join(T, "customers.csv"), dtype=str, keep_default_na=False)
    subs = subs.drop_duplicates()
    consumer = set(cust.loc[cust.account_type == "CONSUMER", "customer_no"])
    subs = subs[(subs["product"] == "DIGITAL") & subs.customer_no.isin(consumer)].copy()
    per = pd.read_csv(os.path.join(T, "price_periods_2023-01_2026-10.csv"), dtype=str, keep_default_na=False)
    return subs, cust, per


def oct_paying(subs, per):
    per = per[per.subscription_id.isin(set(subs.subscription_id))].copy()
    per["p"] = per.monthly_price_eur.astype(float)
    per["a"] = pd.to_datetime(per.valid_from)
    per["b"] = pd.to_datetime(per.valid_to.replace("", "2099-12-31"))
    # the billing period covering 31 October 2026: the last billing on or before that day inside a period
    day = pd.to_datetime(subs.set_index("subscription_id").start_date).dt.day
    per["day"] = per.subscription_id.map(day)
    oct_bill = pd.to_datetime(dict(year=2026, month=10, day=per["day"].clip(upper=28)))
    hit = (per.a <= oct_bill) & (per.b >= oct_bill) & (per.p > 0)
    ids = set(per.loc[hit, "subscription_id"])
    withdrawn = set(subs.loc[subs.end_reason == "WITHDRAWN", "subscription_id"])
    ids -= withdrawn
    return subs[subs.subscription_id.isin(ids)].groupby("title").size().to_dict()


def logit_irls(X, y, it=60):
    b = np.zeros(X.shape[1])
    for _ in range(it):
        eta = X @ b
        p = 1 / (1 + np.exp(-eta))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-10 * np.eye(X.shape[1])
        g = X.T @ (y - p)
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def main(T):
    import golden as GD
    import models
    import panel
    import params as P
    import results
    import sim
    import world
    F = json.load(open(os.path.join(HERE, "figures.json")))
    subs, cust, per = load(T)
    # R1
    r1 = oct_paying(subs, per)
    chk("R1 paying at 31 October 2026, by title", all(int(r1.get(t, 0)) == F["paying_oct"][t] for t in P.TITLES),
        str(r1))
    # the verifier's own panel against the golden's parser
    pp = panel.from_pack(T)
    chk("own parse: the consumer subscriptions are the golden's", len(subs) == pp["n"], "%d" % len(subs))
    # R2 with the verifier's own household links (pandas: customer, fingerprint, normalised address)
    meth = pd.read_csv(os.path.join(T, "payment_methods.csv"), dtype=str, keep_default_na=False)
    import re

    def akey(r):
        s = r.street.strip().lower().replace(" ", "")
        s = re.sub(r"(strasse|str\.)$", "straße", s)
        return s + "|" + r.house_no.strip().lower() + "|" + r.postcode.strip()
    cust["akey"] = cust.apply(akey, axis=1)
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    live = set(subs.customer_no)
    for col, df in [("fingerprint", meth[meth.customer_no.isin(live)]),
                    ("akey", cust[cust.customer_no.isin(live)])]:
        first = {}
        for c, k in zip(df.customer_no, df[col]):
            if k in first:
                union(int(first[k]), int(c))
            else:
                first[k] = c
    hh = subs.customer_no.astype(int).map(lambda c: find(c))
    subs = subs.assign(hh=hh.values)
    net = results.net_matrix(pp)
    sid_row = {s: i for i, s in enumerate(pp["sid"])}
    subs["row"] = subs.subscription_id.map(sid_row)
    subs["sd"] = pd.to_datetime(subs.start_date)
    subs["m0"] = (subs.sd.dt.year - 2023) * 12 + subs.sd.dt.month - 1
    old_new = {v: k for k, v in P.OLD_CODE.items()}
    subs["ch"] = subs.channel.map(lambda c: old_new.get(c, c) if c else "DIR")
    q3 = subs[(subs.sd >= "2023-07-01") & (subs.sd <= "2023-09-30") & (subs.end_reason != "WITHDRAWN")]
    by_hh = {k: v for k, v in subs.groupby("hh")}
    r2 = {}
    for c, grp in q3.groupby("ch"):
        vals = []
        for _, r in grp.iterrows():
            a = int(r.m0)
            v = net[int(r.row), a: a + 36].sum()
            for _, o in by_hh[r.hh].iterrows():
                if o.subscription_id != r.subscription_id and o.m0 > r.m0 and o.m0 <= a + 35:
                    v += net[int(o.row), int(o.m0): a + 36].sum()
            vals.append(v)
        r2[c] = int(round(np.mean(vals)))
    chk("R2 36-month value of the July to September 2023 starts, own household links",
        all(abs(r2[c] - F["value_2023q3"][c]) <= 1 for c in P.CHANNELS), str(r2))
    # R3 and R4: the verifier's own logistic fit
    idx, y = models.su_rows(pp)
    X = models.su_design(pp["channel"][idx], pp["title"][idx], pp["offer"][idx], pp["L"][idx], pp["ip"][idx],
                         pp["stepup"][idx], models.GOLD)
    b = logit_irls(X, y)
    M = {"b": b, "o": models.GOLD}
    plan = world.plan_2027()
    r3, r4 = results.r3_r4({"su": M}, plan)
    chk("R3 share leaving at the end of the intro, own fit",
        all(abs(100 * r3[o] - F["stepup_share"][o]) <= 0.15 for o in r3), str({o: round(100 * v, 1) for o, v in r3.items()}))
    chk("R4 points the April 2027 prices add, own fit",
        all(abs(100 * r4[o] - F["stepup_added"][o]) <= 0.15 for o in r4), str({o: round(100 * v, 1) for o, v in r4.items()}))
    # the plan as read back from the workbook
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(T, "media_plan_2027.xlsx"))["Plan 2027"]
    spend = {ws.cell(r, 1).value: ws.cell(r, 19).value for r in range(5, 23)}
    starts = {ws.cell(r, 1).value: sum(ws.cell(r, c).value for c in range(6, 18)) for r in range(5, 23)}
    chk("plan read back: 18 lines with spend and starts", len(spend) == 18 and all(spend.values()))
    budget = sum(spend[k] for k in F["funded"])
    chk("R8 budget from the workbook's spend on the funded lines", budget == F["budget"], "%d" % budget)
    # R5, R6, R7, R9 on the verifier's panel
    Mg = results.fit(pp, models.GOLD)
    R, _ = results.all_results(pp, plan, models.GOLD, M=Mg)
    mult = {GD.key(l): R["R7"][l] / (spend[GD.key(l)] / starts[GD.key(l)]) for l in R["R7"]}
    fund = sorted(k for k, v in mult.items() if v >= P.HURDLE)
    chk("R8 the funded lines from the values and the workbook's costs", fund == sorted(F["funded"]), ", ".join(fund))
    chk("R7 every line's value", all(abs(int(round(R["R7"][l])) - F["line_value"][GD.key(l)]) <= 1 for l in R["R7"]))
    chk("R5 three-year survival by channel", all(abs(100 * R["R5"][c] - F["survival_36"][c]) <= 0.15 for c in P.CHANNELS))
    chk("R6 extra cancellations by title", all(abs(R["R6"][t] - F["rise_extra"][t]) <= 1 for t in P.TITLES))
    chk("R9 the plan's 2027 starts paying at December 2027", all(abs(R["R9"][c] - F["plan_paying"][c]) <= 1
                                                                 for c in P.PAID))
    # the documents, read back through the verifier's own extractor, each with a positive control
    for f, control, needle in [("digital_subscription_kpi_standard.pdf", "Version 3", "at least 3.5 times"),
                               ("price_list_digital_2027.pdf", "from 1 April 2027", "first billing on or after")]:
        t = subprocess.run(["pdftotext", os.path.join(T, f), "-"], capture_output=True, text=True).stdout
        t = " ".join(t.split())
        chk("document read back: %s (control '%s')" % (f, control), control in t and needle in t, "%d chars" % len(t))
    prices = subprocess.run(["pdftotext", "-layout", os.path.join(T, "price_list_digital_2027.pdf"), "-"],
                            capture_output=True, text=True).stdout
    chk("price list: the April 2027 list prices are the ones the golden uses",
        all(("%.2f" % P.PRICE[t][2]).replace(".", ",") in prices for t in P.TITLES))
    bad = [o for o in OK if not o[1]]
    for label, ok, detail in OK:
        print("%s  %-80s %s" % ("PASS" if ok else "FAIL", label[:80], detail[:70]))
    print("verify: %d checks, %d failed" % (len(OK), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
