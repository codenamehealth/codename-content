import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
OUTD = os.path.dirname(os.path.abspath(__file__))
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/wheel')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dragon_alone import dragon_alone
HOOK, HB = hook_layer2(['PAUSE IT', '3 TIMES'], accent=1, sub='Comment your combo'); print('hook bottom', HB)   # comment prompt 52px in the band from frame 0
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
DRAGON = dragon_alone(A + 'dragon.gif')   # gold-coin hoard removed (VETTING r107; a gummy pile reads as noise at wheel size, so dragon alone)
PH = [
 dict(title='YOUR GUILD', col=(255, 214, 60), bg='hub.gif', rev=1.1, opts=[
   ('FOUNDATION', jar(0), (74, 124, 58), GUM['acv']), ('ENERGY', jar(2), (217, 122, 31), GUM['mush']),
   ('RECOVERY', jar(3), (107, 45, 107), GUM['mel']), ('VITALITY', jar(1), (46, 93, 168), GUM['cre'])]),
 dict(title='YOUR OPPONENT', col=(255, 110, 90), bg='sun_hd.gif', rev=1.5, opts=[
   ('KING SLIME', fit(Image.open(S + 'pixellab/king/king2_idle/00.png').convert('RGBA'), 58), (60, 140, 70), None),
   ('THE DRAGON', fit(DRAGON, 64), (40, 90, 110), None),   # teal wedge so the red dragon reads
   ('MAGMA SLIME', fit(Image.open(S + 'fork_b10/mslime/00.png').convert('RGBA'), 64), (200, 80, 30), None),
   ('SHADOW SPIRIT', fit(Image.open(S + 'fork2/spirit/00.png').convert('RGBA'), 60), (60, 40, 90), None),
   ('BABY SLIME', fit(Image.open(S + 'pixellab/race/slime_idle_c/00.png').convert('RGBA'), 56), (90, 170, 90), None)]),
 dict(title='YOUR SIDEKICK', col=(120, 220, 255), bg='found_hd.gif', rev=1.5, opts=[
   ('JOY', fit(guide('idle_0.gif'), 62), (74, 124, 58), None), ('CYRUS', fit(guide('idle_1.gif'), 62), (217, 122, 31), None),
   ('CLEO', fit(guide('idle_3.gif'), 62), (46, 93, 168), None), ('RAYLEIGH', fit(guide('idle_2.gif'), 62), (107, 45, 107), None)]),   # sidekicks = the 4 guides only
]
def bgframes(p):
    g = Image.open(A + p); out = []; sc = H / 1080; cw = int(W / sc)
    for i in range(0, g.n_frames, 2):
        g.seek(i); fr = g.convert('RGB'); x0 = (fr.width - cw) // 2
        f = fr.crop((x0, 0, x0 + cw, 1080)).resize((W, H), Image.NEAREST)
        out.append(ImageEnhance.Brightness(f).enhance(0.5).convert('RGBA'))
    return out
BGS = [bgframes(p['bg']) for p in PH]
T_INTRO = 0.0; PDUR = 3.3; GAP = 0.0          # no intro card: wheel 1 spinning on frame 0; next wheel arrives on the same frame as its background
PSTART = [T_INTRO + i * (PDUR + GAP) for i in range(3)]
T_END = PSTART[-1] + PDUR + 0.15; END = T_END + 1.5   # end card held 1.5s, then the loop cuts to wheel 1 spinning
CX, CY, R = 159, 356, 106            # wheel centred x477 y1068, rim radius 348 (was y1047 / 360): makes room for the 52px prompt line; icons unchanged
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
KEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)
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
    spd = 2 * math.pi / P['rev']; OFF = (0.37, 0.21, 0.55)[ph]      # already at full spin on its first frame
    ang = -math.pi / 2 + spd * (min(tp, PDUR) + OFF)
    # transition scale (wheel pops in)
    pop = 1.0
    if 0 > tp > -GAP or t < PSTART[0] - GAP: pop = 0.0
    elif 0 <= tp < 0.2 and ph > 0: pop = 0.8 + 0.2 * (1 - (1 - tp / 0.2) ** 2) + 0.06 * math.sin(tp / 0.2 * math.pi)
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
    RY = HB + 10                                          # one row under the hook: 1-2-3 pips + the phase title
    if t < T_END:
        layer(img, lambda dd: dd.rounded_rectangle([80, RY - 6, 944, RY + 62], 16, fill=(14, 10, 24, 215)))
        d = ImageDraw.Draw(img)
        for i in range(3):
            px = 124 + i * 62; done = t >= PSTART[i] + PDUR; cur = i == ph
            d.ellipse([px - 28, RY, px + 28, RY + 56], fill=(255, 214, 60) if done else ((255, 255, 255) if cur else (70, 60, 90)), outline=(20, 15, 35), width=4)
            ctext(d, px, RY + 12, str(i + 1), F(32), (20, 15, 35) if (done or cur) else (160, 150, 180), 0)
        tw = d.textlength(P['title'], font=F(48)); ctext(d, 300 + tw / 2, RY + 6, P['title'], F(48), P['col'], 7)
        if pop > 0.5:
            name = P['opts'][idx][0]
            ctext(d, 478, CY * Q + (R + 10) * Q + 14, name, F(56), (255, 255, 255), 8)
            if tp >= 0 and t < PSTART[ph] + PDUR and int(t * 3) % 2 == 0:   # big flashing PAUSE NOW! stamp across the wheel (was 36px in the header)
                cy0 = CY * Q
                layer(img, lambda dd: (dd.rectangle([CX * Q - 352, cy0 - 50, CX * Q + 352, cy0 + 50], fill=(10, 8, 18, 225)),
                                       dd.line([(CX * Q - 352, cy0 - 50), (CX * Q + 352, cy0 - 50)], fill=P['col'] + (255,), width=5),
                                       dd.line([(CX * Q - 352, cy0 + 50), (CX * Q + 352, cy0 + 50)], fill=P['col'] + (255,), width=5)))
                d = ImageDraw.Draw(img); ctext(d, CX * Q, cy0 - 32, 'PAUSE NOW!', F(64), (255, 255, 255), 8)
        if t - 1 / FPS < PSTART[ph] + 0.05 <= t: ev(PSTART[ph] + 0.05, 'whoosh_8bit')   # one whoosh per new wheel (wedge ticks dropped: metronome)
    if t >= T_END:
        u = t - T_END
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(170 * min(1, u / 0.3)))))
        d = ImageDraw.Draw(img)
        bounce = 1 + 0.05 * math.sin(u * 6)
        ctext(d, 478, 640, 'WOULD YOUR', F(64), (255, 255, 255), 8)
        ctext(d, 478, 740, 'TEAM WIN?', F(int(84 * bounce)), (255, 214, 60), 9)
        ctext(d, 478, 880, 'COMMENT YOUR COMBO', F(44), (255, 255, 255), 6)
        for i, nm in enumerate(['GUILD', 'OPPONENT', 'SIDEKICK']):   # one big row per pick (labels 48px, were 24px boxes)
            py = 970 + i * 112
            d.rounded_rectangle([96, py, 860, py + 96], 16, fill=(30, 24, 44), outline=PH[i]['col'], width=5)
            d.text((130, py + 24), nm, font=F(48), fill=PH[i]['col'], stroke_width=6, stroke_fill=(20, 15, 35))
            d.rounded_rectangle([700, py + 12, 840, py + 84], 12, fill=(14, 10, 24), outline=(255, 255, 255), width=3)
            ctext(d, 770, py + 20, '?', F(56), (255, 255, 255), 6)
        if 0 <= u < 1 / FPS: ev(t, 'chime')
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open(OUTD + '/ev.json', 'w'))
print('done', round(END, 2), len(events))
