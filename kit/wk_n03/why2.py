import os, sys, collections
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
wins = collections.Counter(); outsn = collections.Counter(); first = []
for seed in range(int(os.environ.get('B', '100'))):
    X, fr, ev, gum, B, wh, win = sim(seed)
    outs = [e for e in ev if e[1] == 'out']; outsn[len(outs)] += 1
    if outs: first.append(outs[0][0])
    if win: wins[(win[1], int(win[0]))] += 1
print('outs', sorted(outsn.items()), 'first out median', sorted(first)[len(first) // 2] if first else None)
print('wins', sum(wins.values()), sorted(wins.items()))
