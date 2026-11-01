import sys; sys.path.insert(0, '..')
from common import *
import numpy as np, colorsys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PW, PH = 1000, 562; PX = 40; PY1, PY2 = 392, 982
hub = Image.open(A + 'hub.gif'); NHF = hub.n_frames
k = PW / 1920.0
JOY = idle('joy', 1); CYR = idle('cyrus', 1); RAY = idle('ray', 1)
GM = gummy('mush', 2); GA = gummy('acv', 2)
POT = up(crop(Image.open(PL + 'steal/flowers/01.png').convert('RGBA')), 2)
CRATE = up(crop(Image.open(PL + 'steal/crate/01.png').convert('RGBA')), 2)
def recolor(img, box):
    a = np.array(img).astype(np.float32); x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1, :3] / 255.0
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = sub.max(-1); mn = sub.min(-1)
    yellowish = (r > 0.45) & (g > 0.35) & (b < 0.55) & (mx - mn > 0.18) & (r >= g * 0.9)
    out = sub.copy()
    # rotate yellow -> sky blue: swap channels roughly
    out[..., 0] = np.where(yellowish, b * 0.9 + 0.05, r)
    out[..., 1] = np.where(yellowish, g * 0.85 + 0.1, g)
    out[..., 2] = np.where(yellowish, r * 0.95, b)
    a[y0:y1, x0:x1, :3] = out * 255
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
PANEL = {}
def panel(i, which):
    key = (i, which)
    if key in PANEL: return PANEL[key]
    hub.seek(i); f = hub.convert('RGBA').resize((PW, PH), Image.NEAREST)
    if which == 1: f = recolor(f, (int(770 * 2 * k), int(150 * 2 * k), PW, int(250 * 2 * k)))
    PANEL[key] = f; return f
def decorate(p, which, t):
    p = p.copy()
    # props shared
    p.alpha_composite(CRATE, (int(880 * 2 * k) - CRATE.width // 2, int(470 * 2 * k) - CRATE.height))
    if which == 0: p.alpha_composite(POT, (int(118 * 2 * k) - POT.width // 2, int(468 * 2 * k) - POT.height))   # difference 3
    g = GM if which == 0 else GA                                                                             # difference 1
    p.alpha_composite(g, (int(395 * 2 * k) - g.width // 2, int(372 * 2 * k) - g.height))
    fi = int(t * 10) % 6
    for spr, x, y in ((JOY[fi], 300, 500), (CYR[fi], 640, 498), (RAY[(fi + 2) % 6], 735, 330)):
        p.alpha_composite(spr, (int(x * 2 * k) - 46, int(y * 2 * k) - 78))
    return p
BG = [f for f in bg_frames('hub.gif', (3413, 1920), step=4, bright=0.45, blur=14)]
BGC = [b.crop(((3413 - W) // 2, 0, (3413 - W) // 2 + W, H)) for b in BG]
SPEC = {g: idle(g, 2) for g in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']}
T_GO = 3.0; T_END = T_GO + 10.0; DUR = T_END + 2.6
out = Writer('d6_noaudio.mp4'); ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGC[int(t * 2.5) % len(BGC)].copy()
    hi = int(t * 10) % NHF
    for which, py in ((0, PY1), (1, PY2)):
        p = decorate(panel(hi, which), which, t)
        layer(img, lambda d, py=py: d.rounded_rectangle([PX - 10, py - 10, PX + PW + 10, py + PH + 10], 14, fill=(20, 14, 30, 255), outline=(255, 214, 60, 255), width=5))
        img.alpha_composite(p, (PX, py))
    # header
    layer(img, lambda d: d.rectangle([0, 96, W, 350], fill=(14, 10, 24, 150)))
    text_layer(img, [(W / 2, 128, 'FIND 3 DIFFERENCES', 50, (255, 255, 255), 6, 255), (W / 2, 203, 'IN 10 SECONDS', 50, (255, 214, 60), 6, 255),
                     (W / 2, 280, "or you're an NPC", 30, (200, 230, 255), 5, 255)])
    # timer bar
    rem = max(0.0, T_END - max(t, T_GO)); frac = rem / 10.0
    col = (90, 200, 80) if rem > 5 else ((255, 190, 50) if rem > 2 else (230, 60, 60))
    layer(img, lambda d: (d.rounded_rectangle([60, 1596, W - 60, 1656], 14, fill=(20, 14, 30, 230), outline=(255, 255, 255, 255), width=4),
                          d.rounded_rectangle([68, 1604, 68 + (W - 136) * frac, 1648], 10, fill=col + (255,)) if frac > 0.01 else None))
    lab = "TIME'S UP" if t >= T_END else str(int(math.ceil(rem)) if t >= T_GO else 10)
    text_layer(img, [(W / 2, 1611, lab, 30, (255, 255, 255), 5, 255)])
    # spectators
    for i, g in enumerate(['joy', 'cyrus', 'cleo', 'ray', 'hollow']):
        fr = SPEC[g][(int(t * 10) + i * 2) % 6]; x = 120 + i * 210
        bob = 0
        img.alpha_composite(fr, (x - fr.width // 2, 1905 - 78 * 2 + bob))
    # countdown
    if t < T_GO:
        layer(img, lambda d: [d.rectangle([PX, py, PX + PW, py + PH], fill=(8, 6, 14, 170)) for py in (PY1, PY2)])
        n = 3 - int(t); u = t - int(t); s = int(150 * (1.25 - 0.25 * min(1, u * 4)))
        text_layer(img, [(W / 2, (PY1 + PY2 + PH) / 2 - s / 2, str(n), s, (255, 214, 60), 10, 255)])
        if u < 1 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    elif t < T_GO + 0.8:
        u = t - T_GO; a = int(255 * min(1, (0.8 - u) / 0.3))
        text_layer(img, [(W / 2, (PY1 + PY2 + PH) / 2 - 60, 'GO!', 120, (120, 240, 90), 10, a)])
        if u < 1 / FPS: ev.append((round(t, 3), 'go_8bit'))
    if T_END - 3 <= t < T_END and (t - (T_END - 3)) % 1 < 1 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    if t >= T_END:
        u = t - T_END
        if u < 1 / FPS: ev.append((round(t, 3), 'buzz_8bit'))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, int(min(1, u / 0.25) * 120))))
        sc = 1 + 0.15 * max(0, 1 - u * 5)
        layer(img, lambda d: d.rounded_rectangle([120, 780, W - 120, 1080], 24, fill=(20, 14, 30, 235), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(W / 2, 820, "TIME'S UP!", int(64 * sc), (255, 214, 60), 8, 255), (W / 2, 930, 'Did you find', 40, (255, 255, 255), 6, 255),
                         (W / 2, 990, 'all 3?', 40, (255, 255, 255), 6, 255)])
    out.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close()
json.dump(ev, open('ev.json', 'w')); print('done', DUR, len(ev))
