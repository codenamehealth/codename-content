from PIL import Image
import math
def bite(im, cx, cy, r):
    im = im.copy(); px = im.load(); w, h = im.size
    outline = (40, 12, 8, 255)
    # darkest opaque colour in sprite = its outline
    cols = [px[x, y] for y in range(h) for x in range(w) if px[x, y][3] > 200]
    outline = min(cols, key=lambda p: sum(p[:3]))
    inside = lambda x, y: (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 < r * r
    cut = [(x, y) for y in range(h) for x in range(w) if inside(x, y)]
    for x, y in cut: px[x, y] = (0, 0, 0, 0)
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 200 and not inside(x, y) and any(0 <= x + dx < w and 0 <= y + dy < h and inside(x + dx, y + dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                px[x, y] = outline
    return im
