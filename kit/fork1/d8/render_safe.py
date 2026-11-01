import sys; sys.path.insert(0, '..')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
IDL = {g: idle(g, 3) for g in ['joy', 'cyrus', 'ray', 'hollow', 'cleo']}
CHEER = {g: seq(PL + f'maze/anim/{g}_panic', 1) for g in ['joy', 'cyrus', 'ray', 'hollow']}
CHEER = {g: [f.resize((276, 276), Image.NEAREST) for f in v] for g, v in CHEER.items()}
GUMS = [gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre']]
BG = bg_frames('hub.gif', (1920, 1080), step=2)
BGC = [Image.new('RGBA', (W, H), (176, 132, 88, 255))]
BGC[0].alpha_composite(BG[0].resize((W, 608), Image.NEAREST), (0, 0))
# crowd
crowd = []
y = 600
row = 0
while y < 2100:
    x = -40 + (row % 2) * 48
    while x < W + 40:
        g = rnd.choices(['joy', 'cyrus', 'ray', 'hollow'], [3, 3, 3, 2])[0]
        mode = 'cheer' if rnd.random() < 0.18 else 'idle'
        gum = rnd.choice(GUMS) if rnd.random() < 0.08 else None
        flip = rnd.random() < 0.5
        crowd.append(dict(g=g, x=x + rnd.uniform(-8, 8), y=y + rnd.uniform(-5, 5), ph=rnd.randrange(8), mode=mode, gum=gum, flip=flip))
        x += 96
    y += 76; row += 1
# hide Cleo: lower-middle, mid crowd, behind a row
cands = [c for c in crowd if 1000 < c['y'] < 1420 and 250 < c['x'] < 760]
cleo = rnd.choice(cands); cleo.update(g='cleo', mode='idle', gum=None)
print('cleo at', round(cleo['x']), round(cleo['y']))
crowd.sort(key=lambda c: c['y'])
T0 = 0.6; T_END = T0 + 10; DUR = T_END + 2.6
out = Writer('d8_safe_noaudio.mp4'); ev = [(0.0, 'cheer')]
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGC[0].copy()
    for c in crowd:
        if c['mode'] == 'cheer' and c['g'] != 'cleo':
            fr = CHEER[c['g']][(int(t * 10) + c['ph']) % 8]; bob = 0
        else:
            fr = IDL[c['g']][(int(t * 8) + c['ph']) % 6]; bob = 0
        if c['flip']: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        x, y = int(c['x']), int(c['y'])
        img.alpha_composite(fr, (x - 138, y - 234 + bob))
        if c['gum'] is not None:
            g = c['gum']; img.alpha_composite(g, (x - g.width // 2, y - 234 + 30 - g.height + int(5 * math.sin(t * 6 + c['ph']))))
    # header
    layer(img, lambda d: d.rectangle([0, 250, W, 478], fill=(14, 10, 24, 235)))
    text_layer(img, [(W / 2, 276, 'CAN YOU FIND CLEO?', 52, (255, 255, 255), 6, 255), (W / 2, 356, 'YOU HAVE 10 SECONDS', 34, (255, 214, 60), 5, 255)])
    ic = idle('cleo', 1)[0] if f == 0 else None
    rem = max(0, T_END - max(t, T0)); frac = rem / 10
    col = (90, 200, 80) if rem > 5 else ((255, 190, 50) if rem > 2 else (230, 60, 60))
    layer(img, lambda d: (d.rounded_rectangle([90, 418, W - 90, 456], 12, fill=(20, 14, 30, 255), outline=(255, 255, 255, 255), width=3),
                          d.rounded_rectangle([96, 424, 96 + (W - 192) * frac, 450], 8, fill=col + (255,)) if frac > 0.01 else None))
    if T_END - 3 <= t < T_END and (t - (T_END - 3)) % 1 < 1 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    if t >= T_END:
        u = t - T_END
        if u < 1 / FPS: ev.append((round(t, 3), 'buzz_8bit'))
        layer(img, lambda d: d.rectangle([0, 478, W, H], fill=(8, 6, 14, int(min(1, u / 0.25) * 110))))
        sc = 1 + 0.15 * max(0, 1 - u * 5)
        layer(img, lambda d: d.rounded_rectangle([140, 860, W - 140, 1090], 24, fill=(20, 14, 30, 240), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(W / 2, 900, "TIME'S UP!", int(64 * sc), (255, 214, 60), 8, 255), (W / 2, 1010, 'Did you find her?', 36, (255, 255, 255), 6, 255)])
    out.write(img)
    if f == 90: img.save('k3_safe.png')
out.close(); json.dump(ev, open('ev_safe.json', 'w')); print('done', DUR)
