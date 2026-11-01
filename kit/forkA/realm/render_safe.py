import math, random, json, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30; K = 4
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
def gif92(p):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), K))
    return fr
def pngs(d, lo=1): return [up(Image.open(f).convert('RGBA'), K) for f in sorted(glob.glob(d + '/*.png'))[lo:]]
REALMS = [
 dict(name='THE VILLAGE', sub='Every journey starts here', bg='hub.gif', walk=gif92('hollow-walk-side.gif'), idle=gif92('idle_9.gif'), gum='gold', feet=1470, part=(255, 230, 160), wfps=8),
 dict(name='THORNBERRY FOREST', sub="Joy's realm", bg='found_hd.gif', walk=gif92('joy-walk-side.gif'), idle=gif92('idle_0.gif'), gum='acv', feet=1470, part=(200, 255, 140), wfps=8),
 dict(name='THE SUN TEMPLE', sub="Cyrus's realm", bg='sun_hd.gif', walk=gif92('cyrus-walk-side.gif'), idle=gif92('idle_8.gif'), gum='mush', feet=1470, part=(255, 220, 120), wfps=8),
 dict(name='THE MOON TEMPLE', sub="Rayleigh's realm", bg='recov_hd.gif', walk=pngs(P + 'race/ray_run'), idle=gif92('idle_6.gif'), gum='mel', feet=1470, part=(170, 200, 255), wfps=10),
 dict(name='THE CASTLE', sub="Cleo's realm", bg='vit_hd.gif', walk=pngs(P + 'cleo/walk_mm'), idle=gif92('idle_7.gif'), gum='cre', feet=1470, part=(255, 255, 255), wfps=10)]
for r in REALMS:
    g = Image.open(A + r['bg']); r['src'] = []
    for i in range(0, g.n_frames, 2): g.seek(i); r['src'].append(g.convert('RGB'))
    r['gimg'] = up(Image.open(P + f'gummies/pick_{r["gum"]}.png').convert('RGBA'), 4)
SEG = 3.3; TR = 0.3; INTRO = 0.0; END_CARD = 3.0
TOTAL = len(REALMS) * SEG + END_CARD
sc = H / 1080; cw = W / sc
def bgframe(r, t, u):
    src = r['src'][int(t * 6) % len(r['src'])]
    x0 = 960 - cw / 2 - 30 + 60 * u
    return src.crop((int(x0), 0, int(x0 + cw), 1080)).resize((W, H), Image.NEAREST).convert('RGBA')
def scene(i, t, u):
    r = REALMS[i]; img = bgframe(r, t, u)
    # particles
    def parts(dd):
        rr = random.Random(i * 7)
        for q in range(26):
            px = rr.uniform(0, W); sp = rr.uniform(30, 90); ph = rr.uniform(0, 6.28)
            py = (rr.uniform(0, H) - t * sp) % H if i != 0 else (rr.uniform(0, H) + t * sp * 0.5) % H
            px += 30 * math.sin(t * 1.3 + ph); s = rr.choice([4, 6, 8]); a = int(150 + 100 * math.sin(t * 3 + ph))
            dd.rectangle([px, py, px + s, py + s], fill=r['part'] + (max(0, a),))
    layer(img, parts)
    # gummy treasure floating with glow
    gx, gy = 760, r['feet'] - 360 + 16 * math.sin(t * 2.4)
    def glow(dd):
        for rad, al in ((120, 35), (85, 55), (55, 80)):
            dd.ellipse([gx - rad, gy - rad, gx + rad, gy + rad], fill=(255, 235, 170, al))
        for k in range(5):
            a = t * 2 + k * 1.256; sx, sy = gx + 95 * math.cos(a), gy + 60 * math.sin(a)
            dd.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 250, 210, 230))
    layer(img, glow)
    gi = r['gimg']; img.alpha_composite(gi, (int(gx - gi.width / 2), int(gy - gi.height / 2)))
    # guide walks in, then idles facing us
    walk_end = 1.8
    if u * SEG < walk_end:
        p = (u * SEG) / walk_end; x = -200 + p * 520
        fr = r['walk'][int(t * r['wfps']) % len(r['walk'])]
    else:
        x = 320; fr = r['idle'][int(t * 8) % len(r['idle'])]
    layer(img, lambda dd: dd.ellipse([x + 46 * K - 70, r['feet'] - 12, x + 46 * K + 70, r['feet'] + 12], fill=(0, 0, 0, 70)))
    img.alpha_composite(fr, (int(x), int(r['feet'] - 78 * K)))
    # header + realm banner
    layer(img, lambda dd: (dd.rectangle([0, 250, W, 452], fill=(12, 8, 22, 150)), dd.rounded_rectangle([80, 470, W - 80, 630], 20, fill=(12, 8, 22, 200))))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 268, 'CHOOSE YOUR', F(64)); ctext(d, W / 2, 352, 'REALM', F(80), (255, 214, 60), 8)
    a = int(255 * min(1, u * SEG / 0.35))
    PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
    ctext(pd, W / 2 + 50, 492, r['name'], F(44 if len(r['name']) < 14 else 36), (255, 255, 255), 6, a)
    ctext(pd, W / 2 + 50, 562, r['sub'], F(26), (255, 214, 60), 4, a)
    pd.ellipse([104, 500, 204, 600], fill=(255, 214, 60, a), outline=(20, 15, 35, a), width=6)
    ctext(pd, 156, 530, str(i + 1), F(46), (20, 15, 35), 0, a)
    img.alpha_composite(PL)
    return img
THUMBS = None
def endcard(t, u):
    global THUMBS
    if THUMBS is None:
        THUMBS = []
        for i, r in enumerate(REALMS):
            THUMBS.append(bgframe(r, 1.0, 0.5).resize((270, 480), Image.NEAREST))
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    pos = [(90, 420), (405, 420), (720, 420), (247, 940), (562, 940)]
    for i, (x, y) in enumerate(pos):
        th = THUMBS[i].copy(); r = REALMS[i]
        th.alpha_composite(r['gimg'], (135 - r['gimg'].width // 2, 260 - r['gimg'].height // 2))
        pop = min(1, max(0, (u * END_CARD - i * 0.12) / 0.25))
        if pop <= 0: continue
        if pop < 1: th = th.resize((max(1, int(270 * pop)), max(1, int(480 * pop))), Image.NEAREST)
        img.alpha_composite(th, (int(x + 135 - th.width / 2), int(y + 240 - th.height / 2)))
        if pop >= 1:
            d = ImageDraw.Draw(img); d.rectangle([x - 4, y - 4, x + 274, y + 484], outline=(255, 214, 60), width=6)
            d.ellipse([x + 95, y + 395, x + 175, y + 475], fill=(255, 214, 60), outline=(20, 15, 35), width=5)
            ctext(d, x + 135, y + 416, str(i + 1), F(38), (20, 15, 35), 0)
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 268, 'WHICH ONE IS YOURS?', F(46)); ctext(d, W / 2, 344, 'Comment 1 to 5', F(36), (255, 214, 60), 5)
    return img
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'realm_safe_noaudio.mp4'], stdin=subprocess.PIPE)
ev = []
rng = random.Random(3); BLK = 60
order = [(bx, by) for by in range(0, H, BLK) for bx in range(0, W, BLK)]; rng.shuffle(order)
for f in range(int(TOTAL * FPS)):
    t = f / FPS; i = int(t // SEG)
    if i < len(REALMS):
        u = (t - i * SEG) / SEG; img = scene(i, t, u)
        # pixel-block transition into the next realm / end card
        tl = (i + 1) * SEG - t
        if tl < TR:
            nxt = scene(i + 1, t, 0.0) if i + 1 < len(REALMS) else endcard(t, 0.0)
            n = int(len(order) * (1 - tl / TR))
            m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
            for bx, by in order[:n]: md.rectangle([bx, by, bx + BLK - 1, by + BLK - 1], fill=255)
            img.paste(nxt, (0, 0), m)
    else:
        img = endcard(t, (t - len(REALMS) * SEG) / END_CARD)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p_{f:04d}.png')
ff.stdin.close(); ff.wait()
for i in range(len(REALMS)): ev.append((round(i * SEG + 0.05, 3), 'swish' if i else 'chime')); ev.append((round(i * SEG + 0.5, 3), 'twinkle'))
ev.append((round(len(REALMS) * SEG, 3), 'swish'))
for i in range(5): ev.append((round(len(REALMS) * SEG + i * 0.12 + 0.2, 3), 'coin_8bit'))
json.dump({'events': ev}, open('realm_safe_events.json', 'w')); print('done', TOTAL)
