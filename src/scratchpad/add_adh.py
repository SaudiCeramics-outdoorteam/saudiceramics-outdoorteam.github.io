# usage: add_adh.py CODE "NAME" IMAGE_FILE "spec1=val1|spec2=val2"  -> adds/updates an adhesive in the catalogue (cat 'tile') + ADHESIVES list
import json,sys,io,base64,re
from PIL import Image
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
code,name,img,spec=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
b=io.BytesIO();Image.open(A+img).convert('RGB').save(b,'JPEG',quality=90);ph='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
N=json.load(open(S+'extra/new_items.json'));old=[n for n in N if n['code']==code];N=[n for n in N if n['code']!=code]
it=dict(cat='tile',code=code,name=name,color='',hex='#eeeeee',unit='كيس',qty=1,img=ph,photo=ph,sheet=None,spec=[s.split('=',1) for s in spec.split('|') if '=' in s],full=[])
if old and old[0].get('ds'):it['ds']=old[0]['ds']
if len(sys.argv)>5:
    bb=io.BytesIO();Image.open(A+sys.argv[5]).convert('RGB').save(bb,'JPEG',quality=90);it['ds']=['data:image/jpeg;base64,'+base64.b64encode(bb.getvalue()).decode()]
N.append(it);json.dump(N,open(S+'extra/new_items.json','w'),ensure_ascii=False)
p='/home/claude/villa-src.html';s=open(p).read();m=re.search(r'ADHESIVES=\[([^\]]*)\]',s);L=re.findall(r'"(\d+)"',m.group(1))
if code not in L:L.append(code);s=s[:m.start()]+'ADHESIVES=['+','.join(f'"{c}"' for c in L)+']'+s[m.end():];open(p,'w').write(s)
print('ok',code,len(L))
