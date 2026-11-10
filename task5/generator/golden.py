"""task5 architecture 4: the golden deliverables, computed from the shipped pack alone.

compute() carries the pack through the golden route (methods.Pack.certify), the December 2025 base, the reconciliation
to the published table, the replay on December 2025, the shortcuts a reader will ask about and the standing family
behind every band; the writers put the certification workbook, the employer list and the memo on disk."""
import csv
import math
import os

import numpy as np
import pandas as pd

import methods as M
import world as W

KIND_ORDER = ["batch", "habit", "alone", "twoq", "new"]
KIND_LABEL = {
    "rep": "reported",
    "batch": "estimated: report expected in an agent's batch not yet received",
    "habit": "estimated: files after the cut-off every quarter",
    "alone": "estimated: report outstanding on its own (its usual batch arrived without it, or it files singly)",
    "twoq": "estimated: no report for two quarters",
    "new": "estimated: account established, first report not yet received",
    "unreg": "estimated: employers with no account yet",
}
KIND_SHORT = {"batch": "In an agent's batch not yet received", "habit": "Files after the cut-off every quarter",
              "alone": "Outstanding on its own: its usual batch arrived without it, or it files singly",
              "twoq": "No report for two quarters", "new": "Account established, first report not yet received"}
CONSTRUCTION = "1012"


def load_pack(folder):
    rd = lambda k: pd.read_csv(os.path.join(folder, W.FILES[k]), dtype=str, keep_default_na=False)
    return M.Pack(rd("reports"), rd("accounts"), rd("status"), rd("worksites"), rd("counties"), rd("naics"))


def read_published(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=False)["County"]
    out = {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        if row[0] and str(row[0]).strip().isdigit():
            out[str(row[0]).zfill(3)] = int(row[5])
    return pd.Series(out)


def r100(x):
    return int(math.floor(x / 100.0 + 0.5)) * 100


def r10(x):
    return int(math.floor(x / 10.0 + 0.5)) * 10


def r1(x):
    return round(float(x) + 1e-9, 1) + 0.0


def down(x, unit):
    return math.floor(x / unit + 1e-9) * unit


def up(x, unit):
    return math.ceil(x / unit - 1e-9) * unit


def kept(est, v, idx):
    p = v.loc[idx, "prior"].fillna(v.loc[idx, "prior_any"]).sum()
    return float(est[idx].sum() / p) if p > 0 else float("nan")


def summary(pk, X, base):
    """the graded figures one certify() result carries"""
    v = X["view"]
    ch = M.changes(X["total"], base)
    b = v.index[v["kind"] == "batch"]
    cons = (v.loc[b, "ss"] == CONSTRUCTION).values
    bc, bo = b[cons], b[~cons]
    o = v[(v["prior"] > 0) & v["kind"].isin(["rep", "alone"]) & (v["ss"] == CONSTRUCTION)]
    tc = float(o.loc[o["kind"] == "alone", "prior"].sum() / o["prior"].sum()) if len(o) else float("nan")
    return dict(total=X["total"], reported=X["reported"], estimated=X["outstanding"] + X["unregistered"],
                outstanding=X["outstanding"], unregistered=X["unregistered"], change=ch, designated=M.designated(ch),
                state_total=float(X["total"].sum()), state_change=float(100 * (X["total"].sum() / base.sum() - 1)),
                k_alone=float(X["k_alone"]), unreg_jobs=float(X["unregistered"].sum()), unreg_n=float(X["uinfo"].get("n", 0.0)),
                counts={k: int((v["kind"] == k).sum()) for k in KIND_ORDER},
                kept_constr=kept(X["est"], v, bc), kept_other=kept(X["est"], v, bo), kept_batch=kept(X["est"], v, b),
                batch_jobs=float(X["est"][b].sum()), trouble_constr=tc)


def compute(pk, published, bands=True, quiet=True):
    G = {}
    cut = M.CUT[W.FLASH_Q]
    main = pk.certify()
    base = pk.base(W.BASE_Q, M.EXTRACT)
    S = summary(pk, main, base)
    v = main["view"]
    G.update(main=main, base=base, view=v, **S)
    G["census"] = dict(liable=len(v), received=int(v["rep"].sum()), outstanding=int((~v["rep"]).sum()))
    # December 2025: employers liable for that quarter whose report has still not come. They are counted at nought
    # (silent five quarters; two quarters out keep next to nothing); carried at their last report they would add a few
    # hundred jobs, which is the alternative base the bands allow for
    vb = pk.view(W.BASE_Q, M.EXTRACT)
    end = pk.ended(M.EXTRACT)
    gone = set(end[end <= M.M3START[W.BASE_Q]].index)
    sil = vb[(~vb["rep"]) & ~vb.index.isin(gone)]
    carry = sil["prior"].fillna(sil["prior_any"]).fillna(0.0)
    carry_c, _ = pk.to_counties(carry.astype(float), W.BASE_Q, M.EXTRACT, "site")
    G["base_silent"] = dict(n=int(len(sil)), jobs=float(carry.sum()), by_county=carry_c)
    # the outstanding by kind
    kinds = {}
    for k in KIND_ORDER:
        idx = v.index[v["kind"] == k]
        p = v.loc[idx, "prior"].fillna(v.loc[idx, "prior_any"]).fillna(0.0)
        kinds[k] = dict(n=len(idx), prior=float(p.sum()), est=float(main["est"][idx].sum()))
    G["kinds"] = kinds
    G["k_twoq"], G["k_batch_hist"], G["new_mean"], G["mature"] = main["k_twoq"], main["k_batch_hist"], main["new_mean"], main["mature"]
    # this quarter's trouble beside earlier fourth quarters
    tr = {}
    for q in (3, 7, 11, 12, 13, 14, 15):
        vq = pk.view(q)
        o = vq[(vq["prior"] > 0) & vq["kind"].isin(["rep", "alone"])]
        al = o[o["kind"] == "alone"]
        c_ = o["ss"] == CONSTRUCTION
        tr[q] = dict(constr=float(al[al["ss"] == CONSTRUCTION]["prior"].sum() / o[c_]["prior"].sum()),
                     other=float(al[al["ss"] != CONSTRUCTION]["prior"].sum() / o[~c_]["prior"].sum()),
                     n_alone=int(len(vq[vq["kind"] == "alone"])), n_out=int((~vq["rep"]).sum()))
    G["trouble"] = tr
    rep_route = pk.certify(route=dict(batch="reporters"))
    SR = summary(pk, rep_route, base)
    G["reporters"] = dict(kept_constr=SR["kept_constr"], kept_other=SR["kept_other"], kept_batch=SR["kept_batch"],
                          batch_jobs=SR["batch_jobs"])
    G["transport_jobs"] = SR["batch_jobs"] - S["batch_jobs"]
    # the share kept under the hurried reading (every closed quarter, the unresolved left out) and with the unresolved
    # taken at nought
    G["k_allclosed"] = float(pk.certify(route=dict(alone="allclosed"))["k_alone"])
    G["k_allzero"] = float(pk.certify(route=dict(alone="allzero"))["k_alone"])
    oc = main["outcomes"]
    G["pooled"] = dict(survive=float(oc["pooled_survive_n"].get(W.FLASH_Q % 4, float("nan"))),
                       kept=float(oc["pooled_kept"].get(W.FLASH_Q % 4, float("nan"))))
    # employers with no account yet
    G["uinfo"] = main["uinfo"]
    # worksite splits
    sh = pk.shares(W.FLASH_Q, cut, "site")
    multi = v.index[v["multi"]]
    shm = sh[sh["acct"].isin(multi)]
    own = set(shm.loc[shm["src"] == "own", "acct"])
    G["sites"] = dict(multi=len(multi), own=len(own), carried=len(set(shm["acct"]) - own))
    est_all = main["est"]
    lat, _ = pk.to_counties(est_all, W.FLASH_Q, cut, "latest")
    sit, _ = pk.to_counties(est_all, W.FLASH_Q, cut, "site")
    ya, _ = pk.to_counties(est_all, W.FLASH_Q, cut, "yearago")
    G["latest_minus_site"] = lat - sit
    G["yearago_minus_site"] = ya - sit
    # December 2025 against the published table
    pc = M.TS(W.PUBLISHED_CUT)
    pub, cur = pk.latest(W.BASE_Q, pc)["m3"], pk.latest(W.BASE_Q, M.EXTRACT)["m3"]
    est_d = pk.a["est"]
    notin = cur.index.difference(pub.index)
    late = notin[(est_d.reindex(notin) <= pc).values]
    newa = notin[(est_d.reindex(notin) > pc).values]
    both = cur.index.intersection(pub.index)
    chg = both[(cur[both] != pub[both]).values]
    G["recon"] = dict(published=int(published.sum()), published_county=published, now=int(cur.sum()),
                      late_jobs=int(cur[late].sum()), late_n=len(late), new_jobs=int(cur[newa].sum()), new_n=len(newa),
                      amend_jobs=int((cur[chg] - pub[chg]).sum()), amend_n=len(chg), rebuilt=int(pub.sum()))
    # the replay on December 2025
    R = pk.certify(q=W.BASE_Q)
    rd = (R["total"] / base - 1) * 100
    G["replay"] = dict(total=R["total"], diff=rd, state_total=float(R["total"].sum()),
                       state_diff=float(100 * (R["total"].sum() / base.sum() - 1)), mean_abs=float(rd.abs().mean()),
                       max_abs=float(rd.abs().max()), max_county=rd.abs().idxmax(), k_alone=float(R["k_alone"]),
                       unreg_jobs=float(R["unregistered"].sum()), mature=R["mature"])
    # the shortcuts
    routes = []
    for name, rt in M.SHORTCUTS:
        X = pk.certify(route=rt)
        s = summary(pk, X, base)
        routes.append(dict(name=name, route=rt, state_total=s["state_total"], state_change=s["state_change"],
                           designated=s["designated"], change=s["change"], total=s["total"], unreg_jobs=s["unreg_jobs"],
                           k_alone=s["k_alone"], kept_constr=s["kept_constr"], total_est=float(s["estimated"].sum()),
                           estimated=s["estimated"], counts=s["counts"]))
        if not quiet:
            print("route %-60s %s" % (name[:60], ",".join(W.NAMES[c] for c in s["designated"])))
    G["routes"] = routes
    if bands:
        fam, rfam = [], []
        for name, rt in M.FAMILY:
            X = pk.certify(route=rt)
            s = summary(pk, X, base)
            s["name"] = name
            fam.append(s)
            sl, _ = pk.to_counties(X["est"], W.FLASH_Q, cut, "latest")
            ss_, _ = pk.to_counties(X["est"], W.FLASH_Q, cut, "site")
            s["latest_minus_site"] = sl - ss_
            Rr = pk.certify(q=W.BASE_Q, route=rt)
            d = (Rr["total"] / base - 1) * 100
            rfam.append(dict(name=name, state_diff=float(100 * (Rr["total"].sum() / base.sum() - 1)), mean_abs=float(d.abs().mean()),
                             total=Rr["total"], diff=d))
        alt = dict(summary(pk, main, base + G["base_silent"]["by_county"]))
        alt["name"] = "employers still silent for December 2025 carried at their last report"
        alt["latest_minus_site"] = fam[0]["latest_minus_site"]
        fam.append(alt)
        G["family"], G["replay_family"] = fam, rfam
        tot = pd.DataFrame({i: f["total"] for i, f in enumerate(fam)})
        est = pd.DataFrame({i: f["estimated"] for i, f in enumerate(fam)})
        chf = pd.DataFrame({i: f["change"] for i, f in enumerate(fam)})
        # a band holds every member of the family, padded by a quarter of their spread, and never comes nearer the
        # golden than a floor an independent rebuild of the same estimate stays inside: half a point on a county's
        # change and the same share of its jobs (two rebuilds by the stage 4 judge sat up to 0.45 of a point away)
        FLOOR = 0.5
        B = {}
        B["change"], B["total"], B["estimated"] = {}, {}, {}
        for c in W.CODES:
            lo, hi = chf.loc[c].min(), chf.loc[c].max()
            pad = 0.25 * (hi - lo) + 0.03
            lo, hi = min(lo - pad, S["change"][c] - FLOOR), max(hi + pad, S["change"][c] + FLOOR)
            B["change"][c] = (round(down(lo, 0.1), 1), round(up(hi, 0.1), 1))
            fl = FLOOR / 100.0 * base[c]
            lo, hi = tot.loc[c].min(), tot.loc[c].max()
            pad = 0.25 * (hi - lo) + 8
            B["total"][c] = (down(min(lo - pad, S["total"][c] - fl), 10), up(max(hi + pad, S["total"][c] + fl), 10))
            lo, hi = est.loc[c].min(), est.loc[c].max()
            pad = 0.25 * (hi - lo) + 8
            B["estimated"][c] = (down(min(lo - pad, S["estimated"][c] - fl), 10), up(max(hi + pad, S["estimated"][c] + fl), 10))
        st = [f["state_total"] for f in fam]
        sfl = 0.002 * S["state_total"]          # a fifth of a per cent of the state's jobs
        B["state_total"] = (down(min(min(st) - 100, S["state_total"] - sfl), 100), up(max(max(st) + 100, S["state_total"] + sfl), 100))
        se = [float(f["estimated"].sum()) for f in fam]
        se0 = float(S["estimated"].sum())
        B["state_estimated"] = (down(min(min(se) - 100, se0 - sfl), 100), up(max(max(se) + 100, se0 + sfl), 100))
        sc = [f["state_change"] for f in fam]
        B["state_change"] = (round(down(min(min(sc) - 0.03, S["state_change"] - 0.2), 0.1), 1),
                             round(up(max(max(sc) + 0.03, S["state_change"] + 0.2), 0.1), 1))
        ks = [f["k_alone"] for f in fam]
        B["k_alone"] = (round(down(min(min(ks) - 0.012, S["k_alone"] - 0.045), 0.01), 2),
                        round(up(max(max(ks) + 0.012, S["k_alone"] + 0.045), 0.01), 2))
        uj = [f["unreg_jobs"] for f in fam]
        B["unreg_jobs"] = (down(min(uj) - 150, 100), up(max(uj) + 150, 100))
        un = [f["unreg_n"] for f in fam]
        B["unreg_n"] = (down(min(un) - 30, 10), up(max(un) + 30, 10))
        for k in KIND_ORDER:
            cs = [f["counts"][k] for f in fam]
            w_ = max(10, 0.02 * max(cs))
            B["n_" + k] = (int(down(min(cs) - w_, 10)), int(up(max(cs) + w_, 10)))
        ah = [f["counts"]["alone"] + f["counts"]["habit"] for f in fam]
        B["n_alone_habit"] = (int(down(min(ah) - 0.02 * max(ah), 10)), int(up(max(ah) + 0.02 * max(ah), 10)))
        # the split between the two moves with the rule for "every quarter": a band of 15 per cent of the habitual
        hb = [f["counts"]["habit"] for f in fam]
        w_ = 0.15 * max(hb)
        B["n_habit"] = (int(down(min(hb) - w_, 10)), int(up(max(hb) + w_, 10)))
        al_ = [f["counts"]["alone"] for f in fam]
        B["n_alone"] = (int(down(min(al_) - w_, 10)), int(up(max(al_) + w_, 10)))
        tcs = [100 * f["trouble_constr"] for f in fam]
        B["trouble_constr"] = (round(down(min(tcs) - 0.4, 0.1), 1), round(up(max(tcs) + 0.4, 0.1), 1))
        kc = [f["kept_constr"] for f in fam]
        B["kept_constr"] = (round(down(min(kc) - 0.012, 0.01), 2), round(up(max(kc) + 0.012, 0.01), 2))
        tj = [SR["batch_jobs"] - f["batch_jobs"] for f in fam if f.get("batch_jobs") is not None and "trouble not carried" not in f["name"]]
        B["transport_jobs"] = (down(min(min(tj) - 40, 0.75 * G["transport_jobs"]), 50), up(max(max(tj) + 40, 1.25 * G["transport_jobs"]), 50))
        ls = pd.DataFrame({i: f["latest_minus_site"] for i, f in enumerate(fam)})
        B["latest_minus_site"] = {}
        for c in W.CODES:
            g0 = float(G["latest_minus_site"][c])
            w_ = max(30.0, 0.25 * abs(g0))
            B["latest_minus_site"][c] = (down(min(ls.loc[c].min() - 15, g0 - w_), 10), up(max(ls.loc[c].max() + 15, g0 + w_), 10))
        rs = [f["state_diff"] for f in rfam]
        r0 = G["replay"]["state_diff"]
        # the replay moves with the method's own unregistered estimate on a year with less history behind it
        B["replay_state_diff"] = (round(down(min(min(rs) - 0.04, r0 - 0.25), 0.05), 2), round(up(max(max(rs) + 0.04, r0 + 0.2), 0.05), 2))
        rm = [f["mean_abs"] for f in rfam]
        m0 = G["replay"]["mean_abs"]
        B["replay_mean_abs"] = (round(max(0.0, down(min(min(rm) - 0.03, m0 - 0.12), 0.05)), 2), round(up(max(max(rm) + 0.03, m0 + 0.17), 0.05), 2))
        rt_ = pd.DataFrame({i: f["total"] for i, f in enumerate(rfam)})
        B["replay_total"] = {}
        for c in W.CODES:
            lo, hi = rt_.loc[c].min(), rt_.loc[c].max()
            pad = 0.25 * (hi - lo) + 8
            fl = FLOOR / 100.0 * base[c]
            B["replay_total"][c] = (down(min(lo - pad, G["replay"]["total"][c] - fl), 10), up(max(hi + pad, G["replay"]["total"][c] + fl), 10))
        G["bands"] = B
    return G


# ------------------------------------------------------------------------------------------------- the employer list
def employer_rows(pk, G):
    main = G["main"]
    kind = main["kind"]
    acc = pk.a
    rows = pd.concat([main["rows_rep"], main["rows_out"]], ignore_index=True)
    rows = rows[rows["jobs"].notna()]
    out = []
    for a_, c, e in sorted(zip(rows["acct"], rows["county"], rows["jobs"])):
        k = kind[a_]
        out.append((acc.loc[a_, "account_no"], acc.loc[a_, "legal_name"], c, W.NAMES[c], "Y" if k == "rep" else "N",
                    "%.1f" % e, KIND_LABEL[k]))
    for c in W.CODES:
        out.append(("", "Employers with no account yet", c, W.NAMES[c], "N", "%.1f" % G["unregistered"][c], KIND_LABEL["unreg"]))
    return out


def write_employers(pk, G, path):
    rows = employer_rows(pk, G)
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(["account_no", "legal_name", "county_code", "county", "report_received", "december_2026_jobs", "basis"])
        wr.writerows(rows)
    return len(rows)


# ----------------------------------------------------------------------------------------------------- the workbook
def chart_title(G):
    des = [W.NAMES[c] for c in G["designated"]]
    if not des:
        return "No county is at or below the -2.0% line"
    return ("%s and %s are" % (", ".join(des[:-1]), des[-1]) if len(des) > 1 else "%s is" % des[0]) + " the only counties at or below the -2.0% line"


def write_certification(pk, G, path):
    import openpyxl
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.chart.marker import DataPoint
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="E7EEF5")
    wrap = Alignment(wrap_text=True, vertical="top")

    def header(ws, row, heads, col0=1):
        for k, h in enumerate(heads):
            cell = ws.cell(row=row, column=col0 + k, value=h)
            cell.font, cell.alignment, cell.fill = bold, wrap, head_fill
            cell.border = Border(bottom=Side(style="thin"))

    def put(ws, row, col, v, fmt=None, b=False):
        cell = ws.cell(row=row, column=col, value=v)
        if fmt:
            cell.number_format = fmt
        if b:
            cell.font = bold
        return cell

    wb = openpyxl.Workbook()
    # ---- Certification
    ws = wb.active
    ws.title = "Certification"
    ws["A1"] = "Community Transition Fund: December covered employment, fund year 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Franklin Department of Labor, Labor Market Information. For the Commissioner's certification under "
                "section 5 of the Act.")
    ws["A3"] = ("From the Unemployment Insurance Tax Division's records as they stood at the close of February 15, 2027. "
                "Covered employment for the pay period including the 12th of the month, by worksite county.")
    des = [W.NAMES[c] for c in G["designated"]]
    ws["A5"] = "Counties to designate under section 4 (December 2026 at least 2.0 percent below December 2025): " + (", ".join(des) if des else "none")
    ws["A5"].font = bold
    hr = 7
    header(ws, hr, ["County code", "County", "December 2025 jobs, as now on file", "December 2026 jobs on reports received",
                    "December 2026 jobs estimated", "December 2026 jobs", "Change on December 2025 (%)", "Designate"])
    r = hr + 1
    for c in W.CODES:
        vals = [c, W.NAMES[c], r10(G["base"][c]), r10(G["reported"][c]), r10(G["estimated"][c]), r10(G["total"][c]),
                r1(G["change"][c]), "Yes" if c in G["designated"] else "No"]
        for k, val in enumerate(vals):
            put(ws, r, k + 1, val, "#,##0" if k in (2, 3, 4, 5) else ("0.0" if k == 6 else None), c in G["designated"])
        r += 1
    put(ws, r, 2, "State", b=True)
    for k, val in enumerate([G["base"].sum(), G["reported"].sum(), G["estimated"].sum(), G["total"].sum()]):
        put(ws, r, 3 + k, r100(val), "#,##0", True)
    put(ws, r, 7, r1(G["state_change"]), "0.0", True)
    ws.cell(row=r + 2, column=1, value="County jobs are rounded to the nearest ten and the state's to the nearest hundred, so parts may not add to "
                                        "totals; the change is computed before rounding. The estimated jobs are set out on the next sheet.")
    ws.cell(row=r + 3, column=1, value="Prepared by %s, %s, February 26, 2027." % W.PEOPLE["lmi_director"][:2])
    ws.cell(row=hr, column=11, value="County").font = bold
    ws.cell(row=hr, column=12, value="Change on December 2025 (%)").font = bold
    ws.cell(row=hr, column=13, value="Designation line, -2.0%").font = bold
    for k_ in (11, 12, 13):
        ws.cell(row=hr, column=k_).alignment = wrap
    for i, c in enumerate(W.CODES):
        ws.cell(row=hr + 1 + i, column=11, value=W.NAMES[c])
        ws.cell(row=hr + 1 + i, column=12, value=r1(G["change"][c])).number_format = "0.0"
        ws.cell(row=hr + 1 + i, column=13, value=W.THRESHOLD).number_format = "0.0"
    bar = BarChart()
    bar.type = "col"
    bar.title = chart_title(G)
    bar.y_axis.title = "Change in covered jobs, December 2026 on December 2025 (%)"
    bar.y_axis.number_format = "0.0"
    bar.add_data(Reference(ws, min_col=12, min_row=hr, max_row=hr + len(W.CODES)), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=11, min_row=hr + 1, max_row=hr + len(W.CODES)))
    bar.dataLabels = DataLabelList()
    bar.dataLabels.showVal = True
    line = LineChart()
    line.add_data(Reference(ws, min_col=13, min_row=hr, max_row=hr + len(W.CODES)), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "C00000"
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    ser = bar.series[0]
    ser.graphicalProperties.solidFill = "8497B0"
    ser.graphicalProperties.line.solidFill = "8497B0"
    for i, c in enumerate(W.CODES):
        if c in G["designated"]:
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "A9332B"
            pt.graphicalProperties.line.solidFill = "A9332B"
            ser.dPt.append(pt)
    bar += line
    bar.legend.position = "b"
    bar.height, bar.width = 9.5, 22
    ws.add_chart(bar, "A%d" % (r + 6))
    ws.freeze_panes = "A%d" % (hr + 1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = "A1:H%d" % (r + 26)
    for k, wdt in enumerate([11, 13, 14, 15, 14, 13, 13, 11, 3, 3, 13, 11, 9]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    ws.row_dimensions[hr].height = 62

    # ---- Estimated jobs
    es = wb.create_sheet("Estimated jobs")
    es["A1"] = "December 2026 jobs not on a report received by February 15, 2027"
    es["A1"].font = Font(bold=True, size=12)
    cz = G["census"]
    for i, (a, b) in enumerate([("Employer accounts liable for the fourth quarter of 2026", cz["liable"]),
                                ("Reports received by the cut-off", cz["received"]), ("Reports outstanding", cz["outstanding"])]):
        put(es, 3 + i, 1, a)
        put(es, 3 + i, 2, b, "#,##0")
    header(es, 7, ["Why the jobs are estimated", "Employers", "Jobs the quarter before (September 2026)", "Share carried",
                   "December 2026 jobs", "How estimated"])
    k_al, tr = G["k_alone"], G["trouble"]
    how = {
        "batch": "September jobs moved by the December-on-September change of the reporting employers in its county and "
                 "supersector, except for the share of its supersector and size class's jobs that sits this quarter at "
                 "employers outstanding on their own, which is carried at %.2f as in the third row." % k_al,
        "habit": "As the row above.",
        "alone": "September jobs times %.2f: what employers in the same position at the cut-offs of %s to %s kept in the "
                 "quarter's third month, every one since resolved by a late report, a closure or an inactivation."
                 % (k_al, W.quarter_label(G["mature"][0]), W.quarter_label(G["mature"][-1])),
        "twoq": "Last reported jobs times %.3f, measured the same way." % G["k_twoq"],
        "new": "%.1f jobs each: what such accounts turned out to have at the same cut-offs." % G["new_mean"],
    }
    rr = 8
    for k in KIND_ORDER:
        d = G["kinds"][k]
        put(es, rr, 1, KIND_SHORT[k])
        put(es, rr, 2, d["n"], "#,##0")
        put(es, rr, 3, r100(d["prior"]) if d["prior"] else None, "#,##0")
        put(es, rr, 4, round(d["est"] / d["prior"], 2) if d["prior"] > 0 else None, "0.00")
        put(es, rr, 5, r100(d["est"]), "#,##0")
        put(es, rr, 6, how[k]).alignment = wrap
        rr += 1
    ui = G["uinfo"]
    put(es, rr, 1, "Liable for the quarter, no account yet")
    put(es, rr, 2, int(round(ui["n"], -1)), "#,##0")
    put(es, rr, 5, r100(G["unreg_jobs"]), "#,##0")
    put(es, rr, 6, "%d new employers of the quarter had an account by the cut-off; at earlier fourth-quarter cut-offs %.1f "
                   "more were set up later for each one registered by then, and the late ones had %.1f jobs each in the "
                   "third month. Employers of earlier quarters still without an account are added the same way, county by "
                   "county." % (ui["reg_own"], ui["c_own"], ui["j_own"])).alignment = wrap
    rr += 1
    put(es, rr, 1, "Total estimated", b=True)
    put(es, rr, 5, r100(G["estimated"].sum()), "#,##0", True)
    rr += 2
    put(es, rr, 1, "A batch is three or more reports received in the same second, which is how a payroll agent's file "
                   "arrives; an employer's batch is the one its third-quarter report came in, and it has arrived when at "
                   "least half of the other employers in it have reported. Employers outstanding on their own hold %.1f "
                   "percent of construction jobs this quarter, against %.1f, %.1f and %.1f percent at the fourth-quarter "
                   "cut-offs of 2023, 2024 and 2025 (%.1f, %.1f and %.1f percent at the first three cut-offs of 2026), so "
                   "construction employers in late batches are carried at %.2f of their September jobs; on the reporting "
                   "employers' change alone they would be carried at %.2f."
        % (100 * tr[15]["constr"], 100 * tr[3]["constr"], 100 * tr[7]["constr"], 100 * tr[11]["constr"],
           100 * tr[12]["constr"], 100 * tr[13]["constr"], 100 * tr[14]["constr"],
           G["kept_constr"], G["reporters"]["kept_constr"])).alignment = wrap
    rr += 2
    header(es, rr, ["County", "Reports outstanding", "No account yet", "Estimated, total",
                    "Change in the county's jobs if the latest worksite reports' split were used instead"])
    rr += 1
    for c in W.CODES:
        put(es, rr, 1, W.NAMES[c])
        put(es, rr, 2, r10(G["outstanding"][c]), "#,##0")
        put(es, rr, 3, r10(G["unregistered"][c]), "#,##0")
        put(es, rr, 4, r10(G["estimated"][c]), "#,##0")
        put(es, rr, 5, int(round(G["latest_minus_site"][c], -1)), "#,##0;-#,##0;0")
        rr += 1
    put(es, rr, 1, "State", b=True)
    put(es, rr, 2, r100(G["outstanding"].sum()), "#,##0", True)
    put(es, rr, 3, r100(G["unreg_jobs"]), "#,##0", True)
    put(es, rr, 4, r100(G["estimated"].sum()), "#,##0", True)
    st = G["sites"]
    put(es, rr + 2, 1, "%d liable employers report by worksite; the fourth-quarter worksite report of %d was on file. For the "
                       "other %d each worksite on the latest report is carried by its own change between the same two "
                       "quarters a year earlier, and the employer's December jobs are split in those proportions."
        % (st["multi"], st["own"], st["carried"])).alignment = wrap
    for col, wdt in zip("ABCDEF", [46, 13, 16, 12, 16, 92]):
        es.column_dimensions[col].width = wdt
    es.row_dimensions[7].height = 48

    # ---- December 2025
    d5 = wb.create_sheet("December 2025")
    d5["A1"] = "December 2025 covered employment: as now on file against the published table"
    d5["A1"].font = Font(bold=True, size=12)
    rc = G["recon"]
    lines = [("Published, fourth quarter 2025 county table (reports posted through May 31, 2026)", rc["published"]),
             ("Reports received after May 31, 2026 from accounts established by then (%d accounts)" % rc["late_n"], rc["late_jobs"]),
             ("Reports of accounts established after May 31, 2026 (%d accounts)" % rc["new_n"], rc["new_jobs"]),
             ("Reports amended after May 31, 2026 (%d reports), net" % rc["amend_n"], rc["amend_jobs"]),
             ("As now on file, February 15, 2027", rc["now"])]
    for i, (a, b) in enumerate(lines):
        put(d5, 3 + i, 1, a, b=i in (0, 4))
        put(d5, 3 + i, 2, b, "#,##0;-#,##0", i in (0, 4))
    put(d5, 9, 1, "Unexplained")
    put(d5, 9, 2, rc["now"] - rc["published"] - rc["late_jobs"] - rc["new_jobs"] - rc["amend_jobs"], "#,##0;-#,##0;0")
    header(d5, 11, ["County", "Published", "As now on file", "Difference"])
    for i, c in enumerate(W.CODES):
        put(d5, 12 + i, 1, W.NAMES[c])
        put(d5, 12 + i, 2, int(rc["published_county"][c]), "#,##0")
        put(d5, 12 + i, 3, int(round(G["base"][c])), "#,##0")
        put(d5, 12 + i, 4, int(round(G["base"][c])) - int(rc["published_county"][c]), "#,##0;-#,##0;0")
    put(d5, 12 + len(W.CODES), 1, "State", b=True)
    put(d5, 12 + len(W.CODES), 2, rc["published"], "#,##0", True)
    put(d5, 12 + len(W.CODES), 3, rc["now"], "#,##0", True)
    put(d5, 12 + len(W.CODES), 4, rc["now"] - rc["published"], "#,##0;-#,##0;0", True)
    put(d5, 14 + len(W.CODES), 1, "County figures also move where a worksite report for the quarter came in after May 31, 2026.")
    bs = G["base_silent"]
    put(d5, 15 + len(W.CODES), 1, "December 2025 as now on file is the reports on file. %d employers liable for that quarter have still "
                                   "filed no report for it; silent for five quarters, they are counted at nought (their last reports "
                                   "held %s jobs)." % (bs["n"], "{:,}".format(int(round(bs["jobs"], -1)))))
    d5.column_dimensions["A"].width = 78
    for col in "BCD":
        d5.column_dimensions[col].width = 15

    # ---- Replay
    rp = wb.create_sheet("Replay December 2025")
    rp["A1"] = "The same estimate made for December 2025 from the records as they stood on February 15, 2026"
    rp["A1"].font = Font(bold=True, size=12)
    R = G["replay"]
    header(rp, 3, ["County", "Estimate from the records of February 15, 2026", "As now on file", "Difference (%)"])
    for i, c in enumerate(W.CODES):
        put(rp, 4 + i, 1, W.NAMES[c])
        put(rp, 4 + i, 2, r10(R["total"][c]), "#,##0")
        put(rp, 4 + i, 3, r10(G["base"][c]), "#,##0")
        put(rp, 4 + i, 4, round(float(R["diff"][c]), 2), "0.00")
    n_ = 4 + len(W.CODES)
    put(rp, n_, 1, "State", b=True)
    put(rp, n_, 2, r100(R["state_total"]), "#,##0", True)
    put(rp, n_, 3, r100(G["base"].sum()), "#,##0", True)
    put(rp, n_, 4, round(R["state_diff"], 2), "0.00", True)
    put(rp, n_ + 2, 1, "Mean absolute difference over the counties: %.2f percent; the largest, %s, %.2f. Every share and count "
                       "in the replay is measured on what was on file that day (the resolved quarters were %s to %s)."
        % (R["mean_abs"], W.NAMES[R["max_county"]], R["max_abs"], W.quarter_label(R["mature"][0]), W.quarter_label(R["mature"][-1])))
    rp.column_dimensions["A"].width = 16
    for col in "BCD":
        rp.column_dimensions[col].width = 20
    rp.row_dimensions[3].height = 48

    # ---- What if
    sn = wb.create_sheet("Other treatments")
    sn["A1"] = "What the certification would say under other treatments of what is not yet on file"
    sn["A1"].font = Font(bold=True, size=12)
    header(sn, 3, ["Treatment", "State, December 2026 jobs", "State change (%)", "Counties at or below -2.0%"] + [W.NAMES[c] for c in W.CODES])
    rows = [dict(name="This certification", state_total=G["state_total"], state_change=G["state_change"],
                 designated=G["designated"], change=G["change"])] + G["routes"]
    for i, x in enumerate(rows):
        put(sn, 4 + i, 1, x["name"][0].upper() + x["name"][1:], b=i == 0).alignment = wrap
        put(sn, 4 + i, 2, r100(x["state_total"]), "#,##0")
        put(sn, 4 + i, 3, r1(x["state_change"]), "0.0")
        put(sn, 4 + i, 4, ", ".join(W.NAMES[c] for c in x["designated"]) or "none").alignment = wrap
        for k, c in enumerate(W.CODES):
            put(sn, 4 + i, 5 + k, r1(x["change"][c]), "0.0")
    sn.column_dimensions["A"].width = 70
    sn.column_dimensions["B"].width = 13
    sn.column_dimensions["C"].width = 9
    sn.column_dimensions["D"].width = 34
    for k in range(len(W.CODES)):
        sn.column_dimensions[openpyxl.utils.get_column_letter(5 + k)].width = 9
    sn.row_dimensions[3].height = 32
    sn.freeze_panes = "B4"
    wb.save(path)


# --------------------------------------------------------------------------------------------------------- the memo
def memo_story(G):
    from reportlab.platypus import Paragraph, Spacer
    import docs as D
    des = [W.NAMES[c] for c in G["designated"]]
    names = ", ".join(des[:-1]) + " and " + des[-1] if len(des) > 1 else (des[0] if des else "no county")
    rc, R, ui, tr = G["recon"], G["replay"], G["uinfo"], G["trouble"]
    ch = G["change"]
    near = sorted([c for c in W.CODES if c not in G["designated"]], key=lambda c: ch[c])[0]
    rows = [["County", "December 2025", "December 2026", "Change"]]
    for c in G["designated"] + [near]:
        rows.append([W.NAMES[c], "{:,}".format(r10(G["base"][c])), "{:,}".format(r10(G["total"][c])), "%.1f%%" % r1(ch[c])])
    st = [Paragraph("FRANKLIN DEPARTMENT OF LABOR, LABOR MARKET INFORMATION", D.SANSB),
          Paragraph("Memorandum", D.SANST),
          Paragraph("To: The Commissioner of Labor<br/>From: %s, %s<br/>Date: February 26, 2027<br/>Subject: Certification "
                    "for the 2027 Community Transition Fund" % W.PEOPLE["lmi_director"][:2], D.SANS),
          Spacer(1, 4),
          Paragraph("<b>Recommendation.</b> Certify %s as the counties whose covered jobs in December 2026 were 2.0 percent or "
                    "more below December 2025. No other county is within %.1f of a point of the line; %s, the nearest, is "
                    "at %.1f percent. The state as a whole is at %+.1f percent."
                    % (names, round(abs(r1(ch[near]) - W.THRESHOLD) - 0.1, 1), W.NAMES[near], r1(ch[near]), r1(G["state_change"])), D.SANS),
          D._table(rows, [1.6 * 72, 1.3 * 72, 1.3 * 72, 0.9 * 72]), Spacer(1, 6),
          Paragraph("<b>What the estimates rest on.</b> On February 15, %s of %s liable employers had reported. "
                    "Of the December jobs certified, %s are on those reports and %s are estimated."
                    % ("{:,}".format(G["census"]["received"]), "{:,}".format(G["census"]["liable"]),
                       "{:,}".format(r100(G["reported"].sum())), "{:,}".format(r100(G["estimated"].sum()))), D.SANS),
          Paragraph("1. A report that is out with a payroll agent's whole batch (%s employers; a batch is three or more "
                    "reports received in the same second) says nothing about the employer. A report that is out on its own "
                    "(%s employers), when the employer's usual batch arrived without it or it files singly, mostly means "
                    "trouble: at earlier cut-offs such employers kept %.2f of their September jobs once their cases "
                    "resolved, and we carry them at that."
                    % ("{:,}".format(G["kinds"]["batch"]["n"]), "{:,}".format(G["kinds"]["alone"]["n"]), G["k_alone"]), D.SANS),
          Paragraph("2. This quarter is not like the closed ones. Employers out on their own hold %.1f percent of "
                    "construction jobs, against under one percent at earlier fourth-quarter cut-offs, so construction "
                    "employers in late batches are carried at %.2f of September, not the %.2f their reporting peers show. "
                    "The replay below cannot test this step: December 2025 had no such quarter."
                    % (100 * tr[15]["constr"], G["kept_constr"], G["reporters"]["kept_constr"]), D.SANS),
          Paragraph("3. About %s employers liable for the quarter have no account yet. They add about %s jobs, counted from "
                    "this quarter's registrations so far and the delays of earlier years, at the %.1f jobs late registrants "
                    "have had." % ("{:,}".format(int(round(ui["n"], -1))), "{:,}".format(r100(G["unreg_jobs"])), ui["j_own"]), D.SANS),
          Paragraph("4. %d multi-county employers' worksite reports are still out. Each of their worksites is carried by its "
                    "own December-on-September change a year earlier; the latest reports' split would put about %d more "
                    "jobs in Kittredge and %d more in Talcott than their lake worksites hold in winter."
                    % (G["sites"]["carried"], int(round(G["latest_minus_site"]["013"], -1)), int(round(G["latest_minus_site"]["023"], -1))), D.SANS),
          Paragraph("<b>How far out it could be.</b> December 2025 as now on file is %s, %s above the published %s (late "
                    "reports %s, accounts set up since %s, amendments %s). The same estimate made for December 2025 from "
                    "the records of February 15, 2026 comes within %.2f percent of that for the state and %.2f percent for "
                    "the average county; the largest miss is %s at %.2f."
                    % ("{:,}".format(rc["now"]), "{:,}".format(rc["now"] - rc["published"]), "{:,}".format(rc["published"]),
                       "{:,}".format(rc["late_jobs"]), "{:,}".format(rc["new_jobs"]), "{:,}".format(rc["amend_jobs"]),
                       abs(R["state_diff"]), R["mean_abs"], W.NAMES[R["max_county"]], R["max_abs"]), D.SANS),
          Paragraph("The workbook has every county, the estimated jobs by kind, and what the certification would say under "
                    "other treatments; the employer list is in the CSV.", D.SANS)]
    return st


def write_memo(G, path):
    import datetime as dt
    import docs as D
    D._build(path, memo_story(G), "Certification for the 2027 Community Transition Fund", W.PEOPLE["lmi_director"][0],
             "Memorandum to the Commissioner of Labor", dt.datetime(2027, 2, 25, 10, 12, 0), dt.datetime(2027, 2, 26, 15, 47, 0),
             company="Franklin Department of Labor")


def build(pack_dir, out_dir, bands=True, quiet=True):
    pk = load_pack(pack_dir)
    published = read_published(os.path.join(pack_dir, W.FILES["published"]))
    G = compute(pk, published, bands=bands, quiet=quiet)
    write_certification(pk, G, os.path.join(out_dir, W.DELIVERABLES["cert"]))
    G["n_rows"] = write_employers(pk, G, os.path.join(out_dir, W.DELIVERABLES["employers"]))
    write_memo(G, os.path.join(out_dir, W.DELIVERABLES["memo"]))
    return pk, G
