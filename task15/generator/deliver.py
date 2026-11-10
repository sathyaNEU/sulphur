"""task15: the golden deliverables, written from figures.json's object alone: the workbook, the bridge chart and the
note. One set of numbers everywhere; every container through the house writers."""
import datetime as dt
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import postprocess as PP  # noqa: E402
import world as W  # noqa: E402

UTC = dt.timezone.utc
Y = W.SOW                               # the sowing year the nominations are for, and the year the work is done in
BOOK, CHART, NOTE = "hrz_nominations_%d.xlsx" % Y, "shortfall_bridge.png", "hrz_nominations_%d_note.docx" % Y
STAMPS = {CHART: dt.datetime(Y, 2, 17, 2, 38, 21, tzinfo=UTC)}
CLOSE = max(d for d in (dt.date(Y, 2, k) for k in range(1, 29)) if d.weekday() == 4)   # the last Friday of February
AUTHOR, COMPANY = "Jesse Gibson", "Banyena Grain Genetics"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
HEAD_FILL = PatternFill("solid", fgColor="22382B")
HEAD_FONT = Font(bold=True, color="FFFFFF")
PICK_FILL = PatternFill("solid", fgColor="E3EFE6")
THIN = Side(style="thin", color="BBBBBB")


def and_list(xs):
    xs = [str(x) for x in xs]
    if len(xs) < 2:
        return xs[0] if xs else "none"
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def nums(xs, fmt="%.1f"):
    return and_list([fmt % x for x in xs])


def pcts(xs):
    return and_list(["%d%%" % round(x) for x in xs])


WORDS = {1: "one", 2: "two", 3: "three"}
ORDINALS = {1: "first", 2: "second", 3: "third"}


def signed(x):
    return "%+.1f" % x


def table(ws, top, header, rows, widths=None, formats=None, pick=None):
    for j, h in enumerate(header, 1):
        c = ws.cell(row=top, column=j, value=h)
        c.font, c.fill = HEAD_FONT, HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[top].height = 44
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=top + i, column=j, value=v)
            if formats and j in formats and isinstance(v, (int, float)):
                c.number_format = formats[j]
            if isinstance(v, str):
                c.alignment = Alignment(horizontal="left")
            if pick and pick(row):
                c.fill = PICK_FILL
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
    return top + len(rows)


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=13)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, color="555555")


def workbook(F, path):
    L, std, yr = F["lines"], F["standard"], F["years"]
    picks, nxt, idx3 = F["nominate"], F["first_left_out"], F["index_would_nominate"]
    wb = Workbook()

    # ---- the call
    ws = wb.active
    ws.title = "Nominations"
    npk = len(picks)
    title(ws, "Nominate %s for %d sowing" % (and_list(picks), yr["decision_sow"]),
          "Relative yield is per cent of Byaduk over the line's two series seasons; Mount Rouse's uptake standard is "
          "%.1f." % std)

    def row(w_, role):
        d = L[w_]
        return [w_, role, d["stage3_seasons"], d["index"], d["expected_ry"], d["low"], d["high"], d["lodging_pct"]]

    others = [w_ for w_ in idx3 if w_ not in picks and w_ != nxt]
    rows = [row(w_, "nominate") for w_ in picks] + [row(nxt, "first left out")] + \
           [row(w_, "the index would put up") for w_ in others]
    end = table(ws, 4, ["Line", "", "Stage 3 seasons", "High-rainfall index (% of Byaduk)",
                        "Expected relative yield in the series", "80% range, low", "80% range, high",
                        "Expected lodging in the series (%)"], rows,
                [11, 24, 9, 14, 15, 11, 11, 15], {4: "0.0", 5: "0.0", 6: "0.0", 7: "0.0", 8: "0"},
                pick=lambda r: r[1] == "nominate")
    ws.cell(row=end + 2, column=1, value="The %s nominated stands clear of the first line left out by (points)"
            % ("second line" if npk == 2 else "last line")).font = Font(bold=True)
    ws.cell(row=end + 2, column=5, value=F["cut_points"]).number_format = "0.0"
    ws.freeze_panes = "A5"

    # ---- every Stage 3 line
    ws = wb.create_sheet("Stage 3 lines")
    title(ws, "Stage 3 lines of %d not yet nominated, by expected relative yield in the series" % yr["last_season"],
          "Expected over the series' trials as it has run since %d; ranges are for what two seasons return."
          % yr["first_season"])
    order = sorted(L, key=lambda k: F["rank"][k])
    rows = [[F["rank"][w_], w_, L[w_]["stage3_seasons"], L[w_]["index"], F["index_rank"][w_], L[w_]["expected_ry"],
             L[w_]["low"], L[w_]["high"], L[w_]["lodging_pct"], "nominate" if w_ in picks else ""] for w_ in order]
    end = table(ws, 4, ["Rank", "Line", "Stage 3 seasons", "High-rainfall index (% of Byaduk)", "Rank on the index",
                        "Expected relative yield in the series", "80% range, low", "80% range, high",
                        "Expected lodging in the series (%)", ""], rows,
                [6, 11, 9, 14, 9, 15, 11, 11, 15, 11],
                {4: "0.0", 6: "0.0", 7: "0.0", 8: "0.0", 9: "0"}, pick=lambda r: r[-1] == "nominate")
    ws.auto_filter.ref = "A4:J%d" % end
    ws.freeze_panes = "C5"

    # ---- the bridge
    ws = wb.create_sheet("Bridge")
    title(ws, "Why the %d completed nominations returned %.1f against %.1f quoted"
          % (F["completed_nominations"], F["realised_mean"], F["quoted_mean"]),
          "Means over the nominations sown %d to %d; points are points of relative yield."
          % (yr["first_sow"], yr["last_completed_sow"]))
    rows = [["Mean index quoted", F["quoted_mean"], None],
            ["(a) The index: quoted less the relative yield to expect at the trials it was taken from", None,
             -F["overstated_at_own_sites_points"]],
            ["Relative yield to expect at those trials", F["worth_at_own_sites_mean"], None],
            ["(b) The move to the Series, apart from lodging", None, -F["benchmark_water_response_points"]],
            ["(c) Lodging at the Series trials beyond the index trials, on the lodging recorded", None,
             -F["lodging_points"]],
            ["Relative yield to expect at the Series trials", F["expected_in_series_mean"], None],
            ["(d) The remainder", None, -F["left_over_points"]],
            ["Mean relative yield returned", F["realised_mean"], None]]
    end = table(ws, 4, ["", "Relative yield (% of Byaduk)", "Change (points)"], rows, [74, 16, 14],
                {2: "0.0", 3: "+0.0;-0.0"})
    for r in (5, 7, 10, 12):
        ws.cell(row=r, column=1).font = Font(bold=True)
    bm = F["bridge_means"]
    top = end + 3
    ws.cell(row=top - 1, column=1, value="What the heads are made of (means over the lines)").font = Font(bold=True)
    rows = [["Yield over Byaduk before lodging, t/ha", bm["advantage_at_index_trials_t_ha"],
             bm["advantage_at_series_trials_t_ha"]],
            ["Byaduk's yield, t/ha", bm["byaduk_at_index_trials_t_ha"], bm["byaduk_at_series_trials_t_ha"]],
            ["Season water, mm", bm["water_at_index_trials_mm"], bm["water_at_series_trials_mm"]],
            ["Plot lodged over Byaduk's, points", bm["lodging_over_byaduk_at_index_trials_pct"],
             bm["lodging_over_byaduk_at_series_trials_pct"]],
            ["Cost of a tenth of a plot lodged, t/ha", F["evidence"]["loss_per_tenth_within"], None]]
    end = table(ws, top, ["", "At the index trials", "At the Series trials"], rows, None,
                {2: "0.00", 3: "0.00"})
    for r_ in (top + 3, top + 4):
        for c_ in (2, 3):
            ws.cell(row=r_, column=c_).number_format = "0" if r_ == top + 3 else "0.0"
    ws.cell(row=top + 5, column=2).number_format = "0.000"
    top = end + 3
    ws.cell(row=top - 1, column=1, value="By sowing year").font = Font(bold=True)
    by = F["bridge_by_sowing"]
    rows = [[int(y), by[y]["quoted"], by[y]["realised"], by[y]["shortfall"], by[y]["own"], by[y]["water"],
             by[y]["lodging"], by[y]["left"]] for y in sorted(by, key=int)]
    rows.append(["All", F["quoted_mean"], F["realised_mean"], F["shortfall_points"],
                 F["overstated_at_own_sites_points"], F["benchmark_water_response_points"], F["lodging_points"],
                 F["left_over_points"]])
    end = table(ws, top, ["Sowing year", "Index quoted", "Returned", "Gap", "(a) The index",
                          "(b) The move to the Series", "(c) Lodging", "(d) The remainder"], rows,
                None, {c: "0.0" for c in range(2, 9)})
    for j in range(1, 9):
        ws.cell(row=end, column=j).font = Font(bold=True)
        ws.cell(row=end, column=j).border = Border(top=THIN)
    top = end + 3
    ws.cell(row=top - 1, column=1, value="By nomination").font = Font(bold=True)
    br = F["bridge"]
    rows = [[br[w_]["sowing"], w_, br[w_]["quoted"], br[w_]["worth_at_own_sites"], br[w_]["water"], br[w_]["lodging"],
             br[w_]["expected_in_series"], br[w_]["realised"]] for w_ in sorted(br, key=lambda k: (br[k]["sowing"], k))]
    table(ws, top, ["Sowing year", "Line", "Index quoted", "To expect at the index trials",
                    "(b) The move to the Series", "(c) Lodging", "To expect at the Series trials", "Returned"], rows,
          None, {c: "0.0" for c in range(3, 9)})
    for j, w in enumerate([74, 16, 14, 14, 14, 14, 14, 12], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A5"

    # ---- the quicker routes
    ws = wb.create_sheet("Other routes")
    title(ws, "What the other routes give",
          "Each route's nominations, its split of the gap and its error on the nominations already made had it been "
          "run as each was nominated.")
    h, hw = F["hurried"], F["hurried_on_water"]
    one = F["one_fact"]
    k1 = [k for k in one if "response" in k][0]
    k2 = [k for k in one if "lodge" in k][0]
    ro = F["ruled_out"]
    kl = [k for k in ro if "yield level" in k][0]
    ki = [k for k in ro if "Kerang" in k][0]
    pl = F["proportional_loss"]

    def r_(name, d):
        return [name, ", ".join(d["nominate"]) or "none", d.get("own"), d.get("water"), d.get("lodging"),
                d.get("left"), d.get("rmse")]

    gold = dict(nominate=picks, own=F["overstated_at_own_sites_points"], water=F["benchmark_water_response_points"],
                lodging=F["lodging_points"], left=F["left_over_points"], rmse=F["backtest_rmse_points"])
    kp = [k for k in F["rivals"] if "no pooling" in k][0]
    rows = [r_("This workbook", gold),
            ["The same, the lodging loss read as a share of the plot's yield", ", ".join(picks),
             F["overstated_at_own_sites_points"], pl["water"], pl["lodging"], F["left_over_points"], None],
            r_("Each line fitted on its own trials alone, no pooling", F["rivals"][kp]),
            ["The index as quoted", ", ".join(idx3) or "none", F["shortfall_points"], 0.0, 0.0, 0.0,
             F["index_rmse_points"]],
            ["The index scaled to what past nominations returned", ", ".join(F["index_route"]["nominate"]) or "none",
             None, None, None, None, None],
            r_("One response for all lines to the trial's yield level, the average miss taken off", h),
            r_("The same on season water", hw),
            r_("Every line its own response to season water, lodging not carried to the series", one[k1]),
            r_("Lodging carried to the series, no response to season water", one[k2]),
            r_("Every line its own response to the trial's yield level", ro[kl]),
            r_("Kerang's waterings left out of its season water", ro[ki])]
    table(ws, 4, ["Route", "Nominates", "(a) The index", "(b) The move to the Series", "(c) Lodging",
                  "(d) The remainder", "Error on past nominations (RMS)"], rows,
          [66, 26, 13, 13, 12, 12, 16], {c: "0.0" for c in range(3, 8)})
    ws.freeze_panes = "A5"

    # ---- notes
    ws = wb.create_sheet("Notes")
    ev = F["evidence"]
    notes = [
        ("As at", "12 February %d, on the %d harvest record and the series' results published on 5 February."
         % (yr["decision_sow"], yr["last_season"])),
        ("Relative yield", "An entry's mean yield over a set of series trials as a percentage of Byaduk's over the same "
                           "trials (series protocol, section 7)."),
        ("High-rainfall index", "The mean over a line's Stage 3 trials at Lake Bolac, Skipton and Kerang of its mean "
                                "over harvested plots as a percentage of Byaduk's in the same trial (trial handbook, "
                                "section 6)."),
        ("Uptake standard", "Relative yield of %.1f or more over the series trials of the line's first two seasons "
                            "(option deed, schedule 2, clause 2.1)." % std),
        ("Nominations", "The %s lines with the highest expected relative yield over two series seasons (%s entries "
                        "this year; the deed allows up to %s, schedule 2, clause 1.1)."
         % (WORDS[F["places"]], WORDS[F["places"]], WORDS[F["nominations_allowed"]])),
        ("Completed nominations", "The %d lines sown in the series from %d to %d, each with both seasons "
                                  "published. The %d sown in %d have one season and are left out."
         % (F["completed_nominations"], yr["first_sow"], yr["last_completed_sow"], yr["pending"], yr["pending_sow"])),
        ("Season water", "April to October rain at the site; at Kerang, plus the water applied (irrigation log)."),
        ("Heads of the gap", "As the option deed's schedule 2, clause 4.2 sets them; each head is a mean over the "
                             "lines, rounded on its own."),
        ("Plots", "A plot weighed twice takes its later weighing. An abandoned plot has no weight and keeps its "
                  "lodging figure: %d of %s plots, %.1f%% lodged on average against %.1f%% for harvested plots."
         % (ev["abandoned"], format(ev["plots"], ","), ev["lodging_pct_abandoned"], ev["lodging_pct_harvested"])),
        ("Expected in the series", "Over all %d trials the series has harvested since %d. The 80%% range is the 10th "
                                   "to the 90th percentile of what two seasons would return."
         % (ev["series_trials"], yr["first_season"])),
        ("Rounding", "Relative yields and points to one decimal, lodging to whole per cent; parts are rounded on "
                     "their own, so a row can differ from its total by 0.1."),
    ]
    title(ws, "Definitions and conventions")
    for i, (k, v) in enumerate(notes, 3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=1).alignment = Alignment(vertical="top")
        ws.row_dimensions[i].height = 32
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 110
    for s in wb.worksheets:
        s.sheet_view.showGridLines = False
        s.page_setup.orientation = "landscape"
        s.page_setup.fitToWidth = 1
    wb.save(path)
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, "%d-02-12T23:12:00Z" % Y, "%d-02-17T03:02:00Z" % Y,
                       title="HRBS nominations for %d sowing" % Y, excel=True, company=COMPANY)


def chart(F, path):
    """The bridge: levels as markers, each part a floating bar between two levels. Nothing is drawn from a cut axis."""
    q, own, wat, lod = F["quoted_mean"], F["overstated_at_own_sites_points"], F["benchmark_water_response_points"], \
        F["lodging_points"]
    exp, real, left, std = F["expected_in_series_mean"], F["realised_mean"], -F["left_over_points"], F["standard"]
    worth = F["worth_at_own_sites_mean"]
    after_w = round(worth - wat, 1)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "text.color": INK})
    fig, ax = plt.subplots(figsize=(8.6, 4.5), dpi=160)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    levels = [(0, q, "Index\nquoted"), (4, exp, "Expected in\nthe series"), (6, real, "Returned")]
    steps = [(1, q, worth, "The index", -own), (2, worth, after_w, "The move to\nthe Series", -wat),
             (3, after_w, exp, "Lodging", -lod), (5, exp, real, "The remainder", left)]
    w = 0.34
    for x, a, b, lab, d in steps:
        lo, hi = min(a, b), max(a, b)
        ax.bar(x, hi - lo, bottom=lo, width=w, color=ORANGE if d < 0 else AQUA, linewidth=0, zorder=3)
        ax.text(x, hi + 0.35, signed(d), ha="center", va="bottom", fontsize=9.5, color=INK, fontweight="bold")
    xs = [0, 1, 2, 3, 4, 5, 6]
    conn = [(0, 1, q), (1, 2, worth), (2, 3, after_w), (3, 4, exp), (4, 5, exp), (5, 6, real)]
    for x0, x1, yv in conn:
        ax.plot([x0 + (0.2 if x0 in (0, 4, 6) else w / 2), x1 - (0.2 if x1 in (0, 4, 6) else w / 2)], [yv, yv],
                color=GRID, linewidth=1, zorder=2)
    for x, yv, lab in levels:
        ax.plot([x - 0.2, x + 0.2], [yv, yv], color=BLUE, linewidth=3.2, solid_capstyle="round", zorder=4)
        ax.text(x, yv + 0.4, "%.1f" % yv, ha="center", va="bottom", fontsize=10, color=INK, fontweight="bold")
    ax.axhline(std, color=INK2, linewidth=1, zorder=1)
    ax.text(6.55, std + 0.25, "uptake standard %.1f" % std, ha="right", va="bottom", fontsize=8.5, color=INK2)
    ax.set_xticks(xs)
    ax.set_xticklabels(["Index\nquoted", "The index\noverstated", "The move to\nthe Series", "Lodging at\nthe Series",
                        "To expect in\nthe Series", "The\nremainder", "Returned"], fontsize=8.5, color=INK2)
    ax.set_xlim(-0.6, 6.6)
    ax.set_ylim(94, 117.5)
    ax.set_yticks([95, 100, 105, 110, 115])
    ax.set_ylabel("Relative yield, % of Byaduk", color=INK2, fontsize=9)
    ax.tick_params(axis="y", colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    handles = [plt.Line2D([0], [0], color=BLUE, linewidth=3.2, solid_capstyle="round"),
               plt.Rectangle((0, 0), 1, 1, color=ORANGE)]
    labels = ["mean of the %d nominations" % F["completed_nominations"], "taken off"]
    if any(d > 0 for _, _, _, _, d in steps):
        handles.append(plt.Rectangle((0, 0), 1, 1, color=AQUA))
        labels.append("added back")
    ax.legend(handles, labels, loc="upper right", frameon=False, fontsize=8.5, ncol=3, handlelength=1.4,
              columnspacing=1.4, bbox_to_anchor=(1.0, 1.02))
    fig.suptitle("Quoted at %.1f, returned %.1f: %.1f points were never there, %.1f went in the move to the\n"
                 "Series' wetter trials and %.1f to lodging there" % (q, real, own, wat, lod),
                 x=0.012, y=0.985, ha="left", va="top", fontsize=11, fontweight="bold", color=INK)
    yr = F["years"]
    fig.text(0.012, 0.012, "Banyena nominations sown in the High Rainfall Barley Series %d to %d, two seasons each.\n"
             "Sources: plot harvest record %d to %d; HRBS site results %d to %d."
             % (yr["first_sow"], yr["last_completed_sow"], yr["first_season"], yr["last_season"], yr["first_season"],
                yr["last_season"]), fontsize=7.5, color=INK2, linespacing=1.35)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.84, bottom=0.215)
    fig.savefig(path, format="png", metadata={"Software": None}, facecolor=SURFACE)
    plt.close(fig)


def note(F, path, png):
    L, std, yr = F["lines"], F["standard"], F["years"]
    picks, nxt, idx3 = F["nominate"], F["first_left_out"], F["index_would_nominate"]
    ev = F["evidence"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(21)
    sec.top_margin, sec.bottom_margin = Mm(17), Mm(16)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)

    def para(text, bold=False, size=None, after=5, italic=False, color=None):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor(*color)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(0)
        return p

    def tbl(header, rows, widths):
        t = doc.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        for j, hd in enumerate(header):
            c = t.rows[0].cells[j]
            c.text = ""
            r = c.paragraphs[0].add_run(hd)
            r.bold = True
            r.font.size = Pt(9)
        for row in rows:
            cells = t.add_row().cells
            for j, v in enumerate(row):
                cells[j].text = ""
                r = cells[j].paragraphs[0].add_run(v)
                r.font.size = Pt(9.5)
                if j:
                    cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for row in t.rows:
            for j, wd in enumerate(widths):
                row.cells[j].width = Mm(wd)
        return t

    para("To: Meredith Cooke, Head of Breeding", after=0, size=9.5, color=(70, 70, 70))
    para("From: Jesse Gibson, Trials and Data", after=0, size=9.5, color=(70, 70, 70))
    para("17 February %d. HRBS nominations close on %d February." % (Y, CLOSE.day), after=8, size=9.5,
         color=(70, 70, 70))
    npk = len(picks)
    eo = F["estimate_only"]
    others = [w_ for w_ in idx3 if w_ not in picks]
    para("Nominate %s for %d: %s, high on our index, should lodge %s in the series and return %s"
         % (and_list(picks), yr["decision_sow"], and_list(others), pcts([L[w_]["lodging_pct"] for w_ in others]),
            nums([L[w_]["expected_ry"] for w_ in others])), bold=True, size=14, after=6)
    para("%s are the %s Stage 3 lines we should expect most from in the series: relative yields of %s over two "
         "seasons, against %.1f for the next line, %s. Mount Rouse's standard is %.1f. The 80%% ranges run from %s; "
         "they are ranges for what two seasons return, the seasons drawn as well as what we still do not know about "
         "the lines (%s would run from %.1f to %.1f on the spread of its estimate alone)."
         % (and_list(picks), WORDS[npk], nums([L[w_]["expected_ry"] for w_ in picks]), L[nxt]["expected_ry"], nxt, std,
            and_list(["%.1f to %.1f" % (L[w_]["low"], L[w_]["high"]) for w_ in picks]), picks[0], eo["lo"][0],
            eo["hi"][0]))
    para("The index points elsewhere. It would put up %s, at %s. %s weak-strawed: we expect %s of %s plots to lodge "
         "in the series, against %s for %s, and a relative yield of %s."
         % (and_list(idx3), nums([L[w_]["index"] for w_ in idx3]),
            "%s are" % and_list(others) if len(others) > 1 else "%s is" % others[0],
            pcts([L[w_]["lodging_pct"] for w_ in others]), "their" if len(others) > 1 else "its",
            pcts([L[w_]["lodging_pct"] for w_ in picks]), and_list(picks),
            nums([L[w_]["expected_ry"] for w_ in others])))
    shown = picks + [nxt] + [w_ for w_ in others if w_ != nxt]
    rows = [[w_, "%.1f" % L[w_]["index"], "%.1f" % L[w_]["expected_ry"], "%.1f to %.1f" % (L[w_]["low"], L[w_]["high"]),
             "%d%%" % L[w_]["lodging_pct"]] for w_ in shown]
    tbl(["Line", "Index", "Expected relative yield", "80% range", "Expected lodging"], rows, [28, 26, 42, 38, 34])
    para("Lines in the order above: the %s to nominate, the first left out, the index's other choice%s. "
         "Source: workbook, sheet Stage 3 lines."
         % (WORDS[npk], "s" if len([w_ for w_ in others if w_ != nxt]) > 1 else ""),
         size=8.5, italic=True, after=8, color=(70, 70, 70))
    para("Why the past nominations fell short", bold=True, size=11.5, after=3)
    bm = F["bridge_means"]
    para("The %d nominations with both seasons in were quoted at %.1f on average and returned %.1f, a gap of %.1f "
         "points. Under the deed's four heads: %.1f was the index itself, since lines picked for the highest index "
         "on the Stage 3 list are partly picked on their luck and at the same trials they should have been expected "
         "to give %.1f.\u00b9 %.1f was the move to the Series: before lodging the lines stand %.2f t/ha over Byaduk at "
         "their index trials, where Byaduk yields %.2f t/ha on %d mm of season water, and %.2f t/ha at their Series "
         "trials, where it yields %.2f on %d mm.\u00b2 %.1f was lodging, which costs %.3f t/ha for each tenth of a plot "
         "lodged: the lines lodged %.1f points more than Byaduk at their index trials and %.1f points more in the "
         "Series. The remainder is %.1f."
         % (F["completed_nominations"], F["quoted_mean"], F["realised_mean"], F["shortfall_points"],
            F["overstated_at_own_sites_points"], F["worth_at_own_sites_mean"], F["benchmark_water_response_points"],
            bm["advantage_at_index_trials_t_ha"], bm["byaduk_at_index_trials_t_ha"], bm["water_at_index_trials_mm"],
            bm["advantage_at_series_trials_t_ha"], bm["byaduk_at_series_trials_t_ha"], bm["water_at_series_trials_mm"],
            F["lodging_points"], ev["loss_per_tenth_within"], bm["lodging_over_byaduk_at_index_trials_pct"],
            bm["lodging_over_byaduk_at_series_trials_pct"], F["left_over_points"]))
    doc.add_picture(png, width=Mm(166))
    doc.paragraphs[-1].paragraph_format.space_after = Pt(6)
    wy = F["worst_year"]
    if wy["index_water_mm"] <= ev["water_mm_index_trials"] - 30:
        para("One year shows the second part most plainly: the %d nominations were quoted at %.1f on index trials "
             "that had %d mm of season water in %d, against %d mm over all seasons, and returned %.1f, with %.1f "
             "points going in the move to the Series." % (wy["sow"], wy["quoted"], wy["index_water_mm"], wy["season"],
                                                 ev["water_mm_index_trials"], wy["realised"], wy["water"]))
    else:
        para("One year shows the second part most plainly: the %d nominations were quoted at %.1f and returned "
             "%.1f, with %.1f points going in the move to the Series." % (wy["sow"], wy["quoted"], wy["realised"], wy["water"]))
    para("\u00b9 Relative yield and the index as the series protocol (section 7) and our trial handbook (section 6) define "
         "them; the standard and the review's heads are clauses 2.1 and 4.2 of schedule 2 to the option deed.",
         size=8.5, after=1, color=(70, 70, 70))
    para("² Season water is April to October rain, plus the water applied at Kerang. In the Series' trials Byaduk's "
         "gain over our nominated lines goes with season water (t %.1f); the trial's yield level, entered beside it, "
         "takes the opposite sign (t %.1f)." % (ev["series_lines_joint_water_t"], ev["series_lines_joint_level_t"]),
         size=8.5, after=1, color=(70, 70, 70))
    doc.save(path)
    PP.normalize_docx(path, AUTHOR, AUTHOR, "%d-02-16T04:21:00Z" % Y, "%d-02-17T03:27:00Z" % Y, revision=11,
                      total_time=212, seed=1527, title="HRBS nominations for %d sowing" % Y, company=COMPANY)


def write_all(F, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(F, os.path.join(golden_dir, BOOK))
    png = os.path.join(golden_dir, CHART)
    chart(F, png)
    note(F, os.path.join(golden_dir, NOTE), png)
    return [BOOK, CHART, NOTE]
