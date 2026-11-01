p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("if not (0.15 <= (j - popped) / FPS <= 1.3): return None", "if not (0.5 <= (j - popped) / FPS <= 1.0): return None   # review2: a visible ~0.6s arc on the real path")
rep("""                if popped is not None or not fail_ok(path, hits) or len(bounces) < 4: continue""",
"""                if popped is not None or not fail_ok(path, hits) or len(bounces) < 4: continue
                if min(math.hypot(q[2], q[3]) for q in path[-30:]) < 250: continue   # review2: still moving right up to the freeze (no 'stuck' look)""")
rep("if not (1.0 < tesc - t < 3.6): continue", "if not (0.6 < tesc - t < 3.8): continue")
rep("T_CARD = T_CATCH + 0.25; END = T_CARD + 1.6;", "T_CARD = T_CATCH + 1.0; END = T_CARD + 1.0;   # review2: catch + chew held 1s, end hold 1s\n")
rep("""            bb = BUB[k]; img.alpha_composite(bb, (int(round(px - bb.width / 2)), int(round(py - bb.height / 2))))
            n = max(1, math.ceil(t0 + TRY - t))
            text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])""","""            n = max(1, math.ceil(t0 + TRY - t))
            text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])   # review2: digit under the ball
            bb = BUB[k]; img.alpha_composite(bb, (int(round(px - bb.width / 2)), int(round(py - bb.height / 2))))""")
rep("ds.text((CX - tw / 2, CY - fnt.size / 2), txt,", "ds.text((540 - tw / 2, CY - fnt.size / 2), txt,")
rep("text_layer(img, [(CX, CY - 100, 'ESCAPED ON', int(76 * pop), (255, 214, 60), 10, int(255 * a)), (CX, CY - 4, f'TRY", "text_layer(img, [(540, CY - 100, 'ESCAPED ON', int(76 * pop), (255, 214, 60), 10, int(255 * a)), (540, CY - 4, f'TRY")
open(p,'w').write(s)
