# scripted arc for #20: Hollow pulls way ahead, gets walled in right before the line, then claws back and wins
import random, os
from sim import N, dist, nbrs, legal_wall
def best_wall(rnd, walls, me_pos, me_goal, op_pos, op_goal):
    do = dist(op_pos, op_goal, walls); dm = dist(me_pos, me_goal, walls); best = None
    cands = [(r, c, o) for r in range(N - 1) for c in range(N - 1) for o in 'hv']; rnd.shuffle(cands)
    for w in cands:
        if not legal_wall(w, walls): continue
        walls.add(w); ndo = dist(op_pos, op_goal, walls); ndm = dist(me_pos, me_goal, walls); walls.discard(w)
        if ndo >= 999 or ndm >= 999: continue
        sc = (ndo - do) - (ndm - dm) + rnd.uniform(0, 0.3)
        if best is None or sc > best[0]: best = (sc, w, ndo - do)
    return best
def play2(seed, p):
    rnd = random.Random(seed)
    P = {'hollow': (N - 1, 4), 'cyrus': (0, 4)}; GOAL = {'hollow': 0, 'cyrus': N - 1}
    left = {'hollow': 7, 'cyrus': 7}; walls = set(); log = []; phase = 'lead'
    order = ['hollow', 'cyrus']
    for turn in range(140):
        me = order[turn % 2]; op = order[(turn + 1) % 2]
        dm = dist(P[me], GOAL[me], walls); do = dist(P[op], GOAL[op], walls)
        dh = dist(P['hollow'], 0, walls)
        want = False
        if me == 'hollow':
            if phase == 'lead': want = left['hollow'] > p['reserve'] and do <= dm + p['hth'] and rnd.random() < p['hp']
            else: want = left['hollow'] > 0 and do <= p['clutch'] and do <= dm
        else:
            if phase == 'lead' and dh <= p['trig']: phase = 'trap'
            if phase == 'trap': want = left['cyrus'] > 0
            else: want = left['cyrus'] > 0 and rnd.random() < p['cp'] and do <= dm - 1
        acted = False
        if want:
            b = best_wall(rnd, walls, P[me], GOAL[me], P[op], GOAL[op])
            if b and b[0] >= p['minsc']:
                walls.add(b[1]); left[me] -= 1; log.append(('wall', me, b[1], b[2])); acted = True
            elif me == 'cyrus' and phase == 'trap': phase = 'race'
        if me == 'cyrus' and phase == 'trap' and left['cyrus'] == 0: phase = 'race'
        if not acted:
            r, c = P[me]; opts = []
            for nr, nc in nbrs(r, c, walls):
                if (nr, nc) == P[op]: continue
                opts.append((dist((nr, nc), GOAL[me], walls), rnd.random(), nr, nc))
            if opts:
                _, _, nr, nc = min(opts); P[me] = (nr, nc); log.append(('move', me, (r, c), (nr, nc)))
            else: log.append(('wait', me))
        if P[me][0] == GOAL[me]: return me, log, left
    return None, log, left
def trace(log):
    P = {'hollow': (N - 1, 4), 'cyrus': (0, 4)}; walls = set(); out = []
    for e in log:
        if e[0] == 'move': P[e[1]] = e[3]
        if e[0] == 'wall': walls.add(e[2])
        out.append((dist(P['hollow'], 0, walls), dist(P['cyrus'], N - 1, walls)))
    return out
P0 = dict(reserve=int(os.environ.get('RES', 3)), hth=1, hp=0.85, clutch=int(os.environ.get('CL', 2)), trig=int(os.environ.get('TRIG', 2)), cp=0.0, minsc=0.95)
if __name__ == '__main__':
    import sys
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        win, log, left = play2(seed, P0)
        if win != 'hollow': continue
        tr = trace(log)
        # lead: hollow <=2 steps while cyrus >=5; then trapped: hollow behind by >=4; cyrus later gets within 1-2 steps
        i_lead = next((i for i, (h, c) in enumerate(tr) if h <= 2 and c >= 5), None)
        if i_lead is None: continue
        worst = max(h - c for h, c in tr[i_lead:]); cmin = min(c for h, c in tr[i_lead:])
        cw = sum(1 for e in log if e[0] == 'wall' and e[1] == 'cyrus'); hw = sum(1 for e in log if e[0] == 'wall' and e[1] == 'hollow')
        if worst >= int(os.environ.get('WG', 4)) and cmin <= 2 and len(log) <= int(os.environ.get('ML', 52)):
            print(seed, len(log), 'lead@', i_lead, 'worst', worst, 'cmin', cmin, 'walls H/C', hw, cw, 'peak', max(h for h, c in tr[i_lead:]), flush=True)
