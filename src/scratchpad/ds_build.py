# Official datasheets: /home/claude/datasheets/<src>_<W>x<H>_<T>.pdf  ->  data/ds_0.json {"src|WxH|T":[pages]}
import os,io,base64,json,pypdfium2 as pdfium,numpy as np
from PIL import Image
D='/home/claude/datasheets';out={}
for f in sorted(os.listdir(D)):
    if not f.endswith('.pdf'):continue
    src,wh,t=f[:-4].split('_');w,h=wh.split('x');key=f"{src}|{float(w):g}x{float(h):g}|{float(t):.1f}"
    doc=pdfium.PdfDocument(f'{D}/{f}');pages=[]
    for pg in doc:
        im=pg.render(scale=250/72).to_pil().convert('RGB');a=np.asarray(im).min(2)<235;ys,xs=np.where(a)
        p=40;im=im.crop((max(0,xs.min()-p),max(0,ys.min()-p),min(im.width,xs.max()+p),min(im.height,ys.max()+p)))
        b=io.BytesIO();im.save(b,'JPEG',quality=88,optimize=True);pages.append('data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode())
    out[key]=pages;print(key,len(pages),im.size)
out['guide']=json.load(open('/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/extra/ds_existing.json'))['guide']
json.dump(out,open('/home/claude/villa/data/ds_0.json','w'));print(os.path.getsize('/home/claude/villa/data/ds_0.json')>>10,'KB')
