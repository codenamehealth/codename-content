import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS, DUR = 1080, 1920, 30, 10.6; N = int(DUR * FPS)
def F(s): return ImageFont.truetype(FONT, s)
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
CW, CHh = CARD.size; CX, CY = W // 2, 1014; print('card', CARD.size)
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
G = [('JOY', 'FOUNDATION', 'ACV', (74, 124, 58), 'idle_0.gif', 'acv'), ('CLEO', 'VITALITY', 'CREATINE', (46, 93, 168), 'idle_3.gif', 'cre'),
     ('CYRUS', 'ENERGY', 'MUSHROOM', (217, 122, 31), 'idle_1.gif', 'mush'), ('RAYLEIGH', 'RECOVERY', 'MELATONIN', (107, 45, 107), 'idle_2.gif', 'mel')]
IDL = [gif(g[4], 376) for g in G]; IDS = [gif(g[4], 236) for g in G]
GUM = {g[5]: up(Image.open(R + f'pixellab/gummies/pick_{g[5]}.png').convert('RGBA'), 3) for g in G}
GUMS = {g[5]: up(Image.open(R + f'pixellab/gummies/pick_{g[5]}.png').convert('RGBA'), 2) for g in G}
def card(i, t):
    c = CARD.copy(); d = ImageDraw.Draw(c); name, guild, prod, col, _, gk = G[i]
    ctext(d, CW / 2, 128, guild, F(32), col, 0)
    d.line([CW / 2 - 160, 174, CW / 2 + 160, 174], fill=col, width=4)
    fr = IDL[i][int(t * 8) % len(IDL[i])]; c.alpha_composite(fr, (int(CW / 2 - fr.width / 2), 206))
    ctext(d, CW / 2, 604, name, F(46), (60, 40, 25), 0)
    g = GUM[gk]; tw = d.textlength(prod, font=F(28)); x0 = CW / 2 - (g.width + 20 + tw) / 2
    c.alpha_composite(g, (int(x0), 690)); d = ImageDraw.Draw(c); d.text((x0 + g.width + 20, 690 + g.height / 2 - 14), prod, font=F(28), fill=col)
    return c
def mystery(t):
    c = CARD.copy(); d = ImageDraw.Draw(c)
    lines = ['Think of her.', '', 'Ready?']
    for k, l in enumerate(lines): ctext(d, CW / 2, 260 + k * 64, l, F(30), (60, 40, 25), 0)
    ctext(d, CW / 2, 560, '?', F(int(120 + 10 * math.sin(t * 6))), (150, 110, 60), 0)
    return c
T0 = 0.0; SEQ = []; tt = T0; durs = [2.0, 2.0, 2.0, 2.0]   # Bennett: each guide only once, slower (was 3 rounds 0.8/0.6/0.45s after a 2.4s static intro card)
for k, dd in enumerate(durs): SEQ.append((tt, tt + dd, k % 4)); tt += dd
T_END = tt
rng = random.Random(1); SP = [(rng.uniform(0, W), rng.uniform(450, 1700), rng.uniform(0, 6.3)) for _ in range(36)]
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['If you know her', 'you know'], accent=1, sub="WHICH GUIDE SHE'S CHOOSING"); print('hook bottom', HB)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v33_noaudio.mp4'], stdin=subprocess.PIPE)
events = []
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 6, y + 6], fill=(255, 235, 170, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SP])
    if t < T_END:
        if t < T0: c = mystery(t); fx = 1.0; cur = None
        else:
            s0, s1, i = next(s for s in SEQ if s[0] <= t < s[1])
            u = (t - s0) / (s1 - s0); c = card(i, t)
            a_in = min(1, (t - s0) / 0.24); a_out = min(1, (s1 - t) / 0.18)
            fx = 0.3 + 0.7 * (1 - (1 - min(a_in, a_out)) ** 2)      # flip in, hold, flip out
            if abs(t - s0) < 0.5 / FPS: events.append((round(s0, 3), 'whoosh_8bit'))
        w = max(2, int(CW * fx)); ci = c.resize((w, CHh), Image.NEAREST)
        layer(img, lambda d: d.ellipse([CX - 300, CY + CHh // 2 - 20, CX + 300, CY + CHh // 2 + 40], fill=(0, 0, 0, 90)))
        bob = int(6 * math.sin(t * 2.6)) if t >= T0 else 0
        img.alpha_composite(ci, (CX - w // 2, CY - CHh // 2 + bob))
        if t >= T0 and t - s0 < 0.5:      # little sparkle burst as each card lands
            uu = (t - s0) / 0.5
            layer(img, lambda d: [d.rectangle([CX + math.cos(k * 0.785) * (200 + 260 * uu) - 7, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) - 7,
                                               CX + math.cos(k * 0.785) * (200 + 260 * uu) + 7, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) + 7],
                                              fill=G[i][3] + (int(255 * (1 - uu)),)) for k in range(8)])
    else:
        u = t - T_END
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(T_END, 3), 'ding_8bit'))
        layer(img, lambda d: d.rounded_rectangle([80, 540, 880, 1490], 30, fill=(245, 230, 200, 235), outline=(200, 160, 80, 255), width=8))
        d = ImageDraw.Draw(img)
        for i in range(4):
            x = (280, 680)[i % 2]; yb = (920, 1290)[i // 2]; pop = min(1, max(0, (u - i * 0.1) / 0.2))
            fr = IDS[i][int(t * 8) % len(IDS[i])]
            if pop > 0:
                fr2 = fr.resize((max(1, int(fr.width * pop)), max(1, int(fr.height * pop))), Image.NEAREST)
                img.alpha_composite(fr2, (int(x - fr2.width / 2), int(yb - fr2.height)))
                d = ImageDraw.Draw(img)
                g = GUMS[G[i][5]]; img.alpha_composite(g, (int(x - g.width / 2), yb + 6))
                d = ImageDraw.Draw(img); ctext(d, x, yb + 80, G[i][0], F(30), G[i][3], 0)
        ctext(d, 480, 588, 'Which one is she?', F(40), (60, 40, 25), 0)
        ctext(d, 480, 1426, 'Tag her below', F(40), (150, 90, 30), 0)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    pass
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v33_events.json', 'w')); print('done', T_END)
