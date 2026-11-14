"""The cooperative's 69 kV system: twelve breakered stations on the Texas coastal bend (two 138/69 kV bulk stations fed
by the generation and transmission cooperative, ten switching or distribution stations), sixteen lines, the load taps
along them (the distribution substations, their members and how each is backed up), every structure and span with its
coordinates, insulators and the distance to the Gulf shore, the line-out source impedances behind each line terminal
(Inland's ground source changed when its 150 MVA autotransformer replaced the 75 MVA unit on 14 March 2024), the solar
farm tapped on Shell Ridge-Ponder Creek and its grounded-wye step-up, and the relay at each terminal."""
import cmath
import math

import numpy as np

import common as C

# conductor sequence impedances (ohm per km) and the thermal data the heat balance needs
CONDUCTORS = {
    '477 ACSR Hawk': dict(z1=complex(0.1195, 0.3890), z0=complex(0.4010, 1.2480), r25=0.1196, r75=0.1430,
                          d_mm=21.8, rating_a=659),
    '795 ACSR Drake': dict(z1=complex(0.0727, 0.3730), z0=complex(0.3540, 1.2100), r25=0.0727, r75=0.0869,
                           d_mm=28.1, rating_a=907),
    '336.4 ACSR Linnet': dict(z1=complex(0.1700, 0.3980), z0=complex(0.4510, 1.2710), r25=0.1702, r75=0.2035,
                              d_mm=18.3, rating_a=529),
}

# stations: code, name, kind, (x, y) km, relay family ('ER' EventRecall, 'GV' GridVue, 'EM' electromechanical)
STATIONS = [
    ('BAY', 'Bayside', 'bulk', (62.0, 14.0), 'ER'),
    ('INL', 'Inland', 'bulk', (16.0, 54.0), 'ER'),
    ('PAL', 'Port Alcorn', 'switching', (76.0, 27.0), 'GV'),
    ('SHR', 'Shell Ridge', 'switching', (88.0, 43.0), 'GV'),
    ('SED', 'Sedge Point', 'switching', (97.0, 60.0), 'GV'),
    ('RFP', 'Redfish Pass', 'switching', (55.0, 6.0), 'ER'),
    ('TUL', 'Tule Marsh', 'switching', (68.0, 31.0), 'ER'),
    ('CAN', 'Caney Bend', 'switching', (60.0, 41.0), 'GV'),
    ('PND', 'Ponder Creek', 'switching', (66.0, 62.0), 'EM'),
    ('LOK', 'Live Oak Crossing', 'switching', (40.0, 22.0), 'ER'),
    ('MSQ', 'Mesquite Flat', 'switching', (36.0, 44.0), 'ER'),
    ('GRG', 'Granger Gap', 'switching', (18.0, 28.0), 'GV'),
]
ST = {s[0]: dict(code=s[0], name=s[1], kind=s[2], xy=s[3], relay=s[4]) for s in STATIONS}

# lines: id, A, B, conductor, route factor, construction year, insulator default, kink (km of lateral bow)
LINES = [
    ('L01', 'BAY', 'PAL', '795 ACSR Drake', 1.12, 1987, 'porcelain', 0.8),
    ('L02', 'PAL', 'SHR', '795 ACSR Drake', 1.12, 1984, 'porcelain', -0.9),
    ('L03', 'SHR', 'SED', '477 ACSR Hawk', 1.12, 1981, 'porcelain', 1.1),
    ('L04', 'BAY', 'RFP', '477 ACSR Hawk', 1.13, 1990, 'porcelain', -0.6),
    ('L05', 'RFP', 'LOK', '477 ACSR Hawk', 1.11, 1993, 'porcelain', 1.4),
    ('L06', 'BAY', 'TUL', '795 ACSR Drake', 1.12, 1996, 'porcelain', -1.2),
    ('L07', 'TUL', 'CAN', '477 ACSR Hawk', 1.12, 1979, 'porcelain', 0.7),
    ('L08', 'CAN', 'PND', '477 ACSR Hawk', 1.12, 1983, 'porcelain', -1.5),
    ('L09', 'SHR', 'PND', '477 ACSR Hawk', 1.12, 1985, 'porcelain', 1.8),
    ('L10', 'INL', 'MSQ', '795 ACSR Drake', 1.12, 1998, 'porcelain', -1.0),
    ('L11', 'INL', 'GRG', '477 ACSR Hawk', 1.12, 1992, 'porcelain', 1.2),
    ('L12', 'CAN', 'MSQ', '477 ACSR Hawk', 1.12, 1989, 'porcelain', -1.3),
    ('L13', 'GRG', 'LOK', '336.4 ACSR Linnet', 1.12, 1976, 'porcelain', 0.9),
    ('L14', 'LOK', 'CAN', '477 ACSR Hawk', 1.12, 1991, 'porcelain', -0.8),
    ('L15', 'MSQ', 'LOK', '477 ACSR Hawk', 1.12, 1994, 'porcelain', 1.0),
    ('L16', 'PAL', 'TUL', '477 ACSR Hawk', 1.13, 2001, 'polymer', 0.4),
]
LINE_NAMES = {lid: '%s-%s' % (ST[a]['name'], ST[b]['name']) for lid, a, b, *_ in LINES}

# line-out source impedances behind each terminal (ohm, |Z| and angle), from the protection studies' network model
# (z1 mag, z1 ang, z0 mag, z0 ang); Inland's ground source before and after 14 March 2024
SOURCES = {
    ('L01', 'BAY'): (2.6, 84.0, 1.9, 81.0), ('L01', 'PAL'): (7.8, 81.5, 13.4, 77.0),
    ('L02', 'PAL'): (7.1, 81.0, 12.1, 76.5), ('L02', 'SHR'): (10.6, 80.0, 21.8, 75.5),
    ('L03', 'SHR'): (9.9, 80.0, 19.6, 75.0), ('L03', 'SED'): (17.4, 78.5, 38.5, 73.5),
    ('L04', 'BAY'): (2.5, 84.0, 1.8, 81.0), ('L04', 'RFP'): (11.2, 80.0, 24.7, 75.0),
    ('L05', 'RFP'): (12.9, 79.5, 28.3, 74.5), ('L05', 'LOK'): (8.9, 80.5, 15.6, 76.0),
    ('L06', 'BAY'): (2.6, 84.0, 1.9, 81.0), ('L06', 'TUL'): (8.4, 81.0, 14.9, 76.5),
    ('L07', 'TUL'): (6.9, 81.0, 11.2, 77.0), ('L07', 'CAN'): (9.4, 80.5, 17.8, 76.0),
    ('L08', 'CAN'): (8.7, 80.5, 15.9, 76.0), ('L08', 'PND'): (14.8, 79.0, 31.6, 74.0),
    ('L09', 'SHR'): (10.1, 80.0, 20.4, 75.5), ('L09', 'PND'): (14.2, 79.0, 29.8, 74.0),
    ('L10', 'INL'): (3.1, 84.5, None, 80.5), ('L10', 'MSQ'): (8.2, 81.0, 14.6, 76.5),
    ('L11', 'INL'): (3.2, 84.5, None, 80.5), ('L11', 'GRG'): (11.8, 79.5, 26.2, 75.0),
    ('L12', 'CAN'): (9.0, 80.5, 16.8, 76.0), ('L12', 'MSQ'): (8.6, 81.0, 15.2, 76.5),
    ('L13', 'GRG'): (12.4, 79.5, 27.5, 75.0), ('L13', 'LOK'): (9.6, 80.0, 18.2, 75.5),
    ('L14', 'LOK'): (9.2, 80.5, 17.4, 76.0), ('L14', 'CAN'): (9.8, 80.0, 18.9, 75.5),
    ('L15', 'MSQ'): (8.8, 81.0, 15.8, 76.5), ('L15', 'LOK'): (9.4, 80.5, 17.9, 76.0),
    ('L16', 'PAL'): (6.8, 81.0, 11.0, 77.0), ('L16', 'TUL'): (7.2, 81.0, 11.9, 77.0),
}
INL_Z0 = {'old': 9.8, 'new': 3.6}            # Inland's ground source, 75 MVA (to 14 Mar 2024) and 150 MVA units

# lines rebuilt with their structures renumbered: date, and former number less new number
import datetime as _dt
REBUILT = {'L13': (_dt.date(2023, 4, 18), 9), 'L08': (_dt.date(2023, 9, 26), -6)}

# stretches of line carrying the cooperative's 12.47 kV distribution circuits built under the 69 kV on the same poles
# (structure no. from, to)
UNDERBUILT = {'L01': (20, 35), 'L02': (28, 40), 'L06': (41, 76), 'L10': (30, 44), 'L12': (38, 50), 'L14': (58, 72),
              'L15': (45, 55), 'L16': (1, 999)}

# the solar farm: tap on L09 at km TAP_KM from Shell Ridge, a 1.6 km tap line to the farm's 69/34.5 kV step-up
TAP_LINE = 'L09'
TAP_KM = 23.4
TAP_LEN = 1.6
GSU = dict(mva=66.0, z_pct=9.2, xr=28.0, winding='YNd1', ngr_ohm=10.0)   # grounded-wye on the 69 kV side through a
                                                                         # 10 ohm neutral reactor: a zero-sequence source
INV_I_PU = 1.1                                              # the inverters' fault current, per unit of rated

# the Gulf shoreline (a polyline, km) and the bay's open water (a circle)
SHORE = [(52.0, 0.0), (75.0, 22.0), (92.0, 45.0), (104.0, 70.0)]
BAY_CENTRE, BAY_R = (66.0, 36.5), 4.2

# load taps: name, line, km from terminal A, members (2026), feeders, backup ('auto' alternate source with automatic
# throw-over, 'manual' alternate closed by the control room, 'none' radial), the alternate line, a motor-operated
# sectionalizing switch pair on SCADA (True) or crew-operated (False)
TAPS = [
    ('Beachwood', 'L01', 6.8, 4180, 4, 'auto', 'L04', True),
    ('Costa Verde', 'L01', 15.1, 3620, 3, 'none', None, True),
    ('Palmetto Shores', 'L02', 7.4, 5240, 5, 'manual', 'L16', True),
    ('Gull Harbor', 'L02', 16.2, 2870, 3, 'none', None, False),
    ('Dune Road', 'L03', 9.8, 2310, 3, 'none', None, False),
    ('Sedge Village', 'L03', 17.6, 1960, 2, 'manual', 'L09', False),
    ('Redfish Flats', 'L04', 5.3, 2740, 3, 'auto', 'L01', True),
    ('Saltgrass', 'L05', 8.9, 3150, 3, 'none', None, False),
    ('Coloma', 'L05', 17.7, 2480, 3, 'manual', 'L14', True),
    ('Heron Bend', 'L06', 9.7, 3890, 4, 'auto', 'L16', True),
    ('Tule Point', 'L07', 6.1, 1640, 2, 'none', None, False),
    ('Caney Mill', 'L08', 11.3, 2950, 3, 'manual', 'L14', False),
    ('Ponder Lake', 'L08', 19.8, 2230, 3, 'none', None, False),
    ('Oyster Ridge', 'L09', 8.7, 3370, 3, 'auto', 'L03', True),
    ('Coyote Draw', 'L09', 27.9, 1180, 2, 'none', None, False),
    ('Mesquite North', 'L10', 7.6, 4410, 4, 'manual', 'L15', True),
    ('Inland Crossroads', 'L10', 16.9, 3060, 3, 'none', None, True),
    ('Granger Ranch', 'L11', 12.3, 2580, 3, 'none', None, False),
    ('Bluestem', 'L11', 21.8, 1890, 2, 'manual', 'L13', False),
    ('Caney West', 'L12', 9.1, 3320, 3, 'auto', 'L14', True),
    ('Sandhill', 'L12', 18.4, 2470, 3, 'none', None, False),
    ('Granger Wells', 'L13', 11.6, 1720, 2, 'none', None, False),
    ('Live Oak East', 'L14', 13.4, 4020, 4, 'auto', 'L05', True),
    ('Mesquite South', 'L15', 10.2, 3560, 3, 'manual', 'L12', True),
    ('Loma Alta', 'L15', 18.8, 2310, 3, 'none', None, False),
]


def _shore_dist(x, y):
    best = 1e9
    for (x0, y0), (x1, y1) in zip(SHORE[:-1], SHORE[1:]):
        dx, dy = x1 - x0, y1 - y0
        t = max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
        px, py = x0 + t * dx, y0 + t * dy
        best = min(best, math.hypot(x - px, y - py))
    return best


def _bay_dist(x, y):
    return max(0.0, math.hypot(x - BAY_CENTRE[0], y - BAY_CENTRE[1]) - BAY_R)


def _zpol(mag, ang):
    return cmath.rect(mag, math.radians(ang))


def source(line, end, when=None):
    """the line-out source behind a terminal on a date: (Z1, Z0) complex ohms"""
    m1, a1, m0, a0 = SOURCES[(line, end)]
    if m0 is None:   # Inland
        m0 = INL_Z0['old'] if (when is not None and when < C.INLAND_NEW_AUTO) else INL_Z0['new']
    return _zpol(m1, a1), _zpol(m0, a0)


def gsu_z(seq=0):
    """the solar farm step-up's impedance seen from 69 kV (ohm); the zero sequence adds three times the neutral reactor"""
    zb = 69.0 ** 2 / GSU['mva']
    z = cmath.rect(GSU['z_pct'] / 100.0 * zb, math.atan(GSU['xr']))
    return z + (3j * GSU['ngr_ohm'] if seq == 0 else 0)


def build(rng=None):
    rng = rng or np.random.default_rng(C.SEED)
    net = dict(stations=ST, lines={}, taps=[], structures=[], spans={})
    for lid, a, b, cond, rf, year, ins, kink in LINES:
        xa, ya = ST[a]['xy']
        xb, yb = ST[b]['xy']
        straight = math.hypot(xb - xa, yb - ya)
        length = round(straight * rf + rng.normal(0, 0.15), 2)
        cd = CONDUCTORS[cond]
        # structures: spans of 150 to 245 m, the line bowing sideways by `kink` km at its middle
        n_target = length / 0.198
        spans = rng.uniform(0.150, 0.245, int(n_target * 1.4))
        cum = np.concatenate([[0.0], np.cumsum(spans)])
        cum = cum[cum < length - 0.10]
        cum = np.append(cum, length)
        nx, ny = -(yb - ya) / straight, (xb - xa) / straight
        line = dict(id=lid, a=a, b=b, name=LINE_NAMES[lid], conductor=cond, length=length, year=year,
                    z1=cd['z1'], z0=cd['z0'], structures=[])
        for i, km in enumerate(cum):
            f = km / length
            bow = kink * math.sin(math.pi * f)
            x = xa + (xb - xa) * f + nx * bow + rng.normal(0, 0.02)
            y = ya + (yb - ya) * f + ny * bow + rng.normal(0, 0.02)
            sd = _shore_dist(x, y)
            st = dict(line=lid, no=i + 1, km=round(float(km), 3), x=x, y=y, shore_km=sd, bay_km=_bay_dist(x, y),
                      insulator=ins, ins_year=year, kind=('steel pole' if lid in ('L06', 'L16') else
                                                           'wood H-frame' if cond != '336.4 ACSR Linnet' else
                                                           'wood single pole'))
            line['structures'].append(st)
        net['lines'][lid] = line
    # polymer upgrades (insulators replaced after older flashover programmes): parts of L04 and L05, all of L16
    for lid, k0, k1, yr in (('L04', 6.0, 11.9, 2015), ('L05', 0.0, 6.5, 2015), ('L01', 17.5, 21.6, 2019)):
        for st in net['lines'][lid]['structures']:
            if k0 <= st['km'] <= k1:
                st['insulator'], st['ins_year'] = 'polymer', yr
    for lid, line in net['lines'].items():
        a, b = UNDERBUILT.get(lid, (0, -1))
        for st in line['structures']:
            st['underbuild'] = '12.47 kV' if a <= st['no'] <= b else ''
    for name, lid, km, members, feeders, backup, alt, moab in TAPS:
        net['taps'].append(dict(name=name, line=lid, km=km, members=members, feeders=feeders, backup=backup, alt=alt,
                                moab=moab))
    for lid, line in net['lines'].items():
        for st in line['structures']:
            net['structures'].append(st)
    return net


def structure_at(net, lid, km):
    """the structure nearest a distance along the line"""
    sts = net['lines'][lid]['structures']
    kms = np.array([s['km'] for s in sts])
    return sts[int(np.argmin(np.abs(kms - km)))]


def span_at(net, lid, km):
    """the span (back structure, ahead structure) holding a distance"""
    sts = net['lines'][lid]['structures']
    for s0, s1 in zip(sts[:-1], sts[1:]):
        if s0['km'] <= km <= s1['km']:
            return s0, s1
    return sts[-2], sts[-1]
