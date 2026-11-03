# usage: add_item.py CAT CODE "NAME" "UNIT" PHOTO "k=v|k=v" [DS_IMAGE...]  -> new catalogue product (not an adhesive)
import json,sys,io,base64
from PIL import Image
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
def e(f):b=io.BytesIO();Image.open(A+f).convert('RGB').save(b,'JPEG',quality=90);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
cat,code,name,unit,ph,spec=sys.argv[1:7];p=e(ph)
N=json.load(open(S+'extra/new_items.json'));N=[n for n in N if n['code']!=code]
N.append(dict(cat=cat,code=code,name=name,color='',hex='#d9dde1',unit=unit,qty=1,img=p,photo=p,sheet=None,ds=[e(f) for f in sys.argv[7:]],spec=[s.split('=',1) for s in spec.split('|') if '=' in s],full=[]))
json.dump(N,open(S+'extra/new_items.json','w'),ensure_ascii=False);print('ok',code)
