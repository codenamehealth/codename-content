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
    r=[]
    if len(outs)!=1 or len(caught)!=3 or gt is None: r.append('shape')
    else:
        tw, win = outs[0]
        if win!='cleo': r.append('win')
        if gt[0]!=win: r.append('gum')
        elif rc[win]['behind']<1: r.append('behind')
        if not 7<tw<10.5: r.append('tw')
        if max(caught)<tw-2.5 or min(caught)<4: r.append('caught')
    if len(sv)<3 or len(set(x[2] for x in sv))<2: r.append('nsh')
    for x in r: c[x]+=1
    if not r: c['ok']+=1
    if r==['nsh']: c['only_nsh']+=1
    if r==['win']: c['only_win']+=1
print(c)
