import sys, os, runpy
sys.argv = ['r37.py', 'search', '0', '0']
# load module namespace up to search exit
src = open('r37.py').read()
cut = src.index("if len(sys.argv) > 1 and sys.argv[1] == 'search':")
ns = {'__file__': os.path.abspath('r37.py'), '__name__': 'x'}
exec(compile(src[:cut], 'r37.py', 'exec'), ns)
FR, FINS, HL, FX = ns['sim'](1184)
LEN = ns['LEN']
for n in ['joy', 'cleo', 'cyrus', 'ray']:
    tt = next((k / 30 for k, st in enumerate(FR) if st[n]['s'] >= LEN), None)
    print(n, 'turn sim', tt, 'gs', round(FR[0][n]['gs'], 1), 'LEN', LEN, 'TOT', 2 * LEN)
for k in range(160, 205, 3):
    st = FR[k]; print(round(k / 30, 2), {n: (round(st[n]['s'], 1), round(st[n]['sleep'], 2)) for n in ['cleo', 'cyrus']})
