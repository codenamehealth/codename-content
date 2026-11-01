import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
D17 = SP + 'fork_n1/v17/'; OUT = D17 + 'v17_noaudio.mp4'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_band
# Oct 29 pass: full-width strip (busy bright temple behind it), no box/border; COMMENT YOUR COMBO, the STOMP/CLAP legend,
# the plates behind the call words / DOUBLE TIME and the DID YOU KEEP THE BEAT? end card are cut
HOOK, HB = hook_band(['PLAY ALONG', 'WITH THE BEAT!'], accent=1)
BEAT = 0.6; BAR = 4 * BEAT; T0 = 0.6   # first note lands at 0.6s, already scrolling in at frame 0 (was a 3-2-1 countdown to 2.4s)
# note chart: (time, kind)
chart = []
bars = ['A', 'A', 'B', 'C', 'D', 'E']   # DOUBLE TIME from bar 5 (10.2s) for 2 bars / 4.8s (was 1 bar at 19.2s)
for bi, ty in enumerate(bars):
    b0 = T0 + bi * BAR
    if ty == 'A': pat = [(0, 'S'), (1, 'S'), (2, 'C')]
    elif ty == 'B': pat = [(0, 'S'), (1, 'S'), (2, 'C'), (3, 'C')]
    elif ty == 'C': pat = [(0, 'S'), (0.5, 'S'), (1, 'S'), (2, 'C'), (3, 'C')]
    elif ty == 'D': pat = [(k * 0.5, 'C') for k in range(8)]
    else: pat = [(k * 0.5, 'S' if k % 2 == 0 else 'C') for k in range(8)]
    chart += [(round(b0 + p * BEAT, 4), k) for p, k in pat]
T_END = T0 + len(bars) * BAR; DUR = T_END + 3 * BEAT; N = int(round(DUR * FPS))   # 1.2s end card + 0.6s back to the opening state (DUR is a whole number of beats so the loop stays on the grid)
T_Q1 = T_END + 2 * BEAT
chart_draw = chart + [(round(th + DUR, 4), k) for th, k in chart[:4]]   # next loop's first notes scroll in at the end -> seamless restart
# Liza's sun temple
BGF = bg_frames('sun_hd.gif', (int(1920 * H / 1080), H), step=1, bright=0.95)
BGF = [f.crop(((f.width - W) // 2 + 60, 0, (f.width - W) // 2 + 60 + W, H)) for f in BGF]
def anim(name, k): return seq(SP + 'fork2/' + name, k, 1, 9)
CAST = [('ray', anim('ray_dance', 4), 160, 1040), ('hollow', anim('hollow_dance', 4), 905, 1040), ('joy', anim('joy_clap', 4), 330, 1075),
        ('cleo', anim('cleo_stomp', 4), 750, 1075), ('cyrus', anim('cyrus_dance', 5), 540, 1105)]
BOOT = crop(Image.open(SP + 'fork2/boot/00.png').convert('RGBA')); CLAP = crop(Image.open(SP + 'fork2/clap/02.png').convert('RGBA'))
BOOT = up(BOOT, 84 / BOOT.height); CLAP = up(CLAP, 84 / CLAP.height)
GUMS = [gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']]
LANE_Y = 1242; HIT_X = 190; SPEED = 760
COLR = {'S': (210, 110, 60), 'C': (90, 150, 255)}
def badge(kind, sc=1.0):
    r = int(62 * sc); b = Image.new('RGBA', (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * r + 5, 2 * r + 5], fill=(30, 20, 40, 255)); d.ellipse([6, 6, 2 * r + 1, 2 * r + 1], fill=COLR[kind] + (255,))
    d.ellipse([14, 14, 2 * r - 7, 2 * r - 7], fill=(250, 244, 230, 255))
    ic = BOOT if kind == 'S' else CLAP; ic = up(ic, sc) if sc != 1 else ic
    b.alpha_composite(ic, (b.width // 2 - ic.width // 2, b.height // 2 - ic.height // 2)); return b
BADGE = {k: badge(k) for k in 'SC'}
events = [(t, 'stomp_8bit' if k == 'S' else 'clap_8bit') for t, k in chart] + [(T_END + 0.1, 'cheer')]
rng = random.Random(4); flyers = []
for i, (th, k) in enumerate(chart):
    flyers.append((th, rng.choice(GUMS), rng.uniform(-260, 260), rng.uniform(-900, -700)))
PREV = [int(v) for v in os.environ.get('PREV', '').split(',') if v]
wr = Writer(OUT)
for f in range(N):
    t = f / FPS; bph = (t % BEAT) / BEAT
    img = BGF[int(t * 6) % len(BGF)].copy()
    # beat glow
    pulse = max(0, 1 - bph * 3) if (T0 - 0.05 <= t <= T_END or t >= DUR - 0.05) else 0
    if pulse > 0: layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 220, 140, int(28 * pulse))))
    # band on stage
    beat_i = t / BEAT
    for name, fr, x, y in CAST:
        k = int(beat_i * 4) % 8
        im = fr[k]; hop = int(10 * max(0, 1 - bph * 4)) if (T0 <= t <= T_END and name in ('cyrus',)) else 0
        layer(img, lambda d: d.ellipse([x - 75, y - 14, x + 75, y + 14], fill=(0, 0, 0, 70)))
        img.alpha_composite(im, (int(x - im.width / 2), int(y - 78 * (im.width // 92) - hop)))
    # lane
    def lane(d):
        d.rounded_rectangle([76, LANE_Y - 92, 880, LANE_Y + 92], 30, fill=(20, 12, 30, 190), outline=(255, 214, 60, 255), width=5)
        for k in range(1, 9):
            x = HIT_X + (k * BEAT - (t - T0) % BEAT) * SPEED
            if x < 860: d.line([x, LANE_Y - 70, x, LANE_Y + 70], fill=(255, 255, 255, 40), width=3)
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
    for th, k in chart_draw:
        x = HIT_X + max(0.0, th - t) * SPEED   # Oct 29 2pm (Bennett): the note locks dead centre in the ring on the hit instead of sliding past it to the left before it pops
        if -80 < x < 850 and t <= th + 0.12:
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
        aw = 255 if u < 0.55 else int(255 * (1 - (u - 0.55) / 0.45)); sz = int(64 + 14 * (1 - u)); word = 'STOMP!' if k == 'S' else 'CLAP!'
        items.append((W / 2, HB + 164 - sz / 2, word, sz, (110, 165, 255) if k == 'C' else (255, 150, 60), 10, aw))
    combo = sum(1 for th, k in chart if th <= t)
    if combo and t <= T_END + 0.3:
        cu = min([t - th for th, k in chart if th <= t]); cz = int(64 + 12 * max(0, 1 - cu / 0.15))
        items.append((W / 2 - 40, LANE_Y + 136 - cz / 2, f'COMBO x{combo}', cz, (255, 214, 60), 9, 255))
    if T0 + 4 * BAR - 0.6 <= t < T_END:
        u = t - (T0 + 4 * BAR - 0.6); dz = int(68 * (1.08 - 0.08 * min(1, u / 0.12)))
        items.append((W / 2, HB + 58 - dz / 2, 'DOUBLE TIME!', dz, (255, 110, 110), 10, 255))
    text_layer(img, items); img.alpha_composite(HOOK)
    wr.write(img)
    if f in PREV: img.convert('RGB').save(D17 + f'p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in events]}, open(D17 + 'v17_events.json', 'w'))
print('done', DUR, len(chart))
