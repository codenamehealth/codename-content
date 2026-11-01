import sys
src = open('r104.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x', '__file__': __file__}; exec(compile(src, 'r104', 'exec'), g)
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, G = g['sim'](s)
    print(s, {n: (x['out'] and round(x['out'], 1), x['caught'] and round(x['caught'], 1)) for n, x in G.items()}, [(round(e[0], 1), e[2]) for e in ev if e[1] == 'gum'], [e[2] for e in ev if e[1] == 'blocked'])
