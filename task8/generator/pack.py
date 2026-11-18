"""Write the boards' exports under target/ in each board's own layout, the national registers, the regulator's
review marks and the three files the analysis does not use. Three systems are in use: the bureau system (Carrow,
Ardkeel, Dunmoyle), the assessment suite (Brannock, Fennor: one row per sample, marks in delimited fields) and the
office workbooks (Eskerry, Gortavale)."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import core as C
import world as WL

YEARS = C.YEARS
PSEED = 5512027
TRADES = ["Carpentry and Joinery", "Electrical", "Plumbing", "Motor Mechanics", "Metal Fabrication", "Brick and Stonelaying",
          "Plastering", "Painting and Decorating"]
AGES = ["16-18", "19-24", "25 and over"]
FILES = {"register": "moderator_register_2020_2026.csv", "centres": "centre_register.csv",
         "review": "oer_review_2023_dunmoyle_portfolio_marks.csv",
         "enquiries": "enquiries_about_results_2019_2026.csv", "visits": "centre_approval_visits_2022_2026.xlsx",
         "entries": "entries_by_trade_and_age_2012_2026.csv"}


def names_for(b):
    info = WL.INFO[b]
    lo, code = b.lower(), info["code"]
    if info["layout"] == 1:
        return dict(marks="%s_portfolio_marksheets_2012_2026.csv" % lo, samples="%s_moderation_samples.csv" % lo,
                    outcomes="%s_moderation_outcomes.csv" % lo, scripts="%s_standardisation_scripts.csv" % lo,
                    trial="%s_standardisation_marks.csv" % lo)
    if info["layout"] == 2:
        return dict(marks="%s_PortfolioMarks_2012-2026.csv" % code, samples="%s_ModerationSamples.csv" % code,
                    scripts="%s_StdMeetingScripts.csv" % code, trial="%s_StdMeetingMarks.csv" % code)
    return dict(marks="%s EB portfolio marks 2012-2026.csv" % b, samples="%s EB moderation samples.csv" % b,
                outcomes="%s EB moderation outcomes.xlsx" % b, scripts="%s EB standardisation scripts.xlsx" % b,
                trial="%s EB standardisation marks.csv" % b)


for _b in WL.BOARDS:
    for _k, _v in names_for(_b).items():
        FILES["%s_%s" % (_b, _k)] = _v


def cno(b, own):
    """A centre's number in its board's own scheme."""
    lay = WL.INFO[b]["layout"]
    if lay == 1:
        return "%s%04d" % (b[0], own)
    if lay == 2:
        return str(own)
    return "%s-%d" % (b[0], own)


def mref(WD, b, pid, y):
    p = WD["people"][pid]
    return p["code"][b] if y < WL.REG_FROM else p["reg"]


def series(b, y):
    return "June %d" % y if WL.INFO[b]["layout"] == 3 else str(y)


def datestr(b, d):
    lay = WL.INFO[b]["layout"]
    return d.isoformat() if lay == 1 else (d.strftime("%Y%m%d") if lay == 2 else d.strftime("%d/%m/%Y"))


def put(path, header, lines, sep=","):
    with open(path, "w", newline="") as f:
        f.write(sep.join(header) + "\r\n")
        f.write("\r\n".join(lines))
        f.write("\r\n")


def sheet(path, title, header, rows, widths):
    wb = Workbook()
    ws = wb.active
    ws.title = title
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for i, wd in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wd
    ws.freeze_panes = "A2"
    wb.save(path)


def q(s):
    return '"%s"' % s if ("," in s or " " in s) else s


def build(WD, target):
    rng = np.random.default_rng(PSEED)
    counts = {}
    enq, entries = [], []
    for b in WL.BOARDS:
        B, info, F = WD["boards"][b], WL.INFO[b], names_for(b)
        lay, cen = info["layout"], B["cen"]
        sep = ";" if lay == 2 else ","
        # ---- portfolio mark sheets
        lines, per_series = [], {}
        for (ti, c, seqno, status, marks, adj) in B["cand"]:
            y = YEARS[ti]
            cn, sr = cno(b, cen["own"][c]), series(b, y)
            per_series[y] = per_series.get(y, 0) + len(seqno)
            for s_, st, m in zip(seqno.tolist(), status.tolist(), marks.tolist()):
                if lay == 1:
                    cm, am = ("", "") if st else (str(m), str(m - adj))
                    lines.append("%s,%s,%04d,%s,%s,%s" % (sr, cn, s_, "MWA"[st], cm, am))
                elif lay == 2:
                    cm, am = ("", "") if st else (str(m), str(m - adj))
                    lines.append("%s;%s;%d;%s;%s;%s" % (sr, cn, s_, ("OK", "WD", "ABS")[st], cm, am))
                else:
                    cm, am = ("", "") if st else (str(m), str(m - adj))
                    lines.append("%s,%s,%d,%s,%s,%s" % (sr, cn, s_, ("Marked", "Withdrawn", "Absent")[st], cm, am))
        if b == "Fennor":                       # a batch the suite loaded twice
            k = int(rng.integers(60000, 90000))
            lines += lines[k:k + 173]
        head = {1: ["series", "centre_no", "candidate_no", "entry_status", "centre_mark", "awarded_mark"],
                2: ["Series", "Centre", "CandNo", "Status", "CentreMark", "FinalMark"],
                3: ["Series", "Centre No", "Cand No", "Status", "Centre Mark", "Awarded Mark"]}[lay]
        put(os.path.join(target, F["marks"]), head, lines, sep)
        counts[F["marks"]] = len(lines)
        for y, n in per_series.items():
            shares = rng.dirichlet(np.full(len(TRADES) * len(AGES), 6.0))
            cells = np.floor(shares * n).astype(int)
            cells[0] += n - cells.sum()
            for i, v in enumerate(cells):
                entries.append((b, y, TRADES[i // len(AGES)], AGES[i % len(AGES)], int(v)))
        # ---- moderation: the sample marks and the outcome records
        rec = 1000 + int(rng.integers(0, 400))
        s_lines, o_rows = [], []
        for (ti, c, seqnos, cm, mm, mid), (_, _, _, ns, md, adj) in zip(B["samp"], B["outc"]):
            y = YEARS[ti]
            cn, sr, ref = cno(b, cen["own"][c]), series(b, y), mref(WD, b, mid, y)
            issued = dt.date(y, 6, 20) + dt.timedelta(days=int(rng.integers(0, 36)))
            outcome, applied = ("Adjusted", -adj) if adj else ("Confirmed", 0)
            versions = [(ref, ns, issued)]
            if rng.random() < 0.015:            # a record keyed wrongly and reissued after an enquiry
                later = issued + dt.timedelta(days=int(rng.integers(55, 130)))
                team = [p for p in WD["team"][b][y] if p[0] != mid]
                if rng.random() < 0.5:
                    wrong = (mref(WD, b, team[int(rng.integers(len(team)))][0], y), ns, issued)
                else:
                    wrong = (ref, ns + int(rng.choice([-2, -1, 1, 2])), issued)
                versions = [wrong, (ref, ns, later)]
                enq.append((b, y, int(cen["nat"][c]), later - dt.timedelta(days=int(rng.integers(20, 40))),
                            "Clerical check of moderation record", "Record reissued"))
            if lay == 1:
                for s_, a_, m_ in zip(seqnos.tolist(), cm.tolist(), mm.tolist()):
                    s_lines.append("%s,%s,%04d,%d,%d,%s" % (sr, cn, s_, a_, m_, ref))
            elif lay == 3:
                for s_, a_, m_ in zip(seqnos.tolist(), cm.tolist(), mm.tolist()):
                    s_lines.append("%s,%s,%d,%d,%d,%s" % (sr, cn, s_, a_, m_, ref))
            for vi, (r_, n_, d_) in enumerate(versions):
                rec += 1 + int(rng.integers(0, 3))
                if lay == 1:
                    o_rows.append("%d,%s,%s,%s,%d,%.2f,%s,%d,%s" % (rec, sr, cn, r_, n_, md, outcome, applied, datestr(b, d_)))
                elif lay == 2:
                    s_lines.append(";".join([sr, str(int(cen["nat"][c])), r_, str(n_), "|".join(map(str, seqnos.tolist())),
                                             "|".join(map(str, cm.tolist())), "|".join(map(str, mm.tolist())),
                                             "ADJ" if adj else "CONF", str(applied), datestr(b, d_), str(vi + 1)]))
                else:
                    o_rows.append([rec, sr, cn, r_, n_, round(md, 2), outcome, applied, datestr(b, d_)])
        if lay == 1:
            put(os.path.join(target, F["samples"]), ["series", "centre_no", "candidate_no", "centre_mark", "moderator_mark",
                                                     "moderator_ref"], s_lines)
            put(os.path.join(target, F["outcomes"]), ["record_no", "series", "centre_no", "moderator_ref", "portfolios_sampled",
                                                      "mean_difference", "outcome", "adjustment_marks", "issued"], o_rows)
            counts[F["outcomes"]] = len(o_rows)
        elif lay == 2:
            put(os.path.join(target, F["samples"]), ["Series", "RollNo", "Moderator", "Sampled", "Candidates", "CentreMarks",
                                                     "ModeratorMarks", "Outcome", "MarksApplied", "ReportDate", "Version"],
                s_lines, sep)
        else:
            put(os.path.join(target, F["samples"]), ["Series", "Centre No", "Cand No", "Centre Mark", "Moderator Mark",
                                                     "Moderator"], s_lines)
            sheet(os.path.join(target, F["outcomes"]), "Outcomes",
                  ["Record", "Series", "Centre No", "Moderator", "Portfolios", "Mean difference", "Outcome",
                   "Marks applied", "Issued"], o_rows, [9, 11, 11, 12, 10, 15, 11, 13, 12])
            counts[F["outcomes"]] = len(o_rows)
        counts[F["samples"]] = len(s_lines)
        # ---- the standardisation meetings: the scripts and the marks given before the meeting
        sc_rows, t_lines = [], []
        for y, T in sorted(B["trial"].items()):
            sr = series(b, y)
            for k, ((sti, sc, sseq, _), ag) in enumerate(zip(T["src"], T["agreed"].tolist())):
                sno = "%s%02d/%02d" % (info["code"][0], y % 100, k + 1)
                ssr, scn = series(b, YEARS[sti]), cno(b, cen["own"][sc])
                if lay == 1:
                    sc_rows.append("%s,%s,%s,%s,%04d,%d" % (sr, sno, ssr, scn, sseq, ag))
                elif lay == 2:
                    sc_rows.append(";".join([sr, sno, ssr, str(int(cen["nat"][sc])), str(sseq), str(ag)]))
                else:
                    sc_rows.append([sr, sno, ssr, scn, sseq, ag])
                for j, pid in enumerate(T["members"]):
                    m = int(T["marks"][j, k])
                    t_lines.append(sep.join([sr, sno, mref(WD, b, pid, y), "" if m < 0 else str(m)]))
        if lay == 1:
            put(os.path.join(target, F["scripts"]), ["meeting_series", "script_no", "source_series", "source_centre_no",
                                                     "source_candidate_no", "agreed_mark"], sc_rows)
            put(os.path.join(target, F["trial"]), ["meeting_series", "script_no", "moderator_ref", "mark"], t_lines)
        elif lay == 2:
            put(os.path.join(target, F["scripts"]), ["Meeting", "Script", "FromSeries", "FromRollNo", "FromCandNo",
                                                     "AgreedMark"], sc_rows, sep)
            put(os.path.join(target, F["trial"]), ["Meeting", "Script", "Moderator", "Mark"], t_lines, sep)
        else:
            sheet(os.path.join(target, F["scripts"]), "Scripts", ["Meeting", "Script", "From series", "From centre",
                                                                  "From cand no", "Agreed mark"], sc_rows, [11, 10, 12, 12, 13, 12])
            put(os.path.join(target, F["trial"]), ["Meeting", "Script", "Moderator", "Mark"], t_lines)
        counts[F["trial"]] = len(t_lines)
        counts[F["scripts"]] = len(sc_rows)
        # ---- enquiries that changed nothing
        for y in range(2019, YEARS[-1] + 1):
            for _ in range(int(rng.poisson(9))):
                c = int(rng.integers(0, len(cen["nat"])))
                d_ = dt.date(y, 8, 18) + dt.timedelta(days=int(rng.integers(0, 45)))
                kind = ["Clerical check of moderation record", "Copy of moderator's report", "Clerical check of mark sheet"][
                    int(rng.integers(0, 3))]
                enq.append((b, y, int(cen["nat"][c]), d_, kind, "No change" if kind.startswith("Clerical") else "Issued"))
    # ---- the national registers
    rows = []
    for p in WD["people"]:
        if not p["reg"]:
            continue
        for b, ys in p["boards"].items():
            ys = [y for y in ys if y >= WL.REG_FROM]
            if ys:
                rows.append((p["reg"], p["last"], p["first"], b, min(ys), max(ys)))
    rows.sort(key=lambda r: (r[0], r[3]))
    put(os.path.join(target, FILES["register"]), ["registration_no", "surname", "forename", "board", "first_series",
                                                  "last_series"],
        ["%s,%s,%s,%s,%d,%s" % (r[0], r[1], r[2], r[3], r[4], "" if r[5] == YEARS[-1] else str(r[5])) for r in rows])
    counts[FILES["register"]] = len(rows)
    rows = []
    for b in WL.BOARDS:
        cen = WD["boards"][b]["cen"]
        for i in range(len(cen["nat"])):
            rows.append((int(cen["nat"][i]), b, cno(b, cen["own"][i]), cen["name"][i], cen["county"][i], int(cen["approved"][i])))
    rows.sort()
    put(os.path.join(target, FILES["centres"]), ["roll_no", "board", "board_centre_no", "centre_name", "county", "approved"],
        ["%d,%s,%s,%s,%s,%d" % (r[0], r[1], r[2], q(r[3]), r[4], r[5]) for r in rows])
    counts[FILES["centres"]] = len(rows)
    # ---- the regulator's review marks
    rb = C.REFEREE[0]
    cen = WD["boards"][rb]["cen"]
    lines = []
    for (c, seqnos, cm, rm) in WD["review"]:
        for s_, a_, r_ in zip(seqnos.tolist(), cm.tolist(), rm.tolist()):
            lines.append("%d,%04d,%d,%d" % (cen["nat"][c], s_, a_, r_))
    put(os.path.join(target, FILES["review"]), ["roll_no", "candidate_no", "centre_mark", "review_mark"], lines)
    counts[FILES["review"]] = len(lines)
    # ---- the three files the analysis does not use
    enq = sorted((r for r in enq if r[1] >= 2019), key=lambda r: (r[3], r[0], r[2]))   # the enquiries service opened in 2019
    put(os.path.join(target, FILES["enquiries"]), ["received", "board", "series", "roll_no", "enquiry", "result"],
        ["%s,%s,%d,%d,%s,%s" % (r[3].isoformat(), r[0], r[1], r[2], r[4], r[5]) for r in enq])
    counts[FILES["enquiries"]] = len(enq)
    put(os.path.join(target, FILES["entries"]), ["board", "series", "trade", "age_band", "entries"],
        ["%s,%d,%s,%s,%d" % r for r in entries])
    counts[FILES["entries"]] = len(entries)
    vis = []
    insp = WL.names(rng, 9)
    for b in WL.BOARDS:
        cen = WD["boards"][b]["cen"]
        for i in range(len(cen["nat"])):
            for _ in range(int(rng.random() < 0.55) + int(rng.random() < 0.12)):
                d_ = dt.date(2022, 1, 10) + dt.timedelta(days=int(rng.integers(0, 1790)))
                f_, l_ = insp[int(rng.integers(0, 9))]
                vis.append([d_.strftime("%d/%m/%Y"), int(cen["nat"][i]), cen["name"][i], "%s %s" % (f_, l_),
                            int(rng.integers(4, 31)), ["Satisfactory", "Satisfactory", "Satisfactory", "Good", "Action required"][
                                int(rng.integers(0, 5))], int(rng.integers(0, 5)),
                            ["Approval continued", "Approval continued", "Approval continued", "Continued with conditions"][
                                int(rng.integers(0, 4))], d_.toordinal()])
    vis.sort(key=lambda r: (r[-1], r[1]))
    sheet(os.path.join(target, FILES["visits"]), "Visits", ["Visit date", "Roll no", "Centre", "Inspector", "Work stations",
                                                            "Workshop and equipment", "Safety actions raised", "Result"],
          [r[:-1] for r in vis], [12, 9, 44, 22, 14, 23, 21, 26])
    counts[FILES["visits"]] = len(vis)
    return counts
