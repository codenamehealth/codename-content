import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #82 safe-zone + hook pass (source: fork_b8/r84.py): arena scaled to fit the zone (R0 420 -> 360, bricks 1.5x -> 1.25x),
# exit gap moved from the left (bins 25-27) to the upper right so the escape happens inside the zone, Hollow 1.7x -> 2x (integer) in a slightly bigger bubble.
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
HOOK, HB = hook_layer(['CAN THE HOLLOW', 'ESCAPE?'], accent=1, sub='EVERY BOUNCE ADDS A BRICK')
CX, CY = 478, 1068; R0 = 360; NB = 60; BH = 28; RB = 64
GAP = set(range(50, 53))            # bins (6 deg each) forming the exit gap, upper right (300-318 deg)
BR = up(crop(Image.open(B8 + 'brick/03.png').convert('RGBA')), 1.25)
BR2 = ImageEnhance.Brightness(BR).enhance(1.25)
SPD0 = float(os.environ.get('SP', '550'))
def bin_of(a): return int((math.degrees(a) % 360) // (360 / NB))
def sim(seed, dur=46):
    rnd = random.Random(seed)
    x, y = CX + rnd.uniform(-60, 60), CY + rnd.uniform(-60, 60)
    a = rnd.uniform(0, 6.283); vx, vy = math.cos(a) * SPD0, math.sin(a) * SPD0
    h = [0] * NB; bricks = []; bounces = []; frames = []; esc = None; gums = []; got = []
    spawn_t = 4.0; boost = -9; kinds = ['mush', 'acv', 'mel', 'cre']
    f = 0
    while f < dur * FPS:
        t = f / FPS
        if t >= 1.5 and esc is None:
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
                gums.append(dict(x=CX + gr * math.cos(ga), y=CY + gr * math.sin(ga), k=kinds[len(gums) % 4], t=t, got=None)); spawn_t = t + 6.0
            for g in gums:
                if g['got'] is None and math.hypot(g['x'] - x, g['y'] - y) < RB + 20: g['got'] = t; boost = t
        if esc is not None:
            vy += 900 / FPS; x += vx / FPS * 0.35; y += vy / FPS * 0.35  # slower drift after the escape so the bubble pops below the hook
        frames.append((x, y, list(h), len(bounces)))
        f += 1
        if esc is not None and t > esc + 4.0: break
    return frames, bricks, bounces, esc, gums
if sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        fr, br, bo, esc, gums = sim(s)
        if esc and 28 < esc < 38 and len(bo) > 50 and sum(1 for g in gums if g['got']) >= 3: print(os.environ.get('SP'), s, round(esc, 1), len(bo), sum(1 for g in gums if g['got']), flush=True)
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
END = (ESC or 40) + 4.0; NF = int(END * FPS)
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
    text_layer(img, [(min(940, gx + 60), gy - 110, 'EXIT', 36, (120, 255, 150), 6, 255)])
    # gummies
    for g in GUMS:
        if t >= g['t'] and (g['got'] is None or t < g['got']):
            bob = 6 * math.sin(t * 4 + g['x']); gi = GUMI[g['k']]
            layer(img, lambda d: d.ellipse([g['x'] - 40, g['y'] - 40 + bob, g['x'] + 40, g['y'] + 40 + bob], fill=(255, 230, 150, 70)))
            img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height / 2 + bob)))
        if g['got'] is not None and 0 <= t - g['got'] < 1.0:
            u = t - g['got']; text_layer(img, [(g['x'], g['y'] - 70 - u * 50, 'SPEED UP!', 28, (255, 214, 60), 5, int(255 * (1 - u)))])
            if abs(t - g['got']) < 0.5 / FPS: events.append((round(g['got'], 3), 'coin_8bit'))
    # trail + bubble
    trail = (trail + [(x, y)])[-10:]
    layer(img, lambda d: [d.ellipse([tx - 4 - i * 2, ty - 4 - i * 2, tx + 4 + i * 2, ty + 4 + i * 2], fill=(255, 230, 140, 30 + i * 18)) for i, (tx, ty) in enumerate(trail[:-1])])
    if ESC is None or t < ESC + 0.25:
        bb = bubble(int(t * 8)); img.alpha_composite(bb, (int(x - bb.width / 2), int(y - bb.height / 2)))
    elif t < ESC + 0.6:
        u = (t - ESC - 0.25) / 0.35
        layer(img, lambda d: [d.rectangle([x + (60 * u + 10) * math.cos(k * 0.785) - 5, y + (60 * u + 10) * math.sin(k * 0.785) - 5, x + (60 * u + 10) * math.cos(k * 0.785) + 5, y + (60 * u + 10) * math.sin(k * 0.785) + 5], fill=(220, 245, 255, int(255 * (1 - u)))) for k in range(8)])
    if f in bounce_at: events.append((round(t, 3), 'brick_8bit'))
    # hud
    layer(img, lambda d: d.rounded_rectangle([CX - 230, HB + 12, CX + 230, HB + 82], 16, fill=(14, 8, 26, 210)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([CX - 230, HB + 12, CX + 230, HB + 82], 16, outline=(255, 214, 60), width=4)
    ctext(d, CX, HB + 27, f'BOUNCES: {nb}', F(40), (255, 255, 255), 5)
    if ESC is not None and t >= ESC + 0.3:
        u = t - ESC - 0.3
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(140 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1130 - vf.height))
        rr = random.Random(f)
        layer(img, lambda dd: [dd.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 110, 240)]) + (255,)) for cx_, cy_ in [(rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H) for _ in range(40)]])
        text_layer(img, [(CX, 1170, 'IT ESCAPED!', 70, (120, 255, 150), 8, 255), (CX, 1280, f'after {nb} bounces', 34, (255, 255, 255), 6, 255),
                         (CX, 1350, 'Did you think it would?', 30, (255, 214, 60), 5, int(255 * min(1, max(0, u - 0.8) / 0.4)))])
        if not any(e[1] == 'victory' for e in events): events += [(round(t, 3), 'poof'), (round(t + 0.05, 3), 'powerup_8bit'), (round(t + 0.3, 3), 'victory'), (round(t + 0.4, 3), 'cheer')]
    if t < 1.5:
        text_layer(img, [(CX, CY - 50, 'GO!', 100, (255, 214, 60), 10, int(255 * min(1, (1.5 - t) / 0.5)))])
        if f == 0: events.append((0.2, 'go_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(f'p82_{f:04d}.png')
wr.close(); json.dump(events, open('v82_ev.json', 'w')); print('done', END)
