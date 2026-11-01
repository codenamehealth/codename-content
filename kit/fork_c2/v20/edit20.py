p='r20.py'; s=open(p).read()
rep=[
("sys.path.insert(0, '../../fork1'); from common import *\nsys.path.insert(0, '../../pixellab/safezone')",
 "SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'\nsys.path.insert(0, SP_ + 'fork1'); from common import *\nsys.path.insert(0, SP_ + 'pixellab/safezone')"),
("""from sim import play, dist, N
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 79
WIN, LOG, LEFT = play(SEED)
G = '../gen/'""","""from sim import dist, N
from sim2 import play2, trace, P0
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 71
P0['trig'] = 1
WIN, LOG, LEFT = play2(SEED, P0)
TR = trace(LOG)
# story beats (Bennett): Hollow 1 step from winning -> walled in by Cyrus -> comeback
I_LEAD = next(i for i, (h, c) in enumerate(TR) if h <= 1)
I_TRAP = next(i for i, e in enumerate(LOG) if i > I_LEAD and e[0] == 'wall' and e[1] == 'cyrus')
I_CLUTCH = next(i for i, e in enumerate(LOG) if i > I_TRAP and e[0] == 'wall' and e[1] == 'hollow')
print('beats', I_LEAD, I_TRAP, I_CLUTCH, 'turns', len(LOG))
def caption(k):
    if I_LEAD <= k <= I_TRAP: return ('1 STEP FROM WINNING...', 30, (255, 214, 60))
    if I_TRAP < k < I_CLUTCH: return ('WALLED IN!', 40, (255, 90, 90))
    if I_CLUTCH <= k < I_CLUTCH + 6: return ('COMEBACK TIME!', 40, (130, 240, 110))
    return ('EVERY WALL COSTS A GUMMY', 26, (255, 230, 170))
G = SP_ + 'fork_a2/gen/'"""),
("""    if t < T0 + 0.5: pops.append((BCX, Y0 + N * CS + 22, 'PICK A SIDE!', 52, (255, 255, 255), 8, 255))
    else: pops.append((BCX, Y0 + N * CS + 30, 'EVERY WALL COSTS A GUMMY', 26, (255, 230, 170), 5, 255))""",
"""    if t < T0 + 0.5:
        pops.append((BCX, Y0 + N * CS + 22, "YOU'RE THE HOLLOW", 44, (255, 255, 255), 8, 255))   # Hollow is the player, not a side to pick
        hx, hy = cell_c(*st['hollow']); pr = 62 + 8 * math.sin(t * 8)
        layer(img, lambda dd: dd.ellipse([hx - pr, hy - 40 - pr, hx + pr, hy - 40 + pr], outline=(255, 214, 60, 230), width=6))
    else:
        cap, csz, ccol = caption(k if k < len(LOG) else len(LOG) - 1)
        pops.append((BCX, Y0 + N * CS + 30 - (csz - 26) // 2, cap, csz, ccol, 5 if csz < 34 else 7, 255))"""),
("wr = Writer('sz20_noaudio.mp4')","wr = Writer(SP_ + 'fork_c2/v20/v20_noaudio.mp4')"),
("open('sz20_events.json', 'w')","open(SP_ + 'fork_c2/v20/v20_events.json', 'w')"),
("img.convert('RGB').resize((270, 480)).save(f'prev/sz_{f:04d}.png')","pass"),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
