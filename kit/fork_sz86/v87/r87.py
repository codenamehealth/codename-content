import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #87 Pause when all 3 gummies fit: safe zone + hook only (source fork_a9/vault/render_vault.py)
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
def fitsize(g, m=19):
    s = m / max(g.size); return g.resize((max(1, round(g.width * s)), max(1, round(g.height * s))), Image.NEAREST)
GS = {k: fitsize(v) for k, v in GS.items()}
def socket(g):
    a = g.getchannel('A'); hole = Image.new('RGBA', g.size, (25, 14, 8, 255)); hole.putalpha(a)
    rim = Image.new('RGBA', (g.width + 2, g.height + 2), (0, 0, 0, 0))
    big = a.resize((g.width + 2, g.height + 2), Image.NEAREST); rim.paste((240, 200, 90, 255), (0, 0), big)
    rim.alpha_composite(hole, (1, 1)); return rim
SOCK = {k: socket(v) for k, v in GS.items()}
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
HOOK, HB = hook_layer(['PAUSE WHEN ALL', '3 GUMMIES FIT'], accent=1)
HOOK2, HB2 = hook_layer(['DID YOU', 'GET IT?'], accent=1)
HUD0 = max(HB, HB2) + 14; HUD1 = HUD0 + 58
ANCH = HUD1 + 56                                                  # tether anchors / name plates
VX = 560 - VAULT.width // 2; VY = 1495 - VAULT.height
print('hook', HB, HB2, 'hud', HUD0, HUD1, 'anchor', ANCH, 'dial ring', DY - RR, DY + RR, 'x', XS[0] - RR, XS[2] + RR, 'vault', VX, VY, VAULT.size)
wr = Writer('v87_noaudio.mp4'); ev = []; T_END = 7.2; DUR = 9.0
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
            d.rounded_rectangle([cx - 132, ANCH - 18, cx + 132, ANCH + 30], 10, fill=(14, 10, 24, 220), outline=COL[k] + (255,), width=4)
        layer(img, teth)
        img.alpha_composite(g, (cx - g.width // 2, gy - g.height // 2))
        text_layer(img, [(cx, ANCH - 6, NAME[k], 24, LCOL[k], 5, 255)])
    fits.append(max(errs))
    ms = min(t, T_END)
    layer(img, lambda d: (d.rounded_rectangle([78, HUD0, 330, HUD1], 10, fill=(180, 40, 40, 235)), d.rounded_rectangle([W - 340, HUD0, W - 62, HUD1], 10, fill=(20, 14, 30, 235), outline=(255, 214, 60, 255), width=3)))
    tx = [(204, HUD0 + 16, '99% FAIL', 26, (255, 255, 255), 0, 255), (W - 201, HUD0 + 15, f'00:{int(ms):02d}.{int((ms % 1) * 100):02d}', 28, (255, 214, 60), 0, 255)]
    if t < T_END: tx.append((530, HUD0 + 13, 'PAUSE IT!', 32, (255, 255, 255), 6, 255))
    text_layer(img, tx)
    if t >= T_END:
        if not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
        layer(img, lambda d: d.rounded_rectangle([140, 1124, 816, 1206], 16, fill=(14, 10, 24, 235), outline=(255, 214, 60, 255), width=5))
        text_layer(img, [(478, 1147, 'COMMENT YOUR TIME', 36, (255, 255, 255), 6, 255)])
    if f < T_END * FPS and f % 6 == 0: ev.append((round(t, 3), 'reeltick_8bit'))
    img.alpha_composite(HOOK if t < T_END else HOOK2)
    wr.write(img)
    if f in (FSTAR, 250): img.convert('RGB').save(f'f87_{f}.png')
wr.close()
print('frames within 8deg:', [i for i, e in enumerate(fits[:int(T_END * FPS)]) if e < 8], 'fstar err', fits[FSTAR])
json.dump(ev, open('v87_ev.json', 'w')); print('done')
