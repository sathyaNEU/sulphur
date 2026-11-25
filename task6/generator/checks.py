"""The generator's assertions on the cut pack (architecture 8): the input gates, the results as designed (the golden
list, the lattice of the three judgments, the world's own spans as the check on the bridge), the bar block (R1 to R7:
the raw material ships, each mess item is neutral, each result's hurried figure falls outside its band, nothing is
planted, no one thing carries the results, every rival inside its band), the critical components' independence, every
semantic fork row (SF1 to SF16, SF19 to SF24, SF26, SF27), the rounding margins, the goldens against the figure set
and the documents' controls.

    python3 checks.py [target_dir]            (run by build.py)"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import deliver as D     # noqa: E402

FAILS = []
GOLD = ["fares", "places", "seat-map", "partner-gateway", "notifications"]
TRUTH = {x["fault"] for x in K.DEC_INCIDENTS}
JS = "journey-search"
# the list each combination of hurried judgments files (S1 own hourly counts, S2 whole-window causes, S3 the export's
# hours read as December), as the design note's lattice has it
LATTICE = {"S1": ["places", "seat-map"],
           "S2": ["partner-gateway", "places", JS, "seat-map"],
           "S3": GOLD + [JS],
           "S1+S2": ["places", JS, "seat-map"],
           "S1+S3": ["places", "fares", JS, "seat-map"],
           "S2+S3": ["partner-gateway", "places", JS, "seat-map"],
           "S1+S2+S3": ["places", JS, "seat-map"]}


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def r1set(S):
    return {s: K.r1(S[s]["sli"]) for s in K.SVC}


def over_of(S, bud):
    return [s for s in K.SVC if K.r1(S[s]["sli"]) > bud[s]]


def over_raw(S, bud):
    """The services over budget with the SLI compared unrounded."""
    return [s for s in K.SVC if S[s]["sli"] > bud[s]]


def order_of(S, bud):
    return sorted(over_of(S, bud), key=lambda s: -S[s]["over_requests"])


def text_of(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


# ---------------------------------------------------------------------------------------------- shared variants
def weight_variants(g, att, incs):
    """SF8 to SF10: the golden under each weighting base the whole traces leave standing. {label: SLIs}."""
    ex = g.excluded(att, incs)
    wr = g.weights("root")
    w_sh = g.weights("root_span_hour")
    w_drop = wr.copy()
    for i in np.nonzero(g.dec)[0]:
        if g.tr[i] not in g.root_of:
            w_drop[i] = 0.0
    hf = lambda w: g.hist_fill(w, ex, AN.FILL, incs)
    return {"SF8 Horvitz-Thompson on the balancer's count": g.slis(wr, ex, ht=True, fill=hf(wr)),
            "SF9 the root's share at the span's own hour": g.slis(w_sh, ex, fill=hf(w_sh)),
            "SF10 spans of traces begun before the export dropped": g.slis(w_drop, ex, fill=hf(w_drop))}


def scaled_fill(g, w, ex, incs, factor):
    """The hours before the export with every threshold bucket's split share moved by `factor` (held inside 0 to 1):
    the perturbation of the one fitted input the bridge has."""
    _, det = g.hist_fill(w, ex, AN.FILL, incs, detail=True)
    gone = np.arange(AN.H) < g.held_from()
    out = {}
    for s in K.SVC:
        tot = 0.0
        for (ss, name), d in det.items():
            if ss != s:
                continue
            above = d["slow"] - d["phi"] * d["mid"]
            slow = above + np.clip(d["phi"] * factor, 0.0, 1.0) * d["mid"]
            tot += float((d["wt"] * slow)[gone].sum())
        out[s] = (tot, float(g.N[s][gone].sum()))
    return out


def caller_weight_fill(g, w, ex, incs, how):
    """SF26: the hours before the export with each internal operation weighted another way: "dominant" its single
    largest caller's keep weight (by the client spans the span metrics count over the month), "mix" the callers' keep
    weights at the mix of roots its held spans show over the whole export."""
    HS, _ = g.hist()
    _, det = g.hist_fill(w, ex, AN.FILL, incs, detail=True)
    We = g.hist_edge_weights()
    gone = np.arange(AN.H) < g.held_from()
    tname = {c["Service"]: c["Tracing service name"] for c in g.cat}
    out = {}
    for s in K.SVC:
        tot = 0.0
        for (ss, name), d in sorted(det.items()):
            if ss != s:
                continue
            wt = d["wt"]
            if s not in K.EDGE:
                if how == "dominant":
                    meth, path = name.split(" ", 1)
                    cname = "%s %s %s" % (meth, tname[s], path)
                    calls = {cs: float(a[:, 0].sum()) for (cs, n, kd), a in HS.items() if kd == "CLIENT" and n == cname}
                    wt = We[max(calls, key=calls.get)]
                else:
                    m = g.dec & (g.svc == s) & (g.name == name)
                    cnt = {}
                    for i in np.nonzero(m)[0]:
                        ro = g.root_of.get(g.tr[i])
                        if ro is not None:
                            cnt[ro[0]] = cnt.get(ro[0], 0) + 1
                    n_ = float(sum(cnt.values()))
                    wt = sum(We[e] * (c / n_) for e, c in cnt.items())
            tot += float((wt * d["slow"])[gone].sum())
        out[s] = (tot, float(g.N[s][gone].sum()))
    return out


def world_exact(g, att, incs):
    """Every service's December SLI from the store's own spans of the whole month, which the pack never ships: the
    world's kept spans at their trace roots' keep shares, each duration against its threshold, the same incident
    time left out. What the bridge over the hours before the export has to reproduce."""
    import world as W
    w = W.World()
    sp = w.sp
    H = AN.H
    t0, ms = sp["t0"], sp["ms"]
    srv = sp["kind"] == "SERVER"
    h = np.floor(t0 / 3600).astype(int)
    inwin = srv & (h >= 0) & (h < H)
    tr = sp["trace"].astype(int)
    sidx = {s: i for i, s in enumerate(K.SVC)}
    svc_i = np.array([sidx[s] for s in sp["svc"]])
    root = srv & (sp["parent"] == -1)
    rsvc = np.full(tr.max() + 1, -1)
    rhour = np.full(tr.max() + 1, -999)
    rsvc[tr[root]] = svc_i[root]
    rhour[tr[root]] = h[root]
    Kr = np.zeros((len(K.SVC), H))
    np.add.at(Kr, (svc_i[root & inwin], h[root & inwin]), 1)
    own_k = np.zeros((len(K.SVC), H))
    np.add.at(own_k, (svc_i[inwin], h[inwin]), 1)
    Nm = np.array([g.N[s] for s in K.SVC])
    rs, rh = rsvc[tr], rhour[tr]
    ok = (rs >= 0) & (rh >= 0) & (rh < H)
    wgt = np.zeros(len(t0))
    a = inwin & ok
    wgt[a] = Nm[rs[a], rh[a]] / np.maximum(Kr[rs[a], rh[a]], 1)
    b = inwin & ~ok
    wgt[b] = Nm[svc_i[b], h[b]] / np.maximum(own_k[svc_i[b], h[b]], 1)
    ex = g.excluded(att, incs)
    out = {}
    for s in K.SVC:
        m = inwin & (svc_i == sidx[s])
        for a_, b_ in ex[s]:
            m &= ~((t0 >= a_) & (t0 < b_))
        out[s] = {"sli": 100 * float((wgt[m] * (ms[m] > g.thr[s])).sum()) / float(wgt[m].sum())}
    return out


def main(target):
    del FAILS[:]
    g = AN.Golden(target)
    R = g.run()
    F = D.figures(R)
    incs = R["incidents"]
    dec = [x for x in incs if x["declared"] >= AN.DEC0]
    S, P, L, bud = R["S"], R["P"], R["lattice"], R["bud"]
    gold1 = r1set(S)
    bridged = [s for s in K.SVC if R["bucket"][s] is not None]
    exact = [s for s in K.SVC if s not in bridged]
    band = {s: [float(v) for v in F["sli_band"][s]] for s in bridged}
    in_band = lambda s, v: band[s][0] - 1e-9 <= v <= band[s][1] + 1e-9
    moved1 = lambda SS: {s: K.r1(SS[s]["sli"]) for s in K.SVC if K.r1(SS[s]["sli"]) != gold1[s]}

    # ---------------------------------------------------------------- input gates
    files = sorted(f for f in os.listdir(target) if not f.startswith("."))
    check("IG1 ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "parquet": "database", "json": "database", "docx": "text",
            "md": "text"}
    kinds = {cats.get(f.rsplit(".", 1)[-1]) for f in files}
    check("IG2 two or more file categories", len(kinds - {None}) >= 2, ", ".join(sorted(k for k in kinds if k)))
    n_lb = sum(1 for _ in open(os.path.join(target, K.FILES["lb_h2"]))) - 1
    n_sm = sum(1 for _ in open(os.path.join(target, K.FILES["spanmetrics"]))) - 1
    n_bill = sum(1 for _ in open(os.path.join(target, K.FILES["billing"]))) - 1
    check("IG3 a CSV of 20,000 rows or more", n_lb >= 20000, "%s %d rows" % (K.FILES["lb_h2"], n_lb))
    check("IG3 the span metrics are a second CSV of 20,000 rows or more", n_sm >= 20000,
          "%s %d rows" % (K.FILES["spanmetrics"], n_sm))
    check("IG4 a CSV of ten printed pages or more", n_bill >= 600, "%s %d rows" % (K.FILES["billing"], n_bill))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    dis = [p_.split("/", 1)[1] for p_ in meta.get("distractor_files", [])]
    check("IG5 two or more distractors named in metadata.json", len(dis) >= 2, ", ".join(dis))
    src = open(os.path.join(HERE, "analysis.py")).read()
    read_keys = set(re.findall(r'K\.FILES\["(\w+)"\]', src))
    check("IG6 the golden reads no distractor", not ({K.FILES_KEY_OF[d] for d in dis} & read_keys),
          "reads %s" % ", ".join(sorted(read_keys)))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|distractor", f, re.I)]
    check("IG7 no file describes the pack", not bad, ", ".join(bad) or "none")

    # ---------------------------------------------------------------- the results, as designed
    check("RES1 the golden list", P["over"] == GOLD, ", ".join(P["over"]))
    att = R["attribution"]
    want = {}
    for x, spec in zip(sorted(dec, key=lambda z: z["declared"]), sorted(K.DEC_INCIDENTS, key=lambda z: z["declared"])):
        want[x["id"]] = spec["fault"]
    check("RES2 every December customer-facing incident put on the world's own fault", att == want,
          "; ".join("%s %s" % (k, v) for k, v in att.items()))
    check("RES3 seven customer-facing incidents in December, reviews open", len(dec) == 7 and all(
        x["review"] == "open" and not x["cause"] for x in dec), "%d" % len(dec))
    # each fault's rise leads every other named service's by 20 minutes or more
    lead = []
    for x in dec:
        on = R["onset"][x["id"]]
        f = att[x["id"]]
        others = [v[0] for s_, v in on.items() if s_ != f and v]
        if others:
            lead.append(min(others) - on[f][0])
    check("RES4 each cause leads the other named services' rises by twenty minutes or more",
          all(v >= 1200 for v in lead), "leads %s minutes" % ", ".join("%.0f" % (v / 60) for v in lead))
    # the world's own spans of the whole month (never shipped): the list and every SLI the bridge has to reproduce
    WX = world_exact(g, att, dec)
    gapx = {s: round(S[s]["sli"] - WX[s]["sli"], 3) for s in K.SVC}
    check("RES5 the store's own December spans, each at its threshold, give the golden list", over_of(WX, bud) == GOLD
          and over_raw(WX, bud) == GOLD, ", ".join(over_of(WX, bud)))
    # a boundary-threshold SLI is the same spans counted two ways; a bridged one differs from the store's own spans
    # by which of the bucket's kept spans happened to pass the threshold, the sampling error the interval carries
    check("RES5 every boundary-threshold SLI equals the store's own December spans, and every bridged one has them "
          "inside its 90 per cent interval", all(abs(gapx[s]) <= 0.005 for s in exact) and all(
              R["ci"][s][0] <= WX[s]["sli"] <= R["ci"][s][1] for s in bridged),
          "golden less the store's own spans %s; bridged, own spans against the interval %s" % (
              gapx, {s: (round(WX[s]["sli"], 3), round(R["ci"][s][0], 2), round(R["ci"][s][1], 2)) for s in bridged}))
    outside = {s: (round(WX[s]["sli"], 3), band[s]) for s in bridged if not in_band(s, WX[s]["sli"])}
    print("NOTE  RES5 bridged SLIs whose store's-own-spans value sits outside the split family's stated range "
          "(sampling of the bucket's spans, not a split the pack supports): %s" % (outside or "none"))

    # ---------------------------------------------------------------- the lattice of the three judgments
    lat_ok = {k: set(L[k]["P"]["over"]) == set(v) for k, v in LATTICE.items()}
    check("LAT1 each combination of hurried judgments files the list the design names", all(lat_ok.values()),
          "; ".join("%s: %s" % (k, ", ".join(L[k]["P"]["over"])) for k in LATTICE))
    check("LAT2 each judgment is necessary: made the hurried way alone, the list moves",
          all(set(L[k]["P"]["over"]) != set(GOLD) for k in ("S1", "S2", "S3")),
          "; ".join("%s %d services" % (k, len(L[k]["P"]["over"])) for k in ("S1", "S2", "S3")))
    check("LAT3 none is sufficient: fixed alone on the careful pass, the list is still wrong",
          all(set(L[k]["P"]["over"]) != set(GOLD) for k in ("S2+S3", "S1+S3", "S1+S2")),
          "S1 alone fixed: %s; S2: %s; S3: %s" % tuple(", ".join(L[k]["P"]["over"]) for k in ("S2+S3", "S1+S3", "S1+S2")))
    distinct = {tuple(sorted(L[k]["P"]["over"])) for k in LATTICE}
    check("LAT4 the shortcuts file different wrong lists", len(distinct) >= 5 and len(
        {tuple(sorted(L[k]["P"]["over"])) for k in ("S1", "S2", "S3")}) == 3, "%d distinct lists over 7 routes" % len(distinct))

    # ---------------------------------------------------------------- R1 raw material
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(target, f))))
    check("R1 no shipped column carries an SLI or a keep share", not [h for h in heads if re.search(
        r"sli|keep|sample|weight", h, re.I)], "%d columns read" % len(heads))
    check("R1 the SLIs read the span export, the span metrics and the balancer's counts",
          all(S[s]["kept"] > 1000 for s in K.SVC),
          "kept spans per service %d to %d" % (min(S[s]["kept"] for s in K.SVC), max(S[s]["kept"] for s in K.SVC)))

    # ---------------------------------------------------------------- R2 mess neutral
    g2 = AN.Golden(target, dedupe=False)
    R2 = g2.route(())
    same = r1set(R2["S"]) == gold1 and R2["attribution"] == att and R2["P"]["over"] == GOLD
    check("R2 SF3 re-sent span rows counted twice moves no graded result", same,
          "moved %s" % moved1(R2["S"]) if moved1(R2["S"]) else "every SLI, cause and the list")
    wr = g.weights("root")
    ex = g.excluded(att, dec)
    hfill = lambda w, e, form=AN.FILL: g.hist_fill(w, e, form, dec)
    ex_d = g.excluded(att, dec, from_declaration=True)
    S_d = g.slis(wr, ex_d, fill=hfill(wr, ex_d))
    check("R2 SF11 windows read from the declaration move no SLI (the timeline convention is texture for the SLIs)",
          r1set(S_d) == gold1, str(moved1(S_d)))
    m_back = g.minutes(backdate=True)
    check("R2 reading every service from the declaration moves the incident minutes (graded in R1 only)",
          m_back != R["minutes"], "")

    # ---------------------------------------------------------------- R3 each result's hurried figure
    Sc, Pc = L["S1+S2+S3"]["S"], L["S1+S2+S3"]["P"]
    check("R3 the careful pass (own hourly counts, whole-window causes, the export's hours) misses the list",
          set(Pc["over"]) != set(GOLD) and JS in Pc["over"] and not {"partner-gateway", "fares", "notifications"} & set(
              Pc["over"]), ", ".join(Pc["over"]))
    S3 = L["S3"]["S"]
    check("R3 the export's hours read as December put journey-search over as well",
          set(over_of(S3, bud)) == set(GOLD) | {JS} and S3[JS]["sli"] > bud[JS] + 0.05,
          "%s; journey-search %.3f against %.3f across December" % (", ".join(over_of(S3, bud)), S3[JS]["sli"],
                                                                   S[JS]["sli"]))
    S1 = L["S1"]["S"]
    check("R3 each service's own hourly count leaves fares, partner-gateway and notifications within budget",
          all(K.r1(S1[s]["sli"]) <= bud[s] and S1[s]["sli"] <= bud[s] + 0.05 for s in ("fares", "partner-gateway",
                                                                                        "notifications")),
          "fares %.3f, partner-gateway %.3f, notifications %.3f" % tuple(S1[s]["sli"] for s in (
              "fares", "partner-gateway", "notifications")))
    rc = L["S2"]
    check("R3 the whole-window attribution leaves fares and notifications out and brings journey-search in",
          not {"fares", "notifications"} & set(rc["P"]["over"]) and JS in rc["P"]["over"] and rc["attribution"] != att,
          "fares %.3f, notifications %.3f, journey-search %.3f" % (rc["S"]["fares"]["sli"],
                                                                    rc["S"]["notifications"]["sli"], rc["S"][JS]["sli"]))
    # the misleading form (a blocked caller ending further over its curve than the fault) is not placed only where it
    # decides: each incident the whole-window reading misreads, misread alone on the root weights
    moves = {}
    for iid, s_ in rc["attribution"].items():
        if s_ != att[iid]:
            a_ = dict(att, **{iid: s_})
            e_ = g.excluded(a_, dec)
            moves[iid] = g.programme(g.slis(wr, e_, fill=hfill(wr, e_)))["over"]
    deciding = {k: sorted(set(GOLD) ^ set(v)) for k, v in moves.items() if set(v) != set(GOLD)}
    check("R5 the whole-window reading misreads an incident where nothing turns on it, and two that decide different "
          "services", len(moves) - len(deciding) >= 1 and len(deciding) >= 2 and len({tuple(v) for v in
                                                                                    deciding.values()}) >= 2,
          "; ".join("%s: %s" % (k, ", ".join(sorted(set(GOLD) ^ set(moves[k]))) or "no verdict moves") for k in moves))
    first = {x["id"]: x["named"][0][0] for x in dec}
    last = {x["id"]: x["named"][-1][0] for x in dec}
    for lab, a_ in (("first-named", first), ("last-named", last)):
        e_ = g.excluded(a_, dec)
        S_x = g.slis(wr, e_, fill=hfill(wr, e_))
        check("R3 root weights with the %s service at fault miss the list" % lab, set(over_of(S_x, bud)) != set(GOLD),
              ", ".join(over_of(S_x, bud)))
    e_ = g.excluded({x["id"]: "__none__" for x in dec}, dec)
    S_none = g.slis(wr, e_, fill=hfill(wr, e_))
    check("R3 the route that ignores PR-SLO-3 3.2 loses the symptoms' SLI cells",
          sum(K.r1(S_none[s]["sli"]) != gold1[s] for s in K.SVC) >= 3,
          "cells moved: %s" % ", ".join(s for s in K.SVC if K.r1(S_none[s]["sli"]) != gold1[s]))
    gaps = {s: round(max(abs(R["ci"][s][0] - g.binomial_interval(s, ex, S[s]["sli"])[0]),
                         abs(R["ci"][s][1] - g.binomial_interval(s, ex, S[s]["sli"])[1])), 3) for s in GOLD}
    gaps = {s: float(v) for s, v in gaps.items()}
    # a binomial interval is the right width where every kept span is its own trace at one weight an hour (the edge
    # services); it is too narrow where one service's spans carry several callers' weights (the internal services)
    check("R3 a binomial interval misses each over-budget internal service's interval by 0.03 or more at one end",
          all(v >= 0.03 for s_, v in gaps.items() if s_ in K.INTERNAL), str(gaps))
    lin = R["naive"]["linear"]
    check("R3 straight-line interpolation inside the bucket puts every bridged SLI outside its range",
          all(not in_band(s, lin[s]["sli"]) for s in bridged),
          ", ".join("%s %.3f (%.2f to %.2f)" % (s, lin[s]["sli"], band[s][0], band[s][1]) for s in bridged))
    check("R3 the export's hours read as December put every bridged SLI but accounts' outside its range",
          all(not in_band(s, S3[s]["sli"]) for s in bridged if s != "accounts"),
          ", ".join("%s %.3f" % (s, S3[s]["sli"]) for s in bridged))

    # ---------------------------------------------------------------- R4 no plant
    check("R4 no December fault sits only in the services whose verdict turns on it",
          len(TRUTH) >= 5 and len({s for x in K.DEC_INCIDENTS for s, _ in x["named"]}) >= 8,
          "faults in %s; %d services named" % (", ".join(sorted(TRUTH)),
                                               len({s for x in K.DEC_INCIDENTS for s, _ in x["named"]})))
    closed = [x for x in g.incidents() if x["review"] == "closed" and len(x["named"]) > 1]
    first_right = sum(1 for x in closed if x["cause"] == K.TRACE_NAME[x["named"][0][0]] or
                      g.by_trace.get(x["cause"]) == x["named"][0][0])
    check("R4 the closed reviews show the first service named is not reliably the cause",
          0.2 <= first_right / max(len(closed), 1) <= 0.6, "%d of %d" % (first_right, len(closed)))
    cut = g.held_from()
    check("R4 SF22 the export begins where the store's 31 days began, on a whole hour",
          cut == K.STORE_FROM_H and abs(g.t0[g.dec].min() - cut * 3600) < 60, "hour %d" % cut)
    check("R4 no customer-facing December incident falls in the hours before the export",
          all(AN.sec_of(x["declared"]) >= cut * 3600 for x in dec), "")
    quiet = g.quiet_hours(dec)
    hrs = np.arange(AN.H)
    inside = {}
    for s in K.SVC:
        held_n = g.N[s][(hrs >= cut) & quiet]
        gone_n = g.N[s][hrs < cut]
        inside[s] = round(float(gone_n.max() / held_n.max()), 2)
    check("R4 every early hour's load lies inside the held, incident-free hours' range", all(v <= 1.0 for v in
                                                                                           inside.values()),
          str(inside))
    check("R4 the span metrics' boundaries fall on some thresholds and inside a bucket for others (no service set "
          "apart)", len(exact) >= 3 and len(bridged) >= 3, "boundary: %s; inside a bucket: %s" % (
              ", ".join(exact), ", ".join("%s %s" % (s, F["bucket_ms"][s]) for s in bridged)))
    HS, HB = g.hist()
    cover = {s: int((sum(a[:, 0] for (ss, n_, kd), a in HS.items() if ss == s and kd == "SERVER") > 0).sum())
             for s in K.SVC}
    check("R4 the span metrics hold every service in every December hour", all(v == AN.H for v in cover.values()),
          str(cover))

    # ---------------------------------------------------------------- R5 no one thing: footprints
    shifts = {s: round(S[s]["sli"] - S1[s]["sli"], 3) for s in K.INTERNAL}
    check("R5 the root weights move every internal service's SLI by 0.1 or more, in both directions",
          all(abs(v) >= 0.1 for v in shifts.values()) and min(shifts.values()) < 0 < max(shifts.values()),
          str(shifts))
    held_shift = {s: round(S3[s]["sli"] - S[s]["sli"], 3) for s in K.SVC}
    check("R5 the hours before the export move six or more services' one-decimal SLIs, the deciding one among them",
          sum(K.r1(S3[s]["sli"]) != gold1[s] for s in K.SVC) >= 6 and K.r1(S3[JS]["sli"]) != gold1[JS], str(held_shift))
    lin_shift = {s: round(lin[s]["sli"] - S[s]["sli"], 3) for s in bridged}
    check("R5 the bucket's split moves every bridged service, none of them across its budget",
          all(abs(v) >= 0.1 for v in lin_shift.values()) and over_of(lin, bud) == GOLD, str(lin_shift))
    eff_path = os.path.join(HERE, "effort.json")
    if os.path.exists(eff_path):
        eff = json.load(open(eff_path))
        worst = max(len(h["rescues"]) for h in eff["hints"])
        check("R5 no single correction rescues more than a third of the results", worst <= len(eff["results"]) / 3.0,
              "; ".join("%s: %s" % (h["sentence"][:48], ",".join(h["rescues"]) or "none") for h in eff["hints"]))

    # ---------------------------------------------------------------- the critical components' independence
    pay, pg, pl, bk = "payments", "partner-gateway", "places", "booking"
    first_of = lambda k: (L[k]["P"]["order"] or ["none"])[0]
    check("CC1 the first to start and payments' SLI fall with the weights alone",
          first_of("S1") != P["order"][0] and K.r1(L["S1"]["S"][pay]["sli"]) != gold1[pay] and all(
              first_of(k) == P["order"][0] and K.r1(L[k]["S"][pay]["sli"]) == gold1[pay] for k in ("S2", "S3")),
          "first: golden %s, S1 %s, S2 %s, S3 %s; payments: golden %.3f, S1 %.3f, S2 %.3f, S3 %.3f" % (
              P["order"][0], first_of("S1"), first_of("S2"), first_of("S3"), S[pay]["sli"], L["S1"]["S"][pay]["sli"],
              L["S2"]["S"][pay]["sli"], L["S3"]["S"][pay]["sli"]))
    mis = F["misread"]
    check("CC2 the misread incidents' owners fall with the dated causes alone",
          len(mis) == 3 and all(L["S2"]["attribution"][i] != att[i] for i in mis) and L["S1"]["attribution"] == att
          and L["S3"]["attribution"] == att, "; ".join("%s %s (whole window: %s)" % (
              i, att[i], L["S2"]["attribution"][i]) for i in mis))
    c3 = lambda k: (in_band(pl, L[k]["S"][pl]["sli"]) and K.r1(L[k]["S"][pl]["sli"]) == gold1[pl]
                    and K.r1(L[k]["S"][bk]["sli"]) == gold1[bk])
    check("CC3 places' and booking's SLI fall with the hours before the export alone",
          not in_band(pl, S3[pl]["sli"]) and K.r1(S3[bk]["sli"]) != gold1[bk] and c3("S1") and c3("S2"),
          "places: golden %.3f, S3 %.3f, S1 %.3f, S2 %.3f; booking: golden %.3f, S3 %.3f, S1 %.3f, S2 %.3f" % (
              S[pl]["sli"], S3[pl]["sli"], L["S1"]["S"][pl]["sli"], L["S2"]["S"][pl]["sli"], S[bk]["sli"],
              S3[bk]["sli"], L["S1"]["S"][bk]["sli"], L["S2"]["S"][bk]["sli"]))

    # ---------------------------------------------------------------- R7 rivals inside each band
    WV = weight_variants(g, att, dec)
    for lab, S_r in WV.items():
        check("R7 %s gives the list and every one-decimal SLI" % lab, r1set(S_r) == gold1 and over_of(S_r, bud) == GOLD
              and over_raw(S_r, bud) == GOLD, str({s: round(S_r[s]["sli"], 3) for s in moved1(S_r)}))
    # SF21: every split of the threshold's bucket the held spans support
    fam = R["family"]
    fam_bad = []
    for lab, S_r in fam.items():
        if over_of(S_r, bud) != GOLD or over_raw(S_r, bud) != GOLD:
            fam_bad.append("%s list %s" % (lab, ", ".join(over_raw(S_r, bud))))
        if order_of(S_r, bud) != P["order"]:
            fam_bad.append("%s order %s" % (lab, ", ".join(order_of(S_r, bud))))
        for s in bridged:
            if not in_band(s, S_r[s]["sli"]):
                fam_bad.append("%s %s %.3f" % (lab, s, S_r[s]["sli"]))
        for s in exact:
            if abs(S_r[s]["sli"] - S[s]["sli"]) > 1e-9:
                fam_bad.append("%s %s %.4f" % (lab, s, S_r[s]["sli"]))
    spread = {s: (round(min(f[s]["sli"] for f in fam.values()), 3), round(max(f[s]["sli"] for f in fam.values()), 3))
              for s in bridged}
    check("SF21 every split of the threshold's bucket (%d of them) gives the list, the start order, every bridged SLI "
          "inside its range and every boundary SLI unmoved" % len(fam), not fam_bad,
          "; ".join(fam_bad) if fam_bad else "spread %s" % spread)
    fam1 = {s: sorted({K.r1(f[s]["sli"]) for f in fam.values()}) for s in bridged}
    print("NOTE  SF21 one-decimal values across the split family: %s" % fam1)
    nv = R["naive"]
    nv_bad = [k for k in AN.NAIVE_BRIDGES if over_of(nv[k], bud) != GOLD]
    nv_raw = [k for k in ("linear", "loglinear") if over_raw(nv[k], bud) != GOLD]
    crossing = {k: [(s, round(nv[k][s]["sli"], 3)) for s in sorted(set(over_raw(nv[k], bud)) ^ set(GOLD))]
                for k in ("lower", "upper") if over_raw(nv[k], bud) != GOLD}
    lo_raw = over_raw(nv["lower"], bud) == GOLD
    check("SF21 interpolation inside the bucket and the bucket's lower bound give the same list, the SLI rounded or "
          "not", not nv_raw and lo_raw and not [k for k in ("linear", "loglinear", "lower") if k in nv_bad],
          "rounded differ: %s; unrounded differ: %s" % (nv_bad or "none", nv_raw or "none"))
    # the upper bound is the one treatment that reaches journey-search's line: the blocks say so with its figure
    up = nv["upper"]
    up_cross = sorted(set(over_raw(up, bud)) ^ set(GOLD))
    check("SF21 the bucket's upper bound crosses a budget for journey-search alone, at the figure the blocks state",
          up_cross == ["journey-search"] and D.two(up["journey-search"]["sli"]) == F["upper_sli2"]["journey-search"],
          "%s at %.3f" % (up_cross, up["journey-search"]["sli"]))
    print("NOTE  SF21 bounds that cross a budget unrounded: %s" % (crossing or "none"))
    br = R["bridge_ratios"]
    check("SF21 the blocks' floors on what interpolation and the upper bound rebuild hold on every basis",
          all(min(br["linear"][s].values()) >= float(F["linear_floor"][s]) for s in bridged) and
          all(min(br["upper"][s].values()) >= float(F["upper_floor"][s]) for s in bridged) and
          float(F["linear_floor"]["places"]) >= 2.5 and float(F["linear_floor"]["journey-search"]) >= 1.5 and
          float(F["upper_floor"]["journey-search"]) >= 2.0,
          "linear %s; upper journey-search %s" % (
              {s: {k: round(v, 2) for k, v in br["linear"][s].items()} for s in ("places", "journey-search")},
              {k: round(v, 2) for k, v in br["upper"]["journey-search"].items()}))
    check("SF21 interpolation inside the bucket changes the start order (the blocks name its first service)",
          R["naive_order"]["linear"][0] == F["linear_first"] and F["linear_first"] != P["order"][0] and
          R["naive_order"]["lower"] == list(P["order"]),
          "linear %s; lower %s" % (R["naive_order"]["linear"], R["naive_order"]["lower"]))
    rv = R["rivals"]["lognormal"]
    rv_bad = [s for s in bridged if not (float(F["sli_band"][s][0]) <= rv[s]["sli"] <= float(F["sli_band"][s][1]))]
    check("SF21 a lognormal curve fitted to each early hour's histogram gives the list, the start order and every "
          "bridged SLI inside its range", over_raw(rv, bud) == GOLD and list(g.programme(rv)["order"]) == list(P["order"])
          and not rv_bad, str({s: round(rv[s]["sli"], 3) for s in bridged}))
    bc = R["bridge_check"]
    lin_ratio = {s: round(bc["linear"][s][0] / bc["linear"][s][1], 3) for s in bridged}
    gold_ratio = {s: round(bc[AN.FILL][s][0] / bc[AN.FILL][s][1], 4) for s in K.SVC}
    check("SF21 on the export's own hours straight-line interpolation rebuilds 1.5 times the over-threshold requests "
          "or more for every bridged service", all(v >= 1.5 for v in lin_ratio.values()), str(lin_ratio))
    check("SF21 on the export's own hours the review's split rebuilds every service's over-threshold requests within "
          "2 per cent", all(abs(v - 1) <= 0.02 for v in gold_ratio.values()), str(gold_ratio))
    for lab, lead_h in (("two", 2), ("four", 4)):
        q2 = np.ones(AN.H, dtype=bool)
        for x in dec:
            a_ = int(AN.sec_of(x["declared"]) // 3600) - lead_h
            b_ = int(AN.sec_of(x["end"]) // 3600) + 1
            q2[max(0, a_):min(AN.H, b_ + 1)] = False
        g.quiet_hours = lambda incs=None, _q=q2: _q
        S_r = g.slis(wr, ex, fill=hfill(wr, ex))
        del g.quiet_hours
        check("R7 the split fitted on hours clear of incidents from %s hours before gives the list and every bridged "
              "SLI inside its range" % lab, over_raw(S_r, bud) == GOLD and all(in_band(s, S_r[s]["sli"]) for s in
                                                                               bridged),
              str({s: round(S_r[s]["sli"], 3) for s in bridged}))
    for f_ in (1.2, 0.8):
        S_r = g.slis(wr, ex, fill=scaled_fill(g, wr, ex, dec, f_))
        check("R7 every split share moved to %.1f times itself keeps the list" % f_, over_raw(S_r, bud) == GOLD,
              str({s: round(S_r[s]["sli"], 3) for s in bridged}))

    # SF24: fills that read no span metrics
    lf = R["loadfill"]
    check("SF24 a flat December share misses partner-gateway's measured SLI by 0.4 or more (its threshold is a "
          "boundary: nothing in it is estimated)", abs(lf["flat"]["partner-gateway"]["sli"] - S[pg]["sli"]) >= 0.4,
          "flat %.3f against %.3f measured" % (lf["flat"]["partner-gateway"]["sli"], S[pg]["sli"]))
    six = [k for k in ("flat", "hour", "daytype-hour", "bands2", "bands3") if set(over_raw(lf[k], bud)) != set(GOLD) | {JS}
           or set(over_of(lf[k], bud)) != set(GOLD) | {JS}]
    check("SF24 the flat, hour-of-day, day-type and two- and three-band load fills file journey-search over (the six)",
          not six, "journey-search %s%s" % (
              ", ".join("%s %.3f" % (k, lf[k][JS]["sli"]) for k in ("flat", "hour", "daytype-hour", "bands2", "bands3")),
              "" if not six else "; not the six: %s" % six))
    print("NOTE  SF24 the same-weekday-and-hour load fill puts journey-search at %.3f (reported only)"
          % lf["weekday-hour"][JS]["sli"])
    fine = ["bands8", "bands10", "bands15", "bands20", "bands30", "isotonic", "logit2"]
    lgap = {k: {s: round(max(band[s][0] - lf[k][s]["sli"], lf[k][s]["sli"] - band[s][1], 0.0), 3) for s in bridged}
            for k in fine}
    check("SF24 load fills with eight or more bands, an isotonic share and a curved logit land within 0.06 of every "
          "bridged range and file the golden list", all(v <= 0.06 for d_ in lgap.values() for v in d_.values()) and all(
              over_raw(lf[k], bud) == GOLD for k in fine),
          "largest gap outside a range %s" % {k: max(d_.values()) for k, d_ in lgap.items()})
    lex = {k: {s: round(lf[k][s]["sli"] - S[s]["sli"], 3) for s in exact} for k in ("flat", "bands10")}
    print("NOTE  SF24 load fills against the measured boundary services: %s" % lex)

    # SF26: an internal operation's weight in the hours before the export
    for lab, how in (("its single dominant caller's keep share", "dominant"),
                     ("its callers' keep shares at the export's overall mix", "mix")):
        S_r = g.slis(wr, ex, fill=caller_weight_fill(g, wr, ex, dec, how))
        mv = {s: (gold1[s], round(S_r[s]["sli"], 3)) for s in K.SVC if K.r1(S_r[s]["sli"]) != gold1[s]}
        check("SF26 an internal operation weighted in the early hours by %s gives the list and every one-decimal SLI"
              % lab, over_raw(S_r, bud) == GOLD and not mv, str(mv) if mv else "internal SLIs %s" % {
                  s: round(S_r[s]["sli"], 3) for s in K.INTERNAL})

    # SF27: the span metrics against the export where they overlap
    import pandas as pd
    held_spans = (g.h >= cut) & (g.h < AN.H) & np.isin(g.kind, ["SPAN_KIND_SERVER", "SPAN_KIND_CLIENT"])
    df = pd.DataFrame({"svc": g.svc[held_spans], "name": g.name[held_spans],
                       "kind": [k_.replace("SPAN_KIND_", "") for k_ in g.kind[held_spans]], "ms": g.ms[held_spans]})
    for b_ in HB:
        df["gt_%d" % b_] = df["ms"] > b_
    grp = df.groupby(["svc", "name", "kind"])
    cnt = grp.size().to_dict()
    above = grp[["gt_%d" % b_ for b_ in HB]].sum()
    diff_c, diff_b = [], []
    for key in set(cnt) | set(HS):
        a = HS.get(key)
        m_c = float(a[cut:, 0].sum()) if a is not None else 0.0
        if m_c != cnt.get(key, 0):
            diff_c.append("%s %s %s: metrics %d, export %d" % (key + (m_c, cnt.get(key, 0))))
        if a is not None and key in cnt:
            m_ab = a[cut:, 0].sum() - a[cut:, 1:].sum(axis=0)
            if not np.array_equal(m_ab, above.loc[key].values.astype(float)):
                diff_b.append("%s %s %s" % key)
    check("SF27 SF3 in the export's hours the span metrics count the de-duplicated export's spans, series by series",
          not diff_c, "; ".join(diff_c[:4]) or "%d series, %d spans" % (len(cnt), sum(cnt.values())))
    check("SF27 and the same spans above every boundary", not diff_b, "; ".join(diff_b[:4]) or "%d boundaries" % len(HB))

    # the onsets: every rival detector, calibrated on placebo windows (each incident's window moved by whole days onto
    # the export's incident-free stretches), names the same seven owners
    curves = g.load_curves(dec)

    def series(x, s_):
        a0, b0 = AN.sec_of(x["declared"]) - 3 * 3600, AN.sec_of(x["end"])
        out = []
        for (ss, n_), cf in curves.items():
            if ss != s_:
                continue
            m_ = g.dec & (g.svc == s_) & (g.name == n_) & (g.t0 >= a0) & (g.t0 < b0)
            if m_.sum() < 20:
                continue
            o_ = np.argsort(g.t0[m_])
            out.append((g.t0[m_][o_], (np.log(g.own[m_]) - np.polyval(cf, np.log(g.N[s_][g.h[m_]] + 1)))[o_]))
        return out

    def shifted(x, days):
        y = dict(x)
        y["declared"] = x["declared"] + dt.timedelta(days=days)
        y["end"] = x["end"] + dt.timedelta(days=days)
        a0, b0 = int(AN.sec_of(y["declared"]) // 3600) - 3, int(AN.sec_of(y["end"]) // 3600) + 1
        return y if (a0 >= cut and b0 < AN.H and quiet[a0:b0 + 1].all()) else None

    placebos = [y for x in dec for d_ in range(-6, 7) if d_ for y in [shifted(x, d_)] if y]

    def cp(thr):
        def f(t, r):
            k_ = AN.sustained_split(t, r)
            ok = k_ and k_[2] - k_[1] >= np.log(thr) and k_[2] >= np.log(thr * AN.LEVEL / AN.RISE)
            return t[k_[0]] if ok else None
        return f

    def cp10(thr):
        def f(t, r):
            b_ = np.floor((t - t[0]) / 600).astype(int)
            u_ = np.unique(b_)
            med = np.array([np.median(r[b_ == k]) for k in u_])
            tt = np.array([t[b_ == k][0] for k in u_])
            k_ = AN.sustained_split(tt, med, min_n=3)
            ok = k_ and k_[2] - k_[1] >= np.log(thr) and k_[2] >= np.log(thr * AN.LEVEL / AN.RISE)
            return tt[k_[0]] if ok else None
        return f

    def roll(thr, minutes):
        def f(t, r):
            win = max(6, int(round(len(r) / ((t[-1] - t[0]) / 3600 + 1e-9) * minutes / 60)))
            if len(r) < 2 * win:
                return None
            med = np.array([np.median(r[j - win + 1:j + 1]) for j in range(win - 1, len(r))])
            for j in range(len(med) - win):
                if med[j] > np.log(thr) and med[j:j + win].min() > np.log(thr) * 0.65:
                    return t[j]
            return None
        return f

    def owners_of(fn, xs):
        out = {}
        for x in xs:
            firsts = {}
            for s_, _ in x["named"]:
                ts = [v for v in (fn(t, r) for t, r in series(x, s_)) if v is not None]
                if ts:
                    firsts[s_] = min(ts)
            out[x["id"]] = min(firsts, key=firsts.get) if firsts else None
        return out

    def rate(fn):
        return float(np.mean([any(v is not None for v in owners_of(fn, [y]).values()) for y in placebos]))

    dets = {"the golden's sustained changepoint": cp, "a changepoint on ten-minute medians": cp10,
            "a half-hour rolling median": lambda thr: roll(thr, 30), "an hour's rolling median": lambda thr: roll(thr, 60)}
    calib = {}
    for lab, mk in dets.items():
        for thr in (1.4, 1.6, 1.8, 2.0, 2.2):
            if rate(mk(thr)) <= 1 / 14.0:
                calib[lab] = (thr, mk(thr))
                break
    gold_rate = rate(cp(AN.RISE))
    check("R7 the golden's onset rule fires on one placebo window in fourteen or fewer",
          gold_rate <= 1 / 14.0 + 1e-9, "%d of %d placebo windows fire, %.1f%% against 7.1%%" % (
              round(gold_rate * len(placebos)), len(placebos), 100 * gold_rate))
    disagree = {}
    for lab, (thr, fn) in calib.items():
        o_ = owners_of(fn, dec)                       # a detector that sees no rise at all abstains
        wrong = {k: v for k, v in o_.items() if v is not None and v != att[k]}
        if wrong:
            disagree[lab] = wrong
    check("R7 SF23 every rival onset detector, calibrated on the placebo windows, names the same seven owners",
          len(calib) == len(dets) and not disagree, "; ".join("%s at x%.1f" % (k, v[0]) for k, v in calib.items()) +
          ("" if not disagree else " | disagree: %s" % disagree))
    for lab, kw in (("a two-hour lead", {"lead_min": 120}), ("a four-hour lead", {"lead_min": 240})):
        alt = {x["id"]: (lambda on: min((s_ for s_, v in on.items() if v), key=lambda s_: on[s_][0]))(
            g.onsets(x, curves, **kw)) for x in dec}
        check("R7 SF14 the onset read over %s puts every incident on the same service" % lab, alt == att, str(alt))
    linci = {s: (R["ci"][s][0], R["ci"][s][1]) for s in GOLD}
    boot = R["ci_boot"]
    check("R7 SF16 the trace bootstrap with the splits refitted agrees with the linearised interval to 0.03 at both "
          "ends", all(abs(linci[s][0] - boot[s][0]) <= 0.03 and abs(linci[s][1] - boot[s][1]) <= 0.03 for s in GOLD),
          str({s: (round(linci[s][0], 2), round(boot[s][0], 2), round(linci[s][1], 2), round(boot[s][1], 2))
               for s in GOLD}))
    check("R7 every over-budget service's interval clears its budget", all(R["ci"][s][0] > bud[s] + 0.05 for s in GOLD)
          and all(boot[s][0] > bud[s] + 0.05 for s in GOLD), str({s: round(R["ci"][s][0] - bud[s], 3) for s in GOLD}))

    # ---------------------------------------------------------------- margins
    def edge(v):
        return round(0.05 - abs(v - K.r1(v)), 3) if abs(v - K.r1(v)) <= 0.05 else 0.0
    dist = {s: edge(S[s]["sli"]) for s in K.SVC}
    check("M1 every boundary-threshold SLI 0.015 or more from a rounding line (every SLI's distance reported)",
          all(dist[s] >= 0.015 for s in exact), "boundary %s; bridged %s" % (
              {s: dist[s] for s in exact}, {s: dist[s] for s in bridged}))
    vmarg = {s: round(S[s]["sli"] - (bud[s] + 0.05), 3) for s in K.SVC}
    check("M2 every verdict 0.1 or more from its budget line", all(abs(v) >= 0.1 for v in vmarg.values()), str(vmarg))
    ratio = {"%s over %s" % (a, b): round(S[a]["over_requests"] / S[b]["over_requests"], 3)
             for a, b in zip(P["order"], P["order"][1:])}
    check("M3 the five's order holds by a twentieth of the next service's count or more",
          min(ratio.values()) >= 1.05, str(ratio))
    check("M3 the five's order holds across every split and weighting",
          all(order_of(f, bud) == P["order"] for f in fam.values()) and all(order_of(v, bud) == P["order"] for v in
                                                                            WV.values()), ", ".join(P["order"]))
    shares = {s: round(P["share"][s], 2) for s in P["order"]}
    sh_edge = {s: round(0.5 - abs(P["share"][s] - D.whole(P["share"][s])), 2) for s in P["order"]}
    print("NOTE  M3 shares %s; distance of each to its whole-per-cent line %s; together %.2f, beyond %.0f" % (
        shares, sh_edge, P["together"], P["beyond"]))

    # ---------------------------------------------------------------- the semantic fork rows
    check("SF1 December in Lisbon time is UTC: no span moves between days", True, "PR-SLO-3 3.1; WET all month")
    on_thr = sum(1 for i in np.nonzero(g.dec)[0] if g.ms[i] == g.thr[g.svc[i]])
    check("SF2 over threshold is strictly greater: no span sits on a threshold or on a boundary that is one",
          on_thr == 0, "%d spans on a threshold; boundary thresholds %s" % (on_thr, ", ".join(
              "%s %d" % (s, g.thr[s]) for s in exact)))
    check("SF4 the balancer's probes are not requests", not any(g.name == "GET /healthz"),
          "PR-SLO-3 2.2; the edge sampler never sees a probe, so the export carries none")
    seen, retried = set(), 0
    for i in np.nonzero(g.dec & (g.svc == "partner-gateway"))[0]:
        key = (g.tr[i], g.name[i])
        retried += key in seen
        seen.add(key)
    check("SF5 a retried call is a request: both spans of a retried partner-gateway call are counted", retried > 0,
          "PR-SLO-3 2.2: any call a caller sent; %d second calls in the export" % retried)
    err_rows = sum(1 for row in csv.DictReader(open(os.path.join(target, K.FILES["spanmetrics"])))
                   if row["status_code"] == "STATUS_CODE_ERROR")
    check("SF6 errors count like any request: the span metrics' error and non-error series are summed",
          err_rows > 0, "PR-SLO-3 2.4; %d error rows in the span metrics (SF27: summed, they equal the export)" % err_rows)
    check("SF7 a request belongs to the time its service started it", True, "PR-SLO-3 2.4")
    check("SF8 the weighting base (balancer count or weighted kept count)", True, "R7 above: same one decimal")
    check("SF9 the root's hour or the span's own hour", True, "R7 above")
    check("SF10 spans of traces begun before the export", True, "R7 above")
    check("SF12 an incident ends when the status page shows its last component operational",
          all(x["end"] <= x["resolved"] for x in dec), "PR-SLO-3 3.2 and 5.2")
    check("SF13 a December incident with no status post leaves nothing out", len([x for x in incs if x["declared"] >=
                                                                                 AN.DEC0]) == 7, "PR-SLO-3 5.2")
    check("SF15 shares are of the over-threshold requests all the SLIs count", abs(sum(P["share"].values()) - 100)
          < 1e-6, "the base is the ten SLIs' numerators")
    # an onset is stated to the nearest five minutes: the rounding keeps every pair of rises in its order, ten minutes
    # or more apart, so a time read a few minutes either way grades the same
    gaps5 = []
    for x in dec:
        on = R["onset"][x["id"]]
        f = att[x["id"]]
        for s_, v in on.items():
            if s_ != f and v:
                a5 = D.about((AN.DEC0 + dt.timedelta(seconds=on[f][0])).strftime("%H:%M"))
                b5 = D.about((AN.DEC0 + dt.timedelta(seconds=v[0])).strftime("%H:%M"))
                gaps5.append((x["id"], a5, b5))
    check("SF19 an onset stated to five minutes keeps each cause's rise ten minutes or more before the others'",
          all((int(b[:2]) * 60 + int(b[3:])) - (int(a[:2]) * 60 + int(a[3:])) >= 10 for _, a, b in gaps5),
          "; ".join("%s %s before %s" % g_ for g_ in gaps5))
    gone_n = {s: float(g.N[s][hrs < cut].sum()) for s in K.SVC}
    check("SF20 December's hours before the export count, measured from the span metrics",
          all(abs(R["fill"][s][1] - gone_n[s]) < 1e-6 and R["fill"][s][0] > 0 for s in K.SVC) and cut == 274,
          "PR-SLO-3 2.2 (kept or not) and 3.1 (December); %d hours, %s%% of the edge requests" % (cut, F["gone_pct"]))

    # ---------------------------------------------------------------- the goldens against the figure set
    gdir = os.path.join(os.path.dirname(os.path.abspath(target)), "golden")
    gcsv, gdoc = os.path.join(gdir, K.CSV_OUT), os.path.join(gdir, K.DOCX_OUT)
    if os.path.exists(gcsv) and os.path.exists(gdoc):
        rows = list(csv.reader(open(gcsv)))
        want_rows = [[s, F["sli"][s], F["budget"][s], F["ran_over"][s]] + F["minutes"][s] for s in K.SVC]
        check("GOLD1 the CSV carries the figure set's SLI, budget, verdict and minutes, a row per service",
              rows[1:] == want_rows and rows[0][0] == "service", "%d rows" % (len(rows) - 1))
        doc = text_of(gdoc)
        lines = [" | ".join([str(k), s_, F["share_pct"][s_], F["sli"][s_], "%s to %s" % tuple(F["ci"][s_]),
                             F["budget"][s_]]) for k, s_ in enumerate(F["start_order"], 1)]
        lines += [" | ".join([s, F["threshold_ms"][s], F["sli"][s], F["budget"][s], F["ran_over"][s]]) for s in K.SVC]
        lines += [" | ".join([x["id"], x["declared"], ", ".join(x["named"]), x["cause"]]) for x in F["incidents"]]
        lines += ["served %s%% of the requests" % F["together_pct"], "about %s more than" % F["beyond_budget"]]
        lost = [ln for ln in lines if ln not in doc]
        check("GOLD2 the review carries the figure set's start order, shares, intervals, SLIs, owners and programme "
              "figures", not lost, "; ".join(lost[:3]) or "%d lines" % len(lines))
        fj = os.path.join(HERE, "figures.json")
        if os.path.exists(fj):
            FJ = json.load(open(fj))
            keys = ("over", "sli", "budget", "ran_over", "start_order", "share_pct", "together_pct", "beyond_budget",
                    "ci", "minutes", "root_cause", "sli_band")
            off = [k for k in keys if json.dumps(FJ.get(k), sort_keys=True) != json.dumps(F[k], sort_keys=True)]
            check("GOLD3 figures.json is this run's figure set", not off, ", ".join(off) or "%d keys" % len(keys))
    else:
        print("NOTE  no goldens beside %s: GOLD1 to GOLD3 not run" % target)

    # ---------------------------------------------------------------- the documents
    slo = text_of(os.path.join(target, K.FILES["slo"]))
    check("DOC1 the standard files the incident clause (positive control)", "owned the incident's root cause" in slo
          and "does not." in slo, "")
    check("DOC2 the standard names no method for finding the cause", not re.search(
        r"self.time|own handling time|changepoint|onset|first to slow|load curve|trace", slo.split("3.2")[1].split("3.4")[0],
        re.I), "")
    check("DOC3 no December review records a cause", all(not x["cause"] for x in dec), "")
    check("DOC4 the standard says nothing of the tracing store's retention or its span metrics", not re.search(
        r"31 days|retain|retention|the tracing store holds|expire|span metric|histogram|bucket", slo, re.I), "")
    print("%d checks failed" % len(FAILS) if FAILS else "all checks passed")
    return len(FAILS)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    sys.exit(main(tgt))
