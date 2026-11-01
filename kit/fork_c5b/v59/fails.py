import sys, collections, os
A = sys.argv[1:]; sys.argv = ['r59.py', 'x']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x'}; exec(compile(src, 'r59.py', 'exec'), g)
C = collections.Counter(); NAMES = g['NAMES']
print('GUMS', [(g['PLAT'][gg[0]][0], gg[2]) for gg in g['GUMS']])
for sd in range(int(A[0]), int(A[1])):
    fr, ev, ld, res = g['sim'](sd)
    wins = [n for n in NAMES if res[n][0] is not None]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    picks = [e for e in ev if e[1] == 'pick']; sw = [e for e in ev if e[1] == 'sleepwave']
    f = []
    if len(wins) != 1: f.append('wins%d' % len(wins))
    else:
        tw = res[wins[0]][0]
        if wins[0] != 'cleo': f.append('notcleo')
        if not (13 < tw < 21): f.append('tw')
        if caught[0] < 7: f.append('early')
        if min(caught[1] - caught[0], caught[2] - caught[1]) < 1.0: f.append('bunch')
        if not (0.4 < tw - caught[-1] < 3.0): f.append('lastgap')
    if len(picks) < len(g['GUMS']): f.append('picks%d' % len(picks))
    if not sw or max(len(e[3]) + sum(1 for b in ev if b[1] == 'block' and abs(b[0] - e[0]) < 0.01) for e in sw) < 2: f.append('sleep')
    if sum(e[1] == 'shove' for e in ev) < 1: f.append('shove')
    C.update(f)
    if len(f) <= 0: print(sd, f, {n[:2]: (round(a, 1) if a else None, round(b, 1) if b else None) for n, (a, b) in res.items()}, len(picks))
print(C)
