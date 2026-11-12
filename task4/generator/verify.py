"""An independent recompute from the shipped files alone, on its own code path (its own parsing and cleaning, statsmodels
for the fits, scipy for the serial mixture, the report read from its PDF): the report's twelve-month counts, the
drivers, every part's 2027 removals against its band, the bulletin's effect, the watch list and its withdrawals, the
repairers' lines' spares by Palm's theorem, and the shop's 2026 turnaround. It never imports the generator's analysis.
Exit 1 on any failure."""
import json
import math
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy import optimize, stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
RES = []
ICAO = {"ENBO": "BOO", "ENTC": "TOS", "ENBR": "BGO", "ENVA": "TRD"}
GROUP = {"Bodø": "BOO", "Tromsø": "TOS", "Bergen": "BGO", "Trondheim": "TRD", "Bodø (Helgeland routes)": "HEL"}
M12 = (pd.Timestamp("2025-11-01"), pd.Timestamp("2026-10-31"))


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def norm_pn(x):
    return re.sub(r"[^0-9A-Z]", "", str(x).upper())


def load():
    snap = pd.read_excel(os.path.join(T, "rotable_stores_snapshot_2026-11-30.xlsx"), dtype=str)
    pns = sorted(snap["Part number"].unique())
    canon = {norm_pn(p): p for p in pns}
    qpa = (snap[snap["Condition"] == "Installed"].groupby("Part number").size() / 30).round().astype(int).to_dict()
    # legs: the feed's second copies dropped; air time, else block less the field's usual taxi
    L = pd.read_csv(os.path.join(T, "flight_legs_2023-01_2026-11.csv"), dtype=str).drop_duplicates()
    for c in ("out_utc", "off_utc", "on_utc", "in_utc"):
        L[c] = pd.to_datetime(L[c].str.replace("Z", ""), errors="coerce")
    L["date"] = pd.to_datetime(L["flight_date"])
    air = (L["on_utc"] - L["off_utc"]).dt.total_seconds() / 60
    blk = (L["in_utc"] - L["out_utc"]).dt.total_seconds() / 60
    txo = ((L["off_utc"] - L["out_utc"]).dt.total_seconds() / 60).groupby(L["dep"]).median()
    txi = ((L["in_utc"] - L["on_utc"]).dt.total_seconds() / 60).groupby(L["arr"]).median()
    L["air"] = air.fillna(blk - L["dep"].map(txo) - L["arr"].map(txi))
    day = L.groupby(["aircraft", "date"]).agg(ldg=("air", "size"), fh=("air", lambda s: s.sum() / 60)).reset_index()
    bh = pd.read_excel(os.path.join(T, "fleet_register.xlsx"), sheet_name="Base history")
    day["base"] = None
    for _, r in bh.iterrows():
        z = r["To"] if pd.notna(r["To"]) else pd.Timestamp("2026-11-30")
        m = (day["aircraft"] == r["Registration"]) & (day["date"] >= r["From"]) & (day["date"] <= z)
        day.loc[m, "base"] = r["Base"]
    wx = pd.read_csv(os.path.join(T, "station_weather_daily_2023-2026.csv"))
    wx["base"] = wx["station"].map(ICAO)
    wx["date"] = pd.to_datetime(wx["date"])
    wx = wx.sort_values(["base", "date"])
    wx["tmin_c"] = wx.groupby("base")["tmin_c"].ffill()
    day = day.merge(wx[["base", "date", "tmin_c"]], on=["base", "date"], how="left")
    day["frost"] = (-day["tmin_c"]).clip(lower=0)
    # changes: a corrected entry replaces its original; serials as stores know them
    C = pd.read_csv(os.path.join(T, "component_changes_2023-01_2026-11.csv"), dtype=str, keep_default_na=False)
    stem = C["change_no"].str.replace(r"-R\d+$", "", regex=True)
    fixed = set(stem[C["change_no"] != stem])
    C = C[~((C["change_no"] == stem) & stem.isin(fixed))].copy()
    C["pn"] = C["part_no"].map(lambda x: canon.get(norm_pn(x), x))
    C["sn"] = C["serial_off"].str.replace(r"^S/N\s*", "", regex=True).str.upper()
    C["date"] = pd.to_datetime(C["change_date"])
    C["unsch"] = C["reason"].isin(["U", "UNSCH"]) & (C["sn"] != "")
    # findings from the shop's and the repairers' orders, matched on serial within ten days
    S = pd.read_csv(os.path.join(T, "bodo_shop_work_orders_2023-2026.csv"), dtype=str, keep_default_na=False)
    S = S[S["order_type"] == "ROTABLE"].copy()
    S["rec"] = pd.to_datetime(S["received"])
    S["done"] = pd.to_datetime(S["completed"].replace("", None))

    def shop_f(r):
        if r["finding_code"]:
            return {"CONF": "CF", "NFF": "NFF", "BER": "BER"}[r["finding_code"]]
        t = r["finding"].lower()
        if not t:
            return ""
        if "no fault found" in t or ("serviceable" in t and "replaced" not in t):
            return "NFF"
        return "BER" if ("beyond economic repair" in t or "scrapped" in t) else "CF"
    S["f"] = S.apply(shop_f, axis=1)
    V = pd.read_excel(os.path.join(T, "vendor_repair_orders_2023-2026.xlsx"), sheet_name="Repair orders")
    V.columns = ["ro", "vendor", "pn", "sn", "shipped", "recv", "back", "finding", "amount", "ccy", "fx"]
    V["finding"] = V["finding"].fillna("").astype(str)
    V["f"] = V["finding"].str.lower().map(lambda t: "" if not t else ("SB" if t.startswith("sb 27") else
                                                                       ("NFF" if "no fault found" in t else
                                                                        ("BER" if "beyond economic repair" in t else "CF"))))
    for c in ("shipped", "back"):
        V[c] = pd.to_datetime(V[c])
    U = C[C["unsch"]].copy()
    U["f"], U["back"], U["shop"] = "", pd.NaT, ""
    sb = {s: g.sort_values("rec") for s, g in S.groupby("serial")}
    vb = {s: g.sort_values("shipped") for s, g in V.groupby("sn")}
    for i, r in U.iterrows():
        g = sb.get(r["sn"])
        if g is not None:
            m = g[(g["rec"] >= r["date"]) & (g["rec"] <= r["date"] + pd.Timedelta(days=10))]
            if len(m):
                U.at[i, "f"], U.at[i, "shop"] = m.iloc[0]["f"], "BOO"
                U.at[i, "back"] = m.iloc[0]["done"] + pd.Timedelta(days=1) if pd.notna(m.iloc[0]["done"]) else pd.NaT
                continue
        g = vb.get(r["sn"])
        if g is not None:
            m = g[(g["shipped"] >= r["date"]) & (g["shipped"] <= r["date"] + pd.Timedelta(days=10))]
            if len(m):
                U.at[i, "f"], U.at[i, "shop"], U.at[i, "back"] = m.iloc[0]["f"], "VND", m.iloc[0]["back"]
    return {"snap": snap, "pns": pns, "qpa": qpa, "day": day, "C": C, "U": U, "V": V, "S": S, "txo": txo, "txi": txi}


def report_tables():
    import fitz
    t = "\n".join(p.get_text() for p in fitz.open(os.path.join(T, "reliability_report_2026-10.pdf")))
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    a = lines.index("2. Rotable reliability")
    b = lines.index("3. Watch list")
    sec = lines[a:b]
    rows = {}
    for i, x in enumerate(sec):
        if re.fullmatch(r"[0-9A-Z][0-9A-Z-]{3,}", x) and i + 4 < len(sec) and re.fullmatch(r"\d+", sec[i + 4] or ""):
            rows[x] = int(sec[i + 4])
    c = lines.index("3. Watch list")
    serials = {x for x in lines[c:] if re.fullmatch(r"[A-Z]{1,3}\d{3,6}", x)}
    return rows, serials


def panel(F, pn, finding_set):
    D = F["day"].copy()
    D["ym"] = D["date"].dt.to_period("M")
    g = D.groupby(["aircraft", "ym"]).agg(ldg=("ldg", "sum"), fh=("fh", "sum"), fly=("ldg", "size"),
                                          frost=("frost", "sum")).reset_index()
    g["days"] = g["ym"].map(lambda p: p.days_in_month)
    U = F["U"]
    u = U[(U["pn"] == pn) & U["f"].isin(finding_set)]
    n = u.assign(ym=u["date"].dt.to_period("M")).groupby(["aircraft", "ym"]).size().rename("n")
    g = g.merge(n, left_on=["aircraft", "ym"], right_index=True, how="left").fillna({"n": 0})
    g = g[(g["ym"] >= pd.Period("2023-01", "M")) & (g["ym"] <= pd.Period("2026-10", "M"))]
    q = F["qpa"].get(pn, 1)
    for c in ("ldg", "fh", "days"):
        g[c] = g[c] * q
    g["fr"] = g["frost"] / g["fly"].clip(lower=1)
    return g


def fit(g, expo):
    e = g[expo].values.astype(float)
    k = e > 0
    X = sm.add_constant(g["fr"].values[k])
    m = sm.GLM(g["n"].values[k], X, family=sm.families.Poisson(), offset=np.log(e[k])).fit()
    return m


def main():
    F = load()
    pns = F["pns"]
    key = {v: k for k, v in FIG["pn"].items()}
    # V1: the report's twelve-month counts
    rows, listed_pdf = report_tables()
    U = F["U"]
    u12 = U[(U["date"] >= M12[0]) & (U["date"] <= M12[1])]
    own = u12.groupby("pn").size().to_dict()
    off = [p for p in pns if rows.get(p) != own.get(p, 0)]
    ok("V1 the October report's twelve-month removals reproduce part by part", not off,
       ", ".join("%s %s/%s" % (p, rows.get(p), own.get(p, 0)) for p in off))
    # V2: the drivers of the landing-driven parts
    drv, models = {}, {}
    for p in pns:
        g = panel(F, p, ("CF", "BER"))
        fits = {e: fit(g, e) for e in ("ldg", "fh", "days")}
        best = max(fits, key=lambda e: fits[e].llf)
        drv[p], models[p] = best, fits
    gaps = {}
    for k in ("SG", "BRK", "BAV"):
        p = FIG["pn"][k]
        f = models[p]
        gaps[k] = 2 * (f["ldg"].llf - max(f["fh"].llf, f["days"].llf))
    ok("V2 landings beat flight hours and calendar days for the three priced parts (2 dlogL over 6)",
       all(drv[FIG["pn"][k]] == "ldg" and gaps[k] > 6 for k in gaps), str({k: round(v, 1) for k, v in gaps.items()}))
    # V3: each part's 2027 removals on its own driver, by base and month, the no-fault-found at each station's rate
    G = pd.read_excel(os.path.join(T, "flying_programme_2027.xlsx"), sheet_name="Programme 2027")
    G.columns = ["season", "group", "dep", "arr", "from", "to", "pw", "block"]
    so, si = float(np.percentile(F["txo"].values, 25)), float(np.percentile(F["txi"].values, 25))
    recs = []
    for _, r in G.iterrows():
        days = pd.date_range(r["from"], r["to"])
        per = float(r["pw"]) / 7
        air = (float(r["block"]) - F["txo"].get(r["dep"], so) - F["txi"].get(r["arr"], si)) / 60
        for m, n in pd.Series(1, index=days).groupby(days.month).sum().items():
            recs.append((GROUP[r["group"]], m, per * n, per * n * air))
    X = pd.DataFrame(recs, columns=["g", "m", "ldg", "fh"]).groupby(["g", "m"]).sum().reset_index()
    AB = pd.read_excel(os.path.join(T, "flying_programme_2027.xlsx"), sheet_name="Aircraft by base")
    AB.columns = ["month", "BOO", "TOS", "BGO", "TRD", "HEL"]
    ad = []
    for _, r in AB.iterrows():
        mm = pd.Timestamp(r["month"]).month
        nd = pd.Period("2027-%02d" % mm, "M").days_in_month
        for g in ("BOO", "TOS", "BGO", "TRD", "HEL"):
            ad.append((g, mm, (r[g] - (r["HEL"] if g == "BOO" else 0)) * nd))
    X = X.merge(pd.DataFrame(ad, columns=["g", "m", "days"]), on=["g", "m"], how="outer").fillna(0)
    W = F["day"].copy()
    W["m"] = W["date"].dt.month
    clim = (pd.read_csv(os.path.join(T, "station_weather_daily_2023-2026.csv")).assign(
        base=lambda d: d["station"].map(ICAO), m=lambda d: pd.to_datetime(d["date"]).dt.month,
        fz=lambda d: (-d["tmin_c"]).clip(lower=0)).groupby(["base", "m"])["fz"].mean().to_dict())
    Dd = F["day"][F["day"]["date"] <= M12[1]]
    rem = {}
    for p in pns:
        k = key[p]
        if k == "PEC":
            continue
        e_col = drv[p]
        b = models[p][e_col].params
        q = F["qpa"].get(p, 1)
        nff = U[(U["pn"] == p) & (U["f"] == "NFF") & (U["date"] <= M12[1])].groupby("station").size()
        ex = Dd.groupby("base").agg(ldg=("ldg", "sum"), fh=("fh", "sum"), days=("date", "size")) * q
        nr = {s: float(nff.get(s, 0)) / float(ex.loc[s, e_col]) for s in ex.index}
        tot = 0.0
        for _, r in X.iterrows():
            st = "BOO" if r["g"] == "HEL" else r["g"]
            e = float(r[e_col]) * q
            tot += e * math.exp(b[0] + b[1] * clim.get((st, int(r["m"])), 0.0)) + e * nr.get(st, np.mean(list(nr.values())))
        rem[k] = tot
    out = [k for k in rem if not (FIG["rem_lo_%s" % k] - 0.5 <= rem[k] <= FIG["rem_hi_%s" % k] + 0.5)]
    ok("V3 every part's 2027 removals inside its band on this code path", not out,
       ", ".join("%s %.1f [%d,%d]" % (k, rem[k], FIG["rem_lo_%s" % k], FIG["rem_hi_%s" % k]) for k in out))
    # V4: SB 61-0042 from the repairers' returns and the snapshot
    V = F["V"]
    pec = FIG["pn"]["PEC"]
    moddate = V[(V["pn"] == pec) & V["finding"].str.contains("SB 61-0042")].groupby("sn")["back"].min().to_dict()
    u = U[(U["pn"] == pec) & (U["date"] >= pd.Timestamp("2024-10-07")) & U["f"].isin(["CF", "BER"])]
    n_mod = int(sum(1 for _, r in u.iterrows() if r["sn"] in moddate and r["date"] >= moddate[r["sn"]]))
    n_un = len(u) - n_mod
    # installed exposure split by each serial's modification date, from the changes' fit and removal dates
    Cc = F["C"][F["C"]["pn"] == pec].sort_values(["date", "change_no"])
    fhd = F["day"].set_index(["aircraft", "date"])["fh"]
    e_mod = e_un = 0.0
    for (ac, pos), g in Cc.groupby(["aircraft", "position"]):
        cur, start = None, pd.Timestamp("2023-01-01")
        spans = []
        first = True
        for _, r in g.iterrows():
            if r["sn"]:
                spans.append((r["sn"] if (first or cur is None) else cur, pd.Timestamp("2023-01-01") if first else start, r["date"]))
                cur = None
            first = False
            if r["serial_on"]:
                cur, start = r["serial_on"].upper(), r["date"]
        if cur:
            spans.append((cur, start, pd.Timestamp("2026-12-01")))
        s = fhd.loc[ac] if ac in fhd.index.get_level_values(0) else None
        if s is None:
            continue
        for sn, a, z in spans:
            seg = s[(s.index >= max(a, pd.Timestamp("2024-10-07"))) & (s.index < z)]
            md = moddate.get(sn)
            if md is not None:
                e_mod += float(seg[seg.index >= md].sum())
                e_un += float(seg[seg.index < md].sum())
            else:
                e_un += float(seg.sum())
    cut = 100 * (1 - (n_mod / e_mod) / (n_un / e_un))
    ok("V4 the bulletin's cut in the confirmed-failure rate within 15 points of the golden's", abs(cut - FIG["pec_cut_pct"]) <= 15,
       "%.0f against %d" % (cut, FIG["pec_cut_pct"]))
    # V5: the watch list, read on its own
    lst = u12.groupby("sn").size()
    lst = set(lst[lst >= 3].index)
    ok("V5a the watch list reproduces the report's", lst == listed_pdf, "%d own, %d in the report" % (len(lst), len(listed_pdf)))
    scrap, saving = watch(F, X, drv, lst)
    ok("V5b the serials worth withdrawing match", sorted(scrap) == sorted(FIG["scrap_set"]),
       "own %s" % sorted(scrap))
    ok("V5c the whole list's saving inside the band", FIG["saving_lo"] - 1 <= saving <= FIG["saving_hi"] + 1,
       "%.1f against [%d,%d]" % (saving, FIG["saving_lo"], FIG["saving_hi"]))
    # V6: the repairers' lines by Palm's theorem on this path's removals and the repairer's own turnaround
    offp = []
    for p in pns:
        k = key[p]
        if k in ("SG", "BRK", "BAV", "NWS", "BAT") or k == "PEC":
            continue
        uu = U[(U["pn"] == p) & (U["date"] >= pd.Timestamp("2025-01-01")) & U["back"].notna()]
        tat = float((uu["back"] - uu["date"]).dt.days.mean())
        m = rem[k] / 365.0 * tat
        s = int(stats.poisson.ppf(0.95, m)) + 1
        if not (FIG["need_lo_%s" % k] - 1 <= s <= FIG["need_hi_%s" % k] + 1):
            offp.append("%s %d [%d,%d]" % (k, s, FIG["need_lo_%s" % k], FIG["need_hi_%s" % k]))
    ok("V6 the repairers' lines by Palm's theorem within a unit of their bands", not offp, ", ".join(offp))
    # V7: the in-house lines' 2026 turnaround
    t26 = []
    for k in ("SG", "BRK", "BAV", "NWS", "BAT"):
        uu = U[(U["pn"] == FIG["pn"][k]) & (U["date"] >= pd.Timestamp("2026-01-01")) & U["back"].notna()]
        t26.append(abs(float((uu["back"] - uu["date"]).dt.days.mean()) - FIG["tat_2026_%s" % k]) <= 1.0)
    ok("V7 the in-house lines' 2026 turnaround within a day of the golden's", all(t26))
    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print("%s  %-95s %s" % ("PASS" if good else "FAIL", label, detail))
    print("verify: %d of %d pass" % (len(RES) - len(fails), len(RES)))
    sys.exit(1 if fails else 0)


def watch(F, X, drv, lst):
    """Runs of three or more no-fault-found removals from one aircraft position by two or more serials inside 120 days
    are the aircraft's; each serial's own removals over its own installed exposure, those windows set aside; two groups
    of serials by marginal likelihood (scipy), the expected excess over a new unit counted for the position over a year
    with another unit in it while the serial is away."""
    U = F["U"]
    C = F["C"]
    res = {}
    for p in sorted(set(U[U["sn"].isin(lst)]["pn"])):
        u = U[U["pn"] == p].copy()
        u["air_drv"] = False
        for (ac, pos), g in u[u["f"] == "NFF"].groupby(["aircraft", "position"]):
            g = g.sort_values("date")
            idx, ds, ss = list(g.index), list(g["date"]), list(g["sn"])
            for i in range(len(idx)):
                j = i
                while j + 1 < len(idx) and (ds[j + 1] - ds[i]).days <= 120:
                    j += 1
                if j - i >= 2 and len(set(ss[i:j + 1])) >= 2:
                    u.loc[idx[i:j + 1], "air_drv"] = True
        win = {}
        for (ac, pos), g in u[u["air_drv"]].groupby(["aircraft", "position"]):
            ds = sorted(g["date"])
            spans, a, b = [], ds[0], ds[0]
            for d in ds[1:]:
                if (d - b).days <= 120:
                    b = d
                else:
                    spans.append((a - pd.Timedelta(days=30), b + pd.Timedelta(days=30)))
                    a = b = d
            spans.append((a - pd.Timedelta(days=30), b + pd.Timedelta(days=30)))
            win[(ac, pos)] = spans
        inwin = u.apply(lambda r: any(a <= r["date"] <= b for a, b in win.get((r["aircraft"], r["position"]), [])), axis=1)
        own = u[~u["air_drv"] & ~inwin & (u["date"] <= M12[1])].groupby("sn").size()
        # exposure by serial on the part's own driver
        e_col = drv[p]
        D = F["day"].copy()
        D["one"] = 1.0
        col = {"ldg": "ldg", "fh": "fh", "days": "one"}[e_col]
        s_by = {ac: g.set_index("date")[col].sort_index() for ac, g in D.groupby("aircraft")}
        cc = C[C["pn"] == p].sort_values(["date", "change_no"])
        expo = {}
        stop = M12[1] + pd.Timedelta(days=1)
        for (ac, pos), g in cc.groupby(["aircraft", "position"]):
            cur, start, first = None, pd.Timestamp("2023-01-01"), True
            for _, r in g.iterrows():
                if r["sn"]:
                    sn = r["sn"] if (first or cur is None) else cur
                    a0 = pd.Timestamp("2023-01-01") if first else start
                    z0 = min(r["date"], stop)
                    seg = s_by[ac][(s_by[ac].index >= a0) & (s_by[ac].index < z0)] if ac in s_by else pd.Series(dtype=float)
                    if e_col == "days":
                        seg = pd.Series(1.0, index=pd.date_range(a0, z0 - pd.Timedelta(days=1))) if z0 > a0 else pd.Series(dtype=float)
                    for wa, wb in win.get((ac, pos), []):
                        seg = seg[(seg.index < wa) | (seg.index > wb)]
                    expo[sn] = expo.get(sn, 0.0) + float(seg.sum())
                    cur = None
                first = False
                if r["serial_on"]:
                    cur, start = r["serial_on"].upper(), r["date"]
            if cur and ac in s_by and start < stop:
                seg = (s_by[ac][(s_by[ac].index >= start) & (s_by[ac].index < stop)] if e_col != "days"
                       else pd.Series(1.0, index=pd.date_range(start, stop - pd.Timedelta(days=1))))
                for wa, wb in win.get((ac, pos), []):
                    seg = seg[(seg.index < wa) | (seg.index > wb)]
                expo[cur] = expo.get(cur, 0.0) + float(seg.sum())
        sns = [s for s in expo if expo[s] > 0]
        n = np.array([float(own.get(s, 0)) for s in sns])
        e = np.array([expo[s] for s in sns])

        def nll(th):
            lo, hi, pi = math.exp(th[0]), math.exp(th[0]) + math.exp(th[1]), 1 / (1 + math.exp(-th[2]))
            l1 = np.log(1 - pi) + n * np.log(lo) - lo * e
            l2 = np.log(pi) + n * np.log(hi) - hi * e
            mx = np.maximum(l1, l2)
            return -float(np.sum(mx + np.log(np.exp(l1 - mx) + np.exp(l2 - mx))))
        mu = n.sum() / e.sum()
        best = None
        for start in ((math.log(mu * 0.8), math.log(mu * 5), -3.0), (math.log(mu * 0.9), math.log(mu * 10), -4.0)):
            r = optimize.minimize(nll, start, method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-8, "fatol": 1e-10})
            if best is None or r.fun < best.fun:
                best = r
        lo, hi, pi = math.exp(best.x[0]), math.exp(best.x[0]) + math.exp(best.x[1]), 1 / (1 + math.exp(-best.x[2]))
        l1 = np.log(1 - pi) + n * np.log(lo) - lo * e
        l2 = np.log(pi) + n * np.log(hi) - hi * e
        post = dict(zip(sns, 1 / (1 + np.exp(l1 - l2))))
        e27 = float(X[{"ldg": "ldg", "fh": "fh", "days": "days"}[e_col]].sum()) / 30 if e_col != "days" else 365.0
        uu = U[(U["pn"] == p) & U["back"].notna() & (U["date"] >= pd.Timestamp("2025-01-01"))]
        tat = float((uu["back"] - uu["date"]).dt.days.mean())
        for sn in [s for s in lst if s in set(U[U["pn"] == p]["sn"])]:
            q = post.get(sn, 0.0)
            lam = q * hi + (1 - q) * lo
            on = 1 / (1 + lam * e27 * tat / 365)
            res[sn] = on * (lam - n.sum() / e.sum()) * e27
    scrap = [s for s, v in res.items() if v >= 1.5]
    return scrap, float(sum(res.values()))


if __name__ == "__main__":
    main()
