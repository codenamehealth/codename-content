p='r64.py'; s=open(p).read()
a='''    j = int(round((t - t0) * FPS)) - 1
    return path[max(0, min(j, len(path) - 1))]'''
assert s.count(a)==1
s=s.replace(a,'''    j = int(round((t - t0) * FPS)) - 1
    if j < 0:   # the spawn frame: one step back along the first frame's motion (no one-frame stall at spawn)
        x, y, vx, vy = path[0]; return (x - vx / FPS, y - vy / FPS + 0.5 * GRAV / FPS ** 2, vx, vy - GRAV / FPS)
    return path[min(j, len(path) - 1)]''')
open(p,'w').write(s)
