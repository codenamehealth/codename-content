import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #83 safe-zone + hook pass (source: fork_b8/r85.py): mirror frame 5x -> 4x (shapes unchanged size), Rayleigh moved beside it.
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
HOOK, HB = hook_layer(['PAUSE WHEN IT', 'PERFECTLY MIRRORS'], accent=1, color=(190, 140, 255), sub='ONLY 1 FRAME PER SHAPE', border=(255, 214, 60))
print('hook bottom', HB)
MK = 4; MIR = up(Image.open(B8 + 'mirror/00.png').convert('RGBA'), MK)          # 640x800
MX, MY = 478 - MIR.width // 2, HB + 14
GX0, GY0, GX1, GY1 = MX + 8 * MK + 21, MY + 9 * MK + 22, MX + 152 * MK - 21, MY + 194 * MK - 22   # glass area
CXM = (GX0 + GX1) // 2; CYM = (GY0 + GY1) // 2 + 10
def hollow_head():
    im = Image.open(SP0 + 'syeda_src/hollow/char1.png').convert('RGBA'); return crop(im)
SHAPES = [('THE ACV GUMMY', crop(Image.open(SP0 + 'pixellab/gummies/pick_acv.png').convert('RGBA')), 12),
          ('THE MELATONIN GUMMY', crop(Image.open(SP0 + 'pixellab/gummies/pick_mel.png').convert('RGBA')), 11),
          ('THE HOLLOW', hollow_head(), 7),
          ('THE MUSHROOM GUMMY', crop(Image.open(SP0 + 'pixellab/gummies/pick_mush.png').convert('RGBA')), 14),
          ('THE ACV POTION', crop(Image.open(SP0 + 'fork_b5/jar_native.png').convert('RGBA')), 9)]
def halves(im, k):
    w = im.width; hw = w // 2
    left = im.crop((0, 0, hw, im.height))
    L = up(left, k); Rr = up(left.transpose(Image.FLIP_LEFT_RIGHT), k)
    return L, Rr, hw * k
T_IN = 1.6; SEG = 2.7; OUTRO = 3.0
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
RAY = idle('ray', 3); RAYX = 760 - 28 * 3; RAYF = 1290   # content x760-886, feet on the courtyard ground beside the mirror
END = T_IN + 5 * SEG + OUTRO; NF = int(END * FPS)
wr = Writer('v83_noaudio.mp4'); events = []
STAR = [(random.uniform(GX0, GX1), random.uniform(GY0, GY1), random.uniform(0, 6)) for _ in range(30)]
for f in range(NF):
    t = f / FPS
    bg = BGF[int(t * 6) % len(BGF)]; img = Image.new('RGBA', (W, H), (12, 8, 20, 255))
    bgc = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, bg.height)); img.alpha_composite(bgc, (0, 200))  # raised 100px so the castle's dark statue stays behind the smaller mirror
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
        text_layer(img, [(478, MY + MIR.height + 12, f'SHAPE {i + 1}/5', 40, (255, 214, 60), 6, 255), (478, MY + MIR.height + 66, name, 34, (230, 220, 255), 6, 255)])
        # progress bar for this shape
        layer(img, lambda dd: (dd.rounded_rectangle([168, MY + MIR.height + 118, 788, MY + MIR.height + 142], 10, fill=(20, 14, 40, 220)), dd.rounded_rectangle([168, MY + MIR.height + 118, 168 + 620 * min(1, u0 / SEG), MY + MIR.height + 142], 10, fill=(190, 130, 255, 255))))
        if abs(u0) < 0.5 / FPS: events.append((round(t, 3), 'whoosh_8bit'))
    img.alpha_composite(MIR, (MX, MY))
    # Rayleigh casting at the side
    rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (RAYX, RAYF - 78 * 3))
    if i is not None:
        layer(img, lambda dd: [dd.rectangle([RAYX + 186 + 40 * math.cos(t * 6 + q), RAYF - 160 + 30 * math.sin(t * 6 + q), RAYX + 194 + 40 * math.cos(t * 6 + q), RAYF - 152 + 30 * math.sin(t * 6 + q)], fill=(200, 160, 255, 220)) for q in range(4)])
    # header
    if t < T_IN:
        text_layer(img, [(CXM, CYM - 40, 'PLAY ALONG', 56, (255, 255, 255), 8, int(255 * min(1, (T_IN - t) / 0.4)))])
        if f == 0: events.append((0.1, 'chime'))
    if t >= T_IN + 5 * SEG:
        u = t - T_IN - 5 * SEG
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(160 * min(1, u / 0.3)))))
        text_layer(img, [(478, 860, 'DID YOU GET A', 52, (255, 255, 255), 8, 255), (478, 940, 'PERFECT MIRROR?', 52, (190, 140, 255), 8, 255),
                         (478, 1070, 'Comment how many', 34, (255, 214, 60), 6, int(255 * min(1, max(0, u - 0.5) / 0.4))), (478, 1120, 'you nailed (0 to 5)', 34, (255, 214, 60), 6, int(255 * min(1, max(0, u - 0.5) / 0.4)))])
        if abs(u) < 0.5 / FPS: events.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (60, 250): img.convert('RGB').save(f'f83_{f}.png')
    if any(abs(f - round(ts * FPS)) == 0 for ts in TSTAR): img.convert('RGB').crop((GX0, GY0, GX1, GY1)).resize(((GX1 - GX0) // 2, (GY1 - GY0) // 2)).save(f'm83_{f}.png')
wr.close(); json.dump(events, open('v83_ev.json', 'w')); print('done', END)
