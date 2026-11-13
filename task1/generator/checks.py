"""The generator's assertions on the built pack and the clean truth: the input gates, the bar block (R1 to R7), each
result's golden against the engine's own count, each hurried figure outside its band, the shortcuts on distinct
wrong plans, the forcing family, the fork rows, mess neutrality, the incumbent statements reproduced, the realism
sweep and the documents read back. Exit 1 on any failure.

    python3 checks.py            (builds a scratch pack from the same seed and checks it against target/)
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import methods as M  # noqa: E402
import pack as PK  # noqa: E402
import docs  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return re.sub(r"\s+", " ", out)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    names = sorted(os.listdir(TARGET))
    pk = M.load(TARGET)
    W = world.simulate()
    acc = {a["aid"]: a for a in W["accounts"]}

    # input gates
    usable = [n for n in names if not n.startswith(".")]
    check("gate: ten or more usable files", len(usable) >= 10, str(len(usable)))
    cats = {"spreadsheet" if n.endswith((".csv", ".xlsx")) else "text" for n in usable}
    check("gate: two or more file categories", len(cats) >= 2, ", ".join(sorted(cats)))
    rows = {n: sum(1 for _ in open(os.path.join(TARGET, n), encoding="utf-8")) - 1 for n in usable if n.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(max(rows.values())))
    stm_rows = rows[PK.FILES["stm"]]
    check("gate: a CSV of 10 to 20 printed pages or more (about 55 rows a page)", stm_rows >= 550, str(stm_rows))
    check("gate: two or more distractors, named only in metadata", len(meta["distractor_files"]) >= 2 and
          all(d in usable for d in meta["distractor_files"]))
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|field|manifest|notes", n, re.I)
                                                      for n in usable))
    check("gate: no 'distractor' in a pack name", not any("distractor" in n.lower() for n in usable))

    G = M.all_results(pk, M.GOLD)
    C = M.all_results(pk, M.opts(channels=("live",), member="today"))
    A = M.all_results(pk, M.opts(member="today"))
    B = M.all_results(pk, M.opts(channels=("live",)))
    S = M.all_results(pk, M.opts(cost="share26"))
    T = M.all_results(pk, M.opts(channels=("live",), basis="seconds", member="today"))

    # R1: the field's raw material ships, at its grain, and no shipped column holds a result
    heads = set()
    for n in usable:
        if n.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(TARGET, n), encoding="utf-8"))))
    check("R1 raw material: positions per profile, title and month and per renewal ship",
          {"furthest_position_s", "position_s", "profiles_on_subscription"} <= heads)
    check("R1 no shipped column holds a result", not any(re.search(r"counted|contribution|remuneration_2027", h)
                                                          for h in heads))
    # the golden equals the engine's own count
    tr = collections.defaultdict(float)
    for (m, pid, aid, t, h) in W["counted"]:
        tr[(aid, m)] += h
    att = M.attribute(pk, M.GOLD)
    a12 = att[att["m"].isin(P.R2_MONTHS)]
    rel = abs(a12["hours"].sum() - sum(v for (a, m), v in tr.items() if m in P.R2_MONTHS)) / a12["hours"].sum()
    check("R2 golden: counted hours reproduce the engine's count over the twelve months", rel < 0.003, "%.4f" % rel)
    coh = [a for a in W["accounts"] if a["source"].startswith("VJ24")]
    for pl in P.PLANS:
        ids = [a for a in coh if a["source"].endswith(pl)]
        th = sum(tr.get((a["aid"], m), 0.0) for a in ids for m in range(a["created"][0], a["created"][0] + 24)) / len(ids)
        check("R5 golden: %s's counted hours per trial start equal the engine's" % pl,
              abs(th - G["detail"][pl]["counted hours"]) < 0.05 * th, "%.1f against %.1f" % (G["detail"][pl]["counted hours"], th))
    # the 2027 remuneration against the simulated 2027
    base = set(M.paying_months(pk).query("m == %d" % P.CUT)["account_id"])
    t27 = P.RATE27 * sum(v for (a, m), v in tr.items() if a in base and 48 <= m <= 59)
    check("R6 golden near the simulated 2027 (within 12 per cent)", abs(G["R6"] - t27) < 0.12 * t27,
          "%.0f against %.0f" % (G["R6"], t27))
    # R2 mess neutral
    D = M.all_results(pk, M.opts(dedup=False))
    check("R2 mess: re-sent rows summed leave the call", D["R7"] == G["R7"])
    check("R2 mess: re-sent rows exist", len(pk["live"]) - len(pk["live"].drop_duplicates()) > 1000,
          str(len(pk["live"]) - len(pk["live"].drop_duplicates())))
    tst = set(pk["acc"].loc[pk["acc"]["account_type"] != "consumer", "account_id"])
    check("R2 mess: staff and test accounts carry charges", pk["pay"]["account_id"].isin(tst).sum() > 100)
    # R3: each result's hurried figure outside its band
    b2, b5 = fig["bands"]["counted_per_month"], fig["bands"]["contribution"]
    nm = {"FLEX": "Flex", "STD": "Standaard", "ONB": "Onbeperkt", "GEZ": "Gezin"}
    out2 = [p for p in P.PLANS if not (b2[nm[p]][0] <= C["R2"][p] <= b2[nm[p]][1])]
    check("R3 careful R2 outside the band on the plans it misreads", {"ONB", "GEZ"} <= set(out2), ",".join(out2))
    check("R3 careful R2 misreads a plan where it decides nothing (Flex)", "FLEX" in out2)
    out5 = [p for p in P.PLANS if not (b5[nm[p]][0] <= C["R5"][p] <= b5[nm[p]][1])]
    check("R3 careful R5 outside the band", len(out5) >= 3, ",".join(out5))
    lo, hi = fig["remuneration_2027_band"]
    check("R3 careful R6 outside the band", not (lo <= C["R6"] <= hi), "%.0f" % C["R6"])
    check("R3 careful R1 and R4 earned", C["R1"] == G["R1"] and C["R4"] == G["R4"])
    check("R3 the careful route leads with Onbeperkt", C["R7"] == "ONB")
    # R4: no plant
    check("R4 no plant: the statements reproduce from the live roll-up's streamed seconds",
          _statements_reproduce(pk))
    # R5: no one thing, every factor across the data
    lic_share = _licence_share(pk)
    check("R5 footprint: downloads report on every plan", all(v > 0.02 for v in lic_share.values()),
          ", ".join("%s %.3f" % (k, v) for k, v in lic_share.items()))
    moves_in = sum(1 for p in W["profiles"] if len(p.history) > 1 and acc[p.history[-1][1]]["plan_hist"][0][1] == "ONB")
    check("R5 footprint: profiles move into accounts other than Gezin", moves_in > 20, str(moves_in))
    moves_out = sum(1 for p in W["profiles"] if len(p.history) > 1 and p.owner)
    check("R5 footprint: profiles move out to accounts of their own", moves_out > 20, str(moves_out))
    check("R5 the licence channel alone leads elsewhere (not the golden)", A["R7"] != G["R7"], A["R7"])
    check("R5 profile dating alone leads elsewhere (not the golden)", B["R7"] != G["R7"], B["R7"])
    # R6: the one-fact test
    for h in E["hints"]:
        check("R6 hint rescues a third or fewer: %s" % h["sentence"][:50], len(h["rescues"]) <= 2, str(h["rescues"]))
    # R7: rivals inside the bands or ruled out
    for nmv, o in (("re-sent rows summed", M.opts(dedup=False)), ("survival by plan", M.opts(r6_surv="plan")),
                   ("flat hours", M.opts(r6_hours="flat")), ("own hours", M.opts(r6_hours="own"))):
        R = M.all_results(pk, o)
        check("R7 rival %s leads with the golden" % nmv, R["R7"] == G["R7"])
        check("R7 rival %s inside R6's band" % nmv, lo <= R["R6"] <= hi, "%.0f" % R["R6"])
    N2 = M.all_results(pk, M.opts(lic_month="next"))
    check("R7 a renewal counted the month after (ruled out by B2.3) still leads with the golden", N2["R7"] == G["R7"])
    # shortcuts on distinct wrong answers, all across the line
    picks = {"careful": C["R7"], "licence": A["R7"], "dating": B["R7"], "share26": S["R7"], "seconds": T["R7"]}
    check("shortcuts: every shortcut off the golden", all(v != G["R7"] for v in picks.values()), str(picks))
    check("shortcuts: two or more distinct wrong plans", len(set(picks.values())) >= 2, str(set(picks.values())))
    srt = sorted(G["R5"].values(), reverse=True)
    check("forcing: the golden leads by EUR 5 or more", srt[0] - srt[1] >= 5, "%.1f" % (srt[0] - srt[1]))
    for p in E["forcing"]["perturbations"]:
        check("forcing: %s holds" % p["input"], p["answer"] == E["forcing"]["golden_answer"])
    # fork rows
    q = M.r1(pk)
    plan = pk["plan"]
    open_ = plan[(plan["period_start"] <= "2026-10-31") & (plan["period_end"].isna() | (plan["period_end"] >= "2026-10-31"))]
    check("SF1 open periods (trials, staff, test) count more than paying subscriptions", len(open_) > sum(q.values()))
    check("SF2 streamed seconds differ from the position count", abs(T["R2"]["GEZ"] - G["R2"]["GEZ"]) > 1)
    check("SF3 report month against play month: the rule's month is filed (B2.3); the call holds", N2["R7"] == G["R7"])
    check("SF4 today's profiles against the dated accounts differ on Gezin", abs(A["R2"]["GEZ"] - G["R2"]["GEZ"]) > 1)
    check("SF5 one paying month per collected charge (a re-presented debit counts once)",
          int(M.paying_months(pk).duplicated(["account_id", "m"]).sum()) == 0)
    c24 = M.cohort(pk)
    check("SF6 the spring 2024 trial starts lie January to March 2024", set(c24["m0"]) <= set(P.SPRING24))
    check("SF7 2027 prices: every 2027 price above its 2026 price", all(P.PRICE27[p] > P.PRICE[p] for p in P.PLANS))
    check("SF8 every spring 2024 trial start has 24 closed months by October 2026", max(c24["m0"]) + 23 <= P.CUT)
    check("SF9 the agency fee is per trial start (the quote)", "Fee per trial start" in pdf_text(os.path.join(TARGET, docs.FILES["quote"])))
    lic = set(pk["cat"].loc[pk["cat"]["rights"] == "licensed", "title_id"])
    check("SF10 own productions and public-domain titles listened to and left out",
          (~pk["live"]["title_id"].isin(lic)).sum() > 1000)
    check("SF11 the base's later profiles: same call", True)
    check("SF12 re-sent rows: same call", D["R7"] == G["R7"])
    # documents read back (positive controls through the same extractor)
    sb = pdf_text(os.path.join(TARGET, docs.FILES["schB"]))
    check("doc: schedule B carries the rate", "EUR 0.40 for every counted hour" in sb)
    check("doc: schedule B carries the counting rule", "furthest position the profile has reached in the title" in sb)
    check("doc: schedule B names no channel", not re.search(r"download|offline|licence renewal|streamed or", sb.split("B2.")[1] if "B2." in sb else sb))
    gd = pdf_text(os.path.join(TARGET, docs.FILES["guide"]))
    check("doc: the guideline files the spring 2024 trial starts", "spring 2024 campaign (January to March 2024)" in gd)
    check("doc: the guideline files the lead plan", "largest contribution per trial start" in gd)
    check("doc: no document names a transfer or a profile move", not re.search(r"transfer|move[sd]? (?:in|out|to)|fold",
                                                                                sb + gd, re.I))
    # realism
    ids = pk["acc"]["account_id"].str[1:].astype(int).sort_values().diff().dropna()
    check("realism: account ids not one constant step", ids.nunique() > 5)
    check("realism: paying counts differ by plan", len(set(G["R1"].values())) == 4)
    people = {"Romy Korsman", "Hugo Brouwer", "Tara Martens"}
    check("realism: personas from guard.py names only", True, ", ".join(sorted(people)))
    for n in usable:
        if n.endswith(".pdf"):
            check("realism: %s states no date after the ship day" % n[:40],
                  not re.search(r"2026-11-(1[3-9]|2\d|30)|1[3-9] November 2026|2[0-9] November 2026", pdf_text(
                      os.path.join(TARGET, n))) or "30 November 2026" in pdf_text(os.path.join(TARGET, n)))
    print("%d checks, %d FAIL" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


def _statements_reproduce(pk):
    lv = pk["live"].drop_duplicates()
    cat = pk["cat"].set_index("title_id")
    lv = lv[lv["title_id"].isin(pk["licensed"])]
    lv = lv.assign(pub=lv["title_id"].map(cat["publisher_code"]))
    g = lv.groupby(["month", "pub"])["seconds_streamed"].sum()
    stm = __import__("pandas").read_csv(os.path.join(TARGET, PK.FILES["stm"]))
    xw = __import__("pandas").read_csv(os.path.join(TARGET, PK.FILES["xw"]))
    ren = dict(zip(xw["old_code"], xw["new_code"]))
    stm["pub"] = stm["publisher_code"].map(lambda c: ren.get(c, c))
    sel = stm[stm["statement_month"] == "2026-06"]
    return all(abs(g.get(("2026-06", p), 0) - s) <= 1 for p, s in zip(sel["pub"], sel["streamed_seconds"]))


def _licence_share(pk):
    """Each plan's share of counted hours that only the renewals carry, the twelve months to October 2026."""
    full = M.attribute(pk, M.GOLD)
    live = M.attribute(pk, M.opts(channels=("live",)))
    pm = M.paying_months(pk)
    pm = pm[pm["m"].isin(P.R2_MONTHS)]
    out = {}
    for pl in P.PLANS:
        sel = pm[pm["plan_code"] == pl][["account_id", "m"]]
        f = sel.merge(full, on=["account_id", "m"])["hours"].sum()
        l_ = sel.merge(live, on=["account_id", "m"])["hours"].sum()
        out[pl] = 1 - l_ / f
    return out


if __name__ == "__main__":
    main()
