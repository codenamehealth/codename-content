import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
OUT = SP + 'fork_hfg11/v97/'
# rc11 (review recut; Bennett APPROVED #97, light fixes only, same seed/sim, Rayleigh still wins 9-8):
# reel starts 0.1s before the game (sim time offset 1.5s, the static 3-2-1 lead-in is skipped) with PICK ONE! +
# COMMENT YOUR PICK (46px) on a plate over the falling gummies until ~1.6s; FINAL 3! white on a dark plate for 1.0s;
# ACV gummy gloss + 'ACV GUMMY' tag; missed slimes/gummies clipped at the lane floor; outer pillars inset so the board
# ends at x884; pops/timer 44px; win hold 3.0 -> 1.2s then cut back to the start (loop).
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import gummy_src, acv_tag
def gummy(kind, k=2): return up(gummy_src(kind), k)
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade, hook_band
HSTYLE = os.environ.get('HSTYLE', 'fade')
if HSTYLE == 'band':
    HOOK, HB = hook_band(['PICK YOUR', 'GUIDE'], accent=1, size=72); HOOK2, _ = hook_band(['DID YOURS', 'WIN?'], accent=1, size=72)
else:
    HOOK, HB = hook_fade(['PICK YOUR', 'GUIDE'], accent=1, size=72); HOOK2, _ = hook_fade(['DID YOURS', 'WIN?'], accent=1, size=72)
print('hook bottom', HB)
G4 = ['joy', 'cyrus', 'cleo', 'ray']; KIND = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
COL = {'joy': (110, 210, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 100, 240)}
NAME = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
LW = 203; LX0 = 72; TOP = 700; FLOOR = 1480
T0, GAME = 1.6, 9.0; T_END = T0 + GAME; END = T_END + 1.2; OFF = T0 - 0.1
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
                r = rnd.random(); kind = 'slime' if r < 0.18 else KIND[g]
                items[g].append(dict(x=rnd.uniform(34, LW - 34), y=TOP - 40, vy=rnd.uniform(260, 420) + 6 * (t - T0), kind=kind, born=t, alive=True))
                next_t[g] = t + rnd.uniform(0.64, 1.24)   # half the gummies
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
            nx = min(max(s['x'] + s['vx'] * dt, 46), LW - 46); s['dist'] += abs(nx - s['x']); s['x'] = nx
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
        if srt[0] - srt[1] in (1, 2) and len(ld) >= 4:
            print(seed, fin, len(ld), ld[-4:], flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, FIN, LEAD = sim(SEED)
WIN = max(G4, key=lambda g: FIN[g]); print('final', FIN, 'leads', len(LEAD), WIN)
# lane art
BGN = {'joy': 'found_hd.gif', 'cyrus': 'sun_hd.gif', 'cleo': 'vit_hd.gif', 'ray': 'recov_hd.gif'}
# hfg11 full-bleed: each lane's scene runs from the frame top to the bottom edge; outer lanes run out to the frame edges
# (play area per lane unchanged: LX0 + li*LW .. +LW, so the sim is identical). Scene drawn at a uniform 1.37x (y0..FLOOR),
# below the floor ledge the lane's own ground is mirrored down and darkened (caption zone only).
VIS = {'joy': (0, LX0 + LW), 'cyrus': (LX0 + LW, LX0 + 2 * LW), 'cleo': (LX0 + 2 * LW, LX0 + 3 * LW), 'ray': (LX0 + 3 * LW, W)}
LANE = {}
for g in G4:
    vx0, vx1 = VIS[g]; wv = vx1 - vx0; bw = 1080 * wv / FLOOR
    out = []
    for fr_ in bg_frames(BGN[g], (wv, FLOOR), box=(int(960 - bw / 2), 0, int(960 + bw / 2), 1080), step=6, bright=0.85):
        full = Image.new('RGBA', (wv, H), (0, 0, 0, 255)); full.alpha_composite(fr_, (0, 0))
        mir = ImageEnhance.Brightness(fr_.crop((0, FLOOR - (H - FLOOR), wv, FLOOR)).transpose(Image.FLIP_TOP_BOTTOM)).enhance(0.55)
        full.alpha_composite(mir, (0, FLOOR)); out.append(full)
    LANE[g] = out
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
BGFULL = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=6, bright=0.35)
HUD = 340
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(round((END - OFF) * FPS)); pops = []; TAG = [None]
FRS = [int(x) for x in os.environ['ONLY'].split(',')] if os.environ.get('ONLY') else range(NF)
for f in FRS:
    TAGD = []; t = f / FPS + OFF; fs_ = int(round(t * FPS)); st, items = FR[min(fs_, len(FR) - 1)]
    img = BGFULL[int(t * 5) % len(BGFULL)].copy()
    for li, g in enumerate(G4):
        x0 = LX0 + li * LW; vx0, vx1 = VIS[g]
        lane = LANE[g][int(t * 5) % len(LANE[g])]
        if t >= T_END and g != WIN: lane = ImageEnhance.Brightness(lane).enhance(0.45)
        img.alpha_composite(lane, (vx0, 0))
        # floor ledge (full lane width)
        layer(img, lambda d: (d.rectangle([vx0, FLOOR, vx1, FLOOR + 56], fill=(40, 30, 44, 255)), d.rectangle([vx0, FLOOR, vx1, FLOOR + 10], fill=COL[g] + (255,))))
        # items
        for it in items[g]:
            if it['kind'] == 'slime': spr = SLI[int(t * 8) % len(SLI)]
            else: spr = GUMI[it['kind']]
            a = 255 if it['alive'] else int(255 * max(0, 1 - (t - it.get('missed', t)) / 0.4))
            if it['alive'] or a > 0:
                s2 = spr.copy()
                if a < 255: s2.putalpha(s2.getchannel('A').point(lambda p, a=a: p * a // 255))
                py_ = int(it['y'] - s2.height / 2)
                if py_ + s2.height > FLOOR: s2 = s2.crop((0, 0, s2.width, max(0, FLOOR - py_)))   # rc11: clip at the lane floor
                if s2.height > 0: img.alpha_composite(s2, (int(x0 + it['x'] - s2.width / 2), py_))
                if g == 'joy' and it['kind'] == 'acv' and it['alive'] and TAG[0] is None and t >= OFF + 1.4 and 760 < it['y'] < 900: TAG[0] = (t, it['born'])
                if TAG[0] and it['born'] == TAG[0][1] and it['kind'] == 'acv' and t - TAG[0][0] < 1.0:
                    TAGD.append((int(x0 + it['x']), int(it['y'] - s2.height / 2 - 4), int(255 * min(1, (t - TAG[0][0]) / 0.12, (1.0 - (t - TAG[0][0])) / 0.2))))
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
    layer(img, lambda d: [d.rectangle([LX0 + li * LW - 4, 0, LX0 + li * LW + 4, H], fill=(200, 160, 60, 255)) for li in range(1, 4)])
    # pops
    for (te, g, kind, ix) in EV:
        u = t - te
        if 0 <= u < 0.8:
            x0 = LX0 + G4.index(g) * LW + ix; a = int(255 * min(1, (0.8 - u) / 0.3))
            lab, c = ('BOING!', (150, 240, 120)) if kind == 'slime' else (('+3', (255, 214, 60)) if kind == 'gold' else ('+1', COL[g]))
            sz = 44; x0 = min(max(x0, 76 + len(lab) * sz / 2), 882 - len(lab) * sz / 2)   # inside the zone
            text_layer(img, [(x0, FLOOR - 340 - u * 60, lab, sz, c, 6, a)])
        if abs(t - te) < 0.5 / FPS: ev.append((round(te - OFF, 3), {'slime': 'boing', 'gold': 'ding_8bit'}.get(kind, 'coin_8bit')))
    # HUD
    sc = {g: st[g]['score'] for g in G4}; mx = max(sc.values())
    for li, g in enumerate(G4):
        cx = LX0 + li * LW + LW / 2; y0 = HB + 12
        layer(img, lambda d2, cx=cx, g=g: d2.rounded_rectangle([cx - 96, y0, cx + 96, y0 + 108], 14, fill=(30, 22, 44, 255), outline=COL[g] + (255,), width=4))
        img.alpha_composite(ICON[g], (int(cx - 92), y0 + 6))
        d = ImageDraw.Draw(img)
        ctext(d, cx + 46, y0 + 30, str(sc[g]), F(46), (255, 214, 60) if sc[g] == mx and mx > 0 else (255, 255, 255), 6)
    # footer timer
    rem = max(0, T_END - max(t, T0)) if t >= T0 else GAME
    tc = (255, 90, 90) if rem <= 3 and t >= T0 else (255, 255, 255)
    layer(img, lambda d2: d2.rounded_rectangle([378, HB + 128, 578, HB + 186], 10, fill=(14, 10, 24, 230)))
    text_layer(img, [(478, HB + 135, f'0:{int(math.ceil(rem)):02d}', 44, tc, 6, 255)])
    if t >= T0 and 0 < rem <= 3 and abs((rem % 1.0) - 0.0) < 0.5 / FPS: ev.append((round(t - OFF, 3), 'tick_8bit'))
    if abs(t - T0) < 0.5 / FPS: ev.append((round(t - OFF, 3), 'go_8bit'))
    if t >= T_END:
        u = t - T_END
        li = G4.index(WIN)
        vf = VICF[WIN][int(u * 8) % len(VICF[WIN])]
        img.alpha_composite(vf, (int(478 - vf.width / 2), 1270 - vf.height))
        text_layer(img, [(478, 762, NAME[WIN] + ' WINS!', 56, COL[WIN], 9, int(255 * min(1, u / 0.3)))])
        def conf(d2):
            rr = random.Random(f)
            for _ in range(40):
                cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 450) % H
                d2.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([COL[WIN], (255, 214, 60), (255, 255, 255)]) + (230,))
        layer(img, conf)
        if abs(u) < 0.5 / FPS: ev.append((round(t - OFF, 3), 'victory'))
    img.alpha_composite(HOOK2 if t >= T_END else HOOK)
    w.write(img)
    if f in (0, 15, 40, 200, int((T_END - 3 - OFF) * FPS) + 4, NF - 1) or os.environ.get('ONLY'): img.convert('RGB').save(OUT + f'k_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
