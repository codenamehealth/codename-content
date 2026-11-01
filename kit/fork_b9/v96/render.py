import sys; sys.path.insert(0, '../../fork_a7')
from common7 import *
K = 4
def g92(name):
    im = Image.open(A + name); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA').resize((92, 92), Image.NEAREST))
    return fr
H_IDLE = g92('idle_9.gif'); H_WALK = g92('hollow-walk-side.gif'); C_IDLE_SIDE = Image.open(PL + 'race/in/cyrus_side.png').convert('RGBA')
C_RUN = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(PL + 'race/cyrus_run/*.png'))[1:]]
RED, RED2, GOLD = (178, 36, 48, 255), (120, 20, 34, 255), (240, 196, 70, 255)
def cape_front(t):
    c = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    w = [int(2 * math.sin(t * 9 + k)) for k in range(4)]
    d.polygon([(37, 36), (55, 36), (63 + w[0], 74), (56, 76 + w[1]), (46, 74 + w[2]), (36, 76 + w[3]), (29 - w[0], 74)], fill=RED)
    d.line([(46, 40), (46, 73)], fill=RED2, width=2); d.line([(40, 40), (34, 72)], fill=RED2, width=1); d.line([(52, 40), (58, 72)], fill=RED2, width=1)
    return c
def cape_side(t, strength=1.0):
    c = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    f = [int(strength * 3 * math.sin(t * 11 + k * 1.3)) for k in range(4)]
    d.polygon([(42, 36), (47, 37), (44, 52), (40 + f[0], 66), (33 + f[1], 74), (24 + f[2], 70), (28 + f[3], 58), (36, 44)], fill=RED)
    d.line([(42, 40), (31 + f[1], 70)], fill=RED2, width=2)
    return c
def with_cape(spr, cape, clasp=None):
    o = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); o.alpha_composite(cape); o.alpha_composite(spr)
    if clasp: ImageDraw.Draw(o).rectangle([clasp[0], clasp[1], clasp[0] + 2, clasp[1] + 1], fill=GOLD)
    return up(o, K)
BG = bg_frames('found_hd.gif', (W, H), box=(300, 0, 907, 1080), step=1)
FACE_C = idle('cyrus', 1)[0].crop((28, 10, 64, 46)); FACE_H = H_IDLE[0].crop((28, 10, 64, 46))
GROUND = 1300
LINES = [(0.25, 1.35, 'CYRUS', 'Quick! Run!'), (1.45, 2.55, 'THE HOLLOW', "I don't run."), (2.65, 3.75, 'THE HOLLOW', 'I have a cape.'), (4.15, 5.9, 'THE HOLLOW', '...Wait for me.')]
DUR = 6.2; T_GO = 3.85
out = Writer('v96_noaudio.mp4'); ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 8) % len(BG)].copy()
    # characters
    hx = 690 if t < T_GO + 0.3 else 690 + (t - T_GO - 0.3) * 38
    if t < T_GO + 0.3:
        hs = with_cape(H_IDLE[int(t * 6) % len(H_IDLE)], cape_front(t * (2.2 if 2.65 <= t < 3.75 else 1.0)), (45, 37))
    else:
        hs = with_cape(H_WALK[int((t - T_GO) * 3) % len(H_WALK)], cape_side(t, 0.6))
    if t < T_GO:
        cs = up(C_IDLE_SIDE, K); cx = 300 + int(2 * math.sin(t * 5))
        if 0.25 <= t < 1.35: cs = up(C_RUN[int(t * 6) % 2], K); cx = 300  # eager bounce
    else:
        u = t - T_GO; cx = 300 + 950 * u; cs = up(C_RUN[int(u * 16) % len(C_RUN)], K)
    img.alpha_composite(hs, (int(hx - hs.width / 2), GROUND - 78 * K))
    if cx < W + 200: img.alpha_composite(cs, (int(cx - cs.width / 2), GROUND - 78 * K))
    # FX: cape flourish wind lines and dust behind Cyrus
    def fx(d):
        if 2.65 <= t < 3.75:
            for k in range(5):
                ph = (t * 3 + k * 0.2) % 1.0; y = GROUND - 220 + k * 30; x = hx - 220 + ph * 160
                d.line([(x, y), (x + 70, y)], fill=(255, 255, 255, int(200 * (1 - ph))), width=4)
            for k in range(6):
                a = t * 4 + k; d.rectangle([hx + 110 * math.cos(a) - 4, GROUND - 200 + 60 * math.sin(a) - 4, hx + 110 * math.cos(a) + 4, GROUND - 200 + 60 * math.sin(a) + 4], fill=(255, 230, 120, 220))
        if t >= T_GO:
            for k in range(8):
                u = t - T_GO - k * 0.06
                if 0 <= u < 0.7:
                    px = 300 + 950 * (k * 0.06) ; r = 14 + u * 60
                    d.ellipse([px - r, GROUND - 20 - r * 0.6, px + r, GROUND - 20 + r * 0.6], fill=(220, 200, 160, int(170 * (1 - u / 0.7))))
    layer(img, fx)
    # title
    text_layer(img, [(W / 2, 300, 'Every escort', 52, (255, 255, 255), 7, 255), (W / 2, 380, 'mission ever', 52, (255, 255, 255), 7, 255)])
    # dialogue box
    cur = [l for l in LINES if l[0] <= t < l[1]]
    layer(img, lambda d: d.rectangle([50, 1360, 1030, 1640], fill=(14, 16, 48, 235)))
    d = ImageDraw.Draw(img)
    d.rectangle([50, 1360, 1030, 1640], outline=(240, 236, 220), width=6); d.rectangle([60, 1370, 1020, 1630], outline=(70, 80, 140), width=3)
    if cur:
        t0, t1, who, txt = cur[0]
        n = min(len(txt), int((t - t0) * 24) + 1); shown = txt[:n]
        face = up(FACE_C if who == 'CYRUS' else FACE_H, 4)
        d.rectangle([80, 1395, 80 + face.width + 8, 1395 + face.height + 8], fill=(40, 44, 90), outline=(240, 196, 70), width=4)
        img.alpha_composite(face, (84, 1399)); d = ImageDraw.Draw(img)
        d.text((250, 1440), shown, font=F(40), fill=(255, 255, 255))
        tw = d.textlength(who, font=F(26)); d.rectangle([1000 - tw - 30, 1318, 1000, 1366], fill=(14, 16, 48), outline=(240, 196, 70), width=4)
        d.text((1000 - tw - 15, 1330), who, font=F(26), fill=(255, 214, 60))
        if n == len(txt) and int(t * 3) % 2: d.polygon([(975, 1590), (1005, 1590), (990, 1608)], fill=(255, 214, 60))
        if abs(t - t0) < 0.5 / FPS: ev.append((round(t0, 3), 'tick_8bit'))
    if abs(t - T_GO) < 0.5 / FPS: ev.append((T_GO, 'whoosh_8bit'))
    if abs(t - 2.65) < 0.5 / FPS: ev.append((2.65, 'twinkle'))
    out.write(img)
out.close(); json.dump(ev, open('ev.json', 'w')); print('ok')
