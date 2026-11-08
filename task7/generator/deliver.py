"""task7: the golden deliverables (the facility-level CSV the planning system loads and the executive committee's
deck) and figures.json, every figure computed from the cut pack by golden.py and checks.py."""
import csv
import io
import json
import math
import os

import numpy as np

import golden as GD
import postprocess

UT, UB = 500000.0, 250000.0


def rnd(v, u):
    return round(v / u) * u


def money(v):
    return format(int(round(v)), ",")


def millions(v, nd=2):
    s = ("%." + str(nd) + "f") % (v / 1e6)
    return s.rstrip("0").rstrip(".") if "." in s else s


def pct(x, nd=0):
    return ("%." + str(nd) + "f") % (100 * x)


def band_table(rec, book, edges=((0, 1), (1, 3), (3, 5), (5, 7), (7, 99))):
    out = []
    for lo, hi in edges:
        v = [x["ratio"] for x in rec if (x["book"] == GD.TRADING) == (book == GD.TRADING) and lo <= x["tau"] < hi]
        out.append(dict(lo=lo, hi=hi, n=len(v), mean=float(np.mean(v)) if v else None))
    return out


def figures(C):
    res, fits, rec, items = C["res"], C["fits"], C["rec"], C["items"]
    g = res["golden"]
    loans = GD.ecl(items, GD.factor_fns(rec)[0]["golden"])
    ead_tot = sum(x["ead"] for x in loans)
    top = sorted(loans, key=lambda x: (-x["el"], x["fac"]))[:5]
    inv_b, occ_b = band_table(rec, "Investment"), band_table(rec, GD.TRADING)
    fi, fo = fits["split"][False], fits["split"][True]
    recent = [x for x in rec if x["date"].year >= 2022]
    recent_fresh = [x for x in recent if x["tau"] < 0.5]
    f_at = lambda F, t: math.exp(F["a"] + F["b"] * t) * F["smear"]
    F = {
        "call": {"plan_figure_eur": rnd(g["total"], UT), "plan_figure_display": "€%s million" % millions(rnd(g["total"], UT), 1),
                 "plan_figure_unrounded_eur": round(g["total"])},
        "asks": {"investment_eur": rnd(g["investment"], UB), "investment_display": "€%s million" % millions(rnd(g["investment"], UB)),
                 "owner_occupied_eur": rnd(g["owner_occupied"], UB),
                 "owner_occupied_display": "€%s million" % millions(rnd(g["owner_occupied"], UB)),
                 "investment_unrounded_eur": round(g["investment"]), "owner_occupied_unrounded_eur": round(g["owner_occupied"]),
                 "five_facilities": sorted(g["top5"]),
                 "five_by_loss": [dict(facility=x["fac"], expected_loss_eur=round(x["el"]), book=x["book"]) for x in top],
                 "csv_rows": len(loans), "csv_total_eur": sum(int(round(x["el"])) for x in loans),
                 "csv_top_facility": top[0]["fac"], "csv_top_loss_eur": round(top[0]["el"])},
        "components": {
            "record_defaults": len(rec),
            "inv_first_year_ratio_pct": pct(inv_b[0]["mean"]), "inv_seven_plus_ratio_pct": pct(inv_b[-1]["mean"]),
            "occ_first_year_ratio_pct": pct(occ_b[0]["mean"]), "occ_seven_plus_ratio_pct": pct(occ_b[-1]["mean"]),
            "inv_seven_plus_n": inv_b[-1]["n"], "occ_seven_plus_n": occ_b[-1]["n"],
            "inv_fitted_1y_pct": pct(f_at(fi, 1)), "inv_fitted_8y_pct": pct(f_at(fi, 8)),
            "occ_fitted_1y_pct": pct(f_at(fo, 1)), "occ_fitted_8y_pct": pct(f_at(fo, 8)),
            "fall_per_year_pct": "%.1f" % (100 * (1 - math.exp(fits["pooled"]["b"]))),
            "book_stale_share_pct": pct(C["stale_share"]), "record_stale_share_pct": pct(C["rec_stale"]),
            "book_facilities": len(loans), "book_exposure_display": "€%s billion" % ("%.2f" % (ead_tot / 1e9)),
            "book_exposure_eur": round(ead_tot),
            "record_mean_ratio_1dp": "%.1f" % (100 * fits["mean"]),
            "slope_se_ratio": "%d" % int(abs(fits["pooled"]["b"]) / C["slope_se"]),
            "slope_se_floor": "%d" % (10 * int(abs(fits["pooled"]["b"]) / C["slope_se"] / 10)),
            "slope_t_book_floor": "%d" % (10 * int(min(C["t_book"].values()) / 10)),
            "occ_level_gap_points": "%.0f" % (100 * (math.exp(fits["split"][False]["a"]) - math.exp(fits["split"][True]["a"]))),
            "investment_unrounded_display": "€%s million" % millions(g["investment"], 3),
            "owner_occupied_unrounded_display": "€%s million" % millions(g["owner_occupied"], 3),
            "plan_unrounded_display": "€%s million" % millions(g["total"], 3),
        },
        "rungs": {
            "carried_eur": round(res["carried"]["total"]), "carried_display": "€%s million" % millions(res["carried"]["total"], 2),
            "carried_rounded_display": "€%s million" % millions(rnd(res["carried"]["total"], UT), 1),
            "record_mean_eur": round(res["record_mean"]["total"]),
            "record_mean_display": "€%s million" % millions(res["record_mean"]["total"], 1),
            "record_mean_rounded_display": "€%s million" % millions(rnd(res["record_mean"]["total"], UT), 1),
            "record_mean_ratio_pct": pct(fits["mean"]),
            "cycle_drift_display": "€%s million" % millions(res["cycle_drift"]["total"], 1),
            "pooled_investment_display": "€%s million" % millions(rnd(res["pooled"]["investment"], UB)),
            "pooled_owner_occupied_display": "€%s million" % millions(rnd(res["pooled"]["owner_occupied"], UB)),
            "midyear_display": "€%s million" % millions(res["midyear"]["total"], 1),
            "haircut_pct": "22", "net_proceeds_pct": "78",
            "recent_from": 2022,
            "recent_defaults": len(recent), "recent_fresh_defaults": len(recent_fresh),
            "recent_mean_ratio_1dp": "%.1f" % (100 * float(np.mean([x["ratio"] for x in recent]))),
            "recent_fresh_ratio_pct": pct(float(np.mean([x["ratio"] for x in recent_fresh]))),
            "recent_stale_share_pct": pct(float(np.mean([x["tau"] >= 7 for x in recent]))),
            "recent_display": "€%s million" % millions(res["recent mean from 2022"]["total"], 1),
            "recent_rounded_display": "€%s million" % millions(rnd(res["recent mean from 2022"]["total"], UT), 1),
            "cycle_drift_rounded_display": "€%s million" % millions(rnd(res["cycle_drift"]["total"], UT), 1),
        },
        "constants": {"rounding_plan_eur": 500000, "rounding_split_eur": 250000, "as_if": "1 January 2027",
                      "record_from": 2012, "stale_years": 7, "window_days": 92, "report_year": 2026,
                      "snapshot_key": 20261231, "policy_master_scale": "4.1", "policy_shared_security": "4.4",
                      "policy_records": "4.6"},
    }
    return F, loans, inv_b, occ_b


def write_csv(path, loans):
    hdr = ["facility_no", "customer_no", "lending_book", "internal_grade", "probability_of_default", "exposure_eur",
           "security_value_carried_eur", "expected_security_value_at_default_eur", "loss_given_default",
           "expected_loss_2027_eur"]
    rows = sorted(loans, key=lambda x: (-x["el"], x["fac"]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(hdr)
        for x in rows:
            w.writerow([x["fac"], x.get("cust", ""), x["book"], x["grade"], "%.4f" % x["pd"], "%.2f" % x["ead"],
                        "%d" % round(x["carried"]), "%d" % round(x["vexp"]), "%.4f" % x["lgd"], "%d" % round(x["el"])])


def chart_png(inv_b, occ_b, fits, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task7",
                         "path.simplify": False})
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
    xs = np.linspace(0, 10, 101)
    cols = {"Investment": "#2F6690", GD.TRADING: "#C0622B"}
    for book, bands, F in (("Investment", inv_b, fits["split"][False]), (GD.TRADING, occ_b, fits["split"][True])):
        ax.plot(xs, [100 * math.exp(F["a"] + F["b"] * x) * F["smear"] for x in xs], color=cols[book], lw=2)
        mids = [(b["lo"] + min(b["hi"], 10)) / 2 for b in bands if b["mean"] is not None]
        ax.scatter(mids, [100 * b["mean"] for b in bands if b["mean"] is not None], color=cols[book], s=28, zorder=3)
        ax.text(10.1, 100 * math.exp(F["a"] + F["b"] * 10) * F["smear"], book, color=cols[book], va="center", fontsize=9)
    ax.axhline(100, color="#999999", lw=0.8, ls=":")
    ax.set_xlim(0, 11.6)
    ax.set_ylim(60, 104)
    ax.set_xlabel("Years from the last inspection to the default")
    ax.set_ylabel("Inspection at default, % of the value carried")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E5E5E5", lw=0.6)
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def write_pptx(path, F, loans, inv_b, occ_b, fits, png):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    NAVY = RGBColor(0x14, 0x42, 0x5E)
    GREY = RGBColor(0x44, 0x44, 0x44)

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.0))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.LEFT
        p.font.size, p.font.bold, p.font.color.rgb = Pt(26), True, NAVY
        if sub:
            q = tb.text_frame.add_paragraph()
            q.text = sub
            q.alignment = PP_ALIGN.LEFT
            q.font.size, q.font.color.rgb = Pt(14), GREY

    def bullets(slide, lines, top=1.7, size=16):
        tb = slide.shapes.add_textbox(Inches(0.7), Inches(top), Inches(11.9), Inches(5.0))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.font.size, p.font.color.rgb = Pt(size), GREY
            p.space_after = Pt(10)
        return tb

    def table(slide, rows, top, widths, size=14):
        shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(0.7), Inches(top), Inches(sum(widths)),
                                     Inches(0.45 * len(rows)))
        t = shp.table
        for j, wdt in enumerate(widths):
            t.columns[j].width = Inches(wdt)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                c = t.cell(i, j)
                c.text = str(v)
                for p in c.text_frame.paragraphs:
                    p.font.size = Pt(size)
                    p.font.bold = i == 0
        return t

    c, a, k, r = F["call"], F["asks"], F["components"], F["rungs"]
    s = prs.slides.add_slide(blank)
    title(s, "Commercial property credit loss: the 2027 plan line", "Credit Risk, for the executive committee, February 2027")
    bullets(s, ["Plan %s of credit loss on commercial property lending in 2027." % c["plan_figure_display"],
                "The line covers the %s facilities performing at 31 December 2026 (exposure %s): each facility's "
                "master-scale chance of default times its CRE-LGD-3 loss, as if it defaulted on 1 January 2027."
                % (format(k["book_facilities"], ","), k["book_exposure_display"]),
                "On the values the property register carries the model gives %s. Those values are index roll-forwards "
                "of old inspections; when a borrower defaults the bank's inspection has come in below them, the more so "
                "the longer since the last inspection." % r["carried_display"]], top=2.0, size=18)
    s = prs.slides.add_slide(blank)
    title(s, "The plan line by lending book")
    table(s, [["Lending book", "2027 expected credit loss"], ["Investment lending", a["investment_display"]],
              ["Owner-occupied lending", a["owner_occupied_display"]], ["Commercial property", c["plan_figure_display"]]],
          1.9, [5.0, 4.0], size=18)
    bullets(s, ["Owner-occupied hotels, pubs, nursing homes and childcare centres lose more of their value when the "
                "business behind them fails: at the same distance from the last inspection, their inspection at "
                "default has come in about %s points lower than an investment property's."
                % ("%.0f" % (100 * (math.exp(fits["split"][False]["a"]) - math.exp(fits["split"][True]["a"]))))],
            top=4.4, size=16)
    s = prs.slides.add_slide(blank)
    title(s, "The five facilities expected to cost the bank most in 2027")
    rows = [["Facility", "Lending book", "Grade", "Exposure", "Expected loss"]]
    lk = {x["fac"]: x for x in loans}
    for x in a["five_by_loss"]:
        L = lk[x["facility"]]
        rows.append([x["facility"], L["book"], str(L["grade"]), "€" + money(L["ead"]), "€" + money(L["el"])])
    table(s, rows, 1.9, [2.6, 2.6, 1.2, 2.4, 2.4], size=16)
    s = prs.slides.add_slide(blank)
    title(s, "What the bank's own defaults show", "Defaults since 2012: the inspection at default against the value "
          "carried on the default date")
    s.shapes.add_picture(png, Inches(0.7), Inches(1.7), width=Inches(8.4))
    side = bullets(s, ["A year after the last inspection, the bank's inspection at default comes in at %s%% of the value "
                       "carried for investment property and %s%% for owner-occupied (the fitted line)."
                       % (k["inv_fitted_1y_pct"], k["occ_fitted_1y_pct"]),
                       "Eight years after it, %s%% and %s%%." % (k["inv_fitted_8y_pct"], k["occ_fitted_8y_pct"]),
                       "%s%% of the year-end book's exposure rests on an inspection seven or more years old, against "
                       "fewer than one in ten of the properties in the record." % k["book_stale_share_pct"]],
                   top=1.9, size=13)
    side.left, side.width = Inches(9.3), Inches(3.6)
    s = prs.slides.add_slide(blank)
    title(s, "Basis")
    bullets(s, ["Population: commercial property facilities performing at 31 December 2026; facilities in default "
                "and 2027 lending sit in other lines.",
                "Chance of default: the 2025 master scale at each facility's year-end grade.",
                "Exposure: the year-end balance. Loss: CRE-LGD-3, max(0, EAD - (1 - 22%) x V) / EAD, with V the "
                "expected value of the security at default, shared between facilities in proportion to exposure.",
                "V: the register's carried value times the expected ratio of the inspection at default to the value "
                "carried, by years since the last inspection and lending book, fitted on the defaults since 2012.",
                "Property prices held at their latest published level through 2027."], top=1.7, size=15)
    cp = prs.core_properties
    cp.author, cp.last_modified_by = "Geraldine Harkins", "Geraldine Harkins"
    cp.title = "Commercial property credit loss: 2027 plan line"
    cp.comments, cp.subject, cp.keywords, cp.category = "", "", "", ""
    cp.revision = 4
    prs.save(path)
    postprocess.scrub(path, "Ardcarn Bank", "2027-01-19")
    postprocess.finish_office(path, "2027-01-15T09:20:00Z", "2027-01-19T17:44:00Z", "Ardcarn Bank")


def write_all(C, golden_dir, gen_dir, scratch):
    F, loans, inv_b, occ_b = figures(C)
    T = C.get("T")
    os.makedirs(golden_dir, exist_ok=True)
    write_csv(os.path.join(golden_dir, "cre_expected_loss_2027_by_loan.csv"), loans)
    png = os.path.join(scratch, "record_chart.png")
    chart_png(inv_b, occ_b, C["fits"], png)
    write_pptx(os.path.join(golden_dir, "exco_cre_credit_loss_2027.pptx"), F, loans, inv_b, occ_b, C["fits"], png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    return F
