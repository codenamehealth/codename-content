import sys; sys.path.insert(0, '..')
from common7 import *
import math, random
K = 4; FOOTY = 78 * K
SRUN = seq(PL + 'race/cleo_run', K); SRUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in SRUN]
FRUN = seq(PL + 'maze/anim/cleo_frun', K)
SLIDE = seq(PL + 'maze/anim/cleo_slide', K, 1, 8); SLIDEL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in SLIDE]
IDLE = idle('cleo', K)
GUM = gummy('cre', 4)
BG = bg_frames('vit_hd.gif', (W, H), box=(420, 0, 1028, 1080), step=2, bright=0.95)
# ground shading layer
GROUND = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(GROUND)
for y in range(1000, H):
    a = int(min(110, (y - 1000) * 0.14)); gd.line([(0, y), (W, y)], fill=(30, 20, 10, a))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 3
rng = random.Random(SEED)
ROW = [(240, 1560), (540, 1560), (840, 1560)]
T_TUCK, T_MOVE0 = 1.6, 2.4
moves = []; t = T_MOVE0; pos = list(ROW); holder = 1
durs = [1.05, 1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.66, 0.62, 0.6]
for k, dur in enumerate(durs):
    last = k == len(durs) - 1
    if last: tgt = list(ROW); rng.shuffle(tgt)
    else:
        tgt = []
        for i in range(3):
            for _ in range(50):
                p = (rng.uniform(190, 890), rng.uniform(1230, 1720))
                if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 260 for q in tgt): break
            tgt.append(p)
    ctrl = []
    for i in range(3):
        a, b = pos[i], tgt[i]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]), b[0] - a[0]; L = math.hypot(nx, ny) or 1
        bend = rng.uniform(-0.45, 0.45) * math.hypot(b[0] - a[0], b[1] - a[1])
        ctrl.append((mx + nx / L * bend, my + ny / L * bend))
    moves.append((t, dur, list(pos), tgt, ctrl)); pos = tgt; t += dur + 0.08
T_END = t + 0.1
FINAL = pos  # holder index stays 1 (cleo identity); final slot of cleo 1:
slot_of = {i: min(range(3), key=lambda s: abs(ROW[s][0] - FINAL[i][0])) for i in range(3)}
print('holder ends in slot', 'ABC'[slot_of[holder]], 'T_END', round(T_END, 2))
DUR = T_END + 3.4
def state(t):
    """positions, velocities per cleo"""
    for (t0, dur, a, b, c) in moves:
        if t0 <= t < t0 + dur + 0.08:
            u = min(1, (t - t0) / dur); s = u * u * (3 - 2 * u); ds = 6 * u * (1 - u) / dur
            out = []
            for i in range(3):
                x = (1 - s) ** 2 * a[i][0] + 2 * (1 - s) * s * c[i][0] + s * s * b[i][0]
                y = (1 - s) ** 2 * a[i][1] + 2 * (1 - s) * s * c[i][1] + s * s * b[i][1]
                vx = (2 * (1 - s) * (c[i][0] - a[i][0]) + 2 * s * (b[i][0] - c[i][0])) * ds
                vy = (2 * (1 - s) * (c[i][1] - a[i][1]) + 2 * s * (b[i][1] - c[i][1])) * ds
                out.append((x, y, vx if u < 1 else 0, vy if u < 1 else 0))
            return out
    if t < T_MOVE0: return [(p[0], p[1], 0, 0) for p in ROW]
    return [(p[0], p[1], 0, 0) for p in FINAL]
wr = Writer('v74_noaudio.mp4'); ev = []; dist = [0.0] * 3; prev = None; sliding = [False] * 3
for (t0, dur, a, b, c) in moves: ev.append((round(t0, 3), 'whoosh_8bit'))
for f in range(int(DUR * FPS)):
    t = f / FPS; st = state(t)
    img = BG[int(t * 4) % len(BG)].copy(); img.alpha_composite(GROUND)
    if prev:
        for i in range(3): dist[i] += math.hypot(st[i][0] - prev[i][0], st[i][1] - prev[i][1])
    prev = st
    # slide only while passing through another Cleo: the faster one slides
    for i in range(3):
        sp = math.hypot(st[i][2], st[i][3]); near = False
        for j in range(3):
            if j != i and math.hypot(st[i][0] - st[j][0], (st[i][1] - st[j][1]) * 1.4) < 170 and sp > math.hypot(st[j][2], st[j][3]) and sp > 200: near = True
        if near and not sliding[i]: ev.append((round(t, 3), 'jump'))
        sliding[i] = near
    layer(img, lambda dd: [dd.ellipse([x - 66, y - 14, x + 66, y + 14], fill=(0, 0, 0, 90)) for (x, y, vx, vy) in st])
    for i in sorted(range(3), key=lambda i: st[i][1]):
        x, y, vx, vy = st[i]; sp = math.hypot(vx, vy)
        if sp < 30: spr = IDLE[(int(t * 8) + i * 2) % len(IDLE)]
        elif sliding[i]: spr = (SLIDEL if vx < 0 else SLIDE)[min(6, int(t * 14) % 7)]
        elif vy > 0.75 * sp: spr = FRUN[int(dist[i] / 30) % 8]
        else: spr = (SRUNL if vx < 0 else SRUN)[int(dist[i] / 30) % 8]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOTY)))
    # the gummy: shown, then tucked behind the middle Cleo's shield
    if t < T_TUCK + 0.45:
        gx, gy = 540, 1200 + 10 * math.sin(t * 4)
        if t > T_TUCK:
            u = (t - T_TUCK) / 0.45; gx, gy = 540 - 50 * u, 1200 + 110 * u; sc = 1 - 0.7 * u
            g = up(GUM, sc) if sc > 0.3 else up(GUM, 0.3)
        else: g = GUM
        layer(img, lambda dd: dd.ellipse([gx - 80, gy - 80, gx + 80, gy + 80], fill=(255, 200, 220, 50)))
        img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    if abs(t - T_TUCK) < 0.5 / FPS: ev.append((round(t, 3), 'twinkle'))
    # header text
    if t < T_MOVE0: msg, col = 'Remember the gummy', (255, 255, 255)
    elif t < T_END: msg, col = 'Watch carefully!!', (255, 214, 60)
    elif t < T_END + 1.4: msg, col = 'Where is the gummy?', (255, 255, 255)
    else: msg, col = 'Comment A, B or C', (255, 214, 60)
    layer(img, lambda dd: dd.rounded_rectangle([60, 200, W - 60, 330], 22, fill=(16, 12, 24, 190), outline=(255, 214, 60, 255), width=4))
    text_layer(img, [(W / 2, 240, msg, 46, col, 6, 255)])
    if T_MOVE0 <= t < T_END:
        k = sum(1 for m in moves if m[0] <= t); spd = ['', 'x1', 'x1', 'x1.5', 'x1.5', 'x2', 'x2', 'x2', 'x3', 'x3', 'x3', 'x3'][min(k, 11)]
        text_layer(img, [(W / 2, 380, f'SPEED {spd}', 30, (255, 255, 255), 4, 220)])
    if t >= T_END:
        a = int(255 * min(1, (t - T_END) / 0.3))
        for s, L in enumerate('ABC'):
            text_layer(img, [(ROW[s][0], ROW[s][1] + 40, L, 64, (255, 214, 60), 8, a)])
        if abs(t - T_END) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v74_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
