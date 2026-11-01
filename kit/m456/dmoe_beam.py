# stage A of a two-stage jitter-stream search: from BASESPEC, re-roll the stream at T and keep branches where 2+ live boxes
# sit in the top room continuously from <= t_by up to t_to. usage: dmoe_beam.py BASESPEC T a b t_by t_to
import sys
from dmoe_map import *
base, T, a, b, t_by, t_to = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
for s2 in range(a, b):
    spec = '%s:%s:%d' % (base, T, s2); r = run(spec, dur=t_to + 0.1); fr = r['frames']
    if len(fr) < int(t_to * 30): continue
    k = 0
    for i in range(int(t_to * 30) - 1, 0, -1):
        st = fr[i][0]; inn = [g for g, v in st.items() if v[4] is None and v[5] is None and v[1] < TOP_Y]
        if len(inn) >= 2: k += 1
        else: break
    start_ = t_to - k / 30
    alive = [g for g in G if r['X'][g]['out'] is None]
    print(('OK ' if start_ <= t_by else '   ') + str(dict(spec=spec, both_in_top_since=round(start_, 1), alive=alive)), flush=True)
