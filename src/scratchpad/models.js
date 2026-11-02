/* ---------- higher-fidelity product models (shapes + colours closer to the catalog photos) ---------- */
const V2=(a)=>a.map(([x,y])=>new THREE.Vector2(x,y));
const lathe=(pts,seg=48,ps=0,pl=Math.PI*2)=>new THREE.LatheGeometry(V2(pts),seg,ps,pl);
const rrect=(w,h,r)=>{const sh=new THREE.Shape(),x=-w/2,y=-h/2;r=Math.min(r,w/2,h/2);sh.moveTo(x+r,y);sh.lineTo(x+w-r,y);sh.quadraticCurveTo(x+w,y,x+w,y+r);sh.lineTo(x+w,y+h-r);sh.quadraticCurveTo(x+w,y+h,x+w-r,y+h);sh.lineTo(x+r,y+h);sh.quadraticCurveTo(x,y+h,x,y+h-r);sh.lineTo(x,y+r);sh.quadraticCurveTo(x,y,x+r,y);return sh};
/* extrude a top-view shape upward by h (shape x→x, shape y→-z) */
const extUp=(shape,h,bev=.012,seg=3)=>{const g=new THREE.ExtrudeGeometry(shape,{depth:h,bevelEnabled:bev>0,bevelSize:bev,bevelThickness:bev,bevelSegments:seg,curveSegments:28});g.rotateX(-Math.PI/2);return g};
/* extrude a front-view shape (x→x, y→y) toward +z by d, centred */
const extFront=(shape,d,bev=.006)=>{const g=new THREE.ExtrudeGeometry(shape,{depth:d,bevelEnabled:bev>0,bevelSize:bev,bevelThickness:bev,bevelSegments:3,curveSegments:24});g.translate(0,0,-d/2);return g};
const glossy=(hex,rough=.1)=>SM({color:new THREE.Color(hex),roughness:rough,envMapIntensity:.9});
const satin=(hex,rough=.55)=>SM({color:new THREE.Color(hex),roughness:rough,envMapIntensity:.45});
const isMatt=hex=>!/^#f4f4f2$/i.test(hex||"#f4f4f2");
const VSTYLE={ // cabinet look per catalog photo
  "130321270009600":{style:"shelf",front:"#7b5638",top:"#f2f1ee"},
  "130321270012100":{style:"doors",front:"#2b2b2d",top:"#f2f1ee"},
  "130321270014700":{style:"frame",front:"#ecebe8",frame:"#4a4b4e",top:"#2f3133"},
  "130321270008900":{style:"split",front:"#d9ccb3",accent:"#55575a",top:"#f2f1ee"},
  "130321270004900":{style:"drawers",front:"#dcdcda",top:"#f2f1ee"},
  "130321270009500":{style:"doors",front:"#5d5e61",top:"#f2f1ee"},
  "130321270004700":{style:"stripes",front:"#eeeeec",accent:"#b9bcbe",top:"#3a3f40"},
  "130321270512600":{style:"doors",front:"#8a6a4a",top:"#f2f1ee"},
  "130321270430200":{style:"diag",front:"#e3dccf",accent:"#26272a",top:"#e9e4da"},
  "130321270601400":{style:"fluted",front:"#4b4d50",top:"#f2f1ee"},
  "130321270611400":{style:"fluted",front:"#5e4535",top:"#f2f1ee"}};
Object.assign(build,{
  vanity(p){const g=G.vanity;clear(g);
    const Z=Z0, mixerTop=(y)=>{bathSel._basinTop=y};
    if(p.kind==="wallbasin"||p.kind==="pedestal"){
      const w=p.w,mat=isMatt(p.hex)?satin(p.hex,.5):glossy(p.hex),d=.42,rx=w/2,rz=d;
      if(p.kind==="pedestal"){ // SPARK: tapered floor-standing column with oval section, flat back
        const body=bMesh(lathe([[0,0],[.19,0],[.2,.02],[.205,.3],[.235,.62],[.27,.84],[.275,.87],[0,.87]],56,-Math.PI/2,Math.PI),mat,VX,0,Z+.005,"vanity",g);body.scale.set(rx/.275,1,rz/.275*.95)}
      else{ // TYPE-A / MIRAGE / Model-A / CRYSTAL: wall-hung bowl body, flat back
        const low=p.code.startsWith("12135")?.66:.5;
        const body=bMesh(lathe([[0,low],[.08,low],[.16,low+.04],[.22,low+.14],[.255,.8],[.272,.86],[.275,.875],[0,.875]],56,-Math.PI/2,Math.PI),mat,VX,0,Z+.005,"vanity",g);body.scale.set(rx/.275,1,rz/.275*.95)}
      const inner=bMesh(lathe([[0,.79],[.12,.8],[.19,.83],[.215,.874],[0,.874]],48,-Math.PI/2,Math.PI),satin(isMatt(p.hex)?p.hex:"#e7e9e8",.3),VX,.003,Z+.06,"vanity",g);inner.scale.set(rx/.275*.9,1,rz/.275*.7);
      bMesh(cyl(.016,.004),finish("#c9ccce"),VX,.796,Z+.2,"vanity",g);
      bathSel._basinTop=.875;build.mixer(bathSel.mixer);build.mirror(bathSel.mirror);return}
    const st=VSTYLE[p.code]||{style:"doors",front:p.hex,top:"#f2f1ee"},w=p.width/100,d=.46,h=.46,y0=.4,front=satin(st.front,.5),zf=Z+d;
    // carcass with softened edges
    if(st.style==="fluted"){const sh=rrect(w,d,.2);bMesh(extUp(sh,h,.006),front,VX,y0,Z+d/2,"vanity",g);
      for(let i=0,n=Math.round(w/.035);i<n;i++){const xx=VX-w/2+.1+i*(w-.2)/(n-1);B(.012,h-.04,.012,satin(st.front,.4),xx,y0+.02,zf-.002,"vanity",g)}}
    else{bMesh(extUp(rrect(w,d,.01),h,.004),front,VX,y0,Z+d/2,"vanity",g);
      const line=(x0,y,len,vert)=>vert?B(.004,len,.003,dark,x0,y,zf+.0015,"vanity",g):B(len,.004,.003,dark,x0,y,zf+.0015,"vanity",g);
      if(st.style==="doors"){line(VX,y0+.03,h-.06,true);B(w*.6,.012,.02,finish("#2a2a2b"),VX,y0+h-.03,zf+.01,"vanity",g)}
      if(st.style==="drawers"){line(VX,y0+h*.5,w-.04,false);B(w*.5,.01,.02,finish("#2a2a2b"),VX,y0+h-.04,zf+.01,"vanity",g)}
      if(st.style==="shelf"){B(w-.04,.004,.003,dark,VX,y0+h*.42,zf+.0015,"vanity",g);B(w-.06,h*.36,.02,SM({color:0x1c1d1f,roughness:.8}),VX,y0+.03,zf-.005,"vanity",g)}
      if(st.style==="split"){B(.05,h-.02,.004,satin(st.accent),VX+w*.12,y0+.01,zf+.002,"vanity",g);line(VX-w*.12,y0+.03,h-.06,true)}
      if(st.style==="frame"){[[-1,0],[1,0]].forEach(([s])=>B(.03,h,.004,satin(st.frame),VX+s*(w/2-.015),y0,zf+.002,"vanity",g));B(w,.03,.004,satin(st.frame),VX,y0,zf+.002,"vanity",g)}
      if(st.style==="stripes"){for(let i=0;i<7;i++){const s=B(.006,h*.9,.003,satin(st.accent),VX+w*.08+i*.035,y0+.02,zf+.002,"vanity",g);s.rotation.z=.35}}
      if(st.style==="diag"){const s=B(.05,h*1.05,.004,satin(st.accent),VX+w*.18,y0-.01,zf+.002,"vanity",g);s.rotation.z=.4}}
    // counter top with recessed basin
    const top=glossy(st.top,.15),T=.05;
    const outer=rrect(w+.01,d+.02,.015),hole=rrect(Math.min(.5,w*.6),.3,.08);
    const ring=new THREE.Shape(outer.getPoints(24));ring.holes.push(new THREE.Path(hole.getPoints(24).map(v=>new THREE.Vector2(v.x,v.y+.04))));
    bMesh(extUp(ring,T,.004),top,VX,y0+h,Z+(d+.02)/2,"vanity",g);
    const bowl=bMesh(extUp(rrect(Math.min(.5,w*.6)-.01,.29,.075),.11,.03),new THREE.MeshStandardMaterial({color:new THREE.Color(st.top==="#2f3133"||st.top==="#3a3f40"?"#3a3d3f":"#ecedeb"),roughness:.15,side:THREE.BackSide,envMap:envTex,envMapIntensity:.7}),VX,y0+h-.06,Z+(d+.02)/2-.04,"vanity",g);
    bMesh(cyl(.016,.004),finish("#c9ccce"),VX,y0+h-.045,Z+(d+.02)/2-.04,"vanity",g);
    bathSel._basinTop=y0+h+T;build.mixer(bathSel.mixer);build.mirror(bathSel.mirror)},
  mixer(p){const g=G.mixer;clear(g);const m=finish(p.hex),y=(bathSel._basinTop||.89),z=Z0+.07;
    // RIO single-lever profile (side view), extruded to its width
    const s=new THREE.Shape();s.moveTo(-.022,0);s.lineTo(.022,0);s.lineTo(.024,.12);s.lineTo(.13,.135);s.lineTo(.135,.15);s.lineTo(.02,.16);s.lineTo(-.024,.16);s.lineTo(-.024,0);
    const geo=extFront(s,.034,.004);geo.rotateY(-Math.PI/2);bMesh(geo,m,VX,y,z,"mixer",g);
    const lv=new THREE.Shape();lv.moveTo(-.01,0);lv.lineTo(.012,0);lv.lineTo(.0,.012);lv.lineTo(-.075,.035);lv.lineTo(-.08,.026);lv.lineTo(-.01,0);
    const lg=extFront(lv,.03,.003);lg.rotateY(-Math.PI/2);bMesh(lg,m,VX,y+.16,z,"mixer",g)},
  toilet(p){const g=G.toilet;clear(g);const x=X0,z=.25,hex=p.hex||"#f4f4f2",mat=isMatt(hex)?satin(hex,.45):glossy(hex,.08);
    const bowlProfile=(h0,h1)=>[[0,h0],[.13,h0],[.125,h0+.04],[.14,h0+(h1-h0)*.45],[.19,h1-.03],[.205,h1-.01],[.205,h1],[0,h1]];
    const oval=(mesh,sx)=>{mesh.scale.set(sx,1,1);return mesh};
    if(p.kind==="wall"){ // wall-hung: floating bowl, flat back, concealed cistern plate
      oval(bMesh(lathe(bowlProfile(.24,.4)),mat,x+.36,0,z,"toilet",g),1.35);
      B(.16,.2,.34,mat,x+.08,.24,z,"toilet",g);
      oval(bMesh(lathe([[0,0],[.205,0],[.21,.012],[.2,.026],[0,.03]]),mat,x+.37,.4,z,"toilet",g),1.38);
      B(.012,.15,.24,finish("#d9dde1"),x+.006,1.0,z,"toilet",g);return}
    oval(bMesh(lathe(bowlProfile(0,.4)),mat,x+.44,0,z,"toilet",g),1.38);
    oval(bMesh(lathe([[0,0],[.205,0],[.212,.014],[.2,.03],[0,.034]]),mat,x+.45,.4,z,"toilet",g),1.4);
    if(p.smart===true||p.smart===false&&p.code.startsWith("1305")){ // smart: low sculpted rear, side knob
      const rear=bMesh(lathe([[0,0],[.17,0],[.19,.25],[.2,.42],[.17,.47],[0,.48]],48,0,Math.PI),mat,x+.02,0,z,"toilet",g);rear.rotation.y=-Math.PI/2;rear.scale.set(1.1,1,.75);
      bMesh(cyl(.03,.02,24),SM({color:0xbfc3c6,metalness:.9,roughness:.25}),x+.25,.38,z+.24,"toilet",g).rotation.x=Math.PI/2;
      if(p.smart===false){B(.2,.22,.3,mat,x+.11,.42,z,"toilet",g)}return}
    // one-piece close-coupled: tall rounded cistern merged with bowl, chrome dual-flush button
    bMesh(extUp(rrect(.2,.38,.07),.38,.02),mat,x+.13,.38,z,"toilet",g);
    bMesh(cyl(.028,.012,32),finish("#d9dde1"),x+.13,.79,z,"toilet",g);
    B(.24,.36,.3,mat,x+.14,0,z,"toilet",g)},
  shower(p){const g=G.shower;clear(g);const m=finish(p.hex),x=showerX,z=Z0+.05;
    bMesh(cyl(.012,1.15),m,x,1.5,z,"shower",g);
    const arm=new THREE.CatmullRomCurve3([new THREE.Vector3(x,2.06,z),new THREE.Vector3(x,2.12,z+.04),new THREE.Vector3(x,2.12,z+.3)]);
    bMesh(new THREE.TubeGeometry(arm,20,.01,10,false),m,0,0,0,"shower",g);
    bMesh(lathe([[0,0],[.1,0],[.105,.008],[.1,.014],[0,.016]]),m,x,2.095,z+.31,"shower",g);
    bMesh(new THREE.CircleGeometry(.092,40),SM({color:0x2a2c2e,roughness:.6}),x,2.094,z+.31,"shower",g).rotation.x=Math.PI/2;
    // mixer body + lever + diverter
    const body=bMesh(cyl(.03,.16,32),m,x,.95,z+.035,"shower",g);body.rotation.z=Math.PI/2;
    B(.012,.012,.08,m,x,.97,z+.09,"shower",g);bMesh(cyl(.014,.05),m,x,1.0,z+.035,"shower",g);
    // handset on slider + hose
    B(.04,.05,.04,m,x,1.45,z+.02,"shower",g);
    const hs=new THREE.Group();hs.position.set(x+.04,1.45,z+.05);hs.rotation.z=-.15;g.add(hs);
    bMesh(cyl(.016,.18),m,0,-.06,0,"shower",hs);bMesh(lathe([[0,0],[.05,0],[.052,.01],[.045,.02],[0,.022]]),m,0,.03,0,"shower",hs).rotation.x=Math.PI/2;
    const hose=new THREE.CatmullRomCurve3([new THREE.Vector3(x+.06,1.33,z+.05),new THREE.Vector3(x+.14,.9,z+.08),new THREE.Vector3(x+.02,.7,z+.1),new THREE.Vector3(x,.92,z+.06)]);
    bMesh(new THREE.TubeGeometry(hose,40,.007,8,false),SM({color:0xc6c9cb,metalness:.85,roughness:.3}),0,0,0,"shower",g)},
  heater(p){const g=G.heater;clear(g);const body=glossy("#f7f7f5",.18),x=X0,z=.25,grey=SM({color:0x8c9096,metalness:.6,roughness:.35}),red=SM({color:0xd0202e,roughness:.4});
    if(p.kind==="quad"){bMesh(extFront(rrect(.36,.36,.06),.18,.02).rotateY(Math.PI/2),body,x+.11,1.62,z,"heater",g);
      const t=new THREE.Shape();t.moveTo(-.035,.03);t.lineTo(.035,.03);t.lineTo(0,-.035);t.lineTo(-.035,.03);bMesh(extFront(t,.004,0).rotateY(Math.PI/2),red,x+.215,1.64,z,"heater",g);return}
    if(p.kind==="sink"){bMesh(lathe([[0,0],[.13,0],[.15,.03],[.15,.36],[.13,.39],[0,.39]]),body,x+.17,1.45,z,"heater",g);
      bMesh(cyl(.03,.01,32),grey,x+.32,1.62,z,"heater",g).rotation.z=Math.PI/2;return}
    if(p.kind==="horiz"){const L=.42+p.cap*.0048,r=.21;const c=bMesh(lathe([[0,-L/2],[r*.8,-L/2],[r,-L/2+.05],[r,L/2-.05],[r*.8,L/2],[0,L/2]],56),body,x+r+.04,2.47-r,z,"heater",g);c.rotation.x=Math.PI/2;
      bMesh(cyl(.05,.012,32),grey,x+r+.04,2.47-r,z+L/2+.004,"heater",g).rotation.x=Math.PI/2;bMesh(cyl(.012,.004),red,x+r+.04,2.47-r+.08,z+L/2+.004,"heater",g).rotation.x=Math.PI/2;return}
    const r=p.line==="slim"?.17:.22,h=.42+p.cap*.0055,y0=Math.min(1.3,2.55-h);
    bMesh(lathe([[0,0],[r*.7,0],[r,r*.35],[r,h-r*.35],[r*.7,h],[0,h]],56),body,x+r+.04,y0,z,"heater",g);
    bMesh(cyl(.045,.012,32),grey,x+2*r+.045,y0+h*.3,z,"heater",g).rotation.z=Math.PI/2;
    bMesh(cyl(.01,.004),red,x+2*r+.046,y0+h*.3+.08,z,"heater",g).rotation.z=Math.PI/2;
    if(p.line==="smart"){bMesh(extFront(rrect(.1,.07,.012),.006,0).rotateY(Math.PI/2),SM({color:0x101215,emissive:0x2e8bd9,emissiveIntensity:.45}),x+2*r+.046,y0+h*.6,z,"heater",g)}
    [-.1,.1].forEach(dz=>bMesh(cyl(.012,.12),finish("#d9dde1"),x+r+.04,y0-.06,z+dz,"heater",g))},
  bathing(model,vi){const g=G.bathing;clear(g);const v=model.variants[vi||0],[L,W]=v.size;
    const acr=glossy("#f8f8f5",.12),chrome=finish("#d9dde1"),inside=new THREE.MeshStandardMaterial({color:0xeff1f0,roughness:.12,side:THREE.BackSide,envMap:envTex,envMapIntensity:.8});
    if(model.kind==="free"){ // ROMA: slipper-style freestanding oval
      const prof=[[0,0],[.28,0],[.3,.04],[.36,.3],[.42,.58],[.425,.62],[.405,.625],[.37,.4],[.31,.16],[.26,.11],[0,.11]];
      const t=bMesh(lathe(prof,64),acr,1.6-L/2-.06,0,Z0+W/2+.12,"bathing",g);t.scale.set(L/.85,1,W/.85);showerX=1.25}
    else if(model.kind==="tub"){const cx=1.6-L/2,cz=Z0+W/2,H=.55;
      const outer=rrect(L,W,.03),innerW=W-.12,innerL=L-.16,hole=rrect(innerL,innerW,innerW*.45);
      const ring=new THREE.Shape(outer.getPoints(16));ring.holes.push(new THREE.Path(hole.getPoints(32)));
      bMesh(extUp(ring,H,.01),acr,cx,0,cz,"bathing",g);
      bMesh(extUp(rrect(innerL,innerW,innerW*.45),H-.18,0),inside,cx,.18,cz,"bathing",g);
      const dx=v.side==="L"?1.6-L+.22:1.6-.22;bMesh(cyl(.026,.004),chrome,dx,.182,cz,"bathing",g);bMesh(cyl(.02,.006),chrome,dx+(v.side==="L"?-.05:.05),H+.012,Z0+.08,"bathing",g);
      B(L-.06,.004,.003,SM({color:0xd9d9d6}),cx,.03,Z0+W+.012,"bathing",g);showerX=v.side==="L"?1.6-L+.35:1.6-.35}
    else{const U=L,Vv=W,h=model.h,R=model.kind==="corner"?Math.min(U,Vv)*model.r:.05;
      const tr=(i)=>{const sh=new THREE.Shape(),r=Math.max(.03,R-i);sh.moveTo(-i,-i);sh.lineTo(-U+i,-i);sh.lineTo(-U+i,-(Vv-r-i));sh.absarc(-U+r+i,-(Vv-r-i),r,Math.PI,1.5*Math.PI,false);sh.lineTo(-i,-Vv+i);sh.lineTo(-i,-i);return sh};
      const ring=tr(0);ring.holes.push(new THREE.Path(tr(.06).getPoints(40)));
      bMesh(extUp(ring,h,.008),acr,1.6,0,Z0,"bathing",g);
      bMesh(extUp(tr(.06),.004,0),satin("#eef0ef",.25),1.6,h-.035,Z0,"bathing",g);
      if(model.id==="RIVIERA"||model.id==="LARA"){for(let i=0;i<5;i++)for(let j=0;j<5;j++)B(.035,.003,.035,satin("#e2e5e4",.4),1.6-.12-i*(U-.24)/4,h-.031,Z0+.12+j*(Vv-.24)/4,null,g)}
      bMesh(cyl(.03,.006),chrome,1.6-U*.75,h-.03,Z0+Vv*.25,"bathing",g);
      const glass=new THREE.MeshStandardMaterial({color:0xd9eef0,transparent:true,opacity:.16,roughness:.05,metalness:0,depthWrite:false});
      const gx=1.6-U-.01;const gl=B(.01,1.95,Vv,glass,gx,h+.02,Z0+Vv/2,null,g);gl.userData.pass=true;
      B(.022,.022,Vv,chrome,gx,h+1.97,Z0+Vv/2,null,g).userData.pass=true;showerX=1.6-U/2}
    build.shower(bathSel.shower)},
  mirror(p){const g=G.mirror;clear(g);const v=bathSel.vanity,w=v.width?v.width/100:Math.max(.6,v.w),y=1.62,z=Z0+.012;
    const glass=SM({color:0xdfe6ea,metalness:1,roughness:.04});glass.envMapIntensity=1.4;
    const led=SM({color:0xfff3d6,emissive:0xfff0cc,emissiveIntensity:1});const frame=SM({color:0x1e1f21,roughness:.4,metalness:.3});
    if(p.shape==="round"){const r=Math.min(.38,w*.45);
      if(p.led){bMesh(new THREE.RingGeometry(r-.035,r,64),led,VX,y,z+.004,"mirror",g)}
      else{bMesh(new THREE.TorusGeometry(r,.012,12,64),frame,VX,y,z+.01,"mirror",g);for(let k=1;k<5;k++)bMesh(new THREE.RingGeometry(r*(1-k*.13)-.004,r*(1-k*.13),64),SM({color:0xffe9c2,emissive:0xffe2b0,emissiveIntensity:.5/k}),VX,y,z+.002,"mirror",g)}
      bMesh(new THREE.CircleGeometry(r,64),glass,VX,y,z,"mirror",g)}
    else{const mw=Math.min(1,Math.max(.6,w*.9)),mh=.7;
      if(p.led){const s=rrect(mw,mh,.02),hole=rrect(mw-.06,mh-.06,.01);s.holes.push(new THREE.Path(hole.getPoints(12)));bMesh(new THREE.ShapeGeometry(s),led,VX,y,z+.004,"mirror",g)}
      else{const s=rrect(mw+.03,mh+.03,.005),hole=rrect(mw,mh,.002);s.holes.push(new THREE.Path(hole.getPoints(8)));bMesh(extFront(s,.02,0),frame,VX,y,z+.01,"mirror",g);
        for(let k=1;k<4;k++){const a=rrect(mw*(1-k*.14),mh*(1-k*.17),.01),b=rrect(mw*(1-k*.14)-.012,mh*(1-k*.17)-.012,.01);a.holes.push(new THREE.Path(b.getPoints(8)));bMesh(new THREE.ShapeGeometry(a),SM({color:0xffe9c2,emissive:0xffe2b0,emissiveIntensity:.5/k}),VX,y,z+.002,"mirror",g)}}
      bMesh(new THREE.PlaneGeometry(mw,mh),glass,VX,y,z,"mirror",g)}}
});
