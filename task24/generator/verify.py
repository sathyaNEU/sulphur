"""task24: an independent recomputation, from the installed pack's raw files with pandas only (no analysis.py, no
readpack.py), of every figure the answer blocks state that a second hand can rebuild without the model: the register
against the records it summarises, the usable counts, the plan's mix, the order's and the quote's terms, the cost,
the dashboard figure, the reviews' accuracies, the audit's crowd and desk disagreement with unanimous technicians,
and that the golden's purchase sits inside the vendors' terms. Exit 1 on any mismatch.

    python3 verify.py
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
TYPES = ["order_delivery", "returns_refunds", "account_billing", "product_howto", "device_troubleshooting"]
OUT = []


def check(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def text(name):
    return " ".join(subprocess.run(["pdftotext", "-layout", os.path.join(TGT, name), "-"], capture_output=True,
                                   text=True, check=True).stdout.split())


def main():
    FG = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_excel(os.path.join(TGT, "reward_model_runs.xlsx"), sheet_name="runs")
    rev_sheet = pd.read_excel(os.path.join(TGT, "reward_model_runs.xlsx"), sheet_name="shadow_reviews")
    # 1. the dashboard figure: IS-25 agreement from the item records, one row per run and pair
    IS = pd.read_csv(os.path.join(TGT, "internal_set_IS25.csv"))
    E = pd.read_csv(os.path.join(TGT, "eval_results_by_item.csv")).drop_duplicates(["run_id", "pair_id"])
    m = E.merge(IS[["pair_id", "label"]], on="pair_id")
    agr = (m.preferred == m.label).groupby(m.run_id).mean()
    for _, r in reg.iterrows():
        check("register IS-25 agreement %s" % r.run_id, abs(100 * agr[r.run_id] - r.is25_agreement_pct) < 0.051,
              "%.2f vs %.1f" % (100 * agr[r.run_id], r.is25_agreement_pct))
    prod = reg.loc[reg.status == "production", "run_id"].tolist()
    check("one production run", prod == ["RM-22"], str(prod))
    check("dashboard figure in the answer blocks", abs(FG["R2_dashboard_RM22"] - round(100 * agr["RM-22"], 1)) < 1e-9)
    # 2. the shadow reviews: accuracy against the majority of three, the form's vote codes read as A and B
    R = pd.read_csv(os.path.join(TGT, "shadow_reviews_2026.csv"))
    code = {"first": "A", "second": "B", "A": "A", "B": "B"}
    votes = np.stack([R["vote_%d" % k].map(code).values == "B" for k in (1, 2, 3)], 1).sum(1)
    maj = np.where(votes >= 2, "B", "A")
    for _, r in rev_sheet.iterrows():
        s = R.review_round.values == r.review_round
        acc = (R.model_preferred.values[s] == maj[s]).mean()
        check("review round %d accuracy" % r.review_round, abs(100 * acc - r.accuracy_vs_standard_pct) < 0.051)
    check("seven review rounds, none of the production run", len(rev_sheet) == 7 and "RM-22" not in set(R.run_id))
    # 3. usable counts: the production run's training set is every usable 2026 comparison
    TF = pd.read_csv(os.path.join(TGT, "tallyfield_deliveries_2026.csv"))
    dup = TF.comparison_id.duplicated().sum()
    TF = TF.drop_duplicates("comparison_id")
    use = TF[TF.judgment != "no_preference"]
    AD = pd.read_csv(os.path.join(TGT, "ardentdesk_deliveries_2026.csv"))
    r22 = reg.set_index("run_id").loc["RM-22"]
    for t in TYPES:
        check("RM-22 Tallyfield %s" % t, int(r22["tallyfield_%s" % t]) == int((use.ticket_type == t).sum()))
        check("RM-22 Ardentdesk %s" % t, int(r22["ardentdesk_%s" % t]) == int((AD.ticket_type == t).sum()))
    check("re-exported batches present and repeating their first export", dup > 0, "%d repeated rows" % dup)
    # 4. the plan, the order and the quote
    P = pd.read_csv(os.path.join(TGT, "ticket_mix_plan_2027.csv"))
    g = P.groupby("ticket_type").planned_tickets.sum()
    mix = g / g.sum()
    order = text("tallyfield_order_TF-PEN-2027-Q1.pdf")
    names = {"order_delivery": "Orders and delivery", "returns_refunds": "Returns and refunds",
             "account_billing": "Account and billing", "product_howto": "Product how-to",
             "device_troubleshooting": "Device troubleshooting"}
    by = {t: int(re.search(re.escape(n) + r" ([\d,]+)", order).group(1).replace(",", "")) for t, n in names.items()}
    check("order total 300,000", sum(by.values()) == 300000)
    check("order follows the plan's mix to the nearest 100", all(abs(by[t] - 300000 * mix[t]) <= 100 for t in TYPES))
    check("order troubleshooting in the answer blocks", FG["order_troubleshooting"] == by["device_troubleshooting"])
    quote = text("ardentdesk_quote_AD-Q-2611-07.pdf")
    price = float(re.search(r"USD ([\d.]+) per comparison", quote).group(1))
    cap = int(re.search(r"([\d,]+) comparisons, delivered", quote).group(1).replace(",", ""))
    pol = text("launch_policy_DL-03.pdf")
    bar = float(re.search(r"expected to reach ([\d.]+) per cent accuracy", pol).group(1))
    check("bar in the answer blocks", abs(FG["bar_pct"] - bar) < 1e-9)
    p = FG["R7_purchase"]
    check("purchase within the quote's terms", p["option"] == 0 and 10000 <= p["desk"] <= cap and p["desk"] % 1000 == 0)
    check("cost is the volume at the quote's price", FG["R7_cost_usd"] == int(round(p["desk"] * price)))
    check("expected accuracy at the purchase clears the bar", FG["R7_at_purchase_mix"] >= bar)
    check("80 per cent range holds the expected accuracy", FG["R8_range"]["lo"] < FG["R7_at_purchase_mix"] < FG["R8_range"]["hi"])
    # 5. the audit, read plainly: disagreement with three unanimous technicians
    Au = pd.read_csv(os.path.join(TGT, "label_audit_2026.csv"), keep_default_na=False)
    other = np.where(Au.shown_left.values == "A", "B", "A")
    Au["j"] = np.where(Au.source.values == "ardentdesk", np.where(Au.judgment.values == "left", Au.shown_left.values, other),
                       Au.judgment.values)
    tech = Au[Au.source == "penvale_technician"].groupby("audit_pair_id").j.agg(lambda s: (s == "B").sum())
    unan = tech[(tech == 0) | (tech == 3)]
    truth = (unan == 3).map({True: "B", False: "A"})
    for src, key in (("tallyfield", "crowd"), ("ardentdesk", "desk")):
        s = Au[(Au.source == src) & Au.audit_pair_id.isin(truth.index) & Au.j.isin(["A", "B"])]
        s = s[s.ticket_type == "device_troubleshooting"]
        err = (s.j.values != truth[s.audit_pair_id].values).mean()
        latent = FG["%s_error_troubleshooting" % key]
        check("audit %s troubleshooting disagreement near the fitted error" % src, abs(err - latent) < 0.05,
              "plain %.3f, fitted %.3f" % (err, latent))
    for lab, okk, det in OUT:
        print("%s  %s%s" % ("PASS" if okk else "FAIL", lab, ("  (" + det + ")") if det else ""))
    n_fail = sum(1 for _, okk, _ in OUT if not okk)
    print("verify: %d of %d" % (len(OUT) - n_fail, len(OUT)))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
