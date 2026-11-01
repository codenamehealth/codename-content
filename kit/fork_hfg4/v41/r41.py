import sys; sys.path.insert(0, '../../fork1')
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../pixellab/safezone'); import hook as _hk
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import acv_gloss
# hfg4: soft-fade one-line hook (no box, prompt line cut), panels full width edge to edge, timer bar on the seam
HOOK, HB = _hk.hook_fade(['FIND 3 DIFFERENCES'], accent=0, color=(255, 214, 60), size=64, y=280, fade_to=420)
print('hook bottom', HB)
from PIL import ImageOps
SC_ = 1080 / 1920; CX0, CY0 = 0, 0
PW = W; PHF = round(1080 * SC_); PH1 = round(930 * SC_)        # bottom panel shows the whole scene (608), top panel stops under the floor seal (523)
PX = 0; PY1 = 430; SEAM = 44; PY2 = PY1 + PH1 + SEAM; PH = PHF
CROP = (0, 0, 1920, 1080)
KS = 4                                                       # guides/gummies/slime 3x -> 4x (panel scale 0.443 -> 0.5625)
def P(sx, sy): return (sx - CX0) * SC_, (sy - CY0) * SC_
import numpy as np
def crest(fr):
    box = (820, 20, 1110, 126); im = fr.crop(box); a = np.array(im).astype(int)
    lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11; m = (lum < 185) & ((a[..., 0] - a[..., 2]) > 70)
    g = np.array(ImageOps.colorize(ImageOps.grayscale(im), (40, 50, 80), (215, 230, 255)))
    out = a.copy(); out[m] = g[m]; fr = fr.copy(); fr.paste(Image.fromarray(out.astype('uint8')), box[:2]); return fr
src = Image.open(A + 'sun_hd.gif'); PAN = []; PANB = []
for i in range(0, src.n_frames, 2):
    src.seek(i); fr = src.convert('RGB')
    PAN.append(fr.crop(CROP).resize((PW, PHF), Image.NEAREST).convert('RGBA'))
    PANB.append(crest(fr).crop(CROP).resize((PW, PHF), Image.NEAREST).convert('RGBA'))
def _back(top_row, floor):
    # sky above the top panel: the panel's own top row, darkening toward the frame top (under the hook);
    # under the bottom panel: its lower floor + ornate band mirrored, darkening into the caption area
    B = Image.new('RGBA', (W, H), (12, 8, 16, 255))
    row = np.array(top_row.convert('RGB')).astype(float)[0]
    sky = np.zeros((PY1, W, 3))
    for y in range(PY1):
        u = (y / PY1) ** 1.6; sky[y] = row * u + np.array([14, 10, 30]) * (1 - u)
    B.paste(Image.fromarray(sky.astype('uint8')).convert('RGBA'), (0, 0))
    yb = PY2 + PHF; need = H - yb
    m = floor.transpose(Image.FLIP_TOP_BOTTOM); tiles = [m, floor]; y = yb; k = 0
    while y < H: B.paste(tiles[k % 2], (0, y)); y += floor.height; k += 1
    g = Image.new('L', (1, need), 0)
    for yy in range(need): g.putpixel((0, yy), int(80 + 140 * yy / need))
    sh = Image.new('RGBA', (W, need), (12, 8, 16, 255)); sh.putalpha(g.resize((W, need))); B.alpha_composite(sh, (0, yb))
    return B
CY = idle('cyrus', KS); JO = idle('joy', KS)
SL = seq(PL + 'race/slime_idle_c', KS, 1)
G_M = gummy('mush', KS); G_A = up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), KS); G_G = gummy('gold', KS)
def silver(im):
    g = ImageOps.grayscale(im.convert('RGB')); return ImageOps.colorize(g, (40, 50, 80), (215, 230, 255)).convert('RGBA')
def panel(t, bottom):
    p = (PANB if bottom else PAN)[int(t * 6) % len(PAN)].copy()
    # gummy on the stairs
    g = G_A if bottom else G_M; bob = int(3 * math.sin(t * 4))
    x_, y_ = P(944, 587); p.alpha_composite(g, (int(x_) - g.width // 2, int(y_) - g.height + bob))
    # gold gummy shrine glow on the floor seal (same in both)
    x_, y_ = P(960, 750); p.alpha_composite(G_G, (int(x_) - G_G.width // 2, int(y_) - G_G.height // 2 + int(2 * math.sin(t * 3))))
    # guides
    x_, y_ = P(420, 880); cy = CY[int(t * 8) % len(CY)]; p.alpha_composite(cy, (int(x_) - cy.width // 2, int(y_) - 78 * KS))
    x_, y_ = P(730, 890); jo = JO[int(t * 8 + 3) % len(JO)]; p.alpha_composite(jo, (int(x_) - jo.width // 2, int(y_) - 78 * KS))
    if not bottom:
        x_, y_ = P(1349, 884); s = SL[int(t * 10) % len(SL)]; p.alpha_composite(s, (int(x_) - s.width // 2, int(y_) - s.height + 27))
    return p
TL, HOLD, PRE = 8.0, 1.5, 0.3; TE = TL + HOLD + PRE; NF = int(TE * FPS); wr = Writer('v41_noaudio.mp4'); ev = []
DIG = {}
def digit_img(n, sz):
    k = (n, sz)
    if k not in DIG:
        f_ = F(sz); L = Image.new('RGBA', (sz + 40, sz + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.text((20, 20), str(n), font=f_, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(20, 12, 8, 255)); DIG[k] = L
    return DIG[k]
BX0, BX1 = 186, 1004; BY0 = PY1 + PH1 + (SEAM - 30) // 2; BY1 = BY0 + 30
DIGX = 112
for f in range(NF):
    t = f / FPS
    loop = t >= TE - PRE - 1e-6
    tl = t - TE if loop else t      # last 0.3s: card gone, timer refills (flows into frame 0)
    tp = 0.0 if loop else t         # panels show the opening state
    p1 = panel(tp, False); p2 = panel(tp, True)
    img = _back(p1.crop((0, 0, W, 1)), PANB[int(tp * 6) % len(PAN)].crop((0, PHF - 150, W, PHF)))   # floor from the bare scene (no characters)
    img.alpha_composite(p1.crop((0, 0, W, PH1)), (0, PY1)); img.alpha_composite(p2, (0, PY2))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if loop: rem = min(1, (tl + PRE) / PRE)
    else: rem = max(0.0, 1 - t / TL)
    d.rounded_rectangle([BX0 - 6, BY0 - 6, BX1 + 6, BY1 + 6], 14, fill=(20, 10, 4, 220), outline=(255, 214, 60, 255), width=4)
    if rem > 0:
        col = (120, 220, 90) if (rem > 0.5 or loop) else ((255, 200, 60) if rem > 0.25 else (255, 90, 70))
        d.rounded_rectangle([BX0, BY0, BX0 + int((BX1 - BX0) * rem), BY1], 10, fill=col + (255,))
    img.alpha_composite(L)
    items = []
    if loop or t < TL:
        if loop: n = int(TL); sc = 1.3 * min(1, (tl + PRE) / PRE)
        else:
            n = int(math.ceil(TL - t)) if t > 0 else int(TL); ph = (t % 1.0)
            sc = 1.3 - 0.3 * min(1, ph / 0.2)      # each new second pops in big and settles
        if sc > 0.05:
            sz = 72; di = digit_img(n, sz); w_ = max(1, int(di.width * sc)); di2 = di.resize((w_, w_), Image.NEAREST)
            red = (not loop) and TL - t <= 2.0
            if red:
                di2 = di2.copy(); a_ = np.array(di2); m = (a_[..., 0] > 200) & (a_[..., 1] > 200); a_[m, 1] = 110; a_[m, 2] = 90; di2 = Image.fromarray(a_)
            img.alpha_composite(di2, (int(DIGX - w_ / 2), int((BY0 + BY1) / 2 - w_ / 2 - 4)))
    else:
        u = t - TL; a = int(255 * min(1, u / 0.15)); pop = 1.2 - 0.2 * min(1, u / 0.15)
        items += [(W / 2, (BY0 + BY1) / 2 - 42 - int((pop - 1) * 50), "TIME'S UP!", int(84 * pop), (255, 214, 60), 10, a)]   # unboxed stamp on the seam, no comment line
    text_layer(img, items)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 150, 255, 285): img.convert('RGB').save(f'p_{f:04d}.png')
wr.close()
for s_ in (5, 6, 7): ev.append((float(s_), 'tick_8bit'))   # ticks only in the last 3s (no metronome through the reel)
ev.append((TL, 'buzz_8bit'))
json.dump({'events': ev}, open('v41_ev.json', 'w')); print('done')
