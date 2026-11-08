"""task2 architecture 4: the Stage 5 drilling plan as the geology office prints it: collars by programme on the mine
grid, the Stage 5 crest and floor outlines."""
from PIL import Image, ImageDraw, ImageFont

import params as P

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def draw(path, holes, ids):
    W, H = 1500, 1700
    img = Image.new("RGB", (W, H), (252, 251, 247))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 18)
    fs = ImageFont.truetype(FONT, 14)
    fb = ImageFont.truetype(FONTB, 24)
    sc = 3.2
    ox, oy = 150, 1520

    def px(e, n):
        return ox + (e - 990) * sc, oy - (n - 1990) * sc
    d.rectangle([px(990, 2410)[0], px(990, 2410)[1], px(1310, 1990)[0], px(1310, 1990)[1]], outline=(60, 60, 60), width=2)
    for e in range(1000, 1301, 50):
        x, _ = px(e, 1990)
        d.line([(x, oy), (x, oy + 8)], fill=(60, 60, 60))
        d.text((x - 20, oy + 12), "%dE" % e, font=fs, fill=(60, 60, 60))
    for n in range(2000, 2401, 50):
        _, y = px(990, n)
        d.line([(ox - 8, y), (ox, y)], fill=(60, 60, 60))
        d.text((ox - 70, y - 8), "%dN" % n, font=fs, fill=(60, 60, 60))
    e0, e1, n0, n1 = P.S5_TOP
    s = P.S5_STEP * (P.S5_FLITCHES - 1)
    for (a, b, c, dd), col, lab in (((e0, e1, n0, n1), (180, 40, 40), "Stage 5 crest (RL 400)"),
                                    ((e0 + s, e1 - s, n0 + s, n1 - s), (40, 90, 170), "Stage 5 floor (RL 305)")):
        p0, p1 = px(a, dd), px(b, c)
        d.rectangle([p0[0], p0[1], p1[0], p1[1]], outline=col, width=3)
    for h, hid in zip(holes, ids):
        x, y = px(P.GRID_E0 + h["x"], P.GRID_N0 + h["y"])
        if h["campaign"] <= 2021:
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(30, 30, 30), width=2)
        elif h["type"] == "DD":
            d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(200, 110, 20))
        else:
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(30, 120, 60))
    d.text((150, 30), "MOUNT CARROW: STAGE 5 DRILLING", font=fb, fill=(20, 20, 20))
    d.text((150, 62), "Mine grid, 1:1,000 at A3. Vertical holes, collars only. Geology office, October 2026.", font=f,
           fill=(60, 60, 60))
    lx, ly = 1180, 120
    d.ellipse([lx, ly, lx + 10, ly + 10], outline=(30, 30, 30), width=2)
    d.text((lx + 18, ly - 4), "RC 2019 to 2021", font=fs, fill=(20, 20, 20))
    d.ellipse([lx, ly + 28, lx + 10, ly + 38], fill=(30, 120, 60))
    d.text((lx + 18, ly + 24), "RC 2022 to 2024", font=fs, fill=(20, 20, 20))
    d.rectangle([lx, ly + 56, lx + 10, ly + 66], fill=(200, 110, 20))
    d.text((lx + 18, ly + 52), "Diamond 2022 to 2024", font=fs, fill=(20, 20, 20))
    d.line([(lx, ly + 90), (lx + 24, ly + 90)], fill=(180, 40, 40), width=3)
    d.text((lx + 30, ly + 82), "Stage 5 crest", font=fs, fill=(20, 20, 20))
    d.line([(lx, ly + 114), (lx + 24, ly + 114)], fill=(40, 90, 170), width=3)
    d.text((lx + 30, ly + 106), "Stage 5 floor", font=fs, fill=(20, 20, 20))
    img.save(path, format="PNG")
