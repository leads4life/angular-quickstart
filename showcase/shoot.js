// Captures screenshots of the built demo for the sales page.  node shoot.js <demo_dir> <assets_dir>
const { chromium } = require('playwright'), path = require('path');
const [demo, out] = process.argv.slice(2).map(p => path.resolve(p));
const url = p => 'file://' + path.join(demo, p);
(async () => {
  const b = await chromium.launch();
  const open = async (w, h, dpr, p) => { const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr, isMobile: w < 760 }); const pg = await c.newPage(); await pg.route(/fonts\./, r => r.abort()); await pg.goto(url(p)); await pg.addStyleTag({ content: '.demo-bar{display:none!important}' }); await pg.waitForTimeout(300); return [c, pg]; };
  const jpg = { type: 'jpeg', quality: 82 };
  let [c, pg] = await open(1440, 900, 1, 'index.html'); await pg.screenshot({ path: `${out}/demo-home.jpg`, ...jpg }); await c.close();
  [c, pg] = await open(390, 844, 2, 'index.html'); await pg.screenshot({ path: `${out}/phone-home.jpg`, ...jpg }); await c.close();
  [c, pg] = await open(390, 844, 2, 'menu.html'); await pg.evaluate(() => { const e = document.getElementById('lunch'); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 70, behavior: 'instant' }); }); await pg.waitForTimeout(200); await pg.screenshot({ path: `${out}/phone-menu.jpg`, ...jpg }); await c.close();
  const el = async (p, sel, name, w = 1280) => { const [c, pg] = await open(w, 900, 1.5, p); const e = pg.locator(sel).first(); await e.scrollIntoViewIfNeeded(); await pg.waitForTimeout(150); await e.screenshot({ path: `${out}/${name}.jpg`, ...jpg }); await c.close(); };
  await el('menu.html', '#lunch', 'feat-menu');
  await el('takeout-delivery.html', '#family .combos', 'feat-order');
  await el('private-events.html', '#banquets .packages', 'feat-banquets');
  await el('contact.html', '.visit-grid', 'feat-hours');
  await el('about.html', 'section:has(#name-h)', 'feat-name');
  await el('index.html', '.signature', 'feat-signature');
  await b.close(); console.log('shots ->', out);
})();
