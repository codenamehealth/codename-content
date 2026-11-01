# r060 recut (rc7): same puzzle (right Cleo's silver crossguard), never revealed.
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
import numpy as np
os.chdir(SP + 'fork_b6'); OUT = SP + 'fork_hfg6/v60/'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade   # Oct 29: soft fade, no box, comment line cut
HOOK, HB = hook_fade(['ONLY 1', 'DIFFERENCE'], accent=1); print('HB', HB)
HOOK_END, _ = hook_fade(["TIME'S UP!", 'SPOT IT?'], accent=0, color=(232, 182, 76))
PX0, PX1, PY0, PY1 = 70, 1010, HB + 10, 1150
K = 8; FY = 1112; XL, XR = 290, 810   # Oct 29: halves 520px apart so the copied background fills the frame edge to edge
T1 = 7.0; HOLD = 1.4; N = int(round((T1 + HOLD) * FPS))
BG = bg_frames('vit_hd.gif', (W, H), box=(846, 0, 1454, 1080), step=1, bright=0.62)
src = gif_frames(A + 'idle_3.gif')
def native(f): return f.resize((92, 92), Image.NEAREST)
L5 = [up(native(f), K) for f in src]
def silver(f):
    a = np.array(native(f))
    for y in range(54, 70):
        for x in range(55, 70):
            c = tuple(a[y, x][:3])
            if c == (214, 141, 33): a[y, x, :3] = (120, 126, 148)
            elif c == (255, 213, 0): a[y, x, :3] = (214, 218, 232)
    return up(Image.fromarray(a), K)
R5 = [silver(f) for f in src]
GUM = gummy('cre', 3)
THINK = seq(PL + '../fork2/hollow_think', 3, 1)
FOOT = 78 * K; HALF = 46 * K
ev = [(0.05, 'ding_8bit')] + [(T1 - k, 'tick_8bit') for k in (3, 2, 1)] + [(T1, 'buzz_8bit')]
w = Writer(OUT + 'v60_noaudio.mp4'); rng = random.Random(3)
SP_ = [(rng.uniform(85, 525), rng.uniform(PY0 + 20, PY1 - 20), rng.uniform(0, 6.3)) for _ in range(14)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    img.paste(img.crop((540 - (XR - XL), 0, 1080 - (XR - XL), H)), (540, 0))   # Oct 29 full-bleed: right half = the left scene shifted by the Cleo offset, full height (identical backgrounds, no panel)
    P = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def panel(d):
        for x in (XL, XR):
            d.ellipse([x - 170, FY - 34, x + 170, FY + 30], fill=(46, 93, 168, 90), outline=(123, 157, 209, 200), width=4)
            d.ellipse([x - 125, FY - 20, x + 125, FY + 18], fill=(0, 0, 0, 70))
        for sx, sy, ph in SP_:
            a = int(140 + 110 * math.sin(t * 3 + ph))
            if a > 150:
                for ox in (0, XR - XL): d.rectangle([sx + ox - 3, sy - 3, sx + ox + 3, sy + 3], fill=(200, 220, 255, a - 100))
    panel(ImageDraw.Draw(P))
    d = ImageDraw.Draw(P)
    d.rectangle([536, 0, 543, PY1], fill=(20, 14, 30)); d.rectangle([538, 0, 541, PY1], fill=(232, 182, 76))   # divider only, no panel frame
    k = int(t * 6) % len(L5)
    P.alpha_composite(L5[k], (XL - HALF, FY - FOOT)); P.alpha_composite(R5[k], (XR - HALF, FY - FOOT))
    bob = int(8 * math.sin(t * 3))
    for x in (XL, XR): P.alpha_composite(GUM, (x + 120, PY0 + 40 + bob))
    s = 1.0 if t >= 0.3 else 0.9 + 0.1 * (t / 0.3) ** 0.5
    if s < 1:
        cx, cy = (PX0 + PX1) / 2, (PY0 + PY1) / 2; P2 = P.resize((int(W * s), int(H * s)), Image.NEAREST)
        P = Image.new('RGBA', (W, H), (0, 0, 0, 0)); P.alpha_composite(P2, (int(cx - cx * s), int(cy - cy * s)))
    img.alpha_composite(P)
    # timer from frame 0: bar + one big seconds digit
    u = max(0.0, min(1.0, t / T1)); rem = max(0, math.ceil(T1 - t - 1e-6))
    col = (90, 200, 80) if rem > 3 else (240, 80, 70)
    TY0, TY1 = PY1 + 16, PY1 + 62
    layer(img, lambda dd: dd.rounded_rectangle([80, TY0, 740, TY1], 16, fill=(12, 10, 26, 200)))   # the bar's own dark track
    d = ImageDraw.Draw(img)
    if u < 1: d.rounded_rectangle([88, TY0 + 8, 88 + int(644 * (1 - u)), TY1 - 8], 12, fill=col)
    d.rounded_rectangle([80, TY0, 740, TY1], 16, outline=(232, 182, 76), width=4)
    pulse = 1 + (0.22 * max(0, 1 - ((t - (T1 - 3)) % 1.0) / 0.25) if rem <= 3 and t < T1 else 0)
    text_layer(img, [(820, (TY0 + TY1) / 2 - 32 * pulse, str(rem), int(64 * pulse), col, 8, 255)])
    # Hollow thinking with a '?' thought bubble only
    th = THINK[int(t * 7) % len(THINK)]
    img.alpha_composite(th, (250 - th.width // 2, 1496 - 78 * 3))
    def bub(dd):
        dd.ellipse([370, 1250, 530, 1370], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=5)
        dd.ellipse([336, 1364, 364, 1390], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=4)
        dd.ellipse([314, 1396, 332, 1414], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=3)
    layer(img, bub); d = ImageDraw.Draw(img)
    ctext(d, 450, 1272 + int(4 * math.sin(t * 5)), '?', F(80), (232, 182, 76), 6)
    if t >= T1:
        u = t - T1; a = 1.0 if u > 0.1 else u / 0.1; pop = 1.0 if u > 0.1 else 0.8 + 2 * u
        pass   # Oct 29: no dim, no box over the Cleos; the hook flips to TIME'S UP! / SPOT IT? so both stay visible for a second look
    img.alpha_composite(HOOK_END if t >= T1 and ((t - T1) > 0.08 or int((t - T1) * 60) % 2) else HOOK)
    w.write(img)
    if f in (0, 5, 100, 200, 230): img.convert('RGB').save(OUT + f'k60_{f}.png')
w.close(); json.dump({'events': ev}, open(OUT + 'v60_ev.json', 'w')); print('ok', N / FPS)
