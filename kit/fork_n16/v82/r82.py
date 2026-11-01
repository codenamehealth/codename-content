import sys, os, math, json
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); import hook as HK
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import numpy as np
import sim82 as SM
# #82 Oct 29 notes2 (fork_n16): rebuilt on sim82 (fixed 1/720s step, gravity, exact AABB brick colliders, elastic
# reflections, every bounce = exactly one new brick), then the twist: he escapes, the camera follows and pulls back,
# and the exit drops him straight into a friendly King Slime's open mouth (pixellab/king/king2_*, as used in #68).
SEED = int(sys.argv[1]); RES = SM.sim(SEED); assert RES['fail'] is None, RES['fail']
KP = SM.place_king(RES); assert KP, 'no king placement'
_, TL, MX, MY, KX, KB = KP; TL += SM.DT           # trajectory() index i is time (i+1)*DT after the escape step
ESC = RES['esc']; TRJ = SM.trajectory(RES)
K = SM.K; BGS = 3.0; NV = 805; OY = KB - NV * BGS   # bg (sun_hd, world-locked at 3x): king's base on the floor row NV
SP2 = 0.8; SF = 0.6; CYF = OY + 1620; CXF = KX - 100           # final camera: whole bg height in view, king at screen x ~600
print('seed', SEED, 'esc', round(ESC, 2), 'events', len(RES['events']), 'king', round(KX), round(KB), 'OY', round(OY), 'TL', round(TL, 3), flush=True)
HOOK, HB = HK.hook_fade(['CAN THE HOLLOW', 'ESCAPE?'], accent=1)
HOOK2, _ = HK.hook_fade(['...OR DID HE?'], accent=0)
BR = up(crop(Image.open(B8 + 'brick/03.png').convert('RGBA')), 1.25); assert BR.size == (SM.BW, SM.BHh), BR.size
BR2 = ImageEnhance.Brightness(BR).enhance(1.35)
BRW = Image.blend(BR, Image.new('RGBA', BR.size, (255, 255, 255, 255)), 0.85); BRW.putalpha(BR.getchannel('A'))
NAT = []
_im = Image.open(A + 'sun_hd.gif')
for i in range(0, _im.n_frames, 2):
    _im.seek(i); f = ImageEnhance.Brightness(_im.convert('RGB')).enhance(0.5).convert('RGBA')
    f.alpha_composite(Image.new('RGBA', f.size, (10, 6, 20, 70))); NAT.append(f.convert('RGB'))
HOL = idle('hollow', 1); HOLS = [up(f.crop((20, 10, 76, 60)), 2) for f in HOL]
GUM = gummy('mush', 3)
RB = SM.RB
def bubble(f, alpha=1.0, tint=None):
    b = Image.new('RGBA', (2 * RB + 8, 2 * RB + 8), (0, 0, 0, 0))
    L = Image.new('RGBA', b.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse([4, 4, 2 * RB + 3, 2 * RB + 3], fill=(170, 220, 255, 60), outline=(220, 245, 255, 230), width=4)
    b.alpha_composite(L)
    s = HOLS[f % len(HOLS)]; b.alpha_composite(s, (b.width // 2 - s.width // 2, b.height // 2 - s.height // 2 + 10))
    d = ImageDraw.Draw(b); d.ellipse([22, 20, 42, 34], fill=(255, 255, 255, 200))
    if tint is not None:
        r, g, bl, a = b.split(); col = Image.new('RGBA', b.size, tint + (255,)); col.putalpha(a)
        b = Image.blend(b, col, 0.22)
    if alpha < 1:
        a = b.getchannel('A').point(lambda v: int(v * alpha)); b.putalpha(a)
    return b
KS = lambda d: [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(PL + 'king/' + d + '/*.png'))]
KLAND = KS('king2_land'); KIDLE = KS('king2_idle')
def kpos(spr): return (int(round(KX - 80 * K)), int(round(KB - 156 * K)))
MCX, MCY = KX + (SM.MOUTH[0] - 80) * K, KB - (156 - SM.MOUTH[1]) * K; MRX, MRY = 18 * K, 15 * K
assert abs(MCX - MX) < 1 and abs(MCY - MY) < 1
# ---------- timeline ----------
FE = int(math.ceil(ESC * FPS))          # first frame after the escape
FLIGHT_V = 1.5                          # target on-screen flight length (s)
RS = min(1.0, max(0.42, TL / FLIGHT_V)); RAMP = 0.3
taus = []; tau = (FE / FPS) - ESC; u = 0.0
while tau < TL:
    taus.append(tau); u += 1 / FPS
    r = 1 - (1 - RS) * min(1.0, u / RAMP); tau += r / FPS
FL = FE + len(taus)                     # landing frame (ball centre reaches the mouth centre)
GULP = [(0.0, 9), (0.067, 10), (0.133, 11), (0.2, 12), (0.267, 7), (0.333, 6), (0.533, 7), (0.6, None)]
HOLD = float(os.environ.get('HOLD', '1.45')); NF = FL + int(HOLD * FPS)
ZD = 1.0; PD = len(taus) / FPS + 0.25
print('frames', NF, 'escape frame', FE, 'landing frame', FL, 'slowmo', round(RS, 2), 'flight video s', round(len(taus) / FPS, 2), flush=True)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def cam_plan(f):
    if f < FE: return 1.0, 540.0, 960.0
    u = (f - FE) / FPS
    s = 1 + (SF - 1) * ease(u / ZD); e = ease(u / PD)
    out = (s, 540 + (CXF - 540) * e, 960 + (CYF - 960) * ease(u / ZD))
    if f >= FL:   # after the gulp: push in on the King Slime so the Hollow inside him reads on a phone
        e2 = ease(((f - FL) / FPS - 0.05) / 1.15)
        out = (out[0] + (SP2 - out[0]) * e2, out[1] + (KX - out[1]) * e2, out[2] + (KB - 520 - out[2]) * e2)
    return out
def traj_at(tau):
    i = tau / SM.DT - 1; i0 = int(math.floor(i)); fr = i - i0
    if i0 < 0: x, y, vx, vy = RES['esc_state']; return x + vx * tau, y + vy * tau, vx, vy
    a = TRJ[min(i0, len(TRJ) - 1)]; b = TRJ[min(i0 + 1, len(TRJ) - 1)]
    return tuple(a[k] + (b[k] - a[k]) * fr for k in (1, 2, 3, 4))
def ball_play(f):
    if f == 0: return RES['init']
    return RES['frames'][min(f - 1, len(RES['frames']) - 1)]
CAM = [list(cam_plan(f)) for f in range(NF)]
for f in range(FE, FL):
    s_, cx_, cy_ = CAM[f]; bx_, by_, _, _ = traj_at(taus[f - FE])
    cx_ = min(max(cx_, bx_ - (920 - 540) / s_), bx_ + (540 - 160) / s_)
    cy_ = min(cy_, by_ + (960 - (HB + 150)) / s_)
    CAM[f][1], CAM[f][2] = cx_, cy_
for f in range(FL, NF): CAM[f] = list(cam_plan(f))
for k in (1, 2):
    sm = [c[:] for c in CAM]
    for f in range(FE, NF):
        for j in (1, 2):
            win = [CAM[g][j] for g in range(max(FE, f - 6), min(NF, f + 7))]
            sm[f][j] = sum(win) / len(win)
    CAM = sm
for f in range(NF):
    s_ = CAM[f][0]; CAM[f][2] = min(max(CAM[f][2], OY + 960 / s_ + 3), OY + 1080 * BGS - 960 / s_ - 3)
def cam(f): return tuple(CAM[f])
EVT = sorted(RES['events'], key=lambda e: e['t'])
BRK = [b for b in RES['bricks'] if b[1] > 0]
GAP_A = SM.GA; gx, gy = SM.CX + (SM.R0 + 20) * math.cos(GAP_A), SM.CY + (SM.R0 + 20) * math.sin(GAP_A)
EXIT_XY = (gx + 70, gy - 120)
# ---------- King Slime: hops in from the right (two hops, squash on each landing), rises mouth-open for the catch ----------
STL = ESC + TL                     # sim time the bubble reaches the mouth
HOPA, HOPH, HOPD = 0.42, 110.0, 380.0
def kplace(spr, dx, dy):           # anchor = base centre (KX, KB) whatever the sprite scale
    return (int(round(KX + dx - spr.width / 2)), int(round(KB + dy - spr.height * 156 / 160)))
def king_hop(st):
    u = st - (STL - 1.30)          # 0..1.30: hop1 air, land squash, hop2 air, land squash, rise to mouth-open
    seg = [('air', 0.42, 2), ('gnd', 0.12, 1), ('air', 0.42, 1), ('gnd', 0.10, 0), ('rise', 0.24, 0)]
    t0 = 0.0
    if u < 0: return KLAND[3], 2 * HOPD, 0.0
    for kind, d, n in seg:
        if u < t0 + d or kind == 'rise':
            q = min(1.0, (u - t0) / d)
            if kind == 'air':
                x = HOPD * (n - q); y = -4 * HOPH * q * (1 - q)           # parabola: constant gravity
                fi = 8 if q < 0.45 else (9 if q < 0.6 else (10 if q < 0.75 else (11 if q < 0.88 else 12)))
                return KLAND[fi], x, y
            if kind == 'gnd': return KLAND[[2, 3, 2, 7][min(3, int(q * 4))]], HOPD * n, 0.0
            return KLAND[[1, 7, 8, 9][min(3, int(q * 4))] if q < 0.75 else 9], 0.0, 0.0
        t0 += d
def kscale(spr, sx, sy):
    return spr.resize((max(1, int(round(spr.width * sx))), max(1, int(round(spr.height * sy)))), Image.NEAREST)
_b12, _b0 = KLAND[12].getbbox(), KLAND[0].getbbox()
SY12 = (_b0[3] - _b0[1]) / (_b12[3] - _b12[1]); SX12 = (_b0[2] - _b0[0]) / (_b12[2] - _b12[0])
def king_gulp(w):
    if w < 0.2: return KLAND[[9, 10, 11, 12][min(3, int(w / 0.05))]], (1, 1)
    if w < 0.5:      # settle: the tall gulp shape eases down into the dome over 0.3s (no frame pop)
        e = ease((w - 0.2) / 0.3); sx, sy = 1 + (SX12 - 1) * e, 1 + (SY12 - 1) * e
        return kscale(KLAND[12], sx, sy), (sx, sy)
    if w < 0.9:      # gulp bounce on the dome: squash then a small rebound, damped
        q = (w - 0.5) / 0.4; sy = 1 - 0.09 * math.sin(math.pi * 2 * q) * (1 - q); sx = 1 / math.sqrt(sy)
        return kscale(KLAND[0], sx, sy), (sx, sy)
    return KIDLE[int((w - 0.9) * 8) % len(KIDLE)], (1, 1)
TS2V = lambda ts: ts                # play phase runs in real time (video t == sim t before the escape)
# ---------- render ----------
wr = Writer('v82_noaudio.mp4' if not os.environ.get('QUICK') else 'quick_tmp.mp4'); events = [(0.0, 'go_8bit')]; trail = []; log = {'bounce_vs_brick': [], 'ball_screen': []}
KEYF = set(int(v) for v in os.environ.get('KEYS', '').split(',') if v)
for e in EVT: events.append((round(e['t'], 3), 'brick_8bit'))
for g in RES['gums']:
    if g['got']: events.append((round(g['got'], 3), 'powerup_8bit'))
events += [(round(FE / FPS, 3), 'victory'), (round(FL / FPS, 3), 'squish'), (round(FL / FPS + 0.5, 3), 'boing')]
for _hs in (0.42 + 0.0, 0.42 + 0.12 + 0.42):     # king hop landings (sim time -> video time inside the slow-mo flight)
    _st = STL - 1.30 + _hs
    _fs = [FE + i for i, tau in enumerate(taus) if ESC + tau >= _st]
    if _fs: events.append((round(_fs[0] / FPS, 3), 'stomp_8bit'))
QUICK = os.environ.get('QUICK')
for f in range(NF):
    vt = f / FPS
    if QUICK and f not in KEYF: continue
    s, cx, cy = cam(f)
    # simulation state for this frame
    if f < FE: st = vt; bx, by, bvx, bvy = ball_play(f); phase = 'play'
    elif f < FL: tau = taus[f - FE]; st = ESC + tau; bx, by, bvx, bvy = traj_at(tau); phase = 'flight'
    else: st = ESC + TL; w = (f - FL) / FPS; phase = 'king'
    vw, vh = W / s, H / s; x0, y0 = cx - vw / 2, cy - vh / 2
    ox, oy = math.floor(x0), math.floor(y0); cw, ch = int(math.ceil(vw)) + 2, int(math.ceil(vh)) + 2
    # bg region (native coords) for the canvas
    nat = NAT[int(vt * 6) % len(NAT)]
    u0 = (ox - 540) / BGS + 960; v0 = (oy - OY) / BGS
    cvs = nat.resize((cw, ch), Image.NEAREST, box=(u0, v0, u0 + cw / BGS, v0 + ch / BGS)).convert('RGBA')
    def P(X, Y): return (X - ox, Y - oy)
    CXp, CYp = P(SM.CX, SM.CY); R0 = SM.R0
    layer(cvs, lambda d: (d.ellipse([CXp - R0 - 40, CYp - R0 - 40, CXp + R0 + 40, CYp + R0 + 40], fill=(40, 28, 20, 150)),
                          d.ellipse([CXp - R0 + 10, CYp - R0 + 10, CXp + R0 - 10, CYp + R0 - 10], fill=(70, 50, 30, 120)),
                          d.ellipse([CXp - 200, CYp - 200, CXp + 200, CYp + 200], fill=(255, 220, 140, 22))))
    pulse = 0.5 + 0.5 * math.sin(vt * 5); gxp, gyp = P(gx, gy)
    layer(cvs, lambda d: d.ellipse([gxp - 80, gyp - 80, gxp + 80, gyp + 80], fill=(120, 255, 160, int(40 + 50 * pulse))))
    # bricks: base ring + every spawned brick (exact collider rects)
    for (b, k, rect, ts) in RES['bricks']:
        if k > 0 and ts > st: continue
        if k > 0 and 0 <= vt - TS2V(ts) < 2 / FPS - 1e-6:   # 2 video frames of white flash the moment it appears
            img = BRW; layer(cvs, lambda d: d.ellipse([P(rect[0], rect[1])[0] - 22, P(rect[0], rect[1])[1] - 22, P(rect[2], rect[3])[0] + 22, P(rect[2], rect[3])[1] + 22], fill=(255, 255, 255, 110), outline=(255, 255, 255, 220), width=5))
        else: img = BR2 if (k > 0 and st - ts < 0.2) else BR
        cvs.alpha_composite(img, P(rect[0], rect[1]))
    ex, ey = P(*EXIT_XY); text_layer(cvs, [(ex, ey, 'EXIT', 44, (120, 255, 150), 7, 255)])
    for g in RES['gums']:
        if g['t'] <= st and (g['got'] is None or st < g['got']) and phase == 'play':
            bob = 6 * math.sin(vt * 4 + g['x']); gxp_, gyp_ = P(g['x'], g['y'] + bob)
            layer(cvs, lambda d: d.ellipse([gxp_ - 40, gyp_ - 40, gxp_ + 40, gyp_ + 40], fill=(255, 230, 150, 70)))
            cvs.alpha_composite(GUM, (int(gxp_ - GUM.width / 2), int(gyp_ - GUM.height / 2)))
    # King Slime (off screen until the pull-back)
    if phase != 'play':
        if phase == 'flight': kspr, kdx, kdy = king_hop(st); KSC = (1.0, 1.0)
        else: kspr, KSC = king_gulp(w); kdx = kdy = 0.0
        kx0, ky0 = kplace(kspr, kdx, kdy); cvs.alpha_composite(kspr, (kx0 - ox, ky0 - oy))
    # ball
    if phase in ('play', 'flight'):
        trail = (trail + [(bx, by)])[-10:]
        layer(cvs, lambda d: [d.ellipse([P(tx, ty)[0] - 4 - i * 2, P(tx, ty)[1] - 4 - i * 2, P(tx, ty)[0] + 4 + i * 2, P(tx, ty)[1] + 4 + i * 2], fill=(255, 230, 140, 30 + i * 18)) for i, (tx, ty) in enumerate(trail[:-1])])
        gl = [g['got'] for g in RES['gums'] if g['got'] is not None and g['got'] <= st]; tg = max(gl) if gl else -9
        if st - tg < 1.6 and phase == 'play':
            n_ = math.hypot(bvx, bvy) or 1; ux, uy = bvx / n_, bvy / n_; bxp, byp = P(bx, by)
            layer(cvs, lambda d: [d.line([bxp - ux * (RB + 10 + 26 * q) - uy * o_, byp - uy * (RB + 10 + 26 * q) + ux * o_, bxp - ux * (RB + 90 + 26 * q) - uy * o_, byp - uy * (RB + 90 + 26 * q) + ux * o_], fill=(255, 255, 255, 210), width=6) for q, o_ in ((0, -40), (1, 0), (0, 40), (2, -20), (2, 22))])
        bb = bubble(int(vt * 8)); bxp, byp = P(bx, by); cvs.alpha_composite(bb, (int(round(bxp - bb.width / 2)), int(round(byp - bb.height / 2))))
    else:
        if w < 0.2:   # swallowed: keeps moving into the mouth, shrinks with depth, clipped to the mouth opening
            _, _, lvx, lvy = traj_at(TL); n_ = math.hypot(lvx, lvy); q = w / 0.2
            dxw = lvx / n_ * 40 * q; dyw = lvy / n_ * 40 * q
            sc = 1 - 0.45 * q; bb = bubble(int(vt * 8)); bb = bb.resize((max(1, int(bb.width * sc)), max(1, int(bb.height * sc))), Image.NEAREST)
            M = Image.new('L', cvs.size, 0); mx_, my_ = P(MCX, MCY); ImageDraw.Draw(M).ellipse([mx_ - MRX, my_ - MRY, mx_ + MRX, my_ + MRY], fill=255)
            Lb = Image.new('RGBA', cvs.size, (0, 0, 0, 0)); bxp, byp = P(MX + dxw, MY + dyw)
            Lb.alpha_composite(bb, (int(round(bxp - bb.width / 2)), int(round(byp - bb.height / 2))))
            Lb.putalpha(Image.fromarray(np.minimum(np.asarray(Lb.getchannel('A')), np.asarray(M))))
            cvs.alpha_composite(Lb)
        elif w >= 0.333:   # inside the King Slime, seen through the jelly
            spr = kspr; bbox = spr.getbbox(); kx0, ky0 = kplace(spr, 0, 0)
            icx = kx0 + (bbox[0] + bbox[2]) / 2; icy = ky0 + bbox[1] + (bbox[3] - bbox[1]) * 0.77 + 4 * math.sin(vt * 3)
            bb = bubble(int(vt * 8), alpha=0.9, tint=(60, 190, 60)); bxp, byp = P(icx, icy)
            cvs.alpha_composite(bb, (int(round(bxp - bb.width / 2)), int(round(byp - bb.height / 2))))
    # camera
    if s == 1.0 and ox == 0 and oy == 0: img = cvs.crop((0, 0, W, H))
    else: img = cvs.resize((W, H), Image.LANCZOS, box=(x0 - ox, y0 - oy, x0 - ox + vw, y0 - oy + vh))
    if phase in ('play', 'flight'):
        sx, sy = (bx - x0) * s, (by - y0) * s; log['ball_screen'].append((f, round(sx), round(sy), round(s, 3)))
    # screen overlays
    nb = sum(1 for e in EVT if e['t'] <= st)
    ca = 255 if f < FE else 0
    if ca > 0: text_layer(img, [(540, HB + 50, f'BOUNCES: {nb}', 52, (255, 255, 255), 8, ca)])
    if phase == 'play':
        gl = [g['got'] for g in RES['gums'] if g['got'] is not None and g['got'] <= st]; tg = max(gl) if gl else -9
        if 0 <= st - tg < 0.8:
            sx_ = min(max(bx, 70 + 150), 887 - 150); sy_ = max(HB + 150, by - RB - 100)
            text_layer(img, [(sx_, sy_, 'SPEED!', 56, (255, 170, 50), 9, 255)])
        if vt < 0.35: text_layer(img, [(SM.CX - 40, SM.CY - SM.R0 - 75, 'GO!', 88, (255, 214, 60), 10, 255)])
    if FE <= f and (phase == 'flight' or w < 0.333):
        a = min(1.0, (f - FE) / FPS / 0.12)
        text_layer(img, [(540, HB + 40, 'HE ESCAPED!', 64, (120, 255, 150), 9, int(255 * a))])
    img.alpha_composite(HOOK if (phase != 'king' or w < 0.333) else HOOK2)
    wr.write(img)
    if f in KEYF: img.convert('RGB').save(f'k82_{f}.png')
wr.close()
# rule log: every bounce event -> exactly one new brick, and when it appeared
for e in EVT: log['bounce_vs_brick'].append((round(e['t'], 3), e['b'], e['k'], None if e['spawn_t'] is None else round(e['spawn_t'], 3)))
miss = [e for e in EVT if e['spawn_t'] is None]
delays = [e['spawn_t'] - e['t'] for e in EVT if e['spawn_t'] is not None]
print('bounces', len(EVT), 'bricks spawned', len(BRK), 'missing', len(miss), 'max spawn delay frames', round(max(delays) * FPS, 2), 'reflections', RES['refl'], 'post-escape contacts', RES['post_contacts'])
off = [b for b in log['ball_screen'] if not (40 <= b[1] <= 1040 and 0 <= b[2] <= 1920)]
print('ball off-screen frames', off[:10])
json.dump({'events': sorted(events), 'log': log, 'seed': SEED, 'nf': NF, 'FE': FE, 'FL': FL}, open('v82_ev.json', 'w'))
print('done', NF)
