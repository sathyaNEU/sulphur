"""The generator's assertions on the built pack and the world's own truth: the input gates, the golden against the
truth, the golden family and the perturbations, the factorial, the documents read back, mess and realism."""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as D  # noqa: E402
import obs as OB  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS, N = [], [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def pdf_text(p):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout)


def dup_identical():
    """every repeated (feeder, interval) in the customer-meter export repeats the same row"""
    seen = {}
    with open(os.path.join(TARGET, PK.FILES["ami"])) as fh:
        next(fh)
        for line in fh:
            k = tuple(line.split(",")[:2])
            if k in seen and seen[k] != line:
                return False
            seen[k] = line
    return True


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    names = sorted(n for n in os.listdir(TARGET) if not n.startswith("."))
    check("gate: ten or more usable files", len(names) >= 10, str(len(names)))
    check("gate: two or more file categories", len({n.rsplit(".", 1)[1] for n in names}) >= 2)
    rows = {n: sum(1 for _ in open(os.path.join(TARGET, n), encoding="utf-8")) - 1 for n in names if n.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, str(max(rows.values())))
    check("gate: a CSV of 10 to 20 printed pages or more", rows[PK.FILES["ltc"]] >= 550, str(rows[PK.FILES["ltc"]]))
    size = sum(os.path.getsize(os.path.join(TARGET, n)) for n in names)
    check("gate: the pack holds 30 MB or more", size >= 30e6, "%.0f MB" % (size / 1e6))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two or more distractors, named only in metadata", len(meta["distractor_files"]) >= 2 and all(d in names for d in meta["distractor_files"]))
    check("gate: no file name describes the data or names a distractor", not any(re.search(r"readme|dictionary|manifest|distractor", n, re.I) for n in names))
    # the world's truth
    w = W.build(P.SEED)
    ids = fig["ids"]
    truth_vc = {ids[f]: w.truth[f]["value"] / w.truth[f]["cost"] for f in range(P.NF)}
    tset = sorted(i for i, v in truth_vc.items() if v >= 1)
    check("truth: the golden funds the feeders the world's 2027 would justify", tset == sorted(fig["funded"]), str(tset))
    err = [fig["save_mwh"][ids[f]] / w.truth[f]["total_mwh"] - 1 for f in range(P.NF)]
    check("truth: golden savings within 5 percent of the world's on average", abs(np.mean(err)) < 0.05, "%+.3f" % np.mean(err))
    check("truth: no feeder's golden saving more than 15 percent off the world's", max(abs(e) for e in err) < 0.15, "%.3f" % max(abs(e) for e in err))
    check("truth: every feeder's value over cost 5 percent or more from the line", min(abs(v - 1) for v in truth_vc.values()) >= 0.05,
          "%.3f" % min(abs(v - 1) for v in truth_vc.values()))
    ce = [fig["cust_mwh"][ids[f]] / w.truth[f]["cust_mwh"] - 1 for f in range(P.NF)]
    check("truth: golden customer-meter savings within 5 percent of the world's on average", abs(np.mean(ce)) < 0.05, "%+.3f" % np.mean(ce))
    le = [abs(fig["loss_mwh"][ids[f]] + w.truth[f]["loss_mwh"]) for f in range(P.NF)]
    check("truth: golden loss rise within 15 MWh of the world's on every feeder", max(le) < 15, "%.1f" % max(le))
    check("golden: every feeder 5 percent or more from the line", min(abs(v - 1) for v in fig["value_ratio"].values()) >= 0.05)
    # the golden family, the perturbations, the factorial
    for m in E["forcing"]["golden_family"]:
        check("family files the golden set: %s" % m["name"][:60], sorted(m["answer"]) == sorted(fig["funded"]))
    for m in E["forcing"]["perturbations"]:
        check("perturbation holds: %s" % m["input"][:60], sorted(m["answer"]) == sorted(fig["funded"]))
    F = E["factorial"]
    nec = [j for j in F["judgments"] if j["kind"] == "stump" and sorted(j["dropped"]["answer"]) != sorted(fig["funded"])]
    suf = [j for j in F["judgments"] if j["kind"] == "stump" and sorted(j["alone"]["answer"]) == sorted(fig["funded"])]
    check("factorial: three stumps each necessary", len(nec) == 3, str(len(nec)))
    dist = {tuple(sorted(j["dropped"]["answer"])) for j in nec}
    check("factorial: the single drops land on three distinct wrong sets", len(dist) == 3, str(len(dist)))
    check("factorial: no stump sufficient alone", not suf)
    check("factorial: the reflex route misses the call", sorted(F["reflex_route"]["answer"]) != sorted(fig["funded"]))
    # the documents
    std = pdf_text(os.path.join(TARGET, D.FILES["std"]))
    check("doc: VO-1 files energy at the substation breaker, 115 V and the 4 percent cap",
          "substation breaker" in std and "115 V" in std and "4 percent" in std)
    allt = std + pdf_text(os.path.join(TARGET, D.FILES["proto"])) + pdf_text(os.path.join(TARGET, D.FILES["ar"]))
    check("doc: no document names a method (thermostat, give back, achieved, makeup, current squared, dose)",
          not re.search(r"thermostat|give.?back|achieved|make-?up|squared|dose|instrument|composition", allt, re.I))
    check("doc: the annual report carries the 6.1 percent loss rate", "6.1 percent" in allt)
    # the semantic forks, each closed by a filed sentence or by the golden family
    ar = pdf_text(os.path.join(TARGET, D.FILES["ar"]))
    fam = {m["name"]: sorted(m["answer"]) for m in E["forcing"]["golden_family"]}
    gold = sorted(fig["funded"])
    check("SF1 the saving is energy at the substation breaker", "delivered into the feeder at its substation breaker" in std)
    check("SF2 the comparison is normal running, the trial's ON days excluded", "ON days are not part of normal running" in std)
    check("SF3 the floor is 115 V hour by hour", "(115 V on the 120 V base) in that hour" in std)
    check("SF4 the cap is 4.8 V on the 120 V base", "4.8 V on the 120 V base" in std)
    check("SF5 the value is USD 48 a MWh times 9.4", "USD 48 per MWh" in std and "9.4" in std)
    check("SF6 feeder-head voltage is the bus or the pilot regulator's output", "pilot regulator's output where one is installed" in std)
    check("SF7 far-end voltage is the bellwethers' hourly minimum", "bellwether meters' hourly minimum readings" in std)
    check("SF8 heating draws filed by the load research, the ratio's rivals file the golden",
          bool(re.search(r"Electric resistance space heating [\d,]+ kWh", ar)) and bool(re.search(r"Heat pump space heating [\d,]+ kWh", ar)) and all(v == gold for k, v in fam.items() if "heat pump home" in k))
    check("SF9 the trial's weather terms without squares file the golden", fam["the trial's weather terms without squares"] == gold)
    check("SF10 re-sent rows are exact copies, dropped", PK.FILES["ami"] and dup_identical())
    check("SF11 water heating filed by the load research", bool(re.search(r"Electric water heater [\d,]+ kWh", ar)))
    check("SF12 the trial's control from every untested feeder files the golden",
          fam["the trial's control every untested feeder, not the same class"] == gold)
    check("SF13 the trial's scale as the mean of the trial feeders' ratios files the golden",
          fam["the trial's scale the mean of the trial feeders' ratios, not the median"] == gold)
    check("SF14 the loss fit with a no-load term files the golden", fam["the loss fit with a no-load term"] == gold)
    check("SF15 the average reduction is over the year's hours (the prompt's 'over the year')", "over the year" in open(os.path.join(TASK, "prompt.txt")).read())
    check("SF16 the loss change is a rise, positive when losses grow (the prompt's 'rise')", "rise in its own line losses" in open(os.path.join(TASK, "prompt.txt")).read())
    # mess and the read-back
    R = V.read_pack(TARGET)
    raw = sum(1 for _ in open(os.path.join(TARGET, PK.FILES["ami"]))) - 1
    check("mess: the customer-meter export carries re-sent rows", raw > P.NF * P.NQ, str(raw - P.NF * P.NQ))
    check("mess: estimated intervals flagged", sum(1 for r in open(os.path.join(TARGET, PK.FILES["ami"])) if r.rstrip().endswith(",E")) > 100)
    check("mess: bus SCADA has lost scans", sum(1 for r in open(os.path.join(TARGET, PK.FILES["bus"])) if r.rstrip().endswith(",")) > 50)
    check("mess: some ON days never ran (regulator in local mode)", any(
        (R.assign[f][R.trial_days] == 1).sum() > (R.dose_daily[f][R.trial_days] > 0.5).sum() for f in R.trial))
    check("realism: feeders differ in class mix", len(set(R.kind)) == 3)
    print("%d checks, %d FAIL" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
