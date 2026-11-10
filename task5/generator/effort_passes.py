"""task5 architecture 4: the effort test's passes, computed end to end on the cut pack.

Three complete estimates by named methods (methods.QUICK, methods.CAREFUL and the golden), each result's value as that
pass would file it, the hints executed literally on the careful pass, and each shortcut's designated set; written to
generator/effort.json for stumping/effort.py. Nothing here reads the prompt."""
import importlib.util
import json
import os

import golden as GD
import methods as M
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
EFFORT = os.path.join(HERE, "..", "..", ".claude", "skills", "stumping", "effort.py")


def pass_values(pk, G, route, quick=False):
    """one pass's value at every result: the same pipeline under the pass's route"""
    base = G["base"] if not quick else G["recon"]["published_county"].astype(float)
    X = pk.certify(route=route)
    s = GD.summary(pk, X, base)
    cz, rc = G["census"], G["recon"]
    out = {}
    if quick:
        # ten minutes: the register's active accounts, the reports on file, the published table as the base
        act = pk.a[(pk.a["account_status"] == "ACTIVE") & (pk.a["liab"] <= M.QEND[W.FLASH_Q])]
        got = pk.latest(W.FLASH_Q, M.CUT[W.FLASH_Q]).index.intersection(act.index)
        out["R1"] = dict(liable=len(act), received=len(got), outstanding=len(act) - len(got), published=rc["published"],
                         now=rc["now"], late_reports=None, accounts_since=None, amendments=None)
        out["R2"] = None
        out["R3"] = None
        out["R4"] = None
        out["R5"] = None
        out["R9"] = None
    else:
        out["R1"] = dict(liable=cz["liable"], received=cz["received"], outstanding=cz["outstanding"], published=rc["published"],
                         now=rc["now"], late_reports=rc["late_jobs"], accounts_since=rc["new_jobs"], amendments=rc["amend_jobs"])
        out["R2"] = dict(late_transmission=s["counts"]["batch"], missing_alone=s["counts"]["alone"],
                         late_every_quarter=s["counts"]["habit"], two_quarters=s["counts"]["twoq"],
                         new_account=s["counts"]["new"], missing_alone_keep=round(s["k_alone"], 2))
        rep = GD.summary(pk, pk.certify(route=dict(route, batch="reporters")), base)
        out["R3"] = int(round(rep["batch_jobs"] - s["batch_jobs"], -1))
        out["R4"] = dict(employers=int(round(s["unreg_n"], -1)) if s["unreg_n"] == s["unreg_n"] else None, jobs=GD.r100(s["unreg_jobs"]))
        cut = M.CUT[W.FLASH_Q]
        lat, _ = pk.to_counties(X["est"], W.FLASH_Q, cut, "latest")
        own, _ = pk.to_counties(X["est"], W.FLASH_Q, cut, X["route"]["sites"])
        d = lat - own
        out["R5"] = {W.NAMES[c]: int(round(d[c], -1)) for c in ("013", "023", "027", "003", "015")}
        R = pk.certify(q=W.BASE_Q, route=route)
        rd = (R["total"] / G["base"] - 1) * 100
        out["R9"] = dict(state_difference=round(float(100 * (R["total"].sum() / G["base"].sum() - 1)), 2),
                         mean_county_difference=round(float(rd.abs().mean()), 2))
    out["R6"] = {W.NAMES[c]: GD.r10(s["total"][c]) for c in W.CODES}
    out["R7"] = {W.NAMES[c]: GD.r1(s["change"][c]) for c in W.CODES}
    out["R8"] = [W.NAMES[c] for c in s["designated"]]
    return out


def results(G, figs):
    B = G["bands"]
    nb = lambda d: {W.NAMES[c]: [float(v[0]), float(v[1])] for c, v in d.items()}
    exact = lambda keys: {}
    return [
        dict(id="R1", name="the census at the cut-off and December 2025 against the published total", graded_as="Ask 6",
             figure="r1_census_and_reconciliation", depends=[], independent=""),
        dict(id="R2", name="the outstanding reports by cause, and what the missing-alone keep", graded_as="Component 4",
             figure="r2_outstanding_by_kind", depends=["R1"], independent="",
             bands=dict(late_transmission=list(B["n_batch"]), missing_alone=list(B["n_alone"]), late_every_quarter=list(B["n_habit"]),
                        two_quarters=list(B["n_twoq"]), new_account=list(B["n_new"]), missing_alone_keep=list(B["k_alone"]))),
        dict(id="R3", name="this quarter's trouble carried to the late transmissions (jobs)", graded_as="Component 1",
             figure="r3_late_transmission_jobs", depends=["R2"], independent="",
             band=[float(B["transport_jobs"][0]), float(B["transport_jobs"][1])], partly=[100.0, 800.0]),
        dict(id="R4", name="the employers with no account yet", graded_as="Component 2", figure="r4_unregistered", depends=[],
             independent="the register's liability and establishment dates",
             bands=dict(employers=list(B["unreg_n"]), jobs=list(B["unreg_jobs"]))),
        dict(id="R5", name="the worksite split against the latest reports' (jobs by county)", graded_as="Component 3",
             figure="r5_worksite_split", depends=[], independent="the worksite reports and their dates received",
             bands={W.NAMES[c]: [float(B["latest_minus_site"][c][0]), float(B["latest_minus_site"][c][1])] for c in ("013", "023", "027", "003", "015")}),
        dict(id="R6", name="each county's December 2026 jobs", graded_as="Ask 2", figure="r6_county_jobs",
             depends=["R2", "R3", "R4", "R5"], independent="", bands=nb(B["total"])),
        dict(id="R7", name="each county's change on December 2025", graded_as="Ask 4", figure="r7_changes",
             depends=["R6"], independent="", bands=nb(B["change"])),
        dict(id="R8", name="the counties to designate", graded_as="Recommendation", figure="r8_designated", depends=["R7"],
             independent=""),
        dict(id="R9", name="the replay on December 2025", graded_as="Ask 7", figure="r9_replay", depends=["R2", "R4", "R5"],
             independent="", bands=dict(state_difference=list(B["replay_state_diff"]), mean_county_difference=list(B["replay_mean_abs"]))),
    ]


HINTS = [
    ("More of a quarter's new employers get their account after the cut-off than by it, and the late ones are smaller.",
     dict(ibnr="develop")),
    ("An employer's worksites keep their own seasons, so the latest worksite report does not give December's split.",
     dict(sites="site")),
    ("Employers missing alone hold several times their usual share of the housing chain's jobs this quarter, in the late "
     "transmissions as in the ones that arrived.", dict(batch="transport")),
]


def write(task, pk, G, figs):
    spec = importlib.util.spec_from_file_location("effort", EFFORT)
    eff = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eff)
    res = results(G, figs)
    passes = {"quick": pass_values(pk, G, M.QUICK, quick=True), "careful": pass_values(pk, G, M.CAREFUL),
              "thorough": pass_values(pk, G, {})}
    for r in res:
        r["golden"] = figs[r["figure"]]
        r["passes"] = {p: passes[p][r["id"]] for p in ("quick", "careful", "thorough")}
    grade = lambda vals: {r["id"]: eff.grade(vals[r["id"]], r)[0] for r in res}
    g_care = grade(passes["careful"])
    hints = []
    for sentence, change in HINTS:
        gv = grade(pass_values(pk, G, dict(M.CAREFUL, **change)))
        hints.append(dict(sentence=sentence, rescues=[rid for rid in gv if gv[rid] == "right" and g_care[rid] != "right"]))
    routes = [dict(name="the golden", answer=figs["r8_designated"], golden=True)]
    for x in G["routes"]:
        routes.append(dict(name=x["name"], answer=[W.NAMES[c] for c in x["designated"]]))
    E = dict(results=res, hints=hints, routes=routes,
             passes_are=dict(quick="the register's active accounts, September carried for every outstanding report, the published "
                                   "table as the base, the latest worksite reports, no employer without an account",
                             careful="the outstanding reports read by cause and the missing-alone carried at the resolved quarters' "
                                     "share; the late transmissions at the reporting employers' change; last year's unregistered "
                                     "jobs carried as they were; the latest worksite reports' split; the same on the replay",
                             thorough="the golden"))
    json.dump(E, open(os.path.join(task, "generator", "effort.json"), "w"), indent=1, ensure_ascii=False)
    return E
