import json,io,base64,re,pdfplumber,pypdfium2 as pdfium
from PIL import Image
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
def b64(im,q=80,maxw=1200):
    im=im.convert('RGB');
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
SHEETS={}
# ---------- facade tiles: right half of catalog page ----------
for code in ['111157542512016','111157492512016','111157102512016','111156952512016','111147342512016','111138692512016']:
    im=Image.open(SP+f'pdf/p300_{code}.png');W,H=im.size
    SHEETS['t'+code]=b64(im.crop((W//2,0,W,H)),80,1800)
# ---------- resale accessories: card crops + full text ----------
cat=json.load(open(SP+'acc/cat.json'));items={i['code']:i for i in json.load(open(SP+'acc/items.json'))}
pdf=pdfplumber.open('/mnt/user-data/uploads/Resale_Catalogue__1_.pdf');doc=pdfium.PdfDocument('/mnt/user-data/uploads/Resale_Catalogue__1_.pdf')
cache={}
KEYS=r'(Core material|Material|Handle|Cartridge|Aerator|Finishing|Flexible Hose|Hose|Color|Colour|Warranty|Dimensions?|Size|Fitting|Shower kits|Shower Kits|Diverter|Shower Head|Shower handset|Shower hose|Riser Rail|Function|Capacity|Weight|Thickness|Length|Body|Spray|Cabinet|Main Cabinet|Basin|Mirror|Light|Power|Voltage|Model)'
for p in cat:
    it=items[p['code']];pg=pdf.pages[it['page']]
    w=[x for x in pg.extract_words() if x['text']==p['code']][0]
    x0,top,x1,bot=it['img']
    L,R=x0-10,x1+10
    below=[x for x in pg.extract_words() if w['bottom']+1<x['top']<w['bottom']+125 and x0-6<=x['x0']<(x0+x1)/2+12]
    lines={}
    for x in below: lines.setdefault(round(x['top']/3),[]).append(x)
    t=' '.join(' '.join(y['text'] for y in sorted(v,key=lambda y:y['x0'])) for k,v in sorted(lines.items()))
    t=re.sub(r'(\w)- (\w)',r'\1\2',t);t=re.sub(r'\s+',' ',t).strip()
    parts=re.split(KEYS+r'\s*:',t)
    rows=[]
    if len(parts)>1:
        for i in range(1,len(parts)-1,2):
            v=parts[i+1].strip(' ,;')
            if v: rows.append([parts[i],v[:120]])
    p['full']=rows
    if it['page'] not in cache: cache[it['page']]=doc[it['page']].render(scale=300/72).to_pil()
    s=300/72;im=cache[it['page']]
    half=0 if (x0+x1)/2<pg.width/2 else 1;Wpx=im.size[0]
    SHEETS['r'+p['code']]=b64(im.crop((half*Wpx//2,0,(half+1)*Wpx//2,im.size[1])),84,2000)
    p['sheet']='r'+p['code']
    p['photo']=b64(im.crop((int(x0*s),int(top*s),int(x1*s),int(bot*s))),86,1400)
json.dump(cat,open(SP+'acc/cat2.json','w'),ensure_ascii=False)
# ---------- tubs/trays: spec half pages ----------
tdoc=pdfium.PdfDocument('/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/03b692e7-Bathtub__Shower_Tray_2022.pdf')
def tp(n):return tdoc[n-1].render(scale=300/72).to_pil()
for mid,n in [('ROMA',3),('ALASKA',4),('SALWA',5),('VERONA',6)]:
    im=tp(n);W,H=im.size;SHEETS['b'+mid]=b64(im.crop((0,0,W//2,H)),80,1800)
for mid,n,h in [('RIVIERA',7,0),('LARA',7,1),('ATLANTA',8,0),('TOLEDO',8,1),('PANAMA',9,1)]:
    im=tp(n);W,H=im.size;x=0 if h==0 else W//2;SHEETS['b'+mid]=b64(im.crop((x,int(H*.32),x+W//2,H)),80,1800)
# ---------- sanitary ware ----------
sdoc=pdfium.PdfDocument('/mnt/user-data/uploads/Sanitary_Ware_General_Catalog__3_.pdf');spdf=pdfplumber.open('/mnt/user-data/uploads/Sanitary_Ware_General_Catalog__3_.pdf')
spc={}
def sp(i):
    if i not in spc: spc[i]=sdoc[i].render(scale=300/72).to_pil().convert('RGB')
    return spc[i]
def photo(i,pos):
    """crop the exact embedded photo on the left half of the spread (no neighbouring slivers)"""
    im=sp(i);W,H=im.size;pg=spdf.pages[i];k=W/pg.width
    imgs=[b for b in pg.images if b['x0']<pg.width*.5 and (b['x1']-b['x0'])*(b['bottom']-b['top'])>pg.width*pg.height*.02]
    imgs=[dict(x0=max(0,b['x0']),top=max(0,b['top']),x1=min(pg.width*.5,b['x1']),bottom=min(pg.height,b['bottom'])) for b in imgs]
    if not imgs:
        X0,X1,Y0,Y1=int(W*.02),int(W*.475),int(H*.075),int(H*.935);return im.crop((X0,Y0,X1,Y1))
    imgs.sort(key=lambda b:(round(b['top']/40),b['x0']))
    if pos=='full':b=max(imgs,key=lambda b:(b['x1']-b['x0'])*(b['bottom']-b['top']))
    else:
        idx={'top':0,'bot':1,'tl':0,'tr':1,'bl':2,'br':3}[pos]
        if pos in('tl','tr','bl','br'):
            rows=sorted(imgs,key=lambda b:b['top']);r=[sorted(rows[:2],key=lambda b:b['x0']),sorted(rows[2:4],key=lambda b:b['x0'])];flat=r[0]+r[1]
            b=flat[min(idx,len(flat)-1)]
        else:
            col=sorted(imgs,key=lambda b:b['top']);b=col[min(idx,len(col)-1)]
    nat=native(sdoc,i,b,pg.height)
    if nat is not None and nat.width>=(b['x1']-b['x0'])*k*.6:return nat
    return im.crop((int(b['x0']*k)+2,int(b['top']*k)+2,int(b['x1']*k)-2,int(b['bottom']*k)-2))

import pypdfium2.raw as PR
def native(doc,i,b,pgh):
    """native-resolution bitmap of the embedded image under bbox b (pdfplumber coords), cropped to its visible part"""
    best=None;bi=0
    for o in doc[i].get_objects(filter=[PR.FPDF_PAGEOBJ_IMAGE]):
        l,bo,r,t=o.get_bounds();ox0,oy0,ox1,oy1=l,pgh-t,r,pgh-bo
        ix=max(0,min(ox1,b['x1'])-max(ox0,b['x0']));iy=max(0,min(oy1,b['bottom'])-max(oy0,b['top']))
        if ix*iy>bi:bi=ix*iy;best=(o,ox0,oy0,ox1,oy1)
    if not best:return None
    o,ox0,oy0,ox1,oy1=best
    try:im=o.get_bitmap(render=False).to_pil().convert('RGB')
    except Exception:return None
    W,H=im.size;fx=lambda x:(x-ox0)/(ox1-ox0)*W;fy=lambda y:(y-oy0)/(oy1-oy0)*H
    c=(int(max(0,fx(b['x0']))),int(max(0,fy(b['top']))),int(min(W,fx(b['x1']))),int(min(H,fy(b['bottom']))))
    if c[2]-c[0]<50 or c[3]-c[1]<50:return None
    return im.crop(c)
SAN=[]
def san(cat,code,name,color,hexc,page,pos,kind,extra=None):
    ph=photo(page,pos);th=ph.copy();th.thumbnail((420,420))
    sid='s%d'%page
    if sid not in SHEETS:
        im=sp(page);W,H=im.size;SHEETS[sid]=b64(im.crop((W//2,0,W,H)),80,1800)
    # parse packing row text
    t=spdf.pages[page].extract_text();row=''
    for l in t.split('\n'):
        if code in l: row=l;break
    m=re.search(r'(\d{3,4}\s*[Xx]\s*\d{3,4})\s+([\d.]+)\s+(\d+)',row)
    spec=[]
    if m: spec+=[["الأبعاد (مم)",m.group(1).replace('X','×').replace('x','×')],["الوزن القياسي (كغ)",m.group(2)],["عدد بالكرتون",m.group(3)]]
    d=dict(cat=cat,code=code,name=name,color=color,hex=hexc,unit='قطعة',qty=1,kind=kind,img=b64(th,84,420),photo=b64(ph,86,1700),sheet=sid,spec=spec,full=[])
    if extra:d.update(extra)
    SAN.append(d)
W_='#f4f4f2'
san('toilet','121560251010010','Dream Water Closet One Piece · Drain 25 cm','أبيض',W_,11,'top','floor')
san('toilet','121550253010010','Sky Water Closet One Piece · Drain 25 cm','أبيض',W_,11,'bot','floor')
san('toilet','121210251010010','Paris Water Closet One Piece · Drain 25 cm','أبيض',W_,12,'full','floor')
san('toilet','121210252010010','Paris Water Closet One Piece · Drain 30 cm','أبيض',W_,12,'full','floor')
san('toilet','121200248010010','CADY Water Closet One Piece · Drain 25 cm','أبيض',W_,13,'full','floor')
san('toilet','121350243200020','Model-A WC Wall Hung · Off White','أبيض مطفي فاتح',W_,21,'top','wall')
san('toilet','121350243400020','Model-A WC Wall Hung · Matt White','أبيض مطفي','#efefec',21,'bot','wall')
san('toilet','121350243160020','Model-A WC Wall Hung · Matt Grey','رمادي مطفي','#8a8b8a',22,'top','wall')
san('toilet','121350243220020','Model-A WC Wall Hung · Matt Black','أسود مطفي','#2a2a2b',22,'bot','wall')
san('toilet','121520267010010','MAGIC Water Closet One Piece · Drain 25 cm','أبيض',W_,23,'full','floor')
san('toilet','121520267220010','MAGIC Water Closet One Piece · Matt Black','أسود مطفي','#2a2a2b',24,'full','floor')
san('toilet','121530267010010','FANCY Water Closet One Piece · Drain 25 cm','أبيض',W_,25,'full','floor')
san('toilet','121650267010010','Napoli 1 pc WC (25 cm)','أبيض',W_,37,'top','floor')
san('toilet','121710266010010','Florence 1 pc WC (25 cm)','أبيض',W_,37,'bot','floor')
san('toilet','121470265010020','VERDI Water Closet Wall Hung','أبيض',W_,36,'top','wall')
san('toilet','121570265010020','INFINITY Water Closet Wall Hung','أبيض',W_,36,'bot','wall')
san('basin','121350122200030','Model-A Washbasin Wall Hung · Off White','أبيض مطفي فاتح',W_,21,'top','wallbasin',{'w':.545})
san('basin','121350122400030','Model-A Washbasin Wall Hung · Matt White','أبيض مطفي','#efefec',21,'bot','wallbasin',{'w':.545})
san('basin','121350122160030','Model-A Washbasin Wall Hung · Matt Grey','رمادي مطفي','#8a8b8a',22,'top','wallbasin',{'w':.545})
san('basin','121350122220030','Model-A Washbasin Wall Hung · Matt Black','أسود مطفي','#2a2a2b',22,'bot','wallbasin',{'w':.545})
san('basin','121510133010030','SPARK Washbasin Floor Standing 55 cm','أبيض',W_,23,'full','pedestal',{'w':.555})
san('basin','121510133220030','SPARK Washbasin Floor Standing · Matt Black','أسود مطفي','#2a2a2b',24,'full','pedestal',{'w':.555})
san('basin','121500131010030','CRYSTAL Washbasin Wall Hung 40 cm','أبيض',W_,25,'full','wallbasin',{'w':.405})
san('basin','121230122200030','TYPE-A Washbasin Wall Hung 50 cm · White','أبيض',W_,29,'tl','wallbasin',{'w':.5})
san('basin','121230122160030','TYPE-A Washbasin Wall Hung 50 cm · Matt Grey','رمادي مطفي','#8a8b8a',29,'tr','wallbasin',{'w':.5})
san('basin','121230122220030','TYPE-A Washbasin Wall Hung 50 cm · Matt Black','أسود مطفي','#2a2a2b',29,'bl','wallbasin',{'w':.5})
san('basin','121230122400030','TYPE-A Washbasin Wall Hung 50 cm · Matt White','أبيض مطفي','#efefec',29,'br','wallbasin',{'w':.5})
san('basin','121490131010020','MIRAGE Washbasin Wall Hung 49 cm · White','أبيض',W_,28,'tl','wallbasin',{'w':.49})
san('basin','121490131160020','MIRAGE Washbasin Wall Hung 49 cm · Matt Grey','رمادي مطفي','#8a8b8a',28,'tr','wallbasin',{'w':.49})
san('basin','121490131220020','MIRAGE Washbasin Wall Hung 49 cm · Matt Black','أسود مطفي','#2a2a2b',28,'bl','wallbasin',{'w':.49})
json.dump(SAN,open(SP+'sw/san.json','w'),ensure_ascii=False)
for s in SAN[:3]+SAN[-3:]: print(s['code'],s['spec'])
# ---------- water heaters ----------
wpdf=pdfplumber.open('/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/c46932b5-Water_Heater_Catalogue_2.pdf')
wdoc=pdfium.PdfDocument('/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/c46932b5-Water_Heater_Catalogue_2.pdf')
def wp(n):return wdoc[n-1].render(scale=300/72).to_pil().convert('RGB')
HEAT=[]
def heat(line,title,n,sheetn,models,kind,desc):
    im=wp(n);W,H=im.size;wpg=wpdf.pages[n-1];k=W/wpg.width
    bx=[b for b in wpg.images if b['x0']<wpg.width*.5];bx=max(bx,key=lambda b:(b['x1']-b['x0'])*(b['bottom']-b['top'])) if bx else None
    nat=native(wdoc,n-1,dict(x0=max(0,bx['x0']),top=max(0,bx['top']),x1=min(wpg.width*.5,bx['x1']),bottom=min(wpg.height,bx['bottom'])),wpg.height) if bx else None
    ph=nat if nat is not None else im.crop((int(max(0,bx['x0'])*k)+2,int(max(0,bx['top'])*k)+2,int(min(wpg.width*.5,bx['x1'])*k)-2,int(min(wpg.height,bx['bottom'])*k)-2)) if bx else im.crop((int(W*.02),int(H*.1),int(W*.49),int(H*.94)));th=ph.copy();th.thumbnail((420,420))
    sid='w%d'%sheetn
    if sid not in SHEETS:
        s=wp(sheetn);SHEETS[sid]=b64(s.crop((s.width//2,0,s.width,s.height)),80,1800)
    for cap,model in models:
        HEAT.append(dict(cat='heater',code=model,name=f'{title} · {model}',color='',hex='#ffffff',unit='قطعة',qty=1,kind=kind,cap=cap,line=line,img=b64(th,84,420),photo=b64(ph,86,1700),sheet=sid,
          spec=[["الموديل",model],["السعة",f"{cap} لتر"],["النوع",desc]],full=[]))
heat('quad','QUAD Water Heater',10,10,[(10,'EWH-H10AS'),(15,'EWH-H15AS')],'quad','سخان صغير مدمج (كواد)')
heat('sink','Above / Under Sink Water Heater',11,11,[(10,'EWH-V10-AS/US'),(15,'EWH-V15-AS/US')],'sink','فوق أو تحت المغسلة')
heat('slim','SLIM Water Heater',12,12,[(30,'EWH-V30SL')],'slim','عمودي نحيل')
heat('fat','30 Liters Vertical Water Heater',13,13,[(30,'EWH-V30')],'vert','عمودي 30 لتر')
heat('vstd','Vertical Standard Water Heater',14,14,[(50,'EWH-V50'),(80,'EWH-V80'),(100,'EWH-V100'),(150,'EWH-V150')],'vert','عمودي - النطاق الموحد')
heat('smart','Vertical Smart Wi-Fi Water Heater',15,16,[(50,'EWH-V50EL')],'vert','عمودي ذكي Wi-Fi')
heat('horiz','Horizontal Water Heater',17,17,[(50,'EWH-H50'),(80,'EWH-H80'),(100,'EWH-H100'),(150,'EWH-H150')],'horiz','أفقي')
json.dump(HEAT,open(SP+'wh/heat.json','w'),ensure_ascii=False)
json.dump(SHEETS,open(SP+'sheets.json','w'))
print(len(SAN),len(HEAT),len(SHEETS),sum(len(v) for v in SHEETS.values())//1024,'KB sheets')
