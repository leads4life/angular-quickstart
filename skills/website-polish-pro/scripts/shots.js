#!/usr/bin/env node
/* Full-page screenshots + contact sheets.  node shots.js --base http://localhost:8765 --dir dist --out shots [--widths 1440,390]
   Writes shots/<page>-<w>.png and shots/sheet-<w>-N.png (3 pages per sheet, 480px wide each) for one look. */
const fs = require('fs'), { chromium } = require('playwright');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const BASE = arg('base', 'http://localhost:8765'), DIR = arg('dir', 'dist'), OUT = arg('out', 'shots');
const W = arg('widths', '1440,390').split(',').map(Number);
const PAGES = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort((a, b) => (b === 'index.html') - (a === 'index.html') || a.localeCompare(b));
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const w of W) {
    const ctx = await b.newContext({ viewport: { width: w, height: 800 }, isMobile: w < 760 });
    for (const p of PAGES) {
      const pg = await ctx.newPage(); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
      await pg.goto(`${BASE}/${p}`); const h = await pg.evaluate('document.body.scrollHeight');
      for (let y = 0; y < h; y += 700) { await pg.evaluate(`window.scrollTo({top:${y},behavior:'instant'})`); await pg.waitForTimeout(40); }   // fire lazy images
      await pg.evaluate("window.scrollTo({top:0,behavior:'instant'})"); await pg.waitForTimeout(150);
      await pg.screenshot({ path: `${OUT}/${p.replace('.html', '')}-${w}.png`, fullPage: true }); await pg.close();
    }
    await ctx.close();
  }
  await b.close();
  require('child_process').execFileSync('python3', ['-c', `
import glob,sys
from PIL import Image
out,ws,pages=sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(',')
for w in ws:
  ims=[Image.open(f"{out}/{p.replace('.html','')}-{w}.png") for p in pages]
  for k in range(0,len(ims),3):
    grp=[i.resize((480,int(i.height*480/i.width))) for i in ims[k:k+3]]
    H=max(i.height for i in grp); S=Image.new('RGB',(490*len(grp)-10,H),'white')
    for j,i in enumerate(grp): S.paste(i,(j*490,0))
    if S.height>4000: S=S.resize((int(S.width*4000/S.height),4000))
    S.save(f"{out}/sheet-{w}-{k//3+1}.png")
`, OUT, W.join(','), PAGES.join(',')]);
  console.log('screenshots + sheets in', OUT);
})();
