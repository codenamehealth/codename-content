import sys, importlib, math
M = importlib.import_module(sys.argv[1]); seed = sys.argv[2]
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
pen = 0; spd = set(); mx = 0; jumps = []
S0 = {b['g']: (b['x'], b['y']) for b in M.start(M.parse_seed(seed)[0])}
for g, (x, y) in S0.items():                                            # the spawn itself must be clear of walls and other boxes
    if solid(x, y, [b['hp'] for b in Wd.B]): pen += 1
STEP = M.SPD / 30.0                                                     # max distance a box may cover in one frame
for i, (st, tau, hp, gm) in enumerate(fr):
    for g, v in st.items():
        if v[4] is None and v[5] is None:
            spd.add(round(math.hypot(v[2], v[3]), 3))
            if solid(v[0], v[1], hp): pen += 1
            p = fr[i - 1][0][g] if i else (S0[g][0], S0[g][1], 0, 0, None, None)   # frame 0 is measured from the spawn point
            if p[4] is None and p[5] is None:
                d_ = math.hypot(v[0] - p[0], v[1] - p[1]); mx = max(mx, d_)
                if d_ > STEP + 0.5: jumps.append((i, g, round(d_, 1)))
print('direction changes without contact', bad, '| total changes', ch, '| max box overlap px', round(ovl, 2), '| frames overlapping a wall', pen, '| speeds', spd,
      '| max px/frame', round(mx, 2), 'limit', round(STEP, 2), '| frames over the limit', len(jumps), jumps[:8])
