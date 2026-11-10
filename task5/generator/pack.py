"""task5 architecture 4: the Division's extract, as its systems write it.

The quarterly reports (originals, amendments, the odd resubmission), the employer account register, its status
history, the multiple worksite reports, the county codes and the NAICS concordance, cut from the world in sim.py and
held as tables; write_* put them on disk the way each source exports them."""
import csv
import datetime as dt
import io

import numpy as np
import pandas as pd

import sim
import world as W

SURNAMES = ("Abernathy Ackley Alder Ambrose Aldana Archer Arnett Ashworth Babcock Bainbridge Barlow Beasley Bertrand "
            "Bixby Blackwell Bonner Boyce Bramlett Brennan Briggs Brock Burnham Calloway Carver Castellano Chadwick "
            "Chamberlain Cheney Childers Cobb Colfax Conover Corbin Cormier Crandall Crowell Cutler Dalton Danforth "
            "Darrow DeLuca Dempsey Devlin Dorsey Draper Dunbar Duquette Easton Eckert Ellery Emmons Ewing Fairbanks "
            "Farnham Faulkner Fennell Finley Fitch Fogarty Forsythe Fuentes Gaffney Galloway Garrison Geller Gilchrist "
            "Goddard Gorski Granger Greer Gunderson Haddock Hagen Halvorsen Hammond Harlan Haskell Hatcher Hayward "
            "Hedlund Hendrix Herrera Hollis Holmquist Horne Huckabee Ingersoll Iverson Jarvis Jessup Kavanagh Keane "
            "Kemper Kessler Kincaid Kirkland Kowalski Lachance Landry Langley Larkin Ledbetter Lindqvist Lockhart "
            "Lombardi Lowry Macklin Madsen Marchetti Markham Mattingly McAllister McCready Mercer Merriweather Moody "
            "Mulvaney Nadeau Nolan Novak Oakes Oberlin Ostrander Pacheco Pardee Pelletier Pettibone Platt Prescott "
            "Pruitt Quimby Radcliffe Ransom Reardon Renfro Riordan Rockwell Rourke Rutledge Salazar Sandoval Sawyer "
            "Schaefer Seaver Sheffield Shipley Sinclair Slocum Sorensen Spalding Stafford Steadman Stoddard Strand "
            "Sutter Swanson Talbot Tatum Thibodeau Tillman Trask Tremblay Underhill Upham Vance Vaughn Voss Wadsworth "
            "Walcott Waverly Webber Wendell Whitaker Wilder Winslow Wolcott Yarbrough Yates Zeller Zimmerman").split()
TOWNS = {
    "001": ["Brayton", "Hollins Ford", "Pike Valley", "Ashgrove"],
    "003": ["Port Calder", "East Calder", "Wexley", "Marlow Heights", "Cedar Bluff"],
    "005": ["Corliss", "Fallowfield", "Dunmore Station"],
    "007": ["Fenwick", "Larch Hill", "Northbrook"],
    "009": ["Garrow Mills", "Kestrel", "Ridley", "Stony Brook Junction"],
    "011": ["Hadleyville", "Glenmere", "Upton Falls"],
    "013": ["Kittredge Harbor", "Loon Point", "Tamarack"],
    "015": ["Linden Crossing", "Oakmont", "Westvale", "Benton"],
    "017": ["Merritt Falls", "Quarry Hill", "Elmwood", "Southport"],
    "019": ["Ostrom Junction", "Pinecrest", "Black Spruce", "Rainier Flats"],
    "021": ["Pellston", "Redfield", "Harrow"],
    "023": ["Talcott Lake", "Juniper Bay", "Winslow"],
    "025": ["Whitcomb", "Millbrook", "Ivy Point", "Danby"],
    "027": ["Sayre", "Yarrow", "North Talcott"],
}
FEATURES = ["Cedar Ridge", "Pine Hollow", "Stonegate", "Riverbend", "Maple Grove", "Lakeside", "Northfield",
            "Highland", "Blue Heron", "Granite Peak", "Willow Creek", "Old Mill", "Birchwood", "Summit", "Harbor View",
            "Twin Oaks", "Elk Run", "Silver Lake", "Fox Hollow", "Ironwood", "Meadowbrook", "Eagle Point"]
IND = {
    "111421": ["Nursery", "Tree Farm", "Greenhouses"], "111998": ["Farms", "Farm", "Acres"], "112111": ["Cattle Co.", "Ranch", "Beef"],
    "112120": ["Dairy", "Dairy Farm", "Farms"], "113310": ["Logging", "Timber", "Forest Products"],
    "115310": ["Forestry Services", "Timber Services", "Forest Management"], "212321": ["Sand & Gravel", "Aggregates"],
    "236115": ["Homes", "Builders", "Home Builders"], "236118": ["Remodeling", "Renovations", "Home Improvement"],
    "236220": ["Construction", "Building Co.", "Contracting"], "237310": ["Paving", "Excavating & Paving", "Road Builders"],
    "238110": ["Concrete", "Foundations", "Concrete Works"], "238160": ["Roofing", "Roofing & Siding"],
    "238210": ["Electric", "Electrical Contractors", "Electric Co."], "238220": ["Plumbing & Heating", "Mechanical", "Heating & Cooling"],
    "238310": ["Drywall", "Insulation", "Drywall & Plaster"], "238320": ["Painting", "Painting Co.", "Decorating"],
    "238910": ["Excavating", "Site Work", "Earthworks"], "238990": ["Contracting", "Fence Co.", "Specialty Builders"],
    "311812": ["Bakery", "Baking Co."], "321113": ["Lumber", "Sawmill", "Wood Products"], "321918": ["Millwork", "Woodworks"],
    "322121": ["Paper Co.", "Paper Mill"], "326199": ["Plastics", "Molding"], "332323": ["Metal Works", "Ironworks"],
    "332710": ["Machine", "Machine Shop", "Precision"], "336390": ["Automotive Components", "Auto Parts Mfg"],
    "337110": ["Cabinetry", "Kitchens", "Cabinet Co."], "221122": ["Electric Cooperative", "Power & Light"],
    "423310": ["Building Supply", "Lumber Supply"], "423810": ["Equipment", "Equipment Sales"], "424410": ["Food Distributors", "Grocery Supply"],
    "441110": ["Motors", "Ford", "Chevrolet", "Auto Sales"], "444110": ["Home Center"], "444180": ["Building Supply", "Hardware"],
    "445110": ["Market", "Foods", "Grocery"], "445131": ["Quick Stop", "Mini Mart", "Convenience"], "455211": ["Wholesale Club"],
    "456110": ["Pharmacy", "Drug", "Apothecary"], "457110": ["Fuel & Food", "Gas & Go", "Petroleum"], "458110": ["Outfitters", "Clothing Co."],
    "459110": ["Sporting Goods", "Outdoor Supply"], "459420": ["Gifts", "Gift Shop", "Trading Post"], "459999": ["Supply", "Variety"],
    "484110": ["Trucking", "Freight", "Transport"], "484220": ["Trucking", "Hauling", "Log Hauling"], "488410": ["Towing", "Wrecker Service"],
    "492210": ["Courier", "Delivery"], "493110": ["Warehousing", "Storage"], "513110": ["Gazette", "Herald", "Courier-Journal"],
    "517112": ["Wireless", "Cellular"], "519290": ["Data Services", "Information Services"],
    "522110": ["Savings Bank", "National Bank", "Trust Company"], "522130": ["Federal Credit Union", "Community Credit Union"],
    "524210": ["Insurance Agency", "Insurance Group"], "531110": ["Properties", "Apartments", "Rentals"],
    "531210": ["Realty", "Real Estate", "Realtors"], "531311": ["Property Management", "Management Co."],
    "541110": ["Law Office", "Law Group", "& Associates"], "541211": ["CPAs", "& Company CPAs", "Accounting"],
    "541213": ["Tax Service", "Tax & Bookkeeping"], "541330": ["Engineering", "Engineers"], "541512": ["Technologies", "IT Solutions", "Systems"],
    "541810": ["Advertising", "Creative"], "561320": ["Staffing", "Personnel"], "561720": ["Cleaning", "Janitorial"],
    "561730": ["Landscaping", "Lawn & Garden", "Grounds Care"], "562111": ["Disposal", "Sanitation", "Waste Services"],
    "611110": ["Academy", "School"], "621111": ["Medical Group", "Family Medicine", "Physicians"], "621210": ["Family Dentistry", "Dental Associates", "Dental Care"],
    "621340": ["Physical Therapy", "Rehab"], "621610": ["Home Health", "Home Care"], "622110": ["Medical Center", "Hospital"],
    "623110": ["Health & Rehabilitation", "Nursing Home", "Care Center"], "623312": ["Senior Living", "Assisted Living"],
    "624410": ["Child Care", "Learning Center", "Daycare"], "713930": ["Marina", "Boat Club"], "713940": ["Fitness", "Athletic Club", "Gym"],
    "713990": ["Adventures", "Recreation", "Outfitters"], "721110": ["Inn", "Motel", "Lodge"], "721211": ["Campground", "RV Park"],
    "721214": ["Camp", "Youth Camp"], "722410": ["Tavern", "Pub", "Taproom"], "722511": ["Restaurant", "Grill", "Bistro", "Kitchen"],
    "722513": ["Pizza", "Subs", "Burgers", "Tacos"], "722515": ["Coffee", "Ice Cream", "Bakery & Cafe"],
    "811111": ["Auto Repair", "Garage", "Automotive"], "811121": ["Collision", "Auto Body"], "812111": ["Barber Shop", "Barbers"],
    "812112": ["Salon", "Hair Studio", "Beauty Salon"], "812910": ["Pet Grooming", "Kennels"], "813110": ["Church", "Congregation", "Parish"],
}
PRO_SUFFIX = {"541110": ["PLLC", "LLP", "PC"], "541211": ["PLLC", "LLP", "PC"], "621111": ["PC", "PLLC"],
              "621210": ["PC", "DDS PC", "PLLC"], "541330": ["PLLC", "Inc."], "813110": [""]}
SUFFIX = ["LLC", "LLC", "LLC", "Inc.", "Inc.", "Co.", "Corp.", "Company", ""]


def check_digit(x):
    s = 0
    for k, ch in enumerate(str(x)[::-1]):
        d = int(ch) * (2 if k % 2 == 0 else 1)
        s += d // 10 + d % 10
    return (10 - s % 10) % 10


def account_numbers(w, r):
    """accounts are numbered as they register: initial accounts in order of their liability date, later ones after"""
    order_old = np.argsort(w.liab_date_ord, kind="stable")
    nums = np.zeros(w.n, int)
    x = 1004000 + int(r.integers(0, 900))
    for i in order_old:
        x += int(r.integers(9, 260))
        nums[i] = x
    return nums


def name_for(w, i, r):
    naics, c = w.naics[i], w.county[i]
    town = TOWNS[c][int(r.integers(0, len(TOWNS[c])))]
    cname = W.NAMES[c]
    if w.state[i]:
        return ["Franklin Department of Transportation", "Franklin Department of Corrections",
                "Franklin Department of Health and Human Services", "University of Franklin"][i % 4], ""
    if w.gov[i]:
        if naics == "611110":
            return r.choice(["%s Public Schools", "%s Union School District", "%s Regional School District"]) % town, ""
        if naics == "921140":
            return r.choice(["Town of %s" % town, "City of %s" % town, "%s County" % cname]), ""
        if naics == "922120":
            return "%s Police Department" % town, ""
        if naics == "622110":
            return r.choice(["%s Regional Medical Center" % town, "%s County Hospital" % cname]), ""
        return "%s County" % cname, ""
    words = IND.get(naics, ["Services"])
    iw = words[int(r.integers(0, len(words)))]
    suf = PRO_SUFFIX.get(naics, SUFFIX)
    sx = suf[int(r.integers(0, len(suf)))]
    sn = SURNAMES[int(r.integers(0, len(SURNAMES)))]
    shape = r.random()
    if shape < 0.32:
        nm = "%s %s" % (sn, iw)
    elif shape < 0.48:
        nm = "%s %s" % (town, iw)
    elif shape < 0.58 and naics[:2] in ("23", "11", "48", "81", "33"):
        nm = "%s & Sons %s" % (sn, iw)
    elif shape < 0.66:
        a, b = SURNAMES[int(r.integers(0, len(SURNAMES)))][0], SURNAMES[int(r.integers(0, len(SURNAMES)))][0]
        nm = "%s&%s %s" % (a, b, iw) if r.random() < 0.5 else "%s.%s. %s" % (a, b, iw)
    elif shape < 0.84:
        nm = "%s %s" % (FEATURES[int(r.integers(0, len(FEATURES)))], iw)
    elif shape < 0.92 and naics in ("541110", "541211", "531210", "524210"):
        nm = "%s %s %s" % (sn, SURNAMES[int(r.integers(0, len(SURNAMES)))], iw)
    else:
        nm = "%s %s" % (sn, iw)
    if iw.startswith("&"):
        nm = "%s %s" % (sn, iw)
    legal = (nm + (" " + sx if sx else "")).replace("  ", " ")
    trade = ""
    if r.random() < 0.28 and naics[:2] in ("72", "44", "45", "81", "71"):
        trade = "The %s %s" % (FEATURES[int(r.integers(0, len(FEATURES)))].split()[0], iw)
    return legal, trade



# ------------------------------------------------------------------------------------------------------ tables
def _version_rows(w):
    """every report version of a registered account received by the extract: the original (carrying a month in error
    where it was later amended), the amendment, and a resubmission seconds after the original"""
    rows = []
    for (i, q), t in w.recv.items():
        if t > W.EXTRACT or not w.registered[i]:
            continue
        m = w.jobs[i, 3 * q:3 * q + 3].astype(int).tolist()
        orig = list(m)
        a = w.amend.get((i, q))
        if a is not None:
            k, d = a[1], a[2]
            orig[k] = max(0, orig[k] - d)
        rows.append((i, q, "ORIGINAL", orig, t))
        if (i, q) in w.dup and w.dup[i, q] <= W.EXTRACT:
            rows.append((i, q, "ORIGINAL", orig, w.dup[i, q]))
        if a is not None and a[0] <= W.EXTRACT:
            rows.append((i, q, "AMENDED", m, a[0]))
    return rows


def tables(w):
    r = np.random.default_rng([w.seed, 31])
    rn = sim.rng("names", w.seed)
    n = w.n
    # liability dates: initial accounts registered between 1972 and 2022, the rest on their liability day
    liab, estab = [], []
    setup_lag = r.integers(4, 46, n)
    for i in range(n):
        if w.start_m[i] == 0 and not w.birth[i] and w.pred[i] < 0:
            y = int(r.integers(1972, 2023))
            d = dt.date(y, int(r.integers(1, 13)), int(r.integers(1, 29)))
            e = d + dt.timedelta(days=int(setup_lag[i]))
        else:
            d = sim.liab_date(w, i)
            e = w.established[i]
        liab.append(d)
        estab.append(e)
    w.liab_date = liab
    w.estab_date = estab
    w.liab_date_ord = np.array([d.toordinal() for d in liab])
    # accounts are numbered as they are set up
    order = np.argsort(np.array([e.toordinal() for e in estab]), kind="stable")
    nums = np.zeros(n, int)
    x = 1004000 + int(r.integers(0, 900))
    for i in order:
        x += int(r.integers(9, 260))
        if 5550100 <= x <= 5550199:           # the block the telephone companies keep for fiction
            x = 5550200 + int(r.integers(9, 260))
        nums[i] = x
    w.acct = nums
    fmt = lambda x: "%07d-%d" % (x, check_digit(x))
    w.acct_s = [fmt(x) for x in nums]
    names = [name_for(w, i, rn) for i in range(n)]
    old = {a[0]: a[4] for a in W.NAICS if a[4]}
    naics_reg = []
    for i in range(n):
        c = w.naics[i]
        if c in old and liab[i] < dt.date(2022, 6, 1) and r.random() < 0.78:
            naics_reg.append(old[c])
        else:
            naics_reg.append(c)
    status, sdate = ["ACTIVE"] * n, [""] * n
    ev = sorted([e for e in w.events if e[3] <= W.EXTRACT.date() and w.registered[e[0]]], key=lambda e: (e[3], e[0]))
    for e in ev:
        i, kind = e[0], e[1]
        if kind in ("INACTIVATED", "CLOSED", "TRANSFERRED"):
            status[i], sdate[i] = "INACTIVE", e[2].isoformat()
    acc = pd.DataFrame({
        "_n": nums,
        "_i": np.arange(n),
        "account_no": w.acct_s,
        "legal_name": [nm[0] for nm in names],
        "trade_name": [nm[1] for nm in names],
        "ownership": ["2" if w.state[i] else ("3" if w.gov[i] else "5") for i in range(n)],
        "naics_code": naics_reg,
        "county_code": [w.county[i] for i in range(n)],
        "liability_date": [d.strftime("%m/%d/%Y") for d in liab],
        "account_established": [e.strftime("%m/%d/%Y") for e in estab],
        "account_status": status,
        "status_effective_date": sdate,
        "multi_worksite": ["Y" if i in w.sites else "N" for i in range(n)],
        "predecessor_account": [w.acct_s[w.pred[i]] if w.pred[i] >= 0 else "" for i in range(n)],
    })
    acc = acc[w.registered].sort_values("_n", kind="stable").reset_index(drop=True)
    st = []
    for e in ev:
        i, kind, eff, proc, reason, other = e
        if kind == "TRANSFERRED":
            reason = "SUCCESSOR %s" % w.acct_s[other]
        elif kind == "LIABLE" and other is not None:
            reason = "SUCCESSOR TO %s" % w.acct_s[other]
        st.append((w.acct_s[i], kind, eff.isoformat(), proc.isoformat(), reason))
    stat = pd.DataFrame(st, columns=["account_no", "change_type", "effective_date", "processed_date", "reason"])
    # the reports
    vr = _version_rows(w)
    mw2 = {"11": 3400, "21": 5800, "22": 8200, "23": 5600, "31": 4300, "32": 5200, "33": 5600, "42": 6000, "44": 2900,
           "45": 2700, "48": 4600, "49": 4100, "51": 7400, "52": 7800, "53": 4300, "54": 7900, "56": 3500, "61": 4400,
           "62": 4700, "71": 2500, "72": 1950, "81": 3200, "92": 5100}
    wage = {c: mw2.get(c[:2], 4000) for c in set(w.naics)}
    rw = np.random.default_rng([w.seed, 32]).uniform(0.82, 1.18, (w.n, W.NQ))    # one pay level per account and quarter
    rep = []
    for (i, q, kind, m, t) in vr:
        mw = wage.get(w.naics[i], 4200) * (1 + 0.06 * ((q // 4) - 1))
        tw = sum(m) * mw * rw[i, q]
        tax = min(tw, sum(m) / 3.0 * (14000 if q % 4 == 0 else (9000 if q % 4 == 1 else (3000 if q % 4 == 2 else 900))))
        rep.append((w.acct_s[i], 2023 + q // 4, q % 4 + 1, kind, m[0], m[1], m[2], "%.2f" % tw, "%.2f" % max(0, tax),
                    t.strftime("%Y-%m-%d %H:%M:%S"), i, q))
    reps = pd.DataFrame(rep, columns=["account_no", "year", "quarter", "report_type", "month1_employment",
                                      "month2_employment", "month3_employment", "total_wages", "taxable_wages",
                                      "received_at", "_i", "_q"])
    reps = reps.sort_values(["account_no", "year", "quarter", "received_at"], kind="stable").reset_index(drop=True)
    # multiple worksite reports: one row per worksite, splitting the months of the report it was filed with
    ws = []
    first = {}
    for (i, q, kind, m, t) in vr:
        if i in w.sites and kind == "ORIGINAL" and (i, q) not in first:
            first[i, q] = m
    units = {}
    for (i, q), m in sorted(first.items(), key=lambda kv: (w.acct[kv[0][0]], kv[0][1])):
        md = w.mwr_recv.get((i, q))
        if md is None or md > W.EXTRACT.date():
            continue
        rs = np.random.default_rng([w.seed, 33, int(i), int(q)])
        per_month = [sim.site_weights(w, i, 3 * q + k) for k in range(3)]
        cs = [c for c, _ in per_month[0]]
        split = [[0, 0, 0] for _ in cs]
        for k in range(3):
            sh = np.array([v for _, v in per_month[k]]) * rs.uniform(0.97, 1.03, len(cs))
            part = _whole(int(m[k]), sh)
            for s in range(len(cs)):
                split[s][k] = part[s]
        book = units.setdefault(i, {})
        for s, cc in enumerate(cs):
            if cc not in book:
                book[cc] = len(book) + 1
            town = TOWNS[cc][(int(w.acct[i]) + book[cc]) % len(TOWNS[cc])]
            ws.append(("%07d%d" % (w.acct[i], check_digit(w.acct[i])), "%03d" % book[cc], 2023 + q // 4, q % 4 + 1,
                       "%s COUNTY" % W.NAMES[cc].upper(), town.upper(), w.naics[i],
                       split[s][0], split[s][1], split[s][2], md.strftime("%m/%d/%Y")))
    work = pd.DataFrame(ws, columns=["uiacct", "reporting_unit", "year", "quarter", "worksite_county", "worksite_city",
                                     "naics", "m1_emp", "m2_emp", "m3_emp", "date_received"])
    return {"reports": reps, "accounts": acc, "status": stat, "worksites": work}


def _whole(tot, sh):
    """split a whole number in proportion to shares, whole parts summing to it"""
    sh = np.array(sh, float)
    raw = sh / sh.sum() * tot if sh.sum() else sh
    base = np.floor(raw).astype(int)
    rest = tot - base.sum()
    order = np.argsort(-(raw - base), kind="stable")
    for j in range(rest):
        base[order[j % len(base)]] += 1
    return [int(b) for b in base]


def counties_table():
    seats = {c: TOWNS[c][0] for c in W.CODES}
    return pd.DataFrame([(c[0], c[1] + " County", c[7], seats[c[0]]) for c in W.COUNTIES],
                        columns=["county_code", "county_name", "lmi_region", "county_seat"])


def naics_table():
    rows = []
    for code, title, ss, _, old in W.NAICS:
        rows.append((code, "2022", title, ss, W.SUPERSECTORS[ss][0]))
    seen = {r[0] for r in rows}
    for code, title, ss in W.GOV_NAICS:
        if code not in seen:
            rows.append((code, "2022", title, ss, W.SUPERSECTORS[ss][0]))
            seen.add(code)
    titles2017 = {"444190": "Other Building Material Dealers", "445120": "Convenience Stores",
                  "452311": "Warehouse Clubs and Supercenters", "446110": "Pharmacies and Drug Stores",
                  "447110": "Gasoline Stations with Convenience Stores", "448140": "Family Clothing Stores",
                  "451110": "Sporting Goods Stores", "453220": "Gift, Novelty, and Souvenir Stores",
                  "453998": "All Other Miscellaneous Store Retailers (except Tobacco Stores)",
                  "511110": "Newspaper Publishers", "517312": "Wireless Telecommunications Carriers (except Satellite)",
                  "519130": "Internet Publishing and Broadcasting and Web Search Portals"}
    for code, title, ss, _, old in W.NAICS:
        if old:
            rows.append((old, "2017", titles2017[old], ss, W.SUPERSECTORS[ss][0]))
    for code, title, ss, _, old in W.NAICS:
        if not old:
            rows.append((code, "2017", title.replace("Retailers", "Stores"), ss, W.SUPERSECTORS[ss][0]))
    df = pd.DataFrame(rows, columns=["naics_code", "naics_vintage", "naics_title", "supersector_code", "supersector_title"])
    return df.sort_values(["naics_vintage", "naics_code"], kind="stable").reset_index(drop=True)


def write_csv(df, path, cols=None):
    cols = cols or [c for c in df.columns if not c.startswith("_")]
    buf = io.StringIO()
    df[cols].to_csv(buf, index=False, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return len(df)


# ------------------------------------------------------------------------------------------------------ writers
def write_published(rows, path):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "County"
    ws["A1"] = "Covered Employment and Wages by County, Fourth Quarter 2025"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Franklin Department of Labor, Labor Market Information. Released June 18, 2026."
    ws["A3"] = ("Private and government employers covered by the Unemployment Insurance Law, by worksite county. "
                "Reports posted to employer accounts through May 31, 2026.")
    head = ["County code", "County", "Reporting units", "October 2025 employment", "November 2025 employment",
            "December 2025 employment", "Total quarterly wages ($)", "Average weekly wage ($)"]
    for k, h in enumerate(head):
        cell = ws.cell(row=5, column=k + 1, value=h)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=Side(style="thin"))
    r0 = 6
    for i, row in enumerate(rows):
        for k, v in enumerate(row):
            c = ws.cell(row=r0 + i, column=k + 1, value=v)
            if k >= 2:
                c.number_format = "#,##0"
    tr = r0 + len(rows)
    ws.cell(row=tr, column=2, value="State total").font = Font(bold=True)
    for k in range(2, 7):
        col = openpyxl.utils.get_column_letter(k + 1)
        c = ws.cell(row=tr, column=k + 1, value="=SUM(%s%d:%s%d)" % (col, r0, col, tr - 1))
        c.number_format = "#,##0"
        c.font = Font(bold=True)
    ws.cell(row=tr + 2, column=1, value="Employment is the number of workers on the payroll for the pay period including the 12th of the month.")
    for k, wdt in enumerate([10, 16, 11, 14, 14, 14, 18, 14]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    ws.row_dimensions[5].height = 45
    ws.freeze_panes = "A6"
    wb.save(path)


def write_population(path, rows):
    r = np.random.default_rng([W.SEED, 41])
    out = [("county_code", "county", "population_2025", "households_2025", "median_age_2025", "persons_per_sq_mile")]
    area = r.uniform(380, 1250, len(rows))
    for k, row in enumerate(rows):
        pop = int(row[5] * r.uniform(1.85, 2.45))
        out.append((row[0], row[1], pop, int(pop / r.uniform(2.25, 2.55)), round(r.uniform(36.5, 47.5), 1), round(pop / area[k], 1)))
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(out)


def write_pack(w, T, out, published_rows):
    """every data file into out; returns the row counts"""
    import os
    n = {}
    f = lambda k: os.path.join(out, W.FILES[k])
    n["reports"] = write_csv(T["reports"], f("reports"))
    n["accounts"] = write_csv(T["accounts"], f("accounts"))
    n["status"] = write_csv(T["status"], f("status"))
    n["worksites"] = write_csv(T["worksites"], f("worksites"))
    n["counties"] = write_csv(counties_table(), f("counties"))
    n["naics"] = write_csv(naics_table(), f("naics"))
    write_published(published_rows, f("published"))
    write_population(f("population"), published_rows)
    return n
