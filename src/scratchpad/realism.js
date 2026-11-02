/* ---------- realism pass: filmic tone mapping, real sky, landscaping, and a "finished house" look (glazing, doors, no site clutter) ---------- */
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
hemi.color.set(0xd9e8f7);hemi.groundColor.set(0xcdb894);sun.color.set(0xfff0dc);sun.intensity=Math.max(sun.intensity,.9);
{/* gradient sky dome + matching haze, independent of the page's light/dark theme */
  const g=new THREE.SphereGeometry(140,32,16),m=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,fog:false,uniforms:{top:{value:new THREE.Color(0x5f93c9)},mid:{value:new THREE.Color(0xbcd5ea)},bot:{value:new THREE.Color(0xeee3cf)}},
    vertexShader:"varying vec3 vp;void main(){vp=(modelMatrix*vec4(position,1.)).xyz;gl_Position=projectionMatrix*viewMatrix*vec4(vp,1.);}",
    fragmentShader:"uniform vec3 top,mid,bot;varying vec3 vp;void main(){float h=normalize(vp-cameraPosition).y;vec3 c=h>0.?mix(mid,top,pow(clamp(h*1.6,0.,1.),.7)):mix(mid,bot,clamp(-h*6.,0.,1.));gl_FragColor=vec4(c,1.);}"});
  const sky=new THREE.Mesh(g,m);sky.renderOrder=-1;sky.userData.pass=true;scene.add(sky);
  const fix=()=>{scene.background=null;scene.fog=new THREE.Fog(0xd8dfe3,60,135)};fix();applySky=fix;
  sky.onBeforeRender=(r,s,cam)=>sky.position.copy(cam.position);}
/* landscaping: street, sidewalk, a few palms (always on, they read as context not product) */
const land=new THREE.Group();scene.add(land);
{const asph=SM({color:0x3a3d41,roughness:.95}),walk=SM({color:0xcfc8bb,roughness:.9}),curb=SM({color:0xe6e1d6,roughness:.8});
  const pl=(w,d,mat,x,z,y=.012)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,.02,d),mat);m.position.set(x,y,z);m.receiveShadow=true;m.userData.pass=true;land.add(m);return m};
  pl(80,7,asph,0,17.5);pl(80,2.2,walk,0,12.9,.06);pl(80,.25,curb,0,14.05,.09);
  for(let x=-36;x<=36;x+=4){const d=new THREE.Mesh(new THREE.BoxGeometry(1.8,.022,.15),SM({color:0xf2f0e8,roughness:.6}));d.position.set(x,.025,17.5);land.add(d)}
  const trunkM=SM({color:0x8a6a48,roughness:.95}),leafM=SM({color:0x4f6b3a,roughness:.8,side:THREE.DoubleSide});
  const palm=(x,z,h=5.5)=>{const p=new THREE.Group();p.position.set(x,0,z);
    for(let i=0;i<9;i++){const r=.17-.008*i,s=new THREE.Mesh(new THREE.CylinderGeometry(r*.92,r,h/9,10),trunkM);s.position.y=h/9*(i+.5);s.castShadow=true;p.add(s)}
    for(let k=0;k<11;k++){const sh=new THREE.Shape();sh.moveTo(0,0);sh.quadraticCurveTo(.35,1.1,0,2.4);sh.quadraticCurveTo(-.35,1.1,0,0);
      const leaf=new THREE.Mesh(new THREE.ShapeGeometry(sh,8),leafM);leaf.castShadow=true;const piv=new THREE.Group();piv.position.y=h;piv.rotation.y=k/11*Math.PI*2;
      leaf.rotation.x=-Math.PI/2+.35+(k%2)*.25;piv.add(leaf);p.add(piv)}
    p.traverse(o=>o.userData.pass=true);land.add(p)};
  [[-11.5,12.9],[-3.5,12.9],[4.5,12.9],[12.5,12.9],[-12.5,-9],[12.5,-9.5]].forEach(([x,z])=>palm(x,z,5+Math.random()*1.2))}
/* finished house: glazing in every window, a timber front door, aluminium frames; scaffolding/pallets/rebar go away */
const finishG=new THREE.Group();finishG.visible=false;scene.add(finishG);
{const glass=new THREE.MeshPhysicalMaterial?new THREE.MeshPhysicalMaterial({color:0x9fb7c6,roughness:.05,metalness:.2,transparent:true,opacity:.55,envMap:envTex,envMapIntensity:1.4,clearcoat:1}):SM({color:0x9fb7c6,roughness:.05,metalness:.3,transparent:true,opacity:.55});
  const frameM=SM({color:0x2d2f33,metalness:.6,roughness:.35}),doorM=SM({color:0x6b4a32,roughness:.55}),sillM=SM({color:0xe9e4da,roughness:.6});
  const add=(w,h,d,m,x,y,z)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;o.userData.pass=true;finishG.add(o);return o};
  OPENINGS.forEach(o=>{const w=o.b-o.a,mid=(o.a+o.b)/2,y1=o.y0+o.sill,y2=o.y0+o.top,h=y2-y1,cy=(y1+y2)/2,ft=.05;
    const P=(u,y,dw,dh,dd,m)=>o.axis==="x"?add(dw,dh,dd,m,u,y,o.fixed):add(dd,dh,dw,m,o.fixed,y,u);
    if(o.sill<.05&&h>1.7&&w<2.6){P(mid,cy,w-.02,h-.02,o.t*.5,doorM);P(mid+w*.3,y1+1.05,.04,.04,o.t*.9,frameM);return}
    P(mid,cy,w-.04,h-.04,.02,glass);P(mid,y1+ft/2,w,ft,o.t+.02,frameM);P(mid,y2-ft/2,w,ft,o.t+.02,frameM);
    P(o.a+ft/2,cy,ft,h,o.t+.02,frameM);P(o.b-ft/2,cy,ft,h,o.t+.02,frameM);if(w>1.4)P(mid,cy,ft*.8,h,o.t*.6,frameM);
    if(o.sill>.05)P(mid,y1-.03,w+.1,.06,o.t+.12,sillM)})}
let FINISHED=false;
function setFinished(on){FINISHED=on;finishG.visible=on;const facadeTiled=!!current;scaff.forEach(o=>o.visible=!on&&!facadeTiled);
  const b=document.getElementById("finBtn");if(b){b.setAttribute("aria-pressed",String(on));b.textContent=on?"شكل العظم":"بعد التشطيب"}}
{const b=document.createElement("button");b.id="finBtn";b.className="btn ghost";b.type="button";b.setAttribute("aria-pressed","false");b.textContent="بعد التشطيب";b.title="شوف البيت بالنوافذ والأبواب بعد التشطيب";
  b.onclick=()=>setFinished(!FINISHED);const h=document.getElementById("houseBtn");if(h)h.before(b);else document.querySelector(".topact").prepend(b)}
/* interiors: warmer, brighter lamps so rooms read like a design render */
try{livLight.intensity=1.15;livLight.color.set(0xffe6c4);livLight2.intensity=.5}catch(e){}
