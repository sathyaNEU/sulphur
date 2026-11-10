"""task10 architecture 6: the effort test's passes and the shortcut routes, each computed end to end on the pack by
the generator's own implementations of named methods (nothing here reads the prompt).

  quick      ten minutes: the contracted megawatts at face value, taken off the highest half-hour on record grown
             to 2027/28; no measurement, no range
  careful    an afternoon, the platform runs' own method on this world (architecture 5, both rounds), graded up
             where the record leaves a doubt: every file cleaned, the logged switching days left out, the demand
             side as the guideline files it, each event measured against a weather-adjusted baseline, megawatts
             delivered per megawatt scheduled regressed on temperature zone by zone and read at minus 3.0 C, that
             rate applied to the megawatts contracted, the credit taken off the 17:30 to 18:00 peak, the
             one-day-in-ten level from the megawatts of scatter its own fit leaves on the freezing days (carried
             unchanged to the award) with the demand's day-to-day spread, and the same model back-tested on the
             last winter
  thorough   the golden
"""
import math

import numpy as np
import pandas as pd

import estim as E

NAMES = None


def _ols(B, y):
    beta, *_ = np.linalg.lstsq(B, y, rcond=None)
    resid = y - B @ beta
    s2 = float(resid @ resid) / max(len(y) - B.shape[1], 1)
    cov = s2 * np.linalg.inv(B.T @ B)
    return beta, cov, resid


def careful(X, G):
    """The careful but hurried pass, zone by zone."""
    out = {}
    tr_w, te_w = E.TRAIN_WINTERS, E.TEST_WINTER
    abs_err, n_in, n_in_fit, n_cold, n_all = [], 0, 0, 0, 0
    for z in G["zones"]:
        c = z["code"]
        ev = G["events"][c]
        s = ev["scheduled"].values.astype(float)
        T = ev["T"].values
        B = np.column_stack([s, s * T])
        beta, cov, resid = _ols(B, ev["delivered"].values.astype(float))
        frz = T < E.FREEZING
        sd_mw = float(np.std(resid[frz], ddof=2))           # megawatts of scatter on the freezing days of its own fit
        rel = float(np.std((resid / np.maximum(B @ beta, 1e-9))[frz], ddof=2))
        a = np.array([1.0, E.T_DESIGN])
        rate = float(a @ beta)
        se_rate = math.sqrt(float(a @ cov @ a))
        delivered = rate * z["award"]
        peak = z["before"] - delivered                      # the credit taken off the 17:30 to 18:00 peak
        base_sd = z["cv_base"] * z["before"]                # the demand's own day-to-day spread, megawatts
        hi = peak + E.Z90 * math.sqrt(sd_mw ** 2 + base_sd ** 2)       # the megawatts of scatter carried unchanged
        hi_fit = peak + E.Z90 * math.sqrt((se_rate * z["award"]) ** 2 + (base_sd / math.sqrt(max(z["n_base_days"], 1))) ** 2)
        hi_rel = peak + E.Z90 * math.sqrt((rel * delivered) ** 2 + base_sd ** 2)
        out[z["primary"]] = dict(before=z["before"], rate=rate, delivered=delivered, peak_hh="18:00", peak=peak,
                                 off_peak=delivered, one_in_ten=hi, over=bool(hi > z["firm"]),
                                 not_available=z["award"] - delivered, comeback_loss=0.0,
                                 one_in_ten_fit=hi_fit, over_fit=bool(hi_fit > z["firm"]),
                                 one_in_ten_relative=hi_rel, over_relative=bool(hi_rel > z["firm"]),
                                 scatter_mw=sd_mw, scatter_share=sd_mw / delivered)
        # the same model fitted on the two earlier winters and set against the last one
        tr, te = ev[ev["winter"].isin(tr_w)], ev[ev["winter"] == te_w]
        st = tr["scheduled"].values.astype(float)
        Bt = np.column_stack([st, st * tr["T"].values])
        bt, covt, rt = _ols(Bt, tr["delivered"].values.astype(float))
        sdt = float(np.std(rt[(tr["T"] < E.FREEZING).values], ddof=2))
        se_ = te["scheduled"].values.astype(float)
        Be = np.column_stack([se_, se_ * te["T"].values])
        pred = Be @ bt
        y = te["delivered"].values.astype(float)
        abs_err += list(np.abs(pred - y))
        half_fit = E.Z90 * np.sqrt(np.einsum("ij,jk,ik->i", Be, covt, Be))     # the fitted mean's 80 per cent range
        cold = (te["T"] < E.FREEZING).values
        n_in += int(np.sum((np.abs(pred - y) <= E.Z90 * sdt) & cold))
        n_in_fit += int(np.sum((np.abs(pred - y) <= half_fit) & cold))
        n_cold += int(cold.sum())
        n_all += len(te)
    out["_backtest"] = dict(mae=float(np.mean(abs_err)), inside=n_in, inside_fit_range=n_in_fit, n_cold=n_cold, n=n_all)
    out["_call"] = [p for p in out if not p.startswith("_") and out[p]["over"]]
    out["_call_fit"] = [p for p in out if not p.startswith("_") and out[p]["over_fit"]]
    out["_call_relative"] = [p for p in out if not p.startswith("_") and out[p]["over_relative"]]
    return out


def quick(X, G):
    """The ten-minute pass: the highest half-hour on record in winter 2025/26 grown to 2027/28, less the megawatts
    contracted at face value."""
    prep = X["_prep"]
    out = {}
    for z in G["zones"]:
        c = z["code"]
        s = prep[(prep["code"] == c)]
        last = s[[E.WINTER_OF(d) == "2025/26" for d in s["ldate"]]]
        top = float(last["mw"].max())
        r1, r2 = X["rates"][c]
        before = E.forecast(top, r1, r2, X["growth"].get(c, 0.0))
        peak = before - z["award"]
        out[z["primary"]] = dict(before=before, delivered=z["award"], peak_hh="18:00", peak=peak, off_peak=z["award"],
                                 one_in_ten=None, over=bool(peak > z["firm"]), not_available=0.0, comeback_loss=0.0)
    out["_backtest"] = None
    out["_call"] = [p for p in out if not p.startswith("_") and out[p]["over"]]
    return out


def routes(X, G, C):
    """Each shortcut's committed set beside the golden's (the routes sheet and effort.json's routes)."""
    r = [dict(name="every result of the chain (the golden)", answer=list(G["commit"]), golden=True)]
    face = [z["primary"] for z in G["zones"] if z["before"] - z["award"] > z["firm"]]
    r.append(dict(name="the megawatts contracted taken at face value", answer=face, golden=False))
    r.append(dict(name="megawatts delivered per megawatt scheduled at minus 3.0 C applied to the contract, the fit's own range",
                  answer=list(C["_call_fit"]), golden=False))
    r.append(dict(name="megawatts delivered per megawatt scheduled, the record's megawatts of scatter unchanged",
                  answer=list(C["_call"]), golden=False))
    r.append(dict(name="megawatts delivered per megawatt scheduled, the scatter in proportion, the credit off the 17:30 to 18:00 peak",
                  answer=list(C["_call_relative"]), golden=False))
    # the share of the contract right, the expected day taken as the test (no day-to-day range), with what comes back
    exp_day = [z["primary"] for z in G["zones"] if z["peak"] > z["firm"]]
    r.append(dict(name="the available share right, the expected day set against firm capacity", answer=exp_day, golden=False))
    # the share right, the credit off the 17:30 to 18:00 peak, the record's megawatts of scatter unchanged
    flat_sd = []
    for z in G["zones"]:
        f = G["providers"][z["provider"]]
        e = G["events"][z["code"]]
        e = e[e["T"] <= E.COLD]
        sd = float(np.std(e["delivered"].values - E.line_share(f, e["T"].values) * e["contract"].values, ddof=1))
        q = z["before"] - z["delivered"] + E.Z90 * math.sqrt(sd ** 2 + (z["cv_base"] * z["before"]) ** 2)
        if q > z["firm"]:
            flat_sd.append(z["primary"])
    r.append(dict(name="the available share right, the credit off the 17:30 to 18:00 peak, the record's megawatts of scatter unchanged",
                  answer=flat_sd, golden=False))
    # what the record's largest contract made available carried unchanged (no growth with the megawatts contracted)
    flat = []
    for z in G["zones"]:
        f = G["providers"][z["provider"]]
        d = z["share"] * X["contract"][(z["code"], "2025/26")]
        q, _ = E.day_quantile(z["profile"], d, f["shape"], f["back"], f["cv"], z["cv_base"])
        if q > z["firm"]:
            flat.append(z["primary"])
    r.append(dict(name="the megawatts the 2025/26 contracts made available carried unchanged", answer=flat, golden=False))
    return r


def r1(v):
    if v is None:
        return None
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


def effort_json(X, G, F):
    C = careful(X, G)
    Q = quick(X, G)
    prim = [z["primary"] for z in G["zones"]]
    provs = sorted(G["providers"])
    zp = {p: [z["primary"] for z in G["zones"] if z["provider"] == p] for p in provs}
    award = {z["primary"]: z["award"] for z in G["zones"]}
    B = F["bands"]

    def table(key, src):
        return {p: (None if src[p].get(key) is None else r1(src[p][key])) for p in prim}

    def bands(key):
        return {p: [B[key][p][0], B[key][p][1]] for p in prim}

    def res(rid, name, graded, figure, depends, golden, key=None, independent="", extra=None):
        d = dict(id=rid, name=name, graded_as=graded, figure=figure, depends=depends, independent=independent, golden=golden)
        if key:
            d["bands"] = bands(key)
            d["passes"] = dict(quick=table(key, Q), careful=table(key, C), thorough=golden)
        if extra:
            d.update(extra)
        return d

    # what each pass files as the megawatts available per megawatt contracted on the design day, provider by provider
    def implied(src):
        return {p: round(sum(src[x]["delivered"] for x in zp[p]) / sum(award[x] for x in zp[p]), 2) for p in provs}

    spread_c = {p: int(round(100 * float(np.mean([C[x]["scatter_share"] for x in zp[p]])))) for p in provs}
    results = [
        res("R1", "design-day demand before flexibility, MW", "Ask 1", "r1_before", [], F["r1_before"], "before"),
        dict(id="R2a", name="the share of its contracted megawatts each provider has available on the design day",
             graded_as="Component 1", figure="c1_share", depends=[], golden=F["c1_share"],
             independent="the events, the contracts and the SCADA record", bands={p: B["share"][p] for p in provs},
             passes=dict(quick={p: 1.0 for p in provs}, careful=implied(C), thorough=F["c1_share"])),
        res("R2", "megawatts each contract delivers at 17:30 to 18:00 on the design day", "Ask 2", "r2_delivered", ["R2a"],
            F["r2_delivered"], "delivered"),
        dict(id="R3", name="last winter predicted from the winters before: the average miss, MW", graded_as="Ask 7",
             figure="r3_backtest", depends=["R2a"], independent="", golden=F["r3_backtest"], band=B["backtest"]["mae"],
             passes=dict(quick=None, careful=round(C["_backtest"]["mae"], 2), thorough=F["r3_backtest"])),
        dict(id="R4a", name="megawatts coming back in the half-hour after the window, per megawatt delivered",
             graded_as="Component 2", figure="c2_comeback", depends=[], golden=F["c2_comeback"],
             independent="the half-hours after the window on the event days themselves",
             bands={p: B["comeback"][p] for p in provs},
             passes=dict(quick=None, careful=None, thorough=F["c2_comeback"])),
        res("R4", "megawatts each contract takes off the day's peak once the load that comes back is counted", "Ask 3",
            "r4_off_peak", ["R2", "R4a"], F["r4_off_peak"], "off_peak"),
        res("R5", "expected design-day peak with flexibility, MW", "Ask 4", "r5_peak", ["R1", "R4"], F["r5_peak"], "peak"),
        dict(id="R6a", name="each provider's day-to-day spread as a share of what it delivers, per cent",
             graded_as="Component 3", figure="c3_spread", depends=[], golden=F["c3_spread"],
             independent="the cold days' scatter about the share's line, net of the baseline's own noise",
             bands={p: B["spread"][p] for p in provs},
             passes=dict(quick=None, careful=spread_c, thorough=F["c3_spread"])),
        res("R6", "the level each peak stays under on nine design days in ten, MW", "Ask 5", "r6_one_in_ten", ["R5", "R6a"],
            F["r6_one_in_ten"], "one_in_ten"),
        dict(id="R7", name="the primaries to reinforce", graded_as="Recommendation", figure="call", depends=["R6"],
             independent="", golden=F["call"], passes=dict(quick=Q["_call"], careful=C["_call"], thorough=F["call"])),
        dict(id="R8", name="each contract's megawatts bridged to the megawatts off the peak", graded_as="Ask 6",
             figure="r8_bridge", depends=["R2", "R4"], independent="", golden=F["r8_bridge"],
             bands={k: B["bridge"][k] for k in F["r8_bridge"]},
             passes=dict(quick={k: 0.0 for k in F["r8_bridge"]},
                         careful={**{"%s, not available" % p: r1(C[p]["not_available"]) for p in prim},
                                  **{"%s, lost as load comes back" % p: 0.0 for p in prim}},
                         thorough=F["r8_bridge"])),
    ]
    hints = [
        dict(order=1, sentence="a provider can deliver no more than a share of its contracted megawatts on a cold evening, "
                               "however many are scheduled", rescues=["R2a", "R2"]),
        dict(order=2, sentence="for an hour or two after the service window the curtailed load comes back above normal",
             rescues=["R4a"]),
        dict(order=3, sentence="what a provider has available varies from one cold evening to the next by about a sixth of "
                               "its level", rescues=["R6a"]),
    ]
    return dict(results=results, hints=hints, routes=routes(X, G, C)), C, Q
