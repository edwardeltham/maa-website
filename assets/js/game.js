/* Late for school: a small endless-runner. Reach the gate before the 8:30 bell, or say sorry on the dais. */
(function(){
'use strict';
var box=document.getElementById('gameBox'),cv=document.getElementById('game');
if(!box||!cv||!cv.getContext)return;
var ctx=cv.getContext('2d');
var $=function(id){return document.getElementById(id)};
var over=$('gOver'),res=$('gRes'),kick=$('gKick'),ttl=$('gTitle'),msg=$('gMsg'),btn=$('gBtn'),shr=$('gShare');

var C={navy:'#1F2A44',soft:'#3B4660',gold:'#D4A017',deep:'#B8860B',ink:'#8A6508',goldSoft:'#E8CE85',ivory:'#FFF9EA',cream:'#FBF3DF',white:'#FFFFFF',skin:'#8D5A3B',path:'#E9DCB8'};
var SERIF="'Playfair Display',Georgia,serif",HAND="'Caveat',cursive",SANS="'Jost',system-ui,sans-serif";

/* tuning: 40 real seconds = 8:20 to 8:30. A clean run reaches the gate at about 8:29:10 and each stumble
   costs about 1.2 s, so two stumbles still make it and a third means the dais. Aimed at roughly 6 in 10 players being late. */
var H=450,W=800,GY=372,LIMIT=40,DIST=14230,METRES=1200;
var G=2400,JUMP=860,CUT=380,STUN=1.4,SAFE=1.9;
var SORRY="Sorry Ma'am. I will not come late again!";

var state='title',t=0,st=0,dist=0,hits=0,lastNow=0,ready=false;
var p={y:GY,vy:0,ground:true,stun:0,safe:0,phase:0,buf:0,held:false};
var obs=[],fx=[],nextAt=0;
var sorries=0,best=null;
try{sorries=+sessionStorage.getItem('maaSorries')||0}catch(e){}
try{var b=localStorage.getItem('maaLateBest');best=b?+b:null}catch(e){}

function px(){return Math.round(W*0.18)}
function speed(){return Math.min(460,300+5*t)}
function hash(i){var x=Math.sin(i*12.9898+78.233)*43758.5453;return x-Math.floor(x)}
function rnd(a,b){return a+Math.random()*(b-a)}
function clock(sec){var s=Math.min(600,Math.max(0,sec*15)),m=20+Math.floor(s/60),ss=Math.floor(s%60);return '8:'+m+':'+(ss<10?'0':'')+ss}
function metresLeft(){return Math.max(0,Math.round((DIST-dist)/DIST*METRES))}

/* ---------- sizing */
function resize(){
  var r=cv.getBoundingClientRect();if(!r.width||!r.height)return;
  var dpr=Math.min(window.devicePixelRatio||1,2);
  W=Math.round(H*r.width/r.height);
  cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);
  var k=cv.width/W;ctx.setTransform(k,0,0,k,0,0);
  if(state!=='run')draw();
}
addEventListener('resize',resize);

/* ---------- sound (same bell as the footer) */
var ac=null;
function bell(long){
  try{
    ac=ac||new (window.AudioContext||window.webkitAudioContext)();
    var c=ac,t0=c.currentTime,n=long?4:1;
    for(var k=0;k<n;k++)[880,1318,1760].forEach(function(f,i){
      var o=c.createOscillator(),g=c.createGain(),s=t0+k*.28;o.type='sine';o.frequency.value=f;
      g.gain.setValueAtTime(0,s);g.gain.linearRampToValueAtTime(.18/(i+1),s+.01);g.gain.exponentialRampToValueAtTime(.0001,s+(long?1.2:2));
      o.connect(g);g.connect(c.destination);o.start(s);o.stop(s+2.1);
    });
  }catch(e){}
}

/* ---------- obstacles */
var TYPES={
  puddle:{w:74,h:8,say:'Splash!'},
  stone:{w:34,h:26,say:'Ouch!'},
  bag:{w:40,h:30,say:'Oops!'},
  dog:{w:58,h:36,vx:50,say:'Woof!'},
  cycle:{w:74,h:50,vx:90,say:'Clang!'},
  cow:{w:98,h:66,say:'Moo!'}
};
function pick(){
  var pool=['puddle','stone','puddle','bag'];
  if(t>5)pool.push('dog','dog');
  if(t>10)pool.push('cycle','cow');
  if(t>18)pool.push('cow','cycle','dog');
  return pool[Math.floor(Math.random()*pool.length)];
}
function spawn(){
  var k=pick(),d=TYPES[k];
  obs.push({k:k,x:W+20,w:d.w,h:d.h,vx:d.vx||0,a:Math.random()*6});
  nextAt=dist+speed()*rnd(.95,1.85)+d.w;
}

/* ---------- game flow */
function reset(){
  t=0;st=0;dist=0;hits=0;obs=[];fx=[];nextAt=700;ready=false;
  p.y=GY;p.vy=0;p.ground=true;p.stun=0;p.safe=0;p.phase=0;p.buf=0;
}
function start(){
  reset();state='run';hide();
  try{box.focus({preventScroll:true})}catch(e){}
  lastNow=performance.now();requestAnimationFrame(loop);
}
function press(){
  if(state==='title'){start();return}
  if(state==='run'){p.buf=.14;p.held=true}
}
function release(){p.held=false;if(state==='run'&&p.vy<-CUT)p.vy=-CUT}

function hide(){over.hidden=true;if(res)res.textContent=''}
function show(cls,k,h,m,b){
  over.className='g-over '+cls;kick.textContent=k;ttl.textContent=h;msg.textContent=m;btn.textContent=b;
  if(shr)shr.hidden=!(navigator.share&&cls==='end');
  over.hidden=false;if(res)res.textContent=cls==='end'?m:'';
  if(cls==='end')setTimeout(function(){try{btn.focus({preventScroll:true})}catch(e){}},50);
}

function finishLate(){
  sorries++;try{sessionStorage.setItem('maaSorries',sorries)}catch(e){}
  var m=metresLeft();
  show('end','8:30 AM. The bell has rung.','Late for assembly',
    'You were '+m+' m from the gate'+(hits?', after '+hits+' stumble'+(hits>1?'s':''):'')+'. '+(sorries>1?'That is sorry number '+sorries+' today.':'Up on the dais you go.'),'Run again');
  share='I was late for school and said sorry on the dais at morning assembly. Can you beat the 8:30 bell?';
}
function finishWin(){
  var secs=Math.round(t*15),isBest=best===null||secs<best;
  if(isBest){best=secs;try{localStorage.setItem('maaLateBest',secs)}catch(e){}}
  show('end','Present, Ma’am!','On time!',
    'You reached the gate at '+clock(t)+' AM with '+(hits?hits+' stumble'+(hits>1?'s':''):'no stumbles')+'. '+(isBest?'Your best yet.':'Your best: '+clock(best/15)+' AM.'),'Run again');
  share='I beat the 8:30 bell and reached the Mahatma gate at '+clock(t)+' AM. Can you?';
}
var share='';

/* ---------- update */
function update(dt){
  if(state==='run'){
    t+=dt;
    var v=p.stun>0?70:speed();
    p.stun=Math.max(0,p.stun-dt);p.safe=Math.max(0,p.safe-dt);
    dist+=v*dt;p.phase+=v*dt/26;
    p.buf=Math.max(0,p.buf-dt);
    if(p.buf>0&&p.ground&&p.stun<=0){p.vy=-JUMP;p.ground=false;p.buf=0;if(!p.held)p.vy=-CUT*1.35}
    if(!p.ground){p.vy+=G*dt;p.y+=p.vy*dt;if(p.y>=GY){p.y=GY;p.vy=0;p.ground=true}}
    if(dist>=nextAt&&DIST-dist>W+200)spawn();
    var x0=px();
    for(var i=obs.length-1;i>=0;i--){
      var o=obs[i];o.x-=(v+(p.stun>0?0:o.vx))*dt;o.a+=dt*8;
      if(o.x+o.w<-40){obs.splice(i,1);continue}
      if(p.safe<=0&&x0+9>o.x+8&&x0-9<o.x+o.w-8&&p.y>GY-o.h+4&&p.y-80<GY){
        hits++;p.stun=STUN;p.safe=SAFE;p.vy=Math.min(p.vy,0);
        fx.push({x:x0,y:GY-100,t:0,s:TYPES[o.k].say});
      }
    }
    if(dist>=DIST){state='win';st=0;bell(false);finishWin();return}
    if(t>=LIMIT){state='bell';st=0;bell(true)}
  }else{
    st+=dt;
    if(state==='bell'&&st>1.6){state='late';st=0}
    if(state==='late'&&!ready&&st>typeDone()+.5){ready=true;finishLate()}
  }
  for(var j=fx.length-1;j>=0;j--){fx[j].t+=dt;if(fx[j].t>1)fx.splice(j,1)}
}
function typeDone(){return 2.6+SORRY.length/20}

/* ---------- drawing helpers */
function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath()}
function circ(x,y,r){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2)}
function line(x1,y1,x2,y2,w,c){ctx.strokeStyle=c;ctx.lineWidth=w;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke()}

function gopuram(x,base,h,col){
  var tiers=7,th=h/tiers,w0=h*.62;ctx.fillStyle=col;
  for(var i=0;i<tiers;i++){
    var a=w0*(1-i*.1),b=w0*(1-(i+1)*.1),y=base-i*th;
    ctx.beginPath();ctx.moveTo(x-a/2,y);ctx.lineTo(x+a/2,y);ctx.lineTo(x+b/2,y-th+2);ctx.lineTo(x-b/2,y-th+2);ctx.closePath();ctx.fill();
  }
  var top=base-h;rr(x-w0*.2,top-10,w0*.4,12,6);ctx.fill();
  for(var k=-1;k<=1;k++){circ(x+k*w0*.12,top-14,4);ctx.fill()}
}
function coconut(x,base,h,col){
  ctx.strokeStyle=col;ctx.lineWidth=6;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(x,base);ctx.quadraticCurveTo(x+18,base-h*.5,x+8,base-h);ctx.stroke();
  ctx.lineWidth=4;
  for(var i=0;i<6;i++){var a=-Math.PI+i*Math.PI/5,ex=x+8+Math.cos(a)*44,ey=base-h+Math.sin(a)*14+16;
    ctx.beginPath();ctx.moveTo(x+8,base-h);ctx.quadraticCurveTo((x+8+ex)/2,base-h-18,ex,ey);ctx.stroke()}
}
function layer(off,spacing,fn){
  var s=Math.floor(off/spacing)-1,e=s+Math.ceil(W/spacing)+3;
  for(var i=s;i<e;i++)fn(i*spacing-off,i);
}

function street(d){
  var g=ctx.createLinearGradient(0,0,0,GY);g.addColorStop(0,C.ivory);g.addColorStop(1,C.cream);
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  /* sun */
  ctx.fillStyle='rgba(212,160,23,.18)';circ(W*.82,92,46);ctx.fill();
  /* far: temple towers of Madurai */
  layer(d*.06,620,function(x,i){gopuram(x+hash(i)*200,GY-40,150+hash(i+3)*70,'rgba(212,160,23,.28)')});
  /* houses */
  layer(d*.32,150,function(x,i){
    var hh=60+hash(i)*70,ww=110+hash(i+9)*30;
    ctx.fillStyle='rgba(31,42,68,'+(.08+hash(i+2)*.06)+')';ctx.fillRect(x,GY-hh,ww,hh);
    ctx.fillStyle='rgba(255,249,234,.7)';
    for(var r=0;r<2;r++)for(var c=0;c<3;c++)if(hash(i*7+r*3+c)>.35)ctx.fillRect(x+14+c*32,GY-hh+14+r*26,14,14);
  });
  /* trees */
  layer(d*.55,260,function(x,i){if(hash(i+5)>.3)coconut(x+hash(i)*80,GY,110+hash(i+1)*60,'rgba(59,70,96,.38)')});
  /* footpath and road */
  ctx.fillStyle=C.path;ctx.fillRect(0,GY,W,14);
  ctx.fillStyle=C.navy;ctx.fillRect(0,GY+14,W,H-GY-14);
  ctx.fillStyle=C.gold;var o=d%90;for(var x=-o;x<W;x+=90)ctx.fillRect(x,GY+44,46,5);
  ctx.fillStyle='rgba(255,255,255,.08)';ctx.fillRect(0,GY+14,W,3);
}

function school(x){
  var top=GY-232,w=330;
  ctx.fillStyle=C.cream;ctx.fillRect(x-40,top,w+80,232);
  ctx.strokeStyle=C.navy;ctx.lineWidth=3;ctx.strokeRect(x-40,top,w+80,232);
  ctx.fillStyle='rgba(31,42,68,.12)';
  for(var r=0;r<2;r++)for(var c=0;c<5;c++)ctx.fillRect(x-20+c*76,top+60+r*58,40,38);
  /* name board */
  ctx.fillStyle=C.navy;ctx.fillRect(x-20,top+12,w+40,36);
  ctx.fillStyle=C.gold;ctx.font='600 22px '+SERIF;ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText('MAHATMA SCHOOL',x+w/2,top+31);
  /* gate */
  var gx=x+w/2-80;
  ctx.fillStyle=C.navy;ctx.fillRect(gx-14,GY-150,18,150);ctx.fillRect(gx+156,GY-150,18,150);
  ctx.strokeStyle=C.gold;ctx.lineWidth=8;ctx.beginPath();ctx.arc(gx+80,GY-150,94,Math.PI*1.08,Math.PI*1.92);ctx.stroke();
  ctx.fillStyle=C.gold;circ(gx-5,GY-156,9);ctx.fill();circ(gx+165,GY-156,9);ctx.fill();
}

function kid(x,y,mode,ph,s){
  s=s||1;ctx.save();ctx.translate(x,y);ctx.scale(s,s);
  var air=mode==='air',run=mode==='run'||air,sw=run?Math.sin(ph):0,bow=mode==='sorry'?1:0;
  if(mode==='stun')ctx.rotate(-.18+Math.sin(ph*3)*.04);
  /* legs */
  var f1=run?sw*15:-4,f2=run?-sw*15:4,ly=air?-8:0;
  line(-3,-30,f1,ly-3,5,C.skin);line(3,-30,f2,ly-3,5,C.skin);
  ctx.fillStyle=C.navy;rr(f1-6,ly-6,12,6,3);ctx.fill();rr(f2-6,ly-6,12,6,3);ctx.fill();
  /* shorts */
  ctx.fillStyle=C.navy;rr(-10,-40,20,13,3);ctx.fill();
  /* bag */
  ctx.fillStyle=C.gold;rr(-21,-64,11,24,4);ctx.fill();ctx.strokeStyle=C.deep;ctx.lineWidth=1.5;ctx.stroke();
  /* shirt */
  ctx.save();ctx.translate(0,-40);ctx.rotate(bow*.12);
  ctx.fillStyle=C.white;rr(-10,-25,20,27,5);ctx.fill();ctx.strokeStyle=C.navy;ctx.lineWidth=1.4;ctx.stroke();
  line(0,-23,0,-10,3,C.gold);
  /* arms */
  if(mode==='cheer'){line(-8,-20,-18,-44,4,C.skin);line(8,-20,18,-44,4,C.skin)}
  else if(mode==='sorry'||mode==='stand'){line(-8,-20,-2,-6,4,C.skin);line(8,-20,2,-6,4,C.skin)}
  else{line(-6,-20,-sw*13,-4,4,C.skin);line(6,-20,sw*13,-4,4,C.skin)}
  /* head */
  ctx.translate(0,-34+bow*2);
  ctx.fillStyle=C.skin;circ(0,0,10);ctx.fill();
  ctx.fillStyle=C.navy;ctx.beginPath();ctx.arc(0,-1,10.5,Math.PI*1.05,Math.PI*1.95);ctx.fill();
  ctx.fillStyle=C.navy;circ(4,bow?2:0,1.5);ctx.fill();
  if(mode==='cheer'){ctx.strokeStyle=C.navy;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(3,3,3.5,.1,Math.PI-.1);ctx.stroke()}
  ctx.restore();
  if(mode==='stun'){ctx.fillStyle=C.gold;for(var k=0;k<3;k++){var a=ph*2+k*2.1;circ(Math.cos(a)*14,-90+Math.sin(a)*4,3);ctx.fill()}}
  ctx.restore();
}

function obstacle(o){
  var x=o.x,w=o.w,h=o.h;
  if(o.k==='puddle'){
    ctx.fillStyle='rgba(59,70,96,.55)';ctx.beginPath();ctx.ellipse(x+w/2,GY+4,w/2,7,0,0,Math.PI*2);ctx.fill();
    line(x+w*.3,GY+2,x+w*.5,GY+2,2,'rgba(255,255,255,.6)');
  }else if(o.k==='stone'){
    ctx.fillStyle=C.deep;rr(x,GY-h,w,h,6);ctx.fill();ctx.fillStyle='rgba(255,255,255,.2)';rr(x+5,GY-h+4,w*.4,5,2);ctx.fill();
  }else if(o.k==='bag'){
    ctx.fillStyle=C.soft;rr(x,GY-h,w,h,7);ctx.fill();ctx.fillStyle=C.gold;ctx.fillRect(x+6,GY-h+10,w-12,5);
    ctx.strokeStyle=C.soft;ctx.lineWidth=3;ctx.beginPath();ctx.arc(x+w/2,GY-h,8,Math.PI,0);ctx.stroke();
  }else if(o.k==='dog'){
    var bob=Math.sin(o.a)*2,lg=Math.sin(o.a)*6;
    line(x+12,GY-12,x+12+lg,GY-1,4,C.soft);line(x+42,GY-12,x+42-lg,GY-1,4,C.soft);
    ctx.fillStyle=C.soft;ctx.beginPath();ctx.ellipse(x+28,GY-20+bob,22,10,0,0,Math.PI*2);ctx.fill();
    circ(x+6,GY-30+bob,9);ctx.fill();
    ctx.fillStyle=C.navy;ctx.beginPath();ctx.moveTo(x+3,GY-38+bob);ctx.lineTo(x+9,GY-37+bob);ctx.lineTo(x+5,GY-28+bob);ctx.fill();
    line(x+50,GY-24+bob,x+58,GY-34+bob+lg*.4,3,C.soft);
  }else if(o.k==='cycle'){
    var r=15,sp=o.a;ctx.strokeStyle=C.navy;ctx.lineWidth=3;
    circ(x+r,GY-r,r);ctx.stroke();circ(x+w-r,GY-r,r);ctx.stroke();
    line(x+r,GY-r,x+r+Math.cos(sp)*r,GY-r+Math.sin(sp)*r,1.5,C.navy);line(x+w-r,GY-r,x+w-r+Math.cos(sp)*r,GY-r+Math.sin(sp)*r,1.5,C.navy);
    ctx.strokeStyle=C.gold;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x+r,GY-r);ctx.lineTo(x+32,GY-38);ctx.lineTo(x+w-22,GY-38);ctx.lineTo(x+w-r,GY-r);ctx.moveTo(x+32,GY-38);ctx.lineTo(x+38,GY-r);ctx.lineTo(x+w-22,GY-38);ctx.stroke();
    line(x+28,GY-44,x+38,GY-44,4,C.navy);line(x+w-22,GY-38,x+w-18,GY-50,3,C.navy);line(x+w-24,GY-50,x+w-12,GY-50,3,C.navy);
  }else if(o.k==='cow'){
    var sw=Math.sin(o.a*.3)*3;
    line(x+18,GY-24,x+18,GY,6,C.soft);line(x+30,GY-24,x+30,GY,6,C.soft);line(x+66,GY-24,x+66,GY,6,C.soft);line(x+78,GY-24,x+78,GY,6,C.soft);
    ctx.fillStyle=C.white;rr(x+8,GY-58,82,36,16);ctx.fill();ctx.strokeStyle=C.navy;ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle=C.navy;ctx.beginPath();ctx.ellipse(x+52,GY-44,12,8,.3,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=C.white;rr(x-6,GY-64+sw,24,26,9);ctx.fill();ctx.strokeStyle=C.navy;ctx.stroke();
    ctx.fillStyle=C.goldSoft;rr(x-6,GY-48+sw,18,10,5);ctx.fill();
    line(x+2,GY-64+sw,x-4,GY-78+sw,4,C.gold);line(x+12,GY-64+sw,x+18,GY-78+sw,4,C.gold);
    ctx.fillStyle=C.navy;circ(x+4,GY-56+sw,2);ctx.fill();
    line(x+90,GY-52,x+98,GY-30+sw,2.5,C.navy);
  }
}

function hud(){
  var late=t>LIMIT-6.5,flash=late&&Math.floor(t*4)%2===0;
  ctx.fillStyle=flash?C.gold:C.navy;rr(14,14,150,58,12);ctx.fill();
  ctx.fillStyle=flash?C.navy:C.white;ctx.textAlign='left';ctx.textBaseline='alphabetic';
  ctx.font='600 26px '+SERIF;ctx.fillText(clock(t),28,48);
  ctx.font='500 12px '+SANS;ctx.fillStyle=flash?C.navy:C.goldSoft;ctx.fillText('AM · BELL AT 8:30',28,64);
  /* progress to the gate */
  var bx=184,bw=Math.max(80,W-bx-30),by=36;
  ctx.fillStyle='rgba(31,42,68,.14)';rr(bx,by,bw,8,4);ctx.fill();
  var f=Math.min(1,dist/DIST);ctx.fillStyle=C.gold;rr(bx,by,Math.max(8,bw*f),8,4);ctx.fill();
  ctx.fillStyle=C.navy;circ(bx+bw*f,by+4,8);ctx.fill();ctx.fillStyle=C.white;circ(bx+bw*f,by+4,3.5);ctx.fill();
  ctx.fillStyle=C.navy;ctx.fillRect(bx+bw-2,by-12,4,26);ctx.fillStyle=C.gold;ctx.fillRect(bx+bw+2,by-12,14,9);
  ctx.font='500 14px '+SANS;ctx.fillStyle=C.soft;ctx.textAlign='left';
  ctx.fillText('Gate in '+metresLeft()+' m',bx,by+30);
  if(hits){ctx.textAlign='right';ctx.fillText(hits+' stumble'+(hits>1?'s':''),bx+bw,by+30)}
}

function floaters(){
  ctx.textAlign='center';ctx.font='700 30px '+HAND;
  fx.forEach(function(f){ctx.globalAlpha=1-f.t;ctx.fillStyle=C.ink;ctx.fillText(f.s,f.x,f.y-f.t*30)});
  ctx.globalAlpha=1;
}

function bubble(x,y,w,txt,tx,ty,size){
  ctx.font='700 '+size+'px '+HAND;
  var words=txt.split(' '),lines=[],cur='';
  words.forEach(function(wd){var tst=cur?cur+' '+wd:wd;if(ctx.measureText(tst).width>w-32&&cur){lines.push(cur);cur=wd}else cur=tst});
  if(cur)lines.push(cur);
  var lh=size*1.05,h=Math.max(1,lines.length)*lh+24;
  ctx.fillStyle=C.white;ctx.strokeStyle=C.navy;ctx.lineWidth=2.5;
  rr(x,y,w,h,16);ctx.fill();ctx.stroke();
  var ax=Math.max(x+24,Math.min(x+w-24,tx));
  ctx.beginPath();ctx.moveTo(ax-10,y+h-1);ctx.lineTo(tx,ty);ctx.lineTo(ax+10,y+h-1);ctx.fill();
  ctx.beginPath();ctx.moveTo(ax-10,y+h);ctx.lineTo(tx,ty);ctx.lineTo(ax+10,y+h);ctx.stroke();
  ctx.fillStyle=C.navy;ctx.textAlign='left';ctx.textBaseline='top';
  lines.forEach(function(l,i){ctx.fillText(l,x+16,y+12+i*lh)});
  ctx.textBaseline='alphabetic';
}

function teacher(x,y){
  ctx.save();ctx.translate(x,y);
  ctx.fillStyle=C.gold;ctx.beginPath();ctx.moveTo(-14,-62);ctx.lineTo(14,-62);ctx.lineTo(22,0);ctx.lineTo(-22,0);ctx.closePath();ctx.fill();
  ctx.fillStyle=C.navy;ctx.fillRect(-22,-6,44,6);
  ctx.strokeStyle=C.navy;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-12,-62);ctx.lineTo(16,-24);ctx.stroke();
  line(-12,-50,8,-40,4,C.skin);line(12,-50,-8,-40,4,C.skin);
  ctx.fillStyle=C.skin;circ(0,-74,11);ctx.fill();
  ctx.fillStyle=C.navy;ctx.beginPath();ctx.arc(0,-75,11.5,Math.PI,0);ctx.fill();circ(-12,-72,6);ctx.fill();
  ctx.fillStyle=C.gold;circ(0,-80,1.8);ctx.fill();
  ctx.restore();
}

function assembly(s){
  var stageY=280,mx=Math.round(W*.5),tx=Math.round(W*.8);
  ctx.fillStyle=C.cream;ctx.fillRect(0,0,W,H);
  /* banner */
  var bw=Math.min(W-60,460);ctx.fillStyle=C.navy;ctx.fillRect(W/2-bw/2,24,bw,48);
  ctx.fillStyle=C.gold;ctx.font='600 24px '+SERIF;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('Morning Assembly',W/2,49);
  ctx.textBaseline='alphabetic';
  line(W/2-bw/2-10,24,W/2-bw/2-10,stageY,3,'rgba(31,42,68,.2)');line(W/2+bw/2+10,24,W/2+bw/2+10,stageY,3,'rgba(31,42,68,.2)');
  /* dais */
  ctx.fillStyle=C.gold;ctx.fillRect(40,stageY,W-80,8);
  ctx.fillStyle=C.navy;ctx.fillRect(40,stageY+8,W-80,70);
  ctx.fillStyle=C.gold;for(var x=40;x<W-40;x+=36){ctx.beginPath();ctx.arc(x+18,stageY+8,18,0,Math.PI);ctx.fill()}
  /* mic */
  line(mx+26,stageY,mx+26,stageY-62,3,C.navy);line(mx+14,stageY,mx+38,stageY,4,C.navy);
  ctx.fillStyle=C.navy;rr(mx+20,stageY-74,12,16,5);ctx.fill();
  teacher(tx,stageY);
  /* student walks to the mic, then bows */
  var walk=Math.min(1,Math.max(0,(s-.6)/1.6)),kx=-20+(mx-(-20))*walk,mode=walk<1?'run':'sorry';
  kid(kx,stageY,mode,s*9,1.15);
  if(s>.6&&s<2.4)bubble(Math.min(W-200,tx-170),110,170,'Late again?',tx-6,stageY-96,26);
  if(s>2.4){
    var n=Math.min(SORRY.length,Math.floor((s-2.4)*20)),bwid=Math.min(330,W-40);
    bubble(Math.max(20,Math.min(W-bwid-20,mx-bwid/2)),92,bwid,SORRY.slice(0,n)||'…',mx,stageY-104,30);
  }
  /* the whole school, watching */
  for(var r=2;r>=0;r--){
    var y=H-12-r*30,sc=1-r*.12,step=46*sc;
    for(var i=0,xx=(r%2)*step/2-10;xx<W+30;i++,xx+=step){
      var b=Math.sin(s*3+i*1.7+r)*1.5*(s>2.4?1:0);
      ctx.fillStyle=C.white;rr(xx-17*sc,y-6*sc+b,34*sc,30*sc,12*sc);ctx.fill();ctx.strokeStyle='rgba(31,42,68,.25)';ctx.lineWidth=1;ctx.stroke();
      ctx.fillStyle=C.navy;circ(xx,y-16*sc+b,12*sc);ctx.fill();
    }
  }
  if(s>2.4+SORRY.length/20&&s<typeDone()+3){ctx.font='700 26px '+HAND;ctx.fillStyle=C.ink;ctx.textAlign='left';ctx.fillText('giggle',30,H-110);ctx.textAlign='right';ctx.fillText('hehe',W-30,H-118)}
  if(s<.5){ctx.fillStyle='rgba(31,42,68,'+(1-s/.5)+')';ctx.fillRect(0,0,W,H)}
}

/* ---------- draw */
function draw(){
  if(state==='late'){assembly(st);return}
  street(dist);
  var gx=px()+(DIST-dist)-165;
  if(gx<W+60)school(gx);
  obs.forEach(obstacle);
  var mode=state==='win'?'cheer':state==='title'?'stand':state==='bell'?'stand':p.stun>0?'stun':p.ground?'run':'air';
  var y=state==='win'?GY-Math.abs(Math.sin(st*6))*16:p.y;
  if(!(p.safe>0&&p.stun<=0&&Math.floor(p.safe*12)%2))kid(px(),y,mode,p.phase);
  if(state!=='title')hud();
  floaters();
  if(state==='bell'){
    ctx.fillStyle='rgba(31,42,68,'+Math.min(.6,st)+')';ctx.fillRect(0,0,W,H);
    ctx.fillStyle=C.gold;ctx.textAlign='center';ctx.font='700 '+(64+Math.sin(st*30)*4)+'px '+HAND;ctx.fillText('Brrrring!',W/2,H/2);
    ctx.font='500 18px '+SANS;ctx.fillStyle=C.white;ctx.fillText('8:30 AM. Assembly has begun.',W/2,H/2+36);
  }
}

function loop(now){
  var dt=Math.min(.05,(now-lastNow)/1000);lastNow=now;
  update(dt);draw();
  if(state==='run'||state==='bell'||state==='late'||state==='win')requestAnimationFrame(loop);
}

/* ---------- input */
function isBtn(e){return e.target&&e.target.closest&&e.target.closest('button,a')}
box.addEventListener('pointerdown',function(e){if(isBtn(e))return;e.preventDefault();press()});
addEventListener('pointerup',release);addEventListener('pointercancel',release);
addEventListener('keydown',function(e){
  if(isBtn(e)||e.altKey||e.ctrlKey||e.metaKey)return;
  if(e.code==='Space'||e.key===' '||e.key==='ArrowUp'||e.key==='w'||e.key==='W'){
    if(state==='title'||state==='run'){e.preventDefault();if(!e.repeat)press()}
  }
});
addEventListener('keyup',function(e){if(e.code==='Space'||e.key===' '||e.key==='ArrowUp'||e.key==='w'||e.key==='W')release()});
btn.addEventListener('click',function(){if(state==='title')start();else{state='title';start()}});
if(shr)shr.addEventListener('click',function(){try{navigator.share({title:'Late for school',text:share,url:location.href}).catch(function(){})}catch(e){}});

/* ---------- first frame */
reset();resize();
if(document.fonts&&document.fonts.load)Promise.all([document.fonts.load('700 30px Caveat'),document.fonts.load('600 24px "Playfair Display"')]).then(function(){if(state==='title')draw()},function(){});
})();
