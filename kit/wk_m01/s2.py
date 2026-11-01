import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
M = Maze(CFG); REF = {6: 10.5, 9: 4.5, 12: 2.5, 15: 15.5}; HS = M.HS
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
for seed in range(a0, a1):
    X, fr, ev, gum, win, ct = M.sim(seed, 18)
    gone = {}
    for c in REF:
        ts = [e[0] for e in ev if e[1] == 'break' and e[3][1] == c and e[3][0] in (4, 5, 6)]
        gone[c] = max(ts) if len(ts) == 3 else 99
    dev = max(abs(gone[c] - REF[c]) for c in REF)
    if dev > 1.5: continue
    X, fr, ev, gum, win, ct = M.sim(seed, 56)
    if not win or not (51.5 <= win[0] <= 55.0): continue
    if gum['t'] is None or not (32 <= gum['t'] <= 38.6): continue
    hits = [e for e in ev if e[1] == 'out' and e[3] == 'hit']
    if not hits: continue
    tw = win[0]
    def alive(t): st = fr[min(len(fr) - 1, int(t * FPS))][0]; return sum(1 for g in G if st[g][4] is None)
    if alive(tw - 2) < 2 or alive(tw - 10) < 2: continue
    near = 99
    for st, pr, hp, cf in fr[int(gum['t'] * FPS):]:
        h = st[gum['who']]
        if h[4] is not None: break
        for g in G:
            if g == gum['who'] or st[g][4] is not None: continue
            gap = max(abs(h[0] - st[g][0]), abs(h[1] - st[g][1])) - 2 * HS
            if 0 < gap < near: near = gap
    if near < 8: continue
    outs = [(round(e[0], 2), e[2], e[3]) for e in ev if e[1] == 'out']
    print(json.dumps(dict(seed=seed, win=(round(tw, 2), win[1]), dev=round(dev, 2), gone={c: round(v, 1) for c, v in gone.items()}, outs=outs,
                          gum=(gum['who'], round(gum['t'], 1)), near=round(near, 1), alive2=alive(tw - 2), alive10=alive(tw - 10))), flush=True)
