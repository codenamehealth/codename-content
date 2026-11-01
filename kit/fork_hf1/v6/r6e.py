import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
from hook import _fit
from hook import hook_fade
# Oct 29: soft-fade hook, no box. Cut: the separate 'Comment 0, 1, 2 or 3' line (the end card asks), the boxed band.
HOOKB, HB = hook_fade(['Find 3 differences', "or you're an NPC"], accent=0, fade_to=440); print('hook bottom', HB)
import numpy as np, colorsys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SK = 1080 / 960.0; CROP = (0, 60)   # full scene width, units 60-540 (only sky/roof tips above unit 60 cropped)
PW, PH = 1080, round(480 * SK); PX = 0; PY1 = 400; PY2 = PY1 + PH; CX = 540; SEAM = PY2
FW, FH = round(960 * SK), round(540 * SK)
hub = Image.open(A + 'hub.gif'); NHF = hub.n_frames
k = SK / 2.0   # so x*2*k == x*SK (full-frame coords)
JOY = idle('joy', 2); CYR = idle('cyrus', 2); RAY = idle('ray', 2)
GM = gummy('mush', 3); GA = gummy('acv', 3)
POT = up(crop(Image.open(PL + 'steal/flowers/01.png').convert('RGBA')), 3)
CRATE = up(crop(Image.open(PL + 'steal/crate/01.png').convert('RGBA')), 3)
def recolor(img, box):
    # Oct 29 fix (Bennett: "should be the awning not a random blue box"): recolor only the awning's own yellow/cream
    # pixels (hue ~33-65 deg), so the orange roof tiles and fruit next to it keep their colour.
    a = np.array(img).astype(np.float32); x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1, :3] / 255.0
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = sub.max(-1); mn = sub.min(-1); d = np.maximum(mx - mn, 1e-6)
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    awn = (hue >= 33) & (hue <= 65) & (sat > 0.22) & (mx > 0.42)
    out = sub.copy()
    out[..., 0] = np.where(awn, b * 0.9 + 0.05, r)
    out[..., 1] = np.where(awn, g * 0.85 + 0.1, g)
    out[..., 2] = np.where(awn, r * 0.95, b)
    a[y0:y1, x0:x1, :3] = out * 255
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def blank_sign(img, box):
    # erase the cream lettering on the Tavern board: each cream pixel takes the last wood pixel to its left in the same row
    a = np.array(img); x0, y0, x1, y1 = box
    for y in range(y0, y1):
        last = None
        for x in range(x0 - 4, x1):
            r, g, b = int(a[y, x, 0]), int(a[y, x, 1]), int(a[y, x, 2])
            cream = r > 200 and g > 165 and b > 110
            if cream and x >= x0 and last is not None: a[y, x, :3] = last
            elif not cream: last = a[y, x, :3].copy()
    return Image.fromarray(a)
PANEL = {}
def panel(i, which):
    key = (i, which)
    if key in PANEL: return PANEL[key]
    hub.seek(i); f = hub.convert('RGBA').resize((FW, FH), Image.NEAREST)
    if which == 1: f = blank_sign(f, (586, 241, 665, 265))   # Oct 29 (Bennett): difference 3 is now the blank Tavern sign, no blue awning
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
SKYTOP, SKYBOT = (34, 78, 150), (92, 178, 238)
def backdrop(hi):
    # scene continues past the panels (no dimmed/blurred backdrop): sky above (under the hook fade), ground below
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(img)
    top0 = PY1 - round(60 * SK)
    for y in range(0, top0):
        u = y / max(1, top0); d.line([(0, y), (W, y)], fill=tuple(int(SKYTOP[c] + (SKYBOT[c] - SKYTOP[c]) * u) for c in range(3)) + (255,))
    raw = panel(hi, 0)
    img.alpha_composite(raw.crop((0, 0, W, round(60 * SK))), (0, top0))      # units 0-60 of the top panel's own sky/roofs
    # plaza continues below the lower panel: tile the plain cobble/dirt area (units x330-690, y478-540), mirrored so seams match
    tex = raw.crop((round(330 * SK), round(478 * SK), round(690 * SK), FH)); tw, th = tex.size
    tiles = [tex, tex.transpose(Image.FLIP_LEFT_RIGHT), tex.transpose(Image.FLIP_TOP_BOTTOM), tex.transpose(Image.ROTATE_180)]
    y = PY2 + PH; r = 0
    while y < H:
        x = -((r * 157) % tw); c = 0
        while x < W:
            img.alpha_composite(tiles[(r % 2) * 2 + (c % 2)], (x, y)) if x >= 0 else img.paste(tiles[(r % 2) * 2 + (c % 2)], (x, y))
            x += tw; c += 1
        y += th; r += 1
    g = Image.new('L', (1, H), 0)
    for yy in range(PY2 + PH, H): g.putpixel((0, yy), int(205 * min(1, (yy - PY2 - PH) / 380) ** 0.8))
    sh = Image.new('RGBA', (W, H), (8, 6, 16, 255)); sh.putalpha(g.resize((W, H))); img.alpha_composite(sh)
    return img
SPEC = {g: idle(g, 2) for g in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']}
T_GO = 0.5; T_END = T_GO + 10.0; DUR = T_END + 1.3   # recut: 3s countdown -> 0.5s GO! flash over bright panels; end hold 2.6s -> 1.3s, then loop
STILL = len(sys.argv) > 1
out = Writer('d6hf3_noaudio.mp4') if not STILL else None; ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    hi = int(t * 10) % NHF
    img = backdrop(hi)
    for which, py in ((0, PY1), (1, PY2)):
        p = decorate(panel(hi, which), which, t)
        img.alpha_composite(p, (PX, py))
    # timer: vertical bar right of the panels (the 20px digit was unreadable: cut)
    rem = max(0.0, T_END - max(t, T_GO)); frac = rem / 10.0
    col = (90, 200, 80) if rem > 5 else ((255, 190, 50) if rem > 2 else (230, 60, 60))
    by0, by1 = PY1 - 10, PY2 + PH + 10
    pul = (0.5 + 0.5 * math.sin(t * 4 * math.pi)) if 0 < rem <= 3 else 0
    def tb(d):
        d.rectangle([0, SEAM - 17, W, SEAM + 17], fill=(14, 10, 24, 255))
        gy0 = SEAM - 11; gy1 = SEAM + 11; bx0, bx1 = 80, 1015
        if pul: d.rounded_rectangle([bx0 - 6, gy0 - 5, bx1 + 6, gy1 + 5], 12, fill=(255, 40, 40, int(140 * pul)))
        d.rounded_rectangle([bx0, gy0, bx1, gy1], 9, fill=(20, 14, 30, 235), outline=(255, 255, 255, 255), width=3)
        if frac > 0.01: d.rounded_rectangle([bx0 + 4, gy0 + 4, bx0 + 4 + (bx1 - bx0 - 8) * frac, gy1 - 4], 5, fill=col + (255,))
    layer(img, tb)
    # GO! flash (0.5s) over the live, full-brightness panels
    if t < T_GO + 0.25:
        u = t; a = int(255 * min(1, max(0, (T_GO + 0.25 - u) / 0.25))); sc = 1 + 0.2 * max(0, 1 - u / 0.15)
        text_layer(img, [(CX, SEAM - 60 * sc, 'GO!', int(120 * sc), (120, 240, 90), 10, a)])
        if f == 0: ev.append((0.0, 'go_8bit'))
    if T_END - 3 <= t < T_END and (f - round((T_END - 3) * FPS)) % FPS == 0: ev.append((round(t, 3), 'tick_8bit'))
    if t >= T_END:
        u = t - T_END
        if f == round(T_END * FPS): ev.append((round(t, 3), 'buzz_8bit'))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, 120)))
        sc = 1 + 0.15 * max(0, 1 - u / 0.12)    # hard pop
        cy = SEAM
        layer(img, lambda d: d.rounded_rectangle([130, cy - 150, 950, cy + 150], 24, fill=(20, 14, 30, 240), outline=(255, 214, 60, 255), width=8))
        text_layer(img, [(CX, cy - 112, "TIME'S UP!", int(68 * sc), (255, 214, 60), 9, 255), (CX, cy + 4, 'How many did', 48, (255, 255, 255), 7, 255),
                         (CX, cy + 68, 'you find?', 48, (255, 255, 255), 7, 255)])
    img.alpha_composite(HOOKB)
    if STILL:
        if f in (0, 150, 340): img.convert('RGB').save(f'hf_still_{f}.png')
        if f > 340: break
        continue
    out.write(img)
if STILL: sys.exit()
out.close()
json.dump({'events': ev}, open('ev.json', 'w')); print('done', DUR, len(ev))
