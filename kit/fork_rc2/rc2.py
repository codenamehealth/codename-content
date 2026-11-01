"""Shared helpers for the fork_rc2 review recuts (r008-r013)."""
import sys, os
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork_rc1'); sys.path.insert(0, SP + 'pixellab/safezone')
from hook2 import hook_layer2          # comment prompt as a real >=44px second line of the hook band
from PIL import Image, ImageDraw, ImageFont
import numpy as np
FONT = SP + 'npmfont/ps/package/files/PressStart2P.ttf'
_fc = {}
def FF(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def acv_gloss(g0):
    """gummy gloss on Syeda's apple-shaped ACV gummy (native pick_acv.png size) so it reads as a gummy, not a real apple"""
    g0 = g0.copy()
    gl = Image.new('RGBA', g0.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).arc([5, 7, 26, 29], 290, 350, fill=(255, 240, 230, 170), width=2)
    gl.putalpha(Image.fromarray(np.minimum(np.array(gl.getchannel('A')), np.array(g0.getchannel('A')))))
    g0.alpha_composite(gl); return g0
def gummy_src(kind):
    g0 = Image.open(SP + f'pixellab/gummies/pick_{kind}.png').convert('RGBA')
    return acv_gloss(g0) if kind == 'acv' else g0
def acv_tag(img, jx, jy_top, a=255, ring=(90, 200, 80), xmax=1015):
    """'ACV GUMMY' 44px tag on a dark plate with a pointer down to (jx, jy_top)"""
    L2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2); tag = 'ACV GUMMY'; f = FF(44); tw = d2.textlength(tag, font=f)
    y0 = jy_top - 112; x0 = max(80, min(xmax - tw - 36, jx - tw / 2 - 18))
    d2.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, int(235 * a / 255)), outline=ring + (a,), width=5)
    d2.polygon([(jx - 14, y0 + 70), (jx + 14, y0 + 70), (jx, y0 + 98)], fill=ring + (a,))
    d2.text((x0 + 18, y0 + 14), tag, font=f, fill=(255, 255, 255, a), stroke_width=5, stroke_fill=(10, 6, 18, a))
    img.alpha_composite(L2)
