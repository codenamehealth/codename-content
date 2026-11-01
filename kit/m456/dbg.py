import sys, os, importlib
from PIL import Image, ImageDraw
M = importlib.import_module(sys.argv[1]); seed = int(sys.argv[2]); ts = [float(x) for x in sys.argv[3].split(',')]
r = M.run(seed); Wd = M.Wd; FPS = 30
COL = {'joy': (100, 200, 70), 'cleo': (70, 135, 255), 'cyrus': (255, 145, 30), 'ray': (180, 95, 235)}
k = 0.36; w, h = int(1080 * k), int(1920 * k * 0.62); cols = 6
S = Image.new('RGB', (cols * w, ((len(ts) + cols - 1) // cols) * h), (0, 0, 0))
for i, t in enumerate(ts):
    fi = min(len(r['frames']) - 1, int(t * FPS)); st, tau, hp, gum = r['frames'][fi]
    im = Image.new('RGB', (1080, 1920), (30, 30, 30)); d = ImageDraw.Draw(im)
    for rr in range(Wd.rows):
        for cc in range(Wd.cols):
            x0, y0 = Wd.OX + cc * Wd.C, Wd.OY + rr * Wd.C
            b = Wd.brk[rr, cc]
            if b and hp[b - 1] > 0: col = (200, 200, 200) if Wd.B[b - 1]['owner'] is None else COL[Wd.B[b - 1]['owner']]
            elif Wd.wall[rr, cc]: col = (20, 90, 20)
            elif Wd.haz[rr, cc]: col = (255, 0, 0)
            else: col = (240, 230, 200)
            d.rectangle([x0, y0, x0 + Wd.C - 1, y0 + Wd.C - 1], fill=col)
    for (x0, y0, x1, y1, dd) in Wd.flood_rects(tau): d.rectangle([x0, y0, x1, y1], fill=(60, 20, 90))
    if gum: d.ellipse([gum[0] - 14, gum[1] - 14, gum[0] + 14, gum[1] + 14], fill=(255, 60, 60))
    for g, (x, y, vx, vy, out, won) in st.items():
        if out is not None: continue
        d.rectangle([x - M.HS, y - M.HS, x + M.HS, y + M.HS], fill=COL[g], outline=(0, 0, 0), width=3)
    d.text((40, 420), f't={t} tau={tau:.1f}', fill=(255, 255, 0))
    im = im.crop((0, 400, 1080, 400 + int(1920 * 0.62))).resize((w, h))
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(sys.argv[4]); print(sys.argv[4])
