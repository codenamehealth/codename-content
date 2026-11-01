import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7'); from common7 import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# rc8: motion from frame 0 (was frozen until 0.8s), speeds up gently from 4s, card at 7.8s held 1.2s while the gummy glides back to its frame-0 spot (seamless loop)
DUR = 9.0; N = int(DUR * FPS); T0, T1 = 0.0, 7.8
KW = 0.092
def tw(t): return t + KW * max(0.0, t - 4.0) ** 2 / 2      # warped time: speed x1 until 4s, x1.35 by 7.8s
sh = Image.open(SP + 'fork_a8/gen/shield/02.png').convert('RGBA'); sh = crop(sh); SS = 6
SH = up(sh, SS); SHX, SHY = 478 - SH.width // 2, 752    # rc8: centred on the lower safe column (x478, was 460); below the taller band + rule plate
# rc8: ONLY 0.1% CAN 36px blue-on-navy -> 52px white band line; DID YOU NAIL IT? band carries the comment ask
HOOK_A, HB = hook_layer2(['THINK YOU CAN', 'NAIL IT?'], accent=1, sub='ONLY 0.1% CAN')
HOOK_B, HBB = hook_layer2(['DID YOU', 'NAIL IT?'], accent=1, sub='Comment your time')
print('HB', HB, HBB)
# find recess centre (dark pixels inside the gold ring)
a = np.array(sh).astype(int); cy0, cx0 = sh.height // 2, sh.width // 2
dark = (a[..., 3] > 0) & (a[..., :3].sum(-1) < 220)
ys, xs = np.nonzero(dark[cy0 - 30:cy0 + 20, cx0 - 20:cx0 + 20]); RCX = SHX + (xs.mean() + cx0 - 20 + 0.5) * SS; RCY = SHY + (ys.mean() + cy0 - 30 + 0.5) * SS
print('recess', RCX, RCY)
GK = 5; G0 = gummy('cre', 1); G = up(G0, GK)
def gsc(s): return G0.resize((max(1, round(G0.width * GK * s)), max(1, round(G0.height * GK * s))), Image.NEAREST)
# dashed outline of the gummy silhouette at the target
m = np.array(G.getchannel('A')) > 0
edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
pad = 10; OL = Image.new('RGBA', (G.width + 2 * pad, G.height + 2 * pad), (0, 0, 0, 0)); od = ImageDraw.Draw(OL)
pts = np.argwhere(edge); ang = np.arctan2(pts[:, 0] - G.height / 2, pts[:, 1] - G.width / 2)
for (yy, xx), an in zip(pts, ang):
    if int((an + math.pi) / (2 * math.pi) * 36) % 2 == 0:
        od.rectangle([xx + pad - 3, yy + pad - 3, xx + pad + 3, yy + pad + 3], fill=(255, 255, 255, 235))
OLX, OLY = int(RCX - OL.width / 2), int(RCY - OL.height / 2)
# motion search: exactly one frame lines up (over the motion AND the end glide back to the start)
FR = np.arange(N) / FPS; MOV = FR < T1
TSW = np.array([tw(t) for t in FR[MOV]])
GU = (FR[~MOV] - T1) / (DUR - T1); GS = GU * GU * (3 - 2 * GU)
best = None; rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
for trial in range(12000):
    FMc = rng.randint(int(5.0 * FPS), int(6.8 * FPS)); TM = tw(FMc / FPS)
    f1, f2, f3 = rng.uniform(0.35, 0.75), rng.uniform(0.5, 1.05), rng.uniform(0.6, 1.3)
    A_, B_, C_ = rng.uniform(110, 170), rng.uniform(120, 200), rng.uniform(0.16, 0.26)
    p1, p2, p3 = [-2 * math.pi * fq * TM + rng.choice([0, math.pi]) for fq in (f1, f2, f3)]
    dx = A_ * np.sin(2 * np.pi * f1 * TSW + p1); dy = B_ * np.sin(2 * np.pi * f2 * TSW + p2); ds = C_ * np.sin(2 * np.pi * f3 * TSW + p3)
    # glide: from the pose at T1 back to the pose at t=0
    e1 = np.array([A_ * math.sin(2 * math.pi * f1 * tw(T1) + p1), B_ * math.sin(2 * math.pi * f2 * tw(T1) + p2), C_ * math.sin(2 * math.pi * f3 * tw(T1) + p3)])
    e0 = np.array([dx[0], dy[0], ds[0]])
    g = e1[None, :] + (e0 - e1)[None, :] * GS[:, None]
    DX = np.concatenate([dx, g[:, 0]]); DY = np.concatenate([dy, g[:, 1]]); DS = np.concatenate([ds, g[:, 2]])
    e = np.maximum(np.maximum(np.abs(DX), np.abs(DY)), np.abs(DS) * 140)
    if e[FMc] > 1.0 or e[0] < 100: continue
    e2 = np.delete(e, [FMc]); sec = e2.min()
    if best is None or sec > best[0]: best = (sec, FMc, f1, f2, f3, A_, B_, C_, p1, p2, p3, e)
sec, FM, f1, f2, f3, A_, B_, C_, p1, p2, p3, EALL = best
print('match frame', FM, round(FM / FPS, 3), 'next best err', round(sec, 1), 'frame0 err', round(EALL[0], 1), 'fits(<=1):', list(np.nonzero(EALL <= 1.0)[0]),
      'near(<45):', [(int(i), round(float(EALL[i]), 1)) for i in np.nonzero(EALL < 45)[0]])
def _p(tt): return (A_ * math.sin(2 * math.pi * f1 * tt + p1), B_ * math.sin(2 * math.pi * f2 * tt + p2), C_ * math.sin(2 * math.pi * f3 * tt + p3))
def pose(t):
    if t < T1: dx, dy, ds = _p(tw(t))
    else:
        u = (t - T1) / (DUR - T1); u = u * u * (3 - 2 * u); a, b = _p(tw(T1)), _p(0.0)
        dx, dy, ds = [a[i] + (b[i] - a[i]) * u for i in range(3)]
    return (RCX + dx, RCY + dy, 1 + ds)
# background: Liza's castle (dim, blurred) + Cleo
BG = bg_frames('bg_castle.gif', (1920, 1080), step=2, bright=0.5, blur=2)
BG = [b.crop((600, 0, 600 + 608, 1080)).resize((W, H), Image.NEAREST) for b in BG]
CLEO = idle('cleo', 5)
w = Writer('noaudio.mp4'); ev = []
rr = random.Random(7); SPARK = [(rr.uniform(0, W), rr.uniform(400, 1700), rr.uniform(0, 6.3)) for _ in range(40)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 4, y + 4], fill=(255, 230, 160, int(120 + 120 * math.sin(t * 3 + p)))) for x, y, p in SPARK])
    # glow behind shield
    layer(img, lambda d: [d.ellipse([460 - r, RCY - r * 1.2, 460 + r, RCY + r * 1.2], fill=(120, 170, 255, 18)) for r in (420, 360, 300)])
    img.alpha_composite(SH, (SHX, SHY))
    img.alpha_composite(OL, (OLX, OLY))
    gx, gy, s = pose(t); g = gsc(s)
    layer(img, lambda d: d.ellipse([gx - 80 * s, gy - 80 * s, gx + 80 * s, gy + 80 * s], fill=(255, 140, 170, 40)))
    img.alpha_composite(g, (int(round(gx - g.width / 2)), int(round(gy - g.height / 2))))
    c = CLEO[int(t * 8) % len(CLEO)]; img.alpha_composite(c, (887 - 350, 1500 - 390))   # Cleo 5x, bbox x637-887, feet y1500
    # rc8: the rule as one big gold line + the comment ask, on a dark plate from frame 0 (was 34px two-line white text, no plate)
    if t < T1:
        layer(img, lambda d: d.rounded_rectangle([76, HB + 10, 1018, HB + 150], 18, fill=(14, 10, 24, 225), outline=(255, 214, 60, 255), width=4))
        text_layer(img, [(547, HB + 30, 'PAUSE WHEN IT FITS', 50, (255, 214, 60), 8, 255), (547, HB + 96, 'COMMENT YOUR TIME', 44, (255, 255, 255), 7, 255)])
    img.alpha_composite(HOOK_B if t >= T1 else HOOK_A)
    w.write(img)
    if f in (FM - 1, FM, FM + 1): img.convert('RGB').crop((160, 700, 800, 1460)).save(f'm{f - FM:+d}.png')
    if f in (0, 120, N - 1): img.convert('RGB').save(f'k75_{f}.png')
w.close()
ev.append((0.0, 'whoosh_8bit')); ev.append((T1, 'ding_8bit'))   # rc8: no 1s tick metronome
json.dump({'events': ev, 'fm': FM}, open('events.json', 'w')); print('done')
