import sys
from PIL import Image, ImageDraw
fs=sys.argv[2:]; out=sys.argv[1]; w,h=360,640
M=Image.new('RGB',(w*len(fs),h+16),'white');D=ImageDraw.Draw(M)
for i,f in enumerate(fs): M.paste(Image.open(f).resize((w,h)),(i*w,16)); D.text((i*w+4,2),f,fill='black')
M.save(out)
