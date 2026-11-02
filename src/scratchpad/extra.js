/* ---------- brochure products (deduplicated) ---------- */
const BRO=/*__BRO__*/,STAIRS=/*__STAIRS__*/;
CAT.push(...BRO.filter(b=>!CAT.some(c=>c.code===b.code)));
const PROFILES=CAT.filter(c=>c.cat==="profile"),ADHESIVES=["130940270020100","130941360040100"].map(CATby).filter(Boolean);
/* fittings: angle valves under the basin, shower arm/hose shown on the shower */
build.fitting=function(p){const g=G.fitting;clear(g);const m=finish(p.hex||"#d9dde1"),y=.34,z=Z0+.05;
  [-.12,.12].forEach(dx=>{const x=VX+dx;bMesh(cyl(.018,.06,24),m,x,y,z,"fitting",g).rotation.x=Math.PI/2;
    bMesh(cyl(.014,.05,24),m,x,y+.035,z+.03,"fitting",g);bMesh(lathe([[0,0],[.022,0],[.024,.012],[0,.016]]),m,x,y,z+.035,"fitting",g).rotation.x=Math.PI/2;
    const hose=new THREE.CatmullRomCurve3([new THREE.Vector3(x,y+.06,z+.03),new THREE.Vector3(x,y+.25,z+.05),new THREE.Vector3(x*0.98+VX*.02,.84,z+.06)]);
    bMesh(new THREE.TubeGeometry(hose,20,.006,8,false),SM({color:0xc6c9cb,metalness:.85,roughness:.3}),0,0,0,"fitting",g)})};
G.fitting=new THREE.Group();bath.add(G.fitting);
BCATS.splice(BCATS.findIndex(c=>c[0]==="acc"),0,["fitting","المحابس والليّات"]);
bathSel.fitting=CAT.find(c=>c.cat==="fitting");if(bathSel.fitting)build.fitting(bathSel.fitting);
/* LUXO / LAVINO sintered-stone basins use the cabinet builder with a stone top */
Object.assign(VSTYLE,{"130461570014800":{style:"drawers",front:"#efeeea",top:"#e8e6e1"},"130461570010200":{style:"drawers",front:"#e2d6c2",top:"#d8c9ae"}});

/* ---------- entrance stairs: porcelain tread + riser ---------- */
const STEP={n:3,w:2.4,rise:.4/3,run:.32,x:0,z0:6.1};
const stairG=new THREE.Group();scene.add(stairG);const stairM={tread:[],riser:[]};
(function(){const mat=concreteMat;for(let i=0;i<STEP.n;i++){const yTop=STEP.rise*(STEP.n-i),zf=STEP.z0+STEP.run*(i+1);
  const body=box(STEP.w,yTop,STEP.run+.001,mat,STEP.x,0,zf-STEP.run/2,"stairs");stairG.add(body);
  const tr=box(STEP.w,.02,STEP.run+.02,mat,STEP.x,yTop,zf-STEP.run/2+.01,"stairs");stairG.add(tr);stairM.tread.push(tr);
  const ri=box(STEP.w,yTop-.002,.02,mat,STEP.x,0,zf+.01,"stairs");stairG.add(ri);stairM.riser.push(ri)}
  [...stairM.tread,...stairM.riser].forEach(o=>o.userData.origMat=o.material)})();
ZONES.stairs={title:"الدرج",text:"درج المدخل. اختر درج البورسلان (الدرجة والقائم) ويتركب على درجات المدخل.",cats:[],pos:[4.5,2.4,11],target:[0,.3,6.4]};
(function(){const b=document.createElement("button");b.id="z-stairs";b.dataset.zone="stairs";b.setAttribute("aria-pressed","false");b.textContent="الدرج";
  const ref=document.getElementById("z-pool");ref.after(b);b.addEventListener("click",()=>select("stairs"))})();
async function stripTex(srcs,lenCm,depCm){const imgs=await Promise.all(srcs.map(loadImg));const ppc=4,cols=2;
  const c=document.createElement("canvas");c.width=cols*lenCm*ppc;c.height=depCm*ppc;const g=c.getContext("2d");g.fillStyle="#bdb7ad";g.fillRect(0,0,c.width,c.height);
  for(let k=0;k<cols;k++){const im=imgs[k%imgs.length];g.drawImage(im,k*lenCm*ppc+1,1,lenCm*ppc-2,depCm*ppc-2)}
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;t.anisotropy=8;return t}
let stairSel=null;
async function applyStairs(s){stairSel=s;
  if(!s){[...stairM.tread,...stairM.riser].forEach(o=>o.material=o.userData.origMat);renderStairs();return}
  renderStairs();const[tt,rt]=await Promise.all([stripTex(s.treads,120,32),stripTex(s.risers,120,15)]);if(stairSel!==s)return;
  const fit=(o,t,face)=>{const g=o.geometry,uv=g.attributes.uv;for(let i=0;i<uv.count;i++){uv.setXY(i,(i%4===0||i%4===2)?0:1,(i%4<2)?1:0)}uv.needsUpdate=true;
    o.material=new THREE.MeshBasicMaterial({map:t})};
  stairM.tread.forEach(o=>fit(o,tt));stairM.riser.forEach(o=>fit(o,rt))}
const stState={steps:3,width:2.4};
function stairSpec(s,kind){return kind==="tread"?[["القطعة","درجة (Stair Tread)"],["المقاس","32 × 120 سم"],["السماكة","2.0 سم"],["النوع","بورسلان مطفي، 6 وجوه"],["الاستخدام","داخلي وخارجي"],["قطع بالكرتون","2"],["م² بالكرتون","0.76"],["كغ بالكرتون","37.64"],["كرتون بالطبلية","36"],["م² بالطبلية","27.36"],["كغ بالطبلية","1,373"]]
  :[["القطعة","قائم (Stair Riser)"],["المقاس","15 × 120 سم"],["السماكة","2.0 سم"],["النوع","بورسلان مطفي، 6 وجوه"],["الاستخدام","داخلي وخارجي"],["قطع بالكرتون","2"],["م² بالكرتون","0.36"],["كغ بالكرتون","17.64"],["كرتون بالطبلية","90"],["م² بالطبلية","32.40"],["كغ بالطبلية","1,606"]]}
function renderStairs(){const host=document.getElementById("tileBox");if(selected!=="stairs")return;
  const s=stairSel,pcs=stState.steps*Math.ceil(stState.width/1.2),boxes=Math.ceil(pcs/2);
  host.innerHTML=`<div class="prods tgrid"><button type="button" class="raw" data-i="-1" aria-pressed="${!s}">خرسانة</button>${STAIRS.map((x,i)=>`<button type="button" data-i="${i}" aria-pressed="${s===x}"><img alt="${esc(x.name)}" src="${x.treads[0]}"><span>${esc(x.name)}</span></button>`).join("")}</div>
   <div class="spec">${!s?`<p>اختر تصميم الدرج ويتركب على درجات المدخل.</p>`:`<img class="photo" id="stPh" title="اضغط للتكبير" alt="${esc(s.name)}" src="${s.photo}"><h3 dir="ltr">${esc(s.name)}</h3>
   <div class="code">${s.tread} · ${s.riser}</div><dl>${stairSpec(s,"tread").slice(1,5).map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join("")}</dl>
   <div class="calc"><h4>حساب الكمية</h4><div class="fields"><label for="stN">عدد الدرجات<input id="stN" type="number" min="1" value="${stState.steps}"></label><label for="stW">عرض الدرج (م)<input id="stW" type="number" min=".6" step=".1" value="${stState.width}"></label></div>
   <div class="result">${fmt(pcs)} درجة + ${fmt(pcs)} قائم = <b>${fmt(boxes)} كرتون درج</b> و<b>${fmt(boxes)} كرتون قائم</b><br><span>كل قطعة بطول 120 سم، والكرتون فيه قطعتين.</span></div></div>
   <div class="row"><button class="btn" id="stAdd">${inCart(s.tread)?"حدّث الكمية بالسلة":"أضف للسلة"}</button><button class="btn ghost" id="stSheet" type="button">ورقة المواصفات</button></div>`}</div>`;
  host.querySelectorAll(".tgrid button").forEach(b=>b.onclick=()=>applyStairs(+b.dataset.i<0?null:STAIRS[+b.dataset.i]));
  if(!s)return;
  document.getElementById("stPh").onclick=()=>zoom(s.photo,s.name);document.getElementById("stSheet").onclick=()=>zoom(s.sheet,s.name);
  document.getElementById("stN").onchange=e=>{stState.steps=Math.max(1,parseInt(e.target.value,10)||1);renderStairs()};
  document.getElementById("stW").onchange=e=>{stState.width=Math.max(.6,parseFloat(e.target.value)||1.2);renderStairs()};
  document.getElementById("stAdd").onclick=()=>{cart.filter(i=>i.tz==="stairs"&&!i.code.startsWith(s.tread)&&i.code!==s.riser).forEach(i=>cart.splice(cart.indexOf(i),1));
    putCart({code:s.tread,name:s.name+" · Stair Tread 32×120",color:"",thumb:s.treads[0],photo:s.photo,_sheet:s.sheet,zone:"الدرج",tz:"stairs",qty:boxes,unit:"كرتون",sqmPer:.76,spec:stairSpec(s,"tread")});
    putCart({code:s.riser,name:s.name+" · Stair Riser 15×120",color:"",thumb:s.risers[0],photo:s.photo,_sheet:s.sheet,zone:"الدرج",tz:"stairs",qty:boxes,unit:"كرتون",sqmPer:.36,spec:stairSpec(s,"riser")});renderStairs()};
}
