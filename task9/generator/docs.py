"""task9: the fab's own paperwork and the side records. The ramp plan of record is a Word document exported by
LibreOffice Writer through the house writer; the registers and the data sheet pass through the house workbook writer
with their owners' stamps; the cost inputs are controlling's YAML; the shift notes are the floor's own text; three side
records (the cleanroom's bay environment, the probe cards' touchdowns, the scanners' overlay) are kept by systems the
yield team pulls by habit."""
import datetime as dt
import math

import numpy as np
import openpyxl
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P
import world as W
from pack import F, head, save_xlsx, ts, write_csv

CET = dt.timezone(dt.timedelta(hours=1))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.6, leading=16.0, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.2,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.8, leading=10.2, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.3, leading=10.1)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def ramp_plan(path):
    body, h1, h2, small, cell = _styles()
    mm = 2.83
    story = [Paragraph("VR90 production ramp: Q1 2027 plan of record", h1),
             _grid([["Document", "OPS-PoR-VR90-02"], ["Owner", "Isabelle Hamann, Operations Planning, Fab 2"],
                    ["Issued", "30 October 2026"], ["Status", "filed for the VR90 ramp readiness review of 24 November 2026"],
                    ["Distribution", "Fab 2 operations, yield engineering, module engineering, facilities, controlling"]],
                   [40 * mm, 124 * mm], cell), Spacer(1, 6)]
    secs = [
        ("1. Commitment", [
            "Varnholt has committed 412,000 good VR90 units (sorted, assembled and final-tested) to the radar module "
            "customer for delivery in weeks 1 to 13 of 2027 under the 2027 supply agreement. The quarter's units come from "
            "VR90 wafers sorted in Q1 2027."]),
        ("2. Starts", [
            "VR90 production starts at 12 lots of 25 wafers a week from 9 November 2026, so that the first lots reach "
            "sort in the first week of January. Operations will set the quarter's wafer starts from the sort yield agreed "
            "at the ramp readiness review; until then the 12 lots a week stand."]),
        ("3. Operating conditions for the quarter", [
            [["Area", "Condition for VR90's Q1 2027 wafers"],
             ["Lithography, SC-1 to SC-3", "VR90 reticle set RV90 on SC-1 and SC-3 for the critical layers (ECN-2026-0487), SC-2 for the others; overlay control as VX40."],
             ["Implant, IM-1 to IM-3", "VR90 wells and LDD on the VX40 implant recipes; IM-2 with the upgraded source head (ECN-2026-0315)."],
             ["Pre-gate clean, WB-1 and WB-2", "tank T3 on the chemical life of ECN-2026-0417 (a spike every 10 lots, drain and fill every 24 hours), as today; the saving is in the 2027 chemicals budget. Each bench is planned at 31 lots a day with VR90 and the Q1 product mix."],
             ["Gate oxidation, FN-04 and FN-05", "VR90 on the VX40 gate oxide recipe with the O2 ramp of ECN-2026-0367; no change."],
             ["ILD0 deposition, DP1 to DP3", "DP2B on SH-300-C since its replacement of 6 April 2026, the other five chambers on SH-300-B; SH-300-C is fitted at each chamber's next replacement (ECN-2026-0388), and none falls due before the end of Q1 2027; no hardware change planned."],
             ["Oxide slurry loop SDS-OX1", "P-02A on the EP-114 setpoint of 38 Hz, as it runs today; the saving is in the 2027 energy budget."],
             ["ILD0 CMP, CM1 to CM4", "CM3's ILD0 recipes return to the fleet standard R7 under ECN-2026-0466 on 23 November 2026, before the first VR90 lot reaches ILD0 CMP; VR90's ILD0-VR recipe is qualified on CM1 and CM3 only, and VR90 is dispatched between them by the bay rules used today."],
             ["Contact etch", "VR90 runs CT-DEEP-07 on ET1B and ET3A only, the two chambers qualified for it (ECN-2026-0431), where it will be about 21 per cent of each chamber's wafers; wet cleans at the fleet standard of 2,400 wafers."],
             ["Metallisation and passivation", "as VX40; passivation nitride per ECN-2026-0452."],
             ["Inspection and metrology", "inline scans and ILD0 thickness on the VX40 sampling plan; VR90 maps added to the KL-3 and TH-1 recipe sets."],
             ["Probe, PR-1 and PR-2", "two new VR90 probe cards, PC-VR-01 and PC-VR-02, online clean every 400 touchdowns (ECN-2026-0459)."],
             ["Sort", "VR90-S program r1; the design centre's characterisation of VR90-T puts design-limited fallout (parametric, RF trim and memory) at 1.9 per cent of die."]]]),
        ("4. Back end", [
            "Assembly yield 99.2 per cent and final test yield 98.1 per cent of good die, from schedule 3 of the OSAT "
            "agreement. Gross die per wafer: 184 (product data sheet)."]),
        ("5. Open item for the review", [
            "The VR90 sort yield to plan for Q1 2027, and with it the quarter's wafer starts."]),
    ]
    for hd, paras in secs:
        story.append(Paragraph(hd, h2))
        for p in paras:
            if isinstance(p, list):
                story.append(_grid(p, [46 * mm, 118 * mm], cell))
            else:
                story.append(Paragraph(p, body))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Rev 02 replaces rev 01 of 9 October 2026 (starts moved from 2 to 9 November; contact-etch "
                           "chamber assignment added).", small))
    O.build(path, story, title="VR90 production ramp: Q1 2027 plan of record", author=P.PEOPLE["plan"],
            subject="VR90 ramp Q1 2027", footer="OPS-PoR-VR90-02 | Varnholt Halbleiter GmbH, Fab 2 | internal",
            created=dt.datetime(2026, 10, 9, 9, 14, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            modified=dt.datetime(2026, 10, 30, 16, 41, tzinfo=CET), font="Liberation Sans")


def ecn_register(path):
    rows = [
        ["ECN-2026-0302", "SC-2 reticle pellicle second source", "Litho", "K. Moll", "2026-01-08", "2026-01-21", "2026-02-02", "closed", "pellicle frame supplier B qualified on 4 layers"],
        ["ECN-2026-0306", "KL-3 inspection recipe for VP12 M1", "Metrology", "K. Trubin", "2026-01-12", "2026-01-19", "2026-01-26", "closed", "new defect classes for M1 bridging on VP12"],
        ["ECN-2026-0315", "IM-2 source head upgrade", "Implant", "T. Brandl", "2026-01-15", "2026-02-03", "2026-02-10", "closed", "beam current stability; dose matching to IM-1 within 0.5 %"],
        ["ECN-2026-0322", "WB-1 and WB-2 DI rinse resistivity alarm", "Wet", "H. Siering", "2026-01-20", "2026-01-28", "2026-02-02", "closed", "alarm at 17.5 MOhm cm (was 17.0); no recipe change"],
        ["ECN-2026-0326", "MES release 9.1", "Automation", "L. Roskoth", "2026-01-26", "2026-02-17", "2026-03-02", "closed", "MES 8.6 to 9.1 at the cut-over of 28 February to 2 March; lot IDs written without the period after the product prefix from the cut-over"],
        ["ECN-2026-0329", "DP1 chamber A seasoning after NF3 clean", "Thin films", "A. Dörr", "2026-01-29", "2026-02-11", "2026-02-16", "closed", "seasoning 25 to 20 dummies, particle adders within limit"],
        ["ECN-2026-0341", "VX40-S sort program r15", "Test", "N. Kreutz", "2026-02-02", "2026-02-12", "2026-02-16", "closed", "retention pattern update, test time -3 %"],
        ["ECN-2026-0356", "W-CMP P1 pad change IC1000 to IC1010", "CMP", "M. Hertrampf", "2026-02-18", "2026-03-04", "2026-03-09", "closed", "pad life +20 %"],
        ["ECN-2026-0362", "CM2 pad break-in on IC1010", "CMP", "M. Hertrampf", "2026-02-25", "2026-03-06", "2026-03-10", "closed", "break-in 6 min to 4 min; removal rate settles within the first qual"],
        ["ECN-2026-0367", "FN-05 gate oxide O2 ramp", "Diffusion", "P. Wendt", "2026-03-02", "2026-03-11", "2026-03-16", "closed", "thickness range on boat ends"],
        ["ECN-2026-0371", "ET2 endpoint on CO 483 nm", "Etch", "D. Lindau", "2026-03-03", "2026-03-18", "2026-03-23", "closed", "OES endpoint for CT-STD-11 on ET2 only"],
        ["ECN-2026-0374", "FN-03 boat change interval", "Diffusion", "P. Wendt", "2026-03-04", "2026-03-20", "2026-03-23", "closed", "quartz boat change every 450 runs (was 500)"],
        ["ECN-2026-0388", "PMD showerhead SH-300-C qualified for DP fleet", "Thin films", "A. Dörr", "2026-03-05", "2026-03-26", "2026-03-26", "closed", "SH-300-C replaces SH-300-B as the qualified spare at each chamber's next replacement (longer faceplate life); 5-site thickness and particle qual pass"],
        ["ECN-2026-0395", "STI ceria slurry second source", "CMP", "M. Hertrampf", "2026-03-19", "2026-04-08", "2026-04-20", "closed", "SDS-CE1 supplier B, dishing within spec"],
        ["ECN-2026-0398", "TR-1 resist pump replacement", "Litho", "K. Moll", "2026-03-24", "", "", "withdrawn", "vendor part not released; to be raised again when it is"],
        ["ECN-2026-0402", "M1 etch hardmask TiN thickness", "Etch", "D. Lindau", "2026-04-02", "2026-04-15", "2026-04-27", "closed", "line CD bias"],
        ["ECN-2026-0409", "SC-1 lens heating model update", "Litho", "K. Moll", "2026-04-06", "2026-04-17", "2026-04-20", "closed", "lens heating correction for the dense contact layer"],
        ["ECN-2026-0411", "VP12 trim limits per customer PCN 26-07", "Test", "N. Kreutz", "2026-04-20", "2026-04-29", "2026-05-04", "closed", "VP12-S r10"],
        ["ECN-2026-0417", "PGC T3 chemical life extension", "Wet", "H. Siering", "2026-05-18", "2026-06-09", "2026-07-01", "closed", "T3 spike every 10 lots (was 6), drain and fill every 24 h (was 12 h); chemicals saving EUR 214k a year; qualified on three lots, GOX integrity e-test pass"],
        ["ECN-2026-0424", "IM-3 source life", "Implant", "T. Brandl", "2026-05-21", "2026-06-01", "2026-06-08", "closed", "source change at 600 h (was 500 h)"],
        ["ECN-2026-0431", "VR90 CT-DEEP-07 release on ET1B and ET3A", "Etch", "D. Lindau", "2026-05-25", "2026-06-12", "2026-06-15", "closed", "deep contact etch for VR90 and VR90-T on the two qualified chambers"],
        ["ECN-2026-0444", "TH-2 recipe backup to the host", "Metrology", "K. Trubin", "2026-06-15", "2026-06-24", "2026-06-29", "closed", "nightly recipe backup after the February restore"],
        ["ECN-2026-0446", "IM-2 tilt angle for VP12 LDD", "Implant", "T. Brandl", "2026-06-19", "", "", "rejected", "device engineering review: threshold shift outside the PCN limits"],
        ["ECN-2026-0452", "Passivation nitride +40 nm", "Thin films", "A. Dörr", "2026-07-06", "2026-07-22", "2026-08-03", "closed", "package stress margin, automotive grade"],
        ["ECN-2026-0455", "EM-2 RF match network", "Etch", "D. Lindau", "2026-07-13", "2026-07-24", "2026-08-03", "closed", "match network replaced after repeated faults"],
        ["ECN-2026-0459", "Probe card online clean interval", "Test", "N. Kreutz", "2026-08-10", "2026-08-19", "2026-08-24", "closed", "online clean every 400 touchdowns (was 600)"],
        ["ECN-2026-0462", "CDA point-of-use filters on the litho tracks", "Facilities", "S. Sorgatz", "2026-08-24", "2026-09-02", "2026-09-07", "closed", "0.003 um filters on TR-1 and TR-2"],
        ["ECN-2026-0464", "IM-1 dose monitor frequency", "Implant", "T. Brandl", "2026-09-14", "2026-09-23", "2026-09-28", "closed", "one monitor a day per species (was one a shift)"],
        ["ECN-2026-0466", "ILD0 CMP recipe harmonisation", "CMP", "M. Hertrampf", "2026-09-28", "2026-10-20", "2026-11-23", "approved", "CM3 ILD0 recipes back to the fleet standard R7 (zone 5 2.90 psi) so CM1 to CM4 run one recipe set for VR90"],
        ["ECN-2026-0473", "VR90-S sort program r1", "Test", "N. Kreutz", "2026-10-05", "2026-10-21", "2026-12-14", "approved", "VR90 production sort"],
        ["ECN-2026-0480", "VR90 dispatch at ILD0 CMP", "Operations", "I. Hamann", "2026-10-12", "2026-10-26", "2026-11-09", "approved", "VR90 at ILD0 CMP on CM1 and CM3, the two polishers ILD0-VR is qualified on, dispatched by the bay rules used for VX40 and VP12"],
        ["ECN-2026-0484", "AMHS stocker 4 controller replacement", "Automation", "L. Roskoth", "2026-10-19", "", "", "in review", "repeated slow handling in bay 4; vendor quote received"],
        ["ECN-2026-0487", "VR90 reticle set RV90", "Litho", "K. Moll", "2026-10-22", "2026-10-28", "2026-11-09", "approved", "RV90 on SC-1 and SC-3 for the critical layers, SC-2 for the others"],
    ]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ECN 2026"
    head(ws, ["ecn", "title", "area", "owner", "raised", "approved", "effective", "status", "summary"],
         [14, 44, 11, 13, 11, 11, 11, 9, 90])
    for r in rows:
        ws.append(r)
    save_xlsx(wb, path, "Change Control", "Change Control", "2026-01-08T08:00:00Z", "2026-11-04T08:40:12Z")


def product_sheet(path, fab):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"
    head(ws, ["product", "description", "die_w_mm", "die_h_mm", "die_area_mm2", "gross_die_per_wafer", "gate_oxide_area_mm2",
              "ild0_target_nm", "ild0_cmp_recipe", "ild0_p1_time_s", "ct_etch_recipe", "ct_rf_on_s", "sort_program",
              "design_limited_yield", "status"],
         [9, 30, 9, 9, 12, 12, 12, 10, 12, 10, 13, 10, 11, 12, 22])
    gate = {"VX40": 31.4, "VP12": 15.1, "VR90": 53.4}
    rows = []
    for name in ("VX40", "VP12", "VR90"):
        p, g = P.PRODUCTS[name], fab.grids[name]
        rows.append([name, p["kind"], p["w"], p["h"], round(p["w"] * p["h"], 2), g.n, gate[name], 605,
                     {"VX40": "ILD0-VX", "VP12": "ILD0-VP", "VR90": "ILD0-VR"}[name], p["polish_s"], p["recipe"], p["rf_s"],
                     {"VX40": "VX40-S", "VP12": "VP12-S", "VR90": "VR90-S"}[name], p["design"],
                     "production" if name != "VR90" else "ramp from 9 Nov 2026"])
    for r in rows:
        ws.append(r)
    ws.append([])
    ws.append(["VR90-T", "VR90 front-end test vehicle (no production sort; characterised at the design centre)", 18.2, 17.6,
               320.32, "", "", 605, "ILD0-VR", 76.0, "CT-DEEP-07", 186.0, "", "", "engineering"])
    save_xlsx(wb, path, P.PEOPLE["yield"], "Product Engineering", "2025-09-15T10:02:00Z", "2026-10-21T08:47:36Z")


def costs(path):
    text = """# Fab 2 cost inputs for 2027 planning (Controlling, G. Scheibe), EUR unless stated
# revised 2026-10-28; replaces the 2026 sheet of 2025-10-14
die_value_per_good_die:
  VX40: 9.80
  VP12: 3.10
  VR90: 41.00
wafer_start_cost:
  VX40: 1850
  VP12: 1420
  VR90: 3900
energy:
  electricity_eur_per_kwh: 0.19
  natural_gas_eur_per_mwh: 41.0
  run_hours_per_year: 8760
  drives_kw:                       # 2026 energy audit, measured at the stated setpoint
    sds_ox1_p02a_51_5_hz: 78.0
    sds_ox1_p02a_38_hz: 32.0
    sds_w1_p07a_50_hz: 41.0
    sds_w1_p07a_41_hz: 24.0
    upw_polish_pumps: 96.0
    pcw_loop_1_pumps: 110.0
    acid_exhaust_fans: 240.0
chemicals:
  hcl_37_per_l: 4.20
  hf_49_per_l: 6.80
  h2so4_96_per_l: 1.10
  pgc_t3_wb1_wb2_per_year:         # tank T3 on both benches
    spike_6_lots_drain_12_h: 486000
    spike_10_lots_drain_24_h: 272000
  ild0_slurry_per_l: 7.40
spares:
  dp_showerhead_sh300b: 38400
  dp_showerhead_sh300c: 41900
  cmp_p1_pad: 1250
  cmp_pou_filter: 410
  cmp_retaining_ring: 2350
  ct_etch_liner_kit: 1900
  probe_card_rebuild: 14500
ct_etch_wet_clean:
  parts_and_labour: 2900
  chamber_downtime_h: 6
dp_showerhead_change:
  install_downtime_h: 16
tool_downtime_per_h:
  cmp: 1900
  cvd: 2400
  etch: 2600
  wet_bench: 1700
labour_per_h:
  technician: 62
  engineer: 95
"""
    open(path, "w", encoding="utf-8", newline="\n").write(text)


def shift_notes(path, fab, events):
    """The FT2 shift book: each crew's lead writes up a few lines a shift from what the floor saw (re-probes, holds,
    PMs and downs, bench controller restarts and alarms) and from the areas that keep no log of their own here."""
    rng = np.random.default_rng(P.SEED + 120)
    lo, hi = dt.datetime(2026, 1, 2), dt.datetime(2026, 11, 4)
    fixed = {
        dt.datetime(2026, 1, 19, 11, 20): "CMP: endpoint threshold change on all four ILD0 polishers done by M. Hertrampf, no alarms.",
        dt.datetime(2026, 3, 2, 6, 40): "MES 9.1 live after the weekend cut-over; lot IDs are written without the period from today.",
        dt.datetime(2026, 3, 18, 6, 50): "Facilities: SDS-OX1 controller still being replaced, loop running on local panel, slurry flow normal.",
        dt.datetime(2026, 4, 6, 15, 30): "CVD: DP2 chamber B showerhead change finished, seasoned and released. Particles ok.",
        dt.datetime(2026, 5, 11, 9, 40): "CMP: CM3 ILD0 recipes to R8 (zone 5), first lots out, SPC normal.",
        dt.datetime(2026, 6, 2, 10, 5): "Facilities changed the oxide slurry pump speed this morning (energy programme), loop pressure checked ok.",
        dt.datetime(2026, 7, 1, 6, 25): "Wet: T3 chemical life per ECN-0417 active on both benches from this morning's change.",
        dt.datetime(2026, 8, 10, 14, 40): "Facilities: SDS-OX1 VFD fault, standby pump running. CMP not affected, no slurry alarms.",
        dt.datetime(2026, 8, 24, 17, 0): "Facilities: SDS-OX1 back on the main pump.",
        dt.datetime(2026, 8, 18, 14, 35): "Lab took extra bath samples from WB-1/WB-2 T3 for the yield investigation, more to follow.",
    }
    pick = lambda xs: xs[int(rng.integers(0, len(xs)))]
    plural = lambda n: "" if n == 1 else "s"

    def say(e):
        k = e["kind"]
        if k == "reprobe":
            n = e["n"]
            return pick(["%s contact alarms on %s, card %s cleaned, %d wafer%s re-probed." % (e["tool"], e["lot"], e["card"], n, plural(n)),
                         "%s cleaned on %s after contact fails, re-probed %d wafer%s of %s." % (e["card"], e["tool"], n, plural(n), e["lot"]),
                         "%s: %d wafer%s of %s re-probed after a card clean." % (e["tool"], n, plural(n), e["lot"])])
        if k == "hold":
            lot, step = e["lot"], e["step"]
            return {"METRO-OOC": pick(["%s on hold at %s, metrology out of control, engineering informed." % (lot, step),
                                       "%s held at %s for metrology." % (lot, step)]),
                    "TOOL-DOWN": "%s waiting at %s with the tool down, put on hold." % (lot, step),
                    "ENG-HOLD": pick(["%s on engineering hold at %s." % (lot, step), "%s held at %s for engineering." % (lot, step)]),
                    "QA-REVIEW": "%s to QA review at %s." % (lot, step),
                    "CUST-HOLD": "%s on customer hold at %s (planning)." % (lot, step)}[e["code"]]
        if k == "restart":
            if e["after"] == "BATCH" and e["lot"]:
                return pick(["%s controller restart after watchdog, %s in T3 at the time, batch completed." % (e["tool"], e["lot"]),
                             "%s controller hung and restarted (watchdog) during %s, lot finished normally." % (e["tool"], e["lot"])])
            return "%s controller restart after watchdog, no lot in the tank." % e["tool"]
        if k == "alarm":
            what = {"T3_TEMP_HI": "T3 temperature high", "T3_LEVEL_LO": "T3 level low", "RINSE_RES_LO": "rinse resistivity low",
                    "EXH_FLOW_LO": "exhaust flow low"}[e["code"]]
            return pick(["%s %s alarm, cleared." % (e["tool"], what), "%s: %s alarm, checked and cleared." % (e["tool"], what)])
        t, ty, desc = e["tool"], e["type"], e["desc"]
        if ty == "POU_FILTER":
            return pick(["%s POU filter changed." % t, "%s slurry POU filter replaced, flow ok." % t])
        if ty == "PAD_CHANGE":
            return pick(["%s pad change, qual wafers ok." % t, "%s P1 pad changed, removal rate in spec." % t])
        if ty == "RING_CHANGE":
            return "%s retaining ring changed (%s)." % (t, desc.split("RR-300 ")[-1])
        if ty == "CHAMBER_CLEAN":
            return pick(["%s chamber %s clean, particles ok." % (t, desc.split()[1]), "%s%s clean and season done." % (t, desc.split()[1])])
        if ty == "WET_CLEAN":
            return pick(["%s chamber %s wet clean done, seasoning ok." % (t, desc.split()[1]),
                         "%s%s back from wet clean." % (t, desc.split()[1])])
        if ty == "PM_MONTHLY":
            return pick(["%s monthly PM done." % t, "%s monthly PM, T3 heater calibrated." % t])
        if ty == "UNSCHED_DOWN":
            why, _, rest = desc.partition(", up after ")
            h = max(1, int(round(float(rest.split()[0])))) if rest else 1
            return pick(["%s down: %s, back after about %d h." % (t, why, h), "%s down for %s, about %d h." % (t, why, h)])
        return None

    ret = lambda: "R%s-%02d" % (pick(["VX4", "VP1", "CT0", "M10"]), int(rng.integers(1, 30)))
    other = [lambda: pick(["SC-1 lens heating alarm cleared, no lots affected.",
                           "SC-1 lens heating alarm during %s exposure, cleared by litho on call." % pick(["CT", "M1", "poly"])]),
             lambda: "SC-2 reticle %s cleaned after a particle hit, requalified." % ret(),
             lambda: "SC-3 stage calibration overran by %d min, lots held at litho." % int(rng.integers(20, 75)),
             lambda: pick(["FN-03 boat change.", "FN-04 boat changed, monitor wafers ok.",
                           "FN-0%d monitor run out of range, re-run ok." % int(rng.integers(1, 6))]),
             lambda: pick(["IM-3 source change, %d min to beam." % int(rng.integers(90, 240)), "IM-2 beam retuned after source change.",
                           "IM-1 dose monitor re-measured, in spec."]),
             lambda: "AMHS stocker 4 slow, %d minutes of manual moves." % int(rng.integers(20, 95)),
             lambda: pick(["TH-2 recipe file restored from backup.", "TH-1 stage error, %d wafers re-measured." % int(rng.integers(2, 9))]),
             lambda: "EM-2 RF match fault, chamber down %d h." % int(rng.integers(2, 7)),
             lambda: "TR-%d coat cup clean." % int(rng.integers(1, 3)),
             lambda: "Sorter SO-1 vacuum fault on port %d, cleared." % int(rng.integers(1, 5)),
             lambda: "%s lots waiting for %s over the shift change, cleared within the hour." % (
                 pick(["Two", "Three", "Four"]), pick(["litho", "implant", "the furnaces", "CMP"]))]
    # re-probes are written up per lot, not per wafer
    rp = {}
    for e in events:
        if e["kind"] == "reprobe":
            key = (e["t"].date(), e["tool"], e["lot"])
            if key not in rp:
                rp[key] = dict(e, n=0)
            rp[key]["n"] += 1
    evs = [e for e in events if e["kind"] != "reprobe"] + list(rp.values())
    evs = [e for e in evs if lo <= e["t"] < hi and not (e["kind"] == "pm" and e["type"] == "PART_REPLACE")]

    def shift_of(t):
        h = t.hour
        if 6 <= h < 14:
            return t.date(), 0
        if 14 <= h < 22:
            return t.date(), 1
        return (t - dt.timedelta(hours=8)).date(), 2

    by_shift = {}
    for e in evs:
        by_shift.setdefault(shift_of(e["t"]), []).append(e)
    for t, s in fixed.items():
        by_shift.setdefault(shift_of(t), [])
    must = lambda e: e["kind"] == "restart" or (e["kind"] == "pm" and e["type"] == "UNSCHED_DOWN" and "up after" in e["desc"]
                                                 and float(e["desc"].split("up after ")[1].split()[0]) >= 2.0)
    lines = []
    day = lo.date()
    while day < hi.date():
        for s in range(3):
            got = sorted(by_shift.get((day, s), []), key=lambda e: e["t"])
            chosen = [e for e in got if must(e)]
            rest = [e for e in got if not must(e)]
            for e in rest:
                p = {"hold": 0.18, "reprobe": 0.45, "alarm": 0.5, "pm": 0.4}[e["kind"]]
                if rng.random() < p:
                    chosen.append(e)
            chosen = sorted(chosen, key=lambda e: e["t"])[:3]
            for e in chosen:
                text = say(e)
                if text:
                    lines.append((e["t"] + dt.timedelta(minutes=float(rng.uniform(5, 50))), text))
            if rng.random() < 0.16:
                start = dt.datetime.combine(day, dt.time(6)) + dt.timedelta(hours=8 * s)
                lines.append((start + dt.timedelta(hours=float(rng.uniform(0.5, 7.5))), pick(other)()))
        day += dt.timedelta(days=1)
    lines += list(fixed.items())
    lines.sort()
    leads = P.SHIFT_LEADS
    initials = lambda name: "".join(w[0] for w in name.replace(".", " ").split())

    def lead(t):
        d, s = shift_of(t)
        m = (d - dt.date(2026, 1, 1)).days % 8
        for i in range(4):
            if (m - 2 * i) % 8 in (2 * s, 2 * s + 1):
                return initials(leads[i])
        return "--"
    out = ["Fab 2 shift handover log (FT2 area, exported from the shift book)", ""]
    for t, s in lines:
        shift = ("early", "late", "night")[shift_of(t)[1]]
        out.append("%s  %-5s  %-2s  %s" % (t.strftime("%Y-%m-%d %H:%M"), shift, lead(t), s))
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")


def environment(path):
    rng = np.random.default_rng(P.SEED + 121)
    rows = []
    t = dt.datetime(2026, 1, 1)
    bays = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
    base = {b: rng.uniform(40, 90) for b in bays}
    while t < dt.datetime(2026, 11, 1):
        for b in bays:
            rows.append([t.strftime("%Y-%m-%d %H:00"), b, "%.2f" % (21.0 + rng.normal(0, 0.08)), "%.1f" % (44.0 + rng.normal(0, 0.9)),
                         int(rng.poisson(base[b])), "%.1f" % (12.0 + rng.normal(0, 0.4))])
        t += dt.timedelta(hours=2)
    return write_csv(path, ["TIMESTAMP", "BAY", "ROOM_T_DEGC", "ROOM_RH_PCT", "PART_GE_0P3UM_FT3", "DP_PA"], rows)


def probe_cards(path):
    rng = np.random.default_rng(P.SEED + 122)
    rows = []
    t = dt.date(2026, 1, 1)
    while t < dt.date(2026, 11, 1):
        for card in ("PC-VX-07", "PC-VX-11", "PC-VP-04", "PC-VP-09"):
            td = int(rng.normal(5200, 600))
            rows.append([t.isoformat(), card, td, int(td / (600 if t < dt.date(2026, 8, 24) else 400)),
                         "%.2f" % rng.normal(1.8, 0.12), "%.1f" % rng.normal(27.0, 1.5)])
        t += dt.timedelta(days=1)
    return write_csv(path, ["date", "probe_card", "touchdowns", "online_cleans", "avg_contact_ohm", "tip_length_um_left"], rows)


def overlay(path, fab):
    rng = np.random.default_rng(P.SEED + 123)
    rows = []
    for L in fab.lots:
        for step in ("POLY-LITHO", "CT-LITHO", "M1-LITHO"):
            if step not in L.times:
                continue
            rows.append([L.lid, L.product, step, ("SC-1", "SC-2", "SC-3")[int(rng.integers(0, 3))], ts(L.times[step]),
                         "%.1f" % rng.normal(0, 1.2), "%.1f" % rng.normal(0, 1.2), "%.1f" % abs(rng.normal(6.5, 0.8)),
                         "%.1f" % abs(rng.normal(6.8, 0.8))])
    return write_csv(path, ["lot_id", "product", "layer", "scanner", "exposed", "mean_x_nm", "mean_y_nm", "m3s_x_nm", "m3s_y_nm"], rows)
