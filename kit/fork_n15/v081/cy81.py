import os, sys, math
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
rc, fr, bu, po = sim(180)
for f in range(int((T_START+7.1)*30), int((T_START+8.7)*30), 3):
    s = fr[f][0]['cyrus']; c = fr[f][0]['cleo']
    print(round(f/30 - T_START, 2), int(s['x']), int(s['y']), int(math.hypot(s['vx'], s['vy'])), s['caught'], 'cleo', int(c['x']), int(c['y']), round(c['sleep'] - T_START, 2))
