import sys; sys.path.insert(0, '../../fork_a7'); from common7 import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 15.9; N = int(DUR * FPS)
# table
tb = Image.open('../gen/table/02.png').convert('RGBA').crop((5, 5, 123, 123)); tb = up(tb, 3)
TABLE = Image.new('RGBA', (W, H))
for yy in range(0, H, tb.height):
    for xx in range(0, W, tb.width):
        t2 = tb
        if (xx // tb.width) % 2: t2 = t2.transpose(Image.FLIP_LEFT_RIGHT)
        if (yy // tb.height) % 2: t2 = t2.transpose(Image.FLIP_TOP_BOTTOM)
        TABLE.alpha_composite(t2, (xx, yy))
TABLE = ImageEnhance.Brightness(TABLE).enhance(0.8)
vig = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(vig)
for i in range(40): vd.ellipse([-300 + i * 12, -200 + i * 16, W + 300 - i * 12, H + 200 - i * 16], fill=int(i * 4.5))
dark = Image.new('RGBA', (W, H), (10, 6, 4, 255)); dark.putalpha(vig.point(lambda p: 200 - min(200, p))); TABLE.alpha_composite(dark)
CANDLE = up(crop(Image.open('../gen/candle/01.png').convert('RGBA')), 4)
CANDLES = [(90, 470), (990, 470), (90, 1700), (990, 1700)]
for cx, cy in CANDLES: TABLE.alpha_composite(CANDLE, (cx - CANDLE.width // 2, cy - CANDLE.height // 2))
deco = [('mush', 170, 1520, 3), ('acv', 900, 1560, 3), ('mel', 880, 1880, 3), ('cre', 980, 1180, 2), ('gold', 80, 1080, 2)]
for k, x, y, s in deco:
    g = gummy(k, s); TABLE.alpha_composite(g, (x - g.width // 2, y - g.height // 2))
# cards
CS = 4
parch = up(crop(Image.open('../../fork_a3/parch/00.png').convert('RGBA')), CS); CWd, CHt = parch.size
BACK = crop(Image.open('../gen/cardback/01.png').convert('RGBA')).resize((CWd, CHt), Image.NEAREST)
GUIDES = [('joy', 'JOY', (74, 124, 58), 'acv'), ('cleo', 'CLEO', (46, 93, 168), 'cre'), ('cyrus', 'CYRUS', (217, 122, 31), 'mush'), ('ray', 'RAYLEIGH', (107, 45, 107), 'mel')]
IDL = {g: idle(g, 3) for g, *_ in GUIDES}
def face(i, t):
    g, name, col, gk = GUIDES[i]
    c = parch.copy(); d = ImageDraw.Draw(c)
    d.rectangle([32, 40, CWd - 32, 112], fill=col + (255,)); d.rectangle([32, 40, CWd - 32, 112], outline=(240, 200, 90, 255), width=4)
    ctext(d, CWd / 2, 60, name, F(30 if len(name) < 6 else 24), (255, 255, 255), 5)
    sp = IDL[g][int(t * 8) % len(IDL[g])]; c.alpha_composite(sp, (CWd // 2 - sp.width // 2, 110))
    gm = gummy(gk, 3); c.alpha_composite(gm, (CWd // 2 - gm.width // 2, CHt - 50 - gm.height))
    return c
SLOT = [(285, 790), (795, 790), (285, 1385), (795, 1385)]
SWAPS = [(0, 3), (1, 2), (0, 1), (2, 3), (1, 3), (0, 2), (0, 3), (1, 2), (0, 1)]
T_FLIP, T_SH = 3.2, 4.2; durs = [0.95, 0.85, 0.75, 0.68, 0.6, 0.55, 0.5, 0.46, 0.42]
sched = []; tt = T_SH
for (a, b), du in zip(SWAPS, durs): sched.append((tt, tt + du, a, b)); tt += du + 0.08
T_END = tt + 0.3
where = {i: i for i in range(4)}   # card -> slot (initial)
timeline = []
for (t0, t1, a, b) in sched:
    ca = [c for c, s in where.items() if s == a][0]; cb = [c for c, s in where.items() if s == b][0]
    timeline.append((t0, t1, ca, a, b, cb)); where[ca], where[cb] = b, a
print('Cleo ends in slot', where[1], 'ABCD'[where[1]], 'shuffle ends', round(T_END, 2))
def card_state(c, t):
    s = c; pos = None
    cur = {i: i for i in range(4)}
    for (t0, t1, ca, a, b, cb) in timeline:
        if t >= t1: cur[ca], cur[cb] = b, a; continue
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0); e = u * u * (3 - 2 * u)
            if c in (ca, cb):
                fr, to = (a, b) if c == ca else (b, a); sgn = 1 if c == ca else -1
                x0, y0 = SLOT[fr]; x1, y1 = SLOT[to]
                x = x0 + (x1 - x0) * e; y = y0 + (y1 - y0) * e
                nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1
                bulge = 190 * math.sin(math.pi * e) * sgn
                return x + nx / L * bulge, y + ny / L * bulge, 1 + 0.1 * math.sin(math.pi * e) * (1 if sgn > 0 else -0.4), sgn > 0
        break
    return SLOT[cur[c]][0], SLOT[cur[c]][1], 1.0, False
w = Writer('noaudio.mp4'); ev = [(0.2, 'chime')]
for (t0, t1, *_) in timeline: ev.append((round(t0, 3), 'swish'))
ev += [(T_FLIP, 'whoosh_8bit'), (round(T_END + 0.1, 3), 'twinkle')]
for k in range(3): ev.append((round(T_END + 1.6 + k, 3), 'tick_8bit'))
for f in range(N):
    t = f / FPS; img = TABLE.copy()
    # candle glow
    layer(img, lambda d: [d.ellipse([cx - r, cy - 30 - r, cx + r, cy - 30 + r], fill=(255, 190, 90, int(14 + 6 * math.sin(t * 9 + cx)))) for cx, cy in CANDLES for r in (160, 110, 70)])
    states = [(c,) + card_state(c, t) for c in range(4)]
    states.sort(key=lambda s: (s[4], s[3]))
    for c, x, y, sc, top in states:
        if t < T_FLIP: im = face(c, t); sx = 1.0
        elif t < T_FLIP + 0.5:
            u = (t - T_FLIP) / 0.5
            im = face(c, t) if u < 0.5 else BACK; sx = abs(math.cos(u * math.pi))
        else: im = BACK; sx = 1.0
        ww, hh = max(2, int(im.width * sx * sc)), int(im.height * sc)
        im2 = im.resize((ww, hh), Image.NEAREST)
        layer(img, lambda d: d.rounded_rectangle([x - ww / 2 + 14, y - hh / 2 + 18, x + ww / 2 + 14, y + hh / 2 + 18], 14, fill=(0, 0, 0, 90)))
        img.alpha_composite(im2, (int(x - ww / 2), int(y - hh / 2)))
    items = []
    if t < T_FLIP + 0.4:
        items += [(W / 2, 170, 'REMEMBER', 72, (255, 255, 255), 8, 255), (W / 2, 265, 'THE GUIDES', 72, (255, 214, 60), 8, 255)]
    elif t < T_END:
        items += [(W / 2, 200, 'WATCH CLOSELY', 66, (255, 255, 255), 8, 255)]
    else:
        a = int(255 * min(1, (t - T_END) / 0.3))
        items += [(W / 2, 150, "WHERE'S", 72, (255, 255, 255), 8, a), (W / 2, 245, 'CLEO?', 84, (120, 170, 255), 8, a)]
        layer(img, lambda d: [d.ellipse([x - CWd / 2 - 30, y - CHt / 2 - 30, x - CWd / 2 + 50, y - CHt / 2 + 50], fill=(30, 20, 40, a), outline=(255, 214, 60, a), width=5) for (x, y) in SLOT])
        for i, (x, y) in enumerate(SLOT):
            items.append((x - CWd / 2 + 10, y - CHt / 2 - 14, 'ABCD'[i], 44, (255, 214, 60), 5, a))
        items += [(W / 2, 1745, 'Comment A, B, C or D', 40, (255, 255, 255), 6, a)]
        cd = 3 - int(t - T_END - 1.6)
        if 1 <= cd <= 3 and t - T_END > 1.6: items.append((W / 2, 1810, str(cd), 70, (255, 214, 60), 8, 255))
    text_layer(img, items)
    w.write(img)
w.close(); json.dump({'events': ev}, open('events.json', 'w')); print('done')
