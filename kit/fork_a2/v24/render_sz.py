import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['WHICH VIBE', 'DO I GIVE OFF?'], accent=1)
import numpy as np
BG = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.5, blur=3)
GUIDES = [('joy', '1'), ('cyrus', '2'), ('cleo', '3'), ('ray', '4')]
IDL = {g: idle(g, 3) for g, _ in GUIDES}
JARS = Image.open(A + 'jars.png').convert('RGBA')
def jar(i):
    j = JARS.crop((i * 200, 0, i * 200 + 200, 200)); px = np.array(j); bg = (px[:, :, 0] == px[0, 0, 0]) & (px[:, :, 1] == px[0, 0, 1]) & (px[:, :, 2] == px[0, 0, 2]); px[bg, 3] = 0
    im = crop(Image.fromarray(px)); return im.resize((int(im.width * 130 / im.height), 130), Image.NEAREST)
JAR = [(jar(0), 'acv', 'A'), (jar(2), 'mush', 'B'), (jar(1), 'cre', 'C'), (jar(3), 'mel', 'D')]
GM = {k: gummy(k, 2) for k in ('acv', 'mush', 'cre', 'mel')}
REALMS = []
for nm, sym in (('found_hd.gif', '!'), ('sun_hd.gif', '@'), ('vit_hd.gif', '#'), ('recov_hd.gif', '$')):
    fr = bg_frames(nm, (160, 120), box=(960 - 400, 200, 960 + 400, 800), step=3)
    REALMS.append((fr, sym))
FRM = crop(Image.open('../gen/frame/00.png').convert('RGBA')).resize((190, 150), Image.NEAREST)
def it(k, i):
    im = crop(Image.open(f'../gen/{k}/{i:02d}.png').convert('RGBA')); return up(im, max(1, int(130 / max(im.width, im.height))))
ITEMS = [(it('book', 0), 'W'), (it('coins', 0), 'X'), (it('hourglass', 5), 'Y'), (it('backpack', 1), 'Z')]
PX0, PX1 = 76, 881
ROWS = [('GUIDE', HB + 14, 260), ('GUMMY', HB + 280, 184), ('REALM', HB + 470, 184), ('ITEM', HB + 660, 184)]
COLX = [PX0 + (PX1 - PX0) * (i + 0.5) / 4 for i in range(4)]
rng = random.Random(2); SPK = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, 6.28)) for _ in range(40)]
DUR = 9.0; wr = Writer('sz24_noaudio.mp4'); events = []
for r in range(4): events.append((round(0.4 + r * 0.35, 3), 'whoosh_8bit'))
events.append((2.2, 'chime'))
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2 + 14 * math.sin(t + p), x + 2, y + 2 + 14 * math.sin(t + p)], fill=(255, 240, 190, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SPK])
    for r, (lab, y0, hh) in enumerate(ROWS):
        u = min(1, max(0, (t - 0.4 - r * 0.35) / 0.35)); ease = 1 - (1 - u) ** 3
        if u <= 0: continue
        dy = int((1 - ease) * 80); al = int(255 * u)
        layer(img, lambda d, y0=y0, hh=hh, dy=dy, al=al: d.rounded_rectangle([PX0, y0 + dy, PX1, y0 + hh + dy], 20, fill=(16, 10, 30, int(205 * al / 255)), outline=(255, 214, 60, al), width=4))
        layer(img, lambda d, y0=y0, dy=dy, al=al, lab=lab: d.rectangle([PX0 + 22, y0 + dy - 12, PX0 + 34 + len(lab) * 18, y0 + dy + 12], fill=(16, 10, 30, al)))
        text_layer(img, [(PX0 + 28 + len(lab) * 9, y0 + dy - 9, lab, 18, (255, 214, 60), 4, al)])
        for i, cx in enumerate(COLX):
            bob = int(5 * math.sin(t * 3 + i + r))
            if r == 0:
                g, key = GUIDES[i]; s = IDL[g][int(t * 8 + i) % len(IDL[g])]
                img.alpha_composite(s, (int(cx - s.width / 2), y0 + dy + 212 - 78 * 3))
            elif r == 1:
                j, gk, key = JAR[i]; img.alpha_composite(j, (int(cx - j.width / 2) - 10, y0 + dy + 12 + bob))
                gg = GM[gk]; img.alpha_composite(gg, (int(cx + 26), y0 + dy + 92 + bob))
            elif r == 2:
                fr, key = REALMS[i]; fi = fr[int(t * 6) % len(fr)]
                img.alpha_composite(fi, (int(cx - 80), y0 + dy + 18)); img.alpha_composite(FRM, (int(cx - 95), y0 + dy + 3))
            else:
                ii, key = ITEMS[i]; img.alpha_composite(ii, (int(cx - ii.width / 2), y0 + dy + 76 - ii.height // 2 + bob))
            key = [GUIDES, JAR, REALMS, ITEMS][r][i][-1]
            text_layer(img, [(cx, y0 + dy + hh - 40, key, 30, (255, 255, 255), 6, al)])
    if t > 2.0:
        a = int(255 * min(1, (t - 2.0) / 0.4)); pulse = 1 + 0.04 * math.sin(t * 5)
        layer(img, lambda d: d.rounded_rectangle([PX0 + 20, HB + 858, PX1 - 20, HB + 990], 24, fill=(255, 214, 60, int(a * 0.95)), outline=(20, 15, 35, a), width=5))
        text_layer(img, [((PX0 + PX1) / 2, HB + 884, 'COMMENT YOUR COMBO', int(36 * pulse), (30, 20, 40), 0, a), ((PX0 + PX1) / 2, HB + 944, 'LIKE 2 B @ X', 24, (60, 40, 50), 0, a)])
    img.alpha_composite(HOOK)
    wr.write(img)
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': events}, open('sz24_events.json', 'w')); print('done')
