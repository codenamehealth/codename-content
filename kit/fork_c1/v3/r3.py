import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
HOOKB, HB = hook_layer(["What's the", 'answer?'], accent=1)
# Bennett #3: no slimes; the characters just strike cool poses (Syeda's idle -> Syeda's victory pose, 3x, front-facing).
# One pose per character everywhere, so the pose never looks like it changes the value.
IDL = {g: idle(g, 3) for g in ['hollow', 'cyrus', 'joy']}
VICF = {g: [up(f.resize((92, 92), Image.NEAREST), 3) for f in vic(g, None)] for g in ['hollow', 'cyrus', 'joy']}
PCOL = {'hollow': (190, 170, 255), 'cyrus': (255, 170, 60), 'joy': (140, 230, 110)}
FEET = 216                      # feet line inside each 230px strip (sprite canvas feet at 78*3)
CX = [140, 345, 550]            # character centres (power window starts at x700)
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
        ta = TIN[r] + 0.55
        sd = ImageDraw.Draw(strip)
        L = Image.new('RGBA', strip.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        # power window
        d.rounded_rectangle([700, 18, 880, RH - 18], 18, fill=(14, 10, 24, 215), outline=(255, 214, 60, 255), width=5)
        d.rounded_rectangle([0, 0, 1079, RH - 1], 6, outline=(255, 214, 60, 255), width=6)
        strip.alpha_composite(L)
        cnt = val
        if val != '?':
            k = max(0, min(1, (t - ta) / 0.8)); cnt = str(int(round(int(val) * k)))
        items = [(790, 36, 'POWER', 28, (255, 214, 60), 4, 255)]
        if val == '?':
            pul = 1 + 0.12 * math.sin(t * 7)
            items.append((790, 80, '?', int(104 * pul), (255, 214, 60), 8, 255))
        else:
            items.append((790, 86, cnt, 80, (255, 255, 255), 8, 255))
        text_layer(strip, items)
        strip.alpha_composite(GG, (672, 6))
        img.alpha_composite(strip, (off, y0))
        # characters: idle, then each strikes its pose in turn (small hop + burst), then holds the pose loop
        ta = TIN[r] + 0.55
        for i, g in enumerate(party):
            ts = ta + i * 0.12; v = t - ts
            if v < 0: fr = IDL[g][int(t * 6 + i * 2) % len(IDL[g])]; hop = 0
            else:
                fr = VICF[g][int(v * 10) % 6]
                hop = int(26 * math.sin(v / 0.3 * math.pi)) if v < 0.3 else 0
            x = off + CX[i] - fr.width // 2; y = y0 + FEET - 78 * 3 - hop
            # soft ground shadow
            def sh(d): d.ellipse([off + CX[i] - 62, y0 + FEET - 10, off + CX[i] + 62, y0 + FEET + 8], fill=(0, 0, 0, 90))
            layer(img, sh)
            if 0 <= v < 0.45:
                u = v / 0.45
                def burst(d, u=u, g=g):
                    cx, cy = off + CX[i], y0 + FEET - 100
                    for k in range(10):
                        aa = k * math.pi / 5 + 0.3; r0 = 40 + 90 * u; r1 = r0 + 34 * (1 - u)
                        d.line([(cx + r0 * math.cos(aa), cy + r0 * math.sin(aa) * 0.8), (cx + r1 * math.cos(aa), cy + r1 * math.sin(aa) * 0.8)], fill=PCOL[g] + (int(255 * (1 - u)),), width=7)
                layer(img, burst)
            img.alpha_composite(fr, (x, y))
            if v >= 0.3:   # little twinkles while holding the pose
                def tw(d, g=g, v=v):
                    for k in range(2):
                        ph = (v * 1.3 + k * 0.5 + i * 0.27) % 1.0
                        sx = off + CX[i] + (-70 if k == 0 else 66); sy = y0 + 60 + 30 * k
                        rr = 10 * math.sin(ph * math.pi)
                        if rr > 1:
                            d.polygon([(sx, sy - rr * 1.6), (sx + rr * 0.5, sy), (sx, sy + rr * 1.6), (sx - rr * 0.5, sy)], fill=(255, 250, 220, 230))
                            d.polygon([(sx - rr * 1.6, sy), (sx, sy - rr * 0.5), (sx + rr * 1.6, sy), (sx, sy + rr * 0.5)], fill=(255, 250, 220, 230))
                layer(img, tw)
        text_layer(img, [(off + 210, y0 + 22, name, 22, (255, 255, 255), 4, 255)])
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
    DUR = 11.5; wr = Writer('v3_noaudio.mp4')
    for f in range(int(DUR * FPS)): wr.write(frame_at(f / FPS))
    wr.close()
    ev = []
    for r, ti in enumerate(TIN):
        ev.append((ti, 'whoosh_8bit'))
        for i in range(3): ev.append((ti + 0.55 + i * 0.12, 'jump' if i % 2 == 0 else 'swish'))
        ev.append((ti + 0.85, 'twinkle'))
        if r < 3: ev.append((ti + 1.35, 'coin_8bit'))
        else: ev.append((ti + 1.0, 'ding_8bit'))
    ev += [(5.0 + k, 'tick_8bit') for k in range(5)] + [(10.0, 'buzz_8bit')]
    json.dump({'events': ev}, open('ev.json', 'w')); print('done')
