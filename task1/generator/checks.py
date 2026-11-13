"""The generator's assertions on the built pack and the clean truth (architecture 5 as repaired on 2026-11-13: the
January 2027 rises with the stops that come back and the stayers' listening): the input gates, the bar block (R1 to
R7), every graded figure against the simulated 2027 replayed with and without the rises, each judgment's weight in
the world itself, the stump factorial, the golden family and the perturbations on the golden's side and the shortcuts
across it, the fork rows, mess neutrality, the documents read back and the realism sweep. Exit 1 on any failure."""
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
K27 = 8      # replays of 2027 on the October 2026 world
LOWER = {"STD": "FLEX", "ONB": "STD", "GEZ": "ONB"}


def check(name, ok, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def pdf_text(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)


def _summary(kw):
    W = world.simulate(**kw)
    acc = {a["aid"]: a for a in W["accounts"]}
    pay = collections.defaultdict(dict)
    for c in W["charges"]:
        if c["status"] in ("collected", "re-presented") and c["price"] > 0 and acc[c["aid"]]["kind"] == "consumer":
            pay[c["m"]][c["aid"]] = c["plan"]
    base = dict(pay[P.CUT])
    rev, hrs, hacc = collections.Counter(), collections.Counter(), collections.Counter()
    for c in W["charges"]:
        if P.Y2027[0] <= c["m"] <= P.END and c["aid"] in base:
            rev[base[c["aid"]]] += PK.net_revenue(c)
    for (m, pid, aid, t, h) in W["counted"]:
        if P.Y2027[0] <= m <= P.END and aid in base:
            hrs[base[aid]] += h
            hacc[aid] += h
    cty = {a: acc[a]["country"] for a in base}
    return {"pay": {m: dict(v) for m, v in pay.items() if m >= P.CUT}, "base": base, "rev": dict(rev),
            "hrs": dict(hrs), "hacc": dict(hacc), "cty": cty}


def _truth_seed(s27):
    """One replay of 2027 on the October 2026 world: with the rises, with the 2026 prices held, with the rises but no
    extra listening after them, and both without returns after a stop from November 2026."""
    S = {nm: _summary(dict(kw, seed27=s27)) for nm, kw in (
        ("rise", dict(rise27=P.RISE27)), ("hold", dict(rise27=())), ("rise_nosal", dict(rise27=P.RISE27, sal_off27=True)),
        ("rise_noret", dict(rise27=P.RISE27, ret_off27=True)), ("hold_noret", dict(rise27=(), ret_off27=True)))}
    R, H, NS = S["rise"], S["hold"], S["rise_nosal"]
    base, cty = R["base"], R["cty"]
    n = collections.Counter(base.values())
    out = {}
    for pl in P.PLANS:
        contrib = lambda X: X["rev"].get(pl, 0.0) - P.RATE27 * X["hrs"].get(pl, 0.0)
        d = {"change": (contrib(R) - contrib(H)) / n[pl],
             "change_noret": (contrib(S["rise_noret"]) - contrib(S["hold_noret"])) / n[pl],
             "change_nosal": (contrib(NS) - contrib(H)) / n[pl],
             "end27": sum(1 for a in R["pay"][P.END] if base.get(a) == pl),
             "remun": P.RATE27 * R["hrs"].get(pl, 0.0) / n[pl]}
        for c in ("NL", "BE"):
            def rates(X):
                ids = [a for a, p in X["pay"][P.CUT + 2].items() if p == pl and cty.get(a) == c]
                left = sum(1 for a in ids if a not in X["pay"][P.CUT + 3]) / len(ids)
                down = sum(1 for a in ids if pl in LOWER and X["pay"][P.CUT + 3].get(a) == LOWER[pl]) / len(ids)
                return left, down
            r_, h_ = rates(R), rates(H)
            d["xc_" + c], d["xd_" + c] = 100 * (r_[0] - h_[0]), 100 * (r_[1] - h_[1])
        stop = back = 0
        for a, p in base.items():
            if p == pl and any(a in R["pay"][m - 1] and a not in R["pay"][m] for m in range(P.CUT + 1, P.END + 1)):
                stop += 1
                back += a in R["pay"][P.END]
        d["back"] = 100 * back / max(stop, 1)
        stay = [a for a, p in base.items() if p == pl and all(R["pay"][m].get(a) == pl and NS["pay"][m].get(a) == pl
                                                               for m in P.Y2027)]
        d["sal"] = sum(R["hacc"].get(a, 0.0) - NS["hacc"].get(a, 0.0) for a in stay) / max(len(stay), 1)
        out[EP.NAMES[pl]] = d
    return out


def truth():
    import multiprocessing as mp
    with mp.Pool(min(K27, 8)) as pool:
        res = pool.map(_truth_seed, list(range(1, K27 + 1)))
    agg = {}
    for p in res[0]:
        agg[p] = {}
        for k in res[0][p]:
            v = [r[p][k] for r in res]
            mu = sum(v) / len(v)
            se = (sum((x - mu) ** 2 for x in v) / (len(v) - 1) / len(v)) ** 0.5
            agg[p][k] = (mu, se)
    return agg


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    names = [n for n in sorted(os.listdir(TARGET)) if not n.startswith(".")]
    pk = M.load(TARGET)
    b = fig["bands"]
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
    check("R1 raw material: charges by account and month, plan periods with end reasons, the rival scan, positions", {
        "charged_on", "plan_code", "amount_eur", "end_reason", "rival_plan", "price_eur", "furthest_position_s"} <= heads)
    check("R1 no shipped column holds a result", not any(re.search(r"extra|crossed|contribution|elasticit|reactivat|"
                                                             r"return_rate|uplift", h) for h in heads))
    # every graded figure against the replayed 2027
    tr = truth()
    for p in EP.NAMES.values():
        t = tr[p]
        mu, se = t["change"]
        g = fig["change_2027"][p]
        check("R7 golden and the replayed truth on the same side of zero: %s" % p, (mu > 0) == (g > 0),
              "golden %.1f truth %.2f (se %.2f)" % (g, mu, se))
        check("R7 the replayed truth four standard errors or more from zero: %s" % p, abs(mu) >= 4 * se)
        check("R7 golden within EUR 3.5 of the replayed truth: %s" % p, abs(g - mu) <= 3.5, "%.2f" % (g - mu))
        check("R9 golden within 10 per cent of the replayed truth: %s" % p,
              abs(fig["paying_end27"][p] - t["end27"][0]) <= 0.10 * t["end27"][0],
              "golden %d truth %.0f" % (fig["paying_end27"][p], t["end27"][0]))
        check("R2 golden within 12 per cent of the replayed truth: %s" % p,
              abs(fig["remun_2027"][p] - t["remun"][0]) <= 0.12 * t["remun"][0],
              "golden %.1f truth %.1f" % (fig["remun_2027"][p], t["remun"][0]))
        check("R5 golden within 9 per 100 of the replayed truth: %s" % p, abs(fig["back_share"][p] - t["back"][0]) <= 9,
              "golden %.1f truth %.1f" % (fig["back_share"][p], t["back"][0]))
        check("R6 golden within 15 hours or 60 per cent of the replayed truth: %s" % p,
              abs(fig["sal_hours"][p] - t["sal"][0]) <= max(15.0, 0.6 * t["sal"][0]),
              "golden %.1f truth %.1f" % (fig["sal_hours"][p], t["sal"][0]))
        for c, r in (("NL", "Netherlands"), ("BE", "Flanders")):
            k = "%s %s" % (p, r)
            check("R3 golden within 3.5 per 100 of the replayed truth: %s" % k,
                  abs(fig["extra_cancel"][k] - t["xc_" + c][0]) <= 3.5,
                  "golden %.1f truth %.1f" % (fig["extra_cancel"][k], t["xc_" + c][0]))
            if k in fig["extra_down"]:
                check("R4 golden within 2 per 100 of the replayed truth: %s" % k,
                      abs(fig["extra_down"][k] - t["xd_" + c][0]) <= 2.0,
                      "golden %.1f truth %.1f" % (fig["extra_down"][k], t["xd_" + c][0]))
    # each judgment carries weight in the world itself, not only in the golden's model
    check("world: without returns after a stop Standaard's rise loses", tr["Standaard"]["change_noret"][0] < 0,
          "%.2f" % tr["Standaard"]["change_noret"][0])
    check("world: without the stayers' extra listening Onbeperkt's rise gains", tr["Onbeperkt"]["change_nosal"][0] > 0,
          "%.2f" % tr["Onbeperkt"]["change_nosal"][0])
    # the 2027 rises sit inside the record: each plan's 2027 rise in euros is its past rise, and each 2027 cell has a
    # past rise of its own plan of the same kind (passing the rival's price or not)
    rows_ = M.response(pk, M.GOLD)
    for pl in P.PLANS:
        check("dose: %s's 2027 rise in euros is its past rise" % EP.NAMES[pl],
              abs((P.PRICE27[pl] - P.PRICE[pl]) - (P.PRICE[pl] - P.PRICE0[pl])) < 1e-9)
        for c in ("NL", "BE"):
            cross = P.PRICE[pl] <= pk["rival"][(2027, c, pl)] < P.PRICE27[pl]
            check("support: %s %s's 2027 kind (%s) is one its own past rises ran" % (EP.NAMES[pl], c,
                                                                                    "past" if cross else "not past"),
                  any(r["plan"] == pl and r["cross"] == cross for r in rows_))
    check("support: Standaard never passes the rival's Plus 30 uur", not any(r["cross"] for r in rows_ if r["plan"] == "STD")
          and not any(P.PRICE["STD"] <= pk["rival"][(2027, c, "STD")] < P.PRICE27["STD"] for c in ("NL", "BE")))
    # R2: mess neutral
    D = EP.results(pk, M.opts(dedup=False))
    check("R2 mess: re-sent rows summed leave the call", D["R8"] == fig["raise"])
    check("R2 mess: re-sent rows exist", len(pk["live"]) - len(pk["live"].drop_duplicates()) > 1000)
    check("R2 mess: staff and test accounts carry charges",
          pk["pay"]["account_id"].isin(set(pk["acc"].loc[pk["acc"]["account_type"] != "consumer", "account_id"])).sum() > 100)
    check("R2 mess: the rival scan carries summer promotions", sum(
        1 for r in csv.DictReader(open(os.path.join(TARGET, PK.FILES["riv"]))) if r["note"]) > 5)
    # R3: each hurried figure outside its band
    C = EP.results(pk, EP.CAREFUL)
    for key in ("R2", "R5", "R6", "R7", "R9"):
        out = [k for k, v in C[key].items() if not (b[key][k][0] <= v <= b[key][k][1])]
        check("R3 careful %s outside its band on most cells" % key, len(out) >= max(1, len(C[key]) // 2), ", ".join(out))
    check("R3 the careful route files another set", C["R8"] != fig["raise"], str(C["R8"]))
    check("R3 the careful route earns the paying base", C["R1"] == M.r1(pk))
    # R4: no plant: every plan rose once in each region, the returns and the listening run on every plan
    check("R4 no plant: every plan rose in both regions, one January each",
          all(sum(1 for (y, c), pl in P.RISES.items() if p in pl) == 2 for p in P.PLANS))
    lap = M.lapses(pk, M.GOLD)
    back_by_plan = collections.Counter(pl for (a, f_, nxt, bb, why, pl) in lap if nxt is not None)
    check("R4 no plant: stops come back on every plan", all(back_by_plan[p] > 100 for p in P.PLANS), str(dict(back_by_plan)))
    path, obs, tau = M.salience(pk, M.GOLD)
    check("R4 no plant: the stayers' first-month listening rises on every plan",
          all(obs[p][0][1] > 0 for p in P.PLANS), str({p: round(obs[p][0][1], 3) for p in P.PLANS}))
    # R5: footprints
    ev = fig["events"]
    check("R5 footprint: past rises that passed the rival and rises that did not (Onbeperkt's and Gezin's one of each, "
          "both of Flex's past it, neither of Standaard's)",
          all({e["crossed"] for e in ev if e["plan"] == p} == {True, False} for p in ("Onbeperkt", "Gezin")) and
          all(e["crossed"] for e in ev if e["plan"] == "Flex") and not any(e["crossed"] for e in ev if e["plan"] == "Standaard"))
    check("R5 footprint: the lightest stops come back more often than the heaviest",
          fig["back12_by_band"]["under 3"] > fig["back12_by_band"]["20 and more"] + 10)
    # R6: the one-fact test
    for h in E["hints"]:
        check("R6 hint rescues a third or fewer: %s" % h["sentence"][:45], len(h["rescues"]) <= 3, str(h["rescues"]))
    # R7: the factorial, the golden family and the perturbations, the shortcuts
    st = [j for j in E["factorial"]["judgments"] if j["kind"] == "stump"]
    check("factorial: two or more stumps", len(st) >= 2, str(len(st)))
    for j in st:
        check("factorial: %s necessary (dropped alone, the call moves)" % j["id"], j["dropped"]["answer"] != fig["raise"],
              str(j["dropped"]["answer"]))
        check("factorial: %s not sufficient (fixed alone, the call stays wrong)" % j["id"],
              j["alone"]["answer"] != fig["raise"], str(j["alone"]["answer"]))
    check("factorial: the single drops land on distinct wrong sets", len({tuple(j["dropped"]["answer"]) for j in st}) == len(st))
    for nm, s_ in fig["rival_family"].items():
        check("R7 rival lets the golden's rises through: %s" % nm[:60], s_ == fig["raise"])
    for p in E["forcing"]["perturbations"]:
        check("R7 perturbation holds: %s" % p["input"], p["answer"] == fig["raise"])
    picks = {s_["name"]: tuple(s_["answer"]) for s_ in E["forcing"]["shortcuts"]}
    check("shortcuts: every single shortcut off the golden", all(list(v) != fig["raise"] for v in picks.values()))
    check("shortcuts: three or more distinct wrong sets", len(set(picks.values())) >= 3, str(set(picks.values())))
    for s_ in E["forcing"]["closed_supporting"]:
        check("closed lesson as a supporting step leaves the call: %s" % s_["name"][:60], s_["answer"] == fig["raise"])
    var = [EP.results(pk, o)["R7"] for o in list(EP.RIVALS.values())] + [
        EP.results(pk, M.opts(**{k: v})) ["R7"] for k in ("scale_cancel", "scale_down", "scale_announce", "scale_sal",
                                                           "scale_ret") for v in (0.8, 1.2)]
    for p, g in fig["change_2027"].items():
        lo = min(abs(v[p]) for v in var if (v[p] > 0) == (g > 0))
        check("forcing: %s keeps its side of zero by EUR 0.8 or more under every rival and perturbation" % p,
              all((v[p] > 0) == (g > 0) for v in var) and lo >= 0.8, "nearest %.2f" % lo)
    # fork rows
    check("SF1 open plan periods count more than paying subscriptions", sum(EP._open_periods(pk).values()) > fig["paying_oct_total"])
    check("SF3 the January and February bills as the window: same call", EP.results(pk, M.opts(window="two"))["R8"] == fig["raise"])
    check("SF4 the year before as control: same call", EP.results(pk, M.opts(control="prior"))["R8"] == fig["raise"])
    ex = EP.results(pk, M.opts(down_as_exit=True))
    check("SF6 a downgrade counted as an exit (the base followed through 2027 keeps a downgrader paying): same call",
          ex["R8"] == fig["raise"], "%s, Standaard %.1f" % (ex["R8"], ex["R7"]["Standaard"]))
    s26 = EP.results(pk, M.opts(cost="share26"))
    check("SF7 the 2026 basis (informational: schedule B files the rate, a reflex)", True,
          "%s; %s" % (s26["R8"], {p: round(float(v), 1) for p, v in s26["R7"].items()}))
    check("SF10 re-sent rows: same call", D["R8"] == fig["raise"])
    check("SF11 regions from the accounts export", set(pk["acc"]["country"]) == {"NL", "BE"})
    check("SF12 downgraders modelled on their own hours: same call", EP.results(pk, M.opts(dval="model"))["R8"] == fig["raise"])
    check("SF13 the log dose: same call", EP.results(pk, M.opts(dose="log"))["R8"] == fig["raise"])
    check("SF14 each plan's own rises of the same kind: same call", EP.results(pk, M.opts(resp="kind"))["R8"] == fig["raise"])
    same = True
    for (y, cc, pl) in M.RISE_EVENTS:
        rv = pk["rival"][(y, cc, pl)]
        same &= (P.PRICE0[pl] <= rv < P.PRICE[pl]) == (P.PRICE[pl] > rv)
    for pl in P.PLANS:
        for cc in ("NL", "BE"):
            rv = pk["rival"][(2027, cc, pl)]
            same &= (P.PRICE[pl] <= rv < P.PRICE27[pl]) == (P.PRICE27[pl] > rv)
    check("SF20 passing the rival reads the same as crossing from at or below it and as ending above it, for every past "
          "rise and every 2027 cell (no plan is above the rival before any rise)", same)
    gd310 = pdf_text(os.path.join(TARGET, docs.FILES["guide"]))
    check("SF18 guideline 3.10 counts the first-bill responses among those reaching the bill",
          "counted among the subscriptions that reach that bill" in gd310)
    check("SF19 paying on any plan at the end of 2027 counts a subscription that stopped and paid again",
          fig["paying_end27"]["Flex"] > fig["careful"]["paying_end27"]["Flex"] + 100,
          "%d against %d without returns" % (fig["paying_end27"]["Flex"], fig["careful"]["paying_end27"]["Flex"]))
    pl_txt = pdf_text(os.path.join(TARGET, docs.FILES["price"]))
    check("SF21 a returned subscription pays the price then in force (the price list moves existing subscriptions at "
          "their first 2027 billing date)", "first billing date in 2027" in pl_txt)
    check("SF2 a rise's extra cancellations read beyond the other region over the same months (3.10)",
          "beyond what the same months would have brought without the rise" in gd310 and
          all(abs(e["extra_cancel"]) < 35 for e in ev))
    rv_rows = list(csv.DictReader(open(os.path.join(TARGET, PK.FILES["riv"]))))
    check("SF5 the rival's prices from the scan, promotions out; for 2027 the October 2026 scan (3.8)",
          pk["rival"][(2027, "NL", "FLEX")] == 10.29 and all(pk["rival"][k] > 5 for k in pk["rival"]) and
          any(r["note"] for r in rv_rows))
    ch_pos = M.r2(pk, M.GOLD)
    ch_sec = M.r2(pk, M.opts(basis="seconds"))
    check("SF8 counted hours from positions across every report differ from streamed seconds (schedule B 2.2)",
          all(abs(ch_pos[p] - ch_sec[p]) > 0.2 for p in P.PLANS), str({p: (round(ch_pos[p], 2), round(ch_sec[p], 2))
                                                                        for p in P.PLANS}))
    check("SF9 the 2027 prices are the price list's", all(("EUR %.2f" % P.PRICE27[p]) in pl_txt for p in P.PLANS))
    check("SF15 the e-mail's leavers read against the other region, every e-mail dated 1 December in the price list",
          all(s in pl_txt for s in ("1 December 2024", "1 December 2025", "1 December 2026")) and
          all(p["answer"] == fig["raise"] for p in E["forcing"]["perturbations"] if "December" in p["input"]))
    g_ann = M.gradient(M.announce(pk, M.GOLD), "xb", lambda r: True)
    check("SF16 the stayers' listening within accounts: the December leavers listened less (a plan's average rises "
          "with no one listening more), and the observed months fade", g_ann[0] > g_ann[3] and
          obs["ONB"][0][1] > 3 * max(obs["ONB"][-2][1], 0.01), "leaving by band %s; Onbeperkt %.3f to %.3f" % (
              [round(float(x), 2) for x in g_ann], obs["ONB"][0][1], obs["ONB"][-2][1]))
    check("SF17 the continuation by paying months alone: same call",
          EP.results(pk, M.opts(surv="plan_tenure"))["R8"] == fig["raise"])
    check("SF22 the 2027 remuneration on each subscription's own counted hours differs from the plan's flat share",
          all(abs(fig["remun_2027"][p] - EP.results(pk, M.opts(cost="share26"))["R2"][p]) > 1 for p in EP.NAMES.values()))
    # documents
    check("doc: guideline 3.10 files when a rise goes ahead", "January price rise goes ahead on a plan" in gd310)
    check("doc: guideline 3.8 files the rivals' prices as last scanned", "rivals' prices as last scanned" in gd310)
    pl = pdf_text(os.path.join(TARGET, docs.FILES["price"]))
    check("doc: no document names a crossing, a return or the stayers' listening",
          not re.search(r"cross|threshold|step|passes the rival|come back|returns? (to|after)|take[sn]? .{0,12}up again|"
                        r"reactivat|resubscri|listen more|win[- ]back", gd310 + pl, re.I))
    check("doc: the price list carries each 2027 price", all(("EUR %.2f" % P.PRICE27[p]) in pl for p in P.PLANS))
    check("doc: the price list dates every past e-mail and the 2027 one",
          all(s in pl for s in ("1 December 2024", "1 December 2025", "1 December 2026")))
    sb = pdf_text(os.path.join(TARGET, docs.FILES["schB"]))
    check("doc: schedule B carries the rate", "EUR 0.40 for every counted hour" in sb)
    # realism
    ids = pk["acc"]["account_id"].str[1:].astype(int).sort_values().diff().dropna()
    check("realism: account ids not one constant step", ids.nunique() > 5)
    check("realism: paying counts differ by plan", len(set(fig["paying_oct"].values())) == 4)
    plp = pk["plan"]
    check("realism: some accounts hold more than one paid period with a gap", (plp[plp["phase"] == "paid"].groupby(
        "account_id").size() > 1).sum() > 500)
    print("%d checks, %d FAIL" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
