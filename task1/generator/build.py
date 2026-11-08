"""Cut the task1 pack under target/ from the world in world.py.

    python3 task1/generator/build.py

Writes the eleven input files, metadata.json (outside target/) and generator/truth.json (the clean truth the checks
read; never shipped). Deterministic: every random draw comes from SEED, every timestamp is in-fiction, and every
container's metadata is fixed, so two runs are byte-identical.
"""
import csv
import datetime as dt
import io
import json
import os
import shutil
import sys
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as Wd                                   # noqa: E402
from common import *                                 # noqa: E402,F401,F403

ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'
EUROSTAT_URL = ('https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/edat_aes_l21/'
                '?format=SDMX-CSV&compressed=false')

FILES = dict(
    members='members_export_2026-11-03.csv',
    billing='billing_events_2022-01_2026-10.csv',
    lessons='lesson_activity_monthly_2022-01_2026-10.csv',
    tutors='tutor_directory_2026-11-03.csv',
    attribution='signup_attribution_2022-01_2026-10.csv',
    agency='fenwright_aut26_closeout_and_invoices.xlsx',
    plans='plans_and_promotions.json',
    standard='growth_review_standard.pdf',
    ecb='ecb_euro_reference_rates_2022-01_2026-11.csv',
    eurostat='eurostat_edat_aes_l21_foreign_languages_known.csv',
    nps='nps_in_app_responses_2026-01_2026-10.csv',
)
DISTRACTORS = ['eurostat', 'nps']


# --------------------------------------------------------------------------------------------- real sources
def fetch_real():
    os.makedirs(CACHE, exist_ok=True)
    ecb_zip = os.path.join(CACHE, 'eurofxref-hist.zip')
    if not os.path.exists(ecb_zip):
        urllib.request.urlretrieve(ECB_URL, ecb_zip)
    es = os.path.join(CACHE, 'edat_aes_l21.csv')
    if not os.path.exists(es):
        urllib.request.urlretrieve(EUROSTAT_URL, es)
    import zipfile
    with zipfile.ZipFile(ecb_zip) as z:
        raw = z.read('eurofxref-hist.csv').decode('utf-8')
    return raw, open(es, encoding='utf-8').read()


def ecb_table(raw):
    rows = list(csv.reader(io.StringIO(raw)))
    head = [h for h in rows[0]]
    out = []
    for r in rows[1:]:
        if not r or not r[0]:
            continue
        d = dt.date.fromisoformat(r[0])
        if dt.date(2022, 1, 1) <= d <= PULL_DATE:
            out.append(r)
    out.sort(key=lambda r: r[0], reverse=True)          # the ECB publishes newest first
    rates = {}
    gi, ci = head.index('GBP'), head.index('CHF')
    for r in out:
        rates[r[0]] = (float(r[gi]), float(r[ci]))
    return head, out, rates


# --------------------------------------------------------------------------------------------- helpers
def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        w.writerows(rows)


def iso_z(ts):
    return ts.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def list_price(plan, cur, d):
    p = PLANS[plan]['price'][cur]
    return p[0] if d < PRICE_CHANGE else p[1]


def plan_code(plan, d):
    return PLANS[plan]['old'] if d < PRICE_CHANGE else PLANS[plan]['new']


# --------------------------------------------------------------------------------------------- the cut
def main():
    rng = np.random.default_rng(SEED + 1)
    W = Wd.build_world(SEED)
    M, T = W.M, W.T
    n_m, n_t = len(M['sign']), len(T['hired'])
    os.makedirs(TARGET, exist_ok=True)
    for f in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, f))
    ecb_raw, eurostat_raw = fetch_real()
    ecb_head, ecb_rows, rates = ecb_table(ecb_raw)

    # ---- member identities and calendars
    order = sorted(range(n_m), key=lambda x: (M['sign'][x], M['dom'][x], x))
    mid = {}
    nxt = 1004117
    for x in order:
        nxt += int(rng.integers(1, 40))
        mid[x] = 'CV%07d' % nxt
    sec_of_day = rng.integers(6 * 3600, 21 * 3600 + 1800, size=n_m)
    late_aut = [x for x in order if M['camp'][x] == CAMPAIGN and M['sign'][x] == Wd.CUT][-6:]
    late_aut = set(late_aut)                      # six AUT26 sign-ups that land after midnight Berlin on 31 October

    def signup_ts(x):
        y, m = month_of(M['sign'][x])
        if x in late_aut:
            return dt.datetime(2026, 10, 31, 23, int(rng.integers(5, 55)), int(rng.integers(0, 60)), tzinfo=UTC)
        d = min(M['dom'][x], days_in(y, m))
        return dt.datetime(y, m, d, tzinfo=UTC) + dt.timedelta(seconds=int(sec_of_day[x]))

    sig_ts = {x: signup_ts(x) for x in range(n_m)}
    currency = {x: Wd.CURRENCY.get(M['country'][x], 'EUR') for x in range(n_m)}

    # plan path per member (plan switches are export texture; retention never depends on them)
    plan_path = {}
    for x in range(n_m):
        p = M['plan'][x]; path = []
        for k in range(1, M['paid'][x] + 2):
            if k > 3 and rng.random() < 0.008:
                p = 1 - p
            path.append(p)
        plan_path[x] = path

    # promotions
    promo = {}
    for x in range(n_m):
        if M['camp'][x] == CAMPAIGN:
            promo[x] = 'AUT26-WELCOME10'
        elif M['camp'][x] == 'SPR25':
            promo[x] = 'SPR25-WELCOME10'
        elif rng.random() < 0.09:
            promo[x] = 'FRIEND15'
    PROMO_OFF = {'AUT26-WELCOME10': .10, 'SPR25-WELCOME10': .10, 'FRIEND15': .15}

    # cancellation kinds
    kind = {}
    for x in range(n_m):
        c = M['cancel'][x]
        if c is None:
            continue
        k = M['paid'][x]
        if k == 1 and rng.random() < 0.30:
            kind[x] = 'refund_cooling_off'
        elif k >= 2 and c < Wd.CUT and rng.random() < 0.24:
            kind[x] = 'payment_failed'
        else:
            kind[x] = 'voluntary'

    # ---- billing events
    ev = []          # (created_at, row)
    def eid(*p):
        return 'evt_' + stable_hex('ev', *p)
    charge_ids = {}
    first_charge = {}
    for x in range(n_m):
        y0, m0 = month_of(M['sign'][x])
        cur = currency[x]
        for k in range(1, M['paid'][x] + 1):
            t = M['sign'][x] + k - 1
            y, m = month_of(t)
            if k == 1:
                ts = sig_ts[x] + dt.timedelta(seconds=int(rng.integers(20, 300)))
            else:
                d = min(M['dom'][x], days_in(y, m))
                ts = dt.datetime(y, m, d, 3, 0, tzinfo=UTC) + dt.timedelta(seconds=int(rng.integers(0, 7200)))
            period = ts.astimezone(BERLIN).date()
            plan = plan_path[x][k - 1]
            price = list_price(plan, cur, period)
            amt = price
            pc = ''
            if k == 1 and x in promo:
                pc = promo[x]; amt = round(price * (1 - PROMO_OFF[pc]), 2)
            attempts = [ts]
            if k > 1 and rng.random() < 0.05:
                attempts = [ts, ts + dt.timedelta(days=2, minutes=int(rng.integers(0, 90)))]
                if rng.random() < 0.4:
                    attempts.append(ts + dt.timedelta(days=4, minutes=int(rng.integers(0, 90))))
                    if rng.random() < 0.3:
                        attempts.append(ts + dt.timedelta(days=7, minutes=int(rng.integers(0, 90))))
            for a, ats in enumerate(attempts, start=1):
                ok = a == len(attempts)
                fc = '' if ok else str(rng.choice(['card_declined', 'insufficient_funds', 'expired_card'], p=[.5, .35, .15]))
                e = eid(x, k, a)
                ev.append((ats, [e, mid[x], 'charge', iso_z(ats), period.isoformat(), plan_code(plan, period), cur,
                                 amt, 'succeeded' if ok else 'failed', a, fc, pc, '']))
                if ok:
                    charge_ids[(x, k)] = (e, amt, ats, cur, period, plan)
                    if k == 1:
                        first_charge[x] = (ats, amt, price, cur)
        # refunds
        if kind.get(x) == 'refund_cooling_off':
            e, amt, ats, cur_, period, plan = charge_ids[(x, 1)]
            rts = ats + dt.timedelta(days=int(rng.integers(1, 13)), hours=int(rng.integers(0, 20)))
            ev.append((rts, [eid(x, 'r1'), mid[x], 'refund', iso_z(rts), period.isoformat(), plan_code(plan, period),
                             cur_, amt, 'succeeded', 1, '', '', e]))
        for k in range(2, M['paid'][x] + 1):
            if rng.random() < 0.008:
                e, amt, ats, cur_, period, plan = charge_ids[(x, k)]
                part = round(amt * float(rng.choice([.25, .3, .5])), 2)
                rts = ats + dt.timedelta(days=int(rng.integers(3, 20)))
                ev.append((rts, [eid(x, 'g', k), mid[x], 'refund', iso_z(rts), period.isoformat(),
                                 plan_code(plan, period), cur_, part, 'succeeded', 1, '', '', e]))
        # involuntary churn: the next charge fails four times
        if kind.get(x) == 'payment_failed':
            k = M['paid'][x] + 1
            t = M['sign'][x] + k - 1
            y, m = month_of(t)
            d = min(M['dom'][x], days_in(y, m))
            ts = dt.datetime(y, m, d, 3, 0, tzinfo=UTC) + dt.timedelta(seconds=int(rng.integers(0, 7200)))
            period = ts.astimezone(BERLIN).date()
            plan = plan_path[x][k - 1]
            price = list_price(plan, currency[x], period)
            for a, off in enumerate([0, 2, 4, 7], start=1):
                ats = ts + dt.timedelta(days=off, minutes=int(rng.integers(0, 90)) if a > 1 else 0)
                if ats.date() > CUT_DATE + dt.timedelta(days=2):
                    break
                ev.append((ats, [eid(x, k, a), mid[x], 'charge', iso_z(ats), period.isoformat(),
                                 plan_code(plan, period), currency[x], price, 'failed', a,
                                 str(rng.choice(['card_declined', 'insufficient_funds', 'expired_card'], p=[.45, .4, .15])),
                                 '', '']))
    ev = [e for e in ev if e[0].date() <= PULL_DATE]
    ev.sort(key=lambda e: (e[0], e[1][0]))
    rows = []
    for ts, r in ev:
        amt = r[7]
        if ts >= AMOUNT_MINOR_FROM:
            r = r[:7] + ['', '%d' % round(amt * 100)] + r[8:]
        else:
            r = r[:7] + ['%.2f' % amt, ''] + r[8:]
        rows.append(r)
        if rng.random() < 0.006:                       # webhook replay
            rows.append(list(r))
    write_csv(os.path.join(TARGET, FILES['billing']),
              ['event_id', 'member_id', 'event_type', 'created_at', 'billing_period_start', 'plan_code', 'currency',
               'amount', 'amount_minor', 'status', 'attempt', 'failure_code', 'promo_code', 'refund_of'], rows)

    # ---- members export
    mrows = []
    for x in order:
        c = M['cancel'][x]
        status = 'active' if c is None else 'cancelled'
        reason = kind.get(x, '')
        cdate = ''
        if c is not None:
            y, m = month_of(c)
            if reason == 'refund_cooling_off':
                cdate = (first_charge[x][0] + dt.timedelta(days=3)).astimezone(BERLIN).date().isoformat()
            elif reason == 'payment_failed':
                yy, mm_ = month_of(c + 1)
                cdate = dt.date(yy, mm_, min(M['dom'][x], days_in(yy, mm_))).isoformat()
            else:
                lo = min(M['dom'][x], days_in(y, m))
                cdate = dt.date(y, m, int(rng.integers(lo, days_in(y, m) + 1))).isoformat()
            if dt.date.fromisoformat(cdate) > PULL_DATE:
                cdate = PULL_DATE.isoformat()
        mrows.append([mid[x], iso_z(sig_ts[x]), M['country'][x], currency[x], LANG_NAME[M['lang'][x]],
                      plan_code(M['plan'][x], sig_ts[x].astimezone(BERLIN).date()), status, cdate, reason,
                      'yes' if rng.random() < 0.62 else 'no'])
    write_csv(os.path.join(TARGET, FILES['members']),
              ['member_id', 'created_at', 'country', 'billing_currency', 'learning_language', 'plan_at_signup',
               'status', 'cancel_requested_on', 'cancel_reason', 'marketing_consent'], mrows)

    # ---- tutors: ids, names, countries
    TCOUNTRY = {'EN': (['GB', 'US', 'IE', 'CA', 'AU', 'NZ', 'ZA'], [.30, .25, .12, .10, .08, .05, .10]),
                'ES': (['ES', 'MX', 'AR', 'CO'], [.40, .25, .15, .20]),
                'DE': (['DE', 'AT'], [.75, .25]),
                'FR': (['FR', 'BE', 'CA'], [.75, .15, .10]),
                'IT': (['IT'], [1.0])}
    LOCALE = {'GB': 'en_GB', 'US': 'en_US', 'IE': 'en_IE', 'CA': 'en_US', 'AU': 'en_US', 'NZ': 'en_NZ',
              'ZA': 'en_GB', 'ES': 'es_ES', 'MX': 'es_MX', 'AR': 'es_AR', 'CO': 'es_CO', 'DE': 'de_DE',
              'AT': 'de_AT', 'FR': 'fr_FR', 'BE': 'fr_BE', 'IT': 'it_IT'}
    TZ = {'GB': 'Europe/London', 'US': 'America/New_York', 'IE': 'Europe/Dublin', 'CA': 'America/Toronto',
          'AU': 'Australia/Sydney', 'NZ': 'Pacific/Auckland', 'ZA': 'Africa/Johannesburg', 'ES': 'Europe/Madrid',
          'MX': 'America/Mexico_City', 'AR': 'America/Argentina/Buenos_Aires', 'CO': 'America/Bogota',
          'DE': 'Europe/Berlin', 'AT': 'Europe/Vienna', 'FR': 'Europe/Paris', 'BE': 'Europe/Brussels',
          'IT': 'Europe/Rome'}
    import faker
    fk = {loc: faker.Faker(loc) for loc in set(LOCALE.values())}
    for i, loc in enumerate(sorted(fk)):
        fk[loc].seed_instance(SEED * 100 + i)
    tnum = {}
    n = 10000
    for i in range(n_t):
        n += int(rng.integers(1, 6))
        tnum[i] = n
    tcountry = {}
    for i in range(n_t):
        cs, ps = TCOUNTRY[T['lang'][i]]
        tcountry[i] = str(rng.choice(cs, p=ps))

    # ---- lesson activity (member x tutor x month with a booked lesson)
    eng_p = {0: .58, 1: .86, 2: .95}
    taught_months = {}
    lrows = []
    plan_by_k = plan_path
    for (x, t, k, tu, ten, st, c) in W.mm:
        if tu < 0 or (x in late_aut and t == Wd.CUT):
            continue
        plan = plan_by_k[x][k - 1]
        booked = PLANS[plan]['lessons'] + int(rng.choice([0, 0, 0, 1, -1]))
        comp = int(rng.binomial(booked, eng_p[M['eng'][x]]))
        rest = booked - comp
        by_tutor = int(rng.binomial(rest, .15))
        by_member = int(rng.binomial(rest - by_tutor, .6))
        noshow = rest - by_tutor - by_member
        minutes = comp * 50 - int(rng.integers(0, 3)) * 5 * (comp > 0)
        y, m = month_of(t)
        tid = 'T-%06d' % tnum[tu]
        lrows.append([month_str(t), mid[x], tid, M['lang'][x], booked, comp, by_member, by_tutor, noshow, minutes])
        taught_months.setdefault(tu, []).append(t)
    lrows.sort(key=lambda r: (r[0], r[1], r[2]))
    write_csv(os.path.join(TARGET, FILES['lessons']),
              ['month', 'member_id', 'tutor_id', 'language', 'lessons_booked', 'lessons_completed',
               'cancelled_by_member', 'cancelled_by_tutor', 'no_shows', 'minutes_taught'], lrows)

    # ---- tutor directory
    trows = []
    for i in range(n_t):
        loc = LOCALE[tcountry[i]]
        name = '%s %s.' % (fk[loc].first_name(), fk[loc].last_name()[0])
        taught = i in taught_months
        if T['start'][i] is None:
            status = 'pending' if T['off'][i] is None else 'offboarded'
        elif T['off'][i] is None:
            status = 'active'
        else:
            status = 'inactive' if rng.random() < .6 else 'offboarded'
        if taught and len(taught_months[i]) >= 3:
            cnt = int(len(taught_months[i]) * rng.uniform(.25, .6))
            rating = '%.2f' % min(5.0, max(3.6, rng.normal(4.72, .18))) if cnt >= 5 else ''
        else:
            cnt, rating = 0, ''
        trows.append(['T-%06d' % tnum[i], name, tcountry[i], T['lang'][i].lower(),
                      'Y' if rng.random() < .86 else 'N', str(rng.choice(['A', 'B', 'C'], p=[.3, .5, .2])),
                      rating, cnt, status, 'Y' if rng.random() < .7 else 'N', TZ[tcountry[i]]])
    trows.sort(key=lambda r: r[0])
    write_csv(os.path.join(TARGET, FILES['tutors']),
              ['tutor_id', 'display_name', 'country', 'teaches', 'native_speaker', 'price_band', 'rating',
               'ratings_count', 'profile_status', 'video_intro', 'timezone'], trows)

    # ---- sign-up attribution (paid members and accounts that never paid)
    AUT_CODES = [('meta', 'paid_social', ['aut26_meta_v2', 'AUT26-Meta', 'aut26_meta_retarget'], .44),
                 ('google', 'cpc', ['aut26_google_search', 'AUT26_Google'], .26),
                 ('tiktok', 'paid_social', ['aut26_tiktok', 'AUT26-TT'], .15),
                 ('youtube', 'video', ['aut26_youtube', 'AUT26_YT_preroll'], .10),
                 ('sprachblog', 'affiliate', ['aut26-affiliate-sprachblog'], .05)]
    SPR_CODES = [('meta', 'paid_social', ['spr25_meta'], .6), ('google', 'cpc', ['SPR25-Google'], .4)]
    ORG = [('(direct)', '(none)', '(not set)', .48), ('google', 'organic', '(not set)', .14),
           ('google', 'cpc', 'brand_search', .12), ('blog', 'referral', 'seo_blog', .08),
           ('friend', 'referral', 'referral_programme', .09), ('newsletter', 'email', 'newsletter', .04),
           ('meta', 'paid_social', 'retarget_always_on', .05)]

    def utm(kind_):
        if kind_ in ('AUT26', 'SPR25'):
            pool = AUT_CODES if kind_ == 'AUT26' else SPR_CODES
            j = int(rng.choice(len(pool), p=[p[3] for p in pool]))
            src, med, codes, _ = pool[j]
            return src, med, str(rng.choice(codes))
        j = int(rng.choice(len(ORG), p=[o[3] for o in ORG]))
        return ORG[j][0], ORG[j][1], ORG[j][2]
    arows = []
    seq = 70000000
    for x in order:
        seq += int(rng.integers(1, 9))
        src, med, camp = utm(M['camp'][x] or 'organic')
        arows.append(['su_%d' % seq, mid[x], iso_z(sig_ts[x] - dt.timedelta(seconds=int(rng.integers(30, 900)))),
                      src, med, camp, str(rng.choice(['/', '/pricing', '/learn-english', '/learn-spanish', '/tutors'])),
                      str(rng.choice(['ios', 'android', 'web'], p=[.38, .27, .35])), M['country'][x]])
    # accounts that signed up and never paid
    acc = nxt
    for t in range(0, Wd.CUT + 1):
        y, m = month_of(t)
        n_paid_t = sum(1 for x in range(n_m) if M['sign'][x] == t)
        n_aut = sum(1 for x in range(n_m) if M['sign'][x] == t and M['camp'][x] == CAMPAIGN)
        for q in range(int(n_paid_t * rng.uniform(.75, .95)) + int(n_aut * 1.6)):
            acc += int(rng.integers(1, 30)); seq += int(rng.integers(1, 9))
            d = int(rng.integers(1, days_in(y, m) + 1))
            ts = dt.datetime(y, m, d, tzinfo=UTC) + dt.timedelta(seconds=int(rng.integers(0, 86400)))
            k_ = 'AUT26' if q < n_aut * 1.6 else ('SPR25' if t in (38, 39) and rng.random() < .3 else 'organic')
            src, med, camp = utm(k_)
            arows.append(['su_%d' % seq, 'CV%07d' % (acc % 10000000), iso_z(ts), src, med, camp,
                          str(rng.choice(['/', '/pricing', '/learn-english', '/learn-spanish', '/tutors'])),
                          str(rng.choice(['ios', 'android', 'web'], p=[.38, .27, .35])),
                          str(rng.choice(Wd.COUNTRIES, p=Wd.COUNTRY_P))])
    arows.sort(key=lambda r: (r[2], r[0]))
    write_csv(os.path.join(TARGET, FILES['attribution']),
              ['signup_id', 'account_id', 'signup_at', 'utm_source', 'utm_medium', 'utm_campaign', 'landing_page',
               'device', 'country'], arows)

    # ---- ECB and Eurostat, as published
    with open(os.path.join(TARGET, FILES['ecb']), 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f, lineterminator='\n')
        wr.writerow(ecb_head)
        wr.writerows(ecb_rows)
    with open(os.path.join(TARGET, FILES['eurostat']), 'w', encoding='utf-8', newline='') as f:
        f.write(eurostat_raw)

    # ---- NPS responses (distractor)
    nrows = []
    for x in range(n_m):
        for k in range(1, M['paid'][x] + 1):
            t = M['sign'][x] + k - 1
            if t < 48 or rng.random() > .05:
                continue
            y, m = month_of(t)
            d = int(rng.integers(1, days_in(y, m) + 1))
            ts = dt.datetime(y, m, d, tzinfo=UTC) + dt.timedelta(seconds=int(rng.integers(25000, 80000)))
            base = {0: 6.1, 1: 7.9, 2: 8.8}[M['eng'][x]]
            sc = int(np.clip(round(rng.normal(base, 1.9)), 0, 10))
            nrows.append(['nps_' + stable_hex('n', x, k, n=12), mid[x], iso_z(ts), sc,
                          str(rng.choice(['ios', 'android', 'web'], p=[.42, .3, .28])),
                          str(rng.choice(['4.18', '4.19', '4.20', '4.21', '4.22']))])
    nrows.sort(key=lambda r: (r[2], r[0]))
    write_csv(os.path.join(TARGET, FILES['nps']),
              ['response_id', 'member_id', 'responded_at', 'score', 'platform', 'app_version'], nrows)

    # ---- agency workbook, plans, standard
    import docs
    camp_members = [x for x in range(n_m) if M['camp'][x] == CAMPAIGN]
    media = docs.agency_workbook(os.path.join(TARGET, FILES['agency']), rng, rates, len(camp_members))
    docs.plans_json(os.path.join(TARGET, FILES['plans']))
    docs.standard_pdf(os.path.join(TARGET, FILES['standard']))

    # ---- metadata and the clean truth
    docs.metadata(os.path.join(TASK, 'metadata.json'), FILES, DISTRACTORS)
    truth = dict(
        seed=SEED, members=n_m, tutors=n_t,
        aut26_world=[mid[x] for x in camp_members],
        aut26_late_berlin=[mid[x] for x in sorted(late_aut)],
        member_ids={str(x): mid[x] for x in range(n_m)},
        tutor_ids={str(i): 'T-%06d' % tnum[i] for i in range(n_t)},
        media=media,
    )
    json.dump(truth, open(os.path.join(HERE, 'truth.json'), 'w'), indent=1, sort_keys=True)
    # in-fiction file times
    stamp = PULL_TS.replace(tzinfo=UTC).timestamp()
    for f in os.listdir(TARGET):
        os.utime(os.path.join(TARGET, f), (stamp, stamp))
    print('cut %d files into %s' % (len(os.listdir(TARGET)), TARGET))


if __name__ == '__main__':
    main()
