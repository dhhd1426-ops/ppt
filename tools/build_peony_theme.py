import base64
src=open('/home/claude/ppt/android/app/src/main/assets/index.html').read()
def d(n): return 'data:image/webp;base64,'+base64.b64encode(open(f'/tmp/claude-0/w/cut/{n}.webp','rb').read()).decode()
def rep(old,new):
    global src
    assert src.count(old)==1, (src.count(old), old[:90])
    src=src.replace(old,new)

# ---------------------------------------------------------------- CSS
CSS=r"""
/* ================= 主题：金线牡丹 =================
   Ivory silk and gold thread, taken from the peony sheets: the ground is champagne, the paper is warm white inside a
   gold double rule, the round window is the gold medallion, rain becomes drifting gold dust and every plant is a peony. */
:root[data-skin="peony"]{
  --ground:#e8dcc4; --sheet:#fbf7ee; --ink:#4a3a28; --ink-wet:#a8844a; --ink-soft:#8a7558;
  --night:#f3ead9; --moon:#a5803f; --bar:rgba(251,247,238,.92); --rule:rgba(168,132,74,.35); --gold:#b08a48;
}
[data-skin="peony"] .ground{background:var(--cloud) 6% 10%/46% auto no-repeat,var(--cloud) 96% 84%/40% auto no-repeat,
  radial-gradient(ellipse 70% 50% at 30% 18%,#f8f2e6,rgba(248,242,230,0)),radial-gradient(ellipse 60% 50% at 80% 90%,#f3e9d6,rgba(243,233,214,0)),#e8dcc4}
[data-skin="peony"] .mist{display:none}
[data-skin="peony"] #leaves{mix-blend-mode:multiply;filter:blur(6px)}
[data-skin="peony"] #leaves.on{opacity:.45}
[data-skin="peony"] .sheet{box-shadow:0 22px 50px rgba(110,84,44,.22),0 0 0 1px rgba(176,138,72,.25)}
[data-skin="peony"] .sheet::after{content:"";position:absolute;inset:12px;border:1px solid rgba(176,138,72,.55);outline:1px solid rgba(176,138,72,.28);outline-offset:4px;pointer-events:none;z-index:4}
[data-skin="peony"] .band{display:none}
[data-skin="peony"] .plate{background:linear-gradient(170deg,#f8f2e6,#efe3cb 70%,#e9dbbe)}
[data-skin="peony"] .plate .bg{filter:none;background-size:120% auto;background-repeat:no-repeat;background-position:10% 26%}
[data-skin="peony"] .plate .bg.on{opacity:.55}
[data-skin="peony"] .num{color:var(--moon)}
[data-skin="peony"] .num i{background:rgba(165,128,63,.55)}
[data-skin="peony"] .ring{filter:drop-shadow(0 6px 14px rgba(110,84,44,.2))}
[data-skin="peony"] .hint.dark{color:var(--ink-soft)}
[data-skin="peony"] .grow.lit{filter:drop-shadow(0 6px 12px rgba(110,84,44,.16))}
[data-skin="peony"] .touchink{mix-blend-mode:normal}
[data-skin="peony"] .home-head{color:#5b4630}
[data-skin="peony"] .home-head h1{text-shadow:none}
[data-skin="peony"] .book-note{color:#6d5a40}
[data-skin="peony"] .slot{background:linear-gradient(90deg,rgba(176,138,72,.12),rgba(176,138,72,.05) 12%,rgba(176,138,72,.05));box-shadow:inset 0 0 0 1px rgba(176,138,72,.22)}
[data-skin="peony"] .plank{background:linear-gradient(#f7efdd,#e2d2b0 60%,#cdb88e);box-shadow:0 10px 18px rgba(110,84,44,.22),0 -1px 0 #c9a45e inset}
[data-skin="peony"] .book{box-shadow:0 14px 22px rgba(110,84,44,.28),0 2px 4px rgba(110,84,44,.2)}
[data-skin="peony"] .cover{background-color:#f3eadb!important;background-size:118% auto!important;background-position:20% 130%!important;background-repeat:no-repeat!important;box-shadow:inset 0 0 0 5px #f3eadb,inset 0 0 0 6px rgba(176,138,72,.6)}
[data-skin="peony"] .cover::before{background:linear-gradient(180deg,rgba(250,245,235,0) 50%,rgba(233,219,190,.35))}
[data-skin="peony"] .cover::after{background:linear-gradient(90deg,rgba(110,84,44,.18),rgba(255,255,255,.3) 55%,rgba(110,84,44,.04))}
[data-skin="peony"] .cover .band{display:none}
[data-skin="peony"] .cover .t{color:#4a3a28;text-shadow:none}
[data-skin="peony"] .fly{box-shadow:0 20px 40px rgba(110,84,44,.3)}
/* theme switch on the shelf */
.skins{display:flex;gap:2px;padding:3px;border-radius:999px;background:rgba(242,239,226,.16);border:1px solid rgba(243,239,230,.3)}
.skins button{font-size:12px;letter-spacing:.12em;color:var(--moon);padding:5px 12px}
.skins button[aria-pressed="true"]{background:rgba(242,239,226,.9);color:#22362a}
[data-skin="peony"] .skins{background:rgba(255,252,245,.55);border-color:rgba(176,138,72,.4)}
[data-skin="peony"] .skins button{color:#6d5a40}
[data-skin="peony"] .skins button[aria-pressed="true"]{background:#fbf7ee;color:#4a3a28;box-shadow:0 0 0 1px rgba(176,138,72,.5)}
.home-head .side{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
/* peony-only: hanging bouquets, butterflies */
.grow.hang,.grow.hang img{transform-origin:50% 0}
.grow.hang.on{animation-name:hangIn}
.grow.hang.off{animation-name:hangOut}
.grow.hang.on img{animation-name:sway}
@keyframes hangIn{from{opacity:var(--o);clip-path:inset(0 -20% 100% -20%);transform:scaleY(.85)}to{opacity:var(--o);clip-path:inset(0 -20% -20% -20%);transform:none}}
@keyframes hangOut{from{opacity:var(--o);clip-path:inset(0 -20% -20% -20%)}to{opacity:0;clip-path:inset(0 -20% 100% -20%)}}
.bf{position:absolute;left:0;top:0;z-index:3;pointer-events:none;will-change:transform;opacity:0}
.bf img{display:block;width:100%;height:auto;max-width:100%;filter:drop-shadow(0 4px 6px rgba(110,84,44,.22))}
.bfw{transform-origin:50% 50%;animation:flap .2s ease-in-out infinite alternate}
.bf.side .bfw{transform-origin:70% 75%;animation-name:flapSide}
.bf.rest .bfw{animation:flapRest 4.6s ease-in-out infinite}
.bf.side.rest .bfw{animation-name:flapRestSide}
@keyframes flap{from{transform:scaleX(1)}to{transform:scaleX(.28)}}
@keyframes flapSide{from{transform:none}to{transform:scaleY(.5) skewX(-8deg)}}
@keyframes flapRest{0%,62%,100%{transform:scaleX(1)}67%{transform:scaleX(.42)}72%{transform:scaleX(1)}77%{transform:scaleX(.5)}82%{transform:scaleX(1)}}
@keyframes flapRestSide{0%,62%,100%{transform:none}67%{transform:scaleY(.55)}72%{transform:none}77%{transform:scaleY(.6)}82%{transform:none}}
.home .bf{position:fixed;z-index:3}
@media (prefers-reduced-motion: reduce){.bfw{animation:none!important}}
"""
rep('</style>\n</head>', CSS+'</style>\n</head>')
rep('<title>手帐书架</title>','<title>手帐主题</title>')

# the skin is chosen before anything is drawn
rep('<body>\n','<body>\n<script>(()=>{let s="ink";try{s=localStorage.getItem("shouzhang-skin")||"ink"}catch(_){}document.documentElement.dataset.skin=s==="peony"?"peony":"ink";})();</script>\n')

# shelf header gets the switch
rep('<header class="home-head"><h1>手帐</h1><p id="shelfNote">书架</p></header>',
    '<header class="home-head"><h1>手帐</h1><div class="side"><div class="skins" role="group" aria-label="主题"><button type="button" data-skin="ink">水墨荷塘</button><button type="button" data-skin="peony">金线牡丹</button></div><p id="shelfNote">书架</p></div></header>')

# ---------------------------------------------------------------- JS: the peony skin's materials
PJS="""
const PEONY=document.documentElement.dataset.skin==='peony';
const PIMG={gold:"%s",dark:"%s",branch:"%s",tassel:"%s",sprig:"%s",cloud:"%s",medal:"%s",flyfl:"%s",blossom:"%s"};
if(PEONY)document.documentElement.style.setProperty('--cloud',`url(${PIMG.cloud})`);
""" % tuple(d(n) for n in ['peony_gold','peony_dark','peony_branch','peony_tassel','gold_sprig','cloud_gold','medallion','flyflower','blossom'])
rep("""const INK=""", PJS+"""let INK=""")
rep("""const $=id=>document.getElementById(id);""","""if(PEONY)INK=PIMG.blossom;
const $=id=>document.getElementById(id);""")

# chapters: the plate shows a sweep of gold cloud instead of a dark painting
rep("""const CHAPTERS=[""","""let CHAPTERS=[""")
rep("""/* ---------- scenery from the 李清照 deck, tied to paragraphs ---------- */""",
"""if(PEONY)CHAPTERS=CHAPTERS.map((c,i)=>({...c,img:PIMG.cloud,r:[-6,5,-3][i]}));
/* ---------- scenery from the 李清照 deck, tied to paragraphs ---------- */""")

# decor: gold cloud and a drifting gold flower replace houses, bamboo and lotus leaves
rep("""const DECOR=[""","""const DECOR=PEONY?[
  {k:'cloud',at:0,side:'right',x:'-30px',y:-36,w:'clamp(150px,34vw,260px)',fx:'drift',dur:3600,delay:500,o:.7,cls:'',from:'80px'},
  {k:'flyfl',at:6,side:'left',x:'-20px',y:-18,w:'clamp(70px,14vw,110px)',fx:'drift',dur:3000,delay:700,o:.85,cls:'',from:'-70px'},
  {k:'cloud',at:12,side:'center',y:-60,w:'clamp(160px,36vw,260px)',fx:'circle',dur:2000,delay:500,o:.45,cls:''},
  {k:'cloud',at:17,side:'left',x:'-40px',y:-30,w:'clamp(150px,32vw,240px)',fx:'drift',dur:4200,delay:400,o:.6,cls:'',from:'-110px'},
  {k:'flyfl',at:19,side:'right',x:'-14px',y:-10,w:'clamp(64px,13vw,100px)',fx:'drift',dur:3000,delay:600,o:.85,cls:'',from:'70px',rest:'scaleX(-1)'},
  {k:'tassel',at:22,side:'right',x:'6%',y:-260,w:'clamp(120px,28vw,210px)',fx:'ascend',dur:1200,delay:700,o:.95,cls:'sway'},
  {k:'cloud',at:22,side:'bottom',y:0,w:'100%',fx:'ascend',dur:1400,delay:1300,o:.55,cls:''},
]:[""")
rep("""const IMG={""","""const IMG=PEONY?PIMG:{""")

# ring: the gold medallion, unmasked, morphing between a large chapter pose and a small corner pose
rep("""ring.innerHTML=`<defs>""","""if(PEONY)ring.innerHTML=CHAPTERS.map((c,i)=>`<image href="${PIMG.medal}" x="0" y="0" width="100" height="100" opacity="${i?0:1}" data-ch="${i}"/>`).join('');
else ring.innerHTML=`<defs>""")
rep("""  if(type==='chapter'){
    const s=Math.min(H*1.05,W*1.25);""","""  if(PEONY){
    if(type==='chapter'){const s=Math.min(H*.6,W*.9);ring.style.setProperty('--rs',s+'px');ring.style.setProperty('--rx',(W-s*.74)+'px');ring.style.setProperty('--ry',(H*.06)+'px');}
    else{const s=Math.max(72,Math.min(W*.17,112));ring.style.setProperty('--rs',s+'px');ring.style.setProperty('--rx',(W-s*1.05)+'px');ring.style.setProperty('--ry',(s*.28)+'px');}
    spin=CHAPTERS[ch].r+(type==='chapter'?0:(pageNo%3-1)*4); ring.style.setProperty('--rr',spin+'deg'); ring.style.setProperty('--ro',1); return;
  }
  if(type==='chapter'){
    const s=Math.min(H*1.05,W*1.25);""")

# grow: peonies only, a different one each time
rep("""const GROW=[""","""const GROW=PEONY?[
  {k:'dark',ch:0,side:'left',x:'-8%',w:'clamp(210px,54%,420px)',o:.96,cls:'lit',delay:700},
  {k:'gold',ch:1,side:'right',x:'-9%',w:'clamp(220px,58%,440px)',o:.96,cls:'lit',delay:500},
  {k:'branch',ch:2,side:'right',x:'-2%',w:'clamp(150px,36%,270px)',o:.96,cls:'lit',delay:900},
  {k:'tassel',ch:2,side:'left',x:'6%',w:'clamp(110px,26%,200px)',o:.95,cls:'lit hang',delay:400},
  {k:'branch',t:0,side:'right',x:'-3%',w:'clamp(110px,26%,190px)',o:.8,cls:''},
  {k:'dark',t:1,side:'left',x:'-6%',w:'clamp(150px,36%,260px)',o:.75,cls:''},
  {k:'branch',t:2,side:'left',x:'-2%',w:'clamp(110px,26%,190px)',o:.8,cls:''},
  {k:'dark',t:3,side:'right',x:'-6%',w:'clamp(150px,36%,260px)',o:.75,cls:''},
  {k:'gold',t:4,side:'right',x:'-7%',w:'clamp(160px,38%,280px)',o:.75,cls:''},
]:[""")
rep("""const GIMG={""","""const GIMG=PEONY?PIMG:{""")
rep("""el.style.width=G.w; el.style.bottom='0';""","""el.style.width=G.w; if(/hang/.test(G.cls))el.style.top='0'; else el.style.bottom='0';""")

# ---------------------------------------------------------------- butterflies (peony only)
BF=r"""
/* ---------- butterflies: fly in (起), settle (顿), flutter now and then (铺), leave when the page turns (收) ---------- */
const BIMG=PEONY?{a:"%s",b:"%s",c:"%s",d:"%s",e:"%s"}:{};
const BSIDE={d:1,e:1};
function mkBf(k,w){const el=document.createElement('div');el.className='bf'+(BSIDE[k]?' side':'');el.style.width=w+'px';
  el.innerHTML=`<div class="bfw"><img src="${BIMG[k]}" alt=""></div>`;return el;}
function flightPath(x0,y0,x1,y1,n,wob){const kf=[];for(let j=0;j<=n;j++){const u=j/n,e=1-Math.pow(1-u,2.2);
  const x=x0+(x1-x0)*e+Math.sin(u*Math.PI*3)*wob*(1-u), y=y0+(y1-y0)*e+Math.sin(u*Math.PI*5+.6)*wob*.7*(1-u);
  const tilt=Math.sin(u*Math.PI*4)*14*(1-u);kf.push({transform:`translate(${x}px,${y}px) rotate(${tilt}deg)`,opacity:u<.12?u/.12:1});}return kf;}
function bfLand(el,from,to,dur,delay){
  el.classList.remove('rest'); el._at=to;
  const a=el.animate(flightPath(from[0],from[1],to[0],to[1],24,Math.max(40,Math.abs(to[0]-from[0])*.12)),{duration:reduceMotion?1:dur,delay:reduceMotion?0:delay,easing:'linear',fill:'forwards'});
  el._anim=a; a.onfinish=()=>{ if(el._anim!==a)return; el.classList.add('rest');
    el._anim=el.animate([{transform:`translate(${to[0]}px,${to[1]}px) rotate(-2deg)`},{transform:`translate(${to[0]+2}px,${to[1]-3}px) rotate(3deg)`},{transform:`translate(${to[0]}px,${to[1]}px) rotate(-2deg)`}],{duration:5200,iterations:Infinity,easing:'ease-in-out'});};
}
function bfLeave(el,dx){ if(!el._at)return; const f=el._at; el._at=null; el.classList.remove('rest');
  el._anim=el.animate(flightPath(f[0],f[1],f[0]+dx,f[1]-260,14,30).map((k,j,arr)=>({...k,opacity:1-j/(arr.length-1)})),{duration:reduceMotion?1:1400,easing:'ease-in',fill:'forwards'}); }
const BFS={};
if(PEONY){const layer=document.createElement('div');layer.setAttribute('aria-hidden','true');sheet.insertBefore(layer,$('hint'));
  ['a','b','c','d','e'].forEach(k=>{BFS[k]=mkBf(k,60);layer.appendChild(BFS[k]);});}
function bflyFor(i){
  const P=pages[i];
  if(P.type==='chapter')return [{k:'b',w:.2,max:120,from:[-.2,.12],to:[.36,.62]},{k:'d',w:.24,max:150,from:[-.2,.05],to:[.3,.24]},{k:'e',w:.26,max:160,from:[1.2,.2],to:[.6,.62]}][P.ch];
  const n=pages.slice(0,i).filter(q=>q.type==='text').length;
  if(i===pages.length-1)return {k:'a',w:.12,max:80,from:[-.15,.4],to:[.3,.72]};
  if(n%%2)return null;
  return [{k:'c',w:.09,max:60,from:[-.15,.3],to:[.5,.035]},{k:'a',w:.11,max:72,from:[1.15,.5],to:[.3,.03]},{k:'c',w:.09,max:60,from:[1.1,.1],to:[.66,.9]}][(n/2)%%3];
}
let bfCur=null;
function bflyTo(i,lead){
  if(!PEONY)return;
  const B=bflyFor(i), W=sheet.clientWidth, H=sheet.clientHeight;
  if(bfCur&&(!B||B.k!==bfCur.k))bfLeave(BFS[bfCur.k],bfCur.to[0]<.5?-W*.6:W*.6);
  if(B){const el=BFS[B.k], w=Math.min(B.max,W*B.w); el.style.width=w+'px';
    const to=[B.to[0]*W-w/2,B.to[1]*H], cont=el._at&&bfCur&&bfCur.k===B.k, from=cont?el._at:[B.from[0]*W,B.from[1]*H];
    bfLand(el,from,to,cont?2200:3400,lead+600);}
  bfCur=B?{...B}:null;
}
""" % tuple(d(n) for n in ['bfly_a','bfly_b','bfly_c','bfly_d','bfly_e'])
rep("""/* ---------- scenery placement and motion ---------- */""", BF+"""/* ---------- scenery placement and motion ---------- */""")
rep("""  growTo(i,P.type==='chapter'?0:(prevType?(prevType==='chapter'?700:350):0)+400);""",
"""  growTo(i,P.type==='chapter'?0:(prevType?(prevType==='chapter'?700:350):0)+400);
  bflyTo(i,P.type==='chapter'?300:700);""")
rep("""decorEls.forEach(d=>{if(d.at>=0)d.el.classList.remove('on','out');}); show(to);""",
"""decorEls.forEach(d=>{if(d.at>=0)d.el.classList.remove('on','out');}); Object.values(BFS).forEach(b=>{b.getAnimations().forEach(a=>a.cancel());b._at=null;}); bfCur=null; show(to);""")

# touch: a small gold blossom glints instead of an ink blot
rep("""  const w=60+Math.random()*40, h=w*886/743, d=document.createElement('div'); d.className='touchink';""",
"""  const w=PEONY?26+Math.random()*16:60+Math.random()*40, h=PEONY?w:w*886/743, d=document.createElement('div'); d.className='touchink';""")
rep("""opacity:.1,transform:`rotate(${Math.random()*360}deg)`});""","""opacity:PEONY?.6:.1,transform:`rotate(${Math.random()*360}deg)`});""")

# rain becomes gold dust that floats up and twinkles
rep("""function rain(dt){""","""function dust(dt){
  rainT+=dt*(1+gust*.6); gust*=.96;
  ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
  for(const r of drops){
    const ph=((rainT*.25+r.d*3)%12000)/12000, x=(r.x+.5)/1.2*W+Math.sin(ph*6.28*2+r.d)*18+gust*30*ph, y=H*(1.05-ph*1.15)+r.y*40;
    const tw=.35+.65*Math.abs(Math.sin(rainT*.0015+r.d)), rad=1+r.len*30;
    const g=ctx.createRadialGradient(x,y,0,x,y,rad*3); g.addColorStop(0,`rgba(214,176,98,${.55*tw})`); g.addColorStop(1,'rgba(214,176,98,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,rad*3,0,6.283); ctx.fill();
  }
}
function rain(dt){
  if(PEONY)return dust(dt);""")
rep("""  for(let i=0;i<n;i++)drops.push(""","""  if(PEONY)drops.length=0;
  for(let i=0;i<(PEONY?Math.round(n*.45):n);i++)drops.push(""")
rep("""lc.fillStyle='rgba(44,74,44,.22)';""","""lc.fillStyle=PEONY?'rgba(96,74,42,.16)':'rgba(44,74,44,.22)';""")

# shelf: peony plants, a peony cover, a butterfly on the book, and the theme switch
rep("""const BOOKS=[{title:'开学日',cover:""","""if(PEONY){document.querySelector('.home-plant.l img').src=PIMG.dark;document.querySelector('.home-plant.r img').src=PIMG.sprig;
  const r=document.querySelector('.home-plant.r');r.style.width='clamp(150px,30vw,260px)';r.querySelector('img').style.transform='scaleX(-1)';}
const BOOKS=[{title:'开学日',cover:PEONY?PIMG.branch:""")
rep("""$('shelfBtn').onclick=closeBook;""","""$('shelfBtn').onclick=closeBook;
document.querySelectorAll('.skins button').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.skin===(PEONY?'peony':'ink')));
  b.onclick=()=>{if(b.getAttribute('aria-pressed')==='true')return;try{localStorage.setItem('shouzhang-skin',b.dataset.skin);}catch(_){}
    document.documentElement.dataset.skin=b.dataset.skin;location.reload();};});
let homeBf=null;
function homeVisit(){ if(!PEONY||!bookBtn)return; if(!homeBf){homeBf=mkBf('a',54);$('home').appendChild(homeBf);}
  const r=bookBtn.getBoundingClientRect(), w=Math.min(64,r.width*.36); homeBf.style.width=w+'px';
  homeBf.getAnimations().forEach(a=>a.cancel()); homeBf._at=null; bfLand(homeBf,[innerWidth*1.05,innerHeight*.15],[r.left+r.width*.62-w/2,r.top-w*.62],3600,1500); }
let hv; addEventListener('resize',()=>{clearTimeout(hv);hv=setTimeout(homeVisit,300);});""")
rep("""fontsReady.then(()=>{layout();""","""fontsReady.then(()=>{layout();homeVisit();""")
open('/tmp/claude-0/w/build/index.html','w').write(src)
print(len(src))
