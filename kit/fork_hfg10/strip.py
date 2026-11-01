import sys
from PIL import Image
fs=sys.argv[2:]; ims=[Image.open(f).convert('RGB').resize((540,960)) for f in fs]
s=Image.new('RGB',(540*len(ims),960)); [s.paste(im,(i*540,0)) for i,im in enumerate(ims)]; s.save(sys.argv[1],quality=85)
