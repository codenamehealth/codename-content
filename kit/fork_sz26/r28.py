import sys; sys.path.insert(0, '../fork1'); sys.path.insert(0, '../pixellab/safezone')
from hook import hook_layer
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 13.0; NF = int(DUR * FPS)
HOOK, HB = hook_layer(['SWIPE TO', 'THE BEAT!'], accent=1)
print('hook bottom', HB)
BG = up(Image.open('../fork3/tavern2/00.png').convert('RGBA'), 3)
B0, BP = 0.03, 0.4643
HITS = [B0 + BP * k for k in range(4, 20, 2)]           # 8 swipes on every other beat
KINDS = ['mush', 'acv', 'mel', 'cre', 'mush', 'acv', 'mel', 'cre']
TFIN = HITS[-1] + 1.0
EAT1 = [Image.open(f'../fork3/hollow_eat/{i:02d}.png').convert('RGBA') for i in range(13)]
VICT = vic('hollow', 576)
G2 = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}; G1 = {k: gummy(k, 1) for k in G2}
HX, HY = 390, 1480            # Hollow feet
RX, RY = 800, 830             # hit ring (lane runs up the right side)
LB = 1500                     # lane bottom
def hscale(n): return 3 if n < 2 else (4 if n < 5 else 5)
w = Writer('v28_noaudio.mp4'); ev = []
rr = random.Random(4)
for f in range(NF):
    t = f / FPS; img = BG.copy()
    eaten = sum(1 for h in HITS if t >= h + 0.25)
    # spotlight on the stage
    layer(img, lambda d: (d.ellipse([HX - 300, HY - 60, HX + 300, HY + 60], fill=(255, 220, 140, 60))))
    # header + gummy counter
    for i in range(8):
        x = W / 2 + (i - 3.5) * 104; y = HB + 56
        if i < eaten:
            g = G2[KINDS[i]]; pop = max(0, 1 - (t - HITS[i] - 0.25) / 0.2); g2 = up(g, 1 + 0.4 * pop) if pop > 0 else g
            img.alpha_composite(g2, (int(x - g2.width / 2), int(y - g2.height / 2)))
        else:
            layer(img, lambda d, x=x, y=y: d.ellipse([x - 26, y - 26, x + 26, y + 26], outline=(255, 230, 180, 160), width=4))
    # Hollow
    if t < TFIN:
        last = max([h for h in HITS if h <= t], default=None)
        k = 0
        if last is not None:
            u = t - last
            if u < 0.5: k = [4, 5, 6, 7, 8][min(4, int(u / 0.1))]
            elif u < 0.8: k = [9, 10, 11][min(2, int((u - 0.5) / 0.1))]
        sc = hscale(eaten); spr = up(EAT1[k], sc)
        bob = int(6 * abs(math.sin(math.pi * (t - B0) / BP)))
        layer(img, lambda d: d.ellipse([HX - 26 * sc, HY - 5 * sc, HX + 26 * sc, HY + 5 * sc], fill=(0, 0, 0, 90)))
        img.alpha_composite(spr, (HX - spr.width // 2, HY - 78 * sc - bob))
        mouth = (HX, HY - 78 * sc + 30 * sc)
    else:
        u = t - TFIN
        v = VICT[int(u * 8) % len(VICT)]
        layer(img, lambda d: d.ellipse([540 - 300, HY - 50, 540 + 300, HY + 50], fill=(0, 0, 0, 90)))
        img.alpha_composite(v, (540 - v.width // 2, HY - v.height))
        mouth = (HX, HY - 400)
    # swipe lane
    if t < TFIN:
        def lane(d):
            d.rounded_rectangle([RX - 80, RY - 80, RX + 80, LB], 40, fill=(20, 12, 6, 170), outline=(255, 214, 60, 200), width=4)
            for j in range(5):
                yy = LB - 20 - ((t * 260 + j * 70) % 560)
                if yy > RY + 90: d.polygon([(RX - 26, yy + 14), (RX, yy - 12), (RX + 26, yy + 14)], outline=(255, 230, 160, 120), fill=None, width=4)
            beat = (t - B0) / BP; pulse = max(0, 1 - (beat - round(beat)) ** 2 * 12)
            d.ellipse([RX - 66, RY - 66, RX + 66, RY + 66], outline=(255, 240, 200, 220), width=6 + int(4 * pulse))
        layer(img, lane)
    for i, h in enumerate(HITS):
        g = G2[KINDS[i]]
        if h - 1.0 <= t < h:
            p = (t - (h - 1.0)) / 1.0; y = LB + 40 - (LB + 40 - RY) * p
            gc = g.crop((0, 0, g.width, max(1, min(g.height, int(LB - 8 - (y - g.height / 2))))))
            img.alpha_composite(gc, (int(RX - g.width / 2), int(y - g.height / 2)))
        elif h <= t < h + 0.25 and t < TFIN:
            p = (t - h) / 0.25; x = RX + (mouth[0] - RX) * p; y = RY + (mouth[1] - RY) * p - 180 * math.sin(math.pi * p)
            gg = up(G1[KINDS[i]], 2 - p * 0.8)
            img.alpha_composite(gg, (int(x - gg.width / 2), int(y - gg.height / 2)))
        if 0 <= t - h < 0.35:
            a = int(255 * (1 - (t - h) / 0.35)); r = 66 + (t - h) * 260
            layer(img, lambda d, r=r, a=a: d.ellipse([RX - r, RY - r, RX + r, RY + r], outline=(255, 214, 60, a), width=8))
        if 0.25 <= t - h < 1.0 and t < TFIN:
            u = t - h - 0.25; a = int(255 * min(1, (0.75 - u) / 0.3))
            text_layer(img, [(HX + 240, int(HY - 430 - u * 60), '+1', 54, (255, 214, 60), 7, a), (RX, RY - 130, 'PERFECT!', 30, (140, 255, 140), 5, a)])
        if abs(t - h) < 0.5 / FPS: ev.append((round(h, 3), 'whoosh_8bit'))
        if abs(t - h - 0.25) < 0.5 / FPS: ev.append((round(h + 0.25, 3), 'coin_8bit'))
    if t < HITS[0] - 0.1:
        text_layer(img, [(RX, RY - 150, 'SWIPE UP', 34, (255, 255, 255), 6, 255)])
    if t >= TFIN:
        u = t - TFIN; a = int(255 * min(1, u / 0.25))
        text_layer(img, [(W / 2, HB + 110, 'THAT WAS', 64, (255, 255, 255), 8, a), (W / 2, HB + 196, 'SO YUMMY!', 76, (255, 214, 60), 9, a)])
        cr = random.Random(f)
        def conf(d):
            for _ in range(60):
                x = cr.uniform(0, W); y = (cr.uniform(-300, H) + u * 600) % H
                d.rectangle([x, y, x + 12, y + 12], fill=cr.choice([(255, 214, 60, 255), (255, 120, 120, 255), (120, 220, 120, 255), (150, 180, 255, 255)]))
        layer(img, conf)
        if not any(e[1] == 'victory' for e in ev): ev.append((round(TFIN, 3), 'victory'))
    img.alpha_composite(HOOK)
    w.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/d_{f:04d}.png')
w.close(); json.dump(ev, open('v28_ev.json', 'w')); print('done', [round(h, 2) for h in HITS], TFIN)
