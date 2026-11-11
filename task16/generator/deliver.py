"""The golden deliverables: the scope workbook and the note that carries the recommendation."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Mm, Pt, RGBColor
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import golden as GD
import params as P
import postprocess

WORKBOOK = "peak_assistant_scope.xlsx"
NOTE = "peak_assistant_scope_memo.docx"
ORG = "Quellstein Paket GmbH"
AUTHOR = "Simon Pertl"
STAMPS = {WORKBOOK: ("2026-11-09T10:20:00Z", "2026-11-10T15:42:00Z"), NOTE: ("2026-11-10T16:05:00Z", "2026-11-10T16:58:00Z")}
FAM = P.FAM
BLUE, ORANGE, INK, MUTED = "2A78D6", "EB6834", "0B0B0B", "52514E"
HEAD = PatternFill("solid", fgColor="E9EEF5")
THIN = Side(style="thin", color="B8C2CC")


def _head(ws, row, labels, widths=None):
    for j, lab in enumerate(labels, start=1):
        c = ws.cell(row=row, column=j, value=lab)
        c.font = Font(bold=True); c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths, start=1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = Font(bold=True, size=13)
    if sub:
        ws["A2"] = sub; ws["A2"].font = Font(italic=True, color=MUTED)


def write_workbook(path, F):
    wb = openpyxl.Workbook()
    nm = F["families"]
    # ---- Scope
    ws = wb.active; ws.title = "Scope"
    _title(ws, "Peak season 2026: assistant-first reason families under KS-07 4.2",
           "Version 3 conversations 28 September to 1 November 2026 (seven days old at the 9 November cut), carried to the season plan of 16 November to 3 January")
    _head(ws, 4, ["Reason family", "Conversations in the record", "Resolved so far %", "Expected over the season %", "90% range, low", "90% range, high",
                  "Against 75%", "Offer first"], [34, 15, 13, 15, 12, 12, 11, 14])
    r = 5
    for k in sorted(FAM, key=lambda x: -F["expected"][x]):
        keep = k in F["keep"]
        row = [nm[k], sum(F["cell_n"][k].values()), F["achieved"][k], F["expected"][k], F["low"][k], F["high"][k],
               round(F["expected"][k] - F["line"], 1), "Assistant" if keep else "Adviser"]
        for j, v in enumerate(row, start=1):
            c = ws.cell(row=r, column=j, value=v)
            if j in (3, 4, 5, 6):
                c.number_format = "0.0"
            if j == 7:
                c.number_format = '+0.0;-0.0;0.0'
            if j == 2:
                c.number_format = "#,##0"
            if j == 8:
                c.font = Font(bold=True, color=BLUE if keep else ORANGE)
        r += 1
    tot = ["All ten families", F["conversations"], F["achieved_all"], F["expected_all"], F["low_all"], F["high_all"], "", ""]
    for j, v in enumerate(tot, start=1):
        c = ws.cell(row=r, column=j, value=v); c.font = Font(bold=True); c.border = Border(top=THIN)
        if j in (3, 4, 5, 6):
            c.number_format = "0.0"
        if j == 2:
            c.number_format = "#,##0"
    ws.cell(row=r + 2, column=1, value="Source: assistant, live chat, telephony and case exports of 9 November 2026; network daily service record; season plan of 6 November.").font = Font(size=9, color=MUTED)
    ws.cell(row=r + 3, column=1, value="The rule is applied to the expected rate (KS-07 4.2); the all-families row is shown for reference and is not a family.").font = Font(size=9, color=MUTED)
    ws.freeze_panes = "B5"
    # ---- Build-up
    b = wb.create_sheet("Build-up")
    _title(b, "From the linked contact record to the rate achieved", "Version 3 conversations that ended 28 September to 1 November")
    _head(b, 4, ["Step", "Figure", "Unit", "How it is read"], [52, 12, 14, 92])
    ch = F["by_channel"]
    rc = F["recon"]; tk = F["tick"]
    rows = [
        ("Conversations about a consignment", F["conversations"], "conversations", "assistant export, tracking number present, reason family from the intent"),
        ("... followed within 168 hours by another assistant conversation", ch["assistant"], "conversations", "same tracking number, later start"),
        ("... by a live chat session", ch["chat"], "conversations", "includes conversations the assistant handed over"),
        ("... by a telephone call that carries the tracking number", ch["phone"], "conversations", "first leg of inbound calls; callbacks are not contacts"),
        ("... by a written case in the resolution extract", ch["written"], "conversations", "web form and e-mail cases; cases advisers opened are not contacts"),
        ("Followed by any linked contact", F["linked_followed"], "conversations", ""),
        ("Resolution rate on the linked record alone", F["linked_rate"], "per cent", "what the four exports show as they stand"),
        ("Telephone follow-up calls that carry the tracking number", F["phone_keyed"], "calls", "each counted once, against the latest conversation it follows"),
        ("Telephone follow-up calls, with those that carry no number", F["phone_total"], "calls", "each keyed call weighted by the inverse of the share of consignment calls keyed in its queue, bypass running or not"),
        ("Share of telephone follow-ups with no tracking number", F["phone_unkeyed_share"], "per cent", ""),
        ("Written follow-up cases in the resolution extract", F["written_closed"], "cases", ""),
        ("Written follow-up cases still open at the cut", F["written_open"], "cases", "each closed follow-up case stands for the cases raised in its queue on its day and the days either side that the backlog report still counts open"),
        ("Resolution rate achieved, follow-ups restored", F["achieved_all"], "per cent", "a conversation whose only follow-up is a keyed call or a closed case stands for those the record cannot see"),
        ("Check: inbound calls after cleaning, against telephony's weekly summary", "%s = %s" % ("{:,}".format(rc["calls"]), "{:,}".format(rc["acd_calls"])), "calls", "no week and queue differs"),
        ("Check: customer cases in the extract plus open in the backlog report", "%s + %s = %s" % ("{:,}".format(rc["cases_closed"]), "{:,}".format(rc["cases_open_now"]), "{:,}".format(rc["cases_opened"])), "cases", "equals the cases opened in the weekly flow"),
        ("Check: unkeyed calls that follow an assistant conversation, since 28 September", "%s by capture, %s by the advisers' tick" % ("{:,}".format(tk["unkeyed_follow_capture"]), "{:,}".format(tk["unkeyed_follow_tick"])), "calls",
         "the tick is set on %s per cent of keyed follow-ups and %s per cent of other keyed calls" % (tk["hit_rate"], tk["false_rate"])),
    ]
    for i, row in enumerate(rows, start=5):
        for j, v in enumerate(row, start=1):
            c = b.cell(row=i, column=j, value=v); c.alignment = Alignment(wrap_text=True, vertical="top")
            if j == 2 and isinstance(v, int):
                c.number_format = "#,##0"
            if j == 2 and isinstance(v, float):
                c.number_format = "0.0"
    b.freeze_panes = "A5"
    # ---- Season mix
    m = wb.create_sheet("Season mix")
    _title(m, "The conversations the season plan generates, by how the parcel runs",
           "Plan parcels of 16 November to 3 January at the planned service levels; contact rates from parcels due 28 September to 1 November")
    _head(m, 4, ["Delivery outcome", "Plan parcels, season", "Assistant conversations per 1,000 parcels, no alert", "Delay alert in the season",
                 "Conversations expected, season", "Share of season conversations %", "Share in the weeks observed %"], [26, 16, 22, 16, 18, 16, 16])
    for i, c in enumerate(P.CLASSES, start=5):
        x = F["mix"][c]
        row = [GD.CLASS_LABEL[c].capitalize(), x["plan_parcels"], x["contact_per_1000"], ("minus %d%%" % F["alert_effect"]) if c in ("L1", "L2") else "none",
               x["conversations"], x["share"], x["observed_share"]]
        for j, v in enumerate(row, start=1):
            cc = m.cell(row=i, column=j, value=v)
            if j in (2, 5):
                cc.number_format = "#,##0"
            if j in (3, 6, 7):
                cc.number_format = "0.0"
    i = 5 + len(P.CLASSES)
    for j, v in enumerate(["All outcomes", sum(F["mix"][c]["plan_parcels"] for c in P.CLASSES), "", "", F["season_conversations"], 100.0, 100.0], start=1):
        cc = m.cell(row=i, column=j, value=v); cc.font = Font(bold=True); cc.border = Border(top=THIN)
        if j in (2, 5):
            cc.number_format = "#,##0"
        if j in (6, 7):
            cc.number_format = "0.0"
    notes = [
        "Conversations a week over the season's %d weeks: about %s, against %s a week in the weeks observed." % (F["weeks"], "{:,}".format(F["per_week"]), "{:,}".format(F["obs_per_week"])),
        "Late and exception parcels generate %s per cent of the season's conversations, against %s per cent in the weeks observed." % (F["late_share"], F["obs_late_share"]),
        "Delay alerts: conversations per late parcel at Linz, Graz and Innsbruck after 12 October against before, relative to the other seven depots: minus %d per cent (one day late minus %d, two or more days late minus %d)."
        % (F["alert_effect"], F["alert_by_class"]["one day late"], F["alert_by_class"]["two or more days late"]),
    ]
    for k, t in enumerate(notes):
        m.cell(row=i + 2 + k, column=1, value=t).font = Font(size=10)
    m.freeze_panes = "B5"
    # ---- Rates by outcome
    c2 = wb.create_sheet("Rates by outcome")
    _title(c2, "Resolution rate by reason family and delivery outcome, version 3, follow-ups restored", "Per cent; conversations in the record beneath each rate's column group")
    _head(c2, 4, ["Reason family"] + ["%s %%" % GD.CLASS_LABEL[c].capitalize() for c in P.CLASSES] + ["n " + GD.CLASS_LABEL[c] for c in P.CLASSES] + ["Season weight on late and exception %"],
          [34, 11, 11, 13, 11, 10, 10, 12, 10, 16])
    for i, k in enumerate(FAM, start=5):
        c2.cell(row=i, column=1, value=nm[k])
        for j, c in enumerate(P.CLASSES):
            v = F["cells"][k][c]
            cc = c2.cell(row=i, column=2 + j, value=v if v is not None else "none"); cc.number_format = "0.0"
            c2.cell(row=i, column=6 + j, value=F["cell_n"][k][c]).number_format = "#,##0"
        c2.cell(row=i, column=10, value=F["season_weight_late"][k]).number_format = "0.0"
    c2.freeze_panes = "B5"
    # ---- Routes
    rt = wb.create_sheet("Routes")
    _title(rt, "What each shorter reading gives, beside the figures above", "Expected resolution rate over the season, per cent; families at 75 or more would be offered the assistant first")
    order = ["linked", "careful", "asis", "parcel_mix", "no_alerts", "no_phone", "no_written", "stationary"]
    _head(rt, 4, ["Reading"] + [nm[k] for k in FAM] + ["All families", "Assistant-first under this reading"], [58] + [13] * 10 + [12, 60])
    rows = [("This workbook", F["expected_table"], F["keep"])] + [(F["routes"][o]["label"][0].upper() + F["routes"][o]["label"][1:], F["routes"][o]["expected"], F["routes"][o]["keep"]) for o in order]
    for i, (lab, ex, keep) in enumerate(rows, start=5):
        c0 = rt.cell(row=i, column=1, value=lab); c0.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 5:
            c0.font = Font(bold=True)
        for j, k in enumerate(FAM + ["ALL"], start=2):
            cc = rt.cell(row=i, column=j, value=ex[k]); cc.number_format = "0.0"
            if k != "ALL" and (ex[k] >= F["line"]) != (F["expected"][k] >= F["line"]):
                cc.font = Font(bold=True, color=ORANGE)
        rt.cell(row=i, column=13, value=", ".join(nm[k] for k in keep)).alignment = Alignment(wrap_text=True, vertical="top")
    rt.cell(row=6 + len(rows), column=1, value="Orange: the reading puts the family on the other side of 75 per cent.").font = Font(size=9, color=MUTED)
    rt.freeze_panes = "B5"
    # ---- Notes
    n = wb.create_sheet("Notes")
    _title(n, "Definitions and conventions")
    lines = [
        "Resolution, contact, reason family and the assistant-first rule are as KS-07 issue 4 defines them (sections 2 to 4).",
        "Data cut: Monday 9 November 2026, 00:00. Rates are for version 3 conversations that ended from 28 September to 1 November (KS-07 3.3).",
        "A further contact is one that starts after the conversation ends and within 168 hours, on the same tracking number, in any of the four channels.",
        "Telephone times are converted from UTC to local time (clocks went back on 25 October).",
        "Delivery outcome is the network system's class of the consignment at the cut.",
        "Ranges are the 5th and 95th percentiles of 1,000 resamples of whole days (the days before version 3, the version 3 days before the alerts and the days after kept apart), every step redone; the season plan is taken as given (KS-07 4.3).",
        "A telephone call or written case that follows two conversations is counted once, against the later one, when calls and cases are counted.",
    ]
    for i, t in enumerate(lines, start=3):
        cc = n.cell(row=i, column=1, value=t); cc.alignment = Alignment(wrap_text=True, vertical="top")
    n.column_dimensions["A"].width = 150
    wb.save(path)
    created, modified = STAMPS[WORKBOOK]
    postprocess.normalize_ooxml(path, AUTHOR, AUTHOR, created, modified, excel=True, company=ORG)


def write_chart(path, F):
    nm = F["families"]
    order = sorted(FAM, key=lambda k: F["expected"][k])
    fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=200)
    fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
    for i, k in enumerate(order):
        col = "#2a78d6" if k in F["keep"] else "#eb6834"
        ax.plot([F["low"][k], F["high"][k]], [i, i], color=col, lw=2, solid_capstyle="round")
        ax.plot([F["expected"][k]], [i], "o", color=col, ms=7, mec="#fcfcfb", mew=1.5)
        ax.text(F["high"][k] + 0.8, i, "%.1f" % F["expected"][k], va="center", ha="left", fontsize=8.5, color="#0b0b0b")
    ax.axvline(F["line"], color="#52514e", lw=1, ls=(0, (4, 3)))
    ax.text(F["line"] + 0.4, len(order) - 0.35, "75% rule", fontsize=8.5, color="#52514e", va="bottom")
    ax.set_yticks(range(len(order))); ax.set_yticklabels([nm[k] for k in order], fontsize=8.5, color="#0b0b0b")
    ax.set_xlim(40, 100); ax.set_xlabel("Expected resolution rate over the peak season, % (dot) with 90% range (bar)", fontsize=8.5, color="#52514e")
    ax.tick_params(axis="x", labelsize=8, colors="#52514e"); ax.tick_params(axis="y", length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.grid(axis="x", color="#e6e5df", lw=0.6); ax.set_axisbelow(True)
    ax.plot([], [], "o", color="#2a78d6", label="Assistant first"); ax.plot([], [], "o", color="#eb6834", label="Adviser first")
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax.set_title("Five families clear 75% for the season; five do not", fontsize=10.5, loc="left", color="#0b0b0b", pad=10)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


def note_paragraphs(F):
    nm = F["families"]
    keep = [nm[k] for k in F["keep"]]; back = [nm[k] for k in F["hand_back"]]
    h = F["hurried"]
    extra = [nm[k] for k in h["extra"]]
    lst = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
    p = {}
    p["title"] = "Keep five reason families with the assistant through peak and offer an adviser first in the other five"
    p["call"] = ("Offer the assistant first for %s, and an adviser first for %s. On the season plan the assistant should resolve %s per cent of its "
                 "conversations across all ten families (90 per cent range %s to %s), against %s per cent in the five weeks of version 3 we can measure."
                 % (lst(keep), lst(back), F["expected_all"], F["low_all"], F["high_all"], F["achieved_all"]))
    p["notc"] = ("The linked record on its own reads %s per cent and would keep every family but one. With every follow-up restored but the weeks "
                 "observed carried into the season as they stand, %s would stay with the assistant at %s per cent; over the season it comes to %s."
                 % (F["linked_rate"], lst(extra) if extra else "the same families", h["expected"][h["extra"][0]] if extra else "", F["expected"][h["extra"][0]] if extra else ""))
    p["how"] = ("Three things move the figures. First, the record cannot see every follow-up: %s per cent of the telephone calls that follow an "
                "assistant conversation carry no tracking number, because the IVR is bypassed when the queue is long, and about %s written cases "
                "that follow a conversation were still open at the cut and so are not in the resolution extract. Restoring both takes the rate "
                "achieved from %s to %s per cent. Second, the season's conversations will not look like October's: late and exception parcels "
                "generate %s per cent of the conversations the plan implies, against %s per cent in the weeks observed, because a recipient of a "
                "parcel two or more days late is about %d times as likely to open a conversation as one whose parcel is on time. Third, the delay "
                "alerts go network-wide on 16 November: at the three pilot depots they cut conversations per late parcel by %d per cent, which is "
                "worth %s points on Delivery day and time and keeps that family above the line."
                % (F["phone_unkeyed_share"], F["written_open"], F["linked_rate"], F["achieved_all"], F["late_share"], F["obs_late_share"],
                   round(F["mix"]["L2"]["contact_per_1000"] / F["mix"]["ON"]["contact_per_1000"]), F["alert_effect"],
                   round(F["expected"]["DLV"] - F["routes"]["no_alerts"]["expected"]["DLV"], 1)))
    p["rest"] = ("The plan implies about %s assistant conversations a week over the season, against %s a week now. The ranges come from resampling "
                 "whole days, since good and bad days move every family together; resampling conversations one at a time would give a range for all "
                 "families of plus or minus %s points where the day-by-day figure is plus or minus %s."
                 % ("{:,}".format(F["per_week"]), "{:,}".format(F["obs_per_week"]), h["half_all"], F["half_all"]))
    p["caption"] = "Expected resolution rate over 16 November to 3 January by reason family, with its 90 per cent range, against the 75 per cent rule."
    p["foot"] = ("Basis: KS-07 issue 4 (resolution: no further contact about the same consignment through any channel within 168 hours; rates for "
                 "conversations at least seven days old at the cut; the season plan taken as given). Workings in %s." % WORKBOOK)
    return p


def write_note(path, F, png):
    P_ = note_paragraphs(F)
    nm = F["families"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(24); sec.top_margin = Mm(22); sec.bottom_margin = Mm(20)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    hp = sec.header.paragraphs[0]; hp.text = "Quellstein Paket, Customer Contact planning"; hp.runs[0].font.size = Pt(8); hp.runs[0].font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    t = doc.add_paragraph(); r = t.add_run(P_["title"]); r.bold = True; r.font.size = Pt(13)
    for k, v in (("To", "Helena Neumann"), ("From", "Simon Pertl"), ("Date", "10 November 2026"), ("Re", "assistant-first reason families for the peak season, KS-07 4.2")):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
        a = p.add_run("%s: " % k); a.bold = True
        p.add_run(v)
    doc.add_paragraph()
    for key in ("call", "notc", "how"):
        p = doc.add_paragraph(P_[key]); p.paragraph_format.space_after = Pt(6)
    doc.add_picture(png, width=Mm(155))
    c = doc.add_paragraph(P_["caption"]); c.runs[0].font.size = Pt(8.5); c.runs[0].italic = True
    p = doc.add_paragraph(P_["rest"]); p.paragraph_format.space_after = Pt(6)
    tb = doc.add_table(rows=1, cols=4)
    tb.style = "Light Grid Accent 1"; tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Reason family", "Expected over the season %", "90% range", "Offer first"]):
        tb.rows[0].cells[j].text = h
    for k in sorted(FAM, key=lambda x: -F["expected"][x]):
        cells = tb.add_row().cells
        cells[0].text = nm[k]; cells[1].text = "%.1f" % F["expected"][k]
        cells[2].text = "%.1f to %.1f" % (F["low"][k], F["high"][k]); cells[3].text = "Assistant" if k in F["keep"] else "Adviser"
    cells = tb.add_row().cells
    cells[0].text = "All ten families"; cells[1].text = "%.1f" % F["expected_all"]; cells[2].text = "%.1f to %.1f" % (F["low_all"], F["high_all"]); cells[3].text = ""
    for row in tb.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9)
    s = doc.add_paragraph(P_["foot"]); s.runs[0].font.size = Pt(8.5)
    doc.save(path)
    created, modified = STAMPS[NOTE]
    postprocess.normalize_docx(path, AUTHOR, AUTHOR, created, modified, 7, 96, "task16-note2", title="Assistant-first reason families, peak season 2026", company=ORG)


def write_all(F, golden_dir, scratch):
    os.makedirs(golden_dir, exist_ok=True)
    png = os.path.join(scratch, "scope.png")
    write_chart(png, F)
    write_workbook(os.path.join(golden_dir, WORKBOOK), F)
    write_note(os.path.join(golden_dir, NOTE), F, png)
