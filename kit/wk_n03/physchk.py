import sys, os
sd = int(sys.argv[1]); sys.argv = ['n03.py', 'x']; os.environ['TAILSIM'] = '7'
src = open('n03.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
B, fr, ev, gum, hits = sim(sd)
worst_ov = 0; worst_wall = 0; maxjump = 0; maxacc = 0
prev = None
for f, (st, front) in enumerate(fr):
    live = [g for g in G if st[g][4] is None]
    for i in range(len(live)):
        for j in range(i + 1, len(live)):
            a, b = st[live[i]], st[live[j]]
            px, py = 2 * HS - abs(a[0] - b[0]), 2 * HS - abs(a[1] - b[1])
            if px > 0 and py > 0: worst_ov = max(worst_ov, min(px, py))
    for g in live:
        x, y = st[g][:2]
        GATES_OPEN[0] = f / 30 >= T_GO
        for (r, c) in solid_overlap(x, y):
            ox = min(x + HS - (OX + c * C), OX + c * C + C - (x - HS)); oy = min(y + HS - (OY + r * C), OY + r * C + C - (y - HS))
            worst_wall = max(worst_wall, min(ox, oy))
        if prev:
            px_, py_ = prev[g][:2]; maxjump = max(maxjump, math.hypot(x - px_, y - py_))
    prev = st
print('max box overlap px', round(worst_ov, 2), 'max wall penetration px', round(worst_wall, 2), 'max move per frame px', round(maxjump, 1))
