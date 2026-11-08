"""task3 architecture 4: Figure 3 of the 2019 wellhead protection plan, the zones of contribution (PNG)."""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def draw(path):
    W_, H_ = 2200, 1560
    im = Image.new("RGB", (W_, H_), (252, 252, 248))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 28)
    fs = ImageFont.truetype(FONT, 23)
    fb = ImageFont.truetype(FONTB, 34)
    # the ridge
    ridge = [(560, 260), (980, 220), (1180, 420), (1160, 980), (900, 1180), (600, 1060), (520, 640)]
    d.polygon(ridge, fill=(236, 226, 205))
    for k in range(-1400, 2200, 34):
        d.line([(k, 1300), (k + 1100, 200)], fill=(220, 205, 175), width=2)
    im2 = Image.new("RGB", (W_, H_), (252, 252, 248))
    mask = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(mask).polygon(ridge, fill=255)
    im2.paste(im, (0, 0), mask)
    im = im2
    d = ImageDraw.Draw(im)
    d.polygon(ridge, outline=(160, 130, 90), width=3)
    # zones of contribution
    zones = {
        "Well 7": [(300, 240), (1000, 200), (1560, 520), (1610, 690), (1150, 640), (420, 620)],
        "Well 6": [(420, 620), (1150, 640), (1610, 700), (1600, 840), (1120, 920), (460, 980)],
        "Well 5": [(1150, 200), (1900, 300), (1920, 560), (1640, 690), (1560, 520)],
        "Well 3": [(1120, 920), (1600, 850), (1700, 1240), (1300, 1380), (1050, 1220)],
    }
    cols = {"Well 3": (60, 120, 190), "Well 5": (50, 150, 100), "Well 6": (190, 100, 40), "Well 7": (140, 60, 150)}
    for k, poly in zones.items():
        d.line(poly + [poly[0]], fill=cols[k], width=5)
    # the river
    xs = [(1980 + 30 * ((i % 4) - 1.5), 120 + 90 * i) for i in range(17)]
    d.line(xs, fill=(70, 130, 200), width=9)
    d.text((2000, 760), "Cadle River", font=f, fill=(40, 90, 160))
    # wells
    wells = {"Well 7": (1600, 600), "Well 6": (1625, 760), "Well 5": (1660, 650), "Well 3": (1640, 900)}
    for k, (x, y) in wells.items():
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(20, 20, 20))
        d.text((x + 18, y - 14), k, font=fs, fill=(20, 20, 20))
    d.text((640, 700), "Sallow Ridge", font=fb, fill=(120, 90, 50))
    d.text((360, 330), "Zone of contribution, Well 7", font=fs, fill=cols["Well 7"])
    d.text((470, 900), "Zone of contribution, Well 6", font=fs, fill=cols["Well 6"])
    d.text((1300, 240), "Zone of contribution, Well 5", font=fs, fill=cols["Well 5"])
    d.text((1150, 1300), "Zone of contribution, Well 3", font=fs, fill=cols["Well 3"])
    d.line([(1380, 1060), (1480, 1060)], fill=(80, 80, 80), width=3)
    d.text((1300, 960), "Sallow Road", font=fs, fill=(80, 80, 80))
    d.line([(1200, 1000), (1900, 1000)], fill=(150, 150, 150), width=4)
    # title, north arrow, scale
    d.text((60, 40), "Figure 3. Zones of contribution, Sallow Road well field (2019)", font=fb, fill=(20, 20, 20))
    d.polygon([(2080, 1380), (2100, 1320), (2120, 1380)], fill=(20, 20, 20))
    d.text((2088, 1390), "N", font=f, fill=(20, 20, 20))
    d.line([(80, 1460), (480, 1460)], fill=(20, 20, 20), width=5)
    for x in (80, 280, 480):
        d.line([(x, 1448), (x, 1472)], fill=(20, 20, 20), width=3)
    d.text((80, 1480), "0", font=fs, fill=(20, 20, 20))
    d.text((265, 1480), "0.5", font=fs, fill=(20, 20, 20))
    d.text((440, 1480), "1 mile", font=fs, fill=(20, 20, 20))
    d.text((60, 1515), "Fenwright Hydrogeologic for Corlinden Water Utility. Parcel attributes in Appendix B.", font=fs,
           fill=(70, 70, 70))
    im.save(path, format="PNG", optimize=True)
