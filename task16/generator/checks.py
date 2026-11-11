"""The generator's assertions: the input gates, the reconciliations, the golden against the simulated truth, the
rivals inside every band, the hurried routes outside where they are priced, each factor's footprint beyond the
families it decides, the margins at the line, and the conventions the fork table closes.
"""
import os
import re

import numpy as np

import analysis as AN
import golden as GD
import load as LD
import pack as PK
import params as P
import results as RS

RESULTS = []
FAM = P.FAM
NF, NC = len(FAM), 4


def ck(name, ok, detail=""):
    RESULTS.append((name, bool(ok), str(detail)))


def truth(W):
    """The world's own account: every follow-up, keyed or not, open or closed."""
    C = W["contacts"]; follow = W["follow"]; cons = W["cons"]; ph = W["phone"]
    ext = P.DAYS * 24.0
    open_w = set(c[0] for c in W["cases"] if c[0] >= 0 and c[5] >= ext)
    n = np.zeros((NF, NC)); u = np.zeros((NF, NC))
    calls = 0; unkeyed = 0; open_follow = 0
    last = {}
    for j, fl in follow.items():
        r = C[j]; d = r[5] / 24.0
        if not (P.V3_DAY <= d < P.ACHIEVED_END):
            continue
        ci = cons[r[0]][2]; n[r[3], ci] += 1
        if fl:
            u[r[3], ci] += 1
        for k in fl:
            if k not in last or C[last[k]][5] < r[5]:
                last[k] = j
    for k in last:
        if C[k][2] == "P":
            calls += 1; unkeyed += ph[k][0] != "KEYED"
        elif C[k][2] == "W" and k in open_w:
            open_follow += 1
    conv = np.zeros((NF, NC)); par = np.zeros(NC)
    N = W["N"]
    for j in follow:
        r = C[j]; dep, due, ci, _, _, al = cons[r[0]]
        if P.V3_DAY <= due < P.ACHIEVED_END and not al:
            conv[r[3], ci] += 1
    for t in range(P.V3_DAY, P.ACHIEVED_END):
        for i, dp in enumerate(P.DEPOTS):
            for ci in range(NC):
                if not (dp[0] in P.PILOT and t >= P.ALERT_DAY and ci in (1, 2)):
                    par[ci] += N[t, i, ci]
    Wc = np.zeros(NC)
    for pp, sv in zip(P.PEAK_PARCELS, P.PEAK_SERVICE):
        Wc += pp * 1000 * np.array(sv) / 100.0
    M = Wc * (conv / par) * np.array([1, 1 - P.ALERT_CUT, 1 - P.ALERT_CUT, 1.0])
    r = 1 - u / np.maximum(n, 1)
    return dict(achieved=100 * (1 - u.sum(axis=1) / n.sum(axis=1)), achieved_all=100 * (1 - u.sum() / n.sum()),
                expected=100 * (M * r).sum(axis=1) / M.sum(axis=1), expected_all=100 * (M * r).sum() / M.sum(),
                per_week=M.sum() / len(P.PEAK_PARCELS), late_share=100 * M[:, 1:].sum() / M.sum(),
                unkeyed_share=100 * unkeyed / calls, open_follow=open_follow, n=int(n.sum()))


def run(W, O, F, E, target, prompt_path):
    RESULTS.clear()
    G = O["golden"]; g = RS.figures(G); B = RS.BAND; T = truth(W)
    # ---- the input gates
    files = sorted(os.listdir(target))
    ck("ten or more usable files", len(files) >= 10, len(files))
    ck("two file categories (spreadsheet, text)", {os.path.splitext(f)[1] for f in files} >= {".csv", ".xlsx", ".docx"})
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    big = sorted(rows.values(), reverse=True)
    ck("a CSV of 20,000 rows or more", big[0] >= 20000, big[0])
    ck("a second long, messy CSV", big[1] >= 20000, big[1])
    ck("no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook", f, re.I) for f in files), files)
    ck("the distractors ship and the loader never opens them", all(PK.FILES[k] in files for k in PK.DISTRACTORS) and
       not any(('f["%s"]' % k) in open(LD.__file__).read() for k in PK.DISTRACTORS))
    # ---- mess is in the files and cleaned
    D = O["D"]
    ck("no conversation is in the assistant export twice", D["assistant_rows"] == D["assistant_distinct"])
    ck("call legs and callbacks are in the call export", D["call_rows"] - len(D["P"]) > 5000, D["call_rows"] - len(D["P"]))
    rc = G["recon"]
    ck("cleaned inbound calls equal telephony's weekly summary in every week and queue", rc["call_gap"] == 0 and rc["calls"] == rc["acd_calls"], rc)
    ck("customer cases in the extract plus the open ones equal the cases opened", rc["cases_closed"] + rc["cases_open_now"] == rc["cases_opened"], rc)
    # ---- the golden against the world's own account
    ck("the window's conversations are the world's", g["conversations"] == T["n"], (g["conversations"], T["n"]))
    ck("achieved rate, all families, within 0.8 of the truth", abs(g["achieved_all"] - T["achieved_all"]) <= 0.8, (g["achieved_all"], round(T["achieved_all"], 2)))
    ck("expected rate, all families, within 0.9 of the truth", abs(g["expected_all"] - T["expected_all"]) <= 0.9, (g["expected_all"], round(T["expected_all"], 2)))
    for i, k in enumerate(FAM):
        ck("achieved %s within its band of the truth" % k, abs(g["achieved"][k] - T["achieved"][i]) <= B["expected"][k] + 0.3, (g["achieved"][k], round(T["achieved"][i], 2)))
        ck("expected %s within its band of the truth" % k, abs(g["expected"][k] - T["expected"][i]) <= B["expected"][k], (g["expected"][k], round(T["expected"][i], 2)))
        ck("%s falls on the truth's side of the line" % k, (g["expected"][k] >= P.LINE) == (T["expected"][i] >= P.LINE))
    ck("unkeyed share of telephone follow-ups near the truth", abs(g["phone_unkeyed_share"] - T["unkeyed_share"]) <= 4.0, (g["phone_unkeyed_share"], round(T["unkeyed_share"], 1)))
    ck("open written follow-ups within a fifth of the truth", abs(g["written_open"] - T["open_follow"]) <= 0.2 * T["open_follow"], (g["written_open"], T["open_follow"]))
    ck("alerts' effect near the world's 42 per cent", abs(g["alert_effect"] - 100 * P.ALERT_CUT) <= 6, g["alert_effect"])
    ck("season conversations a week within 7 per cent of the truth", abs(g["per_week"] - T["per_week"]) <= 0.07 * T["per_week"], (g["per_week"], round(T["per_week"])))
    ck("late and exception share of season conversations within 3 points", abs(g["late_share"] - T["late_share"]) <= 3, (g["late_share"], round(T["late_share"], 1)))
    # ---- every sound rival inside every band
    for name, R in O["rivals"]:
        f = RS.figures(dict(R, boot=G["boot"]))
        bad = [k for k in RS.KEYS if RS.grade(f, g, k) != "right"]
        ck("rival inside every band: %s" % name, not bad, bad)
    for name, bt in O["boot_rivals"] + [("a third draw", O["boot_plain"])]:
        lo, hi = B["half_ratio"]
        r = [bt["half"][i] / g["half"][k] for i, k in enumerate(FAM)] + [bt["half_all"] / g["half_all"]]
        ck("range width stable under %s" % name, all(lo * 1.15 <= x <= hi / 1.15 for x in r), [round(x, 2) for x in r])
    # ---- the hurried routes
    gr = {name: {k: RS.grade(RS.figures(O[name]), g, k) for k in RS.KEYS} for name in RS.ROUTES}
    ck("the quick pass earns a third of the results or fewer", sum(v == "right" for v in gr["linked"].values()) <= 3, gr["linked"])
    c = gr["careful"]
    ck("the careful pass earns the linked record and both restorations", all(c[k] == "right" for k in ("linked", "phone", "written", "achieved")), c)
    ck("the careful pass loses the season, the alerts, the rates, the range and the set", all(c[k] != "right" for k in ("alerts", "season", "expected", "range", "call")), c)
    keep = {name: tuple(RS.figures(O[name])["call"]["keep"]) for name in RS.ROUTES}
    wrong = {v for v in keep.values() if v != tuple(g["call"]["keep"])}
    ck("the shortcuts land on four or more different wrong sets", len(wrong) >= 4, len(wrong))
    ck("the weeks carried forward keep Track and trace", "TRK" in keep["asis"] and "TRK" not in g["call"]["keep"])
    ck("the alerts left out hand back Delivery day and time", "DLV" not in keep["no_alerts"] and "DLV" in g["call"]["keep"])
    ck("unkeyed calls left out keep Missed delivery and redelivery", "RDL" in keep["no_phone"] and "RDL" not in g["call"]["keep"])
    ck("open cases left out keep Damaged parcel", "DMG" in keep["no_written"] and "DMG" not in g["call"]["keep"])
    for k in ("LST", "RET"):
        ck("%s is on the same side under every route (a family nothing decides)" % k, len({(k in v) for v in keep.values()}) == 1)
    # ---- margins at the line
    for k in FAM:
        ck("%s clear of the line by 2 points" % k, abs(g["expected"][k] - P.LINE) >= 2.0, g["expected"][k])
        ck("%s's range does not reach the line" % k, g["low"][k] > P.LINE or g["high"][k] < P.LINE, (g["low"][k], g["high"][k]))
    # ---- each factor's footprint beyond the families it decides
    cq = O["S"]["cq"]
    byq = cq.groupby("queue").apply(lambda d: (d.ivr_path == "BYPASS").mean())
    ck("the bypass runs in every telephone queue", (byq > 0.05).all(), byq.round(2).to_dict())
    wk = cq.groupby("week").keyed.mean()
    ck("a third or more of consignment calls unkeyed in every week", (wk < 0.75).all() and (wk > 0.30).all(), wk.round(2).tolist())
    ck("open cases in every case queue at the cut", all(sum(v for (q, d), v in O["S"]["open_qd"].items() if q == qq) > 0 for qq in P.CASE_QUEUES))
    cell = G["cell"]; n = G["n"]
    drop = [100 * (cell[i, 0] - cell[i, 2]) for i in range(NF) if n[i, 0] > 100 and n[i, 2] > 30]
    ck("late parcels resolve worse in every family with both kinds", len(drop) >= 8 and min(drop) > 3, [round(x, 1) for x in drop])
    es = G["es"]
    ck("the alerts cut contacts in both late classes", min(es.values()) > 0.25, {k: round(v, 2) for k, v in es.items()})
    d = G["diag"]
    ck("the daily rate moves more than independent conversations would", d["day_dispersion"] >= 2.0, round(d["day_dispersion"], 2))
    ck("late-parcel conversations resolve alike with and without alerts", abs(d["alerted_rate"] - d["unalerted_like_rate"]) <= 4.0, (round(d["alerted_rate"], 1), round(d["unalerted_like_rate"], 1)))
    tk = G["tick"]
    ck("the advisers' tick and the capture weights agree on unkeyed follow-ups", abs(tk["unkeyed_follow_tick"] - tk["unkeyed_follow_capture"]) <= 0.15 * tk["unkeyed_follow_capture"],
       (round(tk["unkeyed_follow_tick"]), round(tk["unkeyed_follow_capture"])))
    # ---- conventions the fork table closes (SF rows of the design note)
    from docx import Document
    A = O["S"]["A"]; w = O["S"]["win"]; S = O["S"]
    std = " ".join(p.text for p in Document(os.path.join(target, PK.FILES["standard"])).paragraphs)
    rel = " ".join(p.text for p in Document(os.path.join(target, PK.FILES["release"])).paragraphs)
    S2 = AN.prep(dict(D, A=D["A"].assign(end=D["A"].start)))
    S2["_g"] = AN.case_growth(S2, D)
    r2 = AN.run(S2, D, **RS.GOLD)
    d12 = max(abs(a - b) for a, b in zip(r2["expected"], G["expected"]))
    ck("SF1 seven days is 168 hours from the end (filed); counted from the start the rates agree within 0.6", "168 hours" in std and d12 <= 0.6, round(d12, 2))
    raw_chat = LD.pd.read_csv(os.path.join(target, PK.FILES["chat"]), dtype=str).fillna("")
    ck("SF2 any channel counts and a handed-over conversation is not resolved (filed); handovers are in the chat record",
       "through any contact channel" in std and "hands to an adviser" in std and (raw_chat.source == "assistant").sum() > 500, int((raw_chat.source == "assistant").sum()))
    raw_calls = LD.pd.read_csv(os.path.join(target, PK.FILES["calls"]), dtype=str).fillna("")
    ck("SF3 a transferred call is one contact (filed); second legs exist and the cleaned calls are one row a call",
       "transferred between advisers is one contact" in std and (raw_calls.leg == "2").sum() > 1000 and D["P"].call_id.is_unique, int((raw_calls.leg == "2").sum()))
    ck("SF4 callbacks and adviser-opened cases are not contacts (filed); both are in the files and out of the link",
       "are not contacts" in std and (raw_calls.direction == "OUT").sum() > 500 and (~D["K"].customer).sum() > 500 and set(D["P"].direction) == {"IN"},
       (int((raw_calls.direction == "OUT").sum()), int((~D["K"].customer).sum())))
    raw_a = LD.pd.read_csv(os.path.join(target, PK.FILES["assistant"]), dtype=str).fillna("")
    odd = (raw_a.tracking_no != "") & ~raw_a.tracking_no.str.fullmatch(r"QP\d{11}")
    ck("SF5 a consignment is identified by its tracking number; a sixth or more of typed numbers need bringing to one form and every one then matches a consignment",
       0.15 < odd.sum() / (raw_a.tracking_no != "").sum() < 0.30 and A.cls.notna().all(), round(float(odd.sum() / (raw_a.tracking_no != "").sum()), 3))
    ck("SF6 a rate covers conversations about a consignment that ended seven days before the cut (filed); those about none are in the export and out",
       "at least seven days before the data were cut" in std and "Contacts that concern no consignment are outside" in std and (raw_a.tracking_no == "").sum() > 5000
       and A.end[w].max() < P.ACHIEVED_END * 24.0 and A.end[w].min() >= P.V3_DAY * 24.0)
    b0 = w & (A.build == "3.0.0").values; b1 = w & (A.build == "3.0.1").values
    Ug = AN.weights(S, RS.GOLD["capture_how"], RS.GOLD["written"])[0]
    ck("SF7 version 3 is builds 3.0.0 and 3.0.1 (the release note: 3.0.1 changes no answers; 3.0 in service through peak)",
       set(A.build[w]) == {"3.0.0", "3.0.1"} and "no change to the answers" in rel and "stays in service through the peak season" in rel
       and abs((1 - Ug[b0].sum() / b0.sum()) - (1 - Ug[b1].sum() / b1.sum())) < 0.05, (int(b0.sum()), int(b1.sum())))
    ck("SF8 a conversation takes the family of its intent (filed)", "takes the family of its intent" in std and set(A.fam[w]) == set(FAM))
    fa = RS.figures(O["asis"]); fp = RS.figures(O["parcel_mix"])
    ck("SF9 the expected rate is a share of the season's conversations: October's mix and the parcel-weighted reading are other figures",
       "share of the assistant conversations" in std and "given the season plan" in std and fa["expected_all"] - g["expected_all"] > 3 and fp["expected_all"] - g["expected_all"] > 6,
       (g["expected_all"], fa["expected_all"], fp["expected_all"]))
    fn = RS.figures(O["no_alerts"])
    ck("SF10 the plan is taken as given, alerts included: every depot's alerts are live by 16 November and leaving them out moves the rate 2 points or more",
       "season plan is taken as given" in std.replace("  ", " ") and max(D["alerts_from"].values()) == 105 and g["expected_all"] - fn["expected_all"] >= 2.0, fn["expected_all"])
    ck("SF11 the rule is read on the expected rate; no family's range reaches the line, so the low end gives the same set",
       "is at least 75 per cent" in std and all(g["low"][k] > P.LINE or g["high"][k] < P.LINE for k in FAM))
    ck("SF12 the range is for what the record supports (filed)", "90 per cent range for what the record supports" in std and 0.5 < g["half_all"] < 3.0, g["half_all"])
    ck("SF13 delivery outcome is the consignment record's own class, the four the plan's service levels use",
       set(A.cls[w]) == set(P.CLASSES) and D["plan_service"].shape[1] == 4 and abs(D["plan_service"].sum(axis=1) - 1).max() < 0.011)
    ck("SF14 a call with no keyed number is still a contact (KS-07 2.1 and 5.1); leaving them out moves the rate achieved 2 points or more",
       "only where the caller keyed" in std and RS.figures(O["no_phone"])["achieved_all"] - g["achieved_all"] >= 2.0, RS.figures(O["no_phone"])["achieved_all"])
    ck("SF15 a written approach is a contact from receipt (KS-07 2.1 and 5.2); the extract and the backlog together are the cases opened",
       "when the case is closed" in std and rc["cases_closed"] + rc["cases_open_now"] == rc["cases_opened"])
    # ---- the effort contract
    by = {e["id"]: e for e in E["results"]}
    ck("every effort result carries its figures.json key", all(e["golden"] == F[e["figure"]] for e in E["results"]))
    ck("no single hint rescues more than three results", max(len(h["rescues"]) for h in E["hints"]) <= 3, [h["rescues"] for h in E["hints"]])
    ck("nine results in the chain", len(by) == 9)
    if os.path.exists(prompt_path):
        t = open(prompt_path, encoding="utf-8").read().strip()
        ck("the prompt is one paragraph under 1,000 characters", len(t) < 1000 and "\n" not in t, len(t))
        stems = [" ".join(x for x in re.split(r"[_\-]", os.path.splitext(v)[0]) if x.isalpha())[:40].lower() for v in PK.FILES.values()]
        ck("the prompt names no pack file", not any(st and len(st.split()) >= 2 and " ".join(st.split()[:2]) in t.lower() for st in stems), stems)
    return RESULTS
