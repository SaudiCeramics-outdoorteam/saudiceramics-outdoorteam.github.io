/* ---------- hi-res images: big images live in data/hi_*.json and are swapped in on demand ---------- */
const HIMAP=/*__HIMAP__*/,hiChunks={};
const hiURL=u=>{if(typeof u!=="string"||!u.startsWith("hi:"))return Promise.resolve(u);const h=u.slice(3),c=HIMAP[h];if(!c)return Promise.resolve("");
  return(hiChunks[c]||(hiChunks[c]=fetch("data/"+c+".json").then(r=>r.json()))).then(d=>d[h])};
function fixImg(img){const s=img.getAttribute("src");if(!s||!s.startsWith("hi:"))return;img.dataset.hi=s;img.removeAttribute("src");img.classList.add("hiwait");
  hiURL(s).then(u=>{if(img.dataset.hi===s){img.src=u;img.classList.remove("hiwait")}})}
new MutationObserver(ms=>ms.forEach(m=>{if(m.type==="attributes"){if(m.target.tagName==="IMG")fixImg(m.target);return}
  m.addedNodes.forEach(n=>{if(n.nodeType!==1)return;if(n.tagName==="IMG")fixImg(n);n.querySelectorAll&&n.querySelectorAll("img").forEach(fixImg)})}))
  .observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:["src"]});
document.querySelectorAll("img").forEach(fixImg);
async function resolveImgs(root){await Promise.all([...root.querySelectorAll("img")].map(async im=>{const s=im.dataset.hi||im.getAttribute("src")||"";
  if(s.startsWith("hi:")){im.dataset.hi="";im.src=await hiURL(s)}if(!im.complete)await new Promise(r=>{im.onload=im.onerror=r})}))}

/* ---------- categories (as the sales team names them) ---------- */
const NAV=[
 {id:"in",label:"بلاط داخلي",subs:[["bath","bwall","الجدران"],["bath","bfloor","الأرضيات"]]},
 {id:"out",label:"بلاط خارجي",subs:[["facade",null,"الواجهات"],["court",null,"الأحواش"]]},
 {id:"pool",label:"بلاط مسابح",subs:[["pool",null,"المسبح"]]},
 {id:"roof",label:"بلاط أسطح",subs:[["roof",null,"السطح"]]},
 {id:"stairs",label:"بلاط الدرج",subs:[["stairs",null,"الدرج"]]},
 {id:"san",label:"الأدوات الصحية",subs:[["bath","vanity","المغاسل"],["bath","toilet","الكراسي"],["bath","bathing","البانيو وأحواض القدم"],["bath","mixer","خلاطات المغسلة"],["bath","shower","الدش وخلاطاته"],["bath","shattaf","الشطافات"],["bath","mirror","المرايا"],["bath","fitting","المحابس والليّات"],["bath","acc","الإكسسوارات"],["bath","drain","الصفايات"]]},
 {id:"heat",label:"السخانات",subs:[["bath","heater","السخانات"]]}];
const catnav=document.getElementById("catnav"),subz=document.getElementById("subz"),homeBtn=document.getElementById("homeBtn");
function goSub(z,bc){if(z==="bath"&&bc)bathCat=bc;if(selected===z&&z==="bath"){renderBath()}else select(z)}
function curNav(zone){return NAV.find(n=>n.subs.some(([z,bc])=>z===zone&&(zone!=="bath"||bc===bathCat)))}
function syncNav(zone){const cur=zone==="all"?null:curNav(zone);homeBtn.setAttribute("aria-pressed",String(zone==="all"));
  catnav.innerHTML=NAV.map(n=>`<button type="button" data-n="${n.id}" aria-pressed="${cur===n}">${n.label}</button>`).join("");
  catnav.querySelectorAll("button").forEach(b=>b.onclick=()=>{const n=NAV.find(x=>x.id===b.dataset.n);const[z,bc]=n.subs[0];goSub(z,bc)});
  const on=catnav.querySelector('[aria-pressed="true"]');if(on)on.scrollIntoView({block:"nearest",inline:"nearest"});
  subz.innerHTML=cur&&cur.subs.length>1?cur.subs.map(([z,bc,l])=>`<button type="button" data-z="${z}" data-bc="${bc||""}" aria-pressed="${z===zone&&(z!=="bath"||bc===bathCat)}">${l}</button>`).join(""):"";
  subz.querySelectorAll("button").forEach(b=>b.onclick=()=>goSub(b.dataset.z,b.dataset.bc||null))}
homeBtn.onclick=()=>select("all");
{const _rb=renderBath;renderBath=function(){_rb();syncNav(selected)}}
ZONES.all.text="اختر تصنيف من الأعلى: البلاط الداخلي أو الخارجي أو المسابح أو الأسطح أو الدرج، أو الأدوات الصحية والسخانات. كل اختيار يتركب على البيت مباشرة.";
syncNav("all");infoTitle.textContent=ZONES.all.title;infoText.textContent=ZONES.all.text;

/* ---------- pool water appears once the pool is tiled ---------- */
const water=new THREE.Mesh(new THREE.PlaneGeometry(PW-.02,PL-.02),new THREE.MeshStandardMaterial({color:0x3aa6d0,transparent:true,opacity:.38,roughness:.05,metalness:.1}));
water.rotation.x=-Math.PI/2;water.position.set(pcx,-.22,pcz);water.visible=false;water.userData.pass=true;scene.add(water);

/* ---------- customer gate: name + mobile, kept on this device and printed on the catalog ---------- */
const WA_NUMBER="";// sales WhatsApp in international format, e.g. 9665XXXXXXXX
let CUSTOMER=null;try{CUSTOMER=JSON.parse(localStorage.getItem("scc-customer")||"null")}catch(e){}
const gate=document.getElementById("gate"),whoBtn=document.getElementById("whoBtn");
function showWho(){whoBtn.hidden=!CUSTOMER;if(CUSTOMER)whoBtn.textContent=`${CUSTOMER.name} · ${CUSTOMER.phone}`}
function openGate(){gate.hidden=false;document.getElementById("gName").value=CUSTOMER?.name||"";document.getElementById("gPhone").value=CUSTOMER?.phone||"";setTimeout(()=>document.getElementById("gName").focus(),50)}
document.getElementById("gateForm").addEventListener("submit",e=>{e.preventDefault();
  const name=document.getElementById("gName").value.trim(),raw=document.getElementById("gPhone").value.replace(/[\s\-()]/g,"").replace(/[٠-٩]/g,d=>"٠١٢٣٤٥٦٧٨٩".indexOf(d)),err=document.getElementById("gErr");
  let ph=raw.replace(/^\+?966/,"0");if(/^5\d{8}$/.test(ph))ph="0"+ph;
  if(name.length<2){err.textContent="اكتب اسمك عشان نجهز الكتالوج باسمك.";err.hidden=false;return}
  if(!/^05\d{8}$/.test(ph)){err.textContent="رقم الجوال لازم يكون 10 أرقام ويبدأ بـ 05، مثل 0551234567.";err.hidden=false;return}
  err.hidden=true;CUSTOMER={name,phone:ph};try{localStorage.setItem("scc-customer",JSON.stringify(CUSTOMER))}catch(e){}
  gate.hidden=true;showWho()});
whoBtn.onclick=openGate;showWho();if(!CUSTOMER)openGate();
function waLink(){if(!WA_NUMBER||!cart.length)return"";
  const lines=[`طلب من صفحة "شطّب بيتك مع الخزف السعودي"`,CUSTOMER?`العميل: ${CUSTOMER.name} - ${CUSTOMER.phone}`:"",...cart.map(i=>`• ${i.name} (${i.code}) - ${i.zone}: ${itemLine(i)}`)].filter(Boolean);
  return"https://wa.me/"+WA_NUMBER+"?text="+encodeURIComponent(lines.join("\n"))}
