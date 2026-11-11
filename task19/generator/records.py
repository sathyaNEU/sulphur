"""task19 records: every row each system holds, built from the simulated world (no file is written here).

Addresses and postcodes for every dwelling, the practices, each person's name, and the rows of the register extract,
the coverage survey, its follow-up and clerical review, the border system, civil registration, the defence return,
the population accounts, the 2021 census tables and link study, the list-size series and the enrolment return."""
import datetime as dt

import numpy as np
import pandas as pd

import names as NM
import params as PR
import world as WD

STREET_A = ["Church", "Main", "Mill", "Bridge", "Station", "Chapel", "Abbey", "Castle", "Market", "Green", "Park",
            "River", "Harbour", "Strand", "Hill", "Glebe", "Fair", "Convent", "College", "Quay", "Rock", "Well", "Pound",
            "Forge", "Orchard", "Meadow", "Ash", "Oak", "Beech", "Hazel", "Rowan", "Willow", "Elm", "Holly", "Larch",
            "Kiln", "Ferry", "Tower", "Cross", "Manor", "Sea", "Shore", "Bay", "Cliff", "Lough", "Bog", "Moor", "Glen",
            "Ard", "Knock", "Carrig", "Drum", "Kil", "Rath", "Bally", "Lis", "Dun", "Clon", "Tully", "Gort", "Inch"]
STREET_B = ["Street", "Road", "Lane", "Avenue", "Park", "Terrace", "Court", "Crescent", "Drive", "Close", "Grove", "View",
            "Heights", "Way", "Square", "Rise", "Row", "Place", "Walk", "Gardens", "Meadows", "Green"]
POST_LET = "ABDEFGHJLNPQRSTUWXYZ"
CITIZEN = {1: ["PL", "PL", "PL", "LT", "LT", "RO", "RO", "LV", "SK"], 2: ["IN", "IN", "BD", "BD", "PK", "LK"],
           3: ["SY", "SY", "IQ", "IR", "EG", "SD", "JO"], 4: ["BR", "BR", "BR", "CO", "MX", "AR"],
           5: ["DE", "FR", "IT", "ES", "NL", "PT", "BE"]}
EPOCH = PR.EPOCH


def ddmmyyyy(d, m, y):
    return "%02d/%02d/%04d" % (d, m, y)


def iso(n):
    return PR.date_of(n).isoformat()


def dmy(n):
    x = PR.date_of(n)
    return "%02d/%02d/%04d" % (x.day, x.month, x.year)


def khs_numbers(rng, n):
    """Ten-digit numbers whose last digit is a modulus-11 check on the first nine."""
    out, seen = [], set()
    w = np.arange(10, 1, -1)
    while len(out) < n:
        cand = rng.integers(100_000_000, 999_999_999, size=int((n - len(out)) * 1.3) + 10)
        for c in cand:
            if c in seen:
                continue
            digits = np.array(list(str(c)), int)
            r = 11 - int((digits * w).sum() % 11)
            if r == 11:
                r = 0
            if r == 10:
                continue
            seen.add(c)
            s = "%d%d" % (c, r)
            out.append("%s %s %s" % (s[:3], s[3:6], s[6:]))
            if len(out) == n:
                break
    return out


def build(W):
    rng = np.random.default_rng(PR.SEED + 5)
    P, R = W["P"], W["R"]
    dwell, blocks = W["dwell"], W["blocks"]
    nb = len(blocks["dist"])
    nd_ = len(dwell["dist"])
    # ------------------------------------------------------------------ blocks, streets, postcodes, addresses
    bcode = []
    cnt = {}
    for b in range(nb):
        di = blocks["dist"][b]
        pc = PR.DISTRICTS[di][2]
        cnt[pc] = cnt.get(pc, 0) + 1
        bcode.append("%s-%04d" % (pc, cnt[pc] * 3 + int(rng.integers(0, 3))))
    W["block_code"] = np.array(bcode)
    street_of_block = {}
    used = {}
    for b in range(nb):
        di = blocks["dist"][b]
        k = int(rng.integers(1, 4))
        names = []
        for _ in range(k):
            for _try in range(20):
                nm = "%s %s" % (STREET_A[rng.integers(len(STREET_A))], STREET_B[rng.integers(len(STREET_B))])
                if (di, nm) not in used or used[(di, nm)] < 3:
                    break
            used[(di, nm)] = used.get((di, nm), 0) + 1
            names.append(nm)
        street_of_block[b] = names
    # postcodes: each block's dwellings carry one to three postcodes in the district's sectors
    pcs = {}
    dw_pc = np.empty(nd_, dtype=object)
    dw_addr = np.empty(nd_, dtype=object)
    order = np.argsort(dwell["block"], kind="stable")
    bstart = np.searchsorted(dwell["block"][order], np.arange(nb))
    bend = np.searchsorted(dwell["block"][order], np.arange(nb), side="right")
    for b in range(nb):
        di = blocks["dist"][b]
        area = PR.DISTRICTS[di][2]
        members = order[bstart[b]:bend[b]]
        sector = 1 + (b % 9)
        n_pc = max(1, int(np.ceil(len(members) / rng.integers(10, 18))))
        codes = []
        for _ in range(n_pc):
            while True:
                c = "%s%d %d%s%s" % (area, sector, rng.integers(1, 10), POST_LET[rng.integers(len(POST_LET))],
                                      POST_LET[rng.integers(len(POST_LET))])
                if c not in pcs:
                    pcs[c] = di
                    codes.append(c)
                    break
        streets = street_of_block[b]
        num = {s: int(rng.integers(1, 6)) for s in streets}
        for j, dwi in enumerate(members):
            s = streets[j % len(streets)]
            t = dwell["type"][dwi]
            if t == "communal":
                dw_addr[dwi] = "Block %s, Larrick Barracks" % "ABCDEFGH"[j % 8] if area == "FL" else "%s House, %s" % (s.split()[0], s)
            elif t == "flat":
                dw_addr[dwi] = "Flat %d, %d %s" % (int(rng.integers(1, 9)), num[s], s)
                if rng.random() < 0.7:
                    num[s] += int(rng.integers(1, 3))
            else:
                dw_addr[dwi] = "%d %s" % (num[s], s)
                num[s] += int(rng.choice([1, 2, 2, 3]))
            dw_pc[dwi] = codes[min(len(codes) - 1, j * len(codes) // max(1, len(members)))]
    # 2024 recoding: some sectors in three districts were split, the old codes kept on records registered before
    recode = {}
    for pc_old, di in list(pcs.items()):
        if PR.DISTRICTS[di][2] in ("PA", "BR", "NB") and pc_old[-3] in "12" and rng.random() < 0.55:
            while True:
                c = pc_old[:-3] + "%d%s%s" % (rng.integers(1, 10), POST_LET[rng.integers(len(POST_LET))],
                                             POST_LET[rng.integers(len(POST_LET))])
                if c not in pcs and c not in recode.values():
                    break
            recode[pc_old] = c
    for dwi in range(nd_):
        if dw_pc[dwi] in recode:
            dw_pc[dwi] = recode[dw_pc[dwi]]
    W["dw_pc"], W["dw_addr"], W["pc_recode"] = dw_pc, dw_addr, recode
    pc_rows = []
    for pc_old, di in pcs.items():
        d = PR.DISTRICTS[di]
        if pc_old in recode:
            pc_rows.append([pc_old, d[0], d[1], "1998-01-01" if rng.random() < 0.8 else "2009-06-01", "2024-04-01"])
            pc_rows.append([recode[pc_old], d[0], d[1], "2024-04-01", ""])
        else:
            pc_rows.append([pc_old, d[0], d[1], "1998-01-01" if rng.random() < 0.7 else
                            ["2006-03-01", "2012-09-01", "2017-05-01", "2021-11-01"][rng.integers(4)], ""])
    pcd = pd.DataFrame(pc_rows, columns=["postcode", "district_code", "district_name", "date_introduced",
                                         "date_terminated"]).sort_values("postcode").reset_index(drop=True)
    W["postcodes"] = pcd

    # ------------------------------------------------------------------ practices
    prac = []
    for di, d in enumerate(PR.DISTRICTS):
        k = max(3, int(round(d[4] / 9000)))
        for j in range(k):
            s = "%s %s" % (STREET_A[rng.integers(len(STREET_A))], STREET_B[rng.integers(len(STREET_B))])
            kind = ["Medical Centre", "Surgery", "Health Centre", "Family Practice", "Medical Practice", "Clinic"][rng.integers(6)]
            nm = "%s %s" % (s.split()[0], kind) if rng.random() < 0.5 else "%s %s" % (d[1], kind) if j == 0 else "%s %s" % (s, kind)
            prac.append(["K%d%04d" % (8 + (di % 2), int(rng.integers(1000, 9999))), nm, di])
    pr_codes = [p[0] for p in prac]
    if len(set(pr_codes)) != len(pr_codes):
        for i, p in enumerate(prac):
            p[0] = "K%d%04d" % (8 + i % 2, 1000 + 61 * i)
    prac_by_d = {di: [i for i, p in enumerate(prac) if p[2] == di] for di in range(WD.ND)}
    W["practices"] = prac

    # ------------------------------------------------------------------ people: canonical names
    N = NM.Names(PR.SEED + 9)
    n = P.n
    sex, origin = P.view("sex"), P.view("origin")
    citizen = W["citizen"]
    canon = [N.canonical(int(sex[i]), int(origin[i]), citizen[i]) for i in range(n)]
    # surname changed at marriage after the register record was made: kept as the maiden name on old records
    age_ref = WD.ages_at(P.view("dob"), PR.REF)
    married = W["married"]
    maiden = {}
    for i in np.where(married)[0]:
        maiden[i] = N.nat_l[rng.integers(len(N.nat_l))] if origin[i] == 0 else canon[i]["l"] + "-" + N.nat_l[rng.integers(len(N.nat_l))]
    W["canon"], W["maiden"] = canon, maiden

    # ------------------------------------------------------------------ register extract
    o = W["rec_open"]
    rec_dw = W["rec_dw"]
    numbers = khs_numbers(rng, R.n)
    W["khs"] = numbers
    rows = []
    nrec = len(o)
    rpid = R.pid[o]
    for j in range(nrec):
        rid = o[j]
        p = int(rpid[j])
        f, l = N.render(canon[p], int(sex[p]), int(origin[p]), int(age_ref[p]), "register")
        if p in maiden and R.reg[rid] < PR.REF - 3 * 365:
            l = maiden[p]
        dd, mm, yy = NM.dob_variant(N.rng, int(P.dob[p]), int(origin[p]), "register")
        dwi = rec_dw[j]
        pc = dw_pc[dwi]
        di = R.dist[rid]
        # the practice: usually in the district of the address
        if rng.random() < 0.92:
            pi = prac_by_d[di][rng.integers(len(prac_by_d[di]))]
        else:
            pi = int(rng.integers(len(prac)))
        last = int(R.last[rid])
        last_s = dmy(last) if last > R.reg[rid] + 3 else ""
        rows.append([numbers[rid], l, f, "M" if sex[p] == 1 else "F",
                     ddmmyyyy(dd, mm, yy), dw_addr[dwi], pc, prac[pi][0], dmy(int(R.reg[rid])), last_s])
    reg = pd.DataFrame(rows, columns=["khs_number", "surname", "forenames", "sex", "date_of_birth", "address_line_1",
                                      "postcode", "practice_code", "registration_date", "last_attended"])
    # postcodes: records registered before the 2024 recoding often still carry the old code
    inv = {v: k for k, v in recode.items()}
    regdate = R.reg[o]
    old_ok = (regdate < PR.day(2024, 4, 1)) & (rng.random(nrec) < 0.62)
    pcs_col = reg["postcode"].values.copy()
    for j in np.where(old_ok)[0]:
        if pcs_col[j] in inv:
            pcs_col[j] = inv[pcs_col[j]]
    # keying conventions differ between practices' systems
    style = rng.random(nrec)
    pcs_col = [c.replace(" ", "") if style[j] < 0.06 else (c.lower() if style[j] < 0.09 else c)
               for j, c in enumerate(pcs_col)]
    reg["postcode"] = pcs_col
    # the extract's order: by practice, then registration
    reg["_p"] = reg["practice_code"]
    reg["_r"] = regdate
    reg = reg.sort_values(["_p", "_r"], kind="stable").drop(columns=["_p", "_r"]).reset_index(drop=True)
    W["register_df"] = reg
    W["rec_index"] = {numbers[o[j]]: j for j in range(nrec)}   # khs number to position in the open arrays

    # practices file
    prow = []
    for p in prac:
        di = p[2]
        pool = np.where(dwell["dist"] == di)[0]
        dwi = pool[rng.integers(len(pool))]
        prow.append([p[0], p[1], dw_pc[dwi], PR.DISTRICTS[di][0]])
    W["practice_df"] = pd.DataFrame(prow, columns=["practice_code", "practice_name", "postcode", "district_code"])

    # ------------------------------------------------------------------ the coverage survey
    sp = W["survey_pid"]
    dw_of = W["dw_of"]
    blk_of_dw = dwell["block"]
    rows = []
    pnum = {}
    # number dwellings within each block in street order
    blk_dw = {}
    for p in sp:
        dwi = int(dw_of[p])
        blk_dw.setdefault(int(blk_of_dw[dwi]), set()).add(dwi)
    dwno = {}
    for b, s in blk_dw.items():
        for k, dwi in enumerate(sorted(s, key=lambda x: (dw_addr[x], x))):
            dwno[dwi] = k + 1
    survey_ids = []
    for p in sp:
        p = int(p)
        dwi = int(dw_of[p])
        b = int(blk_of_dw[dwi])
        pnum[dwi] = pnum.get(dwi, 0) + 1
        f, l = N.render(canon[p], int(sex[p]), int(origin[p]), int(age_ref[p]), "survey")
        dd, mm, yy = NM.dob_variant(N.rng, int(P.dob[p]), int(origin[p]), "survey")
        if rng.random() < PR.SURVEY_DOB_TYPO["nonnational" if origin[p] else "national"]:
            dd, mm, yy = NM.proxy_dob(rng, dd, mm, yy)
        if origin[p] in (1, 2, 3) and rng.random() < PR.NAME_ORDER_SWAP:
            f, l = l, f
        if age_ref[p] >= 18 and rng.random() < PR.SURVEY_INITIAL["shared" if dwell["type"][dwi] == "shared" else "other"]:
            f = f[0]
        cit = "KV" if origin[p] == 0 else W["citizen"][p]
        if origin[p] != 0:
            rng.integers(len(CITIZEN[int(origin[p])]))     # the draw the survey's own coding once took, kept for the stream
        if origin[p] != 0 and rng.random() < 0.04:
            cit = "KV"      # naturalised
        pid = "%s-%03d-%02d" % (bcode[b], dwno[dwi], pnum[dwi])
        survey_ids.append(pid)
        iv = PR.SURVEY_START + int(rng.integers(0, PR.SURVEY_END - PR.SURVEY_START))
        rows.append([pid, bcode[b], dwno[dwi], pnum[dwi], f, l, "Male" if sex[p] == 1 else "Female",
                     "%04d-%02d-%02d" % (yy, mm, dd), cit, "Y" if P.forces[p] else "", "Y" if P.student[p] else "",
                     dw_addr[dwi], dw_pc[dwi], iso(iv)])
    surv = pd.DataFrame(rows, columns=["person_id", "block_id", "dwelling_no", "person_no", "forename", "surname", "sex",
                                       "date_of_birth", "citizenship", "defence_forces", "student", "address", "postcode",
                                       "interview_date"])
    W["survey_df"], W["survey_ids"] = surv, survey_ids

    # survey design: every block, its district, dwellings listed, selected or not
    ndw_b = np.bincount(dwell["block"], minlength=nb)
    frac = W["block_frac"]
    brow = []
    for b in range(nb):
        di = blocks["dist"][b]
        brow.append([bcode[b], PR.DISTRICTS[di][0], int(ndw_b[b]), "Y" if W["block_sel"][b] else "N",
                     round(float(frac[di]), 6)])
    W["blocks_df"] = pd.DataFrame(brow, columns=["block_id", "district_code", "dwellings_listed", "selected",
                                                 "selection_probability"])

    # ------------------------------------------------------------------ the follow-up of listed records
    fo = W["follow_pos"]
    contact = W["follow_contact"]
    vac = W["follow_vacant"]
    cls = W["rec_class"]
    frows = []
    truth_ce = []
    for k, j in enumerate(fo):
        rid = o[j]
        p = int(rpid[j])
        dwi = rec_dw[j]
        b = int(blk_of_dw[dwi])
        c = int(cls[j])
        out, mv_to, left_y, dup_of = "", "", "", ""
        visits = int(rng.integers(1, 4)) if contact[k] else 3 + int(rng.random() < 0.4)
        nk_draw, known_draw, year_draw = rng.random(), rng.random(), rng.random()
        if c == 1:
            # the Office's desk check finds a second registration for the same person, whatever the visit gave
            cur_d = [jj for jj in W["person_open"].get(p, []) if jj != j and cls[jj] == 0]
            out = "duplicate registration"
            dup_of = numbers[o[cur_d[0]]] if cur_d else ""
        elif vac[k]:
            out = "address vacant" if contact[k] else "no contact"
        elif not contact[k]:
            out = "no contact"
        elif c == 0 and not R.stale_within[rid]:
            out = "resident at address"
        elif nk_draw < PR.FOLLOW_NOT_KNOWN:
            # the household can say only that the person does not live there
            out = "not known at address"
        elif c in (0, 2):
            out = "moved, now elsewhere in Kilvarra"
            mv_to = PR.DISTRICTS[int(P.dist[p])][0] if known_draw < 0.80 else ""
        elif c == 3:
            out = "left Kilvarra"
            left_y = PR.date_of(int(P.leave[p])).strftime("%Y-%m") if year_draw < 0.70 else ""
        else:
            out = "died"
        ftype = dwell["type"][dwi]
        fd = PR.FOLLOW_START + int(rng.integers(0, PR.FOLLOW_END - PR.FOLLOW_START))
        frows.append([numbers[rid], bcode[b], ftype, visits, out, mv_to, left_y, dup_of, iso(fd)])
    fol = pd.DataFrame(frows, columns=["khs_number", "block_id", "dwelling_type", "visits", "outcome",
                                       "moved_to_district", "left_kilvarra_month", "duplicate_of", "followup_date"])
    fol = fol.sort_values(["block_id", "khs_number"]).reset_index(drop=True)
    W["followup_df"] = fol

    # ------------------------------------------------------------------ clerical review subsample
    gp = W["gold_pos"]
    grows = []
    for k in gp:
        p = int(sp[k])
        recs = W["person_open"].get(p, [])
        cur = [jj for jj in recs if cls[jj] == 0]
        pick = cur[0] if cur else (sorted(recs, key=lambda jj: -int(R.reg[o[jj]]))[0] if recs else None)
        rd = PR.REF + 60 + int(rng.integers(0, 50))
        grows.append([survey_ids[k], "matched" if pick is not None else "no record found",
                      numbers[o[pick]] if pick is not None else "", iso(rd)])
    gold = pd.DataFrame(grows, columns=["person_id", "review_outcome", "khs_number", "review_date"])
    W["gold_df"] = gold.sort_values("person_id").reset_index(drop=True)
    return W


def person_open_index(W):
    """{person index: [positions in the open-record arrays]}."""
    R = W["R"]
    o = W["rec_open"]
    out = {}
    for j, p in enumerate(R.pid[o]):
        out.setdefault(int(p), []).append(j)
    W["person_open"] = out
    return out


AGE5 = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
        "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]
PERMIT = ["work", "work", "work", "family", "study", "protection"]


def citizenship(W):
    """Each person's citizenship as the survey and the border system record it (one draw per person)."""
    rng = np.random.default_rng(PR.SEED + 6)
    P = W["P"]
    origin = P.view("origin")
    cit = np.array(["KV"] * P.n, dtype=object)
    for o_, pool in CITIZEN.items():
        idx = np.where(origin == o_)[0]
        cit[idx] = np.array(pool, dtype=object)[rng.integers(0, len(pool), len(idx))]
    W["citizen"] = cit
    return cit


def build_other(W):
    rng = np.random.default_rng(PR.SEED + 8)
    P, R = W["P"], W["R"]
    N = NM.Names(PR.SEED + 10)
    canon, maiden = W["canon"], W["maiden"]
    sex, origin, dob = P.view("sex"), P.view("origin"), P.view("dob")
    cit = W["citizen"]
    out = {}

    # ---------------------------------------------------------------- civil registration
    # births in Kilvarra by calendar year and sex: before mid-2021 from the cohorts living here then, carried back
    # through survival and the cohort's small net emigration since; from mid-2021 the births the simulation made
    res2021 = W["res2021"]
    nat21 = res2021[(P.view("nat")[res2021] == 0)]
    by = np.array([PR.date_of(int(d)).year for d in dob[nat21]])
    bm = np.array([PR.date_of(int(d)).month for d in dob[nat21]])
    a21 = WD.ages_at(dob[nat21], PR.T0)
    surv = np.where(sex[nat21] == 1, WD.SURV_M[np.clip(a21, 0, 100)], WD.SURV_F[np.clip(a21, 0, 100)])
    wt = (1.0 + 0.0035 * np.minimum(a21, 45)) / surv
    births = {}
    for y in range(1955, 2022):
        for s_ in (1, 0):
            m = (by == y) & (sex[nat21] == s_) & ((y < 2021) | (bm <= 6))
            births[(y, s_)] = float(wt[m].sum())
    sim_births = np.where((P.view("born_here")) & (dob > PR.T0) & (dob <= PR.REF))[0]
    for p in sim_births:
        y = PR.date_of(int(dob[p])).year
        births[(y, int(sex[p]))] = births.get((y, int(sex[p])), 0.0) + 1.0
    brow = []
    for y in range(1955, 2027):
        m_, f_ = births.get((y, 1), 0.0), births.get((y, 0), 0.0)
        if y < 2021:
            m_, f_ = rng.poisson(m_), rng.poisson(f_)
        brow.append([y if y < 2026 else "2026 (January to June)", int(round(m_)), int(round(f_)), int(round(m_)) + int(round(f_))])
    out["births"] = pd.DataFrame(brow, columns=["Year of registration", "Males", "Females", "Total"])
    drow = []
    for y in PR.YEARS:
        db = W["components"][y]["deaths_by"]
        for g in range(19):
            drow.append(["%d-%02d" % (y - 1, y % 100), AGE5[g], int(db[2 * g + 1]), int(db[2 * g])])
    out["deaths"] = pd.DataFrame(drow, columns=["Year to 30 June", "Age at death", "Males", "Females"])
    a = np.arange(101)
    qm = WD.mortality(a, np.ones(101, int))
    qf = WD.mortality(a, np.zeros(101, int))
    lm = 100000 * np.concatenate([[1.0], np.cumprod(1 - qm)[:-1]])
    lf = 100000 * np.concatenate([[1.0], np.cumprod(1 - qf)[:-1]])
    out["lifetable"] = pd.DataFrame({"Age": [str(x) if x < 100 else "100+" for x in a], "qx males": np.round(qm, 6),
                                     "lx males": np.round(lm).astype(int), "qx females": np.round(qf, 6),
                                     "lx females": np.round(lf).astype(int)})

    # ---------------------------------------------------------------- border movements of non-national permit holders
    rows = []
    arr = np.where((P.view("nat") == 1) & (P.view("arrive") > PR.T0) & ~P.view("born_here") & (P.view("status") != 9))[0]
    for p in arr:
        f, l = N.render(canon[p], int(sex[p]), int(origin[p]), 30, "border")
        dd, mm, yy = NM.dob_variant(N.rng, int(dob[p]), int(origin[p]), "border")
        rows.append([f, l, "M" if sex[p] == 1 else "F", ddmmyyyy(dd, mm, yy), cit[p], "arrival", int(P.arrive[p]),
                     PERMIT[rng.integers(len(PERMIT))], ["Port Ardain Airport", "Port Ardain Airport", "Ballinrea Ferry Port"][rng.integers(3)]])
    dep = np.where((P.view("nat") == 1) & (P.view("status") == 1) & P.view("border_dep"))[0]
    for p in dep:
        f, l = N.render(canon[p], int(sex[p]), int(origin[p]), 30, "border")
        dd, mm, yy = NM.dob_variant(N.rng, int(dob[p]), int(origin[p]), "border")
        rows.append([f, l, "M" if sex[p] == 1 else "F", ddmmyyyy(dd, mm, yy), cit[p], "departure", int(P.leave[p]),
                     "", ["Port Ardain Airport", "Port Ardain Airport", "Ballinrea Ferry Port"][rng.integers(3)]])
    bd = pd.DataFrame(rows, columns=["forenames", "surname", "sex", "date_of_birth", "nationality", "movement", "_d",
                                     "permit_type", "port"])
    bd = bd.sort_values("_d", kind="stable").reset_index(drop=True)
    bd.insert(0, "movement_ref", ["KBA%08d" % (40_000_000 + 37 * i + int(rng.integers(0, 37))) for i in range(len(bd))])
    bd.insert(7, "movement_date", [iso(int(d)) for d in bd["_d"]])
    out["border"] = bd.drop(columns=["_d"])

    # ---------------------------------------------------------------- the defence return
    srv = np.where((P.view("status") == 0) & P.view("forces"))[0]
    sa = WD.ages_at(dob[srv], PR.REF)
    bands = [(18, 24, "18-24"), (25, 29, "25-29"), (30, 34, "30-34"), (35, 39, "35-39"), (40, 120, "40 and over")]
    drows = []
    for lo, hi, lab in bands:
        for s_, sl in ((1, "Male"), (0, "Female")):
            drows.append(["Larrick Barracks, Fort Larrick", sl, lab, int(((sa >= lo) & (sa <= hi) & (sex[srv] == s_)).sum())])
    out["defence"] = pd.DataFrame(drows, columns=["unit_location", "sex", "age_band", "personnel"])

    # ---------------------------------------------------------------- population accounts (the rolled-forward series)
    t21 = W["truth2021"]
    base = int(round(t21["census_estimate_total"]))
    rows = []
    pop = base
    for y in PR.YEARS:
        c = W["components"][y]
        imm_nn = int(c["imm_rec_nn"])
        imm_kv = int(c["imm_rec"] - c["imm_rec_nn"])
        close = pop + c["births"] - c["deaths"] + imm_nn + imm_kv - c["emig_rec"]
        rows.append(["%d-%02d" % (y - 1, y % 100), pop, c["births"], c["deaths"], imm_nn, imm_kv, c["emig_rec"], close])
        pop = close
    out["accounts"] = pd.DataFrame(rows, columns=["Year to 30 June", "Population at start", "Births", "Deaths",
                                                  "Immigration: non-nationals", "Immigration: returning Kilvarrans",
                                                  "Emigration", "Population at end"])
    W["official_2026"] = pop

    # ---------------------------------------------------------------- 2021 census tables (coverage-adjusted)
    out["census"] = t21["table"]

    # ---------------------------------------------------------------- 2021 register and census link study
    n21 = W["records2021"]
    take = np.where(rng.random(n21) < 0.5)[0]
    enum = np.zeros(P.n, bool)
    enum[W["census_enum"]] = True
    dist21 = np.full(P.n, -1, np.int16)
    dist21[res2021] = W["dist2021"]
    rows = []
    for rid in take:
        p = int(R.pid[rid])
        a = int(WD.ages_at(np.array([dob[p]]), PR.CENSUS)[0])
        if a < 0:
            continue
        yr_reg = (PR.CENSUS - int(R.reg[rid])) / 365.25
        yr_last = (PR.CENSUS - int(W["last2021"][rid])) / 365.25
        if enum[p] and dist21[p] == R.dist[rid]:
            outc = "enumerated in district"
        elif enum[p]:
            outc = "enumerated elsewhere in Kilvarra"
        else:
            outc = "not enumerated"
        rows.append([PR.DISTRICTS[int(R.dist[rid])][0], AGE5[min(18, a // 5)], "M" if sex[p] == 1 else "F",
                     round(max(0.0, yr_reg), 1), round(max(0.0, yr_last), 1), outc])
    out["link2021"] = pd.DataFrame(rows, columns=["district_code", "age_group", "sex", "years_registered",
                                                  "years_since_last_attendance", "census_outcome"])

    # ---------------------------------------------------------------- quarterly list sizes (from mid-2021)
    qends = [PR.day(y, m, 30 if m in (6, 9) else 31) for y in range(2021, 2027) for m in (3, 6, 9, 12)
             if PR.day(y, m, 28) >= PR.T0 and PR.day(y, m, 28) <= PR.REF]
    nR = R.n
    reg_d = R.view("reg")
    closed = np.where(R.view("open"), 10 ** 7, R.view("closed"))
    rdist = R.view("dist")
    rsex = sex[R.view("pid")]
    rdob = dob[R.view("pid")]
    rows = []
    for q in qends:
        on = (reg_d <= q) & (closed > q)
        ag = WD.ages_at(rdob[on], q)
        grp = np.digitize(ag, [18, 45, 65])
        key = rdist[on].astype(int) * 8 + grp * 2 + rsex[on]
        cnt = np.bincount(key, minlength=12 * 8)
        for di in range(12):
            for g, lab in enumerate(["0-17", "18-44", "45-64", "65+"]):
                for s_, sl in ((1, "M"), (0, "F")):
                    rows.append([iso(q), PR.DISTRICTS[di][0], lab, sl, int(cnt[di * 8 + g * 2 + s_])])
    out["listsize"] = pd.DataFrame(rows, columns=["quarter_end", "district_code", "age_group", "sex", "patients_registered"])

    # ---------------------------------------------------------------- higher education enrolments 2025/26
    st = np.where((P.view("status") == 0) & P.view("student"))[0]
    dw_of, dw_pc = W["dw_of"], W["dw_pc"]
    dwell = W["dwell"]
    rows = []
    for p in st:
        f, l = N.render(canon[p], int(sex[p]), int(origin[p]), 20, "he")
        hd = int(P.home[p])
        pool = np.where(dwell["dist"] == hd)[0]
        home_pc = dw_pc[pool[rng.integers(len(pool))]]
        inst = "University of Kilvarra (Drumcastle)" if P.dist[p] == WD.UNI_IDX[0] else "Tullaghvane Institute of Technology"
        rows.append(["%07d" % int(rng.integers(1_000_000, 9_999_999)), l, f, iso(int(dob[p])), "M" if sex[p] == 1 else "F",
                     inst, int(rng.integers(1, 5)), "full-time", dw_pc[dw_of[p]], home_pc])
    out["he"] = pd.DataFrame(rows, columns=["student_no", "surname", "forenames", "date_of_birth", "sex", "institution",
                                            "year_of_study", "mode", "term_time_postcode", "home_postcode"])
    W["other"] = out
    return out
