import sys
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP_ + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
DUR = 10.0; NF = int(DUR * FPS)
HOOK, HB = hook_layer2(['+1 XP A DAY'], accent=0, sub='WHAT DAY ARE YOU ON?')
print('hook bottom', HB)
TOPB = bg_frames('found_hd.gif', (1707, 960), step=2, bright=0.8); TOPB = [b.crop((420, 0, 1500, 960)) for b in TOPB]
BOTB = bg_frames('sun_hd.gif', (1707, 960), step=2); BOTB = [b.crop((313, 0, 1393, 960)) for b in BOTB]
EAT = seq(SP_ + 'fork3/hollow_eat', 4, 0, 13); FOOT3 = 78 * 4          # Day 1 Hollow 3x -> 4x
VICT = vic('hollow', 384)
GUMS = [up(acv_gummy_strong(), 3) if k == 'acv' else gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']]
SMALLG = gummy('mush', 3)
DIV0, DIV1 = 944, 1012           # divider band
BOFF = 1430 - 725                # bottom bg offset so the Hollow's ground sits at y1430
w = None if PREVIEW else Writer('v27_noaudio.mp4'); ev = []
rs = random.Random(5); LINES = [(rs.uniform(0, 1), rs.uniform(-150, 40), rs.choice((-1, 1)), rs.uniform(60, 150)) for _ in range(14)]
EATP = 2.0
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
        items.append((hx - 250, int(hy - 230), 'SPEED!', int(52 * sc), (255, 160, 40), 9, a))
        if pop < 1 / FPS: ev.append((round(t, 3), 'swish'))
    text_layer(img, items)
    def bar1(d):
        d.rounded_rectangle([300, 880, 940, 916], 12, fill=(15, 15, 30, 220), outline=(120, 200, 255, 255), width=3)
        d.rectangle([306, 886, 306 + 6 + 3 * (int(t / EATP) % 3), 910], fill=(120, 220, 255, 255))
    layer(img, bar1)
    text_layer(img, [(176, 874, 'LV 1', 44, (200, 230, 255), 7, 255)])
    # ---- divider
    layer(img, lambda d: (d.rectangle([0, DIV0, W, DIV0 + 12], fill=(255, 214, 60, 255)), d.rectangle([0, DIV0 + 12, W, DIV1], fill=(20, 12, 4, 200))))
    text_layer(img, [(W / 2, DIV0 + 22, '1 YEAR LATER', 44, (255, 214, 60), 6, 255)])
    # ---- bottom: level 99
    cx, cy = 540, 1250
    def aura(d):
        for r, a in ((230, 55), (180, 75), (130, 95)):
            rr = r + 12 * math.sin(t * 4 + r)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 245, 190, a))
        for i in range(14):
            ang = t * 1.5 + i * 0.449; rr = 270 + 20 * math.sin(t * 3 + i)
            sx, sy = cx + rr * math.cos(ang), cy + rr * 0.45 * math.sin(ang)
            d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 250, 200, 220))
    A_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); aura(ImageDraw.Draw(A_))
    A_ = A_.crop((0, DIV1, W, 1500)); img.alpha_composite(A_, (0, DIV1))
    orb = []
    for i, g in enumerate(GUMS):
        ang = t * 1.2 + i * 2 * math.pi / 5; orb.append((math.sin(ang), cx + 290 * math.cos(ang), cy - 20 + 100 * math.sin(ang), g))
    for z, x, y, g in sorted(orb, key=lambda o: o[0]):
        if z < 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    v = VICT[int(t * 8) % len(VICT)]
    img.alpha_composite(v, (cx - v.width // 2, 1430 - v.height))
    for z, x, y, g in sorted(orb, key=lambda o: o[0]):
        if z >= 0: img.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    def bar2(d):
        d.rounded_rectangle([300, 1448, 880, 1492], 14, fill=(30, 20, 5, 220), outline=(255, 214, 60, 255), width=4)
        sh = int((t * 300) % (880 - 300 - 80))
        d.rectangle([308, 1456, 872, 1484], fill=(255, 196, 40, 255)); d.rectangle([308 + sh, 1456, 308 + sh + 60, 1484], fill=(255, 245, 190, 255))
    layer(img, bar2)
    text_layer(img, [(200, 1446, 'LV 99', 44, (255, 214, 60), 7, 255), (250, DIV1 + 16, 'DAY 365', 48, (255, 230, 150), 7, 255)])
    if 0.2 <= t < 1.4:      # Syeda's ACV gummy: name it on first appearance so it reads as a gummy, not an apple
        z, x, y, g = orb[1]; a = int(255 * min(1, (t - 0.2) / 0.12, (1.4 - t) / 0.15))
        tx = min(max(x, 70 + 210), 887 - 210); ty = y - 110
        layer(img, lambda d: d.rounded_rectangle([tx - 206, ty - 8, tx + 206, ty + 56], 14, fill=(14, 10, 24, int(220 * a / 255)), outline=(120, 230, 80, a), width=4))
        text_layer(img, [(tx, ty, 'ACV GUMMY', 44, (140, 240, 100), 6, a)])
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(f'p_{f:03d}.png')
    else: w.write(img)
if not PREVIEW: w.close(); json.dump({'events': ev}, open('v27_events.json', 'w')); print('done')
