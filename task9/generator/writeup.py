"""task9 (architecture 10): submission.md, the four answer blocks, written from the figures as stated (F)."""
import figures as FG
import golden as GD
import pack as PK
import params as P

LBL = GD.label


STATED = []          # every figure the blocks state, as they state it; figures.json carries them for figures_check


def _say(*xs):
    STATED.extend(xs)


def mm(v):
    s = "%.2f" % (v / 1e6)
    _say(s)
    return "USD %s million" % s


def kk(v):
    s = "{:,.0f}".format(round(v / 1e3) * 1e3)
    _say(s)
    return "USD " + s


def band_m(b):
    lo, hi = "%.2f" % (b[0] / 1e6), "%.2f" % (b[1] / 1e6)
    _say(lo, hi)
    return "USD %s million and %s million" % (lo, hi)


def band_k(b):
    return "%s and %s" % (kk(b[0]), kk(b[1]))


def cm(v):
    """A cost in USD per million face, to the dollar."""
    s = "{:,.0f}".format(v)
    _say(s)
    return "USD " + s


def band_c(b):
    lo, hi = "{:,.0f}".format(b[0]), "{:,.0f}".format(b[1])
    _say(lo, hi)
    return "USD %s and %s" % (lo, hi)


def pct(v):
    s = "%.1f" % (100 * v)
    _say(s)
    return s + "%"


def num(x):
    """A stated parameter (a horizon, a day count), recorded as stated."""
    _say(str(x))
    return str(x)


def joined(xs):
    xs = list(xs)
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def build(F):
    g, b = F["gold"], F["bands"]
    segs = F["segments"]
    lose = g["lose"]
    pays = [s for s in segs if s not in lose]
    either = F.get("lose_either", [])
    R = F["routes"]
    nd, car, wk = R["the desk's next-day view"], R["careful but hurried"], R["the tape's levels, a week's marks"]
    cp = R[FG.CAREFUL]
    dep = F["dependence"]
    avg = R["the tape's levels, today's wins' cost for the added trades"]
    iid = R["the golden's figures, days drawn one at a time"]
    n = GD.NUMBER
    loss_total = sum(g["bridge"][s] for s in lose)
    del STATED[:]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (strategy backtesting and evaluation: a dealer's "
             "auto-quoting schedule backtested on its own request-for-quote history).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append(
        "**Plan %s of desk P&L for 2027 on the draft schedule** (sound methods land between %s), four years in five between %s "
        "and %s, against %s on the schedule in force, and **approve the draft without its changes for %s**, which together "
        "lose %s; without them the plan is **%s**. It rejects the %s that rivals' levels with a week's marks give when the "
        "trades a tighter quote adds are costed like today's wins, which %s because Ashcote's evaluations of medium and thin "
        "bonds take the move in only at the month-end review, the %s of the desk's next-day markouts and the %s of a win "
        "model fitted on the desk's own quotes%s." % (
            mm(g["proposed"]), band_m(b["proposed"]), mm(g["p10"]), mm(g["p90"]), mm(g["current"]),
            joined(LBL(s) for s in lose), kk(-loss_total), mm(g["adopt"]), mm(cp["proposed"]),
            ("keeps the change for %s" % joined(LBL(s) for s in sorted(set(lose) - set(cp["lose"])))) if set(lose) - set(cp["lose"])
            else ("drops %s as well" % joined(LBL(s) for s in sorted(set(cp["lose"]) - set(lose)))),
            mm(nd["proposed"]), mm(car["proposed"]),
            (" (%s sit%s close enough to zero that sound methods split on %s)" % (
                joined(LBL(s) for s in either), "s" if len(either) == 1 else "", "it" if len(either) == 1 else "them"))
            if either else ""))
    L.append("\n## Supplementary Questions\n")
    L.append("### %s\n" % GD.BOOK)
    L.append(
        "1. A first sheet with the 2027 P&L at the current schedule, **%s** (between %s), at the draft schedule, **%s** (between "
        "%s), the draft's %s%% range from **%s** to **%s** (the %sth percentile between %s, the %sth between %s), and the plan "
        "without the changes that lose money, %s (between %s). Each is the policy's P&L (edge at execution less the move after "
        "the trade once complete, less the bucket's offload charge) on the record since January 2023 replayed at the "
        "schedule and carried at the requests of the twelve months to October 2026; the range draws the year's days in runs "
        "of %s, because the daily P&L is serially dependent (runs of %s to %s days stay inside these bands)." % (
            mm(g["current"]), band_m(b["current"]), mm(g["proposed"]), band_m(b["proposed"]), num(P.RANGE_P[1] - P.RANGE_P[0]),
            mm(g["p10"]), mm(g["p90"]), num(P.RANGE_P[0]), band_m(b["p10"]), num(P.RANGE_P[1]), band_m(b["p90"]), mm(g["adopt"]),
            band_m(b["adopt"]), num(P.BLOCK), num(min(FG.BLOCK_RIVALS)), num(max(FG.BLOCK_RIVALS))))
    L.append(
        "2. The difference between the two schedules split across the %s changed segments, which adds to %s: %s. The changes "
        "that lose money are **%s**; the others add P&L." % (
            n[len(segs)], kk(g["proposed"] - g["current"]),
            "; ".join("%s %s (between %s)" % (LBL(s), kk(g["bridge"][s]), band_k(b["bridge"][s])) for s in segs),
            joined(LBL(s) for s in lose)))
    L.append(
        "3. For each changed segment, the share of its requests since January 2023 the draft's quote would win: %s." % (
            "; ".join("%s %s (between %s and %s; %s at the current schedule)" % (LBL(s), pct(g["share"][s]), pct(b["share"][s][0]),
                                                                pct(b["share"][s][1]), pct(F["today_share"][s])) for s in segs)))
    L.append(
        "4. For each changed segment, what the price moves after the trades cost per million traded since January 2023, read "
        "once the move is complete: on the trades the current schedule wins, %s; on the trades the draft's quote would add, %s." % (
            "; ".join("%s %s (between %s)" % (LBL(s), cm(g["won_cost"][s]), band_c(b["won_cost"][s])) for s in segs),
            "; ".join("%s %s (between %s)" % (LBL(s), cm(g["add_cost"][s]), band_c(b["add_cost"][s])) for s in segs)))
    L.append(
        "5. Further sheets: each changed segment's half-spreads, shares and costs side by side; the bridge with a chart; the "
        "range; and what other readings of the record would plan (the desk's next-day view %s at the draft, a week's marks %s, "
        "a week's marks with the added trades costed like today's wins %s, a win model on the desk's own quotes %s)." % (
            mm(nd["proposed"]), mm(wk["proposed"]), mm(cp["proposed"]), mm(car["proposed"])))
    L.append("\n### %s\n" % GD.NOTE)
    L.append(
        "6. One page for the electronic trading committee: the plan on the draft and on the schedule in force with the range, "
        "the changes to keep at today's quotes and why (what the trades a tighter quote adds cost once Ashcote's marks catch "
        "up, against what today's wins cost), and the plan without them.")
    L.append("\n## Critical Components\n")
    L.append(
        "1. The draft's 2027 P&L is **%s** (between %s), four years in five between %s and %s; the schedule in force makes %s "
        "(between %s)." % (mm(g["proposed"]), band_m(b["proposed"]), mm(g["p10"]), mm(g["p90"]), mm(g["current"]),
                           band_m(b["current"])))
    ex = F["note_examples"]
    L.append(
        "2. The trades a tighter quote adds are not like the trades the current schedule wins: %s. Costing them like those gives the draft %s." % (
            "; ".join("in %s, the current schedule's trades cost %s a million against %s for the added trades" % (
                LBL(s), cm(g["won_cost"][s]), cm(g["add_cost"][s])) for s in ex), mm(avg["proposed"])))
    L.append(
        "3. What a trade costs after it is done arrives only when Ashcote's evaluations catch up, at the month-end review for "
        "medium and thin bonds: the desk's next-day markouts put the schedule in force at %s and a week's marks at %s, against "
        "%s once the moves are complete." % (mm(nd["current"]), mm(wk["current"]), mm(g["current"])))
    L.append("\n## Step-by-Step\n")
    L.append(
        "1. The requests come from Tidewell's audit in two generations (%s to 4 April 2025 in New York time with quantities in "
        "face; %s from 7 April 2025 in UTC with quantities in thousands and the outcomes coded), each request kept at its "
        "latest message version with re-sent messages counted once; 144A bonds are joined to their registered successors "
        "through the security master; a request's segment is its issuer's rating band on its date, its bond's bucket for its "
        "quarter and its client's type." % (PK.F["rfq1"], PK.F["rfq2"]))
    L.append(
        "2. The auto-quoter's distance is the half-spread times multiples the schedule states, so a request's distance at "
        "another schedule is the distance shown times the ratio of the half-spreads; the current schedule is version 3 and "
        "the draft changes %s segments." % n[len(segs)])
    L.append(
        "3. Whether a request would be won at another quote is read from the level it traded at: the cover on the requests "
        "the desk won, and on the requests it lost the winning dealer's print on the public tape (a customer trade in the same "
        "bond on the same side within three minutes, of the same size or capped; cancelled reports dropped and corrected ones "
        "used), which matches %s of them. A win model fitted on the desk's own quotes puts the draft's win shares far lower, "
        "because its quotes widen when the rivals' do." % pct(F["match_rate"]))
    L.append(
        "4. A trade's cost after it is done (policy 5b) is the bond's evaluated price %s trading days on, net of the Treasury "
        "curve's move and of the median move in the evaluated spreads of other issuers' bonds of its rating; %s and %s days "
        "give the same answers. Ashcote takes a medium or " % (num(FG.GOLD["H"]), num(FG.RIVALS["the cost read 25 trading days on"]["H"]),
                                                             num(FG.RIVALS["the cost read 45 trading days on"]["H"])) +
        "thin bond's own move in mostly at its month-end review, so the desk's next-day markouts and a week's marks miss much of "
        "what the requests that pick off stale evaluations cost.")
    L.append(
        "5. Each schedule's 2027 P&L is the record since January 2023 replayed at its quotes (edge less cost less the offload "
        "charge on each trade won), each segment carried at its requests in the twelve months to October 2026, which gives %s "
        "at the current schedule and %s at the draft. The difference by changed segment is the bridge; %s lose money." % (
            mm(g["current"]), mm(g["proposed"]), joined(LBL(s) for s in lose)))
    L.append(
        "6. The year's range draws %s trading days from the record in runs of %s days (%s simulated years): %s to %s; runs of "
        "%s days land inside the bands. Days drawn one at a time give %s to %s, too narrow: the draft's daily P&L has a "
        "first-order autocorrelation of %s (the bound for independent days is %s) and its %s-day sums vary %s times what "
        "independent days would, because informed flow and pick-offs cluster around issuer moves and stress clusters." % (
            num(P.PLAN_DAYS), num(P.BLOCK), num("{:,}".format(P.SIMS)), mm(g["p10"]), mm(g["p90"]),
            joined(num(x) for x in FG.BLOCK_RIVALS), mm(iid["p10"]), mm(iid["p90"]), num("%.2f" % dep["acf1"]),
            num("%.2f" % dep["noise_bound"]), num(P.BLOCK), num("%.1f" % dep["vr21"])))
    L.append(
        "7. No other conclusion survives: rivals' levels with a week's marks and the added trades costed like today's wins "
        "plan %s and drop only %s; with each added request costed on its own record a week's marks plan %s and drop only %s; "
        "the next-day view drops only %s and plans %s; a win model on the desk's own quotes drops %s and plans %s; complete "
        "costs with the added trades costed like today's wins plan %s. Only the replay on the rivals' levels with complete "
        "costs, each added trade on its own record, drops exactly %s." % (
            mm(cp["proposed"]), joined(LBL(s) for s in cp["lose"]), mm(wk["proposed"]), joined(LBL(s) for s in wk["lose"]),
            joined(LBL(s) for s in nd["lose"]), mm(nd["proposed"]), joined(LBL(s) for s in car["lose"]), mm(car["proposed"]),
            mm(avg["proposed"]), joined(LBL(s) for s in lose)))
    return "\n".join(L) + "\n"


def write(F, path):
    open(path, "w").write(build(F))
