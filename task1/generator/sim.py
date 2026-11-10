"""The process behind Tekenbord's files, simulated month by month.

Business accounts hold annual seat contracts: they true up seats mid-term when more people need the product than
they licensed, and at each anniversary they renew (repricing to the new list from March 2026 at a negotiated
uplift), cut seats toward the people actually working in the product, or leave. Parent groups that consolidate their
software vendors take their subsidiaries' accounts with them at each one's next renewal. Team accounts pay monthly
per member, from April 2026 for at least three seats, upgrade to Business once they grow, and cancel on a hazard
that falls with age. Sales opportunities move through four stages and go cold when they stall. Every file is a view
of this one process; nothing is added where a result is decided."""
import copy
import math

import numpy as np

import params as P


def ym(m):
    y, mo = divmod(P.M0_MONTH - 1 + m, 12)
    return P.M0_YEAR + y, mo + 1


def trend(a, b, m, m_a, m_b):
    t = min(max((m - m_a) / float(m_b - m_a), 0.0), 1.0)
    return a + (b - a) * t


class World:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.parents = []
        self.bus = []
        self.team = []
        self.opps = []
        self.next_id = {"P": 4100, "B": 20000, "T": 700000, "O": 310000, "W": 5000}
        self.record = True
        self.log = {"lines": [], "team_inv": [], "ws": [], "snap": [], "opp_closed": [], "ws_map": [],
                    "events": []}
        self.flows = None
        self.cut_ids = set()

    # ------------------------------------------------------------------ ids
    def nid(self, k, step=None):
        r = self.rng
        self.next_id[k] += int(step if step else r.integers(1, 9))
        return self.next_id[k]

    # ------------------------------------------------------------------ parents and accounts
    def new_parent(self, group):
        r = self.rng
        pid = self.nid("P", 3)
        self.parents.append({"id": pid, "group": group, "consolidating": False, "cons_month": None,
                             "country": None})
        return self.parents[-1]

    def new_workspace(self, owner, m, share):
        wid = self.nid("W", 1)
        ws = {"id": wid, "share": share, "owner": owner, "from": m, "noise": float(self.rng.normal(0, 0.05))}
        if self.record:
            self.log["ws_map"].append({"ws": wid, "owner": owner, "from": m, "to": None})
        return ws

    def new_business(self, m, seats_need, currency, parent, source, team_ws=None):
        r = self.rng
        u = float(np.clip(r.normal(P.UTIL_MEAN, P.UTIL_SD), 0.38, 0.99))
        seats = max(5, int(math.ceil(seats_need / u)))
        disc = float(np.clip(0.04 + 0.035 * math.log(max(seats, 5) / 20.0) + r.normal(0, 0.035), 0.0, 0.28))
        if source == "upgrade":
            disc = float(np.clip(r.normal(0.02, 0.02), 0.0, 0.08))
        lst = (P.BUS_LIST_NEW if m >= P.PRICE_RISE else P.BUS_LIST_OLD)[currency]
        price = round(lst * (1 - disc), 2)
        aid = self.nid("B")
        nws = 1 if seats < 25 else int(r.choice([1, 2, 2, 3, 4], p=[0.25, 0.3, 0.2, 0.15, 0.1]))
        shares = r.dirichlet(np.ones(nws) * 3.0)
        acc = {"id": aid, "parent": parent["id"], "cur": currency, "start": m, "day": int(r.integers(1, 29)),
               "seats": seats, "price": price, "disc": disc, "u": u, "need": float(seats_need),
               "g": float(r.normal(P.NEED_GROWTH_MEAN, P.NEED_GROWTH_SD)), "rc": 0, "active": True,
               "repriced": m >= P.PRICE_RISE, "hist": [], "source": source, "ws": [], "end": None,
               "line": None}
        if team_ws is not None:
            team_ws["owner"] = aid
            if self.record:
                for row in self.log["ws_map"]:
                    if row["ws"] == team_ws["id"] and row["to"] is None:
                        row["to"] = m - 1
                self.log["ws_map"].append({"ws": team_ws["id"], "owner": aid, "from": m, "to": None})
            team_ws["share"] = float(shares[0])
            acc["ws"].append(team_ws)
            shares = shares[1:]
        for s in shares:
            acc["ws"].append(self.new_workspace(aid, m, float(s)))
        self.bus.append(acc)
        self.write_line(acc, m, "new", seats, price)
        if self.record and r.random() < (0.55 if seats >= 40 else 0.18) and source != "upgrade":
            self.log["lines"].append({"acc": aid, "type": "onboarding_fee", "m": m, "day": acc["day"],
                                      "seats": 0, "price": P.ONBOARDING_FEE[currency], "cur": currency,
                                      "months": 0})
        return acc

    def write_line(self, acc, m, typ, seats, price, months=12):
        if self.flows is not None:
            return
        if self.record:
            self.log["lines"].append({"acc": acc["id"], "type": typ, "m": m, "day": acc["day"], "seats": seats,
                                      "price": price, "cur": acc["cur"], "months": months})

    def active_users(self, acc, m):
        age = m - acc["start"]
        ramp = 1.0 - P.RAMP_DEPTH * math.exp(-age / P.RAMP_TAU)
        return acc["need"] * ramp

    # ------------------------------------------------------------------ team accounts
    def new_team(self, m, members, currency):
        tid = self.nid("T")
        acc = {"id": tid, "cur": currency, "start": m, "members": members, "active": True, "padded": None,
               "end": None, "ws": None, "upgraded": None, "billing_day": int(self.rng.integers(1, 29))}
        acc["ws"] = self.new_workspace(tid, m, 1.0)
        self.team.append(acc)
        return acc

    def team_seats(self, acc, m):
        if m >= P.TEAM_MIN:
            return max(acc["members"], P.TEAM_MIN_SEATS)
        return acc["members"]

    # ------------------------------------------------------------------ one month
    def step(self, m):
        r = self.rng
        fl = self.flows
        # parent groups start consolidating vendors
        counts = {}
        for a in self.bus:
            if a["active"]:
                counts[a["parent"]] = counts.get(a["parent"], 0) + 1
        for p in self.parents:
            if not p["consolidating"] and counts.get(p["id"], 0) >= 2 and r.random() < P.CONSOLIDATION_HAZARD:
                p["consolidating"] = True
                p["cons_month"] = m
        pmap = {p["id"]: p for p in self.parents}

        # Business accounts: needs drift, true-ups, renewals
        for a in self.bus:
            if not a["active"] or a["start"] == m:
                continue
            a["need"] *= math.exp(a["g"] / 12.0 + r.normal(0, 0.008))
            A = self.active_users(a, m)
            a["hist"].append((m, A))
            age = m - a["start"]
            if age % 12 == 0:
                a["rc"] += 1
                recent = [x for (mm, x) in a["hist"][-3:]]
                A3 = sum(recent) / len(recent)
                U = A3 / a["seats"]
                p_ch = P.CHURN_BASE + (P.CHURN_FIRST if a["rc"] == 1 else 0.0) + P.CHURN_UTIL * max(0.0, 0.70 - U)
                par = pmap[a["parent"]]
                if par["consolidating"]:
                    p_ch = max(p_ch, P.CONSOLIDATION_CHURN)
                old_arr = self.arr_bus(a)
                if r.random() < p_ch:
                    a["active"] = False
                    a["end"] = m
                    if fl is not None:
                        fl["churn"] += old_arr
                        fl["churn_n"] += 1
                    if self.record:
                        self.log["events"].append({"acc": a["id"], "type": "non_renewal", "m": m})
                    continue
                new_seats = a["seats"]
                if U < P.RIGHTSIZE_BELOW:
                    q = P.RIGHTSIZE_P_FIRST if a["rc"] == 1 else P.RIGHTSIZE_P_LATER
                    if r.random() < q:
                        new_seats = max(5, int(math.ceil(A3 / P.RIGHTSIZE_HEADROOM)))
                        new_seats = min(new_seats, a["seats"])
                new_price = a["price"]
                if m >= P.PRICE_RISE and not a["repriced"]:
                    up = P.UPLIFT_FULL - P.UPLIFT_SLOPE * math.log(max(a["seats"], 5) / 20.0) + r.normal(0, P.UPLIFT_SD)
                    up = float(np.clip(up, P.UPLIFT_FLOOR, P.UPLIFT_FULL))
                    new_price = round(a["price"] * (1 + up), 2)
                    a["repriced"] = True
                fx = P.PLAN_RATE_GBP if a["cur"] == "GBP" else 1.0
                if fl is not None:
                    fl["price"] += a["seats"] * (new_price - a["price"]) * 12 * fx
                    fl["contraction"] += (a["seats"] - new_seats) * new_price * 12 * fx
                    if m <= P.PRICE_RISE + 11 + 0 and not a.get("_counted"):
                        pass
                a["seats"], a["price"] = new_seats, new_price
                self.write_line(a, m, "renewal", new_seats, new_price)
                A = self.active_users(a, m)
            if A > a["seats"] * 1.0:
                add = int(math.ceil(A * 1.04 - a["seats"]))
                if add > 0:
                    months_left = 12 - (age % 12)
                    if fl is not None:
                        fx = P.PLAN_RATE_GBP if a["cur"] == "GBP" else 1.0
                        fl["expansion"] += add * a["price"] * 12 * fx
                        if a["id"] in self.cut_ids:
                            fl["expansion_book"] += add * a["price"] * 12 * fx
                    a["seats"] += add
                    self.write_line(a, m, "true_up", add, a["price"], months=months_left)

        # Team accounts
        for t in self.team:
            if not t["active"] or t["start"] == m:
                continue
            age = m - t["start"]
            if m == P.TEAM_MIN and t["members"] < P.TEAM_MIN_SEATS:
                t["padded"] = m
            h = P.TEAM_HAZARD + (P.TEAM_HAZARD_1 if t["members"] == 1 else 0) + \
                (P.TEAM_HAZARD_2 if t["members"] == 2 else 0)
            if age <= 3:
                h *= P.TEAM_YOUNG_MULT
            if t["padded"] is not None:
                k = m - t["padded"]
                h += P.PAD_SHOCK * math.exp(-k / P.PAD_DECAY) + P.PAD_PERSIST
            u = r.random()
            if u < h:
                t["active"] = False
                t["end"] = m
                if fl is not None:
                    fl["team_churn"] += self.team_seats(t, m - 1) * P.TEAM_PRICE[t["cur"]] * 12 * \
                        (P.PLAN_RATE_GBP if t["cur"] == "GBP" else 1.0)
                continue
            x = r.random()
            if x < 0.052:
                t["members"] += 1 if r.random() < 0.8 else 2
            elif x < 0.052 + 0.028 and t["members"] > 1:
                t["members"] -= 1
            if t["members"] >= P.UPGRADE_AT and r.random() < P.UPGRADE_P:
                t["active"] = False
                t["end"] = m
                t["upgraded"] = m
                par = self.new_parent(False)
                acc = self.new_business(m, t["members"] * float(r.uniform(0.95, 1.25)), t["cur"], par, "upgrade",
                                        team_ws=t["ws"])
                if fl is not None:
                    fl["new_upgrade"] += self.arr_bus(acc)
                continue
        # Team sign-ups
        lam = trend(P.TEAM_SIGNUPS[0] * 0.6, P.TEAM_SIGNUPS[1], m, -36, P.CUT)
        lam *= 1.0 + 0.10 * math.cos(2 * math.pi * (ym(m)[1] - 2) / 12.0)
        n = r.poisson(lam)
        for _ in range(n):
            mem = int(min(1 + r.geometric(0.42) - 1, 30))
            mem = max(1, mem)
            if m >= P.TEAM_MIN and mem < 3 and r.random() < P.SMALL_SIGNUP_DROP:
                continue
            cur = "GBP" if r.random() < 0.17 else "EUR"
            self.new_team(m, mem, cur)

        # pipeline
        self.pipeline_step(m)

        if self.record:
            self.log_month(m)

    def pipeline_step(self, m):
        r = self.rng
        fl = self.flows
        still = []
        for o in self.opps:
            s = o["stage"]
            stale = max(0, o["mis"] - P.TYPICAL[s])
            p_adv = P.ADV[s] * math.exp(-stale / P.STALE_DECAY)
            p_lost = P.LOST[s] + P.STALE_LOSS * stale
            if o["age"] >= P.CLEANUP_AGE:
                p_lost += P.CLEANUP_P
            u = r.random()
            o["age"] += 1
            if u < p_adv:
                if s == 3:
                    self.win(o, m)
                    continue
                o["stage"] += 1
                o["mis"] = 0
            elif u < p_adv + p_lost:
                o["closed"] = ("lost", m)
                if self.record:
                    self.log["opp_closed"].append(dict(o))
                continue
            else:
                o["mis"] += 1
            still.append(o)
        self.opps = still
        if m < P.PRICE_RISE:
            lam = trend(P.OPP_RATE[0] * 0.75, P.OPP_RATE[1], m, -36, P.PRICE_RISE - 1)
        else:
            lam = P.OPP_RATE[2]
        lam *= 1.0 + 0.12 * math.cos(2 * math.pi * (ym(m)[1] - 3) / 12.0)
        for _ in range(r.poisson(lam)):
            seats_need = float(np.clip(r.lognormal(math.log(P.SEAT_MEDIAN), P.SEAT_SIGMA), 8, 900))
            o = {"id": self.nid("O"), "created": m, "stage": 0, "mis": 0, "age": 0, "need": seats_need,
                 "cur": "GBP" if r.random() < 0.16 else "EUR", "closed": None, "orig": None,
                 "_new": fl is not None}
            o["quote_seats"] = int(math.ceil(seats_need / P.UTIL_MEAN))
            self.opps.append(o)

    def win(self, o, m):
        r = self.rng
        groups = [p for p in self.parents if p["group"]]
        if groups and r.random() < P.SUBSIDIARY_SHARE:
            par = groups[int(r.integers(0, len(groups)))]
        else:
            par = self.new_parent(r.random() < 0.10)
        acc = self.new_business(m, o["need"], o["cur"], par, "sales")
        o["closed"] = ("won", m, acc["id"])
        if self.record:
            self.log["opp_closed"].append(dict(o))
        if self.flows is not None:
            key = "new_new" if o.get("_new") else "new_open"
            self.flows[key] += self.arr_bus(acc)

    # ------------------------------------------------------------------ ARR
    def arr_bus(self, a):
        fx = P.PLAN_RATE_GBP if a["cur"] == "GBP" else 1.0
        return a["seats"] * a["price"] * 12 * fx

    def arr(self, m):
        b = sum(self.arr_bus(a) for a in self.bus if a["active"])
        t = sum(self.team_seats(x, m) * P.TEAM_PRICE[x["cur"]] * 12 * (P.PLAN_RATE_GBP if x["cur"] == "GBP" else 1.0)
                for x in self.team if x["active"])
        return b, t

    # ------------------------------------------------------------------ the month's records
    def log_month(self, m):
        r = self.rng
        if m < 0:
            return
        for t in self.team:
            if t["active"] and t["start"] <= m:
                seats = self.team_seats(t, m)
                self.log["team_inv"].append({"acc": t["id"], "m": m, "day": t["billing_day"], "members": t["members"],
                                             "seats": seats, "cur": t["cur"]})
        for a in self.bus:
            if a["active"] and a["start"] <= m:
                A = self.active_users(a, m) if a["start"] < m else a["need"] * (1 - P.RAMP_DEPTH)
                for w in a["ws"]:
                    val = A * w["share"] * math.exp(w["noise"] + r.normal(0, 0.06))
                    self.log["ws"].append({"ws": w["id"], "m": m, "active": max(0, int(round(val)))})
        for t in self.team:
            if t["active"] and t["start"] <= m:
                val = t["members"] * float(np.clip(r.normal(0.82, 0.18), 0.2, 1.0))
                self.log["ws"].append({"ws": t["ws"]["id"], "m": m, "active": max(0, int(round(val)))})
        for o in self.opps:
            self.log["snap"].append({"id": o["id"], "m": m, "created": o["created"], "stage": o["stage"],
                                     "mis": o["mis"], "seats": o["quote_seats"], "cur": o["cur"]})


def build_history():
    w = World(P.SEED)
    r = w.rng
    w.record = False
    # the book at the start of the warm-up (January 2019)
    for _ in range(int(P.BUS_INITIAL * 0.55)):
        par = w.new_parent(r.random() < 0.26)
        need = float(np.clip(r.lognormal(math.log(P.SEAT_MEDIAN), P.SEAT_SIGMA), 8, 700))
        a = w.new_business(-36 - int(r.integers(0, 12)), need, "GBP" if r.random() < 0.15 else "EUR", par, "sales")
        a["rc"] = int(r.integers(0, 3))
    for p in w.parents[:60]:
        if p["group"]:
            for _ in range(int(r.integers(2, 6))):
                need = float(np.clip(r.lognormal(math.log(P.SEAT_MEDIAN * 1.6), P.SEAT_SIGMA), 8, 900))
                w.new_business(-36 - int(r.integers(0, 12)), need, "EUR", p, "sales")
    for _ in range(int(P.TEAM_INITIAL * 0.45)):
        w.new_team(-36 - int(r.integers(0, 12)), max(1, int(r.geometric(0.42))), "GBP" if r.random() < 0.17 else "EUR")
    for m in range(-36, 0):
        w.step(m)
    w.record = True
    # the live book at January 2022 opens the export: one line per account in force, dated at its last anniversary
    for a in w.bus:
        if a["active"]:
            age = (0 - a["start"]) % 12
            w.log["lines"].append({"acc": a["id"], "type": "renewal" if a["start"] < -12 else "new",
                                   "m": -age if age else -12, "day": a["day"], "seats": a["seats"], "price": a["price"],
                                   "cur": a["cur"], "months": 12, "opening": True})
        for ws in a["ws"]:
            w.log["ws_map"].append({"ws": ws["id"], "owner": a["id"], "from": min(a["start"], 0), "to": None})
    for t in w.team:
        w.log["ws_map"].append({"ws": t["ws"]["id"], "owner": t["id"], "from": min(t["start"], 0), "to": None})
    for m in range(0, P.CUT + 1):
        w.step(m)
    return w


def forward(w, seed, months=None):
    """One forward replication from the cut; returns ARR by month and the flows."""
    v = copy.deepcopy(w)
    v.rng = np.random.default_rng(seed)
    v.record = False
    v.log = {"lines": [], "team_inv": [], "ws": [], "snap": [], "opp_closed": [], "ws_map": [], "events": []}
    for o in v.opps:
        o["_new"] = False
    v.flows = {"price": 0.0, "contraction": 0.0, "churn": 0.0, "churn_n": 0, "expansion": 0.0, "team_churn": 0.0,
               "new_open": 0.0, "new_new": 0.0, "new_upgrade": 0.0}
    team_ids = {t["id"] for t in v.team if t["active"]}
    v.cut_ids = {a["id"] for a in v.bus if a["active"]}
    v.flows["expansion_book"] = 0.0
    path = []
    for m in range(P.CUT + 1, (months or P.HORIZON) + 1):
        v.step(m)
        path.append(v.arr(m))
    v.flows["book_dec27"] = sum(v.arr_bus(a) for a in v.bus if a["active"] and a["id"] in v.cut_ids)
    team_left = sum(v.team_seats(t, P.HORIZON) * P.TEAM_PRICE[t["cur"]] * 12 *
                    (P.PLAN_RATE_GBP if t["cur"] == "GBP" else 1.0)
                    for t in v.team if t["active"] and t["id"] in team_ids)
    return path, v.flows, team_left
