import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7'); from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 9.0; N = int(DUR * FPS); T0, T1 = 0.8, 8.2
sh = Image.open(SP + 'fork_a8/gen/shield/02.png').convert('RGBA'); sh = crop(sh); SS = 6
SH = up(sh, SS); SHX, SHY = 460 - SH.width // 2, 640    # was centred x540, y560 (shield unchanged 6x)
HOOK_A, HB = hook_layer(['THINK YOU CAN', 'NAIL IT?'], accent=1, sub='ONLY 0.1% CAN', sub_color=(120, 190, 255))
HOOK_B, _ = hook_layer(['DID YOU', 'NAIL IT?'], accent=1, sub='ONLY 0.1% CAN', sub_color=(120, 190, 255))
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
# motion search: exactly one frame lines up
ts = np.arange(int(T0 * FPS), int(T1 * FPS)) / FPS
best = None; rng = random.Random(3)
for trial in range(4000):
    TM = round(rng.uniform(5.0, 6.8) * FPS) / FPS
    f1, f2, f3 = rng.uniform(0.35, 0.75), rng.uniform(0.5, 1.05), rng.uniform(0.6, 1.3)
    A_, B_, C_ = rng.uniform(110, 170), rng.uniform(120, 200), rng.uniform(0.16, 0.26)
    p1, p2, p3 = [-2 * math.pi * fq * TM + rng.choice([0, math.pi]) for fq in (f1, f2, f3)]
    dx = A_ * np.sin(2 * np.pi * f1 * ts + p1); dy = B_ * np.sin(2 * np.pi * f2 * ts + p2); ds = C_ * np.sin(2 * np.pi * f3 * ts + p3)
    e = np.maximum(np.maximum(np.abs(dx), np.abs(dy)), np.abs(ds) * 140)
    i = int(np.argmin(e))
    if e[i] > 1.0: continue
    e2 = np.delete(e, [i]); sec = e2.min()
    if best is None or sec > best[0]: best = (sec, i, f1, f2, f3, A_, B_, C_, p1, p2, p3)
sec, IM, f1, f2, f3, A_, B_, C_, p1, p2, p3 = best
FM = int(T0 * FPS) + IM; print('match frame', FM, FM / FPS, 'next best err', round(sec, 1))
def pose(t):
    if t < T0: tt = T0
    elif t > T1: tt = T1
    else: tt = t
    return (RCX + A_ * math.sin(2 * math.pi * f1 * tt + p1), RCY + B_ * math.sin(2 * math.pi * f2 * tt + p2), 1 + C_ * math.sin(2 * math.pi * f3 * tt + p3))
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
    items = [(W / 2, HB + 12, 'Pause when the gummy', 34, (255, 255, 255), 6, 255), (W / 2, HB + 58, 'fits the shield', 34, (255, 255, 255), 6, 255)]
    if t <= 8.2: text_layer(img, items)      # end card: the bigger DID YOU / NAIL IT? hook takes this space
    img.alpha_composite(HOOK_B if t > 8.2 else HOOK_A)
    w.write(img)
    if f in (FM - 1, FM, FM + 1): img.convert('RGB').crop((160, 580, 760, 1380)).save(f'm{f - FM:+d}.png')
    if f % 30 == 0: ev.append((round(t, 3), 'tick_8bit')) if T0 < t < T1 else None
w.close()
ev.append((round(T0, 3), 'whoosh_8bit')); ev.append((8.2, 'ding_8bit'))
json.dump({'events': ev, 'fm': FM}, open('events.json', 'w')); print('done')
