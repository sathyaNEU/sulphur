"""task15: the world. Banyena Grain Genetics' barley breeding programme, 2014 to 2025, simulated plot by plot the
way the programme runs, and the independent High Rainfall Barley Series its lines are nominated to.

Nothing here is written for a result. Each line has a yield level, a response to season water and a straw
strength; each trial has its season's water, its fertility and its lodging pressure; plots carry block and field
trend and plot error; badly lodged plots are sometimes left unharvested; the breeder advances lines each year on
that year's raw trial means and nominates three Stage 3 lines a year on an index of her own. The series grows the
nominees beside the benchmark and other breeders' entries, harvests everything and publishes site means.

build(seed) returns the clean truth as plain arrays and dicts. pack.py writes the files, golden.py analyses them.
"""
import math

import numpy as np

SEED = 3153
FIRST, LAST = 2014, 2025
SOW = LAST + 1                 # the sowing year the next nominations are for
OLD_LAST = FIRST + 4           # the old plot logger's last season; the harvest system took over the season after
WIDE_FROM = FIRST + 3          # the season the wider plot seeder came in
FIRST_SOW = FIRST + 3          # the first sowing year Banyena nominated for (its first Stage 3 season was FIRST + 2)
STANDARD = 107.0               # Mount Rouse's uptake standard (option deed, schedule 2, clause 2.1)

# the pack's files, named the way each system or author names them
FILES = dict(
    old="PlotHarvest_%d_%d.csv" % (FIRST, OLD_LAST),
    new="plot_harvest_%d_%d.csv" % (OLD_LAST + 1, LAST),
    entries="trial_entry_lists_%d_%d.csv" % (FIRST, LAST),
    trials="trials_%d_%d.csv" % (FIRST, LAST),
    rain="site_rainfall_monthly_%d_%d.csv" % (FIRST, LAST),
    irrigation="kerang_irrigation_%d_%d.csv" % (FIRST, LAST),
    sites="trial_sites.xlsx",
    register="line_register.xlsx",
    nominations="hrbs_nominations_%d_%d.xlsx" % (FIRST_SOW, LAST),
    results="HRBS_site_results_%d_%d.csv" % (FIRST, LAST),
    seasons="HRBS_site_seasons_%d_%d.csv" % (FIRST, LAST),
    quality="grain_quality_stage3_%d_%d.csv" % (LAST - 2, LAST),
    disease="disease_nursery_scores_%d_%d.csv" % (LAST - 2, LAST),
    seed="seed_store_inventory_%d-02.xlsx" % SOW,
    protocol="HRBS_trial_protocol_%d.pdf" % (LAST - 2),
    deed="option_deed_schedule_2.pdf",
    handbook="BGG_trial_handbook_%d.pdf" % (LAST - 1),
    review="season_review_%d.docx" % LAST,
)

PARAM = dict(
    # how many lines a year enter each stage: the intake follows the crossing block and the seed on hand, the
    # advancements follow the season review, so no two years are the same size (low, high exclusive)
    n_s1=(268, 337), n_s2=(63, 84), n_s3_new=(17, 25), n_s3_keep=(8, 13), n_nom=3,
    series_entries=(26, 36),   # entries in a series season, the standards included
    p_site_lost=0.035,         # a series trial lost before harvest (waterlogging, hail, establishment)
    sd_g=0.25,          # line yield level, t/ha
    sd_b=0.13,          # line response to season water, t/ha per 100 mm
    gain=0.028,         # genetic gain per cohort year, t/ha
    rho_sg=0.30,        # weaker straw goes with a higher dryland yield level
    sd_ge=0.08,         # line by trial
    sd_gy=0.0,          # line by season (carried by the water response and lodging)
    family_share=0.40,  # the share of each trait's variance that sister lines have in common
    cv_plot=0.065,
    sd_block=0.11, sd_trend=0.06,
    lodge_loss=0.18,    # t/ha lost per tenth of the plot lodged
    sd_bench_season=0.07,  # the benchmark's own season swing in the series' district, t/ha
)

# name, district, zone, lat, lon, soil, mean April-October rain (mm), irrigated
PROGRAMME_SITES = [
    ("Walpeup", "Mallee", "LRZ", -35.14, 142.02, "calcarosol sandy loam", 188, 0),
    ("Hopetoun", "Mallee", "LRZ", -35.73, 142.37, "calcarosol sandy clay loam", 203, 0),
    ("Manangatang", "Mallee", "LRZ", -35.05, 142.88, "calcarosol sandy loam", 196, 0),
    ("Birchip", "Mallee", "LRZ", -35.98, 142.92, "calcarosol clay loam", 226, 0),
    ("Horsham", "Wimmera", "MRZ", -36.72, 142.17, "grey vertosol", 287, 0),
    ("Minyip", "Wimmera", "MRZ", -36.46, 142.59, "grey vertosol", 274, 0),
    ("Kaniva", "Wimmera", "MRZ", -36.38, 141.24, "sodosol over clay", 318, 0),
    ("Lake Bolac", "Western District", "HRZ", -37.71, 142.84, "chromosol clay loam", 362, 0),
    ("Skipton", "Western District", "HRZ", -37.68, 143.36, "sodosol loam", 394, 0),
    ("Kerang", "Northern irrigation", "MRZ", -35.73, 143.92, "red-brown earth", 214, 1),
]
S1_SITES = ["Horsham", "Birchip"]
S2_SITES = ["Walpeup", "Hopetoun", "Minyip", "Kaniva", "Lake Bolac"]
S3_SITES = [s[0] for s in PROGRAMME_SITES]
INDEX_SITES = ["Lake Bolac", "Skipton", "Kerang"]

SERIES_SITES = [
    ("Westmere", "Western District", -37.69, 142.97, "chromosol clay loam", 452),
    ("Streatham", "Western District", -37.68, 143.06, "chromosol loam", 446),
    ("Dunkeld", "Southern Grampians", -37.65, 142.34, "sodosol loam", 471),
    ("Derrinallum", "Western District", -37.95, 143.22, "ferrosol clay loam", 468),
    ("Hamilton", "Southern Grampians", -37.74, 142.02, "chromosol silty loam", 497),
    ("Casterton", "Glenelg", -37.59, 141.40, "sodosol sandy loam", 519),
    ("Mortlake", "Moyne", -38.08, 142.81, "ferrosol clay loam", 536),
    ("Penshurst", "Southern Grampians", -37.87, 142.29, "ferrosol clay", 542),
    ("Branxholme", "Southern Grampians", -37.86, 141.80, "chromosol loam", 561),
    ("Macarthur", "Moyne", -38.03, 142.00, "ferrosol clay loam", 583),
]

BENCH = "Byaduk"
CHECKS = ["Byaduk", "Wando", "Carapook", "Nareen"]          # in every programme trial
SERIES_STANDARDS = ["Byaduk", "Wando", "Carapook"]           # in every series trial
CHECK_TRAITS = {  # yield level, water response, straw weakness (0 strong to 1 weak)
    "Byaduk": (0.12, 0.125, 0.30),
    "Wando": (0.02, -0.05, 0.50),
    "Carapook": (-0.05, 0.08, 0.38),
    "Nareen": (0.05, -0.12, 0.62),
}
MONTH_SHARE = np.array([0.105, 0.150, 0.160, 0.165, 0.160, 0.140, 0.120])   # April to October


def abandon_p(L):
    """The chance a plot is left unharvested, by how much of it has lodged (L in tenths of the plot)."""
    return float(np.interp(L, [0.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], [0.0, 0.0, 0.06, 0.18, 0.36, 0.56, 0.78, 0.92]))


SITE_ABANDON = {"Kerang": 1.0, "Lake Bolac": 0.9, "Skipton": 0.6, "Kaniva": 0.8, "Horsham": 0.7, "Minyip": 0.7}
OTHER_BREEDERS = [("Glenelg Plant Breeding", "GPB"), ("Otway Cereals", "OC"), ("Corangamite Seeds", "CS"),
                  ("Limestone Coast Genetics", "LCG"), ("Tasman Barley", "TB")]


def env_mean(W):
    """Trial mean yield against season water (t/ha): a rising, flattening response."""
    return 8.6 * (1.0 - math.exp(-(W - 80.0) / 380.0))


def _rng(seed, *key):
    return np.random.default_rng([seed, *key])


def build(seed=SEED, P=None):
    P = dict(PARAM, **(P or {}))
    years = list(range(FIRST, LAST + 1))
    r = _rng(seed, 1)
    yfac = {y: float(np.exp(r.normal(0, 0.22))) for y in years}

    # ---- environments: one per site and season
    env = {}
    for (name, district, zone, lat, lon, soil, gsr, irr) in PROGRAMME_SITES:
        fert = r.normal(0, 0.22)
        for y in years:
            rr = _rng(seed, 2, hash_name(name), y)
            rain = gsr * yfac[y] * math.exp(rr.normal(0, 0.10))
            months = np.round(rain * dirichlet_about(rr, MONTH_SHARE, 38.0), 1)
            offseason = np.round(rr.gamma(4.0, 9.0, size=5) * (gsr / 250.0), 1)
            events = []
            if irr:
                n = int(rr.integers(4, 7))
                tot = rr.uniform(165, 255)
                sh = dirichlet_about(rr, np.ones(n) / n, 20.0)
                doy = np.sort(rr.choice(np.arange(225, 300), size=n, replace=False))
                events = [(int(d), round(float(tot * s), 0)) for d, s in zip(doy, sh)]
            W = float(months.sum() + sum(mm for _, mm in events))
            e = dict(site=name, zone=zone, season=y, kind="programme", months=months, offseason=offseason,
                     irrigation=events, W=W, x=(W - 350.0) / 100.0)
            e["mu"] = max(0.75, env_mean(W) + fert + rr.normal(0, 0.28) + (0.20 if irr else 0.0))
            e["pi"] = float(np.clip((W - 300.0) / 190.0, 0.0, 1.3) * max(0.45, rr.normal(1.0, 0.15)))
            e["cv"] = float(np.clip(rr.normal(P["cv_plot"], 0.012), 0.055, 0.125))
            env[(name, y)] = e
    bench_swing = {y: float(_rng(seed, 3, y).normal(0, P["sd_bench_season"])) for y in years}
    for (name, district, lat, lon, soil, gsr) in SERIES_SITES:
        fert = r.normal(0, 0.20)
        for y in years:
            rr = _rng(seed, 4, hash_name(name), y)
            rain = gsr * (yfac[y] ** 0.7) * math.exp(rr.normal(0, 0.09))
            months = np.round(rain * dirichlet_about(rr, MONTH_SHARE, 45.0), 1)
            W = float(round(float(months.sum())))        # the series prints April to October rain to the millimetre
            e = dict(site=name, zone="HRZ", season=y, kind="series", months=months, irrigation=[], W=W,
                     x=(W - 350.0) / 100.0)
            e["mu"] = max(2.5, env_mean(W) + fert + rr.normal(0, 0.26))
            e["pi"] = float(np.clip((W - 300.0) / 190.0, 0.0, 1.3) * max(0.45, rr.normal(1.0, 0.15)))
            e["cv"] = float(np.clip(rr.normal(P["cv_plot"] - 0.01, 0.010), 0.05, 0.11))
            env[(name, y)] = e

    # ---- lines
    lines = {}
    order = []

    def add_line(lid, cohort, g, b, s, kind):
        lines[lid] = dict(id=lid, cohort=cohort, g=float(g), b=float(b), s=float(s), kind=kind, wi=None,
                          gy={})
        order.append(lid)

    for c, (g, b, s) in CHECK_TRAITS.items():
        add_line(c, 0, g, b, s, "check")

    def draw_traits(rr, mean_g, mean_b=0.0, mean_s=0.44, sd_s=0.19, sd_g=None, sd_b=None, fam=None):
        """A line's yield level, water response and straw weakness. Sister lines share their cross's part of each
        (fam: three standard normal draws for the cross), so a good cross gives several good lines."""
        z = rr.normal(size=3)
        if fam is not None:
            k = P["family_share"]
            z = math.sqrt(k) * np.asarray(fam) + math.sqrt(1 - k) * z
        g = mean_g + (sd_g or P["sd_g"]) * z[0]
        b = mean_b + (sd_b or P["sd_b"]) * z[1]
        zs = P["rho_sg"] * z[0] + math.sqrt(1 - P["rho_sg"] ** 2) * z[2]
        s = float(np.clip(mean_s + sd_s * zs, 0.05, 0.95))
        return g, b, s

    def gy(lid, y):
        d = lines[lid]["gy"]
        if y not in d:
            d[y] = float(_rng(seed, 5, hash_name(lid), y).normal(0, P["sd_gy"]))
        return d[y]

    plots = []        # programme plots, one tuple each
    trials = {}       # code -> dict
    rel = {}          # (line, trial) -> breeder's raw per cent of the benchmark

    def run_trial(code, site, y, stage, entries, reps, series=False):
        e = env[(site, y)]
        rr = _rng(seed, 6, hash_name(code))
        n_chk = 2 if not series else 1
        chk = SERIES_STANDARDS if series else CHECKS
        ent = list(entries) + [c for c in chk for _ in range(n_chk)]
        entry_no = {}
        base = list(entries) + list(chk)
        perm = rr.permutation(len(entries))
        numbered = [entries[k] for k in perm] + list(chk)
        for k, lid in enumerate(numbered, 1):
            entry_no[lid] = k
        n = len(ent)
        ncol = 12 if n >= 48 else (8 if n >= 24 else 6)
        blk_size = ncol
        ge = {lid: rr.normal(0, P["sd_ge"]) for lid in base}
        rows = []
        plot_no = 0
        tr_slope = rr.normal(0, P["sd_trend"]) * e["mu"] / 4.5
        for rep in range(1, reps + 1):
            seq = rr.permutation(n)
            nblk = int(math.ceil(n / float(blk_size)))
            beff = rr.normal(0, P["sd_block"] * e["mu"] / 4.5, size=nblk)
            for pos, idx in enumerate(seq):
                lid = ent[idx]
                t = lines[lid]
                blk = pos // blk_size
                rng_ = blk + 1 + (rep - 1) * nblk       # field range (a strip across the trial)
                col = pos % blk_size + 1
                plot_no = rng_ * 100 + col
                lat = 10.0 * t["s"] * e["pi"] * math.exp(rr.normal(-0.045, 0.30))
                L = float(np.clip(np.rint(lat * 2.0) / 2.0, 0.0, 10.0))     # tenths of the plot lodged, to the nearest 5 per cent
                swing = bench_swing[y] if (series and lid == BENCH) else 0.0
                yv = (e["mu"] + t["g"] + t["b"] * e["x"] + gy(lid, y) + ge[lid] + beff[blk]
                      + tr_slope * (col - (blk_size + 1) / 2.0) / blk_size + swing
                      - P["lodge_loss"] * L + rr.normal(0, e["cv"] * e["mu"]))
                yv = round(max(0.15, yv), 3)            # the harvest system stores kilograms per hectare
                pa = 0.0 if series else abandon_p(L) * SITE_ABANDON.get(site, 0.6)
                ab = bool(rr.random() < pa)
                rows.append((code, plot_no, rep, blk + 1 + (rep - 1) * nblk, rng_, col, entry_no[lid], lid,
                             float(yv), L, ab))
        trials[code] = dict(code=code, site=site, season=y, stage=stage, reps=reps, ncol=ncol,
                            entry_no=entry_no, n_entries=len(base), series=series)
        return rows

    def breeder_rel(rows):
        """The breeder's own figure: a line's mean harvested yield as a percentage of the benchmark's, per trial."""
        acc = {}
        for (code, _, _, _, _, _, _, lid, yv, L, ab) in rows:
            if not ab:
                acc.setdefault(lid, []).append(yv)
        b = float(np.mean(acc[BENCH]))
        return {lid: 100.0 * float(np.mean(v)) / b for lid, v in acc.items()}

    stage_sets, s3_seasons = {}, {}
    nominations = {}      # sowing year -> list of dicts
    nominated = set()
    advanced = []         # (season, from stage, line)
    cross_no = {}

    def trial_code(stage, y, site):
        ab = {"Walpeup": "WAL", "Hopetoun": "HOP", "Manangatang": "MAN", "Birchip": "BIR", "Horsham": "HOR",
              "Minyip": "MIN", "Kaniva": "KAN", "Lake Bolac": "LBO", "Skipton": "SKI", "Kerang": "KER"}[site]
        return "%02d%s%s" % (y % 100, stage, ab)

    wi_next = 3100 + int(_rng(seed, 7).integers(0, 40))
    sizes = {}
    for y in years:
        rr = _rng(seed, 8, y)
        n_s1, n_s2 = int(rr.integers(*P["n_s1"])), int(rr.integers(*P["n_s2"]))
        n_new3, n_keep3 = int(rr.integers(*P["n_s3_new"])), int(rr.integers(*P["n_s3_keep"]))
        sizes[y] = dict(s1=n_s1, to_s2=n_s2, to_s3=n_new3, kept=n_keep3)
        # the year's new lines come from about forty crosses, a few sister lines each
        new, cno = [], 100 + int(rr.integers(0, 30))
        while len(new) < n_s1:
            cno += int(rr.integers(1, 6))
            k = int(rr.integers(3, 13))
            fam = rr.normal(size=3)
            for sib in rr.choice(np.arange(1, 40), size=k, replace=False):
                if len(new) >= n_s1:
                    break
                lid = "%02dX%03d-%02d" % (y % 100, cno, int(sib))
                if lid in lines:
                    continue
                g, b, s = draw_traits(_rng(seed, 9, hash_name(lid)), P["gain"] * (y - FIRST), fam=fam)
                add_line(lid, y, g, b, s, "line")
                new.append(lid)
        stage_sets[("S1", y)] = new
        season_rel = {}
        for stage, sites, reps in (("S1", S1_SITES, 2), ("S2", S2_SITES, 2), ("S3", S3_SITES, 3)):
            ents = stage_sets.get((stage, y), [])
            if not ents:
                continue
            for site in sites:
                code = trial_code(stage, y, site)
                rows = run_trial(code, site, y, stage, ents, reps)
                plots.extend(rows)
                rr_ = breeder_rel(rows)
                for lid in ents:
                    rel[(lid, code)] = rr_.get(lid, float("nan"))
                    season_rel.setdefault((stage, lid), []).append(rr_.get(lid, float("nan")))
            if stage == "S3":
                for lid in ents:
                    s3_seasons.setdefault(lid, []).append(y)

        def score(stage, lid):
            return float(np.nanmean(season_rel[(stage, lid)])) + rr.normal(0, 0.6)

        if ("S1", y) in stage_sets:
            s1 = sorted(stage_sets[("S1", y)], key=lambda l: -score("S1", l))
            stage_sets[("S2", y + 1)] = s1[:n_s2]
            advanced += [(y, "S1", l) for l in s1[:n_s2]]
        new3 = []
        if ("S2", y) in stage_sets:
            s2 = sorted(stage_sets[("S2", y)], key=lambda l: -score("S2", l))
            new3 = s2[:n_new3]
            advanced += [(y, "S2", l) for l in new3]
            for lid in new3:               # a Stage 3 line gets its WI number
                wi_next += int(rr.integers(1, 5))
                lines[lid]["wi"] = "WI%d" % wi_next
        keep3 = []
        if ("S3", y) in stage_sets:
            def index(lid):
                v = [rel[(lid, trial_code("S3", yy, s))] for yy in s3_seasons[lid] for s in INDEX_SITES]
                v = [a for a in v if a == a]
                return float(np.mean(v)) if v else float("nan")
            cands = [l for l in stage_sets[("S3", y)] if l not in nominated]
            noms = []
            if y < LAST:
                ranked = sorted(cands, key=lambda l: -index(l))
                noms = ranked[:P["n_nom"]]
                nominations[y + 1] = [dict(line=l, index=index(l), s3=list(s3_seasons[l])) for l in noms]
                nominated.update(noms)
            first_year = [l for l in cands if len(s3_seasons[l]) == 1 and l not in noms]
            keep3 = sorted(first_year, key=lambda l: -score("S3", l))[:n_keep3]
            advanced += [(y, "S3", l) for l in keep3]
        if new3 or keep3:
            stage_sets[("S3", y + 1)] = new3 + keep3

    # ---- the series: nominees for two seasons beside the standards and other breeders' entries
    series_rows, series_entries = [], {}
    carry = []
    for y in years:
        rr = _rng(seed, 10, y)
        ours = [d["line"] for yy in (y, y - 1) for d in nominations.get(yy, [])]
        others = [l for (l, last) in carry if last >= y]
        carry = [(l, last) for (l, last) in carry if last >= y]
        n_new = int(rr.integers(*P["series_entries"])) - len(ours) - len(others) - len(SERIES_STANDARDS)
        for k in range(max(0, n_new)):
            br, pre = OTHER_BREEDERS[int(rr.integers(0, len(OTHER_BREEDERS)))]
            lid = "%s%02d-%03d" % (pre, y % 100, int(rr.integers(100, 990)))
            if lid in lines:
                continue
            g, b, s = draw_traits(_rng(seed, 11, hash_name(lid)), 0.10 + 0.012 * (y - FIRST), mean_b=0.10,
                                  mean_s=0.36, sd_s=0.15, sd_g=0.20, sd_b=0.09)
            add_line(lid, -1, g, b, s, "other")
            lines[lid]["breeder"] = br
            dur = int(rr.choice([1, 2, 2, 2, 3, 4]))
            carry.append((lid, y + dur - 1))
            others.append(lid)
        ents = ours + others
        series_entries[y] = ents
        # now and then a trial is lost before harvest (waterlogging, hail, a failed establishment)
        lost = {name for (name, *_r) in SERIES_SITES if rr.random() < P["p_site_lost"]}
        for (name, *_rest) in SERIES_SITES:
            if name in lost:
                continue
            code = "HRBS%02d-%s" % (y % 100, name[:3].upper())
            rows = run_trial(code, name, y, "HRBS", ents, 3, series=True)
            series_rows.extend(rows)
        trials_lost = lost
        series_entries[(y, "lost")] = sorted(trials_lost)

    # the series publishes each entry's site mean (two decimals), its mean lodging (one decimal) and the trial's cv
    acc = {}
    for (code, plot_no, rep, blk, rng_, col, eno, lid, yv, L, ab) in series_rows:
        acc.setdefault((code, lid), []).append((yv, L))
    series_cells, by_trial = [], {}
    for (code, lid), v in acc.items():
        ys = np.array([a for a, _ in v])
        row = dict(trial=code, site=trials[code]["site"], season=trials[code]["season"], line=lid, plots=len(v),
                   y=round(float(ys.mean()), 2), L=round(float(np.mean([b for _, b in v])) * 10.0, 1) / 10.0,
                   sd=float(ys.std(ddof=1)) if len(v) > 1 else 0.0)
        series_cells.append(row)
        by_trial.setdefault(code, []).append(row)
    series_trials = {}
    for code, rows_ in by_trial.items():
        m = float(np.mean([r_["y"] for r_ in rows_]))
        sd = math.sqrt(float(np.mean([r_["sd"] ** 2 for r_ in rows_])))
        e = env[(trials[code]["site"], trials[code]["season"])]
        series_trials[code] = dict(site=trials[code]["site"], season=trials[code]["season"], mean=round(m, 2),
                                   cv=round(100.0 * sd / m, 1), rain=int(e["W"]))

    return dict(seed=seed, P=P, years=years, yfac=yfac, env=env, lines=lines, order=order, plots=plots,
                series_cells=series_cells, series_trials=series_trials,
                trials=trials, rel=rel, stage_sets=stage_sets, s3_seasons=s3_seasons, nominations=nominations,
                advanced=advanced, series_rows=series_rows, series_entries=series_entries,
                bench_swing=bench_swing, sizes=sizes)


def hash_name(s):
    """A stable small integer for a name (python's own hash is salted per process)."""
    h = 2166136261
    for ch in str(s).encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return int(h)


def dirichlet_about(rr, share, conc):
    a = np.asarray(share, float) * conc
    return rr.dirichlet(a)
