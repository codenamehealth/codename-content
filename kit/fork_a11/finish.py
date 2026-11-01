import sys, json; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
# finish.py video_noaudio ev.json music offset outname [vol]
v, evp, music, off, outname = sys.argv[1:6]; vol = float(sys.argv[6]) if len(sys.argv) > 6 else 0.55
ev = json.load(open(evp)); ev = ev['events'] if isinstance(ev, dict) else ev
tmp = v.replace('.mp4', '_mix.mp4'); mix(v, ev, music, float(off), tmp, vol)
out = PL + 'batch_safe/' + outname; print('LUFS', louder(tmp, out), out)
