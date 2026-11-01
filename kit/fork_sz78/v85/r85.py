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
CX, CY = 478, 1110; KX, KY = 320 / 330, 330 / 430
SPK = float(os.environ.get('SPK', '0.88'))
PY = [(CX, CY)] + [(CX + 320 * math.cos(-math.pi / 2 + k * math.pi / 4), CY + 330 * math.sin(-math.pi / 2 + k * math.pi / 4)) for k in range(8)]
NP = len(PY); CAP = 1.3; DUR = 30.0; T0 = 2.4
def inside(x, y):
    a = math.atan2((y - CY) / 1.2 / KY, (x - CX) / KX); r = 470 + 26 * math.sin(3 * a + 0.7) + 18 * math.sin(5 * a + 2.1)
    return math.hypot((x - CX) / KX, (y - CY) / 1.2 / KY) < r
def sim(seed):
    rnd = random.Random(seed)
    ag = {}
    starts = [PY[k] for k in (1, 3, 5, 7)]; rnd.shuffle(starts)
    for i, n in enumerate(NAMES):
        sx, sy = starts[i]
        ag[n] = dict(x=sx, y=sy + 40, vx=0.0, vy=0.0, tgt=None, spd=rnd.uniform(240, 270) * SPK, oc=-9, dist=0.0, ph=rnd.uniform(0, 6.3), greed=rnd.uniform(0.6, 1.4))
    own = [None] * NP; prog = [0.0] * NP; capper = [None] * NP; pts = {n: 0.0 for n in NAMES}
    gum = None; gsched = [6.0, 11.0, 16.0, 21.0, 25.5]
    frames = []; events = []; leaders = []
    for f in range(int((DUR + T0) * FPS)):
        t = f / FPS; dt = 1 / FPS; tt = t - T0
        if tt >= 0:
            for gt in gsched:
                if abs(tt - gt) < dt / 2:
                    a = rnd.uniform(0, 6.28); r = rnd.uniform(80, 260); gum = dict(x=CX + KX * r * math.cos(a), y=CY + KY * 1.2 * r * math.sin(a), k=rnd.choice(['mush', 'acv', 'mel', 'cre']))
            for n, s in ag.items():
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
                sp = s['spd'] * (1 + 0.15 * math.sin(1.7 * t + s['ph'])) * (1 + 0.1 * (max(pts.values()) - pts[n]))
                if L < 40: sp *= L / 40
                s['vx'] += (dx / L * sp - s['vx']) * 0.15; s['vy'] += (dy / L * sp - s['vy']) * 0.15
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                for m, o in ag.items():
                    if m == n: continue
                    ddx, ddy = nx - o['x'], (ny - o['y']) * 1.5; dd = math.hypot(ddx, ddy)
                    if 0 < dd < 50: nx += ddx / dd * (50 - dd) * 0.4; ny += ddy / dd * (50 - dd) * 0.25
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                if gum and math.hypot(gum['x'] - s['x'], gum['y'] - s['y']) < 44:
                    s['oc'] = tt; events.append((t, 'gum', n, gum['k'])); gum = None
            for i, (px, py) in enumerate(PY):
                near = [n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80]
                if len(set(near)) == 1 and own[i] != near[0]:
                    n = near[0]
                    if capper[i] != n: capper[i] = n; prog[i] = 0.0
                    rate = (3.0 if tt - ag[n]['oc'] < 4.0 else 1.0) * (1 + 0.25 * (max(pts.values()) - pts[n]))
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
        frames.append(dict(ag={n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], dist=s['dist'], oc=s['oc']) for n, s in ag.items()}, own=list(own), prog=list(prog), capper=list(capper), pts=dict(pts), gum=dict(gum) if gum else None,
                           contested=[len(set(n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80)) > 1 for (px, py) in PY]))
    return frames, events, pts, leaders
def score(seed):
    fr, ev, pts, ld = sim(seed)
    sh = sorted(((v, n) for n, v in pts.items()), reverse=True)
    win = sh[0][1]
    if win not in ('ray',): return None
    if sh[0][0] != sh[1][0] + 1 or len(ld) < 6 or sh[-1][0] < 1: return None
    # late drama: leader in the last 6 seconds changes at least once
    late = [e for e in ev if e[1] == 'lead' and e[0] > T0 + DUR - 5]
    if not late: return None
    return win, [(n, p) for p, n in sh], len(ld), round(late[-1][0], 1)
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, PTS, LD = sim(SEED)
srt = sorted(((v, n) for n, v in PTS.items()), reverse=True); WIN = srt[0][1]
print('final', srt, 'leads', len(LD))
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', 2, 1, 9) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
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
ICON = {n: face(n, 26) for n in NAMES}
# island from the sky Wang tileset
T = wang(A9 + 'gen/sky_meta.json', A9 + 'gen/sky_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
TS = 64; AY0 = 470; GC, GR = 17, 23
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
GUM = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']}
HDR = bg_frames('vit_hd.gif', (W, 470), box=(0, 60, 1920, 60 + 835), step=2, bright=0.65)
VICF = vic(WIN, 330)
END = T0 + DUR + 3.4
HOOK, HB = hook_layer(['ARENA WAR'], accent=0, sub='HOLD THE MOST CRYSTALS')
SB0 = HB + 10; print('hook bottom', HB)
wr = Writer('v85_noaudio.mp4'); out_ev = []
rr = random.Random(9); CLOUDS = [(rr.uniform(-200, W), rr.uniform(AY0, H), rr.uniform(60, 140), rr.uniform(10, 30)) for _ in range(16)]
for f in range(int(END * FPS)):
    t = f / FPS; st = FR[min(f, len(FR) - 1)]; tt = t - T0
    img = GROUND.copy()
    def clouds(d):
        for (x0, y0, r, sp) in CLOUDS:
            x = (x0 + t * sp) % (W + 300) - 150
            if any(inside(x + dx, y0 + dy) for dx in (-r - 20, 0, r + 20) for dy in (-r * 0.5 - 20, 0, r * 0.5 + 20)): continue
            d.ellipse([x - r, y0 - r * 0.5, x + r, y0 + r * 0.5], fill=(255, 255, 255, 110))
    layer(img, clouds)
    # pylon glows + capture rings (under sprites)
    def glows(d):
        for i, (px, py) in enumerate(PY):
            o = st['own'][i]
            if o:
                p = 0.5 + 0.5 * math.sin(t * 4 + i)
                d.ellipse([px - 70, py - 30, px + 70, py + 30], fill=COL[o] + (int(70 + 50 * p),))
            d.ellipse([px - 80, py - 34, px + 80, py + 34], outline=(255, 255, 255, 90), width=3)
            if st['capper'][i] and st['prog'][i] > 0:
                c = st['capper'][i]; d.arc([px - 80, py - 34, px + 80, py + 34], -90, -90 + 360 * st['prog'][i], fill=COL[c] + (255,), width=8)
    layer(img, glows)
    if st['gum']:
        g = st['gum']; gi = GUM[g['k']]; bob = int(6 * math.sin(t * 5))
        layer(img, lambda d: d.ellipse([g['x'] - 32, g['y'] - 18, g['x'] + 32, g['y'] + 10], fill=(255, 230, 140, 110)))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height - 6 + bob)))
    # sprites + pylons y-sorted
    objs = [(py, 'p', i) for i, (px, py) in enumerate(PY)] + [(st['ag'][n]['y'], 'a', n) for n in NAMES]
    layer(img, lambda d: [d.ellipse([st['ag'][n]['x'] - 28, st['ag'][n]['y'] - 8, st['ag'][n]['x'] + 28, st['ag'][n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES])
    for _, kind, key in sorted(objs, key=lambda o: o[0]):
        if kind == 'p':
            px, py = PY[key]; o = st['own'][key]; im = PYT[o] if o else PYL
            img.alpha_composite(im, (int(px - im.width / 2), int(py - im.height + 14)))
        else:
            n = key; s = st['ag'][n]; x, y = s['x'], s['y']
            if tt < 0 or t >= T0 + DUR: spr = STAND[n]
            else:
                ph = int(s['dist'] / 22) % 8; v = math.hypot(s['vx'], s['vy']) or 1
                spr = STAND[n] if v < 25 else (FRUN[n][ph] if s['vy'] > 0.75 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph])
            if 0 <= tt - s['oc'] < 4.0:
                layer(img, lambda d, x=x, y=y, n=n: d.ellipse([x - 44, y - 16, x + 44, y + 16], outline=(255, 220, 90, 230), width=5))
            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    items = []
    for e in EV:
        u = t - e[0]
        if 0 <= u < 0.9:
            a = int(255 * min(1, (0.9 - u) / 0.3))
            if e[1] == 'cap': px, py = PY[e[3]]; items.append((min(max(px, 200), 760), py - 150 - u * 40, 'CAPTURED!', 26, COL[e[2]], 6, a))
            elif e[1] == 'gum':
                s = FR[min(int(e[0] * FPS), len(FR) - 1)]['ag'][e[2]]; items.append((min(max(s['x'], 230), 720), s['y'] - FOOT - 30 - u * 40, 'OVERCHARGE!', 28, (255, 214, 60), 6, a))
        if abs(t - e[0]) < 0.5 / FPS and e[1] in ('cap', 'gum'):
            out_ev.append((round(e[0], 3), 'chime' if e[1] == 'cap' else 'powerup_8bit'))
    for i, cont in enumerate(st['contested']):
        if cont and tt > 0 and t < T0 + DUR: px, py = PY[i]; items.append((px, py + 40, 'CONTESTED', 18, (255, 120, 100), 4, 220))
    text_layer(img, items)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: (d.rectangle([0, 0, W, 470], fill=(12, 8, 24, 80)), d.rounded_rectangle([76, SB0, 1019, SB0 + 156], 16, fill=(12, 8, 24, 215))))
    d = ImageDraw.Draw(img); d.rounded_rectangle([76, SB0, 1019, SB0 + 156], 16, outline=(255, 214, 60, 255), width=4)
    rem = max(0.0, DUR - max(0, tt)) if tt >= 0 else DUR
    text_layer(img, [(930, SB0 + 58, f'{int(math.ceil(rem))}s', 40, (255, 120, 100) if rem <= 5 and tt > 0 else (255, 255, 255), 6, 255)])
    # live scoreboard sorted
    cnt = {n: sum(1 for o in st['own'] if o == n) for n in NAMES}
    order = sorted(NAMES, key=lambda n: (-cnt[n], NAMES.index(n)))
    lead_ok = cnt[order[0]] > cnt[order[1]]
    rows = []
    for r, n in enumerate(order):
        y = SB0 + 12 + r * 33; ic = ICON[n].resize((30, 30), Image.NEAREST); img.alpha_composite(ic, (96, y))
        bw = int(420 * cnt[n] / NP)
        layer(img, lambda d, y=y, bw=bw, n=n: (d.rounded_rectangle([320, y + 6, 740, y + 24], 6, fill=(255, 255, 255, 40)), d.rounded_rectangle([320, y + 6, 320 + max(8, bw), y + 24], 6, fill=COL[n] + (255,)) if cnt[n] else None))
        rows.append((225, y + 6, LABEL[n], 20, COL[n], 4, 255)); rows.append((768, y + 5, f'{cnt[n]}', 22, (255, 255, 255), 4, 255))
        if r == 0 and lead_ok: rows.append((830, y + 6, 'LEAD', 18, (255, 214, 60), 3, 255))
    text_layer(img, rows)
    if tt < 0.4: text_layer(img, [(CX, CY - 190, 'PICK ONE!', 60, (255, 255, 255), 8, 255)])
    LE = [e for e in EV if e[1] == 'lead' and e[0] <= t]
    for e in LE[-1:]:
        if 0 <= t - e[0] < 1.2 and t < T0 + DUR and e[0] > T0 + 1:
            text_layer(img, [(CX, CY - 175, LABEL[e[2]] + ' TAKES THE LEAD!', 32, COL[e[2]], 7, int(255 * min(1, (1.2 - (t - e[0])) / 0.4)))])
            if abs(t - e[0]) < 0.5 / FPS and not any(abs(x[0] - e[0]) < 0.6 and x[1] == 'ding_8bit' for x in out_ev): out_ev.append((round(e[0], 3), 'ding_8bit'))
    if 0 < rem <= 5 and tt > 0 and t < T0 + DUR:
        text_layer(img, [(CX, SB0 + 166, f'FINAL SECONDS: {int(math.ceil(rem))}', 32, (255, 120, 100), 7, 255)])
        if abs(rem - round(rem)) < 0.5 / FPS: out_ev.append((round(t, 3), 'tick_8bit'))
    if t >= T0 + DUR:
        u = t - T0 - DUR
        layer(img, lambda d: d.rectangle([0, SB0 + 160, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1110 - vf.height))
        def conf(d):
            r2 = random.Random(f)
            for _ in range(45):
                x, y = r2.uniform(0, W), SB0 + 160 + (r2.uniform(0, H) + u * 500) % (1500 - SB0 - 160)
                d.rectangle([x, y, x + 10, y + 10], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (190, 90, 240)]) + (255,))
        layer(img, conf)
        text_layer(img, [(CX, 1150, LABEL[WIN] + ' CONQUERS', 46, (255, 214, 60), 8, 255), (CX, 1222, f'THE ARENA WITH {cnt[WIN]} CRYSTALS', 30, (255, 255, 255), 6, 255)])
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T0 + DUR, 3), 'victory'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(out_ev, open('v85_ev.json', 'w')); print('done', round(END, 2))
