import sys, importlib, math
M = importlib.import_module(sys.argv[1]); seed = int(sys.argv[2])
from engine import selfcheck
r = M.run(seed); fr = r['frames']; Wd = M.Wd; HS = M.HS; C = Wd.C; OX, OY = Wd.OX, Wd.OY
bad, ch, ovl = selfcheck(r, M.G, HS)
def solid(x, y, hp):
    r0, r1 = int((y - HS - OY) // C), int((y + HS - OY - 1e-6) // C); c0, c1 = int((x - HS - OX) // C), int((x + HS - OX - 1e-6) // C)
    for rr in range(max(0, r0), r1 + 1):
        for cc in range(max(0, c0), c1 + 1):
            if Wd.wall[rr, cc]: return True
            k = Wd.brk[rr, cc]
            if k and hp[k - 1] > 0: return True
    return False
pen = 0; spd = set(); mx = 0
for i, (st, tau, hp, gm) in enumerate(fr):
    for g, v in st.items():
        if v[4] is None and v[5] is None:
            spd.add(round(math.hypot(v[2], v[3]), 3))
            if solid(v[0], v[1], hp): pen += 1
            if i:
                p = fr[i - 1][0][g]
                if p[4] is None and p[5] is None: mx = max(mx, math.hypot(v[0] - p[0], v[1] - p[1]))
print('direction changes without contact', bad, '| total changes', ch, '| max box overlap px', round(ovl, 2), '| frames overlapping a wall', pen, '| speeds', spd, '| max px/frame', round(mx, 1))
