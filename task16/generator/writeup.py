"""submission.md: the four answer blocks, every figure from figures.json."""
import deliver as DL
import golden as GD
import params as P

FAM = P.FAM


def _lst(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def text(F):
    nm = F["families"]; B = GD.bands(F)
    keep = [nm[k] for k in F["keep"]]; back = [nm[k] for k in F["hand_back"]]
    h = F["hurried"]; R = F["routes"]
    x = h["extra"][0]
    tk = F["tick"]; rc = F["recon"]; ch = F["by_channel"]
    fmt = "{:,}".format
    order = sorted(FAM, key=lambda k: -F["expected"][k])
    L = []
    L.append("# task16 answer blocks\n")
    L.append("## Tags\n")
    L.append("**Domain:** Machine Learning Research, General Statistics & Data Science (data integration, record linkage and entity resolution).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n")
    L.append("## Final Recommendation\n")
    L.append("**Offer the assistant first through the peak season for %s, and an adviser first for %s.** On the season plan those last five "
             "come to %s per cent, all under the 75 per cent rule, and the assistant resolves %s per cent across all ten families (90 per cent range %s to %s). "
             "This rejects keeping %s with the assistant, which is what the weeks observed carried into the season unchanged would do: it reads %s per cent on "
             "October's conversations and %s on the season's, because late and exception parcels generate %s per cent of the conversations the plan implies "
             "against %s per cent of October's.\n"
             % (_lst(keep), _lst(back), _lst(["%s" % F["expected"][k] for k in F["hand_back"]]), F["expected_all"], F["low_all"], F["high_all"],
                nm[x], h["expected"][x], F["expected"][x], F["late_share"], F["obs_late_share"]))
    L.append("## Supplementary Questions\n")
    L.append("### %s\n" % DL.WORKBOOK)
    L.append("1. The workbook's first sheet has one row per reason family, sorted by expected rate, highest first, and a last row for all ten families "
             "together; columns: reason family, conversations in the record, resolution rate so far (per cent), expected rate over the season (per cent), "
             "the 90 per cent range's low and high, the distance to 75, and which is offered first (assistant or adviser). Further sheets show how the "
             "figures are built up from the contact records: the linked record and the follow-ups it cannot see, the season's conversations by delivery "
             "outcome, the rates by family and outcome, and what each shorter reading gives. Rates are stated to 0.1 of a point.")
    L.append("2. Each reason family's expected resolution rate over the season, per cent, with the band a sound rebuild lands in:")
    for k in order:
        b = B["expected_table"][k]
        L.append("   - %s: **%s** (%s to %s), %s first." % (nm[k], F["expected"][k], b[0], b[1], "assistant" if k in F["keep"] else "adviser"))
    b = B["expected_table"]["ALL"]
    L.append("   - All ten families together: **%s** (%s to %s)." % (F["expected_all"], b[0], b[1]))
    L.append("3. Each rate's 90 per cent range, per cent. The range is graded on its width: half the distance from low to high, with the band a "
             "day-by-day resampling lands in:")
    for k in order:
        b = B["half_table"][k]
        L.append("   - %s: %s to %s (half-width **%s**, band %s to %s)." % (nm[k], F["low"][k], F["high"][k], F["half"][k], b[0], b[1]))
    b = B["half_table"]["ALL"]
    L.append("   - All ten families together: %s to %s (half-width **%s**, band %s to %s)." % (F["low_all"], F["high_all"], F["half_all"], b[0], b[1]))
    b = B["linked"]
    L.append("4. The build-up from the contact records starts from the linked record: **%s** version 3 conversations about a consignment that ended from "
             "28 September to 1 November 2026 (%s to %s), of which %s are followed within 168 hours by a linked contact (%s by another assistant "
             "conversation, %s by live chat, %s by a telephone call that carries the tracking number, %s by a written case in the resolution extract), "
             "a resolution rate of **%s** per cent on the linked record alone (%s to %s)."
             % (fmt(F["conversations"]), fmt(b["conversations"][0]), fmt(b["conversations"][1]), fmt(F["linked_followed"]), fmt(ch["assistant"]), fmt(ch["chat"]),
                fmt(ch["phone"]), fmt(ch["written"]), F["linked_rate"], b["linked_rate"][0], b["linked_rate"][1]))
    L.append("\n### %s\n" % DL.NOTE)
    L.append("5. A memo of about a page that opens with the recommendation (the five families kept with the assistant and the five offered an adviser "
             "first), gives the all-families expected rate with its range, says why the linked record and the weeks observed both overstate the "
             "season, and carries one chart of the ten expected rates with their ranges against the 75 per cent line and a short table of the same figures.\n")
    L.append("## Critical Components\n")
    b = B["phone_unkeyed_share"]
    L.append("1. **%s per cent** of the telephone calls that follow a version 3 conversation carry no tracking number (%s to %s): %s keyed follow-up calls stand "
             "for about %s once each is weighted by the share of consignment calls keyed in its queue with the IVR bypass running or not."
             % (F["phone_unkeyed_share"], b[0], b[1], fmt(F["phone_keyed"]), fmt(F["phone_total"])))
    b = B["written_open"]
    L.append("2. About **%s** written cases that follow a version 3 conversation were still open at the cut and so are not in the resolution extract (%s to %s), "
             "beside %s that are." % (F["written_open"], b[0], b[1], fmt(F["written_closed"])))
    b = B["achieved_all"]
    L.append("3. With both restored, version 3 has resolved **%s per cent** of its conversations (%s to %s), not the %s per cent the linked record shows."
             % (F["achieved_all"], b[0], b[1], F["linked_rate"]))
    b = B["alert_effect"]
    L.append("4. The delay alerts cut assistant conversations per late parcel by **%d per cent** at the pilot depots (%d to %d), measured after against "
             "before 12 October and against the other seven depots." % (F["alert_effect"], b[0], b[1]))
    b = B["season"]
    L.append("5. Late and exception parcels generate **%s per cent** of the conversations the season plan implies (%s to %s), against %s per cent in the "
             "weeks observed, at about **%s** conversations a week (%s to %s)."
             % (F["late_share"], b["late_share"][0], b["late_share"][1], F["obs_late_share"], fmt(F["per_week"]), fmt(b["per_week"][0]), fmt(b["per_week"][1])))
    L.append("\n## Step-by-Step\n")
    L.append("1. Cleaned the four contact exports: kept conversations in `%s` that carry a tracking number, kept the first leg of each inbound call "
             "in `%s` (a transferred call is one contact, callbacks are not contacts, KS-07 2.1) and put its UTC times on the local clock, brought "
             "every tracking number to one form, and mapped intents, wrap-up codes and case categories to the ten reason families with the three "
             "code lists; the cleaned inbound calls equal telephony's weekly summary (%s) in every week and queue."
             % ("assistant_conversations_2026w32_w45.csv", "acd_call_legs_2026-08-03_2026-11-08.csv", fmt(rc["calls"])))
    L.append("2. Linked each of the %s version 3 conversations that ended from 28 September to 1 November to later contacts on the same tracking number "
             "within 168 hours (KS-07 3.1): %s are followed, a rate of %s per cent. This is the hurried reading: it keeps every family but %s."
             % (fmt(F["conversations"]), fmt(F["linked_followed"]), F["linked_rate"], _lst([nm[k] for k in FAM if k not in R["linked"]["keep"]])))
    L.append("3. The telephone export keys a tracking number on only part of its calls, and far fewer when the IVR bypass is running. Weighted each keyed "
             "follow-up call by the inverse of the share of consignment calls keyed in its queue and bypass state: %s keyed calls stand for about %s, so %s "
             "per cent of telephone follow-ups carry no number. The advisers' previous-contact tick agrees: it marks %s unkeyed calls since 28 September as "
             "following the assistant where the capture weights give %s."
             % (fmt(F["phone_keyed"]), fmt(F["phone_total"]), F["phone_unkeyed_share"], fmt(tk["unkeyed_follow_tick"]), fmt(tk["unkeyed_follow_capture"])))
    L.append("4. `%s` holds resolved cases only: its %s customer cases plus the %s the backlog report counts open equal the %s opened. Each closed "
             "follow-up case stands for the cases raised in its queue on its day and the days either side that are still open: about %s open follow-up "
             "cases. Completing on the summer's closing times instead finds %s, because the queues have slowed since October."
             % ("case_resolutions_to_2026-11-08.csv", fmt(rc["cases_closed"]), fmt(rc["cases_open_now"]), fmt(rc["cases_opened"]), F["written_open"],
                R["stationary"]["written_open"]))
    L.append("5. With a conversation whose only follow-up is a keyed call or a closed case standing for those the record cannot see, version 3 has "
             "resolved %s per cent, by family from %s (%s) to %s (%s)."
             % (F["achieved_all"], F["achieved"][min(FAM, key=lambda k: F["achieved"][k])], nm[min(FAM, key=lambda k: F["achieved"][k])],
                F["achieved"][max(FAM, key=lambda k: F["achieved"][k])], nm[max(FAM, key=lambda k: F["achieved"][k])]))
    L.append("6. Carrying those rates into the season unchanged keeps %s at %s per cent (the careful but hurried reading). But the rate depends on how the "
             "parcel runs (%s: %s per cent when on time, %s when two or more days late), and the season's conversations come from its parcels: joined "
             "conversations to `%s` and `%s` for conversations per parcel by delivery outcome, %s per 1,000 on-time parcels against %s per 1,000 two or "
             "more days late." % (nm[x], h["expected"][x], nm[x], F["cells"][x]["ON"], F["cells"][x]["L2"], "consignments_referenced.csv",
                                  "network_performance_daily.csv", F["mix"]["ON"]["contact_per_1000"], F["mix"]["L2"]["contact_per_1000"]))
    L.append("7. Weighting each family's rates by the plan's parcel service levels as if parcels were conversations gives %s per cent for all families, "
             "above the rate achieved; that reading is wrong because a late parcel is many times as likely to generate a conversation."
             % R["parcel_mix"]["expected"]["ALL"])
    L.append("8. The plan turns delay alerts on at every depot from 16 November. At Linz, Graz and Innsbruck, where they have run since 12 October, "
             "conversations per late parcel fell %d per cent against the other depots over the same weeks. Without that cut the season would read %s "
             "per cent for all families and %s for %s, under the line."
             % (F["alert_effect"], R["no_alerts"]["expected"]["ALL"], R["no_alerts"]["expected"]["DLV"], nm["DLV"]))
    L.append("9. Season conversations by outcome are plan parcels times contact rate, late classes cut by the alerts: about %s a week, %s per cent from "
             "late and exception parcels (%s in the weeks observed). Each family's expected rate is its rates by outcome weighted by its own season "
             "conversations: %s per cent for all families; five families at 75 or more." % (fmt(F["per_week"]), F["late_share"], F["obs_late_share"], F["expected_all"]))
    L.append("10. Ranges from 1,000 resamples of whole days, every step redone: plus or minus %s points for all families. Resampling conversations one by "
             "one gives plus or minus %s, too narrow because good and bad days move every family together.\n" % (F["half_all"], h["half_all"]))
    L.append("No other conclusion survives. The linked record (%s per cent) leaves out follow-ups the files themselves show exist: the call counts reconcile "
             "only with unkeyed calls in, and the case counts only with the backlog in. Leaving out the calls keeps %s; leaving out the open cases keeps %s. "
             "The weeks observed cannot stand for the season, because the plan's parcels run later and the record shows what lateness does to both the "
             "number of conversations and their outcome; and the alerts cannot be left out, because the plan turns them on and the pilot depots measure "
             "them. Every sound variant of each step (capture by week, day, hour or wait; open cases by day or week raised; the alerts read class by "
             "class or against version 3 weeks only) keeps the same five families."
             % (F["linked_rate"], _lst([nm[k] for k in R["no_phone"]["keep"] if k not in F["keep"]]) or "the same families",
                _lst([nm[k] for k in R["no_written"]["keep"] if k not in F["keep"]]) or "the same families"))
    return "\n".join(L) + "\n"


def write(F, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text(F))
