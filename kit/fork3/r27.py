import sys; sys.path.insert(0, '../fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.0; NF = int(DUR * FPS)
TOPB = bg_frames('found_hd.gif', (1707, 960), step=2, bright=0.8); TOPB = [b.crop((420, 0, 1500, 960)) for b in TOPB]
BOTB = bg_frames('sun_hd.gif', (1707, 960), step=2); BOTB = [b.crop((313, 0, 1393, 960)) for b in BOTB]
EAT = seq('hollow_eat', 3, 0, 13); FOOT3 = 78 * 3
VICT = vic('hollow', 470)
GUMS = [gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']]
SMALLG = gummy('mush', 2)
w = Writer('v27_noaudio.mp4'); ev = []
EATP = 2.0
for f in range(NF):
    t = f / FPS; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    img.alpha_composite(TOPB[int(t * 6) % len(TOPB)], (0, 0)); img.alpha_composite(BOTB[int(t * 6) % len(BOTB)], (0, 960))
    # ---- top: day 1
    layer(img, lambda d: d.rectangle([0, 0, W, 300], fill=(10, 10, 20, 120)))
    u = (t % EATP) / EATP; k = min(12, int(u * 1.6 * 13))
    hx, hy = 540, 860
    if u < 0.12:   # gummy floats down into the hands
        g = SMALLG; gy = hy - 330 + u / 0.12 * 140
        img.alpha_composite(g, (hx - g.width // 2, int(gy)))
    e = EAT[k if u < 0.62 else 0]
    layer(img, lambda d: d.ellipse([hx - 70, hy - 14, hx + 70, hy + 14], fill=(0, 0, 0, 90)))
    img.alpha_composite(e, (hx - e.width // 2, hy - FOOT3))
    pop = (t % EATP) - 0.55 * EATP
    items = [(W / 2, 70, '+1 XP A DAY', 64, (255, 255, 255), 7, 255), (190, 200, 'DAY 1', 40, (140, 220, 255), 5, 255)]
    if 0 <= pop < 0.8:
        a = int(255 * min(1, (0.8 - pop) / 0.3)); items.append((hx + 150, int(hy - 300 - pop * 60), '+1 XP', 40, (120, 230, 255), 6, a))
        if pop < 1 / FPS: ev.append((round(t, 3), 'coin_8bit'))
    text_layer(img, items)
    def bar1(d):
        d.rounded_rectangle([140, 900, W - 140, 936], 12, fill=(15, 15, 30, 220), outline=(120, 200, 255, 255), width=3)
        d.rectangle([146, 906, 146 + 6 + 3 * (int(t / EATP) % 3), 930], fill=(120, 220, 255, 255))
    layer(img, bar1)
    text_layer(img, [(W / 2, 836, 'LV 1', 26, (200, 230, 255), 4, 255)])
    # ---- divider
    layer(img, lambda d: (d.rectangle([0, 952, W, 968], fill=(255, 214, 60, 255)), d.rectangle([0, 968, W, 1080], fill=(20, 12, 4, 150))))
    text_layer(img, [(W / 2, 995, '1 YEAR LATER', 54, (255, 214, 60), 7, 255)])
    # ---- bottom: level 99
    cx, cy = 540, 1560
    def aura(d):
        for r, a in ((340, 55), (270, 75), (200, 95)):
            rr = r + 16 * math.sin(t * 4 + r)
            d.ellipse([cx - rr, cy - rr - 40, cx + rr, cy + rr - 40], fill=(255, 245, 190, a))
        for i in range(14):
            ang = t * 1.5 + i * 0.449; rr = 300 + 30 * math.sin(t * 3 + i)
            sx, sy = cx + rr * math.cos(ang), cy - 40 + rr * 0.55 * math.sin(ang)
            d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 250, 200, 220))
    layer(img, aura)
    # orbiting gummies behind / in front
    orb = []
    for i, g in enumerate(GUMS):
        ang = t * 1.2 + i * 2 * math.pi / 5; orb.append((math.sin(ang), cx + 300 * math.cos(ang), cy - 60 + 110 * math.sin(ang), g))
    for z, x, y, g in sorted(orb):
        if z < 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    v = VICT[int(t * 8) % len(VICT)]
    img.alpha_composite(v, (cx - v.width // 2, cy + 125 - v.height))
    for z, x, y, g in sorted(orb):
        if z >= 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    def bar2(d):
        d.rounded_rectangle([140, 1810, W - 140, 1856], 14, fill=(30, 20, 5, 220), outline=(255, 214, 60, 255), width=4)
        sh = int((t * 300) % (W - 300))
        d.rectangle([148, 1818, W - 148, 1848], fill=(255, 196, 40, 255)); d.rectangle([148 + sh, 1818, 148 + sh + 60, 1848], fill=(255, 245, 190, 255))
    layer(img, bar2)
    text_layer(img, [(W / 2, 1745, 'LV 99', 52, (255, 214, 60), 7, 255), (190, 1110, 'DAY 365', 40, (255, 230, 150), 5, 255)])
    w.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/c_{f:04d}.png')
w.close(); json.dump(ev, open('v27_ev.json', 'w')); print('done')
