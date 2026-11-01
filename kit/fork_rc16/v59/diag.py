import os, sys, collections
sys.argv = ['r59.py', 'noop']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r59', 'exec'))
C = collections.Counter()
for sd in range(int(os.environ.get('N', '150'))):
    fr, ev, ld, res = sim(sd, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: C['nwin'] += 1; continue
    w = wins[0]
    if w != 'cleo': C['notcleo'] += 1; continue
    tw = res[w][0]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(caught) != 3: C['ncaught'] += 1; continue
    if not (11.5 < tw < 14.8): C['tw%d' % int(tw)] += 1; continue
    if not (4.0 < caught[0] < 7.2): C['c0_%d' % int(caught[0])] += 1; continue
    if min(caught[1] - caught[0], caught[2] - caught[1]) < 1.6 or max(caught[1] - caught[0], caught[2] - caught[1]) > 4.8: C['gaps'] += 1; continue
    if not (0.25 < tw - caught[-1] < 1.4): C['tail'] += 1; continue
    picks = [e for e in ev if e[1] == 'pick']
    if len(picks) < len(GUMS): C['picks%d' % len(picks)] += 1; continue
    cp = [e[3] for e in picks if e[2] == 'cleo']
    if 'cre' in cp or len(cp) > 1: C['cleopicks'] += 1; continue
    C['ok-ish'] += 1
print(dict(C))
