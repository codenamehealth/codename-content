# m05 DOXTeq2DVZd recreation: map, flood schedule, start state (shared by the search, chk.py and the renderer)
# v2 layout: reference proportions. Reference board x 40-1040, y 248-1640 -> ours x 40-1040, y 250-1610 (x 1:1, y 0.977).
# Grid C=10: col = (ref_x - 40) / 10, row = (ref_y - 248) * 0.0977.
import math, random, os
from engine import World, sim, selfcheck, parse_seed
C = 10; COLS, ROWS = 100, 136; OX = 40; OY = 250
G = ['joy', 'cleo', 'cyrus', 'ray']
HS = int(os.environ.get('HS', '25')); SPD = float(os.environ.get('SPD', '300'))   # reference: 48 px squares at ~300 px/s
Wd = World(COLS, ROWS, C, OX, OY)
Wd.floor(19, 7, 37, 45)                                   # top room, left part (gummy, exit side)
BLOCK = Wd.breakable(37, 7, 76, 45, 66, kind='block')     # the 66 block, full room height
Wd.floor(76, 7, 96, 19)                                   # top-right subroom
EXIT = (4, 21, 19, 30)                                    # exit opening in the left wall of the top room
Wd.floor(*EXIT)
Wd.exits.append(Wd.px(*EXIT))
Wd.floor(44, 58, 70, 65)                                  # corridor over the column
GATE = {}
GATE['ray'] = Wd.breakable(44, 65, 56, 71, 3, owner='ray', kind='gate')      # ceiling of the column: the bottom lane's guide
LANES = {'joy': 71, 'cleo': 87, 'cyrus': 103, 'ray': 119}
LH = 10
for g, y0 in LANES.items(): Wd.floor(4, y0, 56, y0 + LH)
GATE['joy'] = Wd.breakable(44, 81, 56, 87, 3, owner='joy', kind='gate')
GATE['cleo'] = Wd.breakable(44, 97, 56, 103, 3, owner='cleo', kind='gate')
GATE['cyrus'] = Wd.breakable(44, 113, 56, 119, 3, owner='cyrus', kind='gate')
Wd.floor(63, 58, 70, 129)                                 # right column down
Wd.floor(63, 123, 95, 129)                                # bottom corridor
Wd.floor(85, 111, 94, 123); Wd.floor(86, 86, 93, 111); Wd.floor(87, 19, 93, 86)   # funnel: 1.8 boxes, 1.4, single file (1.2)
# ---- flood (the shadow), flood-clock seconds; front speeds are the reference's measured ones (vertical x0.977)
V = dict(lane=float(os.environ.get('VL', '33')), col=float(os.environ.get('VC', '65')), cor=float(os.environ.get('VR', '100')),
         fun=float(os.environ.get('VF', '76')), sub=float(os.environ.get('VS', '20')), room=float(os.environ.get('VM', '80')))
for g, y0 in LANES.items():
    e = Wd.seg(4, y0, 44, y0 + LH, '+x', 0.0, V['lane'])
t_c = Wd.seg(44, 71, 56, 129, '-y', e, V['col'])           # the column fills from the bottom once the lanes are full
HOLD_ROW = int(os.environ.get('HOLDROW', '90'))            # the dark holds this far under the blue gate until Rayleigh breaks it (room for 4 boxes)
Wd.B[GATE['ray']]['stop_at'] = e + (129 - HOLD_ROW) * C / V['col']
t_c = Wd.seg(44, 65, 56, 71, '-y', t_c, V['col'])
Wd.seg(44, 58, 70, 65, '+x', t_c, V['cor'])                # then the dark runs along the corridor
t_d0 = t_c + (63 - 44) * C / V['cor']
Wd.seg(63, 65, 70, 129, '+y', t_d0, V['cor'])               # down the right column
t_b0 = t_d0 + (123 - 65) * C / V['cor']
Wd.seg(70, 123, 95, 129, '+x', t_b0, V['cor'])              # along the bottom corridor
t_f0 = t_b0 + (85 - 70) * C / V['cor']                      # the funnel starts once the corridor under it is full
t_f = Wd.seg(85, 111, 94, 123, '-y', t_f0, V['fun'])
t_f = Wd.seg(86, 86, 93, 111, '-y', t_f, V['fun'])
t_f = Wd.seg(87, 19, 93, 86, '-y', t_f, V['fun'])
t_s = Wd.seg(76, 7, 96, 19, '-y', t_f, V['sub'])
Wd.B[BLOCK]['stop_at'] = t_f - 0.05                        # the dark waits at the top of the shaft until the block is broken
                                                           # (letting it into the subroom first stacks single-file boxes and crushes them)
t_m = Wd.seg(19, 7, 76, 45, '-x', t_s, V['room'])
t_x = Wd.seg(*EXIT, '-x', t_m, V['room'])
FLOOD_T0 = float(os.environ.get('FT0', '0.1'))
GUM0 = dict(x=OX + 28 * C, y=OY + 25 * C, r=16)
TOP_Y = OY + 45 * C                                        # a box centre above this is in the top rooms
def start(seed):
    rnd = random.Random(seed * 7 + 1)
    a = math.radians(45) * (1 if rnd.random() < 0.5 else -1)   # all four launch together at a true 45 degrees, lockstep in identical lanes
    out = []
    for g, y0 in LANES.items():
        out.append(dict(g=g, x=OX + 4 * C + HS + 1, y=OY + (y0 + LH / 2) * C, vx=SPD * math.cos(a), vy=SPD * math.sin(a)))
    return out
def run(seed, dur=None):
    a, b, ts = parse_seed(seed)
    return sim(Wd, start(a), a, dur or float(os.environ.get('DUR', '62')), SPD, HS, flood_t0=FLOOD_T0, gummy=GUM0, LP=160, seed2=b, t_split=ts,
               jitter=float(os.environ.get('JIT', '0.026')), post_win=float(os.environ.get('POST', '2.6')))
