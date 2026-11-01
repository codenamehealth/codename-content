# pure-physics seed search: winner != cleo (Cyrus preferred), catches spread, lead changes, no dead stretch
import os, sys, math
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
    if not (13.5 <= tw <= 16.8): continue
    outs = sorted(e[0] for e in ev if e[1] == 'out')
    if len(outs) < 2 or outs[0] > 6.8: continue
    if any(gb is None or gb[0] > sh0 + 0.5 for gb in [B['gate%d' % k]['broke'] for k in range(4)]): continue
    # leader by path distance to the exit (held 0.5s to count)
    lead = None; cand = None; cand_t = 0; changes = []
    for i in range(int(T_GO * FPS) + 15, len(fr)):
        st = fr[i][0]; livs = [g for g in G if st[g][4] is None]
        if len(livs) < 2: break
        L = min(livs, key=lambda g: pdist(st[g][0], st[g][1]))
        if L != cand: cand, cand_t = L, i / FPS
        if cand != lead and i / FPS - cand_t >= 0.5:
            if lead is not None: changes.append(round(i / FPS, 1))
            lead = cand
    evt = sorted([T_GO] + outs + [e[0] for e in ev if e[1] in ('crack', 'break', 'pick')] + changes + [tw])
    dead = max(b - a for a, b in zip(evt, evt[1:]))
    sp = min(b - a for a, b in zip(outs, outs[1:]))
    print(seed, win[1], round(tw, 2), 'outs', [round(o, 1) for o in outs], 'leadchg', changes, 'dead', round(dead, 1), 'minsp', round(sp, 1),
          'gum', gum['who'], gum['t'] and round(gum['t'], 1), 'exit', B['exit']['broke'] and (round(B['exit']['broke'][0], 1), B['exit']['broke'][1]), flush=True)
