"""task3 documents: the county's road design standard (chapter 7 excerpt), the state's regional flood equations
report (Region 3 excerpt) and the hydraulic consultant's span ratings, each a Word document exported by LibreOffice
Writer the way the issuing office writes it."""
import datetime as dt

import numpy as np
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import freq as F
import officepdf as O
import world as W

PT = dt.timezone(dt.timedelta(hours=-8))
PDT = dt.timezone(dt.timedelta(hours=-7))

# The consultant's rated flows: the largest discharge each span carries with 2.0 ft of freeboard to the low chord.
SPANS = [(140, 20500), (185, 29000), (240, 40000)]
COSTS = {140: 6.84, 185: 8.47, 240: 10.92}
RETURN_PERIODS = (2, 10, 25, 50, 100, 500)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=10.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def county_standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Pelton County Department of Public Works", small),
         Paragraph("Road Design Standards, Chapter 7: Drainage Structures and Bridges (excerpt, sections 7.1 and 7.4)", h1),
         Paragraph("Revision 6, adopted by the Board of County Commissioners on 14 March 2023 (Resolution 2023-031). "
                   "Sections 7.2, 7.3 and 7.5 to 7.9 (culverts, ditches, scour countermeasures, fish passage) are not "
                   "reproduced.", small),
         Spacer(1, 6),
         Paragraph("7.1 Application", h2),
         Paragraph("This chapter applies to every drainage structure and bridge the County designs, replaces or "
                   "rehabilitates on a County road, including projects funded through the state's local programs "
                   "office. A bridge over a stream is designed under 7.4.", body),
         Paragraph("7.4 Bridges over streams", h2),
         Paragraph("7.4.1 <b>Design flood.</b> The design flood is the peak flow with a 1 per cent chance of being "
                   "equalled or exceeded in any one year (the 1 per cent annual exceedance probability flood), taken as "
                   "the instantaneous peak discharge at the bridge, on the climate of the gauged and station records. "
                   "No allowance for a future climate is applied on County roads.", body),
         Paragraph("7.4.2 <b>Freeboard and span.</b> A bridge carries the design flood with at least 2.0 ft between the "
                   "water surface and the low chord. The hydraulic consultant reports for each span considered its "
                   "rated flow, the largest discharge it carries with that freeboard. The span selected is the shortest "
                   "whose rated flow is at least the design flood.", body),
         Paragraph("7.4.3 <b>Estimating the design flood.</b> For a basin of 10 square miles or less, the rational "
                   "method or a rainfall-runoff model calibrated in the County's drainage manual is used. For a larger "
                   "basin the design flood comes from stream gauge records, in this order: (a) the record of a gauge at "
                   "the site where it holds 25 years or more of annual peaks; otherwise (b) the record of the nearest "
                   "gauged basin holding 25 years or more of annual peaks, carried to the site; (c) the state's regional "
                   "flood equations only where no gauged basin within 15 miles of the site holds such a record, and only "
                   "inside the ranges of the equations' explanatory variables.", body),
         Paragraph("7.4.4 <b>Frequency curves.</b> Flood frequency curves follow Bulletin 17C (U.S. Geological Survey "
                   "Techniques and Methods, book 4, chapter B5): the log-Pearson Type III distribution fitted to annual "
                   "peaks by the expected moments algorithm, potentially influential low floods identified by the "
                   "Multiple Grubbs-Beck test, and the station skew weighted with the regional skew given in the state's "
                   "regional flood report for the region the basin lies in.", body),
         Paragraph("7.4.5 <b>Hydraulic report.</b> The hydraulic report filed with the design states the basin's drainage "
                   "area, the 50 per cent and 1 per cent annual exceedance probability flows at the site, the records and "
                   "methods used, the spans considered with their rated flows and how often each rated flow would be "
                   "exceeded, and the span selected under 7.4.2.", body),
         Spacer(1, 6),
         Paragraph("Approved: County Engineer, Pelton County Department of Public Works.", small)]
    O.build(path, s, "Road Design Standards, Chapter 7 (excerpt)", "Pelton County Public Works",
            "Drainage structures and bridges", "Pelton County Road Design Standards, rev. 6, chapter 7 (excerpt)",
            dt.datetime(2026, 4, 7, 10, 12, 41, tzinfo=PDT), dt.datetime(2026, 4, 7, 10, 12, 41, tzinfo=PDT))


def regional_equations(W_, maps, years=range(1951, 2026)):
    """The state's Region 3 equations, fitted to the region's gauged basins (the river, the four regional gauges and the
    twelve other basins of the state study): log10 Q_T = a + b log10 A + c log10 P, A the drainage area (sq mi), P the
    basin's mean annual precipitation (in)."""
    idx = [0, 2, 3, 4, 5] + list(range(6, len(W_.basins)))
    rows = []
    for k in idx:
        b = W_.basins[k]
        pk = W.annual_peaks(W_, k)
        q = np.array([pk[y][0] for y in years])
        par = F.fit(q)
        rows.append((b["area"], maps[k], [F.quantile(par, 1.0 / T) for T in RETURN_PERIODS], par["station_skew"]))
    A = np.array([r[0] for r in rows])
    P = np.array([r[1] for r in rows])
    X = np.column_stack([np.ones(len(A)), np.log10(A), np.log10(P)])
    eq = {}
    for j, T in enumerate(RETURN_PERIODS):
        y = np.log10([r[2][j] for r in rows])
        beta, res, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        se = float(np.sqrt((resid ** 2).sum() / (len(y) - 3)))
        eq[T] = dict(a=float(10 ** beta[0]), b=float(beta[1]), c=float(beta[2]), se_log=se,
                     se_pct=float(100 * np.sqrt(np.exp((se * np.log(10)) ** 2) - 1)))
    return eq, dict(n=len(rows), area=(float(A.min()), float(A.max())), map=(float(P.min()), float(P.max())),
                    mean_skew=float(np.mean([r[3] for r in rows])))


def state_report(path, eq, rng_info):
    body, h1, h2, small, cell = _styles()
    rows = [["Return period (years)", "Annual exceedance probability", "a", "b (drainage area)", "c (precipitation)",
             "Standard error of prediction (per cent)"]]
    for T in RETURN_PERIODS:
        e = eq[T]
        rows.append([str(T), "%.3g" % (1.0 / T), "%.4g" % e["a"], "%.3f" % e["b"], "%.3f" % e["c"], "%.0f" % e["se_pct"]])
    s = [Paragraph("Washington State Department of Transportation, Hydraulics Section, in cooperation with the "
                   "U.S. Geological Survey Washington Water Science Center", small),
         Paragraph("Magnitude and Frequency of Floods in Western Washington, 2019 Update: Region 3, Cascade West Slope "
                   "(excerpt: sections 4 and 5, tables 3 and 4)", h1),
         Paragraph("Excerpt reproduced for project files.", small),
         Spacer(1, 6),
         Paragraph("4. Regional regression equations", h2),
         Paragraph("Peak flows at ungaged sites in Region 3 are estimated with equations of the form "
                   "Q<sub>T</sub> = a A<super>b</super> P<super>c</super>, where Q<sub>T</sub> is the T-year peak flow "
                   "(cubic feet per second), A the drainage area (square miles) and P the mean annual precipitation over "
                   "the basin (inches, 1981-2010 normals). The equations were fitted by generalized least squares to the "
                   "Bulletin 17C frequency curves of the region's long-record gauges (%d gauges with 25 years or more of "
                   "systematic record through water year 2018)." % rng_info["n"], body),
         _grid(rows, [62, 72, 52, 62, 62, 80], cell),
         Spacer(1, 4),
         Paragraph("Table 3. Region 3 regression coefficients.", small),
         Paragraph("4.2 Applicability. The equations apply to unregulated basins in Region 3 whose explanatory "
                   "variables lie inside the ranges of the gauged basins used to fit them: drainage area %.1f to %.0f "
                   "square miles, mean annual precipitation %.0f to %.0f inches. Estimates outside these ranges are not "
                   "supported by the data and are not to be used for design." % (
                       rng_info["area"][0], rng_info["area"][1], rng_info["map"][0], rng_info["map"][1]), body),
         Paragraph("5. Regional skew", h2),
         Paragraph("The regional skew coefficient of the logarithms of annual peak flows for Region 3 is %.2f, with a "
                   "mean square error of %.2f, from a Bayesian generalized least squares regional skew analysis of the "
                   "region's gauges. It is weighted with the station skew under Bulletin 17C." % (
                       F.REGIONAL_SKEW, F.REGIONAL_SKEW_MSE), body),
         _grid([["Region", "Regional skew", "Mean square error", "Equivalent record length (years)"],
                ["3, Cascade west slope", "%.2f" % F.REGIONAL_SKEW, "%.2f" % F.REGIONAL_SKEW_MSE, "61"]],
               [110, 90, 90, 130], cell),
         Paragraph("Table 4. Regional skew.", small)]
    O.build(path, s, "Magnitude and Frequency of Floods in Western Washington, Region 3", "WSDOT Hydraulics Section",
            "Regional flood equations", "WSDOT state flood study (2019), Region 3 excerpt",
            dt.datetime(2024, 5, 14, 9, 3, 17, tzinfo=PDT), dt.datetime(2024, 5, 14, 9, 3, 17, tzinfo=PDT))


def consultant_tm(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Alternative", "Clear span (ft)", "Low chord elevation (ft, NAVD 88)", "Rated flow, 2.0 ft freeboard (cfs)",
             "Water surface at the rated flow (ft)", "Construction estimate (USD million, 2026)"]]
    for j, (span, q) in enumerate(SPANS):
        lc = 638.4 + 2.6 * j
        rows.append(["%s" % "ABC"[j], "%d" % span, "%.1f" % lc, "{:,}".format(q), "%.1f" % (lc - 2.0), "%.2f" % COSTS[span]])
    rating = [["Discharge (cfs)"] + ["%d ft span" % sp for sp, _ in SPANS]]
    for qd in range(4000, 48001, 4000):
        line = ["{:,}".format(qd)]
        for j, (sp, qr) in enumerate(SPANS):
            lc = 638.4 + 2.6 * j
            ws = (lc - 2.0) - 7.6 * (1 - (qd / qr) ** 0.42)
            line.append("%.1f%s" % (ws, " *" if qd > qr else ""))
        rating.append(line)
    s = [Paragraph("Hess Hydraulic Engineering PLLC", small),
         Paragraph("Technical memorandum: Durrow Creek Bridge 2209-04 replacement, Ransom Bar Road. Hydraulic rating of "
                   "the span alternatives", h1),
         Paragraph("To: Amy Rasmussen, PE, Bridge Engineer, Pelton County Department of Public Works. From: Frederick "
                   "Hess, PE. Date: 21 September 2026.", small),
         Spacer(1, 6),
         Paragraph("1. Purpose", h2),
         Paragraph("The County asked us to rate the three clear-span alternatives developed at the type, size and "
                   "location stage for the replacement of bridge 2209-04, where Ransom Bar Road crosses Durrow Creek. "
                   "This memorandum gives each alternative's rated flow under section 7.4.2 of the County's road design "
                   "standards. Design discharges are the County's; this memorandum rates the openings only and makes no "
                   "estimate of flood frequency.", body),
         Paragraph("2. Model", h2),
         Paragraph("A one-dimensional steady-flow HEC-RAS 6.4 model of 1.9 miles of Durrow Creek, 31 cross sections "
                   "from the County's 2025 lidar and our April 2026 channel survey, bridge modelled by the energy method "
                   "with pressure and weir flow checks. Manning's n 0.042 in the channel and 0.085 to 0.10 on the "
                   "forested overbanks, from the survey's bed material counts and the 2009 high-water marks. Downstream "
                   "boundary normal depth at a slope of 0.0061 ft/ft. Each alternative keeps the existing profile grade "
                   "of Ransom Bar Road and raises the low chord as the deeper superstructure of a longer span requires.",
                   body),
         Paragraph("3. Results", h2),
         _grid(rows, [52, 50, 78, 78, 80, 78], cell),
         Spacer(1, 4),
         Paragraph("Table 1. Rated flows of the span alternatives.", small),
         Spacer(1, 4),
         _grid(rating, [90, 110, 110, 110], cell),
         Spacer(1, 4),
         Paragraph("Table 2. Water surface elevation at the upstream face (ft, NAVD 88) against discharge. An asterisk "
                   "marks a discharge above the alternative's rated flow.", small),
         Paragraph("4. Notes", h2),
         Paragraph("Scour at the abutments, the debris allowance and the fish passage review are reported separately. "
                   "We are glad to re-run the rating if the County's design discharge falls between the alternatives' "
                   "rated flows and an intermediate span is wanted.", body)]
    O.build(path, s, "Durrow Creek Bridge 2209-04: hydraulic rating of span alternatives", "Hess Hydraulic Engineering PLLC",
            "Hydraulic rating", "Hess Hydraulic Engineering PLLC, TM 26-118",
            dt.datetime(2026, 9, 21, 15, 47, 9, tzinfo=PDT), dt.datetime(2026, 9, 21, 15, 47, 9, tzinfo=PDT))
