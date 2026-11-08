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
    v = 0.0 if round(v, dp) == 0 else v
    return ("%." + str(dp) + "f") % v


def chart(F, path):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
    fig, ax = plt.subplots(figsize=(6.4, 3.5), dpi=200)
    grid = [100 * g for g in F["grid"]]
    for key, col, label in (("KL", BLUE, "Kestrel Lane portfolio"), ("OS", ORANGE, "Ostvale portfolio")):
        y = [max(100 * v, 1e-3) for v in F["golden"][key]["exceed_raw"]]
        ax.plot(grid, y, color=col, lw=2, label=label, solid_capstyle="round")
    sk, so = F["subordination_pct"]["KL"], F["subordination_pct"]["OS"]
    ax.axvline(sk, color=BLUE, lw=1, ls=(0, (4, 3)))
    ax.axvline(so, color=ORANGE, lw=1, ls=(0, (4, 3)))
    ax.axhline(F["bar_pct"], color=INK2, lw=1, ls=(0, (1, 2)))
    ax.text(sk + 0.3, 40, "Kestrel Lane's subordination, %s%%" % pct(sk, 1), color=INK2, fontsize=7.5, va="center")
    ax.text(so - 0.3, 40, "Ostvale's, %s%%" % pct(so, 1), color=INK2, fontsize=7.5, va="center", ha="right")
    ax.text(29.6, F["bar_pct"] * 1.18, "MP-RN-2 test, %s%%" % pct(F["bar_pct"], 0), color=INK2, fontsize=7.5, ha="right")
    kl, os_ = F["golden"]["KL"]["p5_pct"], F["golden"]["OS"]["p5_pct"]
    ax.plot([sk], [kl], "o", ms=5, color=BLUE, mec="#fcfcfb", mew=1.5)
    ax.plot([so], [os_], "o", ms=5, color=ORANGE, mec="#fcfcfb", mew=1.5)
    ax.annotate("%s%%" % pct(kl, 1), (sk, kl), xytext=(8, 6), textcoords="offset points", color=INK, fontsize=7.5)
    ax.annotate("%s%%" % pct(os_, 1), (so, os_), xytext=(-30, 6), textcoords="offset points", color=INK, fontsize=7.5)
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
    ax.set_title("Both portfolios' losses pass 15 per cent of par more often than the test allows", fontsize=9.5, color=INK,
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
    rg = F["rungs"]
    hp, yl = rg["house_pooled_lgd"], rg["house_year_link"]
    _para(doc, "Buy neither note; both fail MP-RN-2's test", 15, bold=True, after=6)
    _para(doc, ("We recommend declining both offers and leaving the allocation in the cash and government bond sleeve "
                "until the next round, as MP-RN-2 2.2 provides. Over 2027 to 2031 Kestrel Lane's Class A note has a %s "
                "per cent chance of losing principal and Ostvale's a %s per cent chance, against the standard's test of "
                "%s per cent. Kestrel Lane's note looks the safer of the two on its borrowers' ratings, but its loans "
                "sit with %s sponsor houses, and the defaults that cluster in a house's bad year are the ones that "
                "recover least. We expect credit losses over the five years of %s per cent of par on Kestrel Lane's "
                "portfolio and %s per cent on Ostvale's.")
          % (pct(kl["p5_pct"], 1), pct(os_["p5_pct"], 1), pct(F["bar_pct"], 0), word(kl["houses"]),
             pct(kl["el_pct"], 1), pct(os_["el_pct"], 1)), 10)

    rows = [["Note", "Loans", "Par, EUR m", "Subordination", "Chance of loss 2027-31", "Expected loss 2027-31",
             "Needed for 1.0%", "for 0.5%"]]
    for key, nm in (("KL", "Kestrel Lane"), ("OS", "Ostvale")):
        g = G[key]
        rows.append([nm, "%d" % g["n"], "{:,.0f}".format(g["par_eur_m"]), "%s%%" % pct(F["subordination_pct"][key], 1),
                     "%s%%" % pct(g["p5_pct"], 1), "%s%%" % pct(g["el_pct"], 1), "%d%%" % g["need_pct"][0],
                     "%d%%" % g["need_pct"][1]])
    _para(doc, "Table 1. The two notes under MP-RN-2", 9, bold=True, after=2, before=4)
    _table(doc, rows, [24, 12, 18, 22, 24, 24, 22, 18])
    _para(doc, ("Par converted at the ECB reference rate of 31 December 2026. Chances and expected losses from %s "
                "simulated five-year paths, the expected loss as a share of the portfolio's par; subordination needed in "
                "whole per cent of par, rounded up.") % "{:,}".format(F["paths"]),
          7.5, italic=True, color="555555", after=8)

    doc.add_picture(png, width=Mm(160))
    _para(doc, ("Figure 1. Chance that each portfolio's credit loss over 2027 to 2031 exceeds a given share of par. "
                "Kestrel Lane's note starts losing principal at %s per cent and Ostvale's at %s per cent.")
          % (pct(F["subordination_pct"]["KL"], 1), pct(F["subordination_pct"]["OS"], 1)), 7.5, italic=True, color="555555",
          after=10)

    _para(doc, "Defaults cluster by sponsor house", 11.5, bold=True, after=4)
    ev = F["evidence"]
    E = F["estimates"]
    _para(doc, ("Lenderbase records %s company-years of European sponsor-backed first-lien loans from 2008 to 2026, with "
                "%s defaults. Joined to Dealtrail's buyout records, every loan traces to the sponsor house whose fund "
                "held the company. Pairs in the same house, sector and year defaulted together %s per cent of the time "
                "against %s per cent for pairs in the same sector and year under different houses; pairs in the same "
                "house in different years sit at the independence rate. The economy's year carries %s of the variance "
                "of a borrower's standing, the sector's year %s, and the house's year %s of what those leave. Kestrel "
                "Lane's %d loans sit with %s houses and Ostvale's %d with %d.")
          % ("{:,}".format(F["panel"]["company_years"]), "{:,}".format(F["panel"]["defaults"]),
             pct(ev["same_house_same_sector_year_pct"]), pct(ev["other_house_same_sector_year_pct"]),
             pct(E["am"], 3), pct(E["ak"], 3), pct(E["ch"], 3), kl["n"], word(kl["houses"]), os_["n"],
             os_["houses"]), 10)

    _para(doc, "The clustered defaults recover least", 11.5, bold=True, after=4, before=4)
    rb = F["recovery_by_other_defaults"]
    LK, Ly = F["link"], F["link_year_only"]
    L = F["lgd"]
    _para(doc, ("A house in a bad year stops putting money into its companies' restructurings, so lenders sell or wind "
                "up the businesses instead. On the 2008 to 2019 defaults, whose workouts have all closed, a default with "
                "no other default in its house that year recovered %s per cent of the loan; one with three or more "
                "others recovered %s per cent. The recent clustered defaults are not yet in that comparison: they take "
                "longer to work out, and %d workouts are still open. Inferring each house-year's shock from its own "
                "defaults against what its companies' ratings, ages and sector-year expected, and the year's shock "
                "from the year's default rate, recovery on the closed cohorts runs %s plus %s per unit of the year's "
                "shock and %s per unit of the house-year's shock.")
          % (pct(rb["0"]["recovery_pct"], 1), pct(rb["3"]["recovery_pct"], 1), L["open"], pct(LK["a"], 3),
             pct(LK["bm"], 3), pct(LK["bh"], 3)), 10)
    gr, CK, ci = F["grain"], F["count_link"], rg["count_in_portfolio"]
    _para(doc, ("The comparison counts each default's companions across its house's whole book: a default in the record "
                "shared its house-year with a median of %d of the house's companies. Ostvale's tape holds %s companies "
                "of each house and Kestrel Lane's %s. Counted among each note's own loans, Ostvale's defaults would "
                "nearly always look like lone ones and its note would pass at %s per cent, while Kestrel Lane's would "
                "fail at %s; but what a default recovers depends on the year its house is having, not on how many of "
                "the house's loans a note happens to hold, so the house-year's shock carries it into the simulation.")
          % (CK["book_seen_median"], word(int(gr["OS"]["loans_per_house_median"])), word(int(gr["KL"]["loans_per_house_median"])),
             pct(ci["OS"]["p5_pct"], 1), pct(ci["KL"]["p5_pct"], 1)), 10)
    _para(doc, ("Simulated with each default recovering on the shocks that drew it, both notes fail. With one average "
                "loss of %s per cent for every default, as the closed workouts give it, Kestrel Lane's note would pass "
                "at %s per cent and be bought (Ostvale's is at %s); tying recovery to the economy's year leaves Kestrel "
                "Lane at %s per cent, because a default recovers no less in the economy's bad years. It is the "
                "house's year, which also clusters Kestrel Lane's defaults, that takes its tail past the test.")
          % (pct(L["lgd_pct"], 1), pct(hp["KL"]["p5_pct"], 1), pct(hp["OS"]["p5_pct"], 1), pct(yl["KL"]["p5_pct"], 1)), 10)
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    cb = rg["count_whole_book"]
    _para(doc, ("Estimated other ways, the default rates from a cohort table, the dependence from pair counts, or each "
                "house-year's shock read against the year's rates rather than the sector-year's, the chances run %s to "
                "%s per cent for Kestrel Lane and %s to %s per cent for Ostvale; the record's co-default counts taken "
                "over each house's whole book give %s and %s per cent. No sound estimate brings either note under the "
                "test. Fitting the link on every closed workout instead of the closed cohorts would leave out the open "
                "workouts, which MP-RN-2 4.1 keeps and which are the clustered defaults' long ones.")
          % (pct(bk[0], 1), pct(bk[1], 1), pct(bo[0], 1), pct(bo[1], 1), pct(cb["KL"]["p5_pct"], 1), pct(cb["OS"]["p5_pct"], 1)), 10)

    _para(doc, "Table 2. Chance that the note has taken a loss by the end of each year", 9, bold=True, after=2, before=6)
    rows = [["", "2027", "2028", "2029", "2030", "2031"]]
    for key, nm in (("KL", "Kestrel Lane"), ("OS", "Ostvale")):
        rows.append([nm] + ["%s%%" % pct(v, 1) for v in G[key]["by_year_pct"]])
    _table(doc, rows, [30, 22, 22, 22, 22, 22])
    _para(doc, ("Portfolios held as they stood on 31 December 2026 with repaid loans replaced, as MP-RN-2 3.2 sets out. "
                "Sources: Lenderbase extract of 16 February 2027 and its workout file, Dealtrail extract of 15 February "
                "2027, managers' tapes at 31 December 2026."), 7.5, italic=True, color="555555", after=8)
    _para(doc, ("To meet the test, Kestrel Lane's note would need %d per cent subordination against the %s it offers, "
                "and Ostvale's %d per cent against its %s. Either manager may re-offer at that level in the next round.")
          % (kl["need_pct"][0], pct(F["subordination_pct"]["KL"], 1), os_["need_pct"][0],
             pct(F["subordination_pct"]["OS"], 1)), 10)
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
                            "%d-12-31" % y, pct(v, 1)])


def write(F, out, scratch):
    os.makedirs(out, exist_ok=True)
    png = os.path.join(scratch, "figure1.png")
    chart(F, png)
    ic_note(F, os.path.join(out, "ic_note_senior_notes_2027.docx"), png)
    by_year_csv(F, os.path.join(out, "senior_note_loss_by_year.csv"))
