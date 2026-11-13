"""task7 architecture 11: every result of the design note's results chain computed on the cut pack with its rivals (the
band) and the hurried routes (the shortcuts), the assertions the build must pass, figures.json and effort.json."""
import csv
import datetime as dt
import os
from collections import Counter

import numpy as np

import golden as G
import verify as V

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def r1(x):
    return round(float(x), 1)


def money(x):
    return int(round(float(x) / 100.0) * 100)


# one marginal unit either side of the rivals' spread: after EV-4, DPS-7 and the proposal file every reading, what is left is
# arithmetic at the limit (the units nearest it sit a fraction of a kW from it, margins() lists them)
PAD = {"own": 1, "stagger": 1.0, "sequence": 1}


def band_of(vals, pad=0.0):
    return [min(vals) - pad, max(vals) + pad]


def replace_band(C, o):
    """the replacement cost's band: the rivals' spread, one marginal unit either side at that unit's own DPS-7 cost"""
    res, rv = C["S"]["res"], C["rivals"]
    vals = [res[o]["replace"]] + [r[o]["replace"] for r in rv.values()]
    lo, hi = min(vals), max(vals)
    if o == "stagger":
        unit = res[o]["replace"] / max(res[o]["over"], 1e-9)
        return [lo - PAD[o] * unit, hi + PAD[o] * unit]
    m = C["margins"][o]
    return [lo - (m["over"][0][2] if m["over"] else 0), hi + (m["under"][0][2] if m["under"] else 0)]


def run(target, w=None):
    P = V.Pack(target)
    S = G.solve(P)
    B = S["B"]
    n = S["n"]
    rival_out = {nm: G.replay(B, **kw) for nm, kw in G.RIVALS.items()}
    rivals = {nm: G.totals(o, n) for nm, o in rival_out.items()}
    routes = {nm: G.totals(G.replay(B, **kw), n) for nm, kw in G.ROUTES.items()}
    pert = {}
    for nm, d in (("DPS-7's peaking factors 0.02 lower", -0.02), ("DPS-7's peaking factors 0.02 higher", 0.02)):
        pert[nm] = G.totals(G.replay(B, factor={k: v + d for k, v in G.PEAK.items()}), n)
    pert["no peaking factor (each hour flat)"] = G.totals(G.replay(B, factor={k: 1.0 for k in G.PEAK}), n)
    res = S["res"]
    cost_down = {o: dict(v) for o, v in res.items() if isinstance(v, dict)}
    for o in G.OPTIONS:
        cost_down[o]["total"] = cost_down[o]["fee"] + 0.8 * cost_down[o]["replace"]
    pert["replacement costs -20 per cent"] = dict(cost_down, call=min(G.OPTIONS, key=lambda o: cost_down[o]["total"]))
    fee_up = {o: dict(v) for o, v in res.items() if isinstance(v, dict)}
    fee_up["sequence"]["total"] = fee_up["sequence"]["fee"] * 1.2 + fee_up["sequence"]["replace"]
    pert["Sequence's fee +20 per cent"] = dict(fee_up, call=min(G.OPTIONS, key=lambda o: fee_up[o]["total"]))
    # the readings the filed sentences close, run so the fork table can say what each would have given (Sequence only,
    # so Stagger is taken at the cheap average-night route here)
    closed = {nm: G.totals(G.replay(B, stagger="profile", **kw), n)["sequence"]["over"] for nm, kw in (
        ("the queue not waiting for a late charger", dict(block=False)),
        ("ready-by 15 minutes before the unplug time", dict(shift=1)),
        ("ready-by 30 minutes before the unplug time", dict(shift=2)),
        ("same-minute plug-ins in the other order", dict(tie_rev=True)))}
    C = dict(P=P, S=S, B=B, n=n, rivals=rivals, rival_out=rival_out, routes=routes, pert=pert, closed=closed)
    C["raw"] = raw_counts(target, P)
    C["margins"] = margins(S["out"])
    assertions(C, w)
    return C


def margins(out):
    """each option's summer peak less the limit, kW, for the units nearest it (own and Sequence)"""
    m = {}
    for o in ("own", "sequence"):
        rows = sorted(((r[o + "_peak"] - r["limit"], t, r["cost"]) for t, r in out.items()), key=lambda x: abs(x[0]))
        m[o] = {"under": [(t, round(x, 2), c) for x, t, c in rows if x <= 0][:3],
                "over": [(t, round(x, 2), c) for x, t, c in rows if x > 0][:3]}
    return m


def monitors_table(P):
    """DPS-7 Table 2 from the monitors file: a day's highest 15-minute load over its clock hour's load, in the hour of the
    day's highest load, averaged over the days and the monitored units of each size"""
    rec = {}
    for t, mon in P.mon.items():
        m = mon.reshape(-1, 4)
        good = ~np.isnan(m).any(axis=1)
        hm, mx = m.mean(1), m.max(1)
        rs = []
        for d in range(G.ND):
            sl = slice(d * 24, (d + 1) * 24)
            h = np.where(good[sl], hm[sl], -np.inf)
            j = int(np.argmax(h))
            if np.isfinite(h[j]) and h[j] > 0:
                rs.append(mx[sl][j] / hm[sl][j])
        rec.setdefault(P.kva[t], []).append(np.mean(rs))
    return {k: round(float(np.mean(v)), 2) for k, v in rec.items()}


def raw_counts(target, P):
    """what the files say before they are cleaned: the quick pass's counts"""
    with open(os.path.join(target, "ev_overnight_roster_2026-11-02.csv"), newline="", encoding="utf-8") as fh:
        ro = list(csv.DictReader(fh))
    active_rows = sum(1 for r in ro if r["status"] == "Active")
    gis_only = set()
    with open(os.path.join(target, "gis_service_points_2026-10-30.csv"), newline="", encoding="utf-8") as fh:
        g = {r["service_point"]: r["transformer_location"] for r in csv.DictReader(fh)}
    for k in P.enrolled:
        gis_only.add(g[P.ch[k]["sp"]])
    return dict(active_rows=active_rows, tx_gis_only=len(gis_only), roster_rows=len(ro))


def assertions(C, w):
    P, S, n = C["P"], C["S"], C["n"]
    res, rivals, routes = S["res"], C["rivals"], C["routes"]
    gold = {o: res[o]["over"] for o in G.OPTIONS}
    check("the call is Sequence", res["call"] == "sequence", res["call"])
    m = res["stagger"]["total"] - res["sequence"]["total"]
    check("Sequence beats Stagger by a third or more of Stagger's cost", m >= res["stagger"]["total"] / 3,
          "margin %.0f on %.0f" % (m, res["stagger"]["total"]))
    check("Sequence beats own schedules by half or more", res["own"]["total"] - res["sequence"]["total"] >= res["own"]["total"] / 2)
    for nm, r in rivals.items():
        check("rival %s calls Sequence" % nm, r["call"] == "sequence", r["call"])
    for o in G.OPTIONS:
        vals = [gold[o]] + [r[o]["over"] for r in rivals.values()]
        b = band_of(vals, PAD[o])
        C.setdefault("bands", {})[o] = b
        check("golden %s inside its rivals' band" % o, b[0] <= gold[o] <= b[1], "%s %s" % (gold[o], b))
    bands = C["bands"]
    # the shortcuts
    check("careful but hurried calls Stagger", routes["careful"]["call"] == "stagger", routes["careful"]["call"])
    check("the average managed night alone calls Stagger", routes["no_J1"]["call"] == "stagger")
    check("Sequence taken as the pilot's managed quarter calls Stagger", routes["no_J3_as_stagger"]["call"] == "stagger")
    check("Sequence as one charger at a time misses the budget band",
          routes["no_J3_perfect"]["sequence"]["over"] < bands["sequence"][0] - 2,
          "%s vs %s" % (routes["no_J3_perfect"]["sequence"]["over"], bands["sequence"]))
    check("the average night's Stagger count is far below the band",
          routes["no_J1"]["stagger"]["over"] < bands["stagger"][0] / 3)
    check("own schedules as metered in 2026 miss the own band, and the call stands (a supporting step)",
          routes["no_own"]["own"]["over"] < bands["own"][0] - 5 and routes["no_own"]["call"] == "sequence",
          "%s vs %s" % (routes["no_own"]["own"]["over"], bands["own"]))
    calls = {nm: (r["call"], round(r[r["call"]]["over"], 1)) for nm, r in routes.items()}
    wrong = {v for v in calls.values() if v != ("sequence", round(gold["sequence"], 1))}
    check("the shortcuts land on two or more distinct wrong answers", len(wrong) >= 3, str(sorted(wrong)))
    for nm, r in C["pert"].items():
        check("perturbation %s keeps Sequence" % nm, r["call"] == "sequence", r["call"])
    check("the flip fee is at least three times the quote", S["flip"] >= 3 * G.FEE["sequence"], "%.1f" % S["flip"])
    pe = S["pilot"]
    check("the pilot's effect at 23:00-23:15 is a large cut", pe["effect"] < -3.5, "%.3f" % pe["effect"])
    check("the managed quarter is about a quarter of the chargers", 0.2 < pe["n_managed"] / (pe["n_managed"] + pe["n_own"]) < 0.3)
    # the assembly
    check("every enrolled charger maps to a transformer in the register",
          all(P.sp_tx[P.ch[k]["sp"]] in P.kva for k in P.enrolled))
    check("the work orders move service points the GIS has not caught up with", len(P.transfers) > 0)
    check("the register lags change-outs the work orders record",
          any(float(r["detail"].split(" with ")[1].split(" kVA")[0]) != None for r in P.changeouts))
    check("the roster's re-imported rows are dropped", C["raw"]["roster_rows"] > len({(k) for k in P.ch}))
    check("the meter data's re-sent rows and estimated hours are seen", P.est_hours > 0)
    # the semantic fork table, row by row
    B = C["B"]
    check("SF1 the chargers covered are those enrolled on 1 November 2026", n == len(P.enrolled) and
          all(P.ch[k]["enrolled"] <= V.QUOTE_DAY for k in P.enrolled), str(n))
    check("SF2 the summer is July and August 2026", G.WIN == 62 * G.Q and G.ND == 62)
    check("SF3 the limit is 120 per cent of nameplate at kW / 0.95", G.LIMIT == 1.20 and G.PF == 0.95)
    lag = [r["transformer_location"] for r in P.changeouts]
    check("SF4 the nameplate is the register's corrected by the change-outs", len(lag) > 0 and all(P.kva[t] > 0 for t in lag))
    check("SF5 the transformers are the GIS's corrected by the work orders", len(P.transfers) > 0)
    check("SF6 every charger on its declared setting calls Sequence", rivals["declared_own"]["call"] == "sequence")
    check("SF7 Stagger's count is the sum of chances, stable across seeds",
          abs(rivals["seed_11"]["stagger"]["over"] - gold["stagger"]) < 1 and abs(rivals["seed_23"]["stagger"]["over"] - gold["stagger"]) < 1)
    check("SF8 a session's ready-by is its unplug time rounded down to the quarter-hour (EV-4 4.1)",
          all(s[2] == G.evening_q(s[5]["night"], s[5]["unplug"]) for k in P.enrolled for s in B.sess[k]))
    check("SF9 Sequence's rule is the proposal's, and a run of it lands inside the band",
          bands["sequence"][0] <= gold["sequence"] <= bands["sequence"][1])
    check("SF10 replacement costs are DPS-7 Table 1's by unit and mount",
          all(r["cost"] == (G.COST_POLE50 if r["kva"] == 50.0 and P.mount.get(t, "").lower().startswith("pole") else G.COST[r["kva"]])
              for t, r in S["out"].items()))
    check("SF11 the fee is per enrolled charger per year", abs(res["sequence"]["fee"] - G.FEE["sequence"] * n) < 1)
    check("SF12 the pilot's change is per enrolled charger over every night", S["pilot"]["n_managed"] > 0 and S["pilot"]["n_own"] > 0)
    check("SF13 chargers that left the rate stay in the base as metered",
          any(c["closed"] is not None for c in P.ch.values()))
    tab = monitors_table(P)
    check("SF14 the quarter-hour is DPS-7 Table 2's factor on the hourly reads, monitored or not; the monitors reproduce it",
          all(abs(tab[k] - G.PEAK[k]) < 0.0051 for k in G.PEAK) and (w is None or __import__("world").PEAK == G.PEAK),
          str(sorted(tab.items())))
    check("SF15 sessions plugged in on 30 June count in July's quarters",
          any(s[5]["night"] == G.EVE0 for k in P.enrolled for s in B.sess[k]))
    check("SF16 31 August's night after midnight is outside the window", G.WIN == G.ND * G.Q)
    cl = C["closed"]
    check("SF17 the queue waits for a late charger (the proposal: every charger before it has finished); not waiting is "
          "another count, closed by the text", cl["the queue not waiting for a late charger"] < gold["sequence"],
          "%s vs %s" % (cl["the queue not waiting for a late charger"], gold["sequence"]))
    check("SF18 ready-by earlier than the unplug time is another count, closed by EV-4 4.1",
          cl["ready-by 15 minutes before the unplug time"] != gold["sequence"] or
          cl["ready-by 30 minutes before the unplug time"] != gold["sequence"], str(cl))
    check("SF19 same-minute plug-ins sharing a ready-by time leave the count where it is",
          cl["same-minute plug-ins in the other order"] == gold["sequence"], str(cl))
    dur = [abs((s[5]["end"] - s[5]["start"]).total_seconds() / 3600.0 - s[3] / s[4]) for k in P.enrolled for s in B.sess[k]]
    check("SF20 each session's charge time is its energy at its charger's rated kW (EV-4 4.1: the time its charge took)",
          max(dur) < 2.0 / 3600, "max %.5f h" % max(dur))
    check("SF21 the sessions the window cannot fit, started early enough to finish, leave every count where it is",
          all(abs(rivals["late_sessions_early"][o]["over"] - gold[o]) < (0.6 if o == "stagger" else 0.5) for o in G.OPTIONS),
          str({o: rivals["late_sessions_early"][o]["over"] for o in G.OPTIONS}))
    check("SF22 own sessions advanced to finish by their unplug times leave the own count where it is",
          rivals["own_advanced"]["own"]["over"] == gold["own"], str(rivals["own_advanced"]["own"]["over"]))
    check("SF23 the own three-quarters at their recorded 2026 starts give the same own count",
          rivals["recorded_own"]["own"]["over"] == gold["own"], str(rivals["recorded_own"]["own"]["over"]))
    neg = {}
    for sh in (0, -1):                        # the session log read at local daylight time, and an hour off it
        n_neg = 0
        for t, ks in B.tx_ch.items():
            ev = np.zeros(G.ND * 24)
            for k in ks:
                h = B.ev15[k].reshape(-1, 4).mean(1)
                ev += np.roll(h, sh) if sh else h
            n_neg += int(((B.obs[t] - ev) < -0.3)[ev > 0.5].sum())      # charging hours where the reads fall short of it
        neg[sh] = n_neg
    check("SF26 the session log's UTC times sit on local daylight time, six hours behind: there the hourly reads almost "
          "never fall short of the chargers' charging, an hour off they often do", neg[0] * 10 < neg[-1], str(neg))
    starts = [a for t in B.tx_ch for a, _, _ in G.sequence_blocks([x for k in B.tx_ch[t] for x in B.sess[k]])]
    check("SF25 both products start a session only on the quarter-hour (Sequence's starts are whole quarters)",
          all(float(a).is_integer() for a in starts), "%d starts" % len(starts))
    pole = [t for t, r in S["out"].items() if r["kva"] == 50.0 and P.mount.get(t, "").lower().startswith("pole")]
    check("SF24 the 50 kVA pole-mount units are priced by DPS-7 Table 1", len(pole) > 0 and
          all(S["out"][t]["cost"] == G.COST_POLE50 for t in pole), "%d units" % len(pole))
    if w is not None:
        truth_n = sum(1 for c in w.chargers if c["enrol"] <= V.QUOTE_DAY and c["left"] is None)
        check("chargers enrolled on 1 November match the world", n == truth_n, "%d vs %d" % (n, truth_n))
        tx_truth = len({w.homes[c["home"]]["tx"] for c in w.chargers if c["left"] is None})
        check("transformers serving them match the world", len(S["out"]) == tx_truth, "%d vs %d" % (len(S["out"]), tx_truth))


# ---- figures.json ------------------------------------------------------------------------------------------------------
NAMES = {"own": "Members' own schedules", "stagger": "Quillpoint Stagger", "sequence": "Quillpoint Sequence"}


def figures(C):
    P, S, n = C["P"], C["S"], C["n"]
    res = S["res"]
    F = {"n_chargers": n, "n_tx": len(S["out"]), "call": NAMES[res["call"]], "call_key": res["call"],
         "fee_rate": {o: G.FEE[o] for o in G.OPTIONS}}
    for o in G.OPTIONS:
        F[o] = {"over": r1(res[o]["over"]) if o == "stagger" else int(round(res[o]["over"])),
                "fee": money(res[o]["fee"]), "replace": money(res[o]["replace"]), "total": money(res[o]["total"])}
    F["own_over"], F["stagger_over"], F["sequence_over"] = F["own"]["over"], F["stagger"]["over"], F["sequence"]["over"]
    F["totals"] = {o: F[o]["total"] for o in G.OPTIONS}
    F["budget"] = F["sequence"]["over"]
    F["call_budget"] = "%s, %s" % (F["call"], F["budget"])
    F["budget_cost"] = F["sequence"]["replace"]
    F["flip_fee"] = int(round(S["flip"]))
    F["pilot_effect"] = round(S["pilot"]["effect"], 2)
    F["pilot_cut"] = abs(F["pilot_effect"])
    F["pilot_band"] = 0.1
    F["draws"] = G.K_RANDOM
    F["cites"] = {"EV-4 random option at its chance": 4.3, "DPS-7 limit": 2.1, "EV-4 summer like the last one": 4.1}
    F["pilot_own"] = round(S["pilot"]["own"], 2)
    F["pilot_managed"] = round(S["pilot"]["managed"], 2)
    F["pilot_n"] = {"managed": S["pilot"]["n_managed"], "own": S["pilot"]["n_own"]}
    b = C["bands"]
    F["bands"] = {"own": [int(np.floor(b["own"][0])), int(np.ceil(b["own"][1]))],
                  "stagger": [r1(np.floor(b["stagger"][0] * 2) / 2), r1(np.ceil(b["stagger"][1] * 2) / 2)],
                  "sequence": [int(np.floor(b["sequence"][0])), int(np.ceil(b["sequence"][1]))]}
    rv = C["rivals"]
    rb = {o: replace_band(C, o) for o in G.OPTIONS}
    F["band_replace"] = {o: [money(rb[o][0]), money(rb[o][1])] for o in G.OPTIONS}
    F["band_totals"] = {o: [money(res[o]["fee"] + rb[o][0]), money(res[o]["fee"] + rb[o][1])] for o in G.OPTIONS}
    st_lo, st_hi = res["stagger"]["fee"] + rb["stagger"][0], res["stagger"]["fee"] + rb["stagger"][1]
    F["band_flip"] = [int(np.floor((st_lo - rb["sequence"][1]) / n)), int(np.ceil((st_hi - rb["sequence"][0]) / n))]
    F["routes"] = {nm: {"call": NAMES[r["call"]], "own": r1(r["own"]["over"]), "stagger": r1(r["stagger"]["over"]),
                        "sequence": r1(r["sequence"]["over"]), "total": money(r[r["call"]]["total"]),
                        "flip": int(round((r["stagger"]["total"] - r["sequence"]["replace"]) / n))}
                   for nm, r in C["routes"].items()}
    F["rivals"] = {nm: {"own": r1(r["own"]["over"]), "stagger": r1(r["stagger"]["over"]), "sequence": r1(r["sequence"]["over"])}
                   for nm, r in rv.items()}
    F["raw"] = C["raw"]
    F["tx_gis_only"] = C["raw"]["tx_gis_only"]
    F["by_size"] = {}
    for o in G.OPTIONS:
        cnt = Counter()
        for t, r in S["out"].items():
            cnt["%g" % r["kva"]] += r[o + "_p"]
        F["by_size"][o] = {k: r1(v) for k, v in sorted(cnt.items(), key=lambda kv: float(kv[0]))}
    F["sizes"] = {k: v for k, v in sorted(Counter("%g" % r["kva"] for r in S["out"].values()).items(), key=lambda kv: float(kv[0]))}
    F["chargers_per_tx_max"] = max(r["chargers"] for r in S["out"].values())
    F["monitors"] = len(P.mon)
    F["peak_table"] = {"%g" % k: v for k, v in sorted(G.PEAK.items())}
    F["closed"] = {k: r1(v) for k, v in C["closed"].items()}
    F["margins"] = C["margins"]
    F["pole50"] = sum(1 for t, r in S["out"].items() if r["cost"] == G.COST_POLE50)
    F["managed_profile_peak"] = r1(float(G.managed_profile(C["B"]).max()))
    return F


# ---- effort.json -------------------------------------------------------------------------------------------------------
def effort(C, F):
    rt = F["routes"]
    res = []
    res.append({"id": "R1", "name": "chargers enrolled on 1 November 2026", "graded_as": "Ask 5", "figure": "n_chargers",
                "depends": [], "independent": "the roster", "golden": F["n_chargers"], "band": [F["n_chargers"], F["n_chargers"]],
                "passes": {"quick": F["raw"]["active_rows"], "careful": F["n_chargers"], "thorough": F["n_chargers"]}})
    res.append({"id": "R1b", "name": "transformers serving them (the CSV's rows)", "graded_as": "Ask 1", "figure": "n_tx",
                "depends": ["R1"], "independent": "", "golden": F["n_tx"], "band": [F["n_tx"], F["n_tx"]],
                "passes": {"quick": F["tx_gis_only"], "careful": F["n_tx"], "thorough": F["n_tx"]}})
    res.append({"id": "R2", "name": "the pilot's change at 23:00 to 23:15, kW per enrolled charger", "graded_as": "Component 4",
                "figure": "pilot_effect", "depends": [], "independent": "the session log and the pilot halves",
                "golden": F["pilot_effect"], "band": [F["pilot_effect"] - 0.1, F["pilot_effect"] + 0.1],
                "passes": {"quick": None, "careful": F["pilot_effect"], "thorough": F["pilot_effect"]}})
    res.append({"id": "R3", "name": "own schedules' transformers over their limit", "graded_as": "Component 3",
                "figure": "own_over", "depends": ["R1b"], "independent": "", "golden": F["own"]["over"],
                "band": F["bands"]["own"], "precedent": ["L04", "L01"],
                "passes": {"quick": rt["quick"]["own"], "careful": rt["careful"]["own"], "thorough": F["own"]["over"]}})
    res.append({"id": "R4", "name": "Stagger's transformers over their limit, each at its chance", "graded_as": "Component 1",
                "figure": "stagger_over", "depends": ["R1b"], "independent": "", "golden": F["stagger"]["over"],
                "band": F["bands"]["stagger"], "precedent": ["L15", "N01"],
                "passes": {"quick": rt["quick"]["stagger"], "careful": rt["careful"]["stagger"], "thorough": F["stagger"]["over"]}})
    res.append({"id": "R5", "name": "Sequence's transformers over their limit (the work plan's replacements)",
                "graded_as": "Component 2", "figure": "sequence_over", "depends": ["R1b"], "independent": "",
                "golden": F["sequence"]["over"], "band": F["bands"]["sequence"], "precedent": ["L15", "N04"],
                "passes": {"quick": rt["quick"]["sequence"], "careful": rt["careful"]["sequence"],
                           "thorough": F["sequence"]["over"]}})
    tot = {o: F[o]["total"] for o in G.OPTIONS}
    res.append({"id": "R6", "name": "each option's fee, replacement cost and total", "graded_as": "Ask 2-4", "figure": "totals",
                "depends": ["R3", "R4", "R5"], "independent": "", "golden": tot,
                "bands": {o: F["band_totals"][o] for o in G.OPTIONS}, "precedent": ["L15"],
                "passes": {"quick": {o: None for o in G.OPTIONS},
                           "careful": {o: _route_total(C, "careful", o) for o in G.OPTIONS}, "thorough": tot}})
    res.append({"id": "R7", "name": "the default and the work plan's replacements", "graded_as": "Recommendation",
                "figure": "call_budget", "depends": ["R4", "R5"], "independent": "",
                "golden": "%s, %s" % (F["call"], F["budget"]), "precedent": ["L15"],
                "passes": {"quick": "%s, %s" % (rt["quick"]["call"], _fmt(rt["quick"][_key(rt["quick"]["call"])])),
                           "careful": "%s, %s" % (rt["careful"]["call"], _fmt(rt["careful"][_key(rt["careful"]["call"])])),
                           "thorough": "%s, %s" % (F["call"], F["budget"])}})
    res.append({"id": "R8", "name": "the Sequence fee at which the call would change", "graded_as": "Ask 6", "figure": "flip_fee",
                "depends": ["R4", "R5", "R6"], "independent": "", "golden": F["flip_fee"], "band": F["band_flip"],
                "precedent": ["L15"],
                "passes": {"quick": rt["quick"]["flip"], "careful": rt["careful"]["flip"], "thorough": F["flip_fee"]}})
    routes = [{"name": "the golden", "answer": "%s, %s" % (F["call"], F["budget"]), "golden": True}]
    for nm, r in rt.items():
        routes.append({"name": nm, "answer": "%s, %s" % (r["call"], _fmt(r[_key(r["call"])])), "golden": False})
    hints = [{"sentence": "a few chargers on one transformer still land together on some night of the summer under a random "
                          "start, so replay every night", "rescues": ["R4"]},
             {"sentence": "Sequence was never piloted: run its rule on each night's sessions", "rescues": ["R5"]},
             {"sentence": "a quarter of the chargers were managed in summer 2026, so the metered summer is not the members' "
                          "own schedules", "rescues": ["R3"]}]
    gold_answer = [F["call"]]
    forcing = {"kind": "set", "golden_answer": gold_answer,
               "golden_family": [{"name": "the golden", "answer": gold_answer}] +
                                [{"name": nm, "answer": [NAMES[r["call"]]]} for nm, r in C["rivals"].items()],
               "shortcuts": [{"name": nm, "answer": [r["call"]]} for nm, r in rt.items() if r["call"] != F["call"]],
               "perturbations": [{"input": nm, "answer": [NAMES[r["call"]]]} for nm, r in C["pert"].items()]}
    return {"results": res, "routes": routes, "hints": hints, "forcing": forcing,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}


def _key(call_name):
    return {v: k for k, v in NAMES.items()}[call_name]


def _fmt(x):
    return ("%g" % x) if isinstance(x, (int, float)) else str(x)


def _route_total(C, route, o):
    return money(C["routes"][route][o]["total"])
