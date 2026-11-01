import sys, os; sys.argv=['r89.py','search','0','0']; __file__ = os.path.abspath('r89.py')
src=open('r89.py').read(); src=src[:src.index("if __name__ == '__main__' and sys.argv[1] == 'search':")]
exec(compile(src,'r89','exec'))
fr, ev, outs, win = sim(int(os.environ['SEED']))
print(win, outs)
for e in ev:
    if e[1] != 'wind': print(round(e[0], 2), e[1:])
