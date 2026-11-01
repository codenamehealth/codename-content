import sys, json
cfg = json.load(open(sys.argv[1])); sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
OVR = cfg['c']; SA = cfg['SA']; SB = cfg['SB']
st, fr, ev, obs, lanes, ld = sim(2234, 18)
tp = [e[0] for e in ev if e[1] == 'pick' and e[2] == 'ray'][0]
for f in range(int((tp - 1.6) * 30), int((tp + 0.1) * 30), 3):
    s_, sx, ws = fr[f]; print(round(f / 30, 2), s_['ray']['mode'], round(s_['ray']['x']), round(sx), round(s_['ray']['x'] - sx), s_['ray']['caught'])
