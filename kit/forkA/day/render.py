import math, random, json, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
def load(d, k, clean=False):
    fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
    if clean: fr = [nored(f) for f in fr]
    return [up(f, k) for f in fr]
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
S = 5
ATK = load(P + 'race/cleo_atk', S)                 # 128 canvas, char offset (-14,+26) vs 92 canvas
EAT = load(P + 'cleo/eat_mm', S)                    # 92 canvas
STAND = up(Image.open(P + 'race/in/cleo_side.png').convert('RGBA'), S)
SL = load(P + 'race/slime_idle_c', S, True); SPL = load(P + 'race/slime_splat_c', S, True)
KL = load(P + 'king/king2_land', 4); KI = load(P + 'king/king2_idle', 4)
DUST = up(crop(Image.open(P + 'king/dust_cands/00.png').convert('RGBA')), 3)
GUM = {k: up(Image.open(P + f'gummies/pick_{k}.png').convert('RGBA'), 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}
GSM = up(Image.open(P + 'gummies/pick_cre.png').convert('RGBA'), 2)
vic = Image.open(A + 'vic_victoryPose.gif'); VIC = []
for i in range(vic.n_frames): vic.seek(i); VIC.append(vic.convert('RGBA'))
bb = None
for f in VIC:
    b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
VIC = [f.crop(bb) for f in VIC]; kk = 330 / VIC[0].height; VIC = [f.resize((int(f.width * kk), 330), Image.NEAREST) for f in VIC]
g = Image.open(A + 'vit_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(f.convert('RGBA'))
FEET = 1560; CX = 190; SX = CX + 320; KX = CX + 296
# timeline
DAYS = [(0.0, 1, 1), (3.2, 7, 7), (6.6, 30, 30), (10.0, 365, 365)]
ATK_T = {1: 1.3, 7: 5.0, 30: 8.4, 365: 12.3}; DMG = {1: '1 DMG', 7: '12 DMG', 30: '240 DMG', 365: '9999 DMG'}
EAT_T = {7: 3.6, 30: 7.0, 365: 10.9}
HP0 = {1: 1.0, 7: 0.99, 30: 0.95, 365: 1.0}; HP1 = {1: 0.99, 7: 0.95, 30: 0.0, 365: 0.0}
END_FIGHT = 14.6; END = 18.0; ATK_FPS = 18; HITF = 4
events = []
def day_at(t):
    cur = DAYS[0]
    for d in DAYS:
        if t >= d[0]: cur = d
    return cur
def put_char(img, fr, x, feet, canvas=92):
    img.alpha_composite(fr, (int(x), int(feet - 78 * S)))
rays = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'day_noaudio.mp4'], stdin=subprocess.PIPE)
burst = [(random.Random(i).uniform(-1, 1), random.Random(i + 99).uniform(-1.4, -0.4), ['mush', 'acv', 'mel', 'cre', 'gold'][i % 5]) for i in range(26)]
for f in range(int(END * FPS)):
    t = f / FPS; t0, day, ng = day_at(t)
    img = BGS[int(t * 6) % len(BGS)].copy()
    big = day == 365
    shake = (0, 0)
    ta = ATK_T[day]; hit_t = ta + HITF / ATK_FPS
    if big and hit_t <= t < hit_t + 0.5:
        r = random.Random(f); shake = (r.randint(-16, 16), r.randint(-12, 12))
    if big and t >= 10.0:
        # golden sunburst behind the action
        def rays_fn(dd):
            cx, cy = 540, 1250; a0 = t * 0.4
            for k in range(16):
                a1 = a0 + k * math.pi / 8; a2 = a1 + math.pi / 16
                dd.polygon([(cx, cy), (cx + 2000 * math.cos(a1), cy + 2000 * math.sin(a1)), (cx + 2000 * math.cos(a2), cy + 2000 * math.sin(a2))], fill=(255, 200, 60, 70))
        layer(img, rays_fn)
    stage = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # ---- enemy
    hp = HP0[day]
    if not big:
        if t < hit_t:
            fr = SL[int(t * 8) % len(SL)]; stage.alpha_composite(fr, (SX, FEET - 62 * S))
        else:
            u = t - hit_t
            if day < 30:
                kb = int(60 * math.exp(-u * 6) * (1 if day == 7 else 0.3)); fr = SL[int(t * 8) % len(SL)]
                stage.alpha_composite(fr, (SX + kb, FEET - 62 * S)); hp = HP1[day]
            else:
                k = min(8, 3 + int(u * 12)); hp = 0
                if k < 8 or u < 1.2: stage.alpha_composite(SPL[k], (SX, FEET - 62 * S))
    else:
        tl = 10.25
        if t >= tl:
            u = t - tl
            if u < 0.35: y = FEET - 156 * 4 - (1 - u / 0.35) ** 2 * 1300; fr = KL[0]
            else:
                fr = KL[min(12, int((u - 0.35) * 14))] if u < 1.3 else KI[int(t * 8) % len(KI)]; y = FEET - 156 * 4
            if t < hit_t:
                stage.alpha_composite(fr, (KX, int(y)))
                if 0.35 <= u < 0.9:
                    du = (u - 0.35) / 0.55; dd = DUST.resize((int(DUST.width * (1 + du)), int(DUST.height * (1 + du))), Image.NEAREST)
                    al = dd.getchannel('A').point(lambda p: int(p * (1 - du))); dd.putalpha(al)
                    stage.alpha_composite(dd, (KX + 318 - dd.width // 2, FEET - dd.height + 20))
            elif t < hit_t + 0.25:
                wf = fr.copy(); wh = Image.new('RGBA', wf.size, (255, 255, 255, 255)); wh.putalpha(wf.getchannel('A')); stage.alpha_composite(wh, (KX, int(y)))
            hp = 1.0 if t < hit_t else 0.0
            # gummy shower
            if t >= hit_t:
                u2 = t - hit_t
                for i, (vx, vy, k) in enumerate(burst):
                    gx = KX + 318 + vx * 900 * u2; gy = FEET - 320 + vy * 1500 * u2 + 1800 * u2 * u2
                    if gy < H + 60: gimg = GUM[k]; stage.alpha_composite(gimg, (int(gx - gimg.width / 2), int(gy - gimg.height / 2)))
    # ---- Cleo
    if day == 365 and t >= END_FIGHT:
        vf = VIC[int(t * 8) % len(VIC)]; stage.alpha_composite(vf, (CX + 225 - vf.width // 2, FEET - vf.height))
    elif ta <= t < ta + 12 / ATK_FPS:
        k = min(11, int((t - ta) * ATK_FPS)); stage.alpha_composite(ATK[k], (CX + 70, FEET - 104 * S))
    elif day in EAT_T and EAT_T[day] <= t < EAT_T[day] + 12 / 10:
        k = min(12, int((t - EAT_T[day]) * 10)); stage.alpha_composite(EAT[k], (CX, FEET - 78 * S))
    else:
        stage.alpha_composite(STAND, (CX, FEET - 78 * S + (2 * S if int(t * 2.5) % 2 else 0)))
    # aura grows with the days
    aura = {1: 0, 7: 0, 30: 1, 365: 2}[day]
    if aura and not (day == 365 and t >= END_FIGHT):
        def aura_fn(dd):
            r = random.Random(int(t * 12))
            for q in range(10 * aura):
                ax = CX + 225 + r.uniform(-120, 120); ay = FEET - r.uniform(20, 380) - (t * 200 % 120)
                col = (120, 180, 255, 200) if aura == 1 else (255, 220, 90, 220)
                dd.rectangle([ax - 5, ay - 5, ax + 5, ay + 5], fill=col)
        layer(stage, aura_fn)
    img.alpha_composite(stage, shake)
    d = ImageDraw.Draw(img)
    # damage popup
    if hit_t <= t < hit_t + 1.4:
        u = t - hit_t; a = int(255 * min(1, (1.4 - u) / 0.4))
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        size = {1: 34, 7: 44, 30: 60, 365: 84}[day]; col = {1: (230, 230, 230), 7: (255, 230, 120), 30: (255, 190, 60), 365: (255, 214, 60)}[day]
        ctext(pd, (W / 2 if big else SX + 160), FEET - 520 - u * 60 - (200 if big else 0), DMG[day], F(size), col, 7, a)
        if big: ctext(pd, W / 2, FEET - 620 - u * 60, 'CRITICAL HIT!', F(44), (255, 80, 80), 6, a)
        img.alpha_composite(PL)
        if big and u < 0.25:
            # slash arc
            def slash(dd):
                r0 = 260 + u * 600
                dd.arc([KX + 318 - r0, FEET - 330 - r0, KX + 318 + r0, FEET - 330 + r0], 200, 340, fill=(255, 255, 255, int(255 * (1 - u / 0.25))), width=26)
            layer(img, slash)
    # slime hp bar
    if not (day == 365 and t >= END_FIGHT) and (not big or t >= 10.6):
        bx = (KX + 188) if big else (SX + 60); by = FEET - (500 if big else 210); bw = 260 if big else 200
        def hpb(dd):
            dd.rectangle([bx - 4, by - 4, bx + bw + 4, by + 24], fill=(20, 15, 35, 230))
            dd.rectangle([bx, by, bx + int(bw * hp), by + 20], fill=(90, 220, 90, 255) if hp > 0.3 else (230, 80, 60, 255))
        layer(img, hpb)
    # header: DAY N
    d = ImageDraw.Draw(img)
    layer(img, lambda dd: dd.rectangle([0, 0, W, 330], fill=(12, 8, 22, 170)))
    d = ImageDraw.Draw(img)
    col = (255, 214, 60) if big else (255, 255, 255)
    ctext(d, W / 2, 70, f'DAY {day}', F(96), col, 9)
    # daily gummy counter
    gx0 = W / 2 - 120
    img.alpha_composite(GSM, (int(gx0), 222)); d = ImageDraw.Draw(img)
    d.text((gx0 + GSM.width + 18, 236), f'x {ng}', font=F(40), fill=(255, 255, 255), stroke_width=5, stroke_fill=(20, 15, 35))
    if day in EAT_T and EAT_T[day] + 0.6 <= t < EAT_T[day] + 1.8:
        u = t - EAT_T[day] - 0.6; a = int(255 * min(1, (1.2 - u) / 0.4))
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        ctext(pd, CX + 225, FEET - 520 - u * 50, 'POWER UP!', F(36), (120, 220, 255) if day < 365 else (255, 214, 60), 6, a)
        img.alpha_composite(PL)
    # white flash into day 365
    if 9.8 <= t < 10.3:
        a = int(255 * (1 - abs(t - 10.0) / 0.3)) if t < 10.3 else 0
        img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, max(0, min(255, a)))))
    if t >= END_FIGHT + 0.4:
        u = t - END_FIGHT - 0.4; a = int(255 * min(1, u / 0.4))
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        pd.rectangle([0, 1640, W, 1860], fill=(12, 8, 22, int(200 * a / 255)))
        ctext(pd, W / 2, 1670, 'SAME QUEST.', F(60), (255, 255, 255), 7, a); ctext(pd, W / 2, 1760, 'EVERY DAY.', F(60), (255, 214, 60), 7, a)
        img.alpha_composite(PL)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p_{f:04d}.png')
ff.stdin.close(); ff.wait()
ev = []
for day in (1, 7, 30, 365):
    ht = ATK_T[day] + HITF / ATK_FPS
    ev.append((round(ATK_T[day] + 0.05, 3), 'sword_swish'))
    ev.append((round(ht, 3), {1: 'boing', 7: 'sword_hit', 30: 'squish', 365: 'boom'}[day]))
for day, te in EAT_T.items(): ev.append((round(te + 0.6, 3), 'powerup_8bit'))
ev += [(10.85, 'punch'), (round(ATK_T[365] + HITF / ATK_FPS + 0.1, 3), 'twinkle'), (END_FIGHT, 'victory'), (9.85, 'chime')]
json.dump({'events': sorted(ev)}, open('day_events.json', 'w'))
print('done')
