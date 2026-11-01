# greedy stream search: extend a base spec stage by stage (re-roll at T, keep the first stream where 2+ live boxes stay in the
# top room through T+H), then search the final stream for the win. Each candidate is still one plain deterministic sim.
import sys
from dmoe_map import *
from dmoe_search import summ, ok
spec = sys.argv[1]; Ts = [float(x) for x in sys.argv[2].split(',')]; H = float(sys.argv[3]); TF = sys.argv[4]; WANT = sys.argv[5]
def holds(r, t0, t1):
    fr = r['frames']
    if len(fr) < int(t1 * 30): return False
    for i in range(int(t0 * 30), int(t1 * 30)):
        st = fr[i][0]; inn = [g for g, v in st.items() if v[4] is None and v[5] is None and v[1] < TOP_Y]
        if len(inn) < 2: return False
    return r['win'] is None
for T in Ts:
    for s in range(1, 400):
        cand = '%s:%g:%d' % (spec, T, s); r = run(cand, dur=T + H + 0.1)
        if holds(r, T, T + H): spec = cand; print('stage', cand, flush=True); break
    else:
        print('stuck at', T, flush=True); sys.exit()
for s in range(1, 1500):
    cand = '%s:%s:%d' % (spec, TF, s); d, r = summ(cand)
    good = ok(d) and d['win'][1] == WANT
    print(('OK ' if good else '   ') + str(d), flush=True)
    if good: break
