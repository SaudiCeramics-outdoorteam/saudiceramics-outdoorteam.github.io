/* ---------- product-faithful fittings: series shape (RIO round / Conza square / tall) + colour sampled from the product photo ---------- */
const CONZA_BATH=new Set(["130051380058700","130051380059400","130051380132100","130051380034800"]);
const CONZA_TALL=new Set(["130031380058700","130031380029400","130031380132100","130031380034800"]);
const isConza=p=>/conza/i.test(p.name||"");
const isTall=p=>CONZA_TALL.has(p.code)||(/^1300313801/.test(p.code))||/tall|l-size|high/i.test(p.name||"");
const showerKind=p=>/^1304213/.test(p.code)?"column":(CONZA_BATH.has(p.code)||/^1300513801/.test(p.code)||/bath mixer/i.test(p.name||""))?"bath":"mixer";
Object.assign(build,{
  mixer(p){const g=G.mixer;clear(g);const m=finish(p.hex),y=(bathSel._basinTop||.89),z=Z0+.07,tall=isTall(p),sq=isConza(p),H=tall?.28:.15;
    if(sq){B(.042,H,.042,m,VX,y,z,"mixer",g);B(.042,.022,.15,m,VX,y+H-.03,z+.08,"mixer",g);
      const lv=B(.03,.012,.09,m,VX,y+H+.012,z-.01,"mixer",g);lv.rotation.x=-.25}
    else{bMesh(cyl(.021,H,32),m,VX,y+H/2,z,"mixer",g);bMesh(cyl(.026,.012,32),m,VX,y+.006,z,"mixer",g);
      const arc=new THREE.CatmullRomCurve3([new THREE.Vector3(VX,y+H-.02,z),new THREE.Vector3(VX,y+H+.005,z+.05),new THREE.Vector3(VX,y+H-.01,z+.13)]);
      bMesh(new THREE.TubeGeometry(arc,16,.013,14,false),m,0,0,0,"mixer",g);
      const lv=new THREE.Shape();lv.moveTo(-.01,0);lv.lineTo(.014,0);lv.lineTo(.0,.014);lv.lineTo(-.08,.03);lv.lineTo(-.085,.02);lv.lineTo(-.01,0);
      const lg=extFront(lv,.026,.004);lg.rotateY(-Math.PI/2);bMesh(lg,m,VX,y+H,z,"mixer",g)}},
  shower(p){const g=G.shower;clear(g);const m=finish(p.hex),x=showerX,z=Z0+.05,kind=showerKind(p),sq=isConza(p);
    const body=(yy)=>{if(sq){B(.17,.07,.06,m,x,yy-.035,z+.02,"shower",g);B(.03,.05,.05,m,x,yy+.03,z+.05,"shower",g);const lv=B(.025,.012,.09,m,x,yy+.055,z+.06,"shower",g);lv.rotation.x=.35}
      else{const c=bMesh(cyl(.03,.17,32),m,x,yy,z+.035,"shower",g);c.rotation.z=Math.PI/2;bMesh(cyl(.016,.05,24),m,x,yy+.035,z+.04,"shower",g);
        const lv=B(.016,.01,.085,m,x,yy+.06,z+.075,"shower",g);lv.rotation.x=-.3}};
    const handset=(hx,hy)=>{B(.03,.05,.035,m,hx,hy,z+.015,"shower",g);const hs=new THREE.Group();hs.position.set(hx,hy+.02,z+.05);hs.rotation.z=-.12;g.add(hs);
      bMesh(cyl(.016,.17),m,0,-.05,0,"shower",hs);bMesh(lathe([[0,0],[.05,0],[.052,.01],[.045,.02],[0,.022]]),m,0,.04,0,"shower",hs).rotation.x=Math.PI/2};
    const hose=(a,b)=>bMesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([a,new THREE.Vector3((a.x+b.x)/2+.12,Math.min(a.y,b.y)-.35,z+.1),b]),40,.007,8,false),SM({color:new THREE.Color(p.hex),metalness:.8,roughness:.35}),0,0,0,"shower",g);
    if(kind==="column"){body(.95);bMesh(cyl(.012,1.15),m,x,1.5,z,"shower",g);
      bMesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(x,2.06,z),new THREE.Vector3(x,2.12,z+.04),new THREE.Vector3(x,2.12,z+.3)]),20,.01,10,false),m,0,0,0,"shower",g);
      const head=sq?B(.22,.012,.22,m,x,2.09,z+.31,"shower",g):bMesh(lathe([[0,0],[.1,0],[.105,.008],[.1,.014],[0,.016]]),m,x,2.095,z+.31,"shower",g);
      handset(x+.05,1.45);hose(new THREE.Vector3(x+.06,1.35,z+.05),new THREE.Vector3(x,.92,z+.06));return}
    const yy=kind==="bath"?.75:1.0;body(yy);
    if(kind==="bath"){if(sq)B(.04,.03,.16,m,x,yy-.07,z+.1,"shower",g);else{const sp=bMesh(cyl(.016,.14,24),m,x,yy-.05,z+.1,"shower",g);sp.rotation.x=Math.PI/2}}
    handset(x+.02,1.55);hose(new THREE.Vector3(x+.02,1.45,z+.05),new THREE.Vector3(x,yy-.04,z+.06))}
});
finish=function(hex){const c=new THREE.Color(hex||"#d9dde1"),hsl={};c.getHSL(hsl);let m;
  if(hsl.s<.12&&hsl.l>.55){m=SM({color:new THREE.Color("#eef0f2"),metalness:1,roughness:.07});m.envMapIntensity=1.4}
  else if(hsl.l<.2){m=SM({color:c,metalness:.25,roughness:.45});m.envMapIntensity=.6}
  else{const b=c.clone().offsetHSL(0,0,.06);m=SM({color:b,metalness:.7,roughness:.3});m.envMapIntensity=1.1}
  return m};
["mixer","shower","acc","fitting","shattaf","drain"].forEach(k=>{if(bathSel[k])build[k](bathSel[k])});
