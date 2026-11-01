p='r58.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("T_GO = 0.0   # review2: physics radius = drawn radius", "T_GO = 0.3   # review3: marbles rest on a visible gate until GO!")
rep("WHEELS = [(X(360), 2980 + DY, 130, 1.7), (X(720), 3380 + DY, 130, -1.9)]",
    "WHEELS = [(360, 2980 + DY, 130, 1.7), (590, 3380 + DY, 130, -1.9)]   # review3: >=110px between spoke tips and the walls (Joy was pinned against the wall by the spoke tips)")
rep("b.position = (x + rnd.uniform(-15, 15), 170 + DY)", "b.position = (x + rnd.uniform(-15, 15), 230 + DY - 8 - MR - 2)   # resting on the gate")
rep("WORLD = Image.new('RGBA', (W, WH + 400), (0, 0, 0, 255))", "WORLD = Image.new('RGBA', (W, WH + 500), (0, 0, 0, 255))   # review3: room to frame the finish higher")
rep("JAR = up(crop(Image.open(A + 'jar_mushroom.png').convert('RGBA')), 1)", "JAR = crop(Image.open(A + 'jar_mushroom.png').convert('RGBA')); JAR = JAR.crop((0, 50, JAR.width, JAR.height))   # review3: bottle opened (cork rows cut) so marbles visibly drop into the mouth")
rep("BALL = {n: face(n, MR + 6) for n in NAMES}", "BALL = {n: face(n, MR) for n in NAMES}   # review3: drawn radius = physics radius (was +6: looked like overlaps)")
rep("        tgt = max(0, min(WORLD.height - H, focus - 1290))", "        tgt = max(0, min(WORLD.height - H, focus - 1290, FIN_Y - 1150))   # review3: finish framed at y~1150")
rep("        dl.ellipse([x - 68, sy - 68, x + 68, sy + 68], fill=RING[n] + (70,))", "        dl.ellipse([x - MR - 8, sy - MR - 8, x + MR + 8, sy + MR + 8], fill=RING[n] + (55,))")
# mouth of the opened bottle drawn behind the marbles
rep("        layer(img, lambda dd: dd.ellipse([CX - 280, jy - 40, CX + 280, jy + 420], fill=(255, 210, 120, 50)))",
    "        layer(img, lambda dd: dd.ellipse([CX - 280, jy - 40, CX + 280, jy + 420], fill=(255, 210, 120, 50)))\n        layer(img, lambda dd: dd.ellipse([CX - 70, jy + 4, CX + 70, jy + 40], fill=(16, 8, 6, 255)))   # dark mouth of the open bottle")
# gate drawn until GO, then the two halves swing down
rep("    # standings panel (1.4x): leader slot glows", """    gy_ = 230 + DY - c0
    if tout < T_GO + 0.2:
        uu = max(0.0, tout - T_GO) / 0.2; ang_ = (math.pi / 2) * uu * uu
        for side, hx in ((1, XL + 16), (-1, XR - 16)):
            L_ = (XR - XL - 32) / 2; ex_, ey_ = hx + side * L_ * math.cos(ang_), gy_ + L_ * math.sin(ang_)
            layer(img, lambda dd, hx=hx, ex_=ex_, ey_=ey_: (dd.line([hx, gy_, ex_, ey_], fill=(60, 40, 24, 255), width=20), dd.line([hx, gy_, ex_, ey_], fill=(150, 104, 56, 255), width=12)))
    # standings panel (1.4x): leader slot glows""")
rep("""    if 0.15 <= tout < 0.9:
        u = tout - 0.15; sz = 150 if u > 0.1 else int(90 + 600 * u)
        text_layer(img, [(CX, 1000, 'GO!', sz, (120, 255, 120), 12, int(255 * min(1, (0.75 - u) / 0.2)))])""",
"""    if T_GO <= tout < T_GO + 0.5:
        u = tout - T_GO; sz = 150 if u > 0.1 else int(90 + 600 * u)
        text_layer(img, [(CX, 1250, 'GO!', sz, (120, 255, 120), 12, int(255 * min(1, (0.5 - u) / 0.15)))])   # review3: below the marbles, gone by 0.5s""")
rep("ev(0.2, 'go_8bit')", "ev(T_GO, 'go_8bit')")
rep("PHOTO = T2 - T_WIN < 0.5", "PHOTO = T2 - T_WIN < 0.2   # review3: only a real photo finish gets the slow-mo and stamp")
# clear win stamp when not a photo finish
rep("""    if tout >= T_CARD:
        img = podium_scene(tout - T_CARD, f)""", """    if not PHOTO and TWo <= tout < min(T_CARD, TWo + 0.8):
        u = tout - TWo; pop = 1.0 if u > 0.1 else 0.7 + 3 * u
        text_layer(img, [(CX, 760, '1ST!', int(96 * pop), (255, 214, 60), 10, int(255 * min(1, (0.8 - u) / 0.15)))])
    if tout >= T_CARD:
        img = podium_scene(tout - T_CARD, f)""")
# podium: drop-in with gravity and land
rep("""        x, top = PSLOT[rk]; fr = PVIC[rk][int(uu * 8) % len(PVIC[rk])]
        if uu < 0.18:""", """        x, top = PSLOT[rk]; fr = PVIC[rk][int(uu * 8) % len(PVIC[rk])]
        DROP = 220.0; tf = math.sqrt(2 * DROP / 3000.0)   # review3: each guide drops onto the block (gravity) and lands
        dy_ = -DROP + 0.5 * 3000.0 * min(uu, tf) ** 2
        if uu < tf:
            img.alpha_composite(fr, (x - fr.width // 2, int(top - fr.height + dy_))); continue
        uu = uu - tf
        if uu < 0.18:""")
open(p,'w').write(s)
