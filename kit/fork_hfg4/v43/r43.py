# rc6 recut of #43 (Bennett: safe zone only, so rule + legibility + universal fixes). Source: fork_sz38/r43_sz.py
import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['FINALLY MADE IT', 'TO A SAVE POINT'], accent=1, color=(255, 214, 60), size=64)   # hfg4: soft fade, no box
K = 6; FOOTY = 78 * K                       # characters 4x -> 6x
GROUND = 1200; SHIFT = 1520 - GROUND        # background floor follows the ground (was 340 for ground 1180)
BG = bg_frames('recov_hd.gif', (W, H), box=(677, 0, 1284, 1080), step=1)
WALK = [up(f.resize((92, 92), Image.NEAREST), K) for f in gif_frames(A + 'hollow-walk-side.gif')]
SIT = seq(SP0 + 'fork_a4/hollow_sit', K)
RIDLE = idle('ray', K); RCAST = seq(SP0 + 'fork3/ray_cast', K, 1)
CRY = up(crop(Image.open(SP0 + 'fork_a3/crystal/05.png').convert('RGBA')), 4)
MEL = gummy('mel', 4)                       # Syeda's melatonin gummy (Rayleigh / Recovery)
XH = 255; XR = 640; XC = 452
def shifted(fr):
    o = Image.new('RGBA', (W, H)); o.alpha_composite(fr, (0, -SHIFT)); o.alpha_composite(fr.crop((0, H - SHIFT, W, H)), (0, H - SHIFT)); return o
BG = [shifted(b) for b in BG]
def put(img, spr, cx, foot=GROUND): img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOTY)))
BX = (72, 1250, 884, 1494)
def box(img, name, text, n, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = BX
    d.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x1, y1], fill=(16, 18, 44, 245), outline=(235, 235, 255, 255), width=6)
    d.rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10], outline=(90, 100, 160, 255), width=3)
    tw = d.textlength(name, font=F(40)); d.rectangle([x1 - tw - 70, y0 - 52, x1 - 20, y0 + 6], fill=col + (255,), outline=(235, 235, 255, 255), width=4)
    d.text((x1 - tw - 45, y0 - 40), name, font=F(40), fill=(255, 255, 255))
    y = y0 + 40
    for ln in text[:n].split('\n'):
        assert d.textlength(ln, font=F(44)) <= x1 - x0 - 56, ln
        d.text((x0 + 28, y), ln, font=F(44), fill=(255, 255, 255)); y += 62
    img.alpha_composite(L)
T_ARR, T_SAVE = 1.0, 1.1                    # Hollow already mid-stride in frame at 0.0 (was entering from off-screen until 1.45s)
LINES = [(1.75, 'I saved your game\nfor you.'), (3.4, "You're doing\nbetter than\nyou think.")]
T_GUM = 4.2; T_EAT = 5.0; T_END = 6.4       # melatonin gummy toss 4.2-5.0s, Zzz rest from 5.0s, end 6.4s then loops
T_GS_END = 2.3                              # GAME SAVED holds until 0.55s after the dialogue opens
NF = int(round(T_END * FPS)); wr = Writer('v43_noaudio.mp4'); ev = []
X_START = 165
for f in range(NF):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    bob = 10 * math.sin(t * 2.6); cy = GROUND - 250 + bob
    flash = max(0.0, 1 - abs(t - T_SAVE - 0.15) / 0.45) if t > T_SAVE - 0.3 else 0.0
    def glow(d):
        for r, a in ((170, 35), (125, 60), (90, 90)):
            aa = int(min(255, a * (1 + 2.2 * flash)))
            d.ellipse([XC - r, cy - r, XC + r, cy + r], fill=(150, 210, 255, aa))
        d.ellipse([XC - 100, GROUND - 22, XC + 100, GROUND + 10], fill=(120, 190, 255, int(70 + 120 * flash)))
    layer(img, glow)
    img.alpha_composite(CRY, (int(XC - CRY.width / 2), int(cy - CRY.height / 2)))
    def spark(d):
        for k in range(10):
            ph = (t * 0.6 + k * 0.1) % 1.0; sx = XC + 80 * math.sin(k * 2.4 + t); sy = cy + 90 - ph * 300
            a = int(220 * (1 - ph)); d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(220, 240, 255, a))
    layer(img, spark)
    if T_SAVE <= t < T_SAVE + 0.9: put(img, RCAST[min(len(RCAST) - 1, int((t - T_SAVE) / 0.9 * len(RCAST)))], XR)
    else: put(img, RIDLE[int(t * 8) % len(RIDLE)], XR)
    if t < T_ARR:
        x = X_START + (XH - X_START) * (t / T_ARR); put(img, WALK[(int(t * 7) + 2) % len(WALK)], x)
    else:
        k = min(len(SIT) - 1, int((t - T_ARR) / 0.6 * len(SIT))); put(img, SIT[k], XH)
    # melatonin gummy tossed from Rayleigh to the Hollow, labelled on its first (only) appearance
    if T_GUM <= t < T_EAT:
        u = (t - T_GUM) / (T_EAT - T_GUM); gx = XR - 90 + (XH + 30 - (XR - 90)) * u; gy = GROUND - 330 - 170 * math.sin(math.pi * u)
        img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
        def tag(d):
            fz = F(48); s_ = 'MELATONIN'; tw = d.textlength(s_, font=fz); tx = W / 2 - 60; ty = gy - MEL.height / 2 - 80   # hfg4: one word, no plate
            d.text((tx - tw / 2, ty + 2), s_, font=fz, fill=(225, 200, 255), stroke_width=8, stroke_fill=(10, 6, 18))
        layer(img, tag)
    # payoff: melatonin = sleep. The Hollow dozes off at the save point (big Zzz, held to the end)
    if t >= T_EAT:
        v = t - T_EAT
        if v < 0.25:
            def pop(d):
                r = 30 + 160 * v
                d.ellipse([XH + 30 - r, GROUND - 330 - r, XH + 30 + r, GROUND - 330 + r], outline=(200, 160, 255, int(255 * (1 - v / 0.25))), width=8)
            layer(img, pop)
        items = []
        for j, (sz, dx, dy, t0) in enumerate([(64, 40, 0, 0.0), (84, 110, -100, 0.25), (104, 190, -215, 0.5)]):
            if v >= t0:
                a = int(255 * min(1, (v - t0) / 0.15)); wob = 8 * math.sin((t - t0) * 5)
                items.append((XH + dx + wob, GROUND - 385 + dy, 'Z', sz, (240, 230, 255), 10, a))
        text_layer(img, items)
    items = []
    if T_SAVE <= t < T_GS_END:
        a = int(255 * min(1, (T_GS_END - t) / 0.25)); items.append((W / 2, HB + 40, 'GAME SAVED', 64, (170, 225, 255), 9, a))
    text_layer(img, items)
    for i, (ts, txt) in enumerate(LINES):
        tend = LINES[i + 1][0] if i + 1 < len(LINES) else 99
        if ts <= t < tend:
            n = int((t - ts) * 30) + 1
            box(img, 'RAYLEIGH', txt, n, (107, 45, 107))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 40, 66, 140, 160, 175, NF - 1): img.convert('RGB').save(f'p43_{f:04d}.png')
wr.close()
ev += [(T_SAVE, 'chime'), (T_SAVE + 0.05, 'twinkle'), (LINES[0][0], 'swish'), (LINES[1][0], 'swish'), (T_GUM, 'boing'), (T_EAT, 'squish'), (T_EAT + 0.3, 'poof')]
json.dump({'events': ev}, open('v43_ev.json', 'w')); print('done', NF)
