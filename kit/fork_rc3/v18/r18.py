import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
import numpy as np
D18 = SP + 'fork_rc3/v18/'; OUT = D18 + 'v18_noaudio.mp4'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['THINK YOU CAN', 'NAIL IT?'], accent=1, sub='ONLY 0.1% CAN')
DUR = 6.0; N = int(DUR * FPS)
TM = 2.9   # the one fitting frame stays frame 87
# motion is now periodic over the 6.0s reel (whole harmonics of 1/6 Hz), so the last frame flows into frame 0;
# searched (fork_rc3/v18/search18.py seed 15030): frame 0 misses by ~112px, the only fit is frame 87, nearest misses 16.9/17.3px (frames 86/88; old was 14.3px)
MOT = {'s': (0.22, 7, 3, 0.3206583227804297, 0.6043624986109397, 1.492197475131093), 'dx': (80, 5, 4, 0.267231356284901, 4.134609806650664, 4.957613913875739), 'dy': (48, 2, 4, 0.4909040547018126, 1.1687487353927848, 6.2048822040110085)}
def mot(key, t):
    amp, k1, k2, a2, p1, p2 = MOT[key]; w = 2 * math.pi / DUR
    g = lambda tt: math.sin(k1 * w * tt + p1) + a2 * math.sin(k2 * w * tt + p2)
    return amp * (g(t) - g(TM)) / (1 + a2)
BGF = bg_frames('hub.gif', (int(1920 * H / 1080), H), step=2, bright=0.8)
BGF = [f.crop(((f.width - W) // 2 + 120, 0, (f.width - W) // 2 + 120 + W, H)).filter(ImageFilter.GaussianBlur(2.5)) for f in BGF]
G0 = gummy('mel', 1); K = 10
GT = up(G0, K); CX, CY = 540, 950
# dashed outline of the gummy at the target size
mask = np.array(GT.getchannel('A')) > 0
edge = mask & ~(np.roll(mask, 1, 0) & np.roll(mask, -1, 0) & np.roll(mask, 1, 1) & np.roll(mask, -1, 1))
ys, xs = np.nonzero(edge); ang = np.arctan2(ys - GT.height / 2, xs - GT.width / 2)
OUTL = Image.new('RGBA', (GT.width + 40, GT.height + 40), (0, 0, 0, 0)); od = ImageDraw.Draw(OUTL)
for x, y, a in zip(xs, ys, ang):
    if int((a + math.pi) / (2 * math.pi) * 40) % 2 == 0:
        od.rectangle([x + 20 - 9, y + 20 - 9, x + 20 + 9, y + 20 + 9], fill=(16, 10, 30, 255))   # dark edge
for x, y, a in zip(xs, ys, ang):
    if int((a + math.pi) / (2 * math.pi) * 40) % 2 == 0:
        od.rectangle([x + 20 - 5, y + 20 - 5, x + 20 + 5, y + 20 + 5], fill=(255, 255, 255, 255))   # 3x thicker dashes
PED = crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')); PED = up(PED, 5)
CYR = idle('cyrus', 4); JOY = idle('joy', 4)
rng = random.Random(8); SPK = [(rng.uniform(0, W), rng.uniform(300, 1600), rng.uniform(0, 6.3)) for _ in range(30)]
wr = Writer(OUT)
for f in range(N):
    t = f / FPS
    img = BGF[int(t * 5) % len(BGF)].copy()
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 24, 60)))
    img.alpha_composite(PED, (CX - PED.width // 2, 1225))
    s = 1 + mot('s', t); dx = mot('dx', t); dy = mot('dy', t)
    g = GT.resize((max(1, int(round(GT.width * s))), max(1, int(round(GT.height * s)))), Image.NEAREST)
    # soft glow under the gummy
    layer(img, lambda d: [d.ellipse([CX + dx - r, CY + dy - r, CX + dx + r, CY + dy + r], fill=(255, 190, 120, 14)) for r in range(240, 120, -20)])
    img.alpha_composite(g, (int(round(CX + dx - g.width / 2)), int(round(CY + dy - g.height / 2))))
    img.alpha_composite(OUTL, (CX - OUTL.width // 2, CY - OUTL.height // 2))
    layer(img, lambda d: [d.rectangle([x - 3, y - 3, x + 3, y + 3], fill=(255, 245, 200, int(110 + 110 * math.sin(t * 4 + p)))) for x, y, p in SPK])
    for fr, x in ((CYR, 170), (JOY, 775)):
        im = fr[int(t * 8) % len(fr)]; img.alpha_composite(im, (int(x - im.width / 2), 1490 - 78 * 4))
    layer(img, lambda d: d.rounded_rectangle([76, HB + 10, 1004, HB + 144], 18, fill=(14, 10, 24, 215)))
    text_layer(img, [(W / 2, HB + 24, 'PAUSE WHEN IT FITS', 50, (255, 214, 60), 8, 255), (W / 2, HB + 86, 'COMMENT YOUR TIME', 44, (255, 255, 255), 7, 255)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if abs(t - TM) < 0.5 / FPS: img.convert('RGB').save(D18 + 'nail_match.png')
    if f in (0, 60, 179): img.convert('RGB').save(D18 + f'p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(0.0, 'twinkle')]}, open(D18 + 'v18_events.json', 'w'))
print('done')
