import os, sys
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(compile(src, 'r81', 'exec'))
for seed in range(8):
    rc, fr, bu = sim(seed)
    for n, s in rc.items():
        if s['out'] is None and s['caught'] is None:
            # trace position over time
            tr = [(round(f_ / FPS, 1), round(fr[f_][0][n]['x'] / C, 2), round(fr[f_][0][n]['y'] / C, 2)) for f_ in range(0, len(fr), 60)]
            print(seed, n, tr[-6:], 'DSL', DSL[cell_of(s['x'], s['y'])], 'front', round(fr[-1][1], 1))
