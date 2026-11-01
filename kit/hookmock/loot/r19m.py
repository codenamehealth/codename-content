import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
# rc3 recut of #19 (source fork_c2/v19/r19.py, run with X1=700). Bennett #19: no castle, top panel is the forest too (kept).
D19 = SP + 'fork_rc3/v19/'; OUT = D19 + 'v19_noaudio.mp4'
X1 = 700; GF1 = 720 / 860
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['CHASE THE LOOT'], accent=0, sub='OR PLANT THE TREE?', sub_color=(140, 230, 110))
DUR = 10.0; N = int(round(DUR * FPS))
DIV = 70                                              # divider strip (was 50) holds a 44-48px line
P1 = HB + 14; PH = (1500 - P1 - DIV) // 2; P2 = P1 + PH + DIV   # panel tops
GF = {}
def panel_bg(name, x0, gfrac):
    k = (W + x0) / 1920; ww, hh = int(1920 * k), int(1080 * k)
    fr = bg_frames(name, (ww, hh), step=2); y0 = hh - PH
    GF[name + str(x0)] = int(gfrac * hh) - y0
    return [f.crop((x0, y0, x0 + W, y0 + PH)) for f in fr]
BG1 = panel_bg('found_hd.gif', X1, GF1); BG2 = panel_bg('found_hd.gif', 60, 720 / 860)
GL1, GL2 = GF['found_hd.gif' + str(X1)], GF['found_hd.gif60']    # ground line inside each panel
K = 4                                                  # Joy 3x -> 4x (integer)
RUN = seq(PL + 'race/joy_run', K, 1, 9)
FALL = []
for p in sorted(glob.glob(SP + 'fork2/joy_fall/*.png'))[1:9]:
    im = Image.open(p).convert('RGBA'); a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([0, 81, 92, 92], fill=0); im.putalpha(a); FALL.append(up(im, K))
PLANT = seq(SP + 'fork2/joy_plant', K, 1, 13)
IDLE = idle('joy', K)
LEDGE = up(crop(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA')), 3)
SAP = up(crop(Image.open(SP + 'fork2/sapling/00.png').convert('RGBA')), 3)
SMALL = up(crop(Image.open(SP + 'fork2/smalltree/01.png').convert('RGBA')), 4)
BIG = up(crop(Image.open(SP + 'fork2/bigtree/00.png').convert('RGBA')), 3)
LOOT = gummy('cre', 4)                                 # loot: a sugared product gummy (was the gold gummy, read as a gold nugget)
GS = [gummy(k, 2) for k in ['mush', 'mel', 'cre']]
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
GS.append(up(acv_gummy_strong(), 2))                  # ACV gummy with the gummy shine
_b = Image.open(A + 'found_hd.gif'); _b.seek(0); _b = _b.convert('RGB'); _k = H / _b.height
_b = _b.resize((int(_b.width * _k), H), Image.NEAREST); _b = _b.crop(((_b.width - W) // 2, 0, (_b.width - W) // 2 + W, H))
BACK = ImageEnhance.Brightness(_b.filter(ImageFilter.GaussianBlur(8))).enhance(0.35).convert('RGBA')
EDGE = 770; X0J = 150
# top lane: (start, run time, fall time); later runs/falls quicker; first fall gets a MISSED! stamp
CYC = [(0.0, 2.2, 1.0), (3.6, 1.7, 0.8), (6.6, 1.7, 0.8)]
T_MISS = CYC[0][0] + CYC[0][1] + 0.35   # as she drops into the pit
# bottom lane: plant 0-1.6s, sapling 1.6, small tree 3.0, big tree 4.4, gummies drop 5.2-9.3
T_SAP, T_SMALL, T_BIG = 1.6, 3.0, 4.4
T_Q = 4.8                                             # divider switches from the comment prompt to WHICH ONE ARE YOU?
T_FADE = DUR - 4 / FPS                                # last 4 frames: bottom lane fades back to bare ground (loop)
rng = random.Random(11)
drops = []; td = 5.2
while td < 9.3:
    drops.append((td, rng.choice(GS), rng.uniform(-60, 120), rng.uniform(-140, 140))); td += rng.uniform(0.28, 0.42)
events = []
for (c, rt, ft) in CYC:
    events += [(c + rt, 'jump'), (c + rt + 0.3, 'whoosh_8bit'), (c + rt + ft + 0.05, 'poof')]
events += [(T_MISS, 'buzz_8bit'), (T_SAP, 'twinkle'), (T_SMALL, 'chime'), (T_BIG, 'chime'), (T_BIG, 'twinkle'), (T_Q, 'ding_8bit')]
events += [(drops[i][0] + 0.45, 'coin_8bit') for i in (0, 3, 7, 12) if i < len(drops)]   # coins on a few landings only (no coin metronome)
def stamp(img, cx, cy, txt, size, col, a, sc=1.0):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); fs = int(size * sc); f = F(fs)
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle([cx - tw / 2 - 24, cy - fs / 2 - 18, cx + tw / 2 + 24, cy + fs / 2 + 18], 16, fill=(16, 8, 14, int(a * 0.9)), outline=col + (a,), width=6)
    ctext(d, cx, cy - fs / 2, txt, f, col, 9, a); img.alpha_composite(L)
def label(img, x, y, txt, col):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); f = F(46); tw = d.textlength(txt, font=f)
    d.rounded_rectangle([x, y, x + tw + 36, y + 46 + 28], 14, fill=(14, 10, 24, 215), outline=col + (255,), width=4)
    d.text((x + 18, y + 14), txt, font=f, fill=col + (255,), stroke_width=6, stroke_fill=(10, 6, 18)); img.alpha_composite(L)
PREV = [int(v) for v in os.environ.get('PREV', '').split(',') if v]
wr = None
for f in range(N):
    t = f / FPS
    img = BACK.copy()
    # ---------- panel 1: chase the loot (forest meadow, cliff + dark drop on the right)
    p1 = BG1[int(t * 5) % len(BG1)].copy()
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, min(255, 150 + int((y - GL1 + 60) * 1.2)))) for y in range(GL1 - 60, PH, 4)])
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, int(150 * (y - (GL1 - 110)) / 50))) for y in range(GL1 - 110, GL1 - 60, 4)])
    p1.alpha_composite(LEDGE, (EDGE + 30 - LEDGE.width, GL1 - 18))
    c0 = max([c for c in CYC if c[0] <= t], key=lambda c: c[0])
    cs, rt, ft = c0; u = t - cs
    pop_in = None
    if u < rt:
        k = u / rt; jx = X0J + (EDGE - X0J) * k; jy = GL1; spr = RUN[int(u * 14) % 8]
    elif u < rt + ft:
        v = (u - rt) / ft; spr = FALL[min(7, int(v * 10))]
        jx = EDGE + 120 * v; jy = GL1 + 900 * max(0, v - 0.25) ** 2
    else:
        jx, jy = X0J, GL1; spr = RUN[0]; pop_in = u - rt - ft          # pops back in at the start
    # loot gummy keeps floating just out of reach
    if u < rt + ft + 0.3:
        gx = min(EDGE + 200, X0J + 190 + (EDGE - X0J) * min(1, u / rt) + 40 * max(0, u - rt))
    else: gx = X0J + 190
    gy = GL1 - 215 + 14 * math.sin(t * 5)
    layer(p1, lambda d: [d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 150, 190, 22)) for r in (84, 66, 50)])
    p1.alpha_composite(LOOT, (int(gx - LOOT.width / 2), int(gy - LOOT.height / 2)))
    layer(p1, lambda d: [d.rectangle([gx + 52 * math.cos(t * 3 + q * 2.1) - 4, gy + 40 * math.sin(t * 3 + q * 2.1) - 4, gx + 52 * math.cos(t * 3 + q * 2.1) + 4, gy + 40 * math.sin(t * 3 + q * 2.1) + 4], fill=(255, 240, 250, 220)) for q in range(3)])
    if pop_in is not None and pop_in < 0.4:
        sc = min(1, pop_in / 0.12); spr = up(spr, max(0.2, sc)) if sc < 1 else spr
        v = pop_in / 0.4
        layer(p1, lambda d: d.ellipse([X0J - 40 - 80 * v, GL1 - 150, X0J + 40 + 80 * v, GL1], outline=(255, 255, 255, int(200 * (1 - v))), width=6))
    p1.alpha_composite(spr, (int(jx - spr.width / 2), int(jy - spr.height * 78 / 92)))
    if rt - 0.1 < u < rt + 0.5:
        ctext(ImageDraw.Draw(p1), jx + 80, jy - 300, '!', F(72), (255, 80, 80), 8)
    pass
    # ---------- panel 2: plant the tree
    p2 = BG2[int(t * 5) % len(BG2)].copy()
    q2 = Image.new('RGBA', p2.size, (0, 0, 0, 0))          # tree + gummies (fade out together at the loop)
    TX = 480
    if t >= T_SAP:
        if t < T_SMALL: tr = SAP; sc = min(1, (t - T_SAP) / 0.3)
        elif t < T_BIG: tr = SMALL; sc = min(1, 0.6 + (t - T_SMALL) / 0.4)
        else: tr = BIG; sc = min(1, 0.7 + (t - T_BIG) / 0.5)
        tim = up(tr, sc) if sc < 1 else tr
        layer(q2, lambda d: d.ellipse([TX - tim.width * 0.4, GL2 - 14, TX + tim.width * 0.4, GL2 + 14], fill=(0, 0, 0, 70)))
        q2.alpha_composite(tim, (int(TX - tim.width / 2), int(GL2 - tim.height + 6)))
        for ts_ in (T_SAP, T_SMALL, T_BIG):
            if ts_ <= t < ts_ + 0.6:
                v = (t - ts_) / 0.6
                layer(q2, lambda d: [d.rectangle([TX + math.cos(a) * (40 + 160 * v) - 5, GL2 - 120 + math.sin(a) * (40 + 120 * v) - 5, TX + math.cos(a) * (40 + 160 * v) + 5, GL2 - 120 + math.sin(a) * (40 + 120 * v) + 5], fill=(255, 245, 170, int(255 * (1 - v)))) for a in [k * 0.785 for k in range(8)]])
    landed = 0
    for i, (t0, g, dx, sx) in enumerate(drops):
        if t < t0: continue
        uu = t - t0
        x = TX + dx + sx * min(uu, 0.45) * 0.3; y0 = GL2 - 330
        if uu < 0.45:
            y = y0 + (uu / 0.45) ** 2 * 300; q2.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        else: landed += 1
    for i, (t0, g, dx, sx) in enumerate(drops[:landed]):
        row = i // 5; col = i % 5
        x = 690 + col * 34 + (row % 2) * 17; y = GL2 - 18 - row * 28
        q2.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    if landed:
        lu = t - (drops[landed - 1][0] + 0.45); cz = int(52 + 10 * max(0, 1 - lu / 0.12))
        ctext(ImageDraw.Draw(q2), 770, GL2 - 190 - cz / 2, f'x{landed}', F(cz), (255, 214, 60), 8)
    if t >= T_FADE:
        q2.putalpha(q2.getchannel('A').point(lambda p: int(p * max(0, 1 - (t - T_FADE + 1 / FPS) / (DUR - T_FADE + 1 / FPS)))))
    p2.alpha_composite(q2)
    if t < 1.6: spr2 = PLANT[min(11, int(t / 1.6 * 12))]
    else: spr2 = IDLE[int(t * 8) % len(IDLE)]
    if t >= T_FADE: spr2 = PLANT[0]                         # back to the frame-0 pose for the loop
    p2.alpha_composite(spr2, (int(180 - spr2.width / 2), int(GL2 - 78 * K)))
    pass
    # ---------- compose
    img.alpha_composite(p1, (0, P1)); img.alpha_composite(p2, (0, P2))
    d = ImageDraw.Draw(img)
    d.rectangle([0, P1 + PH, W, P2], fill=(14, 10, 24))
    if T_MISS <= t < T_MISS + 0.85:
        uu = t - T_MISS; stamp(img, 470, P1 + 150, 'MISSED!', 72, (255, 70, 60), int(255 * min(1, (T_MISS + 0.85 - t) / 0.15)), 1.2 - 0.2 * min(1, uu / 0.1))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(L); cy = P1 + PH + DIV / 2
    if t < T_Q:
        parts = [('COMMENT ', (255, 255, 255)), ('LOOT', (255, 214, 60)), (' OR ', (255, 255, 255)), ('TREE', (140, 230, 110))]; fs = F(44)
        tw = sum(dd.textlength(p, font=fs) for p, _ in parts); x = W / 2 - tw / 2
        for p, col in parts:
            dd.text((x, cy - 22), p, font=fs, fill=col, stroke_width=6, stroke_fill=(10, 6, 18)); x += dd.textlength(p, font=fs)
    else:
        sc = 1.15 - 0.15 * min(1, (t - T_Q) / 0.1); fs = int(48 * sc)
        ctext(dd, W / 2, cy - fs / 2, 'WHICH ONE ARE YOU?', F(fs), (255, 255, 255), 7)
    pass
    if f in (40, 150, 260): img.convert('RGB').save('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/hookmock/loot/'+f'clean_{f}.png')
    if f > 260: sys.exit()
    if f in PREV: img.convert('RGB').save(D19 + f'p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in sorted(events)]}, open(D19 + 'v19_events.json', 'w'))
print('done', len(drops), 'P1', P1, 'PH', PH, 'P2', P2, 'ground', GL1, GL2)
