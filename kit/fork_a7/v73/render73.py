import sys; sys.path.insert(0, '..')
from common7 import *
import math
G = '../gen/'
SC = up(crop(Image.open(G + 'scale/03.png').convert('RGBA')), 3)
# scale geometry (native in cropped image: bbox started at (14,7))
DIAL = ((64.5 - 14) * 3, (22.5 - 7) * 3); DR = 26
PLAT_Y = (64 - 7) * 3; PLAT_X0, PLAT_X1 = (16 - 14) * 3, (78 - 14) * 3
BG = bg_frames('sun_hd.gif', (W, H), box=(420, 0, 1500, 1080), step=2, bright=0.45, blur=6)
PW, PH = 516, 690
PANELS = [  # bg gif, crop box, members, weight
    ('vit_hd.gif', (560, 20, 1360, 1080), ['cleo', 'cleo', 'cleo'], 45, 'cre'),
    ('recov_hd.gif', (560, 20, 1360, 1080), ['cleo', 'ray', 'ray'], 39, 'mel'),
    ('found_hd.gif', (560, 20, 1360, 1080), ['ray', 'hollow', 'hollow'], 26, 'acv'),
    ('hub.gif', (560, 20, 1360, 1080), ['hollow', 'cleo'], None, 'gold')]
PBG = [bg_frames(p[0], (PW, PH), box=p[1], step=3, bright=0.9) for p in PANELS]
IDL = {g: idle(g, 2) for g in ['cleo', 'ray', 'hollow']}
GUMI = {k: gummy(k, 2) for k in GUMK}
POS = [(14, 352), (538, 352), (14, 1066), (538, 1066)]
T_DROP = [0.5, 1.7, 2.9, 4.1]; DUR = 11.0
def needle_angle(w): return math.radians(-135 + 270 * min(1, w / 60))
wr = Writer('v73_noaudio.mp4'); ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 4) % len(BG)].copy()
    for k, (bgn, box, mem, wt, gk) in enumerate(PANELS):
        px, py = POS[k]
        pan = PBG[k][int(t * 4 + k) % len(PBG[k])].copy()
        # scale
        sx = PW // 2 - SC.width // 2 + 40; sy = PH - SC.height - 120
        pan.alpha_composite(SC, (sx, sy))
        # members drop onto the platform
        t0 = T_DROP[k]; n = len(mem); landed = 0
        for j, g in enumerate(mem):
            tj = t0 + j * 0.18
            fx = sx + PLAT_X0 + 34 + (j + (0.5 if n == 2 else 0)) * 62
            fy = sy + PLAT_Y + 22
            if t < tj: continue
            u = t - tj
            if u < 0.35: yy = fy - 520 * (1 - u / 0.35) ** 2
            else:
                landed += 1; v = u - 0.35; yy = fy - abs(math.sin(v * 9)) * 26 * math.exp(-v * 5)
            if abs(u - 0.35) < 0.5 / FPS: ev.append((round(t, 3), 'boing'))
            fr = IDL[g][(int(t * 8) + j * 3) % len(IDL[g])]
            pan.alpha_composite(fr, (int(fx - fr.width / 2), int(yy - 78 * 2)))
        # weight shown on needle and plate
        tf = t0 + (n - 1) * 0.18 + 0.35
        if wt is not None:
            cur = 0 if t < t0 + 0.35 else wt * min(1, (t - (t0 + 0.35)) / ((n - 1) * 0.18 + 0.5)) * (landed / n if landed < n else 1)
            cur += (math.sin(t * 20) * 2.5 * math.exp(-max(0, t - tf) * 3) if t > tf else 0)
            shown = f'{int(round(min(wt, max(0, cur))))} kg'
        else:
            cur = 30 + 25 * math.sin(t * 7.3) * (1 if t > t0 + 0.4 else 0); shown = '? kg'
        a = needle_angle(max(0, cur)); cx, cy = sx + DIAL[0], sy + DIAL[1]
        d = ImageDraw.Draw(pan)
        d.line([(cx, cy), (cx + math.sin(a) * DR, cy - math.cos(a) * DR)], fill=(200, 30, 30, 255), width=5)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(40, 30, 20, 255))
        # LCD plate
        layer(pan, lambda dd: (dd.rounded_rectangle([PW // 2 - 130, PH - 100, PW // 2 + 130, PH - 28], 10, fill=(18, 22, 40, 235), outline=(255, 214, 60, 255), width=4),
                               dd.rectangle([PW // 2 - 108, PH - 88, PW // 2 + 108, PH - 40], fill=(120, 220, 90, 255))))
        col = (20, 40, 20) if wt is not None or int(t * 4) % 2 == 0 else (200, 30, 30)
        d = ImageDraw.Draw(pan); fnt = F(34); tw = d.textlength(shown, font=fnt); d.text((PW // 2 - tw / 2, PH - 82), shown, font=fnt, fill=col + (255,))
        if wt is not None and abs(t - (tf + 0.4)) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit'))
        # guild gummy badge
        gg = GUMI[gk]; pan.alpha_composite(gg, (PW - gg.width - 18, 18 + int(4 * math.sin(t * 3 + k))))
        frame = Image.new('RGBA', (PW + 12, PH + 12), (255, 214, 60, 255)); ImageDraw.Draw(frame).rectangle([3, 3, PW + 8, PH + 8], fill=(30, 22, 40, 255))
        frame.alpha_composite(pan, (6, 6)); img.alpha_composite(frame, (px - 6 + 6, py - 6))
    layer(img, lambda dd: dd.rectangle([0, 0, W, 330], fill=(16, 12, 24, 170)))
    text_layer(img, [(W / 2, 90, "WHAT'S THE", 72, (255, 255, 255), 8, 255), (W / 2, 190, 'ANSWER?', 80, (255, 214, 60), 9, 255)])
    if t > 5.2:
        a = int(255 * min(1, (t - 5.2) / 0.4))
        text_layer(img, [(W / 2, 1790, 'Comment your answer', 40, (255, 255, 255), 6, a)])
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v73_ev.json', 'w')); print('done', len(ev))
