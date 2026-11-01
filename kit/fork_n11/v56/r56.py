import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); sys.path.insert(0, SP + 'fork_rc2'); from rc2 import hook_layer2, acv_gloss, acv_tag
from PIL import Image, ImageDraw, ImageEnhance
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_n11/v56/'
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
VY0 = 0; VH = H
from hook import hook_fade
HOOK, HB = hook_fade(['CAN YOU CALL', 'THE WINNER?'], accent=1)   # Oct 29 notes2: job hook (was CHOOSE YOUR / CHAMPION)
P0, P1 = HB + 10, HB + 118   # rank panel (bigger faces + 44px places)
LEADY = 1335
Y_START, Y_F = 1100, int(os.environ.get('YF', '4300'))
WORLD_H = Y_F + 1500
def cx(y): return 478 + 70 * math.sin(y / 820) + 25 * math.sin(y / 330 + 1.3)
HW = 300
BK = 4; GK3 = 3          # barrels 3x -> 4x, guides in them 2x -> 3x (review: zoom ~1.4x on the pack)
CL = HW - 118            # barrel centre clamp from the river centre

# ---------------- physics (content pass): real circle collisions, barrels bounce off rocks, gummy powers per SPEC 12
def _crop(im): return im.crop(im.getbbox())
ROCK_IDS = (5, 10, 0, 23)
ROCK_R = [max(_crop(Image.open(SP + f'fork_a6/rock/{i:02d}.png')).size) * 3 / 2 * 0.95 for i in ROCK_IDS]
RB = 93                                   # barrel collision radius (sprite is 208 px wide)
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRENGTH!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, STRONG_T, SLEEP_T = 1.8, 2.6, 1.1
sys.path.insert(0, SP + 'fork_n11/tools'); from strike import ATK_D, hit_at, frame_idx, REACH; from stamps import schedule, active   # review fix: planted hits, one stamp at a time   # Oct 29 notes2: a shove/smash is a real attack: the hitter stops ~1s and plays Syeda's attack animation, the hit lands on the impact frame
T_GO = 0.05
def course(seed):
    rnd = random.Random(seed * 7 + 1)
    obs = []; y = 1500; kinds = ['rock', 'gum', 'gum', 'pool', 'rock', 'gum', 'rock', 'gum']; i = 0
    gk = ['acv', 'mush', 'cre', 'mel']; rnd.shuffle(gk); step = (Y_F - 350 - 1500) / (len(kinds) - 1)
    while i < len(kinds):
        k = kinds[i % len(kinds)]; i += 1
        if k == 'rock':
            ox = rnd.choice([-1, 1]) * rnd.uniform(60, 130)
            ri = rnd.randrange(4); obs.append(['rock', y + rnd.uniform(-50, 50), ox, ri])
        elif k == 'pool': obs.append(['pool', y, rnd.uniform(-130, 130), 0])
        else:
            g = gk.pop(0) if gk else rnd.choice(['acv', 'mush', 'cre', 'mel'])
            obs.append(['gum', y, rnd.choice([-1, 1]) * rnd.uniform(40, 140), g])
        y += step * rnd.uniform(0.85, 1.15)
    return obs
def sim(seed, dur=22):
    rnd = random.Random(seed)
    obs = course(int(os.environ.get('CSEED', seed)))
    R = {}
    offs = [(-125, 0), (125, 0), (-125, -250), (125, -250)]; rnd.shuffle(offs)   # 2x2 grid start so nobody is hidden
    for k, n in enumerate(NAMES):
        R[n] = dict(y=Y_START + offs[k][1], x=cx(Y_START) + offs[k][0], off=offs[k][0] * 0.8, pad=rnd.uniform(78, 105), ph=rnd.uniform(0, 6.3),
                    vx=0.0, kick=0.0, boost=-9, dizzy=-9, bonk=-9, imm=-9, strong=-9, sleep=-9, shield=False, fin=None, hitcd={}, atk=-9, adir=1, pend=None, lock=None)
    frames = []; events = []; leaders = []; taken = set(); smashed = {}; minclr = 1e9; nbonk = [0]; nshove = [0]; poolused = set()
    rank = NAMES[:]
    def powered(s, t): return t - s['boost'] < SPEED_T or t - s['strong'] < STRONG_T or s['shield']
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_GO:
            for n, s in R.items():
                if s['pend'] is not None and t >= s['pend'][1]:
                    kind_, _, ref_ = s['pend']; s['pend'] = None
                    if kind_ == 'rock': smashed[ref_] = t; events.append((t, 'smash', n, ref_))
                    else:
                        b_ = R[ref_]
                        if b_['fin'] is None:
                            if b_['shield']: b_['shield'] = False; events.append((t, 'block', ref_))
                            else:
                                sgn = 1 if b_['x'] >= s['x'] else -1
                                b_['vx'] += sgn * 430; b_['kick'] -= 200; b_['bonk'] = t; events.append((t, 'shove', ref_, n))
                if s['fin'] is not None:
                    s['y'] += 120 * dt; continue
                c = cx(s['y']); tgt = c + s['off'] + 60 * math.sin(t * 0.7 + s['ph'])
                if n != rank[0] and not powered(s, t):
                    for j, o in enumerate(obs):
                        if o[0] == 'gum' and j not in taken and 0 < o[1] - s['y'] < 480: tgt = cx(o[1]) + o[2]; break
                # steer around rocks ahead (not always in time -> bounces)
                for j, o in enumerate(obs):
                    if o[0] != 'rock' or j in smashed: continue
                    dy_ = o[1] - s['y']
                    if 0 < dy_ < 470:
                        ox = cx(o[1]) + o[2]; need = RB + ROCK_R[o[3]] + 45
                        if abs(tgt - ox) < need:
                            tgt = ox + (need if (ox - cx(o[1])) < 0 else -need)
                        break
                asleep = t < s['sleep']
                if t - s['atk'] < ATK_D and s['lock'] is not None:
                    v_, dy0 = s['lock']; s['y'] = R[v_]['y'] + dy0; s['kick'] = 0; s['vx'] *= 0.8; s['x'] += s['vx'] * dt
                    s['x'] = max(c - CL, min(c + CL, s['x'])); continue
                s['lock'] = None
                if not asleep and t - s['atk'] >= ATK_D: s['x'] += (tgt - s['x']) * 0.05
                s['x'] += s['vx'] * dt; s['vx'] *= 0.9
                sp = 205 + s['pad'] * (1 + 0.3 * math.sin(t * 1.1 + s['ph']))
                if t - s['boost'] < SPEED_T: sp *= 1.75
                if t - s['dizzy'] < 1.3: sp *= 0.12
                if t - s['bonk'] < 0.3: sp *= 0.35
                if asleep: sp = 45
                if t - s['atk'] < ATK_D: sp = 0   # stopped to throw the punch
                s['y'] += (sp + s['kick']) * dt; s['kick'] *= math.exp(-4 * dt)
                s['x'] = max(c - CL, min(c + CL, s['x']))
                strong = t - s['strong'] < STRONG_T
                # pickups
                for j, o in enumerate(obs):
                    if o[0] == 'gum' and j not in taken:
                        ox, oy = cx(o[1]) + o[2], o[1]
                        if math.hypot(s['x'] - ox, s['y'] - oy) < 95 and not powered(s, t) and not asleep:
                            taken.add(j); k_ = o[3]; events.append((t, 'pick', n, k_))
                            if k_ == 'mush': s['boost'] = t
                            elif k_ == 'cre': s['strong'] = t
                            elif k_ == 'acv': s['shield'] = True
                            elif k_ == 'mel':
                                vic = []
                                for m, q in R.items():
                                    if m == n or q['fin'] is not None: continue
                                    if q['shield']: q['shield'] = False; events.append((t, 'block', m))
                                    else: q['sleep'] = t + SLEEP_T; vic.append(m)
                                events.append((t, 'sleepwave', n, vic))
                # whirlpools
                for j, o in enumerate(obs):
                    if o[0] == 'pool':
                        ox, oy = cx(o[1]) + o[2], o[1]
                        if math.hypot(s['x'] - ox, (s['y'] - oy) * 0.9) < 95 and t - s['imm'] > 2.4 and j not in poolused:
                            s['imm'] = t; poolused.add(j)     # one spin per whirlpool (review: DIZZY! fired 5x)
                            if s['shield']: s['shield'] = False; events.append((t, 'block', n))
                            else: s['dizzy'] = t; events.append((t, 'dizzy', n))
                if s['y'] >= Y_F: s['fin'] = t; events.append((t, 'fin', n))
            # ---- planted STRENGTH shove: one victim, level and one body-width away, the far side clear so nobody gets knocked into a third barrel
            live_ = [n for n in NAMES if R[n]['fin'] is None]
            for an in live_:
                a_ = R[an]
                if nshove[0] >= 1 or an == 'cleo' or t - a_['strong'] >= STRONG_T or t - a_['atk'] < ATK_D or t < a_['sleep']: continue
                for bn in live_:
                    if bn == an: continue
                    b_ = R[bn]; dx_ = b_['x'] - a_['x']; reach = REACH[an] * GK3 + 84
                    if abs(b_['y'] - a_['y']) < 60 and 230 < abs(dx_) < min(300, reach) and t >= b_['sleep'] and t - b_['atk'] >= ATK_D:
                        sg = 1 if dx_ > 0 else -1
                        if any(abs(R[q]['y'] - b_['y']) < 300 and 0 < (R[q]['x'] - b_['x']) * sg < 360 for q in live_ if q not in (an, bn)): continue
                        nshove[0] += 1; a_['atk'] = t; a_['adir'] = sg; a_['lock'] = (bn, a_['y'] - b_['y']); a_['pend'] = ('shove', t + hit_at(an), bn)
                        events.append((t, 'atk', an)); break
            # ---- global collision pass: barrels push apart, then rocks (hard, never overlap)
            for it in range(3):
                for i1, n in enumerate(live_):
                    for m in live_[i1 + 1:]:
                        s, o = R[n], R[m]
                        dx_, dy_ = s['x'] - o['x'], (s['y'] - o['y']) * 1.15; d_ = math.hypot(dx_, dy_) or 1
                        if d_ < 2 * RB + 24:   # review fix: barrels never visually overlap
                            nx_, ny_ = dx_ / d_, dy_ / d_
                            if it == 0: s['vx'] += nx_ * 60; o['vx'] -= nx_ * 60
                            p = (2 * RB + 24 - d_) / 2
                            s['x'] += nx_ * p; o['x'] -= nx_ * p; s['y'] += ny_ * p / 1.15; o['y'] -= ny_ * p / 1.15
                for n in live_:
                    s = R[n]; c = cx(s['y']); s['x'] = max(c - CL, min(c + CL, s['x']))
                    strong = t - s['strong'] < STRONG_T; sp = 300
                    for j, o in enumerate(obs):
                        if o[0] != 'rock' or j in smashed: continue
                        ox, oy = cx(o[1]) + o[2], o[1]; rs = RB + ROCK_R[o[3]]
                        dx_, dy_ = s['x'] - ox, s['y'] - oy; d_ = math.hypot(dx_, dy_) or 1
                        if d_ < rs:
                            nx_, ny_ = dx_ / d_, dy_ / d_
                            s['x'] += nx_ * (rs - d_); s['y'] += ny_ * (rs - d_)
                            if it == 0:
                                vy_ = sp + s['kick']; vn = s['vx'] * nx_ + vy_ * ny_
                                if vn < 0:
                                    s['vx'] -= 1.5 * vn * nx_; s['kick'] -= 1.5 * vn * ny_
                                    if t - s['bonk'] > 0.6 and vn < -60 and nbonk[0] < 2:   # still a real bounce every time; only 2 count as BONK! hits
                                        nbonk[0] += 1
                                        if s['shield']: s['shield'] = False; events.append((t, 'block', n, ('rock', s['x'] - nx_ * RB, s['y'] - ny_ * RB)))
                                        else: s['bonk'] = t; events.append((t, 'bonk', n))
            for n in live_:
                s = R[n]
                for j, o in enumerate(obs):
                    if o[0] == 'rock' and j not in smashed:
                        minclr = min(minclr, math.hypot(s['x'] - cx(o[1]) - o[2], s['y'] - o[1]) - RB - ROCK_R[o[3]])
            rank = sorted(NAMES, key=lambda n: (-(1e9 - R[n]['fin']) if R[n]['fin'] is not None else -R[n]['y']))
            if not leaders or leaders[-1] != rank[0]: leaders.append(rank[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], boost=s['boost'], dizzy=s['dizzy'], bonk=s['bonk'], fin=s['fin'], strong=s['strong'], sleep=s['sleep'], shield=s['shield'], atk=s['atk'], adir=s['adir']) for n, s in R.items()}, set(taken), dict(smashed)))
        if all(s['fin'] is not None for s in R.values()) and t > max(s['fin'] for s in R.values()) + 4: break
    return frames, events, obs, leaders, {n: R[n]['fin'] for n in NAMES}, minclr
def score(seed):
    fr, ev, obs, ld, fin, mc = sim(seed)
    if any(v is None for v in fin.values()): return None
    order = sorted(NAMES, key=lambda n: fin[n]); w = order[0]
    if w != os.environ.get('WANT', 'joy'): return None
    tw = fin[w]
    if not (9.6 < tw < 11.8) or fin[order[1]] - tw > 0.6 or len(ld) < 3 or mc < -1: return None
    picks = [e for e in ev if e[1] == 'pick']
    if len(picks) < sum(o[0] == 'gum' for o in obs) or len(set(e[2] for e in picks)) < 3: return None
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sw or len(sw[0][3]) < 2: return None
    nb = sum(e[1] == 'bonk' for e in ev); nst = sum(e[1] in ('smash', 'shove') for e in ev)
    nd = sum(e[1] == 'dizzy' for e in ev)
    if nb > 2 or nst != 1 or nd > 1: return None
    bt = sorted(e[0] for e in ev if e[1] in ('pick', 'shove', 'block', 'dizzy', 'bonk') and e[0] < tw)
    clash = sum(1 for i in range(len(bt) - 1) if bt[i + 1] - bt[i] < 0.8)
    return 'clash', clash, round(tw, 2), round(fin[order[1]] - tw, 2), order, len(ld), nb, nst, sum(e[1] == 'block' for e in ev), sum(e[1] == 'dizzy' for e in ev), [(e[2], e[3]) for e in picks], round(mc, 1)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EVS, OBS, LEAD, FIN, MINCLR = sim(SEED)
ORDER = sorted(NAMES, key=lambda n: FIN[n]); WIN = ORDER[0]; T_WIN = FIN[WIN]
print('order', ORDER, {n: round(FIN[n], 2) for n in NAMES}, 'leaders', LEAD, 'min rock clearance', round(MINCLR, 2))
for e in EVS: print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
# ---------------- world
meta = json.load(open('river_meta.json')); sheet = Image.open('river_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
TS = 64; GC = 18; GR = WORLD_H // TS + 1
def low(i, j):
    x, y = i * TS - 20, j * TS
    return abs(x - cx(y)) < HW + 10
WORLD = Image.new('RGBA', (W, GR * TS), (40, 90, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (low(i, j), low(i + 1, j), low(i, j + 1), low(i + 1, j + 1)); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 5 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        WORLD.alpha_composite(tl, (i * TS - 20, j * TS))
rr = random.Random(7)
TREES = [up(crop(Image.open(p).convert('RGBA')), 1.5) for p in sorted(glob.glob(SP + 'fork2/bigtree/*.png'))]
LILY = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(SP + 'fork4/lilypad/*.png'))]
ROCKS = [up(crop(Image.open(f'rock/{i:02d}.png').convert('RGBA')), 3) for i in (5, 10, 0, 23)]
BANKROCK = [up(crop(Image.open(f'rock/{i:02d}.png').convert('RGBA')), 2) for i in (6, 12, 16, 22)]
for y in range(0, GR * TS, 150):
    c = cx(y)
    for side in (-1, 1):
        if rr.random() < 0.75:
            x = c + side * (HW + rr.uniform(150, 330))
            if 0 < x < W:
                tr = rr.choice(TREES) if rr.random() < 0.6 else rr.choice(BANKROCK)
                WORLD.alpha_composite(tr, (int(x - tr.width / 2), int(y - tr.height / 2)))
for y in range(300, GR * TS, 260):
    c = cx(y); x = c + rr.choice([-1, 1]) * rr.uniform(HW - 60, HW - 20)
    lp = rr.choice(LILY); WORLD.alpha_composite(lp, (int(x - lp.width / 2), int(y)))
# rocks are drawn per frame now (they can be smashed), y-sorted with the barrels
wd = ImageDraw.Draw(WORLD)
for yy, lab in ((Y_START - 60, 'START'), (Y_F, 'FINISH')):
    c = cx(yy)
    for r_ in range(2):
        for k in range(int(2 * HW / 18) + 1):
            x = c - HW + k * 18; col = (245, 245, 245, 255) if (k + r_) % 2 == 0 else (25, 22, 30, 255)
            wd.rectangle([x, yy + r_ * 18, x + 17, yy + r_ * 18 + 17], fill=col)
DOCK = up(crop(Image.open('dock/03.png').convert('RGBA')), 3)
for side in (-1, 1):
    x = cx(Y_F) + side * (HW + 40); WORLD.alpha_composite(DOCK, (int(x - DOCK.width / 2), int(Y_F - DOCK.height + 40)))
# ---------------- sprites
BARREL = up(crop(Image.open('barrel/02.png').convert('RGBA')), BK)
FRONT = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
UPPER = {}
for n, p in FRONT.items():
    im = Image.open(SP + 'syeda_src/' + p).convert('RGBA'); bb = im.getbbox()
    UPPER[n] = up(im.crop((bb[0] - 4, 10, bb[2] + 4, 58)), GK3)
GUM = {k: up(acv_gloss(Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')) if k == 'acv' else Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'), 3) for k in GUMK}
VICF = vic(WIN, 340)
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + FRONT[name]).convert('RGBA')
    bb = im.getbbox(); c_ = (bb[0] + bb[2]) // 2
    head = im.crop((c_ - 15, 12, c_ + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 44) for n in NAMES}; ICS = {n: face(n, 30) for n in NAMES}
HDR = None
ATK = {n: seq(PL + f'race/{n}_atk', GK3, 1) for n in NAMES}   # Syeda-based attack animations (already used in the approved race reels)
ATK_CX = {'joy': 34, 'ray': 30, 'cleo': 31, 'cyrus': 29}   # body centre x in the 128px attack frame
def attack_overlay(img, n, sx, sy, u, adir, bob=0):
    """guide doing their attack in the barrel: upper body of the attack frame above the rim, rim redrawn in front"""
    fr = ATK[n][frame_idx(u, len(ATK[n]))]
    cr = fr.crop((0, 30 * GK3, fr.width, 92 * GK3)); LIFT = 14 * GK3   # stands up in the barrel so the whole swing clears the rim
    if adir < 0: cr = cr.transpose(Image.FLIP_LEFT_RIGHT); x0 = sx - (128 - ATK_CX[n]) * GK3
    else: x0 = sx - ATK_CX[n] * GK3
    bx0, by0 = int(sx - 150), int(sy - 200)
    img.alpha_composite(cr, (int(x0), by0 + 200 - cr.height + 22 + 8 * GK3 + bob - LIFT))
    front = BARREL.crop((0, int(BARREL.height * 0.55), BARREL.width, BARREL.height))
    img.alpha_composite(front, (bx0 + 150 - BARREL.width // 2, by0 + 200 - BARREL.height // 2 + int(BARREL.height * 0.55)))
def boat(n, x, y, t, s, guide=True):
    """barrel with the guide sitting in it, centered at x,y (screen)"""
    B = Image.new('RGBA', (300, 350), (0, 0, 0, 0))
    bx, by = 150 - BARREL.width // 2, 200 - BARREL.height // 2
    B.alpha_composite(BARREL, (bx, by))
    u = UPPER[n]; bob = int(4 * math.sin(t * 6 + x * 0.01))
    if guide: B.alpha_composite(u, (150 - u.width // 2, 200 - u.height + 22 + bob))
    front = BARREL.crop((0, int(BARREL.height * 0.55), BARREL.width, BARREL.height))
    B.alpha_composite(front, (bx, by + int(BARREL.height * 0.55)))
    d = ImageDraw.Draw(B)
    if not guide: return B   # attacking: oars down, the guide is drawn by attack_overlay
    side = 1 if int(t * 2.6 + hash(n) % 7) % 2 else -1
    ph = (t * 2.6) % 1.0
    ox0, oy0 = 150 + side * 35, 173 + bob
    ox1, oy1 = 150 + side * (104 + 21 * math.sin(ph * math.pi)), 160 + 93 * ph
    d.line([ox0, oy0, ox1, oy1], fill=(120, 80, 40, 255), width=8)
    d.ellipse([ox1 - 12, oy1 - 7, ox1 + 12, oy1 + 17], fill=(150, 100, 50, 255), outline=(70, 45, 20, 255), width=3)
    if t - s['dizzy'] < 1.3:
        B = B.rotate(((t - s['dizzy']) * 720) % 360, resample=Image.NEAREST, center=(150, 200))
    return B
# ---------------- render (content pass)
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(0.05, 'cheer'); ev(T_GO, 'whoosh_8bit')
SFX = {'bonk': 'stomp_8bit', 'dizzy': 'whoosh_8bit', 'fin': 'ding_8bit', 'smash': 'crunch_8bit', 'shove': 'punch', 'block': 'boing'}
PSFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
for e in EVS:
    t, k = e[0], e[1]
    if t > T_WIN + 3.0: continue
    if k == 'pick': ev(t, PSFX[e[3]])
    elif k in SFX: ev(t, SFX[k])
    elif k == 'atk': ev(t + hit_at(e[2]) - 0.12, {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'sword_swish', 'cyrus': 'swish'}[e[2]])
ev(T_WIN, 'victory')
T_CARD = T_WIN + 0.15; T_LOOP = T_CARD + 1.9;   # review fix: JOY WINS! fully up >= 1.6s
T_ALL = T_LOOP + 0.3; NF = int(round(T_ALL * FPS))
POPTXT = {'bonk': ('BONK!', (255, 255, 255), 48), 'dizzy': ('DIZZY!', (150, 220, 255), 48), 'smash': ('SMASH!', (90, 160, 255), 48),
          'shove': ('SHOVED!', (255, 255, 255), 48), 'block': ('BLOCKED!', (110, 230, 90), 48)}
RAWS = []   # review fix: one stamp at a time, ~0.3s apart; every power stamp names the guide; no BONK! stamps
for e in EVS:
    t, k = e[0], e[1]
    if t > T_WIN: continue
    if k == 'pick': RAWS.append((t, 'pick', (e[2], LABEL[e[2]] + ': ' + POWER[e[3]][0], POWER[e[3]][1], 46), True))
    elif k in ('shove', 'block'): RAWS.append((t, k, (e[2], ) + POPTXT[k], True))
    elif k == 'dizzy': RAWS.append((t, k, (e[2], ) + POPTXT[k], False))
SCHED = schedule(RAWS, hard_end=T_WIN)
print('stamps', [(round(a, 2), round(b, 2), p_[1]) for a, b, k_, p_ in SCHED])
BLOCKFX = [(e[0], e[3]) for e in EVS if e[1] == 'block' and len(e) > 3 and e[3][0] == 'rock']
POP_D = 1.0
SLEEPW = [e for e in EVS if e[1] == 'sleepwave']
ROCKSPR = ROCKS
cam = 0.0
ACV_SEEN = [None]
ONLY = [int(x) for x in os.environ.get('ONLY', '').split(',') if x]
wr = Writer(OUT + ('only.mp4' if ONLY else 'v56_noaudio.mp4'))
for f in range(NF):
    t = f / FPS
    if t >= T_LOOP: t = 0.0; cam_reset = True
    else: cam_reset = False
    fi = int(round(t * FPS)); st, taken, smashed = FR[min(fi, len(FR) - 1)]
    lead_y = max(st[n]['y'] for n in NAMES)
    tgt = max(0, min(WORLD.height - VH, lead_y - LEADY))
    cam = tgt if (f == 0 or cam_reset) else cam + (tgt - cam) * 0.12
    if ONLY and f not in ONLY: continue
    ACV_TAG = []
    view = WORLD.crop((0, int(cam), W, int(cam) + VH))
    img = Image.new('RGBA', (W, H), (20, 40, 20, 255)); img.alpha_composite(view, (0, VY0))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for o in OBS:
        if o[0] != 'pool': continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0
        if not (VY0 - 150 < sy < H + 150): continue
        for r_ in range(6):
            rad = 20 + r_ * 14; a0 = (t * 220 + r_ * 40) % 360
            dl.arc([sx - rad, sy - rad * 0.7, sx + rad, sy + rad * 0.7], a0, a0 + 230, fill=(225, 245, 255, 200 - r_ * 22), width=5)
        dl.ellipse([sx - 14, sy - 9, sx + 14, sy + 9], fill=(20, 60, 110, 200))
    img.alpha_composite(L)
    # floating gummies + pickup bursts
    for j, o in enumerate(OBS):
        if o[0] != 'gum': continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0 + 6 * math.sin(t * 3 + j)
        if not (VY0 - 100 < sy < H + 100): continue
        col = POWER[o[3]][1]
        if j in taken:
            tp = next((e[0] for e in EVS if e[1] == 'pick' and e[0] <= t + 1e-6 and abs((cx(o[1]) + o[2]) - 0) >= 0 and e[3] == o[3]), None)
            continue
        layer(img, lambda dd, sx=sx, sy=sy, col=col: [dd.ellipse([sx - 50 + k_ * 9, sy - 38 + k_ * 7, sx + 50 - k_ * 9, sy + 38 - k_ * 7], fill=col + (40 + k_ * 25,)) for k_ in range(3)])
        g = GUM[o[3]]; img.alpha_composite(g, (int(sx - g.width / 2), int(sy - g.height / 2)))
        if False and o[3] == 'acv' and P1 + 260 < sy < 1560:   # Oct 29: ACV GUMMY tag cut (SHIELD! names it)
            if ACV_SEEN[0] is None: ACV_SEEN[0] = t
            if t - ACV_SEEN[0] < 1.4: ACV_TAG.append((int(sx), int(sy - g.height / 2 - 8), int(255 * min(1, (t - ACV_SEEN[0]) / 0.12, (1.4 - (t - ACV_SEEN[0])) / 0.25)), 1015 if sy < 1110 else 877))
    for e in EVS:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'], s0['y'] - cam + VY0 - 40; col = POWER[e[3]][1]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    # sleep wave rings
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'], s0['y'] - cam + VY0 - 60
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_ * 0.8, px_ + r_, py_ + r_ * 0.8], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1300 * u, 20 + 900 * u)])
    # rocks + barrels, y-sorted
    items = []
    for j, o in enumerate(OBS):
        if o[0] != 'rock': continue
        sy = o[1] - cam + VY0
        if not (-150 < sy < H + 150): continue
        if j in smashed and t >= smashed[j]:
            u = (t - smashed[j]) / 0.7
            if u < 1:
                sx = cx(o[1]) + o[2]
                layer(img, lambda dd, sx=sx, sy=sy, u=u, j=j: [dd.rectangle([sx + math.cos(q * 0.8 + j) * 200 * u - 10, sy + math.sin(q * 0.8 + j) * 120 * u - 10, sx + math.cos(q * 0.8 + j) * 200 * u + 10, sy + math.sin(q * 0.8 + j) * 120 * u + 10], fill=(120, 116, 104, int(255 * (1 - u)))) for q in range(10)])
            continue
        items.append((o[1], 'rock', j))
    for n in NAMES: items.append((st[n]['y'], 'boat', n))
    off_top = []
    for _, kind, ref in sorted(items, key=lambda it: it[0]):
        if kind == 'rock':
            o = OBS[ref]; r_ = ROCKSPR[o[3]]; x = cx(o[1]) + o[2]; sy = o[1] - cam + VY0
            layer(img, lambda dd, x=x, sy=sy, r_=r_: dd.ellipse([x - r_.width * 0.55, sy + r_.height * 0.25, x + r_.width * 0.55, sy + r_.height * 0.62], fill=(225, 245, 255, 120)))
            img.alpha_composite(r_, (int(x - r_.width / 2), int(sy - r_.height / 2)))
            continue
        n = ref; s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0
        if sy < P1 + 70: off_top.append(n); continue
        if sy > H + 150: continue
        asleep = t < s['sleep']; boosted = t - s['boost'] < SPEED_T; strong = t - s['strong'] < STRONG_T
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for k_ in range(6):
            wy = sy - 66 - k_ * 29; a = (200 - k_ * 32) // (3 if asleep else 1)
            spread = 40 + k_ * 12
            dl.rectangle([sx - spread - 8, wy - 5, sx - spread + 8, wy + 5], fill=(240, 250, 255, a))
            dl.rectangle([sx + spread - 8, wy - 5, sx + spread + 8, wy + 5], fill=(240, 250, 255, a))
        if boosted:
            for k_ in range(6):
                lx = sx - 113 + k_ * 45; ly = sy - 173 - ((t * 700 + k_ * 47) % 220)
                dl.rectangle([lx - 5, ly, lx + 5, ly + 70], fill=(255, 200, 110, 220))
        img.alpha_composite(L)
        attacking = 0 <= t - s['atk'] < ATK_D
        B = boat(n, sx, sy, 0.0 if asleep else t, s, guide=not attacking and not (n == WIN and t >= T_WIN))
        if n == WIN: WINXY = (sx, sy)
        bx0, by0 = int(sx - 150), int(sy - 200)
        if boosted:
            for q in range(3):
                img.alpha_composite(tinted(B, (255, 170, 50), int(255 * (0.32 - 0.09 * q))), (bx0, by0 - int((q + 1) * 34)))
        if strong:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            tt = tinted(B, (16, 24, 80), 255)
            for ox, oy in ((-11, 0), (11, 0), (0, -11), (0, 11), (-8, -8), (8, 8), (-8, 8), (8, -8)): img.alpha_composite(tt, (bx0 + ox, by0 + oy))
            tt = tinted(B, (150, 215, 255), int(200 + 55 * pul))
            for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): img.alpha_composite(tt, (bx0 + ox, by0 + oy))
            layer(img, lambda dd: [dd.rectangle([sx + 126 * math.cos(t * 5 + q * 1.57) - 7, sy - 53 + 146 * math.sin(t * 5 + q * 1.57) - 7, sx + 126 * math.cos(t * 5 + q * 1.57) + 7, sy - 53 + 146 * math.sin(t * 5 + q * 1.57) + 7], fill=(220, 240, 255, 255), outline=(16, 24, 80, 255), width=2) for q in range(4)])
        img.alpha_composite(B, (bx0, by0))
        if attacking: attack_overlay(img, n, sx, sy, t - s['atk'], s['adir'])
        if asleep:
            img.alpha_composite(tinted(B, (40, 20, 90), 120), (bx0, by0))
            u = t - (s['sleep'] - SLEEP_T)
            text_layer(img, [(sx + 66 + 22 * kz, sy - 160 - ((u * 1.4 + kz * 0.33) % 1) * 70 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if s['shield']:
            layer(img, lambda dd: (dd.ellipse([sx - 140, sy - 200, sx + 140, sy + 133], fill=(110, 230, 90, 50), outline=(150, 255, 120, 230), width=8),
                                   dd.arc([sx - 106, sy - 170, sx - 26, sy - 80], 200, 260, fill=(230, 255, 220, 230), width=6)))
        if t - s['bonk'] < 0.5 and t >= s['bonk']:
            u = (t - s['bonk']) / 0.5
            layer(img, lambda dd: [dd.polygon([(sx + math.cos(q * 0.785) * 53, sy - 80 + math.sin(q * 0.785) * 53), (sx + math.cos(q * 0.785 + 0.2) * (107 + 80 * u), sy - 80 + math.sin(q * 0.785 + 0.2) * (107 + 80 * u)), (sx + math.cos(q * 0.785 + 0.39) * 53, sy - 80 + math.sin(q * 0.785 + 0.39) * 53)], fill=(255, 255, 255, int(220 * (1 - u)))) for q in range(8)])
        tag = ICS[n]; tx = sx + 66 if sx < 640 else sx - 130
        if not (n == WIN and t >= T_WIN): img.alpha_composite(tag, (int(tx), int(sy + 40)))
    for tb, (_, bx_, by_) in BLOCKFX:
        if 0 <= t - tb < 0.4:
            u = (t - tb) / 0.4; px_, py_ = bx_, by_ - cam + VY0
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.polygon([(px_ + math.cos(q * 0.785) * 20, py_ + math.sin(q * 0.785) * 20), (px_ + math.cos(q * 0.785 + 0.2) * (60 + 70 * u), py_ + math.sin(q * 0.785 + 0.2) * (60 + 70 * u)), (px_ + math.cos(q * 0.785 + 0.39) * 20, py_ + math.sin(q * 0.785 + 0.39) * 20)], fill=(200, 255, 170, int(255 * (1 - u)))) for q in range(8)])
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW):
        img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    for jx_, jy_, a_, xm_ in ACV_TAG: acv_tag(img, jx_, jy_, a=a_, xmax=xm_)   # drawn above the barrels
    # pop labels (stacked, never overlapping)
    placed = []; items = []
    A_ = active(SCHED, t)
    for t0, en0, _k, (n, text, col, size) in ([A_] if A_ else []):
        u = t - t0
        s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0 - 205 - u * 20
        offtop = s['y'] - cam + VY0 < P1 + 70
        if offtop:                                   # racer is off the top: label sits under their face tag
            size = 44; sx = max(100, min(W - 110, s['x'])); sy = P1 + 112
        w_ = len(text) * size + 20; hh = size + 16
        lim_r = 1015 if sy < 1110 else 877
        sx = min(max(sx, 70 + w_ / 2), lim_r - w_ / 2)
        for _ in range(8):
            if any(abs(sx - px) < (w_ + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): sy += (hh + 6) if offtop else -(hh + 6)
            else: break
        sy = max(sy, P1 + hh / 2 + (86 if off_top else 16))
        if sy > 1490 - hh: continue
        placed.append((sx, sy, w_, hh)); al = int(255 * min(1, (en0 - t) / 0.2)); sc = 1 + 0.15 * max(0, 1 - u / 0.12)
        items.append((sx, sy - hh / 2, text, int(size * sc), col, 8, al))
    if items: text_layer(img, items)
    if t < 0.8:   # review fix: no pop overshoot; settled size fits the safe zone (x ~170-870) on the thumbnail frame
        text_layer(img, [(520, 1290, 'PADDLE!', 100, (120, 220, 255), 10, int(255 * min(1, (0.8 - t) / 0.3)))])
    for k_, n in enumerate(off_top):
        ic = ICS[n]; x = int(max(100, min(W - 110, st[n]['x'])))
        img.alpha_composite(ic, (x - ic.width // 2, P1 + 10))
    rank = sorted(NAMES, key=lambda n: (-(1e9 - st[n]['fin']) if st[n]['fin'] is not None else -st[n]['y']))
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(14, 10, 24, 200)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(rank):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]; img.alpha_composite(ic, (int(x - 112), P0 + 8))
        text_layer(img, [(x + 52, P0 + 32, ['1ST', '2ND', '3RD', '4TH'][i], 44, (255, 214, 60) if i == 0 else (230, 230, 230), 6, 255)])
    if t >= T_WIN:   # review fix: the win pose stands up in Joy's own barrel (the small sprite is hidden), JOY WINS! above her
        u = t - T_WIN; a = min(1, u / 0.15)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(8, 10, 22, int(120 * a))))
        wx, wy = WINXY; Bw = boat(WIN, wx, wy, t, st[WIN], guide=False); img.alpha_composite(Bw, (int(wx - 150), int(wy - 200)))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(wx - vf.width / 2), int(wy + 30 - vf.height)))
        front = BARREL.crop((0, int(BARREL.height * 0.55), BARREL.width, BARREL.height))
        img.alpha_composite(front, (int(wx - BARREL.width / 2), int(wy - BARREL.height / 2 + int(BARREL.height * 0.55))))
        tx_ = min(max(wx, 70 + 300), 877 - 300)
        text_layer(img, [(tx_, int(wy + 30 - vf.height - 90), LABEL[WIN] + ' WINS!', 64, (255, 214, 60), 8, int(255 * a))])
        if True:
            rr2 = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr2.uniform(80, 1010), (rr2.uniform(0, H) + u * 400) % (1480 - P1) + P1
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HOOK)
    wr.write(img)
    if ONLY: img.convert('RGB').save(OUT + f'o_{f:04d}.png')
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p56_{f:04d}.png')
    if os.environ.get('FULL') and any(abs(t - (e[0] + 0.2)) < 0.5 / FPS for e in EVS if e[1] in ('pick', 'smash', 'shove', 'bonk')) and not f >= int(T_LOOP * FPS):
        img.convert('RGB').save(OUT + f'k_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v56_ev.json', 'w'))
print('done', round(T_ALL, 2), len(EV))
