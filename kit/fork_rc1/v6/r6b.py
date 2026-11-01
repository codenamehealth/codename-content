import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
from hook import _fit
def band():
    # recut: hook 72px + NPC line (40px, the longest that fits one line) + comment prompt as a real 44px line
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    f, s = _fit(['FIND 3', 'DIFFERENCES'], 915, 72, 64); fn = F(40); fp = F(44)
    y = 262; h = 22 + s + 26 + s + 16 + 40 + 14 + 3 + 16 + 44 + 24
    d.rounded_rectangle([70, y, 1025, y + h], 22, fill=(14, 10, 24, 232), outline=(255, 214, 60, 255), width=6)
    yy = y + 22
    for i, l in enumerate(['FIND 3', 'DIFFERENCES']):
        w = d.textlength(l, font=f); d.text((547 - w / 2, yy), l, font=f, fill=(255, 214, 60) if i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); yy += s + 26
    yy += 16 - 26
    t = "10 SEC OR YOU'RE AN NPC"; w = d.textlength(t, font=fn); d.text((547 - w / 2, yy), t, font=fn, fill=(200, 230, 255), stroke_width=6, stroke_fill=(10, 6, 18)); yy += 40 + 14
    d.line([(130, yy), (965, yy)], fill=(255, 214, 60, 120), width=3); yy += 3 + 16
    t = 'Comment 0, 1, 2 or 3'; w = d.textlength(t, font=fp); d.text((547 - w / 2, yy), t, font=fp, fill=(255, 255, 255), stroke_width=6, stroke_fill=(10, 6, 18))
    return L, y + h
HOOKB, HB = band(); print('hook bottom', HB)
import numpy as np, colorsys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PW, PH = 796, 405; PX = 80; GAP = 44; PY1, PY2 = HB + 18, HB + 18 + 405 + GAP; CX = 478
SK = PW / 820.0; CROP = (80, 110)   # zoom: show 960-unit region x80-900, y110-525 (was full 960x540)
FW, FH = round(960 * SK), round(540 * SK)
hub = Image.open(A + 'hub.gif'); NHF = hub.n_frames
k = SK / 2.0   # so x*2*k == x*SK (full-frame coords)
JOY = idle('joy', 2); CYR = idle('cyrus', 2); RAY = idle('ray', 2)
GM = gummy('mush', 3); GA = gummy('acv', 3)
POT = up(crop(Image.open(PL + 'steal/flowers/01.png').convert('RGBA')), 3)
CRATE = up(crop(Image.open(PL + 'steal/crate/01.png').convert('RGBA')), 3)
def recolor(img, box):
    a = np.array(img).astype(np.float32); x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1, :3] / 255.0
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = sub.max(-1); mn = sub.min(-1)
    yellowish = (r > 0.45) & (g > 0.35) & (b < 0.55) & (mx - mn > 0.18) & (r >= g * 0.9)
    out = sub.copy()
    # rotate yellow -> sky blue: swap channels roughly
    out[..., 0] = np.where(yellowish, b * 0.9 + 0.05, r)
    out[..., 1] = np.where(yellowish, g * 0.85 + 0.1, g)
    out[..., 2] = np.where(yellowish, r * 0.95, b)
    a[y0:y1, x0:x1, :3] = out * 255
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
PANEL = {}
def panel(i, which):
    key = (i, which)
    if key in PANEL: return PANEL[key]
    hub.seek(i); f = hub.convert('RGBA').resize((FW, FH), Image.NEAREST)
    if which == 1: f = recolor(f, (int(770 * 2 * k), int(150 * 2 * k), FW, int(250 * 2 * k)))
    PANEL[key] = f; return f
def decorate(p, which, t):
    p = p.copy()
    # props shared
    p.alpha_composite(CRATE, (int(880 * 2 * k) - CRATE.width // 2, int(470 * 2 * k) - CRATE.height))
    if which == 0: p.alpha_composite(POT, (int(118 * 2 * k) - POT.width // 2, int(468 * 2 * k) - POT.height))   # difference 3
    g = GM if which == 0 else GA                                                                             # difference 1
    p.alpha_composite(g, (int(395 * 2 * k) - g.width // 2, int(372 * 2 * k) - g.height))
    fi = int(t * 10) % 6
    for spr, x, y in ((JOY[fi], 300, 500), (CYR[fi], 640, 498), (RAY[(fi + 2) % 6], 735, 330)):
        p.alpha_composite(spr, (int(x * 2 * k) - spr.width // 2, int(y * 2 * k) - spr.height * 78 // 92))
    ox, oy = round(CROP[0] * SK), round(CROP[1] * SK)
    return p.crop((ox, oy, ox + PW, oy + PH))
BG = [f for f in bg_frames('hub.gif', (3413, 1920), step=4, bright=0.45, blur=14)]
BGC = [b.crop(((3413 - W) // 2, 0, (3413 - W) // 2 + W, H)) for b in BG]
SPEC = {g: idle(g, 2) for g in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']}
T_GO = 0.5; T_END = T_GO + 10.0; DUR = T_END + 1.3   # recut: 3s countdown -> 0.5s GO! flash over bright panels; end hold 2.6s -> 1.3s, then loop
STILL = len(sys.argv) > 1
out = Writer('d6big_noaudio.mp4') if not STILL else None; ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGC[int(t * 2.5) % len(BGC)].copy()
    hi = int(t * 10) % NHF
    for which, py in ((0, PY1), (1, PY2)):
        p = decorate(panel(hi, which), which, t)
        layer(img, lambda d, py=py: d.rounded_rectangle([PX - 10, py - 10, PX + PW + 10, py + PH + 10], 14, fill=(20, 14, 30, 255), outline=(255, 214, 60, 255), width=5))
        img.alpha_composite(p, (PX, py))
    # timer: vertical bar right of the panels (the 20px digit was unreadable: cut)
    rem = max(0.0, T_END - max(t, T_GO)); frac = rem / 10.0
    col = (90, 200, 80) if rem > 5 else ((255, 190, 50) if rem > 2 else (230, 60, 60))
    by0, by1 = PY1 - 10, PY2 + PH + 10
    pul = (0.5 + 0.5 * math.sin(t * 4 * math.pi)) if 0 < rem <= 3 else 0
    def tb(d):
        gy0 = PY1 + PH + 12; gy1 = PY2 - 12; bx0, bx1 = PX, PX + PW
        if pul: d.rounded_rectangle([bx0 - 6, gy0 - 5, bx1 + 6, gy1 + 5], 12, fill=(255, 40, 40, int(140 * pul)))
        d.rounded_rectangle([bx0, gy0, bx1, gy1], 9, fill=(20, 14, 30, 235), outline=(255, 255, 255, 255), width=3)
        if frac > 0.01: d.rounded_rectangle([bx0 + 4, gy0 + 4, bx0 + 4 + (bx1 - bx0 - 8) * frac, gy1 - 4], 5, fill=col + (255,))
    layer(img, tb)
    # GO! flash (0.5s) over the live, full-brightness panels
    if t < T_GO + 0.25:
        u = t; a = int(255 * min(1, max(0, (T_GO + 0.25 - u) / 0.25))); sc = 1 + 0.2 * max(0, 1 - u / 0.15)
        text_layer(img, [(CX, (PY1 + PY2 + PH) / 2 - 60 * sc, 'GO!', int(120 * sc), (120, 240, 90), 10, a)])
        if f == 0: ev.append((0.0, 'go_8bit'))
    if T_END - 3 <= t < T_END and (f - round((T_END - 3) * FPS)) % FPS == 0: ev.append((round(t, 3), 'tick_8bit'))
    if t >= T_END:
        u = t - T_END
        if f == round(T_END * FPS): ev.append((round(t, 3), 'buzz_8bit'))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, 120)))
        sc = 1 + 0.15 * max(0, 1 - u / 0.12)    # hard pop
        cy = (PY1 + PY2 + PH) // 2
        layer(img, lambda d: d.rounded_rectangle([100, cy - 190, 860, cy + 190], 24, fill=(20, 14, 30, 240), outline=(255, 214, 60, 255), width=8))
        text_layer(img, [(CX, cy - 150, "TIME'S UP!", int(68 * sc), (255, 214, 60), 9, 255), (CX, cy - 40, 'How many did', 48, (255, 255, 255), 7, 255),
                         (CX, cy + 24, 'you find?', 48, (255, 255, 255), 7, 255), (CX, cy + 100, '0, 1, 2 or 3?', 48, (120, 240, 90), 7, 255)])
    img.alpha_composite(HOOKB)
    if STILL:
        if f in (0, 150, 340): img.convert('RGB').save(f'big_still_{f}.png')
        if f > 340: break
        continue
    out.write(img)
if STILL: sys.exit()
out.close()
json.dump({'events': ev}, open('ev.json', 'w')); print('done', DUR, len(ev))
