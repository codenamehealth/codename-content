p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a; s=s.replace(a,b)
rep("CX, CY = 500, 985", "CX, CY = 500, 930   # n10: ring up 55px so the Hollow can stand under any part of it and catch the gummy")
rep("""            if not (742 <= HX <= 850 or 140 <= HX <= 258): return None""","""            if not (140 <= HX <= 850): return None""")
rep("""            # approach from the side: the 5 frames before the catch stay clear of his head box
            for (px, py, _, _) in path[max(popped, j - 5):j]:
                if HX - 45 < px < HX + 55 and HY - 200 < py < HY - 118: return None
            if abs(vy) > 1.6 * abs(vx) + 80: return None
            if not (0.3 <= (j - popped) / FPS <= 1.2): return None""","""            if not (0.25 <= (j - popped) / FPS <= 1.3): return None""")
rep("TRYX = 249 if HX > 400 else 760", "TRYX = 249 if HX >= 470 else 740")
open(p,'w').write(s)
