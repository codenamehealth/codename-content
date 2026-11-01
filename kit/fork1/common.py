import os, glob, math, json, subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = SP + 'npmfont/ps/package/files/PressStart2P.ttf'; A = SP + 'pause/assets/'; PL = SP + 'pixellab/'
W, H, FPS = 1080, 1920, 30
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def crop(im): return im.crop(im.getbbox())
def up(im, k): return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255, sc=(20, 15, 35)):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=tuple(fill[:3]) + (a,), stroke_width=sw, stroke_fill=tuple(sc[:3]) + (a,))
def text_layer(img, items):
    """items: (x, y, text, size, fill, stroke, alpha) centered; drawn with real alpha blending"""
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for it in items:
        x, y, t, s, fill, sw, a = it
        ctext(d, x, y, t, F(s), fill, sw, a)
    img.alpha_composite(L)
def gif_frames(path, scale=None, h=None):
    im = Image.open(path); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    if h is not None:
        bb = None
        for f in fr:
            b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
        fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
        return [f.resize((max(1, int(f.width * k)), h), Image.NEAREST) for f in fr]
    if scale: fr = [up(f, scale) for f in fr]
    return fr
IDLE_FILE = {'joy': 'idle_0.gif', 'cyrus': 'idle_1.gif', 'ray': 'idle_2.gif', 'cleo': 'idle_3.gif', 'hollow': 'idle_9.gif'}
def idle(g, k=1):
    """Syeda idle loop at native 92px canvas times k (feet at y=78*k)"""
    fr = gif_frames(A + IDLE_FILE[g])
    return [up(f.resize((92, 92), Image.NEAREST), k) for f in fr]
VIC = {'joy': 'vic_Victory_Pose.gif', 'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif', 'ray': 'vic_victoryPose_1.gif', 'hollow': 'hollow-victory.gif'}
def vic(g, h): return gif_frames(A + VIC[g], h=h)
def seq(d, k=2, lo=1, hi=None):
    fs = sorted(glob.glob(d + '/*.png'))[lo:hi]
    return [up(Image.open(p).convert('RGBA'), k) for p in fs]
GUMK = ['mush', 'acv', 'mel', 'cre', 'gold']
def gummy(kind, k=2): return up(Image.open(PL + f'gummies/pick_{kind}.png').convert('RGBA'), k)
def bg_frames(name, size, box=None, step=1, bright=1.0, blur=0):
    im = Image.open(A + name); out = []
    for i in range(0, im.n_frames, step):
        im.seek(i); f = im.convert('RGB')
        if box: f = f.crop(box)
        f = f.resize(size, Image.NEAREST)
        if bright != 1.0: f = ImageEnhance.Brightness(f).enhance(bright)
        if blur: f = f.filter(ImageFilter.GaussianBlur(blur))
        out.append(f.convert('RGBA'))
    return out
class Writer:
    def __init__(self, path):
        self.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    def write(self, img): self.p.stdin.write(img.convert('RGB').tobytes())
    def close(self): self.p.stdin.close(); self.p.wait()
def mix(video, events, music, offset, out, vol=0.55):
    json.dump({'events': events}, open(video + '.events.json', 'w'))
    r = subprocess.run(['python3', PL + 'mix.py', video, video + '.events.json', SP + 'music_adobe/' + music, str(offset), out, str(vol)], capture_output=True, text=True)
    print(r.stdout[-300:], r.stderr[-300:])
def ship(mp4, zipname, inner):
    os.makedirs(PL + 'batch', exist_ok=True); tmp = PL + 'batch/_z_' + zipname
    os.makedirs(tmp, exist_ok=True); subprocess.run(['cp', mp4, tmp + '/' + inner])
    subprocess.run(['bash', '-c', f'cd "{tmp}" && rm -f "../{zipname}" && zip -q "../{zipname}" "{inner}" && cd .. && rm -rf "{tmp}"'])
    return PL + 'batch/' + zipname
def sheet(mp4, out, n=8, cols=8):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4], capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-vf', f'fps={n}/{d},scale=270:480,tile={cols}x{max(1, n // cols)}', '-frames:v', '1', out])
