import sys
from PIL import Image, ImageDraw
# strip.py out.png x0 y0 x1 y1 cols file...  : full-res crops tiled, frame name label
out, x0, y0, x1, y1, cols = sys.argv[1], *map(int, sys.argv[2:7]); fs = sys.argv[7:]
w, h = x1 - x0, y1 - y0; rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').crop((x0, y0, x1, y1)); d = ImageDraw.Draw(im); d.text((6, 6), f.split('/')[-1], fill=(255, 255, 0))
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out)
