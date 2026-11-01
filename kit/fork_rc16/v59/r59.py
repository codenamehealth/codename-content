import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
from PIL import Image, ImageDraw, ImageEnhance
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_rc16/v59/'
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import acv_gloss
def hook59():
    # rc16: same band style as hook.py; PICK A GUIDE (80px gold), the post's 'BEFORE THE WATER RISES' (36 -> 40px, the most
    # that fits one line), and the comment prompt COMMENT YOUR PICK as a real 48px line from frame 0
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); y = 262 + 26
    h = 26 + 74 + 22 + 40 + 16 + 18 + 48 + 26
    d.rounded_rectangle([70, 262, 1025, 262 + h], 22, fill=(14, 10, 24, 228), outline=(255, 214, 60), width=6)
    for txt, sz, col, sw, gap in (('PICK A GUIDE', 74, (255, 214, 60), 9, 22), ('BEFORE THE WATER RISES', 40, (120, 220, 255), 6, 16)):
        w_ = d.textlength(txt, font=F(sz)); d.text((540 - w_ / 2, y), txt, font=F(sz), fill=col, stroke_width=sw, stroke_fill=(10, 6, 18)); y += sz + gap
    d.line([(130, y), (965, y)], fill=(255, 214, 60, 120), width=3); y += 18
    txt = 'COMMENT YOUR PICK'; w_ = d.textlength(txt, font=F(48)); d.text((540 - w_ / 2, y), txt, font=F(48), fill=(240, 240, 240), stroke_width=7, stroke_fill=(10, 6, 18))
    return L, 262 + h
HOOK, HB = hook59()
P0, P1 = HB + 12, HB + 152
def X(x): return 110 + (x - 60) * 0.75
CX = X(540)
NAMES = ['joy', 'cleo', 'cyrus', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
ROWH = 250; NROW = int(os.environ.get('NROW', '15')); Y_BOT = 1000 + NROW * ROWH; WH = Y_BOT + 400   # rc16: more headroom above the top ledge (taller header)
T_GO = 0.3
# platform layout: (row, x0, x1); row 0 = floor
rl = random.Random(3)
PLAT = [(0, X(60), X(1020))]
for r in range(1, NROW):
    if r % 2:
        a = rl.uniform(70, 160); w1 = rl.uniform(300, 380); PLAT.append((r, X(a), X(a + w1))); b = rl.uniform(600, 690); w2 = rl.uniform(300, 380); PLAT.append((r, X(b), X(min(1010, b + w2))))
    else:
        a = rl.uniform(330, 400); w1 = rl.uniform(330, 380); PLAT.append((r, X(a), X(a + w1)))
PLAT.append((NROW, X(380), X(700)))
def py(r): return Y_BOT - r * ROWH
SLIMEPAD = {}      # row -> platform index (filled below)
for i, (r, x0, x1) in enumerate(PLAT):
    if r in tuple(int(v) for v in os.environ.get('PADS', '4,9').split(',')) and SLIMEPAD.get(r) is None: SLIMEPAD[r] = i
SLIMEPAD = {r: i for r, i in SLIMEPAD.items() if i is not None}

# ---------------- gummies (content pass): one per chosen platform on the climbing line, every one picked up and used
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRONG!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, STRONG_T, SLEEP_T, STUN_T = 2.5, 3.0, 1.0, 0.6
GROWS = [int(r) for r in os.environ.get('GROWS', '2,5,7,10,12').split(',')]
WDELAY = float(os.environ.get('WDELAY', '1.0'))
LEADOK = int(os.environ.get('LEADOK', '1'))
SHOVE_R = float(os.environ.get('SHOVE_R', '150'))
def make_gums(gseed):
    rg = random.Random(gseed)
    kinds = ['mush', 'cre', 'mel', 'acv'] + ([rg.choice(['mush', 'cre'])] if len(GROWS) > 4 else [])
    while True:
        rg.shuffle(kinds)
        if all(kinds[i] != kinds[i + 1] for i in range(len(kinds) - 1)) and kinds.index('acv') <= 2 and 1 <= kinds.index('mel') <= 3: break
    out = []
    for r, kd in zip(GROWS, kinds):
        cand = [i for i, P in enumerate(PLAT) if P[0] == r and SLIMEPAD.get(r) != i]
        i = rg.choice(cand); x0, x1 = PLAT[i][1], PLAT[i][2]
        out.append((i, rg.uniform(x0 + 60, x1 - 60), kd))
    return out
GSEED = int(os.environ.get('GSEED', '1'))
GUMS = make_gums(GSEED)
def water(t):
    if t < T_GO + WDELAY: return Y_BOT + 120
    u = t - T_GO - WDELAY
    return Y_BOT + 120 - (WA * u + WB * u * u)

WA, WB = float(os.environ.get('WA', '150')), float(os.environ.get('WB', '4'))
def sim(seed, dur=40):
    rnd = random.Random(seed)
    R = {}
    xs = [X(200), X(420), X(640), X(860)]; rnd.shuffle(xs)
    for n, x in zip(NAMES, xs):
        R[n] = dict(p=0, x=x, y=py(0), mode='run', tgt=None, j0=None, sp=rnd.uniform(165, 300), jt=rnd.uniform(0.5, 0.8), ph=rnd.uniform(0, 6),
                    boost=-9, strong=-9, sleep=-9, stun=-9, shield=False, caught=None, done=None, vx=1, hes=0.0, hitcd=-9)
    taken = set(); frames = []; events = []; leaders = []; lead_now = [None]
    def powered(s, t): return t - s['boost'] < SPEED_T or t - s['strong'] < STRONG_T or s['shield']
    def pick(n, s, t):
        for g in GUMS:
            if g[0] == s['p'] and g not in taken and abs(g[1] - s['x']) < 45 and not powered(s, t):
                taken.add(g); kd = g[2]; events.append((t, 'pick', n, kd))
                if kd == 'mush': s['boost'] = t
                elif kd == 'cre': s['strong'] = t
                elif kd == 'acv': s['shield'] = True
                else:
                    vic = []
                    for m, o in R.items():
                        if m == n or o['caught'] is not None or o['done'] is not None: continue
                        if o['shield']: o['shield'] = False; events.append((t, 'block', m, n))
                        else: o['sleep'] = t + SLEEP_T; vic.append(m)
                    events.append((t, 'sleepwave', n, vic))
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS; wl = water(t)
        for n, s in R.items():
            if s['caught'] is not None:
                s['y'] = wl + 30; continue
            if s['done'] is not None or t < T_GO: continue
            if s['mode'] == 'run':
                r = PLAT[s['p']][0]
                if r >= NROW:
                    s['done'] = t; events.append((t, 'win', n)); continue
                if t < s['sleep'] or t < s['stun']:
                    pass
                else:
                    if s['tgt'] is None:
                        cand = [i for i, P in enumerate(PLAT) if P[0] == r + 1]
                        cur = PLAT[s['p']]
                        gum_here = {g[0]: g for g in GUMS if g not in taken}
                        def cost(i):
                            P = PLAT[i]; cx = min(max(s['x'], P[1] + 40), P[2] - 40)
                            c = abs(cx - s['x']) + rnd.uniform(0, 260)
                            if i in gum_here and not powered(s, t) and (n != lead_now[0] or LEADOK): c -= 600
                            if t - s['strong'] < STRONG_T and any(o['p'] == i and o['caught'] is None and o['done'] is None for m, o in R.items() if m != n): c -= 700
                            return c
                        nxt = min(cand, key=cost); P = PLAT[nxt]
                        if nxt in gum_here and not powered(s, t) and (n != lead_now[0] or LEADOK): lx = gum_here[nxt][1]
                        else: lx = min(max(s['x'], P[1] + 50), P[2] - 50)
                        takeoff = min(max(lx, cur[1] + 30), cur[2] - 30)
                        s['tgt'] = (nxt, takeoff, lx); s['hes'] = rnd.uniform(0.1, 0.6) if rnd.random() < 0.45 else 0
                    nxt, takeoff, lx = s['tgt']
                    sp = s['sp'] * (1 + 0.15 * math.sin(t * 1.3 + s['ph'])) * (1.6 if t - s['boost'] < SPEED_T else 1)
                    if abs(takeoff - s['x']) > 6:
                        d = 1 if takeoff > s['x'] else -1; s['vx'] = d; s['x'] += d * min(sp * dt, abs(takeoff - s['x']))
                        pick(n, s, t)
                    else:
                        if s['hes'] > 0: s['hes'] -= dt
                        else:
                            s['mode'] = 'jump'; s['j0'] = (t, s['x'], s['y'], lx, py(PLAT[nxt][0]), nxt, s['jt'] * (0.8 if t - s['boost'] < SPEED_T else 1)); events.append((t, 'jump', n))
                            s['vx'] = 1 if lx >= s['x'] else -1
                # STRONG: shove anyone standing near on the same platform down a level
                if t - s['strong'] < STRONG_T and t - s['hitcd'] > 0.8:
                    for m, o in R.items():
                        if m == n or o['caught'] is not None or o['done'] is not None or t < o['stun']: continue
                        if math.hypot(o['x'] - s['x'], (o['y'] - s['y']) * 0.8) < SHOVE_R:
                            s['hitcd'] = t
                            if o['shield']: o['shield'] = False; events.append((t, 'block', m, n)); break
                            r0 = PLAT[o['p']][0]
                            if r0 >= 1:
                                below = [i for i, P in enumerate(PLAT) if P[0] == r0 - 1]
                                bi = min(below, key=lambda i: abs(min(max(o['x'], PLAT[i][1] + 40), PLAT[i][2] - 40) - o['x']))
                                Pb = PLAT[bi]; lxb = min(max(o['x'] + (90 if o['x'] >= s['x'] else -90), Pb[1] + 40), Pb[2] - 40)
                                o['mode'] = 'jump'; o['j0'] = (t, o['x'], o['y'], lxb, py(r0 - 1), bi, 0.55); o['tgt'] = None
                                o['vx'] = 1 if lxb >= o['x'] else -1
                            o['stun'] = t + STUN_T + 0.55; events.append((t, 'shove', m, n)); break
            elif s['mode'] == 'jump':
                t0, x0, y0, x1, y1, nxt, D = s['j0']
                u = min(1, (t - t0) / D)
                hgt = 170 if y1 <= y0 else 60
                s['x'] = x0 + (x1 - x0) * u; s['y'] = y0 + (y1 - y0) * u - hgt * 4 * u * (1 - u)
                if u >= 1:
                    s['p'] = nxt; s['y'] = y1; s['tgt'] = None; s['mode'] = 'run'
                    pick(n, s, t)
                    if PLAT[nxt][0] in SLIMEPAD and SLIMEPAD[PLAT[nxt][0]] == nxt and y1 <= y0:
                        r2 = PLAT[nxt][0] + 2; cand = [i for i, P in enumerate(PLAT) if P[0] == r2]
                        tgt = min(cand, key=lambda i: abs((PLAT[i][1] + PLAT[i][2]) / 2 - s['x']))
                        P = PLAT[tgt]; lx2 = min(max(s['x'], P[1] + 50), P[2] - 50)
                        s['mode'] = 'jump'; s['j0'] = (t, s['x'], s['y'], lx2, py(P[0]), tgt, s['jt']); events.append((t, 'boing', n))
            if s['y'] > wl - 10 and s['done'] is None:
                s['caught'] = t; s['shield'] = False; events.append((t, 'caught', n))
        live = [n for n in NAMES if R[n]['caught'] is None]
        if live:
            ld = min(live, key=lambda n: (R[n]['done'] if R[n]['done'] is not None else 1e5 + R[n]['y']))
            if not leaders or leaders[-1] != ld: leaders.append(ld)
            lead_now[0] = ld
        frames.append(({n: dict(x=s['x'], y=s['y'], mode=s['mode'], vx=s['vx'], caught=s['caught'], done=s['done'], boost=s['boost'], strong=s['strong'], sleep=s['sleep'], stun=s['stun'], shield=s['shield'], j0=s['j0']) for n, s in R.items()}, wl, set(taken)))
        if all(R[n]['caught'] is not None or R[n]['done'] is not None for n in NAMES) and any(R[n]['done'] for n in NAMES): break
    return frames, events, leaders, {n: (R[n]['done'], R[n]['caught']) for n in NAMES}
STAMPEV = ('pick', 'shove', 'block', 'caught')
def score(seed):
    # rc16 review targets: Cleo wins ~12-14.5s, first OUT by ~6-7s, outs spread ~2-4s apart, last out <=1.3s before the win,
    # every gummy picked up, Cleo never holds both SHIELD and STRONG (STRONG goes to someone else), few stamp collisions
    fr, ev, ld, res = sim(seed, 22)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: return None
    w = wins[0]
    if w != os.environ.get('WANT', 'cleo'): return None
    tw = res[w][0]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(caught) != 3 or not (11.5 < tw < 14.8): return None
    if not (4.0 < caught[0] < 7.5) or min(caught[1] - caught[0], caught[2] - caught[1]) < 1.4 or max(caught[1] - caught[0], caught[2] - caught[1]) > 5.0: return None
    if not (0.25 < tw - caught[-1] < 1.4) or len(ld) < 3: return None
    picks = [e for e in ev if e[1] == 'pick']
    if len(picks) < len(GUMS) or len(set(e[3] for e in picks)) < 3: return None
    cp = [e[3] for e in picks if e[2] == 'cleo']
    if 'cre' in cp or len(cp) > 1: return None
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sw or max(len(e[3]) + sum(1 for b in ev if b[1] == 'block' and abs(b[0] - e[0]) < 0.01) for e in sw) < 2: return None
    nsh = sum(e[1] == 'shove' for e in ev)
    if nsh < 1: return None
    st = sorted(e[0] for e in ev if e[1] in STAMPEV and e[0] <= tw)
    clash = sum(1 for i in range(len(st) - 1) if st[i + 1] - st[i] < 0.7)
    return clash, round(tw, 2), [round(c, 1) for c in caught], len(ld), nsh, sum(e[1] == 'block' for e in ev), [(round(e[0], 1), e[2], e[3]) for e in picks]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EVS, LEAD, RES = sim(SEED)
WIN = [n for n in NAMES if RES[n][0] is not None][0]; T_WIN = RES[WIN][0]
print('win', WIN, round(T_WIN, 2), {n: RES[n] for n in NAMES}, 'leaders', LEAD)
for e in EVS:
    if e[1] != 'jump': print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
# ---------------- art
bg = Image.open('templebg/00.png').convert('RGBA'); k = W / bg.width
bgt = ImageEnhance.Brightness(bg.resize((W, int(bg.height * k)), Image.NEAREST)).enhance(0.62)
WORLD = Image.new('RGBA', (W, WH), (0, 0, 0, 255))
y = WH - bgt.height; flip = False
while y > -bgt.height:
    WORLD.alpha_composite(bgt.transpose(Image.FLIP_TOP_BOTTOM) if flip else bgt, (0, y)); y -= bgt.height; flip = not flip
LEDGE = crop(Image.open('ledge/03.png').convert('RGBA'))
for i, (r, x0, x1) in enumerate(PLAT):
    w_ = int(x1 - x0); lg = LEDGE.resize((w_, int(LEDGE.height * 3)), Image.NEAREST)
    WORLD.alpha_composite(lg, (int(x0), int(py(r) - 14)))
wd = ImageDraw.Draw(WORLD)
ex = (X(380) + X(700)) / 2; ey = py(NROW)
# rc16: the cream 'exit' disc + square (read as a glitch sliding behind the header) is gone; the top ledge glows gold instead
GL = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); gd = ImageDraw.Draw(GL)
for k_ in range(5): gd.rounded_rectangle([X(380) - 40 + k_ * 10, 40 + k_ * 18, X(700) + 40 - k_ * 10, 196], 30, fill=(255, 214, 90, 22 + k_ * 12))
WORLD.alpha_composite(GL, (0, int(ey - 186)))
lg = LEDGE.resize((int(X(700) - X(380)), int(LEDGE.height * 3)), Image.NEAREST); WORLD.alpha_composite(lg, (int(X(380)), int(ey - 14)))
SLIME = seq(PL + 'race/slime_idle_c', 3); SPLAT = seq(PL + 'race/slime_splat_c', 3)
SK = 3
SR = {g: seq(PL + f'race/{g}_run', SK) for g in NAMES}
SWIM = {g: seq(SP + f'fork4/{g}_swim' + ('3' if g == 'cleo' else ''), SK)[3:8] for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SK, 0, 1)[0] for g in NAMES}
GUM = {k: gummy(k, 3) for k in GUMK}
GUM['acv'] = up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), 3)   # rc16: gummy gloss on Syeda's ACV gummy
ACV_SEEN = [None]
VICF = vic(WIN, 380)
FRONT = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
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
ICON = {n: face(n, 46) for n in NAMES}   # rc16: roster faces 72 -> 96px
# ---------------- render (content pass)
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SK) for g in NAMES}
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(T_GO, 'whoosh_8bit')
PSFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
lastj = -1
for e in EVS:
    t, kd = e[0], e[1]
    if kd == 'jump' and t - lastj > 0.25: ev(t, 'jump'); lastj = t
    elif kd == 'boing': ev(t, 'boing')
    elif kd == 'pick': ev(t, PSFX[e[3]])
    elif kd == 'shove': ev(t, 'punch')
    elif kd == 'block': ev(t, 'boing')
    elif kd == 'caught': ev(t, 'poof'); ev(t + 0.05, 'buzz_8bit')
    elif kd == 'win': ev(t, 'victory'); ev(t + 0.1, 'cheer')
T_CARD = T_WIN + 0.6; T_LOOP = T_CARD + 1.3; T_ALL = T_LOOP + 0.2; NF = int(round(T_ALL * FPS))   # rc16: card hold 2.6 -> 1.3s
POPS = []
for e in EVS:
    if e[0] > T_WIN: continue
    if e[1] == 'pick': POPS.append((e[0], e[2], POWER[e[3]][0], POWER[e[3]][1], 50))
    elif e[1] == 'shove': POPS.append((e[0], e[2], 'BONK!', (255, 255, 255), 50))
    elif e[1] == 'block': POPS.append((e[0], e[2], 'BLOCKED!', (110, 230, 90), 46))
CAUGHT = [e for e in EVS if e[1] == 'caught']
SLEEPW = [e for e in EVS if e[1] == 'sleepwave']
GCOL = {k: v[1] for k, v in POWER.items()}
# rc16: one stamp at a time. OUT stamps (prio 2) and WINNER! (prio 3) cut a running pop short; pops queue (dropped if >0.6s late)
_raw = [(e[0], 2, 1.0, ('out', e[2], LABEL[e[2]] + ' OUT!', (255, 95, 95))) for e in CAUGHT if e[0] <= T_WIN]
_raw += [(T_WIN, 3, T_CARD - T_WIN, ('win', WIN, 'WINNER!', (255, 214, 60)))]
_CT = {e[2]: e[0] for e in CAUGHT}
_raw += [(t0, 1, 0.65, ('pop', n, text, col)) for t0, n, text, col, size in POPS if not (text == 'BONK!' and 0 <= _CT.get(n, 99) - t0 < 0.8)]   # a BONK that ends in an OUT shows as the OUT stamp
SCHED = []
for t0, pr, du, it in sorted(_raw, key=lambda r: (r[0], -r[1])):
    if SCHED and SCHED[-1][1] > t0:
        ps, pe, ppr, pit = SCHED[-1]
        if pr > ppr:
            if t0 - ps < 0.3: SCHED.pop()
            else: SCHED[-1] = (ps, t0, ppr, pit)
            st0 = t0
        else: st0 = pe
    else: st0 = t0
    if pr == 1 and st0 - t0 > 0.7: print('dropped pop', round(t0, 2), it); continue
    SCHED.append((st0, st0 + du, pr, it))
print('stamps', [(round(a, 2), round(b, 2), it[2]) for a, b, pr, it in SCHED])
def acv_side(img, gx, gy, a):
    L2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2); tag = 'ACV GUMMY'; f = F(44); tw = d2.textlength(tag, font=f)
    x0 = gx + 62; y0 = gy - 36
    if x0 + tw + 36 > (1015 if gy < 1110 else 875): x0 = gx - 62 - tw - 36
    d2.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, int(235 * a / 255)), outline=(90, 200, 80, a), width=5)
    if x0 > gx: d2.polygon([(x0 + 2, gy - 14), (x0 + 2, gy + 14), (gx + 40, gy)], fill=(90, 200, 80, a))
    else: d2.polygon([(x0 + tw + 34, gy - 14), (x0 + tw + 34, gy + 14), (gx - 40, gy)], fill=(90, 200, 80, a))
    d2.text((x0 + 18, y0 + 14), tag, font=f, fill=(255, 255, 255, a), stroke_width=5, stroke_fill=(10, 6, 18, a))
    img.alpha_composite(L2)
cam = 0
wr = Writer(OUT + 'v59_noaudio.mp4'); KEYF = set(int(v) for v in os.environ.get('KEYF', '0').split(','))
for f in range(NF):
    t = f / FPS; loopcut = t >= T_LOOP
    if loopcut: t = 0.0
    ACV_TAG = []
    fi = int(round(t * FPS)); st, wl, taken = FR[min(fi, len(FR) - 1)]
    live = [n for n in NAMES if st[n]['caught'] is None]
    focus = min(st[n]['y'] for n in live) if live else st[WIN]['y']
    if t < T_GO: focus = py(0)
    low = max(st[n]['y'] for n in live) if live else focus
    recent = any(0 <= t - e[0] < 1.3 for e in CAUGHT)
    danger = (wl - low < 330) or recent
    hi_c = focus - 1000   # rc16: leader lower on screen so jumps stay clear of the taller header + roster
    lo_c = (max(wl - 30, low) if danger else low) - 1450
    tgt = lo_c if lo_c > hi_c and danger else min(hi_c, max(lo_c, focus - 1300))
    if t < T_GO: tgt = py(0) - 1300
    if not danger: tgt = min(tgt, focus - P1 - 170)   # rc16: away from catches, the leader stays clear of the roster/header
    if t >= T_WIN - 0.4: tgt = min(tgt, focus - P1 - 300)   # and the winner is framed for the win
    tgt = max(0, min(WH - H, tgt))
    cam = tgt if (f == 0 or loopcut) else cam + (tgt - cam) * (0.18 if t >= T_WIN - 0.4 else 0.1)
    c0 = int(cam)
    img = WORLD.crop((0, c0, W, c0 + H)).copy()
    for r, i in SLIMEPAD.items():
        rr, x0, x1 = PLAT[i]; sx = (x0 + x1) / 2; sy = py(rr) - c0
        hit = any(0 <= t - e[0] < 0.3 and e[1] == 'boing' and abs(st[e[2]]['x'] - sx) < 400 for e in EVS)
        fr = SPLAT[3] if hit else SLIME[int(t * 10) % len(SLIME)]
        img.alpha_composite(fr, (int(sx - fr.width / 2), int(sy - fr.height + 30)))
    # gummies (each one on a platform the guides climb through)
    for g in GUMS:
        if g in taken: continue
        i, gx, kd = g; gy = py(PLAT[i][0]) - c0 - 60 + 8 * math.sin(t * 3 + gx); col = GCOL[kd]
        layer(img, lambda dd, gx=gx, gy=gy, col=col: [dd.ellipse([gx - 48 + k_ * 9, gy - 44 + k_ * 9, gx + 48 - k_ * 9, gy + 44 - k_ * 9], fill=col + (40 + k_ * 30,)) for k_ in range(3)])
        gm = GUM[kd]; img.alpha_composite(gm, (int(gx - gm.width / 2), int(gy - gm.height / 2)))
        if kd == 'acv' and P1 + 60 < gy < 1440:
            if ACV_SEEN[0] is None: ACV_SEEN[0] = t
            if t - ACV_SEEN[0] < 1.8: ACV_TAG.append((gx, gy, int(255 * min(1, (1.8 - (t - ACV_SEEN[0])) / 0.3))))
    for e in EVS:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'], s0['y'] - c0 - 90; col = GCOL[e[3]]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'], s0['y'] - c0 - 110
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1400 * u, 20 + 1000 * u)])
    # guides
    for n in sorted(NAMES, key=lambda n: (st[n]['shield'] or t - st[n]['strong'] < STRONG_T or t - st[n]['boost'] < SPEED_T)):   # powered guide drawn on top
        s = st[n]; x, yy = s['x'], s['y'] - c0
        if s['caught'] is not None:
            fr = SWIM[n][int(t * 8) % len(SWIM[n])]
            if int(t * 1.5 + NAMES.index(n)) % 2: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (int(x - fr.width / 2), int(yy - 78 * SK + 70 + 4 * math.sin(t * 4))))
            continue
        asleep = t < s['sleep']; stunned = t < s['stun'] and not asleep
        boosted = t - s['boost'] < SPEED_T; strong = t - s['strong'] < STRONG_T
        if t < T_GO or (s['done'] is not None and t > s['done']) or asleep: fr = STAND[n]
        elif stunned: fr = PANIC[n][int(t * 12) % len(PANIC[n])]
        elif s['mode'] == 'jump': fr = SR[n][3]
        else: fr = SR[n][int(t * (20 if boosted else 14)) % 8]
        if s['vx'] < 0 and fr is not STAND[n]: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        x0, y0 = int(x - fr.width / 2), int(yy - 78 * SK + 6)
        if boosted and not asleep and not stunned:
            for q in range(3):
                img.alpha_composite(tinted(fr, (255, 170, 50), int(255 * (0.34 - 0.09 * q))), (x0 - int(s['vx'] * (q + 1) * 26), y0 + (q + 1) * 6))
            sgn = -1 if s['vx'] >= 0 else 1
            layer(img, lambda dd: [dd.rectangle([min(x + sgn * (50 + 26 * q), x + sgn * (130 + 26 * q + (q * 37 + int(t * 60)) % 40)), yy - 150 + q * 30 - 4, max(x + sgn * (50 + 26 * q), x + sgn * (130 + 26 * q + (q * 37 + int(t * 60)) % 40)), yy - 150 + q * 30 + 4], fill=(255, 240, 200, 210)) for q in range(4)] +
                                  [dd.ellipse([x + sgn * (40 + q * 30) - 18, yy - 18 - q * 5, x + sgn * (40 + q * 30) + 18, yy + 6], fill=(210, 190, 150, 170 - q * 45)) for q in range(3)])
        if strong and not asleep:
            tt = tinted(fr, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
            for ox, oy in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
        img.alpha_composite(fr, (x0, y0))
        if asleep:
            img.alpha_composite(tinted(fr, (40, 20, 90), 120), (x0, y0))
            u = t - (s['sleep'] - SLEEP_T)
            text_layer(img, [(x + 50 + 22 * kz, yy - 200 - ((u * 1.4 + kz * 0.33) % 1) * 70 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if stunned:
            layer(img, lambda dd: [dd.polygon([(x + 50 * math.cos(t * 9 + q * 2.09) + dx_ * 1.4, yy - 200 + 14 * math.sin(t * 9 + q * 2.09) + dy_ * 1.4) for dx_, dy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])
        if s['shield']:
            layer(img, lambda dd: (dd.ellipse([x - 100, yy - 250, x + 100, yy + 20], fill=(110, 230, 90, 55), outline=(150, 255, 120, 230), width=7),
                                   dd.arc([x - 74, yy - 226, x - 14, yy - 150], 200, 260, fill=(230, 255, 220, 230), width=6)))
    for e in EVS:
        if e[1] == 'shove' and 0 <= t - e[0] < 0.35:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.35
            cx_, cy_ = s0['x'], s0['y'] - c0 - 110
            layer(img, lambda dd, cx_=cx_, cy_=cy_, u=u: [dd.polygon([(cx_ + math.cos(q * 0.785) * 40, cy_ + math.sin(q * 0.785) * 40), (cx_ + math.cos(q * 0.785 + 0.2) * (80 + 80 * u), cy_ + math.sin(q * 0.785 + 0.2) * (80 + 80 * u)), (cx_ + math.cos(q * 0.785 + 0.39) * 40, cy_ + math.sin(q * 0.785 + 0.39) * 40)], fill=(255, 255, 255, int(240 * (1 - u)))) for q in range(8)])
    # water
    wy = wl - c0
    if wy < H:
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        pts = [(x, wy + 10 * math.sin(x / 70 + t * 3)) for x in range(0, W + 20, 20)]
        dl.polygon(pts + [(W, H), (0, H)], fill=(40, 140, 200, 150))
        for x, yv in pts: dl.rectangle([x - 10, yv - 4, x + 10, yv + 4], fill=(200, 240, 255, 220))
        for k_ in range(26):
            bx = (k_ * 97 + t * 30) % W; by = wy + 40 + ((k_ * 131 - t * 120) % max(1, H - wy))
            if by < H: dl.rectangle([bx - 4, by - 4, bx + 4, by + 4], fill=(210, 245, 255, 140))
        img.alpha_composite(L)
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW):
        img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    # stamps: one at a time (rc16)
    items = []
    for st0, en, pr, it in SCHED:
        if not (st0 <= t < en) or t >= T_CARD: continue
        kind, n, text, col = it; u = t - st0; s = st[n]; al = int(255 * min(1, (en - t) / 0.25))
        if kind == 'pop':
            if s['caught'] is not None and t >= s['caught']: continue
            size = 56; sc = 1 + 0.3 * max(0, 1 - u / 0.15); wv = len(text) * size * sc + 20
            sy = max(s['y'] - c0 - 300 - u * 24, P1 + 16)
            sx = min(max(s['x'], 70 + wv / 2), (1015 if sy + size < 1110 else 877) - wv / 2)
            items.append((sx, sy, text, int(size * sc), col, 8, al))
        else:
            sy = min(max((wl - c0 - 230) if kind == 'out' else (s['y'] - c0 - 330), P1 + 40), 1330)
            base = min(80 if kind == 'win' else 72, int((935 if sy + 72 < 1110 else 800) / (len(text) * 1.2))); sc = 1 + 0.2 * max(0, 1 - u / 0.15); wv = len(text) * base * sc
            sx = min(max(478, 70 + wv / 2 + 4), (1015 if sy + base < 1110 else 877) - wv / 2 - 4)
            items.append((sx, sy, text, int(base * sc), col, 10, al))
    if items: text_layer(img, items)
    for gx_, gy_, a_ in ACV_TAG: acv_side(img, gx_, gy_, a_)
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(10, 24, 30, 220)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]
        if st[n]['caught'] is not None: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 4))
        if st[n]['caught'] is not None: text_layer(img, [(x, P0 + 104, 'OUT', 40, (255, 110, 110), 6, 255)])
        elif st[n]['done'] is not None: text_layer(img, [(x, P0 + 104, 'SAFE!', 40, (255, 214, 60), 6, 255)])
    if t < 0.8:
        sc = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(478, 1000, 'CLIMB!', int(100 * sc), (120, 220, 255), 12, int(255 * min(1, (0.8 - t) / 0.3)))])
    if t >= T_CARD:
        u = t - T_CARD; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(8, 14, 22, int(170 * a))))
        if a > 0.2:
            vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, P1 + 200 + 380 - vf.height))
            text_layer(img, [(W / 2, P1 + 30, LABEL[WIN] + ' WINS!', 64, (255, 214, 60), 8, int(255 * a)),
                             (W / 2, P1 + 120, 'DID YOUR GUIDE WIN?', 48, (255, 255, 255), 8, int(255 * a))])   # rc16: 30 -> 48px, one line
            rr = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr.uniform(80, 1000), (rr.uniform(0, H) + u * 400) % (1480 - P1) + P1
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p59_{f:04d}.png')
    if f in KEYF: img.convert('RGB').save(OUT + f'k_{f:04d}.png')
    if os.environ.get('FULL') and not loopcut and any(abs(t - (e[0] + 0.2)) < 0.5 / FPS for e in EVS if e[1] in ('pick', 'shove', 'caught', 'win')):
        img.convert('RGB').save(OUT + f'k_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v59_ev.json', 'w'))
print('done', round(T_ALL, 2), len(EV))
