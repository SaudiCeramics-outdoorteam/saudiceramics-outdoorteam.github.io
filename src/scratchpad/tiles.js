/* ---------- tile catalog: classify by zone, pick size + thickness, apply to the 3D model ---------- */
let TILES=[];const chunkCache={};
const getChunk=n=>chunkCache[n]||(chunkCache[n]=fetch("data/"+n+".json").then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}));
fetch("data/tiles.json").then(r=>r.json()).then(d=>{TILES=d;
  PRODUCTS.forEach(p=>TILES.unshift({code:p.code,src:"fac",name:p.name,cat:"بورسلان",w:60,h:120,t:"2.0",finish:"Matt",faces:String(p.faces),app:"Facade",zones:["facade"],
    pack:{pcs:"1",sqm:"0.72",kg:"35.28",bpp:"32",sqmp:"23.04",kgp:"1,148.96"},thumb:p.thumb,_p:p}));
  if(TZ[selected]||selected==="bath")refreshTilePanel()}).catch(()=>{});
const TZ={ // zone → label, default area, which meshes
  facade:{label:"الواجهة",area:()=>Math.round(FACADE_AREA)},
  court:{label:"الحوش",area:()=>117},
  roof:{label:"السطح",area:()=>184},
  pool:{label:"المسبح",area:()=>51},
  wall:{label:"جدران الحمام",area:()=>16},
  floor:{label:"أرضية الحمام",area:()=>8}};
scene.traverse(o=>{if(o.isMesh)o.userData.origMat=o.material});
bath.traverse(o=>{if(o.isMesh)o.userData.origMat=o.material});
function zoneMeshes(z){
  if(z==="facade")return facadeMeshes;
  const ref={court:zoneMat.court,roof:zoneMat.roof,pool:zoneMat.pool,wall:wallMat,floor:floorMat}[z],out=[];
  scene.traverse(o=>{if(o.isMesh&&o.userData.origMat===ref)out.push(o)});return out}
const tileSel={},tileState={};// per zone: chosen tile, filters + calc
const zstate=z=>tileState[z]||(tileState[z]={size:null,th:null,area:null,waste:10,boxes:null,grout:"130950270000100"});
const sizeKey=t=>`${+t.w}×${+t.h}`;
const loadImg=src=>new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=src});
async function tileTexture(t){
  if(t.src==="fac"){let tx=texCache[t.code];if(!tx){tx=loader.load(t._p.atlas);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.encoding=THREE.sRGBEncoding;tx.anisotropy=8;tx.repeat.set(TEX/4.8,TEX/4.8);texCache[t.code]=tx}return tx}
  if(texCache[t.code])return texCache[t.code];
  const sw=(await getChunk("sw_"+t.sw))[t.code]||[t.thumb],imgs=await Promise.all(sw.map(loadImg));
  const L=Math.max(t.w,t.h),S=Math.min(t.w,t.h),cols=Math.max(1,Math.round(240/L)),rows=Math.max(1,Math.round(240/S));
  const ppc=Math.min(2048/(cols*L),2048/(rows*S)),tw=Math.round(L*ppc),th=Math.round(S*ppc);
  const c=document.createElement("canvas");c.width=cols*tw;c.height=rows*th;const g=c.getContext("2d");
  g.fillStyle="#bdb7ad";g.fillRect(0,0,c.width,c.height);
  for(let r=0;r<rows;r++)for(let k=0;k<cols;k++){const im=imgs[(r*cols+k*7+r*3)%imgs.length],x=k*tw,y=r*th;
    g.save();g.translate(x+tw/2,y+th/2);if((r+k)%2)g.rotate(Math.PI);
    const portrait=im.height>im.width*1.05;if(portrait&&tw>th*1.05)g.rotate(Math.PI/2);
    const dw=portrait&&tw>th*1.05?th:tw,dh=portrait&&tw>th*1.05?tw:th;g.drawImage(im,-dw/2+1,-dh/2+1,dw-2,dh-2);g.restore()}
  const tx=new THREE.CanvasTexture(c);tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.encoding=THREE.sRGBEncoding;tx.anisotropy=8;
  tx.repeat.set(TEX/(cols*L/100),TEX/(rows*S/100));texCache[t.code]=tx;return tx}
async function applyTile(z,t){
  tileSel[z]=t;const ms=zoneMeshes(z);
  if(!t){ms.forEach(o=>o.material=o.userData.origMat||zoneMat.facade);if(z==="facade"){current=null;scaff.forEach(o=>o.visible=true)}paint();refreshTilePanel();return}
  refreshTilePanel();
  try{const tx=await tileTexture(t);if(tileSel[z]!==t)return;
    const indoor=z==="wall"||z==="floor",pol=/polish/i.test(t.finish||"");
    const m=indoor?SM({map:tx,roughness:pol?.12:.5,envMapIntensity:pol?.5:.2}):new THREE.MeshBasicMaterial({map:tx});
    ms.forEach(o=>o.material=m);if(z==="facade"){current=t._p||t;scaff.forEach(o=>o.visible=false)}paint()}
  catch(e){say("ما قدرنا نحمّل صورة البلاطة، حاول مرة ثانية")}}
const tqty=(z,t)=>{const s=zstate(z),area=s.area??TZ[z].area(),per=parseFloat(t.pack.sqm)||1,sug=Math.ceil(area*(1+s.waste/100)/per),boxes=s.boxes??sug;
  return{area,sug,boxes,sqm:boxes*per,kg:boxes*(parseFloat(t.pack.kg)||0),pallets:boxes/(parseFloat(t.pack.bpp)||1)}};
function tileSpec(t){const p=t.pack||{},num=v=>String(v||"").replace(/,/g,"");return[
  ["المقاس",`${+t.w} × ${+t.h} سم`],["السماكة",`${t.t} سم`],["النوع",t.cat==="بورسلان"?"بلاط بورسلان":"بلاط سيراميك"],["التشطيب",t.finish||"-"],
  ...(t.src!=="cer"?[["الحواف","مشطوفة (Rectified)"]]:[]),["الاستخدام",t.app],...(t.faces?[["عدد الوجوه",t.faces]]:[]),
  ["قطع بالكرتون",p.pcs],["م² بالكرتون",p.sqm],["كغ بالكرتون",num(p.kg)],["كرتون بالطبلية",p.bpp],["م² بالطبلية",p.sqmp],["كغ بالطبلية",num(p.kgp)]].filter(r=>r[1])}
async function pageImg(t){if(t.src==="fac")return{sheet:SHEETS["t"+t.code],photo:t._p.photo};
  const d=(await getChunk(t.pg))[String(t.page)];if(!d)return{};
  if(!t._photo){const im=await loadImg(d),c=document.createElement("canvas");c.width=Math.round(im.width/2);c.height=im.height;c.getContext("2d").drawImage(im,0,0);t._photo=c.toDataURL("image/jpeg",.82)}
  return{sheet:d,photo:t._photo}}
let tileHost=null,tileZone=null;
function refreshTilePanel(){if(tileHost&&tileZone)renderTiles(tileHost,tileZone)}
function renderTiles(host,z){tileHost=host;tileZone=z;
  const s=zstate(z),list=TILES.filter(t=>t.zones.includes(z));
  if(!list.length){host.innerHTML=`<p class="fine">جاري تحميل الكتالوج…</p>`;return}
  const sizes=[...new Set(list.map(sizeKey))].sort((a,b)=>eval(a.replace("×","*"))-eval(b.replace("×","*")));
  if(s.size&&!sizes.includes(s.size))s.size=null;
  const bySize=list.filter(t=>!s.size||sizeKey(t)===s.size),ths=[...new Set(bySize.map(t=>t.t))].sort((a,b)=>a-b);
  if(s.th&&!ths.includes(s.th))s.th=null;
  const shown=bySize.filter(t=>!s.th||t.t===s.th),cur=tileSel[z];
  host.innerHTML=`<div class="tfilt"><span>المقاس (سم)</span><div class="chips">${["الكل",...sizes].map(v=>`<button type="button" data-size="${v}" aria-pressed="${(s.size||"الكل")===v}">${v}</button>`).join("")}</div></div>
   <div class="tfilt"><span>السماكة</span><div class="chips">${["الكل",...ths].map(v=>`<button type="button" data-th="${v}" aria-pressed="${(s.th||"الكل")===v}">${v==="الكل"?v:v+" سم"}</button>`).join("")}</div></div>
   <p class="fine" style="margin:6px 0 0">${shown.length} تصميم</p>
   <div class="prods tgrid"><button type="button" class="raw" data-i="-1" aria-pressed="${!cur}">${z==="facade"?"بلوك":"بدون"}</button>${shown.map((t,i)=>`<button type="button" data-i="${i}" aria-pressed="${cur===t}" title="${esc(t.name)} · ${t.code}"><img loading="lazy" alt="${esc(t.name)}" src="${t.thumb}"><span>${esc(t.name.replace(/^Ceramic (Wall|Floor) Tile /,""))}</span></button>`).join("")}</div>
   <div class="spec" id="tspec"></div>`;
  host.querySelectorAll("[data-size]").forEach(b=>b.onclick=()=>{s.size=b.dataset.size==="الكل"?null:b.dataset.size;renderTiles(host,z)});
  host.querySelectorAll("[data-th]").forEach(b=>b.onclick=()=>{s.th=b.dataset.th==="الكل"?null:b.dataset.th;renderTiles(host,z)});
  host.querySelectorAll(".tgrid button").forEach(b=>b.onclick=()=>{const i=+b.dataset.i;s.boxes=null;applyTile(z,i<0?null:shown[i])});
  const sp=host.querySelector("#tspec");
  if(!cur){sp.innerHTML=`<p>اختر المقاس والسماكة ثم التصميم، ويتركب على ${TZ[z].label} مباشرة.</p>`;return}
  const had=inCart(cur.code);
  sp.innerHTML=`<div class="photo ph-wait" id="tPhoto">جاري تحميل صورة المنتج…</div><h3 dir="ltr">${esc(cur.name)}</h3><div class="code">${cur.code}</div>
   <dl>${tileSpec(cur).map(([a,b])=>`<dt>${a}</dt><dd>${esc(b)}</dd>`).join("")}</dl>
   <div class="calc"><h4>حساب الكمية</h4><div class="fields">
     <label for="tArea">مساحة ${TZ[z].label} (م²)<input id="tArea" type="number" min="1" step="0.5" inputmode="decimal" value="${s.area??TZ[z].area()}"></label>
     <label for="tWaste">نسبة الهالك<select id="tWaste">${[5,10,15].map(w=>`<option value="${w}" ${w===s.waste?"selected":""}>${w}%</option>`).join("")}</select></label></div>
     <div class="qtyrow"><span>عدد الكراتين</span><div class="stepper"><button type="button" id="tMinus" aria-label="أنقص">−</button><input id="tBoxes" type="number" min="1" inputmode="numeric" aria-label="عدد الكراتين"><button type="button" id="tPlus" aria-label="زد">+</button></div></div>
     <div class="result" id="tResult"></div></div>
   <div class="row"><button class="btn" id="tAdd">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button><button class="btn ghost" type="button" id="tSheet">ورقة المواصفات</button></div>
   <div class="sugg"><h4>مكملات التركيب المقترحة</h4><div class="grt"><span>لون الترويبة</span><select id="tGrout"><option value="130950270000100">أبيض</option><option value="130950270001400">رمادي</option></select></div>
     <ul id="tSug"></ul><button class="btn ghost" id="tAll">أضف المكملات كلها</button><p class="fine">الكميات تقديرية للمساعدة، ويأكدها الفني حسب طريقة التركيب.</p></div>`;
  pageImg(cur).then(({photo})=>{const ph=document.getElementById("tPhoto");if(!ph||tileSel[z]!==cur)return;
    if(photo){ph.outerHTML=`<img class="photo" id="tPhoto" title="اضغط للتكبير" alt="${esc(cur.name)}" src="${photo}">`;document.getElementById("tPhoto").onclick=()=>zoom(photo,cur.name)}else ph.textContent=""}).catch(()=>{});
  const gS=document.getElementById("tGrout");gS.value=s.grout;
  const sugg=()=>{const A=tqty(z,cur).sqm,big=Math.max(cur.w,cur.h)>=90,pool=z==="pool";
    return[{p:CATby(pool?"130940270030100":"130940270020100")||CATby("130940270020100"),qty:Math.max(1,Math.ceil(A*(big?5:4)/20)),why:`تقدير ${big?5:4} كغ/م²`},
      {p:CATby(s.grout),qty:Math.max(1,Math.ceil(A*.3/20)),why:"تقدير 0.3 كغ/م²"},{p:CATby("130671800000100"),qty:Math.max(1,Math.ceil(A/30)),why:"لفواصل التمدد والزوايا"}].filter(x=>x.p)};
  const drawSug=()=>{const L=sugg();document.getElementById("tSug").innerHTML=L.map((x,i)=>`<li><img alt="" src="${x.p.img}"><div><span dir="ltr">${esc(x.p.name)}</span><small>${fmt(x.qty)} ${x.p.unit} · ${x.why}</small></div><button class="btn ghost sm" data-i="${i}">${inCart(x.p.code)?"✓":"أضف"}</button></li>`).join("");
    document.querySelectorAll("#tSug button").forEach(b=>b.onclick=()=>{const x=sugg()[+b.dataset.i];putCart(catItem(x.p,x.qty,TZ[z].label));drawSug()})};
  const tB=document.getElementById("tBoxes");
  const upd=()=>{const q=tqty(z,cur);tB.value=q.boxes;
    document.getElementById("tResult").innerHTML=`<b>${fmt(q.sqm,2)} م²</b> · ${fmt(q.kg)} كغ · ${fmt(q.pallets,1)} طبلية<br><span>${s.boxes==null?`المقترح: المساحة + ${s.waste}% هالك، مقرّب لأقرب كرتون.`:`المقترح ${fmt(q.sug)} كرتون. <button type="button" class="link" id="tReset">رجّع للمقترح</button>`}</span>`;
    const r=document.getElementById("tReset");if(r)r.onclick=()=>{s.boxes=null;upd()};drawSug()};
  document.getElementById("tArea").oninput=e=>{const v=parseFloat(e.target.value);s.area=v>0?v:null;s.boxes=null;upd()};
  document.getElementById("tWaste").onchange=e=>{s.waste=+e.target.value;s.boxes=null;upd()};
  tB.oninput=()=>{const v=parseInt(tB.value,10);if(v>0){s.boxes=v;upd()}};
  document.getElementById("tMinus").onclick=()=>{s.boxes=Math.max(1,tqty(z,cur).boxes-1);upd()};
  document.getElementById("tPlus").onclick=()=>{s.boxes=tqty(z,cur).boxes+1;upd()};
  gS.onchange=()=>{s.grout=gS.value;drawSug()};
  document.getElementById("tAll").onclick=()=>{sugg().forEach(x=>putCart(catItem(x.p,x.qty,TZ[z].label)));drawSug()};
  document.getElementById("tSheet").onclick=async()=>{const{sheet}=await pageImg(cur);if(sheet)zoom(sheet,cur.name)};
  document.getElementById("tAdd").onclick=()=>{const q=tqty(z,cur);
    cart.filter(i=>i.tz===z&&i.code!==cur.code).forEach(i=>cart.splice(cart.indexOf(i),1));
    putCart({code:cur.code,name:cur.name,color:"",thumb:cur.thumb,tile:cur,zone:TZ[z].label,tz:z,qty:q.boxes,unit:"كرتون",sqmPer:parseFloat(cur.pack.sqm)||0,spec:tileSpec(cur)});refreshTilePanel()};
  upd()}
