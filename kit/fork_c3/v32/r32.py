import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
# #32 The Hollow eats all the glass: content pass (Bennett): the Hollows never stand on the glass. They live in the picture BEHIND
# the glass and eat it from that side, so there is exactly ONE hole that starts in the middle and grows into a bigger and bigger
# circle until the glass is gone (same rule as the approved #90). Glass is near-opaque so the artwork only shows through the hole.
# Source: fork_sz32/v32/r32s.py (safe zone + hook version).
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
CX, CY, RAD = 490, 1010, 336                       # porthole (unchanged from the safe-zone version)
PX0, PY0 = CX - RAD, CY - RAD
CELL = 8; GN = 2 * RAD // CELL
yy, xx = np.mgrid[0:GN, 0:GN]; INC = ((xx + 0.5 - GN / 2) ** 2 + (yy + 0.5 - GN / 2) ** 2) <= (GN / 2 - 0.3) ** 2
NTOT = INC.sum()
S0 = (CX, CY + 30)                                 # the hole starts here (middle of the picture) and grows outward
BITE = float(os.environ.get('BITE', '2.2')); BINT = float(os.environ.get('BINT', '0.42')); SPD = 230
SPLITS = [2.4, 4.8, 7.2, 9.6, 12.0, 14.4]          # 1 -> 64 Hollows (same doubling as before)
T_FIRST = 0.45                                     # first bite (cracks + tremble before it, so frame 0 already moves)
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def cell_of(x, y): return min(GN - 1, max(0, int((y - PY0) // CELL))), min(GN - 1, max(0, int((x - PX0) // CELL)))
def cpos(j, i): return PX0 + i * CELL + CELL / 2, PY0 + j * CELL + CELL / 2
eaten = np.zeros((GN, GN), bool)
hol = [dict(x=S0[0], y=S0[1] + 60, tx=None, ty=None, born=-1.0, nb=T_FIRST, ph=rnd.uniform(0, 6), chomp=-9, face=1)]
def bite(x, y):
    cj, ci = cell_of(x, y); r = int(BITE) + 1; got = 0
    for jj in range(cj - r, cj + r + 1):
        for ii in range(ci - r, ci + r + 1):
            if 0 <= jj < GN and 0 <= ii < GN and INC[jj, ii] and not eaten[jj, ii] and (ii - ci) ** 2 + (jj - cj) ** 2 <= BITE * BITE + 1:
                eaten[jj, ii] = True; got += 1
    return got
def rim_cells():
    e = eaten; nb = np.zeros_like(e)
    nb[1:, :] |= e[:-1, :]; nb[:-1, :] |= e[1:, :]; nb[:, 1:] |= e[:, :-1]; nb[:, :-1] |= e[:, 1:]
    return np.argwhere(INC & ~e & nb)
events = [(0.0, 'tick_8bit'), (0.2, 'tick_8bit')]; shards = []; frames = []; t_done = None; last_crunch = -1
for f in range(40 * FPS):
    t = f / FPS; dt = 1 / FPS
    if SPLITS and t >= SPLITS[0]:
        SPLITS.pop(0); new = []
        for h in hol:
            nx, ny = h['x'] + rnd.uniform(-30, 30), h['y'] + rnd.uniform(-20, 20)
            if not eaten[cell_of(nx, ny)]: nx, ny = h['x'], h['y']
            new.append(dict(x=nx, y=ny, tx=None, ty=None, born=t, nb=t + rnd.uniform(0.2, 0.5), ph=rnd.uniform(0, 6), chomp=-9, face=-h['face']))
        hol += new; events.append((round(t, 3), 'poof'))
    if t_done is None and t >= T_FIRST:
        if not eaten.any():
            bite(*S0); hol[0]['chomp'] = t; hol[0]['nb'] = t + BINT; events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
            for _ in range(6): shards.append([S0[0], S0[1], rnd.uniform(-200, 200), rnd.uniform(-300, -80), t])
        rim = rim_cells()
        for h in hol:
            if t < h['nb'] or len(rim) == 0: continue
            if h['tx'] is None or eaten[cell_of(h['tx'], h['ty'])]:
                idx = rnd.sample(range(len(rim)), min(50, len(rim)))
                def sc(k):
                    x, y = cpos(*rim[k])
                    return math.hypot(x - S0[0], y - S0[1]) + 0.35 * math.hypot(x - h['x'], y - h['y']) + rnd.uniform(0, 60)
                j, i = rim[min(idx, key=sc)]; h['tx'], h['ty'] = cpos(j, i)
            # stand just inside the hole, mouth at the glass edge it is eating
            ux, uy = S0[0] - h['tx'], S0[1] - h['ty']; L0 = math.hypot(ux, uy) or 1
            gx_, gy_ = h['tx'] + ux / L0 * 22, h['ty'] + uy / L0 * 22
            dx, dy = gx_ - h['x'], gy_ - h['y']; L = math.hypot(dx, dy) or 1
            if abs(dx) > 2: h['face'] = 1 if dx > 0 else -1
            if L > 10: h['x'] += dx / L * min(L, SPD * dt); h['y'] += dy / L * min(L, SPD * dt); h['moving'] = t
            else:
                h['nb'] = t + BINT; h['face'] = 1 if h['tx'] >= h['x'] else -1
                if bite(h['tx'], h['ty']):
                    h['chomp'] = t
                    for _ in range(3): shards.append([h['tx'], h['ty'], rnd.uniform(-160, 160), rnd.uniform(-260, -80), t])
                    if t - last_crunch > 0.14: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
                h['tx'] = None
                rim = rim_cells()
        left = 1 - eaten[INC].sum() / NTOT
        if left < 0.004: eaten[INC] = True; t_done = t; events.append((round(t, 3), 'victory')); events.append((round(t + 0.2, 3), 'cheer'))
    left = 1 - eaten[INC].sum() / NTOT
    frames.append(([dict(x=h['x'], y=h['y'], born=h['born'], chomp=h['chomp'], ph=h['ph'], face=h['face'], mv=h.get('moving', -9)) for h in hol],
                   eaten.copy(), max(0.0, left) if t_done is None else 0.0))
    if t_done is not None and t > t_done + 3.0: break
from scipy import ndimage
print('ALL GONE at', t_done, 'hollows', len(hol), 'frames', len(frames), 'max holes', max(ndimage.label(fr[1])[1] for fr in frames[::10]))
for s_ in (3, 6, 9, 12, 15, 18):
    if s_ * FPS < len(frames): print(' t', s_, 'left', round(frames[s_ * FPS][2] * 100))
if len(sys.argv) > 2 and sys.argv[2] == 'sim': sys.exit()
# ---------------- art
mb = Image.open(A + 'bg_moon.gif'); BGM = []
for i in range(mb.n_frames):
    mb.seek(i); f = mb.convert('RGB'); s = H / f.height; cw = int(W / s)
    BGM.append(ImageEnhance.Brightness(f.crop((f.width // 2 - cw // 2, 0, f.width // 2 + cw // 2, f.height)).resize((W, H), Image.NEAREST)).enhance(0.75).convert('RGBA'))
sg = Image.open(A + 'sun_hd.gif'); SUN = []
for i in range(0, sg.n_frames, 4):
    sg.seek(i); SUN.append(sg.convert('RGB').crop((420, 0, 1500, 1080)).resize((2 * RAD, 2 * RAD), Image.NEAREST).convert('RGBA'))
dg = Image.open(A + 'dragon.gif'); DRG = []
for i in range(dg.n_frames):
    dg.seek(i); f = dg.convert('RGBA').crop((10, 10, 1280, 1270)); DRG.append(f.resize((520, 518), Image.NEAREST))
GK = ['mush', 'acv', 'mel', 'cre']; GUM = {k: up(Image.open(R + f'pixellab/gummies/pick_{k}.png').convert('RGBA'), 2) for k in GK}
rg = random.Random(4); HOARD = []
for _ in range(34):
    a = rg.uniform(math.pi * 0.05, math.pi * 0.95); r = rg.uniform(0.25, 0.95)
    HOARD.append((rg.choice(GK), RAD + 230 * r * math.cos(a), RAD + 175 + 90 * r * math.sin(a) * 0.9))
HOARD.sort(key=lambda h: h[2])
CIRC = Image.new('L', (2 * RAD, 2 * RAD), 0); ImageDraw.Draw(CIRC).ellipse([0, 0, 2 * RAD - 1, 2 * RAD - 1], fill=255)
def picture(t):
    p = SUN[int(t * 4) % len(SUN)].copy()
    dr = DRG[int(t * 6) % len(DRG)]; p.alpha_composite(dr, (RAD - dr.width // 2, 2 * RAD - dr.height + 30))
    for k, x, y in HOARD:
        g = GUM[k]; p.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    return p
# frosted, near-opaque glass (the art only shows through the hole)
gq = Image.new('RGBA', (2 * RAD // 4 + 1, 2 * RAD // 4 + 1), (196, 222, 242, 252)); gd = ImageDraw.Draw(gq)
for k in range(-30, 60):
    x = k * 22
    gd.polygon([(x, 0), (x + 6, 0), (x + 6 - RAD // 2 * 0.55, RAD // 2), (x - RAD // 2 * 0.55, RAD // 2)], fill=(236, 246, 255, 254))
nr = random.Random(1)
for _ in range(500):
    x, y = nr.randrange(gq.width), nr.randrange(gq.height); gq.putpixel((x, y), nr.choice([(210, 232, 248, 252), (185, 212, 236, 252)]))
GLASS = up(gq, 4).crop((0, 0, 2 * RAD, 2 * RAD))
RING = up(Image.open(R + 'fork_a3/ring_big_q.png').convert('RGBA'), 4)
CH = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(R + 'fork_a3/hollow_chomp/*.png'))[1:]]
CHL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in CH]
RUN = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(R + 'pixellab/maze/anim/hollow_srun/*.png'))[1:]]
RUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in RUN]
IDLE = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(R + 'fork_a3/hollow_chomp/*.png'))[:1]]
MOUTH = (92, 74)        # mouth point inside the 2x 184px canvas (head ~y28-46 native, centre x46)
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['The Hollow eats', 'all the glass'], accent=1); print('hook bottom', HB)
CRACKS = []
cr = random.Random(7)
for k in range(7):
    a = k * 2 * math.pi / 7 + cr.uniform(-0.3, 0.3); pts = [(S0[0] - PX0, S0[1] - PY0)]
    for s_ in range(4): x, y = pts[-1]; aa = a + cr.uniform(-0.5, 0.5); L = cr.uniform(18, 34); pts.append((x + L * math.cos(aa), y + L * math.sin(aa)))
    CRACKS.append(pts)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v32_noaudio.mp4'], stdin=subprocess.PIPE)
N = len(frames); SAVE = {int(0.2 * FPS), int(3 * FPS), int(9 * FPS), int(t_done * FPS) - 20, N - 10}
for f in range(N):
    t = f / FPS; hl, em, left = frames[f]
    img = BGM[int(t * 5) % len(BGM)].copy()
    pic = picture(t)
    # Hollows inside the picture (behind the glass), back to front
    for i, h in sorted(enumerate(hl), key=lambda e: e[1]['y']):
        if t_done is not None and t >= t_done:
            fr = IDLE[0]; hop = -int(26 * abs(math.sin((t - t_done) * 7 + h['ph'])))
        else:
            hop = 0
            if t - h['chomp'] < 0.3: fr = (CH if h['face'] > 0 else CHL)[int((t - h['chomp']) * 26) % len(CH)]
            elif t - h['mv'] < 0.1: fr = (RUN if h['face'] > 0 else RUNL)[int(t * 12 + i) % len(RUN)]
            else: fr = (CH if h['face'] > 0 else CHL)[0]
        if t - h['born'] < 0.3 and h['born'] > 0:
            k_ = 0.4 + 0.6 * (t - h['born']) / 0.3; fr = fr.resize((max(1, int(fr.width * k_)), max(1, int(fr.height * k_))), Image.NEAREST)
            mx, my = MOUTH[0] * k_, MOUTH[1] * k_
        else: mx, my = MOUTH
        if h['face'] < 0: mx = fr.width - mx
        pic.alpha_composite(fr, (int(h['x'] - PX0 - mx), int(h['y'] - PY0 - my + hop)))
        if 0 <= t - h['born'] < 0.4 and h['born'] > 0:
            u = (t - h['born']) / 0.4
            layer(pic, lambda d, x=h['x'] - PX0, y=h['y'] - PY0, u=u: [d.ellipse([x - 30 - 30 * u + k * 22, y - 20 - 20 * u, x + 10 * u + k * 22, y + 10], fill=(170, 140, 220, int(200 * (1 - u)))) for k in range(-1, 2)])
    # the glass with the one hole
    gm = Image.fromarray((~em & INC).astype(np.uint8) * 255, 'L').resize((GN * CELL, GN * CELL), Image.NEAREST).crop((0, 0, 2 * RAD, 2 * RAD))
    gl = GLASS.copy(); a = np.array(gl.getchannel('A')).astype(np.uint16) * np.array(gm).astype(np.uint16) // 255
    gl.putalpha(Image.fromarray(a.astype(np.uint8)))
    edge = (~em) & INC & (np.roll(em, 1, 0) | np.roll(em, -1, 0) | np.roll(em, 1, 1) | np.roll(em, -1, 1))
    if edge.any():
        e = Image.fromarray(edge.astype(np.uint8) * 210, 'L').resize((GN * CELL, GN * CELL), Image.NEAREST).crop((0, 0, 2 * RAD, 2 * RAD))
        el = Image.new('RGBA', gl.size, (255, 255, 255, 0)); el.putalpha(e); gl.alpha_composite(el)
    if t < T_FIRST:       # knock knock: cracks spread from the spot the first Hollow is about to bite
        u = min(1, t / T_FIRST)
        def crk(d):
            for pts in CRACKS:
                n = max(2, int(len(pts) * (0.35 + 0.65 * u) + 0.5))
                d.line(pts[:n], fill=(70, 90, 120, 255), width=4)
        layer(gl, crk)
    pic.alpha_composite(gl)
    out = Image.new('RGBA', pic.size, (0, 0, 0, 0)); out.paste(pic, (0, 0), CIRC)
    sh = int(4 * math.sin(t * 60)) if t < T_FIRST else 0
    img.alpha_composite(out, (PX0 + sh, PY0))
    img.alpha_composite(RING, (CX - RING.width // 2, CY - RING.height // 2))
    # glass shards flying out of the hole toward the viewer
    alive = []
    def shd(d):
        for s in shards:
            u = t - s[4]
            if 0 <= u < 0.7:
                x, y = s[0] + s[2] * u, s[1] + s[3] * u + 700 * u * u
                d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(220, 240, 255, int(255 * (1 - u / 0.7)))); alive.append(s)
            elif u < 0: alive.append(s)
    layer(img, shd); shards = alive
    # counter panel under the hook
    d = ImageDraw.Draw(img)
    if t_done is None or t < t_done:
        layer(img, lambda d: d.rounded_rectangle([200, HB + 14, 880, HB + 136], 20, fill=(12, 10, 30, 210), outline=(230, 190, 90, 255), width=5))
        d = ImageDraw.Draw(img)
        ctext(d, 540, HB + 34, f'GLASS LEFT: {max(1, int(math.ceil(left * 100))) if left > 0 else 0}%', F(42), (255, 255, 255), 6)
        ctext(d, 540, HB + 90, f'HOLLOWS: {len(hl)}', F(30), (180, 160, 240), 5)
    else:
        u = t - t_done; s = min(1, u / 0.25)
        ctext(d, 540, HB + 40 - int(20 * s), 'ALL GONE!', F(int(40 + 40 * s)), (255, 214, 60), 8)
        layer(img, lambda d: [d.rectangle([CX + 380 * math.cos(k * 0.7 + t), CY + 380 * math.sin(k * 0.7 + t), CX + 380 * math.cos(k * 0.7 + t) + 10, CY + 380 * math.sin(k * 0.7 + t) + 10], fill=(255, 230, 120, 220)) for k in range(9)])
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in SAVE: img.convert('RGB').save(f'f_{f}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': sorted(events)}, open('v32_events.json', 'w')); print('done', N / FPS)
