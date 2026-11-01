p='r15.py'; s=open(p).read()
OUTD='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c2/v15/'
rep=[
("os.chdir(os.path.dirname(os.path.abspath(__file__)))","os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze')\nOUTD = '%s'" % OUTD),
("GUM = Image.open('../gummies/pick_gold.png')","GUM = Image.open('../gummies/pick_mush.png')   # gold GLOW UP -> mushroom SPEED (gummy powers rule)"),
("SL = 0.5","SL = 0.5\nSTUN, KB = float(os.environ.get('STUN', '0.85')), float(os.environ.get('KB', '430'))   # shove: target stunned STUN s, knocked back KB px/s"),
("""                         ph=rnd.uniform(0, 6.28), caught=None, out=None, mode='side', slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, behind=None, dist=0.0)
    gum_taken = None; frames = []""","""                         ph=rnd.uniform(0, 6.28), caught=None, out=None, mode='side', slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, behind=None, dist=0.0, stun=-9.0, scd=-9.0)
    gum_taken = None; frames = []; shoves = []"""),
("""            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))
            sp = s['base']""","""            stunned = t < s['stun']
            sliding = (t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))) and not stunned
            sp = s['base']"""),
("""            if sliding:
                # locked straight-line slide""","""            if stunned:
                s['vx'] *= 0.86; s['vy'] *= 0.86          # knocked back, dazed: no steering
            elif sliding:
                # locked straight-line slide"""),
("            if not sliding and t - s['slide'] > 1.0 and t > T_START + 0.8:\n                ux, uy","            if not sliding and not stunned and t - s['slide'] > 1.0 and t > T_START + 0.8:\n                ux, uy"),
("""                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.8:
                        v2 = math.hypot(s['vx'], s['vy']) or 1
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v2, s['vy'] / v2; sliding = True; continue
""","""                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and not stunned and t >= o['stun'] and t - s['scd'] > 1.2 and t > T_START + 0.6:
                        # SHOVE: bump the one in the way, they get knocked back and stunned
                        ux, uy = o['x'] - s['x'], o['y'] - s['y']; L2 = math.hypot(ux, uy) or 1
                        o['stun'] = t + STUN; o['vx'], o['vy'] = ux / L2 * KB, uy / L2 * KB
                        s['scd'] = t; s['vx'] *= 0.6; s['vy'] *= 0.6
                        shoves.append((round(t, 3), n, m, (s['x'] + o['x']) / 2, (s['y'] + o['y']) / 2)); continue
"""),
("""                               out=s['out'] is not None and s['out'] <= t, mode=s['mode'], slide=s['slide'], sliding=s['sliding'], boost=s['boost'], dist=s['dist']) for n, s in racers.items()}, front, gum_taken))""",
"""                               out=s['out'] is not None and s['out'] <= t, mode=s['mode'], slide=s['slide'], sliding=s['sliding'], boost=s['boost'], dist=s['dist'],
                               stun=t < s['stun'], st0=s['stun'] - STUN) for n, s in racers.items()}, front, gum_taken))"""),
("    return racers, frames, gum_taken\ndef score(seed):\n    rc, fr, gt = sim(seed)",
 "    return racers, frames, gum_taken, shoves\ndef score(seed):\n    rc, fr, gt, sv = sim(seed)\n    if len(sv) < int(os.environ.get('NSH', '3')) or len(set(x[2] for x in sv)) < 2: return None"),
("    return round(tw, 2), win, round(gt[1], 1), rc[win]['behind'], [round(c, 1) for c in caught]",
 "    return round(tw, 2), win, round(gt[1], 1), rc[win]['behind'], [round(c, 1) for c in caught], [(x[0], x[1][:2] + '>' + x[2][:2]) for x in sv]"),
("rc, FR, GT = sim(SEED)","rc, FR, GT, SHV = sim(SEED)\nprint('shoves', [(x[0], x[1], x[2]) for x in SHV])"),
("'shadow_sz_noaudio.mp4'","OUTD + 'v15_noaudio.mp4'"),("open('shadow_sz_events.json', 'w')","open(OUTD + 'v15_events.json', 'w')"),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
