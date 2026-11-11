"""The data files under target/, each in the form the system that exports it writes: the WMS's zone-hour labour log
and its pick confirmations, the two payroll exports (the old system's semicolon file with decimal commas, the new
one's), the forecast archive and the client's 2027 budget workbook, the order imports, Huippu Sport's own exports,
the item master, the slotting, the roster and the site manager's draft plan. Distractors: the packing benches' log
and the returns register."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import cal
import params as P
import records as RC
import sim

FILES = {
    "zone_hours": "wms_zone_hours_2022-01_2026-10.csv",
    "pay_old": "palkka_tuntikirjaukset_2022-2023.csv",
    "pay_new": "timesheets_2024-01_2026-10.csv",
    "archive": "kotikaari_forecast_archive_2021-10_2026-10.csv",
    "budget27": "kotikaari_budget_2027.xlsx",
    "k_orders": "wms_order_import_kotikaari_2022-01_2026-10.csv",
    "h_daily": "huippu_orders_daily_2024-01_2026-10.csv",
    "h_monthly": "huippu_article_lines_2024-11_2026-10.csv",
    "item_master": "wms_item_master_2026-11-02.xlsx",
    "slotting": "huippu_slotting_2027.xlsx",
    "pilot": "wms_pick_confirmations_HUI_2026w37-w44.csv",
    "roster": "saarnela_own_pickers_2027.xlsx",
    "draft": "saarnela_peak_2027_staffing.xlsx",
    "standard": "saarnela_labour_planning_standard_issue4.pdf",
    "agreement": "tyopiste_framework_agreement_2025.pdf",
    "review": "huippu_pilot_review_2026-11.docx",
    "benches": "saarnela_packing_benches_2026-01_2026-10.csv",
    "returns": "kotikaari_returns_received_2024-01_2026-10.csv",
}
DISTRACTORS = ["benches", "returns"]
FI_W = dt.timezone(dt.timedelta(hours=2))
FI_S = dt.timezone(dt.timedelta(hours=3))
OLD_CC = {"P1": "4111", "P2": "4112", "B1": "4113", "PACK": "4150"}
OLD_ABS = {"SICK": "S", "VAC": "L"}


def fi(x, nd=2):
    return ("%.*f" % (nd, x)).replace(".", ",")


def write_csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=delim, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def zone_hours(w, path):
    df = RC.zone_hours(w)
    df = df[df["date"] >= P.DATA_START].sort_values(["date", "hour", "zone"])
    rows = [list(r) for r in df.itertuples(index=False)]
    out = []
    for r in rows:
        r[0] = r[0].isoformat()
        out.append(r)
        if r[0] in ("2023-03-14", "2023-03-15", "2025-06-02"):    # the nightly export run twice
            out.append(list(r))
    return write_csv(path, RC.ZH_COLS, out)


def payroll(w, old_path, new_path):
    ts = RC.timesheets(w)
    ts = ts[ts["date"] >= P.DATA_START].sort_values(["date", "zone", "shift", "employer", "person"], kind="mergesort")
    old, new = [], []
    for r in ts.itertuples(index=False):
        if r.date < P.PAYROLL_SWITCH:
            old.append((r.date.strftime("%-d.%-m.%Y"), r.person, r.employer, OLD_CC[r.zone],
                        "A" if r.shift == "DAY" else "I", r.start, r.end, fi(r.paid, 1) if r.paid else "0",
                        OLD_ABS.get(r.absence, ""), fi(r.absence_hours, 1) if r.absence_hours else ""))
        else:
            run = "PR-%s" % r.date.strftime("%Y%m")
            row = (r.date.isoformat(), r.person, r.employer, "SAA-" + r.zone, r.shift, r.start, r.end,
                   "%.2f" % r.paid, r.absence, "%.2f" % r.absence_hours if r.absence_hours else "", run)
            new.append(row)
            if r.date.year == 2024 and r.date.month == 3:          # March 2024's correction run re-sent the month
                new.append(row[:-1] + ("PR-202403-K",))
    n1 = write_csv(old_path, ["pvm", "henkilonumero", "tyonantaja", "kustannuspaikka", "vuoro", "alkoi", "paattyi",
                              "tunnit", "poissaolo", "poissaolotunnit"], old, delim=";")
    n2 = write_csv(new_path, ["work_date", "person_id", "employer", "cost_centre", "shift", "start", "end",
                              "paid_hours", "absence_code", "absence_hours", "payroll_run"], new)
    return n1, n2


def archive(w, path):
    f = RC.forecasts(w)
    f = f[~((f["round"] == "budget 2027") & (f["brand"] == P.BRAND_H))]   # the archive's import was set up for Kotikaari
    f = f.sort_values(["issued", "round", "brand", "group", "iso_year", "iso_week"], kind="mergesort")
    rows = [(r.issued.isoformat(), r.round, r.brand, r.group, r.iso_year, r.iso_week, r.order_lines, r.note)
            for r in f.itertuples(index=False)]
    return write_csv(path, ["issued", "round", "brand", "group", "iso_year", "iso_week", "order_lines", "note"], rows)


def _head(ws, row, fill="DCE6F0"):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(vertical="top", wrap_text=True)


def _widths(ws, widths):
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


def budget27(w, path):
    f = RC.forecasts(w)
    b = f[f["round"] == "budget 2027"]
    meta_k = w["fmeta"][(P.BRAND_K, 2027)]
    meta_h = w["fmeta"][(P.BRAND_H, 2027)]
    wb = Workbook()
    ws = wb.active
    ws.title = "Cover"
    cover = [("Kotikaari Oy, demand planning", ""),
             ("Year-ahead order line forecast (budget) 2027", ""),
             ("", ""),
             ("Issued", "15.10.2026"),
             ("Prepared by", P.PEOPLE["planning"]),
             ("For", "%s, %s fulfilment centre" % (P.ORG, P.SITE)),
             ("Brands", "Kotikaari; Huippu Sport (fulfilled at %s from 1.3.2027)" % P.SITE),
             ("Unit", "order lines, by ISO week of order"),
             ("Commercial plan 2027, Kotikaari", "small parts +%d %%, bulky +%d %%" % tuple(round(v * 100) for v in meta_k["g"])),
             ("Commercial plan 2027, Huippu Sport", "small parts +%d %%, bulky +%d %%" % tuple(round(v * 100) for v in meta_h["g"])),
             ("Weekly phasing", "as in 2025; volumes brought forward by the 2026 year-to-date trend and the 2027 commercial plan"),
             ("Huippu Sport", "forecast on the same basis as Kotikaari by the same team since the integration in 2025")]
    for r in cover:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"].font = Font(bold=True, size=11)
    _widths(ws, [36, 88])
    for brand, title in ((P.BRAND_K, "Kotikaari"), (P.BRAND_H, "Huippu Sport")):
        ws = wb.create_sheet(title)
        ws.append(["ISO week 2027", "Small parts, order lines", "Bulky, order lines"])
        _head(ws, 1)
        sp = b[(b["brand"] == brand) & (b["group"] == "small parts")].set_index("iso_week")["order_lines"]
        bu = b[(b["brand"] == brand) & (b["group"] == "bulky")].set_index("iso_week")["order_lines"]
        for wk in sorted(sp.index):
            ws.append([int(wk), int(sp[wk]), int(bu[wk])])
        ws.append(["Total", int(sum(int(sp[w]) for w in sp.index)), int(sum(int(bu[w]) for w in bu.index))])
        ws.freeze_panes = "A2"
        _widths(ws, [14, 24, 20])
        for row in ws.iter_rows(min_row=2, min_col=2, max_col=3):
            for c in row:
                c.number_format = "#,##0"
    wb.save(path)


def k_orders(w, path):
    k = RC.k_orders(w)
    k = k[k["received"] >= dt.date(2022, 1, 1)]
    rows = [(r.received.isoformat(), r.group, r.web_orders, r.web_lines, r.store_lines) for r in k.itertuples(index=False)]
    return write_csv(path, ["received", "group", "web_orders", "web_lines", "store_lines"], rows)


def h_daily(w, path):
    h = RC.h_daily(w)
    rows = [(r.order_date.strftime("%d/%m/%Y"), r.group, r.orders, r.order_lines, r.units) for r in h.itertuples(index=False)]
    return write_csv(path, ["order_date", "product_line", "orders", "order_lines", "units"], rows)


def h_monthly(w, path):
    h = RC.h_monthly(w).sort_values(["month", "article_no"])
    rows = [(r.month, r.article_no, r.order_lines, r.units) for r in h.itertuples(index=False)]
    return write_csv(path, ["month", "article_no", "order_lines", "units"], rows)


def item_master(im, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Items"
    cols = list(im.columns)
    ws.append(cols)
    _head(ws, 1)
    for r in im.itertuples(index=False):
        ws.append([v.isoformat() if isinstance(v, dt.date) else v for v in r])
    ws.freeze_panes = "A2"
    _widths(ws, [11, 7, 12, 40, 30, 14, 14, 10, 10, 10, 10, 11])
    wb.save(path)


def slotting(sl, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Slotting 2027"
    ws.append(["Huippu Sport articles: pick locations for the March 2027 move (slotting run 30.10.2026)"])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["owner_article", "sku", "zone", "aisle", "bay", "level", "velocity_class"])
    _head(ws, 3)
    for r in sl.sort_values(["zone", "aisle", "bay", "level", "owner_article"]).itertuples(index=False):
        ws.append(list(r))
    ws.freeze_panes = "A4"
    _widths(ws, [14, 11, 7, 7, 7, 7, 14])
    wb.save(path)


def pilot(w, im, path, rng):
    sku = dict(zip(im[im["owner"] == "HUI"]["owner_article"], im[im["owner"] == "HUI"]["sku"]))
    loc = {}
    for a in sorted(w["pilot"]):
        loc[a] = "P2-%02d-%02d-%d" % (int(rng.integers(1, 5)), int(rng.integers(1, 25)), int(rng.choice([1, 2, 2, 3, 3, 4])))
    staff = [x for x in w["staff"] if x["zone"] == "P2"]
    badges = sorted(str(x["emp"]) for x in staff if x["end"] is None)
    pickers = badges[:6]
    rows = []
    tid = 88412000
    order = 5100000
    for (tm, d, h, art, u, k) in w["pilot_conf"]:
        tid += int(rng.integers(1, 4))
        if rng.random() < 0.55:
            order += int(rng.integers(1, 30))
        picker = pickers[(k + d.toordinal()) % len(pickers)]
        stamp = tm.replace(microsecond=0).isoformat(sep=" ")
        rows.append((stamp, tid, picker, "P2", loc[art], sku[art], u, "HS-%07d" % order))
        if rng.random() < 0.006:                         # the scanner confirmed twice
            t2 = (tm + dt.timedelta(seconds=int(rng.integers(2, 9)))).replace(microsecond=0).isoformat(sep=" ")
            rows.append((t2, tid, picker, "P2", loc[art], sku[art], u, "HS-%07d" % order))
    return write_csv(path, ["confirmed_at", "task_id", "picker_id", "zone", "location", "sku", "qty", "order_no"], rows)


def roster(ro, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Own pickers 2027"
    ws.append(["employee_no", "name", "home_zone", "contract_hours_week", "employment_start", "leave_until"])
    _head(ws, 1)
    for r in ro.itertuples(index=False):
        ws.append([int(r.employee_no), r.name, r.home_zone, int(r.contract_hours_week),
                   r.employment_start.isoformat() if isinstance(r.employment_start, dt.date) else r.employment_start,
                   r.leave_until])
    ws.freeze_panes = "A2"
    _widths(ws, [13, 24, 11, 20, 17, 14])
    wb.save(path)


def benches(w, path, rng):
    rows = []
    for d in cal.days(dt.date(2026, 1, 2), dt.date(2026, 10, 30)):
        if not cal.working(d):
            continue
        for b in range(1, 19):
            for sh in ("DAY",):
                parcels = int(rng.normal(310, 45))
                rows.append((d.isoformat(), "PK-%02d" % b, sh, parcels, int(parcels * rng.normal(1.31, 0.08)),
                             round(float(rng.normal(7.1, 0.4)), 2)))
    return write_csv(path, ["date", "bench", "shift", "parcels_closed", "items_packed", "bench_hours"], rows)


def returns(w, path, rng):
    D = w["D"]
    rows = []
    for i, d in enumerate(D["days"]):
        if d < dt.date(2024, 1, 1) or d > dt.date(2026, 10, 31) or not cal.working(d) or d.weekday() >= 5:
            continue
        lag = D["web_s"][max(0, i - 12)]
        n = int(lag * 0.081 * float(np.exp(rng.normal(0, 0.12))))
        for reason, sh in (("wrong size or colour", 0.21), ("not as described", 0.18), ("damaged", 0.09),
                           ("changed mind", 0.52)):
            rows.append((d.isoformat(), reason, int(round(n * sh))))
    return write_csv(path, ["received", "reason", "return_lines"], rows)


def draft(w, f, path):
    """The site manager's draft: the 2025 peak's paid hours a line by zone carried to the 2027 budget's weeks, Huippu
    Sport's lines at the pilot's time a line against P2's, and its check of the rate on days of 2025."""
    import analysis as A
    z = A.zone_hours(f)
    t = A.timesheet(f)
    rate = {zz: A.paid_per_line(z, t, 2025, P.PEAK_WEEKS, zz) for zz in P.ZONES}
    zp = z[(z["zone"] == "P2") & (z["date"] >= pd.Timestamp(P.PILOT[0])) & (z["date"] <= pd.Timestamp(P.PILOT[1]))]
    tp = A.pilot_times(f)
    kot_t = float((zp["task_min"].sum() - tp * zp["lines_hui"].sum()) / zp["kot"].sum())
    ratio = round(tp / kot_t, 2)
    bud_k = {g: A.budget_totals(f, P.BRAND_K, g, 2027) for g in ("small parts", "bulky")}
    bud_h = {g: A.budget_totals(f, P.BRAND_H, g, 2027) for g in ("small parts", "bulky")}
    kz = A.picked_by_week(z)
    kz = kz[(kz["iy"] == 2025) & kz["iw"].isin(P.PEAK_WEEKS)]
    kp1 = float(kz[kz["zone"] == "P1"]["kot"].sum() / kz[kz["zone"].isin(A.Z_SMALL)]["kot"].sum())
    hm = A.hui_mix(f)
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan 2027"
    ws.append(["Saarnela peak 2027, picker hours: DRAFT (T. Nieminen, 2.11.2026)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Volumes: Kotikaari budget 2027 (15.10.2026). Hours a line: peak 2025 (weeks 46 to 50), paid hours over "
               "lines picked, by zone. Huippu Sport lines at the pilot's time a line against P2 (%s)." % fi(ratio)])
    ws.append([])
    ws.append(["ISO week", "Zone", "Kotikaari lines", "Huippu Sport lines", "Paid minutes a line (2025)",
               "Picker hours", "Evening shift"])
    _head(ws, 4)
    for wk in P.PEAK_WEEKS:
        for zz in P.ZONES:
            if zz == "B1":
                lk, lh = bud_k["bulky"][wk], bud_h["bulky"][wk]
            else:
                lk = bud_k["small parts"][wk] * (kp1 if zz == "P1" else 1.0 - kp1)
                lh = bud_h["small parts"][wk] * hm[zz]["share"]
            r = round(rate[zz] * 60.0, 3)
            hrs = (lk * r + lh * r * (ratio if zz != "B1" else 1.0)) / 60.0
            ws.append([wk, zz, int(round(lk)), int(round(lh)), r, int(round(hrs)), "to confirm"])
    _widths(ws, [10, 7, 16, 18, 22, 14, 14])
    ws2 = wb.create_sheet("Rate check")
    ws2.append(["The 2025 rates against the 2025 peak's own days, paid hours as booked"])
    ws2["A1"].font = Font(bold=True)
    ws2.append(["Date", "Zone", "Lines", "Hours at the rate", "Paid hours booked", "Difference %"])
    _head(ws2, 2)
    rng = np.random.default_rng(P.SEED + 11)
    days = sorted(set(z[(z["iy"] == 2025) & z["iw"].isin(P.PEAK_WEEKS)]["date"].dt.date))
    pick = list(range(len(days)))
    tt = t[(t["absence"] == "")]
    for i in pick:
        d = days[i]
        for zz in ("P1", "P2"):
            lines = int(z[(z["date"] == pd.Timestamp(d)) & (z["zone"] == zz)]["lines"].sum())
            booked = float(tt[(tt["date"] == pd.Timestamp(d)) & (tt["zone"] == zz)]["paid"].sum())
            at = lines * rate[zz]
            ws2.append([d.isoformat(), zz, lines, round(at, 1), round(booked, 1),
                        round(100.0 * (at - booked) / booked, 1) if booked else None])
    _widths(ws2, [12, 7, 10, 18, 18, 14])
    wb.save(path)
    return {"rate": rate, "ratio": ratio}


def write_tables(w, target):
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    rng = np.random.default_rng(P.SEED + 5)
    n = {}
    n["zone_hours"] = zone_hours(w, F["zone_hours"])
    n["pay_old"], n["pay_new"] = payroll(w, F["pay_old"], F["pay_new"])
    n["archive"] = archive(w, F["archive"])
    budget27(w, F["budget27"])
    n["k_orders"] = k_orders(w, F["k_orders"])
    n["h_daily"] = h_daily(w, F["h_daily"])
    n["h_monthly"] = h_monthly(w, F["h_monthly"])
    im = RC.item_master(w, rng)
    item_master(im, F["item_master"])
    sl = RC.slotting(w, im, rng)
    slotting(sl, F["slotting"])
    n["pilot"] = pilot(w, im, F["pilot"], rng)
    ro = RC.roster(w, rng)
    roster(ro, F["roster"])
    n["benches"] = benches(w, F["benches"], rng)
    n["returns"] = returns(w, F["returns"], rng)
    return n
