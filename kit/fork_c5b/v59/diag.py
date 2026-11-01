import sys
A = sys.argv[1:]; sys.argv = ['r59.py', 'x']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x'}; exec(compile(src, 'r59.py', 'exec'), g)
for sd in range(int(A[0]), int(A[1])):
    fr, ev, ld, res = g['sim'](sd)
    picks = [(round(e[0],1), e[2][:2], e[3][:2]) for e in ev if e[1] == 'pick']
    sw = [len(e[3]) for e in ev if e[1] == 'sleepwave']
    print(sd, {n[:2]: ('W%.1f' % a if a else ('c%.1f' % b if b else '-')) for n, (a, b) in res.items()}, 'ld', len(ld), 'picks', picks, 'sw', sw, 'sh', sum(e[1]=='shove' for e in ev), 'blk', sum(e[1]=='block' for e in ev))
print('GUMS', [(g[0], g['__class__'] if False else g[2], g2) for g, g2 in []])
print('GUMS', [(gg[0], g['PLAT'][gg[0]][0], round(gg[1]), gg[2]) for gg in g['GUMS']])
