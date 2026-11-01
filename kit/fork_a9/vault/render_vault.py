import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PS = json.load(open('dials.json')); FSTAR = 176; N = 240
def ang(p, f):
    t = (f - FSTAR) / FPS; w, A, nu, ph = p
    return w * t + A * (math.sin(nu * t + ph) - math.sin(ph))
DIAL = crop(Image.open('../gen/dial/01.png').convert('RGBA'))
DR = DIAL.width // 2; SOCK_R = 21; K = 4
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
    # socket sits on the 12 o'clock rim of the unrotated dial
    d.alpha_composite(s, (DR - s.width // 2, DR - SOCK_R - s.height // 2))
    r = d.rotate(-a_deg, resample=Image.NEAREST)
    return up(r, K)
VAULT = up(crop(Image.open('../gen/vault/01.png').convert('RGBA')), 6)
BGF = bg_frames('bg_castle.gif', (W, H), box=None, step=2, bright=0.35, blur=4) if os.path.exists(A + 'bg_castle.gif') else None
GUM3 = {k: up(GS[k], K) for k in KINDS}
XS = [188, 540, 892]; DY = 1430
COL = {'acv': (74, 124, 58), 'mush': (217, 122, 31), 'mel': (107, 45, 107)}
NAME = {'acv': 'FOUNDATION', 'mush': 'ENERGY', 'mel': 'RECOVERY'}
HOL = idle('hollow', 3)
wr = Writer('vault_noaudio.mp4'); ev = []; T_END = 7.2; DUR = 9.0
fits = []
for f in range(int(DUR * FPS)):
    t = f / FPS; fc = min(f, int(T_END * FPS))
    img = BGF[int(t * 6) % len(BGF)].copy()
    img.alpha_composite(VAULT, ((W - VAULT.width) // 2, 330))
    layer(img, lambda d: d.rectangle([0, 1080, W, H], fill=(10, 6, 18, 150)))
    errs = []
    for i, k in enumerate(KINDS):
        a = ang(PS[i], fc); errs.append(abs((a + 180) % 360 - 180))
        di = dial_img(k, a); cx = XS[i]
        def ring(d, cx=cx, k=k):
            d.ellipse([cx - DR * K - 14, DY - DR * K - 14, cx + DR * K + 14, DY + DR * K + 14], fill=(0, 0, 0, 120), outline=COL[k] + (255,), width=6)
        layer(img, ring)
        img.alpha_composite(di, (cx - di.width // 2, DY - di.height // 2))
        g = GUM3[k]; gy = DY - SOCK_R * K
        # magic tether from the top
        layer(img, lambda d, cx=cx, gy=gy, k=k: (d.line([cx, 1130, cx, gy - g.height // 2], fill=COL[k] + (120,), width=6), d.ellipse([cx - 12, 1118, cx + 12, 1142], fill=(255, 230, 150, 220))))
        img.alpha_composite(g, (cx - g.width // 2, gy - g.height // 2))
        text_layer(img, [(cx, DY + DR * K + 30, NAME[k], 24, COL[k], 5, 255)])
    fits.append(max(errs))
    # header + hud
    layer(img, lambda d: d.rectangle([0, 0, W, 310], fill=(10, 6, 18, 200)))
    text_layer(img, [(W / 2, 60, 'PAUSE WHEN ALL 3', 62, (255, 255, 255), 8, 255), (W / 2, 150, 'GUMMIES FIT', 62, (255, 214, 60), 8, 255)])
    ms = min(t, T_END)
    layer(img, lambda d: (d.rounded_rectangle([40, 232, 270, 290], 10, fill=(180, 40, 40, 230)), d.rounded_rectangle([W - 320, 232, W - 40, 290], 10, fill=(20, 14, 30, 230), outline=(255, 214, 60, 255), width=3)))
    text_layer(img, [(155, 247, '99% FAIL', 24, (255, 255, 255), 0, 255), (W - 180, 247, f'00:{int(ms):02d}.{int((ms % 1) * 100):02d}', 26, (255, 214, 60), 0, 255)])
    hf = HOL[int(t * 6) % len(HOL)]; img.alpha_composite(hf, (-40, H - 290))
    if t < T_END:
        text_layer(img, [(W / 2, H - 170, 'Pause it!', 40, (255, 255, 255), 6, 255)])
    else:
        u = t - T_END
        text_layer(img, [(W / 2, H - 190, 'DID YOU GET IT?', 56, (255, 214, 60), 8, 255), (W / 2, H - 110, 'Comment your time', 32, (255, 255, 255), 5, 255)])
        if not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
    if f < T_END * FPS and f % 6 == 0: ev.append((round(t, 3), 'reeltick_8bit'))
    wr.write(img)
    if f in (FSTAR - 1, FSTAR, FSTAR + 1): img.convert('RGB').crop((0, 1100, W, 1650)).save(f'fit_{f - FSTAR:+d}.png')
wr.close()
print('frames within 8deg:', [i for i, e in enumerate(fits[:int(T_END * FPS)]) if e < 8], 'fstar err', fits[FSTAR])
json.dump(ev, open('vault_ev.json', 'w')); print('done')
