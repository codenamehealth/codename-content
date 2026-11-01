import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
# #89 Last one in the ring wins: rc10 review recut (source fork_sz86/v89/r89.py). Bennett loves it: rule/legibility/universal fixes only.
# rc10: guides 2x -> 3x (collision 56 -> 80), shoving from frame 0, gummies earlier, re-simmed for ~15s with even eliminations; Joy still wins.
import hook as HK
COLL = float(os.environ.get('COLL', '80'))
# HOLLOW RULE: the Hollow contestant is removed (4 guides). GUMMY POWERS (SPEC 12): creatine = STRONG! (power shove),
# mushroom = SPEED! (runs and dashes faster, speed lines + dust); the old POWER SHOVE (mushroom) / HEAVY (creatine) labels are gone.
# Ring 430 -> 340 radius (characters unchanged 2x) so the whole deck fits the safe zone; re-simulated.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RINGC = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
CX, CY, RR = 478, 1120, 340
# n15 SHOVES (Bennett Oct 29): every shove is a planted attack. The shover stops, winds up (Syeda/PixelLab attack frames), strikes,
# and recovers, about 1s standing still in total. Only the strike moves the victim: knockback impulse, a little hop, deck friction,
# and a fall into the water if they slide past the edge.
ATK_WIND, ATK_LEN = 0.42, 1.0
REACHX, REACHY = 250, 120
IMP0 = float(os.environ.get('IMP', '760')); FRIC = float(os.environ.get('FRIC', '2.6'))
GSCHED = [float(x) for x in os.environ.get('GS', '1.3,3.9,5.9,8.3').split(',')]
GKINDS = ['cre', 'mel', 'acv', 'mush']   # n15b: each power once (STRENGTH, SLEEP, SHIELD, SPEED); SPEED spawns in the final
SLEEP_T, SHIELD_T, DASH_T, DASH_K, SKID_T = 1.0, 6.0, 0.42, 2.7, 0.5
FMASS = float(os.environ.get('FMASS', '1.25')); OPK = float(os.environ.get('OPK', '0.55'))
OUT_R = RR + 34   # n15b: OUT only once the feet are past the deck rim (in the water), so nobody stands on the water
def sim(seed, dur=30):
    rnd = random.Random(seed)
    ag = {}
    for k, n in enumerate(NAMES):
        a = -math.pi / 4 + k * 2 * math.pi / 4
        ag[n] = dict(x=CX + 175 * math.cos(a), y=CY + 175 * math.sin(a), vx=0.0, vy=0.0, out=None, cd=rnd.uniform(0.2, 0.9), tgt=None,
                     spd=rnd.uniform(220, 260), pow=1.0, mass=1.0, buff=None, bt=-9, stun=-9, dist=0.0, ph=rnd.uniform(0, 6.3),
                     atk=-9.0, face=1, avic=None, struck=True, hit=-9.0, shield=-9.0, sleep=-9.0, dash=-9.0, dux=0.0, duy=0.0, dodge=-9.0, dashed=False, dhit=False, ate=False)
    gums = []; gsched = list(zip(GSCHED, GKINDS)); G = {'next': 1e9, 'open': None}   # n15c: nobody attacks before Rayleigh's STRENGTH opener   # n15c: one action at a time (strikes >= ~1s apart, never right on a splash)
    frames = []; events = []; outs = []
    def strike(n, v, t, imp_k=1.0):
        s, o = ag[n], ag[v]
        if t - o['shield'] < SHIELD_T:   # SHIELD: the strike bounces off, bubble pops
            o['shield'] = -9.0; events.append((t, 'block', v, n)); G['next'] = t + 0.6 if G['next'] > 1e8 else max(G['next'], t + 0.6); G['open'] = None; return
        dx, dy = o['x'] - s['x'], o['y'] - s['y']; L = math.hypot(dx, dy) or 1
        if s['face'] and abs(dx) > 1: ux, uy = 0.75 * s['face'] + 0.25 * dx / L, 0.25 * dy / L
        else: ux, uy = dx / L, dy / L
        if G['open'] == n: imp_k *= OPK   # the opener only drives Cyrus to the edge
        U = math.hypot(ux, uy); imp = IMP0 * s['pow'] / (o['mass'] * (FMASS if (v in ('joy', 'cyrus') and len([m for m in NAMES if ag[m]['out'] is None]) > 2) else 1.0)) * rnd.uniform(0.9, 1.1) * imp_k
        o['vx'] = ux / U * imp; o['vy'] = uy / U * imp; o['stun'] = t; o['hit'] = t; o['atk'] = -9.0; o['sleep'] = -9.0
        events.append((t, 'shove', n, v)); G['next'] = t + 0.6 if G['next'] > 1e8 else max(G['next'], t + 0.6); G['open'] = None
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        alive = [n for n in NAMES if ag[n]['out'] is None]
        for gi_, (gt, gk) in enumerate(gsched):
            if gk == 'mush':   # SPEED spawns once the final two are left
                due = len(alive) == 2 and outs and t >= max(gt, outs[-1][1] + 0.8) and not any(g['k'] == 'mush' for g in gums) and not any(e[1] == 'gum' and e[3] == 'mush' for e in events)
            else: due = abs(t - gt) < dt / 2
            if due and len(alive) > 1:
                gsched[gi_] = (1e9 if gk == 'mush' else gt, gk)
                powered = set(e[2] for e in events if e[1] == 'gum')
                cand = [m for m in alive if m not in powered and (m != 'cyrus' or gk == 'mush')] or alive
                who = 'cyrus' if gk == 'mush' and 'cyrus' in cand else ('ray' if gk == 'cre' and 'ray' in cand else rnd.choice(cand))   # n15c: Rayleigh opens with STRENGTH   # n15b: drops just ahead of an unpowered guide
                w = ag[who]; a = math.atan2(CY - w['y'], CX - w['x']) + rnd.uniform(-0.6, 0.6); r = rnd.uniform(60, 90) if gk in ('mush', 'cre') else rnd.uniform(90, 140)
                gx, gy = w['x'] + r * math.cos(a), w['y'] + r * math.sin(a)
                er = math.hypot(gx - CX, gy - CY)
                if er > RR - 110: gx, gy = CX + (gx - CX) * (RR - 110) / er, CY + (gy - CY) * (RR - 110) / er
                gums.append(dict(x=gx, y=gy, k=gk, t=t, who=who if gk in ('cre', 'mush') else None))   # n15c: STRENGTH is Rayleigh's, SPEED is Cyrus's
        if len(alive) > 1:
            for n in alive:
                s = ag[n]
                if s['buff'] and t - s['bt'] > 4.0 and s['buff'] != 'mush': s['buff'] = None; s['pow'] = 1.0; s['mass'] = 1.0
                stunned = t - s['stun'] < 0.6
                attacking = t - s['atk'] < ATK_LEN
                asleep = t < s['sleep']
                dashing = 0 <= t - s['dash'] < DASH_T
                skidding = DASH_T <= t - s['dash'] < DASH_T + SKID_T
                dodging = 0 <= t - s['dodge'] < 0.32
                if stunned or skidding or dodging:   # knocked back / skidding out of a dash / sidestepping: deck friction
                    k_ = math.exp(-(FRIC if not dodging else 5.0) * dt); s['vx'] *= k_; s['vy'] *= k_
                    if stunned: s['atk'] = -9.0
                elif asleep: s['vx'] *= 0.5; s['vy'] *= 0.5; s['atk'] = -9.0
                elif dashing:   # SPEED dash: straight line, can't steer
                    sp = s['spd'] * DASH_K; s['vx'], s['vy'] = s['dux'] * sp, s['duy'] * sp
                    if not s['dhit']:
                        for m in alive:
                            if m == n or 0 <= t - ag[m]['dodge'] < 0.32: continue
                            if math.hypot(ag[m]['x'] - s['x'], ag[m]['y'] - s['y']) < 70:
                                s['dhit'] = True; s['face'] = 0; strike(n, m, t, 1.1); break
                elif attacking:   # planted: no movement while winding up / striking / recovering
                    s['vx'] *= 0.5; s['vy'] *= 0.5
                    if not s['struck'] and t - s['atk'] >= ATK_WIND:
                        s['struck'] = True; v = s['avic']
                        o = ag[v] if v else None
                        if o and o['out'] is None:
                            dx, dy = o['x'] - s['x'], o['y'] - s['y']
                            if 0 < dx * s['face'] < REACHX and abs(dy) < REACHY and not (0 <= t - o['dodge'] < 0.32): strike(n, v, t)
                            else: events.append((t, 'whiff', n, v)); G['next'] = t + 0.6 if G['next'] > 1e8 else max(G['next'], t + 0.6); G['open'] = None
                else:
                    mg = [g for g in gums if (g['who'] is None or g['who'] == n) and (n != 'cyrus' or g['k'] == 'mush')]
                    if mg and not s['ate'] and min(math.hypot(g['x'] - s['x'], g['y'] - s['y']) for g in mg) < 260:   # n15b: one gummy each
                        g = min(mg, key=lambda g: math.hypot(g['x'] - s['x'], g['y'] - s['y'])); tx, ty = g['x'], g['y']; tg = None
                    else:
                        if G['open'] == n and 'cyrus' in alive: s['tgt'] = 'cyrus'   # the opener goes at Cyrus
                        elif s['tgt'] not in alive or s['tgt'] == n or rnd.random() < 0.01:
                            opts = [m for m in alive if m != n and not (len(alive) > 2 and {n, m} == {'joy', 'cyrus'})] or [m for m in alive if m != n]   # n15c: Joy and Cyrus save each other for the final
                            s['tgt'] = min(opts, key=lambda m: math.hypot(ag[m]['x'] - s['x'], ag[m]['y'] - s['y']) - 0.6 * math.hypot(ag[m]['x'] - CX, ag[m]['y'] - CY) - (200 if t < ag[m]['sleep'] else 0) + rnd.uniform(0, 140))
                        o = ag[s['tgt']]; tg = s['tgt']
                        side = -1 if o['x'] >= CX else 1      # stand on the inner side so the strike points outward
                        tx, ty = o['x'] + side * 150, o['y']
                    dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                    sp = s['spd'] * (1 + 0.15 * math.sin(2.1 * t + s['ph']))
                    if L < 50: sp *= L / 50
                    ex, ey = s['x'] - CX, s['y'] - CY; er = math.hypot(ex, ey) or 1
                    inx = iny = 0
                    if er > RR - 90: inx, iny = -ex / er * 1.4, -ey / er * 1.4
                    ux, uy = dx / L + inx, dy / L + iny; U = math.hypot(ux, uy) or 1
                    s['vx'] += (ux / U * sp - s['vx']) * 0.15; s['vy'] += (uy / U * sp - s['vy']) * 0.15
                    if s['buff'] == 'mush' and not s['dashed'] and tg and t - s['bt'] > 0.5 and t >= G['next'] and not any(0 <= t - ag[m]['atk'] < ATK_WIND + 0.1 for m in alive if m != n):   # SPEED: one dash at the target
                        o = ag[tg]; ddx, ddy = o['x'] - s['x'], o['y'] - s['y']; dd = math.hypot(ddx, ddy)
                        if 160 < dd < 420:
                            G['next'] = t + DASH_T + SKID_T + 0.3; s['dash'] = t; s['dashed'] = True; s['dux'], s['duy'] = ddx / dd, ddy / dd; s['dhit'] = False
                            events.append((t, 'dash', n, tg))
                            if t - o['stun'] > 0.6 and t >= o['sleep'] and t - o['atk'] > ATK_LEN:   # the target sidesteps (toward the middle)
                                px, py = -s['duy'], s['dux']
                                if (px * (CX - o['x']) + py * (CY - o['y'])) < 0: px, py = -px, -py
                                o['vx'], o['vy'] = px * 560, py * 560; o['dodge'] = t + 0.12; events.append((t + 0.12, 'dodge', tg, n))
                            continue
                    if tg and t > s['cd'] and (t >= G['next'] or G['open'] == n) and not any(math.hypot(g['x'] - ag[tg]['x'], g['y'] - ag[tg]['y']) < 160 and (g['who'] in (None, tg)) and not ag[tg]['ate'] for g in gums) and not any(0 <= t - ag[m]['atk'] < ATK_WIND + 0.1 for m in alive if m != n) and not any(0 <= t - ag[m]['dash'] < DASH_T for m in alive):
                        o = ag[tg]; ddx, ddy = o['x'] - s['x'], o['y'] - s['y']
                        if 60 < abs(ddx) < 200 and abs(ddy) < 80:
                            s['atk'] = t; s['struck'] = False; s['avic'] = tg; s['face'] = 1 if ddx > 0 else -1
                            s['vx'] *= 0.3; s['vy'] *= 0.3
                            s['cd'] = t + ATK_LEN + rnd.uniform(0.3, 0.9)
                            events.append((t, 'wind', n, tg))
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            # soft separation (bodies don't overlap; a planted attacker is heavier)
            for i, a in enumerate(alive):
                for b in alive[i + 1:]:
                    A_, B_ = ag[a], ag[b]; dx, dy = B_['x'] - A_['x'], B_['y'] - A_['y']; d = math.hypot(dx, dy)
                    if 0 < d < COLL:
                        ux, uy = dx / d, dy / d; push = (COLL - d)
                        wa = 0.2 if t - A_['atk'] < ATK_LEN else 0.5; wb = 0.2 if t - B_['atk'] < ATK_LEN else 0.5
                        tot = wa + wb; A_['x'] -= ux * push * wa / tot; A_['y'] -= uy * push * wa / tot; B_['x'] += ux * push * wb / tot; B_['y'] += uy * push * wb / tot
            for n in alive:
                s = ag[n]
                for g in list(gums):
                    if math.hypot(g['x'] - s['x'], g['y'] - s['y']) < 46 and t >= s['sleep'] and t - s['stun'] > 0.6 and not s['ate'] and (n != 'cyrus' or g['k'] == 'mush') and (g['who'] is None or g['who'] == n):
                        gums.remove(g); events.append((t, 'gum', n, g['k'])); s['ate'] = True
                        if G['next'] < 1e8: G['next'] = max(G['next'], t + 0.8)   # n15c: a pickup is its own beat (no strike lands on it)
                        if g['k'] == 'cre': s['buff'] = 'cre'; s['bt'] = t; s['pow'] = 1.7            # STRENGTH!: harder strike
                        if g['k'] == 'cre' and G['next'] > 1e8: G['open'] = n
                        elif g['k'] == 'mush': s['buff'] = 'mush'; s['bt'] = t                         # SPEED!: one dash
                        elif g['k'] == 'acv': s['shield'] = t                                          # SHIELD!: blocks the next strike
                        elif g['k'] == 'mel':                                                          # SLEEP!: everyone else naps 1s
                            for m in alive:
                                if m != n: ag[m]['sleep'] = t + SLEEP_T; ag[m]['atk'] = -9.0
                        s['cd'] = min(s['cd'], t + 0.2)
                if math.hypot(s['x'] - CX, s['y'] - CY) > OUT_R:
                    s['out'] = t; outs.append((n, t)); events.append((t, 'splash', n, None)); G['next'] = max(G['next'], t + 0.6)
        for n in NAMES:
            s = ag[n]
            if s['out'] is not None:   # keeps a little momentum while it drops into the water
                k_ = math.exp(-9.0 * dt); s['vx'] *= k_; s['vy'] *= k_
                s['x'] += s['vx'] * dt; s['y'] += s['vy'] * dt
        frames.append(({n: dict(x=ag[n]['x'], y=ag[n]['y'], vx=ag[n]['vx'], vy=ag[n]['vy'], out=ag[n]['out'], stun=ag[n]['stun'], buff=ag[n]['buff'], dist=ag[n]['dist'],
                            atk=ag[n]['atk'], face=ag[n]['face'], hit=ag[n]['hit'], shield=ag[n]['shield'], sleep=ag[n]['sleep'], dash=ag[n]['dash'], dodge=ag[n]['dodge']) for n in NAMES}, [dict(g) for g in gums]))
        alive = [n for n in NAMES if ag[n]['out'] is None]
        if len(alive) == 1 and t > outs[-1][1] + 2.4: break
    win = [n for n in NAMES if ag[n]['out'] is None]
    return frames, events, outs, (win[0] if len(win) == 1 else None)
def score(seed):
    fr, ev, outs, win = sim(seed)
    if not win or win != 'joy': return None
    if len(outs) != 3 or not (9.0 <= outs[-1][1] <= 12.6): return None
    ts = [o[1] for o in outs]
    if ts[0] < 2.0 or min(b - a for a, b in zip(ts, ts[1:])) < 1.5: return None
    sh = [e for e in ev if e[1] == 'shove']
    if len(sh) < 5: return None
    wh = sum(1 for e in ev if e[1] == 'whiff')
    if wh > 3: return None
    acv = [e[0] for e in ev if e[1] == 'gum' and e[3] == 'acv']
    for e in ev:   # n15b: the shield is on screen a beat before it blocks, and the blocked guide isn't out right after
        if e[1] == 'block' and (not acv or e[0] - acv[0] < 0.8 or any(o[0] == e[2] and 0 <= o[1] - e[0] < 1.0 for o in outs)): return None
    for n, to in outs:   # every OUT comes from a strike (victim knocked out within 1.2s of being hit)
        if not any(e[3] == n and 0 <= to - e[0] < 1.2 for e in sh): return None
    gm = [(e[2], e[3]) for e in ev if e[1] == 'gum']
    if len(gm) != 4 or len(set(n for n, k in gm)) != 4: return None   # each power once, four different guides
    if ('cyrus', 'mush') not in gm: return None
    d = [e for e in ev if e[1] == 'dash']
    if len(d) != 1 or d[0][2] != 'cyrus' or d[0][3] != 'joy' or d[0][0] < outs[1][1]: return None   # Cyrus's dash comes in the final, at Joy
    if not any(e[1] == 'dodge' and e[2] == 'joy' for e in ev): return None
    if outs[-1][0] != 'cyrus': return None
    act = [e for e in ev if e[1] in ('wind', 'shove', 'whiff', 'dash')]   # n15c: the opener is one beat: Rayleigh eats STRENGTH, plants, strikes Cyrus
    g0 = [e for e in ev if e[1] == 'gum'][0]
    if g0[2] != 'ray' or g0[3] != 'cre' or not act or act[0][1] != 'wind' or act[0][2] != 'ray' or act[0][3] != 'cyrus' or act[0][0] < g0[0]: return None
    if len(act) < 2 or act[1][1] != 'shove' or act[1][2] != 'ray': return None
    if any(e[1] == 'whiff' for e in ev): return None
    f1 = int(act[1][0] * FPS)   # the opener drives Cyrus to the edge (not out)
    if max(math.hypot(fr[f][0]['cyrus']['x'] - CX, fr[f][0]['cyrus']['y'] - CY) for f in range(f1, min(len(fr), f1 + 36))) < RR - 70: return None
    blk = [e for e in ev if e[1] == 'block']
    return win, [(o[0], round(o[1], 1)) for o in outs], len(sh), wh, gm, round(d[0][0], 1), len(blk)
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, OUTS, WIN = sim(SEED)
print('winner', WIN, OUTS)
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WHO STAYS IN', 'THE RING?'], accent=1, size=64)   # n15: a question (was the rule LAST ONE IN / THE RING WINS); PICK A PLAYER! cut   # hfg10: soft fade, COMMENT YOUR PICK cut (caption asks)   # rc10: 46px comment line; SHOVING ALLOWED moves to the opening plate
CH0 = HB + 10; CH1 = CH0 + 96
print('hook bottom', HB, 'chips', CH0, CH1, 'deck', CX - RR - 26, CY - RR - 26, CX + RR + 26, CY + RR + 26)
def clampx(x, w, y): return max(70 + w / 2 + 8, min((887 if y > 1110 else 1025) - w / 2 - 8, x))
SS = 3; FOOT = 78 * SS   # rc10: guides 2x -> 3x
SRUN = {g: seq(PL + f'race/{g}_run', SS, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', SS, 1, 9) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS, 1, 9) for g in NAMES}
ATK = {g: seq(PL + f'race/{g}_atk', SS, 0) for g in NAMES}      # n15: Syeda/PixelLab attack frames (13, facing right; feet y104 in the 128 canvas)
ATKL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in ATK.items()}
BCX = {'joy': 34.5, 'cyrus': 29.0, 'cleo': 31.0, 'ray': 29.5}
def atk_frame(a):
    if a < ATK_WIND: return 0 if a < ATK_WIND * 0.5 else 1
    if a < ATK_WIND + 0.3: return 2 + min(5, int((a - ATK_WIND) / 0.3 * 6))
    return 8 + min(4, int((a - ATK_WIND - 0.3) / (ATK_LEN - ATK_WIND - 0.3) * 5))
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RINGC[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 32) for n in NAMES}; HEAD = {n: face(n, 42) for n in NAMES}
# ground: deck disc inside lake from the Wang tileset
T = wang(SP + 'fork_a9/gen/deck_meta.json', SP + 'fork_a9/gen/deck_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
TS = 64; AY0 = 470; GC, GR = 17, 23
def lowc(i, j):
    x, y = i * TS - 4, AY0 + j * TS
    return (x - CX) ** 2 + (y - CY) ** 2 < (RR + 26) ** 2
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (40, 110, 180, 255)); DECK = Image.new('RGBA', (W, H))
WT = ImageEnhance.Brightness(T[(False, False, False, False)]).enhance(0.82); DT = T[(True, True, True, True)]
for j in range(GR):
    for i in range(GC):
        fl = (i + j) % 2
        GROUND.alpha_composite(WT.transpose(Image.FLIP_LEFT_RIGHT) if fl else WT, (i * TS - 4, AY0 + j * TS))
        DECK.alpha_composite(DT.transpose(Image.FLIP_LEFT_RIGHT) if fl else DT, (i * TS - 4, AY0 + j * TS))
DR = RR + 26
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([CX - DR, CY - DR, CX + DR, CY + DR], fill=255)
layer(GROUND, lambda d: d.ellipse([CX - DR - 10, CY - DR + 6, CX + DR + 10, CY + DR + 26], fill=(10, 40, 70, 150)))
GROUND.paste(DECK, (0, 0), mask)
layer(GROUND, lambda d: (d.ellipse([CX - DR, CY - DR, CX + DR, CY + DR], outline=(70, 40, 20, 255), width=10), d.ellipse([CX - DR + 8, CY - DR + 8, CX + DR - 8, CY + DR - 8], outline=(150, 100, 55, 255), width=4)))
LILY = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(SP + 'fork4/lilypad/*.png'))[:3]]
rr = random.Random(4)
for k in range(9):
    while True:
        x, y = rr.uniform(40, W - 40), rr.uniform(AY0 + 40, H - 160)
        if math.hypot(x - CX, y - CY) > RR + 110: break
    lp = LILY[k % len(LILY)]; GROUND.alpha_composite(lp, (int(x - lp.width / 2), int(y - lp.height / 2)))
gd = ImageDraw.Draw(GROUND)
# rope ring + center mark painted on the deck
def deco(d):
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(240, 220, 170, 255), width=8)
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(120, 80, 40, 255), width=3)
    d.ellipse([CX - 70, CY - 70, CX + 70, CY + 70], outline=(240, 220, 170, 160), width=5)
layer(GROUND, deco)
HDR = bg_frames('found_hd.gif', (W, 470), box=(0, 120, 1920, 120 + 835), step=2, bright=0.7)
GUM = {k: gummy(k, 3) for k in ['mush', 'cre', 'mel']}   # rc10: gummies 2x -> 3x
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
GUM['acv'] = up(acv_gummy_strong(), 3)   # Syeda's ACV gummy with gummy shine
VICF = vic(WIN, 330)
T_LAST = OUTS[-1][1]; T_WIN = T_LAST + 0.7; END = T_WIN + float(os.environ.get('HOLD', '2.1'))   # n15c: JOY WINS! held 2.1s (FIX_COMMON endings rule)   # n15b: win held 0.7s, then a hard cut back to the start
V0 = float(os.environ.get('V0', '0.5'))   # n15b: idle first 0.5s cut, the reel opens on the charge
# rc10: one stamp slot under the IN/OUT panel; OUT stamps and power stamps queued so they never overlap
PWS = {'cre': ('STRENGTH!', (255, 110, 50)), 'mush': ('SPEED!', (255, 200, 60)), 'acv': ('SHIELD!', (110, 235, 110)), 'mel': ('SLEEP!', (200, 140, 255))}
SEV = []   # (time, kind, guide, text, colour, min duration): n15b every stamp carries the guide's face
for e in EV:
    if e[1] == 'gum' and e[3] != 'mush': SEV.append((e[0], 'gum', e[2], PWS[e[3]][0], PWS[e[3]][1], 0.9))
    if e[1] == 'gum' and e[3] == 'mush':   # n15c: SPEED! on the pickup frame, held through the dash
        dd_ = [x for x in EV if x[1] == 'dash' and x[2] == e[2]]
        SEV.append((e[0], 'gum', e[2], 'SPEED!', PWS['mush'][1], (dd_[0][0] + DASH_T + 0.3 - e[0]) if dd_ else 0.9))
    if e[1] == 'block': SEV.append((e[0], 'block', e[2], 'BLOCKED!', (110, 235, 110), 0.8))
    if e[1] == 'splash': SEV.append((e[0], 'out', e[2], LABEL[e[2]] + ' IS OUT!', (255, 90, 80), 1.2))
SEV.sort(key=lambda x: x[0]); STAMPS = []
for (t0, kind, n, txt, col, dur) in SEV:
    if kind == 'block' and STAMPS and STAMPS[-1][1] > t0: t0 = max(t0, STAMPS[-1][0] + 0.45)   # n15b: SHIELD! stays readable before BLOCKED!
    if kind in ('out', 'block') and STAMPS and STAMPS[-1][1] > t0:   # an OUT or BLOCKED always shows the moment it happens: cut the earlier stamp short
        a_ = STAMPS[-1]; STAMPS[-1] = (a_[0], t0) + a_[2:]
    t1 = max(t0, STAMPS[-1][1]) if STAMPS else t0
    if kind == 'out' and n == OUTS[-1][0]: dur = T_WIN - t1
    STAMPS.append((t1, t1 + dur, txt, col, n))
print('stamps', [(round(a - V0, 2), round(b - V0, 2), c) for a, b, c, _, _n in STAMPS])
SY = CH1 + 8
wr = Writer(os.environ.get('OUTV', 'v89_noaudio.mp4')); out_ev = []
BUSY = [0, 20] + [int(e[0] * FPS) + 3 for e in EV if e[1] == 'gum'][:2] + [int(T_LAST * FPS) + 8, int(END * FPS) - 1]
sh_items = [e for e in EV if e[1] == 'shove']
ONLY = [int(x) for x in os.environ.get('ONLY', '').split(',') if x]
for f in range(int(round(V0 * FPS)), int(END * FPS)):
    if ONLY and f not in ONLY: continue
    t = f / FPS; st, gums = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    def water(d):
        r2 = random.Random(7)
        for _ in range(110):
            x, y = r2.uniform(0, W), r2.uniform(AY0, H)
            if math.hypot(x - CX, y - CY) < RR + 40: continue
            ph = r2.uniform(0, 6.28); a = int(120 + 120 * math.sin(t * 3 + ph))
            if a > 150: d.rectangle([x, y, x + 6, y + 3], fill=(230, 250, 255, a - 60))
        for n in NAMES:
            s = st[n]
            if s['out'] is not None:
                if t - s['out'] > 1.2: continue   # n15c: ripples fade where they went in; no parked heads
                for k in range(3):
                    u = ((t - s['out']) * 0.8 + k / 3) % 1.0; rr_ = 20 + 60 * u
                    d.ellipse([s['x'] - rr_, s['y'] - rr_ * 0.5, s['x'] + rr_, s['y'] + rr_ * 0.5], outline=(230, 250, 255, int(200 * (1 - u))), width=3)
    layer(img, water)
    for g in gums:
        gi = GUM[g['k']]; bob = int(6 * math.sin(t * 5 + g['x']))
        layer(img, lambda d, g=g: d.ellipse([g['x'] - 30, g['y'] - 16 - 6, g['x'] + 30, g['y'] + 16 - 6], fill=(255, 220, 120, 90)))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height - 4 + bob)))
    layer(img, lambda d: [d.ellipse([st[n]['x'] - 40, st[n]['y'] - 11, st[n]['x'] + 40, st[n]['y'] + 11], fill=(0, 0, 0, 80)) for n in NAMES if st[n]['out'] is None])
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if WIN and t >= T_WIN and s['out'] is None: continue   # n15c: the win zoom replaces the in-game sprite (no second Joy)
        if s['out'] is not None:
            u = t - s['out']
            if u < 0.6:   # n15b: splash where they go in: droplets + ring at the water line
                k_ = u / 0.6
                layer(img, lambda d, x=x, y=y, k_=k_: (d.ellipse([x - 40 - 90 * k_, y - 14 - 26 * k_, x + 40 + 90 * k_, y + 14 + 26 * k_], outline=(235, 250, 255, int(230 * (1 - k_))), width=7),
                    [d.rectangle([x + math.cos(j * 0.5236) * (30 + 120 * k_) - 7, y - 40 - (210 * k_ - 300 * k_ * k_) * (1.2 if j % 2 else 0.8) - 7, x + math.cos(j * 0.5236) * (30 + 120 * k_) + 7, y - 40 - (210 * k_ - 300 * k_ * k_) * (1.2 if j % 2 else 0.8) + 7], fill=(235, 250, 255, int(255 * (1 - k_)))) for j in range(12)]))
            if u < 0.25:
                spr = PANIC[n][int(t * 14) % 8]; sink = int(u / 0.25 * 180)
                c = spr.crop((0, 0, spr.width, max(1, FOOT - sink))); img.alpha_composite(c, (int(x - spr.width / 2), int(y - FOOT + sink)))
                layer(img, lambda d, x=x, y=y: d.ellipse([x - 56, y - 16, x + 56, y + 16], fill=(40, 110, 180, 255)))   # water line over the feet
            continue   # n15c: no floating heads after they sink (the IN/OUT row shows OUT)
        atk_a = t - s['atk']; hop = 0
        da = t - s['dash']; dashing = 0 <= da < DASH_T; skid = DASH_T <= da < DASH_T + SKID_T; dodging = 0 <= t - s['dodge'] < 0.32
        v_ = math.hypot(s['vx'], s['vy']) or 1
        if WIN and t >= T_WIN: spr = STAND[n]
        elif t < s['sleep'] and t - s['stun'] >= 0.6: spr = STAND[n]   # SLEEP: stands asleep
        elif dashing or dodging: ph = int(t * 24) % 8; spr = (FRUN[n][ph] if s['vy'] > 0.75 * v_ else (SRUNL if s['vx'] < 0 else SRUN)[n][ph])
        elif skid: spr = (FRUN[n][0] if s['vy'] > 0.75 * v_ else (SRUNL if s['vx'] < 0 else SRUN)[n][2])
        elif t - s['stun'] < 0.6:
            spr = PANIC[n][int(t * 14) % 8]; u_ = t - s['hit']
            if 0 <= u_ < 0.32: hop = int(46 * math.sin(math.pi * u_ / 0.32))   # knocked off their feet for a moment
        elif 0 <= atk_a < ATK_LEN: spr = None
        else:
            ph = int(s['dist'] / 22) % 8; v = math.hypot(s['vx'], s['vy']) or 1
            spr = FRUN[n][ph] if s['vy'] > 0.75 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        if dashing or skid or dodging:   # dust kicked up by the dash / sidestep, speed lines on the dash
            layer(img, lambda d, x=x, y=y: [d.ellipse([x - s['vx'] * 0.05 * (k + 1) - 18 + 4 * k, y - 12, x - s['vx'] * 0.05 * (k + 1) + 18 - 4 * k, y + 6], fill=(230, 220, 200, 160 - 40 * k)) for k in range(3)])
        if dashing:
            ux, uy = s['vx'] / v_, s['vy'] / v_
            layer(img, lambda d, x=x, y=y, ux=ux, uy=uy: [d.line([x - ux * (50 + 20 * k) - uy * oy, y - 120 + oy * 0.4 - uy * (50 + 20 * k) + ux * oy, x - ux * (150 + 20 * k) - uy * oy, y - 120 + oy * 0.4 - uy * (150 + 20 * k) + ux * oy], fill=(255, 240, 180, 230), width=7) for k, oy in enumerate((-60, 0, 60))])
        if s['buff'] and not (s['buff'] == 'mush' and s['dash'] > 0 and da >= DASH_T + SKID_T):
            col = (255, 210, 60) if s['buff'] == 'mush' else (255, 80, 40)
            layer(img, lambda d, x=x, y=y, col=col: d.ellipse([x - 62, y - 22, x + 62, y + 22], outline=col + (230,), width=6))
            v = math.hypot(s['vx'], s['vy'])
            if False:          # n15b: SPEED shows on the dash
                ux, uy = s['vx'] / v, s['vy'] / v
                def spl(d, x=x, y=y, ux=ux, uy=uy):
                    for k, oy in enumerate((-160, -110, -60)):
                        x0, y0 = x - ux * 40, y + oy - uy * 20
                        d.line([x0, y0, x0 - ux * (60 + 15 * k), y0 - uy * (60 + 15 * k)], fill=(255, 230, 160, 220), width=5)
                    for k in range(4):
                        r_ = 9 + 5 * k; cx_, cy_ = x - ux * (30 + 26 * k), y - uy * (30 + 26 * k) - 4
                        d.ellipse([cx_ - r_, cy_ - r_ * 0.6, cx_ + r_, cy_ + r_ * 0.6], fill=(230, 210, 170, 150 - 30 * k))
                layer(img, spl)
            if s['buff'] == 'cre':                       # STRONG!: rc10: red/orange power flames rising off the body (no oval: an oval read as the ACV shield)
                def flames(d, x=x, y=y):
                    r3 = random.Random(int(t * 15) + int(x))
                    for k in range(9):
                        fx = x + r3.uniform(-62, 62); fy = y - r3.uniform(20, FOOT - 20); L = r3.uniform(26, 54)
                        c = r3.choice([(255, 80, 40), (255, 140, 40), (255, 200, 80)])
                        d.polygon([(fx - 7, fy), (fx + 7, fy), (fx, fy - L)], fill=c + (215,))
                layer(img, flames)
        if t - s['stun'] < 0.6 and math.hypot(s['vx'], s['vy']) > 80:   # skid dust while sliding back
            layer(img, lambda d, x=x, y=y: [d.ellipse([x - 12 - 8 * k - s['vx'] * 0.05 * k, y - 10, x + 12 + 8 * k - s['vx'] * 0.05 * k, y + 6 - 0 * k], fill=(230, 220, 200, 140 - 35 * k)) for k in range(3)])
        if spr is None:   # planted attack
            fi = atk_frame(atk_a)
            if s['face'] > 0: spr = ATK[n][fi]; ox = BCX[n] * SS
            else: spr = ATKL[n][fi]; ox = (128 - BCX[n]) * SS
            if atk_a < 0.2: layer(img, lambda d, x=x, y=y: [d.ellipse([x + q * 34 - 16, y - 8, x + q * 34 + 16, y + 6], fill=(230, 220, 200, int(150 * (1 - atk_a / 0.2)))) for q in (-1, 1)])
            img.alpha_composite(spr, (int(x - ox), int(y - 104 * SS)))
        else: img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT - hop)))
        if 0 <= t - s['shield'] < SHIELD_T and not (WIN and t >= T_WIN):   # SHIELD bubble
            cy_ = y - 108; r_ = 116 + 3 * math.sin(t * 6)
            layer(img, lambda d, x=x, cy_=cy_, r_=r_: (d.ellipse([x - r_, cy_ - r_, x + r_, cy_ + r_], fill=(110, 235, 110, 50), outline=(150, 255, 150, 230), width=7), d.arc([x - r_ + 20, cy_ - r_ + 20, x + r_ - 20, cy_ + r_ - 20], 200, 250, fill=(235, 255, 235, 230), width=7)))
        if t < s['sleep'] and t - s['stun'] >= 0.6:   # SLEEP Zzz
            zz = []
            for q in range(3):
                u = ((t - s['sleep'] + SLEEP_T) * 1.3 + q / 3) % 1.0
                zz.append((x + 34 + 36 * u, y - FOOT + 20 - 80 * u, 'Z', 48 - 8 * q, (220, 200, 255), 7, int(255 * min(1, 2 * (1 - u)))))
            text_layer(img, zz)
    items = []
    for e in EV:
        u = t - e[0]
        if 0 <= u < 0.8:
            a = int(255 * min(1, (0.8 - u) / 0.3))
            s = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[2]]
            yy = s['y'] - FOOT - 30 - u * 40
            if e[1] == 'shove' and s['buff'] != 'cre' and u < 0.25:   # n15: every landed strike gets a small white impact
                v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[3]]; ix, iy = v['x'] - s['face'] * 30, v['y'] - FOOT * 0.5; k_ = 1 - u / 0.25
                layer(img, lambda d, ix=ix, iy=iy, k_=k_: [d.line([ix + math.cos(j * 0.785) * 20, iy + math.sin(j * 0.785) * 20, ix + math.cos(j * 0.785) * (30 + 50 * (1 - k_)), iy + math.sin(j * 0.785) * (30 + 50 * (1 - k_))], fill=(255, 255, 255, int(255 * k_)), width=8) for j in range(8)])
            if e[1] == 'shove' and s['buff'] == 'cre':     # rc10: only STRONG shoves get a pop: POW! 52px + orange impact burst (SHOVE! pops cut)
                v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[3]]; ix, iy = (s['x'] + v['x']) / 2, (s['y'] + v['y']) / 2 - FOOT * 0.45
                if u < 0.35:
                    k_ = 1 - u / 0.35
                    def burst(d, ix=ix, iy=iy, k_=k_):
                        pts = []
                        for j in range(16):
                            rr_ = (95 if j % 2 == 0 else 42) * (0.6 + 0.6 * (1 - k_)); an = j * math.pi / 8
                            pts.append((ix + rr_ * math.cos(an), iy + rr_ * math.sin(an)))
                        d.polygon(pts, fill=(255, 150, 40, int(230 * k_)), outline=(255, 240, 160, int(255 * k_)))
                    layer(img, burst)
                items.append((clampx(s['x'], 4 * 52, yy), max(SY + 104, yy - 20), 'POW!', 52, (255, 120, 50), 8, a))
        if e[1] == 'block' and 0 <= u < 0.6:   # shield pops
            v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[2]]; px, py = v['x'], v['y'] - 108; rad = 120 + 160 * u; al = int(230 * (1 - u / 0.6))
            layer(img, lambda d, px=px, py=py, rad=rad, al=al: [d.rectangle([px + math.cos(a_) * rad - 8, py + math.sin(a_) * rad - 8, px + math.cos(a_) * rad + 8, py + math.sin(a_) * rad + 8], fill=(150, 255, 150, al)) for a_ in [k_ * 0.628 for k_ in range(10)]])
        if e[1] == 'gum' and 0 <= u < 0.6:   # pickup ring in the power's colour
            v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[2]]; bx, by = v['x'], v['y'] - 110; rad = 50 + 240 * u; al = int(220 * (1 - u / 0.6)); col = PWS[e[3]][1]
            layer(img, lambda d, bx=bx, by=by, rad=rad, al=al, col=col: d.ellipse([bx - rad, by - rad, bx + rad, by + rad], outline=col + (al,), width=10))
        if abs(t - e[0]) < 0.5 / FPS:
            if e[1] in ('shove', 'gum', 'splash', 'whiff', 'block', 'dash'): out_ev.append((round(e[0] - V0, 3), {'shove': 'punch', 'gum': 'powerup_8bit', 'splash': 'boom', 'whiff': 'swish', 'block': 'poof', 'dash': 'whoosh_8bit'}[e[1]]))
    text_layer(img, items)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: d.rectangle([0, CH0, W, CH1], fill=(12, 8, 24, 170)))   # hfg10: IN/OUT standings on an edge-to-edge strip, no box
    chips = []
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray']):
        sx = 78 + 939 * (i + 0.5) / 4; ic = ICON[n] if st[n]['out'] is None else ImageEnhance.Brightness(ImageEnhance.Color(ICON[n]).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(sx - 90 - ic.width / 2), CH0 + 20))
        out = st[n]['out'] is not None and st[n]['out'] <= t
        chips.append((sx + 22, CH0 + 26, 'OUT' if out else 'IN', 44, (255, 90, 80) if out else (140, 230, 120), 7, 255))   # rc10: 30 -> 44px
        if WIN and t >= T_WIN and n == WIN: layer(img, lambda d, sx=sx: d.ellipse([sx - 130, CH0 + 12, sx - 50, CH0 + 92], outline=(255, 214, 60, 255), width=6))
    text_layer(img, chips)
    if False: pass   # n15: PICK A PLAYER! cut (generic pick prompt)   # in the stamp slot over open water, not over the guides (first stamp is at 3.2s)   # hfg10: plate + SHOVING ALLOWED cut (the shoving shows)
    for (t1, t2, txt, col, sn) in STAMPS:
        if t1 <= t < t2 and t < T_WIN:
            sc = 1.0 + 0.25 * max(0, 0.12 - (t - t1)) / 0.12; fs_ = int((56 if 'OUT' in txt else 60) * sc); ic = ICON[sn]
            tw_ = ImageDraw.Draw(img).textlength(txt, font=F(fs_)); bw = tw_ + ic.width + 24; lx = int(547 - bw / 2)
            img.alpha_composite(ic, (lx, SY + 46 - ic.height // 2))   # n15b: the guide's face on every stamp
            text_layer(img, [(lx + ic.width + 24 + tw_ / 2, SY + 46 - fs_ // 2, txt, fs_, col, 10, 255)])   # hfg10: stamp without plate
    if t >= T_WIN:
        u = t - T_WIN
        layer(img, lambda d: d.rectangle([0, CH1 + 6, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1170 - vf.height))
        def conf(d):
            r2 = random.Random(f)
            for _ in range(45):
                x, y = r2.uniform(0, W), (r2.uniform(470, H) + u * 500) % H
                d.rectangle([x, y, x + 10, y + 10], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (190, 90, 240)]) + (255,))
        layer(img, conf)
        text_layer(img, [(CX, 1206, LABEL[WIN] + ' WINS!', int(66 * (1 + 0.3 * max(0, 0.12 - u) / 0.12)), (255, 214, 60), 9, 255)])
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN - V0, 3), 'victory'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if ONLY: img.convert('RGB').save(f'f89_{f}.png')
wr.close(); json.dump({'events': sorted(e for e in out_ev if e[0] >= 0)}, open('v89_ev.json', 'w')); print('done', round(END - V0, 2))
