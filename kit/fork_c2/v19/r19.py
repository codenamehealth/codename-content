import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
OUT = SP + 'fork_c2/v19/v19_noaudio.mp4'
X1 = int(os.environ.get('X1', '400')); GF1 = float(os.environ.get('GF1', str(720 / 860))); FLIP1 = os.environ.get('FLIP1') == '1'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['CHASE THE LOOT'], accent=0, sub='OR PLANT THE TREE?', sub_color=(140, 230, 110))
DUR = 11.0; N = int(DUR * FPS)
PH = 490; P1, P2 = HB + 14, HB + 14 + PH + 50        # panel tops
GF = {}
def panel_bg(name, x0, gfrac):
    k = (W + x0) / 1920; ww, hh = int(1920 * k), int(1080 * k)
    fr = bg_frames(name, (ww, hh), step=2); y0 = hh - PH
    GF[name] = int(gfrac * hh) - y0
    out = [f.crop((x0, y0, x0 + W, y0 + PH)) for f in fr]
    return out
BG1 = panel_bg('found_hd.gif', X1, GF1)   # Bennett: no castle, top panel is the forest too
if FLIP1: BG1 = [b.transpose(Image.FLIP_LEFT_RIGHT) for b in BG1]
GF1_px = GF['found_hd.gif']; BG2 = panel_bg('found_hd.gif', 60, 720 / 860)
RUN = seq(PL + 'race/joy_run', 3, 1, 9)
FALL = []
for p in sorted(glob.glob(SP + 'fork2/joy_fall/*.png'))[1:9]:
    im = Image.open(p).convert('RGBA'); a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([0, 81, 92, 92], fill=0); im.putalpha(a); FALL.append(up(im, 3))
PLANT = seq(SP + 'fork2/joy_plant', 3, 1, 13)
IDLE = idle('joy', 3)
LEDGE = up(crop(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA')), 3)
SAP = up(crop(Image.open(SP + 'fork2/sapling/00.png').convert('RGBA')), 3)
SMALL = up(crop(Image.open(SP + 'fork2/smalltree/01.png').convert('RGBA')), 4)
BIG = up(crop(Image.open(SP + 'fork2/bigtree/00.png').convert('RGBA')), 3)
GOLD = gummy('gold', 3); GS = [gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']]
_b = Image.open(A + 'found_hd.gif'); _b.seek(0); _b = _b.convert('RGB'); _k = H / _b.height
_b = _b.resize((int(_b.width * _k), H), Image.NEAREST); _b = _b.crop(((_b.width - W) // 2, 0, (_b.width - W) // 2 + W, H))
BACK = ImageEnhance.Brightness(_b.filter(ImageFilter.GaussianBlur(8))).enhance(0.35).convert('RGBA')
G1 = P1 + GF1_px; G2 = P2 + GF['found_hd.gif']       # ground lines
print('ground', G1 - P1, G2 - P2)
EDGE = 770
CYC = [0.3, 4.0, 7.7]; RUN_T = 2.4
events = []
rng = random.Random(11)
drops = []; td = 5.9
while td < DUR - 0.3:
    drops.append((td, rng.choice(GS), rng.uniform(-60, 120), rng.uniform(-140, 140))); td += rng.uniform(0.28, 0.42)
for c in CYC:
    events += [(c + RUN_T, 'jump'), (c + RUN_T + 0.35, 'whoosh_8bit'), (c + 3.5, 'poof')]
events += [(1.4, 'twinkle'), (3.4, 'chime'), (5.0, 'chime'), (5.0, 'twinkle')] + [(d[0] + 0.45, 'coin_8bit') for d in drops]
wr = Writer(OUT)
pile = []
PREV = os.environ.get('PREV')
for f in (range(N) if not PREV else [int(float(PREV) * FPS)]):
    t = f / FPS
    img = BACK.copy()
    # ---------- panel 1: chase the loot
    p1 = BG1[int(t * 5) % len(BG1)].copy()
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, min(255, 150 + int((y - G1 + P1 + 60) * 1.2)))) for y in range(G1 - P1 - 60, PH, 4)])
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, int(150 * (y - (G1 - P1 - 110)) / 50))) for y in range(G1 - P1 - 110, G1 - P1 - 60, 4)])
    p1.alpha_composite(LEDGE, (EDGE + 30 - LEDGE.width, G1 - P1 - 18))
    c0 = max([c for c in CYC if c <= t], default=None)
    if c0 is None:
        jx, jy, spr, gxo = 120, G1 - P1, RUN[0], 0
    else:
        u = t - c0
        if u < RUN_T:
            k = u / RUN_T; jx = 120 + (EDGE - 120) * k; jy = G1 - P1; spr = RUN[int(u * 14) % 8]
        elif u < RUN_T + 1.1:
            v = (u - RUN_T) / 1.1; k = min(7, int(v * 10)); spr = FALL[k]
            jx = EDGE + 120 * v; jy = G1 - P1 + 900 * max(0, v - 0.25) ** 2
        else: spr = None; jx, jy = 120, G1 - P1
    # the gold gummy keeps floating just out of reach
    if c0 is not None and t - c0 < RUN_T + 1.4:
        u = t - c0; gx = min(EDGE + 200, 120 + 170 + (EDGE - 120) * min(1, u / RUN_T) + 40 * max(0, u - RUN_T)); gy = G1 - P1 - 190 + 14 * math.sin(t * 5)
    else: gx, gy = 290, G1 - P1 - 190 + 14 * math.sin(t * 5)
    layer(p1, lambda d: [d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 220, 120, 18)) for r in (70, 55, 40)])
    p1.alpha_composite(GOLD, (int(gx - GOLD.width / 2), int(gy - GOLD.height / 2)))
    if spr is not None:
        p1.alpha_composite(spr, (int(jx - spr.width / 2), int(jy - 78 * 3)))
        if c0 is not None and RUN_T - 0.1 < t - c0 < RUN_T + 0.5:
            ctext(ImageDraw.Draw(p1), jx + 40, jy - 300, '!', F(64), (255, 80, 80), 7)
    if c0 is not None and RUN_T + 1.1 <= t - c0 < RUN_T + 1.5:
        v = (t - c0 - RUN_T - 1.1) / 0.4
        layer(p1, lambda d: [d.ellipse([120 - 30 - 60 * v + k * 20, G1 - P1 - 120, 120 + 30 + 60 * v - k * 20, G1 - P1], outline=(255, 255, 255, int(200 * (1 - v))), width=6) for k in range(1)])
    # ---------- panel 2: plant the tree
    p2 = BG2[int(t * 5) % len(BG2)].copy()
    TX = 470
    if t >= 1.4:
        if t < 3.4: tr = SAP; sc = min(1, (t - 1.4) / 0.3)
        elif t < 5.0: tr = SMALL; sc = min(1, 0.6 + (t - 3.4) / 0.4)
        else: tr = BIG; sc = min(1, 0.7 + (t - 5.0) / 0.5)
        tim = up(tr, sc) if sc < 1 else tr
        layer(p2, lambda d: d.ellipse([TX - tim.width * 0.4, G2 - P2 - 14, TX + tim.width * 0.4, G2 - P2 + 14], fill=(0, 0, 0, 70)))
        p2.alpha_composite(tim, (int(TX - tim.width / 2), int(G2 - P2 - tim.height + 6)))
        for ts_ in (1.4, 3.4, 5.0):
            if ts_ <= t < ts_ + 0.6:
                v = (t - ts_) / 0.6
                layer(p2, lambda d: [d.rectangle([TX + math.cos(a) * (40 + 160 * v) - 5, G2 - P2 - 120 + math.sin(a) * (40 + 120 * v) - 5, TX + math.cos(a) * (40 + 160 * v) + 5, G2 - P2 - 120 + math.sin(a) * (40 + 120 * v) + 5], fill=(255, 245, 170, int(255 * (1 - v)))) for a in [k * 0.785 for k in range(8)]])
    # gummies falling from the tree into a growing pile
    landed = 0
    for i, (t0, g, dx, sx) in enumerate(drops):
        if t < t0: continue
        u = t - t0
        x = TX + dx + sx * min(u, 0.45) * 0.3; y0 = G2 - P2 - 330
        if u < 0.45:
            y = y0 + (u / 0.45) ** 2 * 300; p2.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        else:
            landed += 1
    for i, (t0, g, dx, sx) in enumerate(drops[:landed]):
        row = i // 6; col = i % 6
        x = 662 + col * 34 + (row % 2) * 17; y = G2 - P2 - 18 - row * 28
        p2.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    if t < 0.4: spr2 = IDLE[int(t * 8) % len(IDLE)]
    elif t < 2.2: spr2 = PLANT[min(11, int((t - 0.4) / 1.8 * 12))]
    else: spr2 = IDLE[int(t * 8) % len(IDLE)]
    p2.alpha_composite(spr2, (int(205 - spr2.width / 2), int(G2 - P2 - 78 * 3)))
    if landed: ctext(ImageDraw.Draw(p2), 760, G2 - P2 + 22, f'x{landed}', F(40), (255, 214, 60), 6)
    # compose
    img.alpha_composite(p1, (0, P1)); img.alpha_composite(p2, (0, P2))
    d = ImageDraw.Draw(img)
    d.rectangle([0, P1 + PH, W, P2], fill=(14, 10, 24))
    items = [(W / 2, P1 + PH + 5, 'OR', 40, (200, 190, 255), 6, 255)]
    if t > 9.4:
        a = int(255 * min(1, (t - 9.4) / 0.3))
        layer(img, lambda dd: dd.rectangle([0, P1 + PH - 70, W, P2 + 70], fill=(14, 10, 24, int(220 * a / 255))))
        items = [it for it in items if it[2] != 'OR'] + [(W / 2, P1 + PH - 50, 'WHICH ONE', 54, (255, 255, 255), 8, a), (W / 2, P1 + PH + 20, 'ARE YOU?', 54, (255, 214, 60), 8, a)]
    text_layer(img, items); img.alpha_composite(HOOK)
    if PREV: img.convert('RGB').resize((540, 960)).save(SP + 'fork_c2/v19/prev_%s.png' % os.environ.get('TAG', 'x')); break
    wr.write(img)
    if f in (60, 150, 315): img.convert('RGB').save(SP + f'fork_c2/v19/p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in sorted(events)]}, open(SP + 'fork_c2/v19/v19_events.json', 'w'))
print('done', len(drops))
