import sys, os, time
from dox_map import *
WANT = os.environ.get('WANT', 'joy')
def summ(seed, verbose=False):
    t0 = time.time(); r = run(seed)
    ev = r['ev']; B = r['B']
    br = {g: (round(B[GATE[g]]['broke'], 1) if B[GATE[g]]['broke'] else None) for g in G}
    blk = B[BLOCK]['broke']
    outs = [(round(e[0], 1), e[2], e[3]) for e in ev if e[1] == 'out']
    picks = [(round(e[0], 1), e[2]) for e in ev if e[1] == 'pick']
    win = r['win']
    d = dict(seed=seed, win=(round(win[0], 1), win[1]) if win else None, gates=br, block=round(blk, 1) if blk else None, outs=outs, picks=picks,
             tau=round(r['frames'][-1][1], 1), tsim=round(time.time() - t0, 1))
    return d, r
if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for s in range(a, b):
        d, r = summ(s)
        ok = d['win'] and d['win'][1] == WANT and d['block'] and not any(o[0] < d['block'] for o in d['outs'])
        print(('OK ' if ok else '   '), d, flush=True)
