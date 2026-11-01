import sys, os, collections
sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C = collections.Counter()
for seed in range(int(os.environ.get('A','1')), int(os.environ.get('B','250'))):
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3: C['n']+=1; continue
    w = done[0]; tw = st[w]['done']
    E = [e for e in ev if e[0] <= tw]
    picks = {e[3]: e[0] for e in E if e[1] == 'pick'}
    blocks = [e for e in E if e[1] == 'block']
    C['blk1wave'] += len(blocks)==1 and blocks[0][3]=='wave'
    C['acv'] += 'acv' in picks
    if len(blocks)==1 and blocks[0][3]=='wave' and 'acv' in picks: C['blkgap'] += blocks[0][0]-picks['acv']>=1.2
    sm=[e[0] for e in E if e[1]=='smash']
    C['sm'] += bool(sm and 'cre' in picks and 0 < sm[0]-picks['cre'] < 1.6)
    bt = sorted([(e[0], e[1]) for e in E if e[1] in ('pick', 'smash', 'block', 'caught')])
    C['sep'] += all(a2-a1 >= (1.2 if k1=='pick' else 0.95) for (a1,k1),(a2,k2) in zip(bt,bt[1:]))
    if w=='joy': C['joywin']+=1
    C['ok'] += score(seed) is not None
print(C)
