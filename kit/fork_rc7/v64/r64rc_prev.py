import sys; sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../fork_rc1'); from hook2 import hook_layer2
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
CX, CY, RR, r = 500, 985, 340, 62   # ring moved left 40px so the timer arc clears the lower-right buttons (sim is translation-invariant, same plan)
GAPW = 0.78; OMEGA = 1.35; GRAV = 1500
KINDS = ['s1', 's2', 's3', 'gold']   # 3 frozen tries then the escape (was 4 + escape)
GLOW = {'s1': (120, 220, 120), 's2': (110, 160, 255), 's3': (240, 120, 200), 's4': (190, 120, 255), 'gold': (255, 160, 50)}   # 'gold' slot is now the mushroom gummy
T0 = 0.0; TRY = 4.0; GAP_T = 0.25
def gap_center(t): return -math.pi / 2 + OMEGA * t
def angdiff(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi
def run_attempt(seed, frozen, tstart, dur=TRY):
    rnd = random.Random(seed); ang = rnd.uniform(0, 2 * math.pi); spd = rnd.uniform(650, 950)
    x, y = CX + rnd.uniform(-40, 40), CY + rnd.uniform(-60, 20); vx, vy = spd * math.cos(ang), spd * math.sin(ang)
    path = []; sub = 8; dt = 1 / (FPS * sub); bounces = []; near = []
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
                    if vn > 0 and abs(angdiff(a, gap_center(tt))) - GAPW / 2 < 0.10: near.append(tt)
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
        if math.hypot(x - CX, y - CY) > RR + r + 4:
            vel = (vx, vy); return 'escape', path, bounces, t + 1 / FPS, near, vel
    return 'fail', path, bounces, tstart + dur, near, (vx, vy)
def plan(base):
    frozen = []; seq_ = []; t = T0
    for i, k in enumerate(KINDS):
        for s in range(base * 1000 + i * 100, base * 1000 + i * 100 + 99):
            res, path, b, tend, near, vel = run_attempt(s, frozen, t)
            if i < 3 and res == 'fail' and len(b) >= 4 and (i != 2 or any(1.0 < x - t < 3.0 for x in near)) and (i == 2 or not near): break
            if i == 3 and res == 'escape' and 1.6 < tend - t < 2.3: break
        else: return None
        seq_.append((k, t, res, path, b, tend, near, vel))
        if res == 'fail': frozen.append(path[-1])
        t = tend + GAP_T
    return seq_
SEQ = None
for base in range(1, 30):
    SEQ = plan(base)
    if SEQ: print('plan base', base, [(k, round(t, 2), res, round(tend - t, 2), [round(x, 2) for x in nr[:3]]) for k, t, res, p, b, tend, nr, v in SEQ]); break
T_ESC = SEQ[-1][5]; T_CARD = T_ESC + 0.5; END = T_CARD + 1.5; N = int(round(END * FPS))
NEAR_T = [x for x in SEQ[2][6] if 1.0 < x - SEQ[2][1] < 3.0][0]; print('esc', round(T_ESC, 2), 'near', round(NEAR_T, 2), 'end', round(END, 2))
BG = bg_frames('found_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.45)
def nored(im):
    a = np.array(im); rr_, gg, bb_ = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(rr_ > 140) & (gg < 110) & (bb_ < 140)] = 0; return Image.fromarray(a)
SLM = up(crop(nored(Image.open(PL + 'race/slime_idle_c/00.png').convert('RGBA'))), 3)
GUM = {k: SLM for k in KINDS[:4]}; GUM['gold'] = gummy('mush', 3)   # COIN/GOLD FIX: the 5th ball carries a mushroom product gummy instead of the gold gummy
EAT = seq('../../fork3/hollow_eat', 3, 0, 13); HID = idle('hollow', 3)
HX, HY = 790, 1495
HOOK, HB = hook_layer2(['EACH BALL HAS', 'ONLY 4 SECONDS'], accent=1, sub='Which try escapes?'); print('HB', HB)
ev = []
for k, t, res, path, b, tend, nr, vel in SEQ:
    lb = -9
    for bt in b:
        if bt - lb >= 0.3 and bt < tend - 0.1: ev.append((round(bt, 3), 'tick_8bit')); lb = bt
    ev.append((round(tend, 3), 'buzz_8bit' if res == 'fail' else 'powerup_8bit'))
ev += [(round(NEAR_T, 3), 'whoosh_8bit'), (round(T_ESC + 0.05, 3), 'poof'), (round(T_ESC + 0.9, 3), 'crunch_8bit'), (round(T_CARD, 3), 'victory')]
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
    for i, (k, t0, res, path, b, tend, nr, vel) in enumerate(SEQ):
        if t0 <= t < tend + (GAP_T if res == 'fail' else 0) : cur = i
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
    for i, (k, t0, res, path, b, tend, nr, vel) in enumerate(SEQ):
        if res == 'fail' and t >= tend:
            fx, fy = path[-1]; fb = FROZ[k]; img.alpha_composite(fb, (int(fx - fb.width / 2), int(fy - fb.height / 2)))
    if cur is not None:
        k, t0, res, path, b, tend, nr, vel = SEQ[cur]
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
            pass
    # escape: pop and gummy flies to the Hollow
    k5, t5, res5, path5, b5, tend5, nr5, vel5 = SEQ[-1]
    if t >= T_ESC:
        u = t - T_ESC; ex, ey = path5[-1]
        if u < 0.5:
            sx_, sy_ = ex + vel5[0] * u * 1.6, ey + vel5[1] * u * 1.6
            def streak(d):
                for j in range(10):
                    q = j / 10; d.ellipse([ex + (sx_ - ex) * q - 22, ey + (sy_ - ey) * q - 22, ex + (sx_ - ex) * q + 22, ey + (sy_ - ey) * q + 22], fill=GLOW['gold'] + (int(40 + 120 * q),))
            layer(img, streak); bb = BUB['gold']
            if u < 0.3: img.alpha_composite(bb, (int(sx_ - bb.width / 2), int(sy_ - bb.height / 2)))
        if u < 0.4:
            def popfx(d):
                for j in range(12):
                    pass
                for j in range(12):
                    a = j * 0.52; rr_ = 20 + 160 * u
                    d.rectangle([ex + rr_ * math.cos(a) - 6, ey + rr_ * math.sin(a) - 6, ex + rr_ * math.cos(a) + 6, ey + rr_ * math.sin(a) + 6], fill=(255, 235, 150, int(255 * (1 - u / 0.4))))
            layer(img, popfx)
        if 0.3 <= u < 0.9:
            ex, ey = ex + vel5[0] * 0.3 * 1.6, ey + vel5[1] * 0.3 * 1.6
            v = (u - 0.3) / 0.6; gx = ex + (HX - ex) * v; gy = ey + (HY - 150 - ey) * v - 260 * math.sin(v * math.pi)
            g = GUM['gold']; img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    # the Hollow waiting outside the ring
    if t >= T_ESC + 0.9: hf = EAT[min(len(EAT) - 1, int((t - T_ESC - 0.9) * 12))]
    else: hf = HID[int(t * 6) % len(HID)]
    layer(img, lambda d: d.ellipse([HX - 70, HY - 14, HX + 70, HY + 14], fill=(0, 0, 0, 90)))
    img.alpha_composite(hf, (HX - hf.width // 2, HY - 78 * 3))
    # TRY chip (2x)
    layer(img, lambda d: d.rounded_rectangle([78, 1418, 420, 1496], 20, fill=(12, 10, 26, 225), outline=(170, 140, 255, 255), width=5))
    att = (cur + 1) if cur is not None else (len(SEQ) if t >= T_ESC else 1)
    text_layer(img, [(249, 1427, f'TRY {att}', 60, (255, 255, 255), 8, 255)])
    # big stamps: FROZEN! across the ring on every fail, SO CLOSE! on try 3's near miss, ESCAPED! on the escape
    st = None
    for i, (k, t0, res, path, b, tend, nr, vel) in enumerate(SEQ):
        if res == 'fail' and 0 <= t - tend < 0.45: st = ('FROZEN!', (150, 220, 255), t - tend, 0.45)
    if 0 <= t - NEAR_T < 0.6 and st is None: st = ('SO CLOSE!', (255, 200, 70), t - NEAR_T, 0.6)
    if 0 <= t - T_ESC < 0.5: st = ('ESCAPED!', (120, 255, 120), t - T_ESC, 0.5)
    if st:
        txt, col, u, du = st; pop = 1.0 if u > 0.08 else 0.7 + 3.75 * u; a = int(255 * min(1, (du - u) / 0.1))
        fnt = F(int(96 * pop)); Ls = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(Ls); tw = ds.textlength(txt, font=fnt)
        ds.rectangle([CX - 386, CY - 80, CX + 386, CY + 80], fill=(10, 8, 22, int(a * 0.9)))
        ds.line([(CX - 386, CY - 80), (CX + 386, CY - 80)], fill=col + (a,), width=6); ds.line([(CX - 386, CY + 80), (CX + 386, CY + 80)], fill=col + (a,), width=6)
        ds.text((CX - tw / 2, CY - fnt.size / 2), txt, font=fnt, fill=col + (a,), stroke_width=10, stroke_fill=(10, 6, 18, a))
        img.alpha_composite(Ls)
    if t >= T_CARD:
        u = t - T_CARD; a = 1.0 if u > 0.1 else u / 0.1; pop = 1.0 if u > 0.1 else 0.8 + 2 * u
        layer(img, lambda dd: dd.rounded_rectangle([96, 820, 866, 1210], 26, fill=(12, 10, 26, int(235 * a)), outline=(232, 182, 76, int(255 * a)), width=6))
        text_layer(img, [(481, 848, 'ESCAPED ON', int(64 * pop), (255, 214, 60), 9, int(255 * a)), (481, 928, f'TRY {len(SEQ)}!', int(64 * pop), (255, 214, 60), 9, int(255 * a)),
                         (481, 1040, 'COMMENT', 52, (255, 255, 255), 8, int(255 * a)), (481, 1110, 'YOUR GUESS', 52, (255, 255, 255), 8, int(255 * a))])
    img.alpha_composite(HOOK)
    w.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/q64_{f:04d}.png')
w.close(); json.dump({'events': sorted(ev)}, open('v64_ev.json', 'w')); print('done', END)
