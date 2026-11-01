import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #82 safe-zone + hook pass (source: fork_b8/r84.py): arena scaled to fit the zone (R0 420 -> 360, bricks 1.5x -> 1.25x),
# exit gap moved from the left (bins 25-27) to the upper right so the escape happens inside the zone, Hollow 1.7x -> 2x (integer) in a slightly bigger bubble.
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import hook as HK
def band(lines, accent, sub, subsize=46, color=(255, 214, 60)):
    f, s = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=(255, 255, 255), stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
OLDHB = band(['CAN THE HOLLOW', 'ESCAPE?'], 1, 'COMMENT YES OR NO')[1]
HOOK, HB = HK.hook_fade(['CAN THE HOLLOW', 'ESCAPE?'], accent=1)   # hfg9: soft fade, no box, comment line cut
HX = 547; CX, CY = 478, 1068; R0 = 360; NB = 60; BH = 28; RB = 64
GAP = set(range(50, 53))            # bins (6 deg each) forming the exit gap, upper right (300-318 deg)
BR = up(crop(Image.open(B8 + 'brick/03.png').convert('RGBA')), 1.25)
BR2 = ImageEnhance.Brightness(BR).enhance(1.25)
SPD0 = float(os.environ.get('SP', '550')); T_GO = 0.0; GS0, GSI = 2.0, 3.0
def bin_of(a): return int((math.degrees(a) % 360) // (360 / NB))
def sim(seed, dur=46):
    rnd = random.Random(seed)
    x, y = CX + rnd.uniform(-60, 60), CY + rnd.uniform(-60, 60)
    a = rnd.uniform(0, 6.283); vx, vy = math.cos(a) * SPD0, math.sin(a) * SPD0
    h = [0] * NB; bricks = []; bounces = []; frames = []; esc = None; gums = []; got = []
    spawn_t = GS0; boost = -9; kinds = ['mush']  # rc9: mushroom gummies only (SPEED fits this game)
    f = 0
    while f < dur * FPS:
        t = f / FPS
        if t >= T_GO and esc is None:
            sp = SPD0 * (1 + 0.004 * len(bounces)) * (1.35 if t - boost < 2.0 else 1.0)
            n = math.hypot(vx, vy); vx, vy = vx / n * sp, vy / n * sp
            for _ in range(4):
                x += vx / FPS / 4; y += vy / FPS / 4
                dx, dy = x - CX, y - CY; dist = math.hypot(dx, dy); ang = math.atan2(dy, dx); b = bin_of(ang)
                if b in GAP:
                    if dist > R0 + RB + 30: esc = t; break
                    continue
                reff = R0 - h[b] * BH - 14
                if dist + RB > reff and (dx * vx + dy * vy) > 0:
                    nx, ny = dx / dist, dy / dist
                    dot = vx * nx + vy * ny; vx -= 2 * dot * nx; vy -= 2 * dot * ny
                    th = rnd.uniform(-0.28, 0.28); c, s = math.cos(th), math.sin(th); vx, vy = vx * c - vy * s, vx * s + vy * c
                    x, y = CX + nx * (reff - RB - 1), CY + ny * (reff - RB - 1)
                    if h[b] < 9:
                        h[b] += 1; bricks.append((t, b, h[b]))
                    bounces.append((t, b))
            if esc is not None: pass
            if t >= spawn_t and len(gums) < 6:
                gr = rnd.uniform(50, 190); ga = rnd.uniform(0, 6.28)
                gums.append(dict(x=CX + gr * math.cos(ga), y=CY + gr * math.sin(ga), k='mush', t=t, got=None)); spawn_t = t + GSI
            for g in gums:
                if g['got'] is None and math.hypot(g['x'] - x, g['y'] - y) < RB + 20: g['got'] = t; boost = t
        if esc is not None:
            vy += 900 / FPS; x += vx / FPS * 0.35 * 600 / SPD0; y += vy / FPS * 0.35 * 600 / SPD0  # rc9: same drift speed as the 600px/s version  # slower drift after the escape so the bubble pops below the hook
        frames.append((x, y, list(h), len(bounces)))
        f += 1
        if esc is not None and t > esc + 4.0: break
    return frames, bricks, bounces, esc, gums
if sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        fr, br, bo, esc, gums = sim(s)
        if esc and 13.5 < esc < 18 and len(bo) > 45 and sum(1 for g in gums if g['got']) >= 3:
            adj = [round(tb, 1) for tb, b in bo if (b in (min(GAP) - 1, max(GAP) + 1))]
            print(os.environ.get('SP'), s, round(esc, 1), len(bo), [round(g['got'], 1) for g in gums if g['got']], adj, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, BRICKS, BOUNCES, ESC, GUMS = sim(SEED)
print('escape', ESC, 'bounces', len(BOUNCES), 'gums', [(round(g['got'], 1) if g['got'] else None) for g in GUMS])
BG = bg_frames('sun_hd.gif', (int(1920 * 1.8), int(1080 * 1.8)), step=2, bright=0.5)
HOL = idle('hollow', 1); HOLS = [up(f.crop((20, 10, 76, 60)), 2) for f in HOL]
VICF = vic('hollow', 320)
GUMI = {k: gummy(k, 3) for k in GUMK}
def bubble(f):
    b = Image.new('RGBA', (2 * RB + 8, 2 * RB + 8), (0, 0, 0, 0))
    L = Image.new('RGBA', b.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse([4, 4, 2 * RB + 3, 2 * RB + 3], fill=(170, 220, 255, 60), outline=(220, 245, 255, 230), width=4)
    b.alpha_composite(L)
    s = HOLS[f % len(HOLS)]; b.alpha_composite(s, (b.width // 2 - s.width // 2, b.height // 2 - s.height // 2 + 10))
    d = ImageDraw.Draw(b); d.ellipse([22, 20, 42, 34], fill=(255, 255, 255, 200))
    return b
END = ESC + 0.3 + 1.5; NF = int(round(END * FPS)); print('hook bottom', HB, 'end', END)
KEYF = [int(os.environ.get('K%d' % i, -1)) for i in range(4)]
wr = Writer('v82_noaudio.mp4'); events = []; trail = []
bounce_at = {}
for (tb, b) in BOUNCES: bounce_at.setdefault(int(round(tb * FPS)), []).append(b)
for f in range(NF):
    t = f / FPS; x, y, h, nb = FR[min(f, len(FR) - 1)]
    bg = BG[int(t * 6) % len(BG)]; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    img.alpha_composite(bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)), (0, 0))
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 6, 20, 70)))
    # arena floor glow
    layer(img, lambda d: (d.ellipse([CX - R0 - 40, CY - R0 - 40, CX + R0 + 40, CY + R0 + 40], fill=(40, 28, 20, 150)), d.ellipse([CX - R0 + 10, CY - R0 + 10, CX + R0 - 10, CY + R0 - 10], fill=(70, 50, 30, 120)), d.ellipse([CX - 200, CY - 200, CX + 200, CY + 200], fill=(255, 220, 140, 22))))
    # exit gate
    ga0 = math.radians(min(GAP) * 6); ga1 = math.radians((max(GAP) + 1) * 6); gm = (ga0 + ga1) / 2
    gx, gy = CX + (R0 + 20) * math.cos(gm), CY + (R0 + 20) * math.sin(gm)
    pulse = 0.5 + 0.5 * math.sin(t * 5)
    layer(img, lambda d: d.ellipse([gx - 80, gy - 80, gx + 80, gy + 80], fill=(120, 255, 160, int(40 + 50 * pulse))))
    d = ImageDraw.Draw(img)
    # bricks: base ring + stacks
    for b in range(NB):
        if b in GAP: continue
        am = math.radians(b * 6 + 3)
        for k in range(0, h[b] + 1):
            r = R0 - k * BH
            bx, by = CX + r * math.cos(am), CY + r * math.sin(am)
            br = BR2 if (k > 0 and f - int(round([bt for bt, bb, kk in BRICKS if bb == b and kk == k][0] * FPS)) < 6) else BR
            img.alpha_composite(br, (int(bx - br.width / 2), int(by - br.height / 2)))
    # gate pillars
    for ga in (ga0 - math.radians(2), ga1 + math.radians(2)):
        for k in range(3):
            px, py = CX + (R0 + 6 + k * 18) * math.cos(ga), CY + (R0 + 6 + k * 18) * math.sin(ga)
            img.alpha_composite(BR2, (int(px - BR2.width / 2), int(py - BR2.height / 2)))
    text_layer(img, [(gx + 112, gy - 44, 'EXIT', 44, (120, 255, 150), 7, 255)])
    # gummies
    for g in GUMS:
        if t >= g['t'] and (g['got'] is None or t < g['got']):
            bob = 6 * math.sin(t * 4 + g['x']); gi = GUMI[g['k']]
            layer(img, lambda d: d.ellipse([g['x'] - 40, g['y'] - 40 + bob, g['x'] + 40, g['y'] + 40 + bob], fill=(255, 230, 150, 70)))
            img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height / 2 + bob)))
        if g['got'] is not None and abs(t - g['got']) < 0.5 / FPS: events.append((round(g['got'], 3), 'powerup_8bit'))
    # hud
    text_layer(img, [(CX, HB + 50, f'BOUNCES: {nb}', 52, (255, 255, 255), 8, 255)])   # hfg9: counter only, no plate, rule line cut
    # trail + bubble
    trail = (trail + [(x, y)])[-10:]
    layer(img, lambda d: [d.ellipse([tx - 4 - i * 2, ty - 4 - i * 2, tx + 4 + i * 2, ty + 4 + i * 2], fill=(255, 230, 140, 30 + i * 18)) for i, (tx, ty) in enumerate(trail[:-1])])
    gl = [g['got'] for g in GUMS if g['got'] is not None and g['got'] <= t]; tb_ = max(gl) if gl else -9
    if t - tb_ < 2.0 and (ESC is None or t < ESC):   # SPEED (mushroom): white speed lines behind the bubble + orange glow trail
        vx_, vy_ = x - FR[max(0, f - 2)][0], y - FR[max(0, f - 2)][1]; n_ = math.hypot(vx_, vy_) or 1; ux, uy = vx_ / n_, vy_ / n_
        layer(img, lambda d: [d.line([x - ux * (RB + 10 + 26 * q) - uy * o_, y - uy * (RB + 10 + 26 * q) + ux * o_, x - ux * (RB + 90 + 26 * q) - uy * o_, y - uy * (RB + 90 + 26 * q) + ux * o_], fill=(255, 255, 255, 210), width=6) for q, o_ in ((0, -40), (1, 0), (0, 40), (2, -20), (2, 22))])
    if ESC is None or t < ESC + 0.25:
        bb = bubble(int(t * 8)); img.alpha_composite(bb, (int(x - bb.width / 2), int(y - bb.height / 2)))
    if 0 <= t - tb_ < 0.8 and (ESC is None or t < ESC):   # SPEED! stamp rides above the bubble
        sx_ = min(max(x, 70 + 170), 887 - 170); sy_ = max(OLDHB + 170, y - RB - 110)
        layer(img, lambda d: d.rounded_rectangle([sx_ - 165, sy_ - 10, sx_ + 165, sy_ + 76], 16, fill=(14, 10, 24, 230), outline=(255, 170, 50, 255), width=5))
        text_layer(img, [(sx_, sy_ + 6, 'SPEED!', 56, (255, 170, 50), 8, 255)])
    elif t < ESC + 0.6:
        u = (t - ESC - 0.25) / 0.35
        layer(img, lambda d: [d.rectangle([x + (60 * u + 10) * math.cos(k * 0.785) - 5, y + (60 * u + 10) * math.sin(k * 0.785) - 5, x + (60 * u + 10) * math.cos(k * 0.785) + 5, y + (60 * u + 10) * math.sin(k * 0.785) + 5], fill=(220, 245, 255, int(255 * (1 - u)))) for k in range(8)])
    if f in bounce_at: events.append((round(t, 3), 'brick_8bit'))
    if ESC is not None and t >= ESC + 0.3:
        u = t - ESC - 0.3
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(140 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1130 - vf.height))
        rr = random.Random(f)
        layer(img, lambda dd: [dd.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 110, 240)]) + (255,)) for cx_, cy_ in [(rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H) for _ in range(40)]])
        text_layer(img, [(CX, 1170, 'IT ESCAPED!', 70, (120, 255, 150), 8, 255)])
        if not any(e[1] == 'victory' for e in events): events += [(round(t, 3), 'poof'), (round(t + 0.05, 3), 'powerup_8bit'), (round(t + 0.3, 3), 'victory'), (round(t + 0.4, 3), 'cheer')]
    if t < 0.35:   # GO! flash over the already-moving bubble
        text_layer(img, [(CX, CY - 50, 'GO!', 100, (255, 214, 60), 10, 255)])
        if f == 0: events.append((0.0, 'go_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in KEYF: img.convert('RGB').save(f'k82_{f}.png')
wr.close(); json.dump({'events': sorted(events)}, open('v82_ev.json', 'w')); print('done', END)
