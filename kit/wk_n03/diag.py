import sys, collections
sys.argv = ['n03.py', 'x']
src = open('n03.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C_ = collections.Counter()
for sd in range(1, 80):
    B, fr, ev, gum, hits = sim(sd)
    done = [g for g in G if B[g]['done'] is not None]; caught = sorted((round(B[g]['caught'],1), g) for g in G if B[g]['caught'] is not None)
    npk = sum(1 for e in ev if e[1]=='pick')
    C_[(tuple(done), len(caught))] += 1
    if sd < 15: print(sd, done, [round(B[g]['done'],1) for g in done], caught, npk)
print(C_)
