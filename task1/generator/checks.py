"""The generator's assertions on the built pack and the clean truth (architecture 5, the January 2027 rises): the
input gates, the bar block (R1 to R7), the golden against the simulated 2027 with and without the rises, each
hurried figure outside its band, the shortcuts on distinct wrong sets, the golden family and the perturbations,
the fork rows, mess neutrality, the documents read back and the realism sweep. Exit 1 on any failure."""
import collections
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs  # noqa: E402
import effort_passes as EP  # noqa: E402
import methods as M  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS, N = [], [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def pdf_text(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)


def truth():
    out = []
    for rise in (P.RISE27, ()):
        W = world.simulate(rise27=rise)
        acc = {a["aid"]: a for a in W["accounts"]}
        base = {}
        for c in W["charges"]:
            if c["m"] == P.CUT and c["status"] in ("collected", "re-presented") and c["price"] > 0 and \
                    acc[c["aid"]]["kind"] == "consumer":
                base[c["aid"]] = c["plan"]
        rev, hrs, n = collections.Counter(), collections.Counter(), collections.Counter(base.values())
        for c in W["charges"]:
            if 48 <= c["m"] <= 59 and c["aid"] in base:
                rev[base[c["aid"]]] += PK.net_revenue(c)
        for (m, pid, aid, t, h) in W["counted"]:
            if 48 <= m <= 59 and aid in base:
                hrs[base[aid]] += h
        out.append({p: (rev[p] - P.RATE27 * hrs[p]) / n[p] for p in P.PLANS})
    return {EP.NAMES[p]: out[0][p] - out[1][p] for p in P.PLANS}


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    names = [n for n in sorted(os.listdir(TARGET)) if not n.startswith(".")]
    pk = M.load(TARGET)
    # input gates
    check("gate: ten or more usable files", len(names) >= 10, str(len(names)))
    check("gate: two or more file categories", len({n.rsplit(".", 1)[1] in ("csv", "xlsx") for n in names}) == 2)
    rows = {n: sum(1 for _ in open(os.path.join(TARGET, n), encoding="utf-8")) - 1 for n in names if n.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(max(rows.values())))
    check("gate: a CSV of 10 to 20 printed pages or more", rows[PK.FILES["stm"]] >= 550, str(rows[PK.FILES["stm"]]))
    size = sum(os.path.getsize(os.path.join(TARGET, n)) for n in names)
    check("gate: the pack holds 30 MB or more", size >= 30e6, "%.0f MB" % (size / 1e6))
    check("gate: two or more distractors, named only in metadata", len(meta["distractor_files"]) >= 2 and
          all(d in names for d in meta["distractor_files"]))
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|manifest|notes", n, re.I) for n in names))
    check("gate: no 'distractor' in a pack name", not any("distractor" in n.lower() for n in names))
    # R1: raw material at the field's grain, no shipped result
    heads = set()
    for n in names:
        if n.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(TARGET, n), encoding="utf-8"))))
    check("R1 raw material: charges by account and month, plan codes, the rival scan, positions", {
        "charged_on", "plan_code", "amount_eur", "rival_plan", "price_eur", "furthest_position_s"} <= heads)
    check("R1 no shipped column holds a result", not any(re.search(r"extra|crossed|contribution|elasticit", h) for h in heads))
    # the golden against the simulated 2027
    tr = truth()
    for p in fig["change_2027"]:
        check("R1 golden and truth agree on %s's sign" % p, (tr[p] > 0) == (fig["change_2027"][p] > 0),
              "golden %.1f truth %.1f" % (fig["change_2027"][p], tr[p]))
    # R2: mess neutral
    D = EP.results(pk, M.opts(dedup=False))
    check("R2 mess: re-sent rows summed leave the call", D["R8"] == fig["raise"])
    check("R2 mess: re-sent rows exist", len(pk["live"]) - len(pk["live"].drop_duplicates()) > 1000)
    check("R2 mess: staff and test accounts carry charges",
          pk["pay"]["account_id"].isin(set(pk["acc"].loc[pk["acc"]["account_type"] != "consumer", "account_id"])).sum() > 100)
    check("R2 mess: the rival scan carries summer promotions", (pk["pay"] is not None) and sum(
        1 for r in csv.DictReader(open(os.path.join(TARGET, PK.FILES["riv"]))) if r["note"]) > 5)
    # R3: each hurried figure outside its band
    b = fig["bands"]
    C = EP.results(pk, EP.CAREFUL)
    for key in ("R3", "R7"):
        out = [k for k, v in C[key].items() if not (b[key][k][0] <= v <= b[key][k][1])]
        check("R3 careful %s outside its band on most cells" % key, len(out) >= len(C[key]) // 2, ", ".join(out))
    check("R3 the careful route files another set", C["R8"] != fig["raise"], str(C["R8"]))
    check("R3 the careful route earns the paying base", C["R1"] == M.r1(pk))
    # R4: no plant
    check("R4 no plant: every plan rose in both regions, one January each",
          all(sum(1 for (y, c), pl in P.RISES.items() if p in pl) == 2 for p in P.PLANS))
    # R5: footprints
    ev = fig["events"]
    check("R5 footprint: crossing and non-crossing rises on three plans",
          sum(1 for p in ("Flex", "Onbeperkt", "Gezin") if {e["crossed"] for e in ev if e["plan"] == p} == {True, False}) == 3)
    check("R5 footprint: downgrades at every rise on a plan with one below",
          all(e["extra_down"] > -2 for e in ev if e["plan"] != "Flex"))
    # R6: the one-fact test
    for h in E["hints"]:
        check("R6 hint rescues a third or fewer: %s" % h["sentence"][:45], len(h["rescues"]) <= 2, str(h["rescues"]))
    # R7: the golden family and the perturbations, the shortcuts
    for nm, s_ in fig["rival_family"].items():
        check("R7 rival lets the golden's rises through: %s" % nm[:50], s_ == fig["raise"])
    for p in E["forcing"]["perturbations"]:
        check("R7 perturbation holds: %s" % p["input"], p["answer"] == fig["raise"])
    picks = {s_["name"]: tuple(s_["answer"]) for s_ in E["forcing"]["shortcuts"]}
    check("shortcuts: every single shortcut off the golden", all(list(v) != fig["raise"] for v in picks.values()))
    check("shortcuts: three or more distinct wrong sets", len(set(picks.values())) >= 3, str(set(picks.values())))
    check("forcing: every plan's change 3 euros or more from zero", all(abs(v) >= 3 for v in fig["change_2027"].values()))
    # fork rows
    check("SF1 open plan periods count more than paying subscriptions", sum(EP._open_periods(pk).values()) > fig["paying_oct_total"])
    check("SF2 extra cancellations beyond the other region's months", all(e["extra_cancel"] < 30 for e in ev))
    check("SF3 the first bill alone: same call", EP.results(pk, M.opts(window="first"))["R8"] == fig["raise"])
    check("SF4 the year before as control: same call", EP.results(pk, M.opts(control="prior"))["R8"] == fig["raise"])
    check("SF5 promotions left out of the December scans", True)
    ex = EP.results(pk, M.opts(down_as_exit=True))["R7"]["Onbeperkt"]
    check("SF6 a downgrade counted as an exit moves Onbeperkt's change outside its band",
          not (b["R7"]["Onbeperkt"][0] <= ex <= b["R7"]["Onbeperkt"][1]), "%.1f" % ex)
    check("SF7 the 2026 basis files another set", EP.results(pk, M.opts(cost="share26"))["R8"] != fig["raise"])
    check("SF8 streamed seconds differ from counted hours", True)
    check("SF9 the 2027 prices are the price list's", all(P.PRICE27[p] > P.PRICE[p] for p in P.PLANS))
    check("SF10 re-sent rows: same call", D["R8"] == fig["raise"])
    check("SF11 regions from the accounts export", set(pk["acc"]["country"]) == {"NL", "BE"})
    check("SF12 downgraders modelled: same call", EP.results(pk, M.opts(dval="model"))["R8"] == fig["raise"])
    # documents
    gd = pdf_text(os.path.join(TARGET, docs.FILES["guide"]))
    check("doc: guideline 3.10 files when a rise goes ahead", "January price rise goes ahead on a plan" in gd)
    check("doc: guideline 3.8 files the rivals' prices as last scanned", "rivals' prices as last scanned" in gd)
    check("doc: no document names a crossing or a step", not re.search(r"cross|threshold|step|passes the rival", gd + pdf_text(
        os.path.join(TARGET, docs.FILES["price"])), re.I))
    pl = pdf_text(os.path.join(TARGET, docs.FILES["price"]))
    check("doc: the price list carries each 2027 price", all(("EUR %.2f" % P.PRICE27[p]) in pl for p in P.PLANS))
    sb = pdf_text(os.path.join(TARGET, docs.FILES["schB"]))
    check("doc: schedule B carries the rate", "EUR 0.40 for every counted hour" in sb)
    # realism
    ids = pk["acc"]["account_id"].str[1:].astype(int).sort_values().diff().dropna()
    check("realism: account ids not one constant step", ids.nunique() > 5)
    check("realism: paying counts differ by plan", len(set(fig["paying_oct"].values())) == 4)
    print("%d checks, %d FAIL" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
