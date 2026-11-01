import sys, os, math, random, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 6   # Cyrus 5x -> 6x (~384px)
ATK = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(PL + 'race/cyrus_atk/*.png'))]   # 384 canvas, feet ~ y 104*3
CFOOT = 104 * K
DUMMY = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/dummy/00.png').convert('RGBA')), 7)
BGF = bg_frames('vit_hd.gif', (W, H), box=(520, 0, 1127, 1080), step=2, bright=0.9)
GUM = gummy('mush', 5)
CX, CY = 315, 1480           # Cyrus feet (x moved in so the 6x sprite stays inside x>=72)
DX, DY = 740, 1480           # dummy base
# levels: (start, dur, speed per s, stop value, label, verdict)
LV = [dict(t0=0.0, dur=3.4, sp=34.0, stop=21, label='LEVEL 1/3', sub='SLOW', verdict='WAY OFF', bar=True),
      dict(t0=4.6, dur=2.2, sp=62.0, stop=67, label='LEVEL 2/3', sub='FASTER', verdict='SO CLOSE', bar=True),
      dict(t0=8.6, dur=1.3, sp=140.0, stop=78, label='LEVEL 3/3', sub='NO BAR', verdict='MISSED IT', bar=False)]
T_GUM = 8.0; END = 12.4   # counter runs from frame 0; gummy beat 0.6s with the HUD up; end card 1.3s
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
    if T_GUM <= t < LV[2]['t0']: return 2, 'pre'
    return None, None
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
HOOK, HB = hook_layer2(['Pause the video', 'on 99'], accent=1, sub='Comment your number'); print('hook bottom', HB)
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
                    d.ellipse([CX + 30 - r, CY - 250 - r, CX + 30 + r, CY - 250 + r], outline=(255, 170 + q * 15, 60, int(50 + 140 * pw) - q * 20), width=6)
            layer(img, aura)
    if T_GUM + 0.3 <= t < LV[2]['t0'] + LV[2]['dur']:
        # mushroom SPEED: bright speed streaks rushing past behind Cyrus + dust kicked up at his feet
        def streaks(d):
            for q in range(8):
                yy = CY - 400 + q * 48; ph = (t * 4.5 + q * 0.37) % 1
                x1 = 600 - ph * 520; d.rectangle([max(72, x1 - 200), yy, max(72, x1), yy + 12], fill=(255, 225, 140, int(235 * (1 - ph * 0.7))))
            for q in range(4):
                ph = (t * 5 + q * 0.25) % 1; r = 16 + 30 * ph
                d.ellipse([CX - 60 - ph * 100 - r, CY - 14 - r * 0.6, CX - 60 - ph * 100 + r, CY - 14 + r * 0.6], fill=(235, 210, 170, int(190 * (1 - ph))))
        layer(img, streaks)
    img.alpha_composite(spr, (CX - spr.width // 2 + 40, CY - CFOOT))
    # energy gummy moment
    if T_GUM <= t < LV[2]['t0'] + LV[2]['dur']:
        u = (t - T_GUM) / 0.3
        if u < 1:
            gx = 700 + (CX + 30 - 700) * u; gy = 1180 + (CY - 250 - 1180) * u - 160 * math.sin(math.pi * u)
            img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        else:
            if u < 2.2: layer(img, lambda d: [d.ellipse([CX + 30 - r, CY - 250 - r, CX + 30 + r, CY - 250 + r], outline=(255, 200, 80, max(0, 255 - r // 2)), width=10) for r in range(int((u - 1) * 300), int((u - 1) * 300) + 90, 30)])
        if not any(e[1] == 'powerup_8bit' for e in ev): ev.append((round(T_GUM + 0.3, 3), 'powerup_8bit'))
    # header + meter window
    if li is not None:
        L = LV[li]
        if ph == 'run': v = int(L['off'] + L['sp'] * (t - L['t0'])) % 100
        elif ph == 'pre': v = int(L['off']) % 100
        else: v = L['stop']
        def win(d):
            d.rounded_rectangle([140, 555, W - 140, 1050], 28, fill=(16, 12, 30, 225), outline=(255, 214, 60, 255), width=8)
            d.rounded_rectangle([156, 571, W - 156, 1034], 22, outline=(120, 90, 30, 255), width=3)
        layer(img, win)
        text_layer(img, [(374, 586, L['label'], 44, (255, 214, 60), 6, 255), (772, 586, L['sub'], 44, (255, 255, 255), 6, 255)])
        jit = (random.Random(f).randint(-6, 6) if (li == 2 and ph == 'run') else 0)
        col = (255, 255, 255) if ph == 'run' else (255, 120, 90)
        if ph == 'pre': text_layer(img, [(W / 2, 720, 'SPEED!', 120, (255, 170, 50), 12, 255)])
        else: text_layer(img, [(W / 2 + jit, 660, f'{v:02d}', F_BIG, col, 12, 255)])
        if L['bar']:
            def bar(d, v=v):
                x0, x1, y = 220, W - 220, 1000
                d.rounded_rectangle([x0, y - 22, x1, y + 22], 12, fill=(40, 30, 60, 255), outline=(255, 255, 255, 255), width=4)
                xx = x0 + 8 + (x1 - x0 - 16) * v / 99
                d.rounded_rectangle([x0 + 8, y - 14, xx, y + 14], 8, fill=(255, 150 + int(100 * v / 99), 40, 255))
                d.polygon([(x1 - 8, y - 46), (x1 - 26, y - 70), (x1 + 10, y - 70)], fill=(255, 80, 80, 255))
            layer(img, bar); text_layer(img, [(W - 228, 876, '99', 44, (255, 120, 120), 6, 255)])
        if ph == 'hit':
            u = t - (L['t0'] + L['dur'])
            if u > 0.2:
                a = int(255 * min(1, (1.2 - u) / 0.3)) if u > 0.9 else 255
                layer(img, lambda d: d.rounded_rectangle([380, DY - 425, 860, DY - 230], 20, fill=(150, 18, 18, int(a * 0.93)), outline=(255, 255, 255, a), width=6))
                text_layer(img, [(620, DY - 408, str(v), 110, (255, 230, 120), 11, a), (620, DY - 288, L['verdict'] + '!', 48, (255, 255, 255), 7, a)])
    elif t >= LV[2]['t0'] + LV[2]['dur'] + 1.2:
        u = t - (LV[2]['t0'] + LV[2]['dur'] + 1.2)
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 6, 20, 150)))
        layer(img, lambda d: d.rounded_rectangle([120, 600, W - 120, 900], 28, fill=(16, 12, 30, 240), outline=(255, 214, 60, 255), width=8))
        text_layer(img, [(W / 2, 650, 'DID YOU', 90, (255, 255, 255), 9, 255), (W / 2, 770, 'GET 99?', 90, (255, 214, 60), 9, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK)
    W_.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/b_{f:04d}.png')
W_.close()
json.dump({'events': [e[:2] for e in ev]}, open('d36_ev.json', 'w')); print('done', END)
