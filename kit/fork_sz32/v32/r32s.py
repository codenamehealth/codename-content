import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '../../'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
CX, CY, RAD = 490, 1010, 336; CELL = 4; GN = 2 * RAD // CELL
yy, xx = np.mgrid[0:GN, 0:GN]; INC = ((xx + 0.5 - GN / 2) ** 2 + (yy + 0.5 - GN / 2) ** 2) <= (GN / 2) ** 2
TOTAL = INC.sum()
# ---------------- simulation
SPAWN = [1.0, 3.4, 5.8, 8.2, 10.6, 13.0, 15.4]
def sim(seed, BR=3, BI=0.42, SP=150):
    rng = random.Random(seed); mask = INC.copy(); hol = []; t = 0; dt = 1 / FPS; frames = []; ev = []; done_t = None
    cells = np.argwhere(INC)
    while True:
        si = sum(1 for s in SPAWN if s <= t + 1e-9)
        target_n = 0 if si == 0 else 2 ** (si - 1)
        if len(hol) < target_n:
            if not hol: hol.append(dict(x=CX, y=CY + 120, tx=None, ty=None, nb=0, ph=rng.uniform(0, 6), born=t, vx=0, bite=-1)); ev.append((t, 'poof'))
            else:
                for h in list(hol):
                    hol.append(dict(x=h['x'] + rng.uniform(-20, 20), y=h['y'] + rng.uniform(-10, 10), tx=None, ty=None, nb=0, ph=rng.uniform(0, 6), born=t, vx=0, bite=-1))
                ev.append((t, 'poof'))
        remaining = mask.sum()
        if remaining == 0 and done_t is None: done_t = t
        for h in hol:
            if h['tx'] is None and remaining > 0:
                rem = np.argwhere(mask)
                cand = rem[[rng.randrange(len(rem)) for _ in range(24)]]
                dd = [(c[1] * CELL + CX - RAD - h['x']) ** 2 + (c[0] * CELL + CY - RAD - h['y']) ** 2 for c in cand]
                c = cand[int(np.argmin(dd))]; h['tx'], h['ty'] = c[1] * CELL + CX - RAD + 2, c[0] * CELL + CY - RAD + 2
            if h['tx'] is None: continue
            dx, dy = h['tx'] - h['x'], h['ty'] - h['y']; L = math.hypot(dx, dy)
            if L > 6:
                s = min(L, SP * dt * (1 + 0.3 * math.sin(t * 3 + h['ph']))); h['x'] += dx / L * s; h['y'] += dy / L * s; h['vx'] = dx
            elif t - h['bite'] >= BI:
                h['bite'] = t; gx, gy = int((h['tx'] - CX + RAD) / CELL), int((h['ty'] - CY + RAD) / CELL)
                y0, y1, x0, x1 = max(0, gy - BR), min(GN, gy + BR + 1), max(0, gx - BR), min(GN, gx + BR + 1)
                sub = (xx[y0:y1, x0:x1] - gx) ** 2 + (yy[y0:y1, x0:x1] - gy) ** 2 <= BR * BR + rng.uniform(-2, 3)
                mask[y0:y1, x0:x1] &= ~sub
                h['nb'] += 1
                if h['nb'] >= rng.choice([2, 3]) or not mask[max(0, gy - BR):gy + BR + 1, max(0, gx - BR):gx + BR + 1].any():
                    h['tx'] = None; h['nb'] = 0
        if remaining and remaining < TOTAL * 0.004: mask[:] = False
        frames.append((mask.copy() if len(frames) % 1 == 0 else None, [(h['x'], h['y'], h['bite'], h['vx'], h['born']) for h in hol], remaining / TOTAL))
        t += dt
        if done_t is not None and t > done_t + 3.6: break
        if t > 40: break
    return frames, ev, done_t
if len(sys.argv) > 1 and sys.argv[1] == 'tune':
    for BR, BI, SP in ((5, 0.5, 200), (4, 0.4, 220), (5, 0.4, 240), (6, 0.5, 220)):
        fr, ev, dt_ = sim(1, BR, BI, SP)
        tl = [round(fr[int(s * FPS)][2] * 100) for s in (3, 6, 9, 12, 15, 18, 21, 24) if int(s * FPS) < len(fr)]
        print(BR, BI, SP, 'done', dt_ and round(dt_, 1), tl)
    sys.exit()
BR, BI, SPD = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
FR, EV, DONE = sim(1, BR, BI, SPD); N = len(FR); print('frames', N, 'done', DONE)
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
GK = ['mush', 'acv', 'mel', 'cre', 'gold']; GUM = {k: up(Image.open(R + f'pixellab/gummies/pick_{k}.png').convert('RGBA'), 2) for k in GK}
rg = random.Random(4); HOARD = []
for _ in range(34):
    a = rg.uniform(math.pi * 0.05, math.pi * 0.95); r = rg.uniform(0.25, 0.95)
    HOARD.append((rg.choice(GK), RAD + 230 * r * math.cos(a) * 1.0 - 0, RAD + 175 + 90 * r * math.sin(a) * 0.9))
HOARD.sort(key=lambda h: h[2])
CIRC = Image.new('L', (2 * RAD, 2 * RAD), 0); ImageDraw.Draw(CIRC).ellipse([0, 0, 2 * RAD - 1, 2 * RAD - 1], fill=255)
def picture(t):
    p = SUN[int(t * 4) % len(SUN)].copy()
    dr = DRG[int(t * 6) % len(DRG)]; p.alpha_composite(dr, (RAD - dr.width // 2, 2 * RAD - dr.height + 30))
    for k, x, y in HOARD:
        g = GUM[k]; p.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    out = Image.new('RGBA', p.size, (0, 0, 0, 0)); out.paste(p, (0, 0), CIRC); return out
# glass texture
GL = Image.new('RGBA', (2 * RAD, 2 * RAD), (180, 220, 255, 150)); gd = ImageDraw.Draw(GL)
for k in range(-8, 14):
    x0 = k * 110; gd.polygon([(x0, 2 * RAD), (x0 + 26, 2 * RAD), (x0 + 26 + 2 * RAD, 0), (x0 + 2 * RAD, 0)], fill=(255, 255, 255, 200))
GLA = np.array(GL)
RING = up(Image.open('../../fork_a3/ring_big_q.png').convert('RGBA'), 4)
CH = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('../../fork_a3/hollow_chomp/*.png'))[1:]]
RUN = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(R + 'pixellab/maze/anim/hollow_srun/*.png'))[1:]]
RUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in RUN]
VIC = Image.open(A + 'hollow-victory.gif'); VF = []
for i in range(VIC.n_frames):
    VIC.seek(i); f = VIC.convert('RGBA'); VF.append(f.crop(f.getbbox()))
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['The Hollow eats', 'all the glass'], accent=1); print('hook bottom', HB)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v32_noaudio.mp4'], stdin=subprocess.PIPE)
events = [(round(t, 3), 'poof') for t, k in EV]; shards = []; last_crunch = -1; rng = random.Random(9); prev_bites = {}
for f in range(N):
    t = f / FPS; mask, hol, frac = FR[f]
    img = BGM[int(t * 5) % len(BGM)].copy()
    pic = picture(t)
    # glass where mask is set
    m = np.repeat(np.repeat(mask, CELL, 0), CELL, 1)
    ga = GLA.copy(); ga[..., 3] = np.where(m, ga[..., 3], 0)
    edge = m & ~(np.roll(m, 4, 0) & np.roll(m, -4, 0) & np.roll(m, 4, 1) & np.roll(m, -4, 1))
    ga[edge] = (240, 250, 255, 235)
    glint = 0.5 + 0.5 * math.sin(t * 1.3)
    gl = Image.fromarray(ga.astype(np.uint8))
    pic.alpha_composite(gl)
    # shine sweep
    img.alpha_composite(pic, (CX - RAD, CY - RAD))
    img.alpha_composite(RING, (CX - RING.width // 2, CY - RING.height // 2))
    # hollows
    for i, (x, y, bt, vx, born) in enumerate(hol):
        if t - bt < 0.25: fr = CH[int((t - bt) * 32) % len(CH)]
        else: fr = (RUNL if vx < 0 else RUN)[int(t * 12 + i) % 8]
        hop = 0
        if t - born < 0.35: hop = -int(40 * math.sin((t - born) / 0.35 * math.pi))
        img.alpha_composite(fr, (int(x - fr.width / 2), int(y - 150 + hop)))
        if bt > 0 and prev_bites.get(i) != bt:
            prev_bites[i] = bt
            for _ in range(2): shards.append([x + rng.uniform(-10, 10), y - 70, rng.uniform(-120, 120), rng.uniform(-260, -80), t])
            if t - last_crunch > 0.12: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
        if t - born < 0.4 and born > 0.9:
            layer(img, lambda d, x=x, y=y, u=(t - born) / 0.4: [d.ellipse([x - 40 * u - 10 + k * 12, y - 60 - 30 * u, x - 10 * u + 10 + k * 12, y - 30 - 10 * u], fill=(170, 140, 220, int(200 * (1 - u)))) for k in range(3)])
    alive = []
    def sh(d):
        for s in shards:
            u = t - s[4]
            if u < 0.7:
                x, y = s[0] + s[2] * u, s[1] + s[3] * u + 700 * u * u
                d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(220, 240, 255, int(255 * (1 - u / 0.7)))); alive.append(s)
    layer(img, sh); shards = alive
    # header + counters
    d = ImageDraw.Draw(img)
    done = DONE is not None and t >= DONE
    if not done:
        layer(img, lambda d: d.rounded_rectangle([200, HB + 14, 880, HB + 136], 20, fill=(12, 10, 30, 190), outline=(230, 190, 90, 255), width=5))
        d = ImageDraw.Draw(img)
        ctext(d, 540, HB + 34, f'GLASS LEFT: {max(1, int(math.ceil(frac * 100))) if frac > 0 else 0}%', F(42), (255, 255, 255), 6)
        ctext(d, 540, HB + 90, f'HOLLOWS: {len(hol)}', F(30), (180, 160, 240), 5)
    else:
        u = t - DONE; s = min(1, u / 0.25)
        ctext(d, 540, HB + 40 - int(20 * s), 'ALL GONE!', F(int(40 + 40 * s)), (255, 214, 60), 8)
        layer(img, lambda d: [d.rectangle([CX + 380 * math.cos(k * 0.7 + t), CY + 380 * math.sin(k * 0.7 + t), CX + 380 * math.cos(k * 0.7 + t) + 10, CY + 380 * math.sin(k * 0.7 + t) + 10], fill=(255, 230, 120, 220)) for k in range(9)])
        if not any(e[1] == 'victory' for e in events): events.append((round(DONE, 3), 'victory')); events.append((round(DONE + 0.2, 3), 'cheer'))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 45 == 0: img.convert('RGB').resize((216, 384)).save(f'p_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v32_events.json', 'w')); print('done', N / FPS)
