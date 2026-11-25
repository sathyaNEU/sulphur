"""The paging encoder's transmit log for the 2026 season (local time, one row per page transmitted, each page repeated
once a few seconds later by the encoder) and the supplier's daily cooling index."""
import datetime as dt

import numpy as np

import common as CM
import params as P


def addresses(r):
    """Each AC paging group's address on each system: the VHF tone-group code and the FLEX capcode."""
    vhf = {g: "%04d" % (3100 + 7 * g + int(r.integers(0, 3))) for g in range(16)}
    flex = {g: "%07d" % (1407000 + 13 * g + int(r.integers(0, 5))) for g in range(16)}
    return vhf, flex


def group_code(g):
    return "AC-%02d" % (g + 1)


def encoder_rows(W, S, r):
    """Shed and restore pages for every trial event, on the system or systems each group's switches listen to; the
    Monday test page; a few pre-season tests."""
    vhf_addr, flex_addr = addresses(r)
    systems = {}
    for g in range(16):
        m = W["grp"] == g
        s = []
        if W["vhf"][m].any():
            s.append("VHF")
        if (~W["vhf"][m]).any():
            s.append("FLEX")
        systems[g] = s
    out = []

    def page(t, sysn, g, cmd):
        addr = vhf_addr[g] if sysn == "VHF" else flex_addr[g]
        out.append((t, sysn, addr, group_code(g), cmd, "N"))
        out.append((t + dt.timedelta(seconds=int(r.integers(9, 17))), sysn, addr, group_code(g), cmd, "Y"))

    for e, d in enumerate(P.EVENT_DAYS):
        for k, g in enumerate(S["order"][e]):
            t0 = CM.local(d, P.FLEET_MIN0 + 10 * k, S["tx_sec"][(e, g)])
            for j, sysn in enumerate(systems[g]):
                page(t0 + dt.timedelta(seconds=j), sysn, g, "SHED")
            t1 = CM.local(d, P.RESTORE_MIN + k, S["rs_sec"][(e, g)])
            for j, sysn in enumerate(systems[g]):
                page(t1 + dt.timedelta(seconds=j), sysn, g, "RESTORE")
    # the weekly test page to the test address on both systems, Mondays at 10:15
    d = dt.date(2026, 5, 18)
    while d <= dt.date(2026, 9, 28):
        if d not in P.HOLIDAYS:
            t = dt.datetime(d.year, d.month, d.day, 10, 15, int(r.integers(0, 20)), tzinfo=P.CDT)
            out.append((t, "VHF", "3099", "TEST", "TEST", "N"))
            out.append((t + dt.timedelta(seconds=2), "FLEX", "1406999", "TEST", "TEST", "N"))
        d += dt.timedelta(7)
    # the pre-season check of each group's address on 20 and 21 May (a two-minute shed, restored at once)
    for j, g in enumerate(range(16)):
        dd = dt.date(2026, 5, 20) if g < 8 else dt.date(2026, 5, 21)
        t = dt.datetime(dd.year, dd.month, dd.day, 9, 30, 0, tzinfo=P.CDT) + dt.timedelta(minutes=4 * (g % 8), seconds=int(r.integers(0, 30)))
        for sysn in systems[g]:
            out.append((t, sysn, vhf_addr[g] if sysn == "VHF" else flex_addr[g], group_code(g), "SHED", "N"))
            out.append((t + dt.timedelta(minutes=2), sysn, vhf_addr[g] if sysn == "VHF" else flex_addr[g], group_code(g), "RESTORE", "N"))
    out.sort(key=lambda t: (t[0], t[1]))
    rows = [(t.strftime("%m/%d/%Y %H:%M:%S"), s, a, g, c, rt) for (t, s, a, g, c, rt) in out]
    return rows, dict(vhf=vhf_addr, flex=flex_addr, systems=systems)


def index_rows(S):
    rows = []
    for d in S["index_days"]:
        rows.append((CM.fmt_date(d), "%.3f" % S["index"][d]))
    return rows
