"""The files Fjordkob's systems export, written from the world's run of the trade as it happened.

The ERP's daily store and item extract changed layout with the ERP upgrade on 1 January 2026 (the 2025 file is the
old export: semicolons, decimal commas, Danish headers, Windows-1252); its export job re-sent a few store-days; a
store that scans its write-offs the next morning books them on the next day. Business intelligence's weekly history
renamed its category codes at the 2026 range review. Kornblomst logs every order proposal with both forecasts from
the start of the pilot (its own forecast for every store, used only in the pilot stores)."""
import csv
import datetime as dt
import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import world as W

F_D25 = "dagssalg_frisk_2025.csv"
F_D26 = "dagssalg_frisk_2026.csv"
F_FC = "ordreforslag_2026.csv"
F_BI = "bi_uge_butik_kategori.csv"
F_PROF = "timeprofil_salg_frisk.csv"
F_ITEMS = "vareregister_frisk.xlsx"
F_STORES = "butiksregister.xlsx"
F_PROMO = "kampagneplan_2025_2026.xlsx"
F_COMP = "konkurrentaabninger.csv"
F_PILOT = "pilotaftale_kornblomst_2026.pdf"
F_DASH = "pilot_dashboard_uge35.xlsx"
F_WEATHER = "vejr_dmi_2025_2026.csv"
F_STAFF = "personaletimer_frisk_2026.csv"
DISTRACTORS = [F_WEATHER, F_STAFF]
ORG = "Fjordkøb A/S"
UTC = dt.timezone.utc
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))

# item numbers as Fjordkob's ERP issues them; two dairy items were renumbered when the supplier changed on 1 January
ITEM_NO = [412037, 412041, 412066, 412078, 412103, 412119, 412154, 412161, 433208, 433215, 433241, 433262, 433277,
           433290, 451306, 451321, 451348, 451355, 451382, 451397, 451414, 451429, 467503, 467518, 467542, 467559,
           489612, 489634, 489657, 489671, 489693, 489708]
RENUMBERED = {16: 451819, 17: 451826}       # item index: number from 2026 (letmælk, letmælk økologisk)
CAT_CODE_OLD = ["BAG", "FOG", "MEJ", "KOD", "FAE"]
CAT_CODE_NEW = ["Bageri", "Frugt & grønt", "Mejeri", "Kød", "Færdigretter"]
SUPPLIER = ["Kornets Bageri", "Kornets Bageri", "Kornets Bageri", "Kornets Bageri", "Kornets Bageri",
            "Kornets Bageri", "Mester Hansens Konditori", "Mester Hansens Konditori", "Grøn Gård Salater",
            "Grøn Gård Salater", "Frugtkompagniet", "Frugtkompagniet", "Frugtkompagniet", "Frugtkompagniet",
            "Thise Mejeri", "Thise Mejeri", "Arla Foods", "Arla Foods", "Arla Foods", "Arla Foods", "Arla Foods",
            "Arla Foods", "Danish Crown", "Danish Crown", "Danpo", "Danpo", "Køkkenet Skejby", "Køkkenet Skejby",
            "Køkkenet Skejby", "Køkkenet Skejby", "Køkkenet Skejby", "Køkkenet Skejby"]
ADDRESS = {
    2104: ("Skanderborgvej 190", "8260"), 2117: ("Udbyhøjvej 140", "8930"), 2131: ("Vestergade 52", "8700"),
    2146: ("Århusvej 88", "8600"), 2158: ("Vestre Engvej 47", "7100"), 2163: ("Adelgade 61", "8660"),
    2179: ("Vestre Strandallé 14", "8240"), 2185: ("Østergade 30", "8500"), 3012: ("Tordenskjoldsgade 21", "8200"),
    3027: ("Jægergårdsgade 108", "8000"), 3031: ("Randersvej 162", "8200"), 3048: ("Holme Byvej 9", "8270"),
    3055: ("Brabrand Byvej 4", "8220"), 3069: ("Hasle Ringvej 133", "8210"), 3072: ("Rosensgade 19", "8300"),
    3086: ("Østergade 5", "8382"), 3093: ("Søndergade 18", "8370"), 3101: ("Klostervej 2", "8680"),
    3114: ("Mølletoften 11", "8464"), 3128: ("Middelgade 4", "8900"), 3136: ("Dæmningen 34", "7100"),
    3142: ("Strandpromenaden 8", "8700"), 3157: ("Banegårdspladsen 3", "8000"), 3165: ("Brendstrupgårdsvej 5", "8200"),
    3170: ("Drewsensvej 1", "8600"), 3189: ("Finlandsgade 22", "8200"), 4203: ("Banegårdspladsen 2", "8000"),
    4218: ("Jernbanevej 1", "8660"), 4224: ("Banegårdspladsen 7", "8700"), 4237: ("Banegårdspladsen 1", "7100"),
    4241: ("Jernbanegade 4", "8900"), 4256: ("Drewsensvej 1B", "8600"), 4262: ("Nordre Ringgade 1", "8000"),
    4279: ("Inge Lehmanns Gade 10", "8000"), 4285: ("Bernhardt Jensens Boulevard 7", "8000"),
    4290: ("Palle Juul-Jensens Boulevard 99", "8200"), 4307: ("Havneøen 6", "7100"), 4313: ("Åbogade 15", "8200"),
    4326: ("Søndergade 31", "8000"), 4331: ("Søndergade 17", "7100"), 4345: ("Søndergade 46", "8700"),
    4352: ("Brødregade 12", "8900"),
}
AREA = {"Super": (1800, 2600), "Kvarter": (550, 900), "To Go": (95, 190)}
OPENED = [1998, 2003, 2011, 2007, 2015, 1994, 2019, 2001, 1989, 1992, 2005, 2009, 2012, 1997, 2004, 2008, 2014, 2000,
          2016, 2010, 2006, 2013, 2018, 2020, 2017, 2021, 2014, 2016, 2018, 2015, 2019, 2017, 2020, 2022, 2021, 2019,
          2023, 2022, 2016, 2018, 2021, 2023]


def item_no(i, d):
    return RENUMBERED.get(i, ITEM_NO[i]) if d >= dt.date(2026, 1, 1) else ITEM_NO[i]


def price_on(i, s, k, w):
    """The shelf price a sale went through at: the year's list price, the leaflet price in a promotion week, the
    To Go premium on top."""
    base = W.PRICE[i] * (1.025 if W.DAYS[k].year == 2026 else 1.0)
    if w.promo[k, i]:
        base = base * (1 - w.promo_disc[i])
    return round(base * W.PREMIUM[s] / 0.05) * 0.05


def cost_on(i, k):
    return round(W.COST[i] * (1.025 if W.DAYS[k].year == 2026 else 1.0), 2)


def dk(x, nd=2):
    return ("%." + str(nd) + "f") % x


def dkc(x, nd=2):
    return dk(x, nd).replace(".", ",")


def hhmm(t, secs=False, rng=None):
    if t != t:
        return ""
    t = min(max(t, 0.0), 23.99)
    h = int(t)
    m = int((t - h) * 60)
    if secs:
        sec = int(((t - h) * 60 - m) * 60)
        return "%02d:%02d:%02d" % (h, m, sec)
    return "%02d:%02d" % (h, m)


class Records:
    """The run as the systems recorded it, with the recording conventions applied."""

    def __init__(self, w, run):
        self.w = w
        self.r = run
        rng = np.random.default_rng(w.seed + 101)
        nd, ns, ni = W.ND, W.NS, W.NI
        waste = run["waste"].copy()
        stock = run["close_stock"].copy()
        # a store that scans its write-offs the next morning books them on the next day
        late = rng.random((nd, ns)) < 0.03
        late[-1] = False
        wrec = waste.copy()
        srec = stock.copy()
        for k in range(nd - 1):
            for s in np.where(late[k])[0]:
                wrec[k + 1, s] += waste[k, s]
                wrec[k, s] = 0.0
                srec[k, s] += waste[k, s]
        self.late = late
        self.waste_rec = wrec
        self.stock_rec = srec
        # re-sent store-days in the old export
        self.resent = [(k, s) for k in range(nd) for s in range(ns)
                       if W.DAYS[k].year == 2025 and W.EXPORT[k] and rng.random() < 0.0025]
        self.rng = rng
        # shelf price and cost of every sale, day x store x item
        yr = np.array([1.025 if d.year == 2026 else 1.0 for d in W.DAYS])
        base = W.PRICE[None, None, :] * yr[:, None, None] * np.where(w.promo[:, None, :], 1 - w.promo_disc[None, None, :], 1.0)
        self.price = np.round(base * W.PREMIUM[None, :, None] / 0.05) * 0.05
        self.cost = np.round(W.COST[None, :] * yr[:, None], 2)
        self.sales_val = run["sold"] * self.price
        self.waste_val = self.waste_rec * self.cost[:, None, :]


def write_daily(target, R):
    w, r = R.w, R.r
    # 2025: the old export
    rows25 = []
    hdr25 = ["Dato", "Butik", "Varenr", "Solgt antal", "Omsætning ekskl. moms kr", "Sidste salg", "Modtaget antal", "Svind antal",
             "Lager ved lukning"]
    resent = {}
    for k, s in R.resent:
        resent.setdefault((W.DAYS[k].year, W.DAYS[k].month), []).append((k, s))
    lines = [";".join(hdr25)]
    cur_month = None
    for k, d in enumerate(W.DAYS):
        if d.year != 2025 or not W.EXPORT[k]:
            continue
        if cur_month is not None and (d.year, d.month) != cur_month:
            for kk, ss in resent.get(cur_month, []):
                lines.extend(_rows25(R, kk, ss))
        cur_month = (d.year, d.month)
        for s in range(W.NS):
            lines.extend(_rows25(R, k, s))
    for kk, ss in resent.get(cur_month, []):
        lines.extend(_rows25(R, kk, ss))
    with open(os.path.join(target, F_D25), "wb") as f:
        f.write(("\r\n".join(lines) + "\r\n").encode("cp1252"))
    # 2026: the new export
    out = io.StringIO()
    wr = csv.writer(out, lineterminator="\n")
    wr.writerow(["date", "store", "item_no", "units_sold", "sales_excl_vat_dkk", "last_sale", "units_received",
                 "units_written_off", "closing_stock"])
    for k, d in enumerate(W.DAYS):
        if d.year != 2026:
            continue
        for s in range(W.NS):
            for i in range(W.NI):
                if not W.RANGED[s, i]:
                    continue
                u = int(r["sold"][k, s, i])
                wr.writerow([d.isoformat(), int(W.SNO[s]), item_no(i, d), u, dk(R.sales_val[k, s, i]),
                             hhmm(r["t_last"][k, s, i], secs=True) if u > 0 else "", int(r["deliv"][k, s, i]),
                             int(R.waste_rec[k, s, i]), int(R.stock_rec[k, s, i])])
    open(os.path.join(target, F_D26), "w", encoding="utf-8").write(out.getvalue())


def _rows25(R, k, s):
    w, r = R.w, R.r
    d = W.DAYS[k]
    out = []
    for i in range(W.NI):
        if not W.RANGED[s, i]:
            continue
        u = int(r["sold"][k, s, i])
        out.append(";".join([d.strftime("%d-%m-%Y"), str(int(W.SNO[s])), str(item_no(i, d)), str(u),
                             dkc(R.sales_val[k, s, i]), hhmm(r["t_last"][k, s, i]) if u > 0 else "",
                             str(int(r["deliv"][k, s, i])), str(int(R.waste_rec[k, s, i])),
                             str(int(R.stock_rec[k, s, i]))]))
    return out


def write_forecasts(target, R):
    r = R.r
    out = io.StringIO()
    wr = csv.writer(out, lineterminator="\n")
    wr.writerow(["delivery_date", "store", "item_no", "autoordre_forecast", "kornblomst_forecast", "safety_stock",
                 "order_units", "order_basis"])
    for k, d in enumerate(W.DAYS):
        if d.year != 2026:
            continue
        for s in range(W.NS):
            basis = "Kornblomst" if r["system"][k, s] else "AutoOrdre"
            for i in range(W.NI):
                if not W.RANGED[s, i]:
                    continue
                fn = r["fc_n"][k, s, i]
                wr.writerow([d.isoformat(), int(W.SNO[s]), item_no(i, d), "%.1f" % r["fc_l"][k, s, i],
                             "" if fn != fn else "%.1f" % fn, "%.1f" % r["ss"][k, s, i], int(r["order"][k, s, i]),
                             basis])
    open(os.path.join(target, F_FC), "w", encoding="utf-8").write(out.getvalue())


def iso_weeks():
    seen = []
    for d in W.DAYS:
        if d < W.D0:
            continue
        y, wk, _ = d.isocalendar()
        if (y, wk) not in seen:
            seen.append((y, wk))
    return seen


def write_bi(target, R):
    """Weekly history from the BI cube: fresh categories from the deduplicated daily extract (waste by scan date,
    at that year's cost price), and the ambient trade."""
    w, r = R.w, R.r
    weeks = iso_weeks()
    ex = np.where(W.EXPORT)[0]
    wk_of = np.array([weeks.index((W.YEAR[k], W.WEEK[k])) for k in ex])
    nw = len(weeks)
    sv = np.zeros((nw, W.NS, W.NC)); wv = np.zeros((nw, W.NS, W.NC)); un = np.zeros((nw, W.NS, W.NC))
    for c in range(W.NC):
        ii = W.CAT_IDX[c]
        np.add.at(sv[:, :, c], wk_of, R.sales_val[ex][:, :, ii].sum(axis=2))
        np.add.at(wv[:, :, c], wk_of, R.waste_val[ex][:, :, ii].sum(axis=2))
        np.add.at(un[:, :, c], wk_of, r["sold"][ex][:, :, ii].sum(axis=2))
    lines = ["aar_uge;butik;kategori;omsaetning_ekskl_moms_kr;svind_kostpris_kr;solgt_antal"]
    for wi, (y, wk) in enumerate(weeks):
        new = (y, wk) >= (2026, 2)
        for s in range(W.NS):
            for c in range(W.NC):
                code = CAT_CODE_NEW[c] if new else CAT_CODE_OLD[c]
                lines.append(";".join(["%d-W%02d" % (y, wk), str(int(W.SNO[s])), code, dkc(sv[wi, s, c]),
                                       dkc(wv[wi, s, c]), str(int(un[wi, s, c]))]))
            amb = w.ambient_week[wi + W.WEEK_OFFSET, s]
            lines.append(";".join(["%d-W%02d" % (y, wk), str(int(W.SNO[s])), "Kolonial" if new else "KOL", dkc(amb),
                                   dkc(amb * 0.0042 * (1 + 0.15 * R.rng.normal())), str(int(amb / 21.3))]))
    with open(os.path.join(target, F_BI), "wb") as f:
        f.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))


def write_profile(target, w):
    lines = ["format;kategori;ugedag;time;andel_af_dagens_salg"]
    days = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
    for f, cat, dw, h, share in w.profile_table():
        lines.append(";".join([f, cat, days[dw], "%02d-%02d" % (h, h + 1), dkc(share, 4)]))
    with open(os.path.join(target, F_PROF), "wb") as fh:
        fh.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))


def write_competitors(target):
    rows = [
        ("14-03-2024", "Netto", "Ringvej Syd 104, 8260 Viby J", 2104, "1,9", "åbnet"),
        ("02-09-2024", "Lidl", "Silkeborgvej 450, 8220 Brabrand", 3055, "1,2", "åbnet"),
        ("12-05-2025", "Lidl", "Skovvej 2, 8464 Galten", 3114, "0,8", "åbnet"),
        ("12-05-2025", "Lidl", "Skovvej 2, 8464 Galten", 2146, "2,6", "åbnet, nærmeste Fjordkøb er Galten"),
        ("30-06-2025", "Rema 1000", "Nørregade 12, 8900 Randers C", 3128, "3,4", "lukket"),
        ("13-04-2026", "Netto", "Randersvej 140, 8200 Aarhus N", 3031, "0,9", "åbnet"),
        ("13-04-2026", "Netto", "Randersvej 140, 8200 Aarhus N", 3012, "1,7", "åbnet"),
        ("08-06-2026", "Lidl", "Fabriksvej 3, 8700 Horsens", 2131, "0,7", "åbnet"),
        ("08-06-2026", "Lidl", "Fabriksvej 3, 8700 Horsens", 4224, "1,3", "åbnet"),
        ("24-08-2026", "Netto", "Vestergade 9, 7100 Vejle", 3136, "0,6", "åbner 2. november 2026 (byggetilladelse)"),
    ]
    lines = ["dato;kaede;adresse;naermeste_butik;afstand_km;bemaerkning"]
    for r in rows:
        lines.append(";".join([r[0], r[1], r[2], str(r[3]), r[4], r[5]]))
    with open(os.path.join(target, F_COMP), "wb") as f:
        f.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))


def write_weather(target, w):
    towns = sorted(set(W.TOWN))
    rng = np.random.default_rng(w.seed + 303)
    lines = ["Dato;By;Maks. temperatur (°C);Nedbør (mm);Solskin (timer)"]
    for k, d in enumerate(W.DAYS):
        doy = d.timetuple().tm_yday
        for t in towns:
            base = 11.5 - 9.5 * np.cos(2 * np.pi * (doy - 20) / 365.25)
            temp = base + rng.normal(0, 3.0)
            rain = max(0.0, rng.gamma(0.6, 3.2) - 0.8) if rng.random() < 0.48 else 0.0
            sun = max(0.0, min(16.5, (7.5 - 5.5 * np.cos(2 * np.pi * (doy - 10) / 365.25)) * rng.uniform(0.1, 1.2)))
            lines.append(";".join([d.strftime("%d-%m-%Y"), t, dkc(temp, 1), dkc(rain, 1), dkc(sun, 1)]))
    with open(os.path.join(target, F_WEATHER), "wb") as fh:
        fh.write(("\r\n".join(lines) + "\r\n").encode("utf-8"))


def write_staff(target, w):
    rng = np.random.default_rng(w.seed + 404)
    lines = ["store,iso_week,fresh_dept_hours,of_which_ordering_hours"]
    for y, wk in iso_weeks():
        if y != 2026:
            continue
        for s in range(W.NS):
            hrs = {"Super": 410, "Kvarter": 165, "To Go": 62}[W.FMT[s]] * (W.SIZE[s] / {"Super": 2.4, "Kvarter": 1.0, "To Go": 0.4}[W.FMT[s]]) ** 0.6
            hrs *= rng.uniform(0.9, 1.1)
            order = hrs * rng.uniform(0.045, 0.07) * (0.8 if (W.ISPILOT[s] and wk >= 10) else 1.0)
            lines.append(",".join([str(int(W.SNO[s])), "%d-W%02d" % (y, wk), "%.1f" % hrs, "%.1f" % order]))
    open(os.path.join(target, F_STAFF), "w", encoding="utf-8").write("\n".join(lines) + "\n")


def _style_header(ws, row=1):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_items(target, stamp):
    wb = Workbook()
    ws = wb.active
    ws.title = "Varer"
    ws.append(["Varenr", "Varenavn", "Kategori", "Underkategori", "Holdbarhed (dage)", "Kolli (stk)",
               "Kolli To Go (stk)", "Salgspris ekskl. moms 2025 kr", "Kostpris 2025 kr", "Salgspris ekskl. moms 2026 kr",
               "Kostpris 2026 kr",
               "Leverandør", "Tidligere varenr"])
    _style_header(ws)
    for i, it in enumerate(W.ITEMS):
        no26 = RENUMBERED.get(i, ITEM_NO[i])
        ws.append([no26, it[0], CAT_CODE_NEW[W.ICAT[i]], W.SUBCAT[i], int(W.LIFE[i]), int(W.PACK[i]),
                   int(max(1, W.PACK[i] // 3)) if W.RANGED[W.FMT == "To Go"][:, i].any() else None,
                   round(W.PRICE[i], 2), round(W.COST[i], 2),
                   round(W.PRICE[i] * 1.025, 2), round(W.COST[i] * 1.025, 2), SUPPLIER[i],
                   ITEM_NO[i] if i in RENUMBERED else None])
    for col, wd in zip("ABCDEFGHIJKLM", [9, 34, 14, 14, 10, 8, 10, 11, 11, 11, 11, 24, 12]):
        ws.column_dimensions[col].width = wd
    p = os.path.join(target, F_ITEMS)
    wb.save(p)
    PP.normalize_ooxml(p, "Mette Kjær", "Mette Kjær", stamp[0], stamp[1], excel=True, company=ORG)


def write_stores(target, w, stamp):
    rng = np.random.default_rng(w.seed + 505)
    wb = Workbook()
    ws = wb.active
    ws.title = "Butikker"
    ws.append(["Butiksnr", "Navn", "Format", "Adresse", "Postnr", "By", "Åbningstid", "Salgsareal m2", "Åbnet"])
    _style_header(ws)
    for s, st in enumerate(W.STORES):
        lo, hi = AREA[st[2]]
        area = int(lo + (hi - lo) * min(1.0, max(0.0, (st[5] - {"Super": 1.9, "Kvarter": 0.8, "To Go": 0.25}[st[2]]) /
                                                {"Super": 1.1, "Kvarter": 0.55, "To Go": 0.5}[st[2]])) + rng.integers(-40, 40))
        hours = "Alle dage %02d-%02d" % (st[7], st[8]) if st[7] != 8 else "Man-lør 08-21, søn 10-18"
        ad, pc = ADDRESS[st[0]]
        ws.append([st[0], st[1].replace("Fjordkob", "Fjordkøb"), st[2], ad, pc, st[3], hours, area, OPENED[s]])
    for col, wd in zip("ABCDEFGHI", [9, 34, 9, 30, 8, 12, 22, 12, 7]):
        ws.column_dimensions[col].width = wd
    p = os.path.join(target, F_STORES)
    wb.save(p)
    PP.normalize_ooxml(p, "Søren Holm", "Søren Holm", stamp[0], stamp[1], excel=True, company=ORG)


def write_promo(target, w, stamp):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tilbudsavis"
    ws.append(["Uge", "Varenr", "Varenavn", "Normalpris ekskl. moms kr", "Tilbudspris ekskl. moms kr", "Side i avisen"])
    _style_header(ws)
    rng = np.random.default_rng(w.seed + 606)
    for wi, (y, wk) in enumerate(iso_weeks()):
        k = (wi + W.WEEK_OFFSET) * 7
        d = W.DAYS[k]
        for i in np.where(w.promo_week[wi + W.WEEK_OFFSET])[0]:
            normal = W.PRICE[i] * (1.025 if y == 2026 else 1.0)
            ws.append(["%d-%02d" % (y, wk), item_no(i, d), W.ITEMS[i][0], round(normal, 2),
                       round(round(normal * (1 - w.promo_disc[i]) / 0.05) * 0.05, 2), int(rng.integers(2, 13))])
    for col, wd in zip("ABCDEF", [9, 9, 34, 12, 12, 10]):
        ws.column_dimensions[col].width = wd
    p = os.path.join(target, F_PROMO)
    wb.save(p)
    PP.normalize_ooxml(p, "Line Mortensen", "Line Mortensen", stamp[0], stamp[1], excel=True, company=ORG)


def week_rows(R):
    """The dashboard's weekly series, pilot stores against the rest, from the deduplicated daily extract."""
    out = []
    for (y, wk) in iso_weeks():
        if not (10 <= wk <= 35):
            continue
        ks = np.array([k for k in range(W.ND) if (W.YEAR[k], W.WEEK[k]) == (y, wk)])
        for grp, mask in [("Pilot stores", W.ISPILOT), ("Other stores", ~W.ISPILOT)]:
            sv = R.sales_val[ks][:, mask].sum()
            wv = R.waste_val[ks][:, mask].sum()
            avail = float((R.stock_rec[ks][:, mask] > 0).mean())
            out.append((y, wk, grp, sv, wv, avail))
    return out


# each file's own save, in the fiction's calendar (created, modified); every stamp distinct
STAMPS = {
    F_ITEMS: ("2026-01-05T08:14:00Z", "2026-08-31T13:42:00Z"),
    F_STORES: ("2024-02-12T09:30:00Z", "2026-06-22T10:05:00Z"),
    F_PROMO: ("2025-02-17T12:01:00Z", "2026-08-21T14:37:00Z"),
    F_DASH: ("2026-03-09T07:55:00Z", "2026-09-07T06:48:00Z"),
}
