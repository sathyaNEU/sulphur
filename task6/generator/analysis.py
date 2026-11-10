"""task6's golden, computed from the shipped pack alone (architecture 7), with the hurried passes beside it.

The results, in the order the review needs them:
  R1  each service's customer-facing incident minutes in each half of 2026 (the incident tool, its timeline and the
      status page reconciled; a service counts from when the tool added it, PR-SLO-3 5.2 and 5.4);
  R2  the service that owned the root cause of each December customer-facing incident: per span name, each named
      service's own handling time (its span less the union of the calls it was waiting on) against a load curve fitted
      on December's incident-free hours, the onset of each sustained rise dated by a changepoint, the earliest rise
      owning the cause (PR-SLO-3 3.3);
  R3  every service's December latency SLI: each kept server span counted at its trace root's hourly keep share (the
      balancer's request count over the roots the store kept), the requests left out by PR-SLO-3 3.2 removed, and the
      December hours the store had dropped before the export (it begins at 12 December 10:00) counted from the
      balancer's requests at the share over threshold each service's held, incident-free hours show in the same tenth
      of hourly load;
  R4  a 90 per cent interval on each over-budget service's SLI for the trace store's sample: strata are the root
      service's hours, the units are whole traces, each also moving the load-band shares the dropped hours carry;
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
FILL = "bands"                                       # the expired hours: ten bands of each service's hourly load


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


# a rise is sustained when the later stretch runs half an hour and twenty spans or more, the earlier twenty spans or
# more; RISE and LEVEL are set on the quiet days (checks R7: at most one placebo window in fourteen fires)
RISE, LEVEL, MIN_SPANS, MIN_SECONDS = 2.0, 1.75, 20, 1800


def sustained_split(t, r, min_n=MIN_SPANS, min_s=MIN_SECONDS):
    """The split of a time-ordered residual series that best separates two means, among splits leaving both stretches
    sustained: (index, earlier mean, later mean), or None."""
    n = len(r)
    if n < 2 * min_n:
        return None
    c = np.concatenate([[0.0], np.cumsum(r)])
    ks = np.arange(min_n, n - min_n + 1)
    ks = ks[(t[-1] - t[np.minimum(ks, n - 1)]) >= min_s]
    if not len(ks):
        return None
    m1 = c[ks] / ks
    m2 = (c[-1] - c[ks]) / (n - ks)
    j = int(np.argmax(ks * (n - ks) / n * (m2 - m1) ** 2))
    return int(ks[j]), float(m1[j]), float(m2[j])


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
                k_ = sustained_split(t, r)
                if k_ is None:
                    continue
                bestk, m1, m2 = k_
                if m2 - m1 >= np.log(RISE) and m2 >= np.log(LEVEL):
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

    # ------------------------------------------------------------------ the hours the store no longer held
    def held_from(self):
        """The first December hour the export holds: the store deletes whole hours, so it is the hour of the earliest
        December server span."""
        return int(np.floor(self.t0[self.dec].min() / 3600))

    def quiet_hours(self, incs=None):
        """December's hours clear of every customer-facing incident (three hours before the declaration to an hour
        after the end), the hours a load model is fitted on."""
        incs = incs or self.december()
        quiet = np.ones(H, dtype=bool)
        for x in incs:
            a_ = int(sec_of(x["declared"]) // 3600) - 3
            b_ = int(sec_of(x["end"]) // 3600) + 1
            quiet[max(0, a_):min(H, b_ + 1)] = False
        return quiet

    def hourly(self, s, w, ex):
        """A service's weighted over-threshold and weighted requests in each December hour, its excluded stretches
        left out."""
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        slow = self.ms > self.thr[s]
        O = np.bincount(self.h[keep], weights=w[keep] * slow[keep], minlength=H)[:H]
        C = np.bincount(self.h[keep], weights=w[keep], minlength=H)[:H]
        return O, C

    @staticmethod
    def _logit_fit(X, o, c, iters=80):
        """A binomial model with fractional counts (o of c over the threshold), fitted by iterated weighted least
        squares."""
        from scipy.special import expit
        b = np.zeros(X.shape[1])
        b[0] = np.log(max(o.sum(), 1e-9) / max(c.sum() - o.sum(), 1e-9))
        for _ in range(iters):
            p = expit(X @ b)
            W = c * p * (1 - p) + 1e-12
            z = X @ b + (o - c * p) / W
            b = np.linalg.solve(X.T @ (W[:, None] * X) + 1e-9 * np.eye(X.shape[1]), X.T @ (W * z))
        return b

    def load_model(self, s, O, C, fit, form="bands"):
        """The share of a service's requests over its threshold as a function of its hourly requests, from the hours in
        `fit`: "bands" (the hours in ten bands of load, each band's pooled share), "isotonic" (a share that never
        falls as load rises), "logit" (linear in log load) or "logit2" (quadratic). Returns share(N)."""
        from scipy.special import expit
        x = np.log(self.N[s] + 1)
        xf, of, cf = x[fit], O[fit], C[fit]
        if form == "bands":
            edges = np.quantile(xf, np.linspace(0, 1, 11))
            band = np.clip(np.searchsorted(edges, xf, side="right") - 1, 0, 9)
            share = np.array([of[band == k].sum() / max(cf[band == k].sum(), 1e-9) for k in range(10)])
            return lambda n: share[np.clip(np.searchsorted(edges, np.log(n + 1), side="right") - 1, 0, 9)]
        if form == "isotonic":
            o_ = np.argsort(xf)
            xs, y, wt = xf[o_], (of / np.maximum(cf, 1e-9))[o_], cf[o_]
            blocks = []                                     # pool adjacent violators
            for xi, yi, wi in zip(xs, y, wt):
                blocks.append([yi * wi, wi, xi, xi])
                while len(blocks) > 1 and blocks[-2][0] / max(blocks[-2][1], 1e-12) > blocks[-1][0] / max(blocks[-1][1], 1e-12):
                    b2 = blocks.pop()
                    blocks[-1][0] += b2[0]; blocks[-1][1] += b2[1]; blocks[-1][3] = b2[3]
            mids = np.array([(b_[2] + b_[3]) / 2 for b_ in blocks])
            vals = np.array([b_[0] / max(b_[1], 1e-12) for b_ in blocks])
            return lambda n: np.interp(np.log(n + 1), mids, vals)
        if form == "bands20":
            edges = np.quantile(xf, np.linspace(0, 1, 21))
            band = np.clip(np.searchsorted(edges, xf, side="right") - 1, 0, 19)
            share = np.array([of[band == k].sum() / max(cf[band == k].sum(), 1e-9) for k in range(20)])
            return lambda n: share[np.clip(np.searchsorted(edges, np.log(n + 1), side="right") - 1, 0, 19)]
        if form == "called":                          # own load and the loads of the services it calls
            called = [c for c, op, p in K.GRAPH.get(s, (None, []))[1]]
            Z = np.column_stack([np.ones(H), x, x ** 2] + [np.log(self.N[c] + 1) for c in called])
            b = self._logit_fit(Z[fit], of, cf)
            pz = expit(Z @ b)
            return lambda n, _p=pz: _p[:len(n)] if False else _p[self._gone_idx]
        X = np.column_stack([np.ones(len(xf)), xf] + ([xf ** 2] if form == "logit2" else []))
        b = self._logit_fit(X, of, cf)
        return lambda n: expit(np.column_stack([np.ones(len(np.atleast_1d(n))), np.log(np.atleast_1d(n) + 1)] +
                                               ([np.log(np.atleast_1d(n) + 1) ** 2] if form == "logit2" else [])) @ b)

    def band_terms(self, s, w, ex, incs=None):
        """For the ten-band fill: each December hour's band share p and its weight A (the expired requests in its band
        over the band's weighted requests in the fitted hours), and the mask of fitted hours."""
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        hrs = np.arange(H)
        O, C = self.hourly(s, w, ex)
        fit = (hrs >= cut) & quiet & (C > 0)
        x = np.log(self.N[s] + 1)
        edges = np.quantile(x[fit], np.linspace(0, 1, 11))
        band = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, 9)
        gone = hrs < cut
        Cb = np.array([C[fit & (band == k)].sum() for k in range(10)])
        Ob = np.array([O[fit & (band == k)].sum() for k in range(10)])
        Mb = np.array([self.N[s][gone & (band == k)].sum() for k in range(10)])
        pb = Ob / np.maximum(Cb, 1e-9)
        Ab = Mb / np.maximum(Cb, 1e-9)
        return pb[band], Ab[band], fit, float(self.N[s][gone].sum())

    def fill(self, w, ex, form="bands", incs=None):
        """The expired hours, each service's requests there counted at the share its load model gives: {service:
        (over-threshold requests, requests)} for December's hours before the export begins."""
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        hrs = np.arange(H)
        out = {}
        for s in K.SVC:
            O, C = self.hourly(s, w, ex)
            fit = (hrs >= cut) & quiet & (C > 0)
            f = self.load_model(s, O, C, fit, form)
            gone = hrs < cut
            self._gone_idx = np.nonzero(gone)[0]
            n = self.N[s][gone]
            out[s] = (float((n * f(n)).sum()), float(n.sum()))
        return out

    def share_by(self, method, s, O, C, fit):
        """The over-threshold share every December hour gets under a fill method fitted on the hours in `fit`: the load
        forms of load_model, or a match that ignores load ("weekday-hour", "hour", "daytype-hour", "flat") or adds the
        hour of day to load ("load+hour")."""
        from scipy.special import expit
        hrs = np.arange(H)
        if method in ("weekday-hour", "hour", "daytype-hour", "flat"):
            hod = hrs % 24
            dow = (hrs // 24 + DEC0.weekday()) % 7
            key = {"weekday-hour": dow * 24 + hod, "hour": hod, "daytype-hour": (dow >= 5) * 24 + hod,
                   "flat": np.zeros(H, dtype=int)}[method]
            pooled = O[fit].sum() / max(C[fit].sum(), 1e-9)
            out = np.full(H, pooled)
            for k in np.unique(key):
                m = fit & (key == k)
                if C[m].sum() > 0:
                    out[key == k] = O[m].sum() / C[m].sum()
            return out
        x = np.log(self.N[s] + 1)
        if method == "load+hour":
            hod = hrs % 24
            Z = np.column_stack([np.ones(H), x, x ** 2] + [f(2 * np.pi * k * hod / 24) for k in (1, 2)
                                                            for f in (np.sin, np.cos)])
            return expit(Z @ self._logit_fit(Z[fit], O[fit], C[fit]))
        self._gone_idx = hrs
        return self.load_model(s, O, C, fit, method)(self.N[s])

    def backtest(self, method, w, ex, incs=None, split_day=17):
        """The fill earning its place out of sample: fitted on the export's incident-free hours from 18 December, each
        service's over-threshold requests predicted for its incident-free hours from the export's start to 17 December
        (held, so observed): {service: (predicted, observed)}."""
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        hrs = np.arange(H)
        out = {}
        for s in K.SVC:
            O, C = self.hourly(s, w, ex)
            fit = (hrs >= split_day * 24) & quiet & (C > 0)
            test = (hrs >= cut) & (hrs < split_day * 24) & quiet & (C > 0)
            p = self.share_by(method, s, O, C, fit)
            out[s] = (float((C[test] * p[test]).sum()), float(O[test].sum()))
        return out

    def slis(self, w, ex, ht=False, fill=None):
        """Every service's December SLI from the kept spans; with `fill`, the expired hours' requests counted at their
        load model's share as well (otherwise the SLI covers only the hours the export holds)."""
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
                counted = float(self.N[s][self.held_from():].sum() - w[m & ~keep].sum())
            if fill is not None:
                over += fill[s][0]
                counted += fill[s][1]
            out[s] = {"sli": 100 * over / counted, "over_requests": over, "counted": counted,
                      "kept": int(keep.sum()), "kept_slow": int((slow & keep).sum())}
        return out

    def interval(self, s, w, ex, sli, fill=False, incs=None):
        """The linearised 90 per cent interval of a ratio estimated from a stratified sample of whole traces: strata
        are the root service's hours, units the traces the store kept there (every one, touching the service or not).
        With `fill`, the expired hours counted at their load band's share: a kept span in a fitted hour also moves
        that band's share, and so the expired requests counted at it."""
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        R = sli / 100.0
        slow = (self.ms > self.thr[s]).astype(float)
        if fill:
            ph, Ah, fit, M = self.band_terms(s, w, ex, incs)
        else:
            ph, Ah, fit, M = np.zeros(H), np.zeros(H), np.zeros(H, dtype=bool), 0.0
        z = {}
        for i in np.nonzero(keep)[0]:
            h = self.h[i]
            extra = Ah[h] * (slow[i] - ph[h]) if fit[h] else 0.0
            z[self.tr[i]] = z.get(self.tr[i], 0.0) + (slow[i] - R) + extra
        X = float(w[keep].sum()) + M
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
            u = np.array([w[i] * ((slow[i] - R) + (Ah[self.h[i]] * (slow[i] - ph[self.h[i]]) if fit[self.h[i]] else 0.0))
                          / X for i in orphans])
            orphan = len(u) / (len(u) - 1) * float(((u - u.mean()) ** 2).sum())
        se = 100 * np.sqrt(V + orphan)
        return sli - Z90 * se, sli + Z90 * se, se

    def interval_boot_fill(self, s, w, ex, reps=300, seed=7, incs=None):
        """The rival interval with the fill: whole traces resampled within each root service's hour, each one's spans
        of the service summed into their hours, the ten-band fill refitted and the SLI re-estimated."""
        rng = np.random.default_rng(seed)
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        hrs = np.arange(H)
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        slow = (self.ms > self.thr[s]).astype(float)
        idx = np.nonzero(keep)[0]
        unit = {}                                          # (trace) -> list of span indices
        for i in idx:
            unit.setdefault(self.tr[i], []).append(i)
        groups = {}
        for t, lst in unit.items():
            key = self.root_of.get(t, ("__orphan__", int(self.h[lst[0]])))
            groups.setdefault(key, []).append(lst)
        x = np.log(self.N[s] + 1)
        O0, C0 = self.hourly(s, w, ex)
        fit0 = (hrs >= cut) & quiet & (C0 > 0)
        edges = np.quantile(x[fit0], np.linspace(0, 1, 11))
        band = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, 9)
        gone = hrs < cut
        Mb = np.array([self.N[s][gone & (band == k)].sum() for k in range(10)])
        out = []
        for _ in range(reps):
            O = np.zeros(H); C = np.zeros(H)
            for key, lsts in groups.items():
                k = len(lsts)
                pick = rng.integers(0, k, k) if (k >= 2 and key[0] != "__orphan__") else np.arange(k)
                for j in pick:
                    for i in lsts[j]:
                        O[self.h[i]] += w[i] * slow[i]; C[self.h[i]] += w[i]
            fit = fit0 & (C > 0)
            pb = np.array([O[fit & (band == kk)].sum() / max(C[fit & (band == kk)].sum(), 1e-9) for kk in range(10)])
            out.append(100 * (O[~gone].sum() + (Mb * pb).sum()) / (C[~gone].sum() + Mb.sum()))
        return float(np.percentile(out, 5)), float(np.percentile(out, 95))

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
        w_root, w_own, w_unw = self.weights("root"), self.weights("own"), self.weights("unw")
        ex = self.excluded(att, incs)
        F = self.fill(w_root, ex, FILL, incs)
        S = self.slis(w_root, ex, fill=F)
        P = self.programme(S)
        ci = {s: self.interval(s, w_root, ex, S[s]["sli"], fill=True, incs=incs) for s in K.SVC}
        mins = self.minutes()
        # the careful but hurried pass, calibrated to the run record: each service's own spans on its own hourly count,
        # every December cause dated right, December read from the hours the export holds
        S_c = self.slis(w_own, ex)
        P_c = self.programme(S_c)
        ci_c = {s: self.binomial_interval(s, ex, S_c[s]["sli"]) for s in K.SVC}
        # the quick pass: the kept spans unweighted, the first-named service at fault, the held hours
        first = {x["id"]: x["named"][0][0] for x in incs}
        ex_q = self.excluded(first, incs)
        S_q = self.slis(w_unw, ex_q)
        P_q = self.programme(S_q)
        ci_q = {s: self.binomial_interval(s, ex_q, S_q[s]["sli"]) for s in K.SVC}
        mins_q = self.minutes(backdate=True, tool_end=True)
        # the routes a hint opens from the careful pass, and the whole-window reading of the causes
        S_w = self.slis(w_root, ex)                                            # the trace roots' weights, held hours
        F_p = self.fill(w_own, ex, FILL, incs)
        S_p = self.slis(w_own, ex, fill=F_p)                                   # the expired hours filled, own counts
        win = self.window_excess(incs, curves)
        ex_w = self.excluded(win, incs)
        S_x = self.slis(w_root, ex_w, fill=self.fill(w_root, ex_w, FILL, incs))  # root weights, whole-window causes
        ci_hc = {s: self.interval(s, w_own, ex, S_c[s]["sli"]) for s in K.SVC}
        ci_boot = {s: self.interval_boot_fill(s, w_root, ex, incs=incs) for s in P["over"]}
        bt = {m: self.backtest(m, w_root, ex, incs) for m in (FILL, "weekday-hour")}
        F_wh = {}
        cut, quiet, hrs = self.held_from(), self.quiet_hours(incs), np.arange(H)
        for s in K.SVC:
            O, C = self.hourly(s, w_root, ex)
            fit = (hrs >= cut) & quiet & (C > 0)
            p = self.share_by("weekday-hour", s, O, C, fit)
            n = self.N[s][hrs < cut]
            F_wh[s] = (float((n * p[hrs < cut]).sum()), float(n.sum()))
        S_wh = self.slis(w_root, ex, fill=F_wh)
        return {"incidents": incs, "attribution": att, "onset": onset, "S": S, "P": P, "ci": ci, "minutes": mins,
                "fill": F, "held_from": self.held_from(),
                "careful": {"attribution": att, "S": S_c, "P": P_c, "ci": ci_c, "minutes": mins},
                "quick": {"attribution": first, "S": S_q, "P": P_q, "ci": ci_q, "minutes": mins_q},
                "weights_only": {"attribution": att, "S": S_w, "P": self.programme(S_w)},
                "periods_only": {"attribution": att, "S": S_p, "P": self.programme(S_p)},
                "window": {"attribution": win, "S": S_x, "P": self.programme(S_x)},
                "weekday_hour": {"attribution": att, "S": S_wh, "P": self.programme(S_wh)}, "backtest": bt,
                "hint_ci": ci_hc, "ci_boot": ci_boot, "thr": self.thr, "bud": self.bud}
