"""task24 independent verifier. Reads only target/ and the golden files, never the generator's modules, and recomputes
every graded figure on its own code path: the policies' values from the PDFs' own text (pdftotext), R1 from the pay
register read cell by cell with the punch clock re-run under the pay policy, the samples' counts from the JSON, the
video tasks' tracks from the archive by SQL, the issue intensities by EM, the time models by bounded least squares,
the floor top-up by Gauss-Hermite quadrature over each annotator's week-to-week spread (the golden simulates it), each
request's cost and the call, the 2026 projects' actuals and costing, and the golden workbook and note against
figures.json.

    python3 verify.py      # exit 1 on any FAIL
"""
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import lsq_linear

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TG = os.path.join(TASK, "target")
GDIR = os.path.join(TASK, "golden")
FG = json.load(open(os.path.join(HERE, "figures.json")))
BAD = []
W0 = dt.date(2026, 4, 6)
CNT = ["obj_small", "obj_small_occl", "obj_medium", "obj_medium_occl", "obj_large", "obj_large_occl"]
KEY_OF_CLIENT = {"corvane": "A", "shelfgrid": "B", "ardley": "C", "brindle": "D", "kestrin": "E"}
KIND = {"A": "box", "B": "box", "C": "video", "D": "polygon", "E": "box"}
OFFSET_H = {"KSM": 3, "ILO": 8}


def ok(name, cond, detail=""):
    print("%-4s %-78s %s" % ("PASS" if cond else "FAIL", name[:78], detail))
    if not cond:
        BAD.append(name)


def near(a, b, rel, absol=0.0):
    return abs(a - b) <= max(rel * abs(b), absol)


def pdf(name):
    return subprocess.run(["pdftotext", "-layout", os.path.join(TG, name), "-"], capture_output=True, text=True,
                          check=True).stdout


def grab(pat, text):
    m = re.search(pat, text, re.S)
    return float(m.group(1)) if m else float("nan")


def bnnls(X, y):
    return lsq_linear(X, y, bounds=(0, np.inf), method="bvls", tol=1e-12).x


def file_like(prefix):
    return next(n for n in sorted(os.listdir(TG)) if n.startswith(prefix))


# ------------------------------------------------------------------ the filed values, from the documents' own text
pricing, paypol, qastd = pdf(file_like("pricing_policy")), pdf(file_like("annotator_pay_policy")), pdf(file_like("qa_review"))
ok("pdf read-back positive control: each policy's title extracted",
   "Pricing policy for annotation requests" in pricing and "Annotator pay policy 2026" in paypol and "QA review standard" in qastd)
MARGIN = grab(r"at least\s+([\d.]+)\s+times its", pricing)
OVH = grab(r"USD\s+([\d.]+)\s+per\s+paid\s+hour\s+of\s+annotators", pricing)
RATE = dict(box=grab(r"Bounding boxes\s+([\d.]+)\s+per object", paypol),
            polygon=grab(r"Polygon segmentation\s+([\d.]+)\s+per polygon", paypol),
            track=grab(r"Video tracking\s+([\d.]+)\s+per track", paypol), frame=grab(r"per track and\s+([\d.]+)\s+per frame", paypol))
FLOOR = dict(KSM=grab(r"USD\s+([\d.]+)\s+per\s+paid\s+hour\s+at\s+Kisumu", paypol), ILO=grab(r"USD\s+([\d.]+)\s+at\s+Iloilo\.", paypol))
LUNCH = dict(KSM=grab(r"\((\d+)\s+minutes\s+at\s+Kisumu", paypol), ILO=grab(r"(\d+)\s+minutes\s+at\s+Iloilo\)", paypol))
ok("pricing policy files the line (1.18) and the overhead (USD 1.55 per paid hour)",
   MARGIN == FG["margin"] and OVH == FG["overhead_rate"], "%s, %s" % (MARGIN, OVH))
ok("pricing policy files the week's pay shared across projects by tool active time",
   re.search(r"shared\s+across\s+the\s+projects\s+in\s+proportion\s+to\s+the\s+labelling\s+tool's\s+active\s+time", pricing) is not None)
ok("pricing policy files the staffing: roster at the costing date, shares by contracted hours",
   re.search(r"in\s+proportion\s+to\s+their\s+contracted\s+weekly\s+hours", pricing) is not None)
ok("pay policy files four piece rates, two floors and two lunch breaks",
   all(v == v for v in list(RATE.values()) + list(FLOOR.values()) + list(LUNCH.values())), "%s %s %s" % (RATE, FLOOR, LUNCH))
ok("QA standard files the return on any found issue and the fourth review",
   re.search(r"returns\s+a\s+task\s+to\s+its\s+annotator\s+when\s+the\s+review\s+finds\s+any\s+missed\s+object", qastd) is not None
   and re.search(r"After\s+a\s+task's\s+fourth\s+review", qastd) is not None)
PRICE, SAMPLE = {}, {}
for n in sorted(os.listdir(TG)):
    low = n.lower()
    if n.startswith("RFQ_"):
        k = KEY_OF_CLIENT[low.split("_")[1]]
        t = pdf(n)
        PRICE[k] = grab(r"USD\s+([\d.]+)\s+per\s+(?:image|frame),\s+all\s+in", t)
    elif low.endswith(".json") and low.split("_")[0] in KEY_OF_CLIENT:
        SAMPLE[KEY_OF_CLIENT[low.split("_")[0]]] = n
ok("five RFQs read back with their offered prices", sorted(PRICE) == list("ABCDE") and
   all(PRICE[k] == FG["price_%s" % k] for k in PRICE), str(PRICE))

# ------------------------------------------------------------------ the task passes and the QA reviews
P = pd.read_csv(os.path.join(TG, file_like("pellucid_task_passes")), dtype={"parent_pass_id": str})
n_raw = len(P)
P = P[~P.duplicated()]
n_dup = n_raw - len(P)
P = P[P.pass_type != "released"].reset_index(drop=True)
par = dict(zip(P.pass_id, P.parent_pass_id.fillna("")))
depth = np.ones(len(P), int)
cur = P.parent_pass_id.fillna("").to_numpy(object)
while (cur != "").any():
    has = cur != ""
    depth += has
    cur = np.array([par.get(c, "") if c else "" for c in cur], object)
P["depth"] = depth
P["kind"] = np.where(P.frames.notna(), "video", np.where(P.polygons.notna(), "polygon", "box"))
P["week"] = (pd.to_datetime(P.submitted_at.str[:10]) - pd.Timestamp(W0)).dt.days // 7
P["act"] = P.tool_active_s.astype(float)
ok("passes: sync-retry repeats and released tasks set aside", n_dup > 0 and len(P) < n_raw, "%d repeats" % n_dup)

Rv = pd.read_csv(os.path.join(TG, file_like("qa_reviews")))
Rv["rid"] = [x if "-" in x else x[:3] + "-" + x[3:] for x in Rv.reviewer_id]
Rv["site"] = Rv.rid.str[:3]
Rv = Rv[Rv.pass_id.isin(set(P.pass_id))].reset_index(drop=True)
ok("reviews: the Iloilo desk's unhyphenated keys normalised", (Rv.reviewer_id != Rv.rid).sum() > 0 and Rv.rid.str.contains("-").all())

# video tasks: tracks starting and ending in each 25-frame task, by SQL on the archive
mem = sqlite3.connect(":memory:")
src = sqlite3.connect(os.path.join(TG, file_like("video_delivery_archive")))
src.backup(mem)
src.close()
V = P[P.kind == "video"][["item_ref"]].drop_duplicates()
ref = V.item_ref.str.extract(r"^(SEQ-[^/]+)/(\d+)-(\d+)$")
V = V.assign(seq=ref[0], f0=ref[1].astype(int), f1=ref[2].astype(int))
V.to_sql("chunk", mem, index=False)
CH = pd.read_sql("""SELECT c.item_ref, SUM(t.first_frame BETWEEN c.f0 AND c.f1) AS starts,
                           SUM(t.last_frame BETWEEN c.f0 AND c.f1 AND t.last_frame < s.frames - 1) AS ends
                    FROM chunk c JOIN tracks t ON t.sequence_id = c.seq JOIN sequences s ON s.sequence_id = c.seq
                    GROUP BY c.item_ref""", mem).set_index("item_ref")
TASK_LEN = int((V.f1 - V.f0 + 1).mode().iloc[0])
P["starts"] = P.item_ref.map(CH.starts)
P["ends"] = P.item_ref.map(CH.ends)
ok("archive: every video task joined to its sequence's tracks", P[P.kind == "video"].starts.notna().all(), "task length %d" % TASK_LEN)
P["nobj"] = np.where(P.kind == "box", P[CNT].sum(axis=1),
                     np.where(P.kind == "polygon", P.polygons.fillna(0) + P.polygons_occl.fillna(0), P.starts))

# ------------------------------------------------------------------ the punch clock under the pay policy, and R1
pu = pd.read_csv(os.path.join(TG, file_like("punch_clock")))
pu["t"] = pd.to_datetime(pu.punch_local.str[:19])
pu = pu.sort_values(["staff_id", "t"], kind="stable")
paid = {}
for sid, g in pu.groupby("staff_id", sort=False):
    open_t = None
    for t, d, s, site in zip(g.t, g.direction, g.source, g.site):
        if d == "IN":
            if open_t is not None and (t - open_t).total_seconds() <= 300:
                continue
            open_t = t
        elif s != "AUTO_CLOSE" and open_t is not None:
            wk = (open_t.date() - W0).days // 7
            paid[(sid, wk)] = paid.get((sid, wk), 0.0) + (t - open_t).total_seconds() / 3600 - LUNCH[site] / 60
            open_t = None
clock = pd.Series(paid)

wb = openpyxl.load_workbook(os.path.join(TG, file_like("pay_register")), read_only=True, data_only=True)


def sheet(ws):
    it = ws.iter_rows(values_only=True)
    h = next(it)
    return [dict(zip(h, r)) for r in it if r[0] is not None]


ann_rows, rev_rows, per_rows = sheet(wb["annotator weeks"]), sheet(wb["reviewer weeks"]), sheet(wb["period totals"])
wkey = lambda r: (r["staff_id"], (dt.date.fromisoformat(str(r["week_start"])[:10]) - W0).days // 7)
WK = {}
for r in ann_rows:
    e = WK.setdefault(wkey(r), dict(site=r["site"], hours=0.0, piece=0.0, topup=0.0))
    e["hours"] += r["paid_hours"]; e["piece"] += r["piece_pay_usd"]; e["topup"] += r["floor_topup_usd"]
WK = {k: v for k, v in WK.items() if abs(v["hours"]) > 1e-9}
RW = {}
for r in rev_rows:
    e = RW.setdefault(wkey(r), dict(site=r["site"], hours=0.0, pay=0.0))
    e["hours"] += r["paid_hours"]; e["pay"] += r["pay_usd"]
reg_hours = pd.Series({k: v["hours"] for k, v in WK.items()} | {k: v["hours"] for k, v in RW.items()})
both = clock.reindex(reg_hours.index).fillna(0.0)
ok("the punch clock re-run under the pay policy gives the register's paid hours, week by week",
   (both - reg_hours).abs().max() < 0.011 and abs(both.sum() - reg_hours.sum()) < 1.0,
   "max weekly gap %.3f h, total %.1f against %.1f" % ((both - reg_hours).abs().max(), both.sum(), reg_hours.sum()))
piece = sum(v["piece"] for v in WK.values()); topup = sum(v["topup"] for v in WK.values())
rpay = sum(v["pay"] for v in RW.values())
ah = sum(v["hours"] for v in WK.values()); rh = sum(v["hours"] for v in RW.values())
total = piece + topup + rpay + OVH * (ah + rh)
ok("R1 delivery cost as payroll settled it", abs(total - FG["R1_total"]) < 1.0, "%.0f against %.0f" % (total, FG["R1_total"]))
for nm, v in (("piece", piece), ("topup", topup), ("reviewer", rpay), ("overhead", OVH * (ah + rh))):
    ok("R1 %s" % nm, abs(v - FG["R1_%s" % nm]) < 1.0, "%.0f against %.0f" % (v, FG["R1_%s" % nm]))
ok("R1 paid hours", abs(ah - FG["R1_ann_hours"]) < 0.1 and abs(rh - FG["R1_rev_hours"]) < 0.1, "%.1f, %.1f" % (ah, rh))
ok("the period totals sheet agrees with the weekly sheets once the voided re-run nets out",
   abs(sum(r["piece_pay_usd"] for r in per_rows) - piece) < 0.5 and abs(sum(r["reviewer_pay_usd"] for r in per_rows) - rpay) < 0.5)

# ------------------------------------------------------------------ the fits, on their own code path
B1 = P[(P.kind == "box") & (P.depth == 1)]
Xb = np.column_stack([np.ones(len(B1))] + [B1[c].to_numpy(float) for c in CNT])
yb = B1.act.to_numpy()
spd = pd.Series(1.0, index=B1.annotator_id.unique())
for _ in range(4):
    beta = bnnls(Xb, yb / spd.reindex(B1.annotator_id).to_numpy())
    spd = pd.Series(yb / (Xb @ beta)).groupby(B1.annotator_id.to_numpy()).median()
    spd = spd / np.exp(np.log(spd).mean())
sp_of = lambda ids: spd.reindex(ids).fillna(1.0).to_numpy()
P1 = P[(P.kind == "polygon") & (P.depth == 1)]
bpoly = bnnls(np.column_stack([np.ones(len(P1)), P1.polygons, P1.polygons_occl, P1.vertices]).astype(float),
              P1.act.to_numpy() / sp_of(P1.annotator_id))
V1 = P[(P.kind == "video") & (P.depth == 1)]
bvid = bnnls(np.column_stack([np.ones(len(V1)), V1.frames, V1.boxes_on_screen, V1.starts, V1.ends]).astype(float),
             V1.act.to_numpy() / sp_of(V1.annotator_id))
bstock = bnnls(np.column_stack([np.ones(len(V1)), V1.frames, V1.boxes_on_screen]).astype(float), V1.act.to_numpy() / sp_of(V1.annotator_id))

# QA: found issues Poisson in the object counts with each annotator's care, by EM
J = P.merge(Rv[["pass_id", "missed", "misplaced", "review_s", "rid", "site", "reviewed_at_utc"]], on="pass_id")
Jb = J[J.kind == "box"]
Xc = Jb[CNT].to_numpy(float)
yc = (Jb.missed + Jb.misplaced).to_numpy(float)
fi = (Jb.depth == 1).to_numpy()
care = pd.Series(1.0, index=Jb.annotator_id.unique())
lam = np.full(6, 0.005)
for _ in range(3):
    cw = care.reindex(Jb.annotator_id).to_numpy()
    Xf, yf, cf = Xc[fi], yc[fi], cw[fi]
    den = (Xf * cf[:, None]).sum(axis=0)
    for it in range(4000):
        mu = cf * (Xf @ lam)
        new = lam * ((Xf * (cf * yf / np.maximum(mu, 1e-300))[:, None]).sum(axis=0) / den)
        if np.max(np.abs(new / lam - 1)) < 1e-10:
            lam = new
            break
        lam = new
    g = pd.DataFrame(dict(a=Jb.annotator_id.to_numpy()[fi], y=yf, p=Xf @ lam)).groupby("a").sum()
    care = (g.y + 2.0) / (g.p + 2.0)
    care = care / np.average(care, weights=g.p)
cw = care.reindex(Jb.annotator_id).to_numpy()
m2 = yc[~fi].sum() / (cw[~fi] * (Xc[~fi] @ lam)).sum()
prev = J[["item_ref", "depth", "missed", "misplaced"]].assign(depth=J.depth + 1)
C = P[(P.kind == "box") & (P.depth > 1)].merge(prev, on=["item_ref", "depth"], how="left")
bcorr = bnnls(np.column_stack([np.ones(len(C)), C.nobj, C.missed.fillna(0), C.misplaced.fillna(0)]).astype(float),
              C.act.to_numpy() / sp_of(C.annotator_id))
brev = {kd: bnnls(np.column_stack([np.ones(len(g)), g.nobj]).astype(float), g.review_s.to_numpy(float)) for kd, g in J.groupby("kind")}

# the hurried QA inputs: a logistic of a pass's return on its counts (Newton steps), 2026's re-return share, density bins
def newton_logit(X, y, steps=40):
    Z = np.column_stack([np.ones(len(X)), (X - X.mean(axis=0)) / X.std(axis=0)])
    w = np.zeros(Z.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(Z @ w)))
        g = Z.T @ (y - p)
        Hs = (Z * (p * (1 - p))[:, None]).T @ Z
        dw = np.linalg.solve(Hs, g)
        w = w + dw
        if np.max(np.abs(dw)) < 1e-10:
            break
    mu, sd = X.mean(axis=0), X.std(axis=0)
    return lambda Xn: 1 / (1 + np.exp(-(np.column_stack([np.ones(len(Xn)), (Xn - mu) / sd]) @ w)))


retc = (yc > 0).astype(float)
p_first = newton_logit(Xc[fi], retc[fi])
p_corr = newton_logit(Xc[~fi], retc[~fi])
rereturn = float(retc[~fi].mean())
EDGES = [20, 40, 60, 80, 100, 120]
nb = np.digitize(Xc.sum(axis=1), EDGES)
bin1 = pd.Series(retc[fi]).groupby(nb[fi]).mean()
bin2 = pd.Series(retc[~fi]).groupby(nb[~fi]).mean()
ok("2026's re-return share of corrected tasks as the answer blocks quote it", abs(rereturn - FG["rereturn_share_2026"]) < 0.0015,
   "%.4f against %s" % (rereturn, FG["rereturn_share_2026"]))

# paid time per tool second, paid weeks, week-to-week spread, reviewers' paid time per review second
act_w = P.groupby(["annotator_id", "week"]).act.sum()
aw = pd.DataFrame([dict(a=k[0], w=k[1], hours=v["hours"]) for k, v in WK.items()]).set_index(["a", "w"])
aw = aw.join(act_w.rename_axis(["a", "w"]).rename("act"), how="inner")
prod = (aw.groupby(level=0).act.sum() / (aw.groupby(level=0).hours.sum() * 3600)).to_dict()
pweek = aw.groupby(level=0).hours.median().to_dict()
rat = pd.DataFrame(dict(a=B1.annotator_id.to_numpy(), w=B1.week.to_numpy(), r=yb / (Xb @ beta))).groupby(["a", "w"]).r.median()
wsd = np.log(rat).groupby(level=0).std().fillna(0.07).to_dict()
rev_ratio = {s: sum(v["hours"] for k, v in RW.items() if v["site"] == s) * 3600 / Rv[Rv.site == s].review_s.sum() for s in OFFSET_H}

rost = openpyxl.load_workbook(os.path.join(TG, file_like("staff_roster")), read_only=True, data_only=True)
RA, RQ = sheet(rost["annotators"]), sheet(rost["qa reviewers"])
REVRATE = {s: sorted({r["hourly_rate_usd"] for r in RQ if r["site"] == s}) for s in OFFSET_H}
ok("roster: one QA reviewer rate per centre", all(len(v) == 1 for v in REVRATE.values()), str(REVRATE))
REVRATE = {s: v[0] for s, v in REVRATE.items()}
proj = pd.read_csv(os.path.join(TG, file_like("project_register"))).set_index("project_code")

# 2026's own shares (the hurried route's inputs) and the rates used for polygons and video
J1 = J[J.depth == 1].assign(scene=lambda d: d.project_code.map(proj.scene), ret=lambda d: (d.missed + d.misplaced) > 0)
CP = P[P.depth > 1].assign(scene=lambda d: d.project_code.map(proj.scene))
scene_ret, kind_ret = J1.groupby("scene").ret.mean(), J1.groupby("kind").ret.mean()
scene_fix, kind_fix = CP.groupby("scene").act.mean(), CP.groupby("kind").act.mean()
SCENE = {"A": "street", "B": "retail", "D": "pallet", "E": "warehouse"}
top_share = topup / piece


# ------------------------------------------------------------------ the samples
def area_size(a):
    return "small" if a < 32 * 32 else ("medium" if a < 96 * 96 else "large")


def read_sample(k):
    d = json.load(open(os.path.join(TG, SAMPLE[k])))
    if KIND[k] == "box":
        xyxy = d["info"].get("bbox_format") == "xyxy"
        rows = {im["id"]: dict.fromkeys(CNT, 0) for im in d["images"]}
        for a in d["annotations"]:
            x0, y0, x1, y1 = a["bbox"]
            w, h = (x1 - x0, y1 - y0) if xyxy else (x1, y1)
            occ = a["occlusion"] if "occlusion" in a else a["attributes"]["occluded"]
            rows[a["image_id"]]["obj_" + area_size(w * h) + ("_occl" if occ else "")] += 1
        return pd.DataFrame(list(rows.values()))
    if KIND[k] == "polygon":
        rows = {im["id"]: dict(polygons=0, polygons_occl=0, vertices=0) for im in d["images"]}
        for a in d["annotations"]:
            r = rows[a["image_id"]]
            occ = bool(a["attributes"]["occluded"])
            r["polygons_occl" if occ else "polygons"] += 1
            r["vertices"] += len(a["segmentation"][0]) // 2
        return pd.DataFrame(list(rows.values()))
    fr = {im["id"]: (im["video_id"], im["frame_id"]) for im in d["images"]}
    an = pd.DataFrame([(fr[a["image_id"]][0], fr[a["image_id"]][1], a["track_id"]) for a in d["annotations"]], columns=["v", "f", "tr"])
    span = an.groupby(["v", "tr"]).f.agg(["min", "max"]).reset_index()
    onf = an.groupby(["v", "f"]).size()
    out = []
    for v in d["videos"]:
        nf, vid = v["frames"], v["id"]
        sp = span[span.v == vid]
        for c0 in range(0, nf, TASK_LEN):
            c1 = min(nf, c0 + TASK_LEN) - 1
            out.append(dict(seq=vid, frames=c1 - c0 + 1, frame_objects=int(onf.reindex([(vid, f) for f in range(c0, c1 + 1)]).fillna(0).sum()),
                            starts=int(((sp["min"] >= c0) & (sp["min"] <= c1)).sum()),
                            ends=int(((sp["max"] >= c0) & (sp["max"] <= c1) & (sp["max"] < nf - 1)).sum())))
    return pd.DataFrame(out)


S = {k: read_sample(k) for k in "ABCDE"}
ok("samples: 400 images for each still request and the video's sequences cut into tasks",
   all(len(S[k]) == 400 for k in "ABDE") and len(S["C"]) > 100, ", ".join("%s %d" % (k, len(S[k])) for k in "ABCDE"))

GH_Z, GH_W = np.polynomial.hermite.hermgauss(60)


def cost(kind, s, staff, ret_share, fix_s, golden=(1, 1, 1), qa="logit_const"):
    """golden[0] = 0 takes the QA chain the hurried way (qa: a logistic first-pass return with 2026's re-return share,
    or with a logistic re-return, or 2026's density bins); golden[1] = 0 the floor at 2026's top-up share; golden[2] = 0
    the video on frames and objects on screen."""
    g1, g2, g3 = golden
    sh = staff.share.to_numpy()
    if kind == "box":
        X = s[CNT].to_numpy(float)
        t1 = beta[0] + X @ beta[1:]
        nobj = X.sum(axis=1); pc = nobj * RATE["box"]; per = 1.0
    elif kind == "polygon":
        t1 = (bpoly[0] + bpoly[1] * s.polygons + bpoly[2] * s.polygons_occl + bpoly[3] * s.vertices).to_numpy(float)
        nobj = (s.polygons + s.polygons_occl).to_numpy(float); pc = nobj * RATE["polygon"]; per = 1.0
    else:
        if g3:
            t1 = (bvid[0] + bvid[1] * s.frames + bvid[2] * s.frame_objects + bvid[3] * s.starts + bvid[4] * s.ends).to_numpy(float)
        else:
            t1 = (bstock[0] + bstock[1] * s.frames + bstock[2] * s.frame_objects).to_numpy(float)
        nobj = s.starts.to_numpy(float); pc = nobj * RATE["track"] + s.frames.to_numpy(float) * RATE["frame"]
        per = float(s.frames.mean())
    if kind == "box" and g1:
        Dn = X @ lam
        cwa = staff.annotator_id.map(care).fillna(1.0).to_numpy()
        q1 = 1 - np.exp(-np.outer(Dn, cwa)); q2 = 1 - np.exp(-np.outer(Dn * m2, cwa))
        ec = (q1 * (1 + q2 + q2 ** 2)) @ sh
        ct = ec * (bcorr[0] + bcorr[1] * nobj + bcorr[2] * np.minimum(Dn, 3.0))
        nrev = 1 + ec
    elif kind == "box":
        Dn = X @ lam
        if qa == "binned_binned":
            cb = np.digitize(X.sum(axis=1), EDGES)
            p1 = bin1.reindex(cb).fillna(bin1.iloc[-1]).to_numpy(); r2 = bin2.reindex(cb).fillna(bin2.iloc[-1]).to_numpy()
        else:
            p1 = p_first(X)
            r2 = p_corr(X) if qa == "logit_logit" else rereturn
        ec = p1 * (1 + r2 + r2 * r2)
        ct = ec * (bcorr[0] + bcorr[1] * nobj + bcorr[2] * np.minimum(Dn, 3.0))
        nrev = 1 + ec
    else:
        ct = np.full(len(t1), ret_share * fix_s); nrev = np.full(len(t1), 1 + ret_share)
    a_act = float((t1 + ct).mean()); r_act = float((nrev * (brev[kind][0] + brev[kind][1] * nobj)).mean()); pt = float(pc.mean())
    pm = float(np.mean(list(prod.values())))
    a_paid, tau = [], []
    for a, site, hrs in zip(staff.annotator_id, staff.site, staff.hours):
        sec = a_act * float(spd.get(a, 1.0)); pr = float(prod.get(a, pm)); pw = float(pweek.get(a, hrs * 0.95))
        a_paid.append(sec / pr / 3600)
        f = np.exp(np.sqrt(2.0) * wsd.get(a, 0.07) * GH_Z)
        imgs = pw * 3600 * pr / (sec * f)
        tau.append(float(np.dot(GH_W, np.maximum(0.0, FLOOR[site] * pw - imgs * pt)) / np.dot(GH_W, imgs)))
    a_h = float(np.dot(sh, a_paid))
    tp = float(np.dot(sh, tau)) if g2 else top_share * pt
    sc = staff.groupby("site").share.sum()
    r_h = r_act / 3600 * sum(sc[c] * rev_ratio[c] for c in sc.index)
    c = pt + tp + r_h * sum(sc[c] * REVRATE[c] for c in sc.index) + OVH * (a_h + r_h)
    return dict(cost=c / per, reviews=float(nrev.mean()), minutes=a_h * 60 / per, topup=tp / per)


skill = {"box": "box", "polygon": "polygon", "video": "video"}
STAFF = {}
for kd in skill:
    e = pd.DataFrame([r for r in RA if r["leave_date"] in (None, "") and kd in str(r["skills"]).split(";")])
    STAFF[kd] = pd.DataFrame(dict(annotator_id=e.staff_id, site=e.site, hours=e.contract_hours_week.astype(float),
                                  share=e.contract_hours_week / e.contract_hours_week.sum()))


def hist(k):
    kd = KIND[k]
    sc = SCENE.get(k)
    return (float(scene_ret.get(sc, kind_ret[kd])), float(scene_fix.get(sc, kind_fix[kd])))


GOLD = {k: cost(KIND[k], S[k], STAFF[KIND[k]], *hist(k)) for k in "ABCDE"}
REFL = {k: cost(KIND[k], S[k], STAFF[KIND[k]], *hist(k), golden=(0, 1, 0)) for k in "ABCDE"}
for k in "ABCDE":
    g = GOLD[k]
    ok("R2 QA reviews per delivered unit, request %s" % k, near(g["reviews"], FG["R2_reviews_%s" % k], 0.05),
       "%.3f against %.2f" % (g["reviews"], FG["R2_reviews_%s" % k]))
    ok("R3 annotator paid minutes per delivered unit, request %s" % k, near(g["minutes"], FG["R3_minutes_%s" % k], 0.05),
       "%.4f against %s" % (g["minutes"], FG["R3_minutes_%s" % k]))
    ok("R4 floor top-up per delivered unit, request %s" % k,
       near(g["topup"], FG["R4_topup_%s" % k], 0.20, 0.0005 if k == "C" else 0.005), "%.4f against %s" % (g["topup"], FG["R4_topup_%s" % k]))
    ok("R6 expected cost per delivered unit, request %s" % k, near(g["cost"], FG["R6_cost_%s" % k], 0.03),
       "%.4f against %s" % (g["cost"], FG["R6_cost_%s" % k]))
acc = sorted(k for k in "ABCDE" if PRICE[k] >= MARGIN * GOLD[k]["cost"])
ok("R7 the accept set from the recomputed costs and the RFQs' prices", acc == FG["call_accept"], str(acc))
ok("R7 every request at least 8 per cent from its line on the recomputed cost",
   all(abs(GOLD[k]["cost"] * MARGIN / PRICE[k] - 1) >= 0.08 for k in "ABCDE"),
   ", ".join("%s %+.1f%%" % (k, 100 * (GOLD[k]["cost"] * MARGIN / PRICE[k] - 1)) for k in "ABCDE"))
for k in FG["call_decline"]:
    ok("R7 lowest acceptable price, request %s" % k, near(MARGIN * GOLD[k]["cost"], FG["R7_lowest_price_%s" % k], 0.03),
       "%.4f against %s" % (MARGIN * GOLD[k]["cost"], FG["R7_lowest_price_%s" % k]))
hacc = sorted(k for k in "ABCDE" if PRICE[k] >= MARGIN * REFL[k]["cost"])
ok("the hurried costing (2026 shares, objects on screen) files a different set", hacc != acc, str(hacc))
ok("the hurried figures the answer blocks quote recompute (A and B reviews, C minutes)",
   all(near(REFL[k]["reviews"], FG["careful_reviews_%s" % k], 0.02) for k in "AB") and
   near(REFL["C"]["minutes"], FG["careful_minutes_C"], 0.02),
   "A %.3f, B %.3f, C %.4f" % (REFL["A"]["reviews"], REFL["B"]["reviews"], REFL["C"]["minutes"]))
for qa, key in (("logit_logit", "logit"), ("binned_binned", "binned")):
    alt = {k: cost("box", S[k], STAFF["box"], *hist(k), golden=(0, 1, 1), qa=qa) for k in "AB"}
    ok("the %s QA alternative the answer blocks quote recomputes" % qa,
       all(near(alt[k]["reviews"], FG["alt_%s_reviews_%s" % (key, k)], 0.02) for k in "AB"),
       ", ".join("%s %.3f" % (k, alt[k]["reviews"]) for k in "AB"))

# the 80 per cent ranges: each holds its cost and stays on one side of the line, recomputed by a bootstrap of our own
rng = np.random.default_rng(2027)
for k in "ABCDE":
    lo, hi = FG["R6_range_%s" % k]
    line = PRICE[k] / MARGIN
    vals = []
    for _ in range(80):
        if k == "C":
            pick = rng.choice(S[k].seq.unique(), S[k].seq.nunique(), replace=True)
            s = pd.concat([S[k][S[k].seq == v] for v in pick], ignore_index=True)
        else:
            s = S[k].iloc[rng.integers(0, len(S[k]), len(S[k]))].reset_index(drop=True)
        vals.append(cost(KIND[k], s, STAFF[KIND[k]], *hist(k))["cost"])
    q10, q90 = np.percentile(vals, [10, 90])
    side = (lo > line) == (hi > line) == (FG["R6_cost_%s" % k] > line)
    ok("R6 80 per cent range, request %s: holds the cost, clears the line, recomputes" % k,
       lo < FG["R6_cost_%s" % k] < hi and side and near(q10, lo, 0.05) and near(q90, hi, 0.05) and ((q10 > line) == (q90 > line)),
       "[%.4f, %.4f] against [%s, %s], line %.4f" % (q10, q90, lo, hi, line))

# ------------------------------------------------------------------ R5: each 2026 project's actual and its costing
aw2 = P.groupby(["annotator_id", "week", "project_code"]).act.sum().rename("s").reset_index()
aw2["w"] = aw2.s / aw2.groupby(["annotator_id", "week"]).s.transform("sum")
aw2["c"] = [w * (WK[(a, wk)]["piece"] + WK[(a, wk)]["topup"] + OVH * WK[(a, wk)]["hours"]) if (a, wk) in WK else 0.0
            for a, wk, w in zip(aw2.annotator_id, aw2.week, aw2.w)]
loc = pd.to_datetime(J.reviewed_at_utc.str[:19]) + pd.to_timedelta(J.site.map(OFFSET_H), unit="h")
rw2 = pd.DataFrame(dict(r=J.rid, w=(loc.dt.normalize() - pd.Timestamp(W0)).dt.days // 7, p=J.project_code, s=J.review_s))
rw2 = rw2.groupby(["r", "w", "p"]).s.sum().reset_index()
rw2["sh"] = rw2.s / rw2.groupby(["r", "w"]).s.transform("sum")
rw2["c"] = [sh * (RW[(r, w)]["pay"] + OVH * RW[(r, w)]["hours"]) if (r, w) in RW else 0.0 for r, w, sh in zip(rw2.r, rw2.w, rw2.sh)]
pc = aw2.groupby("project_code").c.sum().add(rw2.groupby("p").c.sum(), fill_value=0.0)
actual = pc / proj.delivered_units.reindex(pc.index)
ok("R5 project costs add back to the 2026 delivery cost", abs(pc.sum() - total) < 0.005 * total, "%.0f against %.0f" % (pc.sum(), total))
ra = {k: r for k, r in ((r["staff_id"], r) for r in RA)}
gaps = {}
for p, g in P[P.depth == 1].groupby("project_code"):
    kd = g.kind.iloc[0]
    if kd == "video":
        s = pd.DataFrame(dict(frames=g.frames, frame_objects=g.boxes_on_screen, starts=g.starts, ends=g.ends)).reset_index(drop=True)
    else:
        s = g[CNT if kd == "box" else ["polygons", "polygons_occl", "vertices"]].astype(float).reset_index(drop=True)
    n = g.groupby("annotator_id").size()
    st = pd.DataFrame(dict(annotator_id=n.index, site=[ra[a]["site"] if a in ra else a[:3] for a in n.index],
                           hours=[float(ra[a]["contract_hours_week"]) if a in ra else 40.0 for a in n.index], share=(n / n.sum()).to_numpy()))
    sc = proj.loc[p, "scene"]
    rs, fx = float(scene_ret.get(sc, kind_ret[kd])), float(scene_fix.get(sc, kind_fix[kd]))
    gold_p = cost(kd, s, st, rs, fx)["cost"]
    gaps[p] = gold_p / actual[p] - 1
    if p in ("P26-0446", "P26-0441", "P26-0434"):
        hur_p = cost(kd, s, st, rs, fx, golden=(0, 1, 0))["cost"]
        ok("R5 %s actual cost per delivered unit" % p, near(actual[p], FG["R5_actual_%s" % p], 0.01),
           "%.4f against %s" % (actual[p], FG["R5_actual_%s" % p]))
        ok("R5 %s costing per delivered unit" % p, near(gold_p, FG["R5_costing_%s" % p], 0.03),
           "%.4f against %s" % (gold_p, FG["R5_costing_%s" % p]))
        ok("R5 %s hurried costing quoted in the answer blocks" % p, near(hur_p, FG["R5_hurried_%s" % p], 0.03),
           "%.4f against %s" % (hur_p, FG["R5_hurried_%s" % p]))
gp = pd.Series(gaps).abs()
gp = gp[[p for p in gp.index if proj.loc[p, "end_date"] <= "2026-10-18"]]
ok("R5 the costing within 6 per cent on the stated count of closed projects, and its largest gap",
   abs(int((gp <= 0.06).sum()) - FG["R5_within_6pct"]) <= 1 and len(gp) == FG["R5_projects"] and abs(100 * gp.max() - FG["R5_max_gap_pct"]) < 1.0,
   "%d of %d, max %.1f per cent" % ((gp <= 0.06).sum(), len(gp), 100 * gp.max()))

# ------------------------------------------------------------------ the golden files read back against figures.json
gx = [n for n in os.listdir(GDIR) if n.endswith(".xlsx")]
gd = [n for n in os.listdir(GDIR) if n.endswith(".docx")]
ok("the golden set is one workbook and one note", len(gx) == 1 and len(gd) == 1 and len(os.listdir(GDIR)) == 2, str(os.listdir(GDIR)))
gw = openpyxl.load_workbook(os.path.join(GDIR, gx[0]), data_only=True)
q = sheet(gw["Q1 2027 requests"])
q = [r for r in q if r.get("Unit") in ("image", "frame")]
ok("workbook: five requests", len(q) == 5)
for r, k in zip(q, "ABCDE"):
    ok("workbook request %s: cost, range, drivers and decision as figures.json" % k,
       r["Expected cost per unit (USD)"] == FG["R6_cost_%s" % k] and [r["80% range low"], r["80% range high"]] == FG["R6_range_%s" % k]
       and r["QA reviews per unit"] == FG["R2_reviews_%s" % k] and r["Annotator paid minutes per unit"] == FG["R3_minutes_%s" % k]
       and r["Floor top-up per unit (USD)"] == FG["R4_topup_%s" % k] and r["Decision"] == ("accept" if k in FG["call_accept"] else "decline")
       and (r["Lowest acceptable price (USD)"] in (None, "") if k in FG["call_accept"] else r["Lowest acceptable price (USD)"] == FG["R7_lowest_price_%s" % k]))
pr = {r["Project"]: r for r in sheet(gw["2026 projects"])}
ok("workbook 2026 projects: the three graded projects as figures.json",
   all(pr[p]["Actual cost per unit (USD)"] == FG["R5_actual_%s" % p] and pr[p]["Costing per unit (USD)"] == FG["R5_costing_%s" % p]
       for p in ("P26-0446", "P26-0441", "P26-0434")) and
   sum(1 for r in pr.values() if r["Closed by 18 October"] == "yes") == FG["R5_projects"])
dc = {r["Line"]: r["USD or hours"] for r in sheet(gw["2026 delivery cost"])}
ok("workbook 2026 delivery cost as figures.json", dc["Delivery cost, 6 April to 1 November 2026"] == FG["R1_total"] and
   dc["Annotator paid hours"] == FG["R1_ann_hours"] and dc["Piece pay"] == FG["R1_piece"])
import docx  # noqa: E402

dtext = "\n".join(p.text for p in docx.Document(os.path.join(GDIR, gd[0])).paragraphs)
ok("note: the recommendation names the accepted and declined requests with the lowest prices",
   all(("USD %.2f" % FG["R7_lowest_price_%s" % k]) in dtext for k in FG["call_decline"]) and dtext.count("Accept") >= 1)
ok("note: every figure it quotes is the figures.json figure at the same rounding",
   all(t in dtext for t in ["%.2f reviews per image; this year's re-return rate carried along the chain gives %.2f" % (
       FG["R2_reviews_A"], FG["careful_reviews_A"]), "(%.2f reviews per image)" % FG["R2_reviews_B"],
       "USD %.3f an image" % FG["R4_topup_D"], "%.3f paid minutes a frame" % FG["R3_minutes_C"],
       "USD %.4f a frame" % FG["R6_cost_C"], "%.1f per cent off" % FG["R5_max_gap_pct"],
       "on %d of the %d projects" % (FG["R5_within_6pct"], FG["R5_projects"])]))
print("%d FAIL" % len(BAD))
sys.exit(1 if BAD else 0)
