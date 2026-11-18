"""Every owed figure from the cut pack: the golden's estimate and its account year by year, the bands the answer
blocks state (the battery's range and a quarter of it each side, rounded outward), every route of the lattice, the
referee, the forcing table, the core re-proved on the shipped files (corelib) and the effort passes (effort.json)."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
import corelib  # noqa: E402
import effort as EF  # noqa: E402
import analysis as A  # noqa: E402
import core as C  # noqa: E402

HOME, HOSTS, STATES = C.HOME, C.HOSTS, C.STATES
NY, LAST, Y0, REF = C.NY, C.LAST, C.Y0, C.REF
KEYS = list(C.lattice_opts())
REFLEX = "+".join(sorted(C.HURRIED))
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
ROUTE_NAME = {
    "S1": "each host's arrivals table taken as the arrivals",
    "S2": "each host's departures table taken as the exits",
    "S3": "2021 to 2023 carried through 2024 to 2026",
    "S1+S2": "the hosts' tables at face value to 2023, 2024 to 2026 from the home register",
    "S1+S3": "arrivals as tabled, the account closed between the censuses, 2021 to 2023 carried forward",
    "S2+S3": "arrivals corrected, departures as tabled, 2021 to 2023 carried forward",
    "S1+S2+S3": "the hosts' tables at face value from the 2021 census, 2021 to 2023 carried forward",
}
STUMP_NAME = {
    "S1": "a host's arrivals table is that host's share of the citizens who arrived; the shares come from the two "
          "reports of every flow, and their level from Orlava's census table against its own register",
    "S2": "a host's exits are what its two censuses, the corrected arrivals and the births and deaths leave; its "
          "departures table is a share of them",
    "S3": "the moves of 2024 to 2026 come from Orlava's register, at the share of each host's moves it caught in the "
          "years both sides report",
}
PREC = {"S1": ["L22", "L51", "N27"], "S2": ["L48", "L32", "N10"], "S3": ["N13", "N28", "L03"]}


def officers(n):
    return int(math.ceil(n / C.STD))


def call_of(n):
    return ["%s %d" % (h, officers(n[h])) for h in HOSTS]


def band_of(golden, family, step):
    lo, hi = min(family + [golden]), max(family + [golden])
    room = corelib.BAND_ROOM * (hi - lo)
    q = 1.0 / step
    return [math.floor((lo - room) * q + 1e-9) / q, math.ceil((hi + room) * q - 1e-9) / q]


def account(R, h):
    """The golden's account for one host, year by year: citizens on 1 January, the year's arrivals, exits and
    births less deaths, 2011 to 2026, and the citizens on 1 January 2027."""
    g = C.chain(R, h)
    q = R["host"][h]
    inn = R["recA"][HOME, h][:LAST] / g["a"]
    ex = q["dep"][:LAST] / g["d"]
    rows, n = [], q["n11"]
    for t in range(10):
        rows.append([Y0 + t, n, inn[t], ex[t], q["nat"][t]])
        n = n + inn[t] - ex[t] + q["nat"][t]
    assert abs(n - q["n21"]) < 1e-6, (h, n, q["n21"])
    n, py = q["n21"], 0.0
    for t in range(10, LAST):
        rows.append([Y0 + t, n, inn[t], ex[t], q["nat"][t]])
        py += n
        n = n + inn[t] - ex[t] + q["nat"][t]
    rate = q["nat"][10:LAST].sum() / py
    for k in range(NY - LAST):
        a2, e2 = R["recD"][HOME, h][LAST + k] / g["b_h"], q["ret"][LAST + k] / g["r_h"]
        rows.append([Y0 + LAST + k, n, a2, e2, n * rate])
        n = n + a2 - e2 + n * rate
    assert abs(n - g["n"]) < 1e-6, (h, n, g["n"])
    rows.append([Y0 + NY, n, None, None, None])
    return rows, rate


WEIGHTINGS = ("unweighted", "by arrivals", "by the 2011 count", "by the square of arrivals")
T95 = 2.5706          # Student's t, 97.5 per cent point on five degrees of freedom (seven citizenships, two shares)


def closure(R, fig, G, f):
    """What the files say about the other standard route the pack affords: each host's two shares fitted on its own
    census accounts of the seven foreign citizenships (no second report of a flow, no census table), and the one
    thing those accounts can fix beside the two reports, the level of the shares."""
    cit = R["cit"]
    inside = lambda v, b: b[0] <= v <= b[1]

    def rows(h):
        cs = [c for c in STATES if c != h]
        arr = np.array([np.nansum(R["recA"][c, h][:10]) for c in cs])
        dep = np.array([np.nansum(cit["dep"][h, c][:10]) for c in cs])
        chg = np.array([cit["n21"][h, c] - cit["n11"][h, c] - np.nansum(cit["nat"][h, c][:10]) for c in cs])
        n11 = np.array([cit["n11"][h, c] for c in cs])
        return cs, arr, dep, chg, n11

    def weights(name, arr, n11):
        return {"unweighted": np.ones(len(arr)), "by arrivals": 1.0 / arr, "by the 2011 count": 1.0 / n11,
                "by the square of arrivals": 1.0 / arr ** 2}[name]

    def fit(h, name, drop=None):
        cs, arr, dep, chg, n11 = rows(h)
        keep = np.array([c != drop for c in cs])
        M, y, w = np.column_stack([arr, -dep])[keep], chg[keep], np.sqrt(weights(name, arr, n11)[keep])
        sol = np.linalg.lstsq(M * w[:, None], y * w, rcond=None)[0]
        res = (y - M @ sol) * w
        cov = (res ** 2).sum() / (len(y) - 2) * np.linalg.inv((M * w[:, None]).T @ (M * w[:, None]))
        return 1.0 / sol[0], 1.0 / sol[1], sol[0], float(np.sqrt(cov[0, 0]))

    out = dict(hosts={}, fits={})
    for h in HOSTS:
        a, d, coef, se = fit(h, "unweighted")
        send = [np.nansum(R["recA"][i, h][:LAST]) * f["b"][i] / np.nansum(R["recD"][i, h][:LAST]) for i in HOSTS if i != h]
        out["hosts"][h] = dict(share_pct=round(100.0 * a, 1),
                               interval_pct=[round(100.0 / (coef + T95 * se), 1), round(100.0 / (coef - T95 * se), 1)],
                               senders_pct=[round(100.0 * min(send), 1), round(100.0 * max(send), 1)],
                               outside_senders=bool(not min(send) <= a <= max(send)), golden_pct=round(100.0 * G[h]["a"], 1))
    out["outside_senders"] = [h for h in HOSTS if out["hosts"][h]["outside_senders"]]

    def carried(h, name, mode):
        a, d, _, _ = fit(h, name)
        o = {"x_a": a / G[h]["a"]}
        if mode == "both":
            o["x_d"] = d / C.chain(R, h, o)["d"]
        return o

    for name in WEIGHTINGS:
        for mode in ("both", "closed"):
            o = {h: carried(h, name, mode) for h in HOSTS}
            r = {h: C.chain(R, h, o[h]) for h in HOSTS}
            out["fits"][name + ", " + mode] = dict(
                citizens={h: int(round(r[h]["n"])) for h in HOSTS}, officers={h: officers(r[h]["n"]) for h in HOSTS},
                left={h: int(round(r[h]["left"])) for h in HOSTS}, c2=round(100.0 * r["Skarholm"]["d"], 1),
                census_2021_miss={h: int(round(C.chain(R, h, o[h], 10)["n"] - R["host"][h]["n21"])) for h in HOSTS},
                referee_value=int(round(C.chain(R, C.REFHOST, o[C.REFHOST], REF)["n"])),
                referee_off=int(round(abs(C.chain(R, C.REFHOST, o[C.REFHOST], REF)["n"] - R["host"][C.REFHOST]["n16"]))))
    miss = out["fits"]["unweighted, both"]["census_2021_miss"]
    over, under = max(HOSTS, key=lambda h: miss[h]), min(HOSTS, key=lambda h: miss[h])
    out["census_2021_miss_quoted"] = dict(over=dict(host=over, by=int(miss[over])), under=dict(host=under, by=int(-miss[under])))
    offs = [v["referee_off"] for v in out["fits"].values()]
    out["referee_off"] = [int(min(offs)), int(max(offs))]
    out["weightings"], out["interval_level_pct"] = len(WEIGHTINGS), 95
    out["officers_same"] = all(v["officers"] == fig["officers"] for v in out["fits"].values())
    out["officers_total"] = int(sum(fig["officers"].values()))
    near = min((min(n % C.STD, C.STD - n % C.STD), h, n) for v in out["fits"].values() for h, n in v["citizens"].items())
    out["nearest_line"] = dict(distance=int(near[0]), host=near[1], citizens=int(near[2]))

    # --- the level: the two reports' ratios between the hosts kept, one factor on every host's share, each host's
    # departure share fitted across its citizenships, the factor that fits the 49 accounts best
    grid = np.linspace(0.85, 1.15, 3001)

    def level(o, name, pooled):
        fo = C.factors(R, o)
        tot = np.zeros(len(grid))
        for h in HOSTS:
            cs, arr, dep, chg, n11 = rows(h)
            w = weights(name, arr, n11)
            y = chg[None, :] - arr[None, :] / (fo["a"][h] * grid[:, None])        # what the departures must explain
            slope = (w * -dep * y).sum(axis=1) / (w * dep * dep).sum()
            sse = (w * (y + slope[:, None] * dep[None, :]) ** 2).sum(axis=1)
            tot += sse if pooled else sse / (w * chg ** 2).sum()         # the 49 accounts pooled, or each host's own weighed equally
        return float(grid[int(np.argmin(tot))])

    singles = [(n, o) for n, o in C.FAMILY[1:] if len(o) == 1 and "anchor" not in o]
    lev, ok_bands, ok_call, lo, hi = {}, True, True, {h: np.inf for h in HOSTS}, {h: -np.inf for h in HOSTS}
    cfn = {"C1": lambda o: 100.0 * C.b_home(R, o),
           "C2": lambda o: 100.0 * R["host"]["Skarholm"]["dep"][:10].sum() / C.chain(R, "Skarholm", o)["ex_p"],
           "C3": lambda o: C.chain(R, "Tesmar", o)["late"]}
    for name, pooled in [(n_, p_) for p_ in (False, True) for n_ in WEIGHTINGS]:
        for label, o in [("alone", {})] + singles:
            k = level(o, name, pooled)
            ok_ = dict(o, x_a=k)
            r = {h: C.chain(R, h, ok_) for h in HOSTS}
            if label == "alone":
                lev[name + (", pooled" if pooled else ", by host")] = dict(home_share_pct=round(100.0 * f["a_home"] * k, 1), citizens={h: int(round(r[h]["n"])) for h in HOSTS})
            ok_call &= all(officers(r[h]["n"]) == fig["officers"][h] for h in HOSTS)
            ok_bands &= all(inside(r[h]["n"], fig["citizens_band"][h]) and inside(r[h]["left"], fig["left_band"][h]) for h in HOSTS)
            ok_bands &= inside(cfn["C1"](o) * k, fig["c1_band"]) and inside(cfn["C2"](ok_), fig["c2_band"]) and inside(cfn["C3"](ok_), fig["c3_band"])
            for h in HOSTS:
                lo[h], hi[h] = min(lo[h], r[h]["n"]), max(hi[h], r[h]["n"])
    out["level"] = dict(readings=lev, home_share_pct=[min(v["home_share_pct"] for v in lev.values()), max(v["home_share_pct"] for v in lev.values())],
                        inside_every_band=bool(ok_bands), officers_same=bool(ok_call), rebuilds=2 * len(WEIGHTINGS) * (1 + len(singles)),
                        citizens_range={h: [int(round(lo[h])), int(round(hi[h]))] for h in HOSTS}, accounts=len(HOSTS) * (len(STATES) - 1))

    # --- the departure share pooled over a host's citizenships, at the estimate's arrival share
    pooled = {}
    for h in HOSTS:
        cs, arr, dep, chg, n11 = rows(h)
        d = dep.sum() / (arr.sum() / G[h]["a"] - chg.sum())
        o = {"x_d": d / G[h]["d"]}
        r = C.chain(R, h, o)
        pooled[h] = dict(share_pct=round(100.0 * d, 1), census_2021=int(round(C.chain(R, h, o, 10)["n"])), citizens=int(round(r["n"])),
                         left=int(round(r["left"])))
    out["pooled_departures"] = pooled

    # --- a share above one, capped
    cap = {}
    for h in HOSTS:
        if G[h]["a"] > 1.0:
            r = C.chain(R, h, {"x_a": 1.0 / G[h]["a"]})
            cap[h] = dict(citizens=int(round(r["n"])), left=int(round(r["left"])), officers=officers(r["n"]),
                          home_moves_pct=round(100.0 * r["b_h"], 1), home_moves_measured_pct=round(100.0 * G[h]["b_h"], 1))
    top = max(cap, key=lambda h: G[h]["a"])
    others = [100.0 * G[h]["b_h"] for h in HOSTS if h != top]
    out["cap"] = dict(hosts=cap, top=top, others_home_moves_pct=[round(min(others), 1), round(max(others), 1)])
    return out


def run(target):
    world = C.simulate()
    R = A.load(target)
    spec = C.main(world, R, task="task5 architecture 5, cut pack", quiet=True)
    lat_o = C.lattice_opts()
    G = {h: C.chain(R, h) for h in HOSTS}
    f = C.factors(R, {})
    figs = {x["id"]: x for x in spec["figures"]}
    mem = spec["members"]
    fig = {}
    # --- the estimate and its bands
    fig["citizens"] = {h: int(round(G[h]["n"])) for h in HOSTS}
    fig["citizens_band"] = {h: [int(v) for v in band_of(mem[h]["golden"], list(mem[h]["family"]), 10)] for h in HOSTS}
    fig["officers"] = {h: officers(G[h]["n"]) for h in HOSTS}
    fig["call"] = call_of({h: G[h]["n"] for h in HOSTS})
    fig["left"] = {h: int(round(G[h]["left"])) for h in HOSTS}
    fig["left_band"] = {h: [int(v) for v in band_of(figs["L-" + h]["golden"], list(figs["L-" + h]["family"]), 10)] for h in HOSTS}
    fig["c1"], fig["c1_band"] = round(figs["C1"]["golden"], 1), band_of(figs["C1"]["golden"], list(figs["C1"]["family"]), 0.1)
    fig["c2"], fig["c2_band"] = round(figs["C2"]["golden"], 1), band_of(figs["C2"]["golden"], list(figs["C2"]["family"]), 0.1)
    fig["c3"], fig["c3_band"] = round(figs["C3"]["golden"], 2), band_of(figs["C3"]["golden"], list(figs["C3"]["family"]), 0.01)
    for h in HOSTS:
        figs["N-" + h]["band"] = [float(v) for v in fig["citizens_band"][h]]
        figs["L-" + h]["band"] = [float(v) for v in fig["left_band"][h]]
    for c in ("c1", "c2", "c3"):
        figs[c.upper()]["band"] = fig[c + "_band"]
    # --- the establishment in force and the change
    fig["census_2011"] = {h: int(R["host"][h]["n11"]) for h in HOSTS}
    fig["census_2021"] = {h: int(R["host"][h]["n21"]) for h in HOSTS}
    fig["officers_in_force"] = {h: officers(R["host"][h]["n21"]) for h in HOSTS}
    fig["officers_change"] = {h: fig["officers"][h] - fig["officers_in_force"][h] for h in HOSTS}
    fig["officers_total"] = [sum(fig["officers_in_force"].values()), sum(fig["officers"].values())]
    fig["rate"] = int(C.STD)
    fig["margin_to_line"] = int(min(min(fig["citizens"][h] % fig["rate"], fig["rate"] - fig["citizens"][h] % fig["rate"]) for h in HOSTS))
    # --- the shares
    fig["share_home_arrivals_pct"] = round(100.0 * f["a_home"], 1)
    fig["share_partner_emigrants_pct"] = {h: round(100.0 * f["b"][h], 1) for h in HOSTS}
    fig["share_host_arrivals_pct"] = {h: round(100.0 * f["a"][h], 1) for h in HOSTS}
    fig["share_host_departures_pct"] = {h: round(100.0 * G[h]["d"], 1) for h in HOSTS}
    fig["share_home_moves_pct"] = {h: round(100.0 * G[h]["b_h"], 1) for h in HOSTS}
    fig["share_home_exits_pct"] = {h: round(100.0 * G[h]["r_h"], 1) for h in HOSTS}
    fig["late_ratio"] = {h: round(G[h]["late"], 2) for h in HOSTS}
    fig["exits_decade"] = {h: int(round(G[h]["ex_p"])) for h in HOSTS}
    fig["citizens_2024"] = {h: int(round(G[h]["n24"])) for h in HOSTS}
    fig["arrivals_2021_2026"] = {h: int(round(G[h]["arr"])) for h in HOSTS}
    fig["census_table_abroad"] = {h: int(R["census_in"][h]) for h in HOSTS}
    fig["register_arrivals_2020"] = {h: int(R["recA"][h, HOME][9]) for h in HOSTS}
    fig["census_table_abroad_total"] = sum(fig["census_table_abroad"].values())
    fig["register_arrivals_2020_total"] = sum(fig["register_arrivals_2020"].values())
    by_cit = [100.0 * R["recA"][h, HOME][9] / R["census_in"][h] for h in HOSTS]
    fig["share_home_arrivals_by_citizenship_pct"] = [round(min(by_cit), 1), round(max(by_cit), 1)]
    with_other = (fig["register_arrivals_2020_total"] + R["reg"]["A_other"][9]) / (fig["census_table_abroad_total"] + R["census_in_other"])
    n_other = {h: C.chain(R, h, {"x_a": with_other / f["a_home"]})["n"] for h in HOSTS}
    fig["other_row"] = dict(share_pct=round(100.0 * with_other, 1), citizens={h: int(round(n_other[h])) for h in HOSTS},
                            call_holds=call_of(n_other) == call_of({h: G[h]["n"] for h in HOSTS}),
                            inside_bands=all(mem[h]["golden"] is not None and min(mem[h]["family"]) - 0.25 * (max(mem[h]["family"]) - min(mem[h]["family"]))
                                             <= n_other[h] <= max(mem[h]["family"]) + 0.25 * (max(mem[h]["family"]) - min(mem[h]["family"])) for h in HOSTS))
    gm = float(np.exp(np.mean([np.log(v) for v in f["a"].values()])))
    fig["mean_route_home_share_pct"] = round(100.0 * f["a_home"] / gm, 1)
    # --- R1: what is on file, on one schema
    fig["tabled_arrivals_2011_2023"] = {h: int(R["recA"][HOME, h][:LAST].sum()) for h in HOSTS}
    fig["tabled_departures_2011_2023"] = {h: int(R["host"][h]["dep"][:LAST].sum()) for h in HOSTS}
    fig["register_deregistrations_2011_2026"] = {h: int(R["recD"][HOME, h].sum()) for h in HOSTS}
    fig["register_returns_2011_2026"] = {h: int(R["host"][h]["ret"].sum()) for h in HOSTS}
    fig["register_deregistrations_2024_2026"] = {h: int(R["recD"][HOME, h][LAST:].sum()) for h in HOSTS}
    fig["register_returns_2024_2026"] = {h: int(R["host"][h]["ret"][LAST:].sum()) for h in HOSTS}
    fig["register_returns_2021_2023"] = {h: int(R["host"][h]["ret"][10:LAST].sum()) for h in HOSTS}
    fig["natural_2011_2020"] = {h: int(R["host"][h]["nat"][:10].sum()) for h in HOSTS}
    face = {h: int(round(C.direct(R, h, 10) - R["host"][h]["n21"])) for h in HOSTS}
    fig["face_value_census_gap_by_host"] = face
    fig["face_value_census_gap"] = sum(abs(v) for v in face.values())
    fig["births_exceed_deaths_everywhere"] = bool(all((R["host"][h]["nat"][:LAST] > 0).all() for h in HOSTS))
    m = R["meta"]
    fig["counts"] = dict(register_rows=m["register_rows"], register_events=m["register_events"],
                         register_repeats=m["register_rows"] - m["register_events"], entry_lag_max_days=m["lag_max"],
                         table_rows=m["table_rows"], table_cells=m["table_cells"],
                         table_rows_superseded=m["table_rows"] - m["table_cells"], states=len(C.STATES),
                         entered_last=m["entered_last"], blank_codes=m["blank_codes"], releases=[m["releases"][0], m["releases"][-1]],
                         pairs=len(C.STATES) * (len(C.STATES) - 1), years_tables=[Y0, Y0 + LAST - 1],
                         years_register=[Y0, Y0 + NY - 1])
    # --- the account, year by year
    acc, rates = {}, {}
    for h in HOSTS:
        rows, rate = account(R, h)
        acc[h] = [dict(year=r[0], citizens_1_january=int(round(r[1])),
                       arrivals=None if r[2] is None else int(round(r[2])), exits=None if r[3] is None else int(round(r[3])),
                       births_less_deaths=None if r[4] is None else int(round(r[4]))) for r in rows]
        rates[h] = round(1000.0 * rate, 2)
    fig["account"], fig["natural_rate_per_1000"] = acc, rates
    fig["account_rows"] = int(sum(len(v) for v in acc.values()))
    # --- every route
    lat = spec["lattice"]
    fig["routes"] = {k: dict(name=ROUTE_NAME[k], citizens={h: int(round(lat[k][h])) for h in HOSTS},
                             officers={h: officers(lat[k][h]) for h in HOSTS}) for k in KEYS}
    extra = {"direct": "each host's 2021 census count and its own tables to 1 January 2024, taken as the latest figure",
             "mirror": "the larger of the two reports of every flow, the last three years repeated",
             "rigorous": "shares scaled so the fullest recorder is complete"}
    for k, name in extra.items():
        v = {h: mem[h]["routes"][k] for h in HOSTS}
        fig["routes"][k] = dict(name=name, citizens={h: int(round(v[h])) for h in HOSTS}, officers={h: officers(v[h]) for h in HOSTS})
    mean = {h: C.chain(R, h, {"a_mode": "mean"})["n"] for h in HOSTS}
    fig["routes"]["mean"] = dict(name="shares scaled about their own average", citizens={h: int(round(mean[h])) for h in HOSTS},
                                 officers={h: officers(mean[h]) for h in HOSTS})
    fig["routes_left"] = {k: {h: int(round(figs["L-" + h]["lattice"][k])) for h in HOSTS} for k in KEYS}
    fig["route_officer_totals"] = {k: int(sum(v["officers"].values())) for k, v in fig["routes"].items()}
    fig["routes_c"] = {c: {k: round(float(figs[c]["lattice"][k]), 2) for k in KEYS} for c in ("C1", "C2", "C3")}
    fig["rigorous_c"] = {c: round(float(figs[c]["routes"]["rigorous"]), 2) for c in ("C1", "C2", "C3")}
    fig["rigorous_home_share_pct"] = round(100.0 * f["a_home"] / max(f["a"].values()), 1)
    fig["hurried"] = dict(c1=round(float(figs["C1"]["lattice"][REFLEX]), 1), c2=round(float(figs["C2"]["lattice"][REFLEX]), 1),
                          c3=round(float(figs["C3"]["lattice"][REFLEX]), 2))
    # --- the referee and the held-out years
    rf = spec["referee"]
    fig["referee"] = dict(count=int(rf["truth"]), golden=int(round(rf["golden"])), off=int(round(abs(rf["golden"] - rf["truth"]))),
                          rivals={k: dict(value=int(round(v)), off=int(round(abs(v - rf["truth"])))) for k, v in rf["rivals"].items()})
    v = C.chain(R, C.REFHOST, {"a_mode": "mean"}, REF)["n"]
    fig["referee"]["rivals"]["shares scaled about their own average"] = dict(value=int(round(v)), off=int(round(abs(v - rf["truth"]))))
    ref_fam = [C.chain(R, C.REFHOST, o, REF)["n"] for _, o in C.FAMILY if o.get("anchor") != "referee"]
    fig["referee"]["band"] = [int(v) for v in band_of(rf["golden"], ref_fam, 10)]
    fig["referee_citizens"] = fig["referee"]["golden"]
    hold = {}
    for h in HOSTS:
        inn = R["recA"][HOME, h][:LAST] / G[h]["a"]
        br = R["recD"][HOME, h][:10].sum() / inn[:10].sum()
        hold[h] = dict(arrivals=int(round(inn[10:LAST].sum())), register_scaled=int(round(R["recD"][HOME, h][10:LAST].sum() / br)),
                       carried=int(round(3.0 * inn[7:10].mean())))
    fig["held_out"] = hold
    # --- the battery and the forcing
    fam = {h: list(mem[h]["family"]) for h in HOSTS}
    n = len(C.FAMILY)
    fig["variants"] = n
    fig["variant_names"] = [name for name, _ in C.FAMILY]
    fig["family_calls_all_golden"] = all(call_of({h: fam[h][i] for h in HOSTS}) == fig["call"] for i in range(n))
    fig["variant_range"] = {h: [int(round(min(fam[h]))), int(round(max(fam[h])))] for h in HOSTS}
    near = min((min(abs(fam[h][i] - C.STD * round(fam[h][i] / C.STD)), abs(fam[h][i] - C.STD * round(fam[h][i] / C.STD))), h,
                C.FAMILY[i][0], fam[h][i]) for h in HOSTS for i in range(n))
    fig["nearest_variant"] = dict(distance=int(round(near[0])), host=near[1], variant=near[2], citizens=int(round(near[3])))
    rows, sp = C.forcing_rows(R)
    fig["perturbations"] = [dict(input=name, call_holds=call_of(v) == fig["call"], citizens={h: int(round(v[h])) for h in HOSTS})
                            for name, v in rows]
    fig["spreads_pct"] = {h: {k: round(100.0 * v, 2) for k, v in sp[h].items()} for h in HOSTS}
    # --- the world's own numbers, for the checks (never shipped)
    fig["truth"] = {h: int(round(mem[h]["truth"])) for h in HOSTS}
    fig["truth_left"] = {h: int(world["host"][h]["ex"][10:].sum()) for h in HOSTS}
    fig["truth_officers"] = {h: officers(mem[h]["truth"]) for h in HOSTS}
    # --- the core on the cut pack
    rws, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    fig["rubric"] = dict(level=level, fails=[r[0] + ": " + r[2] for r in rws if r[1] == "FAIL"],
                         one_lost={s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                         fixed_alone={s: round(earn["earn"][key(ALONE[s])], 1) for s in ("S1", "S2", "S3")},
                         reflex=round(earn["earn"][key(REFLEX)], 1), rigorous=round(earn["rigorous"], 1))
    fig["closure"] = closure(R, fig, G, f)
    m = R["meta"]
    fig["late_entries"] = dict(reach_days=int(m["lag_reach"]), over_reach_pct=round(m["lag_over_reach_pct"], 1), tail_moves=int(m["tail_moves"]),
                               outstanding=int(round(m["tail_outstanding"])), tail_days=int(m["lag_max"] - m["lag_reach"]))
    fig["stated"] = dict(order=["1.1", "2.1", "2.2", "2.3", "3.1", "4.1"], regulation=["2", "3", "4", "5", "6"],
                         order_no=14, order_year=2025, regulation_no=[7, 2009], twelve_months=12, board_meeting="18 March 2027",
                         cycle=[2027, 2029], windows=[[2014, 2023], [2016, 2023], [2019, 2023], [2011, 2020], [2021, 2023]],
                         census_dates=["1 January 2011", "1 January 2021", "1 January 2016", "1 January 2020"],
                         release="May 2026", months=24, c14="C-14", question=14)
    E, g_lost = effort(R, fig, spec)
    fig["result_grades"] = g_lost
    return R, fig, E, spec


def result_values(R, o, fig, cfn):
    g = {h: C.chain(R, h, o) for h in HOSTS}
    return {"R1": dict(fig["tabled_arrivals_2011_2023"]), "R2": float(cfn["C1"](o)), "R3": float(cfn["C2"](o)),
            "R4": float(C.chain(R, C.REFHOST, {k: v for k, v in o.items() if k != "fwd"}, REF)["n"]),
            "R5": float(cfn["C3"](o)), "R6": {h: int(round(g[h]["n"])) for h in HOSTS},
            "R7": {h: int(round(g[h]["left"])) for h in HOSTS}, "R8": call_of({h: g[h]["n"] for h in HOSTS})}


def effort(R, fig, spec):
    lat_o = C.lattice_opts()

    def c2(o):
        return 100.0 if o.get("ex_level") == "recorded" else 100.0 * R["host"]["Skarholm"]["dep"][:10].sum() / C.chain(R, "Skarholm", o)["ex_p"]
    cfn = {"C1": lambda o: 100.0 * C.b_home(R, o), "C2": c2, "C3": lambda o: C.chain(R, "Tesmar", o)["late"]}
    gold = result_values(R, {}, fig, cfn)
    gold.update(R2=fig["c1"], R3=fig["c2"], R4=fig["referee_citizens"], R5=fig["c3"])
    careful = result_values(R, lat_o[REFLEX], fig, cfn)
    careful["R4"] = float(C.direct(R, C.REFHOST, REF))
    quick = {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None, "R6": dict(fig["census_2021"]), "R7": None,
             "R8": call_of({h: R["host"][h]["n21"] for h in HOSTS})}
    whole = ["N27", "L48", "N13"]
    meta = [
        ("R1", "both reports of every flow among the eight states, Orlava's register to 2026, the censuses and the vital "
               "events on one schema: each host's tabled arrivals of Orlavan citizens, 2011 to 2023", "Step-by-Step",
         "tabled_arrivals_2011_2023", [], "", {}, []),
        ("R2", "the recording shares: the share of Orlava's emigrants to the seven states, 2011 to 2023, who "
               "deregistered (per cent)", "Component 1", "c1", ["R1"],
         "Orlava's census table against its register; the two reports of every flow", dict(band=fig["c1_band"]), PREC["S1"]),
        ("R3", "each host's exits between its two censuses and the share its departures table holds: Skarholm's "
               "(per cent)", "Component 2", "c2", ["R1", "R2"], "the census pair, the arrivals and the vital events",
         dict(band=fig["c2_band"]), PREC["S2"]),
        ("R4", "Fenmark's count of 1 January 2016 reproduced from its 2011 census (citizens)", "Step-by-Step",
         "referee_citizens", ["R2", "R3"], "Fenmark's 2016 count", dict(band=fig["referee"]["band"]), ["L28", "L29", "L03"]),
        ("R5", "the home register's shares by host and the moves of 2024 to 2026: Tesmar's exits over those of 2021 to "
               "2023", "Component 3", "c3", ["R2", "R3"], "Orlava's register after 2023 against the years both report",
         dict(band=fig["c3_band"]), PREC["S3"]),
        ("R6", "citizens usually resident in each district on 1 January 2027", "Asks 2 to 8", "citizens", ["R2", "R3", "R5"], "",
         dict(bands={h: fig["citizens_band"][h] for h in HOSTS}, partly_share=0.5), whole),
        ("R7", "citizens who moved away from each district from the 2021 census to the end of 2026", "Asks 9 to 15", "left",
         ["R3", "R5"], "", dict(bands={h: fig["left_band"][h] for h in HOSTS}, partly_share=0.5), whole),
        ("R8", "the officers the Order gives each district", "Recommendation", "call", ["R6"], "", {}, whole),
    ]
    res = []
    for rid, name, graded, key, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(k):
        v = result_values(R, lat_o[k], fig, cfn)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(k) for k in KEYS}
    lat = spec["lattice"]
    said = {s: spec["stumps"][s]["said_out_loud"] for s in ("S1", "S2", "S3")}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = ALONE[s]
        judgments.append({"id": s, "name": STUMP_NAME[s], "kind": "stump", "precedent": PREC[s],
                          "dropped": {"answer": call_of(lat[s]), "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": call_of(lat[ak]),
                                    "results_rescued": [r for r, x in g_lost[ak].items() if x == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "the tables, the register and the censuses on one footing: three state codings to one, the "
                             "latest release of a table, a repeated register event counted once, the state read from "
                             "the clerk's text where the code is blank, the year of the move", "kind": "reflex",
         "precedent": ["R01", "R13"]},
        {"id": "J5", "name": "every file read, the two unused ones set aside", "kind": "reflex", "precedent": ["R02"]},
        {"id": "J6", "name": "a population at a date rebuilt from a count and the events after it, and checked against "
                             "the next count", "kind": "reflex", "precedent": ["R57", "R93"]},
        {"id": "J7", "name": "the establishment in force reproduced from the 2021 census counts", "kind": "reflex",
         "precedent": ["R18"]},
        {"id": "J8", "name": "several windows tried for a carried value, a hold-out on the latest years and a stress "
                             "on a fitted rate", "kind": "reflex", "precedent": ["R31", "R03", "R16"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat[REFLEX])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k])} for k in KEYS]
    for k in ("direct", "mirror", "rigorous"):
        routes.append({"name": fig["routes"][k]["name"], "answer": ["%s %d" % (h, fig["routes"][k]["officers"][h]) for h in HOSTS]})
    routes.append({"name": "the 2021 census counts carried", "answer": call_of({h: R["host"][h]["n21"] for h in HOSTS})})
    mem = spec["members"]
    fam_rows = [{"name": name, "answer": call_of({h: mem[h]["family"][i] for h in HOSTS})} for i, (name, _) in enumerate(C.FAMILY)]
    forcing = {"kind": "set", "golden_answer": fig["call"], "golden_family": fam_rows,
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": p["input"], "answer": ["%s %d" % (h, officers(p["citizens"][h])) for h in HOSTS]}
                                 for p in fig["perturbations"]]}
    hints = [{"sentence": said[s], "rescues": [r for r, x in g_lost[ALONE[s]].items() if x == "right" and r != "R1"]}
             for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


if __name__ == "__main__":
    import json
    R, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    code = corelib.run(spec)
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "result_grades", "referee", "truth")}, default=float))
    for h in HOSTS:
        print("%-9s citizens %6d %-16s officers %2d (in force %2d)  left %6d %-16s truth %6d %6d" % (
            h, fig["citizens"][h], fig["citizens_band"][h], fig["officers"][h], fig["officers_in_force"][h], fig["left"][h],
            fig["left_band"][h], fig["truth"][h], fig["truth_left"][h]))
    print("C1", fig["c1"], fig["c1_band"], "C2", fig["c2"], fig["c2_band"], "C3", fig["c3"], fig["c3_band"], "hurried", fig["hurried"])
    for x in fig["perturbations"]:
        print("%-62s %s" % (x["input"][:62], "same call" if x["call_holds"] else "CALL MOVES"))
    sys.exit(code)
