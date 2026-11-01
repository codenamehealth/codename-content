import sys, collections, os
A = sys.argv[1:]; sys.argv = ['r63.py', 'x']
src = open('r63.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x', '__file__': os.path.abspath('r63.py')}; exec(compile(src, 'r63.py', 'exec'), g)
C = collections.Counter(); G = g['G']; WN = collections.Counter()
for sd in range(int(A[0]), int(A[1])):
    st, fr, ev, obs, lanes, ld = g['sim'](sd)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    f = []
    if len(done) != 1: f.append('done%d' % len(done))
    else:
        tw = st[done[0]]['done']; WN[done[0]] += 1
        if done[0] != 'joy': f.append('notjoy')
        if not (13 < tw < 19): f.append('tw')
        if len(caught) < 3: f.append('alive'); C.update(f); continue
        if caught[0] < 7: f.append('early')
        if min(caught[1] - caught[0], caught[2] - caught[1]) < 1.0: f.append('bunch')
        if caught[-1] < tw - 3.5: f.append('lastgap')
        if len(ld) < 4: f.append('ld')
        picks = [e for e in ev if e[1] == 'pick' and e[0] < tw]
        if len(picks) < 4: f.append('picks')
    if sum(e[1] == 'smash' for e in ev) < 1: f.append('smash')
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sw or len(sw[0][3]) + sum(1 for b in ev if b[1] == 'block' and abs(b[0] - sw[0][0]) < 0.01) < 2: f.append('sleep')
    C.update(f)
    if len(f) == 1: print(sd, f)
print(C, WN)
