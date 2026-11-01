import sys; sys.path.insert(0, '..'); 
from dox_map import *
for s in map(int, sys.argv[1:]):
    r = run(s)
    for e in r['ev']:
        if e[1] == 'out':
            f = int(round(e[0] * 30)); f = min(f, len(r['frames']) - 1); v = r['frames'][f][0][e[2]]
            print(s, e[0], e[2], e[3], 'col', round((v[0] - OX) / C, 1), 'row', round((v[1] - OY) / C, 1), 'tau', round(r['frames'][f][1], 1))
