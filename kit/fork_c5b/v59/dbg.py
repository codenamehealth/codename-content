import sys, math
A = sys.argv[1:]; sys.argv = ['r59.py', 'x']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x'}; exec(compile(src, 'r59.py', 'exec'), g)
for sd in map(int, A):
    fr, ev, ld, res = g['sim'](sd)
    for e in ev:
        if e[1] == 'pick' and e[3] == 'cre':
            n = e[2]; f0 = int(e[0] * 30)
            ds = []
            for f in range(f0, min(len(fr), f0 + 90), 10):
                st = fr[f][0]
                ds.append({m[:2]: round(math.hypot(st[m]['x'] - st[n]['x'], st[m]['y'] - st[n]['y'])) for m in st if m != n and st[m]['caught'] is None})
            print(sd, n, round(e[0], 1), ds)
