"""Reading the pack: every file parsed the way the analyst has to read it (each on its own clock, the archive's two
message formats and its standby server's echoes, the register's tag crosswalk, the outage record's steps), into
one set of tables the golden and every hurried pass share. Nothing here reads the generator's world."""
import datetime as dt
import os
import re
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

CENTRAL = ZoneInfo('America/Chicago')
CST = dt.timezone(dt.timedelta(hours=-6))

FILES = {
    'adms': 'adms_flisr_event_archive_2022-2026.csv',
    'oms': 'oms_outage_events_2022-2026.csv',
    'scada': 'scada_hourly_amps_2025-2026.csv',
    'devents': 'scada_device_events_2022-2026.csv',
    'register': 'da_device_register_2026.xlsx',
    'loops': 'flisr_loop_configuration_2026.xlsx',
    'maint': 'da_maintenance_records_2019-2026.xlsx',
    'weather': 'kmkt_hourly_weather_2022-2026.csv',
    'incidents': 'comms_and_control_system_incidents_2022-2026.csv',
    'capital': 'distribution_capital_works_2019-2027.xlsx',
    'loads': 'large_load_requests_2026-2027.xlsx',
    'dashboard': 'adms_flisr_kpi_dashboard_2022-2026.xlsx',
}


def _sheet(path, name, header_row=None):
    raw = pd.read_excel(path, sheet_name=name, header=None)
    if header_row is None:
        # the header is the first row whose cells are all text and that is followed by data
        for i in range(min(8, len(raw))):
            row = raw.iloc[i]
            if row.notna().sum() >= max(2, raw.shape[1] - 2) and all(isinstance(x, str) for x in row.dropna()):
                header_row = i
                break
    df = raw.iloc[header_row + 1:].copy()
    df.columns = [str(c) for c in raw.iloc[header_row]]
    return df.dropna(how='all').reset_index(drop=True)


def central_naive_to_utc(s):
    """outage record times: Central prevailing wall clock, no offset (the repeated hour in November read as the first)"""
    t = pd.to_datetime(s, format='%m/%d/%Y %H:%M')
    return t.dt.tz_localize(CENTRAL, ambiguous=True, nonexistent='shift_forward').dt.tz_convert('UTC')


class Pack:
    def __init__(self, target):
        self.dir = target
        p = lambda k: os.path.join(target, FILES[k])
        # register and configuration
        self.reg = _sheet(p('register'), 'Devices')
        self.cbs = _sheet(p('register'), 'Breakers')
        self.loops = _sheet(p('loops'), 'Loops')
        self.secs = _sheet(p('loops'), 'Sections')
        self.feeders = _sheet(p('loops'), 'Feeders')
        self.changes = _sheet(p('loops'), 'Changes')
        self.tag2asset = {}
        for _, r in self.reg.iterrows():
            self.tag2asset[str(r['ADMS tag'])] = r['Asset No']
            self.tag2asset[str(r['ADMS tag before 18 Mar 2025'])] = r['Asset No']
        for _, r in self.cbs.iterrows():
            f = r['Feeder']
            self.tag2asset[f + '_CB'] = f + ' CB'
            self.tag2asset[f + '-CB'] = f + ' CB'
        self.dev = {r['Asset No']: r for _, r in self.reg.iterrows()}
        self.loop_of_feeder = {}
        self.partner = {}
        self.scheme_loop = {}
        for _, r in self.loops.iterrows():
            self.loop_of_feeder[r['Feeder A']] = r['Loop']
            self.loop_of_feeder[r['Feeder B']] = r['Loop']
            self.partner[r['Feeder A']] = r['Feeder B']
            self.partner[r['Feeder B']] = r['Feeder A']
            self.scheme_loop[r['ADMS scheme']] = r['Loop']
        self.in_service = {r['Loop']: pd.Timestamp(r['FLISR in service']).date() for _, r in self.loops.iterrows()}
        self.tie = {r['Loop']: r['Tie switch'] for _, r in self.loops.iterrows()}
        self.sec_cust = {(r['Feeder'], int(r['Section'])): int(r['Customers (Sep 2026)']) for _, r in self.secs.iterrows()}
        self.sec_km = {(r['Feeder'], int(r['Section'])): float(r['Main line (km)']) for _, r in self.secs.iterrows()}
        self.dev_at = {}
        for _, r in self.reg.iterrows():
            if r['Position'].startswith('Midline recloser'):
                self.dev_at[(r['Feeder'], 'R' + r['Position'][-1])] = r['Asset No']
        self.emerg = {r['Feeder']: int(r['Emergency limit (A)']) for _, r in self.feeders.iterrows()}
        self.recon = []
        for _, r in self.changes.iterrows():
            m = re.search(r'about (\d+) customers moved from section 3 to section 2', str(r['Change']))
            if m:
                self.recon.append((pd.Timestamp(r['Date']).date(), r['Feeder'], int(m.group(1))))
        self._adms = None
        self._oms = None
        self._dev = None
        self._wx = None
        self._scada = None
        self.p = p

    # -------------------------------------------------------------------------------------------------- tables
    def customers(self, f, k, when):
        """section customers at a date: the September 2026 figure, with the October 2024 relocations undone before
        their date"""
        c = self.sec_cust[(f, k)]
        for d, ff, moved in self.recon:
            if ff == f and when < d:
                c += -moved if k == 2 else (moved if k == 3 else 0)
        return c

    @property
    def adms(self):
        if self._adms is None:
            df = pd.read_csv(self.p('adms'))
            df['t'] = pd.to_datetime(df['event_time_utc'], utc=True)
            df = df.sort_values(['scheme', 'message', 't'])
            echo = (df['scheme'] == df['scheme'].shift()) & (df['message'] == df['message'].shift()) & \
                ((df['t'] - df['t'].shift()).dt.total_seconds() < 1.0)
            df = df[~echo].sort_values(['t', 'record_no']).reset_index(drop=True)
            df['loop'] = df['scheme'].map(self.scheme_loop)
            df['kind'], df['tag'], df['n'] = zip(*df['message'].map(_parse_adms))
            df['asset'] = df['tag'].map(lambda x: self.tag2asset.get(x) if isinstance(x, str) else None)
            self._adms = df
        return self._adms

    @property
    def oms(self):
        if self._oms is None:
            df = pd.read_csv(self.p('oms'))
            df['Feeder'] = df['Feeder'].str.replace('-', '', regex=False)
            df['start'] = central_naive_to_utc(df['Outage Start'])
            df['step_t'] = central_naive_to_utc(df['Step Restored'])
            self._oms = df
        return self._oms

    @property
    def devents(self):
        if self._dev is None:
            df = pd.read_csv(self.p('devents'))
            df['t'] = pd.to_datetime(df['Time (CST)']).dt.tz_localize(CST).dt.tz_convert('UTC')
            df['amps'] = pd.to_numeric(df['Value'].str.extract(r'^(\d+) A$')[0], errors='coerce')
            v = df['Value'].str.extract(r'V_REST=([\d.]+) V_LOAD=([\d.]+)')
            df['v_rest'] = pd.to_numeric(v[0], errors='coerce')
            df['v_load'] = pd.to_numeric(v[1], errors='coerce')
            df['feeder'] = df['Device'].map(self._feeder_of_device)
            self._dev = df
        return self._dev

    def _feeder_of_device(self, d):
        if isinstance(d, str) and d.endswith(' CB'):
            return d[:-3]
        r = self.dev.get(d)
        return None if r is None else r['Feeder']

    @property
    def wx(self):
        if self._wx is None:
            df = pd.read_csv(self.p('weather'), na_values=['M'])
            df['t'] = pd.to_datetime(df['valid']).dt.tz_localize('UTC')
            df['temp_c'] = (df['tmpf'] - 32) * 5 / 9
            df['hour'] = (df['t'] + pd.Timedelta(minutes=7)).dt.floor('h')
            s = df.set_index('hour')['temp_c'].sort_index()
            s = s[~s.index.duplicated()]
            full = pd.date_range(s.index.min(), s.index.max(), freq='h')
            self._wx = s.reindex(full).interpolate(limit=3)
        return self._wx

    @property
    def scada(self):
        if self._scada is None:
            df = pd.read_csv(self.p('scada'))
            df.index = pd.to_datetime(df['TIMESTAMP_CST']).dt.tz_localize(CST).dt.tz_convert('UTC')
            self._scada = df.drop(columns=['TIMESTAMP_CST'])
        return self._scada

    def temp_at(self, ts):
        h = pd.Timestamp(ts).floor('h')
        try:
            return float(self.wx.loc[h])
        except KeyError:
            return float('nan')


def _parse_adms(m):
    """the archive's messages in both releases' wording, as (kind, device tag, number)"""
    u = m.upper()
    g = re.search(r'LOCKOUT(?: DEVICE=| )([A-Z0-9_\-]+)', u)
    if u.startswith('FLISR START') or u.startswith('FLISR SEQUENCE STARTED'):
        return 'START', g.group(1) if g else None, None
    if u.startswith('FLISR NOT STARTED'):
        t = re.search(r'\(([A-Z0-9_\-]+) COMM\)|COMMUNICATION LOST: ([A-Z0-9_\-]+)\)', u)
        tag = (t.group(1) or t.group(2)) if t else None
        return 'NOT STARTED', tag, None
    t = re.search(r'^FPI ([A-Z0-9_\-]+): (FAULT|NO FAULT)$', u) or re.search(r'^FAULT INDICATION: ([A-Z0-9_\-]+) = (YES|NO)$', u)
    if t:
        return 'FPI', t.group(1), 1 if t.group(2) in ('FAULT', 'YES') else 0
    t = re.search(r'SECTION (\d)', u)
    if u.startswith('FAULT LOCATED'):
        return 'LOCATED', None, int(t.group(1)) if t else None
    t = re.search(r'^OPEN ([A-Z0-9_\-]+)(?:: CONFIRMED| CONFIRMED)$', u)
    if t:
        return 'OPENED', t.group(1), None
    t = re.search(r'COMMAND TIMEOUT: ([A-Z0-9_\-]+) \((\w+)\)|COMMAND (\w+) TO ([A-Z0-9_\-]+) TIMED OUT', u)
    if t:
        return 'TIMEOUT', t.group(1) or t.group(4), None
    t = re.search(r'OPERATION FAILED: ([A-Z0-9_\-]+)|COMMAND \w+ TO ([A-Z0-9_\-]+) FAILED', u)
    if t:
        return 'OP FAILED', t.group(1) or t.group(2), None
    if u.startswith('CAPACITY CHECK'):
        nums = [int(x) for x in re.findall(r'(\d+) ?A', u)]
        ok = ('PASS' in u) or ('RESULT OK' in u)
        return 'CAPACITY', None, (nums, ok)
    t = re.search(r'^SET GROUP 2 ([A-Z0-9_\-]+)|^ALTERNATE SETTINGS GROUP ACTIVATED: ([A-Z0-9_\-]+)', u)
    if t:
        return 'GROUP2', t.group(1) or t.group(2), None
    t = re.search(r'^CLOSE ([A-Z0-9_\-]+): CONFIRMED|^TIE ([A-Z0-9_\-]+) CLOSED', u)
    if t:
        return 'TIE CLOSED', t.group(1) or t.group(2), None
    t = re.search(r'RESTORATION COMPLETE[:;] (?:CUSTOMERS RESTORED=)?(\d+)', u)
    if t:
        return 'COMPLETE', None, int(t.group(1))
    if u.startswith('RESTORATION BLOCKED'):
        return 'BLOCKED', None, None
    if 'TRIPPED ON' in u:
        t = re.search(r'DEVICE ([A-Z0-9_\-]+) TRIPPED', u)
        return 'RECV TRIP', t.group(1) if t else None, None
    if 'ONTO FAULT' in u:
        return 'RECLOSE ONTO FAULT', None, None
    if 'ABORT' in u:
        return 'ABORTED', None, None
    if u.startswith('NO RESTORATION AVAILABLE'):
        return 'END SECTION', None, None
    if u.startswith('UPSTREAM'):
        return 'UPSTREAM', None, None
    t = re.search(r'SCHEME DISARMED: ([A-Z0-9_\-]+) COMM FAIL|COMMUNICATION LOST WITH ([A-Z0-9_\-]+)', u)
    if t:
        return 'DISARM COMM', t.group(1) or t.group(2), None
    t = re.search(r'SCHEME ARMED: ([A-Z0-9_\-]+) COMM OK|COMMUNICATION RESTORED WITH ([A-Z0-9_\-]+)', u)
    if t:
        return 'ARM COMM', t.group(1) or t.group(2), None
    if 'LOOP ABNORMAL' in u or 'NOT IN NORMAL CONFIGURATION' in u:
        return 'DISARM ABNORMAL', None, None
    if 'LOOP NORMAL' in u or 'RETURNED TO NORMAL' in u:
        return 'ARM NORMAL', None, None
    return 'OTHER', None, None
