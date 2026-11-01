import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1'); from hook2 import hook_layer2
HOOK, HB = hook_layer2(['Which jar is', "Cyrus's?"], accent=1, color=(255, 160, 40), sub='Comment A, B, C or D')
import numpy as np
G = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a11/gen/'
def pk(d, i): return crop(Image.open(f'{G}{d}/{i:02d}.png').convert('RGBA'))
DOCK = up(pk('dock', 0), 7); JAR = up(pk('mjar', 0), 4)
FISH = [up(pk('fish', i), 3) for i in (1, 5, 11)]
KELP = [up(pk('kelp', i), 3) for i in (0, 3, 5, 9, 13)]
ROCK = [up(pk('rock', i), 3) for i in (1, 2, 12)]
NAMES = ['joy', 'cyrus', 'cleo', 'ray']; LBL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
GCOL = {'joy': (120, 210, 90), 'cyrus': (255, 160, 40), 'cleo': (110, 160, 255), 'ray': (200, 120, 240)}
IDL = {g: idle(g, 4) for g in NAMES}   # guides 4x (RECUT_BRIEF rule)
SURF = 968; DECK = 860; BED = 1468; TOP = 1050   # TOP: lines drop straight down past the dock planks, tangle starts below
LANES = [170, 365, 560, 755]
GX = [150, 405, 675, 930]
PERM = [2, 0, 3, 1]          # joy->C, cyrus->A, cleo->D, ray->B  (never shown)
rnd = random.Random(int(os.environ.get('PS', '11')))
# simpler tangle (review): 5 single crossings, ladder style; Cyrus's line zig-zags lane 1 -> 2 -> 1 -> 0 (A)
order = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 3, 1], [1, 2, 3, 0], [2, 1, 3, 0], [2, 0, 3, 1]]
assert order[-1] == PERM
levels = list(np.linspace(TOP, BED - 95, len(order)))
JIT = [[rnd.uniform(-10, 10) for _ in range(len(levels))] for _ in range(4)]
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
    img = FOREST[int(t * 6) % len(FOREST)].copy().resize((1740, 980)).crop((330, 0, 1410, 980))
    canvas = Image.new('RGBA', (W, H), (14, 10, 24, 255)); canvas.alpha_composite(img, (0, SURF - 980 + 12))
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
    def plates(d):
        for j, x in enumerate(LANES):
            d.rounded_rectangle([x - 36, BED - 52, x + 36, BED + 16], 10, fill=(14, 10, 24, 225), outline=(255, 214, 60, 255), width=4)
    layer(canvas, plates)
    # dock and guides
    canvas.alpha_composite(DOCK, ((W - DOCK.width) // 2, DECK - 90))
    tips = []
    for i, g in enumerate(NAMES):
        fr = IDL[g][int(t * 6) % len(IDL[g])]
        fx = GX[i]; canvas.alpha_composite(fr, (int(fx - fr.width / 2), int(DECK - 78 * 4)))
        tips.append((fx + 80, DECK - 270))
    def rods(d):
        for i, (tx, ty) in enumerate(tips):
            hx, hy = GX[i] + 32, DECK - 139
            d.line([(hx, hy), (tx, ty)], fill=(110, 70, 35, 255), width=7)
            d.line([(hx, hy), (tx, ty)], fill=(160, 110, 60, 255), width=3)
    layer(canvas, rods)
    # fish + bubbles BEHIND the lines (review: fish were hiding the lines)
    for k, (y0, sp, ph, f) in enumerate([(1040, 170, 0, 0), (1180, -140, 3.0, 1), (1310, 120, 6.0, 2)]):
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
    # fishing lines: ONE continuous line per rod, from the rod tip straight down in front of the dock,
    # into the water and through the tangle to its jar. Drawn above the dock so nothing cuts it.
    rev = 0.0 if t < 0.55 else min(1.0, (t - 0.55) / 0.85)   # line sinks from the tip after the cast
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i, cv in enumerate(CURVES):
        tx, ty = tips[i]
        drop = [(tx, ty + k * (cv[0][1] - ty) / 24.0) for k in range(24)]
        full = drop + [(float(p[0]), float(p[1])) for p in cv]
        pts = []
        for (px, py) in full:
            amp = 5 * max(0.0, min(1.0, (py - TOP) / 60.0))
            pts.append((px + amp * math.sin(py * 0.012 + t * 1.6 + i), py))
        if t < 0.55:
            n = 0
        else:
            n = len(drop) + int(rev * (len(full) - len(drop)))
        # above-water part is always there (hangs from the tip); underwater part sinks in after the cast
        vis = pts[:max(len(drop) + 1, n)] if t >= 0.55 else [p for p in pts if p[1] <= SURF - 6]
        if len(vis) > 1:
            d.line(vis, fill=(20, 28, 46, 255), width=17, joint='curve')
            d.line(vis, fill=(245, 248, 255, 255), width=9, joint='curve')
            for (px, py) in (vis[0], vis[-1]):
                d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(20, 28, 46, 255)); d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(245, 248, 255, 255))
        if rev >= 1.0:
            hx, hy = pts[-1]
            d.arc([hx - 14, hy - 4, hx + 10, hy + 26], 200, 520, fill=(170, 175, 190, 255), width=5)
    canvas.alpha_composite(L)
    def splash(d):
        if 0.55 < t < 1.6:
            u = (t - 0.55) / 1.05
            for i, (tx, ty) in enumerate(tips):
                for s_ in range(8):
                    a = s_ * 0.785; rr = 10 + 60 * u
                    d.rectangle([tx + rr * math.cos(a) - 5, SURF - 6 - abs(rr * math.sin(a)) * 0.6 - 5, tx + rr * math.cos(a) + 5, SURF - 6 - abs(rr * math.sin(a)) * 0.6 + 5], fill=(220, 245, 255, int(255 * (1 - u))))
    layer(canvas, splash)
    # labels
    items = []
    # only Cyrus is labelled (44px, orange): the other labels were ~28px, under the 44px floor
    items.append((360, DECK + 6 + 5 * abs(math.sin(t * 4)), 'CYRUS', 44, GCOL['cyrus'], 8, 255))
    for j, x in enumerate(LANES): items.append((x, BED - 44, 'ABCD'[j], 52, (255, 214, 60), 7, 255))
    text_layer(canvas, items)
    # vertical timer bar on the right (the jar row now uses the old footer space); red pulse for the last 3s
    T0, T1, TR = 1.4, 8.0, 5.0
    if t < T1:
        k = 1 - max(0, min(1, (t - T0) / (T1 - T0)))
        red = t >= TR; pul = (0.5 + 0.5 * math.sin((t - TR) * 2 * math.pi * 2)) if red else 0
        def bar(d):
            x0, x1, y0, y1 = 838, 884, 1110, 1490
            if red: d.rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], fill=(255, 40, 40, int(150 * pul)))
            d.rectangle([x0, y0, x1, y1], fill=(14, 10, 24, 230), outline=(255, 214, 60, 255), width=5)
            hh = (y1 - y0 - 14) * k
            c = (255, 50 + int(60 * pul), 50) if red else (120, 210, 90)
            d.rectangle([x0 + 7, y1 - 7 - hh, x1 - 7, y1 - 7], fill=c + (255,))
        layer(canvas, bar)
    else:
        u = t - T1; sc = 1.0 + 0.15 * max(0, 1 - u / 0.12)    # hard pop: scale-in over 4 frames
        cw, ch = 860, 150
        card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, cw - 1, ch - 1], 24, fill=(14, 10, 24, 240), outline=(255, 214, 60, 255), width=8)
        ff = ImageFont.truetype(FONT, 76); tw = cd.textlength("TIME'S UP!", font=ff)
        cd.text(((cw - tw) / 2, (ch - 76) / 2), "TIME'S UP!", font=ff, fill=(255, 214, 60), stroke_width=9, stroke_fill=(10, 6, 18))
        if sc > 1.01: card = card.resize((int(cw * sc), int(ch * sc)), Image.NEAREST)
        canvas.alpha_composite(card, (int(547 - card.width / 2), int(905 - card.height / 2)))   # over the dock: the tangle stays visible
    canvas.alpha_composite(HOOK)
    return canvas
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in (0.7, 3.0, 6.0, 8.05, 9.0): frame_at(t).convert('RGB').save(f'h_still_{t}.png')
        sys.exit()
    DUR = 9.4; wr = Writer('v1_noaudio.mp4'); ev = []
    for f in range(int(DUR * FPS)):
        t = f / FPS; wr.write(frame_at(t))
    wr.close()
    ev = [(0.55, 'swish'), (0.75, 'jump'), (1.0, 'chime')] + [(1.4 + k, 'tick_8bit') for k in range(4)] + [(5.0 + 0.5 * k, 'tick_8bit') for k in range(6)] + [(8.0, 'buzz_8bit')]
    json.dump({'events': ev}, open('ev.json', 'w')); print('done')
