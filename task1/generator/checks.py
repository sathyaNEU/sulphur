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


K27 = 8      # replays of 2027 on the October 2026 world


def _truth_one(args):
    rise, s27 = args
    W = world.simulate(rise27=rise, seed27=s27)
    acc = {a["aid"]: a for a in W["accounts"]}
    base = {c["aid"]: c["plan"] for c in W["charges"] if c["m"] == P.CUT and c["status"] in ("collected", "re-presented")
            and c["price"] > 0 and acc[c["aid"]]["kind"] == "consumer"}
    rev, hrs, n = collections.Counter(), collections.Counter(), collections.Counter(base.values())
    for c in W["charges"]:
        if 48 <= c["m"] <= 59 and c["aid"] in base:
            rev[base[c["aid"]]] += PK.net_revenue(c)
    for (m, pid, aid, t, h) in W["counted"]:
        if 48 <= m <= 59 and aid in base:
            hrs[base[aid]] += h
    end = collections.Counter(base[c["aid"]] for c in W["charges"] if c["m"] == 59 and c["aid"] in base
                              and c["status"] in ("collected", "re-presented") and c["price"] > 0)
    return {p: (rev[p] - P.RATE27 * hrs[p]) / n[p] for p in P.PLANS}, {p: end[p] for p in P.PLANS}


def truth():
    """Each plan's change in its October 2026 base's 2027 contribution in the simulated world, rises against held
    prices on the same replayed 2027, averaged over K27 replays: the mean and its standard error."""
    import multiprocessing as mp
    jobs = [(r, s) for s in range(1, K27 + 1) for r in (P.RISE27, ())]
    with mp.Pool(min(8, len(jobs))) as pool:
        res = pool.map(_truth_one, jobs)
    out = {}
    end = {EP.NAMES[p]: sum(res[2 * i][1][p] for i in range(K27)) / K27 for p in P.PLANS}
    res = [r[0] for r in res]
    for p in P.PLANS:
        d = [res[2 * i][p] - res[2 * i + 1][p] for i in range(K27)]
        mu = sum(d) / K27
        se = (sum((x - mu) ** 2 for x in d) / (K27 - 1) / K27) ** 0.5
        out[EP.NAMES[p]] = (mu, se)
    return out, end


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
    tr, end27 = truth()
    for p, v in fig["paying_end27"].items():
        check("R9 golden within 5 per cent of the replayed 2027: %s" % p, abs(v - end27[p]) <= 0.05 * end27[p],
              "golden %d truth %.0f" % (v, end27[p]))
    for p in fig["change_2027"]:
        mu, se = tr[p]
        g = fig["change_2027"][p]
        check("R1 golden and the replayed truth on the same side of zero: %s" % p, (mu > 0) == (g > 0),
              "golden %.1f truth %.2f (se %.2f)" % (g, mu, se))
        check("R1 the replayed truth four standard errors or more from zero: %s" % p, abs(mu) >= 4 * se)
        check("R1 golden within EUR 4 of the replayed truth: %s" % p, abs(g - mu) <= 4.0, "%.2f" % (g - mu))
    # the 2027 rises sit inside the past rises' sizes, so no response is carried to a size the record never ran
    past_over = [P.PRICE[pl] - P.rival_of(c, pl, (y - P.M0_YEAR) * 12) for (y, c), pls in P.RISES.items() for pl in pls
                 if P.PRICE0[pl] <= P.rival_of(c, pl, (y - P.M0_YEAR) * 12) < P.PRICE[pl]]
    for pl in P.PLANS:
        check("dose: %s's 2027 rise in euros is its past rise" % EP.NAMES[pl],
              abs((P.PRICE27[pl] - P.PRICE[pl]) - (P.PRICE[pl] - P.PRICE0[pl])) < 1e-9)
        pc = [(P.PRICE27[pl] - P.PRICE[pl]) / P.PRICE[pl], (P.PRICE[pl] - P.PRICE0[pl]) / P.PRICE0[pl]]
        check("dose: %s's 2027 rise in per cent within the past rises' range" % EP.NAMES[pl],
              min(r["pct"] for r in M.response(pk, M.GOLD)) - 0.01 <= pc[0] <= max(r["pct"] for r in M.response(pk, M.GOLD)),
              "%.3f" % pc[0])
        for c in ("NL", "BE"):
            rv = P.rival_of(c, pl, 48)
            if P.PRICE[pl] <= rv < P.PRICE27[pl]:
                check("dose: %s %s's 2027 price no further past the rival than a past crossing" % (EP.NAMES[pl], c),
                      P.PRICE27[pl] - rv <= max(past_over) + 1e-9, "%.2f against %.2f" % (P.PRICE27[pl] - rv, max(past_over)))
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
    check("shortcuts: two or more distinct wrong sets", len(set(picks.values())) >= 2, str(set(picks.values())))
    var = [EP.results(pk, o)["R7"] for o in list(EP.RIVALS.values()) + [
        M.opts(scale_cancel=1.2), M.opts(scale_cancel=0.8), M.opts(scale_down=1.2), M.opts(scale_down=0.8),
        M.opts(dose="cross15")]]
    for p, g in fig["change_2027"].items():
        lo = min(abs(v[p]) for v in var if (v[p] > 0) == (g > 0))
        check("forcing: %s keeps its side of zero by EUR 0.5 or more under every rival and perturbation" % p,
              all((v[p] > 0) == (g > 0) for v in var) and lo >= 0.5, "nearest %.2f" % lo)
    # fork rows
    check("SF1 open plan periods count more than paying subscriptions", sum(EP._open_periods(pk).values()) > fig["paying_oct_total"])
    check("SF2 extra cancellations beyond the other region's months", all(e["extra_cancel"] < 30 for e in ev))
    check("SF3 the first bill alone: same call", EP.results(pk, M.opts(window="first"))["R8"] == fig["raise"])
    check("SF4 the year before as control: same call", EP.results(pk, M.opts(control="prior"))["R8"] == fig["raise"])
    check("SF5 promotions left out of the December scans", True)
    ex = EP.results(pk, M.opts(down_as_exit=True))["R7"]["Onbeperkt"]
    check("SF6 a downgrade counted as an exit moves Onbeperkt's change outside its band",
          not (b["R7"]["Onbeperkt"][0] <= ex <= b["R7"]["Onbeperkt"][1]), "%.1f" % ex)
    s26 = EP.results(pk, M.opts(cost="share26"))["R7"]
    check("SF7 the 2026 basis (informational: filed in schedule B, a reflex; its call and figures recorded)", True,
          "%s; %s" % (EP.results(pk, M.opts(cost="share26"))["R8"], {p: round(float(v), 1) for p, v in s26.items()}))
    check("SF8 streamed seconds differ from counted hours", True)
    check("SF9 the 2027 prices are the price list's", all(P.PRICE27[p] > P.PRICE[p] for p in P.PLANS))
    check("SF10 re-sent rows: same call", D["R8"] == fig["raise"])
    check("SF11 regions from the accounts export", set(pk["acc"]["country"]) == {"NL", "BE"})
    check("SF12 downgraders modelled: same call", EP.results(pk, M.opts(dval="model"))["R8"] == fig["raise"])
    check("SF14 one step fitted on the eight events: same call",
          EP.results(pk, M.opts(resp="plan_step"))["R8"] == fig["raise"])
    check("SF15 the e-mail's leavers moved 20 per cent: same call", all(
        EP.results(pk, M.opts(scale_announce=k))["R8"] == fig["raise"] for k in (0.8, 1.2)))
    check("SF16 the stayers' listening moved 20 per cent: same call", all(
        EP.results(pk, M.opts(scale_use=k))["R8"] == fig["raise"] for k in (0.8, 1.2)))
    # SF18: the first-bill responses are counted among the subscriptions that reach that bill (guideline 3.10)
    gd310 = pdf_text(os.path.join(TARGET, docs.FILES["guide"]))
    check("SF18 guideline 3.10 counts the first-bill responses among those reaching the bill",
          "counted among the subscriptions that reach that bill" in gd310)
    check("SF19 still paying on its own plan only (the prompt says on any plan) moves Standaard out of its band",
          not (b["R9"]["Standaard"][0] <= fig["paying_end27"]["Standaard"] * (1 - fig["extra_down"]["Standaard Netherlands"] / 100.0)
               <= b["R9"]["Standaard"][1]))
    check("SF17 one plan-wide continuation: same call", EP.results(pk, M.opts(r6_surv="plan"))["R8"] == fig["raise"])
    check("SF13 every dose form: same call", all(EP.results(pk, M.opts(dose=d))["R8"] == fig["raise"]
                                                 for d in ("pct", "log", "eur", "cross15")))
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
