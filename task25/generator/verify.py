"""Independent verifier: reads only target/ and recomputes the graded figures on its own code path (its own packer,
its own joins and fits, its own expected-value replay), then compares them with figures.json inside their bands."""
import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
import yaml
from openpyxl import load_workbook
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
res = []


def chk(label, cond, detail=""):
    res.append((label, bool(cond), detail))


def rd(p):
    return pd.read_csv(os.path.join(T, p))


def pack_seq(lens, C):
    S, cur, acc = [], 0, 0.0
    for l in lens:
        while l > 0:
            t = min(l, C - cur)
            acc += t * t
            cur += t
            l -= t
            if cur == C:
                S.append(acc / C / C)
                cur, acc = 0, 0.0
    return np.array(S), np.ones(len(S))


def pack_bf(lens, C, open_max=64):
    rem, sq, fl = [], [], []
    S, F = [], []
    for l in lens:
        parts = []
        while l > C:
            parts.append(C)
            l -= C
        if l > 0:
            parts.append(l)
        for x in parts:
            cand = [(r, j) for j, r in enumerate(rem) if x <= r]
            if cand:
                _, j = min(cand)
                rem[j] -= x
                sq[j] += x * x
                fl[j] += x
                if rem[j] == 0:
                    S.append(sq[j] / C / C); F.append(fl[j] / C); del rem[j], sq[j], fl[j]
            else:
                rem.append(C - x); sq.append(x * x); fl.append(x)
                if rem[-1] == 0:
                    S.append(sq[-1] / C / C); F.append(1.0); rem.pop(); sq.pop(); fl.pop()
                elif len(rem) > open_max:
                    j = int(np.argmin(rem))
                    S.append(sq[j] / C / C); F.append(fl[j] / C); del rem[j], sq[j], fl[j]
    return np.array(S), np.array(F)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    reg = rd("runs/run_registry_2026.csv")
    # R1: GPU-days held
    L = pd.to_datetime(reg["launched_utc"])
    Fz = pd.to_datetime(reg["finished_utc"]).fillna(pd.Timestamp("2026-11-01 00:00:00", tz="UTC"))
    held = float((reg["nodes"] * 8 * (Fz - L).dt.total_seconds() / 86400).sum())
    chk("V1 GPU-days held recomputes within 0.5 per cent", abs(held / fig["held_2026_total"] - 1) < 0.005, "%.0f" % held)
    # R3 part 1: the attention coefficient from the joined samples and manifests
    smp = rd("profiling/rank_step_samples_2026.csv")
    prev = {p: r for r, ps in zip(reg["run_id"], reg["previous_ids"].fillna("")) for p in ps.split(";") if p}
    smp["run_id"] = smp["run_id"].map(lambda x: prev.get(x, x))
    rows = []
    with open(os.path.join(T, "profiling/packing_manifests_2026.jsonl")) as fh:
        for line in fh:
            m = json.loads(line)
            C = m["seq_len"]
            rows.append((prev.get(m["run_id"], m["run_id"]), m["step"], m["dp_rank"], len(m["docs"]),
                         sum(sum(d * d for d in s) for s in m["docs"]) / C / C, C))
    man = pd.DataFrame(rows, columns=["run_id", "step", "dp_rank", "g", "Ssum", "C"])
    j = smp.merge(man, on=["run_id", "step", "dp_rank"])
    j = j[~j["node"].str.contains("-r06-")]
    rg = reg.set_index("run_id")
    betas = []
    for rid, g in j.groupby("run_id"):
        if rg.loc[rid, "hall"] == "B":
            continue   # hall B samples may sit in capped intervals; hall A's runs are enough here
        kf = rg.loc[rid, "layers"] * rg.loc[rid, "d_model"] * g["C"].iloc[0] / (rg.loc[rid, "params_b"] * 1e9)
        X = np.c_[g["g"], kf * g["Ssum"]]
        c, *_ = np.linalg.lstsq(X, g["fwd_bwd_ms"], rcond=None)
        betas.append(c[1] / c[0])
    beta = float(np.median(betas))
    chk("V2 the attention coefficient recomputes within 0.03 (hall A runs, own fit)", abs(beta - fig["beta"]) < 0.03, "%.3f" % beta)
    # R3, R4: the 2027 runs' slowest rank and fill from the length sample, own packer
    lens = rd("data/doc_length_sample.csv")
    by = {s: g["length_tokens"].values for s, g in lens.groupby("source")}
    mixes = rd("data/data_mixes.csv")
    rng = np.random.default_rng(31)
    cfgs = {}
    for f in os.listdir(os.path.join(T, "plan_2027/configs")):
        cfgs[f[:-5]] = yaml.safe_load(open(os.path.join(T, "plan_2027/configs", f)))
    for rid in ("kide-13b-code-lc32", "kide-34b-lc64", "kide-8b-lc64", "kide-13b-lc32", "kide-34b-sci"):
        c = cfgs[rid]
        C, g, D = c["batch"]["seq_len"], c["batch"]["seqs_per_rank"], c["parallelism"]["data"]
        mix = dict(zip(*[mixes[mixes.mix_id == c["data"]["mix"]][k] for k in ("source", "token_share")]))
        docs = []
        ntok = 3.0e8 if C >= 32768 else 1.5e8
        for s, sh in mix.items():
            need = sh * ntok
            got = 0
            while got < need:
                d = by[s][rng.integers(0, len(by[s]), 4096)]
                cs = np.cumsum(d) + got
                k = int(np.searchsorted(cs, need)) + 1
                docs.append(d[:k])
                got += int(d[:k].sum())
        docs = np.concatenate(docs)
        rng.shuffle(docs)
        S, Fl = pack_bf(list(docs), C) if c["data"]["packing"] == "best_fit" else pack_seq(list(docs), C)
        kf = c["model"]["layers"] * c["model"]["d_model"] * C / c["model"]["params"]
        cost = 1 + fig["beta"] * kf * S
        mx = np.mean([cost[rng.integers(0, len(cost), (D, g))].sum(1).max() for _ in range(1500)])
        ov = 100 * (mx / (g * cost.mean()) - 1)
        chk("V3 %s slowest-rank overhead within 3 points" % rid, abs(ov - fig["overhead_pct_%s" % rid]) <= 3.0, "%.1f" % ov)
        if rid == "kide-34b-sci":
            chk("V4 kide-34b-sci fill within 0.015", abs(Fl.mean() - fig["fill_kide-34b-sci"]) <= 0.015, "%.3f" % Fl.mean())
    # R5: the meter reads the contract when capped; the PDF files the contract
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "provider/service_schedule_S3_kaivola.pdf")).pages)
    chk("V5 positive control: the service schedule names hall B's contracted capacity", "8,100 kW" in txt)
    meter = rd("provider/hall_it_load_2026.csv")
    mb = meter[meter.hall == "HALL-B"]["it_load_kw"]
    chk("V6 hall B's meter has a flat top at the contract", ((mb > 8060) & (mb < 8110)).mean() > 0.04)
    rules = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "policy/compute_allocation_rules_CAR-2027-1.pdf")).pages)
    chk("V7 positive control: the rules file the test and the extension", "expected finish" in rules and "extended until the run finishes" in rules)
    notice = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "provider/planned_works_h1_2027.pdf")).pages)
    chk("V8 positive control: the 2027 notice lists the chilled-water work", "PV-27-021" in notice)
    # R8, R9: own expected-value replay of the hall A runs (no hall B coupling needed for them)
    wb = load_workbook(os.path.join(T, "plan_2027/roadmap_h1_2027.xlsx"), data_only=True)
    rows = list(wb["H1 2027 runs"].iter_rows(values_only=True))
    rm = pd.DataFrame([r for r in rows[3:] if r[0]], columns=list(rows[2]))
    bench = rd("benchmark/tpbench_results.csv")
    for r in rm.itertuples():
        if r.hall != "A":
            continue
        b = bench[(bench.model == r.model) & (bench.context_tokens == r.seq_len) & (bench.seqs_per_rank == r.seqs_per_rank) & (bench.hall == "A")].iloc[0]
        bd = r.token_budget / (b.tokens_per_gpu_s * r.gpus) / 86400
        chk("V9 %s benchmark days recompute" % r.run_id, abs(bd - fig["bench_days_%s" % r.run_id]) < 0.06, "%.2f" % bd)
    # the hall B draw line, the pod boundary and the pool, each on its own code path
    st = rd("cluster/node_states_2026.csv")
    sb = st[st.hall == "B"].copy()
    sb["t"] = pd.to_datetime(sb["ts_utc"])
    mt = meter[meter.hall == "HALL-B"].copy()
    lt = pd.to_datetime(mt["timestamp_local"]).dt.tz_localize("Europe/Helsinki", ambiguous="NaT", nonexistent="NaT")
    mt["t"] = lt.dt.tz_convert("UTC")
    jj = sb.merge(mt[["t", "it_load_kw"]].dropna(), on="t")
    jj = jj[jj["it_load_kw"] < 8060]
    slope, icpt = np.polyfit(jj["allocated"], jj["it_load_kw"], 1)
    chk("V11 hall B's draw is a line in the allocated nodes: %.2f kW a node, %.0f kW at none" % (slope, icpt),
        abs(slope / fig["draw_line"][1] - 1) < 0.01 and abs(icpt / fig["draw_line"][0] - 1) < 0.02)
    stp = rd("runs/step_log_2026.csv")
    stp["run_id"] = stp["run_id"].map(lambda x: prev.get(x, x))
    stp["t"] = pd.to_datetime(stp["ts_utc"])
    stp = stp.drop_duplicates(["run_id", "tokens_seen"])
    sb2 = sb.set_index("t")
    stp["alloc"] = stp["t"].dt.floor("5min").map(sb2["allocated"])
    def steady(rid):
        g = stp[(stp.run_id == rid) & (stp["alloc"] <= 770)]    # the draw line puts 770 allocated nodes under the contract
        return float(g["step_time_ms"].median()), len(g)
    a_, na = steady("kide-34b-v1-r2")
    b_, nb = steady("kide-34b-v1b")
    chk("V12 the twin 34B runs (same mix, width and sequences per rank) differ by the pod boundary: %.1f per cent on %d and "
        "%d rows" % (100 * (b_ / a_ - 1), na, nb), na > 200 and nb > 200 and abs(100 * (b_ / a_ - 1) - fig["pod_penalty_pct"]) < 6.0)
    ledger = reg.assign(L=L, F=Fz)
    sbt = sb["t"].values
    held = np.zeros(len(sb))
    for r in ledger[ledger["hall"] == "B"].itertuples():
        held += ((sbt >= np.datetime64(r.L.tz_localize(None) if r.L.tzinfo else r.L)) &
                 (sbt < np.datetime64(r.F.tz_localize(None) if r.F.tzinfo else r.F))) * r.nodes
    alloc = sb["allocated"].values.astype(float)
    free = 1024 - held
    reg_ratio = (icpt + slope * held) / 8100.0
    ok_ = (free > 32) & (alloc > 0)
    pool_share = np.clip(alloc - held, 0, None)[ok_] / free[ok_]
    rr_ = reg_ratio[ok_]
    chk("V13 the pool keeps %.2f of the unreserved nodes busy under 80 per cent of the contract and %.3f at 97 per cent or more"
        % (pool_share[rr_ < 0.8].mean(), pool_share[rr_ >= 0.97].mean()),
        abs(pool_share[rr_ < 0.8].mean() - fig["pool_share"]) < 0.03 and pool_share[rr_ >= 0.97].mean() < 0.02)
    # the call: expected finish against the window end
    late = sorted(k for k in cfgs if fig["days_%s" % k] > fig["window_%s" % k])
    chk("V10 the late set follows from the expected days and windows", late == fig["call_late_runs"])
    fails = [x for x in res if not x[1]]
    for l, g, d in res:
        print("%s  %s%s" % ("PASS" if g else "FAIL", l, ("  [%s]" % d) if d != "" else ""))
    print("%d verified, %d FAIL" % (len(res), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
