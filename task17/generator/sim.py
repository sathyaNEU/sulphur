"""The process behind the files, simulated from November 2023 to the export cut in November 2026.

Projects apply each December for node-hour grants and draw on them as their researchers submit: in sessions (sweeps
of near-identical jobs, chains, resubmissions after a crash or a time-out) with hour-of-day, weekday and term
structure, a ramp in a project's first months, deadline peaks, and a stop when the project's own appetite for its
grant is spent. Run times follow a heavy-tailed (log-logistic) law per job template, cut at the quality of service's
limit in force. Nodes fail from software causes on a hazard that rises with uptime, from hardware causes with a
parts lead time, and together by rack when a switch or a power feed fails; a job on a failed node is requeued and
restarts from its last checkpoint. Planned maintenance drains the partition monthly. The scheduler (des.c) starts
jobs first come first served by eligible time with conservative backfill over whole nodes. Every file in the pack is
a view of this one record; nothing is added where a result is decided."""
import calendar
import datetime as dt
import math

import numpy as np
import pandas as pd
from faker import Faker

import des
import params as P

HOUR = dt.timedelta(hours=1)


# ---------------------------------------------------------------- clock helpers
def hrs(d):
    """hours since T0 of an aware datetime"""
    return (d - P.T0).total_seconds() / 3600.0


def at(h):
    return P.T0 + dt.timedelta(hours=float(h))


def local(h):
    return at(h).astimezone(P.TZ)


def hour_of_week_local(hs):
    """for an array of hours since T0: local hour of week (0 = Monday 00:00) and the local date ordinal"""
    out_h = np.empty(len(hs), dtype=np.int32)
    out_d = np.empty(len(hs), dtype=np.int64)
    # vectorised through a lookup of each hour's local offset (DST changes at most twice a year)
    base = np.floor(hs).astype(np.int64)
    uniq, inv = np.unique(base, return_inverse=True)
    lh = np.empty(len(uniq), dtype=np.int32)
    ld = np.empty(len(uniq), dtype=np.int64)
    for i, b in enumerate(uniq):
        l = local(float(b))
        lh[i] = l.weekday() * 24 + l.hour
        ld[i] = l.toordinal()
    out_h[:] = lh[inv]
    out_d[:] = ld[inv]
    return out_h, out_d


# ---------------------------------------------------------------- distributions
def loglogistic(rng, m, beta, size=None):
    u = rng.uniform(size=size)
    return m * (u / (1.0 - u)) ** (1.0 / beta)


def lognormal_median(rng, median, sigma, size=None):
    return median * np.exp(rng.normal(0.0, sigma, size=size))


# ---------------------------------------------------------------- the people and the projects
UNIVERSITIES = [("Universität Ravensfeld", "URF", 0.40), ("Technische Universität Ravensfeld", "TURF", 0.33),
                ("Universität Hohenmark", "UHM", 0.17), ("Hochschule Wessenbrück", "HSW", 0.10)]
INSTITUTES = {
    "FOR": ["Institut für Informatik", "Institut für Theoretische Physik", "Institut für Strömungsmechanik",
            "Institut für Biochemie", "Lehrstuhl für Maschinelles Lernen", "Institut für Materialwissenschaft",
            "Institut für Medizinische Informatik", "Lehrstuhl für Computerlinguistik", "Institut für Geophysik",
            "Institut für Robotik und Kognitive Systeme", "Lehrstuhl für Bioinformatik", "Institut für Astrophysik",
            "Institut für Chemie", "Lehrstuhl für Verbrennungstechnik", "Institut für Photogrammetrie"],
    "NWG": ["Nachwuchsgruppe Lernende Systeme", "Emmy-Noether-Gruppe Molekulare Simulation",
            "Nachwuchsgruppe Klimamodellierung", "Nachwuchsgruppe Medizinische Bildgebung",
            "Juniorprofessur Quantenchemie", "Nachwuchsgruppe Sprachtechnologie", "Nachwuchsgruppe Turbulenz",
            "Juniorprofessur Datenwissenschaft"],
    "LEH": ["Fakultät für Informatik, Lehre", "Studiengang Data Science", "Fakultät für Maschinenbau, Lehre",
            "Studiengang Computational Engineering", "Zentrum für Digitale Lehre", "Fakultät für Physik, Praktikum"],
    "KOP": ["Transferzentrum Industrielle KI", "Kooperationsprojekt Medizintechnik", "Industrie-Kooperation Mobilität",
            "Kooperationsprojekt Energiesysteme", "Transferzentrum Materialforschung"],
}
TITLE_WORDS = {
    "FOR": [("Transformer-Modelle", "für die Proteinstrukturvorhersage"), ("Turbulente Strömungen", "in Brennkammern"),
            ("Dichtefunktionaltheorie", "für Batteriematerialien"), ("Graph-Neuronale Netze", "für Molekülentwurf"),
            ("Segmentierung", "medizinischer Bilddaten"), ("Mehrskalensimulation", "poröser Medien"),
            ("Sprachmodelle", "für juristische Texte"), ("Kosmologische Simulationen", "der Strukturbildung"),
            ("Reinforcement Learning", "für Robotergreifen"), ("Molekulardynamik", "von Membranproteinen"),
            ("Diffusionsmodelle", "für Materialmikrostrukturen"), ("Wettervorhersage", "mit neuronalen Netzen"),
            ("Spektrale Methoden", "für Plasmaphysik"), ("Genomweite Assoziation", "seltener Varianten"),
            ("Partikelsimulation", "granularer Medien"), ("Bildrekonstruktion", "in der Tomographie"),
            ("Verkehrsflussmodelle", "für Stadtregionen"), ("Selbstüberwachtes Lernen", "auf Satellitenbildern"),
            ("Quantenchemie", "von Übergangsmetallkomplexen"), ("Neuronale Operatoren", "für Wellengleichungen")],
    "NWG": [("Lernende Systeme", "unter Verteilungsverschiebung"), ("Klimamodelle", "mit maschinellem Lernen"),
            ("Molekulare Simulation", "von Enzymkatalyse"), ("Sprachtechnologie", "für Dialekte"),
            ("Turbulenzmodellierung", "mit Deep Learning"), ("Quantenchemische Methoden", "für Katalysatoren"),
            ("Medizinische Bildgebung", "mit generativen Modellen"), ("Datenwissenschaft", "für Epidemiologie")],
    "LEH": [("Praktikum", "Maschinelles Lernen"), ("Vorlesung", "Deep Learning"), ("Übung", "Numerische Strömungsmechanik"),
            ("Projektseminar", "Data Science"), ("Praktikum", "Computational Physics"), ("Kurs", "Sprachverarbeitung"),
            ("Seminar", "Rechnergestützte Chemie"), ("Übung", "Parallele Programmierung")],
    "KOP": [("Fehlererkennung", "in Fertigungsdaten"), ("Bildgestützte Diagnostik", "im Klinikbetrieb"),
            ("Batteriealterung", "aus Flottendaten"), ("Netzlastprognose", "für Verteilnetze"),
            ("Werkstoffmodelle", "für Leichtbau"), ("Sensorfusion", "für automatisiertes Fahren")],
}
TEMPLATES = {
    # name: (categories' weights, node dist, median range h, shape range, qos, habit weights (max, round, tight),
    #        mean session size, kind, within-session sigma range, crash p, chain?, stems)
    "train": ({"FOR": 0.36, "NWG": 0.40, "LEH": 0.30, "KOP": 0.36}, {1: 0.55, 2: 0.25, 4: 0.14, 8: 0.06}, (9.5, 13.5),
              (1.55, 1.75), "normal", (0.40, 0.45, 0.15), (2.9, "sweep"), (0.02, 0.05), 0.030, False,
              ["train_resnet", "train_vit", "train_gpt2", "train_unet", "train_gnn", "run_lr", "train_dit", "pretrain"]),
    "finetune": ({"FOR": 0.14, "NWG": 0.16, "LEH": 0.30, "KOP": 0.18}, {1: 0.72, 2: 0.20, 4: 0.08}, (2.9, 4.4),
                 (1.55, 1.75), "normal", (0.35, 0.50, 0.15), (2.9, "sweep"), (0.02, 0.05), 0.030, False,
                 ["ft_bert", "ft_llama", "finetune", "lora_run", "ft_clip", "sft"]),
    "eval": ({"FOR": 0.12, "NWG": 0.12, "LEH": 0.09, "KOP": 0.12}, {1: 0.90, 2: 0.10}, (0.15, 1.1), (2.6, 4.0), "short",
             (0.80, 0.15, 0.05), (4.2, "sweep"), (0.03, 0.07), 0.020, False,
             ["eval_ckpt", "eval", "infer", "predict", "score_run", "bench_eval"]),
    "md": ({"FOR": 0.17, "NWG": 0.14, "LEH": 0.04, "KOP": 0.05}, {1: 0.60, 2: 0.30, 4: 0.10}, (14.5, 21.0), (1.55, 1.75),
           "normal", (0.50, 0.42, 0.08), (2.8, "chain"), (0.02, 0.05), 0.015, True,
           ["md_prod", "md_equil", "gromacs_run", "namd_prod", "md_chunk", "lammps_run"]),
    "cfd": ({"FOR": 0.11, "NWG": 0.10, "LEH": 0.04, "KOP": 0.12}, {2: 0.35, 4: 0.45, 8: 0.20}, (10.5, 15.5), (1.55, 1.75),
            "normal", (0.45, 0.45, 0.10), (2.0, "chain"), (0.02, 0.05), 0.020, True,
            ["cfd_mesh", "les_run", "openfoam", "dns_box", "channel_re", "cfd_case"]),
    "preproc": ({"FOR": 0.06, "NWG": 0.05, "LEH": 0.05, "KOP": 0.07}, {1: 1.0}, (0.08, 0.7), (2.8, 4.5), "short",
                (0.75, 0.20, 0.05), (4.2, "sweep"), (0.03, 0.07), 0.025, False,
                ["prep_shard", "tokenize", "preprocess", "extract_feat", "convert", "resample"]),
    "interactive": ({"FOR": 0.06, "NWG": 0.05, "LEH": 0.06, "KOP": 0.06}, {1: 0.95, 2: 0.05}, (0.4, 2.5), (2.0, 3.0),
                    "short", (0.85, 0.12, 0.03), (1.0, "single"), (0.15, 0.30), 0.010, False,
                    ["jupyter", "interactive", "notebook", "dev_session", "srun_bash", "test"]),
    "lab": ({"FOR": 0.0, "NWG": 0.0, "LEH": 0.18, "KOP": 0.0}, {1: 1.0}, (0.06, 0.45), (2.8, 4.5), "short",
            (0.88, 0.10, 0.02), (7.0, "sweep"), (0.04, 0.09), 0.040, False,
            ["lab", "uebung", "exercise", "aufgabe", "blatt", "hausaufgabe"]),
    "bench": ({"FOR": 0.03, "NWG": 0.03, "LEH": 0.03, "KOP": 0.04}, {4: 0.40, 8: 0.60}, (0.3, 1.8), (2.5, 3.5), "short",
              (0.80, 0.15, 0.05), (1.8, "sweep"), (0.05, 0.10), 0.030, False,
              ["bench_nccl", "scaling", "bench_allreduce", "perf_test", "strong_scaling", "iobench"]),
}
ROUND_LIMITS = [1.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0, 36.0, 48.0]


class World:
    def __init__(self, seed=P.SEED):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.n_created = 0
        self.fake = Faker("de_DE")
        self.fake.seed_instance(seed)
        self.users = {}            # username -> dict
        self.projects = {}         # project id -> dict
        self.grants = []           # (project, year, granted, requested)
        self.requests = []         # 2027 requests
        self.taken_names = set()

    def R(self, *keys):
        """a random stream of its own for one part of the process, so a change elsewhere leaves it untouched"""
        import hashlib
        h = hashlib.blake2b(("%d|%s" % (self.seed, "|".join(str(k) for k in keys))).encode(), digest_size=8).digest()
        return np.random.default_rng(int.from_bytes(h, "big"))

    # ------------------------------------------------------------ people
    def _username(self, first, last):
        base = (first[0] + last).lower()
        base = "".join(ch for ch in base.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
                       if ch.isalpha())[:8]
        for _ in range(50):
            cand = "%s%02d" % (base, self.rng.integers(1, 99))
            if cand not in self.users:
                return cand
        return "%s%04d" % (base[:4], self.rng.integers(1000, 9999))

    def new_user(self, uni, institute):
        first, last = self.fake.first_name(), self.fake.last_name()
        u = self._username(first, last)
        self.users[u] = {"user": u, "uid": int(20000 + self.rng.integers(100, 9000)), "name": "%s %s" % (first, last),
                         "university": uni, "institute": institute, "projects": [], "created": None}
        while sum(1 for v in self.users.values() if v["uid"] == self.users[u]["uid"]) > 1:
            self.users[u]["uid"] = int(20000 + self.rng.integers(100, 9000))
        return u

    def _project_id(self):
        while True:
            pid = "p%04d" % self.rng.integers(1000, 9999)
            if pid not in self.projects:
                return pid

    def _title(self, cat):
        for _ in range(30):
            a, b = TITLE_WORDS[cat][self.rng.integers(len(TITLE_WORDS[cat]))]
            if cat == "LEH":
                t = "%s %s" % (a, b)
            else:
                t = "%s %s" % (a, b)
            qual = ["", "", "", " (Phase II)", " II", ", Teil B", " 2.0", " (Fortsetzung)"]
            t = t + qual[self.rng.integers(len(qual))]
            if t not in self.taken_names:
                self.taken_names.add(t)
                return t
        return "%s %s %d" % (a, b, self.rng.integers(100))

    def new_project(self, cat, first_year):
        self.n_created += 1
        rng = self.R("project", first_year, self.n_created)
        self.rng = rng
        pid = self._project_id()
        w = np.array([u[2] for u in UNIVERSITIES])
        uni = UNIVERSITIES[rng.choice(len(UNIVERSITIES), p=w / w.sum())]
        inst = INSTITUTES[cat][rng.integers(len(INSTITUTES[cat]))]
        pi = self.new_user(uni[0], inst)
        n_members = int(rng.integers(1, {"FOR": 7, "NWG": 6, "LEH": 14, "KOP": 5}[cat]))
        members = [self.new_user(uni[0], inst) for _ in range(n_members)]
        # a few members come from another project of the same institute (shared staff)
        for q in self.projects.values():
            if q["institute"] == inst and q["university"] == uni[0] and rng.uniform() < 0.25:
                members.append(q["members"][rng.integers(len(q["members"]))])
        members = list(dict.fromkeys(members))
        # templates: 1 to 4 drawn by the category's weights, each with its own parameters
        names = list(TEMPLATES)
        wts = np.array([TEMPLATES[n][0][cat] for n in names])
        k = int(rng.integers(2, 5))
        chosen = list(rng.choice(names, size=min(k, (wts > 0).sum()), replace=False, p=wts / wts.sum()))
        # every project runs at least one long-running kind (its grant is spent on that)
        long_kinds = ["train", "finetune", "md", "cfd"]
        if not any(n in long_kinds for n in chosen):
            lw = np.array([TEMPLATES[n][0][cat] for n in long_kinds])
            chosen[0] = long_kinds[rng.choice(4, p=lw / lw.sum())]
        tpl = []
        for n in chosen:
            spec = TEMPLATES[n]
            m = float(np.exp(rng.uniform(np.log(spec[2][0]), np.log(spec[2][1]))))
            beta = float(rng.uniform(*spec[3]))
            habit = np.array(spec[5]) * rng.uniform(0.6, 1.4, size=3)
            stem = spec[10][rng.integers(len(spec[10]))]
            tpl.append({"kind": n, "nodes": spec[1], "m": m, "beta": beta, "qos": spec[4], "habit": habit / habit.sum(),
                        "habit_cls": int(rng.choice(3, p=habit / habit.sum())),
                        "K": spec[6][0] * rng.uniform(0.7, 1.4), "mode": spec[6][1],
                        "sigma": float(rng.uniform(*spec[7])), "crash": spec[8] * rng.uniform(0.5, 1.6),
                        "chain": spec[9], "stem": stem, "weight": float(rng.uniform(0.5, 1.5))})
        ck = rng.choice(3, p=np.array(P.CKPT_SHARE[cat]))
        # a weekly submission shape: office hours, with a night/cron share and a weekend share of the project's own
        night = float(rng.beta(2, 6)) * (0.9 if cat != "LEH" else 0.3)
        weekend = float(rng.beta(3, 4))
        peak = float(rng.uniform(9.0, 15.0))
        self.projects[pid] = {"id": pid, "category": cat, "title": self._title(cat), "university": uni[0],
                              "uni_short": uni[1], "institute": inst, "pi": pi, "members": members,
                              "first_year": first_year, "templates": tpl, "ckpt": P.CKPT_HOURS[ck],
                              "night": night, "weekend": weekend, "peak": peak,
                              "deadlines": sorted(rng.uniform(0, 52, size=int(rng.integers(1, 4))).tolist()),
                              "grants": {}, "targets": {}, "last_year": first_year}
        for u in [pi] + members:
            self.users[u]["projects"].append(pid)
        return pid

    def rounds(self):
        """the 2023 round (projects already running when the record opens), then 2024 to 2026 and the 2027 requests"""
        rng = self.rng
        cats = P.CATEGORIES
        cw = np.array([P.CAT_SHARE[c] for c in cats])
        for year in (2023, 2024, 2025, 2026, 2027):
            rng = self.R("round", year)
            self.rng = rng
            if year > 2023:
                # continuing projects renew, with their requests growing with their use
                for pid, pr in list(self.projects.items()):
                    if pr["last_year"] != year - 1:
                        continue
                    rc = self.R("continue", pid, year)
                    if rc.uniform() < P.CONTINUE_P[pr["category"]] * (1.0 if year < 2027 else 1.04):
                        prev = pr["grants"][year - 1]
                        growth = float(np.exp(rc.normal(0.06, 0.28)))
                        req = prev * growth * (P.GRANT_GROWTH[year] / P.GRANT_GROWTH[year - 1])
                        self.rng = rc
                        self._grant(pid, year, req, False)
            n_new = P.NEW_PROJECTS[year]
            rr = self.R("round-new", year)
            for _ in range(n_new):
                cat = cats[rr.choice(4, p=cw / cw.sum())]
                pid = self.new_project(cat, year)
                med = P.GRANT_MEDIAN[cat] * P.GRANT_GROWTH.get(year, 1.0)
                req = float(lognormal_median(rr, med, P.GRANT_SIGMA))
                self.rng = rr
                self._grant(pid, year, req, True)
        return self

    def _grant(self, pid, year, req, new):
        rng = self.rng
        pr = self.projects[pid]
        req = float(max(200.0, round(req / 50.0) * 50.0))
        if year == 2027:
            # the 2027 round: requests only, on file; scaled by the round's appetite
            r = req * P.REQUEST_SCALE_2027 / P.GRANT_GROWTH[2027] * float(np.exp(rng.normal(0.0, 0.12)))
            r = float(max(300.0, round(r / 100.0) * 100.0))
            self.requests.append({"project": pid, "requested": r, "new": new,
                                  "submitted": P.REQUEST_DEADLINE - dt.timedelta(days=int(rng.integers(0, 40)))})
            pr["last_year"] = 2027
            return
        # the committee grants most of what is asked, trimming large requests
        trim = 1.0 if req < 6000 else float(rng.uniform(0.82, 0.97))
        granted = float(max(200.0, round(req * trim / 50.0) * 50.0))
        pr["grants"][year] = granted
        pr["last_year"] = year
        age = 0 if year == pr["first_year"] else 1
        mu = P.USE_TARGET[pr["category"]][age]
        a = mu * (mu * (1 - mu) / P.USE_SD ** 2 - 1)
        b = (1 - mu) * (mu * (1 - mu) / P.USE_SD ** 2 - 1)
        pr["targets"][year] = float(np.clip(rng.beta(a, b), 0.04, 0.985))
        self.grants.append({"project": pid, "year": year, "requested": req, "granted": granted, "new": new})

    # ------------------------------------------------------------ demand: sessions and jobs
    def weekly_profile(self, pr):
        """168 local hours, Monday 00:00 first"""
        h = np.arange(24)
        office = np.exp(-0.5 * ((h - pr["peak"]) / 4.2) ** 2)
        office[(h >= 8) & (h <= 18)] += 0.35
        prof = 0.08 + office / office.max()
        prof = (1 - pr["night"]) * prof + pr["night"] * (0.35 + 0.65 * np.exp(-0.5 * ((h - 22) / 5.0) ** 2))
        week = np.concatenate([prof] * 5 + [prof * pr["weekend"] * 0.9, prof * pr["weekend"]])
        return week / week.mean()

    def season(self, cat, year):
        """the year's weekly intensity (52 weeks): lecture periods for teaching, dips in August and late December
        for research, a ramp before the year-end for everyone"""
        w = np.arange(52)
        if cat == "LEH":
            s = np.where(((w >= 15) & (w <= 28)) | (w >= 41) | (w <= 5), 1.0, 0.12)
            s = s * (1.0 + 0.3 * np.exp(-0.5 * ((w - 26) / 1.5) ** 2) + 0.3 * np.exp(-0.5 * ((w - 4) / 1.5) ** 2))
        else:
            s = np.ones(52)
            s[(w >= 31) & (w <= 34)] = 0.72
            s[w >= 51] = 0.45
            s[(w >= 46) & (w <= 50)] = 1.05
            s[(w >= 1) & (w <= 3)] = 0.85
        return s

    def sessions_for(self, pid, year):
        """sessions of one project in one grant year: times (hours since T0), template index, planned node-hours;
        the project stops when its appetite for the grant is spent"""
        rng = self.R("sessions", pid, year)
        pr = self.projects[pid]
        grant = pr["grants"][year]
        target = pr["targets"][year] * grant
        y0 = hrs(dt.datetime(year, 1, 1, tzinfo=P.TZ))
        y1 = hrs(dt.datetime(year + 1, 1, 1, tzinfo=P.TZ))
        share = 1.0
        if year == 2023:
            y0 = 0.0
            share = (y1 - y0) / (365.0 * 24.0)
            inten_start = float(rng.uniform(0.0, 3.0)) * 168.0
        n_h = int(math.ceil(y1 - y0))
        hs = y0 + np.arange(n_h)
        how, _ = hour_of_week_local(hs)
        inten = self.weekly_profile(pr)[how]
        wk = np.minimum(((hs - hrs(dt.datetime(year if year > 2023 else 2023, 1, 1, tzinfo=P.TZ))) / 168.0).astype(int), 51)
        inten = inten * self.season(pr["category"], year)[wk]
        if year == 2023:
            inten = inten * np.clip((hs - inten_start) / (2.0 * 168.0), 0.0, 1.0)
        if year == pr["first_year"] and year > 2023:
            start_delay = float(rng.uniform(0.0, 4.0)) * 168.0
            ramp = np.clip((hs - y0 - start_delay) / (float(rng.uniform(3.0, 9.0)) * 168.0), 0.0, 1.0)
            inten = inten * ramp
        for d in pr["deadlines"]:
            inten = inten * (1.0 + 0.6 * np.exp(-0.5 * ((wk - d) / 1.1) ** 2) * (hs < y0 + (d + 0.3) * 168))
        tpl = pr["templates"]
        tw = np.array([t["weight"] for t in tpl])
        tw = tw / tw.sum()
        # expected planned node-hours of one session
        exp_nh = 0.0
        for t, w in zip(tpl, tw):
            en = sum(k * v for k, v in t["nodes"].items())
            lim = 4.0 if t["qos"] == "short" else 24.0
            ed = t["m"] * min(1.0, (math.pi / t["beta"]) / math.sin(math.pi / t["beta"])) if t["beta"] > 1 else t["m"]
            exp_nh += w * en * min(ed, lim * 0.9) * t["K"]
        exp_sessions = target / exp_nh
        tot = inten.sum()
        if tot <= 0 or exp_sessions <= 0:
            return np.zeros(0), np.zeros(0, dtype=int), np.zeros(0)
        n = int(min(rng.poisson(exp_sessions * share * 0.86), 320))
        idx = rng.choice(n_h, size=n, p=inten / tot)
        times = np.sort(hs[idx] + rng.uniform(0, 1, size=n))
        which = rng.choice(len(tpl), size=n, p=tw)
        return times, which, np.full(n, target)

    def build_jobs(self):
        """every job of the record: the sessions expanded, with chains, crashes, cancellations and resubmissions"""
        rows = []          # dicts of job attributes
        followups = []     # (job index, follower dict)
        for pid, pr in self.projects.items():
            for year in sorted(pr["grants"]):
                rng = self.R("jobs", pid, year)
                times, which, _ = self.sessions_for(pid, year)
                if len(times) == 0:
                    continue
                target = pr["targets"][year] * pr["grants"][year]
                used = 0.0
                members = pr["members"] + [pr["pi"]]
                muw = np.ones(len(members))
                muw[-1] = 0.25
                muw = muw / muw.sum()
                stop = target * (1.0 if year > 2023 else (y1_share(year))) * 1.15
                for s_i, (ts, ti) in enumerate(zip(times, which)):
                    if used >= stop:
                        break
                    t = pr["templates"][ti]
                    user = members[rng.choice(len(members), p=muw)]
                    if t["mode"] == "single":
                        K = 1
                    elif t["mode"] == "chain":
                        K = int(max(1, round(rng.gamma(2.0, t["K"] / 2.0))))
                    else:
                        K = int(rng.geometric(1.0 / max(t["K"], 1.0)))
                    K = min(K, 40)
                    nodes_opts = list(t["nodes"])
                    nw = np.array([t["nodes"][k] for k in nodes_opts])
                    nn = int(nodes_opts[rng.choice(len(nodes_opts), p=nw / nw.sum())])
                    qos = t["qos"]
                    dbase = float(loglogistic(rng, t["m"], t["beta"]))
                    # a session is bounded by what a researcher launches at once: about 500 node-hours
                    cap_k = max(1, int(500.0 / max(nn * min(dbase * 1.1, 4.0 if qos == "short" else 48.0), 1e-6)))
                    K = min(K, cap_k)
                    habit = t["habit_cls"]
                    variant = "%s%d" % (["s", "lr", "e", "run", "c", "v", "seed", "cfg"][rng.integers(8)], rng.integers(1, 400))
                    gaps = np.cumsum(rng.exponential(0.02 if t["mode"] == "sweep" else 0.01, size=K)) - 0.0
                    gaps[0] = 0.0
                    prev = -1
                    for k in range(K):
                        d = dbase * float(np.exp(rng.normal(0.0, t["sigma"])))
                        sub = ts + gaps[k]
                        maxwall = 4.0 if qos == "short" else normal_limit(sub)
                        if habit == 0:
                            wall = maxwall
                        elif habit == 1:
                            cands = [x for x in ROUND_LIMITS if x >= 1.3 * t["m"] and x <= maxwall]
                            wall = cands[0] if cands else maxwall
                        else:
                            wall = min(maxwall, max(0.5, math.ceil(2 * 1.15 * dbase) / 2.0))
                        endstate = 0
                        u = rng.uniform()
                        if u < t["crash"]:
                            d = float(rng.uniform(0.02, 0.2))
                            endstate = 2
                        elif u < t["crash"] + 0.016:
                            d = d * float(rng.uniform(0.05, 0.6))
                            endstate = 3
                        name = "%s_%s" % (t["stem"], variant) if K == 1 else "%s_%s_%d" % (t["stem"], variant, k + 1)
                        row = {"project": pid, "user": user, "year": year, "template": t["kind"], "submit": sub,
                               "nodes": nn, "qos": qos, "wall": wall, "dur": d, "ckpt": pr["ckpt"],
                               "dep": prev if t["chain"] else -1, "after": -1, "after_delay": 0.0,
                               "endstate": endstate, "name": name, "session": "%s-%d-%d" % (pid, year, s_i),
                               "cancel_before": rng.uniform() < 0.028 and endstate == 0}
                        rows.append(row)
                        j = len(rows) - 1
                        if t["chain"]:
                            prev = j
                        used += nn * min(d, wall)
                        # a resubmission after a time-out or a crash, as a follow-up job
                        if endstate == 0 and d > wall and rng.uniform() < 0.08:
                            f = dict(row)
                            f.update({"wall": maxwall if habit != 0 else maxwall, "dur": d * float(rng.uniform(0.96, 1.04)),
                                      "after": j, "after_delay": float(lognormal_median(rng, 1.5, 0.7)),
                                      "dep": -1, "name": name + "_r", "cancel_before": False})
                            followups.append(f)
                            used += nn * min(f["dur"], f["wall"])
                        elif endstate == 2 and rng.uniform() < 0.65:
                            f = dict(row)
                            f.update({"dur": dbase * float(np.exp(rng.normal(0.0, t["sigma"]))), "endstate": 0,
                                      "after": j, "after_delay": float(lognormal_median(rng, 0.7, 0.6)),
                                      "dep": -1, "name": name + "_fix", "cancel_before": False})
                            followups.append(f)
        rows.extend(followups)
        self.jobs = pd.DataFrame(rows)
        return self.jobs

    # ------------------------------------------------------------ the fleet
    def outages(self):
        """maintenance windows, rack-level events, per-node software and hardware failures, drains and scheduler
        restarts, as intervals in hours since T0"""
        rng = self.R("maintenance")
        # maintenance windows: monthly, a Tuesday or Wednesday in the first half of the month
        maint = []
        m = dt.date(2023, 11, 1)
        while m <= dt.date(2027, 12, 1):
            days = [d for d in range(2, 15) if dt.date(m.year, m.month, d).weekday() in (1, 2)]
            day = int(rng.choice(days))
            start = dt.datetime(m.year, m.month, day, 8, 0, tzinfo=P.TZ) + dt.timedelta(minutes=int(rng.integers(-20, 50)))
            if P.MAINT_LONG_MONTHS.get(m.year) == m.month:
                dur = float(rng.uniform(30.0, 34.0))
                kind = "long"
            else:
                dur = float(lognormal_median(rng, 6.6, 0.28))
                kind = "regular"
            maint.append({"start": hrs(start), "end": hrs(start) + dur, "kind": kind, "month": m})
            m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        self.maint = maint
        mstart = np.array([x["start"] for x in maint])
        mend = np.array([x["end"] for x in maint])
        # rack events over the whole period
        rack_events = []
        for r in range(1, P.RACKS + 1):
            rng = self.R("rack", r)
            r0 = hrs(P.RACK_IN_SERVICE[r])
            for kind, rate, med, sig in (("switch", P.RACK_SWITCH_RATE, 17.0, 0.5), ("pdu", P.RACK_PDU_RATE, 30.0, 0.5)):
                t = r0
                while True:
                    t += rng.exponential(1.0 / rate)
                    if t > hrs(P.SIM_END):
                        break
                    if np.any((mstart <= t) & (t <= mend)):
                        continue
                    rep = float(lognormal_median(rng, med, sig))
                    if kind == "pdu":
                        feed = int(rng.integers(0, 2))
                        nodes = [(r - 1) * 8 + feed * 4 + k for k in range(4)]
                    else:
                        nodes = [(r - 1) * 8 + k for k in range(8)]
                    rack_events.append({"start": t, "end": t + rep, "kind": kind, "rack": r, "nodes": nodes,
                                        "feed": feed if kind == "pdu" else None})
        rack_events.sort(key=lambda x: x["start"])
        # per node: software failures on an uptime hazard, hardware failures with a parts lead time
        intervals = []   # dicts: node, start, end, cls, event
        for node in range(P.N_NODES):
            rng = self.R("node", node)
            r = node // 8 + 1
            t = hrs(P.RACK_IN_SERVICE[r])
            racks_mine = [e for e in rack_events if node in e["nodes"]]
            down_until = t
            ev_i = 0
            uptime0 = t
            while t < hrs(P.SIM_END):
                # next reset points: maintenance start, rack event start
                nm = mstart[mstart > t]
                next_m = nm[0] if len(nm) else 1e18
                while ev_i < len(racks_mine) and racks_mine[ev_i]["start"] <= t:
                    ev_i += 1
                next_r = racks_mine[ev_i]["start"] if ev_i < len(racks_mine) else 1e18
                # software failure from the uptime hazard: Lambda(u) = h0 (u + (u0/(k+1)) (u/u0)^(k+1))
                E = rng.exponential(1.0)
                u = t - uptime0
                lo, hi = u, u + 20000.0
                lam = lambda x: P.SW_H0 * ((x - u) + (P.SW_U0 / (P.SW_K + 1)) * ((x / P.SW_U0) ** (P.SW_K + 1) - (u / P.SW_U0) ** (P.SW_K + 1)))
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    if lam(mid) < E:
                        lo = mid
                    else:
                        hi = mid
                t_sw = uptime0 + hi
                t_hw = t + rng.exponential(1.0 / P.HW_RATE)
                t_next = min(t_sw, t_hw, next_m, next_r)
                if t_next >= hrs(P.SIM_END):
                    break
                if t_next == next_m:
                    me = mend[mstart == next_m][0]
                    t = me + rng.uniform(0.05, 0.4)
                    uptime0 = t
                    continue
                if t_next == next_r:
                    e = racks_mine[ev_i]
                    jit = rng.uniform(0.0, 0.4)
                    intervals.append({"node": node, "start": e["start"], "end": e["end"] + jit, "cls": "rack",
                                      "event": e, "state": "DOWN"})
                    t = e["end"] + jit + rng.uniform(0.02, 0.2)
                    uptime0 = t
                    ev_i += 1
                    continue
                if t_next == t_hw:
                    rep = float(lognormal_median(rng, 4.65 * 24.0, 0.42))
                    fin = at(t_hw + rep).astimezone(P.TZ)
                    if fin.weekday() >= 5 and rng.uniform() < 0.7:
                        rep += (7 - fin.weekday()) * 24.0 + 9.0 - fin.hour
                    intervals.append({"node": node, "start": t_hw, "end": t_hw + rep, "cls": "hardware", "state": "DOWN"})
                    t = t_hw + rep + rng.uniform(0.05, 0.5)
                    uptime0 = t
                    continue
                # software failure: the repair depends on when it happens
                l = at(t_sw).astimezone(P.TZ)
                office = l.weekday() < 5 and 7.5 <= l.hour + l.minute / 60.0 <= 19.0
                if office:
                    rep = float(lognormal_median(rng, 0.33, 0.55))
                elif rng.uniform() < 0.65:
                    rep = float(lognormal_median(rng, 1.2, 0.5))
                else:
                    nxt = l.replace(hour=8, minute=int(rng.integers(0, 50)), second=0)
                    if l.hour >= 8:
                        nxt += dt.timedelta(days=1)
                    while nxt.weekday() >= 5:
                        nxt += dt.timedelta(days=1)
                    rep = (nxt - l).total_seconds() / 3600.0 + float(lognormal_median(rng, 0.5, 0.5))
                intervals.append({"node": node, "start": t_sw, "end": t_sw + rep, "cls": "software", "state": "DOWN"})
                t = t_sw + rep + rng.uniform(0.02, 0.3)
                uptime0 = t
        # administrative drains
        rng = self.R("drains")
        t = 0.0
        while True:
            t += rng.exponential(24.0 * 14)
            if t > hrs(P.SIM_END):
                break
            node = int(rng.integers(0, P.N_NODES))
            if t < hrs(P.RACK_IN_SERVICE[node // 8 + 1]):
                continue
            intervals.append({"node": node, "start": t, "end": t + float(rng.uniform(1.0, 9.0)), "cls": "admin", "state": "DRAIN"})
        # overlapping intervals on one node are merged by the fleet (a node cannot fail twice at once)
        intervals.sort(key=lambda x: (x["node"], x["start"]))
        clean = []
        for iv in intervals:
            if clean and clean[-1]["node"] == iv["node"] and iv["start"] < clean[-1]["end"]:
                clean[-1]["end"] = max(clean[-1]["end"], iv["end"])
                continue
            clean.append(iv)
        self.node_intervals = clean
        self.rack_events = rack_events
        # scheduler restarts: at the start of most maintenance windows, plus ad hoc ones
        rng = self.R("restarts")
        restarts = [mw["start"] + rng.uniform(0.2, 1.5) for mw in maint if mw["start"] < hrs(P.SIM_END) and rng.uniform() < 0.8]
        restarts += list(rng.uniform(24.0 * 30, hrs(P.SIM_END) - 24.0, size=P.RESTARTS_ADHOC))
        self.restarts = sorted(restarts)
        return clean

    # ------------------------------------------------------------ the scheduler run
    def run(self):
        self.rounds()
        jobs = self.build_jobs()
        self.outages()
        run_mask = ~jobs["cancel_before"].values
        J = jobs[run_mask].reset_index(drop=True)
        idx_map = -np.ones(len(jobs), dtype=np.int64)
        idx_map[np.where(run_mask)[0]] = np.arange(len(J))
        dep = J["dep"].values.copy()
        dep = np.where(dep >= 0, idx_map[np.maximum(dep, 0)], -1)
        after = J["after"].values.copy()
        after = np.where(after >= 0, idx_map[np.maximum(after, 0)], -1)
        # jobs whose predecessor was cancelled before start lose the link
        order = np.argsort(J["submit"].values, kind="stable")
        inv = np.empty(len(J), dtype=np.int64)
        inv[order] = np.arange(len(J))
        J = J.iloc[order].reset_index(drop=True)
        dep = np.where(dep[order] >= 0, inv[np.maximum(dep[order], 0)], -1)
        after = np.where(after[order] >= 0, inv[np.maximum(after[order], 0)], -1)
        J["dep"] = dep
        J["after"] = after
        K = {"submit": J["submit"].values.astype(float), "nodes": J["nodes"].values.astype(np.int32),
             "wall": J["wall"].values.astype(float), "dur": J["dur"].values.astype(float),
             "ckpt": J["ckpt"].values.astype(float), "dep": dep.astype(np.int32), "after": after.astype(np.int32),
             "after_delay": J["after_delay"].values.astype(float), "endstate": J["endstate"].values.astype(np.int32)}
        out_n = np.array([iv["node"] for iv in self.node_intervals], dtype=np.int32)
        out_s = np.array([iv["start"] for iv in self.node_intervals])
        out_e = np.array([iv["end"] for iv in self.node_intervals])
        # racks not yet in service are down from the start
        pre_n, pre_s, pre_e = [], [], []
        for r in range(1, P.RACKS + 1):
            if hrs(P.RACK_IN_SERVICE[r]) > 0:
                for k in range(8):
                    pre_n.append((r - 1) * 8 + k); pre_s.append(-1.0); pre_e.append(hrs(P.RACK_IN_SERVICE[r]))
        out_n = np.concatenate([out_n, np.array(pre_n, dtype=np.int32)])
        out_s = np.concatenate([out_s, np.array(pre_s)])
        out_e = np.concatenate([out_e, np.array(pre_e)])
        ms = np.array([mw["start"] for mw in self.maint if mw["start"] < hrs(P.SIM_END)])
        me = np.array([mw["end"] for mw in self.maint if mw["start"] < hrs(P.SIM_END)])
        self.kernel_inputs = (K, (out_n, out_s, out_e), (ms, me))
        R = des.simulate(P.N_NODES, K, (out_n, out_s, out_e), (ms, me), hrs(P.SIM_END), mode=P.BF_MODE,
                         bf_max=P.BF_MAX, hold=P.REQUEUE_HOLD)
        J["submit"] = R["submit"]
        J["first_start"] = R["first_start"]
        J["final_end"] = R["final_end"]
        J["final_state"] = R["final_state"]
        J["restarts"] = R["restarts"]
        J["nh"] = R["nh"]
        J["rework"] = R["rework"]
        self.ran = J
        self.seg = pd.DataFrame(R["seg"])
        self.cancelled = jobs[~run_mask].reset_index(drop=True)
        self.assign_ids()
        return self

    def assign_ids(self):
        """job ids in submission order, the counter wrapping at MaxJobId; cancelled-before-start jobs take ids too"""
        ran = self.ran
        canc = self.cancelled.copy()
        canc["final_end"] = canc["submit"] + lognormal_median(self.R("cancel"), 1.0, 0.9, size=len(canc))
        allsub = np.concatenate([ran["submit"].values, canc["submit"].values])
        kind = np.concatenate([np.zeros(len(ran), dtype=int), np.ones(len(canc), dtype=int)])
        order = np.argsort(allsub, kind="stable")
        span = P.MAX_JOB_ID - P.FIRST_JOB_ID + 1
        ids = P.FIRST_JOB_ID + (np.arange(len(allsub)) % span)
        jid = np.empty(len(allsub), dtype=np.int64)
        jid[order] = ids
        ran["jobid"] = jid[:len(ran)]
        canc["jobid"] = jid[len(ran):]
        epoch = np.empty(len(allsub), dtype=np.int64)
        epoch[order] = np.arange(len(allsub)) // span
        ran["epoch"] = epoch[:len(ran)]
        canc["epoch"] = epoch[len(ran):]
        self.cancelled = canc


def y1_share(year):
    """the share of a grant year the record covers (the warm-up year opens at T0)"""
    y0 = hrs(dt.datetime(year, 1, 1, tzinfo=P.TZ))
    y1 = hrs(dt.datetime(year + 1, 1, 1, tzinfo=P.TZ))
    return (y1 - max(y0, 0.0)) / (y1 - y0)


def normal_limit(h):
    """the `normal` quality of service's limit in force at hour h since T0"""
    lim = P.QOS_NORMAL_LIMITS[0][1]
    for d, l in P.QOS_NORMAL_LIMITS:
        if h >= hrs(d):
            lim = l
    return lim


def world(seed=P.SEED):
    return World(seed).run()
