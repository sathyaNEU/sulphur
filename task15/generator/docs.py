"""task15: the pack's documents. Each PDF is a Word document exported by LibreOffice Writer (officepdf.py); the
season review stays a Word document.

They file the WHAT: what the series grows, harvests and publishes and how it defines a relative yield; the seed
partner's uptake standard; how Banyena's stages run, what a lodging figure and an abandoned plot are, and what the
high-rainfall index quoted in a nomination is. They say nothing of why a nomination realises what it does, how a
line's yield is to be estimated, what compares with what, or how a chance is to be worked out.
"""
import datetime as dt
import os

from docx import Document
from docx.shared import Mm, Pt
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import golden as G
import officepdf
import postprocess as PP
import world as W

AEDT = dt.timezone(dt.timedelta(hours=11))
AEST = dt.timezone(dt.timedelta(hours=10))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#22382B")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#22382B")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def series_protocol(target):
    ED = W.LAST - 2
    sites = [["Site", "District", "Soil"]] + [[s[0], s[1], s[4]] for s in W.SERIES_SITES]
    s = [P("Southern Cropping Trials Trust", SMALL),
         P("High Rainfall Barley Series: trial protocol", H1),
         P("%d edition, in force from the %d sowing. It replaces the %d edition; sections 5 to 7 are unchanged "
           "from the Series' first season." % (ED, ED, ED - 5), SMALL),
         P("1 Purpose", H2),
         P("The High Rainfall Barley Series compares barley varieties and breeders' advanced lines in the high-rainfall "
           "cropping districts of south-west Victoria, independently of the breeders, and publishes what each entry "
           "yields at each site."),
         P("2 Sites and trials", H2),
         P("One trial is sown at each of the ten sites below each season, between late May and the middle of June, on "
           "a paddock the host grower would crop to barley. A trial that is lost before harvest is not a trial of the "
           "Series for that season, and the Trust publishes no results for it."),
         T(sites, [110, 130, 150]),
         P("3 Entries", H2),
         P("Three standard varieties, Byaduk, Wando and Carapook, are sown in every trial. A breeder nominates new "
           "entries for a sowing year by the last Friday of February and may nominate up to three; a nominated entry "
           "is sown in every trial of that season and of the next. Entries are listed under the name or number the "
           "breeder nominates them by."),
         P("4 Layout and husbandry", H2),
         P("Each trial has three replicates in incomplete blocks, plots of eight rows by ten metres, sown at 150 "
           "plants a square metre with the district's usual fertiliser. Fungicide and herbicide follow the host "
           "grower's programme. No growth regulator is applied."),
         P("5 Measurements", H2),
         P("Lodging is assessed at maturity as the percentage of the plot that has lodged. Every plot is harvested, "
           "lodged plots included, and grain yield is reported in tonnes a hectare at 12.5 per cent moisture."),
         P("6 Publication", H2),
         P("For each trial the Trust publishes every entry's mean grain yield and mean lodging over its plots, with the "
           "trial's sowing and harvest dates, the April to October rain at the site, the trial's mean yield and its "
           "coefficient of variation."),
         P("7 Relative yield", H2),
         P("An entry's relative yield over a set of trials is its mean grain yield over those trials as a percentage of "
           "Byaduk's mean grain yield over the same trials."),
         P("8 Enquiries", H2),
         P("John Morgan, Series Coordinator, Southern Cropping Trials Trust, Hamilton.")]
    path = os.path.join(target, W.FILES["protocol"])
    officepdf.build(path, s, "High Rainfall Barley Series: trial protocol, %d edition" % ED, "John Morgan",
                    "HRBS trial protocol", "Southern Cropping Trials Trust | HRBS trial protocol | %d edition" % ED,
                    dt.datetime(ED, 1, 24, 10, 42, tzinfo=AEDT), dt.datetime(ED, 2, 2, 15, 7, tzinfo=AEDT),
                    producer="LibreOffice 7.4")
    return path


def option_schedule(target):
    DY = W.FIRST_SOW - 1
    std = "%.1f" % W.STANDARD
    s = [P("Line Evaluation and Option Deed between Banyena Grain Genetics Pty Ltd and Mount Rouse Seeds Pty Ltd", SMALL),
         P("Schedule 2: nominations and the uptake standard", H1),
         P("Executed 8 September %d. This schedule is read with clauses 6 and 7 of the Deed." % DY, SMALL),
         P("1 Nominations", H2),
         P("1.1 Banyena may nominate up to three barley lines to the High Rainfall Barley Series of the Southern "
           "Cropping Trials Trust (the Series) for each sowing year, by the Series' closing date for that year."),
         P("1.2 Banyena meets the Series' entry fees and supplies the seed. A line is nominated once."),
         P("2 The uptake standard", H2),
         P("2.1 Mount Rouse will exercise its option over a nominated line whose relative yield, as the Series "
           "defines it, over the Series trials of the line's first two seasons is %s or more." % std),
         P("2.2 Mount Rouse may, but need not, exercise its option over a nominated line that does not meet the "
           "standard in 2.1."),
         P("3 On exercise", H2),
         P("3.1 Mount Rouse meets the costs of seed increase and of plant breeder's rights from the date of exercise "
           "and pays Banyena the end-point royalty share in Schedule 3."),
         P("3.2 Where Mount Rouse does not exercise its option within six months of the Trust publishing the line's "
           "second season, the line returns to Banyena free of this Deed."),
         P("4 Review of nominations", H2),
         P("4.1 Either party may ask for a review of the nominations made under this schedule before Banyena "
           "nominates for a sowing year."),
         P("4.2 A review takes the nominated lines for which the Trust has published both seasons. It states the "
           "mean of the index Banyena quoted for those lines, the mean of their relative yield over the Series "
           "trials of their two seasons, and the difference between the two under four heads, each a mean over the "
           "lines in points of relative yield:"),
         P("(a) the index: the index quoted for a line less the relative yield to be expected of the line at the "
           "trials the index was taken from;"),
         P("(b) the move to the Series: the relative yield to be expected of the line at the trials the index was "
           "taken from less that to be expected of it at the Series trials of its two seasons, apart from head (c);"),
         P("(c) lodging: the relative yield the line lost to lodging beyond what Byaduk lost at those Series trials, "
           "less the same at the trials the index was taken from, on the lodging recorded;"),
         P("(d) the remainder: the relative yield to be expected of the line at those Series trials less the "
           "relative yield it returned."),
         P("5 Notices", H2),
         P("Notices under this schedule go to the head of breeding at Banyena and to the variety manager at Mount "
           "Rouse.")]
    path = os.path.join(target, W.FILES["deed"])
    officepdf.build(path, s, "Line Evaluation and Option Deed: Schedule 2", "Mount Rouse Seeds Pty Ltd",
                    "Option deed, Schedule 2", "Banyena Grain Genetics and Mount Rouse Seeds | Option Deed | Schedule 2",
                    dt.datetime(DY, 9, 6, 16, 18, tzinfo=AEST), dt.datetime(DY, 9, 8, 9, 51, tzinfo=AEST),
                    producer="LibreOffice 5.1")
    return path


def trial_handbook(target):
    HY = W.LAST - 1
    stages = [["Stage", "Lines", "Sites", "Replicates"],
              ["Stage 1", "each year's new lines", "Horsham and Birchip", "2"],
              ["Stage 2", "lines advanced from Stage 1", "Walpeup, Hopetoun, Minyip, Kaniva and Lake Bolac", "2"],
              ["Stage 3", "lines advanced from Stage 2, and the lines kept for a second Stage 3 season",
               "all ten trial sites", "3"]]
    s = [P("Banyena Grain Genetics", SMALL),
         P("Barley programme: trial handbook", H1),
         P("%d revision. Trials and data team. It replaces the %d handbook." % (HY, HY - 4), SMALL),
         P("1 The stages", H2),
         P("A line is tested for up to four seasons. Lines are advanced at the season review in January on the "
           "season's trials."),
         T(stages, [55, 190, 190, 55]),
         P("2 Line codes", H2),
         P("A line carries its cross code (the year of the cross's first trial, the cross number and the plant "
           "selection) through Stage 1 and Stage 2. On entering Stage 3 it is given a WI number, which it keeps; "
           "nominations and seed lots use the WI number. The line register holds both."),
         P("3 Check varieties", H2),
         P("Byaduk, Wando, Carapook and Nareen are sown in every trial, each twice in every replicate."),
         P("4 Layout", H2),
         P("Trials are sown in replicates of incomplete blocks, one block to a range. Plots are eight rows wide and are "
           "trimmed to the harvested length before harvest."),
         P("5 Plot records", H2),
         P("Lodging is recorded at maturity as the percentage of the plot that has lodged, to the nearest five. "
           "A plot the harvester cannot pick up is abandoned: it is recorded as not harvested and has no weight. "
           "The weight off each harvested plot is taken at field moisture with a moisture reading, and the yield is "
           "stored at 12.5 per cent moisture. Where a sample is weighed again, the later weighing stands."),
         P("6 The high-rainfall index", H2),
         P("The high-rainfall index quoted in a nomination to the High Rainfall Barley Series is the mean, over the "
           "line's Stage 3 trials at Lake Bolac, Skipton and Kerang, of the line's mean yield over its harvested plots "
           "in the trial as a percentage of Byaduk's in the same trial."),
         P("7 Irrigation at Kerang", H2),
         P("The Kerang trials are watered from the channel through the spring. Every watering is entered in the "
           "irrigation log with the depth applied."),
         P("8 Seed", H2),
         P("Seed of every Stage 3 line is cleaned after harvest and held in the seed store under its WI number, "
           "with the lot's purity and germination.")]
    path = os.path.join(target, W.FILES["handbook"])
    officepdf.build(path, s, "Barley programme: trial handbook, %d revision" % HY, "Jesse Gibson",
                    "Trial handbook", "Banyena Grain Genetics | Barley programme | Trial handbook %d" % HY,
                    dt.datetime(HY, 3, 11, 9, 26, tzinfo=AEDT), dt.datetime(HY, 3, 13, 13, 40, tzinfo=AEDT),
                    producer="LibreOffice 24.2")
    return path


def season_review(target, w, facts, counts):
    """The trials manager's close-out of the last season: what was sown and harvested, the season, the plots lost."""
    y = W.LAST
    tr = {c: t for c, t in w["trials"].items() if not t["series"] and t["season"] == y}
    n_plots = sum(1 for p in w["plots"] if p[0] in tr)
    ab = {}
    for p in w["plots"]:
        if p[0] in tr and p[10]:
            ab[tr[p[0]]["site"]] = ab.get(tr[p[0]]["site"], 0) + 1
    rain = {s[0]: float(sum(w["env"][(s[0], y)]["months"])) for s in W.PROGRAMME_SITES}
    mean = {s[0]: float(sum(sum(w["env"][(s[0], yy)]["months"]) for yy in w["years"]) / len(w["years"]))
            for s in W.PROGRAMME_SITES}
    first = min(facts[c]["sown"] for c in tr)
    last_h = max(facts[c]["harvest"] for c in tr)
    irr = w["env"][("Kerang", y)]["irrigation"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    h = doc.add_paragraph()
    r = h.add_run("Barley programme: %d season review" % y)
    r.bold = True
    r.font.size = Pt(14)
    doc.add_paragraph("Trials and data team, 9 February %d. For the season review meeting." % W.SOW)

    def para(t):
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(6)
        return p

    def head(t):
        p = doc.add_paragraph()
        rr = p.add_run(t)
        rr.bold = True
        return p

    head("Trials")
    para("All %d trials were sown and harvested: Stage 1 at Horsham and Birchip, Stage 2 at the five Stage 2 sites and "
         "Stage 3 at all ten. Sowing ran from %s to %s and the last plot came off on %s. %s plots were sown in all."
         % (len(tr), first.strftime("%-d %B"), max(facts[c]["sown"] for c in tr).strftime("%-d %B"),
            last_h.strftime("%-d %B"), format(n_plots, ",")))
    head("The season")
    wet = sorted(rain, key=lambda s_: rain[s_] - mean[s_])
    para("April to October rain was %d mm at Horsham against %d mm on average over our seasons there, %d mm at "
         "Walpeup (%d) and %d mm at Skipton (%d). %s was furthest below its own average (%d mm against %d) and %s "
         "furthest above (%d against %d)."
         % (round(rain["Horsham"]), round(mean["Horsham"]), round(rain["Walpeup"]), round(mean["Walpeup"]),
            round(rain["Skipton"]), round(mean["Skipton"]), wet[0], round(rain[wet[0]]), round(mean[wet[0]]), wet[-1],
            round(rain[wet[-1]]), round(mean[wet[-1]])))
    para("Kerang was watered %d times between %s and %s, %d mm in all." % (
        len(irr), (dt.date(y, 1, 1) + dt.timedelta(days=irr[0][0] - 1)).strftime("%-d %B"),
        (dt.date(y, 1, 1) + dt.timedelta(days=irr[-1][0] - 1)).strftime("%-d %B"), sum(mm for _, mm in irr)))
    head("Plots not harvested")
    if ab:
        parts = ", ".join("%d at %s" % (n, s_) for s_, n in sorted(ab.items(), key=lambda kv: -kv[1]))
        para("%d plots were abandoned as too lodged for the harvester: %s. They are in the harvest record as abandoned "
             "with their lodging figure." % (sum(ab.values()), parts))
    else:
        para("No plot was abandoned this season.")
    head("Equipment and people")
    para("The plot harvester's weigh cell was recalibrated before Hopetoun and again before Lake Bolac. Samples that "
         "read oddly on the day were weighed again in the shed. Two casuals joined for harvest from 9 November.")
    head("Seed and dates")
    last_friday = max(d for d in (dt.date(W.SOW, 2, k) for k in range(1, 29)) if d.weekday() == 4)
    para("Seed of every Stage 3 line is cleaned and in the store. Nominations to the High Rainfall Barley Series for "
         "%d close on Friday %d February. The Trust published the Series' %d results on 5 February."
         % (W.SOW, last_friday.day, y))
    path = os.path.join(target, W.FILES["review"])
    doc.save(path)
    PP.normalize_docx(path, "Jesse Gibson", "Jesse Gibson", "%d-02-03T03:12:00Z" % W.SOW, "%d-02-08T22:03:00Z" % W.SOW,
                      revision=6, total_time=148, seed=1503, title="Barley programme: %d season review" % y,
                      company="Banyena Grain Genetics")
    return path


def write_all(target, w, facts, counts):
    return [series_protocol(target), option_schedule(target), trial_handbook(target),
            season_review(target, w, facts, counts)]
