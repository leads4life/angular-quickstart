const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const dir=process.argv[2];
 const pages=['index','menu','takeout-delivery','private-events','about','contact','privacy','accessibility'];
 for(const w of [1280,390]){
  const ctx=await b.newContext({viewport:{width:w,height:900}});
  for(const p of pages){
   const pg=await ctx.newPage(); const errs=[];
   pg.on('pageerror',e=>errs.push(e.message));
   await pg.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());
   await pg.goto('file://'+dir+'/dist/'+p+'.html');
   await pg.waitForTimeout(300);
   const sw=await pg.evaluate(()=>document.documentElement.scrollWidth);
   if(sw>w||errs.length) console.log('PROBLEM',p,w,sw,errs);
   await pg.screenshot({path:`work/shot-${p}-${w}.png`,fullPage:true});
   await pg.close();
  }
 }
 await b.close(); console.log('done');
})();
