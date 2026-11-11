"""The process behind task14's files: Penmarra's rental market, simulated from 2008 to the end of 2026.

Dwellings come into and leave the rental market; small landlords, a few property companies and three operators let
them; every tenancy starts at the going rent for its dwelling, runs until its tenants leave, and has its rent raised
at reviews (small landlords at some anniversaries, the operators on their own schedules). The Tenancy Bond Board
sees a tenancy when its bond is lodged and when it is refunded; it sees a rise only if the landlord lodges more bond.
The Statistics Office's rent panel, drawn from the dwellings let at the end of 2017, sees the rent every quarter.
Nothing here is placed for a result: every file under target/ is written by pack.py from these records."""
import datetime as dt
import math

import numpy as np

import params as P

EPOCH = dt.date(1970, 1, 1)


def day(d):
    return (d - EPOCH).days


def date_of(n):
    return EPOCH + dt.timedelta(days=int(n))


def month_index(n):
    """Months since January 2000 for a day number."""
    d = date_of(n)
    return (d.year - 2000) * 12 + d.month - 1


M0 = 2000
N_MONTHS = (2028 - M0) * 12


# ------------------------------------------------------------------------------------------------ names
SUBURB_PARTS_A = ["Ash", "Bell", "Birch", "Brook", "Cairn", "Cedar", "Clare", "Clifton", "Corran", "Crest",
                  "Dun", "Elm", "Fair", "Fern", "Glen", "Gold", "Green", "Hallam", "Harbour", "Hazel", "Heath",
                  "High", "Holly", "Kerrow", "Kings", "Lark", "Lea", "Linden", "Maple", "Marsh", "Mead", "Mill",
                  "Moor", "Neven", "Oak", "Orchard", "Pine", "Quarry", "Raven", "Red", "Ridge", "Rose", "Rowan",
                  "Sand", "Shore", "Silver", "Spring", "Stone", "Strath", "Tane", "Thorn", "Wake", "Wells",
                  "West", "Willow", "Wren", "Yarrow"]
SUBURB_PARTS_B = ["field", "dale", "ton", "wood", "vale", "bank", "side", "view", "mere", "brook", "ford",
                  "leigh", "worth", "haven", "hurst", " Heights", " Park", " Bay", " Hill", " Valley", " Downs",
                  " Point", " Flat", " Grove", " Junction", " Beach", " Rise"]
STREET_NAMES = ["Albert", "Alexander", "Anzac", "Arthur", "Ashgrove", "Aurora", "Avon", "Balmoral", "Bannister",
                "Barrow", "Beach", "Beaumont", "Bell", "Birchfield", "Blair", "Bower", "Bracken", "Bridge",
                "Brighton", "Burnside", "Cambridge", "Campbell", "Carlton", "Castle", "Cecil", "Chapel",
                "Charles", "Chester", "Church", "Clarence", "Clifford", "Clyde", "College", "Collingwood",
                "Cook", "Coronation", "Cross", "Crown", "Cuba", "Dalton", "Derby", "Devon", "Dock", "Domain",
                "Dover", "Duke", "Durham", "Earl", "Eden", "Edward", "Elgin", "Elizabeth", "Esk", "Fairview",
                "Fenwick", "Fitzroy", "Forth", "Fox", "Frederick", "Garden", "George", "Gladstone", "Glebe",
                "Gordon", "Grafton", "Grange", "Grey", "Grove", "Hamilton", "Hanover", "Harbour", "Harley",
                "Hastings", "Heaton", "Henry", "Herbert", "High", "Hill", "Hobson", "Holland", "Hope", "Howard",
                "Huntley", "Inglis", "Jackson", "James", "Jervois", "Kent", "Kimberley", "King", "Kingsley",
                "Kitchener", "Lambton", "Lancaster", "Lansdowne", "Lever", "Lincoln", "Lindsay", "Livingstone",
                "Lomond", "Lorne", "Lyndhurst", "Main", "Manor", "Marine", "Market", "Marlborough", "Matlock",
                "Melrose", "Merton", "Mill", "Milton", "Moana", "Montrose", "Moray", "Morgan", "Napier", "Nelson",
                "Newcastle", "Norfolk", "Norman", "Oxford", "Palmer", "Park", "Parnell", "Pembroke", "Percy",
                "Picton", "Pitt", "Princes", "Queen", "Raleigh", "Regent", "Richmond", "Ridge", "Riverside",
                "Rochester", "Rodney", "Ross", "Russell", "Rutland", "Salisbury", "Sandringham", "School",
                "Selwyn", "Seymour", "Shakespeare", "Sheffield", "Sherwood", "Somerset", "Spencer", "Stafford",
                "Stanley", "Station", "Stirling", "Stuart", "Surrey", "Sussex", "Sydney", "Tasman", "Taylor",
                "Thames", "Thomas", "Tower", "Trafalgar", "Tweed", "Union", "Valley", "Vernon", "Victoria",
                "Vine", "Walker", "Wallace", "Warwick", "Waterloo", "Watson", "Wellesley", "Wellington", "Wesley",
                "Westminster", "William", "Wilton", "Winchester", "Windsor", "Wolseley", "Worcester", "York"]
STREET_TYPES = [("Street", 0.40), ("Road", 0.20), ("Avenue", 0.09), ("Terrace", 0.06), ("Crescent", 0.06),
                ("Place", 0.06), ("Drive", 0.05), ("Lane", 0.03), ("Grove", 0.02), ("Parade", 0.01),
                ("Way", 0.01), ("Close", 0.01)]
OLD_AREAS = [  # code, name, the 2024 region(s) its suburbs went to
    ("A01", "City Centre", ["HC"]), ("A02", "Inner Harbour", ["HC"]), ("A03", "Hallam Fringe", ["HC", "HE"]),
    ("A04", "University", ["HN"]), ("A05", "North Hills", ["HN"]), ("A06", "Northern Bays", ["HN", "KC"]),
    ("A07", "Eastern Suburbs", ["HE"]), ("A08", "Brickfields", ["HE"]), ("A09", "Southern Suburbs", ["HS"]),
    ("A10", "South Hallam", ["HS"]), ("A11", "Southern Plains", ["HS", "MV"]), ("A12", "Kerrow", ["KC"]),
    ("A13", "Tane Bay", ["KC"]), ("A14", "Coast North", ["KC"]), ("A15", "Midvale Town", ["MV"]),
    ("A16", "Midvale Rural", ["MV"]), ("A17", "Corran Valley", ["MV"]), ("A18", "Westport", ["WS"]),
    ("A19", "Western Ranges", ["WS"]), ("A20", "Strath", ["WS"]),
]
AGENCY_NAMES = ["Bayline Property", "Kestrel Rentals", "Harbourview Lettings", "Tane Bay Realty",
                "Coastline Property Management", "Northside Rentals", "Brightwater Property", "Keystone Lettings",
                "Ridgeway Rentals", "Southern Cross Property", "Midvale Rentals", "Westerly Property Group",
                "Corran Lettings", "Quayline Management", "Ironbark Property", "Bluegum Rentals",
                "Seaside Property Services", "Heritage Lettings", "Parkside Rentals", "Summit Property Management",
                "Cityside Lettings", "Greenwood Rentals", "Lighthouse Property", "Anchor Property Management",
                "Rosewood Lettings", "Kingfisher Rentals", "Silverdale Property", "Meadowbank Lettings",
                "Fernleigh Property", "Hallam Rental Co", "Oakridge Property", "Strathmore Lettings",
                "Waterfront Rentals", "Cornerstone Property", "Pinnacle Lettings", "Driftwood Rentals",
                "Clearview Property", "Northgate Lettings"]
COMPANY_NAMES = ["Penmarra Housing Trust", "Ardent Property Holdings", "Marsden Investments", "Kerrow Estates",
                 "Halcyon Property Ltd", "Bramley Holdings", "Westbury Property Ltd", "Tasman Bay Estates",
                 "Corran Property Ltd", "Linden Investments", "Rowan Holdings", "Greystone Property",
                 "Fairhaven Estates", "Calder Property Ltd", "Bellbird Holdings", "Stonegate Property",
                 "Ashby Investments", "Millbrook Estates", "Northcote Holdings", "Pembroke Property Ltd",
                 "Larkspur Investments", "Rivermead Holdings", "Thornbury Property", "Wakefield Estates"]


class World:
    pass


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    W.rng_seed = seed
    _geography(W, rng)
    _market(W, rng)
    _dwellings(W, rng)
    _tenancies(W, rng)
    _panel(W, rng)
    return W


# ------------------------------------------------------------------------------------------------ geography
def _geography(W, rng):
    used = set()
    suburbs = []          # dicts: name, postcode, area, region
    area_regions = {a[0]: a[2] for a in OLD_AREAS}
    # number of suburbs per area, more in the capital
    pc_blocks = {"HC": 6000, "HN": 6100, "HE": 6200, "HS": 6300, "KC": 7100, "MV": 7300, "WS": 7500}
    pc_used = set()
    for code, name, regs in OLD_AREAS:
        n = int(rng.integers(5, 9)) if regs[0] in ("HC", "HN", "HE", "HS") else int(rng.integers(4, 8))
        for i in range(n):
            while True:
                nm = rng.choice(SUBURB_PARTS_A) + rng.choice(SUBURB_PARTS_B)
                if nm not in used:
                    used.add(nm)
                    break
            reg = regs[0] if len(regs) == 1 else (regs[0] if i < (n + 1) // 2 else regs[1])
            while True:
                pc = pc_blocks[reg] + int(rng.integers(10, 99))
                if pc not in pc_used:
                    pc_used.add(pc)
                    break
            suburbs.append({"name": nm, "postcode": pc, "area": code, "region": reg,
                            "weight": float(rng.gamma(3.0, 1.0))})
    # some endings come up often from the parts above; rotate every other one to another local ending (no draws)
    extra = [" Terrace", " Gardens", " Common", " Reach", " Green", " Fields", " Ridge", " End", "minster", "gate",
             "stow", "combe", "ley", "ham"]
    seen = {s["name"] for s in suburbs}
    for k, s in enumerate(suburbs):
        for end in ("hurst", " Rise", " Flat", " Junction", " Downs", " Heights"):
            if s["name"].endswith(end) and k % 2 == 0:
                stem = s["name"][: -len(end)]
                for m in range(len(extra)):
                    cand = stem + extra[(k + m) % len(extra)]
                    if cand not in seen:
                        seen.discard(s["name"])
                        s["name"] = cand
                        seen.add(cand)
                        break
                break
    W.suburbs = suburbs
    W.area_regions = area_regions
    # streets per suburb
    streets = {}
    types = [t for t, _ in STREET_TYPES]
    tw = np.array([w for _, w in STREET_TYPES])
    tw = tw / tw.sum()
    for s_i, s in enumerate(suburbs):
        k = int(rng.integers(22, 48))
        names = rng.choice(STREET_NAMES, size=k, replace=False)
        stypes = rng.choice(types, size=k, p=tw)
        streets[s_i] = [(str(a), str(b)) for a, b in zip(names, stypes)]
    W.streets = streets


# ------------------------------------------------------------------------------------------------ market
def _market(W, rng):
    nreg = len(P.REGIONS)
    logm = np.zeros((nreg, N_MONTHS))
    for ri, reg in enumerate(P.REGIONS):
        mult = reg[4]
        lvl = 0.0
        ar = 0.0
        for m in range(N_MONTHS):
            y = M0 + m // 12
            g = P.MARKET_MONTH.get((y, m % 12 + 1), P.MARKET_GROWTH.get(y, 0.035))
            # a regional boom multiplies the deviation from a 3.5 per cent trend
            ga = 0.035 + (g - 0.035) * mult
            ar = 0.55 * ar + rng.normal(0.0, 0.0022)
            lvl += ga / 12.0 + ar * 0.25
            logm[ri, m] = lvl
        # level so that January 2021 is zero
        logm[ri] -= logm[ri, (2021 - M0) * 12]
    W.logm = logm
    W.region_index = {r[0]: i for i, r in enumerate(P.REGIONS)}


def market_rent(W, ri, dtype, beds, q, n):
    m = month_index(n)
    d = date_of(n)
    code = P.REGIONS[ri][0]
    base = P.BASE_RENT_2021[code] * P.TYPE_FACTOR[dtype] * P.BED_FACTOR[beds]
    return base * q * math.exp(W.logm[ri, m] + P.SEASON[d.month - 1])


def trailing_growth(W, ri, n):
    m = month_index(n)
    return float(W.logm[ri, m] - W.logm[ri, max(m - 12, 0)])


def prior_year_growth(W, ri, y):
    """The region's letting-market growth over the previous calendar year (December to December)."""
    m1 = (y - 1 - M0) * 12 + 11
    m0 = m1 - 12
    if m0 < 0:
        return 0.035
    return float(W.logm[ri, m1] - W.logm[ri, m0])


def round_rent(x):
    if x <= 600:
        return float(max(5 * round(x / 5.0), 5))
    return float(10 * round(x / 10.0))


# ------------------------------------------------------------------------------------------------ dwellings
def _dwellings(W, rng):
    sub_by_region = {r: [i for i, s in enumerate(W.suburbs) if s["region"] == r] for r in P.REGION_CODES}
    dw = {k: [] for k in ("region", "suburb", "dtype", "beds", "q", "street", "number", "unit", "owner",
                          "entry", "operator", "block")}
    owners = []           # dicts: kind (small, company, operator), agent, name
    building_count = {}   # (suburb, street index, number) -> units taken, to keep addresses distinct

    def new_owner(kind, agent=None, name=None):
        owners.append({"kind": kind, "agent": agent, "name": name})
        return len(owners) - 1

    agents = list(range(len(AGENCY_NAMES)))
    agent_w = rng.gamma(1.4, 1.0, size=len(agents))
    agent_w = agent_w / agent_w.sum()
    companies = [new_owner("company", agent=int(rng.choice(agents, p=agent_w)) if rng.random() < 0.6 else None,
                           name=COMPANY_NAMES[i]) for i in range(len(COMPANY_NAMES))]

    def pick_address(si, dtype):
        sts = W.streets[si]
        while True:
            st = int(rng.integers(0, len(sts)))
            if dtype == "H":
                num = int(rng.integers(1, 240))
                key = (si, st, num)
                if key not in building_count:
                    building_count[key] = 1
                    return st, num, ""
            elif dtype == "T":
                num = int(rng.integers(1, 240))
                key = (si, st, num)
                if key not in building_count:
                    building_count[key] = int(rng.integers(2, 7))
                k = building_count.setdefault((si, st, num, "taken"), 0)
                if k < building_count[key]:
                    building_count[(si, st, num, "taken")] = k + 1
                    return st, num, str(k + 1)
            else:
                num = int(rng.integers(1, 180))
                key = (si, st, num)
                if key not in building_count:
                    building_count[key] = int(rng.integers(6, 36))
                k = building_count.setdefault((si, st, num, "taken"), 0)
                if k < building_count[key]:
                    building_count[(si, st, num, "taken")] = k + 1
                    return st, num, str(k + 1)

    def small_owner():
        agent = int(rng.choice(agents, p=agent_w)) if rng.random() < P.AGENT_SHARE else None
        return new_owner("small", agent=agent)

    # small landlords own one to six dwellings; a dwelling joins an existing owner's portfolio sometimes
    open_owners = []

    def assign_owner(dtype):
        if dtype in ("T", "A") and rng.random() < P.MEDIUM_SHARE / 0.5:
            return int(rng.choice(companies))
        if open_owners and rng.random() < 0.30:
            i = int(rng.integers(0, len(open_owners)))
            o = open_owners[i]
            if rng.random() < 0.5:
                open_owners.pop(i)
            return o
        o = small_owner()
        if rng.random() < 0.35:
            open_owners.append(o)
        return o

    def add(ri, si, dtype, beds, q, st, num, unit, owner, entry, operator="", block=-1):
        dw["region"].append(ri)
        dw["suburb"].append(si)
        dw["dtype"].append(dtype)
        dw["beds"].append(beds)
        dw["q"].append(q)
        dw["street"].append(st)
        dw["number"].append(num)
        dw["unit"].append(unit)
        dw["owner"].append(owner)
        dw["entry"].append(entry)
        dw["operator"].append(operator)
        dw["block"].append(block)

    def draw_beds(dtype):
        if dtype == "H":
            return int(rng.choice([2, 3, 4, 5], p=[0.16, 0.50, 0.28, 0.06]))
        if dtype == "T":
            return int(rng.choice([1, 2, 3], p=[0.20, 0.55, 0.25]))
        return int(rng.choice([0, 1, 2, 3], p=[0.12, 0.44, 0.36, 0.08]))

    def new_small_dwelling(entry, region=None):
        if region is None:
            ri = int(rng.choice(len(P.REGIONS), p=np.array([r[2] for r in P.REGIONS]) / sum(r[2] for r in P.REGIONS)))
        else:
            ri = region
        code = P.REGIONS[ri][0]
        mix = P.REGIONS[ri][3]
        dtype = str(rng.choice(["H", "T", "A"], p=mix))
        subs = sub_by_region[code]
        sw = np.array([W.suburbs[s]["weight"] for s in subs])
        si = int(rng.choice(subs, p=sw / sw.sum()))
        beds = draw_beds(dtype)
        q = float(np.exp(rng.normal(0.0, 0.13)))
        st, num, unit = pick_address(si, dtype)
        owner = assign_owner(dtype)
        add(ri, si, dtype, beds, q, st, num, unit, owner, entry)

    start = day(P.SIM_START)
    for _ in range(P.STOCK_2008):
        new_small_dwelling(start)
    # entries month by month: new builds and conversions into the rental market
    stock = float(P.STOCK_2008)
    n_months = (P.SIM_END.year - P.SIM_START.year + 1) * 12
    for m in range(n_months):
        y = P.SIM_START.year + m // 12
        mo = m % 12 + 1
        lam = stock * P.ENTRY_RATE / 12.0 * (1.15 if y >= 2021 else 1.0)
        k = int(rng.poisson(lam))
        first = day(dt.date(y, mo, 1))
        for _ in range(k):
            # new dwellings lean to the capital's apartments and townhouses
            ri = int(rng.choice(len(P.REGIONS), p=[0.19, 0.15, 0.17, 0.14, 0.13, 0.12, 0.10]))
            new_small_dwelling(first + int(rng.integers(0, 28)), region=ri)
        stock += k * 0.55   # exits run at about half the entries over the long run
    # operator blocks
    op_owner = {op: new_owner("operator", name=P.OPERATORS[op]["name"]) for op in P.OPERATORS}
    for bi, (op, code, opened, units, stname, num, bedmix) in enumerate(P.BLOCKS):
        ri = W.region_index[code]
        subs = sub_by_region[code]
        si = int(rng.choice(subs))
        # the block's street joins the suburb's street list
        stype = "Street" if op != "C" else "Road"
        W.streets[si].append((stname, stype))
        st = len(W.streets[si]) - 1
        floors = max(3, units // 60)
        per_floor = -(-units // floors)
        for u in range(units):
            fl = 1 + u // per_floor
            unit = "%d%02d" % (fl, u % per_floor + 1)
            beds = int(rng.choice([0, 1, 2, 3], p=bedmix))
            q = P.OPERATOR_QUALITY[op] * float(np.exp(rng.normal(0.0, 0.05)))
            add(ri, si, "A" if op != "C" else "R", beds if op != "C" else 0, q, st, num, unit, op_owner[op],
                day(opened), operator=op, block=bi)
    for k in dw:
        dw[k] = np.array(dw[k], dtype=object if k in ("dtype", "unit", "operator") else None)
    W.dw = dw
    W.n_dw = len(dw["region"])
    W.owners = owners
    W.op_owner = op_owner
    W.agent_names = AGENCY_NAMES


# ------------------------------------------------------------------------------------------------ tenancies
def _hazard_cdf(h, mult, n=360):
    a, b, c, d = h
    s = 1.0
    cdf = np.zeros(n)
    acc = 0.0
    for k in range(1, n + 1):
        if k < 12:
            p = a
        elif k == 12:
            p = b
        elif k <= 24:
            p = c
        else:
            p = d
        p = min(p * mult, 0.95)
        acc += s * p
        s *= (1 - p)
        cdf[k - 1] = acc
    cdf[-1] = 1.0
    return cdf


def _draw_months(rng, cdf):
    u = rng.random()
    return int(np.searchsorted(cdf, u)) + 1


def _anniversaries(start, end):
    s = date_of(start)
    out = []
    k = 1
    while True:
        try:
            a = s.replace(year=s.year + k)
        except ValueError:
            a = s.replace(year=s.year + k, day=28)
        n = day(a)
        if n >= end:
            break
        out.append(n)
        k += 1
    return out


def _tenancies(W, rng):
    T = {k: [] for k in ("dwelling", "start", "end", "rent0", "bonded", "lodged", "refund", "owner0")}
    CH = {k: [] for k in ("tenancy", "date", "rent", "pct", "topup", "topup_date", "effective_field")}
    EV = {k: [] for k in ("tenancy", "kind", "date", "owner")}       # transfers and changes of parties
    sim_end = day(P.SIM_END)
    cdf_small = {ri: _hazard_cdf(P.HAZARD_SMALL, P.REGIONS[ri][5]) for ri in range(len(P.REGIONS))}
    cdf_btr = _hazard_cdf(P.HAZARD_BTR, 1.0)
    owner_of = list(W.dw["owner"])     # current owner, changes with transfers

    def cpi(y, q):
        return P.CPI_YOY[(y, q)] / 100.0

    def topup_p(r, agent):
        a, b, c = P.TOPUP_LOGIT
        z = a + b * r + c * (1 if agent is not None else 0)
        return 1.0 / (1.0 + math.exp(-z))

    for d in range(W.n_dw):
        ri = int(W.dw["region"][d])
        dtype = W.dw["dtype"][d]
        beds = int(W.dw["beds"][d])
        q = float(W.dw["q"][d])
        op = W.dw["operator"][d]
        entry = int(W.dw["entry"][d])
        if op == "C":
            _student_tenancies(W, rng, d, T, CH)
            continue
        # first tenancy
        if entry == day(P.SIM_START):
            # the stock at the start of 2008 holds tenancies of every age
            age_m = int(rng.choice(np.arange(0, 96), p=_stationary_age()))
            t_start = entry - int(age_m * 30.4375) - int(rng.integers(0, 28))
            lease_up = 0
        else:
            lease_up = int(rng.integers(0, 200)) if op in ("A", "B") else int(rng.integers(7, 70))
            t_start = entry + lease_up
        prev_rent = None
        while t_start < sim_end:
            owner = owner_of[d]
            o = W.owners[owner]
            if op:
                rent = round_rent(market_rent(W, ri, dtype, beds, q, t_start) * math.exp(rng.normal(0, 0.025))
                                  * (0.96 if t_start - entry < 240 else 1.0))
                if rent > 600:
                    rent = float(round(rent))
            else:
                mk = market_rent(W, ri, dtype, beds, q, t_start) * math.exp(rng.normal(0, 0.045))
                if prev_rent is not None and rng.random() < P.RELET_LAGGARD:
                    mk = prev_rent * (1 + rng.uniform(0.0, 0.03))
                rent = round_rent(mk)
            cdf = cdf_btr if op else cdf_small[ri]
            k = _draw_months(rng, cdf)
            if k == 12:
                t_end = t_start + 364 + int(rng.integers(-6, 11))
            else:
                t_end = t_start + int(round(30.4375 * k)) - int(rng.integers(0, 25))
            t_end = max(t_end, t_start + 40)
            bonded = bool(op) or rng.random() > P.P_NO_BOND
            lodged = t_start + int(rng.integers(P.LODGE_DELAY[0], P.LODGE_DELAY[1] + 1))
            refund = t_end + int(rng.integers(P.REFUND_DELAY[0], P.REFUND_DELAY[1] + 1))
            tid = len(T["dwelling"])
            T["dwelling"].append(d)
            T["start"].append(t_start)
            T["end"].append(t_end)
            T["rent0"].append(rent)
            T["bonded"].append(bonded)
            T["lodged"].append(lodged)
            T["refund"].append(refund)
            T["owner0"].append(owner)
            # reviews
            cur = rent
            if not op:
                for a in _anniversaries(t_start, min(t_end, sim_end + 1)):
                    y = date_of(a).year
                    if rng.random() < P.P_RISE.get(y, 0.66):
                        g = prior_year_growth(W, ri, y)
                        med = max(P.RISE_FLOOR, P.RISE_SLOPE * g + P.RISE_FLOOR)
                        r = min(med * math.exp(rng.normal(0, P.RISE_SIGMA)), P.RISE_CAP)
                        new = round_rent(cur * (1 + r))
                        if new <= cur:
                            new = cur + 5
                        pct = new / cur - 1
                        agent = W.owners[owner_of[d]]["agent"]
                        tp = rng.random() < topup_p(pct, agent)
                        tdate = a + int(rng.integers(P.TOPUP_DELAY[0], P.TOPUP_DELAY[1] + 1)) if tp else -1
                        if tp and tdate >= t_end:
                            tp, tdate = False, -1
                        CH["tenancy"].append(tid)
                        CH["date"].append(a)
                        CH["rent"].append(new)
                        CH["pct"].append(pct)
                        CH["topup"].append(tp)
                        CH["topup_date"].append(tdate)
                        CH["effective_field"].append(bool(tp and rng.random() < P.EFFECTIVE_FIELD_SHARE))
                        cur = new
            else:
                for y in range(date_of(t_start).year, date_of(min(t_end, sim_end)).year + 1):
                    if op == "A":
                        rd = day(dt.date(y, 12, 1))
                        eligible = t_start < day(dt.date(y, 6, 1))
                        pct_target = cpi(y, 3) + P.OPERATORS["A"]["margin"] / 100.0
                    else:
                        rd = day(dt.date(y, 11, 1))
                        eligible = t_start < day(dt.date(y, 5, 1))
                        pct_target = cpi(y, 3) + P.OPERATORS["B"]["margin"] / 100.0
                    if not eligible or rd <= t_start or rd >= t_end or rd > sim_end:
                        continue
                    new = float(round(cur * (1 + pct_target)))
                    pct = new / cur - 1
                    lag = P.OP_TOPUP_LAG[op]
                    tdate = rd + int(rng.integers(lag[0], lag[1]))
                    tp = tdate < t_end
                    CH["tenancy"].append(tid)
                    CH["date"].append(rd)
                    CH["rent"].append(new)
                    CH["pct"].append(pct)
                    CH["topup"].append(tp)
                    CH["topup_date"].append(tdate if tp else -1)
                    CH["effective_field"].append(bool(tp))
                    cur = new
            # transfers (sold with the tenant in place) and changes of parties during the tenancy
            if not op:
                span_y = (min(t_end, sim_end) - t_start) / 365.25
                for kind, rate in (("transfer", P.P_TRANSFER_YR), ("parties", P.P_PARTIES_YR)):
                    nev = int(rng.poisson(max(span_y, 0) * rate))
                    for _ in range(nev):
                        when = t_start + int(rng.integers(30, max(31, min(t_end, sim_end) - t_start)))
                        if when >= t_end:
                            continue
                        new_owner = None
                        if kind == "transfer":
                            agent = int(rng.choice(len(W.agent_names))) if rng.random() < P.AGENT_SHARE else None
                            W.owners.append({"kind": "small", "agent": agent, "name": None})
                            new_owner = len(W.owners) - 1
                            owner_of[d] = new_owner
                        EV["tenancy"].append(tid)
                        EV["kind"].append(kind)
                        EV["date"].append(when)
                        EV["owner"].append(new_owner if new_owner is not None else -1)
            prev_rent = cur
            # what happens after the tenancy ends
            if not op and rng.random() < P.P_EXIT_SMALL:
                break
            if op:
                gap = int(rng.integers(5, 30))
            else:
                gap = int(round(7 * rng.gamma(P.VACANCY_WEEKS[0], P.VACANCY_WEEKS[1])))
            t_start = t_end + gap
    for k in T:
        T[k] = np.array(T[k])
    for k in CH:
        CH[k] = np.array(CH[k])
    for k in EV:
        EV[k] = np.array(EV[k], dtype=object if k == "kind" else None)
    # transfers recorded in time order per tenancy; owner chains kept for the register
    W.T = T
    W.CH = CH
    W.EV = EV
    W.n_t = len(T["dwelling"])


_STAT = None


def _stationary_age():
    global _STAT
    if _STAT is None:
        cdf = _hazard_cdf(P.HAZARD_SMALL, 1.0, n=96)
        surv = 1 - np.concatenate([[0.0], cdf[:-1]])
        _STAT = surv / surv.sum()
    return _STAT


def _student_tenancies(W, rng, d, T, CH):
    entry = int(W.dw["entry"][d])
    ri = int(W.dw["region"][d])
    q = float(W.dw["q"][d])
    year0 = date_of(entry).year
    rate = round_rent(market_rent(W, ri, "R", 0, q, entry) * 1.02)
    for y in range(year0, P.SIM_END.year + 1):
        if y > year0:
            rate = float(round(rate * (1 + P.STUDENT_RATE_STEP.get(y, 0.04))))
        feb = dt.date(y, 2, 1)
        # the academic year's leases start on the second Monday of February, a few days either side
        sm = feb + dt.timedelta(days=(7 - feb.weekday()) % 7 + 7)
        t_start = day(sm) + int(rng.integers(-3, 5))
        if t_start < entry:
            t_start = entry
        if rng.random() > 0.95 and y > year0:
            continue
        t_end = t_start + 357 + int(rng.integers(-4, 3))
        if t_start > day(P.SIM_END):
            break
        tid = len(T["dwelling"])
        T["dwelling"].append(d)
        T["start"].append(t_start)
        T["end"].append(t_end)
        T["rent0"].append(rate)
        T["bonded"].append(True)
        T["lodged"].append(t_start + int(rng.integers(1, 15)))
        T["refund"].append(t_end + int(rng.integers(3, 20)))
        T["owner0"].append(int(W.dw["owner"][d]))


# ------------------------------------------------------------------------------------------------ the panel
def ref_days():
    out = []
    y, qq = P.PANEL_FIRST_Q
    while (y, qq) <= P.PANEL_LAST_Q:
        mo = 3 * qq - 1
        out.append(((y, qq), day(dt.date(y, mo, 15))))
        qq += 1
        if qq == 5:
            y, qq = y + 1, 1
    return out


def rent_on(W, tid, n):
    """Rent payable on day n under tenancy tid (assumes the tenancy is in place on n)."""
    lo, hi = W.ch_index[tid]
    r = W.T["rent0"][tid]
    for j in range(lo, hi):
        if W.CH["date"][j] <= n:
            r = W.CH["rent"][j]
        else:
            break
    return float(r)


def index_changes(W):
    """Changes sorted by tenancy then date, with an index of each tenancy's slice."""
    order = np.lexsort((W.CH["date"], W.CH["tenancy"]))
    for k in W.CH:
        W.CH[k] = W.CH[k][order]
    W.ch_index = {}
    t = W.CH["tenancy"]
    if len(t):
        starts = np.flatnonzero(np.r_[True, t[1:] != t[:-1]])
        ends = np.r_[starts[1:], len(t)]
        for s, e in zip(starts, ends):
            W.ch_index[int(t[s])] = (int(s), int(e))
    for tid in range(W.n_t):
        W.ch_index.setdefault(tid, (0, 0))
    # tenancies of each dwelling in time order
    order = np.lexsort((W.T["start"], W.T["dwelling"]))
    W.ten_by_dw = {}
    for tid in order:
        W.ten_by_dw.setdefault(int(W.T["dwelling"][tid]), []).append(int(tid))


def tenancy_on(W, d, n):
    for tid in W.ten_by_dw.get(d, []):
        if W.T["start"][tid] <= n < W.T["end"][tid]:
            return tid
    return -1


def _panel(W, rng):
    index_changes(W)
    frame_day = day(P.PANEL_FRAME)
    frame = []
    for d in range(W.n_dw):
        if W.dw["operator"][d]:
            continue
        tid = tenancy_on(W, d, frame_day)
        if tid >= 0 and W.T["bonded"][tid]:
            frame.append(d)
    frame = np.array(frame)
    strata = {}
    for d in frame:
        key = (P.REGION_CODES[int(W.dw["region"][d])], W.dw["dtype"][d])
        strata.setdefault(key, []).append(int(d))
    total = len(frame)
    alloc = {}
    for key, members in strata.items():
        alloc[key] = max(P.PANEL_MIN_STRATUM, int(round(P.PANEL_SIZE * len(members) / total)))
    sample = {}
    for key, members in strata.items():
        pick = rng.choice(members, size=min(alloc[key], len(members)), replace=False)
        sample[key] = [int(x) for x in pick]
    W.panel_strata = {k: {"N": len(v), "n": len(sample[k])} for k, v in strata.items()}
    W.panel_frame = set(int(x) for x in frame)
    # follow each panel slot through the quarters; a dwelling that leaves the rental market is replaced from its stratum
    refs = ref_days()
    rows = []
    in_panel = set(x for v in sample.values() for x in v)
    slot = 0
    for key, members in sample.items():
        for d0 in members:
            slot += 1
            cur = d0
            replaced_from = None
            for (yq, rd) in refs:
                tid = tenancy_on(W, cur, rd)
                if tid < 0:
                    # vacant, or gone from the rental market for good
                    later = [t for t in W.ten_by_dw.get(cur, []) if W.T["start"][t] > rd]
                    if not later:
                        # replace from the stratum with a dwelling still let, not already in the panel
                        cands = [x for x in strata[key] if x not in in_panel and tenancy_on(W, x, rd) >= 0]
                        if cands:
                            new = int(rng.choice(cands))
                            in_panel.add(new)
                            rows.append((slot, cur, yq, rd, "X", -1, None))
                            replaced_from = cur
                            cur = new
                            tid = tenancy_on(W, cur, rd)
                        else:
                            rows.append((slot, cur, yq, rd, "X", -1, None))
                            continue
                    else:
                        rows.append((slot, cur, yq, rd, "V", -1, replaced_from))
                        replaced_from = None
                        continue
                if rng.random() > P.PANEL_RESPONSE:
                    rows.append((slot, cur, yq, rd, "N", tid, replaced_from))
                else:
                    rows.append((slot, cur, yq, rd, "R", tid, replaced_from))
                replaced_from = None
    W.panel_rows = rows
