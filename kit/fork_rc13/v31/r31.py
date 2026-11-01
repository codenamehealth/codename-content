"""#31 Hold your thumb on the crystal: review recut (Bennett: Joy's smile fixed, rest is good).
joke lines 18px -> 44px (one column), clear stamps name the joke on a dark plate, WHAT'S YOUR DEBUFF? band line from frame 0,
first clear at 1.2s (hold ring 1.8s -> 0.8s), Joy 4x -> 5x, ACV gummy reward with gloss + tag, hold 1.4s then cut back to the start."""
import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, R + 'fork_rc2'); from rc2 import hook_layer2, acv_gloss, acv_tag
HOOK, HB = hook_layer2(['HOLD YOUR THUMB', 'ON THE CRYSTAL'], accent=1, sub="WHAT'S YOUR DEBUFF?")
print('hook bottom', HB)
FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
TEST = len(sys.argv) > 1
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
BG = up(Image.open(R + 'fork_a3/shrine1/00.png').convert('RGBA'), 3).crop((36, 60, 36 + W, 60 + H))
CRY = up(Image.open(R + 'fork_a3/crystal/03.png').convert('RGBA').crop(Image.open(R + 'fork_a3/crystal/03.png').getbbox()), 5)
CX, CY = 470, 790
CAST = [up(Image.open(p).convert('RGBA'), 5) for p in sorted(glob.glob(R + 'fork_a3/joy_cast/*.png'))]
JX, JY = 838, 1000           # Joy's feet (5x, was 4x)
WX0, WX1, WY0, WY1 = 72, 884, 1006, 1496   # status window
GUM = up(acv_gloss(Image.open(R + 'pixellab/gummies/pick_acv.png').convert('RGBA')), 3)
DEBUFF = [('Doomscrolling', 'DOOMSCROLLING', (150, 90, 200)), ('Monday', 'MONDAY', (220, 70, 70)), ('1% battery', '1% BATTERY', (90, 150, 255)),
          ('37 tabs open', '37 TABS OPEN', (170, 60, 170)), ('The group chat', 'THE GROUP CHAT', (240, 200, 60)), ('One more episode', 'ONE MORE EPISODE', (140, 140, 160))]
T_HOLD = 0.8; STEP = 1.2; TCL = [1.2 + i * STEP for i in range(6)]; T_END = TCL[-1] + 1.0
HOLDEND = 1.4; DUR = T_END + HOLDEND; N = int(round(DUR * FPS))
rng = random.Random(3); FLIES = [(rng.uniform(0, W), rng.uniform(450, 1450), rng.uniform(0, 6.3)) for _ in range(30)]
events = [(round(T_HOLD, 3), 'twinkle')] + [(round(tc, 3), 'chime') for tc in TCL] + [(round(T_END, 3), 'powerup_8bit')]
def bez(p0, p1, p2, u): return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])
def stamp(img, l1, l2, u, c2=(140, 240, 110)):
    """two-line stamp on a dark plate between the hook band and the scene; u = seconds since it fired"""
    if u < 0 or u > 1.0: return
    a = int(255 * min(1, (1.0 - u) / 0.2)); sc = 1 + 0.2 * max(0, 1 - u / 0.12)
    f1 = F(int(52 * sc)); f2 = F(int(48 * sc))
    def pl(d):
        w = max(d.textlength(l1, font=f1), d.textlength(l2, font=f2)) + 56
        d.rounded_rectangle([540 - w / 2, HB + 14, 540 + w / 2, HB + 152], 18, fill=(14, 10, 24, int(230 * a / 255)), outline=c2 + (a,), width=5)
        ctext(d, 540, HB + 32, l1, f1, (255, 255, 255), 8, a); ctext(d, 540, HB + 94, l2, f2, c2, 8, a)
    layer(img, pl)
def frame(f):
    t = f / FPS; img = BG.copy()
    layer(img, lambda d: [d.rectangle([x, y + 20 * math.sin(t + p), x + 5, y + 5 + 20 * math.sin(t + p)], fill=(230, 255, 140, int(120 + 110 * math.sin(t * 2.5 + p)))) for x, y, p in FLIES])
    held = t >= T_HOLD
    bob = 10 * math.sin(t * 2.2); glow = 0.6 + 0.4 * math.sin(t * 4) + (0.5 if held else 0)
    def aura(d):
        for k in range(6, 0, -1):
            r = 70 + k * 22 * (1.15 if held else 1)
            d.ellipse([CX - r, CY + bob - r, CX + r, CY + bob + r], fill=(140, 220, 255, int(min(255, 16 * glow * (7 - k)))))
        if held:
            for k in range(10):
                a = t * 0.8 + k * math.pi / 5; L = 260 + 30 * math.sin(t * 3 + k)
                d.line([CX + 90 * math.cos(a), CY + bob + 90 * math.sin(a), CX + L * math.cos(a), CY + bob + L * math.sin(a)], fill=(200, 240, 255, 60), width=10)
    layer(img, aura)
    img.alpha_composite(CRY, (int(CX - CRY.width / 2), int(CY + bob - CRY.height / 2)))
    # hold ring + arrow (ring already part-filled on frame 0)
    if not held or t < T_HOLD + 0.4:
        prog = min(1, 0.15 + 0.85 * t / T_HOLD)
        def ring(d):
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], 0, 360, fill=(255, 255, 255, 110), width=12)
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], -90, -90 + 360 * prog, fill=(150, 240, 120, 255), width=14)
        layer(img, ring)
        if not held:
            ay = CY - 190 + 10 * math.sin(t * 6 + 1.2); d = ImageDraw.Draw(img)
            d.polygon([(CX - 32, ay), (CX + 32, ay), (CX, ay + 40)], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
            d.rectangle([CX - 12, ay - 40, CX + 12, ay], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
    if held and t < T_END:
        def stream(d):
            for k in range(26):
                u = ((t * 0.9 + k / 26) % 1.0)
                x, y = bez((CX, CY + bob), (CX + 210, CY - 120 + 60 * math.sin(k)), (JX - 30, JY - 220), u)
                s = 4 + 4 * math.sin(u * math.pi)
                d.rectangle([x - s, y - s, x + s, y + s], fill=(170, 255, 140, int(220 * math.sin(u * math.pi))))
        layer(img, stream)
    # Joy (cast loop uses frames 1-9 only: frames 10-12 are the teeth grin Bennett flagged)
    if not held: fr = CAST[0]
    else:
        k = int((t - T_HOLD) * 10)
        fr = CAST[1 + (k % 9)] if t < T_END else CAST[0]
    layer(img, lambda d: d.ellipse([JX - 75, JY - 16, JX + 75, JY + 14], fill=(0, 0, 0, 80)))
    img.alpha_composite(fr, (JX - fr.width // 2, JY - 78 * 5))
    # status window
    def win(d):
        d.rounded_rectangle([WX0, WY0, WX1, WY1], 22, fill=(16, 22, 40, 232), outline=(240, 230, 200, 255), width=6)
        d.rounded_rectangle([WX0 + 12, WY0 + 12, WX1 - 12, WY1 - 12], 16, outline=(110, 120, 160, 255), width=3)
    layer(img, win)
    cleared = sum(1 for tc in TCL if t >= tc)
    hp = 12 + (88 * cleared / 6 if cleared < 6 else 88)
    def hud(d):
        y = WY0 + 26
        d.text((WX0 + 28, y), 'HP', font=F(44), fill=(255, 214, 60), stroke_width=5, stroke_fill=(10, 10, 20))
        bx0, bx1 = WX0 + 132, WX0 + 448
        d.rectangle([bx0, y, bx1, y + 44], fill=(40, 30, 50), outline=(240, 230, 200), width=4)
        col = (220, 70, 70) if hp < 35 else (240, 200, 60) if hp < 70 else (110, 220, 90)
        d.rectangle([bx0 + 5, y + 5, bx0 + 5 + int((bx1 - bx0 - 10) * hp / 100), y + 39], fill=col)
        s = f'{int(hp)}/100'; tw = d.textlength(s, font=F(44))
        d.text((WX1 - 26 - tw, y), s, font=F(44), fill=(255, 255, 255), stroke_width=5, stroke_fill=(10, 10, 20))
        for i, (joke, cap, c) in enumerate(DEBUFF):
            x = WX0 + 22; yy = WY0 + 92 + i * 64
            done = t >= TCL[i]
            d.rounded_rectangle([x, yy, x + 44, yy + 44], 7, fill=c if not done else (110, 220, 90), outline=(10, 10, 20), width=3)
            if done: d.line([x + 9, yy + 23, x + 19, yy + 33, x + 36, yy + 11], fill=(255, 255, 255), width=6)
            d.text((x + 58, yy), joke, font=F(44), fill=(245, 245, 245) if not done else (120, 125, 135), stroke_width=5, stroke_fill=(10, 10, 20))
            if done:
                tw = d.textlength(joke, font=F(44)); d.line([x + 54, yy + 22, x + 62 + tw, yy + 22], fill=(230, 80, 80), width=6)
    layer(img, hud)
    for i, tc in enumerate(TCL):
        u = t - tc
        if 0 <= u < 0.9:
            aa = int(255 * min(1, (0.9 - u) / 0.3))
            layer(img, lambda d, u=u, aa=aa: ctext(d, WX0 + 290, WY0 - 60 - u * 50, '+15 HP', F(48), (255, 214, 60), 8, aa))
        stamp(img, DEBUFF[i][1], 'CLEARED!', u)
    if t >= T_END:
        u = t - T_END
        stamp(img, 'ALL DEBUFFS', 'CLEARED!', u if u < 0.15 else 0.15)
        gu = min(1, u / 0.6); gx, gy = bez((CX, CY), (CX + 200, CY - 200), (JX - 95, JY - 118), gu)
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        if u >= 0.55:
            a2 = int(255 * min(1, (u - 0.55) / 0.12))
            def tag(d, a=a2):
                s_ = 'ACV GUMMY'; f_ = F(44); tw = d.textlength(s_, font=f_); x1 = JX - 95 - GUM.width / 2 - 26; x0 = x1 - tw - 36; y0 = JY - 118 - 36
                d.rounded_rectangle([x0, y0, x1, y0 + 72], 14, fill=(14, 10, 24, int(235 * a / 255)), outline=(90, 200, 80, a), width=5)
                d.polygon([(x1 - 2, y0 + 22), (x1 - 2, y0 + 50), (x1 + 22, y0 + 36)], fill=(90, 200, 80, a))
                d.text((x0 + 18, y0 + 14), s_, font=f_, fill=(255, 255, 255, a), stroke_width=5, stroke_fill=(10, 10, 20, a))
            layer(img, tag)
        layer(img, lambda d: ctext(d, 400, 938, '+100 HP', F(60), (255, 214, 60), 9))
    img.alpha_composite(HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]: frame(int(float(ts) * FPS)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v31_noaudio.mp4'], stdin=subprocess.PIPE)
for f in range(N): ff.stdin.write(frame(f).convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v31_events.json', 'w')); print('done', T_END, DUR)
