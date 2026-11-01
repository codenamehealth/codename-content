import os, sys
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
os.environ['SH0'] = '999'; os.environ['SIMDUR'] = '17'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
for seed in range(a0, a1):
    X, fr, ev, gum, B, wh, win = sim(seed)
    if win and win[1] == 'cyrus' and 12.0 <= win[0] <= 16.8: print(seed, round(win[0], 2), gum['who'], gum['t'] and round(gum['t'], 1), flush=True)
