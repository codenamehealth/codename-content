import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont
OUTD = os.path.dirname(os.path.abspath(__file__))
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/shop')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['WINDOW SHOPPING,', 'RPG EDITION'], accent=1); print('hook bottom', HB)
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = S + 'npmfont/ps/package/files/PressStart2P.ttf'; A = S + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
BG0 = up(Image.open(S + 'fork_b11/gen/bg_shop_1/00.png').convert('RGBA'), 3)
DY = 350                                        # whole shop raised 350px so the Hollow's feet land at y1500 (was 1850)
BG = Image.new('RGBA', (W, H)); BG.paste(BG0.crop((0, DY, W, H)), (0, 0)); BG.paste(BG0.crop((0, H - DY, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - DY))
COUNTER_Y = 1336 - DY
FRONT = BG.crop((0, COUNTER_Y, W, H))          # counter + floor redrawn over Joy
K = 5
def gif(p):
    im = Image.open(A + p); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), K))
    return out
JIDLE = gif('idle_0.gif'); JTALK = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(S + 'fork_b5/joy_talk/*.png'))[1:9]]
HWALK = gif('hollow-walk-side.gif'); HWALKL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in HWALK]
HSTAND = up(Image.open(S + 'syeda_src/hollow/char2.png').convert('RGBA'), K)
HPOUCH = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(S + 'fork_b11/gen/hollow_pouch/*.png'))[1:9]]
FOOT = 78 * K
GUMS = {k: crop(Image.open(S + f'pixellab/gummies/pick_{k}.png').convert('RGBA')) for k in ('acv', 'mush', 'mel', 'cre', 'gold')}
FACE = None
def face(rad=44):
    im = Image.open(S + 'syeda_src/char1/char11.png').convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad, 2 * rad), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 12, 2 * rad + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 2 * rad + 11, 2 * rad + 11], fill=(20, 15, 35)); d.rectangle([4, 4, 2 * rad + 7, 2 * rad + 7], fill=(74, 124, 58))
    b.alpha_composite(head, (6, 6)); return b
FACE = face()
JX = 300; JFEET = 1420 - DY
HFEET = 1850 - DY
LINES = [(0.0, ['Welcome! Anything', 'catch your eye?']), (3.25, ['Welcome ba-']), (3.95, ['...You\'re not', 'buying anything,', 'are you?'])]   # 3 lines at 40px (was 2 at 34px)
PRE = [8, 0, 0]          # 'Welcome!' already on screen on frame 0
CPS = 26; T_OUT = 6.2; END = 6.9   # LOOP: the Hollow turns and walks out left in the last 0.7s; frame 0 has him walking back in
events = []
def ev(t, n):
    if not any(e[1] == n and abs(e[0] - t) < 0.02 for e in events): events.append((round(t, 3), n))
def hollow(t):
    if t < 0.95: u = t / 0.95; return HWALK[int(t * 10) % len(HWALK)], -120 + 760 * u
    if t < 1.3: return HSTAND, 640
    if t < 2.05: u = (t - 1.3) / 0.75; return HPOUCH[min(7, int(u * 8))], 640
    if t < 2.7: u = (t - 2.05) / 0.65; return HWALKL[int(t * 10) % len(HWALKL)], 640 - 800 * u
    if t < 3.25: u = (t - 2.7) / 0.55; return HWALK[int(t * 10) % len(HWALK)], -160 + 800 * u
    if t < T_OUT: return HSTAND, 640
    u = (t - T_OUT) / (END - T_OUT); return HWALKL[int(t * 10) % len(HWALKL)], 640 - 800 * u
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)
KEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}
jars = Image.open(A + 'jars.png').convert('RGBA')
def jar(i):
    c = jars.crop((i * 200, 0, i * 200 + 200, 200)); a = np.array(c); bg = a[0, 0, :3]
    m = (np.abs(a[:, :, :3].astype(int) - bg.astype(int)).sum(2) < 12); a[m, 3] = 0
    return crop(Image.fromarray(a).resize((50, 50), Image.NEAREST))
JARS = [jar(i) for i in range(4)]
TAGG = up(GUMS['mush'], 1)                     # price unit: gummies (no gold)
for f in range(int(END * FPS)):
    t = f / FPS
    img = BG.copy()
    # which line is active / typing
    cur = None
    for i, (t0, ls) in enumerate(LINES):
        if t >= t0: cur = i
    typing = False
    if cur is not None:
        t0, ls = LINES[cur]; full = ''.join(ls); n = PRE[cur] + int((t - t0) * CPS)
        typing = n < len(full)
        if typing and n % 4 == 0 and n > PRE[cur]: ev(t, 'tick_8bit')
    # Joy behind the counter
    jf = JTALK[int(t * 10) % len(JTALK)] if typing else JIDLE[int(t * 6) % len(JIDLE)]
    img.alpha_composite(jf, (int(JX - jf.width / 2), int(JFEET - FOOT)))
    img.alpha_composite(FRONT, (0, COUNTER_Y))
    # gummy display on the counter with price tags
    d = ImageDraw.Draw(img)
    items = [(0, '99'), (2, '99'), (1, '999'), (3, '99'), (0, '99')]
    for i, (k, p) in enumerate(items):
        gx = 440 + i * 118; g = up(JARS[k], 2 if p != '999' else 3); gy = COUNTER_Y - g.height + 6
        if i == 4: g = up(JARS[3].transpose(Image.FLIP_LEFT_RIGHT), 2)
        if p == '999':
            layer(img, lambda dd: [dd.ellipse([gx - r, gy + g.height / 2 - r, gx + r, gy + g.height / 2 + r], fill=(255, 220, 90, a)) for r, a in ((70, 40), (50, 60))])
            for q in range(3):
                a = t * 3 + q * 2.1; sx, sy = gx + 50 * math.cos(a), gy + 30 + 30 * math.sin(a)
                ImageDraw.Draw(img).rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 245, 190))
        img.alpha_composite(g, (int(gx - g.width / 2), int(gy)))
        d = ImageDraw.Draw(img)
        tw = d.textlength(p, font=F(28)) + 4 + TAGG.width; x0 = gx - tw / 2      # price tags 28px (were 20px)
        d.rectangle([x0 - 7, COUNTER_Y + 10, x0 + tw + 7, COUNTER_Y + 52], fill=(240, 226, 190), outline=(60, 40, 20), width=3)
        d.text((x0, COUNTER_Y + 17), p, font=F(28), fill=(120, 40, 30))
        img.alpha_composite(TAGG, (int(x0 + tw - TAGG.width), COUNTER_Y + 18)); d = ImageDraw.Draw(img)
    # the Hollow (customer) in front of the counter
    sp, hx = hollow(t)
    layer(img, lambda dd: dd.ellipse([hx - 70, HFEET - 14, hx + 70, HFEET + 12], fill=(0, 0, 0, 90)))
    img.alpha_composite(sp, (int(hx - sp.width / 2), int(HFEET - FOOT)))
    if f == 0 or (t - 1 / FPS < 2.7 <= t): ev(t, 'chime')
    # 3 gold reveal
    if 1.75 <= t < 2.85:
        u = t - 1.75; d = ImageDraw.Draw(img)
        # the 3 gummies pop out of the pouch beside him (fixed spot, inside the safe zone), '3 GUMMIES' held 1.1s (was 0.55s, slid off the left edge)
        if t < 2.3:
            for q, gk in enumerate(('mush', 'acv', 'mel')):
                gg = up(GUMS[gk], 3) if gk != 'mel' else up(GUMS[gk], 2)
                cx, cy = 330 + q * 90, 1268 - min(1, u / 0.15) * 30 - (10 if q == 1 else 0)
                img.alpha_composite(gg, (int(cx - gg.width / 2), int(cy - gg.height / 2)))
        layer(img, lambda dd: ctext(dd, 420, 1150, '3 GUMMIES', F(44), (255, 214, 60), 7, int(255 * min(1, (2.85 - t) / 0.15))))
        ev(1.75, 'coin_8bit')
    # sweat drop on the last line
    if t >= LINES[2][0] + 0.6:
        d = ImageDraw.Draw(img); u = (t - LINES[2][0] - 0.6); dy = (u * 40) % 30
        sx, sy = hx + 75, HFEET - FOOT + 110 + dy * 0.6
        d.polygon([(sx, sy - 44), (sx - 22, sy), (sx + 22, sy)], fill=(140, 200, 255), outline=(20, 15, 35)); d.ellipse([sx - 22, sy - 18, sx + 22, sy + 26], fill=(140, 200, 255), outline=(20, 15, 35), width=4)
        d.ellipse([sx - 10, sy - 8, sx - 2, sy], fill=(230, 245, 255))
        if 0 <= u < 1 / FPS: ev(t, 'boing')
    # header
    # dialogue box
    if cur is not None:
        t0, ls = LINES[cur]
        n = PRE[cur] + int((t - t0) * CPS)
        bx0, by0, bx1, by1 = 76, HB + 14, 1004, HB + 254
        layer(img, lambda dd: dd.rectangle([bx0, by0, bx1, by1], fill=(18, 16, 48, 235)))
        d = ImageDraw.Draw(img)
        d.rectangle([bx0, by0, bx1, by1], outline=(255, 255, 255), width=6); d.rectangle([bx0 + 10, by0 + 10, bx1 - 10, by1 - 10], outline=(110, 110, 170), width=3)
        img.alpha_composite(FACE, (bx0 + 30, by0 + 40)); d = ImageDraw.Draw(img)
        d.rectangle([bx0 + 30, by0 + 150, bx0 + 30 + FACE.width, by0 + 196], fill=(74, 124, 58), outline=(20, 15, 35), width=4)
        tw = d.textlength('JOY', font=F(28)); d.text((bx0 + 30 + FACE.width / 2 - tw / 2, by0 + 159), 'JOY', font=F(28), fill=(255, 255, 255))
        k0 = 0
        for j, ln in enumerate(ls):
            d.text((bx0 + 170, by0 + 36 + j * 60), ln[:max(0, n - k0)], font=F(40), fill=(255, 255, 255)); k0 += len(ln)
        if not typing and int(t * 3) % 2 == 0 and cur != 1:
            d.polygon([(bx1 - 60, by1 - 50), (bx1 - 36, by1 - 50), (bx1 - 48, by1 - 34)], fill=(255, 214, 60))
    # comment prompt from 0.3s on its own plate, right under the potions it points at
    if t >= 0.3:
        pa = int(255 * min(1, (t - 0.3) / 0.15))
        layer(img, lambda dd: (dd.rounded_rectangle([96, COUNTER_Y + 60, 984, COUNTER_Y + 124], 14, fill=(14, 10, 24, int(pa * 0.9)), outline=(255, 214, 60, pa), width=4),
                               ctext(dd, 540, COUNTER_Y + 70, 'WHICH WOULD YOU BUY?', F(44), (255, 255, 255), 6, pa)))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open(OUTD + '/ev.json', 'w')); print('done', END, len(events))
