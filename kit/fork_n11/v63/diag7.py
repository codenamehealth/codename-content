import sys, os
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3 or done[0] != 'joy': continue
    tw = st['joy']['done']
    if not (12.0 < tw < 15.0) or not (3.8 < caught[0] < 7.5) or len(ld) < 3: continue
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.4 or max(gaps) > 4.6 or not (0.3 < tw - caught[-1] < 2.4): continue
    picks = [e for e in ev if e[1] == 'pick' and e[0] < tw]
    if len(picks) < 3: continue
    jb = [e[0] for e in ev if e[1] == 'block' and e[2] == 'joy']
    if not jb or min(jb) > tw - 2.5: continue
    sm = [e for e in ev if e[1] == 'smash' and e[0] < tw]
    if not sm: continue
    other = [e[0] for e in ev if e[1] in ('pick', 'sleepwave', 'block', 'caught') and e[0] < tw]
    sep = min(min(abs(s[0] - o) for o in other) for s in sm)
    smg = sm[0][2]; cg = st[smg]['caught']
    if sep < 0.6 or (cg is not None and cg - sm[0][0] < 0.6) or not [e for e in ev if e[1] == "sleepwave"]: continue
    sw = [e for e in ev if e[1] == 'sleepwave']
    print(seed, round(tw, 1), [round(c, 1) for c in caught], 'picks', [(round(e[0], 1), e[2], e[3]) for e in picks], 'jb', [round(x, 1) for x in jb], 'sw', [(round(e[0], 1), e[3]) for e in sw], 'smash', [(round(s[0], 1), s[2]) for s in sm], 'sep', round(sep, 2), flush=True)
