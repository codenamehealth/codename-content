# m06 DMOEx9VvQTm recreation: staircase, rising water, pencil-tip hazards, one-box exit slot in the top room's ceiling corner.
# v2 layout: reference proportions. Reference board x 40-1040, y 200-1500 -> ours x 40-1040, y 250-1500 (x 1:1, y 0.9615).
# Grid C=10: col = (ref_x - 40) / 10, row = (ref_y - 200) * 0.09615.
import math, random, os
from engine import World, sim, parse_seed
C = 10; COLS, ROWS = 100, 125; OX = 40; OY = 250
G = ['joy', 'cleo', 'cyrus', 'ray']
HS = int(os.environ.get("HS", "23")); SPD = float(os.environ.get('SPD', '277'))          # reference 277 px/s on the same 1000 px board width; 44 px boxes (ref 40)
Wd = World(COLS, ROWS, C, OX, OY)
# left (upper) wall steps: corridor left edge per row band (ref x 40,180,...,880 at y 1400-1500, 1215-1400, ...)
LEFT = [(115, 125, 0), (98, 115, 14), (80, 98, 28), (62, 80, 42), (44, 62, 56), (26, 44, 70), (9, 26, 84)]
for r0, r1, lx in LEFT: Wd.floor(lx, r0, COLS, r1)
# right step blocks (top row, bottom row, left col); under each a 5-row slot holding a pencil (tip at the block's inner corner)
RIGHT = [(108, 120, 45), (91, 103, 54), (74, 86, 63), (57, 69, 73), (40, 52, 82), (24, 35, 91)]
PENCILS = []
for i, (top, bot, rx) in enumerate(RIGHT):
    Wd.solid(rx, top, COLS, bot)                           # the step block
    Wd.solid(rx + 4, bot + 1, COLS, bot + 4)               # pencil body (3 rows, centred in the 5-row slot)
    Wd.hazard(rx, bot + 1, rx + 4, bot + 4, 'pencil%d' % i)  # pencil tip (cone) at the slot mouth
    PENCILS.append(dict(i=i, x0=rx, x1=COLS, row0=bot + 1, row1=bot + 4, slot0=bot, slot1=bot + 5))
EXIT = (95, 1, 100, 9)                                     # exit slot through the top room's ceiling, top-right corner
Wd.floor(*EXIT)
Wd.exits.append(Wd.px(*EXIT))
VW = float(os.environ.get('VW', '16.2'))                   # reference ~16.8 px/s, x0.9615
t_w = Wd.seg(0, 1, COLS, ROWS, '-y', 0.0, VW)              # water rises over the whole board (it only shows on floor)
FLOOD_T0 = float(os.environ.get('FT0', '0.3'))
TOP_Y = OY + 27 * C                                         # a box centre above this is in the top room
def start(seed):
    out = []; a = math.radians(-45)                         # all four launch together at a true 45 degrees up-right, 4 px gaps
    for k, g in enumerate(G):
        out.append(dict(g=g, x=OX + 2 + HS + k * (2 * HS + 4), y=OY + ROWS * C - HS - 1, vx=SPD * math.cos(a), vy=SPD * math.sin(a)))
    return out
def run(seed, dur=None):
    a, b, ts = parse_seed(seed)
    return sim(Wd, start(a), a, dur or float(os.environ.get('DUR', '76')), SPD, HS, flood_t0=FLOOD_T0, seed2=b, t_split=ts,
               jitter=float(os.environ.get('JIT', '0.026')), post_win=float(os.environ.get('POST', '3.0')))
