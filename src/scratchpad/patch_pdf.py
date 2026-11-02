p='villa-src.html';s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep('<div class="catbar"><span id="catCount"></span><button class="x" id="catClose" aria-label="إغلاق الكتالوج">×</button></div>',
    '<div class="catbar"><span id="catCount"></span><div class="row" style="margin:0"><button class="btn" id="catPdf" hidden>تصدير PDF</button><button class="x" id="catClose" aria-label="إغلاق الكتالوج">×</button></div></div>')
rep('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>',
'''<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>''')
rep('.toast{','''.page.export{position:relative;inset:auto;margin:0;width:1123px;height:794px;max-width:none;transform:none;animation:none;border-radius:0;box-shadow:none;grid-template-columns:1fr 1fr!important;grid-template-rows:none!important}
.page.export.full{grid-template-columns:1fr!important}.page.export .eyebrow{letter-spacing:0}
#exportStage{position:fixed;left:-20000px;top:0;width:1123px;direction:rtl}
.toast{''')
rep('renderProducts();renderCart();\n','''/* PDF export: render each page to an image, assemble an A4-landscape PDF, hand it to the viewer */
const pdfBtn=document.getElementById("catPdf");let dl=null;
Promise.resolve(window.claude&&window.claude.use?window.claude.use("downloads"):null).then(d=>{dl=d;pdfBtn.hidden=!d||!window.jspdf||!window.html2canvas}).catch(()=>{});
pdfBtn.onclick=async()=>{
  if(!dl)return;pdfBtn.disabled=true;const label=pdfBtn.textContent;pdfBtn.textContent="جاري تجهيز الملف…";
  const stage=document.createElement("div");stage.id="exportStage";document.body.appendChild(stage);
  try{
    const pdf=new window.jspdf.jsPDF({orientation:"landscape",unit:"mm",format:"a4"});
    for(let i=0;i<pages.length;i++){
      const el=document.createElement("div");el.className="page export"+(pages[i].startsWith('<div class="body"')?" full":"");el.innerHTML=pages[i];
      stage.innerHTML="";stage.appendChild(el);
      await Promise.all([...el.querySelectorAll("img")].map(im=>im.complete?0:new Promise(r=>{im.onload=im.onerror=r})));
      if(document.fonts&&document.fonts.ready)await document.fonts.ready;
      const cv=await window.html2canvas(el,{scale:2,backgroundColor:"#fbfaf7",logging:false});
      if(i)pdf.addPage();pdf.addImage(cv.toDataURL("image/jpeg",.9),"JPEG",0,0,297,210);
    }
    await dl.save({filename:"كتالوج-اختياراتي-الخزف-السعودي.pdf",data:pdf.output("blob")});
    say("تم حفظ الكتالوج PDF");
  }catch(e){if(!(e&&e.code==="declined"))say(e&&e.code==="unavailable"?"الحفظ غير متاح هنا":"ما قدرنا نجهز الملف، حاول مرة ثانية")}
  finally{stage.remove();pdfBtn.disabled=false;pdfBtn.textContent=label}
};
renderProducts();renderCart();
''')
open(p,'w').write(s)
import json
sp='/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/'
tex=json.load(open(sp+'pdf/tex3.json'));cat=json.load(open(sp+'acc/cat.json'))
meta=[('111157542512016','NAJDI DESIGN'),('111157492512016','SANDY DESERT DARK'),('111156952512016','SANDY DESERT BEIGE'),('111157102512016','ROMAN TRAVERTINE'),('111147342512016','TRAVERTINO CREAM'),('111138692512016','LIMESTONE LIGHT')]
prods=[{'code':c,'name':n,'faces':tex[c]['n'],'sqmBox':0.72,'kgBox':35.28,'boxPallet':32,'atlas':tex[c]['atlas'],'thumb':tex[c]['thumb'],'photo':tex[c]['photo']} for c,n in meta]
s=s.replace('/*__PRODUCTS__*/',json.dumps(prods)).replace('/*__CAT__*/',json.dumps(cat,ensure_ascii=False))
s=s.replace('هنا يختار العميل بلاط الواجهات ويشوف شكل البيت يتغير مباشرة.','اختر بلاطة وشوف الواجهة تتغير مباشرة.')
open('villa-3d.html','w').write(s)
print(round(len(s)/1048576,1),'MB')
