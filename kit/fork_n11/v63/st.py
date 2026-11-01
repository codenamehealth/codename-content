import sys, os
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]
    sm = [e for e in ev if e[1] == 'smash']
    if len(done) != 1 or not sm: continue
    caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    other = [e[0] for e in ev if e[1] in ('pick', 'sleepwave', 'block', 'caught')]
    sep = min(abs(sm[0][0] - o) for o in other); cg = st[sm[0][2]]['caught']
    print(seed, done[0], round(st[done[0]]['done'], 1), [round(c, 1) for c in caught], 'sm', round(sm[0][0], 1), sm[0][2], 'sep', round(sep, 2), 'cg-sm', None if cg is None else round(cg - sm[0][0], 2), 'sw', any(e[1] == 'sleepwave' for e in ev), flush=True)
