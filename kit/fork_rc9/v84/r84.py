import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #84 safe-zone + hook pass (source: fork_b8/r86.py): same motion/rng (answer unchanged); cauldron 8x -> 6x and the whole
# gummy motion mapped 0.8x about the liquid centre at render time (gummies unchanged 3x); Joy moved into the zone.
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CAUL = up(crop(Image.open(B8 + 'cauldron/03.png').convert('RGBA')), 7)   # rc9: 6x -> 7x
import hook as HK
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 255, 255)):
    f, s = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
HOOK, HB = band(['LOCK YOUR EYES ON', 'THE GOLDEN GUMMY'], 1, 'COMMENT ITS NUMBER')
HOOK2, _ = band(['LOCK YOUR EYES ON', 'THE GOLDEN GUMMY'], 1, 'COMMENT THE NUMBER', subcol=(255, 214, 60))   # end: the band line becomes the comment ask
LX_ = 560
print('hook bottom', HB)
CT = HB + 98; CL = 110                          # rc9: cauldron 7x at x110-964, y592-1376 (lower rows stay inside x<=887)
NX, NY = CL + CAUL.width // 2, CT + CAUL.height // 2
KS = 0.8 * 7 / 6
def M(x, y): return NX + KS * (x - 540), NY - 22 * 7 / 6 + KS * (y - 1060)
print('cauldron', CL, CT, CL + CAUL.width, CT + CAUL.height)
CX, CY = 540, 1090
N = 12; RIN = 270
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
ACV = up(acv_gummy_strong(), 4); GOLD0 = Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'); GOLD = up(GOLD0, 4)   # rc9: gummies 3x -> 4x, ACV with gummy shine
GOLDK = {k: up(GOLD0, k) for k in range(4, 9)}
T_SHOW, T_FADE, T_MOVE, T_END = 0.0, 1.35, 1.5, 10.5   # rc9: drop-in from frame 0, shuffle 13s -> 9s (faster ramp)
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
G = [dict(t0=rng.uniform(0, 6.28), a=rng.uniform(0.6, 1.4), p=rng.uniform(0, 6.28), b=rng.uniform(0.8, 1.9), q=rng.uniform(0, 6.28), rb=rng.uniform(100, 250), ra=rng.uniform(40, 70)) for _ in range(N)]
TARGET = 0
def omega(t):
    if t < T_MOVE: return 0.0
    u = t - T_MOVE; return min(3.4, 0.9 + 0.35 * u)
OM = [0.0]
for f in range(1, int(T_END * FPS) + 1): OM.append(OM[-1] + omega(f / FPS) / FPS)
def pos(i, f):
    t = f / FPS; g = G[i]; th = g['t0'] + OM[min(f, len(OM) - 1)]; r = g['rb']
    if t > T_MOVE:
        u = t - T_MOVE; amp = min(1, u / 1.0)
        th += amp * 0.7 * math.sin(g['b'] * u * (1 + u / 7) + g['q']); r += amp * g['ra'] * math.sin(g['a'] * u * (1 + u / 8.4) + g['p'])
    r = max(40, min(275, r))
    return CX + r * math.cos(th), CY - 30 + r * math.sin(th) * 0.86
def raw(i, f):
    return pos(i, f)
TS = T_END - 1.3
def settle_targets():
    f0 = int(TS * FPS); P = [raw(i, f0) for i in range(N)]
    pol = [(math.hypot(x - CX, (y - CY + 30) / 0.86), math.atan2((y - CY + 30) / 0.86, x - CX), i) for i, (x, y) in enumerate(P)]
    pol.sort(); inner = sorted(pol[:4], key=lambda p: p[1]); outer = sorted(pol[4:], key=lambda p: p[1])
    T = {}
    for ring, rr in ((inner, 115), (outer, 255)):
        n = len(ring); a0 = ring[0][1]
        for k, (_, a, i) in enumerate(ring):
            ang = a0 + 2 * math.pi * k / n; T[i] = (CX + rr * math.cos(ang), CY - 30 + rr * math.sin(ang) * 0.86)
    return T
def final_pos(i, f):
    t = f / FPS; x, y = raw(i, f)
    if t <= TS: return x, y
    k = min(1, (t - TS) / 1.3); k = k * k * (3 - 2 * k); tx, ty = TGT[i]
    x0, y0 = raw(i, min(f, int(T_END * FPS)))
    return x0 * (1 - k) + tx * k, y0 * (1 - k) + ty * k
# ensure gummies start well separated
def sep_ok():
    pts = [pos(i, 0) for i in range(N)]
    return min(math.hypot(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(pts) for b in pts[i + 1:]) > 105
tries = 0
while not sep_ok() and tries < 500:
    for g in G: g['t0'] = rng.uniform(0, 6.28); g['rb'] = rng.uniform(90, 255)
    tries += 1
print('sep tries', tries)
TGT = settle_targets()
NUM = list(range(1, N + 1)); rng.shuffle(NUM)
print('target number', NUM[TARGET])
BGF = bg_frames('found_hd.gif', (int(1920 * 1.8), int(1080 * 1.8)), step=2, bright=0.45)
JOY = idle('joy', 4)   # rc9: Joy 3x -> 4x (~256px)
TIERS = [(T_MOVE, '100% STILL HERE', (130, 240, 130)), (T_MOVE + 2.3, 'TOP 30% LEFT', (255, 214, 60)), (T_MOVE + 4.6, 'TOP 5% REMAINING', (255, 160, 70)), (T_MOVE + 6.9, 'TOP 1% ELITE', (255, 110, 110))]
END = T_END + 1.5; NF = int(END * FPS)
DROP = {i: -0.25 + 0.05 * k for k, i in enumerate([j for j in range(N) if j != TARGET])}; DROP[TARGET] = 0.2   # staggered drop-in, a few already mid-fall on frame 0; golden one lands last
wr = Writer('v84_noaudio.mp4'); events = []
BUB = [(rng.uniform(-200, 200), rng.uniform(-110, 110), rng.uniform(0, 3), rng.uniform(8, 22)) for _ in range(26)]
for f in range(NF):
    t = f / FPS; ff = min(f, int(T_END * FPS))
    bg = BGF[int(t * 6) % len(BGF)]; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    img.alpha_composite(bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)), (0, 0))
    layer(img, lambda d: d.ellipse([NX - 440, NY - 330, NX + 440, NY + 400], fill=(120, 255, 120, 20)))
    img.alpha_composite(CAUL, (NX - CAUL.width // 2, NY - CAUL.height // 2))
    # bubbles
    layer(img, lambda d: [d.ellipse([NX + KS * bx * 1.2 - s * ((t * 0.7 + ph) % 1), NY - 22 + KS * by * 1.6 - s * ((t * 0.7 + ph) % 1), NX + KS * bx * 1.2 + s * ((t * 0.7 + ph) % 1), NY - 22 + KS * by * 1.6 + s * ((t * 0.7 + ph) % 1)], outline=(200, 255, 170, int(220 * (1 - (t * 0.7 + ph) % 1))), width=3) for bx, by, ph, s in BUB])
    # swirl lines when stirring
    if t > T_MOVE and t < T_END:
        th0 = OM[ff]
        layer(img, lambda d: [d.arc([NX - r_, NY - 22 - r_ * 0.86, NX + r_, NY - 22 + r_ * 0.86], math.degrees(th0 + k * 2.1) % 360, (math.degrees(th0 + k * 2.1) + 50) % 360, fill=(220, 255, 200, 90), width=4) for k, r_ in enumerate((88, 160, 224))])
    # gummies (y-sorted)
    pts = sorted([(M(*final_pos(i, ff)), i) for i in range(N)], key=lambda p: (p[1] == TARGET and t < T_FADE + 0.4, p[0][1]))   # golden one drawn in front until it turns
    for (x, y), i in pts:
        dl = DROP[i]; u_ = (t - dl) / 0.42
        if u_ < 0: continue
        if u_ < 1: y = y - 520 * (1 - u_ * u_)          # falling in (ease-in)
        elif u_ < 1.9: layer(img, lambda d: d.ellipse([x - 30 - 50 * (u_ - 1), y + 20 - 14 * (u_ - 1), x + 30 + 50 * (u_ - 1), y + 44 + 14 * (u_ - 1)], outline=(210, 255, 180, int(230 * (1.9 - u_) / 0.9)), width=4))   # splash ring
        g = ACV
        if i == TARGET and t < T_FADE + 0.4:
            k = 0 if t < T_FADE else (t - T_FADE) / 0.4
            if k > 0: g = Image.blend(GOLD.resize(ACV.size, Image.NEAREST), ACV, k)
            else:
                v = t - (dl + 0.42); g = GOLDK[max(4, min(8, 8 - int(max(0, v - 0.35) / 0.1)))] if v >= 0 else GOLDK[8]   # 2x big while it falls and for 0.35s after landing, then shrinks back to 4x   # lands 2x big, shrinks back in integer steps
            if t < T_FADE + 0.2 and u_ >= 1:
                pulse = 0.5 + 0.5 * math.sin(t * 10); rr_ = max(96, g.width * 0.75)
                layer(img, lambda d: d.ellipse([x - rr_ - 20, y - rr_ - 20, x + rr_ + 20, y + rr_ + 20], fill=(255, 220, 80, int(80 + 80 * pulse))))
                layer(img, lambda d: d.ellipse([x - rr_, y - rr_, x + rr_, y + rr_], outline=(255, 214, 60, 255), width=10))
        img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    # numbers at the end
    if t >= T_END:
        u = t - T_END
        for (x, y), i in pts:
            bw_ = 18 + 22 * len(str(NUM[i]))   # number badge centred on its gummy (neighbours are >=150px apart, so badges never overlap)
            layer(img, lambda d: d.rounded_rectangle([x - bw_, y - 40, x + bw_, y + 30], 16, fill=(20, 14, 30, 240), outline=(255, 255, 255, 255), width=4))
            text_layer(img, [(x + 2, y - 27, str(NUM[i]), 44, (255, 255, 255), 0, 255)])
    # Joy stirring beside
    jf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(jf, (70 - 26 * 4, 1495 - 78 * 4))
    # header
    cur = None
    for tt, txt, col in TIERS:
        if t >= tt: cur = (tt, txt, col)
    def pill(txt, col, fs=52):   # tier / question line: one bold line on a dark pill under the band
        tw_ = ImageDraw.Draw(img).textlength(txt, font=F(fs))
        layer(img, lambda d: d.rounded_rectangle([547 - tw_ / 2 - 28, HB + 8, 547 + tw_ / 2 + 28, HB + 88], 20, fill=(14, 10, 24, 235), outline=col + (255,), width=5))
        text_layer(img, [(547, HB + 22, txt, fs, col, 8, 255)])
    def low(txt, col=(255, 255, 255)):   # box under the cauldron (gummy name, then timer, then the comment ask)
        tw_ = ImageDraw.Draw(img).textlength(txt, font=F(44))
        layer(img, lambda d: d.rounded_rectangle([LX_ - tw_ / 2 - 24, 1388, LX_ + tw_ / 2 + 24, 1468], 16, fill=(10, 18, 12, 225)))
        text_layer(img, [(LX_, 1406, txt, 44, col, 6, 255)])
    if t < T_END:
        if cur and t >= T_MOVE:
            pill(cur[1], cur[2])
            if abs(t - cur[0]) < 0.5 / FPS: events.append((round(t, 3), 'swish'))
        else: pill("DON'T LOSE IT", (255, 255, 255))
        if t < T_MOVE: low('ACV GUMMIES', (170, 255, 150))
        else: low(f'{max(0, t - T_MOVE):04.1f}s')
        if t > T_END - 3.2 and abs((t - T_MOVE) - round(t - T_MOVE)) < 0.5 / FPS: events.append((round(t, 3), 'reeltick_8bit'))
    else:
        u = t - T_END
        pill('WHICH ONE WAS IT?', (255, 214, 60))
        if abs(u) < 0.5 / FPS: events.append((round(t, 3), 'ding_8bit'))
    if f == 0: events.append((0.0, 'chime'))
    if abs(t - (DROP[TARGET] + 0.42)) < 0.5 / FPS: events.append((round(t, 3), 'twinkle'))
    img.alpha_composite(HOOK2 if t >= T_END else HOOK)
    wr.write(img)
    if f in (0, 8, 22, 40, 200, 300, NF - 1): img.convert('RGB').save(f'f84_{f}.png')
wr.close(); json.dump({'events': sorted(events)}, open('v84_ev.json', 'w')); print('done', END)
