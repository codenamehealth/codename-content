import sys, os, itertools
src = open('r37.py').read(); cut = src.index("if len(sys.argv) > 1 and sys.argv[1] == 'search':")
ns = {'__file__': os.path.abspath('r37.py'), '__name__': 'x'}
sys.argv = ['r37.py', 'search', '0', '0']
exec(compile(src[:cut], 'r37.py', 'exec'), ns)
LEN = ns['LEN']; TOT = 2 * LEN; SLEEP_T = ns['SLEEP_T']; SHOVE_T = ns['SHOVE_T']
res = []
for joy, cy, ray, cl in itertools.product([148], range(200, 271, 10), range(240, 311, 10), range(500, 600, 15)):
    for ck in [1.0 + 0.01 * i for i in range(0, 10)]:
        ns['GSO'] = {'joy': joy, 'cyrus': cy, 'ray': ray, 'cleo': cl}; ns['CK'] = ck
        FR, fins, hl, fx = ns['sim'](1184)
        if fins[0][1] != 'cleo' or not (0.05 <= fins[1][0] - fins[0][0] <= 0.17): continue
        pk = sorted((e[0], e[2]) for e in fx if e[1] == 'pick')
        if len(pk) < 4 or [p[1] for p in pk] != ['joy', 'cyrus', 'ray', 'cleo']: continue
        if min(b[0] - a[0] for a, b in zip(pk, pk[1:])) < 1.3: continue
        turns = {n: next((k / 30 for k, st in enumerate(FR) if st[n]['s'] >= LEN), 99) for n in ns['NAMES']}
        sl = [e for e in fx if e[1] == 'sleep']; ts = sl[0][0] if sl else None
        if ts is None or not any(e[2] == 'cleo' for e in sl) or not any(e[2] == 'cyrus' for e in sl): continue
        if not any(e[1] == 'block' and e[2] == 'joy' for e in fx): continue
        if any(ts - 0.15 <= turns[e[2]] <= ts + SLEEP_T + 0.1 for e in sl): continue      # nobody turns asleep or right at the sleep
        bonks = [e[2] for e in fx if e[1] == 'bonk']
        if 'cyrus' not in bonks: continue
        tc = pk[3][0]
        if turns['cleo'] > tc - 1.0 or ts + SLEEP_T + 0.3 > tc - 0.6: continue           # her gummy can surface after turn + after sleep
        lead = None; ch = 0
        for st in FR[int(0.6 * 30):]:
            l = max(st, key=lambda n: st[n]['s'])
            if l != lead: ch += 1; lead = l
        if ch < 3 or hl == 'cleo': continue
        res.append((round(fins[1][0] - fins[0][0], 3), joy, cy, ray, cl, round(ck, 2), [round(p[0], 2) for p in pk], {k: round(v, 2) for k, v in turns.items()}, round(ts, 2), ch, fins[1][1], bonks))
        break
for r in sorted(res, key=lambda r: (abs(r[0] - 0.1), -r[9]))[:15]: print(r)
print(len(res))
