import json,io,base64,pypdfium2 as pdfium
from PIL import Image
S='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/';A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
def enc(im,q=88):b=io.BytesIO();im.convert('RGB').save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
ph=enc(Image.open(A+'bb3d94c1-image.png'));dr=enc(Image.open(A+'0a8073df-image.png'))
lot=[enc(p.render(scale=200/72).to_pil(),86) for p in pdfium.PdfDocument('/home/claude/inbox/9743a4cf-Spark_Heat_technical_data_sheet_Lot97_7.pdf')]
H=json.load(open(S+'wh/heat_new.json'));H=[h for h in H if h['code']!='149709010105011']
H.append(dict(cat='heater',code='149709010105011',name='سخان مياه كهربائي 50 لتر · سبارك هيت',color='',hex='#f4f4f2',unit='قطعة',qty=1,kind='vert',cap=50,line='vstd',img=ph,photo=ph,sheet=None,ds=[dr]+lot,
 spec=[["الموديل","EWH-V50 · Spark Heat"],["السعة","50 لتر"],["النوع","عمودي معلّق"],["القدرة","1200 واط · 220–240 فولت"],["الضمان","3 سنوات على الخزان"]],
 full=[["الأبعاد","531 × 445 × 465 مم"],["زمن التسخين (Δt=45°)","ساعتين و30 دقيقة"],["أقصى ضغط","0.75 ميجا باسكال"],["سماكة العزل","20 مم"],["الوزن","16.5 كغ"],
  ["المميزات","صناعة سعودية بمواصفات عالمية · مطابق للمواصفات السعودية SASO · عازل خالٍ من مركبات الكلوروفلوروكربون · ثرموستات سلامة مزدوج · تسخين سريع · توفر قطع الغيار · معالجة بالبورسلان · غلاف خارجي مقاوم للصدأ · صمامي أمان علوي وسفلي"],
  ["ملاحظة","ليّات التوصيل تباع منفصلة"]]))
ph2=enc(Image.open(A+'bfe6e9dd-image.png'));dr2=enc(Image.open(A+'bc292ae3-image.png'))
H=[h for h in H if h['code']!='149711010105011']
H.append(dict(cat='heater',code='149711010105011',name='سخان مياه كهربائي 80 لتر عمودي · سبارك هيت',color='',hex='#f4f4f2',unit='قطعة',qty=1,kind='vert',cap=80,line='vstd',img=ph2,photo=ph2,sheet=None,ds=[dr2]+lot,
 spec=[["الموديل","EWH-V80 · Spark Heat"],["السعة","80 لتر"],["النوع","عمودي معلّق"],["القدرة","1200 واط · 220–240 فولت"],["الضمان","3 سنوات"]],
 full=[["الأبعاد","769 × 445 × 465 مم"],["زمن التسخين (Δt=45°)","3 ساعات و55 دقيقة"],["أقصى ضغط","0.75 ميجا باسكال"],["سماكة العزل","20 مم"],["الوزن","22.5 كغ"],
  ["المميزات","صناعة سعودية بمواصفات عالمية · مطابق للمواصفات السعودية SASO"],["ملاحظة","ليّات التوصيل تباع منفصلة"]]))
ph3=enc(Image.open(A+'c42a7b3c-image.png'));dr3=enc(Image.open(A+'9ed753cb-image.png'))
H=[h for h in H if h['code']!='149709010205011']
H.append(dict(cat='heater',code='149709010205011',name='سخان مياه كهربائي 50 لتر أفقي · سبارك هيت',color='أبيض',hex='#f4f4f2',unit='قطعة',qty=1,kind='horiz',cap=50,line='horiz',img=ph3,photo=ph3,sheet=None,ds=[dr3]+lot,
 spec=[["الموديل","EWH-H50 · Spark Heat"],["السعة","50 لتر"],["النوع","أفقي معلّق"],["اللون","أبيض"],["الضمان","3 سنوات على الخزان"]],
 full=[["الأبعاد","531 × 460 × 465 مم"],["القدرة","1200 واط · 220–240 فولت"],["المميزات","صناعة سعودية بمواصفات عالمية · مطابق للمواصفات السعودية SASO"]]))
ph4=enc(Image.open(A+'51c6e9fe-image.png'));dr4=enc(Image.open(A+'7a58b5b0-image.png'))
H=[h for h in H if h['code']!='149711010205011']
H.append(dict(cat='heater',code='149711010205011',name='سخان مياه كهربائي 80 لتر أفقي · سبارك هيت',color='',hex='#f4f4f2',unit='قطعة',qty=1,kind='horiz',cap=80,line='horiz',img=ph4,photo=ph4,sheet=None,ds=[dr4]+lot,
 spec=[["الموديل","EWH-H80 · Spark Heat"],["السعة","80 لتر"],["النوع","أفقي معلّق"],["القدرة","1200 واط · 220–240 فولت"],["الضمان","3 سنوات على الخزان"]],
 full=[["الأبعاد","769 × 460 × 465 مم"],["زمن التسخين (Δt=45°)","3 ساعات و55 دقيقة"],["أقصى ضغط","0.75 ميجا باسكال"],["سماكة العزل","20 مم"],["الوزن","22.5 كغ"],
  ["المميزات","صناعة سعودية بمواصفات عالمية · مطابق للمواصفات السعودية SASO"],["ملاحظة","ليّات التوصيل تباع منفصلة"]]))
json.dump(H,open(S+'wh/heat_new.json','w'),ensure_ascii=False);print('spark added')
