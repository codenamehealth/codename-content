# hfg4 pass of #45 (from fork_rc6/v45/r45.py). Same questions, order and timing (audio reused).
# Changes: soft-fade hook (no box, no 'Comment your guild'); COUNT YOUR COLORS as one line inside the fade (intro + loop);
# legend = the 4 realm strips edge to edge with each guide standing on its own realm (no panels, names only, product lines cut);
# questions = the two realm halves are the options (no cards): option words in the guild colour, guide + jar + gummy standing
# on the realm's ground; QUESTION n/4 plate + bar cut; end = the legend slides back in under WHICH GUILD ARE YOU? (2x2 grid
# and the MOST PICKED COLOR = YOUR GUILD plate cut), then slides out right and frame 0 slides it in from the left (loop).
import sys, math, json, random, os
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
      ('ONE MORE LEVEL', 'E', 'SAVE AND LOG OFF', 'R')]
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
def count_line(a):                              # the one instruction, inside the same fade under the hook
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ctext(d, W / 2, HB + 6, 'COUNT YOUR COLORS', F(44), (255, 255, 255), 7, a); return L
SH = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # deepen the fade a little under the instruction line
_g = Image.new('L', (1, H), 0)
for yy in range(H): _g.putpixel((0, yy), int(120 * max(0.0, min(1.0, (HB + 110 - yy) / 160))) if yy > HB - 50 else 0)
_s = Image.new('RGBA', (W, H), (8, 6, 16, 255)); _s.putalpha(_g.resize((W, H))); SH.alpha_composite(_s)
# ---- legend: 4 realm strips edge to edge, rows inside the safe zone
LY0 = HB + 72; RWH = (1498 - LY0) // 4
ROWS = [(LY0 + i * RWH, LY0 + (i + 1) * RWH) for i in range(4)]
print('legend rows', ROWS)
def legend_bg(img, t):
    for i, k in enumerate('FVER'):
        y0 = 0 if i == 0 else ROWS[i][0]; y1 = H if i == 3 else ROWS[i][1]
        put_realm(img, k, t, ROWS[i][1] - 12, y0, y1, ph=i)
    layer(img, lambda d: [d.rectangle([0, ROWS[i][0] - 3, W, ROWS[i][0] + 3], fill=(12, 8, 20, 255)) for i in range(1, 4)])
def legend_row(img, i, k, t, dx):
    y0, y1 = ROWS[i]; feet = y1 - 12; R = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fr = IDL[k][int(t * 8) % 6]; R.alpha_composite(fr, (int(150 - fr.width / 2), feet - 78 * 3))
    js = JARS[k]; R.alpha_composite(js, (300, feet - js.height))
    g = GUM[k]; gx, gy = 470, feet - g.height - 22 + int(8 * math.sin(t * 4 + i))
    layer(R, lambda d: d.ellipse([gx - 22, gy - 22, gx + g.width + 22, gy + g.height + 22], fill=G[k][1] + (70,)))
    R.alpha_composite(g, (gx, gy))
    d = ImageDraw.Draw(R); f_ = F(52); assert 290 + d.textlength(G[k][0], font=f_) <= (1025 if y1 <= 1110 else 887), G[k][0]
    d.text((290, y0 + 16), G[k][0], font=f_, fill=G[k][1], stroke_width=8, stroke_fill=(16, 10, 26))
    if dx: R = R.transform(R.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0))
    img.alpha_composite(R)
# ---- questions: the two realm halves are the two options
FA, FB = 900, 1452                              # guide feet for option A (top) and B (bottom)
CW, CH = 800, 370; CX0 = 78
SEAM = (FA + FB - CH + 12) // 2 + 18
def option(text, k, t, glow):
    col = G[k][1]
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    fs = min(68, int((CW - 40) / len(text)))
    ctext(d, CW / 2, 30, text, F(fs), col, 9, sc=(14, 8, 22))
    fr = IDL4[k][int(t * 8) % len(IDL4[k])]
    c.alpha_composite(fr, (-50, CH - 12 - 312))
    j = JAR[k]; c.alpha_composite(j, (CW // 2 - j.width // 2 + 10, CH - 12 - j.height))
    g = GUM[k]; bob = int(10 * math.sin(t * 4 + len(text)))
    gx, gy = CW - 200, 190 + bob
    layer(c, lambda dd: dd.ellipse([gx - 30, gy - 30, gx + g.width + 30, gy + g.height + 30], fill=col + (int(60 + 40 * glow),)))
    c.alpha_composite(g, (gx, gy))
    for s in range(4):
        a = t * 3 + s * 1.57; sx, sy = gx + g.width / 2 + 70 * math.cos(a), gy + g.height / 2 + 50 * math.sin(a)
        d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 200))
    return c
YA, YB = FA - (CH - 12), FB - (CH - 12)
print('options', YA, YB, 'seam', SEAM); assert YA >= HB - 10 and YB + CH <= 1500 and YB > SEAM + 40
T0 = 2.4; TQ = 2.6; TEND = T0 + TQ * NQ
GRID_HOLD = 2.0; OUTRO = 0.4; DUR = TEND + 0.5 + GRID_HOLD + OUTRO
NF = int(round(DUR * FPS))
wr = Writer('v45_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (12, 10, 20, 255))
    cl = 0
    if t < T0:
        legend_bg(img, t)
        for i, k in enumerate('FVER'):
            u = ease((t + 0.08 - i * 0.12) / 0.4); legend_row(img, i, k, t, -900 * (1 - u))   # legend already mid-slide on frame 0
        cl = 255
    elif t < TEND:
        qi = int((t - T0) // TQ); u = t - T0 - qi * TQ
        a, ka, b, kb = QS[qi]
        put_realm(img, kb, t, FB, SEAM, H, ph=3)
        put_realm(img, ka, t, FA, 0, SEAM)
        layer(img, lambda d: d.polygon([(0, SEAM - 14), (W, SEAM - 44), (W, SEAM + 14), (0, SEAM + 44)], fill=(14, 10, 24, 255)))
        inn = ease(u / 0.35); out = ease((u - (TQ - 0.3)) / 0.3)
        glow = 0.5 + 0.5 * math.sin(t * 6)
        ca = option(a, ka, t, glow); cb = option(b, kb, t + 1, 1 - glow)
        xa = CX0 + (-1100) * (1 - inn) + 1100 * out; xb = CX0 + 1100 * (1 - inn) - 1100 * out
        img.alpha_composite(ca, (int(xa), YA)); img.alpha_composite(cb, (int(xb), YB))
        osc = max(0.0, min(inn, 1 - out))               # OR badge scales in/out with the options (never alone)
        if osc > 0.02:
            r = int((64 + 6 * math.sin(t * 5)) * osc); ox = CX0 + CW / 2; sy = SEAM
            layer(img, lambda dd: dd.ellipse([ox - r, sy - r, ox + r, sy + r], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=8))
            if osc > 0.5: d = ImageDraw.Draw(img); ctext(d, ox, sy - int(24 * osc), 'OR', F(max(8, int(48 * osc))), (20, 15, 35), 0)
        if u < 1 / FPS - 1e-6: ev.append((round(t, 3), 'swish')); ev.append((round(t + 0.25, 3), 'ding_8bit'))
    else:
        u = t - TEND
        legend_bg(img, t)
        oq = (u - 0.5 - GRID_HOLD) / OUTRO              # outro: rows slide out right; frame 0 slides them in from the left (loop)
        for i, k in enumerate('FVER'):
            q = ease((u - i * 0.1) / 0.35)
            dx = -1100 * (1 - q) + (1100 * ease((oq * OUTRO - i * 0.05) / (OUTRO - 0.15)) if oq > 0 else 0)
            legend_row(img, i, k, t, dx)
        if oq > 0: cl = int(255 * min(1, oq))
    if cl: img.alpha_composite(SH) if cl == 255 else img.alpha_composite(Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 0)), SH, cl / 255))
    img.alpha_composite(HOOK)
    if cl: img.alpha_composite(count_line(cl))
    wr.write(img)
    if f in (0, 12, 60, 80, 150, 300, 390, 420, 445, NF - 1): img.convert('RGB').save(f'p45_{f:04d}.png')
wr.close()
ev += [(0.0, 'swish'), (round(TEND, 3), 'chime')]
json.dump({'events': ev}, open('v45_ev.json', 'w')); print('done', DUR, NF)
