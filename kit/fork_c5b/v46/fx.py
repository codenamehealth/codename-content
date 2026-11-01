import sys
A = sys.argv[1:]; sys.argv = ['r46.py', 'map']
src = open('r46.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__file__': __import__('os').path.abspath('r46.py'), '__name__': 'x'}
exec(compile(src, 'r46.py', 'exec'), g)
for sd in map(int, A):
    rc, fr, ld, fx, sm = g['sim'](sd)
    print(sd, sorted((round(s['out'],2), n) for n, s in rc.items()), ld)
    for e in fx: print('   ', round(e[0], 2), e[1:])
