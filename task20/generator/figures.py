"""figures.json (every figure the answer blocks state) and effort.json (the effort test on the generator's own
passes) from analysis.full()."""
import json
import math
import os


def r1(x, n=1):
    return round(float(x), n)


def dstr(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def write(R, root):
    g = R["golden"]
    sc = dict(R["shortcuts"])
    quick = R["shortcuts"][0][1]
    careful = R["shortcuts"][1][1]
    Pm = R["params"]
    rat = R["ratios"]
    F = {
        "peak_m": r1(g["peak"]), "peak_date": dstr(g["day"]), "facility_m": int(R["facility"]),
        "facility_2026_m": int(R["facility_2026"]), "increase_m": int(R["facility"] - R["facility_2026"]),
        "rounding_m": int(R["rounding"]),
        "book_open_2027_twh": round(R["book_open"][2027], 3), "book_open_2028_twh": round(R["book_open"][2028], 3),
        "book_peak_2027_twh": round(g["book"][2027], 3), "book_peak_2028_twh": round(g["book"][2028], 3),
        "book_peak_2029_twh": round(g["book"][2029], 3), "book_peak_2030_twh": round(g["book"][2030], 3),
        "im_peak_m": r1(g["im"]), "vm_m": r1(g["vm"]), "dlv_m": r1(g["dlv"]), "dim_m": r1(g["dim"]),
        "da_net_m": r1(g["da_net"]), "rec_m": r1(g["rec"]), "out_gwh": int(round(g["out"])), "out_gwh_txt": "{:,}".format(int(round(g["out"]))),
        "ratio_2027_pct": r1(100 * rat[2027]["policy"]), "ratio_2028_pct": r1(100 * rat[2028]["policy"]),
        "ratio_2029_pct": r1(100 * rat[2029]["policy"]), "ratio_ex_2027_pct": r1(100 * rat[2027]["exchange"]),
        "ratio_ex_2028_pct": r1(100 * rat[2028]["exchange"]), "ratio_ex_2029_pct": r1(100 * rat[2029]["exchange"]) + 0.0,
        "c22_actual_m": r1(R["check2022"]["actual"]), "c22_actual_date": dstr(R["check2022"]["actual_day"]),
        "c22_method_m": r1(R["check2022"]["method"]), "c22_method_date": dstr(R["check2022"]["method_day"]),
        "rule_look": Pm["rule"]["look"], "rule_q_pct": int(round(100 * Pm["rule"]["q"])),
        "rule_band_pct": int(round(100 * Pm["rule"]["band"])),
        "desk_theta": r1(Pm["desk"]["theta"], 2), "desk_speed_pts": r1(100 * Pm["desk"]["speed"]),
        "aff_window": Pm["aff"]["window"], "aff_lag": Pm["aff"]["lag"],
        "lag_smelter": int(Pm["lags"]["SMELTER"]), "lag_pulp": int(Pm["lags"]["PULP"]),
        "lag_affiliate": int(Pm["lags"]["AFFILIATE"]), "lag_grid": int(Pm["lags"]["GRID"]),
        "storage_open_gwh": int(round(R["storage_open"])), "floor_gwh": int(Pm["plants"]["floor"]),
        "careful_peak_m": r1(careful["peak"]), "quick_peak_m": r1(quick["peak"]),
        "min_peak_m": r1(sc["the desk held to the policy minimum, nothing else"]["peak"]),
        "nosmelter_peak_m": r1(sc["the smelter's contract left out of the hedge ratio, nothing else"]["peak"]),
        "pct2022_peak_m": r1(sc["2022's rates as a share of price, nothing else"]["peak"]),
        "pct2022_im_m": r1(sc["2022's rates as a share of price, nothing else"]["im"]),
        "const_peak_m": r1(sc["rates held at the year end, nothing else"]["peak"]),
        "ratio22_peak_m": r1(sc["output carried from 2022's own shortfall, nothing else"]["peak"]),
        "inflow_peak_m": r1(sc["output scaled with the week's inflow, nothing else"]["peak"]),
        "budget_peak_m": r1(sc["output at budget, nothing else"]["peak"]),
        "affspot_peak_m": r1(sc["the affiliate at spot, nothing else"]["peak"]),
        "ewma_peak_m": r1(R["ewma"]["peak"]), "ewma_im_m": r1(R["ewma"]["im"]),
        "ror_share_pct": int(round(100 * Pm["plants"]["ror_share"])), "ror_cap": int(Pm["plants"]["ror_cap"]),
        "below_n": int(R["below"][0]), "months_n": int(R["below"][1]),
        "rule_match_n": int(Pm["rule"]["match"]), "rule_notices_n": int(Pm["rule"]["notices"]),
    }
    single = [abs(x["peak"] / g["peak"] - 1) for n, x in R["shortcuts"][2:] if "paid on delivery" not in n and "maximum at once" not in n]
    F["single_lo_pct"], F["single_hi_pct"] = int(math.floor(100 * min(single))), int(math.ceil(100 * max(single)))
    fam_peaks = [x["peak"] for n, x in R["family"]]
    F["band_peak_lo"], F["band_peak_hi"] = 320, 345
    F.update({"band_im_lo": 57.0, "band_im_hi": 63.0, "band_out_lo": "1,700", "band_out_hi": "1,790",
              "band_da_lo": 78.0, "band_da_hi": 86.0, "band_rec_lo": 155.0, "band_rec_hi": 182.0, "book_tol": 0.03,
              "ratio_tol": 0.5, "c22_rec_tol": 3, "c22_method_tol": 15, "careful_facility_m": 300,
              "nosmelter_facility_m": 450, "smelter_mw": 100, "smelter_px": "38.00"})
    assert F["band_peak_lo"] <= min(fam_peaks) and max(fam_peaks) <= F["band_peak_hi"], fam_peaks
    F["r1_book_open"] = {"2027": F["book_open_2027_twh"], "2028": F["book_open_2028_twh"]}
    F["r2_ratios"] = {"2027": F["ratio_2027_pct"], "2028": F["ratio_2028_pct"], "2029": F["ratio_2029_pct"]}
    F["r3_book_peak"] = {"2028": F["book_peak_2028_twh"], "2029": F["book_peak_2029_twh"], "2030": F["book_peak_2030_twh"]}
    F["r5_out_da"] = {"output_gwh": F["out_gwh"], "dayahead_m": F["da_net_m"]}
    F["r7_peak_facility"] = {"peak_m": F["peak_m"], "facility_m": F["facility_m"]}
    F["r8_check"] = {"records_m": F["c22_actual_m"], "method_m": F["c22_method_m"]}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1)

    def book3(x):
        return {"2028": round(x["book"][2028], 3), "2029": round(x["book"][2029], 3), "2030": round(x["book"][2030], 3)}
    fam = R["family"]

    def span(key, sub=None, pad=0.0):
        vals = [(x[key][sub] if sub else x[key]) for n, x in fam]
        return [round(min(vals) - pad, 3), round(max(vals) + pad, 3)]
    res = [
        dict(id="R1", name="the open exchange book at 31 December 2026 (TWh by delivery year)", graded_as="Ask 2",
             figure="r1_book_open", depends=[], independent="the month-end position statement",
             golden={"2027": F["book_open_2027_twh"], "2028": F["book_open_2028_twh"]},
             bands={"2027": [F["book_open_2027_twh"] - 0.01, F["book_open_2027_twh"] + 0.01],
                    "2028": [F["book_open_2028_twh"] - 0.01, F["book_open_2028_twh"] + 0.01]},
             passes={"quick": {"2027": F["book_open_2027_twh"], "2028": F["book_open_2028_twh"]},
                     "careful": {"2027": F["book_open_2027_twh"], "2028": F["book_open_2028_twh"]},
                     "thorough": {"2027": F["book_open_2027_twh"], "2028": F["book_open_2028_twh"]}}),
        dict(id="R2", name="hedge ratios at 31 December 2026 as the policy counts them (per cent)", graded_as="Ask 3",
             figure="r2_ratios", depends=["R1"], independent="the contract register and the position statement",
             golden={"2027": F["ratio_2027_pct"], "2028": F["ratio_2028_pct"], "2029": F["ratio_2029_pct"]},
             bands={y: [F["ratio_%s_pct" % y] - 0.5, F["ratio_%s_pct" % y] + 0.5] for y in ("2027", "2028", "2029")},
             passes={"quick": {"2027": F["ratio_ex_2027_pct"], "2028": F["ratio_ex_2028_pct"], "2029": F["ratio_ex_2029_pct"]},
                     "careful": {"value": {"2027": F["ratio_ex_2027_pct"], "2028": F["ratio_ex_2028_pct"], "2029": F["ratio_ex_2029_pct"]},
                                 "grade": "missed", "why": "the exchange book divided by budgeted output; the smelter's fixed-price contract is a supply contract in another file"},
                     "thorough": {"2027": F["ratio_2027_pct"], "2028": F["ratio_2028_pct"], "2029": F["ratio_2029_pct"]}},
             precedent=["L38", "N03"]),
        dict(id="R3", name="the exchange book at the peak (TWh for 2028, 2029 and 2030)", graded_as="Ask 2",
             figure="r3_book_peak", depends=["R1", "R2"], independent="",
             golden=book3(g), bands={"2028": span("book", 2028, 0.03), "2029": span("book", 2029, 0.03),
                                     "2030": span("book", 2030, 0.03)},
             passes={"quick": book3(quick), "careful": {"value": book3(careful), "grade": "missed",
                                                        "why": "the book grown along the policy's minimum ladder on exchange positions"},
                     "thorough": book3(g)}, precedent=["L15", "N03"]),
        dict(id="R4", name="initial margin at the peak (EUR million)", graded_as="Component 1, Ask 2", figure="im_peak_m",
             depends=["R3"], independent="", golden=F["im_peak_m"], band=[57.0, 63.0], partly=[54.0, 66.0],
             passes={"quick": r1(quick["im"]), "careful": {"value": r1(careful["im"]), "grade": "missed",
                                                          "why": "2022's rates as a share of price carried to 2027"},
                     "thorough": F["im_peak_m"]}, precedent=["L26", "L37"]),
        dict(id="R5", name="output and day-ahead purchases net of sales, 1 January to the peak", graded_as="Component 2, Ask 3",
             figure="r5_out_da", depends=[], independent="the hydrology, plant and day-ahead records",
             golden={"output_gwh": F["out_gwh"], "dayahead_m": F["da_net_m"]},
             bands={"output_gwh": [1700, 1790], "dayahead_m": [78.0, 86.0]},
             passes={"quick": {"output_gwh": int(round(quick["out"])), "dayahead_m": r1(quick["da_net"])},
                     "careful": {"value": {"output_gwh": int(round(careful["out"])), "dayahead_m": r1(careful["da_net"])},
                                 "grade": "missed", "why": "2022's own output shortfall carried to 2027"},
                     "thorough": {"output_gwh": F["out_gwh"], "dayahead_m": F["da_net_m"]}}, precedent=["N02", "L37"]),
        dict(id="R6", name="payments received from supply customers, 1 January to the peak (EUR million)",
             graded_as="Ask 3", figure="rec_m", depends=[], independent="the sales ledger and the contract register",
             golden=F["rec_m"], band=[155.0, 182.0], partly=[145.0, 190.0],
             passes={"quick": r1(quick["rec"]), "careful": {"value": r1(careful["rec"]), "grade": "missed",
                                                           "why": "the affiliate taken at spot like the other customers"},
                     "thorough": F["rec_m"]}, precedent=["L26"]),
        dict(id="R7", name="the stress requirement, its date and the facility", graded_as="Recommendation",
             figure="r7_peak_facility", depends=["R3", "R4", "R5", "R6"], independent="",
             golden={"peak_m": F["peak_m"], "facility_m": F["facility_m"]},
             bands={"peak_m": [F["band_peak_lo"], F["band_peak_hi"]], "facility_m": [F["facility_m"], F["facility_m"]]},
             passes={"quick": {"peak_m": r1(quick["peak"]), "facility_m": 50},
                     "careful": {"value": {"peak_m": r1(careful["peak"]), "facility_m": 300}, "grade": "missed",
                                 "why": "the careful route's own parts added up"},
                     "thorough": {"peak_m": F["peak_m"], "facility_m": F["facility_m"]}}, precedent=["L11", "L37"]),
        dict(id="R8", name="the same requirement for 2022 on the end-2021 book against 2022's records", graded_as="Ask 4",
             figure="r8_check", depends=[], independent="the 2022 statements, day-ahead settlements and ledger",
             golden={"records_m": F["c22_actual_m"], "method_m": F["c22_method_m"]},
             bands={"records_m": [F["c22_actual_m"] - 3, F["c22_actual_m"] + 3], "method_m": [F["c22_actual_m"] - 15, F["c22_actual_m"] + 15]},
             passes={"quick": {"value": {"records_m": F["c22_actual_m"], "method_m": None}, "grade": "partly",
                               "why": "the records read, no method run"},
                     "careful": {"records_m": F["c22_actual_m"], "method_m": F["c22_actual_m"]},
                     "thorough": {"records_m": F["c22_actual_m"], "method_m": F["c22_method_m"]}}),
    ]
    hints = [dict(sentence="the desk's hedge ratio counts the smelter's fixed-price supply contract", rescues=["R2"]),
             dict(sentence="the desk steps to the policy maximum, three points a week, once the year contract is a quarter above its budget price", rescues=["R3"]),
             dict(sentence="NEX's rates are the 99th percentile of the front contract's two-day moves over 250 days, reviewed weekly", rescues=["R4"]),
             dict(sentence="the reservoir opens near the licence floor, so the dry spring cuts output below the committed supply", rescues=["R5"]),
             dict(sentence="the affiliate pays the average system price of the twelve months ending two months before delivery", rescues=["R6"])]
    routes = [dict(name="golden", golden=True, answer=[int(R["facility"])])]
    for n, x in R["shortcuts"]:
        routes.append(dict(name=n, answer=[int(R["facility_of"](x["peak"]))]))
    routes.append(dict(name="rates re-estimated as an exponentially weighted volatility, nothing else",
                       answer=[int(R["facility_of"](R["ewma"]["peak"]))]))
    forcing = dict(kind="set", golden_answer=[int(R["facility"])],
                   golden_family=[dict(name=n, answer=[int(R["facility_of"](x["peak"]))], value=r1(x["peak"]))
                                  for n, x in R["family"] if not n.startswith(("payment habits", "release response", "the affiliate's window", "the desk's threshold", "the desk at"))],
                   perturbations=[dict(input=n, answer=[int(R["facility_of"](x["peak"]))], value=r1(x["peak"]))
                                  for n, x in R["family"] if n.startswith(("payment habits", "release response", "the affiliate's window", "the desk's threshold", "the desk at"))],
                   shortcuts=[dict(name=n, value=r1(x["peak"])) for n, x in R["shortcuts"]],
                   notes="The call is the facility, the requirement rounded up to the next EUR 50 million. Every "
                         "golden-family method and every fitted input moved by its spread files EUR 350 million; the "
                         "shortcuts file between EUR 50 million and EUR 450 million.")
    E = dict(results=res, hints=hints, routes=routes, forcing=forcing)
    json.dump(E, open(os.path.join(root, "effort.json"), "w"), indent=1, default=str)
    return F, E
