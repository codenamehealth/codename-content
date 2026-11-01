import os, sys
sys.argv = ['r82.py', 'none']
src = open('r82.py').read().split("if sys.argv[1] == 'search':")[0]
exec(compile(src, 'r82', 'exec'))
for sp in (600, 640, 560):
    SPD0 = sp
    for s in range(0, 300):
        fr, br, bo, esc, gums = sim(s)
        got = sorted(g['got'] for g in gums if g['got'])
        if esc and 30 < esc < 37 and len(bo) > 55 and len(got) >= 3 and all(b - a > 1.5 for a, b in zip(got, got[1:])):
            print(sp, s, round(esc, 1), len(bo), [round(x, 1) for x in got], flush=True)
