import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image, ImageDraw, ImageEnhance
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a6'); OUT = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc15/v55/'
sys.path.insert(0, '../pixellab/safezone'); sys.path.insert(0, '../fork_rc2'); from rc2 import hook_layer2, acv_gloss, acv_tag
HK, HB = hook_layer2(['WHO WOULD WIN', 'THE RACE?'], accent=1, sub='PICK YOUR RUNNER!', sub_max=44); print('HB', HB)
KS = 4   # runners 3x -> 4x (review: ~1.4x bigger)
def MX(x): return 200 + (x - 120) * (620 / 852)
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
def lane_y(k): return TY0 + LH * (k + 0.5) + 102    # feet (lower in the lane so 4x heads clear the band)
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
ICON = {n: face(n, 28) for n in NAMES}
for k, n in enumerate(NAMES):
    ic = ICON[n]; GROUND.alpha_composite(ic, (100 - ic.width // 2, int(TY0 + LH * k + 14)))
# ---------------- sprites
SR = {g: seq(PL + f'race/{g}_run', KS) for g in ['joy', 'cyrus', 'cleo', 'ray']}
hw = Image.open(A + 'hollow-walk-side.gif'); HW = []
for i in range(hw.n_frames):
    hw.seek(i); f = hw.convert('RGBA').crop((290, 120, 610, 790)); k = 192 / 650
    HW.append(f.resize((int(f.width * k), int(f.height * k)), Image.NEAREST))
HEAT = seq(SP + 'fork3/hollow_eat', 3)
CBLK = seq(SP + 'fork_a4/cleo_block', KS)
RCAST = seq(SP + 'fork3/ray_cast', KS)
JCAST = seq(SP + 'fork_a3/joy_cast', KS, 1, 10)   # frames 10-12 show Joy's teeth: never used
CVIC = vic('cyrus', 300)
HVIC = vic('cleo', 360)
CWALK = [up(Image.open(f'../fork_a5/gen/cleo_walk/{i:02d}.png').convert('RGBA'), KS) for i in range(1, 9)]
GUM = {k: up(acv_gloss(Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')) if k == 'acv' else Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'), 3) for k in ('mush', 'cre', 'acv', 'mel')}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', KS) for g in ['cyrus', 'ray', 'joy']}
ROCK = up(Image.open('rock/08.png').convert('RGBA'), 4)
SLIME = seq(PL + 'race/slime_idle_c', 3)
SLIME_S = [up(f, 0.62) for f in SLIME]
STAND = {g: up(Image.open(SP + 'syeda_src/' + p).convert('RGBA'), KS) for g, p in {'joy': 'char1/char8.png', 'cyrus': 'char4/char10.png', 'cleo': 'char3/char7.png', 'ray': 'char2/char5.png'}.items()}
# ---------------- header bg (Liza castle)
HDR = bg_frames('vit_hd.gif', (W, 430), box=(0, 40, 1920, 40 + 764), step=2, bright=0.62)
# ---------------- timeline (content pass: more happens to every runner)
T_GO = 0.3
HV = 83.1                                   # Cleo's steady walk
CRE_X, ROCK_X, ACV_X, MUSH_X, MEL_X = 280, 480, 620, 250, 470
C_STOP = ROCK_X - 90
T_CRE = T_GO + (CRE_X - X0) / HV
T_SMASH0 = T_GO + (C_STOP - X0) / HV; T_SMASH1 = T_SMASH0 + 0.4; T_SMASH = T_SMASH0 + 0.15
T_ACV = T_SMASH1 + (ACV_X - C_STOP) / HV
T_WIN = T_SMASH1 + (XF - C_STOP) / HV
T_MUSH = T_GO + (MUSH_X - X0) / 390; T_CSTOP = T_MUSH + (800 - MUSH_X) / 760
T_RSTOP = T_GO + (330 - X0) / 300; T_JSTOP = T_GO + (520 - X0) / 320
T_BOOM = 5.6; T_ROCKET = T_BOOM - 1.0
T_SLEEP = T_WIN - 2.6; SLEEP_D = 1.2
T_RNOTICE = T_SLEEP - 0.9; T_RSTEP0, T_RSTEP1 = T_SLEEP - 0.6, T_SLEEP - 0.1
T_RRUN = T_SLEEP + 0.85
T_NOTICE = T_WIN - 0.75; T_CRUN = T_NOTICE + 0.55
T_END = T_WIN + 0.9 + 1.5; T_LOOP = T_END; T_ALL = T_END + 0.3
STRONG_END = T_SMASH1 + 0.3
print('T_WIN', round(T_WIN, 2), 'cre', round(T_CRE, 2), 'smash', round(T_SMASH, 2), 'acv', round(T_ACV, 2), 'sleep', round(T_SLEEP, 2))
def pos(n, t):
    if t < T_GO: return X0
    if n == 'cleo':
        if t < T_SMASH0: return X0 + (t - T_GO) * HV
        if t < T_SMASH1: return C_STOP
        return min(XF, C_STOP + (t - T_SMASH1) * HV)
    if n == 'cyrus':
        if t < T_MUSH: return X0 + (t - T_GO) * 390
        if t < T_CSTOP: return MUSH_X + (t - T_MUSH) * 760
        if t < T_CRUN: return 800
        return min(XF + 60, 800 + (t - T_CRUN) * 430)
    if n == 'ray':
        if t < T_RSTOP: return X0 + (t - T_GO) * 300
        if t < T_RSTEP0: return 330
        if t < T_RSTEP1: return 330 + (t - T_RSTEP0) / (T_RSTEP1 - T_RSTEP0) * (MEL_X - 330)
        if t < T_RRUN: return MEL_X
        return min(XF + 5, MEL_X + (t - T_RRUN) * 250)
    if n == 'joy':
        return min(520, X0 + (t - T_GO) * 320)
def fin_t(n):
    if n == 'cleo': return T_WIN
    if n == 'cyrus': return T_CRUN + (XF - 800) / 430
    if n == 'ray': return T_RRUN + (XF - MEL_X) / 250
    return 99
print('finish', {n: round(fin_t(n), 2) for n in NAMES})
def asleep(n, t): return n in ('joy', 'cyrus') and T_SLEEP <= t < T_SLEEP + SLEEP_D
EV = []
def ev(t, name):
    if not any(abs(e[0] - t) < 0.01 and e[1] == name for e in EV): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(T_GO, 'whoosh_8bit'); ev(0.1, 'cheer')
ev(T_MUSH, 'powerup_8bit'); ev(T_CRE, 'powerup2'); ev(T_SMASH, 'crunch_8bit'); ev(T_SMASH, 'punch')
ev(T_ACV, 'twinkle'); ev(T_ROCKET, 'whoosh_8bit'); ev(T_BOOM, 'boom'); ev(T_BOOM + 0.05, 'poofpops')
ev(T_SLEEP, 'poof'); ev(T_SLEEP + 0.05, 'powerup1'); ev(T_SLEEP + 0.15, 'boing'); ev(T_RRUN, 'swish')
FIREWORKS = [T_RSTOP + 0.6 + i * 1.15 for i in range(12) if T_RSTOP + 0.6 + i * 1.15 < T_RNOTICE - 0.3 and abs(T_RSTOP + 0.6 + i * 1.15 - T_ROCKET) > 0.5]
for f_ in FIREWORKS: ev(f_ + 0.35, 'poofpops')
HEALS = [T_JSTOP + 0.4 + i * 1.6 for i in range(10) if T_JSTOP + 0.4 + i * 1.6 < T_WIN + 2 and not (T_SLEEP - 0.9 <= T_JSTOP + 0.4 + i * 1.6 < T_SLEEP + SLEEP_D)]
for h in HEALS: ev(h + 0.5, 'chime')
ev(T_NOTICE, 'buzz_8bit'); ev(T_WIN, 'victory'); ev(T_WIN + 0.1, 'cheer'); ev(fin_t('cyrus'), 'ding_8bit'); ev(fin_t('ray'), 'ding_8bit')
TICK = [(0, 'PICK YOUR RUNNER!'), (1.0, 'CYRUS ATE A SPEED GUMMY!'), (1.9, 'RAYLEIGH STOPS FOR A SHOW?!'), (2.9, 'JOY IS HEALING A BABY SLIME'),
        (T_SMASH, 'CLEO SMASHES THE ROCK!'), (T_BOOM, 'BOOM! CYRUS GOT HIT!'), (T_BOOM + 1.1, 'CYRUS IS STILL SHOWING OFF'),
        (T_RNOTICE, 'WAIT. WHERE IS CLEO?'), (T_SLEEP, 'RAYLEIGH: SLEEP GUMMY!'), (T_SLEEP + 0.8, 'CLEO BLOCKED IT!'),
        (T_NOTICE, 'PHOTO FINISH!'), (T_WIN, 'CLEO WINS!')]
POPS = [(T_MUSH, 'cyrus', MUSH_X, 'SPEED!', (255, 160, 40)), (T_CRE, 'cleo', CRE_X, 'STRONG!', (90, 160, 255)),
        (T_SMASH, 'cleo', ROCK_X, 'SMASH!', (255, 255, 255)), (T_ACV, 'cleo', ACV_X, 'SHIELD!', (110, 230, 90)),
        (T_BOOM, 'cyrus', 800, 'BOOM!', (255, 110, 60)), (T_SLEEP, 'ray', MEL_X, 'SLEEP!', (190, 120, 255)),
        (T_SLEEP + 0.12, 'cleo', None, 'BLOCKED!', (110, 230, 90))]
GUMS = [('mush', 'cyrus', MUSH_X, T_MUSH), ('cre', 'cleo', CRE_X, T_CRE), ('acv', 'cleo', ACV_X, T_ACV), ('mel', 'ray', MEL_X, T_SLEEP)]
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
def aura(img, spr, x0, y0, col, a):
    tt = tinted(spr, col, a)
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
def bubble(img, x, y, text, a=255, col=(255, 255, 255)):
    f = F(44); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    w = d.textlength(text, font=f); bx0, by0 = int(x - w / 2 - 20), max(HB + 14, int(y - 74))
    bx0 = max(74, min((1021 if by0 + 80 < 1110 else 883) - w - 40, bx0))
    d.rounded_rectangle([bx0, by0, bx0 + w + 40, by0 + 72], 14, fill=(255, 255, 255, a), outline=(25, 20, 35, a), width=5)
    d.polygon([(x - 14, by0 + 70), (x + 14, by0 + 70), (x - 2, by0 + 92)], fill=(255, 255, 255, a), outline=(25, 20, 35, a))
    d.rectangle([x - 11, by0 + 64, x + 11, by0 + 70], fill=(255, 255, 255, a))
    d.text((bx0 + 20, by0 + 14), text, font=f, fill=(25, 20, 35, a))
    img.alpha_composite(L)
CROWD_T = [(x, Y0 + 92 + (i % 2) * 58) for i, x in enumerate(range(20, W, 76))]
CROWD_B = [(x, TY1 + 150 + (i % 2) * 70) for i, x in enumerate(range(40, W, 80))]
FLAGC = [RING[n] for n in NAMES]
NF = int(round(T_ALL * FPS))
ROCK_PIECES = [(random.Random(q).uniform(-1, 1), random.Random(q + 50).uniform(-1.3, -0.4), random.Random(q + 99).randint(14, 26)) for q in range(12)]
wr = Writer(OUT + 'v55_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    if t >= T_LOOP: t = 0.0                     # loop cut back to the opening
    img = GROUND.copy()
    hype = 1.6 if (t > T_WIN or t < 0.8) else 1.0
    for i, (x, y) in enumerate(CROWD_T + CROWD_B):
        fr = SLIME[(int(t * 10) + i * 3) % len(SLIME)]
        hop = int(abs(math.sin(t * 6 * hype + i * 1.3)) * 10 * hype)
        img.alpha_composite(fr, (int(x - fr.width / 2), int(y - fr.height + 30 - hop)))
        if i % 3 == 0:
            c = FLAGC[i % len(FLAGC)]; d = ImageDraw.Draw(img); px, py = x + 18, y - 40 - hop
            d.line([px, py, px, py + 34], fill=(70, 50, 30, 255), width=3)
            d.polygon([(px, py), (px + 24 + int(3 * math.sin(t * 8 + i)), py + 7), (px, py + 14)], fill=c + (255,))
    # gummies on the racing lines (each one gets eaten)
    for kind, n, gx, tp in GUMS:
        if t < tp:
            g = GUM[kind]; k = NAMES.index(n); bob = int(6 * math.sin(t * 4 + gx))
            gxs, gys = MX(gx), lane_y(k)
            layer(img, lambda dd, gxs=gxs, gys=gys: dd.ellipse([gxs - 26, gys - 8, gxs + 26, gys + 6], fill=(0, 0, 0, 60)))
            img.alpha_composite(g, (int(gxs - g.width / 2), int(gys - g.height - 22 + bob)))
        elif t - tp < 0.5:
            u = (t - tp) / 0.5; gxs, gys = MX(gx), lane_y(NAMES.index(n)) - 60
            col = {'mush': (255, 160, 40), 'cre': (90, 160, 255), 'acv': (110, 230, 90), 'mel': (190, 120, 255)}[kind]
            layer(img, lambda dd, gxs=gxs, gys=gys, u=u, col=col: [dd.rectangle([gxs + (20 + 120 * u) * math.cos(q * 0.628) - 7, gys + (20 + 120 * u) * math.sin(q * 0.628) - 7, gxs + (20 + 120 * u) * math.cos(q * 0.628) + 7, gys + (20 + 120 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    if 0.5 <= t < 2.3:   # ACV GUMMY tag on its first appearance (after the GO! stamp clears)
        acv_tag(img, int(MX(ACV_X)), int(lane_y(2) - 22 - GUM['acv'].height), a=int(255 * min(1, (t - 0.5) / 0.15, (2.3 - t) / 0.25)))
    # ray fireworks
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    rx = MX(pos('ray', t))
    for k, ft in enumerate(FIREWORKS):
        u = t - ft
        if 0 <= u < 1.4:
            cx, cy = MX(330) + 60 + (k % 3 - 1) * 140, lane_y(3) - 330 - (k % 2) * 90 - min(u, 0.35) * 200
            if u < 0.35:
                dl.rectangle([MX(330) + 30, lane_y(3) - 120 - u * 400, MX(330) + 38, lane_y(3) - 108 - u * 400], fill=(255, 230, 150, 255))
            else:
                v = u - 0.35; a = int(255 * max(0, 1 - v / 1.05))
                cols = [(255, 120, 220), (255, 214, 60), (190, 90, 240), (120, 220, 255)]
                for s_ in range(16):
                    ang = s_ * math.pi / 8; r = 30 + v * 240
                    sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang) + v * v * 40
                    dl.rectangle([sx - 8, sy - 8, sx + 8, sy + 8], fill=cols[(s_ + k) % 4] + (a,))
    # the stray rocket: Rayleigh's firework flies off course into Cyrus
    if T_ROCKET <= t < T_BOOM:
        u = (t - T_ROCKET) / (T_BOOM - T_ROCKET)
        x0_, y0_, x1_, y1_ = MX(330) + 46, lane_y(3) - 170, MX(800), lane_y(1) - 150
        for q in range(18, -1, -1):
            uu = max(0, u - q * 0.018)
            px_ = x0_ + (x1_ - x0_) * uu; py_ = y0_ + (y1_ - y0_) * uu - 200 * 4 * uu * (1 - uu)
            if q == 0:
                dl.ellipse([px_ - 30, py_ - 30, px_ + 30, py_ + 30], fill=(255, 220, 120, 110))
                dl.rectangle([px_ - 15, py_ - 15, px_ + 15, py_ + 15], fill=(255, 250, 220, 255), outline=(255, 90, 40, 255), width=4)
            else:
                sz = max(4, 13 - q * 0.5)
                dl.rectangle([px_ - sz, py_ - sz, px_ + sz, py_ + sz], fill=((255, 200, 80) if q % 2 else (255, 110, 50)) + (max(60, 255 - q * 10),))
    if T_BOOM <= t < T_BOOM + 0.8:
        v = (t - T_BOOM) / 0.8; cx, cy = MX(800), lane_y(1) - 150
        if v < 0.25: dl.ellipse([cx - 40 - 300 * v, cy - 40 - 300 * v, cx + 40 + 300 * v, cy + 40 + 300 * v], fill=(255, 240, 200, int(230 * (1 - v / 0.25))))
        cols = [(255, 120, 60), (255, 214, 60), (255, 80, 80), (255, 255, 255)]
        for s_ in range(20):
            ang = s_ * math.pi / 10 + 0.2; r = 40 + v * 260
            sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.8 + v * v * 60
            dl.rectangle([sx - 9, sy - 9, sx + 9, sy + 9], fill=cols[s_ % 4] + (int(255 * (1 - v)),))
    img.alpha_composite(L)
    # sleep wave from Rayleigh
    if T_SLEEP <= t < T_SLEEP + 0.7:
        u = (t - T_SLEEP) / 0.7; cx, cy = MX(MEL_X), lane_y(3) - 120
        layer(img, lambda dd: [dd.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1300 * u, 20 + 900 * u)])
    # runners, back lanes first
    for k, n in enumerate(NAMES):
        x = MX(pos(n, t)); y = lane_y(k); dy = 0
        layer(img, lambda dd: dd.ellipse([x - 42, y - 10, x + 42, y + 10], fill=(0, 0, 0, 70)))
        if n == 'cleo':
            # the rock in her lane
            if t < T_SMASH:
                rxs = MX(ROCK_X); img.alpha_composite(ROCK, (int(rxs - ROCK.width / 2), int(y - ROCK.height + 12)))
            elif t < T_SMASH + 0.7:
                u = (t - T_SMASH) / 0.7; rxs = MX(ROCK_X)
                layer(img, lambda dd, u=u, rxs=rxs: [dd.rectangle([rxs + vx * 260 * u - sz, y - 60 + vy * 300 * u + 500 * u * u - sz, rxs + vx * 260 * u + sz, y - 60 + vy * 300 * u + 500 * u * u + sz], fill=(118, 108, 92, int(255 * (1 - u ** 3)))) for vx, vy, sz in ROCK_PIECES])
            if t < T_GO: spr = CWALK[int(t * 10) % len(CWALK)]
            elif t >= T_WIN: spr = STAND['cleo']
            elif T_SMASH0 <= t < T_SMASH1: spr = CBLK[min(len(CBLK) - 1, int((t - T_SMASH0) / 0.4 * len(CBLK)))]
            else: spr = CWALK[int(t * 8) % len(CWALK)]
        elif asleep(n, t):
            spr = STAND[n]
        elif n == 'cyrus':
            if t < T_GO: spr = SR[n][int(t * 14) % 8]
            elif t < T_CSTOP or t >= T_CRUN: spr = SR[n][int(t * (20 if t < T_CSTOP and t > T_MUSH else 16)) % 8]
            elif T_BOOM <= t < T_BOOM + 1.0: spr = PANIC['cyrus'][int(t * 12) % len(PANIC['cyrus'])]; dy = -int(60 * math.sin(min(1, (t - T_BOOM) / 0.5) * math.pi))
            elif T_SLEEP + SLEEP_D <= t < T_SLEEP + SLEEP_D + 0.35 or T_NOTICE <= t: spr = STAND['cyrus']
            else: spr = CVIC[int((t - T_CSTOP) * 8) % len(CVIC)]
        elif n == 'ray':
            if t < T_GO: spr = SR[n][int(t * 14) % 8]
            elif t < T_RSTOP or T_RSTEP0 <= t < T_RSTEP1 or t >= T_RRUN: spr = SR[n][int(t * (16 if t >= T_RRUN else 12)) % 8]
            elif t < T_RNOTICE: spr = RCAST[int((t - T_RSTOP) * 10) % len(RCAST)]
            elif t < T_RSTEP0: spr = STAND['ray']
            else: spr = RCAST[min(len(RCAST) - 1, int((t - T_RSTEP1) * 12))] if t >= T_SLEEP else STAND['ray']
        else:  # joy
            if t < T_JSTOP: spr = SR[n][int(t * 14) % 8]
            else: spr = JCAST[int((t - T_JSTOP) * 8) % len(JCAST)]
        if n == 'cyrus' and spr in CVIC: y0 = int(y - spr.height + 5)
        else: y0 = int(y - spr.height + 14 * KS)
        x0 = int(x - spr.width / 2); y0 += dy
        if n == 'cyrus' and T_MUSH <= t < T_CSTOP + 0.3:      # SPEED: afterimages, speed lines, dust
            for q in range(4):
                gx2 = MX(max(X0, pos(n, t - (q + 1) * 0.05)))
                img.alpha_composite(tinted(spr, (255, 170, 50), int(255 * (0.4 - 0.08 * q))), (int(gx2 - spr.width / 2), y0))
            layer(img, lambda dd: [dd.rectangle([x - 90 - 40 * q - (q * 37 + int(t * 90)) % 60, y - 200 + q * 45 - 5, x - 90 - 40 * q + 70, y - 200 + q * 45 + 5], fill=(255, 240, 200, 210)) for q in range(4)] +
                                  [dd.ellipse([x - 40 - q * 34 - 18, y - 16 - q * 5, x - 40 - q * 34 + 18, y + 10], fill=(210, 190, 150, 170 - q * 40)) for q in range(3)])
        if n == 'cleo' and T_CRE <= t < STRONG_END:
            aura(img, spr, x0, y0, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
        if asleep(n, t):
            img.alpha_composite(spr, (x0, y0)); img.alpha_composite(tinted(spr, (40, 20, 90), 130), (x0, y0))
            u = t - T_SLEEP
            text_layer(img, [(x + 64 + 22 * kz, y - 190 - ((u * 1.4 + kz * 0.33) % 1) * 60 - kz * 16, 'Z', 34 + 10 * kz, (220, 200, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        else:
            img.alpha_composite(spr, (x0, y0))
        if n == 'cyrus' and T_BOOM <= t < T_BOOM + 1.0:   # dizzy stars
            layer(img, lambda dd: [dd.polygon([(x + 50 * math.cos(t * 9 + q * 2.09) + ddx_ * 1.4, y0 + 93 + dy * 0 + 14 * math.sin(t * 9 + q * 2.09) + ddy_ * 1.4) for ddx_, ddy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])
        if n == 'cleo' and T_ACV <= t < T_SLEEP + 0.12:   # ACV shield bubble
            layer(img, lambda dd: (dd.ellipse([x - 122, y - 330, x + 122, y + 26], fill=(110, 230, 90, 55), outline=(150, 255, 120, 230), width=8),
                                   dd.arc([x - 88, y - 300, x - 8, y - 200], 200, 260, fill=(230, 255, 220, 230), width=6)))
        if n == 'cleo' and T_SLEEP + 0.12 <= t < T_SLEEP + 0.6:   # bubble pops
            u = (t - T_SLEEP - 0.12) / 0.48
            layer(img, lambda dd: [dd.rectangle([x + (122 + 90 * u) * math.cos(q * 0.524) - 7, y - 152 + (170 + 90 * u) * math.sin(q * 0.524) - 7, x + (122 + 90 * u) * math.cos(q * 0.524) + 7, y - 152 + (170 + 90 * u) * math.sin(q * 0.524) + 7], fill=(150, 255, 120, int(255 * (1 - u)))) for q in range(12)])
        # Joy's queue of baby slimes
        if n == 'joy' and t >= T_JSTOP:
            u = t - T_JSTOP
            for q in range(5):
                qx = x - 150 - q * 70 + min(1, (u % 1.6) / 1.6) * 70 * (1 if q > 0 else 0)
                if q == 0: qx = x - 130
                fr = SLIME_S[(int(t * 10) + q) % len(SLIME_S)]
                img.alpha_composite(fr, (int(qx - fr.width / 2), int(y - fr.height + 18 - abs(math.sin(t * 7 + q)) * 8)))
            for h in HEALS:
                v = t - h
                if 0 <= v < 0.9:
                    text_layer(img, [(x - 130, y - 150 - v * 60, '+HP', 44, (120, 255, 120), 5, int(255 * (1 - v / 0.9)))])
        # Cyrus hearts from fans while he shows off
        if n == 'cyrus' and T_CSTOP <= t < T_NOTICE and not asleep(n, t) and not (T_BOOM <= t < T_BOOM + 1.0):
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for s_ in range(5):
                ph = (t * 0.7 + s_ * 0.21) % 1.0
                hx = x - 120 + s_ * 60 + 10 * math.sin(t * 3 + s_); hy = Y0 + 150 + ph * (y - Y0 - 240)
                a = int(255 * (1 - abs(ph - 0.5) * 2) ** 0.5)
                for (ddx_, ddy_) in ((-6, -3), (6, -3), (0, 3), (-3, 0), (3, 0), (0, 6)):
                    dl.rectangle([hx + ddx_ - 4, hy + ddy_ - 4, hx + ddx_ + 4, hy + ddy_ + 4], fill=(255, 100, 150, a))
            img.alpha_composite(L)
    if T_SLEEP <= t < T_SLEEP + 0.25:
        img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 60)))
    # speech bubbles (guides only)
    def show(n, t0, t1, text):
        if t0 <= t < t1:
            k = NAMES.index(n); a = int(255 * min(1, (t - t0) / 0.15, (t1 - t) / 0.15))
            bubble(img, int(MX(pos(n, t))), int(lane_y(k) - 290), text, a)
    show('cyrus', T_CSTOP + 0.1, T_CSTOP + 2.0, 'TOO EASY!')
    show('ray', T_ROCKET - 0.1, T_BOOM + 0.4, 'OOPS!')
    show('ray', T_RNOTICE, T_SLEEP - 0.05, 'WAIT... CLEO?!')
    # pop labels for every power / hit
    items = []
    for t0, n, wx, text, col in POPS:
        u = t - t0
        if 0 <= u < 1.0:
            k = NAMES.index(n); px_ = MX(wx if wx is not None else pos(n, t0) - 330); py_ = max(HB + 20, lane_y(k) - 345 - u * 30)
            sz = int(52 * (1 + 0.35 * max(0, 1 - u / 0.15))); wdt = len(text) * sz
            px_ = min(max(px_, 70 + wdt / 2 + 10), (1015 if py_ < 1110 else 877) - wdt / 2)
            items.append((px_, py_, text, sz, col, 8, int(255 * min(1, (1.0 - u) / 0.3))))
    if T_WIN <= t < T_WIN + 0.9:
        u = t - T_WIN; sc = 1 + 0.4 * max(0, 1 - u / 0.15)
        items.append((500, lane_y(2) - 200, 'WINNER!', int(68 * sc), (255, 214, 60), 9, 255))
    if items: text_layer(img, items)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)].crop((0, 0, W, Y0)), (0, 0))
    if t < 0.75:
        sc = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(W / 2, TY0 + 360, 'GO!', int(150 * sc), (120, 255, 120), 10, int(255 * min(1, (0.75 - t) / 0.3)))])
    # ticker

    # finale
    if t >= T_WIN + 0.9:
        u = t - T_WIN - 0.9; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, HB, W, H], fill=(10, 8, 18, int(170 * a))))
        vf = HVIC[int(u * 8) % len(HVIC)]
        if a > 0.2:
            img.alpha_composite(vf, (478 - vf.width // 2, 1150 - vf.height))
            text_layer(img, [(478, 1190, 'CLEO WINS!', 64, (255, 214, 60), 8, int(255 * a)),
                             (478, 1290, 'SLOW AND STEADY.', 44, (255, 255, 255), 7, int(255 * a)),
                             (478, 1370, 'WHO DID YOU PICK?', 44, (255, 255, 255), 7, int(255 * a))])
            rr = random.Random(f)
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                cx_, cy_ = rr.uniform(80, 1010), (rr.uniform(0, 500) + u * 300) % 500 + HB + 20
                dl.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HK)
    wr.write(img)
    if f % 15 == 0 or f == NF - 1: img.convert('RGB').resize((270, 480)).save(OUT + f'p_{f:04d}.png')
    if os.environ.get('FULL') and any(abs(f / FPS - tt) < 0.5 / FPS for tt in (T_MUSH + 0.25, T_SMASH + 0.1, T_BOOM + 0.2, T_SLEEP + 0.15, T_WIN + 0.1, T_ACV + 0.3)):
        img.convert('RGB').save(OUT + f'k_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'ev55.json', 'w'))
print('done', round(T_ALL, 2), len(EV))
