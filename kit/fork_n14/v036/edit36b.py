p = 'r36.py'; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
rep("E_PLANT, E_WIND, E_DROP0, E_LAND, E_PUNCH, E_HIT, E_KB, E_FLY1, E_ASK = 0.0, 0.15, 0.2, 0.55, 0.85, 0.94, 1.06, 1.54, 2.05   # E_HIT fist meets the bubble, held to E_KB",
"""# review2 (Oct 29): gummy falls 0.45s with a glow and bounces once on the dummy's head before SHIELD!; fist-on-bubble held 0.22s with an
# impact flash; PAUSE THE VIDEO ON 99 fades out once the counter is gone; Cyrus lands 60px further right (head clears the 70px margin)
E_PLANT, E_WIND, E_DROP0, E_LAND, E_SHLD, E_PUNCH, E_HIT, E_KB, E_FLY1, E_ASK = 0.0, 0.15, 0.15, 0.6, 0.74, 0.98, 1.07, 1.29, 1.77, 2.28""")
a0 = s.index("    if t >= T_E0:\n        u = t - T_E0")
a1 = s.index("    # header + meter window")
new = '''    if t >= T_E0:
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
            X0, X1 = CX - 10, CX - 40                  # body centre: launch -> landing (review2: +60px so his head clears x=70)
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
        # the ACV gummy falls onto the dummy's head (gravity, white glow so it reads over the wall), one small bounce, then the shield
        HEADY = DY - DUMMY.height - ACV.height // 2 + 10
        if E_DROP0 <= u < E_SHLD:
            if u < E_LAND:
                p_ = (u - E_DROP0) / (E_LAND - E_DROP0); gy = 520 + (HEADY - 520) * p_ * p_
            else:
                qq = (u - E_LAND) / (E_SHLD - E_LAND); gy = HEADY - 38 * math.sin(math.pi * qq)
            for k_ in range(12):
                a_ = k_ * math.pi / 6; img.alpha_composite(GLOW, (int(DX - GLOW.width / 2 + 7 * math.cos(a_)), int(gy - GLOW.height / 2 + 7 * math.sin(a_))))
            img.alpha_composite(ACV, (DX - ACV.width // 2, int(gy - ACV.height / 2)))
            if u < E_LAND:
                def trail(d, gy=gy):
                    for k_ in range(4):
                        yy = gy - 70 - k_ * 46; d.rectangle([DX - 5 + (k_ % 2) * 14, yy - 5, DX + 5 + (k_ % 2) * 14, yy + 5], fill=(255, 255, 255, 200 - k_ * 45))
                layer(img, trail)
            if u >= E_LAND and not any(e[1] == 'jump' for e in ev): ev.append((round(T_E0 + E_LAND, 3), 'jump'))
        if u >= E_SHLD:
            g_ = min(1, (u - E_SHLD) / 0.15); pop = 0 if u < E_HIT else min(1, (u - E_HIT) / 0.22)
            fade = 1.0 if u < E_ASK - 0.25 else max(0, 1 - (u - E_ASK + 0.25) / 0.3)
            if fade > 0:
                cyb = (SH_TOP + DY + 22) / 2; hh = (DY + 22 - SH_TOP) / 2 * (0.3 + 0.7 * g_)
                w_ = SH_W * (0.3 + 0.7 * g_) * (1 + 0.06 * math.sin(pop * math.pi))
                flash = int(150 * max(0, 1 - pop)) if u >= E_HIT else 0
                def bubble(d, w_=w_, cyb=cyb, hh=hh, fade=fade, flash=flash):
                    d.ellipse([DX - w_, cyb - hh, DX + w_, cyb + hh], fill=(110 + flash // 2, 230, 90 + flash, int((55 + flash) * fade)), outline=(150, 255, 120, int(230 * fade)), width=8)
                    d.arc([DX - w_ * 0.78, cyb - hh + 18, DX - w_ * 0.12, cyb - hh + 150], 200, 260, fill=(230, 255, 220, int(230 * fade)), width=7)
                layer(img, bubble)
            if u < E_SHLD + 0.3: burst(img, DX, HEADY, (u - E_SHLD) / 0.3, (150, 255, 120), n=12, r0=30, r1=160)
            if not any(e[1] == 'twinkle' for e in ev): ev.append((round(T_E0 + E_SHLD, 3), 'twinkle'))
        if E_HIT <= u < E_KB + 0.06:      # impact flash where the fist meets the bubble, held while the punch freezes on contact
            qf = (u - E_HIT) / (E_KB + 0.06 - E_HIT); ix, iy = DX - SH_W + 6, 1226
            def impact(d, qf=qf):
                r = 50 + 70 * qf; a_ = int(255 * (1 - qf * 0.8))
                d.ellipse([ix - r, iy - r, ix + r, iy + r], fill=(255, 255, 255, int(a_ * 0.55)))
                for k_ in range(8):
                    an = k_ * math.pi / 4 + 0.2; r0, r1 = r * 0.6, r * 1.5 + 40
                    d.line([(ix + r0 * math.cos(an), iy + r0 * math.sin(an)), (ix + r1 * math.cos(an), iy + r1 * math.sin(an))], fill=(255, 255, 230, a_), width=10)
            layer(img, impact)
        if u >= E_HIT:
            if not any(e[1] == 'boing' for e in ev): ev.append((round(T_E0 + E_HIT, 3), 'boing')); ev.append((round(T_E0 + E_HIT, 3), 'punch'))
        # stamps (one at a time, same unboxed style as the verdicts, above the dummy inside the safe zone)
        if E_SHLD <= u < E_HIT:
            qs = u - E_SHLD; sc = 1 + 0.3 * max(0, 1 - qs / 0.12)
            text_layer(img, [(DX - 40, 860, 'SHIELD!', int(72 * sc), (110, 230, 90), 10, 255)])
        elif E_HIT <= u < E_ASK:
            qs = u - E_HIT; sc = 1 + 0.3 * max(0, 1 - qs / 0.12); a_ = 255 if u < E_ASK - 0.2 else int(255 * (E_ASK - u) / 0.2)
            text_layer(img, [(DX - 80, 860, 'BLOCKED!', int(72 * sc), (150, 255, 120), 10, a_)])
'''
s = s[:a0] + new + s[a1:]
rep("ACV = gummy('acv', 5)", """ACV = gummy('acv', 5)
GLOW = ACV.copy(); GLOW.putalpha(ACV.getchannel('A').point(lambda p_: 230 if p_ > 0 else 0)); GLOW = Image.composite(Image.new('RGBA', ACV.size, (255, 255, 255, 230)), Image.new('RGBA', ACV.size, (0, 0, 0, 0)), GLOW.getchannel('A'))""")
# header fade: hook fades out over 0.3s once the counter is gone, the question comes in at E_ASK as before
rep("""    img.alpha_composite(HOOK_END if (li is None and t >= T_E0 + E_ASK) else HOOK)""",
"""    if li is None and t >= T_E0 + E_ASK: img.alpha_composite(HOOK_END)
    elif t >= T_E0:
        ha = max(0.0, 1 - (t - T_E0) / 0.3)
        if ha > 0: hk = HOOK.copy(); hk.putalpha(HOOK.getchannel('A').point(lambda p_, ha=ha: int(p_ * ha))); img.alpha_composite(hk)
    else: img.alpha_composite(HOOK)""")
open(p, 'w').write(s); print('ok')
