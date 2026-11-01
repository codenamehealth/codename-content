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
    key=(len(outs), len(sv)>=3, outs[0][1] if outs else None, bool(gt is not None and outs and gt[0]==outs[0][1]))
    c[key]+=1
    if len(outs)==1 and gt and gt[0]==outs[0][1]: print(sd, round(outs[0][0],2), outs[0][1], 'behind', rc[outs[0][1]]['behind'], 'caught', [round(x,1) for x in caught], 'shoves', [(x[0], x[1][:2]+'>'+x[2][:2]) for x in sv])
print(c)
