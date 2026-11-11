"""task19 fieldwork: dwellings and enumeration blocks at 30 June 2026, the coverage survey of a sample of blocks, the
field follow-up of the register's records listed at the sampled blocks' addresses, and the clerical review of a
random subsample of survey persons against the register.

Households are formed from the residents of each district on the reference date; blocks of about forty residents
are the survey's sampling units. A register record's address is the person's current dwelling when the record is
current, and an earlier dwelling in the record's district otherwise."""
import numpy as np

import params as PR
import world as WD


def households(rng, idx, typ, shared_share, P):
    """Split one district's residents into households and dwellings; returns dwelling id per person (local) and the
    dwelling table (type, and a flag for a dwelling with nobody in it)."""
    n = len(idx)
    order = rng.permutation(n)
    # serving personnel live in barracks blocks, students mostly in shared houses and halls
    forces = P.view("forces")[idx]
    student = P.view("student")[idx]
    hh = np.full(n, -1, np.int64)
    dtype = []
    k = 0
    # barracks: rooms of 1, grouped into blocks later as communal dwellings of 8
    fi = np.where(forces)[0]
    for s in range(0, len(fi), 8):
        hh[fi[s:s + 8]] = k
        dtype.append("communal")
        k += 1
    si = np.where(student & ~forces)[0]
    si = si[rng.permutation(len(si))]
    p = 0
    while p < len(si):
        m = int(rng.choice([1, 3, 4, 5, 6], p=[0.15, 0.2, 0.3, 0.2, 0.15]))
        hh[si[p:p + m]] = k
        dtype.append("shared")
        k += 1
        p += m
    rest = np.array([i for i in order if hh[i] < 0], dtype=np.int64)
    p = 0
    city = typ == "city"
    sizes = [1, 2, 3, 4, 5, 6]
    psz = [0.31, 0.33, 0.15, 0.13, 0.06, 0.02] if city else [0.27, 0.34, 0.16, 0.15, 0.06, 0.02]
    while p < len(rest):
        m = int(rng.choice(sizes, p=psz))
        sh = rng.random() < shared_share
        if sh:
            m = int(rng.choice([3, 4, 5, 6]))
        hh[rest[p:p + m]] = k
        dtype.append("shared" if sh else ("flat" if rng.random() < (0.45 if city else 0.2) else "house"))
        k += 1
        p += m
    return hh, dtype


def build(W, seed=PR.SEED + 1):
    rng = np.random.default_rng(seed)
    P, R = W["P"], W["R"]
    res = np.where(P.view("status") == 0)[0]
    dw_of = np.full(P.n, -1, np.int64)
    dwell = {"dist": [], "type": [], "block": [], "vacant": []}
    blocks = {"dist": [], "persons": []}
    nd = 0
    for di, d in enumerate(PR.DISTRICTS):
        idx = res[P.view("dist")[res] == di]
        hh, dtypes = households(rng, idx, d[3], d[9], P)
        ndw = len(dtypes)
        # vacant dwellings, about four in a hundred
        nvac = int(0.04 * ndw)
        types = list(dtypes) + list(rng.choice(["house", "flat", "shared"], size=nvac, p=[0.5, 0.35, 0.15]))
        vac = np.r_[np.zeros(ndw, bool), np.ones(nvac, bool)]
        order = rng.permutation(len(types))      # street order, unrelated to household formation
        size = np.r_[np.bincount(hh, minlength=ndw), np.zeros(nvac, int)]
        # blocks of about forty residents along the street order
        blk = np.empty(len(types), np.int64)
        acc, b = 0, len(blocks["dist"])
        target = PR.CLUSTER_PERSONS * rng.uniform(0.75, 1.25)
        for j in order:
            blk[j] = b
            acc += size[j]
            if acc >= target:
                blocks["dist"].append(di)
                blocks["persons"].append(acc)
                b += 1
                acc = 0
                target = PR.CLUSTER_PERSONS * rng.uniform(0.75, 1.25)
        if acc > 0:
            blocks["dist"].append(di)
            blocks["persons"].append(acc)
        dw_of[idx] = nd + hh
        dwell["dist"] += [di] * len(types)
        dwell["type"] += types
        dwell["block"] += list(blk)
        dwell["vacant"] += list(vac)
        nd += len(types)
    for k in dwell:
        dwell[k] = np.array(dwell[k])
    blocks = {k: np.array(v) for k, v in blocks.items()}
    W["dw_of"], W["dwell"], W["blocks"] = dw_of, dwell, blocks

    # ---------------------------------------------------------------- each open record's address
    o = np.where(R.view("open"))[0]
    pid = R.view("pid")[o]
    rd = R.view("dist")[o]
    alive = P.view("status")[pid] == 0
    # serving personnel are counted from the defence return: any civilian record of theirs lives elsewhere
    here = alive & (P.view("dist")[pid] == rd) & ~P.view("forces")[pid]
    # the person's current record is the latest open one where they live; others are duplicates or elsewhere
    rec_dw = np.full(len(o), -1, np.int64)
    cur = here & ~R.view("stale_within")[o]
    # if a person has two open records in their own district, the later one is current, the earlier a duplicate
    latest = {}
    for j in np.where(here)[0]:
        p = pid[j]
        if p not in latest or R.reg[o[j]] > R.reg[o[latest[p]]]:
            latest[p] = j
    is_latest = np.zeros(len(o), bool)
    is_latest[list(latest.values())] = True
    cur = cur & is_latest
    rec_dw[cur] = dw_of[pid[cur]]
    # every other record sits at another dwelling of its district
    for di in range(WD.ND):
        need = np.where((rec_dw < 0) & (rd == di))[0]
        pool = np.where(dwell["dist"] == di)[0]
        rec_dw[need] = rng.choice(pool, size=len(need))
    W["rec_open"], W["rec_dw"] = o, rec_dw
    # truth class of each open record: 0 correct here (district), 1 duplicate, 2 lives elsewhere in Kilvarra,
    # 3 left Kilvarra or had left before 2021, 4 died
    cls = np.full(len(o), 2, np.int8)
    st = P.view("status")[pid]
    cls[st == 1] = 3
    cls[st == 9] = 3
    cls[st == 2] = 4
    # a person with a current record somewhere: their other open records are duplicates
    has_cur = np.zeros(P.n, bool)
    has_cur[pid[here & is_latest]] = True
    cls[here & is_latest] = 0
    dup = alive & ~(here & is_latest) & has_cur[pid]
    cls[dup] = 1
    # a person whose only records are elsewhere: the latest elsewhere record is "elsewhere"; extra ones duplicates
    W["rec_class"] = cls

    # ---------------------------------------------------------------- the coverage survey
    nb = len(blocks["dist"])
    sel = np.zeros(nb, bool)
    for di in range(WD.ND):
        bi = np.where(blocks["dist"] == di)[0]
        m = max(8, int(round(PR.SAMPLE_FRACTION * len(bi))))
        sel[rng.choice(bi, size=m, replace=False)] = True
    W["block_sel"] = sel
    W["block_frac"] = np.array([sel[blocks["dist"] == di].mean() for di in range(WD.ND)])
    in_blk = np.where((dw_of >= 0))[0]
    pblk = dwell["block"][dw_of[in_blk]]
    psel = in_blk[sel[pblk]]
    # household contact, then each member listed
    hh_ids = dw_of[psel]
    uh, inv = np.unique(hh_ids, return_inverse=True)
    vbar = np.bincount(inv, weights=P.view("v")[psel].astype(float)) / np.bincount(inv)
    typ = dwell["type"][uh]
    hc = WD.Phi(1.75 + 0.35 * vbar - np.where(typ == "shared", 0.35, 0.0) + np.where(typ == "communal", 0.9, 0.0))
    hh_ok = rng.random(len(uh)) < hc
    listed = rng.random(len(psel)) < WD.Phi(1.65 + 0.55 * P.view("v")[psel].astype(float))
    resp = psel[hh_ok[inv] & listed]
    W["survey_pid"] = resp
    W["survey_frame_pid"] = psel

    # ---------------------------------------------------------------- the follow-up of listed records
    rblk = dwell["block"][rec_dw]
    fo = np.where(sel[rblk])[0]           # positions in the open-record arrays
    fdw = rec_dw[fo]
    occ_v = np.zeros(nd)
    cnt = np.bincount(dw_of[res], minlength=nd)
    occ_v_sum = np.bincount(dw_of[res], weights=P.view("v")[res].astype(float), minlength=nd)
    occ_v[cnt > 0] = occ_v_sum[cnt > 0] / cnt[cnt > 0]
    vac = (cnt[fdw] == 0)
    ftyp = dwell["type"][fdw]
    contact = np.where(vac, rng.random(len(fo)) < 0.88,
                       rng.random(len(fo)) < WD.Phi(1.55 + 0.35 * occ_v[fdw] - np.where(ftyp == "shared", 0.55, 0.0)))
    W["follow_pos"], W["follow_contact"], W["follow_vacant"] = fo, contact, vac

    # ---------------------------------------------------------------- clerical review subsample
    nat = P.view("nat")[resp]
    gn = rng.choice(np.where(nat == 0)[0], size=PR.GOLD["national"], replace=False)
    gx = rng.choice(np.where(nat == 1)[0], size=PR.GOLD["nonnational"], replace=False)
    W["gold_pos"] = np.r_[gn, gx]
    return W


if __name__ == "__main__":
    import time
    t = time.time()
    W = WD.build()
    build(W)
    print("%.1fs blocks %d sampled %d survey %d follow-up %d" % (time.time() - t, len(W["blocks"]["dist"]),
          W["block_sel"].sum(), len(W["survey_pid"]), len(W["follow_pos"])))
    cls = W["rec_class"]
    print("record classes", np.bincount(cls))
