"""An independent recomputation from the shipped files, sharing no code with load.py, analysis.py or passes.py: its
own CSV and workbook readers, its own de-duplication, closed-form expectations in place of the golden's simulation.
It recomputes the October 2026 book exactly, the KPI export's nine months exactly, the price line from its own
uplift regression, the October Team book left in December 2027 from its own hazard table, the open deals' expected
new ARR from its own win table, and reads the golden workbook and note back to check that every figure they state is
the generator's and that the bridge adds up. Exit 1 on any failure.

    python3 verify.py [target]
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
RATE = 1.16
CUT = dt.date(2026, 10, 31)
FAIL, N = [], [0]


def ok(name, cond, detail=""):
    N[0] += 1
    print("%s  %s %s" % ("ok  " if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def rows(target, prefix):
    f = [x for x in os.listdir(target) if x.startswith(prefix)][0]
    with open(os.path.join(target, f), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def d(s):
    return dt.date.fromisoformat(s)


def mi(day):
    return (day.year - 2022) * 12 + day.month - 1


def month_end(m):
    y, mo = 2022 + m // 12, m % 12 + 1
    nxt = dt.date(y + (mo == 12), mo % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def sheet(path, name):
    z = zipfile.ZipFile(path)
    wbx = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
           for s in wbx.find("m:sheets", NS) if s.get("name") == name][0]
    tgt = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    ws = ET.fromstring(z.read("xl/" + tgt.lstrip("/").replace("xl/", "")))
    out = []
    for row in ws.find("m:sheetData", NS):
        vals = []
        for c in row:
            col = 0
            for ch in c.get("r"):
                if ch.isalpha():
                    col = col * 26 + ord(ch) - 64
            while len(vals) < col - 1:
                vals.append(None)
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s":
                vals.append(shared[int(v.text)])
            elif t == "inlineStr":
                vals.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
            else:
                vals.append(None if v is None else float(v.text))
        out.append(vals)
    return out


def docx_text(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode()
    paras = re.findall(r"<w:p[ >].*?</w:p>", x, re.S)
    return "\n".join("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras)


# ------------------------------------------------------------------------------------------------ the book
def business_lines(target):
    seen, keep = set(), []
    for r in rows(target, "billing_contract_lines"):
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        keep.append(r)
    credited = {r["credits_line_id"] for r in keep if r["credits_line_id"]}
    return [r for r in keep if r["line_type"] != "Credit note" and r["line_id"] not in credited]


def business_arr(lines, day):
    """Seats in force on a day at the contracted price, times twelve, at the plan rate."""
    subs = [r for r in lines if r["line_type"].startswith("Subscription") and d(r["service_start"]) <= day <=
            d(r["service_end"])]
    tu = defaultdict(int)
    for r in lines:
        if r["line_type"] == "Seat true-up" and d(r["service_start"]) <= day <= d(r["service_end"]):
            tu[r["billing_account"]] += int(r["quantity"])
    tot = 0.0
    for r in subs:
        fx = RATE if r["currency"] == "GBP" else 1.0
        tot += (int(r["quantity"]) + tu[r["billing_account"]]) * float(r["unit_price"]) * 12 * fx
    return tot, len(subs)


def team_arr(inv, day):
    tot, n = 0.0, 0
    for r in inv:
        if r["status"] == "paid" and d(r["period_start"]) <= day <= d(r["period_end"]):
            fx = RATE if r["currency"] == "GBP" else 1.0
            tot += int(r["seats_billed"]) * float(r["price_per_seat"]) * 12 * fx
            n += 1
    return tot, n


def r10k(x):
    return int(round(x / 1e4)) * 10000


def r50k(x):
    return int(round(x / 5e4)) * 50000


def rprec(x, key, figs):
    step = figs["conventions"]["precision"].get(key, 10000)
    return int(round(x / step)) * step


def pdf_text(path):
    import subprocess
    return " ".join(subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout.split())


# ------------------------------------------------------------------------------------------------ price
def price_line(lines, survive):
    """Per-seat price change at each renewal since 1 January 2026 on log seats (OLS), applied to each contract in force
    at the cut that has not yet repriced, on its seats at the cut, weighted by the chance it renews."""
    by_acc = defaultdict(list)
    for r in lines:
        if r["line_type"].startswith("Subscription"):
            by_acc[r["billing_account"]].append(r)
    tu = defaultdict(list)
    for r in lines:
        if r["line_type"] == "Seat true-up":
            tu[r["billing_account"]].append(r)
    xs, ys = [], []
    for a, L in by_acc.items():
        L.sort(key=lambda r: r["service_start"])
        for prev, nxt in zip(L, L[1:]):
            if d(nxt["service_start"]) >= dt.date(2026, 1, 1) and float(nxt["unit_price"]) > float(prev["unit_price"]) + 0.005:
                seats = int(prev["quantity"]) + sum(int(t["quantity"]) for t in tu[a] if prev["service_start"] <=
                                                    t["service_start"] <= prev["service_end"])
                xs.append(math.log(max(seats, 5) / 20.0))
                ys.append(float(nxt["unit_price"]) / float(prev["unit_price"]) - 1)
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a0 = my - b * mx
    tot = 0.0
    for a, L in by_acc.items():
        cur = [r for r in L if d(r["service_start"]) <= CUT <= d(r["service_end"])]
        if not cur:
            continue
        r = cur[0]
        if d(r["service_start"]) >= dt.date(2026, 1, 1):
            continue
        seats = int(r["quantity"]) + sum(int(t["quantity"]) for t in tu[a] if r["service_start"] <= t["service_start"]
                                         <= r["service_end"] and d(t["service_start"]) <= CUT)
        up = min(max(a0 + b * math.log(max(seats, 5) / 20.0), 0.0), 19.0 / 15.0 - 1)
        fx = RATE if r["currency"] == "GBP" else 1.0
        tot += survive * seats * float(r["unit_price"]) * up * 12 * fx
    return tot, n, a0, b


def renewal_rate(lines):
    """Share of contract terms that ended before the cut and were followed by a renewal."""
    by_acc = defaultdict(list)
    for r in lines:
        if r["line_type"].startswith("Subscription"):
            by_acc[r["billing_account"]].append(d(r["service_start"]))
    ren = tot = 0
    for a, L in by_acc.items():
        L.sort()
        for i, s in enumerate(L):
            end = dt.date(s.year + 1, s.month, min(s.day, 28)) if s.month == 2 and s.day == 29 else \
                dt.date(s.year + 1, s.month, s.day)
            if dt.date(2022, 1, 1) <= end <= CUT:
                tot += 1
                ren += 1 if i + 1 < len(L) else 0
    return ren / tot


# ------------------------------------------------------------------------------------------------ Team
def team_left(inv):
    paid = [r for r in inv if r["status"] == "paid"]
    hist = defaultdict(dict)
    cur = {}
    for r in paid:
        m = mi(d(r["period_start"]))
        hist[r["team_account"]][m] = int(r["active_members"])
        cur[r["team_account"]] = r["currency"]
    last = {a: max(h) for a, h in hist.items()}
    first = {a: min(h) for a, h in hist.items()}
    links = rows(TARGET, "workspace_account_links")
    upg = set()
    for r in links:
        if r["plan"] == "Team" and r["linked_to"]:
            upg.add(r["account_id"])
    cut = 57
    MIN = 47   # the last month before the three-seat minimum (January 2026 is month 48)
    # base exits by members (1, 2, 3+) and age (under 3, 3 to 11, 12+ months) from January 2023 to November 2025, with
    # a multiplicative calendar index of the exit month, fitted by alternating ratios
    obs = []
    for a, h in hist.items():
        for m, mem in h.items():
            if 12 <= m < MIN:
                age = m - first[a]
                k = (min(mem, 3), 0 if age < 3 else (1 if age < 12 else 2))
                gone = (m + 1) not in h and m < cut
                obs.append((k, (m + 1) % 12 + 1, 1 if (gone and a not in upg) else 0))
    base = {}
    cnt = defaultdict(lambda: [0, 0])
    for k, c, y in obs:
        cnt[k][0] += 1
        cnt[k][1] += y
    base = {k: v[1] / v[0] for k, v in cnt.items()}
    sidx = {c: 1.0 for c in range(1, 13)}
    for _ in range(4):
        o = defaultdict(float)
        e = defaultdict(float)
        for k, c, y in obs:
            o[c] += y
            e[c] += base[k]
        raw = {c: o[c] / e[c] for c in range(1, 13)}
        w = sum(e.values())
        norm = sum(raw[c] * e[c] for c in range(1, 13)) / w
        sidx = {c: raw[c] / norm for c in range(1, 13)}
        num = defaultdict(float)
        den = defaultdict(float)
        for k, c, y in obs:
            num[k] += y
            den[k] += sidx[c]
        base = {k: num[k] / den[k] for k in num}
    padded = {a for a, h in hist.items() if MIN in h and h[MIN] < 3}
    exc = defaultdict(lambda: [0, 0.0, 0])
    for a in padded:
        h = hist[a]
        for m in range(MIN, cut):
            if m in h:
                age = m - first[a]
                k = (min(h[m], 3), 0 if age < 3 else (1 if age < 12 else 2))
                gone = (m + 1) not in h
                exc[m][0] += 1
                exc[m][1] += base[k] * sidx[(m + 1) % 12 + 1]
                exc[m][2] += 1 if (gone and a not in upg) else 0
    series = [(exc[m][2] - exc[m][1]) / exc[m][0] for m in range(MIN, cut)]
    persist = sum(series[-3:]) / 3
    # each October account's chance of still billing on Team in December 2027, members held at October's
    nine = sum(1 for a, h in hist.items() for m, mem in h.items() if 11 <= m < cut and mem >= 9)
    ups = sum(1 for a in upg if a in last and last[a] >= 11)
    up_rate = ups / nine if nine else 0.0
    # members move a step at a time: the chances of a gain (one or two) and of a loss, from consecutive months
    nup = ntwo = ndown = nst = 0
    for a, h in hist.items():
        for m, mem in h.items():
            if m < cut and (m + 1) in h:
                dlt = h[m + 1] - mem
                nst += 1
                nup += dlt > 0
                ntwo += dlt >= 2
                ndown += dlt < 0 and mem > 1
    pu, p2, pd = nup / nst, ntwo / max(nup, 1), ndown / nst
    S = 80
    tot = 0.0
    for a, h in hist.items():
        if cut not in h:
            continue
        dist = [0.0] * S
        dist[min(h[cut], S - 1)] = 1.0
        for k in range(1, 15):
            age = cut + k - first[a]
            ab = 0 if age < 3 else (1 if age < 12 else 2)
            cal = (cut + k) % 12 + 1
            nd = [0.0] * S
            for mem in range(1, S):
                pmass = dist[mem]
                if pmass == 0.0:
                    continue
                hz = base[(min(mem, 3), ab)] * sidx[cal] + (persist if a in padded else 0.0) + (up_rate if mem >= 9 else 0.0)
                stay = pmass * (1 - hz)
                up1, up2 = pu * (1 - p2), pu * p2
                dn = pd if mem > 1 else 0.0
                nd[min(mem + 1, S - 1)] += stay * up1
                nd[min(mem + 2, S - 1)] += stay * up2
                nd[mem - 1 if mem > 1 else mem] += stay * dn
                nd[mem] += stay * (1 - up1 - up2 - dn)
            dist = nd
        price = 10.40 * RATE if cur[a] == "GBP" else 12.0
        tot += sum(p * max(mm, 3) for mm, p in enumerate(dist)) * price * 12
    return tot, persist, sidx


# ------------------------------------------------------------------------------------------------ pipeline
def open_deals(target, per_seat):
    seen, snap = set(), []
    for r in rows(target, "pipeline_snapshots"):
        k = tuple(r.values())
        if k not in seen:
            seen.add(k)
            snap.append(r)
    won = {}
    for r in rows(target, "opportunities_closed"):
        if r["outcome"] == "Closed Won":
            won[r["opportunity_id"]] = mi(d(r["close_date"]))
    typical = {"Discovery": 2, "Evaluation": 2, "Proposal": 2, "Negotiation": 1}
    tab = defaultdict(lambda: [0, 0])
    now = []
    for r in snap:
        m = mi(d(r["snapshot_date"]))
        mis = m - mi(d(r["stage_entered"]))
        st = min(max(mis - typical[r["stage"]], 0), 4)
        sb = 0 if st == 0 else (1 if st <= 2 else 2)
        key = (r["stage"], sb)
        if 12 <= m <= 57 - 14:
            w = won.get(r["opportunity_id"])
            tab[key][0] += 1
            tab[key][1] += 1 if (w is not None and m < w <= m + 14) else 0
        if m == 57:
            now.append((key, int(r["seats_quoted"])))
    return sum(tab[k][1] / tab[k][0] * s * per_seat for k, s in now if tab[k][0])


def per_quoted_seat(target, lines):
    first = {}
    for r in lines:
        if r["line_type"] == "Subscription - new":
            first[r["billing_account"]] = r
    arr = seats = 0.0
    for r in rows(target, "opportunities_closed"):
        if r["outcome"] == "Closed Won" and d(r["close_date"]) >= dt.date(2026, 1, 1) and r["billing_account"] in first:
            f = first[r["billing_account"]]
            arr += int(f["quantity"]) * float(f["unit_price"]) * 12 * (RATE if f["currency"] == "GBP" else 1.0)
            seats += int(r["seats_quoted"])
    return arr / seats


TARGET = None


def main(target):
    global TARGET
    TARGET = target
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    lines = business_lines(target)
    inv = rows(target, "team_invoices")
    b, nb = business_arr(lines, CUT)
    t, nt = team_arr(inv, CUT)
    ok("R1 Business ARR 31 Oct 2026", r10k(b) == figs["open_bus"], "%d against %d" % (r10k(b), figs["open_bus"]))
    ok("R1 Team ARR 31 Oct 2026", r10k(t) == figs["open_team"], "%d against %d" % (r10k(t), figs["open_team"]))
    kpi = sheet(os.path.join(target, [f for f in os.listdir(target) if f.startswith("kpi_monthly")][0]),
                "ARR month end")
    body = [r for r in kpi if len(r) > 5 and isinstance(r[1], float)]
    ok("KPI export has nine months", len(body) == 9, str(len(body)))
    for i, r in enumerate(body):
        day = month_end(48 + i)
        bb, nbb = business_arr(lines, day)
        tt, ntt = team_arr(inv, day)
        ok("KPI %s reproduces" % r[0], abs(bb - r[1]) < 0.02 and abs(tt - r[2]) < 0.02 and nbb == r[4] and
           ntt == r[5], "%.2f/%.2f against %.2f/%.2f" % (bb, tt, r[1], r[2]))
    surv = renewal_rate(lines)
    pl, n, a0, bslope = price_line(lines, surv)
    ok("R2 price line within EUR 15,000 of the golden", abs(pl - figs["price"]) <= 15000,
       "%.0f against %d (%d repricings, uplift %.3f at 20 seats, slope %.3f)" % (pl, figs["price"], n, a0, bslope))
    ok("R2 flat mean uplift two bins or more above", figs["route_mean_uplift_applied_flat"]["price"] - figs["price"] >= 20000)
    tl, persist, sidx = team_left(inv)
    ok("R3 October Team book left rounds to the golden's figure at its precision", rprec(tl, "team_left", figs) == figs["team_left"],
       "%.0f against %d (lasting excess %.4f, index Oct %.2f Mar %.2f)" % (tl, figs["team_left"], persist, sidx[10],
                                                                         sidx[3]))
    ps = per_quoted_seat(target, lines)
    od = open_deals(target, ps)
    ok("R5 open deals' new ARR rounds to the golden's figure at its precision", rprec(od, "new_open", figs) == figs["new_open"],
       "%.0f against %d" % (od, figs["new_open"]))
    # the trailing extrapolation a ten-minute pass takes, from the book's own month ends
    b12, _ = business_arr(lines, month_end(45))
    t12, _ = team_arr(inv, month_end(45))
    naive12 = (b + t) + ((b + t) - (b12 + t12)) * 14.0 / 12.0
    ok("the trailing twelve months carried forward clear the draft by two steps", naive12 >= figs["draft"] * 1e6 + 2e5,
       "%.0f against the draft %.1f million" % (naive12, figs["draft"]))
    # the policy, read back through an independent extractor: the plan-forecast sentences the call runs on
    pol = pdf_text(os.path.join(target, [f for f in os.listdir(target) if f.startswith("arr_reporting_policy")][0]))
    ok("policy read (control)", "ARR reporting policy" in pol and "Version 5" in pol, str(len(pol)))
    ok("policy 5.2 files what the range carries", "10th to the 90th percentile" in pol and
       "carry their own estimation uncertainty in the range" in pol and
       "No allowance is added to the range beyond what the records show" in pol)
    ok("policy 5.3 files the commitment rule", "largest EUR 0.1 million step that is met or beaten in at least 80 per "
       "cent of the outcomes" in pol)
    ok("policy 5 names no method", not any(w in pol.lower() for w in ("simulat", "monte carlo", "bootstrap", "regress",
                                                                        "hazard", "logistic")))
    # the golden files
    gx = os.path.join(TASK, "golden", "arr_2027_forecast.xlsx")
    fc = sheet(gx, "Forecast")
    path = [r for r in fc if r and isinstance(r[0], float) and r[1] is not None and r[2] is not None]
    ok("workbook path has 14 months", len(path) == 14, str(len(path)))
    ok("workbook path is figures.json's", [int(r[1]) for r in path] == figs["path"] and
       [int(r[2]) for r in path] == figs["path_p10"] and [int(r[3]) for r in path] == figs["path_p90"])
    br = sheet(gx, "Bridge")
    lines_b = {r[0]: r[1] for r in br if r and isinstance(r[0], str) and len(r) > 1 and isinstance(r[1], float)}
    six = ["New Business", "Business seat additions", "Price", "Business seat reductions", "Business accounts lost",
           "Change in Team"]
    ok("bridge has the six lines in the policy's order", [r[0] for r in br if r and r[0] in six] == six)
    ok("bridge adds up", abs(lines_b["ARR 31 October 2026"] + sum(lines_b[k] for k in six) -
                             lines_b["Expected ARR 31 December 2027"]) < 0.5)
    ok("bridge lines are figures.json's", all(int(lines_b[k]) == figs["bridge"][k] for k in six))
    ok("bridge ends at the expected December figure", int(lines_b["Expected ARR 31 December 2027"]) == figs["dec27"])
    txt = docx_text(os.path.join(TASK, "golden", "arr_2027_note.docx"))
    ok("note read (control)", "December 2027" in txt and len(txt) > 800, str(len(txt)))
    for k in ("open_bus", "open_team", "team_left", "new_open", "new_bus", "p10", "p90", "dec27"):
        ok("note states %s" % k, "{:,}".format(figs[k]) in txt)
    ok("note states the commitment and the draft", "Commit EUR %.1f million" % figs["commitment"] in txt and
       "not EUR %.1f million" % figs["draft"] in txt)
    ok("note states the commitment rule", "largest 0.1 million step" in txt and "80 per cent" in txt)
    ok("commitment below the draft by 0.2 or more", figs["draft"] - figs["commitment"] >= 0.2 - 1e-9)
    sm = {r[0]: r[1] for r in fc if r and isinstance(r[0], str) and len(r) > 1 and isinstance(r[1], (float, int))}
    ck = [k for k in sm if k.startswith("Commitment, EUR million")][0]
    ok("workbook states the commitment under the policy's rule", abs(sm[ck] - figs["commitment"]) < 1e-9 and
       "largest 0.1m step" in ck)
    ok("workbook's share at the commitment is 80 per cent or more and the next step's under",
       sm["Share of outcomes at or above the commitment"] >= 0.8 > sm["Share of outcomes at or above the next step up"])
    print("verify: %d checks, %d failed" % (N[0], len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
