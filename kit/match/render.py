import numpy as np, subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS,N,MATCH=1080,1920,30,270,92
def F(s): return ImageFont.truetype(FONT,s)
random.seed(4)
# background: Moon Temple at night, heavily blurred and dimmed, with a starfield
g=Image.open(A+'scene_moon.png').convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
g=g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14)); g=ImageEnhance.Brightness(g).enhance(0.32).convert('RGBA')
st=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(st)
for _ in range(260):
    x,y=random.randrange(W),random.randrange(H); r=random.choice([1,1,2,2,3]); a=random.randint(70,200)
    d.rectangle([x,y,x+r,y+r],fill=(220,225,255,a))
g.alpha_composite(st)
band=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(band).rectangle([0,150,W,615],fill=(8,8,20,150)); g.alpha_composite(band)
d=ImageDraw.Draw(g)
def ctext(y,t,f,fill):
    w=d.textlength(t,font=f); d.text(((W-w)/2+4,y+4),t,font=f,fill=(0,0,0,180)); d.text(((W-w)/2,y),t,font=f,fill=fill)
ctext(215,'PAUSE WHEN',F(66),(255,255,255)); ctext(325,'ALL 3 MATCH',F(66),(255,255,255)); ctext(510,'ONLY 1 FRAME!',F(44),(255,214,90))
BOX=(90,900,990,1298)
BG=g
# icons
def first(path):
    im=Image.open(A+path); im.seek(0); return im.convert('RGBA')
def bust(img,frac=0.58):
    b=img.getbbox(); c=img.crop(b); return c.crop((0,0,c.width,int(c.height*frac)))
def scale_to(img,h):
    k=max(1,round(h/img.height)); return img.resize((img.width*k,img.height*k),Image.NEAREST)
def scale_f(img,h):
    k=h/img.height; return img.resize((int(img.width*k),int(img.height*k)),Image.NEAREST)
IC={
 'H':scale_f(bust(first('idle_9.gif')),205),   # the Hollow
 'L':scale_f(bust(first('idle_7.gif')),205),   # Cleo
 'M':scale_f(bust(first('idle_6.gif')),205),   # Rayleigh
 'O':scale_f(bust(first('idle_8.gif')),205),   # Cyrus
 'R':scale_f(bust(first('idle_5.gif')),205),   # Joy
 'C':scale_f(first('jar_acv.png').crop(first('jar_acv.png').getbbox()),215),  # ACV potion
}
dr=first('dragon.gif'); DR=scale_f(dr.crop(dr.getbbox()),250)
def glow(img,color,r=22,k=1.8):
    a=img.split()[3].filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(r)).point(lambda v:min(255,int(v*k)))
    o=Image.new('RGBA',img.size,color+(0,)); o.putalpha(a); return o
def padd(img,p=40):
    c=Image.new('RGBA',(img.width+2*p,img.height+2*p),(0,0,0,0)); c.paste(img,(p,p)); return c
DRG=padd(DR); DRGL=glow(DRG,(255,140,40),26,2.0)
COMBOS=[('H','L','M'),('O','M','L'),('H','O','H'),('O','R','C'),('H','C','R'),('O','H','O')]
ORDER=['H','L','M','O','R','C']
CX=[243,540,837]; CY=1099
def dim(img,f):
    o=img.copy(); o.putalpha(img.split()[3].point(lambda v:int(v*f))); return o
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
rnd=random.Random(11)
for f in range(N):
    img=BG.copy()
    reel=Image.new('RGBA',(W,H),(0,0,0,0))
    if f==MATCH:
        for cx in CX:
            reel.alpha_composite(DRGL,(cx-DRG.width//2,CY-DRG.height//2)); reel.alpha_composite(DRG,(cx-DRG.width//2,CY-DRG.height//2))
    else:
        combo=COMBOS[f%6]
        for i,cx in enumerate(CX):
            k=combo[i]; ic=IC[k]; jy=rnd.randint(-14,14)
            nb_up=IC[ORDER[(ORDER.index(k)+1+i)%6]]; nb_dn=IC[ORDER[(ORDER.index(k)+3+i)%6]]
            reel.alpha_composite(dim(nb_up,0.35),(cx-nb_up.width//2,CY-ic.height//2-nb_up.height-40+jy))
            reel.alpha_composite(dim(nb_dn,0.35),(cx-nb_dn.width//2,CY+ic.height//2+40+jy))
            reel.alpha_composite(ic,(cx-ic.width//2,CY-ic.height//2+jy))
    # reels are only visible inside the window, plus a faint peek above it like the reference
    win=Image.new('L',(W,H),0); wd=ImageDraw.Draw(win); wd.rectangle(BOX,fill=255); wd.rectangle([BOX[0],BOX[1]-150,BOX[2],BOX[1]-1],fill=45)
    reel.putalpha(Image.fromarray(np.minimum(np.array(reel.split()[3]),np.array(win))))
    img.alpha_composite(reel)
    d2=ImageDraw.Draw(img); d2.rectangle(BOX,outline=(201,162,74),width=4)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (0,MATCH): img.convert('RGB').save(f'frame_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
