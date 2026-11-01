p='r58.py'; s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n, (a[:60], s.count(a)); s=s.replace(a,b)
# physical marble radius = drawn radius (was 39 physical vs 45 drawn -> marbles overlapped each other and solids by 6px)
rep("MR = 39; WH = 6000 - CUT + DY; T_GO = 0.0", "MR = 45; WH = 6000 - CUT + DY; T_GO = 0.0   # review2: physics radius = drawn radius")
# side walls: physical inner edge = drawn inner edge
rep("seg((44, -DY), (44, WH + 300), 26); seg((1036, -DY), (1036, WH + 300), 26);", "seg((44, -DY), (44, WH + 300), 16, 'wall'); seg((1036, -DY), (1036, WH + 300), 16, 'wall');")
# finish chute + jar position
rep("FIN_Y = 5740 - C + DY", """FIN_Y = 5700 - C + DY + 10      # review2: finish = entering the single-file chute under the last funnel
JT = FIN_Y + 75                  # jar top (world y); marbles drop behind the jar and are removed once fully hidden
SEGS.append(((CX - 63, FIN_Y - 10), (CX - 63, JT + 20), 8, 'chute')); SEGS.append(((CX + 63, FIN_Y - 10), (CX + 63, JT + 20), 8, 'chute'))""")
# sim: segment physical radius matches the drawn stone (drawn 2r+10 wide), diamond pegs, slime hull, wheels
rep("""        s = pymunk.Segment(sp.static_body, a, b, r); s.friction = 0.5; s.elasticity = 0.45; sp.add(s)""",
"""        s = pymunk.Segment(sp.static_body, a, b, r if kind == 'wall' else r + 5); s.friction = 0.5; s.elasticity = 0.45; sp.add(s)""")
rep("""        c = pymunk.Circle(sp.static_body, r, (x, y)); c.elasticity = 0.7; c.friction = 0.3; sp.add(c)""",
"""        c = pymunk.Poly(sp.static_body, [(x, y - r - 8), (x + r, y), (x, y + r + 8), (x - r, y)]); c.elasticity = 0.7; c.friction = 0.3; sp.add(c)   # same diamond as drawn""")
rep("""        c = pymunk.Circle(sp.static_body, r, (x, y)); c.elasticity = 1.35; c.friction = 0.2; c.collision_type = 3; sp.add(c)""",
"""        c = pymunk.Poly(sp.static_body, [(x + px, y + py) for px, py in SLIME_HULL]); c.elasticity = 0.9; c.friction = 0.2; c.collision_type = 3; sp.add(c)   # slime body as drawn (2x), springy but no energy gain""")
rep("""            a = k * math.pi / 3; s = pymunk.Segment(b, (0, 0), (R * math.cos(a), R * math.sin(a)), 9); s.friction = 0.6; s.elasticity = 0.3; sp.add(s)
        hub = pymunk.Circle(b, 26); sp.add(hub); wheels.append(b)""","""            a = k * math.pi / 3; s = pymunk.Segment(b, (0, 0), (R * math.cos(a), R * math.sin(a)), 11); s.friction = 0.6; s.elasticity = 0.3; sp.add(s)
        hub = pymunk.Circle(b, 28); sp.add(hub); wheels.append(b)   # spoke/hub thickness = drawn thickness""")
rep("""            if v.length > 1500: b.velocity = v * (1500 / v.length); KLOG.append(('cap', round(t,2), n, round(v.length)))""",
"""            if v.length > 1500: KLOG.append(('cap', round(t,2), n, round(v.length)))   # review2: no velocity clamp, logged only (search rejects)""")
rep("""                if still[n] > 30: KLOG.append(('kick', round(t,2), n)); b.apply_impulse_at_local_point((rnd.choice([-1, 1]) * rnd.uniform(180, 300), -260)); still[n] = 0""",
"""                if still[n] > 30: KLOG.append(('kick', round(t,2), n)); still[n] = 0   # review2: no scripted kick, logged only (search rejects)""")
rep("""            if b.position.y > FIN_Y:
                fin[n] = t""","""            if b.position.y > FIN_Y:
                fin[n] = t
        for n, b in balls.items():
            if b.position.y > JT + 95 and b.space is not None: sp.remove(b, *b.shapes)   # fully behind the jar: it's in""")
rep("""def score(seed):
    fr, fin, ld, bo = sim(seed, record=False)""","""def score(seed):
    del KLOG[:]
    fr, fin, ld, bo = sim(seed, record=False)
    if KLOG: return None""")
rep("""    if fin[order[1]] - tw > 0.4 or len(ld) < 6: return None""","""    if fin[order[1]] - tw > 0.4 or fin[order[1]] - tw < 0.12 or len(ld) < 6: return None
    if fin[order[2]] - tw > 3.0: return None""")
# slime hull computed before the sim
rep("KLOG = []\n", """KLOG = []
import numpy as _np
_sl = Image.open(sorted(glob.glob(PL + 'race/slime_idle_c/*.png'))[1]).convert('RGBA'); _sl = _sl.resize((_sl.width * 2, _sl.height * 2), Image.NEAREST)
_a = _np.array(_sl)[:, :, 3] > 0; SLIME_HULL = []
for _y in range(_a.shape[0]):
    _xs = _np.where(_a[_y])[0]
    if len(_xs): SLIME_HULL += [(_xs[0] - _sl.width / 2, _y - _sl.height / 2 - 24), (_xs[-1] + 1 - _sl.width / 2, _y - _sl.height / 2 - 24)]
""")
# art: 2x slimes drawn on the hull, smaller/transparent splats, jar 400 wide drawn over the marbles, no wheel rim, chute stone
rep("JAR = JAR.resize((300, int(JAR.height * 300 / JAR.width)), Image.NEAREST) if JAR.width > 0 else JAR", "JAR = JAR.resize((400, int(JAR.height * 400 / JAR.width)), Image.NEAREST)   # review2: neck now wider than a marble")
rep("SLIME = seq(PL + 'race/slime_idle_c', 3)\nSPLAT = seq(PL + 'race/slime_splat_c', 3)", """SLIME = seq(PL + 'race/slime_idle_c', 2)
SPLAT = seq(PL + 'race/slime_splat_c', 2)
SPLAT = [Image.blend(Image.new('RGBA', s_.size, (0, 0, 0, 0)), s_, 0.65) for s_ in SPLAT]   # review2: smaller, see-through splats""")
rep("""            d.ellipse([wx - R, sy - R, wx + R, sy + R], outline=(90, 60, 30, 255), width=10)\n""", "")
rep("""            hit = any(0 <= t - bt < 0.25 and math.hypot(p[0] - x, p[1] - yy) < 90 for (bt, p) in BOUNCES if bt <= t)
            fr = SPLAT[min(len(SPLAT) - 1, 3)] if hit else SLIME[(int(t * 10) + i * 2) % len(SLIME)]
            img.alpha_composite(fr, (int(x - fr.width / 2), int(sy - fr.height + 70)))""","""            hit = any(0 <= t - bt < 0.2 and math.hypot(p[0] - x, p[1] - yy) < 100 for (bt, p) in BOUNCES if bt <= t)
            fr = SPLAT[min(len(SPLAT) - 1, 3)] if hit else SLIME[(int(t * 10) + i * 2) % len(SLIME)]
            img.alpha_composite(fr, (int(x - fr.width / 2), int(sy - fr.height / 2 - 24)))""")
rep("""    jy = FIN_Y - c0 - 40
    if -400 < jy < H + 100:
        layer(img, lambda dd: dd.ellipse([CX - 230, jy - 40, CX + 230, jy + 340], fill=(255, 210, 120, 50)))
        img.alpha_composite(JAR, (int(CX - JAR.width / 2), int(jy - 30)))""","""    jy = JT - c0
    if -800 < jy < H + 100:
        layer(img, lambda dd: dd.ellipse([CX - 280, jy - 40, CX + 280, jy + 420], fill=(255, 210, 120, 50)))""")
rep("""        if n in fin and t > fin[n] + 0.25: continue
        for k_ in range(1, 9):""","""        if pos[n][1] > JT + 95: continue
        for k_ in range(1, 9):""")
rep("""        x, yy, ang = pos[n]; sy = yy - c0
        if n in fin and t > fin[n] + 0.25: continue
        if -60 < sy < H + 60:
            b = BALL[n].rotate(-math.degrees(ang), resample=Image.NEAREST)
            img.alpha_composite(b, (int(x - b.width / 2), int(sy - b.height / 2)))""","""        x, yy, ang = pos[n]; sy = yy - c0
        if yy > JT + 95: continue
        if -60 < sy < H + 60:
            b = BALL[n].rotate(-math.degrees(ang), resample=Image.NEAREST)
            img.alpha_composite(b, (int(x - b.width / 2), int(sy - b.height / 2)))
    if -800 < jy < H + 100: img.alpha_composite(JAR, (int(CX - JAR.width / 2), int(jy)))   # drawn over the marbles: they drop into it""")
# standings: '?' until the order means something; no leader glow before 1s
rep("""        if rk == 0: layer(img,""","""        if rk == 0 and tout >= 1.0: layer(img,""")
rep("""        text_layer(img, [(x, P0 + 128, ['1ST', '2ND', '3RD', '4TH'][rk], 44, (255, 214, 60) if rk == 0 else (225, 225, 225), 7, 255)])""",
"""        text_layer(img, [(x, P0 + 128, ['1ST', '2ND', '3RD', '4TH'][rk] if tout >= 1.0 else '?', 44, (255, 214, 60) if (rk == 0 and tout >= 1.0) else (225, 225, 225), 7, 255)])   # review2: no ranks before ~1s""")
# PHOTO FINISH from the crossing frame, 0.8s
rep("""    if PHOTO and SM0o <= tout < min(T_CARD, SM1o + 0.8):
        u = tout - SM0o; pop""","""    if PHOTO and TWo <= tout < min(T_CARD, TWo + 0.8):
        u = tout - TWo; pop""")
rep("SM0o, SM1o = out_t(SM0), out_t(SM1)", "SM0o, SM1o = out_t(SM0), out_t(SM1); TWo = out_t(T_WIN)")
rep("if PHOTO: ev(SM0o, 'whoosh_8bit')", "if PHOTO: ev(TWo, 'whoosh_8bit')")
# camera locks at the first finish; podium hold 1.8s
rep("    if t < T3 + 0.3:\n", "    if t < T_WIN:   # review2: camera locks once the first marble finishes (no bob)\n")
rep("NHOLD = int(round(2.6 * FPS))", "NHOLD = int(round(1.8 * FPS))   # review2: podium hold 2.6 -> 1.8s")
open(p,'w').write(s)
