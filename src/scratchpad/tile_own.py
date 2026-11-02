# Tiles that share one catalogue page get their own photo: pool tiles -> laid-out pattern of that exact tile;
# other series pages -> the series photo with that tile's own swatch + name inset, so no two designs show the same image.
import json,io,base64,collections,os
from PIL import Image,ImageDraw,ImageFilter,ImageFont
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';D='/home/claude/villa/data/'
T=json.load(open(SP+'tiles.json'));c=collections.Counter((t['src'],t['page']) for t in T)
shared={k for k,v in c.items() if v>1};swc={}
def sw(t):
    if t['sw'] not in swc:swc[t['sw']]=json.load(open(D+'sw_'+t['sw']+'.json'))
    v=swc[t['sw']].get(t['code']);v=v[0] if isinstance(v,list) else v
    return Image.open(io.BytesIO(base64.b64decode(v.split(',',1)[1]))).convert('RGB') if v else None
try:F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
except Exception:F=ImageFont.load_default()
used=set();n=0
import glob
BASE={}
for t in T:
    k=(t['src'],t['page']);bf=SP+'tpbase/%s_%s.jpg'%k
    if os.path.exists(bf):BASE[k]=bf
for t in T:
    k=(t['src'],t['page'])
    if k not in shared:t.pop('tpf',None);continue
    s=sw(t)
    if s is None:continue
    if t['page']==171 and t['src']=='cer':   # pool: lay the tile out as a wall, 12x24.5 with grout
        W,H=1600,1100;img=Image.new('RGB',(W,H),(232,236,238));tw=150;th=int(tw*24.5/12);g=5
        piece=s.resize((tw,th),Image.LANCZOS)
        for yy in range(-th//2,H,th+g):
            for xx in range(-(tw//3),W,tw+g):img.paste(piece,(xx,yy))
        sh=Image.new('L',(W,H),0);ImageDraw.Draw(sh).rectangle((0,0,W,H),fill=0)
        light=Image.linear_gradient('L').resize((W,H)).rotate(90);img=Image.composite(img,Image.blend(img,Image.new('RGB',(W,H),(255,255,255)),.12),light.point(lambda v:255-v//3))
    else:
        base=Image.open(BASE.get(k) or D+'tp/%s_%s.jpg'%k).convert('RGB');img=base.copy();W,H=img.size
        iw=int(W*.3);ih=int(iw*s.height/s.width) if s.width else iw;ih=min(ih,int(H*.45));iw=int(ih*s.width/s.height)
        card=Image.new('RGB',(iw+24,ih+24+46),'white');card.paste(s.resize((iw,ih),Image.LANCZOS),(12,12))
        ImageDraw.Draw(card).text((14,ih+18),(t['name'].replace('Ceramic Wall Tile ','').replace('Ceramic Floor Tile ','')[:18]+'  '+t['code']),fill=(30,30,30),font=F)
        shadow=Image.new('RGBA',(card.width+30,card.height+30),(0,0,0,0));ImageDraw.Draw(shadow).rectangle((15,18,card.width+12,card.height+15),fill=(0,0,0,90));shadow=shadow.filter(ImageFilter.GaussianBlur(8))
        x,y=int(W*.03),H-card.height-int(H*.04);img.paste(shadow,(x-15,y-12),shadow);img.paste(card,(x,y))
    img.save(D+'tp/t_%s.jpg'%t['code'],quality=84,optimize=True,progressive=True);t['tpf']='t_'+t['code'];n+=1
for k in shared:
    if all(t.get('tpf') for t in T if (t['src'],t['page'])==k):
        f=D+'tp/%s_%s.jpg'%k
        if os.path.exists(f):os.remove(f);used.add(k)
json.dump(T,open(SP+'tiles.json','w'),ensure_ascii=False);json.dump(T,open(D+'tiles.json','w'),ensure_ascii=False)
print(n,'own photos;',len(used),'shared base photos removed;',len(os.listdir(D+'tp')),'tp files')
