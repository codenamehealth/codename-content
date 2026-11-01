p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("GEM = (4.7, -89.8)          # gem/hands point of hollow_eat frame 1 relative to (HX, HY) (feet)",
    "GEM = (4.7, -89.8)          # gem/hands point of hollow_eat frame 1 relative to (HX, HY) (feet)\nHAND = (52, -194)          # review3: gummy resting on the raised right hand of Syeda's hollow-victory pose, relative to (HX, HY)")
rep("""        if vy > 0 and y >= 1395:
            HX, HY = x - GEM[0], y - GEM[1]""", """        if vy > 0 and y >= 1236:
            HX, HY = x - HAND[0], y - HAND[1]""")
rep("""            return j, HX, HY
""", """            # it comes down onto the raised hand, never across his head or body
            for (px, py, _, _) in path[max(popped, j - 8):j]:
                if HX - 45 < px < HX + 48 and HY - 205 < py < HY: return None
            return j, HX, HY
""")
rep("""            near = [h[1] for h in hits if h[0] == 'cap' or (h[0] == 'wall' and h[2] < 0.10)]""",
"""            near = [h[1] for h in hits if h[0] == 'cap' or (h[0] == 'wall' and h[2] < 0.10)]
            caps = [h[1] for h in hits if h[0] == 'cap']
            if min(math.hypot(q[2], q[3]) for q in path[:15]) < 250: continue   # review3: no hang after the spawn""")
rep("""                if i == 2 and not any(1.0 < x - t < 3.0 for x in near): continue""",
"""                if i == 2 and not any(1.0 < x - t < 3.0 for x in caps): continue   # review3: SO CLOSE! = the ball bouncing off the gap edge""")
rep("NEAR_T = [x for x in SEQ[2][6] if 1.0 < x - SEQ[2][1] < 3.0][0]",
    "NEAR_T = [h[1] for h in SEQ[2][4] if h[0] == 'cap' and 1.0 < h[1] - SEQ[2][1] < 3.0][0]   # the frame it hits the gap edge")
rep("T_CARD = T_CATCH + 1.0; END = T_CARD + 1.0;", "T_CARD = T_CATCH + 1.0; END = T_CARD + 0.8;")
rep("""SLO0, SLO1, SLOW = T_ESC - 0.15, T_CATCH + 0.05, 0.4
TMAP = []; _st = 0.0
while _st < END - 1e-9:
    TMAP.append(_st); _st += (SLOW if SLO0 <= _st < SLO1 else 1.0) / FPS""","""# review3: slow motion eases in before the pop and out after the catch (no sudden 'stop' at the pop), 0.5x at its slowest
def _spd(x):
    def sm(e0, e1, v): v = max(0.0, min(1.0, (v - e0) / (e1 - e0))); return v * v * (3 - 2 * v)
    return 1.0 - 0.5 * sm(T_ESC - 0.45, T_ESC - 0.1, x) * (1 - sm(T_CATCH + 0.05, T_CATCH + 0.35, x))
TMAP = []; _st = 0.0
while _st < END - 1e-9:
    TMAP.append(_st); _st += _spd(_st) / FPS""")
# frozen look: icy crust + frost spikes, applied as the ball freezes
rep("""    if frozen:
        d.ellipse([4, 4, sz - 4, sz - 4], fill=(150, 170, 200, 235), outline=(230, 240, 255, 255), width=4)""",
"""    if frozen:   # review3: clearly frozen: icy blue crust with frost spikes around the rim
        d.ellipse([4, 4, sz - 4, sz - 4], fill=(170, 215, 245, 240), outline=(235, 250, 255, 255), width=5)
        for j in range(14):
            a = j * 2 * math.pi / 14 + 0.2; r0 = sz / 2 - 6; r1 = sz / 2 + (3 if j % 2 else -1)
            cx_, cy_ = sz / 2, sz / 2
            d.polygon([(cx_ + r0 * math.cos(a - 0.12), cy_ + r0 * math.sin(a - 0.12)), (cx_ + r1 * math.cos(a), cy_ + r1 * math.sin(a)), (cx_ + r0 * math.cos(a + 0.12), cy_ + r0 * math.sin(a + 0.12))], fill=(255, 255, 255, 235))""")
rep("        g = ImageEnhance.Color(GUM[k]).enhance(0.25); g = ImageEnhance.Brightness(g).enhance(0.75)",
    "        g = ImageEnhance.Color(GUM[k]).enhance(0.2); g = ImageEnhance.Brightness(g).enhance(0.8)\n        g = Image.blend(g, Image.new('RGBA', g.size, (150, 210, 255, 0)), 0.0)")
# Hollow: idle -> raises hands (victory) as the gummy comes -> holds it on his raised hand
rep("""    HOLD = None
    if t >= T_CATCH:
        ei = min(len(EAT) - 1, 1 + int((t - T_CATCH) * 12)); hf, gp = EAT[ei]
        if gp is not None: g = GUM['gold']; HOLD = (g, (int(round(HX - 138 + gp[0] - g.width / 2)), int(round(HY - 234 + gp[1] - g.height / 2))))
    else: hf = HID[int(t * 6) % len(HID)]""","""    HOLD = None
    if t >= T_CATCH - 0.35:   # review3: Syeda's hollow-victory pose: hands up to catch, then holds it up
        vi = int(max(0.0, t - (T_CATCH - 0.35)) * 8) % len(VICH); hf = VICH[vi]
        if t >= T_CATCH:
            g = GUM['gold']; hx_, hy_ = VHAND[vi]
            HOLD = (g, (int(round(HX - 138 + hx_ - g.width / 2)), int(round(HY - 234 + hy_ - g.height / 2 + 4))))
    else: hf = HID[int(t * 6) % len(HID)]""")
rep("EAT_RAW = seq(SPD + 'fork3/hollow_eat', 3, 0, 13); HID = idle('hollow', 3)", """EAT_RAW = seq(SPD + 'fork3/hollow_eat', 3, 0, 13); HID = idle('hollow', 3)
VICH = [up(f.resize((92, 92), Image.NEAREST), 3) for f in gif_frames(A + 'hollow-victory.gif')]
VHAND = []
for _f in VICH:   # top of the raised right hand in each frame; the gummy sits on it
    _a = np.array(_f)[:, :, 3] > 0; _R = _a[:, 180:]; _y = int(np.nonzero(_R.any(1))[0].min()); _x = 180 + float(np.nonzero(_R[_y])[0].mean())
    VHAND.append((_x, _y - 26))""")
# SO CLOSE above the ring centre and the digit hidden while a stamp shows
rep("""            n = max(1, math.ceil(t0 + TRY - t))
            text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])""","""            n = max(1, math.ceil(t0 + TRY - t))
            if not (0 <= t - NEAR_T < 0.6):   # review3: digit hidden while SO CLOSE! shows
                text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])""")
open(p,'w').write(s)
