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
FILL = "bands5"                                      # the hours before the export: the threshold bucket split in five
                                                     # bands of the service's hourly load (hist_fill)
SPLIT_FAMILY = ("pooled", "bands2", "bands3", "bands4", "bands5", "bands6", "bands8", "bands10", "bands15", "bands20",
                "bands30", "logit", "hour")          # every split of the threshold bucket the held spans support
NAIVE_BRIDGES = ("linear", "loglinear", "lower", "upper")   # interpolation inside the bucket, and its two bounds


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
RISE, LEVEL, MIN_SPANS, MIN_SECONDS = 2.2, 1.9, 20, 1800


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

    # ------------------------------------------------------------------ the store's span metrics (whole December)
    def hist(self):
        """The tracing store's hourly span metrics: {(service, span name, kind): array [hour, 1 + buckets]} with the
        spans ingested and the cumulative count at each boundary, error and non-error series summed; and the
        boundaries, read from the file's own header."""
        if hasattr(self, "_HS"):
            return self._HS, self._HB
        HS, HB = {}, None
        with open(os.path.join(self.t, K.FILES["spanmetrics"])) as fh:
            rd = csv.DictReader(fh)
            HB = [int(c.rsplit("_", 1)[1]) for c in rd.fieldnames if c.startswith("latency_bucket_le_")
                  and not c.endswith("_inf")]
            for row in rd:
                t = dt.datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%SZ")
                h = int((t - DEC0).total_seconds() // 3600)
                if not 0 <= h < H:
                    continue
                key = (self.by_trace[row["service_name"]], row["span_name"], row["span_kind"].replace("SPAN_KIND_", ""))
                a = HS.get(key)
                if a is None:
                    a = HS[key] = np.zeros((H, 1 + len(HB)))
                a[h, 0] += float(row["calls_total"])
                for j, b in enumerate(HB):
                    a[h, 1 + j] += float(row["latency_bucket_le_%d" % b])
        self._HS, self._HB = HS, HB
        return HS, HB

    def hist_edge_weights(self):
        """Each edge service's hourly keep weight for every December hour: its RequestCount over the root spans the
        store ingested that hour (every server span of an edge service starts a trace)."""
        HS, _ = self.hist()
        out = {}
        for e in K.EDGE:
            k = sum(a[:, 0] for (s_, n, kd), a in HS.items() if s_ == e and kd == "SERVER")
            out[e] = np.where(k > 0, self.N[e] / np.maximum(k, 1), 0.0)
        return out

    def hist_series_weight(self, s, name, how="root"):
        """The weight of one server series of the span metrics, hour by hour: an edge service's own keep weight; an
        internal operation's callers' keep weights averaged over the client spans each caller's kept traces sent it
        that hour ("root"), or the service's RequestCount over all its ingested server spans ("own")."""
        HS, _ = self.hist()
        if how == "own" or s in K.EDGE:
            if how == "own":
                k = sum(a[:, 0] for (s_, n, kd), a in HS.items() if s_ == s and kd == "SERVER")
                return np.where(k > 0, self.N[s] / np.maximum(k, 1), 0.0)
            return self.hist_edge_weights()[s]
        We = self.hist_edge_weights()
        meth, path = name.split(" ", 1)
        tname = [c["Tracing service name"] for c in self.cat if c["Service"] == s][0]
        cname = "%s %s %s" % (meth, tname, path)
        num, den = np.zeros(H), np.zeros(H)
        for (cs, n, kd), a in HS.items():
            if kd == "CLIENT" and n == cname and cs in We:
                num += We[cs] * a[:, 0]
                den += a[:, 0]
        return np.where(den > 0, num / np.maximum(den, 1e-9), 0.0)

    def bucket_of(self, s):
        """The histogram bucket (lo, hi] that holds a service's threshold, or None when the threshold is a boundary."""
        _, HB = self.hist()
        thr = self.thr[s]
        if thr in HB:
            return None
        return max([0] + [b for b in HB if b < thr]), min(b for b in HB if b > thr)

    def split_terms(self, s, name, w, form, quiet, cut, weighted=True):
        """For one server series whose threshold sits inside a bucket: the held, incident-free spans in that bucket,
        the group each falls in under `form` and each group's share over the threshold. Returns (group of hour ->
        index, shares, span index, span group, group weights)."""
        from scipy.special import expit
        lo, hi = self.bucket_of(s)
        hrs = np.arange(H)
        x = np.log(self.N[s] + 1)
        m = self.dec & (self.svc == s) & (self.name == name) & (self.ms > lo) & (self.ms <= hi)
        m &= quiet[np.clip(self.h, 0, H - 1)]
        idx = np.nonzero(m)[0]
        y = (self.ms[idx] > self.thr[s]).astype(float)
        ww = w[idx] if weighted else np.ones(len(idx))
        if form == "logit":
            if len(idx) < 5:
                return None
            X = np.column_stack([np.ones(len(idx)), x[self.h[idx]]])
            b = self._logit_fit(X, ww * y, ww)
            return {"kind": "logit", "phi": expit(b[0] + b[1] * x), "idx": idx}
        if form == "pooled":
            grp_h = np.zeros(H, dtype=int)
            ng = 1
        elif form == "hour":
            grp_h = hrs % 24
            ng = 24
        else:
            ng = int(form[5:])
            fit = (hrs >= cut) & quiet
            edges = np.quantile(x[fit], np.linspace(0, 1, ng + 1))
            grp_h = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, ng - 1)
        g = grp_h[self.h[idx]]
        W = np.array([ww[g == k].sum() for k in range(ng)])
        Y = np.array([(ww * y)[g == k].sum() for k in range(ng)])
        pooled = Y.sum() / max(W.sum(), 1e-12)
        sh = np.where(W > 0, Y / np.maximum(W, 1e-12), np.nan)
        filled = [k for k in range(ng) if W[k] > 0]
        for k in range(ng):                                   # a group with no held span takes its nearest neighbour's
            if W[k] <= 0:
                sh[k] = sh[min(filled, key=lambda j: abs(j - k))] if filled else pooled
        return {"kind": "groups", "phi": sh[grp_h], "grp_h": grp_h, "share": sh, "W": W, "idx": idx, "g": g,
                "y": y, "ww": ww}

    def hist_fill(self, w, ex=None, form=None, incs=None, how="root", weighted=True, detail=False):
        """The hours before the export begins, measured from the span metrics: for each server series the spans the
        store ingested over the service's threshold (exact where the threshold is a bucket boundary; otherwise the
        buckets above it and the threshold's own bucket split at the share its held, incident-free spans show under
        `form`), each at its series' weight. {service: (over-threshold requests, requests)}; `form` may also be an
        interpolation inside the bucket ("linear", "loglinear") or a bound ("lower", "upper")."""
        form = form or FILL
        HS, HB = self.hist()
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        gone = np.arange(H) < cut
        out, det = {}, {}
        for s in K.SVC:
            thr, bk, tot = self.thr[s], self.bucket_of(s), 0.0
            for (ss, name, kd), a in sorted(HS.items()):
                if ss != s or kd != "SERVER":
                    continue
                wt = self.hist_series_weight(s, name, how)
                cnt = a[:, 0]
                if bk is None:
                    slow = cnt - a[:, 1 + HB.index(thr)]
                    mid, phi, terms = np.zeros(H), np.zeros(H), None
                else:
                    lo, hi = bk
                    above = cnt - a[:, 1 + HB.index(hi)]
                    mid = a[:, 1 + HB.index(hi)] - (a[:, 1 + HB.index(lo)] if lo > 0 else 0.0)
                    terms = None
                    if form == "linear":
                        phi = np.full(H, (hi - thr) / (hi - lo))
                    elif form == "loglinear":
                        phi = np.full(H, np.log(hi / thr) / np.log(hi / max(lo, 1)))
                    elif form == "lower":
                        phi = np.zeros(H)
                    elif form == "upper":
                        phi = np.ones(H)
                    else:
                        terms = self.split_terms(s, name, w, form, quiet, cut, weighted)
                        phi = terms["phi"] if terms else np.zeros(H)
                    slow = above + phi * mid
                tot += float((wt * slow)[gone].sum())
                det[(s, name)] = {"wt": wt, "cnt": cnt, "slow": slow, "mid": mid, "phi": phi, "terms": terms}
            out[s] = (tot, float(self.N[s][gone].sum()))
        return (out, det) if detail else out

    def bridge_check(self, w, ex, form, incs=None):
        """The bridge on the hours the export does hold: each service's over-threshold requests in the export's
        incident-free hours rebuilt from the span metrics under `form`, over the same requests counted span by span.
        {service: (rebuilt, counted)}."""
        HS, HB = self.hist()
        cut = self.held_from()
        quiet = self.quiet_hours(incs)
        hrs = np.arange(H)
        sel = (hrs >= cut) & quiet
        _, det = self.hist_fill(w, ex, form, incs, detail=True)
        out = {}
        for s in K.SVC:
            O, C = self.hourly(s, w, ex)
            est = sum(float((d["wt"] * d["slow"])[sel].sum()) for (ss, n), d in det.items() if ss == s)
            out[s] = (est, float(O[sel].sum()))
        return out

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
        if form.startswith("bands") and form != "bands20":
            nb = 10 if form == "bands" else int(form[5:])
            edges = np.quantile(xf, np.linspace(0, 1, nb + 1))
            band = np.clip(np.searchsorted(edges, xf, side="right") - 1, 0, nb - 1)
            share = np.array([of[band == k].sum() / max(cf[band == k].sum(), 1e-9) for k in range(nb)])
            return lambda n: share[np.clip(np.searchsorted(edges, np.log(n + 1), side="right") - 1, 0, nb - 1)]
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

    def _keep(self, s, ex):
        m = self.dec & (self.svc == s)
        keep = m.copy()
        for a_, b_ in ex[s]:
            keep &= ~((self.t0 >= a_) & (self.t0 < b_))
        return keep

    def interval(self, s, w, ex, sli, det=None, incs=None):
        """The linearised 90 per cent interval of a ratio estimated from a stratified sample of whole traces: strata
        are the root service's hours, units the traces the store kept there (every one, touching the service or not).
        With `det` (hist_fill's detail), the hours before the export are in the ratio as well: their spans are
        counted in the span metrics, a sample of the same design with no trace to group them, so each series' hour
        adds its own sampling variance, and a kept span in the threshold's bucket in a held hour also moves the share
        that bucket was split at."""
        keep = self._keep(s, ex)
        R = sli / 100.0
        slow = (self.ms > self.thr[s]).astype(float)
        cut = self.held_from()
        gone = np.arange(H) < cut
        M = float(self.N[s][gone].sum()) if det is not None else 0.0
        X = float(w[keep].sum()) + M
        extra = np.zeros(len(self.t0))
        Vu = 0.0
        if det is not None:
            for (ss, name), d in det.items():
                if ss != s:
                    continue
                wt, cnt, mid, phi = d["wt"][gone], d["cnt"][gone], d["mid"][gone], d["phi"][gone]
                above = d["slow"][gone] - phi * mid
                ok = cnt > 0
                m1 = np.where(ok, (above + phi * mid) / np.maximum(cnt, 1), 0.0)
                m2 = np.where(ok, (above + phi ** 2 * mid) / np.maximum(cnt, 1), 0.0)
                f = np.where(wt > 0, 1.0 / np.maximum(wt, 1e-9), 1.0)
                Vu += float((wt ** 2 * cnt * (m2 - m1 ** 2) * (1 - np.minimum(f, 1.0)) *
                             np.where(cnt > 1, cnt / np.maximum(cnt - 1, 1), 1.0)).sum())
                t = d["terms"]
                if t is not None and t["kind"] == "groups":
                    T = np.array([float((d["wt"] * d["mid"])[gone & (t["grp_h"] == k)].sum())
                                  for k in range(len(t["share"]))])
                    for i, g, y in zip(t["idx"], t["g"], t["y"]):
                        if t["W"][g] > 0:
                            extra[i] += T[g] * (y - t["share"][g]) / t["W"][g]
        z = {}
        for i in np.nonzero(keep | (extra != 0))[0]:
            v = ((slow[i] - R) if keep[i] else 0.0) + extra[i]
            z[self.tr[i]] = z.get(self.tr[i], 0.0) + v
        V = 0.0
        strata = {}
        for i in np.nonzero(self.root & (self.h >= 0) & (self.h < H))[0]:
            strata.setdefault((self.svc[i], int(self.h[i])), []).append(z.get(self.tr[i], 0.0))
        for (e, h), zs in strata.items():
            k = len(zs)
            if k < 2:
                continue
            wh = self.N[e][h] / k
            u = wh * np.array(zs) / X
            f = min(1.0, k / max(self.N[e][h], 1))
            V += (1 - f) * k / (k - 1) * float(((u - u.mean()) ** 2).sum())
        # spans whose root is not in the export (traces begun in the hour before it): their own stratum
        orphan = 0.0
        orphans = [i for i in np.nonzero(keep)[0] if self.tr[i] not in self.root_of]
        if len(orphans) > 1:
            u = np.array([w[i] * ((slow[i] - R) + extra[i]) / X for i in orphans])
            orphan = len(u) / (len(u) - 1) * float(((u - u.mean()) ** 2).sum())
        se = 100 * np.sqrt(V + orphan + Vu / X ** 2)
        return sli - Z90 * se, sli + Z90 * se, se

    def interval_boot(self, s, w, ex, det=None, form=None, incs=None, reps=400, seed=7):
        """The rival interval: whole traces resampled within each root service's hour and the ratio re-estimated; with
        `det`, the span metrics' counts for the hours before the export redrawn series by series and hour by hour, and
        the threshold bucket's split refitted on each resample."""
        rng = np.random.default_rng(seed)
        form = form or FILL
        keep = self._keep(s, ex)
        slow = (self.ms > self.thr[s]).astype(float)
        cut = self.held_from()
        gone = np.arange(H) < cut
        M = float(self.N[s][gone].sum()) if det is not None else 0.0
        series = [(n, d) for (ss, n), d in sorted(det.items()) if ss == s] if det is not None else []
        split = [(n, d) for n, d in series if d["terms"] is not None and d["terms"]["kind"] == "groups"]
        # one feature row per trace: weighted over-threshold and weighted spans of the service, then for every split
        # series and group the weighted bucket spans over the threshold and the weighted bucket spans
        col = {}
        ncol = 2
        for n, d in split:
            for k in range(len(d["terms"]["share"])):
                col[(n, k)] = ncol
                ncol += 2
        feat = {}
        for i in np.nonzero(keep)[0]:
            v = feat.setdefault(self.tr[i], np.zeros(ncol))
            v[0] += w[i] * slow[i]
            v[1] += w[i]
        for n, d in split:
            t = d["terms"]
            for i, g, y, ww in zip(t["idx"], t["g"], t["y"], t["ww"]):
                v = feat.setdefault(self.tr[i], np.zeros(ncol))
                c = col[(n, g)]
                v[c] += ww * y
                v[c + 1] += ww
        strata = {}
        for i in np.nonzero(self.root & (self.h >= 0) & (self.h < H))[0]:
            strata.setdefault((self.svc[i], int(self.h[i])), []).append(self.tr[i])
        in_root = set(self.root_of)
        rows, off, size, fixed = [], [], [], np.zeros(ncol)
        zero = np.zeros(ncol)
        for key in sorted(strata):
            trs = strata[key]
            if len(trs) < 2:
                for t_ in trs:
                    fixed += feat.get(t_, zero)
                continue
            o = len(rows)
            for t_ in trs:
                rows.append(feat.get(t_, zero))
                off.append(o)
                size.append(len(trs))
        for t_, v in feat.items():
            if t_ not in in_root:
                fixed += v
        rows = np.array(rows) if rows else np.zeros((0, ncol))
        off, size = np.array(off), np.array(size)
        out = []
        for _ in range(reps):
            tot = fixed.copy()
            if len(rows):
                tot += rows[off + np.floor(rng.random(len(off)) * size).astype(int)].sum(axis=0)
            over, counted = tot[0], tot[1] + M
            for n, d in series:
                wt, cnt, mid = d["wt"][gone], d["cnt"][gone].astype(int), d["mid"][gone]
                phi0 = d["phi"][gone]
                above = np.clip(np.rint(d["slow"][gone] - phi0 * mid), 0, None).astype(int)
                midc = np.clip(np.rint(mid), 0, None).astype(int)
                pa = np.where(cnt > 0, above / np.maximum(cnt, 1), 0.0)
                a_star = rng.binomial(cnt, np.clip(pa, 0, 1))
                rest = cnt - a_star
                pm = np.where(cnt - above > 0, midc / np.maximum(cnt - above, 1), 0.0)
                m_star = rng.binomial(rest, np.clip(pm, 0, 1))
                t = d["terms"]
                if t is not None and t["kind"] == "groups":
                    sh = np.array([tot[col[(n, k)]] / tot[col[(n, k)] + 1] if tot[col[(n, k)] + 1] > 0
                                   else t["share"][k] for k in range(len(t["share"]))])
                    phi = sh[t["grp_h"]][gone]
                else:
                    phi = phi0
                over += float((wt * (a_star + phi * m_star)).sum())
            out.append(100 * over / counted)
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
    def load_fill(self, w, ex, method, incs=None):
        """A fill that reads no span metrics: the hours before the export counted at a share modelled from the held
        hours, by a load form of load_model or a match of share_by. The rivals the span metrics rule out."""
        cut, quiet, hrs = self.held_from(), self.quiet_hours(incs), np.arange(H)
        out = {}
        for s in K.SVC:
            O, C = self.hourly(s, w, ex)
            fit = (hrs >= cut) & quiet & (C > 0)
            p_ = self.share_by(method, s, O, C, fit)
            n = self.N[s][hrs < cut]
            out[s] = (float((n * p_[hrs < cut]).sum()), float(n.sum()))
        return out

    def route(self, lost=(), incs=None, curves=None, form=None, cache=None):
        """Every SLI and the programme with the judgments in `lost` made the hurried way and the rest as the golden
        makes them: "S1" each service's own hourly count for the trace roots' keep shares, "S2" each December incident
        on the service furthest over its load curve across the whole incident, "S3" December read from the hours the
        export holds."""
        cache = cache if cache is not None else {}
        incs = incs or self.december()
        curves = curves or self.load_curves(incs)
        how = "own" if "S1" in lost else "root"
        if how not in cache:
            cache[how] = self.weights(how)
        w = cache[how]
        akey = "win" if "S2" in lost else "att"
        if akey not in cache:
            cache[akey] = self.window_excess(incs, curves) if akey == "win" else self.attribute(incs, curves)[0]
        att = cache[akey]
        ex = self.excluded(att, incs)
        F = None if "S3" in lost else self.hist_fill(w, ex, form, incs, how=how)
        S = self.slis(w, ex, fill=F)
        return {"attribution": att, "S": S, "P": self.programme(S), "w": w, "ex": ex, "fill": F}

    def run(self):
        incs = self.december()
        curves = self.load_curves(incs)
        att, onset = self.attribute(incs, curves)
        w_root, w_unw = self.weights("root"), self.weights("unw")
        ex = self.excluded(att, incs)
        F, det = self.hist_fill(w_root, ex, FILL, incs, detail=True)
        S = self.slis(w_root, ex, fill=F)
        P = self.programme(S)
        ci = {s: self.interval(s, w_root, ex, S[s]["sli"], det=det, incs=incs) for s in K.SVC}
        ci_boot = {s: self.interval_boot(s, w_root, ex, det=det, incs=incs) for s in P["over"]}
        mins = self.minutes()
        # the lattice: every combination of the three judgments made the hurried way
        cache = {"root": w_root, "att": att}
        lattice = {}
        for key in ("S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"):
            r_ = self.route(tuple(key.split("+")), incs, curves, cache=cache)
            r_["ci"] = {s: self.binomial_interval(s, r_["ex"], r_["S"][s]["sli"]) for s in K.SVC}
            lattice[key] = r_
        win = cache["win"]
        # the quick pass: the kept spans unweighted, the first-named service at fault, the export's hours
        first = {x["id"]: x["named"][0][0] for x in incs}
        ex_q = self.excluded(first, incs)
        S_q = self.slis(w_unw, ex_q)
        quick = {"attribution": first, "S": S_q, "P": self.programme(S_q),
                 "ci": {s: self.binomial_interval(s, ex_q, S_q[s]["sli"]) for s in K.SVC},
                 "minutes": self.minutes(backdate=True, tool_end=True)}
        # the golden family: every split of the threshold bucket the held spans support, weighted and not
        family = {}
        for f in SPLIT_FAMILY:
            for wtd in (True, False):
                Ff = self.hist_fill(w_root, ex, f, incs, weighted=wtd)
                family["%s%s" % (f, "" if wtd else " unweighted")] = self.slis(w_root, ex, fill=Ff)
        # the bridges a tool would apply without the held spans, and the bucket's two bounds
        naive = {f: self.slis(w_root, ex, fill=self.hist_fill(w_root, ex, f, incs)) for f in NAIVE_BRIDGES}
        # fills that read no span metrics (the hours before the export modelled from the held hours)
        loadfill = {}
        for m_ in ["bands%d" % k for k in (2, 3, 4, 5, 6, 8, 10, 15, 20, 30)] + \
                ["isotonic", "logit2", "weekday-hour", "hour", "daytype-hour", "flat"]:
            loadfill[m_] = self.slis(w_root, ex, fill=self.load_fill(w_root, ex, m_, incs))
        checks_ = {f: self.bridge_check(w_root, ex, f, incs) for f in (FILL, "pooled", "linear", "loglinear")}
        return {"incidents": incs, "attribution": att, "onset": onset, "S": S, "P": P, "ci": ci, "ci_boot": ci_boot,
                "minutes": mins, "fill": F, "held_from": self.held_from(), "lattice": lattice, "quick": quick,
                "window": win, "family": family, "naive": naive, "loadfill": loadfill, "bridge_check": checks_,
                "bucket": {s: self.bucket_of(s) for s in K.SVC}, "thr": self.thr, "bud": self.bud}
