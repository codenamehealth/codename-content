import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = S + 'npmfont/ps/package/files/PressStart2P.ttf'; A = S + 'pause/assets/'
W, H, FPS = 1080, 1920, 30; Q = 3; LW, LH = W // Q, H // Q
def F(s): return ImageFont.truetype(FONT, s)
def crop(im): return im.crop(im.getbbox())
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
def fit(im, m):
    im = crop(im); k = m / max(im.size)
    if k >= 1: k = int(k)
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.NEAREST)
def g0(p):
    im = Image.open(p); im.seek(0); return im.convert('RGBA')
def guide(n):  # Syeda idle frame at native 92
    return g0(A + n).resize((92, 92), Image.NEAREST)
jars = Image.open(A + 'jars.png').convert('RGBA')
def jar(i):
    c = jars.crop((i * 200, 0, i * 200 + 200, 200)); a = np.array(c); bg = a[0, 0, :3]
    m = (np.abs(a[:, :, :3].astype(int) - bg.astype(int)).sum(2) < 12); a[m, 3] = 0
    return fit(Image.fromarray(a).resize((50, 50), Image.NEAREST), 54)
GUM = {k: crop(Image.open(S + f'pixellab/gummies/pick_{k}.png').convert('RGBA')) for k in ('acv', 'mush', 'mel', 'cre', 'gold')}
PH = [
 dict(title='YOUR GUILD', col=(255, 214, 60), bg='hub.gif', rev=1.1, opts=[
   ('FOUNDATION', jar(0), (74, 124, 58), GUM['acv']), ('ENERGY', jar(2), (217, 122, 31), GUM['mush']),
   ('RECOVERY', jar(3), (107, 45, 107), GUM['mel']), ('VITALITY', jar(1), (46, 93, 168), GUM['cre'])]),
 dict(title='YOUR OPPONENT', col=(255, 110, 90), bg='sun_hd.gif', rev=1.5, opts=[
   ('KING SLIME', fit(Image.open(S + 'pixellab/king/king2_idle/00.png').convert('RGBA'), 58), (60, 140, 70), None),
   ('THE DRAGON', fit(g0(A + 'dragon.gif').resize((128, 128), Image.NEAREST), 64), (150, 40, 40), None),
   ('MAGMA SLIME', fit(Image.open(S + 'fork_b10/mslime/00.png').convert('RGBA'), 64), (200, 80, 30), None),
   ('THE HOLLOW', fit(guide('idle_9.gif'), 60), (70, 60, 100), None),
   ('SHADOW SPIRIT', fit(Image.open(S + 'fork2/spirit/00.png').convert('RGBA'), 60), (60, 40, 90), None),
   ('BABY SLIME', fit(Image.open(S + 'pixellab/race/slime_idle_c/00.png').convert('RGBA'), 56), (90, 170, 90), None)]),
 dict(title='YOUR SIDEKICK', col=(120, 220, 255), bg='found_hd.gif', rev=1.5, opts=[
   ('JOY', fit(guide('idle_0.gif'), 62), (74, 124, 58), None), ('CYRUS', fit(guide('idle_1.gif'), 62), (217, 122, 31), None),
   ('CLEO', fit(guide('idle_3.gif'), 62), (46, 93, 168), None), ('RAYLEIGH', fit(guide('idle_2.gif'), 62), (107, 45, 107), None),
   ('THE HOLLOW', fit(guide('idle_9.gif'), 62), (70, 60, 100), None), ('THE DRAGON', fit(g0(A + 'dragon.gif').resize((128, 128), Image.NEAREST), 64), (150, 40, 40), None)]),
]
def bgframes(p):
    g = Image.open(A + p); out = []; sc = H / 1080; cw = int(W / sc)
    for i in range(0, g.n_frames, 2):
        g.seek(i); fr = g.convert('RGB'); x0 = (fr.width - cw) // 2
        f = fr.crop((x0, 0, x0 + cw, 1080)).resize((W, H), Image.NEAREST)
        out.append(ImageEnhance.Brightness(f).enhance(0.5).convert('RGBA'))
    return out
BGS = [bgframes(p['bg']) for p in PH]
T_INTRO = 0.9; PDUR = 3.2; GAP = 0.35
PSTART = [T_INTRO + i * (PDUR + GAP) for i in range(3)]
T_END = PSTART[-1] + PDUR + 0.2; END = T_END + 2.6
CX, CY, R = LW // 2, 300, 148
events = []
def ev(t, n):
    if not any(e[1] == n and abs(e[0] - t) < 0.02 for e in events): events.append((round(t, 3), n))
def draw_wheel(L, opts, ang, t):
    d = ImageDraw.Draw(L); n = len(opts); step = 2 * math.pi / n
    # shadow + rim
    d.ellipse([CX - R - 12, CY - R - 8, CX + R + 12, CY + R + 16], fill=(10, 8, 16, 160))
    d.ellipse([CX - R - 10, CY - R - 10, CX + R + 10, CY + R + 10], fill=(122, 78, 20, 255))
    d.ellipse([CX - R - 7, CY - R - 7, CX + R + 7, CY + R + 7], fill=(236, 186, 60, 255))
    d.ellipse([CX - R - 2, CY - R - 2, CX + R + 2, CY + R + 2], fill=(90, 55, 15, 255))
    for i, (name, ic, col, gm) in enumerate(opts):
        a0 = ang + i * step - step / 2
        pts = [(CX, CY)] + [(CX + R * math.cos(a0 + step * j / 24), CY + R * math.sin(a0 + step * j / 24)) for j in range(25)]
        c2 = tuple(min(255, int(v * 1.25 + 20)) for v in col) if i % 2 else col
        d.polygon(pts, fill=c2 + (255,))
        # inner light band
        pts2 = [(CX + (R - 10) * math.cos(a0 + step * j / 24), CY + (R - 10) * math.sin(a0 + step * j / 24)) for j in range(25)]
        d.line(pts2, fill=tuple(min(255, v + 60) for v in c2) + (255,), width=2)
    for i in range(n):
        a0 = ang + i * step - step / 2
        d.line([(CX, CY), (CX + R * math.cos(a0), CY + R * math.sin(a0))], fill=(250, 220, 120, 255), width=3)
    # bulbs
    for j in range(24):
        a = j * 2 * math.pi / 24; on = (j + int(t * 10)) % 3 == 0
        bx, by = CX + (R + 5) * math.cos(a), CY + (R + 5) * math.sin(a)
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 250, 200, 255) if on else (170, 120, 40, 255))
    for i, (name, ic, col, gm) in enumerate(opts):
        a = ang + i * step; rr = R * 0.62
        ix, iy = CX + rr * math.cos(a), CY + rr * math.sin(a)
        L.alpha_composite(ic, (int(ix - ic.width / 2), int(iy - ic.height / 2)))
        if gm is not None:
            L.alpha_composite(gm, (int(ix + ic.width / 2 - 8), int(iy + ic.height / 2 - gm.height)))
    # hub
    d.ellipse([CX - 20, CY - 20, CX + 20, CY + 20], fill=(122, 78, 20, 255)); d.ellipse([CX - 16, CY - 16, CX + 16, CY + 16], fill=(236, 186, 60, 255))
    d.ellipse([CX - 9, CY - 9, CX + 9, CY + 9], fill=(200, 60, 80, 255)); d.ellipse([CX - 6, CY - 7, CX - 2, CY - 3], fill=(255, 200, 210, 255))
    # pointer at top
    py = CY - R - 16
    d.polygon([(CX - 16, py - 10), (CX + 16, py - 10), (CX, py + 20)], fill=(90, 55, 15, 255))
    d.polygon([(CX - 12, py - 7), (CX + 12, py - 7), (CX, py + 15)], fill=(255, 220, 90, 255))
    d.ellipse([CX - 5, py - 6, CX + 5, py + 4], fill=(120, 220, 255, 255))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'wheel_noaudio.mp4'], stdin=subprocess.PIPE)
NF = int(END * FPS); last_idx = None
rnd = random.Random(3); sparks = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0, 6.3)) for _ in range(30)]
for f in range(NF):
    t = f / FPS
    ph = 0
    for i in range(3):
        if t >= PSTART[i] - GAP: ph = i
    P = PH[ph]; bgl = BGS[ph]
    img = bgl[int(t * 6) % len(bgl)].copy()
    layer(img, lambda dd: [dd.rectangle([sx, (sy - t * 30) % H, sx + 5, (sy - t * 30) % H + 5], fill=(255, 236, 170, int(90 + 80 * math.sin(t * 3 + p)))) for sx, sy, p in sparks])
    L = Image.new('RGBA', (LW, LH), (0, 0, 0, 0))
    n = len(P['opts']); step = 2 * math.pi / n
    tp = t - PSTART[ph]
    if t < PSTART[0]: ang = -math.pi / 2
    else:
        spd = 2 * math.pi / P['rev']; ramp = min(1, max(0, tp) / 0.35)
        ang = -math.pi / 2 + spd * (max(0, tp) - 0.35 / 2 * (1 - ramp) * ramp if tp < 0.35 else max(0, tp) - 0.175)
        if t > PSTART[ph] + PDUR: ang = -math.pi / 2 + spd * (PDUR - 0.175)
    # transition scale (wheel pops in)
    pop = 1.0
    if 0 > tp > -GAP: pop = 0.0
    elif 0 <= tp < 0.25: pop = 0.6 + 0.4 * (1 - (1 - tp / 0.25) ** 2) + 0.08 * math.sin(tp / 0.25 * math.pi)
    draw_wheel(L, P['opts'], ang, t)
    big = L.resize((W, H), Image.NEAREST)
    if pop != 1.0 and pop > 0:
        sw, sh = int(W * pop), int(H * pop); big = big.resize((sw, sh), Image.NEAREST)
        cxp, cyp = CX * Q, CY * Q; tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        tmp.alpha_composite(big, (int(cxp - cxp * pop), int(cyp - cyp * pop))); big = tmp
    if pop > 0 and t < T_END: img.alpha_composite(big)
    # option under the pointer
    rel = ((-math.pi / 2 - ang) % (2 * math.pi)); idx = int((rel + step / 2) // step) % n
    d = ImageDraw.Draw(img)
    # header
    layer(img, lambda dd: dd.rectangle([0, 0, W, 300], fill=(14, 10, 24, 150)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 40, 'PAUSE IT 3 TIMES', F(48), (255, 255, 255), 7)
    for i in range(3):
        px = W / 2 + (i - 1) * 110; done = t >= PSTART[i] + PDUR; cur = i == ph and t < T_END
        d.ellipse([px - 34, 118, px + 34, 186], fill=(255, 214, 60) if done else ((255, 255, 255) if cur else (70, 60, 90)), outline=(20, 15, 35), width=5)
        ctext(d, px, 136, str(i + 1), F(30), (20, 15, 35) if (done or cur) else (160, 150, 180), 0)
    if PSTART[0] - GAP <= t < T_END:
        ctext(d, W / 2, 220, P['title'], F(56), P['col'], 8)
        if pop > 0.5:
            name = P['opts'][idx][0]
            ctext(d, W / 2, CY * Q + R * Q + 110, name, F(60), (255, 255, 255), 8)
            if tp >= 0 and t < PSTART[ph] + PDUR and int(t * 3) % 2 == 0:
                tw = d.textlength('PAUSE NOW!', font=F(40)); bx, by = W / 2 - (tw + 80) / 2, 1640
                d.rectangle([bx, by, bx + 18, by + 52], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                d.rectangle([bx + 30, by, bx + 48, by + 52], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                ctext(d, bx + 80 + tw / 2, by + 6, 'PAUSE NOW!', F(40), (255, 255, 255), 6)
        if idx != last_idx and PSTART[ph] <= t < PSTART[ph] + PDUR: ev(t, 'tick_8bit')
        last_idx = idx
        if abs(t - (PSTART[ph] - GAP + 0.05)) < 0.5 / FPS: ev(t, 'whoosh_8bit')
    if t < PSTART[0] - GAP + 0.05:
        ctext(d, W / 2, 1420, '1. GUILD', F(48), (255, 214, 60), 7); ctext(d, W / 2, 1510, '2. OPPONENT', F(48), (255, 110, 90), 7); ctext(d, W / 2, 1600, '3. SIDEKICK', F(48), (120, 220, 255), 7)
    if t >= T_END:
        u = t - T_END
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(170 * min(1, u / 0.3)))))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, 620, 'DID YOU', F(64), (255, 255, 255), 8)
        bounce = 1 + 0.06 * math.sin(u * 6)
        ctext(d, W / 2, 740, 'WIN', F(int(96 * bounce)), (255, 214, 60), 9)
        ctext(d, W / 2, 880, 'OR', F(48), (255, 255, 255), 7)
        ctext(d, W / 2, 970, 'LOSE?', F(int(96 * bounce)), (255, 110, 90), 9)
        ctext(d, W / 2, 1200, 'Comment your combo', F(40), (255, 255, 255), 6)
        for i, nm in enumerate(['GUILD', 'OPPONENT', 'SIDEKICK']):
            px = W / 2 + (i - 1) * 320; py = 1360
            d.rounded_rectangle([px - 140, py, px + 140, py + 150], 16, fill=(30, 24, 44), outline=PH[i]['col'], width=5)
            ctext(d, px, py + 22, nm, F(24), PH[i]['col'], 4); ctext(d, px, py + 70, '?', F(56), (255, 255, 255), 6)
        if abs(u) < 0.5 / FPS: ev(t, 'chime')
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('wheel_events.json', 'w'))
print('done', round(END, 2), len(events))
