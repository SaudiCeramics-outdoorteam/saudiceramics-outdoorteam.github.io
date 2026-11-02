p='/home/claude/villa-src.html';s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep('const CAT=/*__CAT__*/;','const CAT=/*__CAT__*/;\nconst BATHING=/*__BATHING__*/;')
rep('const VX=-.55;','const VX=-.8;let showerX=1.2;')
rep('["vanity","mixer","mirror","toilet","shattaf","shower","acc","drain"].forEach(k=>','["vanity","mixer","mirror","toilet","shattaf","shower","acc","drain","bathing"].forEach(k=>')
# shower: dynamic x, glass moved out
rep('const g=G.shower;clear(g);const m=finish(p.hex),x=1.1,z=Z0+.05;','const g=G.shower;clear(g);const m=finish(p.hex),x=showerX,z=Z0+.05;')
rep('''    const glass=new THREE.MeshStandardMaterial({color:0xd9eef0,transparent:true,opacity:.16,roughness:.05,metalness:0,depthWrite:false});
    const gl=B(.01,2,.95,glass,.55,0,Z0+.48,null,g);gl.userData.pass=true;B(.02,.02,.95,m,.55,2,Z0+.48,"shower",g).userData.pass=true},''','''  },''')
rep('drain(p){const g=G.drain;clear(g);B(.15,.006,.15,finish(p.hex),1.1,.0,-.75,"drain",g)}','''drain(p){const g=G.drain;clear(g);B(.15,.006,.15,finish(p.hex),.35,.0,.35,"drain",g)},
  bathing(model,vi){const g=G.bathing;clear(g);const v=model.variants[vi||0],[L,W]=v.size;
    const acr=SM({color:0xf8f8f5,roughness:.16,envMapIntensity:.8}),inner=SM({color:0xe6eaea,roughness:.2,envMapIntensity:.8}),chrome=finish("#d9dde1");
    const ext=(shape,depth)=>{const geo=new THREE.ExtrudeGeometry(shape,{depth,bevelEnabled:true,bevelSize:.012,bevelThickness:.012,bevelSegments:3,curveSegments:32});geo.rotateX(-Math.PI/2);return geo};
    const rr=(w,h,r)=>{const sh=new THREE.Shape();sh.moveTo(-w/2+r,-h/2);sh.lineTo(w/2-r,-h/2);sh.absarc(w/2-r,-h/2+r,r,-Math.PI/2,0);sh.lineTo(w/2,h/2-r);sh.absarc(w/2-r,h/2-r,r,0,Math.PI/2);sh.lineTo(-w/2+r,h/2);sh.absarc(-w/2+r,h/2-r,r,Math.PI/2,Math.PI);sh.lineTo(-w/2,-h/2+r);sh.absarc(-w/2+r,-h/2+r,r,Math.PI,1.5*Math.PI);return sh};
    if(model.kind==="free"){const cx=1.6-L/2-.06,cz=Z0+W/2+.12;
      bMesh(ext(rr(L,W,W/2*.98),.56),acr,cx,0,cz,"bathing",g);
      bMesh(ext(rr(L-.14,W-.14,(W-.14)/2*.98),.004),inner,cx,.575,cz,"bathing",g);
      bMesh(cyl(.03,.006),chrome,cx,.585,cz,"bathing",g);showerX=1.25}
    else if(model.kind==="tub"){const cx=1.6-L/2,cz=Z0+W/2;
      B(L,.55,W,acr,cx,0,cz,"bathing",g);
      bMesh(ext(rr(L-.18,W-.16,.16),.003),inner,cx,.556,cz,"bathing",g);
      bMesh(cyl(.028,.006),chrome,v.side==="L"?1.6-L+.3:1.6-.3,.563,cz,"bathing",g);
      B(L-.04,.006,.004,SM({color:0xdedede}),cx,.25,Z0+W+.002,"bathing",g);showerX=v.side==="L"?1.6-L+.35:1.6-.35}
    else{const [U,V]=[L,W],h=model.h,R=model.kind==="corner"?Math.min(U,V)*model.r:.04;
      const sh=new THREE.Shape();sh.moveTo(0,0);sh.lineTo(-U,0);sh.lineTo(-U,-(V-R));sh.absarc(-U+R,-(V-R),R,Math.PI,1.5*Math.PI,false);sh.lineTo(0,-V);sh.lineTo(0,0);
      bMesh(ext(sh,h),acr,1.6,0,Z0,"bathing",g);
      const i=.06,R2=Math.max(.03,R-i),sh2=new THREE.Shape();sh2.moveTo(-i,-i);sh2.lineTo(-U+i,-i);sh2.lineTo(-U+i,-(V-R));sh2.absarc(-U+R,-(V-R),R2,Math.PI,1.5*Math.PI,false);sh2.lineTo(-i,-V+i);sh2.lineTo(-i,-i);
      bMesh(ext(sh2,.002),inner,1.6,h+.012,Z0,"bathing",g);
      bMesh(cyl(.028,.006),chrome,1.6-U*.3,h+.018,Z0+V*.3,"bathing",g);
      const glass=new THREE.MeshStandardMaterial({color:0xd9eef0,transparent:true,opacity:.16,roughness:.05,metalness:0,depthWrite:false});
      const gx=1.6-U-.01;const gl=B(.01,1.95,V,glass,gx,h+.02,Z0+V/2,null,g);gl.userData.pass=true;
      B(.025,.025,V,chrome,gx,h+1.97,Z0+V/2,null,g).userData.pass=true;showerX=1.6-U/2}
    build.shower(bathSel.shower)}''')
rep('const BCATS=[["vanity","المغسلة والدولاب"],','const BCATS=[["vanity","المغسلة والدولاب"],["bathing","البانيو وحوض القدم"],')
rep('const bathSel={};BCATS.forEach(([k])=>bathSel[k]=CAT.find(c=>c.cat===k));','const bathSel={};BCATS.forEach(([k])=>bathSel[k]=CAT.find(c=>c.cat===k));\nbathSel.bathing=BATHING.find(m=>m.id==="RIVIERA");const bathVar={RIVIERA:1};')
rep('["vanity","toilet","shattaf","shower","acc","drain"].forEach(k=>build[k](bathSel[k]));','["vanity","toilet","shattaf","acc","drain"].forEach(k=>build[k](bathSel[k]));build.bathing(bathSel.bathing,bathVar.RIVIERA);')
# renderBath: branch for bathing
rep('''  const list=CAT.filter(c=>c.cat===bathCat),cur=bathSel[bathCat];''','''  if(bathCat==="bathing"){renderBathing(bc,bp,bs);return}
  const list=CAT.filter(c=>c.cat===bathCat),cur=bathSel[bathCat];''')
rep('let saved=null;','''function renderBathing(bc,bp,bs){
  const cur=bathSel.bathing,vi=bathVar[cur.id]||0,v=cur.variants[vi];
  bp.innerHTML="";bp.className="prods wide";
  BATHING.forEach(m=>{const b=document.createElement("button");b.setAttribute("aria-pressed",String(m===cur));b.title=m.title;
    b.innerHTML=`<img alt="${esc(m.title)}" src="${m.img}"><span>${m.title}</span>`;b.onclick=()=>{bathSel.bathing=m;build.bathing(m,bathVar[m.id]||0);renderBath()};bp.appendChild(b)});
  const had=cart.find(i=>i.bcat==="bathing");
  bs.innerHTML=`<img class="photo" title="اضغط للتكبير" alt="${esc(cur.title)}" src="${cur.photo}"><h3>${esc(v.name)}</h3><div class="code">${v.code}</div>
   ${cur.variants.length>1?`<div class="fields" style="margin-top:10px;grid-template-columns:1fr"><label for="vSel">المقاس والاتجاه<select id="vSel">${cur.variants.map((x,i)=>`<option value="${i}" ${i===vi?"selected":""}>${x.label}</option>`).join("")}</select></label></div>`:""}
   <dl>${cur.spec.map(([a,b])=>`<dt>${a}</dt><dd>${b}</dd>`).join("")}</dl>
   <div class="row"><button class="btn" id="bAdd">${had&&had.code===v.code?"بالسلة ✓":had?"استبدل بالسلة":"أضف للسلة"}</button></div>`;
  const vs=document.getElementById("vSel");if(vs)vs.onchange=()=>{bathVar[cur.id]=+vs.value;build.bathing(cur,+vs.value);renderBath()};
  document.getElementById("bAdd").onclick=()=>{cart.filter(i=>i.bcat==="bathing").forEach(i=>cart.splice(cart.indexOf(i),1));
    putCart({code:v.code,name:v.name,color:"أبيض",thumb:cur.img,photo:cur.photo,zone:"الحمام",qty:1,unit:"قطعة",spec:cur.spec,bcat:"bathing"});renderBath()};
  bs.querySelector(".photo").onclick=()=>zoom(cur.photo,cur.title);
}
let saved=null;''')
rep('.prods.sq{','.prods.wide{grid-template-columns:repeat(3,1fr)}.prods.wide button{aspect-ratio:auto;background:#111;display:flex;flex-direction:column}.prods.wide button img{aspect-ratio:3/2;object-fit:cover}.prods.wide button span{font:600 11px var(--body);color:#fff;padding:4px 0;letter-spacing:.04em}\n.prods.sq{')
open(p,'w').write(s)
