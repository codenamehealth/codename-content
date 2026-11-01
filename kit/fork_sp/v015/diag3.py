import sys, os
os.environ.update(TS='0.0', TSL='1.2', GC='8,8', SA='6.5', SB='0.5', SPD='0.72')
src=open('r15.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g={'__file__':os.path.abspath('r15.py')}
exec(compile(src,'r15','exec'),g)
from collections import Counter
c=Counter(); tm=Counter()
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    rc, fr, gt, sv = g['sim'](sd)
    c[len(sv)]+=1
    for x in sv: tm[int(x[0])]+=1
print(sorted(c.items()), sorted(tm.items()))
