import sys
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SP_ + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
DUR = 7.2; NF = int(round(DUR * FPS))   # review2: 10.0 -> 7.2s (4 eat cycles of 1.8s), ~3s after the reveal
# Oct 29 hookfade pass: boxed band, 'WHAT DAY ARE YOU ON?', '1 YEAR LATER' divider text and the ACV GUMMY tag cut; gold gummy out of the orbit
HOOK, HB = hook_fade(['+1 XP A DAY'], accent=0, size=72)
print('hook bottom', HB)
TOPB = bg_frames('found_hd.gif', (1707, 960), step=2, bright=0.8); TOPB = [b.crop((420, 0, 1500, 960)) for b in TOPB]
BOTB = bg_frames('sun_hd.gif', (1707, 960), step=2); BOTB = [b.crop((313, 0, 1393, 960)) for b in BOTB]
EAT = seq(SP_ + 'fork3/hollow_eat', 4, 0, 13); FOOT3 = 78 * 4          # Day 1 Hollow 3x -> 4x
VICT = vic('hollow', 384)
GUMS = [up(acv_gummy_strong(), 3) if k == 'acv' else gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre']]      # 'gold' gummy dropped (no gold rule; it read as a gold bell/nugget)
SMALLG = gummy('mush', 3)
# ---- n13 (Oct 29): Day 365 starts dark with a '?' (LV ?? bar filling); at T_REV it opens on the SAME small Hollow (LV 99)
# with his party: the four guides cheering in Syeda's victory poses (the arms-up set from #012, exact 4x) and the gummies orbiting him.
T_REV = float(os.environ.get('T_REV', 3.8)); T_DARK = DUR - 0.3      # reveal; fade back to dark for a seamless loop
def vic4(g):
    fr = gif_frames(A + VIC[g]); bb = None
    for f_ in fr:
        b = f_.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    return [up(f_.crop(bb).resize(((bb[2] - bb[0]) // 10, (bb[3] - bb[1]) // 10), Image.NEAREST), 4) for f_ in fr]   # 10x source -> exact 4x
VICS = {g: vic4(g) for g in ['joy', 'ray', 'cleo', 'cyrus', 'hollow']}      # hollow at 4x = 256px, same size as the Day 1 Hollow
GBACK, GFRONT = 1345, 1440
PARTY = [('joy', 330, GBACK, 0), ('ray', 712, GBACK, 3), ('cleo', 172, GFRONT, 1), ('cyrus', 806, GFRONT, 4)]   # (guide, x, feet y, frame offset)
HX2 = 500
QF = F(230)
crs = random.Random(11); CONF = [(crs.uniform(0, W), crs.uniform(-400, 0), crs.uniform(380, 620), crs.choice([(255, 214, 60), (255, 120, 120), (120, 220, 120), (150, 180, 255), (200, 130, 255)])) for _ in range(46)]
GUMS2 = [up(acv_gummy_strong(), 2) if k == 'acv' else gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']]
DIV0, DIV1 = 944, 956            # divider: thin gold seam only (the '1 YEAR LATER' band text is cut; DAY 365 says it)
BOFF = 1430 - 725                # bottom bg offset so the Hollow's ground sits at y1430
w = None if PREVIEW else Writer('v27_noaudio.mp4'); ev = []
rs = random.Random(5); LINES = [(rs.uniform(0, 1), rs.uniform(-150, 40), rs.choice((-1, 1)), rs.uniform(60, 150)) for _ in range(14)]
EATP = 1.8
for f in ([int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(NF)):
    t = f / FPS; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    tb = TOPB[int(t * 6) % len(TOPB)]; bb = BOTB[int(t * 6) % len(BOTB)]
    img.alpha_composite(tb, (0, -20))
    img.alpha_composite(bb.crop((0, DIV1 - BOFF, W, 960)), (0, DIV1))
    tail = bb.crop((0, 960 - (H - (BOFF + 960)), W, 960)).transpose(Image.FLIP_TOP_BOTTOM)
    img.alpha_composite(ImageEnhance.Brightness(tail).enhance(0.55), (0, BOFF + 960))
    # ---- top: day 1
    u = (t % EATP) / EATP; k = min(12, int(u * 1.6 * 13))
    hx, hy = 540, 860
    if u < 0.12:
        g = SMALLG; gy = HB + 10 + u / 0.12 * 150
        img.alpha_composite(g, (hx - g.width // 2, int(gy)))
    e = EAT[k if u < 0.62 else 0]
    pop = (t % EATP) - 0.55 * EATP
    spd = 0 <= pop < 0.75          # mushroom gummy = SPEED (SPEC 12): speed lines + dust + jitter when it kicks in
    jit = int(5 * math.sin(t * 80)) if spd and pop < 0.5 else 0
    if spd:
        a0 = min(1, (0.75 - pop) / 0.25)
        def lines(d):
            for (ph, dy, sd, ln) in LINES:
                x = hx + sd * (80 + ((pop * 3 + ph) % 1) * 260); y = hy - 130 + dy
                d.line([(x, y), (x + sd * ln, y)], fill=(255, 255, 255, int(200 * a0)), width=6)
            for j in range(3):
                r = 20 + pop * 70 + j * 12; dx = (j - 1) * 60
                d.ellipse([hx + dx - r, hy - r * 0.45, hx + dx + r, hy + r * 0.25], fill=(230, 210, 170, int(120 * a0)))
        layer(img, lines)
    layer(img, lambda d: d.ellipse([hx - 90, hy - 16, hx + 90, hy + 16], fill=(0, 0, 0, 90)))
    img.alpha_composite(e, (hx - e.width // 2 + jit, hy - FOOT3))
    items = [(214, HB + 20, 'DAY 1', 48, (140, 220, 255), 7, 255)]
    if spd:
        a = int(255 * min(1, (0.75 - pop) / 0.25)); sc = 1 + 0.3 * max(0, 1 - pop / 0.1)
        items.append((hx + 250, int(hy - 300 - pop * 50), '+1 XP', 56, (255, 230, 90), 9, a))
    text_layer(img, items)
    def bar1(d):
        d.rounded_rectangle([300, 880, 940, 916], 12, fill=(15, 15, 30, 220), outline=(120, 200, 255, 255), width=3)
        # review2: the bar grows a sliver on each +1 XP (eases in over 0.2s at the pop)
        n_ = int(t // EATP) + min(1.0, max(0.0, ((t % EATP) - 0.55 * EATP) / 0.2))
        d.rectangle([306, 886, 306 + 8 + int(26 * n_), 910], fill=(120, 220, 255, 255))
    layer(img, bar1)
    text_layer(img, [(176, 874, 'LV 1', 44, (200, 230, 255), 7, 255)])
    # ---- divider
    layer(img, lambda d: (d.rectangle([0, DIV0, W, DIV0 + 12], fill=(255, 214, 60, 255)), d.rectangle([0, DIV0 + 12, W, DIV1], fill=(20, 12, 4, 200))))
    # ---- bottom: Day 365
    rev = T_REV <= t < T_DARK + 0.3
    if rev:
        cx, cy = HX2, 1340
        def aura(d):
            for r, a in ((190, 45), (150, 65), (110, 85)):
                rr = r + 10 * math.sin(t * 4 + r)
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 245, 190, a))
        A_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); aura(ImageDraw.Draw(A_))
        A_ = A_.crop((0, DIV1, W, 1500)); img.alpha_composite(A_, (0, DIV1))
        def shad(d):
            for (g, x, y, o) in PARTY + [('hollow', HX2, GFRONT, 2)]:
                d.ellipse([x - 70, y - 12, x + 70, y + 12], fill=(0, 0, 0, 80))
        layer(img, shad)
        for (g, x, y, o) in sorted(PARTY, key=lambda q: q[2]):
            if y == GBACK:
                v = VICS[g][(int(t * 8) + o) % len(VICS[g])]; img.alpha_composite(v, (x - v.width // 2, y - v.height))
        orb = []
        for i, g in enumerate(GUMS2):
            ang = t * 1.6 + i * 2 * math.pi / len(GUMS2); orb.append((math.sin(ang), cx + 150 * math.cos(ang), cy - 40 + 46 * math.sin(ang), g))
        for z, x, y, g in sorted(orb, key=lambda o: o[0]):
            if z < 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        v = VICS['hollow'][int(t * 8) % len(VICS['hollow'])]
        img.alpha_composite(v, (HX2 - v.width // 2, GFRONT - v.height))
        for z, x, y, g in sorted(orb, key=lambda o: o[0]):
            if z >= 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        for (g, x, y, o) in PARTY:
            if y == GFRONT:
                v = VICS[g][(int(t * 8) + o) % len(VICS[g])]; img.alpha_composite(v, (x - v.width // 2, y - v.height))
        ur = t - T_REV
        if ur < 2.2:      # confetti burst on the reveal, falling under gravity
            def conf(d):
                for (x, y0, vy, c) in CONF:
                    y = DIV1 + y0 + vy * ur + 300 * ur * ur
                    if DIV1 < y < 1500: d.rectangle([x, y, x + 12, y + 12], fill=c + (int(255 * min(1, (2.2 - ur) / 0.4)),))
            layer(img, conf)
    # dark cover: on before the reveal, fades out on the reveal (white flash), fades back in at the end for the loop
    if t < T_REV: dk = 1.0
    elif t < T_DARK: dk = 0.0
    else: dk = min(1.0, (t - T_DARK) / 0.2)          # fully dark from 9.9s, so the cut to frame 0 is seamless
    if dk > 0:
        cov = Image.new('RGBA', (W, H - DIV1), (6, 4, 12, int(244 * dk))); img.alpha_composite(cov, (0, DIV1))
        sc = 1 + 0.06 * math.sin(t * 2 * math.pi * 1.2)
        q = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dq = ImageDraw.Draw(q); fz = int(230 * sc)
        tw_ = dq.textlength('?', font=F(fz)); dq.text((540 - tw_ / 2, 1225 - fz / 2), '?', font=F(fz), fill=(255, 230, 150, int(255 * dk)), stroke_width=12, stroke_fill=(30, 18, 6, int(255 * dk)))
        img.alpha_composite(q)
    if 0 <= t - T_REV < 0.45:
        fa = 1 - (t - T_REV) / 0.45; img.alpha_composite(Image.new('RGBA', (W, H - DIV1), (255, 250, 225, int(255 * fa * fa))), (0, DIV1))
    full = T_REV <= t < T_DARK + 0.2                  # back to 'LV ??' + empty bar once dark again (matches frame 0)
    prog = 1.0 if full else (0.0 if t >= T_REV else min(1.0, t / T_REV))
    def bar2(d):
        d.rounded_rectangle([300, 1448, 880, 1492], 14, fill=(30, 20, 5, 220), outline=(255, 214, 60, 255), width=4)
        xe = 308 + int((872 - 308) * prog)
        if xe > 308: d.rectangle([308, 1456, xe, 1484], fill=(255, 196, 40, 255))
        if full:
            sh = int((t * 300) % (880 - 300 - 80)); d.rectangle([308 + sh, 1456, 308 + sh + 60, 1484], fill=(255, 245, 190, 255))
    layer(img, bar2)
    text_layer(img, [(200, 1446, 'LV 99' if full else '', 44, (255, 214, 60), 7, 255), (250, DIV1 + 24, 'DAY 365', 48, (255, 230, 150), 7, 255)])
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(f'p_{f:03d}.png')
    else: w.write(img)
ev = [(round(k * EATP + 0.55 * EATP, 3), 'swish') for k in range(int(DUR / EATP))]   # n13: one swish per eat (old float test doubled some and missed 5.1/7.1)
ev += [(round(T_REV, 3), 'twinkle'), (round(T_REV + 0.05, 3), 'cheer')]
if not PREVIEW: w.close(); json.dump({'events': ev}, open('v27_events.json', 'w')); print('done')
