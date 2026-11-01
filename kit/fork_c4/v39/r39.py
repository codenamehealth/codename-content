import sys, os, math, random, json
sys.path.insert(0, '../../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['THE SHORTCUT OR', 'THE LONG ROAD?'], accent=1)
TC0, TC1, BC0, BC1 = 280, 770, 300, 824
SS = 3; FOOT = 78 * SS
WALK = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'hollow-walk-side.gif')]
RUN = seq(PL + 'maze/anim/hollow_srun', SS)
PANIC = seq(PL + 'maze/anim/hollow_panic', SS)
VICF = [up(f.resize((92, 92), Image.NEAREST), 3) for f in gif_frames(A + 'hollow-victory.gif')]
STAIR = up(crop(Image.open('../../fork4/stair/00.png').convert('RGBA')), 3)
LILY = up(crop(Image.open('../../fork4/lilypad/02.png').convert('RGBA')), 2)
TOP0, BOT0, PH = 470, 972, 830
TOPBG = bg_frames('found_hd.gif', (W, PH), box=(380, 140, 1500, 1000), step=2, bright=0.8)
BOTBG = bg_frames('vit_hd.gif', (W, PH), box=(700, 110, 1700, 878), step=2, bright=1.0)
# shortcut geometry (panel coords)
GY = 700                       # ground line top panel
SX0, SX1, SY1 = 430, 650, 760
SWX, SWY = 760, 730           # swamp centre
def swamp_layer(t):
    L = Image.new('RGBA', (W // 3, PH // 3), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse([(SWX - 330) // 3, (SWY - 70) // 3, (SWX + 340) // 3, (SWY + 110) // 3], fill=(70, 48, 26, 255))
    d.ellipse([(SWX - 300) // 3, (SWY - 56) // 3, (SWX + 310) // 3, (SWY + 92) // 3], fill=(34, 44, 18, 255))
    d.ellipse([(SWX - 270) // 3, (SWY - 44) // 3, (SWX + 280) // 3, (SWY + 78) // 3], fill=(58, 70, 26, 255))
    d.ellipse([(SWX - 160) // 3, (SWY - 20) // 3, (SWX + 120) // 3, (SWY + 30) // 3], fill=(76, 88, 34, 255))
    rr = random.Random(int(t * 4))
    for k in range(8):
        bx = (SWX + rr.uniform(-200, 200)) // 3; by = (SWY + rr.uniform(-10, 40)) // 3
        d.ellipse([bx, by, bx + 3, by + 3], outline=(150, 180, 90, 255))
    for k in range(9):
        rx = (SWX - 250 + k * 62) // 3; d.line([(rx, (SWY - 20) // 3), (rx + (k % 2), (SWY - 50 - (k % 3) * 8) // 3)], fill=(60, 90, 30, 255), width=1)
    return up(L, 3)
# long road geometry: stairs from bottom-left up to the castle gate
NST = 9; ST0 = (135, 800); ST1 = (590, 560)
STEPS = [(ST0[0] + (ST1[0] - ST0[0]) * i / (NST - 1), ST0[1] + (ST1[1] - ST0[1]) * i / (NST - 1)) for i in range(NST)]
LAND1 = 880                          # right end of the top landing (panel x)
TROPHY_X = 790                       # trophy stands on the landing at the end of the stairs
GUMS = [(2, 'acv'), (4, 'cre'), (6, 'mush'), (8, 'mel')]
T_START = 0.3; T_SLIDE = 2.2; T_SPLASH = 3.0
T_TOP = 9.4; END = 12.6
def long_pos(t):
    u = max(0, min(1, (t - T_START) / (T_TOP - T_START)))
    f = u * (NST - 1); i = int(f); fr = f - i
    if i >= NST - 1: return STEPS[-1][0] + 50, STEPS[-1][1]
    x0, y0 = STEPS[i]; x1, y1 = STEPS[i + 1]
    hop = math.sin(math.pi * fr) * 10
    return x0 + (x1 - x0) * fr, y0 + (y1 - y0) * min(1, fr * 1.6) - hop
def build_stairs():
    """one solid masonry staircase (side view) rising to a stone landing; continuous brick courses, lit treads, ground shadow"""
    L = Image.new('RGBA', (W // 3, PH // 3), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    sw = (STEPS[1][0] - STEPS[0][0]) / 3; bot = PH // 3
    xs = [sx / 3 - sw / 2 for sx, sy in STEPS]; ys = [sy / 3 for sx, sy in STEPS]
    xl = xs[0]; xr = LAND1 / 3
    # stepped silhouette
    poly = [(xl, bot)]
    for i in range(NST):
        poly += [(xs[i], ys[i]), ((xs[i + 1] if i + 1 < NST else xr), ys[i])]
    poly += [(xr, bot)]
    STONE, MORTAR, DARK, LIGHT, OUT = (132, 128, 142, 255), (102, 98, 114, 255), (88, 84, 100, 255), (196, 192, 204, 255), (40, 34, 52, 255)
    d.polygon(poly, fill=STONE)
    mask = Image.new('L', L.size, 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    B = Image.new('RGBA', L.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(B)
    y0 = int(min(ys))
    for r, yy in enumerate(range(y0 + 7, bot, 7)):
        bd.line([(xl, yy), (xr, yy)], fill=MORTAR)
        for xx in range(int(xl) + (6 if r % 2 else 0), int(xr), 12): bd.line([(xx, yy - 6), (xx, yy - 1)], fill=MORTAR)
        if r % 3 == 1:
            for xx in range(int(xl) + 3 + (r * 5) % 12, int(xr) - 4, 37): bd.rectangle([xx, yy - 5, xx + 7, yy - 2], fill=(144, 140, 154, 255))
    L.paste(B, (0, 0), Image.composite(B.getchannel('A'), Image.new('L', L.size, 0), mask))
    # treads: light cap + dark lip, riser shade
    for i in range(NST):
        xa = xs[i]; xb = xs[i + 1] if i + 1 < NST else xr
        d.rectangle([xa, ys[i], xb, ys[i] + 1], fill=LIGHT)
        d.line([(xa, ys[i] + 2), (xb, ys[i] + 2)], fill=DARK)
        d.line([(xa, ys[i]), (xa, (ys[i - 1] if i else bot))], fill=OUT)
    # landing cornice
    d.rectangle([xs[-1], ys[-1] - 1, xr + 2, ys[-1] + 3], fill=LIGHT); d.line([(xs[-1], ys[-1] + 4), (xr + 2, ys[-1] + 4)], fill=OUT)
    d.line([(xr, ys[-1]), (xr, bot)], fill=OUT); d.rectangle([xr - 3, ys[-1] + 5, xr - 1, bot], fill=DARK)
    d.line(poly[:-1], fill=OUT)
    # contact shadow where the base meets the courtyard
    return up(L, 3)
def build_trophy():
    """gold pixel trophy on a stone plinth (native 30 x 44, drawn at 4x)"""
    T = Image.new('RGBA', (30, 46), (0, 0, 0, 0)); d = ImageDraw.Draw(T)
    O, D, G, Lg, Wt = (60, 30, 8, 255), (186, 112, 18, 255), (250, 196, 46, 255), (255, 236, 140, 255), (255, 255, 240, 255)
    # handles
    d.ellipse([1, 4, 10, 15], outline=O, width=3); d.ellipse([2, 5, 9, 14], outline=D, width=1)
    d.ellipse([19, 4, 28, 15], outline=O, width=3); d.ellipse([20, 5, 27, 14], outline=D, width=1)
    # bowl
    d.polygon([(5, 2), (24, 2), (23, 10), (20, 16), (15, 19), (14, 19), (9, 16), (6, 10)], fill=O)
    d.polygon([(6, 3), (23, 3), (22, 10), (19, 15), (15, 18), (14, 18), (10, 15), (7, 10)], fill=G)
    d.polygon([(16, 3), (23, 3), (22, 10), (19, 15), (15, 18)], fill=D)
    d.line([(8, 4), (9, 11)], fill=Lg, width=2); d.point((9, 5), fill=Wt)
    d.rectangle([5, 1, 24, 3], fill=O); d.rectangle([6, 2, 23, 2], fill=Lg)
    # stem + base
    d.rectangle([12, 19, 17, 25], fill=O); d.rectangle([13, 19, 16, 24], fill=G); d.line([(15, 19), (15, 24)], fill=D)
    d.rectangle([9, 25, 20, 28], fill=O); d.rectangle([10, 26, 19, 27], fill=G); d.line([(16, 26), (19, 26)], fill=D)
    d.rectangle([7, 28, 22, 32], fill=O); d.rectangle([8, 29, 21, 31], fill=D); d.line([(8, 29), (14, 29)], fill=G)
    # star emblem on the bowl
    d.point([(14, 8), (13, 9), (14, 9), (15, 9), (14, 10)], fill=Wt)
    # stone plinth it stands on
    S1, S2, S3 = (150, 146, 160, 255), (110, 106, 122, 255), (200, 196, 208, 255)
    d.rectangle([4, 32, 25, 45], fill=(40, 34, 52, 255)); d.rectangle([5, 33, 24, 44], fill=S1)
    d.rectangle([5, 33, 24, 34], fill=S3); d.rectangle([21, 35, 24, 44], fill=S2); d.line([(5, 39), (24, 39)], fill=S2)
    return up(T, 4)
TROPHY = build_trophy()
STAIRS_IMG = build_stairs()
BACK = bg_frames('vit_hd.gif', (W, H), box=(900, 0, 1508, 1080), step=1000, bright=0.45, blur=10)[0]
W_ = Writer('v39_noaudio.mp4'); ev = []
got = set()
for f in range(int(END * FPS)):
    t = f / FPS
    LOOP = t >= END - 0.3            # last 0.3s: cut back to the opening state so the reel loops
    if LOOP: t = 0.0
    img = BACK.copy()
    # ---- top panel: the shortcut
    P = TOPBG[int(t * 6) % len(TOPBG)].copy(); P.alpha_composite(swamp_layer(t))
    for k, lx in enumerate([620, 700, 960]): P.alpha_composite(LILY, (lx, SWY - 8 + 18 * (k % 2)))
    if t < T_SLIDE:
        x = 140 + (SX0 - 140) * max(0, (t - T_START)) / (T_SLIDE - T_START) if t > T_START else 140; y = GY
        spr = RUN[int(t * 12) % 8] if t > T_START else WALK[0]
        P.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    elif t < T_SPLASH:
        u = (t - T_SLIDE) / (T_SPLASH - T_SLIDE); x = SX0 + (SWX - 60 - SX0) * u; y = GY + (SWY + 10 - GY) * (u ** 1.4)
        spr = RUN[int(t * 16) % 8].rotate(-22, resample=Image.NEAREST, expand=True)
        P.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    else:
        u = t - T_SPLASH; x = SWX - 60; sink = min(70, 40 + u * 4)
        spr = PANIC[int(t * 12) % 8]; cut = int(FOOT - sink)
        s2 = spr.copy(); a = s2.getchannel('A'); ImageDraw.Draw(a).rectangle([0, cut, s2.width, s2.height], fill=0); s2.putalpha(a)
        P.alpha_composite(s2, (int(x - spr.width / 2), int(SWY + 20 - FOOT)))
        layer(P, lambda d: (d.ellipse([x - 90, SWY + 20 - sink - 14, x + 90, SWY + 20 - sink + 30], outline=(160, 190, 90, 255), width=6)))
        if u < 0.6:
            layer(P, lambda d: [d.rectangle([x + math.cos(k) * (30 + u * 200), SWY - 40 - math.sin(abs(math.cos(k * 1.7))) * u * 180 + u * u * 200, x + math.cos(k) * (30 + u * 200) + 9, SWY - 31 - math.sin(abs(math.cos(k * 1.7))) * u * 180 + u * u * 200], fill=(120, 160, 60, 255)) for k in range(14)])
        if not any(e[1] == 'squish' for e in ev): ev.append((round(T_SPLASH, 3), 'squish')); ev.append((round(T_SPLASH + 0.05, 3), 'boing'))
        if u > 0.4: text_layer(P, [(x, TC0 + 120, 'STUCK!', 64, (190, 230, 120), 8, 255)])
    text_layer(P, [(270, TC0 + 16, 'THE SHORTCUT', 38, (255, 255, 255), 6, 255 if t < T_TOP + 1.0 else 0), (905, TC0 + 412, 'THE SWAMP', 26, (190, 230, 120), 5, 255)])
    img.alpha_composite(P.crop((0, TC0, W, TC1)), (0, TOP0))
    # ---- bottom panel: the long road
    Q = BOTBG[int(t * 6) % len(BOTBG)].copy()
    Q.alpha_composite(STAIRS_IMG)
    tb = int(STEPS[-1][1]); tx = TROPHY_X; won = t >= T_TOP
    def tglow(d):
        pr = 1 + 0.08 * math.sin(t * 5) + (0.35 * max(0, 1 - (t - T_TOP) / 0.6) if won else 0)
        for rr_, al in ((120, 40), (88, 60), (60, 80)):
            r2 = rr_ * pr; d.ellipse([tx - r2, tb - 110 - r2, tx + r2, tb - 110 + r2], fill=(255, 220, 110, al))
        if won:
            for k in range(10):
                a_ = (t - T_TOP) * 1.5 + k * math.pi / 5; r1, r2 = 70, 170
                d.polygon([(tx + r1 * math.cos(a_ - 0.08), tb - 120 + r1 * math.sin(a_ - 0.08)), (tx + r2 * math.cos(a_ - 0.13), tb - 120 + r2 * math.sin(a_ - 0.13)),
                           (tx + r2 * math.cos(a_ + 0.13), tb - 120 + r2 * math.sin(a_ + 0.13)), (tx + r1 * math.cos(a_ + 0.08), tb - 120 + r1 * math.sin(a_ + 0.08))], fill=(255, 236, 150, 70))
    layer(Q, tglow)
    Q.alpha_composite(TROPHY, (int(tx - TROPHY.width / 2), tb - TROPHY.height))
    def twinkle(d):
        for k, (ox, oy) in enumerate(((-38, -150), (40, -128), (-6, -186))):
            ph = (t * 1.6 + k * 0.33) % 1; s_ = int(10 * math.sin(math.pi * ph)) + 2
            X, Y = tx + ox, tb + oy; d.rectangle([X - s_, Y - 2, X + s_, Y + 2], fill=(255, 255, 230, 230)); d.rectangle([X - 2, Y - s_, X + 2, Y + s_], fill=(255, 255, 230, 230))
    layer(Q, twinkle)
    for (i, k) in GUMS:
        if k in got and not LOOP: continue
        gx, gy = STEPS[i]; g = gummy(k, 3); bob = int(6 * math.sin(t * 4 + i))
        layer(Q, lambda d, gx=gx, gy=gy: d.ellipse([gx - 40, gy - 240, gx + 40, gy - 160], fill=(255, 230, 150, 70)))
        Q.alpha_composite(g, (int(gx - g.width / 2), int(gy - 200 - g.height / 2 + bob)))
    if t < T_TOP:
        x, y = long_pos(t); spr = WALK[int(t * 8) % len(WALK)] if t > T_START else WALK[0]
        Q.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT + 4)))
        for (i, k) in GUMS:
            if not LOOP and k not in got and x >= STEPS[i][0] - 10:
                got.add(k); ev.append((round(t, 3), 'coin_8bit')); GOT_T = getattr(sys.modules[__name__], 'GOT_T', {}); GOT_T[k] = t; sys.modules[__name__].GOT_T = GOT_T
    else:
        u = t - T_TOP; vf = VICF[int(u * 8) % len(VICF)]
        x, y = long_pos(T_TOP)
        layer(Q, lambda d: [d.ellipse([x - r, y - 150 - r, x + r, y - 150 + r], outline=(255, 214, 60, max(0, 200 - r)), width=8) for r in range(int(u * 300) % 240, int(u * 300) % 240 + 1)])
        Q.alpha_composite(vf, (int(x - vf.width / 2), int(y - 78 * 3)))
        if not any(e[1] == 'victory' for e in ev): ev.append((round(T_TOP, 3), 'victory'))
        text_layer(Q, [(335, BC0 + 70, 'MADE IT!', 64, (255, 214, 60), 8, 255)])
    for k, tg in getattr(sys.modules[__name__], 'GOT_T', {}).items():
        if 0 <= t - tg < 0.9 and t < T_TOP:
            x, y = long_pos(tg); text_layer(Q, [(x, max(BC0 + 8, y - 270 - (t - tg) * 40), '+1 XP', 34, (255, 214, 60), 5, int(255 * min(1, (0.9 - (t - tg)) / 0.3)))])
    text_layer(Q, [(290, BC0 + 16, 'THE LONG ROAD', 38, (255, 214, 60), 6, 255), (880, BC0 + 62, 'THE CASTLE', 28, (255, 255, 255), 5, 255 if t < T_TOP else 0)])
    # XP counter on the long road
    n = 0 if LOOP else len(got); text_layer(Q, [(900, BC0 + 16, f'XP {n}/4', 34, (255, 255, 255), 5, 255)])
    img.alpha_composite(Q.crop((0, BC0, W, BC1)), (0, BOT0))
    # frame + header
    def frames(d):
        d.rectangle([0, TOP0 - 6, W, TOP0 + (TC1 - TC0) + 6], outline=(255, 214, 60, 255), width=6)
        d.rectangle([0, BOT0 - 6, W, BOT0 + (BC1 - BC0) + 6], outline=(255, 214, 60, 255), width=6)
    layer(img, frames)
    
    if t >= T_TOP + 1.0:
        a = int(255 * min(1, (t - T_TOP - 1.0) / 0.4))
        layer(img, lambda d: d.rounded_rectangle([110, TOP0 + 10, W - 110, TOP0 + 86], 16, fill=(16, 12, 30, a), outline=(255, 214, 60, a), width=4))
        text_layer(img, [(W / 2, TOP0 + 30, 'Which road are you on?', 34, (255, 255, 255), 5, a)])
    img.alpha_composite(HOOK)
    W_.write(img)
    if f in (20, 100, 200, 300, 370): img.convert('RGB').save(f'p_{f:04d}.png')
W_.close(); json.dump(ev, open('v39_ev.json', 'w')); print('done')
