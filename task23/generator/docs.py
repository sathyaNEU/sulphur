"""task23 architecture 1: the documents in the pack, each a Word document its issuing office exported to PDF
(officepdf): the Solid Waste Division's 2027 gas collection options for Council with Resolution 2025-41, the
division's 2025 greenhouse gas report under the state reporting rule, Tessaline Environmental's whole-site methane
survey for the state, and Brightwater Geoscience's 2019 cover oxidation study."""
import datetime as dt

import numpy as np
import pandas as pd
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf
import params as P

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.0, spaceAfter=0, leading=9.8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")
PST = dt.timezone(dt.timedelta(hours=-8))
PDT = dt.timezone(dt.timedelta(hours=-7))

# filed sentences the checks and the verifier read back
RES_LIMIT = ("Section 2. Fernhallow Regional Landfill's methane emissions in calendar year 2027 shall not exceed "
             "%s metric tons. Methane emissions means the methane leaving the site to the atmosphere over the year "
             "from every surface of the landfill and from the flare and the engines.")
RES_RULE = ("Section 3. The Solid Waste Division shall bring to the Council, with the January 2027 budget "
            "amendment, the least-cost package from its 2027 gas collection plan that it expects to keep 2027 at or "
            "under the limit in Section 2 in a year of normal weather.")
CELL5_RECIRC = ("Cell 5 was built with leachate injection lines in every lift and has taken recirculated leachate "
                "across its whole footprint since July 13, 2026.")
CAPTURE_NOTE = ("Design capture is the share of the methane generated in cell 5 that the new collectors take from "
                "their in-service date: %d per cent with the horizontal collectors alone, %d per cent once the "
                "vertical wells are in.")
PUMPS_NOTE = ("Package C's pumps go into every cell 4 well whose liquid stood above the bottom of its screen at the "
              "October 2026 liquid level survey and hold the liquid below the screen, as the June 2025 pilot pumps do.")
CAP_NOTE = "Package E's cap brings cell 4's collection to %d per cent of its methane from the month it is complete."
CLOSED_NOTE = ("The closed cells (1 to 3) are carried at the 2015 closure plan's design collection of %d per cent of "
               "their methane.")
RULE_EQ = ("Methane emissions are the collected methane divided by the area-weighted collection efficiency, less "
           "the collected methane, times one less the oxidation fraction, plus the collected methane times one less "
           "the destruction efficiency.")


def P_(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P_(str(c), CELL) for c in r] for r in rows], colWidths=[w * 72 / 25.4 for w in widths_mm])


def fmt(x, d=0):
    return ("{:,.%df}" % d).format(x)


# ------------------------------------------------------------------ the options paper for Council
def plan(path):
    pk = P.PACKAGES
    rows = [["Package", "Works", "In service", "Capital cost (USD million)"],
            ["A", "Plan of record: cell 5 gas collection installed at final grade in 2029; no new works in 2027",
             "-", "0.00"],
            ["B", "Horizontal collectors in cell 5's completed lifts, connected to the header", "May 1, 2027",
             "%.2f" % pk["B"]["cost"]],
            ["C", "Package B, and pneumatic pumps in cell 4's wells with liquid above the screen",
             "May 1, 2027 (pumps)", "%.2f" % pk["C"]["cost"]],
            ["D", "Package C, and 18 vertical wells with pumps across cell 5's completed area", "June 1, 2027 (wells)",
             "%.2f" % pk["D"]["cost"]],
            ["E", "Package D, and a geomembrane cap on cell 4's north and east slopes", "October 1, 2027 (cap)",
             "%.2f" % pk["E"]["cost"]]]
    story = [
        P_("<b>KELLOWAY COUNTY SOLID WASTE DIVISION</b>  |  Fernhallow Regional Landfill", LH),
        P_("For the County Council's January 2027 budget amendment. Prepared October 28, 2026.", LH),
        Spacer(1, 8),
        P_("Fernhallow Regional Landfill: 2027 Gas Collection Options", TITLE),
        P_("1. Why this paper", H2),
        P_("In September 2025 the Council adopted Resolution 2025-41 after the state's first survey campaigns at "
           "Fernhallow found emissions well above the Division's reported figures. Sections 2 and 3 of the resolution are reproduced "
           "in the attachment. This paper sets out the gas collection packages the Division has costed for 2027. "
           "The Division will bring one of them to the Council with the January 2027 budget amendment."),
        P_("2. The site and the gas system", H2),
        P_("Fernhallow has five cells. Cells 1 to 3 are closed under final cover with a geomembrane. Cell 4 took "
           "waste from April 2013 to January 2025 and is under intermediate cover; leachate has been recirculated "
           "into it through the converted horizontal collectors since April 2023. Cell 5 opened in February 2025 "
           "and will fill into 2028. " + CELL5_RECIRC + " The gas collection system draws on the wells of cells 1 "
           "to 4 and sends the gas to two 1.6 MW engines and an enclosed flare. Under the plan of record cell 5 has "
           "no gas collection until it reaches final grade in 2029."),
        P_("3. The packages", H2),
        P_("The packages build on each other: each includes the works of the one before."),
        T(rows, [16, 92, 33, 33]),
        Spacer(1, 6),
        P_("4. Design basis", H2),
        P_(CAPTURE_NOTE % (round(P.CE5_HC * 100), round(P.CE5_WELLS * 100)) + " The vertical wells in package D "
           "carry pumps from installation because cell 5 takes recirculated leachate."),
        P_(PUMPS_NOTE),
        P_(CAP_NOTE % round(P.CE4_CAP * 100)),
        P_(CLOSED_NOTE % round(P.CE_CLOSED_DESIGN * 100)),
        P_("Waste receipts for cell 5 through 2027 are in the Division's 2027 fill plan. Capital costs are the "
           "Division's engineer's estimates at 2026 prices and include design, construction and connection."),
        P_("5. What the Council will be asked", H2),
        P_("To fund, in the January 2027 budget amendment, the package the Division brings under Section 3."),
        Spacer(1, 10),
        P_("<b>Attachment: Resolution 2025-41 (adopted September 16, 2025), Sections 2 and 3</b>", BODY),
        P_(RES_LIMIT % fmt(P.LIMIT_T)),
        P_(RES_RULE),
    ]
    officepdf.build(path, story, "Fernhallow Regional Landfill: 2027 Gas Collection Options", P.ENGINEER,
                    "2027 gas collection options for Council", "Kelloway County Solid Waste Division",
                    dt.datetime(2026, 10, 27, 15, 12, tzinfo=PDT), dt.datetime(2026, 10, 28, 10, 41, 9, tzinfo=PDT),
                    producer="LibreOffice 25.2")


# ------------------------------------------------------------------ the 2025 greenhouse gas report
def ghg_report(path, R_col, history_rows, wip_tons, monthly=None):
    A = P.RULE_AREAS_2025
    ac = {k: v / 4046.86 for k, v in A.items()}
    ce = sum(a * P.RULE["ce"][k] for k, a in A.items()) / sum(A.values())
    gen = R_col / ce
    em = (gen - R_col) * (1 - P.RULE["ox"]) + R_col * (1 - P.RULE["de"])
    rows = [["Area", "Cover and collection", "Acres", "Collection efficiency (rule Table 3)"],
            ["Cells 1 to 3", "Final cover, active collection", fmt(ac["final"], 1), "0.95"],
            ["Cell 4", "Intermediate cover, active collection", fmt(ac["intermediate"], 1), "0.75"],
            ["Cell 5 (filled area)", "Daily and interim cover, no collection", fmt(ac["none"], 1), "0.00"],
            ["Site", "Area-weighted", fmt(sum(ac.values()), 1), "%.4f" % ce]]
    hist = [["Reporting year", "Methane collected (t)", "Methane emissions reported (t)"]] + \
        [[str(y), fmt(c), fmt(e)] for y, c, e in history_rows]
    story = [
        P_("<b>KELLOWAY COUNTY SOLID WASTE DIVISION</b>  |  State Greenhouse Gas Reporting Rule, landfills", LH),
        P_("Annual report, reporting year 2025. Submitted March 27, 2026.", LH),
        Spacer(1, 8),
        P_("Fernhallow Regional Landfill: Greenhouse Gas Report, Reporting Year 2025", TITLE),
        P_("1. Facility", H2),
        P_("Fernhallow Regional Landfill, Kelloway County. Municipal solid waste landfill with an active gas "
           "collection and control system (enclosed flare and two engines). Waste in place at December 31, 2025: "
           "%s tons." % fmt(wip_tons)),
        P_("2. Method", H2),
        P_("The report uses the rule's collection-based method for landfills with gas collection. " + RULE_EQ +
           " The collection efficiency is the area-weighted value from the rule's Table 3 for each area's cover and "
           "collection status; the oxidation fraction is the rule's default of 0.10; the destruction efficiency for "
           "an enclosed flare and engines is the rule's default of 0.99. Collected methane is the gas system's "
           "metered flow times its methane fraction, summed hourly, at 0.0192 kg of methane per standard cubic foot."),
        T(rows, [36, 62, 22, 54]),
        Spacer(1, 6),
        P_("3. Results for 2025", H2),
        T([["Quantity", "2025"],
           ["Methane collected and sent to the flare and engines (t)", fmt(R_col)],
           ["Area-weighted collection efficiency", "%.4f" % ce],
           ["Methane generated, collected methane over collection efficiency (t)", fmt(gen)],
           ["Oxidation fraction", "0.10"],
           ["Destruction efficiency", "0.99"],
           ["Methane emissions (t)", fmt(em)]], [120, 54]),
        Spacer(1, 6),
        P_("4. Methane collected by month, 2025", H2),
        P_("From the gas plant's hourly record: the flare's and each engine's metered flow times the methane fraction "
           "its analyzer read in that hour (the engines' analyzer where the flare's was out of service or reading "
           "below 5 per cent)."),
        T([["Month", "Methane collected (t)"]] + [[m, fmt(v, 1)] for m, v in (monthly or [])] +
          [["2025", fmt(R_col, 1)]], [50, 50]),
        Spacer(1, 6),
        P_("5. Reported emissions, 2021 to 2025", H2),
        T(hist, [40, 60, 70]),
        Spacer(1, 6),
        P_("Prepared by N. Wheeler, Landfill Gas and Compliance Engineer. Certified by the Solid Waste Division "
           "Manager."),
    ]
    officepdf.build(path, story, "Greenhouse Gas Report, Reporting Year 2025", P.ENGINEER,
                    "State greenhouse gas reporting rule, landfills, RY2025", "Kelloway County Solid Waste Division",
                    dt.datetime(2026, 3, 19, 9, 2, tzinfo=PDT), dt.datetime(2026, 3, 27, 16, 18, 44, tzinfo=PDT),
                    producer="LibreOffice 25.2")
    return em, gen, ce


# ------------------------------------------------------------------ the state's survey
def survey(path, camp):
    c = camp.copy()
    c25 = c[pd.to_datetime(c["date"]).dt.year == 2025]
    rate25 = float(c25["site_kg_h"].mean())
    annual = rate25 * 8.76
    rows = [["Campaign", "Date", "Local time", "Tracers", "Wind (m/s)", "Transects", "Site (kg/h)",
             "Cell 4 (kg/h)", "Cell 5 (kg/h)"]]
    for _, r in c.iterrows():
        rows.append([r["campaign"], pd.Timestamp(r["date"]).strftime("%b %d, %Y"),
                     "%s to %s" % (r["start_local"], r["end_local"]), r["tracers"], "%.1f" % r["wind_ms"],
                     str(r["transects"]), "%d ± %d" % (r["site_kg_h"], r["site_sd_kg_h"]),
                     "-" if pd.isna(r["cell4_kg_h"]) else "%d ± %d" % (r["cell4_kg_h"], r["cell4_sd_kg_h"]),
                     "-" if pd.isna(r["cell5_kg_h"]) else "%d ± %d" % (r["cell5_kg_h"], r["cell5_sd_kg_h"])])
    story = [
        P_("<b>TESSALINE ENVIRONMENTAL</b>  |  for the State Department of Environmental Stewardship", LH),
        P_("Final report, contract DES-24-118, September 2026.", LH),
        Spacer(1, 8),
        P_("Whole-Site Methane Emission Measurements at Fernhallow Regional Landfill, 2025 and 2026", TITLE),
        P_("Summary", H2),
        P_("Tessaline Environmental measured whole-site methane emissions at Fernhallow Regional Landfill on four "
           "days in 2025 and four days in 2026 by tracer correlation. The 2025 campaigns averaged %s kg of methane "
           "per hour, equivalent to %s metric tons over a year of 8,760 hours. The 2026 campaigns released a second "
           "tracer so that cell 4 and cell 5 could be measured separately." % (fmt(rate25), fmt(annual))),
        P_("Method", H2),
        P_("A known flow of acetylene was released at the centre of the area of interest and, in 2026, nitrous oxide "
           "at cell 5's working area. A cavity ring-down analyzer in a vehicle crossed the combined plume on public "
           "roads 1 to 3 km downwind. Each transect's methane enhancement was integrated against each tracer's, and "
           "the emission rate is the tracer release rate times the integrated ratio times the ratio of molecular "
           "weights. A campaign is carried out between about 10:00 and 15:00 local time on a day with no "
           "precipitation during the measurements or in the three hours before, and with wind between 2.5 and "
           "8 m/s throughout (3 to 7 m/s when two tracers are released). Campaigns were scheduled in three-week "
           "windows and carried out on the first day in each window that met these conditions."),
        P_("Site and conditions", H2),
        P_("Public roads cross the plume at 1 to 3 km on the north, east and south sides of the site, so every "
           "campaign day with westerly to southerly winds could be measured. The table gives each campaign's mean "
           "transect distance, wind and air temperature from the vehicle's mast."),
        T([["Campaign", "Mean distance (km)", "Wind direction (deg)", "Air temperature (C)"]] +
          [[r["campaign"], "%.1f" % r["mean_distance_km"], "%d" % r["wind_dir_deg"], "%.1f" % r["air_temp_c"]]
           for _, r in c.iterrows()], [40, 40, 40, 40]),
        Spacer(1, 6),
        P_("Quality assurance", H2),
        P_("Tracer release rates were set by mass flow controllers and checked against the cylinders' weights before "
           "and after each campaign. The analyzer was checked against two certified methane standards and an "
           "acetylene standard at the start and end of each day. A transect was kept when the methane and tracer "
           "plumes overlapped and the tracer's peak enhancement was at least ten times the analyzer's noise; a "
           "campaign needs at least eight kept transects."),
        P_("Results", H2),
        T(rows, [21, 21, 21, 18, 13, 14, 22, 22, 22]),
        Spacer(1, 6),
        P_("Uncertainties are one standard deviation of the transect estimates. The 2025 annual equivalent "
           "(%s metric tons) is %.1f times the emissions the Division reported for 2025 under the state rule."
           % (fmt(annual), annual / P.REPORTED_2025 if P.REPORTED_2025 else 0.0)),
        P_("Project lead: D. Martinez. Field team: K. Osei, L. Varga."),
    ]
    officepdf.build(path, story, "Whole-Site Methane Emission Measurements at Fernhallow Regional Landfill",
                    P.SURVEY_LEAD, "Tracer correlation survey, 2025 and 2026", P.CONTRACTOR,
                    dt.datetime(2026, 9, 8, 13, 30, tzinfo=PDT), dt.datetime(2026, 9, 18, 11, 6, 37, tzinfo=PDT),
                    producer="LibreOffice 25.2")
    return annual


# ------------------------------------------------------------------ the 2019 oxidation study
def ox_study(path, plots):
    s = plots.dropna(subset=["fraction_oxidized"])
    rows = [["Cover", "Plots", "Measurements", "Mean surface flux (g/m2/d)", "Mean fraction oxidized", "95% interval"]]
    names = {"final": "Final cover (cells 2 and 3)", "intermediate": "Intermediate cover (cell 4)",
             "active": "Daily cover (cell 4 working area)"}
    for cv in ("final", "intermediate", "active"):
        ss = s[s["cover"] == cv]
        m = ss["fraction_oxidized"].mean()
        se = ss["fraction_oxidized"].std(ddof=1) / np.sqrt(len(ss))
        rows.append([names[cv], str(ss["plot_id"].nunique()), str(len(ss)), "%.1f" % ss["surface_flux_g_m2_d"].mean(),
                     "%.2f" % m, "%.2f to %.2f" % (m - 1.96 * se, m + 1.96 * se)])
    seas = [["Cover", "Visit", "Soil temperature (C)", "Mean surface flux (g/m2/d)", "Mean fraction oxidized"]]
    vm = pd.to_datetime(s["visit_date"]).dt.month
    for cv in ("final", "intermediate", "active"):
        for mth, lab in ((2, "February"), (5, "May"), (8, "August"), (11, "November")):
            ss = s[(s["cover"] == cv) & (vm == mth)]
            seas.append([names[cv].split(" (")[0], lab, "%.1f" % ss["soil_temp_c"].mean(),
                         "%.1f" % ss["surface_flux_g_m2_d"].mean(), "%.2f" % ss["fraction_oxidized"].mean()])
    story = [
        P_("<b>BRIGHTWATER GEOSCIENCE</b>  |  for the Kelloway County Solid Waste Division", LH),
        P_("Report BG-19-064, January 2020.", LH),
        Spacer(1, 8),
        P_("Methane Oxidation in the Covers at Fernhallow Regional Landfill, 2019", TITLE),
        P_("1. Purpose", H2),
        P_("The Division asked for site measurements of the share of methane oxidized in Fernhallow's covers, for "
           "comparison with the reporting rule's default oxidation fraction of 0.10."),
        P_("2. Method", H2),
        P_("Forty-four plots were set on cells 2 and 3 (final cover), on cell 4's completed lifts (intermediate "
           "cover) and on cell 4's working area (daily cover). Each plot was visited in February, May, August and "
           "November 2019. At each visit a static chamber measured the methane flux at the surface, a soil gas "
           "probe below the cover sampled the methane before oxidation, and the stable carbon isotope ratio of "
           "each was measured. The fraction oxidized is the difference between the emitted and the below-cover "
           "ratio divided by 25 per mil, the fractionation of methane oxidation in landfill cover soils. Seven runs "
           "whose isotope analysis failed are excluded."),
        P_("3. Results", H2),
        T(rows, [44, 14, 22, 32, 30, 30]),
        Spacer(1, 6),
        P_("Table 2 gives the same means for each visit."),
        T(seas, [44, 24, 30, 30, 30]),
        Spacer(1, 6),
        P_("The plot measurements are in the accompanying data file. The final covers oxidized most of the methane "
           "reaching them at every visit; the intermediate and daily covers oxidized a smaller share."),
        P_("Prepared by T. Achebe, PG, and S. Ruiz."),
    ]
    officepdf.build(path, story, "Methane Oxidation in the Covers at Fernhallow Regional Landfill, 2019",
                    "Brightwater Geoscience", "Cover oxidation study", P.CONSULTANT,
                    dt.datetime(2020, 1, 22, 14, 5, tzinfo=PST), dt.datetime(2020, 1, 29, 15, 47, 21, tzinfo=PST),
                    producer="LibreOffice 6.3")


def write_all(target, F, R_col, history_rows, wip_tons, monthly=None):
    f = {k: target + "/" + v for k, v in P.FILES.items()}
    em, gen, ce = ghg_report(f["ghg2025"], R_col, history_rows, wip_tons, monthly)
    P.REPORTED_2025 = round(em)
    annual = survey(f["survey"], F["campaigns"])
    ox_study(f["oxstudy"], F["oxplots"])
    plan(f["plan"])
    return dict(reported_2025=round(em), survey_2025=round(annual), rule_gen_2025=gen, rule_ce_2025=ce)
