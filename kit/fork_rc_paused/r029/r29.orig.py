import sys; sys.path.insert(0, '../fork1'); sys.path.insert(0, '../pixellab/safezone')
from hook import hook_layer
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sim29b import sim, NAMES, AX0, AY0, AX1, AY1, NT
HOOK, HB = hook_layer(['GUIDE BATTLE'], accent=0, sub='WHO WILL WIN?')
print('hook bottom', HB)
HDRB = 632
SEED = int(sys.argv[1])
FR, EV, END, LEAD = sim(SEED)
TEND = END[0]; WIN = NAMES[END[1]]; INTRO = 2.0
DUR = INTRO + len(FR) / FPS; NF = int(DUR * FPS)
print('winner', WIN, TEND, 'frames', len(FR), 'dur', DUR)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 40) for n in NAMES}
RUN = {g: seq(PL + f'race/{g}_run', 1, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}; RUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', 1, 1, 9)
RUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in RUN.items()}
FOOT = 78
G = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
VICF = vic(WIN, 420)
# ground from the PixelLab Wang tileset: dirt arena inside grass
meta = json.load(open('../fork3/arena/meta.json')); sheet = Image.open('../fork3/arena/sheet.png').convert('RGBA'); TILE = {}
for tt in meta['tileset_data']['tiles']:
    c = tt['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = tt['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
GY0 = 448; GC, GR = 17, 24; CX, CY = 540, (AY0 + AY1) / 2
def low(i, j):
    x, y = i * 64 - 4, GY0 + j * 64
    return ((x - CX) / 480) ** 2 + ((y - CY) / 470) ** 2 < 1.0 + 0.15 * math.sin(i * 1.3 + j * 2.1)
CORN = [[low(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (40, 80, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * 64 - 4, GY0 + j * 64))
HDR = bg_frames('vit_hd.gif', (1707, 960), step=2, bright=0.7); HDR = [b.crop((420, 120, 1500, 600)) for b in HDR]
w = Writer('v29_noaudio.mp4'); ev = []; lastpoof = -1
conv_by_frame = {}
for e in EV:
    conv_by_frame.setdefault(int(round(e[0] * FPS)), []).append(e)
for f in range(NF):
    t = f / FPS; st = t - INTRO; sf = max(0, min(len(FR) - 1, int(round(st * FPS))))
    units, gums = FR[sf]
    img = GROUND.copy()
    # gummies on the ground
    def gl(d):
        for g in gums:
            r = 42 + 6 * math.sin(t * 5); d.ellipse([g['x'] - r, g['y'] - r - 10, g['x'] + r, g['y'] + r - 10], fill=(255, 230, 140, 70))
    layer(img, gl)
    for g in gums:
        gi = G[g['k']]; b = int(6 * math.sin(t * 4 + g['x']))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height / 2 - 10 + b)))
    # shadows + shields
    def sh(d):
        for (k, x, y, vx, dist, shield, fl) in units:
            d.ellipse([x - 20, y - 6, x + 20, y + 6], fill=(0, 0, 0, 70))
            if shield:
                r = 34 + 4 * math.sin(t * 10); d.ellipse([x - r, y - r * 0.45, x + r, y + r * 0.45], outline=(255, 214, 60, 230), width=4)
    layer(img, sh)
    for (k, x, y, vx, dist, shield, fl) in sorted(units, key=lambda u: u[2]):
        g = NAMES[k]; ph = int(dist / 14) % 8 if st > 0 else 0
        spr = (RUNL if vx < 0 else RUN)[g][ph]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if 0 <= st - fl < 0.3:
            u = (st - fl) / 0.3; ds = up(DUST, 0.8 + 0.8 * u); al = ds.getchannel('A').point(lambda p: int(p * (1 - u))); ds.putalpha(al)
            img.alpha_composite(ds, (int(x - ds.width / 2), int(y - ds.height + 10)))
    # sparkles for shielded
    def sp(d):
        for (k, x, y, vx, dist, shield, fl) in units:
            if shield:
                for q in range(3):
                    a = t * 8 + q * 2.1 + x; sx, sy = x + 26 * math.cos(a), y - 40 + 30 * math.sin(a * 1.2)
                    d.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 245, 180, 230))
    layer(img, sp)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: (d.rectangle([0, 470, W, HDRB], fill=(10, 8, 20, 200)), d.rectangle([0, 0, W, 470], fill=(10, 8, 20, 120)), d.rectangle([0, HDRB - 6, W, HDRB + 2], fill=(255, 214, 60, 255))))
    cnt = [sum(1 for u in units if u[0] == k) for k in range(NT)]
    mx = max(cnt); leaders = [k for k in range(NT) if cnt[k] == mx]
    for k, n in enumerate(NAMES):
        x = W / 2 + (k - 1.5) * 220; y = HB + 76
        ic = ICON[n]
        if cnt[k] == 0: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(x - ic.width / 2), int(y - ic.height / 2)))
        if len(leaders) == 1 and leaders[0] == k and st > 0:
            def crown(d, x=x, y=y):
                cy = y - 62; d.polygon([(x - 26, cy + 14), (x - 26, cy - 8), (x - 13, cy + 2), (x, cy - 14), (x + 13, cy + 2), (x + 26, cy - 8), (x + 26, cy + 14)], fill=(255, 214, 60, 255), outline=(90, 60, 10, 255))
            layer(img, crown)
        text_layer(img, [(x, y + 52, str(cnt[k]), 40, RING[n] if cnt[k] else (120, 120, 130), 6, 255)])
    if t < INTRO:
        text_layer(img, [(W / 2, 980, 'PICK YOUR GUIDE!', 56, (255, 255, 255), 8, 255)])
    # sounds
    if st >= 0:
        for e in conv_by_frame.get(sf, []) if abs(st * FPS - sf) < 0.6 else []:
            if e[1] == 'conv' and t - lastpoof > 0.22: ev.append((round(t, 3), 'poof')); lastpoof = t
            if e[1] == 'gum': ev.append((round(t, 3), 'powerup_8bit'))
    if st >= TEND:
        u = st - TEND; a = min(1, u / 0.3)
        layer(img, lambda d: d.rectangle([0, HDRB + 2, W, H], fill=(8, 6, 14, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1440 - vf.height))
        text_layer(img, [(W / 2, 720, LABEL[WIN] + ' WINS!', 64, (255, 214, 60), 8, int(255 * a))])
        cr = random.Random(f)
        def conf(d):
            for _ in range(50):
                x = cr.uniform(0, W); y = HDRB + (cr.uniform(0, H) + u * 500) % (H - HDRB)
                d.rectangle([x, y, x + 12, y + 12], fill=cr.choice([(255, 214, 60, 255), (255, 120, 120, 255), (120, 220, 120, 255), (150, 180, 255, 255)]))
        layer(img, conf)
        if not any(e[1] == 'victory' for e in ev): ev.append((round(t, 3), 'victory'))
    img.alpha_composite(HOOK)
    w.write(img)
    if f % 150 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/e_{f:04d}.png')
w.close(); json.dump({'events': ev}, open('v29_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
