# DMOEx9VvQTm recreation: staircase, rising water, pencil-tip hazards, one-box exit slot in the top room's ceiling corner
import math, random, os
from engine import World, sim
C = 11; COLS, ROWS = 94, 84; OX = (1080 - COLS * C) // 2; OY = 468
G = ['joy', 'cleo', 'cyrus', 'ray']
HS = 19; SPD = float(os.environ.get('SPD', '285'))
Wd = World(COLS, ROWS, C, OX, OY)
LEFT = [(77, 82, 1), (65, 77, 13), (53, 65, 26), (41, 53, 40), (30, 41, 53), (18, 30, 66), (6, 18, 79)]   # (row0, row1, corridor left x)
for r0, r1, lx in LEFT: Wd.floor(lx, r0, 93, r1)
RIGHT = [(71, 82, 42), (60, 71, 50), (50, 60, 59), (38, 50, 68), (27, 38, 76), (17, 27, 85)]           # step blocks: rows [top, next) right of x
PENCILS = []
for i, (top, nxt, rx) in enumerate(RIGHT):
    Wd.solid(rx, top, 93, nxt - 4)                        # the step block
    # slot under it (4 rows) holds the pencil: body solid, tip (cone) a hazard at the slot mouth
    Wd.solid(rx + 3, nxt - 3, 92, nxt - 2)                # body (one cell high, centred in the slot)
    Wd.hazard(rx + 1, nxt - 3, rx + 3, nxt - 2, 'pencil%d' % i)
    PENCILS.append(dict(i=i, x0=rx + 1, x1=92, row=nxt - 3))
Wd.floor(85, 1, 89, 6)                                    # exit slot in the top room's ceiling corner
Wd.exits.append(Wd.px(85, 1, 89, 6))
VW = float(os.environ.get('VW', '11.8'))
t_w = Wd.seg(0, 1, 94, 82, '-y', 0.0, VW)                # water rises over the whole board (it only shows on floor)
FLOOD_T0 = float(os.environ.get('FT0', '0.3'))
def start(seed):
    rnd = random.Random(seed * 11 + 3)
    a = math.radians(rnd.uniform(-58, -32)); b = math.radians(rnd.uniform(-75, -20))
    out = []
    for k, g in enumerate(G):
        aa = a if k < 3 else b
        out.append(dict(g=g, x=OX + 1 * C + HS + 1 + k * 2 * HS + k * 0.5, y=OY + 82 * C - HS - 1, vx=SPD * math.cos(aa), vy=SPD * math.sin(aa)))
    return out
def run(seed, dur=None):
    return sim(Wd, start(seed), seed, dur or float(os.environ.get('DUR', '78')), SPD, HS, flood_t0=FLOOD_T0,
               jitter=float(os.environ.get('JIT', '0.026')), post_win=float(os.environ.get('POST', '3.0')))
