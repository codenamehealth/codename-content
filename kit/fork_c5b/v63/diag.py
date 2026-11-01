import sys, collections, os
A = sys.argv[1:]; sys.argv = ['r63.py', 'x']
src = open('r63.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x', '__file__': os.path.abspath('r63.py')}; exec(compile(src, 'r63.py', 'exec'), g)
C = collections.Counter(); G = g['G']
for sd in range(int(A[0]), int(A[1])):
    st, fr, ev, obs, lanes, ld = g['sim'](sd)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    picks = [e for e in ev if e[1] == 'pick']; sw = [e for e in ev if e[1] == 'sleepwave']
    print(sd, {x[:2]: ('W%.1f' % st[x]['done'] if st[x]['done'] else ('c%.1f' % st[x]['caught'] if st[x]['caught'] else '-')) for x in G}, 'ld', len(ld), 'picks', [(round(e[0], 1), e[2][:2]) for e in picks], 'sw', [len(e[3]) for e in sw], 'blk', sum(e[1] == 'block' for e in ev), 'sm', sum(e[1] == 'smash' for e in ev))
