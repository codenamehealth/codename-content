import sys; sys.path.insert(0, '../fork1')
from common import *
BG = bg_frames('hub.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=0.6, blur=5)
jars = Image.open(A + 'jars.png').convert('RGBA')
# jars.png is RGB on grey; key out the grey background
import numpy as np
a = np.array(jars); bgc = a[2, 2, :3]; m = (np.abs(a[..., :3].astype(int) - bgc.astype(int)).sum(-1) < 12); a[m, 3] = 0
POT = crop(Image.fromarray(a).crop((0, 0, 200, 200))); POT = up(POT, 2.0)
GUM = up(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA'), 7)
def sil(im):
    s = Image.new('RGBA', im.size, (18, 12, 30, 235)); s.putalpha(im.getchannel('A').point(lambda p: 235 if p > 0 else 0)); return s
SPOT, SGUM = sil(POT), sil(GUM)
P0 = (320, 960); G0 = (770, 960)
LEVELS = [('NOOB', (120, 230, 110), 1.0), ('PRO', (90, 160, 255), 1.6), ('HACKER', (255, 90, 90), 2.4), ('GOD', (255, 214, 60), 3.4)]
LD = 4.0; rnd = random.Random(3)
TSTAR = [round((i * LD + rnd.uniform(1.4, 3.0)) * FPS) / FPS for i in range(4)]
print('match frames', [int(t * FPS) for t in TSTAR])
def pose(t):
    i = min(3, int(t / LD)); w = LEVELS[i][2]; s = t - TSTAR[i]
    pdx = 105 * math.sin(2.3 * w * s); pdy = 110 * math.sin(3.7 * w * s); pa = 24 * math.sin(1.7 * w * s)
    gdx = 120 * math.sin(1.9 * w * s); gdy = 60 * (1 - math.cos(1.9 * w * s)); ga = 20 * math.sin(1.9 * w * s)
    return i, (pdx, pdy, pa), (gdx, gdy, ga)
JOY = idle('joy', 3)
TE = 4 * LD + 1.4; NF = int(TE * FPS); wr = Writer('v42_noaudio.mp4'); ev = []
def place(img, spr, c, d, ang):
    r = spr.rotate(ang, resample=Image.NEAREST, expand=True)
    img.alpha_composite(r, (int(c[0] + d[0] - r.width / 2), int(c[1] + d[1] - r.height / 2)))
for f in range(NF):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    tt = min(t, 4 * LD - 1 / FPS)
    i, p, g = pose(tt)
    # pedestals
    def ped(d):
        for cx, cy in (P0, G0):
            d.ellipse([cx - 170, cy + 150, cx + 170, cy + 210], fill=(0, 0, 0, 90))
    layer(img, ped)
    img.alpha_composite(SPOT, (P0[0] - SPOT.width // 2, P0[1] - SPOT.height // 2))
    img.alpha_composite(SGUM, (G0[0] - SGUM.width // 2, G0[1] - SGUM.height // 2))
    place(img, POT, P0, p[:2], p[2]); place(img, GUM, G0, g[:2], g[2])
    jo = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(jo, (W - 150 - jo.width // 2, 1880 - 78 * 3))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, 0, W, 290], fill=(16, 10, 30, 175)); img.alpha_composite(L)
    name, col, _ = LEVELS[i]
    items = [(W / 2, 80, 'PAUSE WHEN BOTH', 56, (255, 255, 255), 7, 255), (W / 2, 165, 'FIT PERFECTLY', 56, (255, 214, 60), 7, 255)]
    ls = i * LD; u = t - ls
    pop = 1.0 if u > 0.25 else 0.6 + 1.6 * u
    items.append((W / 2, 1290, name, int(84 * min(1.2, pop)), col, 9, 255))
    items.append((W / 2, 1410, f'LEVEL {i + 1} OF 4', 30, (255, 255, 255), 5, 255))
    if t >= 4 * LD:
        u2 = t - 4 * LD; a = int(255 * min(1, u2 / 0.3))
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L2).rounded_rectangle([100, 1480, 980, 1650], 26, fill=(16, 10, 30, int(220 * a / 255)), outline=(255, 214, 60, a), width=6); img.alpha_composite(L2)
        items += [(W / 2, 1510, 'Which level did', 38, (255, 255, 255), 5, a), (W / 2, 1575, 'you beat?', 38, (255, 214, 60), 5, a)]
    text_layer(img, items)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p42_{f:04d}.png')
wr.close()
for k in range(4): ev.append((k * LD, 'whoosh_8bit')); ev.append((k * LD + 0.05, 'ding_8bit'))
ev.append((4 * LD, 'chime'))
json.dump(ev, open('v42_ev.json', 'w')); print('done')
