import sys, os
for b in range(int(sys.argv[1]), int(sys.argv[2])):
    os.environ['BR'] = str(b)
    import importlib, sim29d; importlib.reload(sim29d); from sim29d import *
    fr, ev, end, ld, outs = sim(31)
    C = np.array([np.bincount(f['T'], minlength=4) for f in fr])
    tb = next((k for k in range(len(C)) if C[k, 3] == 1 and C[k, 0] == 0 and C[k, 2] == 0), None)
    ok = end and NAMES[end[1]] == 'ray' and tb
    print(b, 'end', end and (round(end[0], 2), NAMES[end[1]]), 'tb', tb and round(tb / 30, 2), [(o[0], NAMES[o[1]]) for o in outs], [(e[0], NAMES[e[4]], e[5]) for e in ev if e[1] == 'gum'],
          'sh', [e[0] for e in ev if e[1] == 'shove'], 'joy', C[219, 0], C[219 + 120, 0], 'cymax', C[318:, 3].max(), round((318 + C[318:, 3].argmax()) / 30, 1), 'raymin', C[318:, 1].min(), 'OK' if ok else '', flush=True)
