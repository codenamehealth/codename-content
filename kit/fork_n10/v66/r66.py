import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1')
from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
# rc8: comment prompt as a real 52px band line from frame 0; at TIME'S UP the band itself swaps
HOOK, HB = hook_fade(['WHICH GUMMY FITS', 'THE OUTLINE?'], accent=1)   # hfg7: soft fade, 'Comment A, B, C or D' cut (A-D plates invite it, caption asks)
HOOK2, HB2 = hook_fade(["TIME'S UP!"], accent=0, size=72)   # hfg7: TIME'S UP! replaces the hook in the same fade
import numpy as np
from skimage import measure
STILL = os.environ.get('STILL')
random.seed(66)
BGS = bg_frames('recov_hd.gif', (1214, 1920), box=(624, 0, 1264, 1080), step=2, bright=0.62)
def _shift(b):
    o = Image.new('RGBA', (W, H)); c = b.crop((67, 0, 67 + W, H))
    o.alpha_composite(c.crop((0, 100, W, H)), (0, 0)); o.alpha_composite(c.crop((0, H - 100, W, H)), (0, H - 100)); return o
BGS = [_shift(b) for b in BGS]
STARS = [(random.uniform(0, W), random.uniform(20, 780), random.uniform(0, 6.3), random.choice([2, 3, 4])) for _ in range(140)]
TGT = 'cre'   # Oct 29 n10: outline is now the creatine gummy (D); the apple was too easy. Only D is the wide, squat dome.
acv = Image.open(PL + f'gummies/pick_{TGT}.png').convert('RGBA'); m = np.array(acv)[..., 3] > 0
m = np.pad(m, 2)
cont = max(measure.find_contours(m.astype(float), 0.5), key=len)
cont = measure.approximate_polygon(cont, tolerance=0.5)   # n10 review: faithful contour so the gumdrop taper, squat width and tucked-in bottom read on a phone
# rc8: taller band (52px comment line) -> constellation 15x -> 14x and centred lower (y742 -> 806) so it clears the band
SC = 15; ch, cw = m.shape; CX0, CY0 = W / 2, 760   # hfg7: back to 15x and up 46px into the space the smaller hook freed
pts = [(CX0 + (c - cw / 2) * SC, CY0 + (r - ch / 2) * SC) for r, c in cont]
if pts[0] == pts[-1]: pts = pts[:-1]
print('target', TGT, 'stars', len(pts), 'outline y', min(p[1] for p in pts), max(p[1] for p in pts))
SIL = Image.fromarray((m * 255).astype(np.uint8), 'L').resize((cw * SC, ch * SC), Image.NEAREST)
SILX, SILY = int(CX0 - cw * SC / 2), int(CY0 - ch * SC / 2)
OPTS = [('A', 'mel'), ('B', 'mush'), ('C', 'acv'), ('D', 'cre')]
# rc8: gummies 4x -> 5x (+25%); ACV gets the gummy shine (VETTING: reads as a gummy, not a real apple)
GUM = {k: (up(acv_gummy_strong(), 5) if k == 'acv' else gummy(k, 5)) for _, k in OPTS}
PED = up(crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')), 3)
RAY = seq(SP + 'fork3/ray_cast', 4, 1)    # rc8: Rayleigh 3x -> 4x (~256px, brief: guides >= 4x)
# rc8 timing: constellation drawing from frame 0 (was 0.9s), 3.0s draw, 4s countdown (was 5.5s), TIME'S UP at 7.0s, 1.4s hold, then loop
T_DRAW0, T_DRAW1, T_TIMER0, T_TIMER1 = -0.4, 3.0, 3.0, 7.0; DUR = 7.8   # n10 review: TIME'S UP hold 1.4s -> 0.8s
BY = 1362; BAR = (90, 1054, 776, 1084)   # n10 review: countdown box now ends at x866 (was 912)
w = Writer('v66_noaudio.mp4'); events = []
NF = int(round(DUR * FPS))
for f in range(NF):
    if STILL and f not in [int(x) for x in STILL.split(',')]: continue
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for (x, y, ph, s) in STARS:
        a = int(110 + 100 * math.sin(t * 2.2 + ph)); d.rectangle([x, y, x + s, y + s], fill=(230, 235, 255, max(0, a)))
    img.alpha_composite(L)
    u = max(0.0, min(1.0, (t - T_DRAW0) / (T_DRAW1 - T_DRAW0))); n = len(pts); shown = u * n
    if t > T_DRAW1:
        a = int(min(1, (t - T_DRAW1) / 0.6) * 120)   # n10 review: stronger silhouette fill so the shape reads as a solid at phone size
        fill = Image.new('RGBA', SIL.size, (120, 150, 255, 0)); fill.putalpha(SIL.point(lambda p: a if p else 0))
        img.alpha_composite(fill, (SILX, SILY))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    k = int(shown)
    for i in range(min(k, n)):
        p, q = pts[i], pts[(i + 1) % n]
        d.line([p, q], fill=(150, 190, 255, 90), width=14); d.line([p, q], fill=(225, 240, 255, 230), width=4)
    if k < n and shown > 0:   # rc8: the line being drawn right now (also on frame 0)
        p, q = pts[k], pts[(k + 1) % n]; fr = shown - k; q = (p[0] + (q[0] - p[0]) * fr, p[1] + (q[1] - p[1]) * fr)
        d.line([p, q], fill=(150, 190, 255, 90), width=14); d.line([p, q], fill=(225, 240, 255, 230), width=4)
    for i in range(min(k + 1, n)):
        x, y = pts[i]; s = 9 + 3 * math.sin(t * 5 + i)
        d.ellipse([x - s - 6, y - s - 6, x + s + 6, y + s + 6], fill=(150, 190, 255, 70)); d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 255))
        d.line([x - s - 4, y, x + s + 4, y], fill=(255, 255, 255, 180), width=2); d.line([x, y - s - 4, x, y + s + 4], fill=(255, 255, 255, 180), width=2)
    img.alpha_composite(L)
    for i in range(n):
        ti = T_DRAW0 + (T_DRAW1 - T_DRAW0) * i / n
        if ti >= 0 and abs(t - ti) < 0.5 / FPS and i % 4 == 0: events.append((round(t, 3), 'twinkle'))
    # Rayleigh casting the stars (4x, feet y1000, body x~70-250)
    rf = RAY[int(t * 9) % len(RAY)] if t < T_DRAW1 + 0.3 else RAY[0]
    img.alpha_composite(rf, (-42, 1000 - 78 * 4))
    if t < T_DRAW1:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(f)
        for _ in range(12):
            v = rr.random(); x = 250 + v * 230 + rr.uniform(-30, 30); y = 830 - v * 260
            d.rectangle([x, y, x + 6, y + 6], fill=(200, 170, 255, 200))
        img.alpha_composite(L)
    # options on pedestals (gummies 5x)
    for i, (lab, kk) in enumerate(OPTS):
        cx = 172 + i * 204; by = BY
        img.alpha_composite(PED, (int(cx - PED.width / 2), by - PED.height // 2))
        g = GUM[kk]; bob = int(9 * math.sin(t * 2.6 + i * 1.3))
        gcy = by - 92 - g.height / 2 + bob
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.ellipse([cx - 88, gcy - 88, cx + 88, gcy + 88], fill=(255, 240, 200, 45)); img.alpha_composite(L)
        img.alpha_composite(g, (int(cx - g.width / 2), int(gcy - g.height / 2)))
        text_layer(img, [(cx, by + 70, lab, 60, (255, 214, 60), 8, 255)])
    d = ImageDraw.Draw(img)
    if t >= T_TIMER1:
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(t, 3), 'ding_8bit'))
    if T_TIMER0 <= t < T_TIMER1:
        u2 = (t - T_TIMER0) / (T_TIMER1 - T_TIMER0); col = (90, 220, 120) if u2 < 0.6 else (255, 200, 60) if u2 < 0.85 else (240, 80, 80)
        x0, y0, x1, y1 = BAR
        d.rounded_rectangle([x0, y0, x1, y1], 12, fill=(20, 18, 40), outline=(200, 190, 255), width=3)
        d.rounded_rectangle([x0 + 4, y0 + 4, x0 + 4 + int((x1 - x0 - 8) * (1 - u2)), y1 - 4], 10, fill=col)
        secs = int(math.ceil(T_TIMER1 - t)); ph = (secs - (T_TIMER1 - t))       # 0 at the tick, -> 1 just before the next
        sz = 72 if ph < 0.18 else 64      # rc8: big single digit at the bar's right end (was 30px under it), pops on each tick
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(L)
        d2.rounded_rectangle([x1 + 14, y0 - 34, x1 + 104, 1108], 14, fill=(14, 10, 24, 230), outline=col, width=4)
        ctext(d2, x1 + 59, (y0 - 34 + 1108) / 2 - sz / 2, str(secs), F(sz), col if secs <= 3 else (255, 255, 255), 6)
        img.alpha_composite(L)
        if secs <= 3 and abs((T_TIMER1 - t) - secs) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    img.alpha_composite(HOOK if t < T_TIMER1 else HOOK2)
    w.write(img)
    if STILL: img.convert('RGB').save(f'k66_{f}.png')
w.close(); json.dump({'events': events}, open('v66_ev.json', 'w')); print('HB', HB, HB2, events)
