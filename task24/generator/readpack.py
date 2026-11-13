"""task24: read the cut pack back into the tables the costing runs on, applying only what the pack's own documents
file (the pay policy's punch rules, the QA standard's return rule, the register's voided run, each system's keys).
Nothing here reads generator state: the golden and the verifier both start from these tables."""
import datetime as dt
import json
import os
import sqlite3

import numpy as np
import pandas as pd

FILES = dict(passes="pellucid_task_passes_2026-04-06_2026-11-01.csv", reviews="qa_reviews_2026-04-06_2026-11-01.csv",
             punch="punch_clock_2026-04-06_2026-11-01.csv", pay="pay_register_2026_apr_oct.xlsx",
             roster="staff_roster_2026-11-06.xlsx", projects="project_register_2026.csv",
             archive="video_delivery_archive_2026.sqlite")
SAMPLES = {"A": "vantorra_VTA-2027-014_preview_labels.json", "B": "shelfgrid_SG27-03_preview_labels.json",
           "C": "ardley_HWY-Q1-27_preview_sequences.json", "D": "brindle_BPS-2027-02_preview_labels.json",
           "E": "kestrin_KW-2701_preview_labels.json"}
WEEK0 = dt.date(2026, 4, 6)
COUNT_COLS = ["n_S_clr", "n_S_occ", "n_M_clr", "n_M_occ", "n_L_clr", "n_L_occ"]
TOOL = dict(obj_small="n_S_clr", obj_small_occl="n_S_occ", obj_medium="n_M_clr", obj_medium_occl="n_M_occ",
            obj_large="n_L_clr", obj_large_occl="n_L_occ")
CHUNK = 25


def _week(ts):
    d = dt.datetime.fromisoformat(ts).date()
    return (d - WEEK0).days // 7


def passes(target):
    df = pd.read_csv(os.path.join(target, FILES["passes"]), dtype={"parent_pass_id": str})
    df = df.drop_duplicates()                                   # the tool's sync retries
    df = df[df.pass_type != "released"].copy()
    df["parent_pass_id"] = df.parent_pass_id.fillna("")
    parent = dict(zip(df.pass_id, df.parent_pass_id))
    depth = {}
    for pid in df.pass_id:
        n, p = 1, parent[pid]
        while p:
            n += 1
            p = parent.get(p, "")
        depth[pid] = n
    df["pass_no"] = df.pass_id.map(depth)
    df["kind"] = np.where(df.frames.notna(), "video", np.where(df.polygons.notna(), "polygon", "box"))
    for k, v in TOOL.items():
        df[v] = df[k]
    df["n_poly"] = df.polygons.fillna(0) + df.polygons_occl.fillna(0)
    df["n_poly_occ"] = df.polygons_occl
    df["week"] = [_week(t) for t in df.submitted_at]
    df["active_seconds"] = df.tool_active_s.astype(float)
    df["nobj"] = np.where(df.kind == "box", df[list(TOOL)].sum(axis=1), np.where(df.kind == "polygon", df.n_poly, np.nan))
    df["project"] = df.project_code
    df["item"] = df.item_ref
    df["pass_key"] = df.pass_id
    return df.reset_index(drop=True)


def reviews(target, P):
    r = pd.read_csv(os.path.join(target, FILES["reviews"]))
    r["reviewer_id"] = [x if "-" in x else x[:3] + "-" + x[3:] for x in r.reviewer_id]
    r["centre"] = r.reviewer_id.str[:3]
    r = r.rename(columns={"missed": "found_missed", "misplaced": "found_misplaced", "review_s": "seconds"})
    r["pass_key"] = r.pass_id
    return r[r.pass_key.isin(set(P.pass_key))].reset_index(drop=True)


def punches(target):
    """Paid hours per person per pay week under the pay policy's rules."""
    df = pd.read_csv(os.path.join(target, FILES["punch"]))
    df["t"] = [dt.datetime.fromisoformat(x) for x in df.punch_local]
    df = df.sort_values(["staff_id", "t"]).reset_index(drop=True)
    lunch = {"KSM": 45, "ILO": 60}
    out = []
    for sid, g in df.groupby("staff_id", sort=False):
        ins = None
        rows = g.to_dict("records")
        i = 0
        while i < len(rows):
            r = rows[i]
            if r["direction"] == "IN":
                if ins is not None and (r["t"] - ins).total_seconds() <= 300:
                    i += 1
                    continue                                   # a second IN within five minutes counts once
                ins = r["t"]
            else:
                if r["source"] == "AUTO_CLOSE":
                    i += 1
                    continue                                   # paid as the supervisor's edit records it
                if ins is not None:
                    h = (r["t"] - ins).total_seconds() / 3600 - lunch[r["site"]] / 60
                    out.append(dict(staff_id=sid, site=r["site"], day=ins.date(), paid_hours=h,
                                    week=(ins.date() - WEEK0).days // 7))
                    ins = None
            i += 1
    return pd.DataFrame(out)


def pay_register(target):
    x = pd.ExcelFile(os.path.join(target, FILES["pay"]))
    a = x.parse("annotator weeks")
    r = x.parse("reviewer weeks")
    t = x.parse("period totals")
    for d in (a, r):
        d["week"] = [(dt.date.fromisoformat(str(w)[:10]) - WEEK0).days // 7 for w in d.week_start]
    num = ["paid_hours", "boxes_paid", "polygons_paid", "tracks_paid", "frames_paid", "piece_pay_usd", "floor_topup_usd",
           "transport_allowance_usd", "adjustment_usd", "gross_usd"]
    a_net = a.groupby(["staff_id", "site", "week"])[num].sum().reset_index()      # the voided re-run nets to nothing
    a_net = a_net[a_net.paid_hours.abs() > 1e-9]
    return a_net, r, t, a


def roster(target):
    x = pd.ExcelFile(os.path.join(target, FILES["roster"]))
    a = x.parse("annotators", dtype={"leave_date": str})
    q = x.parse("qa reviewers")
    a["leave_date"] = a.leave_date.replace({"nan": None, "": None})
    a["skills"] = a.skills.str.split(";")
    a = a.rename(columns={"staff_id": "annotator_id", "site": "centre", "contract_hours_week": "scheduled_hours",
                          "leave_date": "left_date"})
    a["left_date"] = a.left_date.where(a.left_date.notna(), None)
    q = q.rename(columns={"staff_id": "reviewer_id", "site": "centre", "contract_hours_week": "scheduled_hours"})
    return a, q


def projects(target):
    p = pd.read_csv(os.path.join(target, FILES["projects"]))
    p["project"] = p.project_code
    p["kind"] = p.task_type.map({"bounding boxes": "box", "polygon segmentation": "polygon", "video tracking": "video"})
    return p


def archive(target):
    con = sqlite3.connect(os.path.join(target, FILES["archive"]))
    seq = pd.read_sql("SELECT * FROM sequences", con)
    tr = pd.read_sql("SELECT * FROM tracks", con)
    con.close()
    tr = tr.merge(seq[["sequence_id", "project_code", "frames"]], on="sequence_id")
    return seq, tr


def video_chunks(P, seq, tr):
    """Each video pass's chunk with the archive's tracks starting and ending in it (an ending before the
    sequence's last frame), and the objects on screen the tool counted."""
    v = P[P.kind == "video"].copy()
    ref = v.item_ref.str.extract(r"^(SEQ-[^/]+)/(\d+)-(\d+)$")
    v["sequence_id"] = ref[0]; v["frame_from"] = ref[1].astype(int); v["frame_to"] = ref[2].astype(int)
    ch = v[["item_ref", "sequence_id", "frame_from", "frame_to", "frames", "boxes_on_screen"]].drop_duplicates("item_ref")
    last = tr.groupby("sequence_id").frames.first() - 1
    starts, ends = [], []
    by = {k: g for k, g in tr.groupby("sequence_id")}
    for r in ch.itertuples():
        t = by[r.sequence_id]
        ff, lf = t.first_frame.to_numpy(), t.last_frame.to_numpy()
        starts.append(int(((ff >= r.frame_from) & (ff <= r.frame_to)).sum()))
        ends.append(int(((lf >= r.frame_from) & (lf <= r.frame_to) & (lf < last[r.sequence_id])).sum()))
    ch["starts"] = starts; ch["ends"] = ends
    ch["frame_objects"] = ch.boxes_on_screen
    return ch


# ------------------------------------------------------------------ the requests' samples
def _size(area):
    return "S" if area < 32 * 32 else ("M" if area < 96 * 96 else "L")


def sample_counts(target, key):
    doc = json.load(open(os.path.join(target, SAMPLES[key])))
    if key == "C":
        return sample_video(doc)
    if key == "D":
        rows = {im["id"]: dict(n_poly=0, n_poly_occ=0, vertices=0) for im in doc["images"]}
        for a in doc["annotations"]:
            r = rows[a["image_id"]]
            r["n_poly"] += 1
            r["n_poly_occ"] += int(a["attributes"]["occluded"])
            r["vertices"] += len(a["segmentation"][0]) // 2
        return pd.DataFrame(list(rows.values()))
    fmt = doc["info"].get("bbox_format", "xywh")
    rows = {im["id"]: {c: 0 for c in COUNT_COLS} for im in doc["images"]}
    for a in doc["annotations"]:
        b = a["bbox"]
        w, h = (b[2] - b[0], b[3] - b[1]) if fmt == "xyxy" else (b[2], b[3])
        occ = bool(a["occlusion"]) if "occlusion" in a else bool(a["attributes"]["occluded"])
        rows[a["image_id"]]["n_%s_%s" % (_size(w * h), "occ" if occ else "clr")] += 1
    return pd.DataFrame(list(rows.values()))


def sample_video(doc):
    """The sample's sequences cut into 25-frame chunks as the tool cuts them, with tracks starting and ending."""
    frames_of = {v["id"]: v["frames"] for v in doc["videos"]}
    img = {im["id"]: (im["video_id"], im["frame_id"]) for im in doc["images"]}
    first, last, on = {}, {}, {}
    for a in doc["annotations"]:
        vid, f = img[a["image_id"]]
        k = (vid, a["track_id"])
        first[k] = min(first.get(k, f), f); last[k] = max(last.get(k, f), f)
        on[(vid, f)] = on.get((vid, f), 0) + 1
    rows = []
    for vid, F_ in frames_of.items():
        tf = np.array([first[k] for k in first if k[0] == vid]); tl = np.array([last[k] for k in last if k[0] == vid])
        for c0 in range(0, F_, CHUNK):
            c1 = min(F_, c0 + CHUNK) - 1
            rows.append(dict(seq=vid, frame_from=c0, frame_to=c1, frames=c1 - c0 + 1,
                             frame_objects=sum(on.get((vid, f), 0) for f in range(c0, c1 + 1)),
                             starts=int(((tf >= c0) & (tf <= c1)).sum()),
                             ends=int(((tl >= c0) & (tl <= c1) & (tl < F_ - 1)).sum())))
    return pd.DataFrame(rows)


def load(target):
    P = passes(target)
    R = reviews(target, P)
    pay_a, pay_r, totals, pay_raw = pay_register(target)
    ann, rev = roster(target)
    proj = projects(target)
    seq, tr = archive(target)
    ch = video_chunks(P, seq, tr)
    vi = P.kind == "video"
    P.loc[vi, "nobj"] = P.loc[vi, "item_ref"].map(ch.set_index("item_ref").starts)
    WK = pay_a.rename(columns={"staff_id": "annotator_id", "site": "centre", "piece_pay_usd": "piece",
                               "floor_topup_usd": "topup"})
    clock = punches(target)
    S = {k: sample_counts(target, k) for k in "ABCDE"}
    return dict(P=P, R=R, WK=WK, pay_r=pay_r, totals=totals, pay_raw=pay_raw, ann=ann, rev=rev, proj=proj, seq=seq,
                tracks=tr, chunks=ch, clock=clock, samples=S)
