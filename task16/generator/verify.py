"""An independent check of the shipped figures, from target/ alone and on its own code path.

    python3 verify.py            reads ../target and figures.json and recomputes the linked record, the rate
                                 achieved, the alerts' effect, the season's conversations, each family's expected
                                 rate and the set with table merges (analysis.py links with per-consignment loops)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
OUT = []


def ck(name, ok, detail=""):
    OUT.append((name, bool(ok), str(detail)))


def key(s):
    s = s.fillna("").astype(str).str.replace(r"\s+", "", regex=True).str.upper()
    return np.where(s.str.match(r"^\d{11}$"), "QP" + s, s)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    t0 = pd.Timestamp("2026-08-03")
    hrs = lambda x: (pd.to_datetime(x) - t0).dt.total_seconds() / 3600.0
    fam_i = pd.read_csv(os.path.join(T, "assistant_intents.csv"), dtype=str).fillna("").set_index("intent").reason_family
    fam_w = pd.read_csv(os.path.join(T, "wrapup_codes.csv"), dtype=str).fillna("").set_index("wrapup_code").reason_family
    a = pd.read_csv(os.path.join(T, "assistant_conversations_2026w32_w45.csv"), dtype=str).drop_duplicates("conversation_id")
    a = a.assign(trk=lambda d: key(d.tracking_no), fam=lambda d: d.intent.map(fam_i).fillna(""))
    a = a[(a.trk != "") & (a.fam != "")].assign(s=lambda d: hrs(d.started_at), e=lambda d: hrs(d.ended_at))
    a["cid"] = np.arange(len(a))
    c = pd.read_csv(os.path.join(T, "acd_call_legs_2026-08-03_2026-11-08.csv"), dtype=str).fillna("")
    c = c[(c.direction == "IN") & (c.leg == "1")].copy()
    u = pd.to_datetime(c.start_utc.str.slice(0, 19))
    c["s"] = ((u + pd.to_timedelta(np.where(u < pd.Timestamp("2026-10-25 01:00"), 2, 1), unit="h")) - t0).dt.total_seconds() / 3600.0
    c["trk"] = key(c.tracking_keyed); c["fam"] = c.wrapup_code.map(fam_w).fillna("")
    acd = pd.read_excel(os.path.join(T, "acd_weekly_summary.xlsx"))
    ck("inbound first legs equal telephony's summary", len(c) == int(acd["Inbound calls handled"].sum()), (len(c), int(acd["Inbound calls handled"].sum())))
    cc = c[c.fam != ""].copy()
    cc["slot"] = np.floor(cc.s * 4)
    by = c.assign(slot=np.floor(c.s * 4)); by = by[by.ivr_path == "BYPASS"][["slot", "queue"]].drop_duplicates().assign(on=True)
    cc = cc.merge(by, on=["slot", "queue"], how="left"); cc["on"] = cc.on.fillna(False).astype(bool)
    cc["keyed"] = cc.trk != ""
    cc["cap"] = cc.groupby(["queue", "on"]).keyed.transform("mean")
    h = pd.read_csv(os.path.join(T, "livechat_sessions_2026w32_w45.csv"), dtype=str).assign(trk=lambda d: key(d.tracking_no), s=lambda d: hrs(d.started_at))
    k = pd.read_csv(os.path.join(T, "case_resolutions_to_2026-11-08.csv"), dtype=str).assign(trk=lambda d: key(d.tracking_no), s=lambda d: hrs(d.created_at))
    k = k[k.origin.isin(["WEB_FORM", "EMAIL"])].copy(); k["day"] = np.floor(k.s / 24).astype(int)
    bl = pd.read_excel(os.path.join(T, "case_backlog_weekly.xlsx"), sheet_name="Open by age")
    bl = bl[(bl.iloc[:, 0] == bl.iloc[:, 0].max()) & (bl["Raised by"] == "Customer")]
    bl = bl[pd.to_numeric(bl["Days open"], errors="coerce").notna()]
    opn = {(q, 97 - int(d)): int(o) for q, d, o in zip(bl.Queue, bl["Days open"], bl["Open cases"])}
    cls = k.groupby(["queue", "day"]).size().to_dict()
    near = lambda q, d: (sum(opn.get((q, x), 0) for x in (d - 1, d, d + 1)) / max(sum(cls.get((q, x), 0) for x in (d - 1, d, d + 1)), 1))
    k["g"] = [near(q, d) for q, d in zip(k.queue, k.day)]
    win = a[a.build.str.startswith("3.") & (a.e >= 56 * 24) & (a.e < 91 * 24)]
    cons = pd.read_csv(os.path.join(T, "consignments_referenced.csv"), dtype=str).fillna("")
    cons["ci"] = cons.outcome_class.map({"ON_TIME": 0, "LATE_1": 1, "LATE_2PLUS": 2, "EXCEPTION": 3})
    cons["due"] = (pd.to_datetime(cons.promised_date) - t0).dt.days
    win = win.merge(cons[["tracking_no", "ci", "depot", "due"]], left_on="trk", right_on="tracking_no", how="left")
    win = win[win.ci.notna()]
    ck("conversations in the window", len(win) == F["conversations"], (len(win), F["conversations"]))

    def follows(ev, strict):
        m = win[["cid", "trk", "e"]].merge(ev, on="trk")
        m = m[(m.s > m.e) if strict else (m.s >= m.e)]
        return m[m.s <= m.e + 168.0]
    fa = follows(a[["trk", "s", "cid"]].rename(columns={"cid": "cid2"}), True); fa = fa[fa.cid != fa.cid2]
    fc = follows(h[h.trk != ""][["trk", "s"]], False)
    fp = follows(cc[cc.keyed][["trk", "s", "cap"]], False)
    fw = follows(k[k.trk != ""][["trk", "s", "g"]], False)
    seen = set(fa.cid) | set(fc.cid) | set(fw.cid)
    linked = seen | set(fp.cid)
    ck("linked rate", abs(100 * (1 - len(linked) / len(win)) - F["linked_rate"]) < 0.06, round(100 * (1 - len(linked) / len(win)), 2))
    miss = fp[~fp.cid.isin(seen)].assign(q=lambda d: 1 - d.cap).groupby("cid").q.prod()
    U = pd.Series(0.0, index=win.cid.values)
    U[list(seen)] = 1.0
    U[miss.index] = 1.0 / (1.0 - miss.values)
    sole = fw[~fw.cid.isin(set(fa.cid) | set(fc.cid) | set(fp.cid))].sort_values("s").groupby("cid").g.first()
    U[sole.index] += sole.values
    win = win.assign(U=U.reindex(win.cid.values).values)
    ach = 100 * (1 - win.U.sum() / len(win))
    ck("rate achieved, all families", abs(ach - F["achieved_all"]) < 0.06, round(ach, 2))
    # the season: conversations per parcel by outcome, the alerts, the plan
    net = pd.read_csv(os.path.join(T, "network_performance_daily.csv"))
    net["due"] = (pd.to_datetime(net.due_date) - t0).dt.days
    plan = pd.read_excel(os.path.join(T, "season_plan_w47_w53.xlsx"), sheet_name=None)
    Wc = (plan["Volumes"]["All depots"].values[:, None] * plan["Service levels"].iloc[:, 1:5].values / 100.0).sum(axis=0)
    nt = plan["Notifications"]; first = pd.to_datetime(nt.iloc[:, 1]).min()
    pilot = set(x.split()[0] for x in nt.iloc[:, 0][pd.to_datetime(nt.iloc[:, 1]) == first]); d0 = (first - t0).days
    allc = a.merge(cons[["tracking_no", "ci", "depot", "due"]], left_on="trk", right_on="tracking_no")
    allc = allc[allc.ci.notna()]
    col = ["on_time", "late_1", "late_2plus", "exception"]

    def rate(ci, deps, lo, hi):
        n = ((allc.ci == ci) & allc.depot.isin(deps) & (allc.due >= lo) & (allc.due < hi)).sum()
        p = net[net.depot.isin(deps) & (net.due >= lo) & (net.due < hi)][col[ci]].sum()
        return n / p, n
    deps = set(net.depot); rest = deps - pilot
    es, ws = [], []
    for ci in (1, 2):
        p1, n1 = rate(ci, pilot, d0, 91); p0, _ = rate(ci, pilot, 0, d0); q1, _ = rate(ci, rest, d0, 91); q0, _ = rate(ci, rest, 0, d0)
        es.append(1 - (p1 / p0) / (q1 / q0)); ws.append(n1)
    e = float(np.average(es, weights=ws))
    ck("the alerts' effect", abs(round(100 * e) - F["alert_effect"]) <= 1, round(100 * e, 1))
    fams = list(F["families"])
    M = np.zeros((len(fams), 4)); r = np.zeros((len(fams), 4))
    for ci in range(4):
        un = allc[(allc.ci == ci) & (allc.due >= 56) & (allc.due < 91)]
        pr = net[(net.due >= 56) & (net.due < 91)]
        if ci in (1, 2):
            un = un[~(un.depot.isin(pilot) & (un.due >= d0))]; pr = pr[~(pr.depot.isin(pilot) & (pr.due >= d0))]
        for i, f in enumerate(fams):
            M[i, ci] = Wc[ci] * (un.fam == f).sum() / pr[col[ci]].sum() * ((1 - e) if ci in (1, 2) else 1.0)
            w = win[(win.fam == f) & (win.ci == ci)]
            r[i, ci] = 1 - w.U.sum() / max(len(w), 1)
    ex = 100 * (M * r).sum(axis=1) / M.sum(axis=1)
    for i, f in enumerate(fams):
        ck("expected rate %s" % f, abs(ex[i] - F["expected"][f]) < 0.11, round(ex[i], 2))
    ck("expected rate, all families", abs(100 * (M * r).sum() / M.sum() - F["expected_all"]) < 0.11, round(100 * (M * r).sum() / M.sum(), 2))
    ck("the families kept", [f for i, f in enumerate(fams) if round(ex[i], 1) >= F["line"]] == F["keep"])
    ck("conversations a week over the season", abs(M.sum() / len(plan["Volumes"]) - F["per_week"]) < 60, round(M.sum() / len(plan["Volumes"])))
    ck("late and exception share of season conversations", abs(100 * M[:, 1:].sum() / M.sum() - F["late_share"]) < 0.11)
    bad = [x for x in OUT if not x[1]]
    for n, ok, d in OUT:
        print("%s  %s  %s" % ("ok  " if ok else "FAIL", n, d))
    print("verify: %d of %d" % (len(OUT) - len(bad), len(OUT)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
