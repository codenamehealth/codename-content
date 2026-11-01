# Oct 29 coordinator pass on #19: cliff edge + bottom fill (applied after edit19.py)
p = 'r19.py'; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
rep("BG1 = panel_bg('found_hd.gif', X1, 1.0, GL1, PH1); BG2 = panel_bg('found_hd.gif', 300, 1.0, GL2, PH2)\n",
"""BG1 = panel_bg('found_hd.gif', X1, 1.0, GL1, PH1); BG2 = panel_bg('found_hd.gif', 300, 1.0, GL2, PH2)
# Oct 29 bottom fill: the tiled/mirrored meadow strip under the lower scene is covered by the scene's own near foreground
# (native x250-790, y870-1080: grass + the big dark fern clump) at an integer 2x, bottom-anchored to the frame edge, blended in
# over the last 40 rows of the real scene and darkened a little toward the bottom (near-camera foreground). No tiling.
_FGF = bg_frames('found_hd.gif', (1920, 1080), step=2)
FG_H = 420; FG_Y = PH2 - FG_H
_ram = Image.new('L', (1, FG_H), 255)
for _y in range(30): _ram.putpixel((0, _y), int(255 * _y / 30))
_dk = Image.new('L', (1, FG_H), 0)
for _y in range(FG_H): _dk.putpixel((0, _y), int(120 * max(0, (_y - 80) / (FG_H - 80))))
for _i in range(len(BG2)):
    _fg = _FGF[_i % len(_FGF)].crop((250, 870, 790, 1080)).resize((1080, FG_H), Image.NEAREST)
    _sh = Image.new('RGBA', _fg.size, (6, 10, 8, 255)); _sh.putalpha(_dk.resize(_fg.size)); _fg.alpha_composite(_sh)
    _fg.putalpha(_ram.resize(_fg.size)); BG2[_i].alpha_composite(_fg, (0, FG_Y))
""")
rep("LEDGE = up(crop(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA')), 3)\n",
"""LEDGE = up(crop(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA')), 3)
# Oct 29 cliff: the flat black pit is now a side-on chasm: a jagged ground edge (pixel-stepped, dark earth lip, the far rim
# fringed with the ledge_cands/01 grass cap), a short far rock wall (ledge_cands/02 stones) dropping into a teal-to-black
# gradient, a distant tree line from the same forest scene sunk in mist, and drifting mist. The near ledge sprite stays the
# cliff Joy runs off. All built from existing scenery art.
from PIL import ImageChops
CH_RIM = GL1 - 104
_mr = random.Random(5)
_m4 = Image.new('L', (W // 4, PH1 // 4), 0); _pts = [(201, PH1 // 4 + 1), (201, 201)]
_y = 201; _x = 201
while _y > CH_RIM // 4 + 2:
    _y -= _mr.choice((2, 3, 4)); _x = max(193, min(203, _x + _mr.choice((-2, -1, 0, 1, 2)))); _pts.append((_x, _y))
_pts.append((_x, CH_RIM // 4)); _x2 = _x
while _x2 < W // 4:
    _x2 += _mr.choice((3, 4, 5, 6)); _pts.append((_x2, CH_RIM // 4 + _mr.choice((-2, -1, 0, 1, 2))))
_pts += [(W // 4 + 2, CH_RIM // 4), (W // 4 + 2, PH1 // 4 + 1)]
ImageDraw.Draw(_m4).polygon(_pts, fill=255)
CHM = _m4.resize((W, PH1), Image.NEAREST)
_ab = Image.new('RGBA', (W, PH1), (0, 0, 0, 255)); _ad = ImageDraw.Draw(_ab)
for _yy in range(CH_RIM - 10, PH1):
    _v = max(0, min(1, (_yy - CH_RIM) / (PH1 - CH_RIM)))
    _c = tuple(int(a0 + (a1 - a0) * _v ** 0.7) for a0, a1 in zip((92, 132, 128), (5, 8, 11)))
    _ad.line([(0, _yy), (W, _yy)], fill=_c + (255,))
_f0 = bg_frames('found_hd.gif', (1920, 1080))[0]
_tl = _f0.crop((1000, 20, 1920, 330)).resize((460, 155), Image.NEAREST)          # distant canopy, half size
_tg = _tl.convert('L').point(lambda v: int(v * 0.8)); _tl = Image.merge('RGBA', (_tg.point(lambda v: int(v * 0.55)), _tg.point(lambda v: int(v * 0.85)), _tg.point(lambda v: int(v * 0.85)), Image.new('L', _tg.size, 255)))
_ta = Image.new('L', (1, 155), 0)
for _yy in range(155): _ta.putpixel((0, _yy), int(200 * min(1, _yy / 20) * max(0, 1 - _yy / 155)))
_tl.putalpha(_ta.resize(_tl.size))
for _xx in (760, 760 + 460 - 140):
    _ab.alpha_composite(_tl if _xx == 760 else _tl.transpose(Image.FLIP_LEFT_RIGHT), (_xx, CH_RIM + 38))
_L2 = Image.open(PL + 'plat/ledge_cands/02.png').convert('RGBA').crop((4, 52, 92, 92))
_L2 = up(_L2, 1); _fw = Image.new('RGBA', (W, 40), (0, 0, 0, 0)); _xx = 700
while _xx < W: _fw.alpha_composite(_L2, (_xx, 0)); _xx += _L2.width
_fa = Image.new('L', (1, 40), 0)
for _yy in range(40): _fa.putpixel((0, _yy), int(230 * (1 - _yy / 40)))
_fw.putalpha(ImageChops.multiply(_fw.getchannel('A'), _fa.resize(_fw.size)))
_ab.alpha_composite(_fw, (0, CH_RIM + 2))
CHASM = Image.new('RGBA', (W, PH1), (0, 0, 0, 0)); CHASM.paste(_ab, (0, 0), CHM)
_rim = ImageChops.subtract(CHM.filter(ImageFilter.MaxFilter(9)), CHM)
_rl = Image.new('RGBA', (W, PH1), (58, 40, 28, 255)); _rl.putalpha(_rim); CHASM.alpha_composite(_rl)
_cap = up(Image.open(PL + 'plat/ledge_cands/01.png').convert('RGBA').crop((0, 0, 93, 14)), 2)
_xx = 790
while _xx < W:
    CHASM.alpha_composite(_cap, (_xx, CH_RIM - 20)); _xx += _cap.width - 8
MIST = Image.new('RGBA', (W * 2, PH1), (0, 0, 0, 0)); _md = ImageDraw.Draw(MIST); _mr = random.Random(5)
for _q in range(16):
    _cx = _mr.uniform(0, W * 2); _cy = _mr.uniform(CH_RIM + 70, CH_RIM + 150); _rw = _mr.uniform(90, 200); _rh = _mr.uniform(12, 26)
    _md.ellipse([_cx - _rw, _cy - _rh, _cx + _rw, _cy + _rh], fill=(170, 200, 196, int(_mr.uniform(50, 90))))
MIST = MIST.filter(ImageFilter.GaussianBlur(14))
""")
rep("""    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, min(255, 150 + int((y - GL1 + 60) * 1.2)))) for y in range(GL1 - 60, PH, 4)])
    layer(p1, lambda d: [d.rectangle([EDGE + 22, y, W, y + 4], fill=(6, 4, 14, int(150 * (y - (GL1 - 110)) / 50))) for y in range(GL1 - 110, GL1 - 60, 4)])
""", """    p1.alpha_composite(CHASM)
    _mo = int(130 + 110 * math.sin(2 * math.pi * t / DUR));   # drifts and comes back for the loop
    _mc = MIST.crop((_mo, 0, _mo + W, PH1)); _mc.putalpha(ImageChops.multiply(_mc.getchannel('A'), CHM)); p1.alpha_composite(_mc)
""")
rep("    im = Image.open(p).convert('RGBA'); a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([0, 81, 92, 92], fill=0); im.putalpha(a); FALL.append(up(im, K))",
    "    im = Image.open(p).convert('RGBA'); a = im.getchannel('A'); ImageDraw.Draw(a).rectangle([0, 81, 92, 92], fill=0)\n"
    "    if p.endswith('04.png'): ImageDraw.Draw(a).rectangle([80, 74, 92, 81], fill=0)   # stray ground chip (was invisible on the black pit)\n"
    "    im.putalpha(a); FALL.append(up(im, K))")
open(p, 'w').write(s)
