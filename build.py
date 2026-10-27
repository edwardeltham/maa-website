# Static site generator for the MAA website. Run: python3 build.py  (outputs *.html next to this file)
import html, json
REG="https://www.mahatmaschools.com"
MAIL="alumni@mahatmaschools.com"
CAM='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>'
ARW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BELL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 17V11a6 6 0 1 1 12 0v6l1.5 2h-15z"/><path d="M10 21h4"/></svg>'

def ph(label,ratio="r43",extra="",src=""):
    d=f' data-src="{src}"' if src else ''
    return f'<figure class="ph {ratio} {extra}"{d}>{CAM}<b>{label}</b><small>Photo placeholder</small></figure>'

PAGES=[("index.html","Home"),("premalatha.html","Ma'am"),("about.html","About"),("programmes.html","Programmes"),("homecoming.html","Homecoming"),("team.html","Team"),("join.html","Join")]

def head(title,desc,page):
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1F2A44">
<link rel="icon" href="assets/img/logo.png">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Jost:wght@400;500;600&family=Noto+Sans+Tamil:wght@500&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head><body data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="bar" id="webinarBar">Live webinar · <b>Sat 31 Oct, 10 AM</b> · Premalatha Ma'am addresses alumni · <a href="#" data-todo="YouTube link">Watch on YouTube</a></div>
<header class="site"><div class="wrap nav">
<a class="brand" href="index.html" aria-label="Mahatma Alumni Association, home"><img src="assets/img/logo.png" alt="" width="54" height="54"><span><b>Mahatma Alumni<br>Association</b><small>Once a Mahatmite</small></span></a>
<nav aria-label="Main"><ul id="menu">{''.join(f'<li><a href="{u}"'+(' aria-current="page"' if u==page else '')+f'>{n}</a></li>' for u,n in PAGES)}<li><a class="btn solid" href="{REG}" style="padding:10px 20px;color:#fff;border-bottom:2px solid var(--navy)">Register</a></li></ul>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></nav>
</div></header>
<main id="main">'''

def foot():
    return f'''</main>
<footer><div class="wrap">
<div class="grid">
<div><a class="brand" href="index.html"><img src="assets/img/logo.png" alt="" width="64" height="64"><span><b>Mahatma Alumni<br>Association</b></span></a>
<p class="mt" style="font-size:1rem">By the alumni, for the alumni. Connect. Contribute. Celebrate.</p>
<p class="hand mt">Once a Mahatmite, always a Mahatmite.</p></div>
<div><h4>Explore</h4><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for u,n in PAGES)}</ul></div>
<div><h4>Get involved</h4><ul><li><a href="{REG}">Register for Homecoming</a></li><li><a href="join.html#raise">Put your hand up</a></li><li><a href="programmes.html">All programmes</a></li><li><a href="homecoming.html#faq">FAQ</a></li></ul></div>
<div><h4>Say hello</h4><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="#" data-todo="Instagram">Instagram</a></li><li><a href="#" data-todo="YouTube">YouTube</a></li><li><a href="#" data-todo="LinkedIn">LinkedIn</a></li></ul>
<p class="mt"><button class="bell" id="bell" type="button">{BELL} Ring the bell</button></p></div>
</div>
<div class="fine"><span>© <span id="yr">2026</span> Mahatma Alumni Association. Independent and run by alumni.</span><span>Made with chalk dust and nostalgia. <a href="game.html">Late for school?</a></span></div>
</div></footer>
<script src="assets/js/main.js" defer></script>
</body></html>'''

# ---------- DATA
PROGS=[
 dict(id="mentorship",g="guide",t="Mentorship",tag="Guidance from someone who has walked the road, one conversation at a time.",
  how=["Mentors and mentees sign up with their field and goals","MAA matches them by field, city and interest","Monthly one-to-one talks for six months (proposed)"],
  give=["About one hour a month","Honest advice on studies, choices and first jobs","An introduction to their network"],
  gain=["Mentees find direction early","Mentors find purpose and perspective","Batches meet across years"],
  start="Starts 27 Dec: mentor and mentee sign-ups.",st="27 Dec"),
 dict(id="careers",g="guide",t="Careers",tag="Know what the work is really like, from people who do it.",
  how=["Alumni list their profession and field","Short talks, panels and Q&A in school and online","A directory by field, so students know whom to ask"],
  give=["A talk, a panel seat or a 15-minute call","An honest account of the path, detours included","Pointers on skills and courses to pick up"],
  gain=["Students meet careers they have never seen","Alumni become role models within reach","Better choices before the exam results"],
  start="Starts 27 Dec: alumni add their profession and field at sign-up.",st="27 Dec"),
 dict(id="abroad",g="guide",t="Moving abroad",tag="Someone who has already made the move, a message away.",
  how=["Alumni abroad register their country and city","One peer group per country for questions","Sessions on applications, moving and settling in"],
  give=["Their lessons from the first year","Pointers on applications and first weeks","A familiar face on arrival, where possible"],
  gain=["Fewer costly mistakes for those moving","A welcome waiting in the new city","Alumni abroad stay close to home"],
  start="Starts 27 Dec: alumni abroad register where they live. Peer guidance only, not legal or immigration advice.",st="27 Dec"),
 dict(id="internships",g="doors",t="Internships",tag="A first real experience, through people the school already trusts.",
  how=["Alumni businesses and teams list short internships","Students and young alumni apply through MAA","A mentor or contact checks in during the stint"],
  give=["A place, or a small project, for a few weeks","A supervisor who explains the work","Feedback and a reference at the end"],
  gain=["Early experience and a first reference","Businesses meet motivated young talent","The network proves itself in practice"],
  start="Starts 27 Dec: alumni employers register the openings they can offer.",st="27 Dec"),
 dict(id="jobs",g="doors",t="Jobs",tag="A warm introduction travels further than a résumé.",
  how=["Alumni post openings in their teams and companies","Job seekers share a short profile with MAA","Alumni refer, introduce and advise"],
  give=["An opening posted, or a referral made","A quick résumé review","A mock interview for a batchmate"],
  gain=["Job seekers get introductions, not cold applications","Employers meet candidates they can trust","Trust in the network keeps growing"],
  start="Starts after 27 Dec: an openings board and a profile list on the MAA platform.",st="After 27 Dec"),
 dict(id="resource-persons",g="back",t="Alumni as resource persons",tag="Our classrooms deserve our best people, and they are our alumni.",
  how=["Alumni pick a topic they know well","The school schedules visits through the year","Talks, workshops and demonstrations for students"],
  give=["A morning or an hour on campus","Expertise in their field, explained simply","A story from their own school days"],
  gain=["Students hear from working professionals","Teachers get fresh support in class","Alumni return to where it began"],
  start="Starts 25 and 26 Dec: School Visit Days, where alumni can offer a topic.",st="25–26 Dec"),
 dict(id="csr",g="back",t="CSR and community",tag="Giving back together, with a plan and open accounts.",
  how=["The school and alumni name the needs together","Projects are chosen, costed and tracked openly","Funds and volunteers come through MAA"],
  give=["Time and skills on a project","Funds, large or small","Their company's CSR support, where possible"],
  gain=["Students and the community see real results","Alumni employers find a meaningful local project","Open accounts build lasting trust"],
  start="Starts 27 Dec: pledges of time, skills and funds, and a shortlist of needs from the school.",st="27 Dec"),
 dict(id="vodcast",g="celebrate",t="Alumni Talks vodcast",tag="Our stories, told by us, in our own voices.",
  how=["A regular episode with one alumni guest, interviewed by students","School memories, a turning point and one lesson","Full episodes on the school YouTube channel, plus short clips"],
  give=["An hour of conversation as a guest","Nominations of batchmates with a story","Skills in hosting, editing or design"],
  gain=["Role models students can hear and see","Batches rediscover one another","A growing archive of the school's story"],
  start="Open call: guest nominations and a volunteer production team.",st="Open call"),
 dict(id="competition",g="celebrate",t="MAA inter-school competition",tag="Eight schools, one friendly rivalry, organised by alumni.",
  how=["Alumni design events: for example quiz, debate, sports, arts","Each of the 8 schools sends its teams","One finals day, alumni as organisers and judges"],
  give=["Time to organise, judge and coach","Prizes and sponsorship","Venues, equipment and refreshments"],
  gain=["Students get a stage and learn teamwork","Eight schools feel like one family","Alumni become organisers they remember"],
  start="Starts after 27 Dec: the council confirms the format and calendar; alumni volunteer to run events.",st="After 27 Dec"),
]
GROUPS={"guide":("A","Guide","Alumni who have walked the road show those who are about to."),
        "doors":("B","Open doors","Alumni open the first doors for the next ones through them."),
        "back":("C","Give back","Alumni return to the school and the community that raised them."),
        "celebrate":("D","Connect and celebrate","Stories and friendly rivalry that keep the family together all year.")}

def prog_card(p,compact=False):
    li=lambda a:''.join(f'<li>{html.escape(x)}</li>' for x in a)
    L,gn,_=GROUPS[p['g']]
    return f'''<article class="prog rv" id="{p['id']}" data-g="{p['g']}">
<div class="ptop"><span class="st{' open' if p['st']=='Open call' else ''}">{p['st']}</span><span class="gl">{L} · {gn}</span></div>
<h3>{p['t']}</h3><p>{p['tag']}</p>
<button class="more" type="button" aria-expanded="false">How it works {ARW}</button>
<div class="detail"><div class="cols3">
<div><h4>How it works</h4><ul>{li(p['how'])}</ul></div>
<div><h4>Alumni give</h4><ul>{li(p['give'])}</ul></div>
<div><h4>Everyone gains</h4><ul>{li(p['gain'])}</ul></div></div>
<p class="startnote">{html.escape(p['start'])}</p></div></article>'''

ROAD=[("25–26 Dec","School Visit Days","Alumni offer topics to teach and talk about."),
      ("27 Dec","Homecoming","All sign-ups open, the MAA app launches, pledges are collected."),
      ("January","Matching begins","Mentor matching starts, vodcast guests are chosen, an openings board is set up."),
      ("Feb–Mar","First visits and first jobs","Resource-person visits are scheduled, first internships and referrals happen, CSR needs are shortlisted."),
      ("Apr–Jun","Eight schools, one rivalry","The inter-school competition is planned and run; the first CSR project is reported.")]
def roadmap():
    items=''.join(f'<li class="rm rv"><span class="when">{w}</span><h3>{t}</h3><p>{d}</p></li>' for w,t,d in ROAD)
    return f'<ol class="roadmap">{items}</ol><p class="hand center mt">A proposed order of work, not a promise. Dates depend on school calendars and volunteers.</p>'

CCC=f'''<div class="cards3">
<article class="note-card rv"><div class="n">1</div><h3>Connect</h3><p>Find your batch. Find your people. Friends and teachers found again, mentors in your field, peers abroad who know the way.</p><p class="mt"><a class="lnk" href="programmes.html?f=guide">Mentorship · Careers · Moving abroad</a></p></article>
<article class="note-card rv"><div class="n">2</div><h3>Contribute</h3><p>Give back to the school and to each other. A classroom talk, an internship, a job opening, a project you can see and follow.</p><p class="mt"><a class="lnk" href="programmes.html?f=doors">Internships · Jobs · Resource persons · CSR</a></p></article>
<article class="note-card rv"><div class="n">3</div><h3>Celebrate</h3><p>Come home and make memories. Stories told in our own voices, and a friendly rivalry between eight schools.</p><p class="mt"><a class="lnk" href="programmes.html?f=celebrate">Vodcast · Inter-school competition · Homecoming</a></p></article></div>'''

VISION='A Mahatma family of 20,000+ alumni, connected for life, and growing the school that raised them.'
MISSION='To connect every alumnus with their batch, their teachers and each other; to contribute time, skills and support to the school and the community; and to celebrate where we began.'

HAND='''<section class="hands-sec"><div class="wrap"><div class="head"><div><p class="eyebrow">How to be part of it</p><h2>Six ways to put your hand up</h2></div><p>Every alumnus can do at least one. Every programme is optional, and you choose how much time to give.</p></div>
<div class="hands">
<div class="hand-item rv"><h3><small>01</small>Mentor</h3><p>An hour a month for a student or a younger alumnus.</p></div>
<div class="hand-item rv"><h3><small>02</small>Speaker</h3><p>A talk at school, or a seat on a career panel.</p></div>
<div class="hand-item rv"><h3><small>03</small>Employer</h3><p>An internship, an opening or a referral.</p></div>
<div class="hand-item rv"><h3><small>04</small>Guest or guide</h3><p>A vodcast story, or a guide for those moving abroad.</p></div>
<div class="hand-item rv"><h3><small>05</small>Organiser</h3><p>Run an event in the inter-school competition.</p></div>
<div class="hand-item rv"><h3><small>06</small>Supporter</h3><p>Sponsor a prize, a stall or a CSR project.</p></div></div>
<p class="mt2 center"><a class="btn solid" href="join.html#raise">Put your hand up {ARW}</a></p></div></section>'''.replace('{ARW}',ARW)

def countdown():
    return '''<div class="count" data-target="2026-12-27T09:00:00+05:30" aria-live="off"><div><b data-u="d">00</b><span>Days</span></div><div><b data-u="h">00</b><span>Hours</span></div><div><b data-u="m">00</b><span>Minutes</span></div><div><b data-u="s">00</b><span>Seconds</span></div></div>'''

KURAL='''<section class="chalk"><div class="wrap"><div class="grid2">
<div><p class="eyebrow">Morning assembly</p><h2>Kural of the day</h2><p class="mt">Before the first period, there was always a Thirukkural. Here is today's, in the voice you still hear in your head.</p></div>
<div class="board" id="kboard"><p class="kural" id="kt"></p><p class="kmean" id="km"></p><p class="kref" id="kr"></p><button class="btn" id="knext" type="button">Next kural {ARW}</button></div></div></div></section>'''.replace('{ARW}',ARW)

def polas(n=6,labels=None):
    labels=labels or ["Assembly line, [year]","Our favourite bench","The ground after the bell","Batch photo, [batch]","Teachers' day, [year]","Canteen, 11 o'clock"]
    return '<div class="polas">'+''.join(f'<figure class="pola rv"><span class="tape"></span>{ph("Memory "+str(i+1),"r43")}<figcaption>{labels[i%len(labels)]}</figcaption></figure>' for i in range(n))+'</div>'

# ---------- PAGES
out={}

# HOME
h=head("Mahatma Alumni Association · Connect. Contribute. Celebrate.","The alumni family of Mahatma School, Madurai. 20,000+ of us, one home. Connect, contribute, celebrate.","index.html")
h+=f'''
<section class="hero"><div class="wrap grid">
<div>
<p class="eyebrow rv">Mahatma Alumni Association</p>
<h1 class="rv mt">It began in a house with <span class="gold doodle">fewer than fifteen</span> children.</h1>
<p class="lede mt rv">Premalatha Ma'am started a school. Today more than 20,000 children have called it theirs, and she calls every one of them her own.</p>
<p class="hand mt rv" style="font-size:2.1rem">Come back to your <span class="rot" id="rot">bench</span>.</p>
<div class="cta rv"><a class="btn solid" href="premalatha.html">Meet Ma'am {ARW}</a><a class="btn line" href="homecoming.html">Homecoming · 27 Dec</a></div>
</div>
<div class="mam-frame rv" id="tilt">
<span class="note">Ma'am!</span>
{ph("Premalatha Ma'am — portrait","r45","arch")}
<div class="stamp">The one who<b>started it all</b></div>
</div></div></section>

<section class="roll"><div class="wrap"><div class="grid">
<div class="cell"><div class="num"><span data-count="20000">20,000</span><i>+</i></div><span>Alumni worldwide</span></div>
<div class="cell"><div class="num"><span data-count="8">8</span></div><span>Schools, one family</span></div>
<div class="cell"><div class="num"><span data-count="9">9</span></div><span>Programmes to join</span></div>
<div class="cell"><div class="num"><span data-count="1">1</span></div><span>Ma'am who started it</span></div></div></div></section>

<section class="feature"><div class="wrap grid">
<div class="rv">{ph("Ma'am with the children","r43")}</div>
<div><p class="eyebrow rv">A message from Ma'am</p>
<blockquote class="quote rv mt">“Add Ma'am's message to the alumni here.”<cite>Premalatha Ma'am, founder</cite></blockquote>
<p class="mt rv">From a house with fewer than 15 children to a school family of more than 20,000. Every alumnus carries a little of her in how they work and how they treat people.</p>
<p class="mt rv"><a class="btn solid" href="premalatha.html">Read Ma'am's story {ARW}</a></p></div></div></section>

<section><div class="wrap">
<div class="head"><div><p class="eyebrow">Why we exist</p><h2>Vision and mission</h2></div><p>A school's greatest work walks out of its gates every year. We are how it walks back in, together.</p></div>
<div class="vm">
<div class="vm-card rv"><span class="hand">Our vision</span><p class="big">{VISION}</p></div>
<div class="vm-card rv"><span class="hand">Our mission</span><p class="big">{MISSION}</p></div></div></div></section>

<section style="padding-top:0"><div class="wrap">
<div class="head"><div><p class="eyebrow">Our promise</p><h2>Connect. Contribute. Celebrate.</h2></div><p>Three ideas, nine programmes. Pick the ones that suit your life.</p></div>
{CCC}</div></section>

<section class="picker-sec"><div class="wrap">
<div class="head"><div><p class="eyebrow">What's in it for you?</p><h2>Tell us who you are</h2></div><p>Choose a role and see where you fit in.</p></div>
<div class="chips" role="tablist" id="roles">
<button class="chip on" role="tab" data-role="india">Alumnus in India</button>
<button class="chip" role="tab" data-role="abroad">Alumnus abroad</button>
<button class="chip" role="tab" data-role="employer">Employer or entrepreneur</button>
<button class="chip" role="tab" data-role="young">Recent alumnus</button>
<button class="chip" role="tab" data-role="organiser">Volunteer organiser</button></div>
<div class="role-out" id="roleOut" aria-live="polite"></div></div></section>

<section class="feature"><div class="wrap">
<div class="head"><div><p class="eyebrow">The value to everyone</p><h2>Four groups, one network</h2></div><p>None of this needs a large budget at the start. It needs names on a list, and 27 December is when the list begins.</p></div>
<div class="tabs" role="tablist" id="vtabs"><button class="tab on" role="tab" data-v="alumni">Alumni</button><button class="tab" role="tab" data-v="students">Students</button><button class="tab" role="tab" data-v="school">The school</button><button class="tab" role="tab" data-v="community">The community</button></div>
<div class="vpanel" id="vpanel" aria-live="polite"></div></div></section>

<section class="hc"><div class="wrap grid">
<div><p class="eyebrow">The big reunion</p><h2 class="mt">27 December 2026</h2>
<p class="mt">One day that starts everything else. Reconnect with your batch, see the MAA app launch, and put your name down for what you will do next.</p>
<p class="hand mt" style="font-size:1.9rem">Days until the last bell</p>{countdown()}
<div class="cta" style="display:flex;gap:14px;flex-wrap:wrap"><a class="btn gold" href="{REG}">Register now {ARW}</a><a class="btn line" href="homecoming.html">Plan your three days</a></div></div>
<div><ul class="facts">
<li><span>Date</span><span>Sunday, 27 December 2026</span></li>
<li><span>City</span><span>Madurai</span></li>
<li><span>Ticket</span><span>₹1,299 + GST</span></li>
<li><span>On the day</span><span>Programme · panel · networking · lunch · MAA app launch</span></li>
<li><span>Before it</span><span>School Visit Days, 25 and 26 Dec · free</span></li></ul></div></div></section>

{KURAL}

<section><div class="wrap">
<div class="head"><div><p class="eyebrow">Memory lane</p><h2>Do you remember this?</h2></div><p>Send us your photos from school days and we will pin them here.</p></div>
{polas(6)}
<p class="mt2 center"><a class="btn line" href="mailto:{MAIL}?subject=My%20school%20photo">Send us a photo {ARW}</a></p></div></section>

<section class="chalk"><div class="wrap center">
<p class="hand" style="color:var(--gold)">Running late again?</p>
<h2 class="mt">Beat the 8:30 bell</h2>
<p class="mt">A one-minute game. Race to the school gate past puddles, stray dogs and cows, or say sorry on the dais in front of the whole assembly.</p>
<p class="mt2"><a class="btn gold" href="game.html">Play Late for school {ARW}</a></p></div></section>

<section class="feature"><div class="wrap">
<div class="head"><div><p class="eyebrow">From one day to a year-round network</p><h2>The first six months</h2></div><p>A proposed plan. Light programmes start first, heavier ones follow once the team is steady.</p></div>
{roadmap()}</div></section>

{HAND}
'''+foot()
out["index.html"]=h

# PREMALATHA
h=head("Premalatha Ma'am · Mahatma Alumni Association","The story of Premalatha Ma'am, who started Mahatma School in a house with fewer than 15 children and now has 20,000+ alumni.","premalatha.html")
h+=f'''
<section class="pagehead"><div class="wrap grid2h">
<div><p class="eyebrow">Our Ma'am</p><h1 class="mt">The woman who started with a house.</h1>
<p class="lede mt">Fewer than fifteen children. One relentless woman. And a school family that now numbers more than twenty thousand.</p></div>
<div class="mam-frame" style="margin:0 0 0 auto">{ph("Premalatha Ma'am — portrait","r45","arch")}<div class="stamp">Founder<b>Ma'am</b></div></div></div></section>

<section><div class="wrap"><div class="head"><div><p class="eyebrow">Her story</p><h2>How a house became a school</h2></div><p>A timeline for you to complete with Ma'am's own dates and photos.</p></div>
<ol class="roadmap tl">
<li class="rm rv"><span class="when">[Year]</span><h3>A house</h3><p>The school begins in a house, with fewer than 15 children. Add a line and a photo here.</p></li>
<li class="rm rv"><span class="when">[Year]</span><h3>The first batch</h3><p>The first children leave with their first board results. Add the story here.</p></li>
<li class="rm rv"><span class="when">[Year]</span><h3>The school grows</h3><p>New classrooms, new teachers, new campuses. Add a line here.</p></li>
<li class="rm rv"><span class="when">[Year]</span><h3>Eight schools</h3><p>One family across eight schools. Add a line here.</p></li>
<li class="rm rv"><span class="when">Today</span><h3>20,000+ children</h3><p>She calls every one of them her own.</p></li></ol></div></section>

<section class="feature"><div class="wrap grid2h">
<div class="rv">{ph("Ma'am reading in assembly","r43")}</div>
<div><p class="eyebrow">Every morning</p><h2 class="mt">The voice you still hear</h2>
<p class="mt">Ask any alumnus for their first memory of school and many will mention the morning assembly: the Thirukkural, the quiet, and Ma'am's voice. Add your own memories below and we will place them here.</p>
<p class="mt todo">Add a short passage about Ma'am's morning readings (Thirukkural, Kamba Ramayanam) here.</p></div></div></section>

<section><div class="wrap"><div class="head"><div><p class="eyebrow">What she taught us</p><h2>Lessons that outlasted the syllabus</h2></div><p>Alumni, tell us yours. We will add the best to this page.</p></div>
<div class="cards3">
<article class="note-card rv"><div class="n">1</div><h3>[Lesson one]</h3><p>A line from an alumnus about something Ma'am taught that stayed with them.</p></article>
<article class="note-card rv"><div class="n">2</div><h3>[Lesson two]</h3><p>Another memory, in an alumnus's own words, with their batch.</p></article>
<article class="note-card rv"><div class="n">3</div><h3>[Lesson three]</h3><p>One more, from a different decade of the school.</p></article></div></div></section>

<section class="feature" id="write"><div class="wrap grid2h">
<div><p class="eyebrow">Write to Ma'am</p><h2 class="mt">Tell her what you have become.</h2>
<p class="mt">Every alumnus has a note they never sent. Write it now, and we will make sure Ma'am reads it.</p></div>
<form class="mailform" data-to="{MAIL}" data-subject="A note for Ma'am">
<label>Your name<input name="name" required></label><label>Batch<input name="batch" placeholder="e.g. 2008"></label>
<label>What would you like to tell Ma'am?<textarea name="msg" rows="5" required></textarea></label>
<button class="btn solid" type="submit">Write to Ma'am {ARW}</button><p class="fine2">This opens your email app with your note ready to send.</p></form></div></section>

{KURAL}
<section><div class="wrap"><div class="head"><div><p class="eyebrow">Memory lane</p><h2>Ma'am through the years</h2></div></div>{polas(3,["Ma'am, [year]","Annual day, [year]","With the first batch"])}</div></section>
'''+foot()
out["premalatha.html"]=h

# ABOUT
h=head("About · Mahatma Alumni Association","Our vision, mission and the three ideas that guide the Mahatma Alumni Association: connect, contribute, celebrate.","about.html")
h+=f'''
<section class="pagehead"><div class="wrap"><p class="eyebrow">About MAA</p><h1 class="mt">By the alumni, for the alumni.</h1><p class="lede mt">The Mahatma Alumni Association is an independent, alumni-run body that keeps 20,000+ Mahatmites connected to each other and to the school that raised them.</p></div></section>

<section><div class="wrap"><div class="vm">
<div class="vm-card rv"><span class="hand">Our vision</span><p class="big">{VISION}</p></div>
<div class="vm-card rv"><span class="hand">Our mission</span><p class="big">{MISSION}</p></div></div></div></section>

<section class="feature"><div class="wrap"><div class="head"><div><p class="eyebrow">Why it matters</p><h2>A school's greatest work walks out of its gates every year.</h2></div><p>Homecoming is the day we walk back in, together, and decide what we build with 20,000 alumni.</p></div></div></section>

<section><div class="wrap">
<div class="head"><div><p class="eyebrow">What we stand for</p><h2>Connect. Contribute. Celebrate.</h2></div></div>
<div class="pillar rv"><div class="big">C</div><div><h2>Connect</h2><p class="lede mt">Find your batch. Find your people.</p><p class="mt">Alumni who have walked the road show those who are about to. Friends and teachers are found again, mentors appear in your field, and peers abroad know the way.</p><p class="mt"><a class="lnk" href="programmes.html?f=guide">Mentorship · Careers · Moving abroad →</a></p></div></div>
<div class="pillar rv"><div class="big">C</div><div><h2>Contribute</h2><p class="lede mt">Give back to the school and to each other.</p><p class="mt">Alumni open the first doors for the next ones through them, and return to the school and community that raised them: internships, jobs, classroom talks, and projects with open accounts.</p><p class="mt"><a class="lnk" href="programmes.html?f=doors">Internships · Jobs · Resource persons · CSR →</a></p></div></div>
<div class="pillar rv"><div class="big">C</div><div><h2>Celebrate</h2><p class="lede mt">Come home and make memories.</p><p class="mt">Stories and friendly rivalry keep the family together all year: the alumni vodcast, the inter-school competition and, above all, Homecoming.</p><p class="mt"><a class="lnk" href="programmes.html?f=celebrate">Vodcast · Inter-school competition →</a></p></div></div>
</div></section>

<section class="chalk"><div class="wrap"><div class="head"><div><p class="eyebrow">How we work</p><h2>Independent. Open. Alumni-run.</h2></div><p>The principles behind everything in this website.</p></div>
<div class="cards4">
<div class="tile rv"><h3>Independent</h3><p>MAA is an alumni-run body. No money is collected from the school.</p></div>
<div class="tile rv"><h3>Recognised</h3><p>The school gave a No Objection Certificate and signed an MOU. It recognises MAA as its alumni association and monitors its activities.</p></div>
<div class="tile rv"><h3>Open books</h3><p>Accounts are audited by an independent auditor. The school receives MAA's accounts, data and reports.</p></div>
<div class="tile rv"><h3>Child-safe</h3><p>Every programme that involves students follows the school's child-safety rules.</p></div></div></div></section>

<section><div class="wrap"><div class="head"><div><p class="eyebrow">Our story</p><h2>How MAA began</h2></div></div>
<div class="grid2h"><div class="rv"><p class="lede">MAA was started by the 2008 batch, which still spearheads it. Today it is run by a Core Council, an Organising Council, committees and a representative from every batch.</p><p class="mt"><a class="btn line" href="team.html">Meet the team {ARW}</a></p></div>
<div class="rv">{ph("The 2008 batch","r43")}</div></div></div></section>
{HAND}
'''+foot()
out["about.html"]=h

# PROGRAMMES
cards=''.join(prog_card(p) for p in PROGS)
h=head("Programmes · Mahatma Alumni Association","Nine programmes, four purposes: guide, open doors, give back, connect and celebrate. Find where you fit in.","programmes.html")
h+=f'''
<section class="pagehead"><div class="wrap"><p class="eyebrow">Programmes</p><h1 class="mt">Nine programmes, four purposes.</h1><p class="lede mt">Every one is optional. Pick what suits your life, and give as much or as little time as you choose.</p></div></section>
<section><div class="wrap">
<div class="tabs" id="filters" role="tablist"><button class="tab on" data-f="all">All nine</button><button class="tab" data-f="guide">A · Guide</button><button class="tab" data-f="doors">B · Open doors</button><button class="tab" data-f="back">C · Give back</button><button class="tab" data-f="celebrate">D · Connect and celebrate</button></div>
<p class="hand mt" id="fnote" style="min-height:1.6em"></p>
<div class="progs mt">{cards}</div>
<p class="mt2 center"><span class="hand">Every programme is a proposal until the council confirms it. Dates are indicative.</span></p></div></section>

<section class="feature"><div class="wrap"><div class="head"><div><p class="eyebrow">What's in it for the alumni</p><h2>You get far more than a reunion</h2></div></div>
<div class="cards4">
<div class="tile light rv"><h3>Belong</h3><ul><li>Friends and teachers found again</li><li>A school that still counts you as its own</li><li>Pride in where you began</li></ul></div>
<div class="tile light rv"><h3>Grow</h3><ul><li>Mentors in your field</li><li>Career guidance from people who have done it</li><li>Peers abroad who know the way</li></ul></div>
<div class="tile light rv"><h3>Earn</h3><ul><li>Warm introductions to jobs</li><li>Trusted candidates and interns for your own team</li><li>Business among batchmates</li></ul></div>
<div class="tile light rv"><h3>Give</h3><ul><li>A classroom talk, in the school you remember</li><li>A project you can see and follow</li><li>A story told on the vodcast</li></ul></div></div>
<p class="mt2 hand center">What it costs: a registration, and as much or as little time as you choose.</p></div></section>

<section><div class="wrap"><div class="head"><div><p class="eyebrow">What's in it for the school</p><h2>A school with 20,000 people behind it</h2></div></div>
<div class="cards4">
<div class="tile light rv"><h3>Students</h3><ul><li>Role models they can meet</li><li>Career talks and internships</li><li>A stage in the inter-school competition</li></ul></div>
<div class="tile light rv"><h3>Teachers</h3><ul><li>Guest speakers for their classes</li><li>Volunteers for events</li><li>Recognition from former students</li></ul></div>
<div class="tile light rv"><h3>Resources</h3><ul><li>Skills and time on tap</li><li>Funds for projects, tracked openly</li><li>CSR support from alumni companies</li></ul></div>
<div class="tile light rv"><h3>Standing</h3><ul><li>Alumni who stay connected and proud</li><li>Stories of where graduates went</li><li>Eight schools working as one family</li></ul></div></div>
<p class="mt2 hand center">What the school gives: a point of contact, permission for visits, and child-safety rules that every programme follows.</p></div></section>

<section class="feature"><div class="wrap"><div class="head"><div><p class="eyebrow">The first six months</p><h2>From one day to a year-round network</h2></div></div>{roadmap()}</div></section>
{HAND}
'''+foot()
out["programmes.html"]=h

# HOMECOMING
h=head("Homecoming 2026 · Mahatma Alumni Association","Homecoming 2026 on 27 December, with School Visit Days on 25 and 26 December. Register at mahatmaschools.com.","homecoming.html")
h+=f'''
<section class="pagehead"><div class="wrap grid2h"><div><p class="eyebrow">Homecoming 2026</p><h1 class="mt">Come home on 27 December.</h1><p class="lede mt">Three days, one reunion. Walk the corridors on the 25th and 26th, then join the whole family on the 27th.</p>
<div class="cta mt2" style="display:flex;gap:14px;flex-wrap:wrap"><a class="btn solid" href="{REG}">Register · ₹1,299 + GST {ARW}</a><a class="btn line" href="#timetable">See the timetable</a></div></div>
<div><p class="hand" style="font-size:1.9rem">Days until the last bell</p>{countdown()}<p class="fine2">Sunday, 27 December 2026 · Madurai</p></div></div></section>

<section><div class="wrap"><div class="head"><div><p class="eyebrow">Why come</p><h2>One day that starts everything else</h2></div></div>
<div class="cards3">
<article class="note-card rv"><div class="n">01</div><h3>Reconnect</h3><p>Batches find each other, and the teachers who shaped them.</p></article>
<article class="note-card rv"><div class="n">02</div><h3>Launch</h3><p>The MAA app and the programmes you can join. The network gets a place to live after the day ends.</p></article>
<article class="note-card rv"><div class="n">03</div><h3>Commit</h3><p>Sign-ups for mentors, speakers, employers and sponsors. Goodwill becomes a name on a list, with a date next to it.</p></article></div></div></section>

<section class="feature" id="timetable"><div class="wrap"><div class="head"><div><p class="eyebrow">Your timetable</p><h2>Three days, three periods</h2></div><p>Come to one or come to all.</p></div>
<div class="tt-wrap"><table class="tt"><thead><tr><th>Day</th><th>What happens</th><th>Good to know</th></tr></thead><tbody>
<tr><td>Fri 25 Dec</td><td><span class="tag">School Visit Day</span>Walk your old corridors. Games, classrooms, photos, family.</td><td>10 am to 4 pm · free · lunch provided · alumni and family</td></tr>
<tr><td>Sat 26 Dec</td><td><span class="tag">School Visit Day</span>More games, more memories. Offer a topic to talk about as a resource person.</td><td>10 am to 4 pm · free · lunch provided · alumni and family</td></tr>
<tr><td>Sun 27 Dec</td><td><span class="tag gold">Homecoming</span>Programme, panel, networking session, lunch and the launch of the MAA app.</td><td>Ticket ₹1,299 + GST · register at mahatmaschools.com</td></tr></tbody></table></div>
<p class="mt hand center">Sports for all batches on 25 and 26 December: free, mixed batches, campus to be announced.</p></div></section>

<section><div class="wrap grid2h"><div><p class="eyebrow">Before the big day</p><h2 class="mt">Live webinar with Ma'am</h2>
<p class="mt">Saturday, 31 October at 10 am, on YouTube. Premalatha Ma'am addresses alumni, and the webinar settles all your questions about Homecoming. Free, for every batch.</p>
<p class="mt"><a class="btn line" href="#" data-todo="YouTube link">YouTube link coming soon</a></p></div>
<div>{ph("Webinar poster","r43")}</div></div></section>

<section class="feature" id="faq"><div class="wrap"><div class="head"><div><p class="eyebrow">Questions</p><h2>The FAQ</h2></div></div>
<div class="faq">
<details><summary>When is Homecoming?</summary><p>Sunday, 27 December 2026, in Madurai. The School Visit Days are on Friday 25 and Saturday 26 December.</p></details>
<details><summary>How do I register, and what does it cost?</summary><p>Register at {REG.replace('https://','')}. The ticket is ₹1,299 + GST.</p></details>
<details><summary>What happens on the day?</summary><p>The programme, a panel, a networking session, lunch for all attendees and the launch of the MAA app.</p></details>
<details><summary>What are the School Visit Days?</summary><p>Free visits to the school from 10 am to 4 pm, with lunch provided, for alumni and family. Sign up through the visit form (link coming soon).</p></details>
<details><summary>Can I bring my family?</summary><p>Yes, to the School Visit Days. Please mention the number in the visit form.</p></details>
<details><summary>Do I have to join any programme?</summary><p>No. Every programme is optional. You choose how much time to give.</p></details>
<details><summary>Who do I contact?</summary><p>Write to <a href="mailto:{MAIL}">{MAIL}</a>.</p></details></div></div></section>
{HAND}
'''+foot()
out["homecoming.html"]=h

# TEAM
h=head("The team · Mahatma Alumni Association","How MAA is organised: the Core Council, the Organising Council, committees and a representative for every batch.","team.html")
persons=lambda names:''.join(f'<div class="person rv">{ph(n,"r45")}<h3>[Name]</h3><span>{n}</span></div>' for n in names)
h+=f'''
<section class="pagehead"><div class="wrap"><p class="eyebrow">The team</p><h1 class="mt">Alumni, running it for alumni.</h1><p class="lede mt">Started by the 2008 batch, which still spearheads it. Every batch has a voice through its representative.</p></div></section>
<section><div class="wrap"><div class="head"><div><p class="eyebrow">Leadership</p><h2>Core Council</h2></div><p>Replace the placeholders with names, roles and photos.</p></div>
<div class="org"><div class="person rv">{ph("Arun Kesav","r45")}<h3>Arun Kesav</h3><span>Leads the association</span></div>{persons(["Core council","Core council","Core council"])}</div></div></section>
<section class="feature"><div class="wrap"><div class="head"><div><p class="eyebrow">The wider team</p><h2>Organising Council and committees</h2></div></div>
<div class="org">{persons(["Organising council","Organising council","Organising council","Organising council"])}</div>
<h3 class="mt2">Committees</h3><div class="chips mt"><span class="chip">Cultural</span><span class="chip">Sponsorship</span><span class="chip">Program and Execution</span><span class="chip">Event and Planning</span><span class="chip">Catering</span></div></div></section>
<section><div class="wrap grid2h"><div><p class="eyebrow">Batch representatives</p><h2 class="mt">One representative for every batch</h2><p class="mt">Batch representatives link the councils and the batches. They carry your questions up and the news down. Not sure who your representative is? Write to us.</p><p class="mt"><a class="btn line" href="mailto:{MAIL}?subject=Who%20is%20my%20batch%20representative%3F">Find my batch rep {ARW}</a></p></div>
<div>{ph("Batch representatives","r43")}</div></div></section>
{HAND}
'''+foot()
out["team.html"]=h

# JOIN
h=head("Join · Mahatma Alumni Association","Register for Homecoming, sign up for School Visit Days and put your hand up for a programme.","join.html")
h+=f'''
<section class="pagehead"><div class="wrap"><p class="eyebrow">Join</p><h1 class="mt">Mark your attendance.</h1><p class="lede mt">No homework. Four small steps, and you are on the register for life.</p></div></section>
<section><div class="wrap"><div class="steps">
<div class="step rv"><div><h3>Register for Homecoming</h3><p>Sunday, 27 December 2026. ₹1,299 + GST.</p></div><a class="btn solid" href="{REG}">Register {ARW}</a></div>
<div class="step rv"><div><h3>Sign up for School Visit Days</h3><p>25 and 26 December, 10 am to 4 pm. Free, with lunch, for alumni and family.</p></div><a class="btn line" href="#" data-todo="School Visit sign-up form">Sign up {ARW}</a></div>
<div class="step rv"><div><h3>Put your hand up</h3><p>Mentor, speak, hire, guest, organise or support. Tell us below.</p></div><a class="btn line" href="#raise">Choose {ARW}</a></div>
<div class="step rv"><div><h3>Find your batch</h3><p>Tell your batchmates. Ask for your batch representative.</p></div><a class="btn line" href="mailto:{MAIL}?subject=Find%20my%20batch">Ask us {ARW}</a></div></div></div></section>

<section class="feature" id="raise"><div class="wrap grid2h">
<div><p class="eyebrow">Raise your hand</p><h2 class="mt">What would you like to do?</h2><p class="mt">Pick as many as you like. We will write back to you after Homecoming with next steps.</p></div>
<form class="mailform" data-to="{MAIL}" data-subject="I would like to help">
<label>Your name<input name="name" required></label>
<label>Batch and city<input name="batch" placeholder="e.g. 2008, Chennai"></label>
<fieldset><legend>I can help as a</legend>
<label class="ck"><input type="checkbox" name="role" value="Mentor"> Mentor</label>
<label class="ck"><input type="checkbox" name="role" value="Speaker or resource person"> Speaker</label>
<label class="ck"><input type="checkbox" name="role" value="Employer (internships or jobs)"> Employer</label>
<label class="ck"><input type="checkbox" name="role" value="Vodcast guest or volunteer"> Guest or guide</label>
<label class="ck"><input type="checkbox" name="role" value="Organiser (inter-school competition)"> Organiser</label>
<label class="ck"><input type="checkbox" name="role" value="Supporter or sponsor"> Supporter</label></fieldset>
<label>Anything else?<textarea name="msg" rows="3"></textarea></label>
<button class="btn solid" type="submit">Send my hand-raise {ARW}</button><p class="fine2">This opens your email app with your note ready to send.</p></form></div></section>
'''+foot()
out["join.html"]=h

# GAME
h=head("Late for school · Mahatma Alumni Association","A little game for Mahatmites: race the 8:30 bell to the school gate, or say sorry on the dais at morning assembly.","game.html")
h+=f'''
<section class="gamesec"><div class="wrap">
<div class="gamehead"><div><p class="eyebrow">Just for fun</p><h1 class="mt">Late for school.</h1></div><p class="lede">8:20 AM. The bell rings at 8:30. You know what happens if you miss it.</p></div>
<div class="game" id="gameBox" tabindex="-1">
<canvas id="game" role="img" aria-label="Late for school: a running game. A student runs along a Madurai street to the school gate, jumping over obstacles, before the 8:30 bell."></canvas>
<div class="g-over" id="gOver" aria-live="polite">
<p class="hand" id="gKick">Bell rings at 8:30</p>
<h2 id="gTitle">Late for school</h2>
<p id="gMsg">You are 1.2 km from the gate. Jump over puddles, stray dogs, cows and runaway cycles. Every stumble costs you time. Miss the bell, and it is the dais, the mic and the whole school watching.</p>
<div class="g-btns"><button class="btn gold" id="gBtn" type="button">Start running</button><button class="btn line" id="gShare" type="button" hidden>Share</button></div>
</div></div>
<p class="g-res" id="gRes"></p>
<p class="g-help"><b>Tap</b> anywhere on the game, or press <kbd>Space</kbd> or <kbd>↑</kbd>, to jump. Hold for a higher jump.</p>
</div></section>
'''+foot().replace('<script src="assets/js/main.js" defer></script>','<script src="assets/js/main.js" defer></script>\n<script src="assets/js/game.js" defer></script>')
out["game.html"]=h

for k,v in out.items(): open(k,'w').write(v)
# 404
open('404.html','w').write(head("Lost? · MAA","Page not found","404.html")+'<section class="pagehead"><div class="wrap center"><p class="hand" style="font-size:2.4rem">Bunking class?</p><h1 style="margin-inline:auto" class="mt">This page is not on the timetable.</h1><p class="mt lede">Let us walk you back to the main gate.</p><p class="mt2"><a class="btn solid" href="index.html">Back to the homepage</a> <a class="btn line" href="game.html">Or race the bell</a></p></div></section>'+foot())
print("built",len(out)+1,"pages")
