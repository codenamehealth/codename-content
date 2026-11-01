import sys, os; os.chdir('../../fork_b5/v53'); OUT='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc18/v53/'; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '../../pixellab/safezone')
from common import *
from hook import hook_layer
sys.path.insert(0, '../../fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, '../../fork_rc2'); from rc2 import acv_gloss
sys.path.insert(0, '../../fork_c7'); from powers import *
# rc18: comment prompt as a 44px second line of the hook band from frame 0 (was a 36px line only on the intro/end card)
HK1, HB1 = hook_layer2(['PICK A', 'CHEST'], accent=1, sub='Comment 1, 2 or 3')
HK2, HB2 = hook_layer2(['WHICH CHEST', 'DID YOU PICK?'], accent=1, sub='Comment 1, 2 or 3'); print('HB', HB1, HB2)
K = 4; GY = 1150;   # rc18: action 70px lower (and the background with it) to clear the taller hook band
SH = -140; FEET = 1495
BG = bg_frames('sun_hd.gif', (W, H), box=(660, 0, 1267, 1080), step=2, bright=0.9)
BGD = [ImageEnhance.Brightness(b).enhance(0.45) for b in BG]
def lift(b):
    n = Image.new('RGBA', (W, H)); n.paste(b.crop((0, 130, W, 1650)), (0, 0)); n.paste(b.crop((0, 1520, W, H)), (0, 1520)); return n
BG = [lift(b) for b in BG]
GUMS = [gummy(k, 2) for k in ('mush', 'cre', 'acv', 'mel')]
ATK = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob('../hollow_punch2/*.png'))]
RUN = seq(PL + 'maze/anim/hollow_srun', K, 1, 9)
PANIC = seq(PL + 'maze/anim/hollow_panic', K, 1, 9)
EAT = seq(SP + 'fork3/hollow_eat', K, 1, 13)
import numpy as np
def pinkify(im):   # the eaten gummy is red in the eat sprite: recolour it creatine pink (matches the chest item)
    a = np.array(im).astype(int); r, g, b_ = a[..., 0], a[..., 1], a[..., 2]; m = (r > 140) & (g < 120) & (b_ < 120) & (a[..., 3] > 0)
    a[..., 2][m] = np.minimum(255, b_[m] + (r[m] * 0.6).astype(int)); a[..., 1][m] = g[m] + (r[m] * 0.12).astype(int)
    return Image.fromarray(a.astype(np.uint8))
EAT_ACV = EAT                     # rc18: the unrecoloured eat sprite's red gummy = Syeda's apple-shaped ACV gummy
EAT = [pinkify(f) for f in EAT]
CYI = idle('cyrus', K)
IDLE = idle('hollow', K)
VICC = [up(f.resize((92, 92), Image.NEAREST), K) for f in gif_frames(A + VIC['hollow'])]
DF = seq('../../fork_c7/assets/dragonfire_gum', 1, 0, 9)   # hoard = gummy pile (no gold)
CHC = crop(Image.open('../chest_closed/14.png').convert('RGBA'))
CHO = [crop(Image.open(p).convert('RGBA')) for p in sorted(glob.glob('../chest_open/*.png'))]
STICK = crop(Image.open('../stick/01.png').convert('RGBA')); SHIELD = crop(Image.open('../shield/02.png').convert('RGBA'))
GUM = crop(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'))   # creatine: STRONG (SPEC 12)
ACV = crop(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')))   # rc18: chest 2 is the ACV gummy (SHIELD), not a plain shield
ITEMS = [(STICK, 'WOODEN STICK', 'STICK'), (ACV, 'ACV GUMMY', 'ACV GUMMY'), (GUM, 'CREATINE GUMMY', 'CREATINE')]
ENDLAB = [['STICK'], ['ACV', 'GUMMY'], ['CREATINE', 'GUMMY']]; ITK = [8, 9, 9]; ENDK = [4, 5, 5]
def strong_aura(img, spr, x0, y0, b):
    pu = 0.5 + 0.5 * math.sin(b * 14)
    tt = tinted(spr, (200, 235, 255), int(170 + 70 * pu))
    for k_ in range(12):
        a_ = k_ * math.pi / 6; img.alpha_composite(tt, (int(x0 + 12 * math.cos(a_)), int(y0 + 12 * math.sin(a_))))
    tt = tinted(spr, (60, 130, 255), 255)
    for k_ in range(8):
        a_ = k_ * math.pi / 4; img.alpha_composite(tt, (int(x0 + 6 * math.cos(a_)), int(y0 + 6 * math.sin(a_))))
def put_atk(img, fr, cx, tint=None):
    if tint: fr = ImageEnhance.Brightness(fr).enhance(tint)
    img.alpha_composite(fr, (int(cx - 45 * K), int(GY - 104 * K)))
def put92(img, fr, cx, gy=None):
    img.alpha_composite(fr, (int(cx - fr.width / 2), int((gy or GY) - 78 * K)))
DX = 400 + SH   # dragon canvas left
def dragon(img, k, shift=0, tint=None):
    fr = DF[k]
    if tint: fr = ImageEnhance.Brightness(fr).enhance(tint)
    img.alpha_composite(fr, (int(DX + shift), int(GY + 30 - fr.height)))
# rc18: chests rattle from frame 0 and chest 1 opens at 0.8s (was 2.6s still intro + 0.5s); reveal cards 1.4 -> 1.0s;
# stalemate 2.0 -> 1.0s; end card 3.2 -> 2.5s
S0 = 0.45; RV = 1.0; ACT = [3.0, 2.9, 3.2]
ST = [S0, S0 + RV + ACT[0], S0 + 2 * RV + ACT[0] + ACT[1]]; END0 = ST[2] + RV + ACT[2]; DUR = END0 + 2.5; NF = int(DUR * FPS)
ev = []
def once(key, t, snd):
    if key not in done: done.add(key); ev.append((round(t, 3), snd))
done = set()
wr = Writer(OUT + 'v53_noaudio.mp4'); OPEN = []
for f in range(NF):
    t = f / FPS; fi = int(t * 10)
    if t < S0 or t >= END0:
        img = BGD[int(t * 6) % len(BGD)].copy()
        if t < S0:
            for k, x in enumerate([230, 540, 850]):
                c = up(CHC, 5); bob = int(6 * math.sin(t * 5 + k)); sh = int(8 * math.sin(t * 55 + k * 2))   # rattling from frame 0
                if k == 0 and t > 0.15:
                    gl = (t - 0.15) / 0.3
                    layer(img, lambda d, x=x, gl=gl: [d.ellipse([x - 130 - q, 860 - 70 - q, x + 130 + q, 860 + 150 + q], fill=(255, 220, 110, int(60 * gl))) for q in (0, 24)])
                    sh = int(14 * math.sin(t * 70))
                img.alpha_composite(c, (int(x - c.width / 2 + sh), 860 + bob)); text_layer(img, [(x, 860 + c.height + 20, str(k + 1), 60, (255, 214, 60), 7, 255)])
            put92(img, IDLE[fi % len(IDLE)], 478, FEET)
        else:
            u = t - END0
            for k, x in enumerate([230, 540, 840]):
                c = up(CHO[-1], 4); img.alpha_composite(c, (int(x - c.width / 2), 760))
                it = up(ITEMS[k][0], ENDK[k]); bob = int(8 * math.sin(t * 4 + k))
                img.alpha_composite(it, (int(x - it.width / 2), 732 - it.height + bob))
                # number on the chest front, item label under it, all above y1110 (lower-right safe zone)
                text_layer(img, [(x, 880, str(k + 1), 60, (255, 214, 60), 9, 255)] + [(x, 1014 + 48 * j, ln, 44, (255, 255, 255), 7, 255) for j, ln in enumerate(ENDLAB[k])])
            vf = VICC[int(u * 8) % len(VICC)]; put92(img, vf, 340, FEET); put92(img, CYI[fi % len(CYI)], 640, FEET)
        img.alpha_composite(HK1 if t < S0 else HK2)
        wr.write(img)
        if f < 9: OPEN.append(img.copy())
        continue
    k = max(i for i in range(3) if t >= ST[i]); u = t - ST[k]
    item, label, short = ITEMS[k]
    if u < RV:
        # reveal card
        img = BGD[int(t * 6) % len(BGD)].copy()
        text_layer(img, [(W / 2, 640, f'CHEST {k + 1}', 80, (255, 214, 60), 9, 255)])
        if u < 0.35:
            c = up(CHC, 8); sh = int(10 * math.sin(u * 60)) if u > 0.08 else 0
            img.alpha_composite(c, (int(W / 2 - c.width / 2 + sh), 1150 - c.height))
        else:
            c = up(CHO[min(len(CHO) - 1, int((u - 0.35) * 18))], 7)
            img.alpha_composite(c, (int(W / 2 - c.width / 2), 1150 - c.height))
            once(('open', k), t, 'chime')
            rise = min(1, (u - 0.35) / 0.4); it = up(item, ITK[k])
            def rays(d, rise=rise):
                for a in range(12):
                    ang = a * math.pi / 6 + u; r1, r2 = 60, 260 * rise
                    d.line([(W / 2 + r1 * math.cos(ang), 850 + r1 * math.sin(ang)), (W / 2 + r2 * math.cos(ang), 850 + r2 * math.sin(ang))], fill=(255, 230, 120, 110), width=14)
            layer(img, rays)
            img.alpha_composite(it, (int(W / 2 - it.width / 2), int(1030 - 180 * rise - it.height / 2)))
            text_layer(img, [(W / 2 if len(label) < 13 else 478, 1220, label, 52 if len(label) < 13 else 46, (255, 255, 255), 7, int(255 * rise))])
        if u < 0.1: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(180 * (1 - u / 0.1)))))
        img.alpha_composite(HK1)
        wr.write(img); continue
    b = u - RV
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.rounded_rectangle([70, HB1 + 8, 1025, HB1 + 80], 16, fill=(14, 10, 24, 210)))
    text_layer(img, [(W / 2, HB1 + 22, f'CHEST {k + 1}: {short}', 44, (255, 214, 60), 7, 255)])
    if k == 0:
        if b < 0.6:
            x = 150 + 210 * (b / 0.6); put92(img, RUN[fi % 8], x); dragon(img, 0)
            st = up(STICK, 4).rotate(-30, expand=True, resample=Image.NEAREST); img.alpha_composite(st, (int(x + 10), int(GY - 230)))
        elif b < 1.0:
            x = 500 + SH; put_atk(img, ATK[min(12, 3 + int((b - 0.6) * 20))], x); dragon(img, 0)
            if b > 0.75:
                once('snap', t, 'poof')
                for s, dx in ((-1, -30), (1, 30)):
                    h = up(STICK, 3).crop((0, 0, up(STICK, 3).width // 2, up(STICK, 3).height)) if s < 0 else up(STICK, 3).crop((up(STICK, 3).width // 2, 0, up(STICK, 3).width, up(STICK, 3).height))
                    yy = (b - 0.75) * 900; img.alpha_composite(h.rotate(s * (b - 0.75) * 700, expand=True), (int(620 + SH + dx * (b - 0.75) * 8), int(GY - 260 + yy)))
                text_layer(img, [(640 + SH, GY - 440, 'SNAP!', 56, (255, 255, 255), 7, 255)])
        else:
            bb = b - 1.0; fk = min(8, 1 + int(bb * 9)) if bb < 1.0 else 0
            dragon(img, fk)
            once('fire0', t, 'boom')
            if bb < 0.35: put_atk(img, ATK[0], 500 + SH)
            else:
                x = 500 + SH - min(1, (bb - 0.35) / 0.3) * 170
                put92(img, ImageEnhance.Brightness(PANIC[fi % 8]).enhance(0.45 if bb < 1.4 else 0.75), x)
                for q in range(4):
                    pu = (bb * 1.5 + q * 0.25) % 1
                    layer(img, lambda d, q=q, pu=pu, x=x: d.ellipse([x - 40 + q * 25 - pu * 20, GY - 380 - pu * 160, x + q * 25 + pu * 20, GY - 340 - pu * 160 + 20], fill=(90, 90, 90, int(180 * (1 - pu)))))
                if bb > 1.2: text_layer(img, [(max(x, 270), GY - 430, 'OOPS...', 50, (255, 255, 255), 7, 255)])   # rc18: inside the 70px margin (was x~24)
    elif k == 1:
        x = 400 + SH          # rc18: 40px right so the shield bubble stays inside the left safe margin
        if b < 0.5:
            put92(img, EAT_ACV[min(11, int(b / 0.5 * 12))], x); dragon(img, 0)
        else:
            once('acv', t, 'twinkle')
            put_atk(img, ATK[0], x)
            # ACV SHIELD (SPEC 12): green bubble around the Hollow
            pu = 0.5 + 0.5 * math.sin(b * 10)
            layer(img, lambda d: (d.ellipse([x - 165, GY - 360, x + 165, GY + 24], fill=(110, 230, 90, int(50 + 25 * pu)), outline=(150, 255, 120, 235), width=8),
                                  d.arc([x - 125, GY - 330, x - 10, GY - 200], 200, 260, fill=(230, 255, 220, 230), width=7)))
            if b < 0.8: burst(img, x, GY - 170, (b - 0.5) / 0.3, (130, 240, 100), 12, 40, 200)
            if b < 1.5: text_layer(img, [(330, GY - 450, 'SHIELD!', 64, (130, 240, 100), 8, 255)])
        fk = min(8, int(max(0, b - 0.6) * 9)) if 0.6 <= b < 1.6 else 0
        if b >= 0.5: dragon(img, fk)
        if 0.9 < b < 1.8:
            once('fire1', t - 0.3, 'boom'); once('clang', t, 'boing')
            def sparks(d):
                rr = random.Random(f)
                for q in range(18):
                    a = rr.uniform(-1.3, 1.3); r = rr.uniform(40, 200)
                    sx, sy = x + 165 + r * math.cos(math.pi - a) * 0.5, GY - 170 + r * math.sin(a)
                    d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=rr.choice([(255, 200, 60, 230), (255, 120, 40, 230), (255, 240, 180, 230)]))
            layer(img, sparks)
        if b > 1.9: text_layer(img, [(478, 1290, 'STALEMATE...', 64, (255, 255, 255), 8, int(255 * min(1, (b - 1.9) / 0.25)))])
        if b > 2.2: text_layer(img, [(x + 60, GY - 430, '. . .', 44, (255, 255, 255), 6, 255), (820 + SH, GY - 430, '. . .', 44, (255, 255, 255), 6, 255)])
    else:
        if b < 0.5:
            put92(img, EAT[min(11, int(b / 0.5 * 12))], 300 + SH); dragon(img, 0)
        elif b < 1.2:
            once('pow', t, 'powerup2')
            fr_ = ATK[0]; x0_, y0_ = int(300 + SH - 45 * K), int(GY - 104 * K)
            strong_aura(img, fr_, x0_, y0_, b)
            def rings(d):
                for q in range(3):
                    r = 120 + q * 40 + 20 * math.sin(b * 12 + q)
                    d.ellipse([300 + SH - r * 0.7, GY - 200 - r, 300 + SH + r * 0.7, GY + 10], outline=(110, 180, 255, 170 - q * 45), width=10)
            layer(img, rings)
            img.alpha_composite(fr_, (x0_, y0_)); dragon(img, 0)
            if b < 0.8: burst(img, 300 + SH, GY - 200, (b - 0.5) / 0.3, (110, 180, 255), 12, 40, 200)
            text_layer(img, [(330, GY - 450, 'STRONG!', 64, (110, 180, 255), 8, 255)])
        elif b < 1.7:
            x = 300 + SH + 260 * ((b - 1.2) / 0.5); spr_ = RUN[fi % 8]; x0_, y0_ = int(x - spr_.width / 2), int(GY - 78 * K)
            strong_aura(img, spr_, x0_, y0_, b); img.alpha_composite(spr_, (x0_, y0_)); dragon(img, 0)
        elif b < 2.3:
            once('punch', t, 'punch')
            if b > 1.85: once('boom2', t, 'boom')
            ai = min(12, 1 + int((b - 1.7) * 20)); fr_ = ATK[ai]; x0_, y0_ = int(520 + SH - 45 * K), int(GY - 104 * K)
            strong_aura(img, fr_, x0_, y0_, b); img.alpha_composite(fr_, (x0_, y0_))
            kb = min(1, max(0, b - 1.85) / 0.25) * 90
            dragon(img, 0, shift=kb, tint=1.6 if 1.85 < b < 1.95 else None)
            if b > 1.85: text_layer(img, [(740 + SH, GY - 440, 'POW!', 80, (255, 220, 60), 9, 255)])
        else:
            vf = VICC[int(b * 8) % len(VICC)]; put92(img, vf, 520 + SH); dragon(img, 0, shift=90)
            cx = 40 + min(1, (b - 2.3) / 0.4) * 120; put92(img, CYI[fi % len(CYI)], cx)
            if b > 2.6: text_layer(img, [(max(cx, 130), GY - 410, 'NICE!', 44, (255, 180, 40), 7, 255)])
            for q in range(5):
                a = b * 5 + q * 1.256; sx, sy = 880 + SH + 70 * math.cos(a), GY - 330 + 25 * math.sin(a)
                text_layer(img, [(sx, sy, '*', 30, (255, 240, 120), 4, 255)])
            for q in range(10):
                rr = random.Random(q); vx, vy = rr.uniform(-500, -100), rr.uniform(-900, -500); tt = b - 2.3
                gx, gy = 860 + SH + vx * tt, GY - 120 + vy * tt + 1600 * tt * tt
                if gy < GY and gx > 90: g = GUMS[q % 4]; img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
            once('vic', t, 'victory')
            text_layer(img, [(478, 1290, 'VICTORY!', 90, (255, 214, 60), 10, int(255 * min(1, (b - 2.3) / 0.2)))])
    img.alpha_composite(HK1)
    wr.write(img)
    if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(OUT + f'pv_{f:04d}.png')
for im_ in OPEN: wr.write(im_)          # loop: cut back to the opening
wr.close()
ev.append((round(END0, 3), 'chime'))
json.dump(sorted(ev), open(OUT + 'ev53.json', 'w')); print('done', round(DUR + 0.3, 2))
