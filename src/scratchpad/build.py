import json,sys,re,hashlib,base64,os
sp='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
sys.path.insert(0,sp);from bathing import BATHING
s=open('/home/claude/villa-src.html').read()
from enhance import enhance
_DSX=json.load(open('/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/extra/ds_existing.json'))
def attach(items,ewh=False):
    # official datasheets the user supplied for products already in the catalogue
    for it in items:
        if it.get('code') in _DSX['code']:it['ds']=_DSX['code'][it['code']]
        if ewh and it.get('cat')=='heater' and not it.get('ds'):it['ds']=_DSX['ewh']
    return items
tex=json.load(open(sp+'pdf/tex3.json'));cat=enhance(json.load(open(sp+'acc/cat2.json')))
meta=[('111157542512016','NAJDI DESIGN'),('111157492512016','SANDY DESERT DARK'),('111156952512016','SANDY DESERT BEIGE'),('111157102512016','ROMAN TRAVERTINE'),('111147342512016','TRAVERTINO CREAM'),('111138692512016','LIMESTONE LIGHT')]
prods=[{'code':c,'name':n,'faces':tex[c]['n'],'sqmBox':0.72,'kgBox':35.28,'boxPallet':32,'atlas':tex[c]['atlas'],'thumb':tex[c]['thumb'],'photo':tex[c]['photo']} for c,n in meta]
J=lambda o:json.dumps(o,ensure_ascii=False)
s=s.replace('/*__BATHING__*/',J(BATHING)).replace('/*__PRODUCTS__*/',J(prods)).replace('/*__CAT__*/',J(cat))
s=s.replace('/*__BRO__*/',J(enhance(json.load(open(sp+'broch_items.json'))))).replace('/*__STAIRS__*/',J(json.load(open(sp+'stairs.json'))))
SHX=json.load(open(sp+'broch_sheets.json'))
try:
    import bathing as _bt;SHX['bMALAGA']=_bt.MALAGA_SHEET
except Exception:pass
s=s.replace('/*__SAN__*/',J(enhance(attach(json.load(open(sp+'sw/san.json'))+json.load(open(sp+'extra/new_items.json')))))).replace('/*__HEAT__*/',J(enhance(json.load(open(sp+'wh/heat_new.json'))+attach(json.load(open(sp+'wh/heat.json')),ewh=True)))).replace('/*__SHEETS__*/',J({**json.load(open(sp+'sheets.json')),**SHX}))
s=s.replace('هنا يختار العميل بلاط الواجهات ويشوف شكل البيت يتغير مباشرة.','اختر بلاطة وشوف الواجهة تتغير مباشرة.')
# big images -> data/hi_N.json chunks, referenced as "hi:<hash>"
out='/home/claude/villa'; os.makedirs(out+'/img',exist_ok=True);os.makedirs(out+'/data',exist_ok=True)
for f in os.listdir(out+'/img'): os.remove(out+'/img/'+f)
for f in os.listdir(out+'/data'):
    if f.startswith('hi_'): os.remove(out+'/data/'+f)
os.system(f'cp {sp}logo.png {out}/img/logo.png')
HI={};order=[]
def sub(m):
    d=m.group(0)
    if len(d)<30000: return d
    h=hashlib.md5(d.encode()).hexdigest()[:12]
    if h not in HI: HI[h]=d;order.append(h)
    return 'hi:'+h
s2=re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+',sub,s)
himap={};chunk={};size=0;n=0
for h in order:
    chunk[h]=HI[h];size+=len(HI[h]);himap[h]=f'hi_{n}'
    if size>1_500_000:
        json.dump(chunk,open(f'{out}/data/hi_{n}.json','w'));chunk={};size=0;n+=1
if chunk: json.dump(chunk,open(f'{out}/data/hi_{n}.json','w'))
s2=s2.replace('/*__HIMAP__*/',json.dumps(himap))
print(len(order),'hi images in',n+1,'chunks',round(sum(len(v) for v in HI.values())/1048576,1),'MB')
TRACK=(open(sp+'track_url.txt').read().strip() if os.path.exists(sp+'track_url.txt') else '')
s2=s2.replace('/*__TRACK_URL__*/','')   # the claude.ai artifact never posts out
open(out+'/index.html','w').write(s2)
# public website copy (GitHub Pages / any static host): same page as a full document, with the Google Sheet log switched on
pub='/home/claude/site_public';os.system(f'rm -rf {pub} && mkdir -p {pub} && cp -r {out}/img {out}/data {pub}/ && cp {sp}share.jpg {pub}/img/share.jpg && cp -r {sp}docs {pub}/docs')
open(pub+'/index.html','w').write('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>شطّب بيتك وأنت مرتاح مع الخزف السعودي · فريق المبيعات الخارجية</title><meta name="description" content="اختر بلاطك وأدواتك الصحية وسخاناتك على بيتك ثلاثي الأبعاد، واحصل على كتالوج PDF بالكميات — فريق المبيعات الخارجية Outdoor Team"><meta property="og:type" content="website"><meta property="og:site_name" content="الخزف السعودي"><meta property="og:title" content="شطّب بيتك وأنت مرتاح مع الخزف السعودي · فريق المبيعات الخارجية"><meta property="og:description" content="اختر بلاطك وأدواتك الصحية وسخاناتك على بيتك ثلاثي الأبعاد، واحصل على كتالوج PDF بالكميات — فريق المبيعات الخارجية Outdoor Team"><meta property="og:url" content="https://talha1998-sc.github.io/saudi-ceramics/"><meta property="og:image" content="https://talha1998-sc.github.io/saudi-ceramics/img/share.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="شطّب بيتك وأنت مرتاح مع الخزف السعودي · فريق المبيعات الخارجية"><meta name="twitter:image" content="https://talha1998-sc.github.io/saudi-ceramics/img/share.jpg"><link rel="icon" href="img/logo.png"></head><body>'+re.sub(r'<title>[^<]*</title>','',s2).replace('const TRACK_URL="";','const TRACK_URL="'+TRACK+'";',1)+'</body></html>')
open(pub+'/.nojekyll','w').write('')
print(round(len(s2)/1024),'KB html')
t=s2
for a,b in [('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','../t/three-0.128.0/package/build/three.min.js'),('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js','../t/three-0.128.0/package/examples/js/controls/OrbitControls.js'),('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js','../t/jspdf-2.5.1/package/dist/jspdf.umd.min.js'),('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js','../t/html2canvas-1.4.1/package/dist/html2canvas.min.js')]: t=t.replace(a,b)
os.makedirs(sp+'site',exist_ok=True)
os.system(f'rm -rf {sp}site/img {sp}site/data && cp -r {out}/img {sp}site/img && cp -r {out}/data {sp}site/data')
open(sp+'site/test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+t+'</body></html>')
