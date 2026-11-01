import os, sys
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
if os.environ.get('SHOWMAP'):
    for r in MAP: print(r)
    print('BDIST', BDIST, 'exit y', EXIT_Y, 'bottom', OY + ROWS * C)
ws = []; ex = []; who = {}
for seed in range(int(os.environ.get('B', '60'))):
    X, fr, ev, gum, B, wh, win = sim(seed)
    ws.append(win[0] if win else 99); ex.append(B['exit']['broke'][0] if B['exit']['broke'] else 99)
    if win: who[win[1]] = who.get(win[1], 0) + 1
import numpy as np; ws = np.array(ws); ex = np.array(ex)
print('win pct', [round(float(np.percentile(ws, q)), 1) for q in (10, 25, 50, 75)], 'exitbreak', [round(float(np.percentile(ex, q)), 1) for q in (10, 25, 50, 75)], who)
