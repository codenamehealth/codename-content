import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
import hook as HK
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
from PIL import ImageFilter
# #87 Pause when all 3 gummies fit: rc10 review recut (source fork_sz86/v87/r87.py). Bennett loves it: legibility + universal fixes only.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
GEN = SP0 + 'fork_a9/gen/'
PS = json.load(open('dials.json')); FSTAR = 176
def ang(p, f):
    t = (f - FSTAR) / FPS; w, A_, nu, ph = p
    return w * t + A_ * (math.sin(nu * t + ph) - math.sin(ph))
DIAL = crop(Image.open(GEN + 'dial/01.png').convert('RGBA'))
DR = DIAL.width // 2; SOCK_R = 21; K = 4                         # dials unchanged 4x
KINDS = ['acv', 'mush', 'mel']
GS = {k: crop(Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')) for k in KINDS}
GS['acv'] = crop(acv_gummy_strong())   # rc10: Syeda's ACV gummy + gummy shine (same alpha, so the socket shape is unchanged)
def fitsize(g, m=19):
    s = m / max(g.size); return g.resize((max(1, round(g.width * s)), max(1, round(g.height * s))), Image.NEAREST)
GS = {k: fitsize(v) for k, v in GS.items()}
LCOL0 = {'acv': (150, 235, 110), 'mush': (255, 170, 60), 'mel': (215, 150, 255)}
def socket(g, col):
    a = g.getchannel('A'); hole = Image.new('RGBA', g.size, (25, 14, 8, 255)); hole.putalpha(a)
    pa = Image.new('L', (g.width + 4, g.height + 4), 0); pa.paste(a, (2, 2))
    dil = pa.filter(ImageFilter.MaxFilter(5))                     # rc10: 2px rim (8px at 4x) in the dial's colour
    rim = Image.new('RGBA', pa.size, (0, 0, 0, 0)); rim.paste(col + (255,), (0, 0), dil)
    rim.alpha_composite(hole, (2, 2)); return rim
SOCK = {k: socket(v, LCOL0[k]) for k, v in GS.items()}
def dial_img(k, a_deg):
    d = DIAL.copy(); s = SOCK[k]
    d.alpha_composite(s, (DR - s.width // 2, DR - SOCK_R - s.height // 2))
    return up(d.rotate(-a_deg, resample=Image.NEAREST), K)
VAULT = up(crop(Image.open(GEN + 'vault/01.png').convert('RGBA')), 3)    # backdrop prop 6x -> 3x, moved under the dials
BGF = bg_frames('bg_castle.gif', (W, H), box=None, step=2, bright=0.35, blur=4)
GUM3 = {k: up(GS[k], K) for k in KINDS}
RR = DR * K + 8
XS = [220, 545, 870]; DY = 955                                    # dial row above y1110 (right dial clear of the lower buttons)
COL = {'acv': (74, 124, 58), 'mush': (217, 122, 31), 'mel': (107, 45, 107)}
LCOL = {'acv': (130, 210, 100), 'mush': (255, 160, 60), 'mel': (200, 130, 240)}
NAME = {'acv': 'FOUNDATION', 'mush': 'ENERGY', 'mel': 'RECOVERY'}
HOL = idle('hollow', 3)                                           # unchanged 3x
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
# rc10: comment prompt from frame 0 as a 46px second line inside the hook band (the 36px end-only card is gone)
HOOK, HB = band(['PAUSE WHEN ALL', '3 GUMMIES FIT'], 1, 'COMMENT YOUR TIME', subcol=(255, 255, 255))
HOOK2, HB2 = band(['DID YOU', 'GET IT?'], 1, 'COMMENT YOUR TIME', subcol=(255, 255, 255))
HUD0 = max(HB, HB2) + 12; HUD1 = HUD0 + 84                        # rc10: taller HUD row for the big timer
ANCH = HUD1 + 40                                                  # tether anchors
VX = 560 - VAULT.width // 2; VY = 1495 - VAULT.height
print('hook', HB, HB2, 'hud', HUD0, HUD1, 'anchor', ANCH, 'dial ring', DY - RR, DY + RR, 'x', XS[0] - RR, XS[2] + RR, 'vault', VX, VY, VAULT.size)
wr = Writer('v87_noaudio.mp4'); ev = []; T_END = 7.2; DUR = 8.7   # rc10: end hold 1.8s -> 1.5s, then loops to frame 0
fits = []
for f in range(int(DUR * FPS)):
    t = f / FPS; fc = min(f, int(T_END * FPS))
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: d.rectangle([0, HUD1 + 20, W, H], fill=(10, 6, 18, 110)))
    img.alpha_composite(VAULT, (VX, VY))
    hf = HOL[int(t * 6) % len(HOL)]; img.alpha_composite(hf, (VX - 200, 1495 - 78 * 3))   # Hollow watching beside the vault, feet on the floor
    errs = []
    for i, k in enumerate(KINDS):
        a = ang(PS[i], fc); errs.append(abs((a + 180) % 360 - 180))
        di = dial_img(k, a); cx = XS[i]
        layer(img, lambda d, cx=cx, k=k: d.ellipse([cx - RR, DY - RR, cx + RR, DY + RR], fill=(0, 0, 0, 130), outline=COL[k] + (255,), width=6))
        img.alpha_composite(di, (cx - di.width // 2, DY - di.height // 2))
        g = GUM3[k]; gy = DY - SOCK_R * K
        def teth(d, cx=cx, gy=gy, k=k, g=g):
            d.line([cx, ANCH + 30, cx, gy - g.height // 2], fill=COL[k] + (150,), width=6)
            d.rounded_rectangle([cx - 46, ANCH + 14, cx + 46, ANCH + 34], 8, fill=COL[k] + (255,), outline=LCOL[k] + (255,), width=3)   # rc10: plain anchor (the 24px guild names are cut)
        layer(img, teth)
        img.alpha_composite(g, (cx - g.width // 2, gy - g.height // 2))
    fits.append(max(errs))
    ms = min(t, T_END)
    # rc10: PAUSE IT! cut; 99% FAIL 26 -> 44px; timer 28 -> 60px (its own big plate, the number people comment)
    layer(img, lambda d: (d.rounded_rectangle([78, HUD0, 438, HUD1], 12, fill=(180, 40, 40, 240)), d.rounded_rectangle([462, HUD0, 1017, HUD1], 12, fill=(20, 14, 30, 240), outline=(255, 214, 60, 255), width=4)))
    tx = [(258, HUD0 + 20, '99% FAIL', 44, (255, 255, 255), 6, 255), (740, HUD0 + 12, f'00:{int(ms):02d}.{int((ms % 1) * 100):02d}', 60, (255, 214, 60), 8, 255)]
    if t < 1.6: tx.append((275, ANCH, 'ACV GUMMY', 44, (150, 235, 110), 6, 255))   # rc10: ACV label on first appearance
    if t < 1.6: layer(img, lambda d: d.rounded_rectangle([70, ANCH - 14, 480, ANCH + 58], 12, fill=(14, 10, 24, 225), outline=(150, 235, 110, 255), width=4))
    text_layer(img, tx)
    if t >= T_END and not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK if t < T_END else HOOK2)
    wr.write(img)
    if f in (0, 20, FSTAR, 250, int(DUR * FPS) - 1): img.convert('RGB').save(f'f87_{f}.png')
wr.close()
print('frames within 8deg:', [i for i, e in enumerate(fits[:int(T_END * FPS)]) if e < 8], 'fstar err', fits[FSTAR])
json.dump({'events': ev}, open('v87_ev.json', 'w')); print('done')
