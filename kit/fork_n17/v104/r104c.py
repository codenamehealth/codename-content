import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
OUTD = os.path.dirname(os.path.abspath(__file__))
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b10')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
sys.path.insert(0, SP + 'fork_rc12'); from rc12 import hook_layer2, plate, Stamps, gummy_src, acv_tag
# rc12 review recut: digging from frame 0 (dam breaks 1.6s), re-sim; one 60px plate stamp at a time over the guide; big OUT stamps
# (caught guides greyed); text moved off the portal; REACH THE PORTAL! rule line; ACV gloss + tag; STRONG flames; 1.5s hold then loop.
NAMES = ['joy', 'cyrus', 'cleo', 'ray']      # Hollow racer removed (he is the player, never a competitor)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
KS = 1.25                                    # n18: columns, blocks and guides scaled 1.25x, centred on the lower-half safe width (70..887)
SX = {n: 165 + i * 210 for i, n in enumerate(NAMES)}
TOP = 720; ROWH = 80; NROWS = int(os.environ.get('NROWS', '7')); BOT = TOP + NROWS * ROWH          # shaft bottom
TUNNEL_Y = 1484; TUN_TOP = BOT + 22; EXIT_X = int(os.environ.get('EXITX', '480')); CW = 87   # carve half-width
PLAB = {'joy': 'SHIELD!', 'cyrus': 'SPEED!', 'cleo': 'STRENGTH!', 'ray': 'SLEEP!'}
PCOL = {'joy': (120, 230, 110), 'cyrus': (255, 170, 60), 'cleo': (110, 170, 255), 'ray': (200, 130, 255)}
T_GO, T_FLOOD = float(os.environ.get('TG', '0.0')), float(os.environ.get('TF', '1.6'))   # rc12: digging from frame 0, dam breaks at 1.6s
FA, FB = float(os.environ.get('FA', '60')), float(os.environ.get('FB', '3.5'))
GUMROW = dict((kv.split(':')[0], int(kv.split(':')[1])) for kv in os.environ.get('GUMROWS', '').split(',') if kv)   # n19: staggered gummy rows -> powers fire one at a time
RAYK = float(os.environ.get('RAYK', '1.0'))
SPD = float(os.environ.get('SPD', '2.4')); SLP = float(os.environ.get('SLP', '1.0')); STR = float(os.environ.get('STR', '1.6')); HOLD = float(os.environ.get('HOLD', '1.9'))
# ---- n19: scripted race (same flood, catch, sleep and shield rules as the sim; dig timings authored per guide)
SCR = {   # rows: (break time, hp, hits); stuck: hp of the row they never get through; gum: row holding their gummy
    'cleo':  dict(rows=[(0.9, 2, 2), (1.25, 3, 1)], stuck=6, gum=0, iv=0.46),           # STRENGTH at 0.9: one smash breaks a 3-hp block
    'ray':   dict(rows=[(0.8, 1, 1), (2.0, 2, 2), (2.6, 2, 2), (3.2, 2, 2), (3.7, 2, 2), (4.9, 2, 2), (6.0, 2, 2)], stuck=2, gum=1, iv=0.5),
    'joy':   dict(rows=[(0.7, 1, 1), (1.4, 2, 2), (3.35, 2, 2)], stuck=6, gum=2, iv=0.5),
    'cyrus': dict(rows=[(0.65, 1, 1), (1.6, 2, 2), (3.45, 1, 1), (3.8, 2, 2), (4.15, 2, 2), (4.5, 2, 2)], stuck=6, gum=3, iv=0.44),   # SPEED 3.8: next two rows in 0.7s
}
def _hits(n):
    sc = SCR[n]; T_SL = SCR['ray']['rows'][SCR['ray']['gum']][0]; sl = (T_SL, T_SL + SLP) if n != 'ray' else (99, 99)
    out = []; prev = 0.15
    for (tb, hp, nh) in sc['rows']:
        segs = [(a, b) for a, b in ((prev, min(tb, sl[0])), (max(prev, sl[1]), tb)) if b - a > 1e-6]
        tot = sum(b - a for a, b in segs); dmg = [hp // nh + (1 if q < hp % nh else 0) for q in range(nh)]
        for q in range(nh):
            want = tot * (q + 1) / nh; acc = 0
            for a, b in segs:
                if want <= acc + (b - a) + 1e-9: out.append((a + want - acc, dmg[q])); break
                acc += b - a
        prev = tb
    t = prev; hp = sc['stuck']; spd_end = sc['rows'][sc['gum']][0] + SPD if n == 'cyrus' else -1
    while t < 12:
        t += sc['iv'] * (0.5 if t < spd_end else 1.0)
        if sl[0] <= t < sl[1]: t = sl[1] + 0.05
        out.append((t, 1 if hp > 1 else 0)); hp = max(1, hp - 1)
    return out
def sim_scripted(seed=0):
    g = {}
    for n in NAMES:
        sc = SCR[n]; hp = [r[1] for r in sc['rows']] + [sc['stuck']] + [2] * NROWS; hp = hp[:NROWS]
        g[n] = dict(d=0, hp=list(hp), hp0=list(hp), gum={sc['gum']}, hits=_hits(n), hi=0, power=-9, caught=None, out=None, x=float(SX[n]), y=float(TOP), phase='dig',
                    drop=-9, sleep=-9, shield=False, hold=-9, nxt=0.0)
    frames = []; ev = []
    for f in range(int(40 * 30)):
        t = f / 30; dt = 1 / 30
        fl = -99 if t < T_FLOOD else (t - T_FLOOD) * (FA + FB * (t - T_FLOOD)); wy = TOP - 70 + fl
        for n, s in g.items():
            if s['caught'] is not None or s['out'] is not None: continue
            if s['phase'] == 'dig':
                while s['hi'] < len(s['hits']) and s['hits'][s['hi']][0] <= t:
                    th, dmg = s['hits'][s['hi']]; s['hi'] += 1; ev.append((th, 'hit', n)); s['hp'][s['d']] -= dmg
                    if s['hp'][s['d']] <= 0:
                        if s['d'] in s['gum']:
                            s['power'] = th; ev.append((th, 'gum', n))
                            if n == 'joy': s['shield'] = True
                            if n == 'ray':
                                for m, o in g.items():
                                    if m == n or o['caught'] is not None or o['out'] is not None or o['phase'] != 'dig': continue
                                    if o['shield']: o['shield'] = False; ev.append((th, 'blocked', m))
                                    else: o['sleep'] = th + SLP; ev.append((th, 'sleep', m))
                        s['d'] += 1; s['drop'] = th; ev.append((th, 'break', n))
                        if s['d'] >= NROWS: s['phase'] = 'fall'; ev.append((th, 'through', n)); break
                s['nxt'] = s['hits'][s['hi']][0] if s['hi'] < len(s['hits']) else 99
                s['y'] = TOP + s['d'] * ROWH
                if s['phase'] == 'dig' and wy > s['y'] - 50 and t >= s['hold']:
                    if s['shield']: s['shield'] = False; s['hold'] = t + HOLD; ev.append((t, 'blocked', n))
                    else: s['caught'] = t; ev.append((t, 'caught', n))
            elif s['phase'] == 'fall':
                s['y'] += 900 * dt
                if s['y'] >= TUNNEL_Y: s['y'] = TUNNEL_Y; s['phase'] = 'run'
            elif s['phase'] == 'run':
                dx = EXIT_X - s['x']; st = 420 * dt
                if abs(dx) <= st: s['x'] = EXIT_X; s['out'] = t; ev.append((t, 'out', n))
                else: s['x'] += st * (1 if dx > 0 else -1)
        frames.append(({n: dict(d=s['d'], hp=list(s['hp']), x=s['x'], y=s['y'], phase=s['phase'], caught=s['caught'], out=s['out'], power=s['power'], drop=s['drop'], nxt=s['nxt'], sleep=s['sleep'], shield=s['shield'], hold=s['hold']) for n, s in g.items()}, wy))
        if all(s['caught'] is not None or s['out'] is not None for s in g.values()):
            last = max([s['caught'] or 0 for s in g.values()] + [s['out'] or 0 for s in g.values()])
            if t > last + 0.1: break
    return frames, ev, g
def sim(seed):
    if os.environ.get('SCRIPT'): return sim_scripted(seed)
    rnd = random.Random(seed)
    g = {}
    for n in NAMES:
        hp = [rnd.choice([1, 1, 2, 2, 2, 3]) for _ in range(NROWS)]
        gum = set(rnd.sample(range(1, NROWS - int(os.environ.get('GRM', '3'))), 1))
        if GUMROW: gum = {GUMROW[n]}
        g[n] = dict(d=0, hp=list(hp), hp0=list(hp), gum=gum, nxt=T_GO + rnd.uniform(0.1, 0.4), iv=rnd.uniform(0.40, 0.48) * float(os.environ.get('IVK', '1')) * (RAYK if n == 'ray' else 1.0), power=-9, caught=None,
                    out=None, x=float(SX[n]), y=float(TOP), phase='dig', ph=rnd.uniform(0, 6.3), hits=0, drop=-9, gotgum=[], sleep=-9, shield=False, hold=-9)
    frames = []; ev = []
    for f in range(int(40 * 30)):
        t = f / 30; dt = 1 / 30
        fl = -99 if t < T_FLOOD else (t - T_FLOOD) * (FA + FB * (t - T_FLOOD))      # flood front depth below TOP
        wy = TOP - 70 + fl                                                          # water surface y
        for n, s in g.items():
            if s['caught'] is not None or s['out'] is not None: continue
            if s['phase'] == 'dig':
                if t < s['sleep']: s['nxt'] = max(s['nxt'], s['sleep'] + 0.05)
                if t >= s['nxt'] and t >= T_GO:
                    iv = s['iv'] * (1 + 0.15 * math.sin(t * 0.9 + s['ph']))
                    if n == 'cyrus' and t - s['power'] < SPD: iv *= 0.5                  # SPEED: dig rate x2 (n18: 2.4s)
                    s['nxt'] = t + iv; s['hits'] += 1
                    dmg = 3 if (n == 'cleo' and t - s['power'] < STR) else 1                # STRONG: one smash per block
                    s['hp'][s['d']] -= dmg; ev.append((t, 'hit', n))
                    if s['hp'][s['d']] <= 0:
                        if s['d'] in s['gum']:
                            s['power'] = t; ev.append((t, 'gum', n)); s['gotgum'].append(t)
                            if n == 'joy': s['shield'] = True
                            if n == 'ray':
                                for m, o in g.items():
                                    if m == n or o['caught'] is not None or o['out'] is not None or o['phase'] != 'dig': continue
                                    if o['shield']: o['shield'] = False; ev.append((t, 'blocked', m))
                                    else: o['sleep'] = t + SLP; ev.append((t, 'sleep', m))
                        s['d'] += 1; s['drop'] = t; ev.append((t, 'break', n))
                        if s['d'] >= NROWS: s['phase'] = 'fall'; ev.append((t, 'through', n))
                s['y'] = TOP + s['d'] * ROWH
                if wy > s['y'] - 50 and t >= s['hold']:
                    if s['shield']: s['shield'] = False; s['hold'] = t + HOLD; ev.append((t, 'blocked', n))   # n19: crack, pop, then ~1s before the water gets her
                    else: s['caught'] = t; ev.append((t, 'caught', n))
            elif s['phase'] == 'fall':
                s['y'] += 900 * dt
                if s['y'] >= TUNNEL_Y: s['y'] = TUNNEL_Y; s['phase'] = 'run'
            elif s['phase'] == 'run':
                dx = EXIT_X - s['x']; st = 420 * dt
                if abs(dx) <= st: s['x'] = EXIT_X; s['out'] = t; ev.append((t, 'out', n))
                else: s['x'] += st * (1 if dx > 0 else -1)
        frames.append(({n: dict(d=s['d'], hp=list(s['hp']), x=s['x'], y=s['y'], phase=s['phase'], caught=s['caught'], out=s['out'], power=s['power'], drop=s['drop'], nxt=s['nxt'], sleep=s['sleep'], shield=s['shield'], hold=s['hold']) for n, s in g.items()}, wy))
        if all(s['caught'] is not None or s['out'] is not None for s in g.values()):
            last = max([s['caught'] or 0 for s in g.values()] + [s['out'] or 0 for s in g.values()])
            if t > last + 0.1: break
    return frames, ev, g
def score(seed):
    fr, ev, g = sim(seed)
    outs = sorted((s['out'], n) for n, s in g.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in g.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != 3: return None
    tw, w = outs[0]
    if not (8.0 < tw < 10.5): return None
    if os.environ.get('WANT') and w != os.environ['WANT']: return None
    if max(caught) < tw - 2.5: return None
    gums = [(round(e[0], 1), e[2]) for e in ev if e[1] == 'gum']
    if len(gums) < 4: return None
    bl = [(round(e[0], 1), e[2]) for e in ev if e[1] == 'blocked']; sl = [e[2] for e in ev if e[1] == 'sleep']
    if not bl: return None
    return round(tw, 2), w, [round(c, 1) for c in caught], gums, 'blocked', bl, 'slept', sl
def score2(seed):
    fr, ev, g = sim(seed)
    outs = sorted((s['out'], n) for n, s in g.items() if s['out'] is not None)
    if len(outs) != 1: return None
    tw, w = outs[0]
    if w != os.environ.get('WANT', 'ray'): return None
    if not (float(os.environ.get('TW0', '7.0')) < tw < float(os.environ.get('TW1', '8.6'))): return None
    caught = {n: s['caught'] for n, s in g.items() if s['caught'] is not None}
    if len(caught) != 3: return None
    cs = sorted(caught.values())
    if any(b - a < 0.5 for a, b in zip(cs, cs[1:])): return None
    thr = [e[0] for e in ev if e[1] == 'through' and e[2] == w][0]
    if any(-0.15 < c - thr < 0.6 for c in cs) or any(-0.8 < c - tw < 0.1 for c in cs): return None        # breakthrough and win each get their own beat
    if caught['joy'] > thr - 0.6: return None
    gum = {e[2]: e[0] for e in ev if e[1] == 'gum'}
    if len(gum) < 4 or max(gum.values()) > tw: return None
    # SPEED: Cyrus visibly out-digs everyone while it lasts, and is caught only after it ends
    tc = gum['cyrus']; br = {n: sum(1 for e in ev if e[1] == 'break' and e[2] == n and tc <= e[0] < tc + SPD) for n in NAMES}
    if br['cyrus'] < 3 or br['cyrus'] < max(br[n] for n in NAMES if n != 'cyrus') + int(os.environ.get('SPM', '1')): return None
    if caught['cyrus'] < tc + SPD - 0.2: return None
    # SHIELD: the water pops Joy's bubble, then she goes out
    jb = [e[0] for e in ev if e[1] == 'blocked' and e[2] == 'joy']
    if not any(HOLD - 0.2 < caught['joy'] - b < HOLD + 0.15 for b in jb): return None
    tb = [b for b in jb if HOLD - 0.2 < caught['joy'] - b < HOLD + 0.15][0]
    if any(-0.15 < c - tb < 0.5 for n, c in caught.items() if n != 'joy'): return None   # BLOCKED gets its own moment
    dur = {'cleo': STR, 'cyrus': SPD, 'ray': SLP + 0.1, 'joy': 0.4}
    gs = sorted((v, n) for n, v in gum.items())
    if any(b - a < dur[n] + 0.05 for (a, n), (b, _) in zip(gs, gs[1:])): return None   # one power effect at a time
    if not any(e[1] == 'sleep' for e in ev): return None
    order = [n for n, _ in sorted(caught.items(), key=lambda kv: kv[1])]
    return round(tw, 2), round(thr, 2), {n: round(c, 2) for n, c in caught.items()}, order, {n: round(v, 2) for n, v in gum.items()}, br
if len(sys.argv) > 1 and sys.argv[1] == 'search2':
    for s_ in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score2(s_)
        if r: print(s_, r, flush=True)
    sys.exit()
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, G = sim(SEED)
WIN = [n for n, s in G.items() if s['out'] is not None][0]; T_WIN = G[WIN]['out']
print('winner', WIN, round(T_WIN, 2), {n: (round(s['caught'], 1) if s['caught'] else None) for n, s in G.items()})
# ---------------- art
DIG = {'joy': seq('joy_dig', KS * 2, 1, 9), 'cyrus': seq('cyrus_dig', KS * 2, 1, 9), 'cleo': seq('cleo_dig', KS * 2, 1, 9), 'ray': seq('ray_dig', KS * 2, 1, 9)}
STAND = {n: seq(f'../pixellab/maze/anim/{n}_frun', KS * 2, 0, 1)[0] for n in NAMES}
SRUN = {n: seq(f'../pixellab/race/{n}_run', KS * 2, 1, 9) for n in ['joy', 'cyrus', 'cleo', 'ray']}
PANIC = {n: seq(f'../pixellab/maze/anim/{n}_panic', KS * 2, 1, 9) for n in NAMES}
BLK = crop(Image.open('block/07.png').convert('RGBA')).resize((ROWH, ROWH), Image.NEAREST)
FT = int(78 * 2 * KS)   # sprite foot offset
def tint(im, col, k=0.55):
    a = np.array(im).astype(np.float32); c = np.array(col, np.float32)
    a[..., :3] = a[..., :3] * (1 - k) + (a[..., :3] / 255.0) * c * k * 1.25
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
BLKC = {n: tint(BLK, RING[n]) for n in NAMES}
GUM = {n: gummy(GK[n], 2 * KS) for n in NAMES}; GUM['joy'] = up(gummy_src('acv'), 2 * KS)
PORTAL = crop(Image.open('portal/12.png').convert('RGBA')); PORTAL = up(PORTAL, 4); print('portal', PORTAL.size)
from hook import hook_fade
HOOK, HB = hook_fade(['WHO SURVIVES', 'THE FLOOD?'], accent=1, color=(120, 200, 255), size=72, strength=225); HOOK2, _ = hook_fade(['DID YOURS', 'LIVE?'], accent=1, color=(120, 200, 255), size=72, strength=225); print('hook bottom', HB)
ROSTER_Y = HB + 10
CAVE = Image.open('cave/00.png').convert('RGB')
k_ = max(W / CAVE.width, H / CAVE.height); CAVE = CAVE.resize((int(CAVE.width * k_) + 1, int(CAVE.height * k_) + 1), Image.NEAREST)
CAVE = ImageEnhance.Brightness(CAVE.crop((0, 0, W, H))).enhance(0.72).convert('RGBA')
HUB = bg_frames('hub.gif', (1920, 1080), step=4)
HUB = [ImageEnhance.Brightness(f.crop((420, 0, 420 + W, TOP))).enhance(0.95).convert('RGBA') for f in HUB]   # hfg11: full height 0..TOP
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
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
ICON = {n: face(n, 32) for n in NAMES}
VICF = vic(WIN, 360)
# static board: carved shafts + tunnel into the cave
BOARD = CAVE.copy()
def carve(d):
    for n in NAMES:
        x = SX[n]; d.rectangle([x - CW, TOP - 20, x + CW, BOT + 6], fill=(22, 14, 12, 255)); d.rectangle([x - CW, TOP - 20, x + CW, BOT + 6], outline=(90, 62, 40, 255), width=5)
    d.rectangle([76, TUN_TOP, 880, 1500], fill=(26, 18, 14, 235)); d.rectangle([76, TUN_TOP, 880, 1500], outline=(90, 62, 40, 255), width=5)
    for n in NAMES:
        d.rectangle([SX[n] - ROWH, BOT, SX[n] + ROWH, TUN_TOP + 3], fill=(22, 14, 12, 255))
layer(BOARD, carve)
BOARD.alpha_composite(PORTAL, (EXIT_X - PORTAL.width // 2, 1496 - PORTAL.height))
# ---------------- render
CARD = 1.1; END = T_WIN + CARD; NF = int(END * 30); NREW = 24   # n18: win card 1.1s, then a 0.8s rewind back to frame 0 (water drains)
T_THR = [e[0] for e in EV if e[1] == 'through' and e[2] == WIN][0]
GH = 0.5; T_CRK = 0.42; T_POP = 0.78          # n19: ghost-to-icon time; shield crack / pop times after BLOCKED
CARDX = 480
WY_THR = FR[int(round(T_THR * 30))][1]; GW = 2800.0   # once the floor is open, the water in his shaft falls by gravity
T_POUR = T_THR + math.sqrt(2 * max(0, TUN_TOP - WY_THR) / GW)
print('T_THR', round(T_THR, 2), 'T_POUR', T_POUR and round(T_POUR, 2), 'T_WIN', round(T_WIN, 2))
REW = False
def oev(e):
    if not REW: out_ev.append(e)
PRE = float(os.environ.get('PRE', '1.3')); PF = int(round(PRE * 30))   # n17: setup beat before digging starts
SEV = [(T_FLOOD, 'FLOOD!', (120, 200, 255), 'center', 0, 3, 1.2)]   # n18: was THE DAM BROKE!
for (te, kind, n) in EV:
    if te >= T_WIN: continue
    if kind == 'gum': SEV.append((te, PLAB[n], PCOL[n], n, 0, 3, 0.9))
    elif kind == 'blocked': SEV.append((te, 'BLOCKED!', (170, 255, 150), n, 0, 2, 0.7))
    elif kind == 'caught': SEV.append((te, LABEL[n] + ' OUT!', (255, 255, 255), n, 0, 3, 0.9))
STAMPS = Stamps().build(SEV, min_show=0.4)
STAMPS = [(a0, (min(b0, T_THR) if a0 < T_THR else b0),) + tuple(rest) for (a0, b0, *rest) in STAMPS]   # n18: nothing on screen over the breakthrough beat
print('stamps', [(round(a, 2), round(b, 2), tx) for a, b, tx, *_ in STAMPS])
ACV_ROW = sorted(G['joy']['gum'])[0]; wr = Writer(OUTD + '/noaudio.mp4'); out_ev = []
KEEP = {int(x) for x in os.environ.get('KEEP', '').split(',') if x}
rise = {}
def render(ta):
    t = ta - PRE; st, wy = FR[max(0, min(int(round(ta * 30)) - PF, len(FR) - 1))]
    img = BOARD.copy()
    # surface: Liza's village band with the river and a dam
    img.alpha_composite(HUB[int(t * 5) % len(HUB)], (0, 0))
    if ta < PRE + 0.4:                                   # n17: the goal glows while the setup reads
        pu = (ta * 1.6) % 1; al = int(200 * (1 - pu) * min(1, (PRE + 0.4 - ta) / 0.3))
        pr = 120 + 90 * pu; pcx, pcy = EXIT_X, 1496 - PORTAL.height // 2
        layer(img, lambda d: d.ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], outline=(120, 220, 255, al), width=10))
    # blocks
    for n in NAMES:
        s = st[n]; x = SX[n]
        for r in range(s['d'], NROWS):
            y = TOP + r * ROWH
            for c in (0, 1):
                img.alpha_composite(BLKC[n], (x - ROWH + c * ROWH, y))
            if r in G[n]['gum'] and r >= s['d']:
                gg = GUM[n]; img.alpha_composite(gg, (x - gg.width // 2, y + ROWH // 2 - gg.height // 2))
            hp0 = G[n]['hp0'][r]; hp = s['hp'][r] if r == s['d'] else hp0
            if hp < hp0:
                layer(img, lambda d: [d.line([x - 50 + q * 28, y + 10, x - 38 + q * 28, y + 70], fill=(40, 30, 30, 220), width=5) for q in range(hp0 - hp + 1)])
    # water: in each shaft from TOP-60 down to the dug floor (or the flood front), plus the surge from the dam
    def water(d):
        if wy < TOP - 70:
            # n17 setup: river water already trickling in along the street from the left, rising slowly until the dam breaks
            fx = min(W + 40, 340 + 330 * ta); hh = 34 + 12 * ta; base = TOP - 4   # n18: a clear wave front on frame 0
            pts = [(0, base)] + [(xx, base - hh - 4 * math.sin(xx * 0.06 - ta * 9) * min(1, (fx - xx) / 60)) for xx in range(0, int(fx) + 1, 12)] + [(fx, base)]
            if fx > 20: d.polygon(pts, fill=(60, 150, 240, 200))
            for xx in range(0, int(fx) - 10, 12):
                d.line([(xx, base - hh - 4 * math.sin(xx * 0.06 - ta * 9) * min(1, (fx - xx) / 60)), (xx + 12, base - hh - 4 * math.sin((xx + 12) * 0.06 - ta * 9) * min(1, (fx - xx - 12) / 60))], fill=(225, 245, 255, 240), width=6)
            for q in range(14):        # spray along the advancing front
                u = (ta * 2.2 + q * 0.071) % 1; bx = fx - 30 + u * 50 + (q % 3) * 8; by = base - hh - 10 - 40 * math.sin(u * 3.14) + (q % 4) * 4
                d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(220, 245, 255, int(230 * (1 - u))))
            return
        wav = lambda xx: 6 * math.sin(xx * 0.05 + t * 6)
        d.rectangle([0, TOP - 110, W, TOP - 10], fill=(60, 150, 240, 170))
        for n in NAMES:
            s = st[n]; floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else TUN_TOP
            bottom = min(wy, floor)
            if n == WIN and t >= T_THR: bottom = min(TUN_TOP, max(bottom, WY_THR + 0.5 * GW * (t - T_THR) ** 2))
            TBn = s['hold'] - HOLD if s['hold'] > 0 else -99
            if 0 <= t - TBn < HOLD and s['caught'] is None:
                btop = floor - 215
                if t - TBn < T_POP: bottom = min(bottom, btop)
                else: kk = min(1, (t - TBn - T_POP) / (HOLD - T_POP)); bottom = min(bottom, btop + (floor - 40 - btop) * kk * kk)
            if bottom > TOP - 20:
                d.rectangle([SX[n] - CW + 4, TOP - 20, SX[n] + CW - 4, bottom], fill=(60, 150, 240, 175))
                d.rectangle([SX[n] - CW + 4, bottom - 6, SX[n] + CW - 4, bottom], fill=(190, 230, 255, 200))
        if T_POUR is not None and t >= T_POUR:          # the winner's shaft drains into the chamber behind him
            u = t - T_POUR; xw = SX[WIN]; fall_ = min(1, u / 0.18); floor_y = 1496
            d.rectangle([xw - CW + 10, TUN_TOP - 4, xw + CW - 10, TUN_TOP + (floor_y - TUN_TOP) * fall_], fill=(60, 150, 240, 190))
            for q in range(5):
                yy = TUN_TOP + ((u * 520 + q * 40) % max(1, (floor_y - TUN_TOP) * fall_))
                d.line([xw - CW + 20 + q * 30, yy, xw - CW + 20 + q * 30, yy + 26], fill=(210, 240, 255, 200), width=5)
            if fall_ >= 1:
                ph_ = min(80, 150 * (u - 0.18)); xl = max(80, xw - 360 * (u - 0.18)); xr_ = min(876, xw + 200 * (u - 0.18))
                d.rectangle([xl, floor_y - ph_, xr_, floor_y], fill=(60, 150, 240, 185))
                d.rectangle([xl, floor_y - ph_ - 5, xr_, floor_y - ph_ + 3], fill=(200, 235, 255, 210))
        for q in range(26):
            bx = (q * 97 + t * 40) % W; by = TOP - ((t * 120 + q * 53) % 60)
            d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(220, 240, 255, 160))
    layer(img, water)
    # guides
    for n in NAMES:
        s = st[n]; x, y = s['x'], s['y']
        if s['caught'] is not None:
            u = t - s['caught']
            if u < GH:
                k = u / GH; e = k * k * (3 - 2 * k); sc = 1 - 0.62 * e
                ix, iy = SX[n], ROSTER_Y + 34; cx0, cy0 = x, y - 100
                bxc = cx0 + (ix - cx0) * e; byc = cy0 + (iy - cy0) * e
                spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # OUT = greyed
                spr = spr.resize((max(1, int(spr.width * sc)), max(1, int(spr.height * sc))), Image.NEAREST)
                img.alpha_composite(spr, (int(bxc - spr.width / 2), int(byc + 100 * sc - FT * sc)))
                rb = 100 * sc
                layer(img, lambda d: (d.ellipse([bxc - rb, byc - rb, bxc + rb, byc + rb], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=6), d.ellipse([bxc - rb * 0.62, byc - rb * 0.72, bxc - rb * 0.42, byc - rb * 0.52], fill=(255, 255, 255, 220))))
            elif u < GH + 0.25:                          # pops into the crossed-out tracker icon
                k = (u - GH) / 0.25; ix, iy = SX[n], ROSTER_Y + 34; r0 = 34 + 40 * k; al_ = int(255 * (1 - k))
                layer(img, lambda d: [d.line([ix + r0 * math.cos(a_), iy + r0 * math.sin(a_), ix + (r0 + 14) * math.cos(a_), iy + (r0 + 14) * math.sin(a_)], fill=(230, 245, 255, al_), width=6) for a_ in [q * 0.785 for q in range(8)]])
            if n not in rise and not REW: rise[n] = t; oev((round(t, 3), 'poof')); oev((round(t + GH, 3), 'poofpops'))
            continue
        if s['out'] is not None and t >= s['out']: continue
        if t < T_GO:
            i_ = NAMES.index(n); tp = 0.35 + 0.12 * i_          # n17: each guide spots the water, panics, then starts digging
            spr = STAND[n] if ta < tp else PANIC[n][int((ta - tp) * 12) % 8]
            if tp <= ta < tp + 0.7 and not REW:
                u_ = ta - tp; sc_ = 1.3 - 0.3 * min(1, u_ / 0.1)
                text_layer(img, [(x + 70, y - 235 - 10 * min(1, u_ / 0.1), '!', int(72 * sc_), (255, 214, 60), 8, int(255 * min(1, (tp + 0.7 - ta) / 0.12)))])
                if i_ == 0 and abs(ta - tp) < 0.5 / 30: oev((round(t, 3), 'boing'))
        elif s['phase'] == 'dig':
            ph = int((1 - max(0, s['nxt'] - t) / 0.3) * 7.99); spr = DIG[n][max(0, min(7, ph))]
            if t < s['sleep']: spr = DIG[n][0]
            if t - s['power'] < STR and n == 'cleo':      # rc12: power flames (the blue bubble read like Joy's shield)
                def flames(d, x=x, y=y):
                    for q in range(12):
                        a_ = q * 0.5236; fl = 26 + 14 * math.sin(t * 18 + q * 1.7)
                        bx, by_ = x + 100 * math.cos(a_), y - 100 + 118 * math.sin(a_)
                        d.polygon([(bx - 12, by_ + 8), (bx + 12, by_ + 8), (bx, by_ - fl)], fill=(255, 120 + 60 * (q % 2), 40, 210))
                layer(img, flames)
            if t - s['power'] < SPD and n == 'cyrus':
                layer(img, lambda d: [d.line([x + sd * (88 + 12 * ((q + int(t * 15)) % 2)), y - 188 + q * 42, x + sd * (88 + 12 * ((q + int(t * 15)) % 2)), y - 138 + q * 42 + 25], fill=(255, 190, 90, 230), width=7) for sd in (-1, 1) for q in range(4)] + [d.rectangle([x - 62 + q * 28 + 7 * math.sin(t * 20 + q), y - 28 - ((t * 90 + q * 13) % 38), x - 47 + q * 28 + 7 * math.sin(t * 20 + q), y - 13 - ((t * 90 + q * 13) % 38)], fill=(210, 180, 140, 170)) for q in range(5)])
        elif s['phase'] == 'fall': spr = PANIC[n][2]
        else:
            ph = int(t * 14) % 8; spr = (SRUN[n][ph] if EXIT_X > x else SRUN[n][ph].transpose(Image.FLIP_LEFT_RIGHT))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FT)))
        TBn = s['hold'] - HOLD if s['hold'] > 0 else -99
        if s['shield'] or (0 <= t - TBn < T_POP):
            layer(img, lambda d: (d.ellipse([x - 98, y - 215, x + 98, y + 15], fill=(120, 230, 110, 55)), d.ellipse([x - 98, y - 215, x + 98, y + 15], outline=(170, 255, 150, 235), width=7), d.ellipse([x - 72, y - 190, x - 50, y - 168], fill=(255, 255, 255, 200))))
            if T_CRK <= t - TBn < T_POP:                 # cracks spread across the bubble
                kc = (t - TBn - T_CRK) / (T_POP - T_CRK)
                CR = [[(0, -112), (-14, -80), (8, -52), (-6, -20)], [(-60, -150), (-36, -128), (-46, -100)], [(58, -146), (34, -118), (48, -86), (30, -60)]]
                layer(img, lambda d: [d.line([(x + px_, y - 100 + py_) for px_, py_ in cr[:max(2, int(len(cr) * min(1, kc * 1.6)))]], fill=(250, 255, 245, 245), width=5) for cr in CR[:1 + int(kc * 2.99)]])
                if abs(t - TBn - T_CRK) < 0.5 / 30: oev((round(t, 3), 'crunch_8bit'))
        if s['hold'] > 0 and 0 <= t - (TBn + T_POP) < 0.3:      # shield POP (ring bursts into shards)
            u_ = (t - (TBn + T_POP)) / 0.3; al_ = int(255 * (1 - u_)); r0 = 100 + 70 * u_; cy_ = y - 100
            layer(img, lambda d: [d.line([x + r0 * math.cos(a_), cy_ + r0 * math.sin(a_), x + (r0 + 26) * math.cos(a_), cy_ + (r0 + 26) * math.sin(a_)], fill=(170, 255, 150, al_), width=8) for a_ in [q * 0.785 + 0.3 for q in range(8)]]
                  + [d.ellipse([x + (r0 - 20) * math.cos(a_) - 7, cy_ + (r0 - 20) * math.sin(a_) - 7 + 60 * u_ * u_, x + (r0 - 20) * math.cos(a_) + 7, cy_ + (r0 - 20) * math.sin(a_) + 7 + 60 * u_ * u_], fill=(200, 255, 190, al_)) for a_ in [q * 0.785 for q in range(8)]])
            if abs(t - (TBn + T_POP)) < 0.5 / 30: oev((round(t, 3), 'poofpops'))
        if t < s['sleep'] and s['phase'] == 'dig':
            u = (t * 1.3) % 1
            text_layer(img, [(min(x + 50, 840), y - 238 - 40 * u, 'Z', 62, (220, 190, 255), 8, int(255 * (1 - u))), (min(x + 100, 860), y - 296 - 40 * u, 'z', 48, (220, 190, 255), 7, int(255 * (1 - u)))])
        if s['drop'] > 0 and 0 <= t - s['drop'] < 0.25 and s['phase'] == 'dig':
            u = (t - s['drop']) / 0.25
            layer(img, lambda d: [d.rectangle([x - 75 + q * 30, y - 12 - u * 50 + (q % 2) * 12, x - 60 + q * 30, y + 3 - u * 50 + (q % 2) * 12], fill=RING[n] + (int(255 * (1 - u)),)) for q in range(6)])
    # popups and sounds
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    for (te, kind, n) in EV:
        if abs(t - te) < 0.5 / 30:
            snd = {'hit': 'stomp_8bit', 'break': 'brick_8bit', 'gum': 'powerup_8bit', 'out': 'vg02', 'blocked': 'sword_hit'}.get(kind)
            if snd: oev((round(te, 3), snd))
        u = t - te
        if REW: continue
        if kind == 'gum' and 0 <= u < 1.0:
            if n == 'ray' and u < 0.6:
                r_ = 60 + 900 * u; dd.ellipse([SX[n] - r_, st[n]['y'] - 100 - r_, SX[n] + r_, st[n]['y'] - 100 + r_], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14)
    img.alpha_composite(L)
    # dam break flash
    if T_FLOOD <= t < T_FLOOD + 1.4:
        if not any(e[1] == 'boom' for e in out_ev): oev((T_FLOOD, 'boom'))
    # n18: Rayleigh's breakthrough gets its own beat (flash + purple burst at the shaft floor)
    if not REW and 0 <= t - T_THR < 0.5:
        u = (t - T_THR) / 0.5; bxw = SX[WIN]; byw = BOT
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 255, int(170 * max(0, 1 - u / 0.3)))))
        layer(img, lambda dd: [dd.ellipse([bxw - r_, byw - r_ * 0.6, bxw + r_, byw + r_ * 0.6], outline=(210, 150, 255, int(240 * (1 - u))), width=12) for r_ in (60 + 420 * u, 20 + 260 * u)]
              + [dd.rectangle([bxw + (q - 3.5) * 34 - 9, byw - 40 + 300 * u * u - 120 * u * (q % 3), bxw + (q - 3.5) * 34 + 9, byw - 22 + 300 * u * u - 120 * u * (q % 3)], fill=RING[WIN] + (int(255 * (1 - u)),)) for q in range(8)])
        if abs(t - T_THR) < 0.5 / 30: oev((round(t, 3), 'powerup1')); oev((round(t, 3), 'brick_8bit'))
    # header
    for i, n in enumerate(NAMES):
        ix = SX[n]; ic = ICON[n]; s = st[n]
        icc = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55) if (s['caught'] is not None and t >= s['caught'] + GH) else ic
        img.alpha_composite(icc, (ix - ic.width // 2, ROSTER_Y))
        d = ImageDraw.Draw(img)
        if s['caught'] is not None and t >= s['caught'] + GH:
            d.line([ix - 24, ROSTER_Y + 10, ix + 24, ROSTER_Y + 58], fill=(230, 50, 50), width=8); d.line([ix - 24, ROSTER_Y + 58, ix + 24, ROSTER_Y + 10], fill=(230, 50, 50), width=8)
        if s['out'] is not None and t >= s['out']: d.ellipse([ix - 40, ROSTER_Y - 6, ix + 40, ROSTER_Y + 74], outline=(255, 214, 60), width=6)
    # rc12: stamps (one at a time, over the guide or mid-board; never on the portal)
    for (a0, b0, tx, c0, n0, _, pr) in STAMPS:
        if a0 <= t < b0 and t < T_WIN and not REW:
            u = t - a0; sc = 1.25 - 0.25 * min(1, u / 0.12); al = int(255 * min(1, (b0 - t) / 0.12))
            if n0 == 'center':
                plate(img, CARDX, TOP - 95, tx, 64, c0, al, scale=sc, border=(120, 200, 255))   # n18: FLOOD! above the columns
            else:
                s_ = st[n0]; yy_ = s_['y'] - 300
                plate(img, SX[n0], max(ROSTER_Y + 84, min(yy_, 1200)), tx, 56 if len(tx) > 10 else 60, c0, al, scale=sc, border=(255, 90, 60) if 'OUT' in tx else None)
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, ROSTER_Y + 80, W, H], fill=(6, 8, 18, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CARDX - vf.width // 2, 1140 - vf.height))
        plate(img, CARDX, 1150, LABEL[WIN], 64, (255, 214, 60), int(255 * a))
        plate(img, CARDX, 1252, 'SURVIVED!', 64, (255, 214, 60), int(255 * a))
        if not any(e[1] == 'victory' for e in out_ev): oev((round(T_WIN + 0.05, 3), 'victory'))
    img.alpha_composite(HOOK2 if t >= T_WIN else HOOK)
    return img
for f in range(NF + PF):
    img = render(f / 30); wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
REW = True; TA0 = PRE + T_WIN - 1 / 30; out_ev.append((round(T_WIN + CARD - 0.05, 3), 'rewind'))
for i in range(NREW):
    u = (i + 1) / NREW; ta = TA0 * (1 - u) ** 1.15
    img = render(ta)
    tint = Image.new('RGBA', (W, H), (40, 70, 140, int(70 * math.sin(math.pi * u)))); img.alpha_composite(tint)
    layer(img, lambda dd: [dd.rectangle([0, (yy + i * 53) % H, W, (yy + i * 53) % H + 6], fill=(230, 240, 255, 60)) for yy in (300, 900, 1400)])
    wr.write(img)
    if NF + PF + i in KEEP: img.convert('RGB').save(OUTD + f'/k_{NF + PF + i:04d}.png')
wr.close()
# thin out dig thuds
out = []; last = -9
for e in sorted((round(a + PRE, 3), b) for a, b in out_ev):
    if e[1] == 'stomp_8bit':
        if e[0] - last < 0.12: continue
        last = e[0]
    out.append(e)
json.dump({'events': out}, open(OUTD + '/ev.json', 'w'))
print('done', round(END, 2), len(out))
