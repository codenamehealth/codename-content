import sys; sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CX, CY, RR, r = 500, 960, 340, 62   # ring moved left 40px so the timer arc clears the lower-right buttons (sim is translation-invariant, same plan)
GAPW = 0.78; OMEGA = 1.35; GRAV = 1500
KINDS = ['s1', 's2', 's3', 's4', 'gold']
GLOW = {'s1': (120, 220, 120), 's2': (110, 160, 255), 's3': (240, 120, 200), 's4': (190, 120, 255), 'gold': (255, 160, 50)}   # 'gold' slot is now the mushroom gummy
T0 = 0.8; TRY = 4.0
def gap_center(t): return -math.pi / 2 + OMEGA * t
def angdiff(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi
def run_attempt(seed, frozen, tstart, dur=TRY):
    rnd = random.Random(seed); ang = rnd.uniform(0, 2 * math.pi); spd = rnd.uniform(650, 950)
    x, y = CX + rnd.uniform(-40, 40), CY + rnd.uniform(-60, 20); vx, vy = spd * math.cos(ang), spd * math.sin(ang)
    path = []; sub = 8; dt = 1 / (FPS * sub); bounces = []
    for f in range(int(dur * FPS)):
        t = tstart + f / FPS
        for k in range(sub):
            tt = t + k * dt
            vy += GRAV * dt; x += vx * dt; y += vy * dt
            dx, dy = x - CX, y - CY; d = math.hypot(dx, dy)
            if d + r > RR and d < RR + r:
                a = math.atan2(dy, dx); inside_gap = abs(angdiff(a, gap_center(tt))) < GAPW / 2 - math.asin(r / RR) * 0.9
                if not inside_gap and d < RR:
                    nx, ny = dx / d, dy / d; vn = vx * nx + vy * ny
                    if vn > 0:
                        vx -= 2 * vn * nx; vy -= 2 * vn * ny; x, y = CX + nx * (RR - r), CY + ny * (RR - r)
                        if not bounces or tt - bounces[-1] > 0.08: bounces.append(tt)
            for (fx, fy) in frozen:
                ddx, ddy = x - fx, y - fy; dd = math.hypot(ddx, ddy)
                if 0 < dd < 2 * r:
                    nx, ny = ddx / dd, ddy / dd; vn = vx * nx + vy * ny
                    if vn < 0: vx -= 2 * vn * nx; vy -= 2 * vn * ny
                    x, y = fx + nx * 2 * r, fy + ny * 2 * r
                    if not bounces or tt - bounces[-1] > 0.08: bounces.append(tt)
        path.append((x, y))
        if math.hypot(x - CX, y - CY) > RR + r + 4: return 'escape', path, bounces, t + 1 / FPS
    return 'fail', path, bounces, tstart + dur
def plan(base):
    frozen = []; seq_ = []; t = T0
    for i, k in enumerate(KINDS):
        for s in range(base * 1000 + i * 100, base * 1000 + i * 100 + 99):
            res, path, b, tend = run_attempt(s, frozen, t)
            if i < 4 and res == 'fail' and len(b) >= 4: break
            if i == 4 and res == 'escape' and 2.0 < tend - t < 3.7: break
        else: return None
        seq_.append((k, t, res, path, b, tend))
        if res == 'fail': frozen.append(path[-1])
        t = tend + 0.35
    return seq_
SEQ = None
for base in range(1, 30):
    SEQ = plan(base)
    if SEQ: print('plan base', base, [(k, round(t, 2), res, round(tend - t, 2)) for k, t, res, p, b, tend in SEQ]); break
T_ESC = SEQ[-1][5]; END = T_ESC + 3.2; N = int(END * FPS)
BG = bg_frames('found_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.45)
def nored(im):
    a = np.array(im); rr_, gg, bb_ = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(rr_ > 140) & (gg < 110) & (bb_ < 140)] = 0; return Image.fromarray(a)
SLM = up(crop(nored(Image.open(PL + 'race/slime_idle_c/00.png').convert('RGBA'))), 3)
GUM = {k: SLM for k in KINDS[:4]}; GUM['gold'] = gummy('mush', 3)   # COIN/GOLD FIX: the 5th ball carries a mushroom product gummy instead of the gold gummy
EAT = seq('../../fork3/hollow_eat', 3, 0, 13); HID = idle('hollow', 3)
HX, HY = 790, 1495
HOOK, HB = hook_layer(['EACH BALL HAS', 'ONLY 4 SECONDS'], accent=1, sub='TO ESCAPE')
ev = [(T0 - 0.2, 'go_8bit')]
for k, t, res, path, b, tend in SEQ:
    ev += [(round(bt, 3), 'tick_8bit') for bt in b[:40]]
    ev += [(round(t + s_, 3), 'reeltick_8bit') for s_ in (1, 2, 3)]
    ev.append((round(tend, 3), 'buzz_8bit' if res == 'fail' else 'poof'))
ev += [(round(T_ESC + 0.6, 3), 'crunch_8bit'), (round(T_ESC + 0.9, 3), 'victory')]
def bubble(k, frozen=False):
    sz = 2 * r + 8; im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if frozen:
        d.ellipse([4, 4, sz - 4, sz - 4], fill=(150, 170, 200, 235), outline=(230, 240, 255, 255), width=4)
        g = ImageEnhance.Color(GUM[k]).enhance(0.25); g = ImageEnhance.Brightness(g).enhance(0.75)
        im.alpha_composite(g, (sz // 2 - g.width // 2, sz // 2 - g.height // 2))
        d.polygon([(sz * 0.3, sz * 0.2), (sz * 0.45, sz * 0.12), (sz * 0.4, sz * 0.35)], fill=(255, 255, 255, 160))
        d.line([(sz * 0.6, sz * 0.25), (sz * 0.75, sz * 0.5), (sz * 0.62, sz * 0.7)], fill=(255, 255, 255, 140), width=3)
    else:
        c = GLOW[k]
        d.ellipse([4, 4, sz - 4, sz - 4], fill=c + (70,), outline=(240, 250, 255, 230), width=4)
        g = GUM[k]; im.alpha_composite(g, (sz // 2 - g.width // 2, sz // 2 - g.height // 2))
        d.ellipse([sz * 0.25, sz * 0.18, sz * 0.42, sz * 0.32], fill=(255, 255, 255, 190))
    return im
BUB = {k: bubble(k) for k in KINDS}; FROZ = {k: bubble(k, True) for k in KINDS}
rng = random.Random(4); FLY = [(rng.uniform(40, 1040), rng.uniform(420, 1800), rng.uniform(0, 6.3)) for _ in range(30)]
w = Writer('v64_noaudio.mp4')
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    def bgfx(d):
        for fx, fy, ph in FLY:
            a = int(120 + 120 * math.sin(t * 2 + ph))
            if a > 60: d.ellipse([fx + 20 * math.sin(t + ph) - 4, fy - 4, fx + 20 * math.sin(t + ph) + 4, fy + 4], fill=(230, 255, 150, a))
        d.ellipse([CX - RR + 10, CY - RR + 10, CX + RR - 10, CY + RR - 10], fill=(10, 8, 24, 110))
    layer(img, bgfx)
    # current attempt
    cur = None
    for i, (k, t0, res, path, b, tend) in enumerate(SEQ):
        if t0 <= t < tend + (0.35 if res == 'fail' else 0) : cur = i
    # ring + timer arc
    gc = gap_center(min(t, T_ESC + 2))
    def ring(d):
        for deg in range(0, 360, 2):
            a = math.radians(deg)
            if abs(angdiff(a, gc)) < GAPW / 2: continue
            for rad, col, wdt in ((RR + 18, (120, 90, 220, 90), 30), (RR + 12, (170, 140, 255, 255), 16)):
                d.arc([CX - rad, CY - rad, CX + rad, CY + rad], deg, deg + 2.4, fill=col, width=wdt)
        for deg in range(0, 360, 30):
            a = math.radians(deg) + t * 0.3
            if abs(angdiff(a, gc)) < GAPW / 2 + 0.05: continue
            px, py = CX + (RR + 12) * math.cos(a), CY + (RR + 12) * math.sin(a)
            d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=(255, 225, 140, 255))
        if cur is not None and t < SEQ[cur][5]:
            u = (t - SEQ[cur][1]) / TRY; rem = max(0, 1 - u)
            col = (90, 210, 90) if rem > 0.5 else ((240, 200, 60) if rem > 0.25 else (240, 80, 70))
            d.arc([CX - RR - 46, CY - RR - 46, CX + RR + 46, CY + RR + 46], -90, -90 + 360 * rem, fill=col + (255,), width=12)
    layer(img, ring)
    # frozen bubbles
    for i, (k, t0, res, path, b, tend) in enumerate(SEQ):
        if res == 'fail' and t >= tend:
            fx, fy = path[-1]; fb = FROZ[k]; img.alpha_composite(fb, (int(fx - fb.width / 2), int(fy - fb.height / 2)))
    if cur is not None:
        k, t0, res, path, b, tend = SEQ[cur]
        idx = int((t - t0) * FPS)
        if t < tend:
            def trail(d):
                for j in range(max(0, idx - 10), idx):
                    px, py = path[min(j, len(path) - 1)]; a = int(30 + 15 * (j - idx + 10))
                    d.ellipse([px - 18, py - 18, px + 18, py + 18], fill=GLOW[k] + (a,))
            layer(img, trail)
            px, py = path[min(idx, len(path) - 1)]; bb = BUB[k]; img.alpha_composite(bb, (int(px - bb.width / 2), int(py - bb.height / 2)))
            n = max(1, math.ceil(t0 + TRY - t))
            text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])
        elif res == 'fail':
            px, py = path[-1]
            text_layer(img, [(px, py - 100 - (t - tend) * 60, 'FROZEN!', 30, (170, 210, 255), 5, int(255 * max(0, 1 - (t - tend) / 0.35)))])
    # escape: pop and gummy flies to the Hollow
    k5, t5, res5, path5, b5, tend5 = SEQ[-1]
    if t >= T_ESC:
        u = t - T_ESC; ex, ey = path5[-1]
        if u < 0.4:
            def popfx(d):
                for j in range(12):
                    pass
                for j in range(12):
                    a = j * 0.52; rr_ = 20 + 160 * u
                    d.rectangle([ex + rr_ * math.cos(a) - 6, ey + rr_ * math.sin(a) - 6, ex + rr_ * math.cos(a) + 6, ey + rr_ * math.sin(a) + 6], fill=(255, 235, 150, int(255 * (1 - u / 0.4))))
            layer(img, popfx)
        if u < 0.6:
            v = u / 0.6; gx = ex + (HX - ex) * v; gy = ey + (HY - 150 - ey) * v - 260 * math.sin(v * math.pi)
            g = GUM['gold']; img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    # the Hollow waiting outside the ring
    if t >= T_ESC + 0.6: hf = EAT[min(len(EAT) - 1, int((t - T_ESC - 0.6) * 12))]
    else: hf = HID[int(t * 6) % len(HID)]
    layer(img, lambda d: d.ellipse([HX - 70, HY - 14, HX + 70, HY + 14], fill=(0, 0, 0, 90)))
    img.alpha_composite(hf, (HX - hf.width // 2, HY - 78 * 3))
    # header + footer
    layer(img, lambda d: d.rounded_rectangle([78, 1408, 470, 1490], 20, fill=(12, 10, 26, 210)))
    d = ImageDraw.Draw(img)
    att = (cur + 1) if cur is not None else (5 if t >= T_ESC else 1)
    d.text((104, 1432), f'ATTEMPT {att}', font=F(34), fill=(255, 255, 255), stroke_width=4, stroke_fill=(20, 15, 35))
    if t < T0: text_layer(img, [(CX, CY - 40, 'READY?', 70, (255, 255, 255), 8, 255)])
    if t >= T_ESC + 0.2:
        u = min(1, (t - T_ESC - 0.2) / 0.3)
        layer(img, lambda dd: dd.rounded_rectangle([88, 900, 868, 1170], 26, fill=(12, 10, 26, int(225 * u))))
        d = ImageDraw.Draw(img); d.rounded_rectangle([88, 900, 868, 1170], 26, outline=(232, 182, 76, int(255 * u)), width=5)
        ctext(d, 478, 930, 'ESCAPED ON TRY 5!', F(44), (255, 214, 60), 6, int(255 * u))
        ctext(d, 478, 1020, 'Did you guess it?', F(34), (255, 255, 255), 5, int(255 * u))
        ctext(d, 478, 1085, 'Comment your number', F(30), (255, 255, 255), 5, int(255 * u))
    img.alpha_composite(HOOK)
    w.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/q64_{f:04d}.png')
w.close(); json.dump(ev, open('v64_ev.json', 'w')); print('done', END)
