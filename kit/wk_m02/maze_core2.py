# Core for the "Ball Chaos" recreations with replayed floods and pistons (m02, m03).
# Rules (igref/SPEC_*.md): face boxes at constant speed on 45-degree diagonals reflect off walls, bricks, pistons, dead boxes
# and each other (no steering); bricks break cell by cell when hit; the flood is replayed from the reference per half-cell
# arrival times, is solid and pushes boxes; pistons are solid triangle-wave slabs that push boxes; a box dies only when a
# flood front or a piston pins it against something solid (crushed). Pickups: 'grow' (2x size). First box into the exit wins.
import sys, os, math, random, json
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (100, 200, 70), 'cleo': (70, 135, 255), 'cyrus': (255, 145, 30), 'ray': (180, 95, 235)}
SUB = 8

class Maze:
    def __init__(s, cfg):
        s.cfg = cfg; s.U = cfg['U']; s.X0 = cfg['X0']; s.Y0 = cfg['Y0']; s.MAP = cfg['MAP']
        s.ROWS, s.COLS = len(s.MAP), len(s.MAP[0]); s.HS = cfg['HS']; s.SPD = cfg['SPD_U'] * s.U
        s.BRK = {(r, c): dict(hp=hp, hp0=hp, col=col) for (r, c), (hp, col) in cfg['BRICKS'].items()}
        H2 = s.U / 2; s.H2 = H2
        s.FT = {tuple(int(v) for v in k.split(',')): t for k, t in cfg['FLOODMAP'].items()}
        s.FDIR = {}; s.FW = {}
        for (r, c), tv in s.FT.items():
            best = None
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                tn = s.FT.get((r + dr, c + dc))
                if tn is not None and tn < tv and (best is None or tn < best[0]): best = (tn, dr, dc)
            if best is None: s.FDIR[(r, c)] = cfg.get('FLOOD_DIR0', (1, 0)); s.FW[(r, c)] = 0.6   # first cells: rise from below
            else: s.FDIR[(r, c)] = (best[1], best[2]); s.FW[(r, c)] = min(1.5, max(0.3, tv - best[0]))
        src = {k for k, tv in s.FT.items() if not any(s.FT.get((k[0] + dr, k[1] + dc), 1e9) < tv for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        t_min = min(s.FT.values())
        for _ in range(12):                                     # equal-time plateaus inherit the direction of the plateau they join
            for k in list(src):
                if s.FT[k] <= t_min + 0.05: continue
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (k[0] + dr, k[1] + dc)
                    if n in s.FT and n not in src and abs(s.FT[n] - s.FT[k]) < 0.05:
                        s.FDIR[k] = (dr, dc); s.FW[k] = 0.3; src.discard(k); break
        for _ in range(3):                                      # make every plateau progressive: never earlier than its source + 0.08s
            for k, tv in sorted(s.FT.items(), key=lambda z: z[1]):
                if k in src: continue
                n = (k[0] + s.FDIR[k][0], k[1] + s.FDIR[k][1])
                if n in s.FT and s.FT[k] < s.FT[n] + 0.08: s.FT[k] = s.FT[n] + 0.08
        s.FORDER = sorted(s.FT.items(), key=lambda z: z[1])
    def cell(s, x, y): return int((y - s.Y0) // s.U), int((x - s.X0) // s.U)
    def is_wall(s, r, c): return r < 0 or c < 0 or r >= s.ROWS or c >= s.COLS or s.MAP[r][c] == '#'
    def piston_rect(s, k, t):
        p = s.cfg['PISTONS'][k]; c0, c1 = p['cols']; ph = ((t - p['t0']) % p['period']) / p['period']
        e = p['amp'] * (2 * ph if ph < 0.5 else 2 - 2 * ph)
        if t < p.get('start', -1e9): e = 0.0
        x0, x1 = s.X0 + c0 * s.U, s.X0 + (c1 + 1) * s.U; yb = p['base']
        return (x0, yb - e, x1, yb) if p['dir'] == 'U' else (x0, yb, x1, yb + e)
    def flood_rect(s, r, c, cov):
        """the covered part of half-cell (r, c): it creeps in from the neighbour it came from"""
        x0, y0 = s.X0 + c * s.H2, s.Y0 + r * s.H2; H2 = s.H2
        if cov >= 1: return (x0, y0, x0 + H2, y0 + H2)
        k = H2 * cov; dr, dc = s.FDIR[(r, c)]
        if dr == 1: return (x0, y0 + H2 - k, x0 + H2, y0 + H2)   # (dr, dc) points at the earlier neighbour the flood comes from
        if dr == -1: return (x0, y0, x0 + H2, y0 + k)
        if dc == 1: return (x0 + H2 - k, y0, x0 + H2, y0 + H2)
        return (x0, y0, x0 + k, y0 + H2)
    def cover_of(s, F):
        out = []
        for (r, c), tv in s.FORDER:
            w = s.FW[(r, c)]; cov = (F - (tv - w / 2)) / w
            if cov <= 0: break
            if (r // 2, c // 2) in s.BRK and s.BRK[(r // 2, c // 2)]['hp'] > 0: continue
            out.append(((r, c), s.flood_rect(r, c, min(1.0, cov))))
        return out
    def sim(s, seed, dur):
        cfg = s.cfg; rnd = random.Random(seed); U = s.U
        for b in s.BRK.values(): b['hp'] = b['hp0']
        X = {}
        for g in G:
            sc, sr = cfg['START'][g]; jx, jy = cfg.get('JIT', (0.3, 0.3)); dx, dy = cfg.get('DIR0', (1, -1)); v = s.SPD / math.sqrt(2)
            X[g] = dict(x=s.X0 + (sc + rnd.uniform(0, jx)) * U, y=s.Y0 + (sr - rnd.uniform(0, jy)) * U, vx=dx * v, vy=dy * v, hs=s.HS, hs_t=s.HS,
                        out=None, how=None, strong=False, last={})
        for g in G:
            p = X[g]; HS = p['hs']
            r0, r1 = int((p['y'] - HS - s.Y0) // U), int((p['y'] + HS - 1 - s.Y0) // U); c0, c1 = int((p['x'] - HS - s.X0) // U), int((p['x'] + HS - 1 - s.X0) // U)
            assert not any(s.is_wall(r, c) or (r, c) in s.BRK for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)), ('spawn in wall', g)
        PK = [dict(x=s.X0 + px * U, y=s.Y0 + py * U, t=None, who=None, kind=kd) for (px, py, kd) in cfg['PICKUPS']]
        ev = []; frames = []; contacts = []; win = None; lag = 0.0; T_START = cfg.get('T_START', 0.1)
        def solids(x, y, HS, t, me=None):
            out = []
            r0, r1 = int((y - HS - s.Y0) // U) - 1, int((y + HS - s.Y0) // U) + 1
            c0, c1 = int((x - HS - s.X0) // U) - 1, int((x + HS - s.X0) // U) + 1
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    if s.is_wall(r, c): out.append((s.X0 + c * U, s.Y0 + r * U, s.X0 + c * U + U, s.Y0 + r * U + U, None))
                    elif (r, c) in s.BRK and s.BRK[(r, c)]['hp'] > 0: out.append((s.X0 + c * U, s.Y0 + r * U, s.X0 + c * U + U, s.Y0 + r * U + U, (r, c)))
            for k in range(len(cfg['PISTONS'])):
                pr = s.piston_rect(k, t)
                if pr[2] - pr[0] > 0.5 and pr[3] - pr[1] > 0.5: out.append(pr + ('piston',))
            for g2, q in X.items():
                if q['out'] is not None and g2 != me: out.append((q['x'] - q['hs'], q['y'] - q['hs'], q['x'] + q['hs'], q['y'] + q['hs'], 'dead'))
            return out
        def overlap_solid(p, t, me, skip_pistons=False):
            best = 0.0; HS = p['hs']
            for (x0, y0, x1, y1, k) in solids(p['x'], p['y'], HS, t, me):
                if skip_pistons and k == 'piston': continue
                ox_ = min(p['x'] + HS, x1) - max(p['x'] - HS, x0); oy_ = min(p['y'] + HS, y1) - max(p['y'] - HS, y0)
                if ox_ > 0 and oy_ > 0: best = max(best, min(ox_, oy_))
            return best
        def push(p, g, rect, dirn, t, what, CF):
            """push box p out of a moving solid rect; dirn = the mover's direction (dx, dy); crushed if pinned"""
            x0, y0, x1, y1 = rect; HS = p['hs']; px0, py0 = p['x'], p['y']
            opts = {'D': (y1 + HS) - p['y'], 'U': p['y'] - (y0 - HS), 'R': (x1 + HS) - p['x'], 'L': p['x'] - (x0 - HS)}
            front = {(0, 1): 'D', (0, -1): 'U', (1, 0): 'R', (-1, 0): 'L'}[dirn]
            side = ('L', 'R') if front in 'DU' else ('U', 'D')
            mv = front if what == 'piston' else min('DURL', key=lambda z: opts[z])   # flood: out by the shortest way
            if mv == 'D': p['y'] = y1 + HS; ch = p['vy'] < 0; p['vy'] = abs(p['vy'])
            elif mv == 'U': p['y'] = y0 - HS; ch = p['vy'] > 0; p['vy'] = -abs(p['vy'])
            elif mv == 'R': p['x'] = x1 + HS; ch = p['vx'] < 0; p['vx'] = abs(p['vx'])
            else: p['x'] = x0 - HS; ch = p['vx'] > 0; p['vx'] = -abs(p['vx'])
            if ch: CF[g] = True
            if overlap_solid(p, t, g, skip_pistons=(what == 'piston')) > 0.5 or (what != 'piston' and overlap_solid(p, t, g) > 0.5):
                p['x'], p['y'] = px0, py0; p['out'] = t; p['how'] = 'crush'; ev.append((t, 'out', g, 'crush', what)); return True
            return False
        nfr = int(dur * FPS)
        for f in range(nfr):
            t = f / FPS; dt = 1 / FPS / SUB; CF = {g: False for g in G}
            F = t - lag
            for (r, c), tv in s.FORDER:                          # an intact brick holds the flood (and the clock) back
                if tv - s.FW[(r, c)] / 2 > F: break
                if (r // 2, c // 2) in s.BRK and s.BRK[(r // 2, c // 2)]['hp'] > 0: lag += 1 / FPS; F = t - lag; break
            cover = s.cover_of(F)
            for sub in range(SUB if t >= T_START else 0):
                ts = t + sub * dt
                for g in G:
                    p = X[g]
                    if p['out'] is not None: continue
                    if p['hs'] < p['hs_t']:                       # growing, only where there is room (shifted at most 1px)
                        nh = min(p['hs_t'], p['hs'] + 0.5); ox, oy = p['x'], p['y']
                        for sx, sy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                            p['x'], p['y'], ohs = ox + sx, oy + sy, p['hs']; p['hs'] = nh
                            if overlap_solid(p, ts, g) <= 0 and all(X[o]['out'] is not None or o == g or abs(X[o]['x'] - p['x']) >= nh + X[o]['hs'] or abs(X[o]['y'] - p['y']) >= nh + X[o]['hs'] for o in G): break
                            p['hs'] = ohs
                        else: p['x'], p['y'] = ox, oy
                    HS = p['hs']
                    for axis in ('x', 'y'):
                        sol = solids(p['x'], p['y'], HS, ts, g)
                        pre = [not (p['x'] + HS <= x0 or p['x'] - HS >= x1 or p['y'] + HS <= y0 or p['y'] - HS >= y1) for (x0, y0, x1, y1, k) in sol]
                        p[axis] += p['v' + axis] * dt
                        for (x0, y0, x1, y1, k), was in zip(sol, pre):
                            if was: continue                              # overlap made by a moving piston: the push step resolves it
                            if p['x'] + HS <= x0 or p['x'] - HS >= x1 or p['y'] + HS <= y0 or p['y'] - HS >= y1: continue
                            if k not in (None, 'dead', 'piston') and s.BRK[k]['hp'] <= 0: continue
                            v = p['v' + axis]
                            if axis == 'x': before = p['x'] < (x0 + x1) / 2; p['x'] = x0 - HS if before else x1 + HS
                            else: before = p['y'] < (y0 + y1) / 2; p['y'] = y0 - HS if before else y1 + HS
                            if (v > 0) == before and v != 0:
                                p['v' + axis] = -v; CF[g] = True; contacts.append((ts, g, k))
                                if k not in (None, 'dead', 'piston') and ts - p['last'].get(k, -9) > 0.1:
                                    p['last'][k] = ts; b = s.BRK[k]; b['hp'] -= 1
                                    ev.append((ts, 'break' if b['hp'] <= 0 else 'crack', g, k))
                live = [g for g in G if X[g]['out'] is None]
                for i in range(len(live)):
                    for j in range(i + 1, len(live)):
                        a_, b_ = X[live[i]], X[live[j]]; HH = a_['hs'] + b_['hs']
                        px, py = HH - abs(a_['x'] - b_['x']), HH - abs(a_['y'] - b_['y'])
                        if px <= 0 or py <= 0: continue
                        if px < py:
                            sg_ = 1 if a_['x'] < b_['x'] else -1; a_['x'] -= sg_ * px / 2; b_['x'] += sg_ * px / 2
                            if (b_['vx'] - a_['vx']) * sg_ < 0: a_['vx'] = -sg_ * abs(a_['vx']); b_['vx'] = sg_ * abs(b_['vx']); CF[live[i]] = CF[live[j]] = True
                        else:
                            sg_ = 1 if a_['y'] < b_['y'] else -1; a_['y'] -= sg_ * py / 2; b_['y'] += sg_ * py / 2
                            if (b_['vy'] - a_['vy']) * sg_ < 0: a_['vy'] = -sg_ * abs(a_['vy']); b_['vy'] = sg_ * abs(b_['vy']); CF[live[i]] = CF[live[j]] = True
                # pistons push (they move along their axis), then the flood pushes; pinned = crushed
                for g in G:
                    p = X[g]
                    if p['out'] is not None: continue
                    for k, pc in enumerate(cfg['PISTONS']):
                        pr = s.piston_rect(k, ts + dt); prev = s.piston_rect(k, ts)
                        HS = p['hs']; ox_ = min(p['x'] + HS, pr[2]) - max(p['x'] - HS, pr[0]); oy_ = min(p['y'] + HS, pr[3]) - max(p['y'] - HS, pr[1])
                        if ox_ <= 0 or oy_ <= 0: continue
                        if (pr[3] - pr[1]) <= (prev[3] - prev[1]): continue          # only an extending piston pushes
                        if push(p, g, pr, (0, -1) if pc['dir'] == 'U' else (0, 1), ts + dt, 'piston', CF): break
                    if p['out'] is not None: continue
                    for (rc, (x0, y0, x1, y1)) in cover:
                        HS = p['hs']; ox_ = min(p['x'] + HS, x1) - max(p['x'] - HS, x0); oy_ = min(p['y'] + HS, y1) - max(p['y'] - HS, y0)
                        if ox_ <= 0 or oy_ <= 0: continue
                        dr, dc = s.FDIR[rc]
                        if push(p, g, (x0, y0, x1, y1), (-dc, -dr), ts, 'flood', CF): break
            for g in G:
                p = X[g]
                if p['out'] is not None or t < T_START: continue
                for pk in PK:
                    if pk['t'] is None and abs(p['x'] - pk['x']) < p['hs'] + 14 and abs(p['y'] - pk['y']) < p['hs'] + 14:
                        pk['t'] = t; pk['who'] = g; ev.append((t, 'pick', g, pk['kind']))
                        if pk['kind'] == 'grow': p['hs_t'] = 2 * s.HS; p['strong'] = True
                if cfg['WIN'](s, p):
                    win = (t, g); ev.append((t, 'win', g)); break
            frames.append(({g: (X[g]['x'], X[g]['y'], X[g]['vx'], X[g]['vy'], X[g]['out'], X[g]['strong'], X[g]['how'], X[g]['hs']) for g in G},
                           F, {k: b['hp'] for k, b in s.BRK.items()}, CF))
            if win or all(X[g]['out'] is not None for g in G): break
        return X, frames, ev, PK, win, contacts
