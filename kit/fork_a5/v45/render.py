import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
import numpy as np
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
    w_src = int(1080 * W / W * (1080 / h) * (W / 1080)) if False else int(1080 * W / h)
    w_src = min(1920, int(1080 * (W / h)))
    x0 = (1920 - w_src) // 2
    return bg_frames(name, (W, h), box=(x0, 0, x0 + w_src, 1080), step=2, bright=bright)
RT = {k: realm(v[2], HALF) for k, v in G.items()}            # half-height realm strips
RQ = {k: realm(v[2], 690, 0.7) for k, v in G.items()}        # end quadrants (540 wide crop later)
JAR = {}
for k, v in G.items():
    j = crop(Image.open(A + v[3]).convert('RGBA')); JAR[k] = j.resize((int(j.width * 200 / j.height), 200), Image.NEAREST)
JARS = {k: j.resize((int(j.width * 150 / j.height), 150), Image.NEAREST) for k, j in JAR.items()}
GUM = {k: gummy(v[4], 3) for k, v in G.items()}
IDL = {k: idle(v[5], 3) for k, v in G.items()}               # 276px canvas, feet ~ y 234
IDL4 = {k: idle(v[5], 4) for k, v in G.items()}
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def card(text, k, t, glow):
    name, col = G[k][0], G[k][1]
    cw, chh = 980, 560
    c = Image.new('RGBA', (cw, chh), (0, 0, 0, 0))
    layer(c, lambda d: d.rounded_rectangle([0, 0, cw - 1, chh - 1], 26, fill=(14, 10, 24, 205)))
    d = ImageDraw.Draw(c)
    bw = 7 + int(3 * glow)
    d.rounded_rectangle([3, 3, cw - 4, chh - 4], 24, outline=col, width=bw)
    d.rounded_rectangle([16, 16, cw - 17, chh - 17], 18, outline=tuple(int(x * 0.45) for x in col), width=3)
    fs = 64 if len(text) <= 12 else 50
    ctext(d, cw / 2, 50, text, F(fs), (255, 255, 255), 7)
    # guide idle, jar, gummy
    ctext(d, cw / 2, 140, name + ' GUILD', F(30), col, 5)
    fr = IDL4[k][int(t * 8) % len(IDL4[k])]
    c.alpha_composite(fr, (40, 540 - 312))
    j = JAR[k]; c.alpha_composite(j, (cw // 2 - j.width // 2 + 20, 530 - j.height))
    g = GUM[k]; bob = int(10 * math.sin(t * 4 + len(text)))
    gx, gy = cw - 240, 300 + bob
    layer(c, lambda dd: dd.ellipse([gx - 30, gy - 30, gx + g.width + 30, gy + g.height + 30], fill=col + (60,)))
    c.alpha_composite(g, (gx, gy))
    for s in range(4):
        a = t * 3 + s * 1.57; sx, sy = gx + g.width / 2 + 75 * math.cos(a), gy + g.height / 2 + 55 * math.sin(a)
        d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 200))
    return c
TQ = 3.7; T0 = 3.2; TEND = T0 + TQ * 5; DUR = TEND + 6.0
NF = int(DUR * FPS)
wr = Writer('v45_noaudio.mp4'); ev = []
FONT_T = F(62)
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (12, 10, 20, 255))
    if t < T0:
        # intro: four guild realms tiled in stripes behind
        for i, k in enumerate('FVER'):
            strip = RT[k][int(t * 5) % len(RT[k])].crop((0, 0, W, 480))
            img.alpha_composite(strip, (0, 400 + i * 380 - 50))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 18, 110)))
        d = ImageDraw.Draw(img)
        for i, k in enumerate('FVER'):
            u = ease((t - 0.3 - i * 0.15) / 0.4); x = -600 + (600) * u
            y = 470 + i * 330
            panel = Image.new('RGBA', (900, 290), (0, 0, 0, 0))
            layer(panel, lambda dd: dd.rounded_rectangle([0, 0, 899, 289], 22, fill=(14, 10, 24, 200), outline=G[k][1] + (255,), width=6))
            fr = IDL[k][int(t * 8) % 6]; panel.alpha_composite(fr, (20, 290 - 250))
            js = JARS[k]; panel.alpha_composite(js, (300, 290 - js.height - 40))
            g = GUM[k]; panel.alpha_composite(g, (470, 130 + int(8 * math.sin(t * 4 + i))))
            pd = ImageDraw.Draw(panel); pd.text((570, 110), G[k][0], font=F(30), fill=G[k][1], stroke_width=4, stroke_fill=(20, 15, 35))
            pd.text((570, 160), G[k][6], font=F(24), fill=(230, 230, 230), stroke_width=3, stroke_fill=(20, 15, 35))
            img.alpha_composite(panel, (int(90 + x), y))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, 110, 'WHICH GUILD', F(78)); ctext(d, W / 2, 210, 'ARE YOU?', F(78), (255, 214, 60))
        ctext(d, W / 2, 330, 'Pick one each round. Count your colors.', F(26), (235, 235, 235), 4)
        if f == int(0.3 * FPS): ev.append((0.3, 'whoosh_8bit'))
    elif t < TEND:
        qi = int((t - T0) // TQ); u = t - T0 - qi * TQ
        a, ka, b, kb = QS[qi]
        img.alpha_composite(RT[ka][int(t * 5) % len(RT[ka])], (0, 0))
        img.alpha_composite(RT[kb][int(t * 5 + 3) % len(RT[kb])], (0, HALF))
        # seam
        layer(img, lambda d: (d.polygon([(0, HALF - 18), (W, HALF - 48), (W, HALF + 18), (0, HALF + 48)], fill=(14, 10, 24, 255)),
                              d.rectangle([0, 0, W, 330], fill=(10, 8, 18, 150))))
        inn = ease(u / 0.35); out = ease((u - (TQ - 0.3)) / 0.3)
        glow = 0.5 + 0.5 * math.sin(t * 6)
        ca = card(a, ka, t, glow); cb = card(b, kb, t + 1, 1 - glow)
        xa = 50 + (-1100) * (1 - inn) + 1100 * out; xb = 50 + 1100 * (1 - inn) - 1100 * out
        img.alpha_composite(ca, (int(xa), 370)); img.alpha_composite(cb, (int(xb), HALF + 70))
        d = ImageDraw.Draw(img)
        # OR emblem
        r = 74 + int(6 * math.sin(t * 5))
        layer(img, lambda dd: dd.ellipse([W / 2 - r, HALF - r, W / 2 + r, HALF + r], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=8))
        d = ImageDraw.Draw(img); ctext(d, W / 2, HALF - 26, 'OR', F(52), (20, 15, 35), 0)
        ctext(d, W / 2, 70, f'QUESTION {qi + 1}/5', F(44), (255, 214, 60), 6)
        for p in range(5):
            px = W / 2 - 200 + p * 100
            d.rounded_rectangle([px - 34, 150, px + 34, 170], 8, fill=(255, 214, 60) if p <= qi else (70, 64, 90))
        ctext(d, W / 2, 210, 'Which one are you?', F(30), (235, 235, 235), 4)
        # timer bar
        frac = max(0, 1 - u / (TQ - 0.3))
        layer(img, lambda dd: dd.rounded_rectangle([60, 1840, W - 60, 1872], 14, fill=(14, 10, 24, 220)))
        d = ImageDraw.Draw(img); d.rounded_rectangle([66, 1846, 66 + int((W - 132) * frac), 1866], 10, fill=(255, 214, 60))
        if abs(u - 0.02) < 0.5 / FPS: ev.append((round(t, 3), 'whoosh_8bit')); ev.append((round(t + 0.25, 3), 'ding_8bit'))
    else:
        u = t - TEND
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(12, 10, 20, 255)))
        for i, k in enumerate('FVER'):
            cx, cy = (i % 2) * 540, 360 + (i // 2) * 720
            fr = RQ[k][int(t * 5) % len(RQ[k])].crop((270, 0, 270 + 540, 690))
            q = ease((u - i * 0.12) / 0.4)
            tile = fr.copy()
            layer(tile, lambda dd: dd.rectangle([0, 0, 539, 689], outline=G[k][1] + (255,), width=8))
            td = ImageDraw.Draw(tile)
            ctext(td, 270, 40, G[k][0], F(40), G[k][1], 6)
            fi = IDL[k][int(t * 8) % 6]; tile.alpha_composite(fi, (10, 690 - 276 - 70))
            js = JARS[k]; tile.alpha_composite(js, (300, 690 - js.height - 120))
            g = GUM[k]; tile.alpha_composite(g, (330, 160 + int(10 * math.sin(t * 4 + i))))
            ctext(td, 270, 620, G[G and k][6] if False else G[k][6], F(28), (255, 255, 255), 5)
            if q < 1: tile = up(tile, 0.2 + 0.8 * q) if q > 0.05 else None
            if tile is not None: img.alpha_composite(tile, (int(cx + 270 - tile.width / 2), int(cy + 345 - tile.height / 2)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, 120, 'MOST PICKED COLOR', F(56)); ctext(d, W / 2, 210, '= YOUR GUILD', F(56), (255, 214, 60))
        if u > 0.8:
            a_ = int(255 * min(1, (u - 0.8) / 0.4)); sc = 1 + 0.04 * math.sin(t * 6)
            text_layer(img, [(W / 2, 1830, 'COMMENT YOUR GUILD', int(52 * sc), (255, 214, 60), 7, a_)])
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'chime'))
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v45_ev.json', 'w')); print('done', DUR, len(ev))
