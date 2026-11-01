"""Shared helpers for fork_rc3 recuts."""
from PIL import Image, ImageDraw
import numpy as np
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
def acv_gummy_strong():
    """Syeda's ACV gummy (native 30x32) with a clearer gummy shine: bright curved highlight top-left, specular dot,
    and a soft light rim on the lower right (translucent-candy look). Art itself untouched."""
    g0 = Image.open(SP + 'pixellab/gummies/pick_acv.png').convert('RGBA'); A = np.array(g0.getchannel('A'))
    gl = Image.new('RGBA', g0.size, (0, 0, 0, 0)); d = ImageDraw.Draw(gl)
    d.arc([4, 8, 24, 30], 195, 265, fill=(255, 250, 240, 215), width=2)
    d.rectangle([7, 11, 8, 12], fill=(255, 255, 255, 255))
    d.arc([5, 7, 28, 31], 20, 75, fill=(255, 225, 215, 110), width=1)
    m = np.minimum(np.array(gl.getchannel('A')), A); gl.putalpha(Image.fromarray(m))
    out = g0.copy(); out.alpha_composite(gl); return out
if __name__ == '__main__':
    g = acv_gummy_strong(); b = Image.new('RGBA', (400, 200), (60, 90, 50, 255))
    b.alpha_composite(Image.open(SP + 'pixellab/gummies/pick_acv.png').convert('RGBA').resize((150, 160), Image.NEAREST), (20, 20))
    b.alpha_composite(g.resize((150, 160), Image.NEAREST), (220, 20)); b.convert('RGB').save('gloss_test.png')
