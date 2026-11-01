import sys, os; sys.argv=['r89.py','search','0','0']; __file__ = os.path.abspath('r89.py')
src=open('r89.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r89','exec'))
for sd in [int(x.split()[0]) for x in open('g89g.txt') if x.strip()]:
    fr, ev, outs, win = sim(sd)
    hits = [e[0] for e in ev if e[1] in ('shove', 'block')]
    gm = [e[0] for e in ev if e[1] == 'gum']
    bad = [g for g in gm[1:] if any(-0.3 < h - g < 0.8 for h in hits)]
    sp = [e[0] for e in ev if e[1] == 'splash']
    bad2 = [s_ for s_ in sp if any(0 < h - s_ < 0.9 for h in hits)]
    print(sd, 'gumclash', len(bad), 'splashclash', len(bad2), [(o[0], round(o[1], 1)) for o in outs], 'blocks', sum(1 for e in ev if e[1] == 'block'))
