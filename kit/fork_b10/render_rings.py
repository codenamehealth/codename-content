import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NR = 200; R0 = 70.0; DR = 9.0
GAP = math.radians(float(os.environ.get('GAPDEG', '34')))
CX, CY = W / 2, 1150
BR = 22.0                     # ball radius in world units at scale 1
T0 = 2.0
def ring_r(k): return R0 + DR * k
def omega(k): return float(os.environ.get('OM', '1.9')) * (1 - k / 260.0) * (1 if (k // int(os.environ.get('ALT', '3'))) % 2 == 0 else -1)
_PJ = [random.Random(k * 7 + 1).uniform(-1, 1) for k in range(260)]
def phase0(k): return k * float(os.environ.get('PH', '0.11')) + float(os.environ.get('JIT', '0.4')) * _PJ[k]
def gap_angle(k, t): return phase0(k) + omega(k) * t
def angdiff(a, b):
    d = (a - b + math.pi) % (2 * math.pi) - math.pi; return d
def sim(seed, dur=45):
    rnd = random.Random(seed)
    balls = [dict(x=0.0, y=0.0, vx=math.cos(1.0), vy=math.sin(1.0))]
    k = 0; frames = []; events = []; gums = []; combo = 0; last_break = -9; combos = []
    nextgum = [float(x) for x in os.environ.get('GUMT', '4,9.5,15,21,27').split(',')]
    for f in range(int(dur * 30)):
        t = f / 30; dt = 1 / 30
        if k >= NR: frames.append((k, [dict(b) for b in balls], list(gums), combo)); continue
        R = ring_r(k)
        scale = min(1.0, 430.0 / (R + 40))
        if t >= T0:
            if nextgum and t >= nextgum[0]:
                nextgum.pop(0)
                a = rnd.uniform(0, 6.28); rr = rnd.uniform(0.2, 0.6) * R
                gums.append(dict(x=rr * math.cos(a), y=rr * math.sin(a), kind=rnd.choice(['mush', 'acv', 'mel', 'cre']), t=t))
            spd = float(os.environ.get('SPD', '560')) / scale
            sub = 4
            for _ in range(sub):
                for b in balls:
                    b['x'] += b['vx'] * spd * dt / sub; b['y'] += b['vy'] * spd * dt / sub
                    br = BR / scale
                    while k < NR:
                        R = ring_r(k)
                        d = math.hypot(b['x'], b['y'])
                        if d + br * 0.3 < R: break
                        ang = math.atan2(b['y'], b['x'])
                        if abs(angdiff(ang, gap_angle(k, t))) < GAP / 2:
                            events.append((t, 'break', k)); k += 1
                            if t - last_break < 0.35: combo += 1
                            else:
                                if combo >= 3: combos.append((last_break, combo))
                                combo = 1
                            last_break = t
                            continue
                        nx, ny = b['x'] / d, b['y'] / d
                        dot = b['vx'] * nx + b['vy'] * ny
                        if dot > 0:
                            b['vx'] -= 2 * dot * nx; b['vy'] -= 2 * dot * ny
                            # tiny random deflection so it never loops
                            a = math.atan2(b['vy'], b['vx']) + rnd.uniform(-0.12, 0.12); b['vx'], b['vy'] = math.cos(a), math.sin(a)
                            events.append((t, 'bounce', k))
                        b['x'] = nx * (R - br * 0.3 - 0.5); b['y'] = ny * (R - br * 0.3 - 0.5)
                        break
            # gummy pickups -> clones
            for g in list(gums):
                for b in balls:
                    if math.hypot(b['x'] - g['x'], b['y'] - g['y']) < (BR + 26) / scale:
                        gums.remove(g); events.append((t, 'gum', g['kind']))
                        for q in range(2):
                            if len(balls) < int(os.environ.get('MAXB', '9')):
                                a = math.atan2(b['vy'], b['vx']) + (q + 1) * 2.1
                                balls.append(dict(x=b['x'], y=b['y'], vx=math.cos(a), vy=math.sin(a)))
                        break
            # keep gummies inside the shrinking-to-grow ring
            for g in gums:
                if math.hypot(g['x'], g['y']) > ring_r(k) * 0.7:
                    g['x'] *= 0.98; g['y'] *= 0.98
        frames.append((k, [dict(b) for b in balls], [dict(g) for g in gums], combo))
        if k >= NR and not any(e[1] == 'escape' for e in events): events.append((t, 'escape', 0))
        if k >= NR and t > [e[0] for e in events if e[1] == 'escape'][0] + 3.6: break
    return frames, events, combos
def score(seed):
    fr, ev, cb = sim(seed)
    esc = [e[0] for e in ev if e[1] == 'escape']
    if not esc: return ('stuck at', fr[-1][0], max([c for _, c in cb] + [0]))
    te = esc[0]
    big = max([c for _, c in cb] + [0])
    return round(te, 1), big, len(cb)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        print(s, score(s), flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, CB = sim(SEED)
T_ESC = [e[0] for e in EV if e[1] == 'escape'][0]
print('escape', round(T_ESC, 2), 'combos', CB[:12])
# ---------------- art
COLS = [(90, 200, 80), (255, 160, 40), (90, 150, 255), (190, 90, 240), (255, 214, 60)]
def ring_col(k):
    c = COLS[(k // 4) % 5]; lift = 30 if k % 2 else 0
    return tuple(min(255, v + lift) for v in c)
HSPR = idle('hollow', 1)
GUMS = {k: gummy(k, 4) for k in ['mush', 'acv', 'mel', 'cre']}
HVIC = vic('hollow', 420)
# starry cosmic background
rng = random.Random(4)
bgarr = np.zeros((H, W, 3), np.float32)
yy, xx = np.mgrid[0:H, 0:W]
d = np.hypot(xx - CX, yy - CY) / 900
bgarr[..., 0] = 30 + 40 * np.exp(-d * 2); bgarr[..., 1] = 14 + 20 * np.exp(-d * 2.5); bgarr[..., 2] = 50 + 70 * np.exp(-d * 1.6)
BG = Image.fromarray(np.clip(bgarr, 0, 255).astype(np.uint8)).convert('RGBA')
STARS = [(rng.uniform(0, W), rng.uniform(0, H), rng.choice([2, 3, 4]), rng.uniform(0, 6.3)) for _ in range(150)]
parts = []
ev_out = []; ev_i = 0; seen_break = 0
wr = Writer('rings_noaudio.mp4')
END = T_ESC + 3.6; NF = int(END * 30)
for f in range(NF):
    t = f / 30; k, balls, gums, combo = FR[min(f, len(FR) - 1)]
    R = ring_r(min(k, NR - 1)); scale = min(1.0, 430.0 / (R + 40))
    img = BG.copy()
    def stars(dd):
        for (sx, sy, s, ph) in STARS:
            a = int(120 + 120 * math.sin(t * 2 + ph)); dd.rectangle([sx, sy, sx + s, sy + s], fill=(255, 255, 255, max(0, a)))
    layer(img, stars)
    # new break events -> sugar shards
    while ev_i < len(EV) and EV[ev_i][0] <= t:
        te, kind, val = EV[ev_i]; ev_i += 1
        if kind == 'break':
            rr = ring_r(val); col = ring_col(val)
            for q in range(14):
                a = q * 2 * math.pi / 14 + random.random() * 0.3
                parts.append([rr * math.cos(a), rr * math.sin(a), math.cos(a) * random.uniform(120, 340), math.sin(a) * random.uniform(120, 340), te, col])
            ev_out.append((round(te, 3), 'brick_8bit' if os.path.exists(SP + 'sfx_adobe/brick_8bit.wav') else 'ding_8bit'))
        elif kind == 'gum':
            ev_out.append((round(te, 3), 'powerup_8bit'))
        elif kind == 'escape':
            ev_out.append((round(te, 3), 'victory'))
    # rings
    def rings(dd):
        lw = max(2, int(7 * scale))
        for j in range(k, NR):
            rr = ring_r(j) * scale
            if rr > 1500: break
            g0 = math.degrees(gap_angle(j, t)); gh = math.degrees(GAP) / 2
            col = ring_col(j)
            alpha = 255 if rr < 640 else int(255 * max(0, 1 - (rr - 640) / 500))
            dd.arc([CX - rr, CY - rr, CX + rr, CY + rr], g0 + gh, g0 - gh + 360, fill=col + (alpha,), width=lw)
            if lw >= 4:
                dd.arc([CX - rr + 1, CY - rr + 1, CX + rr - 1, CY + rr - 1], g0 + gh, g0 - gh + 360, fill=(255, 255, 255, alpha // 3), width=max(1, lw // 3))
    layer(img, rings)
    # shards
    def shards(dd):
        for p in parts:
            u = t - p[4]
            if u < 0 or u > 0.9: continue
            px = CX + (p[0] + p[2] * u / scale * 0.3) * scale; py = CY + (p[1] + p[3] * u / scale * 0.3) * scale + 200 * u * u
            s = 6; dd.rectangle([px - s, py - s, px + s, py + s], fill=p[5] + (int(255 * (1 - u / 0.9)),))
    layer(img, shards)
    parts = [p for p in parts if t - p[4] < 1.0]
    # gummies
    for g in gums:
        gs = GUMS[g['kind']]; gx, gy = CX + g['x'] * scale, CY + g['y'] * scale + 6 * math.sin(t * 4)
        layer(img, lambda dd: dd.ellipse([gx - 40, gy - 40, gx + 40, gy + 40], fill=(255, 240, 170, 70)))
        img.alpha_composite(gs, (int(gx - gs.width / 2), int(gy - gs.height / 2)))
    # hollows in bubbles
    if t < T_ESC:
        for b in balls:
            bx, by = CX + b['x'] * scale, CY + b['y'] * scale
            br = BR + 24
            hs = HSPR[int(t * 8) % len(HSPR)]; hs = hs.crop((27, 13, 68, 80)).resize((53, 87), Image.NEAREST)
            layer(img, lambda dd: dd.ellipse([bx - br, by - br, bx + br, by + br], fill=(160, 140, 255, 70), outline=(230, 220, 255, 220), width=4))
            img.alpha_composite(hs, (int(bx - hs.width / 2), int(by - hs.height / 2 - 2)))
            layer(img, lambda dd: dd.ellipse([bx - br + 8, by - br + 8, bx - br + 18, by - br + 18], fill=(255, 255, 255, 200)))
    # header
    layer(img, lambda dd: dd.rectangle([0, 0, W, 470], fill=(10, 6, 22, 150)))
    left = NR - min(k, NR)
    items = [(W / 2, 60, 'CAN THE HOLLOW', 60, (255, 255, 255), 8, 255), (W / 2, 145, 'ESCAPE 200 RINGS?', 56, (255, 214, 60), 8, 255),
             (W / 2, 260, str(left), 120, (255, 255, 255), 10, 255)]
    if combo >= 3 and t < T_ESC:
        items.append((W / 2 + 270, 300, f'x{combo}', 58, COLS[combo % 5], 7, 255))
    text_layer(img, items)
    if t < T_0 if False else t < T0:
        text_layer(img, [(W / 2, 1700, 'GO HOLLOW!', 54, (255, 255, 255), 8, 255)])
    if t >= T_ESC:
        u = t - T_ESC
        vf = HVIC[int(u * 8) % len(HVIC)]; img.alpha_composite(vf, (int(CX - vf.width / 2), int(1360 - vf.height)))
        text_layer(img, [(W / 2, 1450, 'HE ESCAPED!', 76, (255, 214, 60), 9, int(255 * min(1, u / 0.3)))])
        rr2 = random.Random(f)
        def conf(dd):
            for _ in range(50):
                cx_, cy_ = rr2.uniform(0, W), (rr2.uniform(-200, H) + u * 520) % H
                if cy_ > 470: dd.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr2.choice(COLS) + (255,))
        layer(img, conf)
    wr.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/r_{f:04d}.png')
wr.close()
# thin out break sounds so they don't machine-gun
out = []; last = -9
for e in sorted(ev_out):
    if e[1] in ('brick_8bit', 'ding_8bit'):
        if e[0] - last < 0.09: continue
        last = e[0]
    out.append(e)
json.dump({'events': out}, open('rings_events.json', 'w'))
print('done', round(END, 2), len(out))
