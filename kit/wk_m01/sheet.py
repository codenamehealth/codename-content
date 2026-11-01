import sys
from PIL import Image, ImageDraw
d, out, n0, n1, step = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
box = tuple(int(v) for v in sys.argv[6].split(',')) if len(sys.argv) > 6 else (40, 380, 1040, 1540)
sc = float(sys.argv[7]) if len(sys.argv) > 7 else 0.36; cols = int(sys.argv[8]) if len(sys.argv) > 8 else 6
fps = float(sys.argv[9]) if len(sys.argv) > 9 else 10
ns = list(range(n0, n1 + 1, step))
ims = [Image.open(d % n).crop(box) for n in ns]
w, h = ims[0].size; w2, h2 = int(w * sc), int(h * sc)
o = Image.new('RGB', (w2 * cols, h2 * ((len(ims) + cols - 1) // cols)), (0, 0, 0))
for i, (n, im) in enumerate(zip(ns, ims)):
    o.paste(im.resize((w2, h2)), ((i % cols) * w2, (i // cols) * h2)); ImageDraw.Draw(o).text(((i % cols) * w2 + 4, (i // cols) * h2 + 4), '%.2f' % ((n - 1) / fps), fill=(255, 0, 0))
o.save(out)
