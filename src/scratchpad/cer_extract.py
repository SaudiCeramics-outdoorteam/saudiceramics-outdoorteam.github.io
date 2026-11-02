import pdfplumber,re,json,io,base64,pypdfium2 as pdfium
from PIL import Image
F='/mnt/user-data/uploads/Ceramic_catalogue__2_.pdf'
pdf=pdfplumber.open(F);doc=pdfium.PdfDocument(F)
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
def b64(im,q=80,maxw=420):
    im=im.convert('RGB');im.thumbnail((maxw,maxw),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
sections=[];prods={};pages={}
for i,pg in enumerate(pdf.pages):
    t=pg.extract_text() or ''
    if len(t)<80 and t.strip():
        l=t.strip().split('\n');sections.append((i,l[0].strip()));continue
    ws=pg.extract_words()
    codes=[w for w in ws if re.fullmatch(r'11\d{13}',w['text'])]
    if not codes:continue
    sec=[s for s in sections if s[0]<i][-1][1]
    pack={}
    for m in re.finditer(r'([\d.]+)x([\d.]+)\s*cm\s+([\d.]+)\s*cm\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.,]+)',t):
        pack[(m.group(1),m.group(2))]=dict(t=m.group(3),pcs=m.group(4),sqm=m.group(5),kg=m.group(6),bpp=m.group(7),sqmp=m.group(8),kgp=m.group(9))
    imgs=[im for im in pg.images if 40<im['x1']-im['x0']<420 and im['x0']>860]
    R=None
    for c in codes:
        code=c['text']
        if code in prods:continue
        near=[w for w in ws if abs(w['x0']-c['x0'])<40 and -22<w['top']-c['top']<20 and w is not c]
        txt=' '.join(w['text'] for w in sorted(near,key=lambda w:(round(w['top']),w['x0'])))
        desc=re.search(r'(Wall|Floor|Decor|Border|Listello|Beveled|Pool)\w*\s+tile[s]?\s*(\((\d+)\s*Faces\))?',txt,re.I)
        sz=re.search(r'([\d.]+)[xX]([\d.]+)[xX]([\d.]+)',txt)
        if not sz:continue
        W,H,T=sz.groups()
        # swatches: left of code overlapping vertically, else above in same column
        A=[im for im in imgs if im['x1']<=c['x0']+4 and im['top']<c['top']+20 and im['bottom']>c['top']-110 and c['x0']-im['x1']<500]
        if not A: A=[im for im in imgs if im['x0']>=c['x0']-8 and im['x0']<c['x0']+130 and im['bottom']<=c['top']+4 and c['top']-im['bottom']<320]
        if not A or len(codes)==1: A=[im for im in imgs if im['bottom']<=c['top']+40] or A
        A.sort(key=lambda im:(round(im['top']),im['x0']))
        if R is None: R=doc[i].render(scale=300/72).to_pil().convert('RGB')
        s=300/72;faces=[]
        for im in A[:4]:
            faces.append(b64(R.crop((int(im['x0']*s)+1,int(im['top']*s)+1,int(im['x1']*s)-1,int(im['bottom']*s)-1)),86,900))
        kind=(desc.group(1).title() if desc else ('Wall' if 'Wall' in sec else 'Floor'))
        prods[code]=dict(code=code,src='cer',name='',kind=kind,faces=desc.group(3) if desc and desc.group(3) else '',w=float(W),h=float(H),t=T,sec=sec,page=i,swatches=faces,pack=pack.get((W,H)) or pack.get((H,W)))
    pages[i]=1
P=list(prods.values())
json.dump(P,open(SP+'cer/prods.json','w'))
import collections
print(len(P),collections.Counter((p['sec'],p['kind'],p['w'],p['h'],p['t']) for p in P).most_common(40))
print(sum(1 for p in P if not p['swatches']),'no swatch',sum(1 for p in P if not p['pack']),'no pack',len(pages),'pages')
