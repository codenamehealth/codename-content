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
HOLD = 2.4; NF = FL + int(HOLD * FPS)
ZD = 1.0; PD = len(taus) / FPS + 0.25
print('frames', NF, 'escape frame', FE, 'landing frame', FL, 'slowmo', round(RS, 2), 'flight video s', round(len(taus) / FPS, 2), flush=True)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def cam_plan(f):
    if f < FE: return 1.0, 540.0, 960.0
    u = (f - FE) / FPS
    s = 1 + (SF - 1) * ease(u / ZD); e = ease(u / PD)
    out = (s, 540 + (CXF - 540) * e, 960 + (CYF - 960) * ease(u / ZD))
    if f >= FL:   # after the gulp: push in on the King Slime so the Hollow inside him reads on a phone
        e2 = ease(((f - FL) / FPS - 0.55) / 0.9)
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

for f in range(FL-8, FL+20): print(f, [round(v,3) for v in CAM[f]])
