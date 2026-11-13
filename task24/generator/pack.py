"""task24: the pack's records, written as each system exports them: Tallyfield's portal export, Ardentdesk's
labelling tool, Penvale's evaluation pipeline, the shadow review log, the label audit, the reward-model run register,
the operating plan and the support team's own side files. Layer 1 mess comes from each system's own behaviour:
batches exported twice after Tallyfield's June platform move, 'no preference' judgments, the desk tool's display
order, evaluation jobs re-run from their last checkpoint, the review form's change of vote codes in May, three
clocks."""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Font

import postprocess as PP
import world as Wd

FIRM = "Penvale Electronics Ltd"
UTC = dt.timezone.utc
NZDT = dt.timezone(dt.timedelta(hours=13))
NZST = dt.timezone(dt.timedelta(hours=12))
MNL = dt.timezone(dt.timedelta(hours=8))
F = dict(runs="reward_model_runs.xlsx", evals="eval_results_by_item.csv", internal="internal_set_IS25.csv",
         reviews="shadow_reviews_2026.csv", audit="label_audit_2026.csv", tf="tallyfield_deliveries_2026.csv",
         ad="ardentdesk_deliveries_2026.csv", plan="ticket_mix_plan_2027.csv", vol26="ticket_volumes_2026.csv",
         csat="draftline_csat_2026.csv", config="draftline_eval_config.yaml", policy="launch_policy_DL-03.pdf",
         order="tallyfield_order_TF-PEN-2027-Q1.pdf", quote="ardentdesk_quote_AD-Q-2611-07.pdf",
         quality="tallyfield_quality_summary_2026.pdf")
TECHS = ["T-%02d" % k for k in (1, 2, 3, 4, 5, 6, 7, 8)]
REDELIVERED = ("TF26-022", "TF26-023", "TF26-024")


def pacific(t):
    """a naive US Pacific wall-clock time as Tallyfield's export writes it, with its offset"""
    dst = dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 2)
    return t.replace(tzinfo=dt.timezone(dt.timedelta(hours=-7 if dst else -8)))


def nz(d):
    """New Zealand's offset on a date (daylight time from the last Sunday of September to the first Sunday of April)"""
    return NZDT if (d < dt.date(2026, 4, 5) or d >= dt.date(2026, 9, 27)) else NZST


def iso(t):
    return t.isoformat(timespec="seconds")


def tname(i):
    return Wd.TYPES[int(i)]


# ------------------------------------------------------------------ Tallyfield and Ardentdesk exports
def tallyfield_export(T, path):
    D = T["TF"]
    rng = Wd.rng_for("tf-export")
    secs = D.seconds.values.copy()
    stuck = rng.random(len(D)) < 0.003
    secs[stuck] = (rng.uniform(900, 3600, stuck.sum())).astype(int)       # a task left open on a worker's screen
    out = pd.DataFrame(dict(
        comparison_id=D.comparison_id.values, batch_id=D.batch_id.values, worker_id=D.worker_id.values,
        ticket_type=[tname(i) for i in D.type.values], reply_a_words=D.words_a.values, reply_b_words=D.words_b.values,
        judgment=np.where(D.choice.values == "none", "no_preference", D.choice.values), seconds_on_task=secs,
        submitted_at=[iso(pacific(t.to_pydatetime())) for t in D.submitted_local],
        delivered_at=[iso(pacific(t.to_pydatetime())) for t in D.delivered_local]))
    again = out[out.batch_id.isin(REDELIVERED)].copy()
    again["delivered_at"] = iso(pacific(dt.datetime(2026, 6, 26, 9, 12)))
    out = pd.concat([out, again], ignore_index=True)
    out = out.sort_values(["delivered_at", "batch_id", "submitted_at", "comparison_id"], kind="mergesort")
    out.to_csv(path, index=False)
    return len(out), len(again)


def ardentdesk_export(T, path):
    D = T["AD"]
    shown_left = np.where(D.swapped.values, "B", "A")
    out = pd.DataFrame(dict(
        record_id=D.record_id.values, batch=D.batch.values, agent_id=D.agent_id.values,
        ticket_type=[tname(i) for i in D.type.values], reply_a_words=D.words_a.values, reply_b_words=D.words_b.values,
        shown_left=shown_left, chose=D.chose.values,
        handled_at=[iso(t.to_pydatetime().replace(tzinfo=MNL)) for t in D.handled_local], seconds=D.seconds.values))
    out.to_csv(path, index=False)
    return len(out)


# ------------------------------------------------------------------ the internal set and the evaluation pipeline
def internal_set(T, path):
    IS = T["IS"]
    rng = Wd.rng_for("is-months")
    months = ["2025-%02d" % m for m in rng.integers(1, 11, len(IS))]
    out = pd.DataFrame(dict(pair_id=IS.pair_id.values, ticket_type=[tname(i) for i in IS.type.values],
                            reply_a_words=IS.words_a.values, reply_b_words=IS.words_b.values, label=IS.label.values,
                            source_month=months))
    out.to_csv(path, index=False)


EVAL_CRASH = {"RM-09": (5312, 5200), "RM-18": (2950, 2900)}   # pairs scored before the crash, re-run checkpoint


def eval_results(T, path):
    IS = T["IS"]
    rows = []
    job = 101
    n = len(IS)
    for rid, trained, *_ in Wd.RUNS:
        picks = T["picks"][rid]
        t0 = dt.datetime.combine(trained + dt.timedelta(days=1), dt.time(2, 10), UTC)
        step = dt.timedelta(seconds=0.42)
        if rid in EVAL_CRASH:
            done, ck = EVAL_CRASH[rid]
            for i in range(done):
                rows.append(("EJ-26-%04d" % job, rid, IS.pair_id.values[i], picks[i], iso(t0 + i * step)))
            job += 1
            t1 = t0 + dt.timedelta(hours=3, minutes=17)
            for i in range(ck, n):
                rows.append(("EJ-26-%04d" % job, rid, IS.pair_id.values[i], picks[i], iso(t1 + (i - ck) * step)))
            job += 1
        else:
            for i in range(n):
                rows.append(("EJ-26-%04d" % job, rid, IS.pair_id.values[i], picks[i], iso(t0 + i * step)))
            job += 1
    out = pd.DataFrame(rows, columns=["job_id", "run_id", "pair_id", "preferred", "scored_at"])
    out.to_csv(path, index=False)
    return len(out)


def is25_agreement(T):
    IS = T["IS"]
    return {rid: float((np.asarray(T["picks"][rid]) == IS.label.values).mean()) for rid, *_ in Wd.RUNS}


# ------------------------------------------------------------------ the shadow reviews and the label audit
def reviews(T, path):
    R = T["REV"]
    rng = Wd.rng_for("review-techs")
    rows = []
    for rnd, g in R.groupby("round", sort=True):
        d0, rid = Wd.REVIEW_ROUNDS[rnd]
        days = [d0 + dt.timedelta(days=k) for k in range(12) if (d0 + dt.timedelta(days=k)).weekday() < 5]
        for j, (_, r) in enumerate(g.iterrows()):
            techs = rng.choice(len(TECHS), 3, replace=False)
            votes = [r["vote%d" % k] for k in (1, 2, 3)]
            if rnd <= 3:      # the review form recorded the reply listed first or second until May
                votes = ["first" if v == "A" else "second" for v in votes]
            day = days[min(len(days) - 1, j * len(days) // len(g))]
            rows.append((rnd, day.isoformat(), rid, "SR%d-%04d" % (rnd, j + 1), tname(r.type), int(r.words_a),
                         int(r.words_b), r.pick, TECHS[techs[0]], votes[0], TECHS[techs[1]], votes[1],
                         TECHS[techs[2]], votes[2]))
    out = pd.DataFrame(rows, columns=["review_round", "reviewed_on", "run_id", "draft_pair_id", "ticket_type",
                                      "reply_a_words", "reply_b_words", "model_preferred", "tech_1", "vote_1",
                                      "tech_2", "vote_2", "tech_3", "vote_3"])
    out.to_csv(path, index=False)


def audit(T, path):
    ST = T["ST"]
    rng = Wd.rng_for("audit-judges")
    tf_workers = sorted(set(T["TF"].worker_id.values))
    ad_agents = sorted(set(T["AD"].agent_id.values))
    rows = []
    d0 = dt.date(2026, 7, 6)
    for i, r in ST.iterrows():
        pid = "LA26-%04d" % (i + 1)
        day = d0 + dt.timedelta(days=int(i * 46 // len(ST)))
        tt = rng.choice(len(TECHS), 3, replace=False)
        ww = rng.choice(len(tf_workers), 3, replace=False)
        aa = rng.choice(len(ad_agents), 3, replace=False)
        for k in range(3):
            v = r["crowd%d" % (k + 1)]
            rows.append((pid, tname(r.type), int(r.words_a), int(r.words_b), "tallyfield", tf_workers[ww[k]],
                         "no_preference" if v == "none" else v, "",
                         iso(pacific(dt.datetime.combine(day, dt.time(9)) + dt.timedelta(minutes=int(rng.integers(0, 600)))))))
        for k in range(3):
            v = r["desk%d" % (k + 1)]
            left = "B" if rng.random() < 0.5 else "A"
            chose = "left" if v == left else "right"
            rows.append((pid, tname(r.type), int(r.words_a), int(r.words_b), "ardentdesk", ad_agents[aa[k]], chose,
                         left, iso(dt.datetime.combine(day + dt.timedelta(days=1), dt.time(9), MNL)
                                   + dt.timedelta(minutes=int(rng.integers(0, 540))))))
        for k in range(3):
            v = r["tech%d" % (k + 1)]
            rows.append((pid, tname(r.type), int(r.words_a), int(r.words_b), "penvale_technician", TECHS[tt[k]], v,
                         "", iso(dt.datetime.combine(day + dt.timedelta(days=2), dt.time(9), nz(day))
                                 + dt.timedelta(minutes=int(rng.integers(0, 480))))))
    out = pd.DataFrame(rows, columns=["audit_pair_id", "ticket_type", "reply_a_words", "reply_b_words", "source",
                                      "judge_id", "judgment", "shown_left", "judged_at"])
    out.to_csv(path, index=False)


# ------------------------------------------------------------------ the run register
def run_register(T, path, created, modified):
    agr = is25_agreement(T)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "runs"
    head = ["run_id", "trained_on", "status", "note"] + ["tallyfield_%s" % t for t in Wd.TYPES] + \
           ["ardentdesk_%s" % t for t in Wd.TYPES] + ["is25_agreement_pct"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    for rid, trained, cs, ds, rnd, status, note in Wd.RUNS:
        nA, nB = T["counts"][rid]
        ws.append([rid, trained, status, note] + [int(x) for x in nA] + [int(x) for x in nB] +
                  [round(100 * agr[rid], 1)])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in r:
            c.number_format = "yyyy-mm-dd"
    ws.column_dimensions["A"].width = 9
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["D"].width = 28
    ws2 = wb.create_sheet("shadow_reviews")
    ws2.append(["review_round", "reviewed_from", "run_id", "drafts_reviewed", "accuracy_vs_standard_pct"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    R = T["REV"]
    maj = np.where(np.stack([(R["vote%d" % k].values == "B") for k in (1, 2, 3)], 1).sum(1) >= 2, "B", "A")
    for rnd, (d0, rid) in Wd.REVIEW_ROUNDS.items():
        s = R["round"].values == rnd
        ws2.append([rnd, d0, rid, int(s.sum()), round(100 * float((R.pick.values[s] == maj[s]).mean()), 1)])
    for r in ws2.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in r:
            c.number_format = "yyyy-mm-dd"
    wb.save(path)
    PP.normalize_ooxml(path, "Sam Bartlett", "Bridget Sanders", created, modified, excel=True, company=FIRM)


# ------------------------------------------------------------------ plans, volumes and side files
def plan27(path):
    rows = []
    for m in range(1, 13):
        mix = np.array(Wd.PLAN27_MONTHS[m], float); mix /= mix.sum()
        tot = Wd.TICKETS27[m]
        n = np.round(tot * mix).astype(int)
        for d in range(Wd.ND):
            rows.append(("2027-%02d" % m, Wd.TYPES[d], int(n[d])))
    pd.DataFrame(rows, columns=["month", "ticket_type", "planned_tickets"]).to_csv(path, index=False)


def plan27_mix_from_file(path):
    P = pd.read_csv(path)
    g = P.groupby("ticket_type").planned_tickets.sum()
    return np.array([g[t] for t in Wd.TYPES], float) / g.sum()


def volumes26(path):
    rng = Wd.rng_for("vol26")
    rows = []
    for m in range(1, 11):
        mix = np.array(Wd.MONTH_MIX26[m], float); mix /= mix.sum()
        n = np.round(Wd.TICKETS26[m] * mix * rng.normal(1, 0.015, Wd.ND)).astype(int)
        for d in range(Wd.ND):
            rows.append(("2026-%02d" % m, Wd.TYPES[d], int(n[d])))
    pd.DataFrame(rows, columns=["month", "ticket_type", "tickets"]).to_csv(path, index=False)


def csat(path):
    """weekly customer satisfaction on replies sent after an agent's review, by how the reply was written"""
    rng = Wd.rng_for("csat")
    base = dict(order_delivery=4.31, returns_refunds=4.02, account_billing=4.12, product_howto=4.38,
                device_troubleshooting=3.86)
    rows = []
    wk = dt.date(2026, 1, 5)
    while wk <= dt.date(2026, 11, 2):
        for t in Wd.TYPES:
            n_d = int(rng.integers(140, 420)); n_a = int(rng.integers(60, 220))
            rows.append((wk.isoformat(), t, n_d, round(base[t] + rng.normal(0.02, 0.06), 2), n_a,
                         round(base[t] + rng.normal(0.05, 0.08), 2)))
        wk += dt.timedelta(weeks=1)
    pd.DataFrame(rows, columns=["week_starting", "ticket_type", "drafted_replies_surveyed", "drafted_csat",
                                "agent_written_surveyed", "agent_written_csat"]).to_csv(path, index=False)


def config(path):
    txt = """# Draftline offline evaluation pipeline
# Support Automation, Penvale Electronics. Last changed 2026-05-04 (S. Bartlett).

benchmark:
  id: IS-25
  file: internal_set_IS25.csv
  pairs: %d
  drawn_from: Penvale support tickets, January to October 2025, sampled by ticket type
  labels: one Tallyfield judgment per pair under guideline v2 (2025)
  no_preference: pairs judged 'no preference' were re-queued until a reply was chosen

metric:
  name: is25_agreement
  definition: share of benchmark pairs on which the run's preferred reply is the benchmark label
  dashboard: support-automation/rm-quality (weekly)

jobs:
  scorer: rm-score v2.3 (deterministic, no sampling)
  batch_size: 400
  retry: a failed job is resubmitted from its last checkpoint under a new job id
  output: eval_results_by_item.csv  # one row per scored pair per job

runs:
  register: reward_model_runs.xlsx
  training_counts: usable comparisons by vendor and ticket type (no-preference judgments are not used)
""" % Wd.INTERNAL_N
    open(path, "w").write(txt)


def quality_rows(T):
    D = T["TF"]
    rng = Wd.rng_for("quality")
    rows = []
    for m in range(1, 10):
        s = D.delivered_local.dt.month.values == m
        rows.append(dict(month=dt.date(2026, m, 1).strftime("%B"), completed=int(s.sum()),
                         workers=int(len(set(D.worker_id.values[s]))), gold=float(93.2 + rng.normal(0.6, 0.5)),
                         turnaround=float(rng.normal(44, 6))))
    return rows
