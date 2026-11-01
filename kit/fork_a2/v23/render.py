import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
BG = bg_frames('bg_castle.gif', (W, H), box=(800 - 253, 0, 800 + 253, 900), step=1, bright=0.55, blur=2)
DR = gif_frames(A + 'dragon.gif', h=210)
CH = [('joy', 'JOY', 'acv'), ('cleo', 'CLEO', 'cre'), ('cyrus', 'CYRUS', 'mush'), ('ray', 'RAYLEIGH', 'mel'), ('hollow', 'THE HOLLOW', 'gold'), ('dragon', 'DRAGON', None)]
IDL = {g: idle(g, 3) for g, _, _ in CH if g != 'dragon'}
GM = {k: gummy(k, 2) for k in ('acv', 'cre', 'mush', 'mel', 'gold')}
TIERS = [('S', (235, 70, 70)), ('A', (245, 150, 50)), ('B', (245, 210, 60)), ('C', (110, 200, 90)), ('D', (80, 150, 240))]
X0, X1 = 50, W - 50; RY0 = 340; RH = 140; GAPR = 12
SHY = RY0 + 5 * (RH + GAPR) + 30; SHH = 420
DUR = 6.0; wr = Writer('v23_noaudio.mp4'); events = []
rng = random.Random(4); SP_ = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, 6.28)) for _ in range(40)]
for i in range(5): events.append((round(0.12 + i * 0.1, 3), 'tick_8bit'))
for j in range(6): events.append((round(0.85 + j * 0.12, 3), 'coin_8bit'))
events.append((2.1, 'chime'))
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2 + 14 * math.sin(t + p), x + 2, y + 2 + 14 * math.sin(t + p)], fill=(255, 240, 190, int(120 + 100 * math.sin(t * 3 + p)))) for x, y, p in SP_])
    # title
    layer(img, lambda d: d.rectangle([0, 90, W, 300], fill=(10, 6, 22, 170)))
    text_layer(img, [(W / 2, 128, 'RANK THE GUIDES', 60, (255, 214, 60), 8, 255), (W / 2, 222, 'Comment your tier list', 32, (255, 255, 255), 5, 255)])
    # tier rows slide in
    for i, (lt, col) in enumerate(TIERS):
        u = min(1, max(0, (t - 0.1 - i * 0.1) / 0.3)); ease = 1 - (1 - u) ** 3
        off = int((1 - ease) * -W)
        y = RY0 + i * (RH + GAPR)
        def row(d, y=y, off=off, col=col):
            d.rounded_rectangle([X0 + off, y, X1 + off, y + RH], 14, fill=(14, 10, 26, 210), outline=(255, 214, 60, 255), width=4)
            d.rounded_rectangle([X0 + off + 10, y + 10, X0 + off + 10 + RH - 20, y + RH - 10], 12, fill=col + (255,), outline=(20, 15, 35, 255), width=4)
            for k in range(5): d.rectangle([X0 + off + RH + 14 + k * 160, y + 18, X0 + off + RH + 14 + k * 160 + 144, y + RH - 18], outline=(80, 70, 110, 160), width=2)
        layer(img, row)
        text_layer(img, [(X0 + off + 10 + (RH - 20) / 2, y + 36, lt, 64, (255, 255, 255), 7, 255)])
        sh = (t * 0.5 + i * 0.15) % 2.0
        if sh < 0.4: layer(img, lambda d, y=y, sh=sh, off=off: d.rectangle([X0 + off + 10 + sh / 0.4 * (RH - 20) - 6, y + 12, X0 + off + 10 + sh / 0.4 * (RH - 20) + 6, y + RH - 12], fill=(255, 255, 255, 110)))
    # shelf with candidates
    layer(img, lambda d: d.rounded_rectangle([30, SHY, W - 30, SHY + SHH], 22, fill=(14, 10, 26, 220), outline=(255, 214, 60, 255), width=5))
    for j, (g, nm, gk) in enumerate(CH):
        cx = 30 + (W - 60) * (j + 0.5) / 6
        u = min(1, max(0, (t - 0.85 - j * 0.12) / 0.25))
        if u <= 0: continue
        sc = 0.4 + 0.6 * u
        if g == 'dragon': s = DR[int(t * 8) % len(DR)]
        else: s = IDL[g][int(t * 8 + j) % len(IDL[g])]
        if sc < 1: s = up(s, sc)
        feet = SHY + 350
        if g == 'dragon': img.alpha_composite(s, (int(cx - s.width / 2), int(feet - s.height)))
        else: img.alpha_composite(s, (int(cx - s.width / 2), int(feet - 78 * 3 * sc)))
        if gk and u >= 1:
            gg = GM[gk]; bob = int(5 * math.sin(t * 4 + j)); img.alpha_composite(gg, (int(cx - gg.width / 2), SHY + 18 + bob))
        text_layer(img, [(cx, SHY + 370, nm, 16 if len(nm) > 8 else 18, (255, 255, 255), 4, int(255 * u))])
    wr.write(img)
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': events}, open('v23_events.json', 'w')); print('done')
