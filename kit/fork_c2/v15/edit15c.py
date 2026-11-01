p='r15.py'; s=open(p).read()
rep=[
("                bd2.text((x - tw / 2, ty_), txt, font=F16, fill=(255, 160, 40, al), stroke_width=5, stroke_fill=(40, 20, 10, al))",
 "                LABELS.append((s['boost'], x, ty_, txt, (255, 160, 40), al))"),
("""            al = int(255 * min(1, (0.9 - u) / 0.3)); txt = 'BUMP!'; tw = bd2.textlength(txt, font=F16)
            bx_, by_ = st[b_s]['x'], st[b_s]['y'] - FOOT - 18 - u * 40
            bd2.text((bx_ - tw / 2, by_), txt, font=F16, fill=(255, 255, 255, al), stroke_width=5, stroke_fill=(40, 20, 10, al))""",
"""            al = int(255 * min(1, (0.9 - u) / 0.3))
            LABELS.append((t_s, st[b_s]['x'], st[b_s]['y'] - FOOT - 18 - u * 40, 'BUMP!', (255, 255, 255), al))
    placed = []   # pop labels: newest keeps its spot, older ones stack above it so they never overlap
    for (t0_, lx, ly, txt, col, al) in sorted(LABELS, key=lambda e: -e[0]):
        tw = bd2.textlength(txt, font=F16); box = [lx - tw / 2 - 6, ly - 4, lx + tw / 2 + 6, ly + 36]
        moved = True
        while moved:
            moved = False
            for pb in placed:
                if box[0] < pb[2] and pb[0] < box[2] and box[1] < pb[3] and pb[1] < box[3]:
                    dy = box[3] - pb[1] + 2; box[1] -= dy; box[3] -= dy; moved = True
        placed.append(box)
        bd2.text((box[0] + 6, box[1] + 4), txt, font=F16, fill=col + (al,), stroke_width=5, stroke_fill=(40, 20, 10, al))"""),
("    fxL[0] = Image.new('RGBA', b.size, (0, 0, 0, 0)); bd2 = ImageDraw.Draw(fxL[0])\n","    fxL[0] = Image.new('RGBA', b.size, (0, 0, 0, 0)); bd2 = ImageDraw.Draw(fxL[0]); LABELS = []\n"),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
