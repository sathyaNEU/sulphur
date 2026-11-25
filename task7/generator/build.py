"""Build the pack: the world (core.py, replayed), what each of the cooperative's systems records, the data files, the
documents and the workbooks, each container through the house writers with its owner's stamps and its own save time.

    python3 task7/generator/build.py [--out <folder>]
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import common as CM  # noqa: E402
import docs  # noqa: E402
import paging  # noqa: E402
import params as P  # noqa: E402
import records as RC  # noqa: E402
import scada  # noqa: E402
import study  # noqa: E402
import world  # noqa: E402

F = CM.FILES
_E = {"scada": (2026, 10, 5, 8, 14, 22), "points": (2026, 10, 5, 8, 16, 40), "encoder": (2026, 10, 1, 7, 42, 10),
      "register": (2026, 10, 1, 10, 5, 51), "switching": (2026, 10, 2, 13, 21, 5), "rebates": (2026, 10, 1, 15, 47, 33),
      "permits": (2026, 10, 8, 9, 2, 18), "study_homes": (2026, 10, 14, 11, 30, 7), "study_assign": (2026, 10, 14, 11, 31, 42),
      "study_meters": (2026, 10, 14, 11, 44, 16), "index": (2026, 10, 2, 7, 3, 29), "tests": (2026, 10, 1, 10, 22, 48),
      "orders": (2026, 10, 1, 10, 31, 19), "amr": (2026, 10, 6, 16, 11, 2), "wh": (2026, 3, 20, 14, 40, 55)}
EXPORTED = {F[k]: dt.datetime(*v, tzinfo=P.CDT if v[1] > 3 else P.CST) for k, v in _E.items()}


def build(target, seed=P.SEED):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = world.build(seed)
    n = {}
    # the study homes first: their positions and feeders enter the feeder loads
    sx, sy, sfeed = study.place(W, CM.rng("study_homes"))
    W["study_feeder"] = sfeed
    S = scada.build(W, CM.rng("scada"))
    n["scada"] = CM.write_csv(os.path.join(target, F["scada"]), ["utc_time", "point", "kw"], scada.rows(S, W))
    n["points"] = CM.write_csv(os.path.join(target, F["points"]),
                               ["point", "description", "substation", "feeder", "district", "in_service", "retired"],
                               scada.point_rows(S, W))
    n["switching"] = CM.write_csv(os.path.join(target, F["switching"]),
                                  ["switch_order", "section", "from_feeder", "to_feeder", "transferred", "returned", "reason",
                                   "authorised_by"], scada.switching_rows(S, W, CM.rng("switching")))
    enc, addr = paging.encoder_rows(W, S, CM.rng("encoder"))
    n["encoder"] = CM.write_csv(os.path.join(target, F["encoder"]),
                                ["tx_time_local", "system", "address", "group", "command", "retry"], enc)
    n["index"] = CM.write_csv(os.path.join(target, F["index"]), ["date", "cooling_index"], paging.index_rows(S))
    # the premises and the member records
    rr = CM.rng("register")
    PR = RC.premises(W, rr, (sx, sy))
    inst = RC.install_dates(W, rr)
    codes, _ = CM.feeder_codes(W["dist"])
    reg, ser = RC.register(W, PR, inst, codes, rr)
    n["register"] = CM.write_csv(os.path.join(target, F["register"]),
                                 ["serial", "load_controlled", "premise_no", "old_premise_no", "service_address", "city", "district",
                                  "feeder", "grid_x_km", "grid_y_km", "receiver", "paging_group", "install_date", "status",
                                  "status_date"], reg)
    REP = RC.replacements(W, inst, CM.rng("rebates"))
    reb, per = RC.rebates_permits(W, PR, inst, REP, CM.rng("permits"))
    n["rebates"] = CM.write_csv(os.path.join(target, F["rebates"]),
                                ["rebate_no", "premise_no", "equipment", "equipment_installed", "paid", "amount_usd", "seer",
                                 "contractor"], reb)
    n["permits"] = CM.write_csv(os.path.join(target, F["permits"]),
                                ["permit_no", "issued", "site_address", "city", "work", "valuation_usd", "contractor", "status"],
                                per)
    n["tests"] = CM.write_csv(os.path.join(target, F["tests"]),
                              ["check_date", "serial", "premise_no", "check", "result", "note"],
                              RC.test_log(W, PR, inst, ser, CM.rng("tests")))
    wo, n_y, n_found = RC.orders(W, PR, inst, REP, CM.rng("orders"))
    n["orders"] = CM.write_csv(os.path.join(target, F["orders"]),
                               ["work_order", "visit_date", "premise_no", "reason", "lm_switch_on_site",
                                "ac_replaced_since_switch_installed", "lm_switch_found", "technician"], wo)
    n["amr"] = CM.write_csv(os.path.join(target, F["amr"]), ["premise_no", "meter_no", "read_date", "kwh", "read_type"],
                            RC.amr(W, PR, CM.rng("amr")))
    n["wh"] = CM.write_csv(os.path.join(target, F["wh"]),
                           ["date", "group", "morning_shed_start", "morning_shed_end", "evening_shed_start",
                            "evening_shed_end", "reason"], RC.wh_schedule(CM.rng("wh")))
    st_prem = [(PR["no"][W["n_s"] + h], PR["addr"][W["n_s"] + h]) for h in range(len(W["study"]["d"]))]
    sinfo = study.write(target, W, S["index"], st_prem, CM.rng("study_assign"))
    n["study_meters"] = sinfo["rows"]
    # documents and workbooks
    _, pruett_on = docs.sites_xlsx(os.path.join(target, F["sites"]), W)
    docs.outages_xlsx(os.path.join(target, F["outages"]), CM.rng("outages"))
    docs.plan_docx(os.path.join(target, F["plan"]))
    docs.report_pdf(os.path.join(target, F["report"]), report_counts(W, reg))
    docs.invoices_pdf(os.path.join(target, F["invoices"]), peaks(W, S))
    docs.coverage_png(os.path.join(target, F["map"]), W, pruett_on)
    postprocess.normalize_ooxml(os.path.join(target, F["sites"]), P.PEOPLE["radio"], P.PEOPLE["radio2"],
                                "2019-05-20T14:22:00Z", (pruett_on + dt.timedelta(3)).strftime("%Y-%m-%dT16:08:41Z"),
                                excel=True, company=P.ORG_SHORT)
    postprocess.normalize_ooxml(os.path.join(target, F["outages"]), P.PEOPLE["radio"], P.PEOPLE["radio2"],
                                "2026-01-06T15:41:00Z", "2026-10-02T19:56:13Z", excel=True, company=P.ORG_SHORT)
    postprocess.normalize_docx(os.path.join(target, F["plan"]), P.PEOPLE["energy"], P.PEOPLE["energy"],
                               "2026-10-27T15:05:00Z", "2026-11-12T22:47:00Z", revision=14, total_time=412, seed=P.SEED,
                               title="2027 Work Plan, Section 6: Load management", company=P.ORG_SHORT)
    mt = dict(EXPORTED)
    mt[F["map"]] = dt.datetime(pruett_on.year, pruett_on.month, pruett_on.day, 15, 2, 44, tzinfo=P.CDT) + dt.timedelta(days=9)
    postprocess.own_mtimes(target, mt)
    return dict(W=W, S=S, PR=PR, inst=inst, REP=REP, counts=n, orders_y=n_y, orders_found=n_found, study=sinfo,
                pruett_on=pruett_on, addr=addr)


def report_counts(W, reg):
    """The 2025 report's enrolment table, from the register as it stood at 31 December 2025."""
    ac = {d: 0 for d in P.DISTRICTS}
    wh = {d: 0 for d in P.DISTRICTS}
    new, removed = 0, 0
    for row in reg:
        inst = dt.date.fromisoformat(row[12])
        gone = dt.date.fromisoformat(row[14]) if row[14] else None
        if inst > dt.date(2025, 12, 31):
            continue
        active = gone is None or gone > dt.date(2025, 12, 31)
        if row[1].startswith("Central"):
            if active:
                ac[row[6]] += 1
                if inst.year == 2025:
                    new += 1
            elif gone.year == 2025:
                removed += 1
        elif active:
            wh[row[6]] += 1
    return dict(ac=ac, wh=wh, new=new, removed=removed)


def peaks(W, S):
    """The supplier's four summer coincident peaks: the hour, the cooperative's load in it (its feeders' breakers plus
    substation losses and station service, from the same historian), and that afternoon's index."""
    out = {}
    for e in P.PEAK_EVENTS:
        d = P.EVENT_DAYS[e]
        hb = P.PEAK_HOUR[e]
        m0 = (hb - 15) * 60
        kw = sum(float(S["series"][(d, f)][m0:m0 + 60].mean()) for f in range(W["n_feed"])) * 1.031 + 412.0
        out[d.month] = (d, hb + 1, kw, round(float(S["index"][d]), P.W_DEC))
    return out


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(out)
    print(r["counts"], "work orders Y:", r["orders_y"], "found:", r["orders_found"])
