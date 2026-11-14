"""submission.md: the four answer blocks, every figure from figures.json."""
import params as P

ORDER = P.ORDER


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(path, f, E):
    b, r = f["bands"], f["roas_2027"]
    by = {k: [c for c in ORDER if b[c] == k] for k in P.BANDS}
    res = {x["id"]: x for x in E["results"]}
    def band_txt(rid, c, nd=2, pct=False):
        lo, hi = res[rid]["bands"][c]
        return ("%.*f to %.*f" % (nd, lo, nd, hi)) if not pct else ("%d to %d" % (lo, hi))
    lines = ["# task1 answer blocks", "", "## Final Recommendation", ""]
    lines.append(
        "Scale %s; hold %s; cut %s for 2027 (2027 return per euro at the media plan's weekly spend: %s). This rejects "
        "scaling Meta iOS, TikTok iOS and Google Android and cutting AppLovin Android, which the billing records scaled "
        "to the stores' totals, the iOS networks' users who allowed tracking and 2025's return per euro would file." % (
            _list(by["scale"]), _list(by["hold"]), _list(by["cut"]),
            "; ".join("%s %.2f" % (c, r[c]) for c in ORDER)))
    lines += ["", "## Supplementary Questions", ""]
    n = 0
    def q(txt):
        nonlocal n
        n += 1
        lines.append("%d. %s" % (n, txt))
    q("A spreadsheet with one row per paid channel (Meta iOS, TikTok iOS, Apple Search Ads, Meta Android, Google "
      "Android, TikTok Android, AppLovin Android) and, for each, the figures in items 2 to 6.")
    q("Installs each channel bought from 4 November 2024 to 2 November 2025 (each within 2 per cent): %s." % "; ".join(
        "%s %s (%s to %s)" % (c, format(f["installs_2025"][c], ","), format(res["R1"]["bands"][c][0], ","),
                              format(res["R1"]["bands"][c][1], ",")) for c in ORDER))
    q("Those installs' 12-month net revenue per install, in euros to the cent (band in brackets): %s." % "; ".join(
        "%s %.2f (%s)" % (c, f["v12_2025"][c], band_txt("R2", c)) for c in ORDER))
    q("Installs a week at each channel's 2027 weekly spend, to the whole install (band in brackets): %s." % "; ".join(
        "%s %d (%d to %d)" % (c, f["installs_week_2027"][c], res["R3"]["bands"][c][0], res["R3"]["bands"][c][1]) for c in ORDER))
    q("Each channel's 2027 return per euro of planned spend, to two decimals (band in brackets): %s." % "; ".join(
        "%s %.2f (%s)" % (c, r[c], band_txt("R4", c)) for c in ORDER))
    q("Each channel's band under the growth policy (cut under 0.90, hold from 0.90, scale from 1.20): %s." % "; ".join(
        "%s %s" % (c, b[c]) for c in ORDER))
    q("A short note (one page) to the head of financial planning and the head of growth giving the bands and the "
      "return behind each, and saying why the figures differ from the billing records and the attribution export.")
    lines += ["", "## Critical Components", ""]
    us = f["unrecorded_share_2025"]
    lines.append(
        "1. The 2025 installs' 12-month net revenue per install carries the store charges the billing records miss "
        "(a charge reaches them only when the subscriber next opens the app; the stores' daily reports exceed the "
        "records over November 2024 to November 2026 by about two fifths of the records' net revenue; %s): AppLovin Android EUR %.2f per install (%.1f per cent of it not in the records), "
        "Meta Android EUR %.2f, Google Android EUR %.2f; spreading the stores' excess over every account in proportion "
        "puts AppLovin Android's return at %.2f, a cut." % (
            "the part missing runs from %.1f per cent of Apple Search Ads' 2025 installs' revenue to %.1f per cent of AppLovin Android's" % (100 * us["Apple Search Ads"], 100 * us["AppLovin Android"]),
            f["v12_2025"]["AppLovin Android"], 100 * us["AppLovin Android"], f["v12_2025"]["Meta Android"],
            f["v12_2025"]["Google Android"], f["routes"]["prop|golden|pooled"]["AppLovin Android"]))
    lines.append(
        "2. The iOS networks are read over all their installs from the install postbacks' conversion values, not on "
        "the users who allowed tracking (%.1f per cent of Meta iOS's installs, %.1f per cent of TikTok iOS's): Meta "
        "iOS EUR %.2f per install against %.2f for its consenting users, TikTok iOS %.2f against %.2f; on the "
        "consenting users both would scale." % (
            100 * f["consent_share_2025"]["Meta iOS"], 100 * f["consent_share_2025"]["TikTok iOS"], f["v12_2025"]["Meta iOS"],
            f["v12_consenters_2025"]["Meta iOS"], f["v12_2025"]["TikTok iOS"], f["v12_consenters_2025"]["TikTok iOS"]))
    lines.append(
        "3. Google Android at the plan's weekly spend (EUR %s a week on average, %.0f per cent over 2025): %d installs a "
        "week and EUR %.2f per install, a return of %.2f against %.2f at 2025's spend, so it holds rather than "
        "scales." % (format(f["plan_weekly_avg"]["Google Android"], ","), 100 * f["google_plan_rise"],
                     f["installs_week_2027"]["Google Android"], f["vpi_2027"]["Google Android"], r["Google Android"],
                     f["roas_2025"]["Google Android"]))
    lines += ["", "## Step-by-Step", ""]
    steps = [
        "Kept consumer accounts and production charges; took each account's first install from the attribution export "
        "(re-sent rows and reinstalls dropped) and its channel; counted the iOS networks' installs from the install "
        "postbacks (the export holds only their users who allowed tracking).",
        "Valued each account's charges in the 365 days from its install at the policy's VAT and 15 per cent commission, "
        "less refunds.",
        "Set the billing records against the stores' daily reports by store, product and month: the stores charged "
        "more, and the excess matches the subscriptions whose last open came before a charge they were still set to "
        "take (%s of them, and %s trials last seen still set to renew); fitted the share of those trials charged at "
        "the trial's end (%.3f) and the monthly continuation of a subscription the app no longer sees (%.3f), and added "
        "each such account's expected charges inside its twelve months. The hurried route spreads the excess in "
        "proportion to what was recorded, which moves it to the subscribers who keep opening the app." % (
            format(f["candidates_renewal"], ","), format(f["candidates_trial"], ","), f["trial_end_share"], f["silent_q"]),
        "Read Meta iOS and TikTok iOS over every install: each postback's conversion value (fine where Apple gave it, "
        "coarse otherwise), valued at that value from the network's consenting users and every non-consenting iOS "
        "user; the consenting users alone overstate Meta iOS by %.0f per cent and TikTok iOS by %.0f per cent." % (
            100 * f["consenter_overstate"]["Meta iOS"], 100 * f["consenter_overstate"]["TikTok iOS"]),
        "Fitted each channel's weekly installs and value per install on its weekly spend, with the month pattern "
        "shared across channels, over 2024-26 for installs and the twelve-month weeks for value; carried each to the "
        "plan's 52 weeks. Only Google Android's plan moves far from 2025's spend.",
        "Returned each channel's 12-month net revenue per euro at the plan's spend and placed it against 0.90 and 1.20.",
        "No other conclusion survives: every defensible variant of each step (the continuation fitted by store or with "
        "its own first month, the non-consenting value pooled or by ratio, coarse values only, the spend response by "
        "channel or without the month pattern) and every fitted input moved by its spread files the same bands, while "
        "the shortcuts file %d different wrong sets among %d shortcut routes." % (f["distinct_wrong_calls"], f["shortcut_routes"])]
    for i, s in enumerate(steps):
        lines.append("%d. %s" % (i + 1, s))
    open(path, "w").write("\n".join(lines) + "\n")
