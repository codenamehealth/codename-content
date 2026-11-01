import sys; sys.path.insert(0, '../fork1')
from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CAUL = up(crop(Image.open('cauldron/03.png').convert('RGBA')), 8)
CX, CY = 540, 1090
N = 12; RIN = 270
ACV = gummy('acv', 3); GOLD = gummy('gold', 3)
T_SHOW, T_FADE, T_MOVE, T_END = 0.4, 2.4, 3.0, 16.0
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
G = [dict(t0=rng.uniform(0, 6.28), a=rng.uniform(0.6, 1.4), p=rng.uniform(0, 6.28), b=rng.uniform(0.8, 1.9), q=rng.uniform(0, 6.28), rb=rng.uniform(100, 250), ra=rng.uniform(40, 70)) for _ in range(N)]
TARGET = 0
def omega(t):
    if t < T_MOVE: return 0.0
    u = t - T_MOVE; return min(3.4, 0.7 + 0.22 * u)
OM = [0.0]
for f in range(1, int(T_END * FPS) + 1): OM.append(OM[-1] + omega(f / FPS) / FPS)
def pos(i, f):
    t = f / FPS; g = G[i]; th = g['t0'] + OM[min(f, len(OM) - 1)]; r = g['rb']
    if t > T_MOVE:
        u = t - T_MOVE; amp = min(1, u / 1.5)
        th += amp * 0.7 * math.sin(g['b'] * u * (1 + u / 10) + g['q']); r += amp * g['ra'] * math.sin(g['a'] * u * (1 + u / 12) + g['p'])
    r = max(40, min(275, r))
    return CX + r * math.cos(th), CY - 30 + r * math.sin(th) * 0.86
def raw(i, f):
    return pos(i, f)
TS = T_END - 1.3
def settle_targets():
    f0 = int(TS * FPS); P = [raw(i, f0) for i in range(N)]
    pol = [(math.hypot(x - CX, (y - CY + 30) / 0.86), math.atan2((y - CY + 30) / 0.86, x - CX), i) for i, (x, y) in enumerate(P)]
    pol.sort(); inner = sorted(pol[:4], key=lambda p: p[1]); outer = sorted(pol[4:], key=lambda p: p[1])
    T = {}
    for ring, rr in ((inner, 115), (outer, 255)):
        n = len(ring); a0 = ring[0][1]
        for k, (_, a, i) in enumerate(ring):
            ang = a0 + 2 * math.pi * k / n; T[i] = (CX + rr * math.cos(ang), CY - 30 + rr * math.sin(ang) * 0.86)
    return T
def final_pos(i, f):
    t = f / FPS; x, y = raw(i, f)
    if t <= TS: return x, y
    k = min(1, (t - TS) / 1.3); k = k * k * (3 - 2 * k); tx, ty = TGT[i]
    x0, y0 = raw(i, min(f, int(T_END * FPS)))
    return x0 * (1 - k) + tx * k, y0 * (1 - k) + ty * k
# ensure gummies start well separated
def sep_ok():
    pts = [pos(i, 0) for i in range(N)]
    return min(math.hypot(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(pts) for b in pts[i + 1:]) > 105
tries = 0
while not sep_ok() and tries < 500:
    for g in G: g['t0'] = rng.uniform(0, 6.28); g['rb'] = rng.uniform(90, 255)
    tries += 1
print('sep tries', tries)
TGT = settle_targets()
NUM = list(range(1, N + 1)); rng.shuffle(NUM)
print('target number', NUM[TARGET])
BGF = bg_frames('found_hd.gif', (int(1920 * 1.8), int(1080 * 1.8)), step=2, bright=0.45)
JOY = idle('joy', 3)
TIERS = [(T_MOVE, '100% STILL WITH IT', (120, 230, 120)), (T_MOVE + 3.2, 'TOP 30% KEEP UP', (255, 214, 60)), (T_MOVE + 6.4, 'TOP 5% REMAINING', (255, 150, 60)), (T_MOVE + 9.4, 'TOP 1% ELITE', (255, 90, 90))]
END = T_END + 3.8; NF = int(END * FPS)
wr = Writer('r86_noaudio.mp4'); events = []
BUB = [(rng.uniform(-200, 200), rng.uniform(-110, 110), rng.uniform(0, 3), rng.uniform(8, 22)) for _ in range(26)]
for f in range(NF):
    t = f / FPS; ff = min(f, int(T_END * FPS))
    bg = BGF[int(t * 6) % len(BGF)]; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    img.alpha_composite(bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)), (0, 0))
    layer(img, lambda d: d.ellipse([CX - 560, CY - 420, CX + 560, CY + 520], fill=(120, 255, 120, 20)))
    img.alpha_composite(CAUL, (CX - CAUL.width // 2, CY - CAUL.height // 2))
    # bubbles
    layer(img, lambda d: [d.ellipse([CX + bx * 1.2 - s * ((t * 0.7 + ph) % 1), CY - 30 + by * 1.6 - s * ((t * 0.7 + ph) % 1), CX + bx * 1.2 + s * ((t * 0.7 + ph) % 1), CY - 30 + by * 1.6 + s * ((t * 0.7 + ph) % 1)], outline=(200, 255, 170, int(220 * (1 - (t * 0.7 + ph) % 1))), width=3) for bx, by, ph, s in BUB])
    # swirl lines when stirring
    if t > T_MOVE and t < T_END:
        th0 = OM[ff]
        layer(img, lambda d: [d.arc([CX - r_, CY - 30 - r_ * 0.86, CX + r_, CY - 30 + r_ * 0.86], math.degrees(th0 + k * 2.1) % 360, (math.degrees(th0 + k * 2.1) + 50) % 360, fill=(220, 255, 200, 90), width=4) for k, r_ in enumerate((110, 200, 280))])
    # gummies (y-sorted)
    pts = sorted([(final_pos(i, ff), i) for i in range(N)], key=lambda p: p[0][1])
    for (x, y), i in pts:
        if t < T_SHOW: continue
        g = ACV
        if i == TARGET and t < T_FADE + 0.4:
            k = 0 if t < T_FADE else (t - T_FADE) / 0.4
            g = Image.blend(GOLD.resize(ACV.size, Image.NEAREST), ACV, k) if k > 0 else GOLD
            if t < T_FADE:
                pulse = 0.5 + 0.5 * math.sin(t * 8)
                layer(img, lambda d: d.ellipse([x - 90, y - 90, x + 90, y + 90], fill=(255, 220, 80, int(70 + 70 * pulse))))
                layer(img, lambda d: d.ellipse([x - 72, y - 72, x + 72, y + 72], outline=(255, 214, 60, 255), width=9))
        img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    # numbers at the end
    if t >= T_END:
        u = t - T_END
        for (x, y), i in pts:
            layer(img, lambda d: d.ellipse([x - 32, y - 32 - 58, x + 32, y + 32 - 58], fill=(20, 14, 30, 235), outline=(255, 255, 255, 255), width=4))
            text_layer(img, [(x + 2, y - 72, str(NUM[i]), 30, (255, 255, 255), 0, 255)])
    # Joy stirring beside
    jf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(jf, (150 - jf.width // 2, 1880 - 78 * 3))
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 400], fill=(10, 18, 12, 170)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 60, 'LOCK YOUR EYES ON', F(54)); ctext(d, W / 2, 140, 'THE GOLDEN GUMMY', F(56), (255, 214, 60))
    cur = None
    for tt, txt, col in TIERS:
        if t >= tt: cur = (tt, txt, col)
    if t < T_END:
        if cur and t >= T_MOVE:
            text_layer(img, [(W / 2, 250, cur[1], 36, cur[2], 6, 255)])
            if abs(t - cur[0]) < 0.5 / FPS: events.append((round(t, 3), 'whoosh_8bit'))
        elif t < T_FADE + 0.5:
            text_layer(img, [(W / 2, 250, "DON'T LOSE IT...", 36, (255, 255, 255), 6, 255)])
        layer(img, lambda d: d.rounded_rectangle([W / 2 - 120, 1620, W / 2 + 120, 1690], 14, fill=(10, 18, 12, 200)))
        text_layer(img, [(W / 2, 1638, f'{max(0, t - T_MOVE):04.1f}s', 34, (255, 255, 255), 0, 255)])
        if t > T_MOVE and abs((t - T_MOVE) - round(t - T_MOVE)) < 0.5 / FPS: events.append((round(t, 3), 'reeltick_8bit'))
    else:
        u = t - T_END
        text_layer(img, [(W / 2, 1620, 'WHICH ONE WAS IT?', 50, (255, 214, 60), 8, 255), (W / 2, 1700, 'Comment the number', 34, (255, 255, 255), 6, int(255 * min(1, max(0, u - 0.4) / 0.4)))])
        if abs(u) < 0.5 / FPS: events.append((round(t, 3), 'ding_8bit'))
    if abs(t - T_SHOW) < 0.5 / FPS: events.append((round(t, 3), 'chime'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p86_{f:04d}.png')
wr.close(); json.dump(events, open('r86_ev.json', 'w')); print('done', END)
