import pdfplumber,re,json,io,base64,pypdfium2 as pdfium
from PIL import Image
F='/mnt/user-data/uploads/PORCELAIN_BOOK_final_2026_web__1_.pdf'
pdf=pdfplumber.open(F);doc=pdfium.PdfDocument(F)
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
def b64(im,q=78,maxw=900):
    im=im.convert('RGB')
    if max(im.size)>maxw: im.thumbnail((maxw,maxw),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
rc={}
def render(i,scale):
    k=(i,scale)
    if k not in rc: rc[k]=doc[i].render(scale=scale/72).to_pil().convert('RGB')
    return rc[k]
prods={};pack={}
# packaging rows
for i,pg in enumerate(pdf.pages):
    t=pg.extract_text() or ''
    for m in re.finditer(r'(\d+)\s*x\s*(\d+)\s*cm\s+([\d.]+)\s*cm\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.,]+)',t):
        k=(int(m.group(1)),int(m.group(2)),m.group(3));pack[k]=dict(pcs=m.group(4),sqm=m.group(5),kg=m.group(6),bpp=m.group(7),sqmp=m.group(8),kgp=m.group(9))
# index pages
for i,pg in enumerate(pdf.pages):
    t=pg.extract_text() or ''
    m=re.search(r'SURFACE\s+(\d+)\s*X\s*(\d+)',t);th=re.search(r'THICKNESS\s+([\d.]+)\s*CM',t)
    if not(m and th and len(set(re.findall(r'111\d{12}',t)))>=2):continue
    W,H=int(m.group(1)),int(m.group(2));T=th.group(1)
    ws=pg.extract_words(keep_blank_chars=True,x_tolerance=2)
    imgs=[im for im in pg.images if im['x1']-im['x0']>40]
    for w in ws:
        mm=re.match(r'(.+?)\s*:\s*(111\d{12})\s*(\|\s*[LR])?',w['text'])
        if not mm:continue
        name=mm.group(1).strip();code=mm.group(2);side=(mm.group(3) or '').replace('|','').strip()
        below=[x for x in ws if abs(x['x0']-w['x0'])<4 and 0<x['top']-w['top']<30]
        fin=below[0]['text'].strip() if below else '';faces=''
        for x in below:
            f=re.search(r'Faces\s*:\s*(.+)',x['text'])
            if f:faces=f.group(1).strip()
        cand=[im for im in imgs if im['bottom']<=w['top']+3 and abs(im['x0']-w['x0'])<12]
        cand.sort(key=lambda im:w['top']-im['bottom'])
        if not cand:continue
        im=cand[0];s=300/72;R=render(i,300)
        sw=R.crop((int(im['x0']*s)+1,int(im['top']*s)+1,int(im['x1']*s)-1,int(im['bottom']*s)-1))
        prods[code]=dict(code=code,name=(name+(' '+side if side else '')).strip(),finish=fin,faces=faces,w=W,h=H,t=T,swatch=b64(sw,86,1100),idx=i)
# product pages: application/category/edge + lifestyle photo + datasheet
for i,pg in enumerate(pdf.pages):
    t=pg.extract_text() or ''
    for m in re.finditer(r'SURFACE CODE\s*:\s*(111\d{12})',t):
        code=m.group(1)
        row=re.search(r'No\. of Faces\s*\n?(.+?)\n',t[m.end():]+'\n')
        app=''
        if row:
            r=row.group(1)
            a=re.search(r'(Floor & Wall|Floor&Wall|Wall|Floor|Outdoor|Facade|Façade)',r)
            app=a.group(1) if a else ''
        p=prods.setdefault(code,dict(code=code,name='',finish='',faces='',w=0,h=0,t='',swatch=''))
        if 'app' in p:continue
        p['app']=app;p['page']=i
        if row:p['row']=row.group(1)
# photos and sheets
for code,p in prods.items():
    if 'page' not in p:continue
    i=p['page'];R=render(i,110)
    pg=pdf.pages[i];big=sorted([im for im in pg.images],key=lambda im:-(im['x1']-im['x0'])*(im['bottom']-im['top']))
    s=110/72
    if big:
        im=big[0];p['photo']=b64(R.crop((max(0,int(im['x0']*s)),max(0,int(im['top']*s)),int(min(pg.width,im['x1'])*s),int(min(pg.height,im['bottom'])*s))),76,900)
    p['sheet']=b64(R,70,1300)
json.dump(list(prods.values()),open(SP+'por/prods.json','w'))
print(len(prods),'products');import collections
print(collections.Counter((p['w'],p['h'],p['t']) for p in prods.values()))
print(collections.Counter(p.get('app','?') for p in prods.values()))
print(pack)
for p in list(prods.values())[:3]+[p for p in prods.values() if not p['swatch']][:5]: print(p['code'],p['name'],p['finish'],p['faces'],p.get('app'),p.get('row','')[:80])
# ---- fill facade (40x80x2) and outdoor (60x60x2) products
for code,p in prods.items():
    if p['w'] or 'page' not in p:continue
    i=p['page'];pg=pdf.pages[i];t=pg.extract_text()
    caps=[l.strip() for l in t.split('\n') if re.fullmatch(r'[A-Z][A-Z \-]{3,}',l.strip()) and 'TECHNICAL' not in l]
    p['name']=caps[0].title() if caps else code
    sz=re.search(r'(\d{2,3})\s*[Xx×]\s*(\d{2,3})',t);p['w'],p['h']=int(sz.group(1)),int(sz.group(2));p['t']='2.0'
    p['app']='Facade' if p['w']==40 else 'Outdoor'
    fin=re.search(r'Porcelain Tiles\s+(\S+)',t);p['finish']=fin.group(1) if fin else 'Matt'
    fc=re.search(r'Outdoor\s+(\d+)|Facade\s+(\d+)',t);p['faces']=(fc.group(1) or fc.group(2)) if fc else ''
    sw=[im for im in pg.images if im['top']>680 and im['x1']-im['x0']>90]
    if sw:
        im=sw[0];s=300/72;R=render(i,300);p['swatch']=b64(R.crop((int(im['x0']*s)+1,int(im['top']*s)+1,int(im['x1']*s)-1,int(im['bottom']*s)-1)),86,1100)
for p in prods.values():
    if not p.get('app'):p['app']='Floor & Wall'
    k=(p['w'],p['h'],p['t']);p['pack']=pack.get(k) or pack.get((p['h'],p['w'],p['t']))
json.dump(list(prods.values()),open(SP+'por/prods.json','w'))
import collections
print(collections.Counter((p['w'],p['h'],p['t'],p['app']) for p in prods.values()))
print([p['name'] for p in prods.values() if p['app'] in('Facade','Outdoor')])
print(sum(1 for p in prods.values() if not p['swatch']),'no swatch',sum(1 for p in prods.values() if not p['pack']),'no pack')
