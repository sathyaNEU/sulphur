"""Halvergate Mutual's exports, written the way each producing system writes them.

The four comparison sites' market-position extracts (Halvergate's quote engine logs every quote it returned with the
panel position the site reports; the MI team's extract keeps every quote that sold and one in fifty of the rest, each
row carrying its weight), the policy system's new-business extract, the claims system's extract as at 31 October 2026
and the renewal pricing team's 2027 schedule for over-65 customers. Each site's own layout is kept: Kitecompare in
ISO local time and pounds, Covertide as JSON lines in epoch milliseconds (its scheduler re-sent 14 May 2026),
Brightquote semicolon-separated with day-first dates and prices in pence, Pricelark in UTC with the reference scheme
it moved to on 1 July 2025. Every site's monitoring script prices a fixed test risk at postcode ZZ99 a few times a
day, and those quotes are in the extracts like any other quote that did not sell.
"""
import csv
import datetime as dt
import io
import json
import os
import zoneinfo

import numpy as np

import params as P
import world

LONDON = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc

FILES = {
    "kc": "kitecompare_market_position_2025-01-01_2026-10-31.csv",
    "ct": "covertide_mi_quotes_2025_2026.jsonl",
    "bq": "brightquote_quote_report_20250101_20261031.csv",
    "pl": "pricelark_insurer_quotes_2025-2026.csv",
    "pol": "pcw_nb_policies_sold_2025-01_2026-10.csv",
    "clm": "motor_claims_extract_2026-10-31.csv",
    "ren": "renewal_schedule_2027_aged_65_plus.csv",
    "log": "hpm_model_deployments.txt",
    "idx": "motor_premium_index_2019Q1_2026Q3.csv",
}
CLAIM_NAME = {"AD": "Accidental damage", "TPPD": "Third party property", "TPBI": "Third party injury",
              "THEFT": "Theft", "WS": "Windscreen"}
COVER_NAME = {"COMP": "Comprehensive", "TPFT": "Third party fire and theft"}


def district(rng, region):
    return "%s%d" % (world.REGIONS[region], int(rng.integers(1, 40)))


def _local(d, h, m, s):
    return dt.datetime(d.year, d.month, d.day, int(h), int(m), int(s), tzinfo=LONDON)


def _rows_for_export(W):
    Q = W["Q"]
    dates = Q["date"]
    keep = np.array([x >= P.QUOTE_EXPORT_FROM for x in dates])
    idx = np.where(keep)[0]
    rng = np.random.default_rng(P.SEED + 101)
    dist = np.array([district(rng, r) for r in Q["region"]])
    return Q, idx, dist


def _test_quotes(site, rng):
    """The site's monitoring quotes: one fixed risk, priced a few times a day; one in fifty is kept by the MI extract
    like any other quote that did not sell."""
    out = []
    d = P.QUOTE_EXPORT_FROM
    k = 0
    while d <= P.AS_AT:
        for h in (3, 9, 15, 21):
            if rng.random() < 1 / 50.0:
                k += 1
                when = _local(d, h, int(rng.integers(0, 4)), int(rng.integers(0, 60)))
                lvl = world.sev_index(d) * (1.0 if d >= dt.date(2026, 2, 1) else 0.97)
                price = round(612.40 * lvl * (1 + world.IPT) * float(np.exp(rng.normal(0, 0.01))), 2)
                rivals = sorted(round(price * float(np.exp(rng.normal(0.02, 0.09))), 2) for _ in range(3))
                rank = 1 + sum(r < price for r in rivals)
                out.append(dict(when=when, age=35, lic=17, ncd=5, vg=20, pc="ZZ99", mil=9000, cover="COMP",
                                gross=price, rank=rank, panel=11, r1=rivals[0], r2=rivals[1], r3=rivals[2], w=50,
                                ref=None, k=k))
        d += dt.timedelta(days=1)
    return out


def write_feeds(W, folder):
    Q, idx, dist = _rows_for_export(W)
    rng = np.random.default_rng(P.SEED + 103)
    per_site = {s: [] for s in P.SITES}
    for i in idx:
        when = _local(Q["date"][i], Q["hour"][i], Q["minute"][i], Q["second"][i])
        per_site[Q["site"][i]].append(dict(
            when=when, age=int(Q["age"][i]), lic=int(Q["licence_years"][i]), ncd=int(Q["ncd"][i]),
            vg=int(Q["vehicle_group"][i]), pc=dist[i], mil=int(Q["mileage"][i]), cover=Q["cover"][i],
            gross=round(float(Q["gross"][i]), 2), rank=int(Q["rank"][i]), panel=int(P.RIVALS[Q["seg"][i]] + 1),
            r1=round(float(Q["comp1"][i]), 2), r2=round(float(Q["comp2"][i]), 2), r3=round(float(Q["comp3"][i]), 2),
            w=1 if Q["kind"][i] == "sold" else 50, ref=Q["quote_ref"][i], k=None))
    for s in P.SITES:
        tests = _test_quotes(s, rng)
        for t in tests:
            t["ref"] = world._ref(s, t["when"].date(), 9000000 + t["k"])
        per_site[s] = sorted(per_site[s] + tests, key=lambda r: (r["when"], r["ref"]))
    _kitecompare(per_site["Kitecompare"], os.path.join(folder, FILES["kc"]))
    _covertide(per_site["Covertide"], os.path.join(folder, FILES["ct"]))
    _brightquote(per_site["Brightquote"], os.path.join(folder, FILES["bq"]))
    _pricelark(per_site["Pricelark"], os.path.join(folder, FILES["pl"]))
    return {s: len(v) for s, v in per_site.items()}


def _kitecompare(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quote_ref", "quote_time_local", "main_driver_age", "licence_years", "ncd_years", "vehicle_group",
                    "postcode_district", "annual_mileage", "cover", "halvergate_premium_gbp", "halvergate_position",
                    "panel_size", "rival_1_gbp", "rival_2_gbp", "rival_3_gbp", "extract_weight"])
        for r in rows:
            w.writerow([r["ref"], r["when"].strftime("%Y-%m-%dT%H:%M:%S"), r["age"], r["lic"], r["ncd"], r["vg"],
                        r["pc"], r["mil"], COVER_NAME[r["cover"]], "%.2f" % r["gross"], r["rank"], r["panel"],
                        "%.2f" % r["r1"], "%.2f" % r["r2"], "%.2f" % r["r3"], r["w"]])


def _covertide(rows, path):
    resent = [r for r in rows if r["when"].date() == dt.date(2026, 5, 14)]
    with open(path, "w") as f:
        for r in rows:
            f.write(_ct_line(r))
        # the scheduler's retry after a failed transfer: the day's file again, appended on 16 May
        for r in resent:
            f.write(_ct_line(r))


def _ct_line(r):
    ts = int(r["when"].astimezone(UTC).timestamp() * 1000)
    o = {"ref": r["ref"], "ts": ts, "risk": {"age": r["age"], "licYears": r["lic"], "ncd": r["ncd"], "vehGroup": r["vg"],
                                            "postcode": r["pc"], "mileage": r["mil"], "cover": r["cover"]},
         "quotedPremium": r["gross"], "rank": r["rank"], "panel": r["panel"], "top3": [r["r1"], r["r2"], r["r3"]],
         "weight": r["w"]}
    return json.dumps(o, separators=(",", ":")) + "\n"


def _brightquote(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["QuoteID", "QuoteDate", "DriverAge", "LicenceYrs", "NCD", "VehGroup", "PostcodeDistrict",
                    "Mileage", "CoverType", "PremiumPence", "Rank", "PanelSize", "Comp1Pence", "Comp2Pence",
                    "Comp3Pence", "Weight"])
        for r in rows:
            w.writerow([r["ref"], r["when"].strftime("%d/%m/%Y %H:%M"), r["age"], r["lic"], r["ncd"], r["vg"], r["pc"],
                        r["mil"], r["cover"], int(round(r["gross"] * 100)), r["rank"], r["panel"],
                        int(round(r["r1"] * 100)), int(round(r["r2"] * 100)), int(round(r["r3"] * 100)), r["w"]])


def _pricelark(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reference", "created_utc", "age", "years_licensed", "no_claims_years", "group", "district",
                    "miles", "cover_level", "price", "position", "brands_quoting", "cheapest_other", "second_other",
                    "third_other", "sampling_weight"])
        for r in rows:
            w.writerow([r["ref"], r["when"].astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S+00:00"), r["age"], r["lic"],
                        r["ncd"], r["vg"], r["pc"], r["mil"], {"COMP": "COMP", "TPFT": "TPF&T"}[r["cover"]],
                        "%.2f" % r["gross"], r["rank"], r["panel"], "%.2f" % r["r1"], "%.2f" % r["r2"],
                        "%.2f" % r["r3"], r["w"]])


# ---- the policy extract ------------------------------------------------------------------------------------------
def policy_number(j):
    base = 41000000 + j * 7 + (j * 37) % 5
    check = "ABCDEFGHJKLMNPQRSTUVWXYZ"[sum(int(c) * (k + 2) for k, c in enumerate(str(base))) % 24]
    return "HM%d%s" % (base, check)


def export_policy_mask(W):
    Q, pol = W["Q"], W["pol"]
    return np.array([Q["date"][q] >= P.NB_START for q in pol["q"]])


def write_policies(W, folder):
    Q, pol = W["Q"], W["pol"]
    keep = export_policy_mask(W)
    rng = np.random.default_rng(P.SEED + 107)
    _, _, dist = _rows_for_export(W)
    path = os.path.join(folder, FILES["pol"])
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy_number", "quote_reference", "sales_channel", "inception_date", "expiry_date",
                    "main_driver_age", "licence_years", "ncd_years", "vehicle_group", "postcode_district",
                    "annual_mileage", "cover", "payment_method", "member", "written_premium_gbp", "ipt_gbp",
                    "risk_premium_gbp", "predicted_claim_frequency", "rating_model", "cancelled_on",
                    "cancellation_reason"])
        for j in np.where(keep)[0]:
            q = pol["q"][j]
            net = float(Q["net"][q])
            canc = pol["cancel_date"][j]
            if canc is not None and canc > P.AS_AT:         # a cancellation still to come is not on the system yet
                canc = None
            w.writerow([policy_number(j), Q["quote_ref"][q], Q["site"][q], pol["inception"][j].isoformat(),
                        pol["expiry"][j].isoformat(), int(Q["age"][q]), int(Q["licence_years"][q]), int(Q["ncd"][q]),
                        int(Q["vehicle_group"][q]), dist[q], int(Q["mileage"][q]), COVER_NAME[Q["cover"][q]],
                        "Monthly" if Q["monthly"][q] else "Annual", "Y" if Q["member"][q] else "N",
                        "%.2f" % net, "%.2f" % (net * world.IPT), "%.2f" % float(Q["pred"][q]),
                        "%.4f" % float(Q["pfreq"][q]), "HPM " + Q["version"][q],
                        canc.isoformat() if canc is not None else "", pol["cancel_reason"][j] if canc is not None else ""])
    return int(keep.sum())


def write_claims(W, folder, CB):
    pol = W["pol"]
    keep = export_policy_mask(W)
    reported, paid, case, status = CB.value(P.AS_AT)
    path = os.path.join(folder, FILES["clm"])
    order = np.lexsort((np.arange(len(CB.rep)), CB.rep))
    n = 0
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["claim_number", "policy_number", "accident_date", "notified_date", "claim_type", "status",
                    "paid_to_date_gbp", "outstanding_estimate_gbp", "incurred_gbp", "settled_date"])
        for k in order:
            j = CB.pol[k]
            if not reported[k] or j < 0 or not keep[j]:
                continue
            n += 1
            st = status[k]
            # a closed claim's settlement as the system holds it on the as-at date: the reopened-and-reclosed ones
            # carry their second close, the rest their first
            again = CB.reopen[k] and CB.reopen_at[k] <= P.AS_AT.toordinal()
            settled = "" if st != "Closed" else dt.date.fromordinal(
                int(CB.reopen_close[k] if again else CB.settle[k])).isoformat()
            w.writerow(["C%s%06d" % (dt.date.fromordinal(int(CB.rep[k])).strftime("%y%m"), 100000 + k),
                        policy_number(j), dt.date.fromordinal(int(CB.acc[k])).isoformat(),
                        dt.date.fromordinal(int(CB.rep[k])).isoformat(), CLAIM_NAME[CB.type[k]], st,
                        "%.2f" % paid[k], "%.2f" % case[k], "%.2f" % (paid[k] + case[k]), settled])
    return n


def write_renewals(W, folder):
    R = W["R"]
    rng = np.random.default_rng(P.SEED + 109)
    path = os.path.join(folder, FILES["ren"])
    n = len(R["age"])
    order = np.lexsort((np.arange(n), R["renewal_month"]))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["renewal_ref", "first_sold_through", "renewal_month", "main_driver_age", "ncd_years",
                    "vehicle_group", "postcode_district", "annual_mileage", "current_premium_ex_ipt_gbp",
                    "renewal_risk_premium_2027_gbp", "intended_renewal_premium_ex_ipt_gbp", "enbp_ex_ipt_at_current_nb_rates_gbp",
                    "renewal_premium_offered_ex_ipt_gbp"])
        for k in order:
            off = min(R["intended"][k], R["enbp"][k])
            w.writerow(["R27-%06d" % (200000 + k * 3 + int(rng.integers(0, 3))), R["site"][k],
                        "2027-%02d" % R["renewal_month"][k], int(R["age"][k]), min(int(R["ncd"][k]) + 1, 15),
                        int(R["vehicle_group"][k]), district(rng, R["region"][k]), int(R["mileage"][k]),
                        "%.2f" % R["last_premium"][k], "%.2f" % R["pred_ren"][k], "%.2f" % R["intended"][k],
                        "%.2f" % R["enbp"][k], "%.2f" % off])
    return n


RELEASE_NOTES = """HALVERGATE PRICING MODEL (HPM) - DEPLOYMENT LOG
Pricing Analytics, Halvergate Mutual Insurance Society
Kept by: Roy Osborne

HPM v7.1   deployed 2026-07-06
  Claims-cost index updated for Q3 2026 (quarterly update).
  Vehicle group table extended to the 2026 model-year groups issued by Thatcham.

HPM v7.0   deployed 2026-02-01 with the 2026 rate review
  Main drivers aged 25 to 64: frequency model rebuilt as a gradient-boosted model trained on 2021-2025 claims,
  adding vehicle-use and declared-mileage interactions and postcode-district risk scores (replacing area bands).
  Main drivers under 25 and aged 65 and over: v6 frequency relativities carried over; base rates refreshed.
  Severity models refreshed for every age on 2022-2025 settlements.

HPM v6.6   deployed 2026-01-12
  Claims-cost index updated for Q1 2026.
  No change to rating factors.

HPM v6.5   deployed 2025-07-07
  Claims-cost index updated for Q3 2025.

HPM v6.4   deployed 2025-01-13
  Claims-cost index updated for Q1 2025.

HPM v6.3   deployed 2024-07-08
  Claims-cost index updated for Q3 2024; windscreen severity re-based on the new repairer contract.

HPM v6.0   deployed 2023-03-06
  Frequency and severity GLMs refitted on 2019-2022 claims for all ages.
"""


def write_notes(folder):
    with open(os.path.join(folder, FILES["log"]), "w", newline="\r\n") as f:
        f.write(RELEASE_NOTES)


def write_index(folder):
    """An industry series the market reads (a distractor here): the average comparison-site premium quoted for a
    basket of risks, by quarter, as the publisher releases it."""
    rng = np.random.default_rng(P.SEED + 113)
    lvl = 100.0
    growth = [0.004, -0.006, 0.002, -0.004, -0.011, -0.009, 0.006, 0.013, 0.021, 0.034, 0.052, 0.061, 0.071, 0.064,
              0.041, 0.022, 0.009, -0.014, -0.021, -0.017, -0.012, -0.006, 0.004, 0.009, 0.011, 0.012, 0.010, 0.009,
              0.011, 0.012, 0.010]
    rows = []
    q = 0
    for y in range(2019, 2027):
        for qq in range(1, 5):
            if (y, qq) > (2026, 3):
                break
            lvl *= 1 + growth[q] + float(rng.normal(0, 0.003))
            rows.append(("%dQ%d" % (y, qq), round(lvl, 1), round(lvl * 6.112, 0)))
            q += 1
    with open(os.path.join(folder, FILES["idx"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quarter", "index_2019Q1_100", "average_quoted_premium_gbp", "source"])
        for r in rows:
            w.writerow([r[0], "%.1f" % r[1], "%d" % r[2], "Ostrander Data comparison-site basket, release 2026-10-21"])
