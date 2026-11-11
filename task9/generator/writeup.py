"""task9: submission.md, the four answer blocks, written from the figures as computed (F) and as stated (F["stated"])."""
import golden as GD
import params as P

STATED = []          # every figure the blocks state, as they state it; figures.json carries them for figures_check
FAM_ORDER = GD.FAM_ORDER


def _say(*xs):
    STATED.extend(str(x) for x in xs)


def n(v):
    s = "{:,}".format(int(round(v)))
    _say(s)
    return s


def pct(v, k=1):
    s = ("%." + str(k) + "f") % (100 * v)
    _say(s)
    return s + " per cent"


def dec(v, k=1):
    s = ("%." + str(k) + "f") % v
    _say(s)
    return s


def rng(b, f=n):
    return "%s to %s" % (f(b[0]), f(b[1]))


def build(F):
    del STATED[:]
    g, S, B = F["gold"], F["stated"], F["bands"]
    R = F["routes"]
    q = F["quick"]
    car = R["careful but hurried"]
    be = P.COSTS["migrate_vault"] / (P.VAULT_DRIVES * P.COSTS["failure_handling"])
    w0, w1 = (GD.week_label(x) for x in g["hot_window"])
    y0, k0 = g["hot_window"][0].split("-W")
    y1, k1 = g["hot_window"][1].split("-W")
    w0, w1 = ("weeks %d" % int(k0), "%d of %s" % (int(k1), y1)) if y0 == y1 else (w0, w1)
    fw = R["the firmware release as the batch"]
    pooled = R["one curve per family over every vault"]
    pois = R["Poisson counts at the fitted values"]
    ages = R["ages from the inventory"]
    fam = R["the hot batch inside its family"]
    allrem = R["every removal in the age curve"]
    src = F["record"]["age_sources"]
    L = []
    a = L.append

    # ---- 1. Final Recommendation
    mig = list(S["rec"]["migrate"])
    keep = sorted(v for v in S["vaults"] if v not in mig)
    vs = lambda xs: (", ".join(xs[:-1]) + " and " + xs[-1]) if len(xs) > 1 else (xs[0] if xs else "none")
    a("## Final Recommendation")
    a("")
    a("Plan on about %s drive replacements from October 2026 to September 2027 (80 per cent interval %s), rising from %s in "
      "the fourth quarter to %s in the third quarter of 2027, and migrate vaults %s this quarter, leaving %s to run: the "
      "HX-8 drives built in %s to %s are failing at an accelerating rate and fill those vaults, while %s holds only %s of them "
      "and its own replacements over 24 months (%s) fall short of the %s a migration needs; migration stays the cheaper "
      "choice unless the batch's rate doubles more slowly than every %s months. Rejected: the close-out's rates carried "
      "forward (about %s replacements and no migration), blaming the HX8.2.0 firmware (which takes in %s drives that are "
      "not failing, migrates all five vaults and moves the flip point to %s months), and migrating every vault on the "
      "batch's average." % (
          n(S["total"]), rng(S["total_band"]), n(S["path"][P.FORECAST_Q[0]]), n(S["path"][P.FORECAST_Q[-1]]), vs(mig), vs(keep),
          w0, w1, vs(keep), vs([n(S["vaults"][v]["batch"]) for v in keep]), vs([n(S["vaults"][v]["mean"]) for v in keep]),
          n(P.COSTS["migrate_vault"] / P.COSTS["failure_handling"]), dec(S["rec"]["flip"]), n(q["total"]),
          n(fw["hot_batch"]["drives"] - S["hot_batch"]["drives"]), dec(fw["rec"]["flip"])))
    a("")

    # ---- 2. Supplementary Questions
    a("## Supplementary Questions")
    a("")
    a("1. The spreadsheet (%s) has six sheets. \"Quarterly path\" gives, for each quarter from 2026-Q4 to 2027-Q3, the mean "
      "replacements with P10 and P90 (%s, %s, %s and %s; four quarters %s, P10 %s, P90 %s, a width of %s), the means by data "
      "centre (DC-1 %s, DC-2 %s, DC-3 %s over the four quarters), and each data centre's four-quarter interval. Each quarter's "
      "mean is graded against the band %s, %s, %s and %s respectively; the four-quarter interval's width is graded against %s. "
      "\"By family\" gives each family's mean per quarter and its four-quarter total with its interval." % (
          GD.BOOK, *(n(S["path"][qq]) for qq in P.FORECAST_Q), n(S["total"]), n(S["total_band"][0]), n(S["total_band"][1]),
          n(S["total_width"]), n(S["by_dc"]["DC-1"]), n(S["by_dc"]["DC-2"]), n(S["by_dc"]["DC-3"]),
          *(rng(B["path"][qq]) for qq in P.FORECAST_Q), rng(B["total_width"])))
    vt = "; ".join("%s %s drives, %s of the batch, %s expected replacements, %s" % (
        v, n(s["drives"]), n(s["batch"]), n(s["mean"]), "migrate" if v in S["rec"]["migrate"] else "run to failure")
        for v, s in sorted(S["vaults"].items()))
    a("2. \"HX-8 bad builds\" names the batch (HX-8 drives built in %s to %s, read from the serial's YYWW), its %s drives in "
      "service on 30 September 2026 (band %s), their annualized replacement rate over July to September 2026 of %s (band "
      "%s to %s, replacements per drive-year in service), their replacements over the four quarters, %s (band %s), the "
      "expected share of them replaced within 24 months (%s against the break-even %s: USD %s over 1,200 drives at USD %s "
      "each), and the doubling time above which a vault made wholly of the batch stops paying for its migration, %s months "
      "(band %s to %s). Its vault table gives, for each vault where the batch is a tenth or more of the drives, the drives in "
      "service, the batch's share, the expected replacements of all its drives over the 24 months from 1 October 2026 "
      "against the break-even of %s, and the call: %s." % (
          w0, w1, n(S["hot_batch"]["drives"]), rng(B["hot_batch"]["drives"]), pct(S["hot_batch"]["rate"]),
          pct(B["hot_batch"]["rate"][0]), pct(B["hot_batch"]["rate"][1]), n(S["hot_count"]), rng(B["hot_count"]),
          pct(S["frac24"]), pct(be, 0), n(P.COSTS["migrate_vault"]), P.COSTS["failure_handling"],
          dec(S["rec"]["flip"]), dec(B["rec_flip"][0]), dec(B["rec_flip"][1]),
          n(P.COSTS["migrate_vault"] / P.COSTS["failure_handling"]), vt))
    sp = ", ".join("%s %s" % (f, n(S["spares"][f])) for f in FAM_ORDER if f in S["spares"])
    a("3. \"Q4 spares\" gives, for each family, the fourth quarter's mean and 90th-percentile replacements, the stock on hand "
      "on 30 September 2026 and the order (the 90th percentile less stock, never below zero): %s; each family's order is "
      "graded within 10 per cent of the range the defensible methods give." % sp)
    a("4. \"Back-test\" shows intervals built the same way from the record to 30 September 2025, for every drive family and "
      "quarter from 2025-Q4 to 2026-Q3 in the vaults that stayed in service, against what happened: %s of %d cells inside, "
      "a coverage of %s (band %s to %s)." % (
          n(round(S["coverage"] * g["backtest_cells"])), g["backtest_cells"], pct(S["coverage"]), pct(B["coverage"][0]),
          pct(B["coverage"][1])))
    a("5. \"Drivers\" lists what moves the forecast: DC-3's %s replacements on ages rebuilt from the Brightstore manifest "
      "(%s drives), power-on hours (%s) and the serial's build week plus the deploy lag (%s); the surviving OM-6 vaults' %s; "
      "the bad builds' %s; the infant term, the health pulls of healthy drives under P2 and the counts' extra spread." % (
          n(S["dc3"]), n(src.get("manifest", 0)), n(src.get("power-on hours", 0)), n(src.get("build week", 0)), n(S["om6"]),
          n(S["hot_count"])))
    a("6. The chart (%s) draws the actual replacements per quarter from 2024-Q4 to 2026-Q3 and the forecast mean for each "
      "quarter to 2027-Q3 with its 80 per cent interval shaded, each forecast quarter labelled with its mean." % GD.CHART)
    a("")

    # ---- 3. Critical Components
    a("## Critical Components")
    a("")
    a("1. DC-3's replacements over the four quarters are %s (band %s): its install dates are the 2024-03-01 migration day, "
      "so ages are rebuilt (median deploy lag %s days from the HX-8 serials) and the hazard is fitted with each drive entering "
      "at its age on that day; the close-out's DC-3 rate carried forward gives %s." % (
          n(S["dc3"]), rng(B["dc3"]), n(F["record"]["deploy_lag"]), n(q["dc3"])))
    a("2. The batch with the rising hazard is the HX-8 drives built in %s to %s, %s of them in service at a current annualized "
      "rate of %s; the HX8.2.0 firmware also ran on builds of 2024 weeks 10 to 15, which fail at the family's normal rate, so "
      "the firmware story counts %s drives at %s." % (
          w0, w1, n(S["hot_batch"]["drives"]), pct(S["hot_batch"]["rate"]), n(fw["hot_batch"]["drives"]),
          pct(fw["hot_batch"]["rate"])))
    a("3. The OM-6 vaults still in service will replace %s drives (band %s): the reviews retired the vaults failing fastest, "
      "so one age curve over every OM-6 vault's history prices the survivors at %s." % (
          n(S["om6"]), rng(B["om6"]), n(pooled["om6"])))
    a("4. The fleet's quarterly path is %s, %s, %s and %s (four quarters %s, 80 per cent interval %s); Poisson counts at the "
      "same means give an interval only %s wide, and the same intervals built a year earlier covered %s of the back-test "
      "cells against %s for the golden's." % (
          *(n(S["path"][qq]) for qq in P.FORECAST_Q), n(S["total"]), rng(S["total_band"]), n(pois["total_width"]),
          pct(pois["coverage"], 0), pct(S["coverage"], 0)))
    a("")

    # ---- 4. Step-by-Step
    a("## Step-by-Step")
    a("")
    steps = [
        "Assemble the replacements: a data drive's removal for FAIL or PULL, with blank reasons read from the technicians' "
        "tickets, reseats (the serial back within 30 days) merged into one service life, DECOM removals, boot SSDs and the "
        "QA-01 vault left out, duplicate telemetry rows dropped. Counting every removal in the age curve, the P2 harvest of "
        "healthy SMART 187 drives in June to August 2025 included, gives %s." % n(allrem["total"]),
        "Rebuild DC-3's ages: every migrated drive's install date is 2024-03-01. Take Brightstore's manifest deploy date where "
        "it has one, the VB-12 drives' power-on hours at their first quarter, and otherwise the serial's build week plus the "
        "median deploy lag of Halden's own HX-8 drives (%s days); each drive then enters the hazard fit at its rebuilt age on "
        "2024-03-01, so the failures Brightstore never passed on are not counted as survival." % n(F["record"]["deploy_lag"]),
        "Fit each family's hazard by age on drive-days (monthly bands in the first year, half-yearly after), with one infant "
        "term for the fleet (its decay chosen by "
        "likelihood, %s months) and each family's age slope shrunk to the fleet's; health pulls of healthy drives under P2 are "
        "a separate rate (%s per drive-year since September 2025), not wear-out." % (dec(g["infant_months"], 0),
                                                                                     dec(g["spur_rate"], 4)),
        "Fit each vault's own level as a gamma frailty on its observed against expected replacements. The OM-6 reviews "
        "retired the vault with the most failures each time, and KS-10's review did the same, so the survivors sit below "
        "their family's curve: %s OM-6 replacements, not the %s one pooled curve gives." % (n(S["om6"]), n(pooled["om6"])),
        "Find the batch: scan the HX-8 drives' replacements over the last year by build week against each vault's own earlier "
        "level. The run of %s to %s stands out (likelihood ratio %s against the rest); the HX8.2.0 builds of weeks 10 to "
        "15 do not, so the cause is the build window, not the firmware. Fit the ramp in months since build as an exponential, "
        "a linear and a power shape and weight them by likelihood (%s, %s and %s)." % (
            w0, w1, dec(F["record"]["hot_scan"]["llr"], 0), dec(g["hot_weights"].get("exp", 0), 2),
            dec(g["hot_weights"].get("lin", 0), 2), dec(g["hot_weights"].get("pow", 0), 2)),
        "Forecast by posterior predictive simulation: draw each family's curve, each vault's frailty and the ramp's shape, "
        "onset and slope, run the drives in service forward quarter by quarter (each replacement used up and its spare "
        "starting young), add the scheduled X-24 vaults, and draw Poisson counts (with each vault's level drawn, the "
        "vault-quarter residuals show no spread beyond it). The path is %s, %s, %s and %s, %s in all with an 80 per cent "
        "interval of %s." % (
            *(n(S["path"][qq]) for qq in P.FORECAST_Q), n(S["total"]), rng(S["total_band"])),
        "Back-test the method: build the same intervals from the record to 30 September 2025 and score every family-quarter "
        "of the following year in the vaults that stayed in service: %s coverage. The batch was not yet visible at that cut, "
        "so the HX-8 cells are the misses; Poisson intervals cover %s and the careful-but-hurried method %s." % (
            pct(S["coverage"]), pct(pois["coverage"]), pct(car["coverage"])),
        "Decide: the fourth quarter's spare order per family is its 90th percentile less stock (%s in all). A vault pays for "
        "its migration when its own replacements over the 24 months from 1 October 2026 exceed %s (USD %s over USD %s each); "
        "the batch would lose %s of its drives in that time, but the vaults hold it unevenly, so the call is made vault by "
        "vault: %s. A vault made wholly of the batch stops paying only if the batch's rate doubles more slowly than every %s "
        "months." % (
            n(sum(S["spares"].values())), n(P.COSTS["migrate_vault"] / P.COSTS["failure_handling"]),
            n(P.COSTS["migrate_vault"]), P.COSTS["failure_handling"], pct(S["frac24"]),
            "; ".join("%s %s (%s)" % (v, n(s["mean"]), "migrate" if v in S["rec"]["migrate"] else "run to failure")
                      for v, s in sorted(S["vaults"].items())), dec(S["rec"]["flip"])),
        "Why nothing else survives: the close-out's rates carried give %s and no migration, with DC-3 at %s; the batch "
        "inside its family gives %s of its replacements and migrates %s; the firmware story counts "
        "%s drives at %s, migrates all five vaults and moves the flip point to %s months; deciding every vault on the batch's "
        "average migrates %s too; one curve over every vault prices the OM-6 survivors at %s; and Poisson bands are %s wide "
        "and covered %s of the back-test cells. Each misses a different figure, and every defensible variant of the golden "
        "(the infant term over two or four months, unshrunk slopes, either ramp shape alone, the build window a week "
        "narrower, DC-3's lag from the mean) migrates the same vaults; a week wider is ruled out by the week-15 builds, "
        "which fail at the family's normal rate, and would wrongly put %s over the line." % (
            n(q["total"]), n(q["dc3"]), n(fam["hot_count"]), vs(sorted(fam["rec"]["migrate"])), n(fw["hot_batch"]["drives"]),
            pct(fw["hot_batch"]["rate"]),
            dec(fw["rec"]["flip"]), vs(keep), n(pooled["om6"]), n(pois["total_width"]), pct(pois["coverage"], 0), vs(keep)),
    ]
    for i, s in enumerate(steps, 1):
        a("%d. %s" % (i, s))
    a("")
    return "\n".join(L)
