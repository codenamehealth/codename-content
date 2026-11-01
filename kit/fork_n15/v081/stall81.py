import os, sys, math
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    rc, fr, bu, po = sim(seed)
    for n_, s_ in rc.items():
        if s_['caught'] is None: continue
        f1 = int(s_['caught'] * FPS); f0 = max(0, f1 - 18)
        st0, st1 = fr[f0][0][n_], fr[f1 - 1][0][n_]
        dd = math.hypot(st1['x'] - st0['x'], st1['y'] - st0['y'])
        if st1['sleep'] < s_['caught'] - 0.2 and dd < 40:
            print(seed, n_, round(s_['caught'] - T_START, 2), 'pos', int(st1['x']), int(st1['y']), 'cell', int(st1['y'] // C), int(st1['x'] // C), 'moved', int(dd), 'atk', round(st1['atk'] - T_START, 2), 'others', {m: (int(fr[f1-1][0][m]['x']), int(fr[f1-1][0][m]['y'])) for m in NAMES if m != n_})
