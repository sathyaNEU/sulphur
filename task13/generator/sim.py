"""The simulated world in one pass: the network, the weather, the loading, the crews' washing, every fault, and (in
relays.py and ops.py) what each instrument and system recorded. world() caches the result outside the task folder."""
import os
import pickle
import tempfile

import common as C
import faults as F
import field as FD
import loads as L
import network as N
import weather as W

CACHE = os.path.join(tempfile.gettempdir(), 'task13_v5_world_cache')
SIM_FILES = ('common', 'network', 'weather', 'loads', 'faults', 'field', 'relays', 'ops', 'sim')
CRIT = 0.052          # the deposit (mg per cm2 ESDD) past which the Gulf lines' porcelain flashes over in fog


def simulate():
    net = N.build()
    wx = W.simulate()
    W.index_fog(wx)
    W.apply_fog_to_series(wx)
    ld = L.simulate(net, wx)
    secs, washes = FD.washing_schedule(net, wx)
    washes = [w for w in washes if w['date'].year < 2026]
    plan = FD.plan_2026(net, wx, secs, washes, CRIT)
    washes = sorted(washes + plan, key=lambda w: (w['date'], w['section']))
    fl = F.simulate(net, wx, ld, washes)
    tests, test_series = FD.test_readings(wx)
    w = dict(net=net, wx=wx, ld=ld, sections=secs, washes=washes, faults=fl['faults'], deposits=fl['deposits'],
             replaced=fl['replaced'], trims=fl['trims'], strings=fl['strings'], tests=tests, test_series=test_series)
    import relays as R
    import ops as O
    R.record(w)
    O.operate(w)
    return w


def world(refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, 'world.pkl')
    src = max(os.path.getmtime(os.path.join(C.HERE, f + '.py')) for f in SIM_FILES if os.path.exists(os.path.join(C.HERE, f + '.py')))
    if not refresh and os.path.exists(p) and os.path.getmtime(p) > src:
        return pickle.load(open(p, 'rb'))
    w = simulate()
    pickle.dump(w, open(p, 'wb'))
    return w
