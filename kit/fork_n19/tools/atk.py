# Shove/attack helper (Oct 29 shove rule): the existing PixelLab attack animations built from Syeda's sprites
# (pixellab/race/<g>_atk/00-12.png, 128x128, feet y=104, facing right; already used in the approved race reels).
# Timeline of one shove (ATK_DUR ~1.0s, the shover stands still the whole time):
#   0 .. PLANT          frame 00 (planted stance)
#   PLANT .. ATK_DUR    frames 01..12 at AFPS (wind-up, strike, follow-through, recover)
#   hit_t(g)            the strike frame: the victim is knocked back at this moment
from PIL import Image
P = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race/'
PLANT, AFPS = 0.12, 13.0
NFR = 13
ATK_DUR = PLANT + (NFR - 1) / AFPS          # 1.04s
HITF = {'joy': 3, 'ray': 3, 'cleo': 4, 'cyrus': 3}   # first frame where the strike connects (vine / bolt / blade / fist)
FOOT_Y = 104
def hit_t(g): return PLANT + (HITF[g] - 1) / AFPS
def frame_idx(u):
    if u < PLANT: return 0
    return min(NFR - 1, 1 + int((u - PLANT) * AFPS))
_cache = {}
def frames(g, k):
    key = (g, k)
    if key not in _cache:
        fr = [Image.open(P + f'{g}_atk/{i:02d}.png').convert('RGBA') for i in range(NFR)]
        bb = fr[0].getbbox(); cx = (bb[0] + bb[2]) / 2           # body centre in the planted frame
        R = [f.resize((int(f.width * k), int(f.height * k)), Image.NEAREST) for f in fr]
        L = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in R]
        _cache[key] = (R, L, cx * k, (fr[0].width - cx) * k)
    return _cache[key]
def sprite(g, k, u, left=False):
    """returns (image, dx, dy): paste at (body_x + dx, feet_y + dy)"""
    R, L, cxr, cxl = frames(g, k); i = frame_idx(u)
    im = (L if left else R)[i]
    return im, -int(round(cxl if left else cxr)), -int(round(FOOT_Y * k))
def draw(img, g, k, u, body_x, feet_y, left=False):
    im, dx, dy = sprite(g, k, u, left); img.alpha_composite(im, (int(body_x + dx), int(feet_y + dy)))
    return im
