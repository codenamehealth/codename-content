import os, sys
seed = int(sys.argv[1]); sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
X, fr, ev, gum, B, wh, win = sim(seed)
ov = 0; pen = 0; step = 0; spd = []; outgap = []
sh = (float(os.environ.get('SH0', '6')), float(os.environ.get('SHV', '2')), float(os.environ.get('SHA', '0.2')))
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
            step = max(step, math.hypot(x - fr[i - 1][0][g][0], y - fr[i - 1][0][g][1]))
        spd.append(math.hypot(st[g][2], st[g][3]))
for e in ev:                                                       # how deep the dark is into each caught box on its OUT frame
    if e[1] != 'out': continue
    i = int(round(e[0] * FPS)); x, y = fr[i][0][e[2]][:2]; front = fr[i][1]; best = 0
    r0, r1 = int((y - HS - OY) // H2), int((y + HS - 1 - OY) // H2); c0, c1 = int((x - HS - OX) // H2), int((x + HS - 1 - OX) // H2)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            dv = DIST.get((r, c))
            if dv is None or dv >= front: continue
            a0, b0, a1, b1 = sub_rect(r, c, min(1.0, front - dv))
            best = max(best, min(min(a1, x + HS) - max(a0, x - HS), min(b1, y + HS) - max(b0, y - HS)))
    outgap.append((e[2], round(e[0], 2), round(best, 1)))
print('max box-box overlap px', round(ov, 3), '| max wall/dragon penetration px', round(pen, 3), '| max step px/frame', round(step, 2), '| speed', round(min(spd), 1), round(max(spd), 1), '| dark overlap at each OUT (px)', outgap)
