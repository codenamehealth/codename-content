import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
import numpy as np
# #90 Slimes eat all the glass: safe zone + hook + Bennett note (source fork_b9/v92/render.py):
# slimes stay OFF the glass: they live in the scene BEHIND the glass and eat it from that side, so there is ONE hole that
# starts at the bottom and grows bigger and bigger until the glass is gone (same rule as #32). Glass is near-opaque so the
# artwork only shows through the hole.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 3
BITE = float(os.environ.get('BITE', '2.6'))
rnd = random.Random(SEED)
HOOK, HB = hook_layer(['SLIMES EAT ALL', 'THE GLASS'], accent=1, color=(130, 210, 255))
P0, P1 = HB + 12, HB + 116                     # counter panel under the hook
# ---------------- geometry: arched window (was x150-930, y400-1560)
X0, X1 = 136, 820; CXW = (X0 + X1) // 2; RA = (X1 - X0) // 2; YB = 1446; YR = P1 + 70 + RA
WX0, WY0 = X0, int(YR - RA); WW, WH = X1 - X0, YB - WY0
print('hook', HB, 'panel', P0, P1, 'glass', X0, WY0, X1, YB)
def inside(x, y): return (X0 <= x <= X1 and YR <= y <= YB) or ((x - CXW) ** 2 + (y - YR) ** 2 <= RA ** 2 and y < YR)
CELL = 10; GW, GH = WW // CELL + 1, WH // CELL + 1
INSIDE = np.zeros((GH, GW), bool)
for j in range(GH):
    for i in range(GW): INSIDE[j, i] = inside(WX0 + i * CELL + 5, WY0 + j * CELL + 5)
NTOT = INSIDE.sum()
MASKW = Image.new('L', (WW, WH), 0); md = ImageDraw.Draw(MASKW)
md.rectangle([0, YR - WY0, WW, WH], fill=255); md.ellipse([0, 0, WW, 2 * RA], fill=255)
# ---------------- reveal scene: Cleo at the castle gate (Liza's vit_hd), crop re-cut to the new window aspect
cw = int(1080 * WW / WH); REV = bg_frames('vit_hd.gif', (WW, WH), box=(1254 - cw // 2, 0, 1254 + cw // 2, 1080), step=2)
GROUND = YB - 56
CLEOV = vic('cleo', 380); CLEO_STAND = idle('cleo', 4)          # unchanged sizes
CRE = gummy('cre', 3)
PILE = [(-150, -20), (-100, 5), (130, -10), (175, 10), (-190, 15), (95, 20)]
# ---------------- glass texture: frosted and near-opaque (only the hole shows the scene)
gq = Image.new('RGBA', (WW // 4 + 1, WH // 4 + 1), (196, 222, 242, 252)); gd = ImageDraw.Draw(gq)
for k in range(-40, 80):
    x = k * 22
    gd.polygon([(x, 0), (x + 6, 0), (x + 6 - WH // 4 * 0.55, WH // 4), (x - WH // 4 * 0.55, WH // 4)], fill=(236, 246, 255, 254))
nrnd = random.Random(1)
for _ in range(700):
    x, y = nrnd.randrange(WW // 4), nrnd.randrange(WH // 4); gq.putpixel((x, y), nrnd.choice([(210, 232, 248, 252), (185, 212, 236, 252)]))
GLASS = up(gq, 4).crop((0, 0, WW, WH))
# ---------------- frame (gold + stone band with gummy gems; the old gold gem on top is now creatine)
FRAME = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(FRAME)
def arch_outline(d, pad, col, width):
    d.arc([X0 - pad, YR - RA - pad, X1 + pad, YR + RA + pad], 180, 360, fill=col, width=width)
    d.line([(X0 - pad + width // 2 - 1, YR), (X0 - pad + width // 2 - 1, YB + pad)], fill=col, width=width)
    d.line([(X1 + pad - width // 2, YR), (X1 + pad - width // 2, YB + pad)], fill=col, width=width)
    d.line([(X0 - pad, YB + pad - width // 2), (X1 + pad, YB + pad - width // 2)], fill=col, width=width)
arch_outline(fd, 40, (40, 30, 52, 255), 16); arch_outline(fd, 30, (120, 80, 28, 255), 14); arch_outline(fd, 22, (232, 182, 76, 255), 10)
arch_outline(fd, 15, (255, 226, 130, 255), 4); arch_outline(fd, 8, (120, 80, 28, 255), 8)
for kind, (gx, gy) in zip(['acv', 'cre', 'mush', 'mel', 'cre'], [(X0 - 22, YR + 120), (X1 + 22, YR + 120), (X0 - 22, YB - 80), (X1 + 22, YB - 80), (CXW, YR - RA - 22)]):
    g = gummy(kind, 3); fd.ellipse([gx - 34, gy - 34, gx + 34, gy + 34], fill=(40, 30, 52, 255), outline=(255, 214, 90, 255), width=5)
    FRAME.alpha_composite(g, (gx - g.width // 2, gy - g.height // 2))
# ---------------- wall background (castle stone, full bleed)
wm = json.load(open(PL + 'maze/walls_meta.json'))
wsh = Image.open(PL + 'maze/walls_sheet.png').convert('RGBA'); TL = wm['tileset_data']['tiles']
def tile(b): return up(wsh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)), 2)
BRICK = tile(TL[15]['bounding_box']); TOPT = tile(TL[6]['bounding_box'])
BG = Image.new('RGBA', (W, H), (14, 10, 22, 255))
for y in range(0, H, 64):
    for x in range(0, W, 64): BG.alpha_composite(BRICK if (y // 64 + x // 64) % 5 else TOPT, (x, y))
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (10, 8, 20, 150)))
TORCH = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]   # wall sconces
SL = slime_frames(2)
# ---------------- simulation: one hole, grown only from its rim by slimes on the scene side
S0 = (CXW - 150, GROUND + 10)               # the hole starts at the bottom, where slime #1 sits behind the glass
def cell_of(x, y): return min(GH - 1, max(0, int((y - WY0) // CELL))), min(GW - 1, max(0, int((x - WX0) // CELL)))
def cpos(j, i): return WX0 + i * CELL + 5, WY0 + j * CELL + 5
eaten = np.zeros((GH, GW), bool)
slimes = [dict(x=S0[0], y=S0[1], tx=None, ty=None, born=-1.0, nb=0.8, hop=rnd.uniform(0, 6))]
SPLITS = [2.2, 4.6, 6.8, 9.0, 11.0, 13.0]
events = []; shards = []; frames = []; DUR_MAX = 34
def bite(x, y):
    cj, ci = cell_of(x, y); R = int(BITE); got = 0
    for jj in range(cj - R, cj + R + 1):
        for ii in range(ci - R, ci + R + 1):
            if 0 <= jj < GH and 0 <= ii < GW and INSIDE[jj, ii] and not eaten[jj, ii] and (ii - ci) ** 2 + (jj - cj) ** 2 <= BITE * BITE + 1:
                eaten[jj, ii] = True; got += 1
    return got
def rim_cells():
    e = eaten
    nb = np.zeros_like(e)
    nb[1:, :] |= e[:-1, :]; nb[:-1, :] |= e[1:, :]; nb[:, 1:] |= e[:, :-1]; nb[:, :-1] |= e[:, 1:]
    return np.argwhere(INSIDE & ~e & nb)
last_crunch = -1; t_done = None
for f in range(int(DUR_MAX * FPS)):
    t = f / FPS; dt = 1 / FPS
    if SPLITS and t >= SPLITS[0]:
        SPLITS.pop(0); new = []
        for s in slimes:
            nx, ny = s['x'] + rnd.uniform(-30, 30), s['y'] + rnd.uniform(-20, 20)
            j, i = cell_of(nx, ny)
            if not eaten[j, i]: nx, ny = s['x'], s['y']
            new.append(dict(x=nx, y=ny, tx=None, ty=None, born=t, nb=t + rnd.uniform(0.2, 0.5), hop=rnd.uniform(0, 6)))
        slimes += new; events.append((round(t, 3), 'boing'))
    if t_done is None and t >= 0.8:
        if not eaten.any():
            bite(*S0); slimes[0]['chomp'] = t; slimes[0]['nb'] = t + 0.42; events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
            for _ in range(4): shards.append([S0[0], S0[1] - 20, rnd.uniform(-160, 160), rnd.uniform(-260, -80), t])
        rim = rim_cells()
        for s in slimes:
            if t < s['nb'] or len(rim) == 0: continue
            if s['tx'] is None or eaten[cell_of(s['tx'], s['ty'])]:
                idx = rnd.sample(range(len(rim)), min(50, len(rim)))
                def sc(k):
                    x, y = cpos(*rim[k])
                    return math.hypot(x - S0[0], y - S0[1]) + 0.35 * math.hypot(x - s['x'], y - s['y']) + rnd.uniform(0, 90)
                j, i = rim[min(idx, key=sc)]; s['tx'], s['ty'] = cpos(j, i)
            # stand just inside the hole, next to the glass edge it is eating
            ux, uy = S0[0] - s['tx'], S0[1] - s['ty']; L0 = math.hypot(ux, uy) or 1
            gx_, gy_ = s['tx'] + ux / L0 * 24, s['ty'] + uy / L0 * 24
            dx, dy = gx_ - s['x'], gy_ - s['y']; L = math.hypot(dx, dy) or 1
            if L > 10: s['x'] += dx / L * min(L, 230 * dt); s['y'] += dy / L * min(L, 230 * dt)
            else:
                s['nb'] = t + 0.42
                if bite(s['tx'], s['ty']):
                    s['chomp'] = t
                    for _ in range(3): shards.append([s['tx'], s['ty'], rnd.uniform(-160, 160), rnd.uniform(-260, -80), t])
                    if t - last_crunch > 0.16: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
                s['tx'] = None
                rim = rim_cells()
        left_frac = 1 - eaten[INSIDE].sum() / NTOT
        if left_frac < 0.004: eaten[INSIDE] = True; t_done = t; events.append((round(t, 3), 'victory'))
    left_frac = 1 - eaten[INSIDE].sum() / NTOT
    # connectivity check (one hole): count components occasionally
    frames.append(([dict(x=s['x'], y=s['y'], born=s['born'], chomp=s.get('chomp', -9), hop=s['hop']) for s in slimes], eaten.copy(), max(0.0, left_frac) if t_done is None else 0.0))
    if t_done is not None and t > t_done + 2.9: break
print('done eating at', t_done, 'slimes', len(slimes), 'frames', len(frames))
from scipy import ndimage
ncomp = max(ndimage.label(fr[1])[1] for fr in frames[::15])
print('max holes', ncomp)
if len(sys.argv) > 2 and sys.argv[2] == 'sim': sys.exit()
# ---------------- render
out = Writer('v90_noaudio.mp4'); NF = len(frames)
exits = {k: (rnd.uniform(0, 0.8), rnd.uniform(-300, 300)) for k in range(80)}
SAVE = (int(1.5 * FPS), int(9 * FPS), int(15 * FPS), NF - 20)
for f in range(NF):
    t = f / FPS; sl, em, left = frames[f]
    img = BG.copy()
    for k, tx_ in enumerate((96, W - 210)):
        fr = TORCH[(int(t * 10) + k * 3) % len(TORCH)]; img.alpha_composite(fr, (tx_ - fr.width // 2, 760 - fr.height))
    win = REV[int(t * 6) % len(REV)].copy()
    rv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rv.alpha_composite(win, (WX0, WY0))
    for (px, py) in PILE: rv.alpha_composite(CRE, (CXW + 60 + px - CRE.width // 2, GROUND + 6 + py - CRE.height))
    # slimes (scene side, behind the glass)
    for k, s in enumerate(sorted(sl, key=lambda s: s['y'])):
        fr = SL[int(t * 10 + s['hop'] * 3) % len(SL)]
        age = t - s['born']
        if age < 0.25: k_ = 0.3 + 0.7 * age / 0.25; fr = fr.resize((max(1, int(fr.width * k_)), max(1, int(fr.height * k_))), Image.NEAREST)
        x, y = s['x'], s['y'] - abs(math.sin(t * 7 + s['hop'])) * 8
        if t_done is not None and t > t_done + 0.6:
            dl, vx = exits[k % 80]; u = t - t_done - 0.6 - dl
            if u > 0: x += vx * u; y += -420 * u + 1300 * u * u
        if t - s['chomp'] < 0.12: fr = fr.resize((int(fr.width * 1.15), int(fr.height * 0.88)), Image.NEAREST)
        rv.alpha_composite(fr, (int(x - fr.width / 2), int(y - fr.height + 30 + 26)))
    # Cleo always in front of the slimes (never hidden), behind the glass until it is eaten
    if t_done is not None and t >= t_done:
        cf = CLEOV[int((t - t_done) * 8) % len(CLEOV)]; rv.alpha_composite(cf, (CXW + 60 - cf.width // 2, GROUND + 6 - cf.height))
    else:
        st = CLEO_STAND[int(t * 6) % len(CLEO_STAND)]; rv.alpha_composite(st, (CXW + 60 - st.width // 2, GROUND + 6 - 78 * 4))
    # glass with the one hole
    gm = Image.fromarray((~em).astype(np.uint8) * 255, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST).crop((0, 0, WW, WH))
    gl = GLASS.copy(); a = np.array(gl.getchannel('A')).astype(np.uint16) * np.array(gm).astype(np.uint16) // 255
    gl.putalpha(Image.fromarray(a.astype(np.uint8))); rv.alpha_composite(gl, (WX0, WY0))
    edge = (~em) & (np.roll(em, 1, 0) | np.roll(em, -1, 0) | np.roll(em, 1, 1) | np.roll(em, -1, 1)) & INSIDE
    if edge.any():
        e = Image.fromarray(edge.astype(np.uint8) * 200, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST).crop((0, 0, WW, WH))
        el = Image.new('RGBA', (WW, WH), (255, 255, 255, 0)); el.putalpha(e); rv.alpha_composite(el, (WX0, WY0))
    L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(L2)
    for sx, sy, vx, vy, t0 in shards:
        u = t - t0
        if 0 <= u < 0.6:
            x = sx + vx * u; y = sy + vy * u + 700 * u * u; a = int(230 * (1 - u / 0.6))
            sd.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(225, 240, 255, a))
    rv.alpha_composite(L2)
    mk = Image.new('L', (W, H), 0); mk.paste(MASKW, (WX0, WY0))
    img.paste(rv, (0, 0), Image.composite(rv.getchannel('A'), Image.new('L', (W, H), 0), mk))
    img.alpha_composite(FRAME)
    # counter panel under the hook
    layer(img, lambda d: d.rounded_rectangle([78, P0, 1017, P1], 18, fill=(10, 8, 20, 225), outline=(232, 182, 76, 255), width=4))
    if t_done is not None and t >= t_done:
        u = t - t_done; sc_ = min(1.0, u / 0.25)
        text_layer(img, [(547, (P0 + P1) / 2 - int(64 * (0.6 + 0.4 * sc_)) / 2, 'ALL GONE!', int(64 * (0.6 + 0.4 * sc_)), (255, 214, 60), 8, 255)])
    else:
        text_layer(img, [(547, P0 + 14, f'GLASS LEFT: {int(math.ceil(left * 100)) if left > 0 else 0}%', 36, (225, 240, 255), 6, 255),
                         (547, P0 + 62, f'SLIMES: {len(sl)}', 30, (150, 235, 110), 5, 255)])
    img.alpha_composite(HOOK)
    out.write(img)
    if f in SAVE: img.convert('RGB').save(f'f90_{f}.png')
out.close()
json.dump(events, open('v90_ev.json', 'w')); print('rendered', NF / FPS)
mix('v90_noaudio.mp4', events, 'chiptune_gameboy.wav', 4, 'v90_mix.mp4')
print('LUFS', loudness('v90_mix.mp4'), '->', louder('v90_mix.mp4', 'v90_final.mp4'))
