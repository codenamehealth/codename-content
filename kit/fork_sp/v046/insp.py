import sys, os
seeds = [int(x) for x in sys.argv[1:]]; sys.argv = ['r46.py', 'map']
src = open('r46.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r46', 'exec'))
for sd in seeds:
    rc, fr, ld, fx, sm = sim(sd)
    outs = sorted((round(s['out'] / SPD, 2), n) for n, s in rc.items() if s['out'] is not None)
    print(sd, 'outs(video)', outs, 'spacing', spacing(fr, fx))
    print('  fx(video t):', [(round(e[0] / SPD, 2), e[1], e[2], e[3] if e[1] != 'sleepwave' else e[3]) for e in fx])
    print('  stamps:', [(round(a / SPD, 2), round(b / SPD, 2), round(d / SPD, 2)) for a, b, d in sched([e[0] for e in fx if e[1] in ('pick', 'block', 'smash')])])
