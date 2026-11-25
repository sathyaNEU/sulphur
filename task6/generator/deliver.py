"""task6's golden deliverables, drawn from one figure set: reliability_review_2026.docx, the annual reliability
review's latency note (the services that breached, in the order their engineers start, with each one's share of the
over-threshold requests the SLIs count and a 90 per cent interval on its SLI; every service's December SLI beside its
budget and the chart; the service that owned the root cause of each December customer-facing incident; the requests
beyond budget; how the SLI was read), and service_sli_2026.csv, a row per service with its SLI, budget, verdict and
customer-facing incident minutes by half."""
import csv
import io
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from docx import Document               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH   # noqa: E402
from docx.shared import Cm, Pt, RGBColor        # noqa: E402

import common as K   # noqa: E402

matplotlib.rcParams["svg.hashsalt"] = "task6"
matplotlib.rcParams["font.family"] = "DejaVu Sans"


def whole(x):
    return int(Decimal(repr(float(x))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def names(lst):
    return ", ".join(lst[:-1]) + " and " + lst[-1] if len(lst) > 1 else lst[0]


def nearest(x, step):
    return int(Decimal(repr(float(x) / step)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * step


def two(x):
    return "%.2f" % float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def lisbon(t):
    return t.strftime("%-d December %H:%M")


def about(hhmm):
    """A changepoint's time as a reviewer states it: to the nearest five minutes."""
    h, m = map(int, hhmm.split(":"))
    t = nearest(h * 60 + m, 5)
    return "%02d:%02d" % divmod(t % 1440, 60)


# how the write-up names each service's slowed handling
HANDLING = {"notifications": "notifications' SMS verification", "accounts": "accounts' sign-in handling"}


def handling(s):
    return HANDLING.get(s, "%s own handling" % (s + "'" if s.endswith("s") else s + "'s"))


BRIDGE_ROOM = 0.01          # an accepted range is the split family's own range and a hundredth each side


def band_of(vals):
    """The range a figure is accepted in: every split of the threshold bucket the held spans support, and a
    hundredth of a point either side, to two decimals."""
    from math import ceil, floor
    lo, hi = min(vals) - BRIDGE_ROOM, max(vals) + BRIDGE_ROOM
    return [floor(lo * 100 + 1e-9) / 100.0, ceil(hi * 100 - 1e-9) / 100.0]


def figures(R):
    S, P = R["S"], R["P"]
    L = R["lattice"]
    over = list(P["over"])
    import analysis as A
    import datetime as dt
    win = R["window"]
    incs = []
    for x in R["incidents"]:
        if x["declared"] < A.DEC0:
            continue
        on = R["onset"][x["id"]]
        incs.append({"id": x["id"], "declared": lisbon(x["declared"]), "named": [s_ for s_, _ in x["named"]],
                     "cause": R["attribution"][x["id"]], "careful_cause": win[x["id"]],
                     "onset": {s_: (A.DEC0 + dt.timedelta(seconds=v[0])).strftime("%H:%M") for s_, v in on.items() if v},
                     "end": lisbon(x["end"])})
    for x in incs:
        x["onset_about"] = {s_: about(v) for s_, v in x["onset"].items()}
    r1 = lambda SS: {s: "%.1f" % K.r1(SS[s]["sli"]) for s in K.SVC}
    held = dt.datetime(2026, 12, 1) + dt.timedelta(hours=R["held_from"])
    gone_req = sum(R["fill"][s][1] for s in K.EDGE)
    all_req = sum(R["S"][s]["counted"] for s in K.EDGE)
    fam = R["family"]
    bridged = [s for s in K.SVC if R["bucket"][s] is not None]
    F = {"over": over, "over_count": len(over),
         "sli": r1(S),
         "sli2": {s: two(S[s]["sli"]) for s in K.SVC},
         "budget": {s: "%.1f" % R["bud"][s] for s in K.SVC},
         "threshold_ms": {s: "{:,}".format(int(R["thr"][s])) for s in K.SVC},
         "ran_over": {s: "yes" if s in over else "no" for s in K.SVC},
         "start_order": list(P["order"]),
         "share_pct": {s: "%d" % whole(P["share"][s]) for s in K.SVC},
         "together_pct": "%d" % whole(P["together"]),
         "beyond_budget": "{:,}".format(nearest(P["beyond"], 10000)),
         "ci": {s: [two(R["ci"][s][0]), two(R["ci"][s][1])] for s in over},
         "incidents": incs,
         "minutes": {s: ["%d" % whole(v) for v in R["minutes"][s]] for s in K.SVC},
         # where the export begins, and the share of December's edge requests in the hours before it
         "held_from": held.strftime("%-d December %H:%M"),
         "gone_days": "%d" % int((R["held_from"]) // 24),
         "gone_hours": "%d" % int(R["held_from"]),
         "gone_pct": "%d" % whole(100 * gone_req / all_req),
         # the services whose threshold sits inside a bucket of the span metrics, and the bucket
         "bridged": bridged,
         "exact": [s for s in K.SVC if s not in bridged],
         "bucket_ms": {s: "{:,} to {:,}".format(*R["bucket"][s]) for s in bridged},
         # the range each bridged SLI is accepted in: every split of its bucket the held spans support
         "sli_band": {s: [two(v) for v in band_of([f[s]["sli"] for f in fam.values()] +
                                                   [f[s]["sli"] for f in R["rivals"].values()])] for s in bridged},
         # each judgment made the hurried way alone, the other two as the review makes them
         "own_sli": r1(L["S1"]["S"]), "own_over": list(L["S1"]["P"]["over"]),
         "window_sli": r1(L["S2"]["S"]), "window_over": list(L["S2"]["P"]["over"]),
         "export_sli": r1(L["S3"]["S"]), "export_over": list(L["S3"]["P"]["over"]),
         # in pairs, and all three (the careful but hurried pass)
         "own_window_over": list(L["S1+S2"]["P"]["over"]),
         "own_export_over": list(L["S1+S3"]["P"]["over"]),
         "window_export_over": list(L["S2+S3"]["P"]["over"]),
         "careful_sli": r1(L["S1+S2+S3"]["S"]), "careful_over": list(L["S1+S2+S3"]["P"]["over"]),
         "quick_over": list(R["quick"]["P"]["over"]),
         # the threshold bucket split by straight-line interpolation instead of the held spans' own share
         "linear_sli": r1(R["naive"]["linear"])}
    # the bridge on the hours the export does hold: over-threshold requests rebuilt from the span metrics over those
    # counted span by span, with straight-line interpolation inside the bucket
    bc = R["bridge_check"]["linear"]
    F["linear_check"] = {s: "%.1f" % (bc[s][0] / bc[s][1]) for s in bridged}
    # a flat December share against the span metrics, for the service whose threshold is a boundary
    F["flat_sli"] = r1(R["loadfill"]["flat"])
    F["interval_level_pct"] = 90
    # what the split family spans on the programme's figures: the requests beyond budget and each share
    def beyond_of(SS):
        return sum(SS[s]["over_requests"] - R["bud"][s] / 100 * SS[s]["counted"] for s in over)
    def share_of(SS, s):
        return 100 * SS[s]["over_requests"] / sum(SS[x]["over_requests"] for x in K.SVC)
    bys = [beyond_of(f) for f in fam.values()]
    F["beyond_band"] = ["{:,}".format(nearest(min(bys), 10000) - 10000), "{:,}".format(nearest(max(bys), 10000) + 10000)]
    F["share_room_pts"] = 1
    F["share_spread_pts"] = "%.1f" % max(max(share_of(f, s) for f in fam.values()) - min(share_of(f, s) for f in fam.values())
                                         for s in over)
    F["ci_room"] = "0.06"
    F["ci_methods_room"] = "0.03"
    # straight-line interpolation on the hours the export holds: the least it over-counts on any basis (requests or
    # spans, with or without the incident hours), rounded down; and the order it would give
    from math import floor
    fl = lambda form, s_: "%.1f" % (floor(min(R["bridge_ratios"][form][s_].values()) * 10 + 1e-9) / 10.0)
    F["linear_floor"] = {s_: fl("linear", s_) for s_ in bridged}
    F["linear_first"] = R["naive_order"]["linear"][0]
    # the bucket's upper bound (every span in it counted as over the threshold) for journey-search
    F["upper_sli2"] = {s_: two(R["naive"]["upper"][s_]["sli"]) for s_ in bridged}
    F["upper_floor"] = {s_: fl("upper", s_) for s_ in bridged}
    F["sli_room"] = "0.1"
    F["span_metrics_bounds"] = "{:,}".format(1000)
    # the thinnest margin in the start order: the last two places' over-threshold requests
    od = list(P["order"])
    F["order_last_gap_pct"] = "%d" % whole(100 * (S[od[-2]]["over_requests"] / S[od[-1]]["over_requests"] - 1))
    F["order_last_two"] = od[-2:]
    F["root_cause"] = {x["id"]: x["cause"] for x in incs}
    F["ci_cells"] = ci_cells(R["ci"], over)
    F["programme_cells"] = programme_cells(P)
    # the incidents the whole-window reading puts on a caller, and those of them that decide a verdict
    F["misread"] = [x["id"] for x in incs if x["cause"] != x["careful_cause"]]
    F["deciding"] = [x["id"] for x in incs if x["cause"] != x["careful_cause"] and x["cause"] not in F["window_over"]]
    # the other readings of the same records and the lists they give, each a route a hurried review takes
    F["routes"] = [
        {"reading": "Kept spans unweighted; each incident on the service named first; the export's hours alone",
         "over": F["quick_over"]},
        {"reading": "Each service's own hourly count; each incident on the service furthest over its load curve; "
                    "the export's hours alone", "over": F["careful_over"]},
        {"reading": "Each service's own hourly count; causes dated; the hours before the export from the span "
                    "metrics", "over": F["own_over"]},
        {"reading": "Each span at its trace root's keep share; each incident on the service furthest over its load "
                    "curve; the hours before the export from the span metrics", "over": F["window_over"]},
        {"reading": "Each span at its trace root's keep share; causes dated; the export's hours alone",
         "over": F["export_over"]},
        {"reading": "Each span at its trace root's keep share; causes dated; the hours before the export from the "
                    "span metrics (this review)", "over": over, "golden": True}]
    return F


def ci_cells(ci, svcs):
    out = {}
    for s in svcs:
        out["%s lo" % s] = float(two(ci[s][0]))
        out["%s hi" % s] = float(two(ci[s][1]))
    return out


def programme_cells(P):
    out = {"order": ", ".join(P["order"]), "together": "%d" % whole(P["together"]),
           "beyond": "{:,}".format(nearest(P["beyond"], 10000))}
    for s in P["order"]:
        out["share %s" % s] = "%d" % whole(P["share"][s])
    return out


def chart_png(F):
    fig, ax = plt.subplots(figsize=(7.2, 4.1), dpi=150)
    svcs = list(K.SVC)[::-1]
    y = range(len(svcs))
    vals = [float(F["sli"][s]) for s in svcs]
    cols = ["#c0392b" if F["ran_over"][s] == "yes" else "#7f8c8d" for s in svcs]
    ax.barh(list(y), vals, color=cols, height=0.62)
    for i, s in enumerate(svcs):
        b = float(F["budget"][s])
        ax.plot([b, b], [i - 0.42, i + 0.42], color="#1f2d3d", linewidth=2.2)
        ax.text(max(vals[i], b) + 0.06, i, F["sli"][s], va="center", fontsize=8.5, color="#1f2d3d")
    ax.set_yticks(list(y))
    ax.set_yticklabels(["%s (budget %s%%)" % (s_, F["budget"][s_]) for s_ in svcs], fontsize=8.5)
    i_pg = svcs.index("partner-gateway")
    ax.annotate("%s%% against %s%%" % (F["sli"]["partner-gateway"], F["budget"]["partner-gateway"]),
                xy=(float(F["sli"]["partner-gateway"]), i_pg), xytext=(float(F["sli"]["partner-gateway"]) + 0.35, i_pg - 1.4),
                fontsize=8, color="#c0392b", arrowprops=dict(arrowstyle="-", color="#c0392b", lw=0.8))
    ax.set_title("%s services over their own error budget, December 2026" % ("Five" if len(F["over"]) == 5 else
                 str(len(F["over"]))), fontsize=10, loc="left", color="#1f2d3d")
    ax.set_xlabel("Latency SLI, December 2026 (% of requests slower than the threshold)", fontsize=8.5)
    ax.set_xlim(0, max(vals) + 0.6)
    ax.tick_params(axis="x", labelsize=8)
    for sp_ in ("top", "right"):
        ax.spines[sp_].set_visible(False)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#c0392b", label="over budget"), Patch(color="#7f8c8d", label="within budget"),
                       Line2D([0], [0], color="#1f2d3d", linewidth=2.2, label="error budget")],
              fontsize=8, frameon=False, loc="upper right")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _p(doc, text, bold=False, size=10.5, italic=False, space=4, color=None):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold, run.italic = bold, italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    para.paragraph_format.space_after = Pt(space)
    return para


def _table(doc, head, rows, right=()):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = "Table Grid"
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        _shade(c, "DCE6F0")
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = v
            if i in right:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    return t


def write_docx(path, R, F):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
        sec.top_margin = sec.bottom_margin = Cm(2.0)
    n = "Five" if len(F["over"]) == 5 else str(len(F["over"]))
    _p(doc, "Rotalinha Platform Reliability", bold=True, size=9, color=(0x55, 0x55, 0x55))
    _p(doc, "To: Engineering leadership group    From: %s, Platform Reliability    Date: 14 January 2027"
       % K.PEOPLE["head"], size=9, space=0)
    _p(doc, "Ref: PR-SLO-3 annual review 2026, latency objectives, read over December 2026 in Lisbon time", size=9,
       space=10)
    _p(doc, "%s services ran over their latency budget in 2026" % n, bold=True, size=16, space=8)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = "PR-SLO-3 annual review 2026    page "
    footer.runs[0].font.size = Pt(8)
    _page_field(footer)
    _p(doc, "%s services ran over their 2026 latency error budget and get a reliability engineer for January to June "
            "2027, starting in this order, the service whose SLI counts the most requests over its threshold first: "
            "%s." % (n, names(F["start_order"])), bold=True, size=11.5, space=8)
    _table(doc, ["Start", "Service", "Share of over-threshold requests (%)", "Latency SLI (%)",
                 "90% interval (%)", "Error budget (%)"],
           [[str(k), s_, F["share_pct"][s_], F["sli"][s_], "%s to %s" % tuple(F["ci"][s_]), F["budget"][s_]]
            for k, s_ in enumerate(F["start_order"], 1)], right=(0, 2, 3, 4, 5))
    _p(doc, "Source: trace_spans_2026-12.parquet and tracing_span_metrics_2026-12.csv weighted by the load balancer's "
            "hourly counts; budgets from PR-SLO-3 section 4. The interval is for the trace store's sample of "
            "December's requests.",
       italic=True, size=8, space=8)
    _p(doc, "Between them the %s served %s%% of the requests over their thresholds that all our services' SLIs count, "
            "about %s more than their budgets allow." % (n.lower(), F["together_pct"], F["beyond_budget"]), space=8)

    _p(doc, "Every service against its budget", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    _table(doc, ["Service", "Threshold (ms)", "Latency SLI (%)", "Error budget (%)", "Ran over"],
           [[s, F["threshold_ms"][s], F["sli"][s], F["budget"][s], F["ran_over"][s]] for s in K.SVC],
           right=(1, 2, 3))
    _p(doc, "Source: as above; thresholds from PR-SLO-3 section 4.", italic=True, size=8, space=8)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Cm(16.0))
    _p(doc, "Each bar is the service's December SLI; the dark mark on it is the service's own error budget.",
       italic=True, size=8.5, space=10)

    _p(doc, "December's customer-facing incidents", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    _p(doc, "PR-SLO-3 3.2 leaves a service's requests out of its SLI while a customer-facing incident named it, unless "
            "it owned the incident's root cause. December's post-incident reviews were still open, so the review "
            "dated, for each service an incident named, when its own handling of requests rose above what its load "
            "that hour would explain; the earliest rise owns the cause.", space=4)
    _table(doc, ["Incident", "Declared (Lisbon)", "Services named, in order", "Root cause owned by"],
           [[x["id"], x["declared"], ", ".join(x["named"]), x["cause"]] for x in F["incidents"]])
    _p(doc, "Source: incidents_2026.csv, incident_timeline_2026.csv, status_page_history_2026.json and the span "
            "export.", italic=True, size=8, space=8)
    dec = [x for x in F["incidents"] if x["id"] in F["deciding"]]
    if dec:
        _p(doc, "%s are the ones to read twice. %s Charged to %s, they would leave %s at %s." % (
            names([x["id"] for x in dec]),
            " ".join("In %s, %s slowed from about %s, and %s only backed up behind it from about %s." % (
                x["id"], handling(x["cause"]), x["onset_about"][x["cause"]], handling(x["careful_cause"]),
                x["onset_about"][x["careful_cause"]]) for x in dec),
            names([x["careful_cause"] for x in dec]), names([x["cause"] for x in dec]),
            ("%s%% each" % F["window_sli"][dec[0]["cause"]]) if len({F["window_sli"][x["cause"]] for x in dec}) == 1
            else names(["%s%%" % F["window_sli"][x["cause"]] for x in dec])), space=10)

    _p(doc, "How the SLI was read", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    _p(doc, "The tracing store keeps a trace whole or not at all, and decides where the trace starts: each edge service "
            "keeps about the same number of traces every hour whatever its traffic. Each kept server span therefore "
            "counts for the requests its trace's edge service handled in the hour the trace started, over the traces it "
            "kept then, from the load balancer's hourly counts. For an internal service that weight belongs to the "
            "caller, not to the service: fares, partner-gateway and notifications are called from busy, thinly kept "
            "edge services for their slow operations and from quiet ones for their fast ones, so their own hourly "
            "counts, with the same incident time left out, would put them at %s%%, %s%% and %s%%." % (
                F["own_sli"]["fares"], F["own_sli"]["partner-gateway"], F["own_sli"]["notifications"]))
    _p(doc, "The trace export begins at %s: by the day it was pulled the store no longer held the spans of December's "
            "first %s days, %s%% of the month's edge requests, and those requests still count. The store's span "
            "metrics do hold them: an hourly duration histogram of every span it ingested, by service and span name. "
            "For those hours each series' spans over the service's threshold come from the histogram, weighted like "
            "the spans themselves (an internal operation by the keep shares of the edge services whose traces called "
            "it that hour). Where the threshold is a histogram boundary nothing is estimated (%s). Where it sits "
            "inside a bucket (%s), the bucket is split at the share of its spans over the threshold that the "
            "service's held, incident-free spans show in the same band of hourly load." % (
                F["held_from"], F["gone_days"], F["gone_pct"], names(F["exact"]), names(F["bridged"])), space=4)
    _p(doc, "The first weeks were quieter than the holiday weeks the export holds: read on the export's hours alone "
            "journey-search would be at %s%% and over its budget; across December it is %s%%. Splitting a bucket by "
            "straight-line interpolation instead would count %s times the over-threshold requests the spans "
            "themselves show for %s in the hours the export holds, so the review does not use it." % (
                F["export_sli"]["journey-search"], F["sli"]["journey-search"],
                F["linear_check"]["places"], "places"), space=8)
    _p(doc, "The interval treats the kept traces as the sample they are: drawn within each edge service's hours, a "
            "whole trace at a time, so a service's spans in one trace move together and a thinly kept hour weighs more; "
            "the hours read from the span metrics add their own sampling error and the error of the bucket's split.",
       space=8)
    _p(doc, "The same records read other ways give other lists:", space=4).paragraph_format.keep_with_next = True
    _table(doc, ["Reading of the December spans", "Services over budget"],
           [[x["reading"], names(x["over"]) if x["over"] else "none"] for x in F["routes"]])
    _p(doc, "Source: trace_spans_2026-12.parquet, tracing_span_metrics_2026-12.csv and the load balancer's hourly "
            "counts, with the exclusions of PR-SLO-3 3.2 under each attribution.", italic=True, size=8, space=10)
    _p(doc, "Notes: SLIs are per cents to one decimal; intervals are to two decimals. Shares and the requests beyond "
            "budget are worked from the unrounded figures. December in Lisbon time is UTC throughout, and the trace "
            "export's re-sent spans are counted once.", italic=True, size=8.5)
    doc.save(path)


def _shade(cell, fill):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    tc = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    tc.append(sh)


def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = par.add_run()
    run.font.size = Pt(8)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            run._r.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            run._r.append(it)


def write_csv(path, R, F):
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["service", "latency_sli_pct", "error_budget_pct", "ran_over", "incident_minutes_h1",
                     "incident_minutes_h2"])
        for s in K.SVC:
            wr.writerow([s, F["sli"][s], F["budget"][s], F["ran_over"][s]] + F["minutes"][s])
