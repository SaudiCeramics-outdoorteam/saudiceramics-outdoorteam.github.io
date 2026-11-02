import json,re
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
B=json.load(open(SP+'broch.json'))
have=set()
for f in ['acc/cat2.json','sw/san.json','wh/heat.json']:
    have|={p['code'] for p in json.load(open(SP+f))}
have|={t['code'] for t in json.load(open(SP+'tiles.json'))}
import sys;sys.path.insert(0,SP);from bathing import BATHING
have|={v['code'] for m in BATHING for v in m['variants']}
SUF={'5200':('كروم','CHROME','#d9dde1'),'8600':('فضي مطفي','BRUSHED NICKEL','#bdb6aa'),'9400':('فضي مطفي','BRUSHED SILVER','#c3c4c4'),'8800':('رمادي مطفي','MATT GREY','#6f7276'),
 '4800':('رمادي مطفي','MATT GREY','#6f7276'),'1400':('رمادي','GREY','#8a8c8e'),'2100':('أسود مطفي','MATT BLACK','#222224'),'1500':('ذهبي لامع','ENGLISH GOLD','#d6ad55'),
 '8700':('ذهبي مطفي','BRUSHED GOLD','#c4a463'),'9700':('ذهبي مطفي','BRUSHED GOLD','#c4a463'),'0200':('بيج','BEIGE','#d8c9ae'),'0100':('أبيض','WHITE','#f2f2f0'),'4700':('ذهبي مطفي','BRUSHED GOLD','#c4a463')}
def typ(c):
    for pre,(cat,nm,unit) in {'1300313':('mixer','WB Mixer','قطعة'),'1300513':('shower','Shower / Bath Mixer','قطعة'),'1304213':('shower','Shower Column','قطعة'),'13044138013':('fitting','Shower Arm','قطعة'),'13044138030':('fitting','Shower Arm','قطعة'),'13044138043':('fitting','Shower Arm','قطعة'),'13044138033':('fitting','Shower Arm','قطعة'),
      '1304413':('fitting','Shower Hose 1.5 m','قطعة'),'1301613':('fitting','Angle Valve','قطعة'),'1302315':('acc','BR Accessories Set','طقم'),'1308818':('profile','Tile Profile Trim','قطعة'),'1304615':('vanity','Wash Basin Cabinet','قطعة'),'1309413':('tile','Tile Adhesive','كيس')}.items():
        if c.startswith(pre):return cat,nm,unit
    return None
out=[];seen=set()
for b in B:
    c=b['code']
    if c in have or c in seen:continue
    t=typ(c)
    if not t:continue
    seen.add(c);cat,nm,unit=t
    col=SUF.get(c[-4:],('','',"#d9dde1"))
    series=re.sub(r'\s*(brochure|Brochure|Update|Collection|Set-2|Mixers|Tile Adhesive|PROFILE TRIM).*$','',b['title']).strip()
    ctx=b['ctx']
    spec=[]
    if cat=='vanity' and b['art']:spec.append(['رقم الموديل',b['art']])
    if cat=='vanity' and b['dims']:spec.append(['الأبعاد (مم)',b['dims']])
    m=re.search(r'(Brass|Stainless Steel ?\d*|Aluminum|Sintered Stone|Zinc Alloy)',ctx,re.I)
    if m:spec.append(['الخامة',m.group(1)])
    m=re.search(r'Warranty\s*:?\s*(\d+\s*Years?)',ctx,re.I)
    if m:spec.append(['الضمان',m.group(1)])
    if cat=='profile':
        size=re.search(r'Size:\s*(\d+\s*mm)',ctx);shape='Square Box Trim' if 'HM-B' in ctx or c[9:11] in('00','01') else ('Round Trim' if c[9:11] in('02','03','04') else 'L Angle Profile')
        nm=shape;spec+= [['المادة','ألمنيوم'],['الضمان','2 Years']]
    name=f"{series+' ' if cat in('mixer','shower','vanity','acc') and series.upper()!=nm.upper() else ''}{nm}{' · '+col[1] if col[1] else ''}".strip()
    if cat=='vanity':name=f"{series} Wash Basin · Sintered Stone";
    if cat=='tile':name='SCC Ultra Mix Tile Adhesive 20 kg'
    item=dict(cat=cat,code=c,name=name,color=col[0],hex=col[2],unit=unit,qty=1,img=b['img'],photo=b.get('photo',b['img']),sheet=b['sheet'],spec=spec,full=[])
    if cat=='vanity':
        item.update(width=80,kind='stone')
        if 'LUXO' in series:item.update(color='أبيض كرارا',hex='#ecebe7')
        else:item.update(color='بيج',hex='#d8c9ae')
    if cat=='mixer':item['tall']=c[9]=='1' or 'L-size' in ctx
    out.append(item)
json.dump(out,open(SP+'broch_items.json','w'),ensure_ascii=False)
import collections;print(len(out),collections.Counter(o['cat'] for o in out))
for o in out:print(o['cat'],o['code'],o['name'],o['color'],o['spec'])
# single-product brochures (LUXO / LAVINO): use the large native lifestyle photo
import pypdfium2 as _pd, pypdfium2.raw as _R, io as _io, base64 as _b64
from PIL import Image as _I
def _big(path):
    best=None
    for o in _pd.PdfDocument(path)[0].get_objects(filter=[_R.FPDF_PAGEOBJ_IMAGE]):
        try:w,h=o.get_px_size()
        except Exception:continue
        if not best or w*h>best[0]:best=(w*h,o)
    im=best[1].get_bitmap(render=False).to_pil().convert('RGB');im.thumbnail((1800,1800),_I.LANCZOS)
    b=_io.BytesIO();im.save(b,'JPEG',quality=86,optimize=True);return 'data:image/jpeg;base64,'+_b64.b64encode(b.getvalue()).decode()
_A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
for it in out:
    if it['cat']=='vanity':
        it['photo']=_big(_A+('a19c7254-LUXO_Brochure.pdf' if 'LUXO' in it['name'] else '6a116dff-LAVINO_Brochure.pdf'))
json.dump(out,open(SP+'broch_items.json','w'),ensure_ascii=False)
