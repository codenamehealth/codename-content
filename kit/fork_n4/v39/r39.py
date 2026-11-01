"""#39, Oct 29 notes (Bennett): the top panel needed something interesting while the long-road Hollow climbs. Now a swamp monster
(PixelLab, generated for this reel: fork_n4/v39/gen) rises behind the stuck Hollow, hugs him and pulls him under, spits him back
onto the shore, then pops up and waves. Bottom panel, hook, timing of the climb/win and the loop pre-roll unchanged.
Base: fork_hfg4/v39/r39.py.
r039 review recut (fork_rc14). From fork_c4/v39/r39.py (Bennett's solid staircase + trophy kept).
Changes: 'Comment your road' 52px band line from frame 0; both Hollows mid-stride on frame 0 (pre-roll loop);
Hollows 3x -> 4x, gummies 3x -> 4x; stuck Hollow struggles every 2s and sinks further; MADE IT! on its own dark plate
over the lower-left stairs (clear of the banner and the label, label hides when it fires); labels 44px and inset;
location tags dropped; payoff 9.4s -> 8.2s, total 12.6s -> 9.9s; ACV gummy gloss + 'ACV GUMMY' tag on first appearance."""
import sys, os, math, random, json
sys.path.insert(0, '../../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import gummy_src
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
# hfg4: soft-fade hook, no box, no sub line; line colours map to the scenes (top = shortcut swamp green, bottom = long road gold)
_HA, HB = hook_fade(['THE SHORTCUT OR', 'THE LONG ROAD?'], accent=0, color=(170, 225, 110))
_HB2, _ = hook_fade(['THE SHORTCUT OR', 'THE LONG ROAD?'], accent=1, color=(255, 214, 60))
HSPLIT = 286 + int(64 * 1.32) - 6
HOOK = Image.new('RGBA', (W, H)); HOOK.paste(_HA.crop((0, 0, W, HSPLIT)), (0, 0)); HOOK.paste(_HB2.crop((0, HSPLIT, W, H)), (0, HSPLIT))
# full-bleed: two scenes edge to edge, top 0-940, 10px seam, bottom 950-1920 (no blurred backdrop, no gold frames)
SPLIT = 940; BOT0 = SPLIT + 10
TOFF = 80                                # top scene: old panel row r -> frame y r + 80
QOFF = 670                               # bottom scene: old panel row r -> frame y r + 670
QR0, QR1 = BOT0 - QOFF, H - QOFF         # bottom scene rows shown (280..1250)
print('hook', HB, 'split', SPLIT, 'bottom rows', QR0, QR1)
SS = 4; FOOT = 78 * SS
WALK = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'hollow-walk-side.gif')]
RUN = seq(PL + 'maze/anim/hollow_srun', SS)
PANIC = seq(PL + 'maze/anim/hollow_panic', SS)
VICF = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'hollow-victory.gif')]
LILY = up(crop(Image.open('../../fork4/lilypad/02.png').convert('RGBA')), 2)
PH = 830
TOPBG = bg_frames('found_hd.gif', (W, SPLIT), box=(380, 57, 1500, 1031), step=2, bright=0.8)   # same scale as the old 830-row crop, 80 rows more above
def _bot_bg():
    sy = 830 / 768; y0 = 110 + QR0 / sy; nreal = int(round((1080 - y0) * sy))
    out = []
    for f in bg_frames('vit_hd.gif', (W, nreal), box=(700, int(round(y0)), 1700, 1080), step=2, bright=1.0):
        B = Image.new('RGBA', (W, H - BOT0)); B.paste(f, (0, 0))
        rest = (H - BOT0) - nreal          # cobble plaza continues below the art: mirrored rows, darkening into the caption area
        m = f.crop((0, nreal - rest, W, nreal)).transpose(Image.FLIP_TOP_BOTTOM); B.paste(m, (0, nreal))
        g = Image.new('L', (1, H - BOT0), 0)
        for yy in range(H - BOT0):
            g.putpixel((0, yy), int(150 * max(0, min(1, (yy - (nreal - 120)) / 330))))
        sh = Image.new('RGBA', B.size, (16, 12, 22, 255)); sh.putalpha(g.resize(B.size)); B.alpha_composite(sh)
        out.append(B)
    return out
BOTBG = _bot_bg()
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
T_TOP = 8.2; HOLD = 1.4; PRE = 0.0;   # review: pre-roll dropped (its reset at 9.6s read as a hitch); plain loop cut at the end
END = T_TOP + HOLD + PRE
STRUG = [3.2]                            # one struggle, then the monster
T_BUB = 3.5; T_RISE = 3.9; RISE_D = 0.6; T_GRAB = 4.6; GFPS = 10; T_GONE = T_GRAB + 3 / GFPS   # hug frame: he disappears
T_SPIT = 6.0; T_LAND = 6.7; SHORE_X = 150
T_WAVE = 7.5; T_WAVE_END = 9.0; SINK_D = 0.4
MX = 790; YW = 770; MK = 4; WLN = 100   # monster centre x, waterline (panel y), scale, waterline row in its 128 canvas
MGRAB = [up(Image.open(f'gen/grab61/{i:02d}.png').convert('RGBA'), MK) for i in range(9)]
MRISE = MGRAB[0]
MWAVE = up(Image.open('gen/monster/01.png').convert('RGBA'), MK)
IDLEH = [up(f.resize((92, 92), Image.NEAREST), SS) for f in gif_frames(A + 'idle_9.gif')]
def mon(P, fr, rise):
    """monster frame with its waterline at YW; rise 0..1 (0 = fully under). Rows below the water are clipped."""
    dy = int((1 - rise) * (WLN - 4) * MK)
    m = fr.copy()
    if dy > 0:
        a = m.getchannel('A'); ImageDraw.Draw(a).rectangle([0, WLN * MK + 8 - dy, m.width, m.height], fill=0); m.putalpha(a)
    P.alpha_composite(m, (int(MX - 64 * MK), int(YW - WLN * MK + dy)))
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
    d.line([(xl, bot - 1), (xr, bot - 1)], fill=OUT)
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
def plate_text(img, cx, y, txt, size, fill, a=255, ring=(255, 214, 60)):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); f = F(size); tw = d.textlength(txt, font=f)
    d.rounded_rectangle([cx - tw / 2 - 18, y - 14, cx + tw / 2 + 18, y + size + 16], 14, fill=(16, 12, 30, int(230 * a / 255)), outline=ring + (a,), width=5)
    ctext(d, cx, y, txt, f, fill, 8, a); img.alpha_composite(L)
ONLY = [int(v) for v in os.environ.get('ONLY', '').split(',') if v]
W_ = Writer('v39_noaudio.mp4' if not ONLY else '_test.mp4'); ev = []
got = {}
NF = int(round(END * FPS))
for f in range(NF):
    t = f / FPS
    LOOP = t >= END - PRE - 1e-6
    if LOOP: t = t - END                 # pre-roll: both Hollows walking up to their frame-0 marks, so the loop is seamless
    img = Image.new('RGBA', (W, H), (12, 10, 18, 255))
    # ---- top panel: the shortcut (drawn in the old panel coordinates on a transparent layer, then set on the taller scene)
    P = Image.new('RGBA', (W, SPLIT - TOFF)); P.alpha_composite(swamp_layer(max(0, t)))
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
        # --- swamp monster (behind the Hollow)
        if T_RISE <= t < T_GRAB:
            mon(P, MRISE, min(1, (t - T_RISE) / RISE_D))
        elif T_GRAB <= t < T_GRAB + 9 / GFPS + 0.6:
            k = min(8, int((t - T_GRAB) * GFPS)); mon(P, MGRAB[k], 1)
        elif T_WAVE <= t < T_WAVE_END + SINK_D:
            r_ = min(1, (t - T_WAVE) / 0.45) if t < T_WAVE_END else max(0, 1 - (t - T_WAVE_END) / SINK_D)
            bobm = int(6 * math.sin(t * 5)); m_ = MWAVE.rotate(5 * math.sin(t * 9), resample=Image.NEAREST, center=(64 * MK, WLN * MK))   # sways while it waves
            mon(P, m_, r_)
        if not LOOP:
            for t_, nm_ in ((T_RISE, 'whoosh_8bit'), (T_GONE, 'squish'), (T_SPIT, 'boing'), (T_LAND, 'stomp_8bit'), (T_WAVE, 'twinkle')):
                if f == round(t_ * FPS): ev.append((round(t_, 3), nm_))
        if T_BUB <= t < T_RISE + 0.3 or T_GONE + 0.3 <= t < T_SPIT:
            rb = random.Random(int(t * 6))
            bub = [(MX + rb.uniform(-120, 120), YW - 20 - rb.uniform(0, 40), rb.choice([8, 12, 16])) for _ in range(6)]
            layer(P, lambda d: [d.ellipse([bx - r, by - r, bx + r, by + r], outline=(170, 200, 110, 255), width=4) for bx, by, r in bub])
        if t < T_GONE:
            base = min(100, 56 + u * 6)
            lift = 0.0; sp = None
            for ts in STRUG:
                if 0 <= t - ts < 0.7:
                    p = (t - ts) / 0.7; lift = 34 * math.sin(math.pi * p); sp = p
                    if f == round(ts * FPS) and not LOOP: ev.append((round(ts, 3), 'squish'))
            sink = base - lift
            if t >= T_GRAB: sink += (t - T_GRAB) / (T_GONE - T_GRAB) * 60
            spr = PANIC[int(t * (18 if (sp is not None or t >= T_RISE) else 12)) % 8]; cut = int(FOOT - sink)
            s2 = spr.copy(); a = s2.getchannel('A'); ImageDraw.Draw(a).rectangle([0, cut, s2.width, s2.height], fill=0); s2.putalpha(a)
            P.alpha_composite(s2, (int(x - spr.width / 2), int(SWY + 20 - FOOT)))
            layer(P, lambda d: (d.ellipse([x - 110, SWY + 20 - sink - 16, x + 110, SWY + 20 - sink + 34], outline=(160, 190, 90, 255), width=7)))
            if T_RISE + 0.2 <= t:     # '!' emote when he sees it
                text_layer(P, [(x - 70, int(SWY + 20 - FOOT + sink * 0 + 30), '!', 72, (255, 255, 255), 9, 255)])
        elif T_SPIT <= t < T_LAND:   # spat out: spins through the air onto the shore
            p = (t - T_SPIT) / (T_LAND - T_SPIT)
            hx = MX + (SHORE_X - MX) * p; hy = YW - 60 + (GY - (YW - 60)) * p - 150 * math.sin(math.pi * p)
            spr = PANIC[int(t * 16) % 8].rotate(-720 * p, resample=Image.NEAREST, expand=True)
            P.alpha_composite(spr, (int(hx - spr.width / 2), int(hy - spr.height / 2 - 40)))
            if p < 0.3: layer(P, lambda d: [d.rectangle([MX + math.cos(k) * 200 * p * 3 - 8, YW - 40 - abs(math.sin(k)) * 300 * p * 3, MX + math.cos(k) * 200 * p * 3 + 8, YW - 32 - abs(math.sin(k)) * 300 * p * 3], fill=(120, 160, 60, 255)) for k in range(12)])
        elif t >= T_LAND:            # dazed on the shore, stars round his head
            v = t - T_LAND; sq = max(0, 1 - v / 0.15)
            spr = IDLEH[int(t * 8) % len(IDLEH)]
            if sq > 0: spr = spr.resize((int(spr.width * (1 + 0.25 * sq)), int(spr.height * (1 - 0.25 * sq))), Image.NEAREST)
            P.alpha_composite(spr, (int(SHORE_X - spr.width / 2), int(GY - FOOT * (1 - 0.25 * sq))))
            if v < 2.2:
                def stars(d):
                    for k in range(3):
                        a_ = t * 5 + k * 2.094; sx_ = SHORE_X + 70 * math.cos(a_); sy_ = GY - FOOT + 50 + 18 * math.sin(a_)
                        d.polygon([(sx_, sy_ - 14), (sx_ + 5, sy_ - 4), (sx_ + 15, sy_), (sx_ + 5, sy_ + 4), (sx_, sy_ + 14), (sx_ - 5, sy_ + 4), (sx_ - 15, sy_), (sx_ - 5, sy_ - 4)], fill=(255, 230, 90, 255), outline=(60, 40, 10, 255))
                layer(P, stars)
        def drops(d, uu, y0):
            for k in range(14):
                X = x + math.cos(k) * (36 + uu * 230); Y = y0 - math.sin(abs(math.cos(k * 1.7))) * uu * 200 + uu * uu * 230
                d.rectangle([X, Y, X + 10, Y + 10], fill=(120, 160, 60, 255))
        if u < 0.6: layer(P, lambda d: drops(d, u, SWY - 40))
        if not LOOP and not any(e[1] == 'boing' and e[0] < 3 for e in ev): ev.append((round(T_SPLASH, 3), 'squish')); ev.append((round(T_SPLASH + 0.05, 3), 'boing'))
        if 0.4 < u and t < T_RISE: text_layer(P, [(x, 428, 'STUCK!', 64, (190, 230, 120), 8, 255)])
    PF = TOPBG[int((t % 30) * 6) % len(TOPBG)].copy(); PF.alpha_composite(P, (0, TOFF))
    img.alpha_composite(PF, (0, 0))
    # ---- bottom panel: the long road
    Q = Image.new('RGBA', (W, QR1))
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
    for (i, k) in GUMS:                     # review: sparkle pop where each gummy is picked up
        if k in got and 0 <= t - got[k] < 0.4:
            v = (t - got[k]) / 0.4; gx, gy = STEPS[i]; gy -= 150
            def pop(d, v=v, gx=gx, gy=gy):
                d.ellipse([gx - 40 - 90 * v, gy - 40 - 90 * v, gx + 40 + 90 * v, gy + 40 + 90 * v], outline=(255, 240, 160, int(230 * (1 - v))), width=8)
                for a_ in range(8):
                    r_ = 30 + 140 * v; X = gx + r_ * math.cos(a_ * 0.785); Y = gy + r_ * math.sin(a_ * 0.785); s_ = int(12 * (1 - v)) + 3
                    d.rectangle([X - s_, Y - 3, X + s_, Y + 3], fill=(255, 255, 230, int(255 * (1 - v)))); d.rectangle([X - 3, Y - s_, X + 3, Y + s_], fill=(255, 255, 230, int(255 * (1 - v))))
            layer(Q, pop)
    QF = BOTBG[int((t % 30) * 6) % len(BOTBG)].copy(); QF.alpha_composite(Q.crop((0, QR0, W, QR1)))
    img.alpha_composite(QF, (0, BOT0))
    n = 0 if LOOP else len(got)             # XP counter = the long road's score (the +1 XP pops, the panel labels and the ACV tag are cut)
    tg = max([v for v in got.values() if v <= t], default=None)
    bump = 0 if (tg is None or LOOP) else max(0, 1 - (t - tg) / 0.25)    # review: XP ticks with a small bump on each pickup
    xs = int(44 * (1 + 0.3 * bump)); col = (255, 214, 60) if bump > 0 else (255, 255, 255)
    text_layer(img, [(880 - F(xs).getlength(f'XP {n}/4') / 2, BOT0 + 24 - (xs - 44) // 2, f'XP {n}/4', xs, col, 7, 255)])   # review: ends by x880
    if t >= T_TOP and not LOOP:            # MADE IT! stamp (no plate) over the lower-left stairs
        pop = min(1, (t - T_TOP) / 0.15); sz = int(72 * (1.25 - 0.25 * pop))
        text_layer(img, [(420, QOFF + 690 + (72 - sz) // 2, 'MADE IT!', sz, (255, 214, 60), 9, 255)])
    img.alpha_composite(HOOK)
    if ONLY:
        if f in ONLY: img.convert('RGB').save(f't_{f}.png')
        continue
    W_.write(img)
W_.close(); json.dump({'events': ev}, open('v39_ev.json', 'w')); print('done', END, NF, got)
