# pure-physics seed search for a contested finish (Bennett: "too obvious who wins")
import os, sys, math, json
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
src = open('n03c.py').read().split("WANT = os.environ.get('WANT'")[0]
exec(compile(src, 'n', 'exec'))
from collections import deque
EXSRC = [(r, c) for r in range(SUBR) for c in range(SUBC) if MAP[r // 2][c // 2] == 'b' and sub_open(r, c)]
DEX = {s_: 0 for s_ in EXSRC}; q_ = deque(EXSRC)
while q_:
    r, c = q_.popleft()
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n_ = (r + dr, c + dc)
        if 0 <= n_[0] < SUBR and 0 <= n_[1] < SUBC and sub_open(*n_) and n_ not in DEX and MAP[n_[0] // 2][n_[1] // 2] not in 'E': DEX[n_] = DEX[(r, c)] + 1; q_.append(n_)
def pdist(x, y): return DEX.get((int((y - OY) // H2), int((x - OX) // H2)), 999)
sh0 = float(os.environ['SH0'])
for seed in range(a0, a1):
    X, fr, ev, gum, B, wh, win = sim(seed)
    if not win or win[1] == 'cleo': continue
    tw = win[0]
    if not (14.0 <= tw <= 18.6): continue
    exh = sorted(set(h[1] for h in B['exit']['hits']))
    if len(exh) < 2: continue
    if any(gb is None or gb[0] > sh0 + 0.5 for gb in [B['gate%d' % k]['broke'] for k in range(4)]): continue
    outs = sorted((e[0], e[2]) for e in ev if e[1] == 'out')
    lead = None; cand = None; cand_t = 0; changes = []
    for i in range(int(T_GO * FPS) + 15, len(fr)):
        st = fr[i][0]; livs = [g for g in G if st[g][4] is None]
        if len(livs) < 2: break
        L = min(livs, key=lambda g: pdist(st[g][0], st[g][1]))
        if L != cand: cand, cand_t = L, i / FPS
        if cand != lead and i / FPS - cand_t >= 0.5:
            if lead is not None: changes.append(round(cand_t, 2))
            lead = cand
    def alive(t): return sum(1 for g in G if fr[min(len(fr) - 1, int(t * FPS))][0][g][4] is None)
    evt = sorted([T_GO + 0.9] + [o[0] for o in outs] + [e[0] for e in ev if e[1] in ('crack', 'break', 'pick')] + changes + [tw])
    evt = [e for e in evt if e >= T_GO + 0.9]
    gaps = [b - a for a, b in zip(evt, evt[1:])]
    dead = max(gaps) if gaps else 99
    last_out = outs[-1][0] if outs else 0
    r = dict(seed=seed, win=win[1], tw=round(tw, 2), outs=[(round(a, 1), g) for a, g in outs], lead=changes, exh=exh,
             breaker=B['exit']['broke'][1], strong=B['exit']['broke'][4], gum=(gum['who'], gum['t'] and round(gum['t'], 1)),
             alive3=alive(tw - 3), alive6=alive(tw - 6), lastout_gap=round(tw - last_out, 2), dead=round(dead, 2),
             leadlate=any(c >= tw - 5 for c in changes), sh=(sh0, os.environ['SHV'], os.environ['SHA']))
    print(json.dumps(r), flush=True)
