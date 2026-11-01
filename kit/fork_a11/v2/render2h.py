import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
HOOKB, HB = hook_layer(["What's the", 'answer?'], accent=1)
SIDE = {g: up(Image.open(PL + f'race/in/{g}_side.png').convert('RGBA'), 3) for g in ['joy', 'cyrus', 'cleo', 'ray']}
SIDE['hollow'] = up(Image.open(SP + 'syeda_src/hollow/char2.png').convert('RGBA'), 3)
SL = slime_frames(3)
GG = gummy('gold', 2)
ROWS = [(['hollow', 'hollow', 'hollow'], '30', 'hub.gif', 0.55, 'VILLAGE'),
        (['hollow', 'hollow', 'cyrus'], '35', 'found_hd.gif', 0.5, 'FOREST'),
        (['cyrus', 'joy', 'joy'], '31', 'sun_hd.gif', 0.5, 'SUN TEMPLE'),
        (['hollow', 'cyrus', 'joy'], '?', 'recov_hd.gif', 0.45, 'MOON TEMPLE')]
RH = 230; Y0 = [546, 784, 1022, 1260]
BGS = []
for (_, _, bg, yy, _) in ROWS:
    fr = bg_frames(bg, (1080, 608), step=4, bright=0.85)
    top = int(608 * yy) - RH // 2
    BGS.append([f.crop((0, top, 1080, top + RH)) for f in fr])
TIN = [0.3, 1.5, 2.7, 3.9]
def frame_at(t):
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    hub = bg_frames('hub.gif', (1080, 608), step=8, bright=0.4)[0] if False else None
    for r, (party, val, bg, yy, name) in enumerate(ROWS):
        u = (t - TIN[r]) / 0.45
        if u <= 0: continue
        off = int((1 - min(1, u)) ** 2 * -1100)
        y0 = Y0[r]
        strip = BGS[r][int(t * 5) % len(BGS[r])].copy()
        sd = ImageDraw.Draw(strip)
        # party
        ta = TIN[r] + 0.55
        for i, g in enumerate(party):
            sp = SIDE[g]; x = 70 + i * 170
            lunge = 0
            if t > ta + i * 0.12:
                v = t - (ta + i * 0.12)
                if v < 0.35: lunge = int(60 * math.sin(v / 0.35 * math.pi))
            bob = int(4 * math.sin(t * 6 + i))
            strip.alpha_composite(sp, (x - 60 + lunge, RH - 18 - 78 * 3 + bob))
        # friendly slime target
        sf = SL[int(t * 8) % len(SL)]; sx = 620
        hit = any(0 < t - (ta + i * 0.12) - 0.15 < 0.2 for i in range(3))
        strip.alpha_composite(sf, (sx - sf.width // 2 + (8 if hit else 0), RH - 22 - sf.height))
        L = Image.new('RGBA', strip.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        if hit:
            for k in range(8):
                a = k * 0.785; rr = 40
                d.line([(sx - 60, RH - 110), (sx - 60 + rr * math.cos(a), RH - 110 + rr * math.sin(a))], fill=(255, 240, 160, 255), width=6)
        # power window
        d.rounded_rectangle([700, 18, 880, RH - 18], 18, fill=(14, 10, 24, 215), outline=(255, 214, 60, 255), width=5)
        d.rounded_rectangle([0, 0, 1079, RH - 1], 6, outline=(255, 214, 60, 255), width=6)
        strip.alpha_composite(L)
        cnt = val
        if val != '?':
            k = max(0, min(1, (t - ta) / 0.8)); cnt = str(int(round(int(val) * k)))
        items = [(790, 36, 'POWER', 28, (255, 214, 60), 4, 255), (210, 22, name, 22, (255, 255, 255), 4, 255)]
        if val == '?':
            pul = 1 + 0.12 * math.sin(t * 7)
            items.append((790, 80, '?', int(104 * pul), (255, 214, 60), 8, 255))
        else:
            items.append((790, 86, cnt, 80, (255, 255, 255), 8, 255))
        text_layer(strip, items)
        strip.alpha_composite(GG, (672, 6))
        img.alpha_composite(strip, (off, y0))
    # header
    T0, T1 = 5.0, 10.0
    if t < T1:
        k = 1 - max(0, min(1, (t - T0) / (T1 - T0)))
        def bar(d):
            d.rectangle([90, 512, 900, 538], fill=(14, 10, 24, 255), outline=(255, 214, 60, 255), width=4)
            d.rectangle([96, 518, 96 + (900 - 102) * k, 532], fill=(120, 210, 90, 255) if k > 0.3 else (255, 120, 60, 255))
        layer(img, bar)
    else:
        u = min(1, (t - T1) / 0.3)
        def card(d): d.rounded_rectangle([110, 556, 880, 846], 24, fill=(14, 10, 24, int(235 * u)), outline=(255, 214, 60, int(255 * u)), width=6)
        layer(img, card)
        text_layer(img, [(495, 606, "TIME'S UP!", 64, (255, 214, 60), 8, int(255 * u)), (495, 726, 'Comment your answer', 38, (255, 255, 255), 5, int(255 * u))])
    img.alpha_composite(HOOKB)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in (1.0, 4.8, 10.5): frame_at(t).convert('RGB').save(f'h_still_{t}.png')
        sys.exit()
    DUR = 11.5; wr = Writer('v2h_noaudio.mp4')
    for f in range(int(DUR * FPS)): wr.write(frame_at(f / FPS))
    wr.close()
    ev = []
    for r, ti in enumerate(TIN):
        ev.append((ti, 'whoosh_8bit'))
        for i in range(3): ev.append((ti + 0.55 + i * 0.12, 'sword_swish' if i % 2 == 0 else 'punch'))
        ev.append((ti + 0.75, 'boing'))
        if r < 3: ev.append((ti + 1.35, 'coin_8bit'))
        else: ev.append((ti + 1.0, 'ding_8bit'))
    ev += [(5.0 + k, 'tick_8bit') for k in range(5)] + [(10.0, 'buzz_8bit')]
    json.dump(ev, open('ev.json', 'w')); print('done')
