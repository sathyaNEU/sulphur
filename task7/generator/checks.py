"""The generator's assertions on the cut pack (dataset-generation 7.1 and 11, determinism-check 4): the pack against
core.py, the bar block R1 to R7, every row of the note's semantic fork table, the pinning list, the forcing
perturbations, the face-value records, the input gates and the realism sweep.

    python3 task7/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402
import common as CM  # noqa: E402
import core as C  # noqa: E402
import params as P  # noqa: E402
import read as R  # noqa: E402
import world  # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
OUT = []


def check(label, ok, detail=""):
    OUT.append((label, bool(ok), detail))


def text_of(path):
    """A shipped document's text through one extractor per format (the verifier reads it the same way)."""
    if path.endswith(".pdf"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    if path.endswith(".docx"):
        from docx import Document
        d = Document(path)
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts += [c.text for c in row.cells]
        return "\n".join(parts)
    return open(path, encoding="utf-8").read()


def inside(v, b):
    return b[0] <= v <= b[1]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    B = F["bands_raw"]
    KEYS = list(B)
    wd, ex = R.read(T)
    ln, cnt = C.lines(wd)
    gm = C.model(wd)
    gold = C.all_figures(wd, gm, ln)
    W = world.build()
    cw = W["core"]
    # ---- the pack against core.py ----
    kp = {(round(a, 3), round(b, 3)): i for i, (a, b) in enumerate(zip(wd["x"], wd["y"]))}
    mp = np.array([kp[(round(a, 3), round(b, 3))] for a, b in zip(cw["x"], cw["y"])])
    check("C01 the register holds core's switches", len(mp) == wd["n_s"] == cw["n_s"], "%d switches" % wd["n_s"])
    check("C02 the replaced-unit list is core's flag, switch by switch", np.array_equal(wd["flag"][mp], cw["flag"]),
          "%d flagged" % int(wd["flag"].sum()))
    check("C03 paging groups and install years are core's", np.array_equal(wd["grp"][mp], cw["grp"]) and np.array_equal(wd["yr"][mp], cw["yr"]))
    check("C04 every switch's reach band on every event day and in 2027 is core's",
          np.array_equal(np.digitize(wd["reach"][:, mp], C.RB), np.digitize(cw["reach"], C.RB))
          and np.array_equal(np.digitize(wd["now"][mp], C.RB), np.digitize(cw["now"], C.RB)))
    codes, _ = CM.feeder_codes(cw["dist"])
    perm = np.array([sorted(codes).index(c) for c in codes])
    ce, cg, cf = cw["obs"]
    pe, pg, pf = wd["obs"]
    key_p = {(int(a), int(b), int(c)): i for i, (a, b, c) in enumerate(zip(pe, pg, pf))}
    idx = np.array([key_p[(int(a), int(b), int(perm[c]))] for a, b, c in zip(ce, cg, cf)])
    worst = 0.0
    for a_ in C.WINDOWS:
        for b_ in C.WINDOWS:
            w2 = R.steps_for_window(wd, ex, a_, b_)
            worst = max(worst, float(np.abs(w2["step"][idx] - cw["step_win"][(a_, b_)]).max()))
    check("C05 every step on every window (3 to 10 minutes each side) is core's to rounding", worst < 0.15, "%.3f kW" % worst)
    st, stc = C.study(wd), C.study(cw)
    check("C06 the study homes' figures are core's", all(abs(st[k] - stc[k]) < 2e-3 for k in st),
          "working %.4f against %.4f" % (st["working"], stc["working"]))
    cgold = C.all_figures(cw, C.model(dict(cw, wx=cw["w"])), C.lines(cw)[0])
    rel = max(abs(gold[k] - cgold[k]) / max(abs(cgold[k]), 1e-9) for k in C.MEMBERS)
    check("C07 every golden member figure is core's to 0.5 per cent", rel < 0.005, "largest %.2f per cent" % (100 * rel))
    frozen = {"c1_fringe_loss": (0.777, 0.905), "c2_failed_old": (0.302, 0.372), "c3_unwired": (0.628, 0.733),
              "rep_w": (230.7, 262.1), "rep_n": (149.5, 207.4), "fix_t": (451.4, 572.0), "fix_w": (207.5, 324.3),
              "recon_in": (1252, 1552), "recon_out": (195.2, 253.1), "lost_reach": (1527, 2018), "lost_hw": (2056, 2824),
              "lost_unwired": (1451, 1787), "plan_kw": (2045, 2285), "plan_cost_per_kw": (37.43, 41.81)}
    import effort_passes as EP
    for k_, (lo_, hi_) in EP.AUDIT_BANDS.items():
        frozen[k_] = (min(frozen[k_][0], lo_), max(frozen[k_][1], hi_))
    bad = [k for k, (lo, hi) in frozen.items() if abs(B[k][0] - lo) > 0.006 * abs(lo) + 0.002 or abs(B[k][1] - hi) > 0.006 * abs(hi) + 0.002]
    check("C08 the bands are the architect's frozen bands (78 rebuilds), widened only where the stage 4 judge's rivals "
          "reach past them", not bad and F["counts"]["variants"] == 78, ", ".join(bad))
    for k_, (lo_, hi_) in EP.AUDIT_BANDS.items():
        s_own = {"c2_failed_old": "S2", "c3_unwired": "S3", "fix_t": "S2", "lost_reach": "S1", "lost_hw": "S2"}.get(k_)
        if s_own:
            v_ = C.all_figures(wd, C.hurried(gm, (s_own,)), ln)[k_]
            check("C08 with %s lost alone, %s stays outside its widened band" % (s_own, k_), not inside(v_, B[k_]), "%.3f" % v_)
    check("C09 the golden funds the repeater, the Larkin round and the reconnection round within 14 km",
          AN.funded(gold, ln) == ["rep_w", "fix_t", "recon_in"])
    # ---- R1: the field's raw material ships, no column holds a result ----
    reg_cols = open(os.path.join(T, CM.FILES["register"])).readline().strip().split(",")
    check("R1 the register carries no switch condition, signal, last-heard or delivery field",
          not any(re.search(r"deliver|work|signal|heard|condition|fail|wired|reach|kw", c, re.I) for c in reg_cols), ",".join(reg_cols))
    check("R1 the SCADA export carries time, point and kW only",
          open(os.path.join(T, CM.FILES["scada"])).readline().strip() == "utc_time,point,kw")
    check("R1 the golden reads the minute data and the members' records (21,896 steps from 1.2 million minutes)",
          len(wd["step"]) == 21896 and F["counts"]["steps"] == 21896)
    # ---- R2: each piece of mess, mishandled the way a careful run could, leaves every graded figure in band ----
    GRADED = [k for k in KEYS if k != "delivered"]       # the delivered total is stated in the Step-by-Step only

    def in_band_all(f):
        return [k for k in GRADED if k in f and not inside(f[k], B[k])]
    for lab, kw in (("held readings kept", dict(hold=False)), ("old premise numbers mapped only before the conversion", dict(old_numbers="before")),
                    ("permit addresses cleaned without dropping periods and doubled spaces", dict(normalise="partial"))):
        C._TENSORS.clear()
        w2, _ = R.read(T, **kw)
        l2, _ = C.lines(w2)
        f2 = C.all_figures(w2, C.model(w2), l2)
        out = in_band_all(f2)
        check("R2 %s: the call holds and no graded figure leaves its band" % lab, not out and AN.funded(f2, l2) == AN.funded(gold, ln),
              ", ".join(out))
    C._TENSORS.clear()
    w2, _ = R.read(T, renamed=False)
    keep = ~np.isnan(w2["step"])
    w2["step"] = np.nan_to_num(w2["step"])
    f2 = C.all_figures(w2, C.model(w2, keep=keep), C.lines(w2)[0])
    check("R2 the renamed Pruett points left unmapped (steps lost): the call holds, every figure in band",
          not in_band_all(f2) and AN.funded(f2, ln) == AN.funded(gold, ln), "%d steps lost" % int((~keep).sum()))
    C._TENSORS.clear()
    tr = {(t[0], t[1]) for t in [(r_["from_feeder"], r_["transferred"][:10]) for r_ in R.rows(os.path.join(T, CM.FILES["switching"]))]}
    ev = {d.strftime("%m/%d/%Y") for d in ex["days"]}
    check("R2 the switching log touches no event afternoon (feeder membership as operated is the register's on every event day)",
          not any(d_ in ev for _, d_ in tr), "%d transfers" % len(tr))
    # ---- R3: each result's hurried figure sits outside its band ----
    L = F["lattice"]
    check("R3 the coverage map read as it stands: all commands get through, outside 1 (band %d to %d)" % tuple(F["c1_through_band"]),
          not inside(L["S1"]["c1_through"], F["c1_through_band"]))
    check("R3 the test log read as it stands: 96 in 100 work, outside 2", not inside(L["S2"]["c2_work"], F["c2_work_band"]))
    check("R3 the work orders read as they stand: 91 in 100 wired, outside 3", not inside(L["S3"]["c3_wired"], F["c3_wired_band"]))
    for m in ("rep_w", "fix_t", "recon_in"):
        s_ = {"rep_w": "S1", "fix_t": "S2", "recon_in": "S3"}[m]
        check("R3 %s with its stump read at face value is across its line" % m, (L[s_][m] >= ln[m]) != (gold[m] >= ln[m]),
              "%s kW against %.1f" % (L[s_][m], ln[m]))
    check("R3 the reflex route funds none of the six", F["routes"]["reflex"]["funded"] == [])
    # ---- R4: no plant ----
    days = ex["days"]
    blocks = {}
    dup = 0
    for (fc, d), (v, h) in ex["series"].items():
        k_ = tuple(np.round(v[60:120], 1))
        dup += k_ in blocks
        blocks[k_] = 1
    check("R4 no feeder afternoon repeats another's readings (no copied block)", dup == 0)
    # ---- R5: every factor runs across the data, outside the deciding units ----
    far_other = int(((wd["now"] > 20) & (wd["dist"][wd["sf"]] != 1)).sum())
    check("R5 fringe switches outside the Kettle Ridge proposal's district (the reach loss runs fleet-wide)", far_other > 50, "%d" % far_other)
    h_new = np.array(F["fit"]["h"])[10:]
    check("R5 the batch term falls with age across batches no proposal touches (the post-2015 groups)",
          h_new[0] < h_new[-1] or np.polyfit(np.arange(len(h_new)), h_new, 1)[0] > 0, ", ".join("%.3f" % v for v in h_new))
    by_d = [int((wd["flag"] & (wd["dist"][wd["sf"]] == k)).sum()) for k in range(4)]
    check("R5 replaced units in every district", min(by_d) > 200, ", ".join(map(str, by_d)))
    hint_r = {h["sentence"]: h["rescues"] for h in E["hints"]}
    check("R5 each stump alone on the reflex route rescues a third of the results or fewer",
          all(len(v) <= 7 // 3 for v in hint_r.values()), json.dumps(hint_r)[:200])
    # ---- R6: the one-fact test computed ----
    check("R6 the largest single hint (reach to the switch's own on-air transmitter) rescues R1 alone",
          E["hints"][0]["rescues"] == ["R1"])
    # ---- R7: the rivals land in band or are ruled out by named data ----
    C._TENSORS.clear()
    static = np.tile(wd["now"], (wd["n_events"], 1))
    f_st = C.all_figures(wd, C.model(wd, reach=static), ln)
    check("R7 reach to the switch's own transmitters with the off-air days ignored: the golden set, every figure in band",
          AN.funded(f_st, ln) == AN.funded(gold, ln) and not in_band_all(f_st), ", ".join(in_band_all(f_st)))
    for rb in ((2.0, 8.0, 14.0, 20.0), (4.0, 8.0, 14.0, 20.0), tuple(float(v) for v in range(4, 32, 4)),
               tuple(float(v) for v in range(2, 32, 2))):
        m_ = C.model(wd, rb=rb)
        qn = m_["q"][np.digitize(wd["now"][wd["now"] <= 8], rb)].mean()
        m2 = dict(m_, q=m_["q"] / qn, th=m_["th"] * qn)
        f_ = C.all_figures(wd, m2, ln)
        check("R7 reception in finer bands %s on the within-8-km footing: the golden set, members in band" % "/".join("%g" % v for v in rb),
              AN.funded(f_, ln) == AN.funded(gold, ln) and not [k for k in C.MEMBERS if not inside(f_[k], B[k])])
    check("R7 the nearest listed transmitter of either system is ruled out by the off-air slice",
          F["fals"]["generous"] > 4 * F["fals"]["golden"], "%.3f against %.3f" % (F["fals"]["generous"], F["fals"]["golden"]))
    check("R7 the study homes carried to the fleet are ruled out by the steps (delivered %s kW against %s)" % (
        F["routes"]["rigorous"]["delivered"], F["delivered"]), F["routes"]["rigorous"]["delivered"] > 1.5 * F["delivered"])
    # ---- the semantic fork table ----
    ln_m = {m: ln[m] for m in C.MEMBERS}
    check("SF1 worth funding is the kW at USD 88 covering the cost: every funded member clears its break-even",
          all(gold[m] >= ln_m[m] for m in AN.funded(gold, ln)))
    i_mean = float(np.mean(wd["wx"]))
    go_mean = [m for m in C.MEMBERS if gold[m] * i_mean / C.W_CP >= ln[m]]
    check("SF2 at the trial's mean index instead of the appraisal's 1.15: the funded set", go_mean == AN.funded(gold, ln),
          "index %.3f funds %s" % (i_mean, go_mean))
    old_unf = (wd["yr"] <= 2015) & (~wd["flag"])
    dd = wd["dist"][wd["sf"]]
    check("SF3 each proposal on its own: the rounds' premises never overlap",
          cnt["fix_t"] == int((old_unf & (dd == 0)).sum()) and cnt["fix_w"] == int((old_unf & (dd == 1)).sum())
          and cnt["recon_in"] + cnt["recon_out"] == int(wd["flag"].sum()))
    sites = ex["sites"]
    check("SF4 the 2027 footing is every listed transmitter with no off-air date (the old tower out, the Pruett site in)",
          sorted(s["id"] for s in sites if s["off"] is None) == sorted([s[0] for s in P.VHF_SITES] + [s[0] for s in P.FLEX_SITES]))
    check("SF5 the fringe is reach to the switch's own system: either-system reach moves the repeater across its line",
          F["routes"]["generous"]["rep_w"] < ln["rep_w"] <= gold["rep_w"])
    check("SF6 the fringe share is stated against the switches within 8 km (the near band is the reference)", F["fit"]["q"][0] == 1.0)
    vhf_old = (wd["yr"] <= 2015) == wd["vhf"]
    check("SF7 installed through 2015 and VHF receivers coincide on the register", bool(vhf_old.all()))
    allp = 1.0 - float(np.mean(gm["th"][wd["yr"] <= 2015] * gm["c"][wd["flag"].astype(int)][wd["yr"] <= 2015])) / gm["k"]
    check("SF8 still working is read at premises with no replaced unit (the all-premises reading is stated beside it)",
          abs(F["c2_failed"] / 100.0 - gold["c2_failed_old"]) < 0.006 and allp > gold["c2_failed_old"], "all premises %.3f" % allp)
    C._TENSORS.clear()
    w_und, _ = R.read(T, dated=False)
    check("SF9 a record counts only when dated after the switch went in (undated, %d more switches are listed)" % int(w_und["flag"].sum() - wd["flag"].sum()),
          w_und["flag"].sum() > wd["flag"].sum())
    C._TENSORS.clear()
    tot = F["lost_reach"] + F["lost_hw"] + F["lost_unwired"] + F["delivered"]
    check("SF10 the bridge in the appraisal's order closes on what the switches could take off", abs(tot - F["could_shed"]) <= 2,
          "%d against %d" % (tot, F["could_shed"]))
    check("SF11 the planning figure (1.0 kW a switch) is priced beside the measured level", F["fit"]["working_kw"] < 1.0)
    check("SF12 every step window from 3 to 10 minutes each side files the golden set (in the battery)",
          all(AN.funded(v, ln) == AN.funded(gold, ln) for k, v in F["family"].items() if k.startswith("step window")),
          "%d windows" % sum(1 for k in F["family"] if k.startswith("step window")))
    enc = R.rows(os.path.join(T, CM.FILES["encoder"]))
    grp_ok = all(r_["group"] == "TEST" or re.fullmatch(r"AC-\d\d", r_["group"]) for r_ in enc)
    check("SF13 the encoder addresses the register's paging groups", grp_ok)
    check("SF14 feeder membership as operated equals the register's on every event day", not any(d_ in ev for _, d_ in tr))
    check("SF15 the reach bands: the battery's four other band sets file the golden set",
          all(AN.funded(F["family"][v], ln) == AN.funded(gold, ln) for v in F["family"] if v.startswith("bands")))
    for sf, v in (("SF16", "unweighted least squares"), ("SF17", "batch term a line in age"), ("SF18", "study responders cut at 0.15 kW"),
                  ("SF18", "study responders cut at 0.35 kW"), ("SF19", "cooling index measured from 0.1")):
        check("%s %s files the golden set" % (sf, v), AN.funded(F["family"][v], ln) == AN.funded(gold, ln))
    check("SF20 the rounds' premises follow their scopes (find-and-fix excludes the reconnection lists; the reconnection lists split at 14 km)",
          cnt["recon_in"] + cnt["recon_out"] == int(wd["flag"].sum()))
    # ---- the pinning list ----
    plan = text_of(os.path.join(T, CM.FILES["plan"]))
    inv = text_of(os.path.join(T, CM.FILES["invoices"]))
    rep = text_of(os.path.join(T, CM.FILES["report"]))
    check("P0 the documents were read (positive controls)", "Section 6. Load management" in plan and "Billing demand" in inv
          and "planning figure" in rep and len(plan) > 2000)
    for s_ in ("USD 88 a kW-year", "1.15", "more than 20 km", "within 8 km", "within 14 km", "USD 16,300", "USD 24,600",
               "USD 15.60", "USD 28.40", "USD 13.70", "USD 24.50", "-31.0 km, 12.0 km", "3.0 km, 25.0 km", "installed through 2015",
               "dated after the switch was installed", "each switch counted once against the first of these that stops it"):
        check("P1 the work plan files %r" % s_, s_ in plan)
    check("P2 the invoices file the USD 22.00 demand rate", "USD 22.00 a kW-month" in inv)
    idx = ex["idx"]
    pk = [idx[P.EVENT_DAYS[e]] for e in P.PEAK_EVENTS]
    check("P3 the four coincident-peak afternoons' index averages the appraisal's 1.15", abs(np.mean(pk) - 1.15) < 0.0026, "%.4f" % np.mean(pk))
    for e in P.PEAK_EVENTS:
        check("P3 the invoice states the index of %s" % P.EVENT_DAYS[e], ("%.3f" % idx[P.EVENT_DAYS[e]]) in inv)
    # ---- forcing ----
    check("F1 each fitted input moved by its spread (20 per cent, the working level 10) holds the call",
          all(AN.funded(v, ln) == AN.funded(gold, ln) for v in F["perturb"].values()), "%d moves" % len(F["perturb"]))
    tight = min((F["perturb"][v][m] - ln[m]) / ln[m] for v in F["perturb"] for m in AN.funded(gold, ln))
    check("F2 the tightest funded member under perturbation stays above its line", tight > 0.05, "%.1f per cent" % (100 * tight))
    # ---- the face-value records ----
    tests = R.rows(os.path.join(T, CM.FILES["tests"]))
    pass_share = sum(r_["result"] == "PASS" for r_ in tests) / len(tests)
    check("V1 the bench checks pass 96 in 100", round(100 * pass_share) == 96, "%.4f" % pass_share)
    wo = R.rows(os.path.join(T, CM.FILES["orders"]))
    y = [r_ for r_ in wo if r_["ac_replaced_since_switch_installed"] == "Y"]
    share = sum(r_["lm_switch_found"] == "Found unwired" for r_ in y) / len(y)
    check("V2 the work orders find 9 in 100 unwired where the air conditioner was replaced", round(100 * share) == 9, "%.4f of %d" % (share, len(y)))
    rv = float(W["dv"].min(1)[W["vhf"]].max()) + 2.6
    rc = float(W["dc"].min(1)[~W["vhf"]].max()) + 2.4
    far_v = float(wd["now"][wd["vhf"]].max())
    far_c = float(wd["now"][~wd["vhf"]].max())
    check("V3 the published coverage contours reach past every premise on their own system", far_v < rv and far_c < rc,
          "VHF %.1f km inside %.1f, FLEX %.1f inside %.1f" % (far_v, rv, far_c, rc))
    # ---- input gates ----
    files = sorted(os.listdir(T))
    cats = {os.path.splitext(f)[1] for f in files}
    check("G1 ten or more usable files", len(files) >= 10, "%d" % len(files))
    check("G2 two or more file categories", len(cats & {".csv", ".xlsx"}) and len(cats & {".pdf", ".docx", ".png"}), ", ".join(sorted(cats)))
    n_scada = sum(1 for _ in open(os.path.join(T, CM.FILES["scada"]))) - 1
    n_reg = sum(1 for _ in open(os.path.join(T, CM.FILES["register"]))) - 1
    check("G3 a large messy CSV of 20,000 rows or more", n_scada >= 20000, "%d" % n_scada)
    check("G4 a CSV of ten printed pages or more", n_reg >= 600, "%d register rows" % n_reg)
    check("G5 two distractors, never named as such", all(f in files for f in CM.DISTRACTORS)
          and not any(re.search("distract", f, re.I) for f in files))
    check("G6 the golden reads no distractor", "amr_monthly" not in open(os.path.join(HERE, "read.py")).read()
          and "water_heater_winter" not in open(os.path.join(HERE, "read.py")).read())
    # ---- realism sweep ----
    regr = R.rows(os.path.join(T, CM.FILES["register"]))
    for col, rows_ in (("premise_no", regr), ("rebate_no", R.rows(os.path.join(T, CM.FILES["rebates"]))),
                       ("permit_no", R.rows(os.path.join(T, CM.FILES["permits"]))), ("work_order", wo)):
        vals = sorted(int(re.sub(r"\D", "", r_[col])) for r_ in rows_ if r_[col])
        dif = np.diff(vals)
        check("H1 %s is not an arithmetic sequence" % col, len(set(dif.tolist())) > 2)
    cons = {r_["contractor"] for r_ in R.rows(os.path.join(T, CM.FILES["rebates"]))}
    check("H2 contractor names take more than two shapes", len({re.sub(r"^\w+ ", "", c) for c in cons}) > 2)
    late = [r_ for r_ in R.rows(os.path.join(T, CM.FILES["permits"])) if r_["issued"] > "2026-10-08"]
    check("H3 no permit after the county's pull", not late)
    late = [r_ for r_ in R.rows(os.path.join(T, CM.FILES["rebates"])) if r_["paid"] and r_["paid"] > "2026-10-01"]
    check("H3 no rebate paid after the rebate extract", not late)
    check("H4 no em dash in any shipped document", not any("—" in text_of(os.path.join(T, f)) for f in
                                                         (CM.FILES["plan"], CM.FILES["invoices"], CM.FILES["report"])))
    loads = np.array([v[0][:45].mean() for v in ex["series"].values()])
    check("H5 feeder loads in kW sit between 0.8 and 4.5 MW", 800 < loads.min() and loads.max() < 4500,
          "%.0f to %.0f kW" % (loads.min(), loads.max()))
    sm = [float(r_["kwh"]) for r_ in R.rows(os.path.join(T, CM.FILES["study_meters"]))[:50000]]
    check("H5 study home hourly kWh between 0 and 15", 0 < min(sm) and max(sm) < 15, "%.2f to %.2f" % (min(sm), max(sm)))
    fails = [o for o in OUT if not o[1]]
    for lab, ok, det in OUT:
        print("%s  %-110s %s" % ("PASS" if ok else "FAIL", lab[:110], det[:120]))
    print("%s  task7 checks: %d assertions, %d FAIL" % ("FAIL" if fails else "PASS", len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
