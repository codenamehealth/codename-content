"""r033 review recut (fork_rc14). From fork_c3/v33/r33.py.
Changes: 'TAG HER BELOW' as a 48px band line from frame 0 (replaces the small WHICH GUIDE SHE'S CHOOSING sub);
cards 2.0s -> 1.7s each (still once each, still much slower than the original 0.8s), full edge-on swing on every card;
card text >=44px (guild, product), ACV gummy gloss + 'ACV GUMMY' label; end grid guides 236 -> 260px, names 30 -> 44px,
selector cursor hops Joy > Cleo > Rayleigh > Cyrus > Joy during a 1.9s hold, then the loop cuts into Joy's card flipping in."""
import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
sys.path.insert(0, R + 'fork_rc2'); from rc2 import hook_layer2, acv_gloss
CARD_T = 1.7; END_T = 1.9
W, H, FPS = 1080, 1920, 30; DUR = 4 * CARD_T + END_T; N = int(round(DUR * FPS))
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255, sc=(20, 15, 35)):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=sc + (a,))
vg = Image.open(A + 'vit_hd.gif'); BG = []
for i in range(0, vg.n_frames, 2):
    vg.seek(i); f = vg.convert('RGB'); s = H / 1080; cw = int(W / s)
    f = f.crop((960 - cw // 2, 0, 960 + cw // 2, 1080)).resize((W, H), Image.NEAREST)
    BG.append(ImageEnhance.Brightness(f.filter(ImageFilter.GaussianBlur(3))).enhance(0.55).convert('RGBA'))
CARD = up(Image.open(R + 'fork_a3/parch/03.png').convert('RGBA').crop(Image.open(R + 'fork_a3/parch/03.png').getbbox()), 7)
CW, CHh = CARD.size; CX, CY = W // 2, 1016; print('card', CARD.size)
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
G = [('JOY', 'FOUNDATION', 'ACV GUMMY', (74, 124, 58), 'idle_0.gif', 'acv'), ('CLEO', 'VITALITY', 'CREATINE', (46, 93, 168), 'idle_3.gif', 'cre'),
     ('CYRUS', 'ENERGY', 'MUSHROOM', (217, 122, 31), 'idle_1.gif', 'mush'), ('RAYLEIGH', 'RECOVERY', 'MELATONIN', (107, 45, 107), 'idle_2.gif', 'mel')]
IDL = [gif(g[4], 376) for g in G]; IDS = [gif(g[4], 260) for g in G]
def gsrc(k):
    g0 = Image.open(R + f'pixellab/gummies/pick_{k}.png').convert('RGBA')
    return acv_gloss(g0) if k == 'acv' else g0
GUM = {g[5]: up(gsrc(g[5]), 3) for g in G}
GUMS = {g[5]: up(gsrc(g[5]), 2) for g in G}
def card(i, t):
    # layout inside the parchment: 540px wide between y200-770, 240px between the corners below that
    c = CARD.copy(); d = ImageDraw.Draw(c); name, guild, prod, col, _, gk = G[i]
    ctext(d, CW / 2, 212, guild, F(44), col, 0)
    d.line([CW / 2 - 200, 266, CW / 2 + 200, 266], fill=col, width=5)
    fr = IDL[i][int(t * 8) % len(IDL[i])]; c.alpha_composite(fr, (int(CW / 2 - fr.width / 2), 280))
    d = ImageDraw.Draw(c)
    ctext(d, CW / 2, 664, name, F(50), (60, 40, 25), 0)
    ctext(d, CW / 2, 728, prod, F(44), col, 0)
    g = GUM[gk]; c.alpha_composite(g, (int(CW / 2 - g.width / 2), 790))
    return c
SEQ = []; tt = 0.0
for k in range(4): SEQ.append((tt, tt + CARD_T, k)); tt += CARD_T
T_END = tt
rng = random.Random(1); SP = [(rng.uniform(0, W), rng.uniform(450, 1700), rng.uniform(0, 6.3)) for _ in range(36)]
HOOK, HB = hook_layer2(['If you know her', 'you know'], accent=1, sub='Tag her below'); print('hook bottom', HB)
# end grid geometry
PX0, PY0, PX1, PY1 = 80, 552, 880, 1490
CELLX = (280, 680); FEET = (906, 1316)
ORDER = [0, 1, 3, 2, 0]; HOPS = [0.5, 0.8, 1.1, 1.4, 1.65]       # Joy > Cleo > Rayleigh > Cyrus > Joy (lands on Joy for the loop)
def cell_box(i):
    x = CELLX[i % 2]; yb = FEET[i // 2]
    return (x - 180, yb - 272, x + 180, yb + 128)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v33_noaudio.mp4'], stdin=subprocess.PIPE)
events = []
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 6, y + 6], fill=(255, 235, 170, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SP])
    if t < T_END - 1e-6:
        s0, s1, i = next(s for s in SEQ if s[0] <= t + 1e-6 < s[1])
        c = card(i, t)
        a_in = min(1, (t - s0) / 0.24); a_out = min(1, (s1 - t) / 0.18)
        fx = 0.1 + 0.9 * (1 - (1 - min(a_in, a_out)) ** 2)      # full edge-on swing in, hold, swing out (every card)
        if f == round(s0 * FPS): events.append((round(s0, 3), 'swish'))
        w = max(2, int(CW * fx)); ci = c.resize((w, CHh), Image.NEAREST)
        layer(img, lambda d: d.ellipse([CX - 300, CY + CHh // 2 - 20, CX + 300, CY + CHh // 2 + 40], fill=(0, 0, 0, 90)))
        bob = int(round(3 * math.sin((t - s0) * 3.2)))
        img.alpha_composite(ci, (CX - w // 2, CY - CHh // 2 + bob))
        if t - s0 < 0.5:      # sparkle burst as each card lands
            uu = (t - s0) / 0.5
            layer(img, lambda d: [d.rectangle([CX + math.cos(k * 0.785) * (200 + 260 * uu) - 8, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) - 8,
                                               CX + math.cos(k * 0.785) * (200 + 260 * uu) + 8, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) + 8],
                                              fill=G[i][3] + (int(255 * (1 - uu)),)) for k in range(8)])
    else:
        u = t - T_END
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(T_END, 3), 'ding_8bit'))
        layer(img, lambda d: d.rounded_rectangle([PX0, PY0, PX1, PY1], 30, fill=(245, 230, 200, 238), outline=(200, 160, 80, 255), width=8))
        # selector cursor (JRPG style): glowing cell frame + pointer arrow, hops across the four guides and lands on Joy
        if u >= HOPS[0]:
            ci_ = ORDER[max(k for k in range(len(HOPS)) if u >= HOPS[k])]
            bx0, by0, bx1, by1 = cell_box(ci_); pulse = 0.5 + 0.5 * math.sin(u * 14)
            def cur(d):
                d.rounded_rectangle([bx0, by0, bx1, by1], 22, fill=(255, 214, 60, 60), outline=(255, 190, 40, 255), width=7)
                ax = bx0 + 8 + int(6 * pulse); ay = by0 + 150
                d.polygon([(ax, ay - 26), (ax + 34, ay), (ax, ay + 26)], fill=(255, 214, 60, 255), outline=(60, 35, 10, 255))
            layer(img, cur)
        d = ImageDraw.Draw(img)
        for i in range(4):
            x = CELLX[i % 2]; yb = FEET[i // 2]; pop = min(1, max(0, (u - i * 0.08) / 0.2))
            fr = IDS[i][int(t * 8) % len(IDS[i])]
            if pop > 0:
                fr2 = fr.resize((max(1, int(fr.width * pop)), max(1, int(fr.height * pop))), Image.NEAREST)
                img.alpha_composite(fr2, (int(x - fr2.width / 2), int(yb - fr2.height)))
                g = GUMS[G[i][5]]; img.alpha_composite(g, (int(x - g.width / 2), yb + 6))
                d = ImageDraw.Draw(img); ctext(d, x, yb + 76, G[i][0], F(44), G[i][3], 0)
        ctext(d, (PX0 + PX1) / 2, 580, 'Which one is she?', F(44), (60, 40, 25), 0)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v33_events.json', 'w')); print('done', T_END, DUR, N)
