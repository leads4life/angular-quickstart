const {chromium}=require('playwright');
const PAGES=['index.html','menu.html','takeout-delivery.html','private-events.html','about.html','contact.html','privacy.html','accessibility.html'];
const SEAM=`() => {
  const W=document.documentElement.clientWidth, decos=[], px=parseFloat;
  for (const el of document.querySelectorAll('main > section, main > section *, footer, footer *')) for (const ps of ['::before','::after']) {
    const cs=getComputedStyle(el,ps);
    if (cs.content==='none'||cs.content==='normal'||cs.display==='none'||cs.position!=='absolute'||!/url\\(|gradient/.test(cs.backgroundImage)) continue;
    const r=el.getBoundingClientRect(), h=px(cs.height), w=px(cs.width);
    const top=cs.top!=='auto'?r.top+px(cs.top):r.bottom-px(cs.bottom)-h, left=cs.left!=='auto'?r.left+px(cs.left):r.right-px(cs.right)-w;
    decos.push({top:top+scrollY,bottom:top+h+scrollY,left,right:left+w});
  }
  for (const el of document.querySelectorAll('svg.wave')) { const r=el.getBoundingClientRect(); decos.push({top:r.top+scrollY-1,bottom:r.bottom+scrollY+1,left:r.left,right:r.right}); }
  for (const el of document.querySelectorAll('.visit-band')) { const r=el.getBoundingClientRect(); decos.push({top:r.top+scrollY,bottom:r.top+scrollY+60,left:r.left,right:r.right}); }
  const blocks=[...document.querySelectorAll('main > section'),document.querySelector('footer')], seams=[];
  for (let i=1;i<blocks.length;i++){ const R=blocks[i].getBoundingClientRect(); const P=blocks[i-1].getBoundingClientRect();
    seams.push({name:blocks[i-1].className.split(' ')[0]+' -> '+(blocks[i].tagName==='FOOTER'?'FOOTER':blocks[i].className.split(' ')[0]),y:Math.min(R.top,P.bottom)+scrollY,y2:Math.max(R.top,P.bottom)+scrollY,x0:0,x1:W}); }
  const bare=[];
  for (const s of seams){ const iv=[];
    for (const d of decos){ const hit=(d.top<s.y2+2&&d.bottom>s.y-2); if(hit) iv.push([Math.max(d.left,s.x0),Math.min(d.right,s.x1)]); }
    iv.sort((a,b)=>a[0]-b[0]); let cov=0,cur=null;
    for (const [a,b] of iv){ if(b<=a)continue; if(!cur||a>cur[1]){ if(cur)cov+=cur[1]-cur[0]; cur=[a,b]; } else cur[1]=Math.max(cur[1],b); }
    if(cur)cov+=cur[1]-cur[0];
    if(cov<.9*(s.x1-s.x0)) bare.push(s.name+' ('+Math.round(100*cov/(s.x1-s.x0))+'%)'); }
  return {n:seams.length,bare}; }`;
const SHAPE=`() => { const out=[]; let n=0;
  for (const img of document.querySelectorAll('main img')) {
    if (img.closest('.hero, .page-hero, .home-hero')||img.parentElement.classList.contains('photo-band')||img.getAttribute('aria-hidden')==='true') continue;
    n++; let ok=false, el=img;
    for (let i=0;i<5&&el&&!ok;i++,el=el.parentElement){ const cs=getComputedStyle(el), mask=cs.maskImage||cs.webkitMaskImage||'none';
      const rad=['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius'].map(k=>parseFloat(cs[k])||0);
      if(mask!=='none'||cs.clipPath!=='none') ok=true; else if((el===img||/hidden|clip/.test(cs.overflow+cs.overflowX))&&Math.min(...rad)>=6) ok=true; }
    if(!ok) out.push((img.getAttribute('src')||'').split('/').pop()); }
  return {n,out}; }`;
const FIRST=`() => { const vh=innerHeight, hero=document.querySelector('.home-hero, .page-hero'), out=[];
  const later=[...document.querySelectorAll('main h1,main h2,main h3,main p,main li,main a,main button,main input,main label,main img,footer p,footer a')].filter(e=>!hero||!hero.contains(e));
  for (const e of later){ const r=e.getBoundingClientRect(); if(r.height&&r.top<vh-.5&&r.bottom>0) out.push('PEEKS '+(e.className||e.tagName)+'@'+Math.round(r.top)); }
  if(hero){ const hb=document.querySelector('header').getBoundingClientRect().bottom;
    for (const e of hero.querySelectorAll('.eyebrow,.eyebrow-wide,h1,p,.btn')){ const r=e.getBoundingClientRect(); if(!r.height)continue;
      if(r.top<vh-1&&r.bottom>vh+1) out.push('FOLD SLICES '+(e.className||e.tagName));
      if(r.top<hb+16) out.push('CROWDS NAV '+(e.className||e.tagName)); }
    const w=hero.querySelector('svg.wave'); if(w){ const wr=w.getBoundingClientRect();
      for (const e of hero.querySelectorAll('h1,p,.btn')){ const r=e.getBoundingClientRect(); if(r.bottom>wr.top+4) out.push('UNDER WAVE '+(e.className||e.tagName)); } } }
  return out; }`;
(async()=>{
  const port=process.argv[2]||'8765', b=await chromium.launch(); let bare=0,seams=0,sq=0,imgs=0,bad=0;
  for (const w of [1536,1024,768,390]) { const ctx=await b.newContext({viewport:{width:w,height:800},isMobile:w<760});
    for (const p of PAGES){ const pg=await ctx.newPage(); await pg.route(/fonts\\./,r=>r.abort()); await pg.goto(`http://localhost:${port}/${p}`); await pg.waitForTimeout(120);
      const r=await pg.evaluate(`(${SEAM})()`); seams+=r.n; for(const x of r.bare){bare++; if(port==='8765')console.log('BARE',w,p,x);}
      if(w!==1024){ const s=await pg.evaluate(`(${SHAPE})()`); imgs+=s.n; for(const x of s.out){sq++; if(port==='8765')console.log('SQUARE',w,p,x);} }
      await pg.close(); } await ctx.close(); }
  console.log(`[${port}] SEAMS ${seams} checked, ${bare} bare | SHAPES ${imgs} photos, ${sq} square`);
  for (const [w,h] of [[1536,696],[1920,969],[1440,789],[1366,657],[1280,720],[768,1024],[390,844],[390,664]]) {
    const ctx=await b.newContext({viewport:{width:w,height:h},isMobile:w<760});
    for (const p of PAGES){ const pg=await ctx.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message)); await pg.route(/fonts\\./,r=>r.abort());
      await pg.goto(`http://localhost:${port}/${p}`); await pg.waitForTimeout(150);
      const iss=await pg.evaluate(`(${FIRST})()`); const ov=await pg.evaluate('document.documentElement.scrollWidth-innerWidth');
      if(ov>0) iss.push('OVERFLOW '+ov); if(errs.length) iss.push('ERR '+errs[0]);
      if(iss.length){bad++; if(port==='8765')console.log('BAD',p,`${w}x${h}`,iss.slice(0,5).join(' | '));}
      await pg.close(); } await ctx.close(); }
  console.log(`[${port}] FIRST-SCREEN BAD COUNT ${bad}`); await b.close(); })();
