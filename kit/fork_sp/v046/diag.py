import sys, os, collections
sys.argv = ['r46.py', 'map']
src = open('r46.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r46', 'exec'))
cnt = collections.Counter()
for sd in range(int(os.environ.get('A', '0')), int(os.environ.get('B', '150'))):
    rc, fr, ld, fx, sm = sim(sd)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    if len(outs) < 4: cnt['notfinish'] += 1; continue
    t1, w = outs[0]; t2 = outs[1][0]; r = []
    if w != 'cleo': r.append('win')
    if len([e for e in fx if e[1] == 'pick']) < len(POWS): r.append('picks')
    if not (9.0 < t1 < 14.5): r.append('t1')
    if t2 - t1 > 0.6: r.append('close')
    if len(ld) < 5: r.append('leads')
    if not any(e[1] == 'sleepwave' and len(e[3]) >= 2 for e in fx): r.append('wave')
    if sum(e[1] == 'hit' for e in fx) < 1: r.append('hit')
    if sum(e[1] in ('block', 'wblock') for e in fx) < 1: r.append('block')
    for x in r: cnt[x] += 1
    if not r: cnt['ok'] += 1
    st = [e for e in fx if e[1] == 'strike']; cnt['strikes'] += len(st)
print(dict(cnt))
