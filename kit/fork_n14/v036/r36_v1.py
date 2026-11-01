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
T_GUM = 8.0   # counter runs from frame 0; gummy beat 0.6s with the HUD up
# n14 (Bennett-approved break, Oct 29): after level 3's MISSED IT! (all three pause windows are over), Cyrus plants and winds up one last
# punch, an ACV gummy drops onto the dummy, SHIELD! (green bubble), the punch hits the bubble, BLOCKED!, and Cyrus bounces back onto his
# back (existing king/cyrus_ko frames); then the hook turns into DID YOU GET 99? as before. Everything before T_E0 is unchanged.
T_E0 = 8.6 + 1.3 + 1.2                     # = old end-card start (LV3 end + 1.2)
E_PLANT, E_WIND, E_DROP0, E_LAND, E_PUNCH, E_HIT, E_KB, E_FLY1, E_ASK = 0.0, 0.15, 0.2, 0.55, 0.85, 0.94, 1.06, 1.54, 2.05   # E_HIT fist meets the bubble, held to E_KB
END = T_E0 + E_ASK + float(os.environ.get('ASK', '1.3'))
KO = [up(Image.open(p_).convert('RGBA'), K) for p_ in sorted(glob.glob(PL + 'king/cyrus_ko/*.png'))]
KOBB = [Image.open(p_).getbbox() for p_ in sorted(glob.glob(PL + 'king/cyrus_ko/*.png'))]
ACV = gummy('acv', 5)
SH_W, SH_TOP = 146, DY - DUMMY.height - 34      # bubble half-width (keeps x <= 886) and top
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
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
# Oct 29 soft-fade pass: no box, 'Comment your number' cut (caption asks); end question replaces the hook text (no plate)
HOOK, HB = hook_fade(['Pause the video', 'on 99'], accent=1); HOOK_END, _ = hook_fade(['Did you', 'get 99?'], accent=1); print('hook bottom', HB)
UY = -64   # HUD moved up into the space the smaller hook frees
W_ = Writer('d36_noaudio.mp4'); ev = []
PV = [int(x) for x in os.environ.get('PV', '').split(',') if x]
F_BIG = 230
sys.path.insert(0, SP + 'fork_c7'); from powers import burst, dizzy
STILLS = [int(x) for x in os.environ.get('STILLS', '').split(',') if x]
if STILLS: W_.close(); W_ = None
for f in range(int(round(END * FPS))):
    if STILLS and f not in STILLS:
        if f > max(STILLS): break
        continue
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
    if t < T_E0: img.alpha_composite(spr, (CX - spr.width // 2 + 40, CY - CFOOT))
    # energy gummy moment
    if T_GUM <= t < LV[2]['t0'] + LV[2]['dur']:
        u = (t - T_GUM) / 0.3
        if u < 1:
            gx = 700 + (CX + 30 - 700) * u; gy = 1180 + (CY - 250 - 1180) * u - 160 * math.sin(math.pi * u)
            img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        else:
            if u < 2.2: layer(img, lambda d: [d.ellipse([CX + 30 - r, CY - 250 - r, CX + 30 + r, CY - 250 + r], outline=(255, 200, 80, max(0, 255 - r // 2)), width=10) for r in range(int((u - 1) * 300), int((u - 1) * 300) + 90, 30)])
        if not any(e[1] == 'powerup_8bit' for e in ev): ev.append((round(T_GUM + 0.3, 3), 'powerup_8bit'))
    if t >= T_E0:
        u = t - T_E0
        ATKX = CX - ATK[0].width // 2 + 40          # ATK sprite left (unchanged placement)
        if u < E_KB:
            if u < E_WIND: spr2 = ATK[0]
            elif u < E_PUNCH: spr2 = ATK[1]          # planted, fist cocked back
            else: spr2 = ATK[min(4, 2 + int((u - E_PUNCH) * 22))]
            if E_WIND <= u < E_PUNCH:                 # wind-up charge (same aura as the levels)
                pw = min(1, (u - E_WIND) / (E_PUNCH - E_WIND))
                def aura2(d, pw=pw):
                    for q in range(5):
                        r = 120 + q * 26 + 14 * math.sin(t * 20 + q)
                        d.ellipse([CX + 30 - r, CY - 250 - r, CX + 30 + r, CY - 250 + r], outline=(255, 170 + q * 15, 60, int(50 + 140 * pw) - q * 20), width=6)
                layer(img, aura2)
            spr_final = (spr2, ATKX, CY - CFOOT)
        else:
            # knocked back: KO frames 1-2 in the air on a ballistic arc (rises, drifts back), lands on his back (frame 3), one small bounce
            q = u - E_KB; fl = E_FLY1 - E_KB
            X0, X1 = CX - 70, CX - 100                 # body centre: lunge position -> landing (head stays in frame)
            if q < fl:
                k = 1 if q < fl * 0.45 else 2; p_ = q / fl
                xc = X0 + (X1 - X0) * p_; hgt = 4 * 150 * p_ * (1 - p_)
            else:
                k = 3; xc = X1; qq = q - fl; hgt = 30 * max(0, math.sin(math.pi * qq / 0.22)) if qq < 0.22 else 0
            bb = KOBB[k]; spr2 = KO[k]
            spr_final = (spr2, int(xc - (bb[0] + bb[2]) / 2 * K), int(CY - bb[3] * K - hgt))
            if q >= fl:
                qq = q - fl
                if qq < 0.3: burst(img, int(X1), CY - 10, qq / 0.3, (235, 210, 170), n=10, r0=40, r1=170)
                if qq > 0.2: dizzy(img, int(X1 - 110), CY - (bb[3] - bb[1]) * K - 30, t)
                if not any(e[1] == 'stomp_8bit' for e in ev): ev.append((round(t, 3), 'stomp_8bit'))
        img.alpha_composite(spr_final[0], (spr_final[1], spr_final[2]))
        # the ACV gummy drops onto the dummy's head (gravity), then the shield bubble
        if E_DROP0 <= u < E_LAND:
            p_ = (u - E_DROP0) / (E_LAND - E_DROP0); gy = 560 + (SH_TOP + 40 - 560) * p_ * p_
            img.alpha_composite(ACV, (DX - ACV.width // 2, int(gy - ACV.height / 2)))
        if u >= E_LAND:
            g_ = min(1, (u - E_LAND) / 0.15); pop = 0 if u < E_HIT else min(1, (u - E_HIT) / 0.12)
            fade = 1.0 if u < E_ASK - 0.25 else max(0, 1 - (u - E_ASK + 0.25) / 0.3)
            if fade > 0:
                w_ = SH_W * (0.3 + 0.7 * g_) * (1 + 0.06 * math.sin(pop * math.pi)); top_ = DY - (DY - SH_TOP) * (0.3 + 0.7 * g_)
                flash = int(150 * max(0, 1 - pop)) if u >= E_HIT else 0
                def bubble(d, w_=w_, top_=top_, fade=fade, flash=flash):
                    d.ellipse([DX - w_, top_, DX + w_, DY + 22], fill=(110 + flash // 2, 230, 90 + flash, int((55 + flash) * fade)), outline=(150, 255, 120, int(230 * fade)), width=8)
                    d.arc([DX - w_ * 0.78, top_ + 18, DX - w_ * 0.12, top_ + 150], 200, 260, fill=(230, 255, 220, int(230 * fade)), width=7)
                layer(img, bubble)
            if u < E_LAND + 0.3: burst(img, DX, SH_TOP + 40, (u - E_LAND) / 0.3, (150, 255, 120), n=12, r0=30, r1=160)
            if not any(e[1] == 'twinkle' for e in ev): ev.append((round(T_E0 + E_LAND, 3), 'twinkle'))
        if u >= E_HIT:
            if not any(e[1] == 'boing' for e in ev): ev.append((round(T_E0 + E_HIT, 3), 'boing')); ev.append((round(T_E0 + E_HIT, 3), 'punch'))
        # stamps (one at a time, same unboxed style as the verdicts, above the dummy inside the safe zone)
        if E_LAND <= u < E_HIT:
            qs = u - E_LAND; sc = 1 + 0.3 * max(0, 1 - qs / 0.12)
            text_layer(img, [(DX - 40, 860, 'SHIELD!', int(72 * sc), (110, 230, 90), 10, 255)])
        elif E_HIT <= u < E_ASK:
            qs = u - E_HIT; sc = 1 + 0.3 * max(0, 1 - qs / 0.12); a_ = 255 if u < E_ASK - 0.2 else int(255 * (E_ASK - u) / 0.2)
            text_layer(img, [(DX - 80, 860, 'BLOCKED!', int(72 * sc), (150, 255, 120), 10, a_)])
    # header + meter window
    if li is not None:
        L = LV[li]
        if ph == 'run': v = int(L['off'] + L['sp'] * (t - L['t0'])) % 100
        elif ph == 'pre': v = int(L['off']) % 100
        else: v = L['stop']
        def win(d):
            d.rounded_rectangle([140, 555 + UY, W - 140, 1050 + UY], 28, fill=(16, 12, 30, 225), outline=(255, 214, 60, 255), width=8)
            d.rounded_rectangle([156, 571 + UY, W - 156, 1034 + UY], 22, outline=(120, 90, 30, 255), width=3)
        layer(img, win)
        text_layer(img, [(W / 2, 586 + UY, L['label'], 44, (255, 214, 60), 6, 255)])   # SLOW / FASTER / NO BAR cut (the speed and the missing bar show it)
        jit = (random.Random(f).randint(-6, 6) if (li == 2 and ph == 'run') else 0)
        col = (255, 255, 255) if ph == 'run' else (255, 120, 90)
        if ph == 'pre': text_layer(img, [(W / 2, 720 + UY, 'SPEED!', 120, (255, 170, 50), 12, 255)])
        else: text_layer(img, [(W / 2 + jit, 660 + UY, f'{v:02d}', F_BIG, col, 12, 255)])
        hitv = ph == 'hit' and t - (L['t0'] + L['dur']) > 0.2
        if L['bar'] and not hitv:
            def bar(d, v=v):
                x0, x1, y = 220, W - 220, 1000 + UY
                d.rounded_rectangle([x0, y - 22, x1, y + 22], 12, fill=(40, 30, 60, 255), outline=(255, 255, 255, 255), width=4)
                xx = x0 + 8 + (x1 - x0 - 16) * v / 99
                d.rounded_rectangle([x0 + 8, y - 14, xx, y + 14], 8, fill=(255, 150 + int(100 * v / 99), 40, 255))
                d.polygon([(x1 - 8, y - 46), (x1 - 26, y - 70), (x1 + 10, y - 70)], fill=(255, 80, 80, 255))
            layer(img, bar)   # '99' label at the marker cut (the hook says 99; the red marker shows the target)
        if ph == 'hit':
            u = t - (L['t0'] + L['dur'])
            if u > 0.2:
                a = int(255 * min(1, (1.2 - u) / 0.3)) if u > 0.9 else 255
                # verdict only, unboxed, in the bar's slot inside the HUD (the red frozen number already shows the stop; dummy stays clear)
                text_layer(img, [(W / 2, 1000 + UY - 30, L['verdict'] + '!', 64, (255, 230, 120), 9, a)])
    elif t >= T_E0 + E_ASK:
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK_END if (li is None and t >= T_E0 + E_ASK) else HOOK)
    if STILLS: img.convert('RGB').save(f'st_{f:04d}.png'); continue
    W_.write(img)
    if f in PV: img.convert('RGB').save(f'pv_{f}.png')
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/b_{f:04d}.png')
if W_: W_.close()
json.dump({'events': [e[:2] for e in ev]}, open('d36_ev.json', 'w')); print('done', END)
