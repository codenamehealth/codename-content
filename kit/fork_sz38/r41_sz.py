import sys; sys.path.insert(0, '../fork1')
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['FIND 3', 'DIFFERENCES'], accent=1)
from PIL import ImageOps
PW, PH = 640, 448; PX = 220; PY1, PY2 = 572, 1036; KQ = 0.64
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
CY = idle('cyrus', 2); JO = idle('joy', 2)
SL = seq(PL + 'race/slime_idle_c', 2, 1)
G_M = gummy('mush', 2); G_A = gummy('acv', 2); G_G = gummy('gold', 2)
SUN = ((830 - 290) * PW / 1340, 18, (1100 - 290) * PW / 1340, 104)
def silver(im):
    g = ImageOps.grayscale(im.convert('RGB')); return ImageOps.colorize(g, (40, 50, 80), (215, 230, 255)).convert('RGBA')
def panel(t, bottom):
    p = (PANB if bottom else PAN)[int(t * 6) % len(PAN)].copy()
    # gummy on the stairs
    g = G_A if bottom else G_M; bob = int(3 * math.sin(t * 4))
    p.alpha_composite(g, (int(488 * KQ) - g.width // 2, int(438 * KQ) - g.height + bob))
    # gold gummy shrine glow on the floor seal (same in both)
    p.alpha_composite(G_G, (int(500 * KQ) - G_G.width // 2, int(560 * KQ) - G_G.height // 2 + int(2 * math.sin(t * 3))))
    # guides
    cy = CY[int(t * 8) % len(CY)]; p.alpha_composite(cy, (int(190 * KQ) - cy.width // 2, int(640 * KQ) - 78 * 2))
    jo = JO[int(t * 8 + 3) % len(JO)]; p.alpha_composite(jo, (int(330 * KQ) - jo.width // 2, int(655 * KQ) - 78 * 2))
    if not bottom:
        s = SL[int(t * 10) % len(SL)]; p.alpha_composite(s, (int(790 * KQ) - s.width // 2, int(660 * KQ) - s.height + 13))
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
    rem = max(0.0, 1 - t / TL)
    d.rounded_rectangle([90, HB + 14, 900, HB + 50], 14, fill=(20, 10, 4, 200), outline=(255, 214, 60, 255), width=4)
    if rem > 0:
        col = (120, 220, 90) if rem > 0.5 else ((255, 200, 60) if rem > 0.25 else (255, 90, 70))
        d.rounded_rectangle([96, HB + 20, 96 + int(798 * rem), HB + 44], 10, fill=col + (255,))
    img.alpha_composite(L)
    items = []
    if t < TL:
        items.append((960, HB + 8, f'{int(math.ceil(TL - t))}', 48, (255, 255, 255), 6, 255))
    else:
        u = t - TL; a = int(255 * min(1, u / 0.3))
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L2).rounded_rectangle([110, 860, 970, 1100], 30, fill=(20, 12, 30, int(225 * a / 255)), outline=(255, 214, 60, a), width=6)
        img.alpha_composite(L2)
        items += [(W / 2, 890, "TIME'S UP!", 64, (255, 214, 60), 8, a), (W / 2, 985, 'How many did you spot?', 34, (255, 255, 255), 5, a), (W / 2, 1040, 'Comment 0, 1, 2 or 3', 34, (120, 230, 110), 5, a)]
    text_layer(img, items)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (30, 150, 300): img.convert('RGB').save(f'prev/d41_{f:04d}.png')
wr.close()
for s in range(int(TL)): ev.append((float(s), 'tick_8bit'))
ev.append((TL, 'buzz_8bit'))
json.dump(ev, open('v41_ev.json', 'w')); print('done')
