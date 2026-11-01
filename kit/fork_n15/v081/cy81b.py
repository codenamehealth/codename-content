import os, sys, math
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
rc, fr, bu, po = sim(int(os.environ.get('SEED', '180')))
for f in range(int((T_START+7.5)*30), int((T_START+9.0)*30), 3):
    o = fr[f][0]; s = o[os.environ.get('WHO', 'cyrus')]; r_ = o['ray']
    fr_, fc_ = cell_of(s['x'], s['y'])
    print(round(f/30 - T_START, 2), 'cy', int(s['x']), int(s['y']), int(s['vx']), int(s['vy']), 'grad', round(-GX[fr_, fc_],2), round(-GY[fr_, fc_],2), 'ray', int(r_['x']), int(r_['y']), r_['shield'], 'joy', int(o['joy']['x']), int(o['joy']['y']), o['joy']['caught'], 'front', round(fr[f][1],1), 'dsl', DSL[fr_, fc_])
