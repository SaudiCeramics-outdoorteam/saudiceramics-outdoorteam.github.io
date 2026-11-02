import pdfplumber,re,json,io,base64,glob,os,pypdfium2 as pdfium
from PIL import Image
SP='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
def b64(im,q=80,mx=420):
    im=im.convert('RGB');im.thumbnail((mx,mx),Image.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
COL={'Chrome':('كروم','#d9dde1'),'Brushed Silver':('فضي مطفي','#bdb6aa'),'Brushed Nickel':('فضي مطفي','#bdb6aa'),'Matt Grey':('رمادي مطفي','#6f7276'),'Gun Metal':('رمادي معدني','#5d5f62'),'Grey':('رمادي','#8a8c8e'),
     'Matt Black':('أسود مطفي','#222224'),'Brushed Gold':('ذهبي مطفي','#c4a463'),'English Gold':('ذهبي لامع','#d6ad55'),'Beige':('بيج','#d8c9ae'),'Carrara White':('أبيض كرارا','#ecebe7'),'White':('أبيض','#f2f2f0')}
FILES={'b1dfcb91-TILE_PROFILE_TRIM.pdf':'profile','a19c7254-LUXO_Brochure.pdf':'vanity','6a116dff-LAVINO_Brochure.pdf':'vanity','bc6a4496-Conza__brochure_Update.pdf':'mixer',
  'ee08c449-Shower_Arm_brochure.pdf':'fitting','6db000e5-Angle_Valve_Set-2__brochure.pdf':'fitting','a937b8ec-Angle_Valve_brochure.pdf':'fitting','9f2a583f-BR_Accessories__brochure.pdf':'acc',
  'ef5a7add-RIO_Mixers_brochure.pdf':'mixer','1050e6d4-Hose_Collection__brochure.pdf':'fitting','56a4c490-SCC_Ultra_Mix_Tile_Adhesive__brochure.pdf':'tile'}
out=[];SHEET={}
for fn,cat in FILES.items():
    F=A+fn;pdf=pdfplumber.open(F);doc=pdfium.PdfDocument(F);title=os.path.splitext(fn.split('-',1)[1])[0].replace('_',' ').replace('  ',' ')
    for i,pg in enumerate(pdf.pages):
        R=doc[i].render(scale=300/72).to_pil().convert('RGB');s=300/72
        sid=f"x{len(SHEET)}";SHEET[sid]=b64(R,80,2200)
        ws=pg.extract_words(keep_blank_chars=False)
        lines=(pg.extract_text() or '').split('\n')
        imgs=[im for im in pg.images if (im['x1']-im['x0'])>40 and (im['bottom']-im['top'])>40]
        # colour captions → image above
        capimg={}
        for cname in COL:
            first=cname.split()[0]
            for w in ws:
                if w['text']==first:
                    nxt=[x for x in ws if abs(x['top']-w['top'])<3 and 0<x['x0']-w['x1']<12]
                    full=w['text']+(' '+nxt[0]['text'] if nxt else '')
                    if full!=cname and not (len(cname.split())==1 and not nxt): continue
                    above=[im for im in imgs if im['bottom']<=w['top']+6 and im['x0']-25<=w['x0']<=im['x1']+5 and w['top']-im['bottom']<120]
                    if above and cname not in capimg:
                        im=sorted(above,key=lambda im:w['top']-im['bottom'])[0];capimg[cname]=im
        # section mapping: product photos (top band) left->right pair with table codes top->bottom, per column of the spread
        W=pg.width;nsec=max(1,round(W/595));secw=W/nsec;imgfor={}
        codew=[w for w in ws if re.fullmatch(r'1[13]\d{13}',w['text'])]
        for k in range(nsec):
            cs=sorted([w for w in codew if k*secw<=w['x0']<(k+1)*secw],key=lambda w:w['top'])
            if not cs:continue
            t0=cs[0]['top']
            ph=sorted([im for im in pg.images if 15<(im['x1']-im['x0'])<secw*.55 and 12<(im['bottom']-im['top'])<pg.height*.3 and k*secw-5<=im['x0']<(k+1)*secw and im['bottom']<=t0+5 and (im['bottom']-im['top'])<pg.height*.35],key=lambda im:im['x0'])
            seen_c=[];[seen_c.append(w['text']) for w in cs if w['text'] not in seen_c]
            if len(ph)>=len(seen_c):
                for i,c in enumerate(seen_c):imgfor[c]=ph[i]
            elif ph:
                for i,c in enumerate(seen_c):imgfor[c]=ph[min(i,len(ph)-1)]
        for k,l in enumerate(lines):
            for code in re.findall(r'\b(1[13]\d{13})\b',l):
                ctx=' '.join(lines[max(0,k-2):k+4])
                color=next((c for c in sorted(COL,key=len,reverse=True) if c.lower() in ctx.lower()),'')
                art=re.search(r'(?:Art\.? ?(?:No\.?|#)\s*:?\s*|ART#)([A-Z0-9\-]+)',ctx)
                dims=re.search(r'(\d{3,4}\s*[×xX]\s*\d{3,4}(?:\s*[×xX]\s*\d{2,4})?)',ctx)
                im=imgfor.get(code) or capimg.get(color) or (sorted(imgs,key=lambda im:-(im['x1']-im['x0'])*(im['bottom']-im['top']))[0] if imgs else None)
                crop=R.crop((int(im['x0']*s),int(im['top']*s),int(im['x1']*s),int(im['bottom']*s))) if im else R
                thumb=b64(crop);hi=b64(crop,86,1400)
                out.append(dict(code=code,src=fn,cat=cat,title=title,color=color,art=art.group(1) if art else '',dims=dims.group(1) if dims else '',ctx=ctx[:260],img=thumb,photo=hi,sheet=sid))
json.dump(out,open(SP+'broch.json','w'),ensure_ascii=False);json.dump(SHEET,open(SP+'broch_sheets.json','w'))
seen=set()
for o in out:
    if o['code'] in seen:continue
    seen.add(o['code']);print(o['cat'],o['code'],o['title'][:22],'|',o['color'],'|',o['art'],'|',o['dims'])
