import sys, os; os.chdir('../../fork_b5/v53'); OUT='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n9/v53/'; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '../../pixellab/safezone')
from common import *
from hook import hook_layer
sys.path.insert(0, '../../fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, '../../fork_rc2'); from rc2 import acv_gloss
sys.path.insert(0, '../../fork_c7'); from powers import *
# rc18: comment prompt as a 44px second line of the hook band from frame 0 (was a 36px line only on the intro/end card)
from hook import hook_band
# hfg5: full-width translucent strip (gold CHEST on the gold temple needs the darker backing; fade was too weak here), no box/border;
# 'Comment 1, 2 or 3' sub cut from both hooks (caption asks); end swap kept (replaces the hook, no extra line)
# n9 (Oct 29 notes2): Bennett 'hook could be will he survive or something or i feel bad for the dragon'. Hook = the job (will the
# little Hollow survive the dragon?); after the STRENGTH punch the same strip swaps to the expectation break: I FEEL BAD / FOR THE DRAGON.
HK1, HB1 = hook_band(['WILL HE', 'SURVIVE?'], accent=1, size=64, alpha=180)
HK2, HB2 = hook_band(['I FEEL BAD', 'FOR THE DRAGON'], accent=1, size=64, alpha=180); print('HB', HB1, HB2)
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
EAT_ACV = EAT 
                    # rc18: the unrecoloured eat sprite's red gummy = Syeda's apple-shaped ACV gummy
EAT = [pinkify(f) for f in EAT]
def mushify(im):   # n9 review2: the eaten gummy recoloured to the mushroom gummy's orange for chest 1
    a = np.array(im).astype(int); r, g, b_ = a[..., 0], a[..., 1], a[..., 2]; m = (r > 140) & (g < 120) & (b_ < 120) & (a[..., 3] > 0)
    a[..., 1][m] = (r[m] * 0.58).astype(int); a[..., 2][m] = (r[m] * 0.22).astype(int)
    return Image.fromarray(a.astype(np.uint8))
EAT_MUSH = [mushify(f) for f in EAT_ACV]
MUSHG = crop(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'))
CYI = idle('cyrus', K)
IDLE = idle('hollow', K)
VICC = [up(f.resize((92, 92), Image.NEAREST), K) for f in gif_frames(A + VIC['hollow'])]
DF = seq('../../fork_c7/assets/dragonfire_gum', 1, 0, 9)   # hoard = gummy pile (no gold)
CHC = crop(Image.open('../chest_closed/14.png').convert('RGBA'))
CHO = [crop(Image.open(p).convert('RGBA')) for p in sorted(glob.glob('../chest_open/*.png'))][2:]   # n9: skip the gold-coin-pile frames; light only
STICK = crop(Image.open('../stick/01.png').convert('RGBA')); SHIELD = crop(Image.open('../shield/02.png').convert('RGBA'))
GUM = crop(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'))   # creatine: STRENGTH (SPEC 12)
ACV = crop(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')))   # rc18: chest 2 is the ACV gummy (SHIELD), not a plain shield
ITEMS = [(MUSHG, '', 'MUSH'), (ACV, '', 'ACV'), (GUM, '', 'CREATINE')]   # n9: no gummy name tags (consistency rule)
ENDLAB = [['MUSH'], ['ACV', 'GUMMY'], ['CREATINE', 'GUMMY']]; ITK = [9, 9, 9]; ENDK = [4, 5, 5]
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
S0 = 2.6; RV = 1.0; ACT = [3.0, 2.1, 5.4]   # n9 review2: shield idle -0.4s; chest 3 has the walk-up + held wind-up   # n9: setup 0.45 -> 2.6s; stalemate beat -0.4s (line cut); victory holds for the swap
ST = [S0, S0 + RV + ACT[0], S0 + 2 * RV + ACT[0] + ACT[1]]; END0 = ST[2] + RV + ACT[2]; DUR = END0; NF = int(DUR * FPS)   # n9: recap end card cut (the hook swap is the ending)
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
            # n9 setup: the arena, the dragon on its gummy hoard, the Hollow, three chests on the floor in front. Dragon growls
            # (mouth-flame frames only) at 0.7-1.5s and the Hollow panics; chests rattle from 1.5s, chest 1 glows from 2.0s.
            img = BG[int(t * 6) % len(BG)].copy()
            gk = 0 if not (0.7 <= t < 1.5) else [1, 2, 2, 2, 2, 1][min(5, int((t - 0.7) / 0.8 * 6))]
            dragon(img, gk)
            if 0.7 <= t < 1.5: once('growl', t, 'poof')
            hfr = PANIC[fi % len(PANIC)] if 0.85 <= t < 1.75 else IDLE[fi % len(IDLE)]
            put92(img, hfr, 210)
            for k, x in enumerate([240, 480, 720]):
                c = up(CHC, 5); bob = 0; sh = 0
                if t >= 1.5: bob = int(5 * math.sin(t * 5 + k)); sh = int(6 * math.sin(t * 55 + k * 2))
                if k == 0 and t > 2.0:
                    gl = min(1, (t - 2.0) / 0.4)
                    layer(img, lambda d, x=x, gl=gl: [d.ellipse([x - 120 - q, 1230 - q, x + 120 + q, 1420 + q], fill=(255, 220, 110, int(60 * gl))) for q in (0, 24)])
                    sh = int(12 * math.sin(t * 70))
                cy = 1400 - c.height
                img.alpha_composite(c, (int(x - c.width / 2 + sh), cy + bob)); text_layer(img, [(x, cy + c.height - 78, str(k + 1), 56, (255, 214, 60), 8, 255)])
        else:
            u = t - END0
            for k, x in enumerate([230, 540, 840]):
                c = up(CHO[-1], 4); img.alpha_composite(c, (int(x - c.width / 2), 760))
                it = up(ITEMS[k][0], ENDK[k]); bob = int(8 * math.sin(t * 4 + k))
                img.alpha_composite(it, (int(x - it.width / 2), 732 - it.height + bob))
                # number on the chest front, item label under it, all above y1110 (lower-right safe zone)
                text_layer(img, [(x, 880, str(k + 1), 60, (255, 214, 60), 9, 255)])     # hfg5: item labels under the chests cut (items shown above them)
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
            if label: text_layer(img, [(W / 2 if len(label) < 13 else 478, 1220, label, 52 if len(label) < 13 else 46, (255, 255, 255), 7, int(255 * rise))])   # hfg5: WOODEN STICK label cut (it's a stick); gummy names kept
        if u < 0.1: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(180 * (1 - u / 0.1)))))
        img.alpha_composite(HK1)
        wr.write(img); continue
    b = u - RV
    img = BG[int(t * 6) % len(BG)].copy()
    # hfg5: 'CHEST N: ITEM' plate under the hook cut (repeats the reveal card)
    if k == 0:
        # n9 review2: chest 1 is the mushroom gummy: eat it, SPEED! dash with speed lines, then he still gets roasted
        if b < 0.5:
            put92(img, EAT_MUSH[min(11, int(b / 0.5 * 12))], 170); dragon(img, 0)
        elif b < 0.85:
            once('speed', t, 'powerup_8bit')
            v = (b - 0.5) / 0.35; x = 170 + (500 + SH - 170) * v; spr_ = RUN[int(t * 24) % 8]
            for q in range(4):
                xq = 170 + (500 + SH - 170) * max(0, v - (q + 1) * 0.08)
                img.alpha_composite(tinted(spr_, (255, 170, 50), int(255 * (0.4 - 0.08 * q))), (int(xq - spr_.width / 2), int(GY - 78 * K)))
            layer(img, lambda dd, x=x: [dd.rectangle([x - 110 - 50 * q - (q * 37 + int(t * 90)) % 60, GY - 230 + q * 45 - 5, x - 110 - 50 * q + 80, GY - 230 + q * 45 + 5], fill=(255, 240, 200, 220)) for q in range(4)]
                  + [dd.ellipse([x - 50 - q * 36 - 18, GY - 16 - q * 5, x - 50 - q * 36 + 18, GY + 10], fill=(210, 190, 150, 170 - q * 40)) for q in range(3)])
            put92(img, spr_, x); dragon(img, 0)
        elif b < 1.0:
            put_atk(img, ATK[0], 500 + SH); dragon(img, 0)
        if 0.5 <= b < 1.3: text_layer(img, [(330, GY - 450, 'SPEED!', 64, (255, 170, 50), 8, int(255 * min(1, (1.3 - b) / 0.2)))])
        if b < 1.0: pass
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
                pass   # hfg5: 'OOPS...' cut (it floated over the Hollow and read as him talking; the panic + smoke show it)
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
        if False: text_layer(img, [(478, 1290, 'STALEMATE...', 64, (255, 255, 255), 8, int(255 * min(1, (b - 1.9) / 0.25)))])
        # hfg5: '. . .' over both cut (STALEMATE... says it)
    else:
        # n9 review2: walk up to the dragon, wind up (held), punch connects, POW on contact, loot gummies spill out after the hit
        HX = 420; T_RUN0, T_RUN1, T_WIND, T_HIT, T_VIC = 1.2, 1.8, 1.8, 2.2, 2.75
        if b < 0.5:
            put92(img, EAT[min(11, int(b / 0.5 * 12))], 300 + SH); dragon(img, 0)
        elif b < T_RUN0:
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
            text_layer(img, [(390, GY - 450, 'STRENGTH!', 64, (255, 230, 90), 8, 255)])
        elif b < T_RUN1:
            x = 300 + SH + (HX - 300 - SH) * ((b - T_RUN0) / (T_RUN1 - T_RUN0)); spr_ = RUN[fi % 8]; x0_, y0_ = int(x - spr_.width / 2), int(GY - 78 * K)
            strong_aura(img, spr_, x0_, y0_, b); img.alpha_composite(spr_, (x0_, y0_)); dragon(img, 0)
        elif b < T_VIC:
            if b < T_HIT: ai = 1 if b < T_WIND + 0.2 else 2                      # wind-up held a beat
            else: ai = min(9, 3 + int((b - T_HIT) / 0.09))
            fr_ = ATK[ai]; x0_, y0_ = int(HX - 45 * K), int(GY - 104 * K)
            kb = min(1, max(0, b - T_HIT) / 0.2) * 90
            dragon(img, 0, shift=kb, tint=1.7 if T_HIT <= b < T_HIT + 0.1 else None)
            strong_aura(img, fr_, x0_, y0_, b); img.alpha_composite(fr_, (x0_, y0_))
            if b >= T_HIT:
                once('punch', t, 'punch'); once('boom2', t + 0.03, 'boom')
                cx_, cy_ = HX + 255, GY - 215
                if b < T_HIT + 0.25: burst(img, cx_, cy_, (b - T_HIT) / 0.25, (255, 220, 60), 14, 30, 220)
                text_layer(img, [(cx_ + 20, cy_ - 210, 'POW!', 80, (255, 220, 60), 9, 255)])
        else:
            vf = VICC[int(b * 8) % len(VICC)]; put92(img, vf, HX); dragon(img, 0, shift=90)
            for q in range(5):
                a = b * 5 + q * 1.256; sx, sy = 880 + SH + 70 * math.cos(a), GY - 330 + 25 * math.sin(a)
                text_layer(img, [(sx, sy, '*', 30, (255, 240, 120), 4, 255)])
            once('vic', t, 'victory')
            if b < T_VIC + 1.0: text_layer(img, [(478, 1290, 'VICTORY!', 90, (255, 214, 60), 10, int(255 * min(1, (b - T_VIC) / 0.2, (T_VIC + 1.0 - b) / 0.25)))])
        if b >= T_HIT:      # loot: gummies spill out of the hoard only after the hit, arc out and land on the floor
            for q in range(10):
                rr = random.Random(q); vx, vy = rr.uniform(-520, -120), rr.uniform(-900, -500); tt = min(b - T_HIT, 2.0)
                land = GY - 6 - rr.uniform(0, 40)
                gx, gy = 860 + SH + vx * tt, GY - 120 + vy * tt + 1600 * tt * tt
                if gy >= land:   # landed: stays where it fell
                    tl = (-vy - math.sqrt(max(0, vy * vy - 4 * 800 * (GY - 120 - land) * -1 * -1))) if False else None
                    # solve landing time
                    a_, b_, c_ = 1600, vy, GY - 120 - land; disc = b_ * b_ - 4 * a_ * c_
                    tl = (-b_ + math.sqrt(max(0, disc))) / (2 * a_); gx, gy = 860 + SH + vx * tl, land
                g = GUMS[q % 4]; img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    img.alpha_composite(HK2 if (k == 2 and b >= 3.55) else HK1)
    if k == 2 and abs(b - 3.55) < 0.5 / FPS: once('swap', t, 'twinkle')
    wr.write(img)
    if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(OUT + f'pv_{f:04d}.png')
for im_ in OPEN: wr.write(im_)          # loop: cut back to the opening
wr.close()
json.dump({'events': sorted(ev)}, open(OUT + 'ev53.json', 'w')); print('done', round(DUR + 0.3, 2))
