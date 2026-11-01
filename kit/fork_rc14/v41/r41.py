import sys; sys.path.insert(0, '../../fork1')
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../pixellab/safezone'); import hook as _hk
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import hook_layer2, acv_gloss
_f0 = _hk._fit; _hk._fit = lambda lines, maxw, hi=80, lo=48: _f0(lines, maxw, min(hi, 64), lo)   # 64px main lines so the band can carry the prompt
import hook2 as _h2; _h2._fit = _hk._fit
HOOK, HB = _h2.hook_layer2(['FIND 3', 'DIFFERENCES'], accent=1, sub='Comment 0, 1, 2 or 3', sub_max=48)
print('hook bottom', HB)
from PIL import ImageOps
PH = 412; PW = 717; PX = 125; TROW = HB + 8; PY1 = TROW + 96; PY2 = PY1 + PH + 20   # panels 780x448 -> 717x412 (8%) to fit the prompt line + bigger countdown; guides/gummies/slime stay 3x
CX0, CY0 = 150, 0; SC_ = PW / 1620; CROP = (CX0, CY0, CX0 + 1620, CY0 + round(PH / SC_))
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
    PAN.append(fr.crop(CROP).resize((PW, PH), Image.NEAREST).convert('RGBA'))
    PANB.append(crest(fr).crop(CROP).resize((PW, PH), Image.NEAREST).convert('RGBA'))
BGF = bg_frames('sun_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=4, bright=0.55, blur=6)
CY = idle('cyrus', 3); JO = idle('joy', 3)
SL = seq(PL + 'race/slime_idle_c', 3, 1)
G_M = gummy('mush', 3); G_A = up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), 3); G_G = gummy('gold', 3)
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
    x_, y_ = P(420, 880); cy = CY[int(t * 8) % len(CY)]; p.alpha_composite(cy, (int(x_) - cy.width // 2, int(y_) - 78 * 3))
    x_, y_ = P(730, 890); jo = JO[int(t * 8 + 3) % len(JO)]; p.alpha_composite(jo, (int(x_) - jo.width // 2, int(y_) - 78 * 3))
    if not bottom:
        x_, y_ = P(1349, 884); s = SL[int(t * 10) % len(SL)]; p.alpha_composite(s, (int(x_) - s.width // 2, int(y_) - s.height + 20))
    return p
TL, HOLD, PRE = 8.0, 1.5, 0.3; TE = TL + HOLD + PRE; NF = int(TE * FPS); wr = Writer('v41_noaudio.mp4'); ev = []
DIG = {}
def digit_img(n, sz):
    k = (n, sz)
    if k not in DIG:
        f_ = F(sz); L = Image.new('RGBA', (sz + 40, sz + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.text((20, 20), str(n), font=f_, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(20, 12, 8, 255)); DIG[k] = L
    return DIG[k]
BX0, BX1 = PX, PX + PW; BY0 = TROW + 30; BY1 = BY0 + 36
for f in range(NF):
    t = f / FPS
    loop = t >= TE - PRE - 1e-6
    tl = t - TE if loop else t      # last 0.3s: card gone, timer refills (flows into frame 0)
    tp = 0.0 if loop else t         # panels show the opening state
    img = BGF[int(tp * 3) % len(BGF)].copy()
    def frame_layer(d):
        for py in (PY1, PY2):
            d.rectangle([PX - 12, py - 12, PX + PW + 12, py + PH + 12], fill=(40, 22, 8, 255))
            d.rectangle([PX - 8, py - 8, PX + PW + 8, py + PH + 8], outline=(255, 214, 60, 255), width=6)
    layer(img, frame_layer)
    img.alpha_composite(panel(tp, False), (PX, PY1)); img.alpha_composite(panel(tp, True), (PX, PY2))
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
            img.alpha_composite(di2, (int(W / 2 - PX / 2 + PX / 2 - w_ / 2 + (BX0 + BX1) / 2 - W / 2), int((BY0 + BY1) / 2 - w_ / 2 - 4)))
    else:
        u = t - TL; a = int(255 * min(1, u / 0.15)); pop = 1.2 - 0.2 * min(1, u / 0.15)
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L2).rounded_rectangle([76, 900, 1004, 1124], 30, fill=(20, 12, 30, int(232 * a / 255)), outline=(255, 214, 60, a), width=6)
        img.alpha_composite(L2)
        items += [(W / 2, 930 - int((pop - 1) * 40), "TIME'S UP!", int(72 * pop), (255, 214, 60), 9, a), (W / 2, 1040, 'Comment 0, 1, 2 or 3', 44, (120, 230, 110), 6, a)]
    text_layer(img, items)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 150, 285): img.convert('RGB').save(f'p_{f:04d}.png')
wr.close()
for s_ in (5, 6, 7): ev.append((float(s_), 'tick_8bit'))   # ticks only in the last 3s (no metronome through the reel)
ev.append((TL, 'buzz_8bit'))
json.dump({'events': ev}, open('v41_ev.json', 'w')); print('done')
