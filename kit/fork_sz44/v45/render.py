import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = {  # guild: (name, color, realm gif, jar file, gummy, guide, product)
 'F': ('FOUNDATION', (120, 225, 90), 'found_hd.gif', 'jar_acv.png', 'acv', 'joy', 'ACV'),
 'V': ('VITALITY', (100, 165, 255), 'vit_hd.gif', 'jar_creatine.png', 'cre', 'cleo', 'CREATINE'),
 'E': ('ENERGY', (255, 165, 50), 'sun_hd.gif', 'jar_mushroom.png', 'mush', 'cyrus', 'MUSHROOM'),
 'R': ('RECOVERY', (195, 120, 255), 'recov_hd.gif', 'jar_melatonin.png', 'mel', 'ray', 'MELATONIN')}
QS = [('NIGHT OWL', 'R', 'EARLY BIRD', 'F'), ('TANK', 'V', 'SPEEDRUNNER', 'E'), ('COZY FARM GAME', 'F', 'BOSS RUSH', 'V'),
      ('ONE MORE LEVEL', 'E', 'SAVE AND LOG OFF', 'R'), ('GYM FIRST', 'V', 'COFFEE FIRST', 'E')]
HALF = 960
def realm(name, h, bright=0.62):
    w_src = min(1920, int(1080 * (W / h)))
    x0 = (1920 - w_src) // 2
    return bg_frames(name, (W, h), box=(x0, 0, x0 + w_src, 1080), step=2, bright=bright)
RT = {k: realm(v[2], HALF) for k, v in G.items()}
RQ = {k: realm(v[2], 690, 0.7) for k, v in G.items()}
JAR = {}
for k, v in G.items():
    j = crop(Image.open(A + v[3]).convert('RGBA')); JAR[k] = j.resize((int(j.width * 200 / j.height), 200), Image.NEAREST)
JARS = {k: j.resize((int(j.width * 150 / j.height), 150), Image.NEAREST) for k, j in JAR.items()}
GUM = {k: gummy(v[4], 3) for k, v in G.items()}
IDL = {k: idle(v[5], 3) for k, v in G.items()}               # 276px canvas, feet y 234
IDL4 = {k: idle(v[5], 4) for k, v in G.items()}              # 368px canvas, feet y 312
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
HOOK, HB = hook_layer(['WHICH GUILD', 'ARE YOU?'], accent=1)
print('hook bottom', HB)
CX0, CW, CH = 78, 800, 400       # cards fit x 78..878 (clear of the lower-right buttons)
def card(text, k, t, glow):
    name, col = G[k][0], G[k][1]
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    layer(c, lambda d: d.rounded_rectangle([0, 0, CW - 1, CH - 1], 26, fill=(14, 10, 24, 205)))
    d = ImageDraw.Draw(c)
    bw = 7 + int(3 * glow)
    d.rounded_rectangle([3, 3, CW - 4, CH - 4], 24, outline=col, width=bw)
    d.rounded_rectangle([16, 16, CW - 17, CH - 17], 18, outline=tuple(int(x * 0.45) for x in col), width=3)
    fs = min(64, int((CW - 60) / len(text)))
    ctext(d, CW / 2, 30, text, F(fs), (255, 255, 255), 7)
    ctext(d, CW / 2, 30 + fs + 14, name + ' GUILD', F(30), col, 5)
    fr = IDL4[k][int(t * 8) % len(IDL4[k])]
    c.alpha_composite(fr, (-50, CH - 12 - 312))
    j = JAR[k]; c.alpha_composite(j, (CW // 2 - j.width // 2 + 10, CH - 16 - j.height))
    g = GUM[k]; bob = int(10 * math.sin(t * 4 + len(text)))
    gx, gy = CW - 200, 210 + bob
    layer(c, lambda dd: dd.ellipse([gx - 30, gy - 30, gx + g.width + 30, gy + g.height + 30], fill=col + (60,)))
    c.alpha_composite(g, (gx, gy))
    for s in range(4):
        a = t * 3 + s * 1.57; sx, sy = gx + g.width / 2 + 70 * math.cos(a), gy + g.height / 2 + 50 * math.sin(a)
        d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 200))
    return c
TQ = 3.7; T0 = 3.2; TEND = T0 + TQ * 5; DUR = TEND + 6.0
NF = int(DUR * FPS)
wr = Writer('v45_noaudio.mp4')
YA = HB + 96; SEAM = YA + CH + 30; YB = SEAM + 30          # card A, OR seam, card B
print('cards', YA, SEAM, YB, YB + CH)
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (12, 10, 20, 255))
    if t < T0:
        for i, k in enumerate('FVER'):
            strip = RT[k][int(t * 5) % len(RT[k])].crop((0, 0, W, 480))
            img.alpha_composite(strip, (0, i * 480))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 18, 110)))
        text_layer(img, [(478, HB + 14, 'Pick one each round.', 28, (235, 235, 235), 4, 255),
                         (478, HB + 54, 'Count your colors.', 28, (255, 214, 60), 4, 255)])
        for i, k in enumerate('FVER'):
            u = ease((t - 0.3 - i * 0.15) / 0.4); x = -900 * (1 - u)
            ph = 212; y = HB + 96 + i * (ph + 8)
            panel = Image.new('RGBA', (CW, ph), (0, 0, 0, 0))
            layer(panel, lambda dd: dd.rounded_rectangle([0, 0, CW - 1, ph - 1], 22, fill=(14, 10, 24, 200), outline=G[k][1] + (255,), width=6))
            fr = IDL[k][int(t * 8) % 6]; panel.alpha_composite(fr, (-30, ph - 10 - 234))
            js = JARS[k]; panel.alpha_composite(js, (230, ph - js.height - 18))
            g = GUM[k]; panel.alpha_composite(g, (380, 80 + int(8 * math.sin(t * 4 + i))))
            pd = ImageDraw.Draw(panel); pd.text((470, 66), G[k][0], font=F(30), fill=G[k][1], stroke_width=4, stroke_fill=(20, 15, 35))
            pd.text((470, 116), G[k][6], font=F(24), fill=(230, 230, 230), stroke_width=3, stroke_fill=(20, 15, 35))
            img.alpha_composite(panel, (int(CX0 + x), y))
    elif t < TEND:
        qi = int((t - T0) // TQ); u = t - T0 - qi * TQ
        a, ka, b, kb = QS[qi]
        img.alpha_composite(RT[ka][int(t * 5) % len(RT[ka])], (0, SEAM - HALF))
        img.alpha_composite(RT[kb][int(t * 5 + 3) % len(RT[kb])], (0, SEAM))
        layer(img, lambda d: d.polygon([(0, SEAM - 18), (W, SEAM - 48), (W, SEAM + 18), (0, SEAM + 48)], fill=(14, 10, 24, 255)))
        inn = ease(u / 0.35); out = ease((u - (TQ - 0.3)) / 0.3)
        glow = 0.5 + 0.5 * math.sin(t * 6)
        ca = card(a, ka, t, glow); cb = card(b, kb, t + 1, 1 - glow)
        xa = CX0 + (-1100) * (1 - inn) + 1100 * out; xb = CX0 + 1100 * (1 - inn) - 1100 * out
        img.alpha_composite(ca, (int(xa), YA)); img.alpha_composite(cb, (int(xb), YB))
        r = 64 + int(6 * math.sin(t * 5)); ox = CX0 + CW / 2
        layer(img, lambda dd: dd.ellipse([ox - r, SEAM - r, ox + r, SEAM + r], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=8))
        d = ImageDraw.Draw(img); ctext(d, ox, SEAM - 24, 'OR', F(48), (20, 15, 35), 0)
        # question label + timer bar under the hook
        layer(img, lambda dd: dd.rounded_rectangle([CX0, HB + 10, CX0 + CW, HB + 84], 16, fill=(14, 10, 24, 215)))
        d = ImageDraw.Draw(img); ctext(d, ox, HB + 20, f'QUESTION {qi + 1}/5', F(32), (255, 214, 60), 5)
        frac = max(0, 1 - u / (TQ - 0.3))
        d.rounded_rectangle([CX0 + 20, HB + 62, CX0 + 20 + int((CW - 40) * frac), HB + 74], 6, fill=(255, 214, 60))
    else:
        u = t - TEND
        tw, th = 398, 380; gx0 = 78; gy0 = HB + 124
        for i, k in enumerate('FVER'):
            cx, cy = gx0 + (i % 2) * (tw + 4), gy0 + (i // 2) * (th + 4)
            fr = RQ[k][int(t * 5) % len(RQ[k])].crop((341, 160, 341 + tw, 160 + th))
            q = ease((u - i * 0.12) / 0.4)
            tile = fr.copy()
            layer(tile, lambda dd: dd.rectangle([0, 0, tw - 1, th - 1], outline=G[k][1] + (255,), width=8))
            td = ImageDraw.Draw(tile)
            ctext(td, tw / 2, 22, G[k][0], F(32), G[k][1], 6)
            fi = IDL[k][int(t * 8) % 6]; tile.alpha_composite(fi, (-30, th - 50 - 234))
            js = JARS[k]; tile.alpha_composite(js, (190, th - js.height - 60))
            g = GUM[k]; tile.alpha_composite(g, (300, 100 + int(10 * math.sin(t * 4 + i))))
            ctext(td, tw / 2, th - 44, G[k][6], F(24), (255, 255, 255), 5)
            if q < 1: tile = up(tile, 0.2 + 0.8 * q) if q > 0.05 else None
            if tile is not None: img.alpha_composite(tile, (int(cx + tw / 2 - tile.width / 2), int(cy + th / 2 - tile.height / 2)))
        text_layer(img, [(478, HB + 16, 'MOST PICKED COLOR', 44, (255, 255, 255), 6, 255),
                         (478, HB + 68, '= YOUR GUILD', 44, (255, 214, 60), 6, 255)])
        if u > 0.8:
            a_ = int(255 * min(1, (u - 0.8) / 0.4)); sc = 1 + 0.04 * math.sin(t * 6)
            text_layer(img, [(478, gy0 + 2 * th + 22, 'COMMENT YOUR GUILD', int(42 * sc), (255, 214, 60), 7, a_)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); print('done', DUR)
