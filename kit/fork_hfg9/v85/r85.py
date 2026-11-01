import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
A9 = SP + 'fork_a9/'
# #85 safe-zone + hook pass (source: fork_a9/arena/render_arena.py). HOLLOW RULE: the Hollow team is removed (4 guides).
# Arena scaled to fit the zone: pylon ring 330x430 -> 320x330 around (478,1110), island scaled to match; runners unchanged 2x.
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
COL = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (235, 190, 60)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
CX, CY = 478, 1132; KX, KY = 320 / 330, 300 / 430   # rc9: ring 320x300 around (478,1132) so 3x guides stay under the scoreboard and above y1500
SPK = float(os.environ.get('SPK', '0.88')); GSCHED = [2.6, 5.6, 8.6, 11.6]
PY = [(CX, CY)] + [(CX + 320 * math.cos(-math.pi / 2 + k * math.pi / 4), CY + 300 * math.sin(-math.pi / 2 + k * math.pi / 4)) for k in range(8)]
NP = len(PY); CAP = 1.3; DUR = float(os.environ.get('DUR', '15')); T0 = 0.0   # rc9: match 30s -> 15s, running from frame 0
def inside(x, y):
    a = math.atan2((y - CY) / 1.2 / KY, (x - CX) / KX); r = 470 + 26 * math.sin(3 * a + 0.7) + 18 * math.sin(5 * a + 2.1)
    return math.hypot((x - CX) / KX, (y - CY) / 1.2 / KY) < r
def sim(seed):
    rnd = random.Random(seed)
    ag = {}
    starts = [PY[k] for k in (1, 3, 5, 7)]; rnd.shuffle(starts)
    for i, n in enumerate(NAMES):
        sx, sy = starts[i]
        ag[n] = dict(x=sx, y=sy + 40, vx=0.0, vy=0.0, tgt=None, spd=rnd.uniform(240, 270) * SPK, oc=-9, dist=0.0, ph=rnd.uniform(0, 6.3), greed=rnd.uniform(0.6, 1.4), fast=-9.0, sleep=-9.0, shield=-9.0)
    own = [None] * NP; prog = [0.0] * NP; capper = [None] * NP; pts = {n: 0.0 for n in NAMES}
    gum = None; gsched = GSCHED
    frames = []; events = []; leaders = []
    for f in range(int((DUR + T0) * FPS)):
        t = f / FPS; dt = 1 / FPS; tt = t - T0
        if tt >= 0:
            for gt in gsched:
                if abs(tt - gt) < dt / 2:
                    a = rnd.uniform(0, 6.28); r = rnd.uniform(80, 260); gum = dict(x=CX + KX * r * math.cos(a), y=CY + KY * 1.2 * r * math.sin(a), k=rnd.choice(['mush', 'acv', 'mel', 'cre']))
            for n, s in ag.items():
                if tt < s['sleep']: s['vx'] *= 0.5; s['vy'] *= 0.5; continue   # melatonin: asleep, stopped
                contested_here = s['tgt'] is not None and sum(1 for m in NAMES if math.hypot(ag[m]['x'] - PY[s['tgt']][0], ag[m]['y'] - PY[s['tgt']][1]) < 80) > 1
                if s['tgt'] is None or own[s['tgt']] == n or rnd.random() < 0.004 or (contested_here and rnd.random() < 0.035):
                    best = None
                    for i, (px, py) in enumerate(PY):
                        if own[i] == n: continue
                        d = math.hypot(px - s['x'], py - s['y'])
                        lead_c = max(pts.values()) if pts else 0
                        sc = d / s['greed'] - (120 if own[i] is not None else 0) - (160 if own[i] is not None and pts[own[i]] == lead_c else 0) + rnd.uniform(0, 120) + 140 * sum(1 for m in NAMES if m != n and ag[m]['tgt'] == i)
                        if best is None or sc < best[0]: best = (sc, i)
                    s['tgt'] = best[1] if best else None
                tx, ty = PY[s['tgt']] if s['tgt'] is not None else (CX, CY)
                if gum and math.hypot(gum['x'] - s['x'], gum['y'] - s['y']) < 230: tx, ty = gum['x'], gum['y']
                dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                sp = s['spd'] * (1 + 0.15 * math.sin(1.7 * t + s['ph'])) * (1 + 0.1 * (max(pts.values()) - pts[n])) * (1.6 if tt - s['fast'] < 3.0 else 1.0)
                if L < 40: sp *= L / 40
                s['vx'] += (dx / L * sp - s['vx']) * 0.15; s['vy'] += (dy / L * sp - s['vy']) * 0.15
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                for m, o in ag.items():
                    if m == n: continue
                    ddx, ddy = nx - o['x'], (ny - o['y']) * 1.5; dd = math.hypot(ddx, ddy)
                    if 0 < dd < 70: nx += ddx / dd * (70 - dd) * 0.4; ny += ddy / dd * (70 - dd) * 0.25
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                if gum and math.hypot(gum['x'] - s['x'], gum['y'] - s['y']) < 50:
                    k = gum['k']; events.append((t, 'gum', n, k)); gum = None
                    if k == 'mush': s['fast'] = tt                                  # SPEED
                    elif k == 'acv': s['shield'] = tt                               # SHIELD: blocks the next shove/sleep (up to 6s)
                    elif k in ('cre', 'mel'):
                        for m, o in ag.items():
                            if m == n: continue
                            if k == 'cre' and math.hypot(o['x'] - s['x'], o['y'] - s['y']) > 300: continue   # STRONG: shoves everyone close by
                            if tt - o['shield'] < 6.0: o['shield'] = -9.0; events.append((t, 'block', m, None)); continue
                            if k == 'mel': o['sleep'] = tt + 1.0; o['tgt'] = None   # SLEEP: everyone else stops ~1s
                            else:
                                ddx, ddy = o['x'] - s['x'], o['y'] - s['y']; dd = math.hypot(ddx, ddy) or 1
                                o['vx'] += ddx / dd * 900; o['vy'] += ddy / dd * 700; events.append((t, 'shove', m, None))
                            for i_ in range(NP):
                                if capper[i_] == m: prog[i_] = 0.0; capper[i_] = None
            for i, (px, py) in enumerate(PY):
                near = [n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80 and tt >= ag[n]['sleep']]
                if len(set(near)) == 1 and own[i] != near[0]:
                    n = near[0]
                    if capper[i] != n: capper[i] = n; prog[i] = 0.0
                    rate = 1.0 * (1 + 0.25 * (max(pts.values()) - pts[n]))
                    prog[i] += dt * rate / CAP
                    if prog[i] >= 1: own[i] = n; prog[i] = 0.0; capper[i] = None; events.append((t, 'cap', n, i))
                elif len(set(near)) > 1:
                    pass
                else:
                    prog[i] = max(0.0, prog[i] - dt / CAP * 0.5)
                    if prog[i] == 0: capper[i] = None
            for n in NAMES: pts[n] = sum(1 for o in own if o == n)
            srt = sorted(pts.values())
            lead = max(NAMES, key=lambda n: pts[n])
            if srt[-1] > srt[-2] and (not leaders or leaders[-1] != lead): leaders.append(lead); events.append((t, 'lead', lead, None))
        frames.append(dict(ag={n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], dist=s['dist'], fast=s['fast'], sleep=s['sleep'], shield=s['shield']) for n, s in ag.items()}, own=list(own), prog=list(prog), capper=list(capper), pts=dict(pts), gum=dict(gum) if gum else None,
                           contested=[len(set(n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80)) > 1 for (px, py) in PY]))
    return frames, events, pts, leaders
def score(seed):
    fr, ev, pts, ld = sim(seed)
    sh = sorted(((v, n) for n, v in pts.items()), reverse=True)
    win = sh[0][1]
    if win not in ('ray',): return None
    if sh[0][0] != sh[1][0] + 1 or len(ld) < 6 or sh[-1][0] < 1: return None
    # late drama: leader in the last 6 seconds changes at least once
    late = [e for e in ev if e[1] == 'lead' and e[0] > T0 + DUR - 4]
    if not late or late[-1][2] != 'ray': return None
    ks = [e[3] for e in ev if e[1] == 'gum']
    if 'acv' not in ks or len(set(ks)) < 3: return None
    return win, [(n, p) for p, n in sh], len(ld), round(late[-1][0], 1), [(round(e[0], 1), e[2], e[3]) for e in ev if e[1] == 'gum'], [(round(e[0], 1), e[1], e[2]) for e in ev if e[1] in ('block', 'shove')]
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, PTS, LD = sim(SEED)
srt = sorted(((v, n) for n, v in PTS.items()), reverse=True); WIN = srt[0][1]
print('final', srt, 'leads', len(LD))
SS = 3; FOOT = 78 * SS   # rc9: guides 2x -> 3x
SRUN = {g: seq(PL + f'race/{g}_run', SS, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', SS, 1, 9) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=COL[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}
T = wang(A9 + 'gen/sky_meta.json', A9 + 'gen/sky_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
TS = 64; AY0 = 0; GC, GR = 17, 30   # hfg9: sky/cloud field runs to the top edge (castle header strip gone)
CORN = [[not inside(i * TS - 4, AY0 + j * TS) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (200, 220, 240, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); tl = T[key]
        if all(key) or not any(key):
            if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * TS - 4, AY0 + j * TS))
PYL = up(crop(Image.open(A9 + 'gen/pylon/01.png').convert('RGBA')), 2)
def tint(im, col, k=0.6):
    a = im.getchannel('A'); c = Image.new('RGBA', im.size, col + (255,)); c.putalpha(a)
    out = Image.blend(im, c, k); top = im.copy()
    h = int(im.height * 0.66)
    top.paste(out.crop((0, 0, im.width, h)), (0, 0)); return top
PYT = {n: tint(PYL, COL[n]) for n in NAMES}
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
GUM = {k: gummy(k, 3) for k in ['mush', 'cre', 'mel']}; GUM['acv'] = up(acv_gummy_strong(), 3)   # gummies 2x -> 3x, ACV with gummy shine
HDR = bg_frames('vit_hd.gif', (W, 470), box=(0, 60, 1920, 60 + 835), step=2, bright=0.65)
VICF = vic(WIN, 330)
END = T0 + DUR + 1.5
import hook as HK
def band(lines, accent, sub, subsize=46, color=(255, 214, 60)):
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
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=(255, 255, 255), stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
HOOK, HB = band(['ARENA WAR'], 0, 'COMMENT YOUR PICK')   # rc9: comment prompt (46px) from frame 0
OLDHB = HB
HOOK, HB = HK.hook_band(['ARENA WAR'], accent=0, size=80, y=262, alpha=0)   # hfg9: full-width strip style (busy clouds), text only here; strip drawn under the scoreboard
HOOK_END, _ = HK.hook_band(['DID YOUR', 'PICK WIN?'], accent=1, size=60, y=262, alpha=0)   # end question replaces the hook text
RULE = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # the rule as a secondary line inside the same fade, first 1.6s only (PICK ONE! plate cut)
_d = ImageDraw.Draw(RULE); _f = ImageFont.truetype(HK.FONT, 44); _w = _d.textlength('MOST CRYSTALS WINS', font=_f)
_d.text((W / 2 - _w / 2, 380), 'MOST CRYSTALS WINS', font=_f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(12, 8, 20))
SB0 = 442; print('hook bottom', HB, 'old', OLDHB)
PW = {'mush': ('SPEED!', (255, 170, 50)), 'cre': ('STRONG!', (255, 96, 60)), 'acv': ('SHIELD!', (110, 235, 110)), 'mel': ('SLEEP!', (200, 140, 255))}
# stamps: one slot, newest replaces older (never two at once); lead changes held < 0.6s are skipped
LEADS = [e for e in EV if e[1] == 'lead']
STAMPS = []
for k_, e in enumerate(LEADS):
    nxt = LEADS[k_ + 1][0] if k_ + 1 < len(LEADS) else 1e9
    if nxt - e[0] >= 0.6 and e[0] > T0 + 1.5: STAMPS.append((e[0], 'lead', e[2]))
for e in EV:
    if e[1] == 'gum': STAMPS.append((e[0], 'gum', e[2], e[3]))
    if e[1] == 'block': STAMPS.append((e[0], 'block', e[2]))
STAMPS.append((T0 + DUR - 5, 'final', None)); STAMPS.sort(key=lambda x: x[0])
last_ = -9
for k_ in range(len(STAMPS)):
    t_ = max(STAMPS[k_][0], last_ + 0.75); STAMPS[k_] = (t_,) + STAMPS[k_][1:]; last_ = t_   # each stamp gets >= 0.75s
print('stamps', [(round(x[0], 2),) + x[1:] for x in STAMPS])
ACV_T = next((f / FPS for f, st_ in enumerate(FR) if st_['gum'] and st_['gum']['k'] == 'acv'), None)
wr = Writer('v85_noaudio.mp4'); out_ev = []
rr = random.Random(9); CLOUDS = [(rr.uniform(-200, W), rr.uniform(AY0, H), rr.uniform(60, 140), rr.uniform(10, 30)) for _ in range(16)]
KEYF = [int(os.environ.get('K%d' % i, -1)) for i in range(5)]
for f in range(int(round(END * FPS))):
    t = f / FPS; st = FR[min(f, len(FR) - 1)]; tt = t - T0; live = tt >= 0 and t < T0 + DUR
    img = GROUND.copy()
    def clouds(d):
        for (x0, y0, r, sp) in CLOUDS:
            x = (x0 + t * sp) % (W + 300) - 150
            if any(inside(x + dx, y0 + dy) for dx in (-r - 20, 0, r + 20) for dy in (-r * 0.5 - 20, 0, r * 0.5 + 20)): continue
            d.ellipse([x - r, y0 - r * 0.5, x + r, y0 + r * 0.5], fill=(255, 255, 255, 110))
    layer(img, clouds)
    def glows(d):
        for i, (px, py) in enumerate(PY):
            o = st['own'][i]
            if o:
                p = 0.5 + 0.5 * math.sin(t * 4 + i)
                d.ellipse([px - 70, py - 30, px + 70, py + 30], fill=COL[o] + (int(70 + 50 * p),))
            cont = st['contested'][i] and live
            d.ellipse([px - 80, py - 34, px + 80, py + 34], outline=(255, 90, 80, int(150 + 100 * math.sin(t * 12))) if cont else (255, 255, 255, 90), width=6 if cont else 3)
            if st['capper'][i] and st['prog'][i] > 0:
                c = st['capper'][i]; d.arc([px - 80, py - 34, px + 80, py + 34], -90, -90 + 360 * st['prog'][i], fill=COL[c] + (255,), width=10)
    layer(img, glows)
    if st['gum']:
        g = st['gum']; gi = GUM[g['k']]; bob = int(6 * math.sin(t * 5))
        layer(img, lambda d: d.ellipse([g['x'] - 40, g['y'] - 20, g['x'] + 40, g['y'] + 12], fill=(255, 230, 140, 120)))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height - 6 + bob)))
    objs = [(py, 'p', i) for i, (px, py) in enumerate(PY)] + [(st['ag'][n]['y'], 'a', n) for n in NAMES]
    layer(img, lambda d: [d.ellipse([st['ag'][n]['x'] - 40, st['ag'][n]['y'] - 11, st['ag'][n]['x'] + 40, st['ag'][n]['y'] + 11], fill=(0, 0, 0, 80)) for n in NAMES])
    over = []
    for _, kind, key in sorted(objs, key=lambda o: o[0]):
        if kind == 'p':
            px, py = PY[key]; o = st['own'][key]; im = PYT[o] if o else PYL
            img.alpha_composite(im, (int(px - im.width / 2), int(py - im.height + 14)))
        else:
            n = key; s = st['ag'][n]; x, y = s['x'], s['y']; v = math.hypot(s['vx'], s['vy']) or 1
            if not live or tt < s['sleep']: spr = STAND[n]
            else:
                ph = int(s['dist'] / 30) % 8
                spr = STAND[n] if v < 25 else (FRUN[n][ph] if s['vy'] > 0.75 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph])
            if live and 0 <= tt - s['fast'] < 3.0 and v > 25:   # SPEED: speed lines + dust
                ux, uy = s['vx'] / v, s['vy'] / v
                layer(img, lambda d: [d.line([x - ux * (40 + 30 * q) - uy * o_, y - 80 - uy * (40 + 30 * q) + ux * o_, x - ux * (120 + 30 * q) - uy * o_, y - 80 - uy * (120 + 30 * q) + ux * o_], fill=(255, 255, 255, 210), width=6) for q, o_ in ((0, -36), (1, 0), (0, 36), (2, -16), (2, 18))])
                layer(img, lambda d: [d.ellipse([x - ux * (34 + 28 * q) - 16 + 6 * q, y - 12 - 3 * q, x - ux * (34 + 28 * q) + 16 - 6 * q, y + 8], fill=(225, 215, 200, 170 - 45 * q)) for q in range(3)])
            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
            if live and 0 <= tt - s['shield'] < 6.0:   # SHIELD bubble
                cy_ = y - 92; r_ = 108 + 3 * math.sin(t * 6)
                over.append(lambda d, x=x, cy_=cy_, r_=r_: (d.ellipse([x - r_, cy_ - r_, x + r_, cy_ + r_], fill=(110, 235, 110, 50), outline=(150, 255, 150, 230), width=7), d.arc([x - r_ + 20, cy_ - r_ + 20, x + r_ - 20, cy_ + r_ - 20], 200, 250, fill=(235, 255, 235, 230), width=7)))
            if live and tt < s['sleep']:   # SLEEP Zzz
                for q in range(3):
                    u = ((tt - s['sleep'] + 1.0) * 1.3 + q / 3) % 1.0
                    over.append((x + 30 + 36 * u, y - FOOT + 30 - 80 * u, 'Z', 44 - 8 * q, (220, 200, 255), 7, int(255 * min(1, 2 * (1 - u)))))
    for o in over:
        if callable(o): layer(img, o)
    text_layer(img, [o for o in over if not callable(o)])
    # power bursts
    for e in EV:
        u = t - e[0]
        if e[1] == 'gum' and 0 <= u < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)]['ag'][e[2]]; bx, by = s0['x'], s0['y'] - 80; col = PW[e[3]][1]; al = int(240 * (1 - u / 0.6))
            if e[3] == 'cre':
                rad = 60 + 330 * u
                layer(img, lambda d: [d.line([bx + math.cos(a_) * rad * 0.45, by + math.sin(a_) * rad * 0.45, bx + math.cos(a_) * rad, by + math.sin(a_) * rad], fill=col + (al,), width=14) for a_ in [k_ * 0.785 + 0.39 for k_ in range(8)]])
            else:
                rad = 50 + 240 * u; layer(img, lambda d: d.ellipse([bx - rad, by - rad, bx + rad, by + rad], outline=col + (al,), width=10))
        if e[1] == 'block' and 0 <= u < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)]['ag'][e[2]]; px, py = s0['x'], s0['y'] - 92; rad = 110 + 160 * u; al = int(230 * (1 - u / 0.6))
            layer(img, lambda d: [d.rectangle([px + math.cos(a_) * rad - 8, py + math.sin(a_) * rad - 8, px + math.cos(a_) * rad + 8, py + math.sin(a_) * rad + 8], fill=(150, 255, 150, al)) for a_ in [k_ * 0.628 for k_ in range(10)]])
        if abs(t - e[0]) < 0.5 / FPS:
            if e[1] == 'cap': out_ev.append((round(e[0], 3), 'chime'))
            elif e[1] == 'gum': out_ev.append((round(e[0], 3), 'powerup_8bit')); out_ev += [(round(e[0] + 0.05, 3), 'punch')] if e[3] == 'cre' else []
            elif e[1] == 'block': out_ev.append((round(e[0], 3), 'poof'))
    if False:   # hfg9: ACV GUMMY tag cut (consistency rule)
        g = st['gum']; tx_ = min(max(g['x'], 70 + 222), 887 - 222); ty_ = g['y'] + 26
        layer(img, lambda d: d.rounded_rectangle([tx_ - 222, ty_ - 8, tx_ + 222, ty_ + 60], 12, fill=(14, 10, 24, 225), outline=(110, 235, 110, 255), width=4))
        text_layer(img, [(tx_, ty_ + 4, 'ACV GUMMY', 44, (255, 255, 255), 6, 255)])
    # header: sky + band + live scoreboard chips (sorted, leader gold-framed) + timer
    cnt = {n: sum(1 for o in st['own'] if o == n) for n in NAMES}
    order = sorted(NAMES, key=lambda n: (-cnt[n], NAMES.index(n))); lead_ok = cnt[order[0]] > cnt[order[1]]
    layer(img, lambda d: d.rectangle([0, 262, W, SB0 + 106], fill=(10, 8, 20, 170)))   # hfg9: one edge-to-edge translucent strip behind hook + scoreboard, no border
    for r, n in enumerate(order):
        cx_ = 100 + r * 186; ic = ICON[n]
        if r == 0 and lead_ok: layer(img, lambda d, cx_=cx_: d.rounded_rectangle([cx_ - 8, SB0 + 8, cx_ + 172, SB0 + 92], 14, outline=(255, 214, 60, 255), width=5, fill=(60, 45, 10, 200)))
        img.alpha_composite(ic, (cx_, SB0 + 50 - ic.height // 2))
        text_layer(img, [(cx_ + 124, SB0 + 22, str(cnt[n]), 56, COL[n], 8, 255)])
    rem = max(0.0, DUR - max(0, tt))
    hot = 0 < rem <= 5 and live
    text_layer(img, [(935, SB0 + 28, f'{int(math.ceil(rem))}s', 48 if not hot else int(48 + 6 * (1 - (rem % 1))), (255, 110, 100) if hot else (255, 255, 255), 7, 255)])
    if hot and abs(rem - round(rem)) < 0.5 / FPS: out_ev.append((round(t, 3), 'tick_8bit'))
    # stamp slot
    cur = None
    for k_, x_ in enumerate(STAMPS):
        nxt = STAMPS[k_ + 1][0] if k_ + 1 < len(STAMPS) else 1e9
        if x_[0] <= t < min(x_[0] + 1.0, nxt) and live: cur = x_
    if cur:
        if cur[1] == 'lead': ic, l1, l2, col = ICON[cur[2]], LABEL[cur[2]] + ' LEADS!', None, COL[cur[2]]   # hfg9: one line
        elif cur[1] == 'gum': ic, l1, l2, col = ICON[cur[2]], PW[cur[3]][0], None, PW[cur[3]][1]
        elif cur[1] == 'block': ic, l1, l2, col = ICON[cur[2]], 'BLOCKED!', None, (110, 235, 110)
        else: cur = None   # hfg9: FINAL SECONDS! cut (the red pulsing timer + ticks say it)
    if cur:
        k_ = min(1.0, (t - cur[0]) / 0.08); fs1 = int((48 if cur[1] == 'lead' else 56) * (1.15 - 0.15 * k_))
        w1 = ImageDraw.Draw(img).textlength(l1, font=F(fs1)); w2 = ImageDraw.Draw(img).textlength(l2, font=F(44)) if l2 else 0
        bw = max(w1 + (ic.width + 24 if ic else 0), w2) + 56; sx0 = int(547 - bw / 2); sy0 = SB0 + 112; bh = 92 if not l2 else 150
        # hfg9: stamps unboxed
        lx = sx0 + 28
        if ic: img.alpha_composite(ic, (lx, sy0 + 46 - ic.height // 2)); lx += ic.width + 24
        text_layer(img, [(lx + w1 / 2, sy0 + 46 - fs1 // 2, l1, fs1, col, 9, 255)] + ([(547, sy0 + 92, l2, 44, (255, 255, 255), 7, 255)] if l2 else []))
        if abs(t - cur[0]) < 0.5 / FPS and cur[1] == 'lead': out_ev.append((round(t, 3), 'ding_8bit'))
    if t < 1.6:   # PICK ONE! + the rule over the opening sprint
        if f == 0: out_ev.append((0.0, 'go_8bit'))
    if t >= T0 + DUR:   # win card: hard pop, 1.5s, then loops to the opening sprint
        u = t - T0 - DUR
        layer(img, lambda d: d.rectangle([0, SB0 + 104, W, H], fill=(8, 6, 14, 150)))
        text_layer(img, [(540, 700, LABEL[WIN] + ' CONQUERS', 52, (255, 214, 60), 9, 255)])   # hfg9: unboxed, 'WITH N CRYSTALS' cut (scoreboard shows it)
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1260 - vf.height))
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T0 + DUR, 3), 'victory'))
    img.alpha_composite(HOOK_END if t >= T0 + DUR else HOOK)
    if t < 1.6: img.alpha_composite(RULE)
    wr.write(img)
    if f in KEYF: img.convert('RGB').save(f'k85_{f}.png')
wr.close(); json.dump({'events': sorted(out_ev)}, open('v85_ev.json', 'w')); print('done', round(END, 2))
