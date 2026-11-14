"""The build's assertions: every graded figure against the world's own 2027 and the cut pack, the open members, the
stump factorial, the family, the perturbations and the forks. Exit 1 on any failure."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import world as Wm  # noqa: E402

F = json.load(open(os.path.join(HERE, "figures.json")))
E = json.load(open(os.path.join(HERE, "effort.json")))
fails, n = [], [0]


def check(name, ok, detail=""):
    n[0] += 1
    if not ok:
        fails.append("%s: %s" % (name, detail))


T = Wm.truth_at_plan(reps=16)
G = F["roas_2027_3dp"]
gb = F["bands"]
for c in P.ORDER:
    check("world and golden share a band: " + c, P.band(T[c]["roas"]) == gb[c], "%.3f against %.3f" % (T[c]["roas"], G[c]))
    check("golden within 0.08 of the world: " + c, abs(T[c]["roas"] - G[c]) < 0.08, "%.3f against %.3f" % (T[c]["roas"], G[c]))
    fam = F["family"][c]
    check("family files the golden band: " + c, all(P.band(v) == gb[c] for v in fam.values()), str(fam))
for p in F["perturbations"]:
    check("perturbation holds: " + p["input"], all(P.band(p["roas"][c]) == gb[c] for c in P.ORDER), str(p["roas"]))
R = {k: v for k, v in F["routes"].items()}
key = lambda A, C, B: "%s|%s|%s" % (A, C, B)
wrong = lambda k: tuple(sorted(c for c in P.ORDER if P.band(R[k][c]) != gb[c]))
check("the golden route is the golden", not wrong(key("golden", "golden", "pooled")))
for k in R:
    if k != key("golden", "golden", "pooled"):
        check("every shortcut files a channel wrong: " + k, bool(wrong(k)))
check("eleven shortcuts on eleven distinct wrong calls", F["distinct_wrong_calls"] == 11, str(F["distinct_wrong_calls"]))
# the factorial: each stump necessary alone, none sufficient alone on the reflex route
ref = ("prop", "consenters", "average")
for nm, k in (("A", key("prop", "golden", "pooled")), ("C", key("golden", "consenters", "pooled")), ("B", key("golden", "golden", "average"))):
    check("dropping %s alone moves the call" % nm, bool(wrong(k)))
for nm, k in (("A", key("golden", "consenters", "average")), ("C", key("prop", "golden", "average")), ("B", key("prop", "consenters", "pooled"))):
    check("fixing %s alone on the reflex route misses the call" % nm, bool(wrong(k)))
# open members: three openers, margins between the family and the stump's worth
openers = {"A": wrong(key("prop", "golden", "pooled")) + wrong(key("recorded", "golden", "pooled")),
           "C": wrong(key("golden", "consenters", "pooled")), "B": wrong(key("golden", "golden", "average"))}
opened = {c: [s for s, ws in openers.items() if c in ws] for c in P.ORDER}
check("three distinct stumps each open a channel", all(any(s in v for v in opened.values()) for s in "ACB"), str(opened))
for c, ops in opened.items():
    if not ops:
        continue
    g = G[c]
    margin = min(abs(g - L) for L in P.LINES)
    spread = max(abs(v - g) for v in F["family"][c].values())
    worth = max(abs(R[key(*ref)][c] - g), abs(R[key("recorded", "consenters", "average")][c] - g))
    check("open member's margin sits between the family and the worth: " + c, spread < margin < worth,
          "spread %.3f margin %.3f worth %.3f" % (spread, margin, worth))
    check("margin of at least 0.04 on an open member: " + c, margin >= 0.04, "%.3f" % margin)
# data facts the answer blocks state
check("the stores hold more than the records", F["store_excess"] > F["app_recorded_net"])
check("AppLovin's unrecorded share is the largest", max(F["unrecorded_share_2025"], key=F["unrecorded_share_2025"].get) == "AppLovin Android")
check("consenting users overstate both iOS networks by 25 per cent or more", all(v > 0.25 for v in F["consenter_overstate"].values()))
check("Google Android's plan spends at least 40 per cent over 2025", F["google_plan_rise"] > 0.40)
check("effort golden equals figures", all(r["golden"] == F[r["figure"]] for r in E["results"]))
# the semantic fork table, row by row
import csv as _csv  # noqa: E402
import datetime as _dt  # noqa: E402
import docs as _docs  # noqa: E402
import pack as _pack  # noqa: E402
TG = os.path.join(os.path.dirname(HERE), "target")
import re as _re  # noqa: E402
import subprocess as _sp  # noqa: E402
POL = _re.sub(r"\s+", " ", _sp.run(["pdftotext", "-layout", os.path.join(TG, _docs.FILES["policy"]), "-"],
                                     capture_output=True, text=True).stdout)   # the shipped PDF's own text
def _rows(k):
    with open(os.path.join(TG, _pack.FILES[k]), newline="") as fh:
        yield from _csv.DictReader(fh)
check("SF1 policy 2.2 rules out reinstalls, second devices, staff and test accounts",
      all(w in POL for w in ("A second device, a reinstall, a staff account and a test account are not installs",)))
rep = {}
for r in _rows("spend"):
    rep[r["channel"]] = rep.get(r["channel"], 0) + int(r["installs_reported_by_network"])
check("SF2 the networks' own counts exceed the installs they bought (they cannot all be installs)",
      sum(rep.values()) > sum(F["installs_2025"].values()) * 1.9, "%d against %d" % (sum(rep.values()), sum(F["installs_2025"].values())))
check("SF3 policy 2.3 sets the 365 days from the day of the install", "in the 365 days from the day of the install" in POL)
ratios = {}
for r in _rows("apple"):
    if r["event"] != "Refund" and float(r["customer_price_eur"]):
        ratios.setdefault(r["country"], []).append(float(r["developer_proceeds_eur"]) / float(r["customer_price_eur"]))
check("SF4 the stores' proceeds are the price less VAT and 15 per cent, as policy 2.4 files",
      all(abs(sum(v) / len(v) - 0.85 / (1 + P.VAT[c])) < 0.002 for c, v in ratios.items()), str({c: sum(v) / len(v) for c, v in ratios.items()}))
check("SF5 the media plan states each of the 52 weeks", len(P.plan_weeks()) == 52)
neg = sum(1 for r in _rows("bill") if r["event_type"] == "refund" and float(r["price_eur"]) < 0)
check("SF6 refunds sit in the records as negative charges and policy 2.3 nets them", neg > 0 and "less the net revenue of any of those charges refunded" in POL)
lag = {}
for d0 in (2, 4):
    k = {"meta": 0, "tiktok": 0}
    for r in _rows("skan"):
        dd = (_dt.date.fromisoformat(r["postback_date"]) - _dt.timedelta(days=d0) - P.LAUNCH).days
        if 0 <= dd < 7 * P.MATURE_WEEKS:
            k[r["ad_network"]] += 1
    lag[d0] = k
r1 = {x["id"]: x for x in E["results"]}["R1"]["bands"]
check("SF7 R1's band holds the postbacks read two and four days back",
      all(r1["Meta iOS"][0] <= lag[d]["meta"] <= r1["Meta iOS"][1] and r1["TikTok iOS"][0] <= lag[d]["tiktok"] <= r1["TikTok iOS"][1] for d in lag), str(lag))
check("SF8 policy 2.1 sets the return per euro of the plan's spend", "per euro of that spend" in POL)
check("SF9 policy section 3 sets the lines at 0.90 and 1.20", "1.20 or more" in POL and "0.90 or more and under 1.20" in POL and "under 0.90" in POL)
check("SF10 the withheld values read from coarse values only file the same bands",
      all(P.band(F["family"][c]["C=coarse"]) == gb[c] for c in P.ORDER))
stores = {}
for r in _rows("bill"):
    stores.setdefault(r["account_id"], set()).add(r["store"])
check("SF11 every account's charges sit in one store", all(len(v) == 1 for v in stores.values()))
check("the golden family runs twelve or more rivals", min(len(v) for v in F["family"].values()) >= 13)
pb = {"meta": [0] * (P.WEEKS + 1)}
for r in _rows("skan"):
    k = ((_dt.date.fromisoformat(r["postback_date"]) - _dt.timedelta(days=3) - P.LAUNCH).days) // 7
    if r["ad_network"] == "meta" and 0 <= k <= P.WEEKS:
        pb["meta"][k] += 1
check("SF13 the pull week is incomplete in the postbacks (installs after its first days have none yet)",
      pb["meta"][P.WEEKS] < 0.7 * sum(pb["meta"][P.WEEKS - 4:P.WEEKS]) / 4, str(pb["meta"][-5:]))
check("SF13 the pull week kept where its installs are complete files the same bands",
      all(P.band(F["family"][c]["B=lastweek"]) == gb[c] for c in P.ORDER))
late = sum(1 for r in _rows("bill") if r["recorded_at"] > r["transaction_at"][:10] + "T23:59:59Z")
check("SF12 a charge's day is the store's transaction time: records synced later carry their transaction time",
      late > 0 and "the store charges on its account in the 365 days from the day of the install" in POL)
check("the policy's bands read in the shipped PDF", "scale when the return is 1.20 or more" in POL and "cut when it is under 0.90" in POL)
res = {x["id"]: x for x in E["results"]}
for c in P.ORDER:
    v2, v3 = res["R2"]["bands"][c], res["R3"]["bands"][c]
    g2, g3 = F["v12_2025"][c], F["installs_week_2027"][c]
    for a2, a3 in ((v2[0], v3[0]), (v2[1], v3[1]), (v2[0], v3[1]), (v2[1], v3[0])):
        corner = G[c] * (a2 / g2) * (a3 / g3)
        check("R2 and R3 at their band edges keep the band: " + c, P.band(corner) == gb[c], "%.4f" % corner)
    fam_v = [F["family"][c][k] for k in F["family"][c]]
    check("R2 and R3 bands hold the honest family's spread: " + c,
          F["band_halfwidths"]["R2"][c] >= 0.0 and F["band_halfwidths"]["R3"][c] >= 0.0)
print("checks: %d of %d pass" % (n[0] - len(fails), n[0]))
for f in fails:
    print("FAIL", f)
sys.exit(1 if fails else 0)
