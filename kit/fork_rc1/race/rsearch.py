import sys
src = open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1/race/render_race3.py').read().split('#### ---- v2 render follows')[0]
__file__ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1/race/render_race3.py'
exec(src)
print('559', score(559), flush=True)
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    r = score(sd)
    if r: print(sd, r, flush=True)
