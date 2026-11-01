import sys, os, collections
sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C = collections.Counter()
for seed in range(int(os.environ.get('A','1')), int(os.environ.get('B','300'))):
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    C[(len(done), len(caught))] += 1
    if len(done)==1 and len(caught)==3:
        tw = st[done[0]]['done']; C['tw%d' % int(tw)] += 1; C['c0_%d' % int(caught[0])] += 1
        kinds=[e[1] for e in ev if e[0]<tw]; C['sw'] += 'sleepwave' in kinds; C['sm'] += 'smash' in kinds; C['w_'+done[0]]+=1
print(C)
