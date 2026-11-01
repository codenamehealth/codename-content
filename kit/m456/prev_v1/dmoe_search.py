import sys, os, time
from dmoe_map import *
def summ(seed):
    t0 = time.time(); r = run(seed)
    outs = [(round(e[0], 1), e[2], e[3]) for e in r['ev'] if e[1] == 'out']
    win = r['win']
    # when each live box first reached the top room (rows < 17)
    top = {}
    for i, (st, tau, hp, gm) in enumerate(r['frames']):
        for g, v in st.items():
            if g not in top and v[4] is None and v[1] < OY + 17 * C: top[g] = round(i / 30, 1)
    return dict(seed=seed, win=(round(win[0], 1), win[1]) if win else None, outs=outs, top=top, tsim=round(time.time() - t0, 1)), r
if __name__ == '__main__':
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        d, r = summ(s); print(d, flush=True)
