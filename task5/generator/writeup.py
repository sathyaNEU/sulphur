"""task5 architecture 3: figures.json and submission.md, every figure emitted from the golden and the rungs."""
import json
import os

import numpy as np

import methods as M
import world as W

RUNGS = {
    "R0": dict(missing="zero"),
    "R1": dict(classify="none", two_q="alive", seasonal=False),
    "R1x": dict(classify="none", two_q="zero", seasonal=False),
    "R2": dict(classify="filer", two_q="zero", seasonal=False),
    "R2b": dict(classify="newly", two_q="zero", seasonal=False),
    "R3a": dict(alone="latest"),
    "R3b": dict(alone="closed_dropped"),
    "Rseas": dict(seasonal=False),
}


def fmt_pc(x):
    v = round(x + 1e-9, 1)
    return ("%.1f" % v).replace("-", "minus ") if v < 0 else "%.1f" % v


def pc(x):
    v = round(x + 1e-9, 1)
    return "%.1f" % (v if v != 0 else 0.0)


def jobs(x):
    return "{:,}".format(int(round(x / 100.0)) * 100)


def figures(pk, G, n):
    f = {}
    f["designated"] = [W.NAMES[c] for c in G["designated"]]
    f["threshold"] = W.THRESHOLD
    f["line_pc"] = abs(W.THRESHOLD)
    f["fall_pc"] = {W.NAMES[c]: round(-G["change"][c] + 1e-9, 1) + 0.0 for c in G["designated"]}
    for c in W.CODES:
        k = W.NAMES[c]
        f["county." + k] = dict(base=int(round(G["base"][c] / 100.0)) * 100, reported=int(round(G["reported"][c] / 100.0)) * 100,
                                estimated=int(round(G["imputed"][c] / 100.0)) * 100, total=int(round(G["total"][c] / 100.0)) * 100,
                                change=round(G["change"][c] + 1e-9, 1) + 0.0, change_raw=G["change"][c])
    st = [sum(G[k].values()) for k in ("base", "reported", "imputed", "total")]
    f["state"] = dict(base=int(round(st[0] / 100.0)) * 100, reported=int(round(st[1] / 100.0)) * 100,
                      estimated=int(round(st[2] / 100.0)) * 100, total=int(round(st[3] / 100.0)) * 100,
                      change=round(100 * (st[3] / st[0] - 1) + 1e-9, 1))
    f["n_liable"], f["n_received"], f["n_missing"] = G["n_liable"], G["n_received"], G["n_missing"]
    f["kinds"] = {k: int(v) for k, v in G["counts"].items()}
    f["kind_jobs"] = {k: int(round(sum(v[1] for (c, kk), v in G["by_county_kind"].items() if kk == k) / 100.0)) * 100
                      for k in ("batch", "habitual", "alone", "two_q", "new") if f["kinds"].get(k)}
    f["kept"] = {"alone": round(G["ratios"]["('alone', 'all')"], 2), "two_q": round(G["ratios"]["('two_q', 'all')"], 3)}
    r_closed, _ = pk.outcomes(pk.closed)
    f["kept"]["batch"] = round(r_closed[("batch", "all")], 2)
    r_lat, _ = pk.outcomes(M.LATEST_QUARTERS)
    r_drop, _ = pk.outcomes(pk.closed, drop_never_filed=True)
    f["kept"]["alone_latest"] = round(r_lat[("alone", "all")], 2)
    f["kept"]["alone_dropped"] = round(r_drop[("alone", "all")], 2)
    v = pk.view(W.FLASH_Q)
    a = v["missing"]["arrived"].dropna()
    f["arrived_gap"] = [round(float(a[a < 0.5].max()), 2), round(float(a[a >= 0.5].min()), 2)]
    f["n_employer_rows"] = G.get("n_employer_rows")
    rungs = {}
    for k, rt in RUNGS.items():
        r = M.county_change(pk, rt)
        rungs[k] = dict(designated=[W.NAMES[c] for c in M.designated(r["change"])],
                        change={W.NAMES[c]: round(r["change"][c] + 1e-9, 1) for c in W.CODES},
                        change_raw={W.NAMES[c]: r["change"][c] for c in W.CODES},
                        estimated={W.NAMES[c]: int(round(r["imputed"][c] / 100.0)) * 100 for c in W.CODES})
    f["rungs"] = rungs
    return f


def submission(f):
    d = f["designated"]
    cty = lambda k: f["county." + k]
    gar, ost = cty("Garrow"), cty("Ostrom")
    r1x = f["rungs"]["R1x"]
    others = [W.NAMES[c] for c in W.CODES if W.NAMES[c] not in d]
    lowest_other = min(others, key=lambda k: cty(k)["change"])
    lines = []
    lines.append("## Tags\n")
    lines.append("**Domain:** Other, Survey Research & Official Statistics (census, register and administrative-data quality).  ")
    lines.append("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n")
    lines.append("## Final Recommendation\n")
    lines.append(("Certify Garrow and Ostrom for the 2027 Community Transition Fund: their December 2026 covered jobs are an "
                  "estimated %s and %s per cent below December 2025 once each outstanding report is read by whether its "
                  "usual transmission arrived, and no other county reaches the line (the lowest, %s, is at %s). The field's "
                  "imputation, carrying every outstanding employer's September jobs by its county's reporting employers, "
                  "designates no county (Garrow %s, Ostrom %s), because it keeps the jobs of employers missing from "
                  "transmissions that arrived, most of which had shed jobs or closed.")
                 % (pc(-gar["change"]), pc(-ost["change"]), lowest_other, pc(cty(lowest_other)["change"]),
                    pc(r1x["change"]["Garrow"]), pc(r1x["change"]["Ostrom"])))
    lines.append("")
    lines.append("## Supplementary Questions\n")
    lines.append("### ctf_certification_december_2026.xlsx\n")
    lines.append("1. The Certification sheet names the designated counties at the top, Garrow and Ostrom, under section 4 of the "
                 "Act, above a table with one row per county in county-code order: county code, county, December 2025 jobs, "
                 "December 2026 jobs from the reports received, December 2026 jobs estimated for employers whose report had "
                 "not arrived, December 2026 jobs, change on December 2025 (per cent) and designated, with a state row; jobs "
                 "are rounded to the nearest hundred.")
    rows = []
    for c in W.CODES:
        k = W.NAMES[c]
        x = cty(k)
        rows.append("%s %s" % (k, jobs(x["total"])))
    lines.append("2. December 2026 jobs: " + "; ".join(rows) + "; state %s." % jobs(f["state"]["total"]))
    rows = ["%s %s" % (W.NAMES[c], jobs(cty(W.NAMES[c])["estimated"])) for c in W.CODES]
    lines.append("3. Of those, estimated for employers whose report had not arrived: " + "; ".join(rows) +
                 "; state %s." % jobs(f["state"]["estimated"]))
    rows = ["%s %s" % (W.NAMES[c], pc(cty(W.NAMES[c])["change"])) for c in W.CODES]
    lines.append("4. Change on December 2025, per cent: " + "; ".join(rows) + "; state %s." % pc(f["state"]["change"]))
    lines.append("5. The chart is a column chart of the fourteen counties' changes with the minus 2.0 per cent line drawn "
                 "across it; Garrow (%s) and Ostrom (%s) are the only columns below the line." % (pc(gar["change"]), pc(ost["change"])))
    lines.append("")
    lines.append("### ctf_employer_jobs_december_2026.csv\n")
    k = f["kinds"]
    lines.append(("6. One row for each employer liable for the fourth quarter of 2026 and each county in which it has a "
                  "worksite, %s rows, with columns account_no, legal_name, county_code, county, report_received (Y or N), "
                  "december_2026_jobs (as reported or estimated, to one decimal) and basis. The %s "
                  "liable accounts are %s with a report received and %s without, of which %s are in a transmission that "
                  "had not arrived, %s report after the cutoff every quarter, %s are missing from a transmission that "
                  "arrived or late for the first time and %s have no third-quarter report either%s.")
                 % ("{:,}".format(f["n_employer_rows"]), "{:,}".format(f["n_liable"]), "{:,}".format(f["n_received"]),
                    "{:,}".format(f["n_missing"]), "{:,}".format(k["batch"]), "{:,}".format(k["habitual"]),
                    "{:,}".format(k["alone"]), "{:,}".format(k["two_q"]),
                    (", and %s are new employers" % "{:,}".format(k["new"])) if k.get("new") else ""))
    lines.append("")
    lines.append("## Critical Components\n")
    lines.append(("1. Of the **{:,}** reports outstanding at the cutoff, **{:,}** belong to employers whose usual "
                  "transmission (the reports received in the same second as theirs for the third quarter) had not arrived "
                  "either, and **{:,}** to employers missing from a transmission that arrived or late for the first time.")
                 .format(f["n_missing"], k["batch"], k["alone"]))
    lines.append(("2. On the quarters 2024Q1 to 2025Q3, whose outstanding employers have all since filed or been inactivated, "
                  "employers missing that way kept **%.2f** of their September jobs in December, against **%.2f** for "
                  "employers whose transmission was late.") % (f["kept"]["alone"], f["kept"]["batch"]))
    lines.append("3. Garrow's December 2026 covered jobs are an estimated **%s**, **%s per cent** on December 2025; Ostrom's "
                 "**%s**, **%s per cent**." % (jobs(gar["total"]), pc(gar["change"]), jobs(ost["total"]), pc(ost["change"])))
    lines.append("")
    lines.append("## Step-by-Step\n")
    lines.append(("1. Conformed ui_quarterly_reports_2023q1_2026q4.csv (the latest version of each report received by 15 "
                  "February 2027, a resubmission once), the liable accounts from ui_employer_accounts_2027-02-15.csv and "
                  "ui_account_status_history_2023-2027.csv (an account out from an inactivation, closure or transfer "
                  "effective by the quarter's first day) and ui_multiple_worksite_reports_2023q1_2026q4.csv for worksite "
                  "counties: {:,} liable accounts, {:,} reports received, {:,} outstanding.")
                 .format(f["n_liable"], f["n_received"], f["n_missing"]))
    lines.append("2. Took December 2025 from the closed fourth-quarter 2025 reports by worksite county: %s jobs statewide, "
                 "the same as covered_employment_by_county_2025q4.xlsx." % jobs(f["state"]["base"]))
    lines.append(("3. The shallow read: imputed every outstanding employer's December from its September 2026 jobs moved by "
                  "the reporting employers' change in its county and supersector, an employer missing two quarters as "
                  "ceased; no county falls 2.0 per cent (Garrow %s, Ostrom %s).") % (pc(r1x["change"]["Garrow"]), pc(r1x["change"]["Ostrom"])))
    lines.append(("4. Rebuilt the payroll agents' transmissions from received_at (three or more electronic reports in the "
                  "same second) and read each outstanding employer by whether its third-quarter transmission-mates had "
                  "reported (either none of them had or at least %.2f of them had), giving {:,} in late transmissions, "
                  "{:,} missing alone or late for the first time, {:,} late every quarter and {:,} with no third-quarter "
                  "report.").format(k["batch"], k["alone"], k["habitual"], k["two_q"])
                 % f["arrived_gap"][1])
    lines.append(("5. Measured what such employers turned out to have at the 2024Q1 to 2025Q3 cutoffs, each one resolved "
                  "since by a late report or an inactivation counted at nought: missing alone kept %.2f of September, a late "
                  "transmission %.2f, two quarters missing %.3f; the six months before the flash read %.2f because their "
                  "closures are not yet recorded, and dropping the employers that never filed reads %.2f.")
                 % (f["kept"]["alone"], f["kept"]["batch"], f["kept"]["two_q"], f["kept"]["alone_latest"], f["kept"]["alone_dropped"]))
    lines.append("6. Carried each outstanding employer at those shares, a seasonal lake resort at its own December-to-September "
                 "pattern" + (" and a new employer at the average of the quarter's new employers that reported." if k.get("new") else "."))
    lines.append(("7. Summed by worksite county: Garrow %s and Ostrom %s per cent, %s next at %s; designated Garrow and Ostrom.")
                 % (pc(gar["change"]), pc(ost["change"]), lowest_other, pc(cty(lowest_other)["change"])))
    lines.append("")
    r2, r3a, r3b, r0 = f["rungs"]["R2"], f["rungs"]["R3a"], f["rungs"]["R3b"], f["rungs"]["R0"]
    lines.append(("No other conclusion survives. Reading every outstanding report as if it had kept its September jobs "
                  "designates no county and is refuted by the closed quarters, where employers missing alone kept %.2f "
                  "of their September jobs. Taking every payroll agent's client as late with its agent designates %s, but Garrow's "
                  "missing employers are agent clients whose transmissions arrived. Reading their outcome from the latest "
                  "quarters (%s) or without the employers that never filed (%s) counts survivors only, because those "
                  "employers are closed and inactivated later. Counting only the reports received designates %s counties "
                  "and breaks section 2 of the Act, which counts every liable employer whether or not its report has arrived.")
                 % (f["kept"]["alone"], " and ".join(r2["designated"]) or "no county", ", ".join(r3a["designated"]) or "no county",
                    ", ".join(r3b["designated"]) or "no county", len(r0["designated"])))
    return "\n".join(lines) + "\n"


def write(task, w, T, pk, G, n):
    f = figures(pk, G, n)
    os.makedirs(os.path.join(task, "generator"), exist_ok=True)
    json.dump(f, open(os.path.join(task, "generator", "figures.json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(task, "submission.md"), "w").write(submission(f))
    return f
