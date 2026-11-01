import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
SX = {n: 140 + i * 200 for i, n in enumerate(NAMES)}
TOP = 600; ROWH = 64; NROWS = 13; BOT = TOP + NROWS * ROWH          # shaft bottom
TUNNEL_Y = 1745; EXIT_X = 540
T_GO, T_FLOOD = 2.4, 3.4
FA, FB = float(os.environ.get('FA', '60')), float(os.environ.get('FB', '3.5'))
def sim(seed):
    rnd = random.Random(seed)
    g = {}
    for n in NAMES:
        hp = [rnd.choice([1, 1, 2, 2, 2, 3]) for _ in range(NROWS)]
        gum = set(rnd.sample(range(2, NROWS - 2), 1))
        g[n] = dict(d=0, hp=list(hp), hp0=list(hp), gum=gum, nxt=T_GO + rnd.uniform(0.1, 0.4), iv=rnd.uniform(0.34, 0.41), power=-9, caught=None,
                    out=None, x=float(SX[n]), y=float(TOP), phase='dig', ph=rnd.uniform(0, 6.3), hits=0, drop=-9, gotgum=[])
    frames = []; ev = []
    for f in range(int(40 * 30)):
        t = f / 30; dt = 1 / 30
        fl = -99 if t < T_FLOOD else (t - T_FLOOD) * (FA + FB * (t - T_FLOOD))      # flood front depth below TOP
        wy = TOP - 70 + fl                                                          # water surface y
        for n, s in g.items():
            if s['caught'] is not None or s['out'] is not None: continue
            if s['phase'] == 'dig':
                if t >= s['nxt'] and t >= T_GO:
                    iv = s['iv'] * (1 + 0.15 * math.sin(t * 0.9 + s['ph']))
                    if t - s['power'] < 1.6: iv *= 0.4
                    s['nxt'] = t + iv; s['hits'] += 1
                    s['hp'][s['d']] -= 1; ev.append((t, 'hit', n))
                    if s['hp'][s['d']] <= 0:
                        if s['d'] in s['gum']: s['power'] = t; ev.append((t, 'gum', n)); s['gotgum'].append(t)
                        s['d'] += 1; s['drop'] = t; ev.append((t, 'break', n))
                        if s['d'] >= NROWS: s['phase'] = 'fall'
                s['y'] = TOP + s['d'] * ROWH
                if wy > s['y'] - 40: s['caught'] = t; ev.append((t, 'caught', n))
            elif s['phase'] == 'fall':
                s['y'] += 900 * dt
                if s['y'] >= TUNNEL_Y: s['y'] = TUNNEL_Y; s['phase'] = 'run'
            elif s['phase'] == 'run':
                dx = EXIT_X - s['x']; st = 420 * dt
                if abs(dx) <= st: s['x'] = EXIT_X; s['out'] = t; ev.append((t, 'out', n))
                else: s['x'] += st * (1 if dx > 0 else -1)
        frames.append(({n: dict(d=s['d'], hp=list(s['hp']), x=s['x'], y=s['y'], phase=s['phase'], caught=s['caught'], out=s['out'], power=s['power'], drop=s['drop'], nxt=s['nxt']) for n, s in g.items()}, wy))
        if all(s['caught'] is not None or s['out'] is not None for s in g.values()):
            last = max([s['caught'] or 0 for s in g.values()] + [s['out'] or 0 for s in g.values()])
            if t > last + 0.1: break
    return frames, ev, g
def score(seed):
    fr, ev, g = sim(seed)
    outs = sorted((s['out'], n) for n, s in g.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in g.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != 4: return None
    tw, w = outs[0]
    if not (11 < tw < 15.5): return None
    if max(caught) < tw - 2.5: return None
    # closeness: second-deepest digger rows remaining when winner broke through
    return round(tw, 2), w, [round(c, 1) for c in caught]
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
GUM = {n: gummy(GK[n], 2) for n in NAMES}
PORTAL = crop(Image.open('portal/12.png').convert('RGBA')); PORTAL = up(PORTAL, 4)
CAVE = Image.open('cave/00.png').convert('RGB')
k_ = max(W / CAVE.width, H / CAVE.height); CAVE = CAVE.resize((int(CAVE.width * k_) + 1, int(CAVE.height * k_) + 1), Image.NEAREST)
CAVE = ImageEnhance.Brightness(CAVE.crop((0, 0, W, H))).enhance(0.72).convert('RGBA')
HUB = bg_frames('hub.gif', (1920 * 300 // 1080 * 2, 600), step=4)
HUB = [ImageEnhance.Brightness(f.crop((300, 150, 300 + W, 150 + 260))).enhance(0.95).convert('RGBA') for f in HUB]
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
    d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], fill=(26, 18, 14, 235)); d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], outline=(90, 62, 40, 255), width=5)
    for n in NAMES:
        d.rectangle([SX[n] - 64, BOT, SX[n] + 64, TUNNEL_Y - 170], fill=(22, 14, 12, 255))
layer(BOARD, carve)
BOARD.alpha_composite(PORTAL, (EXIT_X - PORTAL.width // 2, TUNNEL_Y + 30 - PORTAL.height))
# ---------------- render
END = T_WIN + 3.0; NF = int(END * 30); wr = Writer('flood_noaudio.mp4'); out_ev = []
rise = {}
for f in range(NF):
    t = f / 30; st, wy = FR[min(f, len(FR) - 1)]
    img = BOARD.copy()
    # surface: Liza's village band with the river and a dam
    img.alpha_composite(HUB[int(t * 5) % len(HUB)], (0, 330))
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
        d.rectangle([0, 560, W, TOP - 10], fill=(60, 150, 240, 170))
        for n in NAMES:
            s = st[n]; floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else (TUNNEL_Y - 170 if s['phase'] != 'dig' else BOT)
            bottom = min(wy, floor)
            if bottom > TOP - 20:
                d.rectangle([SX[n] - 66, TOP - 20, SX[n] + 66, bottom], fill=(60, 150, 240, 175))
                d.rectangle([SX[n] - 66, bottom - 6, SX[n] + 66, bottom], fill=(190, 230, 255, 200))
            if s['phase'] != 'dig' and wy > BOT:
                lv = min(TUNNEL_Y + 40, TUNNEL_Y - 170 + (wy - BOT))
                d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], fill=(0, 0, 0, 0))
        for q in range(26):
            bx = (q * 97 + t * 40) % W; by = 600 - ((t * 120 + q * 53) % 60)
            d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(220, 240, 255, 160))
    layer(img, water)
    # guides
    for n in NAMES:
        s = st[n]; x, y = s['x'], s['y']
        if s['caught'] is not None:
            u = t - s['caught']; by = max(520, y - 60 - u * 260) + 8 * math.sin(t * 3)
            spr = PANIC[n][int(t * 10) % 8]
            img.alpha_composite(spr, (int(x - spr.width / 2), int(by - 156 + 20)))
            layer(img, lambda d: d.ellipse([x - 70, by - 150, x + 70, by + 10], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=5))
            layer(img, lambda d: d.ellipse([x - 52, by - 132, x - 36, by - 116], fill=(255, 255, 255, 220)))
            if n not in rise: rise[n] = t; out_ev.append((round(t, 3), 'poof'))
            continue
        if s['out'] is not None and t >= s['out']: continue
        if t < T_GO: spr = STAND[n]
        elif s['phase'] == 'dig':
            ph = int((1 - max(0, s['nxt'] - t) / 0.3) * 7.99); spr = DIG[n][max(0, min(7, ph))]
            if t - s['power'] < 1.6:
                layer(img, lambda d: d.ellipse([x - 80, y - 170, x + 80, y + 10], fill=(255, 220, 120, 60)))
        elif s['phase'] == 'fall': spr = PANIC[n][2]
        else:
            ph = int(t * 14) % 8; spr = (SRUN[n][ph] if EXIT_X > x else SRUN[n][ph].transpose(Image.FLIP_LEFT_RIGHT))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))
        if s['drop'] > 0 and 0 <= t - s['drop'] < 0.25 and s['phase'] == 'dig':
            u = (t - s['drop']) / 0.25
            layer(img, lambda d: [d.rectangle([x - 60 + q * 24, y - 10 - u * 40 + (q % 2) * 10, x - 48 + q * 24, y + 2 - u * 40 + (q % 2) * 10], fill=RING[n] + (int(255 * (1 - u)),)) for q in range(6)])
    # popups and sounds
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    for (te, kind, n) in EV:
        if abs(t - te) < 0.5 / 30:
            snd = {'hit': 'stomp_8bit', 'break': 'brick_8bit', 'gum': 'powerup_8bit', 'out': 'vg02'}.get(kind)
            if snd: out_ev.append((round(te, 3), snd))
        u = t - te
        if kind == 'gum' and 0 <= u < 1.0:
            a = int(255 * min(1, (1 - u) / 0.3)); ctext(dd, SX[n], st[n]['y'] - 240 - u * 40, 'POWER DIG!', F(26), (255, 214, 60), 5, a)
    img.alpha_composite(L)
    # dam break flash
    if T_FLOOD <= t < T_FLOOD + 1.4:
        a = int(255 * min(1, (T_FLOOD + 1.4 - t) / 0.4))
        text_layer(img, [(W / 2, 470, 'THE DAM BROKE!', 56, (120, 200, 255), 8, a)])
        if not any(e[1] == 'boom' for e in out_ev): out_ev.append((T_FLOOD, 'boom'))
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 330], fill=(10, 14, 30, 230)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 34, 'WHO SURVIVES', F(64)); ctext(d, W / 2, 118, 'THE FLOOD?', F(64), (120, 200, 255))
    for i, n in enumerate(NAMES):
        ix = SX[n]; ic = ICON[n]; s = st[n]
        icc = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55) if s['caught'] is not None else ic
        img.alpha_composite(icc, (ix - ic.width // 2, 214))
        d = ImageDraw.Draw(img)
        if s['caught'] is not None:
            d.line([ix - 24, 224, ix + 24, 272], fill=(230, 50, 50), width=8); d.line([ix - 24, 272, ix + 24, 224], fill=(230, 50, 50), width=8)
        if s['out'] is not None and t >= s['out']: d.ellipse([ix - 40, 208, ix + 40, 288], outline=(255, 214, 60), width=6)
    if t < T_GO + 0.3:
        text_layer(img, [(W / 2, 1500, 'PICK ONE!', 60, (255, 255, 255), 8, 255)])
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 330, W, H], fill=(6, 8, 18, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(W / 2, 1230, LABEL[WIN] + ' SURVIVED!', 44 if len(LABEL[WIN]) > 8 else 60, (255, 214, 60), 8, 255)])
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN + 0.05, 3), 'victory'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/w_{f:04d}.png')
wr.close()
# thin out dig thuds
out = []; last = -9
for e in sorted(out_ev):
    if e[1] == 'stomp_8bit':
        if e[0] - last < 0.12: continue
        last = e[0]
    out.append(e)
json.dump({'events': out}, open('flood_events.json', 'w'))
print('done', round(END, 2), len(out))
