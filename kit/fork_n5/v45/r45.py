# n5 pass of #45 (Bennett Oct 29: 'guides need to be doing the actions'). Base: fork_hfg4/v45/r45.py.
# Each option now shows its guide DOING the option with existing animations; Q4 swapped (no Rayleigh 'log off' animation).
# hfg4 pass of #45 (from fork_rc6/v45/r45.py). Same questions, order and timing (audio reused).
# Changes: soft-fade hook (no box, no 'Comment your guild'); COUNT YOUR COLORS as one line inside the fade (intro + loop);
# legend = the 4 realm strips edge to edge with each guide standing on its own realm (no panels, names only, product lines cut);
# questions = the two realm halves are the options (no cards): option words in the guild colour, guide + jar + gummy standing
# on the realm's ground; QUESTION n/4 plate + bar cut; end = the legend slides back in under WHICH GUILD ARE YOU? (2x2 grid
# and the MOST PICKED COLOR = YOUR GUILD plate cut), then slides out right and frame 0 slides it in from the left (loop).
import sys, math, json, random, os, glob
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_fade
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = {  # guild: (name, color, realm gif, jar file, gummy, guide, ground row in the source art)
 'F': ('FOUNDATION', (120, 225, 90), 'found_hd.gif', 'jar_acv.png', 'acv', 'joy', 800),
 'V': ('VITALITY', (100, 165, 255), 'vit_hd.gif', 'jar_creatine.png', 'cre', 'cleo', 820),
 'E': ('ENERGY', (255, 165, 50), 'sun_hd.gif', 'jar_mushroom.png', 'mush', 'cyrus', 800),
 'R': ('RECOVERY', (195, 120, 255), 'recov_hd.gif', 'jar_melatonin.png', 'mel', 'ray', 880)}
QS = [('NIGHT OWL', 'R', 'EARLY BIRD', 'F'), ('TANK', 'V', 'SPEEDRUNNER', 'E'), ('COZY FARM GAME', 'F', 'BOSS RUSH', 'V'),
      ('MELEE', 'E', 'MAGIC', 'R')]
ACT = {'NIGHT OWL': 'owl', 'EARLY BIRD': 'bird', 'TANK': 'tank', 'SPEEDRUNNER': 'speed', 'COZY FARM GAME': 'farm', 'BOSS RUSH': 'boss', 'MELEE': 'melee', 'MAGIC': 'magic'}
NQ = len(QS)
RH = 960; RS = RH / 1080                       # realm render (W x 960), scale 0.889 (same as before)
def realm(name, h, bright):
    w_src = min(1920, int(1080 * (W / h))); x0 = (1920 - w_src) // 2
    return bg_frames(name, (W, h), box=(x0, 0, x0 + w_src, 1080), step=2, bright=bright)
RT = {k: realm(v[2], RH, 0.74) for k, v in G.items()}
MIR = 600
def put_realm(img, k, t, feet_y, y0, y1, ph=0):
    """realm k placed so its ground row sits at feet_y, filling y0..y1 (mirrored, slightly darker rows past the art's edges)"""
    fr = RT[k][int(t * 5 + ph) % len(RT[k])]
    E = Image.new('RGBA', (W, RH + 2 * MIR)); E.paste(fr, (0, MIR))
    top = ImageEnhance.Brightness(fr.crop((0, 0, W, MIR)).transpose(Image.FLIP_TOP_BOTTOM)).enhance(0.8); E.paste(top, (0, 0))
    bot = ImageEnhance.Brightness(fr.crop((0, RH - MIR, W, RH)).transpose(Image.FLIP_TOP_BOTTOM)).enhance(0.8); E.paste(bot, (0, MIR + RH))
    yoff = feet_y - (MIR + G[k][6] * RS)
    a, b = int(round(y0 - yoff)), int(round(y1 - yoff)); assert a >= 0 and b <= E.height, (k, a, b)
    img.alpha_composite(E.crop((0, a, W, b)), (0, int(y0)))
JAR = {}
for k, v in G.items():
    j = crop(Image.open(A + v[3]).convert('RGBA')); JAR[k] = j.resize((int(j.width * 200 / j.height), 200), Image.NEAREST)
JARS = {k: j.resize((int(j.width * 150 / j.height), 150), Image.NEAREST) for k, j in JAR.items()}
GUM = {k: (up(acv_gummy_strong(), 3) if v[4] == 'acv' else gummy(v[4], 3)) for k, v in G.items()}   # ACV gets the gummy shine
IDL = {k: idle(v[5], 3) for k, v in G.items()}
IDL4 = {k: idle(v[5], 4) for k, v in G.items()}
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
HOOK, HB = hook_fade(['WHICH GUILD', 'ARE YOU?'], accent=1, color=(255, 214, 60), size=72)
print('hook bottom', HB)
LH = int(72 * 1.32)
def count_line(a, txt='COUNT YOUR COLORS'):     # one short line inside the same fade under the hook
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ctext(d, W / 2, HB + 6, txt, F(44), (255, 255, 255), 7, a); return L
SH = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # deepen the fade a little under the instruction line
_g = Image.new('L', (1, H), 0)
for yy in range(H): _g.putpixel((0, yy), int(120 * max(0.0, min(1.0, (HB + 110 - yy) / 160))) if yy > HB - 50 else 0)
_s = Image.new('RGBA', (W, H), (8, 6, 16, 255)); _s.putalpha(_g.resize((W, H))); SH.alpha_composite(_s)
# ---- legend: 4 realm strips edge to edge, rows inside the safe zone
LY0 = HB + 64; RWH = (1498 - LY0) // 4
ROWS = [(LY0 + i * RWH, LY0 + (i + 1) * RWH) for i in range(4)]
print('legend rows', ROWS)
def legend_bg(img, t):
    for i, k in enumerate('FVER'):
        y0 = 0 if i == 0 else ROWS[i][0]; y1 = H if i == 3 else ROWS[i][1]
        put_realm(img, k, t, ROWS[i][1] - 12, y0, y1, ph=i)
    layer(img, lambda d: [d.rectangle([0, ROWS[i][0] - 3, W, ROWS[i][0] + 3], fill=(12, 8, 20, 255)) for i in range(1, 4)])
JARL = {k: j.resize((int(j.width * 196 / j.height), 196), Image.NEAREST) for k, j in JAR.items()}
GUML = {k: up(GUM[k], 4 / 3) for k in GUM}
def legend_row(img, i, k, t, dx):
    y0, y1 = ROWS[i]; feet = y1 - 10; R = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fr = IDL[k][int(t * 8) % 6]; R.alpha_composite(fr, (int(215 - fr.width / 2), feet - 78 * 3))
    js = JARL[k]; R.alpha_composite(js, (350, feet - js.height + 4))
    g = GUML[k]; gx, gy = 560, feet - g.height - 26 + int(8 * math.sin(t * 4 + i))
    layer(R, lambda d: d.ellipse([gx - 26, gy - 26, gx + g.width + 26, gy + g.height + 26], fill=G[k][1] + (70,)))
    R.alpha_composite(g, (gx, gy))
    d = ImageDraw.Draw(R); f_ = F(60); tx = 340; assert tx + d.textlength(G[k][0], font=f_) <= (1025 if y0 + 70 <= 1110 else 887), G[k][0]
    d.text((tx, y0 + 12), G[k][0], font=f_, fill=G[k][1], stroke_width=8, stroke_fill=(16, 10, 26))
    if dx: R = R.transform(R.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0))
    img.alpha_composite(R)
# ---- questions: the two realm halves are the two options
FA, FB = 900, 1452                              # guide feet for option A (top) and B (bottom)
CW, CH = 930, 370; CX0 = 75
SEAM = (FA + FB - CH + 12) // 2 + 18
KA = 4; FY = CH - 12                            # actors 4x, feet line inside the option canvas
def anim(d, lo=0, hi=None): return [up(Image.open(p).convert('RGBA'), KA) for p in sorted(glob.glob(SP0 + d + '/*.png'))[lo:hi]]
def notooth(d, box, lo=1, hi=9):                # same mouth fix as the approved #52 (Joy never shows teeth)
    out = []
    for p in sorted(glob.glob(SP0 + d + '/*.png'))[lo:hi]:
        im = Image.open(p).convert('RGBA'); px = im.load()
        for x in range(box[0], box[2]):
            for y in range(box[1], box[3]):
                r, g, b_, al = px[x, y]
                if al and r > 235 and g > 225 and b_ > 215: px[x, y] = (106, 38, 9, 255)
        out.append(up(im, KA))
    return out
RCAST = anim('fork3/ray_cast', 1, 9); JSTR = notooth('fork_b5/joy_stretch', (40, 28, 51, 36))
CBLK = anim('fork_a4/cleo_block'); CRUN = anim('pixellab/race/cyrus_run'); JPLANT = anim('fork2/joy_plant')
CATK = anim('pixellab/race/cleo_atk'); YATK = anim('pixellab/race/cyrus_atk'); RATK = anim('pixellab/race/ray_atk')
KING = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(SP0 + 'pixellab/king/king_idle/*.png'))]
SLM = [up(Image.open(p).convert('RGBA'), 3) for p in sorted(glob.glob(SP0 + 'pixellab/race/slime_idle_c/*.png'))]
TREES = [up(crop(Image.open(SP0 + f'fork2/smalltree/{i:02d}.png').convert('RGBA')), 2) for i in (9, 1, 15, 4)]
GUMS = {k: up(GUM[k], 2 / 3) for k in GUM}      # option-word gummy at 2x
def pa(c, spr, x, base=78, cx=46, y=FY):        # paste actor: canvas anchor (cx, base) at (x, y)
    c.alpha_composite(spr, (int(x - cx * KA), int(y - base * KA)))
def flash(spr, a):
    w = Image.new('RGBA', spr.size, (255, 255, 255, 0)); m = spr.getchannel('A').point(lambda v: int(v * a)); w.putalpha(m)
    o = spr.copy(); o.alpha_composite(w); return o
def act(c, name, t):
    d = ImageDraw.Draw(c); fi = int(t * 12)
    if name == 'owl':                           # Rayleigh up late casting under the moon, fireflies
        for k in range(10):
            sx = 380 + (k * 97) % 480; sy = 150 + (k * 61) % 170 + 10 * math.sin(t * 3 + k)
            d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 190, int(140 + 110 * math.sin(t * 4 + k))))
        pa(c, RCAST[fi % len(RCAST)], 330)
    elif name == 'bird':                        # sun coming up, Joy stretching awake (as in the approved #52)
        u = (t % 2.6); sy = FY - 40 - 150 * min(1, u / 1.2)
        S_ = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); sd = ImageDraw.Draw(S_)
        for r, a in ((115, 45), (90, 80)): sd.ellipse([760 - r, sy - r, 760 + r, sy + r], fill=(255, 225, 120, a))
        for k in range(10):
            a_ = k * 0.628 + t * 0.6; sd.line([(760 + 82 * math.cos(a_), sy + 82 * math.sin(a_)), (760 + 108 * math.cos(a_), sy + 108 * math.sin(a_))], fill=(255, 230, 120, 230), width=8)
        sd.ellipse([700, sy - 60, 820, sy + 60], fill=(255, 214, 80, 255), outline=(240, 160, 40, 255), width=5)
        S_ = S_.crop((0, 0, CW, FY - 40)); c.alpha_composite(S_, (0, 0))
        pa(c, JSTR[min(7, int(u * 6)) if u < 1.4 else 4 + int(t * 8) % 4], 330)
    elif name == 'tank':                        # Cleo braced behind her shield, slimes bounce off it
        T = 0.8; u = (t % T) / T; hit = u > 0.55
        pa(c, CBLK[4 + fi % 5] if True else None, 600 + (6 if 0.55 < u < 0.65 else 0))
        for j in range(2):
            uu = (u + j * 0.5) % 1.0
            if uu < 0.55: x = -60 + 520 * (uu / 0.55); y = FY - 62 * 3 - 90 * abs(math.sin(uu / 0.55 * math.pi * 2))
            else: v = (uu - 0.55) / 0.45; x = 460 - 600 * v; y = FY - 62 * 3 - 130 * math.sin(v * math.pi) + 60 * v
            sp = SLM[int(t * 10 + j) % len(SLM)]
            if uu >= 0.55: sp = sp.rotate(360 * (uu - 0.55) * 2, resample=Image.NEAREST, expand=True)
            c.alpha_composite(sp, (int(x - sp.width / 2), int(y)))
            if 0.55 <= uu < 0.63:
                for k in range(6):
                    a = k * 1.05; r = 30 + 400 * (uu - 0.55)
                    d.rectangle([480 + r * math.cos(a) - 6, FY - 170 + r * math.sin(a) - 6, 480 + r * math.cos(a) + 6, FY - 170 + r * math.sin(a) + 6], fill=(255, 240, 160, 255))
    elif name == 'speed':                       # Cyrus sprinting across, dust + speed lines
        T = 1.0; u = (t % T) / T; x = -60 + 1080 * u
        for k in range(6):
            yy = FY - 70 - k * 40; ln = 110 + 60 * ((k * 37) % 3); x1 = x - 90 - (k * 23) % 60
            d.rectangle([x1 - ln - 3, yy - 3, x1 + 3, yy + 9], fill=(60, 30, 10, 140)); d.rectangle([x1 - ln, yy, x1, yy + 6], fill=(255, 250, 235, 235))
        for k in range(5):
            dx = 50 + k * 50; a = int(210 * (1 - k / 5)); r = 18 + k * 7
            d.ellipse([x - dx - r, FY - 2 * r, x - dx + r, FY], fill=(170, 130, 90, a))
        pa(c, CRUN[int(t * 20) % len(CRUN)], x)
    elif name == 'farm':                        # Joy planting, saplings pop up one by one in her row
        pa(c, JPLANT[int(t * 9) % len(JPLANT)], 250)
        d.rectangle([380, FY - 14, 900, FY + 2], fill=(92, 62, 36, 255))
        for i, tr in enumerate(TREES):
            g = min(1.0, max(0.0, ((t % 2.6) - 0.3 - i * 0.45) / 0.3))
            if g <= 0: continue
            sc = g * (1 + 0.12 * math.sin(min(1, g) * math.pi))
            sp = tr.resize((max(1, int(tr.width * sc)), max(1, int(tr.height * sc))), Image.NEAREST)
            c.alpha_composite(sp, (int(450 + i * 135 - sp.width / 2), int(FY - 6 - sp.height)))
    elif name == 'boss':                        # Cleo slashing at a King Slime boss
        T = 13 / 24; u = (t % T) / T; k = min(12, int(u * 13))
        hit = 4 <= k <= 6
        ks = KING[int(t * 8) % len(KING)]
        if hit: ks = flash(ks, 0.6)
        c.alpha_composite(ks, (int(660 - 80 * 2 + (10 if hit else 0)), int(FY - 156 * 2)))
        pa(c, CATK[k], 330, base=104, cx=31)
        if hit:
            for j in range(5):
                a = j * 1.26 + t; r = 40 + 30 * (k - 4)
                d.rectangle([560 + r * math.cos(a) - 7, FY - 160 + r * math.sin(a) - 7, 560 + r * math.cos(a) + 7, FY - 160 + r * math.sin(a) + 7], fill=(255, 255, 255, 255))
    elif name == 'melee':                       # Cyrus fiery punch knocks a slime away
        T = 1.3; u = t % T; k = min(12, int(u * 24))
        pa(c, YATK[k], 300, base=104, cx=29)
        th = 3 / 24
        if u < th: c.alpha_composite(SLM[int(t * 10) % len(SLM)], (int(610 - 96), int(FY - 62 * 3)))
        else:
            v = u - th; sp = SLM[0].rotate(-600 * v, resample=Image.NEAREST, expand=True)
            if v < 0.6: c.alpha_composite(sp, (int(610 + 900 * v - sp.width / 2), int(FY - 62 * 3 - 700 * v + 500 * v * v)))
            elif u > 0.8: hop_in(c, (u - 0.8) / 0.5, t)
    elif name == 'magic':                       # Rayleigh's magic orb pops a slime
        T = 1.3; u = t % T; k = min(12, int(u * 20))
        pa(c, RATK[k], 260, base=104, cx=30)
        if u < 0.36: c.alpha_composite(SLM[int(t * 10) % len(SLM)], (int(640 - 96), int(FY - 62 * 3)))
        elif u > 0.8: hop_in(c, (u - 0.8) / 0.5, t)
        elif u < 0.7:
            v = (u - 0.36) / 0.34
            for j in range(10):
                a = j * 0.628; r = 30 + 160 * v
                d.rectangle([640 + r * math.cos(a) - 8, FY - 100 + r * math.sin(a) - 8, 640 + r * math.cos(a) + 8, FY - 100 + r * math.sin(a) + 8], fill=(225, 150, 255, int(255 * (1 - v))))
def hop_in(c, v, t):                            # next slime hops back in from the right
    x = 625 + 380 * (1 - v); y = FY - 62 * 3 - 110 * abs(math.sin(v * math.pi * 2))
    c.alpha_composite(SLM[int(t * 10) % len(SLM)], (int(x - 96), int(y)))
def option(text, k, t, glow, tw_max=CW):
    col = G[k][1]
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    g = GUMS[k]; fs = min(68, int((tw_max - 30 - g.width - 24) / len(text)))
    tw = d.textlength(text, font=F(fs)); x0 = (tw_max - (tw + 24 + g.width)) / 2
    d.text((x0, 30), text, font=F(fs), fill=col, stroke_width=9, stroke_fill=(14, 8, 22))
    bob = int(6 * math.sin(t * 4 + len(text))); gx, gy = int(x0 + tw + 24), int(30 + fs / 2 - g.height / 2 + bob)
    layer(c, lambda dd: dd.ellipse([gx - 16, gy - 16, gx + g.width + 16, gy + g.height + 16], fill=col + (int(60 + 40 * glow),)))
    c.alpha_composite(g, (gx, gy))
    act(c, ACT[text], t)
    return c
YA, YB = FA - (CH - 12), FB - (CH - 12)
print('options', YA, YB, 'seam', SEAM); assert YA >= HB - 10 and YB + CH <= 1500 and YB > SEAM + 40
T0 = 0.0; TQ = 2.6; TEND = T0 + TQ * NQ     # review fix: open on the first pair (no intro legend); legend only at the end
GRID_HOLD = 2.0; OUTRO = 0.4; DUR = TEND + 0.5 + GRID_HOLD + OUTRO
NF = int(round(DUR * FPS))
def qscene(img, qi, t, inn, out):
    a, ka, b, kb = QS[qi]
    put_realm(img, kb, t, FB, SEAM, H, ph=3)
    put_realm(img, ka, t, FA, 0, SEAM)
    layer(img, lambda d: d.polygon([(0, SEAM - 14), (W, SEAM - 44), (W, SEAM + 14), (0, SEAM + 44)], fill=(14, 10, 24, 255)))
    glow = 0.5 + 0.5 * math.sin(t * 6)
    ca = option(a, ka, t, glow); cb = option(b, kb, t, 1 - glow, tw_max=887 - CX0)
    xa = CX0 + (-1100) * (1 - inn) + 1100 * out; xb = CX0 + 1100 * (1 - inn) - 1100 * out
    img.alpha_composite(ca, (int(xa), YA)); img.alpha_composite(cb, (int(xb), YB))
    osc = max(0.0, min(inn, 1 - out))               # OR badge scales in/out with the options (never alone)
    if osc > 0.02:
        r = int((64 + 6 * math.sin(t * 5)) * osc); ox = CX0 + CW / 2; sy = SEAM
        layer(img, lambda dd: dd.ellipse([ox - r, sy - r, ox + r, sy + r], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=8))
        if osc > 0.5: d = ImageDraw.Draw(img); ctext(d, ox, sy - int(24 * osc), 'OR', F(max(8, int(48 * osc))), (20, 15, 35), 0)
PV = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] == 'preview' else None
wr = None if PV else Writer('v45_noaudio.mp4'); ev = []
for f in (range(NF) if not PV else [int(round(float(x) * FPS)) for x in PV]):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (12, 10, 20, 255))
    cl = 0; ctxt = 'COUNT YOUR COLORS'
    if t < TEND:
        qi = int((t - T0) // TQ); u = t - T0 - qi * TQ
        inn = 1.0 if qi == 0 else ease(u / 0.35); out = ease((u - (TQ - 0.3)) / 0.3)
        qscene(img, qi, t, inn, out)
        if qi == 0: cl = int(255 * min(1, max(0, (TQ - 0.3 - u) / 0.3)))   # COUNT YOUR COLORS under the hook for the first pair
    else:
        u = t - TEND
        oq = (u - 0.5 - GRID_HOLD) / OUTRO              # outro: the legend wipes off right, revealing pair 1 as it is on frame 0 (loop)
        if oq > 0: qscene(img, 0, t - DUR, ease(oq), 0.0)    # t - DUR: animation phases continue straight into frame 0
        Lg = Image.new('RGBA', (W, H), (12, 10, 20, 255)); legend_bg(Lg, t)
        for i, k in enumerate('FVER'):
            q = ease((u - i * 0.1) / 0.35); legend_row(Lg, i, k, t, -1100 * (1 - q))
        ox = int(1100 * ease(oq)) if oq > 0 else 0
        if ox < W: img.alpha_composite(Lg.crop((0, 0, W - ox, H)), (ox, 0))
        ctxt = 'TIE? FIRST PICK WINS'
        cl = int(255 * min(1, max(0, (u - 0.3) / 0.3))) if oq <= 0 else int(255 * max(0, 1 - oq * 2))
        if oq > 0.5: ctxt = 'COUNT YOUR COLORS'; cl = int(255 * min(1, (oq - 0.5) * 2))
    if cl: img.alpha_composite(SH) if cl == 255 else img.alpha_composite(Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 0)), SH, cl / 255))
    img.alpha_composite(HOOK)
    if cl: img.alpha_composite(count_line(cl, ctxt))
    if PV: img.convert('RGB').save(f'pv_{f:04d}.png'); continue
    wr.write(img)
if PV: sys.exit()
wr.close()
ev = [e for q in range(1, NQ) for e in ((round(T0 + q * TQ, 3), 'swish'), (round(T0 + q * TQ + 0.25, 3), 'ding_8bit'))] + [(round(TEND, 3), 'chime'), (round(DUR - OUTRO, 3), 'swish')]
json.dump({'events': ev}, open('v45_ev.json', 'w')); print('done', DUR, NF, ev)
