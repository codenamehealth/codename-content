import sys, os; sys.argv=['r89.py','search','0','0']
src=open('r89.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r89','exec'))
import collections
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','20'))):
    fr, ev, outs, win = sim(seed)
    c=collections.Counter(e[1] for e in ev)
    print(seed, win, [(o[0], round(o[1],1)) for o in outs], dict(c))
if os.environ.get('EVS'):
    fr, ev, outs, win = sim(int(os.environ['EVS']))
    for e in ev:
        if e[1] in ('wind','shove','whiff','splash','gum'): print(round(e[0],2), e[1:])
