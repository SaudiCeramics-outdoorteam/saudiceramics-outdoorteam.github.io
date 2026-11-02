import io,base64,json,sys
from PIL import Image,ImageFilter
import numpy as np
SR_DIR='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/sr/re/models/'
_net=None
def _sr4(im):
    """Real-ESRGAN (realesr-animevideov3 x4, ncnn CPU) super-resolution"""
    global _net
    import ncnn
    if _net is None:
        _net=ncnn.Net();_net.opt.use_vulkan_compute=False;_net.opt.num_threads=2
        _net.load_param(SR_DIR+'realesr-animevideov3-x4.param');_net.load_model(SR_DIR+'realesr-animevideov3-x4.bin')
    a=np.pad(np.asarray(im.convert('RGB')).astype(np.float32)/255.*.94+.02,((8,8),(8,8),(0,0)),mode='reflect');H,W,_=a.shape;out=np.zeros((H*4,W*4,3),np.float32);tile,pad=192,10
    for y in range(0,H,tile):
        for x in range(0,W,tile):
            y0,x0=max(0,y-pad),max(0,x-pad);y1,x1=min(H,y+tile+pad),min(W,x+tile+pad)
            blk=np.ascontiguousarray(a[y0:y1,x0:x1].transpose(2,0,1));mt=ncnn.Mat(blk);ex=_net.create_extractor();ex.input('data',mt)
            r=np.array(ex.extract('output')[1]).copy().transpose(1,2,0);oy,ox=(y-y0)*4,(x-x0)*4;h=min(tile,H-y)*4;w=min(tile,W-x)*4
            out[y*4:y*4+h,x*4:x*4+w]=r[oy:oy+h,ox:ox+w]
    out=(out[32:-32,32:-32]-.02)/.94
    return Image.fromarray((np.clip(out,0,1)*255).round().astype(np.uint8))
def dec(d):return Image.open(io.BytesIO(base64.b64decode(d.split(',',1)[1]))).convert('RGB')
def enc(im,q=86):b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True,progressive=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def _white_bg(im):
    a=np.asarray(im.resize((64,64)));c=np.concatenate([a[:4].reshape(-1,3),a[-4:].reshape(-1,3),a[:,:4].reshape(-1,3),a[:,-4:].reshape(-1,3)])
    return c.mean()>238
def _trim(im):
    a=np.asarray(im);m=(a.min(2)<232)
    if m.sum()<50:return im
    H,W=m.shape;rc=m.sum(1);cc=m.sum(0);tr=max(3,W*.004);tc=max(3,H*.004)
    ys=np.where(rc>tr)[0];xs=np.where(cc>tc)[0]
    if len(ys)<5 or len(xs)<5:return im
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max();w,h=x1-x0,y1-y0;p=int(max(w,h)*.12)
    crop=im.crop((x0,y0,x1+1,y1+1));side_w,side_h=w+2*p,h+2*p
    # frame on a gently proportioned white canvas (no wider than 4:3, no taller than 3:4)
    tw,th=max(side_w,int(side_h*.75)),max(side_h,int(side_w*.75))
    c=Image.new('RGB',(tw,th),(255,255,255));c.paste(crop,((tw-w)//2,(th-h)//2));return c
_cache={}
TARGET=2000
def hq(d,target=TARGET):
    if not d or not d.startswith('data:'):return d
    if d in _cache:return _cache[d]
    im=dec(d)
    if _white_bg(im):im=_trim(im)
    L=max(im.size)
    if L<target*.9:
        if L>600:im.thumbnail((600,600),Image.LANCZOS)   # SR from (near-)native pixels, never from an upsampled crop
        im=_sr4(im)
    if max(im.size)>target:im.thumbnail((target,target),Image.LANCZOS)
    elif max(im.size)<1600:
        k=1600/max(im.size);im=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2,60,2))
    r=enc(im,85);_cache[d]=r;return r
def small(d,px=220):
    if not d or not d.startswith('data:'):return d
    im=dec(d)
    if _white_bg(im):im=_trim(im)
    if max(im.size)>px:im.thumbnail((px,px),Image.LANCZOS)
    return enc(im,76)
def sample_hex(d):
    a=np.asarray(dec(d).resize((160,160))).reshape(-1,3).astype(float)
    mx=a.max(1);mn=a.min(1);sat=(mx-mn)/np.maximum(mx,1)
    keep=(mx<235)|(sat>.18);keep&=~((mx>200)&(sat<.06)&(mn>195));px=a[keep]
    if len(px)<50:return None
    med=np.median(px,0)
    if sat[keep].mean()>.18:s2=px[sat[keep]>np.percentile(sat[keep],50)];med=np.median(s2,0)
    lum=px.mean(1)
    if med.mean()<115:med=np.median(px[lum<=np.percentile(lum,45)],0)
    return '#%02x%02x%02x'%tuple(int(v) for v in med)
METAL={'mixer','shower','acc','fitting','shattaf','drain'}
_done={}
def enhance(items):
    for it in items:
        if it.get('cat') in METAL and it.get('img'):
            h=sample_hex(it['img'])
            if h:it['hex']=h
        src=it.get('photo') or it.get('img')
        if src:
            it['photo']=hq(src)
        if it.get('ds'):it['ds']=[hq(d) for d in it['ds']]
        if it.get('img'):it['img']=small(it['img'])
    return items
