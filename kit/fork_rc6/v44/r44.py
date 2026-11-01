# rc6 recut of #44 (approved by Bennett): universal + legibility fixes only. Source: fork_sz44/r44.py (seed 7, target ends at C)
import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); sys.path.insert(0, SP0 + 'pixellab/safezone')
from hook import _fit, X0 as HX0, X1 as HX1, Y0 as HY0
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import ImageFilter
rnd = random.Random(7)
BG = bg_frames('recov_hd.gif', (W, H), box=(677, 0, 1284, 1080), step=1, bright=0.42, blur=2)
LANES = [200, 393, 587, 780]                 # was 215-725 (spacing 170) -> spacing ~193 for the 2x gummies
L = 7600.0; Y0 = 560.0
SEG = 12
perm = [0, 1, 2, 3]; keys = [list(perm)]
for k in range(SEG):
    p = list(keys[-1])
    if rnd.random() < 0.55:
        i = rnd.randrange(3); p[i], p[i + 1] = p[i + 1], p[i]
    else:
        i, j = rnd.sample(range(4), 2); p[i], p[j] = p[j], p[i]
    keys.append(p)
WOB = [(rnd.uniform(40, 120), rnd.uniform(1.5, 3.5), rnd.uniform(0, 6.28)) for _ in range(4)]
WOB = [(a * 0.4, b, c) for a, b, c in WOB]   # wobble 0.6 -> 0.4 so the bigger gummies stay inside the safe zone
def X(i, y):
    u = max(0.0, min(1.0, (y - Y0) / (L - Y0))) * SEG
    k = min(SEG - 1, int(u)); f = u - k; s = 0.5 - 0.5 * math.cos(math.pi * f)
    a = LANES[keys[k].index(i)]; b = LANES[keys[k + 1].index(i)]
    amp, fr, ph = WOB[i]
    env = math.sin(math.pi * f)
    return a + (b - a) * s + amp * env * math.sin(fr * math.pi * f * 2 + ph + k)
TARGET = 1
END = 'ABCD'[keys[-1].index(TARGET)]; print('target ends at lane', END); assert END == 'C'
T0, T1 = 1.0, 10.5                           # GO at 1.0s (was 2.6s), finish at 10.5s (was 16.6s)
CD = 0.8; TE = T1 + 3 * CD                   # 3-2-1 countdown (was 5)
def prog(t):
    if t <= T0: return 0.0
    if t >= T1: return 1.0
    u = (t - T0) / (T1 - T0); return u ** 1.35
GUM = gummy('gold', 6)                       # 3x -> 6x
# hook band: same look as hook.py; hook words unchanged; comment ask as a real 44px line from frame 0
def band():
    f1, s1 = _fit(['LOCK YOUR EYES'], HX1 - HX0 - 40)
    f2 = F(44); pad = 24; gap = 18
    h = pad + s1 + gap + 44 + 30 + 44 + pad
    Lb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(Lb)
    d.rounded_rectangle([HX0, HY0, HX1, HY0 + h], 22, fill=(14, 10, 24, 232), outline=(255, 214, 60), width=6)
    y = HY0 + pad
    for txt, ft, col, sw, sz in (('LOCK YOUR EYES', f1, (255, 255, 255), 9, s1), ('ON THE GLOWING GUMMY', f2, (255, 214, 60), 7, 44)):
        w = d.textlength(txt, font=ft); assert w <= HX1 - HX0 - 30, txt
        d.text(((HX0 + HX1) / 2 - w / 2, y), txt, font=ft, fill=col, stroke_width=sw, stroke_fill=(10, 6, 18)); y += sz + gap
    y += 4; d.line([(HX0 + 60, y), (HX1 - 60, y)], fill=(255, 214, 60, 120), width=3); y += 14
    w = d.textlength('Comment A, B, C or D', font=f2)
    d.text(((HX0 + HX1) / 2 - w / 2, y), 'Comment A, B, C or D', font=f2, fill=(240, 240, 240), stroke_width=6, stroke_fill=(10, 6, 18))
    return Lb, HY0 + h
HOOK, HB = band(); print('hook bottom', HB)
TIERS = [(T0 + 0.6, '100%', 'STILL WITH IT', (120, 230, 110)), (T0 + 3.0, 'TOP 30%', 'KEEP UP', (255, 214, 60)),
         (T0 + 5.3, 'TOP 5%', 'REMAINING', (255, 150, 60)), (T0 + 7.4, 'TOP 1%', 'ELITE', (255, 90, 90))]
DOCK = HB + 16                               # docked tier line under the band
YS = np.arange(Y0, L + 1, 6.0)
PTS = [[(X(i, y), y) for y in YS] for i in range(4)]
CAM_Y = 1000; START_Y = 800; FIN_Y = 1300
NF = int(round(TE * FPS)); wr = Writer('v44_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 8) % len(BG)].copy()
    wy = Y0 + prog(t) * (L - Y0)
    cam = max(Y0 - START_Y, min(wy - CAM_Y, L - FIN_Y))
    # tracks: dimmer, thinner strings so the gummies are what you follow
    G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(G)
    for i in range(4):
        pts = [(x, y - cam) for x, y in PTS[i] if -60 < y - cam < H + 60]
        if len(pts) > 1: gd.line(pts, fill=(80, 170, 255, 55), width=22, joint='curve')
    G = G.filter(ImageFilter.GaussianBlur(9)); img.alpha_composite(G)
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(Lr)
    for i in range(4):
        pts = [(x, y - cam) for x, y in PTS[i] if -60 < y - cam < H + 60]
        if len(pts) > 1:
            ld.line(pts, fill=(45, 90, 175, 170), width=8, joint='curve'); ld.line(pts, fill=(120, 175, 235, 170), width=3, joint='curve')
    sy = Y0 - cam; fy = L - cam
    if -40 < sy < H: ld.line([(110, sy), (870, sy)], fill=(255, 214, 60, 255), width=5)
    if -40 < fy < H:
        ld.line([(110, fy), (870, fy)], fill=(255, 255, 255, 255), width=5)
        for k, lx in enumerate(LANES):
            ld.ellipse([lx - 46, fy + 92, lx + 46, fy + 184], fill=(20, 16, 40, 255), outline=(255, 214, 60, 255), width=6)
            ctext(ld, lx, fy + 114, 'ABCD'[k], F(52), (255, 255, 255), 0)
    img.alpha_composite(Lr)
    # target glow (fades as the run starts)
    GL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gld = ImageDraw.Draw(GL)
    glow = 1.0 if t < T0 - 0.3 else max(0.0, 1 - (t - (T0 - 0.3)) / 0.6)
    for i in range(4):
        x = X(i, max(wy, Y0)); y = max(wy, Y0) - cam
        if i == TARGET and glow > 0:
            pul = 0.5 + 0.5 * math.sin(t * 8)
            for r, a in ((180, 70), (140, 120), (105, 170)):
                gld.ellipse([x - r, y - r, x + r, y + r], fill=(255, 225, 100, int(a * glow * (0.7 + 0.3 * pul))))
            for k in range(8):
                ang = k * math.pi / 4 + t * 1.5; r1, r2 = 108, 190 + 16 * pul
                gld.line([(x + r1 * math.cos(ang), y + r1 * math.sin(ang)), (x + r2 * math.cos(ang), y + r2 * math.sin(ang))], fill=(255, 245, 170, int(220 * glow)), width=8)
    img.alpha_composite(GL)
    for i in range(4):
        x = X(i, max(wy, Y0)); y = max(wy, Y0) - cam
        bob = int(5 * math.sin(t * 9 + i))
        img.alpha_composite(GUM, (int(x - GUM.width / 2), int(y - GUM.height / 2 + bob)))
    items = []
    # tier stamps: pop big above the gummies for 0.5s, then dock as one 44px line under the band
    cur = None
    for k, tr in enumerate(TIERS):
        if tr[0] <= t < T1 + 0.2: cur = (k, tr)
    if cur:
        k, (ts, big, small, col) = cur; u = t - ts
        if u < 0.55:
            sc = min(1.0, 0.6 + u / 0.12 * 0.4) if u < 0.12 else 1.0
            a = 255 if u < 0.45 else int(255 * (0.55 - u) / 0.1)
            cy = 690
            def plate(d):
                hw, hh = int(330 * sc), int(108 * sc)
                d.rounded_rectangle([W / 2 - 40 - hw, cy - hh, W / 2 - 40 + hw, cy + hh], 22, fill=(14, 10, 24, int(235 * a / 255)), outline=col + (a,), width=7)
            layer(img, plate)
            items += [(W / 2 - 40, cy - int(88 * sc), big, int(84 * sc), col, 10, a), (W / 2 - 40, cy + int(18 * sc), small, int(52 * sc), (255, 255, 255), 7, a)]
            if u < 1 / FPS and (round(ts, 3), 'swish') not in ev: ev.append((round(ts, 3), 'swish'))
        if u >= 0.45:
            a = int(255 * min(1, (u - 0.45) / 0.15)); line = f'{big} {small}'
            def dock(d):
                w = d.textlength(line, font=F(44))
                d.rounded_rectangle([W / 2 - w / 2 - 20, DOCK - 8, W / 2 + w / 2 + 20, DOCK + 60], 14, fill=(14, 10, 24, int(215 * a / 255)), outline=col + (a,), width=4)
            layer(img, dock)
            items.append((W / 2, DOCK + 4, line, 44, col, 7, a))
    if t < T0:
        items.append((490, 1250, "DON'T LOSE IT...", 48, (255, 255, 255), 8, 255))
    if T0 <= t < T0 + 0.6: items.append((490, 1230, 'GO!', 120, (120, 230, 110), 12, int(255 * (1 - (t - T0) / 0.6))))
    if t >= T1:
        u = t - T1; sc = 1.0 if u > 0.12 else 0.8 + u / 0.12 * 0.2
        def card(d):
            d.rounded_rectangle([110, HB + 20, 970, HB + 420], 24, fill=(12, 8, 24, 232), outline=(255, 214, 60, 255), width=6)
        layer(img, card)
        n = 3 - int(u / CD)
        items += [(W / 2, HB + 50, 'WHICH LETTER?', int(64 * sc), (255, 214, 60), 9, 255), (W / 2, HB + 140, 'COMMENT YOUR ANSWER', 44, (255, 255, 255), 7, 255)]
        uu = (u % CD) / CD; dsz = int(150 * (1.15 - 0.15 * min(1, uu * 5)))
        items.append((W / 2, HB + 230 + (150 - dsz) // 2, str(max(1, n)), dsz, (255, 255, 255), 12, 255))
    text_layer(img, items)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 25, 40, 110, 200, 320, NF - 1): img.convert('RGB').save(f'prev/p44_{f:04d}.png')
wr.close()
ev.append((round(T0, 3), 'go_8bit')); ev.append((round(T1, 3), 'ding_8bit'))
for n in range(3): ev.append((round(T1 + n * CD + 0.02, 3), 'tick_8bit'))
json.dump({'events': ev}, open('v44_ev.json', 'w')); print('done', TE, NF)
