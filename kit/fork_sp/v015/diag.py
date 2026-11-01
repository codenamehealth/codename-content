import sys, os
os.environ.update(TS='0.0', TSL='1.2', GC='8,8', SA='6.5', SB='0.5', SPD='0.72')
src=open('r15.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g={'__file__':os.path.abspath('r15.py')}
exec(compile(src,'r15','exec'),g)
from collections import Counter
c=Counter()
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    rc, fr, gt, sv = g['sim'](sd)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    c['shoves%d' % len(sv)] += 1
    c['outs%d' % len(outs)] += 1
    if outs: c['win_' + outs[0][1]] += 1
    if gt and outs and gt[0] == outs[0][1]: c['gumwin'] += 1
    if len(sys.argv) > 3: print(sd, [(round(o[0],2), o[1]) for o in outs], gt, [(x[0], x[1][:2]+'>'+x[2][:2]) for x in sv], g['spacing'](fr))
print(c)
