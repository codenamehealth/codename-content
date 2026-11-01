import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['Which jar is', "Cyrus's?"], accent=1, color=(255, 160, 40), sub='Follow the line')
import numpy as np
G = '../gen/'
def pk(d, i): return crop(Image.open(f'{G}{d}/{i:02d}.png').convert('RGBA'))
DOCK = up(pk('dock', 0), 7); JAR = up(pk('mjar', 0), 4)
FISH = [up(pk('fish', i), 3) for i in (1, 5, 11)]
KELP = [up(pk('kelp', i), 3) for i in (0, 3, 5, 9, 13)]
ROCK = [up(pk('rock', i), 3) for i in (1, 2, 12)]
NAMES = ['joy', 'cyrus', 'cleo', 'ray']; LBL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
GCOL = {'joy': (120, 210, 90), 'cyrus': (255, 160, 40), 'cleo': (110, 160, 255), 'ray': (200, 120, 240)}
IDL = {g: idle(g, 3) for g in NAMES}
SURF = 908; DECK = 800; BED = 1350
LANES = [170, 365, 560, 755]
GX = [150, 405, 675, 930]
PERM = [2, 0, 3, 1]          # joy->C, cyrus->A, cleo->D, ray->B  (never shown)
rnd = random.Random(int(os.environ.get('PS', '11')))
levels = list(np.linspace(SURF + 30, BED - 95, 7))
order = [list(range(4))]
for k in range(len(levels) - 2):
    while True:
        p = list(range(4)); rnd.shuffle(p)
        if sum(p[i] != order[-1][i] for i in range(4)) >= 3: break
    order.append(p)
order.append(PERM)
JIT = [[rnd.uniform(-30, 30) for _ in range(len(levels))] for _ in range(4)]
def curve(i):
    xs = [GX[i] + 66] + [LANES[order[k][i]] + (JIT[i][k] if 0 < k < len(levels) - 1 else 0) for k in range(1, len(levels))]
    xs[-1] = LANES[PERM[i]]
    out = []
    for k in range(len(levels) - 1):
        for s in np.linspace(0, 1, 40, endpoint=False):
            e = s * s * (3 - 2 * s)
            out.append((xs[k] + (xs[k + 1] - xs[k]) * e, levels[k] + (levels[k + 1] - levels[k]) * s))
    out.append((xs[-1], levels[-1])); out.append((xs[-1], BED - 70))
    return out
CURVES = [curve(i) for i in range(4)]
# header / shore: Liza's forest
FOREST = bg_frames('found_hd.gif', (1080, 608), box=(0, 0, 1920, 1080), step=2)
# static underwater layer
UW = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ud = ImageDraw.Draw(UW)
for y in range(SURF, H):
    k = (y - SURF) / (H - SURF)
    ud.line([(0, y), (W, y)], fill=(int(70 - 50 * k), int(170 - 110 * k), int(190 - 90 * k), 255))
sand = Image.new('RGBA', (W, H - BED), (0, 0, 0, 0)); sd = ImageDraw.Draw(sand)
rs = random.Random(3)
for y in range(0, H - BED, 6):
    for x in range(0, W, 6):
        c = rs.choice([(214, 186, 128), (204, 174, 116), (224, 198, 140), (196, 166, 110)])
        sd.rectangle([x, y, x + 5, y + 5], fill=c + (255,))
UW.alpha_composite(sand, (0, BED))
ud.line([(0, BED), (W, BED)], fill=(160, 130, 80, 255), width=6)
for i, (x, kk) in enumerate([(40, 0), (300, 1), (540, 2), (800, 3), (1010, 4), (190, 2), (860, 0)]):
    kl = KELP[kk]; UW.alpha_composite(kl, (x - kl.width // 2, BED + 10 - kl.height))
for x, r in [(260, 0), (560, 1), (790, 2), (980, 0)]:
    rk = ROCK[r]; UW.alpha_composite(rk, (x - rk.width // 2, BED + 30 - rk.height))
def frame_at(t):
    img = FOREST[int(t * 6) % len(FOREST)].copy().resize((1630, 918)).crop((275, 0, 1355, 918))
    canvas = Image.new('RGBA', (W, H), (14, 10, 24, 255)); canvas.alpha_composite(img, (0, SURF - 918 + 10))
    canvas.alpha_composite(UW)
    # light rays
    def rays(d):
        for k in range(6):
            x0 = (k * 230 + t * 40) % 1400 - 200
            d.polygon([(x0, SURF), (x0 + 70, SURF), (x0 + 330, H), (x0 + 200, H)], fill=(255, 255, 230, 18))
    layer(canvas, rays)
    # surface shimmer
    def surf(d):
        for x in range(0, W, 12):
            yy = SURF + int(4 * math.sin(x * 0.03 + t * 3))
            d.rectangle([x, yy - 3, x + 8, yy + 1], fill=(200, 240, 255, 150))
    layer(canvas, surf)
    # jars and labels
    for j, x in enumerate(LANES):
        canvas.alpha_composite(JAR, (x - JAR.width // 2, BED + 26 - JAR.height))
    # lines (fade in after the cast)
    la = 0 if t < 0.9 else min(1, (t - 0.9) / 0.5)
    if la > 0:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i, cv in enumerate(CURVES):
            pts = [(float(p[0]) + 5 * math.sin(p[1] * 0.012 + t * 1.6 + i), float(p[1])) for p in cv]
            d.line(pts, fill=(30, 40, 60, int(255 * la)), width=13, joint='curve')
            d.line(pts, fill=(235, 240, 250, int(255 * la)), width=7, joint='curve')
            hx, hy = pts[-1]
            d.arc([hx - 14, hy - 4, hx + 10, hy + 26], 200, 520, fill=(170, 175, 190, int(255 * la)), width=5)
        canvas.alpha_composite(L)
    # fish swimming over the lines
    for k, (y0, sp, ph, f) in enumerate([(1010, 170, 0, 0), (1150, -140, 3.0, 1), (1265, 120, 6.0, 2)]):
        fx = ((t * sp + ph * 200) % 1400) - 160 if sp > 0 else W + 160 - ((t * -sp + ph * 200) % 1400)
        fi = FISH[f] if sp > 0 else FISH[f].transpose(Image.FLIP_LEFT_RIGHT)
        if sp > 0: fi = fi.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.alpha_composite(fi, (int(fx - fi.width / 2), int(y0 + 10 * math.sin(t * 2 + k) - fi.height / 2)))
    # bubbles
    def bub(d):
        rb = random.Random(7)
        for k in range(26):
            bx = rb.uniform(30, W - 30); sp = rb.uniform(60, 140); r = rb.choice([4, 6, 8])
            by = BED - ((t * sp + rb.uniform(0, 900)) % (BED - SURF))
            d.ellipse([bx + 6 * math.sin(t * 3 + k) - r, by - r, bx + 6 * math.sin(t * 3 + k) + r, by + r], outline=(220, 245, 255, 170), width=2)
    layer(canvas, bub)
    # dock and guides
    canvas.alpha_composite(DOCK, ((W - DOCK.width) // 2, DECK - 90))
    tips = []
    for i, g in enumerate(NAMES):
        fr = IDL[g][int(t * 6) % len(IDL[g])]
        fx = GX[i]; canvas.alpha_composite(fr, (int(fx - fr.width / 2), int(DECK - 78 * 3)))
        tips.append((fx + 66, DECK - 228))
    def rods(d):
        for i, (tx, ty) in enumerate(tips):
            hx, hy = GX[i] + 24, DECK - 104
            d.line([(hx, hy), (tx, ty)], fill=(110, 70, 35, 255), width=7)
            d.line([(hx, hy), (tx, ty)], fill=(160, 110, 60, 255), width=3)
            d.line([(tx, ty), (tx, SURF - 20)], fill=(235, 240, 250, 230), width=3)
            if 0.55 < t < 1.6:
                u = (t - 0.55) / 1.05
                for s in range(8):
                    a = s * 0.785; rr = 10 + 60 * u
                    d.rectangle([tx + rr * math.cos(a) - 5, SURF - 6 - abs(rr * math.sin(a)) * 0.6 - 5, tx + rr * math.cos(a) + 5, SURF - 6 - abs(rr * math.sin(a)) * 0.6 + 5], fill=(220, 245, 255, int(255 * (1 - u))))
    layer(canvas, rods)
    # labels
    items = []
    for i, g in enumerate(NAMES):
        col = GCOL[g] if g == 'cyrus' else (245, 240, 225)
        items.append((GX[i], DECK + 4 + (4 * abs(math.sin(t * 4)) if g == 'cyrus' else 0), LBL[g], 28 if g != 'ray' else 24, col, 6, 255))
    for j, x in enumerate(LANES): items.append((x, BED + 46, 'ABCD'[j], 52, (255, 214, 60), 7, 255))
    text_layer(canvas, items)
    # footer timer
    T0, T1 = 1.4, 8.6
    if t < T1:
        k = 1 - max(0, min(1, (t - T0) / (T1 - T0)))
        def bar(d):
            d.rectangle([90, 1458, 860, 1490], fill=(14, 10, 24, 220), outline=(255, 214, 60, 255), width=4)
            d.rectangle([96, 1464, 96 + (860 - 102) * k, 1484], fill=(255, 160, 40, 255) if k < 0.3 else (120, 210, 90, 255))
        layer(canvas, bar)
    else:
        u = min(1, (t - T1) / 0.3)
        def ov(d): d.rounded_rectangle([110, 900, 870, 1170], 24, fill=(14, 10, 24, int(225 * u)), outline=(255, 214, 60, int(255 * u)), width=6)
        layer(canvas, ov)
        text_layer(canvas, [(490, 940, "TIME'S UP!", 62, (255, 214, 60), 8, int(255 * u)), (490, 1060, 'Comment A, B, C or D', 34, (255, 255, 255), 6, int(255 * u))])
    canvas.alpha_composite(HOOK)
    return canvas
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in (0.7, 3.0, 9.3): frame_at(t).convert('RGB').save(f'h_still_{t}.png')
        sys.exit()
    DUR = 10.6; wr = Writer('v0h_noaudio.mp4'); ev = []
    for f in range(int(DUR * FPS)):
        t = f / FPS; wr.write(frame_at(t))
    wr.close()
    ev = [(0.55, 'swish'), (0.75, 'jump'), (1.0, 'chime')] + [(1.4 + k, 'tick_8bit') for k in range(7)] + [(8.6, 'buzz_8bit')]
    json.dump(ev, open('ev.json', 'w')); print('done')
