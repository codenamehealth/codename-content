import sys; sys.path.insert(0, '../fork1')
from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['ray', 'cyrus', 'joy', 'cleo', 'hollow']
NAME = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
COL = {'joy': (110, 210, 90), 'cyrus': (255, 160, 40), 'cleo': (100, 160, 255), 'ray': (190, 110, 240), 'hollow': (190, 180, 220)}
GUM = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
SIDE = {g: f'../pixellab/race/in/{g}_side.png' for g in ['joy', 'cyrus', 'cleo', 'ray']}; SIDE['hollow'] = '../syeda_src/hollow/char2.png'
SPR = {g: up(Image.open(p).convert('RGBA'), 2) for g, p in SIDE.items()}          # feet at y=156
BOARD = up(crop(Image.open('surfboard/02.png').convert('RGBA')), 2)
LH = up(crop(Image.open('lighthouse/01.png').convert('RGBA')), 3)
BUOY = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('../fork4/buoy/*.png'))]
SLIME = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('../pixellab/race/slime_idle_c/*.png'))]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLIME = [nored(s) for s in SLIME]
OCEAN = Image.open('ocean/00.png').convert('RGBA')
SKY = OCEAN.resize((OCEAN.width * 3, OCEAN.height * 3), Image.NEAREST)        # 1344x768
SKYX = (SKY.width - W) // 2
LY = [860 + i * 205 for i in range(5)]
COURSE = 6600; T0 = 3.0
# ---------- sim
def sim(seed):
    rnd = random.Random(seed)
    order = list(G)
    st = {g: dict(x=0.0, v=0.0, base=rnd.uniform(355, 380), ph=rnd.uniform(0, 6.3), boost=-9, bonk=-9, fin=None) for g in G}
    items = []
    for li, g in enumerate(G):
        for k in range(2):
            items.append(dict(kind='gum', lane=li, x=rnd.uniform(900 + k * 2600, 2600 + k * 2600), got=None))
        for k in range(2):
            items.append(dict(kind='slime', lane=li, x=rnd.uniform(1400 + k * 2400, 3000 + k * 2400), got=None))
    frames = []; ev = []
    f = 0
    while True:
        t = f / FPS
        if t > T0:
            for li, g in enumerate(G):
                s = st[g]
                if s['fin'] is not None: continue
                sp = s['base'] * (1 + 0.16 * math.sin(0.8 * t + s['ph']) + 0.08 * math.sin(2.1 * t + 2 * s['ph']))
                if t - s['boost'] < 1.6: sp *= 1.55
                if t - s['bonk'] < 0.7: sp *= 0.35
                s['v'] += (sp - s['v']) * 0.08; s['x'] += s['v'] / FPS
                for it in items:
                    if it['lane'] == li and it['got'] is None and abs(it['x'] - s['x']) < 40:
                        it['got'] = t
                        if it['kind'] == 'gum': s['boost'] = t; ev.append((t, 'boost', g))
                        else: s['bonk'] = t; ev.append((t, 'bonk', g))
                if s['x'] >= COURSE: s['fin'] = t; ev.append((t, 'fin', g))
        frames.append({g: (st[g]['x'], st[g]['boost'], st[g]['bonk'], st[g]['fin']) for g in G})
        f += 1
        if all(st[g]['fin'] for g in G) or t > 40: break
    return frames, ev, items, st
def leadchanges(frames):
    lead = None; n = 0
    for fr in frames[int(T0 * FPS) + 30:]:
        l = max(G, key=lambda g: fr[g][0])
        if l != lead: n += 1; lead = l
    return n - 1
def score(seed):
    fr, ev, it, st = sim(seed)
    fins = sorted((s['fin'], g) for g, s in st.items())
    m = fins[1][0] - fins[0][0]
    lc = leadchanges(fr)
    if not (0.04 < m < 0.35) or lc < 6: return None
    if not (19 < fins[0][0] < 24): return None
    return fins[0][1], round(m, 2), lc, round(fins[0][0], 1)
if sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, ITEMS, ST = sim(SEED)
fins = sorted((s['fin'], g) for g, s in ST.items()); WIN = fins[0][1]; TW = fins[0][0]
print('winner', WIN, round(TW, 2), [(g, round(t, 2)) for t, g in fins])
END = TW + 3.6; NF = int(END * FPS)
VICF = vic(WIN, 300)
# water (low-res procedural, upscaled 4x for pixel look)
WR = (270, 340)
def water(camx, t):
    w, h = WR
    xs = (np.arange(w) * 4 + camx)[None, :]; ys = (np.arange(h) * 4)[:, None]
    yy = np.arange(h)[:, None]
    band = np.sin(yy / 2.3 + 0.8 * np.sin(xs / 140.0 + t * 0.9))
    dash = np.sin(xs / 29.0 - t * 2.2 + yy * 1.7) + 0.5 * np.sin(xs / 71.0 + t * 0.7 + yy * 0.6)
    hi = (band > 0.82) & (dash > 0.9); mid = (band > 0.6) & (dash > 0.2) & ~hi
    base = np.array([30, 120, 168], float)[None, None, :] + (ys / (h * 4))[..., None] * np.array([-18, -52, -50])[None, None, :]
    img = base + hi[..., None] * np.array([120, 120, 85]) + mid[..., None] * np.array([18, 26, 22])
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img, 'RGB').resize((w * 4, h * 4), Image.NEAREST).convert('RGBA')
wr = Writer('r82_noaudio.mp4'); events = []; camx = 0.0; seen = set()
ICON = {g: up(Image.open(SIDE[g]).convert('RGBA').crop((24, 10, 72, 46)), 2) for g in G}
for f in range(NF):
    t = f / FPS; fr = FR[min(f, len(FR) - 1)]
    lead = max(fr[g][0] for g in G)
    target = min(max(0, lead - 640), COURSE - 640)
    camx += (target - camx) * 0.12
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    # sky band with slow parallax
    sx = int(SKYX + camx * 0.03) % max(1, SKY.width - W)
    img.alpha_composite(SKY.crop((sx, 160, sx + W, 160 + 640)), (0, 0))
    img.alpha_composite(water(camx, t), (0, 600))
    # horizon blend
    layer(img, lambda d: [d.rectangle([0, 600 + k * 4, W, 604 + k * 4], fill=(255, 200, 140, max(0, 120 - k * 12))) for k in range(10)])
    d = ImageDraw.Draw(img)
    # finish line + lighthouse
    fx = COURSE - camx
    if -200 < fx < W + 200:
        for yy in range(700, 1840, 30):
            for k in range(2):
                d.rectangle([fx - 15 + k * 15, yy + (15 if k else 0), fx + k * 15, yy + 15 + (15 if k else 0)], fill=(245, 245, 245))
                d.rectangle([fx - 15 + k * 15, yy + (0 if k else 15), fx + k * 15, yy + (15 if k else 30)], fill=(30, 30, 40))
        img.alpha_composite(LH, (int(fx + 30), 760 - LH.height + 140))
    # lane ropes with buoys
    for li in range(6):
        ry = LY[0] - 120 + li * 205
        d.line([0, ry, W, ry], fill=(240, 240, 240), width=3)
        off = int(-camx) % 200
        for bx in range(off - 200, W + 200, 200):
            b = BUOY[(f // 4 + (bx - off) // 200) % len(BUOY)]; img.alpha_composite(b, (bx - b.width // 2, ry - b.height // 2 + int(3 * math.sin(t * 3 + bx))))
    # items
    for it in ITEMS:
        ix = it['x'] - camx
        if -80 < ix < W + 80:
            y = LY[it['lane']] + int(6 * math.sin(t * 3 + it['x']))
            if it['kind'] == 'gum':
                if it['got'] is None or t < it['got']:
                    g = gummy(GUM[G[it['lane']]] if random.Random(int(it['x'])).random() < 0.7 else 'gold', 3)
                    layer(img, lambda dd: dd.ellipse([ix - 40, y - 60, ix + 40, y + 10], fill=(255, 230, 140, 70)))
                    img.alpha_composite(g, (int(ix - g.width / 2), int(y - g.height - 6)))
                    d = ImageDraw.Draw(img); d.ellipse([ix - 26, y - 6, ix + 26, y + 8], outline=(255, 255, 255), width=3)
            else:
                if it['got'] is None or t - it['got'] < 0.6:
                    s = SLIME[(f // 3) % len(SLIME)]
                    yy = y - (0 if it['got'] is None else int(60 * math.sin((t - it['got']) / 0.6 * math.pi)))
                    img.alpha_composite(s, (int(ix - s.width / 2), int(yy - s.height + 30)))
                    d = ImageDraw.Draw(img); d.ellipse([ix - 40, y + 6, ix + 40, y + 22], outline=(230, 250, 255), width=3)
    # surfers
    for li, g in enumerate(G):
        x, bt, kt, fin = fr[g]; sx_ = x - camx + 90; y = LY[li]
        bob = 6 * math.sin(t * 4 + li)
        if t - kt < 0.7: bob += -20 * math.sin((t - kt) / 0.7 * math.pi)
        # wake
        sp = 1.0 if t > T0 else 0
        if sp:
            layer(img, lambda dd: [dd.rectangle([sx_ - 90 - k * 34, y + 6 + (k % 2) * 6, sx_ - 70 - k * 30, y + 14 + (k % 2) * 6], fill=(255, 255, 255, 200 - k * 30)) for k in range(6)])
            if t - bt < 1.6:
                layer(img, lambda dd: [dd.rectangle([sx_ - 120 - k * 46 - (f * 7 + k * 13) % 30, y - 100 + k * 22, sx_ - 70 - k * 46 - (f * 7 + k * 13) % 30, y - 94 + k * 22], fill=COL[g] + (230 - k * 40,)) for k in range(5)])
                layer(img, lambda dd: [dd.rectangle([sx_ - 80 - k * 18, y - 4 - k * 9 + (f % 3) * 2, sx_ - 68 - k * 18, y + 6 - k * 9 + (f % 3) * 2], fill=(255, 255, 255, 220 - k * 35)) for k in range(6)])
        b = BOARD; img.alpha_composite(b, (int(sx_ - b.width / 2), int(y - b.height / 2 + bob)))
        s = SPR[g]; img.alpha_composite(s, (int(sx_ - s.width / 2 + 6), int(y - 156 + bob)))
        if fin is not None and t >= fin and g == WIN:
            pass
        # popups
        if 0 <= t - bt < 1.0:
            u = t - bt; text_layer(img, [(sx_, y - 190 - u * 40, 'WAVE BOOST!', 26, (255, 220, 70), 5, int(255 * min(1, (1 - u) / 0.3)))])
        if 0 <= t - kt < 0.9:
            u = t - kt; text_layer(img, [(sx_, y - 190 - u * 40, 'BOING!', 28, (150, 255, 140), 5, int(255 * min(1, (0.9 - u) / 0.3)))])
    for (te, kind, g) in EV:
        if abs(t - te) < 0.5 / FPS:
            events.append((round(te, 3), {'boost': 'powerup_8bit', 'bonk': 'boing', 'fin': 'ding_8bit'}[kind]))
    # header + progress track
    layer(img, lambda dd: dd.rectangle([0, 0, W, 330], fill=(20, 12, 30, 120)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 50, 'CHOOSE YOUR', F(64)); ctext(d, W / 2, 135, 'CHAMPION!', F(64), (255, 214, 60))
    layer(img, lambda dd: dd.rounded_rectangle([40, 232, W - 40, 322], 16, fill=(10, 30, 50, 180)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([40, 232, W - 40, 322], 16, outline=(255, 214, 60), width=4)
    for g in G:
        p = min(1, fr[g][0] / COURSE); px = 110 + p * (W - 230)
        ic = ICON[g]; img.alpha_composite(ic, (int(px - ic.width / 2), 240))
    d = ImageDraw.Draw(img); [d.rectangle([W - 118, 240 + k * 10, W - 108, 250 + k * 10], fill=(245, 245, 245) if k % 2 else (30, 30, 40)) for k in range(8)]
    # lane names at start
    if t < T0 + 1.0:
        a = int(255 * min(1, max(0, (T0 + 1.0 - t) / 0.4)))
        text_layer(img, [(400, LY[li] - 70, NAME[g], 30, COL[g], 6, a) for li, g in enumerate(G)])
        n = 3 - int(t)
        if t < T0:
            text_layer(img, [(W / 2 + 160, 1180, str(max(1, n)), 150, (255, 255, 255), 10, 255)])
            if abs(t - int(t)) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
        else:
            text_layer(img, [(W / 2 + 160, 1180, 'GO!', 130, (255, 214, 60), 10, a)])
            if abs(t - T0) < 0.5 / FPS: events.append((round(t, 3), 'go_8bit'))
    if t >= TW:
        u = t - TW
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(10, 8, 20, int(150 * min(1, u / 0.4)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(W / 2, 1220, NAME[WIN] + ' WINS!', 60, COL[WIN], 8, 255), (W / 2, 1330, 'DID YOUR CHAMPION WIN?', 34, (255, 255, 255), 6, int(255 * min(1, max(0, u - 0.6) / 0.4)))])
        if not any(e[1] == 'victory' for e in events): events.append((round(TW, 3), 'victory')); events.append((round(TW + 0.1, 3), 'cheer'))
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'p82_{f:04d}.png')
wr.close()
json.dump(events, open('r82_ev.json', 'w'))
print('done', END)
