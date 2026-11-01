"""r039 review recut (fork_rc14). From fork_c4/v39/r39.py (Bennett's solid staircase + trophy kept).
Changes: 'Comment your road' 52px band line from frame 0; both Hollows mid-stride on frame 0 (pre-roll loop);
Hollows 3x -> 4x, gummies 3x -> 4x; stuck Hollow struggles every 2s and sinks further; MADE IT! on its own dark plate
over the lower-left stairs (clear of the banner and the label, label hides when it fires); labels 44px and inset;
location tags dropped; payoff 9.4s -> 8.2s, total 12.6s -> 9.9s; ACV gummy gloss + 'ACV GUMMY' tag on first appearance."""
import sys, os, math, random, json
sys.path.insert(0, '../../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import hook_layer2, gummy_src, acv_tag
HOOK, HB = hook_layer2(['THE SHORTCUT OR', 'THE LONG ROAD?'], accent=1, sub='Comment your road')
TOP0 = HB + 12
TC0, TC1 = 316, 770                      # top panel crop (454 tall)
BOT0 = TOP0 + (TC1 - TC0) + 14
BC0, BC1 = 328, 328 + (1488 - BOT0)      # bottom panel crop, ends at y1488
print('hook', HB, 'top', TOP0, 'bot', BOT0, BC1)
SS = 4; FOOT = 78 * SS
WALK = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'hollow-walk-side.gif')]
RUN = seq(PL + 'maze/anim/hollow_srun', SS)
PANIC = seq(PL + 'maze/anim/hollow_panic', SS)
VICF = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'hollow-victory.gif')]
LILY = up(crop(Image.open('../../fork4/lilypad/02.png').convert('RGBA')), 2)
PH = 830
TOPBG = bg_frames('found_hd.gif', (W, PH), box=(380, 140, 1500, 1000), step=2, bright=0.8)
BOTBG = bg_frames('vit_hd.gif', (W, PH), box=(700, 110, 1700, 878), step=2, bright=1.0)
GY = 700
SX0 = 430
SWX, SWY = 760, 730
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
# long road: same staircase, a bit lower so the 4x Hollow fits on the landing
NST = 9; ST0 = (135, 790); ST1 = (590, 600)
STEPS = [(ST0[0] + (ST1[0] - ST0[0]) * i / (NST - 1), ST0[1] + (ST1[1] - ST0[1]) * i / (NST - 1)) for i in range(NST)]
LAND1 = 880; TROPHY_X = 800
GUMS = [(2, 'acv'), (4, 'cre'), (6, 'mush'), (8, 'mel')]
GIMG = {k: up(gummy_src(k), 3) for _, k in GUMS}
T_SLIDE = 2.0; T_SPLASH = 2.7
T_TOP = 8.2; HOLD = 1.4; PRE = 0.3; END = T_TOP + HOLD + PRE
STRUG = [4.5, 6.5, 8.5]                  # stuck Hollow tries to climb out, sinks back further
V_LONG = (STEPS[1][0] - STEPS[0][0]) * (NST - 1) / T_TOP
V_SHORT = (SX0 - 180) / T_SLIDE
def long_pos(t):
    if t < 0: return STEPS[0][0] + V_LONG * t, STEPS[0][1]
    u = max(0, min(1, t / T_TOP))
    f = u * (NST - 1); i = int(f); fr = f - i
    if i >= NST - 1: return STEPS[-1][0] + 30, STEPS[-1][1]
    x0, y0 = STEPS[i]; x1, y1 = STEPS[i + 1]
    hop = math.sin(math.pi * fr) * 12
    return x0 + (x1 - x0) * fr, y0 + (y1 - y0) * min(1, fr * 1.6) - hop
def build_stairs():
    L = Image.new('RGBA', (W // 3, PH // 3), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    sw = (STEPS[1][0] - STEPS[0][0]) / 3; bot = PH // 3
    xs = [sx / 3 - sw / 2 for sx, sy in STEPS]; ys = [sy / 3 for sx, sy in STEPS]
    xl = xs[0]; xr = LAND1 / 3
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
    for i in range(NST):
        xa = xs[i]; xb = xs[i + 1] if i + 1 < NST else xr
        d.rectangle([xa, ys[i], xb, ys[i] + 1], fill=LIGHT)
        d.line([(xa, ys[i] + 2), (xb, ys[i] + 2)], fill=DARK)
        d.line([(xa, ys[i]), (xa, (ys[i - 1] if i else bot))], fill=OUT)
    d.rectangle([xs[-1], ys[-1] - 1, xr + 2, ys[-1] + 3], fill=LIGHT); d.line([(xs[-1], ys[-1] + 4), (xr + 2, ys[-1] + 4)], fill=OUT)
    d.line([(xr, ys[-1]), (xr, bot)], fill=OUT); d.rectangle([xr - 3, ys[-1] + 5, xr - 1, bot], fill=DARK)
    d.line(poly[:-1], fill=OUT)
    return up(L, 3)
def build_trophy():
    T = Image.new('RGBA', (30, 46), (0, 0, 0, 0)); d = ImageDraw.Draw(T)
    O, D, G, Lg, Wt = (60, 30, 8, 255), (186, 112, 18, 255), (250, 196, 46, 255), (255, 236, 140, 255), (255, 255, 240, 255)
    d.ellipse([1, 4, 10, 15], outline=O, width=3); d.ellipse([2, 5, 9, 14], outline=D, width=1)
    d.ellipse([19, 4, 28, 15], outline=O, width=3); d.ellipse([20, 5, 27, 14], outline=D, width=1)
    d.polygon([(5, 2), (24, 2), (23, 10), (20, 16), (15, 19), (14, 19), (9, 16), (6, 10)], fill=O)
    d.polygon([(6, 3), (23, 3), (22, 10), (19, 15), (15, 18), (14, 18), (10, 15), (7, 10)], fill=G)
    d.polygon([(16, 3), (23, 3), (22, 10), (19, 15), (15, 18)], fill=D)
    d.line([(8, 4), (9, 11)], fill=Lg, width=2); d.point((9, 5), fill=Wt)
    d.rectangle([5, 1, 24, 3], fill=O); d.rectangle([6, 2, 23, 2], fill=Lg)
    d.rectangle([12, 19, 17, 25], fill=O); d.rectangle([13, 19, 16, 24], fill=G); d.line([(15, 19), (15, 24)], fill=D)
    d.rectangle([9, 25, 20, 28], fill=O); d.rectangle([10, 26, 19, 27], fill=G); d.line([(16, 26), (19, 26)], fill=D)
    d.rectangle([7, 28, 22, 32], fill=O); d.rectangle([8, 29, 21, 31], fill=D); d.line([(8, 29), (14, 29)], fill=G)
    d.point([(14, 8), (13, 9), (14, 9), (15, 9), (14, 10)], fill=Wt)
    S1, S2, S3 = (150, 146, 160, 255), (110, 106, 122, 255), (200, 196, 208, 255)
    d.rectangle([4, 32, 25, 45], fill=(40, 34, 52, 255)); d.rectangle([5, 33, 24, 44], fill=S1)
    d.rectangle([5, 33, 24, 34], fill=S3); d.rectangle([21, 35, 24, 44], fill=S2); d.line([(5, 39), (24, 39)], fill=S2)
    return up(T, 4)
TROPHY = build_trophy()
STAIRS_IMG = build_stairs()
BACK = bg_frames('vit_hd.gif', (W, H), box=(900, 0, 1508, 1080), step=1000, bright=0.45, blur=10)[0]
def plate_text(img, cx, y, txt, size, fill, a=255, ring=(255, 214, 60)):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); f = F(size); tw = d.textlength(txt, font=f)
    d.rounded_rectangle([cx - tw / 2 - 18, y - 14, cx + tw / 2 + 18, y + size + 16], 14, fill=(16, 12, 30, int(230 * a / 255)), outline=ring + (a,), width=5)
    ctext(d, cx, y, txt, f, fill, 8, a); img.alpha_composite(L)
W_ = Writer('v39_noaudio.mp4'); ev = []
got = {}
NF = int(round(END * FPS))
for f in range(NF):
    t = f / FPS
    LOOP = t >= END - PRE - 1e-6
    if LOOP: t = t - END                 # pre-roll: both Hollows walking up to their frame-0 marks, so the loop is seamless
    img = BACK.copy()
    # ---- top panel: the shortcut
    P = TOPBG[int((t % 30) * 6) % len(TOPBG)].copy(); P.alpha_composite(swamp_layer(max(0, t)))
    for k, lx in enumerate([620, 700, 960]): P.alpha_composite(LILY, (lx, SWY - 8 + 18 * (k % 2)))
    if t < T_SLIDE:
        x = 180 + V_SHORT * t; y = GY
        spr = RUN[int((t + 1) * 12) % 8]
        P.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    elif t < T_SPLASH:
        u = (t - T_SLIDE) / (T_SPLASH - T_SLIDE); x = SX0 + (SWX - 60 - SX0) * u; y = GY + (SWY + 10 - GY) * (u ** 1.4)
        spr = RUN[int(t * 16) % 8].rotate(-22, resample=Image.NEAREST, expand=True)
        P.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    else:
        u = t - T_SPLASH; x = SWX - 60
        base = min(100, 56 + u * 6)               # keeps sinking a little
        lift = 0.0; sp = None
        for ts in STRUG:
            if 0 <= t - ts < 0.7:
                p = (t - ts) / 0.7; lift = 34 * math.sin(math.pi * p); sp = p
                if f == round(ts * FPS) and not LOOP: ev.append((round(ts, 3), 'squish'))
        sink = base - lift
        spr = PANIC[int(t * (18 if sp is not None else 12)) % 8]; cut = int(FOOT - sink)
        s2 = spr.copy(); a = s2.getchannel('A'); ImageDraw.Draw(a).rectangle([0, cut, s2.width, s2.height], fill=0); s2.putalpha(a)
        P.alpha_composite(s2, (int(x - spr.width / 2), int(SWY + 20 - FOOT)))
        layer(P, lambda d: (d.ellipse([x - 110, SWY + 20 - sink - 16, x + 110, SWY + 20 - sink + 34], outline=(160, 190, 90, 255), width=7)))
        def drops(d, uu, y0):
            for k in range(14):
                X = x + math.cos(k) * (36 + uu * 230); Y = y0 - math.sin(abs(math.cos(k * 1.7))) * uu * 200 + uu * uu * 230
                d.rectangle([X, Y, X + 10, Y + 10], fill=(120, 160, 60, 255))
        if u < 0.6: layer(P, lambda d: drops(d, u, SWY - 40))
        if sp is not None and sp < 0.75: layer(P, lambda d: drops(d, sp * 0.8, SWY - 20))
        if not LOOP and not any(e[1] == 'boing' for e in ev): ev.append((round(T_SPLASH, 3), 'squish')); ev.append((round(T_SPLASH + 0.05, 3), 'boing'))
        if u > 0.4: text_layer(P, [(x, TC0 + 112, 'STUCK!', 64, (190, 230, 120), 8, 255)])
    text_layer(P, [(86 + F(44).getlength('SHORTCUT') / 2, TC0 + 18, 'SHORTCUT', 44, (255, 255, 255), 7, 255)])
    img.alpha_composite(P.crop((0, TC0, W, TC1)), (0, TOP0))
    # ---- bottom panel: the long road
    Q = BOTBG[int((t % 30) * 6) % len(BOTBG)].copy()
    Q.alpha_composite(STAIRS_IMG)
    tb = int(STEPS[-1][1]); tx = TROPHY_X; won = t >= T_TOP
    def tglow(d):
        pr = 1 + 0.08 * math.sin(t * 5) + (0.35 * max(0, 1 - (t - T_TOP) / 0.6) if won else 0)
        for rr_, al in ((110, 40), (80, 60), (56, 80)):
            r2 = rr_ * pr; d.ellipse([tx - r2, tb - 110 - r2, tx + r2, tb - 110 + r2], fill=(255, 220, 110, al))
        if won:
            for k in range(10):
                a_ = (t - T_TOP) * 1.5 + k * math.pi / 5; r1, r2 = 70, 160
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
        gx, gy = STEPS[i]; g = GIMG[k]; bob = int(6 * math.sin(t * 4 + i))
        layer(Q, lambda d, gx=gx, gy=gy: d.ellipse([gx - 56, gy - 206, gx + 56, gy - 94], fill=(255, 230, 150, 70)))
        Q.alpha_composite(g, (int(gx - g.width / 2), int(gy - 150 - g.height / 2 + bob)))
    if t < T_TOP:
        x, y = long_pos(t); spr = WALK[int((t + 1) * 8) % len(WALK)]
        Q.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT + 4)))
        for (i, k) in GUMS:
            if not LOOP and k not in got and x >= STEPS[i][0] - 10:
                got[k] = t; ev.append((round(t, 3), 'coin_8bit'))
    else:
        u = t - T_TOP; vf = VICF[int(u * 8) % len(VICF)]
        x, y = long_pos(T_TOP)
        layer(Q, lambda d: [d.ellipse([x - r, y - 150 - r, x + r, y - 150 + r], outline=(255, 214, 60, max(0, 200 - r)), width=8) for r in range(int(u * 300) % 240, int(u * 300) % 240 + 1)])
        Q.alpha_composite(vf, (int(x - vf.width / 2), int(y - FOOT)))
        if not any(e[1] == 'victory' for e in ev): ev.append((round(T_TOP, 3), 'victory'))
    if not LOOP:
        for k, tg in got.items():
            if 0 <= t - tg < 0.9 and t < T_TOP:
                x, y = long_pos(tg); text_layer(Q, [(max(80 + 120, x), max(BC0 + 70, y - 330 - (t - tg) * 40), '+1 XP', 44, (255, 214, 60), 6, int(255 * min(1, (0.9 - (t - tg)) / 0.3)))])
    if t < T_TOP:
        text_layer(Q, [(86 + F(44).getlength('LONG ROAD') / 2, BC0 + 18, 'LONG ROAD', 44, (255, 214, 60), 7, 255)])
    n = 0 if LOOP else len(got)
    text_layer(Q, [(1000 - F(44).getlength(f'XP {n}/4') / 2, BC0 + 18, f'XP {n}/4', 44, (255, 255, 255), 7, 255)])
    img.alpha_composite(Q.crop((0, BC0, W, BC1)), (0, BOT0))
    def frames(d):
        d.rectangle([0, TOP0 - 6, W, TOP0 + (TC1 - TC0) + 6], outline=(255, 214, 60, 255), width=6)
        d.rectangle([0, BOT0 - 6, W, BOT0 + (BC1 - BC0) + 6], outline=(255, 214, 60, 255), width=6)
    layer(img, frames)
    if t >= T_TOP and not LOOP:            # MADE IT! on its own plate over the lower-left stairs, above every scenery layer
        pop = min(1, (t - T_TOP) / 0.15); sz = int(64 * (1.25 - 0.25 * pop))
        plate_text(img, 350, BOT0 + (690 - BC0) + (64 - sz) // 2, 'MADE IT!', sz, (255, 214, 60))
    if (0 <= t < 1.6) or LOOP:          # ACV gummy tag on first appearance (it's Syeda's apple-shaped gummy); also in the pre-roll so the loop is seamless
        gx, gy = STEPS[2]; a = 255 if LOOP else int(255 * min(1, (1.6 - t) / 0.3))
        acv_tag(img, int(gx), int(BOT0 + (gy - 150 - BC0) - GIMG['acv'].height / 2 - 4), a=a, xmax=880)
    img.alpha_composite(HOOK)
    W_.write(img)
W_.close(); json.dump({'events': ev}, open('v39_ev.json', 'w')); print('done', END, NF, got)
