import sys; sys.path.insert(0, '../fork1'); sys.path.insert(0, '../pixellab/safezone')
from common import *
from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.0; NF = int(DUR * FPS)
HOOK, HB = hook_layer(['+1 XP A DAY'], accent=0)
print('hook bottom', HB)
TOPB = bg_frames('found_hd.gif', (1707, 960), step=2, bright=0.8); TOPB = [b.crop((420, 0, 1500, 960)) for b in TOPB]
BOTB = bg_frames('sun_hd.gif', (1707, 960), step=2); BOTB = [b.crop((313, 0, 1393, 960)) for b in BOTB]
EAT = seq('../fork3/hollow_eat', 3, 0, 13); FOOT3 = 78 * 3
VICT = vic('hollow', 384)
GUMS = [gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']]
SMALLG = gummy('mush', 2)
DIV0, DIV1 = 944, 1012           # divider band
BOFF = 1430 - 725                # bottom bg offset so the Hollow's ground sits at y1430
w = Writer('v27_noaudio.mp4'); ev = []
EATP = 2.0
for f in range(NF):
    t = f / FPS; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    tb = TOPB[int(t * 6) % len(TOPB)]; bb = BOTB[int(t * 6) % len(BOTB)]
    img.alpha_composite(tb, (0, -20))
    img.alpha_composite(bb.crop((0, DIV1 - BOFF, W, 960)), (0, DIV1))
    tail = bb.crop((0, 960 - (H - (BOFF + 960)), W, 960)).transpose(Image.FLIP_TOP_BOTTOM)
    img.alpha_composite(ImageEnhance.Brightness(tail).enhance(0.55), (0, BOFF + 960))
    # ---- top: day 1
    u = (t % EATP) / EATP; k = min(12, int(u * 1.6 * 13))
    hx, hy = 540, 840
    if u < 0.12:
        g = SMALLG; gy = hy - 330 + u / 0.12 * 140
        img.alpha_composite(g, (hx - g.width // 2, int(gy)))
    e = EAT[k if u < 0.62 else 0]
    layer(img, lambda d: d.ellipse([hx - 70, hy - 14, hx + 70, hy + 14], fill=(0, 0, 0, 90)))
    img.alpha_composite(e, (hx - e.width // 2, hy - FOOT3))
    pop = (t % EATP) - 0.55 * EATP
    items = [(190, HB + 22, 'DAY 1', 40, (140, 220, 255), 5, 255)]
    if 0 <= pop < 0.8:
        a = int(255 * min(1, (0.8 - pop) / 0.3)); items.append((hx + 170, int(hy - 280 - pop * 60), '+1 XP', 40, (120, 230, 255), 6, a))
        if pop < 1 / FPS: ev.append((round(t, 3), 'coin_8bit'))
    text_layer(img, items)
    def bar1(d):
        d.rounded_rectangle([300, 880, 940, 916], 12, fill=(15, 15, 30, 220), outline=(120, 200, 255, 255), width=3)
        d.rectangle([306, 886, 306 + 6 + 3 * (int(t / EATP) % 3), 910], fill=(120, 220, 255, 255))
    layer(img, bar1)
    text_layer(img, [(190, 878, 'LV 1', 34, (200, 230, 255), 5, 255)])
    # ---- divider
    layer(img, lambda d: (d.rectangle([0, DIV0, W, DIV0 + 12], fill=(255, 214, 60, 255)), d.rectangle([0, DIV0 + 12, W, DIV1], fill=(20, 12, 4, 200))))
    text_layer(img, [(W / 2, DIV0 + 22, '1 YEAR LATER', 44, (255, 214, 60), 6, 255)])
    # ---- bottom: level 99
    cx, cy = 540, 1250
    def aura(d):
        for r, a in ((230, 55), (180, 75), (130, 95)):
            rr = r + 12 * math.sin(t * 4 + r)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 245, 190, a))
        for i in range(14):
            ang = t * 1.5 + i * 0.449; rr = 270 + 20 * math.sin(t * 3 + i)
            sx, sy = cx + rr * math.cos(ang), cy + rr * 0.45 * math.sin(ang)
            d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 250, 200, 220))
    A_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); aura(ImageDraw.Draw(A_))
    A_ = A_.crop((0, DIV1, W, 1500)); img.alpha_composite(A_, (0, DIV1))
    orb = []
    for i, g in enumerate(GUMS):
        ang = t * 1.2 + i * 2 * math.pi / 5; orb.append((math.sin(ang), cx + 290 * math.cos(ang), cy - 20 + 100 * math.sin(ang), g))
    for z, x, y, g in sorted(orb, key=lambda o: o[0]):
        if z < 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    v = VICT[int(t * 8) % len(VICT)]
    img.alpha_composite(v, (cx - v.width // 2, 1430 - v.height))
    for z, x, y, g in sorted(orb, key=lambda o: o[0]):
        if z >= 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    def bar2(d):
        d.rounded_rectangle([300, 1448, 880, 1492], 14, fill=(30, 20, 5, 220), outline=(255, 214, 60, 255), width=4)
        sh = int((t * 300) % (880 - 300 - 80))
        d.rectangle([308, 1456, 872, 1484], fill=(255, 196, 40, 255)); d.rectangle([308 + sh, 1456, 308 + sh + 60, 1484], fill=(255, 245, 190, 255))
    layer(img, bar2)
    text_layer(img, [(185, 1446, 'LV 99', 40, (255, 214, 60), 6, 255), (230, DIV1 + 18, 'DAY 365', 40, (255, 230, 150), 5, 255)])
    img.alpha_composite(HOOK)
    w.write(img)
w.close(); json.dump(ev, open('v27_ev.json', 'w')); print('done')
