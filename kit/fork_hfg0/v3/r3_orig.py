import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1'); from hook2 import hook_layer2
HOOKB, HB = hook_layer2(["What's the", 'answer?'], accent=1, sub='Comment your answer')   # comment prompt from frame 0, 44px+
ENDB, _ = hook_layer2(["Time's up!"], accent=0, sub='Comment your answer')
print('hook bottom', HB)   # end card replaces the title box (no clue covered)
# Bennett #3: no slimes; the characters just strike cool poses (Syeda's idle -> Syeda's victory pose, 3x, front-facing).
# One pose per character everywhere, so the pose never looks like it changes the value.
IDL = {g: idle(g, 3) for g in ['hollow', 'cyrus', 'joy']}
VICF = {g: [up(f.resize((92, 92), Image.NEAREST), 3) for f in vic(g, None)] for g in ['hollow', 'cyrus', 'joy']}
PCOL = {'hollow': (190, 170, 255), 'cyrus': (255, 170, 60), 'joy': (140, 230, 110)}
FEET = 202                      # feet line inside each 220px strip (sprite canvas feet at 78*3)
SX0, SX1 = 70, 1025             # strips inset to the safe margins (were edge to edge)
CX = [165, 365, 565]            # character centres (absolute x); '+' at 265/465, '=' at 672, power window x700-880
GG = gummy('gold', 2)
ROWS = [(['hollow', 'hollow', 'hollow'], '30', 'hub.gif', 0.55, 'VILLAGE'),
        (['hollow', 'hollow', 'cyrus'], '35', 'found_hd.gif', 0.5, 'FOREST'),
        (['cyrus', 'joy', 'joy'], '31', 'sun_hd.gif', 0.5, 'SUN TEMPLE'),
        (['hollow', 'cyrus', 'joy'], '?', 'recov_hd.gif', 0.45, 'MOON TEMPLE')]
RH = 214; Y0 = [618, 836, 1054, 1272]
BGS = []
BACK = bg_frames('hub.gif', (1080, 1920), box=(656, 0, 1264, 1080), step=8, bright=0.3, blur=4)   # dim full-bleed backdrop instead of flat black
for (_, _, bg, yy, _) in ROWS:
    fr = bg_frames(bg, (1080, 608), step=4, bright=0.85)
    top = int(608 * yy) - RH // 2
    BGS.append([f.crop((SX0, top, SX1, top + RH)) for f in fr])
TIN = [-0.9, 0.35, 1.6, 2.85]   # Village panel already in at frame 0 with its counter mid-tick
def frame_at(t):
    img = BACK[int(t * 2) % len(BACK)].copy()
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
        d.rounded_rectangle([700 - SX0, 16, 880 - SX0, RH - 16], 18, fill=(14, 10, 24, 215), outline=(255, 214, 60, 255), width=5)
        d.rounded_rectangle([0, 0, SX1 - SX0 - 1, RH - 1], 6, outline=(255, 214, 60, 255), width=6)
        strip.alpha_composite(L)
        cnt = val
        if val != '?':
            k = max(0, min(1, (t - ta) / 0.8)); cnt = str(int(round(int(val) * k)))
        PX = 790 - SX0
        items = []   # 28px POWER label and the gold icon cut (under the 44px floor); the '=' already says it's a total
        if val == '?':
            pul = 1 + 0.12 * math.sin(t * 7)
            items.append((PX, 107 - int(52 * pul), '?', int(104 * pul), (255, 214, 60), 8, 255))
        else:
            items.append((PX, 67, cnt, 80, (255, 255, 255), 8, 255))
        # sum glyphs: + between the figures, = before the POWER box
        for gx, gt in ((265, '+'), (465, '+'), (672, '=')):
            items.append((gx - SX0, 86, gt, 48, (255, 255, 255), 7, 255))
        text_layer(strip, items)
        img.alpha_composite(strip, (off + SX0, y0))
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
            def sh(d): d.ellipse([off + CX[i] - 56, y0 + FEET - 10, off + CX[i] + 56, y0 + FEET + 8], fill=(0, 0, 0, 90))
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
    # header
    T0, T1 = 3.6, 7.3            # think window cut 5.0s -> 3.7s (no dead stretch)
    if t < T1:
        k = 1 - max(0, min(1, (t - T0) / (T1 - T0)))
        red = k < 0.4; pul = 0.5 + 0.5 * math.sin(t * 4 * math.pi) if red else 0
        def bar(d):
            d.rectangle([SX0, 590, SX1, 610], fill=(14, 10, 24, 255), outline=(255, 214, 60, 255), width=4)
            d.rectangle([SX0 + 6, 595, SX0 + 6 + (SX1 - SX0 - 12) * k, 605], fill=((255, 60 + int(80 * pul), 50, 255) if red else (120, 210, 90, 255)))
        layer(img, bar)
        img.alpha_composite(HOOKB)
    else:
        u = t - T1; sc = 1.0 + 0.12 * max(0, 1 - u / 0.12)   # hard pop, in the title slot
        E = ENDB if sc < 1.01 else ENDB.resize((int(W * sc), int(H * sc)), Image.NEAREST).crop((int(547 * sc - 547), int(416 * sc - 416), int(547 * sc - 547) + W, int(416 * sc - 416) + H))
        img.alpha_composite(E)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in (0.0, 1.0, 5.0, 6.8, 7.34, 8.0): frame_at(t).convert('RGB').save(f'h_still_{t}.png')
        sys.exit()
    DUR = 8.6; wr = Writer('v3_noaudio.mp4')
    for f in range(int(DUR * FPS)): wr.write(frame_at(f / FPS))
    wr.close()
    ev = []
    for r, ti in enumerate(TIN):
        if ti >= 0: ev.append((ti, 'whoosh_8bit'))
        for i in range(3): ev.append((ti + 0.55 + i * 0.12, 'jump' if i % 2 == 0 else 'swish'))
        ev.append((ti + 0.85, 'twinkle'))
        if r < 3 and ti + 1.35 > 0: ev.append((ti + 1.35, 'coin_8bit'))
        else: ev.append((ti + 1.0, 'ding_8bit'))
    ev = [e for e in ev if e[0] >= 0] + [(3.6 + k * 0.6, 'tick_8bit') for k in range(4)] + [(6.0 + k * 0.33, 'tick_8bit') for k in range(4)] + [(7.3, 'buzz_8bit')]
    json.dump({'events': ev}, open('ev.json', 'w')); print('done')
