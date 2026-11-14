"""An independent recompute of the graded figures from the shipped files alone, by a second code path (plain csv,
no pandas, no analysis.py): the installs bought, the stores' excess, each channel's recorded 12-month value, and the
bands from the stated returns. Exit 1 on a mismatch."""
import csv
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import pack  # noqa: E402
import params as P  # noqa: E402

F = json.load(open(os.path.join(HERE, "figures.json")))
fails, n = [], [0]


def check(name, ok, detail=""):
    n[0] += 1
    if not ok:
        fails.append("%s: %s" % (name, detail))


def rows(k):
    with open(os.path.join(TARGET, pack.FILES[k]), newline="") as f:
        yield from csv.DictReader(f)


L0 = P.LAUNCH
acc = {}
for r in rows("acc"):
    if r["account_type"] == "consumer":
        acc[r["account_id"]] = r
first = {}
seen = set()
for r in rows("attr"):
    if r["install_id"] in seen or r["is_reinstall"] == "true":
        continue
    seen.add(r["install_id"])
    a = r["account_id"]
    if a not in first or r["install_time"] < first[a]["install_time"]:
        first[a] = r
CH = {("Meta Ads", "ios"): "Meta iOS", ("TikTok For Business", "ios"): "TikTok iOS", ("Apple Search Ads", "ios"): "Apple Search Ads",
      ("Meta Ads", "android"): "Meta Android", ("Google Ads", "android"): "Google Android",
      ("TikTok For Business", "android"): "TikTok Android", ("AppLovin", "android"): "AppLovin Android"}
inst = {c: 0 for c in P.ORDER}
chan = {}
for a, r in acc.items():
    d = (dt.datetime.strptime(r["created_at"], "%Y-%m-%dT%H:%M:%SZ").date() - L0).days
    f = first.get(a)
    c = CH.get((f["media_source"], f["platform"]), "organic") if f else "organic"
    chan[a] = (c, d, r["country"], r["created_at"])
    if c in inst and 0 <= d < 7 * P.MATURE_WEEKS:
        inst[c] += 1
sk = {"meta": 0, "tiktok": 0}
for r in rows("skan"):
    d = (dt.date.fromisoformat(r["postback_date"]) - dt.timedelta(days=3) - L0).days
    if 0 <= d < 7 * P.MATURE_WEEKS:
        sk[r["ad_network"]] += 1
inst["Meta iOS"], inst["TikTok iOS"] = sk["meta"], sk["tiktok"]
for c in P.ORDER:
    check("installs bought: " + c, inst[c] == F["installs_2025"][c], "%d against %d" % (inst[c], F["installs_2025"][c]))
# the stores' net revenue against the billing records' over the whole window
net = lambda price, cc: float(price) / (1 + P.VAT[cc]) * (1 - P.COMMISSION)
app = 0.0
rec12 = {}
for r in rows("bill"):
    if r["environment"] != "production" or r["account_id"] not in acc:
        continue
    v = net(r["price_eur"], r["storefront"])
    app += v
    c, d, cc, cr = chan[r["account_id"]]
    t = dt.datetime.strptime(r["transaction_at"], "%Y-%m-%dT%H:%M:%SZ")
    c0 = dt.datetime.strptime(cr, "%Y-%m-%dT%H:%M:%SZ")
    if t.date() >= c0.date() and t.date() < c0.date() + dt.timedelta(days=365):
        rec12[r["account_id"]] = rec12.get(r["account_id"], 0.0) + v
store = sum(float(r["developer_proceeds_eur"]) for r in rows("apple")) + sum(float(r["net_eur"]) for r in rows("google"))
check("the stores' net revenue", abs(store - F["store_excess"]) < 1.0, "%.2f against %.2f" % (store, F["store_excess"]))
check("the billing records' net revenue", abs(app - F["app_recorded_net"]) < 1.0, "%.2f against %.2f" % (app, F["app_recorded_net"]))
# each Android channel's recorded 12-month value sits below its stated value by its stated unrecorded share
for c, share in F["unrecorded_share_2025"].items():
    ids = [a for a, (cc, d, _, _) in chan.items() if cc == c and 0 <= d < 7 * P.MATURE_WEEKS]
    rv = sum(rec12.get(a, 0.0) for a in ids) / len(ids)
    stated = F["v12_2025"][c] * (1 - share)
    check("recorded value against the stated unrecorded share: " + c, abs(rv - stated) < 0.02 * stated + 0.02,
          "%.3f against %.3f" % (rv, stated))
for c in P.ORDER:
    check("band from the stated return: " + c, P.band(F["roas_2027_3dp"][c]) == F["bands"][c])
print("verify: %d of %d pass" % (n[0] - len(fails), n[0]))
for f in fails:
    print("FAIL", f)
sys.exit(1 if fails else 0)
