"""task9, architecture 6: the truth behind the pack.

Sponsor houses raise buyout funds one after another. A fund buys European mid-market companies during its five-year
investment period, each with a first-lien loan at the buyout; companies refinance, are sold on to other houses' funds,
are sold to trade buyers or listed, or default. A company defaults in a calendar year when its latent credit standing
falls below the threshold its rating and its full years since the current owner's buyout set. The standing carries the
economy's year, its industry's year and the year of the sponsor house whose fund holds it: a house decides across all
the funds it runs, from one partnership's view of the year and its standing with its investors, whether to put more
money into a company that breaches, so a house's companies fail in the same years. Nothing here is shipped; pack.py
writes what each system would hold.
"""
import collections
import datetime as dt

import numpy as np
from scipy.stats import norm

SEED = 107
NH = 80                      # sponsor houses
Y0, Y1 = 1997, 2026          # simulated calendar years; the stock builds up before Lenderbase starts
DB0 = 2008                   # first year of Lenderbase's coverage
AS_OF = dt.date(2026, 12, 31)
NI = 16
AM, AK, AH = 0.10, 0.07, 0.40
RATINGS = ["B+", "B", "B-", "CCC+"]
MOODYS = ["B1", "B2", "B3", "Caa1"]
BASE = np.array([0.0135, 0.0235, 0.0400, 0.0780])
SEAS = np.array([0.0, 0.62, 1.12, 1.38, 1.30, 1.10, 0.92, 0.82, 0.78, 0.76, 0.75, 0.75, 0.75, 0.75, 0.75,
                 0.75, 0.75, 0.75, 0.75, 0.75, 0.75])
MACRO = {1997: 0.8, 1998: 0.4, 1999: 0.7, 2000: 0.5, 2001: -0.6, 2002: -1.3, 2003: -0.5, 2004: 0.6, 2005: 0.8,
         2006: 0.9, 2007: 0.4, 2008: -1.1, 2009: -2.15, 2010: 0.45, 2011: -0.5, 2012: -1.25, 2013: 0.1, 2014: 0.6,
         2015: 0.45, 2016: 0.3, 2017: 1.05, 2018: 0.2, 2019: 0.45, 2020: -1.85, 2021: 1.2, 2022: -0.35, 2023: -1.4,
         2024: -0.6, 2025: 0.05, 2026: 0.25}
RATING_MIX = [0.22, 0.46, 0.26, 0.06]
COVERAGE = 0.78              # share of loans whose lender reports to Lenderbase
FUND_SIZE = (9, 17)          # platform buys over the investment period
EXIT_FROM_AGE = 3
EXIT_P = 0.21
SECONDARY_P = 0.40
REFI_P = 0.12
# workouts: duration in years and the recovery it ends on
WO_SHAPE, WO_SCALE = 2.6, 1.05
REC_A, REC_B, REC_SD = 0.93, 0.125, 0.14

SECTORS = [  # Lenderbase code, Lenderbase name, Kestrel Lane (agency industry), Ostvale (GICS-style), Dealtrail word
    ("LB01", "Business services", "Services: Business", "Commercial & Professional Services", "Business services"),
    ("LB02", "Healthcare services", "Healthcare & Pharmaceuticals", "Health Care Equipment & Services", "Healthcare"),
    ("LB03", "Software and IT services", "High Tech Industries", "Software & Services", "Technology"),
    ("LB04", "Industrial machinery", "Capital Equipment", "Capital Goods", "Industrials"),
    ("LB05", "Building products and services", "Construction & Building", "Building Products", "Construction"),
    ("LB06", "Consumer products", "Consumer Goods: Non-Durable", "Household & Personal Products", "Consumer"),
    ("LB07", "Food and beverage", "Beverage, Food & Tobacco", "Food, Beverage & Tobacco", "Food & drink"),
    ("LB08", "Transport and logistics", "Transportation: Cargo", "Transportation", "Logistics"),
    ("LB09", "Chemicals and materials", "Chemicals, Plastics & Rubber", "Materials", "Chemicals"),
    ("LB10", "Media and telecoms", "Media: Diversified & Production", "Media & Entertainment", "Media"),
    ("LB11", "Education and training", "Services: Consumer", "Consumer Services", "Education"),
    ("LB12", "Environmental services", "Environmental Industries", "Commercial Services & Supplies", "Environmental"),
    ("LB13", "Electrical equipment", "Aerospace & Defense", "Electrical Equipment", "Electrical"),
    ("LB14", "Retail and leisure", "Retail", "Consumer Discretionary Distribution & Retail", "Retail & leisure"),
    ("LB15", "Specialty finance and insurance services", "Banking, Finance, Insurance & Real Estate", "Financial Services", "Financial services"),
    ("LB16", "Automotive parts", "Automotive", "Automobiles & Components", "Automotive"),
]
COUNTRIES = [("DE", "EUR", 0.17), ("FR", "EUR", 0.14), ("NL", "EUR", 0.10), ("GB", "GBP", 0.15), ("SE", "SEK", 0.07),
             ("DK", "DKK", 0.04), ("NO", "NOK", 0.04), ("FI", "EUR", 0.03), ("BE", "EUR", 0.05), ("ES", "EUR", 0.08),
             ("IT", "EUR", 0.07), ("AT", "EUR", 0.02), ("CH", "CHF", 0.04)]
FX = {"EUR": 1.0, "GBP": 0.8631, "SEK": 11.0815, "DKK": 7.4592, "NOK": 11.6740, "CHF": 0.9412}

# ---------------------------------------------------------------- names and identifiers
_PRE = ["Ash", "Brink", "Cald", "Dun", "Esk", "Fen", "Gal", "Har", "Ing", "Lar", "Mar", "North", "Oak", "Pem", "Raven",
        "Salt", "Thorn", "Val", "West", "Yar", "Berg", "Cor", "Del", "Elb", "Fjell", "Gar", "Hav", "Isar", "Kron",
        "Lind", "Mont", "Nord", "Oost", "Prad", "Sol", "Teg", "Vend", "Witt", "Zuid", "Alder", "Birch", "Cran", "Drum",
        "Ember", "Frost", "Glen", "Heath", "Iver", "Juni", "Kel", "Loch", "Moor", "Ness", "Orme", "Quarr", "Rye", "Sedge",
        "Tay", "Ure", "Wren"]
_SUF = ["grove", "haven", "wood", "more", "dale", "wick", "way", "gate", "by", "mont", "low", "stone", "hurst", "ford",
        "worth", "bury", "mere", "stad", "vik", "berg", "strand", "holm", "wal", "ridge", "field", "lake", "cliff",
        "brook", "point", "crest"]
_TAIL = ["Partners", "Capital", "Equity Partners", "Capital Partners", "Investment Partners", "Private Equity"]
_ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
_ON = ["B", "C", "D", "F", "G", "H", "K", "L", "M", "N", "P", "R", "S", "T", "V", "W", "Br", "Cr", "Dr", "Fl",
       "Fr", "Gr", "Kl", "Pr", "Sk", "St", "Tr", "Vr"]
_VW = ["a", "e", "i", "o", "u", "a", "e", "o"]
_MID = ["l", "r", "n", "m", "v", "d", "t", "s", "ld", "rn", "nt", "rt", "lv", "nd", "rk", "lm", "st", "rv"]
_V2 = ["a", "e", "i", "o", "a", "e"]
_TL = ["", "", "n", "s", "x", "ra", "na", "lia", "via", "ris", "tis", "go", "ro", "lo", "nus", "dal", "berg", "holm",
       "heim", "stad", "mark", "ford", "ton", "ville", "ia", "um", "ex"]
_NOUN = {  # by sector code index, then country; "{s}" is the stem
    0: {"DE": "Dienstleistungen", "NL": "Diensten", "FR": "Services", "SE": "Tjänster", "IT": "Servizi", "ES": "Servicios", "": "Services"},
    1: {"DE": "Pflege", "NL": "Zorggroep", "FR": "Santé", "SE": "Omsorg", "IT": "Salute", "ES": "Salud", "": "Healthcare"},
    2: {"FR": "Logiciels", "": "Software"},
    3: {"DE": "Maschinenbau", "NL": "Machinebouw", "FR": "Industries", "SE": "Maskin", "IT": "Meccanica", "": "Engineering"},
    4: {"DE": "Gebäudetechnik", "NL": "Installatietechniek", "FR": "Bâtiment", "SE": "Bygg", "IT": "Costruzioni", "": "Building Services"},
    5: {"DE": "Haushaltswaren", "FR": "Maison", "": "Brands"},
    6: {"DE": "Lebensmittel", "FR": "Alimentaire", "SE": "Livsmedel", "IT": "Alimentari", "ES": "Alimentación", "": "Foods"},
    7: {"DE": "Logistik", "NL": "Logistiek", "FR": "Transports", "SE": "Logistik", "IT": "Trasporti", "": "Logistics"},
    8: {"DE": "Chemie", "NL": "Chemie", "FR": "Chimie", "IT": "Chimica", "": "Chemicals"},
    9: {"FR": "Médias", "": "Media"},
    10: {"DE": "Bildung", "NL": "Opleidingen", "FR": "Formation", "SE": "Utbildning", "IT": "Formazione", "": "Education"},
    11: {"DE": "Umwelttechnik", "NL": "Milieu", "FR": "Environnement", "IT": "Ambiente", "": "Environmental"},
    12: {"DE": "Elektrotechnik", "NL": "Elektro", "FR": "Électrique", "IT": "Elettrica", "": "Electrical"},
    13: {"DE": "Handel", "FR": "Distribution", "": "Retail"},
    14: {"DE": "Versicherungsservice", "": "Insurance Services"},
    15: {"DE": "Automotive", "FR": "Équipements", "IT": "Componenti", "": "Automotive"},
}
_GROUP = {"FR": "Groupe {s}", "IT": "Gruppo {s}", "ES": "Grupo {s}", "DE": "{s} Gruppe", "SE": "{s} Gruppen",
          "DK": "{s} Gruppen", "NO": "{s} Gruppen", "NL": "{s} Groep", "": "{s} Group"}
_FORM = {
    "DE": ["Holding GmbH", "Bidco GmbH", "Gruppe GmbH", "Holdco GmbH"], "AT": ["Holding GmbH", "Bidco GmbH"],
    "CH": ["Holding AG", "Bidco AG"], "NL": ["Holding B.V.", "Groep B.V.", "Bidco B.V."], "BE": ["Holding BV", "Bidco SA"],
    "FR": ["Holding SAS", "SAS", "Bidco SAS"], "GB": ["Group Limited", "Holdings Ltd", "Bidco Limited", "Topco Ltd"],
    "IE": ["Holdings Limited", "Bidco DAC"], "SE": ["Holding AB", "Topco AB", "Bidco AB"], "DK": ["Holding ApS", "Bidco A/S"],
    "NO": ["Holding AS", "Bidco AS"], "FI": ["Holding Oy", "Bidco Oy"], "ES": ["Holdco S.L.", "Bidco S.L.U."],
    "IT": ["Holding S.p.A.", "Bidco S.r.l."],
}
_LOU = ["5299", "8945", "2138", "7245", "9845", "3912", "2549", "6354", "8156", "4469"]


def lei(rng):
    """An ISO 17442 identifier with valid ISO 7064 mod 97-10 check digits."""
    body = rng.choice(_LOU) + "00" + "".join(rng.choice(list("0123456789ABCDEFGHJKLMNPRSTUVWXYZ"), 12))
    num = "".join(str(int(ch, 36)) for ch in body) + "00"
    return body + "%02d" % (98 - int(num) % 97)


def lei_ok(code):
    num = "".join(str(int(ch, 36)) for ch in code)
    return len(code) == 20 and int(num) % 97 == 1


def _stems(rng, n):
    seen, out = set(), []
    while len(out) < n:
        s = rng.choice(_ON) + rng.choice(_VW) + rng.choice(_MID) + rng.choice(_V2) + rng.choice(_TL)
        s = s[0].upper() + s[1:]
        bad = any(s.lower().count(ch * 2) for ch in "aeioulrnmvdtsk") or s.lower().endswith(("ae", "ie", "oe"))
        if 5 <= len(s) <= 11 and s not in seen and not bad:
            seen.add(s)
            out.append(s)
    return out


def trading_name(stem, ind, country, rng):
    if rng.random() < 0.18:
        return _GROUP.get(country, _GROUP[""]).format(s=stem)
    nouns = _NOUN[ind]
    return "%s %s" % (stem, nouns.get(country, nouns[""]))


class World:
    pass


def _date(rng, y, lo=0.0, hi=1.0):
    """A business day inside calendar year y, between fractions lo and hi of the year."""
    start = dt.date(y, 1, 1)
    d = start + dt.timedelta(days=int(lo * 364 + rng.random() * (hi - lo) * 364))
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    if d.year != y:
        d = dt.date(y, 12, 30)
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
    return d


def simulate(seed=SEED, am=AM, ak=AK, ah=AH, nh=NH):
    rng = np.random.default_rng(seed)
    W = World()
    W.seed, W.am, W.ak, W.ah = seed, am, ak, ah
    years = list(range(Y0, Y1 + 1))
    W.M = {y: MACRO[y] for y in years}
    W.I = {(k, y): float(rng.standard_normal()) for k in range(NI) for y in years}
    W.houses, W.funds = [], []
    for h in range(nh):
        spec = sorted(rng.choice(NI, size=int(rng.integers(3, 7)), replace=False).tolist())
        W.houses.append(dict(id=h, spec=spec, funds=[]))
        v = int(rng.integers(Y0 - 9, Y0 + 2))
        n = 1 + int(rng.integers(0, 3))
        while v <= Y1 - 1:
            f = dict(id=len(W.funds), house=h, vint=v, num=n, size=int(rng.integers(*FUND_SIZE)), spec=spec)
            W.funds.append(f)
            W.houses[h]["funds"].append(f["id"])
            v += 5 if rng.random() < 0.7 else 4
            n += 1
    W.F = {}
    W.comps, W.loans, W.deals = [], [], []
    owner, alive = {}, set()
    W.cy = []   # company-year at risk: (comp, year, fund, industry, rating, age, defaulted)

    def new_loan(c, f, d, purpose, rating, buy_date):
        L = dict(id=len(W.loans), comp=c, fund=f, orig=d, purpose=purpose, rating=rating, buy=buy_date,
                 end=None, status="open", covered=bool(rng.random() < COVERAGE),
                 size=float(np.round(np.exp(rng.normal(np.log(16.0), 0.55)), 1)))
        W.loans.append(L)
        W.comps[c]["loan"] = L["id"]
        W.comps[c]["loans"].append(L["id"])
        return L

    for y in years:
        for hh in W.houses:
            W.F[(hh["id"], y)] = float(rng.standard_normal())
        # 1. defaults for companies held since before this year
        for c in sorted(alive):
            C = W.comps[c]
            if C["buy_year"] >= y:
                continue
            age = y - C["buy_year"]
            h = BASE[C["rating"]] * SEAS[min(age, len(SEAS) - 1)]
            x = (np.sqrt(am) * W.M[y] + np.sqrt(ak) * W.I[(C["ind"], y)]
                 + np.sqrt(ah) * W.F[(W.funds[owner[c]]["house"], y)]
                 + np.sqrt(1 - am - ak - ah) * rng.standard_normal())
            dflt = bool(x < norm.ppf(h))
            W.cy.append((c, y, owner[c], C["ind"], C["rating"], age, int(dflt)))
            if dflt:
                L = W.loans[C["loan"]]
                L["end"] = _date(rng, y)
                L["status"] = "default"
                alive.discard(c)
                C["default"] = L["end"]
                W.deals.append(dict(kind="default", comp=c, seller=owner[c], buyer=None, date=L["end"]))
        # 2. sales of companies held three years or more
        forsale = []
        for c in sorted(alive):
            C = W.comps[c]
            age = y - C["buy_year"]
            fund = W.funds[owner[c]]
            last = y >= fund["vint"] + 11
            if age >= EXIT_FROM_AGE and (rng.random() < EXIT_P or last):
                forsale.append(c)
        rng.shuffle(forsale)
        # 3. buys by funds in their investment period: secondaries from the sale list, else primaries
        buyers = []
        for f in W.funds:
            if f["vint"] <= y < f["vint"] + 5:
                buyers += [f["id"]] * int(rng.poisson(f["size"] / 5.0))
        rng.shuffle(buyers)
        sold = set()
        for fid in buyers:
            f = W.funds[fid]
            cands = [c for c in forsale if c not in sold and W.funds[owner[c]]["house"] != f["house"]]
            if cands and rng.random() < SECONDARY_P:
                c = cands[int(rng.integers(len(cands)))]
                sold.add(c)
                old = owner[c]
                d = _date(rng, y, 0.05, 0.95)
                L = W.loans[W.comps[c]["loan"]]
                L["end"], L["status"] = d, "repaid"
                W.deals.append(dict(kind="secondary", comp=c, seller=old, buyer=fid, date=d))
                kind = "SBO"
            else:
                k = int(rng.choice(f["spec"])) if rng.random() < 0.8 else int(rng.integers(NI))
                c = len(W.comps)
                cc = int(rng.choice(len(COUNTRIES), p=[p for _, _, p in COUNTRIES]))
                W.comps.append(dict(id=c, ind=k, first=y, default=None, country=COUNTRIES[cc][0],
                                    ccy=COUNTRIES[cc][1], loans=[], spells=[]))
                alive.add(c)
                d = _date(rng, y, 0.05, 0.95)
                W.deals.append(dict(kind="primary", comp=c, seller=None, buyer=fid, date=d))
                kind = "LBO"
            owner[c] = fid
            C = W.comps[c]
            C["buy_year"], C["buy_date"], C["owner"] = y, d, fid
            C["spells"].append(dict(fund=fid, start=d))
            C["rating"] = int(rng.choice(4, p=RATING_MIX))
            new_loan(c, fid, d, kind, C["rating"], d)
        # 4. the rest of the sale list goes to trade buyers or the market
        for c in forsale:
            if c in sold:
                continue
            d = _date(rng, y, 0.05, 0.95)
            L = W.loans[W.comps[c]["loan"]]
            L["end"], L["status"] = d, "repaid"
            W.deals.append(dict(kind="exit", comp=c, seller=owner[c], buyer=None, date=d,
                                exit_type="IPO" if rng.random() < 0.12 else "Trade sale"))
            alive.discard(c)
            W.comps[c]["exited"] = d
        # 5. refinancings two to four years into a hold
        for c in sorted(alive):
            C = W.comps[c]
            age = y - C["buy_year"]
            if 2 <= age <= 4 and rng.random() < REFI_P and c not in sold:
                L = W.loans[C["loan"]]
                lo = 0.05
                if L["orig"].year == y:
                    lo = max(lo, L["orig"].timetuple().tm_yday / 365.0 + 0.02)
                if lo >= 0.95:
                    continue
                d = _date(rng, y, lo, 0.97)
                if d <= L["orig"]:
                    continue
                L["end"], L["status"] = d, "repaid"
                r = int(np.clip(C["rating"] + rng.choice([-1, 0, 0, 0, 1]), 0, 3))
                C["rating"] = r
                new_loan(c, owner[c], d, "Refinancing", r, C["buy_date"])
    W.owner, W.alive = owner, alive
    W.cy = np.array(W.cy, dtype=np.int64)
    _dress(W, rng)
    _workouts(W, rng)
    W.X, W.Y = _portfolios(W, np.random.default_rng(seed + 1))
    return W


def _dress(W, rng):
    """Names, identifiers and loan terms: what the systems would print about each house, fund, company and loan."""
    combos = [(p, s) for p in _PRE for s in _SUF]
    order = rng.permutation(len(combos))
    used = set()
    for hh in W.houses:
        for i in order:
            p, s = combos[i]
            stem = p + s
            if stem not in used and not stem.startswith(("Kestrel", "Ost")):
                used.add(stem)
                break
        hh["stem"] = stem
        hh["name"] = stem + " " + _TAIL[int(rng.integers(len(_TAIL)))]
        hh["vehicle"] = ["LP", "SCSp", "SCA SICAV-RAIF", "LP"][int(rng.integers(4))]
    for f in W.funds:
        hh = W.houses[f["house"]]
        f["name"] = "%s Fund %s" % (hh["name"], _ROMAN[min(f["num"] - 1, len(_ROMAN) - 1)])
        f["roman"] = _ROMAN[min(f["num"] - 1, len(_ROMAN) - 1)]
    stems = _stems(rng, len(W.comps))
    for C, s in zip(W.comps, stems):
        C["stem"] = s
        C["trading"] = trading_name(s, C["ind"], C["country"], rng)
        C["lei"] = lei(rng)
        form = _FORM.get(C["country"], ["Holding"])[int(rng.integers(len(_FORM.get(C["country"], ["Holding"]))))]
        suffix = form.split()[-1]
        C["legal"] = "%s %s" % (C["trading"], suffix) if not C["trading"].endswith(suffix) else C["trading"]
    for L in W.loans:
        C = W.comps[L["comp"]]
        L["obligor"], L["obligor_lei"] = C["legal"], C["lei"]
        L["ccy"] = C["ccy"]
        L["amount_ccy"] = round(L["size"] * FX[C["ccy"]], 1)
        L["margin"] = int(round((500 + 65 * L["rating"] + rng.normal(0, 35)) / 5.0) * 5)
        L["tenor"] = int(rng.choice([6, 7, 7]))
        mat = dt.date(L["orig"].year + L["tenor"], L["orig"].month, min(L["orig"].day, 28))
        live_to = L["end"] if L["end"] is not None else AS_OF
        if mat <= live_to:
            mat = dt.date(live_to.year + int(rng.integers(1, 4)), L["orig"].month, min(L["orig"].day, 28))
        L["maturity"] = mat
        L["facility"] = "Unitranche" if rng.random() < 0.7 else "Senior term loan"


def _workouts(W, rng):
    for L in W.loans:
        if L["status"] != "default":
            continue
        d = float(rng.gamma(WO_SHAPE, WO_SCALE))
        r = float(np.clip(REC_A - REC_B * d + rng.normal(0, REC_SD), 0.0, 1.0))
        L["wo_years"], L["recovery"] = d, r
        L["resolved"] = L["end"] + dt.timedelta(days=int(round(d * 365.25)))
        L["resolution"] = ("Restructuring" if r > 0.55 else "Sale of business" if r > 0.3 else "Liquidation")


def _quota(cands, n, mix, W, rng):
    want = np.round(np.array(mix) * n).astype(int)
    want[1] += n - want.sum()
    byr = collections.defaultdict(list)
    for c in cands:
        byr[W.comps[c]["rating"]].append(c)
    out = []
    for r in range(4):
        pool = byr[r][:]
        rng.shuffle(pool)
        out += pool[:want[r]]
    if len(out) < n:
        chosen = set(out)
        rest = [c for c in cands if c not in chosen]
        rng.shuffle(rest)
        out += rest[:n - len(out)]
    return out


def _portfolios(W, rng, nXh=5, perh=19, nY=100, maxYh=3, core_n=5, yhouses=42,
                mixX=(0.32, 0.50, 0.17, 0.01), mixY=(0.22, 0.48, 0.25, 0.05)):
    """Kestrel Lane lends to six houses' companies across their funds; Ostvale lends in its five sectors across many
    houses. Each list holds the companies whose current loan sits in the manager's static portfolio."""
    alive = sorted(W.alive)
    own = W.owner
    byh = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in alive:
        byh[W.funds[own[c]]["house"]][own[c]].append(c)
    cand = sorted(h for h, fs in byh.items() if sum(1 for f in fs.values() if len(f) >= 4) >= 2
                  and sum(len(f) for f in fs.values()) >= perh + 4)
    # the houses whose companies carry the better ratings: Kestrel Lane lends to its sponsors' stronger credits
    def quality(h):
        cs = [c for f in byh[h] for c in byh[h][f]]
        return np.mean([W.comps[c]["rating"] for c in cs])
    rng.shuffle(cand)
    cand = sorted(cand, key=quality)[:max(nXh, int(len(cand) * 0.4))]
    rng.shuffle(cand)
    chosen = sorted(cand[:nXh])
    X = []
    for h in chosen:
        allc = sorted(c for f in byh[h] for c in byh[h][f])
        X += _quota(allc, perh, mixX, W, rng)
    cnt = collections.Counter(W.comps[c]["ind"] for c in alive)
    core = sorted(k for k, _ in cnt.most_common(core_n))
    pool = [c for c in alive if W.funds[own[c]]["house"] not in chosen and W.comps[c]["ind"] in core]
    hp = collections.defaultdict(list)
    for c in pool:
        hp[W.funds[own[c]]["house"]].append(c)
    hl = sorted(hp)
    rng.shuffle(hl)
    Yc = []
    for h in hl:
        cs = hp[h][:]
        rng.shuffle(cs)
        fc, got = collections.Counter(), []
        for c in cs:
            if fc[own[c]] >= maxYh:
                continue
            got.append(c)
            fc[own[c]] += 1
            if len(got) == maxYh:
                break
        Yc += got
        if len(set(W.funds[own[c]]["house"] for c in Yc)) >= yhouses and len(Yc) >= int(1.3 * nY):
            break
    Y = _quota(Yc, nY, mixY, W, rng)
    W.core = core
    W.X_houses = chosen
    return X, Y


if __name__ == "__main__":
    W = simulate()
    st = collections.Counter(L["status"] for L in W.loans)
    print("houses", len(W.houses), "funds", len(W.funds), "companies", len(W.comps), "loans", len(W.loans), dict(st),
          "alive", len(W.alive), "X", len(W.X), "Y", len(W.Y))
    for nm, P in (("X", W.X), ("Y", W.Y)):
        print(nm, "houses", len(set(W.funds[W.owner[c]]["house"] for c in P)), "funds", len(set(W.owner[c] for c in P)),
              "industries", len(set(W.comps[c]["ind"] for c in P)),
              "ratings", np.bincount([W.comps[c]["rating"] for c in P], minlength=4))
    print([W.houses[h]["name"] for h in W.X_houses])
    print(W.comps[5]["trading"], "|", W.comps[5]["legal"], "|", W.comps[5]["lei"], lei_ok(W.comps[5]["lei"]))
