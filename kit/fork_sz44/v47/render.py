import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 3; FOOTY = 78 * K
RUN = seq('../../pixellab/race/cyrus_run', K, 1, 9)
SLP = seq('../../fork_a5/gen/cyrus_sleep', K, 0, 13)
WALK = seq('../../fork_a5/gen/cleo_walk', K, 1, 9)
WIN = seq('../../fork_a5/gen/cleo_win', K, 0, 9)
FLAG = up(crop(Image.open('../../fork_a5/gen/flag/00.png').convert('RGBA')), 4).transpose(Image.FLIP_LEFT_RIGHT)
GUM = gummy('cre', 3)
PX0, PW, PH = 70, 817, 500
TOP = bg_frames('sun_hd.gif', (PW, PH), box=(470, 170, 470 + 980, 770), step=2, bright=0.8)
BOT = bg_frames('vit_hd.gif', (PW, PH), box=(470, 170, 470 + 980, 770), step=2, bright=0.8)
HOOK, HB = hook_layer(['MOTIVATION', 'VS DISCIPLINE'], accent=0, color=(255, 165, 50), border=(255, 214, 60))
print('hook bottom', HB)
P1 = HB + 12; P2 = P1 + PH + 12; GROUND = 440; X0, XF = 160, 800
print('panels', P1, P2, P2 + PH)
DUR = 10.0; NF = int(DUR * FPS)
GX = [300, 430, 560, 690]
def ease_io(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
wr = Writer('v47_noaudio.mp4'); ev = []; popped = {}
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for py, bgs, lab, col in ((P1, TOP, 'MOTIVATION', (255, 165, 50)), (P2, BOT, 'DISCIPLINE', (100, 165, 255))):
        img.alpha_composite(bgs[int(t * 5) % len(bgs)], (PX0, py))
        layer(img, lambda d: (d.rectangle([PX0, py + GROUND + 4, PX0 + PW - 1, py + PH - 1], fill=(14, 10, 24, 90)), d.rectangle([PX0, py, PX0 + PW - 1, py + PH - 1], outline=col + (255,), width=8)))
        d = ImageDraw.Draw(img)
        layer(img, lambda dd: dd.rounded_rectangle([PX0 + 20, py + 22, PX0 + 20 + dd.textlength(lab, font=F(40)) + 36, py + 92], 16, fill=(14, 10, 24, 200)))
        d = ImageDraw.Draw(img); d.text((PX0 + 38, py + 38), lab, font=F(40), fill=col, stroke_width=6, stroke_fill=(20, 15, 35))
        img.alpha_composite(FLAG, (PX0 + PW - 16 - FLAG.width, py + GROUND - FLAG.height + 8))
    d = ImageDraw.Draw(img)
    # --- Cyrus (top)
    gy = P1 + GROUND
    if t < 0.4: x = X0; spr = RUN[0]
    elif t < 2.6:
        u = (t - 0.4) / 2.2; x = X0 + (540 - X0) * (u ** 0.85); spr = RUN[int(t * 22) % 8]
        layer(img, lambda dd: [dd.rectangle([x - 110 - q * 46, gy - 120 + q * 34, x - 50 - q * 46, gy - 114 + q * 34], fill=(255, 230, 160, 170)) for q in range(3)])
        if f % 4 == 0:
            pass
    else:
        x = 540; u = t - 2.6; k = min(12, int(u * 11)); spr = SLP[k]
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
        layer(img, lambda dd: dd.rounded_rectangle([118, P2 - 46, 838, P2 + 34], 16, fill=(14, 10, 24, int(225 * a / 255)), outline=(255, 214, 60, a), width=4))
        text_layer(img, [(478, P2 - 26, 'WHICH ONE ARE YOU?', 38, (255, 214, 60), 6, a)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); print('done', len(ev))
