p='r15.py'; s=open(p).read()
rep=[
# stunned sprite
("""        elif t < T_START:
            spr = STAND[n]""","""        elif t < T_START:
            spr = STAND[n]
        elif s['stun']:
            spr = PANIC[n][int(t * 14) % 8]   # dazed after a shove
            if s['st0'] not in [e2[2] for e2 in stun_seen if e2[0] == n]: stun_seen.append((n, t, s['st0']))"""),
("events = []; caught_seen = set(); slides_seen = set(); ghosts = {n: [] for n in NAMES}",
 "events = []; caught_seen = set(); slides_seen = set(); ghosts = {n: [] for n in NAMES}; stun_seen = []\nfor (t_s, a_s, b_s, _x, _y) in SHV: events.append((round(t_s, 3), 'punch'))\ndef star(dd, x, y, r, col):\n    pts = []\n    for k in range(10):\n        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45\n        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))\n    dd.polygon(pts, fill=col, outline=(60, 40, 10, 255))"),
# boost visuals: orange afterimages + speed lines + dust
("tint = Image.new('RGBA', gimg.size, (255, 220, 90, 255)); tint.putalpha(al)","tint = Image.new('RGBA', gimg.size, (255, 160, 40, 255)); tint.putalpha(al)"),
("""        if not s['caught']: bd2.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 80))
        bd2 = flush(b); b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))""",
"""        if not s['caught']: bd2.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 80))
        if boosted and not s['caught']:
            vv = math.hypot(s['vx'], s['vy']) or 1; ux_, uy_ = s['vx'] / vv, s['vy'] / vv
            for q in range(5):   # speed lines trailing behind
                ph_ = (t * 7 + q * 0.37) % 1; off_ = 30 + 70 * ph_; lat_ = (q - 2) * 16
                x0_ = x - ux_ * off_ - uy_ * lat_; y0_ = y - 60 - uy_ * off_ + ux_ * lat_
                bd2.line([x0_, y0_, x0_ - ux_ * 46, y0_ - uy_ * 46], fill=(255, 245, 220, int(230 * (1 - ph_))), width=5)
            for q in range(3):   # dust kicked up at the feet
                ph_ = (t * 5 + q / 3) % 1; dx_ = x - ux_ * (20 + 50 * ph_); dy_ = y - uy_ * (20 + 50 * ph_) - 6
                r_ = 8 + 14 * ph_; bd2.ellipse([dx_ - r_, dy_ - r_ * 0.7, dx_ + r_, dy_ + r_ * 0.7], fill=(215, 195, 160, int(170 * (1 - ph_))))
        bd2 = flush(b); b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['stun'] and not s['caught']:
            for k in range(3):
                a = t * 7 + k * 2.09; star(bd2, x + 30 * math.cos(a), y - FOOT + 18 + 9 * math.sin(a), 11, (255, 220, 70, 255))"""),
("al = int(255 * min(1, (1.4 - u) / 0.4)); txt = 'GLOW UP!'","al = int(255 * min(1, (1.4 - u) / 0.4)); txt = 'SPEED!'"),
("bd2.text((x - tw / 2, ty_), txt, font=F16, fill=(255, 200, 70, al), stroke_width=5, stroke_fill=(40, 20, 10, al))",
 "bd2.text((x - tw / 2, ty_), txt, font=F16, fill=(255, 160, 40, al), stroke_width=5, stroke_fill=(40, 20, 10, al))"),
# shove impact burst + BUMP! pop, drawn after characters
("""    for k in range(26):
        fx_ = (k * 137.5""","""    for (t_s, a_s, b_s, sx_s, sy_s) in SHV:
        u = t - t_s
        if 0 <= u < 0.3:   # impact burst at the contact point
            for k in range(8):
                an = k * math.pi / 4; r0, r1 = 14 + 40 * u / 0.3, 30 + 70 * u / 0.3
                bd2.line([sx_s + r0 * math.cos(an), sy_s - 50 + r0 * math.sin(an), sx_s + r1 * math.cos(an), sy_s - 50 + r1 * math.sin(an)], fill=(255, 255, 230, int(255 * (1 - u / 0.3))), width=6)
        if 0 <= u < 0.9 and not st[b_s]['caught']:
            al = int(255 * min(1, (0.9 - u) / 0.3)); txt = 'BUMP!'; tw = bd2.textlength(txt, font=F16)
            bx_, by_ = st[b_s]['x'], st[b_s]['y'] - FOOT - 18 - u * 40
            bd2.text((bx_ - tw / 2, by_), txt, font=F16, fill=(255, 255, 255, al), stroke_width=5, stroke_fill=(40, 20, 10, al))
    for k in range(26):
        fx_ = (k * 137.5"""),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
