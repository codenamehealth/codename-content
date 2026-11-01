import sys; sys.path.insert(0, '../fork1')
from common import *
from PIL import ImageOps
PW, PH = 1000, 700; PX = 40; PY1, PY2 = 280, 1010
CROP = (290, 0, 1630, 938)
import numpy as np
def crest(fr):
    box = (820, 20, 1110, 126); im = fr.crop(box); a = np.array(im).astype(int)
    lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11; m = (lum < 185) & ((a[..., 0] - a[..., 2]) > 70)
    g = np.array(ImageOps.colorize(ImageOps.grayscale(im), (40, 50, 80), (215, 230, 255)))
    out = a.copy(); out[m] = g[m]; fr = fr.copy(); fr.paste(Image.fromarray(out.astype('uint8')), box[:2]); return fr
src = Image.open(A + 'sun_hd.gif'); PAN = []; PANB = []
for i in range(0, src.n_frames, 2):
    src.seek(i); fr = src.convert('RGB')
    PAN.append(fr.crop(CROP).resize((PW, PH), Image.NEAREST).convert('RGBA'))
    PANB.append(crest(fr).crop(CROP).resize((PW, PH), Image.NEAREST).convert('RGBA'))
BGF = bg_frames('sun_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=4, bright=0.55, blur=6)
CY = idle('cyrus', 3); JO = idle('joy', 3)
SL = seq(PL + 'race/slime_idle_c', 3, 1)
G_M = gummy('mush', 2); G_A = gummy('acv', 2); G_G = gummy('gold', 2)
SUN = ((830 - 290) * PW / 1340, 18, (1100 - 290) * PW / 1340, 104)
def silver(im):
    g = ImageOps.grayscale(im.convert('RGB')); return ImageOps.colorize(g, (40, 50, 80), (215, 230, 255)).convert('RGBA')
def panel(t, bottom):
    p = (PANB if bottom else PAN)[int(t * 6) % len(PAN)].copy()
    # gummy on the stairs
    g = G_A if bottom else G_M; bob = int(3 * math.sin(t * 4))
    p.alpha_composite(g, (488 - g.width // 2, 438 - g.height + bob))
    # gold gummy shrine glow on the floor seal (same in both)
    p.alpha_composite(G_G, (500 - G_G.width // 2, 560 - G_G.height // 2 + int(2 * math.sin(t * 3))))
    # guides
    cy = CY[int(t * 8) % len(CY)]; p.alpha_composite(cy, (190 - cy.width // 2, 640 - 78 * 3))
    jo = JO[int(t * 8 + 3) % len(JO)]; p.alpha_composite(jo, (330 - jo.width // 2, 655 - 78 * 3))
    if not bottom:
        s = SL[int(t * 10) % len(SL)]; p.alpha_composite(s, (790 - s.width // 2, 660 - s.height + 20))
    return p
TL, TE = 8.0, 10.6; NF = int(TE * FPS); wr = Writer('v41_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS; img = BGF[int(t * 3) % len(BGF)].copy()
    def frame_layer(d):
        for py in (PY1, PY2):
            d.rectangle([PX - 12, py - 12, PX + PW + 12, py + PH + 12], fill=(40, 22, 8, 255))
            d.rectangle([PX - 8, py - 8, PX + PW + 8, py + PH + 8], outline=(255, 214, 60, 255), width=6)
    layer(img, frame_layer)
    img.alpha_composite(panel(t, False), (PX, PY1)); img.alpha_composite(panel(t, True), (PX, PY2))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, 0, W, 250], fill=(20, 10, 4, 170))
    rem = max(0.0, 1 - t / TL)
    d.rounded_rectangle([90, 1760, 990, 1800], 14, fill=(20, 10, 4, 200), outline=(255, 214, 60, 255), width=4)
    if rem > 0:
        col = (120, 220, 90) if rem > 0.5 else ((255, 200, 60) if rem > 0.25 else (255, 90, 70))
        d.rounded_rectangle([96, 1766, 96 + int(888 * rem), 1794], 10, fill=col + (255,))
    img.alpha_composite(L)
    items = [(W / 2, 60, 'FIND 3 DIFFERENCES', 56, (255, 214, 60), 7, 255), (W / 2, 150, 'in the Sun Temple', 34, (255, 255, 255), 6, 255)]
    if t < TL:
        items.append((W / 2, 1830, f'{int(math.ceil(TL - t))}', 50, (255, 255, 255), 6, 255))
    else:
        u = t - TL; a = int(255 * min(1, u / 0.3))
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L2).rounded_rectangle([110, 800, 970, 1170], 30, fill=(20, 12, 30, int(225 * a / 255)), outline=(255, 214, 60, a), width=6)
        img.alpha_composite(L2)
        items += [(W / 2, 850, "TIME'S UP!", 64, (255, 214, 60), 8, a), (W / 2, 970, 'How many did you spot?', 34, (255, 255, 255), 5, a), (W / 2, 1050, 'Comment 0, 1, 2 or 3', 34, (120, 230, 110), 5, a)]
    text_layer(img, items)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p41_{f:04d}.png')
wr.close()
for s in range(int(TL)): ev.append((float(s), 'tick_8bit'))
ev.append((TL, 'buzz_8bit'))
json.dump(ev, open('v41_ev.json', 'w')); print('done')
