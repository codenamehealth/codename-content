import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 3; FOOTY = 78 * K
RUN = seq('../../pixellab/race/cyrus_run', K, 1, 9)
SLP = seq('../gen/cyrus_sleep', K, 0, 13)
WALK = seq('../gen/cleo_walk', K, 1, 9)
WIN = seq('../gen/cleo_win', K, 0, 9)
FLAG = up(crop(Image.open('../gen/flag/00.png').convert('RGBA')), 4).transpose(Image.FLIP_LEFT_RIGHT)
GUM = gummy('cre', 3)
TOP = bg_frames('sun_hd.gif', (W, 760), box=(380, 0, 380 + 1160, 816), step=2, bright=0.8)
BOT = bg_frames('vit_hd.gif', (W, 760), box=(380, 0, 380 + 1160, 816), step=2, bright=0.8)
P1, P2 = 300, 1110; GROUND = 650; X0, XF = 150, 940
DUR = 10.0; NF = int(DUR * FPS)
GX = [330, 500, 670, 840]
def ease_io(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
wr = Writer('v47_noaudio.mp4'); ev = []; popped = {}
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for py, bgs, lab, col in ((P1, TOP, 'MOTIVATION', (255, 165, 50)), (P2, BOT, 'DISCIPLINE', (100, 165, 255))):
        img.alpha_composite(bgs[int(t * 5) % len(bgs)], (0, py))
        layer(img, lambda d: (d.rectangle([0, py + GROUND + 4, W, py + 760], fill=(14, 10, 24, 90)), d.rectangle([0, py, W, py + 760], outline=col + (255,), width=8)))
        d = ImageDraw.Draw(img)
        layer(img, lambda dd: dd.rounded_rectangle([30, py + 26, 30 + dd.textlength(lab, font=F(46)) + 40, py + 104], 16, fill=(14, 10, 24, 200)))
        d = ImageDraw.Draw(img); d.text((50, py + 42), lab, font=F(46), fill=col, stroke_width=6, stroke_fill=(20, 15, 35))
        img.alpha_composite(FLAG, (1050 - FLAG.width, py + GROUND - FLAG.height + 8))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 70, 'MOTIVATION', F(64), (255, 165, 50), 7); ctext(d, W / 2, 160, 'vs', F(40), (235, 235, 235), 5); ctext(d, W / 2, 210, 'DISCIPLINE', F(64), (100, 165, 255), 7)
    # --- Cyrus (top)
    gy = P1 + GROUND
    if t < 0.4: x = X0; spr = RUN[0]
    elif t < 2.6:
        u = (t - 0.4) / 2.2; x = X0 + (600 - X0) * (u ** 0.85); spr = RUN[int(t * 22) % 8]
        layer(img, lambda dd: [dd.rectangle([x - 110 - q * 46, gy - 120 + q * 34, x - 50 - q * 46, gy - 114 + q * 34], fill=(255, 230, 160, 170)) for q in range(3)])
        if f % 4 == 0:
            pass
    else:
        x = 600; u = t - 2.6; k = min(12, int(u * 11)); spr = SLP[k]
        if k >= 9:
            for q in range(3):
                zz = (u * 0.8 + q / 3) % 1.0
                text_layer(img, [(x + 40 + zz * 80, gy - 150 - zz * 140, 'Z', 26 + q * 10, (255, 255, 255), 5, int(255 * (1 - zz)))])
    if 0.4 <= t < 2.6:
        layer(img, lambda dd: [dd.ellipse([x - 70 - q * 30 - (t * 300 % 30), gy - 12 - q * 4, x - 40 - q * 30 - (t * 300 % 30), gy + 4], fill=(230, 210, 170, 140 - q * 40)) for q in range(3)])
    layer(img, lambda dd: dd.ellipse([x - 50, gy - 10, x + 50, gy + 10], fill=(0, 0, 0, 80)))
    img.alpha_composite(spr, (int(x - spr.width / 2), int(gy - FOOTY)))
    if abs(t - 0.4) < 0.5 / FPS: ev.append((0.4, 'whoosh_8bit'))
    if abs(t - 3.4) < 0.5 / FPS: ev.append((3.4, 'poof'))
    # --- Cleo (bottom)
    gy = P2 + GROUND; T_ARR = 8.0
    for i, gxp in enumerate(GX):
        if i in popped and t >= popped[i]:
            u = t - popped[i]
            if u < 0.9: text_layer(img, [(gxp, gy - 300 - u * 60, '+1', 44, (120, 190, 255), 6, int(255 * min(1, (0.9 - u) / 0.3)))])
            if u < 0.4:
                layer(img, lambda dd: [dd.rectangle([gxp + (20 + 90 * u) * math.cos(q * 0.785) - 5, gy - 60 + (20 + 90 * u) * math.sin(q * 0.785) - 5,
                                                     gxp + (20 + 90 * u) * math.cos(q * 0.785) + 5, gy - 60 + (20 + 90 * u) * math.sin(q * 0.785) + 5], fill=(190, 225, 255, int(255 * (1 - u / 0.4)))) for q in range(8)])
            continue
        bob = int(8 * math.sin(t * 4 + i))
        layer(img, lambda dd: dd.ellipse([gxp - 40, gy - 100 + bob, gxp + 40, gy - 20 + bob], fill=(120, 180, 255, 60)))
        img.alpha_composite(GUM, (int(gxp - GUM.width / 2), int(gy - 60 - GUM.height / 2 + bob)))
    if t < 0.4: x = X0; spr = WALK[0]
    elif t < T_ARR:
        x = X0 + (XF - 60 - X0) * (t - 0.4) / (T_ARR - 0.4); spr = WALK[int(t * 9) % 8]
        for i, gxp in enumerate(GX):
            if i not in popped and x >= gxp - 10: popped[i] = t; ev.append((round(t, 3), 'coin_8bit'))
    else:
        x = XF - 60; spr = WIN[min(8, int((t - T_ARR) * 10))]
        if abs(t - T_ARR) < 0.5 / FPS: ev.append((round(t, 3), 'victory'))
        u = t - T_ARR
        layer(img, lambda dd: [dd.rectangle([x + 50 + 80 * math.cos(t * 3 + q * 1.26), gy - 260 + 60 * math.sin(t * 3 + q * 1.26), x + 58 + 80 * math.cos(t * 3 + q * 1.26), gy - 252 + 60 * math.sin(t * 3 + q * 1.26)], fill=(255, 230, 120, 230)) for q in range(5)])
    layer(img, lambda dd: dd.ellipse([x - 50, gy - 10, x + 50, gy + 10], fill=(0, 0, 0, 80)))
    img.alpha_composite(spr, (int(x - spr.width / 2), int(gy - FOOTY)))
    if t > 8.4:
        a = int(255 * min(1, (t - 8.4) / 0.4))
        text_layer(img, [(W / 2, 1878 - 6, 'WHICH ONE ARE YOU?', 38, (255, 214, 60), 6, a)])
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v47_ev.json', 'w')); print('done', len(ev))
