import json,io,base64,pypdfium2 as pdfium
from PIL import Image
A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/'
def img(f,mx=None):
    im=Image.open(A+f).convert('RGB');import numpy as np
    a=np.asarray(im).astype(int)
    def flat(v):return v.std()<7 and (v.mean()<200 or v.mean()>246)   # screenshot bars / blank edges
    t,b,l,r=0,a.shape[0],0,a.shape[1]
    while t<b-50 and flat(a[t,l:r]):t+=1
    while b>t+50 and flat(a[b-1,l:r]):b-=1
    while l<r-50 and flat(a[t:b,l]):l+=1
    while r>l+50 and flat(a[t:b,r-1]):r-=1
    im=im.crop((l,t,r,b))
    # drop the thin dark UI bar some screenshots carry at the top
    b=io.BytesIO();im.save(b,'JPEG',quality=92);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def pdfp(f):
    out=[];d=pdfium.PdfDocument(A+f)
    for pg in d:
        im=pg.render(scale=200/72).to_pil().convert('RGB');b=io.BytesIO();im.save(b,'JPEG',quality=86,optimize=True);out.append('data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode())
    return out
SOLAR_PDF=pdfp('325c8bab-SOLAR_SYSTEM_DIRECT_TYPE_-_DATA_SHEETSREV02-240L_1.pdf');CWH_PDF=pdfp('83a2db9d-CENTRAL_WATER_HEATER_Technical_data_sheet.pdf')
INST=["استخدام سلك كهربائي مقاس {w} مم من الطبلون الرئيسي مباشرة مع قاطع {a} أمبير","تمديد سلك (الخط الأرضي)","ضغط المياه لا يقل عن 0.2 بار ولا يزيد عن 6.0 بار","ليّات التوصيل تباع على حدة"]
def inst(code,name,model,photo,sheet,A_,B_,C_,watt,amp,wfr,wire,kg,brk,hexc):
    req=[r.format(w=wire,a=brk) for r in INST]
    spec=[["الموديل",model],["النوع","سخان فوري عمودي"],["القدرة",f"{watt} واط"],["الأبعاد (ارتفاع×عرض×عمق)",f"{A_} × {B_} × {C_} مم"]]
    full=[["الجهد","220–240 فولت"],["التردد","50–60 هرتز"],["ضغط التشغيل","0.02–0.6 ميجا باسكال"],["التيار",f"{amp} أمبير"],["معدل التدفق للتشغيل",f"{wfr} لتر/دقيقة"],["ضبط الحرارة","30–55 °م"],["مقطع أسلاك التوصيل",f"{wire} مم²"],["فئة الأمان","IP25"],["الوزن",f"{kg} كغ"],["ملف التحميل","2XS"],["المميزات","توفير في الطاقة · طلاء أملس عالي الجودة · سهل التنظيف · شاشة لمس · عرض رقمي للحرارة · حماية متعددة · تقنية تسخين حاصلة على براءة اختراع"]]+[["متطلبات التركيب","؛ ".join(req)]]
    return dict(cat='heater',code=code,name=name,color='',hex=hexc,unit='قطعة',qty=1,kind='instant',cap=0,line='fawry',dims=[A_,B_,C_],img=img(photo),photo=img(photo),sheet=None,ds=[img(sheet)],spec=spec,full=full,req=req)
def solar(code,name,model,photo,sheet,cap,Bw,D,E,F,G,lp,panels):
    spec=[["الموديل",model],["النوع","سخان شمسي مباشر (Direct System)"],["السعة",f"{cap} لتر"],["عدد الألواح",str(panels)]]
    full=[["الأبعاد A/B/C/D",f"1190 / {Bw} / 1650 / {D} مم"],["طول الخزان (E) / القطر (F)",f"{E} / {F} مم"],["المسافة بين القاعدتين (G)",f"{G} مم"],["سخان احتياطي","3000 واط · 220–240 فولت"],["أقصى ضغط تشغيل","0.75 ميجا باسكال"],["سماكة العزل","20 مم"],["ملف التحميل",lp],["توصيل المياه",'1/2"'],["توصيل الألواح",'3/4"'],["الألواح","ألمنيوم مؤنود · زجاج مقسّى منخفض الحديد · أنابيب نحاس · امتصاص 95% · EN 12975-2"],["حماية الخزان","أنود ماغنيسيوم · ثرموستات أمان مزدوج"],["مكان التركيب","سطح المنزل"]]
    return dict(cat='heater',code=code,name=name,color='',hex='#ffffff',unit='قطعة',qty=1,kind='solar',cap=cap,line='solar',dims=[Bw,E,F,panels],img=img(photo),photo=img(photo),sheet=None,ds=[img(sheet)]+SOLAR_PDF,spec=spec,full=full)
def central(code,name,model,photo,gal,cap,A_,Bh,C,D,ht,kg):
    spec=[["الموديل",model],["النوع","سخان كهربائي مركزي عمودي (أرضي)"],["السعة",f"{gal} جالون · {cap} لتر"],["الضمان","7 سنوات على الخزان"]]
    full=[["الأبعاد A/B/C/D",f"{A_} / {Bh} / {C} / {D} مم"],["القدرة","عنصران 3800/4500 واط"],["الجهد","220/240 فولت · أحادي الطور"],["زمن التسخين (Δt=45°)",ht],["أقصى ضغط","1.0 ميجا باسكال (10 بار)"],["سماكة العزل","30 مم بولي يوريثان"],["الوزن",f"{kg} كغ"],["المميزات","عنصرا تسخين وثرموستات مزدوج · أنود ماغنيسيوم كبير · صمام أمان حرارة وضغط · صمام تصريف · خزان مبطن بالمينا الزجاجية · هيكل إيبوكسي مقاوم للصدأ"]]
    return dict(cat='heater',code=code,name=name,color='',hex='#ffffff',unit='قطعة',qty=1,kind='central',cap=cap,line='central',dims=[Bh,D],img=img(photo),photo=img(photo),sheet=None,ds=CWH_PDF,spec=spec,full=full)
N=[inst('140100482605183','سخان مياه فوري عمودي · فوري بلس','FAWRY PLUS','9b7e125e-image.png','abb0a9e8-image.png',460,265,75,11000,47.8,2.0,10,5.0,60,'#f4f4f2'),
   inst('140100482505196','سخان مياه فوري عمودي · فوري برو','FAWRY PRO','3b1f657d-image.png','b740797d-image.png',400,200,50,7500,32.6,1.5,6,4.0,40,'#141518'),
   solar('160114151505081','سخان مياه شمسي 150 لتر','SWH-H150','6cbcb01e-image.png','f8cb70dd-image.png',150,1010,1700,1350,510,860,'L',1),
   solar('160121161505081','سخان مياه شمسي 200 لتر','SWH-H200','cb5fe744-image.png','e166863a-image.png',200,2080,1750,1470,560,1080,'XL',2),
   solar('160132161505081','سخان مياه شمسي 240 لتر','SWH-H240','c7acf206-image.png','f17b6e9f-image.png',240,2080,1750,1720,560,1080,'XL',2),
   central('140115030105121','سخان مياه كهربائي مركزي 40 جالون عمودي','CWH-40G','c1aec17f-image.png',40,150,1130,1200,153,508,'1 ساعة 40 دقيقة',46.5),
   central('140116030105121','سخان مياه كهربائي مركزي 50 جالون عمودي','CWH-50G','cfa61537-image.png',50,200,1215,1285,183,560,'2 ساعة',58.0),
   central('140118030105121','سخان مياه كهربائي مركزي 80 جالون عمودي','CWH-80G','c3179f09-image.png',80,300,1755,1825,338,560,'3 ساعات 25 دقيقة',87.0)]
json.dump(N,open('wh/heat_new.json','w'),ensure_ascii=False);print(len(N))
