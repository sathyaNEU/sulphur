"""task6's independent verifier: reads only the bundle (target/), the goldens and figures.json, on its own code path
(no generator module is imported), recomputes the call and every graded figure (the SLIs, the start order, the five's
shares and the share they served together, the requests beyond their budgets, the incident minutes in which an incident
named one of them), reads back every format the pack ships, and reports each disagreement.

    python3 verify.py [task_dir]"""
import csv
import datetime as dt
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

import pyarrow.parquet as pq
from docx import Document
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))


def half_up(x, q):
    return float(Decimal(repr(float(x))).quantize(Decimal(q), rounding=ROUND_HALF_UP))


def lisbon_utc(local):
    """A Lisbon wall-clock minute to UTC (summer time from 29 March 01:00 UTC to 25 October 01:00 UTC in 2026)."""
    t = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
    on, off = dt.datetime(2026, 3, 29, 1), dt.datetime(2026, 10, 25, 1)
    u = t - dt.timedelta(hours=1)
    return u if on <= u < off else t


def run(task_dir):
    tgt = os.path.join(task_dir, "target")
    files = sorted(os.listdir(tgt))
    bad = []
    pick = lambda pre: os.path.join(tgt, [f for f in files if f.startswith(pre)][0])

    # ---- the standard and the catalogue
    slo = Document(pick("PR-SLO-3"))
    slo_text = "\n".join(p.text for p in slo.paragraphs)
    if "whether or not the tracing store kept a span for it" not in slo_text:
        bad.append("PR-SLO-3 read-back: section 2.2 not found")
    thr, bud = {}, {}
    for row in slo.tables[0].rows[1:]:
        c = [x.text for x in row.cells]
        thr[c[0]] = float(c[2].replace(",", ""))
        bud[c[0]] = float(c[3].rstrip("%"))
    ws = load_workbook(pick("service_catalogue"), read_only=True)["Services"]
    rows = list(ws.iter_rows(values_only=True))
    cat = [dict(zip(rows[0], r)) for r in rows[1:] if r[0]]
    svc_of = {c["Tracing service name"]: c["Service"] for c in cat}
    tg = {c["Load balancer target group (from 1 Jul 2026)"]: c["Service"] for c in cat}
    services = [c["Service"] for c in cat]

    # ---- the balancer's December counts
    n = {s: {} for s in services}
    for r in csv.DictReader(open(pick("lb_target_group_requests_2026-H2"))):
        t = dt.datetime.strptime(r["TimePeriodStart"], "%Y-%m-%dT%H:%M:%SZ")
        if t.month == 12:
            n[tg[r["TargetGroupName"]]][(t.day - 1) * 24 + t.hour] = int(r["RequestCount"])

    # ---- the spans: dedupe, drop probes, find each trace's root, weight by the root's hourly keep share
    tb = pq.read_table(pick("trace_spans")).to_pydict()
    dec0 = int(dt.datetime(2026, 12, 1, tzinfo=dt.timezone.utc).timestamp()) * 10 ** 9
    seen, spans = set(), []
    for i in range(len(tb["span_id"])):
        sid = tb["span_id"][i]
        if sid in seen or tb["span_name"][i] == "GET /healthz":
            continue
        seen.add(sid)
        spans.append((tb["trace_id"][i], tb["parent_span_id"][i], svc_of[tb["service_name"][i]], tb["span_kind"][i],
                      (tb["start_time_unix_nano"][i] - dec0) // 3600000000000,
                      (tb["end_time_unix_nano"][i] - tb["start_time_unix_nano"][i]) / 1e6))
    root, kept_root = {}, {}
    for tid, pid, s, kind, h, ms in spans:
        if kind == "SPAN_KIND_SERVER" and pid == "":
            root[tid] = (s, h)
            kept_root[(s, h)] = kept_root.get((s, h), 0) + 1
    num = {s: 0.0 for s in services}
    for tid, pid, s, kind, h, ms in spans:
        if kind != "SPAN_KIND_SERVER" or not 0 <= h < 744 or tid not in root:
            continue
        e, he = root[tid]
        if ms > thr[s]:
            num[s] += n[e][he] / kept_root[(e, he)]
    sli = {s: 100 * num[s] / sum(n[s].values()) for s in services}
    over = [s for s in services if half_up(sli[s], "0.1") > bud[s]]

    figs = json.load(open(os.path.join(HERE, "figures.json")))
    if over != figs["over"]:
        bad.append("the call: %s against figures.json %s" % (over, figs["over"]))
    for s in services:
        if "%.1f" % half_up(sli[s], "0.1") != figs["sli"][s]:
            bad.append("%s SLI %.4f against %s" % (s, sli[s], figs["sli"][s]))

    # ---- the asks on the SLI's numerator: each service's over-threshold December requests
    slow = {s: num[s] for s in services}
    total = sum(slow.values())
    order = sorted(over, key=lambda s: -slow[s])
    if order != figs["start_order"]:
        bad.append("start order %s against %s" % (order, figs["start_order"]))
    for s in services:
        if str(int(half_up(100 * slow[s] / total, "1"))) != figs["share_pct"][s]:
            bad.append("%s share %.3f against %s" % (s, 100 * slow[s] / total, figs["share_pct"][s]))
    together = 100 * sum(slow[s] for s in over) / total
    if str(int(half_up(together, "1"))) != figs["over_share_pct"]:
        bad.append("share served together %.3f against %s" % (together, figs["over_share_pct"]))
    beyond = sum(slow[s] - bud[s] / 100 * sum(n[s].values()) for s in over)
    if "{:,}".format(int(half_up(beyond / 10000, "1")) * 10000) != figs["beyond_budget"]:
        bad.append("requests beyond budget %.0f against %s" % (beyond, figs["beyond_budget"]))

    # ---- the incident ask: minutes in which an incident named one of the services that ran over, by half
    st = json.load(open(pick("status_page_history")))
    posts = [(set(p["components"]), lisbon_utc(p["created_at"])) for p in st["incidents"]]
    ops = {}
    for c in st["component_status_changes"]:
        if c["status"] == "operational":
            ops.setdefault(c["component"], []).append(lisbon_utc(c["at"]))
    named = {(r["incident_id"], r["detail"]): dt.datetime.strptime(r["at_utc"], "%Y-%m-%d %H:%M:%S")
             for r in csv.DictReader(open(pick("incident_timeline"))) if r["event"] == "service added"}
    comp = {c["Service"]: c["Status page component"] for c in cat}
    spans_by = {s: [] for s in services}
    for r in csv.DictReader(open(pick("incidents_2026"))):
        d0 = dt.datetime.strptime(r["declared_at_utc"], "%Y-%m-%d %H:%M:%S")
        ss = r["services"].split(";")
        mine = {comp[svc_of[x]] for x in ss}
        m = [p for p in posts if p[0] & mine and dt.timedelta(0) <= p[1] - d0.replace(second=0) <= dt.timedelta(minutes=15)]
        if not m:
            continue
        end = max(min(t for t in sorted(ops[c]) if t > m[0][1]) for c in m[0][0])
        for x in ss:
            a = max(d0, named[(r["incident_id"], x)])
            if a < end:
                spans_by[svc_of[x]].append((a, end))
    cut = dt.datetime(2026, 6, 30, 23)
    tot, last = [0.0, 0.0], None
    for a, b in sorted(x for s in over for x in spans_by[s]):
        if last and a < last:
            a = last
        if b <= a:
            continue
        for i, (lo, hi) in enumerate(((dt.datetime(2026, 1, 1), cut), (cut, dt.datetime(2027, 1, 1)))):
            lo_, hi_ = max(a, lo), min(b, hi)
            if hi_ > lo_:
                tot[i] += (hi_ - lo_).total_seconds() / 60
        last = b if last is None else max(last, b)
    got = [int(half_up(v, "1")) for v in tot]
    if got != figs["incident_minutes"]:
        bad.append("incident minutes %s against %s" % (got, figs["incident_minutes"]))

    # ---- every shipped format reads back, and the goldens carry figures.json's figures
    for f in files:
        p = os.path.join(tgt, f)
        if f.endswith(".md") and not open(p).read().strip():
            bad.append("%s reads back empty" % f)
        if f.endswith(".xlsx") and not any(load_workbook(p, read_only=True).worksheets[0].iter_rows(max_row=2)):
            bad.append("%s reads back empty" % f)
        if f.endswith(".json"):
            json.load(open(p))
    gold = os.path.join(task_dir, "golden")
    rows_csv = list(csv.DictReader(open(os.path.join(gold, "service_sli_2026.csv"))))
    if [r["service"] for r in rows_csv] != services:
        bad.append("golden csv rows %s" % [r["service"] for r in rows_csv])
    for r in rows_csv:
        s = r["service"]
        want = [figs["sli"][s], figs["budget"][s], figs["ran_over"][s]]
        got = [r["latency_sli_pct"], r["error_budget_pct"], r["ran_over"]]
        if want != got:
            bad.append("golden csv row %s: %s against %s" % (s, got, want))
    memo = Document(os.path.join(gold, "reliability_review_2026.docx"))
    memo_text = "\n".join(p.text for p in memo.paragraphs)
    if ", ".join(figs["start_order"][:-1]) not in memo_text:
        bad.append("golden memo does not name the services that breached in their start order")
    for row in memo.tables[0].rows[1:]:
        c = [x.text for x in row.cells]
        if c[2] != figs["sli"][c[0]] or c[3] != figs["budget"][c[0]]:
            bad.append("golden memo row %s: %s" % (c[0], c))
    start = [[x.text for x in row.cells] for row in memo.tables[1].rows[1:]]
    if [c[1] for c in start] != figs["start_order"] or any(c[2] != figs["share_pct"][c[1]] for c in start):
        bad.append("golden memo start table %s" % start)
    for want in (figs["over_share_pct"] + "%", figs["beyond_budget"]) + tuple(figs["incident_minutes_text"]):
        if want not in memo_text:
            bad.append("golden memo does not carry %s" % want)
    if not memo.inline_shapes:
        bad.append("golden memo carries no chart")
    return bad


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    b = run(task)
    print("verify: %s" % ("PASS" if not b else "FAIL\n  " + "\n  ".join(b)))
    sys.exit(1 if b else 0)
