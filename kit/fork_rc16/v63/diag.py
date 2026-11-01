import os, sys, collections
sys.argv = ['r63.py', 'noop']
src = open('r63.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r63', 'exec'))
C = collections.Counter(); H = collections.Counter(); T = collections.Counter(); GP = []
for sd in range(int(os.environ.get('N', '200'))):
    st, fr, ev, obs, lanes, ld = sim(sd, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    C['d%d c%d' % (len(done), len(caught))] += 1
    if len(done) == 1 and len(caught) == 3:
        H[int(caught[0])] += 1; T[int(st[done[0]]['done'])] += 1
        tw = st[done[0]]['done']
        GP.append(int(max(max(f[0][g]['x'] for g in G if f[0][g]['caught'] is None) - f[1] for f in fr[45:int(tw * FPS)]) / 100))
print(dict(C)); print('c0', sorted(H.items()), 'tw', sorted(T.items()), 'gap', sorted(collections.Counter(GP).items()))
