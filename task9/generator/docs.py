"""task9 documents: PHL's standard for senior rated notes and the two managers' indicative term sheets, each a Word
document exported by LibreOffice Writer the way the issuing office writes it."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O

CET = dt.timezone(dt.timedelta(hours=1))
SUB = {"KL": 0.150, "OS": 0.165}   # the enhancement each manager offers below its Class A notes
GMT = dt.timezone(dt.timedelta(hours=0))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=10.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Stichting Pensioenfonds Havenbedrijf en Logistiek", small),
         Paragraph("Matching portfolio: standard for senior rated notes (MP-RN-2)", h1),
         Paragraph("Adopted by the board of trustees on 18 November 2026 on the advice of the investment committee. "
                   "Replaces MP-RN-1 of 14 March 2024. Prepared by Kadeweg Fiduciair Beheer, the fund's fiduciary "
                   "manager.", small),
         Spacer(1, 6),
         Paragraph("1. Scope", h2),
         Paragraph("This standard applies whenever the matching portfolio buys a senior note backed by a static "
                   "portfolio of loans. It sets the one test such a note has to pass and how the fund chooses between "
                   "notes offered for the same allocation.", body),
         Paragraph("2. The test", h2),
         Paragraph("2.1 The fund buys a note only if the chance that it loses any principal in the five calendar years "
                   "from its portfolio date is below 1.0 per cent.", body),
         Paragraph("2.2 Where more than one note offered for the same allocation passes 2.1, the fund buys the one with "
                   "the lower chance. Where none passes, the allocation stays in the cash and government bond sleeve "
                   "until the next round of offers.", body),
         Paragraph("3. Terms", h2),
         Paragraph("3.1 Portfolio date: the cut-off of the collateral tape the manager supplies with its offer.", body),
         Paragraph("3.2 Portfolio: the loans in that tape, each held for the five years with the same borrower, amount "
                   "and terms as on the portfolio date. A loan repaid early is taken to be replaced by an identical loan to "
                   "the same borrower. Borrowers and loans grow older as the years pass. Amounts are converted to euros at "
                   "the European Central Bank reference rate of the portfolio date.", body),
         Paragraph("3.3 Default: a payment default, an insolvency or a distressed restructuring, as Lenderbase records "
                   "them.", body),
         Paragraph("3.4 Loss: a loan that defaults loses its amount times the share of it that is not recovered by the "
                   "end of its workout, booked in the year of the default. A loan that has defaulted leaves the "
                   "portfolio and is not replaced. Interest, fees and excess spread are left out.", body),
         Paragraph("3.5 Subordination: the share of the portfolio's par that ranks below the note. A note loses "
                   "principal when the portfolio's cumulative loss exceeds its subordination.", body),
         Paragraph("4. The record", h2),
         Paragraph("4.1 Default and recovery are taken from the record of comparable loans: the European sponsor-backed "
                   "first-lien mid-market loans in the Lenderbase database that Kadeweg licenses, from 2008 to the latest "
                   "full year, with Lenderbase's workout file, its open workouts included: a default whose workout is "
                   "still open counts as a default, and what lenders recover is read from the default years whose "
                   "workouts have all closed. The five years are taken to "
                   "be drawn from the same conditions as that record.", body),
         Paragraph("4.2 A borrower defaults in a year when its credit standing falls below the point its one-year "
                   "default chance sets. Credit standings are normally distributed and are correlated as far as the "
                   "record of comparable loans shows them to be, and so is what lenders recover on the loans that "
                   "default.", body),
         Paragraph("5. Review", h2),
         Paragraph("Kadeweg reviews this standard every year and after any change in the matching portfolio's "
                   "liabilities. Changes take effect when the board adopts them.", body),
         Spacer(1, 10),
         _grid([["Document", "MP-RN-2"], ["Owner", "Board of trustees, Stichting Pensioenfonds Havenbedrijf en Logistiek"],
                ["Approved by", "Damian Schenkel, chair of the board of trustees"],
                ["Prepared by", "Ilse Lips, Kadeweg Fiduciair Beheer"], ["Next review", "November 2027"]],
               [110, 350], cell)]
    O.build(path, s, "MP-RN-2 Standard for senior rated notes", "Kadeweg Fiduciair Beheer",
            "Matching portfolio, senior rated notes", "PHL | MP-RN-2 | adopted 18 November 2026",
            dt.datetime(2026, 11, 18, 16, 40, tzinfo=CET), dt.datetime(2026, 11, 18, 16, 52, tzinfo=CET))


def term_sheet(path, who, par_eur_m, n_loans):
    body, h1, h2, small, cell = _styles()
    note = par_eur_m * (1.0 - SUB[who])
    if who == "KL":
        rows = [["Term", "Summary"],
                ["Issuer", "KLCP Senior Loan Note 2027 DAC, a designated activity company incorporated in Ireland"],
                ["Collateral manager", "Kestrel Lane Credit Partners LLP (authorised and regulated by the FCA)"],
                ["Class A Notes", "EUR {:,.1f} million senior secured floating rate notes due 2034".format(note)],
                ["Subordination", "%.1f per cent of the aggregate par of the collateral, as the request for proposals of " % (100 * SUB["KL"]) +
                                  "2 October 2026 asked, provided by the Class B Notes and the subordinated notes retained "
                                  "by the collateral manager"],
                ["Interest", "Three-month EURIBOR plus 2.15 per cent a year, payable quarterly on 15 January, April, "
                             "July and October"],
                ["Collateral", "%d first-lien senior secured loans to European sponsor-backed mid-market borrowers, about "
                               "EUR {:,.0f} million par at the cut-off of 31 December 2026, as listed in "
                               "klcp_static_portfolio_2026-12-31.xlsx".format(par_eur_m) % n_loans],
                ["Replenishment", "Until 31 December 2031 principal repaid on a loan is lent again to the same borrower or "
                                  "held in the principal account; no new obligors may be added"],
                ["Portfolio limits", "No obligor above 2.5 per cent and no industry above 15 per cent of aggregate par"],
                ["Maturity", "Expected final 15 January 2032; legal final maturity 15 January 2034"],
                ["Risk retention", "The collateral manager holds a 5 per cent vertical slice (EU Securitisation Regulation, "
                                   "article 6)"],
                ["Listing and law", "Euronext Dublin; Irish law"],
                ["Timetable", "Indicative; orders by 12 March 2027, settlement 26 March 2027"]]
        s = [Paragraph("Kestrel Lane Credit Partners LLP, London", small), Spacer(1, 6),
             Paragraph("KLCP Senior Loan Note 2027 DAC", h1),
             Paragraph("Summary of principal terms, for Kadeweg Fiduciair Beheer on behalf of Stichting Pensioenfonds "
                       "Havenbedrijf en Logistiek. 8 December 2026.", small),
             Spacer(1, 8), _grid(rows, [108, 352], cell), Spacer(1, 8),
             Paragraph("This summary is for discussion with professional investors and is subject to the final offering "
                       "circular. The collateral tape is the collateral manager's record at the cut-off.", small)]
        O.build(path, s, "KLCP Senior Loan Note 2027 DAC summary of terms", "Kestrel Lane Credit Partners",
                "Class A Notes offer", "Kestrel Lane Credit Partners | Strictly private and confidential",
                dt.datetime(2026, 12, 8, 11, 5, tzinfo=GMT), dt.datetime(2026, 12, 8, 11, 19, tzinfo=GMT))
        return
    paras = [
        ("1. Issuer", "Ostvale Senior Secured Note 2027-1 S.A., a Luxembourg securitisation company acting for its "
                      "compartment 2027-1."),
        ("2. Arranger and servicer", "Ostvale Capital AB, Stockholm, which originated and services the loans."),
        ("3. Notes offered", "Class A senior secured notes, EUR {:,.1f} million, floating rate.".format(note)),
        ("4. Credit enhancement", "The Class B notes and the equity retained by Ostvale together equal %.1f per cent of the " % (100 * SUB["OS"]) +
                                  "collateral principal balance, above the 15.0 per cent Kadeweg's request for proposals of 2 "
                                  "October 2026 set, and absorb losses before the Class A notes."),
        ("5. Interest", "Three-month EURIBOR plus 255 basis points a year, quarterly in arrear."),
        ("6. Collateral", "%d first-lien loans to sponsor-backed companies in Europe, EUR {:,.0f} million principal at "
                          "31 December 2026, set out in ostvale_collateral_tape_20261231.xlsx.".format(par_eur_m) % n_loans),
        ("7. Reinvestment", "Until the end of 2031 a repaid loan may be relent to the same borrower; otherwise the cash is "
                            "held. No borrower may be added."),
        ("8. Eligibility", "No borrower above 2.0 per cent and no industry group above 30 per cent of the principal "
                           "balance."),
        ("9. Maturity", "Expected 15 January 2032; final legal maturity 15 January 2034."),
        ("10. Retention", "Ostvale retains a 5 per cent first-loss tranche under article 6 of the EU Securitisation "
                          "Regulation."),
        ("11. Law", "Luxembourg law; notes cleared through Euroclear and Clearstream."),
        ("12. Timing", "Subscriptions close 12 March 2027; settlement on or about 26 March 2027.")]
    s = [Paragraph("OSTVALE CAPITAL", h2), Paragraph("Ostvale Capital AB, Stockholm", small), Spacer(1, 4),
         Paragraph("Indicative term sheet: Ostvale Senior Secured Note 2027-1", h1),
         Paragraph("Addressee: Kadeweg Fiduciair Beheer for Stichting Pensioenfonds Havenbedrijf en Logistiek. Dated 11 "
                   "December 2026.", small), Spacer(1, 6)]
    for head, txt in paras:
        s.append(Paragraph("<b>%s.</b> %s" % (head.rstrip("."), txt), body))
    s += [Spacer(1, 6), Paragraph("Indicative only. Final terms will be set out in the prospectus of the compartment.", small)]
    O.build(path, s, "Ostvale Senior Secured Note 2027-1 indicative term sheet", "Ostvale Capital",
            "Class A senior secured notes", "Ostvale Capital AB | indicative terms",
            dt.datetime(2026, 12, 11, 14, 30, tzinfo=CET), dt.datetime(2026, 12, 11, 14, 44, tzinfo=CET))
