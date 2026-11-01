import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image, ImageDraw, ImageEnhance
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a6'); OUT = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n9/v55/'
sys.path.insert(0, '../pixellab/safezone'); sys.path.insert(0, '../fork_rc2'); from rc2 import hook_layer2, acv_gloss, acv_tag
from hook import hook_band
HK, HB = hook_band(['WHO WOULD WIN', 'THE RACE?'], accent=1); print('HB', HB)   # Oct 29: full-width strip, no box, no sub line
KS = 4   # runners 3x -> 4x (review: ~1.4x bigger)
def MX(x): return 200 + (x - 120) * (620 / 852)
rnd = random.Random(55)
# ---------------- ground: PixelLab Wang tiles, clay track inside grass
meta = json.load(open('track_meta.json')); sheet = Image.open('track_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
Y0 = 420; TS = 64; GC, GR = 17, 24   # 24 rows: grass now runs to the bottom edge (was a flat green strip below y1764)
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
# n9: Joy plays music with Syeda's own victory pose (staff sparkling), not the PixelLab joy_cast (Joy's face only as Syeda drew it)
JVIC = [up(f.resize((92, 92), Image.NEAREST), KS) for f in gif_frames(A + VIC['joy'])]
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
# ---------------- n9 (Oct 29 notes2): one distraction at a time
# Bennett: "too much chaos. the distractions need to be more obvious and happen one at a time... slimes dancing in a circle with joy
# playing a harp or something. a camera slime taking pics of cyrus. rayleigh falling asleep at the beginning in his bed then waking up".
# Beats: 0.3 GO (Rayleigh is still asleep in his bed on the start line) | 0.6 Cyrus SPEED gummy, zooms ahead | 1.1-3.0 a camera slime
# hops in front of him, flash flash flash, he stops to pose and keeps posing | 3.0-5.0 Joy stops, slimes hop down from the crowd and
# dance in a circle while she plays (music notes from her staff) | 5.1-6.2 Cleo: STRENGTH gummy, smashes the rock | 6.9-7.45 Rayleigh
# wakes ('!'), bed vanishes in a poof, he sprints | Cleo crosses first by a hair. Cut: SHIELD/SLEEP/BLOCKED, +HP, fireworks + OOPS
# rocket, hearts, SMASH!, the acv/mel gummies.
T_GO = 0.3
HV = 83.1
MUSH_X, CRE_X = 250, 518
C_STOP = 572; ROCK_X = C_STOP + 90
T_MUSH = T_GO + (MUSH_X - X0) / 390; CY_STOP = 640; T_CSTOP = T_MUSH + (CY_STOP - MUSH_X) / 760
T_CAM_IN0, T_CAM_IN1 = 1.0, 1.4
FLASHES = [1.6, 2.0, 2.35, 2.75]
JSTOP_X = 560; T_JSTOP = 3.0; JV = (JSTOP_X - X0) / (T_JSTOP - T_GO)
T_SLIME0, T_SLIME1 = 3.0, 3.5
NOTES_T0, NOTES_T1 = 3.2, 5.0
T_CRE = T_GO + (CRE_X - X0) / HV
T_SMASH0 = T_GO + (C_STOP - X0) / HV; T_SMASH1 = T_SMASH0 + 0.4; T_SMASH = T_SMASH0 + 0.15
STRONG_END = T_SMASH1 + 0.3
T_WIN = T_SMASH1 + (XF - C_STOP) / HV
T_WAKE = 6.9; T_POOF = 7.3; T_RRUN = 7.45
RV = (XF - X0) / (T_WIN + 0.7 - T_RRUN)      # n9 review2: Rayleigh is ~0.7s short when Cleo crosses, stops there (clear of her at the line)
T_END = T_WIN + 1.0; T_LOOP = T_END; T_ALL = T_END + 2 / FPS   # n9 review2: ~1s end hold, 2 start frames at the cut
print('T_WIN', round(T_WIN, 2), 'T_CRE', round(T_CRE, 2), 'smash', round(T_SMASH, 2), 'RV', round(RV, 1), 'cstop', round(T_CSTOP, 2))
def pos(n, t):
    if t < T_GO: return X0
    if n == 'cleo':
        if t < T_SMASH0: return X0 + (t - T_GO) * HV
        if t < T_SMASH1: return C_STOP
        return min(XF, C_STOP + (t - T_SMASH1) * HV)
    if n == 'cyrus':
        if t < T_MUSH: return X0 + (t - T_GO) * 390
        if t < T_CSTOP: return MUSH_X + (t - T_MUSH) * 760
        return CY_STOP
    if n == 'ray':
        if t < T_RRUN: return X0
        return X0 + (min(t, T_WIN) - T_RRUN) * RV
    if n == 'joy':
        return min(JSTOP_X, X0 + (t - T_GO) * JV)
EV = []
def ev(t, name):
    if not any(abs(e[0] - t) < 0.01 and e[1] == name for e in EV): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(0.1, 'cheer'); ev(T_GO, 'whoosh_8bit')
ev(T_MUSH, 'powerup_8bit'); ev(T_CAM_IN0 + 0.1, 'jump')
for fl in FLASHES: ev(fl, 'tick_8bit')
ev(FLASHES[0] + 0.05, 'twinkle')
ev(T_SLIME0 + 0.1, 'boing'); ev(3.4, 'chime'); ev(4.1, 'chime'); ev(4.8, 'chime')
ev(T_CRE, 'powerup2'); ev(T_SMASH, 'crunch_8bit'); ev(T_SMASH, 'punch')
ev(T_WAKE, 'boing'); ev(T_POOF, 'poof'); ev(T_RRUN, 'swish')
ev(T_WIN, 'victory'); ev(T_WIN + 0.1, 'cheer')
POPS = [(T_MUSH, 'cyrus', 560, 'SPEED!', (255, 160, 40)), (T_CRE, 'cleo', CRE_X, 'STRENGTH!', (255, 230, 90))]
GUMS = [('mush', 'cyrus', MUSH_X, T_MUSH), ('cre', 'cleo', CRE_X, T_CRE)]
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
def aura(img, spr, x0, y0, col, a):
    tt = tinted(spr, col, a)
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
CROWD_T = [(x, Y0 + 92 + (i % 2) * 58) for i, x in enumerate(range(20, W, 76))]
CROWD_B = [(x, TY1 + 150 + (i % 2) * 70) for i, x in enumerate(range(40, W, 80))]
FLAGC = [RING[n] for n in NAMES]
ROCK_PIECES = [(random.Random(q).uniform(-1, 1), random.Random(q + 50).uniform(-1.3, -0.4), random.Random(q + 99).randint(14, 26)) for q in range(12)]
# props (not characters): a little camera for the camera slime, pixel music notes for Joy's tune
def cam_img():
    im = Image.new('RGBA', (14, 11), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 2, 13, 10], fill=(20, 18, 26, 255)); d.rectangle([1, 3, 12, 9], fill=(70, 72, 86, 255)); d.rectangle([3, 0, 7, 2], fill=(20, 18, 26, 255))
    d.rectangle([4, 1, 6, 2], fill=(110, 112, 128, 255)); d.ellipse([3, 4, 9, 10], fill=(20, 18, 26, 255)); d.ellipse([4, 5, 8, 9], fill=(90, 150, 220, 255))
    d.point((5, 6), fill=(230, 245, 255, 255)); d.rectangle([10, 4, 12, 5], fill=(255, 240, 160, 255))
    return up(im, 6)
CAM = cam_img()
def note_img(col):
    im = Image.new('RGBA', (8, 11), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([4, 0, 5, 8], fill=(20, 16, 30, 255)); d.rectangle([5, 0, 7, 1], fill=(20, 16, 30, 255)); d.rectangle([6, 2, 7, 3], fill=(20, 16, 30, 255))
    d.ellipse([0, 6, 5, 10], fill=(20, 16, 30, 255)); d.ellipse([1, 7, 4, 9], fill=col + (255,)); d.rectangle([4, 1, 4, 7], fill=col + (255,))
    return up(im, 6)
NOTES = [note_img(c) for c in ((255, 214, 60), (120, 230, 120), (255, 140, 200), (140, 200, 255))]
CAMSL = [up(f, 4 / 3) for f in SLIME]          # 4x; n9 review2: comes in from the left, behind Cyrus's lane start, clear of the finish line
CVIC_CLEO = [up(f.resize((92, 92), Image.NEAREST), KS) for f in gif_frames(A + VIC['cleo'])]
DANCE = SLIME      # 3x, same as the crowd
bedf = [f.resize((128, 128), Image.NEAREST) for f in gif_frames(SP + 'pixellab/ray/rayleigh_sleeping_v3.gif')]
bb = bedf[0].getbbox()
for f in bedf[1:]:
    b2 = f.getbbox(); bb = (min(bb[0], b2[0]), min(bb[1], b2[1]), max(bb[2], b2[2]), max(bb[3], b2[3]))
BED = [up(f.crop(bb), 3) for f in bedf]; print('bed', BED[0].size)
BED_CX = 245
NF = int(round(T_ALL * FPS))
wr = Writer(OUT + 'v55_noaudio.mp4')
RING_C = (262, lane_y(0) + 8); RRX, RRY = 160, 62
for f in range(NF):
    t = f / FPS
    if t >= T_LOOP: t = 0.0
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
    for kind, n, gx, tp in GUMS:
        if t < tp:
            g = GUM[kind]; k = NAMES.index(n); bob = int(6 * math.sin(t * 4 + gx))
            gxs, gys = MX(gx), lane_y(k)
            layer(img, lambda dd, gxs=gxs, gys=gys: dd.ellipse([gxs - 26, gys - 8, gxs + 26, gys + 6], fill=(0, 0, 0, 60)))
            img.alpha_composite(g, (int(gxs - g.width / 2), int(gys - g.height - 22 + bob)))
        elif t - tp < 0.5:
            u = (t - tp) / 0.5; gxs, gys = MX(gx), lane_y(NAMES.index(n)) - 60
            col = {'mush': (255, 160, 40), 'cre': (90, 160, 255)}[kind]
            layer(img, lambda dd, gxs=gxs, gys=gys, u=u, col=col: [dd.rectangle([gxs + (20 + 120 * u) * math.cos(q * 0.628) - 7, gys + (20 + 120 * u) * math.sin(q * 0.628) - 7, gxs + (20 + 120 * u) * math.cos(q * 0.628) + 7, gys + (20 + 120 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    # ---- Joy's dance circle (behind the runners in lane 0): slimes hop down from the crowd, then circle and bounce
    if t >= T_SLIME0:
        sl = []
        for q in range(6):
            ang = 2 * math.pi * q / 6 + max(0, t - T_SLIME1) * 1.7
            tx, ty = RING_C[0] + RRX * math.cos(ang), RING_C[1] + RRY * math.sin(ang)
            u = min(1, (t - T_SLIME0 - q * 0.06) / 0.45)
            if u <= 0: continue
            sx0, sy0 = 100 + q * 110, Y0 + 130
            x_ = sx0 + (tx - sx0) * u; y_ = sy0 + (ty - sy0) * u - 120 * math.sin(math.pi * u)
            hop = abs(math.sin(t * 7 + q * 1.2)) * 26 if u >= 1 else 0
            sl.append((y_, x_, hop, q))
        for y_, x_, hop, q in sorted(sl):
            fr = DANCE[(int(t * 10) + q) % len(DANCE)]
            if q % 2: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (int(x_ - fr.width / 2), int(y_ - fr.height + 18 - hop)))
    # ---- Rayleigh asleep in his bed on the start line (drawn before the runners so it never covers Cleo)
    if t < T_POOF + 0.05:
        bf = BED[int(t * 8) % len(BED)] if t < T_WAKE else BED[0]
        bx, by = int(BED_CX - bf.width / 2), int(lane_y(3) + 16 - bf.height)
        img.alpha_composite(bf, (bx, by))
        if T_WAKE <= t < T_POOF + 0.05:
            u = t - T_WAKE; sc = 1 + 0.5 * max(0, 1 - u / 0.12)
            text_layer(img, [(bx + 90, by - 60 - 10 * math.sin(min(1, u / 0.15) * math.pi), '!', int(96 * sc), (255, 214, 60), 9, 255)])
    # ---- runners, back lanes first
    for k, n in sorted(enumerate(NAMES), key=lambda kn: (kn[1] == 'cleo' and t >= T_WIN - 1.5, kn[0])):   # n9 review2: Cleo in front of Rayleigh at the line
        x = MX(pos(n, t)); y = lane_y(k); dy = 0
        if n == 'ray' and t < T_POOF + 0.05: continue      # drawn above, as the bed
        layer(img, lambda dd: dd.ellipse([x - 42, y - 10, x + 42, y + 10], fill=(0, 0, 0, 70)))
        if n == 'cleo':
            if t < T_SMASH:
                rxs = MX(ROCK_X); img.alpha_composite(ROCK, (int(rxs - ROCK.width / 2), int(y - ROCK.height + 12)))
            elif t < T_SMASH + 0.7:
                u = (t - T_SMASH) / 0.7; rxs = MX(ROCK_X)
                layer(img, lambda dd, u=u, rxs=rxs: [dd.rectangle([rxs + vx * 260 * u - sz, y - 60 + vy * 300 * u + 500 * u * u - sz, rxs + vx * 260 * u + sz, y - 60 + vy * 300 * u + 500 * u * u + sz], fill=(118, 108, 92, int(255 * (1 - u ** 3)))) for vx, vy, sz in ROCK_PIECES])
            if t < T_GO: spr = CWALK[int(t * 10) % len(CWALK)]
            elif t >= T_WIN: spr = CVIC_CLEO[int((t - T_WIN) * 8) % len(CVIC_CLEO)]   # one Cleo: victory pose at the line
            elif T_SMASH0 <= t < T_SMASH1: spr = CBLK[min(len(CBLK) - 1, int((t - T_SMASH0) / 0.4 * len(CBLK)))]
            else: spr = CWALK[int(t * 8) % len(CWALK)]
        elif n == 'cyrus':
            if t < T_CSTOP: spr = SR[n][int(t * (20 if t > T_MUSH else 14)) % 8]
            else: spr = CVIC[int((t - T_CSTOP) * 8) % len(CVIC)]
        elif n == 'ray':
            spr = SR[n][int(t * 18) % 8] if T_RRUN <= t < T_WIN else STAND['ray']
        else:
            spr = SR[n][int(t * 12) % 8] if t < T_JSTOP else JVIC[int((t - T_JSTOP) * 8) % len(JVIC)]
        if n == 'cyrus' and spr in CVIC: y0 = int(y - spr.height + 5)
        elif (n == 'joy' and spr in JVIC) or (n == 'cleo' and spr in CVIC_CLEO): y0 = int(y - 78 * KS)
        else: y0 = int(y - spr.height + 14 * KS)
        x0 = int(x - spr.width / 2); y0 += dy
        if n == 'cyrus' and T_MUSH <= t < T_CSTOP + 0.3:
            for q in range(4):
                gx2 = MX(max(X0, pos(n, t - (q + 1) * 0.05)))
                img.alpha_composite(tinted(spr, (255, 170, 50), int(255 * (0.4 - 0.08 * q))), (int(gx2 - spr.width / 2), y0))
            layer(img, lambda dd: [dd.rectangle([x - 90 - 40 * q - (q * 37 + int(t * 90)) % 60, y - 200 + q * 45 - 5, x - 90 - 40 * q + 70, y - 200 + q * 45 + 5], fill=(255, 240, 200, 210)) for q in range(4)] +
                                  [dd.ellipse([x - 40 - q * 34 - 18, y - 16 - q * 5, x - 40 - q * 34 + 18, y + 10], fill=(210, 190, 150, 170 - q * 40)) for q in range(3)])
        if n == 'ray' and T_RRUN <= t < T_WIN:          # late sprint: dust behind him
            layer(img, lambda dd: [dd.ellipse([x - 50 - q * 36 - 18, y - 16 - q * 5, x - 50 - q * 36 + 18, y + 10], fill=(210, 190, 150, 170 - q * 40)) for q in range(3)])
        if n == 'cleo' and T_CRE <= t < STRONG_END:
            aura(img, spr, x0, y0, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
        img.alpha_composite(spr, (x0, y0))
        if n == 'cyrus' and t >= T_CAM_IN0:                     # camera slime in front of him
            u = min(1, (t - T_CAM_IN0) / (T_CAM_IN1 - T_CAM_IN0))
            cx = -120 + (x - 175 + 120) * u; hop = 70 * abs(math.sin(math.pi * u * 2)) if u < 1 else abs(math.sin(t * 5)) * 6
            fr = CAMSL[int(t * 10) % len(CAMSL)]
            img.alpha_composite(fr, (int(cx - fr.width / 2), int(y + 30 - fr.height - hop)))
            lx, ly = int(cx + 62), int(y - 38 - hop)      # held against its front (faces Cyrus, to its right)
            if cx + fr.width / 2 > 0: img.alpha_composite(CAM, (lx - CAM.width // 2, ly - CAM.height // 2))
            for fl in FLASHES:
                v = t - fl
                if 0 <= v < 0.22:
                    a = int(255 * (1 - v / 0.22)); r = 30 + 160 * v / 0.22
                    layer(img, lambda dd, a=a, r=r: (dd.ellipse([lx + 30 - r, ly - r, lx + 30 + r, ly + r], fill=(255, 255, 240, int(a * 0.55))),
                                                    [dd.line([(lx + 30, ly), (lx + 30 + math.cos(q * 0.785) * r * 1.6, ly + math.sin(q * 0.785) * r * 1.6)], fill=(255, 255, 255, a), width=6) for q in range(8)]))
        if n == 'joy' and NOTES_T0 <= t < NOTES_T1 + 0.25:       # her tune: notes float from the staff toward the dancers
            for q in range(6):
                v = ((t - NOTES_T0) * 0.9 + q / 6) % 1
                if t - NOTES_T0 < q * 0.16 or (t > NOTES_T1 and v < (t - NOTES_T1) / 0.25): continue
                nx = x + 40 + (RING_C[0] - x - 40) * v + 18 * math.sin(t * 4 + q); ny = y - 290 + (RING_C[1] - 190 - y + 290) * v + 22 * math.sin(v * 9 + q)
                nimg = NOTES[q % 4]; nimg2 = nimg.copy(); nimg2.putalpha(nimg.getchannel('A').point(lambda p, v=v: int(p * min(1, (1 - v) / 0.25, v / 0.1))))
                img.alpha_composite(nimg2, (int(nx - nimg.width / 2), int(ny - nimg.height / 2)))
    # Rayleigh's wake-up poof (bed vanishes, he's standing in the cloud)
    if T_POOF <= t < T_POOF + 0.5:
        u = (t - T_POOF) / 0.5; cx, cy = BED_CX, lane_y(3) - 110
        layer(img, lambda dd: [dd.ellipse([cx + math.cos(q * 1.047) * (40 + 120 * u) - 70, cy + math.sin(q * 1.047) * (30 + 70 * u) - 60, cx + math.cos(q * 1.047) * (40 + 120 * u) + 70, cy + math.sin(q * 1.047) * (30 + 70 * u) + 60], fill=(235, 230, 245, int(230 * (1 - u)))) for q in range(6)])
    items = []
    for t0, n, wx, text, col in POPS:
        u = t - t0
        if 0 <= u < 1.0:
            k = NAMES.index(n); px_ = MX(wx); py_ = max(HB + 20, lane_y(k) - 345 - u * 30)
            sz = int(52 * (1 + 0.35 * max(0, 1 - u / 0.15))); wdt = len(text) * sz
            px_ = min(max(px_, 70 + wdt / 2 + 10), (1015 if py_ < 1110 else 877) - wdt / 2)
            items.append((px_, py_, text, sz, col, 8, int(255 * min(1, (1.0 - u) / 0.3))))
    if t >= T_WIN:
        u = t - T_WIN; sc = 1 + 0.4 * max(0, 1 - u / 0.15)
        items.append((400, 1420, 'CLEO WINS!', int(58 * sc), (255, 214, 60), 9, 255))
    if items: text_layer(img, items)
    img.alpha_composite(HDR[int(t * 6) % len(HDR)].crop((0, 0, W, Y0)), (0, 0))
    if t < 0.75:
        sc = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(W / 2, TY0 + 360, 'GO!', int(150 * sc), (120, 255, 120), 10, int(255 * min(1, (0.75 - t) / 0.3)))])
    if False:
        u = t - T_WIN - 0.9; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, HB, W, H], fill=(10, 8, 18, int(170 * a))))
        vf = HVIC[int(u * 8) % len(HVIC)]
        if a > 0.2:
            img.alpha_composite(vf, (478 - vf.width // 2, 1150 - vf.height))
            text_layer(img, [(478, 1190, 'CLEO WINS!', 64, (255, 214, 60), 8, int(255 * a))])
            rr = random.Random(f)
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                cx_, cy_ = rr.uniform(80, 1010), (rr.uniform(0, 500) + u * 300) % 500 + HB + 20
                dl.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    if t >= T_WIN:      # confetti over the finish
        u = t - T_WIN; rr = random.Random(f)
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for _ in range(40):
            cx_, cy_ = rr.uniform(80, 1010), (rr.uniform(0, 700) + u * 300) % 700 + HB + 20
            dl.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
        img.alpha_composite(L)
    img.alpha_composite(HK)
    wr.write(img)
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'ev55.json', 'w'))
print('done', round(T_ALL, 2), NF, len(EV))
