import json,io,base64,os,re,pypdfium2 as pdfium
from PIL import Image
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
OUT='/home/claude/villa/data';os.makedirs(OUT,exist_ok=True)
def small(d,px=140,q=78):
    im=Image.open(io.BytesIO(base64.b64decode(d.split(',',1)[1]))).convert('RGB');im.thumbnail((px,px),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def fmtn(x):return ('%g'%x)
por=json.load(open(SP+'por/prods.json'));cer=json.load(open(SP+'cer/prods.json'))
existing={'111157542512016','111157492512016','111157102512016','111156952512016','111147342512016','111138692512016'}
T=[];SW={};seen=set(existing)
for p in por:
    if p['code'] in seen or not p.get('page'):continue
    seen.add(p['code'])
    app=p.get('app','')
    z={'Facade':['facade'],'Outdoor':['court','roof'],'Floor':['floor'],'Floor & Wall':['floor','wall']}.get(app,['floor'])
    k=p['pack'] or {}
    T.append(dict(code=p['code'],src='por',name=p['name'].replace('Statuarioe','Statuario'),cat='بورسلان',w=p['w'],h=p['h'],t=p['t'],finish=p['finish'],faces=p['faces'],app=app,zones=z,page=p['page'],
        pack=k,thumb=small(p['swatch'])))
    SW[p['code']]=[p['swatch']]
KIND={'Wall':'بلاط جدران','Floor':'بلاط أرضيات','Beveled':'بلاط مشطوف','Pool':'بلاط مسابح'}
for p in cer:
    if p['code'] in seen:continue
    seen.add(p['code'])
    sec=p['sec'].lower();t=float(p['t'])
    if 'pool' in sec: z=['pool'];app='Swimming Pool'
    elif 'roof' in sec: z=['roof'];app='Roof'
    elif 'bevel' in sec: z=['wall'];app='Wall'
    elif p['kind']=='Wall': z=['wall'];app='Wall'
    elif t>=1.2: z=['court','roof'];app='Outdoor Floor'
    else: z=['floor'];app='Floor'
    nm=f"Ceramic {'Wall' if 'wall' in z else 'Floor'} Tile {fmtn(p['w'])}×{fmtn(p['h'])}"
    T.append(dict(code=p['code'],src='cer',name=nm,cat='سيراميك',w=p['w'],h=p['h'],t=p['t'],finish='Glazed',faces=p['faces'],app=app,zones=z,page=p['page'],pack=p['pack'] or {},thumb=small(p['swatches'][0])))
    SW[p['code']]=p['swatches']
# swatch chunks by src+size+thickness
groups={}
for t in T: groups.setdefault(f"{t['src']}_{fmtn(t['w'])}x{fmtn(t['h'])}_{t['t']}".replace('.','-'),[]).append(t)
for g,L in groups.items():
    json.dump({t['code']:SW[t['code']] for t in L},open(f'{OUT}/sw_{g}.json','w'))
    for t in L:t['sw']=g
# page sheets, chunked
def pages(src,F,width):
    doc=pdfium.PdfDocument(F);ids=sorted({t['page'] for t in T if t['src']==src});chunk={};n=0
    for k,i in enumerate(ids):
        pg=doc[i];im=pg.render(scale=width/pg.get_size()[0]).to_pil().convert('RGB')
        b=io.BytesIO();im.save(b,'JPEG',quality=78,optimize=True);chunk[str(i)]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
        if len(chunk)==10 or k==len(ids)-1:
            json.dump(chunk,open(f'{OUT}/pg_{src}_{n}.json','w'))
            for t in T:
                if t['src']==src and str(t['page']) in chunk:t['pg']=f'pg_{src}_{n}'
            chunk={};n+=1
pages('por','/mnt/user-data/uploads/PORCELAIN_BOOK_final_2026_web__1_.pdf',2000)
pages('cer','/mnt/user-data/uploads/Ceramic_catalogue__2_.pdf',2000)
json.dump(T,open(SP+'tiles.json','w'),ensure_ascii=False)
import collections
print(len(T),collections.Counter(z for t in T for z in t['zones']))
tot=0
for f in sorted(os.listdir(OUT)):
    s=os.path.getsize(f'{OUT}/{f}');tot+=s
print(len(os.listdir(OUT)),'files',round(tot/1048576,1),'MB; max',round(max(os.path.getsize(f'{OUT}/{f}') for f in os.listdir(OUT))/1048576,1),'MB; tiles.json',round(os.path.getsize(SP+'tiles.json')/1048576,2),'MB')
