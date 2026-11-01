import sys, runpy
A = sys.argv[1:]; sys.argv = ['r46.py', 'map']
src = open('r46.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__file__': __import__('os').path.abspath('r46.py'), '__name__': 'x'}
exec(compile(src, 'r46.py', 'exec'), g)
for sd in range(int(A[0]), int(A[1])):
    rc, fr, ld, fx, sm = g['sim'](sd)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    picks = [e for e in fx if e[1] == 'pick']
    sw = [len(e[3]) for e in fx if e[1] == 'sleepwave']
    print(sd, [(n, round(t, 2)) for t, n in outs], 'picks', len(picks), [e[3][:2]+e[2][:2] for e in picks], 'sw', sw, 'hit', sum(e[1]=='hit' for e in fx), 'blk', sum(e[1]=='block' for e in fx), 'sm', len(sm), 'ld', len(ld))
