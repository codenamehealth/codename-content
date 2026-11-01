import sys; sys.path.insert(0, '..')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(4)
K = 3; GY = 1500
ATK = {g: seq(PL + f'race/{g}_atk', K, 0) for g in ['cleo', 'joy', 'ray', 'cyrus']}      # 13 frames, feet at (30,104) in 128 canvas
FX = {'ray': 300, 'joy': 470, 'cyrus': 640, 'cleo': 800}
HX = 120
SL_IDLE = seq(PL + 'race/slime_idle_c', 3, 1); SL_SPLAT = seq(PL + 'race/slime_splat_c', 3, 1)
HOLLOW = [f.resize((276, 276), Image.NEAREST) for f in seq(PL + 'maze/anim/hollow_panic', 1, 1)]
HIDLE = idle('hollow', K)
VICS = {g: vic(g, 215) for g in ['cleo', 'joy', 'ray', 'cyrus', 'hollow']}
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
GUM = gummy('mush', 3)
jars = Image.open(A + 'jars.png').convert('RGBA'); POTION = up(crop(jars.crop((0, 0, 200, 200))), 1)
POTION = POTION.resize((POTION.width // 2, POTION.height // 2), Image.NEAREST)
def face(name, rad):
    SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
    RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), m); return b
FACE = {g: face(g, 52) for g in ['joy', 'cleo']}
sun = Image.open(A + 'sun_hd.gif'); BG = []
for i in range(0, sun.n_frames, 2):
    sun.seek(i); BG.append(sun.convert('RGB').resize((3413, 1920), Image.NEAREST).crop((1166, 0, 1166 + W, H)).convert('RGBA'))
SLX = 975
# timeline
T_SL_IN = 0.3; T_FIGHT = 1.2
ATK_T = {'cleo': T_FIGHT, 'cyrus': T_FIGHT + 0.25, 'joy': T_FIGHT + 0.5, 'ray': T_FIGHT + 0.75}
ATK_D = 0.75; IMPACT = {'cleo': 5, 'cyrus': 3, 'joy': 4, 'ray': 6}
T_POOF = T_FIGHT + 0.75 + ATK_D; T_VIC = T_POOF + 0.5
T_D1 = T_VIC + 1.1; LINE1 = 'I used every potion we had.'; T_D2 = T_D1 + 2.3; LINE2 = 'Worth it.'; DUR = T_D2 + 2.4
out = Writer('d12_noaudio.mp4'); ev = []
def once(name, t0, t):
    if t0 <= t < t0 + 1 / FPS and (round(t0, 3), name) not in ev: ev.append((round(t0, 3), name))
hits = sorted((ATK_T[g] + IMPACT[g] / 13 * ATK_D, g) for g in ATK_T) + [(T_FIGHT + 0.15 + 0.12 * k, 'extra') for k in range(0)]
POT0 = 12
for f in range(int(DUR * FPS)):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    shake = 0
    for ht, g in hits:
        if 0 <= t - ht < 0.12: shake = 10
    sx = int(rnd.uniform(-shake, shake)); sy = int(rnd.uniform(-shake, shake))
    wl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # shadows
    layer(wl, lambda d: [d.ellipse([x - 55, GY - 12, x + 55, GY + 12], fill=(60, 30, 0, 70)) for x in list(FX.values()) + [HX]])
    # party
    if t < T_VIC:
        for g, x in FX.items():
            u = t - ATK_T[g]; i = 0 if u < 0 else min(12, int(u / ATK_D * 13))
            fr = ATK[g][i]; wl.alpha_composite(fr, (x - 30 * K, GY - 104 * K))
        fr = HOLLOW[int(t * 12) % 8] if t >= T_FIGHT else HIDLE[int(t * 8) % 6]
        wl.alpha_composite(fr, (HX - fr.width // 2, GY - 78 * K))
    else:
        for g, x in list(FX.items()) + [('hollow', HX)]:
            vf = VICS[g][(int((t - T_VIC) * 8) + hash(g) % 4) % len(VICS[g])]
            wl.alpha_composite(vf, (x - vf.width // 2, GY - vf.height + 4))
    # slime
    if t < T_POOF:
        hop = abs(math.sin(t * 5)) * 30 if t < T_FIGHT else 0
        x = SLX + (1 - min(1, (t - T_SL_IN) / 0.8)) * 260 if t < T_SL_IN + 0.8 else SLX
        fr = SL_IDLE[int(t * 10) % len(SL_IDLE)]
        if any(0 <= t - ht < 0.15 for ht, g in hits): fr = ImageEnhance.Brightness(fr).enhance(2.2)
        wl.alpha_composite(fr, (int(x - fr.width / 2), int(GY - fr.height + 8 - hop)))
    elif t < T_POOF + 0.6:
        v = (t - T_POOF) / 0.6; fr = SL_SPLAT[min(len(SL_SPLAT) - 1, int(v * len(SL_SPLAT)))]
        wl.alpha_composite(fr, (SLX - fr.width // 2, GY - fr.height + 8))
        du = up(DUST, 4 + 3 * v); al = du.getchannel('A').point(lambda p: int(p * (1 - v))); du.putalpha(al)
        wl.alpha_composite(du, (SLX - du.width // 2, GY - du.height + 30))
    # gummy drop
    if t >= T_POOF + 0.2:
        v = min(1, (t - T_POOF - 0.2) / 0.5); by = GY - 10 - GUM.height - 140 * math.sin(v * math.pi) * (1 - 0.3 * v)
        wl.alpha_composite(GUM, (SLX - GUM.width // 2, int(by)))
    img.alpha_composite(wl.transform(wl.size, Image.AFFINE, (1, 0, -sx, 0, 1, -sy)) if shake else wl)
    # hit sparks and damage numbers
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); items = []
    for ht, g in hits:
        u = t - ht
        if 0 <= u < 0.25:
            col = {'cleo': (230, 240, 255), 'cyrus': (255, 190, 60), 'joy': (140, 230, 90), 'ray': (230, 120, 255)}[g]
            for k in range(10):
                a = k * 0.628 + hash(g) % 7; r = 20 + u * 500
                px, py = SLX + r * math.cos(a), GY - 60 + r * 0.7 * math.sin(a)
                d.rectangle([px - 6, py - 6, px + 6, py + 6], fill=col + (int(255 * (1 - u / 0.25)),))
        if 0 <= u < 0.8:
            items.append((SLX - 20 + 45 * (hits.index((ht, g)) - 1.5), GY - 300 - u * 110, '1', 72, (255, 255, 255), 6, int(255 * min(1, (0.8 - u) / 0.3))))
            once({'cleo': 'sword_hit', 'cyrus': 'punch', 'joy': 'swish', 'ray': 'twinkle'}[g], round(ht, 3), t)
    img.alpha_composite(L)
    for g in ATK_T: once('sword_swish' if g == 'cleo' else 'swish', round(ATK_T[g], 3), t)
    # HUD
    pots = POT0 if t < T_FIGHT else max(0, POT0 - int((t - T_FIGHT) / 0.11))
    layer(img, lambda d: d.rounded_rectangle([40, 440, 360, 540], 16, fill=(20, 14, 30, 220), outline=(255, 214, 60, 255), width=4))
    img.alpha_composite(POTION, (58, 490 - POTION.height // 2))
    items.append((240, 470, f'x{pots}', 44, (255, 90, 90) if pots == 0 else (255, 255, 255), 6, 255))
    if T_FIGHT <= t < T_FIGHT + POT0 * 0.11 and abs(((t - T_FIGHT) / 0.11) % 1) < 0.34: once('tick_8bit', round(t, 3), t)
    layer(img, lambda d: d.rectangle([0, 150, W, 380], fill=(14, 10, 24, 130)))
    items += [(W / 2, 195, 'Our party after beating', 44, (255, 255, 255), 6, 255), (W / 2, 275, 'a level 1 slime', 44, (255, 255, 255), 6, 255)]
    if t >= T_POOF:
        u = t - T_POOF; s = int(64 * (1.3 - 0.3 * min(1, u * 5)))
        layer(img, lambda d: d.rounded_rectangle([170, 620, W - 170, 760], 18, fill=(20, 14, 30, 235), outline=(255, 214, 60, 255), width=5))
        items.append((W / 2, 660, 'VICTORY! +2 XP', min(s, 54), (255, 214, 60), 7, 255))
        once('victory', round(T_POOF, 3), t)
    if t >= T_POOF + 0.7:
        u = t - T_POOF - 0.7; items.append((SLX - 120, GY - 330 - min(1, u) * 40, '+1 GUMMY', 40, (255, 230, 150), 5, int(255 * max(0, min(1, (1.8 - u) / 0.4)))))
        once('coin_8bit', round(T_POOF + 0.7, 3), t)
    text_layer(img, items)
    # dialogue
    for (td, who, line, tend) in ((T_D1, 'joy', LINE1, T_D2), (T_D2, 'cleo', LINE2, DUR + 1)):
        if td <= t < tend:
            n = min(len(line), int((t - td) * 26))
            layer(img, lambda d: (d.rounded_rectangle([40, 1520, W - 40, 1780], 20, fill=(16, 18, 52, 245), outline=(240, 240, 255, 255), width=6),
                                  d.rounded_rectangle([60, 1478, 330, 1530], 10, fill=(240, 240, 255, 255))))
            img.alpha_composite(FACE[who], (70, 1555))
            dd = ImageDraw.Draw(img)
            dd.text((80, 1490), who.upper(), font=F(30), fill=(20, 18, 52))
            words = line[:n]
            # wrap at ~20 chars
            lines = []; cur = ''
            for wd in line.split(' '):
                if len(cur) + len(wd) + 1 > 19: lines.append(cur); cur = wd
                else: cur = (cur + ' ' + wd).strip()
            lines.append(cur); shown = []; left = n
            for ln in lines:
                shown.append(ln[:max(0, left)]); left -= len(ln) + 1
            for k, ln in enumerate(shown): dd.text((200, 1570 + k * 66), ln, font=F(40), fill=(255, 255, 255))
            if n % 3 == 1 and n < len(line): once('tick_8bit', round(td + (n - 1) / 26, 3), t)
    out.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close(); json.dump(ev, open('ev.json', 'w')); print('done', DUR, len(ev))
