"""task10 architecture 7: an independent recomputation of the graded figures from target/, written without the
generator's estimators (pandas and least squares only, each quantity by a simpler route of its own), set against
generator/figures.json: every independent figure has to land inside the band the answer blocks state, and the list
has to be the same.
python3 task10/generator/verify.py

  demand      the morning at the design temperature from a straight line through the working weekdays at or below
              1 C; each evening half-hour regressed on the day's own morning over the days no service ran
  customers   each customer's latest three months carried forward by its type's own readings at the two ages (the
              mean share of agreed capacity by age band, no curve fitted)
  in service  each site still to come at the share of its class's sites that were in service that many days after
              their planned date, among sites watched at least that long
  share       a straight line through the events at or below 1 C that fell short of their instruction
  the day     the reduction through the window and the load coming back as ratios of sums; twenty thousand design days
  the choices a further contract on the award's terms scanned in half-megawatt steps on the same days, each step site
              given its class's share in service by its planned date's distance from the assessment date; the schedule
              scanned in tenths; the data hall at its type's mean share of agreed capacity at its age
"""
import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import parse as PA   # noqa: E402  (the pack's own reading: registers, PDFs, revisions)

HOL = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29), dt.date(2024, 12, 25),
       dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
HH = ["%02d:%02d" % ((i + 1) // 2, 30 if (i + 1) % 2 else 0) for i in range(48)]
MORN = HH[13:31]
WIN = ["16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30"]
POST = ["20:00", "20:30", "21:00", "21:30"]
ASSESS, BASIS = dt.date(2028, 1, 15), dt.date(2026, 1, 15)
OUT = []


def say(ok, what, detail):
    OUT.append(bool(ok))
    print("%s %-34s %s" % ("PASS" if ok else "FAIL", what, detail))


def winter(d):
    y = d.year if d.month >= 7 else d.year - 1
    return "%d/%02d" % (y, (y + 1) % 100)


def workday(d):
    return d.weekday() < 5 and d not in HOL and not ((d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2))


def months(a, b):
    return (b - a).days / 30.4375


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    B = F["bands_by_result"]
    X = PA.load(TARGET)
    names = F["order"]
    code = {X["names"][c]: c for c in X["contracts_code"]}
    # the documents the figures lean on, read back through the same extractor with a sentence known to be in each
    g = " ".join(X["guideline_text"].split())
    a = " ".join(X["award_text"].split())
    say("Primary Substation Capacity Assessment" in g and "minus 3.0 degrees Celsius" in g and "15 January" in g and
        "more than one design day in ten" in g, "guideline read back", "design condition, assessment date and test found in the PDF")
    say("Contract Award Notice" in a and len(X["contracts_code"]) == 5 and all(len(v) == 5 for v in X["previous"].values()),
        "award notice read back", "five awards and five winters of contracted megawatts")
    say(len(X["firm"]) == 9, "Appendix A read back", "nine firm capacities")

    d = X["demand"].copy()
    loc = d["t_utc"].dt.tz_convert("Europe/London")
    d["day"] = (loc - pd.Timedelta(minutes=30)).dt.date
    lab = loc.dt.strftime("%H:%M")
    d["hh"] = np.where(lab == "00:00", "24:00", lab)
    wx = X["weather"].copy()
    wx["day"] = wx["t_utc"].dt.date
    tm = wx.groupby("day")["temp_c"].agg(["mean", "size"])
    tm = tm[tm["size"] >= 20]["mean"]
    sw = X["switching"]
    reg = X["assets"]
    isd = lambda v: v is not None and not (isinstance(v, float) and math.isnan(v)) and pd.notna(v)

    def in_service(zone, day):
        r = reg[reg["zone"] == zone]
        return sum(k for k, c, l in zip(r["kw"], r["commissioned"], r["left"]) if isd(c) and c <= day and not (isd(l) and l <= day)) / 1000.0

    prof, sd_day, events = {}, {}, []
    for n in names:
        c = code[n]
        z = d[d["code"] == c]
        P = z.pivot_table(index="day", columns="hh", values="mw").reindex(columns=HH)
        P = P[[x in tm.index for x in P.index]]
        swd = set()
        for r in sw.itertuples():
            if c in (r.frm, r.to):
                s0, s1 = r.start.tz_convert("Europe/London").date(), r.end.tz_convert("Europe/London").date()
                swd |= {s0 + dt.timedelta(days=i) for i in range((s1 - s0).days + 1)}
        ev = X["events"][(X["events"]["zone"] == c) & (X["events"]["status"] == "Completed")]
        served = dict(zip(ev["date"], ev["scheduled_mw"]))
        M = P[MORN].mean(axis=1).where(P[MORN].notna().sum(axis=1) >= len(MORN) - 2)
        days = [x for x in P.index if workday(x) and x not in swd and not math.isnan(M[x])]
        ws = sorted({winter(x) for x in days})
        # the morning at the design temperature: a straight line through the days at or below 1 C, winter levels
        cold = [x for x in days if tm[x] <= 1.0]
        A = np.column_stack([[1.0 if winter(x) == w else 0.0 for x in cold] for w in ws] + [[tm[x] for x in cold]])
        b, *_ = np.linalg.lstsq(A, np.array([M[x] for x in cold]), rcond=None)
        mstar = b[ws.index("2025/26")] + b[-1] * (-3.0)
        # every working weekday against a smooth curve (a cubic), for how far a day runs from its usual level
        A3 = np.column_stack([[1.0 if winter(x) == w else 0.0 for x in days] for w in ws] + [[tm[x] ** k for x in days] for k in (1, 2, 3)])
        b3, *_ = np.linalg.lstsq(A3, np.array([M[x] for x in days]), rcond=None)
        rel = (np.array([M[x] for x in days]) - A3 @ b3) / (A3 @ b3)
        sd_day[n] = float(rel.std(ddof=6))
        # each half-hour on the day's own morning, days no service ran
        clean = [x for x in days if x not in served and P.loc[x].notna().sum() == 48]
        A2 = np.column_stack([[1.0 if winter(x) == w else 0.0 for x in clean] for w in ws] + [[M[x] for x in clean]])
        Bh, *_ = np.linalg.lstsq(A2, P.loc[clean].values, rcond=None)
        prof[n] = Bh[ws.index("2025/26")] + Bh[-1] * mstar
        for x, mw in served.items():
            if x not in P.index or x in swd or math.isnan(M[x]) or P.loc[x, WIN + POST].isna().any():
                continue
            cf = Bh[ws.index(winter(x))] + Bh[-1] * M[x]
            red = cf - P.loc[x].values
            events.append(dict(zone=n, prov=X["provider_of"][c], day=x, T=float(tm[x]), sched=float(mw),
                               deliv=float(red[[HH.index("17:30"), HH.index("18:00")]].mean()),
                               win=red[[HH.index(h) for h in WIN]], post=-red[[HH.index(h) for h in POST]],
                               base=in_service(c, x)))
    d26 = {n: float(prof[n].max()) for n in names}

    # customers: the type's mean share of agreed capacity by age band, no curve fitted
    C = X["connections"]
    Mo = X["monitor"].merge(C[["conn", "type", "kva", "energised"]], on="conn")
    Mo["age"] = [months(e, m + dt.timedelta(days=14)) for e, m in zip(Mo["energised"], Mo["month"])]
    Mo["ratio"] = Mo["evening_kw"] / Mo["kva"]

    def level(ctype, age):
        """the mean share at an age: the type's own readings within three months of it, every type's if those are few"""
        lo, hi = max(age - 3.0, 0.0), age + 3.0
        s = Mo[(Mo["type"] == ctype) & (Mo["age"] >= lo) & (Mo["age"] <= hi)]
        if age > 36:
            s = Mo[(Mo["type"] == ctype) & (Mo["age"] >= 33)]
        if s["conn"].nunique() < 3:
            allr = Mo[(Mo["age"] >= lo) & (Mo["age"] <= hi)] if age <= 36 else Mo[Mo["age"] >= 33]
            est = Mo[(Mo["type"] == ctype) & (Mo["age"] >= 30)]["ratio"].mean()
            pooled_est = Mo[Mo["age"] >= 30]["ratio"].mean()
            return float(allr["ratio"].mean() * (est / pooled_est if est == est else 1.0))
        return float(s["ratio"].mean())

    conn = {}
    for n in names:
        tot = 0.0
        for r in C[C["code"] == code[n]].itertuples():
            start = r.energised if isd(r.energised) else r.planned
            if start >= ASSESS:
                continue
            a1 = months(start, ASSESS)
            if isd(r.energised):
                mm = Mo[Mo["conn"] == r.conn].sort_values("month")
                if len(mm) >= 6:
                    now = float(mm.tail(3)["ratio"].mean())
                    age_now = float(mm.tail(3)["age"].mean())
                    lvl1 = r.kva * now * level(r.type, a1) / max(level(r.type, age_now), 1e-6)
                else:
                    lvl1 = r.kva * level(r.type, a1)
                seen = mm[(mm["month"] >= dt.date(2025, 12, 1)) & (mm["month"] <= dt.date(2026, 2, 1))]
                a0 = months(start, BASIS)
                lvl0 = r.kva * float(seen["ratio"].mean()) if len(seen) >= 2 else (r.kva * level(r.type, a0) if a0 > 0 else 0.0)
                tot += lvl1 - lvl0
            else:
                tot += r.kva * level(r.type, a1)
        conn[n] = tot / 1000.0
    before = {}
    for n in names:
        r1_, r2_ = X["rates"][code[n]]
        before[n] = d26[n] * (1 + r1_ / 100) * (1 + r2_ / 100) + conn[n]

    # megawatts in service: the share of a class's sites in service h days after the planned date, among sites
    # watched at least h days (withdrawn sites never in service)
    asof = X["register_date"]
    due = reg[[p <= asof for p in reg["planned"]]]

    def share_by(cls, h):
        s = due[due["cls"] == cls]
        watched = s[[(asof - p).days >= h for p in s["planned"]]]
        if len(watched) < 12:
            watched = s
        return float(np.mean([isd(c) and (c - p).days <= h for c, p in zip(watched["commissioned"], watched["planned"])])), \
            float(np.mean([isd(l) and (l - p).days <= h for l, p in zip(watched["lost"], watched["planned"])]))

    insvc = {}
    for n in names:
        now = in_service(code[n], asof)
        add = 0.0
        pend = reg[(reg["zone"] == code[n]).values & np.array([not isd(c) and not isd(l) for c, l in zip(reg["commissioned"], reg["lost"])])]
        for r in pend.itertuples():
            h, e = (ASSESS - r.planned).days, (asof - r.planned).days
            fh, _ = share_by(r.cls, h)
            if e <= 0:
                add += r.kw * fh
            else:
                fe, le = share_by(r.cls, e)
                add += r.kw * max(fh - fe, 0.0) / max(1.0 - fe - le, 1e-6)
        insvc[n] = now + add / 1000.0

    # the share available at the design temperature: the cold events that fell short of their instruction
    E = pd.DataFrame(events)
    share, cv, ramp, back = {}, {}, {}, {}
    for prov, e in E.groupby("prov"):
        short = e[(e["deliv"] < e["sched"] - np.maximum(0.2, 0.07 * e["sched"])) & (e["T"] <= 1.0)]
        y = np.log(short["deliv"] / short["base"])
        c1, c0 = np.polyfit(short["T"], y, 1)
        res = y - (c0 + c1 * short["T"])
        share[prov] = float(math.exp(c0 + c1 * (-3.0) + 0.5 * res.var(ddof=2)))
        cv[prov] = float(res.std(ddof=2))
        big = e[e["deliv"] > 0.5]
        ramp[prov] = np.vstack(big["win"].values).sum(axis=0) / big["deliv"].sum()
        back[prov] = np.vstack(big["post"].values).sum(axis=0) / big["deliv"].sum()
    key = {v["key"]: k for k, v in F["providers"].items()}
    rng = np.random.default_rng(7)
    res, days = {}, {}
    for n in names:
        c = code[n]
        prov = X["provider_of"][c]
        deliv = min(share[prov] * insvc[n], X["contracts_code"][c])
        p28 = prof[n] * before[n] / d26[n]
        N = 20000
        r = rng.normal(0, sd_day[n], N)
        dl = np.minimum(deliv * np.exp(cv[prov] * rng.normal(0, 1, N) - 0.5 * cv[prov] ** 2), X["contracts_code"][c])
        Pm = p28[None, :] * (1 + r[:, None])
        Pm[:, [HH.index(h) for h in WIN]] -= dl[:, None] * ramp[prov][None, :]
        Pm[:, [HH.index(h) for h in POST]] += dl[:, None] * back[prov][None, :] * (1 + 0.18 * rng.normal(0, 1, (N, 4)))
        pk = Pm.max(axis=1)
        firm = X["firm"][c]
        res[n] = dict(R1=d26[n], R2=conn[n], R3=before[n], R4=insvc[n], R6=deliv, R8=float(pk.mean()), R9=float(np.quantile(pk, 0.9)),
                      R10=100.0 * float((pk > firm).mean()), commit=bool(np.quantile(pk, 0.9) > firm))
        z_a = rng.normal(0, 1, N)
        rb = 1 + 0.18 * rng.normal(0, 1, (N, 4))
        days[n] = (p28, r, z_a, rb, prov, firm, deliv)

    def day_stats(n, deliv, cap, sched=None, scale=1.0):
        p28, r, z_a, rb, prov, firm, _ = days[n]
        dl = np.minimum(deliv * np.exp(cv[prov] * z_a - 0.5 * cv[prov] ** 2), cap)
        if sched is not None:
            dl = np.minimum(dl, sched)
        Pm = (p28 * scale)[None, :] * (1 + r[:, None])
        Pm[:, [HH.index(h) for h in WIN]] -= dl[:, None] * ramp[prov][None, :]
        Pm[:, [HH.index(h) for h in POST]] += dl[:, None] * back[prov][None, :] * rb
        pk = Pm.max(axis=1)
        return float(np.quantile(pk, 0.9)), float((pk > firm).mean())

    # R12: a further contract on the award's terms, each step site at its class's share in service by then
    further, low = {}, {}
    for n in F["call"]:
        c = code[n]
        step = reg[(reg["zone"] == c) & (reg["winter"] == "2027/28")]
        per = sum(r.kw * share_by(r.cls, (ASSESS - r.planned).days)[0] for r in step.itertuples()) / 1000.0 / \
            (X["contracts_code"][c] - X["previous"][n]["2026/27"])
        prov = X["provider_of"][c]
        curve = [(x, day_stats(n, min(share[prov] * (insvc[n] + x * per), X["contracts_code"][c] + x), X["contracts_code"][c] + x)[1])
                 for x in np.arange(0.0, 40.01, 0.5)]
        hit = next((x for x, sh in curve if sh <= 0.10), None)
        if hit is not None and hit > 0:
            fine = [x for x in np.arange(hit - 0.4, hit + 1e-9, 0.1)
                    if day_stats(n, min(share[prov] * (insvc[n] + x * per), X["contracts_code"][c] + x), X["contracts_code"][c] + x)[1] <= 0.10]
            hit = float(fine[0]) if fine else hit
        further[n], low[n] = hit, min(sh for _, sh in curve)
    ok12 = all((further[n] is None and low[n] >= 0.15) if F["r12_further"][n] == "none" else
               (further[n] is not None and B["R11"][n][0] - 0.3 <= further[n] <= B["R11"][n][1] + 0.3) for n in F["call"])
    # R13: Ashcombe Road's schedule
    sa = "Ashcombe Road"
    c = code[sa]
    sched = [(s_, *day_stats(sa, res[sa]["R6"], X["contracts_code"][c], sched=s_)) for s_ in np.arange(0.0, X["contracts_code"][c] + 1e-9, 0.1)]
    s_best = min(sched, key=lambda t: (t[2], t[1], -t[0]))
    ok13 = B["R12"]["schedule"][0] - 0.1 <= s_best[0] <= B["R12"]["schedule"][1] + 0.1 and s_best[1] > X["firm"][c]
    # R14: Hartwell Common with the data hall, at the type's mean share of agreed capacity at its age
    ca = "Hartwell Common"
    det = F["r14_detail"]
    adds = det["kva"] * level(det["type"], months(dt.date(2027, 8, 2), ASSESS)) / 1000.0
    p90c, shc = day_stats(ca, res[ca]["R6"], X["contracts_code"][code[ca]], scale=(before[ca] + adds) / before[ca])
    ok14 = B["R13"]["adds"][0] - 0.05 <= adds <= B["R13"]["adds"][1] + 0.05 and p90c <= X["firm"][code[ca]]
    for rid, label, fmt in (("R1", "demand 2025/26", "%.2f"), ("R2", "customers add", "%.2f"), ("R3", "before flexibility", "%.2f"),
                            ("R4", "in service", "%.2f"), ("R6", "delivered", "%.2f"), ("R8", "expected peak", "%.2f"),
                            ("R9", "nine days in ten", "%.2f"), ("R10", "days over firm", "%.0f")):
        tol = 0.05 if rid != "R10" else 2.0
        miss = [n for n in names if not (B[rid][n][0] - tol <= res[n][rid] <= B[rid][n][1] + tol)]
        say(not miss, label, "; ".join("%s %s [%s to %s]" % (n.split()[0], fmt % res[n][rid], B[rid][n][0], B[rid][n][1]) for n in names))
    say(all(B["R5"][key[p]][0] - 0.005 <= share[p] <= B["R5"][key[p]][1] + 0.005 for p in share), "share available",
        "; ".join("%s %.3f [%s to %s]" % (key[p], share[p], B["R5"][key[p]][0], B["R5"][key[p]][1]) for p in share))
    say(all(B["R7"][key[p]][0] - 0.01 <= back[p].sum() <= B["R7"][key[p]][1] + 0.01 for p in back), "comes back per MW",
        "; ".join("%s %.3f [%s to %s]" % (key[p], back[p].sum(), B["R7"][key[p]][0], B["R7"][key[p]][1]) for p in back))
    mine = [n for n in names if res[n]["commit"]]
    say(mine == F["call"], "the list", "independent: %s" % ", ".join(mine))
    say(ok12, "further contract", "; ".join("%s %s" % (n.split()[0], ("none (lowest %.0f%%)" % (100 * low[n])) if further[n] is None
                                                       else "%.1f MW" % further[n]) for n in F["call"]))
    say(ok13, "schedule", "%s %.1f MW, nine days in ten %.2f MW [%s to %s]" % (sa, s_best[0], s_best[1], *B["R12"]["schedule"]))
    say(ok14, "data hall", "adds %.2f MW [%s to %s]; %s nine days in ten %.2f MW against %.1f" % (
        adds, *B["R13"]["adds"], ca, p90c, X["firm"][code[ca]]))
    say(len(E) == sum(v["events"] for v in F["providers"].values()), "events measured", "%d completed events" % len(E))
    print("verify: %s (%d of %d)" % ("PASS" if all(OUT) else "FAIL", sum(OUT), len(OUT)))
    return 0 if all(OUT) else 1


if __name__ == "__main__":
    sys.exit(main())
