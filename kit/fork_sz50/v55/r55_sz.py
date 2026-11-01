import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image, ImageDraw, ImageEnhance
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a6'); OUT = '../fork_sz50/v55/'
sys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer
HK, HB = hook_layer(['WHO WOULD WIN', 'THE RACE?'], accent=1); print('HB', HB)
def MX(x): return 160 + (x - 120) * (660 / 852)
rnd = random.Random(55)
# ---------------- ground: PixelLab Wang tiles, clay track inside grass
meta = json.load(open('track_meta.json')); sheet = Image.open('track_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
Y0 = 420; TS = 64; GC, GR = 17, 21
def low(i, j): return 3 <= j <= 17
GROUND = Image.new('RGBA', (W, H), (40, 90, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (low(i, j), low(i + 1, j), low(i, j + 1), low(i + 1, j + 1)); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * TS - 10, Y0 + j * TS))
TY0, TY1 = Y0 + 3 * TS + 6, Y0 + 17 * TS - 6
LH = (TY1 - TY0) / 4
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
def lane_y(k): return TY0 + LH * (k + 0.5) + 62     # feet
gd = ImageDraw.Draw(GROUND)
for k in range(1, 4):
    y = int(TY0 + LH * k)
    for x in range(0, W, 36): gd.rectangle([x, y - 3, x + 22, y + 2], fill=(245, 236, 220, 255))
X0, XF = 120, 972
for y in range(int(TY0), int(TY1), 6): gd.rectangle([MX(X0) - 4, y, MX(X0) + 2, y + 3], fill=(245, 236, 220, 255))
for r in range(int((TY1 - TY0) / 14) + 1):
    for c in range(2):
        col = (245, 245, 245, 255) if (r + c) % 2 == 0 else (25, 22, 30, 255)
        gd.rectangle([MX(XF) + c * 14 - 14, TY0 + r * 14, MX(XF) + c * 14 - 1, min(TY1, TY0 + r * 14 + 13)], fill=col)
# lane name tags
def face(name, rad):
    SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 26) for n in NAMES}
for k, n in enumerate(NAMES):
    ic = ICON[n]; GROUND.alpha_composite(ic, (108 - ic.width // 2, int(TY0 + LH * k + 14)))
# ---------------- sprites
SR = {g: seq(PL + f'race/{g}_run', 3) for g in ['joy', 'cyrus', 'cleo', 'ray']}
hw = Image.open(A + 'hollow-walk-side.gif'); HW = []
for i in range(hw.n_frames):
    hw.seek(i); f = hw.convert('RGBA').crop((290, 120, 610, 790)); k = 192 / 650
    HW.append(f.resize((int(f.width * k), int(f.height * k)), Image.NEAREST))
HEAT = seq(SP + 'fork3/hollow_eat', 3)
CBLK = seq(SP + 'fork_a4/cleo_block', 3)
RCAST = seq(SP + 'fork3/ray_cast', 3)
JCAST = seq(SP + 'fork_a3/joy_cast', 3)
CVIC = vic('cyrus', 225)
HVIC = vic('cleo', 360)
CWALK = [up(Image.open(f'../fork_a5/gen/cleo_walk/{i:02d}.png').convert('RGBA'), 3) for i in range(1, 9)]
CREG = gummy('cre', 2)
SLIME = seq(PL + 'race/slime_idle_c', 3)
SLIME_S = [up(f, 0.62) for f in SLIME]
GOLD = gummy('gold', 2)
STAND = {g: up(Image.open(SP + 'syeda_src/' + p).convert('RGBA'), 3) for g, p in {'joy': 'char1/char8.png', 'cyrus': 'char4/char10.png', 'cleo': 'char3/char7.png', 'ray': 'char2/char5.png'}.items()}
# ---------------- header bg (Liza castle)
HDR = bg_frames('vit_hd.gif', (W, 430), box=(0, 40, 1920, 40 + 764), step=2, bright=0.62)
# ---------------- timeline
T_GO = 2.3
PLAN = {  # name: (speed px/s, stop x)
    'ray': (300, 330), 'joy': (320, 520), 'cleo': (310, 650), 'cyrus': (390, 800)}
HV = 64.0; H_START = T_GO + 1.1
T_WIN = H_START + (XF - X0) / HV
T_NOTICE = T_WIN - 0.75
T_END = T_WIN + 4.2
print('T_WIN', round(T_WIN, 2))
def pos(n, t):
    if n == 'cleo':
        if t < H_START: return X0
        return min(XF, X0 + (t - H_START) * HV)
    v, sx = PLAN[n]
    if t < T_GO: return X0
    tstop = T_GO + (sx - X0) / v
    if n == 'cyrus' and t > T_NOTICE + 0.55:
        return min(XF + 60, sx + (t - (T_NOTICE + 0.55)) * 430)
    return min(sx, X0 + (t - T_GO) * v)
def stopped(n, t):
    v, sx = PLAN[n]; return t >= T_GO + (sx - X0) / v
EV = []
def ev(t, name):
    if not any(abs(e[0] - t) < 0.01 and e[1] == name for e in EV): EV.append((round(t, 3), name))
for tt in (0.5, 1.1, 1.7): ev(tt, 'tick_8bit')
ev(T_GO, 'go_8bit'); ev(T_GO + 0.05, 'whoosh_8bit'); ev(T_GO + 0.3, 'twinkle')
ev(0.2, 'cheer')
# distraction timing
PLAN['cleo'] = (HV, XF)
STOPT = {n: T_GO + (PLAN[n][1] - X0) / PLAN[n][0] for n in PLAN if n != 'cleo'}
FIREWORKS = [STOPT['ray'] + 0.6 + i * 1.15 for i in range(12) if STOPT['ray'] + 0.6 + i * 1.15 < T_WIN + 2]
for f in FIREWORKS: ev(f + 0.35, 'poofpops')
HEALS = [STOPT['joy'] + 0.4 + i * 1.6 for i in range(10) if STOPT['joy'] + 0.4 + i * 1.6 < T_WIN + 2]
for h in HEALS: ev(h + 0.5, 'chime')
ev(T_NOTICE, 'buzz_8bit'); ev(T_WIN, 'victory'); ev(T_WIN + 0.1, 'cheer')
TICK = [(0, 'PICK YOUR RUNNER!'), (T_GO, 'AND THEY\'RE OFF!'), (STOPT['ray'] + 0.2, 'RAYLEIGH STOPS FOR A SHOW?!'),
        (STOPT['joy'] + 0.2, 'JOY IS HEALING A BABY SLIME'),
        (STOPT['cyrus'] + 0.2, 'CYRUS IS WAY OUT IN FRONT'), (STOPT['cyrus'] + 3.2, 'JOY: "AWW, ONE MORE!"'),
        (STOPT['cyrus'] + 5.8, 'RAYLEIGH IS DOING AN ENCORE'), (T_NOTICE - 3.2, 'WAIT. WHERE IS CLEO?'),
        (T_WIN, 'CLEO WINS!')]
def bubble(img, x, y, text, a=255, col=(255, 255, 255)):
    f = F(20); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    w = d.textlength(text, font=f); bx0, by0 = int(x - w / 2 - 14), int(y - 44)
    bx0 = max(74, min((1021 if by0 + 54 < 1110 else 883) - w - 28, bx0))
    d.rounded_rectangle([bx0, by0, bx0 + w + 28, by0 + 40], 10, fill=(255, 255, 255, a), outline=(25, 20, 35, a), width=4)
    d.polygon([(x - 10, by0 + 38), (x + 10, by0 + 38), (x - 2, by0 + 54)], fill=(255, 255, 255, a), outline=(25, 20, 35, a))
    d.rectangle([x - 8, by0 + 34, x + 8, by0 + 38], fill=(255, 255, 255, a))
    d.text((bx0 + 14, by0 + 10), text, font=f, fill=(25, 20, 35, a))
    img.alpha_composite(L)
CROWD_T = [(x, Y0 + 92 + (i % 2) * 58) for i, x in enumerate(range(20, W, 76))]
CROWD_B = [(x, TY1 + 150 + (i % 2) * 70) for i, x in enumerate(range(40, W, 80))]
FLAGC = [RING[n] for n in NAMES]
NF = int(T_END * FPS)
wr = Writer(OUT + 'v55_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    img = GROUND.copy()
    # crowds of friendly slimes with guild pennants
    hype = 1.6 if (t > T_WIN or t < 0.8) else 1.0
    for i, (x, y) in enumerate(CROWD_T + CROWD_B):
        fr = SLIME[(int(t * 10) + i * 3) % len(SLIME)]
        hop = int(abs(math.sin(t * 6 * hype + i * 1.3)) * 10 * hype)
        img.alpha_composite(fr, (int(x - fr.width / 2), int(y - fr.height + 30 - hop)))
        if i % 3 == 0:
            c = FLAGC[i % len(FLAGC)]; d = ImageDraw.Draw(img); px, py = x + 18, y - 40 - hop
            d.line([px, py, px, py + 34], fill=(70, 50, 30, 255), width=3)
            d.polygon([(px, py), (px + 24 + int(3 * math.sin(t * 8 + i)), py + 7), (px, py + 14)], fill=c + (255,))
    # ray fireworks
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    rx = MX(pos('ray', t))
    for k, ft in enumerate(FIREWORKS):
        u = t - ft
        if 0 <= u < 1.4:
            cx, cy = rx + 60 + (k % 3 - 1) * 140, lane_y(3) - 330 - (k % 2) * 90 - min(u, 0.35) * 200
            if u < 0.35:
                dl.rectangle([rx + 30, lane_y(3) - 120 - u * 400, rx + 38, lane_y(3) - 108 - u * 400], fill=(255, 230, 150, 255))
            else:
                v = u - 0.35; a = int(255 * max(0, 1 - v / 1.05))
                cols = [(255, 120, 220), (255, 214, 60), (190, 90, 240), (120, 220, 255)]
                for s in range(16):
                    ang = s * math.pi / 8; r = 30 + v * 240
                    sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang) + v * v * 40
                    dl.rectangle([sx - 8, sy - 8, sx + 8, sy + 8], fill=cols[(s + k) % 4] + (a,))
    img.alpha_composite(L)
    # runners, back lanes first
    for k, n in enumerate(NAMES):
        x = MX(pos(n, t)); y = lane_y(k)
        layer(img, lambda dd: dd.ellipse([x - 30, y - 8, x + 30, y + 8], fill=(0, 0, 0, 70)))
        if n == 'cleo':
            if t < H_START or t >= T_WIN: spr = STAND['cleo'] if t < T_WIN + 0.9 else CWALK[0]
            else: spr = CWALK[int(t * 8) % len(CWALK)]
            if T_GO <= t < H_START:
                u = (t - T_GO) / (H_START - T_GO); g = CREG
                if u < 0.8: img.alpha_composite(g, (int(x + 10 - g.width / 2), int(y - 230 + u * 120)))
                if 0.6 < u: text_layer(img, [(x, y - 250 - (u - 0.6) * 60, '+1 STEADY', 22, (120, 180, 255), 5, int(255 * min(1, (1 - u) / 0.2)))])
            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height + 45)))
            if H_START <= t < T_WIN:
                for s in range(3):
                    sx = x - 30 - s * 22 - (t * 40 % 22); sy = y - 60 + 10 * math.sin(t * 5 + s)
                    layer(img, lambda dd: dd.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 90, 200 - s * 50)))
            continue
        if t < T_GO:
            spr = SR[n][0]
        elif n == 'cyrus' and t > T_NOTICE + 0.55:
            spr = SR[n][int(t * 16) % 8]
        elif not stopped(n, t):
            spr = SR[n][int(t * 14) % 8]
        else:
            u = t - STOPT[n]
            if n == 'ray': spr = RCAST[int(u * 10) % len(RCAST)]
            elif n == 'joy': spr = JCAST[int(u * 8) % len(JCAST)]
            elif n == 'cleo': spr = CBLK[min(len(CBLK) - 1, int(((u - 0.3) % 0.95) / 0.95 * len(CBLK) * 1.3))] if u > 0.3 else STAND['cleo']
            else:
                spr = CVIC[int(u * 8) % len(CVIC)] if t < T_NOTICE else STAND['cyrus']
        if n == 'cyrus' and stopped(n, t) and t < T_NOTICE + 0.55 and spr in CVIC:
            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height + 4)))
        else:
            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height + 45)))
        # Joy's queue of baby slimes
        if n == 'joy' and stopped(n, t):
            u = t - STOPT[n]
            for q in range(5):
                qx = x - 120 - q * 70 + min(1, (u % 1.6) / 1.6) * 70 * (1 if q > 0 else 0)
                if q == 0: qx = x - 105
                fr = SLIME_S[(int(t * 10) + q) % len(SLIME_S)]
                img.alpha_composite(fr, (int(qx - fr.width / 2), int(y - fr.height + 18 - abs(math.sin(t * 7 + q)) * 8)))
            for h in HEALS:
                v = t - h
                if 0 <= v < 0.9:
                    text_layer(img, [(x - 105, y - 120 - v * 60, '+HP', 22, (120, 255, 120), 5, int(255 * (1 - v / 0.9)))])
        # Cyrus hearts from fans
        if n == 'cyrus' and stopped(n, t) and t < T_NOTICE:
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for s in range(5):
                ph = (t * 0.7 + s * 0.21) % 1.0
                hx = x - 120 + s * 60 + 10 * math.sin(t * 3 + s); hy = Y0 + 150 + ph * (y - Y0 - 240)
                a = int(255 * (1 - abs(ph - 0.5) * 2) ** 0.5)
                for (dx, dy) in ((-6, -3), (6, -3), (0, 3), (-3, 0), (3, 0), (0, 6)):
                    dl.rectangle([hx + dx - 4, hy + dy - 4, hx + dx + 4, hy + dy + 4], fill=(255, 100, 150, a))
            img.alpha_composite(L)
    # speech bubbles
    def show(n, t0, t1, text):
        if t0 <= t < t1:
            k = NAMES.index(n); a = int(255 * min(1, (t - t0) / 0.15, (t1 - t) / 0.15))
            bubble(img, int(MX(pos(n, t))), int(lane_y(k) - 200), text, a)
    show('ray', STOPT['ray'] + 0.1, STOPT['ray'] + 2.3, 'FOR MY FANS!')
    show('ray', STOPT['ray'] + 6.2, STOPT['ray'] + 8.2, 'ENCORE?!')
    show('joy', STOPT['joy'] + 0.1, STOPT['joy'] + 2.2, 'AWW, ARE YOU HURT?')
    show('joy', STOPT['joy'] + 4.5, STOPT['joy'] + 6.6, 'OK... ONE MORE!')
    show('cyrus', STOPT['cyrus'] + 0.1, STOPT['cyrus'] + 2.6, 'TOO EASY!')
    show('cyrus', STOPT['cyrus'] + 5.0, STOPT['cyrus'] + 7.0, 'THANK YOU FANS!')
    if t >= T_NOTICE:
        for n in ['ray', 'joy', 'cyrus']:
            show(n, T_NOTICE if n == 'cyrus' else T_WIN, T_END, 'WAIT... WHAT?!')
    if T_WIN <= t < T_WIN + 0.9:
        x = MX(XF); y = lane_y(2)
        text_layer(img, [(x - 90, y - 250 - min(1, (t - T_WIN) / 0.3) * 20, 'WINNER!', 30, (255, 214, 60), 6, 255)])
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)].crop((0, 0, W, Y0)), (0, 0))
    if t < T_GO:
        if t >= 0.5:
            text_layer(img, [(W / 2, TY0 + 330, str(max(1, 3 - int((t - 0.5) / 0.6))), 120, (255, 214, 60), 10, 255)])
    elif t < T_GO + 0.6:
        text_layer(img, [(W / 2, TY0 + 330, 'GO!', 120, (120, 255, 120), 10, int(255 * (1 - (t - T_GO) / 0.6)))])
    # ticker
    TB0, TB1 = HB + 6, HB + 68
    layer(img, lambda dd: dd.rounded_rectangle([70, TB0, 1025, TB1], 14, fill=(14, 10, 24, 230)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, TB0, 1025, TB1], 14, outline=(255, 214, 60, 255), width=4)
    msg = [m for (tt, m) in TICK if tt <= t][-1]
    text_layer(img, [(W / 2 + 14, TB0 + 18, msg, 28, (255, 255, 255), 4, 255)])
    d.rectangle([88, TB0 + 23, 104, TB0 + 39], fill=(230, 50, 50, 255) if int(t * 3) % 2 else (120, 30, 30, 255))
    # finale
    if t >= T_WIN + 0.9:
        u = t - T_WIN - 0.9; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, HB + 70, W, H], fill=(10, 8, 18, int(170 * a))))
        vf = HVIC[int(u * 8) % len(HVIC)]
        if a > 0.2:
            img.alpha_composite(vf, (478 - vf.width // 2, 1150 - vf.height))
            text_layer(img, [(478, 1190, 'CLEO WINS!', 64, (255, 214, 60), 8, int(255 * a)),
                             (478, 1300, 'Slow and steady.', 34, (255, 255, 255), 6, int(255 * a)),
                             (478, 1365, 'Who did you pick?', 34, (255, 255, 255), 6, int(255 * a))])
            rr = random.Random(f)
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                cx_, cy_ = rr.uniform(80, 1010), (rr.uniform(0, 500) + u * 300) % 500 + HB + 90
                dl.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').save(OUT + f'p_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'ev55.json', 'w'))
print('done', round(T_END, 2), len(EV))
