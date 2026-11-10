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
DRAFT = 10.3           # the draft plan's December 2027 ARR, EUR million (the prompt)
ORG = "Tekenbord B.V."
AUTHOR = "Jelte Helmerhorst"


def r10k(x):
    return int(round(x / 1e4)) * 10000


def r100k(x):
    return round(round(x / 1e5) / 10.0, 1)


def r50k(x):
    return int(round(x / 5e4)) * 50000


def r100k_eur(x):
    return int(round(x / 1e5)) * 100000


# the precision each coarser figure is stated at: the two note figures as the prompt asks them, the renewal
# components as the Critical Components state them (each the precision the defensible methods pin)
ROUND = {"team_left": 1e5, "new_open": 1e5, "contraction": 1e5, "churn": 5e4}
UNIT_WORD = {1e4: "nearest EUR 10,000", 5e4: "nearest EUR 50,000", 1e5: "nearest EUR 0.1 million"}


def rk(key):
    """The rounding function for a figure key."""
    step = ROUND.get(key, 1e4)
    return (lambda x: int(round(x / step)) * int(step))


def eurk(key, x):
    return "EUR {:,}".format(rk(key)(x))


def eur50(x):
    return "EUR {:,}".format(r50k(x))


def commit_m(f):
    """The commitment in EUR million: the largest 0.1 million step met in at least 80 per cent of the outcomes."""
    return round(f["commitment"] / 1e6, 1)


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
        R["naive"] = dict(PS.naive(B), kind="naive")
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
    ws["A2"] = "Month-end ARR on the ARR reporting policy v5. Data to 31 October 2026, prepared 6 November 2026."
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
    ws.append(["October 2026 is on the books. The range is the 10th to 90th percentile of %d simulated paths "
               "(policy v5, 5.2: the accounts' and deals' outcomes, with each estimated rate redrawn from its own "
               "sampling error; nothing added beyond the records)." % RT.REPS])
    ws.append([])
    ws.append(["December 2027", "EUR"])
    _head(ws, ws.max_row)
    for k, v in (("Expected ARR", r10k(g["dec27"])), ("80% range, low (P10)", r10k(g["p10"])),
                 ("80% range, high (P90)", r10k(g["p90"])), ("20th percentile", r10k(g["p20"]))):
        ws.append([k, v])
        ws.cell(ws.max_row, 2).number_format = "#,##0"
    ws.append(["Commitment, EUR million (largest 0.1m step met in at least 80% of outcomes, policy 5.3)",
               commit_m(g)])
    ws.cell(ws.max_row, 2).number_format = "0.0"
    ws.append(["Share of outcomes at or above the commitment", round(g["commitment_met"], 3)])
    ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append(["Share of outcomes at or above the next step up", round(g["commitment_next_met"], 3)])
    ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append(["Draft plan figure, EUR million", DRAFT])
    ws.cell(ws.max_row, 2).number_format = "0.0"
    ws.append(["Share of outcomes at or above the draft", round(float(np.mean(np.array(g["draws"]) >= DRAFT * 1e6)), 3)])
    ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append(["Draft clears the 80% bar", "No" if commit_m(g) < DRAFT else "Yes"])
    for i, wd in enumerate([62, 16, 16, 16], 1):
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
    wb2.append(["Behind two of the lines (each to the %s)" % UNIT_WORD[ROUND["new_open"]], "EUR"])
    _head(wb2, wb2.max_row)
    for k, v in (("New Business from deals open at 31 October 2026", rk("new_open")(g["new_open"])),
                 ("Team ARR in December 2027 from accounts on Team at 31 October 2026", rk("team_left")(g["team_left"]))):
        wb2.append([k, v])
        wb2.cell(wb2.max_row, 2).number_format = "#,##0"
    wb2.append([])
    wb2.append(["Lines to the nearest EUR 10,000; seat additions carry the bridge's rounding (%s)."
                % ("EUR {:,}".format(gap) if gap else "none needed")])
    wb2.column_dimensions["A"].width = 52
    wb2.column_dimensions["B"].width = 16

    w3 = wb.create_sheet("Inputs")
    w3.append(["Opening book and the estimates behind each line (policy v5)"])
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
        ("Repricings since 1 Jan 2026 used for the uplift", int(An.fit_business(B.E)["uplift_n"]), ""),
        ("Realised uplift at 20 seats", round(float(up[1]), 3), "per-seat price change at renewal"),
        ("Realised uplift, change per doubling of seats", round(float(up[0]) * np.log(2), 3), "log-linear in seats"),
        ("Mean realised uplift (all repricings)", round(An.fit_business(B.E)["uplift_mean"], 3), "not used"),
        ("Exit at renewal, log-odds intercept", round(g["churn_fit"][0], 2), "logistic"),
        ("  first renewal", round(g["churn_fit"][1], 2), ""),
        ("  per point of utilisation below 0.70", round(g["churn_fit"][2], 2), "active users over seats, last 3 months"),
        ("  a group sibling left in the last 12 months", round(g["churn_fit"][3], 2), "CRM parent account"),
        ("Team: lasting extra monthly exit, accounts padded to 3 seats", round(g["team_persist"], 4),
         "excess over the pre-January rate at the calendar index, mean of the last three months"),
        ("Team: calendar index of cancellations, Oct / Mar", "%.2f / %.2f" % (g["team_season"][10], g["team_season"][3]),
         "pre-January history, exposure-weighted mean 1"),
        ("Open deals 31 Oct 2026", int((B.S["m"] == P.CUT).sum()), "pipeline snapshot"),
        ("New Business ARR per quoted seat, deals won since Jan 2026, EUR", round(B.per_seat, 1), "first contracts"),
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
    w4.append(["What each shortcut gives (EUR; the commitment in EUR million)"])
    w4["A1"].font = Font(bold=True, size=12)
    w4.append([])
    w4.append(["Route", "Price", "Seat reductions", "Accounts lost", "Oct Team accounts, Dec 2027 (0.1m)",
               "Open deals' new Business (0.1m)", "New Business", "Expected Dec 2027", "Commitment"])
    _head(w4, 3)

    def line(name, f):
        return [name, r10k(f["price"]), r10k(f["contraction"]), r10k(f["churn"]), rk("team_left")(f["team_left"]),
                rk("new_open")(f["new_open"]), r10k(f["new_bus"]), r10k(f["dec27"]), commit_m(f)]
    w4.append(line("This forecast", g))
    show = ["mean uplift applied flat", "list rise applied flat",
            "pooled renewal rates", "accounts drawn independently", "Team rates of the last three months",
            "Team rates since April", "Team rates of the trailing twelve months", "Team rates before April",
            "CRM stage probabilities", "win odds by stage alone", "trailing run-rate of new ARR",
            "the book's trailing true-up rate near seats", "band without the estimation uncertainty",
            "an assumed common factor of 0.25 added", "careful but hurried"]
    names = {"careful but hurried": "The shortcuts a quick model would take together",
             "Team rates since April": "Team rates since January 2026", "Team rates before April":
             "Team rates before January 2026, no lasting excess"}
    for k in show:
        if k in R:
            w4.append(line(names.get(k, k[0].upper() + k[1:]), R[k]))
    for row in w4.iter_rows(min_row=4, max_row=w4.max_row):
        for c in row[1:8]:
            c.number_format = "#,##0"
        if len(row) > 8 and isinstance(row[8].value, (int, float)):
            row[8].number_format = "0.0"
    w4.append([])
    w4.append(["Trailing extrapolations (point forecasts of December 2027, EUR)", ""])
    _head(w4, w4.max_row)
    if "naive" in R:
        for k, v in R["naive"].items():
            if k == "kind":
                continue
            w4.append([k[0].upper() + k[1:], r10k(v)])
            w4.cell(w4.max_row, 2).number_format = "#,##0"
    w4.append([])
    w4.append(["Each row changes one step against this forecast; the last route row combines the flat uplift, pooled "
               "renewal rates, the last three months' Team rates, CRM probabilities and independent draws. Every "
               "trailing extrapolation clears the draft; the forecast does not."])
    w4.column_dimensions["A"].width = 62
    for i in range(2, 10):
        w4.column_dimensions[get_column_letter(i)].width = 14
    wb.save(path)


# ------------------------------------------------------------------------------------------------ note
def write_docx(path, B, g, R):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    raw, rounded, gap = bridge(g)
    c = commit_m(g)
    draft_pct = int(round(100 * np.mean(np.array(g["draws"]) >= DRAFT * 1e6)))
    p = doc.add_paragraph()
    r = p.add_run("To: Naomi Weijters\nFrom: Jelte Helmerhorst, Revenue operations\nDate: 6 November 2026\n"
                  "Re: December 2027 ARR for the 2027 plan")
    r.font.size = Pt(9.5)
    h = doc.add_paragraph()
    hr = h.add_run("Commit EUR %.1f million of December 2027 ARR, not EUR %.1f million" % (c, DRAFT))
    hr.bold = True
    hr.font.size = Pt(13)
    doc.add_paragraph(
        "EUR %.1f million is the largest 0.1 million step we meet or beat in at least 80 per cent of outcomes (%d in "
        "100; the next step up, EUR %.1f million, only %d in 100), so it is the figure for the plan under policy "
        "5.3. The draft's EUR %.1f million does not clear that bar: on this forecast we would meet it about %d times "
        "in 100. Expected ARR at 31 December 2027 is %s, with an 80 per cent range of %s to %s."
        % (c, int(round(100 * g["commitment_met"])), c + 0.1, int(round(100 * g["commitment_next_met"])), DRAFT,
           draft_pct, eur(g["dec27"]), eur(g["p10"]), eur(g["p90"])))
    doc.add_paragraph(
        "ARR on the books at 31 October 2026 is %s: %s Business and %s Team. The accounts on the Team plan at the end of "
        "October bring %s of Team ARR in December 2027 (to the %s). New Business signed from November "
        "2026 to December 2027 comes to %s, of which %s (to the %s) from deals already open at the end "
        "of October."
        % (eur(g["open_total"]), eur(g["open_bus"]), eur(g["open_team"]), eurk("team_left", g["team_left"]),
           UNIT_WORD[ROUND["team_left"]], eur(g["new_bus"]), eurk("new_open", g["new_open"]),
           UNIT_WORD[ROUND["new_open"]]))
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
    sr = src.add_run("Movement categories and order as in the ARR reporting policy v5, section 4; GBP at EUR 1.16. Lines "
                     "to the nearest EUR 10,000, seat additions carrying the rounding. Sources: billing contract lines "
                     "and Team invoices to 31 October 2026, workspace activity, CRM accounts, pipeline snapshots.")
    sr.font.size = Pt(8.5)
    sr.italic = True
    nv = R.get("naive", {})
    wp = doc.add_paragraph()
    wp.add_run("Why lower than the draft. ").bold = True
    wp.add_run(
        "Carried forward, the last twelve months give %s (compounded) and the last six months %s, and every "
        "trailing view clears EUR %.1f million; they carry the January price rise, which has now landed on every "
        "contract but the November and December renewals. Taken flow by flow the book does not get there. Price: "
        "renewals since January have kept about %.0f per cent of the list rise on contracts of 20 seats and less on "
        "large ones, which negotiate; the rise still to land is %s, and applying the average realised rise to the "
        "remaining contracts would give %s. Seats and exits: the accounts signed in the last two years were sold "
        "more seats per working user than the older book, renewals cut seats toward the people who use the product "
        "(first renewals most) and exit more often where use is low, and a group whose subsidiary has left tends to "
        "take the others with it; pooled renewal rates put accounts lost at %s against %s. Pipeline: deals that "
        "have sat in a stage for months rarely close, so the CRM's stage probabilities make the open pipeline worth "
        "%s against %s on our own win history. The band: each estimated rate is redrawn from its own sampling error "
        "and subsidiaries of one group leave together; drawn one account at a time the commitment would read EUR "
        "%.1f million, and no allowance is added beyond what the records show (policy 5.2)."
        % (eur(nv.get("trailing twelve months' growth compounded", 0)),
           eur(nv.get("trailing six months' net new ARR carried forward", 0)), DRAFT,
           100 * g["uplift_fit"][1] / (P.BUS_LIST_NEW["EUR"] / P.BUS_LIST_OLD["EUR"] - 1), eur(g["price"]),
           eur(R["mean uplift applied flat"]["price"]) if R else "",
           eurk("churn", R["pooled renewal rates"]["churn"]) if R else "", eurk("churn", g["churn"]),
           eurk("new_open", R["CRM stage probabilities"]["new_open"]) if R else "", eurk("new_open", g["new_open"]),
           commit_m(R["accounts drawn independently"]) if R else 0.0))
    tp_ = doc.add_paragraph()
    tp_.add_run("Team. ").bold = True
    tp_.add_run(
        "Cancellations on the Team plan run with the calendar (the autumn months carry about %.0f per cent more "
        "than the year's average, late winter about %.0f per cent less), and the three-seat minimum from January "
        "pushed out many one- and two-person teams in the first months, an excess that has faded to a small "
        "lasting level. Carrying the last three months' rates forward would put the October accounts' Team ARR in "
        "December 2027 at %s (the whole year since January carried forward, %s), against %s."
        % (100 * (max(g["team_season"].values()) - 1), 100 * (1 - min(g["team_season"].values())),
           eurk("team_left", R["Team rates of the last three months"]["team_left"]) if R else "",
           ("the same" if R and eurk("team_left", R["Team rates since April"]["team_left"]) ==
            eurk("team_left", R["Team rates of the last three months"]["team_left"]) else
            eurk("team_left", R["Team rates since April"]["team_left"])) if R else "", eurk("team_left", g["team_left"])))
    doc.add_paragraph("Monthly path, ranges, the inputs and the effect of each shortcut are in arr_2027_forecast.xlsx.")
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
