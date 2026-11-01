p='r90.py'; s=open(p).read()
def R(a,b):
    global s
    assert s.count(a)==1,a; s=s.replace(a,b)
R("import numpy as np\n", "import numpy as np\nimport hook as HK\n# rc10 review recut (source fork_sz86/v90/r90.py). Bennett APPROVED #90: one growing hole, slimes off the glass; only light trims + universal fixes.\n")
R("HOOK, HB = hook_layer(['SLIMES EAT ALL', 'THE GLASS'], accent=1, color=(130, 210, 255))\nP0, P1 = HB + 12, HB + 116                     # counter panel under the hook",
"""def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
HOOK, HB = band(['SLIMES EAT ALL', 'THE GLASS'], 1, 'HOW MANY SLIMES?', color=(130, 210, 255))   # rc10: 46px comment prompt from frame 0
P0, P1 = HB + 10, HB + 80                      # rc10: one-row counter panel (44px), was two rows of 36/30px""")
R("SPLITS = [2.2, 4.6, 6.8, 9.0, 11.0, 13.0]", "SPLITS = [float(x) for x in os.environ.get('SPLITS', '1.2,2.8,4.4,6.0,7.6,9.2').split(',')]   # rc10: faster doubling (was 2.2,4.6,6.8,9.0,11.0,13.0)")
R("    if t_done is None and t >= 0.8:", "    if t_done is None and t >= 0.1:   # rc10: first bite on frame 3 (was 0.8s)")
R("    if t_done is not None and t > t_done + 2.9: break", "    if t_done is not None and t > t_done + 1.5: break   # rc10: 1.5s after ALL GONE, then cut back to the full glass (loop)")
R("SAVE = (int(1.5 * FPS), int(9 * FPS), int(15 * FPS), NF - 20)", "SAVE = (0, 10, int(3 * FPS), int(t_done * FPS) - 30, int(t_done * FPS) + 10, NF - 1)")
R("""        text_layer(img, [(547, P0 + 14, f'GLASS LEFT: {int(math.ceil(left * 100)) if left > 0 else 0}%', 36, (225, 240, 255), 6, 255),
                         (547, P0 + 62, f'SLIMES: {len(sl)}', 30, (150, 235, 110), 5, 255)])""",
"""        text_layer(img, [(310, P0 + 13, f'GLASS {int(math.ceil(left * 100)) if left > 0 else 0}%', 44, (225, 240, 255), 7, 255),
                         (784, P0 + 13, f'SLIMES {len(sl)}', 44, (150, 235, 110), 7, 255)])""")
R("        text_layer(img, [(547, (P0 + P1) / 2 - int(64 * (0.6 + 0.4 * sc_)) / 2, 'ALL GONE!', int(64 * (0.6 + 0.4 * sc_)), (255, 214, 60), 8, 255)])",
  "        text_layer(img, [(547, (P0 + P1) / 2 - int(56 * (0.6 + 0.4 * sc_)) / 2, 'ALL GONE!', int(56 * (0.6 + 0.4 * sc_)), (255, 214, 60), 8, 255)])")
R("""json.dump(events, open('v90_ev.json', 'w')); print('rendered', NF / FPS)
mix('v90_noaudio.mp4', events, 'chiptune_gameboy.wav', 4, 'v90_mix.mp4')
print('LUFS', loudness('v90_mix.mp4'), '->', louder('v90_mix.mp4', 'v90_final.mp4'))""",
"""json.dump({'events': events}, open('v90_ev.json', 'w')); print('rendered', NF / FPS)""")
open(p,'w').write(s); print('ok')
