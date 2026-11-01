# m01 = DaG5nn5v8AP layout (igref/SPEC_DaG5nn5v8AP.md), grid 19 x 22
from maze_core import *
def build_map():
    M = [['#'] * 19 for _ in range(22)]
    def fill(c0, r0, c1, r1, ch='.'):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1): M[r][c] = ch
    for c0 in (4, 7, 10, 13): fill(c0, 0, c0 + 1, 6)          # start chambers
    fill(4, 4, 15, 6)                                          # hall under the gates
    fill(16, 4, 18, 10)                                        # right room
    fill(0, 8, 15, 10)                                         # corridor A (+ D1 at col 15)
    fill(0, 8, 2, 14)                                          # left column
    fill(3, 12, 18, 14)                                        # corridor B (+ D2 at col 3)
    fill(16, 12, 18, 18)                                       # right column
    fill(3, 16, 18, 18)                                        # corridor C (+ D3 at col 3)
    fill(0, 16, 2, 21)                                         # left room
    fill(0, 20, 16, 21)                                        # corridor D (+ D4 at col 16)
    fill(17, 20, 18, 21, 'E')                                  # checkered exit
    return [''.join(r) for r in M]
MAP = build_map()
GATE_COL = {6: 'cyrus', 9: 'cleo', 12: 'ray', 15: 'joy'}       # same colour pattern as the reference (box 3, 2, 4, 1)
DARK = (58, 52, 78)
BRICKS = {}
for c, g in GATE_COL.items():
    for r in (4, 5, 6): BRICKS[(r, c)] = (2, COL[g])
for (c, rows) in ((15, (8, 9, 10)), (3, (12, 13, 14)), (3, (16, 17, 18)), (16, (20, 21))):
    for r in rows: BRICKS[(r, c)] = (2, DARK)
FLOOD = [
    ([(4, 0, 5, 3), (7, 0, 8, 3), (10, 0, 11, 3), (13, 0, 14, 3)], 'D', 0.3, 10.4),
    ([(4, 4, 15, 6)], 'R', 10.4, 23.7),
    ([(16, 4, 18, 10)], 'D', 24.1, 27.0),
    ([(0, 8, 15, 10)], 'L', 26.4, 32.7),
    ([(0, 11, 2, 14)], 'D', 33.0, 35.0),
    ([(3, 12, 18, 14)], 'R', 35.3, 40.7),
    ([(16, 15, 18, 18)], 'D', 41.3, 43.0),
    ([(3, 16, 15, 18)], 'L', 43.0, 47.9),
    ([(0, 16, 2, 21)], 'D', 48.1, 50.9),
    ([(3, 20, 16, 21)], 'R', 50.5, 56.7),
]
U = 46
CFG = dict(U=U, X0=(1080 - 19 * U) // 2, Y0=424, MAP=MAP, BRICKS=BRICKS, FLOOD=FLOOD, SPD_U=6.44, HS=14,
           START={'joy': (5.55, 0.45), 'cleo': (8.55, 0.45), 'cyrus': (11.55, 0.45), 'ray': (14.55, 0.45)}, JIT=(0.25, 0.12), DIR0=(-1, 1),
           GUM=(1.5, 17.5), T_START=0.2,
           WIN=lambda s, p: p['x'] - s.HS >= s.X0 + 17 * s.U and p['y'] > s.Y0 + 20 * s.U)
