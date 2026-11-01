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
SX = {n: 193 + i * 190 for i, n in enumerate(NAMES)}
TOP = 720; ROWH = 64; NROWS = int(os.environ.get('NROWS', '9')); BOT = TOP + NROWS * ROWH          # shaft bottom
TUNNEL_Y = 1484; TUN_TOP = 1316; EXIT_X = 478
PLAB = {'joy': 'SHIELD!', 'cyrus': 'SPEED!', 'cleo': 'STRENGTH!', 'ray': 'SLEEP!'}
PCOL = {'joy': (120, 230, 110), 'cyrus': (255, 170, 60), 'cleo': (110, 170, 255), 'ray': (200, 130, 255)}
T_GO, T_FLOOD = float(os.environ.get('TG', '0.0')), float(os.environ.get('TF', '1.6'))   # rc12: digging from frame 0, dam breaks at 1.6s
FA, FB = float(os.environ.get('FA', '60')), float(os.environ.get('FB', '3.5'))
def sim(seed):
    rnd = random.Random(seed)
    g = {}
    for n in NAMES:
        hp = [rnd.choice([1, 1, 2, 2, 2, 3]) for _ in range(NROWS)]
        gum = set(rnd.sample(range(1, NROWS - 3), 1))
        g[n] = dict(d=0, hp=list(hp), hp0=list(hp), gum=gum, nxt=T_GO + rnd.uniform(0.1, 0.4), iv=rnd.uniform(0.40, 0.48) * float(os.environ.get('IVK', '1')), power=-9, caught=None,
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
                    if n == 'cyrus' and t - s['power'] < 1.6: iv *= 0.4                  # SPEED
                    s['nxt'] = t + iv; s['hits'] += 1
                    dmg = 3 if (n == 'cleo' and t - s['power'] < 1.6) else 1                # STRONG: one smash per block
                    s['hp'][s['d']] -= dmg; ev.append((t, 'hit', n))
                    if s['hp'][s['d']] <= 0:
                        if s['d'] in s['gum']:
                            s['power'] = t; ev.append((t, 'gum', n)); s['gotgum'].append(t)
                            if n == 'joy': s['shield'] = True
                            if n == 'ray':
                                for m, o in g.items():
                                    if m == n or o['caught'] is not None or o['out'] is not None or o['phase'] != 'dig': continue
                                    if o['shield']: o['shield'] = False; ev.append((t, 'blocked', m))
                                    else: o['sleep'] = t + 1.0; ev.append((t, 'sleep', m))
                        s['d'] += 1; s['drop'] = t; ev.append((t, 'break', n))
                        if s['d'] >= NROWS: s['phase'] = 'fall'
                s['y'] = TOP + s['d'] * ROWH
                if wy > s['y'] - 40 and t >= s['hold']:
                    if s['shield']: s['shield'] = False; s['hold'] = t + 0.9; ev.append((t, 'blocked', n))
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
DIG = {'joy': seq('joy_dig', 2, 1, 9), 'cyrus': seq('cyrus_dig2', 2, 1, 9), 'cleo': seq('cleo_dig', 2, 1, 9), 'ray': seq('ray_dig', 2, 1, 9), 'hollow': seq('hollow_dig', 2, 1, 9)}
STAND = {n: seq(f'../pixellab/maze/anim/{n}_frun', 2, 0, 1)[0] for n in NAMES}
FRUN = {n: seq(f'../pixellab/maze/anim/{n}_frun', 2, 1, 9) for n in NAMES}
SRUN = {n: seq(f'../pixellab/race/{n}_run', 2, 1, 9) for n in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq('../pixellab/maze/anim/hollow_srun', 2, 1, 9)
PANIC = {n: seq(f'../pixellab/maze/anim/{n}_panic', 2, 1, 9) for n in NAMES}
BLK = crop(Image.open('block/07.png').convert('RGBA')).resize((64, 64), Image.NEAREST)
def tint(im, col, k=0.55):
    a = np.array(im).astype(np.float32); c = np.array(col, np.float32)
    a[..., :3] = a[..., :3] * (1 - k) + (a[..., :3] / 255.0) * c * k * 1.25
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
BLKC = {n: tint(BLK, RING[n]) for n in NAMES}
GUM = {n: gummy(GK[n], 2) for n in NAMES}; GUM['joy'] = up(gummy_src('acv'), 2)
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
        x = SX[n]; d.rectangle([x - 70, TOP - 20, x + 70, BOT + 6], fill=(22, 14, 12, 255)); d.rectangle([x - 70, TOP - 20, x + 70, BOT + 6], outline=(90, 62, 40, 255), width=5)
    d.rectangle([76, TUN_TOP, 880, 1500], fill=(26, 18, 14, 235)); d.rectangle([76, TUN_TOP, 880, 1500], outline=(90, 62, 40, 255), width=5)
    for n in NAMES:
        d.rectangle([SX[n] - 64, BOT, SX[n] + 64, TUN_TOP + 3], fill=(22, 14, 12, 255))
layer(BOARD, carve)
BOARD.alpha_composite(PORTAL, (EXIT_X - PORTAL.width // 2, 1496 - PORTAL.height))
# ---------------- render
END = T_WIN + 1.5; NF = int(END * 30)
SEV = [(T_FLOOD, 'THE DAM BROKE!', (120, 200, 255), 'center', 0, 3, 1.5)]   # with REACH THE PORTAL! under it
for (te, kind, n) in EV:
    if te >= T_WIN: continue
    if kind == 'gum': SEV.append((te, PLAB[n], PCOL[n], n, 0, 3, 0.9))
    elif kind == 'blocked': SEV.append((te, 'BLOCKED!', (170, 255, 150), n, 0, 2, 0.7))
    elif kind == 'caught': SEV.append((te, LABEL[n] + ' OUT!', (255, 255, 255), n, 0, 3, 0.9))
STAMPS = Stamps().build(SEV, min_show=0.4)
print('stamps', [(round(a, 2), round(b, 2), tx) for a, b, tx, *_ in STAMPS])
ACV_ROW = sorted(G['joy']['gum'])[0]; wr = Writer(OUTD + '/noaudio.mp4'); out_ev = []
KEEP = {int(x) for x in os.environ.get('KEEP', '').split(',') if x}
rise = {}
for f in range(NF):
    t = f / 30; st, wy = FR[min(f, len(FR) - 1)]
    img = BOARD.copy()
    # surface: Liza's village band with the river and a dam
    img.alpha_composite(HUB[int(t * 5) % len(HUB)], (0, 0))
    # blocks
    for n in NAMES:
        s = st[n]; x = SX[n]
        for r in range(s['d'], NROWS):
            y = TOP + r * ROWH
            for c in (0, 1):
                img.alpha_composite(BLKC[n], (x - 64 + c * 64, y))
            if r in G[n]['gum'] and r >= s['d']:
                gg = GUM[n]; img.alpha_composite(gg, (x - gg.width // 2, y + 32 - gg.height // 2))
            hp0 = G[n]['hp0'][r]; hp = s['hp'][r] if r == s['d'] else hp0
            if hp < hp0:
                layer(img, lambda d: [d.line([x - 40 + q * 22, y + 8, x - 30 + q * 22, y + 56], fill=(40, 30, 30, 220), width=4) for q in range(hp0 - hp + 1)])
    # water: in each shaft from TOP-60 down to the dug floor (or the flood front), plus the surge from the dam
    def water(d):
        if wy < TOP - 70: return
        wav = lambda xx: 6 * math.sin(xx * 0.05 + t * 6)
        d.rectangle([0, TOP - 110, W, TOP - 10], fill=(60, 150, 240, 170))
        for n in NAMES:
            s = st[n]; floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else TUN_TOP
            bottom = min(wy, floor)
            if bottom > TOP - 20:
                d.rectangle([SX[n] - 66, TOP - 20, SX[n] + 66, bottom], fill=(60, 150, 240, 175))
                d.rectangle([SX[n] - 66, bottom - 6, SX[n] + 66, bottom], fill=(190, 230, 255, 200))
        for q in range(26):
            bx = (q * 97 + t * 40) % W; by = TOP - ((t * 120 + q * 53) % 60)
            d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(220, 240, 255, 160))
    layer(img, water)
    # guides
    for n in NAMES:
        s = st[n]; x, y = s['x'], s['y']
        if s['caught'] is not None:
            u = t - s['caught']; by = max(TOP - 10, y - 60 - u * 260) + 8 * math.sin(t * 3)
            spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # rc12: OUT = greyed
            img.alpha_composite(spr, (int(x - spr.width / 2), int(by - 156 + 20)))
            layer(img, lambda d: d.ellipse([x - 70, by - 150, x + 70, by + 10], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=5))
            layer(img, lambda d: d.ellipse([x - 52, by - 132, x - 36, by - 116], fill=(255, 255, 255, 220)))
            if n not in rise: rise[n] = t; out_ev.append((round(t, 3), 'poof'))
            continue
        if s['out'] is not None and t >= s['out']: continue
        if t < T_GO: spr = STAND[n]
        elif s['phase'] == 'dig':
            ph = int((1 - max(0, s['nxt'] - t) / 0.3) * 7.99); spr = DIG[n][max(0, min(7, ph))]
            if t < s['sleep']: spr = DIG[n][0]
            if t - s['power'] < 1.6 and n == 'cleo':      # rc12: power flames (the blue bubble read like Joy's shield)
                def flames(d, x=x, y=y):
                    for q in range(12):
                        a_ = q * 0.5236; fl = 26 + 14 * math.sin(t * 18 + q * 1.7)
                        bx, by_ = x + 80 * math.cos(a_), y - 80 + 95 * math.sin(a_)
                        d.polygon([(bx - 12, by_ + 8), (bx + 12, by_ + 8), (bx, by_ - fl)], fill=(255, 120 + 60 * (q % 2), 40, 210))
                layer(img, flames)
            if t - s['power'] < 1.6 and n == 'cyrus':
                layer(img, lambda d: [d.line([x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 150 + q * 34, x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 110 + q * 34 + 20], fill=(255, 190, 90, 230), width=6) for sd in (-1, 1) for q in range(4)] + [d.rectangle([x - 50 + q * 22 + 6 * math.sin(t * 20 + q), y - 22 - ((t * 90 + q * 13) % 30), x - 38 + q * 22 + 6 * math.sin(t * 20 + q), y - 10 - ((t * 90 + q * 13) % 30)], fill=(210, 180, 140, 170)) for q in range(5)])
        elif s['phase'] == 'fall': spr = PANIC[n][2]
        else:
            ph = int(t * 14) % 8; spr = (SRUN[n][ph] if EXIT_X > x else SRUN[n][ph].transpose(Image.FLIP_LEFT_RIGHT))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))
        if s['shield'] or (s['hold'] > 0 and 0 <= t - s['hold'] + 0.9 < 0.9):
            layer(img, lambda d: (d.ellipse([x - 78, y - 172, x + 78, y + 12], fill=(120, 230, 110, 55)), d.ellipse([x - 78, y - 172, x + 78, y + 12], outline=(170, 255, 150, 235), width=6), d.ellipse([x - 58, y - 152, x - 40, y - 134], fill=(255, 255, 255, 200))))
        if t < s['sleep'] and s['phase'] == 'dig':
            u = (t * 1.3) % 1
            text_layer(img, [(min(x + 40, 840), y - 190 - 40 * u, 'Z', 58, (220, 190, 255), 8, int(255 * (1 - u))), (min(x + 84, 860), y - 240 - 40 * u, 'z', 44, (220, 190, 255), 7, int(255 * (1 - u)))])
        if s['drop'] > 0 and 0 <= t - s['drop'] < 0.25 and s['phase'] == 'dig':
            u = (t - s['drop']) / 0.25
            layer(img, lambda d: [d.rectangle([x - 60 + q * 24, y - 10 - u * 40 + (q % 2) * 10, x - 48 + q * 24, y + 2 - u * 40 + (q % 2) * 10], fill=RING[n] + (int(255 * (1 - u)),)) for q in range(6)])
    # popups and sounds
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    for (te, kind, n) in EV:
        if abs(t - te) < 0.5 / 30:
            snd = {'hit': 'stomp_8bit', 'break': 'brick_8bit', 'gum': 'powerup_8bit', 'out': 'vg02', 'blocked': 'sword_hit'}.get(kind)
            if snd: out_ev.append((round(te, 3), snd))
        u = t - te
        if kind == 'gum' and 0 <= u < 1.0:
            if n == 'ray' and u < 0.6:
                r_ = 60 + 900 * u; dd.ellipse([SX[n] - r_, st[n]['y'] - 80 - r_, SX[n] + r_, st[n]['y'] - 80 + r_], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14)
    img.alpha_composite(L)
    # dam break flash
    if T_FLOOD <= t < T_FLOOD + 1.4:
        if not any(e[1] == 'boom' for e in out_ev): out_ev.append((T_FLOOD, 'boom'))
    # header
    for i, n in enumerate(NAMES):
        ix = SX[n]; ic = ICON[n]; s = st[n]
        icc = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55) if s['caught'] is not None else ic
        img.alpha_composite(icc, (ix - ic.width // 2, ROSTER_Y))
        d = ImageDraw.Draw(img)
        if s['caught'] is not None:
            d.line([ix - 24, ROSTER_Y + 10, ix + 24, ROSTER_Y + 58], fill=(230, 50, 50), width=8); d.line([ix - 24, ROSTER_Y + 58, ix + 24, ROSTER_Y + 10], fill=(230, 50, 50), width=8)
        if s['out'] is not None and t >= s['out']: d.ellipse([ix - 40, ROSTER_Y - 6, ix + 40, ROSTER_Y + 74], outline=(255, 214, 60), width=6)
    # rc12: stamps (one at a time, over the guide or mid-board; never on the portal)
    for (a0, b0, tx, c0, n0, _, pr) in STAMPS:
        if a0 <= t < b0 and t < T_WIN:
            u = t - a0; sc = 1.25 - 0.25 * min(1, u / 0.12); al = int(255 * min(1, (b0 - t) / 0.12))
            if n0 == 'center':
                plate(img, EXIT_X, 1020, tx, 60, c0, al, scale=sc, border=(120, 200, 255))
            else:
                s_ = st[n0]; yy_ = (max(TOP - 10, s_['y'] - 60 - (t - s_['caught']) * 260) - 150) if s_['caught'] is not None else s_['y'] - 250
                plate(img, SX[n0], max(ROSTER_Y + 84, min(yy_, 1200)), tx, 56 if len(tx) > 10 else 60, c0, al, scale=sc, border=(255, 90, 60) if 'OUT' in tx else None)
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, ROSTER_Y + 80, W, H], fill=(6, 8, 18, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (EXIT_X - vf.width // 2, 1140 - vf.height))
        plate(img, EXIT_X, 1150, LABEL[WIN], 64, (255, 214, 60), int(255 * a))
        plate(img, EXIT_X, 1252, 'SURVIVED!', 64, (255, 214, 60), int(255 * a))
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN + 0.05, 3), 'victory'))
    img.alpha_composite(HOOK2 if t >= T_WIN else HOOK)
    wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
wr.close()
# thin out dig thuds
out = []; last = -9
for e in sorted(out_ev):
    if e[1] == 'stomp_8bit':
        if e[0] - last < 0.12: continue
        last = e[0]
    out.append(e)
json.dump({'events': out}, open(OUTD + '/ev.json', 'w'))
print('done', round(END, 2), len(out))
