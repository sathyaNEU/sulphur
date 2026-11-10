"""The golden deliverables, from the shipped files only: arr_2027_forecast.xlsx (the monthly path with its 80 per cent
range, the bridge from October 2026 to December 2027, the commitment, the component figures and what each shortcut
gives) and arr_2027_note.docx (the note to the CFO with the call)."""
import calendar
import datetime as dt
import os

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import analysis as An
import load as LD
import params as P
import passes as PS
import postprocess
import routes as RT
import sim

XLSX = "arr_2027_forecast.xlsx"
DOCX = "arr_2027_note.docx"
DRAFT = 10.2           # the draft plan's December 2027 ARR, EUR million (the prompt)
ORG = "Tekenbord B.V."
AUTHOR = "Jelte Helmerhorst"


def r10k(x):
    return int(round(x / 1e4)) * 10000


def r100k(x):
    return round(round(x / 1e5) / 10.0, 1)


def eur(x):
    return "EUR {:,}".format(r10k(x))


def label(m):
    y, mo = sim.ym(m)
    return dt.date(y, mo, calendar.monthrange(y, mo)[1])


def bridge(g):
    """The six movement lines in the policy's order, rounded to EUR 10,000 so that they add up to the rounded
    December figure from the rounded October figure (the remainder, at most a step or two, sits on seat additions)."""
    team_change = g["team_left"] + g["team_new"] - g["open_team"]
    raw = [("New Business", g["new_bus"]), ("Business seat additions", g["expansion"]), ("Price", g["price"]),
           ("Business seat reductions", -g["contraction"]), ("Business accounts lost", -g["churn"]),
           ("Change in Team", team_change)]
    rounded = [[k, r10k(v)] for k, v in raw]
    gap = r10k(g["dec27"]) - r10k(g["open_total"]) - sum(v for _, v in rounded)
    rounded[1][1] += gap
    return raw, rounded, gap


def _digest(target):
    import hashlib
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(f.encode())
        h.update(open(os.path.join(target, f), "rb").read())
    for f in ("analysis.py", "passes.py", "routes.py", "load.py"):
        h.update(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), "rb").read())
    return h.hexdigest()[:20]


def compute(target, rivals=True):
    """The golden and every route on the pack; cached in the temp folder by the pack's and the code's digest."""
    import pickle
    import tempfile
    cache = os.path.join(tempfile.gettempdir(), "task1-routes-cache")
    key = os.path.join(cache, "routes-%s-%d.pkl" % (_digest(target), int(rivals)))
    if os.path.exists(key):
        return pickle.load(open(key, "rb"))
    out = _compute(target, rivals)
    os.makedirs(cache, exist_ok=True)
    pickle.dump(out, open(key, "wb"))
    return out


def _compute(target, rivals=True):
    F = LD.load(target)
    B = PS.Book(F)
    g = RT.golden(B)
    R = {}
    if rivals:
        R.update({k: dict(v, kind="rival") for k, v in RT.run(B, RT.RIVALS).items()})
        R.update({k: dict(v, kind="hurried") for k, v in RT.run(B, RT.HURRIED).items()})
        R["careful but hurried"] = dict(PS.golden(B, reps=RT.REPS, seed=RT.SEED, variant=RT.CAREFUL),
                                        kind="careful")
        R["quick"] = dict(PS.topdown(B), kind="quick")
        for h, fix in RT.HINTS.items():
            R["hint: " + h] = dict(PS.golden(B, reps=RT.RIVAL_REPS, seed=RT.SEED, variant=RT.careful_with(fix)),
                                   kind="hint", sentence=h)
    return F, B, g, R


# ------------------------------------------------------------------------------------------------ workbook
HEAD = PatternFill("solid", fgColor="D9E2EC")
THIN = Side(style="thin", color="9AA5B1")


def _head(ws, row):
    for c in ws[row]:
        if c.value is not None:
            c.font = Font(bold=True)
            c.fill = HEAD
            c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(path, B, g, R):
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    ws["A1"] = "Tekenbord ARR forecast to December 2027 (EUR, plan rate EUR 1.16 per GBP)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Month-end ARR on the ARR reporting policy v4. Data to 31 October 2026, prepared 6 November 2026."
    ws.append([])
    ws.append(["Month end", "Expected ARR", "80% range, low", "80% range, high"])
    _head(ws, 4)
    ws.append([label(P.CUT), r10k(g["open_total"]), None, None])
    for i, m in enumerate(range(P.CUT + 1, P.HORIZON + 1)):
        ws.append([label(m), r10k(g["path"][i]), r10k(g["path_p10"][i]), r10k(g["path_p90"][i])])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[0].number_format = "mmm yyyy"
        for c in row[1:]:
            c.number_format = "#,##0"
    ws.append([])
    ws.append(["October 2026 is on the books. The range is the 10th to 90th percentile of %d simulated paths."
               % RT.REPS])
    ws.append([])
    ws.append(["December 2027", "EUR"])
    _head(ws, ws.max_row)
    for k, v in (("Expected ARR", r10k(g["dec27"])), ("80% range, low (P10)", r10k(g["p10"])),
                 ("80% range, high (P90)", r10k(g["p90"])), ("80% chance of meeting or beating (P20)",
                                                            r10k(g["p20"]))):
        ws.append([k, v])
        ws.cell(ws.max_row, 2).number_format = "#,##0"
    ws.append(["Commitment, EUR million", r100k(g["p20"])])
    ws.append(["Draft plan figure, EUR million", DRAFT])
    ws.append(["Draft clears the 80% bar", "No" if r100k(g["p20"]) < DRAFT else "Yes"])
    for i, wd in enumerate([38, 16, 16, 16], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A5"

    wb2 = wb.create_sheet("Bridge")
    raw, rounded, gap = bridge(g)
    wb2.append(["ARR bridge, 31 October 2026 to 31 December 2027 (EUR, expected values)"])
    wb2["A1"].font = Font(bold=True, size=12)
    wb2.append([])
    wb2.append(["Line", "EUR"])
    _head(wb2, 3)
    wb2.append(["ARR 31 October 2026", r10k(g["open_total"])])
    for k, v in rounded:
        wb2.append([k, v])
    wb2.append(["Expected ARR 31 December 2027", r10k(g["dec27"])])
    wb2.cell(wb2.max_row, 1).font = Font(bold=True)
    wb2.cell(wb2.max_row, 2).font = Font(bold=True)
    for row in wb2.iter_rows(min_row=4, max_row=wb2.max_row):
        row[1].number_format = "#,##0;-#,##0"
    wb2.append([])
    wb2.append(["New Business split", "EUR"])
    _head(wb2, wb2.max_row)
    nf = r10k(g["new_bus"]) - r10k(g["new_open"]) - r10k(g["new_upgrade"])
    for k, v in (("Deals open at 31 October 2026", r10k(g["new_open"])), ("Deals created from November 2026", nf),
                 ("Team accounts moving to Business", r10k(g["new_upgrade"]))):
        wb2.append([k, v])
        wb2.cell(wb2.max_row, 2).number_format = "#,##0"
    wb2.append([])
    wb2.append(["Change in Team split", "EUR"])
    _head(wb2, wb2.max_row)
    for k, v in (("Team ARR 31 October 2026", g["open_team"]),
                 ("Accounts on Team at 31 Oct 2026, their ARR in December 2027", g["team_left"]),
                 ("Team accounts signing from November 2026, December 2027", g["team_new"])):
        wb2.append([k, r10k(v)])
        wb2.cell(wb2.max_row, 2).number_format = "#,##0"
    wb2.append([])
    wb2.append(["Lines to the nearest EUR 10,000; seat additions carry the bridge's rounding (%s) and deals created "
                "from November 2026 the new Business split's." % ("EUR {:,}".format(gap) if gap else "none needed")])
    wb2.column_dimensions["A"].width = 52
    wb2.column_dimensions["B"].width = 16

    w3 = wb.create_sheet("Inputs")
    w3.append(["Opening book and the estimates behind each line"])
    w3["A1"].font = Font(bold=True, size=12)
    w3.append([])
    w3.append(["Item", "Value", "Basis"])
    _head(w3, 3)
    up = g["uplift_fit"]
    rows = [
        ("Business ARR 31 Oct 2026, EUR", r10k(g["open_bus"]), "contract lines in force, true-ups to date"),
        ("Team ARR 31 Oct 2026, EUR", r10k(g["open_team"]), "October paid invoices, seats billed"),
        ("Business contracts in force", int(len(B.st)), ""),
        ("Renewals since Jan 2022 used for the exit and seat models", int(len(B.E)), "contract lines and workspace activity"),
        ("Repricings since 1 Mar 2026 used for the uplift", int(An.fit_business(B.E)["uplift_n"]), ""),
        ("Realised uplift at 20 seats", round(float(up[1]), 3), "per-seat price change at renewal"),
        ("Realised uplift, change per doubling of seats", round(float(up[0]) * np.log(2), 3), "log-linear in seats"),
        ("Mean realised uplift (all repricings)", round(An.fit_business(B.E)["uplift_mean"], 3), "not used"),
        ("Exit at renewal, log-odds intercept", round(g["churn_fit"][0], 2), "logistic"),
        ("  first renewal", round(g["churn_fit"][1], 2), ""),
        ("  per point of utilisation below 0.70", round(g["churn_fit"][2], 2), "active users over seats, last 3 months"),
        ("  a group sibling left in the last 12 months", round(g["churn_fit"][3], 2), "CRM parent account"),
        ("Team: lasting extra monthly exit, accounts padded to 3 seats", round(g["team_persist"], 4),
         "excess over the pre-April rate, mean of the last three months"),
        ("Open deals 31 Oct 2026", int((B.S["m"] == P.CUT).sum()), "pipeline snapshot"),
        ("New Business ARR per quoted seat, deals won since Mar 2026, EUR", round(B.per_seat, 1), "first contracts"),
    ]
    for r in rows:
        w3.append(list(r))
    w3.column_dimensions["A"].width = 60
    w3.column_dimensions["B"].width = 14
    w3.column_dimensions["C"].width = 46
    for row in w3.iter_rows(min_row=4, max_row=w3.max_row):
        if isinstance(row[1].value, int) and row[1].value > 9999:
            row[1].number_format = "#,##0"

    w4 = wb.create_sheet("Routes")
    w4.append(["What each shortcut gives (EUR; commitment in EUR million)"])
    w4["A1"].font = Font(bold=True, size=12)
    w4.append([])
    w4.append(["Route", "Price", "Seat reductions", "Accounts lost", "Oct Team accounts, Dec 2027", "New Business",
               "Expected Dec 2027", "Commitment"])
    _head(w4, 3)

    def line(name, f):
        return [name, r10k(f["price"]), r10k(f["contraction"]), r10k(f["churn"]), r10k(f["team_left"]),
                r10k(f["new_bus"]), r10k(f["dec27"]), r100k(f["p20"])]
    w4.append(line("This forecast", g))
    show = ["mean uplift applied flat", "list rise applied flat", "pooled renewal rates", "accounts drawn independently",
            "Team rates since April", "Team rates of the trailing twelve months", "CRM stage probabilities",
            "trailing run-rate of new ARR", "win odds by stage alone", "careful but hurried"]
    names = {"careful but hurried": "All of the above shortcuts that a quick model would take together"}
    for k in show:
        if k in R:
            w4.append(line(names.get(k, k[0].upper() + k[1:]), R[k]))
    if "quick" in R:
        w4.append(["Last twelve months' growth carried forward", None, None, None, None, None,
                   r10k(R["quick"]["dec27"]), None])
    for row in w4.iter_rows(min_row=4, max_row=w4.max_row):
        for c in row[1:7]:
            c.number_format = "#,##0"
    w4.append([])
    w4.append(["Each row changes one step against this forecast; the second-last row combines the flat uplift, pooled "
               "renewal rates, the last three months' Team rates, CRM probabilities and independent draws."])
    w4.column_dimensions["A"].width = 50
    for i in range(2, 9):
        w4.column_dimensions[get_column_letter(i)].width = 13
    wb.save(path)


# ------------------------------------------------------------------------------------------------ note
def write_docx(path, B, g, R):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    raw, rounded, gap = bridge(g)
    c = r100k(g["p20"])
    p = doc.add_paragraph()
    r = p.add_run("To: Naomi Weijters\nFrom: Jelte Helmerhorst, Revenue operations\nDate: 6 November 2026\n"
                  "Re: December 2027 ARR for the 2027 plan")
    r.font.size = Pt(9.5)
    h = doc.add_paragraph()
    hr = h.add_run("Commit EUR %.1f million of December 2027 ARR, not EUR %.1f million" % (c, DRAFT))
    hr.bold = True
    hr.font.size = Pt(13)
    doc.add_paragraph(
        "We have an 80 per cent chance of ending 2027 at or above %s, so the figure to put in the plan is EUR %.1f "
        "million. The draft's EUR %.1f million does not clear that bar: on this forecast we would meet it about %d "
        "times in 100. Expected ARR at 31 December 2027 is %s, with an 80 per cent range of %s to %s."
        % (eur(g["p20"]), c, DRAFT, int(round(100 * np.mean(np.array(g["draws"]) >= DRAFT * 1e6))),
           eur(g["dec27"]), eur(g["p10"]), eur(g["p90"])))
    doc.add_paragraph(
        "ARR on the books at 31 October 2026 is %s: %s Business and %s Team. The accounts on the Team plan at the end of "
        "October bring %s of Team ARR in December 2027. New Business signed from November 2026 to December 2027 comes to "
        "%s, of which %s from deals already open at the end of October."
        % (eur(g["open_total"]), eur(g["open_bus"]), eur(g["open_team"]), eur(g["team_left"]), eur(g["new_bus"]),
           eur(g["new_open"])))
    t = doc.add_table(rows=1, cols=2)
    t.style = "Table Grid"
    t.rows[0].cells[0].text = "Bridge, 31 Oct 2026 to 31 Dec 2027"
    t.rows[0].cells[1].text = "EUR"
    for k, v in [("ARR 31 October 2026", r10k(g["open_total"]))] + [(k, v) for k, v in rounded] + \
            [("Expected ARR 31 December 2027", r10k(g["dec27"]))]:
        row = t.add_row().cells
        row[0].text = k
        row[1].text = "{:,}".format(v)
        row[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for cell in t.rows[0].cells:
        for run in cell.paragraphs[0].runs:
            run.bold = True
    src = doc.add_paragraph()
    sr = src.add_run("Movement categories and order as in the ARR reporting policy v4, section 4; GBP at EUR 1.16. Lines "
                     "to the nearest EUR 10,000, seat additions carrying the rounding. Sources: billing contract lines "
                     "and Team invoices to 31 October 2026, workspace activity, CRM accounts, pipeline snapshots.")
    sr.font.size = Pt(8.5)
    sr.italic = True
    cr = R.get("careful but hurried", {})
    wp = doc.add_paragraph()
    wp.add_run("Why lower than the draft. ").bold = True
    wp.add_run(
        "Four things in the records pull the trailing numbers up. Price: renewals since "
        "March have kept about %.0f per cent of the list rise on contracts of 20 seats and less on large ones, which "
        "negotiate; applying the average rise to every contract still to renew gives %s of price, not %s. Seats and "
        "exits: renewals cut seats toward the people who use the product, first renewals most, and a group whose "
        "subsidiary has left tends to take the others with it; pooled renewal rates put seat reductions at %s "
        "against %s. Pipeline: deals that have sat in a stage for months rarely close, so the CRM's stage "
        "probabilities make the open pipeline worth %s against %s on our own win history. The band: subsidiaries "
        "of one group leave together, so their exits are drawn together; drawn one account at a time the 80 per "
        "cent figure would be about %s."
        % (100 * g["uplift_fit"][1] / (P.BUS_LIST_NEW["EUR"] / P.BUS_LIST_OLD["EUR"] - 1),
           eur(R["mean uplift applied flat"]["price"]) if R else "", eur(g["price"]),
           eur(R["pooled renewal rates"]["contraction"]) if R else "", eur(g["contraction"]),
           eur(R["CRM stage probabilities"]["new_open"]) if R else "", eur(g["new_open"]),
           eur(R["accounts drawn independently"]["p20"]) if R else ""))
    tp_ = doc.add_paragraph()
    tp_.add_run("Team. ").bold = True
    tp_.add_run(
        "The three-seat minimum from April pushed out many one- and two-person teams, but the extra exits have "
        "fallen back month by month; read as the new normal, the months since April would put the October accounts' Team ARR "
        "in December 2027 at %s, against %s." % (eur(R["Team rates since April"]["team_left"]) if R else "",
                                              eur(g["team_left"])))
    doc.add_paragraph("Monthly path, ranges and the effect of each shortcut are in arr_2027_forecast.xlsx.")
    fp = doc.sections[0].footer.paragraphs[0]
    fp.text = "Tekenbord B.V. | Revenue operations | 2027 plan"
    for r_ in fp.runs:
        r_.font.size = Pt(8)
    doc.core_properties.author = AUTHOR
    doc.save(path)
    postprocess.normalize_docx(path, AUTHOR, AUTHOR, "2026-11-05T13:20:00Z", "2026-11-06T10:48:00Z", revision=5,
                               total_time=71, seed="task1-note", title="December 2027 ARR for the 2027 plan",
                               company=ORG)


def write(target, outdir, rivals=True):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
    F, B, g, R = compute(target, rivals=rivals)
    write_xlsx(os.path.join(outdir, XLSX), B, g, R)
    postprocess.normalize_ooxml(os.path.join(outdir, XLSX), AUTHOR, AUTHOR, "2026-11-04T08:55:00Z",
                                "2026-11-06T10:31:00Z", excel=True, company=ORG)
    write_docx(os.path.join(outdir, DOCX), B, g, R)
    postprocess.own_mtimes(outdir, {})
    return F, B, g, R
