import sys
from sim29c import *
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    try: r = stats(sd)
    except Exception as e: print(sd, 'ERR', e, flush=True); continue
    if not r: print(sd, '-', flush=True); continue
    m = {k: w for (_, w, k) in r['gp']}
    tc = next((t for (t, w, k) in r['gp'] if k == 'cre'), None); C = r['C']
    jd = (int(C[min(len(C) - 1, int(tc * FPS) + 75), NAMES.index(m['cre'])]) - int(C[int(tc * FPS), NAMES.index(m['cre'])])) if tc else None
    print(sd, round(r['tb'], 2), [(round(t, 1), w, k) for t, w, k in r['gp']], [(round(t, 1), w) for t, w in r['outs']],
          'cymax', r['cymax'], 'raymin', r['raymin'], 'sh', r['nshove'], 'credelta', jd, flush=True)
