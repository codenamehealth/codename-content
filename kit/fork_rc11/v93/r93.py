import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer; import hook as HK
# rc11 (review recut, Bennett loves #93: winner/feel kept): scramble from frame 0; shorter re-sim (win ~12-14s, Rayleigh);
# power/effect stamps in ONE fixed slot on a dark plate, queued (never overlap); max one small YOINK!/+1 at a time (<=2 stamps);
# no stamps on the win frame; big two-line win banner; win hold 1.4s then cut back to frame 0 (loop); bigger HUD, timer/steals cut;
# 'POWERS ARE ON!' 36 -> 50px.
# #93 Whoever gets 3 gummies wins, powers on: safe zone + hook (source fork_b9/v95/render.py).
# HOLLOW RULE: the Hollow thief (SHADOW STEP) is removed, 4 guides on a diamond of baskets; re-simulated.
# GUMMY POWERS (SPEC 12): each guide's power is now her gummy's power: Cyrus SPEED (was SUN DASH, same burst),
# Cleo STRONG (was SHIELD BASH, same shove-away), Joy SHIELD (was VINE SNARE: green bubble on her basket blocks the next steal),
# Rayleigh SLEEP (was MOON MAP: everyone else falls asleep ~1s with Zzz).
os.chdir(os.path.dirname(os.path.abspath(__file__))); B9 = SP0 + 'fork_b9/v95/'
import numpy as np
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (160, 150, 190)}
POWER = {'joy': 'SHIELD', 'cyrus': 'SPEED', 'cleo': 'STRONG', 'ray': 'SLEEP'}
PGUM = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun') for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
GUMK = ['mush', 'acv', 'mel', 'cre']
sys.path.insert(0, SP0 + 'fork_rc2'); from rc2 import gummy_src   # rc11: gummy gloss on Syeda's ACV gummy
GUM = {k: up(gummy_src(k), 2) for k in GUMK}; GUMS = {k: gummy_src(k) for k in GUMK}
def pick(d, i): return crop(Image.open(PL + f'steal/{d}/{i:02d}.png').convert('RGBA'))
BASKET = up(pick('basket', 1), 3); BLANKET = up(pick('blanket', 0), 3)
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}; ICONS = {n: face(n, 22) for n in NAMES}
# ---------------- desert arena (PixelLab)
AREN = up(Image.open(B9 + '../gen/arena/00.png').convert('RGBA'), 3)
def band(lines, accent, sub, subsize=50, color=(255, 214, 60), subcol=(255, 150, 70)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 24; fs = ImageFont.truetype(HK.FONT, subsize)
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
HOOK, HB = band(['WHOEVER GETS 3', 'GUMMIES WINS'], 1, 'POWERS ARE ON!')
P0 = HB + 8; P1 = P0 + 150
SLOT0 = P1 + 8; SLOT1 = SLOT0 + 86   # rc11: one fixed stamp slot under the roster panel                     # roster/power panel under the hook
CX, CY = 478, 1165; YMIN = 930; AX0, AY0 = CX - 576, CY - 576   # rc11: arena 25px lower + flatter diamond so the stamp slot under the panel never covers a guide
print('hook', HB, 'panel', P0, P1)
GROUND = Image.new('RGBA', (W, H), (176, 104, 52, 255))
GROUND.alpha_composite(AREN, (AX0, AY0))
GROUND.alpha_composite(AREN.crop((AREN.width - 80, 0, AREN.width, AREN.height)).transpose(Image.FLIP_LEFT_RIGHT), (AX0 + AREN.width, AY0))
GROUND.alpha_composite(AREN.crop((0, AREN.height - 260, AREN.width, AREN.height)).transpose(Image.FLIP_TOP_BOTTOM), (AX0, AY0 + AREN.height))
GROUND.alpha_composite(BLANKET, (CX - BLANKET.width // 2, CY - BLANKET.height // 2))
BASE = {}
for k, n in enumerate(NAMES):
    a = -math.pi / 2 + k * 2 * math.pi / 4
    BASE[n] = (CX + 308 * math.cos(a), CY + 240 * math.sin(a))
layer(GROUND, lambda dd: [dd.ellipse([bx - 84, by - 50, bx + 84, by + 50], fill=RING[n] + (120,), outline=RING[n] + (255,), width=5) for n, (bx, by) in BASE.items()])
for n, (bx, by) in BASE.items():
    GROUND.alpha_composite(BASKET, (int(bx - BASKET.width / 2), int(by - BASKET.height / 2 - 6)))
    ic = ICONS[n]; GROUND.alpha_composite(ic, (int(bx - ic.width / 2), int(by + 26)))
# ---------------- simulation with guild powers
T_START = float(os.environ.get('T0', '0.1')); N0 = 8; WINN = 3; CD = 4.5
def sim(seed, dur=40):
    rnd = random.Random(seed)
    kinds = [GUMK[i % 4] for i in range(N0)]; rnd.shuffle(kinds)
    pile = list(kinds); bases = {n: [] for n in NAMES}
    ag = {}
    for n in NAMES:
        bx, by = BASE[n]
        ag[n] = dict(x=bx, y=by + 20, vx=0.0, vy=0.0, carry=None, tgt=None, spd=rnd.uniform(295, 335), ph=rnd.uniform(0, 6.3),
                     greedy=rnd.random() < 0.5, dist=0.0, mode='down', retarget=0.0, cd=T_START + rnd.uniform(1, 3), slow=-9, dash=-9, blink=None, hid=-9, sleep=-9)
    shield = [-9.0]                         # Joy's basket bubble active until shield[0]
    frames = []; events = []; steals = 0; winner = None; leaders = []; used = {n: 0 for n in NAMES}; denied = 0
    def fire(n, t, extra=None):
        used[n] += 1; ag[n]['cd'] = t + CD; events.append((t, 'power', n, extra))
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_START and winner is None:
            for n, s in ag.items():
                if s['carry'] is not None: s['tgt'] = ('home', n)
                elif pile: s['tgt'] = ('pile', None)
                else:
                    if s['tgt'] is None or s['tgt'][0] != 'base' or not bases[s['tgt'][1]] or t > s['retarget']:
                        opts = [m for m in NAMES if m != n and bases[m]]
                        if opts:
                            if s['greedy']: mx = max(len(bases[m]) for m in opts); opts = [m for m in opts if len(bases[m]) == mx]
                            m = min(opts, key=lambda m: math.hypot(BASE[m][0] - s['x'], BASE[m][1] - s['y']) + rnd.uniform(0, 160))
                            s['tgt'] = ('base', m); s['retarget'] = t + rnd.uniform(0.8, 1.6)
                        else: s['tgt'] = ('home', n)
                kind, who = s['tgt']
                tx, ty = (CX, CY) if kind == 'pile' else BASE[who]
                dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                if t - s['sleep'] < 1.0:            # asleep: stops dead
                    s['vx'] = s['vy'] = 0.0; continue
                # SLEEP (melatonin): Rayleigh puts everyone else to sleep for ~1s when carrying far from home
                if n == 'ray' and t >= s['cd'] and s['carry'] is not None and L > 300:
                    fire(n, t)
                    for m in NAMES:
                        if m != 'ray': ag[m]['sleep'] = t
                sp = s['spd'] * (1 + 0.18 * math.sin(1.3 * t + s['ph'])) * (0.9 if s['carry'] else 1.0)
                if t - s['slow'] < 1.4: sp *= 0.25
                if t - s['dash'] < 1.3: sp *= 1.9
                if L < 60: sp *= L / 60 + 0.3
                wob = 0.25 * math.sin(2.7 * t + s['ph'] * 2)
                ux, uy = dx / L, dy / L; ux, uy = ux - uy * wob, uy + ux * wob
                s['vx'] += (ux * sp - s['vx']) * 0.18; s['vy'] += (uy * sp - s['vy']) * 0.18
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                for m, o in ag.items():
                    if m == n: continue
                    ddx, ddy = nx - o['x'], (ny - o['y']) * 1.5; dd = math.hypot(ddx, ddy)
                    if 0 < dd < 52: nx += ddx / dd * (52 - dd) * 0.4; ny += ddy / dd * (52 - dd) * 0.25
                ny = max(YMIN, min(1488, ny)); nx = max(112, min(848 if ny > 1080 else 980, nx))   # stay in the safe zone
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                v = math.hypot(s['vx'], s['vy']) or 1; s['mode'] = 'down' if s['vy'] > 0.75 * v else 'side'
                # SHIELD (ACV): Joy throws a green bubble over her basket when a thief closes in; it blocks the next steal
                if kind == 'base' and who == 'joy' and n != 'joy' and t >= ag['joy']['cd'] and t - ag['joy']['sleep'] >= 1.0 and math.hypot(BASE['joy'][0] - s['x'], BASE['joy'][1] - s['y']) < 200 and bases['joy']:
                    shield[0] = t + 3.5; fire('joy', t, n)
                if kind == 'pile' and math.hypot(CX - s['x'], CY - s['y']) < 70 and pile and s['carry'] is None:
                    s['carry'] = pile.pop(); events.append((t, 'grab', n, None))
                    if n == 'cyrus' and t >= s['cd']: s['dash'] = t; fire(n, t)
                elif kind == 'base' and who != n and math.hypot(BASE[who][0] - s['x'], BASE[who][1] - s['y']) < 62 and s['carry'] is None:
                    if bases[who]:
                        c = ag['cleo']
                        if who == 'joy' and t < shield[0]:
                            shield[0] = t; events.append((t, 'blocked', n, None))
                            ang = math.atan2(s['y'] - BASE['joy'][1], s['x'] - BASE['joy'][0]); s['x'] += 110 * math.cos(ang); s['y'] += 110 * math.sin(ang)
                            s['y'] = max(YMIN, min(1488, s['y'])); s['x'] = max(112, min(848 if s['y'] > 1080 else 980, s['x']))
                        elif who == 'cleo' and t >= c['cd'] and t - c['sleep'] >= 1.0 and math.hypot(c['x'] - BASE['cleo'][0], c['y'] - BASE['cleo'][1]) < 320:
                            fire('cleo', t, n); denied += 1; events.append((t, 'denied', n, None))
                            ang = math.atan2(s['y'] - BASE['cleo'][1], s['x'] - BASE['cleo'][0]); s['x'] += 150 * math.cos(ang); s['y'] += 150 * math.sin(ang)
                            s['y'] = max(YMIN, min(1488, s['y'])); s['x'] = max(112, min(848 if s['y'] > 1080 else 980, s['x']))
                        else:
                            s['carry'] = bases[who].pop(); steals += 1; events.append((t, 'yoink', n, who))
                            if n == 'cyrus' and t >= s['cd']: s['dash'] = t; fire(n, t)
                    s['tgt'] = None
                elif kind == 'home' and math.hypot(BASE[n][0] - s['x'], BASE[n][1] - s['y']) < 55 and s['carry'] is not None:
                    bases[n].append(s['carry']); s['carry'] = None; events.append((t, 'drop', n, None)); s['tgt'] = None
                    if len(bases[n]) >= WINN: winner = (n, t)
            cnt = {n: len(bases[n]) for n in NAMES}; mx = max(cnt.values())
            if mx > 0:
                lead = [n for n in NAMES if cnt[n] == mx]
                if len(lead) == 1 and (not leaders or leaders[-1] != lead[0]): leaders.append(lead[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], carry=s['carry'], dist=s['dist'], mode=s['mode'], slow=s['slow'], dash=s['dash'], blink=s['blink'], hid=s['hid'], sleep=s['sleep']) for n, s in ag.items()},
                       list(pile), {n: list(b) for n, b in bases.items()}, steals, shield[0]))
        if winner and t > winner[1] + 1.6: break
    return frames, events, winner, steals, leaders, used, denied
def score(seed):
    fr, ev, win, st, ld, used, den = sim(seed)
    if not win: return None
    tw = win[1]; final = fr[-1][2]
    second = sorted((len(b) for n, b in final.items() if n != win[0]), reverse=True)[0]
    if win[0] != os.environ.get('WINNER', 'ray'): return None
    TL, TH = float(os.environ.get('TL', '11')), float(os.environ.get('TH', '14.5'))
    if not (TL < tw < TH) or st < 6 or len(set(ld)) < 2 or second < 2 or min(used.values()) < 1 or den < 1: return None
    if not any(e[1] == 'blocked' for e in ev): return None
    return round(tw, 1), win[0], st, len(ld), used, den
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); print('hook', HB, 'P1', P1, 'slot', SLOT0, SLOT1)
FR, EV, WIN, STEALS, LEAD, USED, DEN = sim(SEED)
print('winner', WIN, 'steals', STEALS, 'leaders', LEAD, USED, DEN)
SX = 478
STAMPS = []; _tq = 0.0
for e in EV:
    te, kind, n, extra = e
    if te >= WIN[1]: continue
    if kind == 'power': txt, col = POWER[n] + '!', RING[n]
    elif kind == 'blocked': txt, col = 'BLOCKED!', (140, 255, 130)
    else: continue                       # Cleo's STRONG! stamp covers the shove-away (DENIED! fired at the same instant)
    ts = max(te, _tq); dur = 0.55 if kind == 'blocked' else 0.7
    if ts - te > 0.8: continue          # too stale to show
    STAMPS.append((ts, min(ts + dur, WIN[1]), txt, col)); _tq = ts + dur
print('stamps', [(round(a, 2), c) for a, b, c, _ in STAMPS])
HUB = bg_frames('sun_hd.gif', (W, 570), box=(0, 120, 1920, 120 + 1013), step=2, bright=0.6)
def clampx(x, w, y): return max(70 + w / 2 + 8, min((887 if y > 1110 else 1025) - w / 2 - 8, x))
win = WIN[0]; T_WIN = WIN[1]; VICF = vic(win, 360)
HOLD = 1.4; END = T_WIN + HOLD; NF = int(round(END * FPS))   # rc11: win hold 3.2 -> 1.4s, then the reel loops to frame 0
out = Writer('v93_noaudio.mp4'); out_ev = []
BUSY_OLD = (set([int(e[0] * FPS) + 8 for e in EV if e[1] == 'power'][:6:2] + [int(T_WIN * FPS) + 40]))
BUSY = {0, 20, 45, int(T_WIN * FPS) - 30, int(T_WIN * FPS) + 20, NF - 1}
PILE_POS = [(-34, -18), (30, -24), (-8, 14), (40, 18), (-46, 22), (6, -40), (52, -6), (-60, -4)]
BSLOT = [(-30, -14), (26, -18), (-2, 4)]
SFX = {'yoink': 'boing', 'grab': 'coin_8bit', 'drop': 'twinkle', 'denied': 'sword_hit', 'blocked': 'boing'}
PSFX = {'joy': 'powerup_8bit', 'cyrus': 'whoosh_8bit', 'cleo': 'sword_hit', 'ray': 'chime'}
for f in range(NF):
    t = f / FPS; st, pile, bases, steals, shu = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    if t < shu:                                  # Joy's SHIELD bubble over her basket
        bx, by = BASE['joy']; p_ = 0.5 + 0.5 * math.sin(t * 8)
        layer(img, lambda dd: dd.ellipse([bx - 96, by - 92, bx + 96, by + 60], fill=(110, 230, 110, int(60 + 30 * p_)), outline=(150, 255, 140, 230), width=6))
    for i, k in enumerate(pile):
        g = GUM[k]; px, py = PILE_POS[i]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))
    for n, b in bases.items():
        bx, by = BASE[n]
        for i, k in enumerate(b[:3]):
            g = GUM[k]; px, py = BSLOT[i]; img.alpha_composite(g, (int(bx + px - g.width / 2), int(by + py - g.height / 2 - 14)))
    FX = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(FX)
    for n in NAMES:
        s = st[n]; x, y = s['x'], s['y']
        fd.ellipse([x - 28, y - 8, x + 28, y + 8], fill=(0, 0, 0, 80))
        if t - s['dash'] < 1.3:
            v = math.hypot(s['vx'], s['vy']) or 1; ux, uy = s['vx'] / v, s['vy'] / v
            for k in range(3):
                x0, y0 = x - ux * 34, y - 40 - 30 * k - uy * 20
                fd.line([x0, y0, x0 - ux * (70 + 15 * k), y0 - uy * (70 + 15 * k)], fill=(255, 230, 160, 220), width=5)
            for q in range(6):
                px_ = x - s['vx'] * 0.02 * q * 3; py_ = y - 30 - s['vy'] * 0.02 * q * 3
                fd.rectangle([px_ - 10 + q, py_ - 10 + q, px_ + 10 - q, py_ + 10 - q], fill=(255, 140 + q * 15, 40, 200 - q * 30))
    img.alpha_composite(FX)
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if s['blink'] is not None: continue
        if t < T_START or t >= T_WIN: spr = STAND[n]
        else:
            ph = int(s['dist'] / 24) % 8
            spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        asleep = t - s['sleep'] < 1.0 and T_START <= t < T_WIN
        if asleep: spr = STAND[n]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if asleep:                                   # SLEEP: Zzz over their heads, they stop
            u_ = t - s['sleep']
            text_layer(img, [(x + 22 + 14 * k + 6 * u_, y - FOOT - 2 - 26 * k - 20 * u_, 'Z', 26 + 6 * k, (210, 170, 255), 5, 255) for k in range(3)])
        if s['carry'] is not None:
            g = GUM[s['carry']]; bob = int(5 * math.sin(t * 10 + x * 0.01))
            img.alpha_composite(g, (int(x - g.width / 2), int(y - FOOT + 14 - g.height + bob)))
    PLy = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PLy)
    for e in EV:
        te, kind, n, extra = e; u = t - te
        s = FR[min(int(te * FPS), len(FR) - 1)][0][n]
        if 0 <= u < 1.0 and kind == 'power':
            if n == 'ray':
                r = 40 + 900 * u; a = int(255 * min(1, (1 - u) / 0.35)); d.ellipse([s['x'] - r, s['y'] - 60 - r * 0.7, s['x'] + r, s['y'] - 60 + r * 0.7], outline=(200, 140, 255, int(a * 0.8)), width=10)
            if n == 'cleo':
                bx, by = BASE['cleo']; r = 60 + 160 * u; a = int(255 * min(1, (1 - u) / 0.35))
                d.ellipse([bx - r, by - r * 0.6, bx + r, by + r * 0.6], outline=(140, 190, 255, a), width=8)
        if abs(t - te) < 0.5 / FPS:
            out_ev.append((round(te, 3), PSFX[n] if kind == 'power' else SFX[kind]))
    if t < T_WIN:
        # rc11: ONE big stamp slot (power / BLOCKED!) on a dark plate under the roster panel, queued so two never overlap
        for (ts, te2, txt, col) in STAMPS:
            if ts <= t < te2:
                u = t - ts; k = 1.2 - 0.2 * min(1, u / 0.12); fs = int(58 * k)
                w_ = d.textlength(txt, font=F(fs)); pw = max(w_ + 56, 400); my = (SLOT0 + SLOT1) / 2
                d.rounded_rectangle([SX - pw / 2, SLOT0, SX + pw / 2, SLOT1], 16, fill=(14, 10, 24, 240), outline=col + (255,), width=6)
                ctext(d, SX, my - fs / 2, txt, F(fs), col, 8, 255)
        # small character pop (YOINK! / +1): only the newest one, 46px
        sm = [e for e in EV if e[1] in ('yoink', 'drop') and 0 <= t - e[0] < 0.8]
        if sm:
            te, kind, n, extra = sm[-1]; u = t - te; s = FR[min(int(te * FPS), len(FR) - 1)][0][n]
            x, y = s['x'], max(s['y'] - FOOT - 10 - u * 50, SLOT1 + 60); a = int(255 * min(1, (0.8 - u) / 0.3))
            if kind == 'yoink': ctext(d, clampx(x, 6 * 46, y), y - 30, 'YOINK!', F(46), (255, 220, 60), 7, a)
            else: ctext(d, clampx(x, 2 * 48, y), y - 20, '+1', F(48), RING[n], 7, a)
    img.alpha_composite(PLy)
    # Liza's sun temple above the arena, roster + powers panel under the hook
    img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
    layer(img, lambda dd: dd.rounded_rectangle([78, P0, 1017, P1], 18, fill=(20, 12, 8, 225), outline=(255, 214, 60, 255), width=4))
    d = ImageDraw.Draw(img)
    active = {e[2]: e[0] for e in EV if e[1] == 'power' and 0 <= t - e[0] < 0.9}
    for i, n in enumerate(NAMES):
        sx = 78 + 939 * (i + 0.5) / 4; ic = ICON[n]
        img.alpha_composite(ic, (int(sx - 68 - ic.width / 2), P0 + 12))
        for k in range(3):
            gx = sx + 2 + k * 42; gy = P0 + 48
            if k < len(bases[n]):
                g = GUMS[bases[n][k]]; g = g.resize((int(g.width * 1.3), int(g.height * 1.3)), Image.NEAREST)
                img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
            else: d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], outline=(140, 120, 100), width=3)
        on = n in active
        d.rounded_rectangle([sx - 114, P0 + 92, sx + 114, P0 + 138], 10, fill=RING[n] if on else (40, 28, 22), outline=RING[n], width=3)
        gi = GUMS[PGUM[n]]; img.alpha_composite(gi, (int(sx - 106), int(P0 + 115 - gi.height / 2)))
        d = ImageDraw.Draw(img)
        tw_ = d.textlength(POWER[n], font=F(28)); d.text((sx + 16 - tw_ / 2, P0 + 101), POWER[n], font=F(28), fill=(20, 15, 35) if on else (235, 225, 210))
        if t >= T_WIN and n == win: d.ellipse([sx - 110, P0 + 6, sx - 26, P0 + 90], outline=(255, 214, 60), width=6)
    if t < 1.9:                                   # rc11: over the action from frame 0, fades 1.5-1.9s
        a_ = int(255 * min(1, (1.9 - t) / 0.4))
        layer(img, lambda dd: dd.rounded_rectangle([520 - 412, CY - 186, 520 + 412, CY - 82], 18, fill=(14, 10, 24, int(a_ * 0.9)), outline=(255, 214, 60, a_), width=6))
        text_layer(img, [(520, CY - 162, 'PICK A PLAYER!', 56, (255, 255, 255), 8, a_)])
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(8, 6, 14, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1180 - vf.height))
        layer(img, lambda dd: dd.rounded_rectangle([CX - 330, 1196, CX + 330, 1420], 22, fill=(14, 10, 24, 245), outline=(255, 214, 60, 255), width=8))
        k_ = 1.2 - 0.2 * min(1, u / 0.15)
        text_layer(img, [(CX, 1222, LABEL[win], int(76 * k_), (255, 214, 60), 9, 255), (CX, 1322, 'WINS!', int(76 * k_), (255, 255, 255), 9, 255)])
        rr = random.Random(f); L3 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d3 = ImageDraw.Draw(L3)
        for _ in range(40):
            cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
            d3.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]))
        img.alpha_composite(L3)
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    img.alpha_composite(HOOK)
    out.write(img)
    if f in BUSY or f in [int(st_[0] * FPS) + 3 for st_ in STAMPS[:4]]: img.convert('RGB').save(f'f93_{f}.png')
out.close(); json.dump(out_ev, open('v93_ev.json', 'w')); print('done', round(END, 2))
if os.environ.get('NOMIX'): sys.exit()
mix('v93_noaudio.mp4', out_ev, 'arcade_loop2.wav', 3, 'v93_mix.mp4')
print('LUFS', loudness('v93_mix.mp4'), '->', louder('v93_mix.mp4', 'v93_final.mp4'))
