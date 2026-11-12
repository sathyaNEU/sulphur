"""task20 architecture 2 (second hardening): the company's quarterly earnings releases (8-K exhibit 99.1, saved as text from EDGAR), fiscal
2021 Q1 to fiscal 2025 Q3. Each carries the condensed income statement, net sales by brand and the condensed balance
sheet; the fourth-quarter releases give net sales by brand for the fiscal year only. The statements beyond net sales,
the brands and customer deposits are texture drawn from the simulated year (margins, expenses, the balance sheet)."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import world as W

HQ = "CHARLOTTE, N.C."
ORD = {1: "First", 2: "Second", 3: "Third", 4: "Fourth"}
WORDS = {13: "Thirteen", 14: "Fourteen", 26: "Twenty-Six", 39: "Thirty-Nine", 52: "Fifty-Two", 53: "Fifty-Three"}
FY2020_GROWTH = [0.41, 0.15, 0.08, 0.05]          # fiscal 2021's quarters on fiscal 2020's (the 2020 store closures)


def fname(d):
    return "bmh_8k_ex99-1_%s.txt" % d.isoformat()


def release_date(qend, fq):
    return (qend + pd.Timedelta(days=26 if fq == 4 else 39)).date()


def qend(n):
    return W.CAL.week_end[W.QIDX == n].iloc[-1]


def lab(d):
    return "%s %d," % (d.strftime("%B"), d.day)


LW, CW = 52, 14


def money(v, dollar=False, w=CW):
    s = "{:,.0f}".format(abs(v))
    if v < 0:
        s = "(" + s + ")"
    return (("$ " + s) if dollar else s).rjust(w)


def figures(w):
    """every quarter's reported figures (USD thousands) and the fiscal 2020 comparatives"""
    rq = np.random.default_rng(w.seed + 4040)
    nq = len(W.QKEYS)
    F = []
    eq = 620000.0
    debt = 300000.0
    shares = 52.9
    for n, k in enumerate(W.QKEYS):
        fq = int(k[-1])
        ns = 1000 * w.rev_q[n]
        fern = 1000 * w.fern_q[n]
        ct = 1000 * w.contract_q[n]
        gm = {1: 0.414, 2: 0.436, 3: 0.431, 4: 0.409}[fq] + 0.002 * (n // 4) + rq.normal(0, 0.003)
        sga = {1: 0.334, 2: 0.307, 3: 0.312, 4: 0.286}[fq] + rq.normal(0, 0.003)
        cogs = ns * (1 - gm)
        gp = ns - cogs
        sg = ns * sga
        oi = gp - sg
        intr = (debt * 0.055 / 4) + rq.normal(0, 150)
        pbt = oi - intr
        tax = pbt * (0.252 + rq.normal(0, 0.004))
        ni = pbt - tax
        shares *= (1 - 0.006 + rq.normal(0, 0.001))
        dil = shares
        bas = shares * 0.991
        if k == "FY2024Q2":
            debt += 250000.0
        debt = max(0.0, debt - (6250.0 if n >= W.QKEYS.index("FY2024Q3") else 0.0))
        eq += ni - 0.30 * dil * 1000 - 0.85 * ni
        dep = 1000 * w.dep_q[n]
        retail = ns - ct
        ar = retail * 3.0 / 91 + ct * 46.0 / 91 + rq.normal(0, 900)
        inv = 0.53 * cogs * (1.18 if fq == 3 else 1.0) + rq.normal(0, 4000)
        pre = 0.030 * ns + rq.normal(0, 1500)
        ppe = 780000 + 6100 * n + rq.normal(0, 1200)
        rou = 1046000 + 3900 * n + rq.normal(0, 2500)
        gw = 182400.0 - 1450 * max(0, n - W.QKEYS.index("FY2024Q2")) if n >= W.QKEYS.index("FY2024Q2") else 0.0
        oth = 121000 + rq.normal(0, 600)
        ap = 0.47 * cogs + rq.normal(0, 3000)
        acc = 158000 + 0.025 * ns + rq.normal(0, 2500)
        cll = 141000 + 650 * n + rq.normal(0, 400)
        lll = 1006000 + 3600 * n + rq.normal(0, 2300)
        olt = 61000 + rq.normal(0, 700)
        tl = ap + acc + dep + cll + debt + lll + olt
        other_assets = ar + inv + pre + ppe + rou + gw + oth
        cash = tl + eq - other_assets
        F.append(dict(key=k, fq=fq, ns=ns, fern=fern, ct=ct, cogs=cogs, gp=gp, sga=sg, oi=oi, intr=intr, pbt=pbt,
                      tax=tax, ni=ni, eps_b=ni / (bas * 1000), eps_d=ni / (dil * 1000), sh_b=bas * 1000,
                      sh_d=dil * 1000, cash=cash, ar=ar, inv=inv, pre=pre, ppe=ppe, rou=rou, gw=gw, oth=oth, ap=ap,
                      acc=acc, dep=dep, cll=cll, debt=debt, lll=lll, olt=olt, eq=eq))
    # fiscal 2020's quarters, the comparatives of the fiscal 2021 releases (net sales, brands, the balance sheet)
    pre = []
    for q in range(4):
        f21 = F[q]
        g = FY2020_GROWTH[q] + rq.normal(0, 0.004)
        x = {key: (v / (1 + g) if isinstance(v, float) and key not in ("eps_b", "eps_d", "sh_b", "sh_d") else v)
             for key, v in f21.items()}
        x["ct"] = 1000 * (11.6 + 0.3 * q + rq.normal(0, 0.5))
        x["fern"] = 0.0
        x["key"] = "FY2020Q%d" % (q + 1)
        x["eps_b"], x["eps_d"] = x["ni"] / f21["sh_b"], x["ni"] / f21["sh_d"]
        x["sh_b"], x["sh_d"] = f21["sh_b"] * 1.006, f21["sh_d"] * 1.006
        x["dep"] = 1000 * float(w.dep_pre[[20, 33, 46, 59][q]])
        x["gw"] = 0.0
        x["cash"] = (x["ap"] + x["acc"] + x["dep"] + x["cll"] + x["debt"] + x["lll"] + x["olt"] + x["eq"]
                     - (x["ar"] + x["inv"] + x["pre"] + x["ppe"] + x["rou"] + x["oth"]))
        pre.append(x)
    return F, pre


def _line(label, vals, dollar=False, indent=0, wl=LW, wv=CW):
    s = (" " * indent + label).ljust(wl)
    out = []
    for i, v in enumerate(vals):
        if v is None:
            out.append(" " * wv)
        elif isinstance(v, str):
            out.append(v.rjust(wv))
        else:
            out.append(money(v, dollar, wv))
        if i % 2 == 1 and i < len(vals) - 1:
            out.append("   ")
    return s + "".join(out)


def _hdr(groups, dates, wl=LW, wv=CW):
    """column heads: groups is [(label, ncols)], or [((label, label), 2)] when the pair's columns cover different numbers
    of weeks; dates the column dates"""
    l1 = " " * wl
    l1b = " " * wl
    split = any(isinstance(g, tuple) for g, _ in groups)
    for g, nc in groups:
        gap = "   " if nc == 2 else ""
        if isinstance(g, tuple):
            l1 += "".join(x.rjust(wv) for x in g) + gap
            l1b += "".join("Ended".rjust(wv) for _ in g) + gap
        else:
            l1 += g.center(wv * nc) + gap
            l1b += " " * (wv * nc) + gap
    l2 = " " * wl
    l3 = " " * wl
    for i, d in enumerate(dates):
        l2 += lab(d).rjust(wv)
        l3 += str(d.year).rjust(wv)
        if i % 2 == 1 and i < len(dates) - 1:
            l2 += "   "
            l3 += "   "
    out = [l1.rstrip()] + ([l1b.rstrip()] if split else []) + [l2.rstrip(), l3.rstrip()]
    return out


def write_release(path, n, F, pre, w):
    k = W.QKEYS[n]
    fy, fq = int(k[2:6]), int(k[-1])
    cur = F[n]
    prv = F[n - 4] if n >= 4 else pre[fq - 1]
    qe = qend(n).date()
    pqe = (qend(n - 4).date() if n >= 4 else (W.FY_START - pd.Timedelta(days=1 + 7 * 13 * (4 - fq))).date())
    fy_end_prev = (W.FY_START - pd.Timedelta(days=1)).date() if fy == 2021 else qend(n - fq).date()
    weeks = int((W.QIDX == n).sum())
    first_n = n - (fq - 1)
    ytd_weeks = int(np.isin(W.QIDX, range(first_n, n + 1)).sum())
    old = fy <= 2022
    rd = release_date(qend(n), fq)
    title = "Brindle & Moss, Inc. Reports %s Quarter%s Fiscal %d Results" % (ORD[fq], " and" if fq == 4 else "", fy)
    if fq == 4:
        title = "Brindle & Moss, Inc. Reports Fourth Quarter and Fiscal %d Results" % fy

    def ytd(key, src_list, first):
        return sum(src_list[i][key] for i in range(first, first + fq))
    first_prev = n - 4 - (fq - 1)

    def ytd_prev(key):
        if n >= 4:
            return sum(F[i][key] for i in range(first_prev, first_prev + fq))
        return sum(pre[i][key] for i in range(0, fq))
    lines = ["EX-99.1", "", "Exhibit 99.1", "", title, "",
             "%s, %s -- Brindle & Moss, Inc. (NYSE: BMH) today reported results for the %s quarter of fiscal %d, the "
             "%s weeks ended %s %d, %d." % (HQ, "%s %d, %d" % (rd.strftime("%B"), rd.day, rd.year), ORD[fq].lower(), fy,
                                             WORDS[weeks].lower(), qe.strftime("%B"), qe.day, qe.year), ""]
    ns_m, pns_m = cur["ns"] / 1000, prv["ns"] / 1000
    para = ("Net sales for the %s quarter were $%s million, compared with $%s million in the %s quarter of fiscal %d. "
            "Net income was $%s million, or $%.2f per diluted share, compared with $%s million, or $%.2f per diluted "
            "share, a year ago." % (ORD[fq].lower(), "{:,.1f}".format(ns_m), "{:,.1f}".format(pns_m), ORD[fq].lower(),
                                    fy - 1, "{:,.1f}".format(cur["ni"] / 1000), cur["eps_d"], "{:,.1f}".format(prv["ni"] / 1000),
                                    prv["eps_d"]))
    lines += [para, ""]
    if fq == 4:
        yn = sum(F[i]["ns"] for i in range(first_n, n + 1)) / 1000
        yp = ytd_prev("ns") / 1000
        lines += ["Net sales for fiscal %d were $%s million, compared with $%s million in fiscal %d." % (
            fy, "{:,.1f}".format(yn), "{:,.1f}".format(yp), fy - 1), ""]
    studios = sum(1 for s in w.studios if s.date() <= qe)
    stores = 96 + (n // 3)
    lines += ["At the end of the quarter the Company operated %d Brindle & Moss stores, %d design studios and 4 outlets%s."
              % (stores, studios, ", and 31 Fernhollow stores" if qe >= W.ACQUIRED.date() else ""), ""]
    lines += ["Conference Call", "The Company will host a conference call at 8:30 a.m. Eastern Time today. The call and a "
              "replay are available at ir.brindlemoss.com.", ""]
    about = ("Brindle & Moss, Inc. sells furniture and home furnishings through its Brindle & Moss stores and design "
             "studios and brindlemoss.com%s, and furnishes hotels, offices and senior living communities through B&M "
             "Contract." % (", and through Fernhollow Outfitters" if qe >= W.ACQUIRED.date() else ""))
    lines += ["About Brindle & Moss", about, ""]
    lines += ["Forward-Looking Statements", "This release contains forward-looking statements within the meaning of the "
              "Private Securities Litigation Reform Act of 1995. Actual results may differ materially from those "
              "expressed or implied. The Company undertakes no obligation to update any forward-looking statement.", ""]
    # the income statement
    pweeks = int((W.QIDX == n - 4).sum()) if n >= 4 else 13
    p_ytd = int(np.isin(W.QIDX, range(n - 4 - (fq - 1), n - 3)).sum()) if n >= 4 else 13 * fq

    def head(a, b, words):
        if a == b:
            return words % WORDS[a]
        return ("%d Weeks" % a, "%d Weeks" % b)
    head_q = "Three Months Ended" if old and weeks == 13 else head(weeks, pweeks, "%s Weeks Ended")
    if fq == 1:
        groups, dates = [(head_q, 2)], [qe, pqe]
    elif fq in (2, 3):
        yh = ("%s Months Ended" % {2: "Six", 3: "Nine"}[fq]) if old else head(ytd_weeks, p_ytd, "%s Weeks Ended")
        groups, dates = [(head_q, 2), (yh, 2)], [qe, pqe, qe, pqe]
    else:
        yh = "Fiscal Year Ended" if old else head(ytd_weeks, p_ytd, "%s Weeks Ended")
        groups, dates = [(head_q, 2), (yh, 2)], [qe, pqe, qe, pqe]
    lines += ["BRINDLE & MOSS, INC.".center(100).rstrip(),
              "CONDENSED CONSOLIDATED STATEMENTS OF INCOME (UNAUDITED)".center(100).rstrip(),
              "(in thousands, except per share amounts)".center(100).rstrip(), ""]
    lines += _hdr(groups, dates)
    rows = [("Net sales", "ns", True), ("Cost of goods sold, including occupancy", "cogs", False),
            ("Gross profit", "gp", False),
            ("Selling, general and administrative" + ("" if old else " expenses"), "sga", False),
            ("Operating income", "oi", False), ("Interest expense, net", "intr", False),
            ("Income before income taxes", "pbt", False), ("Income tax expense", "tax", False),
            ("Net income", "ni", True)]
    for label, key, dol in rows:
        vals = [cur[key], prv[key]]
        if fq > 1:
            vals += [ytd(key, F, first_n), ytd_prev(key)]
        lines.append(_line(label, vals, dol))
    lines.append("")
    lines.append("Earnings per share:")
    for label, key in (("Basic", "eps_b"), ("Diluted", "eps_d")):
        vals = ["$ %.2f" % cur[key], "$ %.2f" % prv[key]]
        if fq > 1:
            yni = ytd("ni", F, first_n)
            pni = ytd_prev("ni")
            sh = cur["sh_b" if key == "eps_b" else "sh_d"]
            psh = prv["sh_b" if key == "eps_b" else "sh_d"]
            vals += ["$ %.2f" % (yni / sh), "$ %.2f" % (pni / psh)]
        lines.append(_line(label, vals, indent=2))
    lines.append("Weighted average shares outstanding:")
    for label, key in (("Basic", "sh_b"), ("Diluted", "sh_d")):
        vals = [cur[key], prv[key]] + ([cur[key] * 1.002, prv[key] * 1.002] if fq > 1 else [])
        lines.append(_line(label, vals, indent=2))
    lines.append("")
    # net sales by brand: the quarter and the year to date in the first three quarters, the fiscal year in the fourth
    lines += ["NET SALES BY BRAND (UNAUDITED)".center(100).rstrip(), "(in thousands)".center(100).rstrip(), ""]
    ct_label = "B&M Contract" if old else "Contract"
    if fq < 4:
        lines += _hdr(groups if fq > 1 else [(head_q, 2)], dates if fq > 1 else [qe, pqe])

        def brand_vals(key):
            v = [cur[key], prv[key]]
            if fq > 1:
                v += [ytd(key, F, first_n), ytd_prev(key)]
            return v
        bm = [a - b - c for a, b, c in zip(brand_vals("ns"), brand_vals("fern"), brand_vals("ct"))]
        lines.append(_line("Brindle & Moss", bm, True))
        fv = brand_vals("fern")
        if any(x > 0 for x in fv):
            lines.append(_line("Fernhollow", [x if x > 0 else "--" for x in fv]))
        lines.append(_line(ct_label, brand_vals("ct")))
        lines.append(_line("Total net sales", brand_vals("ns"), True))
    else:
        yh = "Fiscal Year Ended" if old else head(ytd_weeks, p_ytd, "%s Weeks Ended")
        lines += _hdr([(yh, 2)], [qe, pqe])
        yv = [ytd("ns", F, first_n), ytd_prev("ns")]
        yf = [ytd("fern", F, first_n), ytd_prev("fern")]
        yc = [ytd("ct", F, first_n), ytd_prev("ct")]
        lines.append(_line("Brindle & Moss", [a - b - c for a, b, c in zip(yv, yf, yc)], True))
        if any(x > 0 for x in yf):
            lines.append(_line("Fernhollow", [x if x > 0 else "--" for x in yf]))
        lines.append(_line(ct_label, yc))
        lines.append(_line("Total net sales", yv, True))
    lines.append("")
    # the balance sheet: the quarter's end, the prior fiscal year's end and, in the first three quarters, a year earlier
    lines += ["CONDENSED CONSOLIDATED BALANCE SHEETS (UNAUDITED)".center(100).rstrip(), "(in thousands)".center(100).rstrip(), ""]
    if fq < 4:
        fy_prev = F[first_n - 1] if first_n >= 1 else dict(pre[3])
        cols = [cur, fy_prev, prv]
        bdates = [qe, fy_end_prev, pqe]
    else:
        cols = [cur, prv]
        bdates = [qe, pqe]
    l2 = " " * LW + "".join(lab(d).rjust(CW) for d in bdates)
    l3 = " " * LW + "".join(str(d.year).rjust(CW) for d in bdates)
    lines += [l2.rstrip(), l3.rstrip()]

    def bline(label, key, dol=False, indent=0):
        s = (" " * indent + label).ljust(LW)
        for c in cols:
            v = c.get(key, 0.0)
            s += money(v, dol) if v else "--".rjust(CW)
        return s.rstrip()
    lines.append("ASSETS")
    lines.append("Current assets:")
    lines.append(bline("Cash and cash equivalents", "cash", True, 2))
    lines.append(bline("Accounts receivable, net", "ar", False, 2))
    lines.append(bline("Merchandise inventories", "inv", False, 2))
    lines.append(bline("Prepaid expenses and other current assets", "pre", False, 2))
    for c in cols:
        c["tca"] = c["cash"] + c["ar"] + c["inv"] + c["pre"]
        c["ta"] = c["tca"] + c["ppe"] + c["rou"] + c.get("gw", 0.0) + c["oth"]
        c["tcl"] = c["ap"] + c["acc"] + c["dep"] + c["cll"]
        c["tle"] = c["tcl"] + c["debt"] + c["lll"] + c["olt"] + c["eq"]
    lines.append(bline("Total current assets", "tca", False, 4))
    lines.append(bline("Property and equipment, net", "ppe"))
    lines.append(bline("Operating lease right-of-use assets", "rou"))
    if any(c.get("gw", 0.0) for c in cols):
        lines.append(bline("Goodwill and intangible assets, net", "gw"))
    lines.append(bline("Other assets", "oth"))
    lines.append(bline("Total assets", "ta", True, 4))
    lines.append("LIABILITIES AND STOCKHOLDERS' EQUITY")
    lines.append("Current liabilities:")
    lines.append(bline("Accounts payable", "ap", True, 2))
    lines.append(bline("Accrued expenses and other current liabilities", "acc", False, 2))
    lines.append(bline("Customer deposits", "dep", False, 2))
    lines.append(bline("Current portion of operating lease liabilities", "cll", False, 2))
    lines.append(bline("Total current liabilities", "tcl", False, 4))
    lines.append(bline("Long-term debt", "debt"))
    lines.append(bline("Operating lease liabilities, less current portion", "lll"))
    lines.append(bline("Other long-term liabilities", "olt"))
    lines.append(bline("Total stockholders' equity", "eq"))
    lines.append(bline("Total liabilities and stockholders' equity", "tle", True, 4))
    lines.append("")
    lines.append("# # #")
    open(path, "w", newline="\r\n" if old else "\n").write("\n".join(lines) + "\n")
    return rd


def write_all(tgt, w):
    F, pre = figures(w)
    out = {}
    for n, k in enumerate(W.QKEYS[:-1]):
        rd = release_date(qend(n), int(k[-1]))
        p = os.path.join(tgt, fname(rd))
        write_release(p, n, F, pre, w)
        out[fname(rd)] = (k, rd)
    return out, F, pre
