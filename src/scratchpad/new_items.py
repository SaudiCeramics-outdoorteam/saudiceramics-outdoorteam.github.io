# Products the user supplied official datasheets for that are not in the catalogues yet, plus datasheets for existing codes.
import json,io,base64,pypdfium2 as pdfium,pypdfium2.raw as R
from PIL import Image
A='/mnt/user-data/attachments/9b11369b-255f-547e-a148-3cb5bc61c84e/';X='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/extra/'
def enc(im,q=88):b=io.BytesIO();im.convert('RGB').save(b,'JPEG',quality=q,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def pages(f,dpi=200):return [enc(pg.render(scale=dpi/72).to_pil(),86) for pg in pdfium.PdfDocument(A+f)]
import numpy as np
CROPS={'130230670605200':(.6,.26,.82,.37),'130230290205200':(.08,.1,.62,.32),'130230670195200':(.53,.33,.83,.70),'130581460057800':(.28,.2,.97,.78),'130061380015200':(.3,.05,.66,.9),'130571690009100':(.1,.05,.47,.21)}   # page-fraction crops for scanned sheets: (x0,y0,x1,y1) from top-left
def photoness(im):
    a=np.asarray(im.convert('L').resize((160,160))).astype(float);mid=((a>25)&(a<228)).mean();return mid*(a.std()+1)
def photo(f,page=0,pick=None,dpi=320,crop=None):
    pg=pdfium.PdfDocument(A+f)[page];w,h=pg.get_size()
    if crop:x0,y0,x1,y1=crop;return enc(pg.render(scale=dpi/72,crop=(w*x0,h*(1-y1),w*(1-x1),h*y0)).to_pil())
    ob=[]
    for o in pg.get_objects(filter=(R.FPDF_PAGEOBJ_IMAGE,),max_depth=4):
        l,b,r,t=o.get_bounds();l,b,r,t=max(0,l),max(0,b),min(w,r),min(h,t)
        if r-l>30 and t-b>30 and (r-l)*(t-b)<w*h*.8 and 1-t/h>.13 and 1-b/h<.85:ob.append((l,b,r,t))
    best=None
    for l,b,r,t in ob:
        im=pg.render(scale=dpi/72,crop=(l,b,w-r,h-t)).to_pil();sc=photoness(im)*((r-l)*(t-b))**.25
        if best is None or sc>best[0]:best=(sc,im)
    return enc(best[1]) if best else None
SAT='#c4c7cb'
def acc(code,name,kind,f,dims,extra):
    spec=[["الكود التجاري",name.split('·')[-1].strip()],["الخامة","ستانلس ستيل AISI "+("316" if kind=="rail" else "304")+" · تشطيب ساتان"],["الأبعاد",dims]]
    return dict(cat='acc',code=code,name=name,color='ستانلس ساتان',hex=SAT,unit='قطعة',qty=1,kind=kind,spec=spec,full=extra,img=None,photo=photo(f,crop=CROPS.get(code)),sheet=None,ds=pages(f))
N=[acc('130230670315200','موزع مناديل ورقية · DT2106CS','towel_disp','3835db2e-130230670315200_DT2106CS_Satin_Paper_Towel_Dispenser.pdf','185 × 165 × 95 مم',[["التركيب","على الجدار"]]),
   acc('130230670405200','حامل ورق التواليت · AI0113CS','paper','e9e6e983-130230670405200_AI0113CS_Toilet_Paper_Roll_Holder_1.pdf','52 × 193 × 97 مم',[["المسافة بين مراكز القواعد","141 مم"],["التركيب","على الجدار"]]),
   acc('130230670605200','صحن صابون · AI0118CS','soapdish','cc8bb67f-130230670605200_AI0118CS_Soap_Dish_1.pdf','52 × 108 × 106 مم',[["التركيب","على الجدار"],["الشهادات","ISO 9001:2008"]]),
   acc('130230670215200','موزع صابون سائل أفقي · DJ0112CS','soap_h','3c87e5f9-130230670215200_DJ0112CS_Horizontal_Soap_Dispenser_1.pdf','208 × 121 × 130 مم',[["السعة","1.2 لتر"],["الكمية لكل ضغطة","1.1 مل"],["التشغيل","زر ضغط · مقاوم للعبث"]]),
   acc('130230670225200','موزع صابون سائل عمودي · DJ0111CS','soap_v','82cd9a97-130230670225200_-_DJ0111CS_Vertical_Liquid_Soap_Dispenser.pdf','208 × 121 × 130 مم',[["السعة","1.2 لتر"],["التشغيل","زر ضغط · مقاوم للعبث"]]),
   acc('130230670705200','علاقة روب · AI0033CS','hook','764d7d37-130230670705200_AI0033CS_Robe_Hook.pdf','52 × 52 × 41 مم',[["البعد عن الجدار","41 مم"]]),
   acc('130230670505200','حامل منشفة · AI0184CS','rail','5f13f2f8-130230670505200_AI0184CS_Towel_Rail.pdf','52 × 495 × 88 مم',[["المسافة بين مراكز القواعد","445 مم"]])]
N.append(dict(cat='mirror',code='130231270038300',name='مرآة LED · TC-822',color='',hex='#ffffff',unit='قطعة',qty=1,shape='rect',led=True,mw=50,mh=80,
   spec=[["الموديل","TC-822"],["المقاس","500 × 800 مم بدون إطار"],["الإضاءة","حساس لمس · 3 ألوان إضاءة · إضاءة خلفية"],["الضمان","سنتين"]],full=[],img=None,photo=photo('ef01b1e8-130231270038300.pdf'),sheet=None,ds=pages('ef01b1e8-130231270038300.pdf')))
N.append(dict(cat='mixer',code='180101010352002',name='خلاط مغسلة RISE · كروم',color='كروم',hex='#d9dde1',unit='قطعة',qty=1,series='rise',
   spec=[["السلسلة","RISE"],["الخرطوشة","سيراميك 35 مم"],["المصفاة","مخفية M24×1"],["معدل التدفق","4.4 لتر/دقيقة عند 1 بار"],["اللي","2 لي مرن G1/2 × 60 سم"],["المقبض","زماك"],["يشمل","صفاية ضغط Push waste"]],full=[],img=None,photo=photo('20b533ff-Rise_13.6_1.pdf'),sheet=None,ds=pages('20b533ff-Rise_13.6_1.pdf')))
N.append(dict(cat='kitchen',code='180101010152008',name='خلاط مطبخ CUBIST · كروم',color='كروم',hex='#d9dde1',unit='قطعة',qty=1,kind='kmixer',
   spec=[["السلسلة","CUBIST"],["النوع","خلاط حوض بفتحة واحدة"],["الخرطوشة","سيراميك 35 مم"],["المصفاة","M24×1"],["معدل التدفق","4.9 لتر/دقيقة عند 1 بار"],["المقبض","زماك"]],full=[],img=None,photo=photo('75d141eb-Cubist_Single_Hole_Sink_1.pdf'),sheet=None,ds=pages('75d141eb-Cubist_Single_Hole_Sink_1.pdf')))
N.append(dict(cat='kitchen',code='130571690009300',name='حوض مطبخ ستانلس 60 × 45',color='ستانلس',hex='#c9ccd0',unit='قطعة',qty=1,kind='ksink',
   spec=[["المقاس الخارجي","600 × 450 مم"],["مقاس الحوض","600 × 450 مم"],["العمق","220 مم"],["يشمل","مصفاة سلة + طقم تصريف"],["التصميم","خطوط تصريف داخلية"]],full=[],img=None,photo=photo('99deb820-130571690009300.pdf',crop=(.075,.065,.405,.29)),sheet=None,ds=pages('99deb820-130571690009300.pdf')))
CUPO=[('130461734094900','CUPO LIGHT GREY · Carrara','كرارا رمادي فاتح','#d6d6d2','111140912511016',0),('130461734739901','CUPO WOOD BEIGE','خشبي بيج','#b48c63','111150622511016',1),
      ('130461734734900','CUPO SHALAAL LIGHT GREY','رمادي','#b9bab7','111146932511016',2),('130461734736500','CUPO TRAVERTINE','كريمي فاتح · ترافرتين','#dacdb3','111147342511016',3)]
TP=pages('823e60b4-TDS_1.pdf')
for code,name,col,hexc,tile,i in CUPO:
    N.append(dict(cat='vanity',code=code,name='مغسلة '+name,color=col,hex=hexc,unit='قطعة',qty=1,width=80,cupo=True,
      spec=[["المقاس","800 × 500 × 400 مم"],["النوع","دولاب مغسلة مكسو بالبلاط"],["المرآة","مرآة LED 600 × 800 مم مع حساس"],["كود البلاط",tile],["الضمان","سنة"]],full=[],img=None,photo=photo('823e60b4-TDS_1.pdf',i,dpi=300,crop=(.545,.115,.825,.447) if i==0 else (.545,.095,.825,.427)),sheet=None,ds=[TP[i]]))

# ---- second batch (user list + datasheets, 2 Nov) ----
CH='#d9dde1'
def gen(cat,code,name,f,spec,hexc=CH,color='كروم',unit='قطعة',**kw):
    d=dict(cat=cat,code=code,name=name,color=color,hex=hexc,unit=unit,qty=1,spec=[["الكود",code]]+spec,full=[],img=None,photo=photo(f,crop=CROPS.get(code)) or enc(pdfium.PdfDocument(A+f)[0].render(scale=200/72).to_pil()),sheet=None,ds=pages(f));d.update(kw);return d
B2=[('mixer','130030410005700','خلاط مغسلة إلكتروني بحساس مزدوج · D50300','d27a4f30-Electronic_Dual_Sensor_Faucet_ArtD503002.pdf',[["التشغيل","حساس إلكتروني مزدوج"]],{}),
 ('mixer','130031150015200','خلاط مغسلة إلكتروني GROHE EUROPLUS E · 36207','58439818-GROHE_Technical_Data_Sheets-130031150015200_36207001.pdf',[["الماركة","GROHE"],["التشغيل","حساس إلكتروني"]],{'tall':False}),
 ('mixer','130331380015200','حنفية ذاتية الإغلاق UT63','46f034e2-130331380015200_UT63_Self_Closing_Tap_TDS_2.pdf',[["النوع","حنفية عمودية ذاتية الإغلاق"]],{}),
 ('mixer','180101010352001','خلاط مغسلة RISE 6.8 سم مع Pop-up · كروم','378c4bba-Rise_WB_6.8.pdf',[["السلسلة","RISE"],["يشمل","صفاية Pop-up"]],{}),
 ('mixer','130030150115200','خلاط مغسلة GROHE PLUS · 3261230D','5062686f-130030150115200_GROHE_Specification_Sheet_3261230D.pdf',[["الماركة","GROHE"],["السلسلة","PLUS"]],{}),
 ('mixer','130030150165200','خلاط مغسلة GROHE EUROSMART 2015 · 33265002','b72fabf3-130030150165200__GROHE_Specification_Sheet_33265002.pdf',[["الماركة","GROHE"],["السلسلة","EUROSMART 2015"]],{}),
 ('shattaf','130220150000100','شطاف GROHE NEW TEMPESTA · 27812IL','1997583a-130220150000100_Specification_Sheet_27812IL1.pdf',[["الماركة","GROHE"]],{}),
 ('shattaf','130220150005200','شطاف GROHE NEW TEMPESTA F · 26354000','3d4c1ab0-GROHE_Technical_Data_Sheets-130220150005200_26354000.pdf',[["الماركة","GROHE"]],{}),
 ('shattaf','130220150015200','شطاف GROHE NEW TEMPESTA F 30 · 27513001','761dd96c-GROHE_Technical_Data_Sheets-130220150015200_27513001_1.pdf',[["الماركة","GROHE"]],{}),
 ('fitting','130160150005200','محبس زاوية GROHE 1/2" · 22940000','1272c311-GROHE_Technical_Data_Sheets-130160150005200_22940000_1.pdf',[["الماركة","GROHE"],["المقاس",'1/2"']],{}),
 ('fitting','130190150005200','سيفون P للمغسلة GROHE 1¼" · 28947000','8e60ab02-GROHE_Specification_Sheet__130190150005200_28947000.pdf',[["الماركة","GROHE"],["المقاس",'1¼"']],{}),
 ('fitting','130191490035200','سيفون قارورة دائري BS181 · 1¼"','463cabc2-130191490035200_BS181.pdf',[["الشكل","دائري"]],{}),
 ('fitting','130191490055200','سيفون قارورة مربع BS190 · 1¼"','7146a7d7-130191490055200_BS190.pdf',[["الشكل","مربع"]],{}),
 ('fitting','130120150060000','سيفون مخفي ثنائي الدفق GROHE RAPID SL · 3872100D','361c90f1-GROHE_Specification_Sheet_3872100D_130120150060000.pdf',[["الماركة","GROHE"],["النوع","خزان دفن ثنائي الدفق"]],{'hex':'#e8e8e6','color':''}),
 ('drain','130581460057800','صفاية أرضية KD-123 · طول 150 مم','c0c52289-KD-123_______Model_1.pdf',[["الطول","150 مم"],["المخرج",'4"']],{}),
 ('acc','130230290205200','علاقة روب E_PLUS · 124503 كروم','6e46424f-E_PLUS_Robe_Hook_124503_Data_Sheet__Specs.pdf',[["السلسلة","E_PLUS"]],{'kind':'hook'}),
 ('acc','130230670195200','مجفف أيدي SANIFLOW بحساس · E88ACS','7be9f817-E88ACS_1.pdf',[["الجهد","220 فولت"],["التشغيل","حساس"]],{'kind':'dryer','hex':'#c4c7cb','color':'ستانلس ساتان'}),
 ('kitchen','180101010352009','خلاط مطبخ RISE فتحة واحدة · كروم','165a5f38-Rise_Single_Hole_Sink.pdf',[["السلسلة","RISE"]],{'kind':'kmixer'}),
 ('kitchen','130061380015200','خلاط مطبخ F90 بدش ثنائي الوظيفة','864f856a-130061380015200_F90_Technical_Data_Sheet.pdf',[["المميزات","دش رش بوظيفتين"]],{'kind':'kmixer'}),
 ('kitchen','130060150265200','خلاط مطبخ GROHE EUROSMART 2015 · 33202002','f1e4f4ea-GROHE_Specification_Sheet_33202002_130060150265200.pdf',[["الماركة","GROHE"]],{'kind':'kmixer'}),
 ('kitchen','130571690009100','حوض مطبخ ستانلس مع مصفّى · LS-6045H','93b3065e-130571690009100.pdf',[["الموديل","LS-6045H"],["النوع","حوض مع مصفّى"]],{'kind':'ksink','hex':'#c9ccd0','color':'ستانلس'}),
 ('basin','121480131010020','مغسلة LOUVRE معلقة · أبيض','e0565f74-Louvre_WB_1H_WH_HPCM-Drawing.pdf',[["النوع","مغسلة معلقة فتحة واحدة"]],{'kind':'wallbasin','w':.5,'hex':'#f4f4f2','color':'أبيض'})]
for cat,code,name,f,spec,kw in B2:
    kw=dict(kw);hexc=kw.pop('hex',CH);col=kw.pop('color','كروم');N.append(gen(cat,code,name,f,spec,hexc=hexc,color=col,**kw))
for n in N:
    if n['code']=='180101010352002':n['name']='خلاط مغسلة RISE 13.6 سم · كروم';n['tall']=True
NEWDS={'130230670405200':'7b541966-AI0113CS.pdf','130230670315200':'38fcbb33-130230670315200__DT2106_NEW_Paper_towel_dis.pdf','130230670225200':'e256a2e1-130230670225200_-_DJ0111CS_Vertical_Liquid_Soap_Dispenser_1.pdf','130230670705200':'5091f641-AI0033CS.pdf','180101010152008':'93220bb6-Cubist_Single_Hole_Sink_2.pdf'}
for n in N:
    if n['code'] in NEWDS:n['ds']=pages(NEWDS[n['code']])

# ---- batch 3 (3 Nov) ----
for cat,code,name,f,spec,kw in [
 ('fitting','130170530015200','فلش ميتر GEM-2 · 137-1.6','1c6ddb41-130170530015200_-_GEM-2_137-1.6_Art3070840.pdf',[["النوع","فلش ميتر مكشوف للكرسي"],["الاستهلاك","1.6 جالون/دفعة"]],{}),
 ('fitting','130170530035200','فلش ميتر ROYAL · 137-1.6','66a8eee9-130170530035200_-_ROYAL_137-1.6_Art3910808.pdf',[["النوع","فلش ميتر يدوي"],["الاستهلاك","1.6 جالون/دفعة"],["التشطيب","كروم لامع"]],{}),
 ('fitting','130120150050000','طقم GROHE RAPID SL 3 في 1 للكرسي · 3874500D','16885b25-GROHE_Technical_Data_Sheets-130120150050000_3874500D_1.pdf',[["الماركة","GROHE"],["النوع","هيكل + خزان دفن + لوحة دفع"],["ارتفاع التركيب","1.13 م"]],{'hex':'#e8e8e6','color':''}),
 ('tile','130941680020100','لاصق بلاط C2TE · 130941680020100','dccf2544-130941680020100.pdf',[["التصنيف","C2TE"]],{'hex':'#bdbdbd','color':''}),
 ('tile','130941680010100','لاصق بلاط C2TE · 130941680010100','f5c64ab3-130941680010100.pdf',[["التصنيف","C2TE"]],{'hex':'#eeeeee','color':''})]:
    kw=dict(kw);hexc=kw.pop('hex',CH);col=kw.pop('color','كروم');N.append(gen(cat,code,name,f,spec,hexc=hexc,color=col,unit='كيس' if cat=='tile' else 'قطعة',**kw))

POST={'130230670225200':(0,.09,1,1),'130571690009300':(.07,0,1,1),'130461734739901':(0,0,1,.955)}
for n in N:
    if n['code'] in POST:
        im=Image.open(io.BytesIO(base64.b64decode(n['photo'].split(',')[1])));x0,y0,x1,y1=POST[n['code']];W,H=im.size;n['photo']=enc(im.crop((int(W*x0),int(H*y0),int(W*x1),int(H*y1))))
    n['img']=n['photo']
json.dump(N,open(X+'new_items.json','w'),ensure_ascii=False)
# datasheets for products already in the catalogue
DS={'121550253010010':pages('05a4348f-Dimension_Sky_WC_3L_25cm_Wash_Down_S-Strap__Floor_Mounted_121550253010010_1.pdf'),'121570265010020':pages('008eb3bb-Infinity_WH_WC_PT_RL_4.5L_HP_-_Drawing.pdf'),'121490131010020':pages('aefc7802-Mirage_WB_1H_WH_HPCM-Drawing.pdf'),'121510133010030':pages('6a0292b5-Spark_WB_1H_Floor_Stand_White_FFC_121510133010030.pdf')}
EWH=pages('18cdff66-SCC_Lot-01_technical_data_sheet_Local-_Vertical__Horizontal_EWH_7.pdf')
json.dump({'code':DS,'ewh':EWH,'guide':pages('130e7c55-Tiles_installation_guide_1.pdf')},open(X+'ds_existing.json','w'))
print(len(N),'new items')
