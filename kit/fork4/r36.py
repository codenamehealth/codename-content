import sys, os, math, random, json
sys.path.insert(0, '../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 5
ATK = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(PL + 'race/cyrus_atk/*.png'))]   # 384 canvas, feet ~ y 104*3
CFOOT = 104 * K
DUMMY = up(crop(Image.open('dummy/00.png').convert('RGBA')), 7)
BGF = bg_frames('vit_hd.gif', (W, H), box=(520, 0, 1127, 1080), step=2, bright=0.9)
GUM = gummy('mush', 4)
CX, CY = 300, 1760           # Cyrus feet
DX, DY = 830, 1760           # dummy base
# levels: (start, dur, speed per s, stop value, label, verdict)
LV = [dict(t0=1.2, dur=3.6, sp=34.0, stop=21, label='LEVEL 1/3', sub='Slow. Pause on 99.', verdict='WAY OFF', bar=True),
      dict(t0=6.0, dur=2.2, sp=62.0, stop=67, label='LEVEL 2/3', sub='Faster. Pause on 99.', verdict='SO CLOSE', bar=True),
      dict(t0=10.8, dur=1.3, sp=140.0, stop=5, label='LEVEL 3/3', sub='Energy gummy. No bar.', verdict='MISSED IT', bar=False)]
T_GUM = 9.5; END = 15.6
# choose start offsets so that exactly one frame of each level shows 99
for L in LV:
    best = None
    for off in [i * 0.05 for i in range(0, 2000)]:
        vals = [int(off + L['sp'] * (k / FPS)) for k in range(int(L['dur'] * FPS))]
        if vals[-1] % 100 != L['stop']: continue
        hits = sum(1 for v in vals if v % 100 == 99)
        if hits == 1 and (best is None): best = off
    if best is None:
        # fallback: no exact stop match; take first with one 99 frame
        for off in [i * 0.05 for i in range(0, 2000)]:
            vals = [int(off + L['sp'] * (k / FPS)) for k in range(int(L['dur'] * FPS))]
            if sum(1 for v in vals if v % 100 == 99) == 1: best = off; break
    L['off'] = best; vals = [int(best + L['sp'] * (k / FPS)) % 100 for k in range(int(L['dur'] * FPS))]
    L['stop'] = vals[-1]; L['hit99'] = [k for k, v in enumerate(vals) if v == 99]
    print(L['label'], 'off', round(best, 2), 'stop', L['stop'], '99 at frame', L['hit99'])
def level_at(t):
    for i, L in enumerate(LV):
        if L['t0'] <= t < L['t0'] + L['dur']: return i, 'run'
        if L['t0'] + L['dur'] <= t < L['t0'] + L['dur'] + 1.2: return i, 'hit'
    return None, None
W_ = Writer('d36_noaudio.mp4'); ev = []
F_BIG = 230
for f in range(int(END * FPS)):
    t = f / FPS; img = BGF[int(t * 6) % len(BGF)].copy()
    li, ph = level_at(t)
    # floor shadow + dummy
    layer(img, lambda d: (d.ellipse([CX - 130, CY - 24, CX + 170, CY + 24], fill=(0, 0, 0, 90)), d.ellipse([DX - 140, DY - 22, DX + 140, DY + 22], fill=(0, 0, 0, 90))))
    shake = 0
    if ph == 'hit':
        u = t - (LV[li]['t0'] + LV[li]['dur']); shake = int(22 * math.exp(-u * 4) * math.sin(u * 40)) if u > 0.18 else 0
    dm = DUMMY.rotate(-shake * 0.4, resample=Image.NEAREST, center=(DUMMY.width // 2, DUMMY.height), expand=False)
    img.alpha_composite(dm, (DX - DUMMY.width // 2 + shake, DY - DUMMY.height))
    # Cyrus
    if ph == 'hit':
        u = t - (LV[li]['t0'] + LV[li]['dur']); k = min(12, int(u * 16) + 1); spr = ATK[k]
        key = ('punch', li)
        if key not in [e[2] for e in ev if len(e) > 2]:
            ev.append((round(t + 0.12, 3), 'punch', key)); ev.append((round(t + 0.18, 3), 'sword_hit', ('h', li)))
    else:
        spr = ATK[1] if ph == 'run' else ATK[0]
        if ph == 'run':
            # charging aura
            L = LV[li]; v = int(L['off'] + L['sp'] * (t - L['t0'])) % 100; pw = v / 99
            def aura(d, pw=pw):
                for q in range(5):
                    r = 120 + q * 26 + 14 * math.sin(t * 20 + q)
                    d.ellipse([CX + 30 - r, CY - 230 - r, CX + 30 + r, CY - 230 + r], outline=(255, 170 + q * 15, 60, int(50 + 140 * pw) - q * 20), width=6)
            layer(img, aura)
    img.alpha_composite(spr, (CX - spr.width // 2 + 40, CY - CFOOT))
    # energy gummy moment
    if T_GUM <= t < T_GUM + 1.3:
        u = (t - T_GUM) / 0.6
        if u < 1:
            gx = 540 + (CX - 540) * u; gy = 900 + (CY - 360 - 900) * u - 240 * math.sin(math.pi * u)
            img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        else:
            layer(img, lambda d: [d.ellipse([CX + 30 - r, CY - 230 - r, CX + 30 + r, CY - 230 + r], outline=(255, 200, 80, max(0, 255 - r // 2)), width=10) for r in range(int((u - 1) * 500), int((u - 1) * 500) + 90, 30)])
            text_layer(img, [(CX + 200, CY - 620, 'ENERGY UP!', 50, (255, 170, 50), 7, 255)])
        if not any(e[1] == 'powerup_8bit' for e in ev): ev.append((round(T_GUM + 0.6, 3), 'powerup_8bit'))
    # header + meter window
    layer(img, lambda d: d.rectangle([0, 0, W, 300], fill=(14, 10, 24, 190)))
    text_layer(img, [(W / 2, 60, 'PAUSE THE VIDEO', 66, (255, 255, 255), 7, 255), (W / 2, 160, 'ON 99', 92, (255, 214, 60), 9, 255)])
    if li is not None:
        L = LV[li]
        if ph == 'run':
            v = int(L['off'] + L['sp'] * (t - L['t0'])) % 100
            if not any(e[1] == 'reeltick_8bit' and abs(e[0] - t) < 0.15 for e in ev): ev.append((round(t, 3), 'reeltick_8bit'))
        else: v = L['stop']
        def win(d):
            d.rounded_rectangle([140, 360, W - 140, 900], 28, fill=(16, 12, 30, 225), outline=(255, 214, 60, 255), width=8)
            d.rounded_rectangle([156, 376, W - 156, 884], 22, outline=(120, 90, 30, 255), width=3)
        layer(img, win)
        text_layer(img, [(W / 2, 400, L['label'], 40, (255, 214, 60), 5, 255), (W / 2, 456, L['sub'], 28, (220, 220, 230), 4, 255)])
        jit = (random.Random(f).randint(-6, 6) if (li == 2 and ph == 'run') else 0)
        col = (255, 255, 255) if ph == 'run' else (255, 120, 90)
        text_layer(img, [(W / 2 + jit, 520, f'{v:02d}', F_BIG, col, 12, 255)])
        if L['bar']:
            def bar(d, v=v):
                x0, x1, y = 220, W - 220, 820
                d.rounded_rectangle([x0, y - 22, x1, y + 22], 12, fill=(40, 30, 60, 255), outline=(255, 255, 255, 255), width=4)
                xx = x0 + 8 + (x1 - x0 - 16) * v / 99
                d.rounded_rectangle([x0 + 8, y - 14, xx, y + 14], 8, fill=(255, 150 + int(100 * v / 99), 40, 255))
                d.polygon([(x1 - 8, y - 46), (x1 - 26, y - 70), (x1 + 10, y - 70)], fill=(255, 80, 80, 255))
            layer(img, bar); text_layer(img, [(W - 228, 720, '99', 26, (255, 120, 120), 4, 255)])
        if ph == 'hit':
            u = t - (L['t0'] + L['dur'])
            if u > 0.2:
                a = int(255 * min(1, (1.2 - u) / 0.3)) if u > 0.9 else 255
                text_layer(img, [(DX, DY - 600 - u * 60, str(v), 90, (255, 90, 70), 9, a), (DX, DY - 500 - u * 30, L['verdict'] + '!', 40, (255, 255, 255), 6, a)])
    elif t < LV[0]['t0']:
        text_layer(img, [(W / 2, 600, 'PLAY ALONG', 70, (255, 255, 255), 8, 255), (W / 2, 700, 'Screenshot it if you hit 99', 32, (255, 214, 60), 5, 255)])
    elif t >= LV[2]['t0'] + LV[2]['dur'] + 1.2:
        u = t - (LV[2]['t0'] + LV[2]['dur'] + 1.2)
        layer(img, lambda d: d.rectangle([0, 300, W, H], fill=(10, 6, 20, int(170 * min(1, u / 0.3)))))
        layer(img, lambda d: d.rounded_rectangle([120, 560, W - 120, 1080], 28, fill=(16, 12, 30, 235), outline=(255, 214, 60, 255), width=8))
        text_layer(img, [(W / 2, 640, 'DID YOU', 80, (255, 255, 255), 8, 255), (W / 2, 750, 'GET 99?', 80, (255, 214, 60), 8, 255), (W / 2, 900, 'Comment your number', 36, (255, 255, 255), 5, 255), (W / 2, 970, "Send it to someone who can't", 26, (200, 200, 220), 4, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(t, 3), 'ding_8bit'))
    W_.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/b_{f:04d}.png')
W_.close()
json.dump([e[:2] for e in ev], open('d36_ev.json', 'w')); print('done', END)
