import sys, os, collections
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']; C = collections.Counter()
for seed in range(1, int(os.environ.get('N', '200'))):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    C['d%d_c%d' % (len(done), len(caught))] += 1
    if len(done) == 1 and len(caught) == 3: C['w_' + done[0]] += 1; C['tw%d' % int(st[done[0]]['done'])] += 1; C['c0_%d' % int(caught[0])] += 1
print(sorted(C.items()))
