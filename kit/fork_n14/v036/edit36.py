p = 'r36.py'; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
rep("T_GUM = 8.0; END = 12.4   # counter runs from frame 0; gummy beat 0.6s with the HUD up; end card 1.3s",
"""T_GUM = 8.0   # counter runs from frame 0; gummy beat 0.6s with the HUD up
# n14 (Bennett-approved break, Oct 29): after level 3's MISSED IT! (all three pause windows are over), Cyrus plants and winds up one last
# punch, an ACV gummy drops onto the dummy, SHIELD! (green bubble), the punch hits the bubble, BLOCKED!, and Cyrus bounces back onto his
# back (existing king/cyrus_ko frames); then the hook turns into DID YOU GET 99? as before. Everything before T_E0 is unchanged.
T_E0 = 8.6 + 1.3 + 1.2                     # = old end-card start (LV3 end + 1.2)
E_PLANT, E_WIND, E_DROP0, E_LAND, E_PUNCH, E_HIT, E_FLY1, E_ASK = 0.0, 0.15, 0.2, 0.55, 0.85, 0.94, 1.42, 1.95
END = T_E0 + E_ASK + float(os.environ.get('ASK', '1.3'))
KO = [up(Image.open(p_).convert('RGBA'), K) for p_ in sorted(glob.glob(PL + 'king/cyrus_ko/*.png'))]
KOBB = [Image.open(p_).getbbox() for p_ in sorted(glob.glob(PL + 'king/cyrus_ko/*.png'))]
ACV = gummy('acv', 5)
SH_W, SH_TOP = 146, DY - DUMMY.height - 34      # bubble half-width (keeps x <= 886) and top""")
# extra finale drawing, inserted before the HUD block
rep("""    # header + meter window
    if li is not None:""",
"""    if t >= T_E0:
        u = t - T_E0
        ATKX = CX - ATK[0].width // 2 + 40          # ATK sprite left (unchanged placement)
        if u < E_HIT:
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
            q = u - E_HIT; fl = E_FLY1 - E_HIT
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
    if li is not None:""")
# Cyrus draw: use the finale sprite after T_E0
rep("""    img.alpha_composite(spr, (CX - spr.width // 2 + 40, CY - CFOOT))""",
"""    if t >= T_E0: img.alpha_composite(spr_final[0], (spr_final[1], spr_final[2]))
    else: img.alpha_composite(spr, (CX - spr.width // 2 + 40, CY - CFOOT))""")
rep("""    elif t >= LV[2]['t0'] + LV[2]['dur'] + 1.2:
        u = t - (LV[2]['t0'] + LV[2]['dur'] + 1.2)
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK_END if (li is None and t >= LV[2]['t0'] + LV[2]['dur'] + 1.2) else HOOK)""",
"""    elif t >= T_E0 + E_ASK:
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK_END if (li is None and t >= T_E0 + E_ASK) else HOOK)""")
rep("""for f in range(int(END * FPS)):""", """sys.path.insert(0, SP + 'fork_c7'); from powers import burst, dizzy
STILLS = [int(x) for x in os.environ.get('STILLS', '').split(',') if x]
if STILLS: W_.close(); W_ = None
for f in range(int(round(END * FPS))):
    if STILLS and f not in STILLS:
        if f > max(STILLS): break
        continue""")
rep("""    W_.write(img)
    if f in PV:""", """    if STILLS: img.convert('RGB').save(f'st_{f:04d}.png'); continue
    W_.write(img)
    if f in PV:""")
rep("""W_.close()
json.dump""", """if W_: W_.close()
json.dump""")
open(p, 'w').write(s); print('ok')
