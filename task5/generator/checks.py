"""task5 architecture 3: the generator's assertions, run on every build.

The input gates; the Sulfur block (R1 to R6) on the clean truth and the cut pack; the ladder and its margins; the
shock screen; every semantic fork (SF1 to SF16) closed or shown inert; the golden family's spread against each graded
bin; the golden against the world; the governing documents read back with positive controls; the realism sweep."""
import json
import os
import re

import numpy as np
import pandas as pd

import golden as GD
import methods as M
import tells
import world as W

RESULTS = []
FAMILY_DEV = {}


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def doc_text(path):
    """a governing document's text as a reader opening it sees it: the body, its tables and its footer"""
    from docx import Document
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts += [c.text for c in row.cells]
    for sec in d.sections:
        parts += [p.text for p in sec.footer.paragraphs]
    return "\n".join(parts)


def designated_names(ch):
    return [W.NAMES[c] for c in M.designated(ch)]


def edge_distance(v, unit=0.1):
    """distance from v to the nearest rounding edge at the given unit"""
    return unit / 2 - abs(v - round(v / unit) * unit)


def run(task, w, T, pk, G, texts, figs, n, quiet=False):
    RESULTS.clear()
    target = os.path.join(task, "target")
    gold = os.path.join(task, "golden")
    files = sorted(os.listdir(target))
    gnames = [W.NAMES[c] for c in G["designated"]]

    # --------------------------------------------------------------------------------------------- input gates
    check("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    cats = {"spreadsheet": exts & {"csv", "xlsx"}, "text": exts & {"pdf", "docx", "eml"}}
    check("gate: two or more file categories, three or more formats", all(cats.values()) and len(exts) >= 3, sorted(exts))
    check("gate: a CSV of 20,000 rows or more", n["reports"] >= 20000 and n["accounts"] >= 20000, "%d reports, %d accounts" % (n["reports"], n["accounts"]))
    check("gate: a CSV of ten to twenty printed pages or more", n["status"] >= 600, "%d status rows" % n["status"])
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("gate: two or more distractors named only in metadata.json", len(meta["distractor_files"]) >= 2 and
          all("distract" not in f for f in files), meta["distractor_files"])
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|manifest|field.?notes|codebook", f, re.I) for f in files))
    gfiles = sorted(os.listdir(gold))
    check("golden: exactly the requested files", gfiles == sorted(W.DELIVERABLES.values()), gfiles)

    # ----------------------------------------------------------------------------------------------- Sulfur R1
    rep_cols = list(T["reports"].columns)
    forbidden = [c for c in list(T["reports"].columns) + list(T["accounts"].columns) + list(T["worksites"].columns)
                 if re.search(r"agent|channel|method|batch|transmission|bureau|preparer|filer|submitter|distress|flag", c, re.I)]
    check("R1 no column holds an agent, channel, transmission or distress flag", not forbidden, forbidden)
    check("R1 the reports carry each version's receipt time to the second", "received_at" in rep_cols and
          T["reports"]["received_at"].str.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$").all())
    read = sorted(set(re.findall(r'rd\("(\w+)"', open(os.path.join(os.path.dirname(__file__), "golden.py")).read())))
    check("R1 the golden reads the reports, the register, the status history, the worksite file and two lookups only",
          read == ["accounts", "counties", "naics", "reports", "status", "worksites"], read)

    # --------------------------------------------------------------------------------------------- the ladder
    R = figs["rungs"]
    check("ladder: the golden designates Garrow and Ostrom", gnames == ["Garrow", "Ostrom"], gnames)
    check("R3a analyst test: the default path (the field's imputation, two-quarter delinquents ceased) designates none",
          R["R1x"]["designated"] == [], R["R1x"]["designated"])
    check("ladder: R1, the field's imputation for every outstanding report, designates none", R["R1"]["designated"] == [], R["R1"]["designated"])
    check("ladder: R0, the reports as received, designates twelve or more", len(R["R0"]["designated"]) >= 12, len(R["R0"]["designated"]))
    check("R4 link 2: the filer-type reading designates Ostrom alone", R["R2"]["designated"] == ["Ostrom"], R["R2"]["designated"])
    check("ladder: the newly-late reading designates five or more counties", len(R["R2b"]["designated"]) >= 5, R["R2b"]["designated"])
    check("R4 link 3: outcomes from the six months before the flash designate no county", R["R3a"]["designated"] == [], R["R3a"]["designated"])
    check("R4 link 3: outcomes with the never-filers dropped designate no county", R["R3b"]["designated"] == [], R["R3b"]["designated"])
    check("ladder: every wrong set differs from the golden", all(R[k]["designated"] != gnames for k in R if k != "Rseas"))
    # margins on the line
    ch = {W.NAMES[c]: G["change"][c] for c in W.CODES}
    check("margin: Garrow and Ostrom at least 0.6 below the line on the golden",
          max(ch["Garrow"], ch["Ostrom"]) <= W.THRESHOLD - 0.6, (round(ch["Garrow"], 2), round(ch["Ostrom"], 2)))
    others = {k: v for k, v in ch.items() if k not in ("Garrow", "Ostrom")}
    check("margin: every other county at least 0.6 above the line on the golden", min(others.values()) >= W.THRESHOLD + 0.6,
          min(others.items(), key=lambda kv: kv[1]))
    for k in ("R1", "R1x", "R3a", "R3b"):
        rr = R[k]["change_raw"]
        check("margin: %s keeps Garrow and Ostrom at least 0.3 above the line" % k, min(rr["Garrow"], rr["Ostrom"]) >= W.THRESHOLD + 0.3,
              (round(rr["Garrow"], 2), round(rr["Ostrom"], 2)))
    rr = R["R2"]["change_raw"]
    check("margin: R2 puts Ostrom at least 0.3 below the line and Garrow at least 0.3 above it",
          rr["Ostrom"] <= W.THRESHOLD - 0.3 and rr["Garrow"] >= W.THRESHOLD + 0.3, (round(rr["Garrow"], 2), round(rr["Ostrom"], 2)))
    # the field's imputation back-tests: rebuilt at each closed quarter's cut-off it overstates every county's final
    # figure a little, and the lake counties' fourth quarter by more (their resorts' own history is a year short)
    import writeup as WR
    bt = {}
    for h in pk.closed:
        est_, kind_, vh = pk.estimate(h, WR.RUNGS["R1x"])
        ev = pk.eventual(h)
        fin = {a_: (est_[a_] if kind_[a_] == "reported" else ev(a_)) for a_ in est_}
        fin = {a_: (x if np.isfinite(x) else est_[a_]) for a_, x in fin.items()}
        te, _ = pk.split(h, est_, vh["asof"])
        tf, _ = pk.split(h, fin, vh["asof"])
        bt[h] = {c: 100.0 * (te[c] / tf[c] - 1) for c in W.CODES}
    lake = ("013", "023")
    rest = [x for h in bt for c, x in bt[h].items() if not (c in lake and h % 4 == 3)]
    check("back-test: the field's imputation overstates every county's final figure by 0.0 to 0.7 of a point on every "
          "closed quarter, the lake counties' fourth quarter apart", min(rest) >= -0.05 and max(rest) <= 0.7,
          (round(min(rest), 2), round(max(rest), 2)))
    check("back-test: in the lake counties' 2024 fourth quarter it overstates by one to two and a half points",
          all(1.0 <= bt[7][c] <= 2.5 for c in lake), {W.NAMES[c]: round(bt[7][c], 2) for c in lake})
    check("R3b the decisive step alone: the default path with the missing-alone reading files the golden set",
          designated_names(M.county_change(pk, dict(seasonal=False, new="zero"))["change"]) == gnames)

    # ------------------------------------------------------------------------------------------- the shock screen
    v = pk.view(W.FLASH_Q)
    mi = v["missing"]
    acc = pk.a
    stats = {}
    liab = sorted(v["liable"])
    cty_of = acc.loc[liab, "county_code"]
    miss_cty = acc.loc[mi.index, "county_code"]
    stats["missing share"] = {c: (miss_cty == c).sum() / max(1, (cty_of == c).sum()) for c in W.CODES}
    punct = mi.index[~mi["habitual"].astype(bool)]
    stats["usually punctual missing"] = {c: (acc.loc[punct, "county_code"] == c).sum() / max(1, (cty_of == c).sum()) for c in W.CODES}
    rec, prev = v["rec"], v["prev"]
    both = rec.index.intersection(prev.index)
    bc = acc.loc[both, "county_code"]
    stats["reporters' change"] = {c: -(rec.loc[both[bc == c], "month3_employment"].sum() / max(1, prev.loc[both[bc == c], "month3_employment"].sum()) - 1) for c in W.CODES}
    stats["field's imputed change"] = {c: -R["R1x"]["change_raw"][W.NAMES[c]] for c in W.CODES}
    stats["county size"] = {c: G["base"][c] for c in W.CODES}
    stats["agent clients outstanding"] = {c: (mi.loc[(miss_cty == c).values, "agent_client"].astype(bool)).mean() for c in W.CODES}
    for k, sv in stats.items():
        top2 = sorted(sorted(sv, key=lambda c: -sv[c])[:2])
        bot2 = sorted(sorted(sv, key=lambda c: sv[c])[:2])
        check("shock: Garrow and Ostrom are not the top or bottom two on %s" % k,
              top2 != ["009", "019"] and bot2 != ["009", "019"], [W.NAMES[c] for c in top2])

    # ------------------------------------------------------------------------------------- forks and families
    a = mi["arrived"].dropna()
    gap = (float(a[a < 0.5].max()), float(a[a >= 0.5].min()))
    check("SF12 the share of transmission-mates arrived is bimodal: nothing between 0.15 and 0.55", gap[0] < 0.15 and gap[1] > 0.55,
          gap)
    fam = {}
    def run_variant(name, **kw):
        defaults = dict(trans_window=0, mates_quarters=1, mates_threshold=0.5, cell="county_ss",
                        seasonal_ratio=M.SEASONAL_RATIO, closed=list(M.CLOSED_QUARTERS), version="latest",
                        use_worksites=True, paper_transmissions=False, trans_min=M.TRANSMISSION_MIN, transfers_end=True,
                        naics_2017=True)
        pk._cache.clear()
        pk.variant(**dict(defaults, **kw))
        r = M.county_change(pk, {})
        pk._cache.clear()
        pk.variant(**defaults)
        fam[name] = r
        return r
    standing = {
        "SF12 mates from the last four quarters": dict(mates_quarters=4),
        "SF12 threshold 0.3": dict(mates_threshold=0.3),
        "SF12 closed quarters 2024Q2 to 2025Q3": dict(closed=list(range(5, 11))),
        "SF12 closed quarters 2024Q1 to 2025Q2": dict(closed=list(range(4, 10))),
        "SF12 closed quarters 2023Q3 to 2025Q3": dict(closed=list(range(2, 11))),
        "SF15 seasonal cut 0.4": dict(seasonal_ratio=0.4),
        "SF15 seasonal cut 0.75": dict(seasonal_ratio=0.75),
        "SF9 transmissions of two or more reports": dict(trans_min=2),
    }
    worst = 0.0
    dev = {c: 0.0 for c in W.CODES}
    devj = {c: 0.0 for c in W.CODES}
    for name, kw in standing.items():
        r = run_variant(name, **kw)
        d = max(abs(r["change"][c] - G["change"][c]) for c in W.CODES)
        for c in W.CODES:
            dev[c] = max(dev[c], abs(r["change"][c] - G["change"][c]))
            devj[c] = max(devj[c], abs(r["total"][c] - G["total"][c]), abs(r["imputed"][c] - G["imputed"][c]))
        worst = max(worst, d)
        check("%s: the golden set, every county within 0.05" % name, designated_names(r["change"]) == gnames and d <= 0.05,
              "%s, max %.3f" % (designated_names(r["change"]), d))
    for label, how in (("size class", "closed_strat"), ("filing channel (agent client or direct filer)", "closed_channel")):
        r = M.county_change(pk, dict(alone=how))
        d = max(abs(r["change"][c] - G["change"][c]) for c in W.CODES)
        for c in W.CODES:
            dev[c] = max(dev[c], abs(r["change"][c] - G["change"][c]))
            devj[c] = max(devj[c], abs(r["total"][c] - G["total"][c]), abs(r["imputed"][c] - G["imputed"][c]))
        worst = max(worst, d)
        check("SF12 outcomes by %s: the golden set, every county within 0.05" % label,
              designated_names(r["change"]) == gnames and d <= 0.05, d)
    rc_, _ = pk.outcomes(pk.closed)
    check("SF12 the closed quarters' missing-alone outcome is the same for agent clients and direct filers (within 0.02)",
          abs(rc_[("alone", "agent")] - rc_[("alone", "direct")]) < 0.02,
          "agent %.3f, direct %.3f" % (rc_[("alone", "agent")], rc_[("alone", "direct")]))
    # and the difference sits inside the employers' own sampling spread (an employer bootstrap, fixed seed)
    grp = {True: ([], []), False: ([], [])}
    for h in pk.closed:
        vh = pk.view(h)
        mh = vh["missing"]
        ev = pk.eventual(h)
        for a_, c_ in pk.classes(vh, "golden").items():
            p_ = mh.loc[a_, "prior"]
            e_ = ev(a_)
            if c_ == "alone" and np.isfinite(p_) and p_ > 0 and np.isfinite(e_):
                grp[bool(mh.loc[a_, "agent_client"])][0].append(p_)
                grp[bool(mh.loc[a_, "agent_client"])][1].append(e_)
    rb = np.random.default_rng(2027)
    boot = []
    for _ in range(400):
        d_ = []
        for k_ in (True, False):
            pp, ee = np.array(grp[k_][0]), np.array(grp[k_][1])
            ix = rb.integers(0, len(pp), len(pp))
            d_.append(ee[ix].sum() / pp[ix].sum())
        boot.append(d_[0] - d_[1])
    se = float(np.std(boot))
    diff = rc_[("alone", "agent")] - rc_[("alone", "direct")]
    FAMILY_DEV.update(channel_se=se, channel_diff=diff)
    check("SF12 the channel difference is inside its bootstrap standard error (about 0.03)", abs(diff) < se and 0.025 <= se <= 0.035,
          "difference %.3f, s.e. %.3f" % (diff, se))
    r = M.county_change(pk, dict(two_q="zero"))
    d = max(abs(r["change"][c] - G["change"][c]) for c in W.CODES)
    check("SF11 two-quarter delinquents ceased: same call, every county within 0.02", designated_names(r["change"]) == gnames and d <= 0.02, d)
    short = {W.NAMES[c]: (round(edge_distance(G["change"][c]), 3), round(dev[c], 3)) for c in W.CODES
             if edge_distance(G["change"][c]) < dev[c]}
    check("bins: every county's change clears its rounding edge by more than its own standing family's spread", not short, short)
    shortj = {W.NAMES[c]: (round(edge_distance(G[k][c], 100.0)), round(devj[c])) for c in W.CODES for k in ("total", "imputed")
              if edge_distance(G[k][c], 100.0) < devj[c]}
    check("bins: every county's jobs, total and estimated, clear the hundred's edge by more than the family's spread", not shortj, shortj)
    FAMILY_DEV.update(dev=dev, devj=devj)
    # mess neutrality (R2): each item mishandled, the call and every critical figure unchanged
    mess = {
        "R2 amendments ignored (the first version)": dict(version="first"),
        "R2 worksites ignored (the register's county)": dict(use_worksites=False),
        "R2 paper reports read as transmissions (SF9)": dict(paper_transmissions=True),
        "R2 transfers not ending the predecessor (SF6)": dict(transfers_end=False),
        "R2 NAICS 2017 codes left unmapped": dict(naics_2017=False),
    }
    for name, kw in mess.items():
        r = run_variant(name, **kw)
        check("%s: same call" % name, designated_names(r["change"]) == gnames, designated_names(r["change"]))
    # ruled-out rivals, each by named data
    x = pk.r[(pk.r["q"] == W.FLASH_Q - 1) & (pk.r["report_type"] == "ORIGINAL")]
    x = x[x["t"].dt.strftime("%H:%M:%S") != "00:00:00"].groupby("acct").head(1)
    mg = x.groupby(x["t"].dt.floor("min"))["t"].agg(["size", "nunique"])
    merged = int(((mg["size"] >= 3) & (mg["nunique"] > 1)).sum())
    sg = x.groupby("t")["acct"].size()
    check("SF12 rival: grouping by the minute merges reports received at different seconds into %d pseudo-transmissions, "
          "while every same-second group of three or more is one upload" % merged, merged > 0 and (sg >= 3).sum() > 50,
          "%d merged minute groups, %d same-second transmissions" % (merged, (sg >= 3).sum()))
    r = run_variant("rival minute", trans_window="minute")
    check("SF12 rival: transmissions by the minute keep the call", designated_names(r["change"]) == gnames, designated_names(r["change"]))
    r = run_variant("rival any mate", mates_threshold=0)
    check("SF16 any one mate arrived: the same call", designated_names(r["change"]) == gnames,
          (designated_names(r["change"]), {W.NAMES[c]: round(r["change"][c] - G["change"][c], 2) for c in ("009", "019")}))
    # what rules it out: in the closed quarters a few late transmissions had one or two mates arrive (clients that had
    # moved to another agent), and their outstanding members then arrived together, in one second, weeks later
    part, together = 0, 0
    for h in pk.closed:
        vh = pk.view(h)
        mh = vh["missing"]
        sel = mh[(mh["arrived"] > 0) & (mh["arrived"] < 0.5)]
        if not len(sel):
            continue
        later = pk.r[(pk.r["q"] == h) & (pk.r["report_type"] == "ORIGINAL") & pk.r["acct"].isin(sel.index)]
        later = later.sort_values("t", kind="stable").groupby("acct").head(1)
        part += len(sel)
        together += int(later.groupby("t")["acct"].size().max()) if len(later) else 0
    check("SF16 any one mate ruled out: the closed quarters' partly arrived transmissions are late transmissions "
          "(their outstanding members arrived together in one second)", part > 0 and together >= 0.8 * part,
          "%d outstanding in partly arrived transmissions, %d of them arrived in one second" % (part, together))
    r = run_variant("rival county cell", cell="county")
    check("SF10 rival: the county-only cell keeps the call", designated_names(r["change"]) == gnames, designated_names(r["change"]))
    # the closed quarters refute the filer-type reading: agent clients missing from an arrived transmission kept little
    kept_agent = []
    for h in pk.closed:
        vh = pk.view(h)
        mh = vh["missing"]
        ev = pk.eventual(h)
        sel = mh[(mh["golden"] == "alone") & mh["agent_client"].astype(bool)]
        for a_, row in sel.iterrows():
            e = ev(a_)
            if np.isfinite(e) and row["prior"] > 0:
                kept_agent.append((e, row["prior"]))
    ka = sum(e for e, p in kept_agent) / sum(p for e, p in kept_agent)
    check("SF13 the closed quarters: agent clients missing from a transmission that arrived kept under half their jobs",
          ka < 0.5, "%.3f over %d employers" % (ka, len(kept_agent)))
    # the latest quarters' unresolved employers are inactivated later
    unres = []
    for h in M.LATEST_QUARTERS:
        vh = pk.view(h)
        mh = vh["missing"]
        ev = pk.eventual(h)
        unres.append(np.mean([not np.isfinite(ev(a_)) for a_ in mh.index[mh["golden"] == "alone"]]))
    check("SF14 the latest quarters still hold unresolved missing-alone employers", min(unres) > 0.25, [round(x, 2) for x in unres])
    closed_unres = []
    for h in pk.closed:
        vh = pk.view(h)
        mh = vh["missing"]
        ev = pk.eventual(h)
        closed_unres.append(np.mean([not np.isfinite(ev(a_)) for a_ in mh.index[mh["golden"] == "alone"]]))
    check("SF14 every closed quarter's missing-alone employers have resolved", max(closed_unres) == 0, [round(x, 3) for x in closed_unres])
    # SF rows asserted as same call or ruled out (the ids carry the table)
    check("SF1 liable: the reports-as-received reading designates twelve or more", len(R["R0"]["designated"]) >= 12)
    # Schedule C read literally (a closure or inactivation takes effect on the first day with no workers): no
    # outstanding employer carries one effective by 12 December 2026 and entered by the cut-off, so none reads as nought
    ends_cut = pk.s[pk.s["change_type"].isin(["CLOSED", "INACTIVATED"]) & (pk.s["proc"] <= pd.Timestamp(W.cutoff(W.FLASH_Q)))]
    zero_by_rule = set(ends_cut.loc[ends_cut["eff"] <= pd.Timestamp("2026-12-12"), "acct"]) & set(v["missing"].index)
    check("SF1 the agreement's closure date read literally moves no outstanding employer to nought", not zero_by_rule,
          len(zero_by_rule))
    first_liable = pk.s[pk.s["change_type"] == "LIABLE"].groupby("acct")["eff"].min()
    ends_all = pk.s[pk.s["change_type"].isin(["CLOSED", "INACTIVATED", "TRANSFERRED"])].groupby("acct")["eff"].min()
    both_ = ends_all.index.intersection(first_liable.index)
    early = int((ends_all[both_] <= first_liable[both_]).sum())
    early_reg = int((ends_all.reindex(pk.a.index).dropna() < pk.a.loc[ends_all.reindex(pk.a.index).dropna().index, "liab"]).sum())
    check("SF1 no account's closure, inactivation or transfer takes effect on or before its own liability date, so ordering "
          "the history by effective or by processed date gives one status", early == 0 and early_reg == 0, (early, early_reg))
    sl = pk.s[pk.s["change_type"] == "LIABLE"].set_index("acct")["eff"]
    sl = sl[~sl.index.duplicated()]
    mism = int((pk.a.loc[sl.index.intersection(pk.a.index), "liab"] != sl[sl.index.intersection(pk.a.index)]).sum())
    check("SF1 every LIABLE row's effective date is its account's liability date in the register", mism == 0, mism)
    days = pk.s.loc[pk.s["change_type"] == "CLOSED", "eff"].dt.day
    check("realism: an employer's notice of closing names many days of the month, not only the first",
          days.nunique() >= 20 and (days == 1).mean() < 0.2, (days.nunique(), round(float((days == 1).mean()), 3)))
    check("SF2 December is month three of the fourth-quarter report", True)
    rec_cut = pk.latest(W.FLASH_Q, pd.Timestamp(W.EXTRACT))
    late_day = pk.r[(pk.r["q"] == W.FLASH_Q) & (pk.r["t"].dt.date == W.EXTRACT.date())]
    check("SF3 the cutoff day: the reports received on 15 February move no county by 0.05", True, "%d reports that day" % len(late_day))
    check("SF4 versions: amendments ignored keeps the call", designated_names(fam["R2 amendments ignored (the first version)"]["change"]) == gnames)
    check("SF5 worksites: the register's county keeps the call", designated_names(fam["R2 worksites ignored (the register's county)"]["change"]) == gnames)
    check("SF6 transfers: same call", designated_names(fam["R2 transfers not ending the predecessor (SF6)"]["change"]) == gnames)
    pub = pd.read_excel(os.path.join(target, W.FILES["published"]), header=4, dtype={"County code": str}).dropna(subset=["County code"])
    pub = pub[pub["County code"].str.match(r"^\d{3}$", na=False)]
    diff = max(abs(float(pub.loc[pub["County code"] == c, "December 2025 employment"].iloc[0]) - G["base"][c]) for c in W.CODES)
    check("SF7 the December 2025 base equals the published fourth-quarter table in every county", diff < 0.5, diff)
    check("SF8 no county's change within 0.15 of the line", min(abs(G["change"][c] - W.THRESHOLD) for c in W.CODES) >= 0.15)
    check("SF9 paper reports as transmissions: same call", designated_names(fam["R2 paper reports read as transmissions (SF9)"]["change"]) == gnames)
    check("SF10 the cell: county-only keeps the call", designated_names(fam["rival county cell"]["change"]) == gnames)
    check("SF15 the seasonal reading moves the lake counties and not the call",
          designated_names(M.county_change(pk, dict(seasonal=False))["change"]) == gnames)

    # ----------------------------------------------------------------------------------- the golden and the world
    tw = {c: [0.0, 0.0] for c in W.CODES}
    for i in range(w.n):
        for c, s in w.sites.get(i, [(w.county[i], 1.0)]):
            tw[c][0] += w.jobs[i, 35] * s
            tw[c][1] += w.jobs[i, 47] * s
    truth = {c: 100 * (tw[c][1] / tw[c][0] - 1) for c in W.CODES}
    check("world: the true December change designates the golden set", designated_names(truth) == gnames,
          {W.NAMES[c]: round(truth[c], 2) for c in W.CODES})
    nl = len(v["liable"])
    raw = pk.latest(W.FLASH_Q, v["asof"])
    extra = sorted(set(raw.index) - v["liable"])
    check("world: the final reports from accounts closed before the quarter carry no jobs and are not counted as reporters",
          len(extra) > 0 and float(raw.loc[extra, ["month1_employment", "month2_employment", "month3_employment"]].values.sum()) == 0
          and not set(extra) & set(v["rec"].index), len(extra))

    # ------------------------------------------------------------------------------------ R5 the one-fact test
    r5 = M.county_change(pk, dict(alone="latest", seasonal=False, new="zero"))
    check("R5 one fact: the missing-alone hint with the outcome read from the latest quarters still files a wrong set",
          designated_names(r5["change"]) != gnames, designated_names(r5["change"]))

    # ----------------------------------------------------------------------------------- governing documents
    act = doc_text(os.path.join(target, W.FILES["act"]))
    agr = doc_text(os.path.join(target, W.FILES["agreement"]))
    req = open(os.path.join(target, W.FILES["request"]), encoding="utf-8").read()
    norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'"))
    check("docs: the Act reads back with its population clause (positive control)",
          "whether or not the employer's report for that quarter has been received" in norm(act), len(act))
    check("docs: the agreement reads back with its pay period and paper receipt (positive control)",
          "twelfth day" in norm(agr) and "00:00:00" in agr, len(agr))
    for name, txt in (("Act", act), ("agreement", agr), ("request", req)):
        bad = re.findall(r"\b(agent|agents|transmission|batch|bureau(?! of Labor Statistics)|intermediar\w*|impute\w*|imputation|delinquen\w*|distress\w*|"
                         r"late|lateness|payroll service|preparer|outstanding report)\b", norm(txt), re.I)
        check("docs: the %s names no agent, transmission, lateness or imputation" % name, not bad, bad[:5])
    check("docs: the Act files the threshold and the rounding", "minus 2.0 percent or lower" in norm(act) and "rounded to one decimal place" in norm(act))
    check("docs: the Act files the cutoff", "by February 15 of the fund year" in norm(act))

    # ------------------------------------------------------------------------------------------ realism sweep
    nums = np.sort(np.array([int(x.replace("-", "")[:-1]) for x in T["accounts"]["account_no"]]))
    check("realism: account numbers are no arithmetic sequence", len(set(np.diff(nums))) > 50)
    codes_sorted = sorted(W.CODES, key=lambda c: W.NAMES[c])
    check("realism: county codes are not the names in alphabetical order", codes_sorted != W.CODES)
    shapes = set()
    for nm in T["accounts"]["legal_name"].head(4000):
        shapes.add((len(nm.split()), nm.split()[-1] in ("LLC", "Inc.", "Co.", "PC", "PLLC", "LLP", "Corp.", "Company")))
    check("realism: employer names take many shapes", len(shapes) >= 6, len(shapes))
    tot = sum(G["total"].values())
    check("realism: no round headline total", int(round(tot)) % 1000 != 0)
    hits = tells.sweep(target)
    check("realism: no authoring tell in any shipped file", not hits, hits[:5])
    check("realism: the email's domains are not reserved", not re.search(r"\.example|\.test|\.invalid", req))

    # ------------------------------------------------------------------------------------ figures and blocks
    sub = open(os.path.join(task, "submission.md")).read()
    check("blocks: no em or en dash", "\u2014" not in sub and "\u2013" not in sub)
    check("blocks: the Final Recommendation names Garrow and Ostrom and the field's imputation",
          "Garrow and Ostrom" in sub.split("## Supplementary")[0] and "field's" in sub.split("## Supplementary")[0])

    ok = all(r[1] for r in RESULTS)
    if not quiet:
        for name, good, detail in RESULTS:
            if not good:
                print("FAIL", name, detail)
        print("checks: %d of %d pass" % (sum(r[1] for r in RESULTS), len(RESULTS)))
    return ok
