p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a; s=s.replace(a,b)
rep("CX, CY = 500, 930", "CX, CY = 460, 930")
rep("if not (140 <= HX <= 850): return None", "if not (140 <= HX <= 870): return None")
rep("if not (1440 <= HY <= 1510): return None", "if not (1430 <= HY <= 1525): return None")
rep("if not (0.25 <= (j - popped) / FPS <= 1.3): return None", "if not (0.15 <= (j - popped) / FPS <= 1.3): return None")
open(p,'w').write(s)
