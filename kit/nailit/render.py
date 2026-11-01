import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; N=int(6.0*FPS)
def F(s): return ImageFont.truetype(FONT,s)
hub=Image.open(A+'hub.gif'); hub.seek(0); g=hub.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(16))).enhance(0.6).convert('RGBA')
d=ImageDraw.Draw(BG)
for y,t,f,c in ((300,'THINK YOU CAN',F(60),(255,255,255)),(385,'NAIL IT?',F(60),(255,214,90)),(480,'Pause when the gummy',F(34),(255,255,255)),(530,'fits the outline',F(34),(255,255,255)),(1560,'Only 0.1% can',F(46),(255,214,90))):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c,stroke_width=6,stroke_fill=(20,15,35))
def ld(p,h):
    im=Image.open(p); im=im.crop(im.getbbox()); return im.resize((int(im.width*h/im.height),h),Image.LANCZOS)
G=[ld('../gummy/acv_gummy_single.png',560), ld('../gummy/mush_gummy_single.png',470), ld('../gummy/mel_gummy_single.png',560)]
CX,CY=W//2,1050
def outline(img,dil=14):
    a=img.split()[3].point(lambda v:255 if v>100 else 0)
    big=a.filter(ImageFilter.MaxFilter(dil*2+1)); ring=ImageChops.subtract(big.filter(ImageFilter.MaxFilter(7)),big)
    r=np.array(ring)>0; yy,xx=np.nonzero(r); cy,cx=yy.mean(),xx.mean(); ang=np.arctan2(yy-cy,xx-cx)
    dash=((ang*22/np.pi)%2)<1.15; o=np.zeros(r.shape+(4,),np.uint8); o[yy[dash],xx[dash]]=(255,255,255,240); return Image.fromarray(o)
def pad(im,p=40):
    c=Image.new('RGBA',(im.width+2*p,im.height+2*p),(0,0,0,0)); c.paste(im,(p,p)); return c
TARGET=1   # the mushroom gummy's outline
OUT=outline(pad(G[TARGET]))
glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([CX-380,CY-380,CX+380,CY+380],fill=110); glow=glow.filter(ImageFilter.GaussianBlur(120))
gl=Image.new('RGBA',(W,H),(255,230,170,0)); gl.putalpha(glow)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
order=[0,1,2]
for f in range(N):
    img=BG.copy(); img.alpha_composite(gl)
    k=order[(f//3)%3]; gm=G[k]
    img.alpha_composite(gm,(CX-gm.width//2,CY-gm.height//2))
    img.alpha_composite(OUT,(CX-OUT.width//2,CY-OUT.height//2))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (0,3,6): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
