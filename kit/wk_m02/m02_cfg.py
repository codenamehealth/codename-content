# m02 = DSFjv2viBWJ layout (igref/SPEC_DSFjv2viBWJ.md), grid 14 x 18, reference placement u=69.57 at (53, 333) -> u=70 at (50, 333)
import os, json
from maze_core2 import *
MAP = ['.' * 14, '.' * 14, '.' + '#' * 12 + '.',
       '.#EE##..##..#.', '.#EE##..##..#.', '.#..###.###.#.',
       '.#............', '.#............', '.' + '#' * 13,
       '.' * 14, '.' * 14, '#' * 12 + '..',
       '..............', '..............', '..............',
       '..#..#..#..###', '..#..#..#..###', '..#..#..#..###']
U = 70; X0 = 50; Y0 = 333; HS = 26
GATES = {2: ('joy', 1), 5: ('cleo', 3), 8: ('cyrus', 1), 11: ('ray', 1)}     # colour pattern as the reference (one colour per gate)
DARK = (58, 52, 78)
BRICKS = {}
for c, (g, hp) in GATES.items():
    for r in (12, 13, 14): BRICKS[(r, c)] = (int(os.environ.get('GHP%d' % c, hp)), COL[g])
for rc in ((6, 6), (7, 6), (6, 10), (7, 10)): BRICKS[rc] = (int(os.environ.get('DHP', '2')), DARK)
for rc in ((5, 2), (5, 3)): BRICKS[rc] = (int(os.environ.get('XHP', '2')), DARK)
FLOODMAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flood_m02.json')))
FLOODMAP = {k: v for k, v in FLOODMAP.items() if MAP[int(k.split(',')[0]) // 2][int(k.split(',')[1]) // 2] != '#'}
PISTONS = [dict(cols=(6, 7), base=Y0 + 2 * U, dir='U', amp=2 * U - 4, period=5.4, t0=0.0),
           dict(cols=(1, 2), base=Y0 + 9 * U, dir='D', amp=2 * U - 4, period=12.6, t0=0.0),
           dict(cols=(10, 11), base=Y0 + 9 * U, dir='D', amp=2 * U - 4, period=12.6, t0=6.3, start=6.3)]
_h = HS / U
START = {g: (c0 + _h + 0.12, 18 - _h - 0.12) for g, c0 in zip(G, (0, 3, 6, 9))}
CFG = dict(U=U, X0=X0, Y0=Y0, MAP=MAP, BRICKS=BRICKS, FLOODMAP=FLOODMAP, PISTONS=PISTONS, SPD_U=4.89, HS=HS, START=START, JIT=(0.5, 0.5),
           DIR0=(1, -1), PICKUPS=[(7.5, 3.5, 'grow'), (11.5, 3.5, 'grow')], T_START=0.1, FLOOD_DIR0=(1, 0),
           WIN=lambda s, p: s.X0 + 2 * s.U <= p['x'] <= s.X0 + 4 * s.U and s.Y0 + 3 * s.U <= p['y'] <= s.Y0 + 5 * s.U)
