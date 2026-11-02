p='/home/claude/villa-src.html';s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:80]
    s=s.replace(a,b)
# data
rep('const BATHING=/*__BATHING__*/;','''const BATHING=/*__BATHING__*/;
const SAN=/*__SAN__*/,HEAT=/*__HEAT__*/,SHEETS=/*__SHEETS__*/;
CAT.push(...SAN,...HEAT);''')
rep('function catItem(p,q,zone){return{code:p.code,name:p.name,color:p.color||"",thumb:p.img,photo:p.img,zone,qty:q,unit:p.unit,spec:p.spec}}',
    'function catItem(p,q,zone){return{code:p.code,name:p.name,color:p.color||"",thumb:p.img,photo:p.photo||p.img,zone,qty:q,unit:p.unit,spec:p.spec,full:p.full||[],sheet:p.sheet}}')
rep('putCart({code:current.code,name:current.name,color:"",thumb:current.thumb,photo:current.photo,zone:"الواجهة",qty:q.boxes,unit:"كرتون",sqmPer:current.sqmBox,',
    'putCart({code:current.code,name:current.name,color:"",thumb:current.thumb,photo:current.photo,sheet:"t"+current.code,zone:"الواجهة",qty:q.boxes,unit:"كرتون",sqmPer:current.sqmBox,')
rep('spec:[["المقاس","60 × 120 × 2.0 سم"],["النوع","بورسلان مطفي"],["الحواف","مشطوفة (Rectified)"],["الوجوه",current.faces+" وجه"],["التعبئة",current.sqmBox+" م² للكرتون"]]});',
    'spec:[["المقاس","60 × 120 × 2.0 سم"],["السماكة","2.0 سم"],["النوع","بورسلان مطفي (Matt Porcelain)"],["الحواف","مشطوفة (Rectified)"],["الاستخدام","خارجي وواجهات"],["الوجوه",current.faces+" وجه"],["قطع بالكرتون","1"],["م² بالكرتون",String(current.sqmBox)],["كغ بالكرتون",String(current.kgBox)],["كرتون بالطبلية",String(current.boxPallet)],["م² بالطبلية","23.04"],["كغ بالطبلية","1,148.96"]]});')
rep('<div class="row"><button class="btn" id="addCart">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button><a class="btn ghost" href="https://shop.saudiceramics.com/ar/" target="_blank" rel="noopener">المتجر</a></div>',
    '<div class="row"><button class="btn" id="addCart">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button><button class="btn ghost" type="button" id="tSheet">ورقة المواصفات</button></div>')
rep('  specEl.querySelector(".photo").onclick=()=>zoom(current.photo,current.name);','  specEl.querySelector(".photo").onclick=()=>zoom(current.photo,current.name);\n  document.getElementById("tSheet").onclick=()=>zoom(SHEETS["t"+current.code],current.name);')
# vanity: support sanitary basins
rep('''  vanity(p){const g=G.vanity;clear(g);const w=p.width/100,mat=SM({color:new THREE.Color(p.hex),roughness:.55});''','''  vanity(p){const g=G.vanity;clear(g);
    if(p.kind==="wallbasin"||p.kind==="pedestal"){const w=p.w,mat=SM({color:new THREE.Color(p.hex),roughness:/[2-8]/.test(p.hex)?.5:.12,envMapIntensity:.8});
      if(p.kind==="pedestal"){const ped=bMesh(new THREE.CylinderGeometry(w*.42,w*.36,.84,40),mat,VX,.42,Z0+.24,"vanity",g);ped.scale.set(1,1,.9)}
      else{const b=bMesh(new THREE.CylinderGeometry(w*.5,w*.36,.3,40,1,false,-Math.PI/2,Math.PI),mat,VX,.73,Z0+.005,"vanity",g)}
      B(w,.04,.4,mat,VX,.84,Z0+.2,"vanity",g);B(w*.7,.006,.26,SM({color:0xe9e9e6,roughness:.2}),VX,.881,Z0+.22,"vanity",g);
      build.mixer(bathSel.mixer);build.mirror(bathSel.mirror);return}
    const w=p.width/100,mat=SM({color:new THREE.Color(p.hex),roughness:.55});''')
rep('mirror(p){const g=G.mirror;clear(g);const w=bathSel.vanity.width/100,y=1.6,z=Z0+.012;','mirror(p){const g=G.mirror;clear(g);const w=bathSel.vanity.width?bathSel.vanity.width/100:Math.max(.6,bathSel.vanity.w),y=1.6,z=Z0+.012;')
# toilet kinds + colour
rep('''  toilet(p){const g=G.toilet;clear(g);const x=X0,z=.25;
    const bowl=bMesh(new THREE.CylinderGeometry(.2,.12,.4,40),ceramic,x+.42,.2,z,"toilet",g);bowl.scale.set(1.35,1,1);
    const seat=bMesh(new THREE.CylinderGeometry(.205,.205,.035,40),ceramic,x+.43,.42,z,"toilet",g);seat.scale.set(1.35,1,1);
    if(p.smart){''','''  toilet(p){const g=G.toilet;clear(g);const x=X0,z=.25,ceramic=SM({color:new THREE.Color(p.hex||"#f4f4f2"),roughness:p.hex&&p.hex!=="#f4f4f2"?.45:.12,envMapIntensity:.9});
    if(p.kind==="wall"){const bowl=bMesh(new THREE.CylinderGeometry(.19,.13,.3,40),ceramic,x+.36,.3,z,"toilet",g);bowl.scale.set(1.4,1,1);
      const seat=bMesh(new THREE.CylinderGeometry(.195,.195,.03,40),ceramic,x+.37,.465,z,"toilet",g);seat.scale.set(1.4,1,1);
      B(.12,.3,.36,ceramic,x+.06,.18,z,"toilet",g);B(.012,.14,.22,SM({color:0xd9dde1,metalness:.9,roughness:.2}),x+.006,1.05,z,"toilet",g);return}
    const bowl=bMesh(new THREE.CylinderGeometry(.2,.12,.4,40),ceramic,x+.42,.2,z,"toilet",g);bowl.scale.set(1.35,1,1);
    const seat=bMesh(new THREE.CylinderGeometry(.205,.205,.035,40),ceramic,x+.43,.42,z,"toilet",g);seat.scale.set(1.35,1,1);
    if(p.kind==="floor"){B(.22,.42,.38,ceramic,x+.13,0,z,"toilet",g);B(.18,.3,.4,ceramic,x+.1,.42,z,"toilet",g);B(.2,.03,.42,ceramic,x+.1,.72,z,"toilet",g);return}
    if(p.smart){''')
# shattaf: bigger, own spot, visible hose
rep('''  shattaf(p){const g=G.shattaf;clear(g);const m=finish(p.hex),x=X0+.02,z=.72;
    B(.03,.07,.05,m,x,.55,z,"shattaf",g);const h=bMesh(cyl(.016,.13),m,x+.05,.6,z,"shattaf",g);h.rotation.z=.5;
    const hose=bMesh(new THREE.TorusGeometry(.12,.007,8,40,Math.PI*1.3),SM({color:0xc9ccce,metalness:.9,roughness:.3}),x+.03,.42,z,"shattaf",g);hose.rotation.y=Math.PI/2},''','''  shattaf(p){const g=G.shattaf;clear(g);const m=finish(p.hex||"#d9dde1"),x=X0,z=-.16;
    bMesh(cyl(.03,.05),m,x+.025,.42,z,"shattaf",g).rotation.z=Math.PI/2;bMesh(cyl(.012,.06),m,x+.05,.47,z,"shattaf",g);
    B(.035,.09,.06,m,x+.018,.72,z,"shattaf",g);
    const h=new THREE.Group();h.position.set(x+.09,.8,z);h.rotation.z=-.9;g.add(h);
    bMesh(cyl(.02,.15),m,0,0,0,"shattaf",h);const head=bMesh(new THREE.CylinderGeometry(.032,.024,.07,24),m,0,.1,0,"shattaf",h);
    bMesh(cyl(.006,.03),m,.03,.03,0,"shattaf",h).rotation.z=Math.PI/2;
    const curve=new THREE.CatmullRomCurve3([new THREE.Vector3(x+.05,.42,z),new THREE.Vector3(x+.12,.22,z+.04),new THREE.Vector3(x+.16,.3,z+.02),new THREE.Vector3(x+.12,.6,z),new THREE.Vector3(x+.07,.74,z)]);
    bMesh(new THREE.TubeGeometry(curve,40,.008,8,false),SM({color:0xc6c9cb,metalness:.85,roughness:.3}),0,0,0,"shattaf",g)},
  heater(p){const g=G.heater;clear(g);const body=SM({color:0xf7f7f5,roughness:.3,envMapIntensity:.7}),x=X0,z=.25,trim=SM({color:0x3a3d42,roughness:.4});
    if(p.kind==="quad"){B(.2,.38,.38,body,x+.1,1.45,z,"heater",g);bMesh(cyl(.05,.01,32),trim,x+.205,1.64,z,"heater",g).rotation.z=Math.PI/2;return}
    if(p.kind==="sink"){bMesh(new THREE.CylinderGeometry(.15,.15,.38,40),body,x+.17,1.6,z,"heater",g);return}
    if(p.kind==="horiz"){const L=.4+p.cap*.005,r=.22;const c=bMesh(cyl(r,L,48),body,x+r+.04,2.45-r,z,"heater",g);c.rotation.x=Math.PI/2;
      bMesh(cyl(.045,.012,32),trim,x+r+.04,2.45-r,z+L/2+.006,"heater",g).rotation.x=Math.PI/2;return}
    const r=p.line==="slim"?.18:.22,h=.42+p.cap*.0055;const y0=Math.min(1.35,2.55-h);
    bMesh(cyl(r,h,48),body,x+r+.04,y0+h/2,z,"heater",g);bMesh(new THREE.SphereGeometry(r,48,16,0,Math.PI*2,0,Math.PI/2),body,x+r+.04,y0+h,z,"heater",g);
    const dome=bMesh(new THREE.SphereGeometry(r,48,16,0,Math.PI*2,0,Math.PI/2),body,x+r+.04,y0,z,"heater",g);dome.rotation.x=Math.PI;
    bMesh(cyl(.045,.01,32),trim,x+2*r+.04,y0+h*.35,z,"heater",g).rotation.z=Math.PI/2;
    if(p.line==="smart"){B(.004,.06,.09,SM({color:0x111316,emissive:0x2e8bd9,emissiveIntensity:.6}),x+2*r+.045,y0+h*.6,z,"heater",g)}},''')
rep('["vanity","mixer","mirror","toilet","shattaf","shower","acc","drain","bathing"].forEach(k=>','["vanity","mixer","mirror","toilet","shattaf","shower","acc","drain","bathing","heater"].forEach(k=>')
rep('["mixer","خلاط المغسلة"],','["mixer","خلاط المغسلة"],["heater","سخان الماء"],')
rep('const BCATS=[["vanity","المغسلة والدولاب"],','const BCATS=[["vanity","المغسلة"],')
rep('bathSel.vanity=CAT.find(c=>c.code==="130321270004700");','bathSel.vanity=CAT.find(c=>c.code==="130321270004700");bathSel.toilet=CAT.find(c=>c.code==="121210251010010");bathSel.heater=CAT.find(c=>c.code==="EWH-V80");')
rep('["vanity","toilet","shattaf","acc","drain"].forEach(k=>build[k](bathSel[k]));','["vanity","toilet","shattaf","acc","drain","heater"].forEach(k=>build[k](bathSel[k]));')
# bath list: vanity cat includes basins
rep('  const list=CAT.filter(c=>c.cat===bathCat),cur=bathSel[bathCat];','  const list=CAT.filter(c=>c.cat===bathCat||(bathCat==="vanity"&&c.cat==="basin")),cur=bathSel[bathCat];')
# spec panel: full spec + sheet button
rep('''   <dl>${cur.color?`<dt>اللون</dt><dd>${cur.color}</dd>`:""}${cur.spec.map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join("")}</dl>''',
    '''   <dl>${cur.color?`<dt>اللون</dt><dd>${cur.color}</dd>`:""}${cur.spec.concat(cur.full||[]).map(([a,b])=>`<dt>${a}</dt><dd>${esc(b)}</dd>`).join("")}</dl>''')
rep('   <div class="row"><button class="btn" id="bAdd">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button></div>`;',
    '   <div class="row"><button class="btn" id="bAdd">${had?"حدّث الكمية بالسلة":"أضف للسلة"}</button>${cur.sheet?`<button class="btn ghost" type="button" id="bSheet">ورقة المواصفات</button>`:""}</div>`;')
rep('  bs.querySelector(".photo").onclick=()=>zoom(cur.img,cur.name);\n}','  bs.querySelector(".photo").onclick=()=>zoom(cur.photo||cur.img,cur.name);const sb=document.getElementById("bSheet");if(sb)sb.onclick=()=>zoom(SHEETS[cur.sheet],cur.name);\n}')
rep('<img class="photo pimg" title="اضغط للتكبير" alt="${esc(cur.name)}" src="${cur.img}">','<img class="photo pimg" title="اضغط للتكبير" alt="${esc(cur.name)}" src="${cur.photo||cur.img}">')
rep('''    cart.filter(i=>i.bcat===bathCat&&i.code!==cur.code&&!["acc","drain"].includes(bathCat)).forEach(i=>cart.splice(cart.indexOf(i),1));''','''    cart.filter(i=>i.bcat===bathCat&&i.code!==cur.code&&!["acc","drain"].includes(bathCat)).forEach(i=>cart.splice(cart.indexOf(i),1));''')
# bathing: sheet
rep('''   <div class="row"><button class="btn" id="bAdd">${had&&had.code===v.code?"بالسلة ✓":had?"استبدل بالسلة":"أضف للسلة"}</button></div>`;''','''   <div class="row"><button class="btn" id="bAdd">${had&&had.code===v.code?"بالسلة ✓":had?"استبدل بالسلة":"أضف للسلة"}</button><button class="btn ghost" type="button" id="bSheet">ورقة المواصفات</button></div>`;''')
rep('putCart({code:v.code,name:v.name,color:"أبيض",thumb:cur.img,photo:cur.photo,zone:"الحمام",qty:1,unit:"قطعة",spec:cur.spec,bcat:"bathing"});renderBath()};',
    'putCart({code:v.code,name:v.name,color:"أبيض",thumb:cur.img,photo:cur.photo,sheet:"b"+cur.id,zone:"الحمام",qty:1,unit:"قطعة",spec:[["المقاس",v.label]].concat(cur.spec),bcat:"bathing"});renderBath()};\n  document.getElementById("bSheet").onclick=()=>zoom(SHEETS["b"+cur.id],cur.title);')
open(p,'w').write(s)
