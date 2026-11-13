"""task16: the documents in the pack, each a Word document its issuing office exported to PDF (officepdf): the
matching engine's specification for the Calder Rosario implementation, the HIM patient identity policy, and the One
Chart conversion plan's EMPI section with the candidate automatic linking rules."""
import datetime as dt

import numpy as np
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf
import records as RC

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.0, spaceAfter=0, leading=9.8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")
CDT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))

# filed sentences the checks and the verifier read back
POLICY_LINK = ("Automatic linking may be enabled at the conversion only under a rule whose expected false merges are no "
               "more than one per 2,000 automatic links, counting each pair of records the rule would join. Where more "
               "than one rule meets this, the conversion uses the rule that joins the most pairs; where none does, every "
               "link is made after HIM review.")
POLICY_DEFS = ("A patient's record is a record registered for that patient. An automatic link joins two patient records "
               "with no human review. A false merge is an automatic link between the records of two different patients. A "
               "record that also holds the information of another patient is an overlay. A patient held under more than "
               "one active record is a duplicate.")
RULES = {
    "A": "first name, last name, birth date and sex all the same",
    "B": "Rule A, and the same street address",
    "C": ("last name, birth date and sex the same; first names the same, equivalent in the engine's name equivalence "
          "table, or with a Jaro-Winkler similarity of 0.92 or more; and the same street address or the same phone number"),
    "D": "the same SSN and the same birth date",
}
PLAN_SCOPE = ("Each candidate rule is applied to every pair of active records in the two indexes, across and within each "
              "index, as the indexes stand at the conversion; the 2 November 2026 extracts are the planning baseline.")


def P_(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P_(str(c), CELL) if not hasattr(c, "wrap") else c for c in r] for r in rows],
                 colWidths=[w * 72 / 25.4 for w in widths_mm])


def spec(path):
    lab = {"exact": "Exact", "equiv": "Equivalent", "similar": "Similar", "diff": "Different", "partial": "Partial",
           "same": "Same"}
    rows = [["Field", "Level", "m", "u", "Weight"]]
    for f, levels in RC.VENDOR.items():
        for lv, (m, u) in levels.items():
            rows.append([{"first": "First name", "last": "Last name", "dob": "Birth date", "sex": "Sex",
                          "addr": "Street address", "phone": "Phone", "ssn": "SSN"}[f], lab[lv],
                         "%.4f" % m, ("%.7f" % u).rstrip("0"), "%+.1f" % np.log2(m / u)])
    story = [
        P_("Halvard Identity  |  Halvard Match 6", LH),
        P_("Matching specification: Calder Rosario Health enterprise master patient index", TITLE),
        P_("Prepared by Felicia Soto, Implementation Consultant. Version 6.2, 14 April 2026."),
        P_("1. What the engine compares", H2),
        P_("Halvard Match compares two patient records field by field and adds the weight of each field's outcome into "
           "a score. Before comparing, the engine standardizes each record: names are upper-cased with accents and "
           "punctuation removed and hyphens read as spaces; a last name is compared as a whole and token by token; "
           "street addresses are reduced to house number, street name and suffix in USPS abbreviations, with unit "
           "designators removed; phone numbers to ten digits; SSNs to nine digits, with all-zero and all-nine values "
           "treated as missing."),
        P_("First names are Exact when the standardized names are the same, Equivalent when the Name Equivalence Table "
           "v6 lists them as forms of one name, and Similar at a Jaro-Winkler similarity of 0.88 or more. Last names are "
           "Partial when they share a token and Similar at 0.90 or more. A birth date is Partial when day and month are "
           "transposed, or month and day agree, or year and month agree. A field missing from either record adds no "
           "weight."),
        P_("2. Weights", H2),
        P_("Each level's weight is log2(m/u), where m is the chance the level is seen when both records belong to one "
           "patient and u the chance it is seen when they belong to two different people. Both come from Halvard's "
           "national reference file (2024 release)."),
        T(rows, [30, 24, 20, 26, 18]),
        Spacer(1, 6),
        P_("3. Decisions", H2),
        P_("An exact pass links records whose first name, last name, birth date and sex are all Exact before any "
           "pair is scored. Scored pairs at or above 31.0 are linked; pairs from 19.0 up to 31.0 go to a review "
           "worklist; pairs below 19.0 are not linked. Candidate pairs are drawn by birth date, by SSN, by phone and by "
           "the first four letters of the last name with the birth year."),
        P_("At the national reference rates, two different people agree on first name, last name, birth date and sex "
           "with a chance of about one in 10 billion pairs."),
    ]
    officepdf.build(path, story, "Halvard Match 6: matching specification", "Felicia Soto",
                    "Calder Rosario Health EMPI implementation", "Halvard Identity  |  Halvard Match 6 specification",
                    dt.datetime(2026, 4, 14, 9, 20, tzinfo=CDT), dt.datetime(2026, 4, 20, 16, 45, tzinfo=CDT),
                    page_of=True, producer="LibreOffice 26.2")


def policy(path):
    story = [
        P_("Calder Rosario Health  |  Health Information Management", LH),
        P_("HIM-14: Patient identity integrity", TITLE),
        P_("Effective 1 July 2026. Owner: Brenda Hartman, Director of Health Information Management. Approved by the "
           "One Chart steering committee on 23 June 2026."),
        P_("1. Scope", H2),
        P_("This policy governs the enterprise master patient index of Calder Rosario Health and the patient records it "
           "joins, including the conversion of the Calder Bay and Rosario indexes into One Chart."),
        P_("2. Definitions", H2),
        P_(POLICY_DEFS),
        P_("3. Automatic linking", H2),
        P_(POLICY_LINK),
        P_("4. Overlays and duplicates", H2),
        P_("Every overlay found before the conversion is split before the conversion, with each patient's encounters, "
           "results and documents returned to that patient's own record. Duplicates left after automatic linking are "
           "worked by HIM from the review worklist."),
        P_("5. Records", H2),
        P_("HIM keeps the merge and split history of both indexes for the life of the record."),
    ]
    officepdf.build(path, story, "HIM-14 Patient identity integrity", "Brenda Hartman",
                    "Patient identity integrity policy", "Calder Rosario Health  |  HIM-14",
                    dt.datetime(2026, 6, 23, 14, 5, tzinfo=CDT), dt.datetime(2026, 6, 29, 10, 12, tzinfo=CDT),
                    producer="LibreOffice 26.2")


def plan(path):
    rows = [["Rule", "Records are joined automatically when"]] + [[k, v] for k, v in RULES.items()]
    story = [
        P_("One Chart program office", LH),
        P_("One Chart conversion plan, section 7: the enterprise master patient index", TITLE),
        P_("Version 1.3, 12 October 2026. Richard Wood, Program Director."),
        P_("7.1 Timeline", H2),
        P_("Calder Bay Health and Rosario Medical Group convert to One Chart over the weekend of 3 to 5 April 2027; "
           "One Chart goes live on Monday 5 April 2027. Both patient indexes load into the Halvard enterprise master "
           "patient index during the conversion weekend."),
        P_("7.2 Candidate automatic linking rules", H2),
        P_("The steering committee will decide at its December 2026 meeting whether the conversion links records "
           "automatically, and under which of these rules, under HIM-14. Fields are compared as the matching engine "
           "standardizes them."),
        T(rows, [14, 150]),
        Spacer(1, 6),
        P_(PLAN_SCOPE),
        P_("7.3 Review", H2),
        P_("Pairs not joined automatically are worked by HIM from the engine's review worklist. Contract reviewers "
           "start in January 2027."),
    ]
    officepdf.build(path, story, "One Chart conversion plan, section 7", "Richard Wood", "Enterprise master patient index",
                    "One Chart program office  |  Conversion plan v1.3",
                    dt.datetime(2026, 10, 12, 11, 30, tzinfo=CDT), dt.datetime(2026, 10, 19, 15, 4, tzinfo=CDT))
