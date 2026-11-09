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


def figures(R):
    S, P, Sc, Pc = R["S"], R["P"], R["careful"]["S"], R["careful"]["P"]
    over = list(P["over"])
    import analysis as A
    import datetime as dt
    incs = []
    for x in R["incidents"]:
        if x["declared"] < A.DEC0:
            continue
        on = R["onset"][x["id"]]
        incs.append({"id": x["id"], "declared": lisbon(x["declared"]), "named": [s_ for s_, _ in x["named"]],
                     "cause": R["attribution"][x["id"]], "careful_cause": R["careful"]["attribution"][x["id"]],
                     "onset": {s_: (A.DEC0 + dt.timedelta(seconds=v[0])).strftime("%H:%M") for s_, v in on.items() if v},
                     "end": lisbon(x["end"])})
    for x in incs:
        x["onset_about"] = {s_: about(v) for s_, v in x["onset"].items()}
    F = {"over": over, "over_count": len(over),
         "sli": {s: "%.1f" % K.r1(S[s]["sli"]) for s in K.SVC},
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
         # the careful but hurried pass: each service's own spans reweighted on its own hourly count, each incident put
         # on the service whose own handling ran furthest over its load curve across the whole incident
         "careful_over": list(Pc["over"]),
         "careful_sli": {s: "%.1f" % K.r1(Sc[s]["sli"]) for s in K.SVC},
         # the root weights with that attribution
         "rootcareful_sli": {s: "%.1f" % K.r1(R["rootcareful"]["S"][s]["sli"]) for s in K.SVC},
         # each service's own hourly count with the golden's exclusions: the weighting the only change
         "owncount_sli": {s: "%.1f" % K.r1(R["hint_i5"]["S"][s]["sli"]) for s in K.SVC},
         "owncount_over": list(R["hint_i5"]["P"]["over"]),
         "rootcareful_over": list(R["rootcareful"]["P"]["over"])}
    F["interval_level_pct"] = 90
    F["root_cause"] = {x["id"]: x["cause"] for x in incs}
    F["ci_cells"] = ci_cells(R["ci"], over)
    F["programme_cells"] = programme_cells(P)
    # the incidents the whole-window reading puts on a caller, and those of them that decide a verdict
    F["misread"] = [x["id"] for x in incs if x["cause"] != x["careful_cause"]]
    F["deciding"] = [x["id"] for x in incs if x["cause"] != x["careful_cause"] and x["cause"] not in F["rootcareful_over"]]
    # the other readings of the same spans and the lists they give, each a route a hurried review takes
    F["routes"] = [
        {"reading": "Kept spans unweighted; each incident on the service named first",
         "over": list(R["quick"]["P"]["over"])},
        {"reading": "Each service's spans on its own hourly count; each incident on the service furthest over its load "
                    "curve across the incident", "over": list(Pc["over"])},
        {"reading": "Each service's spans on its own hourly count; causes dated by when own handling rose",
         "over": list(R["hint_i5"]["P"]["over"])},
        {"reading": "Each span at its trace root's keep share; each incident on the service furthest over its load "
                    "curve", "over": list(R["rootcareful"]["P"]["over"])},
        {"reading": "Each span at its trace root's keep share; causes dated by when own handling rose (this review)",
         "over": over, "golden": True}]
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
    _p(doc, "To: Engineering leadership group    From: %s, Platform Reliability    Date: 8 January 2027"
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
    _p(doc, "Source: trace_spans_2026-12.parquet weighted by the load balancer's hourly counts; budgets from PR-SLO-3 "
            "section 4. The interval is for the trace store's sample of December's requests.",
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
            ("%s%% each" % F["rootcareful_sli"][dec[0]["cause"]]) if len({F["rootcareful_sli"][x["cause"]] for x in dec}) == 1
            else names(["%s%%" % F["rootcareful_sli"][x["cause"]] for x in dec])), space=10)

    _p(doc, "How the SLI was read", bold=True, size=12, space=4).paragraph_format.keep_with_next = True
    _p(doc, "The tracing store keeps a trace whole or not at all, and decides where the trace starts: each edge service "
            "keeps about the same number of traces every hour whatever its traffic. Each kept server span therefore "
            "counts for the requests its trace's edge service handled in the hour the trace started, over the traces it "
            "kept then, from the load balancer's hourly counts. For an internal service that weight belongs to the "
            "caller, not to the service: fares, partner-gateway and notifications are called from busy, thinly kept "
            "edge services for their slow operations and from quiet ones for their fast ones, so their own hourly "
            "counts, with the same incident time left out, would put them at %s%%, %s%% and %s%%." % (
                F["owncount_sli"]["fares"], F["owncount_sli"]["partner-gateway"], F["owncount_sli"]["notifications"]))
    _p(doc, "The interval treats the kept traces as the sample they are: drawn within each edge service's hours, a "
            "whole trace at a time, so a service's spans in one trace move together and a thinly kept hour weighs more.",
       space=8)
    _p(doc, "The same spans read other ways give other lists:", space=4).paragraph_format.keep_with_next = True
    _table(doc, ["Reading of the December spans", "Services over budget"],
           [[x["reading"], names(x["over"]) if x["over"] else "none"] for x in F["routes"]])
    _p(doc, "Source: trace_spans_2026-12.parquet and the load balancer's hourly counts, with the exclusions of PR-SLO-3 "
            "3.2 under each attribution.", italic=True, size=8, space=10)
    _p(doc, "Notes: SLIs are per cents to one decimal and are compared with the budget as rounded (PR-SLO-3 3.4); "
            "intervals are to two decimals. Shares and the requests beyond budget are worked from the unrounded "
            "figures. December in Lisbon time is UTC throughout, and the trace export's re-sent spans are counted "
            "once.", italic=True, size=8.5)
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
