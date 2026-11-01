# DOXTeq2DVZd recreation: map, flood schedule, start state (shared by the search and the renderer)
import math, random, os
from engine import World, sim, selfcheck
C = 11; COLS, ROWS = 94, 84; OX = (1080 - COLS * C) // 2; OY = 468
G = ['joy', 'cleo', 'cyrus', 'ray']
HS = 22; SPD = 275.0
Wd = World(COLS, ROWS, C, OX, OY)
Wd.floor(18, 2, 34, 26)                                   # top room, left part (gummy, exit side)
BLOCK = Wd.breakable(34, 2, 66, 26, 66, kind='block')     # the 66 block, full room height
Wd.floor(66, 2, 84, 12)                                   # top-right subroom
Wd.floor(8, 10, 18, 18)                                   # exit opening in the left wall
Wd.exits.append(Wd.px(8, 10, 18, 18))
Wd.floor(34, 28, 56, 34)                                  # corridor over the column
GATE = {}
GATE['ray'] = Wd.breakable(34, 34, 46, 38, 3, owner='ray', kind='gate')      # ceiling of the column: the bottom lane's guide
LANES = {'joy': 38, 'cleo': 50, 'cyrus': 62, 'ray': 74}
for g, y0 in LANES.items(): Wd.floor(2, y0, 46, y0 + 8)
GATE['joy'] = Wd.breakable(34, 46, 46, 50, 3, owner='joy', kind='gate')
GATE['cleo'] = Wd.breakable(34, 58, 46, 62, 3, owner='cleo', kind='gate')
GATE['cyrus'] = Wd.breakable(34, 70, 46, 74, 3, owner='cyrus', kind='gate')
Wd.floor(50, 28, 56, 82)                                  # right column down
Wd.floor(50, 76, 80, 82)                                  # bottom corridor
Wd.floor(71, 66, 79, 76); Wd.floor(72, 54, 78, 66); Wd.floor(73, 12, 78, 54)   # funnel: 2 boxes, 1.5, single file (1.25)
# ---- flood (the shadow), flood-clock seconds; speeds per stretch follow the reference's measured front speeds (scaled to box size)
V = dict(lane=float(os.environ.get('VL', '30')), col=float(os.environ.get('VC', '45')), cor=float(os.environ.get('VR', '90')),
         fun=float(os.environ.get('VF', '50')), sub=float(os.environ.get('VS', '28')), room=float(os.environ.get('VM', '75')))
t1 = 0.0
for g, y0 in LANES.items():
    e = Wd.seg(2, y0, 34, y0 + 8, '+x', 0.0, V['lane'])
t_c = Wd.seg(34, 38, 46, 82, '-y', e, V['col'])            # the column fills from the bottom once the lanes are full
t_c = Wd.seg(34, 34, 46, 38, '-y', t_c, V['col'])
t_r = Wd.seg(34, 28, 56, 34, '+x', t_c, V['cor'])          # then the dark runs along the corridor
t_c = t_c + 12 * C / V['cor']
t_d0 = t_c + 4 * C / V['cor']
t_d = Wd.seg(50, 34, 56, 82, '+y', t_d0, V['cor'])
t_b0 = t_d0 + 42 * C / V['cor']
t_b = Wd.seg(56, 76, 80, 82, '+x', t_b0, V['cor'])
t_f0 = t_b0 + 23 * C / V['cor']                           # the funnel starts once the corridor under it is full
t_f = Wd.seg(71, 66, 79, 76, '-y', t_f0, V['fun'])
t_f = Wd.seg(72, 54, 78, 66, '-y', t_f, V['fun'])
t_f = Wd.seg(73, 12, 78, 54, '-y', t_f, V['fun'])
t_s = Wd.seg(66, 2, 84, 12, '-y', t_f, V['sub'])
Wd.B[BLOCK]['stop_at'] = t_f - 0.05                        # the dark waits at the top of the shaft until the block is broken
t_m = Wd.seg(18, 2, 66, 26, '-x', t_s, V['room'])
t_x = Wd.seg(8, 10, 18, 18, '-x', t_m, V['room'])
FLOOD_T0 = float(os.environ.get('FT0', '0.2'))
GUM0 = dict(x=OX + 26 * C, y=OY + 14 * C, r=14)
def start(seed):
    rnd = random.Random(seed * 7 + 1)
    a = math.radians(rnd.uniform(36, 54)) * (1 if rnd.random() < 0.5 else -1)
    out = []
    for g, y0 in LANES.items():
        out.append(dict(g=g, x=OX + 2 * C + HS + 1, y=OY + (y0 + 4) * C, vx=SPD * math.cos(a), vy=SPD * math.sin(a)))
    return out
def run(seed, dur=None):
    return sim(Wd, start(seed), seed, dur or float(os.environ.get('DUR', '64')), SPD, HS, flood_t0=FLOOD_T0, gummy=GUM0, LP=132,
               jitter=float(os.environ.get('JIT', '0.026')), post_win=float(os.environ.get('POST', '2.6')))
