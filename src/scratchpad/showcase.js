/* ---------- "عرض تصميمي": cinematic tour of the customer's finished house, one shot per chosen product ---------- */
{
const sc=document.createElement("div");sc.id="showcase";sc.hidden=true;sc.setAttribute("role","dialog");sc.setAttribute("aria-label","عرض تصميمي");
sc.innerHTML=`<div class="scfade"></div><div class="sctop"><div class="scbrand"><img src="img/logo.png" alt="الخزف السعودي"><span>شطّب بيتك وأنت مطمّن</span></div><div class="sccount" id="scCount"></div><button class="scx" id="scX" aria-label="إغلاق العرض">✕</button></div>
<div class="scinfo"><div class="sctext"><span class="sceye" id="scEye"></span><h2 id="scTitle"></h2><p id="scSub"></p></div><figure class="sccard" id="scCard" hidden><img id="scImg" alt=""></figure></div>
<div class="scend" id="scEnd" hidden><span class="sceye">تصميمك جاهز</span><h2 id="scEndT"></h2><p>كل المنتجات اللي اخترتها مركّبة على بيتك. صدّر الكتالوج وأرسله لمندوب المبيعات.</p><div class="row"><button class="btn" id="scCat">اعرض الكتالوج وصدّر PDF</button><button class="btn ghost" id="scAgain">أعد العرض</button></div></div>
<div class="scbar"><button id="scPrev" aria-label="السابق">›</button><button id="scPlay" aria-label="إيقاف مؤقت">❚❚</button><button id="scNext" aria-label="التالي">‹</button><div class="scprog"><i id="scProg"></i></div></div>`;
document.getElementById("app").appendChild(sc);
const css=document.createElement("style");css.textContent=`
#showcase{position:fixed;inset:0;z-index:60;pointer-events:none;color:#f4efe6;font-family:var(--body)}
#showcase>*{pointer-events:auto}
#showcase .scfade{position:absolute;inset:0;background:#07090c;opacity:0;transition:opacity .45s;pointer-events:none}
#showcase.dark .scfade{opacity:1}
#showcase::before{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(7,9,12,.75) 0,rgba(7,9,12,0) 18%,rgba(7,9,12,0) 55%,rgba(7,9,12,.85) 100%)}
.sctop{position:absolute;top:0;inset-inline:0;display:flex;align-items:center;gap:14px;padding:14px 20px;border-bottom:1px solid rgba(244,239,230,.14)}
.scbrand{display:flex;align-items:center;gap:10px;flex:1;font:500 13px var(--body);letter-spacing:.02em;color:rgba(244,239,230,.8)}
.scbrand img{height:30px;filter:invert(1)}
.sccount{font:500 12px var(--body);letter-spacing:.18em;color:rgba(244,239,230,.7);font-variant-numeric:tabular-nums}
.scx{background:none;border:1px solid rgba(244,239,230,.3);color:#f4efe6;width:34px;height:34px;border-radius:50%;cursor:pointer}
.scinfo{position:absolute;bottom:74px;inset-inline:24px;display:flex;align-items:flex-end;gap:20px;pointer-events:none}
.sctext{flex:1;min-width:0}
.sceye{display:block;font:600 11px var(--body);letter-spacing:.22em;text-transform:uppercase;color:#d8b98a;margin-bottom:6px}
#showcase h2{font:400 clamp(24px,4vw,44px)/1.15 var(--display);margin:0;color:#fbf7f0;text-wrap:balance}
#scSub{margin:6px 0 0;font:400 13px var(--body);color:rgba(244,239,230,.75);direction:ltr;text-align:right}
.sccard{margin:0;background:#fbfaf7;border-radius:6px;padding:8px;width:clamp(120px,18vw,210px);box-shadow:0 18px 40px rgba(0,0,0,.45);transform:translateY(0);transition:opacity .5s,transform .5s}
.sccard img{display:block;width:100%;aspect-ratio:1;object-fit:contain}
.scend{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;background:rgba(7,9,12,.72)}
.scend p{max-width:460px;color:rgba(244,239,230,.8);line-height:1.7}
.scend .btn.ghost{color:#f4efe6;border-color:rgba(244,239,230,.5)}
.scbar{position:absolute;bottom:0;inset-inline:0;display:flex;align-items:center;gap:8px;padding:14px 20px;border-top:1px solid rgba(244,239,230,.14)}
.scbar button{background:none;border:1px solid rgba(244,239,230,.3);color:#f4efe6;width:38px;height:38px;border-radius:50%;cursor:pointer;font-size:16px}
.scprog{flex:1;height:2px;background:rgba(244,239,230,.18);margin-inline-start:10px}
.scprog i{display:block;height:100%;width:0;background:#d8b98a}
@media (max-width:760px){.scinfo{flex-direction:column;align-items:flex-start;bottom:70px;inset-inline:16px}.sccard{width:110px;order:-1}.sctop{padding:10px 14px}.scbrand span{display:none}}
@media (prefers-reduced-motion:reduce){#showcase .scfade{transition:none}}`;
document.head.appendChild(css);
const V=(a)=>new THREE.Vector3(...a);
const ZN={facade:"الواجهة",court:"الحوش",roof:"السطح",pool:"المسبح",stairs:"الدرج",lfloor:"داخل البيت",lwall:"داخل البيت",lall:"داخل البيت",wall:"دورة المياه",floor:"دورة المياه",ball:"دورة المياه"};
const BN={vanity:"المغسلة",mixer:"خلاط المغسلة",mirror:"المرآة",shower:"الدش",toilet:"الكرسي",shattaf:"الشطاف",acc:"الإكسسوارات",drain:"الصفاية",heater:"السخان",bathing:"البانيو",fitting:"المحابس والسيفونات",kitchen:"المطبخ"};
let shots=[],si=0,playing=true,t0=0,raf=0,saved=null;
function setMode(m){bath.visible=m==="bath";living.visible=m==="living";hemi.intensity=m==="out"?.85:m==="bath"?.5:.58;sun.intensity=m==="out"?.8:.25}
function boxOf(obj){const b=new THREE.Box3().setFromObject(obj);return b.isEmpty()?null:b}
function shotFor(it){const p=CAT.find(c=>c.code===it.code);
  if(it.tz&&ZONES[it.tz]&&["facade","court","roof","pool"].includes(it.tz)){const Z=ZONES[it.tz];return{mode:"out",to:V(Z.target),from:V(Z.pos)}}
  if(it.tz==="stairs")return{mode:"living",from:V([LX-1.9,1.7,1.5]),to:V([LX+1.0,1.0,LZ0+.6])};
  if(it.tz&&/^l/.test(it.tz))return{mode:"living",from:V([LX+4.4,3.4,6.2]),to:V([LX-.7,.8,-.7])};
  if(it.tz||(it.bcat&&/^b(wall|floor|all)$/.test(it.bcat)))return{mode:"bath",from:V([BX+3.4,1.95,3.4]),to:V([BX+.65,1.05,-.4])};
  if(it.bcat==="heater"&&p&&["solar","central"].includes(p.kind)){try{bathSel.heater=p;build.heater(p)}catch(e){}const b=boxOf(solarG);if(b){const c=b.getCenter(new THREE.Vector3());return{mode:"out",to:c,from:c.clone().add(new THREE.Vector3(3.4,2.4,5.6))}}}
  if(it.bcat&&G[it.bcat]){try{if(p&&it.bcat!=="bathing"){bathSel[it.bcat]=p;build[it.bcat](p)}}catch(e){}const b=boxOf(G[it.bcat]);
    if(b){const c=b.getCenter(new THREE.Vector3()),s=b.getSize(new THREE.Vector3()),d=Math.max(.9,Math.max(s.x,s.y,s.z)*2.2);return{mode:"bath",to:c,from:c.clone().add(new THREE.Vector3(d*.75,d*.35,d*.9))}}}
  return{mode:"out",from:V([22,15,24]),to:V([0,3,1]),photoOnly:true}}
function build_(){const who=CUSTOMER?CUSTOMER.name:"";shots=[{mode:"out",from:V([30,17,30]),to:V([0,3,1]),orbit:.5,title:who?`بيت ${who}`:"بيتك بعد التشطيب",eye:"عرض تصميمي",sub:`${cart.length} منتج من الخزف السعودي`}];
  cart.forEach(it=>{const s=shotFor(it);s.title=it.name;s.eye=ZN[it.tz]||BN[it.bcat]||it.zone||"";s.sub=it.code+(it.qty?` · ${it.qty} ${it.unit||""}`:"");s.img=it.photo||it.thumb;shots.push(s)});
  shots.push({mode:"out",from:V([24,9,26]),to:V([0,3,1]),orbit:.8,end:true})}
function look(s,k){const off=s.from.clone().sub(s.to),ang=(s.orbit??.22)*(k-.5),c=Math.cos(ang),n=Math.sin(ang);
  const o=new THREE.Vector3(off.x*c-off.z*n,off.y,off.x*n+off.z*c).multiplyScalar(1.12-.14*ease(k));camera.position.copy(s.to).add(o);controls.target.copy(s.to);camera.lookAt(s.to)}
const $=id=>document.getElementById(id),DUR=4600;
function show(i){si=(i+shots.length)%shots.length;const s=shots[si];sc.classList.add("dark");
  setTimeout(()=>{setMode(s.mode);look(s,0);$("scEnd").hidden=!s.end;$("scEye").textContent=s.eye||"";$("scTitle").textContent=s.title||"";$("scSub").textContent=s.sub||"";
    $("scEndT").textContent=CUSTOMER?`بيت ${CUSTOMER.name}`:"بيتك";const card=$("scCard");if(s.img){$("scImg").src=s.img;card.hidden=false}else card.hidden=true;
    $("scCount").textContent=`${String(si+1).padStart(2,"0")} / ${String(shots.length).padStart(2,"0")}`;t0=performance.now();sc.classList.remove("dark")},reduce?0:420)}
function tick(now){raf=requestAnimationFrame(tick);if(sc.hidden)return;const s=shots[si];if(!s)return;const k=Math.min(1,(now-t0)/DUR);
  if(!sc.classList.contains("dark"))look(s,reduce?1:k);$("scProg").style.width=((si+k)/shots.length*100)+"%";
  if(k>=1&&playing&&!s.end)show(si+1)}
function open(){if(!cart.length){try{say("أضف منتجات للسلة أول، وبعدها شوف عرض تصميمك")}catch(e){}return}
  saved={p:camera.position.clone(),t:controls.target.clone(),bv:bath.visible,lv:living.visible,hi:hemi.intensity,su:sun.intensity,tm:renderer.toneMapping,te:renderer.toneMappingExposure,sel};
  try{cartEl.hidden=true;document.getElementById("houseView").hidden=true}catch(e){}
  anim=null;controls.enabled=false;controls.autoRotate=false;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;scene.traverse(o=>{if(o.material)[].concat(o.material).forEach(m=>m.needsUpdate=true)});
  selected=null;hovered=null;try{paint()}catch(e){}
  build_();playing=true;$("scPlay").textContent="❚❚";sc.hidden=false;document.body.classList.add("showing");show(0);if(!raf)raf=requestAnimationFrame(tick)}
const sel=null;
function close(){sc.hidden=true;document.body.classList.remove("showing");controls.enabled=true;renderer.toneMapping=saved.tm;renderer.toneMappingExposure=saved.te;scene.traverse(o=>{if(o.material)[].concat(o.material).forEach(m=>m.needsUpdate=true)});
  bath.visible=saved.bv;living.visible=saved.lv;hemi.intensity=saved.hi;sun.intensity=saved.su;camera.position.copy(saved.p);controls.target.copy(saved.t);controls.update();try{select("all")}catch(e){}}
$("scX").onclick=close;$("scNext").onclick=()=>show(si+1);$("scPrev").onclick=()=>show(si-1);
$("scPlay").onclick=()=>{playing=!playing;$("scPlay").textContent=playing?"❚❚":"▶";$("scPlay").setAttribute("aria-label",playing?"إيقاف مؤقت":"تشغيل");if(playing)t0=performance.now()};
$("scAgain").onclick=()=>show(0);$("scCat").onclick=()=>{close();document.getElementById("openCat").click()};
addEventListener("keydown",e=>{if(sc.hidden)return;if(e.key==="Escape")close();if(e.key==="ArrowLeft")show(si+1);if(e.key==="ArrowRight")show(si-1)});
window.openShowcase=open;
{const b=document.createElement("button");b.className="btn";b.type="button";b.id="scOpen";b.textContent="اعرض تصميمي 3D";b.onclick=open;document.getElementById("openCat").before(b)}
{const b=document.createElement("button");b.className="btn ghost";b.type="button";b.textContent="عرض تصميمي";b.onclick=open;const h=document.getElementById("houseBtn");if(h)h.after(b)}
{const r=document.querySelector("#houseView .hvbar .row");if(r){const b=document.createElement("button");b.className="btn";b.type="button";b.textContent="اعرض تصميمي 3D";b.onclick=open;r.prepend(b)}}
}
