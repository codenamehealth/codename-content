import sys
A = sys.argv[1:]; sys.argv = ['r56.py', 'x']
src = open('r56.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x'}; exec(compile(src, 'r56.py', 'exec'), g)
for sd in range(int(A[0]), int(A[1])):
    fr, ev, obs, ld, fin, mc = g['sim'](sd)
    picks = [(e[2][:2], e[3][:2]) for e in ev if e[1] == 'pick']
    sw = [len(e[3]) for e in ev if e[1] == 'sleepwave']
    print(sd, sorted((round(v, 2) if v else 99, n) for n, v in fin.items()), 'ld', len(ld), 'picks', picks, 'sw', sw, 'bonk', sum(e[1]=='bonk' for e in ev), 'st', sum(e[1] in ('smash','shove') for e in ev), 'blk', sum(e[1]=='block' for e in ev), 'mc', round(mc,1))
