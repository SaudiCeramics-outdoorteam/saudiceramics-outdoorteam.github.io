import json
im=json.load(open('/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/tub/tubimgs.json'))
tubspec=[["الخامة","أكريليك مصبوب"],["سماكة الجدار","8 مم"],["القاعدة","حديد مجلفن"],["الصرف","Pop-up مطلي كروم"],["الشهادة","SASO"],["الضمان","5 سنوات على تغيّر اللون"]]
def tv(code,mdl,L,W,side): return {"code":code,"name":f"FULL SET Bathtub {mdl} {L} X {W} {'Right' if side=='R' else 'Left'} Side","label":f"{L}×{W} سم · {'يمين' if side=='R' else 'يسار'}","size":[L/100,W/100],"side":side}
def tr(code,mdl,a,b,kind): return {"code":code,"name":f"Shower Tray {mdl} {a if a==b else f'{a}x{b}'} {kind}","label":f"{a}×{b} سم","size":[a/100,b/100]}
M=[
 {"id":"ROMA","title":"ROMA","kind":"free","spec":[["النوع","بانيو قائم بذاته"],["المقاس","171×85 سم"]]+tubspec,"variants":[{"code":"180691501001000","name":"FREE STANDING Bathtub ROMA 171 X 85","label":"171×85 سم","size":[1.71,.85]}]},
 {"id":"ALASKA","title":"ALASKA","kind":"tub","spec":[["النوع","بانيو مع واجهة"]]+tubspec,"variants":[tv("180531500101001","ALASKA",150,70,"R"),tv("180531500101002","ALASKA",150,70,"L")]},
 {"id":"SALWA","title":"SALWA","kind":"tub","spec":[["النوع","بانيو مع واجهة"]]+tubspec,"variants":[tv("180511500101001","SALWA",150,70,"R"),tv("180511500101002","SALWA",150,70,"L"),tv("180511500201001","SALWA",170,70,"R"),tv("180511500201002","SALWA",170,70,"L")]},
 {"id":"VERONA","title":"VERONA","kind":"tub","spec":[["النوع","بانيو مع واجهة"]]+tubspec,"variants":[tv("180521500201001","VERONA",170,70,"R"),tv("180521500201002","VERONA",170,70,"L"),tv("180521500301001","VERONA",170,80,"R"),tv("180521500301002","VERONA",170,80,"L")]},
 {"id":"RIVIERA","title":"RIVIERA","kind":"corner","r":.85,"h":.17,"spec":[["النوع","حوض قدم زاوية"],["ارتفاع الجدار","170 مم"],["سماكة الجدار","6-7 مم"],["الخامة","أكريليك مصبوب"],["الضمان","5 سنوات على تغيّر اللون"]],"variants":[tr("180551601101000","RIVIERA",70,70,"Corner"),tr("180551601201000","RIVIERA",80,80,"Corner")]},
 {"id":"LARA","title":"LARA","kind":"square","h":.17,"spec":[["النوع","حوض قدم مربع"],["ارتفاع الجدار","170 مم"],["سماكة الجدار","6-7 مم"],["الخامة","أكريليك مصبوب"],["الضمان","5 سنوات على تغيّر اللون"]],"variants":[tr("180541601101000","LARA",70,70,"Square"),tr("180541601201000","LARA",80,80,"Square")]},
 {"id":"ATLANTA","title":"ATLANTA","kind":"corner","r":.62,"h":.13,"spec":[["النوع","حوض قدم زاوية بدون قاعدة"],["ارتفاع الجدار","130 مم"],["الخامة","أكريليك مصبوب"],["الضمان","5 سنوات على تغيّر اللون"]],"variants":[tr("180611600101000","ATLANTA",70,70,"Corner"),tr("180611600201000","ATLANTA",80,80,"Corner"),tr("180611600301000","ATLANTA",90,90,"Corner")]},
 {"id":"TOLEDO","title":"TOLEDO","kind":"square","h":.13,"spec":[["النوع","حوض قدم مربع بدون قاعدة"],["ارتفاع الجدار","130 مم"],["الخامة","أكريليك مصبوب"],["الضمان","5 سنوات على تغيّر اللون"]],"variants":[tr("180601600101000","TOLEDO",70,70,"Corner"),tr("180601600201000","TOLEDO",80,80,"Corner"),tr("180601600301000","TOLEDO",90,90,"Corner")]},
 {"id":"PANAMA","title":"PANAMA","kind":"square","h":.13,"spec":[["النوع","حوض قدم مستطيل بدون قاعدة"],["المقاس","120×80 سم"],["ارتفاع الجدار","130 مم"],["سماكة الجدار","4 مم"],["الضمان","5 سنوات على تغيّر اللون"]],"variants":[{"code":"180621600401000","name":"Shower Tray PANAMA 120x80 Rectangular","label":"120×80 سم","size":[1.2,.8]}]},
]
for m in M: m.update(im[m["id"]])
BATHING=M

# MALAGA square shower tray 70x70 (added 3 Nov, user-supplied photo + datasheet)
def _malaga():
    import io,base64,pypdfium2 as _p
    from PIL import Image as _I
    A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
    def e(im):b=io.BytesIO();im.convert('RGB').save(b,'JPEG',quality=88);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    ph=e(_I.open(A+'8ca00dac-image.png'))
    return dict(id='MALAGA',title='MALAGA',kind=[b for b in BATHING if b['id']=='TOLEDO'][0]['kind'],img=ph,photo=ph,
      spec=[['النوع','حوض قدم مربع'],['المقاس','70×70 سم'],['التركيب','قبل البلاط'],['ملاحظة','غطاء فتحة التصريف والهراب يباع على حدة']],
      variants=[dict(code='180561600101000',name='Shower Tray MALAGA 70 X 70 (Before Tiles)',label='70×70 سم',size=[.7,.7])],
      _sheet=e(_p.PdfDocument(A+'6ba12ffe-Malaga_70x70_ST.pdf')[0].render(scale=200/72).to_pil()))
if not any(b['id']=='MALAGA' for b in BATHING):
    _m=_malaga();MALAGA_SHEET=_m.pop('_sheet');BATHING.append(_m)
