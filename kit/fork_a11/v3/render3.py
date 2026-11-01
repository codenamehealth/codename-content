import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
G = '../gen/'
def pot(k): return up(Image.open(A + f'jar_{k}.png').convert('RGBA').crop((130, 20, 410, 520)).resize((28, 50), Image.NEAREST), 4)
def pk(d, i, k): return up(crop(Image.open(f'{G}{d}/{i:02d}.png').convert('RGBA')), k)
SEAS = [('cleo', ['DEC', 'JAN', 'FEB'], 'CLEO', 'VITALITY GUILD', (110, 160, 255), 'vit_hd.gif', 'cre', 'creatine', 'snow'),
        ('joy', ['MAR', 'APR', 'MAY'], 'JOY', 'FOUNDATION GUILD', (120, 210, 90), 'found_hd.gif', 'acv', 'acv', 'petal'),
        ('cyrus', ['JUN', 'JUL', 'AUG'], 'CYRUS', 'ENERGY GUILD', (255, 160, 40), 'sun_hd.gif', 'mush', 'mushroom', 'sun'),
        ('ray', ['SEP', 'OCT', 'NOV'], 'RAYLEIGH', 'RECOVERY GUILD', (200, 120, 240), 'recov_hd.gif', 'mel', 'melatonin', 'leaf')]
def bgv(name, bright=0.95): return bg_frames(name, (1080, 1920), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=bright)
BG = {s[0]: bgv(s[5]) for s in SEAS}; HUB = bgv('hub.gif', 0.9)
VICF = {s[0]: vic(s[0], 640) for s in SEAS}
GUM = {s[0]: gummy(s[6], 4) for s in SEAS}; POT = {s[0]: pot(s[7]) for s in SEAS}
PART = {'snow': [pk('snow', i, 2) for i in (0, 4, 9)], 'petal': [pk('petal', i, 3) for i in (0, 4, 9)], 'leaf': [pk('leaf', i, 3) for i in (0, 4, 11)]}
HOL = idle('hollow', 6); HOLS = idle('hollow', 4); GOLD = gummy('gold', 4)
IDL = {s[0]: idle(s[0], 4) for s in SEAS}
T_INTRO = 2.2; SEG = 2.8; T_END = T_INTRO + 4 * SEG; DUR = T_END + 3.6
def particles(img, kind, t, col):
    if kind == 'sun':
        def f(d):
            rb = random.Random(4)
            for k in range(40):
                x = rb.uniform(0, W); y = (rb.uniform(0, H) - t * rb.uniform(30, 80)) % H; s = 4 + 3 * abs(math.sin(t * 4 + k))
                d.rectangle([x - s, y - 1, x + s, y + 1], fill=(255, 240, 170, 200)); d.rectangle([x - 1, y - s, x + 1, y + s], fill=(255, 240, 170, 200))
        layer(img, f); return
    P = PART[kind]; rb = random.Random(9)
    for k in range(34):
        sp = P[k % len(P)]; x0 = rb.uniform(-50, W); vy = rb.uniform(90, 180); vx = rb.uniform(-40, 40)
        y = (rb.uniform(0, H) + t * vy) % (H + 100) - 50; x = (x0 + t * vx + 30 * math.sin(t * 1.5 + k)) % (W + 60) - 30
        img.alpha_composite(sp, (int(x), int(y)))
def season(img, s, u, t):
    g, months, name, guild, col, bg, gk, pk_, part = s
    img.alpha_composite(BG[g][int(t * 6) % len(BG[g])])
    particles(img, part, t, col)
    # glow behind guide
    def glow(d):
        for r, a in ((380, 40), (290, 55), (200, 70)): d.ellipse([540 - r, 1300 - r, 540 + r, 1300 + r], fill=col + (a,))
    layer(img, glow)
    vf = VICF[g][int(u * 8) % len(VICF[g])]
    pop = min(1, u / 0.25); vfs = vf if pop >= 1 else vf.resize((max(1, int(vf.width * (0.6 + 0.4 * pop))), max(1, int(vf.height * (0.6 + 0.4 * pop)))), Image.NEAREST)
    img.alpha_composite(vfs, (540 - vfs.width // 2, 1700 - vfs.height))
    # gummy and potion float in
    a = min(1, max(0, (u - 0.5) / 0.4))
    if a > 0:
        gg = GUM[g]; pp = POT[g]
        img.alpha_composite(pp, (int(150 - pp.width / 2), int(1160 - pp.height / 2 + 14 * math.sin(t * 2.5) + (1 - a) * 300)))
        img.alpha_composite(gg, (int(930 - gg.width / 2), int(1200 - gg.height / 2 + 14 * math.sin(t * 2.5 + 1.5) + (1 - a) * 300)))
    # banner
    def ban(d):
        d.rectangle([0, 300, W, 600], fill=(14, 10, 24, 200)); d.rectangle([0, 300, W, 308], fill=col + (255,)); d.rectangle([0, 592, W, 600], fill=col + (255,))
    layer(img, ban)
    items = []
    for i, m in enumerate(months):
        k = min(1, max(0, (u - 0.1 * i) / 0.2))
        items.append((240 + i * 300, 340 - (1 - k) * 40, m, 76, (255, 255, 255), 8, int(255 * k)))
    k2 = min(1, max(0, (u - 0.35) / 0.25))
    items.append((W / 2, 448, name, 84, col, 9, int(255 * k2)))
    items.append((W / 2, 1760, guild, 40, col, 6, int(255 * k2)))
    text_layer(img, items)
def frame_at(t):
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    if t < T_INTRO:
        img.alpha_composite(HUB[int(t * 6) % len(HUB)])
        fr = HOL[int(t * 6) % len(HOL)]; img.alpha_composite(fr, (540 - fr.width // 2, 1720 - 78 * 6))
        img.alpha_composite(GOLD, (540 - GOLD.width // 2 + 70, int(1720 - 78 * 6 + 40 + 10 * math.sin(t * 4))))
        def b(d): d.rectangle([0, 520, W, 860], fill=(14, 10, 24, 190))
        layer(img, b)
        k = min(1, t / 0.4)
        text_layer(img, [(W / 2, 560, 'YOUR BIRTH MONTH', 64, (255, 255, 255), 8, int(255 * k)), (W / 2, 680, 'IS YOUR GUIDE', 76, (255, 214, 60), 9, int(255 * k))])
    elif t < T_END:
        si = int((t - T_INTRO) // SEG); u = (t - T_INTRO) - si * SEG
        season(img, SEAS[si], u, t)
        # wipe in with a guild colour band
        if u < 0.35:
            prev = Image.new('RGBA', (W, H), (14, 10, 24, 255))
            if si == 0:
                prev.alpha_composite(HUB[int(t * 6) % len(HUB)])
            else:
                season(prev, SEAS[si - 1], SEG - 0.01, t)
            edge = min(W - 1, int(W * (u / 0.35) * 1.15))
            img.paste(prev.crop((edge, 0, W, H)), (edge, 0))
            def band(d): d.rectangle([edge - 30, 0, edge + 10, H], fill=SEAS[si][4] + (255,))
            layer(img, band)
    else:
        u = t - T_END
        img.alpha_composite(HUB[int(t * 6) % len(HUB)])
        def b(d): d.rectangle([0, 0, W, H], fill=(14, 10, 24, 110))
        layer(img, b)
        items = []
        for i, s in enumerate(SEAS):
            g = s[0]; x = 135 + i * 270; k = min(1, max(0, (u - 0.1 * i) / 0.3))
            fr = IDL[g][int(t * 6) % len(IDL[g])]
            img.alpha_composite(fr, (x - fr.width // 2, int(1250 - 78 * 4 + (1 - k) * 200)))
            gg = GUM[g].resize((GUM[g].width // 2, GUM[g].height // 2), Image.NEAREST); img.alpha_composite(gg, (x - gg.width // 2, 1290))
            items.append((x, 1370, s[2] if g != 'ray' else 'RAYLEIGH', 28 if g != 'ray' else 24, s[4], 5, int(255 * k)))
            items.append((x, 1416, s[1][0] + '-' + s[1][2], 26, (255, 255, 255), 5, int(255 * k)))
        fr = HOLS[int(t * 6) % len(HOLS)]; img.alpha_composite(fr, (540 - fr.width // 2, 1770 - 78 * 4))
        img.alpha_composite(GOLD.resize((GOLD.width // 2, GOLD.height // 2), Image.NEAREST), (585, int(1770 - 78 * 4 + 40 + 8 * math.sin(t * 4))))
        def bb(d): d.rectangle([0, 360, W, 640], fill=(14, 10, 24, 210))
        layer(img, bb)
        items += [(W / 2, 400, 'WHICH GUIDE', 76, (255, 255, 255), 8, 255), (W / 2, 510, 'ARE YOU?', 84, (255, 214, 60), 9, 255),
                  (W / 2, 1810, 'Comment your month', 38, (255, 255, 255), 6, int(255 * min(1, u / 0.5)))]
        text_layer(img, items)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in (1.0, 2.35, 3.6, 6.4, 9.2, 12.0, 15.0): frame_at(t).convert('RGB').save(f'still_{t}.png')
        sys.exit()
    wr = Writer('v3_noaudio.mp4')
    for f in range(int(DUR * FPS)): wr.write(frame_at(f / FPS))
    wr.close()
    ev = [(0.15, 'chime')] + [(T_INTRO + i * SEG, 'whoosh_8bit') for i in range(4)] + [(T_INTRO + i * SEG + 0.35, 'twinkle') for i in range(4)] + [(T_END, 'powerup_8bit')]
    json.dump(ev, open('ev.json', 'w')); print('done', DUR)
