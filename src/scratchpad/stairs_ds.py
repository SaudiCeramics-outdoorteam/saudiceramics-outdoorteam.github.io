import json,io,base64,pypdfium2 as pdfium
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
F='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/2e18a952-15x120x2.0_and_32x120x2.0_1.pdf'
pg=pdfium.PdfDocument(F)[0];b=io.BytesIO();pg.render(scale=200/72).to_pil().convert('RGB').save(b,'JPEG',quality=86);u='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
st=json.load(open(S+'stairs.json'))
for s in st:s['sheet']=u
json.dump(st,open(S+'stairs.json','w'),ensure_ascii=False);print('stairs ds',len(st))
