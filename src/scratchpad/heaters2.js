/* ---------- new heater lines: Fawry instant (wall panel), central floor-standing tank, solar system on the roof ---------- */
const solarG=new THREE.Group();scene.add(solarG);
const SOLAR_AT=[3.2,ROOF,-2.6];
const _heaterOld=build.heater;
build.heater=function(p){clear(solarG);if(!p||!["instant","central","solar"].includes(p.kind))return _heaterOld(p);
  const g=G.heater;clear(g);const x=X0,z=.25,grey=SM({color:0x8c9096,metalness:.6,roughness:.35}),chrome=finish("#d9dde1");
  if(p.kind==="instant"){const[A,Bw,C]=p.dims.map(v=>v/1000),dark=p.hex==="#141518",y0=1.3;
    const body=glossy(dark?"#141518":"#f6f6f4",.1);bMesh(extFront(rrect(Bw,A,.012),C,.004).rotateY(Math.PI/2),body,x+C/2+.01,y0+A/2,z,"heater",g);
    const fx=x+C+.016,glow=SM({color:0x0c1f2a,emissive:dark?0x35d0ff:0x9fb4c8,emissiveIntensity:dark?.9:.35});
    if(dark){bMesh(extFront(rrect(.05,.035,.004),.003,0).rotateY(Math.PI/2),glow,fx,y0+A*.42,z,"heater",g);B(.003,.002,Bw*.98,SM({color:0x2a2b2f}),fx,y0,z,"heater",g)}
    else{const ring=new THREE.Mesh(new THREE.TorusGeometry(.045,.006,12,48),SM({color:0xd7dde3,metalness:.5,roughness:.3}));ring.rotation.y=Math.PI/2;ring.position.set(fx,y0+A*.38,z);g.add(ring);
      B(Bw*.004+.003,.012,Bw,grey,x+C/2+.01,y0-.012,z,"heater",g)}
    [[-.05,0xd0202e],[.05,0x1f4fd1]].forEach(([dz,c])=>{bMesh(cyl(.01,.03),SM({color:c,roughness:.4}),x+C*.6,y0-.03,z+dz,"heater",g);bMesh(cyl(.007,.35),chrome,x+C*.6,y0-.22,z+dz,"heater",g)});return}
  if(p.kind==="central"){const[Bh,D]=p.dims,r=D/2000,h=Bh/1000,cx=x+r+.06,cz=z+.05;
    bMesh(lathe([[0,0],[r*.96,0],[r,.03],[r,h-.05],[r*.92,h],[0,h]],64),glossy("#f3f3f0",.2),cx,.04,cz,"heater",g);
    [.28,.68].forEach(t=>B(.01,.16,.11,glossy("#fbfbfa",.25),cx+r,.04+h*t,cz,"heater",g));
    bMesh(cyl(.03,.012,32),SM({color:0x24365f,roughness:.4}),cx+r+.004,.04+h*.12,cz,"heater",g).rotation.z=Math.PI/2;
    [0,2.1,4.2].forEach(a=>bMesh(cyl(.025,.04),SM({color:0x1b1c1e}),cx+Math.cos(a)*r*.6,.02,cz+Math.sin(a)*r*.6,"heater",g));
    [-.08,.08].forEach(dz=>bMesh(cyl(.014,.35),SM({color:0x3aa54a,roughness:.5}),cx,.04+h+.17,cz+dz,"heater",g));return}
  /* solar: tank + tilted flat-plate panels on the roof */
  const[Bw,E,F,n]=p.dims,PW=1.007,PL=1.503,a=.7,tankR=F/2000,tankL=E/1000;
  const frame=SM({color:0xeef0f2,metalness:.35,roughness:.35}),glass=SM({color:0x1e3f9a,metalness:.35,roughness:.12,envMapIntensity:1.2}),tankM=glossy("#f6f6f4",.18);
  const add=(geo,mat,px,py,pz)=>{const m=new THREE.Mesh(geo,mat);m.position.set(px,py,pz);m.castShadow=true;solarG.add(m);return m};
  const tot=n*PW+(n-1)*.03;for(let i=0;i<n;i++){const px=-tot/2+PW/2+i*(PW+.03);
    const pn=add(new THREE.BoxGeometry(PW,.085,PL),frame,px,Math.sin(a)*PL/2+.15,-Math.cos(a)*PL/2);pn.rotation.x=a;
    const gl=add(new THREE.BoxGeometry(PW-.05,.01,PL-.05),glass,0,0,0);pn.add(gl);solarG.remove(gl);gl.position.set(0,.045,0)}
  const topY=Math.sin(a)*PL+.15,backZ=-Math.cos(a)*PL;
  const tk=add(cyl(tankR,tankL,48),tankM,0,topY+tankR+.02,backZ-tankR*.6);tk.rotation.z=Math.PI/2;
  [-1,1].forEach(s=>{const c=add(cyl(tankR*.98,.01,48),grey,s*(tankL/2+.003),topY+tankR+.02,backZ-tankR*.6);c.rotation.z=Math.PI/2});
  [-tot/2+.05,tot/2-.05].forEach(px=>{add(new THREE.BoxGeometry(.04,topY,.04),frame,px,topY/2,backZ-.02);add(new THREE.BoxGeometry(.04,.04,Math.abs(backZ)+.1),frame,px,.02,backZ/2);
    const st=add(new THREE.BoxGeometry(.035,Math.hypot(topY,Math.abs(backZ)),.035),frame,px,topY/2,backZ/2);st.rotation.x=-Math.atan2(Math.abs(backZ),topY)});
  [-1,1].forEach(s=>{add(cyl(.016,topY*.9),SM({color:0xffffff,roughness:.5}),s*(tot/2+.06),topY*.5+.15,backZ*.5)});
  solarG.position.set(...SOLAR_AT);solarG.rotation.y=Math.PI*.15};
/* when a solar heater is chosen, fly out to the roof so the customer sees it installed; one tap returns to the bathroom */
const solarBack=document.createElement("button");solarBack.type="button";solarBack.className="btn";solarBack.id="solarBack";solarBack.hidden=true;solarBack.textContent="رجوع لدورة المياه";
solarBack.style.cssText="position:absolute;top:12px;inset-inline-start:12px;z-index:5";document.getElementById("stage").appendChild(solarBack);
solarBack.onclick=()=>{solarBack.hidden=true;select("bath")};
function showSolar(){setBathMode(false);controls.minDistance=4;controls.maxDistance=60;controls.minAzimuthAngle=-Infinity;controls.maxAzimuthAngle=Infinity;controls.maxPolarAngle=Math.PI/2.08;hemi.intensity=.78;sun.intensity=.72;
  const t=new THREE.Vector3(SOLAR_AT[0],SOLAR_AT[1]+.8,SOLAR_AT[2]-.6);controls.autoRotate=false;
  anim={t0:performance.now(),p0:camera.position.clone(),t0v:controls.target.clone(),p1:t.clone().add(new THREE.Vector3(3.6,2.6,6.2)),t1:t,dur:reduce?1:1100};solarBack.hidden=false;
  try{say("السخان الشمسي يركّب على سطح البيت")}catch(e){}}
{const ob=build.heater;build.heater=function(p){ob(p);if(p&&p.kind==="solar"&&bathSel.heater===p&&document.readyState==="complete"&&bath.visible)showSolar()}}
