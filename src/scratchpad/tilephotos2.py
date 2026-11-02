import json,io,base64,os,sys,time,pypdfium2 as pdfium,pypdfium2.raw as R
from PIL import Image,ImageFilter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from enhance import _sr4
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';OUT='/home/claude/villa/data'
TARGET=int(os.environ.get('TP_TARGET','1900'));Q=int(os.environ.get('TP_Q','82'))
def photo_region(pg):
    w,h=pg.get_size();ob=[]
    for o in pg.get_objects(filter=(R.FPDF_PAGEOBJ_IMAGE,),max_depth=3):
        l,b,r,t=o.get_bounds();l,b,r,t=max(0,l),max(0,b),min(w,r),min(h,t)
        if r-l>5 and t-b>5:ob.append((l,b,r,t))
    if not ob:return None
    big=max(ob,key=lambda v:(v[2]-v[0])*(v[3]-v[1]))
    if big[2]-big[0]>w*.6:return big+(w,h)            # photo spans the spread: keep all of it
    bx=[v for v in ob if (v[0]+v[2])/2<w/2 and (v[2]-v[0])*(v[3]-v[1])>w*h*.01]
    if not bx:return None
    l=min(v[0] for v in bx);b=min(v[1] for v in bx);r=max(v[2] for v in bx);t=max(v[3] for v in bx)
    if (r-l)*(t-b)<(w/2)*h*.25:return None
    return l,b,r,t,w,h
def get(doc,i):
    pg=doc[i];reg=photo_region(pg);sc=150/72
    if reg:
        l,b,r,t,w,h=reg;im=pg.render(scale=sc,crop=(l,b,w-r,h-t)).to_pil().convert('RGB')
    else:
        w,h=pg.get_size();im=pg.render(scale=sc,crop=(0,0,w/2,0)).to_pil().convert('RGB')
    im.thumbnail((760,760),Image.LANCZOS)
    im=_sr4(im)                       # AI de-blur / super-resolve from native pixels
    im.thumbnail((TARGET,TARGET),Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(.8,40,2))
if __name__=='__main__':
    only=sys.argv[1:]
    T=json.load(open(SP+'tiles.json'))
    for src,F in [('por','/mnt/user-data/uploads/PORCELAIN_BOOK_final_2026_web__1_.pdf'),('cer','/mnt/user-data/uploads/Ceramic_catalogue__2_.pdf')]:
        doc=pdfium.PdfDocument(F);ids=sorted({int(t['page']) for t in T if t['src']==src})
        if only:
            for i in map(int,only):
                if i in ids or True:
                    try:get(doc,i).save(f'{SP}sr/tp_{src}_{i}.jpg',quality=Q)
                    except Exception as e:print(e)
            continue
        for f in os.listdir(OUT):
            if f.startswith(f'tp_{src}_'):os.remove(OUT+'/'+f)
        chunk={};n=0;size=0;t0=time.time()
        for k,i in enumerate(ids):
            im=get(doc,i);b=io.BytesIO();im.save(b,'JPEG',quality=Q,optimize=True,progressive=True)
            d='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode();chunk[str(i)]=d;size+=len(d)
            if k%10==0:print(src,k,len(ids),round(time.time()-t0),'s',flush=True)
            if size>9_000_000 or k==len(ids)-1:
                json.dump(chunk,open(f'{OUT}/tp_{src}_{n}.json','w'))
                for t in T:
                    if t['src']==src and str(t['page']) in chunk:t['tp']=f'tp_{src}_{n}'
                chunk={};size=0;n+=1
    if not only:
        json.dump(T,open(SP+'tiles.json','w'),ensure_ascii=False);os.system(f'cp {SP}tiles.json {OUT}/tiles.json')
        tot=sum(os.path.getsize(OUT+'/'+f) for f in os.listdir(OUT) if f.startswith('tp_'))
        print('DONE',len([f for f in os.listdir(OUT) if f.startswith('tp_')]),'files',round(tot/1048576,1),'MB')
