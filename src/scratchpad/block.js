/* ---------- data ---------- */
const PRODUCTS=/*__PRODUCTS__*/;
const CAT=/*__CAT__*/;
const fmt=(n,d=0)=>n.toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d});
const esc=t=>String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const lightbox=document.getElementById("lightbox"),lbImg=document.getElementById("lbImg");
lightbox.onclick=()=>lightbox.hidden=true;
function zoom(src,alt){lbImg.src=src;lbImg.alt=alt||"";lightbox.hidden=false}

/* ---------- cart (shared) ---------- */
const cart=[],cartEl=document.getElementById("cart"),cartBtn=document.getElementById("cartBtn"),toast=document.getElementById("toast");
let toastT;
function say(t){toast.textContent=t;toast.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>toast.hidden=true,1800)}
function putCart(item){
  const ex=cart.find(i=>i.code===item.code);
  if(ex){Object.assign(ex,item);say(`تحدّثت كمية ${item.name}`)}else{cart.push(item);say(`انضاف ${item.name} للسلة`)}
  renderCart();
}
const inCart=code=>cart.find(i=>i.code===code);
function itemLine(it){return `${fmt(it.qty)} ${it.unit}${it.sqmPer?` · ${fmt(it.qty*it.sqmPer,2)} م²`:""}`}
function renderCart(){
  document.getElementById("cartCount").textContent=cart.length;
  const ul=document.getElementById("cartList");ul.innerHTML="";
  document.getElementById("cartEmpty").hidden=cart.length>0;
  document.getElementById("cartFoot").hidden=!cart.length;
  cart.forEach((it,i)=>{const li=document.createElement("li");
    li.innerHTML=`<img alt="" src="${it.thumb}"><div><span dir="ltr">${esc(it.name)}</span><small>${it.zone}${it.color?" · "+it.color:""} · ${itemLine(it)}</small>
      <div class="stepper sm"><button type="button" aria-label="أنقص">−</button><input type="number" min="1" value="${it.qty}" aria-label="كمية ${esc(it.name)}"><button type="button" aria-label="زد">+</button></div></div><button class="x" aria-label="حذف ${esc(it.name)}">×</button>`;
    const [mi,pl]=li.querySelectorAll(".stepper button"),inp=li.querySelector("input");
    mi.onclick=()=>{it.qty=Math.max(1,it.qty-1);renderCart()};pl.onclick=()=>{it.qty++;renderCart()};
    inp.onchange=()=>{const v=parseInt(inp.value,10);if(v>0)it.qty=v;renderCart()};
    li.querySelector(".x").onclick=()=>{cart.splice(i,1);renderCart();if(selected==="bath")renderBath();else renderProducts()};ul.appendChild(li)});
  const n=cart.reduce((a,i)=>a+i.qty,0),sq=cart.reduce((a,i)=>a+(i.sqmPer?i.qty*i.sqmPer:0),0);
  document.getElementById("cartTotal").textContent=`${cart.length} منتج${sq?` · ${fmt(sq,2)} م² بلاط`:""}`;
}
cartBtn.onclick=()=>{cartEl.hidden=!cartEl.hidden;cartBtn.setAttribute("aria-expanded",String(!cartEl.hidden))};

/* ---------- facade tiles ---------- */
const prodBox=document.getElementById("prodBox"),prodsEl=document.getElementById("prods"),specEl=document.getElementById("spec");
const loader=new THREE.TextureLoader(),texCache={};
let finishMat=null;
const calc={area:null,waste:10,boxes:null,grout:"130950270000100"};
function qtyFor(p,area,waste,ov){const sug=Math.ceil(area*(1+waste/100)/p.sqmBox);const boxes=ov??sug;
  return{sug,boxes,sqm:boxes*p.sqmBox,kg:boxes*p.kgBox,pallets:boxes/p.boxPallet}}
const qty=p=>qtyFor(p,calc.area??Math.round(FACADE_AREA),calc.waste,calc.boxes);
const CATby=code=>CAT.find(c=>c.code===code);
function suggestions(){ // estimates for installing large-format porcelain on a facade
  const q=qty(current),A=q.sqm;
  return[
    {p:CATby("130940270020100"),qty:Math.max(1,Math.ceil(A*5/20)),why:"تقدير 5 كغ/م² للبلاط الكبير"},
    {p:CATby(calc.grout),qty:Math.max(1,Math.ceil(A*.3/20)),why:"تقدير 0.3 كغ/م² بفاصل 3 مم"},
    {p:CATby("130671800000100"),qty:Math.max(1,Math.ceil(A/30)),why:"لفواصل التمدد والزوايا"}];
}
function catItem(p,q,zone){return{code:p.code,name:p.name,color:p.color||"",thumb:p.img,photo:p.img,zone,qty:q,unit:p.unit,spec:p.spec}}
function applyProduct(p){
  current=p;
  if(!p){facadeMeshes.forEach(o=>o.material=zoneMat.facade)}
  else{
    let t=texCache[p.code];
    if(!t){t=loader.load(p.atlas);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.encoding=THREE.sRGBEncoding;t.anisotropy=renderer.capabilities.getMaxAnisotropy();
      t.repeat.set(TEX/4.8,TEX/4.8);texCache[p.code]=t}
    if(!finishMat)finishMat=new THREE.MeshBasicMaterial();
    finishMat.map=t;finishMat.needsUpdate=true;
    facadeMeshes.forEach(o=>o.material=finishMat);
  }
  scaff.forEach(o=>o.visible=!p);
  paint();renderProducts();
}
function renderProducts(){
  prodsEl.innerHTML="";
  const raw=document.createElement("button");raw.className="raw";raw.textContent="بلوك";raw.title="بدون تشطيب";
  raw.setAttribute("aria-pressed",String(!current));raw.onclick=()=>applyProduct(null);prodsEl.appendChild(raw);
  PRODUCTS.forEach(p=>{const b=document.createElement("button");b.setAttribute("aria-pressed",String(current===p));b.title=p.name;
    b.innerHTML=`<img alt="${p.name}" src="${p.thumb}">`;b.onclick=()=>applyProduct(p);prodsEl.appendChild(b)});
  if(!current){specEl.innerHTML=`<p>اختر بلاطة من الأعلى وشوف الواجهة تتغير. مساحة الواجهة بالنموذج تقريبًا <b>${fmt(FACADE_AREA)} م²</b>.</p>`;return}
  const had=inCart(current.code);
  specEl.innerHTML=`<img class="photo" title="اضغط للتكبير" alt="صورة ${current.name} من الكتالوج" src="${current.photo}"><h3>${current.name}</h3><div class="code">${current.code}</div>
  <dl><dt>المقاس</dt><dd>60 × 120 × 2.0 سم</dd><dt>النوع</dt><dd>بورسلان مطفي، حواف مشطوفة</dd>
  <dt>الوجوه</dt><dd>${current.faces} وجه مختلف</dd><dt>التعبئة</dt><dd>${current.sqmBox} م² للكرتون · ${current.boxPallet} كرتون للطبلية</dd></dl>
  <div class="calc"><h4>حساب الكمية</h4>
    <div class="fields">
      <label for="cArea">مساحة الواجهة الفعلية (م²)<input id="cArea" type="number" min="1" step="0.5" inputmode="decimal" value="${calc.area??Math.round(FACADE_AREA)}"></label>
      <label for="cWaste">نسبة الهالك<select id="cWaste">${[5,10,15].map(w=>`<option value="${w}" ${w===calc.waste?"selected":""}>${w}%</option>`).join("")}</select></label>
    </div>
    <div class="qtyrow"><span>عدد الكراتين</span>
      <div class="stepper"><button type="button" id="cMinus" aria-label="أنقص">−</button><input id="cBoxes" type="number" min="1" inputmode="numeric" aria-label="عدد الكراتين"><button type="button" id="cPlus" aria-label="زد">+</button></div></div>
    <div class="result" id="cResult"></div>
  </div>
  <div class="row"><button class="btn" id="addCart">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button><a class="btn ghost" href="https://shop.saudiceramics.com/ar/" target="_blank" rel="noopener">المتجر</a></div>
  <div class="sugg"><h4>مكملات التركيب المقترحة</h4>
    <div class="grt"><span>لون الترويبة</span><select id="gSel"><option value="130950270000100">أبيض</option><option value="130950270001400">رمادي</option></select></div>
    <ul id="sugList"></ul><button class="btn ghost" id="addAll">أضف المكملات كلها</button>
    <p class="fine">الكميات تقديرية للمساعدة، ويأكدها الفني حسب طريقة التركيب.</p></div>`;
  const cArea=document.getElementById("cArea"),cWaste=document.getElementById("cWaste"),cBoxes=document.getElementById("cBoxes"),gSel=document.getElementById("gSel");
  gSel.value=calc.grout;
  const drawSug=()=>{document.getElementById("sugList").innerHTML=suggestions().map((s,i)=>`<li><img alt="" src="${s.p.img}"><div><span dir="ltr">${esc(s.p.name)}</span><small>${fmt(s.qty)} ${s.p.unit} · ${s.why}</small></div><button class="btn ghost sm" data-i="${i}">${inCart(s.p.code)?"✓":"أضف"}</button></li>`).join("");
    document.querySelectorAll("#sugList button").forEach(b=>b.onclick=()=>{const s=suggestions()[+b.dataset.i];putCart(catItem(s.p,s.qty,"الواجهة"));drawSug()})};
  const upd=()=>{const q=qty(current);cBoxes.value=q.boxes;
    document.getElementById("cResult").innerHTML=`<b>${fmt(q.sqm,2)} م²</b> · ${fmt(q.kg)} كغ · ${fmt(q.pallets,1)} طبلية<br><span>${calc.boxes==null?`المقترح: المساحة + ${calc.waste}% هالك، مقرّب لأقرب كرتون.`:`المقترح ${fmt(q.sug)} كرتون. <button type="button" class="link" id="cReset">رجّع للمقترح</button>`}</span>`;
    const r=document.getElementById("cReset");if(r)r.onclick=()=>{calc.boxes=null;upd()};drawSug()};
  cArea.oninput=()=>{const v=parseFloat(cArea.value);calc.area=v>0?v:null;calc.boxes=null;upd()};
  cWaste.onchange=()=>{calc.waste=+cWaste.value;calc.boxes=null;upd()};
  cBoxes.oninput=()=>{const v=parseInt(cBoxes.value,10);if(v>0){calc.boxes=v;upd()}};
  document.getElementById("cMinus").onclick=()=>{calc.boxes=Math.max(1,qty(current).boxes-1);upd()};
  document.getElementById("cPlus").onclick=()=>{calc.boxes=qty(current).boxes+1;upd()};
  gSel.onchange=()=>{calc.grout=gSel.value;drawSug()};
  document.getElementById("addAll").onclick=()=>{suggestions().forEach(s=>putCart(catItem(s.p,s.qty,"الواجهة")));drawSug()};
  upd();
  document.getElementById("addCart").onclick=()=>{const q=qty(current);
    putCart({code:current.code,name:current.name,color:"",thumb:current.thumb,photo:current.photo,zone:"الواجهة",qty:q.boxes,unit:"كرتون",sqmPer:current.sqmBox,
      spec:[["المقاس","60 × 120 × 2.0 سم"],["النوع","بورسلان مطفي"],["الحواف","مشطوفة (Rectified)"],["الوجوه",current.faces+" وجه"],["التعبئة",current.sqmBox+" م² للكرتون"]]});renderProducts()};
  specEl.querySelector(".photo").onclick=()=>zoom(current.photo,current.name);
}

/* ---------- bathroom (interior) ---------- */
const BX=70,bath=new THREE.Group();bath.position.set(BX,0,0);bath.visible=false;scene.add(bath);
const envTex=(()=>{const pm=new THREE.PMREMGenerator(renderer),es=new THREE.Scene();
  es.add(new THREE.Mesh(new THREE.BoxGeometry(12,8,12),new THREE.MeshBasicMaterial({color:0x8d9196,side:THREE.BackSide})));
  const lm=new THREE.MeshBasicMaterial({color:0xffffff});
  [[0,3.9,0,-Math.PI/2,0,8,3],[-5.9,1.5,0,0,Math.PI/2,6,2],[0,1,5.9,0,Math.PI,8,1.2]].forEach(([x,y,z,rx,ry,w,h])=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),lm);m.position.set(x,y,z);m.rotation.set(rx,ry,0);es.add(m)});
  es.add(new THREE.Mesh(new THREE.BoxGeometry(12,.1,12),new THREE.MeshBasicMaterial({color:0x3a3c40})).translateY(-3.9));
  return pm.fromScene(es,.03).texture})();
const tileTex=(c1,c2,w,h)=>canvasTex((g,s)=>{g.fillStyle=c1;g.fillRect(0,0,s,s);speckle(g,s,1200,215,14);g.strokeStyle=c2;g.lineWidth=2;
  for(let x=0;x<=s;x+=s/w){g.beginPath();g.moveTo(x,0);g.lineTo(x,s);g.stroke()}for(let y=0;y<=s;y+=s/h){g.beginPath();g.moveTo(0,y);g.lineTo(s,y);g.stroke()}},512);
const wallT=tileTex("#ece8e1","#d6d1c8",2,1),floorT=tileTex("#c9c4bb","#aaa49a",1,2);
const SM=(o)=>{const m=new THREE.MeshStandardMaterial(Object.assign({roughness:.6,metalness:0},o));m.envMap=envTex;m.envMapIntensity=.6;return m};
const wallMat=SM({map:wallT,roughness:.35}),floorMat=SM({map:floorT,roughness:.5}),ceramic=SM({color:0xf6f6f3,roughness:.12,envMapIntensity:.9}),dark=SM({color:0x1b1c1e,roughness:.3});
function finish(hex){const c=new THREE.Color(hex),hsl={};c.getHSL(hsl);const matt=/[67]/.test(hex)||hsl.l<.2||hex==="#c4a463"||hex==="#bdb6aa"||hex==="#5d5f62"||hex==="#c9cbcc";
  const m=SM({color:c,metalness:hsl.l<.2?.5:.95,roughness:matt?.42:.12});m.envMapIntensity=1.2;return m}
const bMesh=(geo,mat,x,y,z,cat,parent=bath)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;m.userData.zone="bath";if(cat)m.userData.cat=cat;parent.add(m);pickables.push(m);return m};
const B=(w,h,d,mat,x,y,z,cat,parent)=>{const g=new THREE.BoxGeometry(w,h,d);scaleUV(g,w,h,d);return bMesh(g,mat,x,y+h/2,z,cat,parent)};
/* room shell: 3.2 x 2.6 x 2.8, open toward +x and +z */
const RW=3.2,RD=2.6,RH=2.8,X0=-RW/2,Z0=-RD/2;
wallT.repeat.set(1/.6*TEX/2,1/.6*TEX/2);floorT.repeat.set(1/.6*TEX/2,1/.6*TEX/2);
B(RW,.1,RD,floorMat,0,-.1,0);B(RW,RH,.12,wallMat,0,0,Z0-.06);B(.12,RH,RD,wallMat,X0-.06,0,0);
B(RW+.12,.04,.16,dark,0,RH,Z0-.02);
const roomLight=new THREE.PointLight(0xfff4e6,.9,7,1.6);roomLight.position.set(0,2.5,.2);bath.add(roomLight);
/* groups rebuilt per selection */
const G={};["vanity","mixer","mirror","toilet","shattaf","shower","acc","drain"].forEach(k=>{G[k]=new THREE.Group();bath.add(G[k])});
const clear=g=>{g.children.slice().forEach(c=>{g.remove(c);const i=pickables.indexOf(c);if(i>-1)pickables.splice(i,1);if(c.children)c.children.forEach(cc=>{const j=pickables.indexOf(cc);if(j>-1)pickables.splice(j,1)})})};
const cyl=(r,h,seg=24)=>new THREE.CylinderGeometry(r,r,h,seg);
const VX=-.55;
const build={
  vanity(p){const g=G.vanity;clear(g);const w=p.width/100,mat=SM({color:new THREE.Color(p.hex),roughness:.55});
    B(w,.46,.46,mat,VX,.38,Z0+.23,"vanity",g);B(w+.02,.05,.48,ceramic,VX,.84,Z0+.24,"vanity",g);
    const bw=Math.min(.5,w*.62);B(bw,.012,.3,SM({color:0xe9e9e6,roughness:.2}),VX,.885,Z0+.25,"vanity",g);
    B(w-.04,.004,.003,dark,VX,.6,Z0+.462,"vanity",g);build.mixer(bathSel.mixer);build.mirror(bathSel.mirror)},
  mixer(p){const g=G.mixer;clear(g);const m=finish(p.hex),y=.89,z=Z0+.08;
    bMesh(cyl(.024,.17),m,VX,y+.085,z,"mixer",g);const sp=B(.03,.022,.12,m,VX,y+.15,z+.07,"mixer",g);
    const lv=B(.018,.012,.085,m,VX,y+.18,z-.01,"mixer",g);lv.rotation.x=-.35;sp.rotation.x=.08;},
  mirror(p){const g=G.mirror;clear(g);const w=bathSel.vanity.width/100,y=1.6,z=Z0+.012;
    const glass=SM({color:0xdfe6ea,metalness:1,roughness:.04});glass.envMapIntensity=1.4;
    const led=SM({color:0xfff3d6,emissive:0xfff0cc,emissiveIntensity:p.led?1.1:.7});
    if(p.shape==="round"){const r=Math.min(.38,w*.45);
      bMesh(new THREE.CircleGeometry(r+.025,64),p.led?led:dark,VX,y,z-.002,"mirror",g);
      if(!p.led)bMesh(new THREE.RingGeometry(r-.03,r-.018,64),led,VX,y,z+.003,"mirror",g);
      bMesh(new THREE.CircleGeometry(r,64),glass,VX,y,z,"mirror",g)}
    else{const mw=Math.min(1,Math.max(.6,w*.9)),mh=.7;
      bMesh(new THREE.PlaneGeometry(mw+.05,mh+.05),p.led?led:dark,VX,y,z-.002,"mirror",g);
      if(!p.led)bMesh(new THREE.PlaneGeometry(mw-.06,mh-.06),led,VX,y,z+.001,"mirror",g);
      bMesh(new THREE.PlaneGeometry(p.led?mw:mw-.09,p.led?mh:mh-.09),glass,VX,y,z+.003,"mirror",g)}},
  toilet(p){const g=G.toilet;clear(g);const x=X0,z=.25;
    const bowl=bMesh(new THREE.CylinderGeometry(.2,.17,.4,40),ceramic,x+.42,.2,z,"toilet",g);bowl.scale.set(1.35,1,1);
    const seat=bMesh(new THREE.CylinderGeometry(.205,.205,.035,40),ceramic,x+.43,.42,z,"toilet",g);seat.scale.set(1.35,1,1);
    if(p.smart){B(.26,.36,.42,ceramic,x+.16,0,z,"toilet",g);B(.2,.03,.36,ceramic,x+.16,.36,z,"toilet",g);B(.06,.012,.03,dark,x+.16,.392,z+.12,"toilet",g)}
    else{B(.2,.42,.4,ceramic,x+.12,0,z,"toilet",g);B(.16,.36,.44,ceramic,x+.1,.42,z,"toilet",g);bMesh(cyl(.025,.01),finish("#d9dde1"),x+.1,.785,z,"toilet",g)}},
  shattaf(p){const g=G.shattaf;clear(g);const m=finish(p.hex),x=X0+.02,z=.72;
    B(.03,.07,.05,m,x,.55,z,"shattaf",g);const h=bMesh(cyl(.016,.13),m,x+.05,.6,z,"shattaf",g);h.rotation.z=.5;
    const hose=bMesh(new THREE.TorusGeometry(.12,.007,8,40,Math.PI*1.3),SM({color:0xc9ccce,metalness:.9,roughness:.3}),x+.03,.42,z,"shattaf",g);hose.rotation.y=Math.PI/2},
  shower(p){const g=G.shower;clear(g);const m=finish(p.hex),x=1.1,z=Z0+.05;
    bMesh(cyl(.013,1.15),m,x,1.5,z,"shower",g);const arm=bMesh(cyl(.011,.32),m,x,2.06,z+.16,"shower",g);arm.rotation.x=Math.PI/2;
    bMesh(cyl(.1,.014,48),m,x,2.04,z+.32,"shower",g);B(.16,.07,.06,m,x,.9,z+.01,"shower",g);B(.03,.02,.08,m,x+.05,.97,z+.05,"shower",g);
    const hs=bMesh(cyl(.02,.2),m,x+.06,1.45,z+.04,"shower",g);hs.rotation.z=-.2;bMesh(cyl(.035,.03),m,x+.08,1.56,z+.05,"shower",g);
    const glass=new THREE.MeshStandardMaterial({color:0xd9eef0,transparent:true,opacity:.16,roughness:.05,metalness:0,depthWrite:false});
    const gl=B(.01,2,.95,glass,.55,0,Z0+.48,null,g);gl.userData.pass=true;B(.02,.02,.95,m,.55,2,Z0+.48,"shower",g).userData.pass=true},
  acc(p){const g=G.acc;clear(g);const m=finish(p.hex),x=X0+.03;
    const bar=bMesh(cyl(.011,.6),m,x+.04,1.2,-.75,"acc",g);bar.rotation.x=Math.PI/2;[-1.04,-.46].forEach(z=>B(.06,.03,.03,m,x+.01,1.185,z,"acc",g));
    const ring=bMesh(new THREE.TorusGeometry(.08,.008,10,40),m,x+.03,1.05,.95,"acc",g);ring.rotation.y=Math.PI/2;
    const roll=bMesh(cyl(.012,.12),m,x+.07,.68,.6,"acc",g);roll.rotation.x=Math.PI/2;bMesh(cyl(.06,.1),SM({color:0xfafafa,roughness:.9}),x+.08,.62,.6,"acc",g).rotation.x=Math.PI/2},
  drain(p){const g=G.drain;clear(g);B(.15,.006,.15,finish(p.hex),1.1,.0,-.75,"drain",g)}
};
const BCATS=[["vanity","المغسلة والدولاب"],["mixer","خلاط المغسلة"],["mirror","المرآة"],["shower","عمود الدش"],["toilet","الكرسي"],["shattaf","الشطاف"],["acc","الإكسسوارات"],["drain","الصفاية"]];
const bathSel={};BCATS.forEach(([k])=>bathSel[k]=CAT.find(c=>c.cat===k));
bathSel.vanity=CAT.find(c=>c.code==="130321270004700");
["vanity","toilet","shattaf","shower","acc","drain"].forEach(k=>build[k](bathSel[k]));
let bathCat="mixer";
const bathBox=document.getElementById("bathBox");
function renderBath(){
  const bc=document.getElementById("bcats"),bp=document.getElementById("bprods"),bs=document.getElementById("bspec");
  bc.innerHTML=BCATS.map(([k,l])=>`<button type="button" data-k="${k}" aria-pressed="${k===bathCat}">${l}${cart.some(i=>i.bcat===k)?" ✓":""}</button>`).join("");
  bc.querySelectorAll("button").forEach(b=>b.onclick=()=>{bathCat=b.dataset.k;renderBath()});
  const list=CAT.filter(c=>c.cat===bathCat),cur=bathSel[bathCat];
  bp.innerHTML="";bp.className="prods sq";
  list.forEach(p=>{const b=document.createElement("button");b.setAttribute("aria-pressed",String(p===cur));b.title=p.name+(p.color?" · "+p.color:"");
    b.innerHTML=`<img alt="${esc(p.name)}" src="${p.img}">`;b.onclick=()=>{bathSel[bathCat]=p;build[bathCat](p);renderBath()};bp.appendChild(b)});
  const had=inCart(cur.code);let q=had?had.qty:1;
  bs.innerHTML=`<img class="photo pimg" title="اضغط للتكبير" alt="${esc(cur.name)}" src="${cur.img}"><h3>${esc(cur.name)}</h3><div class="code">${cur.code}</div>
   <dl>${cur.color?`<dt>اللون</dt><dd>${cur.color}</dd>`:""}${cur.spec.map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join("")}</dl>
   <div class="qtyrow"><span>الكمية (${cur.unit})</span><div class="stepper"><button type="button" id="bMinus" aria-label="أنقص">−</button><input id="bQty" type="number" min="1" value="${q}" aria-label="الكمية"><button type="button" id="bPlus" aria-label="زد">+</button></div></div>
   <div class="row"><button class="btn" id="bAdd">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button></div>`;
  const bq=document.getElementById("bQty");
  document.getElementById("bMinus").onclick=()=>bq.value=Math.max(1,(+bq.value||1)-1);
  document.getElementById("bPlus").onclick=()=>bq.value=(+bq.value||0)+1;
  document.getElementById("bAdd").onclick=()=>{
    cart.filter(i=>i.bcat===bathCat&&i.code!==cur.code&&!["acc","drain"].includes(bathCat)).forEach(i=>cart.splice(cart.indexOf(i),1));
    putCart(Object.assign(catItem(cur,Math.max(1,parseInt(bq.value,10)||1),"الحمام"),{bcat:bathCat}));renderBath()};
  bs.querySelector(".photo").onclick=()=>zoom(cur.img,cur.name);
}
let saved=null;
function setBathMode(on){
  if(on===bath.visible)return;
  bath.visible=on;
  if(on){saved={a:[controls.minAzimuthAngle,controls.maxAzimuthAngle],d:[controls.minDistance,controls.maxDistance],p:controls.maxPolarAngle};
    controls.minDistance=1.6;controls.maxDistance=6.5;controls.minAzimuthAngle=.05;controls.maxAzimuthAngle=1.5;controls.maxPolarAngle=1.5;controls.autoRotate=false}
  else if(saved){[controls.minAzimuthAngle,controls.maxAzimuthAngle]=saved.a;[controls.minDistance,controls.maxDistance]=saved.d;controls.maxPolarAngle=saved.p}
}

/* ---------- catalog: one page per product (from its image) + quantities page ---------- */
const catEl=document.getElementById("catalog"),book=document.getElementById("book");
let pages=[],pi=0;
function buildPages(){
  const out=[];
  cart.forEach((it,i)=>{
    out.push(`<div class="media"><img alt="${esc(it.name)}" src="${it.photo}"></div>
    <div class="body"><span class="eyebrow">${it.zone} · منتج ${i+1} من ${cart.length}</span><h3>${esc(it.name)}</h3><div class="code">${it.code}</div>
    <table>${it.color?`<tr><td>اللون</td><td>${it.color}</td></tr>`:""}${it.spec.map(([a,b])=>`<tr><td>${a}</td><td>${b}</td></tr>`).join("")}</table>
    <div class="big"><div><b>${fmt(it.qty)}</b><span>${it.unit}</span></div>${it.sqmPer?`<div><b>${fmt(it.qty*it.sqmPer,2)}</b><span>م²</span></div>`:""}</div></div>`)});
  out.push(`<div class="body"><span class="eyebrow">ملخص الطلب</span><h2>الكميات المختارة</h2>
   <div style="overflow-x:auto"><table><tr><th>المنتج</th><th>المنطقة</th><th>الكمية</th></tr>
   ${cart.map(it=>`<tr><td dir="ltr" style="text-align:right">${esc(it.name)}<br><small style="color:#6b6457">${it.code}</small></td><td>${it.zone}</td><td>${itemLine(it)}</td></tr>`).join("")}
   </table></div>
   <p class="note">كميات البلاط محسوبة على المساحة اللي أدخلها العميل مع نسبة الهالك. كميات المكملات تقديرية. للتأكيد النهائي يُراجع المخطط مع مندوب المبيعات.</p></div>`);
  return out;
}
function show(i,dir){
  const old=book.querySelector(".page");pi=i;
  const pg=document.createElement("div");pg.className="page"+(pages[i].startsWith('<div class="body"')?" full":"");pg.innerHTML=pages[i];
  if(old&&dir){old.style.zIndex=2;old.classList.add(dir>0?"turn-out":"turn-back-out");pg.classList.add(dir>0?"turn-in":"turn-back-in");
    book.insertBefore(pg,old);setTimeout(()=>old.remove(),reduce?0:560)}
  else{book.innerHTML="";book.appendChild(pg)}
  document.getElementById("catCount").textContent=`صفحة ${i+1} من ${pages.length}`;
  document.getElementById("catDots").innerHTML=pages.map((_,k)=>`<i class="${k===i?"on":""}"></i>`).join("");
  document.getElementById("catPrev").disabled=i===0;document.getElementById("catNext").disabled=i===pages.length-1;
}
const go=d=>{const n=pi+d;if(n>=0&&n<pages.length)show(n,d)};
document.getElementById("openCat").onclick=()=>{pages=buildPages();catEl.hidden=false;cartEl.hidden=true;cartBtn.setAttribute("aria-expanded","false");show(0)};
document.getElementById("catClose").onclick=()=>catEl.hidden=true;
document.getElementById("catNext").onclick=()=>go(1);document.getElementById("catPrev").onclick=()=>go(-1);
addEventListener("keydown",e=>{if(e.key==="Escape"){lightbox.hidden=true;if(!catEl.hidden)catEl.hidden=true}if(catEl.hidden)return;if(e.key==="ArrowLeft")go(1);if(e.key==="ArrowRight")go(-1)});
let swX=null;book.addEventListener("pointerdown",e=>swX=e.clientX);book.addEventListener("pointerup",e=>{if(swX==null)return;const dx=e.clientX-swX;swX=null;if(Math.abs(dx)>50)go(dx>0?1:-1)});
renderProducts();renderCart();
