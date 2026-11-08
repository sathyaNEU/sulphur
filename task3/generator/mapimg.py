"""task3 architecture 3: Plate 3 of the District's 2019 bedrock surface study, the Harlow reach, as a scanned
plate: bedrock surface contours, the mapped edge of the saturated sand and gravel, and the wells."""
import math

from PIL import Image, ImageDraw, ImageFont

import params as P
import world as W

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
WPX, HPX = 1800, 1350
MAPBOX = (40, 90, 1390, 1290)       # pixel frame of the map
A_RANGE = (-3200.0, 13200.0)
C_RANGE = (-4700.0, 4700.0)


def _frame():
    """State plane window holding the reach, north up."""
    pts = [W.xy((a, c)) for a in A_RANGE for c in C_RANGE]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    span_x = (max(xs) - min(xs)) * 0.86
    w_px, h_px = MAPBOX[2] - MAPBOX[0], MAPBOX[3] - MAPBOX[1]
    scale = w_px / span_x
    span_y = h_px / scale
    return cx - span_x / 2, cy + span_y / 2, scale


def _px(x, y, fr):
    x0, y0, s = fr
    return (MAPBOX[0] + (x - x0) * s, MAPBOX[1] + (y0 - y) * s)


def _bedrock(c):
    """Bedrock surface elevation (ft) across the valley: a flat floor, a wall rising from the sand and gravel's
    edge, the upland beyond."""
    ac = abs(c)
    if ac <= 1600:
        return 612 + 6 * (ac / 1600.0) ** 2
    if ac <= 2500:
        return 618 + 22 * ((ac - 1600) / 900.0) ** 1.6
    return min(752, 640 + 48 * ((ac - 2500) / 700.0))


def draw(path):
    img = Image.new("RGB", (WPX, HPX), (250, 249, 244))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 17)
    fs = ImageFont.truetype(FONT, 14)
    fb = ImageFont.truetype(FONTB, 22)
    fr = _frame()
    d.rectangle(MAPBOX, outline=(40, 40, 40), width=2)
    # saturated sand and gravel, shaded between the mapped edges
    poly = [_px(*W.xy((a, -P.WIDTH / 2)), fr) for a in (A_RANGE[0] - 3000, A_RANGE[1] + 3000)]
    poly += [_px(*W.xy((a, P.WIDTH / 2)), fr) for a in (A_RANGE[1] + 3000, A_RANGE[0] - 3000)]
    shade = Image.new("RGB", (WPX, HPX), (250, 249, 244))
    ImageDraw.Draw(shade).polygon(poly, fill=(226, 236, 214))
    mask = Image.new("L", (WPX, HPX), 0)
    ImageDraw.Draw(mask).rectangle(MAPBOX, fill=255)
    img.paste(shade, (0, 0), mask)
    d = ImageDraw.Draw(img)
    # bedrock contours every 20 ft, each a line parallel to the valley axis
    for elev in range(620, 760, 20):
        for side in (-1, 1):
            # invert the cross profile for this elevation
            lo, hi = 0.0, 6000.0
            for _ in range(50):
                mid = (lo + hi) / 2
                if _bedrock(mid) < elev:
                    lo = mid
                else:
                    hi = mid
            c = side * lo
            if abs(c) > C_RANGE[1] + 2000:
                continue
            p0 = _px(*W.xy((A_RANGE[0] - 3000, c)), fr)
            p1 = _px(*W.xy((A_RANGE[1] + 3000, c)), fr)
            d.line([p0, p1], fill=(150, 112, 70), width=2 if elev % 100 == 0 else 1)
            lab = _px(*W.xy((A_RANGE[0] + 3600 + 700 * (elev % 60) / 20 + (5200 if side > 0 else 0), c)), fr)
            if MAPBOX[0] + 20 < lab[0] < MAPBOX[2] - 60 and MAPBOX[1] + 20 < lab[1] < MAPBOX[3] - 20:
                d.rectangle([lab[0] - 2, lab[1] - 9, lab[0] + 34, lab[1] + 9], fill=(250, 249, 244))
                d.text((lab[0], lab[1] - 8), str(elev), font=fs, fill=(130, 92, 50))
    # mapped edge of the saturated sand and gravel
    for side in (-1, 1):
        a = A_RANGE[0] - 3000
        while a < A_RANGE[1] + 3000:
            p0 = _px(*W.xy((a, side * P.WIDTH / 2)), fr)
            p1 = _px(*W.xy((a + 260, side * P.WIDTH / 2)), fr)
            d.line([p0, p1], fill=(40, 90, 40), width=3)
            a += 420
    # the frame cuts off whatever drew outside it
    d.rectangle([0, 0, WPX, MAPBOX[1] - 1], fill=(250, 249, 244))
    d.rectangle([0, MAPBOX[3] + 1, WPX, HPX], fill=(250, 249, 244))
    d.rectangle([0, 0, MAPBOX[0] - 1, HPX], fill=(250, 249, 244))
    d.rectangle([MAPBOX[2] + 1, 0, WPX, HPX], fill=(250, 249, 244))
    d.rectangle(MAPBOX, outline=(40, 40, 40), width=2)
    # wells
    marks = {"TW-1": "s", "TW-2": "s", "PW-1": "s", "PW-2": "s", "MS-MW": "o", "OW-1": "o", "OW-2": "o",
             "OW-3": "o", "OW-S": "t", "CV-07": "t", "CV-04": "t"}
    for w, kind in marks.items():
        x, y = _px(*W.xy(P.WELLS[w]), fr)
        if kind == "s":
            d.rectangle([x - 6, y - 6, x + 6, y + 6], fill=(20, 60, 160))
        elif kind == "o":
            d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(20, 20, 20), width=2)
        else:
            d.polygon([(x, y - 8), (x - 7, y + 6), (x + 7, y + 6)], fill=(170, 30, 30))
        dx = {"TW-2": 10, "PW-2": 10, "OW-1": 8, "OW-2": -64, "MS-MW": -70, "TW-1": -54, "PW-1": -54}.get(w, 10)
        dy = {"TW-2": -20, "PW-2": 2, "OW-1": -24, "MS-MW": 2, "TW-1": 2, "PW-1": 2}.get(w, -8)
        d.text((x + dx, y + dy), w, font=f, fill=(20, 20, 20))
    # off-plate wells
    d.text((MAPBOX[0] + 110, MAPBOX[3] - 30), "CV-02 (4.9 mi S, valley axis), CV-05, CV-09, CV-13 off plate: see register",
           font=fs, fill=(60, 60, 60))
    d.text((MAPBOX[0] + 110, MAPBOX[1] + 14), "CV-11 (5.8 mi N, valley axis) off plate", font=fs, fill=(60, 60, 60))
    # grid ticks in state plane feet
    x0, y0, s = fr
    for gx in range(int(x0 // 2000 + 1) * 2000, int((x0 + (MAPBOX[2] - MAPBOX[0]) / s)), 2000):
        px = MAPBOX[0] + (gx - x0) * s
        d.line([(px, MAPBOX[3]), (px, MAPBOX[3] + 8)], fill=(40, 40, 40), width=1)
        d.text((px - 30, MAPBOX[3] + 10), "{:,}".format(gx), font=fs, fill=(40, 40, 40))
    for gy in range(int((y0 - (MAPBOX[3] - MAPBOX[1]) / s) // 2000 + 1) * 2000, int(y0), 2000):
        py = MAPBOX[1] + (y0 - gy) * s
        d.line([(MAPBOX[0], py), (MAPBOX[0] + 10, py)], fill=(40, 40, 40), width=1)
        d.rectangle([MAPBOX[0] + 12, py - 9, MAPBOX[0] + 92, py + 9], fill=(250, 249, 244))
        d.text((MAPBOX[0] + 14, py - 8), "{:,}".format(gy), font=fs, fill=(40, 40, 40))
    # side panel: title, legend, scale, north arrow
    X = 1420
    d.text((X, 96), "CORRIN VALLEY WATER", font=fb, fill=(20, 20, 20))
    d.text((X, 124), "CONSERVANCY DISTRICT", font=fb, fill=(20, 20, 20))
    d.text((X, 166), "Bedrock Surface Study (2019)", font=f, fill=(20, 20, 20))
    d.text((X, 190), "Plate 3: Harlow reach", font=f, fill=(20, 20, 20))
    y = 250
    d.line([(X, y + 9), (X + 40, y + 9)], fill=(150, 112, 70), width=2)
    d.text((X + 52, y), "Bedrock surface, ft NAVD88,", font=fs, fill=(20, 20, 20))
    d.text((X + 52, y + 17), "20 ft interval", font=fs, fill=(20, 20, 20))
    y += 52
    d.line([(X, y + 9), (X + 16, y + 9)], fill=(40, 90, 40), width=3)
    d.line([(X + 24, y + 9), (X + 40, y + 9)], fill=(40, 90, 40), width=3)
    d.text((X + 52, y), "Edge of saturated sand", font=fs, fill=(20, 20, 20))
    d.text((X + 52, y + 17), "and gravel", font=fs, fill=(20, 20, 20))
    y += 52
    d.rectangle([X, y + 2, X + 40, y + 18], fill=(226, 236, 214))
    d.text((X + 52, y), "Sand and gravel under till", font=fs, fill=(20, 20, 20))
    y += 40
    d.rectangle([X + 14, y + 3, X + 26, y + 15], fill=(20, 60, 160))
    d.text((X + 52, y), "Production well", font=fs, fill=(20, 20, 20))
    y += 30
    d.ellipse([X + 15, y + 4, X + 25, y + 14], outline=(20, 20, 20), width=2)
    d.text((X + 52, y), "Observation or monitoring well", font=fs, fill=(20, 20, 20))
    y += 30
    d.polygon([(X + 20, y + 1), (X + 13, y + 15), (X + 27, y + 15)], fill=(170, 30, 30))
    d.text((X + 52, y), "District network well", font=fs, fill=(20, 20, 20))
    # scale bar
    y += 70
    L = 2000 * s
    d.rectangle([X, y, X + L / 2, y + 10], fill=(20, 20, 20))
    d.rectangle([X + L / 2, y, X + L, y + 10], outline=(20, 20, 20), width=2)
    d.text((X - 4, y + 16), "0", font=fs, fill=(20, 20, 20))
    d.text((X + L / 2 - 16, y + 16), "1,000", font=fs, fill=(20, 20, 20))
    d.text((X + L - 18, y + 16), "2,000 ft", font=fs, fill=(20, 20, 20))
    # north arrow
    y += 90
    d.polygon([(X + 40, y), (X + 28, y + 50), (X + 40, y + 40), (X + 52, y + 50)], fill=(20, 20, 20))
    d.text((X + 34, y + 56), "N", font=fb, fill=(20, 20, 20))
    y += 120
    for line in ["Indiana State Plane East, NAD83,", "US survey feet.",
                 "Bedrock surface from 212 borings", "and a 2018 seismic refraction line."]:
        d.text((X, y), line, font=fs, fill=(60, 60, 60))
        y += 19
    img.save(path, format="PNG", optimize=False)
