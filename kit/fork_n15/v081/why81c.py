import os, sys, collections
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
a, b = int(os.environ['A']), int(os.environ['B']); C_ = collections.Counter()
for seed in range(a, b):
    rc, fr, bu, po = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    r = []
    if len(outs) != 1: r.append('outs%d' % len(outs))
    elif outs[0][1] != 'ray': r.append('win_' + outs[0][1])
    if len(bu) != 4: r.append('eat%d' % len(bu))
    if [p[1] for p in po] != ['ray']: r.append('pop')
    if outs:
        race = outs[0][0] - T_START
        if not (8.3 < race < 10.8): r.append('race%.1f' % race)
    sm = getattr(sim, 'smashes', [])
    if len(sm) != 1: r.append('nosmash')
    else:
        ta = [b_[0] for b_ in bu if b_[4] == 'acv']
        if not ta or ta[0] < sm[0][0] + 0.75: r.append('acvearly')
    for n_, s_ in rc.items():
        if s_['caught'] is None: continue
        f1 = int(s_['caught'] * FPS); f0 = max(0, f1 - 18, int(fr[f1 - 1][0][n_]['sleep'] * FPS) + 1)
        if f1 - 1 - f0 < 8: continue
        st0, st1 = fr[f0][0][n_], fr[f1 - 1][0][n_]
        if math.hypot(st1['x'] - st0['x'], st1['y'] - st0['y']) < 28 * (f1 - 1 - f0) / 17: r.append('stall'); break
    if len(r) <= 1 and r: print(seed, r, flush=True)
    if not r:
        st_ = sorted([b_[0] for b_ in bu] + [p[0] for p in po]); g1 = min(y - x for x, y in zip(st_, st_[1:]))
        ev = sorted(st_ + caught); gaps = [y - x for x, y in zip(ev, ev[1:])]
        r.append('OK g1=%.2f gmin=%.2f first=%.1f tail=%.1f' % (g1, min(gaps), st_[0] - T_START, outs[0][0] - ev[-1]))
        print(seed, r, [(round(x[0] - T_START, 1), x[1], x[4]) for x in bu], flush=True)
    for x in r: C_[x[:4]] += 1
print(C_)
