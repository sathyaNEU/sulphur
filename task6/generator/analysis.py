"""task6's golden, computed from the shipped pack alone: each service's December 2026 latency SLI (each kept server
span counted at its trace's edge keep share, from the load balancer's hourly request counts), its verdict against its
budget, and the asks that read the SLI's own numerator (each service's over-threshold December requests: their shares,
the order the engineers start in, the share the services that ran over served together and the requests beyond their
budgets) and the customer-facing incident minutes in which an incident named one of those services, by half. The
ladder's rungs are computed beside the golden for the checks."""
import csv
import datetime as dt
import json
import os

import numpy as np
import pyarrow.parquet as pq
from openpyxl import load_workbook

import common as K

DEC0_NS = int((dt.datetime(2026, 12, 1) - dt.datetime(1970, 1, 1)).total_seconds()) * 10 ** 9
H = K.REVIEW_HOURS


def catalogue(target):
    wb = load_workbook(os.path.join(target, K.FILES["catalogue"]), read_only=True)
    ws = wb["Services"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    out = [dict(zip(head, r)) for r in rows[1:] if r[0]]
    return out


class Golden:
    def __init__(self, target):
        self.t = target
        self.cat = catalogue(target)
        self.by_trace = {c["Tracing service name"]: c["Service"] for c in self.cat}
        self.by_tg2 = {c["Load balancer target group (from 1 Jul 2026)"]: c["Service"] for c in self.cat}
        slo = self.slo_table()
        self.thr = {s: slo[s][0] for s in slo}
        self.bud = {s: slo[s][1] for s in slo}

    def slo_table(self):
        from docx import Document
        d = Document(os.path.join(self.t, K.FILES["slo"]))
        tab = d.tables[0]
        out = {}
        for row in tab.rows[1:]:
            c = [x.text for x in row.cells]
            out[c[0]] = (float(c[2].replace(",", "")), float(c[3].rstrip("%")))
        return out

    # ------------------------------------------------------------ the main call
    def spans(self):
        """The kept server spans that started in December, re-sent rows and health probes removed, each with the
        service and start hour of the request that began its trace (None where that span is not in the export)."""
        tb = pq.read_table(os.path.join(self.t, K.FILES["spans"]),
                           columns=["trace_id", "span_id", "parent_span_id", "service_name", "span_name", "span_kind",
                                    "start_time_unix_nano", "end_time_unix_nano"]).to_pydict()
        seen = set()
        rows = []
        for tid, sid, pid, svc, name, kind, t0, t1 in zip(tb["trace_id"], tb["span_id"], tb["parent_span_id"],
                                                          tb["service_name"], tb["span_name"], tb["span_kind"],
                                                          tb["start_time_unix_nano"], tb["end_time_unix_nano"]):
            if sid in seen or name == "GET /healthz":
                continue
            seen.add(sid)
            rows.append((tid, sid, pid, self.by_trace[svc], kind, (t0 - DEC0_NS) // (3600 * 10 ** 9),
                         (t1 - t0) / 1e6))
        root = {}
        for tid, sid, pid, svc, kind, h, ms in rows:
            if kind == "SPAN_KIND_SERVER" and pid == "":
                root[tid] = (svc, int(h))
        self.n_client = sum(1 for x in rows if x[4] == "SPAN_KIND_CLIENT")
        self.ids = {x[1] for x in rows}
        self.parent_of = {x[1]: x[2] for x in rows}
        out = []
        for tid, sid, pid, svc, kind, h, ms in rows:
            if kind != "SPAN_KIND_SERVER" or not 0 <= h < H:
                continue
            out.append((svc, int(h), ms, root.get(tid), pid))
        return out

    def counts(self):
        N = {s: np.zeros(H, dtype=np.int64) for s in K.SVC}
        E = {s: np.zeros(H, dtype=np.int64) for s in K.SVC}
        with open(os.path.join(self.t, K.FILES["lb_h2"])) as fh:
            for row in csv.DictReader(fh):
                t = dt.datetime.strptime(row["TimePeriodStart"], "%Y-%m-%dT%H:%M:%SZ")
                if t < dt.datetime(2026, 12, 1):
                    continue
                h = int((t - dt.datetime(2026, 12, 1)).total_seconds() // 3600)
                s = self.by_tg2[row["TargetGroupName"]]
                N[s][h] = int(row["RequestCount"])
                E[s][h] = int(row["HTTPCode_Target_5XX_Count"])
        return N, E

    def main(self):
        sp = self.spans()
        N, E = self.counts()
        hod, day = np.arange(H) % 24, np.arange(H) // 24
        # each edge service's kept share of its requests, hour by hour: its kept root spans over the balancer's count
        Kroot = {e: np.zeros(H, dtype=np.int64) for e in K.EDGE}
        for svc, h, ms, rt, pid in sp:
            if pid == "":
                Kroot[svc][h] += 1
        for e in K.EDGE:
            assert not ((Kroot[e] == 0) & (N[e] > 0)).any(), e
        out = {}
        for s in K.SVC:
            mine = [x for x in sp if x[0] == s]
            h_own = np.array([x[1] for x in mine], dtype=np.int64)
            slow = np.array([x[2] > self.thr[s] for x in mine], dtype=float)
            Kh = np.bincount(h_own, minlength=H).astype(float)
            Sh = np.bincount(h_own, weights=slow, minlength=H)
            w_root, w_ownh, orphan = [], [], []
            for svc, h, ms, rt, pid in mine:
                if rt is None:                         # the request that began the trace is not in the export
                    orphan.append(True)
                    w_root.append(N[s][h] / max(Kh[h], 1))
                    w_ownh.append(N[s][h] / max(Kh[h], 1))
                else:
                    e, he = rt
                    orphan.append(False)
                    w_root.append(N[e][he] / Kroot[e][he])
                    w_ownh.append(N[e][h] / max(Kroot[e][h], 1))
            w_root, w_ownh, orphan = np.array(w_root), np.array(w_ownh), np.array(orphan, dtype=bool)
            Ns = float(N[s].sum())
            sli = 100 * (w_root * slow).sum() / Ns
            num_h = np.bincount(h_own, weights=w_root * slow, minlength=H)
            den_h = np.bincount(h_own, weights=w_root, minlength=H)

            def strat(g):
                Ng, Kg, Sg = np.bincount(g, N[s].astype(float)), np.bincount(g, Kh), np.bincount(g, Sh)
                return 100 * (np.where(Kg > 0, Ng / np.maximum(Kg, 1), 0) * Sg).sum() / Ns
            w_drop = np.where(orphan, 0.0, w_root)
            out[s] = {"sli": sli, "sli1": K.r1(sli), "budget": self.bud[s], "threshold": self.thr[s],
                      "over": K.r1(sli) > self.bud[s], "requests": int(Ns), "kept": int(Kh.sum()),
                      "kept_slow": int(Sh.sum()), "orphans": int(orphan.sum()),
                      "weighted_requests": float(w_root.sum()),
                      "hajek": 100 * (w_root * slow).sum() / w_root.sum(),
                      "calibrated": 100 * np.where(den_h > 0, N[s] * num_h / np.maximum(den_h, 1e-12), 0).sum() / Ns,
                      "own_hour": 100 * (w_ownh * slow).sum() / Ns,
                      "orphans_dropped": 100 * (w_drop * slow).sum() / Ns,
                      "unweighted": 100 * Sh.sum() / Kh.sum(), "by_day": strat(day), "by_hour_of_day": strat(hod),
                      "by_service_hour": strat(np.arange(H)),
                      "lb_5xx_share": 100 * E[s].sum() / Ns}
            # the root mix of the service's kept spans against the mix its weights give
            mix_k, mix_w = {}, {}
            for (svc, h, ms, rt, pid), wv in zip(mine, w_root):
                key = rt[0] if rt else None
                mix_k[key] = mix_k.get(key, 0) + 1
                mix_w[key] = mix_w.get(key, 0.0) + wv
            out[s]["root_mix_kept"] = {k: v / len(mine) for k, v in mix_k.items()}
            out[s]["root_mix_weighted"] = {k: v / w_root.sum() for k, v in mix_w.items()}
        return out

    # ------------------------------------------------------------ the incident ask: minutes by half
    def incident_intervals(self, backdate=False):
        """Each service's customer-facing incident intervals (UTC): an incident in incidents_2026.csv is matched to its
        status page post by component and time; it runs to the last of the post's components back to operational; a
        service counts from the moment incident_timeline_2026.csv names it (backdate: from the declaration, the
        export's final list read for the whole incident)."""
        import asks as A
        st = json.load(open(os.path.join(self.t, K.FILES["status"])))

        def utc(local):
            t = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
            for off in (1, 0):
                u = t - dt.timedelta(hours=off)
                if A.lisbon_offset(u) == off:
                    return u
            return t
        posts = [{"components": set(p["components"]), "created": utc(p["created_at"])} for p in st["incidents"]]
        ops = {}
        for c in st["component_status_changes"]:
            if c["status"] == "operational":
                ops.setdefault(c["component"], []).append(utc(c["at"]))
        for v in ops.values():
            v.sort()
        named = {}
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["timeline"]))):
            if row["event"] == "service added":
                named[(row["incident_id"], row["detail"])] = dt.datetime.strptime(row["at_utc"], "%Y-%m-%d %H:%M:%S")
        comp = {c["Service"]: c["Status page component"] for c in self.cat}
        iv = {s: [] for s in K.SVC}
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["incidents"]))):
            decl = dt.datetime.strptime(row["declared_at_utc"], "%Y-%m-%d %H:%M:%S")
            names = row["services"].split(";")
            # the post for this incident: on a component of a service it named, opened in the minutes after it was
            # declared
            match = [p for p in posts if p["components"] & {comp[self.by_trace[x]] for x in names}
                     and dt.timedelta(0) <= p["created"] - decl.replace(second=0) <= dt.timedelta(minutes=15)]
            if not match:
                continue
            assert len(match) == 1
            p = match[0]
            end = max(min(t for t in ops[c] if t > p["created"]) for c in p["components"])
            for x in names:
                a_ = decl if backdate else max(decl, named[(row["incident_id"], x)])
                if a_ < end:
                    iv[self.by_trace[x]].append((a_, end))
        return iv

    def incidents(self, services=None, backdate=False):
        """Customer-facing incident minutes by half (PR-SLO-3 5.2 and 5.4): for each service, or with `services` the
        minutes in which an incident named at least one of them, each minute counted once."""
        iv = self.incident_intervals(backdate)
        if services is not None:
            return union_minutes([x for s in services for x in iv[s]])
        return {s: union_minutes(lst) for s, lst in iv.items()}

    def run(self):
        main = self.main()
        over = [s for s in K.SVC if main[s]["over"]]
        N = {s: main[s]["requests"] for s in K.SVC}
        prog = programme({s: main[s]["sli"] for s in K.SVC}, N, self.bud)
        shallow = programme({s: main[s]["by_service_hour"] for s in K.SVC}, N, self.bud)
        return {"main": main, "over": over, "programme": prog, "shallow": shallow,
                "incidents": self.incidents(over), "incidents_by_service": self.incidents(),
                "shallow_incidents": self.incidents(shallow["over"])}


H1_END = dt.datetime(2026, 6, 30, 23, 0)            # 1 July 00:00 Lisbon


def union_minutes(lst):
    """Minutes of a set of intervals in each half of 2026, overlaps counted once, rounded at the end only."""
    merged = []
    for a_, b_ in sorted(lst):
        if merged and a_ <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b_)
        else:
            merged.append([a_, b_])
    m = [0.0, 0.0]
    for a_, b_ in merged:
        for i, (lo, hi) in enumerate(((dt.datetime(2026, 1, 1), H1_END), (H1_END, dt.datetime(2027, 1, 1)))):
            lo_, hi_ = max(a_, lo), min(b_, hi)
            if hi_ > lo_:
                m[i] += (hi_ - lo_).total_seconds() / 60
    return m


def programme(sli, N, bud):
    """The asks that read the SLI's numerator: each service's over-threshold December requests (its SLI times its
    December requests, which is its weighted kept spans over the threshold), their share of all the services' total,
    the services over budget in the order of their over-threshold requests, the share those services served together
    and how many more over-threshold requests than their budgets allow."""
    slow = {s: sli[s] / 100.0 * N[s] for s in K.SVC}
    tot = sum(slow.values())
    over = [s for s in K.SVC if K.r1(sli[s]) > bud[s]]
    order = sorted(over, key=lambda s: -slow[s])
    return {"slow": slow, "total": tot, "share": {s: 100.0 * slow[s] / tot for s in K.SVC}, "over": over,
            "order": order, "over_share": 100.0 * sum(slow[s] for s in over) / tot,
            "beyond": sum(slow[s] - bud[s] / 100.0 * N[s] for s in over)}
