import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
# rc3 recut of #19 (source fork_c2/v19/r19.py, run with X1=700). Bennett #19: no castle, top panel is the forest too (kept).
D19 = SP + 'fork_n3/v19/'; OUT = D19 + 'v19_noaudio.mp4'
X1 = 700; GF1 = 720 / 860
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade, _fit, X0 as HX0, X1 as HX1
# Oct 29: soft fade, no box. Line 1 gold (= top lane), line 2 green (= bottom lane): the colours tell viewers which scene is which,
# so the LOOT/TREE labels and the divider text are cut.
HLINES = ['CHASE THE LOOT', 'OR PLANT THE TREE?']
HOOK, HB = hook_fade(HLINES, accent=None)
_f, _s = _fit(HLINES, HX1 - HX0 - 20, 64, 40); _lh = int(_s * 1.32); _hd = ImageDraw.Draw(HOOK)
for _i, (_l, _c) in enumerate(zip(HLINES, [(255, 214, 60), (140, 230, 110)])):
    _w = _hd.textlength(_l, font=_f); _hd.text((W / 2 - _w / 2, 286 + _i * _lh), _l, font=_f, fill=_c, stroke_width=6, stroke_fill=(12, 8, 20))
DUR = 10.0; N = int(round(DUR * FPS))
# Oct 29 full-bleed: two scenes stacked edge to edge filling the whole frame (no blurred/dimmed backdrop), 10px seam, no divider text
SEAM = 920; SL = 10
P1, PH1 = 0, SEAM - SL // 2; P2, PH2 = SEAM + SL // 2, H - SEAM - SL // 2
PH = PH1
def panel_bg(name, x0, k, ground_y, ph, gfrac=720 / 860):
    # scene at scale k, crop x0..x0+W, ground line placed at panel y=ground_y; rows past the image bottom continue the
    # forest floor (mirrored bottom rows) and darken a little toward the frame edge
    ww, hh = int(1920 * k), int(1080 * k); fr = bg_frames(name, (ww, hh), step=2)
    y0 = int(gfrac * hh) - ground_y; out = []
    for f in fr:
        c = f.crop((x0, max(0, y0), x0 + W, min(hh, y0 + ph))); p = Image.new('RGBA', (W, ph), (0, 0, 0, 255)); p.alpha_composite(c, (0, max(0, -y0)))
        yb = hh - y0
        if yb < ph:
            yb = int(1000 * k) - y0      # forest floor continues from native y1000 with plain meadow grass (native x700-1500, y925-985), mirror-tiled both ways
            tb = f.crop((int(700 * k), int(925 * k), int(1500 * k), int(985 * k))); tbf = tb.transpose(Image.FLIP_LEFT_RIGHT)
            row = Image.new('RGBA', (W, tb.height)); xx = 0; q = 0
            while xx < W: row.paste(tb if q % 2 == 0 else tbf, (xx, 0)); xx += tb.width; q += 1
            rowf = row.transpose(Image.FLIP_TOP_BOTTOM)
            ext = Image.new('RGBA', (W, ph - yb + 40)); y = 0; kk = 0
            while y < ext.height: ext.paste(row if kk % 2 == 0 else rowf, (0, y)); y += row.height; kk += 1
            m = Image.new('L', (1, ext.height), 255)
            for yy in range(40): m.putpixel((0, yy), int(255 * yy / 40))
            ext.putalpha(m.resize(ext.size)); p.alpha_composite(ext, (0, yb - 40))
            g = Image.new('L', (1, ph), 0)
            for yy in range(yb - 40, ph): g.putpixel((0, yy), int(150 * min(1, max(0, (yy - yb + 40) / 320))))
            sh = Image.new('RGBA', (W, ph), (6, 10, 8, 255)); sh.putalpha(g.resize((W, ph))); p.alpha_composite(sh)
        out.append(p)
    return out
GL1, GL2 = 820, 1460 - P2                               # ground lines: top lane y820 (screen), bottom lane y1460 (screen)
BG1 = panel_bg('found_hd.gif', X1, 1.0, GL1, PH1); BG2 = panel_bg('found_hd.gif', 300, 1.0, GL2, PH2)
K = 4                                                  # Joy 3x -> 4x (integer)
RUN = seq(PL + 'race/joy_run', K, 1, 9)
FALL = []
for p in sorted(glob.glob(SP + 'fork2/joy_fall/*.png'))[1:9]:
    im = Image.open(p).convert('RGBA'); a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([0, 81, 92, 92], fill=0); im.putalpha(a); FALL.append(up(im, K))
PLANT = seq(SP + 'fork2/joy_plant', K, 1, 13)
IDLE = idle('joy', K)
# Oct 29 (Bennett #19): the top Joy meets a different disaster each run. Existing PixelLab assets only:
# joy_ko tumble (pixellab/king/joy_ko, same 64px body as the run cycle), King Slime (pixellab/king/king_idle + king_land, 3x),
# landing dust (king/dust_cands/00), floor spikes (pixellab/plat/spike_cands/04, spike rows only, 5x).
def _ko(p):
    im = Image.open(p).convert('RGBA'); return up(im, K), im.getbbox()[3] * K
KO = [_ko(p) for p in sorted(glob.glob(PL + 'king/joy_ko/*.png'))]
KS = 3
KIDLE = seq(PL + 'king/king_idle', KS, 0); KLAND = seq(PL + 'king/king_land', KS, 0)
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
_sp = Image.open(PL + 'plat/spike_cands/04.png').convert('RGBA').crop((20, 9, 84, 31)); SPK = up(_sp, 5)
LEDGE = up(crop(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA')), 3)
SAP = up(crop(Image.open(SP + 'fork2/sapling/00.png').convert('RGBA')), 3)
SMALL = up(crop(Image.open(SP + 'fork2/smalltree/01.png').convert('RGBA')), 4)
BIG = up(crop(Image.open(SP + 'fork2/bigtree/00.png').convert('RGBA')), 3)
LOOT = gummy('cre', 4)                                 # loot: a sugared product gummy (was the gold gummy, read as a gold nugget)
GS = [gummy(k, 2) for k in ['mush', 'mel', 'cre']]
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
GS.append(up(acv_gummy_strong(), 2))                  # ACV gummy with the gummy shine
EDGE = 770; X0J = 150
# top lane: (start, run time, fall time); later runs/falls quicker; first fall gets a MISSED! stamp
# Oct 29: three different disasters (was the same cliff fall three times), no MISSED! stamp. Each ends with Joy popping back in at the start.
# A cliff: run 0-2.1s, off the edge, fall to 3.0, pop in 3.0
# B King Slime: run from 3.4, he drops in front of her at 3.95 (squish, shake), roars at 4.42: the roar blasts her back
#   (tumble, flat on her back 4.95, stars) and he slurps up the loot gummy; he hops off at 5.5; poof 5.9, pop in 5.95
# C spikes: run from 6.25, spikes shoot up at 6.72 right in front of her, she runs into them and is launched out of the top of the frame at 6.9, a beat later she
#   drops back flat at 8.45 (dust, stars); poof 9.35, pop in 9.4 (ends in the frame-0 pose for the loop)
TA_RT, TA_FT = 2.1, 0.9
TB0, TB_LAND, TB_ROAR, TB_FLAT, TB_HOP, TB_POOF = 3.4, 3.95, 4.42, 4.95, 5.5, 5.9
TC0, TC_SPK, TC_HIT, TC_TOP, TC_DROP, TC_FLAT, TC_POOF = 6.25, 6.72, 6.9, 7.35, 8.15, 8.45, 9.35
SPEED = 330.0; KX = 630; KBOT = GL1 + 14; SX0 = 420
# bottom lane: plant 0-1.6s, sapling 1.6, small tree 3.0, big tree 4.4, gummies drop 5.2-9.3
T_SAP, T_SMALL, T_BIG = 1.6, 3.0, 4.4
T_Q = 4.8                                             # divider switches from the comment prompt to WHICH ONE ARE YOU?
T_FADE = DUR - 4 / FPS                                # last 4 frames: bottom lane fades back to bare ground (loop)
rng = random.Random(11)
drops = []; td = 5.2
while td < 9.3:
    drops.append((td, rng.choice(GS), rng.uniform(-60, 120), rng.uniform(-140, 140))); td += rng.uniform(0.28, 0.42)
events = []
events += [(TA_RT, 'jump'), (TA_RT + 0.3, 'whoosh_8bit'), (TA_RT + TA_FT + 0.05, 'poof'),
           (TB_LAND - 0.3, 'whoosh_8bit'), (TB_LAND, 'boom'), (TB_ROAR, 'punch'), (TB_FLAT, 'stomp_8bit'), (TB_HOP, 'jump'), (TB_POOF, 'poof'),
           (TC_SPK, 'sword_shing'), (TC_HIT, 'boing'), (TC_DROP, 'whoosh_8bit'), (TC_FLAT, 'stomp_8bit'), (TC_POOF, 'poof'),
           (T_SAP, 'twinkle'), (T_SMALL, 'chime'), (T_BIG, 'chime'), (T_BIG, 'twinkle')]   # Oct 29: T_Q ding cut with the divider text it cued
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
wr = Writer(OUT) if not PREV else None
for f in range(N):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    # ---------- panel 1: chase the loot (forest meadow, cliff + dark drop on the right)
    p1 = BG1[int(t * 5) % len(BG1)].copy()
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, min(255, 150 + int((y - GL1 + 60) * 1.2)))) for y in range(GL1 - 60, PH, 4)])
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, int(150 * (y - (GL1 - 110)) / 50))) for y in range(GL1 - 110, GL1 - 60, 4)])
    p1.alpha_composite(LEDGE, (EDGE + 30 - LEDGE.width, GL1 - 18))
    # Oct 29 top lane: a different disaster each run (cliff, King Slime, spikes)
    gy = GL1 - 215 + 14 * math.sin(t * 5); gsc = 1.0; gal = True
    joy = None; bang = None; stars = None; shake = 0; fx = []; king = None; kshadow = None; spk_h = 0; jshadow = None
    pop_t = None
    def run_spr(tt): return RUN[int(tt * 14) % 8]
    if t < TA_RT + TA_FT:                                   # A: off the cliff
        u = t
        if u < TA_RT:
            jx = X0J + (EDGE - X0J) * u / TA_RT; joy = ('run', run_spr(u), jx, GL1)
        else:
            v = (u - TA_RT) / TA_FT; jx = EDGE + 120 * v; jy = GL1 + 900 * max(0, v - 0.25) ** 2
            joy = ('run', FALL[min(7, int(v * 10))], jx, jy)
        gx = min(EDGE + 200, X0J + 190 + (EDGE - X0J) * min(1, u / TA_RT) + 40 * max(0, u - TA_RT))
        if TA_RT - 0.1 < u < TA_RT + 0.5: bang = (joy[2] + 80, joy[3] - 300)
    elif t < TB0: pop_t = t - (TA_RT + TA_FT)
    elif t < TB_POOF + 0.05:                                 # B: King Slime
        JB = X0J + SPEED * (TB_LAND + 0.05 - TB0); JL = JB - 210
        if t < TB_LAND + 0.05: jx = X0J + SPEED * (t - TB0); joy = ('run', run_spr(t - TB0), jx, GL1)
        elif t < TB_ROAR: joy = ('ko', 0, JB, GL1)
        elif t < TB_FLAT:
            v = (t - TB_ROAR) / (TB_FLAT - TB_ROAR)
            joy = ('ko', min(7, 2 + int(v * 6)), JB - 210 * v, GL1 - 170 * 4 * v * (1 - v)); jshadow = JB - 210 * v
        elif t < TB_POOF:
            b = min(1, (t - TB_FLAT) / 0.18); joy = ('flat', 8, JL, GL1 - 26 * math.sin(math.pi * b))
            if t - TB_FLAT < 0.5: fx.append(('dust', JL, GL1, (t - TB_FLAT) / 0.5, 1.6))
            stars = (JL, GL1 - 210)
        else: fx.append(('dust', JL, GL1, (t - TB_POOF) / 0.3, 2.2))
        if TB_LAND <= t < TB_ROAR: bang = (JB + 70, GL1 - 300)
        # gummy: leads her in, hovers in front of the King, then he slurps it up during the roar
        gx0 = min(KX - 110, X0J + 190 + SPEED * (min(t, TB_LAND) - TB0))
        if t < TB_ROAR: gx = gx0
        elif t < TB_ROAR + 0.22:
            v = (t - TB_ROAR) / 0.22; gx = gx0 + (KX - 6 - gx0) * v; gy = gy + (KBOT - 150 - gy) * v; gsc = 1 - 0.8 * v
        else: gal = False
        # the King: drops from the sky with a growing shadow, squish-lands, roars, then hops off
        if TB_LAND - 0.5 <= t < TB_HOP + 0.35:
            if t < TB_LAND: kshadow = min(1, (t - (TB_LAND - 0.5)) / 0.5)
            elif t < TB_HOP: kshadow = 1
            else: kshadow = max(0, 1 - (t - TB_HOP) / 0.3)
        if TB_LAND - 0.32 <= t < TB_LAND:
            u = (t - (TB_LAND - 0.32)) / 0.32; king = (KIDLE[0], -60 + (KBOT + 60) * u * u)
        elif TB_LAND <= t < TB_HOP:
            u = t - TB_LAND; k = int(u * 15); king = (KLAND[k] if k < len(KLAND) else KIDLE[int(u * 10) % len(KIDLE)], KBOT)
            if u < 0.7: fx.append(('dust', KX, KBOT + 10, u / 0.7, 3.0))
            if u < 0.4: shake = int(22 * (1 - u / 0.4))
        elif TB_HOP <= t < TB_HOP + 0.35:
            v = (t - TB_HOP) / 0.35; king = (KIDLE[4], KBOT - 1500 * v * v)
    elif t < TC0: pop_t = t - (TB_POOF + 0.05)
    elif t < TC_POOF + 0.05:                                 # C: spikes
        JC = X0J + SPEED * (TC_HIT - TC0); JF = JC - 40
        if t < TC_HIT: jx = X0J + SPEED * (t - TC0); joy = ('run', run_spr(t - TC0), jx, GL1)
        elif t < TC_TOP:
            tt = t - TC_HIT      # 0.2s yelp-hop off the spikes, then rockets out of the top of the frame spinning
            if tt < 0.2: joy = ('ko', 3, JC + 10 * tt / 0.2, GL1 - 230 * (1 - (1 - tt / 0.2) ** 2))
            else: joy = ('ko', 3 + int((tt - 0.2) * 20) % 5, JC + 10 + 40 * (tt - 0.2), GL1 - 230 - 2600 * (tt - 0.2))
            jshadow = JC
        elif t < TC_DROP: pass                                # out of the top of the frame
        elif t < TC_FLAT:
            v = (t - TC_DROP) / (TC_FLAT - TC_DROP); joy = ('flat', 8, JF, -420 + (GL1 + 420) * v * v)
        elif t < TC_POOF:
            b = min(1, (t - TC_FLAT) / 0.16); joy = ('flat', 8, JF, GL1 - 20 * math.sin(math.pi * b))
            if t - TC_FLAT < 0.5: fx.append(('dust', JF, GL1, (t - TC_FLAT) / 0.5, 1.8))
            if t - TC_FLAT < 0.25: shake = int(12 * (1 - (t - TC_FLAT) / 0.25))
            stars = (JF, GL1 - 210)
        else: fx.append(('dust', JF, GL1, (t - TC_POOF) / 0.3, 2.2))
        if TC_DROP - 0.45 <= t < TC_FLAT: jshadow = JF
        if TC_SPK <= t < TC_HIT + 0.3: bang = (JC + 80, GL1 - 300)
        gxh = X0J + 190 + SPEED * (TC_HIT - TC0)
        gx = X0J + 190 + SPEED * (t - TC0) if t < TC_HIT else min(gxh + 60, gxh + 120 * (t - TC_HIT))
        if TC_SPK <= t < 7.75: spk_h = min(1, (t - TC_SPK) / 0.06)
        elif 7.75 <= t < 7.9: spk_h = 1 - (t - 7.75) / 0.15
    else: pop_t = t - (TC_POOF + 0.05)
    if pop_t is not None:
        joy = ('run', RUN[0], X0J, GL1); gx = X0J + 190
    # draw: shadows, King, spikes base slot, gummy, Joy, spikes, fx
    if kshadow:
        layer(p1, lambda d: d.ellipse([KX - 170 * kshadow, KBOT - 16 * kshadow, KX + 170 * kshadow, KBOT + 16 * kshadow], fill=(0, 0, 0, int(90 * kshadow))))
    if jshadow is not None:
        layer(p1, lambda d: d.ellipse([jshadow - 70, GL1 - 10, jshadow + 70, GL1 + 10], fill=(0, 0, 0, 70)))
    if king:
        kf, kb = king; p1.alpha_composite(kf, (int(KX - kf.width / 2), int(kb - 156 * KS)))
    if gal:
        lt = LOOT if gsc >= 1 else up(LOOT, gsc)
        if gsc >= 1: layer(p1, lambda d: [d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 150, 190, 22)) for r in (84, 66, 50)])
        p1.alpha_composite(lt, (int(gx - lt.width / 2), int(gy - lt.height / 2)))
        if gsc >= 1: layer(p1, lambda d: [d.rectangle([gx + 52 * math.cos(t * 3 + q * 2.1) - 4, gy + 40 * math.sin(t * 3 + q * 2.1) - 4, gx + 52 * math.cos(t * 3 + q * 2.1) + 4, gy + 40 * math.sin(t * 3 + q * 2.1) + 4], fill=(255, 240, 250, 220)) for q in range(3)])
    if joy:
        kind, spr, jx, jy = joy
        if kind == 'run':
            if pop_t is not None and pop_t < 0.4:
                sc = min(1, pop_t / 0.12); spr = up(spr, max(0.2, sc)) if sc < 1 else spr; v = pop_t / 0.4
                layer(p1, lambda d: d.ellipse([X0J - 40 - 80 * v, GL1 - 150, X0J + 40 + 80 * v, GL1], outline=(255, 255, 255, int(200 * (1 - v))), width=6))
            p1.alpha_composite(spr, (int(jx - spr.width / 2), int(jy - spr.height * 78 / 92)))
        else:
            im, bot = KO[spr]; yoff = 96 * K if kind == 'ko' else bot
            p1.alpha_composite(im, (int(jx - im.width / 2), int(jy - yoff)))
    if spk_h > 0:
        hh = max(1, int(SPK.height * spk_h)); sp = SPK.crop((0, 0, SPK.width, hh))
        layer(p1, lambda d: d.rectangle([SX0 - 6, GL1 - 4, SX0 + SPK.width + 6, GL1 + 8], fill=(20, 14, 12, 200)))
        p1.alpha_composite(sp, (SX0, GL1 + 4 - hh))
    for kind_, x_, y_, v_, s_ in fx:
        if 0 <= v_ < 1:
            du = up(DUST, s_ * (1 + 0.5 * v_)); du.putalpha(du.getchannel('A').point(lambda p: int(p * (1 - v_))))
            p1.alpha_composite(du, (int(x_ - du.width / 2), int(y_ - du.height + 12)))
    if stars:
        sx, sy = stars
        def _star(d, x, y, c):
            for (dx, dy) in ((0, 0), (-8, 0), (8, 0), (0, -8), (0, 8)): d.rectangle([x + dx - 5, y + dy - 5, x + dx + 5, y + dy + 5], fill=(20, 12, 20, 255))
            for (dx, dy) in ((0, 0), (-7, 0), (7, 0), (0, -7), (0, 7)): d.rectangle([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=c)
        layer(p1, lambda d: [_star(d, sx + 90 * math.cos(t * 7 + q * 2.094), sy + 24 * math.sin(t * 7 + q * 2.094), (255, 230, 90, 255)) for q in range(3)])
    if bang: ctext(ImageDraw.Draw(p1), bang[0], bang[1], '!', F(72), (255, 80, 80), 8)
    if shake:
        rs = random.Random(f); sh_ = p1.copy(); p1.paste((14, 10, 24, 255), (0, 0, W, PH1)); p1.paste(sh_, (rs.randint(-shake, shake), rs.randint(-shake, shake)))
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
    # ---------- compose
    img.alpha_composite(p1, (0, P1)); img.alpha_composite(p2, (0, P2))
    d = ImageDraw.Draw(img)
    img.alpha_composite(HOOK)
    if PREV:
        if f in PREV: img.convert('RGB').save(D19 + f'p_{f:03d}.png')
        if f >= max(PREV): sys.exit()
        continue
    wr.write(img)
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in sorted(events)]}, open(D19 + 'v19_events.json', 'w'))
print('done', len(drops), 'P1', P1, 'PH', PH, 'P2', P2, 'ground', GL1, GL2)
