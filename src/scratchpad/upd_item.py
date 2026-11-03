# usage: upd_item.py CODE "NAME" PHOTO "k=v|k=v" [EXTRA_DS_IMAGE...]  -> update a product in extra/new_items.json, prepending extra datasheet images
import json,sys,io,base64
from PIL import Image
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
def e(f):b=io.BytesIO();Image.open(A+f).convert('RGB').save(b,'JPEG',quality=90);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
code,name,ph,spec=sys.argv[1:5];N=json.load(open(S+'extra/new_items.json'))
for n in N:
    if n['code']==code:
        p=e(ph);n.update(name=name,img=p,photo=p,spec=[s.split('=',1) for s in spec.split('|') if '=' in s]);n['ds']=[e(f) for f in sys.argv[5:]]+(n.get('ds') or []);print('updated',code)
json.dump(N,open(S+'extra/new_items.json','w'),ensure_ascii=False)
