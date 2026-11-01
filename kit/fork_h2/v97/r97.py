import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
OUT = SP + 'fork_h2/v97/'
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
    # fork_h2 Oct 29 hook swap (bottom edge kept): the race is tied 8-8 at 0:00 and Rayleigh's 9th lands after the buzzer,
    # so not IT COMES DOWN TO / THE LAST SECOND; fallback hook, broken WHO GRABS THE / MOST GUMMIES? so it fits at 70px (52px otherwise)
    sys.path.insert(0, SP + 'fork_h2'); import hookx
    HOOK, HB = hookx.fade_keep(['PICK YOUR', 'GUIDE'], ['WHO GRABS THE', [('MOST ', None), ('GUMMIES?', hookx.GOLD)]], size=72, old_accent=1)
    # fork_h2 buzzer fix (seed 2540 after review2): Cyrus breaks an 8-8 tie with Joy 0.37s before 0:00, nothing scores after the buzzer, so the real hook
    HOOK, HB = hookx.fade_keep(['PICK YOUR', 'GUIDE'], ['IT COMES DOWN TO', [('THE ', None), ('LAST SECOND', hookx.GOLD)]], size=72, old_accent=1)
print('hook bottom', HB)
G4 = ['joy', 'cyrus', 'cleo', 'ray']; KIND = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
COL = {'joy': (110, 210, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 100, 240)}
NAME = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
LW = 203; LX0 = 72; TOP = 700; FLOOR = 1480
VICX = int(os.environ.get('VICX', '478'))   # fork_h2: 478 = original centre; Rayleigh's staff needed 454 to stay inside the lower-right safe line (x887)
T0, GAME = 1.6, 9.0; T_END = T0 + GAME; END = T_END + 0.8; OFF = T0 - 0.1   # fork_h2 review3: end card 1.2 -> 0.8s
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
                if not it['alive'] and not it.get('buzz'): continue
                it['vy'] += 220 * dt; it['y'] += it['vy'] * dt
                hx, hy = s['x'], FLOOR - 230
                if it.get('buzz'): continue
                if t >= T_END:   # fork_h2 buzzer rule: nothing scores after 0:00; anything still in the air keeps falling and fades out (0.4s)
                    it['alive'] = False; it['missed'] = t; it['buzz'] = True; continue
                if abs(it['x'] - hx) < 62 and hy - 40 < it['y'] < hy + 50 and t - s['stun'] > 0.9:
                    it['alive'] = False; it['missed'] = -99
                    if it['kind'] == 'slime': s['stun'] = t; events.append((t, g, 'slime', it['x']))
                    else:
                        pts = 3 if it['kind'] == 'gold' else 1; s['score'] += pts; events.append((t, g, it['kind'], it['x']))
                elif it['y'] > FLOOR + 30: it['alive'] = False; it['missed'] = t
            # AI: chase the best gummy, avoid slimes
            if T0 <= t < T_END and t - s['stun'] > 0.9:   # fork_h2: runners stop at the buzzer
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
def last_second(ev, fin, ld):
    # fork_h2: the winner's deciding catch lands in the last ~1s before 0:00: before it the winner was NOT the sole leader
    srt = sorted(fin.values(), reverse=True)
    if srt[0] == srt[1]: return None
    win = max(G4, key=lambda g: fin[g]); sc = {g: 0 for g in G4}; lastc = None
    for (te, g, kind, ix) in sorted(ev):
        if kind == 'slime': continue
        before = dict(sc); sc[g] += 1
        if g == win: lastc = (te, before)
    if lastc is None or not (T_END - 1.0 <= lastc[0] < T_END - 0.05): return None
    te, before = lastc
    if before[win] < max(v for k, v in before.items() if k != win): pass   # was behind
    elif before[win] == max(v for k, v in before.items() if k != win): pass   # was tied
    else: return None   # already leading: not decided in the last second
    return win, round(T_END - te, 2), before
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        fr, ev, fin, ld = sim(seed); srt = sorted(fin.values(), reverse=True)
        r = last_second(ev, fin, ld)
        if r and srt[0] - srt[1] == 1 and len(ld) >= 4:
            print(seed, fin, 'leads', len(ld), ld[-4:], 'win', r[0], 'catch', r[1], 's before 0:00, before', r[2], flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, FIN, LEAD = sim(SEED)
sys.path.insert(0, SP + 'fork_h2/v97'); from pose_state import idle_mask
IDLEM = {g: idle_mask([FR[i][0][g]['vx'] for i in range(len(FR))]) for g in G4}
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
# ---- fork_h2 review3 additions ----
KO = {g: [up(Image.open(PL + f'king/{g}_ko/{i:02d}.png').convert('RGBA'), 3) for i in range(5)] for g in G4}   # PixelLab KO set (as in approved #19/#39): stand > stagger > flat
STUN_VIS = 0.45      # stars + BOING! only for the first 0.45s, so two stuns never show at once
def ko_frame(u):
    # u = time since the slime hit (sim stun lasts 0.9s): fall 0-0.2s, lie flat, get up 0.72-0.9s
    if u < 0.2: return min(4, int(u / 0.05))
    if u < 0.72: return 4
    return max(0, 4 - int((u - 0.72) / 0.045))
SLH = SLI[0].getbbox(); SL_HALF = (SLH[2] - SLH[0]) / 2; SL_H = SLH[3] - SLH[1]
# slimes that would fall through a guide's body: pick one straight-line x (whole fall) that clears the guide (visual only, sim untouched)
SLX = {}
for g in G4:
    paths = {}
    for i, (st_, its) in enumerate(FR):
        for it in its[g]:
            if it['kind'] != 'slime': continue
            paths.setdefault(it['born'], []).append((i, it['x'], it['y'], it['alive'], it.get('missed')))
    for born, pth in paths.items():
        if any(m == -99 for _, _, _, _, m in pth): continue          # caught: it stuns, keep its path
        lvl = [(i, FR[i][0][g]['x']) for i, x, y, al, m in pth if y > FLOOR - 205]
        if not lvl: continue
        x0_ = pth[0][1]; need = 52 + SL_HALF
        clear = lambda xv: min(abs(xv - gx) for _, gx in lvl)
        if clear(x0_) >= need: continue
        cands = [xv for xv in range(34, LW - 33) if clear(xv) >= need]
        xv = min(cands, key=lambda c: abs(c - x0_)) if cands else None   # no straight line clears the guide: this slime is not drawn at all
        SLX[(g, born)] = xv
        if xv is None: print('slime', g, round(born - OFF, 2), 'hidden (no clear line)', flush=True); continue
        print('slime', g, round(born - OFF, 2), 'x', round(x0_), '->', xv, 'clearance', round(clear(xv)), flush=True)
# visual-only gummy that drops right past Rayleigh while she is down (nobody can catch it, it scores nothing)
EXTRA = []
for (te_, gg, kd, ix_) in EV:
    if kd == 'slime':
        gx_ = FR[int(round(te_ * FPS))][0][gg]['x']
        lost = [it for it in FR[min(len(FR) - 1, int(round((te_ + 0.85) * FPS)))][1][gg] if it['kind'] != 'slime' and it['alive'] and it['born'] < te_ + 0.85]
        # does a real gummy already fall past during the stun?
        real = any(FLOOR - 300 < it2['y'] < FLOOR and it2['alive'] and it2['kind'] != 'slime'
                   for i in range(int(round(te_ * FPS)), int(round((te_ + 0.9) * FPS))) for it2 in FR[i][1][gg])
        if real: print('stun', gg, round(te_ - OFF, 2), 'a real gummy falls past', flush=True); continue
        xg = min(max(gx_, 34), LW - 34)   # the gummy she was about to catch: still above her when the slime hits, drops past once she is down
        ys = []; yy = TOP - 40.0; v = 380.0
        while yy < FLOOR + 30: ys.append(yy); v += 220 / FPS; yy += v / FPS
        f_land = int(round((te_ + 0.55) * FPS)); f0 = f_land - len(ys) + 1
        path = [(f0 + i, y_) for i, y_ in enumerate(ys)]
        print('  extra gummy y at the hit', round(dict(path).get(int(round(te_ * FPS)), -1)), 'basket height', FLOOR - 230, flush=True)
        EXTRA.append(dict(g=gg, kind=KIND[gg], x=xg, path=dict(path), land=path[-1][0]))
        print('extra gummy past', gg, 'x', round(xg), 'frames', path[0][0], '-', path[-1][0], flush=True)
ICON = {}
for g in G4:
    im = idle(g, 1)[0]; bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = {g: vic(g, 420) for g in G4}
_vb = VICF[WIN][0].getbbox(); _vx0 = int(VICX - VICF[WIN][0].width / 2); _vy0 = 1270 - VICF[WIN][0].height
VRECT = (_vx0 + _vb[0], _vy0 + _vb[1], _vx0 + _vb[2], _vy0 + _vb[3]); print('victory card rect', VRECT, 'right edge in lower zone ok' if VRECT[2] <= 887 else 'CROSSES x887')
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
            a = 255 if it['alive'] else int(255 * max(0, 1 - (t - it.get('missed', t)) / (0.15 if it.get('buzz') else 0.4)))   # fork_h2: buzzer items fade in 0.15s
            if it.get('buzz') and VRECT and VRECT[0] - 20 < x0 + it['x'] < VRECT[2] + 20 and VRECT[1] - 40 < it['y'] < VRECT[3]: a = 0   # fork_h2: buzzer items behind the victory card are hidden under it
            if it['alive'] or a > 0:
                s2 = spr.copy()
                if a < 255: s2.putalpha(s2.getchannel('A').point(lambda p, a=a: p * a // 255))
                ixv = SLX.get((g, it['born']), it['x']) if it['kind'] == 'slime' else it['x']
                if ixv is None: continue
                py_ = int(it['y'] - s2.height / 2)
                if it['kind'] == 'slime' and it.get('missed', 0) != -99 and py_ + s2.height >= FLOOR:   # fork_h2: slimes land and splat on the floor, then fade
                    s2 = s2.resize((int(s2.width * 1.35), max(1, int(s2.height * 0.6))), Image.NEAREST); py_ = FLOOR - s2.height + 4
                elif py_ + s2.height > FLOOR: s2 = s2.crop((0, 0, s2.width, max(0, FLOOR - py_)))   # rc11: clip at the lane floor
                if s2.height > 0: img.alpha_composite(s2, (int(x0 + ixv - s2.width / 2), py_))
                if g == 'joy' and it['kind'] == 'acv' and it['alive'] and TAG[0] is None and t >= OFF + 1.4 and 760 < it['y'] < 900: TAG[0] = (t, it['born'])
                if TAG[0] and it['born'] == TAG[0][1] and it['kind'] == 'acv' and t - TAG[0][0] < 1.0:
                    TAGD.append((int(x0 + it['x']), int(it['y'] - s2.height / 2 - 4), int(255 * min(1, (t - TAG[0][0]) / 0.12, (1.0 - (t - TAG[0][0])) / 0.2))))
        for ex in EXTRA:
            if ex['g'] != g or fs_ not in ex['path'] and not (ex['land'] < fs_ < ex['land'] + 12): continue
            yy = ex['path'].get(fs_, FLOOR); s2 = GUMI[ex['kind']].copy()
            if fs_ > ex['land'] - 3:   # lands and fades like a missed gummy
                aa = max(0, 1 - (fs_ - ex['land'] + 3) / 12); s2.putalpha(s2.getchannel('A').point(lambda p, aa=aa: int(p * aa)))
            py_ = int(min(yy, FLOOR - s2.height / 2 + 6) - s2.height / 2)
            img.alpha_composite(s2, (int(x0 + ex['x'] - s2.width / 2), py_))
        # guide
        s = st[g]; x = x0 + s['x']
        if t >= T_END and g == WIN: pass
        elif t - s['stun'] < 0.9:
            fr = KO[g][ko_frame(t - s['stun'])]
            if s['face'] < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        elif t < T0 or IDLEM[g][min(fs_, len(FR) - 1)]: fr = IDL[g][int(t * 8) % len(IDL[g])]   # fork_h2: flicker-free idle mask (no short side-run/front-idle snaps)
        else: fr = (RUN if s['face'] > 0 else RUNL)[g][int(s['dist'] / 26) % 8]
        if not (t >= T_END and g == WIN):
            layer(img, lambda d: d.ellipse([x - 50, FLOOR - 12, x + 50, FLOOR + 10], fill=(0, 0, 0, 90)))
            if t - s['stun'] < 0.9:   # KO frames: feet / lowest pixel on the floor, kept inside the lane
                bb = fr.getbbox(); px = int(x - (bb[0] + bb[2]) / 2); py = FLOOR - bb[3]
                px = min(max(px, x0 + 6 - bb[0]), x0 + LW - 6 - bb[2]) if bb[2] - bb[0] < LW - 12 else px
            else: px, py = int(x - fr.width / 2), int(FLOOR - 78 * 3)
            lo_ = x0 + 4 if li > 0 else 0; hi_ = x0 + LW - 4 if li < 3 else W   # fork_h2: guides stay in their own lane (clipped at the pillars)
            fc = fr.crop((max(0, lo_ - px), 0, max(0, min(fr.width, hi_ - px)), fr.height))
            if fc.width > 0: img.alpha_composite(fc, (max(px, lo_), py))
            if t - s['stun'] >= 0.9 or t < T0: img.alpha_composite(BASKET, (int(x - BASKET.width / 2), int(FLOOR - 236 - BASKET.height // 2)))
            if t - s['stun'] < STUN_VIS:
                kx = min(max(x, x0 + 62), x0 + LW - 62) if li in (1, 2) else x
                def stars(d, x=kx):
                    for k in range(3):
                        a2 = t * 8 + k * 2.1; sx2, sy2 = x + 50 * math.cos(a2), FLOOR - (250 if t - s['stun'] < 0.2 else 150) + 16 * math.sin(a2)
                        d.polygon([(sx2, sy2 - 10), (sx2 + 4, sy2 - 3), (sx2 + 11, sy2), (sx2 + 4, sy2 + 3), (sx2, sy2 + 10), (sx2 - 4, sy2 + 3), (sx2 - 11, sy2), (sx2 - 4, sy2 - 3)], fill=(255, 230, 90, 255))
                layer(img, stars)
    # lane dividers (gold pillars)
    layer(img, lambda d: [d.rectangle([LX0 + li * LW - 4, 0, LX0 + li * LW + 4, H], fill=(200, 160, 60, 255)) for li in range(1, 4)])
    # pops
    for (te, g, kind, ix) in EV:
        u = t - te
        life = STUN_VIS if kind == 'slime' else 0.8
        nxt = [te2 for (te2, g2, k2, ix2) in EV if g2 == g and te < te2 <= t]
        if 0 <= u < life and t < T_END:   # fork_h2 review fix: every +1 clears on the buzzer frame
            lx = LX0 + G4.index(g) * LW
            a = int(255 * min(1, (life - u) / 0.2))
            if nxt: a = 0   # a newer pop in this lane replaces this one at once (no stacked +1s)
            lab, c = ('BOING!', (150, 240, 120)) if kind == 'slime' else (('+3', (255, 214, 60)) if kind == 'gold' else ('+1', COL[g]))
            if kind == 'slime': sz = 32; x0 = lx + LW / 2   # centred on its own lane, fits inside it
            else: sz = 44; x0 = min(max(lx + ix, lx + 62), lx + LW - 62)   # +1 kept off the pillars
            x0 = min(max(x0, 76 + len(lab) * sz / 2), 882 - len(lab) * sz / 2)   # inside the zone
            text_layer(img, [(x0, FLOOR - (430 if kind == 'slime' else 340) - u * 60, lab, sz, c, 6, a)])   # BOING! on its own row above the +1 row
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
        CX0, CY0, CX1, CY1 = VRECT[0] - 24, VRECT[1] - 20, VRECT[2] + 24, 1300   # fork_h2: the win pose stands on a card, scales in over 0.2s
        card = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(card)
        dc.rounded_rectangle([CX0, CY0, CX1, CY1], 18, fill=(22, 16, 34, 235), outline=COL[WIN] + (255,), width=6)
        dc.rectangle([CX0 + 6, 1262, CX1 - 6, CY1 - 6], fill=tuple(int(c_ * 0.45) for c_ in COL[WIN]) + (255,))
        card.alpha_composite(vf, (int(VICX - vf.width / 2), 1270 - vf.height))
        k_ = min(1.0, u / 0.2); e_ = 1 - (1 - k_) ** 3; sc_ = 0.6 + 0.4 * e_
        if sc_ < 0.999:
            cb = card.crop((CX0, CY0, CX1 + 1, CY1 + 1)); nw, nh = int(cb.width * sc_), int(cb.height * sc_)
            cb = cb.resize((nw, nh), Image.NEAREST); cb.putalpha(cb.getchannel('A').point(lambda p: int(p * e_)))
            card = Image.new('RGBA', (W, H), (0, 0, 0, 0)); card.alpha_composite(cb, (int((CX0 + CX1) / 2 - nw / 2), CY1 - nh))
        img.alpha_composite(card)
        text_layer(img, [(478, 762, NAME[WIN] + ' WINS!', 56, COL[WIN], 9, int(255 * min(1, u / 0.3)))])
        def conf(d2):
            rr = random.Random(f)
            for _ in range(40):
                cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 450) % H
                if HB - 30 < cy_ < HB + 200: continue   # fork_h2: no confetti over the score chips / timer
                d2.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([COL[WIN], (255, 214, 60), (255, 255, 255)]) + (230,))
        layer(img, conf)
        if abs(u) < 0.5 / FPS: ev.append((round(t - OFF, 3), 'victory'))
    img.alpha_composite(HOOK2 if t >= T_END else HOOK)
    w.write(img)
    if f in (0, 15, 40, 200, int((T_END - 3 - OFF) * FPS) + 4, NF - 1) or os.environ.get('ONLY'): img.convert('RGB').save(OUT + f'k_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); json.dump({'events': sorted(ev)}, open(OUT + 'ev_mix.json', 'w')); print('done', END, len(ev))
