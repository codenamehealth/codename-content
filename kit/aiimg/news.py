from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import sys
FD='/usr/share/fonts/opentype/inter/'
W,H=1080,1350; PH=800
def font(n,s): return ImageFont.truetype(FD+n,s)
def make(photo, crop, headline_lines, out, kicker='DEVELOPING STORY', ay=0.5):
    src=Image.open(photo).convert('RGB').crop(crop)
    # fill a 1080x800 frame (cover)
    k=max(W/src.width, PH/src.height); im=src.resize((round(src.width*k),round(src.height*k)),Image.LANCZOS)
    ox=(im.width-W)//2; oy=int((im.height-PH)*ay); im=im.crop((ox,oy,ox+W,oy+PH))
    im=im.filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2))
    c=Image.new('RGB',(W,H),(17,17,17)); c.paste(im,(0,0)); d=ImageDraw.Draw(c)
    # logo badge
    cx,cy,r=130,130,92
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(200,30,40))
    f=font('Inter-Black.otf',40)
    for i,t in enumerate(['CODE','NAME']):
        w=d.textlength(t,font=f); d.text((cx-w/2,cy-44+i*46),t,font=f,fill='white')
    # kicker
    f=font('Inter-Medium.otf',34); w=d.textlength(kicker,font=f); d.text(((W-w)/2,PH+28),kicker,font=f,fill=(225,225,225))
    # headline: fit size
    for s in range(74,40,-2):
        f=font('Inter-Black.otf',s)
        if max(d.textlength(t,font=f) for t in headline_lines)<=W-90: break
    lh=int(s*1.1); total=lh*len(headline_lines); y0=PH+92+(H-74-(PH+92)-total)//2
    for i,t in enumerate(headline_lines):
        w=d.textlength(t,font=f); d.text(((W-w)/2,y0+i*lh),t,font=f,fill='white')
    # footer
    d.rectangle([0,H-72,W,H],fill=(200,30,40))
    f=font('Inter-SemiBold.otf',32); t='CODE NAME NEWS  •  MORE AS IT HAPPENS'
    w=d.textlength(t,font=f); d.text(((W-w)/2,H-72+19),t,font=f,fill='white')
    c.save(out,quality=94)
if __name__=='__main__':
    make('Creatine_-_lifestyle_grid_panel.png',(40,40,522,522),
         ['TEAMMATE WHO SAID “BRB”','40 MINUTES AGO STILL','LISTED AS ONLINE,','SQUAD HOLDING OUT HOPE'],'news_n13.jpg')
    make('Mushroom_-_lifestyle_grid_panel.png',(558,558,1040,1040),
         ['FAMILY CONFIRMS LOCAL MAN','WILL BE AT THANKSGIVING','DINNER “AFTER THIS ONE RUN”'],'news_n20.jpg', kicker='BREAKING NEWS', ay=0.95)
