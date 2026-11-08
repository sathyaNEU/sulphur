"""task3's documents: Tamsett County's drainage standard (section 4, culverts and bridges on county roads), the roads
division's Kinnard Road culvert alternatives, and the 2024 inspection of the failing culvert. The standard files the
design flow as a forward quantity and names no method; the alternatives give each culvert's capacity and cost."""
import datetime as dt
import os

from docx import Document
from docx.shared import Pt

import common as K


def _doc():
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    return d


def _meta(d, author, created, title):
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = created
    cp.modified = created
    cp.title = title
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.revision = 3


def _p(d, text, bold=False, size=None, italic=False):
    para = d.add_paragraph()
    run = para.add_run(text)
    run.bold, run.italic = bold, italic
    if size:
        run.font.size = Pt(size)
    return para


def write_standard(path):
    d = _doc()
    _p(d, "Tamsett County Drainage Standard", bold=True, size=14)
    _p(d, "Section 4. Culverts and bridges on county roads", bold=True, size=12)
    _p(d, "Adopted by the Board of Commissioners 14 March 2017, Resolution 2017-22. Administered by the Roads "
          "Division.", italic=True, size=9)
    _p(d, "4.1 Scope", bold=True)
    _p(d, "This section applies to every new or replacement culvert and bridge that carries a county road over a "
          "stream with a drainage area of one square mile or more.")
    _p(d, "4.2 Design flow", bold=True)
    _p(d, "A crossing shall pass its design flow without overtopping the road. The design flow is the peak discharge "
          "that has a 1 per cent chance of being equalled or exceeded in any one year of the crossing's first ten "
          "years of service. Flows are stated in cubic feet per second.")
    _p(d, "4.3 Flow information", bold=True)
    _p(d, "Where a stream gauge at or near the crossing has ten or more years of annual peak flows, the design flow "
          "shall be estimated from the full length of the gauge's record together with the other records the county "
          "holds for the watershed. Where no such gauge exists, the design flow shall be estimated by the methods of the state "
          "department of transportation's hydraulics manual for ungauged sites.")
    _p(d, "4.4 Capacity of alternatives", bold=True)
    _p(d, "The capacity of a culvert or bridge alternative is the largest peak flow it passes before the road "
          "overtops, from the Roads Division's hydraulic model of the crossing with the surveyed channel and the road "
          "profile.")
    _p(d, "4.5 Selection", bold=True)
    _p(d, "Of the alternatives whose capacity is at least the design flow, the Roads Division recommends the one of "
          "least construction cost. Where none passes, the alternatives are redesigned before a recommendation is "
          "made.")
    _p(d, "4.6 Design flow memorandum", bold=True)
    _p(d, "The design flow memorandum filed with the state floodplain review states the design flow, how it was "
          "estimated from the records, the alternative recommended and the table of annual peak flows on which the "
          "estimate rests, as the reviewer is to re-run it.")
    _p(d, "4.7 Review", bold=True)
    _p(d, "The Roads Division reviews this section every five years with the Planning Department.")
    _meta(d, "Tamsett County Roads Division", dt.datetime(2017, 3, 16, 9, 40), "Drainage Standard Section 4")
    d.save(path)


def write_options(path):
    d = _doc()
    _p(d, "Tamsett County Roads Division", bold=True, size=9)
    _p(d, "Kinnard Road over Ollery Creek: culvert replacement alternatives", bold=True, size=14)
    _p(d, "Project RD-2026-07. Prepared %s for the design flow memorandum and the capital programme." % "2 December 2025",
       italic=True, size=9)
    _p(d, "The existing crossing is a pair of 8 ft corrugated metal pipe arches installed in 1958 and extended in 1979. "
          "The 2024 inspection rated both barrels poor (section loss at the invert, the downstream apron "
          "undermined). Kinnard Road is a two-lane collector with a low point 3.1 ft above the barrel crowns at the "
          "crossing. The drainage area at the crossing is %.1f square miles; the county's stream gauge on Ollery "
          "Creek is 250 ft downstream of the road." % K.AREA_SQMI)
    _p(d, "Three precast box culvert alternatives were modelled with the surveyed channel (2023) and the road "
          "profile. Capacity is the largest peak flow each passes before the road overtops (Drainage Standard 4.4).")
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for i, h in enumerate(["Alternative", "Barrels", "Capacity (cfs)", "Construction cost (USD)"]):
        t.rows[0].cells[i].text = h
    for a, desc, cap, cost in K.CULVERTS:
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text, row[3].text = a, desc, "{:,}".format(cap), "{:,}".format(cost)
    _p(d, "")
    _p(d, "All three alternatives keep the road profile, fit the existing right of way and are built in one summer "
          "season with a temporary crossing on the upstream side. Alternative C needs a wider headwall and a "
          "longer wingwall on the south bank. Costs are 2025 dollars and include the temporary crossing and "
          "stream restoration.")
    _meta(d, "Lisa Horne", dt.datetime(2025, 12, 2, 15, 10), "Kinnard Road culvert alternatives")
    d.save(path)


def write_inspection(path):
    d = _doc()
    _p(d, "Culvert inspection report", bold=True, size=14)
    _p(d, "Structure 340-018, Kinnard Road over Ollery Creek. Inspected 23 April 2024.", italic=True, size=9)
    for line in ("Barrels: two 8 ft corrugated metal pipe arches, 1958, extended 1979. Invert section loss of 30 to 45 "
                 "per cent over the downstream 40 ft of both barrels; perforations at two seams in the north barrel.",
                 "Headwalls: cracking at the upstream headwall's north wing; spalling at the downstream headwall.",
                 "Channel: scour hole 4.5 ft deep below the downstream apron, which is undermined for 6 ft. Debris "
                 "against the upstream inlet (two root wads) removed by the maintenance crew on 2 May 2024.",
                 "Roadway: pavement settlement of 1.5 in over the north barrel; guardrail sound.",
                 "Rating: barrels 3 (poor), headwalls 4 (fair), channel 3 (poor). Recommendation: replace the "
                 "structure within three years; monitor the apron monthly until then."):
        _p(d, line)
    _meta(d, "Tamsett County Roads Division", dt.datetime(2024, 4, 30, 11, 25), "Culvert inspection 340-018")
    d.save(path)


def write_docs(out, w=None):
    write_standard(os.path.join(out, K.FILES["standard"]))
    write_options(os.path.join(out, K.FILES["options"]))
    write_inspection(os.path.join(out, K.FILES["inspection"]))
