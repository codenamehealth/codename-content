import os, sys, collections
sys.argv = ['r59.py', 'noop']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r59', 'exec'))
H = collections.Counter(); T = collections.Counter()
for sd in range(int(os.environ.get('N', '300'))):
    fr, ev, ld, res = sim(sd, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: continue
    caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    H[int(caught[0])] += 1; T[int(res[wins[0]][0])] += 1
print('c0', sorted(H.items()), 'tw', sorted(T.items()))
