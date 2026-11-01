p='r107.py'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, (s.count(a), a); s=s.replace(a,b)
R("os.chdir(os.path.dirname(os.path.abspath(__file__)))",
  "OUTD = os.path.dirname(os.path.abspath(__file__))\nos.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/wheel')\nsys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['PAUSE IT', '3 TIMES'], accent=1); print('hook bottom', HB)")
R("   ('THE HOLLOW', fit(guide('idle_9.gif'), 60), (70, 60, 100), None),\n","")
R("   ('THE HOLLOW', fit(guide('idle_9.gif'), 62), (70, 60, 100), None), ","   ")
R("CX, CY, R = LW // 2, 300, 148","CX, CY, R = 159, 349, 110            # wheel centred x477 y1047, outer rim radius 360 (was 540,900 / 474)")
R("    if 0 > tp > -GAP: pop = 0.0","    if 0 > tp > -GAP or t < PSTART[0] - GAP: pop = 0.0")
R("ff = subprocess.Popen(","KEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}\nff = subprocess.Popen(")
R("'wheel_noaudio.mp4'], stdin=subprocess.PIPE)","OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)")
R("""    layer(img, lambda dd: dd.rectangle([0, 0, W, 300], fill=(14, 10, 24, 150)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 40, 'PAUSE IT 3 TIMES', F(48), (255, 255, 255), 7)
    for i in range(3):
        px = W / 2 + (i - 1) * 110; done = t >= PSTART[i] + PDUR; cur = i == ph and t < T_END
        d.ellipse([px - 34, 118, px + 34, 186], fill=(255, 214, 60) if done else ((255, 255, 255) if cur else (70, 60, 90)), outline=(20, 15, 35), width=5)
        ctext(d, px, 136, str(i + 1), F(30), (20, 15, 35) if (done or cur) else (160, 150, 180), 0)
    if PSTART[0] - GAP <= t < T_END:
        ctext(d, W / 2, 220, P['title'], F(56), P['col'], 8)
        if pop > 0.5:
            name = P['opts'][idx][0]
            ctext(d, W / 2, CY * Q + R * Q + 110, name, F(60), (255, 255, 255), 8)
            if tp >= 0 and t < PSTART[ph] + PDUR and int(t * 3) % 2 == 0:
                tw = d.textlength('PAUSE NOW!', font=F(40)); bx, by = W / 2 - (tw + 80) / 2, 1640
                d.rectangle([bx, by, bx + 18, by + 52], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                d.rectangle([bx + 30, by, bx + 48, by + 52], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                ctext(d, bx + 80 + tw / 2, by + 6, 'PAUSE NOW!', F(40), (255, 255, 255), 6)""",
"""    RY = HB + 12                                          # pips + PAUSE NOW! row, then the phase title, under the hook
    layer(img, lambda dd: dd.rounded_rectangle([80, RY - 6, 876, RY + 132], 18, fill=(14, 10, 24, 200)))
    d = ImageDraw.Draw(img)
    for i in range(3):
        px = 150 + i * 72; done = t >= PSTART[i] + PDUR; cur = i == ph and t < T_END
        d.ellipse([px - 28, RY, px + 28, RY + 56], fill=(255, 214, 60) if done else ((255, 255, 255) if cur else (70, 60, 90)), outline=(20, 15, 35), width=5)
        ctext(d, px, RY + 14, str(i + 1), F(28), (20, 15, 35) if (done or cur) else (160, 150, 180), 0)
    if PSTART[0] - GAP <= t < T_END:
        ctext(d, 478, RY + 72, P['title'], F(52), P['col'], 8)
        if pop > 0.5:
            name = P['opts'][idx][0]
            ctext(d, 478, CY * Q + (R + 10) * Q + 16, name, F(56), (255, 255, 255), 8)
            if tp >= 0 and t < PSTART[ph] + PDUR and int(t * 3) % 2 == 0:
                tw = d.textlength('PAUSE NOW!', font=F(36)); bx, by = 370, RY + 4
                d.rectangle([bx, by, bx + 16, by + 46], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                d.rectangle([bx + 27, by, bx + 43, by + 46], fill=(255, 255, 255), outline=(20, 15, 35), width=4)
                ctext(d, bx + 70 + tw / 2, by + 6, 'PAUSE NOW!', F(36), (255, 255, 255), 6)""")
R("        ctext(d, W / 2, 1420, '1. GUILD', F(48), (255, 214, 60), 7); ctext(d, W / 2, 1510, '2. OPPONENT', F(48), (255, 110, 90), 7); ctext(d, W / 2, 1600, '3. SIDEKICK', F(48), (120, 220, 255), 7)",
  "        ctext(d, 478, 800, '1. GUILD', F(60), (255, 214, 60), 8); ctext(d, 478, 940, '2. OPPONENT', F(60), (255, 110, 90), 8); ctext(d, 478, 1080, '3. SIDEKICK', F(60), (120, 220, 255), 8)")
R("""        ctext(d, W / 2, 620, 'DID YOU', F(64), (255, 255, 255), 8)
        bounce = 1 + 0.06 * math.sin(u * 6)
        ctext(d, W / 2, 740, 'WIN', F(int(96 * bounce)), (255, 214, 60), 9)
        ctext(d, W / 2, 880, 'OR', F(48), (255, 255, 255), 7)
        ctext(d, W / 2, 970, 'LOSE?', F(int(96 * bounce)), (255, 110, 90), 9)
        ctext(d, W / 2, 1200, 'Comment your combo', F(40), (255, 255, 255), 6)
        for i, nm in enumerate(['GUILD', 'OPPONENT', 'SIDEKICK']):
            px = W / 2 + (i - 1) * 320; py = 1360
            d.rounded_rectangle([px - 140, py, px + 140, py + 150], 16, fill=(30, 24, 44), outline=PH[i]['col'], width=5)""",
"""        ctext(d, 478, 600, 'DID YOU', F(64), (255, 255, 255), 8)
        bounce = 1 + 0.06 * math.sin(u * 6)
        ctext(d, 478, 710, 'WIN', F(int(96 * bounce)), (255, 214, 60), 9)
        ctext(d, 478, 846, 'OR', F(48), (255, 255, 255), 7)
        ctext(d, 478, 926, 'LOSE?', F(int(96 * bounce)), (255, 110, 90), 9)
        ctext(d, 478, 1100, 'Comment your combo', F(40), (255, 255, 255), 6)
        for i, nm in enumerate(['GUILD', 'OPPONENT', 'SIDEKICK']):
            px = 478 + (i - 1) * 270; py = 1220
            d.rounded_rectangle([px - 125, py, px + 125, py + 150], 16, fill=(30, 24, 44), outline=PH[i]['col'], width=5)""")
R("    ff.stdin.write(img.convert('RGB').tobytes())\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev_{f:04d}.png')",
  "    img.alpha_composite(HOOK)\n    ff.stdin.write(img.convert('RGB').tobytes())\n    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')")
R("json.dump({'events': events}, open('wheel_events.json', 'w'))","json.dump({'events': events}, open(OUTD + '/ev.json', 'w'))")
open(p,'w').write(s); print('ok')
