# Shared core for the "Choose a Square" flood-maze recreations (m01-m03).
# Rules measured from the references (igref/SPEC_*.md):
#  - face boxes move at constant speed on 45-degree diagonals, reflect off walls, bricks, dead boxes and each other; no steering
#  - bricks break cell by cell when hit (HP per cell); the STRENGTH gummy breaks a brick cell in one hit and kills any box it touches
#  - the flood is a SOLID moving wall that advances segment by segment along the path with a flat front; it pushes boxes;
#    a box dies only when the front pins it against a wall / brick / dead box (crushed). Intact bricks hold the flood back.
#  - first box into the exit wins; everything freezes on that frame
import sys, os, math, random, json
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
from PIL import ImageFilter, ImageEnhance
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (100, 200, 70), 'cleo': (70, 135, 255), 'cyrus': (255, 145, 30), 'ray': (180, 95, 235)}
SUB = 8

class Maze:
    def __init__(s, cfg):
        s.cfg = cfg; s.U = cfg['U']; s.X0 = cfg['X0']; s.Y0 = cfg['Y0']; s.MAP = cfg['MAP']
        s.ROWS, s.COLS = len(s.MAP), len(s.MAP[0]); s.HS = cfg.get('HS', 14); s.SPD = cfg['SPD_U'] * s.U
        s.BRK = {}                                     # (r, c) -> dict(hp, col)
        for (r, c), (hp, col) in cfg['BRICKS'].items(): s.BRK[(r, c)] = dict(hp=hp, hp0=hp, col=col)
    def cell(s, x, y): return int((y - s.Y0) // s.U), int((x - s.X0) // s.U)
    def is_wall(s, r, c): return r < 0 or c < 0 or r >= s.ROWS or c >= s.COLS or s.MAP[r][c] == '#'
    def rect(s, c0, r0, c1, r1): return (s.X0 + c0 * s.U, s.Y0 + r0 * s.U, s.X0 + (c1 + 1) * s.U, s.Y0 + (r1 + 1) * s.U)
    # ---------------- flood
    def seg_cover(s, k, p):
        """covered px rects of segment k at progress p (units)"""
        rects, d = s.SEGS[k]['rects'], s.SEGS[k]['dir']; out = []
        for (c0, r0, c1, r1) in rects:
            x0, y0, x1, y1 = s.rect(c0, r0, c1, r1); L = p * s.U
            if d == 'D': out.append((x0, y0, x1, min(y1, y0 + L)))
            elif d == 'U': out.append((x0, max(y0, y1 - L), x1, y1))
            elif d == 'R': out.append((x0, y0, min(x1, x0 + L), y1))
            else: out.append((max(x0, x1 - L), y0, x1, y1))
        return [o for o in out if o[2] - o[0] > 0.5 and o[3] - o[1] > 0.5]
    def seg_block(s, k):
        """max progress allowed by intact bricks inside the segment"""
        sg = s.SEGS[k]; best = sg['len']
        for (c0, r0, c1, r1) in sg['rects']:
            for (r, c), b in s.BRK.items():
                if b['hp'] <= 0 or not (c0 <= c <= c1 and r0 <= r <= r1): continue
                d = sg['dir']
                lim = (r - r0) if d == 'D' else (r1 - r) if d == 'U' else (c - c0) if d == 'R' else (c1 - c)
                best = min(best, lim)
        return best
    # ---------------- simulation
    def sim(s, seed, dur):
        cfg = s.cfg; rnd = random.Random(seed); HS = s.HS; U = s.U
        for b in s.BRK.values(): b['hp'] = b['hp0']
        s.SEGS = []
        for (rects, d, t0, t1) in cfg['FLOOD']:
            c0, r0, c1, r1 = rects[0]; L = (r1 - r0 + 1) if d in 'DU' else (c1 - c0 + 1)
            s.SEGS.append(dict(rects=rects, dir=d, t0=t0, v=L / (t1 - t0), len=L, p=0.0))
        X = {}
        for g in G:
            sc, sr = cfg['START'][g]; jx, jy = cfg.get('JIT', (0.5, 0.5))
            d = cfg.get('DIR0', None)
            dx, dy = d if d else (rnd.choice([-1, 1]), rnd.choice([-1, 1]))
            if cfg.get('DIRRAND'): dx, dy = rnd.choice([-1, 1]), rnd.choice([-1, 1])
            v = s.SPD / math.sqrt(2)
            X[g] = dict(x=s.X0 + (sc - rnd.uniform(0, jx)) * U, y=s.Y0 + (sr + rnd.uniform(0, jy)) * U, vx=dx * v, vy=dy * v,
                        out=None, how=None, strong=False, last={})
        for g in G:                                    # spawn check: every box fully inside open floor
            p = X[g]; r0, r1 = int((p['y'] - HS - s.Y0) // U), int((p['y'] + HS - 1 - s.Y0) // U); c0, c1 = int((p['x'] - HS - s.X0) // U), int((p['x'] + HS - 1 - s.X0) // U)
            assert not any(s.is_wall(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)), ('spawn in wall', g)
        gum = dict(x=s.X0 + cfg['GUM'][0] * U, y=s.Y0 + cfg['GUM'][1] * U, t=None, who=None)
        ev = []; frames = []; contacts = []; win = None; lag = 0.0
        T_START = cfg.get('T_START', 0.2)
        def solids(x, y):
            out = []
            r0, r1 = int((y - HS - s.Y0) // U) - 1, int((y + HS - s.Y0) // U) + 1
            c0, c1 = int((x - HS - s.X0) // U) - 1, int((x + HS - s.X0) // U) + 1
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    if s.is_wall(r, c): out.append((s.X0 + c * U, s.Y0 + r * U, s.X0 + c * U + U, s.Y0 + r * U + U, None))
                    elif (r, c) in s.BRK and s.BRK[(r, c)]['hp'] > 0: out.append((s.X0 + c * U, s.Y0 + r * U, s.X0 + c * U + U, s.Y0 + r * U + U, (r, c)))
            for g2, q in X.items():
                if q['out'] is not None and abs(q['x'] - x) < 3 * HS and abs(q['y'] - y) < 3 * HS: out.append((q['x'] - HS, q['y'] - HS, q['x'] + HS, q['y'] + HS, 'dead'))
            return out
        def overlap_solid(p):
            best = 0.0
            for (x0, y0, x1, y1, k) in solids(p['x'], p['y']):
                ox_ = min(p['x'] + HS, x1) - max(p['x'] - HS, x0); oy_ = min(p['y'] + HS, y1) - max(p['y'] - HS, y0)
                if ox_ > 0 and oy_ > 0: best = max(best, min(ox_, oy_))
            return best
        nfr = int(dur * FPS)
        for f in range(nfr):
            t = f / FPS; dt = 1 / FPS / SUB; CF = {g: False for g in G}
            # flood progress (segment by segment; an intact brick holds it back and delays everything after it)
            blocked = False
            for k, sg in enumerate(s.SEGS):
                if t < sg['t0'] + lag or sg['p'] >= sg['len']: continue
                want = sg['p'] + sg['v'] / FPS; lim = s.seg_block(k)
                if want > lim: sg['p'] = max(sg['p'], lim); blocked = True
                else: sg['p'] = min(sg['len'], want)
            if blocked: lag += 1 / FPS
            cover = [(k, r) for k, sg in enumerate(s.SEGS) for r in s.seg_cover(k, sg['p'])]
            for _ in range(SUB if t >= T_START else 0):
                for g in G:
                    p = X[g]
                    if p['out'] is not None: continue
                    for axis in ('x', 'y'):
                        p[axis] += p['v' + axis] * dt
                        for (x0, y0, x1, y1, k) in solids(p['x'], p['y']):
                            if p['x'] + HS <= x0 or p['x'] - HS >= x1 or p['y'] + HS <= y0 or p['y'] - HS >= y1: continue
                            if k not in (None, 'dead') and s.BRK[k]['hp'] <= 0: continue
                            v = p['v' + axis]
                            if axis == 'x': before = p['x'] < (x0 + x1) / 2; p['x'] = x0 - HS if before else x1 + HS
                            else: before = p['y'] < (y0 + y1) / 2; p['y'] = y0 - HS if before else y1 + HS
                            if (v > 0) == before and v != 0:            # moving into it: reflect
                                p['v' + axis] = -v; CF[g] = True; contacts.append((t, g, k))
                                if k not in (None, 'dead') and t - p['last'].get(k, -9) > 0.1:
                                    p['last'][k] = t; b = s.BRK[k]; b['hp'] -= (99 if p['strong'] else 1)
                                    ev.append((t, 'break' if b['hp'] <= 0 else 'crack', g, k, p['strong']))
                live = [g for g in G if X[g]['out'] is None]
                for i in range(len(live)):
                    for j in range(i + 1, len(live)):
                        a_, b_ = X[live[i]], X[live[j]]
                        if a_['out'] is not None or b_['out'] is not None: continue
                        px, py = 2 * HS - abs(a_['x'] - b_['x']), 2 * HS - abs(a_['y'] - b_['y'])
                        if px <= 0 or py <= 0: continue
                        if a_['strong'] != b_['strong']:                     # the gummy holder knocks the other box out on touch
                            vic = live[j] if a_['strong'] else live[i]; X[vic]['out'] = t; X[vic]['how'] = 'hit'
                            ev.append((t, 'out', vic, 'hit', live[i] if vic == live[j] else live[j]))
                        if px < py:
                            sg_ = 1 if a_['x'] < b_['x'] else -1; a_['x'] -= sg_ * px / 2; b_['x'] += sg_ * px / 2
                            if (b_['vx'] - a_['vx']) * sg_ < 0: a_['vx'] = -sg_ * abs(a_['vx']); b_['vx'] = sg_ * abs(b_['vx']); CF[live[i]] = CF[live[j]] = True
                        else:
                            sg_ = 1 if a_['y'] < b_['y'] else -1; a_['y'] -= sg_ * py / 2; b_['y'] += sg_ * py / 2
                            if (b_['vy'] - a_['vy']) * sg_ < 0: a_['vy'] = -sg_ * abs(a_['vy']); b_['vy'] = sg_ * abs(b_['vy']); CF[live[i]] = CF[live[j]] = True
                # the flood pushes; pinned against something solid = crushed
                for g in G:
                    p = X[g]
                    if p['out'] is not None: continue
                    for (k, (x0, y0, x1, y1)) in cover:
                        ox_ = min(p['x'] + HS, x1) - max(p['x'] - HS, x0); oy_ = min(p['y'] + HS, y1) - max(p['y'] - HS, y0)
                        if ox_ <= 0 or oy_ <= 0: continue
                        d = s.SEGS[k]['dir']; px0, py0 = p['x'], p['y']
                        # front push (along the flood's direction) or, if the box only straddles the side of the flooded
                        # strip, a small lateral push out of that side: whichever is shorter
                        opts = {'D': (y1 + HS) - p['y'], 'U': p['y'] - (y0 - HS), 'R': (x1 + HS) - p['x'], 'L': p['x'] - (x0 - HS)}
                        side = ('L', 'R') if d in 'DU' else ('U', 'D')
                        mv = min([d] + list(side), key=lambda z: opts[z])
                        if mv == 'D': p['y'] = y1 + HS; ch = p['vy'] < 0; p['vy'] = abs(p['vy'])
                        elif mv == 'U': p['y'] = y0 - HS; ch = p['vy'] > 0; p['vy'] = -abs(p['vy'])
                        elif mv == 'R': p['x'] = x1 + HS; ch = p['vx'] < 0; p['vx'] = abs(p['vx'])
                        else: p['x'] = x0 - HS; ch = p['vx'] > 0; p['vx'] = -abs(p['vx'])
                        if ch: CF[g] = True
                        if os.environ.get('DBG') and g == os.environ['DBG']: print('flood push', round(t, 2), k, d, (round(px0, 1), round(py0, 1)), '->', (round(p['x'], 1), round(p['y'], 1)), (x0, y0, x1, y1))
                        if overlap_solid(p) > 0.5:                   # pinned: stays flush against the wall, crushed
                            p['x'], p['y'] = px0, py0
                            p['out'] = t; p['how'] = 'crush'; ev.append((t, 'out', g, 'crush', None)); break
            for g in G:
                p = X[g]
                if p['out'] is not None or t < T_START: continue
                if gum['t'] is None and abs(p['x'] - gum['x']) < HS + 12 and abs(p['y'] - gum['y']) < HS + 12:
                    gum['t'] = t; gum['who'] = g; p['strong'] = True; ev.append((t, 'pick', g))
                if cfg['WIN'](s, p):
                    win = (t, g); ev.append((t, 'win', g)); break
            frames.append(({g: (X[g]['x'], X[g]['y'], X[g]['vx'], X[g]['vy'], X[g]['out'], X[g]['strong'], X[g]['how']) for g in G},
                           [sg['p'] for sg in s.SEGS], {k: b['hp'] for k, b in s.BRK.items()}, CF))
            if win or all(X[g]['out'] is not None for g in G): break
        return X, frames, ev, gum, win, contacts
