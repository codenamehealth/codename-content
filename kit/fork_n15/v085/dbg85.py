import sys, os; sys.argv=['r85.py','search','0','0']; __file__ = os.path.abspath('r85.py')
src=open('r85.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r85','exec'))
fr, ev, pts, ld = sim(int(os.environ.get("SEED", "74")))
for e in ev:
    if e[1] in ('shove','wind','gum'): print(e)
for f in range(150, 175, 2): print(round(f/30,2), fr[f]['own'], fr[f]['pts'])
