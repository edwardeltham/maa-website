(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

/* webinar bar */
var wb=$('#webinarBar');
if(wb&&Date.now()>Date.parse('2026-10-31T12:00:00+05:30'))wb.hidden=true;

/* year */
var yr=$('#yr');if(yr)yr.textContent=new Date().getFullYear();

/* scroll progress + header shadow */
var pg=$('.progress'),hd=$('header.site');
function onScroll(){
  var h=document.documentElement,max=h.scrollHeight-h.clientHeight;
  if(pg)pg.style.transform='scaleX('+(max>0?h.scrollTop/max:0)+')';
  if(hd)hd.classList.toggle('stuck',h.scrollTop>8);
}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* burger */
var bg=$('.burger'),mn=$('#menu');
if(bg&&mn){
  var set=function(o){mn.classList.toggle('open',o);bg.setAttribute('aria-expanded',o)};
  bg.addEventListener('click',function(){set(bg.getAttribute('aria-expanded')!=='true')});
  mn.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
  addEventListener('keydown',function(e){if(e.key==='Escape')set(false)});
}

/* reveal */
var rv=$$('.rv');
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  rv.forEach(function(el){io.observe(el)});
}else rv.forEach(function(el){el.classList.add('in')});

/* count up */
function countUp(el){
  var t=parseFloat(el.dataset.count),suf=el.dataset.suffix||'',n=0;
  if(reduce){el.textContent=t.toLocaleString('en-IN')+suf;return}
  var t0=performance.now();
  (function f(now){var p=Math.min((now-t0)/1400,1);n=Math.round(t*(1-Math.pow(1-p,3)));
    el.textContent=n.toLocaleString('en-IN')+suf;if(p<1)requestAnimationFrame(f)})(t0);
}
var cu=$$('[data-count]');
if('IntersectionObserver' in window){
  var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){countUp(e.target);io2.unobserve(e.target)}})},{threshold:.5});
  cu.forEach(function(el){io2.observe(el)});
}else cu.forEach(countUp);

/* countdown */
$$('.count[data-target]').forEach(function(c){
  var T=Date.parse(c.dataset.target);
  function tick(){
    var d=Math.max(0,T-Date.now()),v={d:Math.floor(d/864e5),h:Math.floor(d/36e5)%24,m:Math.floor(d/6e4)%60,s:Math.floor(d/1e3)%60};
    for(var k in v){var n=$('[data-u='+k+']',c);if(n)n.textContent=String(v[k]).padStart(2,'0')}
  }
  tick();setInterval(tick,1000);
});

/* rotating word */
var rot=$('#rot');
if(rot&&!reduce){
  var W=['bench','classroom','playground','assembly line','tiffin box','batch'],i=0;
  setInterval(function(){rot.style.opacity=0;setTimeout(function(){i=(i+1)%W.length;rot.textContent=W[i];rot.style.opacity=1},300)},2400);
}

/* tilt */
var tl=$('#tilt');
if(tl&&!reduce&&matchMedia('(hover:hover)').matches){
  tl.addEventListener('pointermove',function(e){var r=tl.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
    tl.style.transform='perspective(900px) rotateY('+x*7+'deg) rotateX('+-y*7+'deg)'});
  tl.addEventListener('pointerleave',function(){tl.style.transform=''});
}

/* helpers */
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function tabs(box,attr,fn){
  var bs=$$('['+attr+']',box);
  function pick(b){bs.forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});fn(b.getAttribute(attr))}
  bs.forEach(function(b){b.addEventListener('click',function(){pick(b)})});
  box.addEventListener('keydown',function(e){
    var k=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!k)return;
    var i=bs.indexOf(document.activeElement);if(i<0)return;var n=bs[(i+k+bs.length)%bs.length];n.focus();pick(n);e.preventDefault()});
  return pick;
}

/* role picker */
var ROLES={
 india:{h:'Right here, right now',p:'You can be in the room, or on the campus, within a day.',l:[['Be a resource person','resource-persons'],['Mentor a student','mentorship'],['Join the Homecoming','']]},
 abroad:{h:'Near or far, you are still a Mahatma kid',p:'Your distance is an asset. Students and fellow alumni heading your way need you.',l:[['Guide those moving abroad','abroad'],['Be a guest on Alumni Talks','vodcast'],['Pledge to a school project','csr']]},
 employer:{h:'You can open doors',p:'A role, a project or a referral changes a young person\'s year.',l:[['Offer an internship','internships'],['Post a job','jobs'],['Bring your company\'s CSR','csr']]},
 young:{h:'Fresh from the gate',p:'You remember the corridors best. Start with your batch, then pay it forward.',l:[['Find your batch','join'],['Share your career story','careers'],['Help organise events','competition']]},
 organiser:{h:'Every reunion needs a planner',p:'We need people who make things happen quietly and well.',l:[['Run an inter-school event','competition'],['Join a committee','team'],['Produce the vodcast','vodcast']]}
};
var ro=$('#roleOut');
if(ro){
  tabs($('#roles'),'data-role',function(k){
    var r=ROLES[k];
    ro.innerHTML='<h3>'+esc(r.h)+'</h3><p>'+esc(r.p)+'</p><div class="lnks">'+r.l.map(function(x){
      var href=x[1]===''?'homecoming.html':x[1]==='join'?'join.html':x[1]==='team'?'team.html':'programmes.html#'+x[1];
      return '<a class="lnk" href="'+href+'">'+esc(x[0])+' &rarr;</a>'}).join('')+'</div>';
  })($('#roles .chip.on'));
}

/* value tabs */
var VAL={
 alumni:['Alumni','Belong again.',['Reconnect with your batch and your teachers','A trusted network across cities and countries','A meaningful way to give back, on your terms']],
 students:['Students','See what is possible.',['Mentors who have walked the same road','Real internships, jobs and career insight','Role models they can meet, hear and ask']],
 school:['The school','Grow with its own family.',['Expertise in class from alumni resource persons','Support for needs, with open accounts','A proud, engaged community behind every child']],
 community:['The community','Share the good.',['Projects that reach beyond the campus','Eight schools united in friendly rivalry','Stories that inspire the whole neighbourhood']]
};
var vp=$('#vpanel');
if(vp)tabs($('#vtabs'),'data-v',function(k){
  var v=VAL[k];
  vp.innerHTML='<h3>'+esc(v[0])+': <span class="hand">'+esc(v[1])+'</span></h3><ul>'+v[2].map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>';
})($('#vtabs .tab.on'));

/* programme filters */
var fl=$('#filters');
if(fl){
  var NOTES={all:'Nine programmes. Pick the ones that sound like you.',guide:'Alumni who have walked the road show the way.',doors:'Opening the first door for someone else.',back:'Back to the school and the community.',celebrate:'Stories and friendly rivalry all year.'};
  var pf=tabs(fl,'data-f',function(f){
    $$('.prog').forEach(function(p){p.hidden=!(f==='all'||p.dataset.g===f)});
    var n=$('#fnote');if(n)n.textContent=NOTES[f]||'';
  });
  var q=new URLSearchParams(location.search).get('f'),b=q&&$('[data-f="'+q+'"]',fl);
  pf(b||$('.tab.on',fl));
  if(location.hash){var t=$(location.hash);if(t&&t.classList.contains('prog')){t.hidden=false;var m=$('.more',t);setTimeout(function(){t.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'})},200);if(m)m.click()}}
}
$$('.more').forEach(function(b){
  b.addEventListener('click',function(){
    var d=b.nextElementSibling,o=b.getAttribute('aria-expanded')!=='true';
    b.setAttribute('aria-expanded',o);d.classList.toggle('open',o);
    b.firstChild.nodeValue=o?'Close ':'How it works ';
  });
});

/* kurals */
var K=[
 ['அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு','As A is the first of all letters, so the Ancient One is first in the world.','Kural 1'],
 ['செய்யாமல் செய்த உதவிக்கு வையகமும்\nவானகமும் ஆற்றல் அரிது','Help given when none was asked is worth more than earth and heaven.','Kural 101'],
 ['இன்னா செய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயம் செய்து விடல்','Answer a wrong with kindness, and let them feel the shame.','Kural 314'],
 ['பகுத்துண்டு பல்லுயிர் ஓம்புதல் நூலோர்\nதொகுத்தவற்றுள் எல்லாம் தலை','To share your meal and care for all that lives is the first of all duties.','Kural 322'],
 ['கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக','Learn well what is worth learning, then live by it.','Kural 391'],
 ['கேடில் விழுச்செல்வம் கல்வி ஒருவற்கு\nமாடல்ல மற்றை யவை','Learning is the one wealth that never fails; all else is not true wealth.','Kural 400']
];
var kt=$('#kt');
if(kt){
  var ki=Math.floor(Date.now()/864e5)%K.length;
  var show=function(){var k=K[ki];kt.textContent=k[0];kt.style.whiteSpace='pre-line';$('#km').textContent=k[1];$('#kr').textContent=k[2]};
  show();
  var kn=$('#knext');if(kn)kn.addEventListener('click',function(){ki=(ki+1)%K.length;show()});
}

/* mail forms */
$$('.mailform').forEach(function(f){
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var lines=[];
    $$('input,textarea,select',f).forEach(function(x){
      if((x.type==='checkbox'||x.type==='radio')&&!x.checked)return;
      if(x.value&&x.type!=='submit'){var L=x.closest('label'),lab=x.getAttribute('aria-label')||(L?L.firstChild.nodeValue.trim():'')||x.name||'';lines.push((lab?lab+': ':'')+x.value)}
    });
    location.href='mailto:'+f.dataset.to+'?subject='+encodeURIComponent(f.dataset.subject||'')+'&body='+encodeURIComponent(lines.join('\n'));
  });
});

/* bell */
var bell=$('#bell');
if(bell)bell.addEventListener('click',function(){
  bell.classList.remove('ring');void bell.offsetWidth;bell.classList.add('ring');
  try{
    var A=window.AudioContext||window.webkitAudioContext,c=new A(),t=c.currentTime;
    [880,1318,1760].forEach(function(f,i){
      var o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=f;
      g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.22/(i+1),t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+2.2);
      o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+2.3);
    });
  }catch(e){}
});

/* placeholders: swap in photos */
$$('.ph[data-src]').forEach(function(f){
  var im=new Image();im.alt=f.dataset.alt||'';im.loading='lazy';
  im.onload=function(){f.classList.add('has');f.appendChild(im)};im.src=f.dataset.src;
});

/* todo links */
$$('a[data-todo]').forEach(function(a){
  a.addEventListener('click',function(e){if(a.getAttribute('href')==='#'){e.preventDefault();alert('Link coming soon: '+a.dataset.todo)}});
});
})();
