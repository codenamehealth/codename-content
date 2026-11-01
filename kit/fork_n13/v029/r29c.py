# Recut of fork_sz26/r29.py (#29 Guide battle) for the review-recut pass.
# charge from frame 0, re-sim (sim29r.py) ~21s with Rayleigh winning, units 1x -> 2x, scoreboard numbers 40 -> 64px,
# typed gummy powers with stamps, OUT stamps, no gold gummy, 'COMMENT YOUR PICK' 52px in the hook band, loop back to the opening.
import sys, os
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S0 + 'fork1'); sys.path.insert(0, S0 + 'fork_rc_paused')
from common import *
import numpy as np
sys.path.insert(0, S0 + 'pixellab/safezone'); from hook import hook_fade
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
for _k, _v in (('PLAY', '1.4'), ('CD2', '1.5'), ('RC2', '38')): os.environ.setdefault(_k, _v)
os.environ.pop('BR', None)
from sim29d import sim, NAMES, NT, POWDUR, XNOTCH, YNOTCH, SHOVE_T, SHOVE_IMP, PLAY   # n13b: seed-31 sim + creatine shoves, branch BR after the creatine window
# Oct 29 hookfade pass: boxed band, 'COMMENT YOUR PICK' and the ACV GUMMY tag cut; scoreboard is an edge-to-edge strip
HOOK, HB = hook_fade(['PICK AN ARMY'], accent=0, size=80)   # n13: job hook (was GUIDE BATTLE, a label)
SB0, SB1 = HB + 8, HB + 112          # scoreboard
print('hook bottom', HB, 'scoreboard', SB0, SB1)
SEED = int(sys.argv[1])
FR, EV, END, LEAD, OUTS = sim(SEED, dur=26.0)
TEND = END[0]; WIN = NAMES[END[1]]
HOLD = 1.3; NTAIL = 6   # n13: NMAIN/NF set after the time map (speed ramp + break) below
print('winner', WIN, TEND, 'outs', OUTS)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
POW = {'mush': ('SPEED!', (255, 170, 50)), 'cre': ('STRENGTH!', (255, 90, 60)), 'mel': ('SLEEP!', (200, 130, 255)), 'acv': ('SHIELD!', (110, 230, 110))}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 40) for n in NAMES}; ICONG = {n: ImageEnhance.Brightness(ImageEnhance.Color(ICON[n]).enhance(0.15)).enhance(0.45) for n in NAMES}
ICONS = {n: face(n, 34) for n in NAMES}
RUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in NAMES}
RUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in RUN.items()}
ATK = {g: seq(PL + f'race/{g}_atk', 2, 0) for g in NAMES}                      # Syeda-based attack swing (as in #012), feet at (60,208) in the 2x canvas
ATKL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in ATK.items()}
ATK_D = 0.75 * PLAY
FOOT = 78 * 2
def gum_src(k):
    g0 = Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')
    if k == 'acv':   # gloss on Syeda's apple-shaped ACV gummy so it reads as a gummy
        gl = Image.new('RGBA', g0.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).arc([5, 7, 26, 29], 290, 350, fill=(255, 240, 230, 170), width=2)
        gl.putalpha(Image.fromarray(np.minimum(np.array(gl.getchannel('A')), np.array(g0.getchannel('A')))))
        g0.alpha_composite(gl)
    return g0
G = {k: up(gum_src(k), 3) for k in ['mush', 'acv', 'mel', 'cre']}
GI = {k: up(gum_src(k), 2) for k in ['mush', 'acv', 'mel', 'cre']}
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
VICF = vic(WIN, 440)
ZZ = Image.new('RGBA', (90, 70), (0, 0, 0, 0)); _d = ImageDraw.Draw(ZZ)
_d.text((4, 30), 'Z', font=F(32), fill=(235, 220, 255), stroke_width=5, stroke_fill=(40, 20, 70)); _d.text((44, 4), 'z', font=F(26), fill=(235, 220, 255), stroke_width=4, stroke_fill=(40, 20, 70))
# ground: PixelLab Wang dirt arena inside grass (same tileset), reshaped to the new arena
meta = json.load(open(SP + 'fork3/arena/meta.json')); sheet = Image.open(SP + 'fork3/arena/sheet.png').convert('RGBA'); TILE = {}
for tt in meta['tileset_data']['tiles']:
    c = tt['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = tt['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
GY0 = 448; GC, GR = 17, 24; CX, CY = 520, 1080
def low(i, j):
    x, y = i * 64 - 4, GY0 + j * 64
    return ((x - CX) / 520) ** 2 + ((y - CY) / 520) ** 2 < 1.0 + 0.12 * math.sin(i * 1.3 + j * 2.1)
CORN = [[low(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (40, 80, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * 64 - 4, GY0 + j * 64))
HDR = bg_frames('vit_hd.gif', (1707, 960), step=2, bright=0.7); HDR = [b.crop((420, 120, 1500, 600)) for b in HDR]
# ---------------- stamps: one at a time, never overlapping (queued up to ~0.8s, OUT stamps always shown)
SDUR = 0.9; STY = SB1 + 22; SGAP = 0.4; SCX = 540     # n13b: one stamp at a time, 0.4s apart, one fixed centred spot
req = []
for e in EV:
    if e[1] == 'gum': req.append((e[0], 'pow', NAMES[e[4]], e[5]))
    if e[1] == 'out' and e[0] < TEND - 0.05: req.append((e[0], 'out', NAMES[e[4]], None))
req.sort(); STAMPS = []
for (te, kind, who, k) in req:
    t0 = max([te] + [p[1] + SGAP for p in STAMPS])
    STAMPS.append((t0, t0 + SDUR, kind, who, k, 0))
print('stamps', [(round(s[0], 2), round(s[1], 2), s[2], s[3], s[4], s[5]) for s in STAMPS])
def stamp_layer(kind, who, k, u, dur, slot=0):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pop = 1.0 if u > 0.12 else 0.6 + 0.4 * u / 0.12
    a = int(255 * min(1, (dur - u) / 0.15))
    if kind == 'pow':
        txt, col = POW[k]; fs = 72; f = F(fs); tw = d.textlength(txt, font=f)
        ic = ICONS[who]; gi = GI[k]; w = ic.width + 14 + gi.width + 22 + tw + 48; h = 112
        while w > 800 and fs > 48:   # n8: STRENGTH! is 2 letters longer; shrink so the plate stays inside x70 (STRONG! stays 72px)
            fs -= 2; f = F(fs); tw = d.textlength(txt, font=f); w = ic.width + 14 + gi.width + 22 + tw + 48
        if txt == 'STRENGTH!' and not getattr(stamp_layer, 'said', 0): print('STRENGTH fs', fs, 'w', w, 'x0', SCX - w / 2); stamp_layer.said = 1
        x0 = SCX - w / 2; y0 = STY
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 18, fill=(14, 10, 24, int(a * 0.93)), outline=col + (a,), width=7)
        L.alpha_composite(ic, (int(x0 + 22), int(y0 + (h - ic.height) / 2)))
        L.alpha_composite(gi, (int(x0 + 22 + ic.width + 12), int(y0 + (h - gi.height) / 2)))
        d.text((x0 + 22 + ic.width + 14 + gi.width + 18, y0 + (h - fs) / 2), txt, font=f, fill=col + (a,), stroke_width=8, stroke_fill=(10, 6, 18, a))
    else:
        txt = LABEL[who] + ' IS OUT!'; f = F(64 if len(txt) <= 12 else 60); tw = d.textlength(txt, font=f); w = tw + 56; h = 112
        x0 = SCX - w / 2; y0 = STY
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 18, fill=(150, 20, 30, int(a * 0.95)), outline=(255, 255, 255, a), width=7)
        d.text((x0 + 28, y0 + (h - f.size) / 2), txt, font=f, fill=(255, 255, 255, a), stroke_width=8, stroke_fill=(40, 0, 6, a))
    if pop < 1:
        bb = L.getbbox(); c = L.crop(bb); c = c.resize((max(1, int(c.width * pop)), max(1, int(c.height * pop))), Image.NEAREST)
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.alpha_composite(c, (int((bb[0] + bb[2]) / 2 - c.width / 2), int((bb[1] + bb[3]) / 2 - c.height / 2)))
    return L
ACV_FIRST = next((e for e in [(g['t0'], g['x'], g['y']) for fr in FR for g in fr['gums'] if g['k'] == 'acv']), None)
conv_by_frame = {}
for e in EV:
    if e[1] == 'conv': conv_by_frame.setdefault(int(round(e[0] * FPS)), []).append(e)
ev = []; lastpoof = -1
# ======================= n13 (Oct 29): speed ramp over the shield stall + the break =======================
CYR = NAMES.index('cyrus'); RAYI = NAMES.index('ray')
B0F = next(f for f in range(len(FR)) if (FR[f]['T'] == CYR).sum() == 1 and ((FR[f]['T'] == 0) | (FR[f]['T'] == 2)).sum() == 0)      # 39 purple vs 1 orange
TB_SIM = B0F / FPS
RA, RB, RPEAK, RR = float(os.environ.get('RA', 12.3)), float(os.environ.get('RB', 14.7)), float(os.environ.get('RPEAK', 1.0)), 0.5
PB = float(os.environ.get('PB', 1.5))            # playback speed (sim s per output s); sim shove timings are tuned for PLAY=1.4
PRE = float(os.environ.get('PRE', 1.5))          # n13b: open mid-charge (sim 1.5s), whole battle played at PLAY x (no ramp)
TS = [PRE]
while TS[-1] + PB / FPS < TB_SIM - 1e-9: TS.append(TS[-1] + PB / FPS)
NB = len(TS)                                   # first output frame of the break (state = FR[B0F])
def s2o(ts):                                   # sim time -> output time
    for f in range(len(TS) - 1):
        if TS[f + 1] > ts: return (f + (ts - TS[f]) / (TS[f + 1] - TS[f])) / FPS
    return (NB - 1) / FPS + (ts - TS[-1])
def state(ts):
    fl = min(int(ts * FPS + 1e-6), len(FR) - 2); a = ts * FPS - fl
    if a < 1e-6: return FR[fl]
    A, B = FR[fl], FR[fl + 1]; o = dict(A)
    for k in ('X', 'Y', 'D'): o[k] = A[k] * (1 - a) + B[k] * a
    return o
# ---- the break (seconds from the break start)
P0 = FR[B0F]; CI = int(np.where(P0['T'] == CYR)[0][0]); PU = [i for i in range(len(P0['T'])) if i != CI]
TAU = 0.13
def decel(i, u):
    x = P0['X'][i] + P0['VX'][i] * TAU * (1 - math.exp(-u / TAU)); y = P0['Y'][i] + P0['VY'][i] * TAU * (1 - math.exp(-u / TAU))
    v = math.hypot(P0['VX'][i], P0['VY'][i]) * math.exp(-u / TAU); return x, y, v
CX0, CY0, _ = decel(CI, 9)                     # where the last orange soldier comes to a stop
U_DROP, U_LAND, U_GRAB, U_GO = 0.40, 0.74, 1.02, 1.37   # 0.4s standoff (39 vs 1 squared up) before the gummy drops
DIRX = 1 if CX0 > np.mean([P0['X'][i] for i in PU]) else -1     # n13b: he runs away from the army, out the nearer open side
GX, GY = CX0 + DIRX * 100, CY0                  # mushroom gummy lands just behind him (away from the army)
DROPH = 560; GRAV = 2 * DROPH / (U_LAND - U_DROP) ** 2
ACC, VMAX = 4000.0, 1100.0
XG = GX - DIRX * 8                                    # where he stands when he grabs it
def cyr_x(u):
    if u < U_LAND + 0.03: return decel(CI, u)[0]
    if u < U_GRAB:
        s = (u - U_LAND - 0.03) / (U_GRAB - U_LAND - 0.03); s = s * s * (3 - 2 * s); return CX0 + (XG - CX0) * s
    if u < U_GO: return XG + 2 * math.sin(u * 90)          # legs spinning in place
    s = u - U_GO; tv = VMAX / ACC
    return XG + DIRX * (0.5 * ACC * s * s if s < tv else 0.5 * ACC * tv * tv + VMAX * (s - tv))
U_EXIT = U_GO + 0.01
while -90 < cyr_x(U_EXIT) < W + 90: U_EXIT += 0.01
U_WIN = U_EXIT + 0.55
rr = random.Random(7)
TURN = {i: U_GRAB + 0.05 + rr.uniform(0, 0.4) for i in PU}
QM = sorted(PU, key=lambda i: P0['Y'][i])[:14]; QM = sorted(rr.sample(QM, 6), key=lambda i: P0['X'][i]); QT = {i: U_EXIT + 0.05 + k * 0.06 for k, i in enumerate(QM)}
NWIN = NB + int(round(U_WIN * FPS)); NMAIN = NWIN + int(round(HOLD * FPS)); NF = NMAIN + NTAIL
TWIN_OUT = NWIN / FPS
print('break: sim frame', B0F, 'out frame', NB, 'ramp saves', round(TB_SIM - NB / FPS, 2), 's | cyrus stop', round(CX0), round(CY0), '| exit u', round(U_EXIT, 2), 'win at', round(TWIN_OUT, 2), '| frames', NF, round(NF / FPS, 2))
BSTAMP = (U_GRAB, U_GRAB + SDUR)
STAMPS = []                                     # n13b: re-queue in OUTPUT seconds: one at a time, 0.4s apart
for (te, kind, who, k) in req:
    to = s2o(te); t0 = max([to] + [p[1] + SGAP for p in STAMPS])
    STAMPS.append((t0, t0 + SDUR, kind, who, k, 0))
print('stamps(out s)', [(round(p[0], 2), round(p[1], 2), p[2], p[3], p[4]) for p in STAMPS], '| break SPEED stamp at', round(NB / FPS + U_GRAB, 2))
QF = F(44)
def render(f, sound=False):
    global lastpoof
    tout = f / FPS
    brk = f >= NB; u = (f - NB) / FPS if brk else -1
    won = brk and u >= U_WIN
    if not brk:
        t = TS[f]; fr = state(t); sf = int(t * FPS + 1e-6)
        T, X, Y, VX, VY, DI, FL = fr['T'], fr['X'], fr['Y'], fr['VX'], fr['VY'], fr['D'], fr['FL']
        sh, spd, strong, asleep = fr['sh'], fr['spd'], fr['strong'], fr['asleep']; gums = fr['gums']
        units = []
        for i in range(len(T)):
            g = NAMES[T[i]]; ph = int(DI[i] / 22) % 8
            us = t - fr['PLT'][i]
            if 0 <= us < SHOVE_T:          # creatine shove: plant, swing (impact at SHOVE_IMP), hold the pose, then move on
                lf = fr['PLD'][i] < 0
                if us < ATK_D:
                    a_ = (ATKL if lf else ATK)[g][min(12, int(us / ATK_D * 13))]
                    units.append((X[i], Y[i], a_, i, (196 if lf else 60), 208)); continue
                units.append((X[i], Y[i], (RUNL if lf else RUN)[g][0], i)); continue
            units.append((X[i], Y[i], (RUNL if VX[i] < 0 else RUN)[g][ph if not asleep[T[i]] else 0], i))
        cnt = [int((T == k).sum()) for k in range(NT)]
    else:
        t = TB_SIM + u; fr = P0; T = P0['T']; FL = P0['FL'] * 0 - 9
        sh = np.zeros(NT, bool); spd = np.ones(NT); strong = np.zeros(NT, bool); asleep = np.zeros(NT, bool); gums = []
        units = []; X = {}; Y = {}
        cx_ = cyr_x(u)
        for i in PU:
            x, y, v = decel(i, u); X[i], Y[i] = x, y
            dist = P0['D'][i] + math.hypot(x - P0['X'][i], y - P0['Y'][i]); ph = int(dist / 22) % 8 if v > 40 else 0
            left = (P0['VX'][i] < 0) if u < TURN[i] else (cx_ < x)
            units.append((x, y, (RUNL if left else RUN)['ray'][ph], i))
        if u < U_EXIT:
            if u < U_LAND + 0.03:
                x, y, v = decel(CI, u); left = P0['VX'][CI] < 0 if u < 0.25 else DIRX > 0      # stops, turns to face the army
                ph = int((P0['D'][CI] + math.hypot(x - P0['X'][CI], y - P0['Y'][CI])) / 22) % 8 if v > 40 else 0
            elif u < U_GRAB:
                x = cyr_x(u); y = CY0; left = DIRX < 0; ph = int(abs(x - CX0) / 14) % 8
            elif u < U_GO:
                x = cyr_x(u); y = CY0; left = DIRX < 0; ph = int(u * FPS) % 8
            else:
                x = cyr_x(u); y = CY0; left = DIRX < 0; ph = int(abs(XG - x) / 40 + u * FPS) % 8
            X[CI], Y[CI] = x, y
            units.append((x, y, (RUNL if left else RUN)['cyrus'][ph], CI))
        cnt = [0] * NT; cnt[RAYI] = len(PU); cnt[CYR] = 1 if u < U_EXIT else 0
    img = GROUND.copy()
    def gl(d):
        for g in gums:
            r = 56 + 8 * math.sin(t * 5); d.ellipse([g['x'] - r, g['y'] - r - 14, g['x'] + r, g['y'] + r - 14], fill=(255, 230, 140, 80))
        if brk and U_LAND <= u < U_GRAB:
            r = 56 + 8 * math.sin(t * 5); d.ellipse([GX - r, GY - r - 14, GX + r, GY + r - 14], fill=(255, 230, 140, 80))
    layer(img, gl)
    for g in gums:
        gi = G[g['k']]; b = int(6 * math.sin(t * 4 + g['x']))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height / 2 - 14 + b)))
    if brk and U_DROP <= u < U_GRAB:      # the mushroom gummy drops in (gravity, one small bounce)
        gi = G['mush']
        if u < U_LAND: yy = GY - DROPH + 0.5 * GRAV * (u - U_DROP) ** 2
        elif u < U_LAND + 0.16: s_ = (u - U_LAND) / 0.16; yy = GY - 4 * 26 * s_ * (1 - s_)
        else: yy = GY
        k_ = max(0.25, 1 - (GY - yy) / DROPH)
        layer(img, lambda d: d.ellipse([GX - 30 * k_, GY + gi.height / 2 - 22 - 8 * k_, GX + 30 * k_, GY + gi.height / 2 - 22 + 8 * k_], fill=(0, 0, 0, int(90 * k_))))
        img.alpha_composite(gi, (int(GX - gi.width / 2), int(yy - gi.height / 2 - 14)))
    def under(d):
        for (x, y, spr, i, *_r) in units:
            d.ellipse([x - 36, y - 10, x + 36, y + 10], fill=(0, 0, 0, 80))
            if brk: continue
            if strong[T[i]]:
                r = 56 + 8 * math.sin(t * 14 + i); d.ellipse([x - r, y - r * 0.42, x + r, y + r * 0.42], fill=(255, 70, 30, 140), outline=(255, 150, 60, 255), width=7)
                for q in range(4):
                    a_ = (t * 2.2 + q * 0.25 + i * 0.37) % 1.0; sx = x + 40 * math.cos(q * 1.7 + i); sy = y - 20 - a_ * 110
                    d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 120 + int(100 * a_), 50, int(255 * (1 - a_))))
            if spd[T[i]] > 1:
                v = math.hypot(VX[i], VY[i]) or 1; ux, uy = VX[i] / v, VY[i] / v
                for q in (-1, 0, 1):
                    ox, oy = -uy * q * 22, ux * q * 22; L = 50 + 18 * (q == 0)
                    d.line([(x + ox - ux * 40, y - 60 + oy - uy * 40), (x + ox - ux * (40 + L), y - 60 + oy - uy * (40 + L))], fill=(255, 190, 80, 230), width=6)
        if brk and U_GRAB <= u < U_EXIT:     # SPEED!: speed lines behind him (he faces left)
            x, y = X[CI], Y[CI]; L0 = 50 if u < U_GO else 110
            for q in (-1, 0, 1):
                ox = (u * 400) % 14 if u < U_GO else 0
                d.line([(x - DIRX * (40 + ox), y - 60 + q * 22), (x - DIRX * (40 + ox + L0 + 18 * (q == 0)), y - 60 + q * 22)], fill=(255, 190, 80, 230), width=6)
    layer(img, under)
    # dust: kicked up during the wind-up, then a trail along the sprint
    if brk and u >= U_GRAB:
        puffs = []
        k0 = int(U_GRAB * FPS); k1 = int(min(u, U_EXIT) * FPS)
        for k in range(k0, k1 + 1, 2):
            uk = k / FPS; age = u - uk
            if age < 0 or age > 0.5: continue
            xk = cyr_x(uk); drift = 60 * age if uk < U_GO else 0
            puffs.append((xk - DIRX * (30 + drift), CY0, age / 0.5))
        for (px, py, a) in puffs:
            ds = up(DUST, 1.0 + 0.9 * a); al = ds.getchannel('A').point(lambda p_, a=a: int(p_ * 0.85 * (1 - a))); ds.putalpha(al)
            img.alpha_composite(ds, (int(px - ds.width / 2), int(py - ds.height + 14)))
    for u_ in sorted(units, key=lambda q: q[1]):
        x, y, spr, i = u_[:4]
        if len(u_) > 4: img.alpha_composite(spr, (int(x - u_[4]), int(y - u_[5])))
        else: img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if not brk and 0 <= t - FL[i] < 0.35:
            u_ = (t - FL[i]) / 0.35; big_ = strong[T[i]]
            ds = up(DUST, (1.4 if big_ else 1.1) + 1.0 * u_); al = ds.getchannel('A').point(lambda p, u_=u_: int(p * (1 - u_))); ds.putalpha(al)
            img.alpha_composite(ds, (int(x - ds.width / 2), int(y - ds.height + 14)))
    if not brk:
        def over(d):
            for (x, y, spr, i, *_r) in units:
                if sh[T[i]]: d.ellipse([x - 58, y - 140, x + 58, y + 14], fill=(110, 230, 110, 60), outline=(150, 255, 150, 230), width=4)
        layer(img, over)
        for (x, y, spr, i, *_r) in units:
            if asleep[T[i]] and i % 2 == 0:
                bob = int(8 * math.sin(t * 6 + i)); img.alpha_composite(ZZ, (int(x - 10), int(y - FOOT + 10 + bob)))
        if sound:
            psf = int(TS[f - 1] * FPS + 1e-6) if f > 0 else -1
            for k in range(psf + 1, sf + 1):
                if conv_by_frame.get(k) and tout - lastpoof > 0.22: ev.append((round(tout, 3), 'poof')); lastpoof = tout
        for (t0, t1, kind, who, k, slot) in STAMPS:
            uu = tout - t0
            if 0 <= uu < t1 - t0: img.alpha_composite(stamp_layer(kind, who, k, uu, t1 - t0, slot))
    else:
        if not won:
            def qd(d):
                for i in QM:
                    uq = u - QT[i]
                    if uq < 0: continue
                    sc = 1.0 if uq > 0.1 else 0.5 + 0.5 * uq / 0.1; fz = max(8, int(44 * sc)); x, y = X[i], Y[i]
                    d.text((x - fz / 2 + 4, y - FOOT - 6 - fz), '?', font=F(fz), fill=(255, 255, 255), stroke_width=6, stroke_fill=(20, 12, 34))
            layer(img, qd)
            uu = u - BSTAMP[0]
            if 0 <= uu < SDUR: img.alpha_composite(stamp_layer('pow', 'cyrus', 'mush', uu, SDUR, 0))
    img.alpha_composite(HDR[int(tout * 6) % len(HDR)], (0, 0))
    if won:
        uw = u - U_WIN; a = min(1, uw / 0.25)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * a))))
        vf = VICF[int(uw * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1440 - vf.height))
        text_layer(img, [(478, 800, LABEL[WIN] + ' WINS!', 64 if len(LABEL[WIN]) <= 5 else 56, (255, 214, 60), 9, 255)])
        cr = random.Random(f)
        def conf(d):
            for _ in range(50):
                x = cr.uniform(0, W); y = SB1 + (cr.uniform(0, H) + uw * 500) % (H - SB1)
                d.rectangle([x, y, x + 12, y + 12], fill=cr.choice([(255, 214, 60, 255), (255, 120, 120, 255), (120, 220, 120, 255), (150, 180, 255, 255)]))
        layer(img, conf)
    mx = max(cnt); leaders = [k for k in range(NT) if cnt[k] == mx]
    layer(img, lambda d: d.rectangle([0, SB0, W, SB1], fill=(12, 9, 22, 205)))
    cw = (1025 - 70) / 4; d = ImageDraw.Draw(img)
    for k, n in enumerate(NAMES):
        x0 = 70 + cw * k; ic = ICON[n] if cnt[k] else ICONG[n]
        img.alpha_composite(ic, (int(x0 + 8), int(SB0 + (SB1 - SB0 - ic.height) / 2)))
        d.text((x0 + 8 + ic.width + 8, SB0 + (SB1 - SB0 - 64) / 2), str(cnt[k]), font=F(64), fill=(RING[n] if cnt[k] else (110, 110, 120)), stroke_width=7, stroke_fill=(10, 6, 18))
        if len(leaders) == 1 and leaders[0] == k and f > 0:
            d.rounded_rectangle([x0 + 4, SB0 + 5, x0 + cw - 4, SB1 - 5], 14, outline=(255, 214, 60), width=6)
    img.alpha_composite(HOOK)
    return img
for e in EV:
    if e[1] == 'gum': ev.append((round(s2o(e[0]), 3), 'powerup_8bit'))
    if e[1] == 'shove': ev.append((round(s2o(e[0]), 3), 'punch'))
for (t0, t1, kind, who, k, slot) in STAMPS:
    if kind == 'out': ev.append((round(t0, 3), 'boom'))
TB_OUT = NB / FPS
ev += [(round(TB_OUT + U_LAND, 3), 'boing'), (round(TB_OUT + U_GRAB, 3), 'powerup_8bit'), (round(TB_OUT + U_GO, 3), 'whoosh_8bit'), (round(TWIN_OUT, 3), 'victory')]
if __name__ == '__main__':
    ONLY = os.environ.get('ONLY')
    if ONLY:
        for tt in ONLY.split(','):
            fi = int(round(float(tt) * FPS)); render(fi).convert('RGB').save(os.path.join(HERE, f'look/n_{float(tt):05.2f}.png'))
        sys.exit()
    os.makedirs(os.path.join(HERE, 'prevc'), exist_ok=True)
    w = Writer(os.path.join(HERE, 'v29c_noaudio.mp4'))
    F0 = render(0, True)
    for f in range(NF):
        img = F0 if (f == 0 or f >= NMAIN) else render(f, True)
        w.write(img)
        if f % 15 == 0: img.convert('RGB').resize((216, 384)).save(os.path.join(HERE, f'prevc/e_{f:04d}.png'))
    w.close(); json.dump({'events': sorted(ev)}, open(os.path.join(HERE, 'v29c_ev.json'), 'w')); print('done', NF, round(NF / FPS, 2), len(ev))
