"""The simulated business, month by month from January 2023 to December 2027.

Accounts start a trial (a spring campaign's 30 days, or 14 days organically), pay monthly on their billing day by web
(iDEAL then SEPA direct debit, or card) or through an app store, switch plans, and end; a Gezin or Onbeperkt account
holds more than one profile, profiles are added, removed, and moved out to accounts of their own at a month start.
Each profile listens title by title: new progress through the titles it is reading, and re-listening of titles it has
finished (children above all), streamed or played from a download. The app reports a streamed title's position as it
plays (the warehouse rolls the reports up by profile, title and month); a downloaded title's position reaches the
licence server only when the device renews the title's licence, which can fall in the next month or, once the
subscription has ended, never. The remuneration engine counts, per profile and title, the rise in the furthest
position any report shows, in the month of the report; that count is the clean truth here and is rebuilt from the
shipped records by methods.py.
"""
import datetime as dt
import math

import numpy as np

import params as P

KIDS_SHARE = 0.22


def catalogue(rng):
    """About 4,000 titles across 40 publishers, the service's own productions and public-domain recordings."""
    pubs = []
    for i in range(P.N_PUBLISHERS):
        size = float(rng.lognormal(0, 0.9))
        kids = float(rng.beta(1.2, 5.0))
        pubs.append({"i": i, "size": size, "kids": kids})
    w = np.array([p["size"] for p in pubs])
    titles = []
    n = 4100
    for t in range(n):
        r = rng.random()
        if r < 0.035:
            pub, own, pd = -1, True, False
        elif r < 0.06:
            pub, own, pd = -2, False, True
        else:
            pub, own, pd = int(rng.choice(P.N_PUBLISHERS, p=w / w.sum())), False, False
        kidsp = pubs[pub]["kids"] if pub >= 0 else 0.15
        kids = bool(rng.random() < kidsp)
        dur = float(rng.lognormal(math.log(1.4), 0.55)) if kids else float(rng.lognormal(math.log(9.5), 0.45))
        dur = min(max(dur, 0.25 if kids else 1.5), 4.5 if kids else 38.0)
        pop = float(rng.lognormal(0, 1.1))
        titles.append({"t": t, "pub": pub, "own": own, "pd": pd, "kids": kids, "dur": round(dur, 4), "pop": pop})
    return pubs, titles


class Profile:
    __slots__ = ("pid", "acc", "adult", "created", "removed", "intensity", "commuter", "offline_pref", "relisten",
                 "speed", "devices", "current", "finished", "furthest", "dev_pos", "pending", "owner", "history",
                 "rng", "first_month")

    def __init__(self, pid, acc, adult, created, plan, rng, owner):
        self.pid, self.acc, self.adult, self.created, self.removed = pid, acc, adult, created, None
        self.owner = owner
        self.rng = rng
        base = P.HOURS[plan] if adult else P.CHILD_HOURS
        self.intensity = float(rng.lognormal(math.log(base), 1.05 if (adult and plan == "ONB") else 0.55))
        self.commuter = bool(rng.random() < (P.COMMUTER[plan] if adult else 0.0))
        if adult:
            self.offline_pref = float(rng.beta(9, 1.6)) if self.commuter else float(rng.beta(1.0, 14))
        else:
            self.offline_pref = float(rng.beta(1.4, 12))
        self.relisten = float(rng.beta(1.2, 22)) if adult else float(rng.beta(9, 3))
        self.speed = float(rng.choice([1.0, 1.0, 1.0, 1.1, 1.25, 1.25, 1.5, 1.75, 2.0])) if adult else 1.0
        nd = 1 + int(rng.random() < (0.45 if self.commuter else 0.2))
        self.devices = ["D%07d" % int(rng.integers(1000000, 9999999)) for _ in range(nd)]
        self.current = []      # [title, downloaded, device]
        self.finished = []
        self.furthest = {}     # title -> furthest position reached anywhere (hours)
        self.dev_pos = {}      # (device, title) -> furthest position on that device
        self.pending = []      # (title, device, position) offline progress not yet reported
        self.history = [(created, acc)]
        self.first_month = created


def _pick_title(rng, titles, kids_idx, adult_idx, adult, prof):
    pool = adult_idx if (adult and rng.random() > 0.06) else kids_idx
    for _ in range(6):
        t = pool[int(rng.integers(len(pool)))]
        if t not in prof.furthest:
            return t
    return pool[int(rng.integers(len(pool)))]


def _choose_pool(titles, adult):
    w = np.array([titles[i]["pop"] for i in range(len(titles))])
    return w


def simulate(seed=P.SEED, rise27=P.RISE27, seed27=None):
    """seed27 (the clean truth only) redraws every account's and profile's stream from January 2027, so the
    2027 can be replayed many times on the same October 2026 world; the shipped records end before it."""
    rng = np.random.default_rng(seed)
    pubs, titles = catalogue(rng)
    pop = np.array([t["pop"] for t in titles])
    kids_idx = [t["t"] for t in titles if t["kids"]]
    adult_idx = [t["t"] for t in titles if not t["kids"]]
    # popularity-weighted pools, pre-drawn per pick
    kc = np.cumsum(pop[kids_idx] / pop[kids_idx].sum())
    ac = np.cumsum(pop[adult_idx] / pop[adult_idx].sum())

    accounts, profiles = [], []
    live, licences, counted, charges, spells, invoices_profiles = [], [], [], [], [], []
    acc_state = {}
    next_acc = [710000]
    next_prof = [2600000]

    def new_account(m, day, plan, source, trial_days, route=None, country=None, kind="consumer", start_profiles=None,
                    rng_a=None):
        r = rng_a if rng_a is not None else np.random.default_rng(int(rng.integers(1 << 62)))
        aid = "K%07d" % (next_acc[0] + int(r.integers(1, 23)))
        next_acc[0] = int(aid[1:])
        country = country or str(r.choice(list(P.COUNTRY), p=list(P.COUNTRY.values())))
        route = route or str(r.choice(list(P.ROUTE), p=list(P.ROUTE.values())))
        a = {"aid": aid, "country": country, "route": route, "created": (m, day), "kind": kind, "source": source,
             "trial_days": trial_days, "plan": plan, "rng": r, "profiles": [], "status": "trial" if trial_days else "paid",
             "bill_day": None, "paid_months": 0, "tenure": 0, "end": None, "eng": 0.0, "plan_hist": [],
             "store_paid": 0}
        if trial_days:
            d = P.month_start(m) + dt.timedelta(days=day - 1 + trial_days)
            fm = (d.year - P.M0_YEAR) * 12 + d.month - 1
            a["first_charge"] = (fm, min(d.day, 28))
        else:
            a["first_charge"] = (m, day)
        a["bill_day"] = a["first_charge"][1]
        accounts.append(a)
        acc_state[aid] = a
        if start_profiles is None:
            npf = 1
            kids = 0
            if plan == "ONB":
                npf = 1 + int(r.random() < 0.33)
            if plan == "GEZ":
                npf = int(r.choice([2, 3, 3, 4]))
                kids = int(r.binomial(npf - 1, 0.62))
            for k in range(npf):
                adult = k < npf - kids
                pr = Profile("P%07d" % (next_prof[0] + int(r.integers(1, 9))), aid, adult, m, plan,
                             np.random.default_rng(int(r.integers(1 << 62))), owner=(k == 0))
                next_prof[0] = int(pr.pid[1:])
                profiles.append(pr)
                a["profiles"].append(pr)
        else:
            for pr in start_profiles:
                a["profiles"].append(pr)
        a["plan_hist"].append((m, plan, "trial" if trial_days else "paid"))
        return a

    # the base in January 2023: paying accounts with tenures up to four years
    for i in range(P.BASE0):
        plan = str(rng.choice(P.PLANS, p=[0.27, 0.37, 0.25, 0.11]))
        a = new_account(0, int(rng.integers(1, 29)), plan, "organic", 0)
        a["tenure"] = int(rng.integers(3, 48))
        a["orig_start"] = P.month_start(0) - dt.timedelta(days=30 * a["tenure"] + int(rng.integers(0, 28)))
        for pr in a["profiles"]:
            pr.created = -a["tenure"]
            pr.first_month = -a["tenure"]
    # staff and test accounts
    for i in range(46):
        a = new_account(int(rng.integers(0, 30)), int(rng.integers(1, 29)), "ONB", "medewerker", 0, route="web",
                        kind="staff")
    for i in range(17):
        a = new_account(int(rng.integers(12, 44)), int(rng.integers(1, 29)), str(rng.choice(P.PLANS)), "test", 0,
                        route=str(rng.choice(["web", "apple", "google"])), kind="test")

    tit = titles

    def listen(pr, a, m, trial):
        r = pr.rng
        cal = m % 12
        ten = m - pr.first_month
        fade = 0.74 + 0.26 * math.exp(-max(ten, 0) / 5.0)
        h = pr.intensity * P.SEASON[cal] * fade * float(r.lognormal(0, 0.33)) * (1.38 if trial else 1.0)
        if r.random() < (0.07 if pr.adult else 0.05):
            h *= 0.05
        cap = P.CAP[a["plan"]]
        if cap is not None and h > cap:
            h = cap * float(r.uniform(0.93, 1.0))
            a["capped_now"] = True
        h_re = h * pr.relisten if pr.finished else 0.0
        h_new = h - h_re
        rows = {}

        def live_add(t, hours, pos_end):
            k = rows.setdefault(t, [0.0, 0.0])
            k[0] += hours * 3600.0 / pr.speed
            k[1] = max(k[1], pos_end)

        # new progress through the current titles
        guard = 0
        while h_new > 1e-6 and guard < 40:
            guard += 1
            if len(pr.current) < 2 or (not pr.current):
                if pr.adult and r.random() > 0.06:
                    t = adult_idx[min(int(np.searchsorted(ac, r.random())), len(adult_idx) - 1)]
                else:
                    t = kids_idx[min(int(np.searchsorted(kc, r.random())), len(kids_idx) - 1)]
                if t in pr.furthest and pr.furthest[t] >= tit[t]["dur"] - 1e-9:
                    continue
                dl = bool(r.random() < pr.offline_pref)
                dev = pr.devices[-1] if (dl and len(pr.devices) > 1) else pr.devices[0]
                pr.current.append([t, dl, dev])
            slot = pr.current[0] if r.random() < 0.78 else pr.current[-1]
            t, dl, dev = slot
            dur = tit[t]["dur"]
            pos = pr.furthest.get(t, 0.0)
            take = min(h_new, dur - pos, float(r.uniform(0.6, 4.5)))
            if r.random() < 0.012 * take:      # abandoned part-way
                pr.current.remove(slot)
                pr.finished.append(t)
                continue
            new_pos = pos + take
            offline = dl and r.random() < 0.9
            if offline:
                pr.dev_pos[(dev, t)] = max(pr.dev_pos.get((dev, t), 0.0), new_pos)
                pr.pending.append((t, dev, new_pos))
            else:
                live_add(t, take, new_pos)
                if dl:
                    pr.dev_pos[(dev, t)] = max(pr.dev_pos.get((dev, t), 0.0), new_pos)
            pr.furthest[t] = new_pos
            h_new -= take
            if new_pos >= dur - 1e-9:
                pr.current.remove(slot)
                pr.finished.append(t)
        # re-listening of finished titles (positions below the furthest)
        while h_re > 1e-6 and pr.finished:
            t = pr.finished[int(r.integers(max(1, len(pr.finished) - 6), len(pr.finished) + 1)) - 1] \
                if r.random() < 0.9 else pr.finished[int(r.integers(len(pr.finished)))]
            dur = tit[t]["dur"]
            take = min(h_re, dur, float(r.uniform(0.3, 2.0)))
            start = float(r.uniform(0, max(dur - take, 0.0)))
            home = (not pr.adult and r.random() < 0.72) or (pr.adult and r.random() < 0.6)
            if home:
                live_add(t, take, start + take)
            h_re -= take
        return rows

    def report_licences(pr, a, m, alive_next):
        """Offline progress reaches the licence server at renewals: most in the month, the rest at an early
        renewal next month while the subscription still runs, never once it has ended."""
        r = pr.rng
        keep = []
        by_key = {}
        for t, dev, pos in pr.pending:
            by_key[(dev, t)] = max(by_key.get((dev, t), 0.0), pos)
        out = []
        for (dev, t), pos in by_key.items():
            prev = pr.dev_pos.get(("rep", dev, t), 0.0)
            if pos <= prev + 1e-9:
                continue
            n = 1 + int(r.poisson(0.35))
            days = sorted(int(x) for x in r.integers(1, P.days_in(m) + 1, size=n))
            late = r.random() < 0.3
            reach = pos if not late else prev + (pos - prev) * float(r.uniform(0.45, 0.9))
            for j, d in enumerate(days):
                p = prev + (reach - prev) * (j + 1) / n
                out.append((m, d, int(r.integers(0, 86400)), dev, t, p))
            pr.dev_pos[("rep", dev, t)] = reach
            if late and alive_next:
                keep.append((t, dev, pos))
        pr.pending = keep
        return out

    def report_late(pr, m):
        r = pr.rng
        out = []
        for t, dev, pos in pr.pending:
            d = int(r.integers(1, 11))
            out.append((m, d, int(r.integers(0, 86400)), dev, t, pos))
            pr.dev_pos[("rep", dev, t)] = max(pr.dev_pos.get(("rep", dev, t), 0.0), pos)
        pr.pending = []
        return out

    engine = {}   # (pid, t) -> furthest reported

    def engine_count(pid, t, pos, m, aid):
        k = (pid, t)
        prev = engine.get(k, 0.0)
        if pos > prev + 1e-9:
            engine[k] = pos
            if tit[t]["pub"] >= 0:
                counted.append((m, pid, aid, t, pos - prev))

    for m in range(0, P.END + 1):
        if seed27 is not None and m == P.Y2027[0]:
            for a in accounts:
                a["rng"] = np.random.default_rng([seed27, int(a["aid"][1:])])
            for pr in profiles:
                pr.rng = np.random.default_rng([seed27, int(pr.pid[1:]), 1])
        # acquisition
        y = P.ym(m)[0]
        if m % 12 in (0, 1, 2) and y in P.CAMPAIGN:
            n = int(rng.poisson(P.CAMPAIGN[y] / 3.0))
            for _ in range(n):
                plan = str(rng.choice(P.PLANS, p=list(P.CAMPAIGN_MIX.values())))
                new_account(m, int(rng.integers(1, 29)), plan, "VJ%02d-%s" % (y % 100, plan), 30)
        if y <= 2026 or m <= P.END:
            n = int(rng.poisson(P.ORGANIC * (1.0 + 0.012 * m) * (1.25 if m % 12 in (8, 9) else 1.0)))
            if y >= 2027:
                n = 0
            for _ in range(n):
                plan = str(rng.choice(P.PLANS, p=list(P.ORGANIC_MIX.values())))
                new_account(m, int(rng.integers(1, 29)), plan, "organic", 14)
        _moves(m, accounts, rng, new_account, P)
        ia = 0
        while ia < len(accounts):
            a = accounts[ia]
            ia += 1
            if a["end"] is not None or a["created"][0] > m:
                continue
            r = a["rng"]
            plan = a["plan"]
            fm, fd = a["first_charge"]
            trial_month = a["trial_days"] and (a["created"][0] == m) and fm > m
            charge_month = (m >= fm)
            if a["status"] == "trial" and m == fm:
                # the trial converts or not
                q = P.CONVERT[plan] * (1.0 + 0.25 * math.tanh(a["eng"]))
                if a["kind"] != "consumer" or r.random() < q:
                    a["status"] = "paid"
                    a["plan_hist"].append((m, plan, "paid"))
                else:
                    a["end"] = (m, "trial_not_converted")
                    for pr in a["profiles"]:
                        pr.removed = pr.removed or m
                    continue
            if a["status"] == "paid" and charge_month and a["paid_months"] > 0:
                # leave at the end of the cycle, switch plan, or carry on
                ten = a["paid_months"] + a.get("tenure", 0)
                hz = P.CHURN[plan] * (1.45 if ten <= 3 else 1.0 if ten <= 12 else 0.72)
                hz *= math.exp(-0.32 * a["eng"]) * (1.0 + 0.08 * math.sin(2 * math.pi * (m % 12 - 7) / 12))
                if a.get("capped_now"):
                    hz *= 2.3
                new_p = P.price_of(plan, a["country"], m, rise27)
                old_p = a.get("last_price")
                lt = min(max(math.exp(-P.ANN_SEL * a["eng"]), 0.2), 4.0)
                if a["kind"] == "consumer" and m % 12 == 11 and P.price_of(plan, a["country"], m + 1, rise27) > new_p + 1e-9:
                    hz += P.ANNOUNCE * lt          # told by e-mail on 1 December, some leave at the December bill
                if a["kind"] == "consumer" and old_p and new_p > old_p + 1e-9:
                    # the first bill at a higher price: some leave, some move down a plan, the more so where the
                    # new price passes the rival's comparable plan
                    pct = (new_p - old_p) / old_p
                    cross = old_p <= P.rival_of(a["country"], plan, m) < new_p
                    a["rise_m"], a["rise_cross"] = m, cross
                    light = min(max(math.exp(-P.SEL * a["eng"]), 0.3), 3.2)   # light listeners answer a rise first
                    heavy = min(max(math.exp(P.SEL_X * a["eng"]), 0.3), 3.2)  # past the rival, heavy ones switch
                    hz += (0.008 + 0.30 * pct) * light + (P.STEP * heavy if cross else 0.0)
                    pdown = (0.006 + 0.20 * pct + (P.STEP_DOWN if cross else 0.0)) * light
                    lower = {"STD": "FLEX", "ONB": "STD", "GEZ": "ONB"}.get(plan)
                    if lower and r.random() < pdown and len(a["profiles"]) <= P.MAX_PROFILES[lower]:
                        a["plan"] = plan = lower
                        a["plan_hist"].append((m, lower, "paid"))
                        hz = 0.0
                elif (a["kind"] == "consumer" and m >= P.Y2027[0] and old_p and not a.get("bill27")
                      and plan in ("STD", "ONB", "GEZ")):
                    r.random()       # the draw a rise would take, so a held price and a rise replay the same 2027
                if m >= P.Y2027[0]:
                    a["bill27"] = True
                if a["kind"] == "consumer" and r.random() < hz:
                    a["end"] = (m, "cancelled")
                    for pr in a["profiles"]:
                        pr.removed = pr.removed or m
                    continue
                if a["kind"] == "consumer" and r.random() < 0.011:
                    alt = {"FLEX": ["STD"], "STD": ["FLEX", "ONB"], "ONB": ["STD", "GEZ"], "GEZ": ["ONB"]}[plan]
                    nw = str(r.choice(alt))
                    if not (nw in ("FLEX", "STD") and len(a["profiles"]) > 1):
                        a["plan"] = plan = nw
                        a["plan_hist"].append((m, nw, "paid"))
            # profiles added to family accounts, moved out at a month start, removed
            if a["kind"] == "consumer" and a["status"] == "paid":
                cap = P.MAX_PROFILES[plan]
                share = P.SHARE_ADD if (len(a["profiles"]) == 1 and 1 <= m - a.get("rise_m", -99) <= 3) else 0.0  # one user starts to share
                if len(a["profiles"]) < cap and r.random() < (0.012 if plan == "GEZ" else 0.006) + share:
                    pr = Profile("P%07d" % (next_prof[0] + int(r.integers(1, 9))), a["aid"], plan == "ONB" or
                                 r.random() < 0.5, m, plan, np.random.default_rng(int(r.integers(1 << 62))), owner=False)
                    next_prof[0] = int(pr.pid[1:])
                    profiles.append(pr)
                    a["profiles"].append(pr)
                for pr in list(a["profiles"]):
                    if not pr.owner and r.random() < 0.0025:
                        a["profiles"].remove(pr)
                        pr.removed = m
            # this month's charge
            access = trial_month or (a["status"] == "paid" and charge_month)
            if a["status"] == "paid" and charge_month:
                day = min(a["bill_day"], P.days_in(m))
                price = P.price_of(plan, a["country"], m, rise27)
                a["last_price"] = price
                status = "collected"
                if a["kind"] != "consumer":
                    price, status = 0.0, "collected"
                elif a["route"] == "web" and r.random() < 0.024:
                    status = "returned"
                elif r.random() < 0.004:
                    status = "refunded"
                charges.append({"aid": a["aid"], "m": m, "day": day, "plan": plan, "price": price, "status": status,
                                "route": a["route"], "country": a["country"], "paid_idx": a["store_paid"] + 1,
                                "profiles": [p.pid for p in a["profiles"]]})
                if status == "returned":
                    if r.random() < 0.78:
                        charges.append({"aid": a["aid"], "m": m, "day": min(day + 5, P.days_in(m)), "plan": plan,
                                        "price": price, "status": "re-presented", "route": a["route"],
                                        "country": a["country"], "paid_idx": a["store_paid"] + 1,
                                        "profiles": [p.pid for p in a["profiles"]]})
                        status = "collected"
                    else:
                        a["end"] = (m, "debit_returned")
                if status == "refunded":
                    a["end"] = (m, "refunded")
                if status == "collected":
                    a["paid_months"] += 1
                    a["store_paid"] += 1
            if access:
                a["capped_now"] = False
                tot = 0.0
                for pr in a["profiles"]:
                    rows = listen(pr, a, m, trial_month)
                    for t, (secs, pos) in rows.items():
                        live.append((m, pr.pid, t, secs, pos))
                        engine_count(pr.pid, t, pos, m, a["aid"])
                        tot += secs / 3600.0
                    alive_next = a["end"] is None
                    for ev in report_licences(pr, a, m, alive_next):
                        licences.append((ev[0], ev[1], ev[2], ev[3], pr.pid, ev[4], ev[5]))
                        engine_count(pr.pid, ev[4], ev[5], m, a["aid"])
                a["eng"] = 0.7 * a["eng"] + 0.3 * (math.log1p(tot) - 2.2)
            # late licence reports from last month's play
            for pr in a["profiles"]:
                if pr.pending and not access:
                    pr.pending = []
            if a["end"] is not None:
                for pr in a["profiles"]:
                    pr.pending = []
        # late reports reach the engine next month while the subscription still runs
        _flush_late(accounts, m, report_late, licences, engine_count)
    return {"pubs": pubs, "titles": titles, "accounts": accounts, "profiles": profiles, "live": live,
            "licences": licences, "counted": counted, "charges": charges}


def _flush_late(accounts, m, report_late, licences, engine_count):
    """Progress held back at the month's last renewal reaches the server early in the next month."""
    nm = m + 1
    if nm > P.END:
        return
    for a in accounts:
        if a["end"] is not None:
            continue
        for pr in a["profiles"]:
            if pr.pending:
                for ev in report_late(pr, nm):
                    licences.append((ev[0], ev[1], ev[2], ev[3], pr.pid, ev[4], ev[5]))
                    engine_count(pr.pid, ev[4], ev[5], nm, a["aid"])


def _moves(m, accounts, rng, new_account, P):
    """At a month start, a partner or a grown child folds their own single-profile subscription into a Gezin
    account (or an Onbeperkt account's second profile): the profile keeps its id and history, joins the family
    account, and the old subscription is cancelled. A smaller flow runs the other way, a profile leaving a family
    account for a subscription of its own."""
    if m >= P.END:
        return
    live = [a for a in accounts if a["end"] is None and a["kind"] == "consumer" and a["status"] == "paid"
            and a["created"][0] < m]
    donors = [a for a in live if len(a["profiles"]) == 1 and a["plan"] in ("FLEX", "STD", "ONB")
              and a["paid_months"] >= 3 and a["profiles"][0].adult]
    used = set()
    for a in live:
        r = a["rng"]
        room = P.MAX_PROFILES[a["plan"]] - len(a["profiles"])
        p_in = 0.13 if a["plan"] == "GEZ" else (0.006 if a["plan"] == "ONB" else 0.0)
        if room > 0 and donors and r.random() < p_in:
            for _ in range(5):
                d = donors[int(r.integers(len(donors)))]
                if d["profiles"] and d["profiles"][0].intensity < 9.0 and r.random() < 0.5:
                    continue
                if d["aid"] not in used and d["aid"] != a["aid"] and d["country"] == a["country"]:
                    break
            else:
                continue
            used.add(d["aid"])
            pr = d["profiles"].pop()
            d["end"] = (m, "cancelled")
            d["moved_out"] = m
            pr.acc = a["aid"]
            pr.owner = False
            pr.history.append((m, a["aid"]))
            a["profiles"].append(pr)
        for pr in list(a["profiles"]):
            if pr.owner or not pr.adult:
                continue
            p_out = 0.0035 if a["plan"] == "GEZ" else 0.004
            if r.random() < p_out:
                a["profiles"].remove(pr)
                nplan = str(r.choice(["ONB", "STD", "FLEX"], p=[0.5, 0.35, 0.15]))
                b = new_account(m, 1, nplan, "organic", 0, route="web", country=a["country"], start_profiles=[pr],
                                rng_a=np.random.default_rng(int(r.integers(1 << 62))))
                pr.acc = b["aid"]
                pr.owner = True
                pr.history.append((m, b["aid"]))
