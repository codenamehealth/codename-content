import sys, os; sys.argv=['r85.py','search','0','0']; __file__ = os.path.abspath('r85.py')
src=open('r85.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r85','exec'))
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','12'))):
    fr, ev, pts, ld = sim(seed)
    print(seed, sorted(pts.items(), key=lambda x: -x[1]), [(round(e[0],1),) + tuple(e[1:]) for e in ev if e[1] in ('gum','shove','whiff','block','wind')], 'leads', len(ld), flush=True)
