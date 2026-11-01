import sys, os, collections
sys.argv = ['r59.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r59.py')}
try: exec(open('r59.py').read(), g)
except SystemExit: pass
NAMES = g['NAMES']; C = collections.Counter()
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    fr, ev, ld, res = g['sim'](seed, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: C['nwin'] += 1; continue
    w = wins[0]; tw = res[w][0]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(caught) != 3 or not (11.0 < tw < 15.5): C['tw'] += 1; continue
    if not (3.8 < caught[0] < 8.0) or min(caught[1] - caught[0], caught[2] - caught[1]) < 1.0 or max(caught[1] - caught[0], caught[2] - caught[1]) > 5.5: C['gaps'] += 1; continue
    if not (0.25 < tw - caught[-1] < 2.0) or len(ld) < 3: C['last'] += 1; continue
    picks = [e for e in ev if e[1] == 'pick']
    if len(picks) < len(g['GUMS']) or len(set(e[3] for e in picks)) < 3: C['picks'] += 1; continue
    natk = sum(e[1] == 'atk' for e in ev); nsh = sum(e[1] == 'shove' for e in ev)
    if nsh < 1: C['noshove_atk%d' % natk] += 1; continue
    C['ok_' + w] += 1; print('cand', seed, w, round(tw, 2), [round(c, 1) for c in caught], [(round(e[0], 1), e[2], e[3]) for e in picks], flush=True)
print(C)
