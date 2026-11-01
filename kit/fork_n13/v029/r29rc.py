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
from sim29r import sim, NAMES, NT, POWDUR, XNOTCH, YNOTCH
# Oct 29 hookfade pass: boxed band, 'COMMENT YOUR PICK' and the ACV GUMMY tag cut; scoreboard is an edge-to-edge strip
HOOK, HB = hook_fade(['GUIDE BATTLE'], accent=0, size=80)
SB0, SB1 = HB + 8, HB + 112          # scoreboard
print('hook bottom', HB, 'scoreboard', SB0, SB1)
SEED = int(sys.argv[1])
FR, EV, END, LEAD, OUTS = sim(SEED)
TEND = END[0]; WIN = NAMES[END[1]]
HOLD = 1.3; NMAIN = int(round((TEND + HOLD) * FPS)); NTAIL = 6; NF = NMAIN + NTAIL
print('winner', WIN, TEND, 'outs', OUTS, 'dur', NF / FPS)
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
SDUR = 1.15; STY = SB1 + 22
req = []
for e in EV:
    if e[1] == 'gum': req.append((e[0], 'pow', NAMES[e[4]], e[5]))
    if e[1] == 'out' and e[0] < TEND - 0.05: req.append((e[0], 'out', NAMES[e[4]], None))
req.sort(); STAMPS = []; tfree = 0     # (t0, t1, kind, who, k, slot); OUT stamps land on time, in a second row if a power stamp is up
for (te, kind, who, k) in req:
    if kind == 'out':
        busy = [p for p in STAMPS if p[0] <= te < p[1]]
        STAMPS.append((te, te + SDUR, kind, who, k, 1 if busy else 0)); continue
    busy_until = max([p[1] for p in STAMPS] + [0])
    t0 = max(te, busy_until + 0.05)
    if t0 - te > 0.8 or t0 + SDUR > TEND: continue
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
        if txt == 'STRENGTH!' and not getattr(stamp_layer, 'said', 0): print('STRENGTH fs', fs, 'w', w, 'x0', 478 - w / 2); stamp_layer.said = 1
        x0 = 478 - w / 2; y0 = STY
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 18, fill=(14, 10, 24, int(a * 0.93)), outline=col + (a,), width=7)
        L.alpha_composite(ic, (int(x0 + 22), int(y0 + (h - ic.height) / 2)))
        L.alpha_composite(gi, (int(x0 + 22 + ic.width + 12), int(y0 + (h - gi.height) / 2)))
        d.text((x0 + 22 + ic.width + 14 + gi.width + 18, y0 + (h - fs) / 2), txt, font=f, fill=col + (a,), stroke_width=8, stroke_fill=(10, 6, 18, a))
    else:
        txt = LABEL[who] + ' IS OUT!'; f = F(64 if len(txt) <= 12 else 60); tw = d.textlength(txt, font=f); w = tw + 56; h = 112
        x0 = 478 - w / 2; y0 = STY + 126 * slot
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
def render(f, sound=False):
    global lastpoof
    t = f / FPS; sf = min(f, len(FR) - 1); fr = FR[sf]
    T, X, Y, VX, VY, DI, FL = fr['T'], fr['X'], fr['Y'], fr['VX'], fr['VY'], fr['D'], fr['FL']
    sh, spd, strong, asleep = fr['sh'], fr['spd'], fr['strong'], fr['asleep']
    won = t >= TEND
    img = GROUND.copy()
    def gl(d):
        for g in fr['gums']:
            r = 56 + 8 * math.sin(t * 5); d.ellipse([g['x'] - r, g['y'] - r - 14, g['x'] + r, g['y'] + r - 14], fill=(255, 230, 140, 80))
    layer(img, gl)
    for g in fr['gums']:
        gi = G[g['k']]; b = int(6 * math.sin(t * 4 + g['x']))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height / 2 - 14 + b)))
    # under-unit effects: shadows, STRONG aura
    def under(d):
        for i in range(len(T)):
            x, y = X[i], Y[i]; d.ellipse([x - 36, y - 10, x + 36, y + 10], fill=(0, 0, 0, 80))
            if strong[T[i]] and not won:
                r = 56 + 8 * math.sin(t * 14 + i); d.ellipse([x - r, y - r * 0.42, x + r, y + r * 0.42], fill=(255, 70, 30, 140), outline=(255, 150, 60, 255), width=7)
                for q in range(4):   # rising power sparks
                    a_ = (t * 2.2 + q * 0.25 + i * 0.37) % 1.0; sx = x + 40 * math.cos(q * 1.7 + i); sy = y - 20 - a_ * 110
                    d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 120 + int(100 * a_), 50, int(255 * (1 - a_))))
            if spd[T[i]] > 1 and not won:
                v = math.hypot(VX[i], VY[i]) or 1; ux, uy = VX[i] / v, VY[i] / v
                for q in (-1, 0, 1):
                    ox, oy = -uy * q * 22, ux * q * 22; L = 50 + 18 * (q == 0)
                    d.line([(x + ox - ux * 40, y - 60 + oy - uy * 40), (x + ox - ux * (40 + L), y - 60 + oy - uy * (40 + L))], fill=(255, 190, 80, 230), width=6)
    layer(img, under)
    order = np.argsort(Y)
    for i in order:
        g = NAMES[T[i]]; ph = int(DI[i] / 22) % 8
        spr = (RUNL if VX[i] < 0 else RUN)[g][ph if not (asleep[T[i]] and not won) else 0]
        img.alpha_composite(spr, (int(X[i] - spr.width / 2), int(Y[i] - FOOT)))
        if 0 <= t - FL[i] < 0.35:
            u = (t - FL[i]) / 0.35; big_ = strong[T[i]]
            ds = up(DUST, (1.4 if big_ else 1.1) + 1.0 * u); al = ds.getchannel('A').point(lambda p: int(p * (1 - u))); ds.putalpha(al)
            img.alpha_composite(ds, (int(X[i] - ds.width / 2), int(Y[i] - ds.height + 14)))
    # over-unit effects: SHIELD bubbles, SLEEP Zzz
    def over(d):
        for i in range(len(T)):
            x, y = X[i], Y[i]
            if sh[T[i]] and not won:
                d.ellipse([x - 58, y - 140, x + 58, y + 14], fill=(110, 230, 110, 60), outline=(150, 255, 150, 230), width=4)
    layer(img, over)
    for i in range(len(T)):
        if asleep[T[i]] and not won and i % 2 == 0:
            bob = int(8 * math.sin(t * 6 + i)); img.alpha_composite(ZZ, (int(X[i] - 10), int(Y[i] - FOOT + 10 + bob)))
    # conversion sounds
    if sound and not won:
        for e in conv_by_frame.get(sf, []):
            if t - lastpoof > 0.22: ev.append((round(t, 3), 'poof')); lastpoof = t
    # stamps
    for (t0, t1, kind, who, k, slot) in STAMPS:
        u = t - t0
        if 0 <= u < t1 - t0 and not won: img.alpha_composite(stamp_layer(kind, who, k, u, t1 - t0, slot))
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    if won:
        u = t - TEND; a = min(1, u / 0.25)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1440 - vf.height))
        text_layer(img, [(478, 800, LABEL[WIN] + ' WINS!', 64 if len(LABEL[WIN]) <= 5 else 56, (255, 214, 60), 9, 255)])
        cr = random.Random(f)
        def conf(d):
            for _ in range(50):
                x = cr.uniform(0, W); y = SB1 + (cr.uniform(0, H) + u * 500) % (H - SB1)
                d.rectangle([x, y, x + 12, y + 12], fill=cr.choice([(255, 214, 60, 255), (255, 120, 120, 255), (120, 220, 120, 255), (150, 180, 255, 255)]))
        layer(img, conf)
    # scoreboard
    cnt = [int((T == k).sum()) for k in range(NT)]; mx = max(cnt); leaders = [k for k in range(NT) if cnt[k] == mx]
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
    if e[1] == 'gum': ev.append((round(e[0], 3), 'powerup_8bit'))
for (t0, t1, kind, who, k, slot) in STAMPS:
    if kind == 'out': ev.append((round(t0, 3), 'boom'))
ev.append((round(TEND, 3), 'victory'))
os.makedirs(os.path.join(HERE, 'prev'), exist_ok=True)
w = Writer(os.path.join(HERE, 'v29_noaudio.mp4'))
F0 = render(0, True)
for f in range(NF):
    img = F0 if (f == 0 or f >= NMAIN) else render(f, True)
    w.write(img)
    if f % 15 == 0: img.convert('RGB').resize((216, 384)).save(os.path.join(HERE, f'prev/e_{f:04d}.png'))
w.close(); json.dump({'events': sorted(ev)}, open(os.path.join(HERE, 'v29_ev.json'), 'w')); print('done', round(NF / FPS, 2), len(ev))
