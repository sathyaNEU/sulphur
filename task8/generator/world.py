"""The boards' records, laid over the core's arrays (core.simulate) and changing none of them.

Each centre-year of the core becomes candidate rows whose mean centre mark is the core's, each sample becomes
portfolio rows whose mean difference is the core's recorded difference (to the whole marks a form holds), each trial
script is one of the previous series' sampled portfolios marked before the meeting by the whole team, each person
registered with two boards marks both boards' scripts, and the regulator's 2023 review re-marks portfolios from every
Dunmoyle centre. The record-level detail (which candidate, which moderator, a marker's own lean) has its own random
stream; the core's stream is untouched."""
import numpy as np

import core as C

RSEED = 81342027
VSEED = 81342029                     # the posts left open and the extra appointments: a stream of their own
YEARS, NY = C.YEARS, C.NY
TRIAL_FROM, REG_FROM = 2015, 2020
ORG = "Carrow Awards"
REGULATOR = "Office of the Examinations Regulator"
PEOPLE = {"director": "Tamara McPherson", "analyst": "Arran Cullinane", "principal": "Christina Flahive",
          "data": "Kate Montague", "regulator": "Dominic McHale", "secretary": "Owen Hastings"}
# layout: which of three systems the board runs; code: its prefix; block: its range of national roll numbers
INFO = {
    "Carrow": dict(code="CAR", layout=1, block=61000, seat="Athlone"),
    "Ardkeel": dict(code="ARD", layout=1, block=20000, seat="Letterkenny"),
    "Brannock": dict(code="BRN", layout=2, block=31000, seat="Kilkenny"),
    "Dunmoyle": dict(code="DUN", layout=1, block=42000, seat="Dundalk"),
    "Eskerry": dict(code="ESK", layout=3, block=47000, seat="Tralee"),
    "Fennor": dict(code="FEN", layout=2, block=53000, seat="Waterford"),
    "Gortavale": dict(code="GOR", layout=3, block=76000, seat="Castlebar"),
}
BOARDS = list(C.BOARDS)
COUNTIES = {
    "Carrow": ["Westmeath", "Offaly", "Longford", "Roscommon", "Laois", "Kildare", "Dublin"],
    "Ardkeel": ["Donegal", "Sligo", "Leitrim"],
    "Brannock": ["Kilkenny", "Carlow", "Tipperary", "Wexford"],
    "Dunmoyle": ["Louth", "Meath", "Monaghan", "Cavan"],
    "Eskerry": ["Kerry", "Limerick", "Clare"],
    "Fennor": ["Waterford", "Cork", "Wicklow"],
    "Gortavale": ["Mayo", "Galway"],
}
PRE = ["Bally", "Kil", "Clon", "Dun", "Rath", "Knock", "Carrick", "Drum", "Glen", "Inish", "Lis", "Tulla", "Derry",
       "Agha", "Cool", "Gort", "Mona", "Tober", "Curra", "Cloon", "Bel", "Cappa", "Moy", "Ard", "Kin"]
ROOT = ["more", "beg", "duff", "roe", "glass", "een", "keel", "mullen", "nagh", "lea", "bane", "garve", "corra",
        "feale", "tierna", "brack", "gowan", "murry", "cashel", "derg", "finn", "loe", "sheen", "veagh", "namon",
        "avaddy", "croghan", "dangan", "fadda", "killen"]
KIND = ["Community College", "College of Further Education", "Technical College", "Training Centre",
        "Vocational School", "Institute of Further Education", "Community Training Workshop", "College"]
FORE = ["Aoife", "Brendan", "Ciara", "Declan", "Eimear", "Fergal", "Grainne", "Hugh", "Imelda", "John", "Karen",
        "Liam", "Maeve", "Niall", "Orla", "Padraig", "Roisin", "Sean", "Tara", "Una", "Vincent", "Yvonne", "Colm",
        "Deirdre", "Eoin", "Fiona", "Gerard", "Helen", "Kevin", "Laura", "Martin", "Noreen", "Oisin", "Patricia",
        "Ronan", "Sinead", "Tomas", "Aidan", "Bernadette", "Conor", "Dympna", "Enda", "Mairead", "Shane", "Clodagh",
        "Donal", "Emer", "Frank", "Geraldine", "Kieran"]
SUR = ["Brennan", "Byrne", "Callaghan", "Carroll", "Casey", "Clancy", "Coughlan", "Cullen", "Daly", "Doherty",
       "Dolan", "Donnelly", "Doyle", "Duffy", "Dunne", "Fahy", "Farrell", "Finnegan", "Fitzgerald", "Flanagan",
       "Flynn", "Foley", "Gallagher", "Geraghty", "Gilmartin", "Hanley", "Healy", "Hegarty", "Hickey", "Hogan",
       "Joyce", "Kavanagh", "Keane", "Kelleher", "Kenny", "Lally", "Leahy", "Lynch", "MacNamara", "Madden",
       "Maguire", "Mahon", "Molloy", "Moran", "Mulcahy", "Mullins", "Nolan", "O'Dea", "O'Dowd", "O'Gorman",
       "O'Hara", "O'Leary", "O'Mahony", "O'Rourke", "O'Shea", "Power", "Quigley", "Quinn", "Rafferty", "Reidy",
       "Riordan", "Rooney", "Scanlon", "Sheehan", "Sweeney", "Tierney", "Tobin", "Treacy", "Walsh", "Whelan"]
SD_PORT = float(np.sqrt(C.SIG_T ** 2 + C.SIG_M ** 2))   # a portfolio's cold difference about its centre's level


def fix_sum(vals, target, lo=None, hi=None, frozen=None):
    """Whole numbers nearest vals whose sum is target; frozen positions keep their rounded value."""
    v = np.rint(vals).astype(int)
    if lo is not None:
        v = np.clip(v, lo, hi)
    diff = int(target) - int(v.sum())
    if diff == 0:
        return v
    step = 1 if diff > 0 else -1
    resid = (vals - v) * step
    order = [i for i in np.argsort(-resid, kind="stable") if frozen is None or not frozen[i]]
    assert order, "nothing free to carry the sum"
    k = guard = 0
    while diff != 0:
        i = order[k % len(order)]
        if lo is None or lo <= v[i] + step <= hi:
            v[i] += step
            diff -= step
        k += 1
        guard += 1
        assert guard < 100000, "sum cannot be reached"
    return v


def half_up(x):
    return int(np.floor(abs(x) + 0.5) * np.sign(x))


def sample_total(g, ns, tol):
    """The whole-mark total of a sample's differences nearest ns*g that files the same outcome as the core."""
    want_adj = abs(g) > tol
    want_round = int(np.round(g))
    best = None
    for d in sorted(range(-3, 4), key=abs):
        s = int(np.rint(ns * g)) + d
        m = s / ns
        frac = abs(m) - np.floor(abs(m))
        if abs(frac - 0.5) < 1e-9 or abs(abs(m) - tol) < 1e-9:
            continue
        if (abs(m) > tol) != want_adj:
            continue
        if want_adj and half_up(m) != want_round:
            continue
        best = s
        break
    assert best is not None, (g, ns, tol)
    return best


def names(rng, n):
    idx = rng.choice(len(FORE) * len(SUR), n, replace=False)
    return [(FORE[i % len(FORE)], SUR[i // len(FORE)]) for i in idx]


def centres(rng, b, nc):
    info = INFO[b]
    nat = info["block"] + np.cumsum(rng.integers(1, 6, nc))
    own = rng.permutation(np.arange(1, nc + 1)) + 100
    nm = set()
    out = []
    while len(out) < nc:
        place = PRE[rng.integers(len(PRE))] + ROOT[rng.integers(len(ROOT))]
        name = "%s %s" % (place, KIND[rng.integers(len(KIND))])
        if name in nm:
            continue
        nm.add(name)
        out.append(name)
    cty = [COUNTIES[b][i] for i in rng.integers(0, len(COUNTIES[b]), nc)]
    appr = rng.integers(1978, 2010, nc)
    return dict(nat=nat.astype(int), own=own.astype(int), name=out, county=cty, approved=appr.astype(int))


def teams(rng, world):
    """Who moderates for each board each year. Before the national register (2020) a board keeps its own codes; from
    2020 every moderator has one registration number, and the people of each link sit on both boards' teams. A board
    has its standing posts; a post whose holder leaves is sometimes filled a year late, and a board appoints a few
    more moderators for a spell of series when it needs them, so a team is not the same size from year to year."""
    people, team, started = [], {b: {} for b in BOARDS}, []

    def new(first, last):
        people.append(dict(first=first, last=last, lean=float(rng.normal(0, 0.8)), boards={}))
        return len(people) - 1
    # before the register: nm slots a board, about one in twelve replaced each year
    for b in BOARDS:
        nm = C.BOARDS[b]["nm"]
        slots = [new(*n) for n in names(rng, nm)]
        for y in range(YEARS[0], REG_FROM):
            if y > YEARS[0]:
                for i in range(nm):
                    if rng.random() < 0.085:
                        slots[i] = new(*names(rng, 1)[0])
                        started.append((b, y, slots[i]))
            for pid in slots:
                people[pid]["boards"].setdefault(b, []).append(y)
            team[b][y] = [(pid, None) for pid in slots]
    # from the register on: single-board moderators, and the people of each link on both teams
    link_of = {b: 0 for b in BOARDS}
    for a, b2, m in C.DUAL:
        link_of[a] += m
        link_of[b2] += m
    singles = {b: [new(*n) for n in names(rng, C.BOARDS[b]["nm"] - link_of[b])] for b in BOARDS}
    pools = [[new(*n) for n in names(rng, m)] for _, _, m in C.DUAL]
    for yi, y in enumerate(range(REG_FROM, YEARS[-1] + 1)):
        for b in BOARDS:
            if yi:
                for i in range(len(singles[b])):
                    if rng.random() < 0.08:
                        singles[b][i] = new(*names(rng, 1)[0])
                        started.append((b, y, singles[b][i]))
            team[b][y] = [(pid, None) for pid in singles[b]]
            for pid in singles[b]:
                people[pid]["boards"].setdefault(b, []).append(y)
        for li, (a, b2, m) in enumerate(C.DUAL):
            if yi:
                for i in range(m):
                    if rng.random() < 0.10:
                        pools[li][i] = new(*names(rng, 1)[0])
            link = world["D"][li]
            for i, pid in enumerate(pools[li]):
                k = yi * m + i
                team[a][y].append((pid, float(link["ra"][k])))
                team[b2][y].append((pid, float(link["rb"][k])))
                people[pid]["boards"].setdefault(a, []).append(y)
                people[pid]["boards"].setdefault(b2, []).append(y)
    posts = {b: {y: list(v) for y, v in team[b].items()} for b in BOARDS}      # the standing posts as drawn
    regs = rng.permutation(np.arange(10231, 10231 + 4 * len(people)))
    rv = np.random.default_rng(VSEED)
    # a post filled a year late: the new holder's first series is the one after the leaver's last
    for b, y, pid in started:
        u, ys = rv.random(), people[pid]["boards"][b]
        if u < 0.45 and len(ys) >= 2 and ys[0] == y:
            ys.remove(y)
            team[b][y] = [m for m in team[b][y] if m[0] != pid]
    # appointments beyond the standing posts, each for a spell of series inside one numbering
    for b in BOARDS:
        for first, last in ((YEARS[0], REG_FROM - 1), (REG_FROM, YEARS[-1])):
            for _ in range(int(rv.poisson(C.BOARDS[b]["nm"] / 7.0))):
                y0 = int(rv.integers(first, last + 1))
                y1 = min(last, y0 + int(rv.geometric(0.45)) - 1)
                fn, ln = names(rv, 1)[0]
                people.append(dict(first=fn, last=ln, lean=float(rv.normal(0, 0.8)), boards={b: list(range(y0, y1 + 1))}))
                for y in range(y0, y1 + 1):
                    team[b][y].append((len(people) - 1, None))
    # codes: a board's own before 2020 in order of appointment, the national registration number from 2020
    for p in people:
        p["code"] = {}
    for b in BOARDS:
        old = sorted((min(p["boards"][b]), pid) for pid, p in enumerate(people)
                     if b in p["boards"] and min(p["boards"][b]) < REG_FROM)
        for k, (_, pid) in enumerate(old):
            people[pid]["code"][b] = "%s-M%03d" % (INFO[b]["code"], k + 11)
    for pid, p in enumerate(people):
        p["reg"] = "MR%05d" % regs[pid] if any(max(ys) >= REG_FROM for ys in p["boards"].values()) else None
    return people, team, posts


def build(seed=C.SEED):
    world = C.simulate(seed)
    rng = np.random.default_rng(RSEED)
    people, team, posts = teams(rng, world)
    rv = np.random.default_rng(VSEED + 1)
    out = dict(core=world, people=people, team=team, boards={})
    for b in BOARDS:
        w = world["B"][b]
        P = w["P"]
        nc = P["nc"]
        cen = centres(rng, b, nc)
        sd_c = 11.0 * np.exp(rng.normal(0, 0.12, nc))
        scripts_at = {}
        for i in range(len(w["ex_x"])):
            scripts_at.setdefault((int(w["ex_c"][i]), int(w["ex_t"][i])), []).append(i)
        cand, samp, outc, src = [], [], [], {}
        for ti, y in enumerate(YEARS):
            std = [pid for pid, _ in posts[b][y]]
            serving = [pid for pid, _ in team[b][y]]
            order = rng.permutation(len(std))
            mods = [std[i] for i in order if std[i] in set(serving)]
            for pid in [q for q in serving if q not in set(std)]:
                mods.insert(int(rv.integers(0, len(mods) + 1)), pid)
            sampled = np.flatnonzero(w["samp"][:, ti])
            mod_of = {int(c): mods[j % len(mods)] for j, c in enumerate(rng.permutation(sampled))}
            for c in range(nc):
                n = int(w["ncand"][c, ti])
                adj = int(w["adj"][c, ti])
                z = rng.normal(0, 1, n)
                lo, hi = max(16, adj), min(93, 100 + adj)
                marks = fix_sum(w["mbar"][c, ti] + sd_c[c] * (z - z.mean()), int(np.rint(n * w["mbar"][c, ti])), lo, hi)
                extra = int(rng.poisson(0.02 * n))
                status = np.array([0] * n + list(rng.integers(1, 3, extra)))
                seqno = rng.permutation(n + extra) + 1
                cand.append((ti, c, seqno, status, np.concatenate([marks, np.full(extra, -1)]), adj))
                if not w["samp"][c, ti]:
                    continue
                ns = int(w["ns"][c, ti])
                rank = np.argsort(marks, kind="stable")
                pick = rank[np.minimum(n - 1, np.floor((np.arange(ns) + rng.random()) * n / ns).astype(int))]
                pick = np.unique(pick)
                while len(pick) < ns:
                    pick = np.unique(np.concatenate([pick, rng.integers(0, n, ns - len(pick))]))
                pick = rng.permutation(pick)
                g = float(w["G"][c, ti])
                total = sample_total(g, ns, P["tol"])
                zz = rng.normal(0, 1, ns)
                raw = g + (1 - P["w"]) * SD_PORT * (zz - zz.mean())
                frozen = np.zeros(ns, bool)
                here = scripts_at.get((c, ti), [])
                assert len(here) <= ns - 3, (b, c, y, len(here), ns)
                for j, i in enumerate(here):
                    # the copied portfolio: a sampled one whose mark leaves the team's marks room on the scale
                    room = marks[pick[j:]] - w["ex_x"][i]
                    okk = np.flatnonzero((room >= 14) & (room <= 88))
                    q = j + (int(okk[0]) if len(okk) else int(np.argmin(np.abs(room - 52))))
                    pick[[j, q]] = pick[[q, j]]
                    raw[j] = float(np.rint(w["ex_y"][i]))
                    frozen[j] = True
                    src[i] = (ti, c, int(seqno[pick[j]]), int(marks[pick[j]]))
                d = fix_sum(raw, total, frozen=frozen)
                mid = mod_of[c]
                samp.append((ti, c, seqno[pick], marks[pick], marks[pick] - d, mid))
                outc.append((ti, c, mid, ns, total / ns, adj))
        # the standardisation trials: scripts, the team's marks before the meeting, the agreed marks
        trial = {}
        for y in range(TRIAL_FROM, YEARS[-1] + 1):
            ids = [i for i in range(len(w["ex_x"])) if int(w["ex_year"][i]) == y]
            std, nsr = posts[b][y], len(ids)
            serving = set(pid for pid, _ in team[b][y])
            keep = np.array([pid in serving for pid, _ in std])
            more = [m for m in team[b][y] if m[0] not in set(pid for pid, _ in std)]
            members = [m for m, k in zip(std, keep) if k] + more
            nm = len(members)
            blank0 = rng.random((len(std), nsr)) < 0.03                 # drawn over the standing posts, as proved
            blank = np.vstack([blank0[keep], rv.random((len(more), nsr)) < 0.03])
            cnt0, cnt = (~blank0).sum(0), (~blank).sum(0)
            cmark = np.array([src[i][3] for i in ids])
            tot = np.rint((cmark - w["ex_x"][ids]) * cnt).astype(int)
            cons = tot / cnt
            agreed = np.rint(np.rint((cmark - w["ex_x"][ids]) * cnt0) / cnt0 - w["ex_gap"][ids]).astype(int)
            M = np.full((nm, nsr), -1)
            dual = [j for j, (_, r) in enumerate(members) if r is not None]
            row = {int(i): j for j, i in enumerate(np.flatnonzero(keep))}  # a standing post's row among the members
            single0 = [i for i, (_, r) in enumerate(std) if r is None]
            added = list(range(int(keep.sum()), nm))
            for j in dual:
                idx = np.flatnonzero(~blank[j])
                r = members[j][1]
                raw = cons[idx] + r + rng.normal(0, C.SIG_M, len(idx))
                M[j, idx] = fix_sum(raw, int(np.rint(cons[idx].sum() + len(idx) * r)), 0, 100)
            for s in range(nsr):
                js0 = [i for i in single0 if not blank0[i, s]]
                e0 = rng.normal(0, C.SIG_M, len(js0))
                js = [row[i] for i in js0 if keep[i]]
                e = [e0[k] for k, i in enumerate(js0) if keep[i]]
                xj = [j for j in added if not blank[j, s]]
                js, e = js + xj, np.array(e + list(rv.normal(0, C.SIG_M, len(xj))))
                rest = int(tot[s] - sum(M[j, s] for j in dual if not blank[j, s]))
                ln = np.array([people[members[j][0]]["lean"] for j in js])
                raw = rest / len(js) + (ln - ln.mean()) + (e - e.mean())
                M[js, s] = fix_sum(raw, rest, 0, 100)
            assert cons.min() > 6 and cons.max() < 96, (b, y, cons.min(), cons.max())
            trial[y] = dict(ids=ids, src=[src[i] for i in ids], agreed=agreed, marks=M,
                            members=[pid for pid, _ in members])
        out["boards"][b] = dict(cen=cen, cand=cand, samp=samp, outc=outc, trial=trial)
    # the regulator's 2023 review: portfolios from every centre of the referee board, marked at Carrow's standard
    rb, ry = C.REFEREE
    ti = YEARS.index(ry)
    rev = []
    for (t, c, seqno, status, marks, adj) in out["boards"][rb]["cand"]:
        if t != ti:
            continue
        ok = np.flatnonzero(status == 0)
        k = min(C.REVIEW_N, len(ok))
        pick = rng.choice(ok, k, replace=False)
        r = float(world["review"][c])
        z = rng.normal(0, 1, k)
        d = fix_sum(r + SD_PORT * (z - z.mean()), int(np.rint(r * k)))
        rev.append((c, seqno[pick], marks[pick], marks[pick] - d))
    out["review"] = rev
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    WD = build()
    print("built in %.1fs; people %d" % (time.time() - t0, len(WD["people"])))
    for b in BOARDS:
        B = WD["boards"][b]
        print(b, "candidate rows", sum(len(x[2]) for x in B["cand"]), "samples", len(B["samp"]),
              "trial marks", sum(int((t["marks"] >= 0).sum()) for t in B["trial"].values()))
