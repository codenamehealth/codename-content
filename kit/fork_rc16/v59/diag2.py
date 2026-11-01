import os, sys, collections
sys.argv = ['r59.py', 'noop']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r59', 'exec'))
C = collections.Counter(); rows = []
for sd in range(int(os.environ.get('N', '60'))):
    fr, ev, ld, res = sim(sd, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    C['w%d' % len(wins)] += 1
    caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(wins) == 1: rows.append((round(res[wins[0]][0], 1), [round(c, 1) for c in caught], sum(e[1] == 'pick' for e in ev)))
print(dict(C)); print(rows[:12])
