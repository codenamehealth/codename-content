# ---------------- render
STILLS = [float(x) for x in sys.argv[1:]]
OUTV = OUTD + '/race4_noaudio.mp4'
if not STILLS:
    out = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTV], stdin=subprocess.PIPE)
def emit(img, fo):
    if STILLS: img.convert('RGB').save(OUTD + f'/st_{fo / FPS:.2f}.png')
    else: out.stdin.write(img.convert('RGB').tobytes())
REF_X = 100; REF_Y = FEET[1] - 80 * S + 6     # slime referee stands in Cleo's empty lane
# FOUL stamp (race_v4: 0.8x and placed on Cyrus, so the verdict points at him)
STAMP = Image.new('RGBA', (640, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(STAMP)
sd.rounded_rectangle([10, 10, 630, 190], 28, outline=(230, 40, 40), width=14, fill=(255, 245, 235, 60))
tw = sd.textlength('FOUL!', font=F(100)); sd.text(((640 - tw) / 2, 50), 'FOUL!', font=F(100), fill=(230, 40, 40), stroke_width=4, stroke_fill=(90, 10, 16))
STAMP = STAMP.rotate(-8, expand=True, resample=Image.NEAREST)
STAMP = STAMP.resize((STAMP.width * 4 // 5, STAMP.height * 4 // 5), Image.NEAREST)
NTAIL = int(round(LOOP_TAIL * FPS))
RAY_ORG_FIX = [None]

def race_frame(fo, ta=None):
    """the race and its verdict, exactly as before (fo = race output frame); ta = clock for idle animations"""
    if ta is None: ta = fo / FPS
    tr = fo / FPS
    img = world(fo) if tr < T_TOSS_O + 0.8 else world(fo, skip=('ray',))
    if tr >= T_REF_O:   # slime referee
        u = tr - T_REF_O
        if u < 0.25:
            yy = REF_Y + int((1 - u / 0.25) * 500); img.alpha_composite(REF_I[0], (REF_X, yy))
        elif u < 0.25 + len(REF_W) / 12:
            k = min(len(REF_W) - 1, int((u - 0.25) * 12)); img.alpha_composite(REF_W[k], (REF_X, REF_Y))
        else:
            hop = int(abs(math.sin((ta - T_RWIN_O) * 9)) * 40) if tr >= T_RWIN_O else 0   # happy bounce when Rayleigh wins
            img.alpha_composite(REF_I[int(ta * 6) % len(REF_I)], (REF_X, REF_Y - hop))
    live_overlays(img, fo)
    if T_DQ_O <= tr < T_RWIN_O:   # FOUL! on Cyrus
        u = tr - T_DQ_O; cx, cy, rx = POS[(fo, 'cyrus')]
        sc = max(1.0, 1.7 - u / 0.12 * 0.7); st2 = STAMP.resize((int(STAMP.width * sc), int(STAMP.height * sc)), Image.NEAREST)
        x0 = max(72, min(1022 - st2.width, cx - st2.width / 2)); y0 = FEET[0] - 40 * S - st2.height / 2 + 30
        img.alpha_composite(st2, (int(x0), int(y0)))
    rx_, ry_, rr = POS[(fo, 'ray')]; RAY_ORG = (rr, FEET[3] - 78 * S)
    if tr >= T_TOSS_O:
        head = (RAY_ORG[0] + 46 * S - CROWN.width // 2, RAY_ORG[1] + 4 * S - CROWN.height + 10)
        src = (REF_X + 44 * S - CROWN.width // 2, REF_Y + 24 * S)
        p = min(1, (tr - T_TOSS_O) / 0.8); e = p * p * (3 - 2 * p)
        cx = src[0] + (head[0] - src[0]) * e; cyy = src[1] + (head[1] - src[1]) * e - 260 * math.sin(math.pi * e)
        if p >= 1:
            vf = VIC['ray'][int(ta * 8) % len(VIC['ray'])]; img.alpha_composite(vf, RAY_ORG)
            cyy = head[1] + int(3 * math.sin(ta * 8))
            d = ImageDraw.Draw(img)
            for k2 in range(6):
                ang = ta * 3 + k2; r = 150
                sx_, sy_ = RAY_ORG[0] + 46 * S + math.cos(ang) * r, RAY_ORG[1] + 30 * S + math.sin(ang) * r * 0.6
                d.rectangle([sx_ - 6, sy_ - 6, sx_ + 6, sy_ + 6], fill=(255, 230, 120)); d.rectangle([sx_ - 14, sy_ - 2, sx_ + 14, sy_ + 2], fill=(255, 245, 190)); d.rectangle([sx_ - 2, sy_ - 14, sx_ + 2, sy_ + 14], fill=(255, 245, 190))
        img.alpha_composite(CROWN, (int(cx), int(cyy)))
    # top strip
    if tr < T_FIN_O: hook(img)
    elif tr < T_REF_O: win_banner(img, 'cyrus', 'CYRUS WINS!', tr - T_FIN_O, COL['cyrus'])
    elif tr < T_RWIN_O: pass   # referee + FOUL!: the picture says it (HE SKIPPED A SLIME! cut)
    elif tr < T_RWD_O: win_banner(img, 'ray', 'RAYLEIGH WINS!', tr - T_RWIN_O, COL['ray'])
    return img

# ---------------- flashback look
_yy, _xx = np.mgrid[0:H, 0:W]
_r = np.sqrt(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H * 0.47) / (H * 0.6)) ** 2)
VIG = np.clip(1.15 - 0.75 * _r ** 2, 0.25, 1.0)[..., None].astype(np.float32)
def sepia(img, amt=1.0, seed=0, grain=True):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    g = a @ np.array([0.30, 0.59, 0.11], np.float32)
    sp = np.stack([g * 1.02 + 38, g * 0.86 + 22, g * 0.62 + 4], -1)
    o = a * (1 - amt) + sp * amt
    o = o * (1 - amt + amt * VIG)
    if grain:
        rs = np.random.default_rng(seed); n = rs.normal(0, 7, (H // 4, W // 4)).astype(np.float32)
        o += amt * np.repeat(np.repeat(n, 4, 0), 4, 1)[..., None]
        o *= 1 + amt * 0.03 * math.sin(seed * 2.3)   # projector flicker
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).convert('RGBA')
def rewind_fx(img, k, n):
    """VHS rewind: tracking bands shifted sideways, noise lines, a white rewind icon (no text)"""
    a = np.asarray(img.convert('RGB')).copy(); rs = np.random.default_rng(1000 + k)
    for _ in range(3):
        y0 = int(rs.integers(0, H - 80)); h = int(rs.integers(20, 70)); a[y0:y0 + h] = np.roll(a[y0:y0 + h], int(rs.integers(-60, 60)), 1)
    for _ in range(4):
        y0 = int(rs.integers(0, H - 6)); a[y0:y0 + 4] = np.clip(a[y0:y0 + 4].astype(int) + rs.integers(60, 140, (4, W, 1)), 0, 255)
    im = Image.fromarray(a).convert('RGBA'); d = ImageDraw.Draw(im)
    if (k // 4) % 2 == 0:
        x0, y0 = 120, 560
        for j in range(2):
            xo = x0 + j * 62; d.polygon([(xo + 62, y0), (xo + 62, y0 + 96), (xo, y0 + 48)], fill=(255, 255, 255), outline=(10, 6, 18), width=6)
    return im
GUM = Image.open('../gummies/pick_mel.png').convert('RGBA'); GUM = GUM.resize((GUM.width * 3, GUM.height * 3), Image.NEAREST)   # Rayleigh's melatonin gummy (existing art)
def heart(d, cx, cy, s, col=(255, 90, 140)):
    for (x, y) in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (-2, -1)]:
        d.rectangle([cx + x * s - s // 2, cy + y * s - s // 2, cx + x * s + s // 2 - 1, cy + y * s + s // 2 - 1], fill=col)
BRIBED = [sl for sl in st['cyrus']['slimes'] if sl.get('skipped')][0]
FB_CAM = BRIBED['x'] - 720
FB_TS = 1.2   # source time before GO: all racers still at the start line, far off screen
def fb_handoff(u, fo):
    """flashback 1 (u = seconds in): Rayleigh runs in behind the slime in Cyrus's lane, stops, tosses it a gummy, the slime gobbles it.
    returns (sepia base, colour overlay fn): the gummy and its sparkles stay in full colour on the sepia flashback"""
    HIDE_BRIBE[0] = True; img = world(fo, skip=tuple(G), ts_over=FB_TS, cam_over=FB_CAM); HIDE_BRIBE[0] = False
    feet = FEET[0]; stop_x = 720 - 330 - 46 * S; t_run = 0.75; x_start = -260
    t_toss = 0.95; t_land = t_toss + 0.45
    # the bribed slime (existing idle frames), squash-hop when it swallows the gummy
    fr = SL_IDLE[int((u + 5) * 10) % len(SL_IDLE)]; q = u - t_land; hop = 0; sq = 1.0
    if 0 <= q < 0.45: hop = int(70 * math.sin(math.pi * q / 0.45)); sq = 0.88
    elif 0.45 <= q < 0.75: sq = 1.0 + 0.16 * math.sin((q - 0.45) * 18) * (1 - (q - 0.45) / 0.3)
    fr2 = fr.resize((int(fr.width * sq), int(fr.height / sq)), Image.NEAREST) if abs(sq - 1) > 0.01 else fr
    img.alpha_composite(fr2, (720 - 32 * S - (fr2.width - fr.width) // 2, feet - 62 * S + (fr.height - fr2.height) - hop))
    if u < t_run:
        rx = x_start + (stop_x - x_start) * (u / t_run); rf = RUN['ray'][int(u * 14) % len(RUN['ray'])]
    else:
        rx = stop_x; rf = IDLE['ray'][int(u * 8) % len(IDLE['ray'])]
    img.alpha_composite(rf, (int(rx), feet - 78 * S))
    hand = (stop_x + 66 * S, feet - 46 * S); mouth = (720, feet - 30 * S)
    def overlay(im):
        if t_toss <= u < t_land:
            p = (u - t_toss) / (t_land - t_toss)
            gx = hand[0] + (mouth[0] - hand[0]) * p; gy = hand[1] + (mouth[1] - hand[1]) * p - 170 * math.sin(math.pi * p)
            im.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        if q >= 0: draw_bribe_react(im, q, 720, feet - 26 * S - hop)
    return img, overlay
def draw_bribe_react(img, q, cx, top):
    d = ImageDraw.Draw(img)
    if q < 0.5:
        for k2 in range(5):
            ang = k2 * 1.256 + q * 4; r = 60 + 160 * q
            sx_, sy_ = cx + math.cos(ang) * r, top + 40 + math.sin(ang) * r * 0.7
            d.rectangle([sx_ - 7, sy_ - 7, sx_ + 7, sy_ + 7], fill=(200, 120, 255)); d.rectangle([sx_ - 15, sy_ - 2, sx_ + 15, sy_ + 2], fill=(235, 200, 255)); d.rectangle([sx_ - 2, sy_ - 15, sx_ + 2, sy_ + 15], fill=(235, 200, 255))
    if q > 0.12:
        heart(d, int(cx + 20), int(top - 40 - 50 * min(1, (q - 0.12) / 0.3)), 11)
# ---------------- main loop
events = []
NOUT = int(round(END_O * FPS))
NRWD = int(round(D_RWD * FPS)); NFB1 = int(round(D_FB1 * FPS)); NFB2 = int(round(D_FB2 * FPS))
F_RWD = int(round(T_RWD_O * FPS)); F_FB1 = F_RWD + NRWD; F_FB2 = F_FB1 + NFB1; F_NOW = F_FB2 + NFB2
F_LOOP = NOUT - NTAIL
RW_FROM = F_RWD - 1; RW_TO = int(0.4 * FPS)
F_REPLAY0 = int(round((T_CH_O - 0.7) * FPS))
print('frames: rewind', F_RWD, 'fb1', F_FB1, 'fb2', F_FB2, 'now', F_NOW, 'loop', F_LOOP, 'end', NOUT)
for fo in range(NOUT):
    ta = fo / FPS
    if STILLS and not any(abs(ta - x) < 0.5 / FPS for x in STILLS): continue
    if fo >= F_LOOP:                       # loop tail: start line just before frame 0
        fw = fo - NOUT
        img = world(fw); live_overlays(img, fw); hook(img); emit(img, fo); continue
    if fo < F_RWD:
        img = race_frame(fo)
    elif fo < F_FB1:                       # rewind: the whole race runs backwards to the start line, fading to sepia
        k = fo - F_RWD; p = (k + 1) / NRWD
        fr_src = int(round(RW_FROM + (RW_TO - RW_FROM) * (p ** 1.4)))
        img = world(fr_src)
        img = rewind_fx(sepia(img, min(1, 0.25 + p), seed=fo), k, NRWD)
    elif fo < F_FB2:                       # flashback 1: the bribe
        u = (fo - F_FB1) / FPS
        img, ov = fb_handoff(u, fo)
        img = sepia(img, 1.0, seed=fo); ov(img)
    elif fo < F_NOW:                       # flashback 2: replay of the slime hopping out of Cyrus's way
        fr_src = F_REPLAY0 + (fo - F_FB2)
        img = world(fr_src)
        img = sepia(img, 1.0, seed=fo)
        if BRIBE_POS[0] is not None:
            ts_ = src_t(fr_src / FPS); q = ts_ - (T_CH - 0.6)
            if 0 <= q < 0.6: draw_bribe_react(img, q * 0.8, BRIBE_POS[0][0], BRIBE_POS[0][1])
    else:                                  # back to the present: the post-race scene resumes, Rayleigh crowned
        img = race_frame(fo - FBF)
        k = fo - F_NOW
        if k < 4: blend(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 255, int(200 * (1 - k / 4)))))
        strip_lines(img, END_LINES)
    emit(img, fo)
if not STILLS: out.stdin.close(); out.wait()
# ---------------- sound events (source-time hits remapped to output time)
for gname, s in st.items():
    for kind, t in s['events']:
        to = out_t(t)
        if kind == 'atk': events.append((out_t(t + HIT[gname][0] / ATK_FPS * 0.6), SFX[gname]))
        if kind == 'kill': events.append((to, 'squish'))
        if kind == 'bonk': events.append((to, 'punch'))
T_HOP1_O = out_t(T_CH - 0.6); T_HOP2_O = out_t(T_CH + 0.45)
RP = lambda t_src_out: F_FB2 / FPS + (t_src_out - F_REPLAY0 / FPS)   # race output time -> replay output time
events += [(0.0, 'tick_8bit'), (0.25, 'tick_8bit'), (0.5, 'tick_8bit'), (0.75, 'go_8bit'),
           (T_KLAND_O, 'punch'), (T_KLAND_O + 0.02, 'squish'), (T_KLAND_O + 0.05, 'punch'),
           (T_HOP1_O, 'jump'), (T_HOP2_O, 'jump'), (T_FIN_O, 'ding_8bit'),
           (T_REF_O + 0.3, 'whistle'),
           (T_DQ_O, 'punch'), (T_DQ_O + 0.03, 'buzz_8bit'),
           (T_TOSS_O, 'vg02'), (T_RWIN_O, 'vg02'),
           (T_RWD_O, 'rewind'),
           (T_FB1_O + 0.95, 'swish'), (T_FB1_O + 1.40, 'squish'), (T_FB1_O + 1.52, 'twinkle'),
           (RP(T_HOP1_O), 'jump'), (RP(T_HOP1_O) + 0.05, 'twinkle'),
           (T_NOW_O, 'victory')]
events = [(round(a, 3), b) for a, b in events if 0 <= a < END_O - 0.1]
json.dump({'events': sorted(events), 'end': END_O,
           'beats': {'go': out_t(T_GO), 'king_land': T_KLAND_O, 'slime_hop_out': T_HOP1_O, 'cyrus_passes': T_CH_O, 'slime_hop_back': T_HOP2_O,
                     'cyrus_finish': T_FIN_O, 'ray_finish': T_RAY_O, 'referee': T_REF_O, 'foul': T_DQ_O, 'crown': T_TOSS_O, 'ray_wins': T_RWIN_O,
                     'rewind': T_RWD_O, 'fb_bribe': T_FB1_O, 'fb_replay': T_FB2_O, 'replay_hop': RP(T_HOP1_O), 'present': T_NOW_O, 'loop_cut': T_LOOP_O}},
          open(OUTD + '/race4_events.json', 'w'), indent=1)
print('done', round(END_O, 2), NOUT)
