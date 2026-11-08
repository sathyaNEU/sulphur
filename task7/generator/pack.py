"""task7: the warehouse extracts under target/, written from world.py's simulation the way Ardcarn Bank's data
warehouse would export them. Texture (re-keying at the 2021 core migration, legacy codes, reloaded batches,
zero-length type 2 rows, duplicate records from two systems, late postings, inferred members) uses its own random
stream, so it never moves a figure the world decides."""
import csv
import datetime as dt
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

TEXTURE_SEED = 77129
MIGRATION = dt.date(2021, 6, 5)          # core banking conversion: new facility numbers from this date
SNAP_FROM = (2022, 1)                    # the month-end fact extract starts January 2022
EXTRACT_DATE = dt.date(2027, 1, 13)
YEAR_END = dt.date(2026, 12, 31)        # the reporting date the plan is struck at
GO_LIVE = dt.date(2012, 1, 3)           # the warehouse went live
MISSING_SNAPSHOT = (2023, 2)             # the February 2023 month-end batch failed and was never reloaded
RELOADED_SNAPSHOT = (2024, 6)            # the June 2024 batch was loaded twice

TYPES = {
    "Retail": [("Retail unit", 0.55), ("Shop and upper floors", 0.30), ("Retail warehouse", 0.15)],
    "Office": [("Office building", 0.45), ("Office suite", 0.55)],
    "Industrial": [("Industrial unit", 0.50), ("Warehouse", 0.30), ("Light industrial", 0.20)],
    "Hospitality": [("Hotel", 0.35), ("Pub and restaurant", 0.45), ("Guesthouse", 0.20)],
    "Healthcare": [("Nursing home", 0.45), ("Childcare centre", 0.35), ("Medical centre", 0.20)],
}
SERIES = {"Retail": "RET", "Office": "OFF", "Industrial": "IND", "Hospitality": "HOS", "Healthcare": "HLC"}
REG = {"Dublin": "DUB", "Regional cities": "CIT", "Rest of State": "ROS"}
BOOK = {"Retail": "Investment", "Office": "Investment", "Industrial": "Investment",
        "Hospitality": "Owner-occupied", "Healthcare": "Owner-occupied"}
PLACES = {
    "Dublin": [("Dublin 1", "Dublin", "D01"), ("Dublin 2", "Dublin", "D02"), ("Dublin 4", "Dublin", "D04"),
               ("Dublin 8", "Dublin", "D08"), ("Dublin 12", "Dublin", "D12"), ("Dublin 15", "Dublin", "D15"),
               ("Dublin 18", "Dublin", "D18"), ("Swords", "Dublin", "K67"), ("Dún Laoghaire", "Dublin", "A96"),
               ("Tallaght", "Dublin", "D24"), ("Balbriggan", "Dublin", "K32")],
    "Regional cities": [("Cork", "Cork", "T12"), ("Cork", "Cork", "T23"), ("Galway", "Galway", "H91"),
                        ("Limerick", "Limerick", "V94"), ("Waterford", "Waterford", "X91"),
                        ("Ballincollig", "Cork", "P31"), ("Oranmore", "Galway", "H91")],
    "Rest of State": [("Athlone", "Westmeath", "N37"), ("Sligo", "Sligo", "F91"), ("Tralee", "Kerry", "V92"),
                      ("Kilkenny", "Kilkenny", "R95"), ("Letterkenny", "Donegal", "F92"), ("Castlebar", "Mayo", "F23"),
                      ("Ennis", "Clare", "V95"), ("Mullingar", "Westmeath", "N91"), ("Dundalk", "Louth", "A91"),
                      ("Drogheda", "Louth", "A92"), ("Wexford", "Wexford", "Y35"), ("Clonmel", "Tipperary", "E91"),
                      ("Carlow", "Carlow", "R93"), ("Tullamore", "Offaly", "R35"), ("Navan", "Meath", "C15"),
                      ("Killarney", "Kerry", "V93"), ("Portlaoise", "Laois", "R32"), ("Cavan", "Cavan", "H12")],
}
STREETS = ["Main Street", "Church Street", "Market Square", "Bridge Street", "Mill Road", "Station Road",
           "Dublin Road", "Castle Street", "Harbour Road", "Fair Green", "Abbey Street", "Barrack Street",
           "New Road", "Green Street", "Distillery Road", "Quay Street", "John Street", "O'Connell Street"]
ESTATES = ["Business Park", "Industrial Estate", "Enterprise Centre", "Retail Park", "Technology Park"]
SURNAMES = ["Brennan", "Cullinane", "Dineen", "Egan", "Fitzpatrick", "Galvin", "Hegarty", "Joyce", "Kiely",
            "Lenihan", "Mangan", "Nolan", "O'Dwyer", "Phelan", "Quilty", "Ryan", "Sheahan", "Tobin", "Walsh",
            "Ahern", "Bourke", "Coakley", "Daly", "Fahy", "Gleeson", "Horgan", "Kavanagh", "Lynch", "McGrath",
            "Moran", "Noonan", "O'Leary", "Power", "Rabbitte", "Scanlon", "Twomey", "Whelan", "Barrett", "Considine",
            "Donnellan", "Feeney", "Grogan", "Healy", "Keogh", "Lally", "Mulvihill", "Naughton", "O'Mahony"]
FORMS = {"Investment": ["Properties Ltd", "Investments DAC", "Holdings Ltd", "Estates Ltd", "Property Co Ltd"],
         "Owner-occupied": ["Hotels Ltd", "Hospitality Ltd", "Care Ltd", "Leisure Ltd", "Healthcare DAC",
                            "Inns Ltd", "Childcare Ltd"]}
# an owner-occupier's company name follows the business on its property
OWN_FORMS = {"Hotel": ["Hotels Ltd", "Hotel Ltd", "Hospitality Ltd"],
             "Guesthouse": ["Guesthouse Ltd", "Hospitality Ltd", "Accommodation Ltd"],
             "Pub and restaurant": ["Inns Ltd", "Bar and Restaurant Ltd", "Taverns Ltd"],
             "Nursing home": ["Nursing Home Ltd", "Care Ltd", "Healthcare DAC"],
             "Childcare centre": ["Childcare Ltd", "Early Years Ltd", "Creche Ltd"],
             "Medical centre": ["Medical Ltd", "Healthcare DAC", "Practice Ltd"]}
# value per square metre at an index level of 100, for a property's floor area (Dublin dearer, the rest of the State less)
RATE_M2 = {"Retail unit": 3000, "Shop and upper floors": 2500, "Retail warehouse": 1100, "Office building": 2200,
           "Office suite": 2800, "Industrial unit": 900, "Warehouse": 700, "Light industrial": 1000, "Hotel": 1100,
           "Pub and restaurant": 2200, "Guesthouse": 1700, "Nursing home": 1000, "Childcare centre": 2400,
           "Medical centre": 2400}
RATE_REGION = {"Dublin": 1.4, "Regional cities": 1.0, "Rest of State": 0.75}
VALUERS = ["Hanlon Gaffney & Co", "Mulcahy Dunne", "Tierney Prendergast", "Keane O'Brien Surveyors",
           "Corless Valuers", "Byrne Lattimore", "Kenefick & Ward"]
RECEIVERS = ["Molloy Nevin Recovery", "Cregan Hollis Receiverships", "Delahunt Barry", "Fennelly Ross Partners"]
NACE = {"Retail": ("68.20", "Renting and operating of own or leased real estate"),
        "Office": ("68.20", "Renting and operating of own or leased real estate"),
        "Industrial": ("68.20", "Renting and operating of own or leased real estate"),
        "Hotel": ("55.10", "Hotels and similar accommodation"), "Guesthouse": ("55.20", "Holiday and other short-stay accommodation"),
        "Pub and restaurant": ("56.30", "Beverage serving activities"),
        "Nursing home": ("87.10", "Residential nursing care activities"),
        "Childcare centre": ("88.91", "Child day-care activities"),
        "Medical centre": ("86.21", "General medical practice activities")}


def d2(x):
    return "%.2f" % x


def ymd(d):
    return d.strftime("%Y-%m-%d")


def key(d):
    return int(d.strftime("%Y%m%d"))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def day_in(i, rng, lo=2, hi=27):
    y, m = W.MONTHS[i]
    return dt.date(y, m, int(rng.integers(lo, hi + 1)))


class Pack:
    pass


def assemble(w):
    """identities, dates and texture decisions shared by every file and by the golden"""
    rng = np.random.default_rng(TEXTURE_SEED)
    P = Pack()
    P.w = w
    nf, npp = len(w.facs), len(w.props)
    # the warehouse holds facilities on the book at any time from January 2012 (its initial load)
    i12 = W.MI[W.RECORD_START]
    P.facs = [fi for fi, f in enumerate(w.facs) if f["end"] is None or f["end"] >= i12]
    keep = set(P.facs)
    P.props = sorted({p for fi in P.facs for p in w.facs[fi]["props"]})
    # facility numbers: legacy core banking numbers, re-issued at the June 2021 conversion
    perm = rng.permutation(nf)
    # numbers handed out over years with gaps (closed applications, other products); each is increasing in the same
    # permutation index as before, so every sort by number keeps its order, and the gaps come from a stream of their own
    id_rng = np.random.default_rng(TEXTURE_SEED + 17)
    leg_no = 1040000 + np.cumsum(id_rng.integers(5, 70, nf))
    P.legacy = {fi: "CRL-%07d" % int(leg_no[int(perm[fi])]) for fi in range(nf)}
    mig_i = W.MI[(2021, 6)]
    live_at_mig = {fi for fi in keep if W.MI[w.facs[fi]["orig"]] <= mig_i and (w.facs[fi]["end"] is None or w.facs[fi]["end"] >= mig_i)}
    born_after = {fi for fi in keep if W.MI[w.facs[fi]["orig"]] > mig_i}
    newset = sorted(live_at_mig | born_after, key=lambda fi: (W.MI[w.facs[fi]["orig"]], fi))
    P.new = {fi: "AB%09d" % (310000000 + 7919 * k + int(rng.integers(0, 7000))) for k, fi in enumerate(newset)}
    P.current_no = {fi: P.new.get(fi, P.legacy[fi]) for fi in P.facs}
    P.migrated = live_at_mig
    # customers and properties
    nb = max(f["borrower"] for f in w.facs) + 1
    cust_no = 200000 + np.cumsum(id_rng.integers(2, 25, nb))
    P.cust = {b: "C%06d" % int(cust_no[int(x)]) for b, x in zip(range(nb), rng.permutation(nb))}
    P.ptype, P.place, P.addr, P.pid = {}, {}, {}, {}
    pperm = rng.permutation(npp)
    pid_no = 500000 + np.cumsum(id_rng.integers(2, 21, npp))
    for p in range(npp):
        pr = w.props[p]
        names, wts = zip(*TYPES[pr["sector"]])
        P.ptype[p] = str(rng.choice(names, p=np.array(wts) / sum(wts)))
        town, county, rk = PLACES[pr["region"]][int(rng.integers(0, len(PLACES[pr["region"]])))]
        P.place[p] = (town, county, rk + " " + "".join(rng.choice(list("ACDEFHKNPRTVWXY0123456789"), 4)))
        if pr["sector"] == "Industrial" or P.ptype[p] in ("Retail warehouse",):
            P.addr[p] = "Unit %d, %s %s" % (int(rng.integers(1, 40)), town, str(rng.choice(ESTATES)))
        else:
            P.addr[p] = "%d %s, %s" % (int(rng.integers(1, 120)), str(rng.choice(STREETS)), town)
        P.pid[p] = "P%06d" % int(pid_no[int(pperm[p])])
    first_fac = {}
    for fi in range(nf):
        for p in w.facs[fi]["props"]:
            first_fac.setdefault(p, fi)
    P.cust_name = {}
    for b in range(nb):
        fi = next(fi for fi in range(nf) if w.facs[fi]["borrower"] == b)
        bk = BOOK[w.props[w.facs[fi]["props"][0]]["sector"]]
        surname, form = SURNAMES[int(rng.integers(0, len(SURNAMES)))], str(rng.choice(FORMS[bk]))
        t0 = P.ptype.get(w.facs[fi]["props"][0])
        if t0 in OWN_FORMS:
            form = OWN_FORMS[t0][b % len(OWN_FORMS[t0])]
        P.cust_name[b] = "%s %s" % (surname, form)
    # dates of events
    P.orig_date = {fi: day_in(W.MI[w.facs[fi]["orig"]], rng) for fi in range(nf)}
    P.insp_date = {}
    for p in range(npp):
        for (i, val, why) in w.props[p]["insp"]:
            d = day_in(i, rng, 3, 26)
            if why == "origination":
                fi = first_fac[p]
                d = min(d, P.orig_date[fi] - dt.timedelta(days=int(rng.integers(8, 40))))
            P.insp_date[(p, i, why)] = d
    P.default_date = {}
    for ev in w.defaults:
        d = day_in(ev["month"], rng, 1, 28)
        for fi in ev["facs"]:
            P.default_date[fi] = d
    P.sale_date = {}
    for s in w.sales:
        if s["sale_month"] < W.NM:
            P.sale_date[s["prop"]] = day_in(s["sale_month"], rng, 2, 27)
    P.inferred = set()
    lastq = W.NQ - 2   # 2026 Q3: the latest index quarter out by the extract
    for p in P.props:
        if W.MONTHS[w.props[p]["insp"][0][0]] >= (2026, 11):
            P.inferred.add(p)
    P.rng = rng
    P.lastq = lastq
    return P


# ------------------------------------------------------------------ valuation history (type 2)


def valuation_rows(P):
    """every valuation the warehouse holds for each property: inspections, and from 2012 the quarterly roll-forward
    of the latest inspection by the property's index series, as published when the quarter's release came out"""
    w, rng = P.w, P.rng
    rows = []
    sale_q = {}
    for s in w.sales:
        if s["sale_month"] < W.NM:
            sale_q[s["prop"]] = W.QI[W.quarter_of(s["sale_month"])]
    active_until = {}
    for fi in P.facs:
        f = w.facs[fi]
        for p in f["props"]:
            end = f["end"]
            if end is None:
                q = W.NQ - 1
            elif f["end_kind"] == "default":
                q = sale_q.get(p, W.NQ - 1)
            else:
                q = W.QI[W.quarter_of(end)]
            active_until[p] = max(active_until.get(p, -1), q)
    for p in P.props:
        pr = w.props[p]
        ser = (pr["sector"], pr["region"])
        code = "BRCPI-%s-%s" % (SERIES[pr["sector"]], REG[pr["region"]])
        ins = pr["insp"]
        events = []
        for (i, val, why) in ins:
            d = P.insp_date[(p, i, why)]
            eff = d + dt.timedelta(days=int(rng.integers(6, 32)))
            if d <= YEAR_END < eff:
                # the year-end close loads every valuation report dated in the year before the books are struck
                eff = d + dt.timedelta(days=int(rng.integers(1, (YEAR_END - d).days + 1)))
            events.append(("I", d, eff, float(val), why, None))
        # quarterly roll-forwards while the property secures a facility on the book: the warehouse's go-live on
        # 3 January 2012 rolled every value forward to 2011 Q3, the latest quarter then published, and the register
        # has written one at each quarter's release since
        q0 = W.QI[(2011, 3)]
        for k in range(q0, min(active_until.get(p, -1), P.lastq) + 1):
            qe = W.quarter_end(k)
            first = [r for r in w.rel[ser] if r[0] == k and r[1] == 0]
            if not first:
                continue
            load = GO_LIVE if k == q0 else first[0][2]
            anchors = [(d, v) for (t, d, eff, v, why, _) in events if t == "I" and d <= qe]
            if not anchors:
                continue
            # an inspection dated after the quarter end and on file by the release is newer than any roll-forward
            # to that quarter end, so the register writes none
            if any(t == "I" and d > qe and eff <= load for (t, d, eff, v, why, _) in events):
                continue
            ad, av = anchors[-1]
            ka = W.QI.get((ad.year, (ad.month - 1) // 3 + 1), 0)   # a December 2003 inspection rolls from 2004 Q1
            pub = W.published(w.rel[ser], load)
            if k not in pub or ka not in pub:
                continue
            value = av * pub[k] / pub[ka]
            events.append(("X", qe, load, round(value), None, "%dQ%d" % W.QUARTERS[k]))
        events.sort(key=lambda e: (e[2], 0 if e[0] == "X" else 1, e[1]))
        for n, (t, d, eff, v, why, q) in enumerate(events):
            legacy = eff < MIGRATION
            if t == "I":
                basis = "FULL" if legacy else "INSPECTION"
                valuer = str(rng.choice(VALUERS))
                ref = "%s/%d/%04d" % ("".join(x[0] for x in valuer.split()[:2]).upper(), d.year, int(rng.integers(1, 9999)))
                rows.append(dict(p=p, eff=eff, basis=basis, vdate=d, value=v, series=code, quarter="", valuer=valuer,
                                 ref=ref, why=why))
            else:
                basis = "IDX" if legacy else "INDEX ROLL-FORWARD"
                rows.append(dict(p=p, eff=eff, basis=basis, vdate=d, value=v, series=code, quarter=q, valuer="",
                                 ref="", why=None))
    return rows


def write_valuations(P, target):
    rng = P.rng
    rows = valuation_rows(P)
    byp = {}
    for r in rows:
        byp.setdefault(r["p"], []).append(r)
    out = []
    sk = 9100000
    for p in sorted(byp, key=lambda p: P.pid[p]):
        rs = byp[p]
        chain = []
        for n, r in enumerate(rs):
            chain.append(dict(r))
            # a same-day correction: the clerk keyed a value, the load corrected it the same day (zero-length row)
            if r["basis"] in ("FULL", "INSPECTION") and rng.random() < 0.025:
                bad = dict(r)
                bad["value"] = round(r["value"] * float(rng.choice([10.0, 0.1, 1.1, 0.9])))
                chain.insert(len(chain) - 1, bad)
        for n, r in enumerate(chain):
            nxt = chain[n + 1]["eff"] if n + 1 < len(chain) else None
            if nxt is not None and nxt == r["eff"]:
                exp = r["eff"] - dt.timedelta(days=1)
            elif nxt is not None:
                exp = nxt - dt.timedelta(days=1)
            else:
                exp = dt.date(9999, 12, 31)
            cur = "Y" if nxt is None else "N"
            sk += 1
            out.append([P.pid[p], sk, ymd(r["eff"]), ymd(exp), cur, r["basis"], ymd(r["vdate"]), "%d" % r["value"],
                        r["series"], r["quarter"], r["valuer"], r["ref"], "B%s" % r["eff"].strftime("%Y%m%d")])
        # an extract re-sent for a few properties: the same rows twice
        if rng.random() < 0.004:
            out.extend([list(x) for x in out[-min(4, len(chain)):]])
    # a handful of rows left flagged current after a later row superseded them
    flips = rng.choice(len(out), size=9, replace=False)
    for k in flips:
        if out[k][4] == "N" and out[k][5] in ("IDX", "INDEX ROLL-FORWARD"):
            out[k][4] = "Y"
    write_csv(os.path.join(target, "dw_dim_property_valuation_2004_2026.csv"),
              ["property_id", "valuation_key", "row_effective_date", "row_expiry_date", "current_row_ind",
               "valuation_basis", "valuation_date", "market_value_eur", "index_series", "index_quarter", "valuer",
               "valuer_ref", "load_batch"], out)
    return len(out)


# ------------------------------------------------------------------ the month-end fact


def maturity_at(f, i, orig_date):
    ext = sum(e for (k, e) in f["extensions"] if k < i)
    base = f["term"] - sum(e for (k, e) in f["extensions"])
    months = base + ext
    y, m = orig_date.year + (orig_date.month - 1 + months) // 12, (orig_date.month - 1 + months) % 12 + 1
    return dt.date(y, m, min(orig_date.day, 28))


def write_snapshot(P, target):
    w, rng = P.w, P.rng
    rows = []
    i0 = W.MI[SNAP_FROM]
    sale_m = {}
    for s in w.sales:
        for fi in s["facs"]:
            sale_m[fi] = max(sale_m.get(fi, -1), s["sale_month"])
    arrears = {}
    for i in range(i0, W.NM):
        ym = W.MONTHS[i]
        if ym == MISSING_SNAPSHOT:
            continue
        me = W.month_end(i)
        batch = "MEB%s-01" % me.strftime("%Y%m")
        month_rows = []
        for fi in P.facs:
            f = w.facs[fi]
            if W.MI[f["orig"]] > i:
                continue
            g = f["grades"].get(i)
            defaulted = f["end_kind"] == "default" and f["end"] is not None and f["end"] <= i
            if f["end"] is not None and f["end"] < i and not defaulted:
                continue
            if defaulted:
                if sale_m.get(fi, W.NM + 99) < i:
                    continue
                bal = w.facs[fi]["bal_def"] if "bal_def" in w.facs[fi] else (W.balance(f, f["end"]) or f["amount"])
                grade_s, stage, dflag = "D", 3, "Y"
                arr = (i - f["end"]) * 30 + 95
            else:
                if g is None:
                    continue
                bal = W.balance(f, i)
                if bal is None:
                    continue
                grade_s = ("%02d" % g) if ym < (2023, 1) else str(g)
                a = arrears.get(fi, 0)
                if g >= 7 and rng.random() < 0.08:
                    a = int(rng.choice([12, 18, 33, 41, 62]))
                elif rng.random() < 0.004:
                    a = int(rng.choice([3, 6, 9]))
                else:
                    a = 0
                arrears[fi] = a
                arr = a
                stage = 2 if (g >= 6 or a >= 30) else 1
                dflag = "N"
            mat = maturity_at(f, i, P.orig_date[fi])
            month_rows.append([key(me), P.new.get(fi, P.legacy[fi]), P.cust[f["borrower"]],
                               "IO" if f["bullet"] else "AMORT", BOOK[w.props[f["props"][0]]["sector"]].upper()[:3],
                               d2(bal), d2(0.0), arr, grade_s, stage, dflag, "%.2f" % f["rate"], ymd(mat), batch])
        rows.extend(month_rows)
        if ym == RELOADED_SNAPSHOT:
            rows.extend([r[:-1] + ["MEB%s-02" % me.strftime("%Y%m")] for r in month_rows])
    write_csv(os.path.join(target, "dw_fact_loan_month_end_2022_2026.csv"),
              ["month_end_key", "facility_no", "customer_no", "repayment_type", "lending_book", "balance_eur",
               "undrawn_eur", "days_past_due", "internal_grade", "ifrs9_stage", "default_flag", "interest_rate_pct",
               "maturity_date", "load_batch"], rows)
    return len(rows)


# ------------------------------------------------------------------ registers and the record

import postprocess  # noqa: E402

STAMP = dt.datetime(2027, 1, 13, 18, 40)


def wb_new(creator):
    wb = openpyxl.Workbook()
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = STAMP
    wb.properties.modified = STAMP
    return wb


def sheet(ws, header, rows, widths, datecols=(), money=()):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    for row in ws.iter_rows(min_row=2):
        for k in datecols:
            row[k].number_format = "dd/mm/yyyy"
        for k in money:
            row[k].number_format = "#,##0"
    ws.freeze_panes = "A2"


def status_of(P, fi):
    w = P.w
    f = w.facs[fi]
    if f["end"] is None:
        return "Live", None
    if f["end_kind"] == "default":
        sold = [P.sale_date[p] for p in f["props"] if p in P.sale_date]
        if len(sold) == len(f["props"]):
            return "Closed - sold", max(sold)
        return "In default", P.default_date[fi]
    return ("Matured" if f["end_kind"] == "maturity" else "Repaid"), W.month_end(f["end"])


def write_facility_register(P, target):
    w, rng = P.w, P.rng
    wb = wb_new("Ardcarn Bank Lending Operations")
    ws = wb.active
    ws.title = "Facilities"
    rows = []
    for fi in sorted(P.facs, key=lambda fi: P.current_no[fi]):
        f = w.facs[fi]
        st, sd = status_of(P, fi)
        base = f["term"] - sum(e for (k, e) in f["extensions"])
        mat = maturity_at(f, W.NM, P.orig_date[fi])
        rows.append([P.current_no[fi], P.legacy[fi] if fi in P.migrated else None, P.cust[f["borrower"]],
                     BOOK[w.props[f["props"][0]]["sector"]],
                     "Interest-only term loan" if f["bullet"] else "Amortising term loan",
                     P.orig_date[fi], int(f["amount"]), base, mat, len(f["extensions"]), st, sd])
    sheet(ws, ["facility_no", "legacy_facility_no", "customer_no", "lending_book", "product", "origination_date",
               "original_amount_eur", "original_term_months", "maturity_date", "times_extended", "status",
               "status_date"], rows, [14, 15, 11, 15, 22, 13, 15, 12, 13, 10, 13, 12], datecols=(5, 8, 11), money=(6,))
    ws2 = wb.create_sheet("Customers")
    crow = []
    seen = set()
    for fi in P.facs:
        b = w.facs[fi]["borrower"]
        if b in seen:
            continue
        seen.add(b)
        p = w.facs[fi]["props"][0]
        sec = w.props[p]["sector"]
        code, desc = NACE.get(P.ptype[p], NACE[sec] if sec in NACE else ("68.20", ""))
        name = P.cust_name[b]
        if rng.random() < 0.03:
            name = name.upper()
        elif rng.random() < 0.03:
            name = name + " "
        crow.append([P.cust[b], name, P.place[p][1], code, desc])
    crow.sort()
    sheet(ws2, ["customer_no", "customer_name", "county", "nace_code", "nace_description"], crow, [11, 34, 12, 9, 48])
    path = os.path.join(target, "facility_register_2026-12.xlsx")
    wb.save(path)
    postprocess.scrub(path, "Ardcarn Bank Lending Operations", "2027-01-13")
    postprocess.finish_office(path, "2019-03-04T09:12:00Z", "2027-01-13T18:40:00Z", "Ardcarn Bank")
    return len(rows), len(crow)


def write_property_dim(P, target):
    w, rng = P.w, P.rng
    area_rng = np.random.default_rng(TEXTURE_SEED + 11)
    rows = []
    for p in sorted(P.props, key=lambda p: P.pid[p]):
        t = P.ptype[p]
        lo, hi = {"Retail unit": (90, 900), "Shop and upper floors": (120, 600), "Retail warehouse": (800, 4000),
                  "Office building": (600, 6000), "Office suite": (120, 900), "Industrial unit": (300, 2500),
                  "Warehouse": (900, 8000), "Light industrial": (200, 1500), "Hotel": (1800, 9000),
                  "Pub and restaurant": (250, 1200), "Guesthouse": (300, 1100), "Nursing home": (1500, 6000),
                  "Childcare centre": (250, 900), "Medical centre": (200, 1400)}[t]
        int(rng.integers(lo, hi))   # the texture stream's draw is kept so every later draw stays where it was
        pr = w.props[p]
        i0, v_first, _ = pr["insp"][0]
        lvl = w.true[(pr["sector"], pr["region"])][W.QI[W.quarter_of(i0)]]
        raw = v_first / (RATE_M2[t] * RATE_REGION[pr["region"]] * lvl / 100.0) * math.exp(area_rng.normal(0, 0.18))
        area = max(40, int(round(raw, -1 if raw < 1000 else -2)))
        tenure = "Freehold" if rng.random() < 0.86 else "Long leasehold"
        town, county, eir = P.place[p]
        first = P.insp_date[(p,) + tuple(w.props[p]["insp"][0][:1]) + (w.props[p]["insp"][0][2],)]
        loaded = max(first, dt.date(2012, 1, 9))
        if p in P.inferred:
            rows.append([P.pid[p], "", "Unknown", "Unknown", "", "Unknown", "", "", "Y", ymd(loaded), "INFERRED"])
        else:
            rows.append([P.pid[p], P.addr[p], town, county, eir, t, area, tenure, "Y", ymd(loaded), "PROPDIM"])
    write_csv(os.path.join(target, "dw_dim_property_2026-12.csv"),
              ["property_id", "address_line", "town", "county", "eircode", "property_type", "floor_area_m2", "tenure",
               "current_row_ind", "row_effective_date", "source"], rows)
    return len(rows)


def closure_date(P, fi):
    f = P.w.facs[fi]
    if f["end"] is None:
        return None
    if f["end_kind"] == "default":
        sold = [P.sale_date[p] for p in f["props"] if p in P.sale_date]
        return max(sold) if len(sold) == len(f["props"]) else None
    return W.month_end(f["end"])


def write_bridge(P, target):
    w = P.w
    rows = []
    for fi in sorted(P.facs, key=lambda fi: P.current_no[fi]):
        f = w.facs[fi]
        start = P.orig_date[fi]
        end = closure_date(P, fi)
        for p in f["props"]:
            if fi in P.migrated:
                rows.append([P.legacy[fi], P.pid[p], 1, ymd(start), ymd(MIGRATION - dt.timedelta(days=1)), "N"])
                rows.append([P.new[fi], P.pid[p], 1, ymd(MIGRATION), ymd(end) if end else "9999-12-31", "N" if end else "Y"])
            else:
                no = P.new.get(fi, P.legacy[fi])
                rows.append([no, P.pid[p], 1, ymd(start), ymd(end) if end else "9999-12-31", "N" if end else "Y"])
    write_csv(os.path.join(target, "dw_bridge_facility_security_2026-12.csv"),
              ["facility_no", "property_id", "charge_rank", "row_effective_date", "row_expiry_date", "current_row_ind"],
              rows)
    return len(rows)


def ead_at_default(w, fi):
    f = w.facs[fi]
    return round(W.balance(f, f["end"]) or f["amount"], 2)


def write_defaults(P, target):
    w, rng = P.w, P.rng
    rows = []
    n = 0
    for ev in sorted(w.defaults, key=lambda e: (e["month"], e["borrower"])):
        if ev["month"] < W.MI[W.RECORD_START]:
            continue
        for fi in ev["facs"]:
            d = P.default_date[fi]
            no = P.legacy[fi] if d < MIGRATION else P.new[fi]
            trig = str(rng.choice(["90 days past due", "Unlikely to pay", "Receiver appointed"], p=[0.62, 0.28, 0.10]))
            st, sd = status_of(P, fi)
            n += 1
            ref = "DF%s-%04d" % (d.strftime("%y"), n)
            row = [ref, no, P.cust[w.facs[fi]["borrower"]], ymd(d), trig, d2(ead_at_default(w, fi)),
                   "Closed - sold" if st == "Closed - sold" else "In workout", ymd(sd) if st == "Closed - sold" else ""]
            rows.append(row)
            if rng.random() < 0.06:
                d2_ = d + dt.timedelta(days=int(rng.integers(0, 21)))
                rows.append(["CL" + ref[2:], no, row[2], ymd(d2_), "90 days past due" if trig != "90 days past due" else "Unlikely to pay",
                             row[5], row[6], row[7]])
    write_csv(os.path.join(target, "default_register_2012_2026.csv"),
              ["default_ref", "facility_no", "customer_no", "default_date", "default_trigger", "balance_at_default_eur",
               "workout_status", "closed_date"], rows)
    return len(rows)


def write_sales(P, target):
    w, rng = P.w, P.rng
    rows, post = [], []
    n = 0
    for s in sorted(w.sales, key=lambda s: (s["sale_month"], s["prop"])):
        if s["default_month"] < W.MI[W.RECORD_START] or s["prop"] not in P.sale_date:
            continue
        comp = P.sale_date[s["prop"]]
        n += 1
        ref = "RS-%d-%04d" % (comp.year, n)
        agreed = comp - dt.timedelta(days=int(rng.integers(28, 95)))
        rec = str(rng.choice(RECEIVERS))
        rows.append([ref, P.pid[s["prop"]], rec, ymd(agreed), ymd(comp), "%d" % s["price"], "%d" % s["costs"]])
        if rng.random() < 0.05:
            rows.append([ref + "-S", P.pid[s["prop"]], rec, "", ymd(comp + dt.timedelta(days=int(rng.integers(1, 7)))),
                         "%d" % s["price"], ""])
        # proceeds net of costs, shared across the borrower's facilities in proportion to their balances at default
        eads = {fi: ead_at_default(w, fi) for fi in s["facs"] if s["prop"] in w.facs[fi]["props"]}
        if not eads:
            eads = {fi: ead_at_default(w, fi) for fi in s["facs"]}
        tot = sum(eads.values())
        net = s["price"] - s["costs"]
        pd_ = comp + dt.timedelta(days=int(rng.integers(0, 76)))
        for fi, e in sorted(eads.items()):
            no = P.legacy[fi] if P.default_date[fi] < MIGRATION else P.new[fi]
            if pd_ <= EXTRACT_DATE:
                post.append([no, ymd(pd_), d2(s["price"] * e / tot), "Sale proceeds", ref])
                post.append([no, ymd(pd_), d2(-s["costs"] * e / tot), "Selling costs", ref])
    write_csv(os.path.join(target, "receiver_sales_2012_2026.csv"),
              ["sale_ref", "property_id", "receiver", "sale_agreed_date", "completion_date", "gross_price_eur",
               "selling_costs_eur"], rows)
    post.sort(key=lambda r: (r[1], r[0], r[3]))
    out = [["RP%07d" % (k + 1)] + r for k, r in enumerate(post)]
    write_csv(os.path.join(target, "recovery_postings_2012_2027.csv"),
              ["posting_ref", "facility_no", "posting_date", "amount_eur", "posting_type", "sale_ref"], out)
    return len(rows), len(out)


def write_index(P, target):
    w = P.w
    rows = []
    for (s, r) in sorted(w.rel):
        code = "BRCPI-%s-%s" % (SERIES[s], REG[r])
        for k, n, d, x in sorted(w.rel[(s, r)]):
            rows.append([code, s, r, "%dQ%d" % W.QUARTERS[k], n + 1, ymd(d), "%.2f" % x])
    write_csv(os.path.join(target, "brackley_rowe_cre_index_2004_2026.csv"),
              ["series_code", "sector", "region_group", "quarter", "release", "release_date", "index_value"], rows)
    return len(rows)


# ------------------------------------------------------------------ files a planner would weigh and the call never reads

TENANTS = ["Gala Retail", "Brightwater Pharmacy", "Ardmore Insurance Brokers", "Kestrel Logistics", "Fernhill Dental",
           "Corbally Engineering", "Quayside Opticians", "Riverview Physiotherapy", "Shanbally Foods", "Tulla Print",
           "Moycullen Joinery", "Carrigaline Motors", "Bawn Accountancy", "Lisheen Coffee", "Owenmore IT Services",
           "Glenmore Couriers", "Inchicore Fitness", "Sallins Hardware", "Mallow Bakery", "Clonard Solicitors"]


def write_rent_roll(P, target):
    w, rng = P.w, P.rng
    rows = []
    for fi in sorted(w.alive_end, key=lambda fi: P.current_no[fi]):
        p = w.facs[fi]["props"][0]
        if BOOK[w.props[p]["sector"]] != "Investment" or rng.random() < 0.12:
            continue
        for u in range(int(rng.integers(1, 4))):
            start = dt.date(int(rng.integers(2014, 2026)), int(rng.integers(1, 13)), 1)
            exp = start.replace(year=start.year + int(rng.choice([5, 10, 15, 20])))
            rent = round(float(rng.uniform(14, 260)) * 1000, -2)
            rows.append([P.pid[p], "Unit %d" % (u + 1), str(rng.choice(TENANTS)) + " Ltd", ymd(start), ymd(exp),
                         "%d" % rent, ymd(start.replace(year=start.year + 5)) if exp.year - start.year > 5 else ""])
    write_csv(os.path.join(target, "rent_roll_2026-12.csv"),
              ["property_id", "unit", "tenant", "lease_start", "lease_expiry", "passing_rent_eur", "next_rent_review"], rows)
    return len(rows)


def write_insurance(P, target):
    w, rng = P.w, P.rng
    wb = wb_new("Ardcarn Bank Security Team")
    ws = wb.active
    ws.title = "Buildings cover"
    rows = []
    rate = {"Retail": 1450, "Office": 1900, "Industrial": 950, "Hospitality": 2300, "Healthcare": 2500}
    for fi in sorted(w.alive_end, key=lambda fi: P.current_no[fi]):
        for p in w.facs[fi]["props"]:
            area = int(rng.integers(150, 5000))
            si = round(area * rate[w.props[p]["sector"]] * float(rng.uniform(0.85, 1.2)), -3)
            rows.append([P.pid[p], str(rng.choice(["Liffey Mutual Insurance", "Shannon General", "Eastlink Assurance"])),
                         "BC-%07d" % int(rng.integers(1000000, 9999999)), int(si),
                         dt.date(2026 + (rng.random() < 0.7), int(rng.integers(1, 13)), 1)])
    rows = sorted({r[0]: r for r in rows}.values())
    sheet(ws, ["property_id", "insurer", "policy_no", "sum_insured_eur", "renewal_date"], rows, [12, 26, 12, 16, 13],
          datecols=(4,), money=(3,))
    path = os.path.join(target, "buildings_insurance_register_2026.xlsx")
    wb.save(path)
    postprocess.scrub(path, "Ardcarn Bank Security Team", "2026-12-18")
    postprocess.finish_office(path, "2021-02-11T10:02:00Z", "2026-12-18T16:21:00Z", "Ardcarn Bank")
    return len(rows)


def write_all(w, target):
    P = assemble(w)
    counts = {}
    counts["dw_fact_loan_month_end_2022_2026.csv"] = write_snapshot(P, target)
    counts["dw_dim_property_valuation_2004_2026.csv"] = write_valuations(P, target)
    counts["dw_dim_property_2026-12.csv"] = write_property_dim(P, target)
    counts["dw_bridge_facility_security_2026-12.csv"] = write_bridge(P, target)
    counts["facility_register_2026-12.xlsx"] = write_facility_register(P, target)
    counts["default_register_2012_2026.csv"] = write_defaults(P, target)
    counts["receiver_sales_2012_2026.csv"], counts["recovery_postings_2012_2027.csv"] = write_sales(P, target)
    counts["brackley_rowe_cre_index_2004_2026.csv"] = write_index(P, target)
    counts["rent_roll_2026-12.csv"] = write_rent_roll(P, target)
    counts["buildings_insurance_register_2026.xlsx"] = write_insurance(P, target)
    return P, counts
