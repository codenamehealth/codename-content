import sys, os, time
from dox_map import *
def summ(seed):
    t0 = time.time(); r = run(seed)
    ev = r['ev']; B = r['B']; fr = r['frames']
    br = {g: (round(B[GATE[g]]['broke'], 1) if B[GATE[g]]['broke'] else None) for g in G}
    blk = B[BLOCK]['broke']
    outs = [(round(e[0], 2), e[2], e[3]) for e in ev if e[1] == 'out']
    picks = [(round(e[0], 2), e[2]) for e in ev if e[1] == 'pick']
    win = r['win']; share = None; alive = None
    if win:
        tw = win[0]; a = int((tw - 10) * 30); b = int(tw * 30); n = k = 0
        for i in range(max(0, a), min(b, len(fr))):
            st = fr[i][0]; n += 1
            inn = [g for g, v in st.items() if v[4] is None and v[5] is None and v[1] < TOP_Y]
            if win[1] in inn and len(inn) >= 2: k += 1
        share = round(k / max(1, n), 2)
        alive = min(sum(1 for g in G if r['X'][g]['out'] is None or r['X'][g]['out'] > i / 30) for i in range(max(0, a), b))
    d = dict(seed=seed, win=(round(win[0], 2), win[1]) if win else None, gates=br, block=round(blk, 1) if blk else None, outs=outs, picks=picks,
             share10=share, min_alive10=alive, tau=round(fr[-1][1], 1), tsim=round(time.time() - t0, 1))
    return d, r
def ok(d):
    if not d['win'] or d['win'][1] not in ('joy', 'cyrus') or d['win'][0] > 59.0 or not d['block']: return False
    tw = d['win'][0]; ko = [o for o in d['outs'] if o[0] <= tw]
    gk = [o for o in ko if o[2] == 'gummy']
    return len(gk) >= 2 and all(o[0] >= 40 for o in ko) and d['min_alive10'] >= 2 and d['share10'] >= 0.6
def pre(seed):
    # cheap prefix check: nobody out before 40s and Rayleigh's gate broken
    r = run(seed, dur=40.0)
    return not any(e[1] == 'out' for e in r['ev']) and r['B'][GATE['ray']]['broke'] is not None
if __name__ == '__main__':
    for s in range(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1):
        if not pre(s): continue
        d, r = summ(s); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
