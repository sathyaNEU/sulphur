"""task24: the generator's assertions on the installed build (the input gates, the bar block R1 to R7, the fork rows,
mess neutrality, each factor's footprint across the data, the factorial). Exit 1 on any failure.

    python3 checks.py            # reads ../target, ../submission.md, effort.json, figures.json
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import readpack as RP  # noqa: E402

TGT = os.path.join(TASK, "target")
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def main():
    FG = json.load(open(os.path.join(HERE, "figures.json")))
    EF = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    sub = open(os.path.join(TASK, "submission.md")).read()
    B = FG["bands"]
    files = sorted(os.listdir(TGT))
    # ---------------- input gates
    ok("input: 10 or more usable files", len(files) >= 10, "%d files" % len(files))
    ext = {os.path.splitext(f)[1] for f in files}
    ok("input: spreadsheet, text and code categories", {".csv", ".xlsx"} <= ext and ".pdf" in ext and ".yaml" in ext,
       ", ".join(sorted(ext)))
    tf = pd.read_csv(os.path.join(TGT, RP.FILES["tf"]), usecols=["comparison_id"])
    ok("input: a messy CSV of 20,000 rows or more", len(tf) >= 20000, "%d rows" % len(tf))
    rv = pd.read_csv(os.path.join(TGT, RP.FILES["reviews"]), usecols=["draft_pair_id"])
    ok("input: a second large CSV of 10 to 20 printed pages or more", len(rv) >= 1200, "%d rows" % len(rv))
    ok("input: 2 or more distractors, named only in metadata", len(meta["distractor_files"]) >= 2 and
       not any("distract" in f.lower() for f in files))
    used = set(RP.FILES.values())
    ok("input: no distractor is read by the golden", not any(d.split("/")[-1] in used for d in meta["distractor_files"]))
    ok("input: no readme, dictionary, notes or manifest file", not any(re.search(r"readme|dictionar|manifest|notes", f, re.I)
                                                                         for f in files))
    # ---------------- the golden recomputed on the installed pack
    V = RP.view(TGT)
    G = A.golden(V)
    ok("R7 golden purchase: Ardentdesk only", G["option_bought"] == 0 and G["volume"] == FG["R7_purchase"]["desk"],
       str(G["best"]))
    ok("R7 golden purchase inside its band", B["desk"][0] <= FG["R7_purchase"]["desk"] <= B["desk"][1])
    ok("R1 figures match: current model mix", abs(100 * G["current_mix"] - FG["R2_current"]["mix"]) < 0.051)
    ok("R2 figures match: signed order mix", abs(100 * G["grid_mix"][0] - FG["R3_order"]["mix"]) < 0.051)
    ok("R4 figures match: whole option mix", abs(100 * G["option_mix"] - FG["R5_option"]["mix"]) < 0.051)
    ok("R5 cost is the volume at the quote's price", FG["R7_cost_usd"] == int(round(FG["R7_purchase"]["desk"] * V["price_ad"])))
    ok("R5 the purchase clears the bar and one step less does not",
       G["forecast"](0, G["volume"]) >= V["bar"] and (G["volume"] <= V["min_order"] or G["forecast"](0, G["volume"] - 1000) < V["bar"]))
    ok("SF3 expected accuracy is the mean: the range holds it", FG["R8_range"]["lo"] < FG["R7_at_purchase_mix"] < FG["R8_range"]["hi"])
    # ---------------- R3 bar: the careful pass loses on the priced cells
    by = {r["id"]: r for r in EF["results"]}

    def outside(rid):
        r = by[rid]; cv = r["passes"]["careful"]
        if isinstance(r["golden"], dict):
            return [c for c in r["golden"] if not (r["bands"][c][0] <= (cv.get(c) if cv.get(c) is not None else -9) <= r["bands"][c][1])]
        return []
    ok("R3 bar: careful current-model mix outside its band", "mix" in outside("R2"), str(outside("R2")))
    ok("R3 bar: careful troubleshooting cells outside their bands at every Ardentdesk volume",
       all(("%d.device_troubleshooting" % x) in outside("R4") for x in (20000, 40000, 60000, 80000, 120000)))
    ok("R3 bar: careful signed-order and option mixes outside their bands", "mix" in outside("R3") and "mix" in outside("R5"))
    ok("R3 bar: careful call differs from the golden's", by["R6"]["passes"]["careful"] != by["R6"]["golden"])
    ok("R3 bar: the vendor-error result is the careful pass's to earn and the quick pass's to miss",
       by["R1"]["passes"]["careful"] == by["R1"]["golden"] and by["R1"]["passes"]["quick"] != by["R1"]["golden"])
    # ---------------- R7 bar: the family holds the call, the shortcuts leave it, the perturbations hold it
    gold = EF["forcing"]["golden_answer"]
    ok("R7 family: every defensible variant's purchase is carried by Ardentdesk",
       all(f["answer"] == gold for f in EF["forcing"]["golden_family"]),
       str([f["answer"] for f in EF["forcing"]["golden_family"] if f["answer"] != gold]))
    ok("R7 shortcuts: every named shortcut misses the call", all(s["answer"] != gold for s in EF["forcing"]["shortcuts"]),
       str([s["name"] for s in EF["forcing"]["shortcuts"] if s["answer"] == gold]))
    ok("R7 perturbations: each fitted input moved by its spread keeps the call",
       all(p["answer"] == gold for p in EF["forcing"]["perturbations"]),
       str([p["input"] for p in EF["forcing"]["perturbations"] if p["answer"] != gold]))
    distinct = {tuple(s["answer"]) for s in EF["forcing"]["shortcuts"]}
    ok("R7 shortcuts land on two or more distinct wrong calls", len(distinct) >= 2, str(sorted(distinct)))
    ok("R7 the per-type bend is not supported (likelihood ratio under the 5 per cent line on its degrees of freedom)",
       FG["alpha_lr"] < {4: 9.49}.get(FG["alpha_df"], 9.49), "%.1f on %d" % (FG["alpha_lr"], FG["alpha_df"]))
    ok("R7 IS-25 at the audit's error is rejected by the reviewed runs", FG["is_error_lr"] > 20, "%.1f" % FG["is_error_lr"])
    # ---------------- the factorial
    J = {j["id"]: j for j in EF["factorial"]["judgments"]}
    stumps = [j for j in J.values() if j["kind"] == "stump"]
    nec = [j["id"] for j in stumps if j["dropped"]["answer"] != gold]
    suf = [j["id"] for j in stumps if j["alone"]["answer"] == gold]
    ok("factorial: three or more stumps each necessary", len(nec) >= 3, str(nec))
    ok("factorial: no stump sufficient on the reflex route", not suf, str(suf))
    ok("factorial: the single drops land on two or more distinct wrong calls",
       len({tuple(J[j]["dropped"]["answer"]) for j in nec}) >= 2)
    # ---------------- R5 bar: each factor across the data, not only where it decides
    S = G["C"]["S"]
    ok("R5 footprint: the crowd errs more than the desk on every ticket type", all(S["ea"] > S["eb"]))
    ok("R5 footprint: the crowd's pull rises with the length gap across the bins",
       G["C"]["pull"][-1] > 3 * max(G["C"]["pull"][0], 0.01))
    ok("R5 footprint: every ticket type has pairs with no better reply", all(S["a"] > 0.04))
    agr, rev = A.per_run_measures(V)
    ok("R5 footprint: IS-25 agreement sits below review accuracy on every reviewed run and type",
       all((rev[r] - agr[V["runs"].index(r)] > 0).all() for r in rev))
    # ---------------- R2 mess neutrality
    raw_tf = pd.read_csv(os.path.join(TGT, RP.FILES["tf"]))
    ok("R2 mess: re-exported Tallyfield batches exist (a small share of rows)",
       0 < raw_tf.comparison_id.duplicated().sum() < 0.08 * len(raw_tf))
    ok("R2 mess: no-preference judgments exist", (raw_tf.judgment == "no_preference").mean() > 0.03)
    E = pd.read_csv(os.path.join(TGT, RP.FILES["evals"]))
    ok("R2 mess: evaluation jobs re-run from a checkpoint repeat some pairs", E.duplicated(["run_id", "pair_id"]).sum() > 0)
    R = pd.read_csv(os.path.join(TGT, RP.FILES["reviews"]))
    ok("R2 mess: the review form's first and second codes appear in rounds 1 to 3 only",
       set(R.loc[R.review_round <= 3, "vote_1"]) == {"first", "second"} and set(R.loc[R.review_round > 3, "vote_1"]) == {"A", "B"})
    # ---------------- forks
    ok("SF4 no-preference judgments in or out: same call", [f for f in EF["forcing"]["golden_family"]
                                                           if "no-preference" in f["name"]][0]["answer"] == gold)
    ok("SF6 the current model is the production run", V["production"] == "RM-22")
    ok("SF2 the 2027 mix is the plan's annual mix", abs(sum(V["mix27"]) - 1) < 1e-9 and V["mix27"][4] > 0.4)
    ok("SF9 cost per ordered comparison", "USD 3.60 a comparison" in sub)
    pol = RP.pdf_text(os.path.join(TGT, RP.FILES["policy"]))
    flat = " ".join(pol.split())
    ok("SF1 accuracy is against the reply at least two of three technicians choose", "at least two of the three choose" in flat)
    ok("SF5 every pair counts, whatever the split", "Every pair counts, whatever the split" in flat)
    ok("SF3 expected accuracy is the point forecast of section 7, not a bootstrap mean or a quantile",
       "Expected accuracy is the point forecast of section 7" in flat and "the point forecast" in flat
       and "does not move it" in flat)
    ok("SF16 the curve's form is filed: 1 - 0.5 x (1 + T/K)^(-b), a scale per type, one bend, no ceiling below 1",
       "1 - 0.5 x (1 + T/K)^(-b)" in flat and "a single bend fitted for all ticket types together" in flat
       and "no ceiling below 1" in flat and A.GOLDEN["form"] == "power" and A.GOLDEN["alpha"] == "pooled")
    ok("SF17 the ceiling against the standard: pairs the standard's reply is the better one, plus half the equal pairs",
       "plus half the share of pairs whose replies are as good as each other" in flat)
    ok("SF16 the logistic curve no longer sits in the golden family (section 7.1 files the form)",
       not any("logistic" in f["name"] for f in EF["forcing"]["golden_family"]))
    g0 = A.golden(V)
    for nm, o in (("counted", dict(value="raw")), ("accuracy-weighted", dict(value="acc"))):
        alt = A.golden(V, o)
        ok("SF18 the training signal read as labels %s fits the record worse than in information (2 dNLL %.1f)" % (nm, 2 * (alt["nll"] - g0["nll"])),
           2 * (alt["nll"] - g0["nll"]) > 20)
    q = " ".join(RP.pdf_text(os.path.join(TGT, RP.FILES["quote"])).split())
    ok("SF7 the desk's tool has no no-preference choice, so ordered equals usable", "does not offer 'no preference'" in q)
    ok("SF14 the desk's order is at least 10,000 in steps of 1,000", V["min_order"] == 10000 and V["step"] == 1000)
    tr = FG["tranches"]
    ok("SF15 an option tranche of up to 30,000 costs within USD 6,000 of the cheapest purchase, 40,000 or more does not",
       all(tr[o]["extra_usd"] <= 6000 for o in ("0", "10000", "20000", "30000")) and tr["40000"]["extra_usd"] > 6000,
       str({o: tr[o]["extra_usd"] for o in tr}))
    ok("SF8 the range is the expected accuracy's, from the bootstrap", FG["R8_range"]["lo"] < FG["R7_at_purchase_mix"] < FG["R8_range"]["hi"]
       and "bootstrap" in sub)
    ve = FG["R1_vendor_error"]
    ok("SF10 vendor error on every audit pair: the desk's troubleshooting error sits above its latent error, the split pairs counted",
       ve["ardentdesk.device_troubleshooting"] > 100 * FG["desk_error_troubleshooting"])
    ok("SF11 IS-25's own label error is fitted (guideline v2), the audit's reading rejected", FG["is_error_lr"] > 20 and
       "guideline v2" in open(os.path.join(TGT, "draftline_eval_config.yaml")).read())
    o = " ".join(RP.pdf_text(os.path.join(TGT, RP.FILES["order"])).split())
    ok("SF12 the option follows the order's proportions by type", "in the same proportions by ticket type as section 1" in o)
    ok("SF13 RM-22 trained on every usable 2026 comparison, so the Q1 2027 base is its training set",
       all(abs(V["counts"]["RM-22"][0][d] - ((V["TF"].type.values == d) & (V["TF"].choice.values != "none")).sum()) < 0.5
           for d in range(5)))
    # ---------------- the answer blocks
    ok("blocks: four headings in order", [h for h in re.findall(r"^## (.+)$", sub, re.M)] ==
       ["Final Recommendation", "Supplementary Questions", "Critical Components", "Step-by-Step"])
    ok("blocks: no em dash anywhere", "\u2014" not in sub)
    ok("blocks: the recommendation names the purchase", "{:,}".format(FG["R7_purchase"]["desk"]) in sub.split("## Supplementary")[0])
    for lab, okk, det in RES:
        print("%s  %s%s" % ("PASS" if okk else "FAIL", lab, ("  (" + det + ")") if det else ""))
    n_fail = sum(1 for _, okk, _ in RES if not okk)
    print("checks: %d of %d" % (len(RES) - n_fail, len(RES)))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
