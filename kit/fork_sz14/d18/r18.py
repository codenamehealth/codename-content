import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
import numpy as np
OUT = SP + 'fork_sz14/d18/nail_sz_noaudio.mp4'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['THINK YOU CAN', 'NAIL IT?'], accent=1, sub='ONLY 0.1% CAN')
DUR = 6.0; N = int(DUR * FPS)
TM, W1, W2, W3 = 2.9, 4.181088654697786, 3.44380752335462, 3.977770479410516
BGF = bg_frames('hub.gif', (int(1920 * H / 1080), H), step=2, bright=0.8)
BGF = [f.crop(((f.width - W) // 2 + 120, 0, (f.width - W) // 2 + 120 + W, H)).filter(ImageFilter.GaussianBlur(2.5)) for f in BGF]
G0 = gummy('mel', 1); K = 10
GT = up(G0, K); CX, CY = 540, 930
# dashed outline of the gummy at the target size
mask = np.array(GT.getchannel('A')) > 0
edge = mask & ~(np.roll(mask, 1, 0) & np.roll(mask, -1, 0) & np.roll(mask, 1, 1) & np.roll(mask, -1, 1))
ys, xs = np.nonzero(edge); ang = np.arctan2(ys - GT.height / 2, xs - GT.width / 2)
OUTL = Image.new('RGBA', (GT.width + 40, GT.height + 40), (0, 0, 0, 0)); od = ImageDraw.Draw(OUTL)
for x, y, a in zip(xs, ys, ang):
    if int((a + math.pi) / (2 * math.pi) * 48) % 2 == 0:
        od.rectangle([x + 20 - 3, y + 20 - 3, x + 20 + 3, y + 20 + 3], fill=(255, 255, 255, 235))
PED = crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')); PED = up(PED, 5)
CYR = idle('cyrus', 4); JOY = idle('joy', 4)
rng = random.Random(8); SPK = [(rng.uniform(0, W), rng.uniform(300, 1600), rng.uniform(0, 6.3)) for _ in range(30)]
wr = Writer(OUT)
for f in range(N):
    t = f / FPS
    img = BGF[int(t * 5) % len(BGF)].copy()
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 24, 60)))
    img.alpha_composite(PED, (CX - PED.width // 2, 1225))
    s = 1 + 0.2 * math.sin(W1 * (t - TM)); dx = 70 * math.sin(W2 * (t - TM)); dy = 40 * math.sin(W3 * (t - TM))
    g = GT.resize((max(1, int(round(GT.width * s))), max(1, int(round(GT.height * s)))), Image.NEAREST)
    # soft glow under the gummy
    layer(img, lambda d: [d.ellipse([CX + dx - r, CY + dy - r, CX + dx + r, CY + dy + r], fill=(255, 190, 120, 14)) for r in range(240, 120, -20)])
    img.alpha_composite(g, (int(round(CX + dx - g.width / 2)), int(round(CY + dy - g.height / 2))))
    img.alpha_composite(OUTL, (CX - OUTL.width // 2, CY - OUTL.height // 2))
    layer(img, lambda d: [d.rectangle([x - 3, y - 3, x + 3, y + 3], fill=(255, 245, 200, int(110 + 110 * math.sin(t * 4 + p)))) for x, y, p in SPK])
    for fr, x in ((CYR, 170), (JOY, 775)):
        im = fr[int(t * 8) % len(fr)]; img.alpha_composite(im, (int(x - im.width / 2), 1490 - 78 * 4))
    text_layer(img, [(W / 2, HB + 16, 'Pause when the gummy', 32, (255, 255, 255), 5, 255), (W / 2, HB + 64, 'fits the outline', 32, (255, 255, 255), 5, 255)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if abs(t - TM) < 0.5 / FPS: img.convert('RGB').save(SP + 'fork_sz14/d18/nail_match.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(0.0, 'twinkle')]}, open(SP + 'fork_sz14/d18/nail_sz_events.json', 'w'))
print('done')
