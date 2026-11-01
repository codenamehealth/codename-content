import os, sys, math
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    rc, fr, bu, po = sim(seed)
    print(seed, [(round(b_[0] - T_START, 2), b_[1], b_[4]) for b_ in bu], 'smash', [(round(q[0] - T_START, 2), q[1], q[2]) for q in sim.smashes])
