import sys, os, collections
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']; FPS = g['FPS']; C = collections.Counter()
for seed in range(int(os.environ.get('A', 1)), int(os.environ.get('B', 200))):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3 or done[0] != 'joy': C['notjoy'] += 1; continue
    tw = st['joy']['done']
    if not (12.3 < tw < 14.6): C['tw'] += 1; continue
    if not (4.3 < caught[0] < 7.2): C['first'] += 1; continue
    if len(ld) < 3: C['ld'] += 1; continue
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.8 or max(gaps) > 4.2 or not (0.3 < tw - caught[-1] < 2.2): C['gaps'] += 1; continue
    picks = [e for e in ev if e[1] == 'pick' and e[0] < tw]
    if len(picks) < 4: C['picks%d' % len(picks)] += 1; continue
    jb = [e[0] for e in ev if e[1] == 'block' and e[2] == 'joy']
    if not jb or min(jb) > tw - 3.0 or any(b_ > tw - 3.0 for b_ in jb): C['jb'] += 1; continue
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sw or len(sw[0][3]) + sum(1 for b in ev if b[1] == 'block' and abs(b[0] - sw[0][0]) < 0.01) < 2: C['sw'] += 1; continue
    if sum(e[1] == 'smash' for e in ev) < 1: C['smash'] += 1; continue
    C['gapmax'] += 1; print('cand', seed)
print(C)
