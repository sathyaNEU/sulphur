"""The independent verifier: reads only the shipped bundle (target/ and the answer blocks in submission.md) on its
own code path (the csv module, no generator module, no pandas) and recomputes the paying base, the counted hours
per paying subscription-month, each plan's contribution per spring 2024 trial start and the lead plan, then checks
them against the answer blocks. Exit 1 on any failure."""
import csv
import os
import re
import subprocess
import sys
from collections import defaultdict

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
PLANS = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
FAIL = []


def rd(name):
    with open(os.path.join(T, name), encoding="utf-8") as f:
        yield from csv.DictReader(f)


def mi(s):
    return (int(s[:4]) - 2023) * 12 + int(s[5:7]) - 1


def ok(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def pdf(name):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", os.path.join(T, name), "-"],
                                              capture_output=True, text=True).stdout)


def main():
    sub = open(os.path.join(TASK, "submission.md")).read()
    sb = pdf("SUL_licence_agreement_2027-2029_schedule_B.pdf")
    rate = float(re.search(r"EUR (\d+\.\d+) for every counted hour", sb).group(1))
    ok("schedule B read: the rate", rate > 0, str(rate))
    quote = pdf("spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf")
    fee = {k: float(re.search(r"Kraanvogel %s EUR (\d+\.\d+)" % v, quote).group(1)) for k, v in PLANS.items()}
    ok("quote read: four fees", len(fee) == 4, str(fee))
    price = pdf("price_list_2027.pdf")
    p27 = {k: float(re.search(r"Kraanvogel %s .*?EUR (\d+\.\d+)" % v, price).group(1)) for k, v in PLANS.items()}
    ok("price list read", len(p27) == 4, str(p27))
    consumer = {r["account_id"] for r in rd("accounts_export_2026-11-03.csv") if r["account_type"] == "consumer"}
    spring = {r["account_id"]: (mi(r["created_on"]), r["signup_source"][5:]) for r in rd("accounts_export_2026-11-03.csv")
              if r["signup_source"].startswith("VJ24-") and r["account_type"] == "consumer" and r["created_on"] < "2024-04"}
    paying = {}
    members = {}
    for r in rd("payments_2024-01_2026-10.csv"):
        m = mi(r["charged_on"])
        if r["profiles_on_subscription"]:
            for p in r["profiles_on_subscription"].split(";"):
                members[(p, m)] = r["account_id"]
        if r["account_id"] in consumer and r["status"] in ("collected", "re-presented") and float(r["amount_eur"]) > 0:
            paying[(r["account_id"], m)] = (r["plan_code"], r["route"], float(r["vat_rate"]))
    oct_ = defaultdict(int)
    for (a, m), v in paying.items():
        if m == 45:
            oct_[v[0]] += 1
    for k, v in PLANS.items():
        ok("R1 %s paying at 31 October 2026" % v, ("%s %s" % (v, format(oct_[k], ","))) in sub, str(oct_[k]))
    licensed = {r["title_id"] for r in rd("catalogue_2026-10.csv") if r["rights"] == "licensed"}
    best = defaultdict(float)
    seen = set()
    for r in rd("listening_monthly_2024-01_2026-10.csv"):
        key = tuple(r.values())
        if key in seen or r["title_id"] not in licensed:
            continue
        seen.add(key)
        k = (r["profile_id"], r["title_id"], mi(r["month"]))
        best[k] = max(best[k], float(r["furthest_position_s"]))
    for r in rd("licence_server_renewals_2024-01_2026-10.csv"):
        if r["title_id"] not in licensed:
            continue
        k = (r["profile_id"], r["title_id"], mi(r["renewed_at_utc"]))
        best[k] = max(best[k], float(r["position_s"]))
    run = {}
    hours = defaultdict(float)
    for (p, t, m) in sorted(best, key=lambda x: (x[0], x[1], x[2])):
        prev = run.get((p, t), 0.0)
        if best[(p, t, m)] > prev:
            hours[(p, m)] += (best[(p, t, m)] - prev) / 3600.0
            run[(p, t)] = best[(p, t, m)]
    today = {r["profile_id"]: r["account_id"] for r in rd("profiles_export_2026-11-03.csv")}
    by_p = defaultdict(list)
    for (p, m), a in members.items():
        by_p[p].append((m, a))
    acc_h = defaultdict(float)
    for (p, m), h in hours.items():
        a = members.get((p, m))
        if a is None:
            lst = sorted(by_p.get(p, []))
            later = [x for x in lst if x[0] > m]
            earlier = [x for x in lst if x[0] < m]
            a = later[0][1] if later else (earlier[-1][1] if earlier else today.get(p))
        acc_h[(a, m)] += h
    num, den = defaultdict(float), defaultdict(int)
    for (a, m), v in paying.items():
        if 34 <= m <= 45:
            num[v[0]] += acc_h.get((a, m), 0.0)
            den[v[0]] += 1
    for k, v in PLANS.items():
        val = num[k] / den[k]
        ok("R2 %s counted hours per paying month" % v, ("%s %.2f" % (v, val)) in sub, "%.2f" % val)
    contrib = {}
    for k, v in PLANS.items():
        ids = [a for a, (m0, pl) in spring.items() if pl == k]
        rev = hrs = 0.0
        for a in ids:
            m0 = spring[a][0]
            ms = sorted(m for (aa, m) in paying if aa == a)
            for i, m in enumerate(ms, 1):
                if m0 <= m < m0 + 24:
                    pl, route, vat = paying[(a, m)]
                    f = (0.30 if i <= 12 else 0.15) if route == "apple" else (0.15 if route == "google" else 0.0)
                    rev += p27[pl] / (1 + vat) * (1 - f)
            hrs += sum(acc_h.get((a, m), 0.0) for m in range(m0, m0 + 24))
        contrib[k] = (rev - rate * hrs) / len(ids) - fee[k]
        ok("R5 %s contribution per trial start" % v, ("%s %.1f" % (v, contrib[k])) in sub, "%.1f" % contrib[k])
    lead = PLANS[max(contrib, key=contrib.get)]
    ok("R7 the lead plan", ("Lead the spring 2027 campaign with %s" % lead) in sub, lead)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
