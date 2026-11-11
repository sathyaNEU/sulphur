"""The world's records as the organisations' systems hold them, before any export's own form (layouts, encodings,
re-runs) is applied: the WMS labour log, the payroll's rows, the forecast archive, Huippu Sport's order exports, the
item master, the 2027 slotting, the own pickers' roster and the pilot's pick confirmations."""
import datetime as dt

import numpy as np
import pandas as pd

import cal
import params as P
import sim

ZH_COLS = ["date", "hour", "zone", "pickers_logged", "logged_min", "task_min", "idle_min", "lines", "units",
           "lines_cls_a", "lines_cls_b", "lines_cls_c", "lines_cls_d", "lines_cls_f", "lines_store", "lines_hui"]

ROSTER_NAMES = ["Kristian Uusitalo", "Henrik Salmi", "Mikko Vesterinen", "Petteri Vuorinen", "Niko Huttunen",
                "Henry Halonen", "Pekka Kärkkäinen", "Tapio Peltonen", "Harri Karjalainen", "Johannes Johansson",
                "Marika Sutinen", "Liisa Airaksinen", "Sofia Heiskanen", "Ensio Honkanen", "Antero Niemi",
                "Emilia Saarinen", "Anni Laakso", "Maria Mäkelä", "Sisko Koponen", "Marjatta Hämäläinen",
                "Sinikka Paananen", "Raija Lehtinen", "Jan Järvenpää", "Teemu Kokkonen", "Timo Hakala",
                "Anneli Laine", "Esteri Holopainen", "Heidi Kettunen", "Petri Kokko", "Eveliina Ylinen",
                "Pirjo Aaltonen", "Tanja Tanskanen", "Marko Kallio", "Marita Sainio", "Jukka Moilanen",
                "Janne Savolainen", "Minna Silvennoinen", "Inkeri Virtanen"]


def zone_hours(w):
    return pd.DataFrame(w["zone_hours"], columns=ZH_COLS)


def timesheets(w):
    return pd.DataFrame(w["timesheets"], columns=["date", "person", "employer", "zone", "shift", "start", "end", "paid",
                                                  "absence", "absence_hours"])


def forecasts(w):
    f = pd.DataFrame(w["forecasts"], columns=["issued", "round", "brand", "group", "iso_year", "iso_week",
                                              "order_lines"])
    f["order_lines"] = f["order_lines"].round(0).astype(int)
    f["note"] = ""
    for (brand, y), m in w["fmeta"].items():
        gs, gb = m["g"]
        txt = "Budget %d: commercial plan +%d %% small parts, +%d %% bulky" % (y, round(gs * 100), round(gb * 100))
        sel = f.index[(f["round"] == "budget %d" % y) & (f["brand"] == brand) & (f["issued"] == m["issue"])]
        f.loc[sel[0], "note"] = txt
        if "reissue" in m:
            sel = f.index[(f["round"] == "budget %d" % y) & (f["brand"] == brand) & (f["issued"] == m["reissue"])]
            f.loc[sel[0], "note"] = "Bulky re-issued after the furniture range review"
    return f


def k_orders(w):
    """The WMS's order import for Kotikaari by day received: web orders and lines by group, the showrooms' lines."""
    D = w["D"]
    rows = []
    rng = np.random.default_rng(P.SEED + 3)
    for i, d in enumerate(D["days"]):
        if d < P.DATA_START - dt.timedelta(days=3) or d > P.DATA_END:
            continue
        for grp, kw, ks, lpo in (("small parts", "web_s", "store_s", 1.74), ("bulky", "web_b", "store_b", 1.12)):
            web = int(D[kw][i])
            store = int(D[ks][i]) if d.weekday() < 5 and cal.working(d) else 0
            rows.append((d, grp, int(round(web / (lpo * float(np.exp(rng.normal(0, 0.03)))))), web, store))
    return pd.DataFrame(rows, columns=["received", "group", "web_orders", "web_lines", "store_lines"])


def h_daily(w):
    return pd.DataFrame(w["h_daily"], columns=["order_date", "group", "orders", "order_lines", "units"])


def h_monthly(w):
    return pd.DataFrame(w["h_monthly"], columns=["month", "article_no", "order_lines", "units"])


K_GROUPS = [
    # name, zone, articles, class shares (A, B, C, D, F)
    ("Tyynynpäälliset ja liinat", "P2", 760, (0.92, 0.08, 0.0, 0.0, 0.0)),
    ("Pyyhkeet ja kylpytekstiilit", "P2", 540, (0.85, 0.15, 0.0, 0.0, 0.0)),
    ("Torkkupeitot ja päiväpeitot", "P2", 300, (0.55, 0.40, 0.05, 0.0, 0.0)),
    ("Kynttilät ja tuoksut", "P2", 420, (0.10, 0.80, 0.10, 0.0, 0.0)),
    ("Sisustustarvikkeet", "P2", 640, (0.25, 0.50, 0.18, 0.04, 0.03)),
    ("Astiat ja kattaus", "P1", 820, (0.05, 0.30, 0.30, 0.05, 0.30)),
    ("Lasit ja karahvit", "P1", 360, (0.0, 0.10, 0.20, 0.0, 0.70)),
    ("Keittiötarvikkeet", "P1", 780, (0.20, 0.50, 0.25, 0.05, 0.0)),
    ("Kattilat ja pannut", "P1", 300, (0.0, 0.05, 0.75, 0.20, 0.0)),
    ("Säilytys ja korit", "P1", 520, (0.10, 0.35, 0.45, 0.10, 0.0)),
    ("Valaisimet, pienet", "P1", 260, (0.0, 0.20, 0.50, 0.10, 0.20)),
    ("Huonekalut", "B1", 260, (0.0, 0.0, 0.10, 0.90, 0.0)),
    ("Matot", "B1", 210, (0.0, 0.0, 0.20, 0.80, 0.0)),
    ("Valaisimet, suuret", "B1", 130, (0.0, 0.0, 0.25, 0.75, 0.0)),
]

WORDS = {
    "Tyynynpäälliset ja liinat": (["Tyynynpäällinen", "Pöytäliina", "Kaitaliina", "Servetti"], ["pellava", "puuvilla", "sametti"]),
    "Pyyhkeet ja kylpytekstiilit": (["Kylpypyyhe", "Käsipyyhe", "Saunapyyhe", "Kylpytakki"], ["frotee", "vohveli", "luomupuuvilla"]),
    "Torkkupeitot ja päiväpeitot": (["Torkkupeitto", "Päiväpeitto", "Viltti"], ["villa", "puuvilla", "akryyli"]),
    "Kynttilät ja tuoksut": (["Pöytäkynttilä", "Tuikkukynttilä", "Tuoksukynttilä", "Huonetuoksu"], ["soija", "parafiini", "steariini"]),
    "Sisustustarvikkeet": (["Maljakko", "Kehys", "Peili", "Koriste", "Ruukku"], ["keramiikka", "lasi", "messinki", "puu"]),
    "Astiat ja kattaus": (["Lautanen", "Kulho", "Muki", "Tarjoiluvati", "Kahvikuppi"], ["posliini", "kivitavara", "keramiikka"]),
    "Lasit ja karahvit": (["Juomalasi", "Viinilasi", "Karahvi", "Kannu"], ["lasi", "kristalli"]),
    "Keittiötarvikkeet": (["Leikkuulauta", "Kauha", "Siivilä", "Veitsi", "Mittasarja"], ["puu", "teräs", "silikoni"]),
    "Kattilat ja pannut": (["Kattila", "Paistinpannu", "Kasari", "Uunivuoka"], ["valurauta", "teräs", "alumiini"]),
    "Säilytys ja korit": (["Säilytyslaatikko", "Kori", "Purkki", "Hylly"], ["paju", "muovi", "puu", "metalli"]),
    "Valaisimet, pienet": (["Pöytävalaisin", "Lyhty", "Valosarja"], ["metalli", "lasi", "rottinki"]),
    "Huonekalut": (["Sivupöytä", "Jakkara", "Penkki", "Hylly"], ["tammi", "koivu", "metalli"]),
    "Matot": (["Matto", "Käytävämatto", "Ovimatto"], ["villa", "juutti", "puuvilla"]),
    "Valaisimet, suuret": (["Lattiavalaisin", "Riippuvalaisin"], ["metalli", "rottinki", "lasi"]),
}
H_WORDS = {
    "Paidat ja t-paidat": ["T-paita", "Treenipaita", "Pitkähihainen paita", "Juoksupaita"],
    "Housut ja trikoot": ["Trikoot", "Shortsit", "Treenihousut", "Collegehousut"],
    "Sukat ja alusvaatteet": ["Juoksusukat", "Urheiluliivit", "Bokserit", "Villasukat"],
    "Takit": ["Kuoritakki", "Juoksutakki", "Untuvatakki", "Liivi"],
    "Pipot, käsineet ja huivit": ["Pipo", "Juoksukäsineet", "Tuubihuivi", "Lapaset"],
    "Juoksukengät": ["Juoksukengät", "Polkujuoksukengät", "Kävelykengät"],
    "Talvikengät ja saappaat": ["Talvikengät", "Kumisaappaat", "Vaelluskengät"],
    "Sandaalit": ["Sandaalit", "Varvassandaalit"],
    "Laukut ja reput": ["Reppu", "Juoksuvyö", "Treenikassi"],
    "Juomapullot ja pienvarusteet": ["Juomapullo", "Otsalamppu", "Heijastinliivi", "Sauvakärjet"],
    "Kypärät ja suojat": ["Pyöräilykypärä", "Laskettelukypärä", "Polvisuojat"],
    "Lasit ja kellot": ["Urheilulasit", "Laskettelulasit", "Sykemittari"],
    "Pallot ja välineet": ["Jalkapallo", "Salibandymaila", "Jumppakuminauha"],
    "Sukset ja sauvat": ["Murtomaasukset", "Sauvat", "Lumikengät"],
    "Pyöräily": ["Pyöräteline", "Trainer-vastus", "Pyörälaukku"],
    "Kuntoilulaitteet": ["Kahvakuula", "Jumppamatto", "Levypainosarja"],
}
COLOURS = ["musta", "valkoinen", "harmaa", "beige", "sininen", "vihreä", "punainen", "luonnonvalkoinen", "ruskea"]
SIZES = ["XS", "S", "M", "L", "XL"]
DIMS = {"A": ((22, 32), (16, 24), (2, 6), (0.1, 0.6)), "B": ((18, 30), (12, 22), (8, 14), (0.3, 1.4)),
        "C": ((28, 40), (20, 30), (12, 22), (0.8, 3.5)), "D": ((45, 120), (30, 70), (20, 60), (3.0, 22.0)),
        "F": ((15, 30), (12, 25), (10, 25), (0.4, 2.5))}


def _dims(rng, cls):
    (l0, l1), (w0, w1), (h0, h1), (m0, m1) = DIMS[cls]
    return (round(float(rng.uniform(l0, l1)), 1), round(float(rng.uniform(w0, w1)), 1),
            round(float(rng.uniform(h0, h1)), 1), round(float(rng.uniform(m0, m1)), 2))


def item_master(w, rng):
    rows = []
    no = 2104300
    for name, zone, n, shares in K_GROUPS:
        nouns, mats = WORDS[name]
        for _ in range(n):
            no += int(rng.integers(1, 12))
            cls = P.CLASSES[int(rng.choice(5, p=np.array(shares) / sum(shares)))]
            L, W_, H, kg = _dims(rng, cls)
            desc = "%s %s %s" % (rng.choice(nouns), rng.choice(mats), rng.choice(COLOURS))
            if rng.random() < 0.35:
                desc += " %dx%d" % (int(L), int(W_))
            created = dt.date(2021, 3, 1) + dt.timedelta(days=int(rng.integers(0, 2000)))
            rows.append(("K%07d" % no, "KOT", "%06d" % (no - 1800000), desc, name, cls, kg, L, W_, H, zone,
                         min(created, dt.date(2026, 10, 30))))
    pilot = set(w["pilot"])
    hno = 5301200
    for x in w["arts"]:
        hno += int(rng.integers(1, 7))
        g = sim.H_GROUPS[x["group"]][0]
        L, W_, H, kg = _dims(rng, x["cls"])
        desc = "%s %s" % (rng.choice(H_WORDS[g]), rng.choice(COLOURS))
        if x["cls"] == "A" and rng.random() < 0.7:
            desc += " %s" % rng.choice(SIZES)
        if x["cls"] in ("C", "D") and g in ("Juoksukengät", "Talvikengät ja saappaat", "Sandaalit"):
            desc += " %d" % int(rng.integers(36, 47))
        zone = "P2" if x["article"] in pilot else ""
        created = dt.date(2026, 8, int(rng.integers(10, 29))) if x["article"] in pilot else \
            dt.date(2026, 10, int(rng.integers(5, 30)))
        rows.append(("H%07d" % hno, "HUI", x["article"], desc, g, x["cls"], kg, L, W_, H, zone, created))
    return pd.DataFrame(rows, columns=["sku", "owner", "owner_article", "description", "product_group",
                                       "handling_class", "unit_weight_kg", "length_cm", "width_cm", "height_cm",
                                       "pick_zone", "created"])


def slotting(w, im, rng):
    h = im[im["owner"] == "HUI"].copy()
    zmap = {x["article"]: x["zone27"] for x in w["arts"]}
    vel = {x["article"]: x["vel"] * sim.h_group_season(12)[x["group"]] for x in w["arts"]}
    h["zone"] = h["owner_article"].map(zmap)
    h["v"] = h["owner_article"].map(vel)
    out = []
    for z in P.ZONES:
        r = h[h["zone"] == z].sort_values("v", ascending=False)
        n = len(r)
        for i, (_, x) in enumerate(r.iterrows()):
            q = i / max(1, n - 1)
            aisle = 1 + int(min(P.AISLES[z] - 1, q * P.AISLES[z] + rng.normal(0, 0.6)))
            aisle = max(1, aisle)
            bay = int(rng.integers(1, 25))
            level = int(rng.choice([1, 2, 2, 3, 3, 4, 5])) if z != "B1" else int(rng.choice([0, 0, 1, 2]))
            vc = "A" if q < 0.2 else ("B" if q < 0.5 else "C")
            out.append((x["owner_article"], x["sku"], z, aisle, bay, level, vc))
    return pd.DataFrame(out, columns=["owner_article", "sku", "zone", "aisle", "bay", "level", "velocity_class"])


def roster(w, rng):
    """HR's list of own pickers for 2027: everyone on the books on 1 November 2026 with the agreed hires."""
    staff = [x for x in w["staff"] if x["end"] is None]
    hires = [("P1", dt.date(2027, 2, 15)), ("P1", dt.date(2027, 2, 15)), ("P2", dt.date(2027, 2, 15))]
    no = max(x["emp"] for x in w["staff"])
    rows = []
    names = list(ROSTER_NAMES)
    order = rng.permutation(len(names))
    k = 0
    for x in sorted(staff, key=lambda s: s["emp"]):
        rows.append((x["emp"], names[order[k]], x["zone"], 40, x["start"], ""))
        k += 1
    for z, st in hires:
        no += int(rng.integers(5, 30))
        rows.append((no, names[order[k]], z, 40, st, ""))
        k += 1
    df = pd.DataFrame(rows, columns=["employee_no", "name", "home_zone", "contract_hours_week", "employment_start",
                                     "leave_until"])
    # one picker on parental leave over the 2027 peak
    j = int(rng.integers(0, len(df) - 3))
    df.loc[j, "leave_until"] = "2028-01-09"
    return df


def pilot_conf(w, rng):
    rows = []
    sku_of = None
    tid = 88412000
    for (tm, d, h, art, u) in w["pilot_conf"]:
        tid += int(rng.integers(1, 4))
        rows.append((tm, tid, art, u))
    return rows
