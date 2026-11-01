import sys, os
src = open('r104c.py').read(); src = src[:src.index("if len(sys.argv) > 1 and sys.argv[1] == 'search2':")]
g = {'__name__': 'x', '__file__': os.path.abspath('r104c.py')}; sys.argv = ['r104c.py', 'x']
exec(compile(src, 'r104c', 'exec'), g)
for sd in [int(a) for a in os.environ['SEEDS'].split(',')]:
    fr, ev, G = g['sim'](sd)
    outs = {n: round(s['out'], 2) for n, s in G.items() if s['out'] is not None}
    caught = {n: round(s['caught'], 2) for n, s in G.items() if s['caught'] is not None}
    gum = {e[2]: round(e[0], 2) for e in ev if e[1] == 'gum'}
    bl = [(round(e[0], 2), e[2]) for e in ev if e[1] == 'blocked']; sl = [(round(e[0], 2), e[2]) for e in ev if e[1] == 'sleep']
    thr = [(round(e[0], 2), e[2]) for e in ev if e[1] == 'through']
    print(sd, 'out', outs, 'caught', caught, 'gum', gum, 'blocked', bl, 'sleep', sl, 'through', thr, 'score2', g['score2'](sd))
