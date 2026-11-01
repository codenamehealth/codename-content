# torch on a standing iron pole (native res): wall bracket removed, handle continues into a pole with a tripod base
from PIL import Image, ImageDraw
import numpy as np, glob
TA = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze/torch_anim/'
D, M, L = (34, 30, 38, 255), (62, 56, 70, 255), (104, 96, 112, 255)   # dark / mid / light iron
def stand_torch(im, base=88):
    a = np.array(im.convert('RGBA'))
    a[38:62, 23:] = 0                       # bracket
    c = Image.new('RGBA', (48, base + 2), (0, 0, 0, 0)); c.paste(Image.fromarray(a), (0, 0))
    d = ImageDraw.Draw(c)
    # pole (x18-22) from under the handle to the base
    d.rectangle([18, 60, 22, base - 6], fill=D); d.rectangle([19, 60, 19, base - 6], fill=L); d.rectangle([20, 60, 21, base - 6], fill=M)
    for y in (62, 72):   # collars
        d.rectangle([16, y, 24, y + 2], fill=D); d.line([17, y, 23, y], fill=L)
    # tripod base
    d.polygon([(18, base - 7), (22, base - 7), (29, base), (26, base), (20, base - 4), (14, base), (11, base)], fill=D)
    d.line([(17, base - 6), (12, base - 1)], fill=L); d.line([(23, base - 6), (28, base - 1)], fill=M)
    d.rectangle([18, base - 7, 22, base], fill=D); d.line([19, base - 7, 19, base], fill=L)
    d.rectangle([10, base, 15, base + 1], fill=D); d.rectangle([25, base, 30, base + 1], fill=D); d.rectangle([17, base, 23, base + 1], fill=D)
    return c
if __name__ == '__main__':
    fr = stand_torch(Image.open(TA + '00.png'))
    bg = Image.new('RGBA', fr.size, (230, 190, 120, 255)); bg.alpha_composite(fr); bg.resize((fr.width * 6, fr.height * 6), Image.NEAREST).save('stand_preview.png')
