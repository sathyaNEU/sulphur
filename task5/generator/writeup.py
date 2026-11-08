"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    q = f["qualifying"]
    rv = f["rivals"]
    t = f["totals"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Survey Research & Official Statistics (Census, register & administrative-data quality: a "
        "municipality's vacancy share estimated from the cadastre, the meter data hub's metering points and hourly "
        "values and the population register, with the register's overcoverage, undercoverage and net bias).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## Final Recommendation",
        "",
        "**%s of the ten municipalities qualify for the 2027 grant: %s.**" % (
            f["count_word"], _join(["%s (%s)" % (r["name"], r["nr"]) for r in q])),
        "Their vacancy shares run from %s to %s per cent against the regulation's %s; the highest share below the line "
        "is %s's %s per cent. Not none, which a consumption floor anywhere from %s to %s kWh a day gives, because an "
        "empty dwelling in November is left heated and uses more electricity than many lived-in ones; not %s alone, "
        "which a morning or evening rise over the night gives, because %d empty dwellings were heated on a timer that "
        "rises at the same hours every day; and not all %d, which the population register's empty dwellings give, "
        "because the regulation counts who lived there, not who was registered." % (
            min(r["share"] for r in q), max(r["share"] for r in q), f["threshold"], f["highest_below"]["name"],
            f["highest_below"]["share"], rv["floor_low"], rv["floor_high"], _join(f["rise_set"]), f["timer_vacant"],
            rv["register_count"]),
        "",
    ]
    cc_lines = [
        "## Critical Components",
        "",
        "1. Counted dwellings in the county: **%s**; vacant in the fortnight: **%s**." % (t["counted"], t["vacant"]),
        "2. A dwelling was lived in when some hour of some day ran more than **%s kWh** above its own typical day (each "
        "day set at its night hours); vacant when its days repeated. **%d** vacant dwellings heated on a timer rise "
        "every morning and evening, so a rise over the night alone reads them as lived in and leaves %s." % (
            f["cut"], f["timer_vacant"], _join(f["rise_set"])),
        "3. Vacant dwellings still carrying a registered resident on 1 November: **%s**; lived-in dwellings with "
        "nobody registered: **%s**." % (f["vacant_registered"], f["lived_unregistered"]),
        "",
    ]
    qc = f["quality_county"]
    sq = [
        "## Supplementary Questions",
        "",
        "### %s" % W.GOLDEN["docx"],
        "",
        "1. Qualifying municipalities, named first in the letter: %s." % _join(
            ["%s (%s per cent)" % (r["name"], r["share"]) for r in q]),
        "2. A table of all ten municipalities with counted dwellings, vacant dwellings, vacancy share and its 90 per "
        "cent interval, and whether each qualifies; the intervals of %s lie wholly above %s per cent:" % (
            _join(f["wholly_above"]), f["threshold"]),
    ]
    for m in f["municipalities"]:
        sq.append("   - %s (%s): %s vacant of %s counted dwellings, %s per cent%s" % (
            m["name"], m["nr"], m["vacant"], m["counted"], m["share"], ", qualifies" if m["qualifies"] else ""))
    sq += [
        "3. A bar chart of the ten vacancy shares with their 90 per cent intervals against a line at %s per cent, the "
        "qualifying municipalities highlighted." % f["threshold"],
        "4. The population register beside the vacancy figures, by municipality: overcoverage (dwellings, rate), "
        "undercoverage (dwellings, rate) and net bias, per cent:",
    ]
    for r in f["quality"]:
        sq.append("   - %s (%s): overcoverage %s (%s), undercoverage %s (%s), net bias %s" % (
            r["name"], r["nr"], r["over"], r["over_rate"], r["under"], r["under_rate"], r["net_bias"]))
    sq += [
        "   - County: overcoverage %s (%s), undercoverage %s (%s), net bias %s" % (
            qc["over"], qc["over_rate"], qc["under"], qc["under_rate"], qc["net_bias"]),
        "",
        "### %s" % W.GOLDEN["xlsx"],
        "",
        "5. One row per counted dwelling, %s rows, with municipality number and name, dwelling ID, address, unit, "
        "persons registered on 1 November 2026 (%s in all) and vacant yes or no (%s yes); a sheet by municipality "
        "carries the figures of answers 2 and 4." % (t["counted"], t["persons"], t["vacant"]),
        "",
    ]
    steps = [
        "## Step-by-Step",
        "",
        "1. Took the cadastre's units of type Bolig in use on or before 1 November 2026 (Section 3): %s dwellings." % (
            t["counted"]),
        "2. Joined each to its household metering points by bruksenhet_id, else by municipality and address for a "
        "single-unit house; Snøholt's points carry Fjordeid's old municipality number.",
        "3. Put the hourly values on Norwegian time (UTC+1), kept the later delivery where an estimated day was "
        "replaced, and added a dwelling's two points where its meter changed.",
        "4. Read occupancy as a consumption floor first: vacant dwellings used a median %s kWh a day against %s for "
        "lived-in ones, so any floor from %s to %s kWh designates no municipality; read it from the register's empty "
        "dwellings and all %d qualify. Both are rejected." % (
            f["vacant_median_kwh"], f["lived_median_kwh"], rv["floor_low"], rv["floor_high"], rv["register_count"]),
        "5. Took the household's rise next: the mean of 06 to 09 or of 16 to 22 above the mean of 01 to 05 on any "
        "day. It separates cleanly and agrees with the register, but it leaves %s vacant and only %s qualifying, "
        "because %d vacant dwellings heated on a timer rise at the same hours by the same amount every day. Rejected "
        "as the reading of occupancy." % (f["rise_vacant"], _join(f["rise_set"]), f["timer_vacant"]),
        "6. Set each day against its own night hours and each dwelling against its typical day (the median of its "
        "days, hour by hour), and took the largest excess of any hour: no vacant dwelling exceeds %s kWh and every "
        "lived-in one reaches %s, so any cut in that gap marks the same dwellings; a household on any day makes the "
        "dwelling lived in (Section 4): %s vacant. A timer read as days alike gives the same dwellings when its cut "
        "sits in that statistic's own gap." % (f["dep_vacant_max"], f["dep_lived_min"], t["vacant"]),
        "7. Divided each municipality's vacant dwellings by its counted dwellings, rounded to one decimal, and "
        "designated those at 5.0 per cent or more (Section 6); each share's 90 per cent exact binomial interval on "
        "its counted dwellings lies wholly above the line for %s." % _join(f["wholly_above"]),
        "8. Rolled the population register of 5 January 2027 back to 1 November by undoing every later event, "
        "reading the November block renumberings as a change of unit number and every old number written before a "
        "block's day as the flat one floor up: the register held someone in %s counted dwellings and nobody in %s." % (
            qc["held"], qc["none"]),
        "9. Set the register beside the vacancy reading in the assignment's terms: overcoverage %s dwellings (%s per "
        "cent), undercoverage %s (%s per cent), net bias %s per cent of counted dwellings." % (
            qc["over"], qc["over_rate"], qc["under"], qc["under_rate"], qc["net_bias"]),
        "",
        "No other designation survives. A level of use cannot separate an empty dwelling that is heated from a "
        "lived-in one, so every floor gives none; the register gives all ten because two in three of the dwellings "
        "where it holds nobody were lived in; a morning or evening rise gives %s alone because a heating timer rises "
        "too; and the regulation decides on the share, which the departure from each dwelling's own typical day "
        "fixes at the same five for any cut the data allow." % _join(f["rise_set"]),
        "",
    ]
    lines = lines + sq + cc_lines + steps
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
