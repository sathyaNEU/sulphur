"""task24: read the cut pack back into the tables the analysis runs on, applying only what the pack's own files say
(each system's keys, the review form's vote codes, the desk tool's display order, the order's and the quote's terms,
the plan). Nothing here reads generator state: the golden and the verifier both start from these tables."""
import os
import re
import subprocess

import numpy as np
import pandas as pd

TYPES = ["order_delivery", "returns_refunds", "account_billing", "product_howto", "device_troubleshooting"]
TIX = {t: i for i, t in enumerate(TYPES)}
FILES = dict(runs="reward_model_runs.xlsx", evals="eval_results_by_item.csv", internal="internal_set_IS25.csv",
             reviews="shadow_reviews_2026.csv", audit="label_audit_2026.csv", tf="tallyfield_deliveries_2026.csv",
             ad="ardentdesk_deliveries_2026.csv", plan="ticket_mix_plan_2027.csv",
             policy="launch_policy_DL-03.pdf", order="tallyfield_order_TF-PEN-2027-Q1.pdf",
             quote="ardentdesk_quote_AD-Q-2611-07.pdf")
NAMES = {"Orders and delivery": "order_delivery", "Returns and refunds": "returns_refunds",
         "Account and billing": "account_billing", "Product how-to": "product_howto",
         "Device troubleshooting": "device_troubleshooting"}


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def tallyfield(target):
    D = pd.read_csv(os.path.join(target, FILES["tf"]))
    D = D.drop_duplicates("comparison_id", keep="first")      # batches exported twice after the platform move
    return pd.DataFrame(dict(type=D.ticket_type.map(TIX).values, words_a=D.reply_a_words.values,
                             words_b=D.reply_b_words.values,
                             choice=np.where(D.judgment.values == "no_preference", "none", D.judgment.values))), D


def ardentdesk(target):
    D = pd.read_csv(os.path.join(target, FILES["ad"]))
    other = np.where(D.shown_left.values == "A", "B", "A")
    choice = np.where(D.chose.values == "left", D.shown_left.values, other)
    return pd.DataFrame(dict(type=D.ticket_type.map(TIX).values, words_a=D.reply_a_words.values,
                             words_b=D.reply_b_words.values, choice=choice)), D


def audit(target):
    A = pd.read_csv(os.path.join(target, FILES["audit"]), keep_default_na=False)
    other = np.where(A.shown_left.values == "A", "B", "A")
    j = np.where(A.source.values == "ardentdesk", np.where(A.judgment.values == "left", A.shown_left.values, other),
                 np.where(A.judgment.values == "no_preference", "none", A.judgment.values))
    A = A.assign(j=j)
    src = {"tallyfield": "crowd", "ardentdesk": "desk", "penvale_technician": "tech"}
    A["k"] = A.groupby(["audit_pair_id", "source"]).cumcount() + 1
    A["col"] = [src[s] + str(k) for s, k in zip(A.source.values, A.k.values)]
    W = A.pivot(index="audit_pair_id", columns="col", values="j").reset_index()
    base = A.drop_duplicates("audit_pair_id")[["audit_pair_id", "ticket_type", "reply_a_words", "reply_b_words"]]
    W = base.merge(W, on="audit_pair_id", how="left").sort_values("audit_pair_id").reset_index(drop=True)
    W["type"] = W.ticket_type.map(TIX)
    W = W.rename(columns=dict(reply_a_words="words_a", reply_b_words="words_b"))
    return W


def internal(target):
    S = pd.read_csv(os.path.join(target, FILES["internal"]))
    return pd.DataFrame(dict(pair_id=S.pair_id.values, type=S.ticket_type.map(TIX).values,
                             words_a=S.reply_a_words.values, words_b=S.reply_b_words.values, label=S.label.values))


def evals(target, IS, runs):
    E = pd.read_csv(os.path.join(target, FILES["evals"]))
    E = E.drop_duplicates(["run_id", "pair_id"], keep="first")   # a re-run job re-scores from its checkpoint
    picks = {}
    pos = pd.Series(np.arange(len(IS)), index=IS.pair_id.values)
    for rid in runs:
        g = E[E.run_id == rid]
        arr = np.empty(len(IS), dtype=object)
        arr[pos[g.pair_id.values].values] = g.preferred.values
        assert not any(v is None for v in arr), rid
        picks[rid] = arr
    return picks, E


def reviews(target):
    R = pd.read_csv(os.path.join(target, FILES["reviews"]))
    code = {"first": "A", "second": "B", "A": "A", "B": "B"}
    out = pd.DataFrame(dict(run_id=R.run_id.values, round=R.review_round.values, type=R.ticket_type.map(TIX).values,
                            words_a=R.reply_a_words.values, words_b=R.reply_b_words.values,
                            pick=R.model_preferred.values))
    for k in (1, 2, 3):
        out["vote%d" % k] = R["vote_%d" % k].map(code).values
    return out


def register(target):
    X = pd.read_excel(os.path.join(target, FILES["runs"]), sheet_name="runs")
    counts = {}
    for _, r in X.iterrows():
        nA = np.array([r["tallyfield_%s" % t] for t in TYPES], float)
        nB = np.array([r["ardentdesk_%s" % t] for t in TYPES], float)
        counts[r.run_id] = (nA, nB)
    prod = X.loc[X.status == "production", "run_id"].tolist()
    assert len(prod) == 1
    return X, counts, list(X.run_id.values), prod[0]


def plan_mix(target):
    P = pd.read_csv(os.path.join(target, FILES["plan"]))
    g = P.groupby("ticket_type").planned_tickets.sum()
    return np.array([g[t] for t in TYPES], float) / g.sum()


def order_terms(target):
    txt = pdf_text(os.path.join(target, FILES["order"]))
    by = np.zeros(len(TYPES))
    for name, key in NAMES.items():
        m = re.search(re.escape(name) + r"\s+([\d,]+)", txt)
        by[TIX[key]] = float(m.group(1).replace(",", ""))
    price = float(re.search(r"USD ([\d.]+) per completed comparison", txt).group(1))
    flat = " ".join(txt.split())
    m = re.search(r"add up to ([\d,]+) further comparisons .*? in steps of ([\d,]+)", flat)
    option, ostep = float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))
    return by, price, option, ostep


def quote_terms(target):
    txt = pdf_text(os.path.join(target, FILES["quote"]))
    price = float(re.search(r"USD ([\d.]+) per comparison", txt).group(1))
    cap = float(re.search(r"([\d,]+) comparisons, delivered", txt).group(1).replace(",", ""))
    step = float(re.search(r"in steps of ([\d,]+)", txt).group(1).replace(",", ""))
    minimum = float(re.search(r"at least ([\d,]+) comparisons", txt).group(1).replace(",", ""))
    mix = np.zeros(len(TYPES)); mix[TIX["device_troubleshooting"]] = 1.0
    assert "device troubleshooting tickets" in txt
    return price, cap, step, minimum, mix


def bar(target):
    txt = " ".join(pdf_text(os.path.join(target, FILES["policy"])).split())
    return float(re.search(r"expected to reach ([\d.]+) per cent accuracy", txt).group(1)) / 100.0


def view(target):
    TF, TFraw = tallyfield(target)
    X, counts, runs, prod = register(target)
    IS = internal(target)
    picks, E = evals(target, IS, runs)
    REV = reviews(target)
    ST = audit(target)
    order, price_tf, option, option_step = order_terms(target)
    price_ad, cap, step, minimum, desk_mix = quote_terms(target)
    return dict(TF=TF, ST=ST, IS=IS, picks=picks, REV=REV, counts=counts, runs=runs, production=prod,
                mix27=plan_mix(target), order=order, price_tf=price_tf, price_ad=price_ad, cap=cap, step=step,
                min_order=minimum, option=option, option_step=option_step, desk_mix=desk_mix, bar=bar(target),
                register=X)
