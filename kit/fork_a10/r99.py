import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
OUT = SP + 'fork_a10/v99/'
G4 = ['joy', 'cyrus', 'cleo', 'ray']; KIND = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
COL = {'joy': (110, 210, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 100, 240)}
NAME = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
LW = 270; TOP = 380; FLOOR = 1760
T0, GAME = 2.4, 30.0; T_END = T0 + GAME; END = T_END + 3.6
def sim(seed):
    rnd = random.Random(seed)
    st = {g: dict(x=LW / 2, vx=0, score=0, stun=-9, tgt=None, react=rnd.uniform(0.12, 0.3), spd=rnd.uniform(470, 540), face=1, dist=0.0) for g in G4}
    items = {g: [] for g in G4}; next_t = {g: T0 + rnd.uniform(0, 0.4) for g in G4}
    frames = []; events = []; lead = []
    for f in range(int(END * FPS)):
        t = f / FPS; dt = 1 / FPS
        for li, g in enumerate(G4):
            s = st[g]
            if T0 <= t < T_END - 0.3 and t >= next_t[g]:
                r = rnd.random(); kind = 'slime' if r < 0.18 else ('gold' if r < 0.24 else KIND[g])
                items[g].append(dict(x=rnd.uniform(45, LW - 45), y=TOP - 40, vy=rnd.uniform(260, 420) + 6 * (t - T0), kind=kind, born=t, alive=True))
                next_t[g] = t + rnd.uniform(0.32, 0.62)
            # move items + catch
            for it in items[g]:
                if not it['alive']: continue
                it['vy'] += 220 * dt; it['y'] += it['vy'] * dt
                hx, hy = s['x'], FLOOR - 230
                if abs(it['x'] - hx) < 62 and hy - 40 < it['y'] < hy + 50 and t - s['stun'] > 0.9:
                    it['alive'] = False; it['missed'] = -99
                    if it['kind'] == 'slime': s['stun'] = t; events.append((t, g, 'slime', it['x']))
                    else:
                        pts = 3 if it['kind'] == 'gold' else 1; s['score'] += pts; events.append((t, g, it['kind'], it['x']))
                elif it['y'] > FLOOR + 30: it['alive'] = False; it['missed'] = t
            # AI: chase the best gummy, avoid slimes
            if t >= T0 and t - s['stun'] > 0.9:
                best = None; bsc = -1e9
                for it in items[g]:
                    if not it['alive'] or it['born'] > t - s['react']: continue
                    tt = max(0.01, (FLOOR - 230 - it['y']) / max(it['vy'], 50))
                    reach = abs(it['x'] - s['x']) / s['spd']
                    val = (3 if it['kind'] == 'gold' else 1) if it['kind'] != 'slime' else -2
                    sc = val * 2 - tt - max(0, reach - tt) * 4 + rnd.uniform(-0.25, 0.25)
                    if val > 0 and sc > bsc: bsc, best = sc, it
                tx = best['x'] if best else LW / 2
                # dodge slime overhead
                for it in items[g]:
                    if it['alive'] and it['kind'] == 'slime' and abs(it['x'] - s['x']) < 70 and FLOOR - 600 < it['y'] < FLOOR - 200:
                        tx = s['x'] + (90 if it['x'] < s['x'] else -90)
                dx = tx - s['x']; v = max(-s['spd'], min(s['spd'], dx * 7))
                s['vx'] += (v - s['vx']) * 0.35
            else: s['vx'] *= 0.7
            nx = min(max(s['x'] + s['vx'] * dt, 55), LW - 55); s['dist'] += abs(nx - s['x']); s['x'] = nx
            if abs(s['vx']) > 30: s['face'] = 1 if s['vx'] > 0 else -1
            items[g] = [it for it in items[g] if it['alive'] or t - it.get('missed', t) < 0.4]
        sc = {g: st[g]['score'] for g in G4}; mx = max(sc.values())
        if mx > 0:
            ld = [g for g in G4 if sc[g] == mx]
            if len(ld) == 1 and (not lead or lead[-1] != ld[0]): lead.append(ld[0])
        frames.append(({g: dict(x=st[g]['x'], vx=st[g]['vx'], score=st[g]['score'], stun=st[g]['stun'], face=st[g]['face'], dist=st[g]['dist']) for g in G4},
                       {g: [dict(it) for it in items[g]] for g in G4}))
    fin = {g: st[g]['score'] for g in G4}
    return frames, events, fin, lead
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        fr, ev, fin, ld = sim(seed); srt = sorted(fin.values(), reverse=True)
        if srt[0] - srt[1] in (1, 2) and len(ld) >= 6 and srt[1] != srt[2] + 100:
            print(seed, fin, len(ld), ld[-4:], flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, FIN, LEAD = sim(SEED)
WIN = max(G4, key=lambda g: FIN[g]); print('final', FIN, 'leads', len(LEAD), WIN)
# lane art
BGN = {'joy': 'found_hd.gif', 'cyrus': 'sun_hd.gif', 'cleo': 'vit_hd.gif', 'ray': 'recov_hd.gif'}
LANE = {}
for g in G4:
    LANE[g] = bg_frames(BGN[g], (LW, FLOOR - TOP + 160), box=(960 - 250, 0, 960 + 250, 1080), step=6, bright=0.85)
RUN = {g: seq(PL + f'race/{g}_run', 3, 1, 9) for g in G4}; RUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in RUN.items()}
IDL = {g: idle(g, 3) for g in G4}; PAN = {g: seq(PL + f'maze/anim/{g}_panic', 3, 1, 9) for g in G4}
BASKET = up(crop(Image.open(PL + 'steal/basket/01.png').convert('RGBA')), 2)
GUMI = {k: gummy(k, 3) for k in ['acv', 'mush', 'cre', 'mel', 'gold']}
SLI = slime_frames(2)
ICON = {}
for g in G4:
    im = idle(g, 1)[0]; bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = {g: vic(g, 420) for g in G4}
HUD = 340
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS); pops = []
for f in range(NF):
    t = f / FPS; st, items = FR[min(f, len(FR) - 1)]
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for li, g in enumerate(G4):
        x0 = li * LW
        lane = LANE[g][int(t * 5) % len(LANE[g])].copy()
        if t >= T_END and g != WIN: lane = ImageEnhance.Brightness(lane).enhance(0.45)
        img.alpha_composite(lane, (x0, TOP))
        # floor ledge
        layer(img, lambda d: (d.rectangle([x0, FLOOR, x0 + LW, H], fill=(40, 30, 44, 255)), d.rectangle([x0, FLOOR, x0 + LW, FLOOR + 10], fill=COL[g] + (255,))))
        # items
        for it in items[g]:
            if it['kind'] == 'slime': spr = SLI[int(t * 8) % len(SLI)]
            else: spr = GUMI[it['kind']]
            a = 255 if it['alive'] else int(255 * max(0, 1 - (t - it.get('missed', t)) / 0.4))
            if it['alive'] or a > 0:
                s2 = spr.copy()
                if a < 255: s2.putalpha(s2.getchannel('A').point(lambda p, a=a: p * a // 255))
                img.alpha_composite(s2, (int(x0 + it['x'] - s2.width / 2), int(it['y'] - s2.height / 2)))
        # guide
        s = st[g]; x = x0 + s['x']
        if t >= T_END and g == WIN: pass
        elif t - s['stun'] < 0.9:
            fr = PAN[g][int(t * 12) % 8]
        elif t < T0 or abs(s['vx']) < 25: fr = IDL[g][int(t * 8) % len(IDL[g])]
        else: fr = (RUN if s['face'] > 0 else RUNL)[g][int(s['dist'] / 26) % 8]
        if not (t >= T_END and g == WIN):
            layer(img, lambda d: d.ellipse([x - 50, FLOOR - 12, x + 50, FLOOR + 10], fill=(0, 0, 0, 90)))
            img.alpha_composite(fr, (int(x - fr.width / 2), int(FLOOR - 78 * 3)))
            if t - s['stun'] >= 0.9 or t < T0: img.alpha_composite(BASKET, (int(x - BASKET.width / 2), int(FLOOR - 236 - BASKET.height // 2)))
            if t - s['stun'] < 0.9:
                def stars(d, x=x):
                    for k in range(3):
                        a2 = t * 8 + k * 2.1; sx2, sy2 = x + 50 * math.cos(a2), FLOOR - 250 + 16 * math.sin(a2)
                        d.polygon([(sx2, sy2 - 10), (sx2 + 4, sy2 - 3), (sx2 + 11, sy2), (sx2 + 4, sy2 + 3), (sx2, sy2 + 10), (sx2 - 4, sy2 + 3), (sx2 - 11, sy2), (sx2 - 4, sy2 - 3)], fill=(255, 230, 90, 255))
                layer(img, stars)
    # lane dividers (gold pillars)
    layer(img, lambda d: [d.rectangle([li * LW - 4, TOP, li * LW + 4, FLOOR + 10], fill=(200, 160, 60, 255)) for li in range(1, 4)])
    # pops
    for (te, g, kind, ix) in EV:
        u = t - te
        if 0 <= u < 0.8:
            x0 = G4.index(g) * LW + ix; a = int(255 * min(1, (0.8 - u) / 0.3))
            lab, c = ('BOING!', (150, 240, 120)) if kind == 'slime' else (('+3', (255, 214, 60)) if kind == 'gold' else ('+1', COL[g]))
            text_layer(img, [(x0, FLOOR - 340 - u * 60, lab, 36 if kind != 'slime' else 30, c, 6, a)])
        if abs(t - te) < 0.5 / FPS: ev.append((round(te, 3), {'slime': 'boing', 'gold': 'ding_8bit'}.get(kind, 'coin_8bit')))
    # HUD
    layer(img, lambda d: d.rectangle([0, 0, W, HUD + 40], fill=(14, 10, 24, 255)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 40, 'PICK YOUR', F(56)); ctext(d, W / 2, 112, 'GUIDE', F(70), (255, 214, 60), 7)
    sc = {g: st[g]['score'] for g in G4}; mx = max(sc.values())
    for li, g in enumerate(G4):
        cx = li * LW + LW / 2
        layer(img, lambda d2, cx=cx, g=g: d2.rounded_rectangle([cx - 118, 214, cx + 118, 352], 14, fill=(30, 22, 44, 255), outline=COL[g] + (255,), width=4))
        img.alpha_composite(ICON[g], (int(cx - 104), 236))
        d = ImageDraw.Draw(img)
        ctext(d, cx + 40, 250, str(sc[g]), F(52), (255, 214, 60) if sc[g] == mx and mx > 0 else (255, 255, 255), 6)
        ctext(d, cx, 322, NAME[g], F(20), COL[g], 4)
    # footer timer
    rem = max(0, T_END - max(t, T0)) if t >= T0 else GAME
    layer(img, lambda d2: d2.rectangle([0, H - 110, W, H], fill=(14, 10, 24, 230)))
    tc = (255, 90, 90) if rem <= 5 and t >= T0 else (255, 255, 255)
    text_layer(img, [(W / 2, H - 80, f'0:{int(math.ceil(rem)):02d}', 44, tc, 6, 255)])
    if t >= T0 and 0 < rem <= 5 and abs((rem % 1.0) - 0.0) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    if t < T0:
        text_layer(img, [(W / 2, 980, 'PICK ONE!', 72, (255, 255, 255), 9, 255)])
        if t > 1.2: text_layer(img, [(W / 2, 1080, 'Catch your gummies. Dodge the slimes', 26, (255, 230, 150), 5, 255)])
    if abs(t - T0) < 0.5 / FPS: ev.append((round(t, 3), 'go_8bit'))
    if T_END - 5 <= t < T_END - 4: text_layer(img, [(W / 2, 980, 'FINAL 5!', 64, (255, 90, 90), 8, int(255 * (1 - (t - (T_END - 5)))))])
    if t >= T_END:
        u = t - T_END
        li = G4.index(WIN); cx = li * LW + LW / 2
        vf = VICF[WIN][int(u * 8) % len(VICF[WIN])]
        img.alpha_composite(vf, (int(W / 2 - vf.width / 2), 1240 - vf.height))
        text_layer(img, [(W / 2, 1290, NAME[WIN] + ' WINS!', 64, COL[WIN], 8, int(255 * min(1, u / 0.3))), (W / 2, 1380, 'Did your guide win?', 32, (255, 255, 255), 5, int(255 * min(1, u / 0.3)))])
        def conf(d2):
            rr = random.Random(f)
            for _ in range(40):
                cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 450) % H
                d2.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([COL[WIN], (255, 214, 60), (255, 255, 255)]) + (230,))
        layer(img, conf)
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory'))
    w.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
