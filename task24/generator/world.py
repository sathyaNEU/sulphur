"""task24 world: Pellucid Annotation's April to October 2026 operations and its five Q1 2027 requests, simulated from
the process that writes each record (the labelling tool's passes, QA's reviews, the punch clock, payroll, the video
delivery archive, the clients' sample labels). Nothing here is written to carry an answer: every graded quantity is
computed later from the records this module returns."""
import datetime as dt
import math

import numpy as np
import pandas as pd

SEED = 240611
WEEK0 = dt.date(2026, 4, 6)          # first Monday of the extract
NWEEKS = 30                           # to Sunday 2026-11-01
PULL = dt.date(2026, 11, 6)

CENTRES = {
    "KSM": dict(name="Kisumu", utc=3, floor=2.40, lunch_min=45, n_ann=17, n_rev=6, rev_rate=3.30, allowance=3.50,
                holidays=[dt.date(2026, 4, 6), dt.date(2026, 5, 1), dt.date(2026, 6, 1), dt.date(2026, 10, 10),
                          dt.date(2026, 10, 20)]),
    "ILO": dict(name="Iloilo", utc=8, floor=2.70, lunch_min=60, n_ann=13, n_rev=4, rev_rate=3.65, allowance=4.00,
                holidays=[dt.date(2026, 4, 9), dt.date(2026, 5, 1), dt.date(2026, 6, 12), dt.date(2026, 8, 21),
                          dt.date(2026, 8, 31)]),
}
RATES = dict(box=0.0128, polygon=0.0330, track=0.0260, frame=0.0075)
OVERHEAD_PER_PAID_HOUR = 1.55
MARGIN = 1.18
# the clients' offered prices (USD per image; per frame for the video request), as their requests state them
OFFERED = dict(A=6.46, B=5.45, C=0.0390, D=1.78, E=0.42)

# per-object first-pass seconds for the average annotator (the truth the records are drawn from)
T_BOX = {"S": 12.4, "M": 8.6, "L": 6.1}
OCC_T = 1.52
T_IMAGE = 11.0
P_MISS = {"S": 0.0118, "M": 0.0046, "L": 0.0021}
OCC_P = 3.0
P_MISPLACE = 0.0016
DETECT = 0.92
SLIP2 = 0.70            # slips on a correction's re-check of every object, relative to first-pass miss chances
FIX_BASE, FIX_PER_OBJ = 38.0, 3.0
REV_BASE, REV_PER_OBJ = 14.0, 3.6
POLY_BASE, POLY_PER_VERTEX = 15.0, 1.15
V_FRAME, V_FOBJ, V_BIRTH, V_DEATH, V_CHUNK = 3.0, 0.10, 17.0, 6.0, 10.0
V_PMISS = 0.016
CHUNK = 25

# 2026 projects: code, client, kind, scene, start week, end week, weight, object model
# object model for stills: (mean objects, NB size k, share small, share medium, occlusion rate)
# polygons: (mean polygons, k, mean vertices, occlusion); video: (mean on screen, births per frame, sequences)
PROJECTS = [
    ("P26-0412", "Tarnwell Auto", "box", "street", 0, 12, 0.7, (14, 6, 0.30, 0.45, 0.22)),
    ("P26-0417", "Vantorra Mobility", "box", "street", 2, 15, 1.1, (19, 6, 0.32, 0.43, 0.28)),
    ("P26-0423", "Halsey Robotics", "box", "street", 6, 20, 0.9, (24, 7, 0.34, 0.42, 0.31)),
    ("P26-0431", "Tarnwell Auto", "box", "street", 9, 24, 1.0, (29, 7, 0.36, 0.41, 0.33)),
    ("P26-0446", "Vantorra Mobility", "box", "street", 14, 26, 0.6, (44, 8, 0.38, 0.40, 0.38)),
    ("P26-0458", "Ilvane Vision", "box", "street", 18, 29, 0.5, (57, 8, 0.39, 0.40, 0.40)),
    ("P26-0414", "Shelfgrid Retail", "box", "retail", 0, 11, 0.9, (22, 9, 0.44, 0.42, 0.06)),
    ("P26-0427", "Quaymart Analytics", "box", "retail", 5, 18, 0.9, (28, 9, 0.45, 0.42, 0.07)),
    ("P26-0439", "Shelfgrid Retail", "box", "retail", 11, 23, 0.8, (34, 10, 0.47, 0.41, 0.07)),
    ("P26-0452", "Brightaisle", "box", "retail", 16, 29, 0.35, (52, 10, 0.49, 0.40, 0.09)),
    ("P26-0409", "Kestrin Warehousing", "box", "warehouse", 0, 14, 0.45, (8, 5, 0.06, 0.36, 0.05)),
    ("P26-0436", "Lodestar 3PL", "box", "warehouse", 10, 22, 0.4, (11, 5, 0.08, 0.38, 0.06)),
    ("P26-0449", "Kestrin Warehousing", "box", "warehouse", 15, 29, 0.4, (14, 5, 0.09, 0.40, 0.07)),
    ("P26-0419", "Skyhatch Survey", "box", "aerial", 3, 17, 0.7, (38, 6, 0.66, 0.29, 0.08)),
    ("P26-0441", "Skyhatch Survey", "box", "aerial", 12, 27, 0.6, (47, 6, 0.68, 0.27, 0.10)),
    ("P26-0425", "Homefront Devices", "box", "indoor", 4, 16, 0.35, (7, 4, 0.14, 0.43, 0.18)),
    ("P26-0444", "Homefront Devices", "box", "indoor", 13, 25, 0.3, (10, 4, 0.16, 0.44, 0.20)),
    ("P26-0429", "Verdance Agritech", "box", "agriculture", 6, 19, 0.7, (31, 6, 0.58, 0.34, 0.36)),
    ("P26-0455", "Verdance Agritech", "box", "agriculture", 17, 29, 0.6, (46, 7, 0.61, 0.32, 0.39)),
    ("P26-0421", "Metrovale Transit", "box", "traffic", 3, 13, 0.35, (12, 5, 0.25, 0.45, 0.14)),
    ("P26-0448", "Metrovale Transit", "box", "traffic", 15, 28, 0.35, (17, 5, 0.27, 0.45, 0.16)),
    ("P26-0416", "Brindle Pallet Systems", "polygon", "pallet", 1, 13, 0.6, (9, 5, 10.5, 0.12)),
    ("P26-0433", "Ostrava Components", "polygon", "industrial", 8, 21, 0.5, (6, 4, 19.0, 0.08)),
    ("P26-0442", "Brindle Pallet Systems", "polygon", "pallet", 12, 25, 0.6, (12, 5, 12.5, 0.15)),
    ("P26-0451", "Plancast", "polygon", "floorplan", 16, 29, 0.4, (15, 6, 7.0, 0.04)),
    ("P26-0418", "Junction Labs", "video", "urban", 2, 14, 0.6, (16, 0.72, 0.25)),
    ("P26-0438", "Junction Labs", "video", "urban", 11, 24, 0.5, (19, 0.80, 0.25)),
    ("P26-0428", "Promenade AI", "video", "plaza", 6, 18, 0.5, (24, 1.05, 0.25)),
    ("P26-0434", "Parkline Systems", "video", "parking", 9, 22, 0.2, (29, 0.045, 0.25)),
    ("P26-0457", "Harbourline Freight", "video", "dock", 18, 29, 0.4, (10, 0.12, 0.25)),
    ("P26-0426", "Tillcount Retail", "video", "store", 5, 17, 0.4, (7, 0.22, 0.25)),
]

# Q1 2027 requests (the decision); offered prices are set in the RFQs (docs.py), from the clients' own budgets
REQUESTS = {
    "A": dict(client="Vantorra Mobility", kind="box", scene="street", volume=2000, model=(125, 9, 0.42, 0.40, 0.55)),
    "B": dict(client="Shelfgrid Retail", kind="box", scene="retail", volume=6000, model=(106, 12, 0.58, 0.36, 0.09)),
    "C": dict(client="Ardley Autonomy", kind="video", scene="highway", volume=60000, model=(27, 0.26, 0.25)),
    "D": dict(client="Brindle Pallet Systems", kind="polygon", scene="pallet", volume=4000, model=(15, 5, 42.0, 0.18)),
    "E": dict(client="Kestrin Warehousing", kind="box", scene="warehouse", volume=20000, model=(12, 5, 0.07, 0.36, 0.05)),
}


def rng_for(*keys):
    h = SEED
    for k in keys:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % (2 ** 32)
    return np.random.default_rng(h)


# ---------------------------------------------------------------- people
def make_people():
    rng = rng_for("people")
    rows, revs = [], []
    serial = {"KSM": 4100, "ILO": 7300}
    for c, cfg in CENTRES.items():
        for i in range(cfg["n_ann"]):
            serial[c] += int(rng.integers(3, 41))
            hire = WEEK0 - dt.timedelta(days=int(rng.integers(40, 1400)))
            late = rng.random() < 0.12
            if late:
                hire = WEEK0 + dt.timedelta(days=int(rng.integers(10, 150)))
            left = None
            if rng.random() < 0.09:
                left = WEEK0 + dt.timedelta(days=int(rng.integers(60, 200)))
            zs, zc = rng.normal(), rng.normal()
            speed = math.exp(0.33 * zs)                     # > 1 is slower
            care = math.exp(0.30 * zc + 0.25 * 0.33 * zs)   # faster annotators slip a little more
            sched = int(rng.choice([30, 36, 40, 40, 40, 44], p=[0.10, 0.15, 0.25, 0.20, 0.15, 0.15]))
            skills = ["box"] + (["polygon"] if rng.random() < 0.45 else []) + (["video"] if rng.random() < 0.40 else [])
            rows.append(dict(annotator_id="%s-A%05d" % (c, serial[c]), centre=c, hire_date=hire, left_date=left,
                             scheduled_hours=sched, skills=skills, speed=speed, care=care,
                             productive=float(np.clip(rng.normal(0.835, 0.025), 0.76, 0.90)),
                             week_sd=float(np.clip(rng.normal(0.07, 0.015), 0.03, 0.12))))
        for i in range(cfg["n_rev"]):
            revs.append(dict(reviewer_id="%s-Q%04d" % (c, int(rng.integers(100, 9999))), centre=c,
                             speed=math.exp(rng.normal(0, 0.12)), scheduled_hours=40,
                             productive=float(np.clip(rng.normal(0.74, 0.03), 0.66, 0.82))))
    return pd.DataFrame(rows), pd.DataFrame(revs)


# ---------------------------------------------------------------- items
def draw_still(rng, model, n, clarity=1.0):
    m, k, ps, pm, occ = model
    cnt = rng.negative_binomial(k, k / (k + m), size=n)
    cnt = np.maximum(cnt, 1)
    small = rng.binomial(cnt, ps)
    med = rng.binomial(cnt - small, pm / max(1e-9, 1 - ps))
    large = cnt - small - med
    out = {}
    for name, arr in (("S", small), ("M", med), ("L", large)):
        o = rng.binomial(arr, occ)
        out["n_%s_occ" % name] = o
        out["n_%s_clr" % name] = arr - o
    return pd.DataFrame(out)


def draw_polygon(rng, model, n):
    m, k, v, occ = model
    cnt = np.maximum(rng.negative_binomial(k, k / (k + m), size=n), 1)
    occn = rng.binomial(cnt, occ)
    verts = np.array([rng.poisson(v, c).clip(3).sum() for c in cnt])
    return pd.DataFrame(dict(n_poly=cnt, n_poly_occ=occn, vertices=verts))


def still_seconds(df, speed, rng):
    base = T_IMAGE
    for s in "SML":
        base = base + T_BOX[s] * (df["n_%s_clr" % s] + OCC_T * df["n_%s_occ" % s])
    return base.to_numpy() * speed * np.exp(rng.normal(0, 0.17, len(df)))


def still_misses(df, care, rng, factor=1.0):
    miss = np.zeros(len(df), int)
    for s in "SML":
        for o, mult in (("clr", 1.0), ("occ", OCC_P)):
            p = np.minimum(P_MISS[s] * mult * care * factor, 0.9)
            miss += rng.binomial(df["n_%s_%s" % (s, o)].to_numpy(), p)
    return miss


def n_objects(df):
    return sum(df["n_%s_%s" % (s, o)] for s in "SML" for o in ("clr", "occ")).to_numpy()


def poly_seconds(df, speed, rng):
    t = T_IMAGE + POLY_BASE * df["n_poly"] + POLY_PER_VERTEX * df["vertices"] + 0.30 * POLY_BASE * df["n_poly_occ"]
    return t.to_numpy() * speed * np.exp(rng.normal(0, 0.17, len(df)))


def poly_misses(df, care, rng, factor=1.0):
    p1 = np.minimum(0.0040 * care * factor, 0.9)
    p2 = np.minimum(0.0040 * 2.5 * care * factor, 0.9)
    return rng.binomial((df["n_poly"] - df["n_poly_occ"]).to_numpy(), p1) + rng.binomial(df["n_poly_occ"].to_numpy(), p2)


def make_sequences(rng, model, nseq, frames_lo=180, frames_hi=420):
    """Video sequences frame by frame: tracks are born and end; the archive keeps one row per track."""
    stock, birth, _ = model
    tracks, chunks = [], []
    for q in range(nseq):
        F = int(rng.integers(frames_lo, frames_hi))
        life = stock / max(birth, 1e-3)                       # mean frames a track lasts at steady state
        alive = []
        start_n = rng.poisson(stock)
        tid = 0
        for _ in range(start_n):
            alive.append([tid, 0, int(rng.geometric(1 / life))]); tid += 1
        per_frame = np.zeros(F, int); births = np.zeros(F, int); deaths = np.zeros(F, int)
        rate = birth * math.exp(rng.normal(0, 0.25))
        for f in range(F):
            nb = rng.poisson(rate)
            for _ in range(nb):
                alive.append([tid, f, f + int(rng.geometric(1 / life))]); tid += 1
                births[f] += 1
            keep = []
            for tr in alive:
                if tr[2] <= f:
                    deaths[f] += 1
                    tracks.append((q, tr[0], tr[1], f - 1))
                else:
                    keep.append(tr)
            alive = keep
            per_frame[f] = len(alive)
        for tr in alive:
            tracks.append((q, tr[0], tr[1], F - 1))
        births[0] += start_n
        for c0 in range(0, F, CHUNK):
            c1 = min(F, c0 + CHUNK)
            chunks.append(dict(seq=q, frame_from=c0, frame_to=c1 - 1, frames=c1 - c0,
                               frame_objects=int(per_frame[c0:c1].sum()), births=int(births[c0:c1].sum()),
                               deaths=int(deaths[c0:c1].sum())))
    tr = pd.DataFrame(tracks, columns=["seq", "track", "first_frame", "last_frame"])
    return tr, pd.DataFrame(chunks)


def chunk_seconds(ch, speed, rng):
    t = V_CHUNK + V_FRAME * ch["frames"] + V_FOBJ * ch["frame_objects"] + V_BIRTH * ch["births"] + V_DEATH * ch["deaths"]
    return t.to_numpy() * speed * np.exp(rng.normal(0, 0.17, len(ch)))


# ---------------------------------------------------------------- the year: rota, passes, reviews
def simulate():
    ann, rev = make_people()
    rng = rng_for("year")
    proj = pd.DataFrame(PROJECTS, columns=["project", "client", "kind", "scene", "w0", "w1", "weight", "model"])
    proj["clarity"] = np.exp(rng_for("clarity").normal(0, 0.12, len(proj)))
    # video projects get their sequences up front (the archive keeps one row per track)
    vtracks, vchunks = [], []
    for _, p in proj[proj.kind == "video"].iterrows():
        r = rng_for("seq", p.project)
        nseq = {"parking": 60, "dock": 150}.get(p.scene, 260)
        tr, ch = make_sequences(r, p.model, nseq)
        tr["project"] = p.project; ch["project"] = p.project
        vtracks.append(tr); vchunks.append(ch)
    vtracks = pd.concat(vtracks, ignore_index=True); vchunks = pd.concat(vchunks, ignore_index=True)
    vchunks["chunk_key"] = range(len(vchunks))
    vqueue = {p: list(g.chunk_key) for p, g in vchunks.groupby("project")}

    revarr = {c: (g.reviewer_id.to_numpy(), g.speed.to_numpy()) for c, g in rev.groupby("centre")}
    vfo = vchunks.frame_objects.to_numpy()
    passes, reviews, weeks = [], [], []
    pass_serial = 5_100_000
    item_serial = {}
    carry = {}
    for w in range(NWEEKS):
        monday = WEEK0 + dt.timedelta(days=7 * w)
        active = proj[(proj.w0 <= w) & (proj.w1 >= w)]
        for _, a in ann.iterrows():
            if a.hire_date > monday + dt.timedelta(days=4) or (a.left_date is not None and a.left_date < monday):
                continue
            r = rng_for("ww", a.annotator_id, w)
            cfg = CENTRES[a.centre]
            days = [monday + dt.timedelta(days=d) for d in range(5)]
            workdays = [d for d in days if d not in cfg["holidays"] and d >= a.hire_date and
                        (a.left_date is None or d <= a.left_date) and r.random() > 0.045]
            if not workdays:
                continue
            paid = a.scheduled_hours / 5.0 * len(workdays) * float(np.clip(r.normal(1.0, 0.03), 0.9, 1.08))
            tenure_w = max(0.0, (monday - a.hire_date).days / 7.0)
            learn = 1.0 + 0.22 * math.exp(-tenure_w / 4.0)
            wk_speed = a.speed * learn * math.exp(r.normal(0, a.week_sd))
            capacity = paid * 3600 * a.productive
            skills = a.skills
            cand = active[active.kind.isin(skills)]
            if len(cand) == 0:
                continue
            pr = cand.iloc[r.choice(len(cand), p=(cand.weight / cand.weight.sum()).to_numpy())]
            used = 0.0
            queue = carry.pop(a.annotator_id, [])
            # draw this week's new items in one block, more than can be done
            if pr.kind == "video":
                keys = vqueue[pr.project][:400]
                vqueue[pr.project] = vqueue[pr.project][400:] + vqueue[pr.project][:0]
                if not keys:
                    continue
                items = vchunks.iloc[keys].reset_index(drop=True)
                t1 = chunk_seconds(items, wk_speed, r)
                miss1 = r.binomial(items.births.to_numpy(), np.minimum(V_PMISS * a.care * pr.clarity, 0.9))
                nobj = items.births.to_numpy() + 0
            elif pr.kind == "polygon":
                items = draw_polygon(r, pr.model, 900)
                t1 = poly_seconds(items, wk_speed, r)
                miss1 = poly_misses(items, a.care * pr.clarity, r)
                nobj = items.n_poly.to_numpy()
            else:
                items = draw_still(r, pr.model, 1600)
                t1 = still_seconds(items, wk_speed, r)
                miss1 = still_misses(items, a.care * pr.clarity, r)
                nobj = n_objects(items)
            mis1 = r.binomial(nobj, P_MISPLACE * (2 if pr.kind == "polygon" else 1))
            icols = {c: items[c].to_numpy() for c in items.columns if c.startswith("n_") or c == "vertices"}
            ckeys = items.chunk_key.to_numpy() if pr.kind == "video" else None
            done = []
            # first carried corrections, then new items
            for qd in queue:
                used += qd["sec"]
                done.append(qd)
            for i in range(len(items)):
                if used >= capacity:
                    break
                used += t1[i]
                done.append(dict(kind=pr.kind, project=pr.project, idx=i, pass_no=1, sec=float(t1[i]),
                                 miss=int(miss1[i]), mis=int(mis1[i]), nobj=int(nobj[i])))
            weeks.append(dict(annotator_id=a.annotator_id, centre=a.centre, week=w, monday=monday, workdays=workdays,
                              paid_hours=paid, active_seconds=used, project=pr.project))
            # realise every pass's review and the correction chain; corrections that do not fit carry over
            for d in done:
                d["annotator_id"] = a.annotator_id; d["week"] = w
                if d["pass_no"] == 1:
                    key = (d["project"], d["idx"], w, a.annotator_id)
                    item_serial[key] = len(item_serial)
                    d["item"] = item_serial[key]
                    if d["kind"] == "video":
                        d["chunk_key"] = int(ckeys[d["idx"]])
                        d["counts"] = None
                    else:
                        d["counts"] = {c: int(icols[c][d["idx"]]) for c in icols}
                passes.append(d)
            # reviews and corrections (simulated per pass: found issues return the item)
            new_carry = []
            for d in done:
                found_m = r.binomial(d["miss"], DETECT)
                found_p = r.binomial(d["mis"], DETECT)
                ids, sps = revarr[a.centre]
                j = int(r.integers(0, len(ids)))
                rv_id, rv_sp = ids[j], sps[j]
                if d["kind"] == "video":
                    rsec = (20 + 0.6 * d["nobj"] + 0.012 * vfo[d["chunk_key"]]) * rv_sp
                else:
                    rsec = (REV_BASE + REV_PER_OBJ * d["nobj"] * (1.15 if d["kind"] == "polygon" else 1.0)) * rv_sp
                rsec *= math.exp(r.normal(0, 0.2))
                reviews.append(dict(item=d["item"], pass_no=d["pass_no"], reviewer_id=rv_id,
                                    centre=a.centre, seconds=float(rsec), found_missed=int(found_m),
                                    found_misplaced=int(found_p), week=w))
                if found_m + found_p > 0 and d["pass_no"] < 4:
                    # correction: re-check every object, redraw the found misses; residual and new slips
                    left_m = d["miss"] - found_m
                    if d["kind"] == "video":
                        fix = (25 + 0.04 * vfo[d["chunk_key"]] + V_BIRTH * found_m) * wk_speed
                        slip = r.binomial(d["nobj"], min(V_PMISS * SLIP2 * a.care, 0.9))
                    elif d["kind"] == "polygon":
                        fix = (FIX_BASE + 3.0 * d["nobj"] + POLY_BASE * found_m) * wk_speed
                        slip = r.binomial(d["nobj"], min(0.004 * SLIP2 * a.care * 1.4, 0.9))
                    else:
                        cts = d["counts"]
                        fix = (FIX_BASE + FIX_PER_OBJ * d["nobj"] + 9.0 * found_m + 6.0 * found_p) * wk_speed
                        slip = 0
                        for s in "SML":
                            for o, mult in (("clr", 1.0), ("occ", OCC_P)):
                                slip += r.binomial(int(cts["n_%s_%s" % (s, o)]), min(P_MISS[s] * mult * a.care * SLIP2, 0.9))
                    fix *= math.exp(r.normal(0, 0.2))
                    nd = dict(kind=d["kind"], project=d["project"], idx=d["idx"], pass_no=d["pass_no"] + 1,
                              sec=float(fix), miss=int(left_m // 2 + slip), mis=int(r.binomial(d["nobj"], P_MISPLACE * 0.3)),
                              nobj=d["nobj"], item=d["item"], counts=d.get("counts"), chunk_key=d.get("chunk_key"))
                    if used + fix <= capacity * 1.02:
                        used += fix
                        nd["annotator_id"] = a.annotator_id; nd["week"] = w
                        passes.append(nd)
                        done.append(nd)          # its own review follows in this loop
                    else:
                        new_carry.append(nd)
            weeks[-1]["active_seconds"] = used
            if new_carry:
                carry[a.annotator_id] = new_carry
    return dict(ann=ann, rev=rev, proj=proj, passes=passes, reviews=reviews, weeks=weeks, vtracks=vtracks,
                vchunks=vchunks)


# ---------------------------------------------------------------- the requests' sample labels
def request_samples():
    out = {}
    for key, rq in REQUESTS.items():
        r = rng_for("request", key)
        if rq["kind"] == "box":
            out[key] = draw_still(r, rq["model"], 400)
        elif rq["kind"] == "polygon":
            out[key] = draw_polygon(r, rq["model"], 400)
        else:
            tr, ch = make_sequences(r, rq["model"], 12, 280, 320)
            out[key] = (tr, ch)
    return out


if __name__ == "__main__":
    import time
    t = time.time()
    W = simulate()
    print("seconds", round(time.time() - t, 1), "passes", len(W["passes"]), "reviews", len(W["reviews"]),
          "worker-weeks", len(W["weeks"]), "tracks", len(W["vtracks"]), "chunks", len(W["vchunks"]))
