"""task3 architecture 4: the pack's documents. Fenwright Hydrogeologic's 2019 wellhead protection plan for the Sallow
Road well field, Corlinden Water Utility's 2025 water supply plan, and the production wells' construction logs, each
written as a Word document and exported to PDF by LibreOffice Writer (officepdf)."""
import datetime as dt

import numpy as np
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

reportlab.rl_config.invariant = 1
CST = dt.timezone(dt.timedelta(hours=-6))
CDT = dt.timezone(dt.timedelta(hours=-5))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.8, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
UTILITY = "Corlinden Water Utility"
FENWRIGHT = "Fenwright Hydrogeologic"


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


CLASS_NAMES = {"FOR": "Forest and plantation", "GRS": "Grassland, pasture and conservation grass",
               "DRY": "Cropland and hay, not irrigated", "IRC": "Irrigated corn and soybean",
               "IRV": "Irrigated vegetable rotation", "RES": "Residential and farmstead", "WAT": "Open water, wetland"}


def whpa_report(path, truth):
    zones = []
    for w in P.WELLS:
        ps = [p for p in truth["parcels"] if p["zone"] == w]
        ac = sum(p["acres"] for p in ps)
        t5 = sum(p["acres"] for p in ps if p["T"] <= 5.0)
        tt = sum(p["acres"] * p["T"] for p in ps) / ac
        zones.append([P.WELL_NAMES[w], "%d" % len(ps), "{:,.0f}".format(ac), "{:,.0f}".format(t5), "%.1f" % tt])
    wb = [[CLASS_NAMES[c], "%.1f" % P.RECHARGE[c]] for c in P.CLASSES if c != "WAT"]
    s = [Paragraph("Sallow Road Well Field Wellhead Protection Plan", H1),
         Paragraph("Prepared for Corlinden Water Utility by Fenwright Hydrogeologic, "
                   "Patricia Gaines, P.G. Final, 14 November 2019.", SMALL),
         Spacer(1, 4),
         Paragraph("1. Purpose", H2),
         Paragraph("This plan delineates the zones of contribution of the utility's four production wells at the "
                   "Sallow Road well field (Wells 3, 5, 6 and 7), the land within five years' groundwater time of "
                   "travel of each well, and the parcels within each zone, for the utility's wellhead protection "
                   "program and its ordinance review. It replaces the 1998 delineation, which used a fixed radius.",
                   BODY),
         Paragraph("2. Hydrogeologic setting", H2),
         Paragraph("The well field lies on the outwash plain of the central sand plain, about 1.2 miles west of the "
                   "Cadle River. The aquifer is unconfined sand and gravel outwash, 95 to 130 ft thick, over "
                   "Cambrian sandstone. West of the well field the Sallow Ridge, an ice-contact ridge of fine to "
                   "medium sand, rises 40 to 70 ft above the plain. The water table lies 8 to 40 ft below the plain "
                   "and 55 to 100 ft below the ridge. Groundwater moves east-southeast from the ridge and the "
                   "upland beyond it toward the Cadle River, which receives the aquifer's discharge. Recharge is "
                   "from precipitation and, on irrigated land, from irrigation water applied in excess of crop use.",
                   BODY),
         Paragraph("3. Groundwater flow model", H2),
         Paragraph("A steady-state groundwater flow model of the Cadle River basin (one layer, 200 ft cells) was "
                   "calibrated to 64 water levels measured in May 2017 and to the Cadle River's base flow at the "
                   "County Road K gauge. Recharge was assigned by land cover (Table 1). Particles were tracked "
                   "backward from each production well at the pumping rates in the utility's 2019 capital plan for "
                   "2025 onward, with an effective porosity of 0.28. A parcel's groundwater time of travel is the "
                   "flow-weighted mean travel time of the particles that start at the water table beneath it and "
                   "reach the well. The model reproduces the 2017 water levels with a root mean square error of "
                   "1.4 ft and the base flow within 6 per cent.", BODY),
         Paragraph("Table 1. Recharge by land cover in the calibrated model (inches a year)", CELLB),
         _table([["Land cover", "Recharge"]] + wb, [96, 30]),
         Spacer(1, 6),
         Paragraph("4. Zones of contribution", H2),
         Paragraph("Each well's zone of contribution is the land whose recharge reaches that well. The zones of "
                   "Wells 6 and 7 extend west across the Sallow Ridge; the zone of Well 3 lies on the river "
                   "terrace south of the well field. Table 2 summarises the zones; the parcel attributes (Appendix "
                   "B) are supplied as the spreadsheet sallow_road_WHPA_parcel_attributes_2019.xlsx.", BODY),
         Paragraph("Table 2. Zones of contribution", CELLB),
         _table([["Well", "Parcels", "Zone (acres)", "Within 5 years (acres)", "Mean time of travel (years)"]] + zones,
                [26, 18, 26, 38, 44]),
         Spacer(1, 6),
         Paragraph("5. Potential contaminant source inventory", H2),
         Paragraph("Land uses and facilities in the zones that can release contaminants to groundwater: irrigated "
                   "and non-irrigated cropland (nitrogen and pesticides), private onsite wastewater systems in the "
                   "residential parcels, County Road K and the Sallow Road (road salt), one farm fuel storage "
                   "site, and the abandoned Sallow gravel pit. No regulated facility lies within five years' time of "
                   "travel of any well.", BODY),
         Paragraph("6. Recommendations", H2),
         Paragraph("(1) Adopt the zones as the wellhead protection overlay district. (2) Seek nutrient management "
                   "agreements and cost-share with the operators of irrigated land in the zones. (3) Offer "
                   "voluntary purchase or easement to owners of forested parcels within five years' time of "
                   "travel. (4) Continue quarterly raw-water sampling at each well and review this plan within ten "
                   "years.", BODY)]
    O.build(path, s, "Sallow Road Well Field Wellhead Protection Plan", FENWRIGHT,
            "Wellhead protection plan, Sallow Road well field, Corlinden", "Fenwright Hydrogeologic, Sallow Road WHPP",
            dt.datetime(2019, 11, 14, 9, 20, tzinfo=CST), dt.datetime(2019, 11, 14, 16, 2, tzinfo=CST))


def supply_plan(path):
    sh = [[P.WELL_NAMES[w], "%d" % round(P.HIST_SHARE[w] * 100), "%d" % round(P.PLAN_SHARE[w] * 100)] for w in P.WELLS]
    mgd = [["%d" % y, "%.2f" % (P.FIELD_MGD * (1 + 0.006 * (y - 2025)))] for y in (2027, 2030, 2035, 2040)]
    s = [Paragraph("Corlinden Water Utility: 2025 Water Supply Plan", H1),
         Paragraph("Adopted by the Corlinden Common Council, 9 September 2025. Prepared by the utility's general "
                   "manager, Chloe Griffin, and operations superintendent, Dennis Diaz.", SMALL),
         Spacer(1, 4),
         Paragraph("1. The system", H2),
         Paragraph("The utility serves about 14,300 people and two food processors from the Sallow Road well field. "
                   "Wells 3, 5, 6 and 7 pump to a common header; the blended water is chlorinated and fluoridated "
                   "at the Sallow Road pump house and enters the distribution system at entry point EP-01. Average "
                   "day demand in 2025 was 1.62 million gallons.", BODY),
         Paragraph("2. Pumping plan, 2027 to 2040", H2),
         Paragraph("Well 3, the oldest well, has a corroded casing and produces sand at high rates; from 1 January "
                   "2027 it is operated as a peaking well, and Wells 5, 6 and 7 carry the base load. The plan's "
                   "shares of annual pumping are fixed for 2027 to 2040 and do not depend on demand, which is met "
                   "within the wells' capacity in every year.", BODY),
         Paragraph("Table 1. Share of annual pumping by well (per cent)", CELLB),
         _table([["Well", "2009 to 2026 (typical)", "2027 to 2040 (plan)"]] + sh, [30, 44, 44]),
         Spacer(1, 4),
         Paragraph("Table 2. Average day pumping (million gallons a day)", CELLB),
         _table([["Year", "Average day"]] + mgd, [30, 40]),
         Spacer(1, 6),
         Paragraph("3. Nitrate", H2),
         Paragraph("The nitrate standard is 10 mg/L as nitrogen (44.27 mg/L as nitrate). The utility meets it at "
                   "the entry point: the "
                   "standard applies to the blended water at EP-01, and the utility's compliance and planning "
                   "measure is the annual flow-weighted mean nitrate at EP-01. Each well's raw water is sampled "
                   "quarterly and EP-01 monthly.", BODY),
         Paragraph("4. Project NR-1: nitrate removal", H2),
         Paragraph("Project NR-1 is an anion exchange plant at the Sallow Road pump house treating the blended "
                   "flow before EP-01. It is to be funded through the state's Safe Drinking Water Loan Program. "
                   "The utility can carry one loan of this size in the program's 2027 cycle or, after the 2016 "
                   "water main bonds retire, in its 2031 cycle; no cycle between is open to it. A project on the "
                   "2027 cycle's priority list (intent to apply by 15 December 2026) is designed in 2027 and built "
                   "in 2028 and 2029, entering service on 1 January 2030. A project on the 2031 cycle enters "
                   "service on 1 January 2034.", BODY),
         Paragraph("The plant must be in service before the first calendar year in which the annual flow-weighted "
                   "mean nitrate at EP-01 reaches 10 mg/L as nitrogen. The Common Council chooses the cycle at "
                   "its December 2026 meeting.", BODY),
         Paragraph("5. Other capital items", H2),
         Paragraph("Well 3 replacement study (2028); Sallow Road pump house electrical (2027); water main "
                   "replacement on Fourth Street and Kessel Avenue (2029 and 2030); elevated tank painting (2031).",
                   BODY)]
    O.build(path, s, "Corlinden Water Utility 2025 Water Supply Plan", UTILITY,
            "2025 water supply plan as adopted", "Corlinden Water Utility, 2025 Water Supply Plan",
            dt.datetime(2025, 9, 2, 10, 40, tzinfo=CDT), dt.datetime(2025, 9, 10, 8, 15, tzinfo=CDT))


def well_logs(path):
    logs = {
        "W3": (1971, 118, (88, 118), 9.4, [("0-4", "Topsoil and silty sand"), ("4-61", "Sand, fine to medium, brown"),
                                         ("61-112", "Sand and gravel, medium to coarse"), ("112-121", "Sand, coarse"),
                                         ("121-124", "Sandstone, weathered (bottom of hole)")]),
        "W5": (1979, 131, (96, 131), 16.8, [("0-3", "Topsoil"), ("3-58", "Sand, fine to medium"),
                                          ("58-127", "Sand and gravel"), ("127-133", "Sand, coarse, some gravel"),
                                          ("133-136", "Sandstone")]),
        "W6": (1984, 138, (103, 138), 21.5, [("0-2", "Topsoil"), ("2-49", "Sand, fine to medium, brown"),
                                           ("49-134", "Sand and gravel, medium to coarse, grey below 90 ft"),
                                           ("134-140", "Sand, coarse"), ("140-142", "Sandstone")]),
        "W7": (1996, 141, (106, 141), 24.2, [("0-3", "Topsoil and silty sand"), ("3-71", "Sand, fine to medium"),
                                           ("71-138", "Sand and gravel"), ("138-144", "Gravel, coarse"),
                                           ("144-147", "Sandstone")]),
    }
    s = [Paragraph("Sallow Road Well Field: Production Well Construction Records", H1),
         Paragraph("Compiled from the well constructor's reports on file with Corlinden Water Utility. Depths in feet "
                   "below land surface.", SMALL), Spacer(1, 4)]
    for w in P.WELLS:
        yr, depth, scr, swl, lith = logs[w]
        s += [Paragraph("%s (constructed %d)" % (P.WELL_NAMES[w], yr), H2),
              _table([["Item", "Record"], ["Depth", "%d ft" % depth], ["Casing", "16 in steel to %d ft" % scr[0]],
                      ["Screen", "16 in stainless, %d to %d ft, 0.060 in slot" % scr],
                      ["Static water level at completion", "%.1f ft" % swl],
                      ["Test", "24-hour test at completion, see the specific capacity record"]], [60, 100]),
              Spacer(1, 3),
              _table([["Interval (ft)", "Formation"]] + [list(x) for x in lith], [30, 130]), Spacer(1, 6)]
    O.build(path, s, "Sallow Road production well construction records", UTILITY,
            "Construction records, Wells 3, 5, 6 and 7", "Corlinden Water Utility, well records",
            dt.datetime(2021, 3, 8, 13, 5, tzinfo=CST), dt.datetime(2021, 3, 8, 13, 5, tzinfo=CST))
