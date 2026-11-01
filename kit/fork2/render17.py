import sys, math, json
sys.path.insert(0, '../fork1')
from common import *
OUT = SP + 'fork2/beat_noaudio.mp4'
BEAT = 0.6; BAR = 4 * BEAT; T0 = 2.4
# note chart: (time, kind)
chart = []
bars = ['A', 'A', 'A', 'A', 'B', 'B', 'C', 'D']
for bi, ty in enumerate(bars):
    b0 = T0 + bi * BAR
    if ty == 'A': pat = [(0, 'S'), (1, 'S'), (2, 'C')]
    elif ty == 'B': pat = [(0, 'S'), (1, 'S'), (2, 'C'), (3, 'C')]
    elif ty == 'C': pat = [(0, 'S'), (0.5, 'S'), (1, 'S'), (2, 'C'), (3, 'C')]
    else: pat = [(k * 0.5, 'C') for k in range(8)]
    chart += [(round(b0 + p * BEAT, 4), k) for p, k in pat]
T_END = T0 + len(bars) * BAR; DUR = T_END + 3.6; N = int(DUR * FPS)
# Liza's sun temple
BGF = bg_frames('sun_hd.gif', (int(1920 * H / 1080), H), step=1, bright=0.95)
BGF = [f.crop(((f.width - W) // 2 + 60, 0, (f.width - W) // 2 + 60 + W, H)) for f in BGF]
def anim(name, k): return seq(SP + 'fork2/' + name, k, 1, 9)
CAST = [('ray', anim('ray_dance', 4), 118, 1290), ('hollow', anim('hollow_dance', 4), 962, 1290), ('joy', anim('joy_clap', 4), 322, 1320),
        ('cleo', anim('cleo_stomp', 4), 758, 1320), ('cyrus', anim('cyrus_dance', 5), 540, 1365)]
BOOT = crop(Image.open(SP + 'fork2/boot/00.png').convert('RGBA')); CLAP = crop(Image.open(SP + 'fork2/clap/02.png').convert('RGBA'))
BOOT = up(BOOT, 84 / BOOT.height); CLAP = up(CLAP, 84 / CLAP.height)
GUMS = [gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']]
LANE_Y = 1560; HIT_X = 190; SPEED = 760
COLR = {'S': (210, 110, 60), 'C': (90, 150, 255)}
def badge(kind, sc=1.0):
    r = int(62 * sc); b = Image.new('RGBA', (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * r + 5, 2 * r + 5], fill=(30, 20, 40, 255)); d.ellipse([6, 6, 2 * r + 1, 2 * r + 1], fill=COLR[kind] + (255,))
    d.ellipse([14, 14, 2 * r - 7, 2 * r - 7], fill=(250, 244, 230, 255))
    ic = BOOT if kind == 'S' else CLAP; ic = up(ic, sc) if sc != 1 else ic
    b.alpha_composite(ic, (b.width // 2 - ic.width // 2, b.height // 2 - ic.height // 2)); return b
BADGE = {k: badge(k) for k in 'SC'}
events = [(0.6, 'tick_8bit'), (1.2, 'tick_8bit'), (1.8, 'tick_8bit')] + [(t, 'stomp_8bit' if k == 'S' else 'clap_8bit') for t, k in chart] + [(T_END + 0.1, 'cheer')]
rng = random.Random(4); flyers = []
for i, (th, k) in enumerate(chart):
    flyers.append((th, rng.choice(GUMS), rng.uniform(-260, 260), rng.uniform(-900, -700)))
wr = Writer(OUT)
for f in range(N):
    t = f / FPS; bph = (t % BEAT) / BEAT
    img = BGF[int(t * 6) % len(BGF)].copy()
    # beat glow
    pulse = max(0, 1 - bph * 3) if T0 - 0.05 <= t <= T_END else 0
    if pulse > 0: layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 220, 140, int(28 * pulse))))
    # band on stage
    beat_i = t / BEAT
    for name, fr, x, y in CAST:
        k = int(beat_i * 4) % 8 if t >= T0 - BEAT else 0
        im = fr[k]; hop = int(10 * max(0, 1 - bph * 4)) if (T0 <= t <= T_END and name in ('cyrus',)) else 0
        layer(img, lambda d: d.ellipse([x - 75, y - 14, x + 75, y + 14], fill=(0, 0, 0, 70)))
        img.alpha_composite(im, (int(x - im.width / 2), int(y - 78 * (im.width // 92) - hop)))
    # lane
    def lane(d):
        d.rounded_rectangle([20, LANE_Y - 92, W - 20, LANE_Y + 92], 30, fill=(20, 12, 30, 190), outline=(255, 214, 60, 255), width=5)
        for k in range(1, 9):
            x = HIT_X + (k * BEAT - (t - T0) % BEAT) * SPEED
            if x < W - 30: d.line([x, LANE_Y - 70, x, LANE_Y + 70], fill=(255, 255, 255, 40), width=3)
    layer(img, lane)
    # hit target ring (pulses on hit)
    last = max([th for th, k in chart if th <= t], default=-9)
    hk = 1 - min(1, (t - last) / 0.25)
    def target(d):
        r = 74 + 14 * hk
        d.ellipse([HIT_X - r, LANE_Y - r, HIT_X + r, LANE_Y + r], outline=(255, 255, 255, 230), width=8)
        if hk > 0: d.ellipse([HIT_X - r - 30 * (1 - hk), LANE_Y - r - 30 * (1 - hk), HIT_X + r + 30 * (1 - hk), LANE_Y + r + 30 * (1 - hk)], outline=(255, 214, 60, int(255 * hk)), width=6)
    layer(img, target)
    # notes
    for th, k in chart:
        x = HIT_X + (th - t) * SPEED
        if -80 < x < W + 80 and t <= th + 0.12:
            b = BADGE[k]; img.alpha_composite(b, (int(x - b.width / 2), int(LANE_Y - b.height / 2)))
        elif th < t < th + 0.3:
            u = (t - th) / 0.3; b = up(BADGE[k], 1 + 0.6 * u); a = b.getchannel('A').point(lambda p: int(p * (1 - u))); b.putalpha(a)
            img.alpha_composite(b, (int(HIT_X - b.width / 2), int(LANE_Y - b.height / 2)))
    # gummies pop out of each hit
    for th, g, vx, vy in flyers:
        u = t - th
        if 0 <= u < 1.1:
            gx = HIT_X + vx * u * 0.6 + 120 * u; gy = LANE_Y - 60 + vy * u + 1100 * u * u
            gg = g.copy(); gg.putalpha(gg.getchannel('A').point(lambda p: int(p * max(0, 1 - u / 1.1))))
            img.alpha_composite(gg, (int(gx - gg.width / 2), int(gy - gg.height / 2)))
    # big call word + combo
    items = []
    cur = [(th, k) for th, k in chart if th <= t < th + 0.35]
    if cur:
        th, k = cur[-1]; u = (t - th) / 0.35
        items.append((W / 2, LANE_Y - 200, 'STOMP!' if k == 'S' else 'CLAP!', int(60 + 14 * (1 - u)), COLR[k] if k == 'C' else (255, 170, 90), 7, int(255 * (1 - u * u))))
    combo = sum(1 for th, k in chart if th <= t)
    if combo and t <= T_END + 0.3: items.append((W / 2, LANE_Y + 120, f'COMBO x{combo}', 34, (255, 214, 60), 5, 255))
    # title + countdown / legend
    items += [(W / 2, 90, 'PLAY ALONG', 74, (255, 255, 255), 8, 255), (W / 2, 190, 'WITH THE BEAT!', 56, (255, 214, 60), 8, 255)]
    if t < T0:
        for t0, lab in ((0.6, '3'), (1.2, '2'), (1.8, '1')):
            if t0 <= t < t0 + BEAT:
                u = (t - t0) / BEAT; items.append((W / 2, 420, lab, int(170 - 50 * u), (255, 255, 255), 10, int(255 * (1 - u * 0.7))))
    if t < T0 + 2 * BAR:
        a = 255 if t < T0 + 1.5 * BAR else int(255 * max(0, (T0 + 2 * BAR - t) / (0.5 * BAR)))
        items += [(W / 2 - 220, LANE_Y + 190, '= STOMP', 30, (255, 255, 255), 5, a), (W / 2 + 290, LANE_Y + 190, '= CLAP', 30, (255, 255, 255), 5, a)]
        for (kk, xx) in (('S', W / 2 - 420), ('C', W / 2 + 100)):
            b = up(BADGE[kk], 0.55); b.putalpha(b.getchannel('A').point(lambda p: int(p * a / 255))); img.alpha_composite(b, (int(xx), int(LANE_Y + 170)))
    if bars[min(len(bars) - 1, int(max(0, t - T0) / BAR))] == 'D' and T0 + 7 * BAR - 0.6 <= t < T_END:
        items.append((W / 2, 420, 'FINAL BAR!', 64, (255, 120, 120), 8, 255)) if False else items.append((W / 2, 420, 'DOUBLE TIME!', 64, (255, 120, 120), 8, 255))
    if t >= T_END:
        u = t - T_END; a = int(255 * min(1, u / 0.3))
        items += [(W / 2, 400, 'DID YOU KEEP', 64, (255, 255, 255), 8, a), (W / 2, 490, 'THE BEAT?', 64, (255, 214, 60), 8, a), (W / 2, 600, 'Comment your combo', 40, (255, 255, 255), 6, a)]
    text_layer(img, items)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(SP + f'fork2/prev17/p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in events]}, open(SP + 'fork2/beat_events.json', 'w'))
print('done', DUR, len(chart))
