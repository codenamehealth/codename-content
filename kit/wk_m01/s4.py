# m01 v3 seed search: holder (Cyrus/Rayleigh) picks the gummy ~33-35s and gets the KOs; Cleo wins UNARMED with the holder alive
# and close behind; last exit cell >= 47.5s; lead change in the last 10s preferred
import sys, os, json
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
M = Maze(CFG); REF = {6: 10.5, 9: 4.5, 12: 2.5, 15: 15.5}; HS = M.HS; U = M.U
EX = [(r, 17) for r in (20, 21)]                             # path distance (cells) to the exit, ignoring bricks
DX = {e: 0 for e in EX}; q = deque(EX)
while q:
    r, c = q.popleft()
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (r + dr, c + dc)
        if 0 <= n[0] < M.ROWS and 0 <= n[1] < M.COLS and not M.is_wall(*n) and n not in DX: DX[n] = DX[(r, c)] + 1; q.append(n)
def pd(x, y): return DX.get(M.cell(x, y), 99)
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
for seed in range(a0, a1):
    if seed % 100 == 0: print(json.dumps(dict(progress=seed)), flush=True)
    X, fr, ev, gum, win, ct = M.sim(seed, 18)
    gone = {}
    for c in REF:
        ts = [e[0] for e in ev if e[1] == 'break' and e[3][1] == c and e[3][0] in (4, 5, 6)]
        gone[c] = max(ts) if len(ts) == 3 else 99
    if max(abs(gone[c] - REF[c]) for c in REF) > 1.5: continue
    X, fr, ev, gum, win, ct = M.sim(seed, 37)
    if gum['who'] not in ('cyrus', 'ray') or not (31.5 <= gum['t'] <= 37.0) or X['cleo']['out'] is not None: continue
    X, fr, ev, gum, win, ct = M.sim(seed, 57)
    if not win or win[1] != 'cleo' or not (50.0 <= win[0] <= 57.0): continue
    if gum['who'] not in ('cyrus', 'ray') or not (31.5 <= gum['t'] <= 37.0): continue
    hits = [e for e in ev if e[1] == 'out' and e[3] == 'hit']
    pass
    tw = win[0]; st = fr[-1][0]; h = st[gum['who']]
    if h[4] is not None: continue                              # holder alive at the win
    hd = pd(h[0], h[1])
    pass                                        # holder within ~1s (<= 4 cells) behind
    d4 = [e[0] for e in ev if e[1] == 'break' and e[3][1] == 16 and e[3][0] in (20, 21)]
    if len(d4) < 2: continue
    lead = None; ch = []
    for i in range(int((tw - 10) * FPS), len(fr)):
        s_ = fr[i][0]; liv = [g for g in G if s_[g][4] is None]
        L = min(liv, key=lambda g: pd(s_[g][0], s_[g][1]))
        if lead is not None and L != lead: ch.append(round(i / FPS, 1))
        lead = L
    near = 99
    for s_, pr, hp, cf in fr[int(gum['t'] * FPS):]:
        hh = s_[gum['who']]
        for g in G:
            if g == gum['who'] or s_[g][4] is not None: continue
            gap = max(abs(hh[0] - s_[g][0]), abs(hh[1] - s_[g][1])) - 2 * HS
            if 0 < gap < near: near = gap
    outs = [(round(e[0], 2), e[2], e[3]) for e in ev if e[1] == 'out']
    print(json.dumps(dict(seed=seed, win=round(tw, 2), gum=(gum['who'], round(gum['t'], 1)), outs=outs, holder_cells_behind=hd,
                          d4=[round(v, 1) for v in d4], leadchg=ch, near=round(near, 1), gone={c: round(v, 1) for c, v in gone.items()})), flush=True)
