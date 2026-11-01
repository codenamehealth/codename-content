import os, sys, collections
sys.argv = ['r59.py', 'noop']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r59', 'exec'))
C = collections.Counter(); keep = []
for sd in range(int(os.environ.get('N', '800'))):
    fr, ev, ld, res = sim(sd, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: continue
    C['1win'] += 1
    w = wins[0]; tw = res[w][0]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(caught) != 3: continue
    C['3c'] += 1
    picks = [e for e in ev if e[1] == 'pick']
    if len(picks) < len(GUMS): continue
    C['allpicks'] += 1
    if not (11.5 < tw < 14.8): continue
    C['tw'] += 1
    if not (4.0 < caught[0] < 7.5): continue
    C['c0'] += 1
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.4 or max(gaps) > 5.0: continue
    C['gaps'] += 1
    if not (0.25 < tw - caught[-1] < 1.4): continue
    C['tail'] += 1
    keep.append((sd, w, round(tw, 1), [round(c, 1) for c in caught], [(round(e[0], 1), e[2], e[3]) for e in picks]))
print(dict(C))
for k in keep[:15]: print(k)
