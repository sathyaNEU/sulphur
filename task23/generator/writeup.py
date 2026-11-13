"""task23 architecture 1: submission.md, the four answer blocks, every figure read from figures.json."""
import params as P

WB = "fernhallow_methane_2025_2027.xlsx"
DK = "council_briefing_2027_gas_package.pptx"


def _f(x, d=0):
    return ("{:,.%df}" % d).format(x)


def _s(x):
    return ("+" if x >= 0 else "-") + _f(abs(x))


def _pk(v):
    return "; ".join("%s %s" % (k.replace("package ", "package "), _f(t)) for k, t in v.items())


def write(figs, E, path):
    x = figs["_extra"]
    lim = figs["limit_t"]
    e = figs["R7_emissions_2027_t"]
    b = figs["R6_bridge"]
    c4 = x["cell4"]
    car = x["careful"]
    dr = x["drops"]
    sc = x["shortcuts"]
    call = figs["R8_package"]
    cost = x["costs_usd_m"]
    near = x["nearest"]
    L = []
    A = L.append
    A("## Tags")
    A("")
    A("**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (emissions inventory: a "
      "landfill's annual methane balance and its 2027 forecast).")
    A("**Analytical objective:** Comparative Analysis & Explanation.")
    A("")
    A("## Final Recommendation")
    A("")
    A("**Fund %s (USD %s million): it is the cheapest package that keeps 2027 at or under the Council's %s-ton limit, "
      "at %s metric tons of methane in a normal-weather year, while package C (USD %s million) leaves %s.** Reject "
      "package A, which the report's and the survey's levels, cell 4's collected gas and the 2019 study's oxidation "
      "shares together give (2027 at %s tons under the plan of record): the campaigns sampled only the hours when "
      "rising pressure held gas in the waste, the recirculated leachate that sped cell 4's decay also flooded the "
      "wells that see it and now reaches all of cell 5, and cell 5's cover oxidizes a far smaller share of the "
      "flux it will carry in 2027 than of the study's."
      % (call, _f(cost[call], 2), _f(lim), _f(e[call]), _f(cost["package C"], 2), _f(e["package C"]),
         _f(car["R7"]["package A"])))
    A("")
    A("## Supplementary Questions")
    A("")
    A("### %s" % WB)
    A("")
    A("1. The site's actual 2025 methane emission is **%s metric tons** (within 10 per cent), on the 2025 bridge sheet: "
      "the state's %d campaigns of 2025 carried to every hour of the year through the pressure response the "
      "automated chambers on cells 4 and 5 record, with a table of each campaign's measured rate, its pressure "
      "factor (mean %s) and its annual-mean rate."
      % (_f(figs["R2_actual_2025_t"]), x["campaigns_2025"], _f(figs["campaign_factor_2025"], 3)))
    A("2. The bridges on the same sheet, in metric tons: from the 2025 report's %s, collection efficiency **%s** "
      "(within 15 per cent), then oxidation **%s** (within 250 tons), then everything else %s, to %s; from the state "
      "survey's %s, the hours the campaigns did not sample **%s** (within 490 tons), to %s."
      % (_f(figs["report_2025_t"]), _s(b["collection efficiency"]), _s(b["oxidation"]), _s(figs["residual_2025_t"]),
         _f(figs["R2_actual_2025_t"]), _f(figs["survey_2025_t"]), _s(b["the hours the campaigns did not sample"]),
         _f(figs["R2_actual_2025_t"])))
    A("3. Municipal waste placed in cell 5 from its opening through October 2026: **%s short tons** (within 1 per "
      "cent), on the cell 5 sheet." % _f(figs["R1_cell5_msw_tons"]))
    A("4. Cell 4's methane generation rose **%s per cent** (within 8 points) from calendar 2022 to the twelve months "
      "to October 2026, on the cell 4 sheet, with the wells the leachate never reached (+%s per cent), the pumped "
      "wells at full yield (+%s per cent), the flooded wells and the collected gas (+%s per cent) side by side."
      % (_f(figs["R3_cell4_generation_change_pct"], 1), _f(c4["dry_change_pct"], 1),
         _f(c4["pumped_full_yield_change_pct"], 1), _f(c4["collected_change_pct"], 1)))
    A("5. Cell 5 will generate **%s metric tons** of methane in 2027 (within 12 per cent), month by month on the cell 5 "
      "sheet." % _f(figs["R4_cell5_generation_2027_t"]))
    A("6. Under the plan of record cell 5's cover will oxidize **%s per cent** of the methane reaching it in 2027 "
      "(within 4 points), with each month's flux, normal soil temperature and share on the cell 5 sheet."
      % _f(figs["R5_cell5_oxidized_share_2027_pct"], 1))
    A("7. 2027 emissions in a normal-weather year, metric tons (each within 7 per cent), on the package call sheet "
      "with each package's works, cost and margin to the limit: %s. The 2027 by cell sheet splits each package's "
      "total into the closed cells, cell 4, cell 5 and the flare and engines." % _pk(e))
    A("")
    A("### %s" % DK)
    A("")
    A("8. Four slides for the Council: the call (package %s, USD %s million, about %s tons against the %s-ton limit, "
      "package C over it) on the first; a column chart of the five packages' 2027 emissions labelled with their costs, "
      "those over the limit in red and %s in blue; a bar chart of the 2025 bridge from the report and from the survey "
      "to the actual %s tons; and what changed in cells 4 and 5 since 2023."
      % (call.split()[-1], _f(cost[call], 2), _f(e[call]), _f(lim), call, _f(figs["R2_actual_2025_t"])))
    A("")
    A("## Critical Components")
    A("")
    A("1. The site emitted **%s metric tons** of methane in 2025: the state's 2025 campaigns averaged %s kg an hour "
      "on hours whose pressure response ran at %s of the year's mean, so the survey's %s tons and the drone flights' "
      "%s both sit low." % (_f(figs["R2_actual_2025_t"]), _f(x["campaign_mean_2025_kg_h"], 1),
                           _f(figs["campaign_factor_2025"], 3), _f(figs["survey_2025_t"]), _f(x["drone_2025_t"])))
    A("2. Cell 4's methane generation rose **%s per cent** from 2022 to the twelve months to October 2026, though its "
      "collected gas rose only %s per cent: the leachate that sped the decay of the waste it reached also flooded "
      "the wells in that waste." % (_f(figs["R3_cell4_generation_change_pct"], 1), _f(c4["collected_change_pct"], 1)))
    A("3. 2027 emissions in a normal-weather year: package C **%s** tons, over the %s-ton limit; package %s **%s** "
      "tons, under it." % (_f(e["package C"]), _f(lim), call.split()[-1], _f(e[call])))
    A("4. Cell 5's cover will oxidize **%s per cent** of the methane reaching it in 2027, against the %s per cent the "
      "2019 study measured on daily cover at lower fluxes." % (_f(figs["R5_cell5_oxidized_share_2027_pct"], 1),
                                                         _f(x["study_mean_pct"]["active"], 1)))
    A("")
    A("## Step-by-Step")
    A("")
    A("1. Summed the scale tickets for cell 5 (voided tickets dropped and their reissues under the same ticket number "
      "kept, the old material codes mapped to the new ones, a ticket with no disposal area put in the cell the daily "
      "log shows active that day): **%s short "
      "tons** of municipal waste through October 2026, where summing every ticket as filed gives %s."
      % (_f(figs["R1_cell5_msw_tons"]), _f(figs["_quick"]["R1_cell5_msw_tons"])))
    A("2. Reproduced the 2025 report from its own equation: %s tons of methane collected over the area-weighted "
      "collection efficiency %s, the rule's %s per cent oxidation and %s destruction give %s tons."
      % (_f(figs["collected_2025_t"]), _f(x["rule"]["ce_2025"], 4), x["rule"]["ox_pct"], x["rule"]["de"],
         _f(figs["report_2025_t"])))
    A("3. Fitted the soil-cover chambers' hourly flux (cell 4's AC-1 and cell 5's AC-3, QC-OK hours, their UTC "
      "clock put on the station's local standard time) as a log-linear response to the gap between the barometer's "
      "exponential moving average and its reading, the average moving a sixteenth of the way to each hourly reading "
      "(a %d-hour time constant, chosen by least squares among 4 to 48 hours), with chamber-month levels, the soil "
      "temperature's departure from its chamber-month mean and the rain of the preceding six hours: the response is "
      "%s in the log per hPa (cell 3's chamber, pooled in, gives the same within a few per cent). Over each campaign's window (local clock, daylight time in summer) the factor averages "
      "%s in 2025: the state's crews fly on settled days after a front, while pressure is rising and the waste is "
      "holding gas. Carried to every hour, the 2025 campaigns give **%s tons**; the shortcut multiplies the "
      "campaigns' mean by 8,760 hours (%s) and takes the drone flights' %s as confirmation, though the flights sample "
      "the same weather (factor %s)."
      % (x["pressure"]["lag_h"], _f(x["pressure"]["coef_per_hpa"], 3), _f(figs["campaign_factor_2025"], 3),
         _f(figs["R2_actual_2025_t"]), _f(figs["survey_2025_t"]), _f(x["drone_2025_t"]),
         _f(x["drone_factor_2025"], 3)))
    A("4. Split cell 4's wells by the liquid over their screens since 2023: %d of %d never flooded and rose %s per "
      "cent from 2022 to the twelve months to October 2026; the %d wells given pumps in June 2025 rose %s per cent "
      "with %s of each screen still under liquid, %s per cent at full yield (yield loss %s per unit of submerged "
      "screen, from their flows before and after the pumps). Weighting the two zones by their wells (%s per cent in the reached "
      "waste) gives **+%s per cent**; cell 4's collected gas (+%s per cent) mixes the reached waste's rise with the "
      "flooded wells' lost yield and reads as no change in its decay."
      % (c4["dry"], c4["wells"], _f(c4["dry_change_pct"], 1), c4["pumped"], _f(c4["pumped_change_pct"], 1),
         _f(c4["pumped_submergence"], 2), _f(c4["pumped_full_yield_change_pct"], 1), _f(c4["yield_loss"], 2),
         _f(c4["share_reached_pct"], 1), _f(figs["R3_cell4_generation_change_pct"], 1),
         _f(c4["collected_change_pct"], 1)))
    A("5. Took the decay rate of unreached waste from the closed cells' collected gas (%s a year) and fitted the "
      "reached waste's rate so cell 4's reached zone reproduces the pumped wells' full-yield rise (%s a year). Cell 5 "
      "has taken leachate across its whole footprint since July 13, 2026 (the options paper), so its waste moves to "
      "the faster rate from August; its level is set by the spring 2026 two-tracer campaigns on cell 5, all before "
      "the recirculation, on the unreached rate, and puts the municipal waste's methane potential at about %s "
      "cubic meters a short ton (cell 4's campaigns %s, the closed cells' collected gas at their design collection %s). "
      "Cell 5 generates **%s tons** in 2027; carried on the unreached rate from the uncorrected campaigns, as the "
      "shortcut does, it is %s."
      % (_f(x["decay"]["kd"], 4), _f(x["decay"]["kw"], 4), x["implied_l0_m3_per_ton"]["campaigns cell 5"],
         x["implied_l0_m3_per_ton"]["campaigns cell 4"], x["implied_l0_m3_per_ton"]["closed cells"],
         _f(figs["R4_cell5_generation_2027_t"]), _f(car["R4"])))
    A("6. Fitted the 2019 study's %d plots by least squares as a capacity that saturates with the flux: the share "
      "oxidized is V/(V + J), J the flux reaching the cover from below (the plot's surface flux over one less its "
      "share) and V = V15 x Q10^((T - 15)/10) at the plot's soil temperature, V15 for each cover and one Q10 (%s) for "
      "all: daily cover takes about %s g per square meter a day at 15 C. Cell 5's flux is its uncollected methane over "
      "its %s-acre footprint (the Cells sheet): by 2027 its lifts and leachate lines cover the whole footprint (the "
      "options paper; the daily log's fourth lift and the fill plan's fifth), while the 2025 report's %s acres is the "
      "area filled in 2025. At the flux cell 5 will carry in 2027 and normal "
      "soil temperatures it oxidizes **%s per cent**; the study's daily-cover mean (%s per cent) was measured at a small "
      "fraction of that flux."
      % (x["plots"], _f(x["sat_q10"], 2), _f(x["sat_v15_g_m2_d"]["active"], 1), _f(x["cell5_acres"], 1),
         _f(x["cell5_acres_2025_report"], 1), _f(figs["R5_cell5_oxidized_share_2027_pct"], 1),
         _f(x["study_mean_pct"]["active"], 1)))
    A("7. Bridged 2025 in the order of the report's equation: actual generation in place of the rule's collection "
      "efficiency adds **%s tons**, each cover's oxidation at its own monthly flux in place of 10 per cent changes it "
      "by **%s**, and %s tons are left; the survey's gap is the hours its campaigns did not sample, **%s**."
      % (_f(b["collection efficiency"]), _s(b["oxidation"]), _s(figs["residual_2025_t"]),
         _s(b["the hours the campaigns did not sample"])))
    A("8. Forecast 2027 cell by cell in normal weather: closed cells on their own collected gas at the closure plan's "
      "%s per cent design collection, cell 4 by zone (the unflooded wells at %s of the unreached waste's methane, "
      "the wells in the reached waste at %s, each over August to October 2026 and carried with its own zone's "
      "generation) with package C's pumps restoring its flooded wells by the pilot's yield model and package E's cap "
      "at %s per cent, cell 5 at the "
      "options paper's design capture from each works' date, each cover's saturating oxidation and the unburned "
      "share at the flare and engines: %s. The campaigns' rates as measured, one decay rate and the study's shares "
      "give %s and pick package A."
      % (x["ce_closed_pct"], _f(x["ce4_zones"]["dry"], 2), _f(x["ce4_zones"]["wet"], 2), x["ce4_cap_pct"], _pk(e),
         _pk(car["R7"])))
    A("")
    A("No other package survives. %s comes out under a pressure lag fixed at 12 or 20 hours, cell 4's chamber alone "
      "or all three chambers pooled, the campaigns weighted with the drone flights, oxidation as a logistic in the log "
      "of the flux or as a capacity with its own half-saturation flux, cell 5 on cell 4's methane potential, the level "
      "set by the closed cells' collected gas, the faster decay ramped in over three or six months, cell 4's "
      "efficiency held at its autumn 2026 level and package C's gain read as the pilot's mean flow ratio, and under "
      "each fitted input moved by its spread; the nearest, %s, still leaves "
      "package C %s tons over. Each shortcut lands elsewhere: no pressure "
      "correction on %s, one decay rate on %s, the study's oxidation shares on %s, the rule's 10 per cent on %s, any "
      "two of them together on package A, a methane potential taken from a reporting default instead of the "
      "measurements on %s at all, and the closed cells' level with both decay rates but the study's shares on %s."
      % ("Package " + call.split()[-1], near["C_name"], _f(near["C_over_t"]), dr["J2"]["answer"],
         dr["J1"]["answer"], dr["J3"]["answer"],
         sc["the reporting rule's 10 per cent oxidation"]["answer"],
         sc["the rule's default potential, uncalibrated, with both decay rates and a saturating oxidation"]["answer"],
         sc["the closed cells' level with both decay rates and the study's oxidation"]["answer"]))
    open(path, "w").write("\n".join(L) + "\n")
