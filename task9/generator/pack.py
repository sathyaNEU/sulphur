"""task9: the pack's data files, written the way each system would hold them.

Lenderbase reports each loan every quarter (re-submitted quarters, a 2019 change of codes and date formats, legal
entity identifiers only from 2012); Dealtrail records each buyout, sale and listing with the buyers under the names
each fund signed under; the workout file closes recoveries as workouts end; the managers' tapes follow their own
layouts and rating scales. Every item of mess here is recoverable exactly and decides nothing.
"""
import csv
import datetime as dt
import io
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import world as WD

PULL_LB = dt.date(2027, 2, 16)
PULL_DT = dt.date(2027, 2, 15)
CUT2019 = dt.date(2019, 1, 1)
LEI_FROM = dt.date(2012, 7, 1)
_OLD_STATUS = {"P": "P", "W": "W", "D": "D", "R": "R"}
_NEW_STATUS = {"P": "Performing", "W": "Watchlist", "D": "Defaulted", "R": "Repaid"}
_OLD_PURPOSE = {"LBO": "Buyout", "SBO": "Secondary buyout", "Refinancing": "Refi"}
_STRAT = ["Industrier", "Holdings", "Group", "Partners", "Corporation", "Werke", "Industries"]
_STRAT_FORM = ["ASA", "plc", "AG", "SA", "N.V.", "AB", "S.p.A."]
_SELLERS = ["Founder shareholders", "Family owners", "Management and founders", "Founding family",
            "Corporate carve-out", "Private owners"]
COUNTRY_NAME = {"DE": "Germany", "FR": "France", "NL": "Netherlands", "GB": "United Kingdom", "SE": "Sweden",
                "DK": "Denmark", "NO": "Norway", "FI": "Finland", "BE": "Belgium", "ES": "Spain", "IT": "Italy",
                "AT": "Austria", "CH": "Switzerland", "IE": "Ireland"}


def _q_end(d):
    m = ((d.month - 1) // 3 + 1) * 3
    nxt = dt.date(d.year + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def _quarters(a, b):
    q = _q_end(a)
    out = []
    while q <= b:
        out.append(q)
        q = _q_end(q + dt.timedelta(days=1))
    return out


def _period(q):
    return "%dQ%d" % (q.year, (q.month - 1) // 3 + 1) if q < CUT2019 else q.isoformat()


def _fdate(d, q):
    if d is None:
        return ""
    return d.strftime("%d/%m/%Y") if q < CUT2019 else d.isoformat()


def _name_variant(name, rng):
    u = rng.random()
    if u < 0.06:
        return name.upper()
    if u < 0.10:
        return name.replace(".", "")
    if u < 0.13:
        return name + " "
    return name


def _write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


# ---------------------------------------------------------------- Lenderbase
def lenderbase(W, rng, out):
    rows = []
    lb_id = {}
    order = sorted((L for L in W.loans if L["covered"]), key=lambda L: (L["orig"], L["id"]))
    noleibase = set(L["id"] for L in order if rng.random() < 0.09)
    for i, L in enumerate(order):
        start = max(L["orig"], dt.date(WD.DB0, 1, 1))
        end = L["end"] if L["end"] is not None else WD.AS_OF
        if end < dt.date(WD.DB0, 1, 1):
            continue
        lb_id[L["id"]] = "LB-%07d" % (1000003 + 17 * i)
        C = W.comps[L["comp"]]
        qs = _quarters(start, min(_q_end(end), WD.AS_OF))
        if not qs:
            qs = [_q_end(end)]
        commit = L["amount_ccy"]
        watch_from = None
        if L["status"] == "default" and rng.random() < 0.55:
            watch_from = _q_end(L["end"] - dt.timedelta(days=int(rng.integers(100, 280))))
        lender = "L%02d" % int(rng.integers(1, 38))
        for q in qs:
            st = "P"
            if watch_from is not None and q >= watch_from:
                st = "W"
            last = q == qs[-1]
            if last and L["status"] == "default" and _q_end(L["end"]) == q:
                st = "D"
            elif last and L["status"] == "repaid" and _q_end(L["end"]) == q:
                st = "R"
            drawn = round(commit * float(rng.uniform(0.86, 1.0)), 1)
            lei = "" if (L["id"] in noleibase or q < LEI_FROM) else L["obligor_lei"]
            rating = WD.MOODYS[L["rating"]] if q < CUT2019 else WD.RATINGS[L["rating"]]
            purpose = _OLD_PURPOSE[L["purpose"]] if q < CUT2019 else L["purpose"]
            status = _OLD_STATUS[st] if q < CUT2019 else _NEW_STATUS[st]
            ddate = _fdate(L["end"], q) if st == "D" else ""
            dtype = ""
            if st == "D":
                u = rng.random()
                dtype = "Payment default" if u < 0.5 else ("Insolvency" if u < 0.75 else "Distressed restructuring")
            sub = dt.datetime.combine(q + dt.timedelta(days=int(rng.integers(18, 44))), dt.time(int(rng.integers(7, 19)), int(rng.integers(0, 60))))
            row = [lb_id[L["id"]], _period(q), _name_variant(L["obligor"], rng), lei, C["country"], WD.SECTORS[C["ind"]][0],
                   L["facility"], purpose, L["ccy"], "%.1f" % commit, "%.1f" % drawn, L["margin"], rating,
                   _fdate(L["orig"], q), _fdate(L["maturity"], q), status, ddate, dtype, lender,
                   sub.strftime("%Y-%m-%d %H:%M")]
            rows.append(row)
            # a re-submitted quarter: the lender corrects the drawn amount, or files the watch or the default late
            if rng.random() < 0.035 or (st == "D" and rng.random() < 0.18):
                first = list(row)
                if st == "D":
                    first[15] = _OLD_STATUS["W"] if q < CUT2019 else _NEW_STATUS["W"]
                    first[16], first[17] = "", ""
                else:
                    first[10] = "%.1f" % round(drawn * float(rng.uniform(0.9, 1.1)), 1)
                late = sub + dt.timedelta(days=int(rng.integers(9, 60)))
                cap = dt.datetime.combine(PULL_LB - dt.timedelta(days=1), dt.time(16, 30))
                if late > cap:
                    late = cap
                if late > sub:
                    row[19] = late.strftime("%Y-%m-%d %H:%M")
                    rows[-1] = first
                    rows.append(row)
    header = ["lb_loan_id", "report_period", "obligor_name", "obligor_lei", "country", "sector_code", "facility_type",
              "purpose", "currency", "commitment_ccy_m", "drawn_ccy_m", "margin_bps", "rating_at_origination",
              "origination_date", "maturity_date", "status", "default_date", "default_type", "reporting_lender",
              "submission_ts"]
    _write_csv(os.path.join(out, "lenderbase_loan_performance_2008-2026.csv"), header, rows)
    return lb_id, len(rows)


def workouts(W, rng, out, lb_id):
    rows = []
    frac_lenders = set("L%02d" % i for i in rng.choice(np.arange(1, 38), 9, replace=False))
    for L in sorted((L for L in W.loans if L["status"] == "default" and L["id"] in lb_id), key=lambda L: (L["end"], L["id"])):
        if L["end"].year < WD.DB0:
            continue
        ead = round(L["amount_ccy"] * float(rng.uniform(0.92, 1.04)), 1)
        lender = "L%02d" % int(rng.integers(1, 38))
        closed = L["resolved"] <= PULL_LB
        if closed:
            r = L["recovery"]
            rec = "%.3f" % r if lender in frac_lenders else "%.1f" % (100 * r)
            rows.append([lb_id[L["id"]], L["obligor"], L["end"].isoformat(), "Closed", L["resolved"].isoformat(),
                         L["resolution"], rec, "%.1f" % ead, L["ccy"], lender])
        else:
            rows.append([lb_id[L["id"]], L["obligor"], L["end"].isoformat(), "Open", "", "", "", "%.1f" % ead,
                         L["ccy"], lender])
    header = ["lb_loan_id", "obligor_name", "default_date", "workout_status", "resolution_date", "resolution_type",
              "recovery", "exposure_at_default_ccy_m", "currency", "reporting_lender"]
    _write_csv(os.path.join(out, "lenderbase_workout_recoveries_2008-2026.csv"), header, rows)
    return len(rows)


# ---------------------------------------------------------------- Dealtrail
def _fund_variant(W, fid, rng, allow_house_only=True):
    f = W.funds[fid]
    hh = W.houses[f["house"]]
    u = rng.random()
    if allow_house_only and u < 0.07:
        return hh["name"]
    if u < 0.35:
        return f["name"]
    if u < 0.55:
        return "%s %s" % (hh["name"], f["roman"])
    if u < 0.75:
        return "%s Fund %s %s" % (hh["name"], f["roman"], hh["vehicle"])
    if u < 0.88:
        return "%s %s %s" % (hh["stem"], f["roman"], hh["vehicle"])
    return "%s; %s %s Co-Invest %s" % (f["name"], hh["stem"], f["roman"], hh["vehicle"])


def dealtrail(W, rng, out):
    stems = WD._stems(np.random.default_rng(W.seed + 7), 900)
    strat = ["%s %s %s" % (s, rng.choice(_STRAT), rng.choice(_STRAT_FORM)) for s in stems[:260]]
    addon_names = ["%s %s" % (s, rng.choice(["Services", "Technik", "Systems", "Solutions", "Group", "Partners"]))
                   for s in stems[300:900]]
    rows = []
    for D in W.deals:
        if D["kind"] == "default":
            continue
        C = W.comps[D["comp"]]
        comp_d = D["date"]
        ann = comp_d - dt.timedelta(days=int(rng.integers(25, 130)))
        share = 0.55 if comp_d < LEI_FROM else (0.85 if comp_d.year < 2015 else 1.0)
        lei = C["lei"] if rng.random() < share else ""
        ev = float(np.round(np.exp(rng.normal(np.log(120), 0.6)), 0))
        mult = float(np.round(rng.normal(10.5 if comp_d.year > 2014 else 8.5, 1.6), 1))
        if D["kind"] == "primary":
            typ, buyers, sellers = "Primary buyout", _fund_variant(W, D["buyer"], rng), rng.choice(_SELLERS)
        elif D["kind"] == "secondary":
            typ = "Secondary buyout"
            buyers = _fund_variant(W, D["buyer"], rng)
            sellers = _fund_variant(W, D["seller"], rng)
        else:
            typ = D.get("exit_type", "Trade sale")
            buyers = "Public offering" if typ == "IPO" else rng.choice(strat)
            sellers = _fund_variant(W, D["seller"], rng)
        rows.append([ann, comp_d, "Completed", typ, C["trading"], lei, C["country"], WD.SECTORS[C["ind"]][4], buyers,
                     sellers, "%.0f" % ev if rng.random() < 0.7 else "", "%.1f" % mult if rng.random() < 0.6 else ""])
    # withdrawn approaches and add-on acquisitions, as the database carries them
    alive_by_year = {}
    for D in W.deals:
        if D["kind"] in ("primary", "secondary"):
            alive_by_year.setdefault(D["date"].year, []).append(D)
    keys = sorted(alive_by_year)
    for _ in range(140):
        y = keys[int(rng.integers(len(keys)))]
        D = alive_by_year[y][int(rng.integers(len(alive_by_year[y])))]
        C = W.comps[D["comp"]]
        other = int(rng.integers(len(W.funds)))
        d = D["date"] + dt.timedelta(days=int(rng.integers(400, 1500)))
        if d > WD.AS_OF:
            continue
        rows.append([d - dt.timedelta(days=60), d, "Withdrawn", "Secondary buyout", C["trading"],
                     C["lei"] if rng.random() < 0.7 else "", C["country"], WD.SECTORS[C["ind"]][4],
                     _fund_variant(W, other, rng), _fund_variant(W, D["buyer"], rng), "", ""])
    for i in range(620):
        y = keys[int(rng.integers(len(keys)))]
        D = alive_by_year[y][int(rng.integers(len(alive_by_year[y])))]
        C = W.comps[D["comp"]]
        d = D["date"] + dt.timedelta(days=int(rng.integers(120, 1300)))
        if d > WD.AS_OF:
            continue
        rows.append([d - dt.timedelta(days=45), d, "Completed", "Add-on", addon_names[i % len(addon_names)], "",
                     C["country"], WD.SECTORS[C["ind"]][4], C["trading"], rng.choice(_SELLERS),
                     "%.0f" % float(np.round(np.exp(rng.normal(np.log(25), 0.6)), 0)) if rng.random() < 0.5 else "", ""])
    rows.sort(key=lambda r: (r[1], r[4]))
    out_rows = []
    for i, r in enumerate(rows):
        ann, comp_d = r[0], r[1]
        fmt = "%d %b %Y" if rng.random() < 0.25 else "%Y-%m-%d"
        out_rows.append(["DT%06d" % (200011 + 7 * i), ann.strftime(fmt), comp_d.strftime(fmt)] + r[2:])
    header = ["deal_id", "announced", "completed", "deal_status", "deal_type", "target", "target_lei", "target_country",
              "target_sector", "buyers", "sellers", "enterprise_value_eur_m", "ev_ebitda"]
    _write_csv(os.path.join(out, "dealtrail_buyout_transactions_1997-2026.csv"), header, out_rows)
    return len(out_rows)


# ---------------------------------------------------------------- LEI reference
def lei_extract(W, rng, out):
    rows = []
    for C in W.comps:
        status = "ISSUED"
        if C.get("default") is not None and rng.random() < 0.5:
            status = "LAPSED"
        first = max(LEI_FROM, dt.date(C["first"], 1, 1)) + dt.timedelta(days=int(rng.integers(0, 600)))
        rows.append([C["lei"], C["legal"], C["trading"], C["country"], "GENERAL", "ACTIVE", status,
                     min(first, WD.AS_OF).isoformat(), "", ""])
    for hh in W.houses:
        hh["mgr_lei"] = WD.lei(rng)
        rows.append([hh["mgr_lei"], hh["name"].replace(" Partners", "").replace(" Capital", "") + " Management S.a r.l.",
                     hh["name"], "LU", "GENERAL", "ACTIVE", "ISSUED", "2013-02-01", "", ""])
    for f in W.funds:
        hh = W.houses[f["house"]]
        if f["vint"] + 13 < 2013:
            continue
        rows.append([WD.lei(rng), "%s %s" % (f["name"], hh["vehicle"]), "", "LU" if hh["vehicle"] != "LP" else "GB",
                     "FUND", "ACTIVE" if f["vint"] + 12 >= 2026 else "INACTIVE", "ISSUED",
                     max(LEI_FROM, dt.date(f["vint"], 3, 1)).isoformat(), hh["mgr_lei"], "FUND_MANAGER"])
    order = rng.permutation(len(rows))
    rows = [rows[i] for i in order]
    header = ["lei", "legal_name", "other_names", "legal_jurisdiction", "entity_category", "entity_status",
              "registration_status", "initial_registration_date", "related_lei", "relationship_type"]
    _write_csv(os.path.join(out, "lei_reference_extract_2026-12-31.csv"), header, rows)
    return len(rows)


# ---------------------------------------------------------------- the managers' tapes
def _sheet_header(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9)


def _save(wb, path, created):
    wb.properties.creator = "Excel"
    wb.properties.lastModifiedBy = ""
    wb.properties.created = created
    wb.properties.modified = created
    wb.save(path)


def tapes(W, rng, out):
    created = dt.datetime(2027, 1, 5, 9, 12)
    # Kestrel Lane: the agency-format collateral tape
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Portfolio"
    _sheet_header(ws, "Kestrel Lane Credit Partners: KLCP Senior Loan Note 2027 static portfolio",
                  "Collateral data as at 31 December 2026. Par in loan currency, millions.")
    hdr = ["Obligor", "LEI", "Country", "Industry", "Currency", "Par (m)", "Margin (bps)", "Rating at origination (Moody's equivalent)",
           "Facility", "Origination", "Maturity", "Purpose"]
    ws.append([])
    ws.append(hdr)
    for c in sorted(W.X, key=lambda c: W.comps[c]["legal"]):
        C = W.comps[c]
        L = W.loans[C["loan"]]
        ws.append([C["legal"], C["lei"], C["country"], WD.SECTORS[C["ind"]][2], L["ccy"], L["amount_ccy"], L["margin"],
                   WD.MOODYS[L["rating"]], L["facility"], L["orig"], L["maturity"],
                   {"LBO": "LBO", "SBO": "Secondary LBO", "Refinancing": "Refinancing"}[L["purpose"]]])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[9].number_format = row[10].number_format = "dd/mm/yyyy"
    for col, wdt in zip("ABCDEFGHIJKL", (42, 24, 8, 34, 9, 9, 12, 12, 16, 12, 12, 14)):
        ws.column_dimensions[col].width = wdt
    _save(wb, os.path.join(out, "klcp_static_portfolio_2026-12-31.xlsx"), created)
    # Ostvale: its own collateral layout, margins in per cent, S&P-equivalent ratings
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Collateral"
    _sheet_header(ws, "Ostvale Capital Senior Secured Note 2027-1", "Collateral tape, cut-off 31.12.2026")
    hdr = ["Borrower", "Borrower LEI", "Domicile", "GICS industry group", "CCY", "Commitment (CCY m)", "Margin (%)",
           "S&P equivalent at close", "Close date", "Maturity", "Deal type"]
    ws.append([])
    ws.append(hdr)
    for c in sorted(W.Y, key=lambda c: (WD.SECTORS[W.comps[c]["ind"]][3], W.comps[c]["legal"])):
        C = W.comps[c]
        L = W.loans[C["loan"]]
        ws.append([C["legal"] if rng.random() < 0.8 else C["legal"].upper(), C["lei"] if rng.random() < 0.86 else "",
                   COUNTRY_NAME[C["country"]], WD.SECTORS[C["ind"]][3], L["ccy"], L["amount_ccy"],
                   round(L["margin"] / 100.0, 2), WD.RATINGS[L["rating"]], L["orig"], L["maturity"],
                   {"LBO": "Buyout", "SBO": "Secondary", "Refinancing": "Refi"}[L["purpose"]]])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[8].number_format = row[9].number_format = "yyyy-mm-dd"
    for col, wdt in zip("ABCDEFGHIJK", (44, 24, 16, 40, 6, 18, 10, 14, 12, 12, 12)):
        ws.column_dimensions[col].width = wdt
    _save(wb, os.path.join(out, "ostvale_collateral_tape_20261231.xlsx"), created)


# ---------------------------------------------------------------- reference files and distractors
def sector_codes(out):
    doc = {"publisher": "Lenderbase", "version": "2024.1", "effective": "2024-01-01",
           "note": "Lenderbase classifies each obligor in one sector. The crosswalk gives the agency industry and the GICS industry group that Lenderbase maps each code from.",
           "sectors": [{"code": c, "name": n, "agency_industry": a, "gics_industry_group": g} for c, n, a, g, _ in WD.SECTORS]}
    with open(os.path.join(out, "lenderbase_sector_codes.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


ECB_ANCHORS = [("USD", 1.1712, 4), ("JPY", 176.42, 2), ("BGN", 1.9558, 4), ("CZK", 24.612, 3), ("DKK", None, 4),
               ("GBP", None, 5), ("HUF", 398.75, 2), ("PLN", 4.2185, 4), ("RON", 5.0821, 4), ("SEK", None, 4),
               ("CHF", None, 4), ("ISK", 146.30, 2), ("NOK", None, 4), ("TRY", 44.8213, 4), ("AUD", 1.7342, 4),
               ("BRL", 6.4127, 4), ("CAD", 1.6158, 4), ("CNY", 8.3104, 4), ("HKD", 9.1052, 4), ("IDR", 19125.84, 2),
               ("ILS", 4.1376, 4), ("INR", 101.4520, 4), ("KRW", 1658.42, 2), ("MXN", 21.4407, 4), ("MYR", 4.9871, 4),
               ("NZD", 1.9614, 4), ("PHP", 67.912, 3), ("SGD", 1.5103, 4), ("THB", 38.247, 3), ("ZAR", 20.4318, 4)]


def fx(rng, out):
    """The ECB's euro reference rates for December 2026, newest first, in the ECB's own column order."""
    days = []
    d = dt.date(2026, 12, 1)
    while d <= dt.date(2026, 12, 31):
        if d.weekday() < 5 and d not in (dt.date(2026, 12, 25), dt.date(2026, 12, 26)):
            days.append(d)
        d += dt.timedelta(days=1)
    cols = []
    for ccy, anchor, dp in ECB_ANCHORS:
        a = WD.FX[ccy] if anchor is None else anchor
        vals, v = [], a
        for _ in days:
            vals.append(v)
            v = v * float(np.exp(rng.normal(0, 0.0002 if ccy in ("DKK", "BGN") else 0.003)))
        cols.append((ccy, dp, vals[::-1]))
    rows = []
    for j, d in enumerate(days):
        rows.append([d.isoformat()] + [("%." + str(dp) + "f") % vals[j] for _, dp, vals in cols])
    rows.sort(key=lambda r: r[0], reverse=True)
    _write_csv(os.path.join(out, "ecb_euro_reference_rates_2026-12.csv"), ["Date"] + [c for c, _, _ in cols], rows)


def euribor(rng, out):
    rows = []
    spot = {"1M": 2.012, "3M": 2.064, "6M": 2.118, "12M": 2.187}
    for k, v in spot.items():
        rows.append(["fixing", "2026-12-31", k, "%.3f" % v])
    v = 2.064
    for y in range(2027, 2033):
        for q in (3, 6, 9, 12):
            v = v + float(rng.normal(0.012, 0.03))
            rows.append(["forward", "%d-%02d-%02d" % (y, q, 28 if q != 12 else 31), "3M", "%.3f" % v])
    _write_csv(os.path.join(out, "euribor_forward_curve_2026-12-31.csv"), ["kind", "date", "tenor", "rate_pct"], rows)


def liabilities(rng, out):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Matching cash flows"
    ws["A1"] = "PHL matching portfolio: projected benefit cash flows, EUR m (nominal), valuation date 31-12-2026"
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Year", "Retirement benefits", "Survivor benefits", "Disability benefits", "Total"])
    for y in range(2027, 2077):
        t = y - 2026
        rb = 410.0 * np.exp(0.035 * min(t, 18)) * np.exp(-0.06 * max(0, t - 18))
        sb = 0.18 * rb * (1 + 0.01 * t)
        db = 22.0 * np.exp(-0.03 * t)
        ws.append([y, round(rb, 1), round(sb, 1), round(db, 1), round(rb + sb + db, 1)])
    ws.column_dimensions["A"].width = 8
    for col in "BCDE":
        ws.column_dimensions[col].width = 20
    _save(wb, os.path.join(out, "phl_matching_portfolio_cashflows_2027-2076.xlsx"), dt.datetime(2026, 11, 20, 14, 3))


def write(W, out):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(W.seed + 101)
    lb_id, n_lb = lenderbase(W, rng, out)
    n_wo = workouts(W, rng, out, lb_id)
    n_dt = dealtrail(W, rng, out)
    n_lei = lei_extract(W, rng, out)
    tapes(W, rng, out)
    sector_codes(out)
    fx(rng, out)
    euribor(rng, out)
    liabilities(rng, out)
    return dict(lenderbase_rows=n_lb, workout_rows=n_wo, dealtrail_rows=n_dt, lei_rows=n_lei, lb_id=lb_id)


if __name__ == "__main__":
    import sys
    W = WD.simulate()
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/task9_pack"
    info = write(W, out)
    print({k: v for k, v in info.items() if k != "lb_id"})
