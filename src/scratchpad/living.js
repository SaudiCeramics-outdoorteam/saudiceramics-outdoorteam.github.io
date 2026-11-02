/* ---------- inside the house: a living room (majlis) whose floor and walls take interior tiles ---------- */
const LX=-70,living=new THREE.Group();living.position.set(LX,0,0);living.visible=false;scene.add(living);
let livingCat="lfloor";
const livFloorMat=SM({map:floorT.clone(),roughness:.45,envMapIntensity:.2}),livWallMat=SM({map:wallT.clone(),color:0xf1ede6,roughness:.6,envMapIntensity:.1});
livFloorMat.map.needsUpdate=true;livWallMat.map.needsUpdate=true;
const LW=6.4,LD=5.2,LH=3.1,LX0=-LW/2,LZ0=-LD/2;
const LB=(w,h,d,mat,x,y,z,cat,pick=true)=>{const g=new THREE.BoxGeometry(w,h,d);scaleUV(g,w,h,d);const m=new THREE.Mesh(g,mat);m.position.set(x,y+h/2,z);m.castShadow=m.receiveShadow=true;
  m.userData.zone="living";if(cat)m.userData.cat=cat;if(!pick)m.userData.pass=true;m.userData.origMat=mat;living.add(m);pickables.push(m);return m};
const fab=c=>SM({color:new THREE.Color(c),roughness:.9,envMapIntensity:.05}),wood=c=>SM({color:new THREE.Color(c),roughness:.55,envMapIntensity:.15});
/* shell: floor, back wall with door, side wall with window, skirting */
LB(LW,.1,LD,livFloorMat,0,-.1,0,"lfloor");
LB(1.6,LH,.14,livWallMat,LX0+.8,0,LZ0-.07,"lwall");LB(LW-3.0,LH,.14,livWallMat,LX0+1.6+.2+(LW-3.0)/2+.4,0,LZ0-.07,"lwall");
LB(1.0,LH-2.25,.14,livWallMat,LX0+2.1,2.25,LZ0-.07,"lwall");
LB(.14,LH,1.4,livWallMat,LX0-.07,0,LZ0+.7,"lwall");LB(.14,LH,LD-3.0,livWallMat,LX0-.07,0,LZ0+3.0+(LD-3.0)/2,"lwall");
LB(.14,.9,1.6,livWallMat,LX0-.07,0,LZ0+2.2,"lwall");LB(.14,LH-2.4,1.6,livWallMat,LX0-.07,2.4,LZ0+2.2,"lwall");
const glass=new THREE.MeshStandardMaterial({color:0xcfe6f2,transparent:true,opacity:.35,roughness:.05,metalness:.1});
LB(.03,1.5,1.6,glass,LX0-.06,.9,LZ0+2.2,null,false);[0,.75,1.5].forEach(dy=>LB(.05,.04,1.6,wood("#2b2b2d"),LX0-.05,.9+dy-.02,LZ0+2.2,null,false));
const sky=new THREE.Mesh(new THREE.PlaneGeometry(1.6,1.5),new THREE.MeshBasicMaterial({color:0xdcebf5}));sky.rotation.y=Math.PI/2;sky.position.set(LX0-.4,1.65,LZ0+2.2);living.add(sky);
LB(1.0,2.25,.05,wood("#6b4a32"),LX0+2.1,0,LZ0-.02,null,false);LB(.04,.04,.12,finish("#c9ccce"),LX0+2.5,1.05,LZ0+.03,null,false);
LB(LW,.08,.015,wood("#efece6"),0,0,LZ0+.008,null,false);LB(.015,.08,LD,wood("#efece6"),LX0+.008,0,0,null,false);
/* furniture for scale: L-sofa, coffee table, TV unit, side table + lamp, plant, ceiling light */
const sofa=fab("#b9b2a6"),cush=fab("#d9d3c8");
LB(2.6,.42,.9,sofa,LX0+.25+1.3,0,LZ0+.25+.45+1.6,null,false);LB(2.6,.42,.18,sofa,LX0+.25+1.3,.42,LZ0+.25+.09+1.6,null,false);
LB(.9,.42,1.6,sofa,LX0+.25+.45,0,LZ0+.25+.8+2.5,null,false);LB(.18,.42,1.6,sofa,LX0+.25+.09,.42,LZ0+.25+.8+2.5,null,false);
[0,1,2].forEach(i=>LB(.78,.14,.62,cush,LX0+.75+i*.82,.42,LZ0+.25+.45+1.62,null,false));
LB(1.2,.06,.7,wood("#3c2e25"),LX0+2.3,.38,LZ0+3.4,null,false);[-.5,.5].forEach(dx=>LB(.05,.38,.6,wood("#3c2e25"),LX0+2.3+dx,0,LZ0+3.4,null,false));
LB(2.2,.45,.42,wood("#e8e3da"),LX0+4.6,.12,LZ0+.25,null,false);LB(1.5,.85,.04,SM({color:0x111214,roughness:.2,metalness:.4}),LX0+4.6,1.1,LZ0+.1,null,false);
LB(.4,.5,.4,wood("#3c2e25"),LX0+.5,0,LZ0+1.3,null,false);
const lamp=new THREE.Mesh(new THREE.CylinderGeometry(.14,.18,.25,24),SM({color:0xf3eadb,emissive:0xffe2b0,emissiveIntensity:.5}));lamp.position.set(LX0+.5,.75,LZ0+1.3);living.add(lamp);
const pot=new THREE.Mesh(new THREE.CylinderGeometry(.2,.16,.45,24),SM({color:0xd8d2c6,roughness:.6}));pot.position.set(LX0+LW-.5,.225,LZ0+.5);living.add(pot);
const leaf=new THREE.Mesh(new THREE.SphereGeometry(.42,16,12),fab("#5f7a4f"));leaf.scale.set(1,1.5,1);leaf.position.set(LX0+LW-.5,1.0,LZ0+.5);living.add(leaf);
const ceilLight=new THREE.Mesh(new THREE.CylinderGeometry(.35,.35,.04,40),SM({color:0xffffff,emissive:0xfff4e0,emissiveIntensity:.8}));ceilLight.position.set(0,LH-.05,0);living.add(ceilLight);
const livLight=new THREE.PointLight(0xfff1de,.9,12,1.4);livLight.position.set(0,LH-.3,.3);living.add(livLight);
const livLight2=new THREE.PointLight(0xe8f1ff,.35,10,1.6);livLight2.position.set(LX0+.8,1.8,LZ0+2.2);living.add(livLight2);
ZONES.living={title:"داخل البيت",text:"الصالة من الداخل. اختر بلاط الأرضيات أو الجدران وشوفه مركّب على المكان.",cats:[],pos:[LX+3.4,2.6,4.9],target:[LX-.6,.9,-.6]};
Object.assign(TZ,{lfloor:{label:"أرضية الصالة",area:()=>33,list:"floor"},lwall:{label:"جدران الصالة",area:()=>48,list:"wall"}});
TZ.wall.label="جدران دورات المياه";TZ.floor.label="أرضية دورات المياه";
let livSaved=null;
function setLivingMode(on){if(on===living.visible)return;living.visible=on;
  if(on){hemi.intensity=.5;sun.intensity=.2;livSaved={a:[controls.minAzimuthAngle,controls.maxAzimuthAngle],d:[controls.minDistance,controls.maxDistance],p:controls.maxPolarAngle};
    controls.minDistance=2;controls.maxDistance=8.5;controls.minAzimuthAngle=.05;controls.maxAzimuthAngle=1.5;controls.maxPolarAngle=1.5;controls.autoRotate=false}
  else{if(!bath.visible){hemi.intensity=.78;sun.intensity=.72}if(livSaved){[controls.minAzimuthAngle,controls.maxAzimuthAngle]=livSaved.a;[controls.minDistance,controls.maxDistance]=livSaved.d;controls.maxPolarAngle=livSaved.p}}}
