"""task6's golden, computed from the shipped pack alone (architecture 7), with the hurried passes beside it.

The results, in the order the review needs them:
  R1  each service's customer-facing incident minutes in each half of 2026 (the incident tool, its timeline and the
      status page reconciled; a service counts from when the tool added it, PR-SLO-3 5.2 and 5.4);
  R2  the service that owned the root cause of each December customer-facing incident: per span name, each named
      service's own handling time (its span less the union of the calls it was waiting on) against a load curve fitted
      on December's incident-free hours, the onset of each sustained rise dated by a changepoint, the earliest rise
      owning the cause (PR-SLO-3 3.3);
  R3  every service's December latency SLI: each kept server span counted at its trace root's hourly keep share (the
      balancer's request count over the roots the store kept), the requests left out by PR-SLO-3 3.2 removed;
  R4  a 90 per cent interval on each over-budget service's SLI for the trace store's sample: strata are the root
      service's hours, the units are whole traces;
  R5  the services over budget; R6 their start order, each one's share of the over-threshold requests all the SLIs
      count, the share together and the over-threshold requests beyond their budgets.
"""
import csv
import datetime as dt
import json
import os

import numpy as np
import pyarrow.parquet as pq
from openpyxl import load_workbook

import common as K

DEC0 = dt.datetime(2026, 12, 1)
DEC0_NS = int((DEC0 - dt.datetime(1970, 1, 1)).total_seconds()) * 10 ** 9
H = K.REVIEW_HOURS
H1_END = dt.datetime(2026, 6, 30, 23, 0)            # 1 July 00:00 Lisbon
Z90 = 1.6448536269514722


def catalogue(target):
    wb = load_workbook(os.path.join(target, K.FILES["catalogue"]), read_only=True)
    rows = list(wb["Services"].iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:] if r[0]]


def lisbon_offset(t_utc):
    def last_sunday(m):
        d = dt.datetime(2026, m, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)
    return 1 if last_sunday(3) <= t_utc < last_sunday(10) else 0


def utc_of_lisbon(local):
    t = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
    for off in (1, 0):
        u = t - dt.timedelta(hours=off)
        if lisbon_offset(u) == off:
            return u
    return t


def union_minutes(lst, halves=True):
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


def sec_of(t):
    return (t - DEC0).total_seconds()


class Golden:
    def __init__(self, target, dedupe=True, drop_probes=True):
        self.t = target
        self.dedupe, self.drop_probes = dedupe, drop_probes
        self.cat = catalogue(target)
        self.by_trace = {c["Tracing service name"]: c["Service"] for c in self.cat}
        self.by_tg2 = {c["Load balancer target group (from 1 Jul 2026)"]: c["Service"] for c in self.cat}
        self.comp = {c["Service"]: c["Status page component"] for c in self.cat}
        self.thr, self.bud = self.slo_table()
        self._load()

    def slo_table(self):
        from docx import Document
        d = Document(os.path.join(self.t, K.FILES["slo"]))
        thr, bud = {}, {}
        for row in d.tables[0].rows[1:]:
            c = [x.text for x in row.cells]
            thr[c[0]] = float(c[2].replace(",", ""))
            bud[c[0]] = float(c[3].rstrip("%"))
        return thr, bud

    # ------------------------------------------------------------------ the records
    def _load(self):
        tb = pq.read_table(os.path.join(self.t, K.FILES["spans"]),
                           columns=["trace_id", "span_id", "parent_span_id", "service_name", "span_name", "span_kind",
                                    "start_time_unix_nano", "end_time_unix_nano"]).to_pydict()
        seen = set()
        keep = []
        for i, (sid, name) in enumerate(zip(tb["span_id"], tb["span_name"])):
            if (self.dedupe and sid in seen) or (self.drop_probes and name == "GET /healthz"):
                continue
            seen.add(sid)
            keep.append(i)
        g = lambda k: [tb[k][i] for i in keep]
        self.tr = np.array(g("trace_id"))
        self.sid = np.array(g("span_id"))
        self.par = np.array(g("parent_span_id"))
        self.svc = np.array([self.by_trace[x] for x in g("service_name")])
        self.name = np.array(g("span_name"))
        self.kind = np.array(g("span_kind"))
        t0 = np.array(g("start_time_unix_nano"), dtype=np.int64)
        t1 = np.array(g("end_time_unix_nano"), dtype=np.int64)
        self.t0 = (t0 - DEC0_NS) / 1e9
        self.ms = (t1 - t0) / 1e6
        self.h = np.floor(self.t0 / 3600).astype(int)
        self.server = self.kind == "SPAN_KIND_SERVER"
        self.root = self.server & (self.par == "")
        # the balancer's December counts
        self.N = {s: np.zeros(H) for s in K.SVC}
        with open(os.path.join(self.t, K.FILES["lb_h2"])) as fh:
            for row in csv.DictReader(fh):
                t = dt.datetime.strptime(row["TimePeriodStart"], "%Y-%m-%dT%H:%M:%SZ")
                if t >= DEC0:
                    self.N[self.by_tg2[row["TargetGroupName"]]][int((t - DEC0).total_seconds() // 3600)] = \
                        float(row["RequestCount"])
        # roots the store kept, per edge service and hour; each trace's root service and hour
        self.Kroot = {e: np.zeros(H) for e in K.SVC}
        self.root_of = {}
        for i in np.nonzero(self.root & (self.h >= 0) & (self.h < H))[0]:
            self.Kroot[self.svc[i]][self.h[i]] += 1
            self.root_of[self.tr[i]] = (self.svc[i], int(self.h[i]))
        # own handling time: a server span less the union of the calls it made
        idx = {sid: i for i, sid in enumerate(self.sid)}
        kids = {}
        for i in np.nonzero(self.kind == "SPAN_KIND_CLIENT")[0]:
            kids.setdefault(self.par[i], []).append((self.t0[i], self.t0[i] + self.ms[i] / 1000))
        self.own = self.ms.copy()
        for i in np.nonzero(self.server)[0]:
            ch = kids.get(self.sid[i])
            if not ch:
                continue
            ch.sort()
            tot, cur = 0.0, None
            for a_, b_ in ch:
                if cur is None or a_ > cur[1]:
                    if cur:
                        tot += cur[1] - cur[0]
                    cur = [a_, b_]
                else:
                    cur[1] = max(cur[1], b_)
            tot += cur[1] - cur[0]
            self.own[i] = max(0.001, self.ms[i] - tot * 1000)
        self.dec = self.server & (self.h >= 0) & (self.h < H)

    def weights(self, how="root"):
        """Each December server span's weight: its trace root's hourly keep share ("root"), its own service's hourly
        count over its own kept spans ("own"), the root's share at the span's own hour ("root_span_hour"), or one."""
        w = np.ones(len(self.t0))
        own_k = {s: np.bincount(self.h[self.dec & (self.svc == s)], minlength=H).astype(float) for s in K.SVC}
        for i in np.nonzero(self.dec)[0]:
            s, h = self.svc[i], self.h[i]
            fallback = self.N[s][h] / max(own_k[s][h], 1)
            if how == "unw":
                w[i] = 1.0
            elif how == "own":
                w[i] = fallback
            else:
                ro = self.root_of.get(self.tr[i])
                if ro is None:
                    w[i] = fallback
                else:
                    e, he = ro
                    hh = he if how == "root" else h
                    w[i] = self.N[e][hh] / self.Kroot[e][hh] if self.Kroot[e][hh] > 0 else fallback
        return w

    # ------------------------------------------------------------------ incidents
    def incidents(self):
        st = json.load(open(os.path.join(self.t, K.FILES["status"])))
        posts = [{"components": set(p["components"]), "created": utc_of_lisbon(p["created_at"])} for p in st["incidents"]]
        ops = {}
        for c in st["component_status_changes"]:
            if c["status"] == "operational":
                ops.setdefault(c["component"], []).append(utc_of_lisbon(c["at"]))
        for v in ops.values():
            v.sort()
        named = {}
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["timeline"]))):
            if row["event"] == "service added":
                named[(row["incident_id"], self.by_trace[row["detail"]])] = dt.datetime.strptime(
                    row["at_utc"], "%Y-%m-%d %H:%M:%S")
        out = []
        for row in csv.DictReader(open(os.path.join(self.t, K.FILES["incidents"]))):
            decl = dt.datetime.strptime(row["declared_at_utc"], "%Y-%m-%d %H:%M:%S")
            names = [self.by_trace[x] for x in row["services"].split(";")]
            match = [p for p in posts if p["components"] & {self.comp[x] for x in names}
                     and dt.timedelta(0) <= p["created"] - decl.replace(second=0) <= dt.timedelta(minutes=15)]
            if not match:
                continue
            assert len(match) == 1, row["incident_id"]
            p = match[0]
            end = max(min(t for t in ops[c] if t > p["created"]) for c in p["components"])
            out.append({"id": row["incident_id"], "declared": decl, "end": end,
                        "resolved": dt.datetime.strptime(row["resolved_at_utc"], "%Y-%m-%d %H:%M:%S"),
                        "named": [(x, named[(row["incident_id"], x)]) for x in names],
                        "review": row["review_status"], "cause": row["root_cause_service"]})
        return out

    def december(self):
        return [x for x in self.incidents() if x["declared"] >= DEC0]

    def minutes(self, backdate=False, tool_end=False):
        """R1: each service's customer-facing incident minutes by half (backdate: every service from the declaration;
        tool_end: the incident tool's resolve time as the end)."""
        iv = {s: [] for s in K.SVC}
        for x in self.incidents():
            end = x["resolved"] if tool_end else x["end"]
            for s, t in x["named"]:
                a_ = x["declared"] if backdate else max(x["declared"], t)
                if a_ < end:
                    iv[s].append((a_, end))
        return {s: union_minutes(v) for s, v in iv.items()}

    # ------------------------------------------------------------------ R2: the root cause
    def load_curves(self, incs):
        """Per service and span name: a quadratic in the log of the service's hourly request count, fitted to the
        hourly median of the log own handling time over December's hours clear of every customer-facing incident."""
        quiet = np.ones(H, dtype=bool)
        for x in incs:
            a_ = int(sec_of(x["declared"]) // 3600) - 3
            b_ = int(sec_of(x["end"]) // 3600) + 1
            quiet[max(0, a_):min(H, b_ + 1)] = False
        curves = {}
        for s in K.SVC:
            m = self.dec & (self.svc == s)
            for n in np.unique(self.name[m]):
                mm = m & (self.name == n)
                hh = self.h[mm]
                lo = np.log(self.own[mm])
                xs, ys = [], []
                for hv in np.unique(hh):
                    if quiet[hv]:
                        v = lo[hh == hv]
                        if len(v) >= 3:
                            xs.append(np.log(self.N[s][hv] + 1))
                            ys.append(np.median(v))
                if len(xs) >= 30:
                    curves[(s, n)] = np.polyfit(np.array(xs), np.array(ys), 2)
        return curves

    def onsets(self, x, curves, lead_min=180):
        """For each service the incident named: the earliest sustained rise of its own handling time over its load
        curve, by span name (a single changepoint on the time-ordered residuals), with the size of the rise."""
        a_, b_ = sec_of(x["declared"]) - lead_min * 60, sec_of(x["end"])
        out = {}
        for s, _t in x["named"]:
            best = None
            for (ss, n), cf in curves.items():
                if ss != s:
                    continue
                m = self.dec & (self.svc == s) & (self.name == n) & (self.t0 >= a_) & (self.t0 < b_)
                if m.sum() < 10:
                    continue
                o = np.argsort(self.t0[m])
                t = self.t0[m][o]
                r = (np.log(self.own[m]) - np.polyval(cf, np.log(self.N[s][self.h[m]] + 1)))[o]
                cs = np.cumsum(r)
                n_ = len(r)
                bestk, score = None, -1.0
                for k in range(4, n_ - 4):
                    m1, m2 = cs[k - 1] / k, (cs[-1] - cs[k - 1]) / (n_ - k)
                    sc = k * (n_ - k) / n_ * (m2 - m1) ** 2
                    if sc > score:
                        bestk, score = k, sc
                if bestk is None:
                    continue
                m1 = cs[bestk - 1] / bestk
                m2 = (cs[-1] - cs[bestk - 1]) / (n_ - bestk)
                if m2 - m1 >= np.log(1.4) and m2 >= np.log(1.3):
                    cand = (t[bestk], float(np.exp(m2 - m1)), n)
                    if best is None or cand[0] < best[0]:
                        best = cand
            out[s] = best
        return out

    def attribute(self, incs=None, curves=None):
        incs = incs or self.december()
        curves = curves or self.load_curves(incs)
        att, detail = {}, {}
        for x in incs:
            on = self.onsets(x, curves)
            cands = {s: v for s, v in on.items() if v is not None}
            fault = min(cands, key=lambda s: cands[s][0]) if cands else x["named"][0][0]
            att[x["id"]] = fault
            detail[x["id"]] = on
        return att, detail

    def window_excess(self, incs=None, curves=None):
        """The careful but hurried attribution: over the whole window from the declaration to the end, each named
        service's largest median excess of own handling time over its load curve, by span name."""
        incs = incs or self.december()
        curves = curves or self.load_curves(incs)
        att = {}
        for x in incs:
            a_, b_ = sec_of(x["declared"]), sec_of(x["end"])
            best = (0.0, x["named"][0][0])
            for s, _t in x["named"]:
                for (ss, n), cf in curves.items():
                    if ss != s:
                        continue
                    m = self.dec & (self.svc == s) & (self.name == n) & (self.t0 >= a_) & (self.t0 < b_)
                    if m.sum() < 5:
                        continue
                    ex = float(np.median(np.log(self.own[m]) - np.polyval(cf, np.log(self.N[s][self.h[m]] + 1))))
                    if ex > best[0]:
                        best = (ex, s)
            att[x["id"]] = best[1]
        return att

    # ------------------------------------------------------------------ R3 to R6
    def excluded(self, att, incs=None, from_declaration=False):
        """Per service, the stretches PR-SLO-3 3.2 leaves out under an attribution {incident: service at fault}."""
        incs = incs or self.december()
        ex = {s: [] for s in K.SVC}
        for x in incs:
            f = att.get(x["id"])
            if f == "__none__":
                continue
            for s, t in x["named"]:
                if s != f:
                    a_ = x["declared"] if from_declaration else max(x["declared"], t)
                    ex[s].append((sec_of(a_), sec_of(x["end"])))
        return ex

    def slis(self, w, ex, ht=False):
        out = {}
        for s in K.SVC:
            m = self.dec & (self.svc == s)
            keep = m.copy()
            for a_, b_ in ex[s]:
                keep &= ~((self.t0 >= a_) & (self.t0 < b_))
            slow = self.ms > self.thr[s]
            over = float((w[keep] * slow[keep]).sum())
            counted = float(w[keep].sum())
            if ht:
                counted = float(self.N[s].sum() - w[m & ~keep].sum())
            out[s] = {"sli": 100 * over / counted, "over_requests": over, "counted": counted,
                      "kept": int(keep.sum()), "kept_slow": int((slow & keep).sum())}
        return out

    def interval(self, s, w, ex, sli):
        """The linearised 90 per cent interval of a ratio estimated from a stratified sample of whole traces: strata
        are the root service's hours, units the traces the store kept there (every one, touching the service or not)."""
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        R = sli / 100.0
        slow = (self.ms > self.thr[s]).astype(float)
        z = {}
        for i in np.nonzero(keep)[0]:
            z[self.tr[i]] = z.get(self.tr[i], 0.0) + (slow[i] - R)
        X = float(w[keep].sum())
        V = 0.0
        orphan = 0.0
        for e in K.EDGE:
            for h in range(H):
                k = int(self.Kroot[e][h])
                if k < 2:
                    continue
        # per stratum sums over the kept roots
        strata = {}
        for i in np.nonzero(self.root & (self.h >= 0) & (self.h < H))[0]:
            key = (self.svc[i], int(self.h[i]))
            strata.setdefault(key, []).append(z.get(self.tr[i], 0.0))
        for (e, h), zs in strata.items():
            k = len(zs)
            if k < 2:
                continue
            wh = self.N[e][h] / k
            u = wh * np.array(zs) / X
            f = min(1.0, k / max(self.N[e][h], 1))
            V += (1 - f) * k / (k - 1) * float(((u - u.mean()) ** 2).sum())
        # spans whose root is not in the export (traces begun in November): their own stratum, with-replacement
        orphans = [i for i in np.nonzero(keep)[0] if self.tr[i] not in self.root_of]
        if len(orphans) > 1:
            u = np.array([w[i] * (slow[i] - R) / X for i in orphans])
            orphan = len(u) / (len(u) - 1) * float(((u - u.mean()) ** 2).sum())
        se = 100 * np.sqrt(V + orphan)
        return sli - Z90 * se, sli + Z90 * se, se

    def interval_boot(self, s, w, ex, reps=300, seed=7):
        """The rival interval: whole traces resampled within each root service's hour, the ratio re-estimated."""
        rng = np.random.default_rng(seed)
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        slow = (self.ms > self.thr[s]).astype(float)
        yx = {}
        for i in np.nonzero(keep)[0]:
            y, x = yx.get(self.tr[i], (0.0, 0.0))
            yx[self.tr[i]] = (y + w[i] * slow[i], x + w[i])
        strata = {}
        for i in np.nonzero(self.root & (self.h >= 0) & (self.h < H))[0]:
            strata.setdefault((self.svc[i], int(self.h[i])), []).append(yx.get(self.tr[i], (0.0, 0.0)))
        orphan = [(w[i] * slow[i], w[i]) for i in np.nonzero(keep)[0] if self.tr[i] not in self.root_of]
        arrs = [np.array(v) for v in strata.values() if len(v) >= 2]
        fixed = [np.array(v) for v in strata.values() if len(v) < 2]
        base = sum(a.sum(axis=0) for a in fixed) if fixed else np.zeros(2)
        if orphan:
            base = base + np.array(orphan).sum(axis=0)
        out = []
        for _ in range(reps):
            tot = base.copy()
            for a in arrs:
                tot = tot + a[rng.integers(0, len(a), len(a))].sum(axis=0)
            out.append(100 * tot[0] / tot[1])
        return float(np.percentile(out, 5)), float(np.percentile(out, 95))

    def binomial_interval(self, s, ex, sli):
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        n = keep.sum()
        p = sli / 100.0
        se = 100 * np.sqrt(p * (1 - p) / n)
        return sli - Z90 * se, sli + Z90 * se, se

    def programme(self, S):
        over = [s for s in K.SVC if K.r1(S[s]["sli"]) > self.bud[s]]
        tot = sum(S[s]["over_requests"] for s in K.SVC)
        order = sorted(over, key=lambda s: -S[s]["over_requests"])
        share = {s: 100 * S[s]["over_requests"] / tot for s in K.SVC}
        together = 100 * sum(S[s]["over_requests"] for s in over) / tot
        beyond = sum(S[s]["over_requests"] - self.bud[s] / 100 * S[s]["counted"] for s in over)
        return {"over": over, "order": order, "share": share, "together": together, "beyond": beyond}

    # ------------------------------------------------------------------ everything
    def run(self):
        incs = self.december()
        curves = self.load_curves(incs)
        att, onset = self.attribute(incs, curves)
        w_root = self.weights("root")
        ex = self.excluded(att, incs)
        S = self.slis(w_root, ex)
        P = self.programme(S)
        ci = {s: self.interval(s, w_root, ex, S[s]["sli"]) for s in K.SVC}
        mins = self.minutes()
        # the hurried passes
        careful_att = self.window_excess(incs, curves)
        w_own = self.weights("own")
        ex_c = self.excluded(careful_att, incs)
        S_c = self.slis(w_own, ex_c)
        P_c = self.programme(S_c)
        ci_c = {s: self.binomial_interval(s, ex_c, S_c[s]["sli"]) for s in K.SVC}
        S_rc = self.slis(w_root, ex_c)
        P_rc = self.programme(S_rc)
        # the hints, each applied alone to the careful pass
        S_hi = self.slis(w_own, ex)
        P_hi = self.programme(S_hi)
        ci_hc = {s: self.interval(s, w_own, ex_c, S_c[s]["sli"]) for s in K.SVC}
        ci_boot = {s: self.interval_boot(s, w_root, ex) for s in P["over"]}
        first = {x["id"]: x["named"][0][0] for x in incs}
        ex_q = self.excluded(first, incs)
        S_q = self.slis(self.weights("unw"), ex_q)
        P_q = self.programme(S_q)
        ci_q = {s: self.binomial_interval(s, ex_q, S_q[s]["sli"]) for s in K.SVC}
        mins_q = self.minutes(backdate=True, tool_end=True)
        return {"incidents": incs, "attribution": att, "onset": onset, "S": S, "P": P, "ci": ci, "minutes": mins,
                "careful": {"attribution": careful_att, "S": S_c, "P": P_c, "ci": ci_c, "minutes": mins},
                "quick": {"attribution": first, "S": S_q, "P": P_q, "ci": ci_q, "minutes": mins_q},
                "rootcareful": {"attribution": careful_att, "S": S_rc, "P": P_rc},
                "hint_i5": {"attribution": att, "S": S_hi, "P": P_hi}, "hint_ci": ci_hc, "ci_boot": ci_boot,
                "thr": self.thr, "bud": self.bud}
