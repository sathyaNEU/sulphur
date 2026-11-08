"""task9: the golden deliverables, written from figures.json: the investment committee note (DOCX, with its chart)
and the year-by-year chances (CSV). Every number comes from the analysis; nothing is typed."""
import csv
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402

import ooxml  # noqa: E402

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
FONT = "Calibri"


def pct(v, dp=2):
    return ("%." + str(dp) + "f") % v


def chart(F, path):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
    fig, ax = plt.subplots(figsize=(6.4, 3.5), dpi=200)
    grid = [100 * g for g in F["grid"]]
    for key, col, label in (("KL", BLUE, "Kestrel Lane portfolio"), ("OS", ORANGE, "Ostvale portfolio")):
        y = [max(100 * v, 1e-3) for v in F["golden"][key]["exceed_raw"]]
        ax.plot(grid, y, color=col, lw=2, label=label, solid_capstyle="round")
    sub = F["subordination_pct"]["KL"]
    ax.axvline(sub, color=INK2, lw=1, ls=(0, (4, 3)))
    ax.axhline(F["bar_pct"], color=INK2, lw=1, ls=(0, (1, 2)))
    ax.text(sub + 0.3, 40, "both notes' subordination, %s%%" % pct(sub, 1), color=INK2, fontsize=7.5, va="center")
    ax.text(29.6, F["bar_pct"] * 1.18, "MP-RN-2 test, %s%%" % pct(F["bar_pct"], 0), color=INK2, fontsize=7.5, ha="right")
    kl, os_ = F["golden"]["KL"]["p5_pct"], F["golden"]["OS"]["p5_pct"]
    ax.plot([sub], [kl], "o", ms=5, color=BLUE, mec="#fcfcfb", mew=1.5)
    ax.plot([sub], [os_], "o", ms=5, color=ORANGE, mec="#fcfcfb", mew=1.5)
    ax.annotate("%s%%" % pct(kl), (sub, kl), xytext=(8, 6), textcoords="offset points", color=INK, fontsize=7.5)
    ax.annotate("%s%%" % pct(os_), (sub, os_), xytext=(8, -11), textcoords="offset points", color=INK, fontsize=7.5)
    ax.set_yscale("log")
    ax.set_ylim(0.01, 100)
    ax.set_xlim(0, 30)
    ax.set_yticks([0.01, 0.1, 1, 10, 100])
    ax.set_yticklabels(["0.01%", "0.1%", "1%", "10%", "100%"])
    ax.set_xticks(range(0, 31, 5))
    ax.set_xticklabels(["%d%%" % v for v in range(0, 31, 5)])
    ax.set_xlabel("Credit loss on the portfolio over 2027 to 2031, share of par")
    ax.set_ylabel("Chance the loss is exceeded")
    ax.grid(True, which="major", color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="lower left", fontsize=7.5)
    ax.set_title("Kestrel Lane's losses run further into the tail past 10 per cent of par", fontsize=9.5, color=INK,
                 loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=200, metadata={"Software": None})
    plt.close(fig)


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def word(n):
    return WORDS.get(n, "%d" % n)


def _page_field(par):
    r = par.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), kind)
            r._r.append(f)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = txt
            r._r.append(it)
    r.font.size, r.font.name = Pt(7.5), FONT


def _cell(c, text, bold=False, align=None, size=9):
    c.text = ""
    p = c.paragraphs[0]
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = FONT
    if align == "r":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def _rule(cell):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    e = OxmlElement("w:bottom")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), "6")
    e.set(qn("w:color"), "555555")
    b.append(e)
    tcpr.append(b)


def _para(doc, text, size=10, bold=False, italic=False, color=None, after=6, before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = FONT
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return p


def _table(doc, rows, widths, right_from=1):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.width = Mm(widths[j])
            _cell(c, v, bold=(i == 0), align="r" if (j >= right_from and i > 0) else None, size=8.2 if i == 0 else 8.8)
            if i == 0:
                _rule(c)
    return t


def ic_note(F, path, png):
    G, D = F["golden"], F["default_path"]
    kl, os_ = G["KL"], G["OS"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(10)
    hp = sec.header.paragraphs[0]
    hr = hp.add_run("Kadeweg Fiduciair Beheer | Investment committee paper IC-2027-03 | Confidential")
    hr.font.size, hr.font.name = Pt(7.5), FONT
    hr.font.color.rgb = RGBColor.from_string("666666")
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run("PHL matching portfolio, senior note purchase, February 2027\tPage ")
    fr.font.size, fr.font.name = Pt(7.5), FONT
    fr.font.color.rgb = RGBColor.from_string("666666")
    _page_field(fp)

    _para(doc, "To: Board of trustees, Stichting Pensioenfonds Havenbedrijf en Logistiek, through the investment committee",
          9, after=0)
    _para(doc, "From: Ilse Lips, head of credit, Kadeweg Fiduciair Beheer", 9, after=0)
    _para(doc, "Date: 18 February 2027, for the investment committee of 25 February and the board of 4 March 2027",
          9, after=0)
    _para(doc, "Subject: Class A senior notes offered by Kestrel Lane and Ostvale, under MP-RN-2", 9, after=10)
    _para(doc, "Buy Ostvale's Class A note; Kestrel Lane's fails the standard", 15, bold=True, after=6)
    _para(doc, ("We recommend subscribing to the Class A notes of Ostvale Senior Secured Note 2027-1. Over 2027 to 2031 "
                "its chance of losing any principal is %s per cent, inside MP-RN-2's test of %s per cent. Kestrel "
                "Lane's KLCP Senior Loan Note 2027 has a %s per cent chance and fails the test, although its "
                "portfolio is spread over more industries and carries better ratings. The difference comes from the "
                "sponsor houses behind the borrowers: Kestrel Lane's %d loans sit with %s houses, Ostvale's %d loans "
                "with %d.")
          % (pct(os_["p5_pct"]), pct(F["bar_pct"], 0), pct(kl["p5_pct"]), kl["n"], word(kl["houses"]), os_["n"],
             os_["houses"]), 10)

    rows = [["Note", "Loans", "Par, EUR m", "Subordination", "Chance of loss 2027-31", "Needed for 1.0%",
             "for 0.5%", "for 0.25%"]]
    for key, nm in (("KL", "Kestrel Lane"), ("OS", "Ostvale")):
        g = G[key]
        rows.append([nm, "%d" % g["n"], "{:,.0f}".format(g["par_eur_m"]), "%s%%" % pct(F["subordination_pct"][key], 1),
                     "%s%%" % pct(g["p5_pct"]), "%s%%" % pct(g["need_pct"][0], 1), "%s%%" % pct(g["need_pct"][1], 1),
                     "%s%%" % pct(g["need_pct"][2], 1)])
    _para(doc, "Table 1. The two notes under MP-RN-2", 9, bold=True, after=2, before=4)
    _table(doc, rows, [24, 12, 18, 25, 25, 23, 16, 16])
    _para(doc, "Par converted at the ECB reference rate of 31 December 2026. Chances from %s simulated five-year paths."
          % "{:,}".format(F["paths"]), 7.5, italic=True, color="555555", after=8)

    doc.add_picture(png, width=Mm(160))
    _para(doc, ("Figure 1. Chance that each portfolio's credit loss over 2027 to 2031 exceeds a given share of par. "
                "Both notes start losing principal at 15.0 per cent."), 7.5, italic=True, color="555555", after=10)

    _para(doc, "Why Kestrel Lane's note fails", 11.5, bold=True, after=4)
    ev = F["evidence"]
    _para(doc, ("Lenderbase records %s company-years of European sponsor-backed first-lien loans from 2008 to 2026, with "
                "%s defaults. Joined to Dealtrail's buyout records, every loan can be traced to the buyout that began "
                "the ownership it sits in and to the sponsor house whose fund bought the company. Within a year, "
                "companies held by the same house default together far more often than their industry and the year "
                "explain: pairs in the same house, sector and year defaulted together %s per cent of the time against "
                "%s per cent for pairs in the same sector and year under different houses. Pairs in the same house "
                "but different years defaulted together %s per cent of the time, the rate independence gives (%s per "
                "cent), so this is a shared bad year, not a weak house.")
          % ("{:,}".format(F["panel"]["company_years"]), "{:,}".format(F["panel"]["defaults"]),
             pct(ev["same_house_same_sector_year_pct"]), pct(ev["other_house_same_sector_year_pct"]),
             pct(ev["same_house_other_year_pct"], 3), pct(ev["independent_pair_pct"], 3)), 10)
    E = F["estimates"]
    _para(doc, ("We modelled the dependence as MP-RN-2 section 4.2 asks, correlated credit standings estimated from the "
                "record: the economy's year accounts for %s of the variance of a borrower's standing, its sector's "
                "year for %s, and its sponsor house's year for %s of what the economy and sector leave (%s of the "
                "whole). Grouping by fund instead of house fits the record worse, as does a lasting house or fund "
                "effect, because companies in different funds of one house fail in the same years too.")
          % (pct(E["am"], 3), pct(E["ak"], 3), pct(E["ch"], 3), pct(E["ah"], 3)), 10)
    _para(doc, ("Kestrel Lane is the house lender to its sponsors: its %d loans come from %d funds of %s houses, about "
                "%d loans a house, so one house's bad year can take out several of its loans at once. Ostvale "
                "lends in five sectors but across %d houses. A model that links defaults only through the economy and "
                "the sector, the usual set-up, gives Kestrel Lane %s per cent and Ostvale %s per cent and would "
                "have us buy Kestrel Lane; it passes its own back-test on the record's yearly and sector default "
                "counts, because across eighty houses the house years average out. It does not survive the pairs "
                "above, and it understates exactly the portfolio that is concentrated in a few houses.")
          % (kl["n"], kl["funds"], word(kl["houses"]), round(kl["n"] / kl["houses"]), os_["houses"],
             pct(D["KL"]["p5_pct"]), pct(D["OS"]["p5_pct"])), 10)
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    _para(doc, ("The estimates carry their own uncertainty. Taking the default rates from a cohort table instead of a "
                "probit, or the dependence from pair counts instead of a random effect, moves Kestrel Lane's chance "
                "between %s and %s per cent and Ostvale's between %s and %s per cent; neither range crosses the test.")
          % (pct(bk[0], 1), pct(bk[1], 1), pct(bo[0], 1), pct(bo[1], 1)), 10)
    _para(doc, "Loss on default", 11.5, bold=True, after=4, before=4)
    L = F["lgd"]
    _para(doc, ("Each default loses %s per cent of the loan, the average shortfall over the %d workouts on defaults from "
                "2008 to 2019, all of them closed. Averaging every closed workout instead gives %s per cent, because "
                "%d workouts on later defaults are still open and they are the long ones, which recover less; using it "
                "would put Kestrel Lane's chance at %s per cent and Ostvale's at %s per cent.")
          % (pct(L["lgd_pct"], 1), L["n_mature"], pct(L["lgd_closed_pct"], 1), L["open"],
             pct(F["rungs"]["closed_lgd"]["KL"]["p5_pct"]), pct(F["rungs"]["closed_lgd"]["OS"]["p5_pct"])), 10)

    _para(doc, "Table 2. Chance that the note has taken a loss by the end of each year", 9, bold=True, after=2, before=6)
    rows = [["", "2027", "2028", "2029", "2030", "2031"]]
    for key, nm in (("KL", "Kestrel Lane"), ("OS", "Ostvale")):
        rows.append([nm] + ["%s%%" % pct(v) for v in G[key]["by_year_pct"]])
    _table(doc, rows, [30, 22, 22, 22, 22, 22])
    _para(doc, ("Portfolios held as they stood on 31 December 2026 with repaid loans replaced, as MP-RN-2 3.2 sets out; "
                "default chances by rating and years since each company's buyout, from Lenderbase. Sources: Lenderbase "
                "extract of 16 February 2027, Dealtrail extract of 15 February 2027, managers' tapes at 31 December 2026."),
          7.5, italic=True, color="555555", after=8)
    _para(doc, ("Kestrel Lane's note would need %s per cent subordination to meet the test, against the %s per cent "
                "offered. We have not asked Kestrel Lane to restructure: the offer closes on 12 March and Ostvale's "
                "note meets the standard as offered.")
          % (pct(kl["need_pct"][0], 1), pct(F["subordination_pct"]["KL"], 1)), 10)
    doc.core_properties.author = "Ilse Lips"
    doc.core_properties.title = "IC-2027-03 Senior note purchase"
    doc.core_properties.last_modified_by = "Ilse Lips"
    doc.save(path)
    ooxml.normalize(path, dt.datetime(2027, 2, 16, 8, 2), dt.datetime(2027, 2, 18, 16, 47), creator="Ilse Lips",
                    company="Kadeweg Fiduciair Beheer")


def by_year_csv(F, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["note", "issuer", "subordination_pct", "year_end", "chance_of_loss_pct"])
        for key, nm in (("KL", "KLCP Senior Loan Note 2027 DAC Class A"), ("OS", "Ostvale Senior Secured Note 2027-1 S.A. Class A")):
            for y, v in zip(range(2027, 2032), F["golden"][key]["by_year_pct"]):
                w.writerow([{"KL": "Kestrel Lane", "OS": "Ostvale"}[key], nm, pct(F["subordination_pct"][key], 1),
                            "%d-12-31" % y, pct(v)])


def write(F, out, scratch):
    os.makedirs(out, exist_ok=True)
    png = os.path.join(scratch, "figure1.png")
    chart(F, png)
    ic_note(F, os.path.join(out, "ic_note_senior_notes_2027.docx"), png)
    by_year_csv(F, os.path.join(out, "senior_note_loss_by_year.csv"))
