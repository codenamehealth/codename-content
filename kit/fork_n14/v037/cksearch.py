import sys, os
src = open('r37.py').read(); cut = src.index("if len(sys.argv) > 1 and sys.argv[1] == 'search':")
ns = {'__file__': os.path.abspath('r37.py'), '__name__': 'x'}
sys.argv = ['r37.py', 'search', '0', '0']
exec(compile(src[:cut], 'r37.py', 'exec'), ns)
LEN = ns['LEN']
for ck in [1.08 - 0.005 * i for i in range(0, 14)]:
    ns['CK'] = ck
    FR, fins, hl, fx = ns['sim'](1184)
    picks = sorted((round(e[0], 2), e[2]) for e in fx if e[1] == 'pick')
    turns = {n: next((k / 30 for k, st in enumerate(FR) if st[n]['s'] >= LEN), None) for n in ['joy', 'cleo', 'cyrus', 'ray']}
    sleeps = [(round(e[0], 2), e[2]) for e in fx if e[1] in ('sleep', 'block', 'bonk')]
    print(round(ck, 3), [(n, round(t, 2)) for t, n in fins], picks, 'turns', {k: round(v, 2) for k, v in turns.items()}, sleeps)
