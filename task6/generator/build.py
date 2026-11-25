"""Build task6: the evidence pack into <task>/target, the goldens into <task>/golden, submission.md, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task6/generator/build.py                everything
    python3 task6/generator/build.py --out DIR      the pack only, into DIR
    python3 task6/generator/build.py --golden-only  the goldens, figures, submission and metadata from the shipped
                                                    pack: target/ is unpacked from target.zip (never rebuilt), checked
                                                    member by member against it, the goldens built twice and compared
                                                    byte for byte, golden.zip cut; target.zip is left as shipped

The --golden-only path exists because a repair of the ask layer must not move the shipped pack: the pack's simulation
reads scipy's root finder and numpy's generators, and a later library build moves a handful of rows in the span export
and the July to December balancer file, so a rebuild in another environment is not the shipped cut."""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402
import zipfile       # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import pack as PK          # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
_U = __import__("datetime").timezone.utc
_T = lambda *a: __import__("datetime").datetime(*a, tzinfo=_U)
# each export's own save time, by the system that wrote it (the workbooks and documents carry their own stamps)
EXPORTED = {"spans": _T(2027, 1, 12, 10, 4, 37), "spanmetrics": _T(2027, 1, 12, 10, 11, 52),
            "lb_h1": _T(2026, 7, 2, 7, 40, 3), "lb_h2": _T(2027, 1, 2, 7, 41, 19),
            "incidents": _T(2027, 1, 4, 9, 2, 55), "timeline": _T(2027, 1, 4, 9, 3, 12),
            "status": _T(2027, 1, 4, 11, 27, 38), "billing": _T(2027, 1, 5, 8, 15, 4),
            "invoices": _T(2027, 1, 5, 8, 16, 47), "resources": _T(2027, 1, 5, 8, 18, 22),
            "deploys": _T(2027, 1, 4, 8, 12, 44), "rollouts": _T(2027, 1, 4, 8, 30, 9),
            "capacity": _T(2027, 1, 5, 14, 5, 51)}
GOLDEN_CSV_SAVED = _T(2027, 1, 8, 14, 52, 17)


def build_pack(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w, n, truths = PK.write_pack(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(p("slo"), K.PEOPLE["head"], K.PEOPLE["head"], "2025-11-20T10:12:00Z", "2025-12-09T16:41:00Z",
                       title="PR-SLO-3 Service level objectives for internal services")
    PP.normalize_ooxml(p("catalogue"), K.PEOPLE["sre"], K.PEOPLE["sre"], "2025-02-03T09:20:00Z",
                       "2026-12-18T11:05:00Z", excel=True)
    PP.normalize_ooxml(p("feedback"), "Customer Communications", "Customer Communications", "2027-01-05T08:44:00Z",
                       "2027-01-05T08:44:00Z", excel=True)
    PP.own_mtimes(out, {K.FILES[k]: v for k, v in EXPORTED.items()})
    return w, n, truths


def build_golden(target, golden):
    import analysis as A
    import deliver as D
    import writeup as WU
    G = A.Golden(target)
    R = G.run()
    F = D.figures(R)
    text, F = WU.write(R, F)
    # the critical components' own figures, as the blocks state them
    F["component1"] = {"first": F["start_order"][0], "payments": F["sli"]["payments"]}
    F["component3"] = {"places": F["sli"]["places"], "booking": F["sli"]["booking"]}
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    D.write_docx(os.path.join(golden, K.DOCX_OUT), R, F)
    D.write_csv(os.path.join(golden, K.CSV_OUT), R, F)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(os.path.join(golden, K.DOCX_OUT), K.PEOPLE["sre"], K.PEOPLE["head"], "2027-01-13T09:12:00Z",
                       "2027-01-14T15:26:00Z", title="Reliability review 2026: latency objectives")
    PP.own_mtimes(golden, {K.CSV_OUT: GOLDEN_CSV_SAVED})
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    write_effort(R, F, G)
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return R, F


def write_effort(R, F, G):
    """generator/effort.json: each result's golden (the figures.json value), its band, and what the quick, careful but
    hurried and thorough passes file, each pass's methods run end to end on the pack; the hints, each applied alone to
    the careful pass, with the results it rescues measured by effort.py's own grading; the routes; the stump
    factorial (each judgment dropped alone from the golden and fixed alone on the careful pass); and the forcing
    block (the golden family, the shortcuts, the perturbations)."""
    import importlib.util
    import checks as CK
    import deliver as D
    spec = importlib.util.spec_from_file_location("effort", os.path.join(
        os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping", "effort.py"))
    EF = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(EF)
    over, bud, L = F["over"], R["bud"], R["lattice"]
    bridged = F["bridged"]
    sli_bands = {s: [float(v) for v in F["sli_band"][s]] for s in bridged}

    def mins(M):
        return {s: ["%d" % D.whole(v) for v in M[s]] for s in K.SVC}

    def sli_cells(S):
        # a bridged SLI is graded on its range (two decimals filed), a boundary one at its one decimal
        return {s: (float(D.two(S[s]["sli"])) if s in bridged else "%.1f" % K.r1(S[s]["sli"])) for s in K.SVC}

    def comp1(S, P):
        return {"first": (P["order"] or ["none"])[0], "payments": "%.1f" % K.r1(S["payments"]["sli"])}

    def comp3(S):
        return {"places": float(D.two(S["places"]["sli"])), "booking": "%.1f" % K.r1(S["booking"]["sli"])}

    ci_bands = {}
    for s in over:
        lo, hi = float(D.two(R["ci"][s][0])), float(D.two(R["ci"][s][1]))
        ci_bands["%s lo" % s] = [round(lo - 0.06, 2), round(lo + 0.06, 2)]
        ci_bands["%s hi" % s] = [round(hi - 0.06, 2), round(hi + 0.06, 2)]

    def vals(r_, minutes):
        """Every result as one route files it."""
        return {"R1": mins(minutes), "R2": dict(r_["attribution"]), "R3": comp1(r_["S"], r_["P"]),
                "R4": comp3(r_["S"]), "R5": sli_cells(r_["S"]), "R6": D.ci_cells(r_["ci"], over),
                "R7": list(r_["P"]["over"]), "R8": D.programme_cells(r_["P"])}

    golden = {"attribution": R["attribution"], "S": R["S"], "P": R["P"], "ci": R["ci"]}
    V = {"quick": vals(R["quick"], R["quick"]["minutes"]),
         "careful": vals(L["S1+S2+S3"], R["minutes"]),
         "thorough": vals(golden, R["minutes"])}
    meta = [
        ("R1", "incident minutes by half", "Ask 4", "minutes", [], F["minutes"], None, None),
        ("R2", "root cause of each December incident", "Component 2", "root_cause", ["R1"], F["root_cause"], None,
         ["L26"]),
        ("R3", "the first to start and payments' SLI", "Component 1", "component1", ["R1"], F["component1"], None,
         ["L08"]),
        ("R4", "places' and booking's December SLI", "Component 3", "component3", ["R1"], F["component3"],
         {"places": sli_bands["places"]} if "places" in sli_bands else None, ["L34", "L44", "N27"]),
        ("R5", "every service's December SLI", "Ask 2", "sli", ["R2", "R3", "R4"], F["sli"], sli_bands,
         ["L08", "L34", "L26"]),
        ("R6", "the 90 per cent intervals", "Ask 1", "ci_cells", ["R5"], F["ci_cells"], ci_bands, ["L35"]),
        ("R7", "the services over budget", "Recommendation", "over", ["R5"], list(over), None, ["L08", "L34", "L26"]),
        ("R8", "start order, shares, together, beyond", "Ask 1", "programme_cells", ["R5", "R7"],
         F["programme_cells"], None, ["L08", "L34"]),
    ]
    res = []
    for rid, name, graded, fig, dep, gold, bands, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": fig, "depends": dep, "golden": gold,
             "passes": {p: V[p][rid] for p in ("quick", "careful", "thorough")}}
        if bands:
            r["bands"] = bands
        if prec:
            r["precedent"] = prec
        res.append(r)
    by_id = {r["id"]: r for r in res}
    grade = lambda rid, v: EF.grade(v, by_id[rid])[0]

    def lost(v):
        return [rid for rid in sorted(v) if grade(rid, v[rid]) != "right"]

    def rescued(v):
        return [rid for rid in sorted(v) if grade(rid, V["careful"][rid]) != "right" and grade(rid, v[rid]) == "right"]

    route_vals = {k: vals(L[k], R["minutes"]) for k in L}
    # the hints: what each one alone does to the careful pass (the lattice's pair routes)
    hints = [{"sentence": sentence, "rescues": rescued(route_vals[key])} for sentence, key in (
        ("each kept span counts at its trace root's hourly keep share", "S2+S3"),
        ("each December incident's cause is the named service whose own handling rose first, not the one furthest "
         "over its curve", "S1+S3"),
        ("the trace export begins on 12 December; the hours before it still count, and the tracing store's span "
         "metrics hold them", "S1+S2"))]
    # the routes: the services each tempting shortcut puts over budget, beside the golden's five
    names_ = {"S1": "Each service's own hourly count; causes dated; the hours before the export from the span metrics",
              "S2": "Each span at its trace root's keep share; each incident on the service furthest over its load "
                    "curve; the hours before the export from the span metrics",
              "S3": "Each span at its trace root's keep share; causes dated; the export's hours alone",
              "S1+S2": "Each service's own hourly count; each incident on the service furthest over its load curve; "
                       "the hours before the export from the span metrics",
              "S1+S3": "Each service's own hourly count; causes dated; the export's hours alone",
              "S2+S3": "Each span at its trace root's keep share; each incident on the service furthest over its load "
                       "curve; the export's hours alone",
              "S1+S2+S3": "Each service's own hourly count; each incident on the service furthest over its load curve; "
                          "the export's hours alone (the careful but hurried pass)"}
    over_of = lambda S: [s for s in K.SVC if K.r1(S[s]["sli"]) > bud[s]]
    routes = [{"name": "Kept spans unweighted; each incident on the service named first; the export's hours alone",
               "answer": list(R["quick"]["P"]["over"]), "golden": False}]
    routes += [{"name": names_[k], "answer": list(L[k]["P"]["over"]), "golden": False} for k in names_]
    routes += [{"name": "The review's weights and causes; the threshold's bucket split by straight-line interpolation "
                        "(the list holds, the SLIs do not)", "answer": over_of(R["naive"]["linear"]), "golden": False},
               {"name": "The review's weights and causes; the hours before the export at the export's own share, no "
                        "span metrics read", "answer": over_of(R["loadfill"]["flat"]), "golden": False},
               {"name": "Each span at its trace root's keep share; causes dated; the hours before the export from the "
                        "span metrics (this review)", "answer": list(over), "golden": True}]
    # the stump factorial: each judgment made the hurried way alone, and fixed alone on the careful pass
    factorial = {"golden_answer": list(over), "reflex_route": {"answer": list(L["S1+S2+S3"]["P"]["over"])},
                 "judgments": []}
    for jid, name, prec, drop, alone in (
            ("J1", "each kept span weighted by its trace root's hourly keep share, not its own service's count",
             ["L08"], "S1", "S2+S3"),
            ("J2", "each December incident's cause dated by the earliest sustained rise of own handling over load",
             ["L26"], "S2", "S1+S3"),
            ("J3", "the hours before the export counted from the tracing store's span metrics, the threshold's bucket "
                   "split as the held spans show", ["L34", "N27"], "S3", "S1+S2")):
        factorial["judgments"].append({
            "id": jid, "name": name, "kind": "stump", "precedent": prec,
            "dropped": {"answer": list(L[drop]["P"]["over"]), "results_moved": lost(route_vals[drop])},
            "alone": {"answer": list(L[alone]["P"]["over"]), "results_rescued": rescued(route_vals[alone])}})
    # forcing, both sides: every split of the threshold's bucket and every weighting base on the golden's list, the
    # shortcuts off it, and the bridge's one fitted input (the split shares) moved either way
    incs = R["incidents"]
    att = R["attribution"]
    wr = G.weights("root")
    ex = G.excluded(att, incs)
    fam = [{"name": "the threshold's bucket split by %s" % k, "answer": over_of(S_)} for k, S_ in R["family"].items()]
    fam += [{"name": k, "answer": over_of(S_)} for k, S_ in CK.weight_variants(G, att, incs).items()]
    pert = [{"input": "the threshold's bucket split by %s" % {"linear": "straight-line interpolation",
                                                              "loglinear": "interpolation on the log scale",
                                                              "lower": "nothing over the threshold (its lower bound)",
                                                              "upper": "everything over the threshold (its upper "
                                                                       "bound)"}[k], "answer": over_of(R["naive"][k])}
            for k in A_NAIVE]
    for f_, lab in ((1.2, "+20%"), (0.8, "-20%")):
        pert.append({"input": "every split share %s" % lab,
                     "answer": over_of(G.slis(wr, ex, fill=CK.scaled_fill(G, wr, ex, incs, f_)))})
    forcing = {"kind": "set", "golden_answer": list(over), "golden_family": fam,
               "shortcuts": [{"name": names_[k], "answer": list(L[k]["P"]["over"])} for k in names_],
               "perturbations": pert}
    with open(os.path.join(HERE, "effort.json"), "w") as fh:
        json.dump({"results": res, "hints": hints, "routes": routes, "factorial": factorial, "forcing": forcing}, fh,
                  indent=1, sort_keys=True)
        fh.write("\n")


A_NAIVE = ("linear", "loglinear", "lower", "upper")


def write_metadata(n, R):
    if n is None:                      # the shipped pack: its row counts stand as recorded
        old = json.load(open(os.path.join(TASK, "metadata.json")))
        n = {K.FILES_KEY_OF[f]: c for f, c in old["rows"]}
    synth = ("constructed by the task generator (seeded); Rotalinha, its services, staff, systems and every record are "
             "fictional")
    about = {
        "spans": ("the tracing store's export of the December 2026 spans it still held", "2027-01-12"),
        "spanmetrics": ("the tracing store's span metrics for December 2026: the spans it ingested each hour and "
                        "their duration histogram, by service, span name, kind and status", "2027-01-12"),
        "lb_h1": ("the load balancer's hourly request counts by target group, January to June 2026", "2026-07-02"),
        "lb_h2": ("the load balancer's hourly request and 5xx counts by target group, July to December 2026",
                  "2027-01-02"),
        "slo": ("PR-SLO-3, the platform's service level objectives standard, version 3.1", "2025-12-09"),
        "catalogue": ("the platform's service catalogue", "2026-12-18"),
        "incidents": ("the incident tool's export of 2026 incidents", "2027-01-04"),
        "timeline": ("the incident tool's timeline events for 2026 incidents", "2027-01-04"),
        "status": ("the public status page's 2026 history as its provider exports it", "2027-01-04"),
        "billing": ("the cloud provider's 2026 billing lines", "2027-01-05"),
        "invoices": ("the cloud provider's 2026 invoices", "2027-01-05"),
        "resources": ("the cloud provider's inventory of resources that ran in 2026", "2027-01-05"),
        "deploys": ("the delivery pipeline's 2026 deployment log", "2027-01-04"),
        "rollouts": ("the production cluster's rollout history", "2027-01-04"),
        "capacity": ("Platform Infrastructure's Q4 2026 capacity review", "2027-01-05"),
        "feedback": ("app store reviews of the Rotalinha app, July to December 2026", "2027-01-05"),
    }
    prov = {}
    for k, fn in K.FILES.items():
        prov[fn] = {"source": synth, "covers": about[k][0], "date": about[k][1],
                    "licence": "CC0 1.0 (constructed for this task)",
                    "made": "generated by task6/generator from its seeded records"}
    m = {"task": "task6", "as_of": "2027-01-14",
         "title": "Rotalinha: the internal services that ran over their 2026 latency error budget",
         "domain": "General Statistics & Data Science",
         "objective": "Descriptive & Distribution Analysis",
         "decision": "which internal services ran over their 2026 latency error budget and get a reliability engineer "
                     "for the first half of 2027",
         "answer": ", ".join(R["P"]["over"]),
         "deliverables": [K.DOCX_OUT, K.CSV_OUT],
         "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
         "rows": sorted([(K.FILES["spans"], n["spans"]), (K.FILES["lb_h1"], n["lb_h1"]), (K.FILES["lb_h2"], n["lb_h2"])]
                        + ([(K.FILES["spanmetrics"], n["spanmetrics"])] if "spanmetrics" in n else [])),
         "provenance": prov}
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(m, f, indent=1)
        f.write("\n")


def cut_golden_zip(golden, path):
    if os.path.exists(path):
        os.remove(path)
    PP.zip_folder(golden, path, zone="Europe/Lisbon")


def unpack_shipped(target):
    """target/ from the shipped target.zip, every member compared with the file on disk."""
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp) as z:
        names = [n_ for n_ in z.namelist() if not n_.endswith("/")]
        if not os.path.isdir(target) or sorted(os.listdir(target)) != sorted(n_.split("/", 1)[1] for n_ in names):
            if os.path.exists(target):
                shutil.rmtree(target)
            z.extractall(TASK)
        bad = [n_ for n_ in names if hashlib.md5(z.read(n_)).hexdigest() !=
               hashlib.md5(open(os.path.join(TASK, n_), "rb").read()).hexdigest()]
    return hashlib.md5(open(zp, "rb").read()).hexdigest(), bad


def golden_only():
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    zmd5, bad = unpack_shipped(target)
    print("shipped pack: target.zip md5 %s, %s" % (zmd5, "every member matches target/" if not bad else
                                                   "MEMBERS DIFFER " + ", ".join(bad)))
    R, F = build_golden(target, golden)
    write_metadata(None, R)
    import checks
    rc = checks.main(target)
    import verify
    vbad = verify.run(TASK)
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    first = digest(golden)
    fig1 = open(os.path.join(HERE, "figures.json"), "rb").read()
    sub1 = open(os.path.join(TASK, "submission.md"), "rb").read()
    build_golden(target, golden)
    same = digest(golden) == first and open(os.path.join(HERE, "figures.json"), "rb").read() == fig1 and \
        open(os.path.join(TASK, "submission.md"), "rb").read() == sub1
    print("golden rebuild: %s" % ("byte-identical" if same else "DIFFERS"))
    cut_golden_zip(golden, os.path.join(TASK, "golden.zip"))
    for k, v in sorted(digest(golden).items()):
        print("  %s  golden/%s" % (v, k))
    print("  %s  golden.zip" % hashlib.md5(open(os.path.join(TASK, "golden.zip"), "rb").read()).hexdigest())
    sys.exit(1 if (rc or vbad or bad or not same) else 0)


def digest(d):
    out = {}
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(root, f)
            out[os.path.relpath(p, d)] = hashlib.md5(open(p, "rb").read()).hexdigest()
    return out


def cut_zip(target, path):
    if os.path.exists(path):
        os.remove(path)
    PP.zip_folder(target, path, prefix="target/", zone="Europe/Lisbon")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--golden-only", action="store_true")
    a = ap.parse_args()
    if a.golden_only:
        golden_only()
        return
    if a.out:
        build_pack(a.out)
        return
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    w, n, truths = build_pack(target)
    R, F = build_golden(target, golden)
    write_metadata(n, R)
    import checks
    rc = checks.main(target)
    import verify
    vbad = verify.run(TASK)
    print("verify: %s" % ("PASS" if not vbad else "FAIL " + "; ".join(vbad)))
    same = True
    if not a.no_rebuild:
        scratch = os.path.join(TASK, ".rebuild")
        build_pack(os.path.join(scratch, "target"))
        a1, a2 = digest(target), digest(os.path.join(scratch, "target"))
        shutil.rmtree(scratch)
        same = a1 == a2
        print("rebuild: %s" % ("byte-identical" if same else "DIFFERS " + ", ".join(k for k in a1 if a1[k] != a2.get(k))))
    cut_zip(target, os.path.join(TASK, "target.zip"))
    cut_golden_zip(golden, os.path.join(TASK, "golden.zip"))
    for k, v in sorted(digest(target).items()):
        print("  %s  %s" % (v, k))
    sys.exit(1 if (rc or vbad or not same) else 0)


if __name__ == "__main__":
    main()
