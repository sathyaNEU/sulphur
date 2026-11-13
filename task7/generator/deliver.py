"""task7 architecture 11: the golden deliverables, the board memo (Word) and the CSV of every transformer serving the
rate's chargers, with every figure from checks on the cut pack."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402

import checks as CK  # noqa: E402
import golden as G  # noqa: E402
import postprocess  # noqa: E402

INK = "#2F4B2F"
ORG = "Hollins Creek Electric Association"


def usd(x):
    return "$" + format(int(round(x)), ",")


def write_csv(path, C):
    S = C["S"]
    P = C["P"]
    rows = []
    for t, r in S["out"].items():
        rows.append([t, P.area.get(t, ""), "%g" % r["kva"], "%.1f" % r["limit"], r["homes"], r["chargers"],
                     "%.1f" % r["own_peak"], "yes" if r["own_p"] > 0.5 else "no",
                     "%.1f" % r["stagger_peak"], "%.2f" % r["stagger_p"],
                     "%.1f" % r["sequence_peak"], "yes" if r["sequence_p"] > 0.5 else "no",
                     r["cost"]])
    rows.sort(key=lambda x: (x[1], x[0]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["transformer_location", "substation", "kva", "limit_kw_15min", "homes", "enrolled_chargers",
                     "own_schedules_peak_kw", "own_schedules_over", "stagger_mean_peak_kw", "stagger_chance_over",
                     "sequence_peak_kw", "sequence_over", "replacement_cost_usd"])
        for r in rows:
            wr.writerow(r)


def chart(F, scratch):
    sizes = list(F["sizes"].keys())
    labels = ["Members' own\nschedules", "Quillpoint\nStagger", "Quillpoint\nSequence"]
    cols = ["#9DB89D", "#5E8C61", "#2F4B2F", "#C9A227", "#8C6A1F"]
    fig, ax = plt.subplots(figsize=(6.2, 2.7), dpi=150)
    bottom = [0.0, 0.0, 0.0]
    for i, s in enumerate(sizes):
        vals = [F["by_size"][o].get(s, 0.0) for o in G.OPTIONS]
        ax.bar(labels, vals, bottom=bottom, color=cols[i % len(cols)], label="%s kVA" % s, width=0.55)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for x, b, o in zip(range(3), bottom, G.OPTIONS):
        ax.text(x, b + 0.8, ("%.1f" % F[o]["over"]) if o == "stagger" else "%d" % F[o]["over"], ha="center", fontsize=8.5)
    ax.set_ylabel("Transformers over their limit", fontsize=8)
    ax.set_title("A summer like 2026 under each default (July and August)", fontsize=9, color=INK)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7, frameon=False, ncol=5, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(bottom) * 1.25)
    fig.tight_layout()
    p = os.path.join(scratch, "options.png")
    fig.savefig(p, metadata={"Software": None})
    plt.close(fig)
    return p


def write_memo(path, F, png):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Mm(22))
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)

    def para(text, bold=False, size=None, color=None, space=4):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color.lstrip("#"))
        p.paragraph_format.space_after = Pt(space)
        return p
    o, s, q = F["own"], F["stagger"], F["sequence"]
    para(ORG + ", Distribution Planning", size=8.5, color="#555555", space=1)
    para("To: the board of directors    From: Eileen Casey, manager of distribution planning    Date: 12 November 2026",
         size=8.5, color="#555555", space=1)
    para("Make Quillpoint Sequence the EV Overnight default for 2027; the work plan replaces %d transformers" % q["over"],
         bold=True, size=13.5, color=INK, space=6)
    para("Set the EV Overnight rate's charging default for 2027 to Quillpoint Sequence and carry %d transformer replacements "
         "(%s) in the 2027 work plan. Under Board Policy EV-4 it is the cheapest of the three options at %s for the year, "
         "against %s for Quillpoint Stagger and %s for leaving members on their own schedules." %
         (q["over"], usd(q["replace"]), usd(q["total"]), usd(s["total"]), usd(o["total"])), bold=True, space=5)
    t = doc.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    hdr = ["Option", "Transformers over their limit", "Platform fee", "Replacements", "Total for 2027"]
    for c, h in zip(t.rows[0].cells, hdr):
        c.text = h
        for r in c.paragraphs[0].runs:
            r.bold = True
            r.font.size = Pt(8.5)
    for key, name in CK.NAMES.items():
        v = F[key]
        cells = t.add_row().cells
        cnt = ("%.1f" % v["over"]) if key == "stagger" else "%d" % v["over"]
        for c, x in zip(cells, [name, cnt, usd(v["fee"]), usd(v["replace"]), usd(v["total"])]):
            c.text = x
            for r in c.paragraphs[0].runs:
                r.font.size = Pt(8.5)
    para("A summer like 2026: July and August 2026 as metered, the homes' hourly reads brought to the quarter-hour by "
         "DPS-7's peaking factors, with the %s chargers enrolled on 1 November 2026 charging "
         "their 2026 sessions as each option would. Stagger starts sessions at random, so its expected cost counts each "
         "transformer at its chance of being over (EV-4 4.3). Fees at $%g and $%g per charger for the year; replacements at DPS-7's installed "
         "costs." % (format(F["n_chargers"], ","), F["fee_rate"]["stagger"], F["fee_rate"]["sequence"]),
         size=8, color="#555555", space=6)
    doc.add_picture(png, width=Mm(160))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para("What the pilot showed, and what it did not", bold=True, color=INK, space=2)
    para("The pilot's managed quarter took %.2f kW per enrolled charger off the 23:00 to 23:15 interval in July and "
         "August against the chargers on their owners' own schedules (%.2f kW against %.2f), because most own schedules "
         "start the car at 23:00 when the overnight price begins. Read as an average night, that looks as if a random "
         "start clears almost every transformer. It does not: a transformer's limit is its single highest quarter-hour "
         "of the summer, and the two to five chargers on a small transformer still land together on some night when "
         "each starts at random. Replayed night by night over the summer, Stagger still leaves %.1f transformers over." %
         (abs(F["pilot_effect"]), F["pilot_managed"], F["pilot_own"], s["over"]))
    para("Sequence was not in the pilot. Run on each night's actual plug-ins, energy and unplug times, it keeps the "
         "chargers on a transformer apart most nights, but on nights when they need more charging than the hours to "
         "their departures allow, its rule starts a late charger alongside the others and the queue waits for it: %d "
         "transformers stay over." %
         q["over"])
    para("Members' own schedules are not what the meters saw in 2026, because a quarter of the chargers were under "
         "Stagger. With every charger back on its owner's own setting (its own-schedule sessions, or what the member "
         "told us at enrolment) %d transformers would be over." % o["over"])
    para("Sequence stays the cheapest unless its fee rises above about $%d per charger for the year. The CSV gives "
         "every transformer serving the rate's chargers, its limit, and its summer peak under each option." % F["flip_fee"],
         space=2)
    doc.save(path)
    postprocess.normalize_docx(path, "Eileen Casey", "Eileen Casey", "2026-11-09T16:02:00Z", "2026-11-12T22:48:00Z", 7, 186,
                               "task7-memo", title="EV Overnight charging default for 2027", company=ORG)


def write_all(C, golden_dir, gen_dir, scratch):
    F = CK.figures(C)
    write_csv(os.path.join(golden_dir, "ev_overnight_transformers_2027.csv"), C)
    png = chart(F, scratch)
    write_memo(os.path.join(golden_dir, "ev_overnight_default_2027_memo.docx"), F, png)
    import json
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False, default=float)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(CK.effort(C, F), fh, indent=1, ensure_ascii=False, default=float)
    return F
