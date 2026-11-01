from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/npmfont/ps/package/files/PressStart2P.ttf'
W,H=1080,1920
def F(s): return ImageFont.truetype(FONT,s)
def fit(lines,maxw,hi):
    for s in range(hi,30,-2):
        f=F(s); d=ImageDraw.Draw(Image.new('L',(1,1)))
        if all(d.textlength(l,font=f)+20<=maxw for l in lines): return f,s
def text_block(img,lines,cols,y,hi,stroke=8,shadow=True,maxw=940):
    f,s=fit(lines,maxw,hi); L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L)
    for i,(l,c) in enumerate(zip(lines,cols)):
        w=d.textlength(l,font=f); x=W/2-w/2; yy=y+i*int(s*1.32)
        if shadow: d.text((x+6,yy+8),l,font=f,fill=(0,0,0,170),stroke_width=stroke,stroke_fill=(0,0,0,170))
        d.text((x,yy),l,font=f,fill=c,stroke_width=stroke,stroke_fill=(12,8,20))
    img.alpha_composite(L); return y+len(lines)*int(s*1.32)
def style_A(img,lines,cols): text_block(img,lines,cols,272,68); return img          # outline only, 2 lines
def style_B(img,one,col,sub=None):                                                     # one big line (+ tiny optional sub)
    y=text_block(img,[one],[col],280,64)
    if sub: text_block(img,[sub],[(255,255,255)],y+4,40,stroke=6)
    return img
def style_C(img,lines,cols):                                                           # soft top fade, no box edges
    g=Image.new('L',(1,H),0)
    for yy in range(H): g.putpixel((0,yy),int(190*max(0,min(1,(560-yy)/330))) if yy>0 else 190)
    sh=Image.new('RGBA',(W,H),(8,6,16,255)); sh.putalpha(g.resize((W,H))); img.alpha_composite(sh)
    text_block(img,lines,cols,286,60,stroke=6,shadow=False); return img
def tag(img,txt):
    d=ImageDraw.Draw(img); f=F(34); w=d.textlength(txt,font=f)
    d.rectangle([0,1820,W,1920],fill=(0,0,0)); d.text((W/2-w/2,1852),txt,font=f,fill=(255,214,60))
    return img
def sheet(panels,out):
    s=Image.new('RGB',(len(panels)*400+40,760),(24,22,30))
    for i,p in enumerate(panels): s.paste(p.convert('RGB').resize((380,676),Image.LANCZOS),(40+i*400,40))
    s.save(out,quality=92)
Y=(255,214,60); WH=(255,255,255); BL=(110,200,255); GR=(140,230,110)
def ld(p): return Image.open(p).convert('RGBA')
# swim
c=ld('swim/clean_150.png')
sheet([tag(ld('cur_037.png'),'NOW'), tag(style_A(c.copy(),['CHOOSE YOUR','CHAMPION'],[WH,BL]),'A  OUTLINE'),
       tag(style_B(c.copy(),'PICK A SWIMMER',WH),'B  ONE LINE'), tag(style_C(c.copy(),['CHOOSE YOUR','CHAMPION'],[WH,BL]),'C  SOFT FADE')],'sheet_swim.jpg')
c=ld('riv/clean_200.png')
sheet([tag(ld('cur_056.png'),'NOW'), tag(style_A(c.copy(),['CHOOSE YOUR','CHAMPION'],[WH,Y]),'A  OUTLINE'),
       tag(style_B(c.copy(),'WHO WINS?',Y),'B  ONE LINE'), tag(style_C(c.copy(),['CHOOSE YOUR','CHAMPION'],[WH,Y]),'C  SOFT FADE')],'sheet_river.jpg')
c=ld('loot/clean_150.png')
sheet([tag(ld('cur_019.png'),'NOW'), tag(style_A(c.copy(),['LOOT','OR TREE?'],[Y,GR]),'A  OUTLINE'),
       tag(style_B(c.copy(),'LOOT OR TREE?',WH),'B  ONE LINE'), tag(style_C(c.copy(),['CHASE THE LOOT','OR PLANT THE TREE?'],[Y,GR]),'C  SOFT FADE')],'sheet_loot.jpg')
for n in ['swim','river','loot']: print(n)
