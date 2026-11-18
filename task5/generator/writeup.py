"""submission.md: the tags and the four answer blocks, every figure from figures.json."""
import deliver
import docs
import pack
import world as WL

F = dict(pack.FILES)
F.update(docs.FILES)
HOSTS = WL.HOSTS
WORD = deliver.WORD


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _n(x):
    return format(int(x), ",")


def _b(band, nd=0):
    return "%s to %s" % ((_n(band[0]), _n(band[1])) if nd == 0 else ("%.*f" % (nd, band[0]), "%.*f" % (nd, band[1])))


def _rng(xs, nd=1):
    xs = list(xs)
    return "%.*f to %.*f" % (nd, min(xs), nd, max(xs))


def _date(iso):
    y, m, d = iso.split("-")
    return "%d %s %s" % (int(d), ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                                 "November", "December"][int(m) - 1], y)


def _each(d, fmt="%s %s", num=True):
    return _list(fmt % (h, _n(d[h]) if num else d[h]) for h in HOSTS)


def write(path, f):
    st, n, rf, R = f["stated"], f["counts"], f["referee"], f["routes"]
    refl = R["S1+S2+S3"]
    up, down = deliver.changes(f)
    rate = _n(f["rate"])
    margin = min(min(f["citizens"][h] % f["rate"], f["rate"] - f["citizens"][h] % f["rate"]) for h in HOSTS)
    L = ["# task5 answer blocks", "", "## Tags", "",
         "**Domain:** Other, Survey Research & Official Statistics (census, register and administrative-data quality: how "
         "much of the migration between states each population register records, measured to estimate a population no "
         "register counts).",
         "**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).", "", "## Final Recommendation", ""]
    L.append(
        "**Set the 2027 to 2029 establishment at %s: %d consular officers against %d in force, with %s, and %s.** Every district's "
        "estimated citizens stand %s or more from a %s line. This rejects the establishment of %s (%d officers) that the "
        "partner states' tables give when each state's arrivals and departures tables are taken as the moves and 2021 to "
        "%d are carried through 2024 to 2026: an arrivals table holds that state's own share of the arrivals, a "
        "departures table a fraction of the exits, and the moves of 2024 to 2026, which only Orlava's register saw, were "
        "not those of 2021 to %d." % (
            _list("%d officers in %s" % (f["officers"][h], h) if i == 0 else "%d in %s" % (f["officers"][h], h)
                  for i, h in enumerate(HOSTS)),
            f["officers_total"][1], f["officers_total"][0], ", ".join(up), _list(down), _n(margin), rate,
            _list("%d in %s" % (refl["officers"][h], h) for h in HOSTS), sum(refl["officers"].values()),
            n["years_tables"][1], n["years_tables"][1]))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], ""]
    L.append("1. The first sheet states the establishment, one row per district: the Orlavan citizens usually resident on 1 "
             "January 2027, the officers the Order gives and the citizens who moved away between the 2021 census and the "
             "end of 2026, with a chart of the seven counts against the %s lines. Each estimate's band is in brackets." % rate)
    k = 2
    for h in HOSTS:
        L.append("%d. %s: %s citizens usually resident on 1 January 2027 (%s), which the Order makes %d officers." % (
            k, h, _n(f["citizens"][h]), _b(f["citizens_band"][h]), f["officers"][h]))
        k += 1
    for h in HOSTS:
        L.append("%d. %s: %s citizens moved away between the census of 1 January 2021 and the end of 2026 (%s)." % (
            k, h, _n(f["left"][h]), _b(f["left_band"][h])))
        k += 1
    L += ["", "### %s" % deliver.FILES["csv"], ""]
    L.append("%d. One row per district and year from 2011: the citizens on 1 January and the year's arrivals, exits and "
             "births less deaths, each district's account closing on its count of 1 January 2027." % k)
    L += ["", "## Critical Components", ""]
    L.append("1. Of the Orlavan citizens who moved to the seven states in %d to %d, **%.1f per cent** deregistered in "
             "Orlava (band %s)." % (n["years_tables"][0], n["years_tables"][1], f["c1"], _b(f["c1_band"], 1)))
    L.append("2. Skarholm's departures table holds **%.1f per cent** of the Orlavan citizens who left Skarholm between its "
             "censuses of 1 January 2011 and 1 January 2021 (band %s)." % (f["c2"], _b(f["c2_band"], 1)))
    L.append("3. Orlavan citizens' exits from Tesmar in 2024 to 2026 were **%.2f** times those of 2021 to %d (band %s)." % (
        f["c3"], n["years_tables"][1], _b(f["c3_band"], 2)))
    L += ["", "## Step-by-Step", ""]
    riv = rf["rivals"]
    ho = f["held_out"]
    hc = f["hurried"]
    sp = f["spreads_pct"]
    y1 = n["years_tables"][1]
    cl, le = f["closure"], f["late_entries"]
    cap = cl["cap"]
    top = cap["top"]
    steps = [
        "Brought the files to one coding with `%s` (three digits in `%s`, three letters in the tables, two letters in the "
        "register). In `%s` kept, for each table, reporting state, partner, year, sex and age group, the latest release "
        "(Regulation %d/%d, article 6(3), `%s`): %s rows, %s superseded, %s cells, summed over sex and age to the %d "
        "ordered pairs of the %s states for Tables A to D, %d to %d. In `%s` counted a repeated event number once (%s "
        "rows, %s repeats, %s events), read the state from its code or, on the %s rows where the code is blank, from "
        "the clerk's text, and dated each event to the year of the move (article 2(e)); entries follow the move by up to "
        "%d days and the file's last entry is dated %s, %d days after the last move of 2026, so only the slowest entries of "
        "its last %s days can be outstanding (%.1f per cent of entries take longer than %d days: about %d of the %d moves "
        "dated in those days, which moves no figure). The register's yearly counts for %d to %d equal "
        "Orlava's own cells in the released tables to the unit. Each host's Table A holds these arrivals of Orlavan "
        "citizens over %d to %d: %s." % (
            F["codes"], F["census"], F["tables"], st["regulation_no"][0], st["regulation_no"][1], F["regulation"],
            _n(n["table_rows"]), _n(n["table_rows_superseded"]), _n(n["table_cells"]), n["pairs"], WORD.get(n["states"], "eight"),
            n["years_tables"][0], y1, F["register"], _n(n["register_rows"]), _n(n["register_repeats"]), _n(n["register_events"]),
            _n(n["blank_codes"]), n["entry_lag_max_days"], _date(n["entered_last"]), le["reach_days"], WORD.get(le["tail_days"], le["tail_days"]),
            le["over_reach_pct"], le["reach_days"], le["outstanding"], le["tail_moves"], n["years_tables"][0], y1, n["years_tables"][0], y1,
            _each(f["tabled_arrivals_2011_2023"])),
        "Measured what Orlava's own register records of arrivals, where a count exists: table %s of the 2021 census (`%s`) "
        "holds %s citizens of the seven states usually resident on 1 January 2021 who were abroad on 1 January 2020, and "
        "the register holds %s registrations from abroad of those citizenships with a move in 2020: %.1f per cent (%s per "
        "cent citizenship by citizenship; %.1f with the table's other citizenships counted in, which moves no officer)." % (
            st["c14"], F["c14"], _n(f["census_table_abroad_total"]), _n(f["register_arrivals_2020_total"]),
            f["share_home_arrivals_pct"], _b(f["share_home_arrivals_by_citizenship_pct"], 1), f["other_row"]["share_pct"]),
        "Every move between two states is reported twice: by the state left (Table B, its own citizens by state of next "
        "residence) and by the state entered (Table A, by citizenship). Taking Orlava's registered arrivals of a partner's "
        "citizens over %.1f per cent as that flow, the partner's Table B holds %s per cent of its own emigrants to Orlava "
        "(sum over %d to %d against sum). Taking each partner's Table B to a host over that share as the flow, the host's "
        "Table A holds, of the arrivals of the six other partners' citizens (sum of its Table A over the sum of those "
        "flows, %d to %d), %s per cent. A share above 100 per cent is kept as measured, a table that holds more arrivals "
        "than took place: each of the six senders puts %s's table at %s per cent of its own flow, and capped at 100 "
        "Orlava's register would hold %.1f per cent of its citizens' moves to %s against %s per cent in the other six "
        "hosts (%.1f as measured). The arrivals of Orlavan citizens in a host in each year to %d are its Table A over "
        "its share. Against them, Orlava's Table B holds %.1f per cent of the citizens who moved to the seven states "
        "(component 1). The hurried route takes each host's Table A as the arrivals (%.1f per cent) and puts Brennia at "
        "%s citizens, %d officers." % (
            f["share_home_arrivals_pct"], _rng(f["share_partner_emigrants_pct"].values()), n["years_tables"][0], y1,
            n["years_tables"][0], y1, _list("%s %.1f" % (h, f["share_host_arrivals_pct"][h]) for h in HOSTS),
            top, _b(cl["hosts"][top]["senders_pct"], 1), cap["hosts"][top]["home_moves_pct"], top,
            _b(cap["others_home_moves_pct"], 1), cap["hosts"][top]["home_moves_measured_pct"], y1,
            f["c1"], hc["c1"], _n(R["S1"]["citizens"]["Brennia"]), R["S1"]["officers"]["Brennia"]),
        "Closed each host's account between its two censuses (`%s`, sheets T1; births and deaths of Orlavan citizens in "
        "`%s`): the citizens who left from 1 January 2011 to 31 December 2020 are the 2011 count plus the arrivals of step "
        "3 plus births less deaths less the 2021 count, %s. The host's Table C holds %s per cent of them (component 2 is "
        "Skarholm's). Each share is closed on the Orlavan citizens' own account: pooled over the host's seven foreign "
        "citizenships Skarholm's would be %.1f per cent, which carries its 2011 count to %s on 1 January 2021 against "
        "the %s counted. The exits of each year to %d are Table C over that share. The hurried route takes Table C as the "
        "exits and puts Marovia at %s citizens, %d officers." % (
            F["census"], F["vital"], _each(f["exits_decade"]),
            _list("%s %.1f" % (h, f["share_host_departures_pct"][h]) for h in HOSTS),
            cl["pooled_departures"]["Skarholm"]["share_pct"], _n(cl["pooled_departures"]["Skarholm"]["census_2021"]),
            _n(f["census_2021"]["Skarholm"]), y1,
            _n(R["S2"]["citizens"]["Marovia"]), R["S2"]["officers"]["Marovia"]),
        "Checked steps 3 and 4 where a count exists that they do not use: `%s` holds %s Orlavan citizens on 1 January "
        "2016. Fenmark's 2011 census count carried five years by the arrivals and exits of steps 3 and 4 gives %s (%s "
        "off). Fenmark's tables at face value give %s (%s off); arrivals as tabled with Table C scaled to close 2011 to "
        "2021, %s (%s); the larger of the two reports of every flow, %s (%s); the recording shares scaled so that the "
        "fullest recorder is complete, %s (%s); scaled so that the seven hosts' shares have a geometric mean of one, %s (%s)." % (
            F["count16"], _n(rf["count"]), _n(rf["golden"]), _n(rf["off"]),
            _n(riv["the host's tables at face value"]["value"]), _n(riv["the host's tables at face value"]["off"]),
            _n(riv["arrivals as recorded, the account closed on departures"]["value"]),
            _n(riv["arrivals as recorded, the account closed on departures"]["off"]),
            _n(riv["the larger report of each flow"]["value"]), _n(riv["the larger report of each flow"]["off"]),
            _n(riv["shares scaled to the fullest recorder"]["value"]), _n(riv["shares scaled to the fullest recorder"]["off"]),
            _n(riv["shares scaled about their own average"]["value"]), _n(riv["shares scaled about their own average"]["off"])),
        "The partner states' tables end with %d (the %s release; article 6(1) gives a state %d months), and only Orlava's "
        "register reaches the end of 2026. Over %d to %d its deregistrations to a host were %s per cent of the citizens "
        "who moved there (step 3) and its registrations of citizens from a host %s per cent of the citizens who left it "
        "(step 4), sum against sum, host by host. The arrivals and exits of 2024 to 2026 are the register's "
        "deregistrations and registrations over those shares; births less deaths are each district's rate of 2021 to %d "
        "(the three years' births less deaths over the sum of the citizens on 1 January of each) on the citizens at the "
        "start of the year. Exits from Tesmar come to %.2f times those of 2021 to %d (component 3; the register's "
        "registrations from Tesmar rose from %s to %s). The hurried route carries the mean arrivals and the exit rate of "
        "2021 to %d through 2024 to 2026 (a ratio of %.2f) and puts Tesmar at %s citizens, %d officers. Held out, the arrivals of "
        "2021 to %d read from the register at its share of %d to 2020 against those of step 3: %s; the years 2018 to 2020 "
        "carried give %s." % (
            y1, st["release"], st["months"], n["years_tables"][0], y1, _rng(f["share_home_moves_pct"].values()),
            _rng(f["share_home_exits_pct"].values()), y1, f["c3"], y1, _n(f["register_returns_2021_2023"]["Tesmar"]),
            _n(f["register_returns_2024_2026"]["Tesmar"]), y1, f["routes_c"]["C3"]["S3"], _n(R["S3"]["citizens"]["Tesmar"]),
            R["S3"]["officers"]["Tesmar"], y1, n["years_tables"][0],
            _list("%s %s against %s" % (h, _n(ho[h]["register_scaled"]), _n(ho[h]["arrivals"])) for h in HOSTS),
            _list("%s %s" % (h, _n(ho[h]["carried"])) for h in HOSTS)),
        "Carried each 2021 census count to 1 January 2027 by the arrivals, exits and births less deaths of 2021 to 2026 "
        "(to 1 January 2024: %s): %s citizens, which at one officer for every %s or part of %s (Order No. %d of %d, "
        "clause 2.1, `%s`) is %s officers, against %s in force (`%s`). The citizens who moved away from 1 January 2021 "
        "to 31 December 2026 (clause 4.1) are the exits of those six years: %s." % (
            _each(f["citizens_2024"]), _each(f["citizens"]), rate, rate, st["order_no"], st["order_year"], F["order"],
            _each(f["officers"], "%s %s", False), _each(f["officers_in_force"], "%s %s", False), F["estab"], _each(f["left"])),
        "Rebuilt the route %d ways: Orlava's arrival share as the mean or the median of the seven citizenships' ratios; a "
        "host's share as the mean or the median of the six senders' ratios, or without its smallest sender; the shares of "
        "step 3 fitted on 2014 to %d, 2016 to %d or 2011 to 2020; the register's shares of step 6 on 2016 to %d, 2019 to "
        "%d, 2021 to %d or 2011 to 2020, or one share for all seven hosts; a host's exits to %d timed by Orlava's "
        "registrations from it in place of its Table C; births less deaths after %d as the mean yearly count of 2021 to "
        "%d; the level of the shares taken from Fenmark's two five-year accounts (2011 to 2016 and 2016 to 2021) in "
        "place of the census table; and every two of these that change different choices. Every rebuild files the same "
        "officers (%s); the nearest any comes to a %s line is %s citizens (%s at %s). Each band is the range of the "
        "rebuilds widened by a quarter of that range at each end, to the ten outward (a tenth of a per cent and a "
        "hundredth for the components). With each host's fitted shares moved by the furthest any rebuild moves that host's "
        "own (across the hosts, an arrival share by %s per cent, a departure share by %s, the register's share of moves by "
        "%s and of exits by %s), singly or all four together, the officers stay." % (
            f["variants"], y1, y1, y1, y1, y1, y1, y1, y1,
            "; ".join("%s %s to %s" % (h, _n(f["variant_range"][h][0]), _n(f["variant_range"][h][1])) for h in HOSTS),
            rate, _n(f["nearest_variant"]["distance"]), f["nearest_variant"]["host"], _n(f["nearest_variant"]["citizens"]),
            _rng(sp[h]["x_a"] for h in HOSTS), _rng(sp[h]["x_d"] for h in HOSTS), _rng(sp[h]["x_b"] for h in HOSTS),
            _rng(sp[h]["x_r"] for h in HOSTS)),
    ]
    for i, s in enumerate(steps):
        L.append("%d. %s" % (1 + i, s))
    rg, mn, dr, mr = R["rigorous"], R["mean"], R["direct"], R["mirror"]
    fits = cl["fits"]
    mq = cl["census_2021_miss_quoted"]
    lv = cl["level"]
    out_hosts = cl["outside_senders"]
    L += ["",
          "No other establishment survives the files. Each state's tables at face value pass their own arithmetic and "
          "miss both counts that test them: they put Fenmark at %s on 1 January 2016 against the %s counted, and from "
          "the 2011 censuses they miss the 2021 censuses by %s citizens over the seven hosts. The two reports of a flow "
          "fix the recording shares against each other and not their level, so three other levels were tried: with "
          "the fullest recorder taken as complete Orlava's register would hold %.1f per cent of its foreign arrivals, "
          "and with the hosts' shares scaled to a geometric mean of one %.1f per cent, where the census table counts "
          "%.1f; carried through steps 4 to 7 as the estimate is, they miss Fenmark's 2016 count by %s and %s and file "
          "%s and %s officers; the larger of the two reports of every flow, with 2021 to %d repeated through 2024 to "
          "2026, misses it by %s and files %s. The hosts' own tables at face value reach 1 January 2024, which is not "
          "the date of clause 2.1, and taken as the count file %s." % (
              _n(riv["the host's tables at face value"]["value"]), _n(rf["count"]), _n(f["face_value_census_gap"]),
              f["rigorous_home_share_pct"], f["mean_route_home_share_pct"], f["share_home_arrivals_pct"],
              _n(riv["shares scaled to the fullest recorder"]["off"]), _n(riv["shares scaled about their own average"]["off"]),
              sum(rg["officers"].values()), sum(mn["officers"].values()), y1, _n(riv["the larger report of each flow"]["off"]),
              sum(mr["officers"].values()), sum(dr["officers"].values())),
          "",
          "The files afford one more route, which needs neither the second report of a flow nor the census table: each "
          "host's two shares fitted on its own census accounts of its seven foreign citizenships (each citizenship's "
          "change between the two censuses less its births less deaths, against its Table A and Table C sums for %d to "
          "2020). Under %s weightings (none, by arrivals, by the 2011 count, by the square of arrivals), with the "
          "departure share fitted or closed on the Orlavan account, it files the same %d officers and comes no nearer a "
          "line than %s citizens (%s at %s), but it fixes no figure: its 95 per cent interval on Skarholm's arrival share "
          "runs %s per cent; in %s of the seven hosts its share lies outside what any of the six senders' reports give "
          "(%s); with both shares fitted it carries the 2011 census counts of Orlavan citizens to %s above the 2021 "
          "count in %s and %s below it in %s; and it misses Fenmark's 2016 count by %s against the estimate's %s. Used "
          "for what the two reports leave open, the level, the same %d accounts (the reports' ratios between the hosts "
          "kept, one factor on every host's share, each host's departure share fitted across its citizenships, by least "
          "squares under the same weightings with the accounts pooled or each host's weighed equally) put Orlava's "
          "arrival share at %s per cent against the census table's %.1f, and every figure stays inside its band, alone "
          "and with each other single choice of step 8 (%d rebuilds)." % (
              n["years_tables"][0], WORD.get(cl["weightings"], cl["weightings"]), cl["officers_total"],
              _n(cl["nearest_line"]["distance"]), cl["nearest_line"]["host"], _n(cl["nearest_line"]["citizens"]),
              _b(cl["hosts"]["Skarholm"]["interval_pct"], 1), WORD.get(len(out_hosts), len(out_hosts)),
              _list("%s %.1f per cent against %s" % (h, cl["hosts"][h]["share_pct"], _b(cl["hosts"][h]["senders_pct"], 1)) for h in out_hosts),
              _n(mq["over"]["by"]), mq["over"]["host"], _n(mq["under"]["by"]), mq["under"]["host"],
              _b(cl["referee_off"]), _n(rf["off"]), lv["accounts"], _b(lv["home_share_pct"], 1), f["share_home_arrivals_pct"],
              lv["rebuilds"]),
          "",
          "Carrying 2021 to %d forward keeps every earlier check and fails the one that tests it: the register, at "
          "shares fitted on %d to 2020, reproduces the arrivals of 2021 to %d that the carry of 2018 to 2020 misses, "
          "and it shows the moves of 2024 to 2026 changed. All three shortcuts together file %d officers where the "
          "estimate files %d." % (y1, n["years_tables"][0], y1, sum(refl["officers"].values()), f["officers_total"][1]), ""]
    open(path, "w").write("\n".join(L))
