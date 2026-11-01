from sim import *
import sys
res=[]
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    win, log, left = play(seed)
    if win != 'hollow': continue
    nw = {'hollow': sum(1 for e in log if e[0]=='wall' and e[1]=='hollow'), 'cyrus': sum(1 for e in log if e[0]=='wall' and e[1]=='cyrus')}
    # hopeless moment: replay distances
    P = {'hollow': (N-1,4), 'cyrus': (0,4)}; walls=set(); worst=0
    for e in log:
        if e[0]=='move': P[e[1]] = e[3]
        if e[0]=='wall': walls.add(e[2])
        gap = dist(P['hollow'],0,walls) - dist(P['cyrus'],N-1,walls); worst=max(worst,gap)
    if nw['cyrus'] >= 6 and worst >= 4 and 34 <= len(log) <= 56:
        print(seed, len(log), nw, 'worst gap', worst, flush=True)
