import sys, collections, os
sys.argv = ['n03.py', 'x']
src = open('n03.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C_ = collections.Counter(); R = collections.Counter()
for sd in range(1, 300):
    B, fr, ev, gum, hits = sim(sd)
    done = [g for g in G if B[g]['done'] is not None]; caught = sorted(B[g]['caught'] for g in G if B[g]['caught'] is not None)
    C_[len(done)] += 1
    if len(done) == 1:
        w = done[0]; R['w_' + w] += 1
        if w == 'cyrus':
            tw = B[w]['done']; gaps = [b - a for a, b in zip(caught, caught[1:])]
            print(sd, GATE_COL['cyrus'], round(tw, 1), [round(c, 1) for c in caught], sum(1 for e in ev if e[1] == 'pick' and e[0] < tw))
print(C_, R)
