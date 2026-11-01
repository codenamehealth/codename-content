import sys, os
os.environ.pop('BR', None); os.environ['CD2'] = os.environ.get('CD2', '1.5'); os.environ['RC2'] = os.environ.get('RC2', '38'); os.environ['PLAY'] = '1.4'
from sim29d import *
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, end, ld, outs = sim(sd, dur=26.0)
    C = np.array([np.bincount(f['T'], minlength=4) for f in fr])
    tb = next((k for k in range(len(C)) if C[k, 3] == 1 and C[k, 0] == 0 and C[k, 2] == 0), None)
    gp = [(e[0], NAMES[e[4]], e[5]) for e in ev if e[1] == 'gum']
    sv = [e for e in ev if e[1] == 'shove']
    tc = next((t for (t, w, k) in gp if k == 'cre'), None); wc = next((w for (t, w, k) in gp if k == 'cre'), None)
    up_ = None
    if tc and sv:
        a = NAMES.index(wc); f0 = int(tc * FPS); f1 = int(max(e[0] for e in sv) * FPS) + 3
        up_ = int(C[f1, a]) - int(C[f0, a])
    ok = end and NAMES[end[1]] == 'ray' and tb and 15 <= tb / 30 <= 19.6
    extra = ''
    if tb:
        P = fr[tb]; T_ = P['T']; m_ = T_ == 1; ci = int(np.where(T_ == 3)[0][0])
        extra = 'cy@%d,%d army@%d,%d lead %d' % (P['X'][ci], P['Y'][ci], P['X'][m_].mean(), P['Y'][m_].mean(), int((C[:, 3] - C[:, 1]).max()))
    print(extra, sd, 'end', end and (round(end[0], 2), NAMES[end[1]]), 'tb', tb and round(tb / 30, 2), [(o[0], NAMES[o[1]]) for o in outs], gp,
          'sh', len(sv), 'creup', up_, 'cymax', int(C[:, 3].max()), round(C[:, 3].argmax() / 30, 1), 'raymin', int(C[90:, 1].min()), 'OK' if ok else '', flush=True)
