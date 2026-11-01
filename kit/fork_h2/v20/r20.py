# #20 Never give up -- Oct 29 notes rework (fork_n3). Bennett: "stop with all the steps and text on screen. People can place as many
# barriers as possible. A move takes a turn OR a barrier takes a turn. Too chaotic now."
# Now: hand-scripted turns (script20.py, BFS-checked): turns alternate Hollow / Cyrus, each turn is ONE move or ONE barrier.
# The Hollow (player) only moves and never quits; Cyrus moves once, then walls him in (ceiling, right wall, door behind him,
# a block near the top), then runs for his own row too late, stuck behind his own walls: the Hollow wins by one turn.
# Cut: step/gummy HUD, 1 STEP LEFT / WALLED IN / COMEBACK / BLOCKED stamps, +N STEPS pops, screen shake. Calm, even rhythm,
# a soft glow under whoever's turn it is. Kept: NEVER GIVE UP strip hook, YOU'RE THE HOLLOW opener, THE HOLLOW WINS!, loop reset.
import sys, os, math, json
os.environ.setdefault('NB', '7')
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
OUT = SP_ + 'fork_h2/v20/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_band
sys.path.insert(0, SP_ + 'fork_n3/v20/')   # fork_h2: sim/script20/story from the original dir
from sim import N
from script20 import build
HOOK, HB = hook_band(['NEVER GIVE UP'], accent=0)
# fork_h2 Oct 29 hook swap: CAN YOU OUTSMART / CYRUS? (CYRUS? orange). 2 lines cannot fit above the old strip bottom (380) with the text
# starting at y>=262, so the strip runs 250-398 (tight line height), text 262-388, clear of Cyrus's hair (y407); HB (layout) stays 380
import sys as _s; _s.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h2'); import hookx
HOOK, _hb2 = hookx.band_tight(['CAN YOU OUTSMART', [('CYRUS?', (255, 160, 40))]], size=56, y_text=262, lh=70, top=250, bottom=398)   # Cyrus's hair top at frame 0 is y407
PREVIEW = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
LOG = build()
# Oct 29 review: board scaled up to ~944px and centred, so the right column reaches into the lower-right UI zone; the game is
# mirrored left-right (same moves, same barriers, same turn order) so the Hollow's detour runs down the LEFT side and nothing
# that matters ever stands in that corner (column 6 rows 4-6 stay empty)
def _mc(p): return (p[0], N - 1 - p[1])
def _mw(w): return (w[0], N - 2 - w[1], w[2])
LOG = [(e[0], e[1], _mc(e[2]), _mc(e[3])) if e[0] == 'move' else (e[0], e[1], _mw(e[2]), e[3]) for e in LOG]
assert LOG[-1][1] == 'hollow' and LOG[-1][3][0] == 0
I_CAGE = 7                                # the barrier that walls him in on top and on the right (he has to step back)
assert LOG[I_CAGE][0] == 'wall' and LOG[I_CAGE + 1][3][0] > LOG[I_CAGE + 1][2][0]
K = 4                                       # Oct 29 review: pieces 3x -> 4x (+33%)
CS = 136; BW = N * CS - 8                   # board 720 -> 944px, centred
X0 = (W - BW) // 2; Y0 = 556; DY = Y0 - 704; SC = CS / 104
BCX = X0 + BW // 2
def cell_c(r, c): return X0 + c * CS + (CS - 8) // 2, Y0 + r * CS + (CS - 8) // 2
G = SP_ + 'fork_a2/gen/'
def pk(k, i): return crop(Image.open(f'{G}{k}/{i:02d}.png').convert('RGBA'))
TL = up(pk('floor', 4), 3); TD = up(pk('floor', 12), 3)
TL = TL.resize((CS - 8, CS - 8), Image.NEAREST); TD = TD.resize((CS - 8, CS - 8), Image.NEAREST)
WA = pk('wall_amber', 2)
WLEN = 2 * CS - 4
def wall_spr(im, o):
    s = im.resize((WLEN, max(1, int(im.height * WLEN / im.width))), Image.NEAREST)
    return s if o == 'h' else s.transpose(Image.ROTATE_90)
WS = {'h': wall_spr(WA, 'h'), 'v': wall_spr(WA, 'v')}
def wall_xy(w):
    r, c, o = w; return X0 + (c + 1) * CS - 4, Y0 + (r + 1) * CS - 4
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
HG = 'cre'       # the Hollow's goal row gummies (was the gold gummy; no gold framing)
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
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
        g1 = up(Image.open(PL + f'gummies/pick_{HG}.png').convert('RGBA'), 1.5); g2 = up(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'), 1.5)
        BOARD.alpha_composite(g1, (X0 + c * CS + (CS - 8 - g1.width) // 2, Y0 + 6))
        BOARD.alpha_composite(g2, (X0 + c * CS + (CS - 8 - g2.width) // 2, Y0 + (N - 1) * CS + CS - 8 - g2.height - 6))
SRUN_H = seq(PL + 'maze/anim/hollow_srun', K); SRUN_C = seq(PL + 'race/cyrus_run', K)
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', K) for g in ('hollow', 'cyrus')}
BRUN = {g: seq(PL + f'maze/anim/{g}_brun', K) for g in ('hollow', 'cyrus') if os.path.isdir(PL + f'maze/anim/{g}_brun')}
IDL = {'hollow': idle('hollow', K), 'cyrus': idle('cyrus', K)}
ATK = seq(PL + 'race/cyrus_atk', K)
FOOTY = 78 * K
VICF = vic('hollow', 380)
# ---------------- timeline: one even rhythm; each turn = one move or one barrier
TMOVE, TWALL, HOLD = 0.5, 0.75, 0.45       # HOLD: a beat after he is walled in, before he steps back
MOVE_ANIM = 0.36
# Oct 29 review 2: after Cyrus's last barrier the race turns (all single moves) run quicker, 0.38s each (0.28s step + a still
# beat) instead of 0.5s: about 1.5s tighter, same turns, same outcome
LATE = max(i for i, e in enumerate(LOG) if e[0] == 'wall') + 1
DT = [TWALL if e[0] == 'wall' else (TMOVE if i < LATE else 0.38) for i, e in enumerate(LOG)]
AN = [MOVE_ANIM if i < LATE else 0.28 for i in range(len(LOG))]
starts = []; t_ = 0.0                       # Oct 29 review: the Hollow's first step starts on frame 0 (opener text/ring over it)
for i, e in enumerate(LOG):
    starts.append(t_); t_ += DT[i] + (HOLD if i == I_CAGE else 0)
T_END = t_; WINHOLD = 1.6; RESET = 0.6; DUR = T_END + WINHOLD + RESET
print('cage', round(starts[I_CAGE], 2), 'win', round(T_END, 2), 'dur', round(DUR, 2), 'turns', len(LOG))
def kt(t):
    if t >= T_END: return len(LOG), 1
    if t < starts[0]: return -1, 0
    k = max(i for i in range(len(LOG)) if starts[i] <= t)
    return k, min(1, (t - starts[k]) / DT[k])
state = {'hollow': (N - 1, N // 2), 'cyrus': (0, N // 2)}; walls = []
START = dict(state)
steps = []
for i, e in enumerate(LOG):
    steps.append((dict(state), list(walls), e))
    if e[0] == 'move': state[e[1]] = e[3]
    elif e[0] == 'wall': walls.append(e[2])
FINAL = (dict(state), list(walls))
face = {'hollow': 1, 'cyrus': 1}
wr = None if PREVIEW else Writer(OUT + 'v20_noaudio.mp4'); events = []
def addev(t, n): events.append((round(t, 3), n))
addev(0.0, 'go_8bit')
for i, e in enumerate(LOG):
    if e[0] == 'wall': addev(starts[i] + 0.42 * TWALL, 'stomp_8bit')
addev(starts[I_CAGE] + 0.42 * TWALL + 0.25, 'buzz_8bit')
addev(T_END, 'victory'); addev(T_END + WINHOLD, 'rewind')
frames = [int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(int(round(DUR * FPS)))
for f in frames:
    t = f / FPS
    k, u = kt(t)
    if k >= len(LOG): st, ws = FINAL; ev = None; u = 1
    elif k < 0: st, ws = steps[0][0], []; ev = None
    else: st, ws, ev = steps[k]
    reset = max(0.0, (t - T_END - WINHOLD) / RESET) if t >= T_END + WINHOLD else 0.0
    img = BOARD.copy()
    GH0 = up(Image.open(PL + f'gummies/pick_{HG}.png').convert('RGBA'), 1.5).height
    if t < 0.7:      # Oct 29 review 2: the goal row pulses once at the start so the viewer sees where the Hollow is going
        pv = math.sin(math.pi * t / 0.7)
        layer(img, lambda d: d.rectangle([X0, Y0, X0 + BW, Y0 + CS - 8], fill=(255, 230, 140, int(120 * pv))))
        gp = up(Image.open(PL + f'gummies/pick_{HG}.png').convert('RGBA'), 1.5 * (1 + 0.45 * pv))
        for c in range(0, N, 2):
            img.alpha_composite(gp, (int(X0 + c * CS + (CS - 8) / 2 - gp.width / 2), int(Y0 + 6 + GH0 / 2 - gp.height / 2)))
    WDROP = 0.42                              # barrier lands at 42% of Cyrus's turn (after his swing starts)
    for w in ws:
        s = WS[w[2]]; cx, cy = wall_xy(w)
        if reset > 0:
            g = max(0.0, 1 - reset * 1.6)
            if g <= 0: continue
            s = s.resize((max(1, int(s.width * (g if w[2] == 'h' else 1))), max(1, int(s.height * (g if w[2] == 'v' else 1)))), Image.NEAREST)
        img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
    if ev and ev[0] == 'wall' and u >= WDROP - 0.12:
        w = ev[2]; s = WS[w[2]]; cx, cy = wall_xy(w)
        g = min(1, (u - (WDROP - 0.12)) / 0.12)
        s2 = s if g >= 1 else s.copy()
        yo = int(-60 * (1 - g))                       # drops in from just above and lands
        if g < 1: s2.putalpha(s2.getchannel('A').point(lambda p: int(p * g)))
        img.alpha_composite(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2 + yo)))
        if WDROP < u < WDROP + 0.5:
            v = (u - WDROP) / 0.5; dsz = up(DUST, 1.6 + 1.0 * v); dsz.putalpha(dsz.getchannel('A').point(lambda p: int(p * 0.8 * (1 - v))))
            img.alpha_composite(dsz, (int(cx - dsz.width / 2), int(cy - dsz.height / 2)))
    pos = {}
    for g in ('hollow', 'cyrus'):
        x, y = cell_c(*st[g])
        if ev and ev[0] == 'move' and ev[1] == g:
            (r0, c0), (r1, c1) = ev[2], ev[3]; x0, y0 = cell_c(r0, c0); x1, y1 = cell_c(r1, c1)
            uu = min(1, u * DT[k] / AN[k]); uu = uu * uu * (3 - 2 * uu); x, y = x0 + (x1 - x0) * uu, y0 + (y1 - y0) * uu
        if reset > 0:
            sx, sy = cell_c(*START[g]); v = min(1, reset * 1.3); v = v * v * (3 - 2 * v)
            x, y = x + (sx - x) * v, y + (sy - y) * v
        pos[g] = (x, y)
    # whose turn: soft glow under that piece (purple = Hollow, orange = Cyrus)
    if 0 <= k < len(LOG) and reset == 0:
        who = LOG[k][1]; gx, gy = pos[who]; a = int(200 * min(1, (t - starts[k]) / 0.08))
        col = (180, 120, 255) if who == 'hollow' else (255, 160, 40)
        layer(img, lambda d: ([d.ellipse([gx - 74 - q, gy + 14 - q * 0.4, gx + 74 + q, gy + 62 + q * 0.4], fill=col + (int(a * (1 - q / 24)),)) for q in (0, 12)],
                              d.ellipse([gx - 84, gy + 8, gx + 84, gy + 68], outline=col + (min(255, a + 40),), width=5)))
    for g in sorted(['hollow', 'cyrus'], key=lambda g: pos[g][1]):
        x, y = pos[g]; spr = None
        if ev and ev[0] == 'move' and ev[1] == g and u * DT[k] < AN[k]:
            (r0, c0), (r1, c1) = ev[2], ev[3]
            if c1 != c0: face[g] = 1 if c1 > c0 else -1
            ph = int(u * DT[k] / AN[k] * 8) % 8
            if r1 > r0: spr = FRUN[g][ph]
            else:
                rs = SRUN_H if g == 'hollow' else SRUN_C; spr = rs[ph] if face[g] > 0 else rs[ph].transpose(Image.FLIP_LEFT_RIGHT)
        if 0 < reset < 0.85:
            rs = SRUN_H if g == 'hollow' else SRUN_C; spr = rs[int(t * 20) % 8]
        if ev and ev[0] == 'wall' and g == 'cyrus' and u < 0.9:
            a = ATK[min(len(ATK) - 1, int(u / 0.9 * len(ATK)))]
            ix, iy = int(x - 35 * K), int(y + 40 - FOOTY) - 26 * K      # body of the swing frames lines up with his idle spot (was ~90px left)
            img.alpha_composite(a, (ix, iy)); continue
        if g == 'hollow' and t >= T_END and reset < 0.4: continue      # Oct 29 review 2: no second (board) Hollow behind the victory pose
        if spr is None:
            if 0 <= k < len(LOG) and reset == 0 and LOG[k][1] != g: spr = IDL[g][0]   # not your turn: stand still
            else: spr = IDL[g][int(t * 8) % len(IDL[g])]
        layer(img, lambda d, x=x, y=y: d.ellipse([x - 52, y + 28, x + 52, y + 52], fill=(0, 0, 0, 90)))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y + 40 - FOOTY)))
    # walled in: a '!' emote over the Hollow for the beat before he steps back
    tc = starts[I_CAGE] + WDROP * TWALL
    if tc + 0.1 <= t < starts[I_CAGE + 1] + 0.1:
        hx, hy = pos['hollow']; sc = 1 + 0.3 * max(0, 1 - (t - tc - 0.1) / 0.1)
        text_layer(img, [(hx + 4, hy - 315, '!', int(64 * sc), (255, 80, 80), 8, 255)])
    # gold ring + YOU'RE THE HOLLOW: opener, and fading back in before the loop point
    ring_a = 0
    if t < 1.8: ring_a = 230 if t < 1.5 else int(230 * (1.8 - t) / 0.3)
    if reset > 0.55: ring_a = int(230 * min(1, (reset - 0.55) / 0.45))
    if ring_a:
        hx, hy = pos['hollow']; pr = 112 + 10 * math.sin(t * 9)
        layer(img, lambda dd: dd.ellipse([hx - pr, hy - 80 - pr, hx + pr, hy - 80 + pr], outline=(255, 214, 60, ring_a), width=7))
    if t < 1.8 or reset > 0.55:
        a = 255 if t < 1.5 else (int(255 * (1.8 - t) / 0.3) if t < 1.8 else int(255 * min(1, (reset - 0.55) / 0.45)))
        text_layer(img, [(BCX, Y0 + 2 * CS + 40, "YOU'RE THE HOLLOW", 48, (255, 255, 255), 9, a)])
    if T_END <= t:
        uu = t - T_END; a = min(1, uu / 0.25)
        if reset > 0: a = max(0, 1 - reset / 0.4)
        if a > 0:
            img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(165 * a))))
            vf = VICF[int(uu * 8) % len(VICF)].copy()
            if a < 1: vf.putalpha(vf.getchannel('A').point(lambda p: int(p * a)))
            img.alpha_composite(vf, (W // 2 - 60 - vf.width // 2, 1000 + DY - vf.height))
            g2 = up(Image.open(PL + f'gummies/pick_{HG}.png').convert('RGBA'), 3); bob = int(8 * math.sin(uu * 5))
            if a < 1: g2.putalpha(g2.getchannel('A').point(lambda p: int(p * a)))
            img.alpha_composite(g2, (W // 2 + 110, 690 + DY + bob))
        # Oct 29 review 2: YOU WIN! snaps in at full opacity (stroked, no box); only fades with the loop reset
        ta = 255 if reset == 0 else int(255 * max(0, 1 - reset / 0.4))
        if ta > 0:
            sc = 1 + 0.15 * max(0, 1 - uu / 0.12)
            text_layer(img, [(W / 2, 1030 + DY, 'YOU WIN!', int(80 * sc), (255, 214, 60), 10, ta)])
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(OUT + f'p_{t:05.2f}.png')
    else: wr.write(img)
if not PREVIEW:
    wr.close()
    json.dump({'events': sorted(events)}, open(OUT + 'v20_events.json', 'w'))
print('turns', len(LOG), 'dur', round(DUR, 2))
