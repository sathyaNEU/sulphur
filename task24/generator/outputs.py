"""task24: figures.json, the golden workbook and the one-page memo, all from one computed object (the golden on the
cut pack and its bootstrap band)."""
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import analysis as A
import officepdf as O
import postprocess as PP

TYPES = ["order_delivery", "returns_refunds", "account_billing", "product_howto", "device_troubleshooting"]
TNAME = {"order_delivery": "Orders and delivery", "returns_refunds": "Returns and refunds",
         "account_billing": "Account and billing", "product_howto": "Product how-to",
         "device_troubleshooting": "Device troubleshooting"}
NZDT = dt.timezone(dt.timedelta(hours=13))
ANALYST = "Anna Gaines"
VOLS = A.VOLS


def pct(x, nd=1):
    return float(round(100.0 * float(x), nd))


# ------------------------------------------------------------------ the workbook
def _bold(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)


def workbook(G, B, V, D, FG, path, created, modified):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "forecast"
    ws.append(["Expected accuracy against the senior technicians' standard (per cent), Q1 2027 reward model"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Ticket type", "Current model (RM-22)", "Signed order alone", "Whole Tallyfield option added"] +
              ["+%s Ardentdesk" % "{:,}".format(x) for x in VOLS[1:]] + ["2027 plan share"])
    _bold(ws, 2)
    for d, t in enumerate(TYPES):
        ws.append([TNAME[t], pct(G["current"][d]), pct(G["grid"][0][d]), pct(G["option_acc"][d])] +
                  [pct(G["grid"][x][d]) for x in VOLS[1:]] + [pct(V["mix27"][d])])
    ws.append(["2027 mix", pct(G["current_mix"]), pct(G["grid_mix"][0]), pct(G["option_mix"])] +
              [pct(G["grid_mix"][x]) for x in VOLS[1:]] + [100.0])
    _bold(ws, ws.max_row)
    ws.append([])
    ws.append(["Launch bar (policy DL-03)", pct(V["bar"])])
    ws.append(["Recommended purchase", "Ardentdesk %s comparisons; Tallyfield option not taken up" %
               "{:,}".format(FG["R7_purchase"]["desk"])])
    ws.append(["Expected 2027-mix accuracy at the purchase", FG["R7_at_purchase_mix"]])
    ws.append(["80 per cent range at the purchase", "%.1f to %.1f" % (FG["R8_range"]["lo"], FG["R8_range"]["hi"])])
    ws.append(["Cost (USD)", FG["R7_cost_usd"]])
    ws.append(["RM-22 agreement with the IS-25 labels (dashboard)", FG["R2_dashboard_RM22"]])
    ws.column_dimensions["A"].width = 44
    for col in "BCDEFGHIJ":
        ws.column_dimensions[col].width = 15
    for r in ws.iter_rows(min_row=2, max_row=2):
        for c in r:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    w1 = wb.create_sheet("vendor_error")
    w1.append(["Error against the standard (per cent of judgments whose reply is not the technicians' majority), "
               "2026 label audit, no-preference judgments set aside"])
    w1["A1"].font = Font(bold=True)
    w1.append(["Ticket type", "Tallyfield", "Ardentdesk"])
    _bold(w1, 2)
    for t in TYPES:
        w1.append([TNAME[t], FG["R1_vendor_error"]["tallyfield.%s" % t], FG["R1_vendor_error"]["ardentdesk.%s" % t]])
    w1.column_dimensions["A"].width = 28
    w1.column_dimensions["B"].width = 14
    w1.column_dimensions["C"].width = 14
    w2 = wb.create_sheet("label_value")
    w2.append(["Ticket type", "Tallyfield error when not pulled to the longer reply (audit, latent-class fit)",
               "Ardentdesk error (audit, latent-class fit)", "Pairs with no better reply",
               "Information per Tallyfield label", "Information per Ardentdesk label",
               "Tallyfield label worth (Ardentdesk = 1)", "IS-25 label error (fitted on the reviewed runs)"])
    _bold(w2, 1)
    S = G["C"]["S"]
    eis = A._split(G["theta"], G["opt"])[3]
    for d, t in enumerate(TYPES):
        w2.append([TNAME[t], round(float(S["ea"][d]), 3), round(float(S["eb"][d]), 3), round(float(S["a"][d]), 3),
                   round(float(G["C"]["IA"][d]), 4), round(float(G["C"]["IB"][d]), 4),
                   round(float(G["C"]["IA"][d] / G["C"]["IB"][d]), 3), round(float(eis[d]), 3)])
    w2.append([])
    w2.append(["Tallyfield pull to the longer reply, by length ratio of the two drafts"])
    w2.append(["Length ratio from", "to", "Pull"])
    _bold(w2, w2.max_row)
    bins = G["C"]["bins"]
    for k in range(len(bins) - 1):
        lo, hi = np.exp(bins[k]), np.exp(bins[k + 1])
        w2.append([round(float(lo), 2), (round(float(hi), 2) if bins[k + 1] < 5 else "and over"),
                   round(float(G["C"]["pull"][k]), 3)])
    w2.append([])
    lk, al, kap, _ = A._split(G["theta"], G["opt"])
    w2.append(["Learning curve", "1 - 0.5 x (1 + n / K) ^ -alpha on pairs with a better reply, n in label information"])
    w2.append(["alpha (all ticket types)", round(float(al), 3)])
    w2.append(["share of its labels' pull a model takes on", round(float(kap), 3)])
    for d, t in enumerate(TYPES):
        w2.append(["K, %s" % TNAME[t], int(round(float(np.exp(lk[d]))))])
    w2.column_dimensions["A"].width = 36
    for col in "BCDEFGH":
        w2.column_dimensions[col].width = 18

    w3 = wb.create_sheet("runs_2026")
    w3.append(["Run", "Status", "IS-25 agreement (per cent)", "Shadow review accuracy (per cent)"] +
              ["Accuracy vs standard, %s" % TNAME[t] for t in TYPES] + ["Accuracy vs standard, 2027 mix"])
    _bold(w3, 1)
    for rid in V["runs"]:
        acc = A.acc_standard(G["theta"], G["C"], *V["counts"][rid], G["opt"])
        w3.append([rid, D["status"][rid], pct(D["is25"][rid]), (pct(D["review"][rid]) if rid in D["review"] else None)] +
                  [pct(a) for a in acc] + [pct((acc * V["mix27"]).sum())])
    w3.column_dimensions["A"].width = 9
    for col in "BCDEFGHIJ":
        w3.column_dimensions[col].width = 16
    wb.save(path)
    PP.normalize_ooxml(path, ANALYST, ANALYST, created, modified, excel=True, company="Penvale Electronics Ltd")


# ------------------------------------------------------------------ the memo
def memo(G, B, V, D, FG, path, created, modified):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.0, leading=11.8, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.0, leading=14.5, spaceAfter=3)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.0, leading=9.8)
    MM = 2.83
    trb = 4
    head = [["To", "Bridget Sanders, Head of Support Automation"], ["Copy", "Sophie Gibson, Procurement"],
            ["From", "%s, Support Automation" % ANALYST], ["Date", "13 November 2026"]]
    t1 = Table([[Paragraph(a, cell), Paragraph(b, cell)] for a, b in head], colWidths=[18 * MM, 150 * MM])
    t1.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    rows = [["", "Current model", "Signed order", "+ whole option"] + ["+%dk desk" % (x // 1000) for x in VOLS[1:]]]
    rows.append(["Device troubleshooting", "%.1f" % pct(G["current"][trb]), "%.1f" % pct(G["grid"][0][trb]),
                 "%.1f" % pct(G["option_acc"][trb])] + ["%.1f" % pct(G["grid"][x][trb]) for x in VOLS[1:]])
    rows.append(["2027 mix", "%.1f" % pct(G["current_mix"]), "%.1f" % pct(G["grid_mix"][0]), "%.1f" % pct(G["option_mix"])] +
                ["%.1f" % pct(G["grid_mix"][x]) for x in VOLS[1:]])
    t2 = Table([[Paragraph(str(c), cell) for c in r] for r in rows],
               colWidths=[36 * MM, 18 * MM, 17 * MM, 18 * MM] + [15.8 * MM] * 5)
    t2.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    ia, ib = G["C"]["IA"][trb], G["C"]["IB"][trb]
    s = [Paragraph("Q1 2027 label purchase for Draftline auto-send", h1), t1, Spacer(1, 5),
         Paragraph("<b>Recommendation.</b> Buy %s Ardentdesk troubleshooting comparisons (USD %s) and do not take up the "
                   "Tallyfield option. With the signed order, the Q1 2027 model is then expected to reach %.1f per cent "
                   "accuracy against the senior technicians on the planned 2027 mix (80 per cent range %.1f to %.1f), "
                   "against the %.1f per cent bar." % ("{:,}".format(FG["R7_purchase"]["desk"]), "{:,}".format(FG["R7_cost_usd"]),
                                                       FG["R7_at_purchase_mix"], FG["R8_range"]["lo"], FG["R8_range"]["hi"],
                                                       FG["bar_pct"]), body),
         Paragraph("<b>Where we are.</b> RM-22 is at %.1f per cent on the 2027 mix against the standard and %.1f on "
                   "device troubleshooting. The %.1f per cent on the dashboard is agreement with IS-25's 2025 Tallyfield "
                   "labels, which share the crowd's errors and its pull to longer replies, so it neither measures the "
                   "standard nor moves with it." % (FG["R2_current"]["mix"], FG["R2_current"]["device_troubleshooting"],
                                                     FG["R2_dashboard_RM22"]), body),
         Paragraph("<b>Why the signed order is not enough.</b> In the 2026 audit %.0f per cent of Tallyfield's "
                   "troubleshooting judgments disagree with the technicians, against %.0f per cent of Ardentdesk's; with "
                   "the crowd's pull to longer replies and the pairs with no better reply set aside, the error is %.0f "
                   "per cent against %.0f. What a label teaches the model goes with the square of its signal, so a "
                   "Tallyfield troubleshooting label is worth about %.2f of an Ardentdesk one. The order's %s "
                   "troubleshooting comparisons add little, and every crowd label adds to the pull to longer replies "
                   "that the technicians do not share. The signed order alone reaches %.1f per cent; the whole option "
                   "adds %.1f points for USD %s." % (FG["R1_vendor_error"]["tallyfield.device_troubleshooting"],
                                                    FG["R1_vendor_error"]["ardentdesk.device_troubleshooting"],
                                                    100 * G["C"]["S"]["ea"][trb], 100 * G["C"]["S"]["eb"][trb],
                                                    ia / ib, "{:,}".format(int(V["order"][trb])), FG["R3_order"]["mix"],
                                                    FG["R5_option"]["mix"] - FG["R3_order"]["mix"],
                                                    "{:,}".format(int(round(V["option"] * V["price_tf"])))), body),
         t2, Spacer(1, 4),
         Paragraph("<b>How it was built.</b> Each source's error by ticket type comes from the 2026 audit; each run's "
                   "accuracy from a joint fit of every run's IS-25 picks (read through the crowd's error and the pull "
                   "the run shares with it) and the seven shadow reviews; the learning curve is in label information "
                   "and stops short of 100 per cent because the technicians themselves split on some pairs. The range "
                   "resamples the audit, IS-25, the reviews and the deliveries.", body),
         Paragraph("Workbook: specialist_label_forecast.xlsx (forecast, label value, 2026 runs).", body)]
    O.build(path, s, "Q1 2027 label purchase for Draftline auto-send", ANALYST, "Label purchase memo",
            "Penvale Electronics Ltd  |  Support Automation", created, modified, page_of=True, body_pt=9.0)


# ------------------------------------------------------------------ figures, bands and effort.json
VKEYS = ["R2_current", "R3_order"] + ["R4_%d" % x for x in VOLS[1:]] + ["R5_option"]
CELLKEY = {"R2_current": "current", "R3_order": "order", "R5_option": "option"}
CELLKEY.update({"R4_%d" % x: "desk_%d" % x for x in VOLS[1:]})


def table(c):
    return {t: pct(c[d]) for d, t in enumerate(TYPES)} | {"mix": pct(c[5])}


OPTION_TRANCHE_MAX = 30000      # up to three tranches of the option cost within USD 5,400 of the cheapest purchase


def label(p, band):
    """a purchase as the call it makes: Ardentdesk carrying it (no more than three tranches of the option beside
    it), the option carrying it, both in volume, nothing, or nothing that reaches the bar"""
    if not p["reach"]:
        return "out of reach"
    if not p["desk"]:
        return "option only" if p["option"] else "nothing added"
    if (p["option"] or 0) <= OPTION_TRANCHE_MAX:
        return "Ardentdesk, at most a tranche of the option"
    return "option and Ardentdesk"


def all_figures(OUT):
    G, B, V, D = OUT["G"], OUT["B"], OUT["V"], OUT["D"]
    c = OUT["cells"]
    FG = {k: table(c[CELLKEY[k]]) for k in VKEYS}
    FG["R4_grid"] = {"%d.%s" % (x, cell): v for x in VOLS[1:] for cell, v in FG["R4_%d" % x].items()}
    FG["R1_vendor_error"] = {k: pct(v) for k, v in OUT["vendor_error"].items()}
    FG["R2_dashboard_RM22"] = pct(D["dashboard"])
    p = OUT["purchase"]
    FG["R7_purchase"] = {"option": p["option"], "desk": p["desk"]}
    FG["R6_call"] = [label(p, (0, 0))]
    FG["R7_volume"] = int(p["desk"])
    FG["R7_cost_usd"] = int(round(p["cost"]))
    FG["R7_at_purchase_mix"] = pct(G["at_volume"])
    FG["R8_range"] = {"lo": pct(B["acc_lo"]), "hi": pct(B["acc_hi"])}
    FG["bar_pct"] = pct(V["bar"])
    S = G["C"]["S"]
    FG["info_ratio_troubleshooting"] = float(round(G["C"]["IA"][4] / G["C"]["IB"][4], 3))
    FG["acc_ratio_troubleshooting"] = float(round((1 - S["ea"][4]) / (1 - S["eb"][4]), 3))
    FG["crowd_error_troubleshooting"] = float(round(S["ea"][4], 3))
    FG["desk_error_troubleshooting"] = float(round(S["eb"][4], 3))
    FG["order_troubleshooting"] = int(V["order"][4])
    FG["kappa"] = float(round(A._split(G["theta"], G["opt"])[2], 3))
    FG["is_error_lr"] = float(round(-[r for r in OUT["ruled_out"] if r["opt"].get("is_error")][0]["lr"], 1))
    a = [r for r in OUT["ruled_out"] if r["opt"].get("alpha")][0]
    FG["alpha_lr"] = float(round(a["lr"], 1)); FG["alpha_df"] = int(a["df"])
    FG["vol_range"] = {"lo": int(round(B["vol_lo"], -3)), "hi": int(round(B["vol_hi"], -3))}
    FG["context"] = {"record_year": 2026, "plan_year": 2027, "order": 300000, "option": int(V["option"]),
                     "option_cost_usd": int(round(V["option"] * V["price_tf"])), "price_usd": V["price_ad"],
                     "min_order": int(V["min_order"]), "step": int(V["step"]), "option_step": int(V["option_step"]),
                     "capacity": int(V["cap"]), "review_rounds": 7, "audit_pairs": 2000,
                     "quick_vendor_error": OUT["quick_vendor_error"]}
    dr = OUT["drops"]
    FG["shortcut_purchases"] = {k: {"option": dr[k]["purchase"]["option"], "desk": dr[k]["purchase"]["desk"],
                                    "cost_usd": (int(round(dr[k]["purchase"]["cost"])) if dr[k]["purchase"]["cost"] else None)}
                                for k in ("J1", "J2", "J2raw", "J3", "J4", "reflex")}
    FG["shortcut_cells"] = {"J1_current_mix": pct(dr["J1"]["cells"]["current"][5]),
                            "J4_troubleshooting_120000": pct(dr["J4"]["cells"]["desk_120000"][4]),
                            "is_audit_current_mix": pct([r for r in OUT["ruled_out"] if r["opt"].get("is_error")][0]["cells"]["current"][5])}
    FG["family_desk"] = sorted(f["purchase"]["desk"] for f in OUT["family"] if f["purchase"]["reach"])
    base = OUT["tranches"][0]["cost"]
    FG["tranches"] = {str(o): {"desk": t["desk"], "cost_usd": int(round(t["cost"])), "extra_usd": int(round(t["cost"] - base))}
                      for o, t in OUT["tranches"].items() if t}
    FG["context"]["option_tranche_max"] = OPTION_TRANCHE_MAX
    FG["context"]["option_tranche_cost_usd"] = int(round(V["option_step"] * V["price_tf"]))
    FG["context"]["volumes"] = list(VOLS)
    FG["context"]["ceiling_pct"] = 100
    FG["derived"] = {"crowd_error_troubleshooting_pct": int(round(100 * FG["crowd_error_troubleshooting"])),
                     "desk_error_troubleshooting_pct": int(round(100 * FG["desk_error_troubleshooting"])),
                     "option_gain_pts": round(FG["R5_option"]["mix"] - FG["R3_order"]["mix"], 1),
                     "purchase_gain_pts": round(FG["R7_at_purchase_mix"] - FG["R3_order"]["mix"], 1)}
    return FG


def bands(OUT, FG):
    """the graded bands: every defensible rival inside, every named shortcut outside on its call"""
    fam = OUT["family"]
    dev_type = 0.0; dev_mix = 0.0
    for f in fam:
        for k in VKEYS:
            gk = CELLKEY[k]
            g = OUT["cells"][gk]; r = f["cells"][gk]
            dev_type = max(dev_type, max(abs(100 * (r[d] - g[d])) for d in range(5)))
            dev_mix = max(dev_mix, abs(100 * (r[5] - g[5])))
    tb = max(1.5, np.ceil((dev_type + 0.25) * 2) / 2)
    mb = max(1.0, np.ceil((dev_mix + 0.15) * 2) / 2)
    desks = [f["purchase"]["desk"] for f in fam if f["purchase"]["reach"]] + [OUT["purchase"]["desk"]]
    desks += [r["purchase"]["desk"] for r in OUT["ruled_out"] if r["purchase"]["reach"] and not r["purchase"]["option"]]
    g = OUT["purchase"]["desk"]
    lo = int(np.floor(min(min(desks) * 0.85, 0.6 * g) / 1000.0) * 1000)
    hi = int(np.ceil(max(max(desks) * 1.15, 1.6 * g) / 1000.0) * 1000)
    return {"type": float(tb), "mix": float(mb), "desk": [lo, hi], "range": 0.6, "vendor": 2.5}


def shortcut_figures(OUT, BANDS):
    fam = [f["purchase"]["desk"] for f in OUT["family"] if f["purchase"]["reach"]]
    dr = OUT["drops"]
    return {"J1_current_mix": pct(dr["J1"]["cells"]["current"][5]), "family_lo": min(fam),
            "family_hi": max(fam), "quick_vendor_error": OUT["quick_vendor_error"],
            "J2": dr["J2"]["purchase"], "J2raw": dr["J2raw"]["purchase"], "J3": dr["J3"]["purchase"],
            "J4": dr["J4"]["purchase"], "J1": dr["J1"]["purchase"], "reflex": dr["reflex"]["purchase"],
            "J2_option_mix": pct(dr["J2"]["cells"]["option"][5]), "J4_trb120": pct(dr["J4"]["cells"]["desk_120000"][4]),
            "golden_trb120": pct(OUT["cells"]["desk_120000"][4]), "is_audit_current": pct([r for r in OUT["ruled_out"]
                                                                                           if r["opt"].get("is_error")][0]["cells"]["current"][5])}


def _route_value(route, key):
    c = route["cells"][CELLKEY[key]]
    return table(c)


def _purchase_value(route):
    p = route["purchase"]
    if not p["reach"]:
        return {"option": -1, "desk": -1}
    return {"option": p["option"], "desk": p["desk"]}


TABLES = {"R2": ["R2_current"], "R3": ["R3_order"], "R4": ["R4_%d" % x for x in VOLS[1:]], "R5": ["R5_option"]}


def right_results(route, OUT, FG, BANDS):
    """the result ids a route gets right on the golden's bands (R1 and R8 are not routes' work: R1 is read the same
    way by every route past the quick pass, R8 follows the purchase)"""
    ok = ["R1"]
    for rid, keys in TABLES.items():
        good = True
        for k in keys:
            v = _route_value(route, k); g = FG[k]
            for cell, gv in g.items():
                tol = BANDS["mix"] if cell == "mix" else BANDS["type"]
                if abs(v[cell] - gv) > tol + 1e-9:
                    good = False
        if good:
            ok.append(rid)
    pv = _purchase_value(route)
    if pv["desk"] > 0 and 0 <= pv["option"] <= OPTION_TRANCHE_MAX:
        ok.append("R6")
        if BANDS["desk"][0] <= pv["desk"] <= BANDS["desk"][1]:
            ok += ["R7", "R8"]
    return ok


def _table_result(rid, name, graded, keys, FG, passes, prec, tb, mb):
    gold = {}; bnd = {}
    multi = len(keys) > 1
    for k in keys:
        for cell, v in FG[k].items():
            ck = "%s.%s" % (k[3:], cell) if multi else cell
            gold[ck] = v
            t = mb if cell == "mix" else tb
            bnd[ck] = [round(v - t, 2), round(v + t, 2)]
    ps = {}
    for pname, route in passes.items():
        val = {}
        for k in keys:
            for cell, v in _route_value(route, k).items():
                val[("%s.%s" % (k[3:], cell)) if multi else cell] = v
        ps[pname] = val
    return dict(id=rid, name=name, graded_as=graded, figure=("R4_grid" if multi else keys[0]), depends=[],
                independent="the audit, the shadow reviews and IS-25", precedent=prec, golden=gold, bands=bnd,
                partly_share=0.6, passes=ps)


def build_effort(OUT, FG, BANDS):
    dr = OUT["drops"]
    tb, mb = BANDS["type"], BANDS["mix"]
    band = BANDS["desk"]
    golden_route = dict(cells=OUT["cells"], purchase=OUT["purchase"])
    passes = {"quick": dr["quick"], "careful": dr["reflex"], "thorough": golden_route}
    ve = FG["R1_vendor_error"]
    res = [dict(id="R1", name="each vendor's error against the standard by ticket type", graded_as="Ask 1",
                figure="R1_vendor_error", depends=[], independent="the 2026 label audit", golden=ve,
                bands={k: [round(v - BANDS["vendor"], 2), round(v + BANDS["vendor"], 2)] for k, v in ve.items()},
                partly_share=0.6,
                passes={"quick": {k: (OUT["quick_vendor_error"] if k.startswith("tallyfield") else None) for k in ve},
                        "careful": dict(ve), "thorough": dict(ve)})]
    res.append(_table_result("R2", "the current model's accuracy against the standard by ticket type and on the 2027 mix",
                             "Ask 2, Component 1", ["R2_current"], FG, passes, ["L37", "L28"], tb, mb))
    res.append(_table_result("R3", "accuracy with the signed order alone", "Ask 3, Component 2", ["R3_order"], FG, passes,
                             ["L17", "L15", "N01"], tb, mb))
    res.append(_table_result("R4", "accuracy with 20,000 to 120,000 Ardentdesk comparisons added", "Ask 4 to 8",
                             ["R4_%d" % x for x in VOLS[1:]], FG, passes, ["L17", "L40", "N34"], tb, mb))
    res.append(_table_result("R5", "accuracy with the whole Tallyfield option taken up", "Ask 9, Component 2",
                             ["R5_option"], FG, passes, ["L17", "L15", "N01"], tb, mb))
    res.append(dict(id="R6", name="the cheapest purchase that reaches the bar", graded_as="Recommendation, Component 3",
                    figure="R6_call", depends=["R4", "R5"], independent="", precedent=["L17", "L15", "L37"],
                    golden=FG["R6_call"],
                    passes={k: [label(v["purchase"], band)] for k, v in passes.items()}))
    def vol(route):
        p = route["purchase"]
        return int(p["desk"]) if (p["reach"] and p["desk"]) else None
    res.append(dict(id="R7", name="the Ardentdesk volume to buy and its cost", graded_as="Recommendation, Ask 10",
                    figure="R7_volume", depends=["R6"], independent="", precedent=["L17", "L40"],
                    golden=FG["R7_volume"], band=band,
                    passes={k: vol(v) for k, v in passes.items()}))
    rg = FG["R8_range"]
    res.append(dict(id="R8", name="the 80 per cent range at the purchase", graded_as="Ask 11", figure="R8_range",
                    depends=["R7"], independent="", precedent=["L28", "L37"],
                    golden={"lo": rg["lo"], "hi": rg["hi"]},
                    bands={"lo": [rg["lo"] - BANDS["range"], rg["lo"] + BANDS["range"]],
                           "hi": [rg["hi"] - BANDS["range"], rg["hi"] + BANDS["range"]]},
                    partly_share=0.5,
                    passes={"quick": {"lo": None, "hi": None}, "careful": {"lo": None, "hi": None},
                            "thorough": {"lo": rg["lo"], "hi": rg["hi"]}}))
    routes = [dict(name="the golden", golden=True, answer=FG["R6_call"])]
    for key in ("reflex", "J1", "J2", "J2raw", "J3", "J4", "quick", "textbook"):
        routes.append(dict(name=dr[key]["name"], answer=[label(dr[key]["purchase"], band)]))
    fam = [dict(name=f["name"], answer=[label(f["purchase"], band)]) for f in OUT["family"]]
    shortcuts = [dict(name=dr[k]["name"], answer=[label(dr[k]["purchase"], band)])
                 for k in ("reflex", "J1", "J2", "J2raw", "J3", "quick", "textbook")]
    pert = [dict(input="%s %s its spread (%.3g on %.3g)" % (q["input"], "plus" if q["factor"] > 1 else "minus",
                                                           q["spread"], q["value"]),
                 answer=[label(dict(reach=q["desk"] is not None, option=q["option"], desk=q["desk"]), band)])
            for q in OUT["perturbations"]]
    forcing = dict(kind="set", what="the cheapest purchase that reaches the bar: Ardentdesk carries it, with no more than "
                   "three tranches (30,000) of the option beside it (the Ardentdesk volume graded between %s and %s)"
                   % ("{:,}".format(band[0]), "{:,}".format(band[1])),
                   golden_answer=FG["R6_call"], golden_family=fam, shortcuts=shortcuts, perturbations=pert,
                   lines={"bar": FG["bar_pct"]})
    gold_right = right_results(golden_route, OUT, FG, BANDS)
    reflex_right = right_results(dr["reflex"], OUT, FG, BANDS)

    def moved(route):
        rr = right_results(route, OUT, FG, BANDS)
        return [r for r in gold_right if r not in rr]

    def rescued(route):
        rr = right_results(route, OUT, FG, BANDS)
        return [r for r in rr if r not in reflex_right]
    J = [("J1", "the bridge: IS-25's agreement read through the crowd's error and the pull a run shares with it, fitted "
          "on the reviewed runs", ["L37", "L28"], "J1", "J1alone"),
         ("J2", "a label's worth as its information, the square of its signal, not its count or its accuracy",
          ["L17", "N01"], "J2", "J2alone"),
         ("J3", "the crowd's pull to longer replies, inherited by the model in proportion to its crowd share",
          ["L15", "N04"], "J3", "J3alone")]
    judg = []
    for jid, name, prec, dk, ak in J:
        judg.append(dict(id=jid, name=name, kind="stump", precedent=prec,
                         dropped=dict(answer=[label(dr[dk]["purchase"], band)], results_moved=moved(dr[dk])),
                         alone=dict(answer=[label(dr[ak]["purchase"], band)], results_rescued=rescued(dr[ak]))))
    judg.append(dict(id="J4", name="the bound the technicians' split pairs set, each type's curve saturating (priced on "
                     "the troubleshooting cells, the call unmoved)", kind="supporting", precedent=["N34", "L40"],
                     dropped=dict(answer=[label(dr["J4"]["purchase"], band)], results_moved=moved(dr["J4"]))))
    judg.append(dict(id="J5", name="each source's agreement with the technicians read from the audit; duplicates, "
                     "display order, re-runs and vote codes reconciled", kind="reflex", precedent=["R01", "R14"]))
    factorial = dict(golden_answer=FG["R6_call"], reflex_route=dict(answer=[label(dr["reflex"]["purchase"], band)]),
                     judgments=judg)
    hints = [dict(sentence="IS-25's labels are single 2025 Tallyfield judgments, so a run's agreement with them is "
                  "set by its accuracy, the crowd's error and the pull to longer replies the two share",
                  rescues=rescued(dr["J1alone"])),
             dict(sentence="a Tallyfield label on a device troubleshooting pair carries a small fraction of an "
                  "Ardentdesk label's information", rescues=rescued(dr["J2alone"]))]
    return dict(results=res, routes=routes, forcing=forcing, factorial=factorial, hints=hints)
