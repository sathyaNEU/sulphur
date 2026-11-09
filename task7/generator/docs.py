"""task7 architecture 7: the pack's documents. Each PDF is a Word document exported by LibreOffice Writer
(officepdf.py); the committee request stays a Word document. They file the WHAT (what a saving is, normal weather, a
round's lifetime tonnes and grant per tonne, the limit, the pilot's and the 2026 round's terms, the annual report's
season saving, the utility's normalisation) and describe nothing of how a saving is to be estimated, which buildings
compare, how a saving carries over a measure's life or to a building, or how a round is projected."""
import datetime as dt
import os

from docx import Document
from docx.shared import Mm, Pt
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import golden as GD
import officepdf
import postprocess as PP
import world as W

CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#1F4E46")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#1F4E46")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def climate_plan(target):
    lives = [["Measure", "Service life (years)"], ["Insulation", str(GD.LIFE["insulation"])],
             ["Heating optimisation", str(GD.LIFE["heating optimisation"])],
             ["Heating controls", str(GD.LIFE["heating controls"])]]
    s = [P("Stadt Haldenau", SMALL), P("Climate Action Plan 2023: extract", H1),
         P("Adopted by the city council on 16 March 2023. Section 4 of 9. Prepared by the Climate Protection Office.",
           SMALL),
         P("4 Efficiency grants for commercial buildings heated by gas", H2),
         P("Commercial buildings burned about a fifth of the gas supplied in Haldenau in 2022. The city's target of "
           "climate neutrality by 2035 needs that use to fall by more than half, and grants for efficiency measures in "
           "the buildings that use most are one of the plan's instruments."),
         P("4.1 The programme", H2),
         P("The council grants 30 per cent of a contractor's quoted cost, at most €40,000, for one of three measures in a "
           "commercial building heated by gas: insulation of the roof, top-floor ceiling or walls (insulation); "
           "hydraulic balancing, new pumps and a new heating curve (heating optimisation); or room-by-room and "
           "time-based controls (heating controls). The offer is made in Stadtwerke Haldenau's benchmarking notice. A "
           "round is set by the council's Committee for Climate and Environment."),
         P("4.2 Saving", H2),
         P("A measure's saving in a season is the gas its works save, as a share of the gas the buildings that had "
           "them would have used that season without them, both in a season of long-term average weather. The council "
           "takes the evidence of each measure's saving from the 2019 pilot."),
         P("4.3 Normal weather", H2),
         P("A season runs from 1 May to 30 April. Gas use in a season of long-term average weather is the season's use "
           "normalised as Stadtwerke Haldenau normalises it for its benchmarking notices."),
         P("4.4 Appraisal of a round", H2),
         P("An application's lifetime tonnes are the CO2 in the gas its measure's works would save in the building "
           "applied for over the measure's service life, each year's saving taken on the application's reference "
           "consumption, at 0.201 tonnes of CO2 per MWh of gas. A measure's saving rate on a round's applications is "
           "their lifetime tonnes as a share of the tonnes their reference consumption carries over the same life. A "
           "measure's grant per tonne in a round is the grant of the round's applications for it divided by their "
           "lifetime tonnes. The council funds a measure in a round when its grant per tonne is €120 or less, and then "
           "funds every application for that measure in the round."),
         T(lives, [140, 120]),
         P("4.5 Reference consumption", H2),
         P("An application's reference consumption is the normalised use per square metre printed on the notice that "
           "carried the offer, times the building's heated floor area in Stadtwerke Haldenau's register."),
         P("4.6 Monitoring", H2),
         P("The Climate Protection Office reports each year to the committee on the CO2 the programme's works saved in "
           "the season just ended: the gas the buildings with works would have used that season without them, less what "
           "they used, both in normal weather, at the factor in 4.4.")]
    path = os.path.join(target, "climate_action_plan_2023_extract.pdf")
    officepdf.build(path, s, "Climate Action Plan 2023: extract", "Klimaschutzstelle Stadt Haldenau",
                    "Climate Action Plan 2023", "Stadt Haldenau | Climate Action Plan 2023 | Section 4",
                    dt.datetime(2023, 3, 16, 11, 5, tzinfo=CET), dt.datetime(2023, 3, 20, 14, 22, tzinfo=CET),
                    producer="LibreOffice 7.5")


def pilot_rules(target):
    s = [P("Stadt Haldenau and Stadtwerke Haldenau", SMALL),
         P("Pilot 2019: efficiency grants for commercial buildings", H1),
         P("Terms of the pilot, as approved by the Committee for Climate and Environment on 9 April 2019.", SMALL),
         P("1 Who is offered a grant", H2),
         P("The offer goes with Stadtwerke Haldenau's benchmarking notice of May 2019 to every commercial building whose "
           "notice places it in the top fifth of its use type."),
         P("2 How to respond", H2),
         P("An owner responds by 30 June 2019, naming one measure (insulation, heating optimisation or heating controls) "
           "and enclosing a contractor's quote. The grant is 30 per cent of the quoted cost, at most €40,000."),
         P("3 The places", H2),
         P("The pilot's budget funds a little under half of the responses for each measure. Places are drawn by lot "
           "among the responses for each measure at a public draw at the town hall on 8 July 2019, under the eye of the "
           "city's legal office. Owners not drawn may apply in a later round."),
         P("4 The works", H2),
         P("A drawn owner has the works done by 30 September 2019, before the heating season, and sends the "
           "contractor's invoice. The grant is paid on completion; an owner who withdraws loses the place."),
         P("5 Records", H2),
         P("The Climate Protection Office keeps the responses, the result of the draw, withdrawals and completion dates.")]
    path = os.path.join(target, "pilot_2019_rules.pdf")
    officepdf.build(path, s, "Pilot 2019: efficiency grants for commercial buildings", "Klimaschutzstelle Stadt Haldenau",
                    "Pilot 2019", "Stadt Haldenau | Pilot 2019 | Terms",
                    dt.datetime(2019, 4, 9, 16, 40, tzinfo=CEST), dt.datetime(2019, 4, 10, 9, 15, tzinfo=CEST),
                    producer="LibreOffice 6.2")


def round_terms(target):
    s = [P("Stadt Haldenau, Climate Protection Office", SMALL),
         P("Efficiency grants for commercial buildings 2026: terms of the offer", H1),
         P("As approved by the Committee for Climate and Environment on 21 April 2026.", SMALL),
         P("1 The offer", H2),
         P("The offer goes with Stadtwerke Haldenau's benchmarking notice of May 2026 to every commercial building whose "
           "notice places it in the top fifth of its use type, except buildings that had works under the 2019 pilot. It "
           "is open until 30 June 2026."),
         P("2 Applications", H2),
         P("An owner applies by 30 June 2026, naming one measure (insulation, heating optimisation or heating controls) "
           "and enclosing a contractor's quote. The grant is 30 per cent of the quoted cost, at most €40,000. An owner "
           "who revises the quote sends the application again; the later application replaces the earlier one."),
         P("3 The round", H2),
         P("The committee sets at its July meeting which measures the round funds, under section 4 of the climate action "
           "plan. For a funded measure every application received by 30 June 2026 is granted; for any other measure "
           "none is."),
         P("4 The works", H2),
         P("A granted owner has the works done by 30 September 2026 and sends the contractor's invoice. The grant is paid "
           "on completion; an owner who withdraws, or whose works are not completed by then, receives nothing."),
         P("5 Records", H2),
         P("The Climate Protection Office keeps the applications and passes them to Stadtwerke Haldenau for the "
           "appraisal.")]
    path = os.path.join(target, "grant_offer_2026_terms.pdf")
    officepdf.build(path, s, "Efficiency grants 2026: terms of the offer", "Klimaschutzstelle Stadt Haldenau",
                    "Grant offer 2026", "Stadt Haldenau | Efficiency grants 2026 | Terms",
                    dt.datetime(2026, 4, 21, 15, 10, tzinfo=CEST), dt.datetime(2026, 4, 22, 8, 55, tzinfo=CEST),
                    producer="LibreOffice 25.2")


def method(target, w):
    hw = [["Use", "Hot water and process share"]] + [[t, "%d per cent" % round(100 * W.HW_SHARE[t])] for t in W.TYPES]
    s = [P("Stadtwerke Haldenau, Energy Services", SMALL), P("Gas benchmarking for commercial customers: method", H1),
         P("Version 2, May 2022 (version 1, March 2019). Owner: Torben Römer, head of Energy Services.", SMALL),
         P("1 Seasons and reads", H2),
         P("A season runs from 1 May to 30 April, and commercial meters are read for it on 30 April. Where a read is "
           "taken on another day, the use between two reads is shared over the days between them in proportion to each "
           "day's weight: the use type's hot water and process share spread evenly over the days of the year, and the "
           "rest in proportion to the day's degree figure at the Haldenau station (20 less the day's mean temperature "
           "on days below 15 degrees, nothing on warmer days). Where a read is estimated and later replaced, the "
           "replacement counts."),
         P("2 Cubic metres to kWh", H2),
         P("A meter counts cubic metres, some in tens of cubic metres (the meter factor). The kWh billed are the "
           "cubic metres times the meter point's z-number times the season's billing calorific value for the network "
           "area. Network area HN-3 changed from L-gas to H-gas on 1 May 2017."),
         P("3 Normalising for the weather", H2),
         P("A season's use is normalised to long-term average weather as VDI 3807 sets out: the hot water and process "
           "share of the use type is held as it is, and the rest is scaled by the station's long-term degree days "
           "(G20/15, 1991 to 2020 mean, %d) over the season's." % round(w.G_LT)),
         T(hw, [140, 160]),
         P("4 The notice", H2),
         P("Each May the notice goes to every commercial building supplied for the whole of the season just ended and "
           "the one before, whose normalised use per square metre of heated floor area is in the top fifth of its use "
           "type. It prints the heated floor area the figure is taken on, the building's normalised use per square metre "
           "and the median for its use type.")]
    path = os.path.join(target, "benchmarking_method_2022.pdf")
    officepdf.build(path, s, "Gas benchmarking for commercial customers: method", "Torben Römer", "Benchmarking method",
                    "Stadtwerke Haldenau | Energy Services | Benchmarking method v2",
                    dt.datetime(2022, 5, 3, 10, 2, tzinfo=CEST), dt.datetime(2022, 5, 9, 15, 30, tzinfo=CEST),
                    producer="LibreOffice 7.3")


def heat_plan(target):
    rows = [["Area", "Districts", "Heat supply foreseen", "Earliest connection"],
            ["Priority area 1", "Altstadt, Bahnhofsviertel, Hafen", "district heating extension", "2029"],
            ["Priority area 2", "Neckarvorstadt, Uferviertel", "district heating, new network", "2031"],
            ["Priority area 3", "Gewerbegebiet Nord, Gewerbegebiet Süd", "industrial waste heat", "2032"],
            ["Rest of the city", "all other districts", "individual supply (heat pumps, biomass)", "-"]]
    s = [P("Stadt Haldenau", SMALL), P("Municipal heat plan 2026: summary", H1),
         P("Published 27 March 2026 under the Heat Planning Act. The full plan runs to 214 pages.", SMALL),
         P("The heat plan sets out how Haldenau's buildings are to be heated without fossil fuels by 2040. It names "
           "priority areas where district heating is expected to reach most buildings, and leaves the rest of the city "
           "to individual heat supply. It does not oblige any building to connect."),
         T(rows, [85, 155, 150, 85]),
         P("Owners of gas-heated buildings in the priority areas should weigh a connection before replacing a boiler. "
           "Elsewhere the plan expects heat pumps to carry most new installations from 2028.")]
    path = os.path.join(target, "municipal_heat_plan_2026_summary.pdf")
    officepdf.build(path, s, "Municipal heat plan 2026: summary", "Stadtplanungsamt Haldenau", "Heat plan",
                    "Stadt Haldenau | Heat plan 2026 | Summary",
                    dt.datetime(2026, 3, 27, 9, 0, tzinfo=CET), dt.datetime(2026, 3, 27, 9, 40, tzinfo=CET),
                    producer="LibreOffice 25.8")


def federal_overview(target):
    rows = [["Federal programme (BEG EM)", "Grant", "Bonus"],
            ["Building envelope (insulation, windows)", "15 per cent", "5 points with a renovation roadmap"],
            ["Heating optimisation", "15 per cent", "none"],
            ["Heat pumps", "30 per cent", "up to 40 points with bonuses"],
            ["Connection to district heating", "30 per cent", "up to 40 points with bonuses"]]
    s = [P("Energieagentur Region Haldenau", SMALL), P("Federal funding for efficiency in buildings: overview 2025", H1),
         P("Information sheet for owners of non-residential buildings, January 2025.", SMALL),
         P("The federal programme for efficient buildings (BEG) funds single measures in existing buildings. Grants "
           "can be combined with municipal grants up to 60 per cent of the eligible cost."),
         T(rows, [190, 80, 175]),
         P("Applications go to BAFA before the contract is signed. Eligible costs are capped per square metre of floor "
           "area. Gas boilers have not been funded since 2024.")]
    path = os.path.join(target, "federal_funding_overview_2025.pdf")
    officepdf.build(path, s, "Federal funding for efficiency in buildings: overview 2025", "Energieagentur Region Haldenau",
                    "Funding overview", "Energieagentur Region Haldenau | Funding overview 2025",
                    dt.datetime(2025, 1, 14, 13, 20, tzinfo=CET), dt.datetime(2025, 1, 15, 8, 5, tzinfo=CET),
                    producer="LibreOffice 24.8")


def committee_request(target):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    paras = [
        "Stadt Haldenau, Committee for Climate and Environment",
        "From: Magda Peukert, chair",
        "To: Torben Römer, head of Energy Services, Stadtwerke Haldenau",
        "Date: 15 June 2026",
        "Subject: the 2026 efficiency grant round",
        "Dear Mr Römer,",
        "The committee sets the 2026 round at its meeting on 9 July. The May notices carried the offer again, open to 30 "
        "June, and the Climate Protection Office has passed you the applications that came in by 12 June. Your paper goes "
        "out with the agenda on 26 June.",
        "Under the climate action plan we fund a measure only where its grant per tonne of CO2 on this year's "
        "applications is €120 or less. Before the meeting we need your view of which measures to fund and how sure you "
        "are of each, with what the pilot showed season by season, the workbook the office will use to issue the "
        "grants, and what the round will actually pay once the offer has closed and the works are done.",
        "The plan's annual report also needs the CO2 the pilot's works saved in the season to April 2026, as section 4.6 "
        "sets it out.",
        "With thanks and best wishes,",
        "Magda Peukert"]
    for t in paras:
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(6)
    cp = doc.core_properties
    cp.title, cp.author, cp.last_modified_by = "The 2026 efficiency grant round", "Magda Peukert", "Magda Peukert"
    path = os.path.join(target, "committee_request_2026-06-15.docx")
    doc.save(path)
    PP.normalize_docx(path, "Magda Peukert", "Magda Peukert", "2026-06-15T07:48:00Z", "2026-06-15T08:31:00Z", 3, 41,
                      "task7-committee-request", "The 2026 efficiency grant round", "Stadt Haldenau")


def write_all(target, w):
    climate_plan(target)
    pilot_rules(target)
    round_terms(target)
    method(target, w)
    heat_plan(target)
    federal_overview(target)
    committee_request(target)
