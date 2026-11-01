import sys, os, collections; sys.argv=['r89.py','search','0','0']; __file__ = os.path.abspath('r89.py')
src=open('r89.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r89','exec'))
C_ = collections.Counter()
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','100'))):
    fr, ev, outs, win = sim(seed); r = []
    if win != 'joy': r.append('win')
    if len(outs) != 3 or not (9.0 <= outs[-1][1] <= 12.6): r.append('final_t')
    ts = [o[1] for o in outs]
    if len(ts) == 3 and (ts[0] < 2.0 or min(b - a for a, b in zip(ts, ts[1:])) < 2.0): r.append('spacing')
    sh = [e for e in ev if e[1] == 'shove']
    if len(sh) < 5: r.append('fewshoves')
    if sum(1 for e in ev if e[1] == 'whiff') > 3: r.append('whiffs')
    for n, to in outs:
        if not any(e[3] == n and 0 <= to - e[0] < 1.2 for e in sh): r.append('nostrikeout'); break
    gm = [(e[2], e[3]) for e in ev if e[1] == 'gum']
    if len(gm) != 4 or len(set(n for n, k in gm)) != 4: r.append('gums%d' % len(gm))
    d = [e for e in ev if e[1] == 'dash']
    if len(d) != 1 or d[0][2] != 'cyrus' or (len(outs) > 1 and d[0][0] < outs[1][1]): r.append('dash')
    if not any(e[1] == 'dodge' and e[2] == 'joy' for e in ev): r.append('dodge')
    if not outs or outs[-1][0] != 'cyrus': r.append('lastcyrus')
    for x in r: C_[x] += 1
    if len(r) <= 1: print(seed, r, [(o[0], round(o[1], 1)) for o in outs], gm, flush=True)
print(C_)
