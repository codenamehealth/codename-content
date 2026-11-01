# Same dragon, hoard swapped for gummies (brand rule: never coins or gold).
# Strips the coin/gem palette out of the native 128px dragon and builds a mound of Code Name gumdrops under it.
from PIL import Image, ImageDraw
import numpy as np, random
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
a = np.array(Image.open(S + 'fork_b5/dragon128L.png').convert('RGBA')).astype(int)
H_, W_ = a.shape[:2]
COIN = {(73, 46, 25), (249, 216, 59), (156, 90, 33), (182, 133, 54), (255, 219, 128), (190, 103, 22), (240, 190, 57), (255, 250, 237), (187, 93, 21),
        (192, 104, 47), (126, 41, 10), (166, 73, 20), (247, 247, 134), (191, 213, 64), (129, 17, 55)}
def coinish(p):
    r, g, b = p
    if (r, g, b) in COIN: return True
    if (b > g + 60 and r > 140) or b > r + 30 or (g > r and g > b) or (r > 120 and b > 90 and g < 70 and b > g + 40): return True     # gems: blues, greens, magentas
    return False
rgb = a[..., :3]; al = a[..., 3] > 0
rem = np.zeros((H_, W_), bool)
for y in range(H_):
    for x in range(W_):
        if al[y, x] and coinish(tuple(rgb[y, x])): rem[y, x] = True
keep = al & ~rem
blk = al & (rgb == 6).all(-1) & (np.arange(H_)[:, None] >= 80)
body = keep & ~blk
for y in range(H_):                                                       # black outline pixels in the pile area survive only next to the dragon
    for x in range(W_):
        if blk[y, x]:
            nb = body[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
            if not nb.any(): keep[y, x] = False
out = a.copy(); out[~keep] = 0
drag = Image.fromarray(out.astype(np.uint8))
PAL = {'mush': ((120, 52, 22), (176, 92, 44), (72, 28, 12)), 'acv': ((226, 86, 62), (252, 146, 116), (160, 46, 36)),
       'mel': ((244, 142, 102), (255, 196, 156), (198, 96, 70)), 'cre': ((222, 44, 96), (252, 116, 156), (150, 22, 62))}
SHAPE = ["..#####..", ".#######.", "#########", "#########", "#########", "#########", ".#######."]
def gumdrop(kind):
    base, light, dark = PAL[kind]; w, h = len(SHAPE[0]), len(SHAPE)
    g = Image.new('RGBA', (w + 2, h + 2)); px = g.load()
    for yy, row in enumerate(SHAPE):
        for xx, ch in enumerate(row):
            if ch == '#': px[xx + 1, yy + 1] = base + (255,)
    m = np.array(g)[..., 3] > 0
    for yy in range(h + 2):
        for xx in range(w + 2):
            if not m[yy, xx] and any(0 <= yy + dy < h + 2 and 0 <= xx + dx < w + 2 and m[yy + dy, xx + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[xx, yy] = (40, 16, 24, 255)
    for (xx, yy) in [(3, 2), (4, 2), (2, 3), (3, 3)]: px[xx, yy] = light + (255,)
    for xx in range(2, w): px[xx, h] = dark + (255,)
    px[w - 1, h - 1] = dark + (255,)
    if kind in ('mel', 'cre'): px[6, 3] = (255, 240, 235, 255); px[5, 5] = (255, 240, 235, 255)
    return g
K = list(PAL)
rr = random.Random(11)
back = Image.new('RGBA', (W_, H_)); front = Image.new('RGBA', (W_, H_))
pts = []
for i in range(140):                                                      # mound: denser and higher toward the middle
    x = rr.uniform(6, 122); top = 126 - 36 * max(0.0, 1 - ((x - 66) / 62) ** 2)
    col = np.where(out[70:, int(x), 3] > 0)[0]
    if len(col): top = min(top, 70 + col.max() - 1)                       # tuck the mound up under the feet, belly and tail
    y = rr.uniform(top, 127); pts.append((y, x))
for y, x in sorted(pts):
    g = gumdrop(rr.choice(K)); back.alpha_composite(g, (int(x - g.width / 2), int(y - g.height)))
for i in range(9):
    x = 10 + i * 13 + rr.randint(-2, 2); g = gumdrop(rr.choice(K)); front.alpha_composite(g, (int(x - g.width / 2), 128 - g.height))
res = Image.new('RGBA', (W_, H_)); res.alpha_composite(back); res.alpha_composite(drag); res.alpha_composite(front)
res.save(S + 'wk_n03/dragon_gummies.png')
for nm, im in (('dragon_gummies4', res), ('dragon_strip4', drag)):
    bg = Image.new('RGBA', (W_, H_), (200, 180, 140, 255)); bg.alpha_composite(im); bg.resize((W_ * 4, H_ * 4), Image.NEAREST).save(S + f'wk_n03/qa/{nm}.png')
