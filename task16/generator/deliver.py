"""task16 golden deliverables: HIM's evaluation workbook (each candidate rule's automatic links and false merges, rule
A's chance agreement by community, the converted index, Calder Bay's overlays to split) and its one-page memo to the
health system's executive team, both from the same results that write figures.json."""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Font
from reportlab.lib.styles import ParagraphStyle

import analysis as A
import docs as DC
import postprocess

WORKBOOK = "one_chart_autolink_rule_evaluation.xlsx"
MEMO = "one_chart_autolink_recommendation.pdf"
AUTHOR = "Brenda Hartman"
ORG = "Calder Rosario Health"
LABEL = {"A": "Rule A", "B": "Rule B", "C": "Rule C", "D": "Rule D"}
MWH = "#,##0"


def _hdr(ws, row, cols, widths=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd


def community_table(F, R):
    """Rule A's expected chance merges by surname and birth decade (the largest contributors)."""
    e = A.person_entries(R)
    h = A.heap_rates(e)
    e = e.assign(decade=(e["y"] // 10) * 10).join(h, on=["last", "decade"])
    c = e.groupby(["first", "last", "sex", "y"]).agg(n=("n", "size"), r=("n", "mean"), h1=("h1", "mean"),
                                                     h7=("h7", "mean"), decade=("decade", "first")).reset_index()
    c = c[c["n"] >= 2].copy()
    c["exp"] = c["n"] * (c["n"] - 1) / 2.0 * A.p_same_day(c["h1"].to_numpy(), c["h7"].to_numpy()) * c["r"] ** 2
    g = c.groupby(["last", "decade"]).agg(exp=("exp", "sum"), cells=("exp", "size")).reset_index()
    jan1 = e.groupby(["last", "decade"])["d"].apply(lambda s: (s == "0101").mean())
    g = g.join(jan1.rename("jan1"), on=["last", "decade"])
    return g.sort_values("exp", ascending=False)


def community_shares(F, R):
    """Rule A's expected merges of two different patients: the shares among men born since 1975 and among patients
    born before 1960, and among cells whose community records 1 January for a tenth or more of its births."""
    e = A.person_entries(R)
    h = A.heap_rates(e)
    e = e.assign(decade=(e["y"] // 10) * 10).join(h, on=["last", "decade"])
    c = e.groupby(["first", "last", "sex", "y"]).agg(n=("n", "size"), r=("n", "mean"), h1=("h1", "mean"),
                                                     h7=("h7", "mean")).reset_index()
    c = c[c["n"] >= 2].copy()
    c["exp"] = c["n"] * (c["n"] - 1) / 2.0 * A.p_same_day(c["h1"].to_numpy(), c["h7"].to_numpy()) * c["r"] ** 2
    tot = float(c["exp"].sum())
    return dict(men_since_1975=float(c.loc[(c["sex"] == "M") & (c["y"] >= 1975), "exp"].sum() / tot),
                before_1960=float(c.loc[c["y"] < 1960, "exp"].sum() / tot),
                jan1_heavy=float(c.loc[c["h1"] >= 0.10, "exp"].sum() / tot))


def write(F, G, figs, gold_dir):
    os.makedirs(gold_dir, exist_ok=True)
    R = F["R"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rules"
    ws["A1"] = ("%s is the only candidate rule inside one false merge per 2,000 automatic links (2 November 2026 "
                "indexes)" % LABEL[G["rule"]])
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Rule", "Joins records automatically when", "Automatic links", "False merges (estimate)",
                 "False merges per 2,000 links", "Within the policy (one per 2,000)",
                 "Per 2,000 on the engine's chance rates and the pilot"],
         [7, 62, 12, 14, 14, 14, 18])
    r = 4
    order = sorted(A.RULES, key=lambda k: -G["links"][k])
    for k in order:
        vals = [LABEL[k], DC.RULES[k], G["links"][k], round(G["false"][k], 1), round(G["rate"][k], 2),
                "Yes" if G["rate"][k] <= 1.0 else "No", round(figs["incumbent_rate_per_2000"][k], 2)]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j == 2:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=r, column=3).number_format = MWH
        ws.cell(row=r, column=4).number_format = "0.0"
        ws.cell(row=r, column=5).number_format = "0.00"
        ws.cell(row=r, column=7).number_format = "0.00"
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Run at conversion: %s, the compliant rule that links the most pairs." %
            LABEL[G["rule"]]).font = Font(bold=True)
    ws.cell(row=r + 1, column=1, value=(
        "Rule A's estimate: patients who share a first name, last name, sex and birth year, each pair sharing a birth "
        "date with the chance its surname community's birth dates carry. Rule C's: links between patients that a "
        "delivery, a single registration visit or differing blood groups keep apart. Rule D's: links whose first names "
        "are not forms of one name, or that a delivery or a single visit shows are two children under one SSN."))
    ws.cell(row=r + 1, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=7)
    ws.row_dimensions[r + 1].height = 58
    ws.freeze_panes = "A4"
    # rule A by community
    ws = wb.create_sheet("Rule A by community")
    sh = community_shares(F, R)
    ws["A1"] = ("Rule A's merges of two different patients: %.0f per cent among men born since 1975, %.0f per cent among "
                "patients born before 1960" % (100 * sh["men_since_1975"], 100 * sh["before_1960"]))
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Last name", "Birth decade", "Expected false merges", "Name and year cells", "Born 1 January (share)"],
         [16, 12, 16, 16, 18])
    tab = community_table(F, R)
    for i, row in enumerate(tab.head(40).itertuples(index=False), 4):
        ws.cell(row=i, column=1, value=row.last)
        ws.cell(row=i, column=2, value="%ds" % int(row.decade))
        ws.cell(row=i, column=3, value=round(float(row.exp), 2)).number_format = "0.00"
        ws.cell(row=i, column=4, value=int(row.cells))
        ws.cell(row=i, column=5, value=round(float(row.jan1), 3)).number_format = "0.0%"
    n = 4 + min(40, len(tab))
    ws.cell(row=n + 1, column=1, value="All surnames and decades").font = Font(bold=True)
    ws.cell(row=n + 1, column=3, value=round(G["false"]["A"], 1)).number_format = "0.0"
    m, nz = G["marker"]["A"], G["noise"]
    ws.cell(row=n + 3, column=1, value=(
        "Cross-check: of rule A's links where both records carry blood bank results (%d), %d show groups that differ; "
        "%d of them touch a record holding two patients and about %.0f are mislabelled specimens (%d of %d records "
        "typed twice or more disagree with themselves), leaving about %.0f merges of two patients across rule A's "
        "links at the %.0f per cent chance two patients' groups differ."
        % (m["typed_links"], m["discordant"], m["discordant"] - m["discordant_clear"], m["expected_one_patient_clear"],
           nz["disagreeing"], nz["records"], m["net"], 100 * nz["p_diff"])))
    ws.freeze_panes = "A4"
    # what each check HIM could run gives, beside this evaluation
    ws = wb.create_sheet("Checks")
    ws["A1"] = "The engine's checks pass Rule A; the blood bank results as they read pass no rule"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Check", "Rule A", "Rule B", "Rule C", "Rule D", "Rule the policy would run"], [58, 10, 10, 10, 10, 16])
    mk = G["marker"]
    doc, nz0 = G["documented"], G["noise"]
    direct = {k: (doc[k]["discordant_other_ssn"] / nz0["p_diff"] * doc[k]["links_read"] / max(doc[k]["typed"], 1)
                  + (G["incumbent"][k]["false"] if k in ("A", "B", "D") else 0.0)) for k in A.RULES}
    checks = [
        ("The engine's national chance rates (rules A, B, D) and the 2026 pilot's reviewed pairs (rule C)",
         {k: G["incumbent"][k]["false"] for k in A.RULES}),
        ("Two newborns of one delivery or two records made on one registration visit, counted",
         {k: float(doc[k]["documented_twins"]) for k in A.RULES}),
        ("The national rates, raised by the blood-discordant links whose records carry different SSNs (rule A on the "
         "links rule B does not make)", direct),
        ("Blood bank results on each rule's typed links, as they read", {k: mk[k]["as_read"] for k in A.RULES}),
        ("Blood bank results net of mislabelled specimens", {k: mk[k]["net_of_wbit"] for k in A.RULES}),
        ("Blood bank results net of mislabelled specimens and of records holding two patients",
         {k: mk[k]["net"] for k in A.RULES}),
        ("This evaluation", dict(G["false"])),
    ]
    for i, (lab, f) in enumerate(checks, 4):
        ws.cell(row=i, column=1, value=lab).alignment = Alignment(wrap_text=True, vertical="top")
        for j, k in enumerate(A.RULES, 2):
            ws.cell(row=i, column=j, value=round(float(f[k]), 1)).number_format = "0.0"
        ok = [k for k in A.RULES if 2000.0 * f[k] / G["links"][k] <= 1.0]
        ws.cell(row=i, column=6, value=LABEL[max(ok, key=lambda k: G["links"][k])] if ok else "None (all reviewed)")
    ws.cell(row=12, column=1, value=(
        "The blood bank's results come from the transfusion service, whose patients are mostly over 55, so they see "
        "almost none of the working-age men and children where rule A's chance merges sit, and none of the twins who "
        "share a group; the delivery log holds only births in the two hospitals since 2006. They test each estimate "
        "rather than measure it."))
    ws.cell(row=12, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(start_row=12, start_column=1, end_row=12, end_column=6)
    ws.row_dimensions[12].height = 44
    ws.freeze_panes = "A4"
    # the converted index
    ws = wb.create_sheet("Index")
    ws["A1"] = ("The converted index holds {:,} patients, {:,} of them known to both Calder Bay and Rosario"
                .format(G["persons"], G["both"]))
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Figure", "Value"], [64, 14])
    rows = [("Distinct patients the converted index holds", G["persons"]),
            ("Patients held by both Calder Bay and Rosario", G["both"]),
            ("Calder Bay records holding two or more patients (to split before conversion)", G["overlays"]),
            ("Patients still under more than one active record once %s's links are made" % LABEL[G["rule"]], G["left"]),
            ("%s's links that touch a record holding two or more patients" % LABEL[G["rule"]], G["overlay_links"]["links"]),
            ("Records holding two or more patients those links touch, split before they are made", G["overlay_links"]["records"]),
            ("Active records in the two indexes", len(R))]
    for i, (a_, b_) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=a_)
        ws.cell(row=i, column=2, value=b_).number_format = MWH
    # rule B's blood mismatches, each read against what explains it
    ws = wb.create_sheet("Rule B blood mismatches")
    rb = G["resolve_b"]
    ws["A1"] = ("%s's %d blood mismatches: %d on records holding two patients, %d on records whose own typings disagree, "
                "%d left as false merges" % (LABEL["B"], rb["discordant"], rb["overlay"], rb["mislabel"], rb["left"]))
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Record", "Linked record", "Name", "Birth date", "Groups on the record", "Groups on the linked record",
                 "Same SSN", "Read as"], [14, 14, 28, 12, 16, 18, 10, 46])
    typ = A.typings(F)
    m_, ssn_ = R["mrn"].to_numpy(), R["ssn"].to_numpy()
    ov = set(G["overlay_mrns"])
    i = 4
    for x, y in zip(*G["_links"]["B"]):
        sx, sy = set(t[1] for t in typ.get(m_[x], [])), set(t[1] for t in typ.get(m_[y], []))
        if not sx or not sy or (sx & sy):
            continue
        why = ("a record holding two patients, split before the conversion" if (m_[x] in ov or m_[y] in ov) else
               "a record whose own typings disagree (a mislabelled specimen)" if (len(sx) > 1 or len(sy) > 1) else
               "two patients: a false merge")
        vals = [m_[x], m_[y], "%s, %s" % (R["last"].iloc[x], R["first"].iloc[x]), R["dob"].iloc[x].strftime("%m/%d/%Y"),
                ", ".join(sorted(sx)), ", ".join(sorted(sy)), "Yes" if ssn_[x] and ssn_[x] == ssn_[y] else "No", why]
        for j, v in enumerate(vals, 1):
            ws.cell(row=i, column=j, value=v)
        i += 1
    ws.freeze_panes = "A4"
    # overlays worklist
    ws = wb.create_sheet("Overlays to split")
    ws["A1"] = "%d Calder Bay records hold two or more patients: split before the conversion" % G["overlays"]
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Surviving MRN", "Name on the record", "Birth date"], [16, 30, 12])
    ia = F["index_a"].set_index("MRN")
    for i, mrn in enumerate(G["overlay_mrns"], 4):
        ws.cell(row=i, column=1, value=mrn)
        if mrn in ia.index:
            ws.cell(row=i, column=2, value="%s, %s" % (ia.at[mrn, "LAST_NAME"], ia.at[mrn, "FIRST_NAME"]))
            ws.cell(row=i, column=3, value=ia.at[mrn, "DOB"])
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = "A3:C%d" % (3 + len(G["overlay_mrns"]))
    # notes
    ws = wb.create_sheet("Notes")
    ws["A1"] = "Notes"
    ws["A1"].font = Font(bold=True, size=12)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 100
    notes = [
        ("Automatic link", DC.POLICY_DEFS),
        ("The cap", DC.POLICY_LINK),
        ("Rules", "As section 7.2 of the conversion plan defines them, compared as the matching engine standardizes "
                  "names, addresses, phones and SSNs; every pair of active records across and within the two indexes."),
        ("Sources", "Calder Bay patient index and merge history, Rosario patient index, cut 2 November 2026; blood bank "
                    "type and screen results 2016 to 2026; labor and delivery logs 2006 to 2026; the engine's name "
                    "equivalence table v6 and 2026 pilot review."),
        ("Rounding", "False merges to one decimal where an expectation, whole where a count; per 2,000 links to two."),
    ]
    for i, (k, v) in enumerate(notes, 3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    path = os.path.join(gold_dir, WORKBOOK)
    wb.save(path)
    postprocess.normalize_ooxml(path, AUTHOR, AUTHOR, "2026-11-06T15:20:00Z", "2026-11-09T21:47:00Z", excel=True,
                                company=ORG)
    memo(G, figs, os.path.join(gold_dir, MEMO))
    return path


def memo(G, figs, path):
    assert G["rule"] == "B", "the memo's argument is written for Rule B"
    head = ParagraphStyle("memo_head", parent=DC.BODY, spaceAfter=0, leading=12.4)
    title = ParagraphStyle("memo_title", parent=DC.BODY, fontName="Helvetica-Bold", fontSize=11, spaceBefore=8,
                           spaceAfter=6)
    note = ParagraphStyle("memo_note", parent=DC.BODY, fontName="Helvetica-Oblique", fontSize=8, leading=10)
    f, rt, n = G["false"], G["rate"], G["links"]
    rb, ovl, sh = G["resolve_b"], G["overlay_links"], figs["rule_a_shares"]
    doc = G["documented"]
    story = [DC.P_("Calder Rosario Health  |  Health Information Management", DC.LH),
             DC.P_("To: Calder Rosario Health executive team", head),
             DC.P_("From: Brenda Hartman, Director of Health Information Management", head),
             DC.P_("Date: 9 November 2026", head),
             DC.P_("Automatic linking at the One Chart conversion: run Rule B", title)]
    story.append(DC.P_(
        "Run Rule B (first name, last name, birth date, sex and street address the same) at the 5 April conversion. It "
        "joins %s pairs of records and, by our estimate, %.0f of them are two different patients: %.2f per 2,000 links, "
        "inside the policy's one. Its %d blood-group mismatches do not count against it as they stand: %d sit on Calder "
        "Bay records that already hold two patients, which we split before the conversion, and %d %s left as false "
        "merges, with the twins a single registration visit shows."
        % ("{:,}".format(n["B"]), f["B"], rt["B"], rb["discordant"], rb["overlay"], rb["left"],
           "is" if rb["left"] == 1 else "are")))
    story.append(DC.P_(
        "Rule A, the same without the address, joins %s pairs, and about %.0f would merge two different patients (%.2f "
        "per 2,000). Port Calder's names cluster by community and birth year, and many of the men who came to work the "
        "boats and the yards carry the 1 January birth dates their documents gave them; %.0f per cent of Rule A's chance "
        "merges are among men born since 1975. The engine's national rates put Rule A at %.2f, and the blood bank cannot "
        "see these merges: its patients are mostly over 55."
        % ("{:,}".format(n["A"]), f["A"], rt["A"], 100 * sh["men_since_1975"], figs["incumbent_rate_per_2000"]["A"])))
    story.append(DC.P_(
        "Rule C, which accepts near-identical first names at a shared address or phone, joins %s pairs and would merge "
        "about %.0f pairs of twins (%.2f per 2,000). The delivery log and our registration times show only %d of them: "
        "most twins here were registered on different visits or born before their families moved to Port Calder. Rule D, "
        "on SSN and birth date, joins %s pairs and would merge about %.0f (%.2f per 2,000), mostly twins registered at "
        "Rosario under a parent's SSN before June 2021."
        % ("{:,}".format(n["C"]), f["C"], rt["C"], doc["C"]["documented_twins"], "{:,}".format(n["D"]), f["D"],
           rt["D"])))
    story.append(DC.P_(
        "Before the conversion, HIM splits %d Calder Bay records that already hold two or more patients, merged by its "
        "registration system since March 2019; %d of Rule B's links touch %d of them. The converted index will hold about "
        "%s distinct patients, %s of them known to both groups, and %s will still sit under more than one record once Rule "
        "B runs, for the review worklist." % (G["overlays"], ovl["links"], ovl["records"], "{:,}".format(G["persons"]),
                                              "{:,}".format(G["both"]), "{:,}".format(G["left"]))))
    story.append(DC.P_("Detail, by rule and by community, in the evaluation workbook."))
    story.append(DC.P_("False merges are counted as HIM-14 section 3 counts them, for each pair of records a rule would "
                       "join, on the 2 November 2026 extracts the conversion plan takes as its baseline.", note))
    DC.officepdf.build(path, story, "Automatic linking at the One Chart conversion", AUTHOR,
                       "One Chart automatic linking: the recommended rule",
                       "Calder Rosario Health  |  Health Information Management",
                       dt.datetime(2026, 11, 9, 8, 5, tzinfo=DC.CST), dt.datetime(2026, 11, 9, 16, 31, tzinfo=DC.CST))
