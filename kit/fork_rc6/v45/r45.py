# rc6 recut of #45 (Bennett: safe zone). Source: fork_sz44/v45/render.py
import sys, math, json, random, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = {  # guild: (name, color, realm gif, jar file, gummy, guide, product label)
 'F': ('FOUNDATION', (120, 225, 90), 'found_hd.gif', 'jar_acv.png', 'acv', 'joy', 'ACV GUMMY'),
 'V': ('VITALITY', (100, 165, 255), 'vit_hd.gif', 'jar_creatine.png', 'cre', 'cleo', 'CREATINE'),
 'E': ('ENERGY', (255, 165, 50), 'sun_hd.gif', 'jar_mushroom.png', 'mush', 'cyrus', 'MUSHROOM'),
 'R': ('RECOVERY', (195, 120, 255), 'recov_hd.gif', 'jar_melatonin.png', 'mel', 'ray', 'MELATONIN')}
# Q5 (GYM FIRST V vs COFFEE FIRST E) cut: it repeated Q2's pairing and gave V and E 3 appearances vs 2 (VETTING r045)
QS = [('NIGHT OWL', 'R', 'EARLY BIRD', 'F'), ('TANK', 'V', 'SPEEDRUNNER', 'E'), ('COZY FARM GAME', 'F', 'BOSS RUSH', 'V'),
      ('ONE MORE LEVEL', 'E', 'SAVE AND LOG OFF', 'R')]
NQ = len(QS)
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
GUM = {k: (up(acv_gummy_strong(), 3) if v[4] == 'acv' else gummy(v[4], 3)) for k, v in G.items()}   # ACV gets the gummy shine
IDL = {k: idle(v[5], 3) for k, v in G.items()}
IDL4 = {k: idle(v[5], 4) for k, v in G.items()}
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
HOOK, HB = hook_layer2(['WHICH GUILD', 'ARE YOU?'], accent=1, sub='Comment your guild')
print('hook bottom', HB)
CX0, CW, CH = 78, 800, 370
def card(text, k, t, glow):
    col = G[k][1]
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    layer(c, lambda d: d.rounded_rectangle([0, 0, CW - 1, CH - 1], 26, fill=(14, 10, 24, 205)))
    d = ImageDraw.Draw(c)
    bw = 7 + int(3 * glow)
    d.rounded_rectangle([3, 3, CW - 4, CH - 4], 24, outline=col, width=bw)
    d.rounded_rectangle([16, 16, CW - 17, CH - 17], 18, outline=tuple(int(x * 0.45) for x in col), width=3)
    fs = min(64, int((CW - 60) / len(text)))
    ctext(d, CW / 2, 30, text, F(fs), (255, 255, 255), 7)
    fr = IDL4[k][int(t * 8) % len(IDL4[k])]
    c.alpha_composite(fr, (-50, CH - 12 - 312))
    j = JAR[k]; c.alpha_composite(j, (CW // 2 - j.width // 2 + 10, CH - 16 - j.height))
    g = GUM[k]; bob = int(10 * math.sin(t * 4 + len(text)))
    gx, gy = CW - 200, 190 + bob
    layer(c, lambda dd: dd.ellipse([gx - 30, gy - 30, gx + g.width + 30, gy + g.height + 30], fill=col + (60,)))
    c.alpha_composite(g, (gx, gy))
    for s in range(4):
        a = t * 3 + s * 1.57; sx, sy = gx + g.width / 2 + 70 * math.cos(a), gy + g.height / 2 + 50 * math.sin(a)
        d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 200))
    return c
PH = 204; PG = 4
def panel(k, t, i):
    p = Image.new('RGBA', (CW, PH), (0, 0, 0, 0))
    layer(p, lambda dd: dd.rounded_rectangle([0, 0, CW - 1, PH - 1], 22, fill=(14, 10, 24, 205), outline=G[k][1] + (255,), width=6))
    fr = IDL[k][int(t * 8) % 6]; p.alpha_composite(fr, (-64, PH - 6 - 234))
    js = JARS[k]; p.alpha_composite(js, (160, PH - js.height - 22))
    g = GUM[k]; p.alpha_composite(g, (300 - g.width // 2, 64 + int(8 * math.sin(t * 4 + i))))
    pd = ImageDraw.Draw(p)
    for txt, y, colr in ((G[k][0], 40, G[k][1]), (G[k][6], 112, (235, 235, 235))):
        assert 346 + pd.textlength(txt, font=F(44)) <= CW - 8, txt
        pd.text((346, y), txt, font=F(44), fill=colr, stroke_width=6, stroke_fill=(20, 15, 35))
    return p
def strips(t, img):
    for i, k in enumerate('FVER'):
        img.alpha_composite(RT[k][int(t * 5) % len(RT[k])].crop((0, 0, W, 480)), (0, i * 480))
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 18, 110)))
T0 = 2.4; TQ = 2.6; TEND = T0 + TQ * NQ
GRID_HOLD = 2.0; OUTRO = 0.4; DUR = TEND + 0.5 + GRID_HOLD + OUTRO
NF = int(round(DUR * FPS))
wr = Writer('v45_noaudio.mp4'); ev = []
LBL = HB + 8                                     # question label plate / intro line
YA = HB + 112; SEAM = YA + CH + 26; YB = SEAM + 26
print('cards', YA, SEAM, YB, YB + CH); assert YB + CH <= 1496
PY0 = HB + 84
assert PY0 + 4 * PH + 3 * PG <= 1498, PY0 + 4 * PH + 3 * PG
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (12, 10, 20, 255))
    if t < T0:
        strips(t, img)
        layer(img, lambda d: d.rounded_rectangle([CX0, LBL, CX0 + CW, LBL + 72], 16, fill=(14, 10, 24, 215)))
        text_layer(img, [(CX0 + CW / 2, LBL + 14, 'COUNT YOUR COLORS', 44, (255, 214, 60), 7, 255)])
        for i, k in enumerate('FVER'):
            u = ease((t + 0.08 - i * 0.12) / 0.4); x = -900 * (1 - u)   # legend already mid-slide on frame 0
            img.alpha_composite(panel(k, t, i), (int(CX0 + x), PY0 + i * (PH + PG)))
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
        osc = max(0.0, min(inn, 1 - out))               # OR badge scales in/out with the cards (never alone)
        if osc > 0.02:
            r = int((64 + 6 * math.sin(t * 5)) * osc); ox = CX0 + CW / 2
            layer(img, lambda dd: dd.ellipse([ox - r, SEAM - r, ox + r, SEAM + r], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=8))
            if osc > 0.5: d = ImageDraw.Draw(img); ctext(d, ox, SEAM - int(24 * osc), 'OR', F(max(8, int(48 * osc))), (20, 15, 35), 0)
        ox = CX0 + CW / 2
        layer(img, lambda dd: dd.rounded_rectangle([CX0, LBL, CX0 + CW, LBL + 96], 16, fill=(14, 10, 24, 215)))
        d = ImageDraw.Draw(img); ctext(d, ox, LBL + 12, f'QUESTION {qi + 1}/{NQ}', F(44), (255, 214, 60), 7)
        frac = max(0, 1 - u / (TQ - 0.3))
        d.rounded_rectangle([CX0 + 20, LBL + 72, CX0 + 20 + int((CW - 40) * frac), LBL + 84], 6, fill=(255, 214, 60))
        if u < 1 / FPS - 1e-6: ev.append((round(t, 3), 'swish')); ev.append((round(t + 0.25, 3), 'ding_8bit'))
    else:
        u = t - TEND
        strips(t, img)
        tw, th = 404, 372; gx0 = 72; gy0 = HB + 126
        oq = ease((u - 0.5 - GRID_HOLD) / OUTRO)         # outro: tiles shrink away -> opening state (loop)
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 18, int(120 * (1 - oq)))))
        for i, k in enumerate('FVER'):
            cx, cy = gx0 + (i % 2) * (tw + 4), gy0 + (i // 2) * (th + 4)
            fr = RQ[k][int(t * 5) % len(RQ[k])].crop((335, 160, 335 + tw, 160 + th))
            q = ease((u - i * 0.1) / 0.35) * (1 - oq)
            tile = fr.copy()
            layer(tile, lambda dd: dd.rectangle([0, 0, tw - 1, th - 1], outline=G[k][1] + (255,), width=8))
            td = ImageDraw.Draw(tile)
            ctext(td, tw / 2, 22, G[k][0], F(40), G[k][1], 7)
            fi = IDL[k][int(t * 8) % 6]; tile.alpha_composite(fi, (-30, th - 24 - 234))
            js = JARS[k]; tile.alpha_composite(js, (190, th - js.height - 34))
            g = GUM[k]; tile.alpha_composite(g, (300, 110 + int(10 * math.sin(t * 4 + i))))
            if q < 1: tile = up(tile, 0.2 + 0.8 * q) if q > 0.05 else None
            if tile is not None: img.alpha_composite(tile, (int(cx + tw / 2 - tile.width / 2), int(cy + th / 2 - tile.height / 2)))
        if oq > 0:                                       # opening instruction plate comes back so the last frame matches frame 0
            a2 = int(255 * oq)
            layer(img, lambda d: d.rounded_rectangle([CX0, LBL, CX0 + CW, LBL + 72], 16, fill=(14, 10, 24, int(215 * a2 / 255))))
            text_layer(img, [(CX0 + CW / 2, LBL + 14, 'COUNT YOUR COLORS', 44, (255, 214, 60), 7, a2)])
        ta = int(255 * (1 - oq))
        if ta > 0:
            layer(img, lambda d: d.rounded_rectangle([CX0, LBL, CX0 + CW, LBL + 112], 16, fill=(14, 10, 24, int(215 * ta / 255))))
            text_layer(img, [(CX0 + CW / 2, LBL + 10, 'MOST PICKED COLOR', 44, (255, 255, 255), 7, ta),
                             (CX0 + CW / 2, LBL + 60, '= YOUR GUILD', 44, (255, 214, 60), 7, ta)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 12, 60, 80, 150, 300, 420, 445, NF - 1): img.convert('RGB').save(f'p45_{f:04d}.png')
wr.close()
ev += [(0.0, 'swish'), (round(TEND, 3), 'chime')]
json.dump({'events': ev}, open('v45_ev.json', 'w')); print('done', DUR, NF)
