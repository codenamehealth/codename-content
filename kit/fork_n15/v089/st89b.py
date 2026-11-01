import sys, os; sys.argv=['r89.py','search','0','0']; __file__ = os.path.abspath('r89.py')
src=open('r89.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r89','exec'))
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','12'))):
    fr, ev, outs, win = sim(seed)
    print(seed, win, [(o[0], round(o[1],1)) for o in outs], [(round(e[0],1),e[1],e[2],e[3]) for e in ev if e[1] in ('gum','dash','dodge','block')], flush=True)
