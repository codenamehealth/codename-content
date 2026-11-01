# rc6 recut of #42 (approved by Bennett): universal + legibility fixes only. Source: fork_sz38/r42_sz.py
import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP0 + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_fade
# hfg4: soft fade, no box, no comment sub; the end question replaces the hook text in the same fade during the hold
HOOK, HB = hook_fade(['PAUSE WHEN BOTH', 'FIT PERFECTLY'], accent=1, color=(255, 214, 60), size=64)
HOOK_END, _ = hook_fade(['WHICH LEVEL', 'DID YOU BEAT?'], accent=1, color=(255, 214, 60), size=64)
BG = bg_frames('hub.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=float(os.environ.get('BRI', '0.78')), blur=float(os.environ.get('BLUR', '0')))   # was 0.6 + blur 5 (read as a backdrop)
jars = Image.open(A + 'jars.png').convert('RGBA')
import numpy as np
a = np.array(jars); bgc = a[2, 2, :3]; m = (np.abs(a[..., :3].astype(int) - bgc.astype(int)).sum(-1) < 12); a[m, 3] = 0
POT = crop(Image.fromarray(a).crop((0, 0, 200, 200))); POT = up(POT, 2.0)
GUM = up(acv_gummy_strong(), 7)          # Syeda's ACV gummy + gummy shine (same silhouette, so the outline still matches)
def sil(im):
    s = Image.new('RGBA', im.size, (18, 12, 30, 235)); s.putalpha(im.getchannel('A').point(lambda p: 235 if p > 0 else 0)); return s
SPOT, SGUM = sil(POT), sil(GUM)
print('POT', POT.size, 'GUM', GUM.size)
P0 = (312, 836); G0 = (762, 836)
LEVELS = [('NOOB', (120, 230, 110), 1.0), ('PRO', (90, 160, 255), 1.6), ('HACKER', (255, 90, 90), 2.4), ('GOD', (255, 214, 60), 3.4)]
LS = [0.0, 3.0, 6.0, 9.0]; LEND = 12.2          # level starts (was 4s each); GOD payoff at 9.0s
HOLD = 1.3; BACK = 0.3                           # end question hold, then ease back to the frame-0 pose (loop)
rnd = random.Random(int(os.environ.get('SEED', '3')))
def lev(t): return max(i for i in range(4) if t >= LS[i])
ends = LS[1:] + [LEND]
TSTAR = [round(rnd.uniform(LS[i] + 0.9, ends[i] - 0.6) * FPS) / FPS for i in range(4)]
def pose(t):
    i = lev(t); w = LEVELS[i][2]; s = t - TSTAR[i]
    pdx = 105 * math.sin(2.3 * w * s); pdy = 110 * math.sin(3.7 * w * s); pa = 24 * math.sin(1.7 * w * s)
    gdx = 120 * math.sin(1.9 * w * s); gdy = 60 * (1 - math.cos(1.9 * w * s)); ga = 20 * math.sin(1.9 * w * s)
    return i, (pdx, pdy, pa), (gdx, gdy, ga)
def miss(p, g): return max(abs(p[0]) + abs(p[1]) + 4 * abs(p[2]), abs(g[0]) + abs(g[1]) + 4 * abs(g[2]))
TE = LEND + HOLD + BACK; NF = int(round(TE * FPS))
FZ = int(round(LEND * FPS)) - 1                  # last live frame (pose frozen during the hold)
def full_pose(f):
    t = f / FPS
    if f <= FZ: return pose(t)
    i, p, g = pose(FZ / FPS)
    tb = t - (LEND + HOLD)
    if tb <= 0: return i, p, g
    k = min(1.0, tb / BACK + 1 / (BACK * FPS)); k = k * k * (3 - 2 * k)
    _, p0, g0 = pose(0.0)
    return i, tuple(p[j] + (p0[j] - p[j]) * k for j in range(3)), tuple(g[j] + (g0[j] - g[j]) * k for j in range(3))
# one-frame check: exactly one both-fit frame per level, never at the hold/loop
M = [miss(*full_pose(f)[1:]) for f in range(NF)]
fit = [f for f in range(NF) if M[f] < 1.0]
print('both-fit frames', fit, 'TSTAR frames', [int(round(x * FPS)) for x in TSTAR])
for i in range(4):
    lo, hi = int(LS[i] * FPS), (int(ends[i] * FPS) if i < 3 else NF)
    near = sorted(M[f] for f in range(lo, hi) if f not in fit)[:2]
    print('level', i, 'nearest misses', [round(x, 1) for x in near])
assert len(fit) == 4 and all(lev(f / FPS) == k for k, f in enumerate(fit)), fit
assert min(M[f] for f in range(NF) if f not in fit) >= 12, 'near-fit too close'
# bounds (safe zone) for the moving objects
for f in range(0, NF, 2):
    _, p, g = full_pose(f)
    for (c, d, spr) in ((P0, p, POT), (G0, g, GUM)):
        r = spr.height / 2; rw = spr.width / 2
        assert c[1] + d[1] - r >= HB + 4 and c[1] + d[1] + r < 1140 and c[0] + d[0] - rw > 70 and c[0] + d[0] + rw < 1025, (f, c, d)
if os.environ.get('DRY'): sys.exit(0)
JOY = idle('joy', 5)                             # 4x -> 5x (~315px)
def place(img, spr, c, d, ang):
    r = spr.rotate(ang, resample=Image.NEAREST, expand=True)
    img.alpha_composite(r, (int(c[0] + d[0] - r.width / 2), int(c[1] + d[1] - r.height / 2)))
wr = Writer('v42_noaudio.mp4'); ev = []
TX = 600                                         # level text centre (clear of Joy on the left and the x887 notch)
for f in range(NF):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    i, p, g = full_pose(f)
    if f > FZ and t >= LEND + HOLD: i = 0         # loop-back: tag returns to NOOB with the pose
    def ped(d):
        for cx, cy in (P0, G0):
            d.ellipse([cx - 170, cy + 150, cx + 170, cy + 210], fill=(0, 0, 0, 90))
    layer(img, ped)
    img.alpha_composite(SPOT, (P0[0] - SPOT.width // 2, P0[1] - SPOT.height // 2))
    img.alpha_composite(SGUM, (G0[0] - SGUM.width // 2, G0[1] - SGUM.height // 2))
    place(img, POT, P0, p[:2], p[2]); place(img, GUM, G0, g[:2], g[2])
    # 'ACV GUMMY' tag cut (hfg4, less text)
    if False:
        aa = int(255 * min(1, (1.6 - t) / 0.3)); gx, gy = G0[0] + g[0], G0[1] + g[1] - GUM.height // 2 - 74
        def tag(d):
            fz = F(44); tw = d.textlength('ACV GUMMY', font=fz); x = min(max(gx, 80 + tw / 2 + 18), 1015 - tw / 2 - 18)
            yy = max(gy, HB + 14)
            d.rounded_rectangle([x - tw / 2 - 16, yy - 10, x + tw / 2 + 16, yy + 58], 14, fill=(14, 10, 24, int(aa * 0.9)), outline=(140, 230, 110, aa), width=4)
            d.text((x - tw / 2, yy + 2), 'ACV GUMMY', font=fz, fill=(170, 255, 140, aa), stroke_width=6, stroke_fill=(10, 6, 18, aa))
        layer(img, tag)
    # Joy reacts to each level change with a hop
    hop = 0
    for k in range(1, 4):
        u = t - LS[k]
        if 0 <= u < 0.4: hop = int(60 * 4 * (u / 0.4) * (1 - u / 0.4))
    jo = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(jo, (72 - 26 * 5, 1492 - 78 * 5 - hop))
    # level change: short flash + the level name pops on a dark plate (the escalation stamp)
    name, col, _ = LEVELS[i]
    u = t - LS[i] if f <= FZ else 1.0
    if f > FZ and t >= LEND + HOLD: u = 1.0
    if 0 < LS[i] and 0 <= u < 0.18 and f <= FZ:
        fl = Image.new('RGBA', (W, H), col + (int(90 * (1 - u / 0.18)),)); img.alpha_composite(fl)
    pop = 1.0 if u > 0.25 else 0.7 + 1.6 * u
    pop = min(1.1, pop)
    text_layer(img, [(TX, 1200 - int(40 * (pop - 1)), name, int(84 * pop), col, 10, 255)])   # level name as an unboxed stamp; plate + 'LEVEL n/4' cut
    # end question: hard pop under the band, held HOLD s, fades during the loop-back
    img.alpha_composite(HOOK_END if LEND <= t < LEND + HOLD else HOOK)   # end question takes the hook's place for the hold, then the hook returns for the loop
    wr.write(img)
    if f in fit + [0, NF - 1, int(LEND * FPS) + 10, int(9.1 * FPS)]: img.convert('RGB').save(f'p42_{f:04d}.png')
wr.close()
for k in range(4): ev.append((LS[k], 'swish')); ev.append((LS[k] + 0.05, 'ding_8bit'))
ev.append((LEND, 'chime'))
json.dump({'events': ev}, open('v42_ev.json', 'w')); print('done', NF, 'frames', TE, 's; fit', fit)
