import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #83 safe-zone + hook pass (source: fork_b8/r85.py): mirror frame 5x -> 4x (shapes unchanged size), Rayleigh moved beside it.
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import hook as HK
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), border=None, subcol=(255, 255, 255)):
    f, s = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=border or color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
HOOK, HB = band(['PAUSE WHEN IT', 'PERFECTLY MIRRORS'], 1, 'COMMENT YOUR SCORE', color=(190, 140, 255), border=(255, 214, 60), subcol=(255, 214, 60))
OLDHB = HB
HOOK, HB = HK.hook_fade(['PAUSE WHEN IT', 'PERFECTLY MIRRORS'], accent=1, color=(190, 140, 255))   # hfg9: soft fade, no box, comment line cut
HOOK_END, _ = HK.hook_fade(['HOW MANY OF 5', 'DID YOU GET?'], accent=1)   # end question replaces the hook text
print('hook bottom', HB, 'old', OLDHB)
MK = 4; MIR = up(Image.open(B8 + 'mirror/00.png').convert('RGBA'), MK)          # 640x800
MX, MY = 78, OLDHB + 14;   # hfg9: mirror kept exactly where it was
LX = 412   # rc9: mirror moved left so Rayleigh can stand beside it at 4x
GX0, GY0, GX1, GY1 = MX + 8 * MK + 21, MY + 9 * MK + 22, MX + 152 * MK - 21, MY + 194 * MK - 22   # glass area
CXM = (GX0 + GX1) // 2; CYM = (GY0 + GY1) // 2 + 10
def hollow_head():
    im = Image.open(SP0 + 'syeda_src/hollow/char1.png').convert('RGBA'); return crop(im)
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
SHAPES = [('ACV GUMMY', crop(acv_gummy_strong()), 12),   # Syeda's ACV gummy + gummy shine (VETTING); mirrored half carries it too
          ('MELATONIN GUMMY', crop(Image.open(SP0 + 'pixellab/gummies/pick_mel.png').convert('RGBA')), 11),
          ('THE HOLLOW', hollow_head(), 7),
          ('MUSHROOM GUMMY', crop(Image.open(SP0 + 'pixellab/gummies/pick_mush.png').convert('RGBA')), 14),
          ('THE ACV POTION', crop(Image.open(SP0 + 'fork_b5/jar_native.png').convert('RGBA')), 9)]
def halves(im, k):
    w = im.width; hw = w // 2
    left = im.crop((0, 0, hw, im.height))
    L = up(left, k); Rr = up(left.transpose(Image.FLIP_LEFT_RIGHT), k)
    return L, Rr, hw * k
T_IN = 0.0; SEG = 2.7; OUTRO = 1.5   # rc9: shape 1 moving from frame 0 (static PLAY ALONG cut), end card 1.5s then loop
def make(seed):
  rng = random.Random(seed); P = []; TS = []
  for i in range(5):
    ts = T_IN + i * SEG + rng.uniform(0.95, 1.75)
    ts = round(ts * FPS) / FPS
    A = rng.uniform(170, 230); B = rng.uniform(90, 140); w1 = rng.uniform(2.3, 2.9); w2 = w1 * rng.choice([1.618, 1.414, 0.707]); ph = rng.choice([0, math.pi])
    P.append((ts, A, B, w1, w2, ph)); TS.append(ts)
  return P, TS
def offset(i, t):
    ts, A, B, w1, w2, ph = PARAMS[i]; u = t - ts
    k = SHAPES[i][2]
    dx = A * math.sin(w1 * u + ph) + 40 * u; dy = B * math.sin(w2 * u)
    return int(round(dx / k)) * k, int(round(dy / k)) * k
def check():
  worst = 99
  for i in range(5):
    t0 = T_IN + i * SEG; fr = [f for f in range(int(t0 * FPS), int((t0 + SEG) * FPS))]
    near = [(f, offset(i, f / FPS)) for f in fr]
    zero = [f for f, o in near if o == (0, 0)]
    if len(zero) != 1: return -1
    worst = min(worst, min(max(abs(o[0]), abs(o[1])) for f, o in near if f not in zero) / SHAPES[i][2])
  return worst
for sd in range(11, 400):
    PARAMS, TSTAR = make(sd)
    if check() >= 2: print('param seed', sd); break
# verify uniqueness
for i in range(5):
    t0 = T_IN + i * SEG; fr = [f for f in range(int(t0 * FPS), int((t0 + SEG) * FPS))]
    near = [(f, offset(i, f / FPS)) for f in fr]
    zero = [f for f, o in near if o == (0, 0)]
    others = min(max(abs(o[0]), abs(o[1])) for f, o in near if f not in zero)
    print('shape', i, 'perfect frames', zero, 'tstar', round(TSTAR[i] * FPS), 'closest other px', others)
BGF = bg_frames('bg_castle.gif', (int(1600 * 1.8), int(900 * 1.8)), step=2, bright=0.5)
RAY = idle('ray', 4); RAYX = 700 - 28 * 4; RAYF = 1300   # rc9: Rayleigh 3x -> 4x (~256px), figure x700-876   # content x760-886, feet on the courtyard ground beside the mirror
END = T_IN + 5 * SEG + OUTRO; NF = int(END * FPS)
wr = Writer('v83_noaudio.mp4'); events = []
STAR = [(random.uniform(GX0, GX1), random.uniform(GY0, GY1), random.uniform(0, 6)) for _ in range(30)]
for f in range(NF):
    t = f / FPS
    bg = BGF[int(t * 6) % len(BGF)]; img = Image.new('RGBA', (W, H), (12, 8, 20, 255))
    bgc = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, bg.height)); img.alpha_composite(bgc, (0, 200)); img.alpha_composite(bgc.crop((0, 0, W, 200)).transpose(Image.FLIP_TOP_BOTTOM), (0, 0))   # hfg9: no flat dark band at the top  # raised 100px so the castle's dark statue stays behind the smaller mirror
    img.alpha_composite(bgc.crop((0, bgc.height - 120, W, bgc.height)).transpose(Image.FLIP_TOP_BOTTOM), (0, 200 + bgc.height))
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 6, 24, 90)))
    # glass
    layer(img, lambda d: [d.rectangle([GX0, GY0 + k * 20, GX1, GY0 + k * 20 + 20], fill=(30 + k, 30 + k, 70 + k * 2, 235)) for k in range((GY1 - GY0) // 20 + 1)])
    layer(img, lambda d: [d.rectangle([sx - 2, sy - 2, sx + 2, sy + 2], fill=(200, 210, 255, int(120 + 120 * math.sin(t * 3 + ph)))) for sx, sy, ph in STAR])
    i = int((t - T_IN) // SEG) if T_IN <= t < T_IN + 5 * SEG else None
    d = ImageDraw.Draw(img)
    if i is not None:
        name, im, k = SHAPES[i]; L, Rr, hwk = halves(im, k)
        u0 = t - T_IN - i * SEG
        a = min(1, u0 / 0.25)
        cy = CYM - L.height // 2
        # dashed mirror line
        for yy in range(GY0 + 10, GY1 - 10, 24): d.rectangle([CXM - 2, yy, CXM + 2, yy + 12], fill=(220, 200, 255))
        gl = Image.new('RGBA', (GX1 - GX0, GY1 - GY0), (0, 0, 0, 0))
        gl.alpha_composite(L, (CXM - hwk - GX0, cy - GY0))
        ox, oy = offset(i, t)
        ghost = Rr.copy(); al = ghost.getchannel('A').point(lambda p: int(p * 0.92)); ghost.putalpha(al)
        gl.alpha_composite(ghost, (CXM + ox - GX0, cy + oy - GY0))
        img.alpha_composite(gl, (GX0, GY0))
        text_layer(img, [(LX, MY + MIR.height + 12, f'SHAPE {i + 1}/5', 44, (255, 214, 60), 7, 255)])   # hfg9: shape names cut
        # progress bar for this shape
        layer(img, lambda dd: (dd.rounded_rectangle([LX - 310, MY + MIR.height + 72, LX + 310, MY + MIR.height + 94], 10, fill=(20, 14, 40, 220)), dd.rounded_rectangle([LX - 310, MY + MIR.height + 72, LX - 310 + 620 * min(1, u0 / SEG), MY + MIR.height + 94], 10, fill=(190, 130, 255, 255))))
        if abs(u0) < 0.5 / FPS: events.append((round(t, 3), 'swish'))
    img.alpha_composite(MIR, (MX, MY))
    # Rayleigh casting at the side
    rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (RAYX, RAYF - 78 * 4))
    if i is not None:
        layer(img, lambda dd: [dd.rectangle([RAYX + 248 + 28 * math.cos(t * 6 + q), RAYF - 216 + 28 * math.sin(t * 6 + q), RAYX + 258 + 28 * math.cos(t * 6 + q), RAYF - 206 + 28 * math.sin(t * 6 + q)], fill=(200, 160, 255, 220)) for q in range(4)])
    # header
    if False:   # hfg9: ONLY 1 FRAME / PER SHAPE cut (the hook is the instruction); the rule floats over the moving first shape (top of the glass), then clears well before its one perfect frame
        layer(img, lambda dd: dd.rounded_rectangle([CXM - 300, GY0 + 16, CXM + 300, GY0 + 150], 18, fill=(14, 10, 24, 215), outline=(255, 214, 60, 255), width=5))
        text_layer(img, [(CXM, GY0 + 32, 'ONLY 1 FRAME', 48, (255, 255, 255), 8, 255), (CXM, GY0 + 90, 'PER SHAPE', 48, (255, 214, 60), 8, 255)])
    if t >= T_IN + 5 * SEG:
        u = t - T_IN - 5 * SEG
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, 160)))
        if abs(u) < 0.5 / FPS: events.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK_END if t >= T_IN + 5 * SEG else HOOK)
    wr.write(img)
    if f in (0, 30, 250, NF - 1, 32, 126, 195, 291, 361): img.convert('RGB').save(f'f83_{f}.png')
    if any(abs(f - round(ts * FPS)) == 0 for ts in TSTAR): img.convert('RGB').crop((GX0, GY0, GX1, GY1)).resize(((GX1 - GX0) // 2, (GY1 - GY0) // 2)).save(f'm83_{f}.png')
wr.close(); json.dump({'events': sorted(events)}, open('v83_ev.json', 'w')); print('done', END)
