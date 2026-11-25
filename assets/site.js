/* RS Assessoria Aduaneira — interações (vanilla, sem dependências) */
(function(){
"use strict";
var d=document,w=window,root=d.documentElement;
var RM=w.matchMedia&&w.matchMedia("(prefers-reduced-motion: reduce)").matches;
var fine=w.matchMedia&&w.matchMedia("(hover:hover) and (pointer:fine)").matches;
w.dataLayer=w.dataLayer||[];

/* ---------- Nav ---------- */
var nav=d.querySelector(".nav"),lastY=0;
function onScrollNav(){var y=w.scrollY;if(!nav)return;
  if(!nav.classList.contains("light"))nav.classList.toggle("solid",y>40);
  if(!d.body.classList.contains("nav-open"))nav.classList.toggle("hide",y>lastY&&y>420);
  lastY=y;}
var burger=d.querySelector(".burger");
if(burger){burger.addEventListener("click",function(){var o=d.body.classList.toggle("nav-open");nav.classList.toggle("nav-open",o);burger.setAttribute("aria-expanded",o?"true":"false");});
  d.querySelectorAll(".nav-links a").forEach(function(a){a.addEventListener("click",function(){d.body.classList.remove("nav-open");nav.classList.remove("nav-open");burger.setAttribute("aria-expanded","false");});});}

/* ---------- Split text ---------- */
d.querySelectorAll("[data-split]").forEach(function(el){
  var i=0;function walk(node){Array.prototype.slice.call(node.childNodes).forEach(function(n){
    if(n.nodeType===3){var frag=d.createDocumentFragment();n.textContent.split(/(\s+)/).forEach(function(t){
      if(!t)return;if(/^\s+$/.test(t)){frag.appendChild(d.createTextNode(t));return;}
      var o=d.createElement("span");o.className="w";var s=d.createElement("span");s.style.setProperty("--i",i++);s.textContent=t;o.appendChild(s);frag.appendChild(o);});
      n.parentNode.replaceChild(frag,n);}else if(n.nodeType===1&&n.tagName!=="BR"){walk(n);}});}
  walk(el);el.classList.add("split");});

/* ---------- Reveal ---------- */
var revealEls=d.querySelectorAll(".rv,.rv-l,.split,[data-count],.step");
if("IntersectionObserver" in w){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");if(e.target.hasAttribute("data-count"))count(e.target);io.unobserve(e.target);}});},{rootMargin:"0px 0px -8% 0px",threshold:.12});
  revealEls.forEach(function(el){io.observe(el);});
}else{revealEls.forEach(function(el){el.classList.add("in");});}

/* ---------- Counters ---------- */
function count(el){var end=+el.getAttribute("data-count"),dur=1600,t0=null,suf=el.getAttribute("data-suffix")||"";
  if(RM){el.innerHTML=end+suf;return;}
  function f(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,4);el.innerHTML=Math.round(end*e)+suf;if(p<1)requestAnimationFrame(f);}
  requestAnimationFrame(f);}

/* ---------- Parallax (scroll) ---------- */
var par=[].slice.call(d.querySelectorAll("[data-depth]"));
var route=d.querySelector(".route"),routePath=route&&route.querySelector("path"),steps=[].slice.call(d.querySelectorAll(".step"));
if(routePath){var L=Math.ceil(routePath.getTotalLength?routePath.getTotalLength():1200);route.style.setProperty("--len",L);}
var ticking=false;
function frame(){ticking=false;onScrollNav();var vh=w.innerHeight;
  if(!RM){par.forEach(function(el){var r=el.parentElement.getBoundingClientRect();if(r.bottom<-200||r.top>vh+200)return;
    var c=(r.top+r.height/2-vh/2);el.style.transform="translate3d(0,"+(c*-(+el.getAttribute("data-depth"))).toFixed(1)+"px,0)";});}
  if(route){var sr=route.parentElement.getBoundingClientRect();var p=Math.min(Math.max((vh*.85-sr.top)/(sr.height+vh*.35),0),1);
    route.style.setProperty("--p",RM?1:p.toFixed(3));steps.forEach(function(s,i){s.classList.toggle("on",p>=i/(steps.length)+.02);});}
}
w.addEventListener("scroll",function(){if(!ticking){ticking=true;requestAnimationFrame(frame);}},{passive:true});
w.addEventListener("resize",frame);frame();

/* ---------- Tilt + spotlight ---------- */
if(fine&&!RM){
  d.querySelectorAll("[data-tilt]").forEach(function(c){
    c.addEventListener("pointermove",function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
      c.style.transform="perspective(1000px) rotateX("+((.5-y)*7).toFixed(2)+"deg) rotateY("+((x-.5)*9).toFixed(2)+"deg) translateZ(0)";});
    c.addEventListener("pointerleave",function(){c.style.transform="";});});
  var tags=d.querySelectorAll("[data-mouse]");
  if(tags.length){var hero=d.querySelector(".hero");hero.addEventListener("pointermove",function(e){var x=e.clientX/w.innerWidth-.5,y=e.clientY/w.innerHeight-.5;
    tags.forEach(function(t){var k=+t.getAttribute("data-mouse");t.style.transform="translate3d("+(x*k)+"px,"+(y*k)+"px,0)";});});}
}

/* ---------- Globe (hero) ---------- */
var cv=d.getElementById("globe");
if(cv&&cv.getContext){(function(){
  var ctx=cv.getContext("2d"),LAND="0000008671ffff80040000000c0000000000080bf01fff8000000c01ff00200000000feefc0fff00000010dffffc7c007ffffffffffffffffc03c0a0000000001ffffffffffffffff80600000000000003ffffff238380003efffffffffffffe07fffffe0e0000003cfffffffffffe7800c0fffe0fc000021cffffffffffc0c000007fffefe0000519ffffffffff818000003fffeff00003ffffffffffffe00000001fffffd80001ffffffffffffc00000000fffff800001ffffffffffff800000000ffffe000007fbc3bfffffff200000000ffffc00000785ffdffffffc000000000ffff8000007003fdfffffc44000000007fff8000003f00fffffffe4c000000003ffe0000007fd8fffffffe00000000000fd2000000fffffffffffe000000000007c0000001ffff7dfffffe00000000000380000003ffffff8ffffc000000000003c8800003ffffbf87e7d0000000000001f8200003ffffdf03c7c00000000000001c000003ffffde0381e100000000000004000003fffff00101e0000000000000007c0001fffffc01804000000000000000fe0000fffffc00810080000000000000ffc00003fff800028400000000000000ffc00001fff000019c00000000000001fff00001ffe000009e10000000000001fffe0000ffc00000c00f000000000001ffff0000ffc000003007800000000000fffe00007fc000000200000000000000fffe00007fc0000000100000000000007ffc0000ffec000000fb0000000000001ffc0000ff8c000001ff0000000000001ffc00007f98000007ff8000000000001ff000007f9800000fffc000000000001fe000007f00000007ffc000000000001fc000003e00000007ffe000000000003fc000003c000000079fc000000000003f000000000000000007c000000000003e0000000000000000038020000000003c0000000000000000000040000000003800000000000000000000800000000070000000000000000000000000000000700000000000000000000000000000007000000000000000000000000000000030000000000000000000000",W=128,R0=4,ROWS=48;
  function isLand(lat,lon){var y=Math.floor((90-lat)/180*64)-R0;if(y<0||y>=ROWS)return false;var x=Math.floor((lon+180)/360*W);x=(x%W+W)%W;
    var hx=parseInt(LAND.charAt(y*32+(x>>2)),16);return (hx>>(3-(x&3)))&1;}
  var pts=[],step=1.9;
  for(var lat=-58;lat<=80;lat+=step){var n=Math.max(1,Math.round(360*Math.cos(lat*Math.PI/180)/step));
    for(var i=0;i<n;i++){var lon=-180+i*360/n;if(isLand(lat,lon))pts.push(v(lat,lon));}}
  function v(lat,lon){var a=lat*Math.PI/180,b=lon*Math.PI/180;return [Math.cos(a)*Math.sin(b),Math.sin(a),Math.cos(a)*Math.cos(b)];}
  var S=[-23.96,-46.33],SV=v(S[0],S[1]);
  var dest=[[29.7,-95.3],[40.7,-74],[51.9,4.5],[39.5,-.4],[53.5,10],[-34.6,-58.4],[-33,-71.6],[19.2,-96.1],[44.4,8.9],[-29.9,31],[6.5,3.4],[-12,-77],[45.5,-73.6],[38.7,-9.1],[33.6,-7.6],[-8.8,13.2],[10.4,-75.5],[25.8,-80.2]];
  var arcs=dest.map(function(p,k){var B=v(p[0],p[1]),dot=SV[0]*B[0]+SV[1]*B[1]+SV[2]*B[2],om=Math.acos(Math.max(-1,Math.min(1,dot))),seg=[];
    for(var j=0;j<=48;j++){var t=j/48,s=Math.sin(om),a=Math.sin((1-t)*om)/s,b=Math.sin(t*om)/s,h=1+Math.sin(t*Math.PI)*Math.min(om,1.3)*.13;
      seg.push([(a*SV[0]+b*B[0])*h,(a*SV[1]+b*B[1])*h,(a*SV[2]+b*B[2])*h]);}
    return {p:seg,off:k*.37%1,spd:.08+(k%5)*.018};});
  var dpr=Math.min(w.devicePixelRatio||1,1.75),cw,ch,cx,cy,R,mob;
  function size(){var r=cv.getBoundingClientRect();cw=r.width;ch=r.height;cv.width=cw*dpr;cv.height=ch*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);
    mob=cw<900;if(mob){R=Math.min(cw*.62,ch*.36);cx=cw*.62;cy=ch*.27;}else{R=Math.min(ch*.42,cw*.3);cx=cw*.73;cy=ch*.52;}}
  size();w.addEventListener("resize",size);
  var yaw0=(32)*Math.PI/180,tilt=.1,mx=0,my=0,tmx=0,tmy=0;
  if(fine)w.addEventListener("pointermove",function(e){tmx=(e.clientX/w.innerWidth-.5);tmy=(e.clientY/w.innerHeight-.5);},{passive:true});
  function proj(p,cy_,sy,ct,st){var x=p[0]*cy_+p[2]*sy,z=-p[0]*sy+p[2]*cy_,y=p[1];var y2=y*ct-z*st,z2=y*st+z*ct;return [cx+x*R,cy-y2*R,z2];}
  var running=true,vis=true,t0=performance.now();
  function draw(now){var t=Math.max(0,(now-t0)/1000);mx+=(tmx-mx)*.04;my+=(tmy-my)*.04;
    var yaw=yaw0+Math.sin(t*.07)*.45+mx*.5,tl=tilt+my*.25,cyw=Math.cos(yaw),syw=Math.sin(yaw),ct=Math.cos(tl),st=Math.sin(tl);
    ctx.clearRect(0,0,cw,ch);
    var g=ctx.createRadialGradient(cx-R*.35,cy-R*.4,R*.1,cx,cy,R*1.25);g.addColorStop(0,"rgba(200,21,27,.20)");g.addColorStop(.6,"rgba(120,12,16,.08)");g.addColorStop(1,"rgba(0,0,0,0)");
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R*1.25,0,6.283);ctx.fill();
    ctx.strokeStyle="rgba(255,255,255,.08)";ctx.lineWidth=1;ctx.beginPath();ctx.arc(cx,cy,R,0,6.283);ctx.stroke();
    var a=mob?.55:1;
    for(var i=0;i<pts.length;i++){var q=proj(pts[i],cyw,syw,ct,st);if(q[2]<-.05){ctx.fillStyle="rgba(255,255,255,"+(.05*a)+")";ctx.fillRect(q[0],q[1],1,1);continue;}
      var al=(.18+q[2]*.62)*a;ctx.fillStyle="rgba(235,236,240,"+al.toFixed(3)+")";var s=1+q[2]*1.1;ctx.fillRect(q[0]-s/2,q[1]-s/2,s,s);}
    for(var k=0;k<arcs.length;k++){var A=arcs[k],P=A.p,head=(t*A.spd+A.off)%1.6;ctx.lineWidth=1.1;
      var prev=null;for(var j=0;j<P.length;j++){var q2=proj(P[j],cyw,syw,ct,st);if(prev&&q2[2]>-.02&&prev[2]>-.02){var tt=j/P.length,on=tt<head;
          ctx.strokeStyle=on?"rgba(255,90,95,"+(.55*a)+")":"rgba(255,255,255,"+(.06*a)+")";ctx.beginPath();ctx.moveTo(prev[0],prev[1]);ctx.lineTo(q2[0],q2[1]);ctx.stroke();}prev=q2;}
      if(head<=1){var idx=Math.min(P.length-1,Math.floor(head*P.length)),hp=proj(P[idx],cyw,syw,ct,st);if(hp[2]>0){ctx.fillStyle="rgba(255,200,200,"+a+")";ctx.beginPath();ctx.arc(hp[0],hp[1],2.2,0,6.283);ctx.fill();}}
      var e=proj(P[P.length-1],cyw,syw,ct,st);if(e[2]>0){ctx.fillStyle="rgba(255,255,255,"+(.7*a)+")";ctx.beginPath();ctx.arc(e[0],e[1],1.8,0,6.283);ctx.fill();}}
    var sp=proj(SV,cyw,syw,ct,st);if(sp[2]>0){var pr=(t%2)/2;ctx.strokeStyle="rgba(255,90,95,"+(1-pr)*.8+")";ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(sp[0],sp[1],4+pr*18,0,6.283);ctx.stroke();
      ctx.fillStyle="#FF5A5F";ctx.beginPath();ctx.arc(sp[0],sp[1],4,0,6.283);ctx.fill();
      if(!mob){ctx.font="600 12px system-ui,sans-serif";ctx.fillStyle="rgba(255,255,255,.9)";ctx.fillText("SANTOS",sp[0]+10,sp[1]+4);}}
    if(running&&vis&&!RM)requestAnimationFrame(draw);}
  requestAnimationFrame(draw);
  if("IntersectionObserver" in w)new IntersectionObserver(function(es){var was=vis;vis=es[0].isIntersecting;if(vis&&!was&&!RM)requestAnimationFrame(draw);}).observe(cv);
  d.addEventListener("visibilitychange",function(){var was=running;running=!d.hidden;if(running&&!was&&vis&&!RM)requestAnimationFrame(draw);});
})();}

/* ---------- Vídeos controlados pelo scroll (hero e takes) ---------- */
(function(){
var scrubs=[].slice.call(d.querySelectorAll("[data-scrub]"));
if(RM||!scrubs.length)return;
var mq=w.matchMedia("(max-width: 900px)"),conn=navigator.connection,save=conn&&conn.saveData;
function clamp(x){return x<0?0:x>1?1:x;}
var S=scrubs.map(function(el){return {el:el,v:el.querySelector("video"),hero:el.classList.contains("hero-pin"),cur:0,tgt:0,loaded:false,
  inn:el.querySelector(".hero-in"),hero_el:el.querySelector(".hero"),hud:el.querySelector(".hero-hud"),copy:el.querySelector(".take-copy")};});
function load(s){if(s.loaded||!s.v||save)return;s.loaded=true;var v=s.v;
  v.src=(mq.matches&&v.getAttribute("data-src-m"))||v.getAttribute("data-src");v.preload="auto";
  v.addEventListener("loadeddata",function(){v.classList.add("ready");kick();},{once:true});
  v.load();var pr=v.play();if(pr&&pr.then)pr.then(function(){v.pause();kick();}).catch(function(){});}
if("IntersectionObserver" in w){var vio=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)S.forEach(function(s){if(s.el===e.target)load(s);});});},{rootMargin:"100% 0px"});
  S.forEach(function(s){vio.observe(s.el);});}else S.forEach(load);
var raf=0;function kick(){if(!raf)raf=requestAnimationFrame(tick);}
w.addEventListener("scroll",kick,{passive:true});w.addEventListener("resize",kick);
function tick(){raf=0;var vh=w.innerHeight,busy=false;
  S.forEach(function(s){var r=s.el.getBoundingClientRect();if(r.bottom<-vh||r.top>vh*2)return;
    s.tgt=clamp(-r.top/Math.max(1,r.height-vh));s.cur+=(s.tgt-s.cur)*.2;if(Math.abs(s.tgt-s.cur)>.0005)busy=true;else s.cur=s.tgt;
    var v=s.v;if(v&&v.readyState>=2&&v.duration&&!v.seeking){var t=s.cur*(v.duration-.05);if(Math.abs(v.currentTime-t)>.02)v.currentTime=t;}
    if(s.hero){var f=clamp((s.cur-.38)/.34);
      if(s.inn){s.inn.style.opacity=(1-f).toFixed(3);s.inn.style.transform="translate3d(0,"+(-f*70).toFixed(1)+"px,0)";}
      s.hero_el.style.setProperty("--out",(clamp((s.cur-.8)/.2)*.6).toFixed(3));if(s.hud)s.hud.style.setProperty("--p",s.cur.toFixed(3));}
    else if(s.copy){var o=Math.min(clamp((s.cur-.12)/.2),clamp((.92-s.cur)/.2));s.copy.style.setProperty("--o",o.toFixed(3));}});
  if(busy)kick();}
kick();
})();

/* ---------- Cenas do contêiner: vídeo real + cards presos na lateral ----------
   Cada vídeo teve a lateral do contêiner rastreada quadro a quadro (_tools/track.py);
   os dados vêm inline em #crate-track. Os cards seguem o quadro que o vídeo mostra. */
(function(){
var tel=d.getElementById("crate-track"),cs=[].slice.call(d.querySelectorAll("[data-crate]"));
if(!tel||!cs.length)return;
var TR=JSON.parse(tel.textContent),VW=1920,VH=1080;
var FW={"crate":.8,"crate-blue":.8,"take-3":.76};
Object.keys(TR).forEach(function(k){var T=TR[k],B=T.box;for(var i=0;i<T.frames;i++){if(!B[i])B[i]=B[i-1]||B[T.hold];}});
var mq=w.matchMedia("(max-width: 900px)"),conn=navigator.connection,save=conn&&conn.saveData;
function clamp(x){return x<0?0:x>1?1:x;}
var C=cs.map(function(el){var k=el.getAttribute("data-crate"),T=TR[k];return {el:el,k:k,T:T,st:el.querySelector(".crate-stage"),v:el.querySelector("video"),po:el.querySelector(".crate-poster"),
  f:el.querySelector(".crate-face"),cur:.5,tgt:.5,shown:T.hold,want:T.hold,loaded:false,L:null};});
function layout(c){var W=c.st.clientWidth,H=c.st.clientHeight,mob=mq.matches,hb=c.T.box[c.T.hold],s,ox,oy;
  if(mob){s=.92*W/(hb[2]*VW);}else{s=Math.max(W/VW,H/VH,Math.min((FW[c.k]||.7)*W/(hb[2]*VW),.68*H/(hb[3]*VH)));}
  var vw=VW*s,vh=VH*s;
  ox=W/2-(hb[0]+hb[2]/2)*vw;oy=(mob?.5:.56)*H-(hb[1]+hb[3]/2)*vh;
  if(!mob){ox=Math.min(0,Math.max(W-vw,ox));oy=Math.min(0,Math.max(H-vh,oy));}
  [c.po,c.v].forEach(function(m){m.style.width=vw+"px";m.style.height=vh+"px";m.style.left=ox+"px";m.style.top=oy+"px";});
  c.L={vw:vw,vh:vh,ox:ox,oy:oy,fw:hb[2]*vw,fh:hb[3]*vh,hb:hb};c.f.style.width=c.L.fw+"px";c.f.style.height=c.L.fh+"px";place(c,c.shown);}
function place(c,i){var L=c.L;if(!L)return;var b=c.T.box[Math.max(0,Math.min(c.T.frames-1,i))],hb=L.hb;
  var cx=b[0]+b[2]/2,cy=b[1]+b[3]/2;
  if(b[1]<.006)cy=b[1]+b[3]-hb[3]/2;else if(b[1]+b[3]>.994)cy=b[1]+hb[3]/2;   /* lateral cortada pela borda do quadro */
  if(b[0]<.006)cx=b[0]+b[2]-hb[2]/2;else if(b[0]+b[2]>.994)cx=b[0]+hb[2]/2;
  var x=L.ox+cx*L.vw-L.fw/2,y=L.oy+cy*L.vh-L.fh/2;
  c.f.style.transform="translate3d("+x.toFixed(1)+"px,"+y.toFixed(1)+"px,0)";}
C.forEach(layout);
w.addEventListener("resize",function(){C.forEach(layout);});
if(RM)return;
function load(c){if(c.loaded||save)return;c.loaded=true;var v=c.v,FPS=c.T.fps||24;
  v.src=(mq.matches&&v.getAttribute("data-src-m"))||v.getAttribute("data-src");v.preload="auto";
  v.addEventListener("loadeddata",function(){v.classList.add("ready");c.shown=c.want;place(c,c.shown);kick();},{once:true});
  if(v.requestVideoFrameCallback){var cb=function(now,meta){if(v.classList.contains("ready")){c.shown=Math.round(meta.mediaTime*FPS);place(c,c.shown);}v.requestVideoFrameCallback(cb);};v.requestVideoFrameCallback(cb);c.rvfc=true;}
  v.load();var pr=v.play();if(pr&&pr.then)pr.then(function(){v.pause();kick();}).catch(function(){});}
if("IntersectionObserver" in w){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)C.forEach(function(c){if(c.el===e.target)load(c);});});},{rootMargin:"80% 0px"});
  C.forEach(function(c){io.observe(c.el);});}else C.forEach(load);
var raf=0;function kick(){if(!raf)raf=requestAnimationFrame(tick);}
w.addEventListener("scroll",kick,{passive:true});
function tick(){raf=0;var vh=w.innerHeight,busy=false;
  C.forEach(function(c){var r=c.el.getBoundingClientRect();if(r.bottom<-vh||r.top>vh*2)return;
    c.tgt=clamp(-r.top/Math.max(1,r.height-vh));c.cur+=(c.tgt-c.cur)*.22;if(Math.abs(c.tgt-c.cur)>.0005)busy=true;else c.cur=c.tgt;
    var N=c.T.frames,FPS=c.T.fps||24;c.want=Math.round(c.cur*(N-1));var v=c.v;
    if(v.classList.contains("ready")){if(!v.seeking){var t=(c.want+.5)/FPS;if(Math.abs(v.currentTime-t)>.5/FPS)v.currentTime=t;}
      if(!c.rvfc){c.shown=c.want;place(c,c.shown);}}});
  if(busy)kick();}
kick();
})();

/* ---------- WhatsApp tracking ---------- */
d.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest('a[href*="wa.me"]');if(a)w.dataLayer.push({event:"whatsapp_click",page:location.pathname,label:a.getAttribute("data-wa")||"link"});});

/* ---------- Map facade ---------- */
var mb=d.querySelector("[data-map]");
if(mb)mb.addEventListener("click",function(){var f=d.createElement("iframe");f.src=mb.getAttribute("data-map");f.title="Mapa: RS Assessoria Aduaneira, Av. Ana Costa, 146, Santos/SP";f.loading="lazy";f.referrerPolicy="no-referrer-when-downgrade";mb.parentNode.replaceChild(f,mb);});

/* ---------- Form -> e-mail (FormSubmit) ---------- */
var form=d.getElementById("form-contato");
if(form){var st=form.querySelector(".form-status"),btn=form.querySelector('button[type="submit"]');
  function fieldErr(name,msg){var f=form.querySelector('[name="'+name+'"]').closest(".field");f.classList.toggle("invalid",!!msg);f.querySelector(".err").textContent=msg||"";}
  var FALLBACK=' Se preferir, chame no <a href="https://wa.me/5513996140042" target="_blank" rel="noopener">WhatsApp (13) 99614-0042</a> ou ligue (13) 3219-8720.';
  form.addEventListener("submit",function(e){e.preventDefault();
    if(form.website&&form.website.value){return;}
    var n=form.nome.value.trim(),em=form.email.value.trim(),tel=form.telefone.value.trim(),sv=form.servico.value,msg=form.mensagem.value.trim(),ok=true;
    fieldErr("nome",n.length<2?"Informe seu nome.":"");if(n.length<2)ok=false;
    var emOk=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em);fieldErr("email",emOk?"":"Informe um e-mail válido para a resposta.");if(!emOk)ok=false;
    var tOk=tel.replace(/\D/g,"").length>=10;fieldErr("telefone",tOk?"":"Informe telefone com DDD.");if(!tOk)ok=false;
    fieldErr("mensagem",msg.length<5?"Conte em poucas palavras o que precisa.":"");if(msg.length<5)ok=false;
    if(!ok){st.className="form-status bad";st.textContent="Confira os campos destacados.";return;}
    btn.disabled=true;var old=btn.innerHTML;btn.innerHTML="Enviando…";st.className="form-status";st.textContent="";
    var data={nome:n,empresa:form.empresa.value.trim()||"-",telefone:tel,email:em,assunto:sv,mensagem:msg,pagina:location.href,
      _subject:"Novo contato pelo site: "+sv+" ("+n+")",_template:"table",_captcha:"false",_replyto:em,_honey:""};
    fetch(form.getAttribute("data-endpoint"),{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return {};}).then(function(j){return {ok:r.ok,j:j};});})
      .then(function(res){var sOk=res.ok&&(res.j.success===true||res.j.success==="true");
        if(sOk){form.reset();st.className="form-status ok";st.textContent="Mensagem enviada! A equipe da RS responde em breve no e-mail informado.";w.dataLayer.push({event:"form_submit",page:location.pathname,servico:sv});}
        else{st.className="form-status bad";st.innerHTML="Não conseguimos enviar agora."+FALLBACK;}})
      .catch(function(){st.className="form-status bad";st.innerHTML="Falha de conexão ao enviar."+FALLBACK;})
      .then(function(){btn.disabled=false;btn.innerHTML=old;});
  });}

/* ---------- Filtro do blog ---------- */
d.querySelectorAll("[data-filter]").forEach(function(b){b.addEventListener("click",function(){var f=b.getAttribute("data-filter");
  d.querySelectorAll("[data-filter]").forEach(function(x){x.classList.toggle("on",x===b);x.setAttribute("aria-pressed",x===b?"true":"false");});
  d.querySelectorAll(".blog-list .post-card").forEach(function(c){c.classList.toggle("is-hidden",f!=="*"&&c.getAttribute("data-cat")!==f);});});});

/* ---------- Cookies / Consent Mode v2 ---------- */
var GA_ID="";/* preencher com o ID do GA4 (G-XXXX) quando houver */
function loadGA(){if(!GA_ID||w.__ga)return;w.__ga=1;var s=d.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+GA_ID;d.head.appendChild(s);w.gtag("js",new Date());w.gtag("config",GA_ID);}
var ck=d.querySelector(".cookie"),choice=null;try{choice=localStorage.getItem("rs_consent");}catch(e){}
function setH(){if(ck&&ck.classList.contains("show")){d.body.classList.add("has-cookie");root.style.setProperty("--cookie-h",(w.innerWidth<640?ck.offsetHeight+16:0)+"px");}else{d.body.classList.remove("has-cookie");}}
if(choice==="granted"){w.gtag("consent","update",{ad_storage:"granted",analytics_storage:"granted",ad_user_data:"granted",ad_personalization:"granted"});loadGA();}
else if(!choice&&ck){setTimeout(function(){ck.classList.add("show");setH();},900);}
if(ck)ck.addEventListener("click",function(e){var b=e.target.closest("[data-consent]");if(!b)return;var v=b.getAttribute("data-consent");
  try{localStorage.setItem("rs_consent",v);}catch(err){}
  if(v==="granted"){w.gtag("consent","update",{ad_storage:"granted",analytics_storage:"granted",ad_user_data:"granted",ad_personalization:"granted"});loadGA();}
  ck.classList.remove("show");setH();});
w.addEventListener("resize",setH);
})();
