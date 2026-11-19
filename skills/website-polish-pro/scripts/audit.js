#!/usr/bin/env node
/* website-polish-pro audit runner.
   node audit.js --base http://localhost:8765 --dir ./dist [--pages a.html,b.html] [--label after] [--json out.json]
   Runs every audit on every page and prints FAIL / WARN lines plus a summary.
   Exit code 1 if any FAIL. Run it on the saved "before" copy too: it should fail there,
   which proves the checks really detect the problems. */
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const BASE = arg('base', 'http://localhost:8765').replace(/\/$/, '');
const DIR = arg('dir', null), LABEL = arg('label', BASE), JSONOUT = arg('json', null);
let PAGES = arg('pages', null);
PAGES = PAGES ? PAGES.split(',') : DIR ? fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort() : ['index.html'];

/* ---------- in-page checks (each returns {fail:[], warn:[], n}) ---------- */
const SEAM = () => {   // every boundary between main sections / footer must carry a decoration across >=90% of its width
  const W = document.documentElement.clientWidth, decos = [], px = parseFloat, fail = [];
  for (const el of document.querySelectorAll('header, header *, main > *, main > * *, footer, footer *')) for (const ps of ['::before', '::after']) {
    const cs = getComputedStyle(el, ps);
    if (cs.content === 'none' || cs.content === 'normal' || cs.display === 'none' || cs.position !== 'absolute' || !/url\(|gradient/.test(cs.backgroundImage)) continue;
    const r = el.getBoundingClientRect(), h = px(cs.height), w = px(cs.width);
    const top = cs.top !== 'auto' ? r.top + px(cs.top) : r.bottom - px(cs.bottom) - h, left = cs.left !== 'auto' ? r.left + px(cs.left) : r.right - px(cs.right) - w;
    decos.push({ top: top + scrollY, bottom: top + h + scrollY, left, right: left + w });
  }
  // real elements that act as seam pieces: inline SVG waves/dividers, or anything marked data-seam
  for (const el of document.querySelectorAll('svg.wave, [data-seam]')) { const r = el.getBoundingClientRect(); decos.push({ top: r.top + scrollY - 1, bottom: r.bottom + scrollY + 1, left: r.left, right: r.right }); }
  const blocks = [...document.querySelectorAll('main > section, main > div, main > aside'), document.querySelector('footer')].filter(Boolean);
  let n = 0;
  for (let i = 1; i < blocks.length; i++) {
    const R = blocks[i].getBoundingClientRect(), P = blocks[i - 1].getBoundingClientRect();
    if (!R.height || !P.height) continue; n++;
    const y = Math.min(R.top, P.bottom) + scrollY, y2 = Math.max(R.top, P.bottom) + scrollY, iv = [];
    for (const d of decos) if (d.top < y2 + 2 && d.bottom > y - 2) iv.push([Math.max(d.left, 0), Math.min(d.right, W)]);
    iv.sort((a, b) => a[0] - b[0]); let cov = 0, cur = null;
    for (const [a, b] of iv) { if (b <= a) continue; if (!cur || a > cur[1]) { if (cur) cov += cur[1] - cur[0]; cur = [a, b]; } else cur[1] = Math.max(cur[1], b); }
    if (cur) cov += cur[1] - cur[0];
    const name = (blocks[i - 1].className || blocks[i - 1].tagName).toString().split(' ')[0] + ' -> ' + (blocks[i].tagName === 'FOOTER' ? 'FOOTER' : (blocks[i].className || blocks[i].tagName).toString().split(' ')[0]);
    if (cov < .9 * W) fail.push(`bare seam ${name} (${Math.round(100 * cov / W)}% covered)`);
  }
  return { n, fail, warn: [] };
};
const SHAPE = () => {  // framed photos need a soft outline (mask, clip-path or >=6px radius with clipping)
  const fail = []; let n = 0;
  for (const img of document.querySelectorAll('main img')) {
    if (img.closest('.hero, .page-hero, .home-hero, [data-fullbleed]') || img.closest('.photo-band') || img.getAttribute('aria-hidden') === 'true' || img.alt === '') continue;
    n++; let ok = false, el = img;
    for (let i = 0; i < 5 && el && !ok; i++, el = el.parentElement) {
      const cs = getComputedStyle(el), mask = cs.maskImage || cs.webkitMaskImage || 'none';
      const rad = ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius'].map(k => parseFloat(cs[k]) || 0);
      if (mask !== 'none' || cs.clipPath !== 'none') ok = true;
      else if ((el === img || /hidden|clip/.test(cs.overflow + cs.overflowX)) && Math.min(...rad) >= 6) ok = true;
    }
    if (!ok) fail.push('square photo ' + (img.getAttribute('src') || '').split('/').pop());
  }
  return { n, fail, warn: [] };
};
const FIRST = () => {  // the first screen is a composition: hero fills it, nothing from later sections peeks in, nothing sliced
  const vh = innerHeight, hero = document.querySelector('.hero, .page-hero, .home-hero, main > section'), fail = [];
  const later = [...document.querySelectorAll('main h1,main h2,main h3,main p,main li,main a,main button,main input,main label,main img,footer p,footer a')].filter(e => !hero || !hero.contains(e));
  for (const e of later) { const r = e.getBoundingClientRect(); if (r.height && r.top < vh - .5 && r.bottom > 0 && getComputedStyle(e).visibility !== 'hidden') fail.push('peeks into first screen: ' + (e.className || e.tagName) + ' @' + Math.round(r.top)); }
  if (hero) {
    const hdr = document.querySelector('header'), hb = hdr ? hdr.getBoundingClientRect().bottom : 0;
    for (const e of hero.querySelectorAll('.eyebrow,h1,p,.btn,a.button,button')) {
      const r = e.getBoundingClientRect(); if (!r.height) continue;
      if (r.top < vh - 1 && r.bottom > vh + 1) fail.push('fold slices ' + (e.className || e.tagName));
      if (r.top < hb + 16) fail.push('crowds nav ' + (e.className || e.tagName));
    }
  }
  return { n: 1, fail: fail.slice(0, 6), warn: [] };
};
const ALIGN = () => {  // sections should share one content column: compare each section's column container (outermost max-width box)
  const W = document.documentElement.clientWidth, rows = [], warn = [];
  if (W < 1000) return { n: 0, fail: [], warn };
  for (const b of [...document.querySelectorAll('main > section, main > div, footer')]) {
    if (b.matches('[data-align="free"]')) continue;
    const box = [b, ...b.querySelectorAll('*')].find(e => { const cs = getComputedStyle(e); return cs.maxWidth !== 'none' && !cs.maxWidth.endsWith('%') && e.getBoundingClientRect().width > 300 && e.getBoundingClientRect().width < W - 20; });
    if (!box) continue;
    const r = box.getBoundingClientRect(), edge = Math.round(r.left + parseFloat(getComputedStyle(box).paddingLeft));
    rows.push({ name: (b.className || b.tagName).toString().split(' ')[0], edge, width: Math.round(r.width) });
  }
  if (rows.length < 2) return { n: rows.length, fail: [], warn };
  const counts = {}; rows.forEach(r => { counts[r.edge] = (counts[r.edge] || 0) + 1; });
  const mode = +Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
  for (const r of rows) if (Math.abs(r.edge - mode) > 6) warn.push(`content column of ${r.name} starts at ${r.edge}px; most sections start at ${mode}px`);
  return { n: rows.length, fail: [], warn };
};
const BLANK = () => {  // areas that were left empty: orphan grid slots, hollow cards, lopsided columns, dead vertical runs
  const fail = [], warn = [], vis = e => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const isCard = e => { const cs = getComputedStyle(e); const bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.backgroundImage !== 'none'; const bd = ['Top', 'Right', 'Bottom', 'Left'].every(s => parseFloat(cs['border' + s + 'Width']) > 0); return bg || bd; };
  const contentBottom = e => { let b = e.getBoundingClientRect().top; for (const c of e.querySelectorAll('*')) { if (!vis(c) || c.children.length) continue; const r = c.getBoundingClientRect(); if (r.height) b = Math.max(b, r.bottom); } return b; };
  for (const g of document.querySelectorAll('main *')) {
    const cs = getComputedStyle(g); if (cs.display !== 'grid' || !vis(g)) continue;
    const kids = [...g.children].filter(vis); if (kids.length < 2) continue;
    const cols = cs.gridTemplateColumns.split(' ').filter(t => t && parseFloat(t) > 0).length;   // auto-fit leaves 0px tracks: ignore them
    const cards = kids.filter(isCard).length === kids.length;
    if (cards && cols > 1 && kids.length % cols) fail.push(`grid ${g.className || g.tagName}: last row has ${cols - kids.length % cols} empty slot(s) (${kids.length} cards in ${cols} columns)`);
    if (cards) for (const k of kids) { const r = k.getBoundingClientRect(), hollow = r.bottom - contentBottom(k) - parseFloat(getComputedStyle(k).paddingBottom); if (hollow > 90 && hollow > r.height * .35) fail.push(`hollow card in ${g.className || g.tagName}: ${Math.round(hollow)}px empty at the bottom`); }
    if (cols === 2 && kids.length === 2 && innerWidth >= 1000 && !kids.some(k => getComputedStyle(k).position === 'sticky' || k.querySelector('[style*=sticky], .toc'))) {
      const [a, b] = kids.map(k => k.getBoundingClientRect().top), ca = contentBottom(kids[0]) - a, cb = contentBottom(kids[1]) - b, gap = Math.abs(ca - cb);
      if (gap > 260) warn.push(`lopsided columns in ${g.className || g.tagName}: one side ${Math.round(gap)}px shorter`);
    }
  }
  // dead vertical runs inside main (outside the hero): nothing readable for > 240px
  const hero = document.querySelector('.hero, .page-hero, .home-hero'), hb = hero ? hero.getBoundingClientRect().bottom + scrollY : 0, iv = [];
  for (const e of document.querySelectorAll('main h1,main h2,main h3,main h4,main p,main li,main a,main img,main svg,main input,main textarea,main select,main table,main button,main summary,main blockquote,main figure,main dt,main dd')) {
    const r = e.getBoundingClientRect(); if (r.height && vis(e)) iv.push([r.top + scrollY, r.bottom + scrollY]);
  }
  const m = document.querySelector('main').getBoundingClientRect(), end = m.bottom + scrollY;
  iv.sort((a, b) => a[0] - b[0]); let y = hb;
  for (const [a, b] of iv) { if (b <= hb) continue; if (a - y > 280) fail.push(`empty vertical run of ${Math.round(a - y)}px at y=${Math.round(y)}`); y = Math.max(y, b); }
  if (end - y > 300) warn.push(`empty run of ${Math.round(end - y)}px at the end of main`);
  return { n: 1, fail: fail.slice(0, 8), warn: warn.slice(0, 4) };
};
const PLACE = () => {  // visible placeholders read as unfinished: brackets, <mark>, lorem, TBD
  const t = document.body.innerText, fail = [], warn = [];
  const br = t.match(/\[[^\]\n]{1,70}\]/g) || [], marks = document.querySelectorAll('main mark').length;
  if (br.length) fail.push(`${br.length} bracket placeholder(s): ${[...new Set(br)].slice(0, 4).join(' ')}`);
  if (marks) fail.push(`${marks} <mark> highlight(s) left on the page`);
  if (/lorem ipsum|\bTBD\b|\bXXX\b|coming soon/i.test(t)) fail.push('filler text (lorem / TBD / XXX / coming soon)');
  if (/\b555[-.\s]\d{4}\b/.test(t)) warn.push('555 phone number: confirm it is real');
  return { n: 1, fail, warn };
};

(async () => {
  const b = await chromium.launch(), out = { label: LABEL, results: [] };
  const run = async (w, h, page, checks) => {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 760, hasTouch: w < 760 }), pg = await ctx.newPage(), errs = [];
    pg.on('pageerror', e => errs.push(e.message));
    await pg.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());   // offline sandboxes: fonts fall back, layout still checked
    await pg.goto(`${BASE}/${page}`, { waitUntil: 'load' }); await pg.waitForTimeout(200);
    const res = {};
    for (const [k, fn] of Object.entries(checks)) res[k] = await pg.evaluate(`(${fn.toString()})()`);
    const ov = await pg.evaluate('document.documentElement.scrollWidth - innerWidth');
    res.BASICS = { n: 1, fail: [...(ov > 0 ? ['sideways scroll ' + ov + 'px'] : []), ...errs.map(e => 'script error: ' + e)], warn: [] };
    await ctx.close(); return res;
  };
  const plan = [
    [1536, 800, { SEAM, SHAPE, ALIGN, BLANK, PLACE }], [1024, 800, { SEAM, BLANK }], [768, 1024, { SEAM, BLANK }], [390, 844, { SEAM, SHAPE, BLANK }],
    [1536, 696, { FIRST }], [1920, 969, { FIRST }], [1440, 789, { FIRST }], [1366, 657, { FIRST }], [1280, 720, { FIRST }], [768, 1024, { FIRST }], [390, 844, { FIRST }], [390, 664, { FIRST }],
  ];
  const tot = {};
  for (const [w, h, checks] of plan) for (const p of PAGES) {
    const res = await run(w, h, p, checks);
    for (const [k, r] of Object.entries(res)) {
      tot[k] = tot[k] || { fail: 0, warn: 0 };
      for (const f of r.fail) { tot[k].fail++; console.log(`FAIL ${k} ${p} ${w}x${h}: ${f}`); }
      for (const f of r.warn) { tot[k].warn++; console.log(`WARN ${k} ${p} ${w}x${h}: ${f}`); }
      out.results.push({ check: k, page: p, viewport: `${w}x${h}`, ...r });
    }
  }
  console.log(`\n[${LABEL}] summary`);
  for (const [k, t] of Object.entries(tot)) console.log(`  ${k.padEnd(7)} ${t.fail ? 'FAIL' : 'pass'}  fails=${t.fail} warns=${t.warn}`);
  if (JSONOUT) fs.writeFileSync(JSONOUT, JSON.stringify({ ...out, totals: tot }, null, 1));
  await b.close();
  process.exit(Object.values(tot).some(t => t.fail) ? 1 : 0);
})();
