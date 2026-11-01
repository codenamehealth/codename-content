import math, random, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
import sys; sys.path.insert(0, P + 'safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['GUESS THE', 'GUIDE'], accent=1, color=(255, 214, 60), sub='HOW MANY CAN YOU GET?')
print('hook bottom', HB)
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
POSES = [P + 'race/cyrus_atk/06.png', P + 'maze/anim/cleo_slide/04.png', P + 'maze/anim/ray_panic/03.png', P + 'race/joy_atk/04.png', P + 'maze/anim/hollow_srun/03.png']
def sil(p):
    im = Image.open(p).convert('RGBA'); im = im.crop(im.getbbox())
    k = max(1, min(9, 448 // im.width, 466 // im.height)); im = up(im, k)
    a = im.getchannel('A').point(lambda v: 255 if v > 90 else 0)
    s = Image.new('RGBA', im.size, (16, 10, 26, 255)); s.putalpha(a)
    pad = Image.new('RGBA', (im.width + 24, im.height + 24), (0, 0, 0, 0)); pad.alpha_composite(s, (12, 12))
    glow = pad.getchannel('A').filter(ImageFilter.MaxFilter(13))
    g = Image.new('RGBA', pad.size, (255, 250, 220, 255)); g.putalpha(glow.point(lambda v: int(v * 0.9)))
    out = Image.new('RGBA', pad.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(pad)
    return out
SIL = [sil(p) for p in POSES]
GOLD = up(Image.open(P + 'gummies/pick_gold.png').convert('RGBA'), 5)
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W // 6, H // 6), Image.BILINEAR).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.45).convert('RGBA'))
CX, CY, CS = 478, 924, 560   # card centred on the safe column (70-887) so the lower block clears the notch          # card centre and size
Q = 4
def card_frame():
    L = Image.new('RGBA', (CS // Q + 8, CS // Q + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(L); n = CS // Q
    d.rectangle([0, 0, n + 7, n + 7], fill=(60, 34, 12, 255))
    d.rectangle([2, 2, n + 5, n + 5], fill=(220, 160, 40, 255)); d.rectangle([3, 3, n + 4, n + 4], fill=(255, 214, 80, 255))
    d.rectangle([5, 5, n + 2, n + 2], fill=(150, 95, 25, 255)); d.rectangle([6, 6, n + 1, n + 1], fill=(0, 0, 0, 0))
    for (x, y) in ((1, 1), (n + 2, 1), (1, n + 2), (n + 2, n + 2)): d.rectangle([x, y, x + 4, y + 4], fill=(255, 240, 160, 255))
    return up(L, Q)
FRAME = card_frame()
NAMES = ['JOY', 'CLEO', 'CYRUS', 'RAYLEIGH', 'THE HOLLOW']; COLS = [(90, 200, 80), (90, 150, 255), (255, 160, 40), (190, 90, 240), (170, 160, 200)]
EGY = HB + 270   # end-card gummy top
RND = 3.6; TIMER = 3.1; ENDC = 3.4; NR = 5; TOTAL = NR * RND + ENDC
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'guess_v2_noaudio.mp4'], stdin=subprocess.PIPE)
ev = []
for f in range(int(TOTAL * FPS)):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    r = int(t // RND)
    # header
    d = ImageDraw.Draw(img)
    if r < NR:
        u = t - r * RND
        ctext(d, CX, HB + 14, f'ROUND {r + 1}/5', F(34), (255, 255, 255), 6)
        # flip-in scale
        fx = min(1, u / 0.22)
        card = Image.new('RGBA', (CS, CS), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        # rotating sunburst inside the card
        def burst(dd):
            dd.rectangle([0, 0, CS, CS], fill=(255, 200, 60, 255))
            for k in range(14):
                a1 = t * 0.6 + k * math.pi / 7; a2 = a1 + math.pi / 14
                dd.polygon([(CS / 2, CS / 2), (CS / 2 + 900 * math.cos(a1), CS / 2 + 900 * math.sin(a1)), (CS / 2 + 900 * math.cos(a2), CS / 2 + 900 * math.sin(a2))], fill=(255, 236, 140, 255))
        burst(cd)
        rr = random.Random(r)
        for q in range(4):
            qx = rr.uniform(60, CS - 120); qy = (rr.uniform(0, CS) - u * 60) % CS
            cd.text((qx, qy), '?', font=F(48), fill=(200, 130, 40, 255))
        s = SIL[r]; bob = int(8 * math.sin(t * 3))
        card.alpha_composite(s, (CS // 2 - s.width // 2, CS // 2 - s.height // 2 + bob))
        card.alpha_composite(Image.new('RGBA', (1, 1), (0, 0, 0, 0)))
        fr = Image.new('RGBA', FRAME.size, (0, 0, 0, 0)); fr.alpha_composite(card, (6 * Q, 6 * Q)); fr.alpha_composite(FRAME)
        if fx < 1: fr = fr.resize((max(1, int(fr.width * fx)), fr.height), Image.NEAREST)
        img.alpha_composite(fr, (CX - fr.width // 2, CY - fr.height // 2))
        # timer bar
        p = max(0, 1 - max(0, u - 0.25) / TIMER)
        col = (90, 220, 90) if p > 0.5 else ((255, 200, 60) if p > 0.25 else (230, 70, 60))
        bx0, bx1, by0 = 84, 874, 1238
        d = ImageDraw.Draw(img)
        d.rectangle([bx0 - 6, by0 - 6, bx1 + 6, by0 + 36], fill=(20, 15, 35))
        d.rectangle([bx0, by0, bx0 + int((bx1 - bx0) * p), by0 + 30], fill=col)
        # options
        oy = by0 + 54
        for i, (nm, c) in enumerate(zip(NAMES, COLS)):
            if i < 3: x0 = 84 + i * 270; y0 = oy
            else: x0 = 219 + (i - 3) * 270; y0 = oy + 100
            d.rounded_rectangle([x0, y0, x0 + 250, y0 + 86], 14, fill=(20, 15, 35), outline=c, width=6)
            ctext(d, x0 + 125, y0 + 30, nm, F(26 if len(nm) < 7 else 20), (255, 255, 255), 0)
        ctext(d, (bx0 + bx1) / 2, by0 + 4, 'PAUSE IF YOU NEED MORE TIME', F(22), (255, 255, 255), 4)
        if f % FPS == int(0.25 * FPS) % FPS and u < TIMER + 0.25: pass
    else:
        u = t - NR * RND
        d = ImageDraw.Draw(img)
        a = min(1, u / 0.3)
        ctext(d, W / 2, HB + 40, 'HOW MANY', F(72), (255, 255, 255), 8); ctext(d, W / 2, HB + 140, 'DID YOU GET?', F(64), (255, 214, 60), 8)
        bob = int(10 * math.sin(t * 3)); img.alpha_composite(GOLD, (W // 2 - GOLD.width // 2, EGY + bob))
        def sp(dd):
            for k in range(8):
                an = t * 1.5 + k * 0.785; sx, sy = W / 2 + 150 * math.cos(an), EGY + GOLD.height / 2 + 110 * math.sin(an)
                dd.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 245, 190, 230))
        layer(img, sp); d = ImageDraw.Draw(img)
        ctext(d, W / 2, EGY + 230, '5/5 earns the golden gummy', F(30), (255, 214, 60), 5)
        ctext(d, 478, EGY + 320, 'Comment your score', F(36), (255, 255, 255), 5)
        for i in range(5):
            x0 = 118 + i * 150
            d.rectangle([x0, EGY + 400, x0 + 120, EGY + 520], fill=(20, 15, 35), outline=(255, 214, 60), width=6)
            ctext(d, x0 + 60, EGY + 435, str(i + 1), F(52), (255, 255, 255), 0)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/v_{f:04d}.png')
ff.stdin.close(); ff.wait()
for r in range(NR):
    ev.append((round(r * RND, 3), 'swish'))
    for k in range(4): ev.append((round(r * RND + 0.3 + k * 0.8, 3), 'tick_8bit'))
ev.append((round(NR * RND, 3), 'ding_8bit')); ev.append((round(NR * RND + 0.4, 3), 'twinkle'))
json.dump({'events': ev}, open('guess_v2_events.json', 'w')); print('done', TOTAL)
