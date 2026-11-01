import sys, os, collections
sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C = collections.Counter()
for seed in range(1, 400):
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3: C['n']+=1; continue
    w = done[0]; tw = st[w]['done']
    if w=='joy': C['joy']+=1; continue
    if not (11.0 < tw < 15.0): C['tw']+=1; continue
    if not (3.6 < caught[0] < 7.8): C['c0']+=1; continue
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.2 or max(gaps) > 4.6: C['gaps']+=1; continue
    if not (0.4 < tw - caught[-1] < 2.4): C['tail']+=1; continue
    kinds = [e[1] for e in ev if e[0] < tw]
    if 'sleepwave' not in kinds: C['sw']+=1; continue
    if 'smash' not in kinds: C['sm']+=1; continue
    if sum(1 for e in ev if e[1] == 'pick' and e[0] < tw) < 3: C['picks']+=1; continue
    clear = min(f[0][w]['x'] - f[1] for f in fr[int(1.5 * FPS):int(tw * FPS)])
    if clear < EDGE + 140: C['clear']+=1; continue
    C['ok']+=1; print(seed, w, round(tw,1), caught)
print(C)
