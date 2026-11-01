import sys; SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork_a7'); from common7 import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
STILL = os.environ.get('STILL')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# #78 safe-zone + hook pass (source: fork_a8/v80/render.py)
# rc8: timer runs from frame 0 (was a still 1.4s), 7s to count, TIME'S UP held 1.3s then loops to the full tray
T_GO, T_UP = 0.0, 7.0; DUR = T_UP + 1.3; N = int(round(DUR * FPS))
# rc8: comment prompt as a real 46px band line from frame 0; ONLY GENIUSES GET IT RIGHT (36px sub) cut: 26 chars cannot reach 44px on one line anywhere in the safe width
HOOK, HB = hook_layer2(['HOW MANY GUMMIES', 'DO YOU SEE?'], accent=1, sub='Comment your number')
print('hook bottom', HB)
BG = bg_frames('bg_moon.gif', (1600, 900), step=1, bright=0.55, blur=2)
BG = [b.crop((546, 0, 546 + 507, 900)).resize((W, H), Image.NEAREST) for b in BG]
TR = up(crop(Image.open(SP + 'fork_a8/gen/tray/00.png').convert('RGBA')), 7)
CX = 478  # safe-zone centre (x70-887 below y1110)
BAR_Y = HB + 14
TX, TY = CX - TR.width // 2, BAR_Y + 50
print('tray', TX, TY, TX + TR.width, TY + TR.height)
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
hidden = []
for idx, (dx, dy) in zip([2, 9, 13], [(14, -13), (-15, -12), (13, -14)]):
    k, x, y, s = items[idx]; hidden.append([rng.choice(kinds), x + dx, y + dy, 3])
# GOLD FIX: the tiny rim gummy was gold, now an ACV product gummy (same 1x size, same spot)
tiny = ['cre', TX + TR.width - 70, TY + TR.height - 46, 1]
COUNT = len(items) + len(hidden) + 1
print('answer', COUNT)
HOL = seq(SP + 'fork_b5/hollow_nod', 4, 1, None)      # 4x, unchanged
RAY = idle('ray', 4)                                   # Rayleigh takes the 'Count carefully...' line (Hollow never talks)
FEET = 1495
HX = 90 - 116                                           # hollow canvas x (content starts ~x90)
RX = 868 - 70 * 4                                       # ray canvas x so content ends ~x868
GACV = up(acv_gummy_strong(), 3)   # rc8: gummy shine on Syeda's ACV gummies (VETTING)
w = Writer('v78_noaudio.mp4')
ev = [(0.0, 'chime'), (T_UP, 'buzz_8bit')] + [(round(T_UP - k, 3), 'tick_8bit') for k in (3, 2, 1)]   # rc8: ticks on the last 3 seconds only (was every second)
rr = random.Random(2); STARS = [(rr.uniform(0, W), rr.uniform(0, 600), rr.uniform(0, 6.3)) for _ in range(30)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 4, y + 4], fill=(230, 240, 255, int(120 + 110 * math.sin(t * 2 + p)))) for x, y, p in STARS])
    layer(img, lambda d: [d.ellipse([CX - r, TY + TR.height / 2 - r * 0.7, CX + r, TY + TR.height / 2 + r * 0.7], fill=(160, 120, 255, 16)) for r in (560, 480, 400)])
    layer(img, lambda d: d.ellipse([TX + 30, TY + TR.height - 30, TX + TR.width - 30, TY + TR.height + 40], fill=(0, 0, 0, 110)))
    img.alpha_composite(TR, (TX, TY))
    for k, x, y, s in hidden + items + [tiny]:
        g = GACV if (k == 'acv' and s == 3) else gummy(k, s); img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    for i, (k, x, y, s) in enumerate(items):
        ph = (t * 1.3 + i * 0.37) % 3.0
        if ph < 0.25:
            a = int(255 * (1 - ph / 0.25)); layer(img, lambda d: (d.rectangle([x + 10, y - 26, x + 14, y - 14], fill=(255, 255, 255, a)), d.rectangle([x + 6, y - 22, x + 18, y - 18], fill=(255, 255, 255, a))))
    hf = HOL[int(t * 8) % len(HOL)]; img.alpha_composite(hf, (HX, FEET - 78 * 4))
    rf = RAY[int(t * 6) % len(RAY)]; img.alpha_composite(rf, (RX, FEET - 78 * 4))
    its = []
    if t < T_UP:  # Rayleigh's speech box, tail pointing right at her
        bx0, by0, bx1, by1 = 250, 1262, 684, 1372
        layer(img, lambda d: (d.rounded_rectangle([bx0, by0, bx1, by1], 20, fill=(20, 16, 34, 215), outline=(255, 214, 60, 255), width=4),
                              d.polygon([(bx1 - 4, by0 + 34), (bx1 + 46, by0 + 54), (bx1 - 4, by0 + 74)], fill=(255, 214, 60, 255)),
                              d.polygon([(bx1 - 8, by0 + 40), (bx1 + 32, by0 + 54), (bx1 - 8, by0 + 68)], fill=(20, 16, 34, 255))))
        its += [((bx0 + bx1) / 2, by0 + 10, 'COUNT', 44, (255, 255, 255), 6, 255),
                ((bx0 + bx1) / 2, by0 + 60, 'CAREFULLY', 44, (255, 255, 255), 6, 255)]   # rc8: 32 -> 44px
    if T_GO <= t < T_UP:
        u = (t - T_GO) / (T_UP - T_GO)
        layer(img, lambda d: (d.rounded_rectangle([96, BAR_Y, 760, BAR_Y + 36], 16, fill=(20, 16, 34, 225), outline=(255, 214, 60, 255), width=4),
                              d.rounded_rectangle([104, BAR_Y + 7, 104 + int(648 * (1 - u)), BAR_Y + 29], 10, fill=(120, 220, 120, 255) if u < 0.6 else (255, 180, 60, 255) if u < 0.85 else (255, 80, 80, 255))))
        sec = int(math.ceil(T_UP - t)); ph = sec - (T_UP - t); sz = 48 if ph > 0.15 else 56   # rc8: 34 -> 48px, pops on each tick
        its.append((832, BAR_Y + 18 - sz / 2, f'{sec}s', sz, (255, 255, 255) if sec > 3 else (255, 110, 90), 7, 255))
    if t >= T_UP:
        a = int(255 * min(1, (t - T_UP) / 0.1)); cy = TY + TR.height // 2   # rc8: hard pop (was a 0.3s see-through fade)
        # rc8: card centred in the wide upper zone (x547) so the comment line can be 44px (was 34px)
        layer(img, lambda d: d.rounded_rectangle([547 - 462, cy - 110, 547 + 462, cy + 100], 24, fill=(20, 16, 34, int(235 * a / 255)), outline=(255, 214, 60, a), width=6))
        its += [(547, cy - 82, "TIME'S UP!", 72, (255, 214, 60), 9, a), (547, cy + 22, 'COMMENT YOUR NUMBER', 44, (255, 255, 255), 6, a)]
    text_layer(img, its)
    img.alpha_composite(HOOK)
    w.write(img)
    if STILL and f in [int(x) for x in STILL.split(',')]: img.convert('RGB').save(f'k78_{f}.png')
w.close(); json.dump({'events': ev}, open('v78_ev.json', 'w')); print('done', DUR, ev)
