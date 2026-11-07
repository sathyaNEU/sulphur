"""Corvane's marketplace, month by month, from launch (January 2022) to the cut (31 October 2026).

The process the pack is cut from. Members join, are matched to a dedicated tutor who teaches their language, pay a
monthly charge and cancel on their own curve; a member whose tutor stops teaching cancels far more often in that month
and the next. Tutors stop teaching at a rate set by how many months they have been teaching. New members go to the
most established tutor with room; in ordinary months about one in ten goes to a starter roster with a new tutor; the
platform paused onboarding from March to August 2026 and the AUT26 surge in September and October 2026 overflowed onto
the tutors who started then. Members whose tutor stops are offered an established tutor.

Month index t: 0 is January 2022, 57 is October 2026 (the cut), 68 is September 2027.
"""
import copy
import numpy as np

CUT = 57
HORIZON = 68
LAUNCH_TUTORS = 90

LANGS = ['EN', 'ES', 'DE', 'FR', 'IT']
LANG_P = [.50, .18, .14, .10, .08]
CAMP_LANG_P = {'EN': .65, 'ES': .35}
COUNTRIES = ['DE', 'FR', 'ES', 'IT', 'NL', 'AT', 'CH', 'GB']
COUNTRY_P = [.34, .14, .13, .10, .08, .06, .05, .10]
CURRENCY = {'GB': 'GBP', 'CH': 'CHF'}

P = dict(
    mbase={1: .13, 2: .085, 3: .065, 4: .055, 5: .05, 6: .045}, m712=.038, m1324=.030, m25=.025,
    eng_mult=(1.6, 1.0, 0.7), eng_p=(.25, .55, .20),
    season={},
    dep1=.60, dep2=.22, post_mult=1.0, post_len=0,
    tdep={1: .02, 2: .03, 3: .08, 4: .21, 5: .27, 6: .24, 7: .17, 8: .11, 9: .07},
    t1012=.03, t1324=.010, t25=.007,
    pend_quit=.08, cap_lo=18, cap_hi=30, grow_lo=12, grow_hi=22,
    starter_share=.10, starter_max=8, slack=.30,
    lean=(50, 55),
    acq_season={1: 1.45, 2: 1.15, 3: 1.05, 4: .95, 5: .90, 6: .75, 7: .65, 8: .80, 9: 1.35, 10: 1.20, 11: 1.00, 12: .75},
    acq_start=150.0, acq_growth=.034, acq_growth_late=.008, acq_kink=30,
    p_twice=.35,
)
CAMPS = {38: ('SPR25', 150), 39: ('SPR25', 130), 56: ('AUT26', 1800), 57: ('AUT26', 1900)}


def mhaz(k):
    if k in P['mbase']:
        return P['mbase'][k]
    if k <= 12:
        return P['m712']
    if k <= 24:
        return P['m1324']
    return P['m25']


def thaz(j):
    if j in P['tdep']:
        return P['tdep'][j]
    if j <= 12:
        return P['t1012']
    if j <= 24:
        return P['t1324']
    return P['t25']


def acq_base(t):
    """Expected organic paid signups in month t (before seasonality)."""
    if t <= P['acq_kink']:
        return P['acq_start'] * (1 + P['acq_growth']) ** t
    return P['acq_start'] * (1 + P['acq_growth']) ** P['acq_kink'] * (1 + P['acq_growth_late']) ** (t - P['acq_kink'])


class World:
    def __init__(self, seed=601):
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.T = dict(hired=[], start=[], off=[], load=[], cap=[], lang=[], grow=[])
        self.M = dict(sign=[], plan=[], eng=[], camp=[], lang=[], country=[], tutor=[], cancel=[], paid=[],
                      dflag=[], post=[], hist=[], dom=[])
        self.mm = []   # member-month truth rows: (m, t, k, tutor, tenure, state, cancelled)
        self.tm = []   # tutor-month truth rows: (tutor, t, teaching month, stopped)
        for _ in range(LAUNCH_TUTORS):
            self._hire(-1, lang=self.rng.choice(LANGS, p=LANG_P))

    # ------------------------------------------------------------------ tutors
    def _hire(self, t, lang):
        T = self.T
        T['hired'].append(t); T['start'].append(None); T['off'].append(None); T['load'].append(0)
        T['cap'].append(int(self.rng.integers(P['cap_lo'], P['cap_hi'] + 1))); T['lang'].append(lang)
        T['grow'].append(int(self.rng.integers(P['grow_lo'], P['grow_hi'] + 1)))

    def _ten(self, i):
        s = self.T['start'][i]
        return None if s is None else self.t - s

    def _active(self, lang=None):
        T = self.T
        return [i for i in range(len(T['hired'])) if T['off'][i] is None and (lang is None or T['lang'][i] == lang)]

    def _cap(self, i):
        T = self.T
        ten = self._ten(i)
        return T['cap'][i] + (T['grow'][i] if (ten is not None and ten >= 9) else 0)

    def _assign(self, i):
        T = self.T
        T['load'][i] += 1
        if T['start'][i] is None:
            T['start'][i] = self.t

    def _match(self, lang, normal):
        T = self.T
        opn = [i for i in self._active(lang) if T['load'][i] < self._cap(i)]
        est = [i for i in opn if self._ten(i) is not None and self._ten(i) >= 9]
        mid = [i for i in opn if self._ten(i) is not None and 4 <= self._ten(i) <= 8]
        new = [i for i in opn if self._ten(i) is None or self._ten(i) <= 3]
        if normal and new and self.rng.random() < P['starter_share']:
            c = [i for i in new if T['load'][i] < P['starter_max']]
            if c:
                i = min(c, key=lambda q: (T['load'][q], -T['hired'][q]))
                self._assign(i)
                return i
        for pool in (est, mid):
            if pool:
                i = min(pool, key=lambda q: (T['start'][q], q))
                self._assign(i)
                return i
        if new:
            i = min(new, key=lambda q: (0 if T['start'][q] is not None else 1, T['hired'][q], q))
            self._assign(i)
            return i
        # nobody has room: hire on the spot (a recruiter's emergency onboarding)
        self._hire(self.t, lang)
        i = len(T['hired']) - 1
        self._assign(i)
        return i

    def _rematch(self, lang):
        T = self.T
        est = [i for i in self._active(lang) if self._ten(i) is not None and self._ten(i) >= 9]
        if est:
            i = min(est, key=lambda q: (T['load'][q] - self._cap(q), T['start'][q], q))
            self._assign(i)
            return i
        return self._match(lang, False)

    # ------------------------------------------------------------------ one month
    def step(self, record=True, camps=CAMPS):
        t = self.t; rng = self.rng; M = self.M; T = self.T
        cm = (t % 12) + 1
        camp = camps.get(t)
        n_camp = camp[1] if camp else 0
        n_org = int(rng.poisson(acq_base(t) * P['acq_season'][cm]))
        normal = camp is None
        # tutors stop (teaching tutors) or quit while pending
        stopped = set()
        for i in self._active():
            if T['start'][i] is None:
                if t > T['hired'][i] >= 0 and rng.random() < P['pend_quit']:
                    T['off'][i] = t
                continue
            j = t - T['start'][i]
            if j >= 1:
                s = rng.random() < thaz(j)
                if record:
                    self.tm.append((i, t, j, int(s)))
                if s:
                    T['off'][i] = t; stopped.add(i)
        n_m = len(M['sign'])
        for x in range(n_m):
            if M['cancel'][x] is None and M['tutor'][x] in stopped:
                M['dflag'][x] = 1; M['tutor'][x] = None
        for i in stopped:
            T['load'][i] = 0
        # recruitment per language, outside the onboarding pause
        lean = P['lean'][0] <= t <= P['lean'][1]
        if not lean:
            act_by = {}
            for x in range(n_m):
                if M['cancel'][x] is None:
                    act_by[M['lang'][x]] = act_by.get(M['lang'][x], 0) + 1
            for lang, p_ in zip(LANGS, LANG_P):
                exp_new = acq_base(t) * P['acq_season'][cm] * p_ + n_camp * CAMP_LANG_P.get(lang, 0)
                open_ = sum(max(0, self._cap(i) - T['load'][i]) for i in self._active(lang))
                need = int(P['slack'] * act_by.get(lang, 0) + 1.1 * exp_new) + 6
                if open_ < need:
                    for _ in range(int(np.ceil((need - open_) / 24))):
                        self._hire(t, lang)
        # new members
        flags = np.array([1] * n_camp + [0] * n_org); rng.shuffle(flags)
        for f in flags:
            if f:
                lang = rng.choice(list(CAMP_LANG_P), p=list(CAMP_LANG_P.values()))
                country = rng.choice(['DE', 'FR', 'ES', 'IT', 'NL', 'AT', 'GB'], p=[.36, .15, .12, .12, .09, .06, .10])
                if lang == 'ES' and country == 'ES':
                    country = 'DE'
            else:
                lang = rng.choice(LANGS, p=LANG_P)
                country = rng.choice(COUNTRIES, p=COUNTRY_P)
            M['sign'].append(t); M['plan'].append(int(rng.random() < P['p_twice']))
            M['eng'].append(int(rng.choice(3, p=P['eng_p']))); M['camp'].append(camp[0] if (f and camp) else '')
            M['lang'].append(lang); M['country'].append(country)
            tu = self._match(lang, normal)
            M['tutor'].append(tu); M['cancel'].append(None); M['paid'].append(0)
            M['dflag'].append(0); M['post'].append(0); M['hist'].append([(t, tu)])
            M['dom'].append(int(rng.integers(1, 29)))
        # billing and cancellation decisions
        for x in range(len(M['sign'])):
            if M['cancel'][x] is not None or M['sign'][x] > t:
                continue
            M['paid'][x] += 1
            k = M['paid'][x]
            h = mhaz(k) * P['eng_mult'][M['eng'][x]] * P['season'].get(cm, 1.0)
            tu = M['tutor'][x]
            ten = (t - T['start'][tu]) if (tu is not None and T['start'][tu] is not None) else -1
            st = 0
            if M['post'][x] > 0:
                h *= P['post_mult']; st = 3
            h = min(h, .95)
            if M['dflag'][x] == 1:
                h = 1 - (1 - h) * (1 - P['dep1']); st = 1
            elif M['dflag'][x] == 2:
                h = 1 - (1 - h) * (1 - P['dep2']); st = 2
            c = rng.random() < h
            if record:
                self.mm.append((x, t, k, tu if tu is not None else -1, ten, st, int(c)))
            if c:
                M['cancel'][x] = t
                if tu is not None:
                    T['load'][tu] -= 1; M['tutor'][x] = None
            else:
                if st == 3:
                    M['post'][x] -= 1
                if M['dflag'][x] == 1:
                    nt = self._rematch(M['lang'][x])
                    M['tutor'][x] = nt; M['dflag'][x] = 2; M['hist'][x].append((t + 1, nt))
                elif M['dflag'][x] == 2:
                    M['dflag'][x] = 0; M['post'][x] = P['post_len']
        self.t += 1


def build_world(seed=601):
    W = World(seed)
    while W.t <= CUT:
        W.step(record=True)
    return W


def continue_world(W, seed, until=HORIZON):
    V = copy.deepcopy(W)
    V.rng = np.random.default_rng(seed)
    V.mm = []; V.tm = []
    while V.t <= until:
        V.step(record=True, camps={})
    return V
