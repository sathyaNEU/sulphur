"""task24: figures.json, effort.json, the golden workbook and the golden note, all from one computed object."""
import datetime as dt
import json

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import golden as GD
import postprocess as PP
import world as Wd

REQ = "ABCDE"
NAMES = {"A": "Corvane Mobility CRV-2027-014", "B": "Shelfgrid Retail SG27-03", "C": "Ardley Autonomy HWY-Q1-27",
         "D": "Brindle Pallet Systems BPS-2027-02", "E": "Kestrin Warehousing KW-2701"}
GRADED_PROJECTS = ["P26-0446", "P26-0441", "P26-0434"]
CLOSED_BY = "2026-10-18"          # projects whose register end date falls by Sunday 18 October: every chain closed at the pull
EAT = dt.timezone(dt.timedelta(hours=3))


def r(x, nd):
    return float(round(float(x), nd))


def nd_cost(k):
    return 4 if k == "C" else 2


def closed_projects(G):
    p = G["T_proj"].set_index("project")
    return sorted(p.index[p.end_date <= CLOSED_BY])


def build_figures(G):
    req, rx = G["requests"], G["reflex"]
    out = dict(call_accept=G["call"], call_decline=[k for k in REQ if k not in G["call"]])
    for k in REQ:
        nd = nd_cost(k)
        out["R6_cost_%s" % k] = r(req[k]["cost"], nd)
        out["R6_range_%s" % k] = [r(G["ranges"][k][0], nd), r(G["ranges"][k][1], nd)]
        out["R2_reviews_%s" % k] = r(req[k]["reviews"], 2)
        out["R3_minutes_%s" % k] = r(req[k]["ann_min"], 3 if k == "C" else 1)
        out["R4_topup_%s" % k] = r(req[k]["topup"], 4 if k == "C" else 3)
        out["price_%s" % k] = req[k]["price"]
        out["line_%s" % k] = r(req[k]["line"], nd)
        out["R7_lowest_price_%s" % k] = r(req[k]["lowest_price"], nd)
        out["careful_cost_%s" % k] = r(rx[k]["cost"], nd)
        out["careful_reviews_%s" % k] = r(rx[k]["reviews"], 2)
        out["careful_minutes_%s" % k] = r(rx[k]["ann_min"], 3 if k == "C" else 1)
        out["careful_topup_%s" % k] = r(rx[k]["topup"], 4 if k == "C" else 3)
    r1 = G["r1"]
    for f in ("piece", "topup", "reviewer", "overhead", "total", "ann_hours", "rev_hours"):
        out["R1_%s" % f] = r(r1[f], 1 if "hours" in f else 0)
    for p in GRADED_PROJECTS:
        unit_nd = 4 if p == "P26-0434" else 2
        out["R5_actual_%s" % p] = r(r1["projects"][p], unit_nd)
        out["R5_costing_%s" % p] = r(G["costing_golden"][p], unit_nd)
        out["R5_hurried_%s" % p] = r(G["costing_reflex"][p], unit_nd)
    cl = closed_projects(G)
    gap = (G["costing_golden"][cl] / r1["projects"][cl] - 1).abs()
    gap_h = (G["costing_reflex"][cl] / r1["projects"][cl] - 1).abs()
    out["R5_max_gap_pct"] = r(100 * gap.max(), 1)
    out["R5_within_6pct"] = int((gap <= 0.06).sum())
    out["R5_projects"] = int(len(gap))
    out["R5_hurried_within_6pct"] = int((gap_h <= 0.06).sum())
    out["R5_hurried_max_gap_pct"] = r(100 * gap_h.max(), 1)
    out["R1"] = {"total": out["R1_total"]}
    out["R2_reviews"] = {k: out["R2_reviews_%s" % k] for k in REQ}
    out["R3_minutes"] = {k: out["R3_minutes_%s" % k] for k in REQ}
    out["R4_topup"] = {k: out["R4_topup_%s" % k] for k in REQ}
    out["R5_costing"] = {p: out["R5_costing_%s" % p] for p in GRADED_PROJECTS}
    out["R6_cost"] = {k: out["R6_cost_%s" % k] for k in REQ}
    out["R8_range"] = {"%s_%s" % (k, e): out["R6_range_%s" % k][i] for k in REQ for i, e in enumerate(("lo", "hi"))}
    out["R9_lowest_price"] = {k: out["R7_lowest_price_%s" % k] for k in out["call_decline"]}
    out["call"] = " ".join(G["call"])
    out["range_level_pct"] = 80
    out["topup_band_pct"] = 20
    out["topup_band_usd"] = 0.005
    out["margin"] = Wd.MARGIN
    out["overhead_rate"] = Wd.OVERHEAD_PER_PAID_HOUR
    out["rereturn_share_2026"] = r(G["F"]["returns"]["rereturn"], 3)
    out["topup_share_2026"] = r(G["H"]["topup_share"], 3)
    for name, d in G["alternatives"].items():
        key = "logit" if "logistic" in name else "binned"
        for k in "AB":
            out["alt_%s_cost_%s" % (key, k)] = r(d["costs"][k], 2)
            out["alt_%s_reviews_%s" % (key, k)] = r(d["reviews"][k], 2)
    return out


SHORT_NAMES = {"reflex": "the careful but hurried pass: a logistic return model with 2026's re-return share along the chain "
                         "and video on frames and objects on screen",
               "drop_c1": "the QA chain carried at 2026's re-return share (only the video on track turnover)",
               "drop_c3": "video time on frames and objects on screen (only the QA chain built)"}


def build_effort(G, FG):
    req, rx = G["requests"], G["reflex"]
    routes = G["routes"]
    fam_costs = [d["costs"] for d in list(G["rivals"].values()) + list(G["perturb"].values())]
    cost_bands = {}
    for k in REQ:
        vals = [c[k] for c in fam_costs] + [req[k]["cost"]]
        cost_bands[k] = [r(min(vals) * 0.985, 4), r(max(vals) * 1.015, 4)]
    rev_bands = {k: [r(req[k]["reviews"] * 0.95, 3), r(req[k]["reviews"] * 1.05, 3)] for k in REQ}
    min_bands = {k: [r(req[k]["ann_min"] * 0.95, 4), r(req[k]["ann_min"] * 1.05, 4)] for k in REQ}
    top_bands = {k: [r(max(0.0, req[k]["topup"] * 0.80 - (0.0005 if k == "C" else 0.005)), 4),
                     r(req[k]["topup"] * 1.20 + (0.0005 if k == "C" else 0.005), 4)] for k in REQ}
    proj_bands = {p: [r(G["costing_golden"][p] * 0.95, 4), r(G["costing_golden"][p] * 1.05, 4)] for p in GRADED_PROJECTS}
    range_bands = {c: [r(v * 0.94, 4), r(v * 1.06, 4)] for c, v in FG["R8_range"].items()}
    low_bands = {k: [r(v * 0.97, 4), r(v * 1.03, 4)] for k, v in FG["R9_lowest_price"].items()}
    quick_name = "2026's delivery cost per object carried to each request"
    quick = G["extra"][quick_name]["costs"]
    quick_ans = G["extra"][quick_name]["answer"]
    gold_set = G["call"]
    r1 = G["r1"]

    def rng_cells(rg):
        return {"%s_%s" % (k, e): r(rg[k][i], 4) for k in REQ for i, e in enumerate(("lo", "hi"))}

    def lows(costs, answer):
        return {k: r(Wd.MARGIN * costs[k], 4) for k in REQ if k not in answer}

    reflex_costs = {k: rx[k]["cost"] for k in REQ}
    J = lambda x: " ".join(x)
    results = [
        dict(id="R1", name="April to October 2026 delivery cost as payroll settled it", graded_as="Ask 4",
             figure="R1", depends=[], independent="the pay register and the punch clock",
             golden={"total": FG["R1_total"]}, bands={"total": [r(FG["R1_total"] * 0.995, 0), r(FG["R1_total"] * 1.005, 0)]},
             passes={"quick": {"total": r(r1["piece"] + r1["topup"] + r1["reviewer"], 0)}, "careful": {"total": FG["R1_total"]},
                     "thorough": {"total": FG["R1_total"]}}),
        dict(id="R2", name="QA reviews per delivered image", graded_as="Ask 2, Component 2", figure="R2_reviews",
             depends=[], independent="the request samples and the 2026 reviews", precedent=["L40", "L36"],
             golden={k: FG["R2_reviews_%s" % k] for k in REQ}, bands=rev_bands, partly_share=0.6,
             passes={"quick": {k: 1.0 for k in REQ}, "careful": {k: r(rx[k]["reviews"], 3) for k in REQ},
                     "thorough": {k: FG["R2_reviews_%s" % k] for k in REQ}}),
        dict(id="R3", name="annotator paid minutes per delivered image (per frame for the video)", graded_as="Ask 2, Component 3",
             figure="R3_minutes", depends=[], independent="the request samples", precedent=["L36", "L42"],
             golden={k: FG["R3_minutes_%s" % k] for k in REQ}, bands=min_bands, partly_share=0.6,
             passes={"quick": {k: r(rx[k]["first_min"], 4) for k in REQ}, "careful": {k: r(rx[k]["ann_min"], 4) for k in REQ},
                     "thorough": {k: FG["R3_minutes_%s" % k] for k in REQ}}),
        dict(id="R4", name="floor top-up per delivered image", graded_as="Ask 2", figure="R4_topup",
             depends=["R3"], precedent=["L40", "L36"], golden={k: FG["R4_topup_%s" % k] for k in REQ}, bands=top_bands,
             partly_share=0.6,
             passes={"quick": {k: 0.0 for k in REQ}, "careful": {k: r(rx[k]["topup"], 4) for k in REQ},
                     "thorough": {k: FG["R4_topup_%s" % k] for k in REQ}}),
        dict(id="R5", name="each closed 2026 project's costing beside its actual cost per delivered image",
             graded_as="Ask 3, Component 4", figure="R5_costing", depends=["R1"], precedent=["L28", "L37"],
             golden={p: FG["R5_costing_%s" % p] for p in GRADED_PROJECTS}, bands=proj_bands,
             passes={"quick": {p: FG["R5_actual_%s" % p] for p in GRADED_PROJECTS},
                     "careful": {p: FG["R5_hurried_%s" % p] for p in GRADED_PROJECTS},
                     "thorough": {p: FG["R5_costing_%s" % p] for p in GRADED_PROJECTS}}),
        dict(id="R6", name="each request's expected cost per delivered image (per frame for the video)", graded_as="Ask 1, Component 1",
             figure="R6_cost", depends=["R2", "R3", "R4"], precedent=["L40", "L36"],
             golden={k: FG["R6_cost_%s" % k] for k in REQ}, bands=cost_bands, partly_share=0.6,
             passes={"quick": {k: r(quick[k], 4) for k in REQ}, "careful": {k: r(rx[k]["cost"], 4) for k in REQ},
                     "thorough": {k: FG["R6_cost_%s" % k] for k in REQ}}),
        dict(id="R7", name="the requests to accept (offered price at least 1.18 times the expected cost)",
             graded_as="Recommendation", figure="call", depends=["R6"], precedent=["L40", "L36"],
             golden=J(gold_set), passes={"quick": J(quick_ans), "careful": J(routes["reflex"]["answer"]), "thorough": J(gold_set)}),
        dict(id="R8", name="each request's 80 per cent range on its expected cost", graded_as="Ask 1", figure="R8_range",
             depends=["R6"], precedent=["L40", "L36"], golden=FG["R8_range"], bands=range_bands, partly_share=0.6,
             passes={"quick": {}, "careful": rng_cells(G["ranges_reflex"]), "thorough": FG["R8_range"]}),
        dict(id="R9", name="the lowest acceptable price for each request to decline", graded_as="Ask 5",
             figure="R9_lowest_price", depends=["R6"], precedent=["L40", "L36"], golden=FG["R9_lowest_price"], bands=low_bands,
             passes={"quick": lows(quick, quick_ans), "careful": lows(reflex_costs, routes["reflex"]["answer"]),
                     "thorough": FG["R9_lowest_price"]}),
    ]
    shortcut_routes = [dict(name=SHORT_NAMES[k], answer=routes[k]["answer"]) for k in ("reflex", "drop_c1", "drop_c3")]
    shortcut_routes += [dict(name=n, answer=d["answer"]) for n, d in G["extra"].items()]
    shortcut_routes += [dict(name=n, answer=d["answer"]) for n, d in G["alternatives"].items() if d["answer"] != gold_set]
    route_list = [dict(name="the golden", golden=True, answer=gold_set)] + shortcut_routes
    forcing = dict(kind="set", what="the requests whose offered price clears 1.18 times the expected cost of delivery",
                   golden_answer=gold_set,
                   golden_family=[dict(name=n, answer=d["answer"]) for n, d in G["rivals"].items()],
                   shortcuts=shortcut_routes,
                   perturbations=[dict(input=n, answer=d["answer"]) for n, d in G["perturb"].items()],
                   lines={k: FG["line_%s" % k] for k in REQ})
    fact = dict(golden_answer=J(gold_set), reflex_route=dict(answer=J(routes["reflex"]["answer"])), judgments=[
        dict(id="J1", name="the QA chain: per-object issue intensities aggregated over each image, and each correction's "
             "re-review at an intensity that rises with the image's own", kind="stump", precedent=["L40", "L36"],
             dropped=dict(answer=routes["drop_c1"]["answer"], results_moved=["R2", "R3", "R4", "R6", "R7", "R8"]),
             alone=dict(answer=routes["drop_c3"]["answer"], results_rescued=["R2"])),
        dict(id="J2", name="the floor settled per annotator per pay week as an expected cost over paces and weeks", kind="reflex",
             precedent=["R53", "R47"]),
        dict(id="J3", name="video time on tracks starting and ending, not objects on screen", kind="stump",
             precedent=["L36", "L42"], dropped=dict(answer=routes["drop_c3"]["answer"], results_moved=["R3", "R4", "R5", "R6", "R7", "R8"]),
             alone=dict(answer=routes["drop_c1"]["answer"], results_rescued=[])),
        dict(id="J4", name="per-object time with each annotator's pace", kind="reflex", precedent=["R14", "R26"]),
        dict(id="J5", name="paid time per tool second from the punch clock by centre, the 2026 cost rebuilt on payroll",
             kind="reflex", precedent=["R01", "R57"])])
    hints = [dict(sentence="A corrected image goes back to QA with every object re-checked, so the denser the image the likelier "
                           "it comes back again", rescues=["R2"]),
             dict(sentence="The floor is settled per annotator per pay week", rescues=[]),
             dict(sentence="Video time follows the tracks that start and end, not the objects on screen", rescues=[])]
    return dict(results=results, routes=route_list, forcing=forcing, factorial=fact, hints=hints)


def route_costs(G, route):
    return G["routes"][route]["costs"]


# ------------------------------------------------------------------ the golden workbook and note
def workbook(G, FG, path, author, created, modified):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Q1 2027 requests"
    ws.append(["Request", "Unit", "Offered price (USD)", "Expected cost per unit (USD)", "80% range low", "80% range high",
               "Annotator paid minutes per unit", "QA reviews per unit", "Floor top-up per unit (USD)", "Piece pay per unit (USD)",
               "Policy line: price / 1.18", "Decision", "Lowest acceptable price (USD)"])
    for c in ws[1]:
        c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical="top")
    for k in REQ:
        q = G["requests"][k]
        nd = nd_cost(k)
        ws.append([NAMES[k], q["unit"], q["price"], round(q["cost"], nd), round(G["ranges"][k][0], nd), round(G["ranges"][k][1], nd),
                   round(q["ann_min"], 3 if k == "C" else 1), round(q["reviews"], 2),
                   round(q["topup"], 4 if k == "C" else 3), round(q["piece"], 4 if k == "C" else 3), round(q["line"], nd),
                   "accept" if k in G["call"] else "decline", "" if k in G["call"] else round(q["lowest_price"], nd)])
    widths = [32, 7, 12, 14, 11, 11, 14, 11, 13, 12, 13, 10, 14]
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.append([])
    ws.append(["Video request C: QA reviews are per 25-frame task; all other figures per frame."])
    ws2 = wb.create_sheet("2026 projects")
    ws2.append(["Project", "Scene", "Unit", "Delivered units", "Actual cost per unit (USD)", "Costing per unit (USD)", "Gap",
                "Closed by 18 October"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    proj = G["T_proj"].set_index("project")
    for p in sorted(G["r1"]["projects"].index):
        act = G["r1"]["projects"][p]; cg = G["costing_golden"][p]
        nd = 4 if proj.loc[p, "unit"] == "frame" else 2
        ws2.append([p, proj.loc[p, "scene"], proj.loc[p, "unit"], int(proj.loc[p, "delivered_units"]), round(act, nd), round(cg, nd),
                    round(cg / act - 1, 3), "yes" if proj.loc[p, "end_date"] <= CLOSED_BY else "no, running at the pull"])
        ws2.cell(row=ws2.max_row, column=7).number_format = "0.0%"
    for i, w in enumerate([11, 11, 7, 14, 18, 18, 8, 20]):
        ws2.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws3 = wb.create_sheet("2026 delivery cost")
    r1 = G["r1"]
    rows = [("Piece pay", r1["piece"]), ("Floor top-ups", r1["topup"]), ("QA reviewer pay", r1["reviewer"]),
            ("Overhead at USD 1.55 per paid hour", r1["overhead"]), ("Delivery cost, 6 April to 1 November 2026", r1["total"]),
            ("Annotator paid hours", r1["ann_hours"]), ("Reviewer paid hours", r1["rev_hours"])]
    ws3.append(["Line", "USD or hours"])
    for c in ws3[1]:
        c.font = Font(bold=True)
    for a, b in rows:
        ws3.append([a, round(b, 1) if "hours" in a else round(b)])
    ws3.column_dimensions["A"].width = 44; ws3.column_dimensions["B"].width = 16
    wb.save(path)
    PP.normalize_ooxml(path, author, author, created, modified, excel=True, company="Pellucid Annotation Ltd")


def note(G, FG, path, author, created, modified):
    from docx import Document
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    d.add_heading("Q1 2027 annotation requests: what to accept", level=1)
    acc = ", ".join(NAMES[k].split(" ")[0] + " " + NAMES[k].split(" ")[-1] for k in G["call"])
    q = G["requests"]
    short = lambda k: NAMES[k].split(" ")[0] + " " + NAMES[k].split(" ")[-1]
    dec = [k for k in REQ if k not in G["call"]]
    acc_names = [short(k) for k in G["call"]]
    d.add_paragraph("Accept %s at the prices offered. Decline %s unless the clients come up to at least %s per image." % (
        ", ".join(acc_names[:-1]) + " and " + acc_names[-1] if len(acc_names) > 1 else acc_names[0],
        ", ".join(short(k) for k in dec[:-1]) + " and " + short(dec[-1]),
        ", ".join("USD %.2f" % FG["R7_lowest_price_%s" % k] for k in dec[:-1]) + " and USD %.2f" % FG["R7_lowest_price_%s" % dec[-1]]))
    t = d.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    for i, h in enumerate(["Request", "Offered", "Expected cost", "80% range", "Decision"]):
        t.rows[0].cells[i].text = h
    for k in REQ:
        nd = nd_cost(k)
        fmt = "%." + str(nd) + "f"
        row = t.add_row().cells
        row[0].text = NAMES[k]
        row[1].text = ("USD " + fmt % q[k]["price"]) + (" per frame" if k == "C" else "")
        row[2].text = "USD " + fmt % q[k]["cost"]
        row[3].text = (fmt % G["ranges"][k][0]) + " to " + (fmt % G["ranges"][k][1])
        row[4].text = "accept" if k in G["call"] else "decline"
    d.add_paragraph("")
    d.add_paragraph("Why the crowded street request does not pay: QA returns an image when it finds any missed object, and the "
                    "annotator re-checks every object before it goes back, so with well over a hundred objects an image most images "
                    "come back at least once and a corrected one comes back again far more often than this year's work suggests "
                    "(%.2f reviews per image; this year's re-return rate carried along the chain gives %.2f). The shelf request "
                    "carries the same chain (%.2f reviews per image) and its price still leaves room." % (
                        FG["R2_reviews_A"], FG["careful_reviews_A"], FG["R2_reviews_B"]))
    d.add_paragraph("Why the pallet polygons do not pay: at USD 0.033 a polygon, the annotators' weeks on these outlines fall "
                    "under the hourly floor and payroll tops them up week by week (USD %.3f an image)." % FG["R4_topup_D"])
    d.add_paragraph("Why the highway video pays: video work follows the tracks that start and end, not the vehicles on screen; "
                    "this year's busy urban and plaza video makes a per-vehicle rate look right, and the parking-lot project shows "
                    "it is not. At %.3f paid minutes a frame the cost is USD %.4f a frame against USD %.4f offered." %
                    (FG["R3_minutes_C"], FG["R6_cost_C"], q["C"]["price"]))
    d.add_paragraph("Check against 2026: the same costing gives each project's actual cost per delivered unit within 6 per cent "
                    "on %d of the %d projects that closed by 18 October, and at most %.1f per cent off. Projects still running "
                    "at the pull carry corrections not yet delivered, so their actual runs high." % (
                        FG["R5_within_6pct"], FG["R5_projects"], FG["R5_max_gap_pct"]))
    d.save(path)
    PP.normalize_docx(path, author, author, created, modified, revision=4, total_time=58, seed=24, company="Pellucid Annotation Ltd")
