import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
OUT = SP + 'fork_a10/v98/'; G = SP + 'fork_a10/gen/'
rng = random.Random(7)
TS = 96; COLS = 12
WORLD_H = 6400
SURF = 520                     # grass line in world coords
B1, B2, B3 = 2000, 3400, 4900  # soil->stone, stone->purple, purple->magma
CH_Y = 5650                    # chamber floor centre
soil = wang(G + 'soil_meta.json', G + 'soil_sheet.png'); deep = wang(G + 'deep_meta.json', G + 'deep_sheet.png')
def tile(T, key): return up(T[key], 3)
rows = WORLD_H // TS + 2
def low_soil(i, j):
    y = SURF + j * TS; return y + 60 * math.sin(i * 1.3 + j * 0.7) < B1
def low_deep(i, j):
    y = SURF + j * TS; return y + 60 * math.sin(i * 1.1 + j * 0.9) < B3
WORLD = Image.new('RGBA', (W, WORLD_H), (20, 14, 12, 255))
for j in range(rows):
    y = SURF + j * TS
    for i in range(COLS):
        x = i * TS - 36
        if y + TS <= B2 + 40:
            key = (low_soil(i, j), low_soil(i + 1, j), low_soil(i, j + 1), low_soil(i + 1, j + 1)); T = soil
        else:
            key = (low_deep(i, j), low_deep(i + 1, j), low_deep(i, j + 1), low_deep(i + 1, j + 1)); T = deep
        tl = tile(T, key)
        if all(key) or not any(key):
            if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
            if (i * 3 + j) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        WORLD.alpha_composite(tl, (x, y))
wd = ImageDraw.Draw(WORLD)
# seam between stone and purple rock
for x in range(0, W, 8):
    yy = B2 + 40 + int(10 * math.sin(x * 0.03))
    wd.rectangle([x, yy - 6, x + 8, yy + 4], fill=(30, 22, 34, 255))
# surface: Liza forest strip
fb = bg_frames('found_hd.gif', (W, 520), box=(0, 150, 1920, 1074), step=4, bright=0.95)
# grass lip
# decor items buried
def pick(name, i, k): return up(crop(Image.open(G + f'{name}/{i:02d}.png').convert('RGBA')), k)
FOS, COIN, ROOT = pick('fossil', 3, 4), pick('coins', 4, 3), pick('root', 1, 4)
CRY = up(crop(Image.open(SP + 'fork_a7/gen/crystal/01.png').convert('RGBA')), 3)
GK = ['mush', 'acv', 'mel', 'cre', 'gold']
deco = []
for k in range(5): deco.append((ROOT, 80 + k * 230 + rng.uniform(-40, 40), SURF + 120 + rng.uniform(0, 160)))
for k in range(26):
    y = rng.uniform(SURF + 400, CH_Y - 500); x = rng.uniform(60, W - 60)
    if y < B1: im = rng.choice([FOS, COIN, gummy(rng.choice(GK), 3), ROOT])
    elif y < B2: im = rng.choice([FOS, COIN, gummy(rng.choice(GK), 3)])
    else: im = rng.choice([CRY, COIN, gummy(rng.choice(GK), 3), CRY])
    deco.append((im, x, y))
for im, x, y in deco: WORLD.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
# chamber
CX = [190, 540, 890]
def cave(d):
    d.rounded_rectangle([20, CH_Y - 330, W - 20, CH_Y + 170], 90, fill=(16, 10, 20, 255))
    for x in CX: d.ellipse([x - 165, CH_Y - 300, x + 165, CH_Y + 140], fill=(36, 24, 44, 255))
wd = ImageDraw.Draw(WORLD); cave(wd)
for x in CX:
    wd.ellipse([x - 150, CH_Y + 70, x + 150, CH_Y + 130], fill=(10, 6, 12, 255))
# prizes (hidden mapping): chamber 0 treasure, 1 slimed, 2 charm
chest = up(crop(Image.open(sorted(glob.glob(SP + 'fork_b5/chest_open/*.png'))[-1]).convert('RGBA')), 4)
SLIME = slime_frames(5)
JAR = up(Image.open(A + 'jar_mushroom.png').convert('RGBA').resize((54, 54), Image.NEAREST), 5)
GOLD = gummy('gold', 4)
PERM = [2, 0, 1]   # guide i -> chamber PERM[i] (never stated)
NAMES = ['joy', 'cyrus', 'cleo']; COL = {'joy': (110, 210, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255)}
SX = [230, 540, 850]
def path_x(i, y):
    u = (y - SURF) / (CH_Y - 220 - SURF); u = min(max(u, 0), 1)
    e = u * u * (3 - 2 * u)
    base = SX[i] + (CX[PERM[i]] - SX[i]) * e
    amp = 330 * math.sin(math.pi * u) ** 0.8
    return base + amp * (math.sin(u * 9.0 + i * 2.1) * 0.75 + 0.35 * math.sin(u * 17 + i * 4.0))
def clampx(x): return min(max(x, 90), W - 90)
PATH = [[(clampx(path_x(i, y)), y) for y in range(SURF, CH_Y - 200, 6)] for i in range(3)]
DRILL = pick('drill', 2, 3)
STAND = {g: idle(g, 3) for g in NAMES}
# timeline
T_GO = 2.6; T_DIG = 11.0; T_END = T_GO + T_DIG + 0.6; END = T_END + 3.4
DIG_LEN = CH_Y - 200 - SURF
def dig_y(t): 
    if t < T_GO: return SURF
    u = min(1, (t - T_GO) / T_DIG); return SURF + DIG_LEN * (u * 0.9 + 0.1 * u * u)
HEAD = 360
def cam_y(t):
    if t >= T_GO + T_DIG: 
        u = min(1, (t - T_GO - T_DIG) / 0.8); target = CH_Y - 1150
        prev = min(max(dig_y(T_GO + T_DIG) - 1000, 0), WORLD_H - (H - HEAD)); return prev + (target - prev) * u * u * (3 - 2 * u)
    return min(max(dig_y(t) - 1000, 0), WORLD_H - (H - HEAD))
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS)
for f in range(NF):
    t = f / FPS; cy = int(cam_y(t)); dy = dig_y(t)
    view = WORLD.crop((0, cy, W, cy + H - HEAD)).copy()
    # surface scene
    if cy < SURF:
        s = fb[int(t * 6) % len(fb)]; view.alpha_composite(s, (0, SURF - 520 - cy))
        vd = ImageDraw.Draw(view)
        for x in range(0, W, 12): vd.rectangle([x, SURF - cy - 6, x + 12, SURF - cy + 6 + (x // 12) % 2 * 4], fill=(70, 150, 50, 255))
    # tunnels
    def tun(d):
        for i in range(3):
            pts = [(x, y - cy) for x, y in PATH[i] if y <= dy]
            if len(pts) > 1:
                d.line(pts, fill=COL[NAMES[i]] + (255,), width=84, joint='curve')
        for i in range(3):
            pts = [(x, y - cy) for x, y in PATH[i] if y <= dy]
            if len(pts) > 1:
                d.line(pts, fill=(28, 18, 16, 255), width=66, joint='curve')
                for p in pts[::1]: pass
    layer(view, tun)
    # drill heads + dust
    for i in range(3):
        if t >= T_GO and dy < CH_Y - 205:
            k = min(len(PATH[i]) - 1, int((dy - SURF) / 6)); x, y = PATH[i][k]
            x2, y2 = PATH[i][min(k + 3, len(PATH[i]) - 1)]; ang = math.degrees(math.atan2(x2 - x, y2 - y))
            dr = DRILL.rotate(ang + (6 * math.sin(t * 50)), expand=True, resample=Image.NEAREST)
            def glow(d, x=x, y=y, i=i): d.ellipse([x - 70, y - cy - 70, x + 70, y - cy + 70], fill=COL[NAMES[i]] + (80,))
            layer(view, glow)
            view.alpha_composite(dr, (int(x - dr.width / 2), int(y - cy - dr.height / 2)))
            def dust(d, x=x, y=y):
                rr = random.Random(f * 7 + i)
                for _ in range(10):
                    a = rr.uniform(0, 6.28); r = rr.uniform(20, 70)
                    d.rectangle([x + r * math.cos(a) - 5, y - cy + r * math.sin(a) - 5, x + r * math.cos(a) + 5, y - cy + r * math.sin(a) + 5], fill=(150, 110, 80, 200))
            layer(view, dust)
    # guides at the surface
    for i, g in enumerate(NAMES):
        if cy < SURF + 40:
            fr = STAND[g][int(t * 8) % len(STAND[g])]
            view.alpha_composite(fr, (int(SX[i] - fr.width / 2), int(SURF - cy - 78 * 3 - 4)))
            if t < T_GO: text_layer(view, [(SX[i], SURF - cy - 300, g.upper(), 26, COL[g], 5, 255)])
    # prizes
    if cy + H - HEAD > CH_Y - 400:
        for c in range(3):
            x = CX[c]; yb = CH_Y + 90 - cy
            if c == 0:
                view.alpha_composite(chest, (x - chest.width // 2, yb - chest.height))
                view.alpha_composite(GOLD, (x - GOLD.width // 2, yb - chest.height - GOLD.height + 30 + int(6 * math.sin(t * 5))))
                for k in range(3): view.alpha_composite(COIN, (x - 140 + k * 90, yb - COIN.height + 10))
            elif c == 1:
                fr = SLIME[int(t * 8) % len(SLIME)]; view.alpha_composite(fr, (x - fr.width // 2, yb - fr.height + 10))
            else:
                view.alpha_composite(JAR, (x - JAR.width // 2, yb - JAR.height + 10))
            lab = ['TREASURE', 'SLIMED', 'CHARM'][c]
            text_layer(view, [(x, yb + 40, lab, 30, (255, 214, 60) if c == 0 else (150, 240, 120) if c == 1 else (255, 170, 80), 5, 255)])
    img = Image.new('RGBA', (W, H), (10, 8, 16, 255)); img.alpha_composite(view, (0, HEAD))
    # header
    def hdr(d): d.rectangle([0, 0, W, HEAD], fill=(18, 12, 26, 255)); d.rectangle([0, HEAD - 8, W, HEAD], fill=(120, 80, 50, 255))
    layer(img, hdr)
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 70, 'CHOOSE YOUR', F(56)); ctext(d, W / 2, 150, 'DIGGER!', F(72), (255, 190, 80), 7)
    ctext(d, W / 2, 262, 'Who digs up the treasure?', F(30), (255, 255, 255), 5)
    if t >= T_GO and t < T_GO + T_DIG + 0.3:
        depth = int((dy - SURF) / 6)
        text_layer(img, [(W - 150, HEAD + 30, f'{depth}m', 40, (255, 255, 255), 6, 255)])
    if 0.4 <= t < T_GO + 0.5:
        u = t - 0.4; n = ['3', '2', '1', 'DIG!'][min(3, int(u / 0.55))]; a = 255 if t < T_GO + 0.2 else int(255 * (T_GO + 0.5 - t) / 0.3)
        text_layer(img, [(W / 2, 1100, n, 120 if len(n) == 1 else 100, (255, 255, 255) if len(n) == 1 else (255, 214, 60), 10, a)])
        if abs(u % 0.55) < 0.5 / FPS and u < 2.2: ev.append((round(t, 3), 'tick_8bit' if u < 1.6 else 'go_8bit'))
    if t >= T_GO and t < T_GO + T_DIG and int(t * 30) % 12 == 0: ev.append((round(t, 3), 'crunch_8bit'))
    if abs(t - (T_GO + T_DIG)) < 0.5 / FPS: ev.append((round(t, 3), 'boom'))
    if t >= T_END:
        u = t - T_END; a = int(255 * min(1, u / 0.3))
        text_layer(img, [(W / 2, 980, 'WHAT DID YOU DIG UP?', 50, (255, 214, 60), 8, a), (W / 2, 1065, 'Follow your tunnel. Comment your prize', 26, (255, 255, 255), 5, a)])
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'chime'))
    w.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
