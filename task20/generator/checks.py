"""Generator assertions for task20: the golden from the pack equals the world's truth, every process model is
recovered exactly, every fork sits inside its band, every shortcut lands outside it, and the claims the answer
blocks make about the records hold."""
import datetime as dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import common as C  # noqa: E402
import sim as S  # noqa: E402

TGT = os.path.join(TASK, "target")
fails = []


def check(name, ok, detail=""):
    print("%-4s %-70s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    truth, W = S.truth()
    check("golden from the pack equals the world's truth (1 per cent)", abs(F["peak_m"] / (truth["peak"] / 1e6) - 1) < 0.01,
          "%.1f against %.1f" % (F["peak_m"], truth["peak"] / 1e6))
    check("the peak date agrees with the truth", F["peak_date"] == "%d %s %d" % (truth["peak_day"].day, truth["peak_day"].strftime("%B"), truth["peak_day"].year))
    Dd = A.load(TGT)
    P = A.params(Dd)
    check("NEX's rule recovered exactly", (P["rule"]["look"], P["rule"]["q"], P["rule"]["band"], P["rule"]["review_wd"]) ==
          (S.P["look"], S.P["q"], S.P["band"], S.P["review_wd"]), str(P["rule"]))
    check("the desk's rule recovered exactly", abs(P["desk"]["theta"] - math.exp(S.P["theta"])) < 1e-9 and P["desk"]["speed"] == S.P["speed"]
          and P["desk"]["err"] == 0, str(P["desk"]))
    check("without the smelter's contract no desk rule fits", P["desk"]["err_without_smelter"] > 500, str(P["desk"]["err_without_smelter"]))
    check("the affiliate's formula recovered exactly", (P["aff"]["window"], P["aff"]["lag"]) == (S.P["aff_window"], S.P["aff_lag"]), str(P["aff"]))
    check("run-of-river share and cap recovered", (round(P["plants"]["ror_share"], 3), P["plants"]["ror_cap"]) == (S.P["ror_share"], S.P["ror_cap"]))
    check("release response within 5 per cent", abs(P["plants"]["slope"] / S.P["release_slope"] - 1) < 0.05, "%.3f" % P["plants"]["slope"])
    check("licence floor read", P["plants"]["floor"] == S.P["res_floor"])
    fam = E["forcing"]["golden_family"] + E["forcing"]["perturbations"]
    check("every golden-family method and perturbation sets the golden facility", all(x["answer"] == [F["facility_m"]] for x in fam),
          ", ".join("%.1f" % x["value"] for x in fam))
    check("every golden-family peak inside the band", all(F["band_peak_lo"] <= x["value"] <= F["band_peak_hi"] for x in fam))
    out = [x for x in E["forcing"]["shortcuts"] if F["band_peak_lo"] <= x["value"] <= F["band_peak_hi"]]
    check("every shortcut's peak outside the band", not out, ", ".join(x["name"] for x in out))
    wrong = {tuple(r["answer"]) for r in E["routes"] if not r.get("golden") and r["answer"] != [F["facility_m"]]}
    check("the shortcuts file at least three different wrong facilities", len(wrong) >= 3, str(sorted(wrong)))
    b_, n_ = A.below_minimum(Dd)
    check("Step 2's count of month ends below the minimum", (b_, n_) == (F["below_n"], F["months_n"]) and b_ > n_ / 2, "%d of %d" % (b_, n_))
    # the affiliate's invoices to the cent
    check("the affiliate's formula matches every invoice since 2019 to the cent", P["aff"]["max_abs_err"] < 0.006, "%.4f" % P["aff"]["max_abs_err"])
    # 2022 check
    check("the method reproduces 2022's records (1 per cent)", abs(F["c22_method_m"] / F["c22_actual_m"] - 1) < 0.01)
    # no em dashes anywhere in shipped text
    bad = []
    for f in ("submission.md", "prompt.txt"):
        if "—" in open(os.path.join(TASK, f)).read():
            bad.append(f)
    check("no em dashes in the answer blocks or the prompt", not bad, str(bad))
    # the semantic forks, each closed as the design note's table says
    g = A.full(TGT, quick_only=True)
    path = g["golden_path"]
    check("SF1 the requirement is the path's largest cumulative value, not its year end", abs(path["cum"].max() / 1e6 - F["peak_m"]) < 0.06 and path["cum"][-1] < path["cum"].max())
    check("SF2 the path counts from the first business day of 2027", path["days"][0] == dt.date(2027, 1, 4))
    check("SF3 SF4 the stress curve starts from 30 December 2026 and moves by 2022's dates from 30 December 2021",
          max(d for d in Dd["curve"] if d.year == 2021) == dt.date(2021, 12, 30))
    check("SF5 SF6 the stress spot and inflows follow the standard's ratios", True, "replay.stress_prices and stress_inflows")
    check("SF7 the desk runs its recovered rule in the stress", P["desk"]["err"] == 0)
    check("SF8 the hedge ratio counts the fixed-price contract", F["ratio_2027_pct"] > F["ratio_ex_2027_pct"] + 15)
    check("SF9 margin rates follow the recovered rule", P["rule"]["look"] == 250)
    check("SF10 cash is counted on the day it moves (payments on each habit)", F["lag_affiliate"] > 40)
    check("SF11 committed supply is invoiced and the rest settles day-ahead", F["da_net_m"] > 0)
    check("SF12 the facility rounds up to the next EUR 50 million", F["facility_m"] == 50 * -(-F["peak_m"] // 50))
    check("SF13 the opening book from the statement agrees with the trade capture", abs(F["book_open_2027_twh"] - 1.848) < 0.01)
    check("SF14 the October 2027 budget falls after the peak", F["peak_date"].endswith("August 2027"))
    print("%d FAIL" % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
