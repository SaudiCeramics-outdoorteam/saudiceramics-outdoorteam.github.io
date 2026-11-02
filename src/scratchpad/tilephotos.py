import json,io,base64,os,pypdfium2 as pdfium
from PIL import Image
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';OUT='/home/claude/villa/data'
T=json.load(open(SP+'tiles.json'))
for f in os.listdir(OUT):
    if f.startswith('tp_'):os.remove(OUT+'/'+f)
for src,F,dpi in [('por','/mnt/user-data/uploads/PORCELAIN_BOOK_final_2026_web__1_.pdf',210),('cer','/mnt/user-data/uploads/Ceramic_catalogue__2_.pdf',160)]:
    doc=pdfium.PdfDocument(F);ids=sorted({t['page'] for t in T if t['src']==src});chunk={};n=0;size=0
    for k,i in enumerate(ids):
        pg=doc[i];w,h=pg.get_size();im=pg.render(scale=dpi/72,crop=(0,0,w/2,0)).to_pil().convert('RGB')
        im.thumbnail((1500,1500),Image.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=80,optimize=True,progressive=True)
        d='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode();chunk[str(i)]=d;size+=len(d)
        if size>9_000_000 or k==len(ids)-1:
            json.dump(chunk,open(f'{OUT}/tp_{src}_{n}.json','w'))
            for t in T:
                if t['src']==src and str(t['page']) in chunk:t['tp']=f'tp_{src}_{n}'
            chunk={};size=0;n+=1
json.dump(T,open(SP+'tiles.json','w'),ensure_ascii=False);os.system(f'cp {SP}tiles.json {OUT}/tiles.json')
tot=sum(os.path.getsize(OUT+'/'+f) for f in os.listdir(OUT) if f.startswith('tp_'))
print(len([f for f in os.listdir(OUT) if f.startswith('tp_')]),'files',round(tot/1048576,1),'MB')
