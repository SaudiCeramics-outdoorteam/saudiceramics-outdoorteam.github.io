import json,io,base64,re,pdfplumber,pypdfium2 as pdfium
from PIL import Image
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
def b64(im,q=86,mx=1700):
    im=im.convert('RGB');im.thumbnail((mx,mx),Image.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
# tubs
T='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/03b692e7-Bathtub__Shower_Tray_2022.pdf';doc=pdfium.PdfDocument(T)
pg=lambda n:doc[n-1].render(scale=300/72).to_pil().convert('RGB')
out={}
for name,n in [('ROMA',3),('ALASKA',4),('SALWA',5),('VERONA',6)]:
    im=pg(n);W,H=im.size
    out[name]={'img':b64(im.crop((int(W*.022),int(H*.085),int(W*.475),int(H*.31))),84,640),'photo':b64(im.crop((W//2,0,W,H)))}
for name,n,h in [('RIVIERA',7,0),('LARA',7,1),('ATLANTA',8,0),('TOLEDO',8,1),('PANAMA',9,1)]:
    im=pg(n);W,H=im.size;x0=0 if h==0 else W//2;hero=im.crop((x0,0,x0+W//2,int(H*.322)))
    out[name]={'img':b64(hero,84,640),'photo':b64(hero)}
json.dump(out,open(SP+'tub/tubimgs.json','w'))
# facade photos (left half of 300dpi page)
tex=json.load(open(SP+'pdf/tex3.json'))
for code in tex:
    im=Image.open(SP+f'pdf/p300_{code}.png').convert('RGB');W,H=im.size
    tex[code]['photo']=b64(im.crop((0,0,W//2,H)),86,2000)
json.dump(tex,open(SP+'pdf/tex3.json','w'))
# stairs
A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
S=json.load(open(SP+'stairs.json'))
for f,st in zip(['69f2512b-14734.pdf','2294dfd5-15771.pdf','dc41e726-15772.pdf','33954776-15773.pdf','be80d87a-15774.pdf','ba4bf99b-15775.pdf'],S):
    p=pdfplumber.open(A+f).pages[0];R=pdfium.PdfDocument(A+f)[0].render(scale=300/72).to_pil().convert('RGB');s=300/72
    cr=lambda im:b64(R.crop((int(im['x0']*s)+1,int(im['top']*s)+1,int(im['x1']*s)-1,int(im['bottom']*s)-1)),86,1000)
    st['treads']=[cr(im) for im in p.images if 640<im['x0']<1150 and 30<im['bottom']-im['top']<60][:6]
    st['risers']=[cr(im) for im in p.images if 640<im['x0']<1150 and 12<im['bottom']-im['top']<30 and im['top']>330][:3] or st['treads'][:1]
    st['sheet']=b64(R,80,2400);st['photo']=b64(R.crop((0,0,R.width//2,R.height)),86,1800)
json.dump(S,open(SP+'stairs.json','w'))
print('misc done')
