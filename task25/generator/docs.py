"""The pack's documents, each in its issuer's genre: the compute committee's allocation rules for the H1 2027 round
(the governing document), the provider's service schedule for the Kaivola halls, and the provider's notice of planned
works for January to June 2027; plus the 2027 roadmap workbook. PDFs go through the house writer (officepdf), the
workbook through openpyxl and the house container writer."""
import datetime as dt
from zoneinfo import ZoneInfo

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf
import params as P
import postprocess
import world as W

HEL = ZoneInfo("Europe/Helsinki")
SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, spaceAfter=0, leading=10.0)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")


def p(t, st=BODY):
    return Paragraph(t, st)


def table(rows, widths_mm):
    return Table([[p(str(c), CELL) for c in r] for r in rows], colWidths=[w * 2.8346 for w in widths_mm])


def allocation_rules(path):
    story = [
        p("Saukko Labs Oy, Compute Committee", LH),
        p("Compute allocation rules, H1 2027 round", TITLE),
        p("CAR-2027-1, issued 2 November 2026 by the Compute Committee (chair: %s). Supersedes CAR-2026-2." % P.COMMITTEE_CHAIR, LH),
        Spacer(1, 6),
        p("1. Scope", H2),
        p("These rules govern the reservation of GPU blocks in halls A and B at %s's %s campus for runs that start "
          "between 1 January and 30 June 2027, and the committee's review of the 2026 runs against their benchmarks."
          % (P.PROVIDER, P.CAMPUS)),
        p("2. Blocks and windows", H2),
        p("A reservation holds a block of whole nodes in one hall. Its window runs from 00:00 UTC on the window's start "
          "date to 00:00 UTC on its end date, as listed in the H1 2027 roadmap. A block's run launches when its window "
          "opens, or, where the block's nodes are still held by an earlier reservation's run, when that run has "
          "finished and the nodes are handed back, whichever is later."),
        p("Nodes that no reservation holds run the research pool, which schedules its own jobs."),
        p("A block whose run finishes before its window ends runs backfill research jobs on its nodes until the window "
          "ends. If a run is still training when its window ends, its block is extended until the run finishes, and "
          "nothing else is booked on those nodes in the meantime."),
        p("3. When a run has finished", H2),
        p("A run finishes when the trainer's token count reaches the run's token budget. The trainer counts training "
          "tokens; padding positions in a packed sequence are not tokens and are not counted."),
        p("4. The committee's test", H2),
        p("A run is planned to finish inside its window when its expected finish falls at or before 00:00 UTC on the "
          "window's end date. The committee asks for each run's expected days from its window's start to its finish, "
          "and the range within which it will finish four times in five."),
        p("5. Provider works", H2),
        p("Works the provider has notified stop every job in the hall they affect for as long as they last; jobs "
          "resume from their last checkpoint when the hall is handed back."),
        p("6. The 2026 review", H2),
        p("For the review of 2026 the committee counts a run's GPU-days held as its allocated nodes, times eight GPUs a "
          "node, times the hours from its launch to its final checkpoint, divided by 24. A run still training at the "
          "end of the review period (00:00 UTC on 1 November 2026) counts to then. Every run launched in 2026 is in the "
          "review."),
        p("The GPU-days a run's benchmark implies are its training tokens divided by the benchmark's tokens per "
          "GPU-second for its configuration (model, sequence length, sequences per rank and hall), divided by 86,400."),
        Spacer(1, 8),
        p("Approved by the Compute Committee on 2 November 2026.", LH),
    ]
    officepdf.build(path, story, "Compute allocation rules, H1 2027 round", P.COMMITTEE_CHAIR,
                    "Reservation of GPU blocks for H1 2027", P.ORG,
                    dt.datetime(2026, 11, 2, 14, 5, tzinfo=HEL), dt.datetime(2026, 11, 2, 16, 41, 12, tzinfo=HEL),
                    producer="LibreOffice 24.8")


def service_schedule(path):
    rows = [["Hall", "GPU equipment", "Nodes", "Contracted IT capacity", "Cooling"],
            ["HALL-A", P.HALLS["A"]["gpu"], "512", "%s kW" % format(int(P.HALLS["A"]["contract_kw"]), ","),
             "CRAC units 1 to 8, chilled-water loop A"],
            ["HALL-B", P.HALLS["B"]["gpu"], "1,024", "%s kW" % format(int(P.HALLS["B"]["contract_kw"]), ","),
             "Rear-door heat exchangers, chilled-water loop B"]]
    story = [
        p("%s" % P.PROVIDER, LH),
        p("Service Schedule S-3: Kaivola campus halls A and B", TITLE),
        p("To the colocation agreement with %s, revision 4, 18 December 2025" % P.ORG, LH),
        Spacer(1, 6),
        p("1. Halls", H2),
        table(rows, [18, 34, 30, 32, 60]),
        Spacer(1, 6),
        p("2. Power and metering", H2),
        p("Each hall's IT load is metered at its IT distribution boards and reported as a five-minute average in kW. "
          "Meter readings, work orders and incident records are kept in Finnish local time. Collector outages leave "
          "gaps in the meter export; the provider does not backfill them."),
        p("3. Maintenance and works", H2),
        p("Routine inspections take place quarterly in each hall with at least 14 days' notice. Major works are "
          "notified at least 30 days ahead with their planned start and planned hours. A hall affected by works is "
          "handed back to the customer when the work order is closed."),
        p("4. Incidents", H2),
        p("Facility incidents affecting a hall are logged with their opening and closing times and a short summary, "
          "and shared with the customer's operations contact (%s)." % P.INFRA_LEAD),
    ]
    officepdf.build(path, story, "Service Schedule S-3, Kaivola halls A and B", P.PROVIDER_CONTACT,
                    "Colocation service schedule", P.PROVIDER,
                    dt.datetime(2025, 12, 18, 10, 12, tzinfo=HEL), dt.datetime(2025, 12, 18, 11, 3, 40, tzinfo=HEL),
                    producer="LibreOffice 24.2")


def works_notice(path):
    rows = [["Work order", "Hall", "Type", "Planned start", "Planned hours", "Work"]]
    for wid, hall, typ, start, hours, title in sorted(P.WORKS_2027, key=lambda w: w[3]):
        rows.append([wid, "HALL-%s" % hall, typ, start.strftime("%d.%m.%Y %H:%M"), "%.0f" % hours, title])
    story = [
        p("%s, Kaivola campus" % P.PROVIDER, LH),
        p("Notice of planned works, January to June 2027", TITLE),
        p("Issued 28 October 2026 to %s under Service Schedule S-3" % P.ORG, LH),
        Spacer(1, 6),
        p("The following works are planned in halls A and B in the first half of 2027. Start times are Finnish local "
          "time. Each hall is handed back when its work order is closed."),
        table(rows, [24, 18, 18, 30, 22, 66]),
        Spacer(1, 6),
        p("Questions: %s, customer operations." % P.PROVIDER_CONTACT, LH),
    ]
    officepdf.build(path, story, "Planned works, January to June 2027", P.PROVIDER_CONTACT,
                    "Notice of planned works H1 2027", P.PROVIDER,
                    dt.datetime(2026, 10, 28, 9, 30, tzinfo=HEL), dt.datetime(2026, 10, 28, 9, 58, 2, tzinfo=HEL),
                    producer="LibreOffice 24.2")


def roadmap_xlsx(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "H1 2027 runs"
    hdr = ["run_id", "purpose", "model", "hall", "nodes", "gpus", "seq_len", "seqs_per_rank", "data_mix", "packing",
           "window_start", "window_end", "token_budget", "block", "config"]
    ws.append(["Saukko Labs: H1 2027 pretraining roadmap, version 7 (%s)" % P.ROADMAP_DATE.strftime("%d %b %Y")])
    ws.append([])
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7F0")
    for (rid, model, hall, nodes, C, mix, rule, g, wst, wen, budget, purpose) in P.ROADMAP_2027:
        h, r0, r1 = P.BLOCKS_2027[rid]
        ws.append([rid, purpose, model, hall, nodes, nodes * P.GPUS_PER_NODE, C, g, mix, rule,
                   dt.date.fromisoformat(wst), dt.date.fromisoformat(wen), int(budget),
                   W.compress(W.block_nodes(h, r0, r1)), "configs/%s.yaml" % rid])
    for row in ws.iter_rows(min_row=4, max_row=3 + len(P.ROADMAP_2027)):
        row[10].number_format = "yyyy-mm-dd"
        row[11].number_format = "yyyy-mm-dd"
        row[12].number_format = "#,##0"
    widths = [20, 34, 7, 6, 7, 7, 8, 13, 13, 11, 12, 12, 19, 44, 30]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws["A1"].font = Font(bold=True, size=12)
    ws2 = wb.create_sheet("Changes")
    ws2.append(["Version", "Date", "Change"])
    ws2.append([6, dt.date(2026, 10, 21), "Windows and budgets agreed at the committee's 21 October meeting"])
    ws2.append([7, dt.date(2026, 11, 4), "kide-13b-v4 added in hall B from 29 March; kide-34b-16k moved to 15 March at 224 "
                "nodes and kide-120b-v1 set at 480; blocks booked with the provider's reservation desk"])
    for c in ("A", "B", "C"):
        ws2.column_dimensions[c].width = {"A": 9, "B": 12, "C": 90}[c]
    wb.save(path)
    postprocess.normalize_ooxml(path, P.INFRA_LEAD, P.INFRA_LEAD, "2026-10-14T08:21:00Z", "2026-11-04T15:46:31Z",
                                excel=True, company=P.ORG)


def energy_xlsx(path, df):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices 2026"
    ws.append(list(df.columns))
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in df.itertuples(index=False):
        ws.append(list(r))
    for i, w in enumerate([18, 9, 10, 15, 8, 15, 18]):
        ws.column_dimensions[chr(65 + i)].width = w
    wb.save(path)
    postprocess.normalize_ooxml(path, "Laskutus PV", P.INFRA_LEAD, "2026-02-05T07:02:00Z", "2026-11-03T12:10:44Z",
                                excel=True, company=P.PROVIDER)
