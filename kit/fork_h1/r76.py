import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7'); from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
STILL = os.environ.get('STILL')
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong   # rc8: gummy shine on Joy's ACV card gummy (VETTING)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# table
tb = Image.open(SP + 'fork_a8/gen/table/02.png').convert('RGBA').crop((5, 5, 123, 123)); tb = up(tb, 3)
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
CANDLE = up(crop(Image.open(SP + 'fork_a8/gen/candle/01.png').convert('RGBA')), 4)
CANDLES = [(90, 170), (990, 170), (90, 1700), (990, 1700)]   # top pair moved above the hook band
for cx, cy in CANDLES: TABLE.alpha_composite(CANDLE, (cx - CANDLE.width // 2, cy - CANDLE.height // 2))
deco = [('mush', 170, 1520, 3), ('acv', 900, 1560, 3), ('mel', 880, 1880, 3), ('cre', 980, 1180, 2), ('acv', 60, 1080, 2)]   # gold deco gummy -> product gummy
for k, x, y, s in deco:
    g = gummy(k, s); TABLE.alpha_composite(g, (x - g.width // 2, y - g.height // 2))
# cards
CS = 3   # parchment 4x -> 3x so 2 rows fit the zone; guide sprites stay 3x, gummies 3x
parch = up(crop(Image.open(SP + 'fork_a3/parch/00.png').convert('RGBA')), CS); CWd, CHt = parch.size
BACK = crop(Image.open(SP + 'fork_a8/gen/cardback/01.png').convert('RGBA')).resize((CWd, CHt), Image.NEAREST)
GUIDES = [('joy', 'JOY', (74, 124, 58), 'acv'), ('cleo', 'CLEO', (46, 93, 168), 'cre'), ('cyrus', 'CYRUS', (217, 122, 31), 'mush'), ('ray', 'RAYLEIGH', (107, 45, 107), 'mel')]
IDL = {g: idle(g, 3) for g, *_ in GUIDES}
def face(i, t):
    g, name, col, gk = GUIDES[i]
    c = parch.copy(); d = ImageDraw.Draw(c)
    d.rectangle([24, 30, CWd - 24, 84], fill=col + (255,)); d.rectangle([24, 30, CWd - 24, 84], outline=(240, 200, 90, 255), width=4)
    ctext(d, CWd / 2, 42 if len(name) < 6 else 45, name, F(30 if len(name) < 6 else 24), (255, 255, 255), 5)
    sp = IDL[g][int(t * 8) % len(IDL[g])]; c.alpha_composite(sp, (CWd // 2 - sp.width // 2, 36))
    gm = up(acv_gummy_strong(), 3) if gk == 'acv' else gummy(gk, 3); c.alpha_composite(gm, (CWd // 2 - gm.width // 2, CHt - 38 - gm.height))
    return c
# rc8 (VETTING: FOLLOW CLEO from 0s): band sub WATCH CLOSELY 36px -> FOLLOW CLEO 52px in Cleo blue; end band keeps WHERE'S CLEO? + 52px comment line
# hfg8: soft fade, no box. FOLLOW CLEO kept (Bennett's line, the actual task) as a 52px Cleo-blue line inside the same fade;
# end: WHERE'S / CLEO? replaces the hook text, 'Comment A, B, C or D' cut (the A-D badges + caption carry it)
_, HBF = hook_fade(['REMEMBER', 'THE GUIDES'], accent=1, size=72)
HOOK_A, _ = hook_fade(['REMEMBER', 'THE GUIDES'], accent=1, size=72, fade_to=HBF + 200)
import sys as _hw; _hw.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1'); from hookw import hook_fade_w
HOOK_A, HG = hook_fade_w(['KEEP YOUR EYES', 'ON CLEO'], ['CLEO'], color=(120, 170, 255), size=64, y=286, fade_to=HBF + 200); print('new hook', HG)   # fork_h1: replaces REMEMBER / THE GUIDES + FOLLOW CLEO; same top as WHERE'S CLEO?
HOOK_B, HBB = hook_fade(["WHERE'S", 'CLEO?'], accent=1, color=(120, 170, 255), size=72)
HB = 590   # old band bottom: keeps the card slots and swap arcs identical (text now ends ~y540)
print('HB', HB, HBB)
SLOT = [(230, 805), (660, 805), (230, 1283), (660, 1283)]   # rc8: top row 10px lower for the 52px band line (cards x95-795, y598-1490)
SWAPS = [(0, 3), (1, 2), (0, 1), (2, 3), (1, 3), (0, 2), (0, 3), (1, 2), (0, 1)]
T_DEAL, T_FLIP, T_SH = 0.45, 1.6, 2.5;   # rc8: cards deal in from frame 0, flip face down 1.6-2.1s (was a 3.2s static face-up), shuffle 2.5s (was 4.2s)
durs = [0.95, 0.85, 0.75, 0.68, 0.6, 0.55, 0.5, 0.46, 0.42]
sched = []; tt = T_SH
for (a, b), du in zip(SWAPS, durs): sched.append((tt, tt + du, a, b)); tt += du + 0.08
T_END = tt + 0.3
CD0, CDB = T_END + 0.3, 0.6           # rc8: 3-2-1 starts as the A-D badges land, 0.6s per number (was a 1.6s wait + 1s each)
DUR = CD0 + 3 * CDB; N = int(round(DUR * FPS)); print('DUR', round(DUR, 2), 'T_END', round(T_END, 2))
where = {i: i for i in range(4)}   # card -> slot (initial)
timeline = []
for (t0, t1, a, b) in sched:
    ca = [c for c, s in where.items() if s == a][0]; cb = [c for c, s in where.items() if s == b][0]
    timeline.append((t0, t1, ca, a, b, cb)); where[ca], where[cb] = b, a
def _inside(x, y, sc):
    w2, h2 = CWd * sc / 2, CHt * sc / 2
    return x - w2 >= 72 and y - h2 >= HB + 6 and y + h2 <= 1500 and x + w2 <= (887 if y + h2 > 1110 else 1025)
def _maxb(fr, to, sgn, top):
    x0, y0 = SLOT[fr]; x1, y1 = SLOT[to]; nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1
    for b in range(190, -1, -5):
        ok = True
        for k in range(41):
            e = k / 40; bl = b * math.sin(math.pi * e) * sgn
            sc = 1 + 0.1 * math.sin(math.pi * e) * (1 if top else -0.4)
            if not _inside(x0 + (x1 - x0) * e + nx / L * bl, y0 + (y1 - y0) * e + ny / L * bl, sc): ok = False; break
        if ok: return b
    return 0
BUL = []
for (t0, t1, ca, a, b, cb) in timeline:
    best = None
    for fl in (1, -1):
        ba, bb = _maxb(a, b, fl, True), _maxb(b, a, -fl, False)
        if best is None or min(ba, bb) + 0.1 * (ba + bb) > best[0]: best = (min(ba, bb) + 0.1 * (ba + bb), fl, ba, bb)
    BUL.append(best[1:])
print('bulges (flip, top card, other card):', BUL)
print('Cleo ends in slot', where[1], 'ABCD'[where[1]], 'shuffle ends', round(T_END, 2))
def card_state(c, t):
    s = c; pos = None
    cur = {i: i for i in range(4)}
    for k, (t0, t1, ca, a, b, cb) in enumerate(timeline):
        if t >= t1: cur[ca], cur[cb] = b, a; continue
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0); e = u * u * (3 - 2 * u)
            if c in (ca, cb):
                fr, to = (a, b) if c == ca else (b, a); sgn = 1 if c == ca else -1
                x0, y0 = SLOT[fr]; x1, y1 = SLOT[to]
                x = x0 + (x1 - x0) * e; y = y0 + (y1 - y0) * e
                nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1
                fl, ba, bb = BUL[k]; bulge = (ba if c == ca else bb) * math.sin(math.pi * e) * sgn * fl
                return x + nx / L * bulge, y + ny / L * bulge, 1 + 0.1 * math.sin(math.pi * e) * (1 if sgn > 0 else -0.4), sgn > 0
        break
    if t < T_DEAL + 0.08 * 3:      # rc8 deal-in: each card flies out of the centre gap to its slot (staggered, card 0 already moving on frame 0)
        u = min(1.0, max(0.0, (t + 0.06 - 0.08 * c) / T_DEAL)); e = 1 - (1 - u) ** 3
        x1, y1 = SLOT[c]; x0, y0 = 445, 1044
        return x0 + (x1 - x0) * e, y0 + (y1 - y0) * e - 60 * math.sin(math.pi * e), 0.25 + 0.75 * e, False
    return SLOT[cur[c]][0], SLOT[cur[c]][1], 1.0, False
w = Writer('v76_noaudio.mp4'); ev = [(0.0, 'chime')]
for (t0, t1, *_) in timeline: ev.append((round(t0, 3), 'swish'))
ev += [(T_FLIP, 'whoosh_8bit'), (round(T_END + 0.1, 3), 'twinkle')]
for k in range(3): ev.append((round(CD0 + k * CDB, 3), 'tick_8bit'))
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
    if t >= T_END:
        a = int(255 * min(1, (t - T_END) / 0.3))
        layer(img, lambda d: [d.ellipse([x - CWd / 2 - 6, y - CHt / 2 - 6, x - CWd / 2 + 66, y - CHt / 2 + 66], fill=(30, 20, 40, a), outline=(255, 214, 60, a), width=5) for (x, y) in SLOT])
        for i, (x, y) in enumerate(SLOT):
            items.append((x - CWd / 2 + 32, y - CHt / 2 + 8, 'ABCD'[i], 40, (255, 214, 60), 5, a))
        if t >= CD0:      # rc8: countdown badge ~1.5x wider, digit 70 -> 110px (pops on each number), centred in the gap
            cd = max(1, 3 - int((t - CD0) / CDB)); ph = (t - CD0) - (3 - cd) * CDB; R_ = 78 + (8 if ph < 0.12 else 0)
            layer(img, lambda d: d.ellipse([445 - R_, 1044 - R_, 445 + R_, 1044 + R_], fill=(30, 20, 40, 240), outline=(255, 214, 60, 255), width=7))
            sz = 110 + (12 if ph < 0.12 else 0)
            items.append((445 + 5, 1044 - sz / 2, str(cd), sz, (255, 214, 60), 9, 255))
    text_layer(img, items)
    img.alpha_composite(HOOK_B if t >= T_END else HOOK_A)
    if STILL and f in [int(x) for x in STILL.split(',')]: img.convert('RGB').save(f'k76_{f}.png')
    w.write(img)
w.close(); json.dump({'events': ev}, open('v76_events.json', 'w')); print('done')
