import sys, runpy
sys.argv = ['r97.py', 'search', '0', '0']
src = open('r97.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'an'}; exec(compile(src, 'r97', 'exec'), g)
for seed in [204]:
    fr, ev, fin, ld = g['sim'](seed)
    print('seed', seed, fin, 'leads', ld)
    sc = {k: 0 for k in g['G4']}
    for (te, gg, kind, ix) in sorted(ev):
        if kind != 'slime': sc[gg] += 1
        if te > g['T_END'] - 3: print('  %.2f (%.2f to 0:00) %s %s -> %s' % (te - g['OFF'], g['T_END'] - te, gg, kind, dict(sc)))
    # items alive at the buzzer
    fi = int(round(g['T_END'] * g['FPS'])); st, items = fr[fi - 1]
    print('  in the air at the buzzer:', {k: [(round(it['y']), it['kind']) for it in v if it['alive']] for k, v in items.items()})
