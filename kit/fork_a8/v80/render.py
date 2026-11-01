import sys; sys.path.insert(0, '../../fork_a7'); from common7 import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 11.0; N = int(DUR * FPS); T_GO, T_UP = 1.4, 8.4
BG = bg_frames('bg_moon.gif', (1600, 900), step=1, bright=0.55, blur=2)
BG = [b.crop((546, 0, 546 + 507, 900)).resize((W, H), Image.NEAREST) for b in BG]
TR = up(crop(Image.open('../gen/tray/00.png').convert('RGBA')), 7); TX, TY = W // 2 - TR.width // 2, 620
# interior box (velvet) in screen coords
import numpy as np
_a = np.array(TR).astype(int); _m = (_a[..., 0] < 140) & (_a[..., 2] > 50) & (_a[..., 1] < 70) & (_a[..., 3] > 0)
_ys, _xs = np.nonzero(_m); IX0, IY0, IX1, IY1 = TX + np.percentile(_xs, 3) + 18, TY + np.percentile(_ys, 3) + 22, TX + np.percentile(_xs, 97) - 18, TY + np.percentile(_ys, 97) - 10
print('velvet', IX0, IY0, IX1, IY1)
rng = random.Random(11)
kinds = ['mush', 'acv', 'mel', 'cre']
cols, rows = 4, 4; items = []
for r in range(rows):
    for c in range(cols):
        x = IX0 + (c + 0.5) * (IX1 - IX0) / cols + rng.uniform(-12, 12); y = IY0 + (r + 0.5) * (IY1 - IY0) / rows + rng.uniform(-8, 8)
        items.append([rng.choice(kinds), x, y, 3])
# stacked doubles: a second gummy peeking out behind three of them
hidden = []
for idx, (dx, dy) in zip([2, 9, 13], [(14, -13), (-15, -12), (13, -14)]):
    k, x, y, s = items[idx]; hidden.append([rng.choice(kinds), x + dx, y + dy, 3])
tiny = ['gold', TX + TR.width - 70, TY + TR.height - 46, 1]
COUNT = len(items) + len(hidden) + 1
print('answer', COUNT)
HOL = seq('../../fork_b5/hollow_nod', 4, 1, None)
w = Writer('noaudio.mp4'); ev = [(0.2, 'chime'), (T_GO, 'go_8bit'), (T_UP, 'buzz_8bit')]
for s_ in range(int(T_UP - T_GO)): ev.append((round(T_GO + s_ + 1, 3), 'tick_8bit'))
rr = random.Random(2); STARS = [(rr.uniform(0, W), rr.uniform(0, 600), rr.uniform(0, 6.3)) for _ in range(30)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 4, y + 4], fill=(230, 240, 255, int(120 + 110 * math.sin(t * 2 + p)))) for x, y, p in STARS])
    layer(img, lambda d: [d.ellipse([W / 2 - r, TY + TR.height / 2 - r * 0.7, W / 2 + r, TY + TR.height / 2 + r * 0.7], fill=(160, 120, 255, 16)) for r in (560, 480, 400)])
    layer(img, lambda d: d.ellipse([TX + 30, TY + TR.height - 30, TX + TR.width - 30, TY + TR.height + 40], fill=(0, 0, 0, 110)))
    img.alpha_composite(TR, (TX, TY))
    for k, x, y, s in hidden + items + [tiny]:
        g = gummy(k, s); img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    # sparkle glints
    for i, (k, x, y, s) in enumerate(items):
        ph = (t * 1.3 + i * 0.37) % 3.0
        if ph < 0.25:
            a = int(255 * (1 - ph / 0.25)); layer(img, lambda d: (d.rectangle([x + 10, y - 26, x + 14, y - 14], fill=(255, 255, 255, a)), d.rectangle([x + 6, y - 22, x + 18, y - 18], fill=(255, 255, 255, a))))
    hf = HOL[int(t * 8) % len(HOL)]; img.alpha_composite(hf, (40, 1820 - hf.height))
    bub = [(320, 1438, 'Count carefully...', 30, (255, 255, 255), 5, 255)] if t < T_UP else []
    layer(img, lambda d: d.rounded_rectangle([30, 1410, 610, 1490], 20, fill=(20, 16, 34, 200), outline=(255, 214, 60, 255), width=4)) if t < T_UP else None
    its = [(W / 2, 140, 'HOW MANY GUMMIES', 60, (255, 255, 255), 8, 255), (W / 2, 230, 'DO YOU SEE?', 72, (255, 214, 60), 8, 255),
           (W / 2, 340, 'Only geniuses get it right', 30, (200, 210, 255), 5, 255)] + bub
    # timer bar
    if T_GO <= t < T_UP:
        u = (t - T_GO) / (T_UP - T_GO)
        layer(img, lambda d: (d.rounded_rectangle([140, 470, 940, 510], 18, fill=(20, 16, 34, 220), outline=(255, 214, 60, 255), width=4),
                              d.rounded_rectangle([148, 478, 148 + int(784 * (1 - u)), 502], 12, fill=(120, 220, 120, 255) if u < 0.6 else (255, 180, 60, 255) if u < 0.85 else (255, 80, 80, 255))))
        its.append((W / 2, 535, f'{int(math.ceil(T_UP - t))}s', 30, (255, 255, 255), 4, 255))
    if t >= T_UP:
        a = int(255 * min(1, (t - T_UP) / 0.3))
        layer(img, lambda d: d.rounded_rectangle([170, 1440, 910, 1640], 24, fill=(20, 16, 34, int(220 * a / 255)), outline=(255, 214, 60, a), width=5))
        its += [(W / 2, 1470, "TIME'S UP!", 56, (255, 214, 60), 7, a), (W / 2, 1565, 'Comment your number', 34, (255, 255, 255), 5, a)]
    text_layer(img, its)
    w.write(img)
w.close(); json.dump({'events': ev}, open('events.json', 'w')); print('done')
