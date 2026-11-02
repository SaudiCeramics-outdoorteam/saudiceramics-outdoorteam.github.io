/* ---------- "شوف بيتك": renders of the finished house with everything the customer picked ---------- */
function shot(mode,pos,target,w=1600,h=1000){
  const st={p:camera.position.clone(),t:controls.target.clone(),bv:bath.visible,lv:living.visible,hi:hemi.intensity,su:sun.intensity,sel:selected,hov:hovered,fov:camera.fov,asp:camera.aspect,pr:renderer.getPixelRatio()};
  selected=null;hovered=null;paint();
  bath.visible=mode==="bath";living.visible=mode==="living";hemi.intensity=mode==="out"?.78:mode==="bath"?.42:.5;sun.intensity=mode==="out"?.72:.22;
  renderer.setPixelRatio(1);renderer.setSize(w,h,false);camera.aspect=w/h;camera.fov=mode==="out"?38:52;camera.updateProjectionMatrix();
  camera.position.set(...pos);camera.lookAt(new THREE.Vector3(...target));renderer.render(scene,camera);
  const url=renderer.domElement.toDataURL("image/jpeg",.9);
  bath.visible=st.bv;living.visible=st.lv;hemi.intensity=st.hi;sun.intensity=st.su;selected=st.sel;hovered=st.hov;paint();
  renderer.setPixelRatio(st.pr);camera.fov=st.fov;camera.position.copy(st.p);controls.target.copy(st.t);resize();controls.update();
  return url}
function houseShots(){const z=new Set(cart.map(i=>i.tz||(i.bcat?"bath":null)).filter(Boolean));const L=[];
  L.push({cap:"الواجهة والحوش",img:shot("out",[16,9.5,24],[0,3,2])});
  L.push({cap:"المسبح والسطح",img:shot("out",[19,13,8],[6,1.5,-1])});
  L.push({cap:"داخل البيت",img:shot("living",[LX+4.4,2.9,6.2],[LX-.7,.8,-.7])});
  L.push({cap:"الدرج",img:shot("living",[LX-1.9,1.7,1.5],[LX+1.0,1.0,LZ0+.6])});
  L.push({cap:"دورة المياه",img:shot("bath",[BX+3.4,1.95,3.4],[BX+.65,1.05,-.4])});
  return L}
const hv=document.createElement("div");hv.id="houseView";hv.hidden=true;hv.setAttribute("role","dialog");hv.setAttribute("aria-label","بيتك بعد اختياراتك");
hv.innerHTML=`<div class="hvbar"><div><h2>بيتك بعد اختياراتك</h2><p id="hvWho"></p></div><div class="row" style="margin:0"><button class="btn ghost" id="hvBack">رجوع للتصميم</button><button class="btn" id="hvCat">اعرض الكتالوج</button></div></div><div class="hvgrid" id="hvGrid"></div>`;
document.getElementById("app").appendChild(hv);
function openHouse(){cartEl.hidden=true;hv.hidden=false;const g=document.getElementById("hvGrid");g.innerHTML=`<p class="fine">جاري تجهيز صور بيتك…</p>`;
  document.getElementById("hvWho").textContent=(CUSTOMER?`${CUSTOMER.name} · `:"")+`${cart.length} منتج مختار`;
  setTimeout(()=>{const L=houseShots();window._houseShots=L;g.innerHTML=L.map((s,i)=>`<figure class="${i===0?"big":""}"><img alt="${s.cap}" src="${s.img}"><figcaption>${s.cap}</figcaption></figure>`).join("");
    g.querySelectorAll("img").forEach(im=>im.onclick=()=>zoom(im.src,im.alt))},60)}
document.getElementById("hvBack").onclick=()=>hv.hidden=true;
document.getElementById("hvCat").onclick=()=>{hv.hidden=true;document.getElementById("openCat").click()};
{const b=document.createElement("button");b.id="houseBtn";b.className="btn ghost";b.type="button";b.textContent="شوف بيتك";b.onclick=openHouse;document.querySelector(".topact").insertBefore(b,document.getElementById("cartBtn"))}
{const b=document.createElement("button");b.className="btn ghost";b.type="button";b.textContent="شوف بيتك بعد اختياراتك";b.onclick=openHouse;document.getElementById("openCat").before(b)}
