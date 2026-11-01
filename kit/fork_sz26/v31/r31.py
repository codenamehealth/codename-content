import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['HOLD YOUR THUMB', 'ON THE CRYSTAL'], accent=1)
print('hook bottom', HB)
R = '../../'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS, DUR = 1080, 1920, 30, 13.5; N = int(DUR * FPS)
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
BG = up(Image.open('../../fork_a3/shrine1/00.png').convert('RGBA'), 3).crop((36, 60, 36 + W, 60 + H))
CRY = up(Image.open('../../fork_a3/crystal/03.png').convert('RGBA').crop(Image.open('../../fork_a3/crystal/03.png').getbbox()), 5)
CX, CY = 470, 790
CAST = [up(Image.open(p).convert('RGBA'), 4) for p in sorted(glob.glob('../../fork_a3/joy_cast/*.png'))]
JX, JY = 845, 1096           # Joy's feet (4x)
WX0, WX1, WY0, WY1 = 72, 880, 1118, 1496   # status window
GUM = up(Image.open(R + 'pixellab/gummies/pick_acv.png').convert('RGBA'), 3)
DEBUFF = [('POISONED', 'Doomscrolling', (150, 90, 200)), ('-10 HP', 'Monday', (220, 70, 70)), ('SLOWED', '1% battery', (90, 150, 255)),
          ('CURSED', '37 tabs open', (170, 60, 170)), ('CONFUSED', 'The group chat', (240, 200, 60)), ('DRAINED', 'One more episode', (140, 140, 160))]
T_HOLD = 1.8; STEP = 1.45; TCL = [T_HOLD + 0.6 + i * STEP for i in range(6)]; T_END = TCL[-1] + 1.0
rng = random.Random(3); FLIES = [(rng.uniform(0, W), rng.uniform(450, 1450), rng.uniform(0, 6.3)) for _ in range(30)]
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v31_noaudio.mp4'], stdin=subprocess.PIPE)
events = []
def bez(p0, p1, p2, u): return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])
for f in range(N):
    t = f / FPS; img = BG.copy()
    layer(img, lambda d: [d.rectangle([x, y + 20 * math.sin(t + p), x + 5, y + 5 + 20 * math.sin(t + p)], fill=(230, 255, 140, int(120 + 110 * math.sin(t * 2.5 + p)))) for x, y, p in FLIES])
    held = t >= T_HOLD
    # crystal glow + rays
    bob = 10 * math.sin(t * 2.2); glow = 0.6 + 0.4 * math.sin(t * 4) + (0.5 if held else 0)
    def aura(d):
        for k in range(6, 0, -1):
            r = 70 + k * 22 * (1.15 if held else 1)
            d.ellipse([CX - r, CY + bob - r, CX + r, CY + bob + r], fill=(140, 220, 255, int(min(255, 16 * glow * (7 - k)))))
        if held:
            for k in range(10):
                a = t * 0.8 + k * math.pi / 5; L = 260 + 30 * math.sin(t * 3 + k)
                d.line([CX + 90 * math.cos(a), CY + bob + 90 * math.sin(a), CX + L * math.cos(a), CY + bob + L * math.sin(a)], fill=(200, 240, 255, 60), width=10)
    layer(img, aura)
    img.alpha_composite(CRY, (int(CX - CRY.width / 2), int(CY + bob - CRY.height / 2)))
    # hold ring + arrow
    if not held or t < T_HOLD + 0.4:
        prog = min(1, t / T_HOLD)
        def ring(d):
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], 0, 360, fill=(255, 255, 255, 90), width=10)
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], -90, -90 + 360 * prog, fill=(150, 240, 120, 255), width=12)
        layer(img, ring)
        if not held:
            ay = CY - 225 + 18 * math.sin(t * 6); d = ImageDraw.Draw(img)
            d.polygon([(CX - 34, ay), (CX + 34, ay), (CX, ay + 46)], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
            d.rectangle([CX - 13, ay - 60, CX + 13, ay], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
    # sparkle streams to Joy while clearing
    if held and t < T_END:
        def stream(d):
            for k in range(26):
                u = ((t * 0.9 + k / 26) % 1.0)
                x, y = bez((CX, CY + bob), (CX + 230, CY - 120 + 60 * math.sin(k)), (JX - 20, JY - 190), u)
                s = 4 + 4 * math.sin(u * math.pi)
                d.rectangle([x - s, y - s, x + s, y + s], fill=(170, 255, 140, int(220 * math.sin(u * math.pi))))
        layer(img, stream)
    # Joy
    if not held: fr = CAST[0]
    else:
        k = int((t - T_HOLD) * 10)
        fr = CAST[1 + (k % 12)] if t < T_END else CAST[0]
    layer(img, lambda d: d.ellipse([JX - 60, JY - 14, JX + 60, JY + 12], fill=(0, 0, 0, 80)))
    img.alpha_composite(fr, (JX - fr.width // 2, JY - 78 * 4))
    # status window
    def win(d):
        d.rounded_rectangle([WX0, WY0, WX1, WY1], 22, fill=(16, 22, 40, 225), outline=(240, 230, 200, 255), width=6)
        d.rounded_rectangle([WX0 + 12, WY0 + 12, WX1 - 12, WY1 - 12], 16, outline=(110, 120, 160, 255), width=3)
    layer(img, win)
    d = ImageDraw.Draw(img)
    cleared = sum(1 for tc in TCL if t >= tc)
    hp = 12 + (88 * cleared / 6 if cleared < 6 else 88)
    d.text((WX0 + 30, WY0 + 36), 'JOY', font=F(34), fill=(140, 230, 110), stroke_width=4, stroke_fill=(10, 10, 20))
    d.text((WX0 + 148, WY0 + 44), 'HP', font=F(26), fill=(255, 214, 60), stroke_width=3, stroke_fill=(10, 10, 20))
    d.rectangle([WX0 + 210, WY0 + 42, WX0 + 610, WY0 + 72], fill=(40, 30, 50), outline=(240, 230, 200), width=3)
    col = (220, 70, 70) if hp < 35 else (240, 200, 60) if hp < 70 else (110, 220, 90)
    d.rectangle([WX0 + 214, WY0 + 46, WX0 + 214 + int(392 * hp / 100), WY0 + 68], fill=col)
    d.text((WX0 + 626, WY0 + 47), f'{int(hp)}/100', font=F(20), fill=(255, 255, 255), stroke_width=3, stroke_fill=(10, 10, 20))
    for i, (nm, sub, c) in enumerate(DEBUFF):
        x = WX0 + 28 + (i % 2) * 392; y = WY0 + 108 + (i // 2) * 86
        done = t >= TCL[i]; u = t - TCL[i]
        a = 255 if not done else max(90, int(255 - 300 * u))
        d.rounded_rectangle([x, y, x + 34, y + 34], 6, fill=c if not done else (110, 220, 90), outline=(10, 10, 20), width=3)
        if done: d.line([x + 7, y + 18, x + 15, y + 26, x + 28, y + 9], fill=(255, 255, 255), width=5)
        d.text((x + 48, y - 2), nm, font=F(22), fill=c + (a,) if not done else (130, 140, 150), stroke_width=3, stroke_fill=(10, 10, 20))
        d.text((x + 48, y + 28), sub, font=F(18), fill=(235, 235, 235) if not done else (120, 125, 135), stroke_width=2, stroke_fill=(10, 10, 20))
        if done:
            tw = d.textlength(sub, font=F(18)); d.line([x + 46, y + 38, x + 50 + tw, y + 38], fill=(230, 80, 80), width=4)
            if u < 0.9:
                aa = int(255 * min(1, (0.9 - u) / 0.3))
                ctext(d, 700, JY - 400 - u * 60, nm + ' CLEARED!', F(30), (140, 240, 110), 6, aa)
                ctext(d, JX - 20, JY - 345 - u * 60, '+15 HP', F(34), (255, 214, 60), 6, aa)
        if abs(t - TCL[i]) < 0.5 / FPS: events.append((round(TCL[i], 3), 'chime'))
    # header
    d = ImageDraw.Draw(img)
    if t >= T_END:
        u = t - T_END; s = min(1, u / 0.25)
        ctext(d, W / 2, HB + 24, 'ALL DEBUFFS CLEARED!', F(int(28 + 14 * s)), (140, 240, 110), 6)
        # ACV gummy reward pops from the crystal into Joy's hand
        gu = min(1, u / 0.7); gx, gy = bez((CX, CY), (CX + 200, CY - 200), (JX - 80, JY - 190), gu)
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        d = ImageDraw.Draw(img); ctext(d, 470, 960, '+100 HP', F(64), (255, 214, 60), 8)
        if not any(e[1] == 'powerup_8bit' for e in events): events.append((round(T_END, 3), 'powerup_8bit'))
    if abs(t - T_HOLD) < 0.5 / FPS: events.append((round(T_HOLD, 3), 'twinkle'))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((216, 384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v31_events.json', 'w')); print('done', T_END)
