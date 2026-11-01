# physics self-check: overlaps, penetration, speed, dark overlap at each OUT, and steering: the fraction of frames where a box's
# velocity direction changes without a wall/brick/box contact on that frame (must be 0)
import os, sys, math
seed = int(sys.argv[1]); sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
X, fr, ev, gum, B, wh, win = sim(seed)
ov = 0; pen = 0; step = 0; spd = []; outgap = []; steer = {g: [0, 0] for g in G}
for i, (st, front, hp) in enumerate(fr):
    live = [g for g in G if st[g][4] is None]
    for a in range(len(live)):
        for b in range(a + 1, len(live)):
            p, q = st[live[a]], st[live[b]]
            ox_, oy_ = 2 * HS - abs(p[0] - q[0]), 2 * HS - abs(p[1] - q[1])
            if ox_ > 0 and oy_ > 0: ov = max(ov, min(ox_, oy_))
    for g in live:
        x, y = st[g][0], st[g][1]
        for (x0, y0, x1, y1, k) in solids_near(x, y, {kk: dict(rect=BRK0[kk]['rect'], hp=hp[kk]) for kk in BRK0}):
            px_, py_ = min(x + HS, x1) - max(x - HS, x0), min(y + HS, y1) - max(y - HS, y0)
            if px_ > 0 and py_ > 0: pen = max(pen, min(px_, py_))
        spd.append(math.hypot(st[g][2], st[g][3]))
        if i > 0 and fr[i - 1][0][g][4] is None and i / FPS > T_GO + 1 / FPS:
            step = max(step, math.hypot(x - fr[i - 1][0][g][0], y - fr[i - 1][0][g][1]))
            a0 = math.atan2(fr[i - 1][0][g][3], fr[i - 1][0][g][2]); a1 = math.atan2(st[g][3], st[g][2])
            d = abs((a1 - a0 + math.pi) % (2 * math.pi) - math.pi)
            steer[g][1] += 1
            if d > 1e-9 and not CFLAGS[i][g]: steer[g][0] += 1
print('steering (direction changes with no contact / frames):', {g: f'{a}/{b} = {a / max(1, b):.4f}' for g, (a, b) in steer.items()})
print('max box-box overlap px', round(ov, 3), '| max wall/dragon penetration px', round(pen, 3), '| max step px/frame', round(step, 2), '| speed', round(min(spd), 1), round(max(spd), 1))
