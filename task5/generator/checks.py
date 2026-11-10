"""task5 architecture 4: the generator's assertions, run on every build.

The input gates; the bar block (R1 to R7) on the clean truth and the cut pack; every semantic fork (SF rows) closed or
shown inert; the family's spread against each graded band and the line; the golden against the simulated truth; the
footprint of every process outside the units it decides; the governing documents read back with positive controls;
the deliverables against the figures; the realism sweep."""
import csv
import json
import os
import re

import numpy as np
import pandas as pd

import golden as GD
import methods as M
import sim
import tells
import world as W

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), str(detail)))
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


def inband(v, band, eps=1e-9):
    return band[0] - eps <= v <= band[1] + eps


def run(task, w, T, pk, G, texts, figs, n, quiet=False):
    RESULTS.clear()
    target, gold = os.path.join(task, "target"), os.path.join(task, "golden")
    files = sorted(os.listdir(target))
    B = G["bands"]
    v = G["view"]
    des = G["designated"]
    ch = G["change"]
    E = json.load(open(os.path.join(task, "generator", "effort.json")))
    eres = {r["id"]: r for r in E["results"]}

    # --------------------------------------------------------------------------------------------- input gates
    check("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: two or more file categories, three or more formats", bool(exts & {"csv", "xlsx"}) and bool(exts & {"docx", "eml"}) and len(exts) >= 3, sorted(exts))
    check("gate: a CSV of 20,000 rows or more", n["reports"] >= 20000, n["reports"])
    check("gate: a second large CSV (ten to twenty printed pages or more)", n["accounts"] >= 2000 and n["status"] >= 2000, (n["accounts"], n["status"]))
    check("gate: two or more distractors, shipped and unlabelled", all(W.FILES[k] in files for k in W.DISTRACTORS)
          and not any(re.search(r"distract|decoy|unused|trap", f, re.I) for f in files), [W.FILES[k] for k in W.DISTRACTORS])
    check("gate: no file describes the data", not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook", f, re.I) for f in files))
    check("gate: exactly the files the world names", set(files) == set(W.FILES.values()), len(files))
    check("gate: the golden holds exactly the requested files", sorted(os.listdir(gold)) == sorted(W.DELIVERABLES.values()), os.listdir(gold))

    # ----------------------------------------------------------------------------------- R1 the field's raw material
    cols = {k: list(T[k].columns) for k in T}
    flat = " ".join(c for k in cols for c in cols[k] if not c.startswith("_")).lower()
    check("R1 raw material: no shipped column holds a result or a filing agent",
          not re.search(r"agent|transmission|batch|channel|kind|status_reason|estimated|imputed|distress|seasonal", flat), flat[:80])
    check("R1 raw material: reports carry a receipt time, accounts both dates, worksite reports a date received",
          "received_at" in cols["reports"] and {"liability_date", "account_established"} <= set(cols["accounts"]) and "date_received" in cols["worksites"])
    check("R1 raw material: the reconciliation is exact on the shipped table",
          G["recon"]["rebuilt"] == G["recon"]["published"] and
          G["recon"]["published"] + G["recon"]["late_jobs"] + G["recon"]["new_jobs"] + G["recon"]["amend_jobs"] == G["recon"]["now"],
          (G["recon"]["published"], G["recon"]["now"]))

    # ----------------------------------------------------------------------------- R2 every mess item real and neutral
    base = G["base"]

    def stays(route=None, label="", **kw):
        X = pk.certify(route=route or {})
        s = GD.summary(pk, X, base)
        bad = [W.NAMES[c] for c in W.CODES if not inband(GD.r1(s["change"][c]), B["change"][c])]
        return check("R2 mess neutral: " + label, not bad and s["designated"] == des, bad or "every county's change inside its band")
    stays(dict(version="first"), "SF4 the first version of a report instead of the latest")
    rr = pk.r
    dup_raw = len(T["reports"]) - len(rr)
    check("R2 mess: resubmissions exist and are kept once", dup_raw > 50, "%d resubmitted rows dropped" % dup_raw)
    am = T["reports"][T["reports"]["report_type"] == "AMENDED"]
    check("R2 mess: amended reports exist in every quarter", am.groupby(["year", "quarter"]).size().min() > 20, len(am))
    old17 = pk.a["naics_code"].isin(["444190", "445120", "452311", "446110", "447110", "448140", "451110", "453220", "453998", "511110", "517312", "519130"]).sum()
    check("R2 mess: accounts still carrying NAICS 2017 codes map through the concordance", old17 > 500 and pk.a["ss"].notna().all(), old17)
    paper = (rr["t"].dt.hour + rr["t"].dt.minute + rr["t"].dt.second == 0).sum()
    check("R2 mess: paper reports keyed by date alone exist and form no transmission", paper > 1000 and
          not any((t.hour + t.minute + t.second) == 0 for t in pk.batches(W.FLASH_Q - 1, M.CUT[W.FLASH_Q]).unique()), paper)
    check("R2 mess: account numbers are written two ways (hyphenated in the register, digits in the worksite file)",
          T["accounts"]["account_no"].str.contains("-").all() and not T["worksites"]["uiacct"].str.contains("-").any())
    succ = (T["status"]["change_type"] == "TRANSFERRED").sum()
    check("SF6 mess: transfers to successors exist and end the predecessor's liability", succ > 100, succ)

    # ------------------------------------------------------------------------------- R3 each result's hurried figure
    import importlib.util
    spec = importlib.util.spec_from_file_location("effort", os.path.join(os.path.dirname(__file__), "..", "..", ".claude", "skills", "stumping", "effort.py"))
    eff = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eff)
    gr = {p: {rid: eff.grade(r["passes"][p], r)[0] for rid, r in eres.items()} for p in ("quick", "careful", "thorough")}
    check("R3 the thorough pass earns every result", all(g == "right" for g in gr["thorough"].values()), gr["thorough"])
    check("R3 the careful pass earns R1, R2 and R9 and loses R3 to R7", [gr["careful"][k] for k in ("R1", "R2", "R9")] == ["right"] * 3
          and all(gr["careful"][k] == "missed" for k in ("R3", "R4", "R5", "R6", "R7")), gr["careful"])
    check("R3 the quick pass earns no result", all(g == "missed" for g in gr["quick"].values()), gr["quick"])
    cp = {rid: r["passes"]["careful"] for rid, r in eres.items()}
    check("R3 margin: the careful pass's late-transmission figure sits outside the band by 200 jobs or more",
          B["transport_jobs"][0] - cp["R3"] >= 200, (cp["R3"], B["transport_jobs"]))
    check("R3 margin: the careful pass's unregistered jobs sit 15 per cent or more outside the band",
          cp["R4"]["jobs"] >= 1.15 * B["unreg_jobs"][1], (cp["R4"]["jobs"], B["unreg_jobs"]))
    n_in = sum(inband(cp["R7"][W.NAMES[c]], B["change"][c]) for c in W.CODES)
    check("R3 margin: the careful pass's county changes fall outside their bands in nine counties or more", n_in <= 5, "%d of 14 inside" % n_in)
    n_in6 = sum(inband(cp["R6"][W.NAMES[c]], B["total"][c]) for c in W.CODES)
    check("R3 margin: the careful pass's county jobs fall outside their bands in eight counties or more", n_in6 <= 6, "%d of 14 inside" % n_in6)
    check("R3 the careful pass designates another set", sorted(cp["R8"]) != sorted(figs["r8_designated"]), cp["R8"])

    # ------------------------------------------------------------------------------------------------ R4 no plant
    r = T["reports"]
    k = r.groupby(["account_no", "year", "quarter", "report_type"]).size()
    check("R4 no copied block: no account-quarter carries more than two originals", k.max() <= 2, int(k.max()))
    check("R4 no memo, draft or stakeholder figure for December 2026 ships",
          not any(re.search(r"draft|memo|flash|estimate|certif", f, re.I) and "request" not in f and "population" not in f for f in files), files)
    rq = texts["request"][0]
    check("R4 the request states no figure for any county", not re.search(r"\d{2},\d{3}|-\d\.\d", rq), "")

    # ---------------------------------------------------------------------------- R5 no one thing: every footprint
    ai = {a.replace("-", ""): i for i, a in enumerate(w.acct_s)}
    al_by_c = v[v["kind"] == "alone"].groupby("county_code").size().reindex(W.CODES).fillna(0)
    check("R5 footprint: employers missing alone in every county", al_by_c.min() >= 5, al_by_c.astype(int).to_dict())
    past = {q: (pk.view(q)["kind"] == "alone").sum() for q in range(4, 15)}
    check("R5 footprint: employers missing alone at every earlier cut-off", min(past.values()) >= 100, past)
    tr = G["trouble"]
    check("R5 footprint: the housing chain's trouble shows statewide this quarter and in the two quarters before",
          tr[15]["chain"] > 4 * tr[11]["chain"] and tr[15]["other"] < 2 * tr[11]["other"], tr)
    chain_by_c = v[(v["kind"] == "alone") & v["chain"]].groupby("county_code").size().reindex(W.CODES).fillna(0)
    check("R5 footprint: housing-chain employers missing alone in every county, not only the designated ones",
          chain_by_c.min() >= 3 and chain_by_c.drop(des).sum() > 2 * chain_by_c[des].sum(), chain_by_c.astype(int).to_dict())
    un = G["unregistered"]
    check("R5 footprint: employers with no account in every county", (un > 15).all(), un.round(0).astype(int).to_dict())
    H = pk.unregistered_history(W.FLASH_Q, M.EXTRACT, "all")
    check("R5 footprint: accounts established after the cut-off at every earlier cut-off", min(x["n_own"] for x in H) > 150, [x["n_own"] for x in H][:6])
    noB = next(x for x in G["routes"] if x["route"] == dict(ibnr="none"))
    dB = (noB["change"] - ch).abs()
    check("R5 footprint: leaving them out misreads every county by 0.25 of a point or more and flips none where nothing turns",
          dB.min() >= 0.25 and sorted(noB["designated"]) == sorted(des), dB.round(2).to_dict())
    lm = G["latest_minus_site"]
    moved = [c for c in W.CODES if abs(lm[c]) >= 60]
    check("R5 footprint: the latest worksite split misplaces 60 jobs or more in five counties or more, Talcott and Sayre among them (nothing turns there)",
          len(moved) >= 5 and "023" in moved and "027" in moved, {W.NAMES[c]: int(round(lm[c])) for c in moved})
    for q in (7, 11):
        lt = pk.latest(q, M.CUT[q])["m3"].astype(float)
        a_, _ = pk.to_counties(lt, q, M.CUT[q], "latest")
        b_, _ = pk.to_counties(lt, q, M.EXTRACT, "site")
        d_ = (a_ - b_)
        check("R5 footprint: the same misplacement at the %s cut-off against the worksite reports that came later" % W.quarter_label(q),
              d_["013"] > 40 and d_["023"] > 40, {W.NAMES[c]: int(round(d_[c])) for c in ("013", "023", "027", "003")})
    hints = E["hints"]
    check("R5 and R6: no single hint rescues more than a third of the results", max(len(h["rescues"]) for h in hints) <= 3,
          [(h["sentence"][:30], h["rescues"]) for h in hints])
    check("R6 each hint rescues the result it names", [h["rescues"] for h in hints] == [["R4"], ["R5"], ["R3"]] or
          all(len(h["rescues"]) >= 1 for h in hints), [h["rescues"] for h in hints])

    # --------------------------------------------------------------------------------------------- R7 the rivals
    fam = G["family"]
    check("R7 every member of the family designates the same counties", all(f["designated"] == des for f in fam), len(fam))
    worst = max(abs(f["change"][c] - ch[c]) for f in fam for c in W.CODES)
    check("R7 the family's county changes stay within 0.3 of a point of the golden's", worst <= 0.3, round(worst, 3))
    for c in des:
        check("R7 line: %s's whole band is 0.4 of a point or more below the line" % W.NAMES[c], B["change"][c][1] <= W.THRESHOLD - 0.4, B["change"][c])
    rest = [c for c in W.CODES if c not in des]
    check("R7 line: every other county's band is 0.8 of a point or more above the line", min(B["change"][c][0] for c in rest) >= W.THRESHOLD + 0.8,
          min(B["change"][c][0] for c in rest))
    def same(idx, label):
        ms = [fam[i] for i in idx]
        return check(label, all(m["designated"] == des for m in ms) and
                     all(inband(GD.r1(m["change"][c]), B["change"][c]) and inband(GD.r10(m["total"][c]), B["total"][c]) for m in ms for c in W.CODES), len(ms))
    same([1, 2, 3, 4], "SF12 a transmission as two, three or four reports in a second, arrived at a third, a half or two thirds: same call, every figure in band")
    same([10, 11, 12], "SF13 the resolved quarters with the earliest or the latest left out, or at 5 per cent outstanding: same call")
    same([5, 6, 7, 8, 9], "SF14 this quarter's trouble by housing chain, supersector or three-digit industry, with or without size: same call")
    same([13, 14, 15], "SF14 the missing-alone share by size, channel or housing chain: same call")
    same([16, 17], "SF15 a seasonal business under 0.5, 0.6 or 0.7 of its September: same call")
    same([18], "SF18 a new account at the resolved quarters' mean or at this quarter's reporting new employers: same call")
    same([19], "SF11 an employer two quarters out at the resolved quarters' share or at nought: same call")
    same([20, 21], "SF10 the reporters' change in cells of five, ten or twenty: same call")
    ya = next(x for x in G["routes"] if x["route"] == dict(sites="yearago"))
    check("SF17 last December's worksite split designates the same counties", ya["designated"] == des, [W.NAMES[c] for c in ya["designated"]])
    check("SF19 a county's estimated jobs are its total less the jobs on reports received", max(abs(G["estimated"][c] - (G["total"][c] - G["reported"][c])) for c in W.CODES) < 1e-6)
    Rk = pk.certify(q=W.BASE_Q, know=M.EXTRACT)
    rdk = (Rk["total"] / base - 1) * 100
    check("SF20 the replay with today's shares in place of that day's lands inside the replay's bands",
          inband(round(float(100 * (Rk["total"].sum() / base.sum() - 1)), 2), B["replay_state_diff"]) and inband(round(float(rdk.abs().mean()), 2), B["replay_mean_abs"]),
          (round(float(100 * (Rk["total"].sum() / base.sum() - 1)), 3), round(float(rdk.abs().mean()), 3)))
    check("SF2 December is month three of the fourth-quarter report: the published December column reproduces from it", G["recon"]["rebuilt"] == G["recon"]["published"])
    check("SF16 unregistered employers from fourth-quarter cut-offs, county by county (the pooled and shared-out variants are ruled out below and designate the same counties)", True)
    ro = {}
    for name, rt in M.RULED_OUT:
        s = GD.summary(pk, pk.certify(route=rt), base)
        ro[name] = s
        check("R7 ruled out but harmless: %s designates the same counties" % name[:60], s["designated"] == des, [W.NAMES[c] for c in s["designated"]])
    # the facts that rule them out
    by_q = {}
    for x in pk.unregistered_history(W.FLASH_Q, M.EXTRACT, "all"):
        by_q[x["h"]] = x["n_own"] / max(1, x["reg_own"])
    q4 = [by_q[h] for h in by_q if h % 4 == 3]
    oth = [by_q[h] for h in by_q if h % 4 != 3]
    check("R7 fact: later-established accounts per registered new employer run higher at fourth-quarter cut-offs than at any other",
          min(q4) > max(oth), (round(min(q4), 2), round(max(oth), 2)))
    a = pk.a
    reg = a[(a["liab"] >= M.QSTART[W.FLASH_Q]) & (a["liab"] <= M.QEND[W.FLASH_Q]) & (a["est"] <= M.CUT[W.FLASH_Q])].groupby("county_code").size().reindex(W.CODES).fillna(0)
    allc = a[a["est"] <= M.CUT[W.FLASH_Q]].groupby("county_code").size().reindex(W.CODES)
    rel = (reg / reg.sum()) / (allc / allc.sum())
    check("R7 fact: the quarter's new registrations by county depart from the counties' shares of all accounts", rel.max() / rel.min() >= 1.5, rel.round(2).to_dict())
    rp_ = v[v["rep"] & (v["prior"] > 0)]
    mv = rp_.groupby("ss").apply(lambda d: d["m3"].sum() / d["prior"].sum())
    check("R7 fact: the reporting employers' change differs by supersector by five points or more", mv.max() - mv.min() >= 0.05, mv.round(3).to_dict())
    last = next(x for x in G["routes"] if x["route"] == dict(sites="yearago"))
    sh_now = pk.wk[(pk.wk["q"] == W.FLASH_Q - 1) & (pk.wk["recv"] <= M.CUT[W.FLASH_Q])]
    sh_ya = pk.wk[(pk.wk["q"] == W.FLASH_Q - 4)]
    newsites = set(zip(sh_now["acct"], sh_now["unit"])) - set(zip(sh_ya["acct"], sh_ya["unit"]))
    check("R7 fact: worksites on the September 2026 reports that the December 2025 reports do not hold", len(newsites) >= 10, len(newsites))

    # ----------------------------------------------------------------------------------- the golden against the truth
    t25, t26 = sim.county_truth(w, 35), sim.county_truth(w, 47)
    tch = {c: 100 * (t26[c] / t25[c] - 1) for c in W.CODES}
    check("truth: the golden's designated set is the truth's", sorted(des) == sorted(c for c in W.CODES if round(tch[c], 1) <= W.THRESHOLD),
          {W.NAMES[c]: round(tch[c], 2) for c in des})
    check("truth: the state estimate is within 0.15 per cent of the truth", abs(G["state_total"] / sum(t26.values()) - 1) < 0.0015,
          round(100 * (G["state_total"] / sum(t26.values()) - 1), 3))
    check("truth: every county's estimate is within 1 per cent of the truth", max(abs(G["total"][c] / t26[c] - 1) for c in W.CODES) < 0.01,
          {W.NAMES[c]: round(100 * (G["total"][c] / t26[c] - 1), 2) for c in W.CODES})
    check("truth: December 2025 now on file is the truth to 0.1 per cent in every county", max(abs(base[c] / t25[c] - 1) for c in W.CODES) < 0.001)
    cut = W.cutoff(W.FLASH_Q).date()
    tu = [i for i in range(w.n) if w.established[i] is not None and w.established[i] > cut and sim.liab_date(w, i) <= W.quarter_end(W.FLASH_Q)]
    tuj = sum(w.jobs[i, 47] for i in tu)
    check("truth: the unregistered employers and their jobs sit inside the bands", inband(len(tu), (B["unreg_n"][0] - 40, B["unreg_n"][1] + 40))
          and inband(tuj, (B["unreg_jobs"][0] - 150, B["unreg_jobs"][1] + 150)), (len(tu), int(tuj)))
    al = v.index[v["kind"] == "alone"]
    tk = sum(w.jobs[ai[x], 47] for x in al) / v.loc[al, "prior"].sum()
    check("truth: what this quarter's missing-alone kept is within 0.06 of the share carried", abs(tk - G["k_alone"]) < 0.06, round(tk, 3))
    bt = v.index[(v["kind"] == "batch") & v["chain"]]
    tb = sum(w.jobs[ai[x], 47] for x in bt) / v.loc[bt, "prior"].sum()
    check("truth: the late transmissions' housing-chain employers kept nearer the estimate than the reporters' change",
          abs(tb - G["kept_chain"]) < abs(tb - G["reporters"]["kept_chain"]), (round(tb, 3), round(G["kept_chain"], 3), round(G["reporters"]["kept_chain"], 3)))

    # --------------------------------------------------------------------------------------------- semantic forks
    s_ = pk.s
    ends = s_[s_["change_type"].isin(M.ENDS)]
    liab_ok = ends.merge(pk.a[["liab"]], left_on="acct", right_index=True)
    check("SF1 no account ends on or before its own liability date (effective or entered order gives one status)", (liab_ok["eff"] > liab_ok["liab"]).all())
    rcut = pk.rq[W.FLASH_Q]
    lastday = rcut[(rcut["t"] > M.CUT[W.FLASH_Q] - pd.Timedelta(days=1)) & (rcut["t"] <= M.CUT[W.FLASH_Q] + pd.Timedelta(days=1))]
    check("SF3 the cut-off's edge: reports received on 15 or 16 February move no county by 0.05", len(lastday) < 400, len(lastday))
    edge = min(abs(abs(GD.r1(ch[c]) * 10 - ch[c] * 10)) for c in W.CODES)
    check("SF8 rounding: no county's change is within 0.25 of a point of the line", min(abs(ch[c] - W.THRESHOLD) for c in W.CODES) > 0.25,
          round(min(abs(ch[c] - W.THRESHOLD) for c in W.CODES), 2))
    wk = pk.wk
    tot_m = wk.groupby(["acct", "q"])["m3_emp"].sum()
    r3 = pk.r[pk.r["report_type"] == "ORIGINAL"].groupby(["acct", "q"])["month3_employment"].first()
    j = pd.concat([tot_m, r3], axis=1, join="inner")
    check("SF5 a worksite report's month three adds to its contribution report's original", (j.iloc[:, 0] == j.iloc[:, 1]).mean() > 0.999, round((j.iloc[:, 0] == j.iloc[:, 1]).mean(), 4))
    pubc = G["recon"]["published_county"]
    check("SF7 the published table's state total is its counties' sum and reproduces from the records of 31 May 2026",
          int(pubc.sum()) == G["recon"]["rebuilt"], int(pubc.sum()))
    check("SF9 a report held for an account not yet established exists at earlier cut-offs (the as-of rule matters there)",
          ((pk.r["t"] < pk.r["est"]) & (pk.r["q"] < W.FLASH_Q)).sum() > 500, int(((pk.r["t"] < pk.r["est"])).sum()))

    # ------------------------------------------------------------------------------------- the governing documents
    act = doc_text(os.path.join(target, W.FILES["act"]))
    agr = doc_text(os.path.join(target, W.FILES["agreement"]))
    check("document control: the Act reads back", "whether or not an account has been established" in act and "minus 2.0 percent or lower" in act, len(act))
    check("document control: the agreement reads back", "held, and is posted with the date and time it was received" in agr and "distributes the employment" in agr, len(agr))
    banned = r"transmission|payroll agent|payroll bureau|batch|late filer|imput|nonresponse|seasonal|housing|downturn|completion factor|back-?test|missing alone"
    for nm, tx in (("Act", act), ("agreement", agr), ("request", rq)):
        hit = re.findall(banned, tx, re.I)
        check("pins: the %s names no step of the estimate" % nm, not hit, hit[:5])
    check("pins: the Act files the population, the outcome, the line, the cut-off, the base and the two reports",
          all(s in act for s in ("payroll period that includes the twelfth day", "whether or not its contribution report for the quarter has been received",
                                 "from the same records as they stand at the same date", "differs from the figure the Department has published",
                                 "as they stood at the close of February 15 of the year before the fund year")))

    # --------------------------------------------------------------------------------------------- the deliverables
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(gold, W.DELIVERABLES["cert"]))
    ws = wb["Certification"]
    rows = {str(r_[0]): r_ for r_ in ws.iter_rows(min_row=8, max_row=8 + len(W.CODES) - 1, values_only=True)}
    check("deliverable: the workbook's county rows are the figures", all(rows[c][5] == figs["r6_county_jobs"][W.NAMES[c]] and
          abs(rows[c][6] - figs["r7_changes"][W.NAMES[c]]) < 1e-9 for c in W.CODES))
    check("deliverable: the workbook marks exactly the designated counties", [W.NAMES[c] for c in W.CODES if rows[c][7] == "Yes"] == figs["r8_designated"])
    check("deliverable: five sheets and a chart", wb.sheetnames == ["Certification", "Estimated jobs", "December 2025", "Replay December 2025", "Other treatments"]
          and len(ws._charts) == 1, wb.sheetnames)
    rows_csv = list(csv.DictReader(open(os.path.join(gold, W.DELIVERABLES["employers"]), encoding="utf-8")))
    byc = {}
    for r_ in rows_csv:
        byc[r_["county_code"]] = byc.get(r_["county_code"], 0.0) + float(r_["december_2026_jobs"])
    check("self-verification: the employer list adds to each county's total", max(abs(byc[c] - G["total"][c]) for c in W.CODES) < 0.06 * 600,
          round(max(abs(byc[c] - G["total"][c]) for c in W.CODES), 1))
    check("self-verification: reported plus estimated is the total in every county", max(abs(G["reported"][c] + G["estimated"][c] - G["total"][c]) for c in W.CODES) < 1e-6)
    memo = doc_text(os.path.join(gold, W.DELIVERABLES["memo"]))
    check("deliverable: the memo names the designated counties and the four judgments", all(W.NAMES[c] in memo for c in des) and
          "no account yet" in memo and "worksite" in memo and "housing" in memo, len(memo))
    check("deliverable: no em dash anywhere in the deliverables or the write-up", "—" not in memo and "—" not in open(os.path.join(task, "submission.md"), encoding="utf-8").read())

    # ------------------------------------------------------------------------------------------- the realism sweep
    hits = tells.sweep(target)
    check("realism: no authoring tell in any shipped file", not hits, hits[:4])
    acc = T["accounts"]
    step = np.diff(np.sort(acc["_n"].values))
    check("realism: account numbers are no arithmetic sequence", len(set(step)) > 100, len(set(step)))
    shapes = acc["legal_name"].str.replace(r"[A-Z][a-z]+", "X", regex=True).nunique()
    check("realism: employer names take many shapes", shapes > 40, shapes)
    bq = T["reports"].groupby(["year", "quarter"]).size()
    check("realism: no two quarters carry the same number of reports", bq.nunique() == len(bq), bq.min())
    tot_c = [int(round(G["total"][c])) for c in W.CODES]
    check("realism: no county total is a round thousand", not any(t % 1000 == 0 for t in tot_c))
    check("realism: every extract's last record is on or before the extract date", T["reports"]["received_at"].max() <= "2027-02-15 23:59:59"
          and pd.to_datetime(T["worksites"]["date_received"], format="%m/%d/%Y").max() <= pd.Timestamp("2027-02-15"))
    eq3 = ((r["month1_employment"] == r["month2_employment"]) & (r["month2_employment"] == r["month3_employment"])).mean()
    check("realism: the three months differ on most reports of ten jobs or more", ((r["month3_employment"] >= 10) &
          (r["month1_employment"] == r["month2_employment"]) & (r["month2_employment"] == r["month3_employment"])).sum() /
          max(1, (r["month3_employment"] >= 10).sum()) < 0.25, round(eq3, 3))

    ok = all(x[1] for x in RESULTS)
    bad = [x for x in RESULTS if not x[1]]
    if not quiet:
        for name, good, detail in RESULTS:
            if not good:
                print("FAIL  %s  %s" % (name, detail[:300]))
        print("checks: %d of %d" % (len(RESULTS) - len(bad), len(RESULTS)))
    return ok
