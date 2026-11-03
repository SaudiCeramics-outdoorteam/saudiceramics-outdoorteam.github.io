# usage: ov.py CODE IMAGE_FILE ["NAME"] ["k=v|k=v"]  -> override photo/name/spec of an existing catalogue product
import json,sys,io,base64,os
from PIL import Image
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
f=S+'extra/overrides.json';O=json.load(open(f)) if os.path.exists(f) else {}
c=sys.argv[1];b=io.BytesIO();Image.open(A+sys.argv[2]).convert('RGB').save(b,'JPEG',quality=90);ph='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
o=O.get(c,{});o.update(img=ph,photo=ph)
if len(sys.argv)>3 and sys.argv[3]:o['name']=sys.argv[3]
if len(sys.argv)>4 and sys.argv[4]:o['spec']=[s.split('=',1) for s in sys.argv[4].split('|') if '=' in s]
O[c]=o;json.dump(O,open(f,'w'));print('override',c,len(O))
