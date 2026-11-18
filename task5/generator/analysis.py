"""The golden's reading of the pack: every shipped table and export brought to one coding and one schema, as the
arrays core.py's estimators take. Nothing here knows the world; what is not in a shipped file is NaN."""
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import core as C
import docs
import pack

HOME, HOSTS, STATES = C.HOME, C.HOSTS, C.STATES
NY, LAST, Y0 = C.NY, C.LAST, C.Y0
F = dict(pack.FILES)
F.update(docs.FILES)


def codes(target):
    df = pd.read_csv(os.path.join(target, F["codes"]), dtype=str)
    by = {}
    for _, r in df.iterrows():
        for k in ("area_code", "alpha3", "register_code", "name", "official_name"):
            by[str(r[k]).strip().lower()] = r["name"]
    return by


def register(target, by, year_of="move_date"):
    """Orlava's register events: a repeated event number counted once, the state read from its code or, where the
    clerk left the code blank, from the text; the year is the year of the move (Regulation 7/2009, article 2(e))."""
    df = pd.read_csv(os.path.join(target, F["register"]), dtype=str, keep_default_na=False)
    rows = len(df)
    df = df.drop_duplicates("event_no")
    key = np.where(df["state_code"].str.strip() != "", df["state_code"], df["state_text"])
    df["state"] = pd.Series(key, index=df.index).str.strip().str.lower().map(by)
    df["cit"] = df["citizenship"].str.strip().str.lower().map(by)
    assert df["state"].notna().all() and df["cit"].notna().all()
    df["y"] = df[year_of].str[:4].astype(int) - Y0
    df = df[(df["y"] >= 0) & (df["y"] < NY)]
    lag = (pd.to_datetime(df["entered_on"]) - pd.to_datetime(df["move_date"])).dt.days
    last_move, last_entry = pd.Timestamp(Y0 + NY - 1, 12, 31), pd.to_datetime(df["entered_on"]).max()
    reach = int((last_entry - last_move).days)               # the lag the file still holds for a move on the last day
    tail = [int((df["move_date"] == str((last_move - pd.Timedelta(days=k)).date())).sum()) for k in range(int(lag.max()) - reach)]
    out = dict(rows=rows, events=len(df), lag_max=int(lag.max()),
               entered_last=str(df["entered_on"].max()), blank_codes=int((df["state_code"].str.strip() == "").sum()),
               lag_reach=reach, lag_over_reach_pct=float(100.0 * (lag > reach).mean()), tail_moves=int(sum(tail)),
               tail_outstanding=float(sum(n * (lag > reach + k).mean() for k, n in enumerate(tail))))
    dereg, reg = df["event_type"] == "deregistration_abroad", df["event_type"] == "registration_from_abroad"
    own = df["cit"] == HOME

    def series(mask, col, val):
        return np.bincount(df.loc[mask & (df[col] == val), "y"], minlength=NY).astype(float)
    out["B"] = {h: series(dereg & own, "state", h) for h in HOSTS}            # citizens leaving for h
    out["D"] = {h: series(reg & own, "state", h) for h in HOSTS}              # citizens arriving from h
    out["A"] = {h: series(reg & ~own, "cit", h) for h in HOSTS}               # h's citizens arriving
    out["C"] = {h: series(dereg & ~own, "cit", h) for h in HOSTS}             # h's citizens leaving
    out["A_other"] = series(reg & ~own, "cit", "Other")                       # citizens of states outside the Area arriving
    return out


def tables(target, by):
    """The area office's Tables A to D: for each table, reporting state, partner, year, sex and age group the latest
    release (article 6(3)), summed over sex and age."""
    df = pd.read_csv(os.path.join(target, F["tables"]), dtype=str)
    rows = len(df)
    df["persons"] = df["persons"].astype(int)
    releases = list(df["release"].unique())
    df = df.sort_values("release", kind="mergesort").drop_duplicates(["table", "reporting_state", "partner", "reference_year", "sex", "age_group"], keep="last")
    df["rep"] = df["reporting_state"].str.lower().map(by)
    df["par"] = df["partner"].str.lower().map(by)
    df["y"] = df["reference_year"].astype(int) - Y0
    g = df.groupby(["table", "rep", "par", "y"])["persons"].sum()
    out = {}
    for (t, rep, par), s in g.groupby(level=[0, 1, 2]):
        a = np.full(NY, np.nan)
        for (_, _, _, y), v in s.items():
            a[y] = v
        out[t, rep, par] = a
    return out, rows, len(df), releases


def load(target, year_of="move_date"):
    by = codes(target)
    reg = register(target, by, year_of)
    tab, table_rows, table_cells, releases = tables(target, by)
    recA, recD = {}, {}
    for i in STATES:
        for j in STATES:
            if i == j:
                continue
            recA[i, j] = reg["A"][i] if j == HOME else tab["A", j, i]
            recD[i, j] = reg["B"][j] if i == HOME else tab["B", i, j]
    vit = pd.read_csv(os.path.join(target, F["vital"]), dtype=str)
    vit["nat"] = vit["live_births"].astype(int) - vit["deaths"].astype(int)
    vit["rep"] = vit["reporting_state"].str.lower().map(by)
    vit["cit"] = vit["citizenship"].str.lower().map(by)
    wb = load_workbook(os.path.join(target, F["census"]), read_only=True, data_only=True)

    def stock(sheet, host):
        rows = list(wb[sheet].iter_rows(values_only=True))
        head = [str(c) for c in rows[3]]
        col = head.index([k for k, v in by.items() if v == HOME and k.isdigit()][0])
        for r in rows[4:]:
            if r[0] is not None and by.get(str(r[0]).lower()) == host:
                return float(r[col])
        raise KeyError(host)
    ws = load_workbook(os.path.join(target, F["count16"]), read_only=True, data_only=True).active
    n16 = [float(r[1]) for r in ws.iter_rows(values_only=True) if r[0] is not None and by.get(str(r[0]).lower()) == HOME][0]
    ws = load_workbook(os.path.join(target, F["c14"]), read_only=True, data_only=True).active
    census_in, census_in_other = {}, None
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] is not None and by.get(str(r[0]).lower()) in HOSTS:
            census_in[by[str(r[0]).lower()]] = float(r[4])
        elif r[0] == "Other citizenships":
            census_in_other = float(r[4])
    R = dict(recA=recA, recD=recD, census_in=census_in, host={})
    for h in HOSTS:
        v = vit[(vit["rep"] == h) & (vit["cit"] == HOME)]
        nat = np.full(NY, np.nan)
        nat[v["reference_year"].astype(int).to_numpy() - Y0] = v["nat"].to_numpy()
        R["host"][h] = dict(n11=stock("T1 citizenship 2011", h), n21=stock("T1 citizenship 2021", h),
                            dep=tab["C", h, HOME], ret=reg["D"][h], nat=nat, n16=n16 if h == C.REFHOST else None)
    R["meta"] = dict(register_rows=reg["rows"], register_events=reg["events"], lag_max=reg["lag_max"], table_rows=table_rows,
                     lag_reach=reg["lag_reach"], lag_over_reach_pct=reg["lag_over_reach_pct"], tail_moves=reg["tail_moves"],
                     tail_outstanding=reg["tail_outstanding"],
                     table_cells=table_cells, entered_last=reg["entered_last"], blank_codes=reg["blank_codes"],
                     releases=sorted(set(k[:4] for k in releases)))
    R["census_in_other"] = census_in_other
    # every foreign citizenship's account in every host, as the same files hold it (the census closure the pack also affords)
    def stocks(sheet):
        rows = list(wb[sheet].iter_rows(values_only=True))
        head = [by.get(str(c).lower()) for c in rows[3]]
        got = {}
        for r in rows[4:]:
            host = by.get(str(r[0]).lower()) if r[0] is not None else None
            if host in HOSTS:
                for k, c in enumerate(head):
                    if k and c in STATES and c != host and r[k] is not None:
                        got[host, c] = float(r[k])
        return got
    natc = {}
    for (h, c), v in vit.groupby(["rep", "cit"]):
        if h in HOSTS and c in STATES and c != h:
            a = np.full(NY, np.nan)
            a[v["reference_year"].astype(int).to_numpy() - Y0] = v["nat"].to_numpy()
            natc[h, c] = a
    R["cit"] = dict(n11=stocks("T1 citizenship 2011"), n21=stocks("T1 citizenship 2021"), nat=natc,
                    dep={(h, c): tab["C", h, c] for h in HOSTS for c in STATES if c != h})
    R["reg"], R["tab"] = reg, tab
    return R


def same_as_world(R, RW):
    """Every array the estimators read, against the world's own record of it: the list of differences (empty)."""
    bad = []
    for (i, j), a in RW["recA"].items():
        n = NY if j == HOME else LAST
        if not np.array_equal(R["recA"][i, j][:n], a[:n]):
            bad.append(("recA", i, j))
    for (i, j), a in RW["recD"].items():
        n = NY if i == HOME else LAST
        if not np.array_equal(R["recD"][i, j][:n], a[:n]):
            bad.append(("recD", i, j))
    for h in HOSTS:
        q, w = R["host"][h], RW["host"][h]
        for k, n in (("dep", LAST), ("ret", NY), ("nat", LAST)):
            if not np.array_equal(q[k][:n], w[k][:n]):
                bad.append((k, h))
        for k in ("n11", "n21", "n16"):
            if q[k] != w[k]:
                bad.append((k, h))
        if R["census_in"][h] != RW["census_in"][h]:
            bad.append(("census_in", h))
    return bad


if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    R = load(t)
    print(R["meta"])
    print("differences from the world's record:", same_as_world(R, C.records(C.simulate())))
    print({h: round(C.chain(R, h)["n"]) for h in HOSTS})
