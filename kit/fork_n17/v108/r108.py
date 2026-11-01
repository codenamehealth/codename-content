import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
OUTD = os.path.dirname(os.path.abspath(__file__))
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/shop')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
from hook import hook_fade
HOOK, HB = hook_fade(['WILL HE BUY', 'ANYTHING?'], accent=1, size=72); print('hook bottom', HB)   # n17: job hook (watch the customer)
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
BG = BG.filter(ImageFilter.GaussianBlur(3.2)); BG = ImageEnhance.Color(BG).enhance(0.72); BG = ImageEnhance.Brightness(BG).enhance(0.66)   # n17: calmer shop
_v = np.zeros((H, W), np.float32); _yy, _xx = np.mgrid[0:H, 0:W]; _r = np.sqrt(((_xx - 540) / 700.0) ** 2 + ((_yy - 1150) / 1000.0) ** 2)
_va = (np.clip((_r - 0.55) / 0.6, 0, 1) * 150).astype(np.uint8); VIG = Image.new('RGBA', (W, H), (8, 6, 16, 255)); VIG.putalpha(Image.fromarray(_va)); BG.alpha_composite(VIG)
FRONT = BG.crop((0, COUNTER_Y, W, H))          # counter + floor redrawn over Joy
K = 5
def gif(p):
    im = Image.open(A + p); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), K))
    return out
JIDLE = gif('idle_0.gif'); JTALK = gif('../../fork_c4/talk/joy-talk.gif')   # n17: Syeda's own joy-talk.gif (no teeth), same 920 canvas as idle_0
HWALK = gif('hollow-walk-side.gif'); HWALKL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in HWALK]
HIDLE = gif('idle_9.gif')
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
T_SKIP, T_SKIP1 = 2.1, 2.95                     # n17: '3 HOURS LATER...' card
LINES = [(0.0, ['Welcome! Anything', 'catch your eye?']), (T_SKIP1 + 0.1, ['...You\'re not', 'buying anything,', 'are you?'])]
PRE = [8, 0]
CPS = 26; T_POUCH = 4.85; T_CY = 6.25; T_GIVE = 7.15; GFPS = 14; G0, G1 = 11, 54; END = 11.0
BOX_OFF = T_CY                                   # dialogue box fades out as Cyrus walks in
GIVE = []
_g = Image.open(A + 'cyrus-giving-gummy.gif')
for i in range(_g.n_frames): _g.seek(i); GIVE.append(up(_g.convert('RGBA').resize((113, 88), Image.NEAREST), K))
GHX, GFY = 795 // 2, 879 // 2                    # Hollow centre x / feet y inside the scaled gif
CWALK = gif('cyrus-walk-side.gif'); CYX = 640 - 210   # Cyrus stands 42 art px left of the Hollow, as in Syeda's gif
def gidx(t):
    k = int((t - T_GIVE) * GFPS) + G0
    if k > G1: k = 45 + (k - 45) % (G1 - 45 + 1)   # keep the arms-up celebration looping
    return k
events = []
def ev(t, n):
    if not any(e[1] == n and abs(e[0] - t) < 0.02 for e in events): events.append((round(t, 3), n))
def hollow(t):
    if t < 0.95: u = t / 0.95; return HWALK[int(t * 10) % len(HWALK)], -120 + 760 * u
    if t < T_POUCH: return HSTAND, 640
    if t < T_POUCH + 0.75: u = (t - T_POUCH) / 0.75; return HPOUCH[min(7, int(u * 8))], 640
    return HSTAND, 640
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
    # the Hollow (customer) in front of the counter; from T_GIVE on, Syeda's cyrus-giving-gummy.gif plays both characters
    sp, hx = hollow(t)
    layer(img, lambda dd: dd.ellipse([hx - 70, HFEET - 14, hx + 70, HFEET + 12], fill=(0, 0, 0, 90)))
    if T_CY <= t:
        cxx = CYX if t >= T_GIVE else -120 + (CYX + 120) * min(1, (t - T_CY) / (T_GIVE - T_CY - 0.05))
        layer(img, lambda dd: dd.ellipse([cxx - 70, HFEET - 14, cxx + 70, HFEET + 12], fill=(0, 0, 0, 90)))
    if t < T_GIVE:
        if t >= T_CY + 0.35: sp = HIDLE[int(t * 10) % len(HIDLE)]      # he turns to the newcomer (Syeda's front idle, same pose the gif starts in)
        img.alpha_composite(sp, (int(hx - sp.width / 2), int(HFEET - FOOT)))
        if t >= T_CY:
            cf = CWALK[int(t * 10) % len(CWALK)]; img.alpha_composite(cf, (int(cxx - cf.width / 2), int(HFEET - FOOT)))
    else:
        k = gidx(t); gf = GIVE[k]; img.alpha_composite(gf, (int(640 - GHX * 1), int(HFEET - GFY)))
        if k == 30: ev(t, 'swish')
        if k == 38: ev(t, 'crunch_8bit')
        if k == 45 and int((t - T_GIVE) * GFPS) + G0 == 45: ev(t, 'powerup_8bit')
        if int((t - T_GIVE) * GFPS) + G0 == 47: ev(t, 'cheer')
    if f == 0 or (t - 1 / FPS < T_CY <= t): ev(t, 'chime')
    # 3 gummies reveal: all he has, vs the 999 tag
    if T_POUCH + 0.45 <= t < T_CY - 0.1:
        u = t - T_POUCH - 0.45; d = ImageDraw.Draw(img)
        # the 3 gummies pop out of the pouch beside him (fixed spot, inside the safe zone), '3 GUMMIES' held 1.1s (was 0.55s, slid off the left edge)
        if True:
            for q, gk in enumerate(('mush', 'acv', 'mel')):
                gg = up(GUMS[gk], 3) if gk != 'mel' else up(GUMS[gk], 2)
                cx, cy = 330 + q * 90, 1268 - min(1, u / 0.15) * 30 - (10 if q == 1 else 0)
                img.alpha_composite(gg, (int(cx - gg.width / 2), int(cy - gg.height / 2)))
        # hfg12: '3 GUMMIES' label cut (the 3 gummies popping out of the pouch show it)
        ev(T_POUCH + 0.45, 'coin_8bit')
    # sweat drop on the last line
    if T_POUCH + 0.85 <= t < T_GIVE:
        d = ImageDraw.Draw(img); u = (t - T_POUCH - 0.85); dy = (u * 40) % 30
        sx, sy = hx + 75, HFEET - FOOT + 110 + dy * 0.6
        d.polygon([(sx, sy - 44), (sx - 22, sy), (sx + 22, sy)], fill=(140, 200, 255), outline=(20, 15, 35)); d.ellipse([sx - 22, sy - 18, sx + 22, sy + 26], fill=(140, 200, 255), outline=(20, 15, 35), width=4)
        d.ellipse([sx - 10, sy - 8, sx - 2, sy], fill=(230, 245, 255))
        if 0 <= u < 1 / FPS: ev(t, 'boing')
    # header
    # dialogue box
    if cur is not None and t < BOX_OFF + 0.3 and not (T_SKIP <= t < T_SKIP1 + 0.1):
        t0, ls = LINES[cur]
        n = PRE[cur] + int((t - t0) * CPS)
        ba = 1 - max(0, min(1, (t - BOX_OFF) / 0.3))
        if ba < 1:          # fading out: draw the box on its own layer
            base = img; img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
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
        if not typing and int(t * 3) % 2 == 0:
            d.polygon([(bx1 - 60, by1 - 50), (bx1 - 36, by1 - 50), (bx1 - 48, by1 - 34)], fill=(255, 214, 60))
        if ba < 1:
            a_ = img.getchannel('A').point(lambda v: int(v * ba)); img.putalpha(a_); base.alpha_composite(img); img = base
    # n17: time-skip card (cartoon '... LATER' card over the scene)
    if T_SKIP <= t < T_SKIP1:
        u = t - T_SKIP; a = min(1, u / 0.12, (T_SKIP1 - t) / 0.12)
        layer(img, lambda dd: (dd.rectangle([0, 0, W, H], fill=(10, 8, 22, int(225 * a))), ctext(dd, 540, 900, '3 HOURS', F(76), (255, 214, 60), 9, int(255 * a)), ctext(dd, 540, 1000, 'LATER...', F(76), (255, 214, 60), 9, int(255 * a))))
        if f == int(T_SKIP * FPS): ev(t, 'rewind')
    # comment prompt from 0.3s on its own plate, right under the potions it points at
    if False:   # hfg12: WHICH WOULD YOU BUY? cut (caption asks)
        pa = int(255 * min(1, (t - 0.3) / 0.15))
        layer(img, lambda dd: (dd.rounded_rectangle([96, COUNTER_Y + 60, 984, COUNTER_Y + 124], 14, fill=(14, 10, 24, int(pa * 0.9)), outline=(255, 214, 60, pa), width=4),
                               ctext(dd, 540, COUNTER_Y + 70, 'WHICH WOULD YOU BUY?', F(44), (255, 255, 255), 6, pa)))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
ff.stdin.close(); ff.wait()
_o = []
for e in sorted(events):
    if any(q[1] == e[1] and e[0] - q[0] < 0.1 for q in _o): continue
    _o.append(e)
events = _o
json.dump({'events': events}, open(OUTD + '/ev.json', 'w')); print('done', END, len(events))
