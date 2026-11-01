p = 'r78.py'; s = open(p).read()
def R(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
R("sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer",
  "sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2\nsys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong\nSTILL = os.environ.get('STILL')")
R("DUR = 11.0; N = int(DUR * FPS); T_GO, T_UP = 1.4, 8.4",
  "# rc8: timer runs from frame 0 (was a still 1.4s), 7s to count, TIME'S UP held 1.3s then loops to the full tray\nT_GO, T_UP = 0.0, 7.0; DUR = T_UP + 1.3; N = int(round(DUR * FPS))")
R("HOOK, HB = hook_layer(['HOW MANY GUMMIES', 'DO YOU SEE?'], accent=1, sub='ONLY GENIUSES GET IT RIGHT')",
  "# rc8: comment prompt as a real 46px band line from frame 0; ONLY GENIUSES GET IT RIGHT (36px sub) cut: 26 chars cannot reach 44px on one line anywhere in the safe width\nHOOK, HB = hook_layer2(['HOW MANY GUMMIES', 'DO YOU SEE?'], accent=1, sub='Comment your number')")
R("""    for k, x, y, s in hidden + items + [tiny]:
        g = gummy(k, s);""", """    for k, x, y, s in hidden + items + [tiny]:
        g = GACV if (k == 'acv' and s == 3) else gummy(k, s);""")
R("w = Writer('v78_noaudio.mp4')", "GACV = up(acv_gummy_strong(), 3)   # rc8: gummy shine on Syeda's ACV gummies (VETTING)\nw = Writer('v78_noaudio.mp4')\nev = [(0.0, 'chime'), (T_UP, 'buzz_8bit')] + [(round(T_UP - k, 3), 'tick_8bit') for k in (3, 2, 1)]   # rc8: ticks on the last 3 seconds only (was every second)")
R("""        its += [((bx0 + bx1) / 2, by0 + 18, 'COUNT', 32, (255, 255, 255), 5, 255), ((bx0 + bx1) / 2, by0 + 62, 'CAREFULLY...', 32, (255, 255, 255), 5, 255)]""",
  """        its += [((bx0 + bx1) / 2, by0 + 10, 'COUNT', 44, (255, 255, 255), 6, 255),
                ((bx0 + bx1) / 2, by0 + 60, 'CAREFULLY', 44, (255, 255, 255), 6, 255)]   # rc8: 32 -> 44px""")
R("""        its.append((830, BAR_Y + 2, f'{int(math.ceil(T_UP - t))}s', 34, (255, 255, 255), 5, 255))""",
  """        sec = int(math.ceil(T_UP - t)); ph = sec - (T_UP - t); sz = 48 if ph > 0.15 else 56   # rc8: 34 -> 48px, pops on each tick
        its.append((832, BAR_Y + 18 - sz / 2, f'{sec}s', sz, (255, 255, 255) if sec > 3 else (255, 110, 90), 7, 255))""")
R("""        layer(img, lambda d: d.rounded_rectangle([CX - 370, cy - 100, CX + 370, cy + 100], 24, fill=(20, 16, 34, int(230 * a / 255)), outline=(255, 214, 60, a), width=5))
        its += [(CX, cy - 70, "TIME'S UP!", 60, (255, 214, 60), 7, a), (CX, cy + 26, 'COMMENT YOUR NUMBER', 34, (255, 255, 255), 5, a)]""",
  """        # rc8: card centred in the wide upper zone (x547) so the comment line can be 44px (was 34px)
        layer(img, lambda d: d.rounded_rectangle([547 - 462, cy - 110, 547 + 462, cy + 100], 24, fill=(20, 16, 34, int(235 * a / 255)), outline=(255, 214, 60, a), width=6))
        its += [(547, cy - 82, "TIME'S UP!", 72, (255, 214, 60), 9, a), (547, cy + 22, 'COMMENT YOUR NUMBER', 44, (255, 255, 255), 6, a)]""")
R("""    if f in (0, 120, 290): img.convert('RGB').save(f'f78_{f}.png')
w.close(); print('done')""",
  """    if STILL and f in [int(x) for x in STILL.split(',')]: img.convert('RGB').save(f'k78_{f}.png')
w.close(); json.dump({'events': ev}, open('v78_ev.json', 'w')); print('done', DUR, ev)""")
open(p, 'w').write(s); print('ok')
