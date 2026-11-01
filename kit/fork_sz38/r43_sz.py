import sys; sys.path.insert(0, '../fork1')
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['FINALLY MADE IT', 'TO A SAVE POINT'], accent=1)
SHIFT = 340
K = 4; FOOTY = 78 * K
BG = bg_frames('recov_hd.gif', (W, H), box=(677, 0, 1284, 1080), step=1)
WALK = [up(f.resize((92, 92), Image.NEAREST), K) for f in gif_frames(A + 'hollow-walk-side.gif')]
SIT = seq('../fork_a4/hollow_sit', K)
RIDLE = idle('ray', K); RCAST = seq('../fork3/ray_cast', K, 1)
CRY = up(crop(Image.open('../fork_a3/crystal/05.png').convert('RGBA')), 3)
MEL = gummy('mel', 3)
GROUND = 1180; XH = 300; XR = 790; XC = 545
def shifted(fr):
    o = Image.new('RGBA', (W, H)); o.alpha_composite(fr, (0, -SHIFT)); o.alpha_composite(fr.crop((0, H - SHIFT, W, H)), (0, H - SHIFT)); return o
BG = [shifted(b) for b in BG]
def put(img, spr, cx, foot=GROUND): img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOTY)))
def box(img, name, text, n, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = 76, 1258, 880, 1488
    d.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x1, y1], fill=(16, 18, 44, 245), outline=(235, 235, 255, 255), width=6)
    d.rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10], outline=(90, 100, 160, 255), width=3)
    tw = d.textlength(name, font=F(30)); d.rectangle([x1 - tw - 70, y0 - 40, x1 - 20, y0 + 6], fill=col + (255,), outline=(235, 235, 255, 255), width=4)
    d.text((x1 - tw - 45, y0 - 30), name, font=F(30), fill=(255, 255, 255))
    y = y0 + 50
    for ln in text[:n].split('\n'): d.text((x0 + 36, y), ln, font=F(38), fill=(255, 255, 255)); y += 64
    img.alpha_composite(L)
T_ARR, T_SAVE = 1.45, 1.55
LINES = [(2.15, 'I saved your game\nfor you.'), (4.15, "You're doing better\nthan you think.")]
T_GUM = 4.6
TE = 7.4; NF = int(TE * FPS); wr = Writer('v43_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    # crystal glow + bob
    bob = 10 * math.sin(t * 2.6); cy = GROUND - 190 + bob
    flash = max(0.0, 1 - abs(t - T_SAVE - 0.15) / 0.45) if t > T_SAVE - 0.3 else 0.0
    def glow(d):
        for r, a in ((150, 35), (110, 60), (78, 90)):
            aa = int(min(255, a * (1 + 2.2 * flash)))
            d.ellipse([XC - r, cy - r, XC + r, cy + r], fill=(150, 210, 255, aa))
        d.ellipse([XC - 90, GROUND - 22, XC + 90, GROUND + 10], fill=(120, 190, 255, int(70 + 120 * flash)))
    layer(img, glow)
    img.alpha_composite(CRY, (int(XC - CRY.width / 2), int(cy - CRY.height / 2)))
    # sparkles rising from the crystal
    def spark(d):
        for k in range(10):
            ph = (t * 0.6 + k * 0.1) % 1.0; sx = XC + 70 * math.sin(k * 2.4 + t); sy = cy + 80 - ph * 260
            a = int(220 * (1 - ph)); d.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(220, 240, 255, a))
    layer(img, spark)
    # Rayleigh
    if T_SAVE <= t < T_SAVE + 0.9: put(img, RCAST[min(len(RCAST) - 1, int((t - T_SAVE) / 0.9 * len(RCAST)))], XR)
    else: put(img, RIDLE[int(t * 8) % len(RIDLE)], XR)
    # Hollow
    if t < T_ARR:
        x = -140 + (XH + 140) * (t / T_ARR); put(img, WALK[int(t * 9) % len(WALK)], x)
    else:
        k = min(len(SIT) - 1, int((t - T_ARR) / 0.6 * len(SIT))); put(img, SIT[k], XH)
    # melatonin gummy floats from Rayleigh to the Hollow
    if t >= T_GUM:
        u = min(1.0, (t - T_GUM) / 1.0); gx = XR - 60 + (XH + 40 - (XR - 60)) * u; gy = GROUND - 220 - 140 * math.sin(math.pi * u)
        if u < 1.0: img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
        else:
            v = t - T_GUM - 1.0
            if v < 1.2:
                text_layer(img, [(XH, GROUND - 330 - v * 60, '+ HP', 40, (255, 120, 170), 6, int(255 * max(0, 1 - v / 1.2)))])
    items = []
    if T_SAVE <= t < T_SAVE + 1.3:
        a = int(255 * min(1, (T_SAVE + 1.3 - t) / 0.3)); items.append((W / 2, HB + 40, 'GAME SAVED', 56, (170, 225, 255), 8, a))
    text_layer(img, items)
    for i, (ts, txt) in enumerate(LINES):
        tend = LINES[i + 1][0] if i + 1 < len(LINES) else 99
        if ts <= t < tend:
            n = int((t - ts) * 30) + 1
            box(img, 'RAYLEIGH', txt, n, (107, 45, 107))
            if n <= len(txt) and int((t - ts) * 30) % 2 == 0 and int((t - ts) * 30) != int((t - ts - 1 / FPS) * 30): ev.append((round(t, 3), 'tick_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (30, 55, 100, 150, 175, 215): img.convert('RGB').save(f'prev/d43_{f:04d}.png')
wr.close()
ev += [(T_SAVE, 'chime'), (T_SAVE + 0.05, 'twinkle'), (T_GUM, 'whoosh_8bit'), (T_GUM + 1.0, 'coin_8bit')]
json.dump(ev, open('v43_ev.json', 'w')); print('done')
