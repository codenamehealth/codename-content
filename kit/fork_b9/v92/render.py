import sys; sys.path.insert(0, '../../fork_a7')
from common7 import *
import numpy as np
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 3
rnd = random.Random(SEED)
# ---------------- geometry: arched window
X0, X1, YR, YB, CXW = 150, 930, 790, 1560, 540; RA = (X1 - X0) // 2
WX0, WY0 = X0, int(YR - RA); WW, WH = X1 - X0, YB - WY0
def inside(x, y): return (X0 <= x <= X1 and YR <= y <= YB) or ((x - CXW) ** 2 + (y - YR) ** 2 <= RA ** 2 and y < YR)
CELL = 10; GW, GH = WW // CELL, WH // CELL
INSIDE = np.zeros((GH, GW), bool)
for j in range(GH):
    for i in range(GW): INSIDE[j, i] = inside(WX0 + i * CELL + 5, WY0 + j * CELL + 5)
NTOT = INSIDE.sum()
MASKW = Image.new('L', (WW, WH), 0); md = ImageDraw.Draw(MASKW)
md.rectangle([0, YR - WY0, WW, WH], fill=255); md.ellipse([0, 0, WW, 2 * RA], fill=255)
# ---------------- reveal scene: Cleo at the castle gate (Liza's vit_hd)
REV = bg_frames('vit_hd.gif', (WW, WH), box=(900, 0, 1608, 1080), step=2)
CLEOV = vic('cleo', 380); CLEO_STAND = idle('cleo', 4)
CRE = gummy('cre', 3)
PILE = [(-150, 1470), (-100, 1495), (130, 1480), (175, 1500), (-190, 1505), (95, 1510)]
# ---------------- glass texture (drawn at 1/4 res then upscaled for pixel look)
gq = Image.new('RGBA', (WW // 4, WH // 4), (196, 222, 242, 228)); gd = ImageDraw.Draw(gq)
for k in range(-40, 80):
    x = k * 22
    gd.polygon([(x, 0), (x + 6, 0), (x + 6 - WH // 4 * 0.55, WH // 4), (x - WH // 4 * 0.55, WH // 4)], fill=(236, 246, 255, 242))
nrnd = random.Random(1)
for _ in range(900):
    x, y = nrnd.randrange(WW // 4), nrnd.randrange(WH // 4); c = nrnd.choice([(210, 232, 248, 220), (185, 212, 236, 215)]); gq.putpixel((x, y), c)
GLASS = up(gq, 4)
# ---------------- frame (procedural gold + stone band with gummy gems)
FRAME = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(FRAME)
def arch_outline(d, pad, col, width):
    d.arc([X0 - pad, YR - RA - pad, X1 + pad, YR + RA + pad], 180, 360, fill=col, width=width)
    d.line([(X0 - pad + width // 2 - 1, YR), (X0 - pad + width // 2 - 1, YB + pad)], fill=col, width=width)
    d.line([(X1 + pad - width // 2, YR), (X1 + pad - width // 2, YB + pad)], fill=col, width=width)
    d.line([(X0 - pad, YB + pad - width // 2), (X1 + pad, YB + pad - width // 2)], fill=col, width=width)
arch_outline(fd, 40, (40, 30, 52, 255), 16)
arch_outline(fd, 30, (120, 80, 28, 255), 14)
arch_outline(fd, 22, (232, 182, 76, 255), 10)
arch_outline(fd, 15, (255, 226, 130, 255), 4)
arch_outline(fd, 8, (120, 80, 28, 255), 8)
for kind, (gx, gy) in zip(['acv', 'cre', 'mush', 'mel', 'gold'], [(X0 - 22, YR + 200), (X1 + 22, YR + 200), (X0 - 22, YB - 80), (X1 + 22, YB - 80), (CXW, YR - RA - 22)]):
    g = gummy(kind, 3); fd.ellipse([gx - 34, gy - 34, gx + 34, gy + 34], fill=(40, 30, 52, 255), outline=(255, 214, 90, 255), width=5)
    FRAME.alpha_composite(g, (gx - g.width // 2, gy - g.height // 2))
# ---------------- wall background (castle stone)
wm = json.load(open(PL + 'maze/walls_meta.json'))
wsh = Image.open(PL + 'maze/walls_sheet.png').convert('RGBA'); TL = wm['tileset_data']['tiles']
def tile(b): return up(wsh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)), 2)
BRICK = tile(TL[15]['bounding_box']); TOPT = tile(TL[6]['bounding_box'])
BG = Image.new('RGBA', (W, H), (14, 10, 22, 255))
for y in range(0, H, 64):
    for x in range(0, W, 64): BG.alpha_composite(BRICK if (y // 64 + x // 64) % 5 else TOPT, (x, y))
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (10, 8, 20, 150)))
TORCH = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]
SL = slime_frames(2)
# ---------------- simulation
T_END_EAT = None; FPS_ = FPS
eaten = np.zeros((GH, GW), bool)
slimes = [dict(x=CXW, y=1180, tx=None, ty=None, ph=0.0, born=0.6, nb=0.0, hop=rnd.uniform(0, 6))]
SPLITS = [2.2, 4.6, 6.8, 9.0, 11.0, 13.0]
events = []; shards = []
DUR_MAX = 30
frames = []
def nearest_glass(x, y):
    left = np.argwhere(INSIDE & ~eaten)
    if len(left) == 0: return None
    idx = rnd.sample(range(len(left)), min(40, len(left)))
    best = min(idx, key=lambda k: (WX0 + left[k][1] * CELL - x) ** 2 + (WY0 + left[k][0] * CELL - y) ** 2 + rnd.uniform(0, 4000))
    j, i = left[best]; return WX0 + i * CELL + 5, WY0 + j * CELL + 5
last_crunch = -1; t_done = None
for f in range(int(DUR_MAX * FPS)):
    t = f / FPS; dt = 1 / FPS
    if SPLITS and t >= SPLITS[0]:
        SPLITS.pop(0); new = []
        for s in slimes:
            a = rnd.uniform(0, 6.28); nx, ny = s['x'] + 40 * math.cos(a), s['y'] + 30 * math.sin(a)
            if not inside(nx, ny): nx, ny = s['x'], s['y']
            new.append(dict(x=nx, y=ny, tx=None, ty=None, ph=0.0, born=t, nb=t + rnd.uniform(0.2, 0.5), hop=rnd.uniform(0, 6)))
        slimes += new; events.append((round(t, 3), 'boing'))
    left_frac = 1 - eaten[INSIDE].sum() / NTOT
    if t_done is None and t > 1.0:
        for s in slimes:
            if t < s['nb']: continue
            if s['tx'] is None or eaten[min(GH - 1, max(0, int((s['ty'] - WY0) // CELL))), min(GW - 1, max(0, int((s['tx'] - WX0) // CELL)))]:
                g = nearest_glass(s['x'], s['y'])
                if g is None: break
                s['tx'], s['ty'] = g
            dx, dy = s['tx'] - s['x'], s['ty'] - s['y']; L = math.hypot(dx, dy) or 1
            sp = 210
            if L > 12: s['x'] += dx / L * min(L, sp * dt); s['y'] += dy / L * min(L, sp * dt)
            else:
                s['nb'] = t + 0.42; R = 3
                ci, cj = int((s['x'] - WX0) // CELL), int((s['y'] - WY0) // CELL)
                got = 0
                for jj in range(cj - R, cj + R + 1):
                    for ii in range(ci - R, ci + R + 1):
                        if 0 <= jj < GH and 0 <= ii < GW and INSIDE[jj, ii] and not eaten[jj, ii] and (ii - ci) ** 2 + (jj - cj) ** 2 <= R * R + 1:
                            eaten[jj, ii] = True; got += 1
                if got:
                    s['chomp'] = t
                    for _ in range(3): shards.append([s['x'], s['y'] - 20, rnd.uniform(-160, 160), rnd.uniform(-260, -80), t])
                    if t - last_crunch > 0.16: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
                s['tx'] = None
        left_frac = 1 - eaten[INSIDE].sum() / NTOT
        if left_frac < 0.004: eaten[INSIDE] = True; t_done = t; events.append((round(t, 3), 'victory'))
    frames.append(([dict(x=s['x'], y=s['y'], born=s['born'], chomp=s.get('chomp', -9), hop=s['hop']) for s in slimes], eaten.copy(), max(0.0, left_frac) if t_done is None else 0.0))
    if t_done is not None and t > t_done + 2.8: break
print('done eating at', t_done, 'slimes', len(slimes), 'frames', len(frames))
if len(sys.argv) > 2 and sys.argv[2] == 'sim': sys.exit()
# ---------------- render
out = Writer('v92_noaudio.mp4'); NF = len(frames)
exits = {k: (rnd.uniform(0, 0.8), rnd.uniform(-300, 300)) for k in range(80)}
for f in range(NF):
    t = f / FPS; sl, em, left = frames[f]
    img = BG.copy()
    for k, (tx_, ty_) in enumerate([(70, 900), (1010, 900)]):
        fr = TORCH[(int(t * 10) + k * 3) % len(TORCH)]; img.alpha_composite(fr, (tx_ - fr.width // 2, ty_ - fr.height))
    # window content
    win = REV[int(t * 6) % len(REV)].copy()
    rv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rv.alpha_composite(win, (WX0, WY0))
    for (px, py) in PILE: rv.alpha_composite(CRE, (CXW + px - CRE.width // 2, py - CRE.height))
    if t_done is not None and t >= t_done:
        cf = CLEOV[int((t - t_done) * 8) % len(CLEOV)]
    else:
        cf = None
    if cf is None:
        st = CLEO_STAND[int(t * 6) % len(CLEO_STAND)]; rv.alpha_composite(st, (CXW - st.width // 2, 1490 - 78 * 4))
    else: rv.alpha_composite(cf, (CXW - cf.width // 2, 1490 - cf.height))
    # glass with eaten holes
    gm = Image.fromarray((~em).astype(np.uint8) * 255, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST)
    gmask = Image.new('L', (WW, WH), 0); gmask.paste(gm, (0, 0))
    gl = GLASS.copy(); a = np.array(gl.getchannel('A')).astype(np.uint16) * np.array(gmask).astype(np.uint16) // 255
    gl.putalpha(Image.fromarray(a.astype(np.uint8)))
    rv.alpha_composite(gl, (WX0, WY0))
    # bright rim on glass edges
    edge = (~em) & (np.roll(em, 1, 0) | np.roll(em, -1, 0) | np.roll(em, 1, 1) | np.roll(em, -1, 1)) & INSIDE
    if edge.any():
        e = Image.fromarray(edge.astype(np.uint8) * 160, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST)
        em_l = Image.new('RGBA', (WW, WH), (255, 255, 255, 0)); em_l.putalpha(Image.new('L', (WW, WH), 0)); tmp = Image.new('L', (WW, WH), 0); tmp.paste(e, (0, 0))
        em_l.putalpha(tmp); rv.alpha_composite(em_l, (WX0, WY0))
    # slimes
    for k, s in enumerate(sorted(sl, key=lambda s: s['y'])):
        fr = SL[int(t * 10 + s['hop'] * 3) % len(SL)]
        age = t - s['born']
        if age < 0.25: k_ = 0.3 + 0.7 * age / 0.25; fr = fr.resize((max(1, int(fr.width * k_)), max(1, int(fr.height * k_))), Image.NEAREST)
        x, y = s['x'], s['y'] - abs(math.sin(t * 7 + s['hop'])) * 10
        if t_done is not None and t > t_done + 0.6:
            dl, vx = exits[k % 80]; u = t - t_done - 0.6 - dl
            if u > 0: x += vx * u; y += -420 * u + 1300 * u * u
        if t - s['chomp'] < 0.12: fr = fr.resize((int(fr.width * 1.15), int(fr.height * 0.88)), Image.NEAREST)
        rv.alpha_composite(fr, (int(x - fr.width / 2), int(y - fr.height + 30)))
    # shards
    L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(L2)
    for sx, sy, vx, vy, t0 in shards:
        u = t - t0
        if 0 <= u < 0.6:
            x = sx + vx * u; y = sy + vy * u + 700 * u * u; a = int(230 * (1 - u / 0.6))
            sd.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(225, 240, 255, a))
    rv.alpha_composite(L2)
    mk = Image.new('L', (W, H), 0); mk.paste(MASKW, (WX0, WY0))
    img.paste(rv, (0, 0), Image.composite(rv.getchannel('A'), Image.new('L', (W, H), 0), mk))
    # escaping slimes can leave the window: draw those outside the mask on top
    img.alpha_composite(FRAME)
    # header + counters
    layer(img, lambda d: d.rectangle([0, 0, W, 300], fill=(10, 8, 20, 170)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 70, 'SLIMES EAT ALL', F(66)); ctext(d, W / 2, 160, 'THE GLASS', F(66), (130, 210, 255))
    layer(img, lambda d: d.rounded_rectangle([170, 1640, 910, 1810], 18, fill=(10, 8, 20, 200)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([170, 1640, 910, 1810], 18, outline=(232, 182, 76), width=4)
    ctext(d, W / 2, 1668, f'GLASS LEFT: {int(math.ceil(left * 100)) if left > 0 else 0}%', F(40), (225, 240, 255), 5)
    ns = len(sl) if (t_done is None or t < t_done + 0.6) else len(sl)
    ctext(d, W / 2, 1740, f'SLIMES: {ns}', F(32), (150, 235, 110), 5)
    if t_done is not None and t >= t_done:
        u = t - t_done; sc = min(1.0, u / 0.25)
        text_layer(img, [(W / 2, 560, 'ALL GONE!', int(76 * (0.6 + 0.4 * sc)), (255, 214, 60), 9, 255)])
    out.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close()
json.dump(events, open('ev.json', 'w')); print('rendered', NF / FPS)
