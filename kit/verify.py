import os,sys,collections
from PIL import Image
OUT='/home/claude/charlie/raw/'
man={l.split()[0]:int(l.split()[2]) for l in open(sys.argv[1]) if l.strip()}
bad=[];dims=collections.Counter()
for t,sz in sorted(man.items()):
    p=OUT+t
    if not os.path.exists(p): bad.append((t,'missing'));continue
    if os.path.getsize(p)!=sz: bad.append((t,'size',os.path.getsize(p),sz))
    try:
        with Image.open(p) as im:
            im.verify()
        with Image.open(p) as im:
            im.load(); dims[(im.size,im.mode)]+=1
            exif=im.getexif().get(274)
            if exif and exif!=1: dims[('orientation',exif)]+=1
    except Exception as e: bad.append((t,'pil',str(e)))
extra=set(os.listdir(OUT))-set(man)
print('files in dir',len(os.listdir(OUT)),'manifest',len(man),'extra',extra)
print('bad',bad)
print(dims)
