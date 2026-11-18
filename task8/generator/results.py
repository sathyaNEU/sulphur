"""Every owed figure, computed from the shipped pack: the golden route (the core's estimators on the loaded files),
the battery of conventions (the core's 98 and the ones the records add), the lattice of shortcuts, the direct and the
rigorous standard routes, the referee, the forcing rows, the rubric the core prices and the effort record."""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))
import core as C  # noqa: E402
import corelib  # noqa: E402
import effort as EF  # noqa: E402
import load as L  # noqa: E402

MEMBERS, BANKED, LINE = C.MEMBERS, C.BANKED, C.LINE
KEYS = C.lat_keys()
REFLEX = "S1+S2+S3"
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
STUMP_NAME = {
    "S1": "a moderator's recorded difference is a share of the difference a marker working without the centre's "
          "marks finds, measured board by board on the trial scripts joined to the live moderation of the same portfolio",
    "S2": "a centre's marks in the years between samples sit at the level its own mark sheets show for that year after "
          "a sample, within centre and net of the board's year",
    "S3": "each board's standard is placed against Carrow's through the moderators registered with two boards, each "
          "side taken to its own agreed marks",
}
ROUTE_NAME = {
    "S1": "the recorded difference taken as the difference",
    "S2": "a centre's last sample carried to the years it was not sampled",
    "S3": "each board's own principal taken as the standard",
    "S1+S2": "the recorded difference as the difference, the last sample carried",
    "S1+S3": "the recorded difference as the difference, each board's own principal as the standard",
    "S2+S3": "the last sample carried, each board's own principal as the standard",
    "S1+S2+S3": "the moderation record with the adjustments netted, candidate weights and the last sample carried",
}
PREC = {"S1": ["L28", "L22"], "S2": ["N13", "L37"], "S3": ["N27", "L06"]}
WORD = {1: "down", 0: "as banked", -1: "up"}


# ---------------------------------------------------------------- the conventions the records add to the battery
def _with(world, **arrays):
    """A copy of the loaded world with some of every board's arrays replaced."""
    B = {b: dict(w, **{k: f(b, w) for k, f in arrays.items()}) for b, w in world["B"].items()}
    return dict(world, B=B, cache={})


def x_centred(world):
    return _with(world, ex_x=lambda b, w: w["ex_x"] + float(np.mean(w.get("gap_all", w["ex_gap"]))))


def x_agreed(world):
    return _with(world, ex_x=lambda b, w: w["ex_x"] + w.get("gap_all", w["ex_gap"]))


def d_loo(world):
    return dict(world, D=[dict(l, ra=l["ra_loo"], rb=l["rb_loo"]) for l in world["D"]], cache={})


def d_recent(world):
    return dict(world, D=[dict(l, ra=l["ra"][l["year"] >= 2023], rb=l["rb"][l["year"] >= 2023]) for l in world["D"]],
                cache={})


def d_shortest(world):
    """One link a board: Ardkeel, Brannock and Gortavale with Carrow, Dunmoyle with Ardkeel, Eskerry with Brannock,
    Fennor with Gortavale (each board's link with the most people on a shortest path to Carrow)."""
    want = [("Ardkeel", "Carrow"), ("Brannock", "Carrow"), ("Gortavale", "Carrow"), ("Dunmoyle", "Ardkeel"),
            ("Eskerry", "Brannock"), ("Fennor", "Gortavale")]
    first = [l for pq in want for l in world["D"] if (l["a"], l["b"]) == pq]
    return dict(world, D=first + [l for l in world["D"] if (l["a"], l["b"]) not in want], cache={})


def gap_recent(world):
    return _with(world, gap_all=lambda b, w: w.get("gap_all", w["ex_gap"]),
                 ex_gap=lambda b, w: w.get("gap_all", w["ex_gap"])[w["ex_year"] >= 2020])


def ratio_scale(world, centred=True, first=None):
    """The share as the mean live difference over the mean cold difference (the consensus centred on the agreed
    marks, or as marked), on every meeting or on those from `first` on, expressed as a scale on the fitted share."""
    base = C.pulls(world, {})
    out = {}
    for b, w in world["B"].items():
        k = np.ones(len(w["ex_x"]), bool) if first is None else w["ex_year"] >= first
        out[b] = float(np.mean(w["ex_y"][k]) / np.mean(w["ex_x"][k] + (np.mean(w["ex_gap"][k]) if centred else 0.0))) / base[b]
    return out


def own_mark_share(world, raw):
    """The share fitted on the live moderator's own mark of the same script at the next meeting (made without the
    centre's marks) in place of the team's consensus, on the scripts that moderator marked; and, on the same scripts,
    the slope of the difference from the consensus on the difference from that one mark (how well one marker's mark
    measures the difference)."""
    out = {}
    for b in world["B"]:
        j = raw[b]["joined"].merge(raw[b]["trial"][["meeting", "script", "moderator", "mark"]],
                                   on=["meeting", "script", "moderator"])
        xo = (j["centre_mark"] - j["mark"]).to_numpy(float)
        xc = (j["centre_mark"] - j["mean"]).to_numpy(float)
        y = (j["centre_mark"] - j["moderator_mark"]).to_numpy(float)
        xm = xo - xo.mean()
        out[b] = dict(n=int(len(j)), share=float(np.sum(xm * (y - y.mean())) / np.sum(xm * xm)),
                      rel=float(np.sum(xm * (xc - xc.mean())) / np.sum(xm * xm)))
    return out


def recent_scale(world, first):
    """The share fitted on the meetings from `first` on, as a scale on the share fitted on every meeting."""
    base = C.pulls(world, {})
    out = {}
    for b, w in world["B"].items():
        k = w["ex_year"] >= first
        out[b] = C.slope(w["ex_x"][k], w["ex_y"][k], "ols", w["P"]["nm"]) / base[b]
    return out


def g_by_moderator(world, raw):
    """Each sample's recorded difference rescaled so it is divided by its own moderator's share (fitted on the
    scripts that moderator sampled live, ten or more, and shrunk to the board's by the spread between moderators
    beyond their own sampling error) in place of the board's."""
    base = C.pulls(world, {})
    B, spread = {}, {}
    for b, w in world["B"].items():
        sc = raw[b]["joined"]
        x = (sc["centre_mark"] - sc["mean"]).to_numpy(float)
        y = (sc["centre_mark"] - sc["moderator_mark"]).to_numpy(float)
        mod = sc["moderator"].to_numpy()
        est = {}
        for m in np.unique(mod):
            k = mod == m
            if k.sum() < 10:
                continue
            xm, ym = x[k] - x[k].mean(), y[k] - y[k].mean()
            sl = float(np.sum(xm * ym) / np.sum(xm * xm))
            se2 = float(np.sum((ym - sl * xm) ** 2) / (k.sum() - 2) / np.sum(xm * xm))
            est[m] = (sl, se2)
        sl = np.array([v[0] for v in est.values()])
        se2 = np.array([v[1] for v in est.values()])
        tau2 = max(0.0, float(np.var(sl, ddof=1) - se2.mean())) if len(sl) > 2 else 0.0
        own = {m: (base[b] if tau2 == 0 else (v[0] / v[1] + base[b] / tau2) / (1 / v[1] + 1 / tau2)) for m, v in est.items()}
        G = w["G"].copy()
        for (ci, ti), m in raw[b]["who"].items():
            G[ci, ti] = G[ci, ti] * base[b] / own.get(m, base[b])
        B[b] = dict(w, G=G)
        spread[b] = dict(moderators=len(est), between=round(float(np.sqrt(tau2)), 3))
    return dict(world, B=B, cache={}), spread


def awarded_cycle(world):
    """The levels after a sample fitted on the awarded marks in place of the centre's own."""
    return _with(world, mbar=lambda b, w: w["mbar"] - w["adj"])


def awarded_base(world, g):
    """The same estimate with the awarded mark as the base throughout: a centre between samples is placed at its last
    sample net of the adjustment applied then, plus the level after a sample fitted on the awarded marks."""
    wa = awarded_cycle(world)
    by = {y: {} for y in BANKED}
    theta = {}
    for b in MEMBERS:
        w = world["B"][b]
        k, pl, off = w["P"]["k"], g["parts"][b]["pull"], g["parts"][b]["off"]
        th = C.phase_effects(wa, b, {})
        theta[b] = th
        lam_hat = w["G"] / pl
        for y in BANKED:
            ti = C.YEARS.index(y)
            s = w["samp"][:, ti]
            res = np.where(s, np.nan_to_num(lam_hat[:, ti]) - w["adj"][:, ti], 0.0)
            for back in range(1, k):
                m = w["samp"][:, ti - back] & ~s
                res = np.where(m, np.nan_to_num(lam_hat[:, ti - back]) - w["adj"][:, ti - back] + th[back], res)
            n = w["ncand"][:, ti]
            by[y][b] = off + float(np.sum(n * res) / n.sum())
    pool = {b: v for b, v in C.pooled(dict(world, B={b: world["B"][b] for b in MEMBERS}), by).items()}
    return dict(by=by, pool=pool, nat=C.national(world, pool), theta=theta)


def review_calibration(world):
    """The review used as a calibration set: the share and the standard read off the referee board's centres sampled
    in the review's series (the recorded difference against the review's) and carried to every joining board."""
    rb, ry = C.REFEREE
    w = world["B"][rb]
    ti = C.YEARS.index(ry)
    s = w["samp"][:, ti]
    d, g = world["review"][s], w["G"][s, ti]
    dm, gm = d - d.mean(), g - g.mean()
    share = float(np.sum(dm * gm) / np.sum(dm * dm))
    standard = float(d.mean() - g.mean() / share)
    base, off = C.pulls(world, {}), C.offsets(world, {})
    o = {"pull_scale": {b: share / base[b] for b in world["B"]}, "off_shift": {b: standard - off[b] for b in world["B"]}}
    return share, standard, C.view(dict(world, cache={}), o)


EXTRA = {
    "pull": [("the share as the mean live difference over the mean cold difference, the consensus centred on the agreed marks",
              None, "ratio"),
             ("the share through the origin, the consensus centred on the agreed marks", x_centred, {"pull_how": "origin"}),
             ("the share fitted on the agreed marks in place of the consensus", x_agreed, {})],
    "link": [("each marker's own mark left out of the consensus they are read against", d_loo, {}),
             ("links on the 2023 to 2026 meetings", d_recent, {}),
             ("one link a board, on its shortest path to Carrow", d_shortest, {"link_tree": True})],
    "agreed": [("agreed marks against the consensus on the 2020 to 2026 meetings", gap_recent, {})],
}
# beside the battery (each stated range is widened only where one of these leaves it, to hold it): the share on recent
# meetings alone, fitted on the last five or four meetings with every form of the links and of the levels, or as a
# ratio of means on the agreed marks on the last six to three; and the levels on every series on file, alone and with
# each convention of another choice
FIFTEEN = ("the levels on all fifteen series", None, {"phase_years": 15})
RECENT = [("the share fitted on the last five meetings", "last5", ("ols", 5)),
          ("the share fitted on the last four meetings", "last4", ("ols", 4)),
          ("the share as a ratio of means on the agreed marks, the last six meetings", "ratio6", ("ratio", 6)),
          ("the share as a ratio of means on the agreed marks, the last five meetings", "ratio5", ("ratio", 5)),
          ("the share as a ratio of means on the agreed marks, the last four meetings", "ratio4", ("ratio", 4)),
          ("the share as a ratio of means on the agreed marks, the last three meetings", "ratio3", ("ratio", 3))]


def battery(world):
    """[(name, view)], [(name, view)]: the core's battery on the pack, each added convention, and each added
    convention with every convention of another choice; and, beside it, the share on recent meetings alone with
    every form of the links (and of the agreed marks) and every form of the levels."""
    out = [(n, C.view(world, o)) for n, o in C.VARIANTS]
    keep = {k: v for k, v in world["cache"].items() if k[0] == "phase"}
    rs = {"ratio": ratio_scale(world), "ratio_raw": ratio_scale(world, False)}
    for _, key, (how, n) in RECENT:
        rs[key] = recent_scale(world, C.Y1 - n + 1) if how == "ols" else ratio_scale(world, True, C.Y1 - n + 1)

    def run(steps):
        w, o = world, {}
        for _, f, opt in steps:
            if f is not None:
                w = f(w)
            if isinstance(opt, str):
                o["pull_scale"] = rs[opt]
            else:
                o.update(opt)
        w = dict(w, cache=dict(keep))
        return C.view(w, o)
    singles = [(dim, n, None, o) for dim, lst in C.DIMS.items() for n, o in lst]
    extras = [(dim, n, f, o) for dim, lst in EXTRA.items() for n, f, o in lst]
    for dim, n, f, o in extras:
        out.append((n, run([(n, f, o)])))
        for d2, n2, f2, o2 in singles + extras:
            if d2 == dim or (f2 is not None or isinstance(o2, str)) and (d2, n2) <= (dim, n):
                continue
            out.append((n + "; " + n2, run([(n, f, o), (n2, f2, o2)])))
    links = [(n, None, o) for dim in ("link", "agreed") for n, o in C.DIMS[dim]] + EXTRA["link"] + EXTRA["agreed"]
    levels = [(n, None, o) for dim in ("cycle", "carry") for n, o in C.DIMS[dim]] + [FIFTEEN]
    side = []
    for n, key, (how, _) in RECENT:
        for lk in ([None] + links) if how == "ols" else [None]:
            for lv in ([None] + levels) if how == "ols" else [None]:
                steps = [(n, None, key)] + [st for st in (lk, lv) if st is not None]
                side.append(("; ".join(st[0] for st in steps), run(steps)))
    side.append((FIFTEEN[0], run([FIFTEEN])))
    for d2, n2, f2, o2 in singles + extras:
        if d2 != "cycle":
            side.append((FIFTEEN[0] + "; " + n2, run([FIFTEEN, (n2, f2, o2)])))
    return out, side


# ---------------------------------------------------------------- helpers
def call_of(pool):
    return ["%s %s" % (b, WORD[C.band(pool[b])]) for b in MEMBERS]


def band_of(golden, family, step):
    """The family's range and a quarter of its width each side, rounded outward to the stated precision."""
    lo, hi = min(family + [golden]), max(family + [golden])
    lo, hi = lo - corelib.BAND_ROOM * (hi - lo), hi + corelib.BAND_ROOM * (hi - lo)
    return [round(float(np.floor(lo / step + 1e-9) * step), 6), round(float(np.ceil(hi / step - 1e-9) * step), 6)]


def held(band, vals, pad=0.0, step=0.1):
    """A range widened, where a reading beside the battery leaves it, to hold that reading at the stated precision
    (no quarter of the width is added: a reading the filed text refuses sits 0.15 marks beyond Gortavale's)."""
    lo, hi = min(vals) - pad, max(vals) + pad
    return [min(band[0], round(float(np.floor(lo / step + 1e-9) * step), 6)),
            max(band[1], round(float(np.ceil(hi / step - 1e-9) * step), 6))]


def centre_level(world, parts):
    """Each centre's estimated distance from Carrow's standard in each banked series (the golden's conventions)."""
    out = {}
    for b in MEMBERS:
        w = world["B"][b]
        k, th, pl, off = w["P"]["k"], parts[b]["theta"], parts[b]["pull"], parts[b]["off"]
        lam_hat = w["G"] / pl
        for y in BANKED:
            ti = C.YEARS.index(y)
            s = w["samp"][:, ti]
            res = np.where(s, np.nan_to_num(lam_hat[:, ti]) - w["adj"][:, ti], 0.0)
            for back in range(1, k):
                m = w["samp"][:, ti - back] & ~s
                res = np.where(m, np.nan_to_num(lam_hat[:, ti - back]) + th[back], res)
            out[b, y] = dict(est=off + res, n=w["ncand"][:, ti].astype(int), sampled=s)
    return out


def referee_family(world, bat_worlds):
    return bat_worlds


def run(target):
    world, info, raw = L.load(target)
    WC = C.simulate()
    spec0, _ = C.build(WC)
    g = C.view(world)
    bat, side = battery(world)
    fam = [v for _, v in bat]
    sv = [v for _, v in side]
    lat = {k: C.view(world, C.lat_opts(k.split("+"))) for k in KEYS}
    dr_by, rg_by = C.direct(world), C.rigorous(world)
    dr, rg = C.pooled(world, dr_by), C.pooled(world, rg_by)
    tr_by = {y: C.truth_year(WC, y) for y in BANKED}
    tr = C.pooled(WC, tr_by)
    members = {b: dict(lines=[-LINE, LINE], truth=tr[b], golden=g["pool"][b], family=[f["pool"][b] for f in fam],
                       routes={"direct": dr[b], "rigorous": rg[b]}) for b in MEMBERS}
    # the share on recent meetings alone is run beside the battery, with every form of the links and of the levels
    # (crossed through the battery it would stretch every band by a quarter of the wider range): each stated range is
    # the battery's, widened only where one of these readings leaves it, to hold that reading
    recent = {n: C.view(dict(world, cache={}), {"pull_scale": recent_scale(world, first)})
              for n, first in (("five", C.Y1 - 4), ("four", C.Y1 - 3))}
    dband = {b: held(band_of(g["pool"][b], members[b]["family"], 0.1), [v["pool"][b] for v in sv]) for b in MEMBERS}
    yband = {y: {b: held(band_of(g["by"][y][b], [f["by"][y][b] for f in fam], 0.1), [v["by"][y][b] for v in sv])
                 for b in MEMBERS} for y in BANKED}
    wband = held(band_of(g["nat"], [f["nat"] for f in fam], 0.1), [v["nat"] for v in sv])
    c1band = held(band_of(g["pull"], [f["pull"] for f in fam], 0.1), [v["pull"] for v in sv], 0.15)
    c2band = held(band_of(g["cycle"], [f["cycle"] for f in fam], 0.1), [v["cycle"] for v in sv])
    c3band = held(band_of(g["link"], [f["link"] for f in fam], 0.1), [v["link"] for v in sv])
    figs = [dict(id="C1 share recorded, %s" % C.PULL_BOARD, block="component", golden=g["pull"], band=c1band,
                 family=[f["pull"] for f in fam], lattice={k: v["pull"] for k, v in lat.items()}, routes={"rigorous": 100.0}),
            dict(id="C2 year after a sample, %s" % C.CYCLE_BOARD, block="component", golden=g["cycle"], band=c2band,
                 family=[f["cycle"] for f in fam], lattice={k: v["cycle"] for k, v in lat.items()}, routes={"rigorous": 0.0}),
            dict(id="C3 standard against Carrow, %s" % C.LINK_BOARD, block="component", golden=g["link"], band=c3band,
                 family=[f["link"] for f in fam], lattice={k: v["link"] for k, v in lat.items()}, routes={"rigorous": 0.0})]
    for b in MEMBERS:
        figs.append(dict(id="A1 %s" % b, block="ask", member=b, band=dband[b]))
    for y in BANKED:
        for b in MEMBERS:
            figs.append(dict(id="A2 %s %d" % (b, y), block="ask", golden=g["by"][y][b], family=[f["by"][y][b] for f in fam],
                             band=yband[y][b],
                             lattice={k: v["by"][y][b] for k, v in lat.items()}, routes={"rigorous": rg_by[y][b]}))
    figs.append(dict(id="A3 six boards", block="ask", golden=g["nat"], family=[f["nat"] for f in fam], band=wband,
                     lattice={k: v["nat"] for k, v in lat.items()}, routes={"rigorous": C.national(world, rg)}))
    ref = C.referee(world)
    spec = dict(task="task8 architecture 20 (the cut pack)", call="lines", members=members,
                lattice={k: {b: v["pool"][b] for b in MEMBERS} for k, v in lat.items()}, referee=ref,
                stumps=spec0["stumps"], figures=figs)
    x = dict(g=g, fam=fam, lat=lat, dr=dr, rg=rg, rg_by=rg_by, tr=tr, tr_by=tr_by)

    r1, r2 = (lambda v: round(float(v), 1)), (lambda v: round(float(v), 2))
    fig = {}
    fig["distance"] = {b: r1(g["pool"][b]) for b in MEMBERS}
    fig["distance_2dp"] = {b: r2(g["pool"][b]) for b in MEMBERS}
    fig["distance_band"] = dband
    fig["by_series"] = {str(y): {b: r1(g["by"][y][b]) for b in MEMBERS} for y in BANKED}
    fig["by_series_band"] = {str(y): yband[y] for y in BANKED}
    fig["whole"] = r1(g["nat"])
    fig["whole_2dp"] = r2(g["nat"])
    fig["whole_band"] = wband
    fig["side"] = {b: WORD[C.band(g["pool"][b])] for b in MEMBERS}
    fig["call"] = call_of(g["pool"])
    fig["converted"] = {b: abs(r1(g["pool"][b])) for b in MEMBERS if C.band(g["pool"][b])}
    fig["margin"] = {b: r2(min(abs(g["pool"][b] - LINE), abs(g["pool"][b] + LINE))) for b in MEMBERS}
    fig["line"] = LINE
    fig["c1"], fig["c1_band"] = r1(g["pull"]), c1band
    fig["c2"], fig["c2_band"] = r1(g["cycle"]), c2band
    fig["c3"], fig["c3_band"] = r1(g["link"]), c3band
    P = g["parts"]
    fig["share_pct"] = {b: r1(100 * P[b]["pull"]) for b in C.BOARDS}
    fig["cycle"] = {b: [r2(v) for v in P[b]["theta"][1:]] for b in C.BOARDS}
    fig["standard"] = {b: r2(P[b]["off"]) for b in C.BOARDS}
    fig["rota_years"] = {b: int(world["B"][b]["P"]["k"]) for b in C.BOARDS}
    fig["cycle_lower"] = {b: [abs(v) for v in fig["cycle"][b]] for b in C.BOARDS}
    # a centre's successive samples (the check the record passes on itself)
    pairs = []
    for b in MEMBERS:
        w = world["B"][b]
        for row, sm in zip(w["G"], w["samp"]):
            v = row[sm]
            pairs += list(zip(v[:-1], v[1:]))
    pairs = np.array(pairs)
    fig["successive_samples"] = dict(pairs=int(len(pairs)), correlation=r2(float(np.corrcoef(pairs[:, 0], pairs[:, 1])[0, 1])))
    # ---- the links: each pair's people, person-years and difference; each board's agreed marks against its consensus
    fig["links"] = [dict(a=l["a"], b=l["b"], person_years=int(len(l["ra"])), people=int(round(len(l["ra"]) / 7.0)),
                         difference=r2(float(np.mean(l["ra"] - l["rb"])))) for l in world["D"]]
    fig["agreed_gap"] = {b: r2(float(np.mean(world["B"][b]["ex_gap"]))) for b in C.BOARDS}
    fig["link_people_years"] = int(sum(len(l["ra"]) for l in world["D"]))
    # ---- counts and bases every route reaches (stated in the Step-by-Step only)
    ti = [C.YEARS.index(y) for y in BANKED]
    fig["centres"] = {b: int(world["B"][b]["ncand"].shape[0]) for b in C.BOARDS}
    fig["banked_candidates"] = {b: {str(y): int(world["B"][b]["ncand"][:, t].sum()) for y, t in zip(BANKED, ti)} for b in MEMBERS}
    fig["banked_total"] = int(sum(sum(v.values()) for v in fig["banked_candidates"].values()))
    fig["sampled_centres"] = {b: {str(y): int(world["B"][b]["samp"][:, t].sum()) for y, t in zip(BANKED, ti)} for b in MEMBERS}
    fig["sampled_portfolios"] = {b: int(sum(world["B"][b]["ns"][:, t].sum() for t in ti)) for b in MEMBERS}
    fig["recorded_mean"] = {b: r2(float(np.nanmean(world["B"][b]["G"][:, -6:][world["B"][b]["samp"][:, -6:]]))) for b in C.BOARDS}
    fig["adjusted_pct"] = {b: int(round(100 * float(np.mean(world["B"][b]["adj"][:, -6:][world["B"][b]["samp"][:, -6:]] != 0))))
                           for b in C.BOARDS}
    fig["trial_scripts"] = {b: int(info[b]["scripts"]) for b in C.BOARDS}
    fig["trial_markers"] = {b: int(round(info[b]["markers"])) for b in C.BOARDS}
    fig["mark_rows"] = {b: int(info[b]["rows"]) for b in C.BOARDS}
    fig["mark_rows_total"] = int(sum(fig["mark_rows"].values()))
    fig["repeat_rows"] = {b: int(info[b]["rows_raw"] - info[b]["rows"]) for b in C.BOARDS if info[b]["rows_raw"] != info[b]["rows"]}
    fig["review_portfolios"] = int(info["review_rows"])
    fig["appointments"], fig["two_board_people"], fig["board_pairs"] = info["appointments"], info["two_board_people"], len(info["pairs"])
    fig["files"] = dict(total=42, unused=3)
    # ---- every route
    def pooled_row(v):
        return {b: r2(v[b]) for b in MEMBERS}
    fig["routes"] = {k: dict(name=ROUTE_NAME[k], distance=pooled_row(lat[k]["pool"]), call=call_of(lat[k]["pool"]),
                             whole=r2(lat[k]["nat"])) for k in KEYS}
    fig["routes"]["direct"] = dict(name="each board's mean recorded difference on the portfolios sampled in 2025 and 2026",
                                   distance=pooled_row(dr), call=call_of(dr), whole=r2(C.national(world, dr)))
    # the standard route as the blocks and the workbook state it: every step in its words, nothing shrunk (the core
    # prices the same route with a centre's carried sample shrunk to the board's mean, kept beside it)
    rp = C.pooled(world, C.rigorous(world, shrink=False))
    fig["routes"]["rigorous"] = dict(name="each board's own meeting severity added to the record, adjustments netted, "
                                          "candidate weights, a centre between samples carried at its last sample",
                                     distance=pooled_row(rp), call=call_of(rp), whole=r2(C.national(world, rp)))
    fig["routes"]["rigorous_shrunk"] = dict(distance=pooled_row(rg), call=call_of(rg), whole=r2(C.national(world, rg)))
    fig["hurried"] = dict(c1=100, c2=0.0, c3=0.0, distance=pooled_row(lat[REFLEX]["pool"]), whole=r2(lat[REFLEX]["nat"]))
    fig["routes_by_series"] = {k: {str(y): {b: r2(lat[k]["by"][y][b]) for b in MEMBERS} for y in BANKED} for k in KEYS}
    # ---- the referee
    rb, ry = C.REFEREE
    ref_fam = [C.estimate(dict(world, cache={}), o, (ry,), "unsampled")[0][ry][rb] for _, o in C.VARIANTS]
    off = lambda v: r2(abs(r2(v) - r2(ref["truth"])))  # noqa: E731  (the difference of the figures as stated)
    fig["referee"] = dict(board=rb, series=ry, review=r2(ref["truth"]), golden=r2(ref["golden"]),
                          off=off(ref["golden"]), band=band_of(ref["golden"], ref_fam, 0.1),
                          rivals={k: dict(value=r2(v), off=off(v)) for k, v in dict(
                              ref["rivals"], rigorous=C.rigorous(world, (ry,), "unsampled", shrink=False)[ry][rb]).items()},
                          rigorous_shrunk=r2(ref["rivals"]["rigorous"]),
                          raw_all_centres=r2(C.review_raw(world)),
                          reflex=r2(C.estimate(world, C.lat_opts(REFLEX.split("+")), (ry,), "unsampled")[0][ry][rb]),
                          unsampled_centres=int((~world["B"][rb]["samp"][:, C.YEARS.index(ry)]).sum()))
    fig["referee_golden"] = fig["referee"]["golden"]
    fig["asks"] = dict(fig["distance"])
    fig["asks"].update({"%s %d" % (b, y): fig["by_series"][str(y)][b] for y in BANKED for b in MEMBERS})
    fig["asks"]["whole"] = fig["whole"]
    # ---- the battery and the forcing
    fig["variants"] = len(bat)
    fig["variant_names"] = [n for n, _ in bat]
    fig["family_calls_all_golden"] = all(call_of(f["pool"]) == fig["call"] for f in fam)
    fig["variant_range"] = {b: [r2(min(members[b]["family"])), r2(max(members[b]["family"]))] for b in MEMBERS}
    near = min((min(abs(f["pool"][b] - LINE), abs(f["pool"][b] + LINE)), b, n, f["pool"][b]) for n, f in bat for b in MEMBERS)
    fig["nearest_variant"] = dict(distance=r2(near[0]), board=near[1], variant=near[2], value=r2(near[3]))
    rows, sp = C.forcing_rows(world, x)
    fig["perturbations"] = [dict(input=nm, call_holds=bool(same), nearest=r2(d), board=b_, distance=pooled_row(v))
                            for nm, same, d, b_, v in rows]
    fig["spreads"] = {b: dict(share_pct=r1(100 * sp[b]["pull"]), cycle=r2(sp[b]["cycle"]), standard=r2(sp[b]["off"])) for b in MEMBERS}
    # ---- a rival outside the battery: the share as a plain ratio to the consensus as marked (no agreed marks)
    rr = C.view(dict(world, cache={}), {"pull_scale": ratio_scale(world, False)})
    cells = {b: rr["pool"][b] for b in MEMBERS}
    cells.update({"%s %d" % (b, y): rr["by"][y][b] for y in BANKED for b in MEMBERS})
    cells["whole"] = rr["nat"]
    bands = dict(fig["distance_band"])
    bands.update({"%s %d" % (b, y): fig["by_series_band"][str(y)][b] for y in BANKED for b in MEMBERS})
    bands["whole"] = fig["whole_band"]
    fig["rival_plain_ratio"] = dict(distance=pooled_row(rr["pool"]), call=call_of(rr["pool"]), whole=r2(rr["nat"]),
                                    share_pct={b: r1(100 * rr["parts"][b]["pull"]) for b in MEMBERS},
                                    outside=sorted(k for k, v in cells.items() if not bands[k][0] <= round(v, 1) <= bands[k][1]))
    # ---- three more rivals outside the battery, each ruled on by a figure
    def against_bands(v):
        cc = {b: v["pool"][b] for b in MEMBERS}
        cc.update({"%s %d" % (b, y): v["by"][y][b] for y in BANKED for b in MEMBERS})
        cc["whole"] = v["nat"]
        return sorted(k for k, val in cc.items() if not bands[k][0] <= round(val, 1) <= bands[k][1])
    fig["rival_recent_share"] = {n: dict(share_pct=r1(v["pull"]), distance=pooled_row(v["pool"]), call=call_of(v["pool"]),
                                         whole=r2(v["nat"]), outside=against_bands(v)) for n, v in recent.items()}
    ns_ = min((min(abs(v["pool"][b] - LINE), abs(v["pool"][b] + LINE)), b, n, v["pool"][b]) for n, v in side for b in MEMBERS)
    fig["beside"] = dict(rebuilds=len(side), names=[n for n, _ in side],
                         calls_all_golden=all(call_of(v["pool"]) == fig["call"] for v in sv),
                         share_pct=[r1(min(v["pull"] for v in sv)), r1(max(v["pull"] for v in sv))],
                         range={b: [r2(min(v["pool"][b] for v in sv)), r2(max(v["pool"][b] for v in sv))] for b in MEMBERS},
                         nearest=dict(distance=r2(ns_[0]), board=ns_[1], reading=ns_[2], value=r2(ns_[3])),
                         ratio_share_pct=[r1(min(v["pull"] for n, v in side if n.startswith("the share as a ratio"))),
                                          r1(max(v["pull"] for n, v in side if n.startswith("the share as a ratio")))],
                         fifteen_level=r2(abs(dict(side)[FIFTEEN[0]]["cycle"])),
                         crossed=sum(1 for n, _ in side if n.startswith("the share fitted on the last")),
                         outside=sorted(set(k for v in sv for k in against_bands(v))))
    # ---- the paired design the pack affords on one marker: refused by the review and by that mark's own noise
    om, base_ = own_mark_share(world, raw), C.pulls(world, {})
    o_own = {"pull_scale": {b: om[b]["share"] / base_[b] for b in world["B"]}}
    o_cor = {"pull_scale": {b: om[b]["share"] / om[b]["rel"] / base_[b] for b in world["B"]}}
    vo, vk = C.view(dict(world, cache={}), o_own), C.view(dict(world, cache={}), o_cor)
    ro_ = C.estimate(dict(world, cache={}), o_own, (ry,), "unsampled")[0][ry][rb]
    fig["rival_own_mark"] = dict(scripts={b: om[b]["n"] for b in MEMBERS}, share_pct={b: r1(100 * om[b]["share"]) for b in MEMBERS},
                                 distance=pooled_row(vo["pool"]), call=call_of(vo["pool"]),
                                 boards_wrong=[b for b in MEMBERS if C.band(vo["pool"][b]) != C.band(g["pool"][b])],
                                 referee=r2(ro_), referee_off=off(ro_),
                                 reliability={b: r2(om[b]["rel"]) for b in MEMBERS},
                                 corrected_share_pct={b: r1(100 * om[b]["share"] / om[b]["rel"]) for b in MEMBERS},
                                 corrected_distance=pooled_row(vk["pool"]), corrected_call=call_of(vk["pool"]),
                                 corrected_outside=against_bands(vk),
                                 marks_a_script=[int(min(info[b]["count_min"] for b in C.BOARDS)),
                                                 int(max(info[b]["count_max"] for b in C.BOARDS))])
    wm, sp_m = g_by_moderator(world, raw)
    vm = C.view(wm)
    fig["rival_share_by_moderator"] = dict(distance=pooled_row(vm["pool"]), call=call_of(vm["pool"]), whole=r2(vm["nat"]),
                                           outside=against_bands(vm), moderators={b: sp_m[b]["moderators"] for b in MEMBERS},
                                           between={b: sp_m[b]["between"] for b in MEMBERS})
    wa = awarded_cycle(world)
    va = C.view(wa)
    ra_ = C.estimate(wa, {}, (ry,), "unsampled")[0][ry][rb]
    fig["rival_cycle_on_awarded"] = dict(distance=pooled_row(va["pool"]), call=call_of(va["pool"]), whole=r2(va["nat"]),
                                         outside=against_bands(va), first_year={b: r2(va["parts"][b]["theta"][1]) for b in MEMBERS},
                                         referee=r2(ra_), referee_off=off(ra_))
    vb = awarded_base(world, g)
    fig["rival_awarded_base"] = dict(distance=pooled_row(vb["pool"]), call=call_of(vb["pool"]), whole=r2(vb["nat"]),
                                     outside=against_bands(vb), first_year={b: r2(vb["theta"][b][1]) for b in MEMBERS})
    sh_, st_, vc = review_calibration(world)
    fig["rival_review_calibration"] = dict(share_pct=r1(100 * sh_), standard=r2(st_), distance=pooled_row(vc["pool"]),
                                           call=call_of(vc["pool"]), whole=r2(vc["nat"]),
                                           boards_wrong=[b for b in MEMBERS if C.band(vc["pool"][b]) != C.band(g["pool"][b])])
    # ---- two readings the filed text refuses, each with its figures
    zero = lambda only: _with(world, ex_gap=lambda b, w: np.zeros_like(w["ex_gap"]) if (only is None or b == only) else w["ex_gap"])  # noqa: E731
    vc1, vc2 = C.view(zero(C.REF)), C.view(zero(None))
    fig["rival_consensus_standard"] = dict(carrow_only=pooled_row(vc1["pool"]), every_board=pooled_row(vc2["pool"]),
                                           call_carrow_only=call_of(vc1["pool"]), call_every_board=call_of(vc2["pool"]),
                                           carrow_gap=fig["agreed_gap"][C.REF])
    vn = C.view(_with(world, adj=lambda b, w: np.zeros_like(w["adj"])))
    fig["rival_no_netting"] = dict(distance=pooled_row(vn["pool"]), call=call_of(vn["pool"]),
                                   boards_wrong=[b for b in MEMBERS if C.band(vn["pool"][b]) != C.band(g["pool"][b])])
    # ---- the nearest the further readings that keep the outcomes come to a tolerance
    further = [("the plain ratio", rr["pool"]), ("the share by moderator", vm["pool"]), ("the awarded base", vb["pool"]),
               ("the last five meetings", recent["five"]["pool"]), ("the last four meetings", recent["four"]["pool"])]
    nf = min((min(abs(v[b] - LINE), abs(v[b] + LINE)), b, n) for n, v in further for b in MEMBERS)
    fig["nearest_further"] = dict(distance=r2(nf[0]), board=nf[1], reading=nf[2])
    fig["all_rebuilds"] = fig["variants"] + fig["beside"]["rebuilds"]
    fig["nearest_any"] = min((fig["nearest_variant"], fig["beside"]["nearest"]), key=lambda d: d["distance"])
    # ---- the world's own values, for the checks (never shipped)
    fig["truth"] = {b: r2(tr[b]) for b in MEMBERS}
    fig["truth_call"] = call_of(tr)
    # ---- the core on the cut pack
    rws, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))  # noqa: E731
    fig["rubric"] = dict(level=level, fails=[r[0] + ": " + r[2] for r in rws if r[1] == "FAIL"],
                         one_lost={s: round(earn["earn"][key(s)], 1) for s in C.SIDS},
                         fixed_alone={s: round(earn["earn"][key(ALONE[s])], 1) for s in C.SIDS},
                         reflex=round(earn["earn"][key(REFLEX)], 1), rigorous=round(earn["rigorous"], 1))
    fig["stated"] = dict(clauses=[2.1, 2.3, 3.1, 4.1, 4.2, 5.1, 5.2, 3.3, 3.4, 4.5, 5.3, 5.4, 5.5], tolerance=2.0, series=[2025, 2026], awards="June 2027",
                         register_from=2020, meetings=[2015, 2026], sheets=[2012, 2026], review_per_centre=8, nine=9)
    cl = centre_level(world, P)
    for b in MEMBERS:
        for y in BANKED:
            c = cl[b, y]
            assert abs(float(np.sum(c["n"] * c["est"]) / c["n"].sum()) - g["by"][y][b]) < 1e-9
    fig["csv_rows"] = int(sum(len(v["est"]) for v in cl.values()))
    E, g_lost = effort(world, fig, spec, x, ref_fam)
    fig["result_grades"] = g_lost
    return dict(world=world, info=info, raw=raw, x=x, bat=bat, centre=cl, core=WC), fig, E, spec


def result_values(world, o, fig):
    v = C.view(world, o)
    rb, ry = C.REFEREE
    cells = {b: float(v["pool"][b]) for b in MEMBERS}
    for y in BANKED:
        for b in MEMBERS:
            cells["%s %d" % (b, y)] = float(v["by"][y][b])
    cells["whole"] = float(v["nat"])
    return {"R1": dict(fig["recorded_mean"]), "R2": float(v["pull"]), "R3": float(v["cycle"]), "R4": float(v["link"]),
            "R5": float(C.estimate(world, o, (ry,), "unsampled")[0][ry][rb]), "R6": cells, "R7": call_of(v["pool"])}


def effort(world, fig, spec, x, ref_fam):
    gold = result_values(world, {}, fig)
    gold.update(R2=fig["c1"], R3=fig["c2"], R4=fig["c3"], R5=fig["referee_golden"], R6=dict(fig["asks"]))  # as the blocks state them
    careful = result_values(world, C.lat_opts(REFLEX.split("+")), fig)
    dr_by = C.direct(world)
    dr = C.pooled(world, dr_by)
    qcells = {b: float(dr[b]) for b in MEMBERS}
    for y in BANKED:
        for b in MEMBERS:
            qcells["%s %d" % (b, y)] = float(dr_by[y][b])
    qcells["whole"] = float(C.national(world, dr))
    quick = {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None, "R6": qcells, "R7": call_of(dr)}
    bands = {b: fig["distance_band"][b] for b in MEMBERS}
    for y in BANKED:
        for b in MEMBERS:
            bands["%s %d" % (b, y)] = fig["by_series_band"][str(y)][b]
    bands["whole"] = fig["whole_band"]
    whole = ["N13", "N27", "L28"]
    meta = [
        ("R1", "the seven boards' moderation samples, outcomes, rota years and mark sheets on one schema: each board's "
               "mean recorded difference on the samples of 2021 to 2026 (marks)", "Step-by-Step", "recorded_mean", [], "", {}, []),
        ("R2", "the share of a difference found without the centre's marks that each board's moderators record: "
               "Ardkeel's (per cent)", "Component 1", "c1", ["R1"],
         "each trial script's centre mark and consensus against the live moderator's mark of the same portfolio",
         dict(band=fig["c1_band"]), PREC["S1"]),
        ("R3", "the level of a centre's marks by years since its last sample: Fennor's centres one year after a sample "
               "(marks)", "Component 2", "c2", ["R1"], "the mark sheets by centre and year against the rota years",
         dict(band=fig["c2_band"]), PREC["S2"]),
        ("R4", "each board's standard against Carrow's: Gortavale's (marks)", "Component 3", "c3", ["R1"],
         "the moderators registered with two boards on both boards' meetings; each board's agreed marks",
         dict(band=fig["c3_band"]), PREC["S3"]),
        ("R5", "the regulator's 2023 review of Dunmoyle reproduced on the centres not sampled that year (marks)",
         "Step-by-Step", "referee_golden", ["R2", "R3", "R4"], "the review's marks", dict(band=fig["referee"]["band"]),
         ["L28", "N13", "N27"]),
        ("R6", "each joining board's banked marks against Carrow's standard, together and by series, and the joining "
               "boards as a whole (marks)", "Asks 1 to 19", "asks", ["R2", "R3", "R4"], "",
         dict(bands=bands, partly_share=0.5), whole),
        ("R7", "the boards the protocol converts and the direction", "Recommendation", "call", ["R6"], "", {}, whole),
    ]
    res = []
    for rid, name, graded, key_, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key_, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(k):
        v = result_values(world, C.lat_opts(k.split("+")), fig)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(k) for k in KEYS}
    lat = spec["lattice"]
    said = {s: spec["stumps"][s]["said_out_loud"] for s in C.SIDS}
    judgments = []
    for s in C.SIDS:
        ak = ALONE[s]
        judgments.append({"id": s, "name": STUMP_NAME[s], "kind": "stump", "precedent": PREC[s],
                          "dropped": {"answer": call_of(lat[s]), "results_moved": [r for r, v in g_lost[s].items() if v != "right"]},
                          "alone": {"answer": call_of(lat[ak]),
                                    "results_rescued": [r for r, v in g_lost[ak].items() if v == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "seven layouts on one schema: centres by national roll number, a reissued moderation record "
                             "replaced by the later one, a batch loaded twice counted once, withdrawn and absent entries "
                             "left out, blank trial marks left out", "kind": "reflex", "precedent": ["R01", "R13"]},
        {"id": "J5", "name": "every file read, the three unused ones set aside", "kind": "reflex", "precedent": ["R02"]},
        {"id": "J6", "name": "the applied adjustments netted and every centre weighted by its candidates", "kind": "reflex",
         "precedent": ["R18"]},
        {"id": "J7", "name": "a severity for each board's moderators from its own meeting, small samples shrunk, a "
                             "stability check on a centre's successive samples", "kind": "reflex",
         "precedent": ["R31", "R03", "R16"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat[REFLEX])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k])} for k in KEYS]
    for k in ("direct", "rigorous"):
        routes.append({"name": fig["routes"][k]["name"], "answer": fig["routes"][k]["call"]})
    mem = spec["members"]
    n = len(fig["variant_names"])
    fam_rows = [{"name": fig["variant_names"][i], "answer": call_of({b: mem[b]["family"][i] for b in MEMBERS})} for i in range(n)]
    forcing = {"kind": "set", "golden_answer": fig["call"], "golden_family": fam_rows,
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": p["input"], "answer": call_of(p["distance"])} for p in fig["perturbations"]]}
    hints = [{"sentence": said[s], "rescues": [r for r, v in g_lost[ALONE[s]].items() if v == "right" and r != "R1"]}
             for s in C.SIDS]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


if __name__ == "__main__":
    import json
    X, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    code = corelib.run(spec)
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "referee", "truth", "variants")}, default=float))
    for b in MEMBERS:
        print("%-10s %5.2f %-14s 2025 %5.1f %-14s 2026 %5.1f %-14s truth %5.2f  share %5.1f  standard %6.2f  cycle %s" % (
            b, fig["distance_2dp"][b], fig["distance_band"][b], fig["by_series"]["2025"][b], fig["by_series_band"]["2025"][b],
            fig["by_series"]["2026"][b], fig["by_series_band"]["2026"][b], fig["truth"][b], fig["share_pct"][b],
            fig["standard"][b], fig["cycle"][b]))
    print("whole", fig["whole_2dp"], fig["whole_band"], "C1", fig["c1"], fig["c1_band"], "C2", fig["c2"], fig["c2_band"],
          "C3", fig["c3"], fig["c3_band"])
    for p in fig["perturbations"]:
        print("%-46s %s nearest %.2f %s" % (p["input"], "same call" if p["call_holds"] else "CALL MOVES", p["nearest"], p["board"]))
    sys.exit(code)
