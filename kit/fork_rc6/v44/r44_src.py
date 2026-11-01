import sys; sys.path.insert(0, '../fork1'); sys.path.insert(0, '../pixellab/safezone')
from hook import hook_layer
from common import *
import numpy as np
from PIL import ImageFilter
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
# background: Liza's moon temple, darkened and softened so the tracks pop
BG = bg_frames('recov_hd.gif', (W, H), box=(677, 0, 1284, 1080), step=1, bright=0.42, blur=2)
LANES = [215, 385, 555, 725]
L = 7600.0; Y0 = 560.0                       # world track length, start row world y
SEG = 12
# build crossing paths: each segment a permutation step, smooth cosine blend + wobble
perm = [0, 1, 2, 3]; keys = [list(perm)]
for k in range(SEG):
    p = list(keys[-1])
    if rnd.random() < 0.55:
        i = rnd.randrange(3); p[i], p[i + 1] = p[i + 1], p[i]
    else:
        i, j = rnd.sample(range(4), 2); p[i], p[j] = p[j], p[i]
    keys.append(p)
WOB = [(rnd.uniform(40, 120), rnd.uniform(1.5, 3.5), rnd.uniform(0, 6.28)) for _ in range(4)]
WOB = [(a * 0.6, b, c) for a, b, c in WOB]
def X(i, y):
    u = max(0.0, min(1.0, (y - Y0) / (L - Y0))) * SEG
    k = min(SEG - 1, int(u)); f = u - k; s = 0.5 - 0.5 * math.cos(math.pi * f)
    a = LANES[keys[k].index(i)]; b = LANES[keys[k + 1].index(i)]
    amp, fr, ph = WOB[i]
    env = math.sin(math.pi * f)            # wobble vanishes at segment ends so lanes line up
    return a + (b - a) * s + amp * env * math.sin(fr * math.pi * f * 2 + ph + k)
TARGET = 1
print('target ends at lane', 'ABCD'[keys[-1].index(TARGET)])
T0, T1, TE = 2.6, 16.6, 21.9
def prog(t):                                # eased progress with acceleration
    if t <= T0: return 0.0
    if t >= T1: return 1.0
    u = (t - T0) / (T1 - T0); return u ** 1.55
CAM_Y = 960                                  # screen y where the gummies ride
GUM = gummy('gold', 3)
TIERS = [(T0 + 1.0, '100% STILL WITH IT', (120, 230, 110)), (T0 + 4.5, 'TOP 30% KEEP UP', (255, 214, 60)),
         (T0 + 8.0, 'TOP 5% REMAINING', (255, 150, 60)), (T0 + 11.0, 'TOP 1% ELITE', (255, 90, 90))]
# precompute track polylines in world coords
YS = np.arange(Y0, L + 1, 6.0)
PTS = [[(X(i, y), y) for y in YS] for i in range(4)]
HOOK, HB = hook_layer(['LOCK YOUR EYES'], sub='ON THE GLOWING GUMMY', sub_color=(255, 214, 60))
print('hook bottom', HB)
NF = int(TE * FPS); wr = Writer('v44_noaudio.mp4'); ev = []
last_tier = None; F64 = F(58); F28 = F(28); F36 = F(36)
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 8) % len(BG)].copy()
    wy = Y0 + prog(t) * (L - Y0)            # gummies' world y
    if wy <= Y0 + 0.01: cam = Y0 - (CAM_Y - 0) + (CAM_Y - 700)          # start row sits at screen y 700
    else: cam = wy - CAM_Y
    cam = max(Y0 - 700, min(cam, L - 1340))  # finish row lands at screen y 1340
    if wy < Y0 + 1: cam = Y0 - 700
    # tracks with glow
    G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(G)
    for i in range(4):
        pts = [(x, y - cam) for x, y in PTS[i] if -60 < y - cam < H + 60]
        if len(pts) > 1: gd.line(pts, fill=(80, 190, 255, 120), width=26, joint='curve')
    G = G.filter(ImageFilter.GaussianBlur(9)); img.alpha_composite(G)
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(Lr)
    for i in range(4):
        pts = [(x, y - cam) for x, y in PTS[i] if -60 < y - cam < H + 60]
        if len(pts) > 1:
            ld.line(pts, fill=(60, 120, 230, 255), width=12, joint='curve'); ld.line(pts, fill=(150, 215, 255, 255), width=5, joint='curve')
    # start / finish rows
    sy = Y0 - cam; fy = L - cam
    if -40 < sy < H:
        ld.line([(140, sy), (800, sy)], fill=(255, 214, 60, 255), width=4)
        ctext(ld, 470, sy - 130, 'START', F28, (255, 214, 60), 5)
    if -40 < fy < H:
        ld.line([(140, fy), (800, fy)], fill=(255, 255, 255, 255), width=4)
        for k, lx in enumerate(LANES):
            ld.ellipse([lx - 34, fy + 40, lx + 34, fy + 108], fill=(20, 16, 40, 255), outline=(255, 214, 60, 255), width=5)
            ctext(ld, lx, fy + 58, 'ABCD'[k], F(34), (255, 255, 255), 0)
        ctext(ld, 470, fy - 130, 'FINISH', F28, (255, 255, 255), 5)
    img.alpha_composite(Lr)
    # gummies
    GL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gld = ImageDraw.Draw(GL)
    glow = 1.0 if t < T0 - 0.3 else max(0.0, 1 - (t - (T0 - 0.3)) / 0.6)
    for i in range(4):
        x = X(i, max(wy, Y0)); y = max(wy, Y0) - cam
        if i == TARGET and glow > 0:
            pul = 0.5 + 0.5 * math.sin(t * 8)
            for r, a in ((120, 70), (92, 120), (68, 170)):
                gld.ellipse([x - r, y - r, x + r, y + r], fill=(255, 225, 100, int(a * glow * (0.7 + 0.3 * pul))))
            for k in range(8):
                ang = k * math.pi / 4 + t * 1.5; r1, r2 = 70, 130 + 12 * pul
                gld.line([(x + r1 * math.cos(ang), y + r1 * math.sin(ang)), (x + r2 * math.cos(ang), y + r2 * math.sin(ang))], fill=(255, 245, 170, int(220 * glow)), width=6)
    img.alpha_composite(GL)
    for i in range(4):
        x = X(i, max(wy, Y0)); y = max(wy, Y0) - cam
        bob = int(3 * math.sin(t * 9 + i))
        img.alpha_composite(GUM, (int(x - GUM.width / 2), int(y - GUM.height / 2 + bob)))
    # header and text
    items = []
    TL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(TL)
    img.alpha_composite(TL)
    cur = None
    for (ts, txt, col) in TIERS:
        if t >= ts and t < T1 + 0.2: cur = (ts, txt, col)
    if cur:
        a = int(255 * min(1, (t - cur[0]) / 0.25))
        items.append((W / 2, HB + 22, cur[1], 30, cur[2], 5, a))
        if last_tier != cur[1]: ev.append((round(cur[0], 3), 'whoosh_8bit')); last_tier = cur[1]
    if t < T0:
        items.append((478, 1230, "DON'T LOSE IT...", 40, (255, 255, 255), 6, 255))
        n = 3 - int(t / (T0 / 3))
        if t > 0.3: items.append((478, 1310, 'GET READY', 28, (200, 200, 220), 4, 255))
    if T0 <= t < T0 + 0.6: items.append((478, 1230, 'GO!', 64, (120, 230, 110), 8, int(255 * (1 - (t - T0) / 0.6))))
    if t >= T1:
        u = t - T1; a = int(255 * min(1, u / 0.3))
        layer(img, lambda d: d.rounded_rectangle([110, HB + 70, 970, HB + 330], 20, fill=(12, 8, 24, int(200 * a / 255))))
        items += [(W / 2, HB + 100, 'WHICH LETTER?', 56, (255, 214, 60), 8, a), (W / 2, HB + 190, 'COMMENT YOUR ANSWER NOW', 30, (255, 255, 255), 5, a)]
        n = 5 - int(u / 0.95)
        if n >= 1: items.append((W / 2, HB + 245, str(n), 64, (255, 255, 255), 8, a))
    text_layer(img, items)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p44_{f:04d}.png')
wr.close()
# sounds: go, crossings ticks (sparse), finish ding, countdown ticks
ev.append((round(T0, 3), 'go_8bit'))
for k in range(1, SEG):
    tk = None
    target_y = Y0 + k / SEG * (L - Y0)
    for f in range(int(T0 * FPS), int(T1 * FPS)):
        if Y0 + prog(f / FPS) * (L - Y0) >= target_y: tk = f / FPS; break
    if tk: ev.append((round(tk, 3), 'tick_8bit'))
ev.append((round(T1, 3), 'ding_8bit'))
for n in range(5):
    ev.append((round(T1 + n * 0.95, 3), 'tick_8bit'))
pass; print('done', TE)
