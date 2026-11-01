# #20 Never give up -- review recut (fork_rc4). 7x7 board, pieces 3x, motion from frame 0, story stamps, loop.
import sys, os, math, json
os.environ.setdefault('NB', '7'); os.environ.setdefault('WL', '5')
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
OUT = SP_ + 'fork_hfg1/v20/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_band
sys.path.insert(0, OUT)
from sim import dist, N
from sim2 import play2, trace, P0
# Oct 29 pass: full-width strip (busy tiled floor behind it), 'WOULD YOU QUIT?' sub cut (caption asks)
HOOK, HB = hook_band(['NEVER GIVE UP'], accent=0)
print('hook bottom', HB)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 43
PREVIEW = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
P0['trig'] = 1
WIN, LOG, LEFT = play2(SEED, P0); assert WIN == 'hollow'
TR = trace(LOG)
I_LEAD = next(i for i, (h, c) in enumerate(TR) if h <= 1)
I_TRAP = next(i for i, e in enumerate(LOG) if i > I_LEAD and e[0] == 'wall' and e[1] == 'cyrus')
I_CLUTCH = next(i for i, e in enumerate(LOG) if i > I_TRAP and e[0] == 'wall' and e[1] == 'hollow')
I_CLUTCH2 = next((i for i, e in enumerate(LOG) if i > I_CLUTCH and e[0] == 'wall' and e[1] == 'hollow'), None)
print('beats', I_LEAD, I_TRAP, I_CLUTCH, I_CLUTCH2, 'turns', len(LOG))
WL0 = int(os.environ['WL'])
K = 3                                   # piece scale (was 2)
CS = 104; BW = N * CS - 8               # cell pitch, board width (728)
X0 = 478 - BW // 2; Y0 = 620; DY = Y0 - 704            # board centred in the lower safe column (x<887 below y1110)
BCX = X0 + BW // 2
def cell_c(r, c): return X0 + c * CS + (CS - 8) // 2, Y0 + r * CS + (CS - 8) // 2
G = SP_ + 'fork_a2/gen/'
def pk(k, i): return crop(Image.open(f'{G}{k}/{i:02d}.png').convert('RGBA'))
TL = up(pk('floor', 4), 3); TD = up(pk('floor', 12), 3)
TL = TL.resize((CS - 8, CS - 8), Image.NEAREST); TD = TD.resize((CS - 8, CS - 8), Image.NEAREST)
WA = pk('wall_amber', 2); WV = pk('wall_violet', 2)
WLEN = 2 * CS - 4
def wall_spr(im, o):
    s = im.resize((WLEN, max(1, int(im.height * WLEN / im.width))), Image.NEAREST)
    return s if o == 'h' else s.transpose(Image.ROTATE_90)
WS = {('cyrus', 'h'): wall_spr(WA, 'h'), ('cyrus', 'v'): wall_spr(WA, 'v'), ('hollow', 'h'): wall_spr(WV, 'h'), ('hollow', 'v'): wall_spr(WV, 'v')}
def wall_xy(w):
    r, c, o = w; return X0 + (c + 1) * CS - 4, Y0 + (r + 1) * CS - 4
ICONW = {'cyrus': up(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'), 1.5), 'hollow': up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 1.5)}
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
BG = None and bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.55, blur=3)
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
# Oct 29 full-bleed: the floor tiles run edge to edge on the same grid (no board box over a dimmed, blurred temple);
# outside the 7x7 play area the tiles are darker, the play area keeps a gold edge
bd.rectangle([0, 0, W, H], fill=(46, 30, 22, 255))
for r in range(-((Y0 + CS - 1) // CS), (H - Y0) // CS + 1):
    for c in range(-((X0 + CS - 1) // CS), (W - X0) // CS + 1):
        BOARD.alpha_composite(TL if (r + c) % 2 == 0 else TD, (X0 + c * CS, Y0 + r * CS))
_dim = Image.new('RGBA', (W, H), (14, 8, 6, 85)); ImageDraw.Draw(_dim).rectangle([X0 - 8, Y0 - 8, X0 + BW + 7, Y0 + BW + 7], fill=(0, 0, 0, 0))
BOARD.alpha_composite(_dim)
ImageDraw.Draw(BOARD).rectangle([X0 - 14, Y0 - 14, X0 + BW + 13, Y0 + BW + 13], outline=(255, 214, 60, 255), width=6)
def tint_row(r, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).rectangle([X0, Y0 + r * CS, X0 + BW, Y0 + r * CS + CS - 8], fill=col)
    BOARD.alpha_composite(L)
tint_row(0, (170, 90, 255, 80)); tint_row(N - 1, (255, 150, 40, 80))
for c in range(N):
    if c % 2 == 0:
        g1 = up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 1.25); g2 = up(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'), 1.25)
        BOARD.alpha_composite(g1, (X0 + c * CS + (CS - 8 - g1.width) // 2, Y0 + 6))
        BOARD.alpha_composite(g2, (X0 + c * CS + (CS - 8 - g2.width) // 2, Y0 + (N - 1) * CS + CS - 8 - g2.height - 6))
# Oct 29: '1 WALL = 1 GUMMY' rule plate cut (the HUD gummies drop as walls go up)
RULE = Image.new('RGBA', (W, H), (0, 0, 0, 0))
SRUN_H = seq(PL + 'maze/anim/hollow_srun', K); SRUN_C = seq(PL + 'race/cyrus_run', K)
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', K) for g in ('hollow', 'cyrus')}
IDL = {'hollow': idle('hollow', K), 'cyrus': idle('cyrus', K)}
ATK = seq(PL + 'race/cyrus_atk', K)
FOOTY = 78 * K
ICON = {}
for g, src in (('hollow', 'hollow/char1.png'), ('cyrus', 'char4/char9.png')):
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = vic('hollow', 380)
# ---------------- timeline: moves are quick, walls get time (no metronome)
TMOVE, TWALL, HOLD = 0.30, 0.55, 1.0
HOLD_K = I_TRAP
starts = []; t_ = 0.0
for i, e in enumerate(LOG):
    if i == HOLD_K: t_ += HOLD
    starts.append(t_); t_ += TWALL if e[0] == 'wall' else TMOVE
T_END = t_; WINHOLD = 1.5; RESET = 0.55; DUR = T_END + WINHOLD + RESET
T_HOLD0 = starts[HOLD_K] - HOLD
print('1-step hold at', round(T_HOLD0, 2), 'walled in', round(starts[I_TRAP], 2), 'comeback', round(starts[I_CLUTCH], 2), 'win', round(T_END, 2), 'dur', round(DUR, 2))
def kt(t):
    if t >= T_END: return len(LOG), 1, False
    if T_HOLD0 <= t < starts[HOLD_K]: return HOLD_K, 0, True
    k = max(i for i in range(len(LOG)) if starts[i] <= t)
    d = TWALL if LOG[k][0] == 'wall' else TMOVE
    return k, min(1, (t - starts[k]) / d), False
state = {'hollow': (N - 1, N // 2), 'cyrus': (0, N // 2)}; walls = []; left = {'hollow': WL0, 'cyrus': WL0}
START = dict(state)
steps = []
for i, e in enumerate(LOG):
    steps.append((dict(state), list(walls), dict(left), e))
    if e[0] == 'move': state[e[1]] = e[3]
    elif e[0] == 'wall': walls.append((e[1], e[2])); left[e[1]] -= 1
FINAL = (dict(state), list(walls), dict(left))
# stamps: (t0, t1, lines, size, colour, anchor y)  -- one at a time, placed away from the pieces
def free_y(k):
    st = steps[min(k, len(steps) - 1)][0]; rows = [st['hollow'][0], st['cyrus'][0]]
    # choose top band (rows 0-1) or bottom band (rows 5-6) whichever is farther from both pieces
    top = min(abs(r - 0.5) for r in rows); bot = min(abs(r - 5.5) for r in rows)
    return Y0 + 70 if top > bot else Y0 + BW - 230
STAMPS = [
    (T_HOLD0, starts[HOLD_K], ['1 STEP LEFT...'], 64, (255, 214, 60), free_y(HOLD_K)),
    (starts[I_TRAP] + 0.25, starts[I_TRAP] + 1.85, ['WALLED IN!'], 76, (255, 80, 80), free_y(I_TRAP + 2)),
    (starts[I_CLUTCH] + 0.2, starts[I_CLUTCH] + 1.6, ['COMEBACK!'], 76, (130, 240, 110), free_y(I_CLUTCH + 1)),
]
if I_CLUTCH2: STAMPS.append((starts[I_CLUTCH2] + 0.2, starts[I_CLUTCH2] + 1.0, ['BLOCKED!'], 76, (130, 240, 110), free_y(I_CLUTCH2 + 1)))
for a, b in zip(STAMPS, STAMPS[1:]): assert a[1] <= b[0], ('stamp overlap', a, b)
def stamp_layer(img, t):
    for t0, t1, lines, sz, col, y in STAMPS:
        if not (t0 <= t < t1): continue
        u = t - t0; sc = 1.0 + 0.35 * max(0, 1 - u / 0.12)          # hard pop
        a = 255 if t1 - t > 0.12 else int(255 * (t1 - t) / 0.12)
        f = F(int(sz * sc)); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        ws = [d.textlength(l, font=f) for l in lines]; lh = int(sz * sc * 1.25); hh = lh * len(lines) + 30
        d.rounded_rectangle([BCX - max(ws) / 2 - 30, y - 18, BCX + max(ws) / 2 + 30, y - 18 + hh], 18, fill=(12, 8, 20, int(225 * a / 255)), outline=col + (a,), width=6)
        for i, l in enumerate(lines): ctext(d, BCX, y + i * lh, l, f, col, 10, a)
        img.alpha_composite(L)
face = {'hollow': 1, 'cyrus': 1}
wr = None if PREVIEW else Writer(OUT + 'v20_noaudio.mp4'); events = []
def addev(t, n):
    if not any(abs(e[0] - t) < 0.01 and e[1] == n for e in events): events.append((round(t, 3), n))
def distances(st, ws):
    wset = set(w for _, w in ws)
    return dist(st['hollow'], 0, wset), dist(st['cyrus'], N - 1, wset)
addev(0.0, 'go_8bit')
for i, e in enumerate(LOG):
    if e[0] == 'wall': addev(starts[i] + 0.3 * TWALL, 'sword_hit')
addev(T_HOLD0 + 0.05, 'twinkle'); addev(starts[I_TRAP] + 0.25, 'buzz_8bit'); addev(starts[I_CLUTCH] + 0.2, 'powerup_8bit')
if I_CLUTCH2: addev(starts[I_CLUTCH2] + 0.2, 'punch')
addev(T_END, 'victory'); addev(T_END + WINHOLD, 'rewind')
frames = [int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(int(round(DUR * FPS)))
for f in frames:
    t = f / FPS
    k, u, holding = kt(t)
    if k >= len(LOG): st, ws, lf = FINAL; ev = None; u = 1
    else: st, ws, lf, ev = steps[k]
    if holding: ev = None
    reset = max(0.0, (t - T_END - WINHOLD) / RESET) if t >= T_END + WINHOLD else 0.0   # 0..1 slide back to the start
    if reset > 0: lf = {g: lf[g] + round((WL0 - lf[g]) * min(1, reset * 1.5)) for g in lf}
    shake = 0
    if ev and ev[0] == 'wall' and 0.25 < u < 0.45: shake = int(6 * math.sin(u * 90))
    img = BOARD.copy() if not shake else Image.new('RGBA', (W, H), (46, 30, 22, 255))
    if shake: img.alpha_composite(BOARD, (0, shake))
    img.alpha_composite(RULE)
    # walls
    for who, w in ws:
        s = WS[(who, w[2])]; cx, cy = wall_xy(w); cy += shake
        if reset > 0:
            g = max(0.0, 1 - reset * 1.6)
            if g <= 0: continue
            s = s.resize((max(1, int(s.width * (g if w[2] == 'h' else 1))), max(1, int(s.height * (g if w[2] == 'v' else 1)))), Image.NEAREST)
        img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
    if ev and ev[0] == 'wall':
        who, w = ev[1], ev[2]; s = WS[(who, w[2])]; cx, cy = wall_xy(w); cy += shake
        g = min(1, u / 0.3)
        if w[2] == 'h': s2 = s.resize((max(1, int(s.width * (0.3 + 0.7 * g))), max(1, int(s.height * g))), Image.NEAREST)
        else: s2 = s.resize((max(1, int(s.width * g)), max(1, int(s.height * (0.3 + 0.7 * g)))), Image.NEAREST)
        img.alpha_composite(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)))
        if 0.28 < u < 0.95:
            v = (u - 0.28) / 0.67; dsz = up(DUST, 2.0 + 1.4 * v); al = dsz.getchannel('A').point(lambda p: int(p * (1 - v))); dsz.putalpha(al)
            img.alpha_composite(dsz, (int(cx - dsz.width / 2), int(cy - dsz.height / 2)))
    # pieces (sorted by row so the lower one is drawn in front)
    pos = {}
    for g in ('hollow', 'cyrus'):
        x, y = cell_c(*st[g])
        if reset > 0:
            sx, sy = cell_c(*START[g]); v = min(1, reset * 1.3); v = v * v * (3 - 2 * v)
            x, y = x + (sx - x) * v, y + (sy - y) * v
        pos[g] = (x, y)
    for g in sorted(['hollow', 'cyrus'], key=lambda g: pos[g][1]):
        x, y = pos[g]; spr = None
        if ev and ev[0] == 'move' and ev[1] == g:
            (r0, c0), (r1, c1) = ev[2], ev[3]; x0, y0 = cell_c(r0, c0); x1, y1 = cell_c(r1, c1)
            uu = min(1, u / 0.8); x, y = x0 + (x1 - x0) * uu, y0 + (y1 - y0) * uu
            if c1 != c0: face[g] = 1 if c1 > c0 else -1
            ph = int(uu * 8) % 8
            if r1 > r0: spr = FRUN[g][ph]
            else:
                rs = SRUN_H if g == 'hollow' else SRUN_C; spr = rs[ph] if face[g] > 0 else rs[ph].transpose(Image.FLIP_LEFT_RIGHT)
            if uu >= 1: spr = None
        if reset > 0 and reset < 0.85:
            rs = SRUN_H if g == 'hollow' else SRUN_C; spr = rs[int(t * 20) % 8]
        if ev and ev[0] == 'wall' and ev[1] == g and g == 'cyrus' and u < 0.9:
            a = ATK[min(len(ATK) - 1, int(u / 0.9 * len(ATK)))]
            ix, iy = int(x - IDL[g][0].width / 2) - 14 * K, int(y + 30 - FOOTY + shake) - 26 * K
            img.alpha_composite(a, (ix, iy)); continue
        if spr is None: spr = IDL[g][int(t * 8) % len(IDL[g])]
        layer(img, lambda d, x=x, y=y: d.ellipse([x - 40, y + 20, x + 40, y + 40], fill=(0, 0, 0, 90)))
        if g == 'hollow' and ev and ev[0] == 'wall' and ev[1] == 'hollow' and u < 0.6:
            layer(img, lambda d, x=x, y=y, u=u: d.ellipse([x - 70 - 30 * u, y - 90 - 30 * u, x + 70 + 30 * u, y + 40 + 30 * u], outline=(190, 120, 255, int(200 * (1 - u))), width=6))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y + 30 - FOOTY + shake)))
    # gold ring: opening (YOU'RE THE HOLLOW), the 1-step hold, and fading back in before the loop point
    ring_a = 0
    if t < 1.6: ring_a = 230 if t < 1.3 else int(230 * (1.6 - t) / 0.3)
    if holding: ring_a = 230
    if reset > 0.55: ring_a = int(230 * min(1, (reset - 0.55) / 0.45))
    if ring_a:
        hx, hy = pos['hollow'] if not (ev and ev[0] == 'move' and ev[1] == 'hollow') else (x if False else pos['hollow'])
        if ev and ev[0] == 'move' and ev[1] == 'hollow':
            (r0, c0), (r1, c1) = ev[2], ev[3]; x0, y0 = cell_c(r0, c0); x1, y1 = cell_c(r1, c1); uu = min(1, u / 0.8); hx, hy = x0 + (x1 - x0) * uu, y0 + (y1 - y0) * uu
        pr = 84 + 8 * math.sin(t * 9)
        layer(img, lambda dd: dd.ellipse([hx - pr, hy - 60 - pr, hx + pr, hy - 60 + pr], outline=(255, 214, 60, ring_a), width=7))
    # +N step pops next to the blocked piece (48px, dark outline)
    pops = []
    if ev and ev[0] == 'wall' and u > 0.3 and ev[3] >= 1:
        op = 'hollow' if ev[1] == 'cyrus' else 'cyrus'; ox, oy = pos[op]; a = int(255 * min(1, (1 - u) / 0.3))
        col = (255, 90, 90) if op == 'hollow' else (255, 255, 255)
        py_ = max(Y0 - 10, oy - 250 - 30 * u) if oy - 250 > Y0 - 10 else oy + 50
        for t0_, t1_, ln_, sz_, c_, sy_ in STAMPS:      # never under a stamp: drop below the piece's feet instead
            if t0_ - 0.1 <= t < t1_ and sy_ - 30 < py_ + 60 and py_ < sy_ + int(sz_ * 1.25) * len(ln_) + 20: py_ = oy + 55
        txt = f'+{ev[3]} STEP' + ('S' if ev[3] > 1 else ''); hw = len(txt) * 24 + 10
        pops.append((min(max(ox, 72 + hw), 885 - hw), py_, txt, 48, col, 8, a))
    if t < 1.3 or (reset > 0.55):
        a = 255 if t < 1.3 else int(255 * min(1, (reset - 0.55) / 0.45))
        if t >= 1.0 and t < 1.3: a = int(255 * (1.3 - t) / 0.3)
        pops.append((BCX, Y0 + BW - 150, "YOU'RE THE HOLLOW", 48, (255, 255, 255), 9, a))
    # HUD under the hook band: face, step count (biggest), gummies left
    PY = HB + 8; PH = 108
    layer(img, lambda d: (d.rounded_rectangle([72, PY, 540, PY + PH], 18, fill=(20, 14, 34, 230), outline=(180, 120, 255, 255), width=5),
                          d.rounded_rectangle([556, PY, 1023, PY + PH], 18, fill=(20, 14, 34, 230), outline=(255, 160, 40, 255), width=5)))
    if reset > 0: dh, dc = distances(START, []) if reset > 0.5 else distances(st, ws)
    else: dh, dc = distances(st, ws)
    for g, x0_, col in (('hollow', 72, (210, 170, 255)), ('cyrus', 556, (255, 190, 90))):
        img.alpha_composite(ICON[g], (x0_ + 8, PY + 6)); d = ImageDraw.Draw(img)
        n_ = dh if g == 'hollow' else dc
        d.text((x0_ + 116, PY + 10), f'{n_} STEP' + ('' if n_ == 1 else 'S'), font=F(48), fill=col, stroke_width=6, stroke_fill=(20, 15, 35))
        for i in range(WL0):
            ic = ICONW[g]; ix = x0_ + 118 + i * 62; iy = PY + 64
            if i < lf[g]: img.alpha_composite(ic, (ix + (40 - ic.width) // 2, iy + (40 - ic.height) // 2 - 4))
            else: layer(img, lambda dd, ix=ix, iy=iy: dd.ellipse([ix + 4, iy, ix + 36, iy + 32], outline=(110, 100, 130, 220), width=3))
    text_layer(img, pops)
    stamp_layer(img, t)
    if T_END <= t:
        uu = t - T_END; a = min(1, uu / 0.25)
        if reset > 0: a = max(0, 1 - reset / 0.4)
        if a > 0:
            img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(165 * a))))
            vf = VICF[int(uu * 8) % len(VICF)].copy()
            if a < 1: vf.putalpha(vf.getchannel('A').point(lambda p: int(p * a)))
            img.alpha_composite(vf, (W // 2 - 60 - vf.width // 2, 1000 + DY - vf.height))
            g2 = up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 3); bob = int(8 * math.sin(uu * 5))
            if a < 1: g2.putalpha(g2.getchannel('A').point(lambda p: int(p * a)))
            img.alpha_composite(g2, (W // 2 + 110, 690 + DY + bob))
            sc = 1 + 0.3 * max(0, 1 - uu / 0.12)
            text_layer(img, [(W / 2 - 30, 1012 + DY, 'THE HOLLOW WINS!', int(56 * sc), (255, 214, 60), 9, int(255 * a))])   # 'HE NEVER GAVE UP' cut (repeats the hook)
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(OUT + f'p_{t:05.2f}.png')
    else: wr.write(img)
if not PREVIEW:
    wr.close()
    json.dump({'events': sorted(events)}, open(OUT + 'v20_events.json', 'w'))
print('winner', WIN, 'turns', len(LOG), 'dur', round(DUR, 2))
