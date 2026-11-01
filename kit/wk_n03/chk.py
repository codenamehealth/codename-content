import os, sys
seed = int(sys.argv[1]); sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03b.py'
src = open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
os.environ['TAILSIM'] = '4'
X, fr, ev, gum, B, wh = sim(seed)
ov = 0; pen = 0; step = 0; spd = []
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
        if i > 0 and fr[i - 1][0][g][4] is None:
            dx, dy = x - fr[i - 1][0][g][0], y - fr[i - 1][0][g][1]; step = max(step, math.hypot(dx, dy))
        spd.append(math.hypot(st[g][2], st[g][3]))
print('max box-box overlap px', round(ov, 3), '| max wall penetration px', round(pen, 3), '| max step px/frame', round(step, 2), '| speed min/max', round(min(spd), 1), round(max(spd), 1))
