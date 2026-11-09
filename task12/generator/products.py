"""The plant-based beverage category as the panel's product master holds it: brands, own labels, SKUs with their
13-digit codes, pack sizes and everyday shelf prices. Brand families map to the world's preference columns
(world.BRANDS order: Prairie Grove, Silverbrook, Coastline, Wildflax, Haven & Hollow, Little Ferns, own label)."""
import numpy as np

import world as W


def ean13(body12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(body12))
    return body12 + str((10 - s % 10) % 10)


# manufacturer prefixes (UPC-A company prefixes written as 13-digit codes with a leading zero)
MFR = {'Prairie Grove': '06287341', 'Silverbrook': '05589210', 'Coastline': '06801137', 'Wildflax': '06279054',
       'Haven & Hollow': '08583302', 'Little Ferns': '06289166', 'Northvale Oat': '06287702'}
OWN_LABEL = {'FMF': ('Foxmere Kitchen', '06904211'), 'GLM': ('Greenleaf Organics', '06290417'),
             'LYG': ('LG Everyday', '06038827'), 'NGF': ('Northglen Basics', '06228840'),
             'MBV': ('Belvoir', '06244973'), 'VLW': ('ValuWay', '06213378'), 'TBK': ('TB Smart', '06261920'),
             'CWC': ('Costwell Choice', '09661900')}

# (brand, family index, description, segment, pack litres, units in pack, everyday price CAD, organic, first year)
SKUS = [
    ('Prairie Grove', 0, 'Oat Original', 'Oat', 1.75, 1, 4.49, 'N', 2019),
    ('Prairie Grove', 0, 'Oat Unsweetened', 'Oat', 1.75, 1, 4.49, 'N', 2019),
    ('Prairie Grove', 0, 'Oat Chocolate', 'Oat', 0.946, 1, 3.29, 'N', 2021),
    ('Silverbrook', 1, 'Almond Original', 'Almond', 1.89, 1, 4.29, 'N', 2016),
    ('Silverbrook', 1, 'Almond Unsweetened Vanilla', 'Almond', 1.89, 1, 4.29, 'N', 2016),
    ('Silverbrook', 1, 'Soy Original', 'Soy', 1.89, 1, 3.99, 'N', 2014),
    ('Coastline', 2, 'Coconut Original', 'Coconut', 1.89, 1, 4.79, 'N', 2018),
    ('Coastline', 2, 'Coconut Unsweetened', 'Coconut', 1.89, 1, 4.79, 'N', 2018),
    ('Wildflax', 3, 'Organic Oat', 'Oat', 1.75, 1, 6.29, 'Y', 2020),
    ('Wildflax', 3, 'Organic Hemp & Oat', 'Blend', 0.946, 1, 4.29, 'Y', 2022),
    ('Haven & Hollow', 4, 'Barista Oat', 'Oat', 0.946, 1, 4.79, 'N', 2021),
    ('Haven & Hollow', 4, 'Barista Almond', 'Almond', 0.946, 1, 4.79, 'N', 2022),
    ('Little Ferns', 5, 'Pea Protein Original', 'Pea', 1.5, 1, 5.99, 'N', 2023),
    ('Little Ferns', 5, 'Oat & Pea Unsweetened', 'Blend', 1.5, 1, 5.99, 'N', 2024),
]
OWN_LABEL_SKUS = [('Oat Original', 'Oat', 1.89, 1, 3.29), ('Almond Original', 'Almond', 1.89, 1, 3.29),
                  ('Oat Unsweetened', 'Oat', 1.89, 1, 3.29)]
CLUB_SKUS = [('Oat Original 6 x 946 mL', 'Oat', 0.946, 6, 12.99), ('Almond Original 6 x 946 mL', 'Almond', 0.946, 6, 12.99)]
NORTHVALE = [('Oat Original', 'Oat', 1.75, 1, 5.79), ('Oat Unsweetened', 'Oat', 1.75, 1, 5.79),
             ('Barista Oat', 'Oat', 0.946, 1, 4.49)]
BANNER_PRICE = {'FMF': 1.06, 'GLM': 1.08, 'LYG': 1.00, 'NGF': 0.99, 'MBV': 1.01, 'VLW': 0.92, 'TBK': 0.91, 'CWC': 0.88}


def master():
    """Every SKU as a dict: ean, brand, description, manufacturer, own_label_banner, segment, pack litres, units,
    price, organic, first year; and the family index the world's preferences use (-1 own label, -2 Northvale)."""
    out = []
    item = {}

    def code(prefix, k):
        return ean13(prefix + '%04d' % k)
    for b, fam, desc, seg, L, u, p, org, yr in SKUS:
        item[b] = item.get(b, 120) + 37
        out.append(dict(ean=code(MFR[b], item[b]), brand=b, description=desc, manufacturer=b + ' Foods' if b != 'Haven & Hollow' else 'Haven & Hollow Beverage Co.',
                        own_label_banner='', segment=seg, litres=L, units=u, price=p, organic=org, first_year=yr, family=fam))
    for bc, (lab, pre) in OWN_LABEL.items():
        if bc == 'CWC':
            skus = CLUB_SKUS
        elif bc == 'GLM':
            skus = [('Organic Oat', 'Oat', 0.946, 1, 3.49), ('Organic Almond', 'Almond', 0.946, 1, 3.49)]
        else:
            skus = OWN_LABEL_SKUS
        for k, (desc, seg, L, u, p) in enumerate(skus):
            out.append(dict(ean=code(pre, 410 + 23 * k), brand=lab, description=desc, manufacturer='', own_label_banner=bc,
                            segment=seg, litres=L, units=u, price=p, organic='Y' if 'Organic' in desc else 'N',
                            first_year=2017 + k, family=-1))
    for k, (desc, seg, L, u, p) in enumerate(NORTHVALE):
        out.append(dict(ean=code(MFR['Northvale Oat'], 1001 + 14 * k), brand='Northvale Oat', description=desc,
                        manufacturer='Northvale Oat Co.', own_label_banner='', segment=seg, litres=L, units=u, price=p,
                        organic='N', first_year=2026, family=-2))
    return out


def index(m):
    """Lookups the pack writer needs: SKUs by family, own-label SKUs by banner, Northvale SKUs."""
    fam = {f: [s for s in m if s['family'] == f] for f in range(6)}
    own = {bc: [s for s in m if s['own_label_banner'] == bc] for bc in OWN_LABEL}
    nv = [s for s in m if s['family'] == -2]
    return fam, own, nv
