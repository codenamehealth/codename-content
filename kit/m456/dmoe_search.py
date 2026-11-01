import sys, os, time
from dmoe_map import *
def summ(seed):
    t0 = time.time(); r = run(seed)
    outs = [(round(e[0], 2), e[2], e[3]) for e in r['ev'] if e[1] == 'out']
    win = r['win']; fr = r['frames']
    top = {}
    for i, (st, tau, hp, gm) in enumerate(fr):
        for g, v in st.items():
            if g not in top and v[4] is None and v[1] < TOP_Y: top[g] = round(i / 30, 1)
    share = None; alive_end = None; streak = 0
    if win:
        tw = win[0]; a = int((tw - 15) * 30); b = int(tw * 30); n = 0; k = 0
        for i in range(max(0, a), min(b, len(fr))):
            st = fr[i][0]; n += 1
            inn = [g for g, v in st.items() if v[4] is None and v[5] is None and v[1] < TOP_Y]
            if win[1] in inn and len(inn) >= 2: k += 1
        share = round(k / max(1, n), 2)
        alive_end = [g for g in G if r['X'][g]['out'] is None or r['X'][g]['out'] > tw]
        wi = int(tw * 30); k = 0
        for i in range(min(wi, len(fr)) - 1, 0, -1):              # unbroken run, ending at the win, with the winner and 1+ other in the top room
            st = fr[i][0]; inn = [g for g, v in st.items() if v[4] is None and v[5] is None and v[1] < TOP_Y]
            if win[1] in inn and len(inn) >= 2: k += 1
            else: break
        streak = round(k / 30, 1)
    return dict(seed=seed, win=(round(win[0], 1), win[1]) if win else None, outs=outs, top=top, share15=share, streak=streak,
                alive_at_win=alive_end, tsim=round(time.time() - t0, 1)), r
def ok(d):
    if not d['win']: return False
    tw = d['win'][0]; ko = [o for o in d['outs'] if o[0] < tw]
    pen = [o for o in ko if o[2] == 'hazard']
    return (63 <= tw <= 70 and len(d['alive_at_win']) >= 2 and d['streak'] >= 15 and len(pen) >= 2 and pen[0][0] <= 14 and pen[1][0] <= 26)
def pre(seed):
    # cheap prefix check (the sim is deterministic, so a shorter run is an exact prefix of the full one)
    r = run(seed, dur=27.0); ko = [(e[0], e[2]) for e in r['ev'] if e[1] == 'out' and e[3] == 'hazard']
    want = os.environ.get('WANT')
    return len(ko) >= 2 and ko[0][0] <= 14 and ko[1][0] <= 26 and not (want and any(g == want for _, g in ko))
if __name__ == '__main__':
    for s in range(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1):
        if not pre(s): continue
        d, r = summ(s); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
