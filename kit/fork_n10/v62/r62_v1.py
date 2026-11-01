# #62 "Which gummy makes it fall?" Oct 29 n10: real physics tower (phys62.py). Run: python3 r62.py  [FRAMES=a,b,c for stills]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from phys62 import *
sys.path.insert(0, SPD + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WHICH GUMMY', 'MAKES IT FALL?'], accent=1)
OFFS = [0, 6.9, 10.8, 15.4, 22.3, 26.5, 30.7, 46.4]   # searched (phys62.py seed 61 #63): 7 settle, #8 lands, stack leans then goes over
if os.environ.get('OFFS'): OFFS = [float(x) for x in os.environ['OFFS'].split(',')]
FR_, LAND, GH = sim(OFFS, HB + 20, 13.0)
print('land', [round(l, 2) for l in LAND], 'ground', GH, 'HB', HB)
def state(t): return FR_[max(0, min(len(FR_) - 1, int(round((t - TD[0]) * FPS)) - 1))]
# TIMBER: the first frame after #8 lands where any gummy in the stack has tipped past 0.3 rad
T_TIMBER = None
for f in range(len(FR_)):
    t = TD[0] + (f + 1) / FPS
    if t > LAND[7] and any(st and abs(st[2]) > 0.25 for st in FR_[f][1:7]): T_TIMBER = t; break   # the stack itself tips (not #8 alone)
T_END = GH[0] + 2.4; N = int(round(T_END * FPS))
print('timber', round(T_TIMBER, 2), 'end', round(T_END, 2), 'N', N)
BG0 = bg_frames('hub.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.8)
SH = 300
BG = []
for b in BG0:
    nb = Image.new('RGBA', (W, H)); nb.paste(b, (0, -SH)); nb.paste(b.crop((0, H - SH, W, H)), (0, H - SH)); BG.append(nb)
LBL = {'acv': 'ACV', 'cre': 'CREATINE', 'mush': 'MUSHROOM', 'mel': 'MELATONIN'}    # no 'ACV GUMMY' tags
LCOL = {'acv': (120, 200, 90), 'cre': (110, 160, 255), 'mush': (255, 160, 50), 'mel': (205, 125, 245)}
IDL = {g: idle(g, 4) for g in WATCH}
PAN = {g: seq(PL + f'maze/anim/{g}_panic', 4, 1) for g in WATCH}
# sounds from the sim: a soft squish when each gummy lands, thud when the first one hits the ground
ev = [(round(l, 3), 'squish') for l in LAND if l > 0]
GHIT = []
for i in range(len(SEQ)):
    for f in range(len(FR_)):
        st = FR_[f][i]
        if st and st[1] + SPR[SEQ[i]].height / 2 > FLOOR - 6: GHIT.append(TD[0] + (f + 1) / FPS); break
GHIT.sort()
ev += [(round(T_TIMBER, 3), 'boing'), (round(GHIT[0], 3), 'boom')]
_lt = GHIT[0]
for x in GHIT[1:]:
    if x - _lt >= 0.25: ev.append((round(x, 3), 'stomp_8bit')); _lt = x
def frame(f):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.ellipse([CX - 120, FLOOR - 18, CX + 120, FLOOR + 18], fill=(0, 0, 0, 90)))
    img.alpha_composite(PED, (CX - PED.width // 2, FLOOR - PED.height))
    st = state(t)
    sprites = []
    for i, k in enumerate(SEQ):
        if st[i] is None: continue
        x, y, ang = st[i][:3]; s = SPR[k].rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
        sprites.append((s, (int(round(x - s.width / 2)), int(round(y - s.height / 2)))))
    for g, (wx, wy) in sorted(WATCH.items(), key=lambda kv: kv[1][1]):
        fr = PAN[g][int(t * 10) % len(PAN[g])] if T_TIMBER + 0.2 < t < T_TIMBER + 2.4 else IDL[g][int(t * 6) % 6]
        layer(img, lambda d: d.ellipse([wx - 64, wy - 12, wx + 64, wy + 12], fill=(0, 0, 0, 80)))
        img.alpha_composite(fr, (int(wx - fr.width / 2), int(wy - 78 * 4)))
    for s, p in sprites: img.alpha_composite(s, p)     # gummies in front of the watchers (the pile lands at their feet)
    cur = [i for i in range(len(SEQ)) if TD[i] - 0.1 <= t] if t < T_TIMBER else []
    if cur:
        i = cur[-1]; k = SEQ[i]; u = t - TD[i] + 0.1; pop = 1.0 if u > 0.12 else 0.75 + 2 * u
        text_layer(img, [(802, 916, f'#{i + 1}', int(64 * pop), (255, 255, 255), 9, 255), (802, 998, LBL[k], 44, LCOL[k], 8, 255)])
    if t >= T_TIMBER:
        u = t - T_TIMBER; sc = min(1, u / 0.15)
        d = ImageDraw.Draw(img)
        ctext(d, CX + int(6 * math.sin(u * 40) * max(0, 1 - u)), 540, 'TIMBER!', F(int(96 * (0.6 + 0.4 * sc))), (240, 80, 70), 9)
    img.alpha_composite(HOOK)
    return img
if __name__ == '__main__':
    if os.environ.get('FRAMES'):
        for f in [int(x) for x in os.environ['FRAMES'].split(',')]: frame(f).convert('RGB').save(f'k_{f}.png')
        sys.exit()
    w = Writer('v62_noaudio.mp4')
    for f in range(N): w.write(frame(f))
    w.close(); json.dump({'events': sorted(ev)}, open('v62_ev.json', 'w')); print('done', N / FPS, N)
