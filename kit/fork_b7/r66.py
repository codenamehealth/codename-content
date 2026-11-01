import sys; sys.path.insert(0, '../fork1')
from common import *
import numpy as np
from skimage import measure
random.seed(66)
BGS = bg_frames('recov_hd.gif', (1214, 1920), box=(624, 0, 1264, 1080), step=2, bright=0.62)
def _shift(b):
    o = Image.new('RGBA', (W, H)); c = b.crop((67, 0, 67 + W, H)); top = c.crop((0, 0, W, 4)).resize((W, 140), Image.NEAREST)
    o.alpha_composite(top, (0, 0)); o.alpha_composite(c, (0, 140)); return o
BGS = [_shift(b) for b in BGS]
# star field
STARS = [(random.uniform(0, W), random.uniform(330, 1050), random.uniform(0, 6.3), random.choice([2, 3, 4])) for _ in range(140)]
# ACV silhouette -> ordered contour
acv = Image.open(PL + 'gummies/pick_acv.png').convert('RGBA'); m = np.array(acv)[..., 3] > 0
m = np.pad(m, 2)
cont = max(measure.find_contours(m.astype(float), 0.5), key=len)
cont = measure.approximate_polygon(cont, tolerance=0.9)
SC = 15; ch, cw = m.shape; CX0, CY0 = W / 2, 880
pts = [(CX0 + (c - cw / 2) * SC, CY0 + (r - ch / 2) * SC) for r, c in cont]
if pts[0] == pts[-1]: pts = pts[:-1]
print('stars', len(pts))
SIL = Image.fromarray((m * 255).astype(np.uint8), 'L').resize((cw * SC, ch * SC), Image.NEAREST)
SILX, SILY = int(CX0 - cw * SC / 2), int(CY0 - ch * SC / 2)
OPTS = [('A', 'mel'), ('B', 'mush'), ('C', 'acv'), ('D', 'cre')]
GUM = {k: gummy(k, 4) for _, k in OPTS}
PED = up(crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')), 3)
RAY = seq(SP + 'fork3/ray_cast', 3, 1)
T_DRAW0, T_DRAW1, T_TIMER0, T_TIMER1 = 0.9, 3.9, 4.1, 9.6; DUR = 11.8
w = Writer('v66/noaudio.mp4'); events = []
F38 = F(38)
for f in range(int(DUR * FPS)):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for (x, y, ph, s) in STARS:
        a = int(110 + 100 * math.sin(t * 2.2 + ph)); d.rectangle([x, y, x + s, y + s], fill=(230, 235, 255, max(0, a)))
    img.alpha_composite(L)
    # constellation
    u = max(0.0, min(1.0, (t - T_DRAW0) / (T_DRAW1 - T_DRAW0))); n = len(pts); shown = u * n
    if t > T_DRAW1:
        a = int(min(1, (t - T_DRAW1) / 0.6) * 70)
        fill = Image.new('RGBA', SIL.size, (120, 150, 255, 0)); fill.putalpha(SIL.point(lambda p: a if p else 0))
        img.alpha_composite(fill, (SILX, SILY))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    k = int(shown)
    for i in range(min(k, n)):
        p, q = pts[i], pts[(i + 1) % n]
        if i == k - 1 and k < n:
            fr = shown - k; q = (p[0] + (q[0] - p[0]) * fr, p[1] + (q[1] - p[1]) * fr)
        d.line([p, q], fill=(150, 190, 255, 90), width=14); d.line([p, q], fill=(225, 240, 255, 230), width=4)
    for i in range(min(k + 1, n)):
        x, y = pts[i]; s = 9 + 3 * math.sin(t * 5 + i)
        d.ellipse([x - s - 6, y - s - 6, x + s + 6, y + s + 6], fill=(150, 190, 255, 70)); d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 255))
        d.line([x - s - 4, y, x + s + 4, y], fill=(255, 255, 255, 180), width=2); d.line([x, y - s - 4, x, y + s + 4], fill=(255, 255, 255, 180), width=2)
    img.alpha_composite(L)
    for i in range(n):
        ti = T_DRAW0 + (T_DRAW1 - T_DRAW0) * i / n
        if abs(t - ti) < 0.5 / FPS and i % 3 == 0: events.append((round(t, 3), 'twinkle'))
    # Rayleigh casting the stars into the sky
    rf = RAY[int(t * 9) % len(RAY)] if t < T_DRAW1 + 0.3 else idle('ray', 3)[0] if False else RAY[0]
    img.alpha_composite(rf, (60, 1330 - 78 * 3))
    if T_DRAW0 - 0.3 < t < T_DRAW1:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(f)
        for _ in range(12):
            v = rr.random(); x = 200 + v * 340 + rr.uniform(-30, 30); y = 1180 - v * 420
            d.rectangle([x, y, x + 6, y + 6], fill=(200, 170, 255, 200))
        img.alpha_composite(L)
    # options on pedestals
    for i, (lab, kk) in enumerate(OPTS):
        cx = 150 + i * 260; by = 1640
        img.alpha_composite(PED, (int(cx - PED.width / 2), by - PED.height // 2))
        g = GUM[kk]; bob = int(10 * math.sin(t * 2.6 + i * 1.3))
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([cx - 70, by - 210 + bob, cx + 70, by - 70 + bob], fill=(255, 240, 200, 45)); img.alpha_composite(L)
        img.alpha_composite(g, (int(cx - g.width / 2), int(by - 140 - g.height / 2 + bob)))
        text_layer(img, [(cx, by + 70, lab, 52, (255, 214, 60), 7, 255)])
    # header + timer
    layer(img, lambda d: d.rounded_rectangle([50, 80, W - 50, 320], 26, fill=(14, 12, 40, 210), outline=(170, 150, 255, 255), width=5))
    d = ImageDraw.Draw(img)
    if t < T_TIMER1:
        ctext(d, W / 2, 125, 'WHICH GUMMY', F(62)); ctext(d, W / 2, 215, 'FITS THE STARS?', F(56), (190, 170, 255))
    else:
        ctext(d, W / 2, 125, "TIME'S UP!", F(62), (255, 214, 60)); ctext(d, W / 2, 215, 'COMMENT A, B, C OR D', F(42))
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(t, 3), 'ding_8bit'))
    if T_TIMER0 <= t < T_TIMER1:
        u2 = (t - T_TIMER0) / (T_TIMER1 - T_TIMER0); col = (90, 220, 120) if u2 < 0.6 else (255, 200, 60) if u2 < 0.85 else (240, 80, 80)
        d.rounded_rectangle([110, 1380, W - 110, 1414], 12, fill=(20, 18, 40), outline=(200, 190, 255), width=3)
        d.rounded_rectangle([114, 1384, 114 + int((W - 228) * (1 - u2)), 1410], 10, fill=col)
        secs = int(math.ceil(T_TIMER1 - t)); ctext(d, W / 2, 1430, str(secs), F(30), (255, 255, 255), 4)
        if secs <= 3 and abs((T_TIMER1 - t) - secs) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    w.write(img)
w.close(); json.dump(events, open('v66/events.json', 'w'))
