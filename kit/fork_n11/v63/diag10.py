import sys, os
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3: continue
    w = done[0]; tw = st[w]['done']
    if not (11.5 < tw < 15.0) or not (3.8 < caught[0] < 8.0): continue
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.0 or max(gaps) > 5.2 or not (0.3 < tw - caught[-1] < 2.6): continue
    sm = [e for e in ev if e[1] == 'smash' and e[0] < tw]
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sm or not sw: continue
    cg = st[sm[0][2]]['caught']
    if cg is not None and cg - sm[0][0] < 0.8: continue
    beats = sorted(set(round(e[0], 2) for e in ev if e[1] in ('pick', 'sleepwave', 'block', 'caught', 'smash') and e[0] <= tw))
    clash = sum(1 for i in range(len(beats) - 1) if beats[i + 1] - beats[i] < 0.6)
    other = [e[0] for e in ev if e[1] in ('pick', 'sleepwave', 'block', 'caught') and e[0] < tw]
    sep = min(abs(sm[0][0] - o) for o in other)
    print('cand', seed, 'clash', clash, 'sep', round(sep, 2), w, round(tw, 1), [round(c, 1) for c in caught], [(round(e[0], 1), e[1], e[2]) for e in ev if e[1] in ('pick', 'sleepwave', 'block', 'caught', 'smash')], flush=True)
